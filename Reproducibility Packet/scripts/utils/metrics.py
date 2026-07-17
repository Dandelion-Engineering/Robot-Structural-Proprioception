"""Evaluation metrics for the two-layer success bar (schema Slot 7, Claude's lane).

This module renders the pre-declared metrics of the Claim Sheet / schema v1.0 into
pure NumPy/scikit-learn functions. It is deliberately free of any I/O, path, or
config state: it operates on already-loaded arrays so the same functions serve the
pilot, the confirmatory analysis, and the tests. The eval *driver* (a separate
`argparse` CLI, added once the frozen data layout exists) is what reads the §E
role indexes and calls these.

Two layers, kept strictly separate so a diagnosis result can never be silently
conflated with a control result (schema §D):

  * **Layer 1 — diagnosis** (reads §D estimator outputs + labels):
      - `macro_f1` : four-way {healthy, structure, actuator, sensor} macro-F1 with
        **known-class abstention scored as headline error** (Claim Sheet).
      - `per_class_recall` : per-source-class recall (abstention lowers it).
      - calibration: `brier_score`, `nll`, `expected_calibration_error`.
      - selective prediction: `risk_coverage_curve`, `selective_risk_at_coverage`,
        `false_abstention_rate`.
      - OOD: `ood_auroc`, `ood_auprc`, `false_accept_at_id_acceptance`.

  * **Layer 2 — control** (reads §B privileged metric arrays + §D controller logs):
      - `j_5s` : the headline post-change tracking integral (schema §G).
      - `tracking_reduction_pct` : S-vs-C1 percentage reduction in `j_5s`.

Paired hierarchical-bootstrap confidence intervals for the S-vs-C1 headline
comparisons live in `utils.stats`; this module supplies the point statistics those
intervals are built on.

Predictions follow schema §D estimator outputs: `p_class[4]` (known-class
probabilities in the canonical order below), `unknown_score` (higher => more
out-of-distribution), and `abstain_decision`. `resolve_predictions` maps those to a
hard class index or the `ABSTAIN` sentinel.
"""

from __future__ import annotations

import numpy as np
from sklearn.metrics import (
    average_precision_score,
    f1_score,
    recall_score,
    roc_auc_score,
)

from utils.schema_types import SOURCE_CLASSES

# Canonical source-class ordering (index <-> name). The set is the schema's; the
# *order* is a metric-layer convention so p_class columns and label indices align.
SOURCE_CLASS_ORDER: tuple[str, ...] = ("healthy", "structure", "actuator", "sensor")
N_SOURCE_CLASSES = len(SOURCE_CLASS_ORDER)
CLASS_INDICES: tuple[int, ...] = tuple(range(N_SOURCE_CLASSES))
ABSTAIN = -1  # predicted-label sentinel: a known-class sample the model declined

assert set(SOURCE_CLASS_ORDER) == set(SOURCE_CLASSES), "metric order must match schema classes"

_PROB_SUM_TOL = 1.0e-6
_LOG_EPS = 1.0e-12


# --------------------------------------------------------------------------- #
# Input validation (fail loud on malformed estimator output — schema §D).
# --------------------------------------------------------------------------- #
def _check_labels(y_true: np.ndarray) -> np.ndarray:
    """Validate and return integer source-class labels in `[0, 4)`."""

    labels = np.asarray(y_true)
    if labels.ndim != 1:
        raise ValueError(f"y_true must be 1-D, got shape {labels.shape}")
    if not np.issubdtype(labels.dtype, np.integer):
        raise ValueError("y_true must be integer source-class indices")
    if labels.size and (labels.min() < 0 or labels.max() >= N_SOURCE_CLASSES):
        raise ValueError(f"y_true indices must lie in [0, {N_SOURCE_CLASSES})")
    return labels


def _check_probabilities(p_class: np.ndarray, n_expected: int | None = None) -> np.ndarray:
    """Validate a `[N,4]` known-class probability block sums to one and is in `[0,1]`."""

    probs = np.asarray(p_class, dtype=float)
    if probs.ndim != 2 or probs.shape[1] != N_SOURCE_CLASSES:
        raise ValueError(f"p_class must be [N,{N_SOURCE_CLASSES}], got {probs.shape}")
    if n_expected is not None and probs.shape[0] != n_expected:
        raise ValueError(f"p_class has {probs.shape[0]} rows, expected {n_expected}")
    if probs.size:
        if not np.all(np.isfinite(probs)):
            raise ValueError("p_class contains non-finite probabilities")
        if probs.min() < -_PROB_SUM_TOL or probs.max() > 1.0 + _PROB_SUM_TOL:
            raise ValueError("p_class entries must lie in [0, 1]")
        row_sums = probs.sum(axis=1)
        if not np.allclose(row_sums, 1.0, atol=1.0e-4):
            raise ValueError("each p_class row must sum to 1 (known-class simplex)")
    return probs


def resolve_predictions(p_class: np.ndarray, abstain_decision: np.ndarray) -> np.ndarray:
    """Map estimator outputs to a hard label per sample, or `ABSTAIN`.

    A non-abstaining sample predicts ``argmax(p_class)``; an abstaining sample gets
    the `ABSTAIN` sentinel so downstream metrics can score it as a known-class miss
    (it contributes a false negative to its true class and no false positive).
    """

    probs = _check_probabilities(p_class)
    abstain = np.asarray(abstain_decision, dtype=bool)
    if abstain.shape != (probs.shape[0],):
        raise ValueError("abstain_decision must be a length-N boolean vector")
    predicted = np.argmax(probs, axis=1)
    return np.where(abstain, ABSTAIN, predicted)


# --------------------------------------------------------------------------- #
# Layer 1 — diagnosis: classification headline.
# --------------------------------------------------------------------------- #
def macro_f1(y_true: np.ndarray, y_pred: np.ndarray) -> float:
    """Four-way macro-F1 with abstention scored as error (headline diagnosis metric).

    ``y_pred`` may contain the `ABSTAIN` sentinel; because the score is computed with
    the fixed known-class label set, an abstention is a false negative for the true
    class and never a false positive — exactly the "known-class abstention counts as
    a headline error" rule the Claim Sheet locked in.
    """

    labels = _check_labels(y_true)
    pred = np.asarray(y_pred)
    if pred.shape != labels.shape:
        raise ValueError("y_true and y_pred must have the same shape")
    return float(
        f1_score(labels, pred, labels=list(CLASS_INDICES), average="macro", zero_division=0.0)
    )


def per_class_recall(y_true: np.ndarray, y_pred: np.ndarray) -> dict[str, float]:
    """Per-source-class recall (abstentions and misclassifications both lower it).

    Returns a name-keyed dict so the −0.02 non-inferiority check (every source-class
    recall difference's lower 95% bound above −0.02) reads by class rather than index.
    """

    labels = _check_labels(y_true)
    pred = np.asarray(y_pred)
    if pred.shape != labels.shape:
        raise ValueError("y_true and y_pred must have the same shape")
    recalls = recall_score(
        labels, pred, labels=list(CLASS_INDICES), average=None, zero_division=0.0
    )
    return {name: float(r) for name, r in zip(SOURCE_CLASS_ORDER, recalls)}


# --------------------------------------------------------------------------- #
# Layer 1 — diagnosis: probabilistic calibration (reported separately).
# --------------------------------------------------------------------------- #
def _one_hot(labels: np.ndarray) -> np.ndarray:
    """Return the `[N,4]` one-hot encoding of integer source-class labels."""

    one_hot = np.zeros((labels.shape[0], N_SOURCE_CLASSES), dtype=float)
    one_hot[np.arange(labels.shape[0]), labels] = 1.0
    return one_hot


def brier_score(y_true: np.ndarray, p_class: np.ndarray) -> float:
    """Multiclass Brier score: mean squared error between p_class and the one-hot truth.

    Lower is better; range ``[0, 2]``. Measured over whatever sample set the caller
    passes (e.g. in-distribution, non-abstained) — selection is the driver's choice.
    """

    labels = _check_labels(y_true)
    probs = _check_probabilities(p_class, n_expected=labels.shape[0])
    if labels.size == 0:
        raise ValueError("brier_score needs at least one sample")
    return float(np.mean(np.sum((probs - _one_hot(labels)) ** 2, axis=1)))


def nll(y_true: np.ndarray, p_class: np.ndarray) -> float:
    """Mean negative log-likelihood (multiclass cross-entropy) of the true class.

    Probabilities are clipped to ``[eps, 1]`` before the log so a confident miss is
    penalized heavily but finitely.
    """

    labels = _check_labels(y_true)
    probs = _check_probabilities(p_class, n_expected=labels.shape[0])
    if labels.size == 0:
        raise ValueError("nll needs at least one sample")
    true_p = probs[np.arange(labels.shape[0]), labels]
    return float(-np.mean(np.log(np.clip(true_p, _LOG_EPS, 1.0))))


def expected_calibration_error(
    y_true: np.ndarray, p_class: np.ndarray, *, n_bins: int = 15
) -> float:
    """Expected Calibration Error over equal-width confidence bins (Guo et al. 2017).

    Confidence is the top predicted probability; each sample falls in one of
    ``n_bins`` bins over ``[0,1]``; ECE is the sample-weighted mean gap between bin
    accuracy and bin mean confidence. Lower is better.
    """

    labels = _check_labels(y_true)
    probs = _check_probabilities(p_class, n_expected=labels.shape[0])
    if labels.size == 0:
        raise ValueError("expected_calibration_error needs at least one sample")
    if n_bins < 1:
        raise ValueError("n_bins must be >= 1")
    confidence = probs.max(axis=1)
    predicted = probs.argmax(axis=1)
    correct = (predicted == labels).astype(float)
    edges = np.linspace(0.0, 1.0, n_bins + 1)
    # np.digitize with the interior edges puts confidence==1.0 in the last bin.
    bin_index = np.clip(np.digitize(confidence, edges[1:-1], right=False), 0, n_bins - 1)
    total = labels.shape[0]
    ece = 0.0
    for b in range(n_bins):
        in_bin = bin_index == b
        count = int(np.count_nonzero(in_bin))
        if count == 0:
            continue
        ece += (count / total) * abs(correct[in_bin].mean() - confidence[in_bin].mean())
    return float(ece)


# --------------------------------------------------------------------------- #
# Layer 1 — diagnosis: selective prediction (abstention as a first-class outcome).
# --------------------------------------------------------------------------- #
def risk_coverage_curve(
    y_true: np.ndarray, y_pred_class: np.ndarray, confidence: np.ndarray
) -> tuple[np.ndarray, np.ndarray]:
    """Return (coverage, risk) points as the confidence acceptance threshold sweeps.

    A sample is *covered* when its confidence is at or above the threshold; risk is
    the error rate among covered samples. Points are ordered by increasing coverage.
    ``y_pred_class`` here is the model's hard class guess (argmax), independent of the
    abstain decision — selective prediction asks what *would* happen at each operating
    threshold. Higher confidence should mean lower risk for a useful detector.
    """

    labels = _check_labels(y_true)
    pred = np.asarray(y_pred_class)
    conf = np.asarray(confidence, dtype=float)
    if not (labels.shape == pred.shape == conf.shape):
        raise ValueError("y_true, y_pred_class, confidence must share shape")
    if labels.size == 0:
        raise ValueError("risk_coverage_curve needs at least one sample")
    order = np.argsort(-conf, kind="stable")  # most confident first
    wrong = (pred[order] != labels[order]).astype(float)
    n = labels.shape[0]
    coverage = np.arange(1, n + 1) / n
    risk = np.cumsum(wrong) / np.arange(1, n + 1)
    return coverage, risk


def selective_risk_at_coverage(
    y_true: np.ndarray, y_pred_class: np.ndarray, confidence: np.ndarray, coverage: float
) -> float:
    """Risk (error rate) among the most-confident fraction ``coverage`` of samples."""

    if not 0.0 < coverage <= 1.0:
        raise ValueError("coverage must be in (0, 1]")
    cov, risk = risk_coverage_curve(y_true, y_pred_class, confidence)
    idx = int(np.searchsorted(cov, coverage, side="left"))
    idx = min(idx, risk.shape[0] - 1)
    return float(risk[idx])


def false_abstention_rate(abstain_decision: np.ndarray, ood_flag: np.ndarray) -> float:
    """Fraction of in-distribution (non-OOD) samples on which the model abstained.

    Abstaining on a genuinely out-of-distribution sample is desired behaviour, so it
    is excluded; abstaining on an in-distribution known-class sample is the "false
    abstention" the selective layer is meant to keep low. Returns 0.0 when there are
    no in-distribution samples.
    """

    abstain = np.asarray(abstain_decision, dtype=bool)
    ood = np.asarray(ood_flag, dtype=bool)
    if abstain.shape != ood.shape or abstain.ndim != 1:
        raise ValueError("abstain_decision and ood_flag must be 1-D and the same length")
    in_dist = ~ood
    if not np.any(in_dist):
        return 0.0
    return float(np.mean(abstain[in_dist]))


# --------------------------------------------------------------------------- #
# Layer 1 — diagnosis: out-of-distribution detection.
# --------------------------------------------------------------------------- #
def _check_ood_inputs(ood_flag: np.ndarray, unknown_score: np.ndarray) -> tuple[np.ndarray, np.ndarray]:
    """Validate OOD detection inputs: a boolean label and a real-valued score."""

    ood = np.asarray(ood_flag, dtype=bool)
    score = np.asarray(unknown_score, dtype=float)
    if ood.shape != score.shape or ood.ndim != 1:
        raise ValueError("ood_flag and unknown_score must be 1-D and the same length")
    if not np.all(np.isfinite(score)):
        raise ValueError("unknown_score contains non-finite values")
    if ood.all() or (~ood).all():
        raise ValueError("OOD metrics need both in-distribution and OOD samples present")
    return ood, score


def ood_auroc(ood_flag: np.ndarray, unknown_score: np.ndarray) -> float:
    """Area under the ROC for OOD detection (OOD is positive; higher score = more OOD)."""

    ood, score = _check_ood_inputs(ood_flag, unknown_score)
    return float(roc_auc_score(ood, score))


def ood_auprc(ood_flag: np.ndarray, unknown_score: np.ndarray) -> float:
    """Average precision (area under precision-recall) for OOD detection."""

    ood, score = _check_ood_inputs(ood_flag, unknown_score)
    return float(average_precision_score(ood, score))


def false_accept_at_id_acceptance(
    ood_flag: np.ndarray, unknown_score: np.ndarray, *, id_acceptance: float = 0.95
) -> float:
    """OOD false-accept rate at a fixed in-distribution acceptance operating point.

    The threshold is set so a fraction ``id_acceptance`` of in-distribution samples
    are "accepted" (``unknown_score`` at or below threshold). The returned value is
    the fraction of OOD samples that slip through as accepted at that threshold —
    lower is better. This operating-point convention (95% ID accepted by default) is
    documented here and is a config-freeze-time decision; the point estimate itself is
    convention-independent apart from ``id_acceptance``.
    """

    ood, score = _check_ood_inputs(ood_flag, unknown_score)
    if not 0.0 < id_acceptance <= 1.0:
        raise ValueError("id_acceptance must be in (0, 1]")
    id_scores = score[~ood]
    threshold = float(np.quantile(id_scores, id_acceptance))
    ood_scores = score[ood]
    return float(np.mean(ood_scores <= threshold))


# --------------------------------------------------------------------------- #
# Layer 2 — control: task-space tracking (schema §G).
# --------------------------------------------------------------------------- #
def j_5s(
    t_s: np.ndarray,
    task_reference: np.ndarray,
    true_task_output: np.ndarray,
    onset_time_s: float,
    *,
    window_s: float = 5.0,
) -> float:
    """Post-change tracking integral ``J_5s = ∫ ‖e(t)‖ dt`` over ``[t_c, t_c+window]``.

    `e = task_reference − true_task_output` is the planar (x, y) endpoint error using
    the **true deformed tip** (§G [C4]); ``‖·‖`` is the L2 norm; the integral is
    trapezoidal on the control-grid samples that fall in the window. Units: m·s.

    Args:
        t_s: [T] control-grid times (s).
        task_reference: [T,2] commanded task-space endpoint (m).
        true_task_output: [T,2] true deformed-tip position (m).
        onset_time_s: change onset time ``t_c`` (s).
        window_s: post-change window length (s); the frozen headline is 5 s.
    """

    times = np.asarray(t_s, dtype=float)
    reference = np.asarray(task_reference, dtype=float)
    output = np.asarray(true_task_output, dtype=float)
    if times.ndim != 1:
        raise ValueError("t_s must be 1-D")
    if reference.shape != (times.shape[0], 2) or output.shape != (times.shape[0], 2):
        raise ValueError("task_reference and true_task_output must be [T,2] planar")
    if window_s <= 0.0:
        raise ValueError("window_s must be positive")
    tol = 1.0e-9
    in_window = (times >= onset_time_s - tol) & (times <= onset_time_s + window_s + tol)
    if np.count_nonzero(in_window) < 2:
        raise ValueError("the analysis window contains fewer than two control samples")
    error = reference[in_window] - output[in_window]
    error_norm = np.linalg.norm(error, axis=1)  # L2 over planar (x, y)
    return float(np.trapezoid(error_norm, times[in_window]))


def tracking_reduction_pct(j_c1: float, j_s: float) -> float:
    """Percentage reduction in the tracking integral from C1 to S (positive = better).

    ``100 * (J_C1 − J_S) / J_C1``. The headline bar is ``>= 10%`` with a paired 95%
    bootstrap interval excluding zero (schema §G); this returns the point estimate.
    """

    if j_c1 <= 0.0:
        raise ValueError("j_c1 must be positive to form a percentage reduction")
    return float(100.0 * (j_c1 - j_s) / j_c1)
