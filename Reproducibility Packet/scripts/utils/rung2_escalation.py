"""Gate-4 rung-2 escalation: the factory-parameterized fit executable.

This is step 3 of the frozen design `protocol/rung2-escalation-v0.1.md` (canonical
SHA-256 `9a154f90...`, jointly approved at Claude Session 112 / Codex Session 112).
It exists because neither approved fitter can build a rung-2 network: the trainer's
only construction site is `TemporalAttributionNet(seed=seed)`
(`dev_fit_trainer.py:968`) and the Stage-1 sweep's `require_capacity_point` refuses
anything off the `{16..48}` rung-1 grid (design section 4.5).

What this module may do, and what it may not
--------------------------------------------
It may enumerate the run (plan mode) and, under a separate joint authorization naming
an approved plan's digest, fit two rung-1 equivalence arms and ten rung-2 arms on the
same authorized `dev` rows the approved ledger used, scoring each arm in sample. It
may not re-fit the ten approved 32-channel anchors, write into `results/dev_fit`, read
a pilot, validation or test row, spend a rollout, generate data, set a threshold, or
select a capacity. Bound 5 of the dev-fit contract governs the result: development-only
instrument diagnosis and ladder history, never held-out evidence, never a headline
result, and never a capacity selection.

**Building this module is not permission to run it.** Design section 11 sequences the
gates: the design is frozen (done), the rung-2 module is built and reviewed (done),
this executable and its tests are reviewed (this state), plan mode is run and its
artifact reviewed, and only then is execution a separate joint authorization in two
halves.

One fit loop, two factories -- and what measures the copy
---------------------------------------------------------
`fit_arm` below is the approved `dev_fit_trainer.fit_one_arm` body with exactly one
expression parameterized: the network construction becomes `network_factory(seed=seed)`.
The rung-2 arms pass `build_rung2_network`; the equivalence gate passes
`build_rung1_reference_network`, which is `TemporalAttributionNet(seed=seed)` with
every default untouched -- 32 channels, `enforce_rung1_band` at its default `True`.
That is design section 4.5's improvement on Stage 1's Route A: the gate exercises the
*identical* code path the measured arms use and differs only in the factory, rather
than being a second loop that happens to look the same.

The loop is not asserted to equal the approved one; it is **measured** before use.
`equivalence_gate` (invariant R6) refits `(C1, seed 0)` and `(S, seed 4)` through this
module's own path and requires the parameter tensors **and** the per-epoch loss history
to be bit-identical to the approved Session-84 checkpoints and ledger rows. Nothing
downstream runs unless both comparisons pass.

Every **project-defined** name the loop body uses is imported from an approved module
rather than retyped -- `require_predeclared_seed`, `deterministic_conv_precision`,
`arm_loss`, `_stack`, `DevFitDataError` -- so the objective, which is the part that is
science rather than plumbing, keeps exactly one definition across both rungs. The
control flow and the third-party PyTorch/NumPy expressions are necessarily copied; no
project helper wraps them, and design section 4.5's table is the complete
project-defined call surface rather than the complete Python one.

The import ledger, including what it adds to design section 4.5's table
-----------------------------------------------------------------------
Section 4.5 names the imports this module must not re-write. All of them are taken:
`arm_loss`, `_stack`, `DevFitDataError`, `require_predeclared_seed`,
`deterministic_conv_precision`, `AttributionHeads` (through the rung-2 module's own
contract), `capacity_sweep.score_arm`, and `capacity_sweep`'s
`require_permitted_base`, `claim_run_root`, `require_run_label`, `write_document`,
`read_json_document`, `read_field`, `state_dicts_are_bit_identical` and `quantize`.

Eight further names come from `capacity_sweep` beyond that table, and they are listed
here rather than buried, because an import ledger a reviewer cannot check at a glance
is not a ledger:

* `packet_root`, `require_approved_analyzer_identity` -- the same two operations on the
  same packet and the same approved analysis artifact;
* `CapacitySweepError`, `ForbiddenBase`, `RunRootOccupied`, `EquivalenceFailure` -- the
  refusal vocabulary of the machinery being imported. Re-declaring them would mean
  catching two exception families for one condition;
* `ANCHOR_CHANNELS`, `EQUIVALENCE_ARMS`, `EQUIVALENCE_SUBTREE`,
  `UNBOUND_LABEL_DIRECTORY`, the three `APPROVED_*_RELATIVE` paths, and the `ARM_*` /
  `COMPARISON_*` status vocabularies -- the same values naming the same things. Design
  section 4.5 rules the gate's two arms to be "the same pair Stage 1's C9 used", and
  importing the tuple is how that sentence becomes a fact rather than a coincidence.

`Rung2EscalationError` subclasses `CapacitySweepError` for the same reason: one
`except` clause then covers this module's own diagnosis and the imported machinery's,
so a new refusal cannot slip past a handler that named only one of the two.

The one helper that could not be reused, and why it was copied instead
----------------------------------------------------------------------
`capacity_sweep.write_refusal_document` writes into a sink named by that module's
`REFUSAL_SINK_NAME` constant and takes no sink parameter, so a rung-2 refusal would be
filed under the capacity sweep's name. The approved module may not be edited to add one
(design decision D4: `capacity_sweep.py` is an entry of its own `sweep_code_identity()`,
and editing it changes a recorded identity). So this module declares its own sink and
its own near-identical writer, and invariant R9 requires a test that drives both writers
with one fixed valid UUID, asserts the JSON payloads are exactly equal, and isolates the
path difference to the sink-directory component -- so the copy cannot drift silently.

Where this executable is allowed to write
-----------------------------------------
Three locations, all named (design sections 6 R1/R2 and 7):

1. the run root `<base>/<run_label>/`, claimed by **one atomic create that requires the
   path to be absent**; any pre-existing path -- file, empty directory or populated
   directory -- is the named terminal `X_RUN_ROOT_OCCUPIED`;
2. the sibling refusal sink `<base>/_rung2_escalation_refusals/<run_label>/<uuid>.json`,
   and `.../_unbound/<uuid>.json` before a trustworthy label exists. It sits outside the
   run root by necessity: a refusal must never report through the resource whose
   occupancy triggered it (lesson 116);
3. the reserved `_equivalence/` subtree of the claimed run root, which holds the two
   rung-1 compatibility checkpoints and their comparison artifact, so they are inside
   the run whose gate they are and never anywhere near `results/dev_fit`.

Both sink names are safe by construction rather than by convention: `run_label` must
match `^[a-z0-9][a-z0-9-]{2,31}$`, whose character class contains no underscore, so no
conforming label can name `_rung2_escalation_refusals` or `_unbound`.

The two exits that persist nothing, disclosed rather than discovered
--------------------------------------------------------------------
Design section 6 names two pre-persistence boundaries. A missing required destination
has nowhere authorized to write, and `X_FORBIDDEN_BASE` -- a supplied destination at or
inside `results/dev_fit` -- must not persist under the protected base whose use it is
refusing, because every sink this module has is under the supplied destination. Both
print the named refusal **and zero resource counts** to stdout and write nothing.

Why the derived read of design section 5 lives here but is not run here
-----------------------------------------------------------------------
`arm_objective_reduced`, `optimization_check_passed`, `deficit_sign_label` and
`require_complete_rung2_run` are pure functions of persisted primitives and carry no
I/O. They are defined here so the read-only analyzer invariant R7 requires -- a separate
build and a separate review -- imports them instead of writing a second definition of
the criteria the whole read turns on. This executable calls exactly two of them:
`arm_objective_reduced`, because section 5.2 makes `objective_reduced` a **persisted
primitive** of each arm, and `require_complete_rung2_run`, because an incomplete run
must take a named terminal rather than print success. The run-level
`OPTIMIZATION_CHECK_PASSED` status and every paired or cross-rung quantity are the
analyzer's to derive, and this module emits none of them.
"""

from __future__ import annotations

import argparse
import hashlib
import io
import re
import sys
import time
import uuid
from decimal import Decimal
from pathlib import Path
from typing import Any, Callable, Mapping, Sequence

import numpy as np
import torch

from .attribution_net import (
    CAPACITY_LADDER,
    TemporalAttributionNet,
    deterministic_conv_precision,
)
from .attribution_net_rung2 import (
    RUNG2_DECLARED_PARAMETERS,
    RUNG2_MAX_PARAMETERS,
    RUNG2_MIN_PARAMETERS,
    RUNG2_NAME,
    RecurrentAttentionAttributionNet,
)
from .capacity_sweep import (
    ANCHOR_CHANNELS,
    APPROVED_ANALYSIS_RELATIVE,
    APPROVED_CHECKPOINT_RELATIVE,
    APPROVED_RESULT_RELATIVE,
    ARM_COMPLETED,
    ARM_REFUSED,
    ARM_UNATTEMPTED,
    COMPARISON_FAIL,
    COMPARISON_NOT_RUN,
    COMPARISON_PASS,
    EQUIVALENCE_ARMS,
    EQUIVALENCE_SUBTREE,
    UNBOUND_LABEL_DIRECTORY,
    CapacitySweepError,
    EquivalenceFailure,
    ForbiddenBase,
    RunRootOccupied,
    claim_run_root,
    packet_root,
    quantize,
    read_field,
    read_json_document,
    require_approved_analyzer_identity,
    require_permitted_base,
    require_run_label,
    score_arm,
    state_dicts_are_bit_identical,
    write_document,
)
from .dev_fit_contract import (
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
# contexts this module is. Design section 3 requires it: the classification metrics are
# the approved analyzer's, because a second definition of macro-F1 in this project would
# be a second definition of the quantity the whole read is about.
import analyze_dev_fit as approved_analysis  # noqa: E402


# ---------------------------------------------------------------------------
# Terminal exits. A name rather than a bare integer, because every artifact this
# module writes records which exit was taken.
#
# There is deliberately no `X_OUTPUT_DIRTY`. Stage 1 needed one because ten arms shared
# a per-width directory that the plan named and the guard inspected (finding AU); rung 2
# has one configuration, writes every arm into a run root claimed **absent** by one
# atomic create, and therefore has no directory an earlier attempt could have filled.
# ---------------------------------------------------------------------------
X_PLAN_OK = "X_PLAN_OK"
X_RUNG2_OK = "X_RUNG2_OK"
X_CONTRACT_REFUSED = "X_CONTRACT_REFUSED"
X_DATA_MISSING = "X_DATA_MISSING"
X_RUN_INCOMPLETE = "X_RUN_INCOMPLETE"
X_RUN_ROOT_OCCUPIED = "X_RUN_ROOT_OCCUPIED"
X_PLAN_UNAUTHORIZED = "X_PLAN_UNAUTHORIZED"
X_EQUIVALENCE_FAILED = "X_EQUIVALENCE_FAILED"
X_FORBIDDEN_BASE = "X_FORBIDDEN_BASE"

EXIT_CODES: dict[str, int] = {
    X_PLAN_OK: 0,
    X_RUNG2_OK: 0,
    X_CONTRACT_REFUSED: 3,
    X_DATA_MISSING: 4,
    X_RUN_INCOMPLETE: 5,
    X_RUN_ROOT_OCCUPIED: 6,
    X_PLAN_UNAUTHORIZED: 7,
    X_EQUIVALENCE_FAILED: 8,
    X_FORBIDDEN_BASE: 9,
}


# ---------------------------------------------------------------------------
# The design this executable implements, pinned by digest (invariant R11).
#
# The frozen v0.1 document is a tripwire: editing it in place turns plan mode red. That
# is the intended consequence of freezing it -- the document's own version discipline
# says an approved version is never edited in place, only bumped and `git mv`'d, and a
# bump must move this constant with it.
# ---------------------------------------------------------------------------
DESIGN_DOCUMENT_NAME = "rung2-escalation-v0.1.md"
DESIGN_CANONICAL_SHA256 = (
    "9a154f902d7a98dcaa3e8bd34109e2ea6c4f29ba08c86a4ad301bfd62e69bf1f"
)

RUNG2_AUTHORITY = (
    "DEVELOPMENT-ONLY RUNG-2 ESCALATION: one recurrent-plus-attention architecture "
    "fitted in sample under the unchanged rung-1 protocol; not held-out evidence, not "
    "a capacity selection, and not a C1-versus-S result"
)

# The rung names are taken from the approved ladder rather than retyped, so a rename in
# `attribution_net.CAPACITY_LADDER` cannot leave this module naming a rung that no
# longer exists. `RUNG2_NAME` is imported from the rung-2 module, which is itself pinned
# against the ladder's second entry by that module's tests.
RUNG1_NAME = CAPACITY_LADDER[0].name

# Design section 4.1. Held exactly fixed; deliberately NOT command-line arguments,
# because "varies: the architecture, and nothing else" is not a property an operator may
# edit at invocation. Invariant R3 checks each of them against the approved ledger,
# which is an independent source for the same fact.
RUNG2_EPOCHS = 20
RUNG2_BATCH_SIZE = 8
RUNG2_LEARNING_RATE = 1.0e-3
RUNG2_DEVICE = "cpu"

# Design sections 6 R2 and 7. The label grammar is the approved module's; the sink name
# is this module's own, for the reason the docstring gives.
REFUSAL_SINK_NAME = "_rung2_escalation_refusals"
LOGICAL_NAMESPACE_ROOT = "results/rung2_escalation"

PLAN_ARTIFACT = "rung2_escalation_plan.json"
RUN_ARTIFACT = "rung2_escalation_result.json"
EQUIVALENCE_ARTIFACT = "rung2_escalation_equivalence.json"

# Design section 7.1: the maximum budget. It is *stated* in the plan and *recorded* on
# every exit. There is deliberately no run-time comparison of the counts against it --
# the budget is not a limit the executable enforces but an arithmetic property of the
# arm lists it iterates. What keeps the constant honest is
# `test_the_maximum_budget_is_twelve_fits`, which pins it to
# `len(rung2_arms()) + len(EQUIVALENCE_ARMS)` by equality, so the arm lists cannot drift
# away from the number without a red test. Said exactly, because a comment claiming an
# assertion the code does not make is the defect finding AN was about.
MAX_FITS = 12
MAX_CHECKPOINTS = 12

# Design section 5.2: the approved rung-1 numbers are **read**, never recomputed, and
# the field they were read from is recorded beside the value, because a sourced constant
# whose source is not written down is a literal with a footnote.
ANCHOR_MACRO_F1_FIELD = "arms[].classification.macro_f1"
ANCHOR_PER_CLASS_F1_FIELD = "arms[].classification.per_class_f1"

# Design section 5.2's three-valued sign label. It is a description of five signs, not a
# test, and no branch of it authorizes anything.
SIGN_REPRODUCED = "REPRODUCED_IN_SIGN"
SIGN_NOT_REPRODUCED = "NOT_REPRODUCED_IN_SIGN"
SIGN_MIXED = "MIXED"

# Design section 5.1's run-level status names.
OPTIMIZATION_CHECK_PASSED = "OPTIMIZATION_CHECK_PASSED"
OPTIMIZATION_CHECK_FAILED = "OPTIMIZATION_CHECK_FAILED"


class Rung2EscalationError(CapacitySweepError):
    """This module's own diagnosis: an input it needs could not be assembled.

    It subclasses the imported machinery's error deliberately. Every helper this module
    imports from `capacity_sweep` raises `CapacitySweepError`, so a separate root class
    would mean every handler had to name two families for one condition -- and the
    handler that named only one would be the defect. `type(error).__name__` still
    records which class actually fired, so the artifacts stay precise.
    """


# ---------------------------------------------------------------------------
# The arms, the two factories, and the one fit loop
# ---------------------------------------------------------------------------
def rung2_arms() -> tuple[tuple[str, int], ...]:
    """Return the ten `(suite, seed)` rung-2 arms this run fits.

    Inputs: none. Outputs: the two matched suites crossed with the five predeclared
    seeds, in a fixed order. Purpose: design section 3 -- ten development fits of one
    named architecture, at the anchor's own seeds, so the rung-1 pairing survives.
    """

    return tuple(
        (suite, seed)
        for suite in MATCHED_FIT_SUITES
        for seed in PREDECLARED_TRAINING_SEEDS
    )


def build_rung2_network(*, seed: int) -> RecurrentAttentionAttributionNet:
    """Return the rung-2 network at the one selected configuration.

    Inputs: a predeclared seed. Outputs: the constructed network. Purpose: the **one**
    rung-2 construction site in this module, so the declared configuration is a property
    of the module rather than of each call site. Every size argument is left at the
    rung-2 module's declared default, and there is no argument anywhere in this file
    that can disable the band check -- the rung-2 constructor accepts none (invariant
    R5), and this factory adds none.
    """

    require_predeclared_seed(seed)
    return RecurrentAttentionAttributionNet(seed=seed)


def build_rung1_reference_network(*, seed: int) -> TemporalAttributionNet:
    """Return the approved rung-1 network the equivalence gate refits.

    Inputs: a predeclared seed. Outputs: `TemporalAttributionNet(seed=seed)` with every
    default untouched -- 32 channels, nine blocks, and `enforce_rung1_band` at its
    default `True`. Purpose: design section 4.5 requires the gate to pass a rung-1
    factory through the *same* `fit_arm` the rung-2 arms use. Passing any argument other
    than the seed would make the gate a check on a configuration the approved trainer
    never built, which is the one thing it may not be.
    """

    require_predeclared_seed(seed)
    return TemporalAttributionNet(seed=seed)


def rung2_shape() -> dict[str, Any]:
    """Return `{rung, n_parameters, stem_receptive_field}` read off a constructed net.

    Inputs: none. Outputs: the measured shape of the declared configuration. Purpose:
    invariant R4 -- the rung and the band are **recorded from the constructed network**,
    not re-derived from this module's constants, and a disagreement is a refusal rather
    than a note.

    The band assertion here is defence in depth: the rung-2 constructor already makes
    it unconditionally. The **exact-count** assertion is the load-bearing one, and the
    reason is measured rather than asserted -- an `nn.MultiheadAttention` attention block
    builds 228,330 parameters, which is *inside* the declared band, so the band cannot
    tell the two architectures apart and only the exact count refuses the wrong one.
    """

    net = build_rung2_network(seed=PREDECLARED_TRAINING_SEEDS[0])
    n_parameters = int(net.n_parameters)
    stem_receptive_field = int(net.stem_receptive_field)
    rung = str(net.rung)
    require(
        rung == RUNG2_NAME,
        f"the constructed network reports rung {rung!r}; this executable fits "
        f"{RUNG2_NAME!r}",
    )
    require(
        n_parameters == RUNG2_DECLARED_PARAMETERS,
        f"the declared rung-2 configuration built {n_parameters} parameters; the frozen "
        f"design reserves {RUNG2_DECLARED_PARAMETERS}",
    )
    require(
        RUNG2_MIN_PARAMETERS <= n_parameters <= RUNG2_MAX_PARAMETERS,
        f"the declared rung-2 configuration is outside the band "
        f"[{RUNG2_MIN_PARAMETERS}, {RUNG2_MAX_PARAMETERS}]",
    )
    return {
        "n_parameters": n_parameters,
        "rung": rung,
        "stem_receptive_field": stem_receptive_field,
    }


def rung2_code_identity() -> dict[str, str]:
    """Return the twelve-entry code identity every rung-2 arm records.

    Inputs: none. Outputs: `{bare label: canonical text digest}`. Purpose: invariant
    R12 and design section 5.2 -- the approved trainer's eight historical entries
    unchanged, `capacity_sweep.py` and `analyze_dev_fit.py` because this path imports
    their scoring and persistence machinery, and the two new producers
    `attribution_net_rung2.py` and `rung2_escalation.py`.

    The design digest proves which protocol authorized the executable; it does **not**
    substitute for the code identity that produced a checkpoint, which is why both are
    persisted.
    """

    here = Path(__file__).resolve().parent
    identity = dict(trainer.training_code_identity())
    identity.update(
        code_identity(
            {
                "attribution_net_rung2.py": here / "attribution_net_rung2.py",
                "capacity_sweep.py": here / "capacity_sweep.py",
                "rung2_escalation.py": here / "rung2_escalation.py",
            }
        )
    )
    identity.update(
        code_identity(
            {"analyze_dev_fit.py": Path(approved_analysis.__file__).resolve()}
        )
    )
    return dict(sorted(identity.items()))


def new_identity_entries() -> frozenset[str]:
    """Return the four labels this run adds to the approved anchor's code identity.

    Inputs: none. Outputs: the permitted addition set invariant R3 checks against.
    Purpose: R3 refuses any changed historical entry and any addition that is not one of
    these four; stating the set once means the guard and the plan cannot disagree about
    what "the new producers" means.
    """

    return frozenset(
        {
            "analyze_dev_fit.py",
            "attribution_net_rung2.py",
            "capacity_sweep.py",
            "rung2_escalation.py",
        }
    )


def fit_arm(
    examples: Sequence[Any],
    *,
    seed: int,
    network_factory: Callable[..., torch.nn.Module],
    epochs: int,
    batch_size: int,
    learning_rate: float,
    device: torch.device,
) -> tuple[torch.nn.Module, list[float]]:
    """Fit one arm through the one loop, and return its network and per-epoch mean loss.

    Inputs: the arm's examples, its predeclared seed, the network factory that decides
    which rung is being fitted, and the fixed optimization settings. Outputs: the fitted
    network and its per-epoch mean total objective.

    Purpose: the compatibility seam, and design section 4.5's improvement on Stage 1.
    This is `dev_fit_trainer.fit_one_arm`'s body with exactly one expression
    parameterized -- `TemporalAttributionNet(seed=seed)` becomes
    `network_factory(seed=seed)` -- so the rung-2 arms and the equivalence arms run the
    *same* loop and differ only in what it constructs. Three copies of the loop is where
    drift becomes inevitable; this is the second and last.

    `torch.manual_seed(seed)` is called **before** the factory, exactly as the approved
    trainer does, and the factory's own construction forks the RNG internally. Both rung
    constructors seed inside the fork, so the two rungs are matched in initialization
    procedure even though their tensors cannot be matched in value -- different shapes.

    `deterministic_conv_precision()` wraps the **whole** step, forward and backward, for
    the reason the approved trainer states: cuDNN's TF32 default applies to the
    convolution backward kernels too, so a context covering inference alone would leave
    the gradients at a different precision than the numbers it was opened to protect.

    Nothing here asserts that this loop equals the approved one. `equivalence_gate`
    measures it against the approved checkpoints before any rung-2 arm runs, which is
    the whole point of invariant R6.
    """

    require_predeclared_seed(seed)
    if not examples:
        raise DevFitDataError("a development-only fit may not consume an empty row set")
    torch.manual_seed(seed)
    net = network_factory(seed=seed).to(device)
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


# ---------------------------------------------------------------------------
# The approved anchor state: read, checked, never re-fitted (invariants R1 and R3)
# ---------------------------------------------------------------------------
def require_anchor_comparability(ledger: Mapping[str, Any], protocol: Any) -> None:
    """Refuse an anchor that was not produced by the code, data and protocol in use.

    Inputs: the approved fit ledger and the `TrainingProtocol` this run will use.
    Outputs: none. Purpose: invariant R3. If the match fails, a rung-2-versus-rung-1
    comparison is not a comparison of architectures, it is two unrelated experiments,
    and the executable must refuse with a named exit rather than record a number.

    The code-identity comparison is **entry by entry** over all eight historical
    entries. The four new producer labels are the only permitted additions; any changed
    historical entry, any missing entry, and any other addition is a refusal. The
    protocol comparison covers the window schedule, because `TrainingProtocol`'s
    document carries it, and the data identity is checked per approved arm.
    """

    recorded_identity = ledger.get("code_identity")
    require(
        isinstance(recorded_identity, Mapping) and bool(recorded_identity),
        "the approved ledger carries no code identity",
    )
    current = rung2_code_identity()
    additions = set(current) - set(recorded_identity)
    require(
        additions == set(new_identity_entries()),
        "the rung-2 run's code identity adds "
        + ", ".join(sorted(additions))
        + " to the approved ledger's; exactly the four new producer entries are "
        "permitted",
    )
    missing = set(recorded_identity) - set(current)
    require(
        not missing,
        "the rung-2 run's code identity drops " + ", ".join(sorted(missing)),
    )
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
        "the rung-2 run's training protocol differs from the approved anchor's at "
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


def anchor_records(
    ledger: Mapping[str, Any], analysis: Mapping[str, Any]
) -> list[dict[str, Any]]:
    """Return the ten approved rung-1 arms as read-only records.

    Inputs: the approved fit ledger and the approved in-sample analysis. Outputs: one
    record per anchor carrying its macro-F1, its per-class F1 map, the field each was
    read from, and the checkpoint digest. Purpose: design section 5.2 -- these numbers
    are **read from the approved rung-1 records and never recomputed**, because
    recomputing them would produce a second value claiming to be the same measurement,
    and because the approved values reach their record through the analyzer's own
    rounding (finding AV).

    The two documents are cross-checked rather than trusted separately: the digest the
    analysis scored is required to equal the digest the ledger recorded, which is a
    check whose two sides come from different files.
    """

    ledger_arms = ledger.get("arms")
    analysis_arms = analysis.get("arms")
    if not isinstance(ledger_arms, list) or not isinstance(analysis_arms, list):
        raise Rung2EscalationError("the approved anchor documents carry no arms list")

    expected = {(suite, seed) for suite, seed in rung2_arms()}

    def _index(
        rows: Sequence[Any], *, seed_field: str, label: str
    ) -> dict[tuple[str, int], Mapping[str, Any]]:
        indexed: dict[tuple[str, int], Mapping[str, Any]] = {}
        for arm in rows:
            if not isinstance(arm, Mapping):
                raise Rung2EscalationError(f"the {label} carries a non-object arm")
            suite = arm.get("suite")
            seed = arm.get(seed_field)
            if (
                not isinstance(suite, str)
                or not isinstance(seed, int)
                or isinstance(seed, bool)
            ):
                raise Rung2EscalationError(
                    f"the {label} carries an arm without a valid suite/seed identity"
                )
            key = (suite, seed)
            if key in indexed:
                raise Rung2EscalationError(
                    f"the {label} carries duplicate {suite} seed {seed} arms"
                )
            indexed[key] = arm
        if set(indexed) != expected:
            raise Rung2EscalationError(
                f"the {label} does not carry exactly the ten approved anchor identities"
            )
        return indexed

    by_key_ledger = _index(
        ledger_arms, seed_field="training_seed", label="approved ledger"
    )
    by_key_analysis = _index(analysis_arms, seed_field="seed", label="approved analysis")
    records: list[dict[str, Any]] = []
    for suite, seed in rung2_arms():
        ledger_arm = by_key_ledger[(suite, seed)]
        analysis_arm = by_key_analysis[(suite, seed)]
        digest = str(ledger_arm.get("checkpoint_sha256"))
        if str(analysis_arm.get("checkpoint_sha256")) != digest:
            raise Rung2EscalationError(
                f"the approved ledger and analysis disagree on the {suite} seed {seed} "
                "checkpoint digest"
            )
        # Each number is fetched through `read_field` by the exact path recorded beside
        # it, so an absent field is refused **by name** rather than by a `KeyError` two
        # frames away, and so the recorded `*_field` string and the lookup that produced
        # the value cannot describe different fields.
        label = f"approved analysis {suite} seed {seed} arm"
        macro_f1 = read_field(analysis_arm, ("classification", "macro_f1"), label)
        per_class_f1 = read_field(analysis_arm, ("classification", "per_class_f1"), label)
        if not isinstance(per_class_f1, Mapping):
            raise Rung2EscalationError(
                f"the approved analysis carries a non-object per-class F1 map for "
                f"{suite} seed {seed}"
            )
        records.append(
            {
                "checkpoint_sha256": digest,
                "macro_f1": macro_f1,
                "macro_f1_field": ANCHOR_MACRO_F1_FIELD,
                "per_class_f1": dict(sorted(dict(per_class_f1).items())),
                "per_class_f1_field": ANCHOR_PER_CLASS_F1_FIELD,
                "read_only": True,
                "rung": RUNG1_NAME,
                "seed": seed,
                "source": "approved-analysis",
                "suite": suite,
            }
        )
    return records


# ---------------------------------------------------------------------------
# Invariant R6 -- the equivalence gate
# ---------------------------------------------------------------------------
def initial_rung2_arm_records() -> list[dict[str, Any]]:
    """Return all ten rung-2 arm identities in their pre-fit state.

    Inputs: none. Outputs: the ten identities, each marked ``UNATTEMPTED``. Purpose:
    design section 7.2 requires *every* arm to carry exactly one status on every
    post-claim terminal path. Execute mode replaces these records in place as arms
    complete or refuse, so arms downstream of a failure remain explicitly
    ``UNATTEMPTED`` rather than disappearing from the terminal artifact.
    """

    return [
        {
            "rung": RUNG2_NAME,
            "seed": seed,
            "status": ARM_UNATTEMPTED,
            "suite": suite,
        }
        for suite, seed in rung2_arms()
    ]


def initial_equivalence_arm_records() -> list[dict[str, Any]]:
    """Return both equivalence identities in their pre-comparison state.

    Inputs: none. Outputs: the two ruled identities with ``UNATTEMPTED`` / ``NOT_RUN``
    state and null digests. Purpose: the run-level artifact retains the complete gate
    shape even when setup fails before the gate or the first arm refuses.
    """

    return [
        {
            "approved_loss_history": None,
            "channels": ANCHOR_CHANNELS,
            "equivalence_status": COMPARISON_NOT_RUN,
            "fit_code_identity": None,
            "loss_history_bit_identical": None,
            "reason_class": None,
            "refit_checkpoint_relative_name": None,
            "refit_checkpoint_sha256": None,
            "refit_loss_history": None,
            "rung": RUNG1_NAME,
            "rung1_reference_checkpoint_sha256": None,
            "seed": seed,
            "status": ARM_UNATTEMPTED,
            "suite": suite,
            "weights_bit_identical": None,
        }
        for suite, seed in EQUIVALENCE_ARMS
    ]


def equivalence_gate(
    *,
    examples_by_suite: Mapping[str, Sequence[Any]],
    ledger: Mapping[str, Any],
    checkpoint_dir: Path,
    scratch_dir: Path,
    protocol: Any,
    fit_code_identity: Mapping[str, str] | None = None,
) -> dict[str, Any]:
    """Measure this module's fit loop against the approved one, and refuse if it differs.

    Inputs: the loaded dev examples per suite, the approved ledger, the approved
    checkpoint directory, the reserved `_equivalence/` scratch subtree of the claimed
    run root, and the protocol. Outputs: the equivalence artifact.

    Purpose: invariant R6. Two rung-1 arms -- `(C1, 0)` and `(S, 4)` -- are refitted
    through **this module's `fit_arm`** with the rung-1 reference factory, and their
    parameter tensors and per-epoch loss history must be bit-identical to the
    corresponding approved checkpoint and ledger row. Without it, a difference between
    rung 1 and rung 2 is confounded with a difference between two fitting loops, and this
    module contains a new one by necessity.

    Refuses loudly on either difference, on either approved checkpoint being absent (a
    fresh clone carries the ledger without the weights), and on a comparison that cannot
    be made for any other reason. Nothing downstream of this runs unless both comparisons
    report `PASS`.
    """

    scratch_dir = Path(scratch_dir)
    identity = dict(
        sorted(
            dict(
                fit_code_identity
                if fit_code_identity is not None
                else rung2_code_identity()
            ).items()
        )
    )
    results = initial_equivalence_arm_records()
    for entry in results:
        entry["fit_code_identity"] = identity
    fits_attempted = 0
    checkpoints_written = 0

    def _document(*, gate_passed: bool) -> dict[str, Any]:
        return {
            "arms": [dict(entry) for entry in results],
            "authority": RUNG2_AUTHORITY,
            "checkpoints_written": checkpoints_written,
            "code_identity": identity,
            "equivalence_channels": ANCHOR_CHANNELS,
            "equivalence_rung": RUNG1_NAME,
            "fits_attempted": fits_attempted,
            "gate_passed": gate_passed,
            "generation_runs": 0,
            "non_dev_reads": 0,
            "rollouts_spent": 0,
        }

    def _raise_failure(
        message: str,
        *,
        entry: dict[str, Any] | None,
        reason_class: str,
        completed_fit: bool = False,
        cause: BaseException | None = None,
    ) -> None:
        if entry is not None:
            entry["equivalence_status"] = COMPARISON_FAIL
            entry["reason_class"] = reason_class
            entry["status"] = ARM_COMPLETED if completed_fit else ARM_REFUSED
        document = _document(gate_passed=False)
        try:
            write_document(scratch_dir / EQUIVALENCE_ARTIFACT, document)
        except Exception as artifact_error:
            # The claimed run-level terminal remains the authoritative fallback. Keep
            # only the error class; neither a path nor an exception message enters it.
            document["artifact_write_reason_class"] = type(artifact_error).__name__
        raise EquivalenceFailure(message, document=document) from cause

    try:
        scratch_dir.mkdir(parents=True, exist_ok=True)
    except OSError as error:
        _raise_failure(
            "the reserved equivalence subtree could not be created",
            entry=None,
            reason_class=type(error).__name__,
            cause=error,
        )

    ledger_arms: dict[tuple[str, int], Mapping[str, Any]] = {}
    for arm in ledger.get("arms", []):
        if not isinstance(arm, Mapping):
            continue
        suite = arm.get("suite")
        seed = arm.get("training_seed")
        if isinstance(suite, str) and isinstance(seed, int) and not isinstance(seed, bool):
            ledger_arms[(suite, seed)] = arm

    for entry, (suite, seed) in zip(results, EQUIVALENCE_ARMS):
        require_matched_fit_suite(suite)
        require_predeclared_seed(seed)
        arm = ledger_arms.get((suite, seed))
        if arm is None:
            _raise_failure(
                f"the approved ledger carries no {suite} seed {seed} arm to compare against",
                entry=entry,
                reason_class="MissingApprovedLedgerRow",
            )
        approved_path = Path(checkpoint_dir) / str(arm.get("checkpoint_name"))
        entry["rung1_reference_checkpoint_sha256"] = str(arm.get("checkpoint_sha256"))
        approved_history = arm.get("loss_history")
        entry["approved_loss_history"] = (
            [float(value) for value in approved_history]
            if isinstance(approved_history, list)
            and all(isinstance(value, (int, float)) and not isinstance(value, bool) for value in approved_history)
            else None
        )
        if not approved_path.is_file():
            _raise_failure(
                f"the approved {suite} seed {seed} checkpoint is not on disk; a fresh "
                "clone carries the ledger without the weights, and the equivalence gate "
                "cannot be made without them",
                entry=entry,
                reason_class="MissingApprovedCheckpoint",
            )
        try:
            approved_bytes = approved_path.read_bytes()
        except OSError as error:
            _raise_failure(
                f"the approved {suite} seed {seed} checkpoint could not be read "
                f"({type(error).__name__})",
                entry=entry,
                reason_class=type(error).__name__,
                cause=error,
            )
        if hashlib.sha256(approved_bytes).hexdigest() != entry[
            "rung1_reference_checkpoint_sha256"
        ]:
            _raise_failure(
                f"the approved {suite} seed {seed} checkpoint bytes do not match the "
                "digest in the approved ledger",
                entry=entry,
                reason_class="ApprovedCheckpointDigestMismatch",
            )
        try:
            approved_state = torch.load(
                io.BytesIO(approved_bytes), map_location="cpu", weights_only=True
            )
        except (OSError, RuntimeError, TypeError, ValueError) as error:
            _raise_failure(
                f"the approved {suite} seed {seed} checkpoint could not be loaded "
                f"({type(error).__name__})",
                entry=entry,
                reason_class=type(error).__name__,
                cause=error,
            )

        fits_attempted += 1
        try:
            net, history = fit_arm(
                examples_by_suite[suite],
                seed=seed,
                network_factory=build_rung1_reference_network,
                epochs=protocol.epochs,
                batch_size=protocol.batch_size,
                learning_rate=protocol.learning_rate,
                device=torch.device(protocol.device),
            )
        except Exception as error:
            _raise_failure(
                f"the factory-parameterized {suite} seed {seed} equivalence fit refused "
                f"({type(error).__name__})",
                entry=entry,
                reason_class=type(error).__name__,
                cause=error,
            )

        entry["refit_loss_history"] = [float(value) for value in history]
        produced_state = net.state_dict()
        relative = equivalence_relative_name(suite, seed)
        try:
            buffer = io.BytesIO()
            torch.save(produced_state, buffer)
            produced_bytes = buffer.getvalue()
            entry["refit_checkpoint_sha256"] = hashlib.sha256(produced_bytes).hexdigest()
            entry["refit_checkpoint_relative_name"] = relative
            (scratch_dir / equivalence_checkpoint_name(suite, seed)).write_bytes(
                produced_bytes
            )
        except (OSError, RuntimeError, TypeError, ValueError) as error:
            _raise_failure(
                f"the factory-parameterized {suite} seed {seed} checkpoint could not be "
                f"persisted ({type(error).__name__})",
                entry=entry,
                reason_class=type(error).__name__,
                cause=error,
            )
        checkpoints_written += 1
        entry["status"] = ARM_COMPLETED

        identical, reason = state_dicts_are_bit_identical(produced_state, approved_state)
        entry["weights_bit_identical"] = bool(identical)
        if not identical:
            _raise_failure(
                f"the factory-parameterized path did not reproduce the approved "
                f"{suite} seed {seed} weights: {reason}",
                entry=entry,
                reason_class="WeightsDiffer",
                completed_fit=True,
            )
        try:
            history_matches = (
                isinstance(approved_history, list)
                and len(approved_history) == len(history)
                and all(
                    float(left) == float(right)
                    for left, right in zip(approved_history, history)
                )
            )
        except (TypeError, ValueError):
            history_matches = False
        entry["loss_history_bit_identical"] = bool(history_matches)
        if not history_matches:
            _raise_failure(
                f"the factory-parameterized path did not reproduce the approved "
                f"{suite} seed {seed} per-epoch loss history",
                entry=entry,
                reason_class="LossHistoryDiffers",
                completed_fit=True,
            )
        entry["equivalence_status"] = COMPARISON_PASS

    document = _document(gate_passed=True)
    try:
        write_document(scratch_dir / EQUIVALENCE_ARTIFACT, document)
    except Exception as error:
        document["gate_passed"] = False
        document["artifact_write_reason_class"] = type(error).__name__
        raise EquivalenceFailure(
            "the equivalence comparisons passed but their artifact could not be persisted",
            document=document,
        ) from error
    return document


# ---------------------------------------------------------------------------
# Names: one definition each, because a plan may not assert more than the run binds
# ---------------------------------------------------------------------------
def logical_namespace(run_label: str) -> str:
    """Return the packet-relative, label-leading logical output namespace."""

    return f"{LOGICAL_NAMESPACE_ROOT}/{require_run_label(run_label)}"


def rung2_checkpoint_name(suite: str, seed: int) -> str:
    """Return the bare filename of one rung-2 arm's checkpoint.

    Inputs: a matched suite and a predeclared seed. Outputs: the filename, with no
    directory component. Purpose: the **one** definition of that name, so the plan's
    declared destination and the writer's actual destination cannot drift apart --
    finding AM's shape, and finding AP's one level down.
    """

    require_matched_fit_suite(suite)
    require_predeclared_seed(seed)
    return f"rung2_escalation_{suite}_seed{seed}.pt"


def equivalence_checkpoint_name(suite: str, seed: int) -> str:
    """Return the bare filename of one equivalence compatibility checkpoint."""

    require_matched_fit_suite(suite)
    require_predeclared_seed(seed)
    return f"rung2_escalation_equivalence_{suite}_seed{seed}.pt"


def equivalence_relative_name(suite: str, seed: int) -> str:
    """Return one equivalence checkpoint's name inside the reserved scratch subtree."""

    return f"{EQUIVALENCE_SUBTREE}/{equivalence_checkpoint_name(suite, seed)}"


def design_digest() -> str:
    """Return the frozen design document's canonical digest, checked against its pin."""

    path = packet_root() / "protocol" / DESIGN_DOCUMENT_NAME
    require(path.is_file(), "the frozen rung-2 escalation design is not in the packet")
    digest = canonical_text_sha256(path)
    require(
        digest == DESIGN_CANONICAL_SHA256,
        "the packet's rung-2 escalation design is not the frozen approved v0.1; an "
        "approved version is never edited in place, it is bumped and moved",
    )
    return digest


# ---------------------------------------------------------------------------
# Plan mode
# ---------------------------------------------------------------------------
def plan_document(*, run_label: str, protocol: Any) -> dict[str, object]:
    """Return the deterministic plan artifact design section 7.1 requires.

    Inputs: the predeclared run label and the resolved training protocol. Outputs: the
    plan document. Purpose: a twelve-fit action needs an aggregate identity and a
    partial-completion story before it runs, not after one arm fails.

    **No host path enters this document.** The operator supplies the base directory at
    execute time and the plan supplies the label, so two plan runs at the same
    `run_label` into different destinations produce identical bytes. That is what makes
    the plan's digest a statement about the *design of the run* rather than about the
    machine it was written on.

    The plan declares what will be **read** from the approved rung-1 records -- their
    digests and the fields the numbers will come out of -- while the values themselves
    are recorded by the run that reads them. A plan that carried the anchor numbers
    would be asserting a measurement it never made.
    """

    require_run_label(run_label)
    ledger_path = packet_root() / APPROVED_RESULT_RELATIVE
    analysis_path = packet_root() / APPROVED_ANALYSIS_RELATIVE
    ledger = read_json_document(ledger_path, "approved fit ledger")
    analysis = read_json_document(analysis_path, "approved analysis artifact")
    require_anchor_comparability(ledger, protocol)
    require_approved_analyzer_identity(analysis)
    shape = rung2_shape()
    namespace = logical_namespace(run_label)
    anchors = anchor_records(ledger, analysis)
    arms = [
        {
            "checkpoint_relative_name": f"{namespace}/{rung2_checkpoint_name(suite, seed)}",
            "n_parameters": shape["n_parameters"],
            "network_factory": build_rung2_network.__name__,
            "read_only": False,
            "rung": shape["rung"],
            "seed": seed,
            "stem_receptive_field": shape["stem_receptive_field"],
            "suite": suite,
        }
        for suite, seed in rung2_arms()
    ]
    equivalence = [
        {
            "channels": ANCHOR_CHANNELS,
            "checkpoint_relative_name": f"{namespace}/{equivalence_relative_name(suite, seed)}",
            "network_factory": build_rung1_reference_network.__name__,
            "read_only": False,
            "rung": RUNG1_NAME,
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
                "checkpoint_sha256": entry["checkpoint_sha256"],
                "macro_f1_field": entry["macro_f1_field"],
                "per_class_f1_field": entry["per_class_f1_field"],
                "read_only": True,
                "rung": entry["rung"],
                "seed": entry["seed"],
                "suite": entry["suite"],
            }
            for entry in anchors
        ],
        "approved_analysis_sha256": canonical_text_sha256(analysis_path),
        "approved_fit_ledger_sha256": canonical_text_sha256(ledger_path),
        "assignment_sha256": protocol.assignment_sha256,
        "authority": RUNG2_AUTHORITY,
        "code_identity": rung2_code_identity(),
        "config_hash": AUTHORIZED_CONFIG_HASH,
        "design_sha256": design_digest(),
        "equivalence_arms": equivalence,
        "equivalence_artifact_relative_name": (
            f"{namespace}/{EQUIVALENCE_SUBTREE}/{EQUIVALENCE_ARTIFACT}"
        ),
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
        "n_rung2_arms": len(arms),
        "plan_valid": True,
        "role_index_sha256": dict(sorted(AUTHORIZED_ROLE_INDEX_SHA256.items())),
        "run_artifact_relative_name": f"{namespace}/{RUN_ARTIFACT}",
        "run_label": run_label,
        "rung": shape["rung"],
        "rung2_arms": arms,
        "rung2_band": {
            "declared_parameters": RUNG2_DECLARED_PARAMETERS,
            "maximum_parameters": RUNG2_MAX_PARAMETERS,
            "minimum_parameters": RUNG2_MIN_PARAMETERS,
        },
        "training_protocol": protocol.as_document(),
    }


def require_authorized_plan(
    path: Path, *, expected_sha256: str, protocol: Any
) -> dict[str, Any]:
    """Authenticate the approved plan before any of its values names a path.

    Inputs: the plan file, the digest a joint authorization named, and the protocol this
    invocation resolved. Outputs: the parsed plan. Purpose: `--approved-plan-sha256`
    names a **document** and nothing else, exactly as Stage 1's gate does.

    What this gate can and cannot do is stated in design section 7 and is not widened
    here: it checks that the document is a valid plan, that it is the document the
    authorization named, and that the run it describes is the run this executable would
    build -- including invariant R12's entry-by-entry code-identity equality, which is
    therefore established **before the first fit**. It does **not** make the
    authorization single-use. A replay under the same base collides with the preserved
    run root and is refused there; a replay pointed at a different base, or run from a
    copied workspace, is outside what any local mechanism can see and is a protocol
    violation even though this gate passes.
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
    require(
        document.get("exit") == X_PLAN_OK, "the authorized plan is not a terminal plan"
    )
    require(document.get("plan_valid") is True, "the authorized plan is not valid")
    require(
        document.get("design_sha256") == design_digest(),
        "the authorized plan was written against a different design document",
    )
    require(
        document.get("code_identity") == rung2_code_identity(),
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
def write_rung2_refusal_document(
    base_dir: Path, run_label: str | None, document: Mapping[str, object]
) -> Path:
    """Persist a pre-claim or occupied-root refusal in this module's sibling sink.

    Inputs: the base, the validated label or `None`, and the refusal document. Outputs:
    the path written. Purpose: design section 6 R2 -- a refusal must never report
    through the resource whose occupancy triggered it, so the sink is a sibling of the
    run root and is named by a UUID drawn for this invocation.

    **This is a deliberate copy of `capacity_sweep.write_refusal_document`**, differing
    only in which module constant names the sink directory, because that function takes
    no sink parameter and the approved module may not be edited to add one (design
    decision D4). Invariant R9 pins the copy: a test drives both writers with one fixed
    valid `attempt_uuid`, asserts the JSON payloads are exactly equal, and asserts the
    written paths differ only in the sink-directory component. If this body drifts from
    the approved one in any way that changes a payload, that test goes red.
    """

    if run_label is not None:
        require_run_label(run_label)
    directory = Path(base_dir) / REFUSAL_SINK_NAME / (run_label or UNBOUND_LABEL_DIRECTORY)
    directory.mkdir(parents=True, exist_ok=True)
    payload = dict(document)
    candidate = payload.get("attempt_uuid")
    if not isinstance(candidate, str) or re.fullmatch(
        r"[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}",
        candidate,
    ) is None:
        candidate = str(uuid.uuid4())
    for _ in range(8):
        payload["attempt_uuid"] = candidate
        path = directory / f"{candidate}.json"
        text = canonical_json(payload)
        try:
            with path.open("x", encoding="utf-8", newline="\n") as handle:
                handle.write(text)
        except FileExistsError:
            candidate = str(uuid.uuid4())
            continue
        return path
    raise Rung2EscalationError("a unique refusal artifact name could not be drawn")


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

    Design section 6 R2: it records the exit, the reason class, the approved-plan digest
    and `run_label` when those are already validated and `null` when they are not, zero
    resource counts (invariant R8), and the elapsed time. It records neither the
    exception message nor a filesystem path, following the trainer's established rule.
    """

    return {
        "approved_plan_sha256": approved_plan_sha256,
        "attempt_uuid": attempt_uuid,
        "authority": RUNG2_AUTHORITY,
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


# ---------------------------------------------------------------------------
# The derived read of design section 5 -- pure, defined once, mostly not called here
# ---------------------------------------------------------------------------
def arm_objective_reduced(loss_history: Sequence[Any]) -> bool:
    """Return design section 5.1's per-arm objective-reduction flag.

    Inputs: one arm's per-epoch mean total objective. Outputs: `True` iff **every**
    recorded epoch loss is finite and the final epoch's value is **strictly** less than
    the first epoch's.

    It is weak on purpose. It asks only whether the implementation lowered the declared
    combined training objective, which is exactly what bound 5 permits a development fit
    to show, and it asks nothing about how well. The objective contains a severity
    Gaussian-NLL term whose log-scale can drive a reduction without improving
    classification, so this is **not** a learning signal, a classification criterion, a
    comparison, or a performance bar. A history of fewer than two epochs cannot exhibit
    a reduction and is `False`.
    """

    values: list[float] = []
    for value in loss_history:
        if isinstance(value, bool) or not isinstance(value, (int, float)):
            return False
        if not np.isfinite(float(value)):
            return False
        values.append(float(value))
    if len(values) < 2:
        return False
    return values[-1] < values[0]


def optimization_check_passed(document: Mapping[str, Any]) -> bool:
    """Return design section 5.1's run-level status as a boolean.

    Inputs: a terminal run document. Outputs: `True` iff both equivalence arms are
    `PASS`, exactly ten rung-2 arms are `COMPLETED`, and all ten are
    `OBJECTIVE_REDUCED`.

    **This executable never calls it.** It is defined here so the read-only analyzer
    invariant R7 requires imports the criterion rather than writing a second definition
    of it, exactly as Stage 1's descriptive read lives beside its executable. The
    analyzer derives this status first and suppresses every paired sign and
    rung-comparison field unless it is true (invariant R10).
    """

    equivalence = document.get("equivalence_arms")
    arms = document.get("rung2_arms")
    if not isinstance(equivalence, list) or not isinstance(arms, list):
        return False
    if len(equivalence) != len(EQUIVALENCE_ARMS):
        return False
    if not all(
        isinstance(arm, Mapping) and arm.get("equivalence_status") == COMPARISON_PASS
        for arm in equivalence
    ):
        return False
    completed = [
        arm
        for arm in arms
        if isinstance(arm, Mapping) and arm.get("status") == ARM_COMPLETED
    ]
    if len(completed) != len(rung2_arms()):
        return False
    return all(arm.get("objective_reduced") is True for arm in completed)


def optimization_check_status(document: Mapping[str, Any]) -> str:
    """Return design section 5.1's run-level status as the string it is named by.

    Inputs: a terminal run document. Outputs: `OPTIMIZATION_CHECK_PASSED` or
    `OPTIMIZATION_CHECK_FAILED`. Purpose: the analyzer persists the status as a name,
    and the name and the predicate must have one definition between them -- this is the
    predicate, rendered. **This executable never calls it**; section 5.4's status table
    is applied jointly after the analyzer has run and both agents have reviewed the
    exact terminal artifact.
    """

    if optimization_check_passed(document):
        return OPTIMIZATION_CHECK_PASSED
    return OPTIMIZATION_CHECK_FAILED


def deficit_sign_label(paired_differences: Sequence[float]) -> str:
    """Return design section 5.2's three-valued label over the paired signs.

    Inputs: the per-seed `S - C1` paired macro-F1 differences at rung 2. Outputs:
    `REPRODUCED_IN_SIGN` when S is below C1 at every seed, `NOT_REPRODUCED_IN_SIGN`
    when S is at or above C1 at every seed, and `MIXED` otherwise.

    Classification is performed at the declared six-decimal quantization, so a tie is a
    tie at the declared resolution rather than at float64's. **This is a description of
    five signs, not a test**, and no branch of it authorizes anything -- not a threshold,
    not a capacity choice, not a sentence about C1 versus S beyond the one row design
    section 5.4 licenses.

    **This executable never calls it**; it exists so the analyzer has one definition of
    the label the pre-registered read turns on.
    """

    if not paired_differences:
        raise Rung2EscalationError(
            "the paired sign label needs at least one seed difference"
        )
    quantized = [Decimal(quantize(value)) for value in paired_differences]
    zero = Decimal(0)
    if all(value < zero for value in quantized):
        return SIGN_REPRODUCED
    if all(value >= zero for value in quantized):
        return SIGN_NOT_REPRODUCED
    return SIGN_MIXED


def require_complete_rung2_run(document: Mapping[str, Any]) -> None:
    """Refuse to read a rung out of a partial run.

    Invariant R10's first half, stated once here so the read-only analyzer imports it
    rather than restating it: all ten rung-2 arm identities must be present exactly once
    and `COMPLETED`, and both equivalence arms must be present exactly once, `COMPLETED`
    and `PASS`. The objective-reduction status is deliberately **not** part of this
    check: an arm that completed without reducing its objective is a recorded finding
    about the architecture-plus-protocol pair (design section 5.4's third status row),
    not an incomplete run.
    """

    arms = document.get("rung2_arms")
    require(isinstance(arms, list), "the run artifact carries no rung-2 arms list")
    require(
        all(isinstance(arm, Mapping) for arm in arms),
        "the run artifact carries a non-object rung-2 arm",
    )

    def _identity(arm: Mapping[str, Any], label: str) -> tuple[str, int]:
        suite = arm.get("suite")
        seed = arm.get("seed")
        require(
            isinstance(suite, str)
            and isinstance(seed, int)
            and not isinstance(seed, bool),
            f"a {label} arm carries a malformed identity",
        )
        return (str(suite), int(seed))

    completed = [arm for arm in arms if arm.get("status") == ARM_COMPLETED]
    require(
        len(completed) == len(arms),
        "the run artifact carries a rung-2 arm that is not completed",
    )
    actual = [_identity(arm, "rung-2") for arm in completed]
    expected = set(rung2_arms())
    # The middle conjunct is IMPLIED by the other two and is kept deliberately. Measured
    # in the Session-115 mutation sweep: deleting it changed no test, because a list of
    # `len(expected)` items whose set equals `expected` cannot contain a duplicate. It is
    # retained for parity with the approved `capacity_sweep.require_complete_sweep`, whose
    # shape finding T bought, and so that weakening either neighbour does not silently
    # take multiset equality with it. Recorded here rather than left for a later session
    # to rediscover as a gap.
    require(
        len(actual) == len(expected)
        and len(set(actual)) == len(actual)
        and set(actual) == expected,
        f"a complete run completes exactly the {len(expected)} rung-2 arm identities",
    )

    equivalence = document.get("equivalence_arms")
    require(
        isinstance(equivalence, list)
        and all(isinstance(arm, Mapping) for arm in equivalence),
        "the run artifact carries no valid equivalence arms list",
    )
    actual_equivalence = [_identity(arm, "equivalence") for arm in equivalence]
    expected_equivalence = set(EQUIVALENCE_ARMS)
    require(
        len(actual_equivalence) == len(expected_equivalence)
        and len(set(actual_equivalence)) == len(actual_equivalence)
        and set(actual_equivalence) == expected_equivalence,
        f"a complete run records exactly {len(EQUIVALENCE_ARMS)} equivalence-arm "
        "identities",
    )
    require(
        all(
            arm.get("status") == ARM_COMPLETED
            and arm.get("equivalence_status") == COMPARISON_PASS
            for arm in equivalence
        ),
        "a complete run requires both equivalence arms to complete and to pass",
    )


# ---------------------------------------------------------------------------
# The command line and the terminal exits
# ---------------------------------------------------------------------------
def parse_args(argv: Sequence[str] | None = None) -> argparse.Namespace:
    """Parse the executable's command line. Every machine-specific input is required.

    There is deliberately **no architecture flag, no band flag, and no epochs /
    batch-size / learning-rate / device flag.** Design section 4.1 holds the
    optimization protocol exactly fixed and lets the architecture and nothing else vary;
    a command-line override would move that decision to invocation time, which is the
    shape the approved trainer's missing `--window-origin-step` was removed for.
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
    lead being the split's own diagnostic probe offset -- exactly as the approved
    trainer derives it, from the same document checked against the same digest. There is
    no command-line way to supply it.
    """

    schedule_by_trajectory, assignment_digest = trainer.authorized_window_schedule()
    return trainer.TrainingProtocol(
        schedule=tuple(
            schedule_by_trajectory[key] for key in sorted(schedule_by_trajectory)
        ),
        assignment_sha256=assignment_digest,
        window_steps=trainer.DEVELOPMENT_WINDOW_STEPS,
        control_dt_s=trainer.DEVELOPMENT_CONTROL_DT_S,
        epochs=RUNG2_EPOCHS,
        batch_size=RUNG2_BATCH_SIZE,
        learning_rate=RUNG2_LEARNING_RATE,
        device=RUNG2_DEVICE,
    ).validate()


def load_dev_examples(data_root: Path) -> tuple[dict[str, list[Any]], dict[str, Any]]:
    """Load the authorized dev examples once per suite, for every arm.

    Inputs: the delivered data root. Outputs: `{suite: examples}` and the census the run
    artifact records. Purpose: the window policy does not depend on the architecture, so
    the same 152 examples per suite serve every arm; loading them once is the only
    saving this executable takes, and it is a saving that cannot change a number.

    Every bound the approved trainer applies is applied here through the same approved
    call -- the authorized root name, manifest digest and config identity,
    `select_dev_rows`, the matched trajectory census, and `require_dev_only` at the point
    of consumption. **Nothing here can reach a pilot, validation or test row.**
    """

    return approved_analysis.load_authorized_examples(Path(data_root))


def rung2_arm_document(
    *,
    suite: str,
    seed: int,
    shape: Mapping[str, Any],
    checkpoint_name: str,
    checkpoint_sha256: str,
    metrics: Mapping[str, Any],
    fit_code_identity: Mapping[str, str],
    loss_history: Sequence[float],
    n_examples: int,
) -> dict[str, Any]:
    """Return one completed rung-2 arm's persisted record (design section 5.2)."""

    history = [float(value) for value in loss_history]
    if not history:
        raise Rung2EscalationError("a completed arm must carry a loss history")
    return {
        "accuracy": metrics["accuracy"],
        "checkpoint_relative_name": checkpoint_name,
        "checkpoint_sha256": checkpoint_sha256,
        "final_epoch_loss": history[-1],
        "first_epoch_loss": history[0],
        "fit_code_identity": dict(sorted(dict(fit_code_identity).items())),
        "loss_history": history,
        "macro_f1": metrics["macro_f1"],
        "n_examples": n_examples,
        "n_parameters": shape["n_parameters"],
        "objective_reduced": arm_objective_reduced(history),
        "per_class_f1": dict(sorted(dict(metrics["per_class_f1"]).items())),
        "rung": shape["rung"],
        "seed": seed,
        "source": "rung2-escalation",
        "status": ARM_COMPLETED,
        "stem_receptive_field": shape["stem_receptive_field"],
        "suite": suite,
    }


def run_document(
    *,
    exit_name: str,
    reason_class: str | None,
    run_label: str,
    approved_plan_sha256: str,
    code_identity_map: Mapping[str, str],
    protocol: Any,
    anchors: Sequence[Mapping[str, Any]],
    arms: Sequence[Mapping[str, Any]],
    equivalence: Sequence[Mapping[str, Any]],
    equivalence_fits_attempted: int,
    equivalence_checkpoints_written: int,
    rung2_fits_attempted: int,
    rung2_checkpoints_written: int,
    approved_analysis_sha256: str | None,
    approved_fit_ledger_sha256: str | None,
    census: Mapping[str, Any] | None,
    elapsed_s: float,
) -> dict[str, object]:
    """Return the run-level terminal document design section 7.2 requires.

    It is written on **every** terminal path after the atomic claim succeeds, records
    the consumed plan digest and label so separately authorized runs are distinguishable
    in the preserved artifacts, gives every arm exactly one status, separates equivalence
    fits from rung-2 fits in the counts, carries invariant R8's zero resource counts, and
    carries the exit name and elapsed time. A refusal's `reason_class` is recorded; its
    message never is, and no absolute filesystem path enters it (section 5.3).
    """

    fits_attempted = equivalence_fits_attempted + rung2_fits_attempted
    checkpoints_written = equivalence_checkpoints_written + rung2_checkpoints_written
    return {
        "anchor_arms": [dict(entry) for entry in anchors],
        "approved_analysis_sha256": approved_analysis_sha256,
        "approved_fit_ledger_sha256": approved_fit_ledger_sha256,
        "approved_plan_sha256": approved_plan_sha256,
        "authority": RUNG2_AUTHORITY,
        "checkpoints_written": checkpoints_written,
        "code_identity": dict(sorted(dict(code_identity_map).items())),
        "data_census": dict(census) if census is not None else None,
        "design_sha256": DESIGN_CANONICAL_SHA256,
        "elapsed_s": elapsed_s,
        "equivalence_arms": [dict(entry) for entry in equivalence],
        "equivalence_checkpoints_written": equivalence_checkpoints_written,
        "equivalence_fits_attempted": equivalence_fits_attempted,
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
        "rung": RUNG2_NAME,
        "rung2_arms": [dict(entry) for entry in arms],
        "rung2_checkpoints_written": rung2_checkpoints_written,
        "rung2_fits_attempted": rung2_fits_attempted,
        "training_protocol": protocol.as_document(),
    }


def zero_resource_line() -> str:
    """Return invariant R8's stdout statement for the two exits that persist nothing.

    Design section 6 requires the missing-destination and `X_FORBIDDEN_BASE` boundaries
    to print the named refusal **and** zero resource counts, because those are the two
    exits where no artifact can carry them.
    """

    return (
        "0 fits attempted, 0 checkpoints written, 0 rollouts spent, "
        "0 generation runs, 0 non-development reads"
    )


def _plan_mode(args: argparse.Namespace) -> int:
    """Run plan mode: zero fits, zero payload reads, byte-deterministic output."""

    output_dir = args.output_dir
    if output_dir is None:
        print(f"{X_CONTRACT_REFUSED}: --mode plan requires --output-dir")
        print(zero_resource_line())
        return EXIT_CODES[X_CONTRACT_REFUSED]
    output_dir = Path(output_dir)

    # Invariant R1, before plan mode's first write. The same guard execute mode applies
    # to `--base-dir`: R1 constrains the executable, not one of its modes, and plan
    # mode's refusal branch would otherwise deposit a document in the protected tree.
    try:
        output_dir = require_permitted_base(output_dir)
    except ForbiddenBase as error:
        print(f"{X_FORBIDDEN_BASE}: {error} (no artifact written, by construction)")
        print(zero_resource_line())
        return EXIT_CODES[X_FORBIDDEN_BASE]

    try:
        require(args.run_label is not None, "--mode plan requires --run-label")
        protocol = resolve_protocol()
        document = plan_document(run_label=args.run_label, protocol=protocol)
    except (DevFitContractError, CapacitySweepError) as error:
        refusal = {
            "authority": RUNG2_AUTHORITY,
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
        f"{X_PLAN_OK}: {document['n_rung2_arms']} rung-2 arms + "
        f"{document['n_equivalence_arms']} equivalence arms planned at run label "
        f"{document['run_label']}, 0 fits run"
    )
    return EXIT_CODES[X_PLAN_OK]


def _execute_mode(args: argparse.Namespace) -> int:
    """Run execute mode: claim the root, measure the seam, then fit the ten arms."""

    started = time.monotonic()
    attempt_uuid = str(uuid.uuid4())
    if args.base_dir is None:
        print(f"{X_CONTRACT_REFUSED}: --mode execute requires --base-dir")
        print(zero_resource_line())
        return EXIT_CODES[X_CONTRACT_REFUSED]

    # Invariant R1, before any write of any kind. See `require_permitted_base`: this is
    # the one supplied-destination terminal that persists nothing, because every sink
    # this module has is under the supplied base.
    try:
        base_dir = require_permitted_base(args.base_dir)
    except ForbiddenBase as error:
        print(f"{X_FORBIDDEN_BASE}: {error} (no artifact written, by construction)")
        print(zero_resource_line())
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
        write_rung2_refusal_document(
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
        write_rung2_refusal_document(
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
        write_rung2_refusal_document(
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

    # From here every terminal path writes the run-level document inside the claimed
    # root. Start with the complete arm identity sets so a refusal never makes downstream
    # arms disappear. Records are replaced in place as work completes or refuses.
    arms = initial_rung2_arm_records()
    equivalence = initial_equivalence_arm_records()
    anchors: list[dict[str, Any]] = []
    arm_index = {(arm["suite"], arm["seed"]): index for index, arm in enumerate(arms)}
    equivalence_index = {
        (arm["suite"], arm["seed"]): index for index, arm in enumerate(equivalence)
    }
    fit_code_identity = dict(sorted(dict(plan["code_identity"]).items()))
    equivalence_fits_attempted = 0
    equivalence_checkpoints_written = 0
    rung2_fits_attempted = 0
    rung2_checkpoints_written = 0
    approved_analysis_sha256: str | None = None
    approved_fit_ledger_sha256: str | None = None
    census: dict[str, Any] | None = None

    def _replace_arm(entry: Mapping[str, Any]) -> None:
        arms[arm_index[(entry.get("suite"), entry.get("seed"))]] = dict(entry)

    def _replace_equivalence(entry: Mapping[str, Any]) -> None:
        equivalence[equivalence_index[(entry.get("suite"), entry.get("seed"))]] = dict(
            entry
        )

    def _terminal(exit_name: str, reason_class: str | None) -> int:
        document = run_document(
            exit_name=exit_name,
            reason_class=reason_class,
            run_label=run_label,
            approved_plan_sha256=plan_digest,
            code_identity_map=fit_code_identity,
            protocol=protocol,
            anchors=anchors,
            arms=arms,
            equivalence=equivalence,
            equivalence_fits_attempted=equivalence_fits_attempted,
            equivalence_checkpoints_written=equivalence_checkpoints_written,
            rung2_fits_attempted=rung2_fits_attempted,
            rung2_checkpoints_written=rung2_checkpoints_written,
            approved_analysis_sha256=approved_analysis_sha256,
            approved_fit_ledger_sha256=approved_fit_ledger_sha256,
            census=census,
            elapsed_s=time.monotonic() - started,
        )
        write_document(run_root / RUN_ARTIFACT, document)
        return EXIT_CODES[exit_name]

    try:
        shape = rung2_shape()
        ledger_path = packet_root() / APPROVED_RESULT_RELATIVE
        analysis_path = packet_root() / APPROVED_ANALYSIS_RELATIVE
        ledger = read_json_document(ledger_path, "approved fit ledger")
        analysis = read_json_document(analysis_path, "approved analysis artifact")
        require_anchor_comparability(ledger, protocol)
        require_approved_analyzer_identity(analysis)
        anchors = anchor_records(ledger, analysis)
        approved_analysis_sha256 = canonical_text_sha256(analysis_path)
        approved_fit_ledger_sha256 = canonical_text_sha256(ledger_path)
        examples, census = load_dev_examples(args.data_root)
    except DevFitContractError as error:
        print(f"{X_CONTRACT_REFUSED}: {error}")
        return _terminal(X_CONTRACT_REFUSED, type(error).__name__)
    except (
        CapacitySweepError,
        DevFitDataError,
        approved_analysis.DevFitAnalysisError,
    ) as error:
        print(f"{X_DATA_MISSING}: {error}")
        return _terminal(X_DATA_MISSING, type(error).__name__)

    try:
        gate = equivalence_gate(
            examples_by_suite=examples,
            ledger=ledger,
            checkpoint_dir=packet_root() / APPROVED_CHECKPOINT_RELATIVE,
            scratch_dir=run_root / EQUIVALENCE_SUBTREE,
            protocol=protocol,
            fit_code_identity=fit_code_identity,
        )
        for entry in gate["arms"]:
            _replace_equivalence(entry)
        equivalence_fits_attempted = int(gate["fits_attempted"])
        equivalence_checkpoints_written = int(gate["checkpoints_written"])
    except EquivalenceFailure as error:
        for entry in error.document.get("arms", []):
            _replace_equivalence(entry)
        equivalence_fits_attempted = int(error.document.get("fits_attempted", 0))
        equivalence_checkpoints_written = int(
            error.document.get("checkpoints_written", 0)
        )
        print(f"{X_EQUIVALENCE_FAILED}: {error}")
        return _terminal(X_EQUIVALENCE_FAILED, type(error).__name__)
    except (DevFitContractError, DevFitDataError, CapacitySweepError) as error:
        print(f"{X_EQUIVALENCE_FAILED}: {error}")
        return _terminal(X_EQUIVALENCE_FAILED, type(error).__name__)

    device = torch.device(protocol.device)
    for suite, seed in rung2_arms():
        rung2_fits_attempted += 1
        try:
            net, history = fit_arm(
                examples[suite],
                seed=seed,
                network_factory=build_rung2_network,
                epochs=protocol.epochs,
                batch_size=protocol.batch_size,
                learning_rate=protocol.learning_rate,
                device=device,
            )
            metrics = score_arm(net, examples[suite])
        except DevFitContractError as error:
            _replace_arm(
                {
                    "reason_class": type(error).__name__,
                    "rung": RUNG2_NAME,
                    "seed": seed,
                    "status": ARM_REFUSED,
                    "suite": suite,
                }
            )
            print(f"{X_CONTRACT_REFUSED}: {error}")
            return _terminal(X_CONTRACT_REFUSED, type(error).__name__)
        except (DevFitDataError, RuntimeError) as error:
            _replace_arm(
                {
                    "reason_class": type(error).__name__,
                    "rung": RUNG2_NAME,
                    "seed": seed,
                    "status": ARM_REFUSED,
                    "suite": suite,
                }
            )
            print(f"{X_DATA_MISSING}: {error}")
            return _terminal(X_DATA_MISSING, type(error).__name__)
        try:
            buffer = io.BytesIO()
            torch.save(net.state_dict(), buffer)
            payload = buffer.getvalue()
            relative = rung2_checkpoint_name(suite, seed)
            (run_root / relative).parent.mkdir(parents=True, exist_ok=True)
            (run_root / relative).write_bytes(payload)
        except (OSError, RuntimeError, TypeError, ValueError) as error:
            _replace_arm(
                {
                    "reason_class": type(error).__name__,
                    "rung": RUNG2_NAME,
                    "seed": seed,
                    "status": ARM_REFUSED,
                    "suite": suite,
                }
            )
            print(f"{X_DATA_MISSING}: {error}")
            return _terminal(X_DATA_MISSING, type(error).__name__)
        rung2_checkpoints_written += 1
        checkpoint_sha256 = hashlib.sha256(payload).hexdigest()
        try:
            completed = rung2_arm_document(
                suite=suite,
                seed=seed,
                shape=shape,
                checkpoint_name=relative,
                checkpoint_sha256=checkpoint_sha256,
                metrics=metrics,
                fit_code_identity=fit_code_identity,
                loss_history=history,
                n_examples=len(examples[suite]),
            )
        except (KeyError, TypeError, ValueError, IndexError, Rung2EscalationError) as error:
            _replace_arm(
                {
                    "checkpoint_relative_name": relative,
                    "checkpoint_sha256": checkpoint_sha256,
                    "fit_code_identity": fit_code_identity,
                    "reason_class": type(error).__name__,
                    "rung": RUNG2_NAME,
                    "seed": seed,
                    "status": ARM_REFUSED,
                    "suite": suite,
                }
            )
            print(f"{X_DATA_MISSING}: {error}")
            return _terminal(X_DATA_MISSING, type(error).__name__)
        _replace_arm(completed)
        print(
            f"fitted rung 2 {suite} seed {seed}: "
            f"macro-F1 {metrics['macro_f1']:.6f}, final loss {history[-1]:.6f}"
        )

    try:
        require_complete_rung2_run({"rung2_arms": arms, "equivalence_arms": equivalence})
    except DevFitContractError as error:
        print(f"{X_RUN_INCOMPLETE}: {error}")
        return _terminal(X_RUN_INCOMPLETE, type(error).__name__)

    print(
        f"{X_RUNG2_OK}: {len(rung2_arms())} rung-2 arms fitted, "
        f"{len(EQUIVALENCE_ARMS)} equivalence checks passed, "
        f"{len(anchors)} approved anchors read, 0 rollouts spent"
    )
    return _terminal(X_RUNG2_OK, None)


def main(argv: Sequence[str] | None = None) -> int:
    """Run the executable and return the exit code of the terminal exit it took."""

    args = parse_args(argv)
    if args.mode == "plan":
        return _plan_mode(args)
    return _execute_mode(args)


if __name__ == "__main__":  # pragma: no cover - exercised through main(argv)
    sys.exit(main())
