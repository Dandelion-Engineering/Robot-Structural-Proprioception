"""Screen the actuator recovery action on the selected bounded condition.

The fault-tracking-deficit screen selected 0.25 remaining actuator gain because it
provides enough no-action headroom for the Claim Sheet's 10% tracking-reduction bar.
The probability-channel screen then showed that the recorded cap of 2.0 realizes only
57.5% of the analytic exact-restoration ceiling. This screen asks the next question
directly: is there a bounded cap/floor setting whose actuator action is large enough to
help the faulted arm *source-specifically*, rather than merely retuning any arm that is
authorized to act?

The screen is role-separated:

* three tuning-only seeds compare a predeclared cap/floor family using a privileged
  source-correct severity. Candidate selection reads both fault recovery and the same
  actuator diagnosis falsely authorized on a healthy plant;
* four disjoint assessment seeds re-test the selected candidate with an oracle severity
  and with the recorded held-out C1/S severity estimates from the approved severity
  screen; and
* two cap/floor stress profiles show whether raising the cap alone, or raising the cap
  while lowering the floor, changes the deployable arms.

Every source-specific margin is paired within seed:

    fault action benefit - healthy false-authorization benefit.

The assessment reports a deterministic paired percentile-bootstrap interval on that
margin. Four seeds are development-sized, so the interval is a guard against a
sign-unstable effect, not validation-sized evidence.

Run from ``Reproducibility Packet/``:
    ..\\venv\\Scripts\\python.exe scripts\\screen_actuator_recovery_action.py --workers 8
"""

from __future__ import annotations

import argparse
import concurrent.futures
import csv
import hashlib
import json
import sys
from dataclasses import dataclass
from pathlib import Path
from typing import Any

import numpy as np

sys.path.insert(0, str(Path(__file__).resolve().parent))

from screen_actuator_probability_channel import (  # noqa: E402
    ProbabilityDiagnosisEstimator,
)
from screen_bounded_task_contact import (  # noqa: E402
    BoundedTaskContactSpec,
    SingleDecisionHoldEstimator,
    cable_config,
)
from utils.cable_plant import CablePlant  # noqa: E402
from utils.metrics import j_5s, tracking_reduction_pct  # noqa: E402
from utils.online_loop import run_online_rollout  # noqa: E402
from utils.recovery_control import (  # noqa: E402
    GainScheduledRecoveryController,
    RecoveryControlConfig,
)
from utils.schema_types import FaultSpec  # noqa: E402
from utils.sensor_model import OnlineSensorSession, SensorConfig  # noqa: E402
from utils.stats import hierarchical_bootstrap_ci  # noqa: E402
from utils.task_control import (  # noqa: E402
    EstimatorRecoveryTaskPolicy,
    ObservedJointPDController,
)


SELECTED_SEVERITY = 0.25
FAULT_LOCATION = 1
PLANE_Z_M = 0.200
CLAIM_TRACKING_BAR_PCT = 10.0
TUNING_TRACKING_TARGET_PCT = 12.0
TUNING_SEEDS: tuple[int, ...] = (18000, 18001, 18002)
ASSESSMENT_SEEDS: tuple[int, ...] = (17100, 17101, 17102, 17103)
BOOTSTRAP_REPLICATES = 20_000
BOOTSTRAP_SEED = 20260723
CRN_REUSE_TOLERANCE = 1.0e-12
MULTIPLIER_IDENTITY_TOLERANCE = 1.0e-9
CONFIG_HASH = "dev-actuator-recovery-action-screen"


@dataclass(frozen=True)
class ActuatorActionCandidate:
    """One development cap/floor setting for the inverse-gain action."""

    label: str
    maximum_gain_compensation: float
    minimum_gain_remaining: float

    def validate(self) -> None:
        """Fail loudly when the candidate is non-physical or ambiguously named."""

        if not self.label or any(ch.isspace() for ch in self.label):
            raise ValueError("candidate label must be non-empty and contain no spaces")
        if (
            not np.isfinite(self.maximum_gain_compensation)
            or self.maximum_gain_compensation < 1.0
        ):
            raise ValueError("maximum_gain_compensation must be finite and >= 1")
        if (
            not np.isfinite(self.minimum_gain_remaining)
            or not 0.0 < self.minimum_gain_remaining <= 1.0
        ):
            raise ValueError("minimum_gain_remaining must lie in (0, 1]")


CANDIDATES: tuple[ActuatorActionCandidate, ...] = (
    ActuatorActionCandidate("cap2_floor0p25", 2.0, 0.25),
    ActuatorActionCandidate("cap3_floor0p25", 3.0, 0.25),
    ActuatorActionCandidate("cap4_floor0p25", 4.0, 0.25),
    ActuatorActionCandidate("cap5_floor0p25", 5.0, 0.25),
    ActuatorActionCandidate("cap5_floor0p20", 5.0, 0.20),
)


@dataclass(frozen=True)
class ActuatorActionArmSpec:
    """One physical-source × diagnosis × controller-profile rollout."""

    role: str
    seed: int
    physical_source: str
    diagnosis: str
    candidate_label: str
    maximum_gain_compensation: float
    minimum_gain_remaining: float
    estimated_severity: float | None
    severity_uncertainty: float
    suite: str

    def validate(self) -> None:
        """Validate one arm before any MuJoCo work begins."""

        if self.role not in {"tuning", "assessment"}:
            raise ValueError("role must be tuning or assessment")
        if self.physical_source not in {"healthy", "actuator"}:
            raise ValueError("physical_source must be healthy or actuator")
        if self.diagnosis not in {"no_action", "oracle", "C1", "S"}:
            raise ValueError("unsupported diagnosis")
        if self.suite not in {"C1", "S"}:
            raise ValueError("suite must be C1 or S")
        if self.diagnosis == "no_action":
            if self.estimated_severity is not None:
                raise ValueError("no-action arm must not carry an estimated severity")
        elif (
            self.estimated_severity is None
            or not 0.0 < float(self.estimated_severity) <= 1.0
        ):
            raise ValueError("acting arm requires estimated_severity in (0, 1]")
        candidate = ActuatorActionCandidate(
            self.candidate_label,
            self.maximum_gain_compensation,
            self.minimum_gain_remaining,
        )
        candidate.validate()
        if (
            not np.isfinite(self.severity_uncertainty)
            or self.severity_uncertainty < 0.0
        ):
            raise ValueError("severity_uncertainty must be finite and non-negative")


def parse_args() -> argparse.Namespace:
    """Parse portable CLI arguments."""

    parser = argparse.ArgumentParser(
        description=(
            "Screen the selected actuator recovery action with paired healthy "
            "false-authorization and cap/floor sensitivity."
        )
    )
    parser.add_argument("--workers", type=int, default=8)
    parser.add_argument(
        "--severity-summary",
        type=Path,
        default=Path("results/severity_estimation_quality/summary.json"),
    )
    parser.add_argument(
        "--severity-arm-rows",
        type=Path,
        default=Path("results/severity_estimation_quality/arm_rows.csv"),
    )
    parser.add_argument(
        "--output-dir",
        type=Path,
        default=Path("results/actuator_recovery_action_screen"),
    )
    return parser.parse_args()


def _hash_arrays(named_arrays: list[tuple[str, np.ndarray]]) -> str:
    """Return a stable hash over named array shapes, dtypes, and bytes."""

    digest = hashlib.sha256()
    for name, array in named_arrays:
        contiguous = np.ascontiguousarray(array)
        digest.update(name.encode("utf-8"))
        digest.update(str(contiguous.shape).encode("ascii"))
        digest.update(str(contiguous.dtype).encode("ascii"))
        digest.update(contiguous.tobytes())
    return digest.hexdigest()


def load_recorded_inputs(
    summary_path: Path,
    arm_rows_path: Path,
) -> tuple[dict[str, dict[int, float]], dict[str, float], dict[str, dict[int, float]]]:
    """Load recorded C1/S severities, RMS scales, and no-action J5 references."""

    if not summary_path.is_file():
        raise FileNotFoundError(f"missing severity summary: {summary_path}")
    if not arm_rows_path.is_file():
        raise FileNotFoundError(f"missing severity arm rows: {arm_rows_path}")
    summary = json.loads(summary_path.read_text(encoding="utf-8"))
    evaluations = summary.get("suite_evaluations", {})
    estimates: dict[str, dict[int, float]] = {}
    uncertainties: dict[str, float] = {}
    for suite in ("C1", "S"):
        evaluation = evaluations.get(suite)
        if not isinstance(evaluation, dict):
            raise ValueError(f"severity summary is missing suite {suite}")
        suite_estimates = {
            int(row["seed"]): float(row["estimate"])
            for row in evaluation.get("predictions", [])
            if np.isclose(float(row["severity"]), SELECTED_SEVERITY)
        }
        if set(suite_estimates) != set(ASSESSMENT_SEEDS):
            raise ValueError(
                f"suite {suite} severity estimates do not match assessment seeds"
            )
        rms = float(evaluation["holdout_rmse"])
        if not np.isfinite(rms) or rms < 0.0:
            raise ValueError(f"suite {suite} holdout_rmse is invalid")
        estimates[suite] = suite_estimates
        uncertainties[suite] = rms

    references: dict[str, dict[int, float]] = {"healthy": {}, "actuator": {}}
    with arm_rows_path.open(newline="", encoding="utf-8") as handle:
        for row in csv.DictReader(handle):
            if row["role"] != "assessment":
                continue
            severity = float(row["severity"])
            source = (
                "actuator"
                if np.isclose(severity, SELECTED_SEVERITY)
                else "healthy"
                if np.isclose(severity, 1.0)
                else None
            )
            if source is not None:
                references[source][int(row["seed"])] = float(row["j_5s"])
    for source, values in references.items():
        if set(values) != set(ASSESSMENT_SEEDS):
            raise ValueError(
                f"recorded {source} J5 references do not match assessment seeds"
            )
    return estimates, uncertainties, references


def expected_multiplier(spec: ActuatorActionArmSpec) -> float:
    """Return the controller multiplier implied by one arm specification."""

    if spec.diagnosis == "no_action":
        return 1.0
    remaining = max(float(spec.estimated_severity), spec.minimum_gain_remaining)
    return min(1.0 / remaining, spec.maximum_gain_compensation)


def run_arm(spec: ActuatorActionArmSpec) -> dict[str, Any]:
    """Run one arm and return tracking plus fail-loud audit fields."""

    spec.validate()
    mechanics = BoundedTaskContactSpec(
        plane_heights_z_m=(0.100, PLANE_Z_M), sensor_seed=spec.seed
    )
    pair_id = (
        f"severity-quality-assessment-{spec.seed}"
        if spec.role == "assessment"
        else f"actuator-recovery-tuning-{spec.seed}"
    )
    run_id = (
        f"actuator-recovery-{spec.role}-{spec.seed}-{spec.physical_source}-"
        f"{spec.diagnosis}-{spec.candidate_label}"
    )
    fault = (
        FaultSpec(
            source_class="actuator",
            subtype="actuator_gain_loss",
            location=FAULT_LOCATION,
            severity=SELECTED_SEVERITY,
            onset_index=mechanics.onset_index,
        )
        if spec.physical_source == "actuator"
        else FaultSpec()
    )
    plant = CablePlant(
        cable_config(mechanics, PLANE_Z_M),
        point_count=mechanics.point_count,
        simulation_timestep_s=mechanics.simulation_timestep_s,
        fault=fault,
    )
    sensors = OnlineSensorSession(
        spec.suite,
        pair_id=pair_id,
        sensor_seed=spec.seed,
        control_dt_s=mechanics.control_dt_s,
        config=SensorConfig(),
        fault=None,
        run_id=run_id,
        config_hash=CONFIG_HASH,
        split=spec.role,
    )
    inner = ProbabilityDiagnosisEstimator(
        None if spec.diagnosis == "no_action" else 1.0,
        severity=(
            SELECTED_SEVERITY
            if spec.estimated_severity is None
            else float(spec.estimated_severity)
        ),
        severity_uncertainty=spec.severity_uncertainty,
    )
    estimator = SingleDecisionHoldEstimator(
        inner, first_decision_step=mechanics.first_decision_step
    )
    profile = mechanics.task_profile()
    recovery = GainScheduledRecoveryController(
        RecoveryControlConfig(
            maximum_gain_compensation=spec.maximum_gain_compensation,
            minimum_gain_remaining=spec.minimum_gain_remaining,
        )
    )
    policy = EstimatorRecoveryTaskPolicy(
        ObservedJointPDController(profile, mechanics.controller_config()),
        estimator,
        suite=spec.suite,
        run_id=run_id,
        stride=mechanics.stride,
        recovery_controller=recovery,
    )
    rollout = run_online_rollout(
        plant,
        sensors,
        n_steps=mechanics.n_steps,
        history_steps=mechanics.window_steps,
        command_policy=policy,
        reference_fn=profile.task_reference,
        temperature_fn=lambda _i, time_s: 25.0
        + mechanics.thermal_rate_c_s * time_s,
    )
    if inner.calls == 0:
        raise RuntimeError(f"scheduled diagnosis never fired for {run_id}")

    nominal = np.stack(policy.nominal_commands)
    applied = np.stack(policy.commands)
    changed = np.any(
        ~np.isclose(nominal, applied, rtol=0.0, atol=1.0e-12), axis=1
    )
    decision = mechanics.first_decision_step
    usable = (
        (np.arange(nominal.shape[0]) >= decision)
        & (np.abs(nominal[:, FAULT_LOCATION]) > 1.0e-9)
    )
    if not np.any(usable):
        raise RuntimeError(f"no usable post-decision command ratios for {run_id}")
    ratios = applied[usable, FAULT_LOCATION] / nominal[usable, FAULT_LOCATION]
    expected = expected_multiplier(spec)
    multiplier_error = float(np.max(np.abs(ratios - expected)))
    predecision_hash = _hash_arrays(
        [
            ("q_true", rollout.plant.q_true[:decision]),
            ("qd_true", rollout.plant.qd_true[:decision]),
            ("tau_cmd", rollout.plant.tau_cmd[:decision]),
            ("true_task_output", rollout.plant.true_task_output[:decision]),
        ]
    )
    return {
        "role": spec.role,
        "seed": int(spec.seed),
        "physical_source": spec.physical_source,
        "diagnosis": spec.diagnosis,
        "candidate_label": spec.candidate_label,
        "suite": spec.suite,
        "maximum_gain_compensation": float(spec.maximum_gain_compensation),
        "minimum_gain_remaining": float(spec.minimum_gain_remaining),
        "estimated_severity": (
            None
            if spec.estimated_severity is None
            else float(spec.estimated_severity)
        ),
        "severity_uncertainty": float(spec.severity_uncertainty),
        "expected_multiplier": float(expected),
        "applied_multiplier_mean": float(np.mean(ratios)),
        "applied_multiplier_max_error": multiplier_error,
        "run_id": run_id,
        "j_5s": float(
            j_5s(
                rollout.plant.t_s,
                rollout.plant.task_reference,
                rollout.plant.true_task_output,
                mechanics.fault_onset_s,
            )
        ),
        "predecision_hash": predecision_hash,
        "classification_evaluations": int(estimator.classification_evaluations),
        "recovery_command_changed_steps": int(np.count_nonzero(changed)),
        "predecision_command_changed_steps": int(
            np.count_nonzero(changed[:decision])
        ),
        "a1_incident_steps": int(
            np.count_nonzero(np.any(rollout.plant.safety_flag, axis=1))
        ),
        "saturation_steps": int(
            np.count_nonzero(np.any(rollout.plant.saturation_flag, axis=1))
        ),
        "peak_contact_force_n": float(np.max(rollout.plant.contact_state[:, 0])),
        "max_abs_gauge_microstrain": float(
            np.max(np.abs(rollout.plant.gauge_true))
        ),
    }


def build_tuning_specs(
    candidates: tuple[ActuatorActionCandidate, ...] = CANDIDATES,
) -> list[ActuatorActionArmSpec]:
    """Build shared references plus fault/healthy action arms for tuning."""

    specs: list[ActuatorActionArmSpec] = []
    for candidate in candidates:
        candidate.validate()
    reference = candidates[0]
    for seed in TUNING_SEEDS:
        for source in ("actuator", "healthy"):
            specs.append(
                ActuatorActionArmSpec(
                    "tuning",
                    seed,
                    source,
                    "no_action",
                    "reference",
                    reference.maximum_gain_compensation,
                    reference.minimum_gain_remaining,
                    None,
                    0.0,
                    "S",
                )
            )
        for candidate in candidates:
            for source in ("actuator", "healthy"):
                specs.append(
                    ActuatorActionArmSpec(
                        "tuning",
                        seed,
                        source,
                        "oracle",
                        candidate.label,
                        candidate.maximum_gain_compensation,
                        candidate.minimum_gain_remaining,
                        SELECTED_SEVERITY,
                        0.0,
                        "S",
                    )
                )
    return specs


def _index_rows(
    rows: list[dict[str, Any]],
) -> dict[tuple[str, int, str, str], dict[str, Any]]:
    """Index rows by candidate, seed, physical source, and diagnosis."""

    indexed: dict[tuple[str, int, str, str], dict[str, Any]] = {}
    for row in rows:
        key = (
            str(row["candidate_label"]),
            int(row["seed"]),
            str(row["physical_source"]),
            str(row["diagnosis"]),
        )
        if key in indexed:
            raise ValueError(f"duplicate action arm {key}")
        indexed[key] = row
    return indexed


def _lifecycle_sound(rows: list[dict[str, Any]]) -> bool:
    """Return whether every supplied arm satisfies the mechanism contract."""

    return bool(
        rows
        and all(int(row["classification_evaluations"]) == 1 for row in rows)
        and all(int(row["predecision_command_changed_steps"]) == 0 for row in rows)
        and all(int(row["a1_incident_steps"]) == 0 for row in rows)
        and all(int(row["saturation_steps"]) == 0 for row in rows)
        and all(
            float(row["applied_multiplier_max_error"])
            <= MULTIPLIER_IDENTITY_TOLERANCE
            for row in rows
        )
        and all(
            (
                int(row["recovery_command_changed_steps"]) == 0
                if row["diagnosis"] == "no_action"
                else int(row["recovery_command_changed_steps"]) > 0
            )
            for row in rows
        )
    )


def summarize_tuning_candidates(
    rows: list[dict[str, Any]],
    candidates: tuple[ActuatorActionCandidate, ...] = CANDIDATES,
) -> list[dict[str, Any]]:
    """Summarize fault benefit, healthy benefit, and source specificity."""

    indexed = _index_rows(rows)
    summaries: list[dict[str, Any]] = []
    for candidate in candidates:
        reductions: list[float] = []
        healthy_benefits: list[float] = []
        margins: list[float] = []
        participating: list[dict[str, Any]] = []
        for seed in TUNING_SEEDS:
            fault_no = indexed[("reference", seed, "actuator", "no_action")]
            healthy_no = indexed[("reference", seed, "healthy", "no_action")]
            fault_action = indexed[(candidate.label, seed, "actuator", "oracle")]
            healthy_action = indexed[(candidate.label, seed, "healthy", "oracle")]
            fault_reduction = tracking_reduction_pct(
                float(fault_no["j_5s"]), float(fault_action["j_5s"])
            )
            healthy_benefit = tracking_reduction_pct(
                float(healthy_no["j_5s"]), float(healthy_action["j_5s"])
            )
            reductions.append(fault_reduction)
            healthy_benefits.append(healthy_benefit)
            margins.append(fault_reduction - healthy_benefit)
            participating.extend(
                [fault_no, healthy_no, fault_action, healthy_action]
            )
        lifecycle = _lifecycle_sound(participating)
        summaries.append(
            {
                "candidate_label": candidate.label,
                "maximum_gain_compensation": candidate.maximum_gain_compensation,
                "minimum_gain_remaining": candidate.minimum_gain_remaining,
                "expected_oracle_multiplier": min(
                    1.0
                    / max(
                        SELECTED_SEVERITY, candidate.minimum_gain_remaining
                    ),
                    candidate.maximum_gain_compensation,
                ),
                "mean_fault_reduction_pct": float(np.mean(reductions)),
                "min_fault_reduction_pct": float(np.min(reductions)),
                "mean_healthy_false_authorization_benefit_pct": float(
                    np.mean(healthy_benefits)
                ),
                "mean_source_specific_margin_pp": float(np.mean(margins)),
                "min_source_specific_margin_pp": float(np.min(margins)),
                "tracking_gate_pass": bool(
                    np.min(reductions) >= TUNING_TRACKING_TARGET_PCT
                ),
                "specificity_gate_pass": bool(
                    np.mean(margins) >= CLAIM_TRACKING_BAR_PCT
                    and np.min(margins) > 0.0
                ),
                "lifecycle_safety_gate_pass": lifecycle,
                "seed_margins_pp": [float(value) for value in margins],
            }
        )
    return summaries


def select_candidate(
    summaries: list[dict[str, Any]],
) -> tuple[str, bool]:
    """Select the most source-specific tracking-capable candidate on tuning only."""

    capable = [
        row
        for row in summaries
        if row["tracking_gate_pass"] and row["lifecycle_safety_gate_pass"]
    ]
    pool = capable or [
        row for row in summaries if row["lifecycle_safety_gate_pass"]
    ]
    if not pool:
        raise ValueError("no lifecycle-safe actuator candidate is available")
    selected = sorted(
        pool,
        key=lambda row: (
            -float(row["mean_source_specific_margin_pp"]),
            -float(row["mean_fault_reduction_pct"]),
            float(row["maximum_gain_compensation"]),
            -float(row["minimum_gain_remaining"]),
            str(row["candidate_label"]),
        ),
    )[0]
    return str(selected["candidate_label"]), bool(
        selected["tracking_gate_pass"]
        and selected["specificity_gate_pass"]
        and selected["lifecycle_safety_gate_pass"]
    )


def build_assessment_specs(
    selected_label: str,
    estimates: dict[str, dict[int, float]],
    uncertainties: dict[str, float],
    candidates: tuple[ActuatorActionCandidate, ...] = CANDIDATES,
) -> list[ActuatorActionArmSpec]:
    """Build disjoint references, selected arms, and cap/floor stress arms."""

    by_label = {candidate.label: candidate for candidate in candidates}
    if selected_label not in by_label:
        raise ValueError(f"unknown selected candidate {selected_label}")
    stress_labels = [
        selected_label,
        "cap5_floor0p25",
        "cap5_floor0p20",
    ]
    evaluated = [by_label[label] for label in dict.fromkeys(stress_labels)]
    reference = by_label[selected_label]
    specs: list[ActuatorActionArmSpec] = []
    for seed in ASSESSMENT_SEEDS:
        for source in ("actuator", "healthy"):
            specs.append(
                ActuatorActionArmSpec(
                    "assessment",
                    seed,
                    source,
                    "no_action",
                    "reference",
                    reference.maximum_gain_compensation,
                    reference.minimum_gain_remaining,
                    None,
                    0.0,
                    "S",
                )
            )
        for source in ("actuator", "healthy"):
            specs.append(
                ActuatorActionArmSpec(
                    "assessment",
                    seed,
                    source,
                    "oracle",
                    selected_label,
                    reference.maximum_gain_compensation,
                    reference.minimum_gain_remaining,
                    SELECTED_SEVERITY,
                    0.0,
                    "S",
                )
            )
        for candidate in evaluated:
            for diagnosis in ("C1", "S"):
                for source in ("actuator", "healthy"):
                    specs.append(
                        ActuatorActionArmSpec(
                            "assessment",
                            seed,
                            source,
                            diagnosis,
                            candidate.label,
                            candidate.maximum_gain_compensation,
                            candidate.minimum_gain_remaining,
                            estimates[diagnosis][seed],
                            uncertainties[diagnosis],
                            diagnosis,
                        )
                    )
    return specs


def _bootstrap_margin(
    margins: list[float], *, rng_seed: int
) -> dict[str, Any]:
    """Return a deterministic paired bootstrap interval over seed margins."""

    clusters = [[{"margin_pp": float(value)}] for value in margins]

    def statistic(items: list[dict[str, float]]) -> float:
        return float(np.mean([item["margin_pp"] for item in items]))

    result = hierarchical_bootstrap_ci(
        clusters,
        statistic,
        n_boot=BOOTSTRAP_REPLICATES,
        rng=np.random.default_rng(rng_seed),
    )
    return {
        "point_pp": result.point,
        "ci_low_pp": result.ci_low,
        "ci_high_pp": result.ci_high,
        "ci_level": result.ci_level,
        "n_boot": result.n_boot,
        "excludes_zero": result.excludes_zero,
    }


def summarize_assessment(
    rows: list[dict[str, Any]],
    selected_label: str,
) -> list[dict[str, Any]]:
    """Summarize each assessed candidate/diagnosis with paired uncertainty."""

    indexed = _index_rows(rows)
    combinations = sorted(
        {
            (str(row["candidate_label"]), str(row["diagnosis"]))
            for row in rows
            if row["diagnosis"] != "no_action"
        }
    )
    summaries: list[dict[str, Any]] = []
    for index, (candidate_label, diagnosis) in enumerate(combinations):
        reductions: list[float] = []
        healthy_benefits: list[float] = []
        margins: list[float] = []
        multipliers: list[float] = []
        participating: list[dict[str, Any]] = []
        for seed in ASSESSMENT_SEEDS:
            fault_no = indexed[("reference", seed, "actuator", "no_action")]
            healthy_no = indexed[("reference", seed, "healthy", "no_action")]
            fault_action = indexed[
                (candidate_label, seed, "actuator", diagnosis)
            ]
            healthy_action = indexed[
                (candidate_label, seed, "healthy", diagnosis)
            ]
            fault_reduction = tracking_reduction_pct(
                float(fault_no["j_5s"]), float(fault_action["j_5s"])
            )
            healthy_benefit = tracking_reduction_pct(
                float(healthy_no["j_5s"]), float(healthy_action["j_5s"])
            )
            reductions.append(fault_reduction)
            healthy_benefits.append(healthy_benefit)
            margins.append(fault_reduction - healthy_benefit)
            multipliers.append(float(fault_action["expected_multiplier"]))
            participating.extend(
                [fault_no, healthy_no, fault_action, healthy_action]
            )
        interval = _bootstrap_margin(
            margins, rng_seed=BOOTSTRAP_SEED + index
        )
        lifecycle = _lifecycle_sound(participating)
        summaries.append(
            {
                "candidate_label": candidate_label,
                "diagnosis": diagnosis,
                "is_selected_profile": candidate_label == selected_label,
                "mean_expected_multiplier": float(np.mean(multipliers)),
                "min_expected_multiplier": float(np.min(multipliers)),
                "max_expected_multiplier": float(np.max(multipliers)),
                "mean_fault_reduction_pct": float(np.mean(reductions)),
                "min_fault_reduction_pct": float(np.min(reductions)),
                "mean_healthy_false_authorization_benefit_pct": float(
                    np.mean(healthy_benefits)
                ),
                "mean_source_specific_margin_pp": float(np.mean(margins)),
                "min_source_specific_margin_pp": float(np.min(margins)),
                "seed_margins_pp": [float(value) for value in margins],
                "source_specific_margin_interval": interval,
                "tracking_gate_pass": bool(
                    np.mean(reductions) >= CLAIM_TRACKING_BAR_PCT
                    and np.min(reductions) > 0.0
                ),
                "specificity_gate_pass": bool(
                    interval["point_pp"] >= CLAIM_TRACKING_BAR_PCT
                    and interval["excludes_zero"]
                ),
                "lifecycle_safety_gate_pass": lifecycle,
                "advance_gate_pass": bool(
                    lifecycle
                    and np.mean(reductions) >= CLAIM_TRACKING_BAR_PCT
                    and np.min(reductions) > 0.0
                    and interval["point_pp"] >= CLAIM_TRACKING_BAR_PCT
                    and interval["excludes_zero"]
                ),
            }
        )
    return summaries


def build_audit(
    tuning_rows: list[dict[str, Any]],
    assessment_rows: list[dict[str, Any]],
    recorded_j5s: dict[str, dict[int, float]],
    *,
    selected_label: str,
    n_tuning_specs: int,
    n_assessment_specs: int,
) -> dict[str, Any]:
    """Build every integrity condition required before artifact generation."""

    all_rows = tuning_rows + assessment_rows
    predecision_groups: dict[tuple[str, int, str], set[str]] = {}
    for row in all_rows:
        key = (
            str(row["role"]),
            int(row["seed"]),
            str(row["physical_source"]),
        )
        predecision_groups.setdefault(key, set()).add(
            str(row["predecision_hash"])
        )
    indexed = _index_rows(assessment_rows)
    max_reference_delta = 0.0
    for source in ("healthy", "actuator"):
        for seed in ASSESSMENT_SEEDS:
            observed = float(
                indexed[("reference", seed, source, "no_action")]["j_5s"]
            )
            max_reference_delta = max(
                max_reference_delta,
                abs(observed - float(recorded_j5s[source][seed])),
            )
    reference_rows = [
        row for row in all_rows if row["candidate_label"] == "reference"
    ]
    candidate_rows = [
        row for row in all_rows if row["candidate_label"] != "reference"
    ]
    return {
        "tuning_arm_grid_complete": len(tuning_rows) == n_tuning_specs,
        "assessment_arm_grid_complete": len(assessment_rows)
        == n_assessment_specs,
        "roles_disjoint": set(TUNING_SEEDS).isdisjoint(ASSESSMENT_SEEDS),
        "one_classification_per_arm": all(
            int(row["classification_evaluations"]) == 1 for row in all_rows
        ),
        "no_predecision_action": all(
            int(row["predecision_command_changed_steps"]) == 0
            for row in all_rows
        ),
        "withheld_and_acting_behavior_correct": all(
            (
                int(row["recovery_command_changed_steps"]) == 0
                if row["diagnosis"] == "no_action"
                else int(row["recovery_command_changed_steps"]) > 0
            )
            for row in all_rows
        ),
        "reference_a1_clean": all(
            int(row["a1_incident_steps"]) == 0 for row in reference_rows
        ),
        "reference_saturation_clean": all(
            int(row["saturation_steps"]) == 0 for row in reference_rows
        ),
        "reference_multiplier_identity_pass": all(
            float(row["applied_multiplier_max_error"])
            <= MULTIPLIER_IDENTITY_TOLERANCE
            for row in reference_rows
        ),
        "candidate_a1_incident_arms": sum(
            int(row["a1_incident_steps"]) > 0 for row in candidate_rows
        ),
        "candidate_saturated_arms": sum(
            int(row["saturation_steps"]) > 0 for row in candidate_rows
        ),
        "candidate_multiplier_mismatch_arms": sum(
            float(row["applied_multiplier_max_error"])
            > MULTIPLIER_IDENTITY_TOLERANCE
            for row in candidate_rows
        ),
        "predecision_crn_match": all(
            len(hashes) == 1 for hashes in predecision_groups.values()
        ),
        "recorded_step15_reference_match": max_reference_delta
        <= CRN_REUSE_TOLERANCE,
        "max_recorded_reference_j5s_delta": max_reference_delta,
        "selected_candidate_present_in_assessment": any(
            row["candidate_label"] == selected_label
            and row["diagnosis"] == "oracle"
            for row in assessment_rows
        ),
    }


def require_passing_audit(audit: dict[str, Any]) -> None:
    """Fail before writing artifacts if any required integrity gate is false."""

    required = (
        "tuning_arm_grid_complete",
        "assessment_arm_grid_complete",
        "roles_disjoint",
        "one_classification_per_arm",
        "no_predecision_action",
        "withheld_and_acting_behavior_correct",
        "reference_a1_clean",
        "reference_saturation_clean",
        "reference_multiplier_identity_pass",
        "predecision_crn_match",
        "recorded_step15_reference_match",
        "selected_candidate_present_in_assessment",
    )
    missing = [name for name in required if name not in audit]
    failed = [name for name in required if audit.get(name) is not True]
    if missing or failed:
        raise RuntimeError(
            f"actuator action audit failed; missing={missing}, failed={failed}"
        )


def _run_specs(
    specs: list[ActuatorActionArmSpec], *, workers: int
) -> list[dict[str, Any]]:
    """Run specs serially or in a process pool and return sorted rows."""

    if workers < 1:
        raise ValueError("workers must be >= 1")
    if workers == 1:
        rows = [run_arm(spec) for spec in specs]
    else:
        with concurrent.futures.ProcessPoolExecutor(max_workers=workers) as pool:
            rows = list(pool.map(run_arm, specs))
    return sorted(
        rows,
        key=lambda row: (
            row["role"],
            int(row["seed"]),
            row["physical_source"],
            row["candidate_label"],
            row["diagnosis"],
        ),
    )


def run(
    *,
    workers: int,
    severity_summary: Path,
    severity_arm_rows: Path,
) -> dict[str, Any]:
    """Run tuning, select without assessment leakage, then assess disjointly."""

    estimates, uncertainties, recorded_j5s = load_recorded_inputs(
        severity_summary, severity_arm_rows
    )
    tuning_specs = build_tuning_specs()
    print(f"Running {len(tuning_specs)} tuning actuator-action arms...")
    tuning_rows = _run_specs(tuning_specs, workers=workers)
    candidate_summaries = summarize_tuning_candidates(tuning_rows)
    selected_label, tuning_advance = select_candidate(candidate_summaries)
    print(f"Selected {selected_label} on tuning only.")
    assessment_specs = build_assessment_specs(
        selected_label, estimates, uncertainties
    )
    print(f"Running {len(assessment_specs)} disjoint assessment arms...")
    assessment_rows = _run_specs(assessment_specs, workers=workers)
    assessment_summaries = summarize_assessment(
        assessment_rows, selected_label
    )
    audit = build_audit(
        tuning_rows,
        assessment_rows,
        recorded_j5s,
        selected_label=selected_label,
        n_tuning_specs=len(tuning_specs),
        n_assessment_specs=len(assessment_specs),
    )
    require_passing_audit(audit)
    selected_results = {
        row["diagnosis"]: row
        for row in assessment_summaries
        if row["candidate_label"] == selected_label
    }
    required_diagnoses = {"oracle", "C1", "S"}
    all_selected_present = set(selected_results) == required_diagnoses
    selected_all_advance = bool(
        all_selected_present
        and all(
            selected_results[name]["advance_gate_pass"]
            for name in required_diagnoses
        )
    )
    decision = (
        "ADVANCE_ACTUATOR_ACTION_MECHANISM_TO_CALIBRATED_AUTHORIZATION_REVIEW_ONLY"
        if tuning_advance and selected_all_advance
        else "BLOCK_ACTUATOR_ACTION_FAMILY_AT_SOURCE_SPECIFIC_GATE"
    )
    return {
        "screen_spec": {
            "selected_fault_remaining_gain": SELECTED_SEVERITY,
            "fault_location": FAULT_LOCATION,
            "plane_z_m": PLANE_Z_M,
            "claim_tracking_bar_pct": CLAIM_TRACKING_BAR_PCT,
            "tuning_tracking_target_pct": TUNING_TRACKING_TARGET_PCT,
            "tuning_seeds": list(TUNING_SEEDS),
            "assessment_seeds": list(ASSESSMENT_SEEDS),
            "bootstrap_replicates": BOOTSTRAP_REPLICATES,
            "bootstrap_seed": BOOTSTRAP_SEED,
            "config_hash": CONFIG_HASH,
            "candidates": [
                {
                    "label": candidate.label,
                    "maximum_gain_compensation": candidate.maximum_gain_compensation,
                    "minimum_gain_remaining": candidate.minimum_gain_remaining,
                }
                for candidate in CANDIDATES
            ],
        },
        "recorded_deployable_inputs": {
            "severity_estimates": estimates,
            "bias_inclusive_rms_uncertainty": uncertainties,
        },
        "candidate_summaries": candidate_summaries,
        "selected_candidate": selected_label,
        "tuning_selected_gate_pass": tuning_advance,
        "assessment_summaries": assessment_summaries,
        "selected_all_diagnoses_advance": selected_all_advance,
        "audit": audit,
        "decision": decision,
        "n_tuning_arms": len(tuning_rows),
        "n_assessment_arms": len(assessment_rows),
        "tuning_rows": tuning_rows,
        "assessment_rows": assessment_rows,
    }


def _jsonable(value: Any) -> Any:
    """Convert NumPy scalars recursively to strict-JSON-compatible values."""

    if isinstance(value, dict):
        return {str(key): _jsonable(item) for key, item in value.items()}
    if isinstance(value, (list, tuple)):
        return [_jsonable(item) for item in value]
    if isinstance(value, np.generic):
        return value.item()
    return value


def write_csv(path: Path, rows: list[dict[str, Any]]) -> None:
    """Write homogeneous row dictionaries as a deterministic CSV."""

    if not rows:
        raise ValueError(f"cannot write empty CSV {path}")
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(
            handle,
            fieldnames=[
                key
                for key in rows[0]
                if not isinstance(rows[0][key], (list, dict))
            ],
        )
        writer.writeheader()
        for row in rows:
            writer.writerow(
                {
                    key: value
                    for key, value in row.items()
                    if key in writer.fieldnames
                }
            )


def write_report(path: Path, summary: dict[str, Any]) -> None:
    """Write a human-readable report generated only from ``summary``."""

    selected = summary["selected_candidate"]
    candidates = summary["candidate_summaries"]
    assessment = summary["assessment_summaries"]
    selected_rows = [
        row for row in assessment if row["candidate_label"] == selected
    ]
    lines = [
        "# Actuator Recovery Action Screen",
        "",
        f"**Decision:** `{summary['decision']}`",
        "",
        "## Question and evidence boundary",
        "",
        "At the bounded task's selected 0.25 remaining-gain condition, can a "
        "bounded inverse-gain action recover tracking source-specifically rather "
        "than merely improve any arm that is authorized to act? This is a "
        "development action-mechanism screen. It is not calibrated authorization, "
        "a C1-versus-S control result, validation-sized evidence, or a frozen config.",
        "",
        "Three tuning seeds choose from the predeclared cap/floor family using both "
        "fault recovery and the same diagnosis falsely authorized on healthy. Four "
        "disjoint assessment seeds then evaluate the tuning-selected profile with "
        "oracle severity and the already-recorded C1/S held-out severity estimates. "
        "The 95% interval resamples only four physical seeds, so it is a sign-stability "
        "guard rather than a confirmatory uncertainty statement.",
        "",
        "## Tuning-only cap/floor family",
        "",
        "| candidate | cap | floor | oracle m | fault reduction | healthy false-auth benefit | source-specific margin | gates |",
        "|---|---:|---:|---:|---:|---:|---:|---|",
    ]
    for row in candidates:
        gates = (
            "PASS"
            if row["tracking_gate_pass"]
            and row["specificity_gate_pass"]
            and row["lifecycle_safety_gate_pass"]
            else "BLOCK"
        )
        lines.append(
            f"| {row['candidate_label']} | "
            f"{row['maximum_gain_compensation']:.2f} | "
            f"{row['minimum_gain_remaining']:.2f} | "
            f"{row['expected_oracle_multiplier']:.3f} | "
            f"{row['mean_fault_reduction_pct']:.3f}% "
            f"(min {row['min_fault_reduction_pct']:.3f}%) | "
            f"{row['mean_healthy_false_authorization_benefit_pct']:.3f}% | "
            f"{row['mean_source_specific_margin_pp']:.3f} pp "
            f"(min {row['min_source_specific_margin_pp']:.3f}) | {gates} |"
        )
    lines.extend(
        [
            "",
            f"Tuning selected **`{selected}`** by source-specific margin among "
            "tracking-capable, lifecycle-safe candidates; assessment was not read "
            "during selection.",
            "",
            "## Disjoint assessment",
            "",
            "| profile | diagnosis | multiplier range | fault reduction | healthy false-auth benefit | source-specific margin (95% paired bootstrap) | gate |",
            "|---|---|---:|---:|---:|---:|---|",
        ]
    )
    for row in assessment:
        interval = row["source_specific_margin_interval"]
        lines.append(
            f"| {row['candidate_label']} | {row['diagnosis']} | "
            f"{row['min_expected_multiplier']:.3f}–"
            f"{row['max_expected_multiplier']:.3f} | "
            f"{row['mean_fault_reduction_pct']:.3f}% "
            f"(min {row['min_fault_reduction_pct']:.3f}%) | "
            f"{row['mean_healthy_false_authorization_benefit_pct']:.3f}% | "
            f"{row['mean_source_specific_margin_pp']:.3f} pp "
            f"[{interval['ci_low_pp']:.3f}, {interval['ci_high_pp']:.3f}] | "
            f"{'PASS' if row['advance_gate_pass'] else 'BLOCK'} |"
        )
    lines.extend(
        [
            "",
            "## Interpretation",
            "",
        ]
    )
    if summary["decision"].startswith("ADVANCE"):
        lines.extend(
            [
                "The tuning-selected actuator action clears the development tracking "
                "and source-specificity gates under oracle, C1, and S severity inputs. "
                "This advances the **action mechanism only** to a calibrated "
                "authorization review. It does not establish an S advantage: the "
                "fixture forces the class call, location, non-abstention, and action "
                "probability to agree, and the C1/S severity estimates are already "
                "known to be similar.",
                "",
                "The healthy false-authorization stress remains load-bearing. The "
                "reported source-specific margin credits only the fault benefit beyond "
                "what the identical diagnosis-conditioned action does to a healthy arm. "
                "Actual healthy false-authorization *rates* require calibrated class, "
                "abstention, and uncertainty outputs and remain open.",
            ]
        )
    else:
        lines.extend(
            [
                "No candidate clears the development source-specific gate through "
                "disjoint assessment. The action family therefore remains blocked; "
                "larger raw fault recovery is not promoted when the same authorization "
                "also improves or harms a healthy arm enough to consume the margin, or "
                "when the candidate violates the lifecycle/safety contract.",
            ]
        )
    lines.extend(
        [
            "",
            "The cap-5 profiles are sensitivity arms, not extra selected candidates. "
            "Comparing `cap5_floor0p25` with `cap5_floor0p20` isolates whether lowering "
            "the floor lets recorded severity underestimates command above exact "
            "restoration. Any effect is reported in tracking units rather than inferred "
            "from multiplier differences.",
            "",
            "All arms use one held decision, no pre-decision recovery, and exact "
            "within-source pre-decision CRN matching. Reference arms retain zero A1 "
            "incidents, zero saturation, and commanded-versus-applied multiplier "
            "identity. Candidate violations remain visible as scientific block evidence: "
            f"{summary['audit']['candidate_a1_incident_arms']} candidate arms with A1 "
            f"incidents, {summary['audit']['candidate_saturated_arms']} with saturation, "
            f"and {summary['audit']['candidate_multiplier_mismatch_arms']} with multiplier "
            "mismatch. Assessment references reproduce the approved severity screen's "
            "committed no-action J5 values.",
            "",
            "## Selected-profile assessment detail",
            "",
        ]
    )
    for row in selected_rows:
        lines.append(
            f"- **{row['diagnosis']} severity:** fault reduction "
            f"{row['mean_fault_reduction_pct']:.3f}%; healthy false-authorization "
            f"benefit {row['mean_healthy_false_authorization_benefit_pct']:.3f}%; "
            f"source-specific margin {row['mean_source_specific_margin_pp']:.3f} pp."
        )
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text("\n".join(lines) + "\n", encoding="utf-8")


def main() -> int:
    """Run the screen, fail on integrity, and write deterministic artifacts."""

    args = parse_args()
    if args.workers < 1:
        raise ValueError("--workers must be >= 1")
    summary = run(
        workers=args.workers,
        severity_summary=args.severity_summary,
        severity_arm_rows=args.severity_arm_rows,
    )
    output_dir: Path = args.output_dir
    output_dir.mkdir(parents=True, exist_ok=True)
    tuning_rows = summary.pop("tuning_rows")
    assessment_rows = summary.pop("assessment_rows")
    strict = _jsonable(summary)
    (output_dir / "summary.json").write_text(
        json.dumps(strict, indent=2, sort_keys=True, allow_nan=False) + "\n",
        encoding="utf-8",
    )
    write_csv(output_dir / "tuning_rows.csv", tuning_rows)
    write_csv(output_dir / "assessment_rows.csv", assessment_rows)
    write_csv(output_dir / "candidate_summary.csv", strict["candidate_summaries"])
    write_report(output_dir / "actuator_recovery_action_report.md", strict)
    print(strict["decision"])
    print(f"Wrote actuator recovery action screen to {output_dir}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
