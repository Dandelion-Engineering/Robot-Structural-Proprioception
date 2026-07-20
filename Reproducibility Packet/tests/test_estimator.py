"""Tests for the diagnosis-estimator lane (schema §D; Claude's lane).

Each test pins a defining property: the §D output contract's validation, the
suite-agnostic fixed shapes of the window front-end, the honest healthy-vs-not
behaviour of the detection/abstention rung (it detects change and declines the
fault-type call, never inventing an attribution), the oracle ceiling, and end-to-end
integration on the real causal online seam.
"""

from __future__ import annotations

import sys
from pathlib import Path

import numpy as np
import pytest

SCRIPTS_DIR = Path(__file__).resolve().parents[1] / "scripts"
sys.path.insert(0, str(SCRIPTS_DIR))

from utils.cable_plant import CablePlant  # noqa: E402
from utils.estimator import (  # noqa: E402
    DIAGNOSTIC_PROBE_HZ,
    EstimatorCommandPolicy,
    EstimatorOutput,
    EstimatorTrace,
    HEALTHY_INDEX,
    N_EXTRA_FEATURES,
    N_FEATURE_STATS,
    N_SOURCE_CLASSES,
    OracleInterface,
    RECOMMENDED_WINDOW,
    SOURCE_CLASS_ORDER,
    SYNC_AMPLITUDE_FEATURE_COL,
    SYNC_COS_FEATURE_COL,
    SYNC_SIN_FEATURE_COL,
    VALID_FRACTION_COL,
    WindowFeatureExtractor,
    WindowNoveltyDetector,
)
from utils.metrics import SOURCE_CLASS_ORDER as METRIC_ORDER  # noqa: E402
from utils.online_loop import run_online_rollout  # noqa: E402
from utils.schema_types import FaultSpec, N_JOINTS, observed_registry_width  # noqa: E402
from utils.sensor_model import OnlineSensorSession, SensorModel  # noqa: E402
from utils.synthetic_plant import synthetic_privileged_record  # noqa: E402


# --------------------------------------------------------------------------- #
# Helpers.
# --------------------------------------------------------------------------- #
def observed(
    suite: str,
    *,
    traj_seed: int = 0,
    sensor_seed: int = 0,
    fault: FaultSpec | None = None,
    n_steps: int = 80,
):
    """Build one deployable observed record from a synthetic privileged trace.

    `traj_seed` sets the commanded trajectory (phases); `sensor_seed` sets the noise
    realization. A healthy reference is a set of noise realizations of one trajectory,
    so a fault at the same trajectory reads as a clean deviation rather than being
    swamped by trajectory-to-trajectory differences.
    """

    rec = synthetic_privileged_record(n_steps=n_steps, f_ctrl=500.0, seed=traj_seed, thermal_ramp_c=3.0)
    return SensorModel().observe(rec, suite, pair_id=1, sensor_seed=sensor_seed, fault=fault)


def healthy_p_class() -> np.ndarray:
    p = np.zeros(N_SOURCE_CLASSES)
    p[HEALTHY_INDEX] = 1.0
    return p


# --------------------------------------------------------------------------- #
# §D output contract.
# --------------------------------------------------------------------------- #
def test_estimator_output_validates_good_and_rejects_bad():
    good = EstimatorOutput(0, 0.0, healthy_p_class(), unknown_score=0.0, abstain_decision=False)
    good.validate()  # no raise
    with pytest.raises(ValueError):
        EstimatorOutput(0, 0.0, np.array([0.5, 0.4, 0.0, 0.0]), 0.0, False).validate()  # sum != 1
    with pytest.raises(ValueError):
        EstimatorOutput(0, 0.0, np.array([1.0, 0.0, 0.0]), 0.0, False).validate()  # wrong shape
    with pytest.raises(ValueError):
        EstimatorOutput(0, 0.0, healthy_p_class(), np.inf, False).validate()  # non-finite score
    with pytest.raises(ValueError):
        EstimatorOutput(
            0, 0.0, healthy_p_class(), 0.0, False, severity_uncertainty=-1.0
        ).validate()  # negative uncertainty
    with pytest.raises(ValueError):
        EstimatorOutput(-1, 0.0, healthy_p_class(), 0.0, False).validate()
    with pytest.raises(ValueError):
        EstimatorOutput(0, np.nan, healthy_p_class(), 0.0, False).validate()
    with pytest.raises(ValueError):
        EstimatorOutput(
            0, 0.0, healthy_p_class(), 0.0, False, severity_uncertainty=np.nan
        ).validate()
    with pytest.raises(ValueError):
        EstimatorOutput(
            0, 0.0, healthy_p_class(), 0.0, False, detection_time_s=0.1
        ).validate()


def test_estimator_order_matches_metric_order():
    # The estimator's p_class columns must mean the same class the scorer expects.
    assert SOURCE_CLASS_ORDER == METRIC_ORDER


def test_estimator_trace_reductions():
    trace = EstimatorTrace(suite="S", run_id="r")
    trace.append(EstimatorOutput(0, 0.0, healthy_p_class(), 0.1, False))
    trace.append(EstimatorOutput(1, 0.01, healthy_p_class(), 0.2, False, detection_time_s=0.01))
    changed = np.array([0.1, 0.3, 0.3, 0.3])
    trace.append(EstimatorOutput(2, 0.02, changed, 3.0, True, detection_time_s=0.01))
    assert len(trace) == 3
    assert trace.detection_time_s == pytest.approx(0.01)
    assert np.allclose(trace.final_p_class(), changed)
    assert trace.final_abstain() is True
    stacked = trace.stack()
    assert stacked["p_class"].shape == (3, N_SOURCE_CLASSES)
    assert stacked["abstain_decision"].dtype == np.bool_
    with pytest.raises(ValueError):
        trace.append(EstimatorOutput(2, 0.03, changed, 3.0, True))


# --------------------------------------------------------------------------- #
# Window front-end: suite-agnostic fixed shapes, NaN-safe features.
# --------------------------------------------------------------------------- #
def test_window_tensor_fixed_shape_across_suites():
    ext = WindowFeatureExtractor(window_steps=80)
    width = observed_registry_width()
    shapes = set()
    valid_widths = {}
    for suite in ("C0", "C1", "S"):
        rec = observed(suite)
        values, valid = ext.window_tensor(rec)
        shapes.add(values.shape)
        assert values.shape == valid.shape
        valid_widths[suite] = int(valid.any(axis=0).sum())
    # Identical registry width for every suite (the ablation holds the estimator fixed).
    assert shapes == {(80, width)}
    # But S exposes strictly more live columns than C1, and C1 more than C0.
    assert valid_widths["S"] > valid_widths["C1"] > valid_widths["C0"]


def test_window_tensor_left_pads_startup_to_fixed_w():
    ext = WindowFeatureExtractor(window_steps=80)
    values, valid = ext.window_tensor(observed("C1", n_steps=12))
    assert values.shape == valid.shape == (80, observed_registry_width())
    assert not valid[:68].any()
    assert valid[68:].any()
    with pytest.raises(ValueError):
        ext.window_tensor(observed("C1", n_steps=81))


def test_window_features_shape_and_nan_safety():
    ext = WindowFeatureExtractor(window_steps=80)
    # per column: last, mean, std, slope, sync cos/sin/amplitude, valid fraction
    assert ext.n_features == observed_registry_width() * (4 + 4)
    feats_c0 = ext.window_features(observed("C0"))
    assert feats_c0.shape == (ext.n_features,)
    assert np.all(np.isfinite(feats_c0))  # never NaN even though gauges are absent


def test_window_features_last_mean_slope_known_values():
    # Build a tiny hand-made observed record with a linear q_obs channel so the
    # summary stats have known values.
    from utils.schema_types import CHANNEL_NAMES, CHANNEL_WIDTH, SUITE_CHANNELS, ObservedRecord

    t = 5
    times = np.arange(t) * 0.1  # 10 Hz for a clean slope
    values, valid, meas, avail, lat = {}, {}, {}, {}, {}
    for name in CHANNEL_NAMES:
        w = CHANNEL_WIDTH[name]
        values[name] = np.zeros((t, w))
        valid[name] = np.ones((t, w), dtype=bool) if name in SUITE_CHANNELS["C0"] else np.zeros((t, w), dtype=bool)
        meas[name] = times.copy()
        avail[name] = times.copy()
        lat[name] = np.zeros(t)
    # q_obs[:,0] = 2*t (slope 2/s over 0..0.4s), constant elsewhere
    values["q_obs"][:, 0] = 2.0 * times
    rec = ObservedRecord(
        suite="C0", run_id="r", pair_id="1", config_hash="dev-x",
        values=values, valid_mask=valid, measurement_time_s=meas,
        availability_time_s=avail, latency_age_s=lat,
        suite_available_mask={n: n in SUITE_CHANNELS["C0"] for n in CHANNEL_NAMES},
    )
    ext = WindowFeatureExtractor(window_steps=t)
    feats = ext.window_features(rec).reshape(observed_registry_width(), 8)
    # column 0 == q_obs[:,0]: last=0.8, mean=0.4, slope=2.0, valid_frac=1.0
    assert feats[0, 0] == pytest.approx(0.8)
    assert feats[0, 1] == pytest.approx(0.4)
    assert feats[0, 3] == pytest.approx(2.0)
    assert feats[0, VALID_FRACTION_COL] == pytest.approx(1.0)
    # all sync entries are 0: this 5-sample 0.4 s window spans < one 1.25 s cycle
    assert np.all(feats[0, SYNC_COS_FEATURE_COL : SYNC_AMPLITUDE_FEATURE_COL + 1] == 0.0)


def test_window_features_use_each_channels_measurement_times():
    from utils.schema_types import CHANNEL_NAMES, CHANNEL_WIDTH, SUITE_CHANNELS, ObservedRecord

    t = 5
    q_times = np.arange(t) * 0.1
    imu_times = np.arange(t) * 0.2
    values, valid, meas, avail, lat = {}, {}, {}, {}, {}
    for name in CHANNEL_NAMES:
        width = CHANNEL_WIDTH[name]
        values[name] = np.zeros((t, width))
        valid[name] = (
            np.ones((t, width), dtype=bool)
            if name in SUITE_CHANNELS["C1"]
            else np.zeros((t, width), dtype=bool)
        )
        meas[name] = q_times.copy()
        avail[name] = q_times.copy()
        lat[name] = np.zeros(t)
    meas["imu_obs"] = imu_times.copy()
    avail["imu_obs"] = imu_times.copy()
    values["imu_obs"][:, 0] = 3.0 * imu_times
    rec = ObservedRecord(
        suite="C1",
        run_id="r",
        pair_id="1",
        config_hash="dev-x",
        values=values,
        valid_mask=valid,
        measurement_time_s=meas,
        availability_time_s=avail,
        latency_age_s=lat,
        suite_available_mask={n: n in SUITE_CHANNELS["C1"] for n in CHANNEL_NAMES},
    )
    ext = WindowFeatureExtractor(window_steps=t)
    feats = ext.window_features(rec).reshape(observed_registry_width(), 8)
    imu_offset = sum(CHANNEL_WIDTH[name] for name in CHANNEL_NAMES[:4])
    assert feats[imu_offset, 3] == pytest.approx(3.0)


# --------------------------------------------------------------------------- #
# Synchronous (lock-in) window feature at the probe frequency.
# --------------------------------------------------------------------------- #
def _single_tone_record(channel: str, times: np.ndarray, signal: np.ndarray, suite: str):
    """Hand-build an ObservedRecord carrying `signal` on `channel[:,0]` over `times`.

    Every channel in `suite` is fully valid; only `channel[:,0]` carries the signal, so
    the tests read a known per-column synchronous amplitude. `times` is that channel's
    own measurement grid; all others share `times` unless the test overrides them.
    """

    from utils.schema_types import CHANNEL_NAMES, CHANNEL_WIDTH, SUITE_CHANNELS, ObservedRecord

    t = times.shape[0]
    values, valid, meas, avail, lat = {}, {}, {}, {}, {}
    for name in CHANNEL_NAMES:
        w = CHANNEL_WIDTH[name]
        values[name] = np.zeros((t, w))
        valid[name] = (
            np.ones((t, w), dtype=bool)
            if name in SUITE_CHANNELS[suite]
            else np.zeros((t, w), dtype=bool)
        )
        meas[name] = times.copy()
        avail[name] = times.copy()
        lat[name] = np.zeros(t)
    values[channel][:, 0] = signal
    rec = ObservedRecord(
        suite=suite, run_id="r", pair_id="1", config_hash="dev-x",
        values=values, valid_mask=valid, measurement_time_s=meas,
        availability_time_s=avail, latency_age_s=lat,
        suite_available_mask={n: n in SUITE_CHANNELS[suite] for n in CHANNEL_NAMES},
    )
    return rec, meas, values


def test_recommended_window_covers_one_probe_cycle():
    # The synchronous feature needs the window to span a full probe period, so the default
    # W at 500 Hz must cover at least one 0.8 Hz cycle (1.25 s = 625 samples). This is the
    # concrete reason the S9 co-design moved W from 512 to 640.
    span_s = (RECOMMENDED_WINDOW.W - 1) / 500.0
    assert span_s + 1.0e-9 >= 1.0 / DIAGNOSTIC_PROBE_HZ


def test_synchronous_feature_recovers_probe_tone_phase_invariant():
    t = 80
    times = np.arange(t) * 0.02  # 50 Hz grid: one 0.8 Hz period (1.25 s) spans 62.5 < 80
    amp = 5.0
    per_col = N_FEATURE_STATS + N_EXTRA_FEATURES
    recovered = []
    for phase in (0.0, 1.1, 2.7, 4.5):
        signal = amp * np.cos(2.0 * np.pi * DIAGNOSTIC_PROBE_HZ * times + phase)
        rec, _, _ = _single_tone_record("q_obs", times, signal, "C0")
        ext = WindowFeatureExtractor(window_steps=t, probe_frequency_hz=DIAGNOSTIC_PROBE_HZ)
        feats = ext.window_features(rec).reshape(observed_registry_width(), per_col)
        recovered.append(feats[0, SYNC_AMPLITUDE_FEATURE_COL])
        assert feats[0, VALID_FRACTION_COL] == pytest.approx(1.0)
    for r in recovered:
        assert r == pytest.approx(amp, rel=1.0e-6)  # recovers the injected amplitude
    assert max(recovered) - min(recovered) < 1.0e-9  # phase invariant


def test_synchronous_feature_zero_below_one_period():
    t = 20
    times = np.arange(t) * 0.02  # span 0.38 s < one 1.25 s probe period -> gate not met
    signal = 5.0 * np.cos(2.0 * np.pi * DIAGNOSTIC_PROBE_HZ * times)
    rec, _, _ = _single_tone_record("q_obs", times, signal, "C0")
    ext = WindowFeatureExtractor(window_steps=t, probe_frequency_hz=DIAGNOSTIC_PROBE_HZ)
    feats = ext.window_features(rec).reshape(
        observed_registry_width(), N_FEATURE_STATS + N_EXTRA_FEATURES
    )
    assert feats[0, SYNC_COS_FEATURE_COL] == 0.0
    assert feats[0, SYNC_SIN_FEATURE_COL] == 0.0
    assert feats[0, SYNC_AMPLITUDE_FEATURE_COL] == 0.0


def test_synchronous_feature_uses_each_channel_grid():
    from utils.schema_types import CHANNEL_NAMES, CHANNEL_WIDTH

    t = 96
    q_times = np.arange(t) * 0.02
    imu_times = np.arange(t) * 0.03  # imu_obs samples on its own coarser grid
    amp = 4.0
    imu_signal = amp * np.cos(2.0 * np.pi * DIAGNOSTIC_PROBE_HZ * imu_times)
    rec, meas, values = _single_tone_record("q_obs", q_times, np.zeros(t), "C1")
    # override imu_obs to sit on its own grid and carry the tone
    meas["imu_obs"] = imu_times.copy()
    rec.availability_time_s["imu_obs"] = imu_times.copy()
    values["imu_obs"][:, 0] = imu_signal
    ext = WindowFeatureExtractor(window_steps=t, probe_frequency_hz=DIAGNOSTIC_PROBE_HZ)
    feats = ext.window_features(rec).reshape(
        observed_registry_width(), N_FEATURE_STATS + N_EXTRA_FEATURES
    )
    imu_offset = sum(CHANNEL_WIDTH[name] for name in CHANNEL_NAMES[:4])
    # the imu tone is recovered on the imu grid; the flat q_obs reads zero amplitude
    assert feats[imu_offset, SYNC_AMPLITUDE_FEATURE_COL] == pytest.approx(amp, rel=1.0e-6)
    assert feats[0, SYNC_AMPLITUDE_FEATURE_COL] == 0.0


def test_synchronous_feature_retains_phase_not_only_amplitude():
    """Equal amplitudes with different phase remain distinguishable in coefficient space."""

    t = 80
    times = np.arange(t) * 0.02
    amplitude = 5.0
    per_col = N_FEATURE_STATS + N_EXTRA_FEATURES
    phase_0 = amplitude * np.cos(2.0 * np.pi * DIAGNOSTIC_PROBE_HZ * times)
    phase_90 = amplitude * np.cos(
        2.0 * np.pi * DIAGNOSTIC_PROBE_HZ * times + np.pi / 2.0
    )
    rec_0, _, _ = _single_tone_record("q_obs", times, phase_0, "C0")
    rec_90, _, _ = _single_tone_record("q_obs", times, phase_90, "C0")
    ext = WindowFeatureExtractor(window_steps=t, probe_frequency_hz=DIAGNOSTIC_PROBE_HZ)
    feat_0 = ext.window_features(rec_0).reshape(observed_registry_width(), per_col)[0]
    feat_90 = ext.window_features(rec_90).reshape(observed_registry_width(), per_col)[0]

    assert feat_0[SYNC_AMPLITUDE_FEATURE_COL] == pytest.approx(amplitude, rel=1.0e-6)
    assert feat_90[SYNC_AMPLITUDE_FEATURE_COL] == pytest.approx(amplitude, rel=1.0e-6)
    coefficient_delta = (
        feat_0[[SYNC_COS_FEATURE_COL, SYNC_SIN_FEATURE_COL]]
        - feat_90[[SYNC_COS_FEATURE_COL, SYNC_SIN_FEATURE_COL]]
    )
    assert np.linalg.norm(coefficient_delta) == pytest.approx(
        amplitude * np.sqrt(2.0), rel=1.0e-6
    )


def test_synchronous_feature_lifts_novelty_on_probe_amplitude_change():
    # A change confined to the probe-frequency amplitude (structure/actuator signature)
    # raises the interpretable detector's novelty via the synchronous feature.
    rng = np.random.default_rng(0)
    t = 96
    times = np.arange(t) * 0.02
    base_amp = 2.0

    def tone_record(amp: float, seed_noise: np.ndarray):
        signal = amp * np.cos(2.0 * np.pi * DIAGNOSTIC_PROBE_HZ * times) + seed_noise
        rec, _, _ = _single_tone_record("q_obs", times, signal, "C0")
        return rec

    ext = WindowFeatureExtractor(window_steps=t, probe_frequency_hz=DIAGNOSTIC_PROBE_HZ)
    det = WindowNoveltyDetector(ext, detect_threshold=4.0, abstain_threshold=2.5)
    healthy = [tone_record(base_amp, 0.01 * rng.standard_normal(t)) for _ in range(8)]
    det.fit_reference(healthy)
    fresh = det.novelty_score(tone_record(base_amp, 0.01 * rng.standard_normal(t)))
    changed = det.novelty_score(tone_record(base_amp + 3.0, 0.01 * rng.standard_normal(t)))
    assert np.isfinite(fresh)
    assert changed > fresh  # the probe-band amplitude jump is picked up


# --------------------------------------------------------------------------- #
# Detection + calibrated-abstention rung.
# --------------------------------------------------------------------------- #
def test_novelty_requires_reference_before_scoring():
    det = WindowNoveltyDetector()
    with pytest.raises(ValueError):
        det.novelty_score(observed("S"))


def test_novelty_low_on_healthy_high_on_change():
    ext = WindowFeatureExtractor()
    det = WindowNoveltyDetector(ext)
    # reference = noise realizations of ONE trajectory
    healthy = [observed("C1", traj_seed=0, sensor_seed=s) for s in range(8)]
    det.fit_reference(healthy)
    # a fresh healthy realization of the same trajectory scores modestly...
    fresh_healthy = det.novelty_score(observed("C1", traj_seed=0, sensor_seed=99))
    # ...an encoder-bias fault on the same trajectory scores far higher.
    biased = observed(
        "C1", traj_seed=0, sensor_seed=99,
        fault=FaultSpec(source_class="sensor", subtype="encoder_bias", location=0,
                        severity=0.3, onset_index=0),
    )
    changed = det.novelty_score(biased)
    assert np.isfinite(fresh_healthy)
    assert changed > fresh_healthy
    assert changed >= det.detect_threshold


def test_novelty_detection_latches_after_persistence():
    ext = WindowFeatureExtractor()
    det = WindowNoveltyDetector(ext, detect_threshold=4.0, abstain_threshold=2.5, persistence=3)
    det.fit_reference([observed("C1", traj_seed=0, sensor_seed=s) for s in range(8)])
    biased = observed(
        "C1", traj_seed=0, sensor_seed=7,
        fault=FaultSpec(source_class="sensor", subtype="encoder_bias", location=0,
                        severity=0.4, onset_index=0),
    )
    # Two healthy decisions, then repeated changed decisions: detection latches on the
    # 3rd consecutive over-threshold window, not before.
    det.update(0, 0.0, observed("C1", traj_seed=0, sensor_seed=1))
    det.update(1, 0.01, observed("C1", traj_seed=0, sensor_seed=2))
    assert not np.isfinite(det.update(2, 0.02, biased).detection_time_s)
    assert not np.isfinite(det.update(3, 0.03, biased).detection_time_s)
    latched = det.update(4, 0.04, biased)
    assert latched.detection_time_s == pytest.approx(0.04)
    # once latched, detection time is stable
    assert det.update(5, 0.05, biased).detection_time_s == pytest.approx(0.04)


def test_novelty_output_is_honest_healthy_vs_not():
    det = WindowNoveltyDetector()
    det.fit_reference([observed("S", traj_seed=0, sensor_seed=s) for s in range(10)])
    # None window -> confident healthy, no abstain, no detection
    out0 = det.update(0, 0.0, None)
    out0.validate()
    assert out0.p_class[HEALTHY_INDEX] == pytest.approx(1.0)
    assert out0.abstain_decision is False
    # a fresh healthy window -> healthy-dominant simplex, no abstain
    healthy_out = det.update(1, 0.01, observed("S", traj_seed=0, sensor_seed=42))
    healthy_out.validate()
    assert np.argmax(healthy_out.p_class) == HEALTHY_INDEX
    assert healthy_out.abstain_decision is False
    # a strongly changed window -> abstains on the fault type and spreads non-healthy
    # mass uniformly (no structure/actuator/sensor attribution claimed)
    biased = observed(
        "S", traj_seed=0, sensor_seed=42,
        fault=FaultSpec(source_class="sensor", subtype="encoder_bias", location=0,
                        severity=0.5, onset_index=0),
    )
    out = det.update(2, 0.02, biased)
    out.validate()
    assert out.abstain_decision is True
    assert out.location_out == -1  # not localized without a trained head
    fault_probs = out.p_class[list(range(1, N_SOURCE_CLASSES))]
    assert np.allclose(fault_probs, fault_probs[0])  # uniform over fault classes


# --------------------------------------------------------------------------- #
# Oracle ceiling.
# --------------------------------------------------------------------------- #
def test_oracle_reports_true_class():
    rec = synthetic_privileged_record(n_steps=10, f_ctrl=500.0, seed=0)
    state = rec.slice_step(5)
    oracle = OracleInterface(true_source_index=2, location=1, severity=0.4)  # actuator
    out = oracle.update(5, state)
    out.validate()
    assert np.argmax(out.p_class) == 2
    assert out.p_class[2] == pytest.approx(1.0)
    assert out.location_out == 1
    assert np.isfinite(out.detection_time_s)  # a fault is detected immediately
    # healthy oracle does not "detect"
    healthy_out = OracleInterface(true_source_index=HEALTHY_INDEX).update(5, state)
    assert not np.isfinite(healthy_out.detection_time_s)


def test_oracle_does_not_expose_fault_before_onset():
    rec = synthetic_privileged_record(n_steps=10, f_ctrl=500.0, seed=0)
    oracle = OracleInterface(
        true_source_index=2, location=1, severity=0.4, onset_time_s=0.012
    )
    before = oracle.update(4, rec.slice_step(4))
    after = oracle.update(7, rec.slice_step(7))
    assert np.argmax(before.p_class) == HEALTHY_INDEX
    assert before.location_out == -1
    assert not np.isfinite(before.detection_time_s)
    assert np.argmax(after.p_class) == 2
    assert after.detection_time_s == pytest.approx(0.012)


# --------------------------------------------------------------------------- #
# Online-seam integration (real cable plant).
# --------------------------------------------------------------------------- #
def test_estimator_command_policy_drives_online_seam():
    det = WindowNoveltyDetector()
    det.fit_reference([observed("C1", traj_seed=0, sensor_seed=s, n_steps=60) for s in range(4)])
    plant = CablePlant()
    sess = OnlineSensorSession("C1", pair_id=1, sensor_seed=5, control_dt_s=plant.config.control_dt_s)
    policy = EstimatorCommandPolicy(det, suite="C1", run_id="online", stride=4)
    n_steps = 12
    result = run_online_rollout(plant, sess, n_steps=n_steps, history_steps=RECOMMENDED_WINDOW.stride * 3,
                                command_policy=policy)
    # a valid role-separated rollout came back
    assert result.plant.n_steps == result.observations.n_steps == n_steps
    # the estimator ran once per stride window and every emitted output is contract-valid
    expected_updates = len([s for s in range(n_steps) if s % 4 == 0])
    assert len(policy.trace) == expected_updates
    for out in policy.trace.outputs:
        out.validate()
    # trace stacks into §E-shaped arrays
    stacked = policy.trace.stack()
    assert stacked["p_class"].shape == (expected_updates, N_SOURCE_CLASSES)


def test_estimator_outputs_feed_metrics_scorer():
    """The §D outputs the estimator produces are exactly what utils.metrics consumes."""

    from utils.metrics import (
        macro_f1,
        ood_auroc,
        resolve_predictions,
        coverage_at_risk,
    )

    # Six runs: three healthy (confident healthy, no abstain), three detected changes
    # (abstain on the fault type). This is the honest detector's behaviour at run level.
    def healthy_out(step):
        p = np.zeros(N_SOURCE_CLASSES); p[HEALTHY_INDEX] = 0.9
        p[1:] = 0.1 / 3
        return EstimatorOutput(step, 0.0, p, unknown_score=0.5, abstain_decision=False)

    def changed_out(step):
        p = np.zeros(N_SOURCE_CLASSES); p[HEALTHY_INDEX] = 0.05
        p[1:] = 0.95 / 3
        return EstimatorOutput(step, 0.0, p, unknown_score=6.0, abstain_decision=True)

    # sixth run is a held-out compound (OOD) with a distinctly higher novelty score.
    ood = EstimatorOutput(5, 0.0, changed_out(5).p_class, unknown_score=9.0, abstain_decision=True)
    outs = [healthy_out(0), healthy_out(1), healthy_out(2), changed_out(3), changed_out(4), ood]
    p_stack = np.stack([o.p_class for o in outs])
    abstain = np.array([o.abstain_decision for o in outs])
    y_true = np.array([0, 0, 0, 1, 2, 3])  # healthy x3, then structure/actuator/sensor
    resolved = resolve_predictions(p_stack, abstain)
    # healthy runs resolve to healthy; changed runs abstain (scored as error headline)
    assert list(resolved[:3]) == [HEALTHY_INDEX] * 3
    assert np.all(resolved[3:] == -1)
    score = macro_f1(y_true, resolved)  # runs without interface error
    assert 0.0 <= score <= 1.0
    # unknown_score ranks the held-out compound (OOD) above the in-distribution runs.
    ood_flag = np.array([False, False, False, False, False, True])
    unknown = np.array([o.unknown_score for o in outs])
    assert ood_auroc(ood_flag, unknown) == pytest.approx(1.0)  # OOD run has the top score
    # coverage_at_risk consumes the confidence (top prob) the estimator emits
    confidence = p_stack.max(axis=1)
    hard = p_stack.argmax(axis=1)
    cov = coverage_at_risk(y_true, hard, confidence, risk_ceiling=0.5)
    assert 0.0 <= cov <= 1.0


def test_recommended_window_is_past_only_and_sane():
    assert RECOMMENDED_WINDOW.W > 0 and RECOMMENDED_WINDOW.stride > 0
    assert RECOMMENDED_WINDOW.stride <= RECOMMENDED_WINDOW.W
    assert "500 Hz" in RECOMMENDED_WINDOW.rationale or "500" in RECOMMENDED_WINDOW.rationale
