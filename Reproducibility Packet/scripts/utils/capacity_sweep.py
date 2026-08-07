"""Stage 1 of the Gate-4 capacity escalation: the width-parameterized sweep executable.

This is the Route-A module that the frozen design
`protocol/capacity-escalation-v0.1.md` (canonical SHA-256 `05109d97...`, jointly
approved at Claude Session 91 / Codex Session 91) authorizes. It exists **only** because
the approved trainer is width-locked: `dev_fit_trainer.fit_one_arm` constructs
`TemporalAttributionNet(seed=seed)` at its 32-channel default and has no capacity
argument, so a width sweep cannot be run through it without editing a jointly approved
file whose bytes are the recorded producer of ten existing checkpoints (design section
4.4, Finding Y).

What this module may do, and what it may not
--------------------------------------------
It may enumerate the sweep (plan mode) and, under a separate joint authorization naming
an approved plan's digest, fit the two C9 equivalence arms and the forty new curve arms
on the same authorized `dev` rows the approved ledger used, scoring each arm in sample.
It may not re-fit the ten approved 32-channel anchors, write into `results/dev_fit`,
read a pilot, validation or test row, spend a rollout, generate data, set a threshold,
or select a capacity. Bound 5 of the dev-fit contract governs the result: this is
development-only instrument diagnosis and capacity-search history, never a headline
result and never a capacity selection.

**Building this module is not permission to run it.** Design section 12 sequences the
gates: the design is frozen (done), this executable and its tests are reviewed (this
state), plan mode is run and its artifact reviewed, and only then is execution a fourth
and separate joint authorization.

Why the fit loop is duplicated, and what measures the duplicate
--------------------------------------------------------------
`fit_arm_at_width` below is the approved `dev_fit_trainer.fit_one_arm` body
(lines 942-995 of that file at the approved blob) with exactly one expression changed:
the network construction gains `channels=` and an explicit `enforce_rung1_band=True`.
Every **project-defined** name that body uses is imported from the approved modules
rather than retyped -- `TemporalAttributionNet`, `require_predeclared_seed`,
`deterministic_conv_precision`, `arm_loss`, `_stack`, `DevFitDataError` -- so the loss,
which is the part that is science rather than plumbing, keeps exactly one definition.
The control flow and the third-party PyTorch/NumPy expressions are necessarily copied;
no project helper wraps them.

**`_stack` is imported across a module boundary despite its leading underscore, and that
is a disclosure rather than a silent choice** (design section 4.4). It is the batching
function -- the single place a retyped copy would most plausibly diverge in a way that
changes weights -- so importing it is the smaller harm, and paying a C9 failure to
discover a hand-copied batcher had drifted would be a wasted gate.

The duplicated seam is not asserted to be equivalent; it is **measured** before use.
`equivalence_gate` (invariant C9) fits `(C1, seed 0)` and `(S, seed 4)` at 32 channels
through this module's own path and requires the resulting parameter tensors and
per-epoch loss history to be bit-identical to the approved checkpoints and ledger rows.
It refuses loudly on any difference, on a missing approved checkpoint, and on a
comparison it cannot make.

Where this executable is allowed to write
-----------------------------------------
Three locations, all of them named (design sections 6 C2 and 7.1):

1. the run root `<base>/<run_label>/`, claimed by **one atomic create that requires the
   path to be absent**; any pre-existing path -- file, empty directory or populated
   directory -- is the named terminal `X_RUN_ROOT_OCCUPIED`;
2. the sibling refusal sink `<base>/_capacity_sweep_refusals/<run_label>/<uuid>.json`,
   and `.../_unbound/<uuid>.json` for a refusal taken before a trustworthy label exists.
   It sits outside the run root **by necessity**: a refusal must never report through
   the resource whose occupancy triggered it;
3. the reserved `_equivalence/` subtree of the claimed run root, which is where C9's two
   compatibility checkpoints and their comparison artifact go, so they are inside the run
   whose gate they are and a fresh label is a fresh scratch root for free.

The two sink names are safe by construction rather than by convention: `run_label` must
match `^[a-z0-9][a-z0-9-]{2,31}$`, whose character class contains no underscore anywhere,
so no conforming label can ever name `_capacity_sweep_refusals` or `_unbound`.

One refusal deliberately persists nothing, and it is disclosed rather than hidden
---------------------------------------------------------------------------------
`X_FORBIDDEN_BASE` -- a `--base-dir` at or inside the approved `results/dev_fit`
checkpoint directory -- is the single terminal exit that writes no artifact. Every sink
this module could use is *under the base*, so persisting that refusal would itself be the
write into `results/dev_fit` that invariant C1 forbids. The refusal is printed and the
exit code is returned; the design's "every terminal exit persists an artifact" rule is
knowingly not met here, for the same reason lesson 116 exists. Recorded here rather than
discovered later.

Why the descriptive read of design section 5 lives here but is not run here
---------------------------------------------------------------------------
`headroom`, `pair_constraint`, `classify_shape`, `quantize` and `derived_label` are pure
functions of persisted primitives and carry no I/O. They are defined in this module so the
read-only analysis script invariant C7 requires -- which is a separate build and a separate
review -- imports them instead of writing a second definition of the criterion the whole
read turns on. This executable never calls them: it persists per-arm primitives, and the
analysis derives the curves.
"""

from __future__ import annotations

import argparse
import hashlib
import io
import json
import re
import sys
import time
import uuid
from decimal import Decimal, ROUND_HALF_EVEN
from pathlib import Path
from typing import Any, Mapping, Sequence

import numpy as np
import torch

from .attribution_net import TemporalAttributionNet, deterministic_conv_precision
from .dev_fit_contract import (
    DEVELOPMENT_ONLY_AUTHORITY,
    MATCHED_FIT_SUITES,
    PREDECLARED_TRAINING_SEEDS,
    DevFitContractError,
    code_identity,
    require,
    require_matched_fit_suite,
    require_predeclared_seed,
)
from .dev_fit_trainer import (
    AUTHORIZED_CONFIG_HASH,
    AUTHORIZED_MANIFEST_SHA256,
    AUTHORIZED_ROLE_INDEX_SHA256,
    DevFitDataError,
    _stack,
    arm_loss,
)
from . import dev_fit_trainer as trainer
from .protocol_p import canonical_json, canonical_text_sha256

# `analyze_dev_fit` is a top-level module under `scripts/`, which is the same directory
# that makes `utils` importable at all, so this import is available in exactly the
# contexts this module is. Design section 3 requires it: `macro_f1`, `accuracy` and
# `per_class_f1` are obtained from the approved analyzer, because a second definition of
# macro-F1 in this project would be a second definition of the quantity the read is about.
import analyze_dev_fit as approved_analysis  # noqa: E402


# ---------------------------------------------------------------------------
# Terminal exits. A name rather than a bare integer, because every artifact this
# module writes records which exit was taken.
# ---------------------------------------------------------------------------
X_PLAN_OK = "X_PLAN_OK"
X_SWEEP_OK = "X_SWEEP_OK"
X_CONTRACT_REFUSED = "X_CONTRACT_REFUSED"
X_DATA_MISSING = "X_DATA_MISSING"
X_PLAN_INCOMPLETE = "X_PLAN_INCOMPLETE"
X_OUTPUT_DIRTY = "X_OUTPUT_DIRTY"
X_RUN_ROOT_OCCUPIED = "X_RUN_ROOT_OCCUPIED"
X_PLAN_UNAUTHORIZED = "X_PLAN_UNAUTHORIZED"
X_EQUIVALENCE_FAILED = "X_EQUIVALENCE_FAILED"
X_FORBIDDEN_BASE = "X_FORBIDDEN_BASE"

EXIT_CODES: dict[str, int] = {
    X_PLAN_OK: 0,
    X_SWEEP_OK: 0,
    X_CONTRACT_REFUSED: 3,
    X_DATA_MISSING: 4,
    X_PLAN_INCOMPLETE: 5,
    X_OUTPUT_DIRTY: 6,
    X_RUN_ROOT_OCCUPIED: 7,
    X_PLAN_UNAUTHORIZED: 8,
    X_EQUIVALENCE_FAILED: 9,
    X_FORBIDDEN_BASE: 10,
}


# ---------------------------------------------------------------------------
# The design this executable implements, pinned by digest.
#
# The frozen v0.1 document is now a tripwire: editing it in place turns plan mode red.
# That is the intended consequence of freezing it -- design section 1's version
# discipline says an approved version is never edited in place, only bumped and
# `git mv`'d, and a bump must move this constant with it.
# ---------------------------------------------------------------------------
DESIGN_DOCUMENT_NAME = "capacity-escalation-v0.1.md"
DESIGN_CANONICAL_SHA256 = (
    "05109d973f1611756456a01aea8a0aebf7c33ec73e5243225f1f733e3c15e002"
)

SWEEP_AUTHORITY = (
    "DEVELOPMENT-ONLY CAPACITY SWEEP: width sensitivity of the rung-1 in-sample fit "
    "under one fixed optimization protocol; not held-out evidence, not a capacity "
    "selection, and not a C1-versus-S result"
)

# Design section 4.2. Every point is inside Slot 9's rung-1 band, so Stage 1 does not
# climb the ladder and `enforce_rung1_band` stays on for every arm (invariant C5).
CAPACITY_POINTS: tuple[int, ...] = (16, 24, 32, 40, 48)
ANCHOR_CHANNELS = 32

# Design section 4.2's table, which invariant C4 requires every constructed arm to
# reproduce. These are the *expected* values; the recorded ones are read off the
# constructed network, and a disagreement is a refusal rather than a note.
EXPECTED_PARAMETERS: dict[int, int] = {
    16: 10_586,
    24: 22_786,
    32: 39_594,
    40: 61_010,
    48: 87_034,
}
EXPECTED_RECEPTIVE_FIELD = 1_023

# Design section 11 ruling 5: two arms, covering both suite paths and two seeds.
EQUIVALENCE_ARMS: tuple[tuple[str, int], ...] = (("C1", 0), ("S", 4))

# Design section 4.1. Held exactly fixed; deliberately NOT command-line arguments,
# because "varies: channels, and nothing else" is not a property an operator may edit at
# invocation. Invariant C3 checks each of them against the approved ledger, which is an
# independent source for the same fact.
SWEEP_EPOCHS = 20
SWEEP_BATCH_SIZE = 8
SWEEP_LEARNING_RATE = 1.0e-3
SWEEP_DEVICE = "cpu"

# Design sections 6 C2 and 7.1.
RUN_LABEL_PATTERN = re.compile(r"^[a-z0-9][a-z0-9-]{2,31}$")
REFUSAL_SINK_NAME = "_capacity_sweep_refusals"
UNBOUND_LABEL_DIRECTORY = "_unbound"
EQUIVALENCE_SUBTREE = "_equivalence"
LOGICAL_NAMESPACE_ROOT = "results/capacity_sweep"

PLAN_ARTIFACT = "capacity_sweep_plan.json"
RUN_ARTIFACT = "capacity_sweep_result.json"
EQUIVALENCE_ARTIFACT = "capacity_sweep_equivalence.json"

# Design section 7.1: the maximum budget, stated in the plan and asserted on every exit.
MAX_FITS = 42
MAX_CHECKPOINTS = 42

# The approved anchor state this sweep reuses and measures itself against.
APPROVED_RESULT_RELATIVE = "results/dev_fit/dev_fit_result.json"
APPROVED_ANALYSIS_RELATIVE = "results/dev_fit/dev_fit_analysis.json"
APPROVED_CHECKPOINT_RELATIVE = "results/dev_fit"

# Design sections 5.1 and 5.2: both constants are read from the approved analysis
# artifact at run time and named to their exact field, because a sourced constant whose
# source is not written down is a literal with a footnote.
BAR_FIELD_PATH = ("paired_macro_f1", "claim_sheet_success_bar")
ANCHOR_SAMPLE_SD_FIELD_PATH = ("paired_macro_f1", "sample_sd_S_minus_C1")

# Design section 5.2: a predeclared numerical tie rule, far below the 0.05 project bar
# and carrying no claim about the granularity of macro-F1 on 152 examples.
QUANTUM = Decimal("0.000001")

SHAPE_UNDEFINED = "UNDEFINED_TOO_FEW_POINTS"
SHAPE_FLAT = "FLAT"
SHAPE_STRICTLY_INCREASING = "STRICTLY_INCREASING"
SHAPE_STRICTLY_DECREASING = "STRICTLY_DECREASING"
SHAPE_NON_DECREASING = "NON_DECREASING_WITH_TIES"
SHAPE_NON_INCREASING = "NON_INCREASING_WITH_TIES"
SHAPE_NON_MONOTONE = "NON_MONOTONE"

CONSTRAINT_NONE = "NONE"
CONSTRAINT_PARTIAL = "PARTIAL"
CONSTRAINT_ALL = "ALL"

LABEL_ELIGIBLE = "POST_ANCHOR_NONNEGATIVE_AT_ELIGIBLE_POINT"
LABEL_CONSTRAINED_ONLY = "POST_ANCHOR_NONNEGATIVE_ONLY_AT_CONSTRAINED_POINT"
LABEL_NO_ELIGIBLE_POINTS = "NO_ELIGIBLE_POST_ANCHOR_POINTS"
LABEL_NONE = "NO_POST_ANCHOR_NONNEGATIVE_POINT"

ARM_REUSED = "REUSED"
ARM_COMPLETED = "COMPLETED"
ARM_REFUSED = "REFUSED"
ARM_UNATTEMPTED = "UNATTEMPTED"

COMPARISON_PASS = "PASS"
COMPARISON_FAIL = "FAIL"
COMPARISON_NOT_RUN = "NOT_RUN"


class CapacitySweepError(RuntimeError):
    """This module's own diagnosis: an input it needs could not be assembled."""


class EquivalenceFailure(RuntimeError):
    """Invariant C9 refused: the width-parameterized path is not the approved path."""


class RunRootOccupied(RuntimeError):
    """The atomic claim of `<base>/<run_label>/` found the path already present."""


class ForbiddenBase(RuntimeError):
    """Invariant C1 refused a destination at or inside the approved checkpoint tree."""


def packet_root() -> Path:
    """Return the Reproducibility Packet root this module lives inside."""

    return Path(__file__).resolve().parents[2]


# ---------------------------------------------------------------------------
# The grid, the network, and the copied fit loop
# ---------------------------------------------------------------------------
def require_run_label(value: Any) -> str:
    """Return `value` if it is a conforming run label, refusing anything else.

    Inputs: a candidate label. Outputs: the same string. Purpose: the label becomes a
    filesystem component and a JSON member name, so it is validated before either use.
    The character class deliberately admits no underscore, which is what makes the two
    reserved sink names unreachable by any conforming label.
    """

    require(
        isinstance(value, str) and RUN_LABEL_PATTERN.fullmatch(value) is not None,
        f"run_label must match {RUN_LABEL_PATTERN.pattern}, got {value!r}",
    )
    return value


def require_capacity_point(channels: Any) -> int:
    """Return `channels` if it is one of the five predeclared Stage-1 capacity points."""

    require(
        isinstance(channels, int)
        and not isinstance(channels, bool)
        and channels in CAPACITY_POINTS,
        f"channels must be one of {list(CAPACITY_POINTS)}, got {channels!r}",
    )
    return int(channels)


def curve_arms() -> tuple[tuple[int, str, int], ...]:
    """Return the forty new `(channels, suite, seed)` arms this sweep fits.

    The anchor width is excluded by construction rather than by a later filter: design
    section 7.3 makes a plan containing a 32-channel fit arm invalid at plan time, and
    the cheapest way to keep that true is for no producer of the list to emit one.
    """

    return tuple(
        (channels, suite, seed)
        for channels in CAPACITY_POINTS
        if channels != ANCHOR_CHANNELS
        for suite in MATCHED_FIT_SUITES
        for seed in PREDECLARED_TRAINING_SEEDS
    )


def anchor_arms() -> tuple[tuple[int, str, int], ...]:
    """Return the ten approved 32-channel anchors, which are read and never re-fitted."""

    return tuple(
        (ANCHOR_CHANNELS, suite, seed)
        for suite in MATCHED_FIT_SUITES
        for seed in PREDECLARED_TRAINING_SEEDS
    )


def build_network(*, channels: int, seed: int) -> TemporalAttributionNet:
    """Return the Stage-1 network at one capacity point.

    Inputs: a predeclared capacity point and a predeclared seed. Outputs: the
    constructed network. Purpose: the **one** network construction site in this module,
    so `enforce_rung1_band=True` is a property of the module rather than of each call
    site (invariant C5). There is deliberately no argument anywhere in this file that can
    turn that guard off; Stage 2 is a different document.
    """

    require_capacity_point(channels)
    require_predeclared_seed(seed)
    return TemporalAttributionNet(
        seed=seed, channels=channels, enforce_rung1_band=True
    )


def capacity_shape_map() -> dict[int, dict[str, int]]:
    """Return `{channels: {n_parameters, receptive_field}}`, constructed not recalled.

    Inputs: none. Outputs: the measured shape of each capacity point. Purpose: invariant
    C4 -- the parameter count and receptive field of every arm are taken from the
    constructed network rather than re-derived, must match design section 4.2 exactly,
    and two capacity points may not report the same count.
    """

    shape: dict[int, dict[str, int]] = {}
    for channels in CAPACITY_POINTS:
        net = build_network(channels=channels, seed=PREDECLARED_TRAINING_SEEDS[0])
        n_parameters = int(net.n_parameters)
        receptive_field = int(net.receptive_field)
        require(
            n_parameters == EXPECTED_PARAMETERS[channels],
            f"{channels} channels built {n_parameters} parameters; the design's table "
            f"reserves {EXPECTED_PARAMETERS[channels]}",
        )
        require(
            receptive_field == EXPECTED_RECEPTIVE_FIELD,
            f"{channels} channels built a receptive field of {receptive_field}; every "
            f"Stage-1 point must hold {EXPECTED_RECEPTIVE_FIELD}",
        )
        shape[channels] = {
            "n_parameters": n_parameters,
            "receptive_field": receptive_field,
        }
    require_distinct_capacity_counts(shape)
    return shape


def require_distinct_capacity_counts(shape: Mapping[int, Mapping[str, int]]) -> None:
    """Refuse a grid in which two capacity points report the same parameter count.

    Inputs: the constructed shape map. Outputs: none. Purpose: the second half of
    invariant C4, stated as its own routine so a test can drive it directly. Measured in
    the Session-92 mutation sweep: while it lived inline, deleting it changed nothing any
    test could see, because the tests asserted the *property* of the real grid rather than
    the behaviour of the guard -- which is a test of the world, not of the code.

    If two points shared a count the width axis would not be a capacity axis, and the
    curve would be plotting one capacity twice under two names.
    """

    counts = [entry["n_parameters"] for entry in shape.values()]
    require(
        len(set(counts)) == len(counts),
        "two capacity points report the same parameter count; the width axis would not "
        "be a capacity axis",
    )


def sweep_code_identity() -> dict[str, str]:
    """Return the nine-entry code identity every sweep arm records.

    Inputs: none. Outputs: `{bare label: canonical text digest}`. Purpose: invariant C3
    under Route A -- all eight of the approved trainer's historical entries must match
    exactly, and this module is **one additional entry**. `dev_fit_trainer.py` stays in
    the identity because this module imports `arm_loss` and `_stack` from it, so the
    approved trainer really is part of what fits these arms.
    """

    here = Path(__file__).resolve().parent
    identity = dict(trainer.training_code_identity())
    identity["capacity_sweep.py"] = code_identity(
        {"capacity_sweep.py": here / "capacity_sweep.py"}
    )["capacity_sweep.py"]
    return dict(sorted(identity.items()))


def fit_arm_at_width(
    examples: Sequence[Any],
    *,
    seed: int,
    channels: int,
    epochs: int,
    batch_size: int,
    learning_rate: float,
    device: torch.device,
) -> tuple[TemporalAttributionNet, list[float]]:
    """Fit one arm at one width and return its network and per-epoch mean loss.

    Inputs: the arm's examples, its predeclared seed, its capacity point, and the fixed
    optimization settings. Outputs: the fitted network and its loss history.
    Purpose: the compatibility seam. This is `dev_fit_trainer.fit_one_arm`'s body with
    one expression changed -- `TemporalAttributionNet(seed=seed)` becomes
    `build_network(channels=channels, seed=seed)` -- and every project-defined name it
    uses imported from the approved modules rather than retyped.

    `deterministic_conv_precision()` wraps the **whole** step, forward and backward, for
    the reason the approved trainer states: cuDNN's TF32 default applies to the
    convolution backward kernels too, so a context covering inference alone would leave
    the gradients at a different precision than the numbers it was opened to protect.

    Nothing here asserts that this loop equals the approved one. `equivalence_gate`
    measures it at 32 channels against the approved checkpoints before any curve arm
    runs, which is the whole point of invariant C9.
    """

    require_predeclared_seed(seed)
    require_capacity_point(channels)
    if not examples:
        raise DevFitDataError("a development-only fit may not consume an empty row set")
    torch.manual_seed(seed)
    net = build_network(channels=channels, seed=seed).to(device)
    optimizer = torch.optim.Adam(net.parameters(), lr=learning_rate)
    order = np.random.default_rng(seed).permutation(len(examples))
    history: list[float] = []
    with deterministic_conv_precision():
        net.train()
        for _ in range(epochs):
            epoch_losses: list[float] = []
            for start in range(0, len(order), batch_size):
                chunk = [examples[int(index)] for index in order[start : start + batch_size]]
                batch = _stack(chunk, device)
                optimizer.zero_grad(set_to_none=True)
                loss = arm_loss(net(batch["inputs"]), batch)
                if not bool(torch.isfinite(loss).item()):
                    raise DevFitDataError(
                        f"training loss became non-finite for seed {seed}"
                    )
                loss.backward()
                optimizer.step()
                epoch_losses.append(float(loss.detach().cpu()))
            history.append(float(np.mean(epoch_losses)))
        net.eval()
    if any(
        not bool(torch.all(torch.isfinite(parameter)).item())
        for parameter in net.parameters()
    ):
        raise DevFitDataError(f"trained weights became non-finite for seed {seed}")
    return net, history


def score_arm(net: TemporalAttributionNet, examples: Sequence[Any]) -> dict[str, Any]:
    """Return one arm's in-sample classification metrics on its own training examples.

    Inputs: a fitted network and the examples it was fitted on. Outputs: the approved
    analyzer's `accuracy` / `macro_f1` / `per_class_f1` mapping. Purpose: design section
    3 -- the classification metrics are not re-implemented here; they are imported from
    `analyze_dev_fit`, because a second definition of macro-F1 in this project would be a
    second definition of the quantity the whole read is about.

    Every number this produces is **in sample**, on the arm's own 152 training windows.
    """

    batch = _stack(examples, torch.device(SWEEP_DEVICE))
    net.eval()
    with torch.no_grad(), deterministic_conv_precision():
        heads = net(batch["inputs"])
        prediction = heads.class_logits.argmax(dim=1).tolist()
        truth = batch["class_index"].tolist()
    return approved_analysis.classification_metrics(
        truth, prediction, n_classes=len(approved_analysis.SOURCE_CLASS_ORDER)
    )


# ---------------------------------------------------------------------------
# The approved anchor state: read, checked, never re-fitted (invariants C1 and C3)
# ---------------------------------------------------------------------------
def read_json_document(path: Path, label: str) -> dict[str, Any]:
    """Return a parsed JSON object, refusing anything that is not one."""

    path = Path(path)
    if not path.is_file():
        raise CapacitySweepError(f"the {label} is not present at its packet-relative path")
    try:
        document = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, ValueError) as error:
        raise CapacitySweepError(
            f"the {label} could not be read ({type(error).__name__})"
        ) from error
    if not isinstance(document, dict):
        raise CapacitySweepError(f"the {label} is not a JSON object")
    return document


def read_field(document: Mapping[str, Any], path: Sequence[str], label: str) -> Any:
    """Return a nested field by its exact path, refusing an absent one by name."""

    cursor: Any = document
    for key in path:
        if not isinstance(cursor, Mapping) or key not in cursor:
            raise CapacitySweepError(
                f"the {label} carries no field {'.'.join(path)}"
            )
        cursor = cursor[key]
    return cursor


def read_success_bar(analysis: Mapping[str, Any]) -> float:
    """Return `BAR` from the approved analysis artifact's own published field.

    Design section 5.1: `BAR` is not a number this document invents. It is read from
    `paired_macro_f1.claim_sheet_success_bar` and persisted, so the constraint criterion
    inherits an already-approved constant rather than adding a new one. The executable
    refuses if the field is absent or is not a finite float in `(0, 1)`.
    """

    value = read_field(analysis, BAR_FIELD_PATH, "approved analysis artifact")
    if (
        not isinstance(value, float)
        or not np.isfinite(value)
        or not 0.0 < value < 1.0
    ):
        raise CapacitySweepError(
            "the approved analysis artifact's success bar is not a finite float in (0, 1)"
        )
    return float(value)


def read_anchor_sample_sd(analysis: Mapping[str, Any]) -> float:
    """Return `s(32)` from the approved analysis artifact's own published field.

    Design section 5.2 names the field exactly -- `paired_macro_f1.sample_sd_S_minus_C1`
    -- because it is not guessable from the quantity's name, and demotes the value itself
    to a reader's convenience the executable may not carry as a literal.
    """

    value = read_field(analysis, ANCHOR_SAMPLE_SD_FIELD_PATH, "approved analysis artifact")
    if not isinstance(value, float) or not np.isfinite(value) or value <= 0.0:
        raise CapacitySweepError(
            "the approved analysis artifact's anchor sample SD is not a finite positive "
            "float"
        )
    return float(value)


def approved_anchor_arms(ledger: Mapping[str, Any], analysis: Mapping[str, Any]) -> list[dict[str, Any]]:
    """Return the ten approved 32-channel anchors as `REUSED` curve entries.

    Inputs: the approved fit ledger and the approved in-sample analysis. Outputs: one
    entry per anchor carrying its approved metrics and checkpoint digest. Purpose:
    invariant C1 -- the existing ten arms are **read**, never re-run, because re-fitting
    would produce a second set of checkpoints claiming to be the same arms while the
    ledger is their sole provenance record.

    The two documents are cross-checked rather than trusted separately: the digest the
    analysis scored is required to equal the digest the ledger recorded, which is a check
    whose two sides come from different files.
    """

    ledger_arms = ledger.get("arms")
    analysis_arms = analysis.get("arms")
    if not isinstance(ledger_arms, list) or not isinstance(analysis_arms, list):
        raise CapacitySweepError("the approved anchor documents carry no arms list")
    by_key_ledger = {
        (str(arm.get("suite")), int(arm.get("training_seed"))): arm
        for arm in ledger_arms
        if isinstance(arm, Mapping)
    }
    by_key_analysis = {
        (str(arm.get("suite")), int(arm.get("seed"))): arm
        for arm in analysis_arms
        if isinstance(arm, Mapping)
    }
    entries: list[dict[str, Any]] = []
    for channels, suite, seed in anchor_arms():
        key = (suite, seed)
        if key not in by_key_ledger or key not in by_key_analysis:
            raise CapacitySweepError(
                f"the approved anchor documents do not both carry {suite} seed {seed}"
            )
        ledger_arm = by_key_ledger[key]
        analysis_arm = by_key_analysis[key]
        digest = str(ledger_arm.get("checkpoint_sha256"))
        if str(analysis_arm.get("checkpoint_sha256")) != digest:
            raise CapacitySweepError(
                f"the approved ledger and analysis disagree on the {suite} seed {seed} "
                "checkpoint digest"
            )
        classification = analysis_arm.get("classification")
        if not isinstance(classification, Mapping):
            raise CapacitySweepError(
                f"the approved analysis carries no classification for {suite} seed {seed}"
            )
        entries.append(
            {
                "accuracy": classification["accuracy"],
                "channels": channels,
                "checkpoint_sha256": digest,
                "macro_f1": classification["macro_f1"],
                "n_parameters": EXPECTED_PARAMETERS[channels],
                "per_class_f1": dict(sorted(dict(classification["per_class_f1"]).items())),
                "receptive_field": EXPECTED_RECEPTIVE_FIELD,
                "seed": seed,
                "source": "approved-ledger",
                "status": ARM_REUSED,
                "suite": suite,
            }
        )
    return entries


def require_anchor_comparability(ledger: Mapping[str, Any], protocol: Any) -> None:
    """Refuse an anchor that was not produced by the code, data and protocol in use.

    Inputs: the approved fit ledger and the `TrainingProtocol` this sweep will run.
    Outputs: none. Purpose: invariant C3 -- if the match fails, the sweep is not a sweep,
    it is five unrelated experiments, and it must refuse with a named exit rather than
    reporting a curve.

    The code-identity comparison is **entry by entry** over all eight historical entries.
    The sweep module is the one permitted addition; any changed historical entry, any
    missing entry, and any other unlisted addition is a refusal.
    """

    recorded_identity = ledger.get("code_identity")
    require(
        isinstance(recorded_identity, Mapping) and bool(recorded_identity),
        "the approved ledger carries no code identity",
    )
    current = sweep_code_identity()
    additions = set(current) - set(recorded_identity)
    require(
        additions == {"capacity_sweep.py"},
        "the sweep's code identity adds "
        + ", ".join(sorted(additions))
        + " to the approved ledger's; exactly one addition is permitted",
    )
    missing = set(recorded_identity) - set(current)
    require(not missing, "the sweep's code identity drops " + ", ".join(sorted(missing)))
    changed = sorted(
        label
        for label, digest in recorded_identity.items()
        if current.get(label) != digest
    )
    require(
        not changed,
        "the code that fits these arms differs from the code that fitted the approved "
        "anchor at " + ", ".join(changed),
    )

    recorded_protocol = ledger.get("training_protocol")
    require(
        isinstance(recorded_protocol, Mapping),
        "the approved ledger carries no training protocol",
    )
    current_protocol = protocol.as_document()
    differing = sorted(
        key
        for key in set(recorded_protocol) | set(current_protocol)
        if recorded_protocol.get(key) != current_protocol.get(key)
    )
    require(
        not differing,
        "the sweep's training protocol differs from the approved anchor's at "
        + ", ".join(differing),
    )

    recorded_role_index = ledger.get("role_index_sha256")
    require(
        recorded_role_index == dict(sorted(AUTHORIZED_ROLE_INDEX_SHA256.items())),
        "the approved ledger's role indexes are not the authorized delivered indexes",
    )
    for arm in ledger.get("arms", []):
        require(
            isinstance(arm, Mapping)
            and arm.get("manifest_sha256") == AUTHORIZED_MANIFEST_SHA256
            and arm.get("config_hash") == AUTHORIZED_CONFIG_HASH
            and arm.get("assignment_sha256") == protocol.assignment_sha256,
            "an approved anchor arm does not carry the authorized data identity",
        )


# ---------------------------------------------------------------------------
# Invariant C9 -- the equivalence gate
# ---------------------------------------------------------------------------
def state_dicts_are_bit_identical(
    produced: Mapping[str, torch.Tensor], approved: Mapping[str, torch.Tensor]
) -> tuple[bool, str]:
    """Return whether two state dictionaries are bit-identical, and why not if they differ.

    Inputs: two state dictionaries. Outputs: `(identical, reason_when_not)`.
    Purpose: this is C9's scientific comparison. It is done **tensor by tensor** rather
    than over serialized bytes on purpose: `torch.save` writes a zip container whose
    metadata is not part of the weights, so a container difference between two torch
    builds would fail a byte comparison for a reason that is not the one C9 exists to
    catch. The serialized digests are still recorded in the artifact -- they are evidence,
    not the gate.
    """

    if set(produced) != set(approved):
        missing = sorted(set(approved) - set(produced))
        extra = sorted(set(produced) - set(approved))
        return False, f"parameter names differ (missing {missing}, extra {extra})"
    for name in sorted(produced):
        left = produced[name]
        right = approved[name]
        if left.shape != right.shape:
            return False, f"{name} has shape {tuple(left.shape)} against {tuple(right.shape)}"
        if left.dtype != right.dtype:
            return False, f"{name} has dtype {left.dtype} against {right.dtype}"
        if not bool(torch.equal(left, right)):
            return False, f"{name} is not bit-identical to the approved checkpoint"
    return True, ""


def equivalence_gate(
    *,
    examples_by_suite: Mapping[str, Sequence[Any]],
    ledger: Mapping[str, Any],
    checkpoint_dir: Path,
    scratch_dir: Path,
    protocol: Any,
) -> dict[str, Any]:
    """Measure the copied fit path against the approved one, and refuse if it differs.

    Inputs: the loaded dev examples per suite, the approved ledger, the approved
    checkpoint directory, the reserved `_equivalence/` scratch subtree of the claimed run
    root, and the protocol. Outputs: the equivalence artifact.
    Purpose: invariant C9. Two 32-channel arms -- `(C1, 0)` and `(S, 4)` -- are fitted
    through **this module's** width-parameterized path, and their parameter tensors and
    per-epoch loss history must be bit-identical to the corresponding approved checkpoint
    and ledger row.

    Refuses loudly on either difference, on either approved checkpoint being absent (a
    fresh clone carries the ledger without the weights), and on a comparison that cannot
    be made for any other reason. Nothing downstream of this runs unless both comparisons
    report `PASS`.
    """

    scratch_dir = Path(scratch_dir)
    scratch_dir.mkdir(parents=True, exist_ok=True)
    ledger_arms = {
        (str(arm.get("suite")), int(arm.get("training_seed"))): arm
        for arm in ledger.get("arms", [])
        if isinstance(arm, Mapping)
    }
    identity = sweep_code_identity()
    results: list[dict[str, Any]] = []
    for suite, seed in EQUIVALENCE_ARMS:
        require_matched_fit_suite(suite)
        require_predeclared_seed(seed)
        entry: dict[str, Any] = {
            "approved_checkpoint_sha256": None,
            "channels": ANCHOR_CHANNELS,
            "comparison": COMPARISON_NOT_RUN,
            "produced_checkpoint_sha256": None,
            "reason_class": None,
            "seed": seed,
            "status": ARM_UNATTEMPTED,
            "suite": suite,
        }
        results.append(entry)
        arm = ledger_arms.get((suite, seed))
        if arm is None:
            entry["comparison"] = COMPARISON_FAIL
            entry["reason_class"] = "MissingApprovedLedgerRow"
            raise EquivalenceFailure(
                f"the approved ledger carries no {suite} seed {seed} arm to compare against"
            )
        approved_path = Path(checkpoint_dir) / str(arm.get("checkpoint_name"))
        entry["approved_checkpoint_sha256"] = str(arm.get("checkpoint_sha256"))
        if not approved_path.is_file():
            entry["comparison"] = COMPARISON_FAIL
            entry["reason_class"] = "MissingApprovedCheckpoint"
            raise EquivalenceFailure(
                f"the approved {suite} seed {seed} checkpoint is not on disk; a fresh "
                "clone carries the ledger without the weights, and the equivalence gate "
                "cannot be made without them"
            )
        try:
            approved_state = torch.load(approved_path, map_location="cpu", weights_only=True)
        except (OSError, RuntimeError, TypeError, ValueError) as error:
            entry["comparison"] = COMPARISON_FAIL
            entry["reason_class"] = type(error).__name__
            raise EquivalenceFailure(
                f"the approved {suite} seed {seed} checkpoint could not be loaded "
                f"({type(error).__name__})"
            ) from error

        net, history = fit_arm_at_width(
            examples_by_suite[suite],
            seed=seed,
            channels=ANCHOR_CHANNELS,
            epochs=protocol.epochs,
            batch_size=protocol.batch_size,
            learning_rate=protocol.learning_rate,
            device=torch.device(protocol.device),
        )
        produced_state = net.state_dict()
        buffer = io.BytesIO()
        torch.save(produced_state, buffer)
        produced_bytes = buffer.getvalue()
        entry["produced_checkpoint_sha256"] = hashlib.sha256(produced_bytes).hexdigest()
        checkpoint_path = scratch_dir / f"capacity_sweep_equivalence_{suite}_seed{seed}.pt"
        checkpoint_path.write_bytes(produced_bytes)
        entry["status"] = ARM_COMPLETED

        identical, reason = state_dicts_are_bit_identical(produced_state, approved_state)
        if not identical:
            entry["comparison"] = COMPARISON_FAIL
            entry["reason_class"] = "WeightsDiffer"
            raise EquivalenceFailure(
                f"the width-parameterized path did not reproduce the approved "
                f"{suite} seed {seed} weights: {reason}"
            )
        approved_history = arm.get("loss_history")
        if (
            not isinstance(approved_history, list)
            or len(approved_history) != len(history)
            or any(
                float(left) != float(right)
                for left, right in zip(approved_history, history)
            )
        ):
            entry["comparison"] = COMPARISON_FAIL
            entry["reason_class"] = "LossHistoryDiffers"
            raise EquivalenceFailure(
                f"the width-parameterized path did not reproduce the approved "
                f"{suite} seed {seed} per-epoch loss history"
            )
        entry["comparison"] = COMPARISON_PASS

    document = {
        "arms": results,
        "authority": SWEEP_AUTHORITY,
        "code_identity": identity,
        "equivalence_channels": ANCHOR_CHANNELS,
        "generation_runs": 0,
        "non_dev_reads": 0,
        "rollouts_spent": 0,
    }
    write_document(scratch_dir / EQUIVALENCE_ARTIFACT, document)
    return document


# ---------------------------------------------------------------------------
# Plan mode
# ---------------------------------------------------------------------------
def logical_namespace(run_label: str) -> str:
    """Return the packet-relative, label-leading logical output namespace."""

    return f"{LOGICAL_NAMESPACE_ROOT}/{require_run_label(run_label)}"


def checkpoint_relative_name(channels: int, suite: str, seed: int) -> str:
    """Return one curve arm's expected checkpoint name inside the logical namespace."""

    require_capacity_point(channels)
    require_matched_fit_suite(suite)
    require_predeclared_seed(seed)
    return (
        f"channels_{channels:03d}/capacity_sweep_ch{channels:03d}_{suite}_seed{seed}.pt"
    )


def equivalence_relative_name(suite: str, seed: int) -> str:
    """Return one equivalence checkpoint's name inside the reserved scratch subtree."""

    require_matched_fit_suite(suite)
    require_predeclared_seed(seed)
    return f"{EQUIVALENCE_SUBTREE}/capacity_sweep_equivalence_{suite}_seed{seed}.pt"


def design_digest() -> str:
    """Return the frozen design document's canonical digest, checked against its pin."""

    path = packet_root() / "protocol" / DESIGN_DOCUMENT_NAME
    require(path.is_file(), "the frozen capacity-escalation design is not in the packet")
    digest = canonical_text_sha256(path)
    require(
        digest == DESIGN_CANONICAL_SHA256,
        "the packet's capacity-escalation design is not the frozen approved v0.1; an "
        "approved version is never edited in place, it is bumped and moved",
    )
    return digest


def plan_document(*, run_label: str, protocol: Any) -> dict[str, object]:
    """Return the deterministic plan artifact design section 7.1 requires.

    Inputs: the predeclared run label and the resolved training protocol. Outputs: the
    plan document. Purpose: a forty-fit action needs an aggregate identity and a
    partial-completion story before it runs, not after one arm fails.

    **No host path enters this document.** The operator supplies the base directory at
    execute time and the plan supplies the label, so two plan runs at the same
    `run_label` into different destinations produce identical bytes. That is what makes
    the plan's digest a statement about the *design of the run* rather than about the
    machine it was written on.
    """

    require_run_label(run_label)
    ledger = read_json_document(packet_root() / APPROVED_RESULT_RELATIVE, "approved fit ledger")
    analysis = read_json_document(
        packet_root() / APPROVED_ANALYSIS_RELATIVE, "approved analysis artifact"
    )
    require_anchor_comparability(ledger, protocol)
    shape = capacity_shape_map()
    namespace = logical_namespace(run_label)
    anchors = approved_anchor_arms(ledger, analysis)
    new_arms = [
        {
            "channels": channels,
            "checkpoint_relative_name": f"{namespace}/{checkpoint_relative_name(channels, suite, seed)}",
            "n_parameters": shape[channels]["n_parameters"],
            "read_only": False,
            "receptive_field": shape[channels]["receptive_field"],
            "seed": seed,
            "suite": suite,
        }
        for channels, suite, seed in curve_arms()
    ]
    require(
        all(entry["channels"] != ANCHOR_CHANNELS for entry in new_arms),
        "a plan may not contain a 32-channel fit arm; the ten anchors are read-only",
    )
    equivalence = [
        {
            "channels": ANCHOR_CHANNELS,
            "checkpoint_relative_name": f"{namespace}/{equivalence_relative_name(suite, seed)}",
            "seed": seed,
            "suite": suite,
            "target_approved_checkpoint_sha256": next(
                entry["checkpoint_sha256"]
                for entry in anchors
                if entry["suite"] == suite and entry["seed"] == seed
            ),
        }
        for suite, seed in EQUIVALENCE_ARMS
    ]
    return {
        "anchor_arms": [
            {
                "channels": entry["channels"],
                "checkpoint_sha256": entry["checkpoint_sha256"],
                "read_only": True,
                "seed": entry["seed"],
                "suite": entry["suite"],
            }
            for entry in anchors
        ],
        "anchor_sample_sd": read_anchor_sample_sd(analysis),
        "anchor_sample_sd_field": ".".join(ANCHOR_SAMPLE_SD_FIELD_PATH),
        "assignment_sha256": protocol.assignment_sha256,
        "authority": SWEEP_AUTHORITY,
        "capacity_points": list(CAPACITY_POINTS),
        "claim_sheet_success_bar": read_success_bar(analysis),
        "claim_sheet_success_bar_field": ".".join(BAR_FIELD_PATH),
        "code_identity": sweep_code_identity(),
        "config_hash": AUTHORIZED_CONFIG_HASH,
        "design_sha256": design_digest(),
        "equivalence_arms": equivalence,
        "equivalence_relative_namespace": f"{namespace}/{EQUIVALENCE_SUBTREE}",
        "exit": X_PLAN_OK,
        "logical_output_namespace": namespace,
        "manifest_sha256": AUTHORIZED_MANIFEST_SHA256,
        "maximum_budget": {
            "checkpoints": MAX_CHECKPOINTS,
            "fits": MAX_FITS,
            "generation_runs": 0,
            "non_dev_reads": 0,
            "rollouts": 0,
        },
        "mode": "plan",
        "n_anchor_arms": len(anchors),
        "n_equivalence_arms": len(equivalence),
        "n_new_arms": len(new_arms),
        "new_arms": new_arms,
        "plan_valid": True,
        "role_index_sha256": dict(sorted(AUTHORIZED_ROLE_INDEX_SHA256.items())),
        "run_label": run_label,
        "training_protocol": protocol.as_document(),
    }


def require_authorized_plan(path: Path, *, expected_sha256: str, protocol: Any) -> dict[str, Any]:
    """Authenticate the approved plan before any of its values names a path.

    Inputs: the plan file, the digest a joint authorization named, and the protocol this
    invocation resolved. Outputs: the parsed plan. Purpose: `--approved-plan-sha256`
    names a **document** and nothing else, exactly as the payload extension's gate does.

    What this gate can and cannot do is stated in design section 7.1 and is not widened
    here: it checks that the document is a valid plan, that it is the document the
    authorization named, and that the run it describes is the run this executable would
    build. It does **not** make the authorization single-use. A replay under the same
    base collides with the preserved run root and is refused there; a replay pointed at a
    different base, or run from a copied workspace, is outside what any local mechanism
    can see and is a protocol violation even though this gate passes.
    """

    require(
        isinstance(expected_sha256, str)
        and re.fullmatch(r"[0-9a-f]{64}", expected_sha256) is not None,
        "--approved-plan-sha256 must be 64 lowercase hex characters",
    )
    path = Path(path)
    require(path.is_file(), "the approved plan document is not present")
    digest = canonical_text_sha256(path)
    require(
        digest == expected_sha256,
        "the plan document's canonical digest is not the authorized digest",
    )
    document = read_json_document(path, "approved plan")
    require(document.get("mode") == "plan", "the authorized document is not a plan")
    require(document.get("exit") == X_PLAN_OK, "the authorized plan is not a terminal plan")
    require(document.get("plan_valid") is True, "the authorized plan is not valid")
    require(
        document.get("design_sha256") == design_digest(),
        "the authorized plan was written against a different design document",
    )
    require(
        document.get("code_identity") == sweep_code_identity(),
        "the authorized plan was written by a different code state",
    )
    require(
        document.get("training_protocol") == protocol.as_document(),
        "the authorized plan names a different training protocol",
    )
    require_run_label(document.get("run_label"))
    expected = plan_document(run_label=document["run_label"], protocol=protocol)
    require(
        document == expected,
        "the authorized plan is not the plan this executable builds at that run label",
    )
    return document


# ---------------------------------------------------------------------------
# Execute-mode write locations
# ---------------------------------------------------------------------------
def write_document(path: Path, document: Mapping[str, object]) -> str:
    """Write `document` as canonical JSON and return the text written."""

    path = Path(path)
    path.parent.mkdir(parents=True, exist_ok=True)
    text = canonical_json(dict(document))
    path.write_text(text, encoding="utf-8", newline="\n")
    return text


def require_permitted_base(base_dir: Path) -> Path:
    """Refuse a destination at or inside the approved checkpoint tree.

    Invariant C1: the executable must refuse to write into `results/dev_fit`. This check
    runs **before any write of any kind**, including the refusal sink's, because every
    sink this module has is under the base -- so persisting this refusal would itself be
    the forbidden write. That is why `X_FORBIDDEN_BASE` is the one terminal exit with no
    artifact, and why the docstring at the top of this module says so out loud.
    """

    base = Path(base_dir).resolve()
    protected = (packet_root() / APPROVED_CHECKPOINT_RELATIVE).resolve()
    if base == protected or protected in base.parents:
        raise ForbiddenBase(
            "the destination base is at or inside the approved dev-fit checkpoint "
            "directory, whose ledger is the sole provenance record for ten checkpoints"
        )
    return base


def claim_run_root(base_dir: Path, run_label: str) -> Path:
    """Claim `<base>/<run_label>/` with one atomic create requiring the path to be absent.

    Inputs: the operator-supplied base and the plan's label. Outputs: the claimed root.
    Purpose: design section 6 C2. Checking "exists and non-empty" is insufficient twice
    over -- an empty leftover directory admits reuse, and a check followed by a separate
    create admits two concurrent invocations that both pass before either writes. A
    pre-existing **file** at the path is refused by the same operation.

    Every write execute mode makes after this call succeeds is beneath the returned root,
    which is what makes "before any other run write" an exhaustive statement rather than
    a statement about the curve arms only.
    """

    require_run_label(run_label)
    root = Path(base_dir) / run_label
    try:
        root.mkdir(parents=True, exist_ok=False)
    except FileExistsError as error:
        raise RunRootOccupied(
            "the run root for this label already exists; a retry uses a new label, and "
            "the occupied root is preserved as evidence rather than overwritten"
        ) from error
    except OSError as error:
        raise CapacitySweepError(
            f"the run root could not be claimed ({type(error).__name__})"
        ) from error
    return root


def write_refusal_document(
    base_dir: Path, run_label: str | None, document: Mapping[str, object]
) -> Path:
    """Persist a pre-claim or occupied-root refusal in the sibling sink.

    Inputs: the base, the validated label or `None`, and the refusal document. Outputs:
    the path written. Purpose: design section 6 C2 -- a refusal must never report through
    the resource whose occupancy triggered it, so the sink is a sibling of the run root
    and is named by a UUID drawn for this invocation.

    The label directory is `_unbound` when no trustworthy label exists yet. Neither
    reserved name can collide with a conforming `run_label`, because the label grammar
    admits no underscore. The file is created exclusively; on the vanishingly unlikely
    collision a new UUID is drawn rather than overwriting a prior refusal.
    """

    if run_label is not None:
        require_run_label(run_label)
    directory = Path(base_dir) / REFUSAL_SINK_NAME / (run_label or UNBOUND_LABEL_DIRECTORY)
    directory.mkdir(parents=True, exist_ok=True)
    text = canonical_json(dict(document))
    for _ in range(8):
        path = directory / f"{uuid.uuid4()}.json"
        try:
            with path.open("x", encoding="utf-8", newline="\n") as handle:
                handle.write(text)
        except FileExistsError:
            continue
        return path
    raise CapacitySweepError("a unique refusal artifact name could not be drawn")


def refusal_document(
    *,
    exit_name: str,
    reason_class: str,
    run_label: str | None,
    approved_plan_sha256: str | None,
    attempt_uuid: str,
    elapsed_s: float,
) -> dict[str, object]:
    """Return the sibling refusal document, which records no message and no path.

    Design section 6 C2: it records the exit, the reason class, the approved-plan digest
    and `run_label` when those are already validated and `null` when they are not, zero
    resource counts, and the elapsed time. It records neither the exception message nor a
    filesystem path, following the trainer's established rule.
    """

    return {
        "approved_plan_sha256": approved_plan_sha256,
        "attempt_uuid": attempt_uuid,
        "authority": SWEEP_AUTHORITY,
        "checkpoints_written": 0,
        "elapsed_s": elapsed_s,
        "exit": exit_name,
        "fits_attempted": 0,
        "generation_runs": 0,
        "non_dev_reads": 0,
        "reason_class": reason_class,
        "rollouts_spent": 0,
        "run_label": run_label,
    }


def require_clean_capacity_point(directory: Path) -> None:
    """Refuse a per-point directory holding artifacts from an earlier attempt.

    Invariant C2 applies the trainer's `X_OUTPUT_DIRTY` shape unchanged to each capacity
    point. Design section 11 records honestly that this guard is now unreachable on the
    ordinary path, since the run root is created absent and owned by this invocation --
    that is defence in depth rather than a contradiction, and a guard that cannot fire on
    the ordinary path is still correct.
    """

    directory = Path(directory)
    if not directory.exists():
        return
    stale = sorted(path.name for path in directory.glob("capacity_sweep_ch*_seed*.pt"))
    require(
        not stale,
        "a capacity-point directory contains checkpoints from an earlier attempt "
        "(found " + ", ".join(stale) + ")",
    )


# ---------------------------------------------------------------------------
# The pre-declared descriptive read of design section 5 -- pure, and defined once
# ---------------------------------------------------------------------------
def quantize(value: float) -> str:
    """Return the six-decimal `ROUND_HALF_EVEN` rendering design section 5.2 declares.

    This is a predeclared numerical tie rule and nothing else. It is far smaller than the
    project's 0.05 bar and carries no claim about the granularity of macro-F1 on 152
    examples; both the raw float and this string are persisted so a reader can
    re-classify at any resolution.
    """

    if not isinstance(value, (int, float)) or isinstance(value, bool):
        raise CapacitySweepError(f"cannot quantize {value!r}")
    if not np.isfinite(value):
        raise CapacitySweepError("cannot quantize a non-finite value")
    return str(Decimal(str(float(value))).quantize(QUANTUM, rounding=ROUND_HALF_EVEN))


def headroom(c1_macro_f1: float, s_macro_f1: float) -> float:
    """Return the exact upper bound on `|d|` at one `(capacity, seed)` pair.

    For any two macro-F1 values in `[0, 1]`, `|d| = max - min <= 1 - min(...)`
    identically. This is an algebraic bound, not a threshold: it replaces the Session-87
    draft's 0.98 accuracy rule, which would have discarded points where a bar-sized
    difference was still arithmetically available.
    """

    for value in (c1_macro_f1, s_macro_f1):
        if not np.isfinite(value) or not 0.0 <= float(value) <= 1.0:
            raise CapacitySweepError("macro-F1 must be a finite value in [0, 1]")
    return 1.0 - min(float(c1_macro_f1), float(s_macro_f1))


def pair_constraint(headrooms: Sequence[float], bar: float) -> str:
    """Return `NONE` / `PARTIAL` / `ALL` for one capacity point's five seeds.

    A pair is bar-constrained iff its headroom is below the Claim Sheet's pre-declared
    success bar: there the arms cannot exhibit a difference as large as the effect the
    project exists to detect, so `d ~ 0` is forced by arithmetic and carries no
    information about capacity. The aggregation is per pair and then per point, which is
    Codex's Session-88 finding -- a suite mean hides saturated and unsaturated seeds
    inside one point.
    """

    if not headrooms:
        raise CapacitySweepError("a capacity point must carry at least one pair")
    if not np.isfinite(bar) or not 0.0 < float(bar) < 1.0:
        raise CapacitySweepError("the success bar must be a finite float in (0, 1)")
    constrained = sum(1 for value in headrooms if float(value) < float(bar))
    if constrained == 0:
        return CONSTRAINT_NONE
    if constrained == len(headrooms):
        return CONSTRAINT_ALL
    return CONSTRAINT_PARTIAL


def classify_shape(values: Sequence[float]) -> str:
    """Return design section 5.2's shape label for an ordered sequence.

    The seven conditions are evaluated in the document's order and are exhaustive and
    mutually exclusive by construction. Classification is performed on quantized values,
    so a tie is a tie at the declared resolution rather than at float64's.
    """

    if len(values) < 2:
        return SHAPE_UNDEFINED
    quantized = [Decimal(quantize(value)) for value in values]
    deltas = [b - a for a, b in zip(quantized, quantized[1:])]
    zero = Decimal(0)
    if all(delta == zero for delta in deltas):
        return SHAPE_FLAT
    if all(delta > zero for delta in deltas):
        return SHAPE_STRICTLY_INCREASING
    if all(delta < zero for delta in deltas):
        return SHAPE_STRICTLY_DECREASING
    if all(delta >= zero for delta in deltas):
        return SHAPE_NON_DECREASING
    if all(delta <= zero for delta in deltas):
        return SHAPE_NON_INCREASING
    return SHAPE_NON_MONOTONE


def derived_label(
    *,
    first_post_anchor_nonnegative_point: int | None,
    first_eligible_post_anchor_nonnegative_point: int | None,
    eligible_post_anchor_points: Sequence[int],
) -> str:
    """Return design section 5.2's single derived label.

    The four conditions are evaluated in order, exhaustive and mutually exclusive. The
    label is a **pure function of persisted primitives** so a test can recompute it from
    the record and it cannot drift from the numbers it summarises.

    **No branch of it authorizes anything** -- not Stage 2, not a threshold, not a
    capacity choice, not a data read, not a sentence about C1 versus S.
    """

    if first_eligible_post_anchor_nonnegative_point is not None:
        return LABEL_ELIGIBLE
    if first_post_anchor_nonnegative_point is not None:
        return LABEL_CONSTRAINED_ONLY
    if not eligible_post_anchor_points:
        return LABEL_NO_ELIGIBLE_POINTS
    return LABEL_NONE


def require_complete_sweep(document: Mapping[str, Any]) -> None:
    """Refuse to read a curve out of a partial run.

    Invariant C10, stated once here so the read-only analysis script imports it rather
    than restating it: the ten approved anchors must be `REUSED`, all forty new curve
    arms `COMPLETED`, and both equivalence arms `COMPLETED` with `PASS`.
    """

    arms = document.get("curve_arms")
    require(isinstance(arms, list), "the run artifact carries no curve arms list")
    reused = [arm for arm in arms if arm.get("status") == ARM_REUSED]
    completed = [arm for arm in arms if arm.get("status") == ARM_COMPLETED]
    require(
        len(reused) == len(anchor_arms())
        and all(arm.get("channels") == ANCHOR_CHANNELS for arm in reused),
        f"a complete sweep reuses exactly the {len(anchor_arms())} approved anchors",
    )
    require(
        len(completed) == len(curve_arms()),
        f"a complete sweep completes exactly {len(curve_arms())} new curve arms",
    )
    require(
        len(arms) == len(reused) + len(completed),
        "the run artifact carries an arm that is neither reused nor completed",
    )
    equivalence = document.get("equivalence_arms")
    require(
        isinstance(equivalence, list) and len(equivalence) == len(EQUIVALENCE_ARMS),
        f"a complete sweep records exactly {len(EQUIVALENCE_ARMS)} equivalence arms",
    )
    require(
        all(
            arm.get("status") == ARM_COMPLETED and arm.get("comparison") == COMPARISON_PASS
            for arm in equivalence
        ),
        "a complete sweep requires both equivalence arms to complete and to pass",
    )


# ---------------------------------------------------------------------------
# The command line and the terminal exits
# ---------------------------------------------------------------------------
def parse_args(argv: Sequence[str] | None = None) -> argparse.Namespace:
    """Parse the sweep's command line. Every machine-specific input is required.

    There is deliberately **no capacity flag beyond the predeclared grid, no
    `enforce_rung1_band` flag, and no epochs / batch-size / learning-rate / device
    flag.** Design section 4.1 holds the optimization protocol exactly fixed and lets
    width and nothing else vary; a command-line override would move that decision to
    invocation time, which is the shape the approved trainer's missing
    `--window-origin-step` was removed for.
    """

    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument("--mode", choices=("plan", "execute"), required=True)
    parser.add_argument("--run-label", default=None)
    parser.add_argument("--output-dir", type=Path, default=None)
    parser.add_argument("--base-dir", type=Path, default=None)
    parser.add_argument("--data-root", type=Path, default=None)
    parser.add_argument("--approved-plan", type=Path, default=None)
    parser.add_argument("--approved-plan-sha256", default=None)
    return parser.parse_args(argv)


def resolve_protocol() -> Any:
    """Return the fixed training protocol, derived from the approved assignment.

    The window policy is derived rather than supplied -- `origin = onset + lead`, the
    lead being the split's own diagnostic probe offset -- exactly as the approved trainer
    derives it, from the same document checked against the same digest. There is no
    command-line way to supply it.
    """

    schedule_by_trajectory, assignment_digest = trainer.authorized_window_schedule()
    return trainer.TrainingProtocol(
        schedule=tuple(
            schedule_by_trajectory[key] for key in sorted(schedule_by_trajectory)
        ),
        assignment_sha256=assignment_digest,
        window_steps=trainer.DEVELOPMENT_WINDOW_STEPS,
        control_dt_s=trainer.DEVELOPMENT_CONTROL_DT_S,
        epochs=SWEEP_EPOCHS,
        batch_size=SWEEP_BATCH_SIZE,
        learning_rate=SWEEP_LEARNING_RATE,
        device=SWEEP_DEVICE,
    ).validate()


def load_dev_examples(data_root: Path) -> tuple[dict[str, list[Any]], dict[str, Any]]:
    """Load the authorized dev examples once per suite, for every capacity point.

    Inputs: the delivered data root. Outputs: `{suite: examples}` and the census the run
    artifact records. Purpose: the window policy does not depend on width, so the same
    152 examples per suite serve every capacity point; loading them once is the only
    saving this executable takes, and it is a saving that cannot change a number.

    Every bound the approved trainer applies is applied here through the same calls --
    the authorized root name, manifest digest and config identity, `select_dev_rows`, the
    matched trajectory census, and `require_dev_only` at the point of consumption inside
    `load_arm_examples`. **Nothing here can reach a pilot, validation or test row.**
    """

    examples, census = approved_analysis.load_authorized_examples(Path(data_root))
    return examples, census


def curve_arm_document(
    *,
    channels: int,
    suite: str,
    seed: int,
    shape: Mapping[str, int],
    checkpoint_name: str,
    checkpoint_sha256: str,
    metrics: Mapping[str, Any],
    final_loss: float,
    loss_history: Sequence[float],
    n_examples: int,
) -> dict[str, Any]:
    """Return one completed curve arm's persisted record (design section 5.2)."""

    return {
        "accuracy": metrics["accuracy"],
        "channels": channels,
        "checkpoint_relative_name": checkpoint_name,
        "checkpoint_sha256": checkpoint_sha256,
        "final_loss": final_loss,
        "loss_history": list(loss_history),
        "macro_f1": metrics["macro_f1"],
        "n_examples": n_examples,
        "n_parameters": shape["n_parameters"],
        "per_class_f1": dict(sorted(dict(metrics["per_class_f1"]).items())),
        "receptive_field": shape["receptive_field"],
        "seed": seed,
        "source": "capacity-sweep",
        "status": ARM_COMPLETED,
        "suite": suite,
    }


def run_document(
    *,
    exit_name: str,
    reason_class: str | None,
    run_label: str,
    approved_plan_sha256: str,
    protocol: Any,
    curve: Sequence[Mapping[str, Any]],
    equivalence: Sequence[Mapping[str, Any]],
    fits_attempted: int,
    checkpoints_written: int,
    census: Mapping[str, Any] | None,
    elapsed_s: float,
) -> dict[str, object]:
    """Return the run-level terminal document design section 7.2 requires.

    It is written on **every** terminal path after the atomic claim succeeds, records the
    consumed plan digest and label so separately authorized runs are distinguishable in
    the preserved artifacts, gives every curve arm exactly one of the four statuses,
    separates equivalence fits from curve fits in the counts, and carries the exit name
    and elapsed time. A refusal's `reason_class` is recorded; its message never is.
    """

    return {
        "approved_plan_sha256": approved_plan_sha256,
        "authority": SWEEP_AUTHORITY,
        "capacity_points": list(CAPACITY_POINTS),
        "checkpoints_written": checkpoints_written,
        "code_identity": sweep_code_identity(),
        "curve_arms": list(curve),
        "data_census": dict(census) if census is not None else None,
        "design_sha256": DESIGN_CANONICAL_SHA256,
        "elapsed_s": elapsed_s,
        "equivalence_arms": list(equivalence),
        "exit": exit_name,
        "fits_attempted": fits_attempted,
        "generation_runs": 0,
        "maximum_budget": {
            "checkpoints": MAX_CHECKPOINTS,
            "fits": MAX_FITS,
            "generation_runs": 0,
            "non_dev_reads": 0,
            "rollouts": 0,
        },
        "mode": "execute",
        "non_dev_reads": 0,
        "reason_class": reason_class,
        "rollouts_spent": 0,
        "run_label": run_label,
        "training_protocol": protocol.as_document(),
    }


def _plan_mode(args: argparse.Namespace) -> int:
    """Run plan mode: zero fits, zero payload reads, byte-deterministic output."""

    output_dir = args.output_dir
    if output_dir is None:
        print(f"{X_CONTRACT_REFUSED}: --mode plan requires --output-dir")
        return EXIT_CODES[X_CONTRACT_REFUSED]
    output_dir = Path(output_dir)
    try:
        require(
            args.run_label is not None,
            "--mode plan requires --run-label",
        )
        protocol = resolve_protocol()
        document = plan_document(run_label=args.run_label, protocol=protocol)
    except (DevFitContractError, CapacitySweepError) as error:
        refusal = {
            "authority": SWEEP_AUTHORITY,
            "exit": X_CONTRACT_REFUSED,
            "fits_attempted": 0,
            "generation_runs": 0,
            "mode": "plan",
            "non_dev_reads": 0,
            "plan_valid": False,
            "reason_class": type(error).__name__,
            "rollouts_spent": 0,
        }
        write_document(output_dir / PLAN_ARTIFACT, refusal)
        print(f"{X_CONTRACT_REFUSED}: {error}")
        return EXIT_CODES[X_CONTRACT_REFUSED]
    write_document(output_dir / PLAN_ARTIFACT, document)
    print(
        f"{X_PLAN_OK}: {document['n_new_arms']} new arms + "
        f"{document['n_equivalence_arms']} equivalence arms planned at run label "
        f"{document['run_label']}, 0 fits run"
    )
    return EXIT_CODES[X_PLAN_OK]


def _execute_mode(args: argparse.Namespace) -> int:
    """Run execute mode: claim the root, measure the seam, then fit the forty arms."""

    started = time.monotonic()
    attempt_uuid = str(uuid.uuid4())
    if args.base_dir is None:
        print(f"{X_CONTRACT_REFUSED}: --mode execute requires --base-dir")
        return EXIT_CODES[X_CONTRACT_REFUSED]

    # Invariant C1, before any write of any kind. See `require_permitted_base`: this is
    # the one terminal exit that persists nothing, because every sink is under the base.
    try:
        base_dir = require_permitted_base(args.base_dir)
    except ForbiddenBase as error:
        print(f"{X_FORBIDDEN_BASE}: {error} (no artifact written, by construction)")
        return EXIT_CODES[X_FORBIDDEN_BASE]

    # Pre-claim refusals persist in the sibling `_unbound` sink: no trustworthy label or
    # digest exists yet, so both are recorded as null rather than guessed.
    try:
        protocol = resolve_protocol()
        require(
            args.approved_plan is not None and args.approved_plan_sha256 is not None,
            "--mode execute requires --approved-plan and --approved-plan-sha256",
        )
        require(args.data_root is not None, "--mode execute requires --data-root")
        plan = require_authorized_plan(
            args.approved_plan,
            expected_sha256=args.approved_plan_sha256,
            protocol=protocol,
        )
    except (DevFitContractError, CapacitySweepError) as error:
        write_refusal_document(
            base_dir,
            None,
            refusal_document(
                exit_name=X_PLAN_UNAUTHORIZED,
                reason_class=type(error).__name__,
                run_label=None,
                approved_plan_sha256=None,
                attempt_uuid=attempt_uuid,
                elapsed_s=time.monotonic() - started,
            ),
        )
        print(f"{X_PLAN_UNAUTHORIZED}: {error}")
        return EXIT_CODES[X_PLAN_UNAUTHORIZED]

    run_label = plan["run_label"]
    plan_digest = args.approved_plan_sha256
    try:
        run_root = claim_run_root(base_dir, run_label)
    except RunRootOccupied as error:
        write_refusal_document(
            base_dir,
            run_label,
            refusal_document(
                exit_name=X_RUN_ROOT_OCCUPIED,
                reason_class=type(error).__name__,
                run_label=run_label,
                approved_plan_sha256=plan_digest,
                attempt_uuid=attempt_uuid,
                elapsed_s=time.monotonic() - started,
            ),
        )
        print(f"{X_RUN_ROOT_OCCUPIED}: {error}")
        return EXIT_CODES[X_RUN_ROOT_OCCUPIED]
    except CapacitySweepError as error:
        write_refusal_document(
            base_dir,
            run_label,
            refusal_document(
                exit_name=X_DATA_MISSING,
                reason_class=type(error).__name__,
                run_label=run_label,
                approved_plan_sha256=plan_digest,
                attempt_uuid=attempt_uuid,
                elapsed_s=time.monotonic() - started,
            ),
        )
        print(f"{X_DATA_MISSING}: {error}")
        return EXIT_CODES[X_DATA_MISSING]

    # From here every terminal path writes the run-level document inside the claimed root.
    shape = capacity_shape_map()
    ledger = read_json_document(packet_root() / APPROVED_RESULT_RELATIVE, "approved fit ledger")
    analysis = read_json_document(
        packet_root() / APPROVED_ANALYSIS_RELATIVE, "approved analysis artifact"
    )
    curve: list[dict[str, Any]] = []
    equivalence: list[dict[str, Any]] = []
    fits_attempted = 0
    checkpoints_written = 0
    census: dict[str, Any] | None = None

    def _terminal(exit_name: str, reason_class: str | None) -> int:
        document = run_document(
            exit_name=exit_name,
            reason_class=reason_class,
            run_label=run_label,
            approved_plan_sha256=plan_digest,
            protocol=protocol,
            curve=curve,
            equivalence=equivalence,
            fits_attempted=fits_attempted,
            checkpoints_written=checkpoints_written,
            census=census,
            elapsed_s=time.monotonic() - started,
        )
        write_document(run_root / RUN_ARTIFACT, document)
        return EXIT_CODES[exit_name]

    try:
        require_anchor_comparability(ledger, protocol)
        curve.extend(approved_anchor_arms(ledger, analysis))
        examples, census = load_dev_examples(args.data_root)
    except DevFitContractError as error:
        print(f"{X_CONTRACT_REFUSED}: {error}")
        return _terminal(X_CONTRACT_REFUSED, type(error).__name__)
    except (CapacitySweepError, DevFitDataError, approved_analysis.DevFitAnalysisError) as error:
        print(f"{X_DATA_MISSING}: {error}")
        return _terminal(X_DATA_MISSING, type(error).__name__)

    try:
        gate = equivalence_gate(
            examples_by_suite=examples,
            ledger=ledger,
            checkpoint_dir=packet_root() / APPROVED_CHECKPOINT_RELATIVE,
            scratch_dir=run_root / EQUIVALENCE_SUBTREE,
            protocol=protocol,
        )
        equivalence = list(gate["arms"])
        fits_attempted += sum(
            1 for arm in equivalence if arm["status"] == ARM_COMPLETED
        )
        checkpoints_written += sum(
            1 for arm in equivalence if arm["status"] == ARM_COMPLETED
        )
    except EquivalenceFailure as error:
        print(f"{X_EQUIVALENCE_FAILED}: {error}")
        return _terminal(X_EQUIVALENCE_FAILED, type(error).__name__)
    except (DevFitContractError, DevFitDataError, CapacitySweepError) as error:
        print(f"{X_EQUIVALENCE_FAILED}: {error}")
        return _terminal(X_EQUIVALENCE_FAILED, type(error).__name__)

    device = torch.device(protocol.device)
    for channels, suite, seed in curve_arms():
        point_dir = run_root / f"channels_{channels:03d}"
        try:
            require_clean_capacity_point(point_dir)
        except DevFitContractError as error:
            print(f"{X_OUTPUT_DIRTY}: {error}")
            return _terminal(X_OUTPUT_DIRTY, type(error).__name__)
        fits_attempted += 1
        try:
            net, history = fit_arm_at_width(
                examples[suite],
                seed=seed,
                channels=channels,
                epochs=protocol.epochs,
                batch_size=protocol.batch_size,
                learning_rate=protocol.learning_rate,
                device=device,
            )
            metrics = score_arm(net, examples[suite])
        except DevFitContractError as error:
            curve.append(
                {
                    "channels": channels,
                    "reason_class": type(error).__name__,
                    "seed": seed,
                    "status": ARM_REFUSED,
                    "suite": suite,
                }
            )
            print(f"{X_CONTRACT_REFUSED}: {error}")
            return _terminal(X_CONTRACT_REFUSED, type(error).__name__)
        except (DevFitDataError, RuntimeError) as error:
            curve.append(
                {
                    "channels": channels,
                    "reason_class": type(error).__name__,
                    "seed": seed,
                    "status": ARM_REFUSED,
                    "suite": suite,
                }
            )
            print(f"{X_DATA_MISSING}: {error}")
            return _terminal(X_DATA_MISSING, type(error).__name__)
        buffer = io.BytesIO()
        torch.save(net.state_dict(), buffer)
        payload = buffer.getvalue()
        relative = checkpoint_relative_name(channels, suite, seed)
        (run_root / relative).parent.mkdir(parents=True, exist_ok=True)
        (run_root / relative).write_bytes(payload)
        checkpoints_written += 1
        curve.append(
            curve_arm_document(
                channels=channels,
                suite=suite,
                seed=seed,
                shape=shape[channels],
                checkpoint_name=relative,
                checkpoint_sha256=hashlib.sha256(payload).hexdigest(),
                metrics=metrics,
                final_loss=history[-1],
                loss_history=history,
                n_examples=len(examples[suite]),
            )
        )
        print(
            f"fitted {channels} channels {suite} seed {seed}: "
            f"macro-F1 {metrics['macro_f1']:.6f}, final loss {history[-1]:.6f}"
        )

    try:
        require_complete_sweep(
            {"curve_arms": curve, "equivalence_arms": equivalence}
        )
    except DevFitContractError as error:
        print(f"{X_PLAN_INCOMPLETE}: {error}")
        return _terminal(X_PLAN_INCOMPLETE, type(error).__name__)

    print(
        f"{X_SWEEP_OK}: {len(curve_arms())} new arms fitted, "
        f"{len(anchor_arms())} anchors reused, {len(EQUIVALENCE_ARMS)} equivalence "
        f"checks passed, 0 rollouts spent"
    )
    return _terminal(X_SWEEP_OK, None)


def main(argv: Sequence[str] | None = None) -> int:
    """Run the sweep and return the exit code of the terminal exit it took."""

    args = parse_args(argv)
    if args.mode == "plan":
        return _plan_mode(args)
    return _execute_mode(args)


if __name__ == "__main__":  # pragma: no cover - exercised through main(argv)
    sys.exit(main())
