"""Tests for the synchronous-detection noise-floor sensitivity (Claude's lane).

Pins the load-bearing properties of the lock-in detector and the end-to-end floor
result: unit gain at an integer number of probe cycles, exact rejection of a linear
thermal-like ramp, calibrated amplitude recovery, unit-RMS signal shapes, and — over
the real gauge pathology stack — a synchronous noise floor far below the per-sample
mechanics-gate floor with the bounded-burst differentials detected.
"""

from __future__ import annotations

import sys
from pathlib import Path

import numpy as np
import pytest

SCRIPTS_DIR = Path(__file__).resolve().parents[1] / "scripts"
sys.path.insert(0, str(SCRIPTS_DIR))

import analyze_synchronous_detection_floor as mod  # noqa: E402


def test_detector_gain_is_unity_at_integer_cycles():
    # f_ctrl=500, W=500, f_d=1 Hz -> exactly one probe cycle spans the window.
    t = np.arange(500) / 500.0
    assert mod.detector_gain(t, 1.0) == pytest.approx(1.0, rel=0.02)


def test_synchronous_amplitude_rejects_linear_ramp():
    # A pure thermal-like ramp must be removed by the mean+linear detrend.
    t = np.arange(512) / 500.0
    ramp = np.linspace(0.0, 50.0, 512)  # 50 microstrain thermal excursion
    amp = mod.synchronous_amplitude(ramp, np.ones(512, bool), t, 0.8)
    assert amp < 0.02


def test_synchronous_amplitude_recovers_calibrated_tone():
    t = np.arange(500) / 500.0
    f_d, true_amp = 1.0, 7.0
    gain = mod.detector_gain(t, f_d)
    raw = mod.synchronous_amplitude(true_amp * np.cos(2 * np.pi * f_d * t), np.ones(500, bool), t, f_d)
    assert raw / gain == pytest.approx(true_amp, rel=0.02)


def test_unit_shapes_have_unit_rms():
    t = np.arange(512) / 500.0
    for shape in (mod.unit_tone(t, 0.8), mod.unit_burst(t, 0.8)):
        assert np.sqrt(np.mean(shape ** 2)) == pytest.approx(1.0, rel=1e-6)


def test_end_to_end_floor_below_gate_and_signal_detected():
    """The real gauge stack yields a synchronous NES far below the 10-microstrain floor."""

    # Build a minimal args namespace directly (avoid argparse/CLI in the test).
    import argparse

    ns = argparse.Namespace(
        output_dir=Path("."), f_ctrl_hz=500.0, window=512, diagnostic_hz=0.8,
        thermal_ramp_c=3.0, realizations=8, gate_floor_microstrain=10.0,
        target_rms_microstrain=[8.18], target_labels=["structural_1cycle"],
        detect_sigma=5.0, seed=0,
    )
    summary = mod.run(ns)
    nes = summary["noise_only_null"]["synchronous_nes_mean_microstrain"]
    assert 0.0 < nes < 1.0  # far below the 10-microstrain per-sample floor
    assert summary["gate_floor_over_synchronous_nes"] > 20.0
    tone = summary["targets"][0]["pure_tone"]
    assert tone["detection_rate_at_threshold"] == 1.0
    assert tone["z_over_null"] > 20.0
