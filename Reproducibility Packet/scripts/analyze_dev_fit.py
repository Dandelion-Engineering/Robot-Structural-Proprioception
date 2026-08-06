"""Audit the first Gate-4 development fit and persist its in-sample readback.

This is a read-only analysis of the ten already-fitted C1/S rung-1 checkpoints. It reads
only the exact delivered ``dev`` rows authorized by ``utils.dev_fit_trainer``, verifies
the fit result and every checkpoint before inference, and writes one deterministic JSON
summary. It performs no optimization, sets no threshold, generates no data, spends no
rollout, and reads no pilot, validation or test outcome.

The output is deliberately narrower than an evaluation result. Its classification scores
are computed on the same 152 examples used to fit each arm, so they establish only that
the executable data/model path can optimize in sample. The four post-fit loss terms are
reported separately because their sum is not an interpretable ranking statistic: the
Gaussian severity term contains a learned log-scale contribution and may be negative.
"""

from __future__ import annotations

import argparse
import json
import math
import re
from collections import Counter
from pathlib import Path
from typing import Any, Sequence

import torch
from torch import nn

from utils import dev_fit_trainer as trainer
from utils.attribution_net import TemporalAttributionNet, deterministic_conv_precision
from utils.dev_fit_contract import (
    DEVELOPMENT_ONLY_AUTHORITY,
    PREDECLARED_TRAINING_SEEDS,
    DevFitContractError,
    code_identity,
    matched_fit_plan,
    require_complete_matched_plan,
)
from utils.estimator import SOURCE_CLASS_ORDER
from utils.protocol_p import canonical_text_sha256


OUTPUT_NAME = "dev_fit_analysis.json"
ANALYSIS_AUTHORITY = (
    "DEVELOPMENT-ONLY IN-SAMPLE READBACK: establishes optimizer/data-path operation "
    "only; ineligible for capacity selection, threshold setting, generalization, "
    "validation, confirmatory analysis, or a C1-versus-S research conclusion."
)
EXPECTED_TRAJECTORY_COUNTS = {
    "trajectory_dev_diagnostic_b": 76,
    "trajectory_dev_ordinary_a": 76,
}
EXPECTED_TRAJECTORY_CENSUS = {
    trajectory: {suite: count for suite in ("C1", "S")}
    for trajectory, count in EXPECTED_TRAJECTORY_COUNTS.items()
}
SHA256_RE = re.compile(r"[0-9a-f]{64}")
# The decomposition below re-derives, term by term, the composite `trainer.arm_loss`
# optimized. The two cannot be compared for exact equality: `arm_loss` adds four float32
# tensors and converts once, while the decomposition converts each term and adds in
# float64, so the results differ by float32 accumulation order. Measured over five random
# forward passes at the production shape (Claude, Session 85): worst absolute difference
# 3.576e-07. This tolerance sits two orders above that and far below any difference a
# genuine change to either expression would produce.
DECOMPOSITION_TOLERANCE = 1e-5


class DevFitAnalysisError(RuntimeError):
    """The supplied fit state cannot support the bounded development readback."""


class _StrictJSONError(ValueError):
    """Internal marker for duplicate keys and non-finite JSON constants."""


def require(condition: bool, message: str) -> None:
    """Raise ``DevFitAnalysisError`` unless ``condition`` holds."""

    if not condition:
        raise DevFitAnalysisError(message)


def load_strict_json(path: Path, label: str) -> Any:
    """Load strict UTF-8 JSON, refusing duplicates and non-finite constants."""

    path = Path(path)
    require(path.is_file(), f"the {label} does not exist")

    def reject_constant(value: str) -> None:
        raise _StrictJSONError(f"non-finite JSON constant is forbidden: {value}")

    def unique_object(pairs: list[tuple[str, Any]]) -> dict[str, Any]:
        document: dict[str, Any] = {}
        for key, value in pairs:
            if key in document:
                raise _StrictJSONError(f"duplicate JSON key is forbidden: {key}")
            document[key] = value
        return document

    try:
        return json.loads(
            path.read_text(encoding="utf-8"),
            parse_constant=reject_constant,
            object_pairs_hook=unique_object,
        )
    except (json.JSONDecodeError, UnicodeDecodeError, _StrictJSONError) as error:
        raise DevFitAnalysisError(f"the {label} is not strict JSON") from error


def finite_number(value: Any, label: str) -> float:
    """Return ``value`` as a finite float, rejecting booleans and non-numbers."""

    require(
        isinstance(value, (int, float)) and not isinstance(value, bool),
        f"{label} must be numeric",
    )
    parsed = float(value)
    require(math.isfinite(parsed), f"{label} must be finite")
    return parsed


def validate_fit_result(document: Any) -> list[dict[str, Any]]:
    """Validate the complete ten-arm result and return its arms in plan order."""

    require(isinstance(document, dict), "the fit result must be a JSON object")
    require(document.get("authority") == DEVELOPMENT_ONLY_AUTHORITY, "wrong authority")
    require(document.get("exit") == trainer.X_FIT_OK, "the fit did not take X_FIT_OK")
    require(document.get("fits_run") == len(matched_fit_plan()),
            "the fit result must report one completed fit per planned arm")
    require(document.get("rollouts_spent") == 0, "the fit result spent rollouts")
    require(
        document.get("trajectory_census") == EXPECTED_TRAJECTORY_CENSUS,
        "the fit result carries the wrong trajectory census",
    )

    protocol = document.get("training_protocol")
    require(isinstance(protocol, dict), "the fit result carries no training protocol")
    require(protocol.get("split") == "dev", "the fit protocol is not dev-only")
    require(protocol.get("epochs") == 20, "the fit protocol does not use 20 epochs")
    require(protocol.get("batch_size") == 8, "the fit protocol does not use batch size 8")
    require(
        finite_number(protocol.get("learning_rate"), "learning_rate") == 1e-3,
        "the fit protocol does not use learning rate 1e-3",
    )
    require(protocol.get("window_steps") == 768, "the fit window is not 768 steps")
    require(protocol.get("windows_per_run") == 1, "the fit uses more than one window")
    require(
        protocol.get("assignment_sha256") == trainer.ASSIGNMENT_CANONICAL_SHA256,
        "the fit protocol does not name the approved assignment",
    )

    identity = document.get("code_identity")
    require(isinstance(identity, dict) and identity, "the fit carries no code identity")
    for label, digest in identity.items():
        require(isinstance(label, str) and label and "/" not in label and "\\" not in label,
                "a code-identity label is not a bare name")
        require(isinstance(digest, str) and SHA256_RE.fullmatch(digest) is not None,
                f"code identity {label!r} is not a SHA-256 digest")

    arms = document.get("arms")
    require(isinstance(arms, list) and len(arms) == len(matched_fit_plan()),
            "the fit must carry exactly one arm record for every arm the plan declares")
    by_pair: dict[tuple[str, int], dict[str, Any]] = {}
    completed: list[tuple[str, int]] = []
    for arm in arms:
        require(isinstance(arm, dict), "every fit arm must be an object")
        suite = arm.get("suite")
        seed = arm.get("training_seed")
        require(isinstance(suite, str), "an arm suite is not a string")
        require(isinstance(seed, int) and not isinstance(seed, bool), "an arm seed is not an integer")
        pair = (suite, seed)
        require(pair not in by_pair, f"the fit repeats arm {pair}")
        completed.append(pair)

        require(arm.get("authority") == DEVELOPMENT_ONLY_AUTHORITY, f"arm {pair} has wrong authority")
        require(arm.get("data_root_name") == trainer.AUTHORIZED_DATA_ROOT_NAME,
                f"arm {pair} names the wrong data root")
        require(arm.get("manifest_sha256") == trainer.AUTHORIZED_MANIFEST_SHA256,
                f"arm {pair} names the wrong manifest")
        require(arm.get("config_hash") == trainer.AUTHORIZED_CONFIG_HASH,
                f"arm {pair} names the wrong config")
        require(arm.get("assignment_sha256") == trainer.ASSIGNMENT_CANONICAL_SHA256,
                f"arm {pair} names the wrong assignment")
        require(arm.get("role_index_sha256") == trainer.AUTHORIZED_ROLE_INDEX_SHA256,
                f"arm {pair} names the wrong role indices")
        require(arm.get("code_identity") == identity, f"arm {pair} code identity diverges")
        require(arm.get("training_protocol") == protocol, f"arm {pair} protocol diverges")
        require(arm.get("n_examples") == 152, f"arm {pair} does not carry 152 examples")
        require(arm.get("examples_by_trajectory") == EXPECTED_TRAJECTORY_COUNTS,
                f"arm {pair} has the wrong trajectory counts")
        require(arm.get("checkpoint_name") == f"dev_fit_{suite}_seed{seed}.pt",
                f"arm {pair} has the wrong checkpoint name")
        checkpoint_digest = arm.get("checkpoint_sha256")
        require(isinstance(checkpoint_digest, str) and SHA256_RE.fullmatch(checkpoint_digest) is not None,
                f"arm {pair} has no valid checkpoint digest")
        finite_number(arm.get("final_loss"), f"arm {pair} final_loss")
        history = arm.get("loss_history")
        require(isinstance(history, list) and len(history) == protocol["epochs"],
                f"arm {pair} has the wrong loss-history length")
        for epoch, loss in enumerate(history):
            finite_number(loss, f"arm {pair} epoch {epoch} loss")
        by_pair[pair] = arm

    try:
        require_complete_matched_plan(completed)
    except DevFitContractError as error:
        raise DevFitAnalysisError("the fit arms are not the complete matched plan") from error

    expected_final_losses = [
        {"suite": suite, "seed": seed, "final_loss": by_pair[(suite, seed)]["final_loss"]}
        for suite, seed in matched_fit_plan()
    ]
    require(document.get("final_losses") == expected_final_losses,
            "the top-level final-loss index diverges from the arm records")
    return [by_pair[pair] for pair in matched_fit_plan()]


def classification_metrics(
    truth: Sequence[int], prediction: Sequence[int], *, n_classes: int
) -> dict[str, Any]:
    """Return accuracy, macro-F1 and per-class F1 over a fixed class universe."""

    require(len(truth) == len(prediction) and len(truth) > 0,
            "classification arrays must be non-empty and equally sized")
    require(
        n_classes == len(SOURCE_CLASS_ORDER),
        "classification must use the fixed source-class universe",
    )
    require(all(isinstance(value, int) and 0 <= value < n_classes for value in truth),
            "a target class index is outside the fixed class universe")
    require(all(isinstance(value, int) and 0 <= value < n_classes for value in prediction),
            "a predicted class index is outside the fixed class universe")

    per_class: list[float] = []
    for class_index in range(n_classes):
        true_positive = sum(
            actual == class_index and predicted == class_index
            for actual, predicted in zip(truth, prediction)
        )
        false_positive = sum(
            actual != class_index and predicted == class_index
            for actual, predicted in zip(truth, prediction)
        )
        false_negative = sum(
            actual == class_index and predicted != class_index
            for actual, predicted in zip(truth, prediction)
        )
        denominator = 2 * true_positive + false_positive + false_negative
        per_class.append(0.0 if denominator == 0 else 2 * true_positive / denominator)
    return {
        "accuracy": sum(a == b for a, b in zip(truth, prediction)) / len(truth),
        "macro_f1": sum(per_class) / n_classes,
        "per_class_f1": {
            SOURCE_CLASS_ORDER[index]: per_class[index] for index in range(n_classes)
        },
    }


def post_fit_loss_terms(heads: Any, batch: dict[str, torch.Tensor]) -> dict[str, float]:
    """Return the four full-batch loss terms, their sum, and the mean severity log-scale.

    The four expressions below are a decomposition of `trainer.arm_loss`, which returns
    only the scalar sum and is therefore the one thing a reader cannot take apart. Because
    they are written out again here rather than imported, they are a copy, and a copy of an
    expression disagrees silently with its original the moment either moves. So the
    trainer's own composite is this function's post-condition: the four terms are required
    to sum to `arm_loss` on the same heads and the same batch, to `DECOMPOSITION_TOLERANCE`.
    That makes the other routine's value the check rather than this routine's reading of it.
    """

    class_loss = nn.functional.cross_entropy(heads.class_logits, batch["class_index"])
    location_loss = nn.functional.cross_entropy(heads.location_logits, batch["location_index"])
    log_scale = heads.severity_log_scale.clamp(-10.0, 10.0)
    severity_loss = (
        0.5
        * (((batch["severity"] - heads.severity_value) ** 2) * torch.exp(-2.0 * log_scale))
        + log_scale
    ).mean()
    ood_loss = nn.functional.binary_cross_entropy_with_logits(
        heads.unknown_logit, batch["ood"]
    )
    terms = {
        "class_cross_entropy": float(class_loss),
        "location_cross_entropy": float(location_loss),
        "severity_gaussian_nll": float(severity_loss),
        "ood_binary_cross_entropy": float(ood_loss),
    }
    terms["total"] = (
        terms["class_cross_entropy"]
        + terms["location_cross_entropy"]
        + terms["severity_gaussian_nll"]
        + terms["ood_binary_cross_entropy"]
    )
    composite = float(trainer.arm_loss(heads, batch))
    require(
        abs(terms["total"] - composite) <= DECOMPOSITION_TOLERANCE,
        "the decomposed loss terms do not sum to the trainer's own composite loss",
    )
    terms["severity_log_scale_mean"] = float(log_scale.mean())
    return terms


def analysis_code_identity() -> dict[str, str]:
    """Identify the executable text used to load, infer and score this readback."""

    script = Path(__file__).resolve()
    utils = script.parent / "utils"
    return code_identity(
        {
            "analyze_dev_fit.py": script,
            "dev_fit_trainer.py": utils / "dev_fit_trainer.py",
            "dev_fit_contract.py": utils / "dev_fit_contract.py",
            "attribution_net.py": utils / "attribution_net.py",
            "config_contract.py": utils / "config_contract.py",
            "estimator.py": utils / "estimator.py",
            "role_contract.py": utils / "role_contract.py",
            "schema_types.py": utils / "schema_types.py",
            "storage_contract.py": utils / "storage_contract.py",
        }
    )


def load_authorized_examples(data_root: Path) -> tuple[dict[str, list[Any]], dict[str, Any]]:
    """Load exactly the approved dev examples once per suite and return their census."""

    data_root = Path(data_root)
    manifest = data_root / "manifest.csv"
    require(manifest.is_file(), "the authorized data root carries no manifest.csv")
    manifest_digest = trainer.file_sha256(manifest)
    try:
        trainer.require_authorized_dataset(data_root, manifest_sha256=manifest_digest)
        rows, census = trainer.select_dev_rows(manifest)
        trainer.require_authorized_dataset(
            data_root, manifest_sha256=manifest_digest, selected_rows=rows
        )
        schedule, assignment_digest = trainer.authorized_window_schedule()
        loaders, label_loader = trainer.build_role_loaders(data_root)
        trajectory_census = trainer.require_matched_trajectory_census(rows, schedule)
        extractor = trainer.WindowFeatureExtractor(window_steps=trainer.DEVELOPMENT_WINDOW_STEPS)
        examples = {}
        for suite in ("C1", "S"):
            suite_rows = [row for row in rows if row.suite == suite]
            examples[suite] = trainer.load_arm_examples(
                suite_rows,
                suite=suite,
                schedule_by_trajectory=schedule,
                extractor=extractor,
                observation_loader=loaders[suite],
                label_loader=label_loader,
            )
    except (DevFitContractError, trainer.DevFitDataError) as error:
        raise DevFitAnalysisError("the authorized dev rows failed closed") from error

    require(trajectory_census == EXPECTED_TRAJECTORY_CENSUS,
            "the loaded dev rows carry the wrong trajectory census")
    require(all(len(examples[suite]) == 152 for suite in ("C1", "S")),
            "each suite must load exactly 152 dev examples")
    return examples, {
        "manifest_sha256": manifest_digest,
        "assignment_sha256": assignment_digest,
        "row_disclosure": census.disclosure(),
        "trajectory_census": trajectory_census,
    }


def evaluate_arm(
    arm: dict[str, Any], examples: Sequence[Any], checkpoint_dir: Path
) -> dict[str, Any]:
    """Verify, load and score one fitted checkpoint on its own training examples."""

    checkpoint = Path(checkpoint_dir) / arm["checkpoint_name"]
    require(checkpoint.is_file(), f"checkpoint {arm['checkpoint_name']} does not exist")
    require(trainer.file_sha256(checkpoint) == arm["checkpoint_sha256"],
            f"checkpoint {arm['checkpoint_name']} does not match its recorded digest")
    try:
        state = torch.load(checkpoint, map_location="cpu", weights_only=True)
        network = TemporalAttributionNet(seed=arm["training_seed"])
        network.load_state_dict(state, strict=True)
    except (OSError, RuntimeError, TypeError, ValueError) as error:
        raise DevFitAnalysisError(f"checkpoint {arm['checkpoint_name']} cannot be loaded") from error

    batch = trainer._stack(examples, torch.device("cpu"))
    network.eval()
    with torch.no_grad(), deterministic_conv_precision():
        heads = network(batch["inputs"])
        loss_terms = post_fit_loss_terms(heads, batch)
        prediction = heads.class_logits.argmax(dim=1).tolist()
        truth = batch["class_index"].tolist()
    metrics = classification_metrics(truth, prediction, n_classes=len(SOURCE_CLASS_ORDER))
    return {
        "suite": arm["suite"],
        "seed": arm["training_seed"],
        "n_examples": len(examples),
        "checkpoint_name": arm["checkpoint_name"],
        "checkpoint_sha256": arm["checkpoint_sha256"],
        "training_final_epoch_mean_loss": arm["final_loss"],
        "post_fit_full_batch_loss_terms": loss_terms,
        "classification": metrics,
    }


def arithmetic_mean(values: Sequence[float]) -> float:
    """Return the mean of a non-empty finite sequence."""

    require(bool(values), "cannot take the mean of an empty sequence")
    parsed = [finite_number(value, "mean input") for value in values]
    return sum(parsed) / len(parsed)


def sample_standard_deviation(values: Sequence[float]) -> float:
    """Return the ordinary sample SD of at least two finite values."""

    require(len(values) >= 2, "sample SD requires at least two values")
    parsed = [finite_number(value, "sample-SD input") for value in values]
    center = arithmetic_mean(parsed)
    return math.sqrt(sum((value - center) ** 2 for value in parsed) / (len(parsed) - 1))


def rounded(value: Any) -> Any:
    """Round finite floats recursively so the text artifact carries a bounded decimal tail.

    This trims the float64 print of each value; it is **not** a hardware-stability
    mechanism and no claim of one is made here. The loss terms originate in float32
    tensors, and every one of them was measured (Claude, Session 85) to round-trip through
    `round(x, 12)` to the identical float32 — so two machines that disagreed in the float32
    result would still write two different numbers here. What makes this artifact
    reproducible is the fixed CPU device, the deterministic convolution context and the
    verified checkpoint digests, not this function.
    """

    if isinstance(value, float):
        require(math.isfinite(value), "the analysis produced a non-finite float")
        return round(value, 12)
    if isinstance(value, list):
        return [rounded(item) for item in value]
    if isinstance(value, dict):
        return {key: rounded(item) for key, item in value.items()}
    return value


def derive_analysis(
    *, data_root: Path, fit_result_path: Path, checkpoint_dir: Path
) -> dict[str, Any]:
    """Derive the complete bounded development-only fit analysis."""

    fit_result_path = Path(fit_result_path)
    fit_result = load_strict_json(fit_result_path, "fit result")
    arms = validate_fit_result(fit_result)
    current_fit_identity = trainer.training_code_identity()
    require(fit_result["code_identity"] == current_fit_identity,
            "the fit result does not name the current executable training state")
    examples_by_suite, data_census = load_authorized_examples(Path(data_root))
    require(data_census["assignment_sha256"] == fit_result["training_protocol"]["assignment_sha256"],
            "the loaded assignment does not equal the fit result's assignment")

    evaluated = [
        evaluate_arm(arm, examples_by_suite[arm["suite"]], Path(checkpoint_dir))
        for arm in arms
    ]
    class_counts_by_suite: dict[str, dict[str, int]] = {}
    ood_counts: dict[str, int] = {}
    for suite, examples in examples_by_suite.items():
        counts = Counter(example.class_index for example in examples)
        class_counts_by_suite[suite] = {
            SOURCE_CLASS_ORDER[index]: counts.get(index, 0)
            for index in range(len(SOURCE_CLASS_ORDER))
        }
        ood_counts[suite] = sum(bool(example.ood_flag) for example in examples)
    require(class_counts_by_suite["C1"] == class_counts_by_suite["S"],
            "C1 and S do not carry the same class census")
    require(ood_counts == {"C1": 0, "S": 0}, "the dev fit unexpectedly carries OOD rows")

    total = sum(class_counts_by_suite["C1"].values())
    proportions = [count / total for count in class_counts_by_suite["C1"].values()]
    baselines = {
        "empirical_prior_cross_entropy": -sum(p * math.log(p) for p in proportions if p > 0),
        "majority_class_accuracy": max(proportions),
        "majority_class": max(
            class_counts_by_suite["C1"], key=class_counts_by_suite["C1"].get
        ),
    }

    suite_summary: dict[str, Any] = {}
    for suite in ("C1", "S"):
        subset = [entry for entry in evaluated if entry["suite"] == suite]
        suite_summary[suite] = {
            "n_arms": len(subset),
            "mean_accuracy": arithmetic_mean(
                [entry["classification"]["accuracy"] for entry in subset]
            ),
            "mean_macro_f1": arithmetic_mean(
                [entry["classification"]["macro_f1"] for entry in subset]
            ),
            "mean_post_fit_full_batch_loss_terms": {
                key: arithmetic_mean(
                    [entry["post_fit_full_batch_loss_terms"][key] for entry in subset]
                )
                for key in (
                    "class_cross_entropy",
                    "location_cross_entropy",
                    "severity_gaussian_nll",
                    "ood_binary_cross_entropy",
                    "total",
                    "severity_log_scale_mean",
                )
            },
            "mean_per_class_f1": {
                class_name: arithmetic_mean(
                    [entry["classification"]["per_class_f1"][class_name] for entry in subset]
                )
                for class_name in SOURCE_CLASS_ORDER
            },
        }

    paired = []
    # The seeds come from the contract that defined the plan, not from a literal range.
    # `validate_fit_result` has already established that `evaluated` is exactly the matched
    # plan, so every lookup below resolves; a hand-typed range would agree with the plan
    # only until the plan changed, and would then raise `StopIteration` rather than refuse.
    for seed in PREDECLARED_TRAINING_SEEDS:
        c1 = next(entry for entry in evaluated if entry["suite"] == "C1" and entry["seed"] == seed)
        structural = next(entry for entry in evaluated if entry["suite"] == "S" and entry["seed"] == seed)
        paired.append(
            {
                "seed": seed,
                "C1_macro_f1": c1["classification"]["macro_f1"],
                "S_macro_f1": structural["classification"]["macro_f1"],
                "S_minus_C1_macro_f1": (
                    structural["classification"]["macro_f1"]
                    - c1["classification"]["macro_f1"]
                ),
            }
        )
    differences = [row["S_minus_C1_macro_f1"] for row in paired]

    report = {
        "purpose": "In-sample readback of the first ten Gate-4 development-only fits.",
        "authority": ANALYSIS_AUTHORITY,
        "inputs": {
            "fit_result_canonical_sha256": canonical_text_sha256(fit_result_path),
            "fit_code_identity": fit_result["code_identity"],
            "analysis_code_identity": analysis_code_identity(),
            "manifest_sha256": data_census["manifest_sha256"],
            "assignment_sha256": data_census["assignment_sha256"],
            "role_index_sha256": trainer.AUTHORIZED_ROLE_INDEX_SHA256,
            "data_root_name": trainer.AUTHORIZED_DATA_ROOT_NAME,
        },
        "data_census": {
            "n_examples_per_arm": 152,
            "class_counts_by_suite": class_counts_by_suite,
            "ood_counts_by_suite": ood_counts,
            "trajectory_census": data_census["trajectory_census"],
            "row_disclosure": data_census["row_disclosure"],
        },
        "baselines": baselines,
        "arms": evaluated,
        "suite_summary": suite_summary,
        "paired_macro_f1": {
            "by_seed": paired,
            "mean_S_minus_C1": arithmetic_mean(differences),
            "sample_sd_S_minus_C1": sample_standard_deviation(differences),
            "claim_sheet_success_bar": 0.05,
            "interpretation": (
                "development-only in-sample diagnostic; neither the sign nor the spread "
                "is a held-out C1-versus-S result"
            ),
        },
        "loss_interpretation": (
            "training_final_epoch_mean_loss is the mean of minibatch totals during the "
            "last optimizer epoch. post_fit_full_batch_loss_terms are recomputed after "
            "the final update. The severity Gaussian NLL contains log-scale and may be "
            "negative, so the total is not a standalone learning or ranking metric."
        ),
        "boundary": {
            "in_sample": True,
            "development_only": True,
            "generalization_established": False,
            "capacity_selected": False,
            "threshold_selected": False,
            "ood_behavior_established": False,
            "pilot_validation_test_outcomes_read": 0,
        },
        "fits_run": 0,
        "generation_runs": 0,
        "rollouts_spent": 0,
    }
    return rounded(report)


def render(report: dict[str, Any]) -> str:
    """Return a compact human-readable summary of the bounded analysis."""

    c1 = report["suite_summary"]["C1"]
    structural = report["suite_summary"]["S"]
    paired = report["paired_macro_f1"]
    return "\n".join(
        [
            "Gate-4 dev-fit in-sample readback (zero fits, zero rollouts)",
            f"C1 mean accuracy / macro-F1: {c1['mean_accuracy']:.4f} / {c1['mean_macro_f1']:.4f}",
            f" S mean accuracy / macro-F1: {structural['mean_accuracy']:.4f} / {structural['mean_macro_f1']:.4f}",
            f"paired S-C1 macro-F1: mean {paired['mean_S_minus_C1']:+.4f}, sample SD {paired['sample_sd_S_minus_C1']:.4f}",
            "BOUNDARY: in-sample development readback only; no capacity or threshold selected.",
        ]
    )


def main() -> None:
    """Parse paths, derive the analysis, print it, and write canonical JSON."""

    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument("--data-root", required=True, type=Path)
    parser.add_argument("--fit-result", required=True, type=Path)
    parser.add_argument("--checkpoint-dir", required=True, type=Path)
    parser.add_argument("--output-dir", required=True, type=Path)
    args = parser.parse_args()

    report = derive_analysis(
        data_root=args.data_root,
        fit_result_path=args.fit_result,
        checkpoint_dir=args.checkpoint_dir,
    )
    print(render(report), flush=True)
    args.output_dir.mkdir(parents=True, exist_ok=True)
    output_path = args.output_dir / OUTPUT_NAME
    output_path.write_text(
        json.dumps(report, indent=1, sort_keys=True, ensure_ascii=False, allow_nan=False) + "\n",
        encoding="utf-8",
        newline="\n",
    )
    print(f"wrote {output_path}", flush=True)


if __name__ == "__main__":
    main()
