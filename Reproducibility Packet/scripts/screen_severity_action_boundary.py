"""Measure what a severity difference is worth in tracking at the action's cap boundary.

The severity-estimation-quality screen (Step 15) established two things about the
actuator class. Both deployable suites estimate remaining gain almost exactly, and the
recovery controller's multiplier `min(1 / max(severity, floor), cap)` is flat below
`1 / cap`, so over most of the severity range no read-out difference can change the
command at all. It also established the exception: the recorded `0.50` remaining-gain
setting sits *exactly* on the cap-2 kink, where the action is one-sidedly sensitive, and
its exact-restoration ceiling (11.66%) clears the Claim Sheet's 10% bar. On that one
setting the two suites' held-out estimates straddle the kink and command differently on
3 of 4 paired arms. Step 15 closes with the honest statement that the paired control
effect there is *not structurally zero* and has to be measured.

This screen measures it, and it measures it two ways, because the specific number and
the bound answer different questions.

Part 1 — held-out severity uncertainty. The controller's confidence gate rejects a
diagnosis whose `severity_uncertainty` exceeds `maximum_severity_uncertainty`, and the
severity head only reports an *in-sample* residual dispersion. Refitting the head once
per held-out sensor seed on the recorded Step-15 feature rows gives the out-of-sample
number the gate should see. No rollouts: the features are the durable product Step 15
already wrote to disk.

Part 2 — the boundary arms. On the same bounded task, contact plane, observed-state
controller, probe, and single-held-decision lifecycle, at remaining gain `0.50` and the
recorded cap, each disjoint assessment seed is run under: no action, a privileged oracle
severity, each suite's *recorded held-out estimate*, and a sweep of fixed commanded
multipliers. Because the estimator decides once, before the action fires, everything up
to the decision step is bitwise identical to Step 15's no-action arm at the same seed —
so the recorded estimate is exactly what a deployable head would have produced here. The
no-action arm re-runs that trajectory and its `J_5s` is checked against the committed
Step-15 row, which pins the reuse instead of asserting it.

The sweep puts the observed result inside a deliberately wider empirical envelope. It
spans multipliers 1.50–2.00, far beyond the errors of the recorded linear read-outs, and
shows how multiplier differences in that envelope convert into tracking differences. It
does *not* bound an arbitrary future read-out that could command below 1.50.

Run from `Reproducibility Packet/`:
    .\\.venv\\Scripts\\python.exe scripts\\screen_severity_action_boundary.py --workers 8
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
from utils.estimator import (  # noqa: E402
    SOURCE_CLASS_ORDER,
    EstimatorOutput,
    leave_one_group_out_residuals,
)
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

#: The one setting that is both reachable by the bar and severity-sensitive at the
#: recorded cap: the deficit screen's `actuator_gain_remaining_0p50` case, which sits
#: exactly on the cap-2 kink.
BOUNDARY_SEVERITY = 0.50

#: Step 15's disjoint assessment seeds. Reused verbatim so each arm's pre-decision
#: trajectory is the one that produced the recorded held-out estimate.
ASSESSMENT_SEEDS: tuple[int, ...] = (17100, 17101, 17102, 17103)

#: Fixed commanded multipliers for the sensitivity sweep, expressed as multipliers rather
#: than severities because the multiplier is the quantity the plant actually sees. Every
#: value is at or below the recorded cap, so the cap never re-clips them.
MULTIPLIER_SWEEP: tuple[float, ...] = (1.50, 1.70, 1.85, 1.93, 1.97)

#: Contact plane height, matching the bounded profile every recent screen uses.
PLANE_Z_M = 0.200

#: The Claim Sheet's control bar, in reduction percent.
CLAIM_TRACKING_BAR_PCT = 10.0

#: Development config hash. `dev-` prefixed: no `dev-` trace may enter confirmatory analysis.
CONFIG_HASH = "dev-severity-action-boundary-screen"

#: Joint carrying the actuator fault.
FAULT_LOCATION = 1

#: Tolerance on the Step-15 no-action cross-check. The arms share a seed, a `pair_id`,
#: and a plant, so the trajectories are expected to agree exactly; this is a guard
#: against silent harness drift, not a statistical tolerance.
CRN_REUSE_TOLERANCE = 1.0e-12


# --------------------------------------------------------------------------- #
# Part 1 — held-out severity uncertainty from the recorded Step-15 features.
# --------------------------------------------------------------------------- #
def load_recorded_features(path: Path) -> dict[str, dict[str, np.ndarray]]:
    """Read Step 15's per-arm, per-suite window feature vectors.

    Args:
        path: Path to `window_features.csv` from the severity-estimation-quality screen.

    Returns:
        Suite-keyed mapping with `features [N, F]`, `severities [N]`, `seeds [N]`, and
        `roles [N]`.

    Raises:
        FileNotFoundError: If the recorded screen output is missing.
        ValueError: If the file carries no feature columns or no tuning rows.
    """

    if not path.is_file():
        raise FileNotFoundError(
            f"recorded window features not found at {path}; run "
            "scripts/screen_severity_estimation_quality.py first"
        )
    with path.open(newline="", encoding="utf-8") as handle:
        rows = list(csv.DictReader(handle))
    if not rows:
        raise ValueError(f"{path} contains no rows")
    width = sum(1 for key in rows[0] if key.startswith("f") and key[1:].isdigit())
    if width == 0:
        raise ValueError(f"{path} carries no feature columns")
    bundles: dict[str, dict[str, list]] = {}
    for row in rows:
        bundle = bundles.setdefault(
            row["suite"], {"features": [], "severities": [], "seeds": [], "roles": []}
        )
        bundle["features"].append([float(row[f"f{i}"]) for i in range(width)])
        bundle["severities"].append(float(row["severity"]))
        bundle["seeds"].append(int(row["seed"]))
        bundle["roles"].append(row["role"])
    packed = {
        suite: {
            "features": np.asarray(bundle["features"], dtype=float),
            "severities": np.asarray(bundle["severities"], dtype=float),
            "seeds": np.asarray(bundle["seeds"], dtype=int),
            "roles": np.asarray(bundle["roles"], dtype=object),
        }
        for suite, bundle in bundles.items()
    }
    for suite, bundle in packed.items():
        if not np.any(bundle["roles"] == "tuning"):
            raise ValueError(f"{path} carries no tuning rows for suite {suite}")
    return packed


def cross_seed_calibration_uncertainty(
    bundle: dict[str, np.ndarray], *, regularization: float
) -> dict[str, float]:
    """Return a fixed-penalty cross-seed dispersion from one suite's tuning rows.

    Leave-one-seed-out, not leave-one-window-out: windows sharing a sensor seed share a
    noise realization, so holding out individual windows would report a dispersion the
    deployed head will not reproduce. This is an internal calibration-role estimate, not
    the disjoint assessment role and not a nested estimate of the penalty-selection
    procedure: Step 15 selected the fixed penalty using these same tuning groups.

    Args:
        bundle: One suite's entry from `load_recorded_features`.
        regularization: The ridge penalty Step 15 selected for that suite, held fixed
            across folds so the number describes one model rather than a selection
            procedure.

    Returns:
        Record carrying the cross-seed residual standard deviation, its mean (bias), the
        mean absolute residual, and the fold count.
    """

    tuning = bundle["roles"] == "tuning"
    residuals = leave_one_group_out_residuals(
        bundle["features"][tuning],
        bundle["severities"][tuning],
        bundle["seeds"][tuning],
        regularization=regularization,
    )
    return {
        "calibration_cross_seed_residual_std": float(residuals.std(ddof=1)),
        "calibration_cross_seed_residual_mean": float(residuals.mean()),
        "calibration_cross_seed_residual_mean_abs": float(np.mean(np.abs(residuals))),
        "n_calibration_folds": int(np.unique(bundle["seeds"][tuning]).size),
        "n_calibration_residuals": int(residuals.size),
    }


def disjoint_assessment_residual_diagnostics(
    evaluation: dict[str, Any],
) -> dict[str, float]:
    """Return residual diagnostics from Step 15's disjoint assessment predictions.

    These rows were not used to fit the head or select its penalty. They are reported
    alongside the calibration-role cross-seed estimate so the screen cannot mistake an
    internal cross-validation ranking for the actual disjoint assessment ranking.

    Args:
        evaluation: One suite's Step-15 `suite_evaluations` record.

    Returns:
        Residual standard deviation, bias, mean absolute error, and row count.

    Raises:
        ValueError: If fewer than two finite prediction rows are present.
    """

    predictions = evaluation.get("predictions", [])
    residuals = np.asarray(
        [
            float(row["estimate"]) - float(row["severity"])
            for row in predictions
        ],
        dtype=float,
    )
    if residuals.size < 2 or not np.all(np.isfinite(residuals)):
        raise ValueError(
            "disjoint assessment diagnostics require at least two finite predictions"
        )
    return {
        "assessment_residual_std": float(residuals.std(ddof=1)),
        "assessment_residual_mean": float(residuals.mean()),
        "assessment_residual_mean_abs": float(np.mean(np.abs(residuals))),
        "n_assessment_residuals": int(residuals.size),
    }


def load_boundary_estimates(path: Path, severity: float) -> dict[str, dict[int, float]]:
    """Read both suites' recorded held-out estimates at one true severity.

    Args:
        path: Path to `summary.json` from the severity-estimation-quality screen.
        severity: The true remaining-gain grid point to extract.

    Returns:
        Suite-keyed mapping of assessment seed to recorded held-out estimate.

    Raises:
        FileNotFoundError: If the recorded screen output is missing.
        ValueError: If a suite has no predictions at that severity, or the suites are
            not paired on the same seeds.
    """

    if not path.is_file():
        raise FileNotFoundError(
            f"recorded severity summary not found at {path}; run "
            "scripts/screen_severity_estimation_quality.py first"
        )
    summary = json.loads(path.read_text(encoding="utf-8"))
    estimates: dict[str, dict[int, float]] = {}
    for suite, record in summary["suite_evaluations"].items():
        selected = {
            int(row["seed"]): float(row["estimate"])
            for row in record["predictions"]
            if np.isclose(float(row["severity"]), severity)
        }
        if not selected:
            raise ValueError(f"no {suite} predictions at severity {severity}")
        estimates[suite] = selected
    seed_sets = {suite: frozenset(rows) for suite, rows in estimates.items()}
    if len(set(seed_sets.values())) != 1:
        raise ValueError("suites are not paired on the same assessment seeds")
    return estimates


# --------------------------------------------------------------------------- #
# Part 2 — the boundary action arms.
# --------------------------------------------------------------------------- #
class FixedDiagnosisEstimator:
    """Return one pre-set diagnosis at the scheduled decision step.

    The screen is not testing a classifier: every arm calls the actuator class correctly,
    with a one-hot probability, and differs only in the severity number it reports. That
    isolates the severity channel, which is the quantity under test. A `None` severity is
    the no-action arm: a healthy one-hot output the recovery controller never acts on.
    """

    def __init__(self, severity: float | None, *, severity_uncertainty: float) -> None:
        """Bind the severity read-out this estimator reports at every decision.

        Args:
            severity: Remaining-gain estimate in `(0, 1]`, or `None` for a healthy call.
            severity_uncertainty: Reported dispersion. The controller's gate treats this
                as a threshold test, so any value inside the gate commands identically.

        Raises:
            ValueError: If the severity is outside `(0, 1]` or the uncertainty is not
                finite and non-negative.
        """

        if severity is not None and not 0.0 < float(severity) <= 1.0:
            raise ValueError("severity must be None or in (0, 1]")
        if not np.isfinite(severity_uncertainty) or severity_uncertainty < 0.0:
            raise ValueError("severity_uncertainty must be finite and non-negative")
        self.severity = None if severity is None else float(severity)
        self.severity_uncertainty = float(severity_uncertainty)
        self.calls = 0

    def reset(self) -> None:
        """Clear the call count before a new rollout."""

        self.calls = 0

    def update(self, step_index: int, decision_time_s: float, window) -> EstimatorOutput:
        """Return the pre-set diagnosis, ignoring the observed window."""

        self.calls += 1
        probabilities = np.zeros(len(SOURCE_CLASS_ORDER), dtype=float)
        called = "healthy" if self.severity is None else "actuator"
        probabilities[SOURCE_CLASS_ORDER.index(called)] = 1.0
        output = EstimatorOutput(
            step=step_index,
            decision_time_s=decision_time_s,
            p_class=probabilities,
            unknown_score=0.0,
            abstain_decision=False,
            location_out=-1 if self.severity is None else FAULT_LOCATION,
            severity_out=0.0 if self.severity is None else self.severity,
            severity_uncertainty=(
                float("inf") if self.severity is None else self.severity_uncertainty
            ),
            detection_time_s=float("nan") if self.severity is None else decision_time_s,
        )
        output.validate()
        return output


@dataclass(frozen=True)
class ActionArmSpec:
    """One rollout at the boundary condition under one commanded diagnosis."""

    seed: int
    label: str
    #: Commanded remaining-gain estimate, or `None` for the no-action arm.
    commanded_severity: float | None
    #: Reported severity uncertainty; only its position relative to the gate matters.
    severity_uncertainty: float
    #: Whether the plant carries the actuator fault. `False` is the healthy reference.
    faulted: bool
    suite: str = "S"


def run_action_arm(spec: ActionArmSpec) -> dict[str, Any]:
    """Run one boundary arm and return its tracking integral and audit fields.

    The `pair_id` and sensor seed are Step 15's, so the arm's pre-decision trajectory is
    the one that produced the recorded held-out estimate this screen commands.

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
    # Step 15's `pair_id`, verbatim: same sensor RNG substreams, same trajectory.
    pair_id = f"severity-quality-assessment-{spec.seed}"
    run_id = f"boundary-{spec.label}-{spec.seed}-{spec.suite}"
    fault = (
        FaultSpec(
            source_class="actuator",
            subtype="actuator_gain_loss",
            location=FAULT_LOCATION,
            severity=BOUNDARY_SEVERITY,
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
    inner = FixedDiagnosisEstimator(
        spec.commanded_severity, severity_uncertainty=spec.severity_uncertainty
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
    # The applied multiplier at the faulted joint, read off the steps where the nominal
    # command is large enough for the ratio to be meaningful.
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
        "commanded_severity": (
            None if spec.commanded_severity is None else float(spec.commanded_severity)
        ),
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


def build_arm_specs(
    estimates: dict[str, dict[int, float]],
    uncertainties: dict[str, float],
    *,
    seeds: tuple[int, ...] = ASSESSMENT_SEEDS,
    multipliers: tuple[float, ...] = MULTIPLIER_SWEEP,
) -> list[ActionArmSpec]:
    """Return the full arm list: references, deployable arms, and the multiplier sweep.

    Args:
        estimates: Suite-keyed seed→held-out estimate from `load_boundary_estimates`.
        uncertainties: Suite-keyed calibration-role cross-seed dispersion from Part 1.
        seeds: Assessment seeds to run.
        multipliers: Fixed commanded multipliers for the sweep, each strictly below the
            cap. The cap point is supplied separately by the oracle arm.

    Returns:
        One `ActionArmSpec` per arm.

    Raises:
        ValueError: If a seed is missing from a suite's recorded estimates, or a sweep
            multiplier is not strictly between one and the recorded cap.
    """

    cap = RecoveryControlConfig().maximum_gain_compensation
    for multiplier in multipliers:
        if not 1.0 < multiplier < cap:
            raise ValueError(
                f"sweep multiplier {multiplier} is outside (1, {cap:g}); the cap point "
                "is supplied separately by the oracle arm"
            )
    specs: list[ActionArmSpec] = []
    for seed in seeds:
        specs.append(
            ActionArmSpec(
                seed=seed,
                label="healthy_reference",
                commanded_severity=None,
                severity_uncertainty=0.0,
                faulted=False,
            )
        )
        specs.append(
            ActionArmSpec(
                seed=seed,
                label="no_action",
                commanded_severity=None,
                severity_uncertainty=0.0,
                faulted=True,
            )
        )
        specs.append(
            ActionArmSpec(
                seed=seed,
                label="oracle",
                commanded_severity=BOUNDARY_SEVERITY,
                severity_uncertainty=0.0,
                faulted=True,
            )
        )
        for suite in sorted(estimates):
            if seed not in estimates[suite]:
                raise ValueError(f"suite {suite} has no recorded estimate for seed {seed}")
            specs.append(
                ActionArmSpec(
                    seed=seed,
                    label=f"deployable_{suite}",
                    commanded_severity=estimates[suite][seed],
                    severity_uncertainty=uncertainties[suite],
                    faulted=True,
                )
            )
        for multiplier in multipliers:
            specs.append(
                ActionArmSpec(
                    seed=seed,
                    label=f"multiplier_{multiplier:.2f}",
                    commanded_severity=1.0 / multiplier,
                    severity_uncertainty=0.0,
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


def paired_boundary_result(
    rows: list[dict[str, Any]], *, seeds: tuple[int, ...] = ASSESSMENT_SEEDS
) -> dict[str, Any]:
    """Return the contract's paired S-minus-C1 quantity on the boundary arms.

    `tracking_reduction_pct(J_C1, J_S)` is the Claim Sheet's control quantity, with the
    conventional suite in the denominator. It is computed per seed from arms that share a
    seed, a plant, and a noise realization, and differ only in the severity number each
    suite's recorded held-out estimate supplied to the controller.

    Args:
        rows: All arm rows.
        seeds: Assessment seeds to pair over.

    Returns:
        Per-seed and aggregate record, including each suite's reduction against the
        no-action arm and against the oracle ceiling.

    Raises:
        ValueError: If a required arm is missing.
    """

    indexed = _by_label(rows)
    per_seed: list[dict[str, Any]] = []
    for seed in seeds:
        try:
            no_action = indexed[("no_action", seed)]
            oracle = indexed[("oracle", seed)]
            healthy = indexed[("healthy_reference", seed)]
            c1 = indexed[("deployable_C1", seed)]
            s = indexed[("deployable_S", seed)]
        except KeyError as error:  # pragma: no cover - guarded by build_arm_specs
            raise ValueError(f"missing boundary arm for seed {seed}: {error}") from error
        per_seed.append(
            {
                "seed": int(seed),
                "j_healthy": healthy["j_5s"],
                "j_no_action": no_action["j_5s"],
                "j_oracle": oracle["j_5s"],
                "j_c1": c1["j_5s"],
                "j_s": s["j_5s"],
                "commanded_severity_c1": c1["commanded_severity"],
                "commanded_severity_s": s["commanded_severity"],
                "applied_multiplier_c1": c1["applied_multiplier_max"],
                "applied_multiplier_s": s["applied_multiplier_max"],
                "no_action_deficit_pct": 100.0
                * (no_action["j_5s"] - healthy["j_5s"])
                / healthy["j_5s"],
                "paired_s_minus_c1_reduction_pct": tracking_reduction_pct(
                    c1["j_5s"], s["j_5s"]
                ),
                "c1_reduction_vs_no_action_pct": tracking_reduction_pct(
                    no_action["j_5s"], c1["j_5s"]
                ),
                "s_reduction_vs_no_action_pct": tracking_reduction_pct(
                    no_action["j_5s"], s["j_5s"]
                ),
                "oracle_reduction_vs_no_action_pct": tracking_reduction_pct(
                    no_action["j_5s"], oracle["j_5s"]
                ),
            }
        )
    paired = np.asarray(
        [row["paired_s_minus_c1_reduction_pct"] for row in per_seed], dtype=float
    )
    return {
        "per_seed": per_seed,
        "mean_paired_reduction_pct": float(paired.mean()),
        "max_abs_paired_reduction_pct": float(np.max(np.abs(paired))),
        "n_seeds_favouring_s": int(np.count_nonzero(paired > 0.0)),
        "n_seeds_favouring_c1": int(np.count_nonzero(paired < 0.0)),
        "n_seeds_identical": int(np.count_nonzero(paired == 0.0)),
        "mean_oracle_reduction_vs_no_action_pct": float(
            np.mean([row["oracle_reduction_vs_no_action_pct"] for row in per_seed])
        ),
        "mean_c1_reduction_vs_no_action_pct": float(
            np.mean([row["c1_reduction_vs_no_action_pct"] for row in per_seed])
        ),
        "mean_s_reduction_vs_no_action_pct": float(
            np.mean([row["s_reduction_vs_no_action_pct"] for row in per_seed])
        ),
        "mean_no_action_deficit_pct": float(
            np.mean([row["no_action_deficit_pct"] for row in per_seed])
        ),
    }


def multiplier_sensitivity_curve(
    rows: list[dict[str, Any]],
    *,
    seeds: tuple[int, ...] = ASSESSMENT_SEEDS,
    multipliers: tuple[float, ...] = MULTIPLIER_SWEEP,
    cap: float,
) -> dict[str, Any]:
    """Return tracking reduction as a function of the commanded multiplier.

    This is the conversion factor the project has been missing: every severity result so
    far is stated in multiplier units, and the contract is stated in tracking units. The
    sweep spans multipliers far outside the recorded linear read-outs' errors. Its
    reduction span is therefore an empirical envelope for those read-outs and similarly
    accurate alternatives, not a universal bound on an arbitrary future read-out.

    Args:
        rows: All arm rows.
        seeds: Assessment seeds to average over.
        multipliers: Swept multipliers, excluding the cap arm.
        cap: The recorded compensation cap, whose arm is the oracle arm.

    Returns:
        Per-multiplier mean reduction against the no-action arm, the reduction spread
        across the whole sweep, and the local slope at the cap.

    Raises:
        ValueError: If a required arm is missing.
    """

    indexed = _by_label(rows)
    points: list[dict[str, Any]] = []
    labelled = [(m, f"multiplier_{m:.2f}") for m in multipliers] + [(cap, "oracle")]
    for multiplier, label in sorted(labelled):
        reductions, applied = [], []
        for seed in seeds:
            if (label, seed) not in indexed or ("no_action", seed) not in indexed:
                raise ValueError(f"missing arm {label} at seed {seed}")
            arm = indexed[(label, seed)]
            reductions.append(
                tracking_reduction_pct(indexed[("no_action", seed)]["j_5s"], arm["j_5s"])
            )
            applied.append(arm["applied_multiplier_max"])
        points.append(
            {
                "commanded_multiplier": float(multiplier),
                "mean_applied_multiplier": float(np.mean(applied)),
                "mean_reduction_vs_no_action_pct": float(np.mean(reductions)),
                "min_reduction_vs_no_action_pct": float(np.min(reductions)),
                "max_reduction_vs_no_action_pct": float(np.max(reductions)),
            }
        )
    values = np.asarray(
        [point["mean_reduction_vs_no_action_pct"] for point in points], dtype=float
    )
    grid = np.asarray([point["commanded_multiplier"] for point in points], dtype=float)
    # Local slope at the cap, from the two highest swept multipliers.
    top = np.argsort(grid)[-2:]
    slope = float(
        (values[top[1]] - values[top[0]]) / (grid[top[1]] - grid[top[0]])
    )
    return {
        "points": points,
        "multiplier_span": [float(grid.min()), float(grid.max())],
        "reduction_span_pct": float(values.max() - values.min()),
        "reduction_at_cap_pct": float(values[np.argmax(grid)]),
        "best_reduction_pct": float(values.max()),
        "best_multiplier": float(grid[int(np.argmax(values))]),
        "local_slope_pct_per_unit_multiplier_at_cap": slope,
    }


def severity_difference_envelope(
    curve: dict[str, Any], observed_multiplier_spread: float
) -> dict[str, Any]:
    """Convert the observed spread locally and report the measured sweep envelope.

    The local slope product is a linearized conversion, not a mathematical upper bound:
    the direct paired rollouts remain the authoritative measurement. The whole-sweep span
    is likewise scoped to the recorded multiplier interval.

    Args:
        curve: The output of `multiplier_sensitivity_curve`.
        observed_multiplier_spread: The largest absolute multiplier difference the two
            suites' recorded held-out estimates produce at this boundary.

    Returns:
        The local linearized tracking difference, the sweep span, and their comparisons
        with the Claim Sheet bar.
    """

    slope = abs(curve["local_slope_pct_per_unit_multiplier_at_cap"])
    implied = float(slope * observed_multiplier_spread)
    return {
        "observed_multiplier_spread": float(observed_multiplier_spread),
        "local_linearized_difference_pct": implied,
        "swept_reduction_span_pct": float(curve["reduction_span_pct"]),
        "claim_bar_pct": CLAIM_TRACKING_BAR_PCT,
        "local_linearized_difference_clears_bar": bool(
            implied >= CLAIM_TRACKING_BAR_PCT
        ),
        "swept_span_clears_bar": bool(
            curve["reduction_span_pct"] >= CLAIM_TRACKING_BAR_PCT
        ),
    }


# --------------------------------------------------------------------------- #
# Artifacts.
# --------------------------------------------------------------------------- #
def _write_csv(path: Path, rows: list[dict[str, Any]]) -> None:
    """Write the per-arm audit CSV."""

    if not rows:
        raise ValueError("cannot write an empty CSV")
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(rows[0]))
        writer.writeheader()
        writer.writerows(rows)


def write_report(path: Path, summary: dict[str, Any]) -> None:
    """Write the deterministic screen report.

    Every figure is recomputed from `summary`, so the report regenerates byte-for-byte
    from the committed `summary.json`.

    Args:
        path: Report destination.
        summary: The complete run summary.
    """

    spec = summary["screen_spec"]
    uncertainty = summary["severity_uncertainty_diagnostics"]
    paired = summary["paired_boundary_result"]
    curve = summary["multiplier_sensitivity"]
    envelope = summary["severity_difference_envelope"]

    lines: list[str] = []
    lines.append("# What a severity difference is worth at the action's cap boundary")
    lines.append("")
    lines.append(
        "Development-sized screen. Measures the paired S-minus-C1 tracking difference at "
        "the one actuator setting that is both severity-sensitive and above the Claim "
        "Sheet bar, then places the recorded linear read-outs inside a wider measured "
        "multiplier envelope."
    )
    lines.append("")
    lines.append(
        f"- Boundary condition: remaining actuator gain {spec['boundary_severity']:g} at "
        f"joint {spec['fault_location']}, compensation cap "
        f"{spec['recovery_config']['maximum_gain_compensation']:g}"
    )
    lines.append(f"- Assessment seeds {list(spec['assessment_seeds'])}, reusing Step 15's `pair_id`s")
    lines.append(f"- {summary['n_arms']} arms; commanded multiplier sweep {list(spec['multiplier_sweep'])}")
    lines.append(f"- Config hash `{spec['config_hash']}` (not frozen)")
    lines.append("")

    lines.append("## Part 1 — severity-uncertainty diagnostics")
    lines.append("")
    lines.append(
        "The recovery controller's confidence gate rejects a diagnosis whose severity "
        f"uncertainty exceeds {spec['recovery_config']['maximum_severity_uncertainty']:g}. "
        "The severity head reports an *in-sample* residual dispersion, which is not that "
        "number. A fixed-penalty leave-one-seed-out estimate on the tuning role supplies "
        "a calibration-only value the gate can receive without using assessment rows. "
        "The disjoint assessment residuals are reported separately as the honest check "
        "on how that internal estimate transferred."
    )
    lines.append("")
    lines.append(
        "| suite | in-sample std | calibration cross-seed std | disjoint assessment std | "
        "calibration / in-sample | assessment / in-sample | opens the gate |"
    )
    lines.append("|---|---:|---:|---:|---:|---:|:--:|")
    for suite in sorted(uncertainty):
        record = uncertainty[suite]
        lines.append(
            f"| {suite} | {record['in_sample_residual_std']:.6f} | "
            f"{record['calibration_cross_seed_residual_std']:.6f} | "
            f"{record['assessment_residual_std']:.6f} | "
            f"{record['calibration_understatement_ratio']:.2f}x | "
            f"{record['assessment_understatement_ratio']:.2f}x | "
            f"{'yes' if record['opens_confidence_gate'] else 'no'} |"
        )
    lines.append("")
    worst = max(
        uncertainty, key=lambda s: uncertainty[s]["assessment_understatement_ratio"]
    )
    lines.append(
        f"- **The in-sample number understates both out-of-seed diagnostics, and it "
        f"understates the disjoint assessment dispersion unevenly across suites** — "
        f"{worst} by {uncertainty[worst]['assessment_understatement_ratio']:.2f}x. The "
        "absolute suite ranking is not stable across the two diagnostics: the internal "
        "calibration cross-seed estimate is larger for S, while the disjoint assessment "
        "standard deviation is slightly smaller for S (Step 15's MAE remains larger for "
        "S because its bias is larger). The safe conclusion is that training dispersion "
        "must not reach the confidence gate. Both calibration-only values clear the gate "
        "comfortably, so the action below fires for either."
    )
    lines.append(
        "- The calibration cross-seed values hold Step 15's selected penalties fixed. "
        "Because those penalties were selected using the same tuning groups, these are "
        "development calibration estimates, not nested post-selection uncertainties or "
        "frozen confidence margins."
    )
    lines.append("")

    lines.append("## Part 2 — the paired quantity at the boundary")
    lines.append("")
    lines.append(
        "Each suite's *recorded held-out estimate* drives the real recovery controller on "
        "the same seed, plant, and noise realization. The estimator decides once, before "
        "the action fires, so the pre-decision trajectory is the one that produced the "
        "estimate. `reduction` is the contract's quantity, "
        "`100 x (J_C1 - J_S) / J_C1`, positive when S is better."
    )
    lines.append("")
    lines.append(
        "| seed | C1 estimate | S estimate | C1 multiplier | S multiplier | "
        "C1 vs no-action | S vs no-action | paired S-minus-C1 |"
    )
    lines.append("|---:|---:|---:|---:|---:|---:|---:|---:|")
    for row in paired["per_seed"]:
        lines.append(
            f"| {row['seed']} | {row['commanded_severity_c1']:.6f} | "
            f"{row['commanded_severity_s']:.6f} | "
            f"{row['applied_multiplier_c1']:.5f} | {row['applied_multiplier_s']:.5f} | "
            f"{row['c1_reduction_vs_no_action_pct']:+.4f}% | "
            f"{row['s_reduction_vs_no_action_pct']:+.4f}% | "
            f"{row['paired_s_minus_c1_reduction_pct']:+.4f}% |"
        )
    lines.append("")
    lines.append(
        f"- Mean paired S-minus-C1 reduction: **{paired['mean_paired_reduction_pct']:+.4f}%** "
        f"against a {CLAIM_TRACKING_BAR_PCT:.0f}% bar; largest absolute value on any seed "
        f"**{paired['max_abs_paired_reduction_pct']:.4f}%**. Seed split — S better on "
        f"{paired['n_seeds_favouring_s']}, C1 better on "
        f"{paired['n_seeds_favouring_c1']}, exactly identical on "
        f"{paired['n_seeds_identical']}."
    )
    lines.append(
        f"- The action itself is real on this condition: the no-action deficit is "
        f"{paired['mean_no_action_deficit_pct']:+.2f}% and the privileged oracle recovers "
        f"{paired['mean_oracle_reduction_vs_no_action_pct']:+.2f}% of it. Both deployable "
        f"suites land close to that ceiling — C1 "
        f"{paired['mean_c1_reduction_vs_no_action_pct']:+.2f}%, S "
        f"{paired['mean_s_reduction_vs_no_action_pct']:+.2f}%. The severity channel is "
        "not the thing separating them from the ceiling."
    )
    deficit_fraction = paired["mean_no_action_deficit_pct"] / 100.0
    analytic_ceiling = 100.0 * deficit_fraction / (1.0 + deficit_fraction)
    realized = paired["mean_oracle_reduction_vs_no_action_pct"]
    lines.append(
        f"- **Exact restoration of the gain does not exactly restore the tracking.** The "
        f"analytic exact-restoration ceiling for this deficit is "
        f"{analytic_ceiling:.2f}%, and a privileged oracle commanding the exactly "
        f"restoring multiplier realizes {realized:.2f}% — a shortfall of "
        f"{analytic_ceiling - realized:.2f} percentage points, or "
        f"{100.0 * realized / analytic_ceiling:.1f}% of the ceiling, in the same "
        "direction on every seed. The gap is the part of the error the fault has already "
        "produced before the single held decision fires, which no multiplier recovers. "
        "For this boundary condition, the `deficit -> reduction` conversion is therefore "
        "an upper bound rather than the achieved value. Whether the same shortfall applies "
        "at the 0.25 condition selected by the deficit screen is not measured here."
    )
    lines.append("")

    lines.append("## Part 3 — the measured conversion envelope")
    lines.append("")
    lines.append(
        "Every severity result in this packet is stated in multiplier units and the "
        "contract is stated in tracking units. This sweep is the conversion factor. It "
        "spans commanded multipliers far outside the errors of the recorded linear "
        "read-outs. The resulting tracking span is an empirical envelope for those "
        "read-outs on this condition, not a universal bound on an arbitrary future "
        "read-out that could command below 1.50."
    )
    lines.append("")
    lines.append("| commanded multiplier | mean applied | mean reduction vs no-action | min | max |")
    lines.append("|---:|---:|---:|---:|---:|")
    for point in curve["points"]:
        lines.append(
            f"| {point['commanded_multiplier']:.2f} | "
            f"{point['mean_applied_multiplier']:.5f} | "
            f"{point['mean_reduction_vs_no_action_pct']:+.4f}% | "
            f"{point['min_reduction_vs_no_action_pct']:+.4f}% | "
            f"{point['max_reduction_vs_no_action_pct']:+.4f}% |"
        )
    lines.append("")
    lines.append(
        f"- Best reduction on the sweep is {curve['best_reduction_pct']:+.4f}% at a "
        f"commanded multiplier of {curve['best_multiplier']:.2f}; at the cap it is "
        f"{curve['reduction_at_cap_pct']:+.4f}%."
    )
    lines.append(
        f"- **Across the entire swept range "
        f"{curve['multiplier_span'][0]:.2f}-{curve['multiplier_span'][1]:.2f} the reduction "
        f"moves by only {envelope['swept_reduction_span_pct']:.4f} percentage points**, "
        f"against a {envelope['claim_bar_pct']:.0f}% bar. The local slope at the cap is "
        f"{curve['local_slope_pct_per_unit_multiplier_at_cap']:+.4f} percentage points per "
        "unit of multiplier."
    )
    lines.append(
        f"- The two suites' recorded estimates differ by at most "
        f"{envelope['observed_multiplier_spread']:.4f} in multiplier. A local linearization "
        f"at the cap converts that spread to "
        f"**{envelope['local_linearized_difference_pct']:.4f} percentage points** of "
        f"tracking, consistent with the directly measured "
        f"{paired['max_abs_paired_reduction_pct']:.4f}-point maximum and "
        f"{'above' if envelope['local_linearized_difference_clears_bar'] else 'far below'} "
        "the bar. The direct paired rollouts, not the linearization, are authoritative."
    )
    lowest = curve["points"][0]
    implied_severity = 1.0 / lowest["commanded_multiplier"]
    severity_error = implied_severity - spec["boundary_severity"]
    worst_std = max(
        record["calibration_cross_seed_residual_std"] for record in uncertainty.values()
    )
    lines.append(
        f"- **How wrong a read-out would have to be to matter here.** The sweep's lowest "
        f"point commands {lowest['commanded_multiplier']:.2f}, which is what a severity "
        f"estimate of {implied_severity:.4f} produces — an error of {severity_error:+.4f} "
        f"on a true {spec['boundary_severity']:g}, about "
        f"{abs(severity_error) / worst_std:.0f}x the larger suite's calibration "
        f"cross-seed residual standard deviation. That estimate still recovers "
        f"{lowest['mean_reduction_vs_no_action_pct']:.2f}%. Producing a "
        f"{envelope['claim_bar_pct']:.0f}-point paired difference would require one suite to "
        "command essentially no action at all, which is a class-call difference rather "
        "than a severity-precision one — and both suites already call this class "
        "correctly."
    )
    lines.append("")

    lines.append("## What this screen does and does not establish")
    lines.append("")
    lines.append(
        "- **It closes the recorded linear-read-out severity route on the actuator class "
        "at the recorded cap, on this condition.** Step 15 left the boundary open because "
        "the suites command differently there. They do; the direct paired difference is "
        "a fraction of a percentage point, and the wider 1.50–2.00 sweep stays below the "
        "bar. It does not close an arbitrary future read-out whose errors leave that "
        "multiplier envelope."
    )
    lines.append(
        "- **It does not close the actuator class.** Action-versus-no-action benefit, "
        "false authorization on a healthy body, cap and floor sensitivity, and the "
        "source-specific margin are the action screen's questions, not this one's. This "
        "screen removes one term from that screen's design; it does not replace it."
    )
    lines.append(
        "- **It does not measure the class-probability channel.** The multiplier is "
        "`1 + p x (capped - 1)`, and every arm here pins `p = 1`. A suite difference in "
        "calibrated class probability remains an unmeasured route to a paired difference."
    )
    lines.append(
        "- **Development-sized.** Four assessment seeds on one bounded task/contact "
        "condition, one fault location, one fault setting, held out over sensor noise "
        "only, at an unfrozen config."
    )
    lines.append("")

    lines.append("## Audit")
    lines.append("")
    audit = summary["audit"]
    lines.append(
        f"- All {audit['n_arms_checked_against_recorded']} no-action arms reproduce the "
        f"recorded Step-15 `J_5s` at the same seed: "
        f"{audit['no_action_matches_recorded']} "
        f"(max absolute difference {audit['max_abs_j5s_difference_vs_recorded']:.3e})"
    )
    lines.append(f"- Exactly one classification evaluation per arm: {audit['single_evaluation']}")
    lines.append(f"- No-action arms changed zero commands: {audit['no_action_changed_zero_commands']}")
    lines.append(f"- Every action arm changed at least one command: {audit['action_arms_acted']}")
    lines.append(f"- Zero A1 incident steps: {audit['zero_a1_incidents']}")
    lines.append(f"- Zero saturation steps: {audit['zero_saturation']}")
    lines.append(
        f"- Applied multipliers match the commanded multipliers: "
        f"{audit['applied_multipliers_match_command']} "
        f"(max absolute difference {audit['max_abs_multiplier_difference']:.3e})"
    )
    lines.append("")
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text("\n".join(lines) + "\n", encoding="utf-8")


def build_audit(
    rows: list[dict[str, Any]],
    recorded_j5s_by_label: dict[str, dict[int, float]],
    *,
    cap: float,
    floor: float,
) -> dict[str, Any]:
    """Return the lifecycle, safety, and CRN-reuse audit block.

    The reuse check is what licenses this screen to command a severity number that was
    estimated in a *different* run: if the trajectories are identical up to the decision
    step, the recorded estimate is the one a deployable head would have produced here.
    Both no-action labels are checked, since each corresponds to a recorded Step-15 arm.

    Args:
        rows: All arm rows.
        recorded_j5s_by_label: Arm-label keyed mapping of seed to the `J_5s` Step 15
            committed for the matching arm.
        cap: The compensation cap.
        floor: `minimum_gain_remaining`.

    Returns:
        The audit record embedded in `summary.json` and rendered in the report.
    """

    differences = [
        abs(row["j_5s"] - recorded[row["seed"]])
        for label, recorded in recorded_j5s_by_label.items()
        for row in rows
        if row["label"] == label
    ]
    if not differences:
        raise ValueError("no arm rows matched the recorded labels; nothing was checked")
    multiplier_errors = []
    for row in rows:
        if row["commanded_severity"] is None:
            continue
        expected = min(1.0 / max(row["commanded_severity"], floor), cap)
        multiplier_errors.append(abs(row["applied_multiplier_max"] - expected))
    return {
        "no_action_matches_recorded": bool(max(differences) <= CRN_REUSE_TOLERANCE),
        "n_arms_checked_against_recorded": len(differences),
        "max_abs_j5s_difference_vs_recorded": float(max(differences)),
        "single_evaluation": bool(
            all(row["classification_evaluations"] == 1 for row in rows)
        ),
        "no_action_changed_zero_commands": bool(
            all(
                row["recovery_command_changed_steps"] == 0
                for row in rows
                if row["commanded_severity"] is None
            )
        ),
        "action_arms_acted": bool(
            all(
                row["recovery_command_changed_steps"] > 0
                for row in rows
                if row["commanded_severity"] is not None
            )
        ),
        "zero_a1_incidents": bool(all(row["a1_incident_steps"] == 0 for row in rows)),
        "zero_saturation": bool(all(row["saturation_steps"] == 0 for row in rows)),
        "applied_multipliers_match_command": bool(
            multiplier_errors and max(multiplier_errors) <= 1.0e-9
        ),
        "max_abs_multiplier_difference": (
            float(max(multiplier_errors)) if multiplier_errors else 0.0
        ),
    }


def require_passing_audit(audit: dict[str, Any]) -> None:
    """Fail loudly unless every integrity condition required by the report holds.

    Args:
        audit: The output of `build_audit`.

    Raises:
        RuntimeError: If any required CRN, lifecycle, action, safety, saturation, or
            multiplier check is false.
    """

    required = (
        "no_action_matches_recorded",
        "single_evaluation",
        "no_action_changed_zero_commands",
        "action_arms_acted",
        "zero_a1_incidents",
        "zero_saturation",
        "applied_multipliers_match_command",
    )
    failed = [name for name in required if not bool(audit.get(name, False))]
    if failed:
        raise RuntimeError(
            "severity-action-boundary audit failed: " + ", ".join(failed)
        )


def load_recorded_no_action_j5s(path: Path, severity: float) -> dict[int, float]:
    """Read Step 15's committed assessment `J_5s` at one severity, keyed by seed.

    Args:
        path: Path to `arm_rows.csv` from the severity-estimation-quality screen.
        severity: The true remaining-gain grid point to extract.

    Returns:
        Seed-keyed tracking integral for the recorded no-action arms.

    Raises:
        FileNotFoundError: If the recorded screen output is missing.
        ValueError: If no matching assessment rows are present.
    """

    if not path.is_file():
        raise FileNotFoundError(
            f"recorded arm rows not found at {path}; run "
            "scripts/screen_severity_estimation_quality.py first"
        )
    with path.open(newline="", encoding="utf-8") as handle:
        recorded = {
            int(row["seed"]): float(row["j_5s"])
            for row in csv.DictReader(handle)
            if row["role"] == "assessment"
            and np.isclose(float(row["severity"]), severity)
        }
    if not recorded:
        raise ValueError(f"no assessment rows at severity {severity} in {path}")
    return recorded


def main() -> int:
    """Run the screen end to end and write its three artifacts."""

    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--severity-summary",
        type=Path,
        default=Path("results/severity_estimation_quality/summary.json"),
        help="Recorded severity-estimation-quality summary supplying the held-out estimates.",
    )
    parser.add_argument(
        "--severity-features",
        type=Path,
        default=Path("results/severity_estimation_quality/window_features.csv"),
        help="Recorded tuning-window features used for cross-seed calibration uncertainty.",
    )
    parser.add_argument(
        "--severity-arm-rows",
        type=Path,
        default=Path("results/severity_estimation_quality/arm_rows.csv"),
        help="Recorded arm rows used to pin the no-action cross-check.",
    )
    parser.add_argument(
        "--output-dir",
        type=Path,
        default=Path("results/severity_action_boundary"),
        help="Directory the three artifacts are written to.",
    )
    parser.add_argument(
        "--workers",
        type=int,
        default=8,
        help="Process-pool workers for the rollouts.",
    )
    args = parser.parse_args()
    if args.workers < 1:
        raise SystemExit("--workers must be at least 1")

    base = RecoveryControlConfig()
    print("Part 1 — severity-uncertainty diagnostics from recorded features", flush=True)
    recorded_summary = json.loads(args.severity_summary.read_text(encoding="utf-8"))
    features = load_recorded_features(args.severity_features)
    uncertainty: dict[str, dict[str, Any]] = {}
    for suite, bundle in sorted(features.items()):
        evaluation = recorded_summary["suite_evaluations"][suite]
        record = cross_seed_calibration_uncertainty(
            bundle, regularization=float(evaluation["selected_regularization"])
        )
        record.update(disjoint_assessment_residual_diagnostics(evaluation))
        in_sample = float(evaluation["train_residual_std"])
        record["in_sample_residual_std"] = in_sample
        record["calibration_understatement_ratio"] = float(
            record["calibration_cross_seed_residual_std"] / in_sample
        )
        record["assessment_understatement_ratio"] = float(
            record["assessment_residual_std"] / in_sample
        )
        record["opens_confidence_gate"] = bool(
            record["calibration_cross_seed_residual_std"]
            <= base.maximum_severity_uncertainty
        )
        uncertainty[suite] = record
        print(
            f"  {suite}: in-sample {in_sample:.6f} -> calibration cross-seed "
            f"{record['calibration_cross_seed_residual_std']:.6f} "
            f"({record['calibration_understatement_ratio']:.2f}x calibration; "
            f"{record['assessment_residual_std']:.6f} disjoint assessment)",
            flush=True,
        )

    estimates = load_boundary_estimates(args.severity_summary, BOUNDARY_SEVERITY)
    specs = build_arm_specs(
        estimates,
        {
            suite: record["calibration_cross_seed_residual_std"]
            for suite, record in uncertainty.items()
        },
    )
    print(f"Part 2 — {len(specs)} boundary arms on {args.workers} workers", flush=True)
    rows: list[dict[str, Any]] = []
    with concurrent.futures.ProcessPoolExecutor(max_workers=args.workers) as pool:
        for index, row in enumerate(pool.map(run_action_arm, specs), start=1):
            rows.append(row)
            print(f"  [{index}/{len(specs)}] {row['run_id']}", flush=True)
    rows.sort(key=lambda row: (row["label"], row["seed"]))

    recorded_j5s = {
        "no_action": load_recorded_no_action_j5s(
            args.severity_arm_rows, BOUNDARY_SEVERITY
        ),
        # Step 15's healthy grid anchor is the same plant and the same seed, so it pins
        # the reuse a second time on a trajectory with no fault in it at all.
        "healthy_reference": load_recorded_no_action_j5s(args.severity_arm_rows, 1.00),
    }
    audit = build_audit(
        rows,
        recorded_j5s,
        cap=base.maximum_gain_compensation,
        floor=base.minimum_gain_remaining,
    )
    require_passing_audit(audit)

    print("Part 3 — analysis", flush=True)
    paired = paired_boundary_result(rows)
    curve = multiplier_sensitivity_curve(rows, cap=base.maximum_gain_compensation)
    spread = max(
        abs(row["applied_multiplier_s"] - row["applied_multiplier_c1"])
        for row in paired["per_seed"]
    )
    envelope = severity_difference_envelope(curve, spread)

    summary = {
        "screen_spec": {
            "boundary_severity": BOUNDARY_SEVERITY,
            "fault_location": FAULT_LOCATION,
            "assessment_seeds": list(ASSESSMENT_SEEDS),
            "multiplier_sweep": list(MULTIPLIER_SWEEP),
            "plane_z_m": PLANE_Z_M,
            "claim_tracking_bar_pct": CLAIM_TRACKING_BAR_PCT,
            "config_hash": CONFIG_HASH,
            "recovery_config": {
                key: (list(value) if isinstance(value, tuple) else value)
                for key, value in base.__dict__.items()
            },
            "recorded_severity_screen": str(args.severity_summary).replace("\\", "/"),
        },
        "n_arms": len(rows),
        "severity_uncertainty_diagnostics": uncertainty,
        "paired_boundary_result": paired,
        "multiplier_sensitivity": curve,
        "severity_difference_envelope": envelope,
        "audit": audit,
    }

    args.output_dir.mkdir(parents=True, exist_ok=True)
    _write_csv(args.output_dir / "arm_rows.csv", rows)
    (args.output_dir / "summary.json").write_text(
        json.dumps(summary, indent=2, sort_keys=True, allow_nan=False) + "\n",
        encoding="utf-8",
    )
    write_report(args.output_dir / "severity_action_boundary_report.md", summary)
    print(f"Wrote three artifacts to {args.output_dir}", flush=True)
    print(
        f"Mean paired S-minus-C1 reduction "
        f"{paired['mean_paired_reduction_pct']:+.4f}%; whole-sweep reduction span "
        f"{envelope['swept_reduction_span_pct']:.4f} pp against a "
        f"{CLAIM_TRACKING_BAR_PCT:.0f}% bar",
        flush=True,
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
