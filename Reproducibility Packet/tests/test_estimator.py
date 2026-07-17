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
    EstimatorCommandPolicy,
    EstimatorOutput,
    EstimatorTrace,
    HEALTHY_INDEX,
    N_SOURCE_CLASSES,
    OracleInterface,
    RECOMMENDED_WINDOW,
    SOURCE_CLASS_ORDER,
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


# --------------------------------------------------------------------------- #
# Window front-end: suite-agnostic fixed shapes, NaN-safe features.
# --------------------------------------------------------------------------- #
def test_window_tensor_fixed_shape_across_suites():
    ext = WindowFeatureExtractor()
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


def test_window_features_shape_and_nan_safety():
    ext = WindowFeatureExtractor()
    assert ext.n_features == observed_registry_width() * (4 + 1)
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
    ext = WindowFeatureExtractor()
    feats = ext.window_features(rec).reshape(observed_registry_width(), 5)
    # column 0 == q_obs[:,0]: last=0.8, mean=0.4, slope=2.0, valid_frac=1.0
    assert feats[0, 0] == pytest.approx(0.8)
    assert feats[0, 1] == pytest.approx(0.4)
    assert feats[0, 3] == pytest.approx(2.0)
    assert feats[0, 4] == pytest.approx(1.0)


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
