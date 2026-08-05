"""Tests for Gate-4 rung 1, the matched learned temporal-attribution head.

Each test pins one property the matched C0/C1/S ablation or the schema-§D output
contract depends on, and the properties are chosen for how they would fail *silently*:

  * **capacity** — the parameter count sits in Slot 9's rung-1 band, and a
    configuration outside it is refused rather than climbing the ladder by edit;
  * **causality** — measured by perturbation, not asserted from the architecture, and
    checked separately for the normalization, which is where a `GroupNorm` would mix
    a window's future into its past without changing any shape;
  * **suite invariance** — identical parameter count and identical shapes for C0, C1
    and S, so a measured S-over-C1 advantage cannot be model capacity;
  * **honest defaults** — an unfitted estimator abstains, reports uniform `p_class`,
    `location_out = -1`, `severity_uncertainty = +inf`, and never flags a detection;
  * **deployable/privileged boundary** — this module reads observed records only, and
    a source-level check pins that it imports no privileged type.
"""

from __future__ import annotations

import sys
from pathlib import Path

import numpy as np
import pytest
import torch

SCRIPTS_DIR = Path(__file__).resolve().parents[1] / "scripts"
sys.path.insert(0, str(SCRIPTS_DIR))

from utils.attribution_net import (  # noqa: E402
    CAPACITY_LADDER,
    NOT_LOCALIZED_INDEX,
    N_INPUT_STREAMS,
    N_LOCATION_LOGITS,
    RUNG1_MAX_PARAMETERS,
    RUNG1_MIN_PARAMETERS,
    TemporalAttributionEstimator,
    TemporalAttributionNet,
    _CausalDilatedBlock,
    _PerStepChannelNorm,
    deterministic_conv_precision,
    window_to_input,
)
from utils.estimator import (  # noqa: E402
    HEALTHY_INDEX,
    N_SOURCE_CLASSES,
    SOURCE_CLASS_ORDER,
    WindowFeatureExtractor,
)
from utils.schema_types import (  # noqa: E402
    CHANNEL_NAMES,
    CHANNEL_WIDTH,
    N_JOINTS,
    SUITE_CHANNELS,
    ObservedRecord,
    observed_registry_width,
)

D = observed_registry_width()


# --------------------------------------------------------------------------- #
# Shared fixtures.
# --------------------------------------------------------------------------- #
def _record(suite: str, t: int = 40, *, seed: int = 0) -> ObservedRecord:
    """Build a fully-valid `t`-step observed record for `suite` with pseudo signals.

    Channels the suite lacks are all-NaN and masked off, exactly as the real sensor
    model emits them, so the window front-end sees the same missing pattern a real
    C0 or C1 record carries.
    """

    rng = np.random.default_rng(seed)
    times = np.arange(t, dtype=float) * 0.002
    values, valid, meas, avail, lat = {}, {}, {}, {}, {}
    for name in CHANNEL_NAMES:
        width = CHANNEL_WIDTH[name]
        present = name in SUITE_CHANNELS[suite]
        if present:
            values[name] = rng.normal(size=(t, width))
            valid[name] = np.ones((t, width), dtype=bool)
        else:
            values[name] = np.full((t, width), np.nan)
            valid[name] = np.zeros((t, width), dtype=bool)
        meas[name] = times.copy()
        avail[name] = times.copy()
        lat[name] = np.zeros(t, dtype=float)
    return ObservedRecord(
        suite=suite,
        run_id="r",
        pair_id="1",
        config_hash="dev-x",
        values=values,
        valid_mask=valid,
        measurement_time_s=meas,
        availability_time_s=avail,
        latency_age_s=lat,
        suite_available_mask={n: n in SUITE_CHANNELS[suite] for n in CHANNEL_NAMES},
    )


def _small_net(**kwargs) -> TemporalAttributionNet:
    """A cheap net for tests that only need shapes/causality, not the shipped capacity."""

    params = dict(channels=8, n_blocks=3, seed=0, enforce_rung1_band=False)
    params.update(kwargs)
    return TemporalAttributionNet(**params)


def _fitted(net: TemporalAttributionNet, extractor: WindowFeatureExtractor, **kwargs):
    """An estimator with `net`'s own weights attached under a test provenance string."""

    est = TemporalAttributionEstimator(net, extractor, **kwargs)
    est.attach_trained_weights(net.state_dict(), training_provenance="unit-test synthetic weights")
    return est


# --------------------------------------------------------------------------- #
# Capacity: Slot 9's rung-1 band, and the refusal that keeps the ladder honest.
# --------------------------------------------------------------------------- #
def test_default_configuration_sits_in_the_rung1_parameter_band():
    net = TemporalAttributionNet()
    assert RUNG1_MIN_PARAMETERS <= net.n_parameters <= RUNG1_MAX_PARAMETERS


def test_a_configuration_above_the_band_is_refused_by_construction():
    with pytest.raises(ValueError, match="outside Slot 9's rung-1 band"):
        TemporalAttributionNet(channels=256, n_blocks=9)


def test_a_configuration_below_the_band_is_refused_by_construction():
    with pytest.raises(ValueError, match="outside Slot 9's rung-1 band"):
        TemporalAttributionNet(channels=2, n_blocks=1)


def test_the_band_check_can_be_waived_only_explicitly():
    net = TemporalAttributionNet(channels=2, n_blocks=1, enforce_rung1_band=False)
    assert net.n_parameters < RUNG1_MIN_PARAMETERS


def test_capacity_ladder_records_exactly_one_built_rung_and_it_is_rung_one():
    built = [rung for rung in CAPACITY_LADDER if rung.built]
    assert len(built) == 1
    assert built[0].name == "rung1_compact_temporal_conv"
    assert all(rung.escalate_when.strip() for rung in CAPACITY_LADDER)


def test_the_shipped_receptive_field_covers_the_proposed_window():
    from utils.estimator import RECOMMENDED_WINDOW

    assert TemporalAttributionNet().receptive_field >= RECOMMENDED_WINDOW.W


# --------------------------------------------------------------------------- #
# Causality — measured, not asserted.
# --------------------------------------------------------------------------- #
def _feature_response(net: TemporalAttributionNet, t: int, perturb_at: int) -> np.ndarray:
    """Return, per time index, whether the encoder feature moved when input `perturb_at` did."""

    torch.manual_seed(7)
    base = torch.randn(1, N_INPUT_STREAMS * net.registry_width, t)
    perturbed = base.clone()
    perturbed[0, :, perturb_at] += 5.0
    with torch.no_grad():
        a = net.encode(base)[0]
        b = net.encode(perturbed)[0]
    return (a - b).abs().max(dim=0).values.numpy()


def test_no_encoder_feature_depends_on_a_later_input():
    net = _small_net()
    t, j = 32, 20
    moved = _feature_response(net, t, j)
    assert np.all(moved[:j] == 0.0), "an input at t=j changed a feature at t<j (not causal)"
    assert moved[j] > 0.0, "an input at t=j did not reach its own timestep"


def test_the_measured_receptive_field_equals_the_declared_one():
    net = _small_net(n_blocks=3, kernel_size=3)  # declared 1 + 2*(2**3 - 1) = 15
    t = 64
    j = t - 1
    # Perturb the final input and ask how far back the *feature at t-1* would have seen:
    # equivalently, perturb input j and count how many later features moved.
    moved = _feature_response(net, t, 24)
    reached = np.flatnonzero(moved > 0.0)
    assert reached[0] == 24
    assert int(reached[-1] - reached[0] + 1) == net.receptive_field
    assert net.receptive_field == 1 + (net.kernel_size - 1) * (2**net.n_blocks - 1)
    assert j == t - 1  # the final timestep is the one the heads read


def test_per_step_norm_does_not_mix_across_time():
    norm = _PerStepChannelNorm(6)
    torch.manual_seed(3)
    base = torch.randn(1, 6, 12)
    perturbed = base.clone()
    perturbed[0, :, 7] += 9.0
    with torch.no_grad():
        delta = (norm(base) - norm(perturbed)).abs().max(dim=1).values[0]
    assert torch.all(delta[:7] == 0.0)
    assert torch.all(delta[8:] == 0.0)
    assert delta[7] > 0.0


def test_a_time_mixing_normalization_would_fail_the_same_check():
    """The causality check is sharp: a GroupNorm in the same slot fails it.

    Without this, the two preceding tests could be passing because the perturbation is
    too small to see rather than because the normalization is per-timestep.
    """

    norm = torch.nn.GroupNorm(1, 6)
    torch.manual_seed(3)
    base = torch.randn(1, 6, 12)
    perturbed = base.clone()
    perturbed[0, :, 7] += 9.0
    with torch.no_grad():
        delta = (norm(base) - norm(perturbed)).abs().max(dim=1).values[0]
    assert torch.any(delta[:7] > 0.0)


def test_causal_block_left_pads_and_preserves_length():
    block = _CausalDilatedBlock(4, 3, 4)
    x = torch.randn(2, 4, 30)
    with torch.no_grad():
        assert block(x).shape == x.shape
    assert block.left_pad == (3 - 1) * 4


def test_causal_block_refuses_degenerate_geometry():
    with pytest.raises(ValueError, match="kernel_size"):
        _CausalDilatedBlock(4, 0, 1)
    with pytest.raises(ValueError, match="dilation"):
        _CausalDilatedBlock(4, 3, 0)


# --------------------------------------------------------------------------- #
# Suite invariance — the property the whole ablation rests on.
# --------------------------------------------------------------------------- #
@pytest.mark.parametrize("suite", ["C0", "C1", "S"])
def test_window_tensor_to_network_wire_runs_for_every_suite(suite):
    extractor = WindowFeatureExtractor(window_steps=40)
    net = _small_net()
    values, valid = extractor.window_tensor(_record(suite))
    batch = window_to_input(values, valid)
    assert batch.shape == (1, N_INPUT_STREAMS * D, 40)
    with torch.no_grad():
        heads = net(batch)
    assert heads.class_logits.shape == (1, N_SOURCE_CLASSES)
    assert heads.location_logits.shape == (1, N_LOCATION_LOGITS)
    assert heads.unknown_logit.shape == (1,)
    assert torch.all(torch.isfinite(heads.class_logits))


def test_parameter_count_and_shape_do_not_depend_on_the_suite():
    """A suite enters only through the mask; nothing about the model may change."""

    extractor = WindowFeatureExtractor(window_steps=40)
    net = _small_net()
    before = net.n_parameters
    shapes = set()
    for suite in ("C0", "C1", "S"):
        values, valid = extractor.window_tensor(_record(suite))
        shapes.add(window_to_input(values, valid).shape)
    assert len(shapes) == 1
    assert net.n_parameters == before


def test_channels_a_suite_lacks_arrive_as_zero_value_and_false_mask():
    extractor = WindowFeatureExtractor(window_steps=40)
    values, valid = extractor.window_tensor(_record("C1"))
    batch = window_to_input(values, valid)[0]
    gauge_offset = sum(CHANNEL_WIDTH[name] for name in CHANNEL_NAMES[:-1])
    gauge_cols = slice(gauge_offset, gauge_offset + CHANNEL_WIDTH["gauge_obs"])
    assert torch.all(batch[gauge_cols] == 0.0)
    mask_cols = slice(D + gauge_offset, D + gauge_offset + CHANNEL_WIDTH["gauge_obs"])
    assert torch.all(batch[mask_cols] == 0.0)


def test_the_suite_difference_is_visible_to_the_network():
    """S and C1 windows differ in the input the net receives — otherwise nothing to measure."""

    extractor = WindowFeatureExtractor(window_steps=40)
    s_values, s_valid = extractor.window_tensor(_record("S"))
    c1_values, c1_valid = extractor.window_tensor(_record("C1"))
    assert not np.array_equal(s_valid, c1_valid)
    net = _small_net()
    with torch.no_grad():
        s_out = net(window_to_input(s_values, s_valid)).class_logits
        c1_out = net(window_to_input(c1_values, c1_valid)).class_logits
    assert not torch.equal(s_out, c1_out)


# --------------------------------------------------------------------------- #
# `window_to_input` fails loudly rather than broadcasting a wrong window.
# --------------------------------------------------------------------------- #
def test_window_to_input_carries_the_mask_as_its_second_half():
    values = np.arange(12, dtype=float).reshape(4, 3)
    valid = np.array([[True, False, True]] * 4)
    batch = window_to_input(values, valid)
    assert batch.shape == (1, 6, 4)
    assert torch.allclose(batch[0, :3], torch.as_tensor(values.T, dtype=torch.float32))
    assert torch.equal(batch[0, 3:], torch.as_tensor(valid.T.astype(np.float32)))


def test_window_to_input_refuses_mismatched_shapes():
    with pytest.raises(ValueError, match="share shape"):
        window_to_input(np.zeros((4, 3)), np.zeros((4, 2), dtype=bool))


def test_window_to_input_refuses_a_non_two_dimensional_window():
    with pytest.raises(ValueError, match=r"\[W, D\]"):
        window_to_input(np.zeros(4), np.zeros(4, dtype=bool))


def test_window_to_input_refuses_a_non_finite_value():
    values = np.zeros((4, 3))
    values[2, 1] = np.nan
    with pytest.raises(ValueError, match="finite"):
        window_to_input(values, np.ones((4, 3), dtype=bool))


def test_network_refuses_a_wrong_stream_count():
    net = _small_net()
    with pytest.raises(ValueError, match="streams"):
        net.encode(torch.zeros(1, 5, 20))


def test_network_refuses_a_non_batched_input():
    net = _small_net()
    with pytest.raises(ValueError, match=r"\[B, 2D, T\]"):
        net.encode(torch.zeros(N_INPUT_STREAMS * net.registry_width, 20))


# --------------------------------------------------------------------------- #
# Determinism.
# --------------------------------------------------------------------------- #
def test_two_networks_at_the_same_seed_are_bit_identical():
    a, b = _small_net(seed=5), _small_net(seed=5)
    assert all(torch.equal(p, q) for p, q in zip(a.parameters(), b.parameters()))
    x = torch.randn(1, N_INPUT_STREAMS * a.registry_width, 24)
    with torch.no_grad():
        assert torch.equal(a(x).class_logits, b(x).class_logits)


def test_two_networks_at_different_seeds_differ():
    a, b = _small_net(seed=5), _small_net(seed=6)
    assert any(not torch.equal(p, q) for p, q in zip(a.parameters(), b.parameters()))


def test_construction_does_not_consume_the_global_rng():
    """Building a net must not shift anyone else's draw sequence."""

    torch.manual_seed(11)
    expected = torch.randn(4)
    torch.manual_seed(11)
    _small_net(seed=99)
    assert torch.equal(torch.randn(4), expected)


def test_forward_is_repeatable_within_one_instance():
    net = _small_net()
    x = torch.randn(1, N_INPUT_STREAMS * net.registry_width, 24)
    with torch.no_grad():
        assert torch.equal(net(x).class_logits, net(x).class_logits)


def test_seed_must_be_a_non_negative_integer():
    with pytest.raises(ValueError, match="seed"):
        _small_net(seed=-1)


# --------------------------------------------------------------------------- #
# The honest defaults of an unfitted estimator.
# --------------------------------------------------------------------------- #
def test_a_fresh_estimator_is_unfitted():
    assert TemporalAttributionEstimator(_small_net()).fitted is False


def test_an_unfitted_estimator_abstains_and_claims_nothing():
    est = TemporalAttributionEstimator(_small_net(), WindowFeatureExtractor(window_steps=40))
    out = est.update(0, 0.1, _record("S"))
    out.validate()
    assert out.abstain_decision is True
    assert np.allclose(out.p_class, 1.0 / N_SOURCE_CLASSES)
    assert out.location_out == -1
    assert out.severity_uncertainty == float("inf")
    assert np.isnan(out.detection_time_s)


def test_an_unfitted_estimator_gives_the_same_answer_for_every_suite():
    """Randomly initialized weights carry no suite information, so nothing may differ."""

    est = TemporalAttributionEstimator(_small_net(), WindowFeatureExtractor(window_steps=40))
    outs = [est.update(0, 0.1, _record(suite)) for suite in ("C0", "C1", "S")]
    for out in outs[1:]:
        assert np.array_equal(out.p_class, outs[0].p_class)
        assert out.abstain_decision == outs[0].abstain_decision


def test_a_none_window_returns_the_honest_no_information_output():
    est = _fitted(_small_net(), WindowFeatureExtractor(window_steps=40))
    out = est.update(0, 0.1, None)
    out.validate()
    assert out.abstain_decision is True
    assert out.severity_uncertainty == float("inf")


def test_raw_severity_scale_refuses_before_weights_are_attached():
    est = TemporalAttributionEstimator(_small_net(), WindowFeatureExtractor(window_steps=40))
    with pytest.raises(ValueError, match="attached trained weights"):
        est.raw_severity_scale(_record("S"))


# --------------------------------------------------------------------------- #
# Attaching weights requires saying where they came from.
# --------------------------------------------------------------------------- #
def test_attaching_weights_records_provenance_and_marks_fitted():
    net = _small_net()
    est = TemporalAttributionEstimator(net, WindowFeatureExtractor(window_steps=40))
    est.attach_trained_weights(net.state_dict(), training_provenance="  run X, seed 3  ")
    assert est.fitted is True
    assert est.training_provenance == "run X, seed 3"


@pytest.mark.parametrize("provenance", ["", "   ", None, 3])
def test_attaching_weights_without_a_real_provenance_is_refused(provenance):
    net = _small_net()
    est = TemporalAttributionEstimator(net, WindowFeatureExtractor(window_steps=40))
    with pytest.raises(ValueError, match="training_provenance"):
        est.attach_trained_weights(net.state_dict(), training_provenance=provenance)
    assert est.fitted is False


def test_a_refused_attachment_leaves_the_estimator_unfitted_and_silent():
    net = _small_net()
    est = TemporalAttributionEstimator(net, WindowFeatureExtractor(window_steps=40))
    with pytest.raises(ValueError):
        est.attach_trained_weights(net.state_dict(), training_provenance="")
    out = est.update(0, 0.1, _record("S"))
    assert out.abstain_decision is True
    assert np.allclose(out.p_class, 1.0 / N_SOURCE_CLASSES)


def test_a_failed_state_dict_load_is_transactional_and_keeps_its_true_provenance():
    """A partial PyTorch load must not relabel mixed weights as the previous run."""

    net = _small_net()
    est = TemporalAttributionEstimator(net, WindowFeatureExtractor(window_steps=40))
    est.attach_trained_weights(
        net.state_dict(), training_provenance="original run, data root dev, seed 0"
    )
    before = {name: value.detach().clone() for name, value in est.net.state_dict().items()}
    incompatible = {name: value.detach().clone() for name, value in before.items()}
    first_key = next(iter(incompatible))
    last_key = next(reversed(incompatible))
    incompatible[first_key] = incompatible[first_key] + 1.0
    del incompatible[last_key]

    with pytest.raises(RuntimeError, match="Missing key"):
        est.attach_trained_weights(
            incompatible, training_provenance="replacement run, data root dev, seed 1"
        )

    assert est.training_provenance == "original run, data root dev, seed 0"
    assert all(
        torch.equal(value, est.net.state_dict()[name]) for name, value in before.items()
    )


def test_a_successful_attachment_updates_the_live_network_in_place():
    """`attach_trained_weights` must not swap the estimator's network for a new object."""

    est = TemporalAttributionEstimator(_small_net(), WindowFeatureExtractor(window_steps=40))
    captured = est.net
    donor = _small_net(seed=7)
    est.attach_trained_weights(donor.state_dict(), training_provenance="checkpoint, dev, seed 7")

    assert est.net is captured, "attaching weights replaced the live network object"
    assert all(
        torch.equal(value, captured.state_dict()[name])
        for name, value in donor.state_dict().items()
    ), "the captured reference does not see the attached weights"


def test_an_optimizer_built_before_attachment_still_drives_the_live_network():
    """The failure a rebinding install would cause: a silently orphaned optimizer.

    Building the optimizer and then resuming from a checkpoint is an ordinary order.
    If the attach rebinds `est.net`, the optimizer keeps stepping the abandoned module:
    no exception, a falling loss, and an estimator that never moves.
    """

    est = TemporalAttributionEstimator(_small_net(), WindowFeatureExtractor(window_steps=40))
    optimizer = torch.optim.SGD(est.net.parameters(), lr=1.0)
    est.attach_trained_weights(
        _small_net(seed=7).state_dict(), training_provenance="checkpoint, dev, seed 7"
    )

    before = {name: value.detach().clone() for name, value in est.net.state_dict().items()}
    optimizer.zero_grad()
    sum(parameter.sum() for parameter in optimizer.param_groups[0]["params"]).backward()
    optimizer.step()

    moved = [
        name
        for name, value in est.net.state_dict().items()
        if not torch.equal(before[name], value)
    ]
    assert moved, "an optimizer step moved nothing the estimator reads: it was orphaned"


def test_a_failed_attachment_does_not_replace_the_live_network_object():
    """Identity survives the refusal path too, not only the success path."""

    est = TemporalAttributionEstimator(_small_net(), WindowFeatureExtractor(window_steps=40))
    est.attach_trained_weights(est.net.state_dict(), training_provenance="original, dev, seed 0")
    captured = est.net
    incompatible = {
        name: value.detach().clone() for name, value in est.net.state_dict().items()
    }
    del incompatible[next(reversed(incompatible))]

    with pytest.raises(RuntimeError, match="Missing key"):
        est.attach_trained_weights(incompatible, training_provenance="replacement, dev, seed 1")

    assert est.net is captured


# --------------------------------------------------------------------------- #
# The fitted path, and the thresholds validation still owns.
# --------------------------------------------------------------------------- #
def test_a_fitted_estimator_reports_the_networks_simplex_and_validates():
    extractor = WindowFeatureExtractor(window_steps=40)
    est = _fitted(_small_net(), extractor)
    out = est.update(3, 0.2, _record("S"))
    out.validate()
    assert out.p_class.shape == (N_SOURCE_CLASSES,)
    assert out.p_class.sum() == pytest.approx(1.0, abs=1e-12)
    assert not np.allclose(out.p_class, 1.0 / N_SOURCE_CLASSES)


def test_a_fitted_estimator_still_abstains_until_a_threshold_is_supplied():
    est = _fitted(_small_net(), WindowFeatureExtractor(window_steps=40))
    assert est.abstain_threshold is None
    assert est.update(0, 0.1, _record("S")).abstain_decision is True


def test_a_supplied_abstain_threshold_makes_the_call_reachable():
    extractor = WindowFeatureExtractor(window_steps=40)
    lenient = _fitted(_small_net(), extractor, abstain_threshold=0.01)
    strict = _fitted(_small_net(), extractor, abstain_threshold=1.0)
    record = _record("S")
    assert lenient.update(0, 0.1, record).abstain_decision is False
    assert strict.update(0, 0.1, record).abstain_decision is True


def test_severity_uncertainty_is_never_the_raw_in_model_scale():
    """Session-24 finding: an in-sample scale understates true predictive error 5.72x for S."""

    est = _fitted(_small_net(), WindowFeatureExtractor(window_steps=40))
    record = _record("S")
    out = est.update(0, 0.1, record)
    raw = est.raw_severity_scale(record)
    assert np.isfinite(raw) and raw > 0.0
    assert out.severity_uncertainty == float("inf")


def test_detection_never_fires_without_a_supplied_threshold():
    est = _fitted(_small_net(), WindowFeatureExtractor(window_steps=40))
    assert est.detect_threshold is None
    for step in range(3):
        assert np.isnan(est.update(step, 0.1 * (step + 1), _record("S")).detection_time_s)


def test_detection_latches_the_first_crossing_and_holds_it():
    extractor = WindowFeatureExtractor(window_steps=40)
    est = _fitted(_small_net(), extractor, detect_threshold=1.0)  # healthy p always < 1
    first = est.update(0, 0.10, _record("S"))
    second = est.update(1, 0.20, _record("S", seed=1))
    assert first.detection_time_s == pytest.approx(0.10)
    assert second.detection_time_s == pytest.approx(0.10)


def test_reset_clears_the_detection_latch():
    extractor = WindowFeatureExtractor(window_steps=40)
    est = _fitted(_small_net(), extractor, detect_threshold=1.0)
    est.update(0, 0.10, _record("S"))
    est.reset()
    assert np.isnan(est._detection_time_s)
    assert est.update(0, 0.50, _record("S")).detection_time_s == pytest.approx(0.50)


@pytest.mark.parametrize("bad", [0.0, -0.1, 1.5])
def test_out_of_range_thresholds_are_refused(bad):
    with pytest.raises(ValueError, match="threshold"):
        TemporalAttributionEstimator(_small_net(), abstain_threshold=bad)
    with pytest.raises(ValueError, match="threshold"):
        TemporalAttributionEstimator(_small_net(), detect_threshold=bad)


def test_building_an_estimator_does_not_move_or_mutate_the_callers_network():
    """`nn.Module.to` relocates in place; adopting the caller's net would alias it."""

    net = _small_net()
    devices_before = {p.device for p in net.parameters()}
    est = TemporalAttributionEstimator(net, WindowFeatureExtractor(window_steps=40))
    assert est.net is not net
    assert {p.device for p in net.parameters()} == devices_before
    est.attach_trained_weights(
        {k: torch.zeros_like(v) for k, v in net.state_dict().items()},
        training_provenance="zeroed weights",
    )
    assert any(torch.any(p != 0.0) for p in net.parameters())


def test_two_estimators_from_one_network_do_not_share_weights():
    net = _small_net()
    a = TemporalAttributionEstimator(net, WindowFeatureExtractor(window_steps=40))
    b = TemporalAttributionEstimator(net, WindowFeatureExtractor(window_steps=40))
    a.attach_trained_weights(
        {k: torch.zeros_like(v) for k, v in net.state_dict().items()},
        training_provenance="zeroed weights",
    )
    assert any(torch.any(p != 0.0) for p in b.net.parameters())


def test_a_net_and_extractor_that_disagree_on_registry_width_are_refused():
    net = _small_net(registry_width=D + 1)
    with pytest.raises(ValueError, match="registry_width"):
        TemporalAttributionEstimator(net, WindowFeatureExtractor(window_steps=40))


# --------------------------------------------------------------------------- #
# Location decoding.
# --------------------------------------------------------------------------- #
def test_location_index_zero_decodes_to_not_localized():
    extractor = WindowFeatureExtractor(window_steps=40)
    net = _small_net()
    with torch.no_grad():
        net.location_head.weight.zero_()
        net.location_head.bias.zero_()
        net.location_head.bias[NOT_LOCALIZED_INDEX] = 10.0
    est = _fitted(net, extractor)
    assert est.update(0, 0.1, _record("S")).location_out == -1


@pytest.mark.parametrize("joint", range(N_JOINTS))
def test_a_localized_head_decodes_to_its_joint_index(joint):
    extractor = WindowFeatureExtractor(window_steps=40)
    net = _small_net()
    with torch.no_grad():
        net.location_head.weight.zero_()
        net.location_head.bias.zero_()
        net.location_head.bias[joint + 1] = 10.0
    est = _fitted(net, extractor)
    assert est.update(0, 0.1, _record("S")).location_out == joint


def test_the_location_head_has_one_logit_per_joint_plus_not_localized():
    assert N_LOCATION_LOGITS == N_JOINTS + 1


# --------------------------------------------------------------------------- #
# The deployable/privileged boundary, pinned at the source level.
# --------------------------------------------------------------------------- #
def test_the_module_imports_no_privileged_type():
    """A deployable rung may never reach labels, plant truth, identity, or the oracle."""

    source = (SCRIPTS_DIR / "utils" / "attribution_net.py").read_text(encoding="utf-8")
    import_lines = [
        line for line in source.splitlines() if line.startswith(("import ", "from ")) or
        (line.startswith("    ") and " import " in line)
    ]
    joined = "\n".join(import_lines)
    for forbidden in ("PrivilegedRecord", "OracleInterface", "LabelRecord", "PlantStepState"):
        assert forbidden not in joined, f"{forbidden} must not be importable by a deployable rung"


def test_the_estimator_update_signature_takes_only_an_observed_record():
    import inspect

    signature = inspect.signature(TemporalAttributionEstimator.update)
    assert list(signature.parameters) == ["self", "step_index", "decision_time_s", "window"]


def test_class_order_matches_the_scorers_order():
    assert SOURCE_CLASS_ORDER[HEALTHY_INDEX] == "healthy"
    assert len(SOURCE_CLASS_ORDER) == N_SOURCE_CLASSES


# --------------------------------------------------------------------------- #
# Device portability.
# --------------------------------------------------------------------------- #
def test_the_precision_context_restores_the_previous_flag():
    previous = torch.backends.cudnn.allow_tf32
    try:
        torch.backends.cudnn.allow_tf32 = True
        with deterministic_conv_precision():
            assert torch.backends.cudnn.allow_tf32 is False
        assert torch.backends.cudnn.allow_tf32 is True
    finally:
        torch.backends.cudnn.allow_tf32 = previous


def test_the_precision_context_restores_the_flag_after_an_exception():
    previous = torch.backends.cudnn.allow_tf32
    try:
        torch.backends.cudnn.allow_tf32 = True
        with pytest.raises(RuntimeError):
            with deterministic_conv_precision():
                raise RuntimeError("boom")
        assert torch.backends.cudnn.allow_tf32 is True
    finally:
        torch.backends.cudnn.allow_tf32 = previous


@pytest.mark.skipif(not torch.cuda.is_available(), reason="no CUDA device on this machine")
def test_cuda_and_cpu_agree_to_float32_epsilon_on_the_same_window():
    """Session-77 measurement: 5.960e-08 with TF32 off, 8.842e-05 with the default on."""

    extractor = WindowFeatureExtractor(window_steps=40)
    net = _small_net()
    record = _record("S")
    cpu = _fitted(net, extractor)
    gpu = TemporalAttributionEstimator(net, extractor, device="cuda")
    gpu.attach_trained_weights(net.state_dict(), training_provenance="unit-test synthetic weights")
    cpu_out = cpu.update(0, 0.1, record)
    gpu_out = gpu.update(0, 0.1, record)
    assert np.max(np.abs(cpu_out.p_class - gpu_out.p_class)) < 1.0e-6


@pytest.mark.skipif(not torch.cuda.is_available(), reason="no CUDA device on this machine")
def test_the_cuda_agreement_check_is_sharp_against_the_tf32_default():
    """Without the precision context, the same comparison exceeds the 1e-6 tolerance.

    This keeps the test above from passing merely because the perturbation is too
    small to see: at cuDNN's default the divergence is ~1.5 orders larger than the
    tolerance the shipped path meets.
    """

    extractor = WindowFeatureExtractor(window_steps=40)
    net = _small_net()
    values, valid = extractor.window_tensor(_record("S"))
    previous = torch.backends.cudnn.allow_tf32
    try:
        torch.backends.cudnn.allow_tf32 = True
        gpu_net = _small_net().to("cuda")
        gpu_net.load_state_dict(net.state_dict())
        with torch.no_grad():
            cpu_p = torch.softmax(net(window_to_input(values, valid)).class_logits, -1)
            gpu_p = torch.softmax(
                gpu_net(window_to_input(values, valid, device="cuda")).class_logits, -1
            ).cpu()
        assert float((cpu_p - gpu_p).abs().max()) > 1.0e-6
    finally:
        torch.backends.cudnn.allow_tf32 = previous
