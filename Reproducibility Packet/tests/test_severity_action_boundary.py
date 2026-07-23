"""Tests for the cap-boundary action screen and severity-uncertainty diagnostics."""

from __future__ import annotations

import sys
from pathlib import Path

import numpy as np
import pytest

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "scripts"))

from screen_severity_action_boundary import (  # noqa: E402
    ASSESSMENT_SEEDS,
    BOUNDARY_SEVERITY,
    CRN_REUSE_TOLERANCE,
    FixedDiagnosisEstimator,
    build_arm_specs,
    build_audit,
    cross_seed_calibration_uncertainty,
    disjoint_assessment_residual_diagnostics,
    multiplier_sensitivity_curve,
    paired_boundary_result,
    require_passing_audit,
    severity_difference_envelope,
)
from utils.estimator import (  # noqa: E402
    SOURCE_CLASS_ORDER,
    SeverityRidgeHead,
    leave_one_group_out_residuals,
)
from utils.recovery_control import RecoveryControlConfig  # noqa: E402


# --------------------------------------------------------------------------- #
# Cross-seed calibration uncertainty plus the disjoint assessment check.
# --------------------------------------------------------------------------- #
def _grouped_linear_problem(
    n_groups: int = 6, per_group: int = 8, width: int = 5, noise: float = 0.02
) -> tuple[np.ndarray, np.ndarray, np.ndarray]:
    """Return a grouped linear regression problem with a per-group offset.

    The offset is what makes a held-out group genuinely harder than a held-out row: it
    is shared inside a group, exactly like a sensor seed's noise realization.
    """

    rng = np.random.default_rng(11)
    features, targets, groups = [], [], []
    weights = rng.normal(size=width)
    for group in range(n_groups):
        offset = 0.05 * rng.normal()
        block = rng.normal(size=(per_group, width))
        features.append(block)
        targets.append(
            0.5 + block @ weights * 0.01 + offset + noise * rng.normal(size=per_group)
        )
        groups.extend([group] * per_group)
    return (
        np.vstack(features),
        np.concatenate(targets),
        np.asarray(groups),
    )


def test_leave_one_group_out_returns_one_residual_per_row_in_input_order() -> None:
    """Every row gets a residual from a head that never saw its group."""

    features, targets, groups = _grouped_linear_problem()
    residuals = leave_one_group_out_residuals(
        features, targets, groups, regularization=1.0
    )
    assert residuals.shape == targets.shape
    for label in np.unique(groups):
        held = groups == label
        head = SeverityRidgeHead(regularization=1.0).fit(
            features[~held], targets[~held]
        )
        assert residuals[held] == pytest.approx(head.predict(features[held]) - targets[held])


def test_cross_seed_dispersion_exceeds_the_in_sample_dispersion() -> None:
    """The in-sample residual std understates the error on unseen groups.

    This is the whole reason the screen computes a held-out number: the recovery
    controller gates on `severity_uncertainty`, and handing it a training residual
    reports the head as more certain than it is.
    """

    features, targets, groups = _grouped_linear_problem()
    head = SeverityRidgeHead(regularization=1.0).fit(features, targets)
    residuals = leave_one_group_out_residuals(
        features, targets, groups, regularization=1.0
    )
    assert residuals.std(ddof=1) > head.train_residual_std


def test_cross_seed_uncertainty_reads_a_recorded_feature_bundle() -> None:
    """The screen-level wrapper consumes the recorded bundle shape and reports folds."""

    features, targets, groups = _grouped_linear_problem()
    roles = np.asarray(["tuning"] * targets.size, dtype=object)
    record = cross_seed_calibration_uncertainty(
        {
            "features": features,
            "severities": targets,
            "seeds": groups,
            "roles": roles,
        },
        regularization=1.0,
    )
    assert record["n_calibration_folds"] == np.unique(groups).size
    assert record["n_calibration_residuals"] == targets.size
    assert record["calibration_cross_seed_residual_std"] > 0.0
    assert record["calibration_cross_seed_residual_mean_abs"] > 0.0


def test_disjoint_assessment_diagnostics_use_the_recorded_predictions() -> None:
    """The actual assessment role is reported separately from tuning cross-validation."""

    record = disjoint_assessment_residual_diagnostics(
        {
            "predictions": [
                {"estimate": 0.48, "severity": 0.50},
                {"estimate": 0.55, "severity": 0.50},
                {"estimate": 0.67, "severity": 0.70},
            ]
        }
    )
    residuals = np.asarray([-0.02, 0.05, -0.03])
    assert record["assessment_residual_std"] == pytest.approx(residuals.std(ddof=1))
    assert record["assessment_residual_mean"] == pytest.approx(residuals.mean())
    assert record["assessment_residual_mean_abs"] == pytest.approx(
        np.mean(np.abs(residuals))
    )
    assert record["n_assessment_residuals"] == 3


def test_leave_one_group_out_fails_loudly_on_bad_input() -> None:
    """Shape disagreements and a single group are errors, not silently degraded output."""

    features, targets, groups = _grouped_linear_problem(n_groups=2)
    with pytest.raises(ValueError, match="2-D"):
        leave_one_group_out_residuals(
            features[0], targets, groups, regularization=1.0
        )
    with pytest.raises(ValueError, match="shape"):
        leave_one_group_out_residuals(
            features, targets[:-1], groups, regularization=1.0
        )
    with pytest.raises(ValueError, match="two distinct groups"):
        leave_one_group_out_residuals(
            features, targets, np.zeros_like(groups), regularization=1.0
        )


# --------------------------------------------------------------------------- #
# The fixed diagnosis estimator — the only thing that varies across arms.
# --------------------------------------------------------------------------- #
def test_fixed_estimator_reports_actuator_with_the_commanded_severity() -> None:
    """A severity arm calls the actuator class one-hot and carries its own severity."""

    estimator = FixedDiagnosisEstimator(0.5, severity_uncertainty=0.01)
    output = estimator.update(1136, 2.272, None)
    output.validate()
    assert output.p_class[SOURCE_CLASS_ORDER.index("actuator")] == 1.0
    assert output.severity_out == pytest.approx(0.5)
    assert output.severity_uncertainty == pytest.approx(0.01)
    assert output.location_out == 1
    assert not output.abstain_decision


def test_fixed_estimator_none_severity_is_the_no_action_arm() -> None:
    """`None` is a healthy call the recovery controller must not act on."""

    estimator = FixedDiagnosisEstimator(None, severity_uncertainty=0.0)
    output = estimator.update(1136, 2.272, None)
    output.validate()
    assert output.p_class[SOURCE_CLASS_ORDER.index("healthy")] == 1.0
    assert output.severity_out == 0.0
    assert not np.isfinite(output.severity_uncertainty)
    assert output.location_out == -1


def test_fixed_estimator_rejects_impossible_inputs() -> None:
    """An out-of-range severity or a negative uncertainty is an error."""

    with pytest.raises(ValueError, match="severity"):
        FixedDiagnosisEstimator(0.0, severity_uncertainty=0.0)
    with pytest.raises(ValueError, match="severity"):
        FixedDiagnosisEstimator(1.5, severity_uncertainty=0.0)
    with pytest.raises(ValueError, match="uncertainty"):
        FixedDiagnosisEstimator(0.5, severity_uncertainty=-1.0)


# --------------------------------------------------------------------------- #
# Arm construction.
# --------------------------------------------------------------------------- #
def _estimates() -> dict[str, dict[int, float]]:
    """Return paired per-seed estimates straddling the cap-2 kink."""

    return {
        "C1": {seed: 0.498 for seed in ASSESSMENT_SEEDS},
        "S": {seed: 0.512 for seed in ASSESSMENT_SEEDS},
    }


def test_arm_specs_cover_every_reference_and_sweep_point_per_seed() -> None:
    """Each seed carries its own healthy, no-action, oracle, suite, and sweep arms."""

    specs = build_arm_specs(_estimates(), {"C1": 0.007, "S": 0.011}, multipliers=(1.7, 1.9))
    by_seed: dict[int, set[str]] = {}
    for spec in specs:
        by_seed.setdefault(spec.seed, set()).add(spec.label)
    assert set(by_seed) == set(ASSESSMENT_SEEDS)
    for labels in by_seed.values():
        assert labels == {
            "healthy_reference",
            "no_action",
            "oracle",
            "deployable_C1",
            "deployable_S",
            "multiplier_1.70",
            "multiplier_1.90",
        }
    healthy = [spec for spec in specs if spec.label == "healthy_reference"]
    assert all(not spec.faulted and spec.commanded_severity is None for spec in healthy)
    assert all(
        spec.faulted for spec in specs if spec.label != "healthy_reference"
    )
    oracle = next(spec for spec in specs if spec.label == "oracle")
    assert oracle.commanded_severity == pytest.approx(BOUNDARY_SEVERITY)


def test_arm_specs_carry_each_suites_own_calibration_uncertainty() -> None:
    """The uncertainty reported to the gate is the suite's, not a shared constant."""

    specs = build_arm_specs(_estimates(), {"C1": 0.007, "S": 0.011}, multipliers=(1.9,))
    c1 = next(spec for spec in specs if spec.label == "deployable_C1")
    s = next(spec for spec in specs if spec.label == "deployable_S")
    assert c1.severity_uncertainty == pytest.approx(0.007)
    assert s.severity_uncertainty == pytest.approx(0.011)
    assert c1.commanded_severity == pytest.approx(0.498)
    assert s.commanded_severity == pytest.approx(0.512)


def test_arm_specs_reject_the_separate_cap_point_and_out_of_range_multiplier() -> None:
    """The oracle owns the cap point; every explicitly swept point must be below it."""

    cap = RecoveryControlConfig().maximum_gain_compensation
    with pytest.raises(ValueError, match="outside"):
        build_arm_specs(
            _estimates(), {"C1": 0.007, "S": 0.011}, multipliers=(cap,)
        )
    with pytest.raises(ValueError, match="outside"):
        build_arm_specs(_estimates(), {"C1": 0.007, "S": 0.011}, multipliers=(1.0,))


def test_arm_specs_fail_loudly_on_a_missing_recorded_estimate() -> None:
    """A seed with no recorded estimate cannot be silently dropped."""

    estimates = _estimates()
    del estimates["S"][ASSESSMENT_SEEDS[0]]
    with pytest.raises(ValueError, match="no recorded estimate"):
        build_arm_specs(estimates, {"C1": 0.007, "S": 0.011}, multipliers=(1.9,))


# --------------------------------------------------------------------------- #
# Analysis.
# --------------------------------------------------------------------------- #
def _rows(j_by_label: dict[str, float], seeds: tuple[int, ...] = ASSESSMENT_SEEDS):
    """Return arm rows with one tracking integral per label, shared across seeds."""

    floor = RecoveryControlConfig().minimum_gain_remaining
    cap = RecoveryControlConfig().maximum_gain_compensation
    severities = {
        "healthy_reference": None,
        "no_action": None,
        "oracle": BOUNDARY_SEVERITY,
        "deployable_C1": 0.498,
        "deployable_S": 0.512,
    }
    rows = []
    for seed in seeds:
        for label, value in j_by_label.items():
            severity = severities.get(label)
            if severity is None and label.startswith("multiplier_"):
                severity = 1.0 / float(label.split("_")[1])
            multiplier = (
                1.0 if severity is None else min(1.0 / max(severity, floor), cap)
            )
            rows.append(
                {
                    "seed": seed,
                    "label": label,
                    "faulted": label != "healthy_reference",
                    "commanded_severity": severity,
                    "severity_uncertainty": 0.0,
                    "run_id": f"boundary-{label}-{seed}-S",
                    "j_5s": float(value),
                    "applied_multiplier_max": float(multiplier),
                    "classification_evaluations": 1,
                    "recovery_command_changed_steps": 0 if severity is None else 900,
                    "a1_incident_steps": 0,
                    "saturation_steps": 0,
                    "peak_contact_force_n": 2.1,
                    "max_abs_gauge_microstrain": 38.4,
                }
            )
    return rows


def test_paired_result_uses_the_contract_quantity_with_c1_in_the_denominator() -> None:
    """`100 * (J_C1 - J_S) / J_C1`, positive when S is better — schema section G."""

    rows = _rows(
        {
            "healthy_reference": 0.86,
            "no_action": 1.00,
            "oracle": 0.88,
            "deployable_C1": 0.90,
            "deployable_S": 0.99,
        }
    )
    result = paired_boundary_result(rows)
    assert result["mean_paired_reduction_pct"] == pytest.approx(
        100.0 * (0.90 - 0.99) / 0.90
    )
    assert result["n_seeds_favouring_c1"] == len(ASSESSMENT_SEEDS)
    assert result["n_seeds_favouring_s"] == 0
    assert result["mean_no_action_deficit_pct"] == pytest.approx(
        100.0 * (1.00 - 0.86) / 0.86
    )
    assert result["mean_oracle_reduction_vs_no_action_pct"] == pytest.approx(
        100.0 * (1.00 - 0.88) / 1.00
    )


def test_paired_result_records_an_exactly_identical_seed_as_identical() -> None:
    """Two suites landing on the same side of the kink must read as exactly zero."""

    rows = _rows(
        {
            "healthy_reference": 0.86,
            "no_action": 1.00,
            "oracle": 0.88,
            "deployable_C1": 0.90,
            "deployable_S": 0.90,
        }
    )
    result = paired_boundary_result(rows)
    assert result["n_seeds_identical"] == len(ASSESSMENT_SEEDS)
    assert result["max_abs_paired_reduction_pct"] == pytest.approx(0.0)


def test_paired_result_fails_loudly_on_a_missing_arm() -> None:
    """A dropped arm must not silently shrink the comparison."""

    rows = [
        row
        for row in _rows(
            {
                "healthy_reference": 0.86,
                "no_action": 1.00,
                "oracle": 0.88,
                "deployable_C1": 0.90,
                "deployable_S": 0.91,
            }
        )
        if not (row["label"] == "deployable_S" and row["seed"] == ASSESSMENT_SEEDS[0])
    ]
    with pytest.raises(ValueError, match="missing boundary arm"):
        paired_boundary_result(rows)


def test_sensitivity_curve_includes_the_cap_arm_and_reports_its_span() -> None:
    """The oracle arm is the cap point of the sweep, and the span is the bound."""

    rows = _rows(
        {
            "healthy_reference": 0.86,
            "no_action": 1.00,
            "oracle": 0.88,
            "deployable_C1": 0.90,
            "deployable_S": 0.91,
            "multiplier_1.70": 0.92,
            "multiplier_1.90": 0.89,
        }
    )
    curve = multiplier_sensitivity_curve(rows, multipliers=(1.70, 1.90), cap=2.0)
    assert [point["commanded_multiplier"] for point in curve["points"]] == [1.70, 1.90, 2.0]
    assert curve["multiplier_span"] == [1.70, 2.0]
    # Reductions are 8%, 11%, 12% of J_no_action = 1.00.
    assert curve["reduction_span_pct"] == pytest.approx(4.0)
    assert curve["reduction_at_cap_pct"] == pytest.approx(12.0)
    assert curve["best_multiplier"] == pytest.approx(2.0)
    assert curve["local_slope_pct_per_unit_multiplier_at_cap"] == pytest.approx(
        (12.0 - 11.0) / (2.0 - 1.90)
    )


def test_envelope_converts_the_spread_without_calling_linearization_a_bound() -> None:
    """The local slope and whole-sweep span remain explicitly different diagnostics."""

    curve = {
        "local_slope_pct_per_unit_multiplier_at_cap": 10.0,
        "reduction_span_pct": 4.0,
    }
    envelope = severity_difference_envelope(curve, 0.07)
    assert envelope["local_linearized_difference_pct"] == pytest.approx(0.7)
    assert not envelope["local_linearized_difference_clears_bar"]
    assert not envelope["swept_span_clears_bar"]
    big = severity_difference_envelope(
        {"local_slope_pct_per_unit_multiplier_at_cap": -200.0, "reduction_span_pct": 40.0},
        0.07,
    )
    assert big["local_linearized_difference_pct"] == pytest.approx(14.0)
    assert big["local_linearized_difference_clears_bar"]
    assert big["swept_span_clears_bar"]


# --------------------------------------------------------------------------- #
# Audit.
# --------------------------------------------------------------------------- #
def test_audit_detects_a_broken_common_random_number_reuse() -> None:
    """The screen commands an estimate produced in another run; the reuse must be pinned.

    If the no-action trajectories stop matching the recorded ones, the recorded estimate
    is no longer the estimate a deployable head would have produced here, and the whole
    construction is invalid. That has to fail loudly rather than shift a number.
    """

    rows = _rows(
        {
            "healthy_reference": 0.86,
            "no_action": 1.00,
            "oracle": 0.88,
            "deployable_C1": 0.90,
            "deployable_S": 0.91,
        }
    )
    matching = {
        "no_action": {seed: 1.00 for seed in ASSESSMENT_SEEDS},
        "healthy_reference": {seed: 0.86 for seed in ASSESSMENT_SEEDS},
    }
    audit = build_audit(rows, matching, cap=2.0, floor=0.25)
    assert audit["no_action_matches_recorded"]
    assert audit["n_arms_checked_against_recorded"] == 2 * len(ASSESSMENT_SEEDS)
    assert audit["max_abs_j5s_difference_vs_recorded"] <= CRN_REUSE_TOLERANCE

    drifted = {
        "no_action": {seed: 1.00 for seed in ASSESSMENT_SEEDS},
        "healthy_reference": {seed: 0.86 for seed in ASSESSMENT_SEEDS},
    }
    drifted["no_action"][ASSESSMENT_SEEDS[0]] = 1.0001
    broken = build_audit(rows, drifted, cap=2.0, floor=0.25)
    assert not broken["no_action_matches_recorded"]
    assert broken["max_abs_j5s_difference_vs_recorded"] == pytest.approx(1.0e-4)


def test_audit_checks_the_applied_multiplier_against_the_commanded_severity() -> None:
    """What the plant saw has to be what the severity number asked for."""

    rows = _rows(
        {
            "healthy_reference": 0.86,
            "no_action": 1.00,
            "oracle": 0.88,
            "deployable_C1": 0.90,
            "deployable_S": 0.91,
        }
    )
    recorded = {
        "no_action": {seed: 1.00 for seed in ASSESSMENT_SEEDS},
        "healthy_reference": {seed: 0.86 for seed in ASSESSMENT_SEEDS},
    }
    assert build_audit(rows, recorded, cap=2.0, floor=0.25)[
        "applied_multipliers_match_command"
    ]
    for row in rows:
        if row["label"] == "deployable_S":
            row["applied_multiplier_max"] += 0.01
    assert not build_audit(rows, recorded, cap=2.0, floor=0.25)[
        "applied_multipliers_match_command"
    ]


def test_audit_requires_action_arms_to_have_acted() -> None:
    """An action arm that changed no command silently measured the no-action arm."""

    rows = _rows(
        {
            "healthy_reference": 0.86,
            "no_action": 1.00,
            "oracle": 0.88,
            "deployable_C1": 0.90,
            "deployable_S": 0.91,
        }
    )
    recorded = {
        "no_action": {seed: 1.00 for seed in ASSESSMENT_SEEDS},
        "healthy_reference": {seed: 0.86 for seed in ASSESSMENT_SEEDS},
    }
    assert build_audit(rows, recorded, cap=2.0, floor=0.25)["action_arms_acted"]
    for row in rows:
        if row["label"] == "oracle":
            row["recovery_command_changed_steps"] = 0
    assert not build_audit(rows, recorded, cap=2.0, floor=0.25)["action_arms_acted"]


def test_audit_fails_loudly_when_nothing_was_checked() -> None:
    """An empty recorded mapping must not read as a passing reuse check."""

    rows = _rows({"healthy_reference": 0.86, "no_action": 1.00, "oracle": 0.88,
                  "deployable_C1": 0.90, "deployable_S": 0.91})
    with pytest.raises(ValueError, match="nothing was checked"):
        build_audit(rows, {"absent_label": {}}, cap=2.0, floor=0.25)


@pytest.mark.parametrize(
    "failed_field",
    [
        "no_action_matches_recorded",
        "single_evaluation",
        "no_action_changed_zero_commands",
        "action_arms_acted",
        "zero_a1_incidents",
        "zero_saturation",
        "applied_multipliers_match_command",
    ],
)
def test_every_report_integrity_condition_is_a_fail_loud_gate(
    failed_field: str,
) -> None:
    """A false audit field cannot survive into a generated positive narrative."""

    audit = {
        "no_action_matches_recorded": True,
        "single_evaluation": True,
        "no_action_changed_zero_commands": True,
        "action_arms_acted": True,
        "zero_a1_incidents": True,
        "zero_saturation": True,
        "applied_multipliers_match_command": True,
    }
    require_passing_audit(audit)
    audit[failed_field] = False
    with pytest.raises(RuntimeError, match=failed_field):
        require_passing_audit(audit)
