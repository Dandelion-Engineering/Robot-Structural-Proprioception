"""End-to-end diagnosis->control seam regression (interface/mechanism test only).

This is the committed regression Claude proposed (S13) and Codex green-lit (S13): it
pins the *control semantics* of the diagnosis->control seam over multiple real
``CablePlant`` steps through ``run_online_rollout``, which the existing tests exercise
only piecewise (a single ``plant.advance`` in ``test_recovery_control`` and a single
``policy(...)`` call in the recovery-controller/residual seam smokes). Concretely it
holds the socket contract that a *localizing* attribution stand-in sustains active
inverse-gain compensation — restoring delivered torque at the attributed joint across a
whole rollout — while a *detection-only / unlocalized* stand-in on the same fault stays
exactly nominal and therefore does not restore delivery.

Scope discipline (per the S13 agreement): the stand-ins are fixed deployable outputs,
NOT a trained head, and the assertions are on applied/delivered *torque* through the
seam. This is an interface/mechanism regression, not a ``J_5s`` tracking-recovery or a
safety result — those are scored only by the frozen evaluation driver over the declared
post-change window. The learned attribution head, the RMA latent, and the oracle will
later drive this same ``EstimatorCommandPolicy`` socket, so fixing its control semantics
now means the trained head lands into a seam whose behavior is already pinned.
"""

from __future__ import annotations

import sys
from pathlib import Path

import numpy as np
import pytest

SCRIPTS_DIR = Path(__file__).resolve().parents[1] / "scripts"
sys.path.insert(0, str(SCRIPTS_DIR))

from utils.cable_mechanics import commanded_torque  # noqa: E402
from utils.cable_plant import CablePlant  # noqa: E402
from utils.estimator import (  # noqa: E402
    DiagnosisEstimator,
    EstimatorCommandPolicy,
    EstimatorOutput,
    HEALTHY_INDEX,
    N_SOURCE_CLASSES,
    SOURCE_CLASS_ORDER,
)
from utils.online_loop import run_online_rollout  # noqa: E402
from utils.recovery_control import GainScheduledRecoveryController  # noqa: E402
from utils.schema_types import FaultSpec  # noqa: E402
from utils.sensor_model import OnlineSensorSession  # noqa: E402

NOMINAL_SCALE = 0.5
ACTUATOR_INDEX = SOURCE_CLASS_ORDER.index("actuator")
STRUCTURE_INDEX = SOURCE_CLASS_ORDER.index("structure")


class FixedDiagnosisStandIn(DiagnosisEstimator):
    """Emit one fixed deployable ``EstimatorOutput`` at every decision step.

    A deterministic stand-in for a steady post-detection diagnosis; it ignores the
    window content (so it is deliberately not a real estimator) but preserves the causal
    step/time coordinates and latches ``detection_time_s`` at the first decision, which
    is all the seam needs to route the fixed attribution through the recovery controller.
    """

    def __init__(self, template: EstimatorOutput) -> None:
        """Retain a validated output template to reissue at each step."""

        template.validate()
        self._template = template
        self._detection_time_s = float("nan")

    def reset(self) -> None:
        """Reset the first-detection latch for a fresh rollout."""

        self._detection_time_s = float("nan")

    def update(
        self, step_index: int, decision_time_s: float, _window
    ) -> EstimatorOutput:
        """Return the fixed attribution at the current decision coordinates."""

        if not np.isfinite(self._detection_time_s):
            self._detection_time_s = decision_time_s
        return EstimatorOutput(
            step=step_index,
            decision_time_s=decision_time_s,
            p_class=self._template.p_class.copy(),
            unknown_score=self._template.unknown_score,
            abstain_decision=self._template.abstain_decision,
            location_out=self._template.location_out,
            severity_out=self._template.severity_out,
            severity_uncertainty=self._template.severity_uncertainty,
            detection_time_s=self._detection_time_s,
        )


def _output(
    source: str,
    *,
    location: int,
    severity: float,
    uncertainty: float,
    confidence: float = 1.0,
) -> EstimatorOutput:
    """Build one contract-valid fixed diagnosis with the given source confidence."""

    probabilities = np.full(N_SOURCE_CLASSES, 0.0)
    probabilities[SOURCE_CLASS_ORDER.index(source)] = confidence
    probabilities[HEALTHY_INDEX] += 1.0 - confidence
    return EstimatorOutput(
        step=0,
        decision_time_s=0.0,
        p_class=probabilities,
        unknown_score=0.0,
        abstain_decision=False,
        location_out=location,
        severity_out=severity,
        severity_uncertainty=uncertainty,
        detection_time_s=0.0,
    )


def _run_seam(template: EstimatorOutput, *, fault: FaultSpec | None, n_steps: int = 8):
    """Drive a fixed stand-in through the real plant/sensor/controller seam.

    Returns the ``(result, policy, nominal_series)`` triple, where ``nominal_series`` is
    the per-step nominal task command evaluated at the exact decision times the policy
    used, so applied/delivered torque can be compared without assuming the plant clock.
    """

    plant = CablePlant(fault=fault) if fault is not None else CablePlant()
    policy = EstimatorCommandPolicy(
        FixedDiagnosisStandIn(template),
        suite="S",
        run_id="recovery-seam",
        stride=1,
        recovery_command=GainScheduledRecoveryController(),
    )
    result = run_online_rollout(
        plant,
        OnlineSensorSession(
            "S",
            pair_id="recovery-seam",
            sensor_seed=11,
            control_dt_s=plant.config.control_dt_s,
        ),
        n_steps=n_steps,
        history_steps=80,
        command_policy=policy,
    )
    times = [out.decision_time_s for out in policy.trace.outputs]
    nominal_series = np.stack([commanded_torque(t, scale=NOMINAL_SCALE) for t in times])
    return result, policy, nominal_series


def _actuator_fault() -> FaultSpec:
    """A 50%-remaining actuator-gain loss at joint 1, active from the first step."""

    return FaultSpec(
        source_class="actuator",
        subtype="actuator_gain_loss",
        location=1,
        severity=0.5,
        onset_index=0,
    )


def test_localizing_attribution_sustains_active_compensation_over_rollout() -> None:
    """A confident localized actuator attribution restores delivered torque every step."""

    template = _output("actuator", location=1, severity=0.5, uncertainty=0.0)
    result, policy, nominal = _run_seam(template, fault=_actuator_fault())

    assert len(policy.trace) == 8
    assert result.observations.n_steps == 8
    assert all(output.detection_time_s == 0.0 for output in policy.trace.outputs)
    # Joint 1 is driven at 2x nominal (1/0.5 inverse gain); joint 0 stays nominal.
    np.testing.assert_allclose(result.plant.tau_cmd[:, 1], 2.0 * nominal[:, 1], atol=1e-9)
    np.testing.assert_allclose(result.plant.tau_cmd[:, 0], nominal[:, 0], atol=1e-9)
    # The plant's downstream 0.5 gain loss then cancels the compensation: delivery is
    # restored to nominal at the attributed joint, sustained across the whole rollout.
    np.testing.assert_allclose(
        result.plant.tau_delivered_true[:, 1], nominal[:, 1], atol=1e-9
    )
    assert not result.plant.saturation_flag.any()


def test_detection_only_unlocalized_arm_stays_nominal_and_leaves_delivery_degraded() -> None:
    """Confident detection without localization/severity cannot trigger compensation.

    The only thing withheld here versus the active arm is the fault location and a finite
    severity (uncertainty is infinite): the controller's ``np.isfinite(severity_uncertainty)``
    gate therefore blocks the actuator action, so the command stays exactly nominal and
    the plant keeps delivering the degraded 0.5x torque. A real detection rung additionally
    spreads its fault mass and/or abstains on type, so it is blocked a fortiori.
    """

    template = _output(
        "actuator", location=-1, severity=0.0, uncertainty=float("inf"), confidence=0.9
    )
    result, _policy, nominal = _run_seam(template, fault=_actuator_fault())

    np.testing.assert_allclose(result.plant.tau_cmd, nominal, atol=1e-9)
    # Delivery stays degraded (0.5x) because nothing compensated the attributed loss.
    np.testing.assert_allclose(
        result.plant.tau_delivered_true[:, 1], 0.5 * nominal[:, 1], atol=1e-9
    )


def test_active_and_detection_only_arms_diverge_at_the_seam() -> None:
    """The seam's headline property: attribution restores delivery, detection does not."""

    fault = _actuator_fault()
    active, _, nominal = _run_seam(
        _output("actuator", location=1, severity=0.5, uncertainty=0.0), fault=fault
    )
    detect, _, _ = _run_seam(
        _output("actuator", location=-1, severity=0.0, uncertainty=float("inf"),
                confidence=0.9),
        fault=fault,
    )
    # Applied commands diverge at the attributed joint...
    assert np.all(active.plant.tau_cmd[:, 1] > detect.plant.tau_cmd[:, 1] + 1e-6)
    # ...and only the localizing arm restores delivered torque toward nominal.
    active_gap = np.abs(active.plant.tau_delivered_true[:, 1] - nominal[:, 1]).max()
    detect_gap = np.abs(detect.plant.tau_delivered_true[:, 1] - nominal[:, 1]).max()
    assert active_gap < 1e-9 < detect_gap


def test_structural_attribution_applies_sustained_global_derate_over_rollout() -> None:
    """A confident structural diagnosis applies the safe 0.75 global derate every step.

    Driven on a healthy plant so the mechanism (not a fault interaction) is isolated: the
    structural action needs no location, so this pins that the bounded global derate is
    applied end-to-end across the rollout rather than only in the controller unit test.
    """

    template = _output("structure", location=-1, severity=0.5, uncertainty=0.0)
    result, _policy, nominal = _run_seam(template, fault=None)

    np.testing.assert_allclose(result.plant.tau_cmd, 0.75 * nominal, atol=1e-9)
    assert not result.plant.saturation_flag.any()
