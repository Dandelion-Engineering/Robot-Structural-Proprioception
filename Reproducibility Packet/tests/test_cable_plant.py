"""Tests for the schema-facing MuJoCo cable plant producer."""

from __future__ import annotations

import dataclasses
import sys
from pathlib import Path

import numpy as np
import pytest

SCRIPTS_DIR = Path(__file__).resolve().parents[1] / "scripts"
sys.path.insert(0, str(SCRIPTS_DIR))

from utils.cable_mechanics import CableModelConfig  # noqa: E402
from utils.cable_plant import CablePlant  # noqa: E402
from utils.schema_types import (  # noqa: E402
    CONTACT_STATE_FIELDS,
    SAFETY_FLAG_FIELDS,
    FaultSpec,
    PlantStepState,
    PrivilegedRecord,
)


def small_config(**kwargs: float) -> CableModelConfig:
    """Return the selected mechanics with a short-test control interval."""

    return dataclasses.replace(CableModelConfig(), **kwargs)


def test_plant_step_is_lossless_schema_b_state() -> None:
    """Every per-step field must survive stacking and slicing without omission."""

    plant = CablePlant(small_config(), point_count=9, simulation_timestep_s=2.0e-4)
    record = plant.rollout(3)
    assert record.deform_coords.shape == (3, 42)
    assert record.contact_state.shape == (3, len(CONTACT_STATE_FIELDS))
    assert record.safety_flag.shape == (3, len(SAFETY_FLAG_FIELDS))
    assert np.all(record.contact_state == 0.0)
    restored = record.slice_step(1)
    for field in dataclasses.fields(PlantStepState):
        expected = getattr(restored, field.name)
        original = getattr(record, field.name)[1]
        np.testing.assert_array_equal(np.asarray(expected), np.asarray(original))


def test_privileged_trace_round_trip_validates(tmp_path: Path) -> None:
    """A real plant trace persists as a non-pickled schema-B payload."""

    record = CablePlant(
        small_config(diagnostic_tip_load_peak_n=0.0),
        point_count=9,
        simulation_timestep_s=2.0e-4,
    ).rollout(4)
    path = tmp_path / "plant.npz"
    record.save_npz(path)
    restored = PrivilegedRecord.load_npz(path)
    assert restored.n_steps == 4
    assert restored.n_def == 42
    np.testing.assert_allclose(restored.gauge_true, record.gauge_true)


def test_actuator_gain_loss_is_downstream_of_control_effort() -> None:
    """The current-proxy source stays nominal while delivered torque loses gain."""

    fault = FaultSpec(
        source_class="actuator",
        subtype="actuator_gain_loss",
        location=1,
        severity=0.70,
        onset_index=0,
    )
    plant = CablePlant(
        small_config(diagnostic_tip_load_peak_n=0.0),
        point_count=9,
        simulation_timestep_s=2.0e-4,
        fault=fault,
    )
    state = plant.advance(np.array([0.2, 0.1]))
    np.testing.assert_allclose(state.control_effort, [0.2, 0.1])
    np.testing.assert_allclose(state.tau_delivered_true, [0.2, 0.07])


def test_structural_fault_swaps_only_at_declared_control_step() -> None:
    """The softened link-2 model activates at the first declared affected sample."""

    fault = FaultSpec(
        source_class="structure",
        subtype="link_stiffness_loss",
        location=1,
        severity=0.50,
        onset_index=1,
    )
    plant = CablePlant(
        small_config(diagnostic_tip_load_peak_n=0.0),
        point_count=9,
        simulation_timestep_s=2.0e-4,
        fault=fault,
    )
    plant.advance(np.zeros(2))
    assert not plant.handles.softened_geoms
    state = plant.advance(np.zeros(2))
    assert plant.handles.softened_geoms
    assert np.all(np.isfinite(state.deform_coords))


def test_sensor_fault_is_rejected_by_plant_boundary() -> None:
    """Encoder corruption cannot enter the physical plant implementation."""

    fault = FaultSpec(
        source_class="sensor",
        subtype="encoder_bias",
        location=0,
        severity=0.05,
        onset_index=0,
    )
    with pytest.raises(ValueError, match="sensor faults"):
        CablePlant(small_config(), point_count=9, simulation_timestep_s=2.0e-4, fault=fault)


def test_safety_role_uses_fixed_order_and_flags_gauge_overrange() -> None:
    """The implemented seven-wide role must evaluate, not merely allocate, flags."""

    plant = CablePlant(
        small_config(gauge_abs_limit_microstrain=1.0e-9),
        point_count=9,
        simulation_timestep_s=2.0e-4,
    )
    state = plant.advance(np.zeros(2))
    assert state.safety_flag.shape == (len(SAFETY_FLAG_FIELDS),)
    assert bool(state.safety_flag[SAFETY_FLAG_FIELDS.index("gauge_abs_exceeded")])
    assert not bool(state.contact_state[CONTACT_STATE_FIELDS.index("tip_contact_active")])


def test_optional_endpoint_contact_records_mujoco_force_and_safety_truth() -> None:
    """The contact profile must populate A1 from the actual endpoint-plane constraint."""

    plant = CablePlant(
        small_config(
            task_torque_scale=0.0,
            endpoint_contact_enabled=True,
            endpoint_contact_plane_z_m=0.498,
            tip_contact_force_limit_n=0.05,
        ),
        point_count=9,
        simulation_timestep_s=2.0e-4,
    )
    record = plant.rollout(100, command_fn=lambda _time_s: np.zeros(2))
    force_col = CONTACT_STATE_FIELDS.index("tip_contact_force_n")
    active_col = CONTACT_STATE_FIELDS.index("tip_contact_active")
    safety_col = SAFETY_FLAG_FIELDS.index("tip_contact_force_exceeded")

    assert np.any(record.contact_state[:, active_col] == 1.0)
    assert np.max(record.contact_state[:, force_col]) > 0.05
    np.testing.assert_array_equal(
        record.safety_flag[:, safety_col],
        record.contact_state[:, force_col] > plant.config.tip_contact_force_limit_n,
    )


def test_default_rollout_honors_task_torque_scale() -> None:
    plant = CablePlant(
        small_config(task_torque_scale=0.0, diagnostic_tip_load_peak_n=0.0),
        point_count=9,
        simulation_timestep_s=2.0e-4,
    )
    record = plant.rollout(3)
    np.testing.assert_array_equal(record.tau_cmd, np.zeros((3, 2)))
