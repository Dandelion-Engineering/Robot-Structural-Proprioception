"""Tests for the interpretable gain-scheduled recovery-controller floor."""

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
    N_SOURCE_CLASSES,
    SOURCE_CLASS_ORDER,
)
from utils.recovery_control import (  # noqa: E402
    GainScheduledRecoveryController,
    RecoveryControlConfig,
)
from utils.schema_types import FaultSpec  # noqa: E402


def diagnosis(
    source: str,
    *,
    location: int = -1,
    severity: float = 0.0,
    uncertainty: float = 0.0,
    abstain: bool = False,
) -> EstimatorOutput:
    """Build one contract-valid deterministic diagnosis for controller tests."""

    probabilities = np.zeros(N_SOURCE_CLASSES)
    probabilities[SOURCE_CLASS_ORDER.index(source)] = 1.0
    return EstimatorOutput(
        step=0,
        decision_time_s=0.0,
        p_class=probabilities,
        unknown_score=0.0,
        abstain_decision=abstain,
        location_out=location,
        severity_out=severity,
        severity_uncertainty=uncertainty,
        detection_time_s=0.0 if source != "healthy" else float("nan"),
    )


def test_healthy_and_abstained_diagnoses_preserve_nominal_command() -> None:
    """No active recovery occurs without a confident type-specific diagnosis."""

    controller = GainScheduledRecoveryController()
    time_s = 0.137
    nominal = commanded_torque(time_s, scale=controller.config.nominal_task_scale)
    np.testing.assert_allclose(controller(diagnosis("healthy"), 0, time_s), nominal)
    np.testing.assert_allclose(
        controller(
            diagnosis(
                "actuator", location=1, severity=0.5, abstain=True
            ),
            0,
            time_s,
        ),
        nominal,
    )


def test_one_hot_actuator_diagnosis_inverse_schedules_the_affected_joint() -> None:
    """A 50%-remaining attributed actuator receives 2x requested nominal torque."""

    controller = GainScheduledRecoveryController()
    time_s = 0.137
    nominal = commanded_torque(time_s, scale=controller.config.nominal_task_scale)
    recovered = controller(
        diagnosis("actuator", location=1, severity=0.5), 0, time_s
    )
    assert recovered[0] == pytest.approx(nominal[0])
    assert recovered[1] == pytest.approx(2.0 * nominal[1])
    # The plant's downstream 0.5 gain then restores the nominal delivered command.
    assert 0.5 * recovered[1] == pytest.approx(nominal[1])


def test_actuator_compensation_restores_nominal_delivery_on_real_plant() -> None:
    """The recovery callback cancels the plant's downstream attributed gain loss."""

    controller = GainScheduledRecoveryController()
    command = controller(
        diagnosis("actuator", location=1, severity=0.5), 0, 0.0
    )
    plant = CablePlant(
        fault=FaultSpec(
            source_class="actuator",
            subtype="actuator_gain_loss",
            location=1,
            severity=0.5,
            onset_index=0,
        )
    )
    state = plant.advance(command)
    nominal = commanded_torque(0.0, scale=controller.config.nominal_task_scale)
    np.testing.assert_allclose(state.tau_delivered_true, nominal)
    assert not state.saturation_flag.any()


def test_structural_diagnosis_derates_without_claiming_repair() -> None:
    """A confident structural result applies only the explicit safe global derate."""

    controller = GainScheduledRecoveryController()
    time_s = 0.137
    nominal = commanded_torque(time_s, scale=controller.config.nominal_task_scale)
    recovered = controller(
        diagnosis("structure", location=1, severity=0.5), 0, time_s
    )
    np.testing.assert_allclose(
        recovered, nominal * controller.config.structural_command_derate
    )


@pytest.mark.parametrize(
    ("scope", "expected"),
    [
        ("global", np.array([0.12, -0.06])),
        ("localized", np.array([0.08, -0.06])),
    ],
)
def test_structural_inverse_stiffness_action_is_bounded_and_scope_explicit(
    scope: str, expected: np.ndarray
) -> None:
    """A one-hot 50%-remaining diagnosis applies the declared capped multiplier."""

    controller = GainScheduledRecoveryController(
        RecoveryControlConfig(
            structural_action="inverse_stiffness",
            structural_compensation_scope=scope,
            maximum_structural_compensation=1.5,
        )
    )
    nominal = np.array([0.08, -0.04])
    recovered = controller.command_from_nominal(
        diagnosis("structure", location=1, severity=0.5), nominal
    )
    np.testing.assert_allclose(recovered, expected)
    np.testing.assert_allclose(nominal, np.array([0.08, -0.04]))


def test_structural_compensation_requires_location_and_remaining_stiffness() -> None:
    """Tracking compensation fails safe when its physical estimate is unusable."""

    controller = GainScheduledRecoveryController(
        RecoveryControlConfig(structural_action="inverse_stiffness")
    )
    nominal = np.array([0.08, -0.04])
    for output in (
        diagnosis("structure", location=-1, severity=0.5),
        diagnosis("structure", location=1, severity=0.0),
        diagnosis("structure", location=1, severity=1.2),
    ):
        np.testing.assert_allclose(
            controller.command_from_nominal(output, nominal), nominal
        )


def test_recovery_can_condition_an_external_deployable_nominal_command() -> None:
    """Observation-feedback task commands use the same diagnosis gates and actions."""

    controller = GainScheduledRecoveryController()
    nominal = np.array([0.08, -0.04])
    recovered = controller.command_from_nominal(
        diagnosis("actuator", location=1, severity=0.5), nominal
    )
    np.testing.assert_allclose(recovered, np.array([0.08, -0.08]))
    # The caller-owned nominal vector must not be modified in place.
    np.testing.assert_allclose(nominal, np.array([0.08, -0.04]))


def test_external_nominal_command_rejects_privileged_or_malformed_shapes() -> None:
    """The composition seam accepts exactly one finite two-joint command."""

    controller = GainScheduledRecoveryController()
    with pytest.raises(ValueError, match="nominal_command"):
        controller.command_from_nominal(diagnosis("healthy"), np.zeros(3))
    with pytest.raises(ValueError, match="nominal_command"):
        controller.command_from_nominal(
            diagnosis("healthy"), np.array([0.0, np.nan])
        )


def test_unlocalized_or_uncertain_actuator_diagnosis_falls_back_to_nominal() -> None:
    """Active compensation is withheld if location or severity confidence is absent."""

    controller = GainScheduledRecoveryController()
    time_s = 0.137
    nominal = commanded_torque(time_s, scale=controller.config.nominal_task_scale)
    unlocalized = diagnosis("actuator", location=-1, severity=0.5)
    uncertain = diagnosis("actuator", location=1, severity=0.5, uncertainty=float("inf"))
    np.testing.assert_allclose(controller(unlocalized, 0, time_s), nominal)
    np.testing.assert_allclose(controller(uncertain, 0, time_s), nominal)


def test_tied_source_probabilities_do_not_trigger_multiple_recovery_actions() -> None:
    """An ambiguous non-abstained tie still fails safe instead of blending two actions."""

    controller = GainScheduledRecoveryController()
    time_s = 0.137
    nominal = commanded_torque(time_s, scale=controller.config.nominal_task_scale)
    probabilities = np.zeros(N_SOURCE_CLASSES)
    probabilities[SOURCE_CLASS_ORDER.index("structure")] = 0.5
    probabilities[SOURCE_CLASS_ORDER.index("actuator")] = 0.5
    ambiguous = EstimatorOutput(
        step=0,
        decision_time_s=time_s,
        p_class=probabilities,
        unknown_score=0.0,
        abstain_decision=False,
        location_out=1,
        severity_out=0.5,
        severity_uncertainty=0.0,
        detection_time_s=time_s,
    )
    np.testing.assert_allclose(controller(ambiguous, 0, time_s), nominal)


def test_recovery_controller_plugs_into_estimator_command_policy() -> None:
    """The controller satisfies the real online seam's injected callback contract."""

    fixed = diagnosis("actuator", location=0, severity=0.5)

    class FixedEstimator(DiagnosisEstimator):
        """Emit one fixed attribution while preserving the requested step/time."""

        def reset(self) -> None:
            """This deterministic fixture has no rolling state."""

        def update(self, step_index, decision_time_s, _window):
            """Return the fixed attribution at the current decision coordinates."""

            return EstimatorOutput(
                step=step_index,
                decision_time_s=decision_time_s,
                p_class=fixed.p_class.copy(),
                unknown_score=fixed.unknown_score,
                abstain_decision=fixed.abstain_decision,
                location_out=fixed.location_out,
                severity_out=fixed.severity_out,
                severity_uncertainty=fixed.severity_uncertainty,
                detection_time_s=decision_time_s,
            )

    controller = GainScheduledRecoveryController()
    policy = EstimatorCommandPolicy(
        FixedEstimator(), suite="C1", recovery_command=controller
    )
    command = policy(0, 0.137, None)
    nominal = commanded_torque(0.137, scale=controller.config.nominal_task_scale)
    assert command[0] == pytest.approx(2.0 * nominal[0])
    assert command[1] == pytest.approx(nominal[1])
    assert len(policy.trace) == 1


@pytest.mark.parametrize(
    "config",
    [
        RecoveryControlConfig(source_probability_threshold=0.0),
        RecoveryControlConfig(structural_action="unknown"),
        RecoveryControlConfig(structural_compensation_scope="unknown"),
        RecoveryControlConfig(structural_command_derate=1.1),
        RecoveryControlConfig(minimum_stiffness_remaining=1.1),
        RecoveryControlConfig(maximum_structural_compensation=0.9),
        RecoveryControlConfig(minimum_gain_remaining=1.1),
        RecoveryControlConfig(maximum_gain_compensation=0.9),
        RecoveryControlConfig(torque_abs_limit=(1.0, -0.5)),
    ],
)
def test_recovery_config_rejects_nonphysical_values(
    config: RecoveryControlConfig,
) -> None:
    """Development defaults are explicit and malformed alternatives fail loudly."""

    with pytest.raises(ValueError):
        GainScheduledRecoveryController(config)
