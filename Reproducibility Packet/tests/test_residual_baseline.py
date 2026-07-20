"""Tests for the deployable linear system-ID residual attribution baseline."""

from __future__ import annotations

import sys
from pathlib import Path

import numpy as np
import pytest

SCRIPTS_DIR = Path(__file__).resolve().parents[1] / "scripts"
sys.path.insert(0, str(SCRIPTS_DIR))

from utils.cable_mechanics import commanded_torque  # noqa: E402
from utils.cable_plant import CablePlant  # noqa: E402
from utils.estimator import EstimatorCommandPolicy, SOURCE_CLASS_ORDER  # noqa: E402
from utils.online_loop import run_online_rollout  # noqa: E402
from utils.recovery_control import GainScheduledRecoveryController  # noqa: E402
from utils.residual_baseline import (  # noqa: E402
    LinearResidualAttributionEstimator,
    LinearResidualConfig,
)
from utils.schema_types import (  # noqa: E402
    CHANNEL_NAMES,
    CHANNEL_WIDTH,
    SUITE_CHANNELS,
    ObservedRecord,
)
from utils.sensor_model import OnlineSensorSession  # noqa: E402


def arx_record(
    suite: str,
    source_class: str,
    *,
    seed: int,
    n_steps: int = 80,
    dropout: bool = False,
) -> ObservedRecord:
    """Build a small observed-only system whose fault residual patterns are distinct."""

    if source_class not in SOURCE_CLASS_ORDER:
        raise ValueError(source_class)
    rng = np.random.default_rng(seed)
    times = np.arange(n_steps, dtype=float) * 0.01
    command = np.column_stack(
        [
            np.sin(2.0 * np.pi * 0.7 * times + 0.03 * seed),
            0.7 * np.cos(2.0 * np.pi * 0.4 * times - 0.02 * seed),
        ]
    )
    q_true = np.zeros((n_steps, 2), dtype=float)
    for step in range(1, n_steps):
        gain = 0.45 if source_class == "actuator" else 1.0
        q_true[step] = (
            0.94 * q_true[step - 1]
            + gain * np.array([0.06, 0.04]) * command[step]
        )
    q_true += rng.normal(0.0, 2.0e-4, q_true.shape)
    q_obs = q_true.copy()
    if source_class == "sensor":
        q_obs[:, 0] += 0.12
    qd_obs = np.vstack([np.zeros((1, 2)), np.diff(q_obs, axis=0) / 0.01])

    current = command + rng.normal(0.0, 2.0e-4, command.shape)
    imu = np.column_stack(
        [q_true, 0.5 * q_true, q_true[:, :1], -q_true[:, 1:2]]
    )
    gauge = np.column_stack(
        [
            30.0 * q_true[:, 0],
            -20.0 * q_true[:, 0],
            25.0 * q_true[:, 1],
            -15.0 * q_true[:, 1],
        ]
    )
    if source_class == "structure":
        gauge += np.array([8.0, -6.0, 5.0, -4.0])
    gauge += rng.normal(0.0, 0.01, gauge.shape)

    signal = {
        "q_obs": q_obs,
        "qd_obs": qd_obs,
        "tau_cmd": command,
        "current_proxy_obs": current,
        "imu_obs": imu,
        "gauge_obs": gauge,
    }
    values: dict[str, np.ndarray] = {}
    valid: dict[str, np.ndarray] = {}
    measurement: dict[str, np.ndarray] = {}
    availability: dict[str, np.ndarray] = {}
    latency: dict[str, np.ndarray] = {}
    for name in CHANNEL_NAMES:
        width = CHANNEL_WIDTH[name]
        present = name in SUITE_CHANNELS[suite]
        values[name] = (
            signal[name].copy() if present else np.full((n_steps, width), np.nan)
        )
        valid[name] = (
            np.ones((n_steps, width), dtype=bool)
            if present
            else np.zeros((n_steps, width), dtype=bool)
        )
        measurement[name] = times.copy()
        availability[name] = times.copy()
        latency[name] = np.zeros(n_steps, dtype=float)
    if dropout:
        valid["q_obs"][20:35, 0] = False
        values["q_obs"][20:35, 0] = np.nan
        valid["qd_obs"][20:36, 0] = False
        values["qd_obs"][20:36, 0] = np.nan
    return ObservedRecord(
        suite=suite,
        run_id=f"{source_class}-{seed}",
        pair_id=str(seed),
        config_hash="dev-residual-test",
        values=values,
        valid_mask=valid,
        measurement_time_s=measurement,
        availability_time_s=availability,
        latency_age_s=latency,
        suite_available_mask={
            name: name in SUITE_CHANNELS[suite] for name in CHANNEL_NAMES
        },
        split="development",
    )


def fitted_estimator(suite: str = "S") -> LinearResidualAttributionEstimator:
    """Fit all three role-separated stages on deterministic synthetic development data."""

    config = LinearResidualConfig(
        minimum_fit_transitions=16,
        residual_scale_floor=0.05,
        minimum_class_probability=0.4,
        persistence=2,
    )
    estimator = LinearResidualAttributionEstimator(config)
    estimator.fit_dynamics(
        [arx_record(suite, "healthy", seed=seed) for seed in range(4)]
    )
    estimator.fit_prototypes(
        {
            label: [
                arx_record(suite, label, seed=100 + 10 * index + seed)
                for seed in range(4)
            ]
            for index, label in enumerate(SOURCE_CLASS_ORDER)
        }
    )
    estimator.calibrate_unknown_threshold(
        {
            label: [
                arx_record(suite, label, seed=200 + 10 * index + seed)
                for seed in range(2)
            ]
            for index, label in enumerate(SOURCE_CLASS_ORDER)
        },
        false_abstention_rate=0.25,
        min_tail_count=1,
    )
    return estimator


def test_linear_residual_layout_is_suite_matched_and_deployable_only():
    c1 = fitted_estimator("C1")
    structural = fitted_estimator("S")
    assert c1.suite == "C1"
    assert structural.suite == "S"
    assert not any(name.startswith("gauge_obs") for name in c1.state_labels)
    assert sum(name.startswith("gauge_obs") for name in structural.state_labels) == 4
    assert "tau_cmd[0]" not in structural.state_labels
    assert len(structural.residual_feature_names) == 3 * len(structural.state_labels)
    with pytest.raises(ValueError, match="suite/layout"):
        structural.residual_vector(arx_record("C1", "healthy", seed=999))
    with pytest.raises(TypeError, match="ObservedRecord"):
        structural.residual_vector(object())  # type: ignore[arg-type]
    leaked = arx_record("C1", "healthy", seed=1000)
    leaked.suite_available_mask["gauge_obs"] = True
    with pytest.raises(ValueError, match="fixed deployable suite"):
        c1.residual_vector(leaked)


def test_residual_centroids_attribute_held_out_fault_patterns():
    estimator = fitted_estimator("S")
    for index, label in enumerate(SOURCE_CLASS_ORDER):
        distances = estimator.class_distances(
            arx_record("S", label, seed=500 + index)
        )
        assert int(np.argmin(distances)) == index


def test_unknown_tail_guard_and_role_lifecycle_fail_loud():
    estimator = LinearResidualAttributionEstimator(
        LinearResidualConfig(minimum_fit_transitions=16)
    )
    healthy_fit = [arx_record("S", "healthy", seed=seed) for seed in range(3)]
    estimator.fit_dynamics(healthy_fit)
    prototypes = {
        label: [
            arx_record("S", label, seed=50 + 10 * index + seed)
            for seed in range(3)
        ]
        for index, label in enumerate(SOURCE_CLASS_ORDER)
    }
    estimator.fit_prototypes(prototypes)
    with pytest.raises(ValueError, match="at least 100"):
        estimator.calibrate_unknown_threshold(
            {
                label: [
                    arx_record("S", label, seed=90 + 10 * index + seed)
                    for seed in range(3)
                ]
                for index, label in enumerate(SOURCE_CLASS_ORDER)
            }
        )
    estimator.calibrate_unknown_threshold(
        {
            label: [arx_record("S", label, seed=120 + index)]
            for index, label in enumerate(SOURCE_CLASS_ORDER)
        },
        false_abstention_rate=0.25,
        min_tail_count=1,
    )
    assert estimator.unknown_threshold is not None
    estimator.fit_dynamics(healthy_fit)
    assert estimator.unknown_threshold is None
    with pytest.raises(ValueError, match="fit_prototypes"):
        estimator.class_distances(arx_record("S", "healthy", seed=999))


def test_online_update_latches_attributed_fault_but_carries_no_recovery_fields():
    estimator = fitted_estimator("S")
    window = arx_record("S", "actuator", seed=777)
    first = estimator.update(10, 1.0, window)
    second = estimator.update(11, 1.01, window)
    actuator_index = SOURCE_CLASS_ORDER.index("actuator")
    assert int(np.argmax(second.p_class)) == actuator_index
    assert first.abstain_decision is False
    assert np.isnan(first.detection_time_s)
    assert second.detection_time_s == pytest.approx(1.01)
    assert second.location_out == -1
    assert second.severity_uncertainty == np.inf


def test_missing_targets_remain_explicit_and_residual_vector_stays_finite():
    estimator = fitted_estimator("S")
    clean = estimator.residual_vector(arx_record("S", "healthy", seed=900))
    dropped = estimator.residual_vector(
        arx_record("S", "sensor", seed=901, dropout=True)
    )
    assert np.all(np.isfinite(dropped))
    q0_valid_fraction = estimator.residual_feature_names.index(
        "q_obs[0].valid_fraction"
    )
    assert dropped[q0_valid_fraction] < clean[q0_valid_fraction]


def test_baseline_runs_on_real_causal_seam_without_claiming_active_recovery():
    estimator = fitted_estimator("S")
    policy = EstimatorCommandPolicy(
        estimator,
        suite="S",
        run_id="residual-real-seam",
        stride=1,
        recovery_command=GainScheduledRecoveryController(),
    )
    plant = CablePlant()
    result = run_online_rollout(
        plant,
        OnlineSensorSession(
            "S",
            pair_id="residual-real-seam",
            sensor_seed=17,
            control_dt_s=plant.config.control_dt_s,
        ),
        n_steps=6,
        history_steps=80,
        command_policy=policy,
    )
    expected = np.stack(
        [
            commanded_torque(step * plant.config.control_dt_s, scale=0.5)
            for step in range(6)
        ]
    )
    assert len(policy.trace) == 6
    assert result.observations.n_steps == 6
    assert np.allclose(result.plant.tau_cmd, expected)
    assert all(output.location_out == -1 for output in policy.trace.outputs)
    assert all(output.severity_uncertainty == np.inf for output in policy.trace.outputs)


def test_configuration_and_under_sized_fit_validation():
    with pytest.raises(ValueError):
        LinearResidualConfig(ridge=0.0).validate()
    estimator = LinearResidualAttributionEstimator(
        LinearResidualConfig(minimum_fit_transitions=32)
    )
    with pytest.raises(ValueError, match="at least 32"):
        estimator.fit_dynamics(
            [arx_record("S", "healthy", seed=1, n_steps=20)]
        )
