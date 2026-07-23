"""Tests for the class-probability channel screen at the selected actuator condition."""

from __future__ import annotations

import sys
from pathlib import Path

import numpy as np
import pytest

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "scripts"))

from screen_actuator_probability_channel import (  # noqa: E402
    ASSESSMENT_SEEDS,
    CRN_REUSE_TOLERANCE,
    GATE_PROBE_PROBABILITY,
    PROBABILITY_SWEEP,
    SELECTED_SEVERITY,
    ProbabilityDiagnosisEstimator,
    build_arm_specs,
    build_audit,
    expected_multiplier,
    gate_discontinuity,
    gate_uncertainty_from_scales,
    paired_channel_extremes,
    probability_label,
    probability_response_curve,
    reachable_multiplier_set,
    require_passing_audit,
    restoration_realization,
    severity_channel_is_flat,
)
from utils.estimator import SOURCE_CLASS_ORDER, EstimatorOutput  # noqa: E402
from utils.recovery_control import (  # noqa: E402
    GainScheduledRecoveryController,
    RecoveryControlConfig,
)


# --------------------------------------------------------------------------- #
# The identity the whole screen rests on, checked against the real controller.
# --------------------------------------------------------------------------- #
def _diagnosis(probability: float, severity: float, uncertainty: float) -> EstimatorOutput:
    """Build one actuator diagnosis at a chosen class probability."""

    probabilities = np.full(len(SOURCE_CLASS_ORDER), (1.0 - probability) / 3.0)
    probabilities[SOURCE_CLASS_ORDER.index("actuator")] = probability
    output = EstimatorOutput(
        step=1000,
        decision_time_s=2.0,
        p_class=probabilities,
        unknown_score=0.0,
        abstain_decision=False,
        location_out=1,
        severity_out=severity,
        severity_uncertainty=uncertainty,
        detection_time_s=2.0,
    )
    output.validate()
    return output


@pytest.mark.parametrize("probability", [0.50, 0.60, 0.70, 0.80, 0.90, 1.00])
def test_real_controller_commands_one_plus_probability_at_the_selected_condition(
    probability: float,
) -> None:
    """`m = 1 + p (cap - 1)` is read off the controller, not assumed from the source.

    At 0.25 remaining gain the cap binds, so `capped_compensation` is exactly 2 and the
    commanded multiplier collapses to `1 + p`. The screen's whole reachable-set argument
    depends on this, so it is verified against the shipped controller.
    """

    config = RecoveryControlConfig()
    controller = GainScheduledRecoveryController(config)
    # A small nominal: the controller's torque limit would clip a unit command and hide
    # the multiplier.
    nominal = np.array([0.01, 0.02])
    command = controller.command_from_nominal(
        _diagnosis(probability, SELECTED_SEVERITY, 0.01), nominal
    )
    applied = command[1] / nominal[1]
    assert applied == pytest.approx(1.0 + probability)
    assert applied == pytest.approx(
        expected_multiplier(probability, config.maximum_gain_compensation)
    )


def test_real_controller_withholds_below_the_probability_threshold() -> None:
    """The sub-threshold probe must produce no action while keeping the class call."""

    config = RecoveryControlConfig()
    controller = GainScheduledRecoveryController(config)
    nominal = np.array([0.01, 0.02])
    output = _diagnosis(GATE_PROBE_PROBABILITY, SELECTED_SEVERITY, 0.01)
    # The actuator is still the unique argmax, so this isolates the threshold.
    assert int(np.argmax(output.p_class)) == SOURCE_CLASS_ORDER.index("actuator")
    assert GATE_PROBE_PROBABILITY < config.source_probability_threshold
    command = controller.command_from_nominal(output, nominal)
    np.testing.assert_allclose(command, nominal)


@pytest.mark.parametrize("severity", [0.01, 0.10, 0.25, 0.40, 0.49, 0.50])
def test_every_severity_at_or_below_one_half_commands_identically(severity: float) -> None:
    """The severity channel is structurally flat at and below `1 / cap`.

    This is why the probability channel is the only live one at the selected condition.
    """

    config = RecoveryControlConfig()
    controller = GainScheduledRecoveryController(config)
    nominal = np.array([0.01, 0.02])
    command = controller.command_from_nominal(_diagnosis(1.0, severity, 0.01), nominal)
    assert command[1] / nominal[1] == pytest.approx(config.maximum_gain_compensation)


def test_severity_above_one_half_leaves_the_flat_region() -> None:
    """Just above the flat boundary the severity channel becomes live again."""

    config = RecoveryControlConfig()
    controller = GainScheduledRecoveryController(config)
    nominal = np.array([0.01, 0.02])
    command = controller.command_from_nominal(_diagnosis(1.0, 0.55, 0.01), nominal)
    assert command[1] / nominal[1] == pytest.approx(1.0 / 0.55)
    assert command[1] / nominal[1] < config.maximum_gain_compensation


# --------------------------------------------------------------------------- #
# Reachable set and flatness derivations.
# --------------------------------------------------------------------------- #
def test_reachable_set_is_closed_by_recorded_constants() -> None:
    """Both endpoints come from the controller config, not from a chosen grid."""

    config = RecoveryControlConfig()
    record = reachable_multiplier_set(config, SELECTED_SEVERITY)
    assert record["cap_binds"]
    assert record["capped_compensation"] == pytest.approx(config.maximum_gain_compensation)
    assert record["reachable_multiplier_low"] == pytest.approx(
        1.0 + config.source_probability_threshold * (config.maximum_gain_compensation - 1.0)
    )
    assert record["reachable_multiplier_high"] == pytest.approx(
        config.maximum_gain_compensation
    )
    # Exact restoration is out of reach: the action is cap-saturated throughout.
    assert record["exact_restoration_multiplier"] == pytest.approx(4.0)
    assert record["cap_shortfall_factor"] == pytest.approx(2.0)


def test_severity_flatness_margin_is_reported_in_error_scales() -> None:
    """The margin to the flat-region boundary is what makes the flatness robust."""

    config = RecoveryControlConfig()
    record = severity_channel_is_flat(
        config, severity=SELECTED_SEVERITY, estimate_error=0.01
    )
    assert record["severity_channel_flat"]
    assert record["flat_region_upper_severity"] == pytest.approx(0.5)
    assert record["margin_to_flat_region_boundary"] == pytest.approx(0.25)
    assert record["margin_in_error_scales"] == pytest.approx(25.0)


# --------------------------------------------------------------------------- #
# The uncertainty handed to the confidence gate.
# --------------------------------------------------------------------------- #
def test_gate_uncertainty_picks_the_conservative_suite() -> None:
    """No arm may be advantaged by an optimistic uncertainty."""

    scales = {
        "C1": {"assessment_residual_rms": 0.0086},
        "S": {"assessment_residual_rms": 0.0102},
    }
    assert gate_uncertainty_from_scales(scales, limit=0.25) == pytest.approx(0.0102)


def test_gate_uncertainty_fails_loudly_when_it_would_close_the_gate() -> None:
    """A value outside the gate would silently collapse every acting arm to no action."""

    scales = {"S": {"assessment_residual_rms": 0.4}}
    with pytest.raises(ValueError, match="does not clear the gate"):
        gate_uncertainty_from_scales(scales, limit=0.25)


# --------------------------------------------------------------------------- #
# The estimator.
# --------------------------------------------------------------------------- #
@pytest.mark.parametrize(
    "probability", [GATE_PROBE_PROBABILITY, 0.50, *PROBABILITY_SWEEP, 1.00]
)
def test_estimator_emits_a_simplex_with_actuator_as_unique_argmax(
    probability: float,
) -> None:
    """Every swept arm must test the probability channel, not the class call."""

    estimator = ProbabilityDiagnosisEstimator(
        probability, severity=SELECTED_SEVERITY, severity_uncertainty=0.01
    )
    output = estimator.update(1000, 2.0, None)
    probabilities = np.asarray(output.p_class, dtype=float)
    assert probabilities.sum() == pytest.approx(1.0)
    assert np.count_nonzero(np.isclose(probabilities, probabilities.max())) == 1
    assert int(np.argmax(probabilities)) == SOURCE_CLASS_ORDER.index("actuator")
    assert probabilities[SOURCE_CLASS_ORDER.index("actuator")] == pytest.approx(probability)


def test_estimator_rejects_a_probability_that_would_test_the_class_call() -> None:
    """Below the even split the actuator stops being the argmax and the arm changes meaning."""

    with pytest.raises(ValueError, match="unique argmax"):
        ProbabilityDiagnosisEstimator(
            0.20, severity=SELECTED_SEVERITY, severity_uncertainty=0.01
        )


def test_estimator_no_action_arm_is_a_healthy_call_the_controller_ignores() -> None:
    """`None` is the no-action arm, not a low-probability actuator call."""

    estimator = ProbabilityDiagnosisEstimator(
        None, severity=SELECTED_SEVERITY, severity_uncertainty=0.01
    )
    output = estimator.update(1000, 2.0, None)
    assert output.p_class[SOURCE_CLASS_ORDER.index("healthy")] == pytest.approx(1.0)
    assert output.location_out == -1
    assert not np.isfinite(output.severity_uncertainty)
    controller = GainScheduledRecoveryController(RecoveryControlConfig())
    nominal = np.array([0.01, 0.02])
    np.testing.assert_allclose(controller.command_from_nominal(output, nominal), nominal)


# --------------------------------------------------------------------------- #
# Arm construction.
# --------------------------------------------------------------------------- #
def test_arm_specs_cover_both_endpoints_the_probe_and_the_sweep_per_seed() -> None:
    """Nine arms per seed, with the gate and certain endpoints as dedicated arms."""

    specs = build_arm_specs(gate_uncertainty=0.01)
    assert len(specs) == 9 * len(ASSESSMENT_SEEDS)
    labels = {spec.label for spec in specs if spec.seed == ASSESSMENT_SEEDS[0]}
    assert labels == {
        "no_action",
        "healthy_reference",
        "gate_probe",
        probability_label(0.50),
        probability_label(1.00),
        *(probability_label(p) for p in PROBABILITY_SWEEP),
    }
    unfaulted = [spec for spec in specs if not spec.faulted]
    assert len(unfaulted) == len(ASSESSMENT_SEEDS)
    assert all(spec.label == "healthy_reference" for spec in unfaulted)


@pytest.mark.parametrize("bad", [0.50, 1.00, 0.40, 1.20])
def test_arm_specs_reject_a_swept_probability_that_is_not_strictly_interior(
    bad: float,
) -> None:
    """The endpoints own their own arms; a sweep point may never duplicate them."""

    with pytest.raises(ValueError, match="outside"):
        build_arm_specs(gate_uncertainty=0.01, probabilities=(bad,))


# --------------------------------------------------------------------------- #
# Analysis.
# --------------------------------------------------------------------------- #
def _rows(reductions: dict[float, float]) -> list[dict]:
    """Build arm rows whose `J_5s` produce the requested reductions exactly."""

    rows: list[dict] = []
    base_j = 1.0
    healthy_j = 0.8
    for seed in ASSESSMENT_SEEDS:
        rows.append(_row(seed, "no_action", None, base_j, 1.0, 0))
        rows.append(_row(seed, "healthy_reference", None, healthy_j, 1.0, 0))
        rows.append(_row(seed, "gate_probe", GATE_PROBE_PROBABILITY, base_j, 1.0, 0))
        for probability, reduction in reductions.items():
            rows.append(
                _row(
                    seed,
                    probability_label(probability),
                    probability,
                    base_j * (1.0 - reduction / 100.0),
                    1.0 + probability,
                    12,
                )
            )
    return rows


def _row(
    seed: int,
    label: str,
    probability: float | None,
    j_5s_value: float,
    multiplier: float,
    changed: int,
) -> dict:
    """One arm row in the shape `run_probability_arm` returns."""

    return {
        "seed": seed,
        "label": label,
        "faulted": label != "healthy_reference",
        "probability": probability,
        "severity_uncertainty": 0.01,
        "run_id": f"probability-{label}-{seed}-S",
        "j_5s": j_5s_value,
        "applied_multiplier_max": multiplier,
        "classification_evaluations": 1,
        "recovery_command_changed_steps": changed,
        "a1_incident_steps": 0,
        "saturation_steps": 0,
        "peak_contact_force_n": 0.09,
        "max_abs_gauge_microstrain": 3.4,
    }


def test_response_curve_spans_the_reachable_set_and_pairs_within_seed() -> None:
    """The curve runs the gate endpoint to the certain endpoint, paired per seed."""

    reductions = {0.50: 5.0, 0.60: 6.0, 0.70: 7.0, 0.80: 8.0, 0.90: 9.0, 1.00: 10.0}
    curve = probability_response_curve(_rows(reductions))
    assert curve["probability_span"] == [0.50, 1.00]
    assert len(curve["points"]) == len(reductions)
    assert curve["reduction_at_gate_pct"] == pytest.approx(5.0)
    assert curve["reduction_at_certainty_pct"] == pytest.approx(10.0)
    assert curve["reachable_reduction_span_pct"] == pytest.approx(5.0)
    assert not curve["reachable_span_clears_bar"]
    assert curve["local_slope_pct_per_unit_probability"] == pytest.approx(10.0)
    for point in curve["points"]:
        assert point["mean_applied_multiplier"] == pytest.approx(1.0 + point["probability"])


def test_response_curve_reports_a_span_that_clears_the_bar_when_it_does() -> None:
    """The screen must be able to report a positive result, not only a negative one."""

    reductions = {0.50: 1.0, 0.60: 5.0, 0.70: 9.0, 0.80: 13.0, 0.90: 17.0, 1.00: 21.0}
    curve = probability_response_curve(_rows(reductions))
    assert curve["reachable_reduction_span_pct"] == pytest.approx(20.0)
    assert curve["reachable_span_clears_bar"]


def test_gate_discontinuity_decomposes_the_total_into_jump_plus_graded_span() -> None:
    """The gate and the graded channel are separate quantities and must stay separate."""

    curve = {
        "reduction_at_gate_pct": 7.0,
        "reduction_at_certainty_pct": 10.0,
        "reachable_reduction_span_pct": 3.0,
    }
    gate = gate_discontinuity(curve, probe_reduction_pct=0.0)
    assert gate["gate_entry_jump_pct"] == pytest.approx(7.0)
    assert gate["graded_span_above_gate_pct"] == pytest.approx(3.0)
    assert gate["total_channel_span_including_gate_pct"] == pytest.approx(10.0)
    assert not gate["graded_span_clears_bar"]
    assert gate["total_span_clears_bar"]
    assert gate["total_channel_span_including_gate_pct"] == pytest.approx(
        gate["graded_span_above_gate_pct"] + gate["gate_entry_jump_pct"]
    )


def test_paired_extremes_are_in_contract_units_not_reduction_differences() -> None:
    """The contract's quantity is larger than a difference of two no-action reductions.

    `100 (J_C1 - J_S) / J_C1` divides by the *conventional arm*, not by the no-action arm.
    Quoting the reduction span against the Claim Sheet bar would understate the very
    quantity the bar is written in, by `1 / (1 - r_low / 100)`.
    """

    reductions = {0.50: 5.0, 0.60: 6.0, 0.70: 7.0, 0.80: 9.0, 0.90: 11.0, 1.00: 12.0}
    rows = _rows(reductions)
    extremes = paired_channel_extremes(rows)
    curve = probability_response_curve(rows)
    # J at the gate is 0.95, at certainty 0.88: paired = 100 (0.95 - 0.88) / 0.95.
    assert extremes["max_graded_paired_pct"] == pytest.approx(100.0 * 0.07 / 0.95)
    assert extremes["mean_graded_paired_pct"] == pytest.approx(100.0 * 0.07 / 0.95)
    # Strictly larger than the reduction span, by exactly the documented factor.
    span = curve["reachable_reduction_span_pct"]
    assert span == pytest.approx(7.0)
    assert extremes["max_graded_paired_pct"] > span
    assert extremes["max_graded_paired_pct"] == pytest.approx(span / (1.0 - 5.0 / 100.0))
    # The gate-crossing extreme is the full reduction at certainty: J_no_action is 1.0.
    assert extremes["max_gate_crossing_paired_pct"] == pytest.approx(12.0)
    assert not extremes["graded_clears_bar"]
    assert extremes["gate_crossing_clears_bar"]


def test_paired_extremes_report_clearing_the_bar_when_they_do() -> None:
    """The screen must be able to report a positive result in contract units."""

    reductions = {0.50: 1.0, 0.60: 5.0, 0.70: 9.0, 0.80: 13.0, 0.90: 17.0, 1.00: 30.0}
    extremes = paired_channel_extremes(_rows(reductions))
    assert extremes["max_graded_paired_pct"] == pytest.approx(
        100.0 * (0.99 - 0.70) / 0.99
    )
    assert extremes["graded_clears_bar"]


def test_restoration_realization_uses_the_deficit_over_one_plus_deficit_ceiling() -> None:
    """The analytic ceiling is `D / (1 + D)`, always below the deficit itself."""

    reductions = {0.50: 5.0, 0.60: 6.0, 0.70: 7.0, 0.80: 8.0, 0.90: 9.0, 1.00: 10.0}
    record = restoration_realization(_rows(reductions))
    assert len(record["per_seed"]) == len(ASSESSMENT_SEEDS)
    row = record["per_seed"][0]
    # J_no_action 1.0 against J_healthy 0.8: deficit 25%, ceiling 20%.
    assert row["no_action_deficit_pct"] == pytest.approx(25.0)
    assert row["analytic_exact_restoration_ceiling_pct"] == pytest.approx(20.0)
    assert row["realized_reduction_at_certainty_pct"] == pytest.approx(10.0)
    assert row["realization_fraction"] == pytest.approx(0.5)
    assert record["same_direction_on_every_seed"]


# --------------------------------------------------------------------------- #
# Integrity.
# --------------------------------------------------------------------------- #
def _recorded() -> dict[str, dict[int, float]]:
    """Recorded `J_5s` matching `_rows` exactly."""

    return {
        "no_action": {seed: 1.0 for seed in ASSESSMENT_SEEDS},
        "healthy_reference": {seed: 0.8 for seed in ASSESSMENT_SEEDS},
    }


def test_audit_passes_on_well_formed_rows() -> None:
    """The happy path, so the failure tests below mean something."""

    reductions = {0.50: 5.0, 0.60: 6.0, 0.70: 7.0, 0.80: 8.0, 0.90: 9.0, 1.00: 10.0}
    audit = build_audit(_rows(reductions), _recorded(), capped_compensation=2.0)
    require_passing_audit(audit)
    assert audit["n_recorded_comparisons"] == 2 * len(ASSESSMENT_SEEDS)
    assert audit["max_abs_j5s_difference_vs_recorded"] <= CRN_REUSE_TOLERANCE


def test_audit_catches_a_broken_common_random_number_reuse() -> None:
    """A drifted no-action trajectory invalidates the whole construction."""

    reductions = {0.50: 5.0, 0.60: 6.0, 0.70: 7.0, 0.80: 8.0, 0.90: 9.0, 1.00: 10.0}
    rows = _rows(reductions)
    for row in rows:
        if row["label"] == "no_action":
            row["j_5s"] += 1.0e-6
    audit = build_audit(rows, _recorded(), capped_compensation=2.0)
    assert not audit["no_action_matches_recorded"]
    with pytest.raises(RuntimeError, match="no_action_matches_recorded"):
        require_passing_audit(audit)


def test_audit_catches_a_sub_threshold_probe_that_acted() -> None:
    """If the gate probe acts, the gate discontinuity measurement is meaningless."""

    reductions = {0.50: 5.0, 0.60: 6.0, 0.70: 7.0, 0.80: 8.0, 0.90: 9.0, 1.00: 10.0}
    rows = _rows(reductions)
    for row in rows:
        if row["label"] == "gate_probe":
            row["recovery_command_changed_steps"] = 4
    audit = build_audit(rows, _recorded(), capped_compensation=2.0)
    assert not audit["withheld_arms_changed_zero_commands"]


def test_audit_catches_a_multiplier_that_does_not_match_its_probability() -> None:
    """The `m = 1 + p (cap - 1)` identity is the screen's core claim; it is checked."""

    reductions = {0.50: 5.0, 0.60: 6.0, 0.70: 7.0, 0.80: 8.0, 0.90: 9.0, 1.00: 10.0}
    rows = _rows(reductions)
    for row in rows:
        if row["label"] == probability_label(0.70):
            row["applied_multiplier_max"] = 1.90
    audit = build_audit(rows, _recorded(), capped_compensation=2.0)
    assert not audit["applied_multipliers_match_probability"]


def test_audit_refuses_a_vacuous_common_random_number_check() -> None:
    """A check that compared nothing must not report success."""

    reductions = {0.50: 5.0, 0.60: 6.0, 0.70: 7.0, 0.80: 8.0, 0.90: 9.0, 1.00: 10.0}
    with pytest.raises(ValueError, match="nothing was checked"):
        build_audit(_rows(reductions), {"absent_label": {}}, capped_compensation=2.0)


@pytest.mark.parametrize(
    "failed_field",
    [
        "no_action_matches_recorded",
        "single_evaluation",
        "withheld_arms_changed_zero_commands",
        "acting_arms_acted",
        "zero_a1_incidents",
        "zero_saturation",
        "applied_multipliers_match_probability",
    ],
)
def test_every_report_integrity_condition_is_a_fail_loud_gate(failed_field: str) -> None:
    """A false audit field cannot survive into a generated narrative."""

    audit = {
        "no_action_matches_recorded": True,
        "single_evaluation": True,
        "withheld_arms_changed_zero_commands": True,
        "acting_arms_acted": True,
        "zero_a1_incidents": True,
        "zero_saturation": True,
        "applied_multipliers_match_probability": True,
    }
    require_passing_audit(audit)
    audit[failed_field] = False
    with pytest.raises(RuntimeError, match=failed_field):
        require_passing_audit(audit)


def test_a_missing_audit_field_fails_rather_than_defaulting_to_pass() -> None:
    """An audit that stopped emitting a condition must not silently pass."""

    with pytest.raises(RuntimeError, match="zero_saturation"):
        require_passing_audit(
            {
                "no_action_matches_recorded": True,
                "single_evaluation": True,
                "withheld_arms_changed_zero_commands": True,
                "acting_arms_acted": True,
                "zero_a1_incidents": True,
                "applied_multipliers_match_probability": True,
            }
        )
