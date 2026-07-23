"""Tests for the severity-estimation-quality screen and its severity read-out head."""

from __future__ import annotations

import sys
from pathlib import Path

import numpy as np
import pytest

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "scripts"))

from screen_severity_estimation_quality import (  # noqa: E402
    action_sensitivity_map,
    compare_against_oracle_action,
    compare_commanded_actions,
    exact_restoration_ceiling_pct,
    gain_action_multiplier,
    severity_sensitive_interval,
)
from utils.estimator import (  # noqa: E402
    SOURCE_CLASS_ORDER,
    EstimatorOutput,
    SeverityRidgeHead,
)
from utils.recovery_control import (  # noqa: E402
    GainScheduledRecoveryController,
    RecoveryControlConfig,
)


def _actuator_output(severity: float) -> EstimatorOutput:
    """Return a confident one-hot actuator diagnosis carrying one severity read-out."""

    probabilities = np.zeros(len(SOURCE_CLASS_ORDER), dtype=float)
    probabilities[SOURCE_CLASS_ORDER.index("actuator")] = 1.0
    return EstimatorOutput(
        step=1200,
        decision_time_s=2.4,
        p_class=probabilities,
        unknown_score=0.0,
        abstain_decision=False,
        location_out=1,
        severity_out=float(severity),
        severity_uncertainty=0.0,
        detection_time_s=2.4,
    )


# --------------------------------------------------------------------------- #
# Part A — the analytic multiplier must be the real controller's multiplier.
# --------------------------------------------------------------------------- #
def test_analytic_multiplier_matches_the_real_recovery_controller() -> None:
    """The pure function is pinned to the controller, not an independent model of it.

    Part A's whole argument rests on the shape of the applied multiplier. If the analytic
    function ever drifts from `GainScheduledRecoveryController`, the map describes a
    controller the project does not run.
    """

    nominal = np.array([0.01, 0.02])
    for cap in (2.0, 3.0, 4.0, 8.0):
        config = RecoveryControlConfig(maximum_gain_compensation=cap)
        controller = GainScheduledRecoveryController(config)
        for severity in np.linspace(0.05, 1.0, 40):
            applied = controller.command_from_nominal(
                _actuator_output(float(severity)), nominal
            )
            assert applied[1] / nominal[1] == pytest.approx(
                gain_action_multiplier(float(severity), config), abs=1e-12
            )
            # The unfaulted joint is never touched by the actuator action.
            assert applied[0] == pytest.approx(nominal[0], abs=1e-12)


def test_multiplier_is_flat_below_the_sensitive_interval() -> None:
    """Every estimate at or below `1 / cap` commands identically — the core Part A claim."""

    config = RecoveryControlConfig()
    low, high = severity_sensitive_interval(config)
    assert (low, high) == (0.5, 1.0)
    flat = [gain_action_multiplier(s, config) for s in (0.01, 0.10, 0.25, 0.40, low)]
    assert flat == pytest.approx([config.maximum_gain_compensation] * len(flat))
    # Inside the interval the action is strictly decreasing in the estimate.
    inside = [gain_action_multiplier(s, config) for s in (0.55, 0.70, 0.85, 0.99)]
    assert all(a > b for a, b in zip(inside, inside[1:]))
    assert gain_action_multiplier(1.0, config) == pytest.approx(1.0)


def test_gain_floor_keeps_severe_settings_flat_at_every_cap() -> None:
    """`minimum_gain_remaining` bounds the sensitive interval below, so raising the cap
    alone can never make the most severe settings severity-sensitive."""

    for cap in (2.0, 4.0, 8.0, 64.0):
        config = RecoveryControlConfig(maximum_gain_compensation=cap)
        low, _ = severity_sensitive_interval(config)
        assert low >= config.minimum_gain_remaining
        assert gain_action_multiplier(0.25, config) == pytest.approx(
            gain_action_multiplier(0.10, config)
        )


def test_multiplier_rejects_impossible_severities() -> None:
    """The read-out contract is `(0, 1]`; anything else must fail loudly."""

    config = RecoveryControlConfig()
    for bad in (0.0, -0.1, 1.5, float("nan"), float("inf")):
        with pytest.raises(ValueError):
            gain_action_multiplier(bad, config)
    with pytest.raises(ValueError):
        gain_action_multiplier(0.5, config, source_probability=1.5)


def test_exact_restoration_ceiling_inverts_the_deficit() -> None:
    """A deficit `D` maps to `D / (1 + D)`, and the two agree at zero."""

    assert exact_restoration_ceiling_pct(0.0) == pytest.approx(0.0)
    assert exact_restoration_ceiling_pct(100.0) == pytest.approx(50.0)
    for deficit in (2.69, 13.20, 23.16, 65.73):
        ceiling = exact_restoration_ceiling_pct(deficit)
        assert ceiling < deficit
        # Round trip: reduction R corresponds to deficit R / (1 - R).
        fraction = ceiling / 100.0
        assert 100.0 * fraction / (1.0 - fraction) == pytest.approx(deficit)


def test_sensitivity_map_requires_both_conditions_to_reach_the_contract() -> None:
    """A severity advantage needs a sensitive action *and* a ceiling above the bar."""

    # A synthetic grid where the two conditions are deliberately separated: the severe
    # setting has ample headroom but sits in the flat region; the mild setting is
    # severity-sensitive but has no headroom.
    deficits = {0.10: 60.0, 0.80: 3.0}
    result = action_sensitivity_map(deficits, caps=(2.0,), bar_pct=10.0)
    by_severity = {row["severity"]: row for row in result["rows"]}
    assert by_severity[0.10]["ceiling_clears_bar"] is True
    assert by_severity[0.10]["severity_sensitive"] is False
    assert by_severity[0.80]["severity_sensitive"] is True
    assert by_severity[0.80]["ceiling_clears_bar"] is False
    assert result["by_cap"]["2.0"]["n_reachable"] == 0
    assert result["smallest_cap_with_a_reachable_severity"] is None


def test_sensitivity_map_finds_a_reachable_severity_when_one_exists() -> None:
    """A setting that is both sensitive and above the bar must be reported as reachable."""

    # 0.40 sits in the flat region at cap 2.0 (the interval opens at 0.50) and inside the
    # sensitive region at cap 4.0 (it opens at the 0.25 gain floor), with ample headroom
    # at both, so raising the cap is the only thing that changes.
    deficits = {0.40: 30.0}
    result = action_sensitivity_map(deficits, caps=(2.0, 4.0), bar_pct=10.0)
    assert result["by_cap"]["2.0"]["reachable_severities"] == []
    assert result["by_cap"]["4.0"]["reachable_severities"] == [0.40]
    assert result["smallest_cap_with_a_reachable_severity"] == 4.0


# --------------------------------------------------------------------------- #
# Part B — the severity read-out head.
# --------------------------------------------------------------------------- #
def _linear_problem(
    n: int = 40, width: int = 6, *, dead_columns: tuple[int, ...] = ()
) -> tuple[np.ndarray, np.ndarray]:
    """Return a deterministic exactly-linear severity problem with optional dead columns."""

    rng = np.random.default_rng(11)
    x = rng.normal(size=(n, width))
    for column in dead_columns:
        x[:, column] = 0.0
    weights = np.arange(1, width + 1, dtype=float) / width
    weights[list(dead_columns)] = 0.0
    y = 0.5 + 0.05 * (x @ weights)
    return x, y


def test_head_recovers_a_linear_severity_map() -> None:
    """With a weak penalty the head must reproduce an exactly-linear target closely."""

    x, y = _linear_problem()
    head = SeverityRidgeHead(regularization=1e-6).fit(x, y)
    assert head.is_fitted
    assert head.n_train == x.shape[0]
    assert np.max(np.abs(head.predict(x) - y)) < 1e-6
    assert head.train_residual_std < 1e-6


def test_head_ignores_suite_unavailable_columns() -> None:
    """A channel the suite lacks is all-zero, so it must not move the fit at all.

    This is what makes the C1-versus-S comparison a data comparison rather than a code
    comparison: the same head is fitted on both, and the masked columns drop out
    structurally rather than by configuration.
    """

    x, y = _linear_problem(dead_columns=(1, 4))
    head = SeverityRidgeHead(regularization=1e-6).fit(x, y)
    assert head.active_feature_count == x.shape[1] - 2
    baseline = head.predict(x)
    # Perturbing a dead column cannot change any prediction.
    perturbed = x.copy()
    perturbed[:, 1] = 1000.0
    perturbed[:, 4] = -7.5
    assert np.allclose(head.predict(perturbed), baseline, atol=1e-12)


def test_head_clips_predictions_into_the_physical_severity_range() -> None:
    """A read-out may not report a remaining fraction outside its declared bounds."""

    x, y = _linear_problem()
    head = SeverityRidgeHead(regularization=1e-6, severity_bounds=(0.0, 1.0)).fit(x, y)
    extreme = np.vstack([x[0] * 1e4, x[1] * -1e4])
    predictions = head.predict(extreme)
    assert np.all(predictions >= 0.0)
    assert np.all(predictions <= 1.0)


def test_head_regularization_shrinks_toward_the_training_mean() -> None:
    """A large penalty must collapse the head onto the training mean, not diverge."""

    x, y = _linear_problem()
    head = SeverityRidgeHead(regularization=1e12).fit(x, y)
    assert np.allclose(head.predict(x), float(np.mean(y)), atol=1e-6)


def test_head_fails_loudly_on_bad_input() -> None:
    """Silent failure is the worst mode; every misuse must raise."""

    x, y = _linear_problem()
    with pytest.raises(ValueError):
        SeverityRidgeHead(regularization=-1.0)
    with pytest.raises(ValueError):
        SeverityRidgeHead().fit(x, y[:-1])
    with pytest.raises(ValueError):
        SeverityRidgeHead().fit(x[:1], y[:1])
    bad = x.copy()
    bad[0, 0] = np.nan
    with pytest.raises(ValueError):
        SeverityRidgeHead().fit(bad, y)
    with pytest.raises(ValueError):
        SeverityRidgeHead().predict(x)
    fitted = SeverityRidgeHead().fit(x, y)
    with pytest.raises(ValueError):
        fitted.predict(x[:, :-1])
    with pytest.raises(ValueError):
        _ = SeverityRidgeHead().active_feature_count
    with pytest.raises(ValueError):
        SeverityRidgeHead(feature_std_floor=0.0)
    with pytest.raises(ValueError):
        SeverityRidgeHead(severity_bounds=(1.0, 0.0))


# --------------------------------------------------------------------------- #
# Parts A and B composed — the commanded-action comparison.
# --------------------------------------------------------------------------- #
def _evaluation(estimates: list[tuple[float, int, float]]) -> dict[str, object]:
    """Return a minimal `evaluate_suite`-shaped record carrying only predictions."""

    return {
        "predictions": [
            {"severity": severity, "seed": seed, "estimate": estimate}
            for severity, seed, estimate in estimates
        ]
    }


def test_different_severity_estimates_can_still_command_identically() -> None:
    """Two suites disagreeing inside the flat region are behaviourally identical.

    This is the screen's central point: a severity-accuracy difference is not a control
    difference, and only the commanded multiplier decides the contract's paired quantity.
    """

    c1 = _evaluation([(0.25, 1, 0.40), (0.25, 2, 0.12)])
    s = _evaluation([(0.25, 1, 0.26), (0.25, 2, 0.25)])
    result = compare_commanded_actions(c1, s, caps=(2.0,))
    row = result["caps"][0]
    assert row["n_multipliers_differ"] == 0
    assert row["max_abs_multiplier_difference"] == pytest.approx(0.0)


def test_comparison_separates_capped_region_differences() -> None:
    """A suite difference only matters where the action could be worth the bar.

    The capped-region split is what distinguishes "the suites differ somewhere" from "the
    suites differ where it could move the contract."
    """

    c1 = _evaluation([(0.25, 1, 0.30), (0.85, 1, 0.90)])
    s = _evaluation([(0.25, 1, 0.20), (0.85, 1, 0.80)])
    row = compare_commanded_actions(c1, s, caps=(2.0,))["caps"][0]
    # Both capped-region estimates saturate; only the mild arm differs.
    assert row["n_multipliers_differ"] == 1
    assert row["capped_region_pairs"] == 1
    assert row["capped_region_multipliers_differ"] == 0
    assert row["capped_region_max_abs_difference"] == pytest.approx(0.0)


def test_raising_the_cap_can_expose_a_severity_difference() -> None:
    """The same estimates that command identically at one cap may not at a larger one."""

    c1 = _evaluation([(0.40, 1, 0.45)])
    s = _evaluation([(0.40, 1, 0.30)])
    result = compare_commanded_actions(c1, s, caps=(2.0, 4.0))
    at_two, at_four = result["caps"]
    assert at_two["n_multipliers_differ"] == 0
    assert at_four["n_multipliers_differ"] == 1
    assert at_four["max_abs_multiplier_difference"] > 0.0


def test_comparison_requires_arm_for_arm_alignment() -> None:
    """Comparing unpaired predictions would silently invent a difference."""

    c1 = _evaluation([(0.25, 1, 0.30)])
    s = _evaluation([(0.50, 1, 0.30)])
    with pytest.raises(ValueError):
        compare_commanded_actions(c1, s, caps=(2.0,))
    with pytest.raises(ValueError):
        compare_commanded_actions(c1, _evaluation([]), caps=(2.0,))


def test_oracle_agreement_separates_capped_sensitive_and_healthy_arms() -> None:
    """The healthy anchor is its own regime, not part of the capped region.

    At the top of the grid the oracle applies no action at all, so a mismatch there is a
    false authorization on a sound body — a different question from severity precision.
    Folding it into the capped arms understates the capped agreement rate.
    """

    evaluation = {
        "suite": "C1",
        # capped (true 0.25 and 0.10), sensitive (true 0.70), healthy anchor (true 1.00).
        "predictions": [
            {"severity": 0.25, "seed": 1, "estimate": 0.31},
            {"severity": 0.10, "seed": 1, "estimate": 0.44},
            {"severity": 0.70, "seed": 1, "estimate": 0.70},
            {"severity": 1.00, "seed": 1, "estimate": 0.98},
        ],
    }
    row = compare_against_oracle_action(evaluation, caps=(2.0,))["caps"][0]
    assert row["capped_region_arms"] == 2
    assert row["capped_region_oracle_identical_rate"] == pytest.approx(1.0)
    assert row["sensitive_region_arms"] == 1
    assert row["sensitive_region_oracle_identical_rate"] == pytest.approx(1.0)
    assert row["identity_region_arms"] == 1
    # 0.98 estimated on a healthy arm commands 1/0.98 > 1: a real, if small, action.
    assert row["identity_region_oracle_identical_rate"] == pytest.approx(0.0)
    assert row["max_abs_multiplier_error"] > 0.0


def test_oracle_agreement_reports_na_for_an_empty_regime() -> None:
    """A regime with no arms must report NaN rather than a misleading zero."""

    evaluation = {
        "suite": "S",
        "predictions": [{"severity": 0.25, "seed": 1, "estimate": 0.25}],
    }
    row = compare_against_oracle_action(evaluation, caps=(2.0,))["caps"][0]
    assert row["capped_region_arms"] == 1
    assert row["sensitive_region_arms"] == 0
    assert np.isnan(row["sensitive_region_oracle_identical_rate"])
    assert row["identity_region_arms"] == 0
    assert np.isnan(row["identity_region_oracle_identical_rate"])


def test_a_clipped_zero_estimate_is_treated_as_no_action() -> None:
    """A zero read-out is not a legal severity input, so the command must be untouched."""

    c1 = _evaluation([(0.25, 1, 0.0)])
    s = _evaluation([(0.25, 1, 0.0)])
    row = compare_commanded_actions(c1, s, caps=(2.0,))["caps"][0]
    assert row["pairs"][0]["c1_multiplier"] == pytest.approx(1.0)
    assert row["pairs"][0]["s_multiplier"] == pytest.approx(1.0)
