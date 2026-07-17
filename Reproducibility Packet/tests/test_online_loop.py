"""Tests for the causal one-step sensor session and online rollout loop."""

from __future__ import annotations

import sys
from pathlib import Path

import numpy as np
import pytest

SCRIPTS_DIR = Path(__file__).resolve().parents[1] / "scripts"
sys.path.insert(0, str(SCRIPTS_DIR))

from utils.cable_plant import CablePlant  # noqa: E402
from utils.online_loop import run_online_rollout  # noqa: E402
from utils.schema_types import CHANNEL_NAMES, FaultSpec  # noqa: E402
from utils.sensor_model import (  # noqa: E402
    OnlineSensorSession,
    SensorConfig,
    SensorModel,
)
from utils.synthetic_plant import synthetic_privileged_record  # noqa: E402


def test_online_session_matches_batch_wrapper_bitwise() -> None:
    """Incremental emissions stack to the exact batch-facing observation record."""

    record = synthetic_privileged_record(n_steps=30, f_ctrl=500.0, thermal_ramp_c=3.0)
    fault = FaultSpec(
        source_class="sensor",
        subtype="encoder_drift",
        location=1,
        severity=0.02,
        onset_index=8,
    )
    expected = SensorModel().observe(
        record, "S", pair_id="online-eq", sensor_seed=23, fault=fault
    )
    session = OnlineSensorSession(
        "S",
        pair_id="online-eq",
        sensor_seed=23,
        control_dt_s=0.002,
        fault=fault,
    )
    for index in range(record.n_steps):
        session.observe_step(record.slice_step(index))
    actual = session.to_record()
    for name in CHANNEL_NAMES:
        np.testing.assert_array_equal(actual.values[name], expected.values[name])
        np.testing.assert_array_equal(actual.valid_mask[name], expected.valid_mask[name])
        np.testing.assert_array_equal(
            actual.availability_time_s[name], expected.availability_time_s[name]
        )


def test_online_session_rejects_out_of_order_plant_steps() -> None:
    """Skipping the first control step cannot silently desynchronize pathology state."""

    record = synthetic_privileged_record(n_steps=3)
    session = OnlineSensorSession(
        "C1", pair_id=1, sensor_seed=2, control_dt_s=0.002
    )
    with pytest.raises(ValueError, match="expected plant step 0"):
        session.observe_step(record.slice_step(1))


@pytest.mark.parametrize(
    "config",
    [SensorConfig(gauge_hysteresis_alpha=1.0), SensorConfig(dropout_prob=1.1)],
)
def test_online_session_rejects_nonphysical_sensor_config(config: SensorConfig) -> None:
    """Invalid pathology constants fail before a rollout consumes plant state."""

    with pytest.raises(ValueError):
        OnlineSensorSession(
            "C1", pair_id=1, sensor_seed=2, control_dt_s=0.002, config=config
        )


def test_online_rollout_masks_latency_before_policy_decisions() -> None:
    """The policy sees only delivered history; the one-step gauge latency is causal."""

    plant = CablePlant(point_count=5)
    sensors = OnlineSensorSession(
        "S",
        pair_id="loop",
        sensor_seed=5,
        control_dt_s=plant.config.control_dt_s,
        config=SensorConfig(dropout_prob=0.0),
    )
    seen_lengths: list[int] = []

    def policy(step: int, _decision_time_s: float, observations) -> np.ndarray:
        if step == 0:
            assert observations is None
        else:
            assert observations is not None
            seen_lengths.append(observations.n_steps)
            assert np.all(np.isfinite(observations.values["q_obs"][-1]))
            # The immediately preceding gauge sample has 2 ms latency and is not yet
            # delivered at the next command decision; older rows become available.
            assert np.all(np.isnan(observations.values["gauge_obs"][-1]))
            if step >= 2:
                assert np.all(np.isfinite(observations.values["gauge_obs"][-2]))
        return np.zeros(2)

    result = run_online_rollout(
        plant,
        sensors,
        n_steps=4,
        history_steps=2,
        command_policy=policy,
    )
    assert seen_lengths == [1, 2, 2]
    assert result.plant.n_steps == 4
    assert result.observations.n_steps == 4
    assert np.all(np.isfinite(result.observations.values["gauge_obs"]))
