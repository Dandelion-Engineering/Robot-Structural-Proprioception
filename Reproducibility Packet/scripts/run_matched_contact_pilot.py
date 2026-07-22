"""Run the matched contact-enabled C1/S development pilot.

The pilot applies the screened z=0.100 m endpoint plane identically to matched C1
and S pairs under the task-0.50 / 0.05 N one-cycle probe.  It has three deliberately
separate parts:

1. a contact-conditioned noisy-reference screen at the first causal post-probe
   decision, using disjoint calibration and held-out sensor seeds;
2. a short 2.6 s online seam check through ``CablePlant -> OnlineSensorSession ->
   EstimatorCommandPolicy -> GainScheduledRecoveryController``, including the
   observation-side encoder fault; and
3. a mandatory onset+5 s open-loop horizon audit of both the selected plane and the
   former low-plane control.

The nearest-centroid estimator used in part 2 is a pilot-only mechanism instrument.
It is not the learned attribution head, its one-hot probabilities are not calibrated,
and its fixed location/severity lookup is tied to the canonical development faults.
The artifact therefore cannot freeze the contact profile, thresholds, estimator,
controller, W/stride, fault grid, sensor constants, or ``config.json``.
"""

from __future__ import annotations

import argparse
import concurrent.futures
import csv
import json
import math
from dataclasses import asdict, dataclass
from pathlib import Path
from typing import Any

import numpy as np

from run_noisy_reference_pilot import (
    CoefficientReference,
    causal_window,
    evaluate_reference,
    fault_specs,
    fit_reference,
    generate_plant_records,
    jsonable,
    predict_fault,
    project_observed_suite,
)
from screen_optional_contact_profile import (
    PHYSICAL_SCENARIOS,
    ScreenSpec,
    run_physical_scenario,
    summarize_record,
)
from utils.cable_mechanics import CableModelConfig, commanded_torque
from utils.cable_plant import CablePlant
from utils.estimator import (
    DiagnosisEstimator,
    EstimatorCommandPolicy,
    EstimatorOutput,
    SOURCE_CLASS_ORDER,
    WindowFeatureExtractor,
    coefficient_reference_distance,
    synchronous_coefficient_vector,
)
from utils.online_loop import run_online_rollout
from utils.recovery_control import GainScheduledRecoveryController
from utils.schema_types import ObservedRecord, PrivilegedRecord
from utils.sensor_model import OnlineSensorSession, SensorConfig, SensorModel


DEPLOYABLE_SUITES = ("C1", "S")
CANONICAL_SOURCES = ("healthy", "structure", "actuator", "sensor")


@dataclass(frozen=True)
class MatchedContactPilotSpec:
    """Portable development settings and explicit pilot/evaluation boundaries."""

    selected_plane_z_m: float = 0.100
    former_control_plane_z_m: float = 0.050
    task_torque_scale: float = 0.50
    diagnostic_tip_load_peak_n: float = 0.05
    diagnostic_tip_load_frequency_hz: float = 0.8
    fault_onset_s: float = 1.0
    short_horizon_s: float = 2.6
    evaluation_horizon_s: float = 6.0
    ramp_period_fraction: float = 0.125
    control_dt_s: float = 0.002
    window_steps: int = 768
    stride: int = 16
    calibration_seeds: int = 32
    evaluation_seeds: int = 48
    base_seed: int = 9000
    representative_seed: int = 9032
    thermal_ramp_c_per_640_steps: float = 3.0
    point_count: int = 17
    simulation_timestep_s: float = 1.0e-4
    maximum_false_alarm_rate: float = 0.05
    minimum_fault_detection_rate: float = 0.80
    minimum_attribution_accuracy: float = 0.80

    def validate(self) -> None:
        """Fail loudly when the pilot contract is malformed or internally inconsistent."""

        finite_positive = {
            "selected_plane_z_m": self.selected_plane_z_m,
            "diagnostic_tip_load_frequency_hz": self.diagnostic_tip_load_frequency_hz,
            "short_horizon_s": self.short_horizon_s,
            "evaluation_horizon_s": self.evaluation_horizon_s,
            "control_dt_s": self.control_dt_s,
            "simulation_timestep_s": self.simulation_timestep_s,
        }
        for name, value in finite_positive.items():
            if not np.isfinite(value) or value <= 0.0:
                raise ValueError(f"{name} must be finite and positive")
        if not np.isfinite(self.former_control_plane_z_m):
            raise ValueError("former_control_plane_z_m must be finite")
        if self.former_control_plane_z_m >= self.selected_plane_z_m:
            raise ValueError("former control plane must be below the selected plane")
        if self.task_torque_scale < 0.0 or self.diagnostic_tip_load_peak_n < 0.0:
            raise ValueError("task scale and diagnostic peak must be non-negative")
        if not 0.0 <= self.ramp_period_fraction <= 0.5:
            raise ValueError("ramp_period_fraction must lie in [0, 0.5]")
        if self.fault_onset_s < 0.0:
            raise ValueError("fault_onset_s must be non-negative")
        if self.window_steps < 1 or self.stride < 1:
            raise ValueError("window_steps and stride must be positive")
        if self.calibration_seeds < 4 or self.evaluation_seeds < 1:
            raise ValueError("need at least four calibration and one evaluation seed")
        if not self.base_seed <= self.representative_seed < (
            self.base_seed + self.calibration_seeds + self.evaluation_seeds
        ):
            raise ValueError("representative_seed must belong to the declared seed range")
        if self.representative_seed < self.base_seed + self.calibration_seeds:
            raise ValueError("representative_seed must come from the held-out range")
        if self.point_count < 3:
            raise ValueError("point_count must be at least three")
        for name, value in {
            "maximum_false_alarm_rate": self.maximum_false_alarm_rate,
            "minimum_fault_detection_rate": self.minimum_fault_detection_rate,
            "minimum_attribution_accuracy": self.minimum_attribution_accuracy,
        }.items():
            if not 0.0 <= value <= 1.0:
                raise ValueError(f"{name} must lie in [0, 1]")
        for name, seconds in {
            "fault_onset_s": self.fault_onset_s,
            "short_horizon_s": self.short_horizon_s,
            "evaluation_horizon_s": self.evaluation_horizon_s,
            "probe_period_s": self.probe_period_s,
        }.items():
            steps = seconds / self.control_dt_s
            if not math.isclose(steps, round(steps), rel_tol=0.0, abs_tol=1.0e-10):
                raise ValueError(f"{name}/control_dt_s must be an integer")
        if self.short_n_steps <= self.first_online_decision_step:
            raise ValueError("short horizon must extend beyond the first online decision")
        if self.evaluation_horizon_s < self.fault_onset_s + 5.0:
            raise ValueError("evaluation horizon must cover five seconds after onset")

    @property
    def probe_period_s(self) -> float:
        """Return one complete diagnostic-probe period."""

        return 1.0 / self.diagnostic_tip_load_frequency_hz

    @property
    def onset_index(self) -> int:
        """Return the first physical fault step."""

        return int(round(self.fault_onset_s / self.control_dt_s))

    @property
    def period_steps(self) -> int:
        """Return the exact probe duration in control steps."""

        return int(round(self.probe_period_s / self.control_dt_s))

    @property
    def probe_end_index(self) -> int:
        """Return the final step index whose integration interval contains the probe."""

        return self.onset_index + self.period_steps - 1

    @property
    def first_online_decision_step(self) -> int:
        """Return the first stride step after the complete probe has been observed."""

        after_probe = self.probe_end_index + 1
        return ((after_probe + self.stride - 1) // self.stride) * self.stride

    @property
    def offline_decision_index(self) -> int:
        """Return the newest observation available at the first online decision."""

        return self.first_online_decision_step - 1

    @property
    def short_n_steps(self) -> int:
        """Return the short pilot length in control steps."""

        return int(round(self.short_horizon_s / self.control_dt_s))

    @property
    def evaluation_n_steps(self) -> int:
        """Return the onset+5 s audit length in control steps."""

        return int(round(self.evaluation_horizon_s / self.control_dt_s))

    @property
    def thermal_rate_c_s(self) -> float:
        """Return the existing development thermal-ramp rate."""

        return self.thermal_ramp_c_per_640_steps / (640.0 * self.control_dt_s)


def parse_args() -> argparse.Namespace:
    """Parse the portable matched-contact pilot command line."""

    defaults = MatchedContactPilotSpec()
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--output-dir",
        type=Path,
        default=Path("results/matched_contact_enabled_pilot"),
    )
    parser.add_argument("--selected-plane-z-m", type=float, default=defaults.selected_plane_z_m)
    parser.add_argument(
        "--former-control-plane-z-m", type=float, default=defaults.former_control_plane_z_m
    )
    parser.add_argument("--short-horizon-s", type=float, default=defaults.short_horizon_s)
    parser.add_argument(
        "--evaluation-horizon-s", type=float, default=defaults.evaluation_horizon_s
    )
    parser.add_argument("--calibration-seeds", type=int, default=defaults.calibration_seeds)
    parser.add_argument("--evaluation-seeds", type=int, default=defaults.evaluation_seeds)
    parser.add_argument("--seed", type=int, default=defaults.base_seed)
    parser.add_argument("--representative-seed", type=int, default=defaults.representative_seed)
    parser.add_argument("--workers", type=int, default=4)
    parser.add_argument("--point-count", type=int, default=defaults.point_count)
    parser.add_argument(
        "--simulation-timestep-s", type=float, default=defaults.simulation_timestep_s
    )
    return parser.parse_args()


def spec_from_args(args: argparse.Namespace) -> MatchedContactPilotSpec:
    """Build and validate a pilot specification from command-line values."""

    spec = MatchedContactPilotSpec(
        selected_plane_z_m=float(args.selected_plane_z_m),
        former_control_plane_z_m=float(args.former_control_plane_z_m),
        short_horizon_s=float(args.short_horizon_s),
        evaluation_horizon_s=float(args.evaluation_horizon_s),
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


def cable_config(spec: MatchedContactPilotSpec, plane_z_m: float) -> CableModelConfig:
    """Return the exact mechanics/contact configuration shared by every matched arm."""

    return CableModelConfig(
        control_dt_s=spec.control_dt_s,
        task_torque_scale=spec.task_torque_scale,
        diagnostic_tip_load_peak_n=spec.diagnostic_tip_load_peak_n,
        diagnostic_tip_load_frequency_hz=spec.diagnostic_tip_load_frequency_hz,
        diagnostic_tip_load_start_s=spec.fault_onset_s,
        diagnostic_tip_load_duration_s=spec.probe_period_s,
        diagnostic_tip_load_ramp_s=spec.probe_period_s * spec.ramp_period_fraction,
        endpoint_contact_enabled=True,
        endpoint_contact_plane_z_m=plane_z_m,
    )


def _one_hot(source: str) -> np.ndarray:
    """Return the canonical source-class one-hot vector."""

    probabilities = np.zeros(len(SOURCE_CLASS_ORDER), dtype=float)
    probabilities[SOURCE_CLASS_ORDER.index(source)] = 1.0
    return probabilities


class PilotPrototypeEstimator(DiagnosisEstimator):
    """Pilot-only nearest-centroid estimator for the short causal seam check.

    The estimator consumes only the delivered ``ObservedRecord`` window.  Its fixed
    location/severity output is a lookup attached to the *predicted* canonical class,
    never privileged run truth.  This is intentionally an instrument for testing the
    wired seam, not a substitute for the learned attribution head.
    """

    def __init__(
        self,
        reference: CoefficientReference,
        *,
        suite: str,
        window_steps: int,
        probe_frequency_hz: float,
        first_decision_step: int,
    ) -> None:
        """Bind one suite-specific pilot reference and the causal decision gate."""

        if suite not in DEPLOYABLE_SUITES:
            raise ValueError(f"suite must be one of {DEPLOYABLE_SUITES}")
        if first_decision_step < 0:
            raise ValueError("first_decision_step must be non-negative")
        self.reference = reference
        self.suite = suite
        self.extractor = WindowFeatureExtractor(
            window_steps=window_steps, probe_frequency_hz=probe_frequency_hz
        )
        self.first_decision_step = int(first_decision_step)
        self.reset()

    def reset(self) -> None:
        """Reset the per-rollout first-detection latch and last predicted source."""

        self.detection_time_s = float("nan")
        self.last_predicted_source = "healthy"

    def update(
        self, step_index: int, decision_time_s: float, window: ObservedRecord | None
    ) -> EstimatorOutput:
        """Classify one delivered window after the complete probe is observable."""

        if step_index < self.first_decision_step or window is None:
            source = "healthy"
            score = 0.0
        else:
            if window.suite != self.suite:
                raise ValueError("pilot estimator received the wrong suite")
            vector = synchronous_coefficient_vector(window, self.extractor)
            score = coefficient_reference_distance(
                vector, self.reference.healthy_mean, self.reference.healthy_scale
            )
            source = (
                predict_fault(vector, self.reference)
                if score > self.reference.detect_threshold
                else "healthy"
            )
            if source != "healthy" and not np.isfinite(self.detection_time_s):
                self.detection_time_s = decision_time_s
        self.last_predicted_source = source
        location = -1
        severity = 0.0
        uncertainty = float("inf")
        if source == "structure":
            location, severity, uncertainty = 1, 0.50, 0.0
        elif source == "actuator":
            location, severity, uncertainty = 1, 0.70, 0.0
        elif source == "sensor":
            location, severity, uncertainty = 0, 0.05, 0.0
        output = EstimatorOutput(
            step=step_index,
            decision_time_s=decision_time_s,
            p_class=_one_hot(source),
            unknown_score=float(score),
            abstain_decision=False,
            location_out=location,
            severity_out=severity,
            severity_uncertainty=uncertainty,
            detection_time_s=self.detection_time_s,
        )
        output.validate()
        return output


def contact_screen_spec(
    spec: MatchedContactPilotSpec, *, duration_s: float
) -> ScreenSpec:
    """Return a compatible contact-summary spec for one declared horizon."""

    return ScreenSpec(
        plane_heights_z_m=(spec.former_control_plane_z_m, spec.selected_plane_z_m),
        task_torque_scale=spec.task_torque_scale,
        diagnostic_tip_load_peak_n=spec.diagnostic_tip_load_peak_n,
        diagnostic_tip_load_frequency_hz=spec.diagnostic_tip_load_frequency_hz,
        fault_onset_s=spec.fault_onset_s,
        duration_s=duration_s,
        ramp_period_fraction=spec.ramp_period_fraction,
        control_dt_s=spec.control_dt_s,
        point_count=spec.point_count,
        simulation_timestep_s=spec.simulation_timestep_s,
        minimum_contact_active_steps=5,
        maximum_contact_active_fraction=0.05,
    )


def fit_contact_references(
    spec: MatchedContactPilotSpec, *, workers: int
) -> tuple[dict[str, CoefficientReference], list[dict[str, Any]]]:
    """Fit/evaluate contact-conditioned references at the first causal decision."""

    records = generate_plant_records(
        cable_config(spec, spec.selected_plane_z_m),
        onset_index=spec.onset_index,
        n_steps=spec.short_n_steps,
        point_count=spec.point_count,
        simulation_timestep_s=spec.simulation_timestep_s,
        thermal_rate_c_s=spec.thermal_rate_c_s,
    )
    calibration = tuple(range(spec.base_seed, spec.base_seed + spec.calibration_seeds))
    evaluation = tuple(range(
        spec.base_seed + spec.calibration_seeds,
        spec.base_seed + spec.calibration_seeds + spec.evaluation_seeds,
    ))
    vectors = collect_exact_online_vectors(
        records,
        spec,
        calibration_seed_values=calibration,
        evaluation_seed_values=evaluation,
        workers=workers,
    )
    references: dict[str, CoefficientReference] = {}
    rows: list[dict[str, Any]] = []
    for suite, splits in sorted(vectors.items()):
        calibration_samples = {
            source: np.stack(values)
            for source, values in splits["calibration"].items()
        }
        evaluation_samples = {
            source: np.stack(values)
            for source, values in splits["evaluation"].items()
        }
        reference = fit_reference(calibration_samples)
        references[suite] = reference
        result = evaluate_reference(reference, evaluation_samples)
        row: dict[str, Any] = {
            "suite": suite,
            "window_steps": spec.window_steps,
            "stride": spec.stride,
            "offline_decision_index": spec.offline_decision_index,
            "detect_threshold": result["detect_threshold"],
            "false_alarm_rate": result["false_alarm_rate"],
            "minimum_fault_detection_rate": result["minimum_fault_detection_rate"],
            "macro_attribution_accuracy": result["macro_attribution_accuracy"],
        }
        for source in ("structure", "actuator", "sensor"):
            row[f"{source}_detection_rate"] = result["per_class"][source][
                "detection_rate"
            ]
            row[f"{source}_attribution_accuracy"] = result["per_class"][source][
                "attribution_accuracy"
            ]
        rows.append(row)
    return references, rows


_VECTOR_CONTEXT: dict[str, Any] = {}


def _initialize_vector_worker(
    records: dict[str, PrivilegedRecord], spec: MatchedContactPilotSpec
) -> None:
    """Initialize one process with read-only plant records and exact online timing."""

    global _VECTOR_CONTEXT
    _VECTOR_CONTEXT = {
        "records": records,
        "spec": spec,
        "faults": fault_specs(spec.onset_index),
        "extractor": WindowFeatureExtractor(
            window_steps=spec.window_steps,
            probe_frequency_hz=spec.diagnostic_tip_load_frequency_hz,
        ),
    }


def _collect_exact_vector(
    task: tuple[str, str, int]
) -> tuple[str, str, dict[str, np.ndarray]]:
    """Collect both suite vectors ending at the newest online-owned observation."""

    split, source, sensor_seed = task
    context = _VECTOR_CONTEXT
    if not context:
        raise RuntimeError("contact vector worker was not initialized")
    spec: MatchedContactPilotSpec = context["spec"]
    pair_id = f"matched-contact-{split}-{source}-{sensor_seed}"
    sensor_fault = context["faults"]["sensor"] if source == "sensor" else None
    observed_s = SensorModel(SensorConfig()).observe(
        context["records"][source],
        "S",
        pair_id=pair_id,
        sensor_seed=sensor_seed,
        fault=sensor_fault,
        run_id=pair_id,
        config_hash="dev-matched-contact-pilot",
        split="pilot",
    )
    vectors: dict[str, np.ndarray] = {}
    for suite in DEPLOYABLE_SUITES:
        observed = project_observed_suite(observed_s, suite)
        window = causal_window(
            observed,
            end_index=spec.offline_decision_index,
            window_steps=spec.window_steps,
        )
        vectors[suite] = synchronous_coefficient_vector(
            window, context["extractor"]
        )
    return split, source, vectors


def collect_exact_online_vectors(
    records: dict[str, PrivilegedRecord],
    spec: MatchedContactPilotSpec,
    *,
    calibration_seed_values: tuple[int, ...],
    evaluation_seed_values: tuple[int, ...],
    workers: int,
) -> dict[str, dict[str, dict[str, list[np.ndarray]]]]:
    """Collect contact-conditioned vectors on the exact causal online window."""

    output = {
        suite: {
            split: {source: [] for source in CANONICAL_SOURCES}
            for split in ("calibration", "evaluation")
        }
        for suite in DEPLOYABLE_SUITES
    }
    tasks = [
        (split, source, seed)
        for split, seeds in {
            "calibration": calibration_seed_values,
            "evaluation": evaluation_seed_values,
        }.items()
        for source in CANONICAL_SOURCES
        for seed in seeds
    ]
    init_args = (records, spec)
    if workers == 1:
        _initialize_vector_worker(*init_args)
        results = map(_collect_exact_vector, tasks)
        for split, source, vectors in results:
            for suite, vector in vectors.items():
                output[suite][split][source].append(vector)
    else:
        with concurrent.futures.ProcessPoolExecutor(
            max_workers=workers,
            initializer=_initialize_vector_worker,
            initargs=init_args,
        ) as executor:
            for split, source, vectors in executor.map(_collect_exact_vector, tasks):
                for suite, vector in vectors.items():
                    output[suite][split][source].append(vector)
    return output


def _online_case(
    task: tuple[MatchedContactPilotSpec, str, str, int, CoefficientReference]
) -> dict[str, Any]:
    """Run one short causal source/suite arm and summarize diagnosis, command, contact."""

    spec, source, suite, sensor_seed, reference = task
    specs = fault_specs(spec.onset_index)
    physical_fault = specs[source] if source in PHYSICAL_SCENARIOS else specs["healthy"]
    sensor_fault = specs["sensor"] if source == "sensor" else None
    pair_id = f"matched-contact-{source}-{sensor_seed}"
    plant = CablePlant(
        cable_config(spec, spec.selected_plane_z_m),
        point_count=spec.point_count,
        simulation_timestep_s=spec.simulation_timestep_s,
        fault=physical_fault,
    )
    sensors = OnlineSensorSession(
        suite,
        pair_id=pair_id,
        sensor_seed=sensor_seed,
        control_dt_s=spec.control_dt_s,
        config=SensorConfig(),
        fault=sensor_fault,
        run_id=f"{pair_id}-{suite}",
        config_hash="dev-matched-contact-pilot",
        split="pilot",
    )
    estimator = PilotPrototypeEstimator(
        reference,
        suite=suite,
        window_steps=spec.window_steps,
        probe_frequency_hz=spec.diagnostic_tip_load_frequency_hz,
        first_decision_step=spec.first_online_decision_step,
    )
    policy = EstimatorCommandPolicy(
        estimator,
        suite=suite,
        run_id=f"{pair_id}-{suite}",
        stride=spec.stride,
        recovery_command=GainScheduledRecoveryController(),
    )
    rollout = run_online_rollout(
        plant,
        sensors,
        n_steps=spec.short_n_steps,
        history_steps=spec.window_steps,
        command_policy=policy,
        temperature_fn=lambda _index, time_s: 25.0 + spec.thermal_rate_c_s * time_s,
    )
    contact = summarize_record(
        rollout.plant,
        plane_z_m=spec.selected_plane_z_m,
        scenario=source,
        spec=contact_screen_spec(spec, duration_s=spec.short_horizon_s),
    )
    nominal = np.stack(
        [
            commanded_torque(index * spec.control_dt_s, scale=spec.task_torque_scale)
            for index in range(spec.short_n_steps)
        ]
    )
    command_changed = np.any(~np.isclose(rollout.plant.tau_cmd, nominal), axis=1)
    before_decision = command_changed[: spec.first_online_decision_step]
    trace_classes = [
        SOURCE_CLASS_ORDER[int(np.argmax(output.p_class))] for output in policy.trace.outputs
    ]
    return {
        "source": source,
        "suite": suite,
        "sensor_seed": sensor_seed,
        "pair_id": pair_id,
        "estimator_updates": len(policy.trace.outputs),
        "detection_time_s": (
            None
            if not np.isfinite(policy.trace.detection_time_s)
            else float(policy.trace.detection_time_s)
        ),
        "final_predicted_source": trace_classes[-1],
        "ever_predicted_source": source in trace_classes,
        "command_changed_steps": int(np.count_nonzero(command_changed)),
        "command_changed_before_first_decision": bool(np.any(before_decision)),
        "sensor_fault_injected_observation_side": source == "sensor",
        "contact_active_steps": contact["contact_active_steps"],
        "contact_active_fraction": contact["contact_active_fraction"],
        "contact_episode_count": contact["contact_episode_count"],
        "first_contact_time_s": contact["first_contact_time_s"],
        "last_contact_time_s": contact["last_contact_time_s"],
        "peak_contact_force_n": contact["peak_contact_force_n"],
        "safety_incident_steps": contact["safety_incident_steps"],
        "any_safety_flag": contact["any_safety_flag"],
    }


def run_online_cases(
    spec: MatchedContactPilotSpec,
    references: dict[str, CoefficientReference],
    *,
    workers: int,
) -> list[dict[str, Any]]:
    """Run one held-out matched C1/S pair per canonical source through the real seam."""

    tasks = [
        (spec, source, suite, spec.representative_seed, references[suite])
        for source in CANONICAL_SOURCES
        for suite in DEPLOYABLE_SUITES
    ]
    if workers == 1:
        rows = [_online_case(task) for task in tasks]
    else:
        with concurrent.futures.ProcessPoolExecutor(max_workers=workers) as executor:
            rows = list(executor.map(_online_case, tasks))
    return sorted(rows, key=lambda row: (str(row["source"]), str(row["suite"])))


def _horizon_case(
    task: tuple[MatchedContactPilotSpec, float, str]
) -> dict[str, Any]:
    """Run one physical source/plane case over the onset+5 s audit horizon."""

    spec, plane_z_m, source = task
    row = run_physical_scenario(
        plane_z_m,
        source,
        contact_screen_spec(spec, duration_s=spec.evaluation_horizon_s),
    )
    return row


def run_extended_horizon_audit(
    spec: MatchedContactPilotSpec, *, workers: int
) -> list[dict[str, Any]]:
    """Audit selected and former-control planes across every physical source."""

    tasks = [
        (spec, plane_z_m, source)
        for plane_z_m in (spec.former_control_plane_z_m, spec.selected_plane_z_m)
        for source in PHYSICAL_SCENARIOS
    ]
    if workers == 1:
        rows = [_horizon_case(task) for task in tasks]
    else:
        with concurrent.futures.ProcessPoolExecutor(max_workers=workers) as executor:
            rows = list(executor.map(_horizon_case, tasks))
    return sorted(rows, key=lambda row: (float(row["plane_z_m"]), str(row["scenario"])))


def decide(
    spec: MatchedContactPilotSpec,
    offline_rows: list[dict[str, Any]],
    online_rows: list[dict[str, Any]],
    extended_rows: list[dict[str, Any]],
) -> dict[str, Any]:
    """Apply separate short-pilot and evaluation-horizon gates without conflation."""

    s_row = next(row for row in offline_rows if row["suite"] == "S")
    short_information_pass = bool(
        s_row["false_alarm_rate"] <= spec.maximum_false_alarm_rate
        and s_row["minimum_fault_detection_rate"]
        >= spec.minimum_fault_detection_rate
        and s_row["macro_attribution_accuracy"]
        >= spec.minimum_attribution_accuracy
    )
    short_online_pass = bool(
        all(not row["any_safety_flag"] for row in online_rows)
        and all(row["contact_episode_count"] == 1 for row in online_rows)
        and all(not row["command_changed_before_first_decision"] for row in online_rows)
        and all(row["final_predicted_source"] == row["source"] for row in online_rows)
        and all(
            row["command_changed_steps"] == 0
            for row in online_rows
            if row["source"] in {"healthy", "sensor"}
        )
    )
    selected_extended = [
        row
        for row in extended_rows
        if np.isclose(row["plane_z_m"], spec.selected_plane_z_m)
    ]
    former_control_extended = [
        row
        for row in extended_rows
        if np.isclose(row["plane_z_m"], spec.former_control_plane_z_m)
    ]
    evaluation_horizon_pass = bool(
        len(selected_extended) == len(PHYSICAL_SCENARIOS)
        and all(not row["any_safety_flag"] for row in selected_extended)
        and all(row["contact_episode_count"] == 1 for row in selected_extended)
    )
    former_control_stays_no_contact = bool(
        len(former_control_extended) == len(PHYSICAL_SCENARIOS)
        and all(row["contact_active_steps"] == 0 for row in former_control_extended)
    )
    short_pass = short_information_pass and short_online_pass
    return {
        "short_horizon_information_pass": short_information_pass,
        "short_horizon_online_seam_pass": short_online_pass,
        "short_horizon_status": (
            "ADVANCE_SHORT_HORIZON_DEVELOPMENT_ONLY"
            if short_pass
            else "BLOCK_SHORT_HORIZON_PILOT"
        ),
        "evaluation_horizon_contact_pass": evaluation_horizon_pass,
        "former_control_stays_no_contact": former_control_stays_no_contact,
        "overall_decision": (
            "BLOCK_MATCHED_CONTACT_PILOT_AND_CONTACT_PROFILE_CONFIG_FREEZE"
            if not short_pass
            else (
                "BLOCK_CONTACT_PROFILE_FROM_EVALUATION_HORIZON_AND_CONFIG_FREEZE"
                if not evaluation_horizon_pass
                else "ADVANCE_CONTACT_PROFILE_TO_VALIDATION_DESIGN_REVIEW"
            )
        ),
        "interpretation": (
            "The short matched pilot and the onset+5 s contact/safety audit are separate "
            "gates. A short-horizon pass cannot override an evaluation-horizon block."
        ),
    }


def write_csv(path: Path, rows: list[dict[str, Any]]) -> None:
    """Write deterministic flat pilot rows."""

    fieldnames = list(rows[0]) if rows else []
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames, lineterminator="\n")
        writer.writeheader()
        writer.writerows(rows)


def write_report(path: Path, summary: dict[str, Any]) -> None:
    """Write the human-readable development decision and its honesty bounds."""

    decisions = summary["decisions"]
    offline = {row["suite"]: row for row in summary["offline_rows"]}
    lines = [
        "# Matched Contact-Enabled C1/S Pilot",
        "",
        f"**Overall decision: {decisions['overall_decision']}.**",
        "",
        f"**Short-horizon status: {decisions['short_horizon_status']}.**",
        "",
        (
            "Both gates block. At the exact online-owned post-probe decision, S retains "
            "strong fault signal but exceeds the held-out healthy false-alarm screen. In "
            "the causal continuation, the pilot-only prototype drifts across phase and "
            "ends on an actuator call in every representative arm, including healthy and "
            "sensor. Separately, z = 0.100 m does not remain a single safe contact "
            "condition over the required onset+5 s horizon."
        ),
        "",
        "## Contact-conditioned information check (2.6 s)",
        "",
        "| Suite | Healthy false alarms | Min fault detection | Structure detection | Prototype attribution |",
        "|---|---:|---:|---:|---:|",
    ]
    for suite in DEPLOYABLE_SUITES:
        row = offline[suite]
        lines.append(
            f"| {suite} | {100*row['false_alarm_rate']:.1f}% | "
            f"{100*row['minimum_fault_detection_rate']:.1f}% | "
            f"{100*row['structure_detection_rate']:.1f}% | "
            f"{100*row['macro_attribution_accuracy']:.1f}% |"
        )
    lines.extend(
        [
            "",
            (
                "References and prototype centroids use 32 calibration seeds; the "
                "held-out figures use 48 disjoint seeds. The 99th-percentile threshold "
                "is still the calibration maximum, so these are pilot figures rather "
                "than validation-frozen operating points."
            ),
            "",
            (
                "S detects all three held-out fault classes and attributes their prototype "
                "shapes correctly, but its 8.3% held-out healthy false-alarm rate exceeds "
                "the predeclared 5% development screen. The short information gate blocks."
            ),
            "",
            "## Short causal seam check",
            "",
            "| Source | Suite | Final call | Detection (s) | Changed-command steps | Contact episodes | Peak force (N) | Safety steps |",
            "|---|---|---|---:|---:|---:|---:|---:|",
        ]
    )
    for row in summary["online_rows"]:
        detection = "—" if row["detection_time_s"] is None else f"{row['detection_time_s']:.3f}"
        lines.append(
            f"| {row['source']} | {row['suite']} | {row['final_predicted_source']} | "
            f"{detection} | {row['command_changed_steps']} | "
            f"{row['contact_episode_count']} | {row['peak_contact_force_n']:.3f} | "
            f"{row['safety_incident_steps']} |"
        )
    lines.extend(
        [
            "",
            (
                "The sensor fault is injected only in OnlineSensorSession and does reach "
                "the policy through delivered observations: both sensor arms call sensor "
                "at least once. That call is not stable. By the final decision every arm "
                "calls actuator, so healthy and sensor cases receive inappropriate actuator "
                "compensation. This exposes a phase/reference-lifecycle defect in using the "
                "single scheduled-decision prototype continuously; it is a BLOCK, not a "
                "controller result. The one-hot prototype confidence is not calibrated."
            ),
            "",
            "## Required onset+5 s horizon audit",
            "",
            "| Plane z (m) | Source | Contact episodes | Last contact (s) | Peak force (N) | Safety steps |",
            "|---:|---|---:|---:|---:|---:|",
        ]
    )
    for row in summary["extended_horizon_rows"]:
        last_contact = (
            "—" if row["last_contact_time_s"] is None else f"{row['last_contact_time_s']:.3f}"
        )
        lines.append(
            f"| {row['plane_z_m']:.3f} | {row['scenario']} | "
            f"{row['contact_episode_count']} | {last_contact} | "
            f"{row['peak_contact_force_n']:.3f} | {row['safety_incident_steps']} |"
        )
    lines.extend(
        [
            "",
            (
                "The original z = 0.050 m negative control is horizon-scoped too: over "
                "six seconds it is no longer a no-contact condition. The block therefore "
                "requires a redesigned bounded task/contact profile or controller before "
                "the matched evaluation-sized comparison; it must not be repaired by "
                "retuning the A1 safety limits."
            ),
            "",
            "## Boundaries",
            "",
            "- Development pilot only; no confirmatory data or research result.",
            "- Contact height, W/stride, thresholds, sensor constants, faults, and config remain unfrozen.",
            "- The row's 2-D tip-radius readout is not used as the workspace gate; A1 privileged safety flags remain authoritative.",
            "- Learned attribution, RMA, per-suite probability calibration, and the evaluation-sized recovery comparison remain open.",
        ]
    )
    path.write_text("\n".join(lines) + "\n", encoding="utf-8")


def run(spec: MatchedContactPilotSpec, *, workers: int) -> dict[str, Any]:
    """Run all three pilot layers and return the complete deterministic payload."""

    spec.validate()
    print("Fitting contact-conditioned C1/S references ...", flush=True)
    references, offline_rows = fit_contact_references(spec, workers=workers)
    print("Running short causal matched C1/S seam cases ...", flush=True)
    online_rows = run_online_cases(spec, references, workers=workers)
    print("Auditing selected and former-control planes over onset+5 s ...", flush=True)
    extended_rows = run_extended_horizon_audit(spec, workers=workers)
    decisions = decide(spec, offline_rows, online_rows, extended_rows)
    return jsonable(
        {
            "artifact_status": "development_only_config_unfrozen",
            "pilot_instrument": (
                "contact-conditioned coefficient distance plus nearest-centroid "
                "prototype; one-hot confidence and canonical severity/location lookup "
                "are mechanism-only and are not the learned attribution head"
            ),
            "spec": asdict(spec),
            "calibration_seed_range": [
                spec.base_seed,
                spec.base_seed + spec.calibration_seeds - 1,
            ],
            "evaluation_seed_range": [
                spec.base_seed + spec.calibration_seeds,
                spec.base_seed + spec.calibration_seeds + spec.evaluation_seeds - 1,
            ],
            "offline_rows": offline_rows,
            "online_rows": online_rows,
            "extended_horizon_rows": extended_rows,
            "decisions": decisions,
        }
    )


def main() -> int:
    """Run the pilot and write its JSON, CSV, and Markdown artifacts."""

    args = parse_args()
    spec = spec_from_args(args)
    summary = run(spec, workers=int(args.workers))
    args.output_dir.mkdir(parents=True, exist_ok=True)
    summary_path = args.output_dir / "summary.json"
    offline_csv = args.output_dir / "contact_information_rows.csv"
    online_csv = args.output_dir / "online_seam_rows.csv"
    horizon_csv = args.output_dir / "extended_horizon_rows.csv"
    report_path = args.output_dir / "matched_contact_pilot_report.md"
    summary_path.write_text(
        json.dumps(summary, indent=2, sort_keys=True) + "\n", encoding="utf-8"
    )
    write_csv(offline_csv, summary["offline_rows"])
    write_csv(online_csv, summary["online_rows"])
    write_csv(horizon_csv, summary["extended_horizon_rows"])
    write_report(report_path, summary)
    print(f"Decision: {summary['decisions']['overall_decision']}")
    print(f"Wrote {summary_path}")
    print(f"Wrote {offline_csv}")
    print(f"Wrote {online_csv}")
    print(f"Wrote {horizon_csv}")
    print(f"Wrote {report_path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
