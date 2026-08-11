"""Tests for the step-6 read-only rung-2 escalation analysis.

No test in this file reads the completed run, the delivered dataset, or any checkpoint
the run produced. The pre-declared read is driven with synthetic persisted primitives;
path, digest and refusal behaviour are exercised in temporary directories. The
recomputation tests do construct and save a **freshly initialized, never-fitted** rung-2
network in a temporary directory and score it on four synthetic examples -- that is the
only way to give the score comparison an accept side, and it opens nothing the run
wrote. Building and testing the reader is not its separately gated execution.
"""

from __future__ import annotations

import ast
import copy
import hashlib
import json
import sys
from pathlib import Path

import pytest

PACKET_ROOT = Path(__file__).resolve().parents[1]
SCRIPTS_DIR = PACKET_ROOT / "scripts"
sys.path.insert(0, str(SCRIPTS_DIR))

import analyze_rung2_escalation as analysis  # noqa: E402
import analyze_dev_fit as approved_analysis  # noqa: E402
from utils import rung2_escalation as r2  # noqa: E402


LOSS_TERMS = (
    "class_cross_entropy",
    "location_cross_entropy",
    "ood_binary_cross_entropy",
    "severity_gaussian_nll",
    "severity_log_scale_mean",
    "total",
)
CLASSES = tuple(approved_analysis.SOURCE_CLASS_ORDER)
SHAPE = {"n_parameters": r2.RUNG2_DECLARED_PARAMETERS, "stem_receptive_field": 31}
EPOCHS = r2.RUNG2_EPOCHS
SYNTHETIC_IDENTITY = {"synthetic_fit.py": "b" * 64}


def _digest(tag: str) -> str:
    """Return a deterministic synthetic 64-hex digest for one label."""

    return hashlib.sha256(tag.encode("utf-8")).hexdigest()


def _history(first: float, last: float) -> list[float]:
    """Return a synthetic per-epoch history of the declared length."""

    step = (last - first) / (EPOCHS - 1)
    return [first + step * index for index in range(EPOCHS)]


def _macro(suite: str, seed: int) -> float:
    """Return a synthetic rung-2 macro-F1 with S strictly below C1 at every seed."""

    base = 0.60 + seed * 0.01
    return base if suite == "C1" else base - 0.02 - seed * 0.001


def _rung2_arm(suite: str, seed: int, *, macro_f1: float | None = None, reduced: bool = True) -> dict:
    """Return one completed rung-2 arm carrying every section 5.2 primitive."""

    value = _macro(suite, seed) if macro_f1 is None else macro_f1
    history = _history(2.5, 0.4) if reduced else _history(0.4, 2.5)
    return {
        "accuracy": min(1.0, value + 0.03),
        "checkpoint_relative_name": r2.rung2_checkpoint_name(suite, seed),
        "checkpoint_sha256": _digest(f"rung2-{suite}-{seed}"),
        "final_epoch_loss": history[-1],
        "first_epoch_loss": history[0],
        "fit_code_identity": dict(SYNTHETIC_IDENTITY),
        "loss_history": history,
        "macro_f1": value,
        "n_examples": 152,
        "n_parameters": SHAPE["n_parameters"],
        "objective_reduced": reduced,
        "per_class_f1": {name: value for name in CLASSES},
        "rung": r2.RUNG2_NAME,
        "seed": seed,
        "source": "rung2-escalation",
        "status": r2.ARM_COMPLETED,
        "stem_receptive_field": SHAPE["stem_receptive_field"],
        "suite": suite,
    }


def _equivalence_arm(suite: str, seed: int) -> dict:
    """Return one passing gate arm with identical approved and refit histories."""

    history = _history(3.0, -1.2)
    return {
        "approved_loss_history": list(history),
        "channels": r2.ANCHOR_CHANNELS,
        "equivalence_status": r2.COMPARISON_PASS,
        "fit_code_identity": dict(SYNTHETIC_IDENTITY),
        "loss_history_bit_identical": True,
        "reason_class": None,
        "refit_checkpoint_relative_name": r2.equivalence_relative_name(suite, seed),
        "refit_checkpoint_sha256": _digest(f"refit-{suite}-{seed}"),
        "refit_loss_history": list(history),
        "rung": r2.RUNG1_NAME,
        "rung1_reference_checkpoint_sha256": _digest(f"anchor-{suite}-{seed}"),
        "seed": seed,
        "status": r2.ARM_COMPLETED,
        "suite": suite,
        "weights_bit_identical": True,
    }


def _anchor_documents() -> tuple[dict, dict]:
    """Return a synthetic approved ledger and approved first-fit analysis."""

    ledger = {
        "arms": [
            {
                "checkpoint_name": f"dev_fit_{suite}_seed{seed}.pt",
                "checkpoint_sha256": _digest(f"anchor-{suite}-{seed}"),
                "suite": suite,
                "training_seed": seed,
            }
            for suite, seed in r2.rung2_arms()
        ]
    }
    analyzer_digest = r2.code_identity(
        {"analyze_dev_fit.py": Path(approved_analysis.__file__).resolve()}
    )["analyze_dev_fit.py"]
    analysis_document = {
        "arms": [
            {
                "checkpoint_sha256": _digest(f"anchor-{suite}-{seed}"),
                "classification": {
                    "macro_f1": 0.50 + seed * 0.01 + (0.0 if suite == "C1" else -0.01),
                    "per_class_f1": {
                        name: 0.50 + seed * 0.01 for name in CLASSES
                    },
                },
                "seed": seed,
                "suite": suite,
            }
            for suite, seed in r2.rung2_arms()
        ],
        "baselines": {"majority_class": "sensor", "majority_class_accuracy": 96 / 152},
        "data_census": {
            "class_counts_by_suite": {
                suite: {"actuator": 32, "healthy": 8, "sensor": 96, "structure": 16}
                for suite in r2.MATCHED_FIT_SUITES
            },
            "ood_counts_by_suite": {"C1": 0, "S": 0},
        },
        "inputs": {"analysis_code_identity": {"analyze_dev_fit.py": analyzer_digest}},
    }
    return ledger, analysis_document


def _protocol() -> dict:
    """Return the synthetic training protocol both documents must share."""

    return {
        "batch_size": r2.RUNG2_BATCH_SIZE,
        "device": r2.RUNG2_DEVICE,
        "epochs": EPOCHS,
        "learning_rate": r2.RUNG2_LEARNING_RATE,
        "split": "dev",
    }


def _budget() -> dict:
    """Return the frozen maximum budget both documents must carry."""

    return {
        "checkpoints": r2.MAX_CHECKPOINTS,
        "fits": r2.MAX_FITS,
        "generation_runs": 0,
        "non_dev_reads": 0,
        "rollouts": 0,
    }


def _result_document(*, reduced: bool = True, identity: dict | None = None) -> dict:
    """Return a complete synthetic terminal record."""

    ledger, analysis_document = _anchor_documents()
    arms = []
    for index, (suite, seed) in enumerate(r2.rung2_arms()):
        arms.append(_rung2_arm(suite, seed, reduced=reduced or index > 0))
    return {
        "anchor_arms": r2.anchor_records(ledger, analysis_document),
        "approved_analysis_sha256": _digest("approved-analysis"),
        "approved_fit_ledger_sha256": _digest("approved-ledger"),
        "approved_plan_sha256": _digest("approved-plan"),
        "authority": r2.RUNG2_AUTHORITY,
        "checkpoints_written": r2.MAX_CHECKPOINTS,
        "code_identity": dict(identity if identity is not None else SYNTHETIC_IDENTITY),
        "data_census": {
            "assignment_sha256": _digest("assignment"),
            "manifest_sha256": _digest("manifest"),
            "row_disclosure": "304 of 944 manifest rows selected",
            "trajectory_census": {"C1": 152, "S": 152},
        },
        "design_sha256": r2.DESIGN_CANONICAL_SHA256,
        "elapsed_s": 1274.6,
        "equivalence_arms": [
            _equivalence_arm(suite, seed) for suite, seed in r2.EQUIVALENCE_ARMS
        ],
        "equivalence_checkpoints_written": len(r2.EQUIVALENCE_ARMS),
        "equivalence_fits_attempted": len(r2.EQUIVALENCE_ARMS),
        "exit": r2.X_RUNG2_OK,
        "fits_attempted": r2.MAX_FITS,
        "generation_runs": 0,
        "maximum_budget": _budget(),
        "mode": "execute",
        "non_dev_reads": 0,
        "reason_class": None,
        "rollouts_spent": 0,
        "run_label": "synthetic-run",
        "rung": r2.RUNG2_NAME,
        "rung2_arms": arms,
        "rung2_checkpoints_written": len(r2.rung2_arms()),
        "rung2_fits_attempted": len(r2.rung2_arms()),
        "training_protocol": _protocol(),
    }


def _plan_document(result: dict) -> dict:
    """Return the synthetic approved plan bound to one terminal record."""

    return {
        "approved_analysis_sha256": result["approved_analysis_sha256"],
        "approved_fit_ledger_sha256": result["approved_fit_ledger_sha256"],
        "assignment_sha256": result["data_census"]["assignment_sha256"],
        "authority": r2.RUNG2_AUTHORITY,
        "code_identity": dict(result["code_identity"]),
        "design_sha256": result["design_sha256"],
        "exit": r2.X_PLAN_OK,
        "manifest_sha256": result["data_census"]["manifest_sha256"],
        "maximum_budget": _budget(),
        "mode": "plan",
        "plan_valid": True,
        "run_label": result["run_label"],
        "rung": r2.RUNG2_NAME,
        "training_protocol": _protocol(),
    }


def _equivalence_document(result: dict) -> dict:
    """Return the synthetic gate-evidence artifact for one terminal record."""

    return {
        "arms": copy.deepcopy(result["equivalence_arms"]),
        "authority": r2.RUNG2_AUTHORITY,
        "checkpoints_written": len(r2.EQUIVALENCE_ARMS),
        "code_identity": dict(result["code_identity"]),
        "equivalence_channels": r2.ANCHOR_CHANNELS,
        "equivalence_rung": r2.RUNG1_NAME,
        "fits_attempted": len(r2.EQUIVALENCE_ARMS),
        "gate_passed": True,
        "generation_runs": 0,
        "non_dev_reads": 0,
        "rollouts_spent": 0,
    }


def _shared_context() -> dict:
    """Return the synthetic development context the derivation reports."""

    return {
        "baselines": {"majority_class": "sensor", "majority_class_accuracy": 96 / 152},
        "class_counts_by_suite": {
            suite: {"actuator": 32, "healthy": 8, "sensor": 96, "structure": 16}
            for suite in r2.MATCHED_FIT_SUITES
        },
        "ood_counts_by_suite": {"C1": 0, "S": 0},
        "trajectory_census": {"C1": 152, "S": 152},
    }


def _loss_context(arms) -> dict:
    """Return one synthetic post-fit loss term mapping per arm."""

    context = {}
    for arm in arms:
        base = arm["seed"] / 100.0 + (0.01 if arm["suite"] == "S" else 0.0)
        context[(arm["suite"], arm["seed"])] = {
            term: base + index / 10.0 for index, term in enumerate(LOSS_TERMS)
        }
    return context


def _derive(*, reduced: bool = True) -> dict:
    """Drive the pure derivation without touching the completed run."""

    result = _result_document(reduced=reduced)
    ledger, analysis_document = _anchor_documents()
    arms = analysis.validate_rung2_arms(result, shape=SHAPE)
    anchors = analysis.validate_anchor_arms(result, ledger, analysis_document)
    equivalence = analysis.validate_equivalence_arms(result, ledger)
    return analysis.derive_analysis(
        result=result,
        arms=arms,
        anchors=anchors,
        equivalence=equivalence,
        loss_context=_loss_context(arms),
        shared_context=_shared_context(),
        input_digests={
            "approved_anchor_analysis": _digest("approved-analysis"),
            "approved_fit_ledger": _digest("approved-ledger"),
            "approved_plan": _digest("approved-plan"),
            "equivalence_artifact": _digest("equivalence"),
            "run_result": _digest("run-result"),
        },
    )


# ---------------------------------------------------------------------------
# One definition per criterion, and one identity for the whole read
# ---------------------------------------------------------------------------
def test_the_reader_imports_the_frozen_criteria_and_defines_none_of_them():
    """Invariant R7: the criteria are imported, not restated with a second definition."""

    tree = ast.parse(Path(analysis.__file__).read_text(encoding="utf-8"))
    locally_defined = {
        node.name
        for node in ast.walk(tree)
        if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef))
    }
    frozen = {
        "arm_objective_reduced",
        "optimization_check_passed",
        "optimization_check_status",
        "deficit_sign_label",
        "require_complete_rung2_run",
        "anchor_records",
        "rung2_shape",
        "score_arm",
        "quantize",
        "classification_metrics",
    }
    assert frozen.isdisjoint(locally_defined)
    source = Path(analysis.__file__).read_text(encoding="utf-8")
    assert "from utils import rung2_escalation as rung2" in source
    for name in ("optimization_check_status", "deficit_sign_label", "require_complete_rung2_run"):
        assert f"rung2.{name}" in source


def test_the_reader_imports_both_approved_analyzers_rather_than_copying_them():
    """Invariant R7 names both approved readers as imports; neither is edited here."""

    source = Path(analysis.__file__).read_text(encoding="utf-8")
    assert "import analyze_dev_fit as approved_analysis" in source
    assert "from analyze_capacity_sweep import" in source


def test_analysis_identity_covers_the_run_identity_and_both_readers():
    """The artifact binds every module the read executes through, not only its own file."""

    identity = analysis.analysis_code_identity()
    assert set(r2.rung2_code_identity()) <= set(identity)
    assert {
        "analyze_rung2_escalation.py",
        "analyze_capacity_sweep.py",
        "analyze_dev_fit.py",
        "rung2_escalation.py",
        "attribution_net_rung2.py",
    } <= set(identity)
    assert len(identity) == len(r2.rung2_code_identity()) + 2
    assert all(len(digest) == 64 for digest in identity.values())
    assert list(identity) == sorted(identity)


# ---------------------------------------------------------------------------
# The pure derivation
# ---------------------------------------------------------------------------
def test_pure_derivation_emits_every_predeclared_field_without_running_the_executable():
    """Ten arms, ten anchors, two gate arms, five metrics and one label."""

    report = _derive()
    assert set(report) == {
        "anchor_arms",
        "arms",
        "authority",
        "boundary",
        "deficit_sign_reproduced",
        "development_context",
        "equivalence_arms",
        "inputs",
        "optimization_check",
        "paired_S_minus_C1",
        "rung2_minus_rung1",
    }
    assert len(report["arms"]) == 10
    assert len(report["anchor_arms"]) == 10
    assert len(report["equivalence_arms"]) == 2
    assert report["optimization_check"] == {
        "completed_rung2_arms": 10,
        "equivalence_arms_passed": 2,
        "objective_reduced_arms": 10,
        "status": r2.OPTIMIZATION_CHECK_PASSED,
    }
    assert set(report["paired_S_minus_C1"]) == {"macro_f1", "per_class_f1"}
    assert set(report["paired_S_minus_C1"]["per_class_f1"]) == set(CLASSES)
    assert set(report["rung2_minus_rung1"]) == set(r2.MATCHED_FIT_SUITES)
    assert report["deficit_sign_reproduced"] == r2.SIGN_REPRODUCED
    assert report["authority"] == analysis.ANALYSIS_AUTHORITY


def test_every_paired_block_carries_five_seeds_a_mean_a_sample_sd_and_sign_counts():
    """Design section 5.2's paired block shape, at every one of the five metrics."""

    report = _derive()
    blocks = [report["paired_S_minus_C1"]["macro_f1"]] + [
        report["paired_S_minus_C1"]["per_class_f1"][name] for name in CLASSES
    ]
    for block in blocks:
        assert set(block) == {"mean", "per_seed", "sample_sd", "sign_count"}
        assert [row["seed"] for row in block["per_seed"]] == list(
            r2.PREDECLARED_TRAINING_SEEDS
        )
        assert set(block["sign_count"]) == {"negative", "positive", "zero"}
        assert sum(block["sign_count"].values()) == len(r2.PREDECLARED_TRAINING_SEEDS)
        for row in block["per_seed"]:
            assert row["S_minus_C1"]["raw"] == pytest.approx(row["S"] - row["C1"])
            assert row["S_minus_C1"]["quantized"] == r2.quantize(row["S_minus_C1"]["raw"])


def test_the_rung_difference_block_pairs_each_arm_with_its_own_anchor():
    """`rung2_minus_rung1` is per suite and per seed, against the read-only anchors."""

    report = _derive()
    anchors = {(arm["suite"], arm["seed"]): arm for arm in report["anchor_arms"]}
    arms = {(arm["suite"], arm["seed"]): arm for arm in report["arms"]}
    for suite, block in report["rung2_minus_rung1"].items():
        assert set(block) == {"mean", "per_seed", "sample_sd"}
        for row in block["per_seed"]:
            key = (suite, row["seed"])
            assert row["rung1_macro_f1"] == anchors[key]["macro_f1"]
            assert row["rung2_macro_f1"] == arms[key]["macro_f1"]
            assert row["rung2_minus_rung1"]["raw"] == pytest.approx(
                row["rung2_macro_f1"] - row["rung1_macro_f1"]
            )


def test_the_sign_label_is_recomputable_from_the_counts_the_artifact_persists():
    """The label has two independent routes and the artifact publishes both inputs."""

    report = _derive()
    counts = report["paired_S_minus_C1"]["macro_f1"]["sign_count"]
    assert analysis.label_from_sign_counts(counts) == report["deficit_sign_reproduced"]
    differences = [
        row["S_minus_C1"]["raw"] for row in report["paired_S_minus_C1"]["macro_f1"]["per_seed"]
    ]
    assert r2.deficit_sign_label(differences) == report["deficit_sign_reproduced"]


def test_the_reported_arms_carry_their_post_fit_loss_terms():
    """Every arm's record gains exactly the recomputed loss decomposition."""

    report = _derive()
    for arm in report["arms"]:
        assert set(arm["post_fit_full_batch_loss_terms"]) == set(LOSS_TERMS)
    means = report["development_context"]["mean_post_fit_full_batch_loss_terms_by_suite"]
    assert set(means) == set(r2.MATCHED_FIT_SUITES)
    for suite in r2.MATCHED_FIT_SUITES:
        assert set(means[suite]) == set(LOSS_TERMS)


def test_the_boundary_block_states_every_thing_the_read_did_not_do():
    """Section 5.3's boundary, persisted rather than left to a reader's assumption."""

    report = _derive()
    assert report["boundary"] == {
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
    }


def test_the_artifact_names_every_input_document_by_digest():
    """The derived read is bound to the five exact documents it was derived from."""

    report = _derive()
    assert set(report["inputs"]) == {
        "analysis_code_identity",
        "approved_anchor_analysis_canonical_sha256",
        "approved_fit_ledger_canonical_sha256",
        "approved_plan_canonical_sha256",
        "design_sha256",
        "equivalence_artifact_canonical_sha256",
        "fit_code_identity",
        "run_label",
        "run_result_canonical_sha256",
    }
    assert report["inputs"]["design_sha256"] == r2.DESIGN_CANONICAL_SHA256


# ---------------------------------------------------------------------------
# Invariant R10 -- the suppression, and the completeness gate above it
# ---------------------------------------------------------------------------
def test_a_run_that_did_not_reduce_one_objective_publishes_no_paired_or_rung_field():
    """R10's second half: the status is derived first and suppresses everything below."""

    report = _derive(reduced=False)
    assert report["optimization_check"]["status"] == r2.OPTIMIZATION_CHECK_FAILED
    assert report["optimization_check"]["objective_reduced_arms"] == 9
    assert report["paired_S_minus_C1"] is None
    assert report["rung2_minus_rung1"] is None
    assert report["deficit_sign_reproduced"] is None
    assert len(report["arms"]) == 10


def test_a_partial_run_is_refused_before_anything_is_derived():
    """R10's first half, through the executable's own imported completeness check."""

    result = _result_document()
    result["rung2_arms"][3]["status"] = r2.ARM_UNATTEMPTED
    with pytest.raises(analysis.CapacitySweepAnalysisError, match="not a complete rung-2 run"):
        analysis.validate_envelope(
            result,
            _equivalence_document(result),
            _plan_document(result),
            _anchor_documents()[1],
            digests=_digests_for(result),
        )


def test_a_failed_equivalence_arm_is_refused_by_the_completeness_check():
    """A gate arm that did not pass cannot reach the derivation at all."""

    result = _result_document()
    result["equivalence_arms"][0]["equivalence_status"] = r2.COMPARISON_FAIL
    with pytest.raises(analysis.CapacitySweepAnalysisError):
        analysis.validate_envelope(
            result,
            _equivalence_document(result),
            _plan_document(result),
            _anchor_documents()[1],
            digests=_digests_for(result),
        )


# ---------------------------------------------------------------------------
# The sign rule at its declared resolution
# ---------------------------------------------------------------------------
@pytest.mark.parametrize(
    ("differences", "expected"),
    (
        ([-0.1, -0.2, -0.3, -0.4, -0.5], {"negative": 5, "positive": 0, "zero": 0}),
        ([0.1, 0.2, 0.3, 0.4, 0.5], {"negative": 0, "positive": 5, "zero": 0}),
        ([-0.1, 0.2, 0.0, -0.4, 0.5], {"negative": 2, "positive": 2, "zero": 1}),
    ),
)
def test_sign_counts_classify_each_seed_once(differences, expected):
    """Every seed lands in exactly one of the three counts."""

    assert analysis.sign_counts(differences) == expected


def test_a_difference_below_the_declared_quantum_counts_as_a_tie():
    """The tie rule is the frozen six decimals, not float64's."""

    assert analysis.sign_counts([4e-7])["zero"] == 1
    assert analysis.sign_counts([-4e-7])["zero"] == 1
    assert analysis.sign_counts([6e-7])["positive"] == 1
    assert analysis.sign_counts([-6e-7])["negative"] == 1


@pytest.mark.parametrize(
    ("counts", "expected"),
    (
        ({"negative": 5, "positive": 0, "zero": 0}, r2.SIGN_REPRODUCED),
        ({"negative": 0, "positive": 5, "zero": 0}, r2.SIGN_NOT_REPRODUCED),
        ({"negative": 0, "positive": 0, "zero": 5}, r2.SIGN_NOT_REPRODUCED),
        ({"negative": 0, "positive": 3, "zero": 2}, r2.SIGN_NOT_REPRODUCED),
        ({"negative": 3, "positive": 2, "zero": 0}, r2.SIGN_MIXED),
        ({"negative": 4, "positive": 0, "zero": 1}, r2.SIGN_MIXED),
    ),
)
def test_the_count_route_and_the_difference_route_agree_on_every_shape(counts, expected):
    """The two label routes are checked against each other over the whole label space."""

    assert analysis.label_from_sign_counts(counts) == expected
    differences = (
        [-0.5] * counts["negative"] + [0.5] * counts["positive"] + [0.0] * counts["zero"]
    )
    assert r2.deficit_sign_label(differences) == expected


def test_an_empty_sign_count_is_refused_rather_than_labelled():
    """A label over nothing is a name without a measurement."""

    with pytest.raises(analysis.CapacitySweepAnalysisError):
        analysis.sign_counts([])
    with pytest.raises(analysis.CapacitySweepAnalysisError):
        analysis.label_from_sign_counts({"negative": 0, "positive": 0, "zero": 0})


# ---------------------------------------------------------------------------
# Per-arm validation
# ---------------------------------------------------------------------------
def _validate_one(arm: dict):
    """Validate one synthetic arm against the frozen shape and identity."""

    return analysis.validate_rung2_arm(
        arm, shape=SHAPE, epochs=EPOCHS, run_identity=dict(SYNTHETIC_IDENTITY)
    )


def test_a_well_formed_arm_normalizes_to_its_persisted_primitives():
    """The happy path keeps every value the record carried."""

    arm = _rung2_arm("C1", 0)
    parsed = _validate_one(arm)
    assert parsed["macro_f1"] == arm["macro_f1"]
    assert parsed["loss_history"] == arm["loss_history"]
    assert parsed["objective_reduced"] is True


@pytest.mark.parametrize(
    ("field", "value"),
    (
        ("suite", "C0"),
        ("seed", 9),
        ("status", "REFUSED"),
        ("rung", "rung1_temporal_attribution"),
        ("source", "capacity-sweep"),
        ("n_parameters", 39594),
        ("stem_receptive_field", 1023),
        ("n_examples", 0),
        ("accuracy", 1.5),
        ("macro_f1", -0.1),
        ("checkpoint_relative_name", "somewhere_else.pt"),
        ("checkpoint_sha256", "not-a-digest"),
    ),
)
def test_one_wrong_arm_field_is_refused_by_name(field, value):
    """Every declared per-arm property is checked, not merely present."""

    arm = _rung2_arm("S", 2)
    arm[field] = value
    with pytest.raises(analysis.CapacitySweepAnalysisError):
        _validate_one(arm)


def test_a_tampered_objective_flag_is_refused_because_it_is_recomputed():
    """Section 5.1's flag is re-derived from the history rather than read back."""

    arm = _rung2_arm("C1", 1)
    arm["objective_reduced"] = False
    with pytest.raises(analysis.CapacitySweepAnalysisError, match="objective-reduction flag"):
        _validate_one(arm)

    risen = _rung2_arm("C1", 1, reduced=False)
    risen["objective_reduced"] = True
    with pytest.raises(analysis.CapacitySweepAnalysisError, match="objective-reduction flag"):
        _validate_one(risen)


def test_a_history_of_the_wrong_length_or_a_mismatched_endpoint_is_refused():
    """The epoch count and the two recorded endpoints are both checked."""

    short = _rung2_arm("S", 3)
    short["loss_history"] = short["loss_history"][:-1]
    with pytest.raises(analysis.CapacitySweepAnalysisError, match="loss-history length"):
        _validate_one(short)

    moved = _rung2_arm("S", 3)
    moved["final_epoch_loss"] = moved["final_epoch_loss"] + 1.0
    with pytest.raises(analysis.CapacitySweepAnalysisError, match="epoch endpoints"):
        _validate_one(moved)


def test_a_non_finite_loss_value_is_refused():
    """A non-finite epoch cannot enter the record the objective check reads."""

    arm = _rung2_arm("C1", 4)
    arm["loss_history"][5] = float("inf")
    with pytest.raises(analysis.CapacitySweepAnalysisError):
        _validate_one(arm)


def test_the_wrong_per_class_universe_is_refused():
    """The four source classes are the approved analyzer's, not this reader's."""

    arm = _rung2_arm("C1", 0)
    arm["per_class_f1"] = {"healthy": 0.5, "structure": 0.5}
    with pytest.raises(analysis.CapacitySweepAnalysisError, match="per-class F1 universe"):
        _validate_one(arm)


def test_an_arm_fitted_by_a_different_code_state_is_refused():
    """Every arm must name the identity the terminal record names."""

    arm = _rung2_arm("C1", 0)
    arm["fit_code_identity"] = {"other.py": "c" * 64}
    with pytest.raises(analysis.CapacitySweepAnalysisError, match="fitting-code identity"):
        _validate_one(arm)


def test_the_ten_arm_identities_must_be_exactly_the_predeclared_ten():
    """A duplicated identity is refused even when the count is right."""

    result = _result_document()
    result["rung2_arms"][1] = copy.deepcopy(result["rung2_arms"][0])
    with pytest.raises(analysis.CapacitySweepAnalysisError):
        analysis.validate_rung2_arms(result, shape=SHAPE)


def test_two_arms_sharing_one_checkpoint_digest_are_refused():
    """Ten arms are ten checkpoints; a shared digest means one of them is not its own."""

    result = _result_document()
    result["rung2_arms"][1]["checkpoint_sha256"] = result["rung2_arms"][0][
        "checkpoint_sha256"
    ]
    with pytest.raises(analysis.CapacitySweepAnalysisError, match="same checkpoint digest"):
        analysis.validate_rung2_arms(result, shape=SHAPE)


# ---------------------------------------------------------------------------
# The gate arms and the read-only anchors
# ---------------------------------------------------------------------------
def test_both_gate_arms_validate_against_the_approved_ledger():
    """The reference digest comes from a different file than the record asserting it."""

    result = _result_document()
    ledger, _ = _anchor_documents()
    parsed = analysis.validate_equivalence_arms(result, ledger)
    assert [(entry["suite"], entry["seed"]) for entry in parsed] == sorted(
        r2.EQUIVALENCE_ARMS
    )


def test_a_gate_arm_whose_histories_differ_is_refused_even_when_the_flag_says_otherwise():
    """The persisted boolean is recomputed from the persisted histories."""

    result = _result_document()
    result["equivalence_arms"][0]["refit_loss_history"][7] += 1e-9
    ledger, _ = _anchor_documents()
    with pytest.raises(analysis.CapacitySweepAnalysisError, match="not identical"):
        analysis.validate_equivalence_arms(result, ledger)


def test_a_gate_arm_naming_a_reference_the_ledger_does_not_carry_is_refused():
    """The anchor a gate arm compared against must be the approved one."""

    result = _result_document()
    result["equivalence_arms"][1]["rung1_reference_checkpoint_sha256"] = _digest("other")
    ledger, _ = _anchor_documents()
    with pytest.raises(analysis.CapacitySweepAnalysisError, match="reference checkpoint"):
        analysis.validate_equivalence_arms(result, ledger)


def test_a_gate_arm_naming_an_unapproved_refit_path_is_refused():
    """The refit checkpoint name has one definition and the record must use it."""

    result = _result_document()
    result["equivalence_arms"][0]["refit_checkpoint_relative_name"] = "loose.pt"
    ledger, _ = _anchor_documents()
    with pytest.raises(analysis.CapacitySweepAnalysisError, match="refit checkpoint"):
        analysis.validate_equivalence_arms(result, ledger)


def test_an_anchor_number_edited_in_the_record_is_refused_because_it_is_re_read():
    """Section 5.2's read-only numbers are re-fetched from their named source field."""

    result = _result_document()
    result["anchor_arms"][2]["macro_f1"] = 0.99
    ledger, analysis_document = _anchor_documents()
    with pytest.raises(analysis.CapacitySweepAnalysisError, match="approved rung-1 records"):
        analysis.validate_anchor_arms(result, ledger, analysis_document)


def test_a_missing_or_duplicated_anchor_is_refused():
    """All ten approved identities must appear exactly once."""

    ledger, analysis_document = _anchor_documents()
    short = _result_document()
    short["anchor_arms"] = short["anchor_arms"][:-1]
    with pytest.raises(analysis.CapacitySweepAnalysisError, match="omits an approved anchor"):
        analysis.validate_anchor_arms(short, ledger, analysis_document)

    duplicated = _result_document()
    duplicated["anchor_arms"][1] = copy.deepcopy(duplicated["anchor_arms"][0])
    with pytest.raises(analysis.CapacitySweepAnalysisError, match="duplicates an anchor"):
        analysis.validate_anchor_arms(duplicated, ledger, analysis_document)


# ---------------------------------------------------------------------------
# The envelope
# ---------------------------------------------------------------------------
def _digests_for(result: dict) -> dict:
    """Return the digest map the envelope check expects for one synthetic record."""

    return {
        "approved_anchor_analysis": result["approved_analysis_sha256"],
        "approved_fit_ledger": result["approved_fit_ledger_sha256"],
        "approved_plan": result["approved_plan_sha256"],
        "equivalence_artifact": _digest("equivalence"),
        "run_result": _digest("run-result"),
    }


def _bound_state() -> tuple[dict, dict, dict, dict]:
    """Return a synthetic result/equivalence/plan/anchor state bound to the real code."""

    identity = r2.rung2_code_identity()
    result = _result_document(identity=identity)
    for arm in result["rung2_arms"]:
        arm["fit_code_identity"] = dict(identity)
    for arm in result["equivalence_arms"]:
        arm["fit_code_identity"] = dict(identity)
    equivalence = _equivalence_document(result)
    plan = _plan_document(result)
    return result, equivalence, plan, _anchor_documents()[1]


def test_a_fully_bound_envelope_is_accepted():
    """The accept side exists, so the refusals below are not vacuous."""

    result, equivalence, plan, anchor = _bound_state()
    analysis.validate_envelope(result, equivalence, plan, anchor, digests=_digests_for(result))


@pytest.mark.parametrize(
    ("document", "field", "value"),
    (
        ("result", "exit", r2.X_RUN_INCOMPLETE),
        ("result", "mode", "plan"),
        ("result", "reason_class", "SomeError"),
        ("result", "authority", "something else"),
        ("result", "rung", "rung1_temporal_attribution"),
        ("result", "fits_attempted", 11),
        ("result", "checkpoints_written", 11),
        ("result", "rung2_fits_attempted", 9),
        ("result", "equivalence_fits_attempted", 1),
        ("result", "generation_runs", 1),
        ("result", "non_dev_reads", 1),
        ("result", "rollouts_spent", 1),
        ("result", "design_sha256", "a" * 64),
        ("result", "run_label", "another-run"),
        ("plan", "exit", "X_PLAN_REFUSED"),
        ("plan", "mode", "execute"),
        ("plan", "plan_valid", False),
        ("plan", "authority", "something else"),
        ("plan", "design_sha256", "a" * 64),
    ),
)
def test_one_wrong_envelope_field_is_refused(document, field, value):
    """Every envelope property is checked against an independent source."""

    result, equivalence, plan, anchor = _bound_state()
    target = {"result": result, "plan": plan}[document]
    target[field] = value
    if document == "result" and field == "run_label":
        equivalence = _equivalence_document(result)
    with pytest.raises(analysis.CapacitySweepAnalysisError):
        analysis.validate_envelope(
            result, equivalence, plan, anchor, digests=_digests_for(result)
        )


def test_a_result_not_bound_to_the_supplied_plan_digest_is_refused():
    """The plan the run consumed must be the plan this read was handed."""

    result, equivalence, plan, anchor = _bound_state()
    digests = dict(_digests_for(result))
    digests["approved_plan"] = _digest("a different plan")
    with pytest.raises(analysis.CapacitySweepAnalysisError, match="not bound to the supplied"):
        analysis.validate_envelope(result, equivalence, plan, anchor, digests=digests)


def test_a_changed_producing_code_state_is_refused_on_either_document():
    """R12: the record and the plan must both name the code state running today."""

    for target in ("result", "plan"):
        result, equivalence, plan, anchor = _bound_state()
        document = {"result": result, "plan": plan}[target]
        document["code_identity"] = {"rung2_escalation.py": "d" * 64}
        with pytest.raises(analysis.CapacitySweepAnalysisError, match="code state"):
            analysis.validate_envelope(
                result, equivalence, plan, anchor, digests=_digests_for(result)
            )


def test_a_budget_that_is_not_the_frozen_twelve_is_refused_on_either_document():
    """The maximum budget is a frozen property of the design, not an operator's input."""

    for target in ("result", "plan"):
        result, equivalence, plan, anchor = _bound_state()
        document = {"result": result, "plan": plan}[target]
        document["maximum_budget"] = dict(_budget(), fits=13)
        with pytest.raises(analysis.CapacitySweepAnalysisError, match="resource budget"):
            analysis.validate_envelope(
                result, equivalence, plan, anchor, digests=_digests_for(result)
            )


def test_a_protocol_or_census_disagreement_between_plan_and_run_is_refused():
    """The plan and the run must describe one training protocol and one dataset."""

    result, equivalence, plan, anchor = _bound_state()
    plan["training_protocol"] = dict(_protocol(), epochs=21)
    with pytest.raises(analysis.CapacitySweepAnalysisError, match="training protocol"):
        analysis.validate_envelope(
            result, equivalence, plan, anchor, digests=_digests_for(result)
        )

    result, equivalence, plan, anchor = _bound_state()
    plan["manifest_sha256"] = _digest("other manifest")
    with pytest.raises(analysis.CapacitySweepAnalysisError, match="data census"):
        analysis.validate_envelope(
            result, equivalence, plan, anchor, digests=_digests_for(result)
        )


@pytest.mark.parametrize(
    ("field", "value"),
    (
        ("gate_passed", False),
        ("authority", "something else"),
        ("equivalence_channels", 16),
        ("equivalence_rung", "rung2_recurrent_plus_attention"),
        ("fits_attempted", 1),
        ("checkpoints_written", 3),
        ("generation_runs", 1),
        ("rollouts_spent", 1),
    ),
)
def test_one_wrong_gate_evidence_field_is_refused(field, value):
    """The gate artifact is authenticated, not merely opened."""

    result, equivalence, plan, anchor = _bound_state()
    equivalence[field] = value
    with pytest.raises(analysis.CapacitySweepAnalysisError):
        analysis.validate_envelope(
            result, equivalence, plan, anchor, digests=_digests_for(result)
        )


def test_gate_evidence_that_disagrees_with_the_terminal_record_is_refused():
    """Two documents record the same two arms; a difference between them is a refusal."""

    result, equivalence, plan, anchor = _bound_state()
    equivalence["arms"][0]["refit_checkpoint_sha256"] = _digest("something else")
    with pytest.raises(analysis.CapacitySweepAnalysisError, match="disagree about the gate"):
        analysis.validate_envelope(
            result, equivalence, plan, anchor, digests=_digests_for(result)
        )


# ---------------------------------------------------------------------------
# Paths, the artifact, and the command line
# ---------------------------------------------------------------------------
def _write_state(tmp_path: Path) -> dict:
    """Materialize a complete synthetic exact state on disk and return its handles."""

    result, equivalence, plan, anchor = _bound_state()
    ledger, _ = _anchor_documents()
    run_root = tmp_path / "results" / "rung2_escalation" / "synthetic-run"
    (run_root / r2.EQUIVALENCE_SUBTREE).mkdir(parents=True)
    for arm in result["rung2_arms"]:
        path = run_root / arm["checkpoint_relative_name"]
        payload = f"rung2:{arm['suite']}:{arm['seed']}".encode("utf-8")
        path.write_bytes(payload)
        arm["checkpoint_sha256"] = hashlib.sha256(payload).hexdigest()
    for arm in result["equivalence_arms"]:
        path = run_root / arm["refit_checkpoint_relative_name"]
        payload = f"refit:{arm['suite']}:{arm['seed']}".encode("utf-8")
        path.write_bytes(payload)
        arm["refit_checkpoint_sha256"] = hashlib.sha256(payload).hexdigest()
    equivalence = _equivalence_document(result)

    paths = {
        "run_result": run_root / r2.RUN_ARTIFACT,
        "equivalence": run_root / r2.EQUIVALENCE_SUBTREE / r2.EQUIVALENCE_ARTIFACT,
        "plan": tmp_path / "plan.json",
        "ledger": tmp_path / "dev_fit_result.json",
        "anchor": tmp_path / "dev_fit_analysis.json",
    }
    documents = {
        "run_result": result,
        "equivalence": equivalence,
        "plan": plan,
        "ledger": ledger,
        "anchor": anchor,
    }
    digests = {}
    for name, path in paths.items():
        path.write_text(
            json.dumps(documents[name], sort_keys=True, separators=(",", ":")),
            encoding="utf-8",
            newline="\n",
        )
        digests[name] = hashlib.sha256(path.read_bytes()).hexdigest()
    # The plan/ledger/anchor digests the record asserts must be the real ones now.
    result["approved_plan_sha256"] = digests["plan"]
    result["approved_fit_ledger_sha256"] = digests["ledger"]
    result["approved_analysis_sha256"] = digests["anchor"]
    plan["approved_fit_ledger_sha256"] = digests["ledger"]
    plan["approved_analysis_sha256"] = digests["anchor"]
    paths["plan"].write_text(
        json.dumps(plan, sort_keys=True, separators=(",", ":")),
        encoding="utf-8",
        newline="\n",
    )
    digests["plan"] = hashlib.sha256(paths["plan"].read_bytes()).hexdigest()
    result["approved_plan_sha256"] = digests["plan"]
    paths["run_result"].write_text(
        json.dumps(result, sort_keys=True, separators=(",", ":")),
        encoding="utf-8",
        newline="\n",
    )
    digests["run_result"] = hashlib.sha256(paths["run_result"].read_bytes()).hexdigest()
    return {
        "digests": digests,
        "paths": paths,
        "result": result,
        "run_root": run_root,
        "tmp_path": tmp_path,
    }


def _patch_dev_context(monkeypatch, state: dict) -> None:
    """Replace the two steps that would open the delivered dataset."""

    monkeypatch.setattr(
        analysis,
        "load_development_context",
        lambda **kwargs: ({"C1": [], "S": []}, _shared_context()),
    )
    monkeypatch.setattr(
        analysis,
        "evaluate_all_arms",
        lambda arms, **kwargs: _loss_context(arms),
    )


def _argv(state: dict, output_dir: Path) -> list[str]:
    """Return the full required command line for one materialized state."""

    paths = state["paths"]
    return [
        "--data-root", str(state["tmp_path"] / "data"),
        "--run-result", str(paths["run_result"]),
        "--run-result-sha256", state["digests"]["run_result"],
        "--equivalence-artifact", str(paths["equivalence"]),
        "--approved-plan", str(paths["plan"]),
        "--approved-fit-ledger", str(paths["ledger"]),
        "--approved-anchor-analysis", str(paths["anchor"]),
        "--run-root", str(state["run_root"]),
        "--output-dir", str(output_dir),
    ]


def test_the_whole_read_runs_end_to_end_against_a_materialized_synthetic_state(
    tmp_path, monkeypatch, capsys
):
    """One complete pass: authenticate, verify the twelve checkpoints, derive, write."""

    state = _write_state(tmp_path)
    _patch_dev_context(monkeypatch, state)
    output_dir = tmp_path / "out"
    assert analysis.main(_argv(state, output_dir)) == analysis.EXIT_CODES[analysis.X_ANALYSIS_OK]
    written = output_dir / analysis.OUTPUT_NAME
    payload = written.read_bytes()
    assert b"\n" not in payload and b"\r" not in payload
    report = json.loads(payload.decode("utf-8"))
    assert report["optimization_check"]["status"] == r2.OPTIMIZATION_CHECK_PASSED
    assert report["deficit_sign_reproduced"] == r2.SIGN_REPRODUCED
    printed = capsys.readouterr().out
    assert "BOUNDARY" in printed and "zero fits" in printed


def test_the_artifact_carries_no_absolute_path(tmp_path, monkeypatch):
    """Section 5.3: no absolute filesystem path enters any artifact."""

    state = _write_state(tmp_path)
    _patch_dev_context(monkeypatch, state)
    output_dir = tmp_path / "out"
    analysis.main(_argv(state, output_dir))
    payload = (output_dir / analysis.OUTPUT_NAME).read_text(encoding="utf-8")
    assert str(tmp_path) not in payload
    assert ":\\" not in payload and "://" not in payload
    assert str(PACKET_ROOT) not in payload


def test_a_second_write_is_refused_and_the_first_artifact_survives(tmp_path, monkeypatch):
    """The destination is an exclusive create; a rerun does not overwrite the record."""

    state = _write_state(tmp_path)
    _patch_dev_context(monkeypatch, state)
    output_dir = tmp_path / "out"
    assert analysis.main(_argv(state, output_dir)) == 0
    first = (output_dir / analysis.OUTPUT_NAME).read_bytes()
    assert analysis.main(_argv(state, output_dir)) == analysis.EXIT_CODES[
        analysis.X_ANALYSIS_REFUSED
    ]
    assert (output_dir / analysis.OUTPUT_NAME).read_bytes() == first


def test_a_run_result_that_is_not_the_authorized_bytes_is_refused(tmp_path, monkeypatch, capsys):
    """The read is bound to one exact state, named on the command line."""

    state = _write_state(tmp_path)
    _patch_dev_context(monkeypatch, state)
    argv = _argv(state, tmp_path / "out")
    argv[argv.index("--run-result-sha256") + 1] = "0" * 64
    assert analysis.main(argv) == analysis.EXIT_CODES[analysis.X_ANALYSIS_REFUSED]
    assert "X_ANALYSIS_REFUSED" in capsys.readouterr().out
    assert not (tmp_path / "out" / analysis.OUTPUT_NAME).exists()


def test_a_run_result_outside_the_supplied_run_root_is_refused(tmp_path, monkeypatch):
    """The terminal artifact must be the named one at the named root."""

    state = _write_state(tmp_path)
    _patch_dev_context(monkeypatch, state)
    stray = tmp_path / r2.RUN_ARTIFACT
    stray.write_bytes(state["paths"]["run_result"].read_bytes())
    argv = _argv(state, tmp_path / "out")
    argv[argv.index("--run-result") + 1] = str(stray)
    assert analysis.main(argv) == analysis.EXIT_CODES[analysis.X_ANALYSIS_REFUSED]


def test_gate_evidence_outside_the_reserved_subtree_is_refused(tmp_path, monkeypatch):
    """The gate artifact lives in `_equivalence/` of the claimed root, nowhere else."""

    state = _write_state(tmp_path)
    _patch_dev_context(monkeypatch, state)
    stray = state["run_root"] / r2.EQUIVALENCE_ARTIFACT
    stray.write_bytes(state["paths"]["equivalence"].read_bytes())
    argv = _argv(state, tmp_path / "out")
    argv[argv.index("--equivalence-artifact") + 1] = str(stray)
    assert analysis.main(argv) == analysis.EXIT_CODES[analysis.X_ANALYSIS_REFUSED]


def test_a_missing_or_altered_checkpoint_is_refused(tmp_path, monkeypatch):
    """The digests the record publishes are re-taken from the bytes still on disk."""

    state = _write_state(tmp_path)
    _patch_dev_context(monkeypatch, state)
    target = state["run_root"] / r2.equivalence_relative_name(*r2.EQUIVALENCE_ARMS[0])
    target.write_bytes(b"tampered")
    assert analysis.main(_argv(state, tmp_path / "out")) == analysis.EXIT_CODES[
        analysis.X_ANALYSIS_REFUSED
    ]

    state = _write_state(tmp_path / "second")
    _patch_dev_context(monkeypatch, state)
    (state["run_root"] / r2.equivalence_relative_name(*r2.EQUIVALENCE_ARMS[1])).unlink()
    assert analysis.main(_argv(state, tmp_path / "second" / "out")) == analysis.EXIT_CODES[
        analysis.X_ANALYSIS_REFUSED
    ]


def test_every_command_line_input_is_required(tmp_path):
    """No machine-specific path or digest has a default."""

    for flag in (
        "--data-root",
        "--run-result",
        "--run-result-sha256",
        "--equivalence-artifact",
        "--approved-plan",
        "--approved-fit-ledger",
        "--approved-anchor-analysis",
        "--run-root",
        "--output-dir",
    ):
        argv = [
            "--data-root", "d",
            "--run-result", "r",
            "--run-result-sha256", "0" * 64,
            "--equivalence-artifact", "e",
            "--approved-plan", "p",
            "--approved-fit-ledger", "l",
            "--approved-anchor-analysis", "a",
            "--run-root", "x",
            "--output-dir", "o",
        ]
        index = argv.index(flag)
        del argv[index : index + 2]
        with pytest.raises(SystemExit):
            analysis.parse_args(argv)


def test_the_output_name_and_exit_codes_are_the_declared_ones():
    """The artifact's name and the two terminals are pinned by equality."""

    assert analysis.OUTPUT_NAME == "rung2_escalation_analysis.json"
    assert analysis.EXIT_CODES == {"X_ANALYSIS_OK": 0, "X_ANALYSIS_REFUSED": 3}


def test_the_reader_emits_none_of_the_forbidden_inferential_vocabulary():
    """Section 5.3: no p-value, interval, significance, selection or trend statement."""

    report = _derive()
    payload = json.dumps(report).lower()
    for word in (
        "p_value",
        "p-value",
        "confidence",
        "significan",
        "detectable",
        "recommend",
        "trend",
        "slope",
        "improve",
        "better",
        "worse",
    ):
        assert word not in payload


# ---------------------------------------------------------------------------
# The recomputation -- the one part of this read that opens a checkpoint
# ---------------------------------------------------------------------------
REGISTRY_WIDTH = 18
SYNTHETIC_WINDOW = 8


def _training_example(class_index: int):
    """Return one tiny synthetic training example at the real registry width."""

    import numpy as np

    rng = np.random.default_rng(class_index + 1)
    return r2.trainer.TrainingExample(
        run_id=f"synthetic-{class_index}",
        trajectory_spec_id="synthetic",
        values=rng.normal(size=(SYNTHETIC_WINDOW, REGISTRY_WIDTH)),
        valid=np.ones((SYNTHETIC_WINDOW, REGISTRY_WIDTH), dtype=bool),
        class_index=class_index % 4,
        location_index=class_index % 3,
        severity=0.1 * class_index,
        ood_flag=False,
    )


@pytest.fixture(scope="module")
def scored_checkpoint(tmp_path_factory):
    """Return a real rung-2 checkpoint, its digest, and the scores it actually produces."""

    import torch

    directory = tmp_path_factory.mktemp("rescore")
    examples = [_training_example(index) for index in range(4)]
    network = r2.build_rung2_network(seed=0)
    path = directory / r2.rung2_checkpoint_name("C1", 0)
    torch.save(network.state_dict(), path)
    metrics = r2.score_arm(network, examples)
    return {
        "digest": r2.trainer.file_sha256(path),
        "examples": examples,
        "metrics": metrics,
        "path": path,
    }


def _rescore_arm(scored: dict) -> dict:
    """Return one normalized arm whose stored scores are the checkpoint's own."""

    arm = _rung2_arm("C1", 0)
    arm["accuracy"] = scored["metrics"]["accuracy"]
    arm["macro_f1"] = scored["metrics"]["macro_f1"]
    arm["per_class_f1"] = dict(scored["metrics"]["per_class_f1"])
    arm["checkpoint_sha256"] = scored["digest"]
    return _validate_one(arm)


def test_the_rescore_accepts_the_scores_the_checkpoint_actually_produces(scored_checkpoint):
    """The accept side of the recomputation, so the refusals below are not vacuous."""

    terms = analysis.evaluate_rung2_arm(
        _rescore_arm(scored_checkpoint),
        scored_checkpoint["examples"],
        scored_checkpoint["path"],
    )
    assert set(terms) == set(LOSS_TERMS)
    assert all(isinstance(value, float) for value in terms.values())


@pytest.mark.parametrize("field", ("accuracy", "macro_f1", "per_class_f1"))
def test_a_stored_score_the_checkpoint_does_not_produce_is_refused(scored_checkpoint, field):
    """Every stored classification field is compared exactly against a fresh forward pass."""

    arm = dict(_rescore_arm(scored_checkpoint))
    if field == "per_class_f1":
        moved = dict(arm["per_class_f1"])
        moved[CLASSES[0]] = min(1.0, moved[CLASSES[0]] + 0.25)
        arm["per_class_f1"] = moved
    else:
        arm[field] = min(1.0, arm[field] + 0.25)
    with pytest.raises(analysis.CapacitySweepAnalysisError, match="recomputed checkpoint score"):
        analysis.evaluate_rung2_arm(
            arm, scored_checkpoint["examples"], scored_checkpoint["path"]
        )


def test_a_checkpoint_whose_bytes_differ_from_the_recorded_digest_is_refused(
    scored_checkpoint,
):
    """The digest is re-taken from disk before the weights are loaded."""

    arm = dict(_rescore_arm(scored_checkpoint), checkpoint_sha256="0" * 64)
    with pytest.raises(analysis.CapacitySweepAnalysisError, match="differs from the digest"):
        analysis.evaluate_rung2_arm(
            arm, scored_checkpoint["examples"], scored_checkpoint["path"]
        )


def test_an_absent_checkpoint_is_refused_by_name(scored_checkpoint, tmp_path):
    """A record naming a file that is not there is a refusal, not a traceback."""

    with pytest.raises(analysis.CapacitySweepAnalysisError, match="is absent"):
        analysis.evaluate_rung2_arm(
            _rescore_arm(scored_checkpoint),
            scored_checkpoint["examples"],
            tmp_path / "missing.pt",
        )


def test_a_checkpoint_that_is_not_a_rung_two_state_dict_is_refused(
    scored_checkpoint, tmp_path
):
    """A loadable tensor file that is not this architecture refuses at the load."""

    import torch

    path = tmp_path / "wrong.pt"
    torch.save({"not_a_layer.weight": torch.zeros(3)}, path)
    arm = dict(
        _rescore_arm(scored_checkpoint),
        checkpoint_sha256=r2.trainer.file_sha256(path),
    )
    with pytest.raises(analysis.CapacitySweepAnalysisError, match="cannot be loaded"):
        analysis.evaluate_rung2_arm(arm, scored_checkpoint["examples"], path)


# ---------------------------------------------------------------------------
# The two constants this file would otherwise assert against itself
# ---------------------------------------------------------------------------
def test_the_shape_this_file_validates_against_is_the_constructed_network_s_own():
    """The fixture's parameter count and stem span are read off a real rung-2 net."""

    assert r2.rung2_shape() == {
        "n_parameters": SHAPE["n_parameters"],
        "rung": r2.RUNG2_NAME,
        "stem_receptive_field": SHAPE["stem_receptive_field"],
    }


def test_a_protocol_without_a_positive_epoch_count_is_refused():
    """The loss-history length is checked against the record's own protocol."""

    result = _result_document()
    result["training_protocol"] = dict(_protocol(), epochs=0)
    with pytest.raises(analysis.CapacitySweepAnalysisError, match="positive epoch count"):
        analysis.validate_rung2_arms(result, shape=SHAPE)


def test_two_documents_that_agree_with_each_other_but_not_with_today_are_refused():
    """Requirement (z): the identity check needs a source outside the state it checks.

    Measured in this session's mutation sweep: sourcing `current_identity` from the
    terminal record itself survives every other identity test in this file, because
    each of those makes the two documents disagree, and a self-comparison still catches
    a disagreement. The state it stops catching is the one that matters -- an older run
    whose record, plan and gate evidence all name one another consistently, read by a
    newer executable. Only a wrong identity that is wrong *everywhere at once* separates
    the real comparison from the self-comparison.
    """

    result, equivalence, plan, anchor = _bound_state()
    stale = {name: "e" * 64 for name in r2.rung2_code_identity()}
    result["code_identity"] = dict(stale)
    plan["code_identity"] = dict(stale)
    equivalence["code_identity"] = dict(stale)
    for arm in result["rung2_arms"]:
        arm["fit_code_identity"] = dict(stale)
    equivalence["arms"] = copy.deepcopy(result["equivalence_arms"])
    with pytest.raises(analysis.CapacitySweepAnalysisError, match="code state"):
        analysis.validate_envelope(
            result, equivalence, plan, anchor, digests=_digests_for(result)
        )
