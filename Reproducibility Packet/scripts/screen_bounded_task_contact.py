"""Screen a bounded task/contact/controller condition after the matched-pilot block.

The earlier matched contact pilot showed two separate method failures: the perpetual
open-loop task torque drifted beyond the joint-angle envelope over onset plus five
seconds, and a prototype fitted for one scheduled probe decision was incorrectly reused
as the probe left the window. This development screen corrects those mechanics without
claiming an information result:

* a low-authority PD task controller reads only delivered ``q_obs``/``qd_obs``;
* the diagnostic probe completes before a single scheduled diagnosis is made and held;
* a smooth finite contact excursion begins only after that decision, so recovery has
  authority before the safety-relevant contact; and
* the full onset-plus-five-second horizon is checked against unchanged A1 flags.

The scheduled diagnoses are fixed source-correct stand-ins used only to exercise the
controller seam. They are not a trained estimator, do not validate C1-vs-S information,
and cannot freeze the task, contact plane, controller, diagnosis lifecycle, or config.
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

from run_noisy_reference_pilot import fault_specs
from screen_optional_contact_profile import count_contact_episodes
from utils.cable_mechanics import CableModelConfig
from utils.cable_plant import CablePlant
from utils.estimator import (
    DiagnosisEstimator,
    EstimatorOutput,
    HEALTHY_INDEX,
    N_SOURCE_CLASSES,
    SOURCE_CLASS_ORDER,
)
from utils.online_loop import run_online_rollout
from utils.schema_types import N_JOINTS, ObservedRecord, SAFETY_FLAG_FIELDS
from utils.sensor_model import OnlineSensorSession, SensorConfig
from utils.task_control import (
    BoundedTaskProfile,
    EstimatorRecoveryTaskPolicy,
    ObservedJointControllerConfig,
    ObservedJointPDController,
)


CANONICAL_SOURCES = ("healthy", "structure", "actuator", "sensor")
PHYSICAL_SOURCES = ("healthy", "structure", "actuator")


@dataclass(frozen=True)
class BoundedTaskContactSpec:
    """Portable settings and predeclared selection gates for the redesign screen."""

    plane_heights_z_m: tuple[float, ...] = (0.100, 0.125, 0.150, 0.175, 0.200)
    target_joint_rad: tuple[float, float] = (0.30, 0.30)
    proportional_gain: tuple[float, float] = (0.05, 0.03)
    derivative_gain: tuple[float, float] = (0.005, 0.003)
    nominal_torque_abs_limit: tuple[float, float] = (0.20, 0.10)
    movement_start_s: float = 2.40
    transition_s: float = 0.60
    hold_end_s: float = 4.40
    return_end_s: float = 5.00
    fault_onset_s: float = 1.0
    duration_s: float = 6.0
    diagnostic_tip_load_peak_n: float = 0.05
    diagnostic_tip_load_frequency_hz: float = 0.8
    ramp_period_fraction: float = 0.125
    window_steps: int = 768
    stride: int = 16
    control_dt_s: float = 0.002
    point_count: int = 17
    simulation_timestep_s: float = 1.0e-4
    sensor_seed: int = 12000
    thermal_ramp_c_per_640_steps: float = 3.0
    minimum_contact_active_steps: int = 5
    maximum_contact_active_fraction: float = 0.05

    def validate(self) -> None:
        """Fail loudly when the screen or causal ordering is malformed."""

        heights = np.asarray(self.plane_heights_z_m, dtype=float)
        if heights.ndim != 1 or heights.size < 2 or not np.all(np.isfinite(heights)):
            raise ValueError("plane_heights_z_m must contain at least two finite values")
        if not np.all(np.diff(heights) > 0.0):
            raise ValueError("plane heights must be unique and strictly increasing")
        profile = self.task_profile()
        profile.validate()
        controller = self.controller_config()
        controller.validate()
        finite_positive = {
            "fault_onset_s": self.fault_onset_s,
            "duration_s": self.duration_s,
            "diagnostic_tip_load_frequency_hz": self.diagnostic_tip_load_frequency_hz,
            "control_dt_s": self.control_dt_s,
            "simulation_timestep_s": self.simulation_timestep_s,
        }
        for name, value in finite_positive.items():
            if not np.isfinite(value) or value <= 0.0:
                raise ValueError(f"{name} must be finite and positive")
        if not np.isfinite(self.diagnostic_tip_load_peak_n) or self.diagnostic_tip_load_peak_n < 0.0:
            raise ValueError("diagnostic_tip_load_peak_n must be finite and non-negative")
        if not 0.0 <= self.ramp_period_fraction <= 0.5:
            raise ValueError("ramp_period_fraction must lie in [0, 0.5]")
        if self.window_steps < 1 or self.stride < 1:
            raise ValueError("window_steps and stride must be positive")
        if self.point_count < 3:
            raise ValueError("point_count must be at least three")
        if self.sensor_seed < 0:
            raise ValueError("sensor_seed must be non-negative")
        if self.minimum_contact_active_steps <= 0:
            raise ValueError("minimum_contact_active_steps must be positive")
        if not 0.0 < self.maximum_contact_active_fraction < 1.0:
            raise ValueError("maximum_contact_active_fraction must lie in (0, 1)")
        for name, seconds in {
            "fault_onset_s": self.fault_onset_s,
            "duration_s": self.duration_s,
            "probe_period_s": self.probe_period_s,
            "movement_start_s": self.movement_start_s,
            "transition_s": self.transition_s,
            "hold_end_s": self.hold_end_s,
            "return_end_s": self.return_end_s,
        }.items():
            steps = seconds / self.control_dt_s
            if not math.isclose(steps, round(steps), rel_tol=0.0, abs_tol=1.0e-10):
                raise ValueError(f"{name}/control_dt_s must be an integer")
        if self.duration_s < self.fault_onset_s + 5.0:
            raise ValueError("duration_s must cover five seconds after fault onset")
        if self.first_decision_time_s >= self.movement_start_s:
            raise ValueError("the held diagnosis must precede the contact excursion")
        if self.return_end_s > self.duration_s:
            raise ValueError("the bounded task must return within the audit horizon")

    @property
    def probe_period_s(self) -> float:
        """Return one complete diagnostic period."""

        return 1.0 / self.diagnostic_tip_load_frequency_hz

    @property
    def onset_index(self) -> int:
        """Return the first physical-fault step."""

        return int(round(self.fault_onset_s / self.control_dt_s))

    @property
    def period_steps(self) -> int:
        """Return the exact one-cycle probe length in control steps."""

        return int(round(self.probe_period_s / self.control_dt_s))

    @property
    def first_decision_step(self) -> int:
        """Return the first stride decision after the complete probe is observed."""

        probe_end_index = self.onset_index + self.period_steps - 1
        after_probe = probe_end_index + 1
        return ((after_probe + self.stride - 1) // self.stride) * self.stride

    @property
    def first_decision_time_s(self) -> float:
        """Return the scheduled held-decision time."""

        return self.first_decision_step * self.control_dt_s

    @property
    def n_steps(self) -> int:
        """Return the exact onset-plus-five-second audit length."""

        return int(round(self.duration_s / self.control_dt_s))

    @property
    def thermal_rate_c_s(self) -> float:
        """Return the carried development thermal-ramp rate."""

        return self.thermal_ramp_c_per_640_steps / (640.0 * self.control_dt_s)

    def task_profile(self) -> BoundedTaskProfile:
        """Return the task profile represented by this screen specification."""

        return BoundedTaskProfile(
            target_joint_rad=self.target_joint_rad,
            movement_start_s=self.movement_start_s,
            transition_s=self.transition_s,
            hold_end_s=self.hold_end_s,
            return_end_s=self.return_end_s,
        )

    def controller_config(self) -> ObservedJointControllerConfig:
        """Return the deployable feedback settings represented by this screen."""

        return ObservedJointControllerConfig(
            proportional_gain=self.proportional_gain,
            derivative_gain=self.derivative_gain,
            torque_abs_limit=self.nominal_torque_abs_limit,
        )


def _one_hot(source: str) -> np.ndarray:
    """Return one canonical one-hot source distribution."""

    probabilities = np.zeros(N_SOURCE_CLASSES, dtype=float)
    probabilities[SOURCE_CLASS_ORDER.index(source)] = 1.0
    return probabilities


def _output_for_source(source: str, step_index: int, decision_time_s: float) -> EstimatorOutput:
    """Return the fixed source-correct stand-in used only by this mechanics screen."""

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
        unknown_score=0.0,
        abstain_decision=False,
        location_out=location,
        severity_out=severity,
        severity_uncertainty=uncertainty,
        detection_time_s=(
            float("nan") if source == "healthy" else decision_time_s
        ),
    )
    output.validate()
    return output


class FixedSourceStandIn(DiagnosisEstimator):
    """Return one fixed source-correct diagnosis when called by the hold wrapper."""

    def __init__(self, source: str) -> None:
        """Validate and retain one canonical source class."""

        if source not in CANONICAL_SOURCES:
            raise ValueError(f"source must be one of {CANONICAL_SOURCES}")
        self.source = source
        self.calls = 0

    def reset(self) -> None:
        """Reset the call counter for a fresh screen rollout."""

        self.calls = 0

    def update(
        self,
        step_index: int,
        decision_time_s: float,
        _window: ObservedRecord | None,
    ) -> EstimatorOutput:
        """Emit the configured source at the supplied causal coordinates."""

        self.calls += 1
        return _output_for_source(self.source, step_index, decision_time_s)


class SingleDecisionHoldEstimator(DiagnosisEstimator):
    """Evaluate an inner estimator once at a scheduled step and hold that decision."""

    def __init__(
        self, inner: DiagnosisEstimator, *, first_decision_step: int
    ) -> None:
        """Bind the inner estimator and the single allowed evaluation step."""

        if first_decision_step < 0:
            raise ValueError("first_decision_step must be non-negative")
        self.inner = inner
        self.first_decision_step = int(first_decision_step)
        self.reset()

    @property
    def classification_evaluations(self) -> int:
        """Return how many times the inner classifier was actually evaluated."""

        return int(self._classification_evaluations)

    def reset(self) -> None:
        """Clear the held decision and reset the inner estimator."""

        self.inner.reset()
        self._held: EstimatorOutput | None = None
        self._classification_evaluations = 0

    @staticmethod
    def _healthy(step_index: int, decision_time_s: float) -> EstimatorOutput:
        """Return the fail-safe healthy output used before the scheduled decision."""

        probabilities = np.zeros(N_SOURCE_CLASSES, dtype=float)
        probabilities[HEALTHY_INDEX] = 1.0
        output = EstimatorOutput(
            step=step_index,
            decision_time_s=decision_time_s,
            p_class=probabilities,
            unknown_score=0.0,
            abstain_decision=False,
            location_out=-1,
            severity_out=0.0,
            severity_uncertainty=float("inf"),
            detection_time_s=float("nan"),
        )
        output.validate()
        return output

    @staticmethod
    def _at_coordinates(
        held: EstimatorOutput, step_index: int, decision_time_s: float
    ) -> EstimatorOutput:
        """Reissue held diagnosis fields at the current causal coordinates."""

        output = EstimatorOutput(
            step=step_index,
            decision_time_s=decision_time_s,
            p_class=held.p_class.copy(),
            unknown_score=held.unknown_score,
            abstain_decision=held.abstain_decision,
            location_out=held.location_out,
            severity_out=held.severity_out,
            severity_uncertainty=held.severity_uncertainty,
            detection_time_s=held.detection_time_s,
        )
        output.validate()
        return output

    def update(
        self,
        step_index: int,
        decision_time_s: float,
        window: ObservedRecord | None,
    ) -> EstimatorOutput:
        """Return healthy before the gate, then one held scheduled decision."""

        if step_index < self.first_decision_step:
            return self._healthy(step_index, decision_time_s)
        if self._held is None:
            self._held = self.inner.update(step_index, decision_time_s, window)
            self._classification_evaluations += 1
        return self._at_coordinates(self._held, step_index, decision_time_s)


def parse_args() -> argparse.Namespace:
    """Parse the portable bounded-task/contact screen command line."""

    defaults = BoundedTaskContactSpec()
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--output-dir",
        type=Path,
        default=Path("results/bounded_task_contact_screen"),
    )
    parser.add_argument(
        "--plane-heights-z-m",
        type=float,
        nargs="+",
        default=list(defaults.plane_heights_z_m),
    )
    parser.add_argument("--workers", type=int, default=4)
    parser.add_argument("--sensor-seed", type=int, default=defaults.sensor_seed)
    parser.add_argument("--point-count", type=int, default=defaults.point_count)
    parser.add_argument(
        "--simulation-timestep-s", type=float, default=defaults.simulation_timestep_s
    )
    return parser.parse_args()


def spec_from_args(args: argparse.Namespace) -> BoundedTaskContactSpec:
    """Build and validate a screen specification from CLI values."""

    spec = BoundedTaskContactSpec(
        plane_heights_z_m=tuple(float(value) for value in args.plane_heights_z_m),
        sensor_seed=int(args.sensor_seed),
        point_count=int(args.point_count),
        simulation_timestep_s=float(args.simulation_timestep_s),
    )
    spec.validate()
    if int(args.workers) < 1:
        raise ValueError("workers must be at least one")
    return spec


def cable_config(spec: BoundedTaskContactSpec, plane_z_m: float) -> CableModelConfig:
    """Return the identical plant/probe/contact configuration for one arm."""

    return CableModelConfig(
        control_dt_s=spec.control_dt_s,
        task_torque_scale=0.0,
        diagnostic_tip_load_peak_n=spec.diagnostic_tip_load_peak_n,
        diagnostic_tip_load_frequency_hz=spec.diagnostic_tip_load_frequency_hz,
        diagnostic_tip_load_start_s=spec.fault_onset_s,
        diagnostic_tip_load_duration_s=spec.probe_period_s,
        diagnostic_tip_load_ramp_s=spec.probe_period_s * spec.ramp_period_fraction,
        endpoint_contact_enabled=True,
        endpoint_contact_plane_z_m=plane_z_m,
    )


def _summarize_case(
    *,
    spec: BoundedTaskContactSpec,
    plane_z_m: float,
    source: str,
    policy: EstimatorRecoveryTaskPolicy,
    estimator: SingleDecisionHoldEstimator,
    record,
) -> dict[str, Any]:
    """Summarize one source/plane arm against the predeclared screen gates."""

    active = np.asarray(record.contact_state[:, 1] == 1.0, dtype=bool)
    force = np.asarray(record.contact_state[:, 0], dtype=float)
    active_indices = np.flatnonzero(active)
    first_contact_s = (
        None if not active_indices.size else float(record.t_s[active_indices[0]])
    )
    last_contact_s = (
        None if not active_indices.size else float(record.t_s[active_indices[-1]])
    )
    nominal = np.stack(policy.nominal_commands)
    applied = np.stack(policy.commands)
    changed = np.any(~np.isclose(nominal, applied, rtol=0.0, atol=1.0e-12), axis=1)
    changed_indices = np.flatnonzero(changed)
    trace_sources = [
        SOURCE_CLASS_ORDER[int(np.argmax(output.p_class))]
        for output in policy.trace.outputs
    ]
    post_decision_sources = [
        predicted
        for output, predicted in zip(policy.trace.outputs, trace_sources)
        if output.step >= spec.first_decision_step
    ]
    flag_counts = {
        name: int(np.count_nonzero(record.safety_flag[:, index]))
        for index, name in enumerate(SAFETY_FLAG_FIELDS)
    }
    contact_active_steps = int(active_indices.size)
    contact_fraction = float(np.mean(active))
    episodes = count_contact_episodes(active)
    peak_force = float(np.max(force))
    any_safety = bool(np.any(record.safety_flag))
    changed_before_decision = bool(np.any(changed[: spec.first_decision_step]))
    first_recovery_change_s = (
        None
        if not changed_indices.size
        else float(changed_indices[0] * spec.control_dt_s)
    )
    action_expected = source in {"structure", "actuator"}
    recovery_action_gate = bool(
        (changed_indices.size > 0 and first_recovery_change_s is not None)
        if action_expected
        else changed_indices.size == 0
    )
    recovery_precedes_contact = bool(
        True
        if not action_expected
        else (
            first_recovery_change_s is not None
            and first_contact_s is not None
            and first_recovery_change_s < first_contact_s
        )
    )
    candidate_gate = bool(
        contact_active_steps >= spec.minimum_contact_active_steps
        and contact_fraction <= spec.maximum_contact_active_fraction
        and episodes == 1
        and first_contact_s is not None
        and first_contact_s >= spec.movement_start_s
        and first_contact_s > spec.first_decision_time_s
        and peak_force < CableModelConfig().tip_contact_force_limit_n
        and not any_safety
        and not changed_before_decision
        and recovery_action_gate
        and recovery_precedes_contact
        and estimator.classification_evaluations == 1
        and post_decision_sources
        and all(predicted == source for predicted in post_decision_sources)
    )
    row: dict[str, Any] = {
        "plane_z_m": float(plane_z_m),
        "source": source,
        "suite": "C1",
        "sensor_fault_is_observation_side": source == "sensor",
        "n_steps": int(record.n_steps),
        "first_decision_step": spec.first_decision_step,
        "first_decision_time_s": spec.first_decision_time_s,
        "classification_evaluations": estimator.classification_evaluations,
        "held_post_decision_source": (
            post_decision_sources[-1] if post_decision_sources else None
        ),
        "recovery_changed_steps": int(changed_indices.size),
        "recovery_changed_before_decision": changed_before_decision,
        "first_recovery_change_time_s": first_recovery_change_s,
        "recovery_precedes_contact": recovery_precedes_contact,
        "contact_active_steps": contact_active_steps,
        "contact_active_fraction": contact_fraction,
        "contact_episode_count": episodes,
        "first_contact_time_s": first_contact_s,
        "last_contact_time_s": last_contact_s,
        "peak_contact_force_n": peak_force,
        "contact_impulse_n_s": float(np.trapezoid(force, record.t_s)),
        "max_abs_joint_0_rad": float(np.max(np.abs(record.q_true[:, 0]))),
        "max_abs_joint_1_rad": float(np.max(np.abs(record.q_true[:, 1]))),
        "max_abs_joint_speed_0_rad_s": float(
            np.max(np.abs(record.qd_true[:, 0]))
        ),
        "max_abs_joint_speed_1_rad_s": float(
            np.max(np.abs(record.qd_true[:, 1]))
        ),
        "max_abs_gauge_microstrain": float(np.max(np.abs(record.gauge_true))),
        "safety_incident_steps": int(
            np.count_nonzero(np.any(record.safety_flag, axis=1))
        ),
        "any_safety_flag": any_safety,
        "bounded_profile_gate_pass": candidate_gate,
    }
    row.update({f"flag_steps_{name}": count for name, count in flag_counts.items()})
    return row


def _run_case(
    task: tuple[BoundedTaskContactSpec, float, str]
) -> dict[str, Any]:
    """Run one full-horizon source/plane arm through the real causal seam."""

    spec, plane_z_m, source = task
    specs = fault_specs(spec.onset_index)
    physical_fault = specs[source] if source in PHYSICAL_SOURCES else specs["healthy"]
    sensor_fault = specs["sensor"] if source == "sensor" else None
    pair_id = f"bounded-task-contact-{plane_z_m:.3f}-{source}"
    plant = CablePlant(
        cable_config(spec, plane_z_m),
        point_count=spec.point_count,
        simulation_timestep_s=spec.simulation_timestep_s,
        fault=physical_fault,
    )
    sensors = OnlineSensorSession(
        "C1",
        pair_id=pair_id,
        sensor_seed=spec.sensor_seed,
        control_dt_s=spec.control_dt_s,
        config=SensorConfig(),
        fault=sensor_fault,
        run_id=pair_id,
        config_hash="dev-bounded-task-contact-screen",
        split="pilot",
    )
    estimator = SingleDecisionHoldEstimator(
        FixedSourceStandIn(source), first_decision_step=spec.first_decision_step
    )
    profile = spec.task_profile()
    policy = EstimatorRecoveryTaskPolicy(
        ObservedJointPDController(profile, spec.controller_config()),
        estimator,
        suite="C1",
        run_id=pair_id,
        stride=spec.stride,
    )
    rollout = run_online_rollout(
        plant,
        sensors,
        n_steps=spec.n_steps,
        history_steps=spec.window_steps,
        command_policy=policy,
        reference_fn=profile.task_reference,
        temperature_fn=lambda _index, time_s: 25.0
        + spec.thermal_rate_c_s * time_s,
    )
    return _summarize_case(
        spec=spec,
        plane_z_m=plane_z_m,
        source=source,
        policy=policy,
        estimator=estimator,
        record=rollout.plant,
    )


def select_candidate(
    rows: list[dict[str, Any]], spec: BoundedTaskContactSpec
) -> dict[str, Any]:
    """Select the lowest all-source passing plane above a no-contact control."""

    negative_height = spec.plane_heights_z_m[0]
    negative_rows = [row for row in rows if row["plane_z_m"] == negative_height]
    negative_control_pass = bool(
        len(negative_rows) == len(CANONICAL_SOURCES)
        and all(row["contact_active_steps"] == 0 for row in negative_rows)
        and all(not row["any_safety_flag"] for row in negative_rows)
        and all(not row["recovery_changed_before_decision"] for row in negative_rows)
    )
    eligible: list[float] = []
    for height in spec.plane_heights_z_m[1:]:
        height_rows = [row for row in rows if row["plane_z_m"] == height]
        if (
            len(height_rows) == len(CANONICAL_SOURCES)
            and all(row["bounded_profile_gate_pass"] for row in height_rows)
        ):
            eligible.append(height)
    selected = eligible[0] if negative_control_pass and eligible else None
    return {
        "decision": (
            "ADVANCE_BOUNDED_TASK_CONTACT_PROFILE_TO_MATCHED_INFORMATION_REVIEW"
            if selected is not None
            else "BLOCK_BOUNDED_TASK_CONTACT_PROFILE"
        ),
        "selected_plane_z_m": selected,
        "negative_control_plane_z_m": negative_height,
        "negative_control_pass": negative_control_pass,
        "eligible_plane_heights_z_m": eligible,
        "selection_rule": (
            "lowest plane above an all-source no-contact control that yields exactly one "
            "post-decision bounded contact episode in every canonical source arm, with "
            "the source-correct held recovery action applied before contact where an "
            "action exists, no pre-decision recovery, and no A1 safety flag"
        ),
    }


def run_screen(
    spec: BoundedTaskContactSpec, *, workers: int
) -> dict[str, Any]:
    """Run the predeclared plane/source grid and return the complete result."""

    spec.validate()
    tasks = [
        (spec, plane_z_m, source)
        for plane_z_m in spec.plane_heights_z_m
        for source in CANONICAL_SOURCES
    ]
    if workers == 1:
        rows = [_run_case(task) for task in tasks]
    else:
        with concurrent.futures.ProcessPoolExecutor(max_workers=workers) as executor:
            rows = list(executor.map(_run_case, tasks))
    rows = sorted(rows, key=lambda row: (float(row["plane_z_m"]), str(row["source"])))
    selection = select_candidate(rows, spec)
    return {
        "artifact_status": "development_only_config_unfrozen",
        "screen_spec": asdict(spec),
        "task_controller_boundary": (
            "nominal task feedback consumes only delivered q_obs and qd_obs, shared by "
            "C1 and S; no privileged state, contact truth, or labels enter the task command"
        ),
        "diagnosis_boundary": (
            "fixed source-correct stand-ins are evaluated once at the first causal "
            "post-probe decision and then held; they test lifecycle/controller mechanics "
            "only and are not a trained or deployable attribution result"
        ),
        "matched_suite_constraint": (
            "the selected task/contact profile must be applied identically within each "
            "future C1/S CRN pair; this screen uses only their shared encoder channels"
        ),
        "selection": selection,
        "rows": rows,
    }


def _jsonable(value: Any) -> Any:
    """Convert NumPy/scalar containers into strict JSON-compatible values."""

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
    """Write stable scenario-level rows."""

    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(rows[0]))
        writer.writeheader()
        writer.writerows(rows)


def write_report(path: Path, summary: dict[str, Any]) -> None:
    """Write the human-readable development decision from the JSON payload."""

    selection = summary["selection"]
    selected = selection["selected_plane_z_m"]
    spec = summary["screen_spec"]
    lines = [
        "# Bounded Task / Contact / Controller Screen",
        "",
        f"**Decision:** `{selection['decision']}`",
        "",
        (
            "This screen replaces the perpetual open-loop task with low-authority "
            "encoder feedback, makes one scheduled post-probe diagnosis and holds it, "
            "then starts a finite contact excursion under controller authority. It is "
            "a mechanics/lifecycle screen, not a C1-vs-S information or control result."
        ),
        "",
        "## Causal ordering and fixed development settings",
        "",
        f"- Fault/probe onset: {spec['fault_onset_s']:.3f} s.",
        f"- Held diagnosis: step {summary['rows'][0]['first_decision_step']} "
        "(first stride after the probe).",
        f"- Contact excursion starts: {spec['movement_start_s']:.3f} s.",
        f"- Full audit: {spec['duration_s']:.3f} s = onset + 5 s.",
        "- Nominal feedback reads only delivered `q_obs` / `qd_obs`.",
        "- The fixed source-correct diagnosis stand-ins are mechanism instruments only.",
        "",
        "## Selected-plane rows",
        "",
        "| Source | Contact steps | Episodes | First contact (s) | Peak force (N) | Recovery-changed steps | A1 safety steps |",
        "|---|---:|---:|---:|---:|---:|---:|",
    ]
    selected_rows = (
        [] if selected is None else [row for row in summary["rows"] if row["plane_z_m"] == selected]
    )
    for row in selected_rows:
        first = "—" if row["first_contact_time_s"] is None else f"{row['first_contact_time_s']:.3f}"
        lines.append(
            f"| {row['source']} | {row['contact_active_steps']} | "
            f"{row['contact_episode_count']} | {first} | "
            f"{row['peak_contact_force_n']:.3f} | {row['recovery_changed_steps']} | "
            f"{row['safety_incident_steps']} |"
        )
    lines.extend(
        [
            "",
            "## Full plane bracket",
            "",
            "| Plane z (m) | Source | Contact steps | Episodes | Safety steps | Gate |",
            "|---:|---|---:|---:|---:|---|",
        ]
    )
    for row in summary["rows"]:
        lines.append(
            f"| {row['plane_z_m']:.3f} | {row['source']} | "
            f"{row['contact_active_steps']} | {row['contact_episode_count']} | "
            f"{row['safety_incident_steps']} | "
            f"{'PASS' if row['bounded_profile_gate_pass'] else 'BLOCK'} |"
        )
    lines.extend(
        [
            "",
            "## Interpretation boundary",
            "",
            (
                "An advancing plane means only that this bounded feedback/contact setup "
                "is safe enough to enter matched information/reference-lifecycle review. "
                "The classifier stand-ins use known development sources, so this artifact "
                "does not establish attribution, tracking recovery, a suite advantage, or "
                "a frozen configuration. The noisy held-decision information gate, "
                "validation-sized calibration, learned head/RMA, and evaluation-sized "
                "paired C1/S comparison remain open."
            ),
        ]
    )
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text("\n".join(lines) + "\n", encoding="utf-8")


def main() -> int:
    """Run the screen and write deterministic JSON, CSV, and Markdown outputs."""

    args = parse_args()
    spec = spec_from_args(args)
    print("Running bounded task/contact/controller grid ...", flush=True)
    summary = run_screen(spec, workers=int(args.workers))
    args.output_dir.mkdir(parents=True, exist_ok=True)
    summary_path = args.output_dir / "summary.json"
    csv_path = args.output_dir / "bounded_task_contact_rows.csv"
    report_path = args.output_dir / "bounded_task_contact_report.md"
    summary_path.write_text(
        json.dumps(_jsonable(summary), indent=2, allow_nan=False) + "\n",
        encoding="utf-8",
    )
    write_csv(csv_path, summary["rows"])
    write_report(report_path, summary)
    print(f"Decision: {summary['selection']['decision']}", flush=True)
    print(f"Wrote {summary_path}", flush=True)
    print(f"Wrote {csv_path}", flush=True)
    print(f"Wrote {report_path}", flush=True)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
