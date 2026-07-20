"""Interpretable linear system-ID residual baseline for fault attribution.

The Claim Sheet requires a simple residual/linear-system-identification comparator so
the matched learned estimator is not compared only with another black box. This module
implements that floor on the deployable observation side of the causal seam:

* fit one affine, ridge-regularized ARX predictor on healthy ``ObservedRecord`` windows;
* reduce its one-step prediction errors to signed-mean, RMS, and availability residuals;
* fit transparent four-class residual centroids on labeled development windows; and
* calibrate the off-prototype abstention threshold on a separate known-class set.

The same code is used for C0, C1, and S. A fitted instance is bound to one suite and
uses only channels physically present in that suite; ``tau_cmd`` is the known exogenous
input and is never treated as a predicted state. No privileged plant field, label, run
identity, or matched-suite record is accepted by the online ``update`` interface.

This is a development implementation, not a frozen model or a result. Dynamics-fit,
prototype-fit, and abstention-calibration records must come from the eventual frozen
role-separated manifest before confirmatory use.
"""

from __future__ import annotations

from dataclasses import dataclass
from math import ceil
from typing import Mapping, Sequence

import numpy as np

from utils.estimator import (
    DiagnosisEstimator,
    EstimatorOutput,
    HEALTHY_INDEX,
    N_SOURCE_CLASSES,
    SOURCE_CLASS_ORDER,
)
from utils.schema_types import CHANNEL_NAMES, CHANNEL_WIDTH, SUITE_CHANNELS, ObservedRecord


COMMAND_CHANNEL = "tau_cmd"
RESIDUAL_STATS: tuple[str, ...] = ("signed_mean", "rms", "valid_fraction")


@dataclass(frozen=True)
class LinearResidualConfig:
    """Development settings for the linear residual attribution floor.

    ``ridge`` regularizes the normalized ARX coefficients (the intercept is left
    unpenalized). ``minimum_fit_transitions`` prevents a nominal model from being fit
    to an obviously underdetermined trace. ``residual_scale_floor`` bounds prototype
    standardization when a healthy residual feature is nearly constant.

    Class probabilities are a softmax over negative dimension-normalized centroid
    distances. They are comparison scores, not claimed calibrated probabilities; final
    probability calibration and operating thresholds remain validation-owned.
    """

    ridge: float = 1.0e-3
    minimum_fit_transitions: int = 32
    residual_scale_floor: float = 1.0e-3
    probability_temperature: float = 1.0
    minimum_class_probability: float = 0.5
    persistence: int = 3

    def validate(self) -> None:
        """Fail loudly when a baseline setting is non-physical or ambiguous."""

        positive = {
            "ridge": self.ridge,
            "residual_scale_floor": self.residual_scale_floor,
            "probability_temperature": self.probability_temperature,
        }
        for name, value in positive.items():
            if not np.isfinite(value) or value <= 0.0:
                raise ValueError(f"{name} must be finite and positive")
        if (
            not isinstance(self.minimum_fit_transitions, (int, np.integer))
            or int(self.minimum_fit_transitions) < 2
        ):
            raise ValueError("minimum_fit_transitions must be an integer >= 2")
        if not 0.0 < self.minimum_class_probability <= 1.0:
            raise ValueError("minimum_class_probability must lie in (0, 1]")
        if not isinstance(self.persistence, (int, np.integer)) or int(self.persistence) < 1:
            raise ValueError("persistence must be an integer >= 1")


class LinearResidualAttributionEstimator(DiagnosisEstimator):
    """Causal linear-ARX residual classifier and abstaining attribution floor.

    The nominal model predicts each live non-command sensor scalar at row ``t`` from
    the live sensor vector at ``t-1`` and the known command at ``t``. Missing inputs are
    mean-filled *after normalization* (therefore zero) and their validity bits are
    appended to the regressor; invalid targets are excluded from that target's fit and
    residual aggregation. This keeps dropout explicit without discarding an entire
    transition because one unrelated channel is missing.

    Source attribution is intentionally simple: the window residual vector is compared
    with one standardized centroid per known class. The estimator does not localize a
    fault or estimate severity, so it cannot trigger active recovery by itself.
    """

    def __init__(self, config: LinearResidualConfig | None = None) -> None:
        """Validate and retain the provisional baseline configuration."""

        self.config = config or LinearResidualConfig()
        self.config.validate()
        self._suite: str | None = None
        self._state_channels: tuple[str, ...] = ()
        self._state_labels: tuple[str, ...] = ()
        self._state_mean: np.ndarray | None = None
        self._state_scale: np.ndarray | None = None
        self._command_mean: np.ndarray | None = None
        self._command_scale: np.ndarray | None = None
        self._coefficients: np.ndarray | None = None
        self._prototype_feature_mean: np.ndarray | None = None
        self._prototype_feature_scale: np.ndarray | None = None
        self._centroids: np.ndarray | None = None
        self._unknown_threshold: float | None = None
        self.reset()

    @property
    def suite(self) -> str | None:
        """Suite to which the fitted dynamics model is bound, or ``None`` before fit."""

        return self._suite

    @property
    def state_labels(self) -> tuple[str, ...]:
        """Ordered scalar sensor labels predicted by the nominal ARX model."""

        return self._state_labels

    @property
    def residual_feature_names(self) -> tuple[str, ...]:
        """Ordered human-readable names for the residual vector dimensions."""

        return tuple(
            f"{label}.{stat}" for label in self._state_labels for stat in RESIDUAL_STATS
        )

    @property
    def unknown_threshold(self) -> float | None:
        """Frozen development off-prototype threshold, or ``None`` before calibration."""

        return self._unknown_threshold

    def _record_layout(self, record: ObservedRecord) -> tuple[tuple[str, ...], tuple[str, ...]]:
        """Validate one observed record and return its live state channels/labels."""

        if not isinstance(record, ObservedRecord):
            raise TypeError("linear residual baseline accepts only ObservedRecord inputs")
        if record.n_steps <= 0:
            raise ValueError("observed record must contain at least one step")
        if record.suite not in SUITE_CHANNELS:
            raise ValueError(f"unknown deployable suite: {record.suite!r}")
        missing = set(CHANNEL_NAMES) - set(record.values)
        if missing:
            raise ValueError(f"observed record is missing registry channels: {sorted(missing)}")
        expected_channels = set(SUITE_CHANNELS[record.suite])
        actual_channels = {
            name
            for name in CHANNEL_NAMES
            if bool(record.suite_available_mask.get(name, False))
        }
        if actual_channels != expected_channels:
            raise ValueError(
                "suite_available_mask does not match the fixed deployable suite contract"
            )
        state_channels = tuple(
            name
            for name in CHANNEL_NAMES
            if name != COMMAND_CHANNEL and bool(record.suite_available_mask.get(name, False))
        )
        if not state_channels:
            raise ValueError("suite must expose at least one predicted sensor channel")
        if not bool(record.suite_available_mask.get(COMMAND_CHANNEL, False)):
            raise ValueError("suite must expose tau_cmd as the ARX exogenous input")
        labels: list[str] = []
        for name in CHANNEL_NAMES:
            width = CHANNEL_WIDTH[name]
            expected = (record.n_steps, width)
            values = np.asarray(record.values[name], dtype=float)
            valid = np.asarray(record.valid_mask[name])
            if values.shape != expected or valid.shape != expected:
                raise ValueError(
                    f"{name} values/mask must both have shape {expected}, got "
                    f"{values.shape}/{valid.shape}"
                )
            if valid.dtype != np.bool_:
                raise ValueError(f"{name} valid_mask must use boolean dtype")
            if np.any(valid & ~np.isfinite(values)):
                raise ValueError(f"valid {name} entries must be finite")
            if name in state_channels:
                labels.extend(f"{name}[{index}]" for index in range(width))
        return state_channels, tuple(labels)

    def _check_fitted_layout(self, record: ObservedRecord) -> None:
        """Require a record to match the suite and scalar layout used at dynamics fit."""

        channels, labels = self._record_layout(record)
        if self._suite is None:
            raise ValueError("fit_dynamics must be called before using the baseline")
        if (
            record.suite != self._suite
            or channels != self._state_channels
            or labels != self._state_labels
        ):
            raise ValueError(
                "observed record suite/layout does not match the fitted dynamics model"
            )

    @staticmethod
    def _flatten(record: ObservedRecord, channels: Sequence[str]) -> tuple[np.ndarray, np.ndarray]:
        """Concatenate selected registry channels into aligned value/valid matrices."""

        values = np.concatenate(
            [np.asarray(record.values[name], dtype=float) for name in channels], axis=1
        )
        valid = np.concatenate(
            [np.asarray(record.valid_mask[name], dtype=bool) for name in channels], axis=1
        )
        return values, valid

    @staticmethod
    def _masked_mean_scale(
        values: np.ndarray, valid: np.ndarray, *, name: str
    ) -> tuple[np.ndarray, np.ndarray]:
        """Return per-column mean/std over valid entries, failing on unsupported columns."""

        means = np.empty(values.shape[1], dtype=float)
        scales = np.empty(values.shape[1], dtype=float)
        for column in range(values.shape[1]):
            present = values[valid[:, column], column]
            if present.size < 2:
                raise ValueError(f"{name} column {column} has fewer than two valid samples")
            means[column] = float(np.mean(present))
            spread = float(np.std(present))
            scales[column] = spread if spread > 1.0e-6 else 1.0
        return means, scales

    def _normalized_record(
        self, record: ObservedRecord
    ) -> tuple[np.ndarray, np.ndarray, np.ndarray, np.ndarray]:
        """Return normalized state/command values plus their explicit validity masks."""

        self._check_fitted_layout(record)
        assert self._state_mean is not None and self._state_scale is not None
        assert self._command_mean is not None and self._command_scale is not None
        state, state_valid = self._flatten(record, self._state_channels)
        command, command_valid = self._flatten(record, (COMMAND_CHANNEL,))
        state_norm = np.where(state_valid, (state - self._state_mean) / self._state_scale, 0.0)
        command_norm = np.where(
            command_valid, (command - self._command_mean) / self._command_scale, 0.0
        )
        return state_norm, state_valid, command_norm, command_valid

    @staticmethod
    def _regressor_matrix(
        state_norm: np.ndarray,
        state_valid: np.ndarray,
        command_norm: np.ndarray,
        command_valid: np.ndarray,
    ) -> np.ndarray:
        """Build ``[1, x[t-1], mask[t-1], u[t], u_mask[t]]`` for each transition."""

        if state_norm.shape[0] < 2:
            return np.empty((0, 1 + 2 * state_norm.shape[1] + 2 * command_norm.shape[1]))
        return np.concatenate(
            [
                np.ones((state_norm.shape[0] - 1, 1), dtype=float),
                state_norm[:-1],
                state_valid[:-1].astype(float),
                command_norm[1:],
                command_valid[1:].astype(float),
            ],
            axis=1,
        )

    def fit_dynamics(
        self, healthy_records: Sequence[ObservedRecord]
    ) -> "LinearResidualAttributionEstimator":
        """Fit the normalized one-step ARX model on healthy deployable records only.

        A successful re-fit atomically replaces the dynamics model and invalidates all
        prototype/threshold state, because residual prototypes calibrated against the old
        model are not meaningful under a new nominal predictor.
        """

        records = list(healthy_records)
        if not records:
            raise ValueError("need at least one healthy record to fit dynamics")
        suite = records[0].suite
        state_channels, state_labels = self._record_layout(records[0])
        for record in records[1:]:
            channels, labels = self._record_layout(record)
            if record.suite != suite or channels != state_channels or labels != state_labels:
                raise ValueError("all dynamics-fit records must share one suite/layout")

        state_blocks: list[np.ndarray] = []
        state_valid_blocks: list[np.ndarray] = []
        command_blocks: list[np.ndarray] = []
        command_valid_blocks: list[np.ndarray] = []
        for record in records:
            state, state_valid = self._flatten(record, state_channels)
            command, command_valid = self._flatten(record, (COMMAND_CHANNEL,))
            state_blocks.append(state)
            state_valid_blocks.append(state_valid)
            command_blocks.append(command)
            command_valid_blocks.append(command_valid)
        state_all = np.concatenate(state_blocks, axis=0)
        state_valid_all = np.concatenate(state_valid_blocks, axis=0)
        command_all = np.concatenate(command_blocks, axis=0)
        command_valid_all = np.concatenate(command_valid_blocks, axis=0)
        state_mean, state_scale = self._masked_mean_scale(
            state_all, state_valid_all, name="state"
        )
        command_mean, command_scale = self._masked_mean_scale(
            command_all, command_valid_all, name="command"
        )

        regressors: list[np.ndarray] = []
        targets: list[np.ndarray] = []
        target_validity: list[np.ndarray] = []
        for state, state_valid, command, command_valid in zip(
            state_blocks,
            state_valid_blocks,
            command_blocks,
            command_valid_blocks,
        ):
            state_norm = np.where(state_valid, (state - state_mean) / state_scale, 0.0)
            command_norm = np.where(
                command_valid, (command - command_mean) / command_scale, 0.0
            )
            regressors.append(
                self._regressor_matrix(
                    state_norm, state_valid, command_norm, command_valid
                )
            )
            targets.append(state_norm[1:])
            target_validity.append(state_valid[1:])
        design = np.concatenate(regressors, axis=0)
        target = np.concatenate(targets, axis=0)
        target_valid = np.concatenate(target_validity, axis=0)
        if design.shape[0] < self.config.minimum_fit_transitions:
            raise ValueError(
                f"need at least {self.config.minimum_fit_transitions} healthy transitions, "
                f"got {design.shape[0]}"
            )

        coefficients = np.empty((design.shape[1], target.shape[1]), dtype=float)
        penalty = np.eye(design.shape[1], dtype=float) * self.config.ridge
        penalty[0, 0] = 0.0
        for column in range(target.shape[1]):
            keep = target_valid[:, column]
            if int(np.count_nonzero(keep)) < self.config.minimum_fit_transitions:
                raise ValueError(
                    f"state target {state_labels[column]} has too few valid transitions"
                )
            x = design[keep]
            y = target[keep, column]
            coefficients[:, column] = np.linalg.solve(x.T @ x + penalty, x.T @ y)
        if not np.all(np.isfinite(coefficients)):
            raise RuntimeError("linear dynamics fit produced non-finite coefficients")

        self._suite = suite
        self._state_channels = state_channels
        self._state_labels = state_labels
        self._state_mean = state_mean
        self._state_scale = state_scale
        self._command_mean = command_mean
        self._command_scale = command_scale
        self._coefficients = coefficients
        self._prototype_feature_mean = None
        self._prototype_feature_scale = None
        self._centroids = None
        self._unknown_threshold = None
        self.reset()
        return self

    def residual_vector(self, record: ObservedRecord) -> np.ndarray:
        """Return per-sensor signed-mean, RMS, and validity residual features."""

        if self._coefficients is None:
            raise ValueError("fit_dynamics must be called before computing residuals")
        state_norm, state_valid, command_norm, command_valid = self._normalized_record(record)
        if record.n_steps < 2:
            raise ValueError("residual vector requires at least two observed steps")
        design = self._regressor_matrix(
            state_norm, state_valid, command_norm, command_valid
        )
        prediction = design @ self._coefficients
        target = state_norm[1:]
        target_valid = state_valid[1:]
        features = np.zeros((target.shape[1], len(RESIDUAL_STATS)), dtype=float)
        for column in range(target.shape[1]):
            keep = target_valid[:, column]
            features[column, 2] = float(np.mean(keep))
            if not np.any(keep):
                continue
            residual = target[keep, column] - prediction[keep, column]
            features[column, 0] = float(np.mean(residual))
            features[column, 1] = float(np.sqrt(np.mean(np.square(residual))))
        vector = features.reshape(-1)
        if not np.all(np.isfinite(vector)):
            raise RuntimeError("residual feature vector must be finite")
        return vector

    def fit_prototypes(
        self, labeled_windows: Mapping[str, Sequence[ObservedRecord]]
    ) -> "LinearResidualAttributionEstimator":
        """Fit one standardized residual centroid per known source class.

        The mapping must contain exactly ``healthy/structure/actuator/sensor``. These
        are development/training roles, separate from the healthy records used to fit
        dynamics and from the known-class records later used to calibrate abstention.
        """

        if self._coefficients is None:
            raise ValueError("fit_dynamics must precede fit_prototypes")
        if set(labeled_windows) != set(SOURCE_CLASS_ORDER):
            raise ValueError(f"labeled_windows must contain exactly {SOURCE_CLASS_ORDER}")
        matrices: dict[str, np.ndarray] = {}
        for label in SOURCE_CLASS_ORDER:
            windows = list(labeled_windows[label])
            if not windows:
                raise ValueError(f"prototype class {label!r} has no windows")
            matrices[label] = np.stack([self.residual_vector(window) for window in windows])
        healthy = matrices["healthy"]
        feature_mean = healthy.mean(axis=0)
        raw_scale = healthy.std(axis=0)
        feature_scale = np.maximum(raw_scale, self.config.residual_scale_floor)
        centroids = np.stack(
            [
                np.mean((matrices[label] - feature_mean) / feature_scale, axis=0)
                for label in SOURCE_CLASS_ORDER
            ]
        )
        if not np.all(np.isfinite(centroids)):
            raise RuntimeError("residual prototype fit produced non-finite centroids")
        self._prototype_feature_mean = feature_mean
        self._prototype_feature_scale = feature_scale
        self._centroids = centroids
        self._unknown_threshold = None
        self.reset()
        return self

    def class_distances(self, window: ObservedRecord) -> np.ndarray:
        """Return dimension-normalized Euclidean distance to each residual centroid."""

        if (
            self._prototype_feature_mean is None
            or self._prototype_feature_scale is None
            or self._centroids is None
        ):
            raise ValueError("fit_prototypes must be called before class scoring")
        features = self.residual_vector(window)
        standardized = (features - self._prototype_feature_mean) / self._prototype_feature_scale
        distances = np.linalg.norm(self._centroids - standardized[None, :], axis=1)
        distances /= np.sqrt(standardized.size)
        if distances.shape != (N_SOURCE_CLASSES,) or not np.all(np.isfinite(distances)):
            raise RuntimeError("class distances violated the estimator contract")
        return distances

    def _probabilities_from_distances(self, distances: np.ndarray) -> np.ndarray:
        """Convert one validated class-distance vector into normalized class scores."""

        logits = -distances / self.config.probability_temperature
        logits -= np.max(logits)
        weights = np.exp(logits)
        return weights / np.sum(weights)

    def class_probabilities(self, window: ObservedRecord) -> np.ndarray:
        """Return softmax scores over negative residual-centroid distances."""

        return self._probabilities_from_distances(self.class_distances(window))

    def calibrate_unknown_threshold(
        self,
        known_calibration_windows: Mapping[str, Sequence[ObservedRecord]],
        *,
        false_abstention_rate: float = 0.05,
        min_tail_count: int = 5,
    ) -> float:
        """Freeze the off-prototype threshold on a separate known-class calibration set.

        The threshold is the higher-method ``(1 - false_abstention_rate)`` quantile of
        each known window's distance to its nearest class centroid. A tail-resolution
        guard requires at least ``ceil(min_tail_count / false_abstention_rate)`` windows,
        mirroring the coefficient detector's refusal to freeze an unresolved extreme
        quantile.
        """

        if self._centroids is None:
            raise ValueError("fit_prototypes must precede threshold calibration")
        if not 0.0 < false_abstention_rate < 1.0:
            raise ValueError("false_abstention_rate must lie in (0, 1)")
        if not isinstance(min_tail_count, (int, np.integer)) or int(min_tail_count) < 1:
            raise ValueError("min_tail_count must be a positive integer")
        if set(known_calibration_windows) != set(SOURCE_CLASS_ORDER):
            raise ValueError(
                f"known_calibration_windows must contain exactly {SOURCE_CLASS_ORDER}"
            )
        windows: list[ObservedRecord] = []
        for label in SOURCE_CLASS_ORDER:
            class_windows = list(known_calibration_windows[label])
            if not class_windows:
                raise ValueError(f"known calibration class {label!r} has no windows")
            windows.extend(class_windows)
        required = ceil(int(min_tail_count) / float(false_abstention_rate))
        if len(windows) < required:
            raise ValueError(
                f"need at least {required} known calibration windows to resolve the "
                f"false-abstention tail, got {len(windows)}"
            )
        nearest = np.asarray(
            [float(np.min(self.class_distances(window))) for window in windows]
        )
        threshold = float(
            np.quantile(nearest, 1.0 - false_abstention_rate, method="higher")
        )
        if not np.isfinite(threshold) or threshold < 0.0:
            raise RuntimeError("unknown threshold calibration produced an invalid value")
        self._unknown_threshold = threshold
        self.reset()
        return threshold

    def reset(self) -> None:
        """Reset the per-rollout detection persistence and latch."""

        self._fault_count = 0
        self._detection_time_s = float("nan")

    @staticmethod
    def _healthy_output(
        step_index: int, decision_time_s: float, detection_time_s: float
    ) -> EstimatorOutput:
        """Return the no-observation/startup healthy state used across estimators."""

        probabilities = np.zeros(N_SOURCE_CLASSES, dtype=float)
        probabilities[HEALTHY_INDEX] = 1.0
        return EstimatorOutput(
            step=step_index,
            decision_time_s=decision_time_s,
            p_class=probabilities,
            unknown_score=0.0,
            abstain_decision=False,
            location_out=-1,
            severity_out=0.0,
            severity_uncertainty=float("inf"),
            detection_time_s=detection_time_s,
        )

    def update(
        self, step_index: int, decision_time_s: float, window: ObservedRecord | None
    ) -> EstimatorOutput:
        """Score one past-only window and emit a schema-section-D attribution output."""

        if window is None or window.n_steps < 2:
            return self._healthy_output(step_index, decision_time_s, self._detection_time_s)
        if self._unknown_threshold is None:
            raise ValueError("calibrate_unknown_threshold must be called before online scoring")
        distances = self.class_distances(window)
        probabilities = self._probabilities_from_distances(distances)
        predicted = int(np.argmax(probabilities))
        confidence = float(probabilities[predicted])
        unknown_score = float(np.min(distances))
        abstain = bool(
            unknown_score > self._unknown_threshold
            or confidence < self.config.minimum_class_probability
        )
        actionable_fault = bool(predicted != HEALTHY_INDEX and not abstain)
        self._fault_count = self._fault_count + 1 if actionable_fault else 0
        if self._fault_count >= self.config.persistence and not np.isfinite(
            self._detection_time_s
        ):
            self._detection_time_s = float(decision_time_s)
        output = EstimatorOutput(
            step=step_index,
            decision_time_s=decision_time_s,
            p_class=probabilities,
            unknown_score=unknown_score,
            abstain_decision=abstain,
            location_out=-1,
            severity_out=0.0,
            severity_uncertainty=float("inf"),
            detection_time_s=self._detection_time_s,
        )
        output.validate()
        return output


__all__ = [
    "COMMAND_CHANNEL",
    "RESIDUAL_STATS",
    "LinearResidualAttributionEstimator",
    "LinearResidualConfig",
]
