"""Tests for the bounded task/contact/controller redesign screen."""

from __future__ import annotations

import sys
from pathlib import Path

import numpy as np
import pytest

SCRIPTS_DIR = Path(__file__).resolve().parents[1] / "scripts"
sys.path.insert(0, str(SCRIPTS_DIR))

from screen_bounded_task_contact import (  # noqa: E402
    BoundedTaskContactSpec,
    FixedSourceStandIn,
    SingleDecisionHoldEstimator,
    select_candidate,
)
from utils.estimator import SOURCE_CLASS_ORDER  # noqa: E402
from utils.task_control import (  # noqa: E402
    BoundedTaskProfile,
    EstimatorRecoveryTaskPolicy,
    ObservedJointControllerConfig,
    ObservedJointPDController,
)


def test_screen_orders_probe_decision_motion_and_full_horizon() -> None:
    """The controller must decide before contact motion and audit onset plus five seconds."""

    spec = BoundedTaskContactSpec()
    spec.validate()
    assert spec.onset_index == 500
    assert spec.period_steps == 625
    assert spec.first_decision_step == 1136
    assert spec.first_decision_time_s == pytest.approx(2.272)
    assert spec.first_decision_time_s < spec.movement_start_s
    assert spec.n_steps == 3000
    with pytest.raises(ValueError, match="precede the contact excursion"):
        BoundedTaskContactSpec(movement_start_s=2.0).validate()
    with pytest.raises(ValueError, match="five seconds"):
        BoundedTaskContactSpec(duration_s=5.9).validate()


def test_bounded_profile_is_finite_smooth_and_returns_to_zero() -> None:
    """The development task is a finite reference, not perpetual open-loop torque."""

    profile = BoundedTaskProfile()
    np.testing.assert_array_equal(profile.joint_reference(2.0), np.zeros(2))
    np.testing.assert_allclose(profile.joint_reference(2.7), np.array([0.15, 0.15]))
    np.testing.assert_allclose(profile.joint_reference(3.2), np.array([0.30, 0.30]))
    np.testing.assert_allclose(profile.joint_reference(4.7), np.array([0.15, 0.15]))
    np.testing.assert_array_equal(profile.joint_reference(5.0), np.zeros(2))
    np.testing.assert_allclose(profile.task_reference(0.0), np.array([0.8, 0.0]))


def test_single_decision_wrapper_evaluates_once_and_holds_source() -> None:
    """A scheduled classifier is never reused on later out-of-phase windows."""

    inner = FixedSourceStandIn("actuator")
    estimator = SingleDecisionHoldEstimator(inner, first_decision_step=16)
    before = estimator.update(15, 0.030, None)
    first = estimator.update(16, 0.032, None)
    later = estimator.update(32, 0.064, None)
    assert SOURCE_CLASS_ORDER[int(np.argmax(before.p_class))] == "healthy"
    assert SOURCE_CLASS_ORDER[int(np.argmax(first.p_class))] == "actuator"
    assert SOURCE_CLASS_ORDER[int(np.argmax(later.p_class))] == "actuator"
    assert first.detection_time_s == later.detection_time_s == 0.032
    assert first.location_out == later.location_out == 1
    assert inner.calls == estimator.classification_evaluations == 1


def test_task_recovery_composition_never_acts_before_held_decision() -> None:
    """The fixed actuator action begins only after the scheduled classifier call."""

    profile = BoundedTaskProfile(
        target_joint_rad=(0.3, 0.3),
        movement_start_s=0.02,
        transition_s=0.02,
        hold_end_s=0.08,
        return_end_s=0.10,
    )
    task = ObservedJointPDController(
        profile,
        ObservedJointControllerConfig(
            proportional_gain=(0.05, 0.03),
            derivative_gain=(0.0, 0.0),
            torque_abs_limit=(0.2, 0.1),
        ),
    )
    estimator = SingleDecisionHoldEstimator(
        FixedSourceStandIn("actuator"), first_decision_step=4
    )
    policy = EstimatorRecoveryTaskPolicy(
        task, estimator, suite="C1", run_id="test", stride=1
    )
    for step in range(8):
        policy(step, step * 0.01, None)
    nominal = np.stack(policy.nominal_commands)
    applied = np.stack(policy.commands)
    np.testing.assert_allclose(applied[:4], nominal[:4])
    assert np.any(~np.isclose(applied[4:, 1], nominal[4:, 1]))
    np.testing.assert_allclose(applied[4:, 0], nominal[4:, 0])
    assert estimator.classification_evaluations == 1


def test_selection_needs_no_contact_control_and_all_source_pass() -> None:
    """One convenient source row cannot advance a task/contact profile."""

    spec = BoundedTaskContactSpec()
    rows = []
    for plane in spec.plane_heights_z_m:
        for source in ("healthy", "structure", "actuator", "sensor"):
            rows.append(
                {
                    "plane_z_m": plane,
                    "source": source,
                    "contact_active_steps": 0 if plane == 0.100 else 20,
                    "any_safety_flag": False,
                    "recovery_changed_before_decision": False,
                    "bounded_profile_gate_pass": plane >= 0.200,
                }
            )
    result = select_candidate(rows, spec)
    assert result["negative_control_pass"]
    assert result["selected_plane_z_m"] == pytest.approx(0.200)
    assert result["decision"].startswith("ADVANCE_BOUNDED_TASK")
