"""Tests for the noisy deployable-observation healthy-reference pilot."""

from __future__ import annotations

import dataclasses
import sys
from pathlib import Path

import numpy as np

SCRIPTS_DIR = Path(__file__).resolve().parents[1] / "scripts"
sys.path.insert(0, str(SCRIPTS_DIR))

from run_noisy_reference_pilot import (  # noqa: E402
    causal_window,
    ceil_to_stride,
    evaluate_reference,
    fit_reference,
    project_observed_suite,
    synchronous_coefficient_vector,
)
from utils.schema_types import CHANNEL_NAMES  # noqa: E402
from utils.estimator import WindowFeatureExtractor  # noqa: E402
from utils.sensor_model import SensorConfig, SensorModel  # noqa: E402
from utils.synthetic_plant import synthetic_privileged_record  # noqa: E402


def observed_s_record(n_steps: int = 800):
    """Build a deterministic real-path S record with a known gauge tone."""

    privileged = synthetic_privileged_record(
        n_steps=n_steps, f_ctrl=500.0, seed=3, thermal_ramp_c=1.0
    )
    tone = 20.0 * np.cos(2.0 * np.pi * 0.8 * privileged.t_s)
    gauges = privileged.gauge_true.copy()
    gauges[:, 0] += tone
    privileged = dataclasses.replace(privileged, gauge_true=gauges)
    return SensorModel(SensorConfig(dropout_prob=0.0)).observe(
        privileged,
        "S",
        pair_id="pilot-test",
        sensor_seed=9,
        run_id="pilot-test",
        config_hash="dev-test",
    )


def test_ceil_to_stride_uses_first_global_decision_at_or_after_index() -> None:
    """Decision alignment is global, causal, and never before probe end."""

    assert ceil_to_stride(1124, 4) == 1124
    assert ceil_to_stride(1124, 8) == 1128
    assert ceil_to_stride(1124, 16) == 1136


def test_causal_window_withholds_latest_latent_gauge_sample() -> None:
    """The pilot cannot read a gauge row whose declared latency has not elapsed."""

    observed = observed_s_record()
    window = causal_window(observed, end_index=700, window_steps=640)

    assert window.n_steps == 640
    assert window.valid_mask["tau_cmd"][-1].all()
    assert not window.valid_mask["gauge_obs"][-1].any()
    assert np.isnan(window.values["gauge_obs"][-1]).all()


def test_w512_is_inert_and_w640_retains_the_real_gauge_coefficients() -> None:
    """The required sub-cycle negative control stays zero while full-cycle S is live."""

    observed = observed_s_record()
    short = causal_window(observed, end_index=700, window_steps=512)
    full = causal_window(observed, end_index=700, window_steps=640)

    short_vector = synchronous_coefficient_vector(
        short, WindowFeatureExtractor(window_steps=512, probe_frequency_hz=0.8)
    )
    full_vector = synchronous_coefficient_vector(
        full, WindowFeatureExtractor(window_steps=640, probe_frequency_hz=0.8)
    )

    assert short_vector.shape == (36,)
    assert np.array_equal(short_vector, np.zeros_like(short_vector))
    assert np.any(np.abs(full_vector) > 1.0)


def test_projected_c1_is_exactly_the_matched_sensor_model_output() -> None:
    """Discarding S gauges preserves the actual C1 path bit-for-bit under CRN."""

    privileged = synthetic_privileged_record(n_steps=40, f_ctrl=500.0, seed=1)
    model = SensorModel(SensorConfig())
    observed_s = model.observe(
        privileged, "S", pair_id="matched", sensor_seed=7, run_id="S"
    )
    actual_c1 = model.observe(
        privileged, "C1", pair_id="matched", sensor_seed=7, run_id="C1"
    )
    projected_c1 = project_observed_suite(observed_s, "C1")

    for name in CHANNEL_NAMES:
        assert np.array_equal(
            projected_c1.values[name], actual_c1.values[name], equal_nan=True
        )
        assert np.array_equal(projected_c1.valid_mask[name], actual_c1.valid_mask[name])
        assert np.array_equal(
            projected_c1.measurement_time_s[name],
            actual_c1.measurement_time_s[name],
            equal_nan=True,
        )
        assert np.array_equal(
            projected_c1.availability_time_s[name],
            actual_c1.availability_time_s[name],
            equal_nan=True,
        )
        assert np.array_equal(
            projected_c1.latency_age_s[name],
            actual_c1.latency_age_s[name],
            equal_nan=True,
        )
        assert (
            projected_c1.suite_available_mask[name]
            == actual_c1.suite_available_mask[name]
        )


def test_reference_uses_calibration_only_and_scores_held_out_shapes() -> None:
    """A simple separated toy case has zero false alarms and perfect fault centroids."""

    calibration = {
        "healthy": np.array([[0.00, 0.00], [0.01, -0.01], [-0.01, 0.01], [0.02, 0.00]]),
        "structure": np.array([[2.0, 0.0], [2.1, 0.1], [1.9, -0.1], [2.0, 0.1]]),
        "actuator": np.array([[0.0, 2.0], [0.1, 2.1], [-0.1, 1.9], [0.1, 2.0]]),
        "sensor": np.array([[-2.0, -2.0], [-2.1, -1.9], [-1.9, -2.1], [-2.0, -2.1]]),
    }
    evaluation = {
        "healthy": np.array([[0.0, 0.0], [0.005, -0.005]]),
        "structure": np.array([[2.0, 0.05], [2.05, -0.05]]),
        "actuator": np.array([[0.05, 2.0], [-0.05, 2.05]]),
        "sensor": np.array([[-2.0, -2.05], [-2.05, -2.0]]),
    }

    result = evaluate_reference(fit_reference(calibration), evaluation)

    assert result["false_alarm_rate"] == 0.0
    assert result["minimum_fault_detection_rate"] == 1.0
    assert result["macro_attribution_accuracy"] == 1.0
