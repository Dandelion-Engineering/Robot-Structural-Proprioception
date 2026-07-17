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
      - OOD: `ood_auroc`, `ood_auprc`, validation-set threshold selection at a
        fixed unknown-detection sensitivity, and held-out false acceptance.

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


def _check_predictions(
    y_pred: np.ndarray, n_expected: int, *, allow_abstain: bool
) -> np.ndarray:
    """Validate hard source-class predictions, optionally allowing `ABSTAIN`."""

    pred = np.asarray(y_pred)
    if pred.shape != (n_expected,):
        raise ValueError(f"y_pred must be a length-{n_expected} vector")
    if not np.issubdtype(pred.dtype, np.integer):
        raise ValueError("y_pred must contain integer source-class indices")
    allowed_low = ABSTAIN if allow_abstain else 0
    if pred.size and (pred.min() < allowed_low or pred.max() >= N_SOURCE_CLASSES):
        allowed = (
            f"{ABSTAIN} or [0, {N_SOURCE_CLASSES})"
            if allow_abstain
            else f"[0, {N_SOURCE_CLASSES})"
        )
        raise ValueError(f"y_pred entries must lie in {allowed}")
    return pred


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
    abstain = np.asarray(abstain_decision)
    if abstain.shape != (probs.shape[0],):
        raise ValueError("abstain_decision must be a length-N boolean vector")
    if abstain.dtype != np.bool_:
        raise ValueError("abstain_decision must be boolean")
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
    pred = _check_predictions(y_pred, labels.shape[0], allow_abstain=True)
    return float(
        f1_score(labels, pred, labels=list(CLASS_INDICES), average="macro", zero_division=0.0)
    )


def per_class_recall(y_true: np.ndarray, y_pred: np.ndarray) -> dict[str, float]:
    """Per-source-class recall (abstentions and misclassifications both lower it).

    Returns a name-keyed dict so the −0.02 non-inferiority check (every source-class
    recall difference's lower 95% bound above −0.02) reads by class rather than index.
    """

    labels = _check_labels(y_true)
    pred = _check_predictions(y_pred, labels.shape[0], allow_abstain=True)
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
    pred = _check_predictions(y_pred_class, labels.shape[0], allow_abstain=False)
    conf = np.asarray(confidence, dtype=float)
    if not (labels.shape == pred.shape == conf.shape):
        raise ValueError("y_true, y_pred_class, confidence must share shape")
    if labels.size == 0:
        raise ValueError("risk_coverage_curve needs at least one sample")
    if not np.all(np.isfinite(conf)):
        raise ValueError("confidence contains non-finite values")
    order = np.argsort(-conf, kind="stable")  # most confident first
    sorted_conf = conf[order]
    wrong = (pred[order] != labels[order]).astype(float)
    n = labels.shape[0]
    # A threshold cannot split equal-confidence samples. Report only the end of each
    # tie group so the curve is invariant to input order within a tied score.
    group_end = np.r_[sorted_conf[1:] != sorted_conf[:-1], True]
    accepted = np.flatnonzero(group_end) + 1
    coverage = accepted / n
    risk = np.cumsum(wrong)[accepted - 1] / accepted
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

    abstain = np.asarray(abstain_decision)
    ood = np.asarray(ood_flag)
    if abstain.shape != ood.shape or abstain.ndim != 1:
        raise ValueError("abstain_decision and ood_flag must be 1-D and the same length")
    if abstain.dtype != np.bool_ or ood.dtype != np.bool_:
        raise ValueError("abstain_decision and ood_flag must be boolean")
    in_dist = ~ood
    if not np.any(in_dist):
        return 0.0
    return float(np.mean(abstain[in_dist]))


# --------------------------------------------------------------------------- #
# Layer 1 — diagnosis: out-of-distribution detection.
# --------------------------------------------------------------------------- #
def _check_ood_inputs(ood_flag: np.ndarray, unknown_score: np.ndarray) -> tuple[np.ndarray, np.ndarray]:
    """Validate OOD detection inputs: a boolean label and a real-valued score."""

    ood = np.asarray(ood_flag)
    score = np.asarray(unknown_score, dtype=float)
    if ood.shape != score.shape or ood.ndim != 1:
        raise ValueError("ood_flag and unknown_score must be 1-D and the same length")
    if not np.all(np.isfinite(score)):
        raise ValueError("unknown_score contains non-finite values")
    if ood.dtype != np.bool_:
        raise ValueError("ood_flag must be boolean")
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


def unknown_threshold_at_sensitivity(
    calibration_ood_scores: np.ndarray, *, sensitivity: float = 0.95
) -> float:
    """Choose an unknown-score threshold on validation OOD at fixed sensitivity.

    Higher scores mean more likely OOD and scores at or above the threshold are
    detected as unknown. The returned threshold detects at least ``sensitivity`` of
    the supplied *calibration/validation* OOD cases. It must be frozen before use on
    confirmatory data; selecting and evaluating it on the same cases would leak the
    operating point into the held-out result.
    """

    scores = np.asarray(calibration_ood_scores, dtype=float)
    if scores.ndim != 1 or scores.size == 0:
        raise ValueError("calibration_ood_scores must be a non-empty 1-D vector")
    if not np.all(np.isfinite(scores)):
        raise ValueError("calibration_ood_scores contains non-finite values")
    if not 0.0 < sensitivity <= 1.0:
        raise ValueError("sensitivity must be in (0, 1]")
    required_detected = int(np.ceil(sensitivity * scores.size))
    descending = np.sort(scores)[::-1]
    return float(descending[required_detected - 1])


def ood_false_acceptance_rate(
    ood_flag: np.ndarray, unknown_score: np.ndarray, *, threshold: float
) -> float:
    """Held-out OOD false-acceptance rate at a pre-frozen unknown threshold.

    An OOD case is falsely accepted as known when its score is below ``threshold``.
    The threshold should come from `unknown_threshold_at_sensitivity` on validation
    data, matching the Claim Sheet's 95% unknown-detection-sensitivity operating point.
    """

    ood = np.asarray(ood_flag)
    score = np.asarray(unknown_score, dtype=float)
    if ood.shape != score.shape or ood.ndim != 1:
        raise ValueError("ood_flag and unknown_score must be 1-D and the same length")
    if ood.dtype != np.bool_:
        raise ValueError("ood_flag must be boolean")
    if not np.all(np.isfinite(score)) or not np.isfinite(threshold):
        raise ValueError("unknown scores and threshold must be finite")
    if not np.any(ood):
        raise ValueError("at least one held-out OOD sample is required")
    return float(np.mean(score[ood] < threshold))


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
    if not (
        np.all(np.isfinite(times))
        and np.all(np.isfinite(reference))
        and np.all(np.isfinite(output))
    ):
        raise ValueError("tracking inputs must be finite")
    if times.shape[0] < 2 or np.any(np.diff(times) <= 0.0):
        raise ValueError("t_s must be strictly increasing with at least two samples")
    steps = np.diff(times)
    if not np.allclose(steps, steps[0], rtol=1.0e-7, atol=1.0e-12):
        raise ValueError("t_s must lie on one uniform control grid")
    tol = 1.0e-9
    window_end = onset_time_s + window_s
    in_window = (times >= onset_time_s - tol) & (times <= window_end + tol)
    if np.count_nonzero(in_window) < 2:
        raise ValueError("the analysis window contains fewer than two control samples")
    selected_times = times[in_window]
    if not np.isclose(selected_times[0], onset_time_s, rtol=0.0, atol=tol):
        raise ValueError("the analysis window is missing the onset control sample")
    if not np.isclose(selected_times[-1], window_end, rtol=0.0, atol=tol):
        raise ValueError("the analysis window is truncated before onset + window_s")
    error = reference[in_window] - output[in_window]
    error_norm = np.linalg.norm(error, axis=1)  # L2 over planar (x, y)
    return float(np.trapezoid(error_norm, selected_times))


def tracking_reduction_pct(j_c1: float, j_s: float) -> float:
    """Percentage reduction in the tracking integral from C1 to S (positive = better).

    ``100 * (J_C1 − J_S) / J_C1``. The headline bar is ``>= 10%`` with a paired 95%
    bootstrap interval excluding zero (schema §G); this returns the point estimate.
    """

    if j_c1 <= 0.0:
        raise ValueError("j_c1 must be positive to form a percentage reduction")
    return float(100.0 * (j_c1 - j_s) / j_c1)
