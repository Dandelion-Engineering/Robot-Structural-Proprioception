"""Tests for the sensor-realism + fault-injection model (schema section C).

Each test pins a load-bearing schema property: the privileged/observed leakage
boundary, common-random-number substreams, suite channel masking, the sensor-fault
relational signature, thermal apparent strain, dropout validity, latency causality,
and deterministic reproducibility.
"""

from __future__ import annotations

import dataclasses
import sys
from pathlib import Path

import numpy as np

SCRIPTS_DIR = Path(__file__).resolve().parents[1] / "scripts"
sys.path.insert(0, str(SCRIPTS_DIR))

from utils.schema_types import (  # noqa: E402
    CHANNEL_NAMES,
    ObservableSources,
    ObservedRecord,
    PrivilegedRecord,
    SUITE_CHANNELS,
    observable_sources,
    observed_registry_width,
)
from utils.sensor_model import FaultSpec, SensorConfig, SensorModel  # noqa: E402
from utils.synthetic_plant import synthetic_privileged_record  # noqa: E402
from run_sensor_model import indexed_plant_config_hash  # noqa: E402

SHARED_CHANNELS = ("q_obs", "qd_obs", "tau_cmd", "current_proxy_obs", "imu_obs")


def quiet_config(**overrides: float) -> SensorConfig:
    """A config with every stochastic pathology zeroed, for exact-effect tests."""

    base = SensorConfig(
        encoder_noise_rad=0.0,
        encoder_quant_rad=0.0,
        current_noise_floor_nm=0.0,
        current_noise_frac=0.0,
        current_bias_nm=0.0,
        imu_accel_noise=0.0,
        imu_gyro_noise=0.0,
        imu_accel_bias=0.0,
        imu_gyro_bias=0.0,
        gauge_noise_microstrain=0.0,
        gauge_bias_microstrain=0.0,
        gauge_drift_microstrain_per_rt_s=0.0,
        gauge_hysteresis_alpha=0.0,
        gauge_quant_microstrain=0.0,
        dropout_prob=0.0,
        thermal_microstrain_per_c=10.0,
        reference_temperature_c=25.0,
        gauge_latency_s=2.0e-3,
    )
    return dataclasses.replace(base, **overrides)


def small_record(**kwargs) -> PrivilegedRecord:
    """A short synthetic privileged trace for fast tests."""

    return synthetic_privileged_record(n_steps=200, f_ctrl=500.0, **kwargs)


def test_observed_registry_width_matches_schema() -> None:
    """The fixed observed registry is 2+2+2+2+6+4 = 18 scalar columns."""

    assert observed_registry_width() == 18


def test_observable_sources_excludes_privileged_only_fields() -> None:
    """The only doorway from privileged truth must not expose leakage-prone fields."""

    exposed = {f.name for f in dataclasses.fields(ObservableSources)}
    for forbidden in (
        "tau_delivered_true",
        "deform_coords",
        "curvature_true",
        "true_task_output",
        "tracking_error",
        "qd_true",
    ):
        assert forbidden not in exposed
    # And it does expose exactly the measurable sources.
    assert exposed == {
        "t_s",
        "q_true",
        "tau_cmd",
        "control_effort",
        "imu_true",
        "gauge_true",
        "temperature_true",
    }


def test_suite_masking_nan_and_available_channels() -> None:
    """C0/C1/S expose the right channels; absent channels are all-NaN and masked off."""

    record = small_record()
    model = SensorModel(quiet_config())
    for suite, expected in SUITE_CHANNELS.items():
        observed = model.observe(record, suite, pair_id=1, sensor_seed=3)
        assert observed.available_channels == tuple(
            name for name in CHANNEL_NAMES if name in expected
        )
        for name in CHANNEL_NAMES:
            present = name in expected
            assert observed.suite_available_mask[name] is present
            if not present:
                assert np.all(np.isnan(observed.values[name]))
                assert not np.any(observed.valid_mask[name])
    # A C1 record carries only NaN in the gauge slots -- no hidden gauge values.
    c1 = model.observe(record, "C1", pair_id=1, sensor_seed=3)
    assert np.all(np.isnan(c1.values["gauge_obs"]))


def test_common_random_numbers_shared_channels_match_across_pair() -> None:
    """C1 and S in a pair share exogenous seeds -> identical shared-channel draws.

    Feeding the same privileged record to both suites isolates the RNG-independence
    property: adding the S-only gauge channels must not perturb any shared channel.
    """

    record = small_record()
    model = SensorModel()  # default (noisy) config
    c1 = model.observe(record, "C1", pair_id=42, sensor_seed=9)
    s = model.observe(record, "S", pair_id=42, sensor_seed=9)
    for name in SHARED_CHANNELS:
        # assert_array_equal treats same-position NaNs as equal.
        np.testing.assert_array_equal(c1.values[name], s.values[name])
        np.testing.assert_array_equal(c1.valid_mask[name], s.valid_mask[name])
    # The gauge channel is the only difference: present in S, absent in C1.
    assert s.suite_available_mask["gauge_obs"]
    assert not c1.suite_available_mask["gauge_obs"]
    assert np.any(np.isfinite(s.values["gauge_obs"]))


def test_different_pairs_get_different_draws() -> None:
    """Distinct pair ids must produce distinct shared-channel noise realizations."""

    record = small_record()
    model = SensorModel()
    a = model.observe(record, "C1", pair_id=1, sensor_seed=5)
    b = model.observe(record, "C1", pair_id=2, sensor_seed=5)
    assert not np.allclose(a.values["q_obs"], b.values["q_obs"])


def test_thermal_apparent_strain_matches_coefficient() -> None:
    """With other pathologies off, gauge_obs - gauge_true == k_thermal * (T - T_ref)."""

    config = quiet_config(gauge_latency_s=0.0)
    record = small_record(thermal_ramp_c=8.0)
    model = SensorModel(config)
    observed = model.observe(record, "S", pair_id=1, sensor_seed=0)
    expected = config.thermal_microstrain_per_c * (
        record.temperature_true - config.reference_temperature_c
    )
    np.testing.assert_allclose(observed.values["gauge_obs"] - record.gauge_true, expected)


def test_encoder_fault_is_relational_only() -> None:
    """A sensor encoder bias corrupts q_obs only; gauge/IMU histories are untouched."""

    record = small_record()
    config = quiet_config()  # deterministic: q_obs = q_true (+ fault)
    model = SensorModel(config)
    healthy = model.observe(record, "S", pair_id=1, sensor_seed=0)
    fault = FaultSpec(
        source_class="sensor", subtype="encoder_bias", location=0, severity=0.05, onset_index=100
    )
    faulted = model.observe(record, "S", pair_id=1, sensor_seed=0, fault=fault)

    # Physical (independently evolved) channels are identical -- the lie doesn't deform.
    np.testing.assert_array_equal(healthy.values["gauge_obs"], faulted.values["gauge_obs"])
    np.testing.assert_array_equal(healthy.values["imu_obs"], faulted.values["imu_obs"])
    # The encoder disagrees with truth on the faulted joint only, after onset.
    delta = faulted.values["q_obs"] - healthy.values["q_obs"]
    assert np.allclose(delta[:100], 0.0)
    assert np.allclose(delta[100:, 0], 0.05)
    assert np.allclose(delta[:, 1], 0.0)


def test_structural_fault_does_not_change_the_observation_path() -> None:
    """Structural faults live in the plant; they must not alter sensor-model output."""

    record = small_record()
    model = SensorModel(quiet_config())
    healthy = model.observe(record, "S", pair_id=1, sensor_seed=0)
    structural = FaultSpec(source_class="structure", location=3, severity=0.5, onset_index=100)
    observed = model.observe(record, "S", pair_id=1, sensor_seed=0, fault=structural)
    np.testing.assert_array_equal(healthy.values["q_obs"], observed.values["q_obs"])
    np.testing.assert_array_equal(healthy.values["gauge_obs"], observed.values["gauge_obs"])


def test_encoder_dropout_fault_invalidates_samples() -> None:
    """An encoder dropout fault raises invalidity on the faulted joint after onset."""

    record = small_record()
    config = quiet_config()
    model = SensorModel(config)
    fault = FaultSpec(
        source_class="sensor", subtype="encoder_dropout", location=1, severity=0.9, onset_index=100
    )
    observed = model.observe(record, "C0", pair_id=1, sensor_seed=0, fault=fault)
    valid = observed.valid_mask["q_obs"]
    # Before onset (no baseline dropout in quiet config) all samples are valid.
    assert np.all(valid[:100])
    # After onset the faulted joint drops many samples, which are stored as NaN.
    assert valid[100:, 1].mean() < 0.5
    dropped = ~valid[:, 1]
    assert np.all(np.isnan(observed.values["q_obs"][dropped, 1]))


def test_qd_validity_requires_current_and_previous_encoder_samples() -> None:
    """A backward-difference velocity stays invalid for one step after q dropout."""

    record = small_record()
    fault = FaultSpec(
        source_class="sensor",
        subtype="encoder_dropout",
        location=1,
        severity=1.0,
        onset_index=100,
    )
    observed = SensorModel(quiet_config()).observe(
        record, "C0", pair_id=1, sensor_seed=0, fault=fault
    )
    q_valid = observed.valid_mask["q_obs"][:, 1]
    qd_valid = observed.valid_mask["qd_obs"][:, 1]
    expected = q_valid.copy()
    expected[1:] &= q_valid[:-1]
    np.testing.assert_array_equal(qd_valid, expected)
    assert np.all(np.isnan(observed.values["qd_obs"][~qd_valid, 1]))


def test_latency_gives_causal_availability_times() -> None:
    """availability_time = measurement_time + latency >= measurement_time (schema D)."""

    record = small_record()
    model = SensorModel(quiet_config(gauge_latency_s=0.004))
    observed = model.observe(record, "S", pair_id=1, sensor_seed=0)
    for name in observed.available_channels:
        avail = observed.availability_time_s[name]
        meas = observed.measurement_time_s[name]
        assert np.all(avail >= meas - 1e-12)
    gauge_latency = (
        observed.availability_time_s["gauge_obs"]
        - observed.measurement_time_s["gauge_obs"]
    )
    assert np.allclose(gauge_latency, 0.004)
    tau_latency = observed.availability_time_s["tau_cmd"] - observed.measurement_time_s["tau_cmd"]
    assert np.allclose(tau_latency, 0.0)


def test_qd_obs_is_causal_at_first_step() -> None:
    """qd_obs has no past at t=0, so its first sample is zero (past-only derivative)."""

    record = small_record()
    observed = SensorModel(quiet_config()).observe(record, "C0", pair_id=1, sensor_seed=0)
    assert np.all(observed.values["qd_obs"][0] == 0.0)


def test_determinism_same_inputs_same_output() -> None:
    """Identical (record, suite, pair_id, sensor_seed, fault) reproduce identical output."""

    record = small_record()
    model = SensorModel()
    first = model.observe(record, "S", pair_id=7, sensor_seed=11)
    second = model.observe(record, "S", pair_id=7, sensor_seed=11)
    for name in CHANNEL_NAMES:
        np.testing.assert_array_equal(first.values[name], second.values[name])


def test_observed_record_npz_round_trip(tmp_path: Path) -> None:
    """Saving and loading an ObservedRecord preserves values, masks, and timing."""

    record = small_record()
    observed = SensorModel().observe(
        record, "S", pair_id=3, sensor_seed=1, run_id="rt", config_hash="abc", split="dev"
    )
    path = tmp_path / "obs.npz"
    observed.save_npz(path)
    restored = ObservedRecord.load_npz(path)
    assert restored.suite == "S"
    assert restored.split == "dev"
    assert restored.config_hash == "abc"
    for name in CHANNEL_NAMES:
        np.testing.assert_array_equal(observed.values[name], restored.values[name])
        np.testing.assert_array_equal(observed.valid_mask[name], restored.valid_mask[name])


def test_observation_role_inherits_matching_plant_config_hash(tmp_path: Path) -> None:
    """A schema-E plant payload carries one role-shared hash into observations."""

    plant_root = tmp_path / "plant"
    plant_root.mkdir()
    payload = plant_root / "run.npz"
    payload.write_bytes(b"development fixture")
    (plant_root / "index.csv").write_text(
        "run_id,schema_version,config_hash,npz_path,sha256\n"
        "run,1.0,dev-shared,run.npz,unused\n",
        encoding="utf-8",
    )
    assert indexed_plant_config_hash(payload) == "dev-shared"


def test_invalid_fault_spec_fails_loud() -> None:
    """A sensor fault with an unknown subtype or bad location must raise."""

    import pytest

    with pytest.raises(ValueError):
        FaultSpec(source_class="sensor", subtype="nonsense", location=0).validate()
    with pytest.raises(ValueError):
        FaultSpec(source_class="sensor", subtype="encoder_bias", location=9).validate()
