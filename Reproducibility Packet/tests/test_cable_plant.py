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
from utils.schema_types import FaultSpec, PlantStepState, PrivilegedRecord  # noqa: E402


def small_config(**kwargs: float) -> CableModelConfig:
    """Return the selected mechanics with a short-test control interval."""

    return dataclasses.replace(CableModelConfig(), **kwargs)


def test_plant_step_is_lossless_schema_b_state() -> None:
    """Every per-step field must survive stacking and slicing without omission."""

    plant = CablePlant(small_config(), point_count=9, simulation_timestep_s=2.0e-4)
    record = plant.rollout(3)
    assert record.deform_coords.shape == (3, 42)
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
