"""Tests for the development-only fitting contract (`utils.dev_fit_contract`).

Every refusal below is driven by constructing the exact state it exists to catch, and
every accept side is driven by the inputs the trainer will really hand it — a guard that
refuses everything is not a guard (Session 52).

Two disciplines shape the file. The constants that *are* decisions (the seed set, the
matched suites, the withheld splits, the authority string) are pinned by EQUALITY rather
than parametrized over, because a test that iterates a list is a statement about whatever
the list happens to say and stays green when a member is added or dropped (Session 71).
And the authority string is compared against two independent sources outside this
package's own copy — the payload-boundary extension's constant and the frozen extension
document — because a literal copied from a document is a second copy, not a second
source (requirement (r)).
"""

from __future__ import annotations

import importlib.util
import subprocess
import sys
from pathlib import Path, PurePosixPath, PureWindowsPath

import pytest

SCRIPTS_DIR = Path(__file__).resolve().parents[1] / "scripts"
PACKET_DIR = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(SCRIPTS_DIR))

from utils.attribution_net import (  # noqa: E402
    TemporalAttributionEstimator,
    TemporalAttributionNet,
)
from utils.dev_fit_contract import (  # noqa: E402
    AUTHORIZED_FIT_SPLIT,
    DEVELOPMENT_ONLY_AUTHORITY,
    MATCHED_FIT_SUITES,
    PREDECLARED_TRAINING_SEEDS,
    RESERVED_COMPONENT_NAMES,
    WITHHELD_SPLITS,
    DevFitContractError,
    DevFitProvenance,
    code_identity,
    matched_fit_plan,
    require_bare_name,
    require_complete_matched_plan,
    require_dev_only,
    require_matched_fit_suite,
    require_predeclared_seed,
    select_dev_rows,
)
from utils.estimator import WindowFeatureExtractor  # noqa: E402
from utils.protocol_p import ASSIGNMENT_CANONICAL_SHA256, canonical_text_sha256  # noqa: E402
from utils.storage_contract import IdentityManifestRow, write_identity_manifest  # noqa: E402

EXTENSION_SCRIPT = SCRIPTS_DIR / "run_payload_boundary_extension.py"
EXTENSION_DOCUMENT = PACKET_DIR / "protocol" / "payload-boundary-extension-v0.2.md"

_A_DIGEST = "a" * 64
_B_DIGEST = "b" * 64
_CONFIG_HASH = "dev-" + "c" * 64


def _row(split: str, suite: str, index: int) -> IdentityManifestRow:
    """One schema-A identity row with the fields this contract reads set meaningfully."""

    return IdentityManifestRow(
        schema_version="1.0",
        config_hash=_CONFIG_HASH,
        scenario_spec_id=f"scenario_{split}_t01_f000_r{index:02d}",
        pair_id=f"basepair_{split}_t01_f000_r{index:02d}_dataset0",
        run_id=f"scenario_{split}_t01_f000_r{index:02d}_{suite}_dataset0",
        trajectory_spec_id=f"trajectory_{split}_diagnostic_b",
        fault_setting_id=f"fault_{split}_healthy",
        split_group_id=f"group_{split}_{index}",
        split=split,
        suite=suite,
        estimator_id="estimator_none",
        controller_id="controller_task",
        payload_id=f"payload_{split}_0",
        env_profile_id=f"env_{split}_iso25c",
        contact_profile_id=f"contact_{split}_none",
        sim_seed=110000 + index * 10,
        fault_seed=110001 + index * 10,
        sensor_seed=110002 + index * 10,
        controller_seed=110003 + index * 10,
        train_seed=110004 + index * 10,
    )


def _manifest(tmp_path: Path, rows: list[IdentityManifestRow]) -> Path:
    path = tmp_path / "manifest.csv"
    write_identity_manifest(path, rows)
    return path


def _valid_provenance(**overrides) -> DevFitProvenance:
    fields = dict(
        data_root_name="gate3-base-dev-pilot-val-c1-s",
        manifest_sha256=_A_DIGEST,
        config_hash=_CONFIG_HASH,
        assignment_sha256=ASSIGNMENT_CANONICAL_SHA256,
        suite="S",
        training_seed=0,
        checkpoint_sha256=_B_DIGEST,
        code_identity={"attribution_net.py": _A_DIGEST},
        row_disclosure="152 of 944 manifest rows selected (split: dev 304, pilot 304, val 336).",
    )
    fields.update(overrides)
    return DevFitProvenance(**fields)


# --------------------------------------------------------------------------- #
# The authority string, checked against sources outside this package's copy.
# --------------------------------------------------------------------------- #
def test_the_authority_string_equals_the_extension_scripts_own_constant():
    """Requirement (r): the copy is only safe while something compares it to a source."""

    spec = importlib.util.spec_from_file_location("_extension_probe", EXTENSION_SCRIPT)
    module = importlib.util.module_from_spec(spec)
    sys.modules["_extension_probe"] = module
    spec.loader.exec_module(module)
    assert DEVELOPMENT_ONLY_AUTHORITY == module.AUTHORITY


def test_the_authority_string_is_lifted_verbatim_from_the_frozen_document():
    """The second source: the frozen extension document, read rather than transcribed."""

    lines = EXTENSION_DOCUMENT.read_text(encoding="utf-8").splitlines()
    matches = [line.strip() for line in lines if line.strip().startswith("DEVELOPMENT ONLY:")]
    assert matches == [DEVELOPMENT_ONLY_AUTHORITY]


# --------------------------------------------------------------------------- #
# Constants that ARE decisions get equality pins, not parametrization.
# --------------------------------------------------------------------------- #
def test_the_predeclared_seed_set_is_pinned_by_equality():
    """Dropping or adding a seed changes what a fit may run; a loop over it would not notice."""

    assert PREDECLARED_TRAINING_SEEDS == (0, 1, 2, 3, 4)
    assert len(PREDECLARED_TRAINING_SEEDS) >= 5, "Slot 7 requires at least five seeds"
    assert len(set(PREDECLARED_TRAINING_SEEDS)) == len(PREDECLARED_TRAINING_SEEDS)


def test_the_matched_suites_and_withheld_splits_are_pinned_by_equality():
    assert MATCHED_FIT_SUITES == ("C1", "S")
    assert AUTHORIZED_FIT_SPLIT == "dev"
    assert WITHHELD_SPLITS == ("pilot", "val", "test")
    assert AUTHORIZED_FIT_SPLIT not in WITHHELD_SPLITS


def test_the_reserved_component_names_are_pinned_by_equality():
    """`..` reads as a bare name to pathlib, so the list is load-bearing, not decoration.

    Measured while writing this file: `PureWindowsPath("..").name == ".."`, so the
    "equals its own final component" predicate accepted `..` — a value that walks *up*
    the tree the moment it is joined to a root. `PurePath(".").name` is `""` and was
    already refused. Dropping either member from the list re-opens the traversal.
    """

    assert RESERVED_COMPONENT_NAMES == (".", "..")
    assert PureWindowsPath("..").name == ".."  # the reason the list has to exist
    assert PurePosixPath(".").name == ""  # refused by the predicate alone


# --------------------------------------------------------------------------- #
# `require_bare_name` — a total predicate, driven over a grid rather than examples.
# --------------------------------------------------------------------------- #
@pytest.mark.parametrize(
    "accepted",
    ["dev", "gate3-base-dev-pilot-val-c1-s", "attribution_net.py", "a b c", "..data"],
)
def test_bare_names_are_accepted(accepted):
    """The accept side, at the shapes a real data root and a real module label take."""

    assert require_bare_name(accepted, "field") == accepted


@pytest.mark.parametrize(
    "rejected",
    [
        "/mnt/data/row.npz",
        "//host/share",
        "///",
        "/",
        "C:\\Users\\private\\row.npz",
        "C:/Users/private",
        "C:",
        "data/gate3",
        "data\\gate3",
        "gate3/",
        "gate3\\",
        ".",
        "..",
        "",
        "   ",
    ],
)
def test_path_shaped_values_are_refused(rejected):
    with pytest.raises(DevFitContractError):
        require_bare_name(rejected, "data_root_name")


def test_the_refusal_does_not_quote_the_rejected_path():
    """A message that echoes the offending path is the leak the rule exists to prevent."""

    with pytest.raises(DevFitContractError) as excinfo:
        require_bare_name(r"C:\Users\cresp\PRIVATE\row.npz", "data_root_name")
    message = str(excinfo.value)
    assert "PRIVATE" not in message
    assert "Users" not in message
    assert "data_root_name" in message


# --------------------------------------------------------------------------- #
# Seeds, suites, and the matched plan.
# --------------------------------------------------------------------------- #
def test_every_predeclared_seed_is_accepted_and_an_unlisted_one_is_not():
    for seed in PREDECLARED_TRAINING_SEEDS:
        assert require_predeclared_seed(seed) == seed
    with pytest.raises(DevFitContractError, match="not predeclared"):
        require_predeclared_seed(max(PREDECLARED_TRAINING_SEEDS) + 1)


def test_a_bool_is_not_accepted_as_a_seed():
    """`True == 1` in Python, so a bool would pass a naive membership test."""

    with pytest.raises(DevFitContractError, match="must be an int"):
        require_predeclared_seed(True)


def test_c0_is_refused_as_a_fit_suite_because_no_c0_observations_were_delivered():
    for suite in MATCHED_FIT_SUITES:
        assert require_matched_fit_suite(suite) == suite
    with pytest.raises(DevFitContractError, match="matched fit suites"):
        require_matched_fit_suite("C0")


def test_the_matched_plan_crosses_every_suite_with_every_seed():
    plan = matched_fit_plan()
    assert len(plan) == len(MATCHED_FIT_SUITES) * len(PREDECLARED_TRAINING_SEEDS)
    seeds_by_suite = {
        suite: sorted(seed for name, seed in plan if name == suite) for suite in MATCHED_FIT_SUITES
    }
    assert len(set(map(tuple, seeds_by_suite.values()))) == 1, "the arms do not share seeds"


def test_a_complete_plan_is_accepted_and_an_unbalanced_one_is_refused():
    require_complete_matched_plan(matched_fit_plan())
    short = [pair for pair in matched_fit_plan() if pair != ("S", 4)]
    with pytest.raises(DevFitContractError, match="incomplete"):
        require_complete_matched_plan(short)
    with pytest.raises(DevFitContractError, match="outside the predeclared plan"):
        require_complete_matched_plan(list(matched_fit_plan()) + [("S", 99)])


# --------------------------------------------------------------------------- #
# Row selection, its denominator, and the path a filter does not guard.
# --------------------------------------------------------------------------- #
def test_only_dev_rows_of_the_matched_suites_are_selected(tmp_path):
    """The C0 row is what makes the suite filter live.

    Found by mutation, not by reading: with only C1 and S dev rows in the fixture,
    deleting the suite filter entirely left this test green, because the fixture already
    had the property the filter establishes (Session 58's recurring shape).
    """

    rows = [
        _row("dev", "S", 0),
        _row("dev", "C1", 1),
        _row("dev", "C0", 5),
        _row("pilot", "S", 2),
        _row("val", "C1", 3),
        _row("test", "S", 4),
    ]
    selected, census = select_dev_rows(_manifest(tmp_path, rows))
    assert {row.split for row in selected} == {"dev"}
    assert {row.suite for row in selected} == {"C1", "S"}
    assert census.total_rows == 6
    assert census.selected_rows == 2
    assert census.withheld_rows == 4
    assert census.rows_by_split == {"dev": 3, "pilot": 1, "test": 1, "val": 1}
    assert census.rows_by_suite == {"C1": 1, "S": 1}


def test_an_undeliverable_suite_is_withheld_and_the_census_still_shows_it(tmp_path):
    """A dev row of an unmatched suite is dropped — and the denominator says so."""

    rows = [_row("dev", "S", 0), _row("dev", "C0", 1)]
    selected, census = select_dev_rows(_manifest(tmp_path, rows))
    assert [row.suite for row in selected] == ["S"]
    assert census.rows_by_split == {"dev": 2}
    assert census.selected_rows == 1
    assert "1 of 2 manifest rows selected" in census.disclosure()


def test_the_census_disclosure_names_its_denominator(tmp_path):
    rows = [_row("dev", "S", 0), _row("val", "S", 1)]
    _, census = select_dev_rows(_manifest(tmp_path, rows))
    disclosure = census.disclosure()
    assert "1 of 2 manifest rows selected" in disclosure
    assert "val 1" in disclosure
    assert "1 withheld" in disclosure


def test_a_manifest_with_no_dev_row_is_refused_rather_than_returned_empty(tmp_path):
    rows = [_row("val", "S", 0), _row("test", "C1", 1)]
    with pytest.raises(DevFitContractError, match="no dev row"):
        select_dev_rows(_manifest(tmp_path, rows))


def test_a_caller_built_row_list_is_still_checked():
    """The path no filter guards: rows a caller assembled instead of selecting."""

    require_dev_only([_row("dev", "S", 0), _row("dev", "C1", 1)])
    with pytest.raises(DevFitContractError, match="withheld role"):
        require_dev_only([_row("dev", "S", 0), _row("val", "S", 1)])


def test_the_withheld_role_refusal_names_the_role_and_the_count():
    with pytest.raises(DevFitContractError) as excinfo:
        require_dev_only([_row("val", "S", 0), _row("val", "C1", 1), _row("test", "S", 2)])
    message = str(excinfo.value)
    assert "test x1" in message
    assert "val x2" in message


# --------------------------------------------------------------------------- #
# Code identity.
# --------------------------------------------------------------------------- #
def test_code_identity_uses_the_text_domain_digest_of_each_named_file():
    target = SCRIPTS_DIR / "utils" / "attribution_net.py"
    identity = code_identity({"attribution_net.py": target})
    assert identity == {"attribution_net.py": canonical_text_sha256(target)}


def test_code_identity_refuses_a_missing_file_and_a_path_shaped_label(tmp_path):
    with pytest.raises(DevFitContractError, match="does not name a file"):
        code_identity({"absent.py": tmp_path / "absent.py"})
    with pytest.raises(DevFitContractError, match="bare name"):
        code_identity({"utils/attribution_net.py": SCRIPTS_DIR / "utils" / "attribution_net.py"})


# --------------------------------------------------------------------------- #
# The provenance record: one refusal per bound, each state constructed directly.
# --------------------------------------------------------------------------- #
def test_a_complete_record_validates_and_serializes_canonically():
    record = _valid_provenance().validate()
    document = record.as_document()
    assert document["authority"] == DEVELOPMENT_ONLY_AUTHORITY
    assert record.canonical_string().startswith('{"assignment_sha256"')


@pytest.mark.parametrize(
    ("override", "expected"),
    [
        ({"authority": DEVELOPMENT_ONLY_AUTHORITY.replace("ONLY", "only")}, "exact development-only"),
        ({"data_root_name": "data/gate3"}, "bare name"),
        ({"manifest_sha256": "not-a-digest"}, "manifest_sha256"),
        ({"config_hash": "c" * 64}, "config_hash must be a dev- hash"),
        ({"assignment_sha256": _A_DIGEST}, "pinned approved assignment"),
        ({"suite": "C0"}, "matched fit suites"),
        ({"training_seed": 99}, "not predeclared"),
        ({"checkpoint_sha256": "short"}, "checkpoint_sha256"),
        ({"code_identity": {}}, "code_identity must name"),
        ({"code_identity": {"attribution_net.py": "nope"}}, "64 lowercase hex"),
        ({"row_disclosure": "   "}, "row_disclosure"),
    ],
)
def test_each_bound_refuses_its_own_violation(override, expected):
    with pytest.raises(DevFitContractError, match=expected):
        _valid_provenance(**override).validate()


def test_a_frozen_looking_config_hash_is_refused_because_the_config_is_not_frozen():
    """`config.json` deliberately does not exist; a non-`dev-` hash would misstate status."""

    with pytest.raises(DevFitContractError, match="deliberately not frozen"):
        _valid_provenance(config_hash="d" * 64).validate()


# --------------------------------------------------------------------------- #
# The wire: unit-testing both ends does not test the wire (Session 44).
# --------------------------------------------------------------------------- #
def test_the_provenance_string_is_accepted_by_the_rung_and_leads_with_the_authority():
    record = _valid_provenance()
    net = TemporalAttributionNet(channels=8, n_blocks=3, seed=0, enforce_rung1_band=False)
    estimator = TemporalAttributionEstimator(net, WindowFeatureExtractor(window_steps=40))
    estimator.attach_trained_weights(
        net.state_dict(), training_provenance=record.provenance_string()
    )
    assert estimator.fitted is True
    assert estimator.training_provenance.startswith(DEVELOPMENT_ONLY_AUTHORITY)
    assert "suite=S" in estimator.training_provenance
    assert "seed=0" in estimator.training_provenance


def test_an_invalid_record_cannot_produce_a_provenance_string():
    """The record refuses before the estimator can be told anything traceable-looking."""

    with pytest.raises(DevFitContractError):
        _valid_provenance(training_seed=99).provenance_string()


def test_an_invalid_record_cannot_be_serialized_either():
    """Both renderings validate, not just the one an earlier test happened to call.

    Found by mutation: removing `validate()` from `as_document` survived the suite,
    because the only invalid-record test went through `provenance_string`. A record that
    refuses to describe itself but agrees to be written to a file is the worse half.
    """

    with pytest.raises(DevFitContractError, match="matched fit suites"):
        _valid_provenance(suite="C0").as_document()
    with pytest.raises(DevFitContractError, match="matched fit suites"):
        _valid_provenance(suite="C0").canonical_string()


# --------------------------------------------------------------------------- #
# What the module must NOT drag in.
# --------------------------------------------------------------------------- #
def test_the_contract_module_imports_neither_mujoco_nor_torch():
    """Bound 2 in import form: this layer cannot generate data because it cannot simulate.

    Measured in a fresh interpreter rather than in this one, where the test file's own
    imports have already pulled torch in.
    """

    probe = (
        "import sys; sys.path.insert(0, r'{scripts}');"
        "import utils.dev_fit_contract;"
        "print('mujoco' in sys.modules, 'torch' in sys.modules)"
    ).format(scripts=SCRIPTS_DIR)
    result = subprocess.run(
        [sys.executable, "-c", probe], capture_output=True, text=True, check=True
    )
    assert result.stdout.strip() == "False False"
