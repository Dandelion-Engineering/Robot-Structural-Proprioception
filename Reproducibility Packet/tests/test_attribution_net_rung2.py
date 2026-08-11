"""Tests for Gate-4 rung 2, the recurrent-plus-attention attribution network.

Each test pins one property `protocol/rung2-escalation-v0.1.md` commits to, and the
properties are chosen for how they would fail *silently*:

  * **the ledger** - the parameter count is checked term by term against the design's
    seven-term decomposition, because a single total can be right for the wrong
    architecture. The `nn.MultiheadAttention` counterfactual is the case in point:
    228,330 parameters is **inside** the declared band, so the band check would admit
    the wrong attention block and only the exact count refuses it;
  * **the band** - `RUNG2_MIN_PARAMETERS` is pinned by equality to a value *derived*
    from the approved rung-1 constant, so an edit that retypes it goes red, and an
    AST check pins that no constructor argument can disable the check (invariant R5);
  * **the RNG order** - pinned twice, because the parameter count cannot see it.
    Source-level: `manual_seed` is called inside the `fork_rng` block and nowhere
    else. Behavioural: the caller's CPU RNG state survives a construction, with the
    seed-before-fork counterexample driven on the primitive so the guard is shown to
    be load-bearing rather than assumed to be (invariant R13, finding BI);
  * **causality** - measured by perturbation, not read off the diagram, and measured
    on the *recurrent* features, which is where a bidirectional GRU would read the
    window's future into its past without changing any shape;
  * **suite invariance** - identical parameter count and identical shapes with the
    eight gauge columns masked, so a measured S-over-C1 difference cannot be model
    capacity. This is what makes "exactly capacity-matched" a property of the
    construction rather than a promise;
  * **the import discipline** - rung 2 defines no causal block of its own, so this
    project keeps one definition of the causal padding rule (decision D1);
  * **the four disclosed limitations** - each pinned as *behaviour* rather than
    repaired, because repairing any of them means editing a file inside a recorded
    code identity (decision D4).

Speed comes from short windows and small batches. There is no de-banded network
anywhere in this file, because there is no way to build one.
"""

from __future__ import annotations

import ast
import inspect
import math
import sys
from pathlib import Path

import numpy as np
import pytest
import torch
from torch import nn

SCRIPTS_DIR = Path(__file__).resolve().parents[1] / "scripts"
sys.path.insert(0, str(SCRIPTS_DIR))

from utils import attribution_net_rung2 as rung2  # noqa: E402
from utils.attribution_net import (  # noqa: E402
    AttributionHeads,
    CAPACITY_LADDER,
    N_INPUT_STREAMS,
    N_LOCATION_LOGITS,
    RUNG1_MAX_PARAMETERS,
    RUNG1_MIN_PARAMETERS,
    TemporalAttributionEstimator,
    TemporalAttributionNet,
    _CausalDilatedBlock,
    _PerStepChannelNorm,
    window_to_input,
)
from utils.attribution_net_rung2 import (  # noqa: E402
    RUNG2_ATTENTION_HEADS,
    RUNG2_CHANNELS,
    RUNG2_DECLARED_PARAMETERS,
    RUNG2_GRU_LAYERS,
    RUNG2_HIDDEN_SIZE,
    RUNG2_KERNEL_SIZE,
    RUNG2_MAX_PARAMETERS,
    RUNG2_MIN_PARAMETERS,
    RUNG2_NAME,
    RUNG2_STEM_BLOCKS,
    RecurrentAttentionAttributionNet,
)
from utils.estimator import (  # noqa: E402
    N_SOURCE_CLASSES,
    WindowFeatureExtractor,
)
from utils.schema_types import (  # noqa: E402
    CHANNEL_NAMES,
    CHANNEL_WIDTH,
    SUITE_CHANNELS,
    ObservedRecord,
    observed_registry_width,
)

D = observed_registry_width()

# The design's section 4.2 selection grid, transcribed from the approved document:
# (channels, stem blocks, hidden, GRU layers, heads, parameters, stem RF, in band).
SELECTION_GRID = (
    (48, 4, 64, 1, 4, 82_778, 31, False),
    (64, 4, 96, 1, 4, 163_146, 31, True),
    (64, 4, 96, 2, 4, 219_018, 31, True),
    (64, 5, 96, 2, 4, 235_658, 63, True),
    (64, 4, 128, 2, 4, 326_346, 31, True),
    (96, 4, 128, 2, 8, 422_314, 31, True),
    (96, 6, 160, 2, 8, 635_882, 127, True),
)

# The design's seven-term parameter ledger, by the attribute that carries each term.
PARAMETER_LEDGER = (
    ("input_proj", 2_368),
    ("stem", 66_560),
    ("stem_norm", 128),
    ("gru", 102_528),
    ("attention_projections", 27_936),
    ("fuse", 18_528),
    ("heads", 970),
)


# --------------------------------------------------------------------------- #
# Shared fixtures.
# --------------------------------------------------------------------------- #
def _net(**kwargs) -> RecurrentAttentionAttributionNet:
    """The shipped rung-2 configuration; overrides are for grid and refusal cases."""

    return RecurrentAttentionAttributionNet(**kwargs)


def _window(steps: int = 48, *, batch: int = 2, seed: int = 0) -> torch.Tensor:
    """A `[batch, 2D, steps]` pseudo-input of the shape `window_to_input` produces."""

    generator = torch.Generator().manual_seed(seed)
    return torch.randn(batch, N_INPUT_STREAMS * D, steps, generator=generator)


def _record(suite: str, t: int = 40, *, seed: int = 0) -> ObservedRecord:
    """Build a fully-valid `t`-step observed record for `suite` with pseudo signals.

    Channels the suite lacks are all-NaN and masked off, exactly as the real sensor
    model emits them. This is rung 1's own fixture shape, kept identical so the two
    rungs are exercised against the same notion of a suite.
    """

    rng = np.random.default_rng(seed)
    times = np.arange(t, dtype=float) * 0.002
    values, valid, meas, avail, lat = {}, {}, {}, {}, {}
    for name in CHANNEL_NAMES:
        width = CHANNEL_WIDTH[name]
        if name in SUITE_CHANNELS[suite]:
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


def _count(module: nn.Module) -> int:
    """Trainable parameters of one submodule."""

    return sum(int(p.numel()) for p in module.parameters() if p.requires_grad)


def _ledger_terms(net: RecurrentAttentionAttributionNet) -> dict[str, int]:
    """The seven ledger terms, read off the constructed network rather than declared."""

    return {
        "input_proj": _count(net.input_proj),
        "stem": _count(net.stem),
        "stem_norm": _count(net.stem_norm),
        "gru": _count(net.gru),
        "attention_projections": (
            _count(net.q_proj) + _count(net.k_proj) + _count(net.v_proj)
        ),
        "fuse": _count(net.fuse),
        "heads": (
            _count(net.class_head)
            + _count(net.unknown_head)
            + _count(net.location_head)
            + _count(net.severity_head)
        ),
    }


def _init_ast() -> ast.FunctionDef:
    """The `__init__` AST node of the rung-2 class, parsed from the module source."""

    source = Path(rung2.__file__).read_text(encoding="utf-8")
    tree = ast.parse(source)
    for node in tree.body:
        if isinstance(node, ast.ClassDef) and node.name == "RecurrentAttentionAttributionNet":
            for statement in node.body:
                if isinstance(statement, ast.FunctionDef) and statement.name == "__init__":
                    return statement
    raise AssertionError("the rung-2 class has no __init__ to inspect")


def _argument_names(function: ast.FunctionDef) -> set[str]:
    """Every parameter name of a parsed function signature."""

    arguments = function.args
    names = {a.arg for a in arguments.posonlyargs + arguments.args + arguments.kwonlyargs}
    if arguments.vararg is not None:
        names.add(arguments.vararg.arg)
    if arguments.kwarg is not None:
        names.add(arguments.kwarg.arg)
    return names


# --------------------------------------------------------------------------- #
# The parameter ledger: the total, and every term that makes it up.
# --------------------------------------------------------------------------- #
def test_the_shipped_configuration_has_the_declared_parameter_count():
    assert _net().n_parameters == RUNG2_DECLARED_PARAMETERS == 219_018


def test_the_seven_term_ledger_reproduces_from_the_constructed_network():
    """A total can be right for the wrong architecture; the terms cannot."""

    terms = _ledger_terms(_net())
    assert terms == dict(PARAMETER_LEDGER)
    assert sum(terms.values()) == RUNG2_DECLARED_PARAMETERS


def test_the_ledger_terms_are_the_whole_network_and_nothing_is_uncounted():
    net = _net()
    assert sum(_ledger_terms(net).values()) == net.n_parameters


def test_the_shipped_configuration_is_the_declared_one():
    net = _net()
    assert (net.channels, net.n_stem_blocks, net.hidden_size) == (
        RUNG2_CHANNELS,
        RUNG2_STEM_BLOCKS,
        RUNG2_HIDDEN_SIZE,
    )
    assert (net.n_gru_layers, net.n_heads, net.kernel_size) == (
        RUNG2_GRU_LAYERS,
        RUNG2_ATTENTION_HEADS,
        RUNG2_KERNEL_SIZE,
    )
    assert (RUNG2_CHANNELS, RUNG2_STEM_BLOCKS, RUNG2_HIDDEN_SIZE) == (64, 4, 96)
    assert (RUNG2_GRU_LAYERS, RUNG2_ATTENTION_HEADS, RUNG2_KERNEL_SIZE) == (2, 4, 3)


def test_rung_2_is_5_53_times_rung_1_and_both_counts_are_pinned():
    assert TemporalAttributionNet(seed=0).n_parameters == 39_594
    assert _net().n_parameters == 219_018
    assert 219_018 / 39_594 == pytest.approx(5.53, abs=0.005)


# --------------------------------------------------------------------------- #
# The band: derived, contiguous, and with no way to switch it off (R4, R5, D2).
# --------------------------------------------------------------------------- #
def test_the_band_floor_is_derived_from_the_approved_rung_1_constant():
    """Pinned by equality, not by parametrization: retyping the literal goes red."""

    assert RUNG2_MIN_PARAMETERS == RUNG1_MAX_PARAMETERS + 1
    assert RUNG2_MIN_PARAMETERS == 100_001
    assert RUNG2_MAX_PARAMETERS == 1_000_000


def test_the_band_floor_is_derived_in_the_source_and_not_only_in_its_value():
    """"Derived, never retyped" is a property of the expression, not of the number.

    The equality pin above catches a floor retyped to the *wrong* value. It cannot
    catch one retyped to the right value, because that is not a behaviour change at
    all -- and yet it is exactly the edit that silently unbinds the two bands, so that
    a later change to rung 1's constant leaves rung 2's floor sitting where it was.
    The instrument for a source property is the source.
    """

    tree = ast.parse(Path(rung2.__file__).read_text(encoding="utf-8"))
    assignments = [
        node
        for node in tree.body
        if isinstance(node, ast.Assign)
        and any(
            isinstance(t, ast.Name) and t.id == "RUNG2_MIN_PARAMETERS" for t in node.targets
        )
    ]
    assert len(assignments) == 1
    value = assignments[0].value
    assert isinstance(value, ast.BinOp) and isinstance(value.op, ast.Add)
    assert isinstance(value.left, ast.Name) and value.left.id == "RUNG1_MAX_PARAMETERS"
    assert isinstance(value.right, ast.Constant) and value.right.value == 1


def test_the_two_size_bands_are_contiguous_and_disjoint():
    """No parameter count has both size-band answers available."""

    assert RUNG1_MAX_PARAMETERS < RUNG2_MIN_PARAMETERS
    assert RUNG2_MIN_PARAMETERS - RUNG1_MAX_PARAMETERS == 1
    for count in (RUNG1_MIN_PARAMETERS, RUNG1_MAX_PARAMETERS):
        assert not RUNG2_MIN_PARAMETERS <= count <= RUNG2_MAX_PARAMETERS
    for count in (RUNG2_MIN_PARAMETERS, RUNG2_MAX_PARAMETERS):
        assert not RUNG1_MIN_PARAMETERS <= count <= RUNG1_MAX_PARAMETERS


def test_the_shipped_count_sits_inside_the_band_with_margin():
    count = _net().n_parameters
    assert RUNG2_MIN_PARAMETERS < count < RUNG2_MAX_PARAMETERS
    assert count > 2 * RUNG2_MIN_PARAMETERS


@pytest.mark.parametrize(
    "channels,blocks,hidden,layers,heads,parameters,stem_rf,in_band", SELECTION_GRID
)
def test_every_row_of_the_measured_selection_grid_reproduces(
    channels, blocks, hidden, layers, heads, parameters, stem_rf, in_band
):
    """The design's grid is rebuilt by construction, including the row it refuses."""

    build = lambda: RecurrentAttentionAttributionNet(  # noqa: E731
        channels=channels,
        n_stem_blocks=blocks,
        hidden_size=hidden,
        n_gru_layers=layers,
        n_heads=heads,
    )
    if in_band:
        net = build()
        assert net.n_parameters == parameters
        assert net.stem_receptive_field == stem_rf
    else:
        with pytest.raises(ValueError) as error:
            build()
        assert str(parameters) in str(error.value)
        assert f"[{RUNG2_MIN_PARAMETERS}, {RUNG2_MAX_PARAMETERS}]" in str(error.value)


def test_the_undersized_grid_row_is_refused_as_a_band_violation():
    """82,778 is an undersized rung-2 candidate, and the refusal says which band."""

    with pytest.raises(ValueError, match="outside the rung-2 band"):
        RecurrentAttentionAttributionNet(
            channels=48, n_stem_blocks=4, hidden_size=64, n_gru_layers=1, n_heads=4
        )


def test_the_multiheadattention_counterfactual_is_inside_the_band():
    """The band cannot refuse the wrong attention block; only the exact count can.

    `nn.MultiheadAttention` at this width carries an `H -> H` output projection the
    design does not want. Substituting it for the three written-out projections gives
    228,330 parameters -- which the band admits. That is why the executable asserts an
    exact count rather than a band membership, and why this test exists at all.
    """

    net = _net()
    written_out = _ledger_terms(net)["attention_projections"]
    library = _count(nn.MultiheadAttention(net.hidden_size, net.n_heads, batch_first=True))
    counterfactual = net.n_parameters - written_out + library
    assert written_out == 27_936
    assert counterfactual == 228_330
    assert RUNG2_MIN_PARAMETERS <= counterfactual <= RUNG2_MAX_PARAMETERS
    assert counterfactual != RUNG2_DECLARED_PARAMETERS


def test_the_network_carries_no_attention_output_projection():
    net = _net()
    names = {name for name, _ in net.named_children()}
    assert not any("out_proj" in name or name == "attention" for name in names)
    assert not isinstance(getattr(net, "attn", None), nn.MultiheadAttention)
    assert not any(isinstance(module, nn.MultiheadAttention) for module in net.modules())


# --------------------------------------------------------------------------- #
# R5: there is no enforcement bypass, at the signature or at the raise.
# --------------------------------------------------------------------------- #
@pytest.mark.parametrize("forbidden", ("enforce", "band", "skip", "strict", "check"))
def test_no_constructor_parameter_could_disable_the_band_check(forbidden):
    names = _argument_names(_init_ast())
    assert not any(forbidden in name for name in names)


def test_the_band_check_is_the_last_statement_of_the_constructor():
    last = _init_ast().body[-1]
    assert isinstance(last, ast.If)
    assert last.orelse == []
    assert len(last.body) == 1 and isinstance(last.body[0], ast.Raise)


def test_the_band_raise_is_not_guarded_by_any_constructor_argument():
    """Its condition may read module constants and the measured total, nothing else."""

    init = _init_ast()
    condition = init.body[-1].test
    referenced = {node.id for node in ast.walk(condition) if isinstance(node, ast.Name)}
    assert referenced & {"RUNG2_MIN_PARAMETERS", "RUNG2_MAX_PARAMETERS"}
    assert not referenced & _argument_names(init)


def test_the_constructor_refuses_an_unknown_keyword_rather_than_ignoring_it():
    for keyword in ("enforce_rung2_band", "skip_band_check", "strict"):
        with pytest.raises(TypeError):
            RecurrentAttentionAttributionNet(**{keyword: False})


def test_the_signature_is_keyword_only_so_no_positional_can_slip_past():
    parameters = inspect.signature(RecurrentAttentionAttributionNet.__init__).parameters
    for name, parameter in parameters.items():
        if name == "self":
            continue
        assert parameter.kind is inspect.Parameter.KEYWORD_ONLY


# --------------------------------------------------------------------------- #
# R13: matched seeds mean matched initialization, and the RNG order is specified.
# --------------------------------------------------------------------------- #
def test_the_same_seed_builds_bit_identical_parameters():
    left, right = _net(seed=0).state_dict(), _net(seed=0).state_dict()
    assert left.keys() == right.keys()
    assert all(torch.equal(left[k], right[k]) for k in left)


def test_a_different_seed_changes_at_least_one_tensor():
    left, right = _net(seed=0).state_dict(), _net(seed=1).state_dict()
    assert any(not torch.equal(left[k], right[k]) for k in left)


def test_the_suite_is_not_a_constructor_argument_at_all():
    """The strongest form of "matched between C1 and S": the suite cannot be named."""

    assert "suite" not in _argument_names(_init_ast())


def test_construction_leaves_the_callers_cpu_rng_state_unchanged():
    torch.manual_seed(7)
    before = torch.random.get_rng_state().clone()
    _net(seed=3)
    assert torch.equal(before, torch.random.get_rng_state())


def test_seeding_before_the_fork_would_mutate_the_caller_and_the_count_cannot_see_it():
    """The counterexample behind finding BI, driven on the primitive rather than told.

    Both orders build the same 219,018 parameters, so the invariant a reader checks
    first is blind to the difference. What separates them is the caller's RNG state,
    which is why the assertion above is the load-bearing one.
    """

    torch.manual_seed(11)
    before = torch.random.get_rng_state().clone()
    torch.random.manual_seed(3)
    with torch.random.fork_rng(devices=[], enabled=True):
        torch.random.manual_seed(3)
    assert not torch.equal(before, torch.random.get_rng_state())

    torch.manual_seed(11)
    before = torch.random.get_rng_state().clone()
    with torch.random.fork_rng(devices=[], enabled=True):
        torch.random.manual_seed(3)
    assert torch.equal(before, torch.random.get_rng_state())


def test_the_seeding_call_is_inside_the_fork_and_occurs_nowhere_else():
    """Source-level half of the same invariant: the order is in the code, not a habit."""

    init = _init_ast()
    forks = [
        node
        for node in ast.walk(init)
        if isinstance(node, ast.With)
        and any(
            isinstance(item.context_expr, ast.Call)
            and ast.unparse(item.context_expr.func).endswith("fork_rng")
            for item in node.items
        )
    ]
    assert len(forks) == 1
    inside = [
        node
        for node in ast.walk(forks[0])
        if isinstance(node, ast.Call) and ast.unparse(node.func).endswith("manual_seed")
    ]
    everywhere = [
        node
        for node in ast.walk(init)
        if isinstance(node, ast.Call) and ast.unparse(node.func).endswith("manual_seed")
    ]
    assert len(inside) == 1 and len(everywhere) == 1


# --------------------------------------------------------------------------- #
# Causality, measured by perturbation rather than read off the diagram.
# --------------------------------------------------------------------------- #
def test_no_recurrent_feature_depends_on_a_later_input():
    net = _net(seed=0).eval()
    cut = 24
    base = _window(steps=64)
    perturbed = base.clone()
    perturbed[:, :, cut + 1 :] += 3.0
    with torch.no_grad():
        before, after = net.encode(base), net.encode(perturbed)
    difference = (before - after).abs()
    assert float(difference[:, : cut + 1, :].max()) == 0.0
    assert float(difference[:, cut + 1 :, :].max()) > 0.0


def test_the_recurrent_layer_is_unidirectional_and_two_layers_deep():
    net = _net()
    assert net.gru.bidirectional is False
    assert net.gru.num_layers == RUNG2_GRU_LAYERS == 2
    assert net.gru.batch_first is True
    assert net.gru.bias is True
    assert float(net.gru.dropout) == 0.0


def test_the_stem_receptive_field_is_the_declared_31_samples():
    assert _net().stem_receptive_field == 31
    assert _net(n_stem_blocks=5).stem_receptive_field == 63


def test_there_is_no_receptive_field_attribute_to_be_read_as_the_windows_reach():
    """Disclosed limitation 4: a `receptive_field` of 31 would be a false name."""

    net = _net()
    assert not hasattr(net, "receptive_field")
    assert hasattr(net, "stem_receptive_field")
    assert hasattr(TemporalAttributionNet(seed=0), "receptive_field")


def test_the_pooled_read_moves_for_perturbations_anywhere_in_the_window():
    """The GRU and the pool span the window, so an early perturbation is not lost."""

    net = _net(seed=0).eval()
    base = _window(steps=64)
    head, tail = base.clone(), base.clone()
    head[:, :, :16] += 3.0
    tail[:, :, -16:] += 3.0
    with torch.no_grad():
        pooled = net.pool(net.encode(base))
        moved_head = net.pool(net.encode(head))
        moved_tail = net.pool(net.encode(tail))
    assert float((pooled - moved_head).abs().mean()) > 0.0
    assert float((pooled - moved_tail).abs().mean()) > 0.0


# --------------------------------------------------------------------------- #
# Suite invariance: the capacity match is a property of the construction.
# --------------------------------------------------------------------------- #
def test_masking_the_gauge_columns_changes_the_output_and_not_the_capacity():
    net = _net(seed=0).eval()
    base = _window(steps=48)
    offset = sum(CHANNEL_WIDTH[name] for name in CHANNEL_NAMES[:-1])
    width = CHANNEL_WIDTH["gauge_obs"]
    # The design's "eight gauge columns" counts the input tensor's columns, not the
    # registry's: the gauge channel is four registry columns, and each arrives twice
    # -- once as a value and once as its validity mask.
    assert width == 4 and N_INPUT_STREAMS * width == 8
    masked = base.clone()
    masked[:, offset : offset + width, :] = 0.0
    masked[:, D + offset : D + offset + width, :] = 0.0
    with torch.no_grad():
        full, reduced = net(base), net(masked)
    assert net.n_parameters == RUNG2_DECLARED_PARAMETERS
    assert full.class_logits.shape == reduced.class_logits.shape
    assert not torch.equal(full.class_logits, reduced.class_logits)


def test_real_suite_windows_share_one_shape_and_one_parameter_count():
    extractor = WindowFeatureExtractor(window_steps=40)
    net = _net(seed=0).eval()
    before = net.n_parameters
    shapes, outputs = set(), []
    for suite in ("C0", "C1", "S"):
        values, valid = extractor.window_tensor(_record(suite))
        batch = window_to_input(values, valid)
        shapes.add(tuple(batch.shape))
        with torch.no_grad():
            outputs.append(net(batch).class_logits)
    assert len(shapes) == 1
    assert net.n_parameters == before == RUNG2_DECLARED_PARAMETERS
    assert not torch.equal(outputs[1], outputs[2])


# --------------------------------------------------------------------------- #
# The attention block: wired, scaled as specified, and not a no-op.
# --------------------------------------------------------------------------- #
def test_the_attention_weights_are_a_distribution_over_the_time_axis():
    net = _net(seed=0).eval()
    steps = 48
    with torch.no_grad():
        _, weights = net.attend(net.encode(_window(steps=steps)))
    assert tuple(weights.shape) == (2, RUNG2_ATTENTION_HEADS, steps)
    assert torch.allclose(weights.sum(dim=-1), torch.ones(2, RUNG2_ATTENTION_HEADS), atol=1e-5)
    assert float(weights.min()) >= 0.0


def test_the_attention_context_is_not_a_no_op():
    """Zeroing the context changes the pooled vector, so the path carries signal."""

    net = _net(seed=0).eval()
    with torch.no_grad():
        sequence = net.encode(_window(steps=48))
        context, _ = net.attend(sequence)
        pooled = net.pool(sequence)
        without = net.fuse_act(
            net.fuse(torch.cat([sequence[:, -1, :], torch.zeros_like(context)], dim=-1))
        )
    assert float((pooled - without).abs().mean()) > 0.0


def test_the_attention_is_recomputed_by_hand_from_the_projections():
    """The scaling, the head split and the softmax axis are pinned by reconstruction."""

    net = _net(seed=0).eval()
    sequence = net.encode(_window(steps=32))
    with torch.no_grad():
        context, weights = net.attend(sequence)
        batch, steps, hidden = sequence.shape
        head_dim = hidden // net.n_heads
        query = net.q_proj(sequence[:, -1, :]).view(batch, net.n_heads, 1, head_dim)
        keys = net.k_proj(sequence).view(batch, steps, net.n_heads, head_dim).transpose(1, 2)
        values = net.v_proj(sequence).view(batch, steps, net.n_heads, head_dim).transpose(1, 2)
        scores = torch.matmul(query, keys.transpose(-2, -1)) / math.sqrt(head_dim)
        expected_weights = torch.softmax(scores, dim=-1)
        expected_context = torch.matmul(expected_weights, values).reshape(batch, hidden)
    assert torch.equal(context, expected_context)
    assert torch.equal(weights, expected_weights.reshape(batch, net.n_heads, steps))
    assert head_dim == net.head_dim == RUNG2_HIDDEN_SIZE // RUNG2_ATTENTION_HEADS


def test_the_pool_is_the_fusion_of_the_final_state_and_the_attention_context():
    """Which two vectors are fused, and in which order, both pinned by reconstruction.

    Measured by mutation, not guessed at: without this, a fusion reading the context
    twice, or reading the two operands in the opposite order, passes every other test
    in this file. The parameter count cannot see either mutation and neither can any
    shape.
    """

    net = _net(seed=0).eval()
    with torch.no_grad():
        sequence = net.encode(_window(steps=32))
        context, _ = net.attend(sequence)
        final = sequence[:, -1, :]
        expected = net.fuse_act(net.fuse(torch.cat([final, context], dim=-1)))
        swapped = net.fuse_act(net.fuse(torch.cat([context, final], dim=-1)))
        doubled = net.fuse_act(net.fuse(torch.cat([context, context], dim=-1)))
        pooled = net.pool(sequence)
    assert torch.equal(pooled, expected)
    assert not torch.equal(pooled, swapped)
    assert not torch.equal(pooled, doubled)


def test_forward_reads_its_heads_off_the_pooled_representation():
    """`forward` is `encode` then `pool` then the heads, and nothing else.

    Also measured by mutation: a `forward` that pools the final recurrent state
    directly -- leaving the whole attention block constructed but dead -- has the
    declared parameter count, the declared shapes and the declared causality.
    """

    net = _net(seed=0).eval()
    batch = _window(steps=32)
    with torch.no_grad():
        heads = net(batch)
        pooled = net.pool(net.encode(batch))
        severity = net.severity_head(pooled)
        assert torch.equal(heads.class_logits, net.class_head(pooled))
        assert torch.equal(heads.unknown_logit, net.unknown_head(pooled).squeeze(-1))
        assert torch.equal(heads.location_logits, net.location_head(pooled))
        assert torch.equal(heads.severity_value, severity[:, 0])
        assert torch.equal(heads.severity_log_scale, severity[:, 1])


def test_every_constructed_parameter_is_reached_by_the_forward_pass():
    """No stage may be constructed, counted in the ledger, and then left unwired.

    This is the general instrument behind the two reconstruction tests above. A module
    that is built in `__init__` and never applied in `forward` still contributes to
    `n_parameters`, still has the right shape and still passes every determinism and
    causality check -- it simply does nothing. A parameter that receives no gradient
    from the network's own output is exactly that condition, stated once, for every
    tensor at once.
    """

    net = _net(seed=0)
    net.zero_grad(set_to_none=True)
    heads = net(_window(steps=32))
    scalar = (
        heads.class_logits.sum()
        + heads.unknown_logit.sum()
        + heads.location_logits.sum()
        + heads.severity_value.sum()
        + heads.severity_log_scale.sum()
    )
    scalar.backward()
    unreached = [
        name
        for name, parameter in net.named_parameters()
        if parameter.grad is None or not bool(torch.any(parameter.grad != 0).item())
    ]
    assert unreached == []
    assert sum(int(p.numel()) for p in net.parameters()) == RUNG2_DECLARED_PARAMETERS


def test_a_hidden_width_the_heads_cannot_divide_is_refused():
    with pytest.raises(ValueError, match="not divisible by n_heads"):
        RecurrentAttentionAttributionNet(hidden_size=98, n_heads=4)


@pytest.mark.parametrize(
    "kwargs",
    (
        {"registry_width": 0},
        {"channels": 0},
        {"n_stem_blocks": 0},
        {"hidden_size": 0},
        {"n_gru_layers": 0},
        {"n_heads": 0},
        {"kernel_size": 0},
        {"seed": -1},
    ),
)
def test_a_nonsensical_size_is_refused_loudly(kwargs):
    with pytest.raises(ValueError):
        RecurrentAttentionAttributionNet(**kwargs)


# --------------------------------------------------------------------------- #
# The import discipline (D1) and the module census.
# --------------------------------------------------------------------------- #
def test_rung_2_defines_no_causal_block_or_normalization_of_its_own():
    """One definition of the causal padding rule in this project, not two."""

    tree = ast.parse(Path(rung2.__file__).read_text(encoding="utf-8"))
    defined = {node.name for node in tree.body if isinstance(node, ast.ClassDef)}
    assert defined == {"RecurrentAttentionAttributionNet"}


def test_the_stem_is_built_from_the_approved_rung_1_blocks():
    net = _net()
    assert len(net.stem) == RUNG2_STEM_BLOCKS
    assert all(isinstance(block, _CausalDilatedBlock) for block in net.stem)
    assert isinstance(net.stem_norm, _PerStepChannelNorm)
    assert [block.conv.dilation[0] for block in net.stem] == [1, 2, 4, 8]


def test_the_module_type_census_is_the_one_the_design_recorded():
    """Rung 2 is deeper in the recurrent path and shallower in the convolutional one."""

    def census(module: nn.Module) -> dict[str, int]:
        counts: dict[str, int] = {}
        for child in module.modules():
            name = type(child).__name__
            if name in ("Conv1d", "Linear", "GRU", "LayerNorm"):
                counts[name] = counts.get(name, 0) + 1
        return counts

    assert census(_net()) == {"Conv1d": 9, "Linear": 8, "GRU": 1, "LayerNorm": 5}
    rung1 = census(TemporalAttributionNet(seed=0))
    assert rung1 == {"Conv1d": 19, "Linear": 4, "LayerNorm": 10}
    assert "GRU" not in rung1


# --------------------------------------------------------------------------- #
# The contract with the rest of the project.
# --------------------------------------------------------------------------- #
def test_forward_returns_the_approved_attribution_heads_dataclass():
    heads = _net(seed=0).eval()(_window(steps=48))
    assert type(heads) is AttributionHeads


def test_every_head_has_the_shape_the_downstream_contract_expects():
    batch = 3
    heads = _net(seed=0).eval()(_window(steps=48, batch=batch))
    assert tuple(heads.class_logits.shape) == (batch, N_SOURCE_CLASSES)
    assert tuple(heads.unknown_logit.shape) == (batch,)
    assert tuple(heads.location_logits.shape) == (batch, N_LOCATION_LOGITS)
    assert tuple(heads.severity_value.shape) == (batch,)
    assert tuple(heads.severity_log_scale.shape) == (batch,)


def test_the_registry_width_matches_the_schema_and_the_window_front_end():
    net = _net()
    assert net.registry_width == D == WindowFeatureExtractor().registry_width
    assert net.rung == RUNG2_NAME == "rung2_recurrent_plus_attention"


def test_encode_refuses_an_input_that_is_not_the_window_contract():
    net = _net()
    with pytest.raises(ValueError, match=r"\[B, 2D, T\]"):
        net.encode(torch.zeros(2, N_INPUT_STREAMS * D))
    with pytest.raises(ValueError, match="streams"):
        net.encode(torch.zeros(2, N_INPUT_STREAMS * D + 1, 16))


def test_attend_refuses_a_sequence_that_is_not_the_recurrent_contract():
    net = _net()
    with pytest.raises(ValueError, match=r"\[B, T, H\]"):
        net.attend(torch.zeros(2, RUNG2_HIDDEN_SIZE))
    with pytest.raises(ValueError, match="hidden units"):
        net.attend(torch.zeros(2, 16, RUNG2_HIDDEN_SIZE + 1))


def test_the_approved_estimator_wrapper_accepts_a_rung_2_network_unedited():
    """Disclosed limitations 2 and 3: the annotation is narrow, the behaviour is not."""

    net = _net(seed=0)
    extractor = WindowFeatureExtractor(window_steps=40)
    estimator = TemporalAttributionEstimator(net, extractor)
    assert isinstance(estimator.net, RecurrentAttentionAttributionNet)
    assert estimator.net is not net
    assert estimator.fitted is False
    identity = id(estimator.net)
    estimator.attach_trained_weights(
        net.state_dict(), training_provenance="unit-test synthetic weights"
    )
    assert estimator.fitted is True
    assert id(estimator.net) == identity


def test_an_unfitted_rung_2_estimator_still_refuses_to_answer():
    estimator = TemporalAttributionEstimator(
        _net(seed=0), WindowFeatureExtractor(window_steps=40)
    )
    output = estimator.update(0, 0.1, _record("S"))
    assert output.abstain_decision is True
    assert output.location_out == -1
    assert output.severity_uncertainty == float("inf")
    assert output.p_class == pytest.approx([1.0 / N_SOURCE_CLASSES] * N_SOURCE_CLASSES)


# --------------------------------------------------------------------------- #
# The disclosed limitations, pinned as behaviour rather than repaired (D4).
# --------------------------------------------------------------------------- #
def test_the_capacity_ladders_rung_2_entry_is_still_recorded_as_unbuilt():
    """Decision D4: `attribution_net.py` is inside a recorded code identity.

    Flipping this flag would change `dev_fit_trainer.training_code_identity()` and the
    entry-by-entry check would then refuse every future run that reads the approved
    rung-1 anchors. A one-word edit to a comment-level field would cost the project
    its ability to re-verify its own fitted record, so the flag stays and this test
    records why.
    """

    entry = next(rung for rung in CAPACITY_LADDER if rung.name == RUNG2_NAME)
    assert entry.built is False
    assert CAPACITY_LADDER[0].built is True


def test_the_rung_name_is_the_one_the_approved_ladder_already_carries():
    assert RUNG2_NAME in {rung.name for rung in CAPACITY_LADDER}


def test_this_module_does_not_import_the_trainer_the_sweep_or_the_analyzers():
    """Rung 2's architecture is a leaf: no fitting, no persistence, no analysis."""

    tree = ast.parse(Path(rung2.__file__).read_text(encoding="utf-8"))
    imported = set()
    for node in ast.walk(tree):
        if isinstance(node, ast.ImportFrom) and node.module:
            imported.add(node.module)
        elif isinstance(node, ast.Import):
            imported.update(alias.name for alias in node.names)
    assert not any(
        name.endswith(("dev_fit_trainer", "capacity_sweep", "analyze_dev_fit"))
        for name in imported
    )
    assert "utils.attribution_net" in imported
