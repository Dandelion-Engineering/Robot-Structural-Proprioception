"""Diagnosis-estimator lane: §D output contract, past-only window front-end, the
detection/abstention rung, the allowlisted oracle, and the online-seam adapter.

This is Claude's estimator lane (Claim Sheet Slots 1/5/7; schema §D/§F). It is the
*consumer* of the causal online seam (`utils.online_loop.run_online_rollout`) and the
*producer* of the schema-§D estimator outputs that `utils.metrics` scores. Because the
estimator defines the past-only window it reads, the frozen windowing constants `W`
and `stride` are proposed here (see `RECOMMENDED_WINDOW`).

Design boundaries (each traceable to the schema):
  * **Deployable/privileged boundary is structural.** The deployable estimators
    (`WindowNoveltyDetector` and future learned rungs) consume only an
    `ObservedRecord` for one suite (C0/C1/S) — never labels, privileged plant state,
    identity, or another suite. The `OracleInterface` is the *separate allowlisted*
    §D interface that reads privileged §B state; it is never importable by a
    deployable loader and exists only for the ceiling analyses.
  * **Past-only windows.** The front-end reads the bounded, already-availability-
    masked window returned by `OnlineSensorSession.available_record`; nothing here
    reaches forward in time (schema §D causality).
  * **Suite-agnostic front-end.** `WindowFeatureExtractor` emits a fixed-width feature
    vector and a fixed-shape `[W, D]` tensor over the full channel registry for every
    suite; channels a suite lacks contribute their masked "missing" pattern, so the
    matched C0/C1/S comparison holds estimator architecture constant and varies only
    the sensor suite (Slot 5).

The capacity ladder (Slot 9), in rungs that share this front-end and output contract:
  1. **`WindowNoveltyDetector`** (built here) — the interpretable *detection +
     calibrated-abstention* rung. It separates healthy from changed and gates
     abstention/unknown honestly, but makes **no** source-type attribution: without
     trained supervision it cannot say structure-vs-actuator-vs-sensor, so it splits
     the non-healthy mass uniformly and abstains on the fault type. This renders
     ladder stages (a) detect and the calibration/abstention layer today, on the real
     online seam, without fabricating a diagnosis that needs frozen training data.
  2. **`TemporalAttributionNet`** (specified; trained post-freeze) — the matched
     learned temporal-attribution head: a shared temporal encoder over the `[W, D]`
     window (dilated temporal-conv / GRU) feeding class/unknown/location/severity
     heads. Consumes `WindowFeatureExtractor.window_tensor`. This is the headline
     method; it is *specified* now so `W`/`stride` are well-defined, and *trained*
     only once `config.json` freezes and the confirmatory data exists (training on
     absent data would be fabrication).
  3. **`RMALatentEncoder`** (specified; trained post-freeze) — the RMA-style latent
     baseline: an encoder mapping the same `[W, D]` history to an adaptation latent a
     recovery policy consumes, giving "adapt without explicit attribution" as a
     control-only comparison (Slot 5 / Phase-0 point 3).

The learned rungs (2, 3) will live behind the same `DiagnosisEstimator` interface and
`window_tensor` front-end; their training/build is the post-config-freeze step, and
PyTorch (CUDA build, GPU verified) is installed then, not before, per the efficiency
standard (no capacity we cannot yet use).
"""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Callable

import numpy as np

from utils.schema_types import (
    CHANNEL_NAMES,
    CHANNEL_WIDTH,
    ObservedRecord,
    PlantStepState,
    observed_registry_width,
)
from utils.synchronous import harmonic_amplitude

# Canonical source-class order — must match utils.metrics.SOURCE_CLASS_ORDER so a
# p_class column means the same class in the estimator and in the scorer.
SOURCE_CLASS_ORDER: tuple[str, ...] = ("healthy", "structure", "actuator", "sensor")
N_SOURCE_CLASSES = len(SOURCE_CLASS_ORDER)
HEALTHY_INDEX = 0
FAULT_INDICES: tuple[int, ...] = tuple(range(1, N_SOURCE_CLASSES))  # structure/actuator/sensor

# Per-column summary statistics the interpretable front-end computes over a window.
FEATURE_STATS: tuple[str, ...] = ("last", "mean", "std", "slope")
N_FEATURE_STATS = len(FEATURE_STATS)

# The interpretable per-column summary appends two more entries after the FEATURE_STATS
# block, giving the fixed layout ``[last, mean, std, slope, sync_amplitude, valid_frac]``:
#   * a *synchronous (lock-in) amplitude* at the known diagnostic-probe frequency, and
#   * the column's valid fraction.
# The synchronous amplitude is the interpretable realization of the ~100x detector-referred
# headroom the S9 co-design found: a lock-in at the probe frequency rejects the thermal
# ramp / bias / drift that dominate the per-sample floor. (The learned rungs read the raw
# ``[W, D]`` tensor and can learn their own synchronous features.)
N_EXTRA_FEATURES = 2  # synchronous amplitude + valid fraction
SYNC_FEATURE_COL = N_FEATURE_STATS  # index of the synchronous amplitude within a column
VALID_FRACTION_COL = N_FEATURE_STATS + 1  # index of the valid fraction within a column

# Settled diagnostic-probe frequency (config-freeze table: a mechanics parameter, 0.8 Hz).
# The frozen config supplies the authoritative value; this default keeps the estimator
# runnable pre-freeze. The synchronous feature is keyed to this frequency.
DIAGNOSTIC_PROBE_HZ = 0.8
# A column's synchronous amplitude is estimated only when it has at least this many valid
# samples (the shared harmonic regression needs >= 5; we keep a margin) AND those samples
# span at least one full probe period, so the lock-in resolves a complete cycle rather than
# a poorly-conditioned arc (S9 Claude/Codex co-design: W >= one probe cycle).
MIN_SYNC_SAMPLES = 8

_EPS = 1.0e-12


# --------------------------------------------------------------------------- #
# §D estimator-output contract.
# --------------------------------------------------------------------------- #
@dataclass(frozen=True)
class EstimatorOutput:
    """One decision-step estimator output (schema §D `estimator_outputs`).

    Fields render the schema §D struct exactly so `utils.metrics` can score a run
    without translation. `p_class` is the known-class simplex in `SOURCE_CLASS_ORDER`;
    `unknown_score` is higher for more out-of-distribution; `abstain_decision` marks a
    declined known-class call; `location_out` is a joint index or −1 when not
    localized; `severity_out`/`severity_uncertainty` are the point/uncertainty of the
    severity estimate; `detection_time_s` is the time change was first flagged (NaN
    before detection). `step`/`decision_time_s` are bookkeeping, not scored.
    """

    step: int
    decision_time_s: float
    p_class: np.ndarray  # [4] known-class probabilities, sums to 1
    unknown_score: float
    abstain_decision: bool
    location_out: int = -1
    severity_out: float = 0.0
    severity_uncertainty: float = float("inf")
    detection_time_s: float = float("nan")

    def validate(self) -> None:
        """Fail loudly if the output violates the §D shape/range contract."""

        if not isinstance(self.step, (int, np.integer)) or int(self.step) < 0:
            raise ValueError("step must be a non-negative integer")
        if not np.isfinite(self.decision_time_s) or self.decision_time_s < 0.0:
            raise ValueError("decision_time_s must be finite and non-negative")
        probs = np.asarray(self.p_class, dtype=float)
        if probs.shape != (N_SOURCE_CLASSES,):
            raise ValueError(f"p_class must be shape ({N_SOURCE_CLASSES},), got {probs.shape}")
        if not np.all(np.isfinite(probs)):
            raise ValueError("p_class must be finite")
        if probs.min() < -1.0e-6 or probs.max() > 1.0 + 1.0e-6:
            raise ValueError("p_class entries must lie in [0, 1]")
        if not np.isclose(probs.sum(), 1.0, atol=1.0e-4):
            raise ValueError("p_class must sum to 1 (known-class simplex)")
        if not np.isfinite(self.unknown_score):
            raise ValueError("unknown_score must be finite")
        if not isinstance(self.abstain_decision, (bool, np.bool_)):
            raise ValueError("abstain_decision must be boolean")
        if not isinstance(self.location_out, (int, np.integer)) or int(self.location_out) < -1:
            raise ValueError("location_out must be a joint index or -1")
        if (
            not np.isfinite(self.severity_out)
            or np.isnan(self.severity_uncertainty)
            or self.severity_uncertainty < 0.0
        ):
            raise ValueError("severity_out finite and severity_uncertainty non-negative")
        if not np.isnan(self.detection_time_s):
            if (
                not np.isfinite(self.detection_time_s)
                or self.detection_time_s < 0.0
                or self.detection_time_s > self.decision_time_s + 1.0e-12
            ):
                raise ValueError(
                    "detection_time_s must be NaN or a finite time no later than decision_time_s"
                )


@dataclass
class EstimatorTrace:
    """The per-run sequence of estimator outputs (schema §E `estimator_outputs/<suite>`).

    Stacks per-decision `EstimatorOutput`s for one rollout and reduces them to the
    run-level quantities the confirmatory metrics score. Detection time is the first
    decision that flagged a change; the run-level class decision is the last decision's
    `p_class`/abstention (the settled diagnosis after the post-change window).
    """

    suite: str
    run_id: str
    outputs: list[EstimatorOutput] = field(default_factory=list)

    def append(self, output: EstimatorOutput) -> None:
        """Validate and append one decision-step output."""

        output.validate()
        if self.outputs:
            previous = self.outputs[-1]
            if output.step <= previous.step:
                raise ValueError("estimator-output steps must be strictly increasing")
            if output.decision_time_s <= previous.decision_time_s:
                raise ValueError("estimator-output decision times must be strictly increasing")
        self.outputs.append(output)

    def __len__(self) -> int:
        return len(self.outputs)

    @property
    def detection_time_s(self) -> float:
        """First decision time a change was flagged, or NaN if never flagged."""

        for out in self.outputs:
            if np.isfinite(out.detection_time_s):
                return float(out.detection_time_s)
        return float("nan")

    def final_p_class(self) -> np.ndarray:
        """The settled known-class simplex (last decision's `p_class`)."""

        if not self.outputs:
            raise ValueError("empty estimator trace has no final decision")
        return np.asarray(self.outputs[-1].p_class, dtype=float)

    def final_abstain(self) -> bool:
        """Whether the settled decision abstained on the known-class call."""

        if not self.outputs:
            raise ValueError("empty estimator trace has no final decision")
        return bool(self.outputs[-1].abstain_decision)

    def final_unknown_score(self) -> float:
        """The settled unknown/OOD score (last decision)."""

        if not self.outputs:
            raise ValueError("empty estimator trace has no final decision")
        return float(self.outputs[-1].unknown_score)

    def stack(self) -> dict[str, np.ndarray]:
        """Return the trace as parallel numeric arrays (for §E persistence/audit)."""

        if not self.outputs:
            raise ValueError("cannot stack an empty estimator trace")
        return {
            "step": np.asarray([o.step for o in self.outputs], dtype=np.int64),
            "decision_time_s": np.asarray([o.decision_time_s for o in self.outputs], dtype=float),
            "p_class": np.stack([np.asarray(o.p_class, dtype=float) for o in self.outputs]),
            "unknown_score": np.asarray([o.unknown_score for o in self.outputs], dtype=float),
            "abstain_decision": np.asarray([o.abstain_decision for o in self.outputs], dtype=bool),
            "location_out": np.asarray([o.location_out for o in self.outputs], dtype=np.int64),
            "severity_out": np.asarray([o.severity_out for o in self.outputs], dtype=float),
            "severity_uncertainty": np.asarray(
                [o.severity_uncertainty for o in self.outputs], dtype=float
            ),
            "detection_time_s": np.asarray([o.detection_time_s for o in self.outputs], dtype=float),
        }


# --------------------------------------------------------------------------- #
# Past-only window front-end (the concrete W/stride realization).
# --------------------------------------------------------------------------- #
@dataclass(frozen=True)
class RecommendedWindow:
    """A proposed frozen windowing setting with its rationale (schema §F)."""

    W: int  # past-only window length, samples
    stride: int  # decisions hop, samples between successive estimator updates
    rationale: str


# Proposed values for the frozen config (see the chat / progress report for the full
# argument). At f_ctrl = 500 Hz (dt = 2 ms): W = 640 samples ≈ 1.28 s spans a *full*
# 0.8 Hz diagnostic-probe period (1.25 s = 625 samples). Covering a complete cycle is
# what the synchronous window feature needs to resolve the probe (a sub-cycle window
# leaves the lock-in poorly conditioned — the S9 Claude/Codex co-design that moved the
# window from 512 to 640); stride = 8 samples runs the diagnosis at 62.5 Hz (the 500 Hz
# controller zero-order-holds the latest diagnosis between updates). These are
# config-freeze-time values, not pilot-blocking; a cheap pilot sweep over
# W ∈ {512, 640, 768} and stride ∈ {4, 8, 16} confirms them before the freeze.
RECOMMENDED_WINDOW = RecommendedWindow(
    W=640,
    stride=8,
    rationale=(
        "W=640 (~1.28 s at 500 Hz) covers a full 1.25 s (0.8 Hz) diagnostic-probe "
        "period, which the synchronous window feature requires to resolve a complete "
        "cycle (a sub-cycle window such as 512 leaves the lock-in poorly conditioned); "
        "stride=8 updates the diagnosis at 62.5 Hz under a 500 Hz zero-order-hold "
        "controller. Still a pilot-sweep proposal, not frozen: confirm with "
        "W∈{512,640,768}, stride∈{4,8,16} before freeze."
    ),
)


class WindowFeatureExtractor:
    """Turn a past-only observed window into a fixed tensor and a fixed feature vector.

    Both views are over the full fixed channel registry (schema §C), so their shapes
    are identical for C0/C1/S; a channel the suite lacks (all-NaN, masked off)
    contributes zeros and a zero validity indicator rather than changing the width.
    This is what lets the matched suite ablation hold the estimator constant.

    The summary feature vector (`window_features`) carries, per registry column,
    ``[last, mean, std, slope, sync_amplitude, valid_fraction]``. `sync_amplitude` is a
    synchronous (lock-in) amplitude at `probe_frequency_hz`, computed with the shared
    phase-invariant `utils.synchronous` harmonic regression on each channel's own
    measurement grid — the interpretable rung's realization of the ~100x detector-referred
    headroom over the per-sample floor. The learned rungs consume the raw `[W, D]` tensor
    (`window_tensor`) and can learn their own synchronous features, so the tensor is
    unchanged by this.
    """

    def __init__(
        self,
        window_steps: int = RECOMMENDED_WINDOW.W,
        *,
        probe_frequency_hz: float = DIAGNOSTIC_PROBE_HZ,
    ) -> None:
        """Set the fixed past-only window length and probe frequency; cache the layout."""

        if not isinstance(window_steps, (int, np.integer)) or int(window_steps) <= 0:
            raise ValueError("window_steps must be a positive integer")
        if not np.isfinite(probe_frequency_hz) or probe_frequency_hz <= 0.0:
            raise ValueError("probe_frequency_hz must be finite and positive")
        self.window_steps = int(window_steps)
        self.probe_frequency_hz = float(probe_frequency_hz)
        self.registry_width = observed_registry_width()
        # Column offsets so a [T, registry_width] tensor concatenates channels in the
        # fixed CHANNEL_NAMES order.
        self._offsets: dict[str, int] = {}
        offset = 0
        for name in CHANNEL_NAMES:
            self._offsets[name] = offset
            offset += CHANNEL_WIDTH[name]

    @property
    def n_features(self) -> int:
        """Length of the summary feature vector.

        ``registry_width × (#FEATURE_STATS + synchronous amplitude + valid fraction)``.
        """

        return self.registry_width * (N_FEATURE_STATS + N_EXTRA_FEATURES)

    def window_tensor(self, record: ObservedRecord) -> tuple[np.ndarray, np.ndarray]:
        """Return ``(values[T, D], valid[T, D])`` over the registry for the learned rungs.

        Invalid/unavailable/undelivered entries are filled with 0.0 in ``values`` and
        marked ``False`` in ``valid``; a learned model consumes both so it is never
        fed a silently-imputed value without its mask (schema §C [C4]).
        """

        t = record.n_steps
        if t <= 0:
            raise ValueError("observed window must contain at least one step")
        if t > self.window_steps:
            raise ValueError(
                f"observed window has {t} steps, exceeding fixed W={self.window_steps}"
            )
        values = np.zeros((self.window_steps, self.registry_width), dtype=float)
        valid = np.zeros((self.window_steps, self.registry_width), dtype=bool)
        row_start = self.window_steps - t
        for name in CHANNEL_NAMES:
            off = self._offsets[name]
            width = CHANNEL_WIDTH[name]
            col = np.asarray(record.values[name], dtype=float)
            mask = np.asarray(record.valid_mask[name])
            expected = (t, width)
            if col.shape != expected or mask.shape != expected:
                raise ValueError(
                    f"{name} values/mask must both have shape {expected}, got "
                    f"{col.shape}/{mask.shape}"
                )
            if mask.dtype != np.bool_:
                raise ValueError(f"{name} valid_mask must use boolean dtype")
            filled = np.where(mask, col, 0.0)
            values[row_start:, off : off + width] = np.nan_to_num(filled, nan=0.0)
            valid[row_start:, off : off + width] = mask
        return values, valid

    def window_features(self, record: ObservedRecord) -> np.ndarray:
        """Return a fixed-width per-column summary feature vector for the window.

        For each registry column, over the valid samples in the window: the last valid
        value, mean, std, a linear slope (per second), a **synchronous (lock-in)
        amplitude at the probe frequency**, and the column's valid fraction — the fixed
        per-column layout ``[last, mean, std, slope, sync, valid_fraction]``.

        The synchronous amplitude is the phase-invariant harmonic-regression coefficient
        magnitude at ``probe_frequency_hz`` (shared ``utils.synchronous``: one joint
        intercept + linear-trend + cosine + sine fit), on the channel's own measurement
        grid. It is emitted only when the column's valid samples span at least one full
        probe period, so a complete cycle is resolved rather than a poorly-conditioned arc
        (S9 co-design: W >= one probe cycle); otherwise it is 0.0. Columns with no valid
        sample contribute zeros and a zero valid fraction — a suite-agnostic, NaN-safe
        reduction the interpretable rung uses.
        """

        values, valid = self.window_tensor(record)
        t = record.n_steps
        row_start = self.window_steps - t
        feats = np.zeros((self.registry_width, N_FEATURE_STATS + N_EXTRA_FEATURES), dtype=float)
        probe_period_s = 1.0 / self.probe_frequency_hz
        for name in CHANNEL_NAMES:
            off = self._offsets[name]
            width = CHANNEL_WIDTH[name]
            times_raw = np.asarray(record.measurement_time_s[name], dtype=float)
            if times_raw.shape != (t,):
                raise ValueError(
                    f"{name} measurement_time_s must have shape {(t,)}, got {times_raw.shape}"
                )
            times = np.full(self.window_steps, np.nan, dtype=float)
            times[row_start:] = times_raw
            for local_col in range(width):
                col = off + local_col
                col_valid = valid[:, col]
                n_valid = int(np.count_nonzero(col_valid))
                feats[col, VALID_FRACTION_COL] = n_valid / self.window_steps
                if n_valid == 0:
                    continue
                ct = times[col_valid]
                if not np.all(np.isfinite(ct)):
                    raise ValueError(f"valid {name} samples require finite measurement times")
                v = values[col_valid, col]
                feats[col, 0] = v[-1]  # last valid
                feats[col, 1] = float(np.mean(v))
                feats[col, 2] = float(np.std(v))
                if n_valid >= 2 and np.ptp(ct) > _EPS:
                    # least-squares slope on this channel's own measurement grid.
                    feats[col, 3] = float(np.polyfit(ct - ct[0], v, 1)[0])
                # Synchronous (lock-in) amplitude at the probe frequency — only once the
                # valid samples span a full probe period (a complete cycle) on a strictly
                # increasing grid; otherwise the lock-in is ill-posed and it stays 0.0.
                if (
                    n_valid >= MIN_SYNC_SAMPLES
                    and np.ptp(ct) + _EPS >= probe_period_s
                    and np.all(np.diff(ct) > 0.0)
                ):
                    feats[col, SYNC_FEATURE_COL] = harmonic_amplitude(
                        v, np.ones(v.shape[0], dtype=bool), ct, self.probe_frequency_hz
                    )
        return feats.reshape(-1)


# --------------------------------------------------------------------------- #
# Estimator interface and the interpretable detection/abstention rung.
# --------------------------------------------------------------------------- #
class DiagnosisEstimator:
    """Interface for a causal diagnosis estimator over the online seam.

    Concrete rungs implement `reset` and `update`; the learned rungs will subclass this
    with the same signature so the recovery controller and the eval are agnostic to the
    rung. `update` receives the availability-masked past-only window (or ``None`` before
    the first delivered observation) and returns one `EstimatorOutput`.
    """

    def reset(self) -> None:
        """Reset per-rollout state before a new run."""

        raise NotImplementedError

    def update(
        self, step_index: int, decision_time_s: float, window: ObservedRecord | None
    ) -> EstimatorOutput:
        """Consume the past-only window and return one decision-step §D output."""

        raise NotImplementedError


class WindowNoveltyDetector(DiagnosisEstimator):
    """Interpretable detection + calibrated-abstention rung (ladder stage a).

    Fits a healthy feature reference (mean/std per feature) and scores each window by
    a top-k sparse-change z statistic against that reference — a standard,
    dependency-light novelty/change statistic. It separates healthy from changed and
    reports `detection_time_s`, an `unknown_score`, a calibrated `abstain_decision`,
    and an honest `p_class` that splits healthy-vs-not but **not** the fault type: the
    structure/actuator/sensor split is the learned head's job (rung 2), so all
    non-healthy mass is spread uniformly and the detector abstains on the fault type.

    This is deliberately not Codex's interpretable *residual/linear-sysID* baseline
    (that is a physics-model residual in the plant lane); this rung is an
    observation-statistics novelty gate in the estimator lane, whose purpose is to
    exercise the detection/abstention/unknown layer on the real seam.
    """

    def __init__(
        self,
        extractor: WindowFeatureExtractor | None = None,
        *,
        detect_threshold: float = 4.0,
        abstain_threshold: float = 2.5,
        persistence: int = 3,
        top_k: int = 8,
    ) -> None:
        """Configure the novelty gate.

        Thresholds are in **sigma-above-healthy** units: the raw sparse-change statistic
        is standardized against the healthy score distribution estimated at fit time
        (leave-one-out on the reference), so the operating points are interpretable and
        robust to the feature dimensionality rather than tied to absolute z magnitudes.

        Args:
            extractor: shared front-end (a default is created if none is given).
            detect_threshold: standardized novelty (sigma) above which a change is
                declared.
            abstain_threshold: standardized novelty (sigma) above which the known-class
                call is declined (ambiguous band between healthy and a confident call).
            persistence: consecutive over-threshold decisions required to latch
                detection, so a single noisy window does not trip it.
            top_k: the raw statistic is the mean of the ``top_k`` largest per-feature
                |z| deviations, so a *localized* change in a few channels is not diluted
                by the many unaffected features (a sparse-change statistic).
        """

        if detect_threshold <= 0.0 or abstain_threshold <= 0.0:
            raise ValueError("thresholds must be positive")
        if abstain_threshold > detect_threshold:
            raise ValueError("abstain_threshold must be <= detect_threshold")
        if persistence < 1:
            raise ValueError("persistence must be >= 1")
        if top_k < 1:
            raise ValueError("top_k must be >= 1")
        self.extractor = extractor or WindowFeatureExtractor()
        self.detect_threshold = float(detect_threshold)
        self.abstain_threshold = float(abstain_threshold)
        self.persistence = int(persistence)
        self.top_k = int(top_k)
        self._ref_mean: np.ndarray | None = None
        self._ref_std: np.ndarray | None = None
        self._healthy_score_mean: float = 0.0
        self._healthy_score_std: float = 1.0
        self.reset()

    def fit_reference(self, healthy_windows: list[ObservedRecord]) -> "WindowNoveltyDetector":
        """Fit the healthy feature reference (per-feature mean and std).

        The reference is the calibration distribution the novelty score standardizes
        against. It is fit on **healthy** windows only (schema/Claim-Sheet: the healthy
        class is always present); the operating thresholds are then frozen before
        confirmatory use, exactly as the OOD threshold is (metrics.py).
        """

        if not healthy_windows:
            raise ValueError("need at least one healthy window to fit the reference")
        feats = np.stack([self.extractor.window_features(w) for w in healthy_windows])
        self._ref_mean = feats.mean(axis=0)
        std = feats.std(axis=0)
        # floor the std so constant/near-constant features do not blow up the z-score
        self._ref_std = np.where(std > 1.0e-6, std, 1.0)
        # Calibrate the healthy score distribution by leave-one-out so operating
        # thresholds read in sigma-above-healthy (robust to feature dimensionality).
        n = feats.shape[0]
        if n >= 3:
            loo = np.empty(n)
            for i in range(n):
                others = np.delete(feats, i, axis=0)
                m = others.mean(axis=0)
                s = others.std(axis=0)
                s = np.where(s > 1.0e-6, s, 1.0)
                loo[i] = self._raw_from_feats(feats[i], m, s)
            self._healthy_score_mean = float(loo.mean())
            self._healthy_score_std = float(max(loo.std(), 1.0e-3))
        else:
            # too few windows to estimate a spread; fall back to raw scores (sigma==raw)
            self._healthy_score_mean = 0.0
            self._healthy_score_std = 1.0
        return self

    def _raw_from_feats(self, feats: np.ndarray, mean: np.ndarray, std: np.ndarray) -> float:
        """Top-k mean |z| of a feature vector against a given (mean, std) reference."""

        z = np.abs((feats - mean) / std)
        k = min(self.top_k, z.shape[0])
        return float(np.mean(np.partition(z, -k)[-k:]))

    def reset(self) -> None:
        """Reset per-rollout detection latch and timing."""

        self._over_count = 0
        self._detection_time_s = float("nan")

    def novelty_score(self, window: ObservedRecord) -> float:
        """Standardized novelty (sigma above the healthy mean) for one window.

        The raw statistic is the mean of the ``top_k`` largest per-feature |z|
        deviations from the reference — sensitive to a change confined to a few channels
        (an encoder bias, a single-station strain shift) without the many unaffected
        near-zero-|z| features diluting it (the failure mode of a plain
        RMS-over-all-features score). It is then standardized against the healthy score
        distribution so the returned value is in sigma-above-healthy units.
        """

        if self._ref_mean is None or self._ref_std is None:
            raise ValueError("fit_reference must be called before scoring")
        feats = self.extractor.window_features(window)
        raw = self._raw_from_feats(feats, self._ref_mean, self._ref_std)
        return (raw - self._healthy_score_mean) / self._healthy_score_std

    def update(
        self, step_index: int, decision_time_s: float, window: ObservedRecord | None
    ) -> EstimatorOutput:
        """Score one window and emit the §D detection/abstention output."""

        if window is None:
            # No delivered observation yet: assume healthy, no detection, do not abstain.
            p = np.zeros(N_SOURCE_CLASSES)
            p[HEALTHY_INDEX] = 1.0
            return EstimatorOutput(
                step=step_index,
                decision_time_s=decision_time_s,
                p_class=p,
                unknown_score=0.0,
                abstain_decision=False,
                detection_time_s=self._detection_time_s,
            )
        score = self.novelty_score(window)
        if score >= self.detect_threshold:
            self._over_count += 1
        else:
            self._over_count = 0
        if self._over_count >= self.persistence and not np.isfinite(self._detection_time_s):
            self._detection_time_s = decision_time_s

        # Honest healthy-vs-not simplex: a logistic in the novelty score, centered on
        # the abstain band, so a clearly-healthy window reads confidently healthy and a
        # clearly-changed one reads mostly not-healthy; the remaining (non-healthy) mass
        # spreads uniformly over the fault classes (no type attribution is claimed).
        scale = max((self.detect_threshold - self.abstain_threshold) / 2.0, 0.25)
        x = float(np.clip((score - self.abstain_threshold) / scale, -30.0, 30.0))
        healthy_prob = float(np.clip(1.0 / (1.0 + np.exp(x)), 0.02, 0.98))
        p = np.empty(N_SOURCE_CLASSES)
        p[HEALTHY_INDEX] = healthy_prob
        p[list(FAULT_INDICES)] = (1.0 - healthy_prob) / len(FAULT_INDICES)
        # Abstain on the *type* call once the window is out of the confident-healthy
        # band: detection without a trained classifier is exactly when to decline.
        abstain = bool(score >= self.abstain_threshold)
        return EstimatorOutput(
            step=step_index,
            decision_time_s=decision_time_s,
            p_class=p,
            unknown_score=score,
            abstain_decision=abstain,
            location_out=-1,
            severity_out=0.0,
            severity_uncertainty=float("inf"),
            detection_time_s=self._detection_time_s,
        )


# --------------------------------------------------------------------------- #
# Oracle interface (separate allowlisted §D interface; privileged, never deployable).
# --------------------------------------------------------------------------- #
class OracleInterface:
    """The allowlisted privileged oracle `O` (schema §D) — the diagnosis ceiling.

    Unlike every deployable rung, this reads privileged §B state (`PlantStepState`) and
    the run's true fault metadata, so it reports the *best attainable* diagnosis given
    perfect knowledge. It is a **separate interface**, never importable by a deployable
    loader, used only for the oracle-ceiling analyses (Slot 5: how much of the gap S
    closes toward O). It takes privileged input explicitly so the boundary is visible
    in the type signature.
    """

    def __init__(
        self,
        true_source_index: int,
        *,
        location: int = -1,
        severity: float = 0.0,
        onset_time_s: float = 0.0,
    ) -> None:
        """Bind the oracle to a run's ground-truth source class and fault parameters."""

        if not 0 <= int(true_source_index) < N_SOURCE_CLASSES:
            raise ValueError(f"true_source_index must be in [0, {N_SOURCE_CLASSES})")
        if not np.isfinite(onset_time_s) or onset_time_s < 0.0:
            raise ValueError("onset_time_s must be finite and non-negative")
        self.true_source_index = int(true_source_index)
        self.location = int(location)
        self.severity = float(severity)
        self.onset_time_s = float(onset_time_s)

    def update(self, step_index: int, state: PlantStepState) -> EstimatorOutput:
        """Return the perfect-knowledge §D output from privileged plant state."""

        fault_active = (
            self.true_source_index != HEALTHY_INDEX
            and float(state.t_s) + 1.0e-12 >= self.onset_time_s
        )
        active_index = self.true_source_index if fault_active else HEALTHY_INDEX
        p = np.zeros(N_SOURCE_CLASSES)
        p[active_index] = 1.0
        detected = self.onset_time_s if fault_active else float("nan")
        return EstimatorOutput(
            step=step_index,
            decision_time_s=float(state.t_s),
            p_class=p,
            unknown_score=0.0,
            abstain_decision=False,
            location_out=self.location if fault_active else -1,
            severity_out=self.severity if fault_active else 0.0,
            severity_uncertainty=0.0 if fault_active else float("inf"),
            detection_time_s=detected,
        )


# --------------------------------------------------------------------------- #
# Online-seam adapter: wrap an estimator (+ recovery command) into a CommandPolicy.
# --------------------------------------------------------------------------- #
# The recovery controller is Codex's lane; the estimator lane injects it as a callback
# `(EstimatorOutput, step_index, decision_time_s) -> command[N_JOINTS]`. The default is
# a passive zero command so the seam is exercisable before the controller lands.
RecoveryCommand = Callable[[EstimatorOutput, int, float], np.ndarray]


def passive_command(_output: EstimatorOutput, _step_index: int, _decision_time_s: float) -> np.ndarray:
    """Default recovery command: hold zero torque (a placeholder for Codex's controller)."""

    from utils.schema_types import N_JOINTS

    return np.zeros(N_JOINTS)


class EstimatorCommandPolicy:
    """Adapt an estimator (+ recovery command) to the `run_online_rollout` seam.

    Instances are callable with the `CommandPolicy` signature
    ``(step_index, decision_time_s, available) -> command`` and, as a side effect,
    accumulate the per-update `EstimatorOutput`s into `self.trace` (the §D
    estimator-outputs role). The estimator runs every `stride` decisions; between
    updates the controller reuses the latest output (zero-order hold), matching the
    schema's `stride` semantics.
    """

    def __init__(
        self,
        estimator: DiagnosisEstimator,
        *,
        suite: str,
        run_id: str = "run",
        stride: int = 1,
        recovery_command: RecoveryCommand = passive_command,
    ) -> None:
        """Bind the estimator, its diagnosis cadence, and the recovery command."""

        if stride < 1:
            raise ValueError("stride must be >= 1")
        self.estimator = estimator
        self.stride = int(stride)
        self.recovery_command = recovery_command
        self.trace = EstimatorTrace(suite=suite, run_id=run_id)
        self._last_output: EstimatorOutput | None = None
        estimator.reset()

    def __call__(
        self, step_index: int, decision_time_s: float, available: ObservedRecord | None
    ) -> np.ndarray:
        """Run the estimator on stride steps, hold otherwise, and return the command."""

        if step_index % self.stride == 0 or self._last_output is None:
            output = self.estimator.update(step_index, decision_time_s, available)
            self.trace.append(output)
            self._last_output = output
        else:
            output = self._last_output
        from utils.schema_types import N_JOINTS

        command = np.asarray(
            self.recovery_command(output, step_index, decision_time_s), dtype=float
        )
        if command.shape != (N_JOINTS,) or not np.all(np.isfinite(command)):
            raise ValueError("recovery_command must return a finite N_JOINTS vector")
        return command
