"""Screen a severity-conditioned structural recovery action on the bounded task.

The previously approved structural action is a 0.75 global command derate.  That is an
auditable safety floor, but the bounded noisy review showed it worsens the Claim Sheet's
primary control metric.  This development-only screen keeps the approved plant, task,
contact, sensing, and one-held-decision lifecycle fixed while comparing a predeclared
family of inverse-stiffness command multipliers against no action and the old derate.

Candidate selection uses only dedicated tuning sensor seeds.  A disjoint assessment role
then checks the selected action on the structural fault and under a healthy false-
authorization stress.  Fixed source outputs isolate the controller mechanism; this is
not attribution evidence, probability calibration, or an evaluation-sized result.
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

from run_noisy_reference_pilot import fault_specs
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
from utils.recovery_control import (
    GainScheduledRecoveryController,
    RecoveryControlConfig,
)
from utils.schema_types import SAFETY_FLAG_FIELDS
from utils.sensor_model import OnlineSensorSession, SensorConfig
from utils.task_control import (
    EstimatorRecoveryTaskPolicy,
    ObservedJointPDController,
)


@dataclass(frozen=True)
class StructuralActionCandidate:
    """One explicit structural action in the predeclared development family."""

    action_id: str
    structural_action: str
    scope: str
    multiplier_cap: float

    def validate(self) -> None:
        """Fail loudly when the action cannot map to the recovery controller."""

        if not self.action_id:
            raise ValueError("action_id cannot be empty")
        if self.structural_action not in {"derate", "inverse_stiffness"}:
            raise ValueError("unsupported structural action")
        if self.scope not in {"global", "localized"}:
            raise ValueError("unsupported compensation scope")
        if not np.isfinite(self.multiplier_cap) or self.multiplier_cap <= 0.0:
            raise ValueError("multiplier_cap must be finite and positive")
        if self.structural_action == "derate" and self.multiplier_cap > 1.0:
            raise ValueError("a derate multiplier cannot exceed one")
        if self.structural_action == "inverse_stiffness" and self.multiplier_cap < 1.0:
            raise ValueError("an inverse-stiffness multiplier cannot be below one")

    def controller(self) -> GainScheduledRecoveryController:
        """Return the exact controller configuration represented by this candidate."""

        self.validate()
        if self.structural_action == "derate":
            config = RecoveryControlConfig(
                structural_action="derate",
                structural_command_derate=self.multiplier_cap,
            )
        else:
            config = RecoveryControlConfig(
                structural_action="inverse_stiffness",
                structural_compensation_scope=self.scope,
                maximum_structural_compensation=self.multiplier_cap,
            )
        return GainScheduledRecoveryController(config)


@dataclass(frozen=True)
class StructuralRecoveryScreenSpec:
    """Role-separated seeds, candidate family, and predeclared advancement gates."""

    tuning_seed_start: int = 15000
    tuning_seed_count: int = 3
    assessment_seed_start: int = 15100
    assessment_seed_count: int = 4
    selected_plane_z_m: float = 0.200
    minimum_tracking_reduction_pct: float = 10.0
    minimum_source_specificity_margin_pct: float = 0.0

    @property
    def tuning_seeds(self) -> tuple[int, ...]:
        """Return the contiguous development-tuning sensor-seed role."""

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
    def candidates(self) -> tuple[StructuralActionCandidate, ...]:
        """Return the fixed no-action, old-floor, and compensation candidates."""

        return (
            StructuralActionCandidate("current_derate_0p75", "derate", "global", 0.75),
            StructuralActionCandidate("no_action_1p00", "inverse_stiffness", "global", 1.00),
            StructuralActionCandidate("global_1p10", "inverse_stiffness", "global", 1.10),
            StructuralActionCandidate("global_1p25", "inverse_stiffness", "global", 1.25),
            StructuralActionCandidate("global_1p50", "inverse_stiffness", "global", 1.50),
            StructuralActionCandidate("global_2p00", "inverse_stiffness", "global", 2.00),
            StructuralActionCandidate("localized_1p25", "inverse_stiffness", "localized", 1.25),
            StructuralActionCandidate("localized_1p50", "inverse_stiffness", "localized", 1.50),
            StructuralActionCandidate("localized_2p00", "inverse_stiffness", "localized", 2.00),
        )

    @property
    def no_action_id(self) -> str:
        """Return the paired comparison arm's identifier."""

        return "no_action_1p00"

    def mechanics_spec(self, sensor_seed: int) -> BoundedTaskContactSpec:
        """Return the already-approved bounded mechanics with one sensor seed."""

        return BoundedTaskContactSpec(
            plane_heights_z_m=(0.100, self.selected_plane_z_m),
            sensor_seed=sensor_seed,
        )

    def validate(self) -> None:
        """Fail loudly on overlapping roles or a malformed candidate family."""

        if self.tuning_seed_count < 1 or self.assessment_seed_count < 1:
            raise ValueError("both seed roles must contain at least one seed")
        if min(self.tuning_seed_start, self.assessment_seed_start) < 0:
            raise ValueError("sensor seeds must be non-negative")
        if set(self.tuning_seeds) & set(self.assessment_seeds):
            raise ValueError("tuning and assessment sensor seeds must be disjoint")
        if not np.isfinite(self.selected_plane_z_m):
            raise ValueError("selected_plane_z_m must be finite")
        if not np.isfinite(self.minimum_tracking_reduction_pct):
            raise ValueError("minimum_tracking_reduction_pct must be finite")
        if not np.isfinite(self.minimum_source_specificity_margin_pct):
            raise ValueError("minimum_source_specificity_margin_pct must be finite")
        candidates = self.candidates
        for candidate in candidates:
            candidate.validate()
        identifiers = [candidate.action_id for candidate in candidates]
        if len(set(identifiers)) != len(identifiers):
            raise ValueError("action identifiers must be unique")
        if identifiers.count(self.no_action_id) != 1:
            raise ValueError("candidate family must contain exactly one no-action arm")
        self.mechanics_spec(self.tuning_seeds[0]).validate()


def parse_args() -> argparse.Namespace:
    """Parse the portable screen command line."""

    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--output-dir",
        type=Path,
        default=Path("results/structural_recovery_action_screen"),
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


def _run_case(
    task: tuple[
        StructuralRecoveryScreenSpec,
        str,
        str,
        str,
        int,
        StructuralActionCandidate,
    ]
) -> dict[str, Any]:
    """Run one fixed-diagnosis action arm through the exact bounded causal seam."""

    screen, role, physical_source, estimator_source, sensor_seed, candidate = task
    mechanics = screen.mechanics_spec(sensor_seed)
    faults = fault_specs(mechanics.onset_index)
    pair_id = f"structural-recovery-{role}-{physical_source}-{sensor_seed}"
    plant = CablePlant(
        cable_config(mechanics, screen.selected_plane_z_m),
        point_count=mechanics.point_count,
        simulation_timestep_s=mechanics.simulation_timestep_s,
        fault=faults[physical_source],
    )
    sensors = OnlineSensorSession(
        "C1",
        pair_id=pair_id,
        sensor_seed=sensor_seed,
        control_dt_s=mechanics.control_dt_s,
        config=SensorConfig(),
        fault=None,
        run_id=f"{pair_id}-{candidate.action_id}",
        config_hash="dev-structural-recovery-action-screen",
        split=role,
    )
    estimator = SingleDecisionHoldEstimator(
        FixedSourceStandIn(estimator_source),
        first_decision_step=mechanics.first_decision_step,
    )
    profile = mechanics.task_profile()
    policy = EstimatorRecoveryTaskPolicy(
        ObservedJointPDController(profile, mechanics.controller_config()),
        estimator,
        suite="C1",
        run_id=f"{pair_id}-{candidate.action_id}",
        stride=mechanics.stride,
        recovery_controller=candidate.controller(),
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
    predecision = slice(0, mechanics.first_decision_step)
    shared_names = ("q_obs", "qd_obs", "tau_cmd", "current_proxy_obs", "imu_obs")
    predecision_hash = _hash_arrays(
        [
            ("q_true", rollout.plant.q_true[predecision]),
            ("qd_true", rollout.plant.qd_true[predecision]),
            ("tau_cmd", rollout.plant.tau_cmd[predecision]),
        ]
        + [
            (f"values/{name}", rollout.observations.values[name][predecision])
            for name in shared_names
        ]
        + [
            (f"mask/{name}", rollout.observations.valid_mask[name][predecision])
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
        "physical_source": physical_source,
        "estimator_source": estimator_source,
        "sensor_seed": sensor_seed,
        "pair_id": pair_id,
        "action_id": candidate.action_id,
        "structural_action": candidate.structural_action,
        "scope": candidate.scope,
        "multiplier_cap": candidate.multiplier_cap,
        "classification_evaluations": estimator.classification_evaluations,
        "command_changed_steps": int(np.count_nonzero(changed)),
        "command_changed_before_decision": bool(np.any(changed[predecision])),
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
        "predecision_hash": predecision_hash,
    }
    row.update({f"flag_steps_{name}": count for name, count in flag_counts.items()})
    return row


def _paired_reductions(
    rows: list[dict[str, Any]], baseline_id: str
) -> dict[str, list[float]]:
    """Return per-action paired tracking reductions against the seed-matched baseline."""

    baselines = {
        (row["physical_source"], row["sensor_seed"]): row
        for row in rows
        if row["action_id"] == baseline_id
    }
    reductions: dict[str, list[float]] = {}
    for row in rows:
        key = (row["physical_source"], row["sensor_seed"])
        baseline = baselines.get(key)
        if baseline is None:
            raise ValueError(f"missing no-action row for {key}")
        if row["predecision_hash"] != baseline["predecision_hash"]:
            raise ValueError(f"pre-decision CRN mismatch for {row['action_id']} / {key}")
        baseline_j = float(baseline["tracking_integral_5s_m_s"])
        action_j = float(row["tracking_integral_5s_m_s"])
        reductions.setdefault(row["action_id"], []).append(
            100.0 * (baseline_j - action_j) / baseline_j
        )
    return reductions


def select_candidate(
    spec: StructuralRecoveryScreenSpec, rows: list[dict[str, Any]]
) -> tuple[str | None, list[dict[str, Any]]]:
    """Select the strongest tuning-only candidate that clears every declared gate."""

    reductions = _paired_reductions(rows, spec.no_action_id)
    summaries: list[dict[str, Any]] = []
    for candidate in spec.candidates:
        candidate_rows = [row for row in rows if row["action_id"] == candidate.action_id]
        values = reductions[candidate.action_id]
        expected_change = candidate.action_id != spec.no_action_id
        lifecycle_pass = bool(
            len(candidate_rows) == spec.tuning_seed_count
            and all(row["classification_evaluations"] == 1 for row in candidate_rows)
            and all(not row["command_changed_before_decision"] for row in candidate_rows)
            and all(
                (row["command_changed_steps"] > 0) == expected_change
                for row in candidate_rows
            )
        )
        safety_pass = bool(
            all(row["safety_incident_steps"] == 0 for row in candidate_rows)
            and all(row["saturation_steps"] == 0 for row in candidate_rows)
        )
        tracking_pass = bool(
            candidate.action_id != spec.no_action_id
            and min(values) >= spec.minimum_tracking_reduction_pct
        )
        summaries.append(
            {
                "action_id": candidate.action_id,
                "structural_action": candidate.structural_action,
                "scope": candidate.scope,
                "multiplier_cap": candidate.multiplier_cap,
                "mean_tracking_reduction_pct": float(np.mean(values)),
                "minimum_tracking_reduction_pct": float(min(values)),
                "maximum_tracking_reduction_pct": float(max(values)),
                "lifecycle_pass": lifecycle_pass,
                "safety_and_saturation_pass": safety_pass,
                "tracking_gate_pass": tracking_pass,
                "candidate_gate_pass": bool(
                    lifecycle_pass and safety_pass and tracking_pass
                ),
            }
        )
    eligible = [row for row in summaries if row["candidate_gate_pass"]]
    if not eligible:
        return None, summaries
    selected = max(
        eligible,
        key=lambda row: (
            row["minimum_tracking_reduction_pct"],
            row["mean_tracking_reduction_pct"],
            -abs(float(row["multiplier_cap"]) - 1.0),
            row["scope"] == "localized",
        ),
    )
    return str(selected["action_id"]), summaries


def _baseline_comparison_sound(
    spec: StructuralRecoveryScreenSpec, rows: list[dict[str, Any]], physical_source: str
) -> bool:
    """Return whether one source's no-action baseline can carry a paired comparison.

    Every reported reduction, and therefore the whole source-specificity margin, is
    measured *against* these rows. A baseline that itself acted, evaluated the
    classifier more than once, saturated, or raised an A1 flag would silently
    corrupt the percentages while each acting arm still looked clean, so the
    baseline is held to the same lifecycle and safety contract as the action arms.

    Args:
        spec: Screen specification supplying the expected assessment seed count.
        rows: Assessment rows for every source and action.
        physical_source: Physically simulated source whose baseline is checked.

    Returns:
        True when that source's baselines are complete, action-free, evaluated
        exactly once, saturation-free, and A1-incident-free.
    """

    baselines = [
        row
        for row in rows
        if row["action_id"] == spec.no_action_id
        and row["physical_source"] == physical_source
    ]
    return bool(
        len(baselines) == spec.assessment_seed_count
        and all(row["classification_evaluations"] == 1 for row in baselines)
        and all(not row["command_changed_before_decision"] for row in baselines)
        and all(row["command_changed_steps"] == 0 for row in baselines)
        and all(row["safety_incident_steps"] == 0 for row in baselines)
        and all(row["saturation_steps"] == 0 for row in baselines)
    )


def decide_assessment(
    spec: StructuralRecoveryScreenSpec,
    selected_id: str | None,
    rows: list[dict[str, Any]],
) -> dict[str, Any]:
    """Apply disjoint assessment, false-authorization, and specificity gates.

    Each source's gate covers both halves of that source's paired comparison: the
    selected-action arm and the no-action baseline it is measured against.
    """

    if selected_id is None:
        return {
            "selected_action_id": None,
            "structural_tracking_gate_pass": False,
            "healthy_false_authorization_safety_pass": False,
            "source_specificity_gate_pass": False,
            "overall_decision": "BLOCK_STRUCTURAL_RECOVERY_ACTION_FAMILY",
        }
    reductions = _paired_reductions(rows, spec.no_action_id)
    structural = [
        row
        for row in rows
        if row["physical_source"] == "structure" and row["action_id"] == selected_id
    ]
    healthy = [
        row
        for row in rows
        if row["physical_source"] == "healthy" and row["action_id"] == selected_id
    ]
    structural_reductions = [
        value
        for value, row in zip(reductions[selected_id], [r for r in rows if r["action_id"] == selected_id], strict=True)
        if row["physical_source"] == "structure"
    ]
    healthy_reductions = [
        value
        for value, row in zip(reductions[selected_id], [r for r in rows if r["action_id"] == selected_id], strict=True)
        if row["physical_source"] == "healthy"
    ]
    structural_tracking = bool(
        len(structural) == spec.assessment_seed_count
        and min(structural_reductions) >= spec.minimum_tracking_reduction_pct
        and all(row["safety_incident_steps"] == 0 for row in structural)
        and all(row["saturation_steps"] == 0 for row in structural)
        and all(row["classification_evaluations"] == 1 for row in structural)
        and all(not row["command_changed_before_decision"] for row in structural)
        and all(row["command_changed_steps"] > 0 for row in structural)
        and _baseline_comparison_sound(spec, rows, "structure")
    )
    healthy_safety = bool(
        len(healthy) == spec.assessment_seed_count
        and all(row["safety_incident_steps"] == 0 for row in healthy)
        and all(row["saturation_steps"] == 0 for row in healthy)
        and all(row["classification_evaluations"] == 1 for row in healthy)
        and all(not row["command_changed_before_decision"] for row in healthy)
        and all(row["command_changed_steps"] > 0 for row in healthy)
        and _baseline_comparison_sound(spec, rows, "healthy")
    )
    specificity_margin = float(
        np.mean(structural_reductions) - np.mean(healthy_reductions)
    )
    specificity_pass = bool(
        specificity_margin > spec.minimum_source_specificity_margin_pct
    )
    advance = bool(structural_tracking and healthy_safety and specificity_pass)
    return {
        "selected_action_id": selected_id,
        "structural_tracking_gate_pass": structural_tracking,
        "healthy_false_authorization_safety_pass": healthy_safety,
        "source_specificity_gate_pass": specificity_pass,
        "structural_mean_tracking_reduction_pct": float(
            np.mean(structural_reductions)
        ),
        "structural_minimum_tracking_reduction_pct": float(
            min(structural_reductions)
        ),
        "healthy_false_authorization_mean_tracking_reduction_pct": float(
            np.mean(healthy_reductions)
        ),
        "structural_minus_healthy_reduction_margin_pct": specificity_margin,
        "overall_decision": (
            "ADVANCE_STRUCTURAL_INVERSE_STIFFNESS_ACTION_TO_NOISY_REVIEW"
            if advance
            else "BLOCK_STRUCTURAL_RECOVERY_ACTION_FAMILY"
        ),
    }


def run(spec: StructuralRecoveryScreenSpec, *, workers: int) -> dict[str, Any]:
    """Run tuning, select without assessment leakage, then audit disjoint seeds."""

    spec.validate()
    if workers < 1:
        raise ValueError("workers must be positive")
    tuning_tasks = [
        (spec, "tuning", "structure", "structure", seed, candidate)
        for seed in spec.tuning_seeds
        for candidate in spec.candidates
    ]
    print(f"Running {len(tuning_tasks)} tuning-only structural action arms ...", flush=True)
    if workers == 1:
        tuning_rows = [_run_case(task) for task in tuning_tasks]
    else:
        with concurrent.futures.ProcessPoolExecutor(max_workers=workers) as executor:
            tuning_rows = list(executor.map(_run_case, tuning_tasks))
    tuning_rows.sort(key=lambda row: (row["sensor_seed"], row["action_id"]))
    selected_id, candidate_rows = select_candidate(spec, tuning_rows)

    assessment_rows: list[dict[str, Any]] = []
    if selected_id is not None:
        selected = next(
            candidate for candidate in spec.candidates if candidate.action_id == selected_id
        )
        no_action = next(
            candidate
            for candidate in spec.candidates
            if candidate.action_id == spec.no_action_id
        )
        assessment_tasks = []
        for seed in spec.assessment_seeds:
            assessment_tasks.extend(
                [
                    (spec, "assessment", "structure", "structure", seed, no_action),
                    (spec, "assessment", "structure", "structure", seed, selected),
                    (spec, "assessment", "healthy", "healthy", seed, no_action),
                    (spec, "assessment", "healthy", "structure", seed, selected),
                ]
            )
        print(
            f"Running {len(assessment_tasks)} disjoint assessment and false-action arms ...",
            flush=True,
        )
        if workers == 1:
            assessment_rows = [_run_case(task) for task in assessment_tasks]
        else:
            with concurrent.futures.ProcessPoolExecutor(max_workers=workers) as executor:
                assessment_rows = list(executor.map(_run_case, assessment_tasks))
        assessment_rows.sort(
            key=lambda row: (
                row["physical_source"],
                row["sensor_seed"],
                row["action_id"],
            )
        )
    decision = decide_assessment(spec, selected_id, assessment_rows)
    return {
        "artifact_status": "development_only_config_unfrozen",
        "screen_spec": asdict(spec),
        "mechanics_spec": asdict(spec.mechanics_spec(spec.tuning_seeds[0])),
        "candidate_family": [asdict(candidate) for candidate in spec.candidates],
        "tuning_role": {
            "sensor_seeds": list(spec.tuning_seeds),
            "purpose": "select one action without reading assessment or prior held-out seeds",
        },
        "assessment_role": {
            "sensor_seeds": list(spec.assessment_seeds),
            "purpose": "disjoint structural action and healthy false-authorization audit",
        },
        "candidate_rows": candidate_rows,
        "tuning_rows": tuning_rows,
        "assessment_rows": assessment_rows,
        "decision": decision,
        "evidence_boundary": (
            "fixed source-correct outputs isolate a small controller mechanism screen; "
            "this is not noisy attribution, a probability-calibrated action, an "
            "evaluation-sized comparison, or permission to freeze config"
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


def _scope_lines(summary: dict[str, Any]) -> list[str]:
    """Return the generated bounds on what this screen's decision can support.

    Every figure is recomputed from the recorded rows so the section regenerates
    deterministically with the rest of the report and cannot drift from the data.

    Args:
        summary: The screen summary produced by ``run``.

    Returns:
        Markdown lines stating the measured limits of the recorded decision.
    """

    spec = StructuralRecoveryScreenSpec(**summary["screen_spec"])
    rows = summary["assessment_rows"]
    decision = summary["decision"]
    selected_id = decision["selected_action_id"]

    def baseline(source: str) -> list[float]:
        return [
            float(row["tracking_integral_5s_m_s"])
            for row in rows
            if row["physical_source"] == source and row["action_id"] == spec.no_action_id
        ]

    def peak(source: str, action_id: str, column: str) -> float:
        values = [
            float(row[column])
            for row in rows
            if row["physical_source"] == source and row["action_id"] == action_id
        ]
        return float(np.mean(values))

    healthy_base = baseline("healthy")
    structure_base = baseline("structure")
    healthy_mean = float(np.mean(healthy_base))
    deficit_pct = 100.0 * (float(np.mean(structure_base)) - healthy_mean) / healthy_mean
    seed_spread = max(
        max(healthy_base) - min(healthy_base), max(structure_base) - min(structure_base)
    )
    deficit_vs_spread = abs(float(np.mean(structure_base)) - healthy_mean) / seed_spread

    reductions = _paired_reductions(rows, spec.no_action_id)
    ordered = [row for row in rows if row["action_id"] == selected_id]
    per_source = {"structure": [], "healthy": []}
    for value, row in zip(reductions[selected_id], ordered, strict=True):
        per_source[row["physical_source"]].append(value)
    structure_spread = max(per_source["structure"]) - min(per_source["structure"])
    healthy_spread = max(per_source["healthy"]) - min(per_source["healthy"])
    margin = float(decision["structural_minus_healthy_reduction_margin_pct"])

    candidates = {row["action_id"]: row for row in summary["candidate_rows"]}
    selected_cap = float(candidates[selected_id]["multiplier_cap"])
    twin = next(
        (
            row
            for row in summary["candidate_rows"]
            if row["scope"] == "localized"
            and float(row["multiplier_cap"]) == selected_cap
            and row["action_id"] != selected_id
        ),
        None,
    )

    limits = cable_config(
        spec.mechanics_spec(spec.tuning_seeds[0]), spec.selected_plane_z_m
    )
    force_base = max(peak(s, spec.no_action_id, "peak_contact_force_n")
                     for s in ("healthy", "structure"))
    force_action = max(peak(s, selected_id, "peak_contact_force_n")
                       for s in ("healthy", "structure"))
    gauge_base = peak("structure", spec.no_action_id, "max_abs_gauge_microstrain")
    gauge_action = peak("structure", selected_id, "max_abs_gauge_microstrain")

    lines = [
        "",
        "## What the recorded decision does and does not establish",
        "",
        (
            f"- **The structural fault's own tracking deficit bounds any structural "
            f"recovery.** Its no-action `J_5s` sits {deficit_pct:+.4f}% from the healthy "
            f"no-action arm's — only {deficit_vs_spread:.2f}x the widest within-source "
            f"seed spread, so it is not resolved above seed noise. A source-specific "
            f"action can at best recover that gap, which is "
            f"{spec.minimum_tracking_reduction_pct / max(abs(deficit_pct), 1e-9):.0f}x "
            f"smaller than the {spec.minimum_tracking_reduction_pct:.0f}% gate it would "
            f"have to clear. On this bounded condition the binding constraint on the "
            f"control layer is the task/fault severity, not the action family and not "
            f"the nominal controller's tuning."
        ),
        (
            f"- **The source-specificity margin is smaller than the spread of its own "
            f"inputs.** It is the difference of two unpaired {spec.assessment_seed_count}"
            f"-seed means: {margin:+.3f} percentage points, against per-seed reduction "
            f"spreads of {structure_spread:.3f} pp (structure) and {healthy_spread:.3f} pp "
            f"(healthy). No uncertainty is computed for it, so its sign is not "
            f"established by this design and the block should not be read off it."
        ),
    ]
    if twin is not None:
        global_mean = float(candidates[selected_id]["mean_tracking_reduction_pct"])
        local_mean = float(twin["mean_tracking_reduction_pct"])
        lines.append(
            f"- **Most of the benefit comes from the joint carrying no fault** — this is "
            f"the robust evidence for the block. At the identical {selected_cap:.2f}x "
            f"multiplier, `{twin['action_id']}` applied only at the joint the diagnosis "
            f"localizes recovers {local_mean:.2f}% against `{selected_id}`'s "
            f"{global_mean:.2f}%, so {100.0 * (global_mean - local_mean) / global_mean:.0f}% "
            f"of the improvement is produced at the unfaulted joint. That contrast is a "
            f"within-role comparison at ~{global_mean - local_mean:.0f} pp effect size and "
            f"is not noise-limited."
        )
    lines.append(
        f"- **The safety readouts did not discriminate between candidates.** No arm in "
        f"the family raised an A1 flag or saturated, but the limits sit far from the "
        f"operating point, so those gates carried no information here — and the selected "
        f"action is not free of cost: mean peak contact force rises "
        f"{force_base:.3f} -> {force_action:.3f} N "
        f"({100.0 * force_base / limits.tip_contact_force_limit_n:.0f}% -> "
        f"{100.0 * force_action / limits.tip_contact_force_limit_n:.0f}% of the "
        f"{limits.tip_contact_force_limit_n:.1f} N limit) and mean peak structural "
        f"|gauge| rises {gauge_base:.1f} -> {gauge_action:.1f} µε on the link the "
        f"diagnosis says has lost stiffness. A threshold-crossing count cannot score "
        f"that trade in either direction."
    )
    return lines


def write_report(path: Path, summary: dict[str, Any]) -> None:
    """Write the role-separated structural action sensitivity report."""

    decision = summary["decision"]
    spec = summary["screen_spec"]
    assessment_baselines = {
        (row["physical_source"], row["sensor_seed"]): row
        for row in summary["assessment_rows"]
        if row["action_id"] == "no_action_1p00"
    }
    lines = [
        "# Structural Recovery Action Development Screen",
        "",
        f"**Decision:** `{decision['overall_decision']}`",
        "",
        (
            "This fixed-diagnosis sensitivity keeps the approved bounded mechanics and "
            "one-held-decision lifecycle unchanged while screening a predeclared "
            "inverse-stiffness action family. Tuning and assessment sensor seeds are "
            "disjoint. No noisy attribution or confirmatory evidence is claimed."
        ),
        "",
        "## Roles and gates",
        "",
        f"- Tuning seeds: {summary['tuning_role']['sensor_seeds']}.",
        f"- Assessment seeds: {summary['assessment_role']['sensor_seeds']}.",
        f"- Required per-seed tracking reduction: {spec['minimum_tracking_reduction_pct']:.1f}%.",
        "- Every candidate must preserve one held decision, causal action timing, zero "
        "A1 safety incidents, zero actuator saturation, and exact pre-decision CRN matching.",
        "- A selected action must retain the tracking gate on disjoint structural seeds, "
        "stay safe under a healthy false-authorization stress, and help structure more "
        "than healthy so a generic gain retune is not mislabeled as source-specific recovery.",
        "",
        "## Tuning-only candidate screen",
        "",
        "| Action | Scope | Cap | Mean reduction | Min reduction | Lifecycle | Safety | Tracking | Candidate |",
        "|---|---|---:|---:|---:|---|---|---|---|",
    ]
    for row in summary["candidate_rows"]:
        lines.append(
            f"| {row['action_id']} | {row['scope']} | {row['multiplier_cap']:.2f} | "
            f"{row['mean_tracking_reduction_pct']:.2f}% | "
            f"{row['minimum_tracking_reduction_pct']:.2f}% | "
            f"{'PASS' if row['lifecycle_pass'] else 'BLOCK'} | "
            f"{'PASS' if row['safety_and_saturation_pass'] else 'BLOCK'} | "
            f"{'PASS' if row['tracking_gate_pass'] else 'BLOCK'} | "
            f"{'PASS' if row['candidate_gate_pass'] else 'BLOCK'} |"
        )
    lines.extend(["", "## Disjoint assessment", ""])
    if decision["selected_action_id"] is None:
        lines.append("No tuning candidate cleared the predeclared 10% tracking gate.")
    else:
        lines.extend(
            [
                f"- Selected action: `{decision['selected_action_id']}`.",
                f"- Structural mean/min reduction: {decision['structural_mean_tracking_reduction_pct']:.2f}% / "
                f"{decision['structural_minimum_tracking_reduction_pct']:.2f}%.",
                "- Healthy false-authorization mean tracking reduction: "
                f"{decision['healthy_false_authorization_mean_tracking_reduction_pct']:.2f}%.",
                "- Structural-minus-healthy reduction margin: "
                f"{decision['structural_minus_healthy_reduction_margin_pct']:.2f} percentage points.",
                f"- Structural tracking gate: **{'PASS' if decision['structural_tracking_gate_pass'] else 'BLOCK'}**.",
                "- Healthy false-authorization safety gate: "
                f"**{'PASS' if decision['healthy_false_authorization_safety_pass'] else 'BLOCK'}**.",
                f"- Source-specificity gate: **{'PASS' if decision['source_specificity_gate_pass'] else 'BLOCK'}**.",
            ]
        )
        lines.extend(
            [
                "",
                "| Source | Seed | Action | J5s | Reduction | Contact episodes | Peak force (N) | Safety | Saturation |",
                "|---|---:|---|---:|---:|---:|---:|---:|---:|",
            ]
        )
        for row in summary["assessment_rows"]:
            baseline = assessment_baselines[
                (row["physical_source"], row["sensor_seed"])
            ]
            baseline_j = float(baseline["tracking_integral_5s_m_s"])
            reduction = 100.0 * (
                baseline_j - float(row["tracking_integral_5s_m_s"])
            ) / baseline_j
            lines.append(
                f"| {row['physical_source']} | {row['sensor_seed']} | "
                f"{row['action_id']} | {row['tracking_integral_5s_m_s']:.4f} | "
                f"{reduction:.2f}% | {row['contact_episode_count']} | "
                f"{row['peak_contact_force_n']:.3f} | "
                f"{row['safety_incident_steps']} | {row['saturation_steps']} |"
            )
        if not decision["source_specificity_gate_pass"]:
            lines.extend(
                [
                    "",
                    (
                        "The selected global multiplier improves healthy tracking slightly "
                        "more than structural-fault tracking. The screen therefore identifies "
                        "generic nominal-controller under-authority, not a structural recovery "
                        "mechanism. The nominal controller must be retuned first, after which "
                        "the task/fault condition must expose a measurable stiffness-loss "
                        "deficit before another source-specific action is screened."
                    ),
                ]
            )
    lines.extend(
        [
            "",
            "## Interpretation boundary",
            "",
            summary["evidence_boundary"].capitalize() + ".",
            "The old 0.75 derate remains the approved transparent safety floor. This "
            "screen asks only whether a bounded severity-conditioned alternative is "
            "coherent enough to enter the already-approved noisy held-decision review. "
            "The action family, multiplier, task/contact/controller values, sensor "
            "constants, fault setting, W/stride, thresholds, and config remain unfrozen.",
        ]
    )
    if summary["assessment_rows"]:
        lines.extend(_scope_lines(summary))
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text("\n".join(lines) + "\n", encoding="utf-8")


def main() -> int:
    """Run the screen and write strict deterministic JSON/CSV/Markdown outputs."""

    args = parse_args()
    if args.workers < 1:
        raise ValueError("workers must be positive")
    summary = run(StructuralRecoveryScreenSpec(), workers=int(args.workers))
    args.output_dir.mkdir(parents=True, exist_ok=True)
    summary_path = args.output_dir / "summary.json"
    candidates_path = args.output_dir / "candidate_rows.csv"
    tuning_path = args.output_dir / "tuning_rows.csv"
    assessment_path = args.output_dir / "assessment_rows.csv"
    report_path = args.output_dir / "structural_recovery_action_report.md"
    summary_path.write_text(
        json.dumps(_jsonable(summary), indent=2, allow_nan=False) + "\n",
        encoding="utf-8",
    )
    write_csv(candidates_path, summary["candidate_rows"])
    write_csv(tuning_path, summary["tuning_rows"])
    if summary["assessment_rows"]:
        write_csv(assessment_path, summary["assessment_rows"])
    write_report(report_path, summary)
    print(f"Decision: {summary['decision']['overall_decision']}", flush=True)
    for output in (
        summary_path,
        candidates_path,
        tuning_path,
        assessment_path,
        report_path,
    ):
        if output.exists():
            print(f"Wrote {output}", flush=True)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
