"""Screen severity-estimation quality against the severity-sensitivity of the action.

Every recovery number recorded so far has been produced with a severity that came from
somewhere other than a deployable estimator: a privileged oracle (the action family's
ceiling) or a pinned stand-in constant. The recovery controller's actuator action is
severity-conditioned, so "how well can a deployable suite estimate severity?" is an
unmeasured term sitting underneath every control result the project has recorded. It is
also one unmeasured place where the contract's paired S-minus-C1 control quantity could be non-zero
on a fault class the conventional suite already detects: both suites call the class
identically, but they might not size it identically.

This screen answers that in two parts, which have to be read together.

Part A — the action-sensitivity map (analytic, no rollouts). The controller's actuator
multiplier is ``min(1 / max(severity, minimum_gain_remaining), maximum_gain_compensation)``.
That function is flat below a threshold estimate, so over a whole interval of severity
estimates *every* estimator produces the identical command. Part A locates that interval,
crosses it against the per-class no-action deficits the tracking-deficit screen recorded,
and reports where on the severity grid a severity difference between two suites could
change the action at all — as a function of the compensation cap, so the pending
"raise the cap" proposal is quantified before it is run.

Part B — measured severity-estimation accuracy, C1 versus S (rollouts). A matched
`SeverityRidgeHead` is fitted per suite on tuning seeds and evaluated on disjoint
assessment seeds over an actuator-gain severity grid, on the same bounded task, contact
plane, observed-state controller, diagnostic probe, and single-held-decision lifecycle
every recent screen uses. The suites are exactly paired: one S rollout per arm, physically
projected to C1, so the two suites see the same trajectory and the same noise on shared
channels. Part B then pushes both suites' held-out estimates through Part A's multiplier
to report the only quantity that matters for the contract — how often, and by how much,
the two suites would have commanded differently.

This is development-sized evidence about a linear read-out, not a validation-sized or
frozen-config result, and a learned head could raise both suites. It bounds the severity
channel; it does not close it.

Run from `Reproducibility Packet/`:
    .\\.venv\\Scripts\\python.exe scripts\\screen_severity_estimation_quality.py --workers 8
"""

from __future__ import annotations

import argparse
import concurrent.futures
import csv
import json
import sys
from dataclasses import asdict, dataclass
from pathlib import Path
from typing import Any

import numpy as np

sys.path.insert(0, str(Path(__file__).resolve().parent))

from run_noisy_reference_pilot import project_observed_suite  # noqa: E402
from screen_bounded_task_contact import (  # noqa: E402
    BoundedTaskContactSpec,
    SingleDecisionHoldEstimator,
    cable_config,
)
from utils.cable_plant import CablePlant  # noqa: E402
from utils.estimator import (  # noqa: E402
    SOURCE_CLASS_ORDER,
    EstimatorOutput,
    SeverityRidgeHead,
    WindowFeatureExtractor,
)
from utils.metrics import j_5s  # noqa: E402
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

#: Remaining actuator gain at joint 1. 0.55 and 0.40 straddle the 0.50 compensation-cap
#: threshold, while 0.50 itself pins the one-sided boundary that the recorded deficit
#: screen identifies as having enough exact-restoration headroom to clear the Claim-Sheet
#: bar. Omitting the boundary would miss estimator errors that straddle the cap kink.
SEVERITY_GRID: tuple[float, ...] = (1.00, 0.85, 0.70, 0.55, 0.50, 0.40, 0.25, 0.10)

#: Fit seeds. Disjoint from every other screen's seeds so no CRN substream is shared.
TUNING_SEEDS: tuple[int, ...] = (17000, 17001, 17002, 17003, 17004, 17005)

#: Held-out evaluation seeds, disjoint from `TUNING_SEEDS`.
ASSESSMENT_SEEDS: tuple[int, ...] = (17100, 17101, 17102, 17103)

#: Ridge penalties searched by leave-one-seed-out cross-validation on the tuning seeds
#: only. Assessment rows never enter model selection.
REGULARIZATION_GRID: tuple[float, ...] = (0.1, 1.0, 10.0, 100.0, 1000.0)

#: Contact plane height, matching the bounded task/contact profile every recent screen uses.
PLANE_Z_M = 0.200

#: Compensation caps swept in Part A. 2.0 is the recorded controller default.
CAP_SWEEP: tuple[float, ...] = (2.0, 3.0, 4.0, 6.0, 8.0)

#: The Claim Sheet's control bar, in reduction percent.
CLAIM_TRACKING_BAR_PCT = 10.0

#: Development config hash. `dev-` prefixed: no `dev-` trace may enter confirmatory analysis.
CONFIG_HASH = "dev-severity-estimation-quality-screen"

#: Joint carrying the actuator fault.
FAULT_LOCATION = 1


# --------------------------------------------------------------------------- #
# Part A — the action-sensitivity map.
# --------------------------------------------------------------------------- #
def gain_action_multiplier(
    severity_estimate: float,
    config: RecoveryControlConfig,
    *,
    source_probability: float = 1.0,
) -> float:
    """Return the actuator multiplier the recovery controller applies for an estimate.

    This mirrors `GainScheduledRecoveryController.recovery_command`'s actuator branch as
    a scalar function so the map can be reasoned about analytically. It is pinned to the
    controller by a regression test that compares it against the real controller's
    applied command over a severity grid; it is not an independent model of the action.

    Args:
        severity_estimate: Estimated remaining gain fraction, in `(0, 1]`.
        config: The recovery controller configuration supplying the floor and the cap.
        source_probability: Calibrated actuator-class probability, `1.0` at a one-hot call.

    Returns:
        The multiplicative factor applied to the faulted joint's nominal command.

    Raises:
        ValueError: If the estimate is outside `(0, 1]` or the probability is not in `[0, 1]`.
    """

    estimate = float(severity_estimate)
    if not np.isfinite(estimate) or not 0.0 < estimate <= 1.0:
        raise ValueError("severity_estimate must be finite and in (0, 1]")
    probability = float(source_probability)
    if not np.isfinite(probability) or not 0.0 <= probability <= 1.0:
        raise ValueError("source_probability must be finite and in [0, 1]")
    effective_remaining = max(estimate, config.minimum_gain_remaining)
    capped = min(1.0 / effective_remaining, config.maximum_gain_compensation)
    return float(1.0 + probability * (capped - 1.0))


def severity_sensitive_interval(config: RecoveryControlConfig) -> tuple[float, float]:
    """Return the open interval of severity estimates over which the action still varies.

    Below the lower bound the compensation cap binds and every estimate yields the same
    multiplier; at or above the upper bound the action is the identity. Two estimators
    that both land outside this interval on the same side are *behaviourally identical*
    however far apart their numbers are.

    Args:
        config: The recovery controller configuration.

    Returns:
        `(low, high)`: the exclusive lower and upper severity bounds of sensitivity. The
        interval is empty when `low >= high`.
    """

    low = max(1.0 / config.maximum_gain_compensation, config.minimum_gain_remaining)
    return (float(low), 1.0)


def exact_restoration_ceiling_pct(deficit_pct: float) -> float:
    """Convert a no-action healthy-relative deficit into the reduction full restoration gives.

    The contract's control quantity has the degraded arm in the denominator, so a deficit
    `D` maps to a reduction `D / (1 + D)`. This is the same conversion the tracking-deficit
    screen's gate uses; it is recomputed here rather than imported so this screen's report
    stands alone.

    Args:
        deficit_pct: `100 * (J_fault - J_healthy) / J_healthy`.

    Returns:
        `100 * (J_fault - J_healthy) / J_fault`.
    """

    fraction = float(deficit_pct) / 100.0
    return float(100.0 * fraction / (1.0 + fraction))


def action_sensitivity_map(
    deficits_by_severity: dict[float, float],
    *,
    caps: tuple[float, ...] = CAP_SWEEP,
    bar_pct: float = CLAIM_TRACKING_BAR_PCT,
    base_config: RecoveryControlConfig | None = None,
) -> dict[str, Any]:
    """Cross the action's severity-sensitivity against the recorded per-class headroom.

    For every compensation cap, a severity grid point is classified on two independent
    axes: whether it lands inside the sensitive interval or exactly on its one-sided lower
    boundary (so estimator error can change the command), and whether the setting's
    exact-restoration ceiling clears the contract bar (so a better command could be worth
    the bar). A severity advantage can only reach the contract where both hold.

    Args:
        deficits_by_severity: Recorded no-action deficit percent keyed by remaining gain.
        caps: Compensation caps to sweep.
        bar_pct: The Claim Sheet's reduction bar.
        base_config: Controller config supplying the gain floor; default `RecoveryControlConfig()`.

    Returns:
        A JSON-safe mapping with the per-cap rows and the derived joint-region summary.
    """

    base = base_config or RecoveryControlConfig()
    rows: list[dict[str, Any]] = []
    for cap in caps:
        config = RecoveryControlConfig(
            maximum_gain_compensation=float(cap),
            minimum_gain_remaining=base.minimum_gain_remaining,
        )
        low, high = severity_sensitive_interval(config)
        for severity, deficit in sorted(deficits_by_severity.items(), reverse=True):
            ceiling = exact_restoration_ceiling_pct(deficit)
            sensitive = bool(low < severity < high)
            at_boundary = bool(np.isclose(severity, low, rtol=0.0, atol=1.0e-12))
            can_change_action = bool(sensitive or at_boundary)
            above_bar = bool(ceiling >= bar_pct)
            rows.append(
                {
                    "maximum_gain_compensation": float(cap),
                    "sensitive_interval_low": low,
                    "sensitive_interval_high": high,
                    "severity": float(severity),
                    "no_action_deficit_pct": float(deficit),
                    "exact_restoration_ceiling_pct": ceiling,
                    "multiplier_at_true_severity": gain_action_multiplier(
                        severity, config
                    ),
                    "severity_sensitive": sensitive,
                    "severity_at_sensitivity_boundary": at_boundary,
                    "severity_estimation_can_change_action": can_change_action,
                    "ceiling_clears_bar": above_bar,
                    "severity_advantage_can_reach_contract": bool(
                        can_change_action and above_bar
                    ),
                }
            )
    by_cap: dict[str, Any] = {}
    for cap in caps:
        matching = [r for r in rows if r["maximum_gain_compensation"] == float(cap)]
        reachable = [
            r["severity"] for r in matching if r["severity_advantage_can_reach_contract"]
        ]
        by_cap[f"{cap:.1f}"] = {
            "sensitive_interval_low": matching[0]["sensitive_interval_low"],
            "reachable_severities": sorted(reachable, reverse=True),
            "n_reachable": len(reachable),
        }
    smallest_reachable_cap = None
    for cap in sorted(caps):
        if by_cap[f"{cap:.1f}"]["n_reachable"] > 0:
            smallest_reachable_cap = float(cap)
            break
    return {
        "bar_pct": float(bar_pct),
        "minimum_gain_remaining": float(base.minimum_gain_remaining),
        "rows": rows,
        "by_cap": by_cap,
        "smallest_cap_with_a_reachable_severity": smallest_reachable_cap,
    }


# --------------------------------------------------------------------------- #
# Part B — rollout arms and the matched per-suite severity read-out.
# --------------------------------------------------------------------------- #
class WindowCaptureEstimator:
    """Record the observed window at the scheduled decision step and take no action.

    The screen measures what a deployable suite could have estimated from the same window
    every other screen makes its held decision on. It therefore returns a healthy one-hot
    output so the recovery controller never engages: these are no-action arms, and the
    trajectory they record is the plain faulted rollout.
    """

    def __init__(self) -> None:
        """Create the capture with no recorded window."""

        self.window = None
        self.calls = 0

    def reset(self) -> None:
        """Clear the captured window before a new rollout."""

        self.window = None
        self.calls = 0

    def update(self, step_index: int, decision_time_s: float, window):
        """Capture the window and return the fail-safe healthy output."""

        self.calls += 1
        if window is not None:
            self.window = window
        probabilities = np.zeros(len(SOURCE_CLASS_ORDER), dtype=float)
        probabilities[SOURCE_CLASS_ORDER.index("healthy")] = 1.0
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


@dataclass(frozen=True)
class ArmSpec:
    """One rollout: a severity grid point observed under one sensor seed in one role."""

    severity: float
    seed: int
    role: str
    suite: str = "S"


def _actuator_fault(severity: float, onset_index: int) -> FaultSpec:
    """Return the joint-1 actuator-gain fault for a remaining-gain grid point.

    A remaining fraction of exactly 1.0 is physically the healthy plant and is used as the
    top-of-range anchor for the regression, so it is expressed as the no-fault spec rather
    than a zero-magnitude actuator fault.
    """

    if severity >= 1.0:
        return FaultSpec()
    return FaultSpec(
        source_class="actuator",
        subtype="actuator_gain_loss",
        location=FAULT_LOCATION,
        severity=float(severity),
        onset_index=onset_index,
    )


def run_arm(spec: ArmSpec) -> dict[str, Any]:
    """Run one no-action arm and return its per-suite window features and audit fields.

    Generates the S observation once and physically projects it to C1, so both suites see
    the same trajectory and bitwise-identical shared channels. Returns feature vectors as
    lists so the row is JSON-safe and process-pool friendly.

    Args:
        spec: The arm to run.

    Returns:
        A row carrying the per-suite feature vectors, the tracking integral, and the
        lifecycle/safety audit fields every screen in this packet records.
    """

    mechanics = BoundedTaskContactSpec(
        plane_heights_z_m=(0.100, PLANE_Z_M), sensor_seed=spec.seed
    )
    pair_id = f"severity-quality-{spec.role}-{spec.seed}"
    run_id = f"{pair_id}-gain{spec.severity:.2f}-{spec.suite}"
    plant = CablePlant(
        cable_config(mechanics, PLANE_Z_M),
        point_count=mechanics.point_count,
        simulation_timestep_s=mechanics.simulation_timestep_s,
        fault=_actuator_fault(spec.severity, mechanics.onset_index),
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
    capture = WindowCaptureEstimator()
    estimator = SingleDecisionHoldEstimator(
        capture, first_decision_step=mechanics.first_decision_step
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
    if capture.window is None:
        raise RuntimeError(
            f"no observed window was delivered at the decision step for {run_id}"
        )
    extractor = WindowFeatureExtractor(window_steps=mechanics.window_steps)
    features: dict[str, list[float]] = {}
    if spec.suite == "S":
        features["S"] = extractor.window_features(capture.window).tolist()
        features["C1"] = extractor.window_features(
            project_observed_suite(capture.window, "C1")
        ).tolist()
    else:
        features[spec.suite] = extractor.window_features(capture.window).tolist()

    nominal = np.stack(policy.nominal_commands)
    applied = np.stack(policy.commands)
    changed = int(
        np.count_nonzero(
            np.any(~np.isclose(nominal, applied, rtol=0.0, atol=1e-12), axis=1)
        )
    )
    return {
        "severity": float(spec.severity),
        "seed": int(spec.seed),
        "role": spec.role,
        "generated_suite": spec.suite,
        "run_id": run_id,
        "features": features,
        "j_5s": float(
            j_5s(
                rollout.plant.t_s,
                rollout.plant.task_reference,
                rollout.plant.true_task_output,
                mechanics.fault_onset_s,
            )
        ),
        "classification_evaluations": int(estimator.classification_evaluations),
        "recovery_command_changes": changed,
        "a1_incident_steps": int(
            np.count_nonzero(np.any(rollout.plant.safety_flag, axis=1))
        ),
        "saturation_steps": int(
            np.count_nonzero(np.any(rollout.plant.saturation_flag, axis=1))
        ),
        "peak_contact_force_n": float(np.max(rollout.plant.contact_state[:, 0])),
        "max_abs_gauge_microstrain": float(np.max(np.abs(rollout.plant.gauge_true))),
        # Every eighth entry of the summary vector is a column's valid fraction.
        "window_valid_fraction_mean": float(
            np.mean(np.asarray(features[spec.suite])[7::8])
        ),
    }


def _stack(rows: list[dict[str, Any]], suite: str) -> tuple[np.ndarray, np.ndarray]:
    """Return `(features[N, F], severities[N])` for one suite over a set of rows."""

    features = np.asarray([row["features"][suite] for row in rows], dtype=float)
    severities = np.asarray([row["severity"] for row in rows], dtype=float)
    return features, severities


def select_regularization(
    rows: list[dict[str, Any]], suite: str, grid: tuple[float, ...]
) -> dict[str, Any]:
    """Choose a ridge penalty by leave-one-seed-out CV on tuning rows only.

    Holding out whole seeds rather than individual windows keeps the selection honest
    about the axis the assessment split also holds out. Assessment rows are never seen.

    Args:
        rows: Tuning rows only.
        suite: Suite key into each row's feature dict.
        grid: Candidate penalties.

    Returns:
        The selected penalty and the per-penalty cross-validated mean absolute error.
    """

    seeds = sorted({row["seed"] for row in rows})
    if len(seeds) < 2:
        raise ValueError("leave-one-seed-out selection requires at least two seeds")
    scores: list[dict[str, float]] = []
    for penalty in grid:
        errors: list[float] = []
        for held in seeds:
            train = [row for row in rows if row["seed"] != held]
            test = [row for row in rows if row["seed"] == held]
            x_train, y_train = _stack(train, suite)
            x_test, y_test = _stack(test, suite)
            head = SeverityRidgeHead(regularization=penalty).fit(x_train, y_train)
            errors.extend(np.abs(head.predict(x_test) - y_test).tolist())
        scores.append({"regularization": float(penalty), "cv_mae": float(np.mean(errors))})
    best = min(scores, key=lambda item: item["cv_mae"])
    return {"selected_regularization": best["regularization"], "cv_scores": scores}


def evaluate_suite(
    tuning_rows: list[dict[str, Any]],
    assessment_rows: list[dict[str, Any]],
    suite: str,
    grid: tuple[float, ...],
) -> dict[str, Any]:
    """Fit one suite's severity head on tuning rows and score it on assessment rows.

    Args:
        tuning_rows: Fit and model-selection rows.
        assessment_rows: Disjoint held-out rows.
        suite: Suite key into each row's feature dict.
        grid: Ridge penalties to search.

    Returns:
        A JSON-safe record of the selection, the fit, the held-out errors, and the
        per-severity held-out predictions.
    """

    selection = select_regularization(tuning_rows, suite, grid)
    x_train, y_train = _stack(tuning_rows, suite)
    x_test, y_test = _stack(assessment_rows, suite)
    head = SeverityRidgeHead(
        regularization=selection["selected_regularization"]
    ).fit(x_train, y_train)
    predictions = head.predict(x_test)
    errors = predictions - y_test
    per_severity: list[dict[str, float]] = []
    for severity in sorted({float(v) for v in y_test}, reverse=True):
        mask = np.isclose(y_test, severity)
        per_severity.append(
            {
                "severity": float(severity),
                "mean_estimate": float(np.mean(predictions[mask])),
                "std_estimate": float(np.std(predictions[mask])),
                "mean_abs_error": float(np.mean(np.abs(errors[mask]))),
            }
        )
    return {
        "suite": suite,
        "selected_regularization": selection["selected_regularization"],
        "cv_scores": selection["cv_scores"],
        "n_train": head.n_train,
        "n_test": int(x_test.shape[0]),
        "active_feature_count": head.active_feature_count,
        "feature_width": int(x_train.shape[1]),
        "train_residual_std": head.train_residual_std,
        "holdout_mae": float(np.mean(np.abs(errors))),
        "holdout_rmse": float(np.sqrt(np.mean(errors**2))),
        "holdout_max_abs_error": float(np.max(np.abs(errors))),
        "holdout_bias": float(np.mean(errors)),
        "per_severity": per_severity,
        "predictions": [
            {
                "severity": float(true),
                "seed": int(row["seed"]),
                "estimate": float(estimate),
            }
            for row, true, estimate in zip(assessment_rows, y_test, predictions)
        ],
    }


def compare_against_oracle_action(
    evaluation: dict[str, Any],
    *,
    caps: tuple[float, ...] = CAP_SWEEP,
    base_config: RecoveryControlConfig | None = None,
) -> dict[str, Any]:
    """Compare one suite's commanded multiplier against a perfect-severity oracle's.

    Because the multiplier is flat below `1 / cap`, an estimator does not have to be
    accurate to command exactly what an oracle commands — on a fault whose true severity
    is already inside the flat region, *any* estimate that also lands there reproduces the
    oracle's command bit for bit. A true severity exactly on the boundary is different:
    the oracle is capped, but an estimate just above the kink commands less. This reports
    agreement separately for capped-interior, boundary, sensitive, and healthy regimes.

    Args:
        evaluation: `evaluate_suite` record for one suite.
        caps: Compensation caps to sweep.
        base_config: Controller config supplying the gain floor.

    Returns:
        Per-cap agreement rates against the oracle action, overall and split by regime.
    """

    base = base_config or RecoveryControlConfig()
    results: list[dict[str, Any]] = []
    for cap in caps:
        config = RecoveryControlConfig(
            maximum_gain_compensation=float(cap),
            minimum_gain_remaining=base.minimum_gain_remaining,
        )
        low, high = severity_sensitive_interval(config)
        # Four regimes, not two. `capped` is strictly below the cap kink and therefore
        # flat to small estimate errors. `boundary` is the kink itself: the oracle is
        # capped, but an estimate just above the boundary commands less, so estimator
        # noise can create a suite difference. `sensitive` is the varying interior and
        # `identity` is the healthy top anchor, where any action is false authorization.
        agreement: dict[str, list[bool]] = {
            "capped": [],
            "boundary": [],
            "sensitive": [],
            "identity": [],
        }
        differences: list[float] = []
        for row in evaluation["predictions"]:
            truth = float(row["severity"])
            estimate = float(row["estimate"])
            oracle = gain_action_multiplier(truth, config)
            commanded = (
                gain_action_multiplier(estimate, config) if estimate > 0.0 else 1.0
            )
            identical = bool(abs(commanded - oracle) <= 1.0e-12)
            differences.append(abs(commanded - oracle))
            if truth >= high:
                regime = "identity"
            elif np.isclose(truth, low, rtol=0.0, atol=1.0e-12):
                regime = "boundary"
            elif truth > low:
                regime = "sensitive"
            else:
                regime = "capped"
            agreement[regime].append(identical)
        entry: dict[str, Any] = {
            "maximum_gain_compensation": float(cap),
            "mean_abs_multiplier_error": float(np.mean(differences)),
            "max_abs_multiplier_error": float(np.max(differences)),
        }
        for regime, values in agreement.items():
            entry[f"{regime}_region_arms"] = len(values)
            entry[f"{regime}_region_oracle_identical_rate"] = (
                float(np.mean(values)) if values else None
            )
        results.append(entry)
    return {"suite": evaluation["suite"], "caps": results}


def compare_commanded_actions(
    c1_eval: dict[str, Any],
    s_eval: dict[str, Any],
    *,
    caps: tuple[float, ...] = CAP_SWEEP,
    base_config: RecoveryControlConfig | None = None,
) -> dict[str, Any]:
    """Push both suites' held-out severity estimates through the controller's multiplier.

    This is the only quantity the contract cares about. Two suites whose severity numbers
    differ but whose multipliers do not are behaviourally identical, and the paired
    S-minus-C1 control difference on that class is exactly zero by construction rather
    than by measurement.

    Args:
        c1_eval: `evaluate_suite` record for C1.
        s_eval: `evaluate_suite` record for S.
        caps: Compensation caps to sweep.
        base_config: Controller config supplying the gain floor.

    Returns:
        Per-cap counts and magnitudes of commanded-multiplier disagreement.
    """

    base = base_config or RecoveryControlConfig()
    c1_predictions = c1_eval["predictions"]
    s_predictions = s_eval["predictions"]
    if len(c1_predictions) != len(s_predictions):
        raise ValueError("suite prediction sets must be paired one-to-one")
    results: list[dict[str, Any]] = []
    for cap in caps:
        config = RecoveryControlConfig(
            maximum_gain_compensation=float(cap),
            minimum_gain_remaining=base.minimum_gain_remaining,
        )
        low, high = severity_sensitive_interval(config)
        differences: list[float] = []
        # Split the strictly flat interior from the one-sided cap boundary. At the
        # boundary an estimate just above the kink changes the command, so folding it
        # into the capped interior can hide the exact route this screen is meant to test.
        capped_differences: list[float] = []
        boundary_differences: list[float] = []
        per_pair: list[dict[str, float]] = []
        for c1_row, s_row in zip(c1_predictions, s_predictions):
            if not np.isclose(c1_row["severity"], s_row["severity"]) or (
                c1_row["seed"] != s_row["seed"]
            ):
                raise ValueError("suite predictions are not aligned arm-for-arm")
            # A clipped estimate of exactly zero is not a legal severity input; the
            # controller leaves the command untouched, which is a multiplier of 1.
            c1_multiplier = (
                gain_action_multiplier(c1_row["estimate"], config)
                if c1_row["estimate"] > 0.0
                else 1.0
            )
            s_multiplier = (
                gain_action_multiplier(s_row["estimate"], config)
                if s_row["estimate"] > 0.0
                else 1.0
            )
            difference = abs(s_multiplier - c1_multiplier)
            differences.append(difference)
            truth = float(c1_row["severity"])
            if np.isclose(truth, low, rtol=0.0, atol=1.0e-12):
                boundary_differences.append(difference)
            elif truth < low:
                capped_differences.append(difference)
            per_pair.append(
                {
                    "severity": truth,
                    "seed": int(c1_row["seed"]),
                    "c1_multiplier": float(c1_multiplier),
                    "s_multiplier": float(s_multiplier),
                }
            )
        differing = [d for d in differences if d > 1.0e-12]
        capped_differing = [d for d in capped_differences if d > 1.0e-12]
        boundary_differing = [d for d in boundary_differences if d > 1.0e-12]
        results.append(
            {
                "maximum_gain_compensation": float(cap),
                "n_pairs": len(differences),
                "n_multipliers_differ": len(differing),
                "fraction_differ": float(len(differing) / len(differences)),
                "mean_abs_multiplier_difference": float(np.mean(differences)),
                "max_abs_multiplier_difference": float(np.max(differences)),
                "capped_region_pairs": len(capped_differences),
                "capped_region_multipliers_differ": len(capped_differing),
                "capped_region_max_abs_difference": (
                    float(np.max(capped_differences)) if capped_differences else 0.0
                ),
                "boundary_region_pairs": len(boundary_differences),
                "boundary_region_multipliers_differ": len(boundary_differing),
                "boundary_region_max_abs_difference": (
                    float(np.max(boundary_differences))
                    if boundary_differences
                    else 0.0
                ),
                "pairs": per_pair,
            }
        )
    return {"caps": results}


# --------------------------------------------------------------------------- #
# Artifacts.
# --------------------------------------------------------------------------- #
def _write_csv(path: Path, rows: list[dict[str, Any]]) -> None:
    """Write the per-arm audit CSV, excluding the bulky feature vectors."""

    if not rows:
        raise ValueError("cannot write an empty CSV")
    fields = [key for key in rows[0] if key != "features"]
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=fields)
        writer.writeheader()
        for row in rows:
            writer.writerow({key: row[key] for key in fields})


def _write_features_csv(path: Path, rows: list[dict[str, Any]]) -> None:
    """Persist the per-arm, per-suite window feature vectors.

    The rollouts are the expensive part of this screen and the feature vectors are their
    only durable product. Writing them out means the read-out comparison can be refitted
    — with a different model class, penalty, or split — without re-running the physics,
    by anyone, including a reader reproducing this packet.

    Args:
        path: Destination CSV.
        rows: Arm rows carrying a `features` mapping of suite to feature vector.
    """

    if not rows:
        raise ValueError("cannot write an empty CSV")
    width = len(next(iter(rows[0]["features"].values())))
    fields = ["run_id", "severity", "seed", "role", "suite"] + [
        f"f{index}" for index in range(width)
    ]
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=fields)
        writer.writeheader()
        for row in rows:
            for suite, vector in sorted(row["features"].items()):
                if len(vector) != width:
                    raise ValueError("feature vectors must all share one width")
                record = {
                    "run_id": row["run_id"],
                    "severity": row["severity"],
                    "seed": row["seed"],
                    "role": row["role"],
                    "suite": suite,
                }
                record.update({f"f{i}": value for i, value in enumerate(vector)})
                writer.writerow(record)


def write_report(path: Path, summary: dict[str, Any]) -> None:
    """Write the deterministic screen report.

    Every figure is recomputed from `summary`, so the report regenerates byte-for-byte
    from the committed `summary.json`.

    Args:
        path: Report destination.
        summary: The complete run summary.
    """

    sensitivity = summary["action_sensitivity_map"]
    c1_eval = summary["suite_evaluations"]["C1"]
    s_eval = summary["suite_evaluations"]["S"]
    comparison = summary["commanded_action_comparison"]
    base_cap = summary["screen_spec"]["recovery_config"]["maximum_gain_compensation"]
    base_row = next(
        row
        for row in comparison["caps"]
        if np.isclose(row["maximum_gain_compensation"], base_cap)
    )
    interval_low = sensitivity["by_cap"][f"{base_cap:.1f}"]["sensitive_interval_low"]

    lines: list[str] = []
    lines.append("# Severity-estimation quality versus action severity-sensitivity")
    lines.append("")
    lines.append(
        "Development-sized screen. Measures how well each deployable suite estimates "
        "remaining actuator gain, and whether any measured difference between the suites "
        "can change the command the recovery controller actually applies."
    )
    lines.append("")
    lines.append(f"- Severity grid (remaining gain): {list(summary['screen_spec']['severity_grid'])}")
    lines.append(
        f"- Tuning seeds {list(summary['screen_spec']['tuning_seeds'])}; disjoint "
        f"assessment seeds {list(summary['screen_spec']['assessment_seeds'])}"
    )
    lines.append(
        f"- {summary['n_arms']} no-action arms, one S observation each, physically "
        "projected to C1 so the suites are exactly paired"
    )
    lines.append(f"- Config hash `{summary['screen_spec']['config_hash']}` (not frozen)")
    lines.append("")

    lines.append("## Part A — where a severity difference can change the action at all")
    lines.append("")
    lines.append(
        f"The controller's actuator multiplier is "
        f"`min(1 / max(severity, {sensitivity['minimum_gain_remaining']:g}), cap)`. It is "
        f"flat for every estimate at or below `1 / cap`, so at the recorded cap of "
        f"{base_cap:g} any two estimates that both stay in `(0, {interval_low:g}]` command "
        "**identically**. A true fault exactly at the boundary still has to be measured: "
        "an estimate just above the kink commands less. A severity advantage is reachable "
        "where the true setting is inside the sensitive interval **or at that one-sided "
        "boundary**, and its exact-restoration ceiling clears the "
        f"{sensitivity['bar_pct']:.1f}% bar."
    )
    lines.append("")
    lines.append(
        "| cap | sensitive severities | reachable severities (sensitive/boundary *and* ceiling ≥ bar) |"
    )
    lines.append("|---:|---|---|")
    for cap_key, entry in sensitivity["by_cap"].items():
        reachable = (
            ", ".join(f"{value:.2f}" for value in entry["reachable_severities"])
            if entry["reachable_severities"]
            else "none"
        )
        lines.append(
            f"| {float(cap_key):.1f} | `({entry['sensitive_interval_low']:.3f}, 1.000)` | "
            f"{reachable} |"
        )
    lines.append("")
    smallest = sensitivity["smallest_cap_with_a_reachable_severity"]
    if smallest is None:
        lines.append(
            "- **No cap in the sweep opens a reachable severity.** On this grid, severity "
            "precision cannot reach the contract through this action family."
        )
    else:
        lines.append(
            f"- **The smallest cap with any reachable severity is {smallest:g}.** At the "
            f"recorded cap of {base_cap:g} the reachable set is "
            f"{sensitivity['by_cap'][f'{base_cap:.1f}']['reachable_severities'] or 'empty'}: "
            "no setting in the open sensitive interval clears the bar; any reachable "
            "boundary setting must therefore be tested directly because estimator noise "
            "can straddle the kink. Raising the cap moves the boundary and changes this "
            "reachability map, which is why cap/floor sensitivity and severity quality "
            "have to be reviewed together."
        )
    lines.append("")
    lines.append("| severity | no-action deficit | exact-restoration ceiling | multiplier at cap "
                 f"{base_cap:g} | sensitive interior | at cap boundary | ceiling ≥ bar |")
    lines.append("|---:|---:|---:|---:|:--:|:--:|:--:|")
    for row in sensitivity["rows"]:
        if not np.isclose(row["maximum_gain_compensation"], base_cap):
            continue
        lines.append(
            f"| {row['severity']:.2f} | {row['no_action_deficit_pct']:+.2f}% | "
            f"{row['exact_restoration_ceiling_pct']:+.2f}% | "
            f"{row['multiplier_at_true_severity']:.3f} | "
            f"{'yes' if row['severity_sensitive'] else 'no'} | "
            f"{'yes' if row['severity_at_sensitivity_boundary'] else 'no'} | "
            f"{'yes' if row['ceiling_clears_bar'] else 'no'} |"
        )
    lines.append("")

    lines.append("## Part B — measured severity-estimation accuracy, C1 versus S")
    lines.append("")
    lines.append("| suite | active features | ridge penalty | held-out MAE | RMSE | max abs error | bias |")
    lines.append("|---|---:|---:|---:|---:|---:|---:|")
    for record in (c1_eval, s_eval):
        lines.append(
            f"| {record['suite']} | {record['active_feature_count']} / "
            f"{record['feature_width']} | {record['selected_regularization']:g} | "
            f"{record['holdout_mae']:.4f} | {record['holdout_rmse']:.4f} | "
            f"{record['holdout_max_abs_error']:.4f} | {record['holdout_bias']:+.4f} |"
        )
    lines.append("")
    delta = s_eval["holdout_mae"] - c1_eval["holdout_mae"]
    comparison_word = "higher" if delta > 0.0 else "lower"
    lines.append(
        f"- The gauge role contributes "
        f"{s_eval['active_feature_count'] - c1_eval['active_feature_count']} additional "
        f"active feature columns to S. S's held-out mean absolute severity error is "
        f"{abs(delta):.4f} {comparison_word} than C1's "
        f"({s_eval['holdout_mae']:.4f} versus {c1_eval['holdout_mae']:.4f})."
    )
    lines.append("")
    lines.append("| severity | C1 mean estimate | C1 MAE | S mean estimate | S MAE |")
    lines.append("|---:|---:|---:|---:|---:|")
    for c1_row, s_row in zip(c1_eval["per_severity"], s_eval["per_severity"]):
        lines.append(
            f"| {c1_row['severity']:.2f} | {c1_row['mean_estimate']:.3f} | "
            f"{c1_row['mean_abs_error']:.4f} | {s_row['mean_estimate']:.3f} | "
            f"{s_row['mean_abs_error']:.4f} |"
        )
    lines.append("")

    lines.append("## Parts A and B together — does a deployable read-out command like an oracle?")
    lines.append("")
    lines.append(
        "On a fault whose true severity already sits in the flat region, the oracle's own "
        "multiplier is the cap. Any estimate that also lands there therefore reproduces "
        "the oracle's command exactly, however wrong the number is — so a severity "
        "read-out on those settings is a threshold test, not a regression problem."
    )
    lines.append("")
    lines.append(
        "| suite | cap | capped arms | oracle-identical | boundary arms | "
        "oracle-identical | sensitive arms | oracle-identical | healthy arms | "
        "oracle-identical | max multiplier error |"
    )
    lines.append("|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|")

    def _rate(value: float | None) -> str:
        """Render an agreement rate, or `n/a` when its regime has no arms."""

        return "n/a" if value is None else f"{100.0 * value:.1f}%"

    for suite in ("C1", "S"):
        for row in summary["oracle_action_agreement"][suite]["caps"]:
            lines.append(
                f"| {suite} | {row['maximum_gain_compensation']:.1f} | "
                f"{row['capped_region_arms']} | "
                f"{_rate(row['capped_region_oracle_identical_rate'])} | "
                f"{row['boundary_region_arms']} | "
                f"{_rate(row['boundary_region_oracle_identical_rate'])} | "
                f"{row['sensitive_region_arms']} | "
                f"{_rate(row['sensitive_region_oracle_identical_rate'])} | "
                f"{row['identity_region_arms']} | "
                f"{_rate(row['identity_region_oracle_identical_rate'])} | "
                f"{row['max_abs_multiplier_error']:.4f} |"
            )
    lines.append("")
    lines.append(
        "`oracle-identical` is exact multiplier equality. Four regimes are separated "
        "because they ask different questions. In the **capped** regime the cap binds and "
        "any estimate below the threshold reproduces the oracle exactly, so the rate is "
        "the one that matters. At the **boundary**, estimator noise can straddle the kink "
        "even though the oracle itself is capped. In the **sensitive** regime exact equality requires an "
        "exactly correct number and is near zero by construction, so the graded maximum "
        "multiplier error is the quantity to read. The **healthy** arms are the grid's "
        "top anchor, where the oracle applies no action at all: a non-zero rate there is "
        "a false-authorization question, not a severity-precision one. The informative "
        "contrast is across regimes: a read-out that is useless as a regression can still "
        "be exact as an action."
    )
    lines.append("")

    lines.append("### Would the two suites ever command differently?")
    lines.append("")
    lines.append(
        "| cap | pairs | multipliers differ | mean abs difference | max abs difference | "
        "capped-region pairs | of those, differ | boundary pairs | of those, differ |"
    )
    lines.append("|---:|---:|---:|---:|---:|---:|---:|---:|---:|")
    for row in comparison["caps"]:
        lines.append(
            f"| {row['maximum_gain_compensation']:.1f} | {row['n_pairs']} | "
            f"{row['n_multipliers_differ']} ({100.0 * row['fraction_differ']:.1f}%) | "
            f"{row['mean_abs_multiplier_difference']:.4f} | "
            f"{row['max_abs_multiplier_difference']:.4f} | "
            f"{row['capped_region_pairs']} | "
            f"{row['capped_region_multipliers_differ']} | "
            f"{row['boundary_region_pairs']} | "
            f"{row['boundary_region_multipliers_differ']} |"
        )
    lines.append("")
    if base_row["n_multipliers_differ"] == 0:
        lines.append(
            f"- **At the recorded cap of {base_cap:g}, the two suites command identically on "
            f"every one of the {base_row['n_pairs']} held-out arms.** Whatever severity "
            "information the gauge channels carry, this action family cannot spend it."
        )
    else:
        lines.append(
            f"- **At the recorded cap of {base_cap:g}, the suites command differently on "
            f"{base_row['n_multipliers_differ']} of {base_row['n_pairs']} held-out arms**, "
            f"but by a mean absolute multiplier difference of only "
            f"{base_row['mean_abs_multiplier_difference']:.4f} "
            f"(worst {base_row['max_abs_multiplier_difference']:.4f})."
        )
    reachable_boundaries = [
        row["severity"]
        for row in sensitivity["rows"]
        if np.isclose(row["maximum_gain_compensation"], base_cap)
        and row["severity_at_sensitivity_boundary"]
        and row["ceiling_clears_bar"]
    ]
    if reachable_boundaries and base_row["boundary_region_multipliers_differ"] > 0:
        lines.append(
            f"- **The severity route remains live at the cap boundary.** The recorded "
            f"deficit screen places {reachable_boundaries} remaining gain exactly at the "
            f"one-sided boundary with enough restoration headroom to clear the bar, and "
            f"the suites command differently on "
            f"{base_row['boundary_region_multipliers_differ']} of "
            f"{base_row['boundary_region_pairs']} held-out boundary arms (worst multiplier "
            f"difference {base_row['boundary_region_max_abs_difference']:.4f}). The "
            "paired control effect must therefore be measured; it is not structurally zero."
        )
    elif base_row["capped_region_multipliers_differ"] == 0 and (
        not reachable_boundaries or base_row["boundary_region_multipliers_differ"] == 0
    ):
        lines.append(
            f"- No multiplier difference appears in the strictly capped interior or at a "
            "recorded above-bar boundary. Within the evaluated grid, the severity read-out "
            "therefore does not create a paired control route at this cap."
        )
    else:
        lines.append(
            f"- **{base_row['capped_region_multipliers_differ']} of "
            f"{base_row['capped_region_pairs']} capped-region arms do differ between the "
            f"suites** (worst {base_row['capped_region_max_abs_difference']:.4f}). Those "
            "show that the paired S-minus-C1 control difference is not structurally zero; "
            "an action screen must measure it rather than assume it."
        )
    lines.append("")

    lines.append("## What this screen does and does not establish")
    lines.append("")
    lines.append(
        "- **It is a bound on a linear read-out, not on the severity channel.** A learned "
        "head could raise both suites' accuracy. A null S-over-C1 difference here means "
        "the gauge channels carry no severity information a matched linear read-out can "
        "recover at this data size, not that they carry none."
    )
    lines.append(
        "- **The action comparison is stronger than the accuracy comparison.** The "
        "multiplier is flat over most of the severity range, so the commanded-action "
        "result survives read-out quality changes that the MAE comparison would not: any "
        "estimator landing in the same flat region commands the same thing."
    )
    lines.append(
        "- **The class-probability channel is deliberately held fixed, and is untested.** "
        "The controller's multiplier is `1 + p · (capped - 1)`, so two suites that call "
        "the same class with different calibrated confidence command differently even at "
        "an identical severity. This screen pins `p = 1` for both suites in order to "
        "isolate the severity channel. A suite difference in class probability is a "
        "separate route to a non-zero paired control difference, it is not measured by "
        "any artifact in this packet, and the one-hot prototype probabilities the "
        "information review recorded are explicitly not calibrated probabilities."
    )
    lines.append(
        f"- **Development-sized.** {c1_eval['n_train']} fit windows and "
        f"{c1_eval['n_test']} held-out windows, held out over sensor seed only, on one "
        "bounded task/contact condition and one fault location. Not validation-sized, "
        "not frozen-config, and not evidence about the structural or sensor classes."
    )
    lines.append(
        "- **Severity uncertainty is not yet calibrated.** The head reports a training "
        f"residual dispersion (C1 {c1_eval['train_residual_std']:.4f}, S "
        f"{s_eval['train_residual_std']:.4f}), which is an in-sample number. The recovery "
        "controller's confidence gate gates on severity uncertainty, so a deployable "
        "severity arm needs a held-out uncertainty before it can be wired to the action."
    )
    lines.append("")

    lines.append("## Audit")
    lines.append("")
    audit = summary["audit"]
    lines.append(
        f"- Exactly one classification evaluation per arm: {audit['single_evaluation']}"
    )
    lines.append(f"- Zero recovery-command changes on every arm: {audit['no_recovery_action']}")
    lines.append(f"- Zero A1 incident steps: {audit['zero_a1_incidents']}")
    lines.append(f"- Zero saturation steps: {audit['zero_saturation']}")
    lines.append(
        f"- Suite projection verified against a real C1 session on "
        f"{audit['projection_check']['n_arms']} arms; max absolute feature difference "
        f"{audit['projection_check']['max_abs_feature_difference']:.3e}, max absolute "
        f"`J_5s` difference {audit['projection_check']['max_abs_j5s_difference']:.3e}"
    )
    lines.append(
        f"- Tuning and assessment seed sets are disjoint: {audit['seeds_disjoint']}"
    )
    lines.append("")
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text("\n".join(lines) + "\n", encoding="utf-8")


def load_recorded_deficits(path: Path) -> dict[float, float]:
    """Read the actuator per-severity no-action deficits from the deficit screen's CSV.

    Uses the disjoint assessment rows, which are the ones the deficit screen reports.

    Args:
        path: Path to `candidate_summary.csv` from the fault tracking-deficit screen.

    Returns:
        Remaining-gain keyed mean no-action deficit percent.

    Raises:
        FileNotFoundError: If the recorded screen output is missing.
        ValueError: If no actuator assessment rows are present.
    """

    if not path.is_file():
        raise FileNotFoundError(
            f"recorded deficit summary not found at {path}; run "
            "scripts/screen_fault_tracking_deficit.py first"
        )
    deficits: dict[float, float] = {}
    with path.open(newline="", encoding="utf-8") as handle:
        for row in csv.DictReader(handle):
            if row["role"] != "assessment" or row["source_class"] != "actuator":
                continue
            deficits[float(row["severity"])] = float(row["mean_tracking_deficit_pct"])
    if not deficits:
        raise ValueError(f"no actuator assessment rows found in {path}")
    return deficits


def main() -> int:
    """Run the screen end to end and write its three artifacts."""

    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--deficit-summary",
        type=Path,
        default=Path("results/fault_tracking_deficit_screen/candidate_summary.csv"),
        help="recorded per-class deficit summary that Part A crosses against",
    )
    parser.add_argument(
        "--output-dir",
        type=Path,
        default=Path("results/severity_estimation_quality"),
        help="directory the three artifacts are written to",
    )
    parser.add_argument("--workers", type=int, default=8)
    parser.add_argument(
        "--projection-check-arms",
        type=int,
        default=3,
        help="arms re-run with a real C1 session to verify the S-to-C1 projection",
    )
    args = parser.parse_args()
    if args.workers < 1:
        raise ValueError("--workers must be at least 1")
    if args.projection_check_arms < 0:
        raise ValueError("--projection-check-arms must be non-negative")

    deficits = load_recorded_deficits(args.deficit_summary)
    print(
        f"Loaded recorded actuator deficits for severities "
        f"{sorted(deficits, reverse=True)}",
        flush=True,
    )

    specs = [
        ArmSpec(severity=severity, seed=seed, role=role)
        for severity in SEVERITY_GRID
        for role, seeds in (("tuning", TUNING_SEEDS), ("assessment", ASSESSMENT_SEEDS))
        for seed in seeds
    ]
    # Spread the projection checks across the severity grid rather than taking the first
    # arms, so the S-to-C1 equivalence is verified on faulted plants and not only on the
    # healthy anchor at the top of the grid.
    check_stride = max(1, len(specs) // max(1, args.projection_check_arms))
    check_specs = [
        ArmSpec(severity=spec.severity, seed=spec.seed, role=spec.role, suite="C1")
        for spec in specs[::check_stride][: args.projection_check_arms]
    ]
    print(
        f"Running {len(specs)} arms (+{len(check_specs)} projection checks) on "
        f"{args.workers} workers ...",
        flush=True,
    )
    with concurrent.futures.ProcessPoolExecutor(max_workers=args.workers) as pool:
        rows = list(pool.map(run_arm, specs + check_specs))
    main_rows = rows[: len(specs)]
    check_rows = rows[len(specs) :]
    print(f"Completed {len(main_rows)} arms.", flush=True)

    max_feature_difference = 0.0
    max_j5s_difference = 0.0
    for check in check_rows:
        match = next(
            row
            for row in main_rows
            if row["seed"] == check["seed"]
            and np.isclose(row["severity"], check["severity"])
        )
        max_feature_difference = max(
            max_feature_difference,
            float(
                np.max(
                    np.abs(
                        np.asarray(match["features"]["C1"])
                        - np.asarray(check["features"]["C1"])
                    )
                )
            ),
        )
        max_j5s_difference = max(
            max_j5s_difference, abs(match["j_5s"] - check["j_5s"])
        )

    tuning_rows = [row for row in main_rows if row["role"] == "tuning"]
    assessment_rows = [row for row in main_rows if row["role"] == "assessment"]
    order = sorted(
        range(len(assessment_rows)),
        key=lambda i: (-assessment_rows[i]["severity"], assessment_rows[i]["seed"]),
    )
    assessment_rows = [assessment_rows[i] for i in order]

    evaluations = {
        suite: evaluate_suite(tuning_rows, assessment_rows, suite, REGULARIZATION_GRID)
        for suite in ("C1", "S")
    }
    for suite, record in evaluations.items():
        print(
            f"{suite}: held-out severity MAE {record['holdout_mae']:.4f} "
            f"({record['active_feature_count']} active features, penalty "
            f"{record['selected_regularization']:g})",
            flush=True,
        )

    config = RecoveryControlConfig()
    summary: dict[str, Any] = {
        "screen_spec": {
            "severity_grid": list(SEVERITY_GRID),
            "tuning_seeds": list(TUNING_SEEDS),
            "assessment_seeds": list(ASSESSMENT_SEEDS),
            "regularization_grid": list(REGULARIZATION_GRID),
            "plane_z_m": PLANE_Z_M,
            "fault_location": FAULT_LOCATION,
            "claim_tracking_bar_pct": CLAIM_TRACKING_BAR_PCT,
            "config_hash": CONFIG_HASH,
            "recovery_config": {
                key: list(value) if isinstance(value, tuple) else value
                for key, value in asdict(config).items()
            },
            "recorded_deficit_source": str(args.deficit_summary).replace("\\", "/"),
        },
        "n_arms": len(main_rows),
        "recorded_actuator_deficits_pct": {
            f"{severity:.2f}": value for severity, value in sorted(deficits.items())
        },
        "action_sensitivity_map": action_sensitivity_map(deficits),
        "suite_evaluations": evaluations,
        "commanded_action_comparison": compare_commanded_actions(
            evaluations["C1"], evaluations["S"]
        ),
        "oracle_action_agreement": {
            suite: compare_against_oracle_action(record)
            for suite, record in evaluations.items()
        },
        "audit": {
            "single_evaluation": all(
                row["classification_evaluations"] == 1 for row in main_rows
            ),
            "no_recovery_action": all(
                row["recovery_command_changes"] == 0 for row in main_rows
            ),
            "zero_a1_incidents": all(row["a1_incident_steps"] == 0 for row in main_rows),
            "zero_saturation": all(row["saturation_steps"] == 0 for row in main_rows),
            "seeds_disjoint": not (set(TUNING_SEEDS) & set(ASSESSMENT_SEEDS)),
            "projection_check": {
                "n_arms": len(check_rows),
                "max_abs_feature_difference": max_feature_difference,
                "max_abs_j5s_difference": max_j5s_difference,
            },
        },
    }

    args.output_dir.mkdir(parents=True, exist_ok=True)
    _write_csv(args.output_dir / "arm_rows.csv", main_rows)
    _write_features_csv(args.output_dir / "window_features.csv", main_rows)
    (args.output_dir / "summary.json").write_text(
        json.dumps(summary, indent=2, sort_keys=True, allow_nan=False) + "\n",
        encoding="utf-8",
    )
    write_report(args.output_dir / "severity_estimation_quality_report.md", summary)
    print(f"Wrote four artifacts to {args.output_dir}", flush=True)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
