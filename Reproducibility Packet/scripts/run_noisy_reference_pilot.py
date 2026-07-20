"""Pilot the synchronous feature on noisy deployable observations.

This development pilot follows the clean mechanics/detector screen with the test that
screen could not answer: whether the selected probe remains useful after the actual
sensor-pathology stack and a deployable healthy reference replace the privileged
fault-minus-healthy comparison.  It compares the matched C1 and S suites, sweeps the
candidate neighborhood and proposed W/stride values, and evaluates held-out sensor
seeds after fitting references and fault-shape centroids on disjoint calibration seeds.

The pilot deliberately does not freeze configuration, train the headline learned
attribution model, or claim a research result.  The nearest-centroid attribution score
is only a diagnostic-shape instrument for choosing a coherent reference/alignment
convention before the permanent estimator rung is built.
"""

from __future__ import annotations

import argparse
import concurrent.futures
import csv
import json
import math
from dataclasses import asdict, dataclass
from pathlib import Path
from typing import Any, Iterable

import numpy as np

from utils.cable_mechanics import CableModelConfig
from utils.cable_plant import CablePlant
from utils.estimator import (
    WindowFeatureExtractor,
    coefficient_reference_distance as coefficient_distance,
    synchronous_coefficient_vector,
)
from utils.schema_types import (
    CHANNEL_NAMES,
    FaultSpec,
    ObservedRecord,
    PrivilegedRecord,
    SUITE_CHANNELS,
)
from utils.sensor_model import SensorConfig, SensorModel


FAULT_CLASSES: tuple[str, ...] = ("structure", "actuator", "sensor")
DEPLOYABLE_SUITES: tuple[str, ...] = ("C1", "S")


@dataclass(frozen=True)
class CoefficientReference:
    """Healthy normalization, detection threshold, and fault-shape centroids."""

    healthy_mean: np.ndarray
    healthy_scale: np.ndarray
    detect_threshold: float
    fault_centroids: dict[str, np.ndarray]
    calibration_null_scores: np.ndarray


def parse_args() -> argparse.Namespace:
    """Parse portable pilot arguments."""

    parser = argparse.ArgumentParser(
        description="Run the noisy healthy-reference coefficient pilot."
    )
    parser.add_argument(
        "--output-dir",
        type=Path,
        default=Path("results/noisy_reference_pilot"),
        help="Project-relative output directory.",
    )
    parser.add_argument(
        "--task-torque-scales", type=float, nargs="+", default=[0.4, 0.5]
    )
    parser.add_argument(
        "--peak-loads-n", type=float, nargs="+", default=[0.025, 0.05]
    )
    parser.add_argument("--windows", type=int, nargs="+", default=[512, 640, 768])
    parser.add_argument("--strides", type=int, nargs="+", default=[4, 8, 16])
    parser.add_argument(
        "--onset-offset-steps", type=int, nargs="+", default=[0, 5, 11]
    )
    parser.add_argument("--base-onset-s", type=float, default=1.0)
    parser.add_argument("--frequency-hz", type=float, default=0.8)
    parser.add_argument("--ramp-period-fraction", type=float, default=0.125)
    parser.add_argument("--calibration-seeds", type=int, default=8)
    parser.add_argument("--evaluation-seeds", type=int, default=12)
    parser.add_argument("--seed", type=int, default=1000)
    parser.add_argument(
        "--workers",
        type=int,
        default=4,
        help="Independent sensor-seed worker processes (default: 4).",
    )
    parser.add_argument(
        "--thermal-ramp-c-per-window",
        type=float,
        default=3.0,
        help="Linear thermal excursion per 640-sample development window.",
    )
    parser.add_argument("--point-count", type=int, default=17)
    parser.add_argument("--simulation-timestep-s", type=float, default=1.0e-4)
    parser.add_argument(
        "--maximum-false-alarm-rate", type=float, default=0.05
    )
    parser.add_argument(
        "--minimum-fault-detection-rate", type=float, default=0.80
    )
    return parser.parse_args()


def validate_args(args: argparse.Namespace) -> None:
    """Fail loudly on an ill-formed pilot grid."""

    positive_lists = {
        "task_torque_scales": args.task_torque_scales,
        "peak_loads_n": args.peak_loads_n,
        "windows": args.windows,
        "strides": args.strides,
    }
    for name, values in positive_lists.items():
        if not values or any(not np.isfinite(value) or value <= 0 for value in values):
            raise ValueError(f"{name} must contain finite positive values")
    if not args.onset_offset_steps or any(value < 0 for value in args.onset_offset_steps):
        raise ValueError("onset offsets must contain non-negative step counts")
    if not np.isfinite(args.base_onset_s) or args.base_onset_s <= 0.0:
        raise ValueError("base_onset_s must be finite and positive")
    if not np.isfinite(args.frequency_hz) or args.frequency_hz <= 0.0:
        raise ValueError("frequency_hz must be finite and positive")
    if not 0.0 <= args.ramp_period_fraction <= 0.5:
        raise ValueError("ramp_period_fraction must be in [0, 0.5]")
    if args.calibration_seeds < 4:
        raise ValueError("at least four calibration seeds are required")
    if args.evaluation_seeds < 1:
        raise ValueError("at least one evaluation seed is required")
    if args.workers < 1:
        raise ValueError("workers must be at least one")
    if args.point_count < 3:
        raise ValueError("point_count must be at least three")
    if not np.isfinite(args.simulation_timestep_s) or args.simulation_timestep_s <= 0.0:
        raise ValueError("simulation_timestep_s must be finite and positive")
    if not 0.0 <= args.maximum_false_alarm_rate <= 1.0:
        raise ValueError("maximum_false_alarm_rate must be in [0, 1]")
    if not 0.0 <= args.minimum_fault_detection_rate <= 1.0:
        raise ValueError("minimum_fault_detection_rate must be in [0, 1]")


def ceil_to_stride(index: int, stride: int) -> int:
    """Return the first zero-based decision index at or after ``index``."""

    if index < 0 or stride <= 0:
        raise ValueError("index must be non-negative and stride must be positive")
    return int(math.ceil(index / stride) * stride)


def causal_window(
    record: ObservedRecord, *, end_index: int, window_steps: int
) -> ObservedRecord:
    """Slice a fixed past-only window and mask values not yet delivered at decision time."""

    if window_steps <= 0:
        raise ValueError("window_steps must be positive")
    if end_index < window_steps - 1 or end_index >= record.n_steps:
        raise ValueError("end_index cannot supply the requested fixed window")
    start = end_index - window_steps + 1
    stop = end_index + 1
    decision_time = float(record.measurement_time_s["tau_cmd"][end_index])
    if not np.isfinite(decision_time):
        raise ValueError("decision time must be finite")

    values: dict[str, np.ndarray] = {}
    valid_mask: dict[str, np.ndarray] = {}
    measurement_time: dict[str, np.ndarray] = {}
    availability_time: dict[str, np.ndarray] = {}
    latency_age: dict[str, np.ndarray] = {}
    for name in CHANNEL_NAMES:
        availability = np.asarray(record.availability_time_s[name][start:stop], dtype=float)
        delivered = np.isfinite(availability) & (availability <= decision_time + 1.0e-12)
        valid = np.asarray(record.valid_mask[name][start:stop], dtype=bool)
        valid = valid & delivered[:, None]
        valid_mask[name] = valid
        values[name] = np.where(valid, record.values[name][start:stop], np.nan)
        measurement_time[name] = np.asarray(
            record.measurement_time_s[name][start:stop], dtype=float
        ).copy()
        availability_time[name] = availability.copy()
        latency_age[name] = np.asarray(
            record.latency_age_s[name][start:stop], dtype=float
        ).copy()
    return ObservedRecord(
        suite=record.suite,
        run_id=record.run_id,
        pair_id=record.pair_id,
        config_hash=record.config_hash,
        values=values,
        valid_mask=valid_mask,
        measurement_time_s=measurement_time,
        availability_time_s=availability_time,
        latency_age_s=latency_age,
        suite_available_mask=record.suite_available_mask.copy(),
        schema_version=record.schema_version,
        split=record.split,
    )


def project_observed_suite(record: ObservedRecord, suite: str) -> ObservedRecord:
    """Project an S record to C1 by discarding the unavailable gauge role.

    The sensor model's CRN contract makes shared C1/S channels bitwise identical and
    gives the S-only gauges independent substreams.  Generating S once and physically
    masking its gauge role is therefore exactly equivalent to a matched C1 observation,
    while avoiding a second pass through the same pathology stack for every pilot seed.
    """

    if record.suite != "S" or suite not in DEPLOYABLE_SUITES:
        raise ValueError("pilot projection requires an S source and a C1 or S target")
    if suite == "S":
        return record
    available = set(SUITE_CHANNELS[suite])
    values: dict[str, np.ndarray] = {}
    valid_mask: dict[str, np.ndarray] = {}
    suite_mask: dict[str, bool] = {}
    measurement_time: dict[str, np.ndarray] = {}
    availability_time: dict[str, np.ndarray] = {}
    latency_age: dict[str, np.ndarray] = {}
    for name in CHANNEL_NAMES:
        present = name in available
        suite_mask[name] = present
        valid_mask[name] = (
            record.valid_mask[name].copy()
            if present
            else np.zeros_like(record.valid_mask[name], dtype=bool)
        )
        values[name] = (
            record.values[name].copy()
            if present
            else np.full_like(record.values[name], np.nan, dtype=float)
        )
        measurement_time[name] = (
            record.measurement_time_s[name].copy()
            if present
            else np.full_like(record.measurement_time_s[name], np.nan, dtype=float)
        )
        availability_time[name] = (
            record.availability_time_s[name].copy()
            if present
            else np.full_like(record.availability_time_s[name], np.nan, dtype=float)
        )
        latency_age[name] = (
            record.latency_age_s[name].copy()
            if present
            else np.full_like(record.latency_age_s[name], np.nan, dtype=float)
        )
    return ObservedRecord(
        suite=suite,
        run_id=record.run_id,
        pair_id=record.pair_id,
        config_hash=record.config_hash,
        values=values,
        valid_mask=valid_mask,
        measurement_time_s=measurement_time,
        availability_time_s=availability_time,
        latency_age_s=latency_age,
        suite_available_mask=suite_mask,
        schema_version=record.schema_version,
        split=record.split,
    )


def fit_reference(samples: dict[str, np.ndarray]) -> CoefficientReference:
    """Fit a healthy reference and fault centroids on calibration-only vectors."""

    if set(samples) != {"healthy", *FAULT_CLASSES}:
        raise ValueError("samples must contain healthy plus all three fault classes")
    healthy = np.asarray(samples["healthy"], dtype=float)
    if healthy.ndim != 2 or healthy.shape[0] < 4 or healthy.shape[1] < 1:
        raise ValueError("healthy calibration samples must have shape [N>=4,D>=1]")
    if not np.all(np.isfinite(healthy)):
        raise ValueError("healthy calibration samples must be finite")
    mean = healthy.mean(axis=0)
    std = healthy.std(axis=0)
    scale_floor = 1.0e-6 + 1.0e-6 * np.abs(mean)
    scale = np.maximum(std, scale_floor)

    loo_scores = np.empty(healthy.shape[0], dtype=float)
    for index in range(healthy.shape[0]):
        others = np.delete(healthy, index, axis=0)
        loo_mean = others.mean(axis=0)
        loo_std = others.std(axis=0)
        loo_scale = np.maximum(loo_std, 1.0e-6 + 1.0e-6 * np.abs(loo_mean))
        loo_scores[index] = coefficient_distance(healthy[index], loo_mean, loo_scale)
    threshold = float(max(np.quantile(loo_scores, 0.99, method="higher"), 1.0e-12))

    centroids: dict[str, np.ndarray] = {}
    for source in FAULT_CLASSES:
        fault = np.asarray(samples[source], dtype=float)
        if fault.ndim != 2 or fault.shape[1] != healthy.shape[1] or fault.shape[0] < 1:
            raise ValueError(f"{source} samples must have shape [N,D] aligned to healthy")
        if not np.all(np.isfinite(fault)):
            raise ValueError(f"{source} calibration samples must be finite")
        centroids[source] = ((fault - mean) / scale).mean(axis=0)
    return CoefficientReference(
        healthy_mean=mean,
        healthy_scale=scale,
        detect_threshold=threshold,
        fault_centroids=centroids,
        calibration_null_scores=loo_scores,
    )


def predict_fault(vector: np.ndarray, reference: CoefficientReference) -> str:
    """Classify a detected vector by nearest standardized fault-shape centroid."""

    standardized = (vector - reference.healthy_mean) / reference.healthy_scale
    distances = {
        source: float(np.linalg.norm(standardized - centroid))
        for source, centroid in reference.fault_centroids.items()
    }
    return min(FAULT_CLASSES, key=lambda source: (distances[source], source))


def evaluate_reference(
    reference: CoefficientReference, samples: dict[str, np.ndarray]
) -> dict[str, Any]:
    """Evaluate false alarms, fault detection, and prototype attribution held out."""

    healthy = np.asarray(samples["healthy"], dtype=float)
    healthy_scores = np.asarray(
        [
            coefficient_distance(row, reference.healthy_mean, reference.healthy_scale)
            for row in healthy
        ]
    )
    result: dict[str, Any] = {
        "detect_threshold": reference.detect_threshold,
        "calibration_null_mean": float(reference.calibration_null_scores.mean()),
        "calibration_null_max": float(reference.calibration_null_scores.max()),
        "healthy_score_mean": float(healthy_scores.mean()),
        "healthy_score_max": float(healthy_scores.max()),
        "false_alarm_rate": float(np.mean(healthy_scores > reference.detect_threshold)),
        "per_class": {},
    }
    correct_rates: list[float] = []
    detection_rates: list[float] = []
    for source in FAULT_CLASSES:
        fault = np.asarray(samples[source], dtype=float)
        scores = np.asarray(
            [
                coefficient_distance(row, reference.healthy_mean, reference.healthy_scale)
                for row in fault
            ]
        )
        detected = scores > reference.detect_threshold
        predicted = [predict_fault(row, reference) for row in fault]
        correct = np.asarray([label == source for label in predicted], dtype=bool)
        detection_rate = float(np.mean(detected))
        attribution_rate = float(np.mean(correct))
        detected_attribution = (
            float(np.mean(correct[detected])) if np.any(detected) else 0.0
        )
        result["per_class"][source] = {
            "score_mean": float(scores.mean()),
            "score_min": float(scores.min()),
            "detection_rate": detection_rate,
            "attribution_accuracy": attribution_rate,
            "detected_attribution_accuracy": detected_attribution,
        }
        detection_rates.append(detection_rate)
        correct_rates.append(attribution_rate)
    result["minimum_fault_detection_rate"] = float(min(detection_rates))
    result["macro_attribution_accuracy"] = float(np.mean(correct_rates))
    return result


def fault_specs(onset_index: int) -> dict[str, FaultSpec]:
    """Return the fixed development fault settings used by the pilot."""

    return {
        "healthy": FaultSpec(),
        "structure": FaultSpec(
            source_class="structure",
            subtype="link_stiffness_loss",
            location=1,
            severity=0.50,
            onset_index=onset_index,
        ),
        "actuator": FaultSpec(
            source_class="actuator",
            subtype="actuator_gain_loss",
            location=1,
            severity=0.70,
            onset_index=onset_index,
        ),
        "sensor": FaultSpec(
            source_class="sensor",
            subtype="encoder_bias",
            location=0,
            severity=0.05,
            onset_index=onset_index,
        ),
    }


def generate_plant_records(
    config: CableModelConfig,
    *,
    onset_index: int,
    n_steps: int,
    point_count: int,
    simulation_timestep_s: float,
    thermal_rate_c_s: float,
) -> dict[str, PrivilegedRecord]:
    """Generate deterministic healthy/structure/actuator privileged traces."""

    specs = fault_specs(onset_index)
    records: dict[str, PrivilegedRecord] = {}
    for source in ("healthy", "structure", "actuator"):
        print(f"    plant {source} ...", flush=True)
        plant = CablePlant(
            config,
            point_count=point_count,
            simulation_timestep_s=simulation_timestep_s,
            fault=specs[source],
        )
        records[source] = plant.rollout(
            n_steps,
            temperature_fn=lambda _index, time_s: 25.0 + thermal_rate_c_s * time_s,
        )
    records["sensor"] = records["healthy"]
    return records


_VECTOR_WORKER_CONTEXT: dict[str, Any] = {}


def initialize_vector_worker(
    records: dict[str, PrivilegedRecord],
    onset_index: int,
    period_steps: int,
    suites: tuple[str, ...],
    windows: tuple[int, ...],
    strides: tuple[int, ...],
    frequency_hz: float,
    condition_id: str,
) -> None:
    """Initialize one process with read-only mechanics records and pilot constants."""

    global _VECTOR_WORKER_CONTEXT
    _VECTOR_WORKER_CONTEXT = {
        "records": records,
        "specs": fault_specs(onset_index),
        "probe_end_index": onset_index + period_steps - 1,
        "suites": suites,
        "windows": windows,
        "strides": strides,
        "condition_id": condition_id,
        "extractors": {
            window: WindowFeatureExtractor(
                window_steps=window, probe_frequency_hz=frequency_hz
            )
            for window in windows
        },
    }


def collect_seed_vectors(
    task: tuple[str, str, int]
) -> tuple[str, str, dict[tuple[str, int, int], np.ndarray]]:
    """Generate one source/seed S observation and both suites' coefficient vectors."""

    split, source, sensor_seed = task
    context = _VECTOR_WORKER_CONTEXT
    if not context:
        raise RuntimeError("vector worker was not initialized")
    pair_id = f"{context['condition_id']}-{split}-{source}-{sensor_seed}"
    sensor_fault = context["specs"]["sensor"] if source == "sensor" else None
    observed_s = SensorModel(SensorConfig()).observe(
        context["records"][source],
        "S",
        pair_id=pair_id,
        sensor_seed=sensor_seed,
        fault=sensor_fault,
        run_id=pair_id,
        config_hash="dev-noisy-reference-pilot",
        split="pilot",
    )
    vectors: dict[tuple[str, int, int], np.ndarray] = {}
    for suite in context["suites"]:
        observed = project_observed_suite(observed_s, suite)
        for stride in context["strides"]:
            end_index = ceil_to_stride(context["probe_end_index"], stride)
            for window_steps in context["windows"]:
                window = causal_window(
                    observed, end_index=end_index, window_steps=window_steps
                )
                vectors[(suite, window_steps, stride)] = synchronous_coefficient_vector(
                    window, context["extractors"][window_steps]
                )
    return split, source, vectors


def collect_vectors(
    records: dict[str, PrivilegedRecord],
    *,
    onset_index: int,
    period_steps: int,
    suites: Iterable[str],
    windows: Iterable[int],
    strides: Iterable[int],
    calibration_seed_values: Iterable[int],
    evaluation_seed_values: Iterable[int],
    frequency_hz: float,
    condition_id: str,
    workers: int,
) -> dict[tuple[str, int, int], dict[str, dict[str, list[np.ndarray]]]]:
    """Build coefficient vectors for every suite/window/stride/source/split cell."""

    windows = tuple(sorted(set(int(value) for value in windows)))
    strides = tuple(sorted(set(int(value) for value in strides)))
    output: dict[
        tuple[str, int, int], dict[str, dict[str, list[np.ndarray]]]
    ] = {
        (suite, window, stride): {
            split: {source: [] for source in ("healthy", *FAULT_CLASSES)}
            for split in ("calibration", "evaluation")
        }
        for suite in suites
        for window in windows
        for stride in strides
    }
    seed_groups = {
        "calibration": tuple(calibration_seed_values),
        "evaluation": tuple(evaluation_seed_values),
    }
    tasks = [
        (split, source, sensor_seed)
        for split, seeds in seed_groups.items()
        for source in ("healthy", *FAULT_CLASSES)
        for sensor_seed in seeds
    ]
    init_args = (
        records,
        onset_index,
        period_steps,
        tuple(suites),
        windows,
        strides,
        frequency_hz,
        condition_id,
    )
    if workers == 1:
        initialize_vector_worker(*init_args)
        results = map(collect_seed_vectors, tasks)
        for split, source, vectors in results:
            for key, vector in vectors.items():
                output[key][split][source].append(vector)
    else:
        with concurrent.futures.ProcessPoolExecutor(
            max_workers=workers,
            initializer=initialize_vector_worker,
            initargs=init_args,
        ) as executor:
            for split, source, vectors in executor.map(collect_seed_vectors, tasks):
                for key, vector in vectors.items():
                    output[key][split][source].append(vector)
    return output


def jsonable(value: Any) -> Any:
    """Convert numpy-rich result structures into JSON-native values."""

    if isinstance(value, dict):
        return {str(key): jsonable(item) for key, item in value.items()}
    if isinstance(value, (list, tuple)):
        return [jsonable(item) for item in value]
    if isinstance(value, np.ndarray):
        return value.tolist()
    if isinstance(value, (np.floating, np.integer, np.bool_)):
        return value.item()
    return value


def aggregate_rows(rows: list[dict[str, Any]]) -> list[dict[str, Any]]:
    """Aggregate onset-alignment rows for each candidate/suite/W/stride cell."""

    groups: dict[tuple[Any, ...], list[dict[str, Any]]] = {}
    for row in rows:
        key = (
            row["task_torque_scale"],
            row["peak_load_n"],
            row["suite"],
            row["window"],
            row["stride"],
        )
        groups.setdefault(key, []).append(row)
    output: list[dict[str, Any]] = []
    for key, group in groups.items():
        output.append(
            {
                "task_torque_scale": key[0],
                "peak_load_n": key[1],
                "suite": key[2],
                "window": key[3],
                "stride": key[4],
                "onset_alignments": len(group),
                "maximum_false_alarm_rate": max(row["false_alarm_rate"] for row in group),
                "mean_false_alarm_rate": float(
                    np.mean([row["false_alarm_rate"] for row in group])
                ),
                "minimum_fault_detection_rate": min(
                    row["minimum_fault_detection_rate"] for row in group
                ),
                "mean_macro_attribution_accuracy": float(
                    np.mean([row["macro_attribution_accuracy"] for row in group])
                ),
                "minimum_macro_attribution_accuracy": min(
                    row["macro_attribution_accuracy"] for row in group
                ),
                "safety_screen_pass": all(row["safety_screen_pass"] for row in group),
                "sync_vector_nonzero": all(row["sync_vector_nonzero"] for row in group),
            }
        )
    return output


def choose_recommendation(
    aggregate: list[dict[str, Any]], args: argparse.Namespace
) -> dict[str, Any]:
    """Select an evidence-backed development setting without freezing it."""

    s_rows = [
        row
        for row in aggregate
        if row["suite"] == "S"
        and row["safety_screen_pass"]
        and row["sync_vector_nonzero"]
        and row["maximum_false_alarm_rate"] <= args.maximum_false_alarm_rate
        and row["minimum_fault_detection_rate"] >= args.minimum_fault_detection_rate
    ]
    if not s_rows:
        return {
            "decision": "NO SETTING CLEARS THE DEPLOYABLE PILOT SCREEN",
            "setting": None,
            "reason": (
                "No suite-S cell simultaneously cleared safety, held-out false alarms, "
                "the minimum per-fault detection rate, and the full-cycle feature gate."
            ),
        }
    s_rows.sort(
        key=lambda row: (
            -row["minimum_macro_attribution_accuracy"],
            -row["minimum_fault_detection_rate"],
            row["maximum_false_alarm_rate"],
            row["peak_load_n"],
            row["task_torque_scale"],
            row["window"],
            row["stride"],
        )
    )
    selected = s_rows[0]
    return {
        "decision": "ADVANCE SETTING FOR REFERENCE-RUNG IMPLEMENTATION REVIEW",
        "setting": selected,
        "reason": (
            "This suite-S setting cleared the predeclared development false-alarm and "
            "per-fault detection screens across every tested onset alignment and ranked "
            "highest on worst-alignment prototype attribution. It remains a pilot choice, "
            "not a frozen configuration or headline result."
        ),
    }


def write_rows_csv(path: Path, rows: list[dict[str, Any]]) -> None:
    """Write the per-alignment decision table."""

    fields = [
        "task_torque_scale",
        "peak_load_n",
        "onset_offset_steps",
        "onset_index",
        "suite",
        "window",
        "stride",
        "decision_lag_steps",
        "safety_screen_pass",
        "sync_vector_nonzero",
        "detect_threshold",
        "false_alarm_rate",
        "minimum_fault_detection_rate",
        "structure_detection_rate",
        "actuator_detection_rate",
        "sensor_detection_rate",
        "macro_attribution_accuracy",
        "structure_attribution_accuracy",
        "actuator_attribution_accuracy",
        "sensor_attribution_accuracy",
    ]
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=fields)
        writer.writeheader()
        writer.writerows({field: row[field] for field in fields} for row in rows)


def write_aggregate_csv(path: Path, rows: list[dict[str, Any]]) -> None:
    """Write onset-aggregated C1/S comparison rows."""

    fields = [
        "task_torque_scale",
        "peak_load_n",
        "suite",
        "window",
        "stride",
        "onset_alignments",
        "maximum_false_alarm_rate",
        "mean_false_alarm_rate",
        "minimum_fault_detection_rate",
        "mean_macro_attribution_accuracy",
        "minimum_macro_attribution_accuracy",
        "safety_screen_pass",
        "sync_vector_nonzero",
    ]
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=fields)
        writer.writeheader()
        writer.writerows({field: row[field] for field in fields} for row in rows)


def write_report(path: Path, summary: dict[str, Any]) -> None:
    """Write the human-readable pilot decision and its honesty boundaries."""

    recommendation = summary["recommendation"]
    s_rows = [row for row in summary["aggregate"] if row["suite"] == "S"]
    ranked_best = sorted(
        s_rows,
        key=lambda row: (
            -row["minimum_fault_detection_rate"],
            -row["minimum_macro_attribution_accuracy"],
            row["maximum_false_alarm_rate"],
            row["peak_load_n"],
            row["task_torque_scale"],
            row["window"],
            row["stride"],
        ),
    )[0]
    closest = recommendation["setting"] or ranked_best
    c1_match = next(
        row
        for row in summary["aggregate"]
        if row["suite"] == "C1"
        and row["task_torque_scale"] == closest["task_torque_scale"]
        and row["peak_load_n"] == closest["peak_load_n"]
        and row["window"] == closest["window"]
        and row["stride"] == closest["stride"]
    )
    blocked = recommendation["setting"] is None
    if blocked:
        diagnosis_heading = "## What blocked, and what survived"
        diagnosis = (
            f"The block was false alarms: suite S produced a pooled/mean held-out healthy "
            f"false-alarm rate of {100.0 * closest['mean_false_alarm_rate']:.1f}% and a "
            f"worst-alignment rate of {100.0 * closest['maximum_false_alarm_rate']:.1f}%, "
            f"above the {100.0 * summary['development_screen']['maximum_false_alarm_rate']:.1f}% "
            f"development screen. With {summary['grid']['calibration_seeds']} healthy "
            "calibration seeds, the nominal 99th-percentile higher-method threshold is "
            "the maximum leave-one-out calibration score whenever fewer than 100 values "
            "are available. The current sample did not resolve the requested tail. This "
            "pilot therefore supports the coefficient/reference signal path but blocks "
            "the threshold as not validation-ready. The next threshold choice must use "
            "a larger healthy calibration set or a separately predeclared conservative "
            "rule; it must not be tuned on these held-out rows."
        )
        closing_boundary = (
            "- This BLOCK still settles a usable scheduled-reference convention for owner "
            "review, but the threshold must be re-calibrated prospectively before any setting "
            "can advance. Nothing here is a config freeze."
        )
    else:
        diagnosis_heading = "## What cleared, and what remains provisional"
        diagnosis = (
            f"Suite S's pooled/mean held-out healthy false-alarm rate was "
            f"{100.0 * closest['mean_false_alarm_rate']:.1f}% and the worst tested "
            f"alignment was {100.0 * closest['maximum_false_alarm_rate']:.1f}%, while "
            f"the minimum per-fault detection rate remained "
            f"{100.0 * closest['minimum_fault_detection_rate']:.1f}%. This advances the "
            "scheduled-reference convention for estimator-owner review only. With "
            f"{summary['grid']['calibration_seeds']} calibration seeds, the pilot's "
            "99th-percentile higher-method threshold is still the maximum leave-one-out "
            "score; the reported worst-alignment false-alarm rate therefore has only "
            f"1/{summary['grid']['evaluation_seeds']} event resolution. The threshold, "
            "sensor constants, severities, and W/stride values remain development choices "
            "until a larger validation calibration and config freeze."
        )
        closing_boundary = (
            "- The advance is only to estimator-owner review and the next pilot increment; "
            "it is not a research result or a config freeze."
        )
    cell_label = "selected" if not blocked else "closest"
    lines = [
        "# Noisy Healthy-Reference Coefficient Pilot",
        "",
        f"**Decision: {recommendation['decision']}.** {recommendation['reason']}",
        "",
        "Development pilot only. Every score below comes from noisy deployable "
        "`ObservedRecord` data. The healthy reference and the three fault-shape centroids "
        "use calibration sensor seeds; false alarms, detection, and prototype attribution "
        "use disjoint held-out seeds. No privileged fault-minus-healthy trace is a detector "
        "input, and no config value is frozen.",
        "",
        "## Reference and alignment convention tested",
        "",
        "- Phase-locked scheduled probe: the one-cycle 0.8 Hz burst resets phase at the "
        "declared fault/probe onset.",
        "- The estimator decision is the first global stride-grid decision at or after the "
        "probe ends. The healthy reference is conditioned on task/probe setting, W, and "
        "that decision lag; it is a calibration model, not a matched counterfactual run.",
        "- Detection uses the dimension-normalized, healthy-standardized Euclidean distance "
        "between the live cosine/sine coefficient vector and the healthy mean. The threshold "
        "is the 99th-percentile (higher method) leave-one-out healthy calibration score.",
        "- Attribution is nearest fault-shape centroid in the same standardized coefficient "
        "space. It is a pilot instrument, not the learned headline attribution model.",
        f"- Reproduction seed: base {summary['grid']['base_seed']}; calibration uses "
        f"[{summary['grid']['base_seed']}, "
        f"{summary['grid']['base_seed'] + summary['grid']['calibration_seeds'] - 1}] and "
        f"held-out evaluation uses "
        f"[{summary['grid']['base_seed'] + summary['grid']['calibration_seeds']}, "
        f"{summary['grid']['base_seed'] + summary['grid']['calibration_seeds'] + summary['grid']['evaluation_seeds'] - 1}].",
        "",
        diagnosis_heading,
        "",
        f"The {cell_label} cell was task {closest['task_torque_scale']:.3f}, probe "
        f"{closest['peak_load_n']:.3f} N, W={closest['window']}, stride={closest['stride']}. "
        f"Suite S's worst per-fault detection rate across the tested alignments was "
        f"{100.0 * closest['minimum_fault_detection_rate']:.1f}%, and its "
        f"prototype attribution was {100.0 * closest['minimum_macro_attribution_accuracy']:.1f}% "
        f"in the worst alignment. The matched C1 minimum fault-detection rate was only "
        f"{100.0 * c1_match['minimum_fault_detection_rate']:.1f}%.",
        "",
        diagnosis,
        "",
        "## Best cell per candidate (suite S)",
        "",
        "| Task | Probe | W | Stride | Mean / max false alarm | Min fault detect | Min attribution |",
        "|---:|---:|---:|---:|---:|---:|---:|",
    ]
    candidates: dict[tuple[float, float], list[dict[str, Any]]] = {}
    for row in summary["aggregate"]:
        if row["suite"] == "S":
            candidates.setdefault(
                (row["task_torque_scale"], row["peak_load_n"]), []
            ).append(row)
    for key in sorted(candidates):
        eligible_cells = [
            row
            for row in candidates[key]
            if row["safety_screen_pass"]
            and row["sync_vector_nonzero"]
            and row["maximum_false_alarm_rate"]
            <= summary["development_screen"]["maximum_false_alarm_rate"]
            and row["minimum_fault_detection_rate"]
            >= summary["development_screen"]["minimum_fault_detection_rate"]
        ]
        cells = sorted(
            eligible_cells or candidates[key],
            key=lambda row: (
                -row["minimum_fault_detection_rate"],
                -row["minimum_macro_attribution_accuracy"],
                row["maximum_false_alarm_rate"],
            ),
        )
        row = cells[0]
        lines.append(
            f"| {key[0]:.3f} | {key[1]:.3f} N | {row['window']} | {row['stride']} | "
            f"{100.0 * row['mean_false_alarm_rate']:.1f}% / "
            f"{100.0 * row['maximum_false_alarm_rate']:.1f}% | "
            f"{100.0 * row['minimum_fault_detection_rate']:.1f}% | "
            f"{100.0 * row['minimum_macro_attribution_accuracy']:.1f}% |"
        )
    lines.extend(
        [
            "",
            "## Required negative control",
            "",
            "W=512 is shorter than one 0.8 Hz period. Under the current estimator contract "
            "its synchronous cosine/sine entries remain zero; it is retained in the CSV/JSON "
            "as the inert-window negative control rather than silently dropped.",
            "",
            "## Boundaries",
            "",
            "- This is not the confirmatory C1-vs-S experiment, does not set the Claim-Sheet "
            "effect bars, and does not train the matched temporal-attribution or RMA models.",
            "- Reference conditioning assumes a scheduled, phase-reset diagnostic probe. "
            "Unscheduled phase drift and probe-band thermal interference remain open tests.",
            "- The current non-load-bearing sensor constants and fixed development severities "
            "remain provisional. Optional-contact cases are still blocked on endpoint-contact "
            "extraction.",
            closing_boundary,
        ]
    )
    path.write_text("\n".join(lines) + "\n", encoding="utf-8")


def run(args: argparse.Namespace) -> dict[str, Any]:
    """Run the full pilot grid and write reproducible artifacts."""

    validate_args(args)
    dt_s = CableModelConfig().control_dt_s
    base_onset_index = int(round(args.base_onset_s / dt_s))
    period_s = 1.0 / args.frequency_hz
    period_steps = int(round(period_s / dt_s))
    if not math.isclose(period_steps * dt_s, period_s, rel_tol=0.0, abs_tol=1.0e-12):
        raise ValueError("probe period must be an integer number of control steps")
    calibration_seed_values = range(args.seed, args.seed + args.calibration_seeds)
    evaluation_seed_values = range(
        args.seed + args.calibration_seeds,
        args.seed + args.calibration_seeds + args.evaluation_seeds,
    )
    thermal_rate_c_s = args.thermal_ramp_c_per_window / (640.0 * dt_s)

    rows: list[dict[str, Any]] = []
    for task_scale in sorted(set(float(value) for value in args.task_torque_scales)):
        for peak_load in sorted(set(float(value) for value in args.peak_loads_n)):
            for onset_offset in sorted(set(int(value) for value in args.onset_offset_steps)):
                onset_index = base_onset_index + onset_offset
                start_s = onset_index * dt_s
                config = CableModelConfig(
                    task_torque_scale=task_scale,
                    diagnostic_tip_load_peak_n=peak_load,
                    diagnostic_tip_load_frequency_hz=args.frequency_hz,
                    diagnostic_tip_load_start_s=start_s,
                    diagnostic_tip_load_duration_s=period_s,
                    diagnostic_tip_load_ramp_s=period_s * args.ramp_period_fraction,
                )
                probe_end_index = onset_index + period_steps - 1
                n_steps = max(
                    ceil_to_stride(probe_end_index, int(stride))
                    for stride in args.strides
                ) + 1
                condition_id = (
                    f"task{task_scale:.3f}-probe{peak_load:.3f}-offset{onset_offset}"
                )
                print(f"Running {condition_id} ...", flush=True)
                records = generate_plant_records(
                    config,
                    onset_index=onset_index,
                    n_steps=n_steps,
                    point_count=args.point_count,
                    simulation_timestep_s=args.simulation_timestep_s,
                    thermal_rate_c_s=thermal_rate_c_s,
                )
                safety_pass = all(
                    not bool(np.any(records[source].safety_flag))
                    for source in ("healthy", "structure", "actuator")
                )
                vectors = collect_vectors(
                    records,
                    onset_index=onset_index,
                    period_steps=period_steps,
                    suites=DEPLOYABLE_SUITES,
                    windows=args.windows,
                    strides=args.strides,
                    calibration_seed_values=calibration_seed_values,
                    evaluation_seed_values=evaluation_seed_values,
                    frequency_hz=args.frequency_hz,
                    condition_id=condition_id,
                    workers=args.workers,
                )
                for (suite, window_steps, stride), split_samples in vectors.items():
                    calibration = {
                        source: np.stack(values)
                        for source, values in split_samples["calibration"].items()
                    }
                    evaluation = {
                        source: np.stack(values)
                        for source, values in split_samples["evaluation"].items()
                    }
                    reference = fit_reference(calibration)
                    evaluation_result = evaluate_reference(reference, evaluation)
                    decision_index = ceil_to_stride(probe_end_index, stride)
                    row = {
                        "task_torque_scale": task_scale,
                        "peak_load_n": peak_load,
                        "onset_offset_steps": onset_offset,
                        "onset_index": onset_index,
                        "suite": suite,
                        "window": window_steps,
                        "stride": stride,
                        "decision_lag_steps": decision_index - probe_end_index,
                        "safety_screen_pass": safety_pass,
                        "sync_vector_nonzero": bool(
                            any(
                                np.any(np.abs(calibration[source]) > 1.0e-12)
                                for source in calibration
                            )
                        ),
                        "detect_threshold": evaluation_result["detect_threshold"],
                        "false_alarm_rate": evaluation_result["false_alarm_rate"],
                        "minimum_fault_detection_rate": evaluation_result[
                            "minimum_fault_detection_rate"
                        ],
                        "structure_detection_rate": evaluation_result["per_class"][
                            "structure"
                        ]["detection_rate"],
                        "actuator_detection_rate": evaluation_result["per_class"][
                            "actuator"
                        ]["detection_rate"],
                        "sensor_detection_rate": evaluation_result["per_class"]["sensor"][
                            "detection_rate"
                        ],
                        "macro_attribution_accuracy": evaluation_result[
                            "macro_attribution_accuracy"
                        ],
                        "structure_attribution_accuracy": evaluation_result["per_class"][
                            "structure"
                        ]["attribution_accuracy"],
                        "actuator_attribution_accuracy": evaluation_result["per_class"][
                            "actuator"
                        ]["attribution_accuracy"],
                        "sensor_attribution_accuracy": evaluation_result["per_class"][
                            "sensor"
                        ]["attribution_accuracy"],
                        "detail": evaluation_result,
                    }
                    rows.append(row)

    aggregate = aggregate_rows(rows)
    recommendation = choose_recommendation(aggregate, args)
    summary = jsonable(
        {
            "purpose": "development noisy-reference pilot; not confirmatory or frozen",
            "grid": {
                "task_torque_scales": sorted(set(args.task_torque_scales)),
                "peak_loads_n": sorted(set(args.peak_loads_n)),
                "windows": sorted(set(args.windows)),
                "strides": sorted(set(args.strides)),
                "onset_offset_steps": sorted(set(args.onset_offset_steps)),
                "base_seed": args.seed,
                "calibration_seeds": args.calibration_seeds,
                "evaluation_seeds": args.evaluation_seeds,
                "workers": args.workers,
                "frequency_hz": args.frequency_hz,
                "thermal_ramp_c_per_640_sample_window": args.thermal_ramp_c_per_window,
                "point_count": args.point_count,
                "simulation_timestep_s": args.simulation_timestep_s,
            },
            "development_screen": {
                "maximum_false_alarm_rate": args.maximum_false_alarm_rate,
                "minimum_fault_detection_rate": args.minimum_fault_detection_rate,
            },
            "reference_convention": {
                "probe": "scheduled phase-reset one-cycle burst",
                "decision": "first global stride-grid decision at or after probe end",
                "reference": (
                    "healthy calibration mean/scale conditioned on task, probe, W, and "
                    "decision lag; no matched fault-minus-healthy input"
                ),
                "distance": (
                    "dimension-normalized diagonal-Mahalanobis distance on retained "
                    "cosine/sine coefficients"
                ),
                "threshold": (
                    "99th-percentile higher-method leave-one-out healthy calibration score"
                ),
                "attribution": (
                    "nearest calibration fault-shape centroid; pilot instrument only"
                ),
            },
            "rows": rows,
            "aggregate": aggregate,
            "recommendation": recommendation,
        }
    )
    args.output_dir.mkdir(parents=True, exist_ok=True)
    (args.output_dir / "summary.json").write_text(
        json.dumps(summary, indent=2) + "\n", encoding="utf-8"
    )
    write_rows_csv(args.output_dir / "pilot_results.csv", rows)
    write_aggregate_csv(args.output_dir / "pilot_aggregate.csv", aggregate)
    write_report(args.output_dir / "noisy_reference_pilot_report.md", summary)
    print(f"Decision: {recommendation['decision']}; outputs: {args.output_dir}", flush=True)
    return summary


def main() -> int:
    """Run the CLI pilot."""

    run(parse_args())
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
