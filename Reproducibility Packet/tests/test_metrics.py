"""Tests for the two-layer evaluation metrics (schema Slot 7 / §G).

Each test pins a metric against a hand-computed value or a defining property, so a
future refactor cannot quietly change what the pre-declared success bars measure.
The load-bearing one is the abstention rule: a known-class sample the model declines
must count as a headline error, never as a free pass.
"""

from __future__ import annotations

import sys
from pathlib import Path

import numpy as np
import pytest

SCRIPTS_DIR = Path(__file__).resolve().parents[1] / "scripts"
sys.path.insert(0, str(SCRIPTS_DIR))

from utils.metrics import (  # noqa: E402
    ABSTAIN,
    brier_score,
    coverage_at_risk,
    expected_calibration_error,
    false_abstention_rate,
    j_5s,
    macro_f1,
    nll,
    ood_auprc,
    ood_auroc,
    ood_false_acceptance_rate,
    per_class_recall,
    resolve_predictions,
    risk_coverage_curve,
    selective_risk_at_coverage,
    tracking_reduction_pct,
    unknown_threshold_at_sensitivity,
)


# --------------------------------------------------------------------------- #
# Classification headline + the abstention rule.
# --------------------------------------------------------------------------- #
def test_macro_f1_perfect_is_one() -> None:
    """All four classes predicted correctly -> macro-F1 == 1."""

    y = np.array([0, 1, 2, 3, 0, 1, 2, 3])
    assert macro_f1(y, y.copy()) == pytest.approx(1.0)


def test_macro_f1_abstention_counts_as_error() -> None:
    """Abstaining on the single class-3 sample zeroes that class's F1 (0.75 macro)."""

    y_true = np.array([0, 1, 2, 3])
    y_pred = np.array([0, 1, 2, ABSTAIN])  # perfect except an abstention on class 3
    # classes 0,1,2 -> F1 1.0 each; class 3 -> no TP -> F1 0.0; macro = 3/4.
    assert macro_f1(y_true, y_pred) == pytest.approx(0.75)


def test_abstention_never_creates_a_false_positive() -> None:
    """An abstention must not be scored as a wrong-class prediction (no FP anywhere)."""

    y_true = np.array([0, 0])
    abstain_pred = np.array([ABSTAIN, ABSTAIN])
    wrong_pred = np.array([1, 1])  # confidently wrong into class 1
    # Both score 0 recall on class 0, but the wrong prediction also hurts class 1's
    # precision, so abstaining is >= confidently-wrong on macro-F1.
    assert macro_f1(y_true, abstain_pred) >= macro_f1(y_true, wrong_pred)


def test_resolve_predictions_argmax_and_sentinel() -> None:
    """Non-abstaining samples predict argmax; abstaining samples get the sentinel."""

    p = np.array([[0.7, 0.1, 0.1, 0.1], [0.1, 0.1, 0.7, 0.1]])
    abstain = np.array([False, True])
    np.testing.assert_array_equal(resolve_predictions(p, abstain), np.array([0, ABSTAIN]))


def test_per_class_recall_hand_example() -> None:
    """Recall per class, with one abstention lowering exactly one class's recall."""

    y_true = np.array([0, 0, 1, 2, 3])
    y_pred = np.array([0, ABSTAIN, 1, 2, 3])  # class 0 has 1/2 recall
    recalls = per_class_recall(y_true, y_pred)
    assert recalls["healthy"] == pytest.approx(0.5)
    assert recalls["structure"] == pytest.approx(1.0)
    assert recalls["actuator"] == pytest.approx(1.0)
    assert recalls["sensor"] == pytest.approx(1.0)


# --------------------------------------------------------------------------- #
# Calibration.
# --------------------------------------------------------------------------- #
def test_brier_score_perfect_and_uniform() -> None:
    """Brier is 0 for one-hot-correct and 0.75 for a uniform guess over 4 classes."""

    y = np.array([0, 1])
    confident = np.array([[1.0, 0.0, 0.0, 0.0], [0.0, 1.0, 0.0, 0.0]])
    assert brier_score(y, confident) == pytest.approx(0.0)
    uniform = np.full((2, 4), 0.25)
    # (0.25-1)^2 + 3*(0.25)^2 = 0.5625 + 0.1875 = 0.75
    assert brier_score(y, uniform) == pytest.approx(0.75)


def test_nll_uniform_is_log4() -> None:
    """A uniform distribution puts 0.25 on the truth, so NLL == -log(0.25) == log 4."""

    y = np.array([2, 3])
    uniform = np.full((2, 4), 0.25)
    assert nll(y, uniform) == pytest.approx(np.log(4.0))


def test_ece_zero_when_confidence_equals_accuracy() -> None:
    """Confidence 1.0 with all-correct -> ECE 0; all-wrong -> ECE == 1.0."""

    y = np.array([0, 1, 2, 3])
    perfect = np.eye(4)  # confidence 1.0, all correct
    assert expected_calibration_error(y, perfect) == pytest.approx(0.0)
    # Confidence 1.0 on the wrong class every time -> |acc - conf| = |0 - 1| = 1.
    wrong = np.array([[0, 1, 0, 0], [1, 0, 0, 0], [0, 0, 0, 1], [0, 0, 1, 0]], dtype=float)
    assert expected_calibration_error(y, wrong) == pytest.approx(1.0)


# --------------------------------------------------------------------------- #
# Selective prediction.
# --------------------------------------------------------------------------- #
def test_risk_coverage_orders_by_confidence() -> None:
    """The single wrong sample is least confident, so risk stays 0 until full coverage."""

    y_true = np.array([0, 1, 2])
    y_pred = np.array([0, 1, 3])  # last one wrong
    confidence = np.array([0.9, 0.8, 0.4])  # the wrong one is least confident
    coverage, risk = risk_coverage_curve(y_true, y_pred, confidence)
    np.testing.assert_allclose(coverage, [1 / 3, 2 / 3, 1.0])
    np.testing.assert_allclose(risk, [0.0, 0.0, 1 / 3])
    assert selective_risk_at_coverage(y_true, y_pred, confidence, 2 / 3) == pytest.approx(0.0)


def test_risk_coverage_does_not_split_confidence_ties() -> None:
    """A threshold accepts a whole tie group, so tied ordering cannot change the curve."""

    y_true = np.array([0, 1, 2])
    y_pred = np.array([0, 0, 3])
    confidence = np.array([0.9, 0.9, 0.4])
    coverage_a, risk_a = risk_coverage_curve(y_true, y_pred, confidence)
    order = np.array([1, 0, 2])
    coverage_b, risk_b = risk_coverage_curve(
        y_true[order], y_pred[order], confidence[order]
    )
    np.testing.assert_allclose(coverage_a, [2 / 3, 1.0])
    np.testing.assert_allclose(risk_a, [0.5, 2 / 3])
    np.testing.assert_allclose(coverage_b, coverage_a)
    np.testing.assert_allclose(risk_b, risk_a)


def test_false_abstention_rate_excludes_ood() -> None:
    """Only in-distribution abstentions count; an OOD abstention is not 'false'."""

    abstain = np.array([True, False, True, False])
    ood = np.array([False, False, True, False])  # sample 2 is genuinely OOD
    # in-distribution samples: 0,1,3; abstained among them: just sample 0 -> 1/3.
    assert false_abstention_rate(abstain, ood) == pytest.approx(1 / 3)


# --------------------------------------------------------------------------- #
# Out-of-distribution detection.
# --------------------------------------------------------------------------- #
def test_ood_auroc_and_auprc_perfect_separation() -> None:
    """A score that ranks every OOD above every ID gives AUROC == AUPRC == 1."""

    ood = np.array([False, False, True, True])
    score = np.array([0.1, 0.2, 0.8, 0.9])  # OOD strictly higher
    assert ood_auroc(ood, score) == pytest.approx(1.0)
    assert ood_auprc(ood, score) == pytest.approx(1.0)


def test_false_accept_uses_validation_threshold_then_held_out_ood() -> None:
    """Freeze the sensitivity threshold on validation, then score held-out OOD."""

    calibration_ood = np.array([0.1, 0.2, 0.3, 0.4])
    threshold = unknown_threshold_at_sensitivity(calibration_ood, sensitivity=0.75)
    assert threshold == pytest.approx(0.2)  # scores >= .2 detect 3/4 calibration OOD
    ood = np.array([False, False, True, True, True, True])
    score = np.array([0.0, 0.9, 0.1, 0.2, 0.5, 0.8])
    # Only held-out OOD score .1 falls below the frozen threshold -> 1/4 false accept.
    assert ood_false_acceptance_rate(ood, score, threshold=threshold) == pytest.approx(0.25)


def test_ood_metrics_need_both_populations() -> None:
    """OOD metrics fail loud when only one population is present."""

    with pytest.raises(ValueError):
        ood_auroc(np.array([False, False]), np.array([0.1, 0.2]))


# --------------------------------------------------------------------------- #
# Control layer (schema §G).
# --------------------------------------------------------------------------- #
def test_j_5s_constant_error_is_norm_times_window() -> None:
    """A constant 0.1 m planar error integrated over 2 s of grid is 0.2 m·s."""

    t_s = np.array([1.0, 2.0, 3.0])
    reference = np.tile([0.1, 0.0], (3, 1))
    output = np.zeros((3, 2))  # error = [0.1, 0] -> norm 0.1
    # trapezoid of constant 0.1 over t in [1,3] = 0.1 * 2 = 0.2
    assert j_5s(t_s, reference, output, onset_time_s=1.0, window_s=2.0) == pytest.approx(0.2)


def test_j_5s_excludes_samples_outside_the_window() -> None:
    """Samples before onset or past onset+window are dropped before integration."""

    t_s = np.arange(0.0, 8.0)  # includes pre-onset and one sample past the end
    reference = np.tile([0.1, 0.0], (8, 1))
    output = np.zeros((8, 2))
    # Only t in [1.0, 6.0] contributes: constant 0.1 over five seconds = 0.5.
    assert j_5s(t_s, reference, output, onset_time_s=1.0, window_s=5.0) == pytest.approx(0.5)


def test_j_5s_uses_the_deformed_tip_it_is_given() -> None:
    """J_5s integrates the supplied true_task_output; a bent tip raises the error."""

    t_s = np.array([1.0, 2.0])
    reference = np.tile([0.4, 0.0], (2, 1))
    rigid_tip = np.tile([0.4, 0.0], (2, 1))  # perfect -> J 0
    deformed_tip = np.tile([0.4, 0.05], (2, 1))  # 5 cm of flex in y
    assert j_5s(t_s, reference, rigid_tip, onset_time_s=1.0, window_s=1.0) == pytest.approx(0.0)
    assert j_5s(t_s, reference, deformed_tip, onset_time_s=1.0, window_s=1.0) == pytest.approx(0.05)


def test_tracking_reduction_pct() -> None:
    """A drop from 1.0 to 0.85 m·s is a 15% reduction."""

    assert tracking_reduction_pct(1.0, 0.85) == pytest.approx(15.0)


def test_j_5s_needs_two_samples_in_window() -> None:
    """A window with fewer than two grid samples cannot be integrated."""

    t_s = np.array([1.0, 9.0])
    reference = np.zeros((2, 2))
    output = np.zeros((2, 2))
    with pytest.raises(ValueError):
        j_5s(t_s, reference, output, onset_time_s=1.0, window_s=0.5)


def test_j_5s_rejects_a_truncated_five_second_window() -> None:
    """A short trace must not be mislabeled as the frozen five-second integral."""

    t_s = np.array([1.0, 2.0, 3.0])
    reference = np.tile([0.1, 0.0], (3, 1))
    output = np.zeros((3, 2))
    with pytest.raises(ValueError, match="truncated"):
        j_5s(t_s, reference, output, onset_time_s=1.0, window_s=5.0)


def test_coverage_at_risk_pre_registered_ceiling() -> None:
    """Max coverage whose selective risk stays at/below the ceiling (Claim Sheet)."""

    # Top three confident samples correct, least-confident one wrong (distinct confs).
    y_true = np.array([0, 1, 2, 3])
    y_pred = np.array([0, 1, 2, 0])  # last one wrong
    confidence = np.array([0.9, 0.8, 0.7, 0.6])
    # risk is 0 up to 75% coverage, 0.25 at full coverage.
    assert coverage_at_risk(y_true, y_pred, confidence, risk_ceiling=0.05) == pytest.approx(0.75)
    assert coverage_at_risk(y_true, y_pred, confidence, risk_ceiling=0.3) == pytest.approx(1.0)
    # If even the most-confident sample is wrong, no coverage meets a tight ceiling.
    y_pred_bad = np.array([1, 1, 2, 0])  # top-confidence sample now wrong
    assert coverage_at_risk(y_true, y_pred_bad, confidence, risk_ceiling=0.05) == pytest.approx(0.0)


# --------------------------------------------------------------------------- #
# Fail-loud input validation.
# --------------------------------------------------------------------------- #
def test_probabilities_must_sum_to_one() -> None:
    """A malformed p_class block that does not sum to 1 is rejected."""

    with pytest.raises(ValueError):
        brier_score(np.array([0]), np.array([[0.5, 0.1, 0.1, 0.1]]))
