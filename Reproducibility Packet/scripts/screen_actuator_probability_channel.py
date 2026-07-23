"""Measure what the class-probability channel is worth at the selected actuator condition.

This is the last channel through which two sensor suites that both call the actuator class
correctly could still command different recovery actions. The recovery controller's
actuator branch is, verbatim:

    probability = float(output.p_class[ACTUATOR_INDEX])
    multiplier = 1.0 + probability * (capped_compensation - 1.0)

and `_confident_source` withholds the action entirely below
`source_probability_threshold`. Two facts make the channel exactly measurable at the
deficit screen's selected `actuator_gain_remaining_0p25` case:

1. **The severity channel is structurally flat here.** `capped_compensation` is
   `min(1 / max(severity, minimum_gain_remaining), maximum_gain_compensation)`. With the
   recorded floor `0.25` and cap `2.0`, *every* severity estimate at or below `0.50`
   produces `capped_compensation = 2.0` exactly. Both suites estimate remaining gain to
   within roughly 0.008, so on a true `0.25` both land far inside that flat region. No
   severity difference can survive to the plant at this condition.
2. **The probability channel is closed on both ends by recorded constants.** The gate
   closes it below at `source_probability_threshold`; the cap closes it above at
   `maximum_gain_compensation`. So the reachable commanded multiplier is exactly
   `[1 + threshold * (cap - 1), cap]` — here `[1.50, 2.00]` — and the screen sweeps that
   whole set rather than a chosen sub-range. This is a reachable-set span, not an
   extrapolated bound: it is closed by the controller's own constants, and it is reported
   separately from the gate discontinuity below.

The action is cap-saturated throughout. Exact restoration of a `0.25` remaining gain needs
a multiplier of `4.0`; the recorded cap allows `2.0`. Even a maximally confident diagnosis
therefore under-restores by a factor of two, which is why the realized-versus-analytic
ratio is measured here rather than assumed from the boundary condition.

Common random numbers are reused from the deficit screen, not asserted: the no-action and
healthy arms re-run that screen's trajectories under its own `pair_id`s and their `J_5s`
values are checked against its committed rows, and every integrity condition is a
fail-loud gate.

Run from `Reproducibility Packet/`:
    .\\.venv\\Scripts\\python.exe scripts\\screen_actuator_probability_channel.py --workers 8

Development-sized screen at an unfrozen config. Not a confirmatory result.
"""

from __future__ import annotations

import argparse
import concurrent.futures
import csv
import json
import sys
from dataclasses import dataclass
from pathlib import Path
from typing import Any

import numpy as np

sys.path.insert(0, str(Path(__file__).resolve().parent))

from screen_bounded_task_contact import (  # noqa: E402
    BoundedTaskContactSpec,
    SingleDecisionHoldEstimator,
    cable_config,
)
from utils.cable_plant import CablePlant  # noqa: E402
from utils.estimator import SOURCE_CLASS_ORDER, EstimatorOutput  # noqa: E402
from utils.metrics import j_5s, tracking_reduction_pct  # noqa: E402
from utils.online_loop import run_online_rollout  # noqa: E402
from utils.recovery_control import RecoveryControlConfig  # noqa: E402
from utils.schema_types import FaultSpec  # noqa: E402
from utils.sensor_model import OnlineSensorSession, SensorConfig  # noqa: E402
from utils.task_control import (  # noqa: E402
    EstimatorRecoveryTaskPolicy,
    ObservedJointPDController,
)

# --------------------------------------------------------------------------- #
# Pre-declared screen constants. Development values; `config.json` is not frozen.
# --------------------------------------------------------------------------- #

#: The deficit screen's selected actuator case: 0.25 remaining joint-1 delivered gain.
#: This is the condition its action screen will run on, so it is the condition where the
#: probability channel matters.
SELECTED_SEVERITY = 0.25

#: The deficit screen's disjoint assessment seeds, reused verbatim together with its
#: `pair_id`s so each arm's sensor noise realization is that screen's.
ASSESSMENT_SEEDS: tuple[int, ...] = (16100, 16101, 16102, 16103)

#: Swept actuator class probabilities, strictly interior to the gate and the certain
#: end. The gate boundary and `p = 1` are supplied by their own dedicated arms so this
#: sweep can never silently duplicate either endpoint.
PROBABILITY_SWEEP: tuple[float, ...] = (0.60, 0.70, 0.80, 0.90)

#: One probability just below `source_probability_threshold`. The actuator class is still
#: the unique argmax here, so this arm isolates the *threshold*, not the class call, and
#: must produce no action at all.
GATE_PROBE_PROBABILITY = 0.49

#: Contact plane height, matching the bounded profile every recent screen uses.
PLANE_Z_M = 0.200

#: The Claim Sheet's control bar, in reduction percent.
CLAIM_TRACKING_BAR_PCT = 10.0

#: Development config hash. `dev-` prefixed: no `dev-` trace may enter confirmatory analysis.
CONFIG_HASH = "dev-actuator-probability-channel-screen"

#: Joint carrying the actuator fault.
FAULT_LOCATION = 1

#: Tolerance on the deficit-screen cross-check. The arms share a seed, a `pair_id`, and a
#: plant, so the trajectories are expected to agree exactly; this is a guard against
#: silent harness drift, not a statistical tolerance.
CRN_REUSE_TOLERANCE = 1.0e-12

#: Tolerance on the commanded-versus-applied multiplier identity `m = 1 + p (cap - 1)`.
MULTIPLIER_IDENTITY_TOLERANCE = 1.0e-9


# --------------------------------------------------------------------------- #
# Part 0 — the uncertainty this screen hands the controller's confidence gate.
# --------------------------------------------------------------------------- #
def recorded_assessment_rms(path: Path) -> dict[str, float]:
    """Return each suite's bias-inclusive severity error scale from Step 15's rows.

    The controller's gate compares one scalar against `maximum_severity_uncertainty`, and
    the schema does not fix which statistic that scalar is. A residual *standard
    deviation* discards the bias, so a systematically wrong but tightly clustered read-out
    passes a gate it should fail. This screen therefore hands the gate a root-mean-square
    residual, which counts bias and dispersion together, and records both so the choice is
    auditable rather than implicit.

    Args:
        path: Step 15's `severity_estimation_quality/summary.json`.

    Returns:
        Suite-keyed record carrying the RMS, standard deviation, and bias of the disjoint
        assessment residuals.

    Raises:
        ValueError: If a suite has fewer than two finite assessment predictions.
    """

    summary = json.loads(path.read_text(encoding="utf-8"))
    scales: dict[str, float] = {}
    for suite, evaluation in sorted(summary["suite_evaluations"].items()):
        residuals = np.asarray(
            [
                float(row["estimate"]) - float(row["severity"])
                for row in evaluation.get("predictions", [])
            ],
            dtype=float,
        )
        if residuals.size < 2 or not np.all(np.isfinite(residuals)):
            raise ValueError(
                f"suite {suite} has too few finite assessment predictions for an RMS"
            )
        scales[suite] = {
            "assessment_residual_rms": float(np.sqrt(np.mean(residuals**2))),
            "assessment_residual_std": float(residuals.std(ddof=1)),
            "assessment_residual_bias": float(residuals.mean()),
            "n_assessment_residuals": int(residuals.size),
        }
    return scales


def gate_uncertainty_from_scales(scales: dict[str, Any], *, limit: float) -> float:
    """Return the conservative severity uncertainty to report at every acting arm.

    The larger suite's RMS is used so no arm is advantaged by an optimistic uncertainty.
    The gate is a threshold test, so any value inside it commands identically; reporting
    the conservative one makes that insensitivity explicit instead of assumed.

    Args:
        scales: Output of `recorded_assessment_rms`.
        limit: The controller's `maximum_severity_uncertainty`.

    Returns:
        The maximum recorded RMS across suites.

    Raises:
        ValueError: If the conservative value would not open the gate, which would make
            every acting arm silently identical to no action.
    """

    worst = max(float(record["assessment_residual_rms"]) for record in scales.values())
    if not worst <= limit:
        raise ValueError(
            f"conservative severity RMS {worst:.6f} does not clear the gate {limit:g}; "
            "every acting arm would silently collapse to no action"
        )
    return worst


# --------------------------------------------------------------------------- #
# Part 1 — the reachable probability set, derived from the recorded constants.
# --------------------------------------------------------------------------- #
def reachable_multiplier_set(config: RecoveryControlConfig, severity: float) -> dict[str, Any]:
    """Return the commanded-multiplier interval the probability channel can reach.

    Both ends come from recorded controller constants rather than from a chosen grid: the
    confidence gate closes the interval below at `source_probability_threshold`, and
    `capped_compensation` closes it above. That is what makes the swept span a
    reachable-set span instead of an extrapolation.

    Args:
        config: The recovery-controller settings in force.
        severity: Commanded remaining-gain estimate.

    Returns:
        The capped compensation, the reachable multiplier endpoints, whether the cap binds
        (so the severity channel is flat), and the severity above which it stops binding.
    """

    effective_remaining = max(float(severity), config.minimum_gain_remaining)
    ideal = 1.0 / effective_remaining
    capped = min(ideal, config.maximum_gain_compensation)
    threshold = config.source_probability_threshold
    return {
        "ideal_compensation": float(ideal),
        "capped_compensation": float(capped),
        "cap_binds": bool(ideal > config.maximum_gain_compensation),
        "severity_flat_at_or_below": float(1.0 / config.maximum_gain_compensation),
        "probability_threshold": float(threshold),
        "reachable_multiplier_low": float(1.0 + threshold * (capped - 1.0)),
        "reachable_multiplier_high": float(capped),
        "exact_restoration_multiplier": float(1.0 / float(severity)),
        "cap_shortfall_factor": float((1.0 / float(severity)) / capped),
    }


def expected_multiplier(probability: float, capped_compensation: float) -> float:
    """Return the controller's commanded multiplier for one class probability.

    Args:
        probability: Actuator-class probability reported by the diagnosis.
        capped_compensation: The controller's capped compensation at this severity.

    Returns:
        `1 + probability * (capped_compensation - 1)`.
    """

    return 1.0 + float(probability) * (float(capped_compensation) - 1.0)


# --------------------------------------------------------------------------- #
# Part 2 — the arms.
# --------------------------------------------------------------------------- #
class ProbabilityDiagnosisEstimator:
    """Return one pre-set actuator diagnosis at a chosen class probability.

    Every acting arm reports the same severity and differs only in the actuator-class
    probability, which isolates the probability channel. The remaining probability mass is
    spread evenly across the other three classes so the actuator stays the unique argmax
    even at the gate probe — the probe therefore tests the *threshold*, not the class call.
    A `None` probability is the no-action arm: a healthy one-hot call.
    """

    def __init__(
        self,
        probability: float | None,
        *,
        severity: float,
        severity_uncertainty: float,
    ) -> None:
        """Bind the diagnosis this estimator reports at every decision.

        Args:
            probability: Actuator-class probability in `(0, 1]`, or `None` for a healthy
                call that the recovery controller never acts on.
            severity: Reported remaining-gain estimate in `(0, 1]`.
            severity_uncertainty: Reported severity error scale.

        Raises:
            ValueError: If the probability, severity, or uncertainty is out of range, or
                if the probability is too small for the actuator to be the unique argmax.
        """

        if probability is not None:
            value = float(probability)
            if not 0.0 < value <= 1.0:
                raise ValueError("probability must be None or in (0, 1]")
            others = (1.0 - value) / (len(SOURCE_CLASS_ORDER) - 1)
            if value <= others:
                raise ValueError(
                    f"probability {value} does not make actuator the unique argmax "
                    f"(each other class would hold {others:.4f}); the arm would test the "
                    "class call rather than the probability channel"
                )
        if not 0.0 < float(severity) <= 1.0:
            raise ValueError("severity must be in (0, 1]")
        if not np.isfinite(severity_uncertainty) or severity_uncertainty < 0.0:
            raise ValueError("severity_uncertainty must be finite and non-negative")
        self.probability = None if probability is None else float(probability)
        self.severity = float(severity)
        self.severity_uncertainty = float(severity_uncertainty)
        self.calls = 0

    def reset(self) -> None:
        """Clear the call count before a new rollout."""

        self.calls = 0

    def update(self, step_index: int, decision_time_s: float, window) -> EstimatorOutput:
        """Return the pre-set diagnosis, ignoring the observed window."""

        self.calls += 1
        probabilities = np.zeros(len(SOURCE_CLASS_ORDER), dtype=float)
        if self.probability is None:
            probabilities[SOURCE_CLASS_ORDER.index("healthy")] = 1.0
        else:
            others = (1.0 - self.probability) / (len(SOURCE_CLASS_ORDER) - 1)
            probabilities[:] = others
            probabilities[SOURCE_CLASS_ORDER.index("actuator")] = self.probability
        output = EstimatorOutput(
            step=step_index,
            decision_time_s=decision_time_s,
            p_class=probabilities,
            unknown_score=0.0,
            abstain_decision=False,
            location_out=-1 if self.probability is None else FAULT_LOCATION,
            severity_out=0.0 if self.probability is None else self.severity,
            severity_uncertainty=(
                float("inf") if self.probability is None else self.severity_uncertainty
            ),
            detection_time_s=float("nan") if self.probability is None else decision_time_s,
        )
        output.validate()
        return output


@dataclass(frozen=True)
class ProbabilityArmSpec:
    """One rollout at the selected condition under one commanded class probability."""

    seed: int
    label: str
    #: Commanded actuator-class probability, or `None` for the no-action arm.
    probability: float | None
    #: Reported severity uncertainty; only its position relative to the gate matters.
    severity_uncertainty: float
    #: Whether the plant carries the actuator fault. `False` is the healthy reference.
    faulted: bool
    suite: str = "S"


def run_probability_arm(spec: ProbabilityArmSpec) -> dict[str, Any]:
    """Run one arm and return its tracking integral and audit fields.

    The `pair_id` and sensor seed are the deficit screen's, so the no-action and healthy
    arms reproduce that screen's recorded trajectories exactly and the acting arms share
    their noise realization.

    Args:
        spec: The arm to run.

    Returns:
        A row carrying `j_5s`, the applied multiplier at the faulted joint, and the
        lifecycle/safety audit fields every screen in this packet records.

    Raises:
        RuntimeError: If the scheduled decision never fired.
    """

    mechanics = BoundedTaskContactSpec(
        plane_heights_z_m=(0.100, PLANE_Z_M), sensor_seed=spec.seed
    )
    # The deficit screen's `pair_id`, verbatim: same sensor RNG substreams.
    pair_id = f"fault-deficit-assessment-{spec.seed}"
    run_id = f"probability-{spec.label}-{spec.seed}-{spec.suite}"
    fault = (
        FaultSpec(
            source_class="actuator",
            subtype="actuator_gain_loss",
            location=FAULT_LOCATION,
            severity=SELECTED_SEVERITY,
            onset_index=mechanics.onset_index,
        )
        if spec.faulted
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
        split="assessment",
    )
    inner = ProbabilityDiagnosisEstimator(
        spec.probability,
        severity=SELECTED_SEVERITY,
        severity_uncertainty=spec.severity_uncertainty,
    )
    estimator = SingleDecisionHoldEstimator(
        inner, first_decision_step=mechanics.first_decision_step
    )
    profile = mechanics.task_profile()
    policy = EstimatorRecoveryTaskPolicy(
        ObservedJointPDController(profile, mechanics.controller_config()),
        estimator,
        suite=spec.suite,
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
        temperature_fn=lambda _i, time_s: 25.0 + mechanics.thermal_rate_c_s * time_s,
    )
    if inner.calls == 0:
        raise RuntimeError(f"the scheduled decision never fired for {run_id}")
    nominal = np.stack(policy.nominal_commands)
    applied = np.stack(policy.commands)
    changed_mask = np.any(~np.isclose(nominal, applied, rtol=0.0, atol=1e-12), axis=1)
    usable = np.abs(nominal[:, FAULT_LOCATION]) > 1.0e-9
    ratios = (
        applied[usable, FAULT_LOCATION] / nominal[usable, FAULT_LOCATION]
        if np.any(usable)
        else np.array([1.0])
    )
    return {
        "seed": int(spec.seed),
        "label": spec.label,
        "faulted": bool(spec.faulted),
        "probability": (None if spec.probability is None else float(spec.probability)),
        "severity_uncertainty": float(spec.severity_uncertainty),
        "run_id": run_id,
        "j_5s": float(
            j_5s(
                rollout.plant.t_s,
                rollout.plant.task_reference,
                rollout.plant.true_task_output,
                mechanics.fault_onset_s,
            )
        ),
        "applied_multiplier_max": float(np.max(ratios)),
        "classification_evaluations": int(estimator.classification_evaluations),
        "recovery_command_changed_steps": int(np.count_nonzero(changed_mask)),
        "a1_incident_steps": int(
            np.count_nonzero(np.any(rollout.plant.safety_flag, axis=1))
        ),
        "saturation_steps": int(
            np.count_nonzero(np.any(rollout.plant.saturation_flag, axis=1))
        ),
        "peak_contact_force_n": float(np.max(rollout.plant.contact_state[:, 0])),
        "max_abs_gauge_microstrain": float(np.max(np.abs(rollout.plant.gauge_true))),
    }


def probability_label(probability: float) -> str:
    """Return the canonical arm label for one swept probability."""

    return f"probability_{probability:.2f}".replace(".", "p")


def build_arm_specs(
    *,
    gate_uncertainty: float,
    seeds: tuple[int, ...] = ASSESSMENT_SEEDS,
    probabilities: tuple[float, ...] = PROBABILITY_SWEEP,
    config: RecoveryControlConfig | None = None,
) -> list[ProbabilityArmSpec]:
    """Return every arm: two references, the gate endpoints, the probe, and the sweep.

    Args:
        gate_uncertainty: Severity uncertainty reported at every acting arm.
        seeds: Assessment seeds to run.
        probabilities: Swept probabilities, each strictly between the gate threshold and
            one. The threshold and `p = 1` endpoints are supplied by dedicated arms.
        config: Recovery-controller settings; defaults to the recorded development values.

    Returns:
        One `ProbabilityArmSpec` per arm.

    Raises:
        ValueError: If a swept probability is not strictly interior to
            `(source_probability_threshold, 1)`.
    """

    base = config or RecoveryControlConfig()
    threshold = base.source_probability_threshold
    for probability in probabilities:
        if not threshold < probability < 1.0:
            raise ValueError(
                f"swept probability {probability} is outside ({threshold:g}, 1); the "
                "gate boundary and the certain endpoint are supplied by their own arms"
            )
    specs: list[ProbabilityArmSpec] = []
    for seed in seeds:
        specs.append(
            ProbabilityArmSpec(
                seed=seed,
                label="no_action",
                probability=None,
                severity_uncertainty=gate_uncertainty,
                faulted=True,
            )
        )
        specs.append(
            ProbabilityArmSpec(
                seed=seed,
                label="healthy_reference",
                probability=None,
                severity_uncertainty=gate_uncertainty,
                faulted=False,
            )
        )
        specs.append(
            ProbabilityArmSpec(
                seed=seed,
                label="gate_probe",
                probability=GATE_PROBE_PROBABILITY,
                severity_uncertainty=gate_uncertainty,
                faulted=True,
            )
        )
        specs.append(
            ProbabilityArmSpec(
                seed=seed,
                label=probability_label(threshold),
                probability=threshold,
                severity_uncertainty=gate_uncertainty,
                faulted=True,
            )
        )
        for probability in probabilities:
            specs.append(
                ProbabilityArmSpec(
                    seed=seed,
                    label=probability_label(probability),
                    probability=probability,
                    severity_uncertainty=gate_uncertainty,
                    faulted=True,
                )
            )
        specs.append(
            ProbabilityArmSpec(
                seed=seed,
                label=probability_label(1.0),
                probability=1.0,
                severity_uncertainty=gate_uncertainty,
                faulted=True,
            )
        )
    return specs


# --------------------------------------------------------------------------- #
# Part 3 — analysis.
# --------------------------------------------------------------------------- #
def _by_label(rows: list[dict[str, Any]]) -> dict[tuple[str, int], dict[str, Any]]:
    """Index arm rows by `(label, seed)`, failing loudly on a duplicate."""

    indexed: dict[tuple[str, int], dict[str, Any]] = {}
    for row in rows:
        key = (row["label"], int(row["seed"]))
        if key in indexed:
            raise ValueError(f"duplicate arm {key}")
        indexed[key] = row
    return indexed


def probability_response_curve(
    rows: list[dict[str, Any]],
    *,
    seeds: tuple[int, ...] = ASSESSMENT_SEEDS,
    probabilities: tuple[float, ...] = PROBABILITY_SWEEP,
    config: RecoveryControlConfig | None = None,
) -> dict[str, Any]:
    """Return tracking reduction versus no-action as a function of class probability.

    Each point is paired per seed against that seed's own no-action arm, so the curve is
    a within-noise-realization comparison rather than a between-seed one.

    Args:
        rows: All arm rows.
        seeds: Assessment seeds.
        probabilities: The interior swept probabilities.
        config: Recovery-controller settings; defaults to the recorded development values.

    Returns:
        One point per probability with mean/min/max reduction and mean applied multiplier,
        plus the reachable-set span and the local slope at the certain end.

    Raises:
        ValueError: If a required arm is missing.
    """

    base = config or RecoveryControlConfig()
    indexed = _by_label(rows)
    ordered = (base.source_probability_threshold, *probabilities, 1.0)
    points: list[dict[str, Any]] = []
    for probability in ordered:
        label = probability_label(probability)
        reductions: list[float] = []
        applied: list[float] = []
        for seed in seeds:
            try:
                arm = indexed[(label, seed)]
                no_action = indexed[("no_action", seed)]
            except KeyError as error:  # pragma: no cover - guarded by build_arm_specs
                raise ValueError(f"missing arm {label} for seed {seed}") from error
            reductions.append(tracking_reduction_pct(no_action["j_5s"], arm["j_5s"]))
            applied.append(arm["applied_multiplier_max"])
        values = np.asarray(reductions, dtype=float)
        points.append(
            {
                "probability": float(probability),
                "mean_applied_multiplier": float(np.mean(applied)),
                "mean_reduction_vs_no_action_pct": float(values.mean()),
                "min_reduction_vs_no_action_pct": float(values.min()),
                "max_reduction_vs_no_action_pct": float(values.max()),
            }
        )
    means = [point["mean_reduction_vs_no_action_pct"] for point in points]
    slope = 0.0
    if len(points) >= 2:
        run = points[-1]["probability"] - points[-2]["probability"]
        slope = (means[-1] - means[-2]) / run if run else 0.0
    return {
        "points": points,
        "probability_span": [
            float(points[0]["probability"]),
            float(points[-1]["probability"]),
        ],
        "reachable_reduction_span_pct": float(max(means) - min(means)),
        "reduction_at_gate_pct": float(means[0]),
        "reduction_at_certainty_pct": float(means[-1]),
        "local_slope_pct_per_unit_probability": float(slope),
        "claim_bar_pct": CLAIM_TRACKING_BAR_PCT,
        "reachable_span_clears_bar": bool(
            (max(means) - min(means)) >= CLAIM_TRACKING_BAR_PCT
        ),
    }


def gate_discontinuity(
    curve: dict[str, Any], *, probe_reduction_pct: float
) -> dict[str, Any]:
    """Return the jump the confidence gate creates at its threshold.

    The graded channel and the gate are separate quantities and are reported separately.
    Below the threshold the controller withholds the action entirely, so the reduction is
    the no-action arm's zero; at the threshold it is already the full gate-entry value.
    A difference that large is a *gate-crossing* difference — one suite authorizing the
    action and the other not — which is a class-call-scale quantity, not a probability
    precision one.

    Args:
        curve: Output of `probability_response_curve`.
        probe_reduction_pct: Measured reduction of the sub-threshold probe arm.

    Returns:
        The jump size, the graded span, and each one's comparison with the bar.
    """

    jump = float(curve["reduction_at_gate_pct"] - probe_reduction_pct)
    total = float(curve["reduction_at_certainty_pct"] - probe_reduction_pct)
    return {
        "sub_threshold_reduction_pct": float(probe_reduction_pct),
        "gate_entry_jump_pct": jump,
        "graded_span_above_gate_pct": float(curve["reachable_reduction_span_pct"]),
        "total_channel_span_including_gate_pct": total,
        "claim_bar_pct": CLAIM_TRACKING_BAR_PCT,
        "graded_span_clears_bar": bool(
            curve["reachable_reduction_span_pct"] >= CLAIM_TRACKING_BAR_PCT
        ),
        "total_span_clears_bar": bool(total >= CLAIM_TRACKING_BAR_PCT),
    }


def paired_channel_extremes(
    rows: list[dict[str, Any]], *, seeds: tuple[int, ...] = ASSESSMENT_SEEDS
) -> dict[str, Any]:
    """Return the channel's widest possible difference *in the contract's own units*.

    The response curve is stated as reduction against no-action, which is a convenient
    per-arm quantity but is **not** the Claim Sheet's. The contract's quantity is
    `100 (J_C1 - J_S) / J_C1`, with the conventional suite in the denominator, and a
    difference of two no-action reductions is smaller than it by a factor of
    `1 / (1 - r_low / 100)`. Reporting the reduction span against the bar would therefore
    understate the very quantity the bar is written in.

    Two extremes are reported, and they answer different questions:

    * **graded** — the worst pair that both clear the confidence gate, so this is what a
      pure probability-precision difference between two suites can buy.
    * **gate-crossing** — one suite withholding the action entirely against the other at
      full confidence. That is an authorization difference, not a precision one.

    Args:
        rows: All arm rows.
        seeds: Assessment seeds.

    Returns:
        Per-seed and aggregate paired quantities for both extremes.

    Raises:
        ValueError: If a required arm is missing.
    """

    indexed = _by_label(rows)
    gate_label = probability_label(RecoveryControlConfig().source_probability_threshold)
    certain_label = probability_label(1.0)
    per_seed: list[dict[str, Any]] = []
    for seed in seeds:
        try:
            gate_arm = indexed[(gate_label, seed)]
            certain = indexed[(certain_label, seed)]
            no_action = indexed[("no_action", seed)]
        except KeyError as error:  # pragma: no cover - guarded by build_arm_specs
            raise ValueError(f"missing arm for seed {seed}: {error}") from error
        per_seed.append(
            {
                "seed": int(seed),
                "graded_paired_pct": tracking_reduction_pct(
                    gate_arm["j_5s"], certain["j_5s"]
                ),
                "gate_crossing_paired_pct": tracking_reduction_pct(
                    no_action["j_5s"], certain["j_5s"]
                ),
            }
        )
    graded = np.asarray([row["graded_paired_pct"] for row in per_seed], dtype=float)
    crossing = np.asarray(
        [row["gate_crossing_paired_pct"] for row in per_seed], dtype=float
    )
    return {
        "per_seed": per_seed,
        "mean_graded_paired_pct": float(graded.mean()),
        "max_graded_paired_pct": float(np.max(np.abs(graded))),
        "mean_gate_crossing_paired_pct": float(crossing.mean()),
        "max_gate_crossing_paired_pct": float(np.max(np.abs(crossing))),
        "claim_bar_pct": CLAIM_TRACKING_BAR_PCT,
        "graded_clears_bar": bool(np.max(np.abs(graded)) >= CLAIM_TRACKING_BAR_PCT),
        "gate_crossing_clears_bar": bool(
            np.max(np.abs(crossing)) >= CLAIM_TRACKING_BAR_PCT
        ),
    }


def restoration_realization(
    rows: list[dict[str, Any]], *, seeds: tuple[int, ...] = ASSESSMENT_SEEDS
) -> dict[str, Any]:
    """Return the analytic exact-restoration ceiling against what the cap actually buys.

    The boundary screen measured this ratio at the `0.50` condition and explicitly did not
    establish it at the selected `0.25` condition. This is that measurement. It is a
    different regime: at `0.50` the certain diagnosis commands the exactly restoring
    multiplier, whereas here the cap allows only half of what exact restoration needs, so
    the shortfall carries both the pre-decision error and the cap saturation.

    Args:
        rows: All arm rows.
        seeds: Assessment seeds.

    Returns:
        Per-seed and mean deficit, analytic ceiling, realized reduction, and the ratio.

    Raises:
        ValueError: If a required arm is missing.
    """

    indexed = _by_label(rows)
    certain = probability_label(1.0)
    per_seed: list[dict[str, Any]] = []
    for seed in seeds:
        try:
            healthy = indexed[("healthy_reference", seed)]
            no_action = indexed[("no_action", seed)]
            best = indexed[(certain, seed)]
        except KeyError as error:  # pragma: no cover - guarded by build_arm_specs
            raise ValueError(f"missing arm for seed {seed}: {error}") from error
        deficit = 100.0 * (no_action["j_5s"] - healthy["j_5s"]) / healthy["j_5s"]
        ceiling = 100.0 * (no_action["j_5s"] - healthy["j_5s"]) / no_action["j_5s"]
        realized = tracking_reduction_pct(no_action["j_5s"], best["j_5s"])
        per_seed.append(
            {
                "seed": int(seed),
                "no_action_deficit_pct": float(deficit),
                "analytic_exact_restoration_ceiling_pct": float(ceiling),
                "realized_reduction_at_certainty_pct": float(realized),
                "realization_fraction": float(realized / ceiling) if ceiling else 0.0,
            }
        )
    mean_deficit = float(np.mean([r["no_action_deficit_pct"] for r in per_seed]))
    mean_ceiling = float(
        np.mean([r["analytic_exact_restoration_ceiling_pct"] for r in per_seed])
    )
    mean_realized = float(
        np.mean([r["realized_reduction_at_certainty_pct"] for r in per_seed])
    )
    return {
        "per_seed": per_seed,
        "mean_no_action_deficit_pct": mean_deficit,
        "mean_analytic_ceiling_pct": mean_ceiling,
        "mean_realized_reduction_pct": mean_realized,
        "mean_realization_fraction": float(mean_realized / mean_ceiling)
        if mean_ceiling
        else 0.0,
        "same_direction_on_every_seed": bool(
            all(r["realization_fraction"] < 1.0 for r in per_seed)
            or all(r["realization_fraction"] > 1.0 for r in per_seed)
        ),
    }


def severity_channel_is_flat(
    config: RecoveryControlConfig, *, severity: float, estimate_error: float
) -> dict[str, Any]:
    """Return whether any plausible severity estimate commands identically here.

    At the selected condition the cap binds for every estimate at or below
    `1 / maximum_gain_compensation`. A read-out whose error is far smaller than the margin
    to that boundary therefore cannot produce a multiplier difference at all, which is
    what leaves the probability channel as the only live one.

    Args:
        config: Recovery-controller settings.
        severity: True remaining gain.
        estimate_error: A representative severity error scale.

    Returns:
        The flat-region boundary, the margin from the true severity to it, and that margin
        expressed in units of the error scale.
    """

    boundary = 1.0 / config.maximum_gain_compensation
    margin = boundary - float(severity)
    return {
        "flat_region_upper_severity": float(boundary),
        "true_severity": float(severity),
        "margin_to_flat_region_boundary": float(margin),
        "estimate_error_scale": float(estimate_error),
        "margin_in_error_scales": float(margin / estimate_error)
        if estimate_error
        else float("inf"),
        "severity_channel_flat": bool(margin > 0.0),
    }


# --------------------------------------------------------------------------- #
# Integrity.
# --------------------------------------------------------------------------- #
def build_audit(
    rows: list[dict[str, Any]],
    recorded: dict[str, dict[int, float]],
    *,
    capped_compensation: float,
) -> dict[str, Any]:
    """Return every integrity condition the generated report depends on.

    Args:
        rows: All arm rows.
        recorded: Committed deficit-screen `J_5s` keyed by arm label then seed.
        capped_compensation: The controller's capped compensation at this severity.

    Returns:
        The audit record.

    Raises:
        ValueError: If no arm matched any recorded row, which would make the
            common-random-number check vacuously true.
    """

    indexed = _by_label(rows)
    differences: list[float] = []
    for label, by_seed in recorded.items():
        for seed, value in by_seed.items():
            arm = indexed.get((label, int(seed)))
            if arm is not None:
                differences.append(abs(arm["j_5s"] - float(value)))
    if not differences:
        raise ValueError(
            "no arm matched any recorded deficit-screen row; nothing was checked"
        )
    acting = [
        row
        for row in rows
        if row["probability"] is not None
        and row["probability"] >= RecoveryControlConfig().source_probability_threshold
    ]
    withheld = [
        row
        for row in rows
        if row["probability"] is None
        or row["probability"] < RecoveryControlConfig().source_probability_threshold
    ]
    multiplier_errors = [
        abs(row["applied_multiplier_max"] - expected_multiplier(row["probability"], capped_compensation))
        for row in acting
    ]
    return {
        "n_recorded_comparisons": len(differences),
        "max_abs_j5s_difference_vs_recorded": float(max(differences)),
        "no_action_matches_recorded": bool(max(differences) <= CRN_REUSE_TOLERANCE),
        "single_evaluation": bool(
            all(row["classification_evaluations"] == 1 for row in rows)
        ),
        "withheld_arms_changed_zero_commands": bool(
            all(row["recovery_command_changed_steps"] == 0 for row in withheld)
        ),
        "acting_arms_acted": bool(
            all(row["recovery_command_changed_steps"] > 0 for row in acting)
        ),
        "zero_a1_incidents": bool(all(row["a1_incident_steps"] == 0 for row in rows)),
        "zero_saturation": bool(all(row["saturation_steps"] == 0 for row in rows)),
        "applied_multipliers_match_probability": bool(
            bool(multiplier_errors)
            and max(multiplier_errors) <= MULTIPLIER_IDENTITY_TOLERANCE
        ),
        "max_abs_multiplier_identity_error": float(max(multiplier_errors))
        if multiplier_errors
        else 0.0,
    }


def require_passing_audit(audit: dict[str, Any]) -> None:
    """Fail loudly unless every integrity condition required by the report holds.

    Args:
        audit: The output of `build_audit`.

    Raises:
        RuntimeError: If any required CRN, lifecycle, action, safety, saturation, or
            multiplier-identity check is false.
    """

    required = (
        "no_action_matches_recorded",
        "single_evaluation",
        "withheld_arms_changed_zero_commands",
        "acting_arms_acted",
        "zero_a1_incidents",
        "zero_saturation",
        "applied_multipliers_match_probability",
    )
    failed = [name for name in required if not bool(audit.get(name, False))]
    if failed:
        raise RuntimeError(
            "actuator-probability-channel audit failed: " + ", ".join(failed)
        )


def load_recorded_j5s(path: Path, severity: float) -> dict[str, dict[int, float]]:
    """Read the deficit screen's committed assessment `J_5s`, keyed by label then seed.

    Args:
        path: The deficit screen's `summary.json`.
        severity: Remaining actuator gain whose rows to read.

    Returns:
        `{"no_action": {seed: j_5s}, "healthy_reference": {seed: j_5s}}`.

    Raises:
        ValueError: If either case is absent at that severity.
    """

    summary = json.loads(path.read_text(encoding="utf-8"))
    faulted: dict[int, float] = {}
    healthy: dict[int, float] = {}
    for row in summary["assessment_rows"]:
        if row["source_class"] == "actuator" and np.isclose(row["severity"], severity):
            faulted[int(row["sensor_seed"])] = float(row["tracking_integral_5s_m_s"])
        elif row["case_id"] == "healthy_reference":
            healthy[int(row["sensor_seed"])] = float(row["tracking_integral_5s_m_s"])
    if not faulted or not healthy:
        raise ValueError(
            f"deficit screen has no assessment rows at remaining gain {severity}"
        )
    return {"no_action": faulted, "healthy_reference": healthy}


# --------------------------------------------------------------------------- #
# Report.
# --------------------------------------------------------------------------- #
def _write_csv(path: Path, rows: list[dict[str, Any]]) -> None:
    """Write arm rows to CSV with a stable column order."""

    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(rows[0].keys()))
        writer.writeheader()
        writer.writerows(rows)


def write_report(path: Path, summary: dict[str, Any]) -> None:
    """Write the human-readable screen report.

    Args:
        path: Destination markdown file.
        summary: The full screen summary.
    """

    spec = summary["screen_spec"]
    reachable = summary["reachable_set"]
    flat = summary["severity_channel"]
    curve = summary["probability_response"]
    gate = summary["gate_discontinuity"]
    extremes = summary["paired_channel_extremes"]
    realization = summary["restoration_realization"]
    scales = summary["severity_uncertainty_scales"]

    lines: list[str] = []
    lines.append("# What the class-probability channel is worth at the selected actuator condition")
    lines.append("")
    lines.append(
        "Development-sized screen. Measures the last channel through which two suites that "
        "both call the actuator class correctly could still command different recovery "
        "actions, at the condition the deficit screen selected."
    )
    lines.append("")
    lines.append(
        f"- Selected condition: remaining actuator gain {spec['selected_severity']:g} at "
        f"joint {spec['fault_location']}, compensation cap "
        f"{spec['recovery_config']['maximum_gain_compensation']:g}"
    )
    lines.append(
        f"- Assessment seeds {list(spec['seeds'])}, reusing the deficit screen's `pair_id`s"
    )
    lines.append(
        f"- {summary['n_arms']} arms; swept probabilities {list(spec['probability_sweep'])} "
        f"plus the gate endpoint, the certain endpoint, and a sub-threshold probe"
    )
    lines.append(f"- Config hash `{spec['config_hash']}` (not frozen)")
    lines.append("")

    lines.append("## Part 0 — why probability is the only live channel here")
    lines.append("")
    lines.append(
        "The controller's compensation is "
        "`min(1 / max(severity, minimum_gain_remaining), maximum_gain_compensation)`. With "
        f"the recorded cap {spec['recovery_config']['maximum_gain_compensation']:g}, every "
        f"severity estimate at or below **{flat['flat_region_upper_severity']:.4f}** yields "
        "the same capped compensation. The true remaining gain here is "
        f"{flat['true_severity']:g}, which is "
        f"{flat['margin_in_error_scales']:.0f}x the recorded severity error scale away from "
        "that boundary."
    )
    lines.append("")
    lines.append(
        "**So the severity channel is structurally flat at this condition.** Every estimate "
        f"at or below {flat['flat_region_upper_severity']:.4f} commands an identical "
        "multiplier — that bound is the recorded cap, not a judgement about which estimates "
        "are plausible. A read-out would have to err by more than "
        f"{flat['margin_to_flat_region_boundary']:.4f} on a true {flat['true_severity']:g}, "
        f"about {flat['margin_in_error_scales']:.0f}x its recorded error scale, before the "
        "severity channel became live at all. That is what leaves the class probability as "
        "the only remaining way two suites agreeing on the class could act differently."
    )
    lines.append("")
    lines.append(
        "| suite | assessment residual RMS | std | bias | handed to the gate |"
    )
    lines.append("|---|---:|---:|---:|:--:|")
    handed = spec["gate_severity_uncertainty"]
    for suite in sorted(scales):
        record = scales[suite]
        used = np.isclose(record["assessment_residual_rms"], handed)
        lines.append(
            f"| {suite} | {record['assessment_residual_rms']:.6f} | "
            f"{record['assessment_residual_std']:.6f} | "
            f"{record['assessment_residual_bias']:+.6f} | {'yes' if used else 'no'} |"
        )
    lines.append("")
    lines.append(
        "- The gate receives a **bias-inclusive RMS**, not a residual standard deviation. "
        "A standard deviation discards the bias, so a systematically wrong but tightly "
        "clustered read-out would pass a gate it should fail. The conservative suite value "
        f"({handed:.6f}) is used at every acting arm, and it clears the "
        f"{spec['recovery_config']['maximum_severity_uncertainty']:g} gate by "
        f"{spec['recovery_config']['maximum_severity_uncertainty'] / handed:.0f}x, so no "
        "arm is sensitive to the choice."
    )
    lines.append("")

    lines.append("## Part 1 — the reachable probability set")
    lines.append("")
    lines.append(
        "Both ends of this interval are recorded controller constants, not chosen grid "
        f"points. The confidence gate closes it below at p = "
        f"{reachable['probability_threshold']:g}; the compensation cap closes it above. "
        f"The reachable commanded multiplier is therefore exactly "
        f"**[{reachable['reachable_multiplier_low']:.2f}, "
        f"{reachable['reachable_multiplier_high']:.2f}]**."
    )
    lines.append("")
    lines.append(
        f"- The action is **cap-saturated throughout**: exact restoration of a "
        f"{spec['selected_severity']:g} remaining gain needs a multiplier of "
        f"{reachable['exact_restoration_multiplier']:.2f}, and the cap allows "
        f"{reachable['capped_compensation']:.2f} — short by a factor of "
        f"{reachable['cap_shortfall_factor']:.2f}. Even a maximally confident diagnosis "
        "under-restores here."
    )
    lines.append("")

    lines.append("## Part 2 — the measured response")
    lines.append("")
    lines.append(
        "Each point is paired per seed against that seed's own no-action arm, so this is a "
        "within-noise-realization comparison. `reduction` is `100 x (J_no_action - J_arm) / "
        "J_no_action`, positive when the action helps."
    )
    lines.append("")
    lines.append(
        "| class probability | mean applied multiplier | mean reduction vs no-action | min | max |"
    )
    lines.append("|---:|---:|---:|---:|---:|")
    for point in curve["points"]:
        lines.append(
            f"| {point['probability']:.2f} | {point['mean_applied_multiplier']:.5f} | "
            f"{point['mean_reduction_vs_no_action_pct']:+.4f}% | "
            f"{point['min_reduction_vs_no_action_pct']:+.4f}% | "
            f"{point['max_reduction_vs_no_action_pct']:+.4f}% |"
        )
    lines.append("")
    lines.append(
        f"- **Across the entire reachable set p in "
        f"[{curve['probability_span'][0]:.2f}, {curve['probability_span'][1]:.2f}] the "
        f"reduction moves by {curve['reachable_reduction_span_pct']:.4f} percentage "
        f"points**, against a {curve['claim_bar_pct']:.0f}% bar — "
        f"{'above' if curve['reachable_span_clears_bar'] else 'below'} it. The slope at the "
        f"certain end is {curve['local_slope_pct_per_unit_probability']:+.4f} points per "
        "unit of probability."
    )
    lines.append("")

    lines.append("## Part 3 — the gate is a separate quantity from the graded channel")
    lines.append("")
    lines.append(
        f"A sub-threshold probe at p = {spec['gate_probe_probability']:g} keeps the actuator "
        "as the unique argmax and still produces "
        f"{gate['sub_threshold_reduction_pct']:.4f}% reduction — the action is withheld "
        "entirely. Entering the gate jumps straight to "
        f"{gate['gate_entry_jump_pct']:.4f} percentage points."
    )
    lines.append("")
    lines.append(
        "The table below is in **the contract's own units** — "
        "`100 x (J_C1 - J_S) / J_C1`, the conventional suite in the denominator — not in "
        "differences of no-action reductions. Those are not the same number: a difference "
        "of two reductions is smaller by `1 / (1 - r_low / 100)`, so quoting the reduction "
        "span against the bar would understate the quantity the bar is written in. Here "
        f"the reduction span is {curve['reachable_reduction_span_pct']:.4f} pp while the "
        f"paired quantity it corresponds to is "
        f"{extremes['max_graded_paired_pct']:.4f} pp."
    )
    lines.append("")
    lines.append("| paired quantity | worst seed | mean | vs bar |")
    lines.append("|---|---:|---:|---|")
    lines.append(
        f"| graded — both suites past the gate | "
        f"{extremes['max_graded_paired_pct']:.4f} pp | "
        f"{extremes['mean_graded_paired_pct']:.4f} pp | "
        f"{'clears' if extremes['graded_clears_bar'] else 'below'} |"
    )
    lines.append(
        f"| gate-crossing — one suite withholds entirely | "
        f"{extremes['max_gate_crossing_paired_pct']:.4f} pp | "
        f"{extremes['mean_gate_crossing_paired_pct']:.4f} pp | "
        f"{'clears' if extremes['gate_crossing_clears_bar'] else 'below'} |"
    )
    lines.append("")
    lines.append(
        "**These must not be collapsed into one number.** The graded span is what a "
        "*probability-precision* difference between two suites can buy. The gate-entry jump "
        "is what a difference in whether the suite authorizes the action at all can buy, "
        "and that is a class-call-scale quantity, already screened elsewhere: both suites "
        "call this class correctly with one-hot recorded probabilities, so neither the "
        "recorded difference nor the gate crossing is currently in play."
    )
    lines.append("")

    lines.append("## Part 4 — what the cap actually buys at this condition")
    lines.append("")
    lines.append(
        "The boundary screen measured the realized-versus-analytic ratio at the 0.50 "
        "condition and explicitly did not establish it here. This is that measurement, and "
        "it is a different regime: there the certain diagnosis commanded the exactly "
        "restoring multiplier, whereas here the cap allows only half of what exact "
        "restoration needs."
    )
    lines.append("")
    lines.append(
        f"- Mean no-action deficit **{realization['mean_no_action_deficit_pct']:.2f}%**; "
        f"analytic exact-restoration ceiling "
        f"**{realization['mean_analytic_ceiling_pct']:.2f}%**; realized at the cap "
        f"**{realization['mean_realized_reduction_pct']:.2f}%** — "
        f"**{100.0 * realization['mean_realization_fraction']:.1f}% of the ceiling**"
        f"{', in the same direction on every seed' if realization['same_direction_on_every_seed'] else ''}."
    )
    lines.append("")

    lines.append("## What this screen does and does not establish")
    lines.append("")
    if not extremes["graded_clears_bar"]:
        lines.append(
            f"- **It closes the class-probability channel on the actuator class at this "
            f"condition.** The widest paired difference two gate-clearing suites can produce "
            f"through this channel is {extremes['max_graded_paired_pct']:.4f} pp against a "
            f"{CLAIM_TRACKING_BAR_PCT:.0f} pp bar, and that is over the channel's *entire "
            "reachable set*, closed at both ends by the controller's own recorded constants "
            "rather than by a chosen grid. No probability read-out — linear, learned, or "
            "calibrated — can reach the bar through this channel here without also crossing "
            "the confidence gate."
        )
    else:
        lines.append(
            f"- **The graded probability channel reaches the bar at this condition** "
            f"({extremes['max_graded_paired_pct']:.4f} pp). That is a live route and must be "
            "carried into the action screen's design."
        )
    lines.append(
        "- **It does not license collapsing the gate into the channel.** A suite difference "
        "large enough to put one suite below the confidence threshold and the other above "
        "it is a class-call/authorization difference, and it is measured separately above."
    )
    lines.append(
        "- **It does not close the actuator class.** Action-versus-no-action benefit on a "
        "healthy body, false authorization, cap and floor sensitivity, and the "
        "source-specific margin remain the action screen's questions."
    )
    lines.append(
        "- **It does not extend to a different cap.** Both the flat severity region and the "
        "reachable multiplier set are functions of `maximum_gain_compensation`. At a larger "
        "cap the severity channel reopens at this condition and this screen says nothing "
        "about it."
    )
    lines.append(
        "- **Development-sized.** Four assessment seeds on one bounded task/contact "
        "condition, one fault location, one fault setting, held out over sensor noise only, "
        "at an unfrozen config."
    )
    lines.append("")

    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text("\n".join(lines) + "\n", encoding="utf-8")


def main() -> int:
    """Run the screen end to end and write its three artifacts."""

    parser = argparse.ArgumentParser(
        description=(
            "Measure the class-probability channel's reachable tracking span at the "
            "deficit screen's selected actuator condition."
        )
    )
    parser.add_argument(
        "--deficit-summary",
        type=Path,
        default=Path("results/fault_tracking_deficit_screen/summary.json"),
        help="Committed deficit-screen summary supplying the CRN cross-check rows.",
    )
    parser.add_argument(
        "--severity-summary",
        type=Path,
        default=Path("results/severity_estimation_quality/summary.json"),
        help="Committed severity-screen summary supplying the recorded error scales.",
    )
    parser.add_argument(
        "--output-dir",
        type=Path,
        default=Path("results/actuator_probability_channel"),
        help="Directory for the screen's artifacts.",
    )
    parser.add_argument(
        "--workers", type=int, default=4, help="Parallel rollout workers."
    )
    args = parser.parse_args()
    if args.workers < 1:
        raise SystemExit("--workers must be at least 1")

    base = RecoveryControlConfig()
    base.validate()

    print("Part 0 — recorded severity error scales", flush=True)
    scales = recorded_assessment_rms(args.severity_summary)
    gate_uncertainty = gate_uncertainty_from_scales(
        scales, limit=base.maximum_severity_uncertainty
    )
    for suite, record in sorted(scales.items()):
        print(
            f"  {suite}: RMS {record['assessment_residual_rms']:.6f} "
            f"(std {record['assessment_residual_std']:.6f}, "
            f"bias {record['assessment_residual_bias']:+.6f})",
            flush=True,
        )
    print(f"  handing the gate {gate_uncertainty:.6f}", flush=True)

    reachable = reachable_multiplier_set(base, SELECTED_SEVERITY)
    flat = severity_channel_is_flat(
        base, severity=SELECTED_SEVERITY, estimate_error=gate_uncertainty
    )
    print(
        f"Part 1 — reachable multiplier "
        f"[{reachable['reachable_multiplier_low']:.2f}, "
        f"{reachable['reachable_multiplier_high']:.2f}]; severity channel flat at or "
        f"below {flat['flat_region_upper_severity']:.4f} "
        f"({flat['margin_in_error_scales']:.0f}x the error scale away)",
        flush=True,
    )

    specs = build_arm_specs(gate_uncertainty=gate_uncertainty, config=base)
    print(f"Part 2 — {len(specs)} arms on {args.workers} workers", flush=True)
    rows: list[dict[str, Any]] = []
    with concurrent.futures.ProcessPoolExecutor(max_workers=args.workers) as pool:
        for index, row in enumerate(pool.map(run_probability_arm, specs), start=1):
            rows.append(row)
            print(
                f"  [{index}/{len(specs)}] {row['label']} seed {row['seed']} "
                f"J_5s {row['j_5s']:.6f} m {row['applied_multiplier_max']:.5f}",
                flush=True,
            )
    rows.sort(key=lambda row: (row["seed"], row["label"]))

    recorded = load_recorded_j5s(args.deficit_summary, SELECTED_SEVERITY)
    audit = build_audit(
        rows, recorded, capped_compensation=reachable["capped_compensation"]
    )
    require_passing_audit(audit)

    print("Part 3 — analysis", flush=True)
    curve = probability_response_curve(rows, config=base)
    probe = float(
        np.mean(
            [
                tracking_reduction_pct(
                    _by_label(rows)[("no_action", seed)]["j_5s"],
                    _by_label(rows)[("gate_probe", seed)]["j_5s"],
                )
                for seed in ASSESSMENT_SEEDS
            ]
        )
    )
    gate = gate_discontinuity(curve, probe_reduction_pct=probe)
    extremes = paired_channel_extremes(rows)
    realization = restoration_realization(rows)

    summary = {
        "screen_spec": {
            "purpose": (
                "reachable-set span of the class-probability channel at the deficit "
                "screen's selected actuator condition"
            ),
            "selected_severity": SELECTED_SEVERITY,
            "fault_location": FAULT_LOCATION,
            "seeds": list(ASSESSMENT_SEEDS),
            "probability_sweep": list(PROBABILITY_SWEEP),
            "gate_probe_probability": GATE_PROBE_PROBABILITY,
            "gate_severity_uncertainty": gate_uncertainty,
            "plane_z_m": PLANE_Z_M,
            "config_hash": CONFIG_HASH,
            "recovery_config": {
                "source_probability_threshold": base.source_probability_threshold,
                "maximum_severity_uncertainty": base.maximum_severity_uncertainty,
                "maximum_gain_compensation": base.maximum_gain_compensation,
                "minimum_gain_remaining": base.minimum_gain_remaining,
                "torque_abs_limit": list(base.torque_abs_limit),
            },
            "recorded_deficit_screen": str(args.deficit_summary).replace("\\", "/"),
            "recorded_severity_screen": str(args.severity_summary).replace("\\", "/"),
        },
        "n_arms": len(rows),
        "severity_uncertainty_scales": scales,
        "reachable_set": reachable,
        "severity_channel": flat,
        "probability_response": curve,
        "gate_discontinuity": gate,
        "paired_channel_extremes": extremes,
        "restoration_realization": realization,
        "audit": audit,
        "artifact_status": "development_only_config_unfrozen",
    }

    args.output_dir.mkdir(parents=True, exist_ok=True)
    (args.output_dir / "summary.json").write_text(
        json.dumps(summary, indent=2, sort_keys=True) + "\n", encoding="utf-8"
    )
    _write_csv(args.output_dir / "arm_rows.csv", rows)
    write_report(
        args.output_dir / "actuator_probability_channel_report.md", summary
    )

    print(
        f"Widest graded paired difference {extremes['max_graded_paired_pct']:.4f} pp "
        f"against a {CLAIM_TRACKING_BAR_PCT:.0f} pp bar "
        f"(reduction span {curve['reachable_reduction_span_pct']:.4f} pp); "
        f"gate-crossing {extremes['max_gate_crossing_paired_pct']:.4f} pp",
        flush=True,
    )
    print(f"Wrote {args.output_dir}", flush=True)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
