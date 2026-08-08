"""Tests for the Stage-1 capacity-sweep executable (`utils.capacity_sweep`).

Three disciplines shape this file, all of them bought by measured defects earlier in the
project.

**Session 65's.** The exit paths of a program are the region no unit test enters. Every
terminal exit of `main()` below is driven through `main(argv)` and the artifact it wrote
is read back and asserted on -- not asserted from the return code alone, which is the
check that passes while the document is empty, malformed or missing. The one exit that
deliberately writes nothing (`X_FORBIDDEN_BASE`) is tested by asserting that the
protected directory gained nothing.

**Session 47's (requirement (r)).** A pinned literal that also lives in a bound document
is checked by EQUALITY against that document, never adopted from it. The capacity grid's
parameter counts are therefore parsed out of the frozen design's own section 4.2 table
and compared to the module's constants, and the design's canonical digest is compared to
the file rather than to itself.

**No real fit, and no dependence on the git-ignored checkpoints.** Building this module is
not permission to run it, so nothing here fits an arm on the delivered development rows or
reads an approved `.pt` file. The equivalence gate is driven against a synthetic ledger
and synthetic checkpoints in `tmp_path`, which is also what makes these tests pass on a
fresh clone that carries the ledger without the weights.
"""

from __future__ import annotations

import ast
import hashlib
import json
import re
import shutil
import sys
from pathlib import Path

import numpy as np
import pytest
import torch

PACKET_ROOT = Path(__file__).resolve().parents[1]
SCRIPTS_DIR = PACKET_ROOT / "scripts"
sys.path.insert(0, str(SCRIPTS_DIR))

import analyze_dev_fit as approved_analysis  # noqa: E402
from utils import capacity_sweep as cs  # noqa: E402
from utils import dev_fit_trainer as trainer  # noqa: E402
from utils.attribution_net import TemporalAttributionNet  # noqa: E402
from utils.dev_fit_contract import (  # noqa: E402
    MATCHED_FIT_SUITES,
    PREDECLARED_TRAINING_SEEDS,
    DevFitContractError,
)
from utils.protocol_p import canonical_json, canonical_text_sha256  # noqa: E402

DESIGN_PATH = PACKET_ROOT / "protocol" / cs.DESIGN_DOCUMENT_NAME
APPROVED_ANALYSIS_PATH = PACKET_ROOT / cs.APPROVED_ANALYSIS_RELATIVE
APPROVED_LEDGER_PATH = PACKET_ROOT / cs.APPROVED_RESULT_RELATIVE

REGISTRY_WIDTH = 18
SYNTHETIC_WINDOW = 8


# ---------------------------------------------------------------------------
# Shared fixtures: everything synthetic, nothing touching the delivered dataset
# ---------------------------------------------------------------------------
def _module_ast() -> ast.Module:
    """Return the sweep module's parsed AST, for checks a text search gets wrong."""

    return ast.parse(Path(cs.__file__).read_text(encoding="utf-8"))


def _example(class_index: int = 0) -> trainer.TrainingExample:
    """Return one tiny synthetic training example with the real registry width."""

    rng = np.random.default_rng(class_index + 1)
    return trainer.TrainingExample(
        run_id=f"synthetic-{class_index}",
        trajectory_spec_id="synthetic",
        values=rng.normal(size=(SYNTHETIC_WINDOW, REGISTRY_WIDTH)),
        valid=np.ones((SYNTHETIC_WINDOW, REGISTRY_WIDTH), dtype=bool),
        class_index=class_index,
        location_index=0,
        severity=0.25,
        ood_flag=False,
    )


@pytest.fixture()
def examples() -> list[trainer.TrainingExample]:
    """Return a two-class synthetic example set, small enough to optimize instantly."""

    return [_example(0), _example(1)]


@pytest.fixture()
def protocol():
    """Return the real fixed protocol, derived from the approved assignment."""

    return cs.resolve_protocol()


@pytest.fixture()
def plan_file(tmp_path, protocol) -> tuple[Path, str, dict]:
    """Write a valid plan into `tmp_path` and return its path, digest and document."""

    document = cs.plan_document(run_label="stage1-run-1", protocol=protocol)
    path = tmp_path / "plan" / cs.PLAN_ARTIFACT
    cs.write_document(path, document)
    return path, canonical_text_sha256(path), document


def _synthetic_equivalence_world(tmp_path):
    """Return a ledger, checkpoint dir and net factory for driving C9 without real data.

    The two C9 arms are given synthetic 32-channel checkpoints on disk and matching
    ledger rows, so every branch of the gate can be driven on a machine that has never
    run the approved fit.
    """

    checkpoint_dir = tmp_path / "approved"
    checkpoint_dir.mkdir()
    arms = []
    states = {}
    for suite, seed in cs.EQUIVALENCE_ARMS:
        net = cs.build_network(channels=cs.ANCHOR_CHANNELS, seed=seed)
        state = net.state_dict()
        states[(suite, seed)] = state
        name = f"dev_fit_{suite}_seed{seed}.pt"
        torch.save(state, checkpoint_dir / name)
        checkpoint_sha256 = hashlib.sha256((checkpoint_dir / name).read_bytes()).hexdigest()
        arms.append(
            {
                "suite": suite,
                "training_seed": seed,
                "checkpoint_name": name,
                "checkpoint_sha256": checkpoint_sha256,
                "loss_history": [1.0, 0.5],
            }
        )
    return {"arms": arms}, checkpoint_dir, states


# ---------------------------------------------------------------------------
# The grid, checked against the frozen design rather than against itself
# ---------------------------------------------------------------------------
def _design_capacity_table() -> dict[int, tuple[int, int]]:
    """Parse section 4.2's table out of the frozen design document."""

    rows: dict[int, tuple[int, int]] = {}
    for line in DESIGN_PATH.read_text(encoding="utf-8").splitlines():
        cells = [cell.strip().replace("*", "") for cell in line.split("|")[1:-1]]
        if len(cells) != 4:
            continue
        try:
            channels = int(cells[0].replace(",", ""))
            parameters = int(cells[1].replace(",", ""))
            receptive_field = int(cells[3].replace(",", ""))
        except ValueError:
            continue
        rows[channels] = (parameters, receptive_field)
    return rows


def test_the_design_document_is_the_frozen_approved_version():
    """The executable is built against v0.1's exact bytes, checked against the file."""

    assert canonical_text_sha256(DESIGN_PATH) == cs.DESIGN_CANONICAL_SHA256
    assert cs.design_digest() == cs.DESIGN_CANONICAL_SHA256


def test_editing_the_frozen_design_turns_plan_mode_red(monkeypatch, protocol):
    """An approved version is bumped and moved, never edited in place."""

    monkeypatch.setattr(cs, "DESIGN_CANONICAL_SHA256", "f" * 64)
    with pytest.raises(DevFitContractError, match="not the frozen approved v0.1"):
        cs.plan_document(run_label="stage1-run-1", protocol=protocol)


def test_the_capacity_grid_equals_the_designs_own_table():
    """Requirement (r): equality against the bound document, never adoption from it."""

    table = _design_capacity_table()
    assert set(cs.EXPECTED_PARAMETERS) <= set(table)
    for channels, parameters in cs.EXPECTED_PARAMETERS.items():
        assert table[channels][0] == parameters, channels
        assert table[channels][1] == cs.EXPECTED_RECEPTIVE_FIELD, channels


def test_the_constructed_networks_reproduce_the_designs_table():
    """Invariant C4: shape is read off the constructed network, not re-derived."""

    shape = cs.capacity_shape_map()
    assert sorted(shape) == sorted(cs.CAPACITY_POINTS)
    for channels, entry in shape.items():
        assert entry["n_parameters"] == cs.EXPECTED_PARAMETERS[channels]
        assert entry["receptive_field"] == cs.EXPECTED_RECEPTIVE_FIELD
    counts = [entry["n_parameters"] for entry in shape.values()]
    assert len(set(counts)) == len(counts)


def test_c4_refuses_a_capacity_point_whose_count_moved(monkeypatch):
    """A width whose parameter count stops matching the design is a refusal, not a note."""

    monkeypatch.setitem(cs.EXPECTED_PARAMETERS, 40, 61_011)
    with pytest.raises(DevFitContractError, match="the design's table reserves"):
        cs.capacity_shape_map()


def test_c4_refuses_two_capacity_points_sharing_a_parameter_count():
    """Driven directly, because asserting the real grid's property tests the world.

    Session-92 mutation sweep: while this check lived inline inside `capacity_shape_map`,
    deleting it changed nothing any test could see.
    """

    cs.require_distinct_capacity_counts(
        {16: {"n_parameters": 10_586}, 24: {"n_parameters": 22_786}}
    )
    with pytest.raises(DevFitContractError, match="same parameter count"):
        cs.require_distinct_capacity_counts(
            {16: {"n_parameters": 10_586}, 24: {"n_parameters": 10_586}}
        )


def test_c4_refuses_a_moved_receptive_field(monkeypatch):
    """Width must leave the 1,023-sample receptive field alone at every point."""

    monkeypatch.setattr(cs, "EXPECTED_RECEPTIVE_FIELD", 1_022)
    with pytest.raises(DevFitContractError, match="receptive field"):
        cs.capacity_shape_map()


def test_the_arm_lists_are_forty_new_and_ten_read_only():
    """Stage 1 is fifty arms, of which the ten at 32 channels already exist."""

    new = cs.curve_arms()
    anchors = cs.anchor_arms()
    assert len(new) == 40
    assert len(anchors) == 10
    assert all(channels != cs.ANCHOR_CHANNELS for channels, _, _ in new)
    assert all(channels == cs.ANCHOR_CHANNELS for channels, _, _ in anchors)
    assert len(set(new) | set(anchors)) == 50
    assert {suite for _, suite, _ in new} == set(MATCHED_FIT_SUITES)
    assert {seed for _, _, seed in new} == set(PREDECLARED_TRAINING_SEEDS)


def test_the_maximum_budget_is_forty_two_fits():
    """Forty curve arms plus the two C9 equivalence fits, and nothing else."""

    assert cs.MAX_FITS == len(cs.curve_arms()) + len(cs.EQUIVALENCE_ARMS) == 42
    assert cs.MAX_CHECKPOINTS == 42


# ---------------------------------------------------------------------------
# Invariant C5 and the one construction site
# ---------------------------------------------------------------------------
def test_the_rung1_band_guard_cannot_be_turned_off_from_the_command_line():
    """Climbing the ladder is a recorded decision, not a constructor argument.

    Asserted over the module's parsed AST rather than its text, because a text search
    counts the prose that *describes* the guard alongside the expression that carries it.
    """

    tree = _module_ast()
    passed = [
        keyword
        for node in ast.walk(tree)
        if isinstance(node, ast.Call)
        for keyword in node.keywords
        if keyword.arg == "enforce_rung1_band"
    ]
    assert len(passed) == 1
    assert isinstance(passed[0].value, ast.Constant) and passed[0].value.value is True

    flags = {
        node.args[0].value
        for node in ast.walk(tree)
        if isinstance(node, ast.Call)
        and isinstance(node.func, ast.Attribute)
        and node.func.attr == "add_argument"
        and node.args
        and isinstance(node.args[0], ast.Constant)
    }
    assert flags == {
        "--mode",
        "--run-label",
        "--output-dir",
        "--base-dir",
        "--data-root",
        "--approved-plan",
        "--approved-plan-sha256",
    }


@pytest.mark.parametrize("channels", [8, 64, 96, 128, 33, 0, -16, True, 32.0])
def test_build_network_refuses_a_width_outside_the_predeclared_grid(channels):
    """Only the five Stage-1 points exist; Stage 2 is a different document."""

    with pytest.raises(DevFitContractError, match="channels must be one of"):
        cs.build_network(channels=channels, seed=0)


@pytest.mark.parametrize("seed", [5, -1, 10])
def test_build_network_refuses_an_undeclared_seed(seed):
    """Bound 3: the five predeclared training seeds and no others."""

    with pytest.raises(DevFitContractError):
        cs.build_network(channels=16, seed=seed)


@pytest.mark.parametrize("seed", [0, 4])
def test_c9s_precondition_the_width_path_reproduces_the_approved_constructor(seed):
    """At 32 channels this module's one construction site IS the approved network.

    If this were false the equivalence gate would be comparing two different things and
    a `PASS` would mean nothing, so it is measured here rather than assumed.
    """

    approved = TemporalAttributionNet(seed=seed)
    produced = cs.build_network(channels=cs.ANCHOR_CHANNELS, seed=seed)
    identical, reason = cs.state_dicts_are_bit_identical(
        produced.state_dict(), approved.state_dict()
    )
    assert identical, reason
    assert produced.n_parameters == approved.n_parameters == 39_594


# ---------------------------------------------------------------------------
# Route A: the loss and the batcher keep exactly one definition
# ---------------------------------------------------------------------------
def test_the_scientific_loss_and_the_batcher_are_imported_not_reimplemented():
    """Route A's whole justification: the duplicated loop is plumbing, not science."""

    assert cs.arm_loss is trainer.arm_loss
    assert cs._stack is trainer._stack
    source = Path(cs.__file__).read_text(encoding="utf-8")
    assert "def arm_loss" not in source
    assert "def _stack" not in source
    assert "cross_entropy" not in source


def test_the_classification_metrics_come_from_the_approved_analyzer():
    """Design section 3: a second definition of macro-F1 would be a second definition."""

    assert cs.approved_analysis.classification_metrics is (
        approved_analysis.classification_metrics
    )
    source = Path(cs.__file__).read_text(encoding="utf-8")
    assert "def classification_metrics" not in source
    assert "macro_f1 =" not in source


def test_the_code_identity_is_the_eight_historical_entries_plus_this_module():
    """Invariant C3 under Route A: eight exact matches and exactly one addition."""

    identity = cs.sweep_code_identity()
    historical = trainer.training_code_identity()
    assert set(identity) == set(historical) | {"capacity_sweep.py"}
    for label, digest in historical.items():
        assert identity[label] == digest, label
    for label, digest in identity.items():
        assert re.fullmatch(r"[0-9a-f]{64}", digest), label


def test_dev_fit_trainer_stays_inside_the_sweeps_code_identity():
    """The approved trainer really is part of what fits these arms -- it is imported."""

    assert "dev_fit_trainer.py" in cs.sweep_code_identity()


# ---------------------------------------------------------------------------
# Invariant C3 against the real approved ledger
# ---------------------------------------------------------------------------
def _ledger() -> dict:
    """Return an independent copy of the tracked approved ledger."""

    return json.loads(APPROVED_LEDGER_PATH.read_text(encoding="utf-8"))


def test_c3_accepts_the_real_approved_ledger(protocol):
    """The anchor really was produced by the code, data and protocol in use now."""

    cs.require_anchor_comparability(_ledger(), protocol)


def test_c3_refuses_a_changed_historical_code_entry(protocol):
    """One moved historical digest means five unrelated experiments, not a sweep."""

    ledger = _ledger()
    ledger["code_identity"]["attribution_net.py"] = "a" * 64
    with pytest.raises(DevFitContractError, match="differs from the code that fitted"):
        cs.require_anchor_comparability(ledger, protocol)


def test_c3_refuses_an_unlisted_extra_identity_entry(protocol):
    """Exactly one addition is permitted, and it is this module."""

    ledger = _ledger()
    del ledger["code_identity"]["estimator.py"]
    with pytest.raises(DevFitContractError, match="exactly one addition"):
        cs.require_anchor_comparability(ledger, protocol)


def test_c3_refuses_a_dropped_identity_entry(protocol):
    """A historical entry the current code no longer names is a refusal."""

    ledger = _ledger()
    ledger["code_identity"]["retired_module.py"] = "b" * 64
    with pytest.raises(DevFitContractError, match="adds|drops"):
        cs.require_anchor_comparability(ledger, protocol)


@pytest.mark.parametrize("field", ["epochs", "batch_size", "learning_rate", "device"])
def test_c3_refuses_a_protocol_the_anchor_did_not_use(protocol, field):
    """A sweep run under a different optimization protocol is not this sweep."""

    ledger = _ledger()
    ledger["training_protocol"][field] = "moved" if field == "device" else 999
    with pytest.raises(DevFitContractError, match="training protocol differs"):
        cs.require_anchor_comparability(ledger, protocol)


def test_c3_refuses_wrong_role_indexes(protocol):
    """The anchor's role indexes must be the authorized delivered ones."""

    ledger = _ledger()
    ledger["role_index_sha256"]["labels/index.csv"] = "c" * 64
    with pytest.raises(DevFitContractError, match="role indexes"):
        cs.require_anchor_comparability(ledger, protocol)


def test_c3_refuses_an_anchor_arm_with_a_foreign_data_identity(protocol):
    """Every anchor arm carries the authorized manifest, config and assignment."""

    ledger = _ledger()
    ledger["arms"][0]["manifest_sha256"] = "d" * 64
    with pytest.raises(DevFitContractError, match="authorized data identity"):
        cs.require_anchor_comparability(ledger, protocol)


# ---------------------------------------------------------------------------
# Invariant C1: the anchors are read, never re-fitted
# ---------------------------------------------------------------------------
def test_the_ten_anchors_are_read_from_the_two_approved_documents():
    """Invariant C1: the approved ledger is the sole provenance of those checkpoints."""

    ledger = _ledger()
    analysis = json.loads(APPROVED_ANALYSIS_PATH.read_text(encoding="utf-8"))
    entries = cs.approved_anchor_arms(ledger, analysis)
    assert len(entries) == 10
    assert {entry["status"] for entry in entries} == {cs.ARM_REUSED}
    assert {entry["channels"] for entry in entries} == {cs.ANCHOR_CHANNELS}
    by_key = {(entry["suite"], entry["seed"]): entry for entry in entries}
    for arm in analysis["arms"]:
        recorded = by_key[(arm["suite"], arm["seed"])]
        assert recorded["macro_f1"] == arm["classification"]["macro_f1"]
        assert recorded["accuracy"] == arm["classification"]["accuracy"]
        assert recorded["checkpoint_sha256"] == arm["checkpoint_sha256"]
        assert recorded["fit_code_identity"] == dict(sorted(ledger["code_identity"].items()))


def test_the_anchor_read_refuses_two_documents_that_disagree_on_a_digest():
    """A check whose two sides come from one source is a report of a check."""

    ledger = _ledger()
    analysis = json.loads(APPROVED_ANALYSIS_PATH.read_text(encoding="utf-8"))
    analysis["arms"][3]["checkpoint_sha256"] = "e" * 64
    with pytest.raises(cs.CapacitySweepError, match="disagree on the"):
        cs.approved_anchor_arms(ledger, analysis)


def test_the_anchor_read_refuses_a_missing_arm():
    """Ten anchors or none: a partial anchor set cannot carry the paired curve."""

    ledger = _ledger()
    analysis = json.loads(APPROVED_ANALYSIS_PATH.read_text(encoding="utf-8"))
    analysis["arms"] = analysis["arms"][:9]
    with pytest.raises(cs.CapacitySweepError, match="exactly the ten approved"):
        cs.approved_anchor_arms(ledger, analysis)


def test_the_anchor_read_refuses_a_duplicate_in_place_of_one_identity():
    """A ten-row census still fails when one anchor silently replaces another."""

    ledger = _ledger()
    analysis = json.loads(APPROVED_ANALYSIS_PATH.read_text(encoding="utf-8"))
    analysis["arms"][-1] = dict(analysis["arms"][-2])
    with pytest.raises(cs.CapacitySweepError, match="duplicate"):
        cs.approved_anchor_arms(ledger, analysis)


# ---------------------------------------------------------------------------
# BAR and the anchor SD: sourced constants, named to their exact field
# ---------------------------------------------------------------------------
def test_the_bar_and_anchor_sd_are_read_from_their_named_fields():
    """Design sections 5.1 and 5.2: a sourced constant whose source is unnamed is a literal."""

    analysis = json.loads(APPROVED_ANALYSIS_PATH.read_text(encoding="utf-8"))
    assert cs.BAR_FIELD_PATH == ("paired_macro_f1", "claim_sheet_success_bar")
    assert cs.ANCHOR_SAMPLE_SD_FIELD_PATH == ("paired_macro_f1", "sample_sd_S_minus_C1")
    assert cs.read_success_bar(analysis) == analysis["paired_macro_f1"]["claim_sheet_success_bar"]
    assert cs.read_anchor_sample_sd(analysis) == (
        analysis["paired_macro_f1"]["sample_sd_S_minus_C1"]
    )


def test_the_executable_carries_no_literal_copy_of_either_sourced_constant():
    """The parenthetical values in the design are a reader's convenience, not literals.

    Checked over the module's numeric constants rather than its text: prose that names
    the 0.05 project bar is a description, while a `0.05` the code could *use* is the
    defect -- an invented criterion constant that would survive the approved artifact
    changing underneath it.
    """

    literals = {
        node.value
        for node in ast.walk(_module_ast())
        if isinstance(node, ast.Constant) and isinstance(node.value, float)
    }
    assert 0.05 not in literals
    assert 0.149635726834 not in literals


@pytest.mark.parametrize("value", [None, "0.05", 0, 1, -0.1, float("nan"), float("inf")])
def test_the_bar_is_refused_when_it_is_not_a_finite_float_in_the_unit_interval(value):
    """The executable refuses rather than inventing a criterion constant."""

    with pytest.raises(cs.CapacitySweepError):
        cs.read_success_bar({"paired_macro_f1": {"claim_sheet_success_bar": value}})


@pytest.mark.parametrize("value", [None, "0.15", 0.0, -1.0, float("nan")])
def test_the_anchor_sd_is_refused_when_it_is_not_a_finite_positive_float(value):
    """`paired_range_exceeds_anchor_sd` may not be computed against a bad denominator."""

    with pytest.raises(cs.CapacitySweepError):
        cs.read_anchor_sample_sd({"paired_macro_f1": {"sample_sd_S_minus_C1": value}})


def test_an_absent_field_is_refused_by_its_own_name():
    """A missing field is named in the refusal, so a reader knows which one moved."""

    with pytest.raises(cs.CapacitySweepError, match="paired_macro_f1.claim_sheet_success_bar"):
        cs.read_success_bar({"paired_macro_f1": {}})


# ---------------------------------------------------------------------------
# The run label and the two reserved sink names
# ---------------------------------------------------------------------------
@pytest.mark.parametrize(
    "label", ["abc", "stage1-run-1", "a" * 32, "0" * 32, "s1-2", "9-a-b"]
)
def test_conforming_run_labels_are_accepted(label):
    """The accept side is tested at both length boundaries, not only in the middle."""

    assert cs.require_run_label(label) == label


@pytest.mark.parametrize(
    "label",
    [
        "ab",
        "a" * 33,
        "-abc",
        "Abc",
        "abc_def",
        "a b",
        "abc/def",
        "abc.def",
        "",
        None,
        3,
        "_unbound",
        "_capacity_sweep_refusals",
        "..",
        ".",
    ],
)
def test_nonconforming_run_labels_are_refused(label):
    """The label becomes a path component and a JSON member name before anything else."""

    with pytest.raises(DevFitContractError, match="run_label must match"):
        cs.require_run_label(label)


def test_the_two_reserved_sink_names_are_unreachable_by_construction():
    """Safe by construction, not by convention: the label class admits no underscore."""

    for reserved in (cs.REFUSAL_SINK_NAME, cs.UNBOUND_LABEL_DIRECTORY):
        assert reserved.startswith("_")
        assert cs.RUN_LABEL_PATTERN.fullmatch(reserved) is None
    assert "_" not in cs.RUN_LABEL_PATTERN.pattern.split("[")[1].split("]")[0]


# ---------------------------------------------------------------------------
# Plan mode
# ---------------------------------------------------------------------------
def test_plan_mode_writes_a_terminal_artifact_and_runs_zero_fits(tmp_path):
    """Driven through `main(argv)`, and the document it wrote is read back."""

    code = cs.main(
        ["--mode", "plan", "--run-label", "stage1-run-1", "--output-dir", str(tmp_path)]
    )
    assert code == cs.EXIT_CODES[cs.X_PLAN_OK] == 0
    document = json.loads((tmp_path / cs.PLAN_ARTIFACT).read_text(encoding="utf-8"))
    assert document["exit"] == cs.X_PLAN_OK
    assert document["plan_valid"] is True
    assert document["n_new_arms"] == 40
    assert document["n_anchor_arms"] == 10
    assert document["n_equivalence_arms"] == 2
    assert document["maximum_budget"] == {
        "checkpoints": 42,
        "fits": 42,
        "generation_runs": 0,
        "non_dev_reads": 0,
        "rollouts": 0,
    }
    assert not list(tmp_path.glob("*.pt"))


def test_the_plan_is_byte_deterministic_across_destinations(tmp_path, protocol):
    """Two runs at the same label into different host directories are identical bytes."""

    first = tmp_path / "one"
    second = tmp_path / "two"
    cs.main(["--mode", "plan", "--run-label", "stage1-run-1", "--output-dir", str(first)])
    cs.main(["--mode", "plan", "--run-label", "stage1-run-1", "--output-dir", str(second)])
    assert (first / cs.PLAN_ARTIFACT).read_bytes() == (second / cs.PLAN_ARTIFACT).read_bytes()


def test_a_different_run_label_is_a_different_plan_document(protocol):
    """`run_label` is what makes conforming retries distinguishable documents."""

    one = canonical_json(cs.plan_document(run_label="stage1-run-1", protocol=protocol))
    two = canonical_json(cs.plan_document(run_label="stage1-run-2", protocol=protocol))
    assert one != two


def test_the_plan_serializes_no_host_path(tmp_path, protocol):
    """Machine-specific destinations are excluded; that is what buys determinism."""

    text = canonical_json(cs.plan_document(run_label="stage1-run-1", protocol=protocol))
    assert str(PACKET_ROOT) not in text
    assert "\\\\" not in text
    assert re.search(r"[A-Za-z]:/", text) is None
    for entry in json.loads(text)["new_arms"]:
        assert entry["checkpoint_relative_name"].startswith(cs.LOGICAL_NAMESPACE_ROOT + "/")


def test_the_plan_contains_no_thirty_two_channel_fit_arm(protocol):
    """Design section 7.3: that is invalid at plan time, not at run time."""

    document = cs.plan_document(run_label="stage1-run-1", protocol=protocol)
    assert all(entry["channels"] != 32 for entry in document["new_arms"])
    assert all(entry["read_only"] is True for entry in document["anchor_arms"])
    assert all(entry["read_only"] is False for entry in document["new_arms"])


def test_the_equivalence_namespace_is_a_reserved_subtree_of_the_run_root(protocol):
    """The C9 outputs live inside the run whose gate they are."""

    document = cs.plan_document(run_label="stage1-run-1", protocol=protocol)
    namespace = document["logical_output_namespace"]
    assert namespace == f"{cs.LOGICAL_NAMESPACE_ROOT}/stage1-run-1"
    assert document["equivalence_relative_namespace"] == f"{namespace}/_equivalence"
    for entry in document["equivalence_arms"]:
        assert entry["checkpoint_relative_name"].startswith(f"{namespace}/_equivalence/")
        assert entry["channels"] == cs.ANCHOR_CHANNELS


def test_the_plan_binds_both_approved_documents_and_terminal_names(protocol):
    """Section 7.1 names the ledger, analysis, and exact result-file identities."""

    document = cs.plan_document(run_label="stage1-run-1", protocol=protocol)
    namespace = document["logical_output_namespace"]
    assert document["approved_fit_ledger_sha256"] == canonical_text_sha256(
        PACKET_ROOT / cs.APPROVED_RESULT_RELATIVE
    )
    assert document["approved_analysis_sha256"] == canonical_text_sha256(
        PACKET_ROOT / cs.APPROVED_ANALYSIS_RELATIVE
    )
    assert document["run_artifact_relative_name"] == f"{namespace}/{cs.RUN_ARTIFACT}"
    assert document["equivalence_artifact_relative_name"] == (
        f"{namespace}/{cs.EQUIVALENCE_SUBTREE}/{cs.EQUIVALENCE_ARTIFACT}"
    )


def test_plan_mode_refuses_a_bad_label_and_still_writes_a_terminal_artifact(tmp_path):
    """Every terminal exit persists a document; a refusal records its class, not its text."""

    code = cs.main(
        ["--mode", "plan", "--run-label", "Bad_Label", "--output-dir", str(tmp_path)]
    )
    assert code == cs.EXIT_CODES[cs.X_CONTRACT_REFUSED] == 3
    document = json.loads((tmp_path / cs.PLAN_ARTIFACT).read_text(encoding="utf-8"))
    assert document["exit"] == cs.X_CONTRACT_REFUSED
    assert document["plan_valid"] is False
    assert document["reason_class"] == "DevFitContractError"
    assert "Bad_Label" not in json.dumps(document)


def test_plan_mode_refuses_a_missing_label(tmp_path):
    """The label is required, not defaulted."""

    assert cs.main(["--mode", "plan", "--output-dir", str(tmp_path)]) == 3


def test_plan_mode_refuses_a_missing_output_directory():
    """A destination is required; it is simply not serialized."""

    assert cs.main(["--mode", "plan", "--run-label", "stage1-run-1"]) == 3


# ---------------------------------------------------------------------------
# The authorization gate
# ---------------------------------------------------------------------------
def test_the_gate_accepts_the_plan_it_was_given(plan_file, protocol):
    """The happy path is driven so the refusals below mean something."""

    path, digest, document = plan_file
    assert cs.require_authorized_plan(path, expected_sha256=digest, protocol=protocol) == document


def test_the_gate_refuses_a_digest_that_names_another_document(plan_file, protocol):
    """`--approved-plan-sha256` names a document, and this is where that is enforced."""

    path, _, _ = plan_file
    with pytest.raises(DevFitContractError, match="not the authorized digest"):
        cs.require_authorized_plan(path, expected_sha256="a" * 64, protocol=protocol)


@pytest.mark.parametrize("digest", ["", "abc", "A" * 64, "g" * 64, "0" * 63, None])
def test_the_gate_refuses_a_malformed_digest(plan_file, protocol, digest):
    """A digest that is not 64 lowercase hex characters never reaches the file."""

    path, _, _ = plan_file
    with pytest.raises(DevFitContractError, match="64 lowercase hex"):
        cs.require_authorized_plan(path, expected_sha256=digest, protocol=protocol)


@pytest.mark.parametrize(
    ("key", "value", "message"),
    [
        ("plan_valid", False, "not valid"),
        ("mode", "execute", "not a plan"),
        ("exit", "X_CONTRACT_REFUSED", "not a terminal plan"),
        ("design_sha256", "f" * 64, "different design document"),
        ("run_label", "stage1-run-9", "not the plan this executable builds"),
        ("n_new_arms", 39, "not the plan this executable builds"),
    ],
)
def test_the_gate_refuses_a_mutated_plan(tmp_path, protocol, key, value, message):
    """Every field the gate reads is driven by mutating it and re-authenticating."""

    document = cs.plan_document(run_label="stage1-run-1", protocol=protocol)
    document[key] = value
    path = tmp_path / cs.PLAN_ARTIFACT
    cs.write_document(path, document)
    with pytest.raises(DevFitContractError, match=message):
        cs.require_authorized_plan(
            path, expected_sha256=canonical_text_sha256(path), protocol=protocol
        )


def test_the_gate_refuses_a_plan_written_by_another_code_state(tmp_path, protocol):
    """A plan is a statement about the run AND about the code that will make it."""

    document = cs.plan_document(run_label="stage1-run-1", protocol=protocol)
    document["code_identity"] = dict(document["code_identity"])
    document["code_identity"]["capacity_sweep.py"] = "a" * 64
    path = tmp_path / cs.PLAN_ARTIFACT
    cs.write_document(path, document)
    with pytest.raises(DevFitContractError, match="different code state"):
        cs.require_authorized_plan(
            path, expected_sha256=canonical_text_sha256(path), protocol=protocol
        )


def test_the_gate_refuses_an_absent_document(tmp_path, protocol):
    """A named digest over a file that is not there is a refusal, not a crash."""

    with pytest.raises(DevFitContractError, match="not present"):
        cs.require_authorized_plan(
            tmp_path / "absent.json", expected_sha256="a" * 64, protocol=protocol
        )


# ---------------------------------------------------------------------------
# Execute mode: the three write locations and the exits that reach them
# ---------------------------------------------------------------------------
def test_a_base_inside_the_approved_checkpoint_tree_writes_absolutely_nothing(capsys):
    """Invariant C1's one artifact-free exit, and the reason it has to be artifact-free.

    Every sink this module has is under the base, so persisting this refusal would be the
    write into `results/dev_fit` the invariant forbids. The exit is therefore proved by
    the protected directory being unchanged, not by a document.
    """

    protected = PACKET_ROOT / cs.APPROVED_CHECKPOINT_RELATIVE
    before = sorted(path.name for path in protected.iterdir())
    try:
        code = cs.main(["--mode", "execute", "--base-dir", str(protected / "sweep")])
        assert code == cs.EXIT_CODES[cs.X_FORBIDDEN_BASE] == 10
        assert sorted(path.name for path in protected.iterdir()) == before
        assert not (protected / cs.REFUSAL_SINK_NAME).exists()
        assert cs.X_FORBIDDEN_BASE in capsys.readouterr().out
    finally:
        # This is the one test whose subject is a tracked results directory, so it
        # cleans up whatever a *failing* guard would have let through. Measured in the
        # Session-92 mutation sweep: with the guard weakened to an equality test, the
        # run wrote a refusal document under `results/dev_fit/sweep/` before this test
        # went red, and the debris outlived the sweep that produced it.
        shutil.rmtree(protected / "sweep", ignore_errors=True)


def test_the_protected_base_check_also_catches_the_directory_itself():
    """`results/dev_fit` itself, not only a child of it."""

    with pytest.raises(cs.ForbiddenBase):
        cs.require_permitted_base(PACKET_ROOT / cs.APPROVED_CHECKPOINT_RELATIVE)


def test_a_sibling_of_the_protected_directory_is_permitted(tmp_path):
    """The guard is about the protected tree, not about `results/` in general."""

    assert cs.require_permitted_base(PACKET_ROOT / "results" / "capacity_sweep")
    assert cs.require_permitted_base(tmp_path)


def test_a_pre_claim_refusal_persists_in_the_unbound_sink(tmp_path):
    """No trustworthy label or digest exists yet, so both are recorded as null."""

    code = cs.main(["--mode", "execute", "--base-dir", str(tmp_path)])
    assert code == cs.EXIT_CODES[cs.X_PLAN_UNAUTHORIZED] == 8
    sink = tmp_path / cs.REFUSAL_SINK_NAME / cs.UNBOUND_LABEL_DIRECTORY
    written = list(sink.glob("*.json"))
    assert len(written) == 1
    document = json.loads(written[0].read_text(encoding="utf-8"))
    assert document["exit"] == cs.X_PLAN_UNAUTHORIZED
    assert document["run_label"] is None
    assert document["approved_plan_sha256"] is None
    assert document["fits_attempted"] == document["checkpoints_written"] == 0
    assert document["rollouts_spent"] == document["generation_runs"] == 0
    assert document["non_dev_reads"] == 0
    assert written[0].stem == document["attempt_uuid"]
    assert str(tmp_path) not in json.dumps(document)
    assert not list(tmp_path.glob("*/*.pt"))


def test_a_refusal_document_records_no_message_and_no_path(tmp_path):
    """The trainer's established rule: `reason_class` and the exit name only."""

    document = cs.refusal_document(
        exit_name=cs.X_RUN_ROOT_OCCUPIED,
        reason_class="RunRootOccupied",
        run_label="stage1-run-1",
        approved_plan_sha256="a" * 64,
        attempt_uuid="00000000-0000-4000-8000-000000000000",
        elapsed_s=0.5,
    )
    text = json.dumps(document)
    assert "message" not in text and "Traceback" not in text
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
    """Design section 6 C2: any pre-existing path, not merely a non-empty directory.

    The empty-directory case is the one "exists and non-empty" admitted, and the file
    case is the one nobody had considered at all.
    """

    path, digest, document = plan_file
    root = tmp_path / document["run_label"]
    if occupant == "file":
        root.write_text("prior evidence", encoding="utf-8")
        before = root.read_text(encoding="utf-8")
    else:
        root.mkdir()
        if occupant == "populated-directory":
            (root / "prior.json").write_text("{}", encoding="utf-8")
        before = sorted(entry.name for entry in root.iterdir())

    code = cs.main(
        [
            "--mode",
            "execute",
            "--base-dir",
            str(tmp_path),
            "--approved-plan",
            str(path),
            "--approved-plan-sha256",
            digest,
            "--data-root",
            str(tmp_path / "absent-data-root"),
        ]
    )
    assert code == cs.EXIT_CODES[cs.X_RUN_ROOT_OCCUPIED] == 7
    if occupant == "file":
        assert root.read_text(encoding="utf-8") == before
    else:
        assert sorted(entry.name for entry in root.iterdir()) == before

    sink = tmp_path / cs.REFUSAL_SINK_NAME / document["run_label"]
    written = list(sink.glob("*.json"))
    assert len(written) == 1
    refusal = json.loads(written[0].read_text(encoding="utf-8"))
    assert written[0].stem == refusal["attempt_uuid"]
    assert refusal["exit"] == cs.X_RUN_ROOT_OCCUPIED
    assert refusal["run_label"] == document["run_label"]
    assert refusal["approved_plan_sha256"] == digest
    assert refusal["fits_attempted"] == 0


def test_two_refusals_at_one_label_do_not_overwrite_each_other(tmp_path, plan_file):
    """The UUID name is what keeps a second attempt from erasing the first's record."""

    path, digest, document = plan_file
    (tmp_path / document["run_label"]).mkdir()
    argv = [
        "--mode",
        "execute",
        "--base-dir",
        str(tmp_path),
        "--approved-plan",
        str(path),
        "--approved-plan-sha256",
        digest,
        "--data-root",
        str(tmp_path / "absent-data-root"),
    ]
    cs.main(argv)
    cs.main(argv)
    sink = tmp_path / cs.REFUSAL_SINK_NAME / document["run_label"]
    written = list(sink.glob("*.json"))
    assert len(written) == 2
    assert len({entry.name for entry in written}) == 2
    uuids = {json.loads(entry.read_text(encoding="utf-8"))["attempt_uuid"] for entry in written}
    assert len(uuids) == 2


def test_the_refusal_sink_never_overwrites_on_a_uuid_collision(tmp_path, monkeypatch):
    """The exclusive create, driven at the only input that can tell it from a plain write.

    Session-92 mutation sweep: with distinct UUIDs, `open("x")` and `open("w")` behave
    identically, so the earlier test could not see the mode change. Forcing every draw to
    collide is what separates them -- and the correct behaviour is to refuse rather than
    to erase a prior attempt's record.
    """

    monkeypatch.setattr(cs.uuid, "uuid4", lambda: "fixed-collision-name")
    first = cs.write_refusal_document(tmp_path, "stage1-run-1", {"exit": "FIRST"})
    assert json.loads(first.read_text(encoding="utf-8"))["exit"] == "FIRST"
    with pytest.raises(cs.CapacitySweepError, match="unique refusal artifact name"):
        cs.write_refusal_document(tmp_path, "stage1-run-1", {"exit": "SECOND"})
    assert json.loads(first.read_text(encoding="utf-8"))["exit"] == "FIRST"


def test_the_run_root_is_claimed_by_one_atomic_create(tmp_path):
    """A check followed by a separate create admits two invocations that both pass."""

    root = cs.claim_run_root(tmp_path, "stage1-run-1")
    assert root == tmp_path / "stage1-run-1" and root.is_dir()
    with pytest.raises(cs.RunRootOccupied):
        cs.claim_run_root(tmp_path, "stage1-run-1")


def test_the_claim_creates_missing_parents_but_not_the_final_component(tmp_path):
    """`<base>` may be new; `<base>/<run_label>` may not already exist."""

    root = cs.claim_run_root(tmp_path / "a" / "b", "stage1-run-1")
    assert root.is_dir()


def test_the_refusal_sink_is_a_sibling_of_the_run_root(tmp_path):
    """Lesson 116: a refusal never reports through the resource that triggered it."""

    written = cs.write_refusal_document(tmp_path, "stage1-run-1", {"exit": "X"})
    assert written.parent == tmp_path / cs.REFUSAL_SINK_NAME / "stage1-run-1"
    assert not (tmp_path / "stage1-run-1").exists()


def test_the_sink_refuses_to_name_a_directory_from_an_unvalidated_label(tmp_path):
    """The label is validated before it may enter a filesystem path."""

    with pytest.raises(DevFitContractError, match="run_label must match"):
        cs.write_refusal_document(tmp_path, "../escape", {"exit": "X"})


def test_execute_terminal_preserves_partial_c9_and_all_unattempted_curve_arms(
    tmp_path, protocol, monkeypatch
):
    """The C9 exception-to-terminal seam keeps identities and split resource counts."""

    identity = cs.sweep_code_identity()
    monkeypatch.setattr(cs, "resolve_protocol", lambda: protocol)
    monkeypatch.setattr(
        cs,
        "require_authorized_plan",
        lambda *_args, **_kwargs: {
            "code_identity": identity,
            "run_label": "stage1-run-1",
        },
    )
    monkeypatch.setattr(cs, "capacity_shape_map", lambda: {})
    monkeypatch.setattr(cs, "read_json_document", lambda *_args, **_kwargs: {})
    monkeypatch.setattr(cs, "require_anchor_comparability", lambda *_args: None)

    anchors = [
        {
            "channels": channels,
            "fit_code_identity": {"anchor": "a" * 64},
            "seed": seed,
            "status": cs.ARM_REUSED,
            "suite": suite,
        }
        for channels, suite, seed in cs.anchor_arms()
    ]
    monkeypatch.setattr(cs, "approved_anchor_arms", lambda *_args: anchors)
    monkeypatch.setattr(cs, "load_dev_examples", lambda *_args: ({}, {"role": "dev"}))

    c9 = cs.initial_equivalence_arm_records()
    c9[0].update(
        {
            "comparison": cs.COMPARISON_PASS,
            "fit_code_identity": identity,
            "status": cs.ARM_COMPLETED,
        }
    )
    c9[1].update(
        {
            "comparison": cs.COMPARISON_FAIL,
            "fit_code_identity": identity,
            "reason_class": "LossHistoryDiffers",
            "status": cs.ARM_COMPLETED,
        }
    )

    def _fail_c9(**_kwargs):
        raise cs.EquivalenceFailure(
            "second comparison failed",
            document={
                "arms": c9,
                "checkpoints_written": 2,
                "fits_attempted": 2,
            },
        )

    monkeypatch.setattr(cs, "equivalence_gate", _fail_c9)
    code = cs.main(
        [
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
    )
    assert code == cs.EXIT_CODES[cs.X_EQUIVALENCE_FAILED]
    document = json.loads(
        (tmp_path / "stage1-run-1" / cs.RUN_ARTIFACT).read_text(encoding="utf-8")
    )
    assert len(document["curve_arms"]) == 50
    assert sum(arm["status"] == cs.ARM_REUSED for arm in document["curve_arms"]) == 10
    assert sum(arm["status"] == cs.ARM_UNATTEMPTED for arm in document["curve_arms"]) == 40
    assert document["equivalence_arms"] == c9
    assert document["equivalence_fits_attempted"] == 2
    assert document["equivalence_checkpoints_written"] == 2
    assert document["curve_fits_attempted"] == 0
    assert document["curve_checkpoints_written"] == 0


# ---------------------------------------------------------------------------
# Invariant C9 -- the equivalence gate, driven without any real checkpoint
# ---------------------------------------------------------------------------
def test_the_bit_identity_comparison_accepts_the_same_weights():
    """The accept side, so the four refusals below are not vacuous."""

    left = cs.build_network(channels=16, seed=1).state_dict()
    right = cs.build_network(channels=16, seed=1).state_dict()
    identical, reason = cs.state_dicts_are_bit_identical(left, right)
    assert identical and reason == ""


def test_the_bit_identity_comparison_catches_a_single_changed_element():
    """One element, not one tensor: `torch.equal` is the whole claim."""

    left = cs.build_network(channels=16, seed=1).state_dict()
    right = {name: tensor.clone() for name, tensor in left.items()}
    name = sorted(right)[0]
    right[name] = right[name].clone()
    flat = right[name].view(-1)
    flat[0] = flat[0] + 1.0e-7
    identical, reason = cs.state_dicts_are_bit_identical(left, right)
    assert not identical and "bit-identical" in reason


def test_the_bit_identity_comparison_catches_a_shape_a_dtype_and_a_name():
    """Three ways two state dicts differ that an element-wise test alone would miss."""

    left = cs.build_network(channels=16, seed=1).state_dict()
    name = sorted(left)[0]

    # The reason string is asserted, not only the verdict: a shape mismatch also fails
    # the element-wise comparison one line later, so without pinning the message the
    # shape branch could be deleted and nothing would go red (Session-92 sweep).
    shaped = {key: value for key, value in left.items()}
    shaped[name] = torch.zeros(left[name].shape + (1,))
    identical, reason = cs.state_dicts_are_bit_identical(left, shaped)
    assert not identical and "shape" in reason

    typed = {key: value for key, value in left.items()}
    typed[name] = left[name].to(torch.float64)
    identical, reason = cs.state_dicts_are_bit_identical(left, typed)
    assert not identical and "dtype" in reason

    named = {key: value for key, value in left.items()}
    named["extra"] = torch.zeros(1)
    identical, reason = cs.state_dicts_are_bit_identical(left, named)
    assert not identical and "parameter names differ" in reason


def test_c9_refuses_when_an_approved_checkpoint_is_absent(tmp_path, examples, protocol):
    """A fresh clone carries the ledger without the weights; that is a refusal."""

    ledger, checkpoint_dir, _ = _synthetic_equivalence_world(tmp_path)
    for path in checkpoint_dir.glob("*.pt"):
        path.unlink()
    with pytest.raises(cs.EquivalenceFailure, match="not on disk") as caught:
        cs.equivalence_gate(
            examples_by_suite={suite: examples for suite in MATCHED_FIT_SUITES},
            ledger=ledger,
            checkpoint_dir=checkpoint_dir,
            scratch_dir=tmp_path / "run" / cs.EQUIVALENCE_SUBTREE,
            protocol=protocol,
        )
    document = caught.value.document
    assert document["fits_attempted"] == document["checkpoints_written"] == 0
    assert [arm["status"] for arm in document["arms"]] == [
        cs.ARM_REFUSED,
        cs.ARM_UNATTEMPTED,
    ]
    assert (tmp_path / "run" / cs.EQUIVALENCE_SUBTREE / cs.EQUIVALENCE_ARTIFACT).is_file()


def test_c9_refuses_when_the_ledger_has_no_row_for_an_arm(tmp_path, examples, protocol):
    """The comparison must be makeable, and this is one way it is not."""

    ledger, checkpoint_dir, _ = _synthetic_equivalence_world(tmp_path)
    # Drop the FIRST arm, so the gate meets the missing row before it fits anything.
    ledger["arms"] = ledger["arms"][1:]
    with pytest.raises(cs.EquivalenceFailure, match="no .* arm to compare against"):
        cs.equivalence_gate(
            examples_by_suite={suite: examples for suite in MATCHED_FIT_SUITES},
            ledger=ledger,
            checkpoint_dir=checkpoint_dir,
            scratch_dir=tmp_path / "run" / cs.EQUIVALENCE_SUBTREE,
            protocol=protocol,
        )


def test_c9_authenticates_the_approved_checkpoint_bytes_before_fitting(
    tmp_path, examples, protocol, monkeypatch
):
    """The ledger digest names the bytes loaded; a same-name replacement cannot pass."""

    ledger, checkpoint_dir, _ = _synthetic_equivalence_world(tmp_path)
    ledger["arms"][0]["checkpoint_sha256"] = "0" * 64

    def _fit_must_not_run(*_args, **_kwargs):
        raise AssertionError("C9 fitted before authenticating the approved checkpoint")

    monkeypatch.setattr(cs, "fit_arm_at_width", _fit_must_not_run)
    with pytest.raises(cs.EquivalenceFailure, match="digest in the approved ledger") as caught:
        cs.equivalence_gate(
            examples_by_suite={suite: examples for suite in MATCHED_FIT_SUITES},
            ledger=ledger,
            checkpoint_dir=checkpoint_dir,
            scratch_dir=tmp_path / "run" / cs.EQUIVALENCE_SUBTREE,
            protocol=protocol,
        )
    assert caught.value.document["fits_attempted"] == 0
    assert caught.value.document["checkpoints_written"] == 0
    assert caught.value.document["arms"][0]["reason_class"] == (
        "ApprovedCheckpointDigestMismatch"
    )


def test_c9_refuses_when_the_produced_weights_differ(tmp_path, examples, protocol, monkeypatch):
    """The gate's whole purpose: a diverged copied loop must not produce a curve."""

    ledger, checkpoint_dir, states = _synthetic_equivalence_world(tmp_path)

    def _diverged(_examples, *, seed, channels, **_kwargs):
        net = cs.build_network(channels=channels, seed=seed)
        with torch.no_grad():
            next(iter(net.parameters())).add_(1.0)
        return net, [1.0, 0.5]

    monkeypatch.setattr(cs, "fit_arm_at_width", _diverged)
    with pytest.raises(cs.EquivalenceFailure, match="did not reproduce the approved"):
        cs.equivalence_gate(
            examples_by_suite={suite: examples for suite in MATCHED_FIT_SUITES},
            ledger=ledger,
            checkpoint_dir=checkpoint_dir,
            scratch_dir=tmp_path / "run" / cs.EQUIVALENCE_SUBTREE,
            protocol=protocol,
        )


def test_c9_refuses_when_only_the_loss_history_differs(tmp_path, examples, protocol, monkeypatch):
    """Identical weights are not enough: the per-epoch history is part of the claim.

    The difference used here is **one part in 10^9**, deliberately below any tolerance a
    reviewer might reach for. Session-92 mutation sweep: with a 1e-4 difference, replacing
    the exact comparison with `abs(a - b) > 1e-6` still refused, so the test could not see
    the weakening it exists to prevent. "Bit-identical" has to be tested at bit scale.
    """

    ledger, checkpoint_dir, _ = _synthetic_equivalence_world(tmp_path)

    def _wrong_history(_examples, *, seed, channels, **_kwargs):
        return cs.build_network(channels=channels, seed=seed), [1.0, 0.5 + 1.0e-9]

    monkeypatch.setattr(cs, "fit_arm_at_width", _wrong_history)
    with pytest.raises(cs.EquivalenceFailure, match="per-epoch loss history"):
        cs.equivalence_gate(
            examples_by_suite={suite: examples for suite in MATCHED_FIT_SUITES},
            ledger=ledger,
            checkpoint_dir=checkpoint_dir,
            scratch_dir=tmp_path / "run" / cs.EQUIVALENCE_SUBTREE,
            protocol=protocol,
        )


def test_c9_failure_preserves_the_first_pass_and_the_second_failure(
    tmp_path, examples, protocol, monkeypatch
):
    """A later C9 refusal cannot erase a fit/checkpoint already spent by the first arm."""

    ledger, checkpoint_dir, _ = _synthetic_equivalence_world(tmp_path)

    def _second_history_differs(_examples, *, seed, channels, **_kwargs):
        history = [1.0, 0.5] if seed == 0 else [1.0, 0.5 + 1.0e-9]
        return cs.build_network(channels=channels, seed=seed), history

    monkeypatch.setattr(cs, "fit_arm_at_width", _second_history_differs)
    scratch = tmp_path / "run" / cs.EQUIVALENCE_SUBTREE
    with pytest.raises(cs.EquivalenceFailure, match="per-epoch loss history") as caught:
        cs.equivalence_gate(
            examples_by_suite={suite: examples for suite in MATCHED_FIT_SUITES},
            ledger=ledger,
            checkpoint_dir=checkpoint_dir,
            scratch_dir=scratch,
            protocol=protocol,
        )
    document = caught.value.document
    assert document["fits_attempted"] == 2
    assert document["checkpoints_written"] == 2
    assert [arm["status"] for arm in document["arms"]] == [
        cs.ARM_COMPLETED,
        cs.ARM_COMPLETED,
    ]
    assert [arm["comparison"] for arm in document["arms"]] == [
        cs.COMPARISON_PASS,
        cs.COMPARISON_FAIL,
    ]
    assert json.loads((scratch / cs.EQUIVALENCE_ARTIFACT).read_text(encoding="utf-8")) == document


def test_c9_passes_and_writes_into_the_reserved_subtree(tmp_path, examples, protocol, monkeypatch):
    """The accept side, and the placement of what it writes."""

    ledger, checkpoint_dir, _ = _synthetic_equivalence_world(tmp_path)

    def _matching(_examples, *, seed, channels, **_kwargs):
        return cs.build_network(channels=channels, seed=seed), [1.0, 0.5]

    monkeypatch.setattr(cs, "fit_arm_at_width", _matching)
    run_root = tmp_path / "run"
    document = cs.equivalence_gate(
        examples_by_suite={suite: examples for suite in MATCHED_FIT_SUITES},
        ledger=ledger,
        checkpoint_dir=checkpoint_dir,
        scratch_dir=run_root / cs.EQUIVALENCE_SUBTREE,
        protocol=protocol,
    )
    assert [arm["comparison"] for arm in document["arms"]] == [cs.COMPARISON_PASS] * 2
    assert [arm["status"] for arm in document["arms"]] == [cs.ARM_COMPLETED] * 2
    assert document["fits_attempted"] == document["checkpoints_written"] == 2
    assert document["rollouts_spent"] == 0
    scratch = run_root / cs.EQUIVALENCE_SUBTREE
    assert (scratch / cs.EQUIVALENCE_ARTIFACT).is_file()
    assert len(list(scratch.glob("*.pt"))) == 2
    for arm in document["arms"]:
        assert re.fullmatch(r"[0-9a-f]{64}", arm["produced_checkpoint_sha256"])
        assert arm["fit_code_identity"] == document["code_identity"]


def test_the_equivalence_arms_are_the_two_the_design_rules(tmp_path):
    """Codex's Session-88 ruling 5: `(C1, 0)` and `(S, 4)`, both suites, two seeds."""

    assert cs.EQUIVALENCE_ARMS == (("C1", 0), ("S", 4))
    assert {suite for suite, _ in cs.EQUIVALENCE_ARMS} == set(MATCHED_FIT_SUITES)


# ---------------------------------------------------------------------------
# The copied fit loop
# ---------------------------------------------------------------------------
def test_the_fit_loop_refuses_an_empty_example_set(protocol):
    """The approved trainer's refusal, preserved in the copy."""

    with pytest.raises(trainer.DevFitDataError, match="empty row set"):
        cs.fit_arm_at_width(
            [],
            seed=0,
            channels=16,
            epochs=1,
            batch_size=1,
            learning_rate=1e-3,
            device=torch.device("cpu"),
        )


def test_the_fit_loop_refuses_a_nonfinite_loss_before_any_checkpoint(monkeypatch, examples):
    """A diverged optimizer path is a named data failure, not invalid JSON later."""

    def _nonfinite(_heads, batch):
        return torch.tensor(float("nan"), device=batch["inputs"].device, requires_grad=True)

    monkeypatch.setattr(cs, "arm_loss", _nonfinite)
    with pytest.raises(trainer.DevFitDataError, match="non-finite"):
        cs.fit_arm_at_width(
            examples,
            seed=0,
            channels=16,
            epochs=1,
            batch_size=1,
            learning_rate=1e-3,
            device=torch.device("cpu"),
        )


def test_the_fit_loop_is_reproducible_at_one_seed_and_width(examples):
    """Two runs of the copied loop at one `(channels, seed)` produce identical weights."""

    first, first_history = cs.fit_arm_at_width(
        examples,
        seed=0,
        channels=16,
        epochs=1,
        batch_size=2,
        learning_rate=1e-3,
        device=torch.device("cpu"),
    )
    second, second_history = cs.fit_arm_at_width(
        examples,
        seed=0,
        channels=16,
        epochs=1,
        batch_size=2,
        learning_rate=1e-3,
        device=torch.device("cpu"),
    )
    identical, reason = cs.state_dicts_are_bit_identical(
        first.state_dict(), second.state_dict()
    )
    assert identical, reason
    assert first_history == second_history


def test_two_widths_at_one_seed_do_not_share_an_initialization(examples):
    """Design section 4.3 claim 3: the initialization is NOT common across widths."""

    narrow = cs.build_network(channels=16, seed=3)
    wide = cs.build_network(channels=24, seed=3)
    assert not cs.state_dicts_are_bit_identical(narrow.state_dict(), wide.state_dict())[0]


def test_the_row_order_is_common_across_widths():
    """Design section 4.3 claim 2: the permutation depends only on seed and count."""

    for seed in PREDECLARED_TRAINING_SEEDS:
        first = np.random.default_rng(seed).permutation(152)
        second = np.random.default_rng(seed).permutation(152)
        assert np.array_equal(first, second)


def test_scoring_returns_the_approved_analyzers_three_metrics(examples):
    """`score_arm` reports what `classification_metrics` computes, and nothing else."""

    net = cs.build_network(channels=16, seed=0)
    metrics = cs.score_arm(net, examples)
    assert set(metrics) == {"accuracy", "macro_f1", "per_class_f1"}
    assert 0.0 <= metrics["macro_f1"] <= 1.0
    assert set(metrics["per_class_f1"]) == set(approved_analysis.SOURCE_CLASS_ORDER)


# ---------------------------------------------------------------------------
# Invariant C10 -- no partial run presents itself as a curve
# ---------------------------------------------------------------------------
def _complete_run_document() -> dict:
    """Return a synthetic run artifact that satisfies C10."""

    curve = [
        {"channels": 32, "suite": suite, "seed": seed, "status": cs.ARM_REUSED}
        for _, suite, seed in cs.anchor_arms()
    ] + [
        {"channels": channels, "suite": suite, "seed": seed, "status": cs.ARM_COMPLETED}
        for channels, suite, seed in cs.curve_arms()
    ]
    equivalence = [
        {
            "suite": suite,
            "seed": seed,
            "status": cs.ARM_COMPLETED,
            "comparison": cs.COMPARISON_PASS,
        }
        for suite, seed in cs.EQUIVALENCE_ARMS
    ]
    return {"curve_arms": curve, "equivalence_arms": equivalence}


def test_c10_accepts_a_complete_run():
    """The accept side, so the refusals below are not vacuous."""

    cs.require_complete_sweep(_complete_run_document())


def test_c10_refuses_a_missing_anchor():
    """Ten `REUSED` anchors, exactly."""

    document = _complete_run_document()
    document["curve_arms"] = document["curve_arms"][1:]
    with pytest.raises(DevFitContractError, match="reuses exactly"):
        cs.require_complete_sweep(document)


def test_c10_refuses_thirty_nine_completed_arms():
    """Forty new arms, exactly; a partial sweep is not a curve."""

    document = _complete_run_document()
    document["curve_arms"] = [
        arm for arm in document["curve_arms"] if arm["status"] == cs.ARM_REUSED
    ] + [
        arm for arm in document["curve_arms"] if arm["status"] == cs.ARM_COMPLETED
    ][:39]
    with pytest.raises(DevFitContractError, match="completes exactly"):
        cs.require_complete_sweep(document)


def test_c10_refuses_a_refused_arm_alongside_a_full_set():
    """An arm that is neither reused nor completed is a refusal, not a footnote."""

    document = _complete_run_document()
    document["curve_arms"].append(
        {"channels": 40, "suite": "S", "seed": 2, "status": cs.ARM_REFUSED}
    )
    with pytest.raises(DevFitContractError, match="neither reused nor completed"):
        cs.require_complete_sweep(document)


@pytest.mark.parametrize(
    ("key", "value"),
    [("comparison", cs.COMPARISON_FAIL), ("status", cs.ARM_UNATTEMPTED)],
)
def test_c10_refuses_an_equivalence_arm_that_did_not_pass(key, value):
    """Both equivalence arms must complete and both must report `PASS`."""

    document = _complete_run_document()
    document["equivalence_arms"][1][key] = value
    with pytest.raises(DevFitContractError, match="complete and to pass"):
        cs.require_complete_sweep(document)


def test_c10_refuses_a_single_equivalence_arm():
    """Two arms are the ruled design; one is not a compatibility gate."""

    document = _complete_run_document()
    document["equivalence_arms"] = document["equivalence_arms"][:1]
    with pytest.raises(DevFitContractError, match="exactly 2 equivalence"):
        cs.require_complete_sweep(document)


@pytest.mark.parametrize("family", ["anchor", "curve", "equivalence"])
def test_c10_refuses_a_duplicate_that_replaces_one_required_identity(family):
    """Correct counts are insufficient when one required arm is missing and another repeats."""

    document = _complete_run_document()
    if family == "anchor":
        records = [
            arm for arm in document["curve_arms"] if arm["status"] == cs.ARM_REUSED
        ]
    elif family == "curve":
        records = [
            arm for arm in document["curve_arms"] if arm["status"] == cs.ARM_COMPLETED
        ]
    else:
        records = document["equivalence_arms"]
    records[-1].update(records[-2])
    with pytest.raises(DevFitContractError, match="identit"):
        cs.require_complete_sweep(document)


def test_c10_refuses_an_unhashable_malformed_identity_as_a_contract_error():
    """Malformed JSON values fail closed instead of escaping as a Python TypeError."""

    document = _complete_run_document()
    document["curve_arms"][0]["suite"] = ["C1"]
    with pytest.raises(DevFitContractError, match="malformed identity"):
        cs.require_complete_sweep(document)


def test_partial_run_templates_name_every_arm_before_work_begins():
    """A post-claim refusal records downstream arms as UNATTEMPTED, never by omission."""

    curve = cs.initial_curve_arm_records()
    equivalence = cs.initial_equivalence_arm_records()
    assert len(curve) == 50
    assert len({(arm["channels"], arm["suite"], arm["seed"]) for arm in curve}) == 50
    assert {arm["status"] for arm in curve} == {cs.ARM_UNATTEMPTED}
    assert len(equivalence) == 2
    assert {(arm["suite"], arm["seed"]) for arm in equivalence} == set(
        cs.EQUIVALENCE_ARMS
    )
    assert {arm["status"] for arm in equivalence} == {cs.ARM_UNATTEMPTED}
    assert {arm["comparison"] for arm in equivalence} == {cs.COMPARISON_NOT_RUN}


# ---------------------------------------------------------------------------
# The pre-declared descriptive read of design section 5
# ---------------------------------------------------------------------------
def test_headroom_is_an_exact_upper_bound_on_the_paired_difference():
    """`|d| = max - min <= 1 - min(...)` identically, over a grid rather than examples."""

    grid = [i / 20.0 for i in range(21)]
    for left in grid:
        for right in grid:
            assert abs(right - left) <= cs.headroom(left, right) + 1e-12


@pytest.mark.parametrize("bad", [-0.1, 1.1, float("nan"), float("inf")])
def test_headroom_refuses_a_macro_f1_outside_the_unit_interval(bad):
    """The bound is only exact for values the quantity can actually take."""

    with pytest.raises(cs.CapacitySweepError):
        cs.headroom(0.5, bad)


def test_the_anchor_point_is_not_bar_constrained():
    """Design section 5.1's measured claim, re-derived from the approved artifact.

    The design states the rung-1 per-seed headroom as 0.3157 to 0.5133 and `c = 32` as
    `NONE`. Both are recomputed here from the artifact's own published per-seed macro-F1
    rather than quoted, because a number carried from a document into a test is a copy.
    """

    analysis = json.loads(APPROVED_ANALYSIS_PATH.read_text(encoding="utf-8"))
    bar = cs.read_success_bar(analysis)
    headrooms = [
        cs.headroom(entry["C1_macro_f1"], entry["S_macro_f1"])
        for entry in analysis["paired_macro_f1"]["by_seed"]
    ]
    assert len(headrooms) == 5
    assert 0.315 < min(headrooms) < 0.316
    assert 0.513 < max(headrooms) < 0.514
    assert cs.pair_constraint(headrooms, bar) == cs.CONSTRAINT_NONE


@pytest.mark.parametrize(
    ("headrooms", "expected"),
    [
        ([0.4, 0.4, 0.4, 0.4, 0.4], cs.CONSTRAINT_NONE),
        ([0.04, 0.4, 0.4, 0.4, 0.4], cs.CONSTRAINT_PARTIAL),
        ([0.04, 0.04, 0.04, 0.04, 0.04], cs.CONSTRAINT_ALL),
        ([0.05, 0.05, 0.05, 0.05, 0.05], cs.CONSTRAINT_NONE),
        ([0.049999, 0.05, 0.4, 0.4, 0.4], cs.CONSTRAINT_PARTIAL),
        # Four of five: the case that separates `ALL` from "nearly all". Without it, a
        # rule reading `>= n - 1` calls this point `ALL` and silently drops a seed's
        # worth of readable evidence out of the eligible subsequence.
        ([0.04, 0.04, 0.04, 0.04, 0.4], cs.CONSTRAINT_PARTIAL),
        ([0.4, 0.04, 0.04, 0.04, 0.04], cs.CONSTRAINT_PARTIAL),
    ],
)
def test_the_constraint_criterion_aggregates_per_pair_then_per_point(headrooms, expected):
    """Codex's aggregation finding: a point mean hides saturated and unsaturated seeds."""

    assert cs.pair_constraint(headrooms, 0.05) == expected


def test_the_constraint_criterion_refuses_an_empty_point_and_a_bad_bar():
    """The criterion is defined over pairs and a bar, and refuses without either."""

    with pytest.raises(cs.CapacitySweepError):
        cs.pair_constraint([], 0.05)
    with pytest.raises(cs.CapacitySweepError):
        cs.pair_constraint([0.4], 0.0)


@pytest.mark.parametrize(
    ("values", "label"),
    [
        ([0.1], cs.SHAPE_UNDEFINED),
        ([], cs.SHAPE_UNDEFINED),
        ([0.2, 0.2, 0.2], cs.SHAPE_FLAT),
        ([0.1, 0.2, 0.3], cs.SHAPE_STRICTLY_INCREASING),
        ([0.3, 0.2, 0.1], cs.SHAPE_STRICTLY_DECREASING),
        ([0.1, 0.1, 0.2], cs.SHAPE_NON_DECREASING),
        ([0.2, 0.2, 0.1], cs.SHAPE_NON_INCREASING),
        ([0.1, 0.3, 0.2], cs.SHAPE_NON_MONOTONE),
        ([-0.05, -0.01, 0.02], cs.SHAPE_STRICTLY_INCREASING),
    ],
)
def test_the_shape_classifier_is_exhaustive_and_ordered(values, label):
    """Seven conditions, evaluated in the document's order, over the eligible sequence."""

    assert cs.classify_shape(values) == label


def test_the_shape_classifier_reads_ties_at_the_declared_resolution():
    """Classification happens on quantized values, so a sub-quantum move is a tie."""

    assert cs.classify_shape([0.2, 0.2 + 1e-9, 0.2 + 2e-9]) == cs.SHAPE_FLAT
    assert cs.classify_shape([0.2, 0.200001, 0.200002]) == cs.SHAPE_STRICTLY_INCREASING


@pytest.mark.parametrize(
    ("value", "expected"),
    [
        (0.0, "0.000000"),
        (0.5, "0.500000"),
        (-0.032088741654, "-0.032089"),
        (0.0000005, "0.000000"),
        (0.0000015, "0.000002"),
        (0.0000025, "0.000002"),
    ],
)
def test_the_quantization_is_six_decimal_round_half_even(value, expected):
    """A predeclared numerical tie rule, and both halves of the half-even behaviour."""

    assert cs.quantize(value) == expected


@pytest.mark.parametrize("bad", [float("nan"), float("inf"), None, "0.1", True])
def test_quantization_refuses_what_it_cannot_classify(bad):
    """A non-finite or non-numeric value is a refusal rather than a plausible string."""

    with pytest.raises(cs.CapacitySweepError):
        cs.quantize(bad)


@pytest.mark.parametrize(
    ("first", "eligible", "points", "label"),
    [
        (40, 40, [40, 48], cs.LABEL_ELIGIBLE),
        (40, None, [40, 48], cs.LABEL_CONSTRAINED_ONLY),
        (None, None, [], cs.LABEL_NO_ELIGIBLE_POINTS),
        (None, None, [40, 48], cs.LABEL_NONE),
        (48, 48, [], cs.LABEL_ELIGIBLE),
    ],
)
def test_the_derived_label_is_exhaustive_and_evaluated_in_order(first, eligible, points, label):
    """Four conditions in order; the eligible branch wins over the constrained one."""

    assert (
        cs.derived_label(
            first_post_anchor_nonnegative_point=first,
            first_eligible_post_anchor_nonnegative_point=eligible,
            eligible_post_anchor_points=points,
        )
        == label
    )


def test_the_derived_label_is_a_pure_function_of_persisted_primitives():
    """It cannot drift from the numbers it summarises, because it reads only them."""

    arguments = {
        "first_post_anchor_nonnegative_point": 40,
        "first_eligible_post_anchor_nonnegative_point": None,
        "eligible_post_anchor_points": [48],
    }
    assert cs.derived_label(**arguments) == cs.derived_label(**arguments)


# ---------------------------------------------------------------------------
# Design section 5.3 -- what the executable must never emit
# ---------------------------------------------------------------------------
@pytest.mark.parametrize(
    "forbidden",
    ["CAPACITY_BOUND", "NOT_CAPACITY_BOUND", "capacity_bound", "caused_by_capacity"],
)
def test_the_executable_emits_no_causal_verdict(forbidden):
    """Design section 5.3, checked over the module's own text."""

    assert forbidden not in Path(cs.__file__).read_text(encoding="utf-8")


def test_no_document_this_module_writes_carries_a_recommendation(tmp_path, protocol):
    """No recommendation, licence or authorization of any kind."""

    document = cs.plan_document(run_label="stage1-run-1", protocol=protocol)
    text = canonical_json(document).lower()
    for forbidden in ("recommend", "authorized to escalate", "stage 2", "stage2"):
        assert forbidden not in text


def test_every_document_asserts_the_zero_resource_counts(tmp_path, protocol):
    """Invariant C8: asserted and persisted on every exit path."""

    plan = cs.plan_document(run_label="stage1-run-1", protocol=protocol)
    assert plan["maximum_budget"]["rollouts"] == 0
    assert plan["maximum_budget"]["generation_runs"] == 0
    assert plan["maximum_budget"]["non_dev_reads"] == 0

    run = cs.run_document(
        exit_name=cs.X_SWEEP_OK,
        reason_class=None,
        run_label="stage1-run-1",
        approved_plan_sha256="a" * 64,
        code_identity=cs.sweep_code_identity(),
        protocol=protocol,
        curve=[],
        equivalence=[],
        equivalence_fits_attempted=1,
        equivalence_checkpoints_written=1,
        curve_fits_attempted=2,
        curve_checkpoints_written=2,
        census=None,
        elapsed_s=0.0,
    )
    assert run["rollouts_spent"] == 0
    assert run["generation_runs"] == 0
    assert run["non_dev_reads"] == 0
    assert run["mode"] == "execute"
    assert run["design_sha256"] == cs.DESIGN_CANONICAL_SHA256
    assert run["fits_attempted"] == run["checkpoints_written"] == 3
    assert run["equivalence_fits_attempted"] == 1
    assert run["equivalence_checkpoints_written"] == 1
    assert run["curve_fits_attempted"] == 2
    assert run["curve_checkpoints_written"] == 2


def test_every_named_exit_has_a_distinct_code_and_is_referenced():
    """A name rather than a bare integer, and no two refusals sharing a code.

    The two success exits deliberately share code 0, exactly as the approved trainer's
    `X_PLAN_OK` and `X_FIT_OK` do; every refusal is separately identifiable.
    """

    successes = {cs.X_PLAN_OK, cs.X_SWEEP_OK}
    assert all(cs.EXIT_CODES[name] == 0 for name in successes)
    refusals = {
        name: code for name, code in cs.EXIT_CODES.items() if name not in successes
    }
    assert len(set(refusals.values())) == len(refusals)
    assert 0 not in refusals.values()
    source = Path(cs.__file__).read_text(encoding="utf-8")
    for name in cs.EXIT_CODES:
        assert name.startswith("X_")
        assert source.count(f"{name} = ") == 1


def test_the_per_point_cleanliness_guard_still_refuses_a_stale_checkpoint(tmp_path):
    """Defence in depth: unreachable on the ordinary path, still correct."""

    point = tmp_path / "channels_040"
    point.mkdir()
    cs.require_clean_capacity_point(point)
    (point / "capacity_sweep_ch040_S_seed2.pt").write_bytes(b"stale")
    with pytest.raises(DevFitContractError, match="earlier attempt"):
        cs.require_clean_capacity_point(point)


def test_the_checkpoint_names_are_unique_across_the_whole_sweep():
    """Fifty arms, and no two of them naming one file."""

    names = {
        cs.checkpoint_relative_name(channels, suite, seed)
        for channels, suite, seed in cs.curve_arms()
    }
    assert len(names) == len(cs.curve_arms())
    equivalence = {cs.equivalence_relative_name(suite, seed) for suite, seed in cs.EQUIVALENCE_ARMS}
    assert len(equivalence) == len(cs.EQUIVALENCE_ARMS)
    assert not names & equivalence
