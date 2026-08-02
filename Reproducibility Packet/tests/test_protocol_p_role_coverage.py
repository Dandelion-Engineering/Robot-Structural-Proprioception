"""Tests for the Protocol P section-9 role-coverage read.

Every test here asks the question Lesson 37 requires of a new green test: what exact
state would make this red?  The accept-side tests are driven from the real committed
artifact and assignment, so they fail if either document moves; the refusal tests each
construct the one state the guard exists to catch and assert the REASON, matching a
phrase unique to a single raise site.
"""

from __future__ import annotations

import copy
import importlib.util
import json
import sys
from pathlib import Path

import pytest

PACKET_ROOT = Path(__file__).resolve().parents[1]
SCRIPTS_ROOT = PACKET_ROOT / "scripts"
sys.path.insert(0, str(SCRIPTS_ROOT))
SCRIPT = PACKET_ROOT / "scripts" / "analyze_protocol_p_role_coverage.py"
SCREEN = PACKET_ROOT / "results" / "protocol_p" / "stage_abc_screen.json"
ASSIGNMENT = PACKET_ROOT / "config" / "proposed-gate3-assignment-v0.1.json"


def _load_module():
    """Import the analysis script as a module without installing it."""
    spec = importlib.util.spec_from_file_location("protocol_p_role_coverage", SCRIPT)
    module = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = module
    spec.loader.exec_module(module)
    return module


rc = _load_module()


def _rebind_assignment(screen, assignment):
    """Bind a constructed assignment to a constructed screen for branch tests."""
    assignment["assignment_hash"] = rc.expected_assignment_hash(assignment)
    screen["inputs"]["assignment_hash"] = assignment["assignment_hash"]


@pytest.fixture(scope="module")
def screen():
    return json.loads(SCREEN.read_bytes())


@pytest.fixture(scope="module")
def assignment():
    return json.loads(ASSIGNMENT.read_bytes())


@pytest.fixture(scope="module")
def report(screen, assignment):
    return rc.compute_role_coverage(screen, assignment)


# --------------------------------------------------------------------------
# The accept side, against the real committed documents.
# --------------------------------------------------------------------------

def test_the_committed_screen_yields_zero_testable_structural_settings_in_dev(report):
    """The measured Case-B ladder leaves dev with no testable structural setting."""
    assert report["splits"]["dev"]["known_class_structural_severities"] == [0.5, 0.75]
    assert report["splits"]["dev"]["testable_severities"] == []
    assert report["splits"]["dev"]["count"] == 0


def test_the_committed_screen_counts_are_zero_zero_one_one(report):
    """dev 0, pilot 0, val 1, test 1 -- the numbers the outcome text depends on."""
    assert {s: report["splits"][s]["count"]
            for s in ("dev", "pilot", "val", "test")} == {
        "dev": 0, "pilot": 0, "val": 1, "test": 1}


def test_zero_dev_triggers_the_named_non_transfer_outcome(report):
    outcome = report["outcome"]
    assert outcome["role_coverage_bounded_non_transfer"] is True
    assert outcome["zero_count_splits"] == ["dev"]
    assert outcome["named_consequences"] == [
        {"split": "dev", "consequence": "no testable structural training support"}]


def test_zero_pilot_is_recorded_but_does_not_trigger_the_outcome(report):
    """Section 9 keys the outcome to dev/val/test only; pilot gets its own note."""
    assert "pilot" not in report["outcome"]["zero_count_splits"]
    assert "disables data-driven downsizing" in report["outcome"]["pilot_note"]


def test_val_and_test_are_reported_as_thin_single_severity_roles(report):
    assert report["outcome"]["thin_single_severity_roles"] == ["test", "val"]
    assert "opens no new terminal branch" in report["outcome"]["thin_note"]


def test_the_ood_severities_are_absent_from_this_assignments_grids(report):
    """0.45 is TESTABLE on the ladder yet appears in no split's count.

    NOTE, so this test is not mistaken for coverage of the exclusion filter: on the
    committed assignment the OOD severities live only in ``compound_ood_settings``
    and never in ``fault_grid_by_split``, so this asserts a property of the DOCUMENT.
    The filter itself is exercised by the constructed test below.
    """
    assert report["ladder_verdicts"]["0.45"] == "TESTABLE"
    for split in report["splits"].values():
        assert 0.45 not in split["known_class_structural_severities"]
        assert 0.55 not in split["known_class_structural_severities"]


def test_an_ood_severity_inside_a_split_grid_is_excluded_from_the_count(
        screen, assignment):
    """The live test of the exclusion filter.

    0.45 is TESTABLE. If it leaked into dev's known-class count, dev would read 1 and
    the named non-transfer outcome would silently clear -- an OOD label deciding a
    known-class role. Section 9: 'OOD at 0.45/0.55 never counts.'
    """
    doctored_screen = copy.deepcopy(screen)
    doctored = copy.deepcopy(assignment)
    doctored["fault_grid_by_split"]["dev"]["structure"]["severities"] = [0.45, 0.5, 0.75]
    _rebind_assignment(doctored_screen, doctored)
    report = rc.compute_role_coverage(doctored_screen, doctored)
    assert report["splits"]["dev"]["known_class_structural_severities"] == [0.5, 0.75]
    assert report["splits"]["dev"]["count"] == 0
    assert report["outcome"]["role_coverage_bounded_non_transfer"] is True


def test_a_split_with_only_ood_severities_is_refused(screen, assignment):
    """A split whose entire grid is OOD has no known-class role to count.

    Reached by construction rather than argued unreachable (Lesson 47): dev is made
    all-OOD and its two known-class severities are moved to pilot, so the
    ladder-union check still passes and execution reaches the empty-known guard.
    """
    doctored_screen = copy.deepcopy(screen)
    doctored = copy.deepcopy(assignment)
    doctored["fault_grid_by_split"]["dev"]["structure"]["severities"] = [0.45, 0.55]
    doctored["fault_grid_by_split"]["pilot"]["structure"]["severities"] = [
        0.5, 0.6, 0.75, 0.85]
    _rebind_assignment(doctored_screen, doctored)
    with pytest.raises(rc.RoleCoverageError,
                       match="exactly two distinct known-class structural severities"):
        rc.compute_role_coverage(doctored_screen, doctored)


def test_the_read_spends_no_rollouts(report):
    assert report["rollouts_spent"] == 0


def test_the_report_binds_the_screen_it_was_derived_from(report, screen):
    """A coverage claim that does not name its screen is unauditable."""
    assert report["inputs"]["screen_outcome_case"] == screen["results"]["outcome_case"]
    assert report["inputs"]["assignment_hash"] == screen["inputs"]["assignment_hash"]
    assert (report["inputs"]["protocol_canonical_sha256"]
            == screen["protocol"]["canonical_sha256"])


def test_render_names_the_outcome_and_stays_ascii(report):
    text = rc.render(report)
    assert "ROLE-COVERAGE-BOUNDED NON-TRANSFER OUTCOME" in text
    assert "no testable structural training support" in text
    text.encode("ascii")  # the console is cp1252; non-ASCII would fail at print time


# --------------------------------------------------------------------------
# The refusal side.  One constructed state per branch, asserting the reason.
# --------------------------------------------------------------------------

def test_a_plan_mode_artifact_is_refused(screen, assignment):
    bad = copy.deepcopy(screen)
    bad["mode"] = "plan"
    with pytest.raises(rc.RoleCoverageError, match="requires an executed screen"):
        rc.compute_role_coverage(bad, assignment)


def test_a_terminal_run_is_refused(screen, assignment):
    bad = copy.deepcopy(screen)
    bad["results"]["terminal"] = "NO_ADMISSIBLE_PROBE"
    with pytest.raises(rc.RoleCoverageError, match="section 9 requires all ten ladder"):
        rc.compute_role_coverage(bad, assignment)


def test_a_short_ladder_is_refused(screen, assignment):
    bad = copy.deepcopy(screen)
    bad["results"]["ladder"] = bad["results"]["ladder"][:9]
    with pytest.raises(rc.RoleCoverageError, match="exactly ten values"):
        rc.compute_role_coverage(bad, assignment)


def test_a_repeated_ladder_value_is_refused(screen, assignment):
    bad = copy.deepcopy(screen)
    bad["results"]["ladder"][1]["remaining_ei"] = bad["results"]["ladder"][0][
        "remaining_ei"]
    with pytest.raises(rc.RoleCoverageError, match="repeats remaining_ei"):
        rc.compute_role_coverage(bad, assignment)


def test_a_severity_absent_from_the_ladder_is_refused(screen, assignment):
    """The silent-zero hazard: a split severity off the ladder must not read as 0."""
    bad_screen = copy.deepcopy(screen)
    bad = copy.deepcopy(assignment)
    bad["fault_grid_by_split"]["dev"]["structure"]["severities"] = [0.5, 0.7]
    _rebind_assignment(bad_screen, bad)
    with pytest.raises(rc.RoleCoverageError, match="is not the union of the per-split"):
        rc.compute_role_coverage(bad_screen, bad)


def test_moved_ood_severities_are_refused_by_equality_not_adopted(screen, assignment):
    """Lesson 46: a pinned value that also lives in a bound document is checked
    by EQUALITY. If the assignment moves the OOD pair, the read must stop."""
    bad_screen = copy.deepcopy(screen)
    bad = copy.deepcopy(assignment)
    for entry in bad["compound_ood_settings"]:
        if entry["label"].get("source_class") == "structure":
            entry["label"]["severity"] = 0.5
            for component in entry["components"]:
                if component["source_class"] == "structure":
                    component["severity"] = 0.5
    _rebind_assignment(bad_screen, bad)
    with pytest.raises(rc.RoleCoverageError, match="do not equal the protocol's pinned"):
        rc.compute_role_coverage(bad_screen, bad)


def test_a_missing_verdict_is_refused(screen, assignment):
    bad = copy.deepcopy(screen)
    del bad["results"]["ladder"][0]["verdict"]
    with pytest.raises(rc.RoleCoverageError, match="carries no verdict"):
        rc.compute_role_coverage(bad, assignment)


def test_a_missing_fault_grid_is_refused(screen, assignment):
    bad_screen = copy.deepcopy(screen)
    bad = copy.deepcopy(assignment)
    del bad["fault_grid_by_split"]
    _rebind_assignment(bad_screen, bad)
    with pytest.raises(rc.RoleCoverageError, match="no fault_grid_by_split"):
        rc.compute_role_coverage(bad_screen, bad)


def test_a_results_free_artifact_is_refused(screen, assignment):
    bad = copy.deepcopy(screen)
    bad["results"] = None
    with pytest.raises(rc.RoleCoverageError, match="carries no results object"):
        rc.compute_role_coverage(bad, assignment)


def test_require_raises_rather_than_asserting():
    """python -O strips assert; every decision-bearing check must survive it."""
    with pytest.raises(rc.RoleCoverageError, match="the reason"):
        rc.require(False, "the reason")
    rc.require(True, "unreachable")


def test_load_json_names_a_missing_file(tmp_path):
    with pytest.raises(rc.RoleCoverageError, match="does not exist"):
        rc.load_json(tmp_path / "absent.json", "screen result")


def test_load_json_names_a_malformed_file(tmp_path):
    bad = tmp_path / "bad.json"
    bad.write_text("{not json", encoding="utf-8")
    with pytest.raises(rc.RoleCoverageError, match="not strict JSON"):
        rc.load_json(bad, "screen result")


@pytest.mark.parametrize(
    "payload, reason",
    [
        ('{"value": NaN}', "non-finite JSON constant"),
        ('{"value": 1, "value": 2}', "duplicate JSON key"),
    ],
)
def test_load_json_refuses_non_strict_json(tmp_path, payload, reason):
    bad = tmp_path / "bad.json"
    bad.write_text(payload, encoding="utf-8")
    with pytest.raises(rc.RoleCoverageError, match=reason):
        rc.load_json(bad, "screen result")


def test_a_different_self_hashed_assignment_cannot_borrow_the_screen_binding(
        screen, assignment):
    """The split map cannot move while the output keeps the approved hash."""
    bad = copy.deepcopy(assignment)
    bad["fault_grid_by_split"]["dev"]["structure"]["severities"], bad[
        "fault_grid_by_split"]["test"]["structure"]["severities"] = (
            bad["fault_grid_by_split"]["test"]["structure"]["severities"],
            bad["fault_grid_by_split"]["dev"]["structure"]["severities"],
        )
    bad["assignment_hash"] = rc.expected_assignment_hash(bad)
    with pytest.raises(rc.RoleCoverageError, match="does not equal the assignment bound"):
        rc.compute_role_coverage(screen, bad)


def test_an_unknown_ladder_verdict_is_refused(screen, assignment):
    bad = copy.deepcopy(screen)
    bad["results"]["ladder"][0]["verdict"] = "UNRECOGNIZED"
    with pytest.raises(rc.RoleCoverageError, match="carries unknown verdict"):
        rc.compute_role_coverage(bad, assignment)


def test_the_reported_case_must_match_the_ladder(screen, assignment):
    bad = copy.deepcopy(screen)
    bad["results"]["outcome_case"] = "CASE_A"
    with pytest.raises(rc.RoleCoverageError, match="ladder verdicts imply CASE_B"):
        rc.compute_role_coverage(bad, assignment)


def test_every_required_split_must_be_present(screen, assignment):
    bad_screen = copy.deepcopy(screen)
    bad_assignment = copy.deepcopy(assignment)
    bad_assignment["fault_grid_by_split"]["pilot"]["structure"]["severities"] += (
        bad_assignment["fault_grid_by_split"]["dev"]["structure"]["severities"])
    del bad_assignment["fault_grid_by_split"]["dev"]
    _rebind_assignment(bad_screen, bad_assignment)
    with pytest.raises(rc.RoleCoverageError, match="must define exactly"):
        rc.compute_role_coverage(bad_screen, bad_assignment)


def test_derived_report_records_the_exact_screen_bytes():
    report = rc.derive_role_coverage(SCREEN, ASSIGNMENT)
    assert report["inputs"]["screen_result_raw_sha256"] == rc.raw_file_sha256(SCREEN)


# --------------------------------------------------------------------------
# A counted-flip test: the outcome must actually depend on the ladder.
# --------------------------------------------------------------------------

def test_making_a_dev_severity_testable_clears_the_outcome(screen, assignment):
    """If nothing here flips when dev becomes testable, the read is decorative."""
    flipped = copy.deepcopy(screen)
    for row in flipped["results"]["ladder"]:
        if row["remaining_ei"] == 0.5:
            row["verdict"] = "TESTABLE"
    report = rc.compute_role_coverage(flipped, assignment)
    assert report["splits"]["dev"]["count"] == 1
    assert report["outcome"]["role_coverage_bounded_non_transfer"] is False
    assert report["outcome"]["zero_count_splits"] == []
