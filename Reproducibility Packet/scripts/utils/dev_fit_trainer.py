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

Why the development window remains fail-closed
----------------------------------------------
The delivered development split contains both an ordinary trajectory and a diagnostic
trajectory, but no jointly reviewed policy yet maps both to the causal windows this model
will consume. The 1,136 held-decision step belongs to the later bounded-contact screen;
it is not authority to apply ``[368, 1136)`` to every delivered base-dataset row. The two
authorization constants below therefore remain ``None``. Any plan or fit refuses until
the owner supplies and both agents approve the missing training-window policy.

`--data-root` remains required. The executable also pins the delivered root name,
manifest digest and development config identity before it opens any observation or label
payload. Merely recording an arbitrary manifest's digest would describe the wrong data
accurately rather than enforce the dataset this fit is authorized to read.
"""

from __future__ import annotations

import argparse
import dataclasses
import hashlib
import io
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
from .config_contract import ConfigContractError, load_config
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
    require,
    select_dev_rows,
)
from .estimator import SOURCE_CLASS_ORDER, WindowFeatureExtractor
from .protocol_p import canonical_json
from .role_contract import RolePayloadLoader
from .schema_types import ObservedRecord
from .storage_contract import (
    DeployableObservationLoader,
    IdentityManifestRow,
    StorageContractError,
    file_sha256,
)

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

# The exact delivered development partition this one authorized fit may consume. The
# manifest digest is raw-file SHA-256 because the manifest is a data artifact, not a
# line-ending-normalized tracked text document.
AUTHORIZED_DATA_ROOT_NAME = "gate3-base-dev-pilot-val-c1-s"
AUTHORIZED_MANIFEST_SHA256 = (
    "55ea5f0e74ddd24b05eafc51a2b9fc424eda99eac1901534946f42b6012ebe12"
)
AUTHORIZED_CONFIG_HASH = (
    "dev-712abf27c3f8f3c331ae9b76e3f22c48857334cc15a81e819718165e47753e56"
)
AUTHORIZED_ROLE_INDEX_SHA256 = {
    "labels/index.csv": "a7c700e53d917f2ddb256521af3c23bba6f7ec6d6f3af967d14ca9aad3a559f8",
    "observations/C1/index.csv": (
        "f0cc92bf33f7e06f8ac09e4ac0dffd86d567b445de07b049a9475b01f5dff716"
    ),
    "observations/S/index.csv": (
        "fa790f9d03b38d246c7e656164cbbee1ebe33f51c122d91edbf3dc72d526dd00"
    ),
}

# The control rate and window length come from the authorized draft config. A global
# origin/decision does not: the delivered dev role spans ordinary and diagnostic
# trajectories. Leaving these unset makes the unresolved scientific decision executable.
DEVELOPMENT_CONTROL_DT_S = 0.002
DEVELOPMENT_WINDOW_STEPS = 768
DEVELOPMENT_WINDOW_ORIGIN_STEP: int | None = None
DEVELOPMENT_DECISION_STEP: int | None = None


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


@dataclass(frozen=True)
class TrainingProtocol:
    """The runtime choices shared by all ten arms and recorded with their results."""

    window_origin_step: int
    window_steps: int
    decision_step: int
    control_dt_s: float
    epochs: int
    batch_size: int
    learning_rate: float
    device: str

    @property
    def decision_time_s(self) -> float:
        """Return the held-decision time used as the availability cutoff."""

        return float(self.decision_step * self.control_dt_s)

    def validate(self) -> "TrainingProtocol":
        """Refuse a protocol that changes the pinned causal window or is not runnable."""

        require(
            DEVELOPMENT_WINDOW_ORIGIN_STEP is not None
            and DEVELOPMENT_DECISION_STEP is not None,
            "development training-window policy has not been authorized",
        )
        require(
            self.window_origin_step == DEVELOPMENT_WINDOW_ORIGIN_STEP,
            f"development window origin must be {DEVELOPMENT_WINDOW_ORIGIN_STEP}",
        )
        require(
            self.window_steps == DEVELOPMENT_WINDOW_STEPS,
            f"development window length must be {DEVELOPMENT_WINDOW_STEPS}",
        )
        require(
            self.decision_step == DEVELOPMENT_DECISION_STEP
            and self.window_origin_step + self.window_steps == self.decision_step,
            "development window must end exactly at the held decision",
        )
        require(
            np.isfinite(self.control_dt_s)
            and self.control_dt_s == DEVELOPMENT_CONTROL_DT_S,
            f"development control_dt_s must be {DEVELOPMENT_CONTROL_DT_S}",
        )
        require(
            isinstance(self.epochs, int) and not isinstance(self.epochs, bool)
            and self.epochs > 0,
            "epochs must be a positive integer",
        )
        require(
            isinstance(self.batch_size, int) and not isinstance(self.batch_size, bool)
            and self.batch_size > 0,
            "batch_size must be a positive integer",
        )
        require(
            np.isfinite(self.learning_rate) and self.learning_rate > 0.0,
            "learning_rate must be finite and positive",
        )
        require(
            isinstance(self.device, str) and bool(self.device.strip()),
            "device must be a non-empty torch device name",
        )
        return self

    def as_document(self) -> dict[str, object]:
        """Return the canonical-JSON-serializable protocol recorded by every result."""

        self.validate()
        return {
            "batch_size": self.batch_size,
            "control_dt_s": self.control_dt_s,
            "decision_step": self.decision_step,
            "decision_time_s": self.decision_time_s,
            "device": self.device,
            "epochs": self.epochs,
            "learning_rate": self.learning_rate,
            "window_origin_step": self.window_origin_step,
            "window_steps": self.window_steps,
        }


def window_record(
    record: ObservedRecord,
    origin: int,
    window_steps: int,
    *,
    decision_time_s: float,
) -> ObservedRecord:
    """Return the causal stored-row window available at `decision_time_s`.

    Inputs: a full observed trace, the first step of the window, the window length, and
    the online held-decision time. Outputs: a new `ObservedRecord` whose every per-step
    array is that slice and whose values/validity are masked to samples delivered by the
    decision.
    Purpose: `WindowFeatureExtractor.window_tensor` refuses a record longer than `W`
    (`estimator.py`), which makes the window origin the caller's to own. Slicing the
    record and handing it to the existing extractor keeps the registry ORDER defined in
    exactly one place; building the `[W, D]` array here instead would be a second copy of
    that rule, and a second copy is what two guards drifting apart is made of.

    The persisted record intentionally retains measured values that were not yet delivered
    at an earlier decision. The online path masks them in
    `OnlineSensorSession.available_record`; training must reproduce that boundary rather
    than learn from latency-hidden future information.

    Fails loudly when the window does not fit or the decision time is invalid: a short
    tail silently right-aligned into a zero-padded window is a training example that looks
    like data and is not.
    """

    if origin < 0:
        raise DevFitDataError(f"window origin must be non-negative, got {origin}")
    if window_steps <= 0:
        raise DevFitDataError(f"window_steps must be positive, got {window_steps}")
    if not np.isfinite(decision_time_s) or decision_time_s < 0.0:
        raise DevFitDataError(
            f"decision_time_s must be finite and non-negative, got {decision_time_s}"
        )
    end = origin + window_steps
    if end > record.n_steps:
        raise DevFitDataError(
            f"window [{origin}, {end}) does not fit run {record.run_id} "
            f"of {record.n_steps} steps"
        )
    sliced: dict[str, dict[str, np.ndarray]] = {}
    for name in (
        "measurement_time_s",
        "availability_time_s",
        "latency_age_s",
    ):
        source = getattr(record, name)
        sliced[name] = {channel: array[origin:end] for channel, array in source.items()}
    sliced_values: dict[str, np.ndarray] = {}
    sliced_valid: dict[str, np.ndarray] = {}
    for channel, array in record.values.items():
        values = array[origin:end]
        availability = sliced["availability_time_s"][channel]
        delivered = np.isfinite(availability) & (
            availability <= decision_time_s + 1.0e-12
        )
        valid = record.valid_mask[channel][origin:end] & delivered[:, None]
        sliced_valid[channel] = valid
        sliced_values[channel] = np.where(valid, values, np.nan)
    sliced["values"] = sliced_values
    sliced["valid_mask"] = sliced_valid
    return dataclasses.replace(record, **sliced)


def build_example(
    record: ObservedRecord,
    label: dict[str, object],
    *,
    extractor: WindowFeatureExtractor,
    origin: int,
    decision_time_s: float,
) -> TrainingExample:
    """Reduce one observed record and its label to a `TrainingExample`.

    Inputs: a full observed trace, its label payload, the shared extractor, and the
    window origin, and its online availability cutoff. Outputs: one example. Purpose:
    this is the single place a stored row becomes a supervised target, so the causal
    window and class/location conventions are stated once.
    """

    windowed = window_record(
        record,
        origin,
        extractor.window_steps,
        decision_time_s=decision_time_s,
    )
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


def build_role_loaders(
    data_root: Path,
) -> tuple[dict[str, DeployableObservationLoader], RolePayloadLoader]:
    """Build the packet's hash-checking observation and label loaders for this dataset."""

    packet_root = Path(__file__).resolve().parents[2]
    schema_path = packet_root / "schema" / "schema.json"
    config_path = packet_root / "config" / "draft-config-v0.1.json"
    try:
        config = load_config(config_path, schema_path, require_frozen=False)
        require(
            config.config_hash == AUTHORIZED_CONFIG_HASH,
            "the trainer's draft config does not match the authorized dataset config",
        )
        for relative, expected_digest in AUTHORIZED_ROLE_INDEX_SHA256.items():
            index_path = Path(data_root).joinpath(*relative.split("/"))
            require(
                index_path.is_file() and file_sha256(index_path) == expected_digest,
                f"role index {relative!r} does not equal the authorized delivered index",
            )
        schema = json.loads(schema_path.read_text(encoding="utf-8"))
        observations = {
            suite: DeployableObservationLoader(
                Path(data_root) / "observations" / suite,
                suite,
                config,
                require_frozen=False,
            )
            for suite in ("C1", "S")
        }
        labels = RolePayloadLoader(
            Path(data_root) / "labels", "labels", schema, config
        )
    except (ConfigContractError, StorageContractError, OSError, ValueError) as error:
        raise DevFitDataError(
            f"the authorized dataset's role indexes could not be loaded "
            f"({type(error).__name__})"
        ) from error
    return observations, labels


def load_arm_examples(
    rows: Sequence[IdentityManifestRow],
    *,
    suite: str,
    origin: int,
    decision_time_s: float,
    extractor: WindowFeatureExtractor,
    observation_loader: DeployableObservationLoader,
    label_loader: RolePayloadLoader,
) -> list[TrainingExample]:
    """Load every example for one arm, checking the role bound at the point of use.

    Inputs: the rows this arm will consume, its suite, the window origin, held-decision
    time, shared extractor, and hash-checking role loaders. Outputs: the arm's examples.
    Purpose: bound 1 checked where the rows are *consumed*, not only where they were
    selected — a caller can build a row list itself, and that is the path no filter
    guards. `require_dev_only` is therefore called here, with the arm's own suite, so a
    nominal C1 fit cannot consume S rows while every row still truthfully says `dev`.
    """

    require_dev_only(rows, suite=suite)
    examples: list[TrainingExample] = []
    for row in rows:
        try:
            record = observation_loader.load(row.run_id)
            label = label_loader.load(row.run_id)
        except (KeyError, StorageContractError, OSError, ValueError) as error:
            raise DevFitDataError(
                f"indexed payload for run {row.run_id} failed "
                f"({type(error).__name__})"
            ) from error
        examples.append(
            build_example(
                record,
                label,
                extractor=extractor,
                origin=origin,
                decision_time_s=decision_time_s,
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
            "config_contract.py": here / "config_contract.py",
            "estimator.py": here / "estimator.py",
            "role_contract.py": here / "role_contract.py",
            "schema_types.py": here / "schema_types.py",
            "storage_contract.py": here / "storage_contract.py",
        }
    )


def require_authorized_dataset(
    data_root: Path,
    *,
    manifest_sha256: str,
    selected_rows: Sequence[IdentityManifestRow] | None = None,
) -> None:
    """Refuse anything except the exact delivered development partition.

    The manifest digest is checked before its rows are parsed or any payload is opened.
    Once rows exist, their config identity is checked independently so the checkpoint's
    recorded config cannot be borrowed from the first row of a mixed-config selection.
    """

    root_name = Path(data_root).resolve().name
    require(
        root_name == AUTHORIZED_DATA_ROOT_NAME,
        f"data root must be the authorized bare name {AUTHORIZED_DATA_ROOT_NAME!r}",
    )
    require(
        manifest_sha256 == AUTHORIZED_MANIFEST_SHA256,
        "manifest digest does not equal the authorized delivered manifest",
    )
    if selected_rows is not None:
        config_hashes = sorted({row.config_hash for row in selected_rows})
        require(
            config_hashes == [AUTHORIZED_CONFIG_HASH],
            "selected development rows do not all carry the authorized config identity",
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
    protocol_code_identity: dict[str, str],
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
        code_identity=protocol_code_identity,
        row_disclosure=census.disclosure(),
    ).validate()


def write_document(path: Path, document: dict[str, object]) -> str:
    """Write `document` as canonical JSON and return the text written."""

    path.parent.mkdir(parents=True, exist_ok=True)
    text = canonical_json(document)
    path.write_text(text, encoding="utf-8", newline="\n")
    return text


def arm_document(result: ArmResult, protocol: TrainingProtocol) -> dict[str, object]:
    """Return one completed arm with its checkpoint and reproducibility settings."""

    document = result.provenance.as_document()
    document.update(
        {
            "checkpoint_name": result.checkpoint_name,
            "final_loss": result.final_loss,
            "loss_history": list(result.loss_history),
            "n_examples": result.n_examples,
            "role_index_sha256": dict(sorted(AUTHORIZED_ROLE_INDEX_SHA256.items())),
            "training_protocol": protocol.as_document(),
        }
    )
    return document


def plan_document(
    *,
    protocol: TrainingProtocol,
    protocol_code_identity: dict[str, str],
) -> dict[str, object]:
    """Return the plan artifact: the ten arms this trainer is authorized to run."""

    return {
        "authority": DEVELOPMENT_ONLY_AUTHORITY,
        "exit": X_PLAN_OK,
        "arms": [{"suite": suite, "seed": seed} for suite, seed in matched_fit_plan()],
        "code_identity": protocol_code_identity,
        "n_arms": len(matched_fit_plan()),
        "authorized_role_index_sha256": dict(
            sorted(AUTHORIZED_ROLE_INDEX_SHA256.items())
        ),
        "training_protocol": protocol.as_document(),
        "fits_run": 0,
        "rollouts_spent": 0,
    }


def parse_args(argv: Sequence[str] | None = None) -> argparse.Namespace:
    """Parse the trainer's command line. Every machine-specific input is required."""

    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument("--mode", choices=("plan", "fit"), required=True)
    parser.add_argument("--output-dir", required=True, type=Path)
    parser.add_argument("--data-root", type=Path, default=None)
    parser.add_argument(
        "--window-origin-step", type=int, default=None
    )
    parser.add_argument("--window-steps", type=int, default=DEVELOPMENT_WINDOW_STEPS)
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
    if args.window_origin_step is None or (
        args.mode == "fit" and args.data_root is None
    ):
        document = {
            "authority": DEVELOPMENT_ONLY_AUTHORITY,
            "exit": X_DATA_MISSING,
            "reason_class": "MissingRequiredArgument",
            "fits_run": 0,
        }
        target = "dev_fit_plan.json" if args.mode == "plan" else "dev_fit_result.json"
        write_document(output_dir / target, document)
        print(
            f"{X_DATA_MISSING}: --window-origin-step is required"
            + (" and --mode fit requires --data-root" if args.mode == "fit" else "")
        )
        return EXIT_CODES[X_DATA_MISSING]

    protocol = TrainingProtocol(
        window_origin_step=args.window_origin_step,
        window_steps=args.window_steps,
        decision_step=args.window_origin_step + args.window_steps,
        control_dt_s=DEVELOPMENT_CONTROL_DT_S,
        epochs=args.epochs,
        batch_size=args.batch_size,
        learning_rate=args.learning_rate,
        device=args.device,
    )

    try:
        protocol.validate()
        protocol_code_identity = training_code_identity()
    except DevFitContractError as error:
        document = {
            "authority": DEVELOPMENT_ONLY_AUTHORITY,
            "exit": X_CONTRACT_REFUSED,
            "reason_class": type(error).__name__,
            "fits_run": 0,
        }
        target = "dev_fit_plan.json" if args.mode == "plan" else "dev_fit_result.json"
        write_document(output_dir / target, document)
        print(f"{X_CONTRACT_REFUSED}: {error}")
        return EXIT_CODES[X_CONTRACT_REFUSED]

    if args.mode == "plan":
        document = plan_document(
            protocol=protocol,
            protocol_code_identity=protocol_code_identity,
        )
        write_document(output_dir / "dev_fit_plan.json", document)
        print(f"{X_PLAN_OK}: {document['n_arms']} arms planned, 0 fits run")
        return EXIT_CODES[X_PLAN_OK]

    data_root = Path(args.data_root)
    manifest_path = data_root / "manifest.csv"
    completed: list[tuple[str, int]] = []
    results: list[ArmResult] = []

    try:
        if not manifest_path.is_file():
            raise DevFitDataError("the data root has no manifest.csv")
        manifest_digest = file_sha256(manifest_path)
        require_authorized_dataset(data_root, manifest_sha256=manifest_digest)
        rows, census = select_dev_rows(manifest_path)
        require_authorized_dataset(
            data_root,
            manifest_sha256=manifest_digest,
            selected_rows=rows,
        )
        observation_loaders, label_loader = build_role_loaders(data_root)
        extractor = WindowFeatureExtractor(window_steps=protocol.window_steps)
        try:
            device = torch.device(protocol.device)
        except (RuntimeError, ValueError) as error:
            raise DevFitContractError("device must be a valid torch device name") from error
        require(
            device.type in {"cpu", "cuda"},
            "device must name the cpu or cuda backend",
        )
        require(
            device.type != "cuda" or torch.cuda.is_available(),
            "a CUDA device was requested but CUDA is unavailable",
        )
        require(
            device.type != "cuda"
            or device.index is None
            or 0 <= device.index < torch.cuda.device_count(),
            "the requested CUDA device index is unavailable",
        )
        for suite, seed in matched_fit_plan():
            arm_rows = [row for row in rows if row.suite == suite]
            examples = load_arm_examples(
                arm_rows,
                suite=suite,
                origin=protocol.window_origin_step,
                decision_time_s=protocol.decision_time_s,
                extractor=extractor,
                observation_loader=observation_loaders[suite],
                label_loader=label_loader,
            )
            try:
                net, history = fit_one_arm(
                    examples,
                    seed=seed,
                    epochs=protocol.epochs,
                    batch_size=protocol.batch_size,
                    learning_rate=protocol.learning_rate,
                    device=device,
                )
            except RuntimeError as error:
                raise DevFitDataError(
                    f"training runtime failed for {suite} seed {seed} "
                    f"({type(error).__name__})"
                ) from error
            checkpoint_name = f"dev_fit_{suite}_seed{seed}.pt"
            checkpoint_path = output_dir / checkpoint_name
            checkpoint_buffer = io.BytesIO()
            try:
                torch.save(net.state_dict(), checkpoint_buffer)
            except RuntimeError as error:
                raise DevFitDataError(
                    f"checkpoint serialization failed for {suite} seed {seed} "
                    f"({type(error).__name__})"
                ) from error
            checkpoint_bytes = checkpoint_buffer.getvalue()
            checkpoint_digest = hashlib.sha256(checkpoint_bytes).hexdigest()
            provenance = build_provenance(
                data_root=data_root,
                manifest_sha256=manifest_digest,
                config_hash=AUTHORIZED_CONFIG_HASH,
                assignment_sha256=_assignment_digest(),
                suite=suite,
                seed=seed,
                checkpoint_sha256=checkpoint_digest,
                census=census,
                protocol_code_identity=protocol_code_identity,
            )
            checkpoint_path.parent.mkdir(parents=True, exist_ok=True)
            checkpoint_path.write_bytes(checkpoint_bytes)
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
            "arms": [arm_document(result, protocol) for result in results],
            "code_identity": protocol_code_identity,
            "fits_run": len(completed),
            "training_protocol": protocol.as_document(),
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
            "arms": [arm_document(result, protocol) for result in results],
            "code_identity": protocol_code_identity,
            "fits_run": len(completed),
            "training_protocol": protocol.as_document(),
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
            "arms": [arm_document(result, protocol) for result in results],
            "code_identity": protocol_code_identity,
            "fits_run": len(completed),
            "training_protocol": protocol.as_document(),
        }
        write_document(output_dir / "dev_fit_result.json", document)
        print(f"{X_PLAN_INCOMPLETE}: {error}")
        return EXIT_CODES[X_PLAN_INCOMPLETE]

    document = {
        "authority": DEVELOPMENT_ONLY_AUTHORITY,
        "exit": X_FIT_OK,
        "fits_run": len(results),
        "arms": [arm_document(result, protocol) for result in results],
        "code_identity": protocol_code_identity,
        "final_losses": [
            {"suite": r.suite, "seed": r.seed, "final_loss": r.final_loss} for r in results
        ],
        "role_index_sha256": dict(sorted(AUTHORIZED_ROLE_INDEX_SHA256.items())),
        "rollouts_spent": 0,
        "training_protocol": protocol.as_document(),
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
