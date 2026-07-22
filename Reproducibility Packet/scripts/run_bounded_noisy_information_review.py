"""Review noisy held-decision information on the bounded task/contact condition.

This development gate replaces the bounded mechanics screen's fixed source-correct
diagnoses with a real noisy coefficient-reference instrument.  It deliberately keeps
three questions separate:

1. information: do matched C1/S windows support healthy detection, attribution, and
   calibrated type abstention at the exact first causal post-probe decision?;
2. action gating: how often would the pilot-only diagnosis correctly authorize,
   falsely authorize, or withhold the transparent recovery actions?; and
3. mechanics: does one pre-movement decision, held for the full onset-plus-five-second
   audit, preserve the bounded contact and A1 safety properties?

References and abstention margins are fit independently per suite on calibration-only
sensor seeds.  Held-out seeds never tune a threshold.  The type probabilities remain
one-hot pilot instruments rather than calibrated learned-head probabilities, so this
artifact cannot freeze probability calibration, the task/contact profile, W/stride,
fault grids, controller settings, sensor constants, or ``config.json``.  Its one-seed
online continuation is a representative mechanism/safety audit, not an evaluation-
sized recovery comparison.
"""

from __future__ import annotations

import argparse
import concurrent.futures
import csv
import hashlib
import json
import math
from dataclasses import asdict, dataclass
from pathlib import Path
from typing import Any

import numpy as np

from run_noisy_reference_pilot import (
    causal_window,
    fault_specs,
    project_observed_suite,
)
from screen_bounded_task_contact import (
    CANONICAL_SOURCES,
    PHYSICAL_SOURCES,
    BoundedTaskContactSpec,
    SingleDecisionHoldEstimator,
    cable_config,
)
from screen_optional_contact_profile import count_contact_episodes
from utils.cable_plant import CablePlant
from utils.estimator import (
    DiagnosisEstimator,
    EstimatorOutput,
    N_SOURCE_CLASSES,
    SOURCE_CLASS_ORDER,
    WindowFeatureExtractor,
    coefficient_reference_distance,
    synchronous_coefficient_vector,
)
from utils.metrics import ABSTAIN, j_5s, macro_f1, per_class_recall
from utils.online_loop import run_online_rollout
from utils.schema_types import ObservedRecord, SAFETY_FLAG_FIELDS
from utils.sensor_model import OnlineSensorSession, SensorConfig
from utils.task_control import (
    EstimatorRecoveryTaskPolicy,
    ObservedJointPDController,
)


DEPLOYABLE_SUITES = ("C1", "S")
FAULT_SOURCES = ("structure", "actuator", "sensor")
ACTION_SOURCES = ("structure", "actuator")


@dataclass(frozen=True)
class BoundedNoisyInformationSpec:
    """Portable settings and predeclared gates for the held-decision review."""

    selected_plane_z_m: float = 0.200
    calibration_seeds: int = 100
    evaluation_seeds: int = 48
    base_seed: int = 14000
    representative_seed: int = 14100
    healthy_false_alarm_rate: float = 0.05
    calibration_minimum_tail_count: int = 5
    selective_error_ceiling: float = 0.05
    minimum_fault_detection_rate: float = 0.80
    minimum_fault_correct_confident_rate: float = 0.80
    maximum_healthy_false_actionable_rate: float = 0.05
    point_count: int = 17
    simulation_timestep_s: float = 1.0e-4

    def mechanics_spec(self) -> BoundedTaskContactSpec:
        """Return the exact bounded mechanics/controller condition under review."""

        return BoundedTaskContactSpec(
            plane_heights_z_m=(0.100, self.selected_plane_z_m),
            point_count=self.point_count,
            simulation_timestep_s=self.simulation_timestep_s,
        )

    @property
    def calibration_seed_values(self) -> tuple[int, ...]:
        """Return the calibration-only sensor-seed role."""

        return tuple(range(self.base_seed, self.base_seed + self.calibration_seeds))

    @property
    def evaluation_seed_values(self) -> tuple[int, ...]:
        """Return the disjoint held-out sensor-seed role."""

        start = self.base_seed + self.calibration_seeds
        return tuple(range(start, start + self.evaluation_seeds))

    @property
    def minimum_calibration_size(self) -> int:
        """Return the fail-loud size needed to resolve the declared healthy tail."""

        return int(
            math.ceil(
                self.calibration_minimum_tail_count / self.healthy_false_alarm_rate
            )
        )

    def validate(self) -> None:
        """Fail loudly when roles, thresholds, or bounded mechanics are malformed."""

        self.mechanics_spec().validate()
        if not np.isfinite(self.selected_plane_z_m) or self.selected_plane_z_m <= 0.0:
            raise ValueError("selected_plane_z_m must be finite and positive")
        if self.calibration_seeds < self.minimum_calibration_size:
            raise ValueError(
                "calibration_seeds cannot resolve the declared healthy tail; need at "
                f"least {self.minimum_calibration_size}"
            )
        if self.evaluation_seeds < 1:
            raise ValueError("evaluation_seeds must be positive")
        if self.base_seed < 0:
            raise ValueError("base_seed must be non-negative")
        if self.representative_seed not in self.evaluation_seed_values:
            raise ValueError("representative_seed must belong to the held-out role")
        if self.point_count < 3:
            raise ValueError("point_count must be at least three")
        if not np.isfinite(self.simulation_timestep_s) or self.simulation_timestep_s <= 0.0:
            raise ValueError("simulation_timestep_s must be finite and positive")
        for name, value in {
            "healthy_false_alarm_rate": self.healthy_false_alarm_rate,
            "selective_error_ceiling": self.selective_error_ceiling,
            "minimum_fault_detection_rate": self.minimum_fault_detection_rate,
            "minimum_fault_correct_confident_rate": (
                self.minimum_fault_correct_confident_rate
            ),
            "maximum_healthy_false_actionable_rate": (
                self.maximum_healthy_false_actionable_rate
            ),
        }.items():
            if not 0.0 < value < 1.0:
                raise ValueError(f"{name} must lie in (0, 1)")
        if self.calibration_minimum_tail_count < 1:
            raise ValueError("calibration_minimum_tail_count must be positive")


@dataclass(frozen=True)
class SelectivePrototypeReference:
    """Suite-specific healthy reference, prototypes, and calibrated type abstention."""

    healthy_mean: np.ndarray
    healthy_scale: np.ndarray
    detect_threshold: float
    fault_centroids: dict[str, np.ndarray]
    abstain_margin_threshold: float
    calibration_null_scores: np.ndarray
    calibration_selective_coverage: float
    calibration_selective_error: float

    def validate(self) -> None:
        """Validate one fitted reference without accepting silent shape drift."""

        mean = np.asarray(self.healthy_mean, dtype=float)
        scale = np.asarray(self.healthy_scale, dtype=float)
        null = np.asarray(self.calibration_null_scores, dtype=float)
        if mean.ndim != 1 or mean.size < 1 or scale.shape != mean.shape:
            raise ValueError("healthy reference mean/scale must be aligned 1-D vectors")
        if not np.all(np.isfinite(mean)) or not np.all(np.isfinite(scale)):
            raise ValueError("healthy reference vectors must be finite")
        if np.any(scale <= 0.0):
            raise ValueError("healthy reference scale must be positive")
        if set(self.fault_centroids) != set(FAULT_SOURCES):
            raise ValueError("fault centroids must cover all three known fault sources")
        if any(np.asarray(value).shape != mean.shape for value in self.fault_centroids.values()):
            raise ValueError("fault centroids must share the healthy-vector shape")
        if null.ndim != 1 or null.size < 1 or not np.all(np.isfinite(null)):
            raise ValueError("calibration null scores must be a finite non-empty vector")
        if not np.isfinite(self.detect_threshold) or self.detect_threshold <= 0.0:
            raise ValueError("detect_threshold must be finite and positive")
        if not np.isfinite(self.abstain_margin_threshold):
            raise ValueError("abstain_margin_threshold must be finite")
        for name, value in {
            "calibration_selective_coverage": self.calibration_selective_coverage,
            "calibration_selective_error": self.calibration_selective_error,
        }.items():
            if not 0.0 <= value <= 1.0:
                raise ValueError(f"{name} must lie in [0, 1]")


@dataclass(frozen=True)
class PrototypeDecision:
    """One pilot-only held-decision classification before controller translation."""

    score: float
    detected: bool
    predicted_source: str
    margin: float | None
    abstained: bool


def parse_args() -> argparse.Namespace:
    """Parse the portable bounded noisy-information command line."""

    defaults = BoundedNoisyInformationSpec()
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--output-dir",
        type=Path,
        default=Path("results/bounded_noisy_information_review"),
    )
    parser.add_argument(
        "--calibration-seeds", type=int, default=defaults.calibration_seeds
    )
    parser.add_argument(
        "--evaluation-seeds", type=int, default=defaults.evaluation_seeds
    )
    parser.add_argument("--seed", type=int, default=defaults.base_seed)
    parser.add_argument(
        "--representative-seed", type=int, default=defaults.representative_seed
    )
    parser.add_argument("--workers", type=int, default=8)
    parser.add_argument("--point-count", type=int, default=defaults.point_count)
    parser.add_argument(
        "--simulation-timestep-s",
        type=float,
        default=defaults.simulation_timestep_s,
    )
    return parser.parse_args()


def spec_from_args(args: argparse.Namespace) -> BoundedNoisyInformationSpec:
    """Build and validate a review specification from CLI values."""

    spec = BoundedNoisyInformationSpec(
        calibration_seeds=int(args.calibration_seeds),
        evaluation_seeds=int(args.evaluation_seeds),
        base_seed=int(args.seed),
        representative_seed=int(args.representative_seed),
        point_count=int(args.point_count),
        simulation_timestep_s=float(args.simulation_timestep_s),
    )
    spec.validate()
    if int(args.workers) < 1:
        raise ValueError("workers must be at least one")
    return spec


def _distance_margin(distances: dict[str, float]) -> tuple[str, float]:
    """Return nearest prototype and normalized first-vs-second distance margin."""

    if set(distances) != set(FAULT_SOURCES):
        raise ValueError("distances must cover every fault source")
    ordered = sorted(distances.items(), key=lambda item: (item[1], item[0]))
    predicted, first = ordered[0]
    second = ordered[1][1]
    denominator = max(second, 1.0e-12)
    margin = float(np.clip((second - first) / denominator, 0.0, 1.0))
    return predicted, margin


def _prototype_distances(
    vector: np.ndarray, reference: SelectivePrototypeReference
) -> dict[str, float]:
    """Return Euclidean distances to standardized suite-specific prototypes."""

    standardized = (
        np.asarray(vector, dtype=float) - reference.healthy_mean
    ) / reference.healthy_scale
    return {
        source: float(np.linalg.norm(standardized - centroid))
        for source, centroid in reference.fault_centroids.items()
    }


def _select_abstain_margin(
    margins: np.ndarray, correct: np.ndarray, *, error_ceiling: float
) -> tuple[float, float, float]:
    """Choose maximum calibration coverage at the selective-error ceiling."""

    values = np.asarray(margins, dtype=float)
    is_correct = np.asarray(correct, dtype=bool)
    if values.ndim != 1 or values.size < 1 or is_correct.shape != values.shape:
        raise ValueError("margins/correct must be aligned non-empty vectors")
    if not np.all(np.isfinite(values)) or np.any(values < 0.0):
        raise ValueError("classification margins must be finite and non-negative")
    candidates = np.unique(np.concatenate(([0.0], values)))
    selected: tuple[float, float, float] | None = None
    for threshold in candidates:
        accepted = values >= threshold
        coverage = float(np.mean(accepted))
        error = float(np.mean(~is_correct[accepted])) if np.any(accepted) else 0.0
        if error <= error_ceiling and (
            selected is None
            or coverage > selected[1]
            or (math.isclose(coverage, selected[1]) and threshold < selected[0])
        ):
            selected = (float(threshold), coverage, error)
    if selected is None:
        threshold = float(np.nextafter(np.max(values), np.inf))
        return threshold, 0.0, 0.0
    return selected


def fit_selective_reference(
    samples: dict[str, np.ndarray], spec: BoundedNoisyInformationSpec
) -> SelectivePrototypeReference:
    """Fit healthy detection and LOO prototype-margin abstention on calibration only."""

    spec.validate()
    if set(samples) != set(CANONICAL_SOURCES):
        raise ValueError("samples must contain healthy plus all three fault sources")
    healthy = np.asarray(samples["healthy"], dtype=float)
    if (
        healthy.ndim != 2
        or healthy.shape[0] < spec.minimum_calibration_size
        or healthy.shape[1] < 1
        or not np.all(np.isfinite(healthy))
    ):
        raise ValueError(
            "healthy calibration samples must be finite [N,D] with a resolved tail"
        )
    mean = healthy.mean(axis=0)
    std = healthy.std(axis=0)
    scale = np.maximum(std, 1.0e-6 + 1.0e-6 * np.abs(mean))
    loo_scores = np.empty(healthy.shape[0], dtype=float)
    for index in range(healthy.shape[0]):
        others = np.delete(healthy, index, axis=0)
        loo_mean = others.mean(axis=0)
        loo_std = others.std(axis=0)
        loo_scale = np.maximum(
            loo_std, 1.0e-6 + 1.0e-6 * np.abs(loo_mean)
        )
        loo_scores[index] = coefficient_reference_distance(
            healthy[index], loo_mean, loo_scale
        )
    threshold = float(
        max(
            np.quantile(
                loo_scores,
                1.0 - spec.healthy_false_alarm_rate,
                method="higher",
            ),
            1.0e-12,
        )
    )
    standardized_faults: dict[str, np.ndarray] = {}
    centroids: dict[str, np.ndarray] = {}
    for source in FAULT_SOURCES:
        values = np.asarray(samples[source], dtype=float)
        if (
            values.ndim != 2
            or values.shape != healthy.shape
            or not np.all(np.isfinite(values))
        ):
            raise ValueError(
                f"{source} calibration samples must match healthy shape {healthy.shape}"
            )
        standardized_faults[source] = (values - mean) / scale
        centroids[source] = standardized_faults[source].mean(axis=0)

    margins: list[float] = []
    correct: list[bool] = []
    for source in FAULT_SOURCES:
        values = standardized_faults[source]
        for index, vector in enumerate(values):
            own_others = np.delete(values, index, axis=0)
            if own_others.shape[0] < 1:
                raise ValueError("prototype calibration needs at least two fault samples")
            loo_centroids = dict(centroids)
            loo_centroids[source] = own_others.mean(axis=0)
            distances = {
                name: float(np.linalg.norm(vector - centroid))
                for name, centroid in loo_centroids.items()
            }
            predicted, margin = _distance_margin(distances)
            margins.append(margin)
            correct.append(predicted == source)
    abstain_threshold, coverage, selective_error = _select_abstain_margin(
        np.asarray(margins),
        np.asarray(correct),
        error_ceiling=spec.selective_error_ceiling,
    )
    reference = SelectivePrototypeReference(
        healthy_mean=mean,
        healthy_scale=scale,
        detect_threshold=threshold,
        fault_centroids=centroids,
        abstain_margin_threshold=abstain_threshold,
        calibration_null_scores=loo_scores,
        calibration_selective_coverage=coverage,
        calibration_selective_error=selective_error,
    )
    reference.validate()
    return reference


def classify_vector(
    vector: np.ndarray, reference: SelectivePrototypeReference
) -> PrototypeDecision:
    """Classify one vector with separate healthy detection and type abstention."""

    reference.validate()
    score = coefficient_reference_distance(
        vector, reference.healthy_mean, reference.healthy_scale
    )
    if score <= reference.detect_threshold:
        return PrototypeDecision(
            score=float(score),
            detected=False,
            predicted_source="healthy",
            margin=None,
            abstained=False,
        )
    predicted, margin = _distance_margin(_prototype_distances(vector, reference))
    return PrototypeDecision(
        score=float(score),
        detected=True,
        predicted_source=predicted,
        margin=margin,
        abstained=bool(margin < reference.abstain_margin_threshold),
    )


def action_gate_state(true_source: str, decision: PrototypeDecision) -> str:
    """Map one held decision to a transparent recovery-action gate category."""

    predicted = decision.predicted_source
    actionable = decision.detected and not decision.abstained and predicted in ACTION_SOURCES
    if actionable:
        return "correct_actionable" if predicted == true_source else "false_actionable"
    if true_source in ACTION_SOURCES:
        return "withheld_actionable_fault"
    if decision.abstained:
        return "type_abstained_no_action"
    return "correct_no_action" if predicted == true_source else "false_nonaction_call"


class SelectivePrototypeEstimator(DiagnosisEstimator):
    """Translate one pilot prototype decision into the schema-D output contract."""

    def __init__(
        self,
        reference: SelectivePrototypeReference,
        *,
        suite: str,
        window_steps: int,
        probe_frequency_hz: float,
    ) -> None:
        """Bind one suite reference and the canonical synchronous extractor."""

        if suite not in DEPLOYABLE_SUITES:
            raise ValueError(f"suite must be one of {DEPLOYABLE_SUITES}")
        self.reference = reference
        self.suite = suite
        self.extractor = WindowFeatureExtractor(
            window_steps=window_steps, probe_frequency_hz=probe_frequency_hz
        )
        self.calls = 0
        self.last_decision: PrototypeDecision | None = None

    def reset(self) -> None:
        """Reset the one-rollout diagnostic state."""

        self.calls = 0
        self.last_decision = None

    def update(
        self,
        step_index: int,
        decision_time_s: float,
        window: ObservedRecord | None,
    ) -> EstimatorOutput:
        """Evaluate one delivered window without reading labels or privileged state."""

        if window is None:
            raise ValueError("scheduled prototype decision requires a delivered window")
        if window.suite != self.suite:
            raise ValueError("prototype estimator received the wrong suite")
        vector = synchronous_coefficient_vector(window, self.extractor)
        decision = classify_vector(vector, self.reference)
        self.calls += 1
        self.last_decision = decision
        probabilities = np.zeros(N_SOURCE_CLASSES, dtype=float)
        probabilities[SOURCE_CLASS_ORDER.index(decision.predicted_source)] = 1.0
        location = -1
        severity = 0.0
        uncertainty = float("inf")
        if not decision.abstained:
            if decision.predicted_source == "structure":
                location, severity, uncertainty = 1, 0.50, 0.0
            elif decision.predicted_source == "actuator":
                location, severity, uncertainty = 1, 0.70, 0.0
            elif decision.predicted_source == "sensor":
                location, severity, uncertainty = 0, 0.05, 0.0
        output = EstimatorOutput(
            step=step_index,
            decision_time_s=decision_time_s,
            p_class=probabilities,
            unknown_score=decision.score,
            abstain_decision=decision.abstained,
            location_out=location,
            severity_out=severity,
            severity_uncertainty=uncertainty,
            detection_time_s=(
                decision_time_s if decision.detected else float("nan")
            ),
        )
        output.validate()
        return output


class _CaptureBoundedPolicy:
    """Run the bounded nominal controller and capture its exact decision window."""

    def __init__(self, spec: BoundedTaskContactSpec) -> None:
        """Bind the nominal controller and exact first held-decision step."""

        self.controller = ObservedJointPDController(
            spec.task_profile(), spec.controller_config()
        )
        self.capture_step = spec.first_decision_step
        self.window: ObservedRecord | None = None

    def __call__(
        self,
        step_index: int,
        decision_time_s: float,
        available: ObservedRecord | None,
    ) -> np.ndarray:
        """Capture the causal window before returning the matched nominal command."""

        if step_index == self.capture_step:
            if available is None:
                raise RuntimeError("the scheduled decision has no delivered history")
            self.window = available
        return self.controller(step_index, decision_time_s, available)


_VECTOR_CONTEXT: dict[str, Any] = {}


def _initialize_vector_worker(spec: BoundedNoisyInformationSpec) -> None:
    """Initialize one vector worker with immutable review settings."""

    global _VECTOR_CONTEXT
    mechanics = spec.mechanics_spec()
    _VECTOR_CONTEXT = {
        "spec": spec,
        "mechanics": mechanics,
        "faults": fault_specs(mechanics.onset_index),
        "extractor": WindowFeatureExtractor(
            window_steps=mechanics.window_steps,
            probe_frequency_hz=mechanics.diagnostic_tip_load_frequency_hz,
        ),
    }


def _collect_seed_vectors(
    task: tuple[str, str, int]
) -> tuple[str, str, int, dict[str, np.ndarray], bool, int]:
    """Run one noisy feedback history and return its exactly matched C1/S vectors."""

    split, source, sensor_seed = task
    context = _VECTOR_CONTEXT
    if not context:
        raise RuntimeError("bounded vector worker was not initialized")
    spec: BoundedNoisyInformationSpec = context["spec"]
    mechanics: BoundedTaskContactSpec = context["mechanics"]
    faults = context["faults"]
    physical_fault = faults[source] if source in PHYSICAL_SOURCES else faults["healthy"]
    sensor_fault = faults["sensor"] if source == "sensor" else None
    pair_id = f"bounded-information-{split}-{source}-{sensor_seed}"
    plant = CablePlant(
        cable_config(mechanics, spec.selected_plane_z_m),
        point_count=spec.point_count,
        simulation_timestep_s=spec.simulation_timestep_s,
        fault=physical_fault,
    )
    sensors = OnlineSensorSession(
        "S",
        pair_id=pair_id,
        sensor_seed=sensor_seed,
        control_dt_s=mechanics.control_dt_s,
        config=SensorConfig(),
        fault=sensor_fault,
        run_id=f"{pair_id}-S",
        config_hash="dev-bounded-noisy-information-review",
        split=split,
    )
    policy = _CaptureBoundedPolicy(mechanics)
    rollout = run_online_rollout(
        plant,
        sensors,
        n_steps=mechanics.first_decision_step + 1,
        history_steps=mechanics.window_steps,
        command_policy=policy,
        reference_fn=mechanics.task_profile().task_reference,
        temperature_fn=lambda _index, time_s: 25.0
        + mechanics.thermal_rate_c_s * time_s,
    )
    if policy.window is None:
        raise RuntimeError("scheduled causal window was not captured")
    vectors: dict[str, np.ndarray] = {}
    for suite in DEPLOYABLE_SUITES:
        window = project_observed_suite(policy.window, suite)
        vectors[suite] = synchronous_coefficient_vector(
            window, context["extractor"]
        )
    predecision = slice(0, mechanics.first_decision_step)
    any_safety = bool(np.any(rollout.plant.safety_flag[predecision]))
    contact_steps = int(
        np.count_nonzero(rollout.plant.contact_state[predecision, 1] == 1.0)
    )
    return split, source, sensor_seed, vectors, any_safety, contact_steps


def collect_vectors(
    spec: BoundedNoisyInformationSpec, *, workers: int
) -> tuple[
    dict[str, dict[str, dict[str, list[np.ndarray]]]],
    list[dict[str, Any]],
]:
    """Collect calibration/evaluation vectors from the real noisy feedback path."""

    spec.validate()
    output = {
        suite: {
            split: {source: [] for source in CANONICAL_SOURCES}
            for split in ("calibration", "evaluation")
        }
        for suite in DEPLOYABLE_SUITES
    }
    seed_groups = {
        "calibration": spec.calibration_seed_values,
        "evaluation": spec.evaluation_seed_values,
    }
    tasks = [
        (split, source, seed)
        for split, seeds in seed_groups.items()
        for source in CANONICAL_SOURCES
        for seed in seeds
    ]
    predecision_rows: list[dict[str, Any]] = []
    if workers == 1:
        _initialize_vector_worker(spec)
        results = map(_collect_seed_vectors, tasks)
        for split, source, seed, vectors, any_safety, contact_steps in results:
            for suite, vector in vectors.items():
                output[suite][split][source].append(vector)
            predecision_rows.append(
                {
                    "split": split,
                    "source": source,
                    "sensor_seed": seed,
                    "any_safety_flag": any_safety,
                    "contact_active_steps": contact_steps,
                }
            )
    else:
        with concurrent.futures.ProcessPoolExecutor(
            max_workers=workers,
            initializer=_initialize_vector_worker,
            initargs=(spec,),
        ) as executor:
            for split, source, seed, vectors, any_safety, contact_steps in executor.map(
                _collect_seed_vectors, tasks
            ):
                for suite, vector in vectors.items():
                    output[suite][split][source].append(vector)
                predecision_rows.append(
                    {
                        "split": split,
                        "source": source,
                        "sensor_seed": seed,
                        "any_safety_flag": any_safety,
                        "contact_active_steps": contact_steps,
                    }
                )
    predecision_rows.sort(
        key=lambda row: (row["split"], row["source"], row["sensor_seed"])
    )
    return output, predecision_rows


def _decision_row(
    suite: str,
    source: str,
    sensor_seed: int,
    vector: np.ndarray,
    reference: SelectivePrototypeReference,
) -> dict[str, Any]:
    """Return one held-out decision row with explicit action-gate state."""

    decision = classify_vector(vector, reference)
    headline = "abstain" if decision.abstained else decision.predicted_source
    return {
        "suite": suite,
        "source": source,
        "sensor_seed": sensor_seed,
        "score": decision.score,
        "detected": decision.detected,
        "predicted_source": decision.predicted_source,
        "prototype_margin": decision.margin,
        "abstained": decision.abstained,
        "headline_prediction": headline,
        "correct": bool(headline == source),
        "action_gate_state": action_gate_state(source, decision),
    }


def evaluate_references(
    spec: BoundedNoisyInformationSpec,
    vectors: dict[str, dict[str, dict[str, list[np.ndarray]]]],
) -> tuple[
    dict[str, SelectivePrototypeReference],
    list[dict[str, Any]],
    list[dict[str, Any]],
]:
    """Fit suite references and evaluate every held-out exact-decision vector."""

    references: dict[str, SelectivePrototypeReference] = {}
    decision_rows: list[dict[str, Any]] = []
    information_rows: list[dict[str, Any]] = []
    for suite in DEPLOYABLE_SUITES:
        calibration = {
            source: np.stack(vectors[suite]["calibration"][source])
            for source in CANONICAL_SOURCES
        }
        reference = fit_selective_reference(calibration, spec)
        references[suite] = reference
        for source in CANONICAL_SOURCES:
            for seed, vector in zip(
                spec.evaluation_seed_values,
                vectors[suite]["evaluation"][source],
                strict=True,
            ):
                decision_rows.append(
                    _decision_row(suite, source, seed, vector, reference)
                )
        suite_rows = [row for row in decision_rows if row["suite"] == suite]
        y_true = np.asarray(
            [SOURCE_CLASS_ORDER.index(row["source"]) for row in suite_rows], dtype=int
        )
        y_pred = np.asarray(
            [
                ABSTAIN
                if row["abstained"]
                else SOURCE_CLASS_ORDER.index(row["predicted_source"])
                for row in suite_rows
            ],
            dtype=int,
        )
        recalls = per_class_recall(y_true, y_pred)
        healthy_rows = [row for row in suite_rows if row["source"] == "healthy"]
        fault_rows = [row for row in suite_rows if row["source"] in FAULT_SOURCES]
        accepted_fault_rows = [
            row for row in fault_rows if row["detected"] and not row["abstained"]
        ]
        per_fault: dict[str, dict[str, float]] = {}
        for source in FAULT_SOURCES:
            rows = [row for row in fault_rows if row["source"] == source]
            per_fault[source] = {
                "detection_rate": float(np.mean([row["detected"] for row in rows])),
                "abstain_rate": float(np.mean([row["abstained"] for row in rows])),
                "correct_confident_rate": float(
                    np.mean(
                        [
                            row["detected"]
                            and not row["abstained"]
                            and row["predicted_source"] == source
                            for row in rows
                        ]
                    )
                ),
                "false_actionable_rate": float(
                    np.mean([row["action_gate_state"] == "false_actionable" for row in rows])
                ),
            }
        false_alarm = float(np.mean([row["detected"] for row in healthy_rows]))
        healthy_false_actionable = float(
            np.mean(
                [row["action_gate_state"] == "false_actionable" for row in healthy_rows]
            )
        )
        selective_accuracy = (
            float(np.mean([row["correct"] for row in accepted_fault_rows]))
            if accepted_fault_rows
            else 0.0
        )
        row: dict[str, Any] = {
            "suite": suite,
            "calibration_seeds": spec.calibration_seeds,
            "evaluation_seeds": spec.evaluation_seeds,
            "detect_quantile": 1.0 - spec.healthy_false_alarm_rate,
            "detect_threshold": reference.detect_threshold,
            "calibration_null_max": float(reference.calibration_null_scores.max()),
            "threshold_below_calibration_max": bool(
                reference.detect_threshold < reference.calibration_null_scores.max()
            ),
            "abstain_margin_threshold": reference.abstain_margin_threshold,
            "calibration_selective_coverage": (
                reference.calibration_selective_coverage
            ),
            "calibration_selective_error": reference.calibration_selective_error,
            "heldout_macro_f1": macro_f1(y_true, y_pred),
            "heldout_balanced_accuracy": float(np.mean(list(recalls.values()))),
            "healthy_false_alarm_rate": false_alarm,
            "healthy_false_actionable_rate": healthy_false_actionable,
            "maximum_source_false_actionable_rate": float(
                max(
                    healthy_false_actionable,
                    *(values["false_actionable_rate"] for values in per_fault.values()),
                )
            ),
            "minimum_fault_detection_rate": float(
                min(values["detection_rate"] for values in per_fault.values())
            ),
            "macro_fault_correct_confident_rate": float(
                np.mean(
                    [values["correct_confident_rate"] for values in per_fault.values()]
                )
            ),
            "minimum_actionable_fault_correct_action_rate": float(
                min(
                    per_fault[source]["correct_confident_rate"]
                    for source in ACTION_SOURCES
                )
            ),
            "known_fault_abstain_rate": float(
                np.mean([row["abstained"] for row in fault_rows])
            ),
            "known_fault_selective_accuracy": selective_accuracy,
        }
        for source in CANONICAL_SOURCES:
            row[f"recall_{source}"] = recalls[source]
        for source in FAULT_SOURCES:
            for metric, value in per_fault[source].items():
                row[f"{source}_{metric}"] = value
        row["information_gate_pass"] = bool(
            row["threshold_below_calibration_max"]
            and false_alarm <= spec.healthy_false_alarm_rate
            and row["minimum_fault_detection_rate"]
            >= spec.minimum_fault_detection_rate
            and row["macro_fault_correct_confident_rate"]
            >= spec.minimum_fault_correct_confident_rate
        )
        row["action_gate_pass"] = bool(
            row["maximum_source_false_actionable_rate"]
            <= spec.maximum_healthy_false_actionable_rate
            and row["minimum_actionable_fault_correct_action_rate"]
            >= spec.minimum_fault_correct_confident_rate
        )
        information_rows.append(row)
    decision_rows.sort(
        key=lambda row: (row["suite"], row["source"], row["sensor_seed"])
    )
    information_rows.sort(key=lambda row: row["suite"])
    return references, information_rows, decision_rows


def _hash_arrays(named_arrays: list[tuple[str, np.ndarray]]) -> str:
    """Return a stable digest over named array shapes, dtypes, and exact bytes."""

    digest = hashlib.sha256()
    for name, values in named_arrays:
        array = np.ascontiguousarray(values)
        digest.update(name.encode("utf-8"))
        digest.update(str(array.shape).encode("ascii"))
        digest.update(str(array.dtype).encode("ascii"))
        digest.update(array.tobytes())
    return digest.hexdigest()


def _online_case(
    task: tuple[
        BoundedNoisyInformationSpec,
        str,
        str,
        SelectivePrototypeReference,
    ]
) -> dict[str, Any]:
    """Run one representative held decision through the full bounded causal seam."""

    spec, source, suite, reference = task
    mechanics = spec.mechanics_spec()
    faults = fault_specs(mechanics.onset_index)
    physical_fault = faults[source] if source in PHYSICAL_SOURCES else faults["healthy"]
    sensor_fault = faults["sensor"] if source == "sensor" else None
    pair_id = f"bounded-information-evaluation-{source}-{spec.representative_seed}"
    plant = CablePlant(
        cable_config(mechanics, spec.selected_plane_z_m),
        point_count=spec.point_count,
        simulation_timestep_s=spec.simulation_timestep_s,
        fault=physical_fault,
    )
    sensors = OnlineSensorSession(
        suite,
        pair_id=pair_id,
        sensor_seed=spec.representative_seed,
        control_dt_s=mechanics.control_dt_s,
        config=SensorConfig(),
        fault=sensor_fault,
        run_id=f"{pair_id}-{suite}",
        config_hash="dev-bounded-noisy-information-review",
        split="evaluation",
    )
    inner = SelectivePrototypeEstimator(
        reference,
        suite=suite,
        window_steps=mechanics.window_steps,
        probe_frequency_hz=mechanics.diagnostic_tip_load_frequency_hz,
    )
    held = SingleDecisionHoldEstimator(
        inner, first_decision_step=mechanics.first_decision_step
    )
    profile = mechanics.task_profile()
    policy = EstimatorRecoveryTaskPolicy(
        ObservedJointPDController(profile, mechanics.controller_config()),
        held,
        suite=suite,
        run_id=f"{pair_id}-{suite}",
        stride=mechanics.stride,
    )
    rollout = run_online_rollout(
        plant,
        sensors,
        n_steps=mechanics.n_steps,
        history_steps=mechanics.window_steps,
        command_policy=policy,
        reference_fn=profile.task_reference,
        temperature_fn=lambda _index, time_s: 25.0
        + mechanics.thermal_rate_c_s * time_s,
    )
    if inner.last_decision is None:
        raise RuntimeError("representative rollout never reached the held decision")
    decision = inner.last_decision
    active = np.asarray(rollout.plant.contact_state[:, 1] == 1.0, dtype=bool)
    force = np.asarray(rollout.plant.contact_state[:, 0], dtype=float)
    active_indices = np.flatnonzero(active)
    nominal = np.stack(policy.nominal_commands)
    applied = np.stack(policy.commands)
    changed = np.any(~np.isclose(nominal, applied, rtol=0.0, atol=1.0e-12), axis=1)
    predecision = slice(0, mechanics.first_decision_step)
    plant_hash = _hash_arrays(
        [
            ("q_true", rollout.plant.q_true[predecision]),
            ("qd_true", rollout.plant.qd_true[predecision]),
            ("tau_cmd", rollout.plant.tau_cmd[predecision]),
        ]
    )
    shared_names = ("q_obs", "qd_obs", "tau_cmd", "current_proxy_obs", "imu_obs")
    observation_hash = _hash_arrays(
        [
            (f"values/{name}", rollout.observations.values[name][predecision])
            for name in shared_names
        ]
        + [
            (f"mask/{name}", rollout.observations.valid_mask[name][predecision])
            for name in shared_names
        ]
    )
    flag_counts = {
        name: int(np.count_nonzero(rollout.plant.safety_flag[:, index]))
        for index, name in enumerate(SAFETY_FLAG_FIELDS)
    }
    row: dict[str, Any] = {
        "source": source,
        "suite": suite,
        "sensor_seed": spec.representative_seed,
        "pair_id": pair_id,
        "first_decision_step": mechanics.first_decision_step,
        "classification_evaluations": held.classification_evaluations,
        "held_score": decision.score,
        "held_detected": decision.detected,
        "held_predicted_source": decision.predicted_source,
        "held_prototype_margin": decision.margin,
        "held_abstained": decision.abstained,
        "action_gate_state": action_gate_state(source, decision),
        "command_changed_steps": int(np.count_nonzero(changed)),
        "command_changed_before_decision": bool(np.any(changed[predecision])),
        "contact_active_steps": int(active_indices.size),
        "contact_episode_count": count_contact_episodes(active),
        "first_contact_time_s": (
            None
            if not active_indices.size
            else float(rollout.plant.t_s[active_indices[0]])
        ),
        "last_contact_time_s": (
            None
            if not active_indices.size
            else float(rollout.plant.t_s[active_indices[-1]])
        ),
        "peak_contact_force_n": float(np.max(force)),
        "tracking_integral_5s_m_s": j_5s(
            rollout.plant.t_s,
            rollout.plant.task_reference,
            rollout.plant.true_task_output,
            mechanics.fault_onset_s,
        ),
        "safety_incident_steps": int(
            np.count_nonzero(np.any(rollout.plant.safety_flag, axis=1))
        ),
        "any_safety_flag": bool(np.any(rollout.plant.safety_flag)),
        "predecision_plant_hash": plant_hash,
        "predecision_shared_observation_hash": observation_hash,
    }
    row.update({f"flag_steps_{name}": count for name, count in flag_counts.items()})
    return row


def run_representative_online(
    spec: BoundedNoisyInformationSpec,
    references: dict[str, SelectivePrototypeReference],
    *,
    workers: int,
) -> list[dict[str, Any]]:
    """Run one predeclared held-out seed per matched source/suite over six seconds."""

    tasks = [
        (spec, source, suite, references[suite])
        for source in CANONICAL_SOURCES
        for suite in DEPLOYABLE_SUITES
    ]
    if workers == 1:
        rows = [_online_case(task) for task in tasks]
    else:
        with concurrent.futures.ProcessPoolExecutor(max_workers=workers) as executor:
            rows = list(executor.map(_online_case, tasks))
    return sorted(rows, key=lambda row: (row["source"], row["suite"]))


def decide(
    spec: BoundedNoisyInformationSpec,
    information_rows: list[dict[str, Any]],
    decision_rows: list[dict[str, Any]],
    online_rows: list[dict[str, Any]],
    predecision_rows: list[dict[str, Any]],
) -> dict[str, Any]:
    """Keep information, action, and representative mechanics decisions separate."""

    s_information = next(row for row in information_rows if row["suite"] == "S")
    information_pass = bool(s_information["information_gate_pass"])
    action_pass = bool(s_information["action_gate_pass"])
    matched_predecision = all(
        next(
            row for row in online_rows if row["source"] == source and row["suite"] == "C1"
        )["predecision_plant_hash"]
        == next(
            row for row in online_rows if row["source"] == source and row["suite"] == "S"
        )["predecision_plant_hash"]
        and next(
            row for row in online_rows if row["source"] == source and row["suite"] == "C1"
        )["predecision_shared_observation_hash"]
        == next(
            row for row in online_rows if row["source"] == source and row["suite"] == "S"
        )["predecision_shared_observation_hash"]
        for source in CANONICAL_SOURCES
    )
    representative_safety = bool(
        len(online_rows) == len(CANONICAL_SOURCES) * len(DEPLOYABLE_SUITES)
        and all(not row["any_safety_flag"] for row in online_rows)
        and all(not row["command_changed_before_decision"] for row in online_rows)
        and all(row["classification_evaluations"] == 1 for row in online_rows)
    )
    predecision_clean = bool(
        predecision_rows
        and all(not row["any_safety_flag"] for row in predecision_rows)
        and all(row["contact_active_steps"] == 0 for row in predecision_rows)
    )
    false_actionable_counts = {
        suite: int(
            sum(
                row["action_gate_state"] == "false_actionable"
                for row in decision_rows
                if row["suite"] == suite
            )
        )
        for suite in DEPLOYABLE_SUITES
    }
    tracking_pairs: list[dict[str, Any]] = []
    for source in CANONICAL_SOURCES:
        c1 = next(
            row
            for row in online_rows
            if row["source"] == source and row["suite"] == "C1"
        )
        structural = next(
            row
            for row in online_rows
            if row["source"] == source and row["suite"] == "S"
        )
        suite_informed_action = bool(
            structural["action_gate_state"] == "correct_actionable"
            and c1["action_gate_state"] != "correct_actionable"
        )
        c1_j = float(c1["tracking_integral_5s_m_s"])
        s_j = float(structural["tracking_integral_5s_m_s"])
        s_benefits = bool(
            s_j < c1_j
            or int(structural["safety_incident_steps"])
            < int(c1["safety_incident_steps"])
        )
        tracking_pairs.append(
            {
                "source": source,
                "c1_action_gate_state": c1["action_gate_state"],
                "s_action_gate_state": structural["action_gate_state"],
                "suite_informed_action": suite_informed_action,
                "c1_tracking_integral_5s_m_s": c1_j,
                "s_tracking_integral_5s_m_s": s_j,
                "s_tracking_change_pct": float(100.0 * (c1_j - s_j) / c1_j),
                "c1_safety_incident_steps": int(c1["safety_incident_steps"]),
                "s_safety_incident_steps": int(structural["safety_incident_steps"]),
                "suite_informed_action_benefits_representative_outcome": (
                    s_benefits if suite_informed_action else None
                ),
            }
        )
    informative_tracking_pairs = [
        row for row in tracking_pairs if row["suite_informed_action"]
    ]
    control_sensitivity_pass = bool(
        informative_tracking_pairs
        and all(
            row["suite_informed_action_benefits_representative_outcome"]
            for row in informative_tracking_pairs
        )
    )
    if (
        information_pass
        and action_pass
        and representative_safety
        and matched_predecision
        and control_sensitivity_pass
    ):
        overall = "ADVANCE_BOUNDED_NOISY_HELD_DECISION_TO_VALIDATION_DESIGN_REVIEW"
    elif information_pass:
        overall = (
            "ADVANCE_INFORMATION_REFERENCE_LIFECYCLE_ONLY_"
            "BLOCK_RECOVERY_CONTROL_PROFILE"
        )
    else:
        overall = "BLOCK_BOUNDED_NOISY_HELD_DECISION_REVIEW"
    return {
        "information_gate_pass": information_pass,
        "action_gate_pass": action_pass,
        "representative_full_horizon_safety_pass": representative_safety,
        "representative_control_sensitivity_pass": control_sensitivity_pass,
        "matched_predecision_crn_pass": matched_predecision,
        "all_calibration_and_evaluation_predecision_histories_clean": predecision_clean,
        "false_actionable_counts_by_suite": false_actionable_counts,
        "representative_tracking_pairs": tracking_pairs,
        "overall_decision": overall,
        "decision_boundary": (
            "the information/reference lifecycle may advance while the recovery-control "
            "profile remains blocked; one-hot prototype probabilities, the representative "
            "one-seed online continuation, and all development task/contact/controller "
            "values remain unfrozen"
        ),
    }


def run(spec: BoundedNoisyInformationSpec, *, workers: int) -> dict[str, Any]:
    """Execute the complete bounded noisy-information/reference-lifecycle review."""

    spec.validate()
    mechanics = spec.mechanics_spec()
    print("Collecting noisy bounded-feedback decision windows ...", flush=True)
    vectors, predecision_rows = collect_vectors(spec, workers=workers)
    print("Fitting suite references and evaluating held-out decisions ...", flush=True)
    references, information_rows, decision_rows = evaluate_references(spec, vectors)
    print("Running representative six-second matched online audits ...", flush=True)
    online_rows = run_representative_online(spec, references, workers=workers)
    decision = decide(
        spec, information_rows, decision_rows, online_rows, predecision_rows
    )
    return {
        "artifact_status": "development_only_config_unfrozen",
        "review_spec": asdict(spec),
        "bounded_mechanics_spec": asdict(mechanics),
        "causal_schedule": {
            "first_decision_step": mechanics.first_decision_step,
            "first_decision_time_s": mechanics.first_decision_time_s,
            "movement_start_s": mechanics.movement_start_s,
            "duration_s": mechanics.duration_s,
        },
        "calibration_role": {
            "sensor_seeds": list(spec.calibration_seed_values),
            "purpose": (
                "fit suite-specific healthy references, 95th-percentile detection "
                "thresholds, fault prototypes, and LOO selective-margin thresholds"
            ),
        },
        "evaluation_role": {
            "sensor_seeds": list(spec.evaluation_seed_values),
            "purpose": (
                "held-out exact-decision false alarms, per-fault detection/attribution, "
                "abstention, and recovery-action gate behavior"
            ),
        },
        "probability_boundary": (
            "accepted prototype calls use one-hot mechanism probabilities; probability "
            "calibration and validation-frozen class/selective/OOD thresholds remain open"
        ),
        "control_boundary": (
            "the full-horizon online continuation uses one predeclared held-out seed per "
            "source/suite and is a lifecycle/mechanics audit, not an evaluation-sized "
            "tracking-recovery comparison"
        ),
        "information_rows": information_rows,
        "heldout_decision_rows": decision_rows,
        "representative_online_rows": online_rows,
        "predecision_history_summary": {
            "rows": len(predecision_rows),
            "any_safety_rows": int(
                sum(row["any_safety_flag"] for row in predecision_rows)
            ),
            "any_contact_rows": int(
                sum(row["contact_active_steps"] > 0 for row in predecision_rows)
            ),
        },
        "decision": decision,
    }


def _jsonable(value: Any) -> Any:
    """Convert NumPy-rich containers into strict JSON-compatible values."""

    if isinstance(value, dict):
        return {str(key): _jsonable(item) for key, item in value.items()}
    if isinstance(value, (list, tuple)):
        return [_jsonable(item) for item in value]
    if isinstance(value, np.ndarray):
        return _jsonable(value.tolist())
    if isinstance(value, (np.integer,)):
        return int(value)
    if isinstance(value, (np.floating,)):
        return float(value)
    if isinstance(value, (np.bool_,)):
        return bool(value)
    return value


def write_csv(path: Path, rows: list[dict[str, Any]]) -> None:
    """Write stable rows with the first row's declared field order."""

    if not rows:
        raise ValueError("cannot write an empty CSV")
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(rows[0]))
        writer.writeheader()
        writer.writerows(rows)


def write_report(path: Path, summary: dict[str, Any]) -> None:
    """Write the human-readable split decision without merging evidence layers."""

    decision = summary["decision"]
    spec = summary["review_spec"]
    mechanics = summary["bounded_mechanics_spec"]
    schedule = summary["causal_schedule"]
    lines = [
        "# Bounded Noisy Held-Decision Information Review",
        "",
        f"**Decision:** `{decision['overall_decision']}`",
        "",
        (
            "This development review replaces fixed source-correct diagnoses with "
            "suite-specific noisy references at the exact first causal post-probe "
            "decision. Information, recovery-action gating, and the representative "
            "six-second mechanics audit are reported separately."
        ),
        "",
        "## Role and lifecycle contract",
        "",
        f"- Calibration seeds: {spec['calibration_seeds']} "
        f"({spec['base_seed']}-{spec['base_seed'] + spec['calibration_seeds'] - 1}).",
        f"- Held-out seeds: {spec['evaluation_seeds']} "
        f"({spec['base_seed'] + spec['calibration_seeds']}-"
        f"{spec['base_seed'] + spec['calibration_seeds'] + spec['evaluation_seeds'] - 1}).",
        f"- Held decision: step {schedule['first_decision_step']} "
        f"({schedule['first_decision_time_s']:.3f} s), before movement at "
        f"{schedule['movement_start_s']:.3f} s.",
        "- One classification is held for the remainder of each online rollout.",
        "- Accepted prototype calls use one-hot mechanism probabilities; calibrated "
        "probabilities and final selective/OOD thresholds remain open.",
        "",
        "## Held-out information and action-gate results",
        "",
        "| Suite | Macro-F1 | Healthy FA | Min fault detect | Macro correct-confident | Fault abstain | Selective accuracy | Healthy false-actionable | Information gate |",
        "|---|---:|---:|---:|---:|---:|---:|---:|---|",
    ]
    for row in summary["information_rows"]:
        lines.append(
            f"| {row['suite']} | {row['heldout_macro_f1']:.3f} | "
            f"{row['healthy_false_alarm_rate']:.3f} | "
            f"{row['minimum_fault_detection_rate']:.3f} | "
            f"{row['macro_fault_correct_confident_rate']:.3f} | "
            f"{row['known_fault_abstain_rate']:.3f} | "
            f"{row['known_fault_selective_accuracy']:.3f} | "
            f"{row['healthy_false_actionable_rate']:.3f} | "
            f"{'PASS' if row['information_gate_pass'] else 'BLOCK'} |"
        )
    lines.extend(
        [
            "",
            "## Representative full-horizon online rows",
            "",
            "| Source | Suite | Held call | Abstain | Action gate | Contact episodes | Peak force (N) | J5s (m s) | Safety steps |",
            "|---|---|---|---|---|---:|---:|---:|---:|",
        ]
    )
    for row in summary["representative_online_rows"]:
        lines.append(
            f"| {row['source']} | {row['suite']} | "
            f"{row['held_predicted_source']} | {row['held_abstained']} | "
            f"{row['action_gate_state']} | {row['contact_episode_count']} | "
            f"{row['peak_contact_force_n']:.3f} | "
            f"{row['tracking_integral_5s_m_s']:.4f} | "
            f"{row['safety_incident_steps']} |"
        )
    lines.extend(
        [
            "",
            "## Separate gate verdicts",
            "",
            f"- Information gate: **{'PASS' if decision['information_gate_pass'] else 'BLOCK'}**.",
            f"- Held-out action gate: **{'PASS' if decision['action_gate_pass'] else 'BLOCK'}**.",
            f"- Representative full-horizon A1 safety: **{'PASS' if decision['representative_full_horizon_safety_pass'] else 'BLOCK'}**.",
            f"- Representative control sensitivity: **{'PASS' if decision['representative_control_sensitivity_pass'] else 'BLOCK'}**.",
            f"- Matched C1/S pre-decision CRN histories: **{'PASS' if decision['matched_predecision_crn_pass'] else 'BLOCK'}**.",
            "",
            "### Representative paired tracking readout",
            "",
            "| Source | C1 gate | S gate | C1 J5s | S J5s | S change | Suite-informed action benefit |",
            "|---|---|---|---:|---:|---:|---|",
        ]
    )
    for row in decision["representative_tracking_pairs"]:
        benefit = row["suite_informed_action_benefits_representative_outcome"]
        lines.append(
            f"| {row['source']} | {row['c1_action_gate_state']} | "
            f"{row['s_action_gate_state']} | "
            f"{row['c1_tracking_integral_5s_m_s']:.4f} | "
            f"{row['s_tracking_integral_5s_m_s']:.4f} | "
            f"{row['s_tracking_change_pct']:.1f}% | "
            f"{'n/a' if benefit is None else ('yes' if benefit else 'no')} |"
        )
    lines.extend(
        [
            "",
            "## Interpretation boundary",
            "",
            (
                "The information/reference lifecycle advances, but the current recovery-"
                "control profile remains blocked if the suite-informed action does not "
                "improve this representative outcome. This is not the confirmatory C1-vs-S "
                "result: the prototype probabilities are not calibrated, the full-horizon "
                "continuation uses one held-out seed per source/suite, no learned attribution "
                "or RMA model is present, and no paired uncertainty interval is computed for "
                "tracking or safety. The task/contact/controller profile, sensor constants, "
                "severity/onset grids, W/stride, thresholds, and config remain unfrozen."
            ),
        ]
    )
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text("\n".join(lines) + "\n", encoding="utf-8")


def main() -> int:
    """Run the review and write deterministic JSON/CSV/Markdown artifacts."""

    args = parse_args()
    spec = spec_from_args(args)
    summary = run(spec, workers=int(args.workers))
    args.output_dir.mkdir(parents=True, exist_ok=True)
    summary_path = args.output_dir / "summary.json"
    information_path = args.output_dir / "information_rows.csv"
    decisions_path = args.output_dir / "heldout_decision_rows.csv"
    online_path = args.output_dir / "representative_online_rows.csv"
    report_path = args.output_dir / "bounded_noisy_information_report.md"
    summary_path.write_text(
        json.dumps(_jsonable(summary), indent=2, allow_nan=False) + "\n",
        encoding="utf-8",
    )
    write_csv(information_path, summary["information_rows"])
    write_csv(decisions_path, summary["heldout_decision_rows"])
    write_csv(online_path, summary["representative_online_rows"])
    write_report(report_path, summary)
    print(f"Decision: {summary['decision']['overall_decision']}", flush=True)
    for output in (
        summary_path,
        information_path,
        decisions_path,
        online_path,
        report_path,
    ):
        print(f"Wrote {output}", flush=True)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
