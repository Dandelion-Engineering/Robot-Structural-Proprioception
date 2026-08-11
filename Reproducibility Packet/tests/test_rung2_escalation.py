"""Tests for the Gate-4 rung-2 escalation executable (`utils.rung2_escalation`).

Four disciplines shape this file, all of them bought by measured defects earlier in
this project.

**Session 65's.** The exit paths of a program are the region no unit test enters. Every
terminal exit of `main()` below is driven through `main(argv)` and the artifact it wrote
is read back and asserted on -- never from the return code alone, which is the check
that passes while the document is empty, malformed or missing. The two exits that
deliberately write nothing are tested by asserting that nothing was written **and** that
invariant R8's zero resource counts reached stdout, since no artifact can carry them
there.

**Session 47's (requirement (r)).** A pinned literal that also lives in a bound document
is checked by EQUALITY against that document, never adopted from it. The fixed protocol,
the selected configuration, the parameter count, the stem receptive field, the seed set
and the `nn.MultiheadAttention` counterfactual are therefore parsed out of the frozen
design's own tables and compared to the module's constants, and the design's canonical
digest is compared to the file rather than to itself.

**Session 114's.** A test that a component is *connected* cannot see whether it is in the
right *place*. So the seam this module exists to create -- one loop, two factories -- is
not asserted by reading it: `fit_arm` with the rung-1 reference factory is **run** and
its weights and per-epoch history compared bit for bit against the approved width path
at 32 channels, with the caller's global RNG deliberately polluted first.

**No real fit, and no dependence on the git-ignored checkpoints.** Building this module
is not permission to run it, so nothing here fits an arm on the delivered development
rows or reads an approved `.pt` file. The equivalence gate is driven against a synthetic
ledger and synthetic checkpoints in `tmp_path`, which is also what makes these tests pass
on a fresh clone that carries the ledger without the weights.
"""

from __future__ import annotations

import ast
import hashlib
import json
import re
import sys
from pathlib import Path

import numpy as np
import pytest
import torch
from torch import nn

PACKET_ROOT = Path(__file__).resolve().parents[1]
SCRIPTS_DIR = PACKET_ROOT / "scripts"
sys.path.insert(0, str(SCRIPTS_DIR))

import analyze_dev_fit as approved_analysis  # noqa: E402
from utils import attribution_net_rung2 as rung2  # noqa: E402
from utils import capacity_sweep as cs  # noqa: E402
from utils import dev_fit_trainer as trainer  # noqa: E402
from utils import rung2_escalation as r2  # noqa: E402
from utils.attribution_net import (  # noqa: E402
    CAPACITY_LADDER,
    RUNG1_MAX_PARAMETERS,
    TemporalAttributionNet,
)
from utils.dev_fit_contract import (  # noqa: E402
    MATCHED_FIT_SUITES,
    PREDECLARED_TRAINING_SEEDS,
    DevFitContractError,
)
from utils.protocol_p import canonical_text_sha256  # noqa: E402

DESIGN_PATH = PACKET_ROOT / "protocol" / r2.DESIGN_DOCUMENT_NAME
APPROVED_ANALYSIS_PATH = PACKET_ROOT / r2.APPROVED_ANALYSIS_RELATIVE
APPROVED_LEDGER_PATH = PACKET_ROOT / r2.APPROVED_RESULT_RELATIVE

REGISTRY_WIDTH = 18
SYNTHETIC_WINDOW = 8
FIXED_UUID = "0123abcd-4567-89ab-cdef-0123456789ab"


# ---------------------------------------------------------------------------
# Shared fixtures: everything synthetic, nothing touching the delivered dataset
# ---------------------------------------------------------------------------
def _module_ast() -> ast.Module:
    """Return the executable's parsed AST, for checks a text search gets wrong."""

    return ast.parse(Path(r2.__file__).read_text(encoding="utf-8"))


def _example(class_index: int = 0) -> trainer.TrainingExample:
    """Return one tiny synthetic training example with the real registry width."""

    rng = np.random.default_rng(class_index + 1)
    return trainer.TrainingExample(
        run_id=f"synthetic-{class_index}",
        trajectory_spec_id="synthetic",
        values=rng.normal(size=(SYNTHETIC_WINDOW, REGISTRY_WIDTH)),
        valid=np.ones((SYNTHETIC_WINDOW, REGISTRY_WIDTH), dtype=bool),
        class_index=class_index % 4,
        location_index=class_index % 3,
        severity=0.1 * class_index,
        ood_flag=False,
    )


@pytest.fixture()
def examples() -> list[trainer.TrainingExample]:
    """Return a small synthetic example set, cheap enough to optimize instantly."""

    return [_example(0), _example(1)]


@pytest.fixture()
def protocol():
    """Return the real fixed protocol, derived from the approved assignment."""

    return r2.resolve_protocol()


@pytest.fixture()
def plan_file(tmp_path, protocol) -> tuple[Path, str, dict]:
    """Write a valid plan into `tmp_path` and return its path, digest and document."""

    document = r2.plan_document(run_label="rung2-run-1", protocol=protocol)
    path = tmp_path / "plan" / r2.PLAN_ARTIFACT
    r2.write_document(path, document)
    return path, canonical_text_sha256(path), document


def _ledger() -> dict:
    """Return an independent copy of the tracked approved ledger."""

    return json.loads(APPROVED_LEDGER_PATH.read_text(encoding="utf-8"))


def _analysis() -> dict:
    """Return an independent copy of the tracked approved analysis artifact."""

    return json.loads(APPROVED_ANALYSIS_PATH.read_text(encoding="utf-8"))


def _synthetic_equivalence_world(tmp_path):
    """Return a ledger and checkpoint dir for driving R6 without any real data.

    The two equivalence arms are given synthetic **rung-1** checkpoints on disk and
    matching ledger rows, so every branch of the gate can be driven on a machine that
    has never run the approved fit.
    """

    checkpoint_dir = tmp_path / "approved"
    checkpoint_dir.mkdir()
    arms = []
    for suite, seed in r2.EQUIVALENCE_ARMS:
        state = r2.build_rung1_reference_network(seed=seed).state_dict()
        name = f"dev_fit_{suite}_seed{seed}.pt"
        torch.save(state, checkpoint_dir / name)
        arms.append(
            {
                "suite": suite,
                "training_seed": seed,
                "checkpoint_name": name,
                "checkpoint_sha256": hashlib.sha256(
                    (checkpoint_dir / name).read_bytes()
                ).hexdigest(),
                "loss_history": [1.0, 0.5],
            }
        )
    return {"arms": arms}, checkpoint_dir


def _matching_fit(_examples, *, seed, network_factory, **_kwargs):
    """Stand in for `fit_arm` with a fit that reproduces the synthetic approved state."""

    return network_factory(seed=seed), [1.0, 0.5]


def _design_fixed_table() -> dict[str, str]:
    """Parse design section 4.1's held-fixed table out of the frozen document."""

    rows: dict[str, str] = {}
    for line in DESIGN_PATH.read_text(encoding="utf-8").splitlines():
        cells = [cell.strip().replace("*", "").replace("`", "") for cell in line.split("|")[1:-1]]
        if len(cells) == 3 and not cells[0].startswith("---") and cells[0] != "held fixed":
            rows[cells[0]] = cells[1]
    return rows


def _design_selected_row() -> list[str]:
    """Return design section 4.2's selected grid row, parsed from the document."""

    selected = []
    for line in DESIGN_PATH.read_text(encoding="utf-8").splitlines():
        cells = [cell.strip().replace("*", "").replace("`", "") for cell in line.split("|")[1:-1]]
        if len(cells) == 8 and "selected" in cells[-1]:
            selected.append(cells)
    assert len(selected) == 1, "the design must name exactly one selected grid row"
    return selected[0]


# ---------------------------------------------------------------------------
# The frozen design, checked against the document rather than against itself
# ---------------------------------------------------------------------------
def test_the_design_document_is_the_frozen_approved_version():
    """The executable is built against v0.1's exact bytes, checked against the file."""

    assert canonical_text_sha256(DESIGN_PATH) == r2.DESIGN_CANONICAL_SHA256
    assert r2.design_digest() == r2.DESIGN_CANONICAL_SHA256


def test_editing_the_frozen_design_turns_plan_mode_red(monkeypatch, protocol):
    """Invariant R11: an executable may not outlive the document that authorized it."""

    monkeypatch.setattr(r2, "DESIGN_CANONICAL_SHA256", "0" * 64)
    with pytest.raises(DevFitContractError, match="not the frozen approved v0.1"):
        r2.plan_document(run_label="rung2-run-1", protocol=protocol)


def test_the_fixed_protocol_equals_the_designs_own_table(protocol):
    """Design section 4.1's held-fixed values are checked by equality, never adopted."""

    table = _design_fixed_table()
    assert r2.RUNG2_EPOCHS == int(table["epochs"])
    assert r2.RUNG2_BATCH_SIZE == int(table["batch size"])
    assert r2.RUNG2_LEARNING_RATE == float(table["learning rate"])
    assert r2.RUNG2_DEVICE == table["device"]
    assert PREDECLARED_TRAINING_SEEDS == tuple(
        int(value) for value in table["seeds"].split(",")
    )
    assert set(MATCHED_FIT_SUITES) == {
        part.strip() for part in table["suites"].replace(" and ", ",").split(",")
    }
    assert protocol.epochs == r2.RUNG2_EPOCHS
    assert protocol.batch_size == r2.RUNG2_BATCH_SIZE
    assert protocol.learning_rate == r2.RUNG2_LEARNING_RATE
    assert protocol.device == r2.RUNG2_DEVICE


def test_the_selected_configuration_equals_the_designs_selected_row():
    """The parameter count and stem receptive field come from the design's own table."""

    row = _design_selected_row()
    assert int(row[5].replace(",", "")) == rung2.RUNG2_DECLARED_PARAMETERS
    assert int(row[0]) == rung2.RUNG2_CHANNELS
    assert int(row[1]) == rung2.RUNG2_STEM_BLOCKS
    assert int(row[2]) == rung2.RUNG2_HIDDEN_SIZE
    assert int(row[3]) == rung2.RUNG2_GRU_LAYERS
    assert int(row[4]) == rung2.RUNG2_ATTENTION_HEADS
    assert int(row[6]) == r2.rung2_shape()["stem_receptive_field"]


def test_the_multihead_counterfactual_sits_inside_the_band():
    """Only the exact count refuses the wrong attention block; the band cannot.

    The design records 228,330 parameters for the `nn.MultiheadAttention` form. That
    number is read out of the document rather than retyped, and the assertion is that it
    is **admitted** by the band -- which is why invariant R4's load-bearing check is the
    exact count and not the band.
    """

    text = DESIGN_PATH.read_text(encoding="utf-8")
    assert "228,330" in text
    counterfactual = 228_330
    assert rung2.RUNG2_MIN_PARAMETERS <= counterfactual <= rung2.RUNG2_MAX_PARAMETERS
    assert counterfactual != rung2.RUNG2_DECLARED_PARAMETERS


def test_the_band_lower_bound_is_derived_from_the_approved_rung1_constant():
    """Decision D2: contiguous and disjoint by construction, never retyped."""

    assert rung2.RUNG2_MIN_PARAMETERS == RUNG1_MAX_PARAMETERS + 1


# ---------------------------------------------------------------------------
# The arm lists, the budget and the exit vocabulary
# ---------------------------------------------------------------------------
def test_the_arm_lists_are_ten_rung2_and_two_equivalence():
    """Design section 3: two suites x five predeclared seeds, plus the ruled pair."""

    arms = r2.rung2_arms()
    assert len(arms) == 10
    assert len(set(arms)) == 10
    assert {suite for suite, _ in arms} == set(MATCHED_FIT_SUITES)
    assert {seed for _, seed in arms} == set(PREDECLARED_TRAINING_SEEDS)
    assert r2.EQUIVALENCE_ARMS == (("C1", 0), ("S", 4))
    assert r2.EQUIVALENCE_ARMS is cs.EQUIVALENCE_ARMS


def test_the_maximum_budget_is_twelve_fits():
    """The constant is pinned by equality to the arm lists it summarises."""

    assert r2.MAX_FITS == len(r2.rung2_arms()) + len(r2.EQUIVALENCE_ARMS) == 12
    assert r2.MAX_CHECKPOINTS == r2.MAX_FITS


def test_the_exit_codes_are_distinct_and_only_the_two_successes_are_zero():
    """A terminal exit is a name and a code, and two exits may not share a code."""

    codes = r2.EXIT_CODES
    zeros = {name for name, code in codes.items() if code == 0}
    assert zeros == {r2.X_PLAN_OK, r2.X_RUNG2_OK}
    non_zero = [code for name, code in codes.items() if name not in zeros]
    assert len(set(non_zero)) == len(non_zero)


def test_there_is_no_output_dirty_exit():
    """The deliberate absence, pinned so a later session does not add one back silently.

    Stage 1 needed `X_OUTPUT_DIRTY` because ten arms shared a per-width directory; rung 2
    writes every arm into a root claimed **absent** by one atomic create, so there is no
    directory an earlier attempt could have filled. Recording the decision as a test
    means re-introducing the exit is a deliberate act rather than a copy-paste.
    """

    assert not any("DIRTY" in name for name in r2.EXIT_CODES)
    assert "require_clean" not in Path(r2.__file__).read_text(encoding="utf-8")


# ---------------------------------------------------------------------------
# Invariant R4: the rung and the band are read off a constructed network
# ---------------------------------------------------------------------------
def test_the_shape_is_read_off_a_constructed_network():
    """R4: recorded, not re-derived, and equal to the design's declared figures."""

    shape = r2.rung2_shape()
    assert shape["n_parameters"] == rung2.RUNG2_DECLARED_PARAMETERS == 219_018
    assert shape["rung"] == rung2.RUNG2_NAME
    assert shape["stem_receptive_field"] == 31
    net = r2.build_rung2_network(seed=0)
    assert shape["n_parameters"] == net.n_parameters
    assert shape["stem_receptive_field"] == net.stem_receptive_field


def test_r4_refuses_a_parameter_count_that_moved(monkeypatch):
    """A configuration whose count is not the declared one is a refusal, not a note."""

    monkeypatch.setattr(r2, "RUNG2_DECLARED_PARAMETERS", 219_019)
    with pytest.raises(DevFitContractError, match="the frozen design reserves"):
        r2.rung2_shape()


def test_r4_refuses_a_network_reporting_another_rung(monkeypatch):
    """The rung is recorded from the network, so a network of another rung is refused."""

    class _OtherRung(nn.Module):
        rung = "rung3_probabilistic_ensemble_head"
        n_parameters = rung2.RUNG2_DECLARED_PARAMETERS
        stem_receptive_field = 31

    monkeypatch.setattr(r2, "build_rung2_network", lambda *, seed: _OtherRung())
    with pytest.raises(DevFitContractError, match="this executable fits"):
        r2.rung2_shape()


def test_r4_refuses_a_count_outside_the_band(monkeypatch):
    """The band assertion is defence in depth, and it is reachable."""

    class _Undersized(nn.Module):
        rung = rung2.RUNG2_NAME
        n_parameters = 82_778
        stem_receptive_field = 31

    monkeypatch.setattr(r2, "build_rung2_network", lambda *, seed: _Undersized())
    monkeypatch.setattr(r2, "RUNG2_DECLARED_PARAMETERS", 82_778)
    with pytest.raises(DevFitContractError, match="outside the band"):
        r2.rung2_shape()


def test_the_rung_names_come_from_the_approved_ladder():
    """Neither rung name is retyped in this module."""

    assert r2.RUNG1_NAME == CAPACITY_LADDER[0].name == "rung1_compact_temporal_conv"
    assert rung2.RUNG2_NAME == CAPACITY_LADDER[1].name


# ---------------------------------------------------------------------------
# Invariant R5: no enforcement bypass exists anywhere in this module
# ---------------------------------------------------------------------------
def test_no_argument_in_this_module_can_disable_the_band_check():
    """R5, checked over the AST rather than by reading: no escape hatch, anywhere.

    The rung-2 module's own R5 test uses the word list `enforce|band|skip|strict|check`
    on the constructor's signature. **`check` is deliberately absent here**, because at
    module scope it collides with the honest name `checkpoint_dir`, and a test that has
    to be argued around is worse than one whose scope is stated. What it would have
    covered is covered by `test_the_two_factories_pass_only_the_seed`, which drives the
    two constructor call sites in the AST and requires each to pass `seed` and nothing
    else -- so no parameter of any name can reach a constructor at all.
    """

    forbidden = re.compile(r"enforce|band|skip|strict|bypass|disable|override", re.IGNORECASE)
    for node in ast.walk(_module_ast()):
        if not isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef)):
            continue
        arguments = node.args
        names = [
            argument.arg
            for argument in (
                arguments.posonlyargs + arguments.args + arguments.kwonlyargs
            )
        ]
        for name in names:
            assert not forbidden.search(name), f"{node.name} takes {name}"


def test_the_command_line_offers_no_architecture_or_protocol_flag():
    """The protocol is fixed at module scope; an operator may not move it at invocation."""

    parser_flags = {
        action.option_strings[0]
        for action in r2.parse_args.__wrapped__.__defaults__  # type: ignore[attr-defined]
    } if hasattr(r2.parse_args, "__wrapped__") else None
    assert parser_flags is None  # the executable exposes no wrapped parser
    source = Path(r2.__file__).read_text(encoding="utf-8")
    for flag in (
        "--epochs",
        "--batch-size",
        "--learning-rate",
        "--device",
        "--channels",
        "--hidden-size",
        "--enforce-rung1-band",
    ):
        assert flag not in source


def test_the_two_factories_pass_only_the_seed():
    """Every size argument stays at the module's declared default, checked in the AST."""

    tree = _module_ast()
    calls: dict[str, ast.Call] = {}
    for node in ast.walk(tree):
        if isinstance(node, ast.Call) and isinstance(node.func, ast.Name):
            if node.func.id in {
                "RecurrentAttentionAttributionNet",
                "TemporalAttributionNet",
            }:
                assert node.func.id not in calls, f"{node.func.id} has two call sites"
                calls[node.func.id] = node
    assert set(calls) == {"RecurrentAttentionAttributionNet", "TemporalAttributionNet"}
    for name, call in calls.items():
        assert not call.args, f"{name} is called with a positional argument"
        assert [keyword.arg for keyword in call.keywords] == ["seed"]


def test_the_rung1_reference_factory_is_the_approved_default_configuration():
    """The gate must refit the network the approved trainer built, not a variant."""

    net = r2.build_rung1_reference_network(seed=0)
    assert isinstance(net, TemporalAttributionNet)
    assert net.channels == r2.ANCHOR_CHANNELS == 32
    assert net.n_parameters == 39_594
    assert net.receptive_field == 1_023


@pytest.mark.parametrize("seed", [5, -1, 10])
def test_both_factories_refuse_an_undeclared_seed(seed):
    """A seed outside the predeclared five never reaches a constructor."""

    with pytest.raises(DevFitContractError):
        r2.build_rung2_network(seed=seed)
    with pytest.raises(DevFitContractError):
        r2.build_rung1_reference_network(seed=seed)


# ---------------------------------------------------------------------------
# Invariant R13: matched seeds mean matched initialization
# ---------------------------------------------------------------------------
def test_same_seed_constructions_are_bit_identical():
    """R13: the C1 and S arms at one seed start from the same weights by construction."""

    left = r2.build_rung2_network(seed=2).state_dict()
    right = r2.build_rung2_network(seed=2).state_dict()
    identical, reason = r2.state_dicts_are_bit_identical(left, right)
    assert identical, reason


def test_a_different_seed_changes_at_least_one_tensor():
    """R13's second half: the seed really is what moves the initialization."""

    identical, _ = r2.state_dicts_are_bit_identical(
        r2.build_rung2_network(seed=0).state_dict(),
        r2.build_rung2_network(seed=1).state_dict(),
    )
    assert not identical


@pytest.mark.parametrize(
    "factory", [r2.build_rung2_network, r2.build_rung1_reference_network]
)
def test_construction_leaves_the_callers_cpu_rng_state_unchanged(factory):
    """R13's third half: constructing a network is not allowed to move the caller's RNG.

    This is the assertion the parameter count cannot make. Seeding before the fork builds
    the identical parameters and still mutates the global stream (finding BI).
    """

    torch.manual_seed(4321)
    before = torch.random.get_rng_state().clone()
    factory(seed=3)
    assert torch.equal(torch.random.get_rng_state(), before)


# ---------------------------------------------------------------------------
# The one loop, and the seam it exists to create
# ---------------------------------------------------------------------------
def test_the_scientific_loss_and_the_batcher_are_imported_not_reimplemented():
    """One definition of the objective across both rungs (design section 4.5)."""

    assert r2.arm_loss is trainer.arm_loss
    assert r2._stack is trainer._stack
    source = Path(r2.__file__).read_text(encoding="utf-8")
    assert "def arm_loss" not in source
    assert "def _stack" not in source


def test_the_classification_metrics_come_from_the_approved_analyzer():
    """Design section 3: no second definition of macro-F1 enters this project."""

    assert r2.score_arm is cs.score_arm
    source = Path(r2.__file__).read_text(encoding="utf-8")
    assert "def score_arm" not in source
    assert "def classification_metrics" not in source
    assert r2.approved_analysis is approved_analysis


def test_the_one_loop_reproduces_the_approved_width_path_at_thirty_two_channels(
    examples,
):
    """The precondition invariant R6 depends on, measured rather than asserted.

    If `fit_arm` with the rung-1 reference factory did not reproduce
    `capacity_sweep.fit_arm_at_width(channels=32)` bit for bit on identical inputs, the
    equivalence gate could not pass on any machine and the executable would be unrunnable
    in the shape finding AU had. The caller's global RNG is polluted first, so a loop that
    leaked the ambient stream into its initialization would be caught here rather than at
    execution time.
    """

    def _run(fit, **kwargs):
        torch.manual_seed(9_999)
        return fit(
            examples,
            epochs=2,
            batch_size=2,
            learning_rate=r2.RUNG2_LEARNING_RATE,
            device=torch.device(r2.RUNG2_DEVICE),
            **kwargs,
        )

    approved_net, approved_history = _run(
        cs.fit_arm_at_width, seed=0, channels=r2.ANCHOR_CHANNELS
    )
    produced_net, produced_history = _run(
        r2.fit_arm, seed=0, network_factory=r2.build_rung1_reference_network
    )
    identical, reason = r2.state_dicts_are_bit_identical(
        produced_net.state_dict(), approved_net.state_dict()
    )
    assert identical, reason
    assert produced_history == approved_history


def test_the_loop_fits_a_rung_two_network_through_the_same_path(examples):
    """The other factory, through the identical loop, producing the declared rung."""

    net, history = r2.fit_arm(
        examples,
        seed=0,
        network_factory=r2.build_rung2_network,
        epochs=2,
        batch_size=2,
        learning_rate=r2.RUNG2_LEARNING_RATE,
        device=torch.device(r2.RUNG2_DEVICE),
    )
    assert net.rung == rung2.RUNG2_NAME
    assert net.n_parameters == rung2.RUNG2_DECLARED_PARAMETERS
    assert len(history) == 2
    assert all(np.isfinite(value) for value in history)


def test_the_loop_refuses_an_empty_example_set():
    """A development-only fit may not consume an empty row set."""

    with pytest.raises(trainer.DevFitDataError, match="empty row set"):
        r2.fit_arm(
            [],
            seed=0,
            network_factory=r2.build_rung2_network,
            epochs=1,
            batch_size=1,
            learning_rate=1.0e-3,
            device=torch.device("cpu"),
        )


def test_the_loop_refuses_a_nonfinite_loss(monkeypatch, examples):
    """A non-finite objective stops the arm rather than producing a checkpoint."""

    monkeypatch.setattr(
        r2, "arm_loss", lambda *_args, **_kwargs: torch.tensor(float("nan"))
    )
    with pytest.raises(trainer.DevFitDataError, match="non-finite"):
        r2.fit_arm(
            examples,
            seed=0,
            network_factory=r2.build_rung2_network,
            epochs=1,
            batch_size=2,
            learning_rate=1.0e-3,
            device=torch.device("cpu"),
        )


def test_the_loop_refuses_an_undeclared_seed(examples):
    """The seed is checked before anything is constructed or optimized."""

    with pytest.raises(DevFitContractError):
        r2.fit_arm(
            examples,
            seed=7,
            network_factory=r2.build_rung2_network,
            epochs=1,
            batch_size=2,
            learning_rate=1.0e-3,
            device=torch.device("cpu"),
        )


def test_the_loop_passes_the_callers_seed_to_the_factory(examples):
    """The seed the caller names is the seed the network is built from.

    Measured in the Session-115 mutation sweep and added because of it: replacing
    `network_factory(seed=seed)` with `network_factory(seed=0)` survived the whole
    suite. Every same-seed reproducibility test still passed, because both of its runs
    were pinned to the same wrong seed, and the equivalence precondition test happens to
    use seed 0. The result would have been ten arms claiming five seeds and sharing one
    initialization -- the five-seed structure the whole paired read depends on, silently
    gone. Nothing in the module is wrong; the suite could not see it.
    """

    seen: list[int] = []

    def _recording_factory(*, seed: int):
        seen.append(seed)
        return r2.build_rung2_network(seed=seed)

    for seed in (0, 3):
        r2.fit_arm(
            examples,
            seed=seed,
            network_factory=_recording_factory,
            epochs=1,
            batch_size=2,
            learning_rate=1.0e-3,
            device=torch.device("cpu"),
        )
    assert seen == [0, 3]


def test_two_seeds_give_the_loop_two_initializations(examples):
    """The same claim again, behaviourally, without trusting the factory contract.

    `epochs=0` runs no optimizer step, so what is compared is the initialization the
    loop actually built. A second instrument for the same property, because the test
    above would be satisfied by a factory whose recorded seed and constructed weights
    disagreed.
    """

    def _fit(seed: int):
        net, history = r2.fit_arm(
            examples,
            seed=seed,
            network_factory=r2.build_rung2_network,
            epochs=0,
            batch_size=2,
            learning_rate=1.0e-3,
            device=torch.device("cpu"),
        )
        assert history == []
        return net.state_dict()

    identical, _ = r2.state_dicts_are_bit_identical(_fit(0), _fit(3))
    assert not identical


def test_the_loop_is_reproducible_at_one_seed(examples):
    """Two runs of one arm produce bit-identical weights and identical histories."""

    kwargs = dict(
        seed=1,
        network_factory=r2.build_rung2_network,
        epochs=1,
        batch_size=2,
        learning_rate=1.0e-3,
        device=torch.device("cpu"),
    )
    first_net, first_history = r2.fit_arm(examples, **kwargs)
    second_net, second_history = r2.fit_arm(examples, **kwargs)
    identical, reason = r2.state_dicts_are_bit_identical(
        first_net.state_dict(), second_net.state_dict()
    )
    assert identical, reason
    assert first_history == second_history


def test_the_row_order_is_common_across_rungs():
    """Design section 4.4 claim 2: the permutation depends only on seed and row count."""

    for seed in PREDECLARED_TRAINING_SEEDS:
        assert np.array_equal(
            np.random.default_rng(seed).permutation(152),
            np.random.default_rng(seed).permutation(152),
        )


def test_the_two_rungs_do_not_share_an_initialization():
    """Design section 4.4's third part: the tensors have different shapes, so they cannot.

    Stated as a test because the sentence a write-up would most plausibly get wrong is
    "matched seeds mean matched initialization across rungs." They do not.
    """

    rung1_state = r2.build_rung1_reference_network(seed=0).state_dict()
    rung2_state = r2.build_rung2_network(seed=0).state_dict()
    assert set(rung1_state) != set(rung2_state)
    identical, _ = r2.state_dicts_are_bit_identical(rung2_state, rung1_state)
    assert not identical


# ---------------------------------------------------------------------------
# Invariants R3 and R12: the code identity
# ---------------------------------------------------------------------------
def test_the_code_identity_is_the_eight_historical_entries_plus_four():
    """R12: the approved eight, unchanged, plus the four new producers."""

    identity = r2.rung2_code_identity()
    historical = trainer.training_code_identity()
    assert len(historical) == 8
    assert set(identity) - set(historical) == set(r2.new_identity_entries())
    assert all(identity[label] == digest for label, digest in historical.items())
    assert len(identity) == 12
    assert list(identity) == sorted(identity)
    assert all(re.fullmatch(r"[0-9a-f]{64}", value) for value in identity.values())


def test_the_four_new_entries_are_real_files_this_module_depends_on():
    """The permitted-addition set is pinned by equality and each label is a real file."""

    assert r2.new_identity_entries() == frozenset(
        {
            "analyze_dev_fit.py",
            "attribution_net_rung2.py",
            "capacity_sweep.py",
            "rung2_escalation.py",
        }
    )
    here = Path(r2.__file__).resolve().parent
    for label in r2.new_identity_entries():
        candidates = [here / label, here.parent / label]
        assert any(path.is_file() for path in candidates), label


def test_this_module_is_its_own_code_identity_entry():
    """The producer identifies itself: editing this file moves the recorded identity."""

    identity = r2.rung2_code_identity()
    from utils.dev_fit_contract import code_identity as _code_identity

    assert identity["rung2_escalation.py"] == _code_identity(
        {"rung2_escalation.py": Path(r2.__file__).resolve()}
    )["rung2_escalation.py"]


def test_r3_accepts_the_real_approved_ledger(protocol):
    """The anchor really was produced by the code, data and protocol in use now."""

    r2.require_anchor_comparability(_ledger(), protocol)


def test_r3_refuses_a_changed_historical_code_entry(protocol):
    """One moved historical digest means two unrelated experiments, not a comparison."""

    ledger = _ledger()
    ledger["code_identity"]["attribution_net.py"] = "a" * 64
    with pytest.raises(DevFitContractError, match="differs from the code that fitted"):
        r2.require_anchor_comparability(ledger, protocol)


def test_r3_refuses_an_unlisted_extra_identity_entry(protocol):
    """Exactly the four new producer entries are permitted additions."""

    ledger = _ledger()
    del ledger["code_identity"]["estimator.py"]
    with pytest.raises(DevFitContractError, match="four new producer entries"):
        r2.require_anchor_comparability(ledger, protocol)


def test_r3_refuses_a_dropped_identity_entry(protocol):
    """A historical entry the current code no longer names is a refusal."""

    ledger = _ledger()
    ledger["code_identity"]["retired_module.py"] = "b" * 64
    with pytest.raises(DevFitContractError, match="adds|drops"):
        r2.require_anchor_comparability(ledger, protocol)


@pytest.mark.parametrize("field", ["epochs", "batch_size", "learning_rate", "device"])
def test_r3_refuses_a_protocol_the_anchor_did_not_use(protocol, field):
    """A rung-2 run under a different optimization protocol is not this run."""

    ledger = _ledger()
    ledger["training_protocol"][field] = "moved" if field == "device" else 999
    with pytest.raises(DevFitContractError, match="training protocol differs"):
        r2.require_anchor_comparability(ledger, protocol)


def test_r3_refuses_a_moved_window_schedule(protocol):
    """The window policy is part of the protocol comparison, not a separate promise."""

    ledger = _ledger()
    ledger["training_protocol"]["window_schedule"] = []
    with pytest.raises(DevFitContractError, match="window_schedule"):
        r2.require_anchor_comparability(ledger, protocol)


def test_r3_refuses_wrong_role_indexes(protocol):
    """The anchor's role indexes must be the authorized delivered ones."""

    ledger = _ledger()
    ledger["role_index_sha256"]["labels/index.csv"] = "c" * 64
    with pytest.raises(DevFitContractError, match="role indexes"):
        r2.require_anchor_comparability(ledger, protocol)


def test_r3_refuses_an_anchor_arm_with_a_foreign_data_identity(protocol):
    """Every anchor arm carries the authorized manifest, config and assignment."""

    ledger = _ledger()
    ledger["arms"][0]["manifest_sha256"] = "d" * 64
    with pytest.raises(DevFitContractError, match="authorized data identity"):
        r2.require_anchor_comparability(ledger, protocol)


# ---------------------------------------------------------------------------
# Invariant R1: the approved rung-1 numbers are read, never recomputed
# ---------------------------------------------------------------------------
def test_the_ten_anchors_are_read_from_the_two_approved_documents():
    """Design section 5.2: the values are the approved artifact's, not a recomputation."""

    analysis = _analysis()
    records = r2.anchor_records(_ledger(), analysis)
    assert len(records) == 10
    by_key = {(arm["suite"], arm["seed"]): arm for arm in analysis["arms"]}
    for record in records:
        source = by_key[(record["suite"], record["seed"])]
        assert record["macro_f1"] == source["classification"]["macro_f1"]
        assert record["per_class_f1"] == dict(
            sorted(source["classification"]["per_class_f1"].items())
        )
        assert record["checkpoint_sha256"] == source["checkpoint_sha256"]
        assert record["read_only"] is True
        assert record["rung"] == r2.RUNG1_NAME


def test_the_recorded_field_paths_locate_the_recorded_values():
    """The `*_field` strings are checked against the lookup that produced the value.

    A recorded provenance string nobody drives is a sentence, not a provenance. Each
    path is split and walked against the real artifact, and the value it reaches must be
    the value the record carries.
    """

    analysis = _analysis()
    records = r2.anchor_records(_ledger(), analysis)
    by_key = {(arm["suite"], arm["seed"]): arm for arm in analysis["arms"]}
    for record in records:
        arm = by_key[(record["suite"], record["seed"])]
        for field_key, value_key in (
            ("macro_f1_field", "macro_f1"),
            ("per_class_f1_field", "per_class_f1"),
        ):
            head, *tail = record[field_key].split(".")
            assert head == "arms[]"
            reached = r2.read_field(arm, tail, "approved analysis arm")
            if isinstance(reached, dict):
                reached = dict(sorted(reached.items()))
            assert reached == record[value_key]


def test_the_anchor_read_refuses_two_documents_that_disagree_on_a_digest():
    """A cross-check whose two sides come from different files."""

    analysis = _analysis()
    analysis["arms"][0]["checkpoint_sha256"] = "e" * 64
    with pytest.raises(r2.Rung2EscalationError, match="disagree on the"):
        r2.anchor_records(_ledger(), analysis)


def test_the_anchor_read_refuses_a_missing_arm():
    """Nine anchors are not the ten identities the comparison is paired against."""

    ledger = _ledger()
    ledger["arms"] = ledger["arms"][1:]
    with pytest.raises(r2.Rung2EscalationError, match="exactly the ten approved"):
        r2.anchor_records(ledger, _analysis())


def test_the_anchor_read_refuses_a_duplicate_in_place_of_one_identity():
    """Ten rows are not ten identities; a duplicate is refused by name."""

    ledger = _ledger()
    ledger["arms"][1] = json.loads(json.dumps(ledger["arms"][0]))
    with pytest.raises(r2.Rung2EscalationError, match="duplicate"):
        r2.anchor_records(ledger, _analysis())


def test_the_anchor_read_refuses_an_absent_metric_field_by_its_own_name():
    """An absent field is refused by the path it was looked up at."""

    analysis = _analysis()
    del analysis["arms"][0]["classification"]["macro_f1"]
    with pytest.raises(r2.CapacitySweepError, match="classification.macro_f1"):
        r2.anchor_records(_ledger(), analysis)


def test_the_anchor_read_refuses_a_non_object_per_class_map():
    """The per-class map is persisted as a sorted object, so it must be one."""

    analysis = _analysis()
    analysis["arms"][0]["classification"]["per_class_f1"] = [0.1, 0.2]
    with pytest.raises(r2.Rung2EscalationError, match="non-object per-class"):
        r2.anchor_records(_ledger(), analysis)


def test_this_module_never_refits_an_anchor():
    """Invariant R1: `results/dev_fit` is a read, and its ten arms are never re-run."""

    source = Path(r2.__file__).read_text(encoding="utf-8")
    assert "dev_fit_result.json" not in source  # it arrives through the imported constant
    assert r2.APPROVED_RESULT_RELATIVE is cs.APPROVED_RESULT_RELATIVE
    tree = _module_ast()
    fit_calls = [
        node
        for node in ast.walk(tree)
        if isinstance(node, ast.Call)
        and isinstance(node.func, ast.Name)
        and node.func.id == "fit_arm"
    ]
    # Exactly two call sites: the equivalence gate's and the rung-2 arm loop's.
    assert len(fit_calls) == 2


# ---------------------------------------------------------------------------
# Plan mode
# ---------------------------------------------------------------------------
def test_plan_mode_writes_a_terminal_artifact_and_runs_zero_fits(tmp_path):
    """The plan is a terminal exit with an artifact, and it spends nothing."""

    code = r2.main(
        ["--mode", "plan", "--run-label", "rung2-run-1", "--output-dir", str(tmp_path)]
    )
    assert code == r2.EXIT_CODES[r2.X_PLAN_OK]
    document = json.loads(
        (tmp_path / r2.PLAN_ARTIFACT).read_text(encoding="utf-8")
    )
    assert document["exit"] == r2.X_PLAN_OK
    assert document["plan_valid"] is True
    assert document["mode"] == "plan"
    assert document["maximum_budget"] == {
        "checkpoints": 12,
        "fits": 12,
        "generation_runs": 0,
        "non_dev_reads": 0,
        "rollouts": 0,
    }
    assert not list(tmp_path.glob("*.pt"))


def test_the_plan_is_byte_deterministic_across_destinations(tmp_path, protocol):
    """Design section 7.1: the digest is about the run, not about the machine."""

    digests = set()
    for index in range(3):
        destination = tmp_path / f"destination-{index}" / r2.PLAN_ARTIFACT
        r2.write_document(
            destination, r2.plan_document(run_label="rung2-run-1", protocol=protocol)
        )
        digests.add(hashlib.sha256(destination.read_bytes()).hexdigest())
    assert len(digests) == 1


def test_a_different_run_label_is_a_different_plan_document(protocol):
    """The label is part of the plan's identity, not an operator convenience."""

    first = r2.plan_document(run_label="rung2-run-1", protocol=protocol)
    second = r2.plan_document(run_label="rung2-run-2", protocol=protocol)
    assert first != second
    assert first["run_label"] != second["run_label"]


def test_the_plan_serializes_no_host_path(tmp_path, protocol):
    """No absolute filesystem path may enter any artifact (design section 5.3)."""

    text = json.dumps(r2.plan_document(run_label="rung2-run-1", protocol=protocol))
    assert not re.search(r"[A-Za-z]:[\\/]", text)
    assert "//" not in text
    assert str(PACKET_ROOT) not in text
    assert str(tmp_path) not in text


def test_the_plan_declares_twelve_arms_with_their_factories_and_destinations(protocol):
    """Design section 7.1: twelve arms, their suites, seeds, factories and destinations."""

    document = r2.plan_document(run_label="rung2-run-1", protocol=protocol)
    assert document["n_rung2_arms"] == 10
    assert document["n_equivalence_arms"] == 2
    assert document["n_anchor_arms"] == 10
    namespace = document["logical_output_namespace"]
    assert namespace == f"{r2.LOGICAL_NAMESPACE_ROOT}/rung2-run-1"
    declared = {arm["checkpoint_relative_name"] for arm in document["rung2_arms"]}
    assert declared == {
        f"{namespace}/{r2.rung2_checkpoint_name(suite, seed)}"
        for suite, seed in r2.rung2_arms()
    }
    assert {arm["network_factory"] for arm in document["rung2_arms"]} == {
        "build_rung2_network"
    }
    assert {arm["network_factory"] for arm in document["equivalence_arms"]} == {
        "build_rung1_reference_network"
    }
    assert len(declared | {arm["checkpoint_relative_name"] for arm in document["equivalence_arms"]}) == 12


def test_the_plan_states_the_rung_the_band_and_the_expected_parameter_count(protocol):
    """A reader of the plan alone can check what is about to be built."""

    document = r2.plan_document(run_label="rung2-run-1", protocol=protocol)
    assert document["rung"] == rung2.RUNG2_NAME
    assert document["rung2_band"] == {
        "declared_parameters": rung2.RUNG2_DECLARED_PARAMETERS,
        "maximum_parameters": rung2.RUNG2_MAX_PARAMETERS,
        "minimum_parameters": rung2.RUNG2_MIN_PARAMETERS,
    }
    assert all(
        arm["n_parameters"] == rung2.RUNG2_DECLARED_PARAMETERS
        for arm in document["rung2_arms"]
    )
    assert document["design_sha256"] == r2.DESIGN_CANONICAL_SHA256
    assert document["code_identity"] == r2.rung2_code_identity()


def test_the_plan_declares_the_anchor_read_without_asserting_its_numbers(protocol):
    """A plan may declare what will be read; it may not report a measurement.

    The anchor macro-F1 values are recorded by the **run** that reads them. If the plan
    carried them it would be asserting a measurement it never made, and two documents
    would then hold the same number with nothing comparing them.
    """

    document = r2.plan_document(run_label="rung2-run-1", protocol=protocol)
    for anchor in document["anchor_arms"]:
        assert set(anchor) == {
            "checkpoint_sha256",
            "macro_f1_field",
            "per_class_f1_field",
            "read_only",
            "rung",
            "seed",
            "suite",
        }
    assert document["approved_analysis_sha256"] == canonical_text_sha256(
        APPROVED_ANALYSIS_PATH
    )
    assert document["approved_fit_ledger_sha256"] == canonical_text_sha256(
        APPROVED_LEDGER_PATH
    )


def test_the_equivalence_namespace_is_a_reserved_subtree_of_the_run_root(protocol):
    """The two compatibility checkpoints live inside the run whose gate they are."""

    document = r2.plan_document(run_label="rung2-run-1", protocol=protocol)
    namespace = document["logical_output_namespace"]
    assert document["equivalence_relative_namespace"] == (
        f"{namespace}/{r2.EQUIVALENCE_SUBTREE}"
    )
    for arm in document["equivalence_arms"]:
        assert arm["checkpoint_relative_name"].startswith(
            f"{namespace}/{r2.EQUIVALENCE_SUBTREE}/"
        )
    assert r2.APPROVED_CHECKPOINT_RELATIVE not in document["equivalence_relative_namespace"]


def test_plan_mode_refuses_a_bad_label_and_still_writes_a_terminal_artifact(tmp_path):
    """A refusal is a terminal too, and terminals persist."""

    code = r2.main(
        ["--mode", "plan", "--run-label", "Bad_Label", "--output-dir", str(tmp_path)]
    )
    assert code == r2.EXIT_CODES[r2.X_CONTRACT_REFUSED]
    document = json.loads((tmp_path / r2.PLAN_ARTIFACT).read_text(encoding="utf-8"))
    assert document["exit"] == r2.X_CONTRACT_REFUSED
    assert document["plan_valid"] is False
    assert document["reason_class"] == "DevFitContractError"
    assert document["fits_attempted"] == 0
    assert document["rollouts_spent"] == 0


def test_plan_mode_refuses_a_missing_label(tmp_path):
    """The label is required; it is not defaulted."""

    assert r2.main(["--mode", "plan", "--output-dir", str(tmp_path)]) == (
        r2.EXIT_CODES[r2.X_CONTRACT_REFUSED]
    )


def test_plan_mode_refuses_a_missing_output_directory_and_prints_zero_counts(capsys):
    """One of the two boundaries with nowhere authorized to persist (invariant R8)."""

    code = r2.main(["--mode", "plan", "--run-label", "rung2-run-1"])
    assert code == r2.EXIT_CODES[r2.X_CONTRACT_REFUSED]
    printed = capsys.readouterr().out
    assert "requires --output-dir" in printed
    assert r2.zero_resource_line() in printed


# ---------------------------------------------------------------------------
# The authorization gate
# ---------------------------------------------------------------------------
def test_the_gate_accepts_the_plan_it_was_given(plan_file, protocol):
    """The accept side, so the refusals below are not a gate that refuses everything."""

    path, digest, document = plan_file
    assert (
        r2.require_authorized_plan(path, expected_sha256=digest, protocol=protocol)
        == document
    )


def test_the_gate_refuses_a_digest_that_names_another_document(plan_file, protocol):
    """`--approved-plan-sha256` names a document; a different one does not pass."""

    path, _, _ = plan_file
    with pytest.raises(DevFitContractError, match="not the authorized digest"):
        r2.require_authorized_plan(path, expected_sha256="f" * 64, protocol=protocol)


@pytest.mark.parametrize("digest", ["", "abc", "A" * 64, "g" * 64, "0" * 63, None])
def test_the_gate_refuses_a_malformed_digest(plan_file, protocol, digest):
    """The digest is 64 lowercase hex characters or it is not a digest."""

    path, _, _ = plan_file
    with pytest.raises(DevFitContractError, match="64 lowercase hex"):
        r2.require_authorized_plan(path, expected_sha256=digest, protocol=protocol)


@pytest.mark.parametrize(
    "key,value,message",
    [
        ("mode", "execute", "not a plan"),
        ("exit", "X_CONTRACT_REFUSED", "not a terminal plan"),
        ("plan_valid", False, "not valid"),
        ("design_sha256", "0" * 64, "different design document"),
        ("run_label", "Bad_Label", "run_label must match"),
        ("n_rung2_arms", 9, "not the plan this executable builds"),
    ],
)
def test_the_gate_refuses_a_mutated_plan(tmp_path, protocol, key, value, message):
    """Every field the gate names is driven, not merely present in the source."""

    document = r2.plan_document(run_label="rung2-run-1", protocol=protocol)
    document[key] = value
    path = tmp_path / r2.PLAN_ARTIFACT
    r2.write_document(path, document)
    with pytest.raises(DevFitContractError, match=message):
        r2.require_authorized_plan(
            path, expected_sha256=canonical_text_sha256(path), protocol=protocol
        )


def test_the_gate_refuses_a_plan_written_by_another_code_state(tmp_path, protocol):
    """Invariant R12: the plan's identity map must equal the current one, entry by entry."""

    document = r2.plan_document(run_label="rung2-run-1", protocol=protocol)
    document["code_identity"] = dict(document["code_identity"])
    document["code_identity"]["rung2_escalation.py"] = "0" * 64
    path = tmp_path / r2.PLAN_ARTIFACT
    r2.write_document(path, document)
    with pytest.raises(DevFitContractError, match="different code state"):
        r2.require_authorized_plan(
            path, expected_sha256=canonical_text_sha256(path), protocol=protocol
        )


def test_the_gate_refuses_an_absent_document(tmp_path, protocol):
    """A digest naming a file that is not there is not an authorization."""

    with pytest.raises(DevFitContractError, match="not present"):
        r2.require_authorized_plan(
            tmp_path / "absent.json", expected_sha256="0" * 64, protocol=protocol
        )


def test_an_unauthorized_plan_claims_no_run_root(tmp_path, plan_file, monkeypatch):
    """R12 is established before the first fit, and before the root is even claimed."""

    path, _, _ = plan_file
    code = r2.main(
        [
            "--mode",
            "execute",
            "--base-dir",
            str(tmp_path / "base"),
            "--approved-plan",
            str(path),
            "--approved-plan-sha256",
            "f" * 64,
            "--data-root",
            str(tmp_path / "data"),
        ]
    )
    assert code == r2.EXIT_CODES[r2.X_PLAN_UNAUTHORIZED]
    assert not (tmp_path / "base" / "rung2-run-1").exists()
    sink = tmp_path / "base" / r2.REFUSAL_SINK_NAME / r2.UNBOUND_LABEL_DIRECTORY
    written = list(sink.glob("*.json"))
    assert len(written) == 1
    refusal = json.loads(written[0].read_text(encoding="utf-8"))
    assert refusal["exit"] == r2.X_PLAN_UNAUTHORIZED
    assert refusal["run_label"] is None
    assert refusal["approved_plan_sha256"] is None
    assert refusal["fits_attempted"] == refusal["rollouts_spent"] == 0


# ---------------------------------------------------------------------------
# Invariant R1: the protected base, and the exits that persist nothing
# ---------------------------------------------------------------------------
def test_the_real_approved_checkpoint_tree_is_the_one_the_guard_protects():
    """R1 names the real directory, checked without any invocation that could write.

    This is a pure function call: if the guard were removed it would return instead of
    raising and this test would go red, and **no write is reachable from here even
    then**. That property is deliberate -- see the test below.
    """

    protected = PACKET_ROOT / r2.APPROVED_CHECKPOINT_RELATIVE
    assert (protected / "dev_fit_result.json").is_file()
    with pytest.raises(r2.ForbiddenBase):
        r2.require_permitted_base(protected)
    with pytest.raises(r2.ForbiddenBase):
        r2.require_permitted_base(protected / "nested")
    r2.require_permitted_base(protected.parent)


def _redirect_packet_root(monkeypatch, tmp_path) -> Path:
    """Stand a protected tree up inside `tmp_path` and point both modules at it.

    `require_permitted_base` is the approved module's, so it resolves `packet_root`
    in **that** module's globals; both are redirected or the guard would still be
    measuring the real packet.

    Why this exists, and it is the point rather than a convenience: a test that drives
    a destructive guard by aiming a **real** protected path at `main()` is safe only
    while the guard is present. In the Session-115 mutation sweep the case that removed
    the guard from execute mode was correctly caught -- and the mutant, before failing,
    wrote its refusal sink into the real `results/dev_fit` tree. The approved artifacts
    were untouched and the leftover directory was removed, but the shape is finding AU's:
    a check that brackets a spend cannot protect the thing it is bracketing. Redirecting
    the root makes the mutant's write land in `tmp_path`, where it is harmless, while the
    assertion that nothing was written still fires.
    """

    fake_packet = tmp_path / "packet"
    protected = fake_packet / r2.APPROVED_CHECKPOINT_RELATIVE
    protected.mkdir(parents=True)
    (protected / "dev_fit_result.json").write_text("{}", encoding="utf-8")
    monkeypatch.setattr(r2, "packet_root", lambda: fake_packet)
    monkeypatch.setattr(cs, "packet_root", lambda: fake_packet)
    return protected


def test_a_base_inside_the_approved_checkpoint_tree_writes_absolutely_nothing(
    tmp_path, monkeypatch, capsys
):
    """R1's disclosed no-artifact boundary, and R8's stdout counts."""

    protected = _redirect_packet_root(monkeypatch, tmp_path)
    before = sorted(str(path.relative_to(protected)) for path in protected.rglob("*"))
    code = r2.main(
        [
            "--mode",
            "execute",
            "--base-dir",
            str(protected / "nested"),
            "--approved-plan",
            str(protected / "plan.json"),
            "--approved-plan-sha256",
            "0" * 64,
            "--data-root",
            str(protected),
        ]
    )
    assert code == r2.EXIT_CODES[r2.X_FORBIDDEN_BASE]
    printed = capsys.readouterr().out
    assert r2.X_FORBIDDEN_BASE in printed
    assert r2.zero_resource_line() in printed
    assert sorted(str(path.relative_to(protected)) for path in protected.rglob("*")) == (
        before
    )


def test_plan_mode_also_refuses_an_output_dir_inside_the_protected_tree(
    tmp_path, monkeypatch, capsys
):
    """R1 constrains the executable, not one of its modes."""

    protected = _redirect_packet_root(monkeypatch, tmp_path)
    before = sorted(str(path.relative_to(protected)) for path in protected.rglob("*"))
    code = r2.main(
        ["--mode", "plan", "--run-label", "rung2-run-1", "--output-dir", str(protected)]
    )
    assert code == r2.EXIT_CODES[r2.X_FORBIDDEN_BASE]
    assert r2.zero_resource_line() in capsys.readouterr().out
    assert sorted(str(path.relative_to(protected)) for path in protected.rglob("*")) == (
        before
    )


def test_a_sibling_of_the_protected_directory_is_permitted(tmp_path):
    """The guard names one tree, not every tree that looks like it."""

    assert r2.require_permitted_base(tmp_path) == tmp_path.resolve()


# ---------------------------------------------------------------------------
# Invariants R2 and R9: the run root and the duplicated refusal writer
# ---------------------------------------------------------------------------
def test_the_two_reserved_sink_names_are_unreachable_by_construction():
    """No conforming label can name either sink, because the grammar has no underscore."""

    for reserved in (r2.REFUSAL_SINK_NAME, r2.UNBOUND_LABEL_DIRECTORY):
        assert "_" in reserved
        with pytest.raises(DevFitContractError):
            r2.require_run_label(reserved)


def test_r9_both_writers_agree_on_the_payload_and_differ_only_in_the_sink(tmp_path):
    """Invariant R9: the copy is pinned to its approved original by measurement.

    One fixed valid UUID, one document, both writers. The bytes they write must be
    exactly equal and the paths must differ in exactly one component -- the sink
    directory name. Any drift in the copied body that changes a payload turns this red.
    """

    document = r2.refusal_document(
        exit_name=r2.X_RUN_ROOT_OCCUPIED,
        reason_class="RunRootOccupied",
        run_label="rung2-run-1",
        approved_plan_sha256="a" * 64,
        attempt_uuid=FIXED_UUID,
        elapsed_s=1.5,
    )
    approved_base = tmp_path / "approved-writer"
    copied_base = tmp_path / "copied-writer"
    approved_path = cs.write_refusal_document(approved_base, "rung2-run-1", document)
    copied_path = r2.write_rung2_refusal_document(copied_base, "rung2-run-1", document)
    assert approved_path.read_bytes() == copied_path.read_bytes()

    approved_parts = approved_path.relative_to(approved_base).parts
    copied_parts = copied_path.relative_to(copied_base).parts
    assert len(approved_parts) == len(copied_parts) == 3
    differing = [
        index
        for index, (left, right) in enumerate(zip(approved_parts, copied_parts))
        if left != right
    ]
    assert differing == [0]
    assert approved_parts[0] == cs.REFUSAL_SINK_NAME
    assert copied_parts[0] == r2.REFUSAL_SINK_NAME
    assert copied_parts[2] == f"{FIXED_UUID}.json"


def test_the_refusal_writer_draws_a_new_name_rather_than_overwriting(tmp_path):
    """A second refusal at one label may not destroy the first."""

    document = r2.refusal_document(
        exit_name=r2.X_RUN_ROOT_OCCUPIED,
        reason_class="RunRootOccupied",
        run_label="rung2-run-1",
        approved_plan_sha256=None,
        attempt_uuid=FIXED_UUID,
        elapsed_s=0.5,
    )
    first = r2.write_rung2_refusal_document(tmp_path, "rung2-run-1", document)
    second = r2.write_rung2_refusal_document(tmp_path, "rung2-run-1", document)
    assert first != second
    assert first.is_file() and second.is_file()
    assert json.loads(second.read_text(encoding="utf-8"))["attempt_uuid"] != FIXED_UUID


def test_a_refusal_document_records_no_message_and_no_path(tmp_path):
    """Design section 6 R2: the reason class, never the message and never a path."""

    document = r2.refusal_document(
        exit_name=r2.X_PLAN_UNAUTHORIZED,
        reason_class="DevFitContractError",
        run_label=None,
        approved_plan_sha256=None,
        attempt_uuid=FIXED_UUID,
        elapsed_s=0.25,
    )
    text = json.dumps(document)
    assert not re.search(r"[A-Za-z]:[\\/]", text)
    assert str(tmp_path) not in text
    assert set(document) == {
        "approved_plan_sha256",
        "attempt_uuid",
        "authority",
        "checkpoints_written",
        "elapsed_s",
        "exit",
        "fits_attempted",
        "generation_runs",
        "non_dev_reads",
        "reason_class",
        "rollouts_spent",
        "run_label",
    }


@pytest.mark.parametrize("occupant", ["empty-directory", "populated-directory", "file"])
def test_an_occupied_run_root_is_refused_and_never_touched(tmp_path, plan_file, occupant):
    """R2: one atomic create, and the preserved evidence is not overwritten."""

    path, digest, _ = plan_file
    base = tmp_path / "base"
    base.mkdir()
    occupied = base / "rung2-run-1"
    if occupant == "file":
        occupied.write_text("preserved evidence", encoding="utf-8")
        before = occupied.read_text(encoding="utf-8")
    else:
        occupied.mkdir()
        if occupant == "populated-directory":
            (occupied / "earlier.json").write_text("{}", encoding="utf-8")
        before = sorted(item.name for item in occupied.iterdir())
    code = r2.main(
        [
            "--mode",
            "execute",
            "--base-dir",
            str(base),
            "--approved-plan",
            str(path),
            "--approved-plan-sha256",
            digest,
            "--data-root",
            str(tmp_path / "data"),
        ]
    )
    assert code == r2.EXIT_CODES[r2.X_RUN_ROOT_OCCUPIED]
    if occupant == "file":
        assert occupied.read_text(encoding="utf-8") == before
    else:
        assert sorted(item.name for item in occupied.iterdir()) == before
    sink = base / r2.REFUSAL_SINK_NAME / "rung2-run-1"
    written = list(sink.glob("*.json"))
    assert len(written) == 1
    refusal = json.loads(written[0].read_text(encoding="utf-8"))
    assert refusal["exit"] == r2.X_RUN_ROOT_OCCUPIED
    assert refusal["run_label"] == "rung2-run-1"
    assert refusal["approved_plan_sha256"] == digest


def test_the_refusal_sink_is_a_sibling_of_the_run_root(tmp_path):
    """A refusal must never report through the resource whose occupancy triggered it."""

    document = r2.refusal_document(
        exit_name=r2.X_RUN_ROOT_OCCUPIED,
        reason_class="RunRootOccupied",
        run_label="rung2-run-1",
        approved_plan_sha256=None,
        attempt_uuid=FIXED_UUID,
        elapsed_s=0.1,
    )
    written = r2.write_rung2_refusal_document(tmp_path, "rung2-run-1", document)
    assert r2.REFUSAL_SINK_NAME in written.parts
    assert (tmp_path / "rung2-run-1") not in written.parents


def test_the_run_root_is_claimed_by_one_atomic_create(tmp_path):
    """`exist_ok=False` is the claim; an empty leftover directory is still occupied."""

    (tmp_path / "rung2-run-1").mkdir()
    with pytest.raises(r2.RunRootOccupied):
        r2.claim_run_root(tmp_path, "rung2-run-1")


# ---------------------------------------------------------------------------
# Invariant R6: the equivalence gate, driven without any real checkpoint
# ---------------------------------------------------------------------------
def test_the_gate_passes_and_writes_into_the_reserved_subtree(
    tmp_path, examples, protocol, monkeypatch
):
    """The accept side, the placement of what it writes, and the recorded fields."""

    ledger, checkpoint_dir = _synthetic_equivalence_world(tmp_path)
    monkeypatch.setattr(r2, "fit_arm", _matching_fit)
    run_root = tmp_path / "run"
    document = r2.equivalence_gate(
        examples_by_suite={suite: examples for suite in MATCHED_FIT_SUITES},
        ledger=ledger,
        checkpoint_dir=checkpoint_dir,
        scratch_dir=run_root / r2.EQUIVALENCE_SUBTREE,
        protocol=protocol,
    )
    assert document["gate_passed"] is True
    assert document["fits_attempted"] == document["checkpoints_written"] == 2
    assert document["rollouts_spent"] == document["generation_runs"] == 0
    assert document["non_dev_reads"] == 0
    assert document["equivalence_rung"] == r2.RUNG1_NAME
    for arm in document["arms"]:
        assert arm["equivalence_status"] == r2.COMPARISON_PASS
        assert arm["status"] == r2.ARM_COMPLETED
        assert arm["weights_bit_identical"] is True
        assert arm["loss_history_bit_identical"] is True
        assert arm["approved_loss_history"] == [1.0, 0.5]
        assert arm["refit_loss_history"] == [1.0, 0.5]
        assert re.fullmatch(r"[0-9a-f]{64}", arm["rung1_reference_checkpoint_sha256"])
        assert re.fullmatch(r"[0-9a-f]{64}", arm["refit_checkpoint_sha256"])
        assert arm["fit_code_identity"] == document["code_identity"]
    scratch = run_root / r2.EQUIVALENCE_SUBTREE
    assert (scratch / r2.EQUIVALENCE_ARTIFACT).is_file()
    assert len(list(scratch.glob("*.pt"))) == 2


def test_the_gate_writes_its_checkpoints_at_the_exact_names_the_plan_declares(
    tmp_path, examples, protocol, monkeypatch
):
    """The plan promises two paths; this proves the gate produces those two paths."""

    ledger, checkpoint_dir = _synthetic_equivalence_world(tmp_path)
    monkeypatch.setattr(r2, "fit_arm", _matching_fit)
    run_root = tmp_path / "run"
    document = r2.equivalence_gate(
        examples_by_suite={suite: examples for suite in MATCHED_FIT_SUITES},
        ledger=ledger,
        checkpoint_dir=checkpoint_dir,
        scratch_dir=run_root / r2.EQUIVALENCE_SUBTREE,
        protocol=protocol,
    )
    declared = {
        r2.equivalence_relative_name(suite, seed) for suite, seed in r2.EQUIVALENCE_ARMS
    }
    written = {
        str(path.relative_to(run_root)).replace("\\", "/")
        for path in (run_root / r2.EQUIVALENCE_SUBTREE).glob("*.pt")
    }
    assert written == declared
    assert {arm["refit_checkpoint_relative_name"] for arm in document["arms"]} == declared


def test_the_equivalence_checkpoint_name_has_exactly_one_definition():
    """One definition of the name, so the plan and the gate cannot drift apart."""

    source = Path(r2.__file__).read_text(encoding="utf-8")
    assert source.count("rung2_escalation_equivalence_{suite}_seed{seed}.pt") == 1
    assert source.count("rung2_escalation_{suite}_seed{seed}.pt") == 1
    assert r2.equivalence_checkpoint_name("C1", 0) == (
        "rung2_escalation_equivalence_C1_seed0.pt"
    )
    assert r2.rung2_checkpoint_name("C1", 0) == "rung2_escalation_C1_seed0.pt"
    with pytest.raises(DevFitContractError):
        r2.equivalence_checkpoint_name("C0", 0)
    with pytest.raises(DevFitContractError):
        r2.rung2_checkpoint_name("C1", 99)


def test_the_gate_refuses_when_an_approved_checkpoint_is_absent(
    tmp_path, examples, protocol
):
    """A fresh clone carries the ledger without the weights; that is a refusal."""

    ledger, checkpoint_dir = _synthetic_equivalence_world(tmp_path)
    for path in checkpoint_dir.glob("*.pt"):
        path.unlink()
    with pytest.raises(r2.EquivalenceFailure, match="not on disk") as caught:
        r2.equivalence_gate(
            examples_by_suite={suite: examples for suite in MATCHED_FIT_SUITES},
            ledger=ledger,
            checkpoint_dir=checkpoint_dir,
            scratch_dir=tmp_path / "run" / r2.EQUIVALENCE_SUBTREE,
            protocol=protocol,
        )
    document = caught.value.document
    assert document["fits_attempted"] == document["checkpoints_written"] == 0
    assert [arm["status"] for arm in document["arms"]] == [
        r2.ARM_REFUSED,
        r2.ARM_UNATTEMPTED,
    ]
    assert (tmp_path / "run" / r2.EQUIVALENCE_SUBTREE / r2.EQUIVALENCE_ARTIFACT).is_file()


def test_the_gate_refuses_when_the_ledger_has_no_row_for_an_arm(
    tmp_path, examples, protocol
):
    """The comparison must be makeable, and this is one way it is not."""

    ledger, checkpoint_dir = _synthetic_equivalence_world(tmp_path)
    ledger["arms"] = ledger["arms"][1:]
    with pytest.raises(r2.EquivalenceFailure, match="no .* arm to compare against"):
        r2.equivalence_gate(
            examples_by_suite={suite: examples for suite in MATCHED_FIT_SUITES},
            ledger=ledger,
            checkpoint_dir=checkpoint_dir,
            scratch_dir=tmp_path / "run" / r2.EQUIVALENCE_SUBTREE,
            protocol=protocol,
        )


def test_the_gate_authenticates_the_approved_bytes_before_fitting(
    tmp_path, examples, protocol, monkeypatch
):
    """The ledger digest names the bytes loaded; a same-name replacement cannot pass."""

    ledger, checkpoint_dir = _synthetic_equivalence_world(tmp_path)
    ledger["arms"][0]["checkpoint_sha256"] = "0" * 64

    def _must_not_run(*_args, **_kwargs):
        raise AssertionError("the gate fitted before authenticating the approved bytes")

    monkeypatch.setattr(r2, "fit_arm", _must_not_run)
    with pytest.raises(
        r2.EquivalenceFailure, match="digest in the approved ledger"
    ) as caught:
        r2.equivalence_gate(
            examples_by_suite={suite: examples for suite in MATCHED_FIT_SUITES},
            ledger=ledger,
            checkpoint_dir=checkpoint_dir,
            scratch_dir=tmp_path / "run" / r2.EQUIVALENCE_SUBTREE,
            protocol=protocol,
        )
    document = caught.value.document
    assert document["fits_attempted"] == document["checkpoints_written"] == 0
    assert document["arms"][0]["reason_class"] == "ApprovedCheckpointDigestMismatch"


def test_the_gate_refuses_when_the_produced_weights_differ(
    tmp_path, examples, protocol, monkeypatch
):
    """The gate's whole purpose: a diverged loop must not produce a rung-2 number."""

    ledger, checkpoint_dir = _synthetic_equivalence_world(tmp_path)

    def _diverged(_examples, *, seed, network_factory, **_kwargs):
        net = network_factory(seed=seed)
        with torch.no_grad():
            next(iter(net.parameters())).add_(1.0)
        return net, [1.0, 0.5]

    monkeypatch.setattr(r2, "fit_arm", _diverged)
    with pytest.raises(
        r2.EquivalenceFailure, match="did not reproduce the approved"
    ) as caught:
        r2.equivalence_gate(
            examples_by_suite={suite: examples for suite in MATCHED_FIT_SUITES},
            ledger=ledger,
            checkpoint_dir=checkpoint_dir,
            scratch_dir=tmp_path / "run" / r2.EQUIVALENCE_SUBTREE,
            protocol=protocol,
        )
    assert caught.value.document["arms"][0]["weights_bit_identical"] is False


def test_the_gate_refuses_when_only_the_loss_history_differs(
    tmp_path, examples, protocol, monkeypatch
):
    """Identical weights are not enough: the per-epoch history is part of the claim.

    The difference used here is **one part in 10^9**, deliberately below any tolerance a
    reviewer might reach for. "Bit-identical" has to be tested at bit scale, which is the
    Session-92 measurement applied to this gate.
    """

    ledger, checkpoint_dir = _synthetic_equivalence_world(tmp_path)

    def _wrong_history(_examples, *, seed, network_factory, **_kwargs):
        return network_factory(seed=seed), [1.0, 0.5 + 1.0e-9]

    monkeypatch.setattr(r2, "fit_arm", _wrong_history)
    with pytest.raises(
        r2.EquivalenceFailure, match="per-epoch loss history"
    ) as caught:
        r2.equivalence_gate(
            examples_by_suite={suite: examples for suite in MATCHED_FIT_SUITES},
            ledger=ledger,
            checkpoint_dir=checkpoint_dir,
            scratch_dir=tmp_path / "run" / r2.EQUIVALENCE_SUBTREE,
            protocol=protocol,
        )
    arm = caught.value.document["arms"][0]
    assert arm["weights_bit_identical"] is True
    assert arm["loss_history_bit_identical"] is False


def test_a_gate_failure_preserves_the_first_pass_and_the_second_failure(
    tmp_path, examples, protocol, monkeypatch
):
    """A later refusal cannot erase a fit or checkpoint the first arm already spent."""

    ledger, checkpoint_dir = _synthetic_equivalence_world(tmp_path)

    def _second_differs(_examples, *, seed, network_factory, **_kwargs):
        history = [1.0, 0.5] if seed == 0 else [1.0, 0.5 + 1.0e-9]
        return network_factory(seed=seed), history

    monkeypatch.setattr(r2, "fit_arm", _second_differs)
    scratch = tmp_path / "run" / r2.EQUIVALENCE_SUBTREE
    with pytest.raises(r2.EquivalenceFailure, match="per-epoch loss history") as caught:
        r2.equivalence_gate(
            examples_by_suite={suite: examples for suite in MATCHED_FIT_SUITES},
            ledger=ledger,
            checkpoint_dir=checkpoint_dir,
            scratch_dir=scratch,
            protocol=protocol,
        )
    document = caught.value.document
    assert document["fits_attempted"] == document["checkpoints_written"] == 2
    assert [arm["status"] for arm in document["arms"]] == [r2.ARM_COMPLETED] * 2
    assert [arm["equivalence_status"] for arm in document["arms"]] == [
        r2.COMPARISON_PASS,
        r2.COMPARISON_FAIL,
    ]
    assert json.loads((scratch / r2.EQUIVALENCE_ARTIFACT).read_text(encoding="utf-8")) == (
        document
    )


def test_the_gate_passes_the_rung1_factory_and_nothing_else(
    tmp_path, examples, protocol, monkeypatch
):
    """Design section 4.5: the gate differs from the measured arms only in the factory."""

    ledger, checkpoint_dir = _synthetic_equivalence_world(tmp_path)
    seen: list[object] = []

    def _record(_examples, *, seed, network_factory, **kwargs):
        seen.append((network_factory, sorted(kwargs)))
        return network_factory(seed=seed), [1.0, 0.5]

    monkeypatch.setattr(r2, "fit_arm", _record)
    r2.equivalence_gate(
        examples_by_suite={suite: examples for suite in MATCHED_FIT_SUITES},
        ledger=ledger,
        checkpoint_dir=checkpoint_dir,
        scratch_dir=tmp_path / "run" / r2.EQUIVALENCE_SUBTREE,
        protocol=protocol,
    )
    assert [factory for factory, _ in seen] == [r2.build_rung1_reference_network] * 2
    assert {tuple(keys) for _, keys in seen} == {
        ("batch_size", "device", "epochs", "learning_rate")
    }


# ---------------------------------------------------------------------------
# Execute mode's terminals
# ---------------------------------------------------------------------------
def _stub_execute(monkeypatch, protocol, *, gate, fit=None):
    """Wire execute mode onto synthetic inputs so its terminals can be driven."""

    identity = r2.rung2_code_identity()
    monkeypatch.setattr(r2, "resolve_protocol", lambda: protocol)
    monkeypatch.setattr(
        r2,
        "require_authorized_plan",
        lambda *_args, **_kwargs: {
            "code_identity": identity,
            "run_label": "rung2-run-1",
        },
    )
    monkeypatch.setattr(
        r2,
        "rung2_shape",
        lambda: {
            "n_parameters": rung2.RUNG2_DECLARED_PARAMETERS,
            "rung": rung2.RUNG2_NAME,
            "stem_receptive_field": 31,
        },
    )
    monkeypatch.setattr(r2, "read_json_document", lambda *_args, **_kwargs: {})
    monkeypatch.setattr(r2, "require_anchor_comparability", lambda *_args: None)
    monkeypatch.setattr(r2, "require_approved_analyzer_identity", lambda *_args: "a" * 64)
    monkeypatch.setattr(r2, "canonical_text_sha256", lambda *_args: "b" * 64)
    monkeypatch.setattr(
        r2,
        "anchor_records",
        lambda *_args: [
            {
                "macro_f1": 0.5,
                "read_only": True,
                "rung": r2.RUNG1_NAME,
                "seed": seed,
                "suite": suite,
            }
            for suite, seed in r2.rung2_arms()
        ],
    )
    monkeypatch.setattr(
        r2,
        "load_dev_examples",
        lambda *_args: ({suite: [_example(0)] for suite in MATCHED_FIT_SUITES}, {"role": "dev"}),
    )
    monkeypatch.setattr(r2, "equivalence_gate", gate)
    if fit is not None:
        monkeypatch.setattr(r2, "fit_arm", fit)
        monkeypatch.setattr(
            r2,
            "score_arm",
            lambda *_args: {
                "accuracy": 0.5,
                "macro_f1": 0.25,
                "per_class_f1": {"structure": 0.1, "actuator": 0.2},
            },
        )
    return identity


def _execute_argv(tmp_path):
    """Return the execute-mode command line the stubbed terminals are driven through."""

    return [
        "--mode",
        "execute",
        "--base-dir",
        str(tmp_path),
        "--approved-plan",
        str(tmp_path / "synthetic-plan.json"),
        "--approved-plan-sha256",
        "a" * 64,
        "--data-root",
        str(tmp_path / "synthetic-data"),
    ]


def test_a_gate_failure_terminal_preserves_every_arm_identity(
    tmp_path, protocol, monkeypatch
):
    """The exception-to-terminal seam keeps identities and splits the resource counts."""

    gate_arms = r2.initial_equivalence_arm_records()
    gate_arms[0].update(
        {"equivalence_status": r2.COMPARISON_PASS, "status": r2.ARM_COMPLETED}
    )
    gate_arms[1].update(
        {
            "equivalence_status": r2.COMPARISON_FAIL,
            "reason_class": "LossHistoryDiffers",
            "status": r2.ARM_COMPLETED,
        }
    )

    def _fail(**_kwargs):
        raise r2.EquivalenceFailure(
            "second comparison failed",
            document={
                "arms": gate_arms,
                "checkpoints_written": 2,
                "fits_attempted": 2,
            },
        )

    _stub_execute(monkeypatch, protocol, gate=_fail)
    assert r2.main(_execute_argv(tmp_path)) == r2.EXIT_CODES[r2.X_EQUIVALENCE_FAILED]
    document = json.loads(
        (tmp_path / "rung2-run-1" / r2.RUN_ARTIFACT).read_text(encoding="utf-8")
    )
    assert document["exit"] == r2.X_EQUIVALENCE_FAILED
    assert document["reason_class"] == "EquivalenceFailure"
    assert len(document["rung2_arms"]) == 10
    assert all(arm["status"] == r2.ARM_UNATTEMPTED for arm in document["rung2_arms"])
    assert document["equivalence_arms"] == gate_arms
    assert document["equivalence_fits_attempted"] == 2
    assert document["equivalence_checkpoints_written"] == 2
    assert document["rung2_fits_attempted"] == 0
    assert document["rung2_checkpoints_written"] == 0
    assert document["fits_attempted"] == 2
    assert document["rollouts_spent"] == 0
    assert document["generation_runs"] == 0
    assert document["non_dev_reads"] == 0
    assert len(document["anchor_arms"]) == 10


def test_the_success_terminal_records_every_arm_and_spends_nothing_it_may_not(
    tmp_path, protocol, monkeypatch
):
    """The whole execute path, driven end to end on synthetic inputs."""

    identity = _stub_execute(
        monkeypatch,
        protocol,
        gate=lambda **_kwargs: {
            "arms": [
                dict(entry, equivalence_status=r2.COMPARISON_PASS, status=r2.ARM_COMPLETED)
                for entry in r2.initial_equivalence_arm_records()
            ],
            "checkpoints_written": 2,
            "fits_attempted": 2,
        },
        fit=lambda _examples, **kwargs: (nn.Linear(1, 1), [2.0, 1.0]),
    )
    assert r2.main(_execute_argv(tmp_path)) == r2.EXIT_CODES[r2.X_RUNG2_OK]
    run_root = tmp_path / "rung2-run-1"
    document = json.loads((run_root / r2.RUN_ARTIFACT).read_text(encoding="utf-8"))
    assert document["exit"] == r2.X_RUNG2_OK
    assert document["reason_class"] is None
    assert document["fits_attempted"] == 12
    assert document["checkpoints_written"] == 12
    assert document["rung2_fits_attempted"] == 10
    assert document["rung2_checkpoints_written"] == 10
    assert document["rollouts_spent"] == document["generation_runs"] == 0
    assert document["non_dev_reads"] == 0
    assert document["rung"] == rung2.RUNG2_NAME
    assert document["design_sha256"] == r2.DESIGN_CANONICAL_SHA256
    assert document["code_identity"] == identity
    assert len(list(run_root.glob("*.pt"))) == 10
    for arm in document["rung2_arms"]:
        assert arm["status"] == r2.ARM_COMPLETED
        assert arm["objective_reduced"] is True
        assert arm["first_epoch_loss"] == 2.0
        assert arm["final_epoch_loss"] == 1.0
        assert arm["loss_history"] == [2.0, 1.0]
        assert arm["n_parameters"] == rung2.RUNG2_DECLARED_PARAMETERS
        assert arm["stem_receptive_field"] == 31
        assert arm["rung"] == rung2.RUNG2_NAME
        assert arm["fit_code_identity"] == identity
        assert re.fullmatch(r"[0-9a-f]{64}", arm["checkpoint_sha256"])
        assert (run_root / arm["checkpoint_relative_name"]).is_file()
    r2.require_complete_rung2_run(document)
    assert r2.optimization_check_passed(document) is True


def test_the_terminal_artifact_carries_no_absolute_path(tmp_path, protocol, monkeypatch):
    """Design section 5.3: no artifact records an absolute filesystem path."""

    _stub_execute(
        monkeypatch,
        protocol,
        gate=lambda **_kwargs: {
            "arms": [
                dict(entry, equivalence_status=r2.COMPARISON_PASS, status=r2.ARM_COMPLETED)
                for entry in r2.initial_equivalence_arm_records()
            ],
            "checkpoints_written": 2,
            "fits_attempted": 2,
        },
        fit=lambda _examples, **kwargs: (nn.Linear(1, 1), [2.0, 1.0]),
    )
    r2.main(_execute_argv(tmp_path))
    text = (tmp_path / "rung2-run-1" / r2.RUN_ARTIFACT).read_text(encoding="utf-8")
    assert str(tmp_path) not in text
    assert not re.search(r"[A-Za-z]:[\\\\/]", text)


def test_a_refusing_arm_stops_the_run_and_keeps_the_arms_downstream_unattempted(
    tmp_path, protocol, monkeypatch
):
    """One refused arm is a named terminal, not a silently shorter list of arms."""

    calls = {"n": 0}

    def _fit(_examples, **_kwargs):
        calls["n"] += 1
        if calls["n"] == 3:
            raise trainer.DevFitDataError("synthetic arm failure")
        return nn.Linear(1, 1), [2.0, 1.0]

    _stub_execute(
        monkeypatch,
        protocol,
        gate=lambda **_kwargs: {
            "arms": [
                dict(entry, equivalence_status=r2.COMPARISON_PASS, status=r2.ARM_COMPLETED)
                for entry in r2.initial_equivalence_arm_records()
            ],
            "checkpoints_written": 2,
            "fits_attempted": 2,
        },
        fit=_fit,
    )
    assert r2.main(_execute_argv(tmp_path)) == r2.EXIT_CODES[r2.X_DATA_MISSING]
    document = json.loads(
        (tmp_path / "rung2-run-1" / r2.RUN_ARTIFACT).read_text(encoding="utf-8")
    )
    statuses = [arm["status"] for arm in document["rung2_arms"]]
    assert statuses[:2] == [r2.ARM_COMPLETED] * 2
    assert statuses[2] == r2.ARM_REFUSED
    assert statuses[3:] == [r2.ARM_UNATTEMPTED] * 7
    assert document["rung2_fits_attempted"] == 3
    assert document["rung2_checkpoints_written"] == 2
    with pytest.raises(DevFitContractError):
        r2.require_complete_rung2_run(document)
    assert r2.optimization_check_passed(document) is False


# ---------------------------------------------------------------------------
# The derived read of design section 5 -- defined here, applied by the analyzer
# ---------------------------------------------------------------------------
@pytest.mark.parametrize(
    "history,expected",
    [
        ([2.0, 1.0], True),
        ([2.0, 3.0, 1.0], True),
        ([1.0, 1.0], False),
        ([1.0, 2.0], False),
        ([1.0], False),
        ([], False),
        ([float("nan"), 1.0], False),
        ([2.0, float("-inf")], False),
        ([True, False], False),
        (["2.0", 1.0], False),
    ],
)
def test_the_objective_reduction_flag_is_strict_and_finite(history, expected):
    """Design section 5.1: every epoch finite, and a strict final-versus-first decrease."""

    assert r2.arm_objective_reduced(history) is expected


def _complete_run_document() -> dict:
    """Return a minimal terminal document that satisfies the completeness criterion."""

    return {
        "equivalence_arms": [
            {
                "equivalence_status": r2.COMPARISON_PASS,
                "seed": seed,
                "status": r2.ARM_COMPLETED,
                "suite": suite,
            }
            for suite, seed in r2.EQUIVALENCE_ARMS
        ],
        "rung2_arms": [
            {
                "objective_reduced": True,
                "seed": seed,
                "status": r2.ARM_COMPLETED,
                "suite": suite,
            }
            for suite, seed in r2.rung2_arms()
        ],
    }


def test_the_completeness_check_accepts_a_complete_run():
    """The accept side, so the refusals below are not a check that refuses everything."""

    r2.require_complete_rung2_run(_complete_run_document())
    assert r2.optimization_check_passed(_complete_run_document()) is True
    assert r2.optimization_check_status(_complete_run_document()) == (
        r2.OPTIMIZATION_CHECK_PASSED
    )


def test_the_completeness_check_refuses_nine_arms():
    """Invariant R10: no partial run may present itself as a rung."""

    document = _complete_run_document()
    document["rung2_arms"] = document["rung2_arms"][1:]
    with pytest.raises(DevFitContractError, match="exactly the 10 rung-2 arm"):
        r2.require_complete_rung2_run(document)
    assert r2.optimization_check_passed(document) is False


def test_the_completeness_check_refuses_a_duplicate_identity():
    """Ten records are not ten identities."""

    document = _complete_run_document()
    document["rung2_arms"][1] = dict(document["rung2_arms"][0])
    with pytest.raises(DevFitContractError, match="exactly the 10 rung-2 arm"):
        r2.require_complete_rung2_run(document)


def test_the_completeness_check_refuses_a_refused_arm():
    """An arm that did not complete is not a completed arm."""

    document = _complete_run_document()
    document["rung2_arms"][0]["status"] = r2.ARM_REFUSED
    with pytest.raises(DevFitContractError, match="not completed"):
        r2.require_complete_rung2_run(document)


def test_the_completeness_check_refuses_a_failed_equivalence_arm():
    """Both gate arms must pass before any rung-2 arm is readable as a rung."""

    document = _complete_run_document()
    document["equivalence_arms"][1]["equivalence_status"] = r2.COMPARISON_FAIL
    with pytest.raises(DevFitContractError, match="complete and to pass"):
        r2.require_complete_rung2_run(document)
    assert r2.optimization_check_passed(document) is False


def test_the_completeness_check_is_not_the_objective_check():
    """A completed arm that did not reduce its objective is a finding, not incompleteness.

    Design section 5.4 gives them different rows and different sentences, so the two
    criteria are deliberately separable, and this pins that they are.
    """

    document = _complete_run_document()
    document["rung2_arms"][4]["objective_reduced"] = False
    r2.require_complete_rung2_run(document)
    assert r2.optimization_check_passed(document) is False
    assert r2.optimization_check_status(document) == r2.OPTIMIZATION_CHECK_FAILED


@pytest.mark.parametrize(
    "differences,expected",
    [
        ([-0.1, -0.2, -0.3, -0.4, -0.5], "REPRODUCED_IN_SIGN"),
        ([0.1, 0.2, 0.0, 0.3, 0.4], "NOT_REPRODUCED_IN_SIGN"),
        ([-0.1, 0.2, -0.3, 0.4, -0.5], "MIXED"),
        ([0.0, 0.0, 0.0, 0.0, 0.0], "NOT_REPRODUCED_IN_SIGN"),
        ([-1.0e-9, 0.1, 0.2, 0.3, 0.4], "NOT_REPRODUCED_IN_SIGN"),
    ],
)
def test_the_paired_sign_label_is_a_description_of_signs(differences, expected):
    """Design section 5.2's three-valued label, including its quantization boundary.

    The last case is the one worth stating: a difference of `-1e-9` is **below the
    declared six-decimal resolution**, so it classifies as a tie rather than as S being
    below C1. That is what "at the analyzer's quantization" means, and reading the raw
    float sign instead would give a different label.
    """

    assert r2.deficit_sign_label(differences) == expected


def test_the_paired_sign_label_refuses_an_empty_set():
    """A label over no seeds is not a description of anything."""

    with pytest.raises(r2.Rung2EscalationError, match="at least one seed"):
        r2.deficit_sign_label([])


def test_the_quantization_is_the_approved_modules_own():
    """One definition of the six-decimal tie rule across Stage 1 and this run."""

    assert r2.quantize is cs.quantize


def test_the_executable_does_not_apply_the_analyzers_criteria():
    """The read belongs to a separate script under a separate review (invariant R7).

    Checked over the call graph rather than by reading: `optimization_check_passed`,
    `optimization_check_status` and `deficit_sign_label` may be **defined** here so the
    analyzer imports one definition, and they may not be **called** here. The two
    functions the executable does call are named, so this does not silently become a
    test that nothing is called at all.
    """

    tree = _module_ast()
    called_from: dict[str, set[str]] = {}
    for node in ast.walk(tree):
        if not isinstance(node, ast.FunctionDef):
            continue
        for inner in ast.walk(node):
            if isinstance(inner, ast.Call) and isinstance(inner.func, ast.Name):
                called_from.setdefault(inner.func.id, set()).add(node.name)
    assert "deficit_sign_label" not in called_from
    assert "optimization_check_status" not in called_from
    assert called_from.get("optimization_check_passed") == {"optimization_check_status"}
    assert called_from.get("arm_objective_reduced") == {"rung2_arm_document"}
    assert called_from.get("require_complete_rung2_run") == {"_execute_mode"}


def test_the_module_emits_no_forbidden_quantity(protocol):
    """Design section 5.3: no p-value, interval, trend, threshold or capacity choice.

    The check is over what the module **emits**, which is what 5.3 constrains, and not
    over its source text -- the module's own docstring names the forbidden quantities in
    order to forbid them, so a source scan would refuse the prohibition itself.
    """

    forbidden = re.compile(
        r"p_value|confidence|significan|minimum_detectable|threshold|slope|trend"
        r"|recommend|select",
        re.IGNORECASE,
    )

    def _keys(value, found: set[str]) -> set[str]:
        if isinstance(value, dict):
            for key, item in value.items():
                found.add(str(key))
                _keys(item, found)
        elif isinstance(value, list):
            for item in value:
                _keys(item, found)
        return found

    documents = [
        r2.plan_document(run_label="rung2-run-1", protocol=protocol),
        r2.refusal_document(
            exit_name=r2.X_RUN_ROOT_OCCUPIED,
            reason_class="RunRootOccupied",
            run_label="rung2-run-1",
            approved_plan_sha256=None,
            attempt_uuid=FIXED_UUID,
            elapsed_s=0.1,
        ),
        r2.run_document(
            exit_name=r2.X_RUNG2_OK,
            reason_class=None,
            run_label="rung2-run-1",
            approved_plan_sha256="a" * 64,
            code_identity_map=r2.rung2_code_identity(),
            protocol=protocol,
            anchors=[],
            arms=r2.initial_rung2_arm_records(),
            equivalence=r2.initial_equivalence_arm_records(),
            equivalence_fits_attempted=0,
            equivalence_checkpoints_written=0,
            rung2_fits_attempted=0,
            rung2_checkpoints_written=0,
            approved_analysis_sha256=None,
            approved_fit_ledger_sha256=None,
            census=None,
            elapsed_s=0.1,
        ),
    ]
    for document in documents:
        offending = sorted(key for key in _keys(document, set()) if forbidden.search(key))
        assert not offending, offending
    # The one place a forbidden word may appear is the authority string, which exists to
    # say what the run is not. It is checked by equality rather than by the scan.
    for document in documents:
        assert document["authority"] == r2.RUNG2_AUTHORITY
    assert "not a capacity selection" in r2.RUNG2_AUTHORITY


def test_this_module_imports_no_capacity_sweep_analyzer():
    """Invariant R7: the approved analysis scripts are bound by digest, never edited."""

    source = Path(r2.__file__).read_text(encoding="utf-8")
    assert "analyze_capacity_sweep" not in source
    assert "import analyze_dev_fit" in source


def test_the_module_error_is_a_subclass_of_the_imported_machinerys_error():
    """One `except` clause covers both sources, so no refusal slips past a handler."""

    assert issubclass(r2.Rung2EscalationError, r2.CapacitySweepError)
    assert r2.CapacitySweepError is cs.CapacitySweepError
