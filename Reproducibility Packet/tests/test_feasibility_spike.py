"""Tests for the mechanics-only MuJoCo feasibility spike."""

from __future__ import annotations

import sys
from pathlib import Path

import numpy as np
import pytest

SCRIPTS_DIR = Path(__file__).resolve().parents[1] / "scripts"
sys.path.insert(0, str(SCRIPTS_DIR))

from run_feasibility_spike import (  # noqa: E402
    SpikeConfig,
    build_two_link_model,
    run_gate,
    simulate_case,
)
from run_bounded_burst_sensitivity import build_candidates  # noqa: E402
from utils.cable_mechanics import (  # noqa: E402
    diagnostic_tip_force_z,
    diagnostic_tip_load_envelope,
)


def test_two_link_model_compiles_with_expected_independent_state() -> None:
    """The cable model should expose two links, four gauges, and many deformation DOFs."""

    config = SpikeConfig(duration_s=0.02, fault_onset_s=0.01)
    model, handles = build_two_link_model(config, 9, 2.0e-4)
    assert model.nu == 2
    assert model.nv > 2
    assert len(handles.l1_body_ids) == 8
    assert len(handles.l2_body_ids) == 8


def test_local_softening_changes_only_a_bounded_link2_section() -> None:
    """The structural fault should modify a nonempty proper subset of link-2 sections."""

    config = SpikeConfig(duration_s=0.02, fault_onset_s=0.01)
    nominal_model, nominal = build_two_link_model(config, 17, 1.0e-4, False)
    soft_model, softened = build_two_link_model(config, 17, 1.0e-4, True)
    assert 0 < len(softened.softened_geoms) < 16
    for geom_name in softened.softened_geoms:
        nominal_id = nominal_model.geom(geom_name).id
        soft_id = soft_model.geom(geom_name).id
        ratio = soft_model.geom_size[soft_id, 2] / nominal_model.geom_size[nominal_id, 2]
        assert np.isclose(ratio**3, config.structural_ei_remaining)
    assert not nominal.softened_geoms


def test_short_simulation_is_finite_and_has_schema_facing_shapes() -> None:
    """A short healthy run should produce finite causal channel histories."""

    config = SpikeConfig(duration_s=0.02, fault_onset_s=0.01, control_dt_s=0.002)
    result = simulate_case(config, 9, 2.0e-4, "healthy")
    assert result.q_obs_rad.shape == (10, 2)
    assert result.qd_obs_rad_s.shape == (10, 2)
    assert result.tau_cmd_nm.shape == (10, 2)
    assert result.imu.shape == (10, 6)
    assert result.gauge_microstrain.shape == (10, 4)
    assert result.tip_position_m.shape == (10, 3)
    assert np.all(np.isfinite(result.gauge_microstrain))


def test_bounded_diagnostic_burst_is_smooth_bounded_and_zero_mean() -> None:
    """A one-cycle raised-cosine burst should start/end at zero with no net impulse."""

    start = 0.5
    period = 1.0 / 0.8
    config = SpikeConfig(
        diagnostic_tip_load_start_s=start,
        diagnostic_tip_load_duration_s=period,
        diagnostic_tip_load_ramp_s=period / 8.0,
    )
    times = np.linspace(0.0, start + period + 0.5, 10001)
    force = np.asarray([diagnostic_tip_force_z(time, config) for time in times])
    assert diagnostic_tip_load_envelope(start - 1.0e-6, config) == 0.0
    assert diagnostic_tip_load_envelope(start, config) == 0.0
    assert diagnostic_tip_load_envelope(start + period, config) == 0.0
    assert np.max(np.abs(force)) <= config.diagnostic_tip_load_peak_n + 1.0e-12
    assert np.trapezoid(force, times) == pytest.approx(0.0, abs=1.0e-9)


def test_diagnostic_envelope_rejects_ramp_longer_than_half_burst() -> None:
    config = SpikeConfig(
        diagnostic_tip_load_duration_s=1.0,
        diagnostic_tip_load_ramp_s=0.6,
    )
    with pytest.raises(ValueError):
        diagnostic_tip_load_envelope(0.5, config)


def test_burst_sensitivity_candidates_keep_controls_and_integer_cycle_budgets() -> None:
    candidates = build_candidates(
        onset_s=1.0,
        peak_load_n=1.0,
        frequency_hz=0.8,
        cycles=[2, 1],
        ramp_period_fraction=0.125,
        settle_s=0.25,
    )
    assert [candidate.name for candidate in candidates] == [
        "ordinary_no_tip_load",
        "continuous_gate_load",
        "bounded_1_cycle",
        "bounded_2_cycle",
    ]
    one_cycle = candidates[2]
    assert one_cycle.config.diagnostic_tip_load_start_s == pytest.approx(1.0)
    assert one_cycle.config.diagnostic_tip_load_duration_s == pytest.approx(1.25)
    assert one_cycle.config.diagnostic_tip_load_ramp_s == pytest.approx(0.15625)


def test_quick_summary_declares_deformation_coordinate_contract(tmp_path: Path) -> None:
    """The candidate handoff should make n_def and gauge placement machine-readable."""

    config = SpikeConfig(duration_s=0.02, fault_onset_s=0.01, control_dt_s=0.002)
    summary = run_gate(config, tmp_path, quick=True)
    contract = summary["candidate_contract"]
    assert contract["n_def"] == 42
    assert contract["internal_ball_joints_per_link"] == 7
    assert [station["normalized_position"] for station in contract["gauge_stations"]] == [
        0.25,
        0.75,
        0.25,
        0.75,
    ]
