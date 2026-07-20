"""Tests for the mechanics/detector safe-probe co-design screen."""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

import numpy as np
import pytest

SCRIPTS_DIR = Path(__file__).resolve().parents[1] / "scripts"
sys.path.insert(0, str(SCRIPTS_DIR))

from run_bounded_burst_sensitivity import signature_screen  # noqa: E402
from run_feasibility_spike import SimulationResult, SpikeConfig  # noqa: E402
from screen_synchronous_safe_probe import (  # noqa: E402
    actual_harmonic_signatures,
    build_probe_candidates,
    load_detector_contract,
)


def result_with(
    time_s: np.ndarray,
    *,
    q_true: np.ndarray | None = None,
    q_obs: np.ndarray | None = None,
    gauge: np.ndarray | None = None,
) -> SimulationResult:
    """Build a minimal finite mechanics result for pure-function tests."""

    n = time_s.size
    q_true = np.zeros((n, 2)) if q_true is None else q_true
    q_obs = q_true.copy() if q_obs is None else q_obs
    gauge = np.zeros((n, 4)) if gauge is None else gauge
    return SimulationResult(
        time_s=time_s,
        tau_cmd_nm=np.zeros((n, 2)),
        q_true_rad=q_true,
        qd_true_rad_s=np.zeros((n, 2)),
        q_obs_rad=q_obs,
        qd_obs_rad_s=np.zeros((n, 2)),
        imu=np.zeros((n, 6)),
        gauge_microstrain=gauge,
        tip_position_m=np.tile([0.8, 0.0, 0.5], (n, 1)),
        max_connect_residual_m=0.0,
    )


def test_actual_harmonic_signatures_use_all_four_mechanics_channels() -> None:
    time_s = np.arange(640) / 500.0
    tone = np.cos(2.0 * np.pi * 0.8 * time_s)
    healthy = result_with(time_s)
    structural_gauge = np.zeros((640, 4))
    actuator_gauge = np.zeros((640, 4))
    structural_gauge[:, 3] = 0.8 * tone
    actuator_gauge[:, 1] = 0.6 * tone
    cases = {
        "healthy": healthy,
        "structural": result_with(time_s, gauge=structural_gauge),
        "actuator": result_with(time_s, gauge=actuator_gauge),
        "encoder": healthy,
    }
    output = actual_harmonic_signatures(
        cases, onset_s=0.0, window_samples=640, frequency_hz=0.8
    )
    assert output["structural_minus_healthy"]["max_gauge_index"] == 3
    assert output["structural_minus_healthy"]["max_amplitude_microstrain"] == pytest.approx(0.8)
    assert output["actuator_minus_healthy"]["max_gauge_index"] == 1
    assert output["actuator_minus_healthy"]["max_amplitude_microstrain"] == pytest.approx(0.6)


def test_safety_screen_checks_fault_cases_not_only_healthy() -> None:
    time_s = np.arange(10) * 0.002
    healthy = result_with(time_s)
    unsafe_q = np.zeros((10, 2))
    unsafe_q[:, 0] = 4.0
    encoder_q = np.zeros((10, 2))
    encoder_q[:, 0] = 0.05
    cases = {
        "healthy": healthy,
        "structural": result_with(time_s, q_true=unsafe_q),
        "actuator": healthy,
        "encoder": result_with(time_s, q_obs=encoder_q),
    }
    config = SpikeConfig(duration_s=0.02, fault_onset_s=0.0)
    screen = signature_screen(cases, config, analysis_duration_s=0.018)
    assert screen["safety_checks"]["joint_angle_limit_exceeded"]
    assert not screen["safety_screen_pass"]
    assert screen["scenario_safety"]["structural"]["peak_abs_joint_angle_rad"] == 4.0


def test_detector_contract_and_candidate_grid(tmp_path: Path) -> None:
    summary_path = tmp_path / "summary.json"
    summary_path.write_text(
        json.dumps(
            {
                "config": {
                    "diagnostic_hz": 0.8,
                    "f_ctrl_hz": 500.0,
                    "window_samples": 640,
                    "realizations": 200,
                },
                "noise_only_null": {"detect_threshold_microstrain": 0.3},
            }
        ),
        encoding="utf-8",
    )
    contract = load_detector_contract(summary_path, 0.8)
    assert contract["window_samples"] == 640
    args = argparse.Namespace(
        task_torque_scales=[0.2, 0.1],
        peak_loads_n=[0.05, 0.025],
        minimum_detector_margin=2.0,
        fault_onset_s=1.0,
        frequency_hz=0.8,
        ramp_period_fraction=0.125,
        settle_s=0.25,
    )
    candidates = build_probe_candidates(args)
    assert [name for name, _ in candidates] == [
        "task_0.100_probe_0.025N",
        "task_0.100_probe_0.050N",
        "task_0.200_probe_0.025N",
        "task_0.200_probe_0.050N",
    ]
    assert candidates[-1][1].config.task_torque_scale == pytest.approx(0.2)
