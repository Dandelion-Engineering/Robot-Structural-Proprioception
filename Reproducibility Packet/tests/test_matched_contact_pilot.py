"""Tests for the matched contact-enabled C1/S development pilot."""

from __future__ import annotations

import dataclasses
import sys
from pathlib import Path

import numpy as np
import pytest

SCRIPTS_DIR = Path(__file__).resolve().parents[1] / "scripts"
sys.path.insert(0, str(SCRIPTS_DIR))

from run_matched_contact_pilot import (  # noqa: E402
    MatchedContactPilotSpec,
    PilotPrototypeEstimator,
    decide,
)
from run_noisy_reference_pilot import (  # noqa: E402
    CoefficientReference,
    causal_window,
)
from utils.cable_mechanics import commanded_torque  # noqa: E402
from utils.estimator import (  # noqa: E402
    SOURCE_CLASS_ORDER,
    WindowFeatureExtractor,
    coefficient_reference_distance,
    synchronous_coefficient_vector,
)
from utils.recovery_control import GainScheduledRecoveryController  # noqa: E402
from utils.sensor_model import SensorConfig, SensorModel  # noqa: E402
from utils.synthetic_plant import synthetic_privileged_record  # noqa: E402


def real_observed_window():
    """Return a real-path S window with a resolvable synchronous gauge tone."""

    privileged = synthetic_privileged_record(
        n_steps=800, f_ctrl=500.0, seed=5, thermal_ramp_c=1.0
    )
    gauges = privileged.gauge_true.copy()
    gauges[:, 0] += 20.0 * np.cos(2.0 * np.pi * 0.8 * privileged.t_s)
    privileged = dataclasses.replace(privileged, gauge_true=gauges)
    observed = SensorModel(SensorConfig(dropout_prob=0.0)).observe(
        privileged,
        "S",
        pair_id="matched-contact-test",
        sensor_seed=4,
        run_id="matched-contact-test",
    )
    return causal_window(observed, end_index=799, window_steps=768)


def prototype_reference(window, predicted_source: str) -> CoefficientReference:
    """Return a toy reference whose nearest centroid is ``predicted_source``."""

    extractor = WindowFeatureExtractor(window_steps=768, probe_frequency_hz=0.8)
    vector = synchronous_coefficient_vector(window, extractor)
    scale = np.ones_like(vector)
    score = coefficient_reference_distance(vector, np.zeros_like(vector), scale)
    centroids = {
        "structure": vector + 100.0,
        "actuator": vector - 100.0,
        "sensor": vector + 200.0,
    }
    centroids[predicted_source] = vector.copy()
    return CoefficientReference(
        healthy_mean=np.zeros_like(vector),
        healthy_scale=scale,
        detect_threshold=score / 2.0,
        fault_centroids=centroids,
        calibration_null_scores=np.array([0.01, 0.02, 0.03, 0.04]),
    )


def test_spec_pins_exact_online_causal_boundary() -> None:
    """The online policy owns only samples through k-1 at decision step k."""

    spec = MatchedContactPilotSpec()
    spec.validate()
    assert spec.onset_index == 500
    assert spec.period_steps == 625
    assert spec.probe_end_index == 1124
    assert spec.first_online_decision_step == 1136
    assert spec.offline_decision_index == 1135
    assert spec.short_n_steps == 1300
    assert spec.evaluation_n_steps == 3000


def test_spec_requires_the_full_five_second_post_onset_audit() -> None:
    """A short pilot horizon cannot masquerade as the evaluation horizon."""

    with pytest.raises(ValueError, match="five seconds after onset"):
        MatchedContactPilotSpec(evaluation_horizon_s=5.9).validate()


def test_prototype_estimator_is_gated_then_maps_predicted_actuator() -> None:
    """The pilot estimator cannot act before the probe and uses its predicted class."""

    window = real_observed_window()
    estimator = PilotPrototypeEstimator(
        prototype_reference(window, "actuator"),
        suite="S",
        window_steps=768,
        probe_frequency_hz=0.8,
        first_decision_step=16,
    )
    before = estimator.update(15, 0.030, window)
    after = estimator.update(16, 0.032, window)
    assert SOURCE_CLASS_ORDER[int(np.argmax(before.p_class))] == "healthy"
    assert np.isnan(before.detection_time_s)
    assert SOURCE_CLASS_ORDER[int(np.argmax(after.p_class))] == "actuator"
    assert after.location_out == 1
    assert after.severity_out == 0.70
    assert after.severity_uncertainty == 0.0
    assert after.detection_time_s == 0.032


def test_sensor_prototype_reaches_controller_but_preserves_nominal_command() -> None:
    """The current controller has no sensor-specific action and therefore fails safe."""

    window = real_observed_window()
    estimator = PilotPrototypeEstimator(
        prototype_reference(window, "sensor"),
        suite="S",
        window_steps=768,
        probe_frequency_hz=0.8,
        first_decision_step=0,
    )
    output = estimator.update(0, 0.0, window)
    command = GainScheduledRecoveryController()(output, 0, 0.0)
    assert SOURCE_CLASS_ORDER[int(np.argmax(output.p_class))] == "sensor"
    assert np.array_equal(command, commanded_torque(0.0, scale=0.5))


def test_overall_decision_keeps_extended_horizon_block_separate() -> None:
    """A passing short pilot cannot override unsafe or repeated long-horizon contact."""

    spec = MatchedContactPilotSpec()
    offline = [
        {
            "suite": "C1",
            "false_alarm_rate": 0.1,
            "minimum_fault_detection_rate": 0.2,
            "macro_attribution_accuracy": 1.0,
        },
        {
            "suite": "S",
            "false_alarm_rate": 0.0,
            "minimum_fault_detection_rate": 1.0,
            "macro_attribution_accuracy": 1.0,
        },
    ]
    online = [
        {
            "source": source,
            "suite": suite,
            "any_safety_flag": False,
            "contact_episode_count": 1,
            "command_changed_before_first_decision": False,
            "command_changed_steps": 0,
            "final_predicted_source": source,
            "ever_predicted_source": True,
        }
        for source in ("healthy", "structure", "actuator", "sensor")
        for suite in ("C1", "S")
    ]
    extended = [
        {
            "plane_z_m": plane,
            "scenario": source,
            "any_safety_flag": plane == spec.selected_plane_z_m,
            "contact_episode_count": 3 if plane == spec.selected_plane_z_m else 1,
            "contact_active_steps": 10,
        }
        for plane in (spec.former_control_plane_z_m, spec.selected_plane_z_m)
        for source in ("healthy", "structure", "actuator")
    ]
    result = decide(spec, offline, online, extended)
    assert result["short_horizon_status"] == "ADVANCE_SHORT_HORIZON_DEVELOPMENT_ONLY"
    assert not result["evaluation_horizon_contact_pass"]
    assert result["overall_decision"].startswith("BLOCK_CONTACT_PROFILE")
