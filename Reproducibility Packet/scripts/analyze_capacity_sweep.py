"""Derive the pre-declared descriptive read of one complete Gate-4 capacity sweep.

This is invariant C7 from ``protocol/capacity-escalation-v0.1.md``: a new read-only
analysis, separate from both the approved first-fit analyzer and the sweep executable.
It authenticates the approved plan and terminal sweep record, refuses a partial run,
re-opens only the authorized development examples and the checkpoints named by the
record, independently verifies every stored classification metric, and writes one
deterministic descriptive JSON artifact.

The script performs no optimization, writes no checkpoint, reads no pilot, validation or
test outcome, generates no data, spends no rollout, selects no capacity or threshold, and
emits none of section 5.4's interpretation prose. Building and reviewing this file is not
permission to run it; execution and exact-state review remain separate gates.
"""

from __future__ import annotations

import argparse
import json
import math
import re
import sys
from collections import Counter
from pathlib import Path, PurePosixPath
from typing import Any, Mapping, Sequence

import torch

import analyze_dev_fit as approved_analysis
from utils import capacity_sweep as sweep
from utils.attribution_net import TemporalAttributionNet, deterministic_conv_precision
from utils.dev_fit_contract import code_identity
from utils.protocol_p import canonical_text_sha256
from utils.capacity_sweep import (
    classify_shape,
    derived_label,
    headroom,
    pair_constraint,
    quantize,
    require_complete_sweep,
)


OUTPUT_NAME = "capacity_sweep_analysis.json"
X_ANALYSIS_OK = "X_ANALYSIS_OK"
X_ANALYSIS_REFUSED = "X_ANALYSIS_REFUSED"
EXIT_CODES = {X_ANALYSIS_OK: 0, X_ANALYSIS_REFUSED: 3}
SHA256_RE = re.compile(r"[0-9a-f]{64}")

ANALYSIS_AUTHORITY = (
    "DEVELOPMENT-ONLY DESCRIPTIVE READ: in-sample width sensitivity under the frozen "
    "Stage-1 protocol; not held-out evidence, not a threshold or capacity selection, "
    "and not a C1-versus-S conclusion"
)


class CapacitySweepAnalysisError(RuntimeError):
    """The supplied exact state cannot support the bounded descriptive read."""


def require(condition: bool, message: str) -> None:
    """Raise ``CapacitySweepAnalysisError`` unless ``condition`` holds."""

    if not condition:
        raise CapacitySweepAnalysisError(message)


def finite_number(value: Any, label: str) -> float:
    """Return a finite numeric value as float, refusing booleans and non-numbers."""

    require(
        isinstance(value, (int, float)) and not isinstance(value, bool),
        f"{label} must be numeric",
    )
    parsed = float(value)
    require(math.isfinite(parsed), f"{label} must be finite")
    return parsed


def unit_interval(value: Any, label: str) -> float:
    """Return a finite score in the closed unit interval."""

    parsed = finite_number(value, label)
    require(0.0 <= parsed <= 1.0, f"{label} must be in [0, 1]")
    return parsed


def sha256_digest(value: Any, label: str) -> str:
    """Return a lowercase SHA-256 hex digest."""

    require(
        isinstance(value, str) and SHA256_RE.fullmatch(value) is not None,
        f"{label} must be a lowercase SHA-256 digest",
    )
    return value


def strict_object(path: Path, label: str) -> dict[str, Any]:
    """Load one strict-JSON object through the approved analyzer's parser."""

    try:
        document = approved_analysis.load_strict_json(Path(path), label)
    except approved_analysis.DevFitAnalysisError as error:
        raise CapacitySweepAnalysisError(str(error)) from error
    require(isinstance(document, dict), f"the {label} must be a JSON object")
    return document


def analysis_code_identity() -> dict[str, str]:
    """Identify this reader and every bound production module it executes through."""

    identity = dict(sweep.sweep_code_identity())
    identity.update(
        code_identity(
            {
                "analyze_capacity_sweep.py": Path(__file__).resolve(),
                "analyze_dev_fit.py": Path(approved_analysis.__file__).resolve(),
            }
        )
    )
    return dict(sorted(identity.items()))


def observed(value: float) -> dict[str, Any]:
    """Persist one derived float both raw and at the frozen six-decimal tie rule."""

    parsed = finite_number(value, "derived observation")
    return {"raw": parsed, "quantized": quantize(parsed)}


def _same_tree(left: Any, right: Any, label: str) -> None:
    """Require exact equality between two authenticated JSON subtrees."""

    require(left == right, f"{label} differs between the approved plan and sweep record")


def validate_envelope(
    result: Mapping[str, Any],
    plan: Mapping[str, Any],
    anchor_analysis: Mapping[str, Any],
    *,
    plan_sha256: str,
    anchor_analysis_sha256: str,
) -> tuple[float, float]:
    """Authenticate the complete terminal record, plan, design and sourced constants."""

    try:
        require_complete_sweep(result)
    except (sweep.DevFitContractError, sweep.CapacitySweepError) as error:
        raise CapacitySweepAnalysisError(
            "the terminal record is not a complete sweep"
        ) from error

    require(result.get("exit") == sweep.X_SWEEP_OK, "the sweep did not take X_SWEEP_OK")
    require(result.get("mode") == "execute", "the sweep record is not execute mode")
    require(result.get("reason_class") is None, "the successful sweep carries a refusal reason")
    require(result.get("authority") == sweep.SWEEP_AUTHORITY, "the sweep authority is wrong")
    require(plan.get("exit") == sweep.X_PLAN_OK, "the plan did not take X_PLAN_OK")
    require(plan.get("mode") == "plan", "the approved plan is not plan mode")
    require(plan.get("plan_valid") is True, "the approved plan is not valid")
    require(plan.get("authority") == sweep.SWEEP_AUTHORITY, "the plan authority is wrong")

    plan_sha256 = sha256_digest(plan_sha256, "approved plan digest")
    anchor_analysis_sha256 = sha256_digest(
        anchor_analysis_sha256, "approved anchor-analysis digest"
    )
    require(
        result.get("approved_plan_sha256") == plan_sha256,
        "the terminal record is not bound to the supplied approved plan",
    )
    require(
        plan.get("approved_analysis_sha256") == anchor_analysis_sha256,
        "the approved plan is not bound to the supplied anchor analysis",
    )
    require(
        result.get("run_label") == plan.get("run_label"),
        "the terminal record and approved plan name different runs",
    )

    design_sha256 = sweep.design_digest()
    require(
        design_sha256 == sweep.DESIGN_CANONICAL_SHA256,
        "the frozen capacity design no longer matches its pinned digest",
    )
    require(
        result.get("design_sha256") == design_sha256
        and plan.get("design_sha256") == design_sha256,
        "the supplied exact state is not bound to the frozen capacity design",
    )
    current_sweep_identity = sweep.sweep_code_identity()
    require(
        plan.get("code_identity") == current_sweep_identity,
        "the approved plan names a different sweep executable state",
    )
    require(
        result.get("code_identity") == current_sweep_identity,
        "the terminal record names a different sweep executable state",
    )
    try:
        sweep.require_approved_analyzer_identity(anchor_analysis)
    except (sweep.DevFitContractError, sweep.CapacitySweepError) as error:
        raise CapacitySweepAnalysisError(
            "the approved first-fit analyzer no longer matches its recorded identity"
        ) from error

    expected_points = list(sweep.CAPACITY_POINTS)
    require(
        result.get("capacity_points") == expected_points
        and plan.get("capacity_points") == expected_points,
        "the supplied state does not name the frozen five-point grid",
    )
    require(
        result.get("fits_attempted") == sweep.MAX_FITS
        and result.get("checkpoints_written") == sweep.MAX_CHECKPOINTS
        and result.get("curve_fits_attempted") == len(sweep.curve_arms())
        and result.get("curve_checkpoints_written") == len(sweep.curve_arms())
        and result.get("equivalence_fits_attempted") == len(sweep.EQUIVALENCE_ARMS)
        and result.get("equivalence_checkpoints_written") == len(sweep.EQUIVALENCE_ARMS),
        "the terminal resource counts do not equal the complete frozen sweep",
    )
    for document, label in ((result, "terminal record"), (plan, "approved plan")):
        budget = document.get("maximum_budget")
        require(isinstance(budget, Mapping), f"the {label} carries no maximum budget")
        require(
            budget.get("fits") == sweep.MAX_FITS
            and budget.get("checkpoints") == sweep.MAX_CHECKPOINTS
            and budget.get("generation_runs") == 0
            and budget.get("non_dev_reads") == 0
            and budget.get("rollouts") == 0,
            f"the {label} carries the wrong resource budget",
        )
    require(
        result.get("generation_runs") == 0
        and result.get("non_dev_reads") == 0
        and result.get("rollouts_spent") == 0,
        "the terminal record crossed the development-only resource boundary",
    )

    for field in ("training_protocol", "code_identity"):
        _same_tree(result.get(field), plan.get(field), field)
    data_census = result.get("data_census")
    require(isinstance(data_census, Mapping), "the terminal record carries no data census")
    require(
        data_census.get("manifest_sha256") == plan.get("manifest_sha256")
        and data_census.get("assignment_sha256") == plan.get("assignment_sha256"),
        "the terminal data census differs from the approved plan",
    )

    require(
        plan.get("claim_sheet_success_bar_field") == ".".join(sweep.BAR_FIELD_PATH),
        "the plan names the wrong source field for the success bar",
    )
    require(
        plan.get("anchor_sample_sd_field")
        == ".".join(sweep.ANCHOR_SAMPLE_SD_FIELD_PATH),
        "the plan names the wrong source field for the anchor sample SD",
    )
    try:
        bar = sweep.read_success_bar(anchor_analysis)
        anchor_sd = sweep.read_anchor_sample_sd(anchor_analysis)
    except sweep.CapacitySweepError as error:
        raise CapacitySweepAnalysisError("a sourced constant is invalid") from error
    require(
        plan.get("claim_sheet_success_bar") == bar,
        "the plan's success bar differs from its approved source field",
    )
    require(
        plan.get("anchor_sample_sd") == anchor_sd,
        "the plan's anchor sample SD differs from its approved source field",
    )
    return bar, anchor_sd


def _validate_code_identity(value: Any, label: str) -> dict[str, str]:
    """Return a non-empty, sorted module-to-digest identity map."""

    require(isinstance(value, Mapping) and bool(value), f"{label} carries no code identity")
    parsed: dict[str, str] = {}
    for name, digest in value.items():
        require(isinstance(name, str) and bool(name), f"{label} has a malformed module name")
        parsed[name] = sha256_digest(digest, f"{label} identity for {name}")
    return dict(sorted(parsed.items()))


def validate_arm(arm: Mapping[str, Any]) -> dict[str, Any]:
    """Validate and normalize one persisted curve arm without interpreting its scores."""

    require(isinstance(arm, Mapping), "a curve arm is not an object")
    channels = arm.get("channels")
    suite_name = arm.get("suite")
    seed = arm.get("seed")
    require(
        isinstance(channels, int)
        and not isinstance(channels, bool)
        and channels in sweep.CAPACITY_POINTS,
        "a curve arm carries an invalid capacity point",
    )
    require(suite_name in ("C1", "S"), "a curve arm carries an invalid suite")
    require(
        isinstance(seed, int)
        and not isinstance(seed, bool)
        and seed in sweep.PREDECLARED_TRAINING_SEEDS,
        "a curve arm carries an invalid seed",
    )
    expected_status = (
        sweep.ARM_REUSED if channels == sweep.ANCHOR_CHANNELS else sweep.ARM_COMPLETED
    )
    require(arm.get("status") == expected_status, "a curve arm carries the wrong status")
    require(
        arm.get("n_parameters") == sweep.EXPECTED_PARAMETERS[channels],
        "a curve arm carries the wrong parameter count",
    )
    require(
        arm.get("receptive_field") == sweep.EXPECTED_RECEPTIVE_FIELD,
        "a curve arm carries the wrong receptive field",
    )
    accuracy = unit_interval(arm.get("accuracy"), "curve-arm accuracy")
    macro_f1 = unit_interval(arm.get("macro_f1"), "curve-arm macro-F1")
    per_class = arm.get("per_class_f1")
    expected_classes = tuple(approved_analysis.SOURCE_CLASS_ORDER)
    require(
        isinstance(per_class, Mapping) and set(per_class) == set(expected_classes),
        "a curve arm carries the wrong per-class F1 universe",
    )
    parsed_per_class = {
        name: unit_interval(per_class[name], f"curve-arm {name} F1")
        for name in expected_classes
    }
    parsed = {
        "accuracy": accuracy,
        "channels": channels,
        "checkpoint_sha256": sha256_digest(
            arm.get("checkpoint_sha256"), "curve-arm checkpoint digest"
        ),
        "fit_code_identity": _validate_code_identity(
            arm.get("fit_code_identity"), "curve arm"
        ),
        "macro_f1": macro_f1,
        "n_parameters": arm.get("n_parameters"),
        "per_class_f1": parsed_per_class,
        "receptive_field": arm.get("receptive_field"),
        "seed": seed,
        "source": arm.get("source"),
        "status": arm.get("status"),
        "suite": suite_name,
    }
    require(
        parsed["source"]
        == ("approved-ledger" if expected_status == sweep.ARM_REUSED else "capacity-sweep"),
        "a curve arm carries the wrong provenance source",
    )
    if expected_status == sweep.ARM_COMPLETED:
        n_examples = arm.get("n_examples")
        history = arm.get("loss_history")
        require(
            isinstance(n_examples, int) and not isinstance(n_examples, bool) and n_examples > 0,
            "a completed curve arm carries no positive example count",
        )
        require(
            isinstance(history, list) and bool(history),
            "a completed curve arm carries no loss history",
        )
        parsed["n_examples"] = n_examples
        parsed["final_loss"] = finite_number(arm.get("final_loss"), "curve-arm final loss")
        parsed["loss_history"] = [
            finite_number(value, "curve-arm loss-history value") for value in history
        ]
        relative = arm.get("checkpoint_relative_name")
        require(
            isinstance(relative, str) and bool(relative),
            "a completed curve arm carries no checkpoint-relative name",
        )
        parsed["checkpoint_relative_name"] = relative
    return parsed


def validate_arms(
    result: Mapping[str, Any], anchor_analysis: Mapping[str, Any]
) -> list[dict[str, Any]]:
    """Validate all fifty arms and independently bind the ten reused anchors."""

    rows = result.get("curve_arms")
    require(isinstance(rows, list), "the terminal record carries no curve arms")
    arms = [validate_arm(row) for row in rows]
    keys = [(arm["channels"], arm["suite"], arm["seed"]) for arm in arms]
    require(len(keys) == 50 and len(set(keys)) == 50, "the curve-arm identities are not unique")

    result_identity = _validate_code_identity(result.get("code_identity"), "terminal record")
    protocol = result.get("training_protocol")
    require(isinstance(protocol, Mapping), "the terminal record carries no training protocol")
    epochs = protocol.get("epochs")
    require(
        isinstance(epochs, int) and not isinstance(epochs, bool) and epochs > 0,
        "the terminal training protocol carries no positive epoch count",
    )
    anchor_inputs = anchor_analysis.get("inputs")
    require(isinstance(anchor_inputs, Mapping), "the approved anchor analysis carries no inputs")
    anchor_identity = _validate_code_identity(
        anchor_inputs.get("fit_code_identity"), "approved anchor analysis"
    )
    for arm in arms:
        expected_identity = (
            anchor_identity
            if arm["status"] == sweep.ARM_REUSED
            else result_identity
        )
        require(
            arm["fit_code_identity"] == expected_identity,
            "a curve arm carries the wrong fitting-code identity",
        )
        if arm["status"] == sweep.ARM_COMPLETED:
            require(
                len(arm["loss_history"]) == epochs,
                "a completed curve arm carries the wrong loss-history length",
            )
            require(
                arm["final_loss"] == arm["loss_history"][-1],
                "a completed curve arm's final loss differs from its loss-history tail",
            )

    approved_rows = anchor_analysis.get("arms")
    require(isinstance(approved_rows, list), "the approved anchor analysis carries no arms")
    approved_by_key: dict[tuple[str, int], Mapping[str, Any]] = {}
    for row in approved_rows:
        require(isinstance(row, Mapping), "the approved anchor analysis has a non-object arm")
        key = (row.get("suite"), row.get("seed"))
        require(key not in approved_by_key, "the approved anchor analysis duplicates an arm")
        approved_by_key[key] = row
    require(
        set(approved_by_key)
        == {
            (suite_name, seed)
            for suite_name in ("C1", "S")
            for seed in sweep.PREDECLARED_TRAINING_SEEDS
        },
        "the approved anchor analysis carries the wrong arm identities",
    )
    for arm in arms:
        if arm["channels"] != sweep.ANCHOR_CHANNELS:
            continue
        approved = approved_by_key[(arm["suite"], arm["seed"])]
        classification = approved.get("classification")
        require(isinstance(classification, Mapping), "an approved anchor has no classification")
        require(
            arm["checkpoint_sha256"] == approved.get("checkpoint_sha256")
            and arm["accuracy"] == classification.get("accuracy")
            and arm["macro_f1"] == classification.get("macro_f1")
            and arm["per_class_f1"] == classification.get("per_class_f1"),
            "a reused anchor differs from the approved first-fit analysis",
        )
    suite_order = {"C1": 0, "S": 1}
    return sorted(arms, key=lambda arm: (arm["channels"], suite_order[arm["suite"]], arm["seed"]))


def safe_relative_path(root: Path, value: str, label: str) -> Path:
    """Resolve one persisted POSIX relative name beneath an explicitly supplied root."""

    require(
        "\\" not in value and ":" not in value,
        f"{label} must be a relative POSIX path without a drive prefix",
    )
    relative = PurePosixPath(value)
    require(
        not relative.is_absolute()
        and bool(relative.parts)
        and all(part not in ("", ".", "..") for part in relative.parts),
        f"{label} must be a safe relative path",
    )
    base = Path(root).resolve()
    candidate = base.joinpath(*relative.parts).resolve()
    try:
        candidate.relative_to(base)
    except ValueError as error:
        raise CapacitySweepAnalysisError(f"{label} escapes its supplied root") from error
    return candidate


def anchor_checkpoint_names(anchor_analysis: Mapping[str, Any]) -> dict[tuple[str, int], str]:
    """Return the approved anchor checkpoint names, indexed by suite and seed."""

    rows = anchor_analysis.get("arms")
    require(isinstance(rows, list), "the approved anchor analysis carries no arms")
    names: dict[tuple[str, int], str] = {}
    for row in rows:
        require(isinstance(row, Mapping), "the approved anchor analysis has a non-object arm")
        key = (row.get("suite"), row.get("seed"))
        name = row.get("checkpoint_name")
        require(
            key not in names and isinstance(name, str) and bool(name),
            "an approved anchor carries no unique checkpoint name",
        )
        names[key] = name
    return names


def checkpoint_path(
    arm: Mapping[str, Any],
    *,
    run_root: Path,
    anchor_checkpoint_dir: Path,
    anchor_names: Mapping[tuple[str, int], str],
) -> Path:
    """Resolve one arm's checkpoint within its authenticated namespace."""

    if arm["status"] == sweep.ARM_REUSED:
        name = anchor_names.get((arm["suite"], arm["seed"]))
        require(isinstance(name, str), "a reused anchor has no approved checkpoint name")
        return safe_relative_path(anchor_checkpoint_dir, name, "anchor checkpoint name")
    return safe_relative_path(
        run_root,
        str(arm["checkpoint_relative_name"]),
        "capacity checkpoint relative name",
    )


def evaluate_arm_context(
    arm: Mapping[str, Any], examples: Sequence[Any], checkpoint: Path
) -> dict[str, float]:
    """Verify one checkpoint, recompute its metrics, and return its loss decomposition."""

    checkpoint = Path(checkpoint)
    require(checkpoint.is_file(), "a checkpoint named by the terminal record is absent")
    require(
        sweep.trainer.file_sha256(checkpoint) == arm["checkpoint_sha256"],
        "a checkpoint differs from the digest in the terminal record",
    )
    try:
        state = torch.load(checkpoint, map_location="cpu", weights_only=True)
        network = TemporalAttributionNet(
            channels=arm["channels"],
            seed=arm["seed"],
            enforce_rung1_band=True,
        )
        network.load_state_dict(state, strict=True)
    except (OSError, RuntimeError, TypeError, ValueError) as error:
        raise CapacitySweepAnalysisError("a capacity checkpoint cannot be loaded") from error

    batch = sweep._stack(examples, torch.device("cpu"))
    network.eval()
    with torch.no_grad(), deterministic_conv_precision():
        heads = network(batch["inputs"])
        loss_terms = approved_analysis.post_fit_loss_terms(heads, batch)
        prediction = heads.class_logits.argmax(dim=1).tolist()
        truth = batch["class_index"].tolist()
    metrics = approved_analysis.classification_metrics(
        truth,
        prediction,
        n_classes=len(approved_analysis.SOURCE_CLASS_ORDER),
    )
    require(
        metrics["accuracy"] == arm["accuracy"]
        and metrics["macro_f1"] == arm["macro_f1"]
        and metrics["per_class_f1"] == arm["per_class_f1"],
        "a recomputed checkpoint score differs from the terminal record",
    )
    return {
        key: finite_number(value, f"post-fit {key}") for key, value in loss_terms.items()
    }


def load_development_context(
    *,
    data_root: Path,
    result: Mapping[str, Any],
    anchor_analysis: Mapping[str, Any],
) -> tuple[dict[str, list[Any]], dict[str, Any]]:
    """Load only the authorized dev examples and authenticate their shared context."""

    try:
        examples_by_suite, census = approved_analysis.load_authorized_examples(Path(data_root))
    except approved_analysis.DevFitAnalysisError as error:
        raise CapacitySweepAnalysisError("the authorized dev examples failed closed") from error
    result_census = result.get("data_census")
    require(isinstance(result_census, Mapping), "the terminal record carries no data census")
    require(
        census.get("manifest_sha256") == result_census.get("manifest_sha256")
        and census.get("assignment_sha256") == result_census.get("assignment_sha256")
        and census.get("row_disclosure") == result_census.get("row_disclosure")
        and census.get("trajectory_census") == result_census.get("trajectory_census"),
        "the loaded dev census differs from the terminal record",
    )

    class_counts_by_suite: dict[str, dict[str, int]] = {}
    ood_counts_by_suite: dict[str, int] = {}
    for suite_name, examples in examples_by_suite.items():
        counts = Counter(example.class_index for example in examples)
        class_counts_by_suite[suite_name] = {
            approved_analysis.SOURCE_CLASS_ORDER[index]: counts.get(index, 0)
            for index in range(len(approved_analysis.SOURCE_CLASS_ORDER))
        }
        ood_counts_by_suite[suite_name] = sum(bool(example.ood_flag) for example in examples)

    approved_census = anchor_analysis.get("data_census")
    approved_baselines = anchor_analysis.get("baselines")
    require(
        isinstance(approved_census, Mapping) and isinstance(approved_baselines, Mapping),
        "the approved anchor analysis carries no census or baselines",
    )
    require(
        class_counts_by_suite == approved_census.get("class_counts_by_suite")
        and ood_counts_by_suite == approved_census.get("ood_counts_by_suite"),
        "the loaded dev class/OOD census differs from the approved anchor analysis",
    )
    return examples_by_suite, {
        "baselines": dict(approved_baselines),
        "class_counts_by_suite": class_counts_by_suite,
        "ood_counts_by_suite": ood_counts_by_suite,
        "trajectory_census": census["trajectory_census"],
    }


def evaluate_all_arms(
    arms: Sequence[Mapping[str, Any]],
    *,
    examples_by_suite: Mapping[str, Sequence[Any]],
    run_root: Path,
    anchor_checkpoint_dir: Path,
    anchor_analysis: Mapping[str, Any],
) -> dict[tuple[int, str, int], dict[str, float]]:
    """Recompute every arm's stored score and return its post-fit loss context."""

    names = anchor_checkpoint_names(anchor_analysis)
    evaluated: dict[tuple[int, str, int], dict[str, float]] = {}
    for arm in arms:
        key = (arm["channels"], arm["suite"], arm["seed"])
        require(key not in evaluated, "the analysis attempted to evaluate one arm twice")
        checkpoint = checkpoint_path(
            arm,
            run_root=run_root,
            anchor_checkpoint_dir=anchor_checkpoint_dir,
            anchor_names=names,
        )
        evaluated[key] = evaluate_arm_context(
            arm,
            examples_by_suite[arm["suite"]],
            checkpoint,
        )
    return evaluated


def derive_analysis(
    *,
    arms: Sequence[Mapping[str, Any]],
    loss_context: Mapping[tuple[int, str, int], Mapping[str, float]],
    shared_context: Mapping[str, Any],
    bar: float,
    anchor_sample_sd: float,
    result: Mapping[str, Any],
    input_digests: Mapping[str, str],
) -> dict[str, Any]:
    """Derive exactly section 5.2's descriptive fields from verified persisted primitives."""

    by_key = {
        (arm["channels"], arm["suite"], arm["seed"]): arm for arm in arms
    }
    require(len(by_key) == 50, "the descriptive read did not receive all fifty arms")
    require(set(loss_context) == set(by_key), "the loss context does not cover every arm")
    loss_term_sets = {tuple(sorted(terms)) for terms in loss_context.values()}
    require(
        len(loss_term_sets) == 1 and bool(next(iter(loss_term_sets))),
        "the post-fit loss context does not carry one common non-empty term set",
    )
    loss_terms = next(iter(loss_term_sets))

    reported_arms: list[dict[str, Any]] = []
    for arm in arms:
        key = (arm["channels"], arm["suite"], arm["seed"])
        reported_arms.append(
            {
                "accuracy": arm["accuracy"],
                "channels": arm["channels"],
                "checkpoint_sha256": arm["checkpoint_sha256"],
                "fit_code_identity": arm["fit_code_identity"],
                "macro_f1": arm["macro_f1"],
                "n_parameters": arm["n_parameters"],
                "per_class_f1": arm["per_class_f1"],
                "post_fit_full_batch_loss_terms": dict(loss_context[key]),
                "receptive_field": arm["receptive_field"],
                "seed": arm["seed"],
                "source": arm["source"],
                "status": arm["status"],
                "suite": arm["suite"],
            }
        )

    points: list[dict[str, Any]] = []
    for channels in sweep.CAPACITY_POINTS:
        pairs: list[dict[str, Any]] = []
        headrooms: list[float] = []
        differences: list[float] = []
        for seed in sweep.PREDECLARED_TRAINING_SEEDS:
            c1 = by_key[(channels, "C1", seed)]
            structural = by_key[(channels, "S", seed)]
            difference = structural["macro_f1"] - c1["macro_f1"]
            room = headroom(c1["macro_f1"], structural["macro_f1"])
            differences.append(difference)
            headrooms.append(room)
            pairs.append(
                {
                    "C1_macro_f1": c1["macro_f1"],
                    "S_macro_f1": structural["macro_f1"],
                    "S_minus_C1_macro_f1": observed(difference),
                    "bar_constrained": room < bar,
                    "headroom": observed(room),
                    "seed": seed,
                }
            )
        constraint = pair_constraint(headrooms, bar)
        suite_means = {
            suite_name: approved_analysis.arithmetic_mean(
                [by_key[(channels, suite_name, seed)]["macro_f1"] for seed in sweep.PREDECLARED_TRAINING_SEEDS]
            )
            for suite_name in ("C1", "S")
        }
        mean_difference = approved_analysis.arithmetic_mean(differences)
        sample_sd = approved_analysis.sample_standard_deviation(differences)
        loss_means = {
            suite_name: {
                term: approved_analysis.arithmetic_mean(
                    [
                        loss_context[(channels, suite_name, seed)][term]
                        for seed in sweep.PREDECLARED_TRAINING_SEEDS
                    ]
                )
                for term in loss_terms
            }
            for suite_name in ("C1", "S")
        }
        points.append(
            {
                "channels": channels,
                "development_context": {
                    "baselines": dict(shared_context["baselines"]),
                    "class_counts_by_suite": dict(shared_context["class_counts_by_suite"]),
                    "mean_post_fit_full_batch_loss_terms_by_suite": loss_means,
                    "ood_counts_by_suite": dict(shared_context["ood_counts_by_suite"]),
                },
                "pair_constraint": constraint,
                "paired_S_minus_C1_macro_f1_mean": observed(mean_difference),
                "paired_S_minus_C1_macro_f1_sample_sd": observed(sample_sd),
                "pairs": pairs,
                "suite_mean_macro_f1": {
                    suite_name: observed(value) for suite_name, value in suite_means.items()
                },
            }
        )

    eligible = [point for point in points if point["pair_constraint"] == sweep.CONSTRAINT_NONE]
    post_anchor = [point for point in points if point["channels"] > sweep.ANCHOR_CHANNELS]

    def _nonnegative(point: Mapping[str, Any]) -> bool:
        """Return whether one point's quantized paired mean is nonnegative."""

        return float(point["paired_S_minus_C1_macro_f1_mean"]["quantized"]) >= 0.0

    first_post = next((point for point in post_anchor if _nonnegative(point)), None)
    first_eligible_post = next(
        (
            point
            for point in post_anchor
            if point["pair_constraint"] == sweep.CONSTRAINT_NONE and _nonnegative(point)
        ),
        None,
    )
    eligible_post_channels = [
        point["channels"]
        for point in post_anchor
        if point["pair_constraint"] == sweep.CONSTRAINT_NONE
    ]
    first_all = next(
        (point for point in points if point["pair_constraint"] == sweep.CONSTRAINT_ALL),
        None,
    )

    def _shape_block(selected: Sequence[Mapping[str, Any]]) -> dict[str, Any]:
        """Classify all three ordered curves over one declared point domain."""

        return {
            "C1_mean_macro_f1": classify_shape(
                [point["suite_mean_macro_f1"]["C1"]["raw"] for point in selected]
            ),
            "S_mean_macro_f1": classify_shape(
                [point["suite_mean_macro_f1"]["S"]["raw"] for point in selected]
            ),
            "capacity_points": [point["channels"] for point in selected],
            "paired_mean_S_minus_C1_macro_f1": classify_shape(
                [point["paired_S_minus_C1_macro_f1_mean"]["raw"] for point in selected]
            ),
        }

    eligible_values = [point["paired_S_minus_C1_macro_f1_mean"]["raw"] for point in eligible]
    paired_range = max(eligible_values) - min(eligible_values) if eligible_values else None
    anchor_point = next(
        point for point in points if point["channels"] == sweep.ANCHOR_CHANNELS
    )
    require(
        round(anchor_point["paired_S_minus_C1_macro_f1_sample_sd"]["raw"], 12)
        == anchor_sample_sd,
        "the recomputed 32-channel sample SD differs from its approved source",
    )
    require(
        anchor_point["pair_constraint"] == sweep.CONSTRAINT_NONE,
        "the approved 32-channel anchor is unexpectedly bar-constrained",
    )
    label = derived_label(
        first_post_anchor_nonnegative_point=(
            first_post["channels"] if first_post is not None else None
        ),
        first_eligible_post_anchor_nonnegative_point=(
            first_eligible_post["channels"] if first_eligible_post is not None else None
        ),
        eligible_post_anchor_points=eligible_post_channels,
    )

    report = {
        "authority": ANALYSIS_AUTHORITY,
        "arms": reported_arms,
        "boundary": {
            "capacity_selected": False,
            "development_only": True,
            "fits_run": 0,
            "generalization_established": False,
            "generation_runs": 0,
            "in_sample": True,
            "non_dev_reads": 0,
            "rollouts_spent": 0,
            "threshold_selected": False,
        },
        "constraint": {
            "claim_sheet_success_bar": observed(bar),
            "claim_sheet_success_bar_field": ".".join(sweep.BAR_FIELD_PATH),
            "first_all_constrained_point": (
                first_all["channels"] if first_all is not None else None
            ),
        },
        "curve_shapes": {
            "all_points": _shape_block(points),
            "eligible_subsequence": _shape_block(eligible),
        },
        "derived_label": label,
        "first_eligible_post_anchor_nonnegative_point": (
            first_eligible_post["channels"] if first_eligible_post is not None else None
        ),
        "eligible_post_anchor_points": eligible_post_channels,
        "first_post_anchor_nonnegative_point": (
            first_post["channels"] if first_post is not None else None
        ),
        "first_post_anchor_nonnegative_point_constraint": (
            first_post["pair_constraint"] if first_post is not None else None
        ),
        "inputs": {
            "analysis_code_identity": analysis_code_identity(),
            "approved_anchor_analysis_canonical_sha256": input_digests[
                "approved_anchor_analysis"
            ],
            "approved_plan_canonical_sha256": input_digests["approved_plan"],
            "design_sha256": result["design_sha256"],
            "fit_code_identity": result["code_identity"],
            "run_label": result["run_label"],
            "sweep_result_canonical_sha256": input_digests["sweep_result"],
        },
        "paired_range": observed(paired_range) if paired_range is not None else None,
        "paired_range_exceeds_anchor_sd": (
            paired_range is not None and paired_range > anchor_sample_sd
        ),
        "points": points,
        "source_anchor_sample_sd": observed(anchor_sample_sd),
        "source_anchor_sample_sd_field": ".".join(sweep.ANCHOR_SAMPLE_SD_FIELD_PATH),
    }
    # Recompute the label from the persisted primitives, not the locals that produced it.
    require(
        report["derived_label"]
        == derived_label(
            first_post_anchor_nonnegative_point=report[
                "first_post_anchor_nonnegative_point"
            ],
            first_eligible_post_anchor_nonnegative_point=report[
                "first_eligible_post_anchor_nonnegative_point"
            ],
            eligible_post_anchor_points=report["eligible_post_anchor_points"],
        ),
        "the derived label is not recomputable from the persisted primitives",
    )
    return report


def analyze_paths(
    *,
    data_root: Path,
    sweep_result_path: Path,
    approved_plan_path: Path,
    approved_anchor_analysis_path: Path,
    run_root: Path,
    anchor_checkpoint_dir: Path,
    expected_sweep_result_sha256: str,
) -> dict[str, Any]:
    """Load, authenticate, re-score, and derive one complete descriptive analysis."""

    sweep_result_path = Path(sweep_result_path)
    approved_plan_path = Path(approved_plan_path)
    approved_anchor_analysis_path = Path(approved_anchor_analysis_path)
    run_root = Path(run_root)
    require(
        sweep_result_path.resolve().parent == run_root.resolve()
        and sweep_result_path.name == sweep.RUN_ARTIFACT,
        "the sweep result is not the named terminal artifact at the supplied run root",
    )
    result = strict_object(sweep_result_path, "sweep result")
    plan = strict_object(approved_plan_path, "approved capacity plan")
    anchor_analysis = strict_object(
        approved_anchor_analysis_path, "approved first-fit analysis"
    )
    digests = {
        "sweep_result": canonical_text_sha256(sweep_result_path),
        "approved_plan": canonical_text_sha256(approved_plan_path),
        "approved_anchor_analysis": canonical_text_sha256(
            approved_anchor_analysis_path
        ),
    }
    require(
        digests["sweep_result"]
        == sha256_digest(expected_sweep_result_sha256, "approved sweep-result digest"),
        "the sweep result differs from the exact state authorized for analysis",
    )
    bar, anchor_sample_sd = validate_envelope(
        result,
        plan,
        anchor_analysis,
        plan_sha256=digests["approved_plan"],
        anchor_analysis_sha256=digests["approved_anchor_analysis"],
    )
    arms = validate_arms(result, anchor_analysis)
    examples_by_suite, shared_context = load_development_context(
        data_root=Path(data_root),
        result=result,
        anchor_analysis=anchor_analysis,
    )
    losses = evaluate_all_arms(
        arms,
        examples_by_suite=examples_by_suite,
        run_root=run_root,
        anchor_checkpoint_dir=Path(anchor_checkpoint_dir),
        anchor_analysis=anchor_analysis,
    )
    return derive_analysis(
        arms=arms,
        loss_context=losses,
        shared_context=shared_context,
        bar=bar,
        anchor_sample_sd=anchor_sample_sd,
        result=result,
        input_digests=digests,
    )


def render(report: Mapping[str, Any]) -> str:
    """Return a compact boundary-conscious summary of the descriptive artifact."""

    return "\n".join(
        [
            "Gate-4 capacity sweep descriptive read (zero fits, zero rollouts)",
            f"points: {len(report['points'])}; arms: {len(report['arms'])}",
            f"derived label: {report['derived_label']}",
            "BOUNDARY: development-only in-sample description; no capacity or threshold selected.",
        ]
    )


def write_exclusive(output_dir: Path, report: Mapping[str, Any]) -> Path:
    """Write canonical compact JSON once, refusing to overwrite an existing artifact."""

    output_dir = Path(output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)
    output_path = output_dir / OUTPUT_NAME
    payload = json.dumps(
        report,
        sort_keys=True,
        separators=(",", ":"),
        ensure_ascii=False,
        allow_nan=False,
    )
    try:
        with output_path.open("x", encoding="utf-8", newline="\n") as handle:
            handle.write(payload)
    except FileExistsError as error:
        raise CapacitySweepAnalysisError(
            "the analysis output already exists and will not be overwritten"
        ) from error
    return output_path


def parse_args(argv: Sequence[str] | None = None) -> argparse.Namespace:
    """Parse every machine-specific input as a required command-line argument."""

    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument("--data-root", required=True, type=Path)
    parser.add_argument("--sweep-result", required=True, type=Path)
    parser.add_argument("--sweep-result-sha256", required=True)
    parser.add_argument("--approved-plan", required=True, type=Path)
    parser.add_argument("--approved-anchor-analysis", required=True, type=Path)
    parser.add_argument("--run-root", required=True, type=Path)
    parser.add_argument("--anchor-checkpoint-dir", required=True, type=Path)
    parser.add_argument("--output-dir", required=True, type=Path)
    return parser.parse_args(argv)


def main(argv: Sequence[str] | None = None) -> int:
    """Run the bounded read, print its boundary, and write its artifact once."""

    args = parse_args(argv)
    try:
        report = analyze_paths(
            data_root=args.data_root,
            sweep_result_path=args.sweep_result,
            approved_plan_path=args.approved_plan,
            approved_anchor_analysis_path=args.approved_anchor_analysis,
            run_root=args.run_root,
            anchor_checkpoint_dir=args.anchor_checkpoint_dir,
            expected_sweep_result_sha256=args.sweep_result_sha256,
        )
        output_path = write_exclusive(args.output_dir, report)
    except (
        CapacitySweepAnalysisError,
        sweep.CapacitySweepError,
        sweep.DevFitContractError,
        OSError,
        ValueError,
    ) as error:
        print(f"{X_ANALYSIS_REFUSED}: {error}", flush=True)
        return EXIT_CODES[X_ANALYSIS_REFUSED]
    print(render(report), flush=True)
    print(f"wrote {output_path}", flush=True)
    return EXIT_CODES[X_ANALYSIS_OK]


if __name__ == "__main__":
    sys.exit(main())
