"""Tests for the synchronous-detection noise-floor sensitivity (Claude's lane).

Pins phase-invariant harmonic recovery, rejection of a linear thermal-like ramp,
unit-RMS signal shapes, the full-cycle requirement for the burst surrogate, and
the detector floor produced by the real gauge pathology stack.
"""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

import numpy as np
import pytest

SCRIPTS_DIR = Path(__file__).resolve().parents[1] / "scripts"
sys.path.insert(0, str(SCRIPTS_DIR))

import analyze_synchronous_detection_floor as mod  # noqa: E402


def test_detector_gain_is_phase_invariant_on_noninteger_window() -> None:
    """Joint trend/harmonic regression must not need phase-specific calibration."""

    t = np.arange(512) / 500.0  # 0.8192 cycles at 0.8 Hz
    for phase in np.linspace(0.0, 2.0 * np.pi, 16, endpoint=False):
        tone = np.cos(2.0 * np.pi * 0.8 * t + phase)
        recovered = mod.synchronous_amplitude(tone, np.ones(t.size, bool), t, 0.8)
        assert recovered == pytest.approx(1.0, rel=1.0e-9, abs=1.0e-9)


def test_synchronous_amplitude_rejects_linear_ramp() -> None:
    """A pure linear thermal-like ramp is part of the fitted nuisance model."""

    t = np.arange(512) / 500.0
    ramp = np.linspace(0.0, 50.0, 512)
    amp = mod.synchronous_amplitude(ramp, np.ones(512, bool), t, 0.8)
    assert amp < 1.0e-10


def test_synchronous_amplitude_recovers_calibrated_tone() -> None:
    t = np.arange(500) / 500.0
    true_amp = 7.0
    raw = mod.synchronous_amplitude(
        true_amp * np.cos(2.0 * np.pi * t), np.ones(500, bool), t, 1.0
    )
    assert raw == pytest.approx(true_amp, rel=1.0e-9, abs=1.0e-9)


def test_unit_shapes_have_unit_rms() -> None:
    t = np.arange(640) / 500.0
    for shape in (mod.unit_tone(t, 0.8), mod.unit_burst(t, 0.8)):
        assert np.sqrt(np.mean(shape**2)) == pytest.approx(1.0, rel=1.0e-6)


def test_one_cycle_burst_rejects_a_shorter_window() -> None:
    t = np.arange(512) / 500.0
    with pytest.raises(ValueError, match="at least one period"):
        mod.unit_burst(t, 0.8)


def test_end_to_end_floor_below_gate_and_signal_detected() -> None:
    """The real gauge stack yields a synchronous floor below the per-sample floor."""

    args = argparse.Namespace(
        output_dir=Path("."),
        f_ctrl_hz=500.0,
        window=640,
        diagnostic_hz=0.8,
        thermal_ramp_c=3.0,
        realizations=8,
        gate_floor_microstrain=10.0,
        target_rms_microstrain=[8.18],
        target_labels=["structural_1cycle"],
        detect_sigma=5.0,
        seed=0,
    )
    summary = mod.run(args)
    nes = summary["noise_only_null"]["synchronous_nes_mean_microstrain"]
    assert 0.0 < nes < 1.0
    assert summary["gate_floor_over_synchronous_nes"] > 20.0
    assert summary["config"]["harmonic_regression_gain"] == pytest.approx(1.0)
    tone = summary["targets"][0]["pure_tone"]
    assert tone["detection_rate_at_threshold"] == 1.0
    assert tone["z_over_null"] > 20.0
