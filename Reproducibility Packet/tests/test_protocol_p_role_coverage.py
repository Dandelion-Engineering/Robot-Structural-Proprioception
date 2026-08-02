"""Tests for the Protocol P section-9 role-coverage read.

Every test here asks the question Lesson 37 requires of a new green test: what exact
state would make this red?  The accept-side tests are driven from the real committed
artifact and assignment, so they fail if either document moves; the refusal tests each
construct the one state the guard exists to catch and assert the REASON, matching a
phrase unique to a single raise site.
"""

from __future__ import annotations

import copy
import hashlib
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


def test_derived_report_records_the_canonical_screen_digest():
    """The recomputation is INDEPENDENT of the module under test.

    The superseded form of this test asserted the report field against
    ``rc.raw_file_sha256(SCREEN)`` -- the same module, the same file, so both sides
    moved together and no choice of helper could make it red.  Here the expected value
    is built from the bytes with the standard library alone.
    """
    expected = hashlib.sha256(
        SCREEN.read_bytes().lstrip(b"\xef\xbb\xbf").replace(b"\r\n", b"\n")
    ).hexdigest()
    report = rc.derive_role_coverage(SCREEN, ASSIGNMENT)
    assert report["inputs"]["screen_result_canonical_sha256"] == expected


def test_the_recorded_screen_digest_does_not_depend_on_the_checkout(tmp_path):
    """A CRLF checkout and an LF checkout must derive the same artifact.

    This is the property the raw helper did not have: on this repository the tracked
    screen result renders CRLF in the working tree, so a raw digest identifies one
    checkout rather than the document, and an outside reader on an LF checkout would
    regenerate a different role_coverage.json.
    """
    body = SCREEN.read_bytes().replace(b"\r\n", b"\n")
    lf_copy = tmp_path / "screen_lf.json"
    crlf_copy = tmp_path / "screen_crlf.json"
    lf_copy.write_bytes(body)
    crlf_copy.write_bytes(body.replace(b"\n", b"\r\n"))
    assert lf_copy.read_bytes() != crlf_copy.read_bytes()

    lf_report = rc.derive_role_coverage(lf_copy, ASSIGNMENT)
    crlf_report = rc.derive_role_coverage(crlf_copy, ASSIGNMENT)
    assert lf_report == crlf_report
    assert (lf_report["inputs"]["screen_result_canonical_sha256"]
            == rc.derive_role_coverage(SCREEN, ASSIGNMENT)[
                "inputs"]["screen_result_canonical_sha256"])


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


# --------------------------------------------------------------------------
# Session 59: the guards the reviewer added that no test made load-bearing.
#
# A 23-case mutation sweep over the reviewer-edited analyzer left thirteen
# survivors.  Twelve were real -- each guard below could be deleted with the
# whole focused suite still green, because no test constructed the one state it
# exists to refuse.  The thirteenth (reporting the screen-carried digests instead
# of the pinned constants) is forced by arithmetic once the pins are checked for
# equality, and is deliberately NOT tested here.
#
# Each test asserts a REASON phrase unique to a single raise site (Lesson 59).
# --------------------------------------------------------------------------

def test_a_stale_assignment_self_hash_is_refused(screen, assignment):
    """Every other branch test reseals the assignment, so nothing reached this.

    A supplied assignment whose recorded self-hash does not match its own content
    is a document somebody edited without re-deriving the hash.  It must not be
    read as the bound assignment merely because the screen happens to name that
    same stale value.
    """
    bad = copy.deepcopy(assignment)
    bad["fault_grid_by_split"]["dev"]["structure"]["severities"] = [0.35, 0.65]
    bad["fault_grid_by_split"]["test"]["structure"]["severities"] = [0.5, 0.75]
    with pytest.raises(rc.RoleCoverageError, match="self-hash is invalid"):
        rc.compute_role_coverage(copy.deepcopy(screen), bad)


def test_a_screen_carrying_the_wrong_assignment_canonical_digest_is_refused(
        screen, assignment):
    """The screen's recorded canonical digest is pinned, not merely reported."""
    bad_screen = copy.deepcopy(screen)
    bad_screen["inputs"]["assignment_canonical_sha256"] = "0" * 64
    with pytest.raises(rc.RoleCoverageError,
                       match="assignment canonical digest does not equal"):
        rc.compute_role_coverage(bad_screen, copy.deepcopy(assignment))


def test_a_screen_carrying_the_wrong_input_protocol_digest_is_refused(
        screen, assignment):
    """The two protocol-digest call sites are mutually redundant, so neither is
    testable by deletion; they are testable by CONTENT, one field at a time,
    which is what this test and the next one do (Lesson 63)."""
    bad_screen = copy.deepcopy(screen)
    bad_screen["inputs"]["protocol_spec_sha256"] = "0" * 64
    with pytest.raises(rc.RoleCoverageError,
                       match="screen input protocol digest does not equal"):
        rc.compute_role_coverage(bad_screen, copy.deepcopy(assignment))


def test_a_screen_carrying_the_wrong_protocol_block_digest_is_refused(
        screen, assignment):
    bad_screen = copy.deepcopy(screen)
    bad_screen["protocol"]["canonical_sha256"] = "0" * 64
    with pytest.raises(rc.RoleCoverageError,
                       match="screen protocol digest does not equal"):
        rc.compute_role_coverage(bad_screen, copy.deepcopy(assignment))


def test_an_all_testable_ladder_must_be_reported_as_case_a(screen, assignment):
    """The independent case re-derivation was only ever exercised at CASE_B.

    Inverting the CASE_A and CASE_C arms of the rule survived the sweep, because
    the committed ladder is a proper subset and the middle arm is unchanged by the
    inversion.  This test and the next one pin the ends.
    """
    flipped = copy.deepcopy(screen)
    for row in flipped["results"]["ladder"]:
        row["verdict"] = "TESTABLE"
    flipped["results"]["outcome_case"] = "CASE_A"
    report = rc.compute_role_coverage(flipped, copy.deepcopy(assignment))
    assert report["splits"]["dev"]["count"] == 2

    flipped["results"]["outcome_case"] = "CASE_C"
    with pytest.raises(rc.RoleCoverageError, match="imply CASE_A"):
        rc.compute_role_coverage(flipped, copy.deepcopy(assignment))


def test_a_ladder_with_nothing_testable_must_be_reported_as_case_c(
        screen, assignment):
    flipped = copy.deepcopy(screen)
    for row in flipped["results"]["ladder"]:
        row["verdict"] = "SUB_THRESHOLD"
    flipped["results"]["outcome_case"] = "CASE_C"
    report = rc.compute_role_coverage(flipped, copy.deepcopy(assignment))
    assert report["outcome"]["zero_count_splits"] == ["dev", "val", "test"]

    flipped["results"]["outcome_case"] = "CASE_A"
    with pytest.raises(rc.RoleCoverageError, match="imply CASE_C"):
        rc.compute_role_coverage(flipped, copy.deepcopy(assignment))


def test_moving_a_severity_between_splits_is_refused(screen, assignment):
    """The ten-value union survives this, so only the per-split count catches it.

    This is the state that separates 'exactly two known-class severities' from
    'at least one': dev keeps one, pilot takes three, and the ladder is untouched.
    """
    bad_screen = copy.deepcopy(screen)
    bad = copy.deepcopy(assignment)
    grid = bad["fault_grid_by_split"]
    grid["dev"]["structure"]["severities"] = [0.75]
    grid["pilot"]["structure"]["severities"] = sorted(
        set(grid["pilot"]["structure"]["severities"]) | {0.5})
    _rebind_assignment(bad_screen, bad)
    with pytest.raises(rc.RoleCoverageError, match="exactly two distinct known-class"):
        rc.compute_role_coverage(bad_screen, bad)


def test_a_repeated_structural_severity_in_one_split_is_refused(screen, assignment):
    """A duplicate would be counted twice and inflate that split's coverage."""
    bad_screen = copy.deepcopy(screen)
    bad = copy.deepcopy(assignment)
    bad["fault_grid_by_split"]["val"]["structure"]["severities"] = [0.4, 0.4, 0.9]
    _rebind_assignment(bad_screen, bad)
    with pytest.raises(rc.RoleCoverageError, match="repeats a structural severity"):
        rc.compute_role_coverage(bad_screen, bad)


def test_a_non_finite_ladder_value_is_refused(screen, assignment):
    """Unreachable through load_json, which rejects the constants; reachable here."""
    bad_screen = copy.deepcopy(screen)
    bad_screen["results"]["ladder"][0]["remaining_ei"] = float("nan")
    with pytest.raises(rc.RoleCoverageError, match="non-finite remaining_ei"):
        rc.compute_role_coverage(bad_screen, copy.deepcopy(assignment))


def test_a_non_finite_structural_severity_is_refused(assignment):
    """Called directly, because the whole-document path can no longer reach it.

    ``compute_role_coverage`` now derives the assignment's self-hash first, and that
    derivation refuses to serialize a non-finite value -- so a document carrying one
    raises ``Gate3AssignmentError`` from the binding step and never reaches this
    guard.  Measured, not assumed; the companion test below pins that behaviour.
    The guard is kept because this function is public and the failure it names is
    the accurate one for a caller that supplies a parsed grid.
    """
    bad = copy.deepcopy(assignment)
    bad["fault_grid_by_split"]["dev"]["structure"]["severities"] = [0.5, float("inf")]
    with pytest.raises(rc.RoleCoverageError, match="non-finite structural severity"):
        rc.structural_severities_by_split(bad)


def test_a_non_finite_document_fails_loud_at_the_binding_step(screen, assignment):
    """It still fails loudly -- but as a foreign exception type, so say so."""
    bad = copy.deepcopy(assignment)
    bad["fault_grid_by_split"]["dev"]["structure"]["severities"] = [0.5, float("inf")]
    with pytest.raises(Exception, match="not canonical-JSON serializable"):
        rc.compute_role_coverage(copy.deepcopy(screen), bad)


def test_a_non_object_ladder_row_is_refused_rather_than_crashing(screen, assignment):
    """Without the guard this raises AttributeError, not a named refusal."""
    bad_screen = copy.deepcopy(screen)
    bad_screen["results"]["ladder"][3] = [0.5, "TESTABLE"]
    with pytest.raises(rc.RoleCoverageError, match="every ladder row must be an object"):
        rc.compute_role_coverage(bad_screen, copy.deepcopy(assignment))


def test_a_reformatted_assignment_file_is_refused_at_the_file_digest(tmp_path):
    """Re-indenting the assignment leaves assignment_hash identical.

    ``assignment_hash`` is taken over canonical JSON, so whitespace does not move
    it and every in-memory binding check still passes.  Only the file-level
    canonical digest distinguishes the tracked document from a re-rendered copy,
    which is what makes this the one state that reaches that check.
    """
    document = json.loads(ASSIGNMENT.read_bytes())
    reformatted = tmp_path / "assignment_reformatted.json"
    reformatted.write_text(json.dumps(document, indent=4, ensure_ascii=False),
                           encoding="utf-8", newline="\n")
    assert (json.loads(reformatted.read_bytes())["assignment_hash"]
            == document["assignment_hash"])
    with pytest.raises(rc.RoleCoverageError,
                       match="assignment file does not equal the approved canonical"):
        rc.derive_role_coverage(SCREEN, reformatted)


def test_the_tracked_protocol_file_digest_is_checked_at_derive_time(monkeypatch):
    """Wire-test: the tracked protocol file must not be edited to test its check.

    Moving the pinned constant instead does not work -- the same constant is what
    the screen-carried digests are compared against, so the run would refuse
    several steps earlier and the test would pass for the wrong reason.  Measured:
    it fails with 'the screen input protocol digest does not equal ...'.  So the
    digest of that one path is moved rather than the pin, which leaves every
    earlier check reading the real values.
    """
    real = rc.canonical_text_sha256

    def only_the_protocol_file_differs(path):
        if Path(path).name == rc.PROTOCOL_FILENAME:
            return "0" * 64
        return real(path)

    monkeypatch.setattr(rc, "canonical_text_sha256", only_the_protocol_file_differs)
    with pytest.raises(rc.RoleCoverageError,
                       match="tracked Protocol P file does not equal"):
        rc.derive_role_coverage(SCREEN, ASSIGNMENT)
