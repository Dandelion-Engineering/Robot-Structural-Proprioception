"""Tests for the bounded optional endpoint-contact profile screen."""

from __future__ import annotations

import sys
from pathlib import Path

import numpy as np

SCRIPTS_DIR = Path(__file__).resolve().parents[1] / "scripts"
sys.path.insert(0, str(SCRIPTS_DIR))

from screen_optional_contact_profile import (  # noqa: E402
    CANONICAL_SCENARIOS,
    ScreenSpec,
    count_contact_episodes,
    run_physical_scenario,
    select_candidate,
    sensor_alias_row,
)


def synthetic_row(
    plane_z_m: float,
    scenario: str,
    *,
    active_steps: int,
    gate_pass: bool,
    safety: bool = False,
) -> dict[str, object]:
    """Return the fields consumed by the selection rule."""

    return {
        "plane_z_m": plane_z_m,
        "scenario": scenario,
        "contact_active_steps": active_steps,
        "any_safety_flag": safety,
        "contact_profile_gate_pass": gate_pass,
    }


def test_count_contact_episodes_counts_contiguous_runs() -> None:
    active = np.array([False, True, True, False, True, False, True, True], dtype=bool)
    assert count_contact_episodes(active) == 3
    assert count_contact_episodes(np.zeros(5, dtype=bool)) == 0


def test_selection_uses_zero_contact_control_and_lowest_all_scenario_pass() -> None:
    spec = ScreenSpec(plane_heights_z_m=(0.05, 0.075, 0.10))
    rows: list[dict[str, object]] = []
    rows.extend(
        synthetic_row(0.05, scenario, active_steps=0, gate_pass=False)
        for scenario in CANONICAL_SCENARIOS
    )
    rows.extend(
        synthetic_row(
            0.075,
            scenario,
            active_steps=10 if scenario == "actuator" else 0,
            gate_pass=scenario == "actuator",
        )
        for scenario in CANONICAL_SCENARIOS
    )
    rows.extend(
        synthetic_row(0.10, scenario, active_steps=12, gate_pass=True)
        for scenario in CANONICAL_SCENARIOS
    )
    selection = select_candidate(rows, spec)  # type: ignore[arg-type]
    assert selection["negative_control_pass"]
    assert selection["selected_plane_z_m"] == 0.10
    assert selection["decision"].startswith("ADVANCE")


def test_sensor_alias_preserves_physics_but_marks_observation_side_fault() -> None:
    healthy = {
        "plane_z_m": 0.10,
        "scenario": "healthy",
        "plant_fault_source_class": "healthy",
        "sensor_fault_is_observation_side": False,
        "peak_contact_force_n": 1.25,
        "contact_profile_gate_pass": True,
    }
    sensor = sensor_alias_row(healthy)
    assert sensor["scenario"] == "sensor"
    assert sensor["plant_fault_source_class"] == "healthy"
    assert sensor["sensor_fault_is_observation_side"] is True
    assert sensor["peak_contact_force_n"] == healthy["peak_contact_force_n"]
    assert sensor["contact_profile_gate_pass"] == healthy["contact_profile_gate_pass"]


def test_short_real_case_reaches_contact_role() -> None:
    spec = ScreenSpec(
        plane_heights_z_m=(0.49, 0.498),
        task_torque_scale=0.0,
        diagnostic_tip_load_peak_n=0.05,
        fault_onset_s=0.0,
        duration_s=1.25,
        point_count=9,
        simulation_timestep_s=2.0e-4,
        minimum_contact_active_steps=1,
        maximum_contact_active_fraction=0.99,
    )
    row = run_physical_scenario(0.498, "healthy", spec)
    assert row["contact_active_steps"] > 0
    assert row["peak_contact_force_n"] > 0.0
    assert row["safety_incident_steps"] == 0
