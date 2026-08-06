"""Gate-4's development-only trainer: the ten matched arms, and what each one records.

This is the executable that turns the closed dev-fit contract
(`utils.dev_fit_contract`) into fitted rung-1 weights. It exists as its own module,
separate from both the contract and the network, because it is the only place in Gate 4
where a bound can be violated by *doing* something rather than by describing it wrongly.

What this module may do, and what it may not
--------------------------------------------
It may read the `dev` rows of the delivered base dataset, fit `TemporalAttributionNet`
once per `(suite, seed)` arm of `matched_fit_plan()`, and write one checkpoint plus one
`DevFitProvenance` record per arm. It may not read a pilot, validation or test outcome,
may not generate a rollout, may not set a threshold, and may not report a comparison over
an incomplete plan. Each of those is enforced by a call into the contract module rather
than by this file's own opinion: `select_dev_rows` and `require_dev_only` for the role
bound, `require_predeclared_seed` and `matched_fit_plan` for the seed bound,
`require_complete_matched_plan` before any comparison is reported, and
`DevFitProvenance.validate()` for what a checkpoint must be able to say.

**Nothing here is authorized to run yet.** Codex's Session-77 sequencing is: the contract
loop closes, then this executable gets its own review, and only then may a development
fit be invoked. Building it is not permission to run it.

Why every exit writes an artifact
---------------------------------
The exit paths of a program are the region no unit test enters (Session 65), and this
project has been bitten there four times. Every terminal exit below therefore has a name,
writes a result document, and has a test that *drives that exit and reads what it wrote*.

Why a refusal's message is never persisted
------------------------------------------
A `DevFitContractError` message can quote a caller-supplied string — a suite label, a
plan entry — and requirement (z) forbids a result artifact from recording an absolute
filesystem path. The payload-boundary extension spent Sessions 66 through 70 building a
scrubber for exactly that, and the accept side of a scrubber is where damage is invisible.
So this trainer does not scrub: it **never persists a refusal message at all**. The
artifact records which contract check refused and the exception class; the message itself
goes to stdout, for the operator, and nowhere else.

Two inputs are deliberately required rather than defaulted
----------------------------------------------------------
`--window-origin-step` has no default. The window origin is a pre-registration-adjacent
decision (limitation 17: nothing in the codebase fixes it, so whatever the pipeline uses
*is* its pre-registration, and Gate 7 must reuse it). A default here would quietly make
that decision inside a development script. `--data-root` has no default for the same
reason every script in this packet requires it: a script that silently runs against the
wrong path is a reproducibility failure.
"""

from __future__ import annotations

import argparse
import dataclasses
import json
import sys
from dataclasses import dataclass, field
from pathlib import Path
from typing import Sequence

import numpy as np
import torch
from torch import nn

from .attribution_net import (
    TemporalAttributionNet,
    deterministic_conv_precision,
    window_to_input,
)
from .dev_fit_contract import (
    DEVELOPMENT_ONLY_AUTHORITY,
    DevFitContractError,
    DevFitProvenance,
    DevRowCensus,
    code_identity,
    matched_fit_plan,
    require_complete_matched_plan,
    require_dev_only,
    require_predeclared_seed,
    select_dev_rows,
)
from .estimator import SOURCE_CLASS_ORDER, WindowFeatureExtractor
from .protocol_p import canonical_json
from .schema_types import ObservedRecord
from .storage_contract import IdentityManifestRow, file_sha256

# Every terminal exit of `main()`. A name rather than a bare integer, because the
# artifact records which exit was taken and a reader should not have to map numbers.
X_PLAN_OK = "X_PLAN_OK"
X_FIT_OK = "X_FIT_OK"
X_CONTRACT_REFUSED = "X_CONTRACT_REFUSED"
X_DATA_MISSING = "X_DATA_MISSING"
X_PLAN_INCOMPLETE = "X_PLAN_INCOMPLETE"

EXIT_CODES: dict[str, int] = {
    X_PLAN_OK: 0,
    X_FIT_OK: 0,
    X_CONTRACT_REFUSED: 3,
    X_DATA_MISSING: 4,
    X_PLAN_INCOMPLETE: 5,
}

# `location_out` is a joint index or -1; the head's index 0 is "not localized"
# (`attribution_net.NOT_LOCALIZED_INDEX`), so a joint index j occupies logit j + 1.
NOT_LOCALIZED_TARGET = 0

# The eight keys `assignment_generator` writes into `labels/{run_id}.npz`, as 0-d arrays.
LABEL_KEYS = (
    "source_class",
    "subtype",
    "location",
    "severity",
    "onset_index",
    "onset_time_s",
    "compound_flag",
    "ood_flag",
)


class DevFitDataError(RuntimeError):
    """A row named by the manifest could not be assembled into a training example."""


@dataclass(frozen=True)
class TrainingExample:
    """One window and its four targets, already reduced to arrays the network reads."""

    run_id: str
    values: np.ndarray  # [W, D]
    valid: np.ndarray  # [W, D]
    class_index: int
    location_index: int
    severity: float
    ood_flag: bool


@dataclass
class ArmResult:
    """What one `(suite, seed)` arm produced, or why it did not produce it."""

    suite: str
    seed: int
    n_examples: int
    final_loss: float
    checkpoint_name: str
    checkpoint_sha256: str
    provenance: DevFitProvenance
    loss_history: list[float] = field(default_factory=list)


def window_record(record: ObservedRecord, origin: int, window_steps: int) -> ObservedRecord:
    """Return a copy of `record` carrying only steps `[origin, origin + window_steps)`.

    Inputs: a full observed trace, the first step of the window, and the window length.
    Outputs: a new `ObservedRecord` whose every per-step array is that slice.
    Purpose: `WindowFeatureExtractor.window_tensor` refuses a record longer than `W`
    (`estimator.py`), which makes the window origin the caller's to own. Slicing the
    record and handing it to the existing extractor keeps the registry ORDER defined in
    exactly one place; building the `[W, D]` array here instead would be a second copy of
    that rule, and a second copy is what two guards drifting apart is made of.

    Fails loudly when the window does not fit: a short tail silently right-aligned into a
    zero-padded window is a training example that looks like data and is not.
    """

    if origin < 0:
        raise DevFitDataError(f"window origin must be non-negative, got {origin}")
    if window_steps <= 0:
        raise DevFitDataError(f"window_steps must be positive, got {window_steps}")
    end = origin + window_steps
    if end > record.n_steps:
        raise DevFitDataError(
            f"window [{origin}, {end}) does not fit run {record.run_id} "
            f"of {record.n_steps} steps"
        )
    sliced: dict[str, dict[str, np.ndarray]] = {}
    for name in (
        "values",
        "valid_mask",
        "measurement_time_s",
        "availability_time_s",
        "latency_age_s",
    ):
        source = getattr(record, name)
        sliced[name] = {channel: array[origin:end] for channel, array in source.items()}
    return dataclasses.replace(record, **sliced)


def load_label(labels_dir: Path, run_id: str) -> dict[str, object]:
    """Return the eight-key label payload for `run_id` as plain Python scalars.

    Inputs: the dataset's `labels/` directory and a run id. Outputs: a dict over
    `LABEL_KEYS`. Purpose: the label role is stored as 0-d arrays, and reading them as
    arrays into a target tensor is how a shape error becomes a silently broadcast batch.
    """

    path = labels_dir / f"{run_id}.npz"
    if not path.is_file():
        raise DevFitDataError(f"no label payload for run {run_id}")
    with np.load(path, allow_pickle=False) as payload:
        missing = [key for key in LABEL_KEYS if key not in payload]
        if missing:
            raise DevFitDataError(f"label payload for run {run_id} is missing {missing}")
        return {key: payload[key].item() for key in LABEL_KEYS}


def build_example(
    record: ObservedRecord,
    label: dict[str, object],
    *,
    extractor: WindowFeatureExtractor,
    origin: int,
) -> TrainingExample:
    """Reduce one observed record and its label to a `TrainingExample`.

    Inputs: a full observed trace, its label payload, the shared extractor, and the
    window origin. Outputs: one example. Purpose: this is the single place a stored row
    becomes a supervised target, so the class/location conventions are stated once.
    """

    windowed = window_record(record, origin, extractor.window_steps)
    values, valid = extractor.window_tensor(windowed)
    source_class = str(label["source_class"])
    if source_class not in SOURCE_CLASS_ORDER:
        raise DevFitDataError(
            f"run {record.run_id} carries source_class {source_class!r}, "
            f"which is not one of {list(SOURCE_CLASS_ORDER)}"
        )
    location = int(label["location"])
    if location < 0:
        location_index = NOT_LOCALIZED_TARGET
    else:
        location_index = location + 1
    return TrainingExample(
        run_id=record.run_id,
        values=values,
        valid=valid,
        class_index=SOURCE_CLASS_ORDER.index(source_class),
        location_index=location_index,
        severity=float(label["severity"]),
        ood_flag=bool(label["ood_flag"]),
    )


def load_arm_examples(
    data_root: Path,
    rows: Sequence[IdentityManifestRow],
    *,
    suite: str,
    origin: int,
    extractor: WindowFeatureExtractor,
) -> list[TrainingExample]:
    """Load every example for one arm, checking the role bound at the point of use.

    Inputs: the dataset root, the rows this arm will consume, its suite, the window
    origin and the shared extractor. Outputs: the arm's examples.
    Purpose: bound 1 checked where the rows are *consumed*, not only where they were
    selected — a caller can build a row list itself, and that is the path no filter
    guards. `require_dev_only` is therefore called here, with the arm's own suite, so a
    nominal C1 fit cannot consume S rows while every row still truthfully says `dev`.
    """

    require_dev_only(rows, suite=suite)
    observations_dir = Path(data_root) / "observations" / suite
    labels_dir = Path(data_root) / "labels"
    if not observations_dir.is_dir():
        raise DevFitDataError(f"no observations directory for suite {suite}")
    if not labels_dir.is_dir():
        raise DevFitDataError("no labels directory in the dataset root")
    examples: list[TrainingExample] = []
    for row in rows:
        path = observations_dir / f"{row.run_id}.npz"
        if not path.is_file():
            raise DevFitDataError(f"no observation payload for run {row.run_id}")
        record = ObservedRecord.load_npz(path)
        examples.append(
            build_example(
                record, load_label(labels_dir, row.run_id), extractor=extractor, origin=origin
            )
        )
    return examples


def _stack(examples: Sequence[TrainingExample], device: torch.device) -> dict[str, torch.Tensor]:
    """Stack examples into one batch of input and target tensors."""

    inputs = torch.cat([window_to_input(e.values, e.valid, device=device) for e in examples])
    return {
        "inputs": inputs,
        "class_index": torch.tensor([e.class_index for e in examples], device=device),
        "location_index": torch.tensor([e.location_index for e in examples], device=device),
        "severity": torch.tensor(
            [e.severity for e in examples], dtype=torch.float32, device=device
        ),
        "ood": torch.tensor(
            [float(e.ood_flag) for e in examples], dtype=torch.float32, device=device
        ),
    }


def arm_loss(heads, batch: dict[str, torch.Tensor]) -> torch.Tensor:
    """Return the development-only training loss for one forward pass.

    Inputs: the network's `AttributionHeads` and the stacked targets.
    Outputs: a scalar loss. Purpose: one place where the four heads are given their
    objectives, so a later change is one edit rather than four.

    The severity term is a Gaussian negative log-likelihood over the head's own raw
    `severity_log_scale`, which is what that head is for. It is **not** a calibrated
    uncertainty and does not become one by being trained: `severity_uncertainty` stays
    `+inf` until Gate 5, which is bound 5 and is enforced in `attribution_net`, not here.
    The four terms are equally weighted — a development-only choice, recorded rather than
    tuned, because tuning a loss weight against dev data and then reporting the winner is
    capacity selection, which bound 5 forbids.
    """

    class_loss = nn.functional.cross_entropy(heads.class_logits, batch["class_index"])
    location_loss = nn.functional.cross_entropy(heads.location_logits, batch["location_index"])
    log_scale = heads.severity_log_scale.clamp(-10.0, 10.0)
    severity_loss = (
        0.5 * (((batch["severity"] - heads.severity_value) ** 2) * torch.exp(-2.0 * log_scale))
        + log_scale
    ).mean()
    unknown_loss = nn.functional.binary_cross_entropy_with_logits(
        heads.unknown_logit, batch["ood"]
    )
    return class_loss + location_loss + severity_loss + unknown_loss


def fit_one_arm(
    examples: Sequence[TrainingExample],
    *,
    seed: int,
    epochs: int,
    batch_size: int,
    learning_rate: float,
    device: torch.device,
) -> tuple[TemporalAttributionNet, list[float]]:
    """Fit one arm and return its network and per-epoch mean loss.

    Inputs: the arm's examples, its predeclared seed, and the optimization settings.
    Outputs: the fitted network and its loss history.
    Purpose: one arm of `matched_fit_plan()`, and the only place weights change.

    `deterministic_conv_precision()` wraps the **whole** step — forward, backward and the
    optimizer update — not only the forward pass. cuDNN's TF32 default applies to the
    convolution backward kernels as well, so a context that covered inference alone would
    leave the gradients computed at a different precision than the numbers it was opened
    to protect, and a paired C1-vs-S difference would carry a backend flag inside it.
    """

    require_predeclared_seed(seed)
    if not examples:
        raise DevFitDataError("a development-only fit may not consume an empty row set")
    torch.manual_seed(seed)
    net = TemporalAttributionNet(seed=seed).to(device)
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
                loss.backward()
                optimizer.step()
                epoch_losses.append(float(loss.detach().cpu()))
            history.append(float(np.mean(epoch_losses)))
        net.eval()
    return net, history


def training_code_identity() -> dict[str, str]:
    """Return bound 4's code identity for the files that define this training protocol.

    Inputs: none. Outputs: `{bare label: canonical text digest}`.
    Purpose: bound 4 — a checkpoint names the code that produced it, not merely the data
    it read. Built with `code_identity()` rather than assembled by hand, so the mapping
    cannot be one the provenance record will refuse.
    """

    here = Path(__file__).resolve().parent
    return code_identity(
        {
            "dev_fit_trainer.py": here / "dev_fit_trainer.py",
            "dev_fit_contract.py": here / "dev_fit_contract.py",
            "attribution_net.py": here / "attribution_net.py",
        }
    )


def build_provenance(
    *,
    data_root: Path,
    manifest_sha256: str,
    config_hash: str,
    assignment_sha256: str,
    suite: str,
    seed: int,
    checkpoint_sha256: str,
    census: DevRowCensus,
) -> DevFitProvenance:
    """Assemble and validate bound 4's record for one checkpoint.

    `row_disclosure` is `census.disclosure()` and nothing else. The record accepts any
    non-empty string there, so the field is the one place a machine path could enter this
    document (Session 81, Finding G); passing the census's own sentence is what keeps that
    state unreachable, and a test pins it.
    """

    return DevFitProvenance(
        data_root_name=Path(data_root).resolve().name,
        manifest_sha256=manifest_sha256,
        config_hash=config_hash,
        assignment_sha256=assignment_sha256,
        suite=suite,
        training_seed=seed,
        checkpoint_sha256=checkpoint_sha256,
        code_identity=training_code_identity(),
        row_disclosure=census.disclosure(),
    ).validate()


def write_document(path: Path, document: dict[str, object]) -> str:
    """Write `document` as canonical JSON and return the text written."""

    path.parent.mkdir(parents=True, exist_ok=True)
    text = canonical_json(document)
    path.write_text(text, encoding="utf-8", newline="\n")
    return text


def plan_document(*, window_origin_step: int, window_steps: int) -> dict[str, object]:
    """Return the plan artifact: the ten arms this trainer is authorized to run."""

    return {
        "authority": DEVELOPMENT_ONLY_AUTHORITY,
        "exit": X_PLAN_OK,
        "arms": [{"suite": suite, "seed": seed} for suite, seed in matched_fit_plan()],
        "n_arms": len(matched_fit_plan()),
        "window_origin_step": int(window_origin_step),
        "window_steps": int(window_steps),
        "fits_run": 0,
        "rollouts_spent": 0,
    }


def parse_args(argv: Sequence[str] | None = None) -> argparse.Namespace:
    """Parse the trainer's command line. Every machine-specific input is required."""

    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument("--mode", choices=("plan", "fit"), required=True)
    parser.add_argument("--output-dir", required=True, type=Path)
    parser.add_argument("--data-root", type=Path, default=None)
    parser.add_argument("--window-origin-step", type=int, default=None)
    parser.add_argument("--window-steps", type=int, default=768)
    parser.add_argument("--epochs", type=int, default=20)
    parser.add_argument("--batch-size", type=int, default=8)
    parser.add_argument("--learning-rate", type=float, default=1e-3)
    parser.add_argument("--device", default="cpu")
    return parser.parse_args(argv)


def main(argv: Sequence[str] | None = None) -> int:
    """Run the trainer and return the exit code of the terminal exit it took.

    Every return below writes its artifact first. A refusal's *message* is printed and
    never persisted; the artifact records the exception class and the exit name only.
    """

    args = parse_args(argv)
    output_dir = Path(args.output_dir)

    if args.mode == "plan":
        document = plan_document(
            window_origin_step=(
                -1 if args.window_origin_step is None else args.window_origin_step
            ),
            window_steps=args.window_steps,
        )
        write_document(output_dir / "dev_fit_plan.json", document)
        print(f"{X_PLAN_OK}: {document['n_arms']} arms planned, 0 fits run")
        return EXIT_CODES[X_PLAN_OK]

    if args.data_root is None or args.window_origin_step is None:
        document = {
            "authority": DEVELOPMENT_ONLY_AUTHORITY,
            "exit": X_DATA_MISSING,
            "reason_class": "MissingRequiredArgument",
            "fits_run": 0,
        }
        write_document(output_dir / "dev_fit_result.json", document)
        print(f"{X_DATA_MISSING}: --mode fit requires --data-root and --window-origin-step")
        return EXIT_CODES[X_DATA_MISSING]

    data_root = Path(args.data_root)
    manifest_path = data_root / "manifest.csv"
    extractor = WindowFeatureExtractor(window_steps=args.window_steps)
    device = torch.device(args.device)
    completed: list[tuple[str, int]] = []
    results: list[ArmResult] = []

    try:
        rows, census = select_dev_rows(manifest_path)
        manifest_digest = file_sha256(manifest_path)
        for suite, seed in matched_fit_plan():
            arm_rows = [row for row in rows if row.suite == suite]
            examples = load_arm_examples(
                data_root, arm_rows, suite=suite, origin=args.window_origin_step,
                extractor=extractor,
            )
            net, history = fit_one_arm(
                examples,
                seed=seed,
                epochs=args.epochs,
                batch_size=args.batch_size,
                learning_rate=args.learning_rate,
                device=device,
            )
            checkpoint_name = f"dev_fit_{suite}_seed{seed}.pt"
            checkpoint_path = output_dir / checkpoint_name
            checkpoint_path.parent.mkdir(parents=True, exist_ok=True)
            torch.save(net.state_dict(), checkpoint_path)
            provenance = build_provenance(
                data_root=data_root,
                manifest_sha256=manifest_digest,
                config_hash=rows[0].config_hash,
                assignment_sha256=_assignment_digest(),
                suite=suite,
                seed=seed,
                checkpoint_sha256=file_sha256(checkpoint_path),
                census=census,
            )
            results.append(
                ArmResult(
                    suite=suite,
                    seed=seed,
                    n_examples=len(examples),
                    final_loss=history[-1],
                    checkpoint_name=checkpoint_name,
                    checkpoint_sha256=provenance.checkpoint_sha256,
                    provenance=provenance,
                    loss_history=history,
                )
            )
            completed.append((suite, seed))
            print(f"fitted {suite} seed {seed}: {len(examples)} examples, "
                  f"final loss {history[-1]:.6f}")
    except DevFitContractError as error:
        document = {
            "authority": DEVELOPMENT_ONLY_AUTHORITY,
            "exit": X_CONTRACT_REFUSED,
            "reason_class": type(error).__name__,
            "arms_completed": [{"suite": s, "seed": d} for s, d in completed],
            "fits_run": len(completed),
        }
        write_document(output_dir / "dev_fit_result.json", document)
        print(f"{X_CONTRACT_REFUSED}: {error}")
        return EXIT_CODES[X_CONTRACT_REFUSED]
    except DevFitDataError as error:
        document = {
            "authority": DEVELOPMENT_ONLY_AUTHORITY,
            "exit": X_DATA_MISSING,
            "reason_class": type(error).__name__,
            "arms_completed": [{"suite": s, "seed": d} for s, d in completed],
            "fits_run": len(completed),
        }
        write_document(output_dir / "dev_fit_result.json", document)
        print(f"{X_DATA_MISSING}: {error}")
        return EXIT_CODES[X_DATA_MISSING]

    try:
        require_complete_matched_plan(completed)
    except DevFitContractError as error:
        document = {
            "authority": DEVELOPMENT_ONLY_AUTHORITY,
            "exit": X_PLAN_INCOMPLETE,
            "reason_class": type(error).__name__,
            "arms_completed": [{"suite": s, "seed": d} for s, d in completed],
            "fits_run": len(completed),
        }
        write_document(output_dir / "dev_fit_result.json", document)
        print(f"{X_PLAN_INCOMPLETE}: {error}")
        return EXIT_CODES[X_PLAN_INCOMPLETE]

    document = {
        "authority": DEVELOPMENT_ONLY_AUTHORITY,
        "exit": X_FIT_OK,
        "fits_run": len(results),
        "window_origin_step": int(args.window_origin_step),
        "window_steps": int(args.window_steps),
        "arms": [json.loads(result.provenance.canonical_string()) for result in results],
        "final_losses": [
            {"suite": r.suite, "seed": r.seed, "final_loss": r.final_loss} for r in results
        ],
        "rollouts_spent": 0,
    }
    write_document(output_dir / "dev_fit_result.json", document)
    print(f"{X_FIT_OK}: {len(results)} arms fitted, 0 rollouts spent")
    return EXIT_CODES[X_FIT_OK]


def _assignment_digest() -> str:
    """Return the pinned approved assignment digest the provenance record demands."""

    from .dev_fit_contract import ASSIGNMENT_CANONICAL_SHA256

    return ASSIGNMENT_CANONICAL_SHA256


if __name__ == "__main__":  # pragma: no cover - exercised through main(argv)
    sys.exit(main())
