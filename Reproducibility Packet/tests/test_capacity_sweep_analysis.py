"""Tests for the C7 read-only capacity-sweep analysis.

No test in this file reads the completed sweep, the delivered dataset, or a real
checkpoint. The pre-declared read is driven with synthetic persisted primitives; path,
digest and refusal behavior are exercised in temporary directories. Building and testing
the reader is not its separately gated execution.
"""

from __future__ import annotations

import ast
import copy
import hashlib
import json
import sys
from contextlib import nullcontext
from pathlib import Path
from types import SimpleNamespace

import pytest
import torch

PACKET_ROOT = Path(__file__).resolve().parents[1]
SCRIPTS_DIR = PACKET_ROOT / "scripts"
sys.path.insert(0, str(SCRIPTS_DIR))

import analyze_capacity_sweep as analysis  # noqa: E402
import analyze_dev_fit as approved_analysis  # noqa: E402
from utils import capacity_sweep as cs  # noqa: E402


LOSS_TERMS = (
    "class_cross_entropy",
    "location_cross_entropy",
    "ood_binary_cross_entropy",
    "severity_gaussian_nll",
    "severity_log_scale_mean",
    "total",
)


def _arm(channels: int, suite: str, seed: int, macro_f1: float) -> dict:
    """Return one normalized synthetic arm carrying every C7 primitive."""

    status = cs.ARM_REUSED if channels == cs.ANCHOR_CHANNELS else cs.ARM_COMPLETED
    arm = {
        "accuracy": min(1.0, macro_f1 + 0.03),
        "channels": channels,
        "checkpoint_sha256": f"{channels:02x}{seed:02x}".ljust(64, "a"),
        "fit_code_identity": {"synthetic_fit.py": "b" * 64},
        "macro_f1": macro_f1,
        "n_parameters": cs.EXPECTED_PARAMETERS[channels],
        "per_class_f1": {
            name: macro_f1 for name in approved_analysis.SOURCE_CLASS_ORDER
        },
        "receptive_field": cs.EXPECTED_RECEPTIVE_FIELD,
        "seed": seed,
        "source": "approved-ledger" if status == cs.ARM_REUSED else "capacity-sweep",
        "status": status,
        "suite": suite,
    }
    if status == cs.ARM_COMPLETED:
        arm.update(
            {
                "checkpoint_relative_name": (
                    f"ch{channels:03d}/{suite}/capacity_sweep_ch{channels:03d}_"
                    f"{suite}_seed{seed}.pt"
                ),
                "final_loss": 0.5 + seed / 100.0,
                "loss_history": [0.8, 0.6, 0.5 + seed / 100.0],
                "n_examples": 152,
            }
        )
    return arm


def _synthetic_state() -> tuple[list[dict], dict, dict, float]:
    """Return arms, loss context, shared context and the exact anchor sample SD."""

    c1_means = {16: 0.60, 24: 0.64, 32: 0.68, 40: 0.72, 48: 0.76}
    difference_means = {16: -0.06, 24: -0.04, 32: -0.02, 40: 0.01, 48: 0.03}
    seed_offsets = {0: -0.02, 1: -0.01, 2: 0.0, 3: 0.01, 4: 0.02}
    arms: list[dict] = []
    losses: dict[tuple[int, str, int], dict[str, float]] = {}
    for channels in cs.CAPACITY_POINTS:
        for suite in ("C1", "S"):
            for seed in cs.PREDECLARED_TRAINING_SEEDS:
                c1 = c1_means[channels] + seed * 0.002
                macro_f1 = (
                    c1
                    if suite == "C1"
                    else c1 + difference_means[channels] + seed_offsets[seed]
                )
                arm = _arm(channels, suite, seed, macro_f1)
                arms.append(arm)
                key = (channels, suite, seed)
                base = channels / 1000.0 + (0.01 if suite == "S" else 0.0) + seed / 10000.0
                losses[key] = {
                    term: base + index / 100.0 for index, term in enumerate(LOSS_TERMS)
                }
    arms.sort(key=lambda arm: (arm["channels"], 0 if arm["suite"] == "C1" else 1, arm["seed"]))
    anchor_differences = [
        difference_means[cs.ANCHOR_CHANNELS] + seed_offsets[seed]
        for seed in cs.PREDECLARED_TRAINING_SEEDS
    ]
    # The approved analyzer persists floats at its explicit 12-decimal boundary.
    anchor_sd = round(
        approved_analysis.sample_standard_deviation(anchor_differences), 12
    )
    shared = {
        "baselines": {
            "empirical_prior_cross_entropy": 0.9,
            "majority_class": "sensor",
            "majority_class_accuracy": 96 / 152,
        },
        "class_counts_by_suite": {
            suite: {"healthy": 8, "structure": 16, "actuator": 32, "sensor": 96}
            for suite in ("C1", "S")
        },
        "ood_counts_by_suite": {"C1": 0, "S": 0},
        "trajectory_census": {"synthetic": {"C1": 152, "S": 152}},
    }
    return arms, losses, shared, anchor_sd


def _derive() -> dict:
    """Drive the pure C7 derivation without touching the completed result."""

    arms, losses, shared, anchor_sd = _synthetic_state()
    return analysis.derive_analysis(
        arms=arms,
        loss_context=losses,
        shared_context=shared,
        bar=0.05,
        anchor_sample_sd=anchor_sd,
        result={
            "code_identity": {"synthetic_fit.py": "b" * 64},
            "design_sha256": "c" * 64,
            "run_label": "synthetic-run",
        },
        input_digests={
            "approved_anchor_analysis": "d" * 64,
            "approved_plan": "e" * 64,
            "sweep_result": "f" * 64,
        },
    )


def _complete_curve_templates() -> list[dict]:
    """Return the exact identity/status surface C10 requires, with no measurements."""

    return [
        {
            "channels": channels,
            "seed": seed,
            "status": (
                cs.ARM_REUSED if channels == cs.ANCHOR_CHANNELS else cs.ARM_COMPLETED
            ),
            "suite": suite,
        }
        for channels in cs.CAPACITY_POINTS
        for suite in ("C1", "S")
        for seed in cs.PREDECLARED_TRAINING_SEEDS
    ]


def _envelope_fixture() -> tuple[dict, dict, dict, str, str]:
    """Return a synthetic but fully bound plan/result/anchor envelope."""

    plan_digest = "a" * 64
    anchor_digest = "b" * 64
    current_identity = cs.sweep_code_identity()
    protocol = {"split": "dev", "window_steps": 768}
    budget = {
        "checkpoints": cs.MAX_CHECKPOINTS,
        "fits": cs.MAX_FITS,
        "generation_runs": 0,
        "non_dev_reads": 0,
        "rollouts": 0,
    }
    plan = {
        "anchor_sample_sd": 0.15,
        "anchor_sample_sd_field": ".".join(cs.ANCHOR_SAMPLE_SD_FIELD_PATH),
        "approved_analysis_sha256": anchor_digest,
        "assignment_sha256": "c" * 64,
        "authority": cs.SWEEP_AUTHORITY,
        "capacity_points": list(cs.CAPACITY_POINTS),
        "claim_sheet_success_bar": 0.05,
        "claim_sheet_success_bar_field": ".".join(cs.BAR_FIELD_PATH),
        "code_identity": current_identity,
        "design_sha256": cs.DESIGN_CANONICAL_SHA256,
        "exit": cs.X_PLAN_OK,
        "manifest_sha256": "d" * 64,
        "maximum_budget": budget,
        "mode": "plan",
        "plan_valid": True,
        "run_label": "synthetic-run",
        "training_protocol": protocol,
    }
    result = {
        "approved_plan_sha256": plan_digest,
        "authority": cs.SWEEP_AUTHORITY,
        "capacity_points": list(cs.CAPACITY_POINTS),
        "checkpoints_written": cs.MAX_CHECKPOINTS,
        "code_identity": current_identity,
        "curve_arms": _complete_curve_templates(),
        "curve_checkpoints_written": len(cs.curve_arms()),
        "curve_fits_attempted": len(cs.curve_arms()),
        "data_census": {
            "assignment_sha256": plan["assignment_sha256"],
            "manifest_sha256": plan["manifest_sha256"],
        },
        "design_sha256": cs.DESIGN_CANONICAL_SHA256,
        "equivalence_arms": [
            {
                "comparison": cs.COMPARISON_PASS,
                "seed": seed,
                "status": cs.ARM_COMPLETED,
                "suite": suite,
            }
            for suite, seed in cs.EQUIVALENCE_ARMS
        ],
        "equivalence_checkpoints_written": len(cs.EQUIVALENCE_ARMS),
        "equivalence_fits_attempted": len(cs.EQUIVALENCE_ARMS),
        "exit": cs.X_SWEEP_OK,
        "fits_attempted": cs.MAX_FITS,
        "generation_runs": 0,
        "maximum_budget": budget,
        "mode": "execute",
        "non_dev_reads": 0,
        "reason_class": None,
        "rollouts_spent": 0,
        "run_label": plan["run_label"],
        "training_protocol": protocol,
    }
    analyzer_digest = cs.code_identity(
        {"analyze_dev_fit.py": Path(approved_analysis.__file__).resolve()}
    )["analyze_dev_fit.py"]
    anchor = {
        "inputs": {
            "analysis_code_identity": {"analyze_dev_fit.py": analyzer_digest}
        },
        "paired_macro_f1": {
            "claim_sheet_success_bar": 0.05,
            "sample_sd_S_minus_C1": 0.15,
        },
    }
    return result, plan, anchor, plan_digest, anchor_digest


def test_c7_imports_the_six_frozen_descriptive_definitions():
    """The reader imports the criterion; it does not grow a second definition."""

    tree = ast.parse(Path(analysis.__file__).read_text(encoding="utf-8"))
    imported = set()
    locally_defined = set()
    for node in ast.walk(tree):
        if isinstance(node, ast.ImportFrom) and node.module == "utils.capacity_sweep":
            imported.update(alias.name for alias in node.names)
        if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef)):
            locally_defined.add(node.name)
    required = {
        "classify_shape",
        "derived_label",
        "headroom",
        "pair_constraint",
        "quantize",
        "require_complete_sweep",
    }
    assert required <= imported
    assert required.isdisjoint(locally_defined)


def test_analysis_identity_covers_the_reader_scorer_and_full_sweep_identity():
    """The output binds every module the C7 read executes through, not only its own file."""

    identity = analysis.analysis_code_identity()
    assert set(cs.sweep_code_identity()) <= set(identity)
    assert {"analyze_capacity_sweep.py", "analyze_dev_fit.py", "capacity_sweep.py"} <= set(
        identity
    )
    assert all(len(digest) == 64 for digest in identity.values())


def test_pure_derivation_emits_all_predeclared_fields_without_running_the_sweep():
    """Five points, fifty arms, both curve domains, the crossing fields and one pure label."""

    report = _derive()
    assert len(report["points"]) == 5
    assert len(report["arms"]) == 50
    assert report["eligible_post_anchor_points"] == [40, 48]
    assert report["first_post_anchor_nonnegative_point"] == 40
    assert report["first_post_anchor_nonnegative_point_constraint"] == cs.CONSTRAINT_NONE
    assert report["first_eligible_post_anchor_nonnegative_point"] == 40
    assert report["derived_label"] == cs.LABEL_ELIGIBLE
    assert report["curve_shapes"]["all_points"]["capacity_points"] == list(
        cs.CAPACITY_POINTS
    )
    assert (
        report["curve_shapes"]["all_points"]["paired_mean_S_minus_C1_macro_f1"]
        == cs.SHAPE_STRICTLY_INCREASING
    )
    assert (
        report["curve_shapes"]["eligible_subsequence"]["S_mean_macro_f1"]
        == cs.SHAPE_STRICTLY_INCREASING
    )
    assert {point["pair_constraint"] for point in report["points"]} == {
        cs.CONSTRAINT_NONE
    }


def test_raw_and_quantized_values_and_label_are_recomputable_from_the_record():
    """The tie rule and C6 label live in persisted primitives, not in hidden locals."""

    report = _derive()
    point = next(point for point in report["points"] if point["channels"] == 32)
    raw = point["paired_S_minus_C1_macro_f1_mean"]["raw"]
    assert point["paired_S_minus_C1_macro_f1_mean"]["quantized"] == cs.quantize(raw)
    assert report["source_anchor_sample_sd"]["raw"] == round(
        point["paired_S_minus_C1_macro_f1_sample_sd"]["raw"], 12
    )
    assert report["derived_label"] == cs.derived_label(
        first_post_anchor_nonnegative_point=report[
            "first_post_anchor_nonnegative_point"
        ],
        first_eligible_post_anchor_nonnegative_point=report[
            "first_eligible_post_anchor_nonnegative_point"
        ],
        eligible_post_anchor_points=report["eligible_post_anchor_points"],
    )


def test_each_point_carries_loss_census_and_baseline_context():
    """Frozen section 3's context survives at every capacity point and ranks nothing."""

    report = _derive()
    for point in report["points"]:
        context = point["development_context"]
        assert context["class_counts_by_suite"]["C1"]["sensor"] == 96
        assert context["ood_counts_by_suite"] == {"C1": 0, "S": 0}
        assert context["baselines"]["majority_class"] == "sensor"
        assert set(context["mean_post_fit_full_batch_loss_terms_by_suite"]) == {
            "C1",
            "S",
        }
        assert set(
            context["mean_post_fit_full_batch_loss_terms_by_suite"]["C1"]
        ) == set(LOSS_TERMS)


def test_output_boundary_persists_zero_actions_and_no_causal_claim():
    """The analysis describes; no field spends, selects, escalates or concludes."""

    report = _derive()
    assert report["boundary"] == {
        "capacity_selected": False,
        "development_only": True,
        "fits_run": 0,
        "generalization_established": False,
        "generation_runs": 0,
        "in_sample": True,
        "non_dev_reads": 0,
        "rollouts_spent": 0,
        "threshold_selected": False,
    }
    payload = json.dumps(report, sort_keys=True)
    for forbidden in (
        "CAPACITY_BOUND",
        "NOT_CAPACITY_BOUND",
        "caused_by_capacity",
        "authorized to escalate",
    ):
        assert forbidden not in payload


def test_envelope_gate_accepts_one_complete_exact_state():
    """C10, the current code/design bindings, resource boundary and sourced constants agree."""

    result, plan, anchor, plan_digest, anchor_digest = _envelope_fixture()
    assert analysis.validate_envelope(
        result,
        plan,
        anchor,
        plan_sha256=plan_digest,
        anchor_analysis_sha256=anchor_digest,
    ) == (0.05, 0.15)


@pytest.mark.parametrize("mutation", ["partial", "plan-digest", "non-dev-read"])
def test_envelope_gate_refuses_three_independent_contract_breaks(mutation):
    """A partial curve, wrong plan binding and later-role read each fail before analysis."""

    result, plan, anchor, plan_digest, anchor_digest = _envelope_fixture()
    if mutation == "partial":
        result["curve_arms"][0]["status"] = cs.ARM_REFUSED
    elif mutation == "plan-digest":
        result["approved_plan_sha256"] = "0" * 64
    else:
        result["non_dev_reads"] = 1
    with pytest.raises(analysis.CapacitySweepAnalysisError):
        analysis.validate_envelope(
            result,
            plan,
            anchor,
            plan_sha256=plan_digest,
            anchor_analysis_sha256=anchor_digest,
        )


def test_validate_arms_binds_the_reused_anchor_metrics_to_the_approved_analysis():
    """The 32-channel row is read from its approved source, never accepted by shape alone."""

    arms, _, _, _ = _synthetic_state()
    approved_arms = []
    for arm in arms:
        if arm["channels"] != cs.ANCHOR_CHANNELS:
            continue
        approved_arms.append(
            {
                "checkpoint_name": f"anchor-{arm['suite']}-{arm['seed']}.pt",
                "checkpoint_sha256": arm["checkpoint_sha256"],
                "classification": {
                    "accuracy": arm["accuracy"],
                    "macro_f1": arm["macro_f1"],
                    "per_class_f1": arm["per_class_f1"],
                },
                "seed": arm["seed"],
                "suite": arm["suite"],
            }
        )
    normalized = analysis.validate_arms(
        {
            "code_identity": {"synthetic_fit.py": "b" * 64},
            "curve_arms": arms,
            "training_protocol": {"epochs": 3},
        },
        {
            "arms": approved_arms,
            "inputs": {"fit_code_identity": {"synthetic_fit.py": "b" * 64}},
        },
    )
    assert len(normalized) == 50
    broken = copy.deepcopy(approved_arms)
    broken[0]["classification"]["macro_f1"] += 0.01
    with pytest.raises(analysis.CapacitySweepAnalysisError, match="reused anchor differs"):
        analysis.validate_arms(
            {
                "code_identity": {"synthetic_fit.py": "b" * 64},
                "curve_arms": arms,
                "training_protocol": {"epochs": 3},
            },
            {
                "arms": broken,
                "inputs": {"fit_code_identity": {"synthetic_fit.py": "b" * 64}},
            },
        )
    wrong_identity = copy.deepcopy(arms)
    next(arm for arm in wrong_identity if arm["status"] == cs.ARM_COMPLETED)[
        "fit_code_identity"
    ] = {"synthetic_fit.py": "0" * 64}
    with pytest.raises(analysis.CapacitySweepAnalysisError, match="fitting-code identity"):
        analysis.validate_arms(
            {
                "code_identity": {"synthetic_fit.py": "b" * 64},
                "curve_arms": wrong_identity,
                "training_protocol": {"epochs": 3},
            },
            {
                "arms": approved_arms,
                "inputs": {"fit_code_identity": {"synthetic_fit.py": "b" * 64}},
            },
        )


@pytest.mark.parametrize(
    "bad",
    ["../escape.pt", "/absolute.pt", "C:/drive.pt", "nested\\windows.pt"],
)
def test_checkpoint_names_cannot_escape_or_change_path_dialects(tmp_path, bad):
    """A persisted checkpoint name is a relative POSIX name beneath the supplied root."""

    with pytest.raises(analysis.CapacitySweepAnalysisError):
        analysis.safe_relative_path(tmp_path, bad, "checkpoint")
    assert analysis.safe_relative_path(
        tmp_path, "ch016/C1/model.pt", "checkpoint"
    ) == (tmp_path / "ch016" / "C1" / "model.pt").resolve()


def test_checkpoint_digest_is_checked_before_a_model_is_loaded(tmp_path):
    """A damaged file refuses at the byte identity, without reaching tensor/model code."""

    checkpoint = tmp_path / "synthetic.pt"
    checkpoint.write_bytes(b"not a checkpoint")
    arm = _arm(16, "C1", 0, 0.5)
    with pytest.raises(analysis.CapacitySweepAnalysisError, match="differs from the digest"):
        analysis.evaluate_arm_context(arm, [], checkpoint)


def test_checkpoint_success_path_recomputes_metrics_and_returns_loss_terms(
    tmp_path, monkeypatch
):
    """The C7 scorer actually drives the imported metric and loss definitions."""

    checkpoint = tmp_path / "synthetic.pt"
    checkpoint.write_bytes(b"synthetic checkpoint bytes")
    digest = hashlib.sha256(checkpoint.read_bytes()).hexdigest()
    arm = _arm(16, "C1", 0, 0.5)
    arm["checkpoint_sha256"] = digest
    arm["accuracy"] = 1.0
    arm["macro_f1"] = 0.5
    arm["per_class_f1"] = {
        "healthy": 1.0,
        "structure": 1.0,
        "actuator": 0.0,
        "sensor": 0.0,
    }

    class FakeNetwork:
        def load_state_dict(self, state, strict):
            assert state == {"synthetic": True}
            assert strict is True

        def eval(self):
            return self

        def __call__(self, inputs):
            assert inputs.shape == (2, 1)
            return SimpleNamespace(
                class_logits=torch.tensor(
                    [[4.0, 1.0, 0.0, -1.0], [1.0, 4.0, 0.0, -1.0]]
                )
            )

    monkeypatch.setattr(analysis.torch, "load", lambda *_, **__: {"synthetic": True})
    monkeypatch.setattr(analysis, "TemporalAttributionNet", lambda **_: FakeNetwork())
    monkeypatch.setattr(analysis, "deterministic_conv_precision", nullcontext)
    monkeypatch.setattr(
        analysis.sweep,
        "_stack",
        lambda *_: {
            "inputs": torch.zeros((2, 1)),
            "class_index": torch.tensor([0, 1]),
        },
    )
    monkeypatch.setattr(
        analysis.approved_analysis,
        "post_fit_loss_terms",
        lambda *_: {term: float(index) for index, term in enumerate(LOSS_TERMS)},
    )
    terms = analysis.evaluate_arm_context(arm, [object(), object()], checkpoint)
    assert terms == {term: float(index) for index, term in enumerate(LOSS_TERMS)}
    broken = copy.deepcopy(arm)
    broken["macro_f1"] = 0.51
    with pytest.raises(analysis.CapacitySweepAnalysisError, match="score differs"):
        analysis.evaluate_arm_context(broken, [object(), object()], checkpoint)


def test_development_loader_binds_manifest_assignment_class_census_and_ood(
    monkeypatch,
):
    """Only the approved dev census can feed the per-point context."""

    examples = {
        suite: [
            SimpleNamespace(class_index=index, ood_flag=False) for index in range(4)
        ]
        for suite in ("C1", "S")
    }
    census = {
        "assignment_sha256": "a" * 64,
        "manifest_sha256": "b" * 64,
        "row_disclosure": "synthetic dev only",
        "trajectory_census": {"synthetic": {"C1": 4, "S": 4}},
    }
    monkeypatch.setattr(
        analysis.approved_analysis,
        "load_authorized_examples",
        lambda _: (examples, census),
    )
    approved_counts = {
        suite: {name: 1 for name in approved_analysis.SOURCE_CLASS_ORDER}
        for suite in ("C1", "S")
    }
    loaded, context = analysis.load_development_context(
        data_root=Path("unused"),
        result={"data_census": census},
        anchor_analysis={
            "baselines": {"majority_class": "healthy"},
            "data_census": {
                "class_counts_by_suite": approved_counts,
                "ood_counts_by_suite": {"C1": 0, "S": 0},
            },
        },
    )
    assert loaded == examples
    assert context["class_counts_by_suite"] == approved_counts
    broken = copy.deepcopy(census)
    broken["manifest_sha256"] = "0" * 64
    with pytest.raises(analysis.CapacitySweepAnalysisError, match="loaded dev census differs"):
        analysis.load_development_context(
            data_root=Path("unused"),
            result={"data_census": broken},
            anchor_analysis={
                "baselines": {"majority_class": "healthy"},
                "data_census": {
                    "class_counts_by_suite": approved_counts,
                    "ood_counts_by_suite": {"C1": 0, "S": 0},
                },
            },
        )


def test_analyze_paths_requires_the_explicit_reviewed_result_digest(
    tmp_path, monkeypatch
):
    """The plan and result cannot authenticate only each other after both files mutate."""

    run_root = tmp_path / "run"
    result_path = run_root / cs.RUN_ARTIFACT
    plan_path = tmp_path / "plan.json"
    anchor_path = tmp_path / "anchor.json"
    documents = {
        str(result_path): {"kind": "result"},
        str(plan_path): {"kind": "plan"},
        str(anchor_path): {"kind": "anchor"},
    }
    digests = {
        str(result_path): "a" * 64,
        str(plan_path): "b" * 64,
        str(anchor_path): "c" * 64,
    }
    monkeypatch.setattr(
        analysis,
        "strict_object",
        lambda path, _: documents[str(Path(path))],
    )
    monkeypatch.setattr(
        analysis,
        "canonical_text_sha256",
        lambda path: digests[str(Path(path))],
    )
    monkeypatch.setattr(analysis, "validate_envelope", lambda *_, **__: (0.05, 0.15))
    monkeypatch.setattr(analysis, "validate_arms", lambda *_: [])
    monkeypatch.setattr(analysis, "load_development_context", lambda **_: ({}, {}))
    monkeypatch.setattr(analysis, "evaluate_all_arms", lambda *_, **__: {})
    monkeypatch.setattr(analysis, "derive_analysis", lambda **_: {"analysis": "synthetic"})
    kwargs = {
        "data_root": tmp_path / "data",
        "sweep_result_path": result_path,
        "approved_plan_path": plan_path,
        "approved_anchor_analysis_path": anchor_path,
        "run_root": run_root,
        "anchor_checkpoint_dir": tmp_path / "anchors",
        "expected_sweep_result_sha256": "a" * 64,
    }
    assert analysis.analyze_paths(**kwargs) == {"analysis": "synthetic"}
    kwargs["expected_sweep_result_sha256"] = "0" * 64
    with pytest.raises(analysis.CapacitySweepAnalysisError, match="authorized for analysis"):
        analysis.analyze_paths(**kwargs)


def test_canonical_writer_is_exclusive_and_has_no_final_newline(tmp_path):
    """The exact-state artifact is compact canonical JSON and cannot be overwritten."""

    report = _derive()
    path = analysis.write_exclusive(tmp_path, report)
    payload = path.read_bytes()
    assert b"\r" not in payload and b"\n" not in payload
    assert json.loads(payload) == report
    assert payload == json.dumps(
        report,
        sort_keys=True,
        separators=(",", ":"),
        ensure_ascii=False,
        allow_nan=False,
    ).encode("utf-8")
    with pytest.raises(analysis.CapacitySweepAnalysisError, match="will not be overwritten"):
        analysis.write_exclusive(tmp_path, report)


def test_main_writes_the_artifact_and_drives_the_refusal_on_reuse(tmp_path, monkeypatch):
    """The command path is tested, not only its helper: success then occupied-output refusal."""

    report = _derive()
    monkeypatch.setattr(analysis, "analyze_paths", lambda **_: report)
    output_dir = tmp_path / "output"
    argv = [
        "--data-root",
        str(tmp_path / "data"),
        "--sweep-result",
        str(tmp_path / "run" / cs.RUN_ARTIFACT),
        "--sweep-result-sha256",
        "f" * 64,
        "--approved-plan",
        str(tmp_path / "plan.json"),
        "--approved-anchor-analysis",
        str(tmp_path / "anchor.json"),
        "--run-root",
        str(tmp_path / "run"),
        "--anchor-checkpoint-dir",
        str(tmp_path / "anchors"),
        "--output-dir",
        str(output_dir),
    ]
    assert analysis.main(argv) == analysis.EXIT_CODES[analysis.X_ANALYSIS_OK]
    assert (output_dir / analysis.OUTPUT_NAME).is_file()
    assert analysis.main(argv) == analysis.EXIT_CODES[analysis.X_ANALYSIS_REFUSED]
