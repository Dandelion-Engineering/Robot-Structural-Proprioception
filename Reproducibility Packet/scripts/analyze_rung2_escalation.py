"""Derive the pre-declared descriptive read of one complete rung-2 escalation run.

This is step 6 of `protocol/rung2-escalation-v0.1.md` section 11 and invariant R7: a new
read-only script, separate from the rung-2 executable and from both approved analyzers.
It authenticates the approved plan and the terminal run record, refuses a partial run,
re-reads only the authorized development examples and the checkpoints the record names,
independently recomputes every stored rung-2 classification metric, and writes one
deterministic descriptive JSON artifact carrying exactly design section 5.2's derived
fields.

Invariant R7 also requires this file to **import** from `analyze_dev_fit.py` and
`analyze_capacity_sweep.py` rather than restate them; both are jointly approved and
neither is edited here. Invariant R10 is enforced in two places: the run must be
complete before anything is derived, and every paired-sign and rung-comparison field is
suppressed unless the objective-reduction status passes.

The script performs no optimization, writes no checkpoint, reads no pilot, validation or
test outcome, generates no data, spends no rollout, selects no capacity, rung or
threshold, and emits none of section 5.4's interpretation prose. Building and reviewing
this file is not permission to run it; execution and exact-state review remain separate
gates.
"""

from __future__ import annotations

import argparse
import json
import sys
from collections import Counter
from decimal import Decimal
from pathlib import Path
from typing import Any, Mapping, Sequence

import torch

import analyze_dev_fit as approved_analysis
from analyze_capacity_sweep import (
    CapacitySweepAnalysisError,
    finite_number,
    observed,
    safe_relative_path,
    sha256_digest,
    strict_object,
    unit_interval,
)
import analyze_capacity_sweep as approved_sweep_analysis
from utils import rung2_escalation as rung2
from utils.attribution_net import deterministic_conv_precision
from utils.dev_fit_contract import code_identity
from utils.protocol_p import canonical_text_sha256
from utils.capacity_sweep import quantize


OUTPUT_NAME = "rung2_escalation_analysis.json"
X_ANALYSIS_OK = "X_ANALYSIS_OK"
X_ANALYSIS_REFUSED = "X_ANALYSIS_REFUSED"
EXIT_CODES = {X_ANALYSIS_OK: 0, X_ANALYSIS_REFUSED: 3}

ANALYSIS_AUTHORITY = (
    "DEVELOPMENT-ONLY DESCRIPTIVE READ: in-sample rung-2 escalation under the frozen "
    "rung-1 protocol; not held-out evidence, not a rung, capacity or threshold "
    "selection, and not a C1-versus-S conclusion"
)


class Rung2AnalysisError(CapacitySweepAnalysisError):
    """This reader's own diagnosis: the supplied exact state cannot support the read.

    It subclasses the approved capacity reader's error for the same reason
    `Rung2EscalationError` subclasses `CapacitySweepError`: every helper imported from
    `analyze_capacity_sweep` raises that class, so a separate root would force every
    handler to name two families for one condition, and the handler that named only one
    would be the defect. `type(error).__name__` still records which class fired.
    """


def require(condition: bool, message: str) -> None:
    """Raise ``Rung2AnalysisError`` unless ``condition`` holds."""

    if not condition:
        raise Rung2AnalysisError(message)


def analysis_code_identity() -> dict[str, str]:
    """Identify this reader and every bound production module it executes through.

    Inputs: none. Outputs: `{bare label: canonical text digest}`, sorted. Purpose: the
    run's own twelve-entry producing identity plus the two read-only analyzers this file
    executes through -- itself and the approved capacity reader. `analyze_dev_fit.py` is
    already one of the twelve, so it is not added twice.
    """

    identity = dict(rung2.rung2_code_identity())
    identity.update(
        code_identity(
            {
                "analyze_rung2_escalation.py": Path(__file__).resolve(),
                "analyze_capacity_sweep.py": Path(
                    approved_sweep_analysis.__file__
                ).resolve(),
            }
        )
    )
    return dict(sorted(identity.items()))


def validate_code_identity(value: Any, label: str) -> dict[str, str]:
    """Return a non-empty, sorted module-to-digest identity map."""

    require(isinstance(value, Mapping) and bool(value), f"{label} carries no code identity")
    parsed: dict[str, str] = {}
    for name, digest in value.items():
        require(isinstance(name, str) and bool(name), f"{label} has a malformed module name")
        parsed[name] = sha256_digest(digest, f"{label} identity for {name}")
    return dict(sorted(parsed.items()))


def finite_history(value: Any, label: str) -> list[float]:
    """Return one per-epoch loss history as finite floats, refusing an empty list."""

    require(isinstance(value, list) and bool(value), f"{label} carries no loss history")
    return [finite_number(entry, f"{label} loss-history value") for entry in value]


def sign_counts(differences: Sequence[float]) -> dict[str, int]:
    """Count negative, zero and positive differences at the declared quantization.

    Inputs: the per-seed paired differences. Outputs: `{negative, zero, positive}`.
    Purpose: design section 5.2's `sign_count`. The classification happens at the frozen
    six-decimal tie rule, not at float64's, so a tie is a tie at the resolution the
    design declared. The three counts are a description of five signs and nothing else.
    """

    require(bool(differences), "a sign count needs at least one seed difference")
    zero = Decimal(0)
    counts = {"negative": 0, "positive": 0, "zero": 0}
    for value in differences:
        quantized = Decimal(quantize(value))
        if quantized < zero:
            counts["negative"] += 1
        elif quantized > zero:
            counts["positive"] += 1
        else:
            counts["zero"] += 1
    return counts


def label_from_sign_counts(counts: Mapping[str, int]) -> str:
    """Return design section 5.2's three-valued label from persisted sign counts alone.

    Inputs: one `sign_count` block. Outputs: the same three names
    `rung2_escalation.deficit_sign_label` produces. Purpose: this is the *second*,
    independent route to the label -- the first derives it from the differences
    themselves. The artifact records the label produced from the differences and this
    function re-derives it from the counts the artifact persists, so a reader who has
    only the artifact can check the label, and so the two routes disagreeing is a
    refusal rather than a silently published name.
    """

    total = sum(int(counts[name]) for name in ("negative", "positive", "zero"))
    require(total > 0, "a sign label needs at least one counted seed")
    if counts["negative"] == total:
        return rung2.SIGN_REPRODUCED
    if counts["negative"] == 0:
        return rung2.SIGN_NOT_REPRODUCED
    return rung2.SIGN_MIXED


def validate_envelope(
    result: Mapping[str, Any],
    equivalence_document: Mapping[str, Any],
    plan: Mapping[str, Any],
    anchor_analysis: Mapping[str, Any],
    *,
    digests: Mapping[str, str],
) -> None:
    """Authenticate the complete terminal record, its plan, design and gate evidence."""

    try:
        rung2.require_complete_rung2_run(result)
    except (rung2.DevFitContractError, rung2.CapacitySweepError) as error:
        raise Rung2AnalysisError("the terminal record is not a complete rung-2 run") from error

    require(result.get("exit") == rung2.X_RUNG2_OK, "the run did not take X_RUNG2_OK")
    require(result.get("mode") == "execute", "the run record is not execute mode")
    require(result.get("reason_class") is None, "the successful run carries a refusal reason")
    require(
        result.get("authority") == rung2.RUNG2_AUTHORITY,
        "the run record carries the wrong authority",
    )
    require(plan.get("exit") == rung2.X_PLAN_OK, "the plan did not take X_PLAN_OK")
    require(plan.get("mode") == "plan", "the approved plan is not plan mode")
    require(plan.get("plan_valid") is True, "the approved plan is not valid")
    require(
        plan.get("authority") == rung2.RUNG2_AUTHORITY,
        "the approved plan carries the wrong authority",
    )
    require(
        result.get("rung") == rung2.RUNG2_NAME and plan.get("rung") == rung2.RUNG2_NAME,
        "the supplied exact state does not name the rung-2 architecture",
    )
    require(
        result.get("approved_plan_sha256") == digests["approved_plan"],
        "the terminal record is not bound to the supplied approved plan",
    )
    require(
        result.get("run_label") == plan.get("run_label"),
        "the terminal record and approved plan name different runs",
    )
    for document, label in ((result, "terminal record"), (plan, "approved plan")):
        require(
            document.get("approved_analysis_sha256") == digests["approved_anchor_analysis"],
            f"the {label} is not bound to the supplied approved anchor analysis",
        )
        require(
            document.get("approved_fit_ledger_sha256") == digests["approved_fit_ledger"],
            f"the {label} is not bound to the supplied approved fit ledger",
        )

    design_sha256 = rung2.design_digest()
    require(
        design_sha256 == rung2.DESIGN_CANONICAL_SHA256,
        "the frozen rung-2 design no longer matches its pinned digest",
    )
    require(
        result.get("design_sha256") == design_sha256
        and plan.get("design_sha256") == design_sha256,
        "the supplied exact state is not bound to the frozen rung-2 design",
    )
    current_identity = rung2.rung2_code_identity()
    require(
        validate_code_identity(result.get("code_identity"), "terminal record")
        == current_identity,
        "the terminal record names a different producing code state",
    )
    require(
        validate_code_identity(plan.get("code_identity"), "approved plan")
        == current_identity,
        "the approved plan names a different producing code state",
    )
    try:
        rung2.require_approved_analyzer_identity(anchor_analysis)
    except (rung2.DevFitContractError, rung2.CapacitySweepError) as error:
        raise Rung2AnalysisError(
            "the approved first-fit analyzer no longer matches its recorded identity"
        ) from error

    require(
        result.get("fits_attempted") == rung2.MAX_FITS
        and result.get("checkpoints_written") == rung2.MAX_CHECKPOINTS
        and result.get("rung2_fits_attempted") == len(rung2.rung2_arms())
        and result.get("rung2_checkpoints_written") == len(rung2.rung2_arms())
        and result.get("equivalence_fits_attempted") == len(rung2.EQUIVALENCE_ARMS)
        and result.get("equivalence_checkpoints_written") == len(rung2.EQUIVALENCE_ARMS),
        "the terminal resource counts do not equal the complete frozen run",
    )
    for document, label in ((result, "terminal record"), (plan, "approved plan")):
        budget = document.get("maximum_budget")
        require(isinstance(budget, Mapping), f"the {label} carries no maximum budget")
        require(
            budget.get("fits") == rung2.MAX_FITS
            and budget.get("checkpoints") == rung2.MAX_CHECKPOINTS
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
    require(
        result.get("training_protocol") == plan.get("training_protocol"),
        "the training protocol differs between the approved plan and the run record",
    )
    census = result.get("data_census")
    require(isinstance(census, Mapping), "the terminal record carries no data census")
    require(
        census.get("manifest_sha256") == plan.get("manifest_sha256")
        and census.get("assignment_sha256") == plan.get("assignment_sha256"),
        "the terminal data census differs from the approved plan",
    )

    # The gate evidence is a separate artifact under the reserved subtree, so the two
    # documents are cross-checked rather than trusted separately.
    require(
        equivalence_document.get("gate_passed") is True,
        "the equivalence gate evidence does not record a passed gate",
    )
    require(
        equivalence_document.get("authority") == rung2.RUNG2_AUTHORITY,
        "the equivalence artifact carries the wrong authority",
    )
    require(
        equivalence_document.get("equivalence_channels") == rung2.ANCHOR_CHANNELS
        and equivalence_document.get("equivalence_rung") == rung2.RUNG1_NAME,
        "the equivalence artifact does not describe the approved rung-1 anchor",
    )
    require(
        equivalence_document.get("fits_attempted") == len(rung2.EQUIVALENCE_ARMS)
        and equivalence_document.get("checkpoints_written") == len(rung2.EQUIVALENCE_ARMS),
        "the equivalence artifact carries the wrong fit or checkpoint count",
    )
    require(
        equivalence_document.get("generation_runs") == 0
        and equivalence_document.get("non_dev_reads") == 0
        and equivalence_document.get("rollouts_spent") == 0,
        "the equivalence artifact crossed the development-only resource boundary",
    )
    require(
        validate_code_identity(
            equivalence_document.get("code_identity"), "equivalence artifact"
        )
        == current_identity,
        "the equivalence artifact names a different producing code state",
    )
    require(
        equivalence_document.get("arms") == result.get("equivalence_arms"),
        "the equivalence artifact and the terminal record disagree about the gate arms",
    )


def validate_rung2_arm(
    arm: Mapping[str, Any],
    *,
    shape: Mapping[str, Any],
    epochs: int,
    run_identity: Mapping[str, str],
) -> dict[str, Any]:
    """Validate and normalize one persisted rung-2 arm without interpreting its scores."""

    require(isinstance(arm, Mapping), "a rung-2 arm is not an object")
    suite = arm.get("suite")
    seed = arm.get("seed")
    require(suite in rung2.MATCHED_FIT_SUITES, "a rung-2 arm carries an invalid suite")
    require(
        isinstance(seed, int)
        and not isinstance(seed, bool)
        and seed in rung2.PREDECLARED_TRAINING_SEEDS,
        "a rung-2 arm carries an invalid seed",
    )
    require(arm.get("status") == rung2.ARM_COMPLETED, "a rung-2 arm is not completed")
    require(arm.get("rung") == rung2.RUNG2_NAME, "a rung-2 arm carries the wrong rung name")
    require(
        arm.get("source") == "rung2-escalation", "a rung-2 arm carries the wrong provenance"
    )
    require(
        arm.get("n_parameters") == shape["n_parameters"],
        "a rung-2 arm carries the wrong parameter count",
    )
    require(
        arm.get("stem_receptive_field") == shape["stem_receptive_field"],
        "a rung-2 arm carries the wrong stem receptive field",
    )
    n_examples = arm.get("n_examples")
    require(
        isinstance(n_examples, int) and not isinstance(n_examples, bool) and n_examples > 0,
        "a rung-2 arm carries no positive example count",
    )
    accuracy = unit_interval(arm.get("accuracy"), "rung-2 accuracy")
    macro_f1 = unit_interval(arm.get("macro_f1"), "rung-2 macro-F1")
    per_class = arm.get("per_class_f1")
    classes = tuple(approved_analysis.SOURCE_CLASS_ORDER)
    require(
        isinstance(per_class, Mapping) and set(per_class) == set(classes),
        "a rung-2 arm carries the wrong per-class F1 universe",
    )
    parsed_per_class = {
        name: unit_interval(per_class[name], f"rung-2 {name} F1") for name in classes
    }
    history = finite_history(arm.get("loss_history"), "rung-2 arm")
    require(
        len(history) == epochs,
        "a rung-2 arm carries the wrong loss-history length",
    )
    require(
        arm.get("first_epoch_loss") == history[0]
        and arm.get("final_epoch_loss") == history[-1],
        "a rung-2 arm's recorded epoch endpoints differ from its loss history",
    )
    # Recomputed from the history rather than trusted: the flag is section 5.1's whole
    # stop-or-go gate, and a persisted boolean that nothing re-derives is a claim.
    require(
        arm.get("objective_reduced") is rung2.arm_objective_reduced(history),
        "a rung-2 arm's objective-reduction flag is not what its loss history implies",
    )
    relative = arm.get("checkpoint_relative_name")
    require(
        isinstance(relative, str)
        and relative == rung2.rung2_checkpoint_name(str(suite), int(seed)),
        "a rung-2 arm names a checkpoint the approved name rule does not produce",
    )
    require(
        validate_code_identity(arm.get("fit_code_identity"), "rung-2 arm") == dict(run_identity),
        "a rung-2 arm carries the wrong fitting-code identity",
    )
    return {
        "accuracy": accuracy,
        "checkpoint_relative_name": relative,
        "checkpoint_sha256": sha256_digest(
            arm.get("checkpoint_sha256"), "rung-2 checkpoint digest"
        ),
        "final_epoch_loss": history[-1],
        "first_epoch_loss": history[0],
        "fit_code_identity": dict(run_identity),
        "loss_history": history,
        "macro_f1": macro_f1,
        "n_examples": n_examples,
        "n_parameters": arm["n_parameters"],
        "objective_reduced": bool(arm["objective_reduced"]),
        "per_class_f1": parsed_per_class,
        "rung": rung2.RUNG2_NAME,
        "seed": int(seed),
        "source": "rung2-escalation",
        "status": rung2.ARM_COMPLETED,
        "stem_receptive_field": arm["stem_receptive_field"],
        "suite": str(suite),
    }


def validate_rung2_arms(
    result: Mapping[str, Any], *, shape: Mapping[str, Any]
) -> list[dict[str, Any]]:
    """Validate all ten rung-2 arms and require exactly the predeclared identities."""

    rows = result.get("rung2_arms")
    require(isinstance(rows, list), "the terminal record carries no rung-2 arms")
    protocol = result.get("training_protocol")
    require(isinstance(protocol, Mapping), "the terminal record carries no training protocol")
    epochs = protocol.get("epochs")
    require(
        isinstance(epochs, int) and not isinstance(epochs, bool) and epochs > 0,
        "the terminal training protocol carries no positive epoch count",
    )
    run_identity = validate_code_identity(result.get("code_identity"), "terminal record")
    arms = [
        validate_rung2_arm(row, shape=shape, epochs=epochs, run_identity=run_identity)
        for row in rows
    ]
    keys = [(arm["suite"], arm["seed"]) for arm in arms]
    require(
        len(keys) == len(rung2.rung2_arms()) and set(keys) == set(rung2.rung2_arms()),
        "the rung-2 arm identities are not exactly the ten predeclared arms",
    )
    digests = {arm["checkpoint_sha256"] for arm in arms}
    require(len(digests) == len(arms), "two rung-2 arms name the same checkpoint digest")
    suite_order = {name: index for index, name in enumerate(rung2.MATCHED_FIT_SUITES)}
    return sorted(arms, key=lambda arm: (suite_order[arm["suite"]], arm["seed"]))


def validate_equivalence_arms(
    result: Mapping[str, Any], ledger: Mapping[str, Any]
) -> list[dict[str, Any]]:
    """Validate both gate arms and bind each to the approved ledger's own digest."""

    rows = result.get("equivalence_arms")
    require(isinstance(rows, list), "the terminal record carries no equivalence arms")
    ledger_arms = ledger.get("arms")
    require(isinstance(ledger_arms, list), "the approved fit ledger carries no arms")
    by_key: dict[tuple[str, int], Mapping[str, Any]] = {}
    for row in ledger_arms:
        require(isinstance(row, Mapping), "the approved fit ledger carries a non-object arm")
        key = (row.get("suite"), row.get("training_seed"))
        require(key not in by_key, "the approved fit ledger duplicates an arm")
        by_key[key] = row

    parsed: list[dict[str, Any]] = []
    for entry in rows:
        require(isinstance(entry, Mapping), "an equivalence arm is not an object")
        suite = entry.get("suite")
        seed = entry.get("seed")
        require(
            (suite, seed) in rung2.EQUIVALENCE_ARMS,
            "an equivalence arm is not one of the two ruled identities",
        )
        require(
            entry.get("status") == rung2.ARM_COMPLETED
            and entry.get("equivalence_status") == rung2.COMPARISON_PASS,
            "an equivalence arm did not complete and pass",
        )
        require(entry.get("reason_class") is None, "a passing equivalence arm carries a reason")
        require(
            entry.get("channels") == rung2.ANCHOR_CHANNELS
            and entry.get("rung") == rung2.RUNG1_NAME,
            "an equivalence arm does not describe the approved rung-1 anchor",
        )
        require(
            entry.get("weights_bit_identical") is True
            and entry.get("loss_history_bit_identical") is True,
            "an equivalence arm records a comparison that did not hold",
        )
        approved_history = finite_history(
            entry.get("approved_loss_history"), "equivalence approved"
        )
        refit_history = finite_history(entry.get("refit_loss_history"), "equivalence refit")
        # The persisted booleans are recomputed from the persisted histories, so the
        # gate's own claim is re-derived rather than read back.
        require(
            approved_history == refit_history,
            "an equivalence arm's two loss histories are not identical after all",
        )
        ledger_arm = by_key.get((suite, seed))
        require(
            isinstance(ledger_arm, Mapping),
            "the approved fit ledger carries no row for an equivalence arm",
        )
        require(
            entry.get("rung1_reference_checkpoint_sha256")
            == ledger_arm.get("checkpoint_sha256"),
            "an equivalence arm names a reference checkpoint the approved ledger does not",
        )
        relative = entry.get("refit_checkpoint_relative_name")
        require(
            isinstance(relative, str)
            and relative == rung2.equivalence_relative_name(str(suite), int(seed)),
            "an equivalence arm names a refit checkpoint the approved name rule does not "
            "produce",
        )
        parsed.append(
            {
                "approved_loss_history": approved_history,
                "channels": rung2.ANCHOR_CHANNELS,
                "equivalence_status": rung2.COMPARISON_PASS,
                "loss_history_bit_identical": True,
                "refit_checkpoint_relative_name": relative,
                "refit_checkpoint_sha256": sha256_digest(
                    entry.get("refit_checkpoint_sha256"), "equivalence refit digest"
                ),
                "refit_loss_history": refit_history,
                "rung": rung2.RUNG1_NAME,
                "rung1_reference_checkpoint_sha256": sha256_digest(
                    entry.get("rung1_reference_checkpoint_sha256"),
                    "equivalence reference digest",
                ),
                "seed": int(seed),
                "status": rung2.ARM_COMPLETED,
                "suite": str(suite),
                "weights_bit_identical": True,
            }
        )
    keys = [(entry["suite"], entry["seed"]) for entry in parsed]
    require(
        len(keys) == len(rung2.EQUIVALENCE_ARMS) and set(keys) == set(rung2.EQUIVALENCE_ARMS),
        "the equivalence arm identities are not exactly the two ruled arms",
    )
    return sorted(parsed, key=lambda entry: (entry["suite"], entry["seed"]))


def validate_anchor_arms(
    result: Mapping[str, Any],
    ledger: Mapping[str, Any],
    anchor_analysis: Mapping[str, Any],
) -> list[dict[str, Any]]:
    """Re-read every anchor number from the approved analysis by its recorded field path.

    Inputs: the terminal record and both approved rung-1 documents. Outputs: the ten
    read-only anchor records, normalized. Purpose: design section 5.2 says the approved
    rung-1 numbers are **read, never recomputed**. That makes the record's copy of them
    the only route into this analysis, so the copy is re-fetched from its named source
    document rather than trusted -- and the checkpoint digest is cross-checked against
    the ledger, whose row is a different file from the analysis's.
    """

    rows = result.get("anchor_arms")
    require(isinstance(rows, list), "the terminal record carries no anchor arms")
    source = rung2.anchor_records(ledger, anchor_analysis)
    by_key = {(entry["suite"], entry["seed"]): entry for entry in source}
    parsed: list[dict[str, Any]] = []
    seen: set[tuple[str, int]] = set()
    for entry in rows:
        require(isinstance(entry, Mapping), "an anchor arm is not an object")
        key = (entry.get("suite"), entry.get("seed"))
        require(key in by_key, "an anchor arm is not one of the ten approved identities")
        require(key not in seen, "the terminal record duplicates an anchor arm")
        seen.add(key)  # type: ignore[arg-type]
        expected = by_key[key]  # type: ignore[index]
        require(
            dict(entry) == dict(expected),
            "an anchor arm differs from the approved rung-1 records it was read from",
        )
        macro_f1 = unit_interval(entry.get("macro_f1"), "anchor macro-F1")
        per_class = entry.get("per_class_f1")
        classes = tuple(approved_analysis.SOURCE_CLASS_ORDER)
        require(
            isinstance(per_class, Mapping) and set(per_class) == set(classes),
            "an anchor arm carries the wrong per-class F1 universe",
        )
        parsed.append(
            {
                "checkpoint_sha256": sha256_digest(
                    entry.get("checkpoint_sha256"), "anchor checkpoint digest"
                ),
                "macro_f1": macro_f1,
                "macro_f1_field": entry["macro_f1_field"],
                "per_class_f1": {
                    name: unit_interval(per_class[name], f"anchor {name} F1")
                    for name in classes
                },
                "per_class_f1_field": entry["per_class_f1_field"],
                "read_only": True,
                "rung": rung2.RUNG1_NAME,
                "seed": int(entry["seed"]),
                "source": "approved-analysis",
                "suite": str(entry["suite"]),
            }
        )
    require(len(seen) == len(by_key), "the terminal record omits an approved anchor arm")
    suite_order = {name: index for index, name in enumerate(rung2.MATCHED_FIT_SUITES)}
    return sorted(parsed, key=lambda entry: (suite_order[entry["suite"]], entry["seed"]))


def load_development_context(
    *, data_root: Path, result: Mapping[str, Any], anchor_analysis: Mapping[str, Any]
) -> tuple[dict[str, list[Any]], dict[str, Any]]:
    """Load only the authorized dev examples and authenticate their shared context."""

    try:
        examples_by_suite, census = approved_analysis.load_authorized_examples(Path(data_root))
    except approved_analysis.DevFitAnalysisError as error:
        raise Rung2AnalysisError("the authorized dev examples failed closed") from error
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


def evaluate_rung2_arm(
    arm: Mapping[str, Any], examples: Sequence[Any], checkpoint: Path
) -> dict[str, float]:
    """Authenticate one checkpoint, recompute its metrics, and return its loss terms.

    Every rung-2 arm's scores reach the terminal record through `capacity_sweep.score_arm`
    without rounding, so they are compared **exactly** -- the strongest available check.
    Finding AV's domain problem does not arise here: the anchors are never recomputed at
    all in this read, and the ten rung-2 arms all come from one writer.
    """

    checkpoint = Path(checkpoint)
    require(checkpoint.is_file(), "a checkpoint named by the terminal record is absent")
    require(
        rung2.trainer.file_sha256(checkpoint) == arm["checkpoint_sha256"],
        "a checkpoint differs from the digest in the terminal record",
    )
    # `build_rung2_network` is the executable's one construction site for this
    # architecture; a second constructor call here would be a second definition of the
    # network under review, outside the reach of the tests that pin that one.
    network = rung2.build_rung2_network(seed=arm["seed"])
    try:
        state = torch.load(checkpoint, map_location="cpu", weights_only=True)
        network.load_state_dict(state, strict=True)
    except (OSError, RuntimeError, TypeError, ValueError) as error:
        raise Rung2AnalysisError("a rung-2 checkpoint cannot be loaded") from error

    metrics = rung2.score_arm(network, examples)
    stored = {
        "accuracy": arm["accuracy"],
        "macro_f1": arm["macro_f1"],
        "per_class_f1": arm["per_class_f1"],
    }
    require(
        {key: metrics[key] for key in stored} == stored,
        "a recomputed checkpoint score differs from the terminal record",
    )
    batch = rung2._stack(examples, torch.device("cpu"))
    network.eval()
    with torch.no_grad(), deterministic_conv_precision():
        heads = network(batch["inputs"])
        loss_terms = approved_analysis.post_fit_loss_terms(heads, batch)
    return {
        key: finite_number(value, f"post-fit {key}") for key, value in loss_terms.items()
    }


def evaluate_all_arms(
    arms: Sequence[Mapping[str, Any]],
    *,
    examples_by_suite: Mapping[str, Sequence[Any]],
    run_root: Path,
) -> dict[tuple[str, int], dict[str, float]]:
    """Recompute every rung-2 arm's stored score and return its post-fit loss context."""

    evaluated: dict[tuple[str, int], dict[str, float]] = {}
    for arm in arms:
        key = (arm["suite"], arm["seed"])
        require(key not in evaluated, "the analysis attempted to evaluate one arm twice")
        checkpoint = safe_relative_path(
            Path(run_root), str(arm["checkpoint_relative_name"]), "rung-2 checkpoint name"
        )
        evaluated[key] = evaluate_rung2_arm(arm, examples_by_suite[arm["suite"]], checkpoint)
    return evaluated


def verify_equivalence_checkpoints(
    equivalence: Sequence[Mapping[str, Any]], *, run_root: Path
) -> None:
    """Bind each gate arm's persisted digest to the bytes still on disk.

    The gate's own comparison ran inside the executable and is gone; what survives is a
    record naming a file. Re-digesting that file is the only thing in this read that
    makes the record's `refit_checkpoint_sha256` a statement about the packet rather
    than about a run nobody can re-open. The re-fit weights are not loaded or scored --
    the comparison they exist for was made once, under authorization, and repeating it
    would be a thirteenth fit.
    """

    for entry in equivalence:
        checkpoint = safe_relative_path(
            Path(run_root),
            str(entry["refit_checkpoint_relative_name"]),
            "equivalence refit checkpoint name",
        )
        require(
            checkpoint.is_file(),
            "an equivalence refit checkpoint named by the record is absent",
        )
        require(
            rung2.trainer.file_sha256(checkpoint) == entry["refit_checkpoint_sha256"],
            "an equivalence refit checkpoint differs from the digest in the record",
        )


def _difference_block(
    per_seed: Sequence[Mapping[str, Any]], differences: Sequence[float]
) -> dict[str, Any]:
    """Return one paired metric's per-seed rows, mean, sample SD and sign counts."""

    return {
        "mean": observed(approved_analysis.arithmetic_mean(list(differences))),
        "per_seed": list(per_seed),
        "sample_sd": observed(approved_analysis.sample_standard_deviation(list(differences))),
        "sign_count": sign_counts(differences),
    }


def paired_s_minus_c1(arms: Sequence[Mapping[str, Any]]) -> dict[str, Any]:
    """Derive design section 5.2's paired `S - C1` block at rung 2, metric by metric."""

    by_key = {(arm["suite"], arm["seed"]): arm for arm in arms}
    seeds = list(rung2.PREDECLARED_TRAINING_SEEDS)

    def _one(reader) -> dict[str, Any]:
        rows: list[dict[str, Any]] = []
        differences: list[float] = []
        for seed in seeds:
            c1_value = reader(by_key[("C1", seed)])
            s_value = reader(by_key[("S", seed)])
            difference = s_value - c1_value
            differences.append(difference)
            rows.append(
                {
                    "C1": c1_value,
                    "S": s_value,
                    "S_minus_C1": observed(difference),
                    "seed": seed,
                }
            )
        return _difference_block(rows, differences)

    return {
        "macro_f1": _one(lambda arm: arm["macro_f1"]),
        "per_class_f1": {
            name: _one(lambda arm, name=name: arm["per_class_f1"][name])
            for name in approved_analysis.SOURCE_CLASS_ORDER
        },
    }


def rung2_minus_rung1(
    arms: Sequence[Mapping[str, Any]], anchors: Sequence[Mapping[str, Any]]
) -> dict[str, Any]:
    """Derive design section 5.2's per-suite rung difference on macro-F1.

    These are **record contents**. Section 5.3 forbids asserting a trend, slope or
    direction across two rungs and no section 5.4 row licenses a sentence about them;
    persisting the primitives is explicitly permitted by the same paragraph.
    """

    rung2_by_key = {(arm["suite"], arm["seed"]): arm for arm in arms}
    rung1_by_key = {(arm["suite"], arm["seed"]): arm for arm in anchors}
    block: dict[str, Any] = {}
    for suite in rung2.MATCHED_FIT_SUITES:
        rows: list[dict[str, Any]] = []
        differences: list[float] = []
        for seed in rung2.PREDECLARED_TRAINING_SEEDS:
            rung1_value = rung1_by_key[(suite, seed)]["macro_f1"]
            rung2_value = rung2_by_key[(suite, seed)]["macro_f1"]
            difference = rung2_value - rung1_value
            differences.append(difference)
            rows.append(
                {
                    "rung1_macro_f1": rung1_value,
                    "rung2_macro_f1": rung2_value,
                    "rung2_minus_rung1": observed(difference),
                    "seed": seed,
                }
            )
        block[suite] = {
            "mean": observed(approved_analysis.arithmetic_mean(differences)),
            "per_seed": rows,
            "sample_sd": observed(
                approved_analysis.sample_standard_deviation(differences)
            ),
        }
    return block


def derive_analysis(
    *,
    result: Mapping[str, Any],
    arms: Sequence[Mapping[str, Any]],
    anchors: Sequence[Mapping[str, Any]],
    equivalence: Sequence[Mapping[str, Any]],
    loss_context: Mapping[tuple[str, int], Mapping[str, float]],
    shared_context: Mapping[str, Any],
    input_digests: Mapping[str, str],
) -> dict[str, Any]:
    """Derive exactly section 5.2's descriptive fields from verified persisted primitives."""

    require(
        set(loss_context) == {(arm["suite"], arm["seed"]) for arm in arms},
        "the loss context does not cover every rung-2 arm",
    )
    term_sets = {tuple(sorted(terms)) for terms in loss_context.values()}
    require(
        len(term_sets) == 1 and bool(next(iter(term_sets))),
        "the post-fit loss context does not carry one common non-empty term set",
    )
    loss_terms = next(iter(term_sets))

    reported_arms = [
        dict(arm, post_fit_full_batch_loss_terms=dict(loss_context[(arm["suite"], arm["seed"])]))
        for arm in arms
    ]
    mean_loss_terms = {
        suite: {
            term: approved_analysis.arithmetic_mean(
                [
                    loss_context[(suite, seed)][term]
                    for seed in rung2.PREDECLARED_TRAINING_SEEDS
                ]
            )
            for term in loss_terms
        }
        for suite in rung2.MATCHED_FIT_SUITES
    }

    # Invariant R10, second half. The status is derived FIRST, from the terminal record
    # through the executable's own imported predicate, and every paired-sign and
    # rung-comparison field below is suppressed unless it passes.
    status = rung2.optimization_check_status(result)
    reduced = [arm for arm in arms if arm["objective_reduced"]]
    check_block = {
        "completed_rung2_arms": len(arms),
        "equivalence_arms_passed": len(equivalence),
        "objective_reduced_arms": len(reduced),
        "status": status,
    }
    passed = status == rung2.OPTIMIZATION_CHECK_PASSED

    paired = paired_s_minus_c1(arms) if passed else None
    rung_difference = rung2_minus_rung1(arms, anchors) if passed else None
    label: str | None = None
    if passed:
        macro_differences = [
            row["S_minus_C1"]["raw"] for row in paired["macro_f1"]["per_seed"]
        ]
        label = rung2.deficit_sign_label(macro_differences)

    report = {
        "anchor_arms": [dict(entry) for entry in anchors],
        "arms": reported_arms,
        "authority": ANALYSIS_AUTHORITY,
        "boundary": {
            "capacity_selected": False,
            "checkpoints_written": 0,
            "development_only": True,
            "fits_run": 0,
            "generalization_established": False,
            "generation_runs": 0,
            "in_sample": True,
            "non_dev_reads": 0,
            "rollouts_spent": 0,
            "rung_selected": False,
            "threshold_selected": False,
        },
        "deficit_sign_reproduced": label,
        "development_context": {
            "baselines": dict(shared_context["baselines"]),
            "class_counts_by_suite": dict(shared_context["class_counts_by_suite"]),
            "mean_post_fit_full_batch_loss_terms_by_suite": mean_loss_terms,
            "ood_counts_by_suite": dict(shared_context["ood_counts_by_suite"]),
            "trajectory_census": shared_context["trajectory_census"],
        },
        "equivalence_arms": [dict(entry) for entry in equivalence],
        "inputs": {
            "analysis_code_identity": analysis_code_identity(),
            "approved_anchor_analysis_canonical_sha256": input_digests[
                "approved_anchor_analysis"
            ],
            "approved_fit_ledger_canonical_sha256": input_digests["approved_fit_ledger"],
            "approved_plan_canonical_sha256": input_digests["approved_plan"],
            "design_sha256": result["design_sha256"],
            "equivalence_artifact_canonical_sha256": input_digests["equivalence_artifact"],
            "fit_code_identity": dict(sorted(dict(result["code_identity"]).items())),
            "run_label": result["run_label"],
            "run_result_canonical_sha256": input_digests["run_result"],
        },
        "optimization_check": check_block,
        "paired_S_minus_C1": paired,
        "rung2_minus_rung1": rung_difference,
    }

    # Re-derive the label from the primitives the artifact PERSISTS, by a different
    # route than the one that produced it: the first route classified the five raw
    # differences, this one reads the three persisted counts.
    if passed:
        require(
            report["deficit_sign_reproduced"]
            == label_from_sign_counts(report["paired_S_minus_C1"]["macro_f1"]["sign_count"]),
            "the sign label is not recomputable from the persisted sign counts",
        )
    else:
        require(
            report["paired_S_minus_C1"] is None
            and report["rung2_minus_rung1"] is None
            and report["deficit_sign_reproduced"] is None,
            "a run that did not pass the objective check must publish no paired or rung "
            "comparison",
        )
    return report


def analyze_paths(
    *,
    data_root: Path,
    run_result_path: Path,
    equivalence_artifact_path: Path,
    approved_plan_path: Path,
    approved_fit_ledger_path: Path,
    approved_anchor_analysis_path: Path,
    run_root: Path,
    expected_run_result_sha256: str,
) -> dict[str, Any]:
    """Load, authenticate, re-score, and derive one complete descriptive analysis."""

    run_result_path = Path(run_result_path)
    equivalence_artifact_path = Path(equivalence_artifact_path)
    run_root = Path(run_root)
    require(
        run_result_path.resolve().parent == run_root.resolve()
        and run_result_path.name == rung2.RUN_ARTIFACT,
        "the run result is not the named terminal artifact at the supplied run root",
    )
    require(
        equivalence_artifact_path.resolve()
        == (run_root / rung2.EQUIVALENCE_SUBTREE / rung2.EQUIVALENCE_ARTIFACT).resolve(),
        "the equivalence artifact is not in the reserved subtree of the supplied run root",
    )
    result = strict_object(run_result_path, "rung-2 run result")
    equivalence_document = strict_object(equivalence_artifact_path, "equivalence artifact")
    plan = strict_object(approved_plan_path, "approved rung-2 plan")
    ledger = strict_object(approved_fit_ledger_path, "approved fit ledger")
    anchor_analysis = strict_object(
        approved_anchor_analysis_path, "approved first-fit analysis"
    )
    digests = {
        "approved_anchor_analysis": canonical_text_sha256(approved_anchor_analysis_path),
        "approved_fit_ledger": canonical_text_sha256(approved_fit_ledger_path),
        "approved_plan": canonical_text_sha256(approved_plan_path),
        "equivalence_artifact": canonical_text_sha256(equivalence_artifact_path),
        "run_result": canonical_text_sha256(run_result_path),
    }
    require(
        digests["run_result"]
        == sha256_digest(expected_run_result_sha256, "approved run-result digest"),
        "the run result differs from the exact state authorized for analysis",
    )
    validate_envelope(result, equivalence_document, plan, anchor_analysis, digests=digests)
    shape = rung2.rung2_shape()
    arms = validate_rung2_arms(result, shape=shape)
    equivalence = validate_equivalence_arms(result, ledger)
    anchors = validate_anchor_arms(result, ledger, anchor_analysis)
    examples_by_suite, shared_context = load_development_context(
        data_root=Path(data_root), result=result, anchor_analysis=anchor_analysis
    )
    verify_equivalence_checkpoints(equivalence, run_root=run_root)
    losses = evaluate_all_arms(
        arms, examples_by_suite=examples_by_suite, run_root=run_root
    )
    return derive_analysis(
        result=result,
        arms=arms,
        anchors=anchors,
        equivalence=equivalence,
        loss_context=losses,
        shared_context=shared_context,
        input_digests=digests,
    )


def render(report: Mapping[str, Any]) -> str:
    """Return a compact boundary-conscious summary of the descriptive artifact."""

    check = report["optimization_check"]
    return "\n".join(
        [
            "Gate-4 rung-2 escalation descriptive read (zero fits, zero rollouts)",
            f"rung-2 arms: {len(report['arms'])}; "
            f"equivalence arms: {len(report['equivalence_arms'])}; "
            f"anchors read: {len(report['anchor_arms'])}",
            f"objective-reduction status: {check['status']} "
            f"({check['objective_reduced_arms']} of {check['completed_rung2_arms']} arms)",
            f"paired macro-F1 sign label: {report['deficit_sign_reproduced']}",
            "BOUNDARY: development-only in-sample description; no rung, capacity or "
            "threshold selected.",
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
        raise Rung2AnalysisError(
            "the analysis output already exists and will not be overwritten"
        ) from error
    return output_path


def parse_args(argv: Sequence[str] | None = None) -> argparse.Namespace:
    """Parse every machine-specific input as a required command-line argument."""

    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument("--data-root", required=True, type=Path)
    parser.add_argument("--run-result", required=True, type=Path)
    parser.add_argument("--run-result-sha256", required=True)
    parser.add_argument("--equivalence-artifact", required=True, type=Path)
    parser.add_argument("--approved-plan", required=True, type=Path)
    parser.add_argument("--approved-fit-ledger", required=True, type=Path)
    parser.add_argument("--approved-anchor-analysis", required=True, type=Path)
    parser.add_argument("--run-root", required=True, type=Path)
    parser.add_argument("--output-dir", required=True, type=Path)
    return parser.parse_args(argv)


def main(argv: Sequence[str] | None = None) -> int:
    """Run the bounded read, print its boundary, and write its artifact once."""

    args = parse_args(argv)
    try:
        report = analyze_paths(
            data_root=args.data_root,
            run_result_path=args.run_result,
            equivalence_artifact_path=args.equivalence_artifact,
            approved_plan_path=args.approved_plan,
            approved_fit_ledger_path=args.approved_fit_ledger,
            approved_anchor_analysis_path=args.approved_anchor_analysis,
            run_root=args.run_root,
            expected_run_result_sha256=args.run_result_sha256,
        )
        output_path = write_exclusive(args.output_dir, report)
    except (
        CapacitySweepAnalysisError,
        rung2.CapacitySweepError,
        rung2.DevFitContractError,
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
