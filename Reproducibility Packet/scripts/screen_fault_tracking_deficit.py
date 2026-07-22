"""Screen whether any admissible fault setting opens control-layer headroom.

The structural-action screen showed that its bounded development condition carries
essentially no structural tracking deficit, so no source-specific action could recover
the Claim Sheet's required 10 percent.  This development-only screen therefore runs
before any further action design.  It keeps the approved bounded task, contact plane,
observed-state controller, probe, and no-recovery lifecycle fixed while sweeping only
the remaining-stiffness and remaining-actuator-gain fractions.

Dedicated tuning seeds select the mildest fault setting whose paired no-action tracking
deficit is large enough to *admit* the Claim Sheet's 10 percent reduction plus a
predeclared margin on every seed.  Deficit and reduction do not share a denominator, so
the gate converts the reduction target into deficit units rather than comparing the two
directly; see ``FaultTrackingDeficitSpec.required_deficit_pct``.  Disjoint
assessment seeds must reproduce that headroom with zero A1 safety incidents, zero
saturation, no recovery action, and exact paired pre-fault histories.  A fixed encoder-
bias case is retained as an observation-side healthy-plant control.  This is not an
attribution, recovery, or confirmatory result, and it does not freeze any setting.
"""

from __future__ import annotations

import argparse
import concurrent.futures
import csv
import hashlib
import json
from dataclasses import asdict, dataclass
from pathlib import Path
from typing import Any

import numpy as np

from screen_bounded_task_contact import (
    BoundedTaskContactSpec,
    FixedSourceStandIn,
    SingleDecisionHoldEstimator,
    cable_config,
)
from screen_optional_contact_profile import count_contact_episodes
from utils.cable_plant import CablePlant
from utils.metrics import j_5s
from utils.online_loop import run_online_rollout
from utils.schema_types import FaultSpec, SAFETY_FLAG_FIELDS
from utils.sensor_model import OnlineSensorSession, SensorConfig
from utils.task_control import EstimatorRecoveryTaskPolicy, ObservedJointPDController


SCREENED_SOURCES = ("structure", "actuator")


@dataclass(frozen=True)
class FaultDeficitCase:
    """One healthy, physical-fault, or observation-side control condition."""

    case_id: str
    source_class: str
    subtype: str
    location: int
    severity: float
    severity_semantics: str

    def validate(self) -> None:
        """Fail loudly when the case cannot map to the shared fault boundary."""

        if not self.case_id:
            raise ValueError("case_id cannot be empty")
        if self.source_class not in {"healthy", "structure", "actuator", "sensor"}:
            raise ValueError("unsupported source_class")
        if not np.isfinite(self.severity):
            raise ValueError("severity must be finite")
        if self.source_class in SCREENED_SOURCES and not 0.0 < self.severity < 1.0:
            raise ValueError("physical remaining fractions must lie strictly in (0,1)")
        if self.source_class == "sensor" and self.severity <= 0.0:
            raise ValueError("sensor-control severity must be positive")
        if self.source_class == "healthy" and self.severity != 1.0:
            raise ValueError("healthy severity must be the 1.0 remaining-fraction reference")
        if not self.severity_semantics:
            raise ValueError("severity_semantics cannot be empty")


@dataclass(frozen=True)
class FaultTrackingDeficitSpec:
    """Role-separated severity grid and predeclared control-headroom gate."""

    tuning_seed_start: int = 16000
    tuning_seed_count: int = 3
    assessment_seed_start: int = 16100
    assessment_seed_count: int = 4
    selected_plane_z_m: float = 0.200
    claim_tracking_bar_pct: float = 10.0
    development_margin_pct: float = 2.0
    structural_ei_remaining_grid: tuple[float, ...] = (0.75, 0.50, 0.25, 0.10, 0.05)
    actuator_gain_remaining_grid: tuple[float, ...] = (0.85, 0.70, 0.50, 0.25, 0.10)
    sensor_encoder_bias_rad: float = 0.05

    @property
    def required_reduction_pct(self) -> float:
        """Return the reduction target: the Claim Sheet bar plus the margin."""

        return self.claim_tracking_bar_pct + self.development_margin_pct

    @property
    def required_deficit_pct(self) -> float:
        """Return the no-action deficit that admits the required reduction.

        The Claim Sheet's control bar is a *reduction* measured against the degraded
        arm (``100 * (J_C1 - J_S) / J_C1``), while this screen measures a *deficit*
        against the healthy arm (``100 * (J_fault - J_healthy) / J_healthy``).  The two
        do not share a denominator.  A source-specific action that restores healthy
        tracking exactly converts a deficit ``D`` into a reduction ``D / (1 + D)``, so
        gating the deficit at the reduction target under-delivers that target: a 12%
        deficit admits at most a 10.71% reduction, which turns a predeclared 2-point
        margin over a 10% bar into 0.71 points.  Inverting the relation, ``R / (1 - R)``,
        makes the gate deliver the reduction it names.
        """

        required = self.required_reduction_pct / 100.0
        return float(100.0 * required / (1.0 - required))

    @property
    def tuning_seeds(self) -> tuple[int, ...]:
        """Return the contiguous tuning-only sensor-seed role."""

        return tuple(
            range(self.tuning_seed_start, self.tuning_seed_start + self.tuning_seed_count)
        )

    @property
    def assessment_seeds(self) -> tuple[int, ...]:
        """Return the disjoint post-selection assessment sensor-seed role."""

        return tuple(
            range(
                self.assessment_seed_start,
                self.assessment_seed_start + self.assessment_seed_count,
            )
        )

    @property
    def healthy_case(self) -> FaultDeficitCase:
        """Return the paired healthy no-fault reference."""

        return FaultDeficitCase(
            "healthy_reference",
            "healthy",
            "none",
            -1,
            1.0,
            "no fault; remaining fraction reference",
        )

    @property
    def sensor_control_case(self) -> FaultDeficitCase:
        """Return the fixed observation-side encoder-bias control."""

        return FaultDeficitCase(
            "sensor_encoder_bias_0p05",
            "sensor",
            "encoder_bias",
            0,
            self.sensor_encoder_bias_rad,
            "encoder bias in radians; physical plant remains healthy",
        )

    @staticmethod
    def _case_id(prefix: str, remaining_fraction: float) -> str:
        """Return a stable identifier for one remaining-fraction setting."""

        suffix = f"{remaining_fraction:.2f}".replace(".", "p")
        return f"{prefix}_{suffix}"

    def candidate_cases(self, source: str) -> tuple[FaultDeficitCase, ...]:
        """Return the predeclared physical severity grid for one source."""

        if source == "structure":
            return tuple(
                FaultDeficitCase(
                    self._case_id("structure_ei_remaining", value),
                    "structure",
                    "link_stiffness_loss",
                    1,
                    value,
                    "remaining link-2 EI fraction; lower is more severe",
                )
                for value in self.structural_ei_remaining_grid
            )
        if source == "actuator":
            return tuple(
                FaultDeficitCase(
                    self._case_id("actuator_gain_remaining", value),
                    "actuator",
                    "actuator_gain_loss",
                    1,
                    value,
                    "remaining joint-1 delivered-gain fraction; lower is more severe",
                )
                for value in self.actuator_gain_remaining_grid
            )
        raise ValueError(f"no candidate grid for source {source!r}")

    @property
    def all_cases(self) -> tuple[FaultDeficitCase, ...]:
        """Return healthy, both physical grids, and the fixed sensor control."""

        return (
            self.healthy_case,
            *self.candidate_cases("structure"),
            *self.candidate_cases("actuator"),
            self.sensor_control_case,
        )

    def mechanics_spec(self, sensor_seed: int) -> BoundedTaskContactSpec:
        """Return the approved bounded condition with one sensor seed."""

        return BoundedTaskContactSpec(
            plane_heights_z_m=(0.100, self.selected_plane_z_m),
            sensor_seed=sensor_seed,
        )

    def validate(self) -> None:
        """Fail loudly on overlapping roles, malformed grids, or a weak gate."""

        if self.tuning_seed_count < 1 or self.assessment_seed_count < 1:
            raise ValueError("both seed roles must contain at least one seed")
        if min(self.tuning_seed_start, self.assessment_seed_start) < 0:
            raise ValueError("sensor seeds must be non-negative")
        if set(self.tuning_seeds) & set(self.assessment_seeds):
            raise ValueError("tuning and assessment sensor roles must be disjoint")
        if not np.isfinite(self.selected_plane_z_m):
            raise ValueError("selected_plane_z_m must be finite")
        if not np.isfinite(self.claim_tracking_bar_pct) or self.claim_tracking_bar_pct <= 0.0:
            raise ValueError("claim_tracking_bar_pct must be finite and positive")
        if not np.isfinite(self.development_margin_pct) or self.development_margin_pct <= 0.0:
            raise ValueError("development_margin_pct must be finite and positive")
        if self.required_reduction_pct >= 100.0:
            raise ValueError(
                "bar plus margin must stay below a 100% reduction to convert to a deficit"
            )
        for name, grid in (
            ("structural_ei_remaining_grid", self.structural_ei_remaining_grid),
            ("actuator_gain_remaining_grid", self.actuator_gain_remaining_grid),
        ):
            values = np.asarray(grid, dtype=float)
            if values.ndim != 1 or values.size < 2 or not np.all(np.isfinite(values)):
                raise ValueError(f"{name} must contain at least two finite values")
            if not np.all((values > 0.0) & (values < 1.0)):
                raise ValueError(f"{name} values must lie strictly in (0,1)")
            if not np.all(np.diff(values) < 0.0):
                raise ValueError(f"{name} must be strictly descending from mild to severe")
        cases = self.all_cases
        for case in cases:
            case.validate()
        identifiers = [case.case_id for case in cases]
        if len(set(identifiers)) != len(identifiers):
            raise ValueError("case identifiers must be unique")
        self.mechanics_spec(self.tuning_seeds[0]).validate()


def parse_args() -> argparse.Namespace:
    """Parse the portable deficit-screen command line."""

    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--output-dir",
        type=Path,
        default=Path("results/fault_tracking_deficit_screen"),
    )
    parser.add_argument("--workers", type=int, default=8)
    return parser.parse_args()


def _hash_arrays(named_arrays: list[tuple[str, np.ndarray]]) -> str:
    """Return a stable digest over named array shape, dtype, and exact bytes."""

    digest = hashlib.sha256()
    for name, values in named_arrays:
        array = np.ascontiguousarray(values)
        digest.update(name.encode("utf-8"))
        digest.update(str(array.shape).encode("ascii"))
        digest.update(str(array.dtype).encode("ascii"))
        digest.update(array.tobytes())
    return digest.hexdigest()


def _faults_for_case(
    case: FaultDeficitCase, onset_index: int
) -> tuple[FaultSpec, FaultSpec | None]:
    """Return plant-side and observation-side faults without crossing boundaries."""

    case.validate()
    if case.source_class == "healthy":
        return FaultSpec(), None
    if case.source_class == "sensor":
        sensor_fault = FaultSpec(
            source_class="sensor",
            subtype=case.subtype,
            location=case.location,
            severity=case.severity,
            onset_index=onset_index,
        )
        sensor_fault.validate()
        return FaultSpec(), sensor_fault
    plant_fault = FaultSpec(
        source_class=case.source_class,
        subtype=case.subtype,
        location=case.location,
        severity=case.severity,
        onset_index=onset_index,
    )
    plant_fault.validate()
    return plant_fault, None


def _run_case(
    task: tuple[FaultTrackingDeficitSpec, str, int, FaultDeficitCase]
) -> dict[str, Any]:
    """Run one no-recovery fault setting through the approved bounded causal seam."""

    screen, role, sensor_seed, case = task
    mechanics = screen.mechanics_spec(sensor_seed)
    plant_fault, sensor_fault = _faults_for_case(case, mechanics.onset_index)
    pair_id = f"fault-deficit-{role}-{sensor_seed}"
    run_id = f"{pair_id}-{case.case_id}"
    plant = CablePlant(
        cable_config(mechanics, screen.selected_plane_z_m),
        point_count=mechanics.point_count,
        simulation_timestep_s=mechanics.simulation_timestep_s,
        fault=plant_fault,
    )
    sensors = OnlineSensorSession(
        "C1",
        pair_id=pair_id,
        sensor_seed=sensor_seed,
        control_dt_s=mechanics.control_dt_s,
        config=SensorConfig(),
        fault=sensor_fault,
        run_id=run_id,
        config_hash="dev-fault-tracking-deficit-screen",
        split=role,
    )
    estimator = SingleDecisionHoldEstimator(
        FixedSourceStandIn("healthy"),
        first_decision_step=mechanics.first_decision_step,
    )
    profile = mechanics.task_profile()
    policy = EstimatorRecoveryTaskPolicy(
        ObservedJointPDController(profile, mechanics.controller_config()),
        estimator,
        suite="C1",
        run_id=run_id,
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
    nominal = np.stack(policy.nominal_commands)
    applied = np.stack(policy.commands)
    changed = np.any(~np.isclose(nominal, applied, rtol=0.0, atol=1.0e-12), axis=1)
    prefault = slice(0, mechanics.onset_index)
    shared_names = ("q_obs", "qd_obs", "tau_cmd", "current_proxy_obs", "imu_obs")
    pre_fault_hash = _hash_arrays(
        [
            ("q_true", rollout.plant.q_true[prefault]),
            ("qd_true", rollout.plant.qd_true[prefault]),
            ("tau_cmd", rollout.plant.tau_cmd[prefault]),
        ]
        + [
            (f"values/{name}", rollout.observations.values[name][prefault])
            for name in shared_names
        ]
        + [
            (f"mask/{name}", rollout.observations.valid_mask[name][prefault])
            for name in shared_names
        ]
    )
    active = np.asarray(rollout.plant.contact_state[:, 1] == 1.0, dtype=bool)
    force = np.asarray(rollout.plant.contact_state[:, 0], dtype=float)
    flag_counts = {
        name: int(np.count_nonzero(rollout.plant.safety_flag[:, index]))
        for index, name in enumerate(SAFETY_FLAG_FIELDS)
    }
    row: dict[str, Any] = {
        "role": role,
        "case_id": case.case_id,
        "source_class": case.source_class,
        "subtype": case.subtype,
        "location": case.location,
        "severity": case.severity,
        "severity_semantics": case.severity_semantics,
        "sensor_seed": sensor_seed,
        "pair_id": pair_id,
        "classification_evaluations": estimator.classification_evaluations,
        "recovery_command_changed_steps": int(np.count_nonzero(changed)),
        "recovery_changed_before_decision": bool(
            np.any(changed[: mechanics.first_decision_step])
        ),
        "tracking_integral_5s_m_s": j_5s(
            rollout.plant.t_s,
            rollout.plant.task_reference,
            rollout.plant.true_task_output,
            mechanics.fault_onset_s,
        ),
        "safety_incident_steps": int(
            np.count_nonzero(np.any(rollout.plant.safety_flag, axis=1))
        ),
        "saturation_steps": int(
            np.count_nonzero(np.any(rollout.plant.saturation_flag, axis=1))
        ),
        "contact_episode_count": count_contact_episodes(active),
        "contact_active_steps": int(np.count_nonzero(active)),
        "peak_contact_force_n": float(np.max(force)),
        "max_abs_joint_0_rad": float(np.max(np.abs(rollout.plant.q_true[:, 0]))),
        "max_abs_joint_1_rad": float(np.max(np.abs(rollout.plant.q_true[:, 1]))),
        "max_abs_joint_speed_0_rad_s": float(
            np.max(np.abs(rollout.plant.qd_true[:, 0]))
        ),
        "max_abs_joint_speed_1_rad_s": float(
            np.max(np.abs(rollout.plant.qd_true[:, 1]))
        ),
        "max_abs_gauge_microstrain": float(
            np.max(np.abs(rollout.plant.gauge_true))
        ),
        "pre_fault_hash": pre_fault_hash,
    }
    row.update({f"flag_steps_{name}": count for name, count in flag_counts.items()})
    return row


def _paired_deficits(
    rows: list[dict[str, Any]], healthy_case_id: str
) -> dict[str, list[float]]:
    """Return per-case tracking deficits against seed-paired healthy references."""

    baselines: dict[int, dict[str, Any]] = {}
    for row in rows:
        if row["case_id"] != healthy_case_id:
            continue
        seed = int(row["sensor_seed"])
        if seed in baselines:
            raise ValueError(f"duplicate healthy baseline for seed {seed}")
        baselines[seed] = row
    deficits: dict[str, list[float]] = {}
    for row in rows:
        seed = int(row["sensor_seed"])
        baseline = baselines.get(seed)
        if baseline is None:
            raise ValueError(f"missing healthy baseline for seed {seed}")
        if row["pre_fault_hash"] != baseline["pre_fault_hash"]:
            raise ValueError(f"pre-fault CRN mismatch for {row['case_id']} / seed {seed}")
        baseline_j = float(baseline["tracking_integral_5s_m_s"])
        if not np.isfinite(baseline_j) or baseline_j <= 0.0:
            raise ValueError("healthy baseline J_5s must be finite and positive")
        case_j = float(row["tracking_integral_5s_m_s"])
        if not np.isfinite(case_j) or case_j < 0.0:
            raise ValueError("case J_5s must be finite and non-negative")
        deficits.setdefault(str(row["case_id"]), []).append(
            100.0 * (case_j - baseline_j) / baseline_j
        )
    return deficits


def _healthy_baseline_gates(
    rows: list[dict[str, Any]], healthy_case_id: str, expected_seed_count: int
) -> tuple[bool, bool]:
    """Return lifecycle and safety gates for the paired healthy denominator rows.

    Every deficit is measured against these rows. A healthy baseline that itself
    received recovery, evaluated more than once, saturated, or raised an A1 flag
    cannot support any candidate even when the corresponding fault arm is clean.

    Args:
        rows: Complete rows from one seed role.
        healthy_case_id: Identifier of the paired no-fault reference.
        expected_seed_count: Required number of healthy denominator rows.

    Returns:
        ``(lifecycle_pass, safety_and_saturation_pass)`` for the baseline role.
    """

    baselines = [row for row in rows if row["case_id"] == healthy_case_id]
    lifecycle_pass = bool(
        len(baselines) == expected_seed_count
        and all(row["classification_evaluations"] == 1 for row in baselines)
        and all(row["recovery_command_changed_steps"] == 0 for row in baselines)
        and all(not row["recovery_changed_before_decision"] for row in baselines)
    )
    safety_pass = bool(
        len(baselines) == expected_seed_count
        and all(row["safety_incident_steps"] == 0 for row in baselines)
        and all(row["saturation_steps"] == 0 for row in baselines)
    )
    return lifecycle_pass, safety_pass


def summarize_role(
    spec: FaultTrackingDeficitSpec,
    rows: list[dict[str, Any]],
    *,
    expected_seed_count: int,
) -> tuple[dict[str, str | None], list[dict[str, Any]]]:
    """Summarize every physical severity and select the mildest passing setting."""

    deficits = _paired_deficits(rows, spec.healthy_case.case_id)
    baseline_lifecycle_pass, baseline_safety_pass = _healthy_baseline_gates(
        rows, spec.healthy_case.case_id, expected_seed_count
    )
    summaries: list[dict[str, Any]] = []
    selected: dict[str, str | None] = {source: None for source in SCREENED_SOURCES}
    for source in SCREENED_SOURCES:
        for case in spec.candidate_cases(source):
            case_rows = [row for row in rows if row["case_id"] == case.case_id]
            values = deficits.get(case.case_id, [])
            lifecycle_pass = bool(
                baseline_lifecycle_pass
                and
                len(case_rows) == expected_seed_count
                and len(values) == expected_seed_count
                and all(row["classification_evaluations"] == 1 for row in case_rows)
                and all(
                    row["recovery_command_changed_steps"] == 0 for row in case_rows
                )
                and all(
                    not row["recovery_changed_before_decision"] for row in case_rows
                )
            )
            safety_pass = bool(
                baseline_safety_pass
                and
                len(case_rows) == expected_seed_count
                and all(row["safety_incident_steps"] == 0 for row in case_rows)
                and all(row["saturation_steps"] == 0 for row in case_rows)
            )
            headroom_pass = bool(
                len(values) == expected_seed_count
                and min(values) >= spec.required_deficit_pct
            )
            summaries.append(
                {
                    "source_class": source,
                    "case_id": case.case_id,
                    "severity": case.severity,
                    "mean_tracking_deficit_pct": float(np.mean(values)),
                    "minimum_tracking_deficit_pct": float(min(values)),
                    "maximum_tracking_deficit_pct": float(max(values)),
                    "lifecycle_pass": lifecycle_pass,
                    "safety_and_saturation_pass": safety_pass,
                    "headroom_gate_pass": headroom_pass,
                    "candidate_gate_pass": bool(
                        lifecycle_pass and safety_pass and headroom_pass
                    ),
                }
            )
        eligible = [
            row
            for row in summaries
            if row["source_class"] == source and row["candidate_gate_pass"]
        ]
        if eligible:
            mildest = max(
                eligible,
                key=lambda row: (
                    row["severity"],
                    row["minimum_tracking_deficit_pct"],
                ),
            )
            selected[source] = str(mildest["case_id"])
    return selected, summaries


def _control_summary(
    spec: FaultTrackingDeficitSpec,
    rows: list[dict[str, Any]],
    case: FaultDeficitCase,
    *,
    expected_seed_count: int,
) -> dict[str, Any]:
    """Return paired deficit and safety readouts for a non-selected control case."""

    deficits = _paired_deficits(rows, spec.healthy_case.case_id)
    baseline_lifecycle_pass, baseline_safety_pass = _healthy_baseline_gates(
        rows, spec.healthy_case.case_id, expected_seed_count
    )
    case_rows = [row for row in rows if row["case_id"] == case.case_id]
    values = deficits[case.case_id]
    return {
        "case_id": case.case_id,
        "source_class": case.source_class,
        "severity": case.severity,
        "mean_tracking_deficit_pct": float(np.mean(values)),
        "minimum_tracking_deficit_pct": float(min(values)),
        "maximum_tracking_deficit_pct": float(max(values)),
        "complete_and_paired": bool(
            len(case_rows) == expected_seed_count and len(values) == expected_seed_count
        ),
        "lifecycle_pass": bool(
            baseline_lifecycle_pass
            and
            len(case_rows) == expected_seed_count
            and all(row["classification_evaluations"] == 1 for row in case_rows)
            and all(row["recovery_command_changed_steps"] == 0 for row in case_rows)
            and all(not row["recovery_changed_before_decision"] for row in case_rows)
        ),
        "safety_and_saturation_pass": bool(
            baseline_safety_pass
            and
            all(row["safety_incident_steps"] == 0 for row in case_rows)
            and all(row["saturation_steps"] == 0 for row in case_rows)
        ),
    }


def decide(
    spec: FaultTrackingDeficitSpec,
    tuning_selected: dict[str, str | None],
    assessment_summaries: list[dict[str, Any]],
) -> dict[str, Any]:
    """Apply disjoint assessment only to the tuning-selected per-source settings."""

    assessment_by_id = {row["case_id"]: row for row in assessment_summaries}
    source_results: dict[str, dict[str, Any]] = {}
    advancing_sources: list[str] = []
    for source in SCREENED_SOURCES:
        selected_id = tuning_selected[source]
        selected_summary = (
            assessment_by_id.get(selected_id) if selected_id is not None else None
        )
        assessment_pass = bool(
            selected_summary is not None and selected_summary["candidate_gate_pass"]
        )
        if assessment_pass:
            advancing_sources.append(source)
        source_results[source] = {
            "selected_case_id": selected_id,
            "tuning_gate_pass": selected_id is not None,
            "assessment_gate_pass": assessment_pass,
            "assessment_mean_tracking_deficit_pct": (
                None
                if selected_summary is None
                else selected_summary["mean_tracking_deficit_pct"]
            ),
            "assessment_minimum_tracking_deficit_pct": (
                None
                if selected_summary is None
                else selected_summary["minimum_tracking_deficit_pct"]
            ),
        }
    advancing = set(advancing_sources)
    if advancing == {"structure", "actuator"}:
        overall = "ADVANCE_STRUCTURE_AND_ACTUATOR_DEFICIT_CONDITIONS_TO_ACTION_SCREEN"
    elif advancing == {"structure"}:
        overall = "ADVANCE_STRUCTURAL_DEFICIT_ONLY_BLOCK_ACTUATOR_DEFICIT"
    elif advancing == {"actuator"}:
        overall = "ADVANCE_ACTUATOR_DEFICIT_ONLY_BLOCK_STRUCTURAL_DEFICIT"
    else:
        overall = "BLOCK_FAULT_TRACKING_DEFICIT_GRID"
    return {
        "required_tracking_reduction_pct": spec.required_reduction_pct,
        "required_tracking_deficit_pct": spec.required_deficit_pct,
        "source_results": source_results,
        "advancing_sources": advancing_sources,
        "overall_decision": overall,
    }


def run(spec: FaultTrackingDeficitSpec, *, workers: int) -> dict[str, Any]:
    """Run the complete role-separated severity grid and apply the headroom gate."""

    spec.validate()
    if workers < 1:
        raise ValueError("workers must be positive")

    def run_role(role: str, seeds: tuple[int, ...]) -> list[dict[str, Any]]:
        tasks = [(spec, role, seed, case) for seed in seeds for case in spec.all_cases]
        print(f"Running {len(tasks)} {role} no-recovery deficit arms ...", flush=True)
        if workers == 1:
            output = [_run_case(task) for task in tasks]
        else:
            with concurrent.futures.ProcessPoolExecutor(max_workers=workers) as executor:
                output = list(executor.map(_run_case, tasks))
        output.sort(key=lambda row: (row["sensor_seed"], row["case_id"]))
        return output

    tuning_rows = run_role("tuning", spec.tuning_seeds)
    tuning_selected, tuning_summaries = summarize_role(
        spec, tuning_rows, expected_seed_count=spec.tuning_seed_count
    )
    assessment_rows = run_role("assessment", spec.assessment_seeds)
    _, assessment_summaries = summarize_role(
        spec, assessment_rows, expected_seed_count=spec.assessment_seed_count
    )
    decision = decide(spec, tuning_selected, assessment_summaries)
    return {
        "artifact_status": "development_only_config_unfrozen",
        "screen_spec": asdict(spec),
        "mechanics_spec": asdict(spec.mechanics_spec(spec.tuning_seeds[0])),
        "case_grid": [asdict(case) for case in spec.all_cases],
        "tuning_role": {
            "sensor_seeds": list(spec.tuning_seeds),
            "purpose": "select the mildest per-source setting without assessment leakage",
        },
        "assessment_role": {
            "sensor_seeds": list(spec.assessment_seeds),
            "purpose": "disjointly verify the tuning-selected headroom and all grid readouts",
        },
        "tuning_selected": tuning_selected,
        "tuning_candidate_summaries": tuning_summaries,
        "assessment_candidate_summaries": assessment_summaries,
        "tuning_sensor_control": _control_summary(
            spec,
            tuning_rows,
            spec.sensor_control_case,
            expected_seed_count=spec.tuning_seed_count,
        ),
        "assessment_sensor_control": _control_summary(
            spec,
            assessment_rows,
            spec.sensor_control_case,
            expected_seed_count=spec.assessment_seed_count,
        ),
        "tuning_rows": tuning_rows,
        "assessment_rows": assessment_rows,
        "decision": decision,
        "evidence_boundary": (
            "no-recovery severity sensitivity on one bounded development task; this is "
            "not noisy attribution, action efficacy, validation-sized evidence, or "
            "permission to freeze the fault grid, task, controller, or config"
        ),
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
    """Write deterministic CSV rows using the first row's field order."""

    if not rows:
        raise ValueError("cannot write an empty CSV")
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(rows[0]))
        writer.writeheader()
        writer.writerows(rows)


def _ceiling_reduction_pct(deficit_pct: float) -> float:
    """Convert a no-action deficit into the reduction an exact restoration would give.

    Args:
        deficit_pct: ``100 * (J_fault - J_healthy) / J_healthy``.

    Returns:
        ``100 * (J_fault - J_healthy) / J_fault``, the Claim Sheet's own quantity for an
        action that restores healthy tracking exactly.
    """

    fraction = deficit_pct / 100.0
    return float(100.0 * fraction / (1.0 + fraction))


def _scope_lines(summary: dict[str, Any]) -> list[str]:
    """Return the generated bounds on what the recorded headroom licenses.

    Every figure is recomputed from the recorded rows and summaries so the section
    regenerates deterministically from ``summary.json``.

    Args:
        summary: The complete run summary.

    Returns:
        Markdown lines for the scope section.
    """

    decision = summary["decision"]
    assessment = {
        row["case_id"]: row for row in summary["assessment_candidate_summaries"]
    }
    bar = summary["screen_spec"]["claim_tracking_bar_pct"]
    lines = ["", "## What the recorded headroom does and does not license", ""]
    for source in SCREENED_SOURCES:
        result = decision["source_results"][source]
        case_id = result["selected_case_id"]
        if case_id is None or not result["assessment_gate_pass"]:
            continue
        mean_ceiling = _ceiling_reduction_pct(assessment[case_id]["mean_tracking_deficit_pct"])
        min_ceiling = _ceiling_reduction_pct(
            assessment[case_id]["minimum_tracking_deficit_pct"]
        )
        lines.append(
            f"- **Headroom is a ceiling, not a result.** `{case_id}` carries a "
            f"{assessment[case_id]['mean_tracking_deficit_pct']:.2f}% mean / "
            f"{assessment[case_id]['minimum_tracking_deficit_pct']:.2f}% minimum no-action "
            f"deficit, so an action that restored healthy tracking exactly would score a "
            f"{mean_ceiling:.2f}% / {min_ceiling:.2f}% reduction — "
            f"{min_ceiling - bar:+.2f} percentage points over the {bar:.1f}% bar at the "
            "worst seed. Any real action recovers less than all of the deficit, so this "
            "is the most a source-specific recovery on this setting can be worth."
        )
    lines.append(
        "- **Reduction beyond that ceiling is command authority, not recovery.** An "
        "action can beat the ceiling only by tracking better than the healthy arm, which "
        "is generic under-authority being collected rather than a fault being reversed. "
        "The structural action-family screen already recorded that outcome as "
        "`BLOCK_STRUCTURAL_RECOVERY_ACTION_FAMILY`, so the same standard applies here: "
        "an actuator action must be compared against a healthy false-authorization arm "
        "and credited only with the margin above it."
    )
    rows = summary["assessment_rows"]
    structural = [
        case for case in summary["case_grid"] if case["source_class"] == "structure"
    ]
    if structural:
        pieces = []
        for case in structural:
            gauges = [
                float(row["max_abs_gauge_microstrain"])
                for row in rows
                if row["case_id"] == case["case_id"]
            ]
            deficit = assessment[case["case_id"]]["mean_tracking_deficit_pct"]
            pieces.append(
                f"{case['severity']:.2f} EI → {sum(gauges) / len(gauges):.1f} µε / "
                f"{deficit:+.2f}%"
            )
        healthy_gauges = [
            float(row["max_abs_gauge_microstrain"])
            for row in rows
            if row["source_class"] == "healthy"
        ]
        lines.append(
            "- **The structural block is not a weak signal; it is a strong signal with "
            "nowhere to act.** Mean peak |gauge| and mean tracking deficit move in "
            "opposite directions across the same sweep (healthy "
            f"{sum(healthy_gauges) / len(healthy_gauges):.1f} µε; "
            + "; ".join(pieces)
            + "). The strain channel grows monotonically with severity while the "
            "tracking deficit falls to zero and then turns negative, which is the "
            "diagnostic-only shape Slot 13 reserves rather than a sensing failure."
        )
    lines.append(
        "- **No-action headroom is not S-over-C1 headroom.** The contract's control "
        "quantity is the paired difference between the structural and conventional "
        "suites on the same fault, not the difference between acting and not acting. A "
        "fault class the conventional suite already detects yields no paired control win "
        "however much no-action headroom it has, so an advancing class here licenses an "
        "action screen, not a Slot-11 comparison."
    )
    return lines


def write_report(path: Path, summary: dict[str, Any]) -> None:
    """Write the deterministic role-separated fault-headroom report."""

    spec = summary["screen_spec"]
    decision = summary["decision"]
    tuning = {row["case_id"]: row for row in summary["tuning_candidate_summaries"]}
    assessment = {
        row["case_id"]: row for row in summary["assessment_candidate_summaries"]
    }
    lines = [
        "# Fault Tracking-Deficit Development Screen",
        "",
        f"**Decision:** `{decision['overall_decision']}`",
        "",
        (
            "This no-recovery sensitivity keeps the approved bounded task, contact "
            "plane, observed-state controller, probe, and six-second audit fixed while "
            "sweeping only remaining structural stiffness and actuator gain. Tuning and "
            "assessment sensor seeds are disjoint."
        ),
        "",
        "## Roles and gate",
        "",
        f"- Tuning seeds: {summary['tuning_role']['sensor_seeds']}.",
        f"- Assessment seeds: {summary['assessment_role']['sensor_seeds']}.",
        f"- Claim Sheet control bar: {spec['claim_tracking_bar_pct']:.1f}% *reduction*, measured against the degraded arm.",
        f"- Predeclared development margin: +{spec['development_margin_pct']:.1f} percentage points, applied in reduction units.",
        (
            f"- Required per-seed reduction: {decision['required_tracking_reduction_pct']:.1f}%. A "
            "source-specific action that exactly restores healthy tracking converts a "
            "deficit `D` into a reduction `D / (1 + D)`, so the equivalent per-seed "
            f"no-action deficit gate is {decision['required_tracking_deficit_pct']:.2f}%."
        ),
        (
            "- Every row must preserve one held healthy decision, zero recovery-command "
            "changes, exact seed-paired pre-fault histories, zero A1 incidents, and zero saturation."
        ),
        "- The mildest passing tuning severity is selected separately per physical source; only that preselected setting may advance on disjoint assessment.",
        "",
        "## Severity grid",
        "",
        "| Source | Remaining fraction | Tuning mean/min deficit | Tuning gate | Assessment mean/min deficit | Assessment gate |",
        "|---|---:|---:|---|---:|---|",
    ]
    for case in summary["case_grid"]:
        if case["source_class"] not in SCREENED_SOURCES:
            continue
        tune = tuning[case["case_id"]]
        assess = assessment[case["case_id"]]
        lines.append(
            f"| {case['source_class']} | {case['severity']:.2f} | "
            f"{tune['mean_tracking_deficit_pct']:.2f}% / {tune['minimum_tracking_deficit_pct']:.2f}% | "
            f"{'PASS' if tune['candidate_gate_pass'] else 'BLOCK'} | "
            f"{assess['mean_tracking_deficit_pct']:.2f}% / {assess['minimum_tracking_deficit_pct']:.2f}% | "
            f"{'PASS' if assess['candidate_gate_pass'] else 'BLOCK'} |"
        )
    lines.extend(["", "## Disjoint decision", ""])
    for source in SCREENED_SOURCES:
        result = decision["source_results"][source]
        if result["selected_case_id"] is None:
            lines.append(
                f"- **{source.capitalize()}: BLOCK.** No tuning severity cleared the "
                f"{decision['required_tracking_deficit_pct']:.1f}% per-seed headroom gate."
            )
        else:
            lines.append(
                f"- **{source.capitalize()}: "
                f"{'ADVANCE' if result['assessment_gate_pass'] else 'BLOCK'}.** "
                f"Tuning selected `{result['selected_case_id']}`; disjoint assessment "
                f"mean/min deficit = {result['assessment_mean_tracking_deficit_pct']:.2f}% / "
                f"{result['assessment_minimum_tracking_deficit_pct']:.2f}%."
            )
    sensor = summary["assessment_sensor_control"]
    lines.extend(
        [
            "",
            "## Observation-side sensor control",
            "",
            (
                f"The fixed {sensor['severity']:.2f} rad encoder-bias control keeps a "
                "healthy physical plant but corrupts the observed feedback path. Its "
                f"disjoint mean/min tracking deficit is {sensor['mean_tracking_deficit_pct']:.2f}% / "
                f"{sensor['minimum_tracking_deficit_pct']:.2f}%; lifecycle and A1/saturation "
                f"gates are {'PASS' if sensor['lifecycle_pass'] and sensor['safety_and_saturation_pass'] else 'BLOCK'}. "
                "It is a fixed control readout, not a selected severity candidate."
            ),
            *_scope_lines(summary),
            "",
            "## Interpretation boundary",
            "",
            summary["evidence_boundary"].capitalize() + ".",
            (
                "A passing deficit condition establishes only that the fault creates "
                "enough control-layer headroom for a later action screen to be meaningful. "
                "It does not show that any deployable estimator can identify the setting "
                "or that any recovery action can reclaim the deficit. All severity values, "
                "task/contact/controller settings, thresholds, W/stride, sensor constants, "
                "and config remain unfrozen."
            ),
        ]
    )
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text("\n".join(lines) + "\n", encoding="utf-8")


def main() -> int:
    """Run the screen and write strict deterministic JSON/CSV/Markdown outputs."""

    args = parse_args()
    if args.workers < 1:
        raise ValueError("workers must be positive")
    summary = run(FaultTrackingDeficitSpec(), workers=int(args.workers))
    args.output_dir.mkdir(parents=True, exist_ok=True)
    summary_path = args.output_dir / "summary.json"
    candidate_path = args.output_dir / "candidate_summary.csv"
    tuning_path = args.output_dir / "tuning_rows.csv"
    assessment_path = args.output_dir / "assessment_rows.csv"
    report_path = args.output_dir / "fault_tracking_deficit_report.md"
    summary_path.write_text(
        json.dumps(_jsonable(summary), indent=2, allow_nan=False) + "\n",
        encoding="utf-8",
    )
    candidate_rows = [
        {"role": "tuning", **row}
        for row in summary["tuning_candidate_summaries"]
    ] + [
        {"role": "assessment", **row}
        for row in summary["assessment_candidate_summaries"]
    ]
    write_csv(candidate_path, candidate_rows)
    write_csv(tuning_path, summary["tuning_rows"])
    write_csv(assessment_path, summary["assessment_rows"])
    write_report(report_path, summary)
    print(f"Decision: {summary['decision']['overall_decision']}", flush=True)
    for output in (
        summary_path,
        candidate_path,
        tuning_path,
        assessment_path,
        report_path,
    ):
        print(f"Wrote {output}", flush=True)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
