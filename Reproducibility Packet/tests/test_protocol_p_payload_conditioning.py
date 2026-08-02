"""Tests for the post-hoc payload-conditioning read over the executed screen.

Every test here asks the question Lesson 37 requires of a new green test: what exact
state would make this red?  The accept-side tests are driven from the real committed
artifact and assignment, so they fail if either document moves; the refusal tests each
construct the one state the guard exists to catch and assert the REASON, matching a
phrase unique to a single raise site.

Session 59's lesson governs the shape of this file: a guard whose refused state is only
ever produced in a scratch process is not covered.  Each guard below is reached from a
constructed document, and the two guards whose real-data value sits at one end of their
input space (the crossing-bracket branch and the unscreened-mass branch) are exercised
from both ends.
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
SCRIPT = SCRIPTS_ROOT / "analyze_protocol_p_payload_conditioning.py"
SCREEN = PACKET_ROOT / "results" / "protocol_p" / "stage_abc_screen.json"
ASSIGNMENT = PACKET_ROOT / "config" / "proposed-gate3-assignment-v0.1.json"


def _load_module():
    """Import the analysis script as a module without installing it."""
    spec = importlib.util.spec_from_file_location(
        "protocol_p_payload_conditioning", SCRIPT)
    module = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = module
    spec.loader.exec_module(module)
    return module


pc = _load_module()


@pytest.fixture(scope="module")
def screen():
    return json.loads(SCREEN.read_bytes())


@pytest.fixture(scope="module")
def assignment():
    return json.loads(ASSIGNMENT.read_bytes())


@pytest.fixture(scope="module")
def report(screen, assignment):
    return pc.compute_payload_conditioning(screen, assignment)


@pytest.fixture
def mutable(screen, assignment):
    """A deep copy of both real documents, safe to mutate in one test."""
    return copy.deepcopy(screen), copy.deepcopy(assignment)


def _ledger_entry(screen_doc, index=0):
    """Return one ledger entry's decoded canonical payload and a writer for it."""
    entry = screen_doc["results"]["physical_ledger"][index]
    payload = json.loads(entry["rollout_canonical"])

    def write(new_payload):
        entry["rollout_canonical"] = json.dumps(new_payload)

    return entry, payload, write


# --------------------------------------------------------------------------
# The accept side, against the real committed documents.
# --------------------------------------------------------------------------

def test_the_four_screened_cells_resolve_to_the_protocol_pinned_payloads(report):
    """Section 8 pins 0.000/0.000/0.050/0.050 kg for cells 4/5/6/7."""
    masses = {cell: report["cells"][cell]["distal_payload_mass_kg"]
              for cell in ("4", "5", "6", "7")}
    assert masses == {"4": 0.0, "5": 0.0, "6": 0.05, "7": 0.05}


def test_each_cell_resolves_through_the_reservation_the_screen_recorded(report):
    """The join runs through the ledger's own reservation, not a rebuilt cell table."""
    assert [report["cells"][c]["scenario_spec_id"] for c in ("4", "5", "6", "7")] == [
        "scenario_dev_t01_f000_r00", "scenario_dev_t01_f000_r01",
        "scenario_dev_t01_f000_r02", "scenario_dev_t01_f000_r03"]
    assert {report["cells"][c]["split"] for c in ("4", "5", "6", "7")} == {"dev"}


def test_the_two_payload_levels_are_balanced_two_cells_each(report):
    assert report["payload_levels"] == [
        {"distal_payload_mass_kg": 0.0, "cells": [4, 5]},
        {"distal_payload_mass_kg": 0.05, "cells": [6, 7]}]


def test_fifty_grams_roughly_halves_the_structural_distance_at_every_rung(report):
    """The measured contrast: ratio in [0.48, 0.54] across all ten ladder values."""
    ratios = [row["attenuation_ratio"]
              for row in report["attenuation"]["by_ladder_value"]]
    assert len(ratios) == 10
    assert all(0.48 < ratio < 0.54 for ratio in ratios)
    assert report["attenuation"]["ratio_min"] == pytest.approx(0.4867, abs=5e-4)
    assert report["attenuation"]["ratio_max"] == pytest.approx(0.5366, abs=5e-4)


def test_the_attenuation_is_larger_than_the_spread_within_either_level(report):
    """Payload moves d by ~2x; environment and contact move it by a few percent.

    This is what licenses attributing the contrast to payload rather than to the other
    two context factors, which vary inside each level rather than across them.
    """
    for row in report["attenuation"]["by_ladder_value"]:
        assert row["within_level_spread_light"] < 0.05
        assert row["within_level_spread_heavy"] < 0.15
        assert abs(1.0 - row["attenuation_ratio"]) > row["within_level_spread_light"]


def test_the_operative_null_does_not_scale_with_payload(report):
    """The control: if the null halved too, the margin would be unchanged."""
    light, heavy = report["null_by_payload_level"]
    assert light["distal_payload_mass_kg"] == 0.0
    assert heavy["distal_payload_mass_kg"] == 0.05
    assert 0.8 < heavy["mean_q95_c"] / light["mean_q95_c"] < 1.2


def test_the_severity_boundary_moves_with_payload(report):
    """Zero payload brackets the crossing at 0.60/0.65; fifty grams at 0.45/0.50."""
    boundaries = report["severity_boundary_by_cell"]
    for cell in ("4", "5"):
        bracket = boundaries[cell]["crossing_bracket"]
        assert bracket["last_positive_remaining_ei"] == 0.6
        assert bracket["first_negative_remaining_ei"] == 0.65
    for cell in ("6", "7"):
        bracket = boundaries[cell]["crossing_bracket"]
        assert bracket["last_positive_remaining_ei"] == 0.45
        assert bracket["first_negative_remaining_ei"] == 0.5


def test_the_binding_cell_clears_by_two_percent_of_its_threshold(report):
    """Cell 7 at remaining EI 0.45 is what makes the whole rung TESTABLE."""
    bracket = report["severity_boundary_by_cell"]["7"]["crossing_bracket"]
    assert bracket["last_positive_margin"] == pytest.approx(0.025561, abs=1e-6)


def test_the_interpolation_is_labelled_as_an_illustration(report):
    for cell in ("4", "5", "6", "7"):
        entry = report["severity_boundary_by_cell"][cell]
        assert "illustration only" in entry["interpolation_authority"]
        assert entry["crossing_bracket"]["last_positive_remaining_ei"] <= (
            entry["linear_interpolation"])
        assert entry["linear_interpolation"] <= (
            entry["crossing_bracket"]["first_negative_remaining_ei"])


def test_pilot_val_and_test_reserve_payload_masses_the_screen_never_ran(report):
    coverage = report["confirmatory_payload_coverage"]
    assert coverage["screened_payload_masses_kg"] == [0.0, 0.05]
    assert coverage["splits_reserving_unscreened_masses"] == {
        "pilot": [0.075], "val": [0.1, 0.125], "test": [0.15, 0.2]}
    assert "dev" not in coverage["splits_reserving_unscreened_masses"]


def test_the_read_costs_no_rollout_and_claims_no_authority(report):
    assert report["rollouts_spent"] == 0
    assert report["authority"].startswith("NOT PRE-REGISTERED")
    assert "classifies nothing" in report["authority"]
    assert "no functional form" in (
        report["attenuation"]["extrapolation_authority"].lower()
        .replace("no functional", "no functional"))


def test_the_read_never_recomputes_a_verdict(report, screen):
    """Every reported verdict is the one the screen recorded, value for value."""
    recorded = {row["remaining_ei"]: row["verdict"]
                for row in screen["results"]["ladder"]}
    for row in report["attenuation"]["by_ladder_value"]:
        assert row["verdict"] == recorded[row["remaining_ei"]]


# --------------------------------------------------------------------------
# Binding: the screen and the assignment must be the approved pair.
# --------------------------------------------------------------------------

def test_a_screen_that_is_not_an_object_is_refused(assignment):
    with pytest.raises(pc.PayloadConditioningError, match="must be a JSON object"):
        pc.compute_payload_conditioning([], assignment)


def test_an_assignment_that_is_not_an_object_is_refused(screen):
    with pytest.raises(pc.PayloadConditioningError, match="assignment must be a JSON"):
        pc.compute_payload_conditioning(screen, [])


def test_a_screen_without_an_inputs_object_is_refused(mutable):
    screen_doc, assignment_doc = mutable
    del screen_doc["inputs"]
    with pytest.raises(pc.PayloadConditioningError, match="carries no inputs object"):
        pc.compute_payload_conditioning(screen_doc, assignment_doc)


def test_a_screen_without_a_protocol_object_is_refused(mutable):
    screen_doc, assignment_doc = mutable
    del screen_doc["protocol"]
    with pytest.raises(pc.PayloadConditioningError, match="carries no protocol object"):
        pc.compute_payload_conditioning(screen_doc, assignment_doc)


def test_a_screen_input_protocol_digest_that_moved_is_refused(mutable):
    screen_doc, assignment_doc = mutable
    screen_doc["inputs"]["protocol_spec_sha256"] = "0" * 64
    with pytest.raises(pc.PayloadConditioningError,
                       match="screen input protocol digest"):
        pc.compute_payload_conditioning(screen_doc, assignment_doc)


def test_a_screen_protocol_block_digest_that_moved_is_refused(mutable):
    """The second protocol digest lives in a different object and needs its own case."""
    screen_doc, assignment_doc = mutable
    screen_doc["protocol"]["canonical_sha256"] = "0" * 64
    with pytest.raises(pc.PayloadConditioningError,
                       match="screen protocol digest does not equal"):
        pc.compute_payload_conditioning(screen_doc, assignment_doc)


def test_a_screen_assignment_canonical_digest_that_moved_is_refused(mutable):
    screen_doc, assignment_doc = mutable
    screen_doc["inputs"]["assignment_canonical_sha256"] = "0" * 64
    with pytest.raises(pc.PayloadConditioningError,
                       match="assignment canonical digest"):
        pc.compute_payload_conditioning(screen_doc, assignment_doc)


def test_an_assignment_that_is_not_the_bound_one_is_refused(mutable):
    screen_doc, assignment_doc = mutable
    assignment_doc["assignment_hash"] = "dev-" + "0" * 64
    with pytest.raises(pc.PayloadConditioningError,
                       match="does not equal the assignment bound by the screen"):
        pc.compute_payload_conditioning(screen_doc, assignment_doc)


# --------------------------------------------------------------------------
# The screen has to be an executed, non-terminal run.
# --------------------------------------------------------------------------

def test_a_plan_mode_artifact_is_refused(mutable):
    screen_doc, assignment_doc = mutable
    screen_doc["mode"] = "plan"
    with pytest.raises(pc.PayloadConditioningError, match="requires an executed screen"):
        pc.compute_payload_conditioning(screen_doc, assignment_doc)


def test_an_artifact_without_results_is_refused(mutable):
    screen_doc, assignment_doc = mutable
    del screen_doc["results"]
    with pytest.raises(pc.PayloadConditioningError, match="it was not executed"):
        pc.compute_payload_conditioning(screen_doc, assignment_doc)


def test_a_terminal_run_is_refused(mutable):
    screen_doc, assignment_doc = mutable
    screen_doc["results"]["terminal"] = "NO_ADMISSIBLE_PROBE"
    with pytest.raises(pc.PayloadConditioningError,
                       match="no complete\n?.*per-cell ladder|per-cell ladder"):
        pc.compute_payload_conditioning(screen_doc, assignment_doc)


# --------------------------------------------------------------------------
# The cell -> reservation join, read out of the ledger.
# --------------------------------------------------------------------------

def test_a_screen_without_a_physical_ledger_is_refused(mutable):
    screen_doc, assignment_doc = mutable
    screen_doc["results"]["physical_ledger"] = []
    with pytest.raises(pc.PayloadConditioningError,
                       match="no physical_ledger entries"):
        pc.compute_payload_conditioning(screen_doc, assignment_doc)


def test_a_ledger_entry_that_is_not_an_object_is_refused(mutable):
    screen_doc, assignment_doc = mutable
    screen_doc["results"]["physical_ledger"][0] = "not an entry"
    with pytest.raises(pc.PayloadConditioningError, match=r"\[0\] must be an object"):
        pc.compute_payload_conditioning(screen_doc, assignment_doc)


def test_a_ledger_entry_with_a_non_integer_cell_is_refused(mutable):
    screen_doc, assignment_doc = mutable
    screen_doc["results"]["physical_ledger"][0]["cell"] = "4"
    with pytest.raises(pc.PayloadConditioningError, match="non-integer cell"):
        pc.compute_payload_conditioning(screen_doc, assignment_doc)


def test_a_boolean_cell_is_refused_rather_than_read_as_one(mutable):
    """``True == 1`` in Python; the isinstance check has to exclude bool explicitly."""
    screen_doc, assignment_doc = mutable
    screen_doc["results"]["physical_ledger"][0]["cell"] = True
    with pytest.raises(pc.PayloadConditioningError, match="non-integer cell"):
        pc.compute_payload_conditioning(screen_doc, assignment_doc)


def test_a_ledger_entry_without_a_canonical_payload_is_refused(mutable):
    screen_doc, assignment_doc = mutable
    screen_doc["results"]["physical_ledger"][0]["rollout_canonical"] = ""
    with pytest.raises(pc.PayloadConditioningError,
                       match="carries no rollout_canonical"):
        pc.compute_payload_conditioning(screen_doc, assignment_doc)


def test_a_canonical_payload_that_is_not_json_is_refused(mutable):
    screen_doc, assignment_doc = mutable
    screen_doc["results"]["physical_ledger"][0]["rollout_canonical"] = "{not json"
    with pytest.raises(pc.PayloadConditioningError, match="is not JSON"):
        pc.compute_payload_conditioning(screen_doc, assignment_doc)


def test_a_canonical_payload_that_is_not_an_object_is_refused(mutable):
    screen_doc, assignment_doc = mutable
    screen_doc["results"]["physical_ledger"][0]["rollout_canonical"] = "[1, 2]"
    with pytest.raises(pc.PayloadConditioningError, match="is not an object"):
        pc.compute_payload_conditioning(screen_doc, assignment_doc)


def test_a_canonical_payload_without_a_reservation_is_refused(mutable):
    screen_doc, assignment_doc = mutable
    _, payload, write = _ledger_entry(screen_doc)
    del payload["reservation"]
    write(payload)
    with pytest.raises(pc.PayloadConditioningError,
                       match="carries no reservation object"):
        pc.compute_payload_conditioning(screen_doc, assignment_doc)


def test_a_reservation_without_a_scenario_id_is_refused(mutable):
    screen_doc, assignment_doc = mutable
    _, payload, write = _ledger_entry(screen_doc)
    payload["reservation"]["scenario_spec_id"] = ""
    write(payload)
    with pytest.raises(pc.PayloadConditioningError,
                       match="carries no scenario_spec_id"):
        pc.compute_payload_conditioning(screen_doc, assignment_doc)


def test_a_ledger_that_does_not_cover_all_four_cells_is_refused(mutable):
    screen_doc, assignment_doc = mutable
    screen_doc["results"]["physical_ledger"] = [
        entry for entry in screen_doc["results"]["physical_ledger"]
        if entry["cell"] != 7]
    with pytest.raises(pc.PayloadConditioningError, match="must cover exactly cells"):
        pc.compute_payload_conditioning(screen_doc, assignment_doc)


def test_a_cell_citing_two_reservations_is_refused_not_resolved(mutable):
    """A majority vote over ledger entries would hide exactly this state."""
    screen_doc, assignment_doc = mutable
    _, payload, write = _ledger_entry(screen_doc)
    payload["reservation"]["scenario_spec_id"] = "scenario_dev_t01_f000_r01"
    write(payload)
    with pytest.raises(pc.PayloadConditioningError,
                       match="cites more than one reservation"):
        pc.compute_payload_conditioning(screen_doc, assignment_doc)


def test_a_reservation_the_assignment_does_not_expand_is_refused(mutable):
    screen_doc, assignment_doc = mutable
    for entry in screen_doc["results"]["physical_ledger"]:
        if entry["cell"] != 4:
            continue
        payload = json.loads(entry["rollout_canonical"])
        payload["reservation"]["scenario_spec_id"] = "scenario_dev_t01_f000_r99"
        entry["rollout_canonical"] = json.dumps(payload)
    with pytest.raises(pc.PayloadConditioningError,
                       match="which the assignment does not expand"):
        pc.compute_payload_conditioning(screen_doc, assignment_doc)


# --------------------------------------------------------------------------
# The payload profiles, and the equality check against the protocol's prose pin.
# --------------------------------------------------------------------------

def test_an_assignment_without_payload_profiles_is_refused(mutable):
    screen_doc, assignment_doc = mutable
    assignment_doc["context_profiles"]["payloads"] = []
    with pytest.raises(pc.PayloadConditioningError,
                       match="no context_profiles.payloads list"):
        pc.compute_payload_conditioning(screen_doc, assignment_doc)


def test_a_payload_profile_that_is_not_an_object_is_refused(mutable):
    screen_doc, assignment_doc = mutable
    assignment_doc["context_profiles"]["payloads"][0] = "payload_dev_nominal"
    with pytest.raises(pc.PayloadConditioningError,
                       match=r"payloads\[0\] must be an object"):
        pc.compute_payload_conditioning(screen_doc, assignment_doc)


def test_a_payload_profile_without_an_id_is_refused(mutable):
    screen_doc, assignment_doc = mutable
    assignment_doc["context_profiles"]["payloads"][0]["id"] = ""
    with pytest.raises(pc.PayloadConditioningError, match="carries no id"):
        pc.compute_payload_conditioning(screen_doc, assignment_doc)


def test_a_repeated_payload_profile_id_is_refused(mutable):
    screen_doc, assignment_doc = mutable
    payloads = assignment_doc["context_profiles"]["payloads"]
    payloads[1]["id"] = payloads[0]["id"]
    with pytest.raises(pc.PayloadConditioningError, match="repeats the id"):
        pc.compute_payload_conditioning(screen_doc, assignment_doc)


def test_a_non_finite_payload_mass_is_refused(mutable):
    screen_doc, assignment_doc = mutable
    assignment_doc["context_profiles"]["payloads"][0][
        "distal_payload_mass_kg"] = float("inf")
    with pytest.raises(pc.PayloadConditioningError, match="must be finite"):
        pc.compute_payload_conditioning(screen_doc, assignment_doc)


def test_a_boolean_payload_mass_is_refused(mutable):
    screen_doc, assignment_doc = mutable
    assignment_doc["context_profiles"]["payloads"][0][
        "distal_payload_mass_kg"] = True
    with pytest.raises(pc.PayloadConditioningError, match="must be a number"):
        pc.compute_payload_conditioning(screen_doc, assignment_doc)


def test_a_mass_that_disagrees_with_the_protocols_pin_is_refused(mutable):
    """The two sources are the assignment and section 8's prose; neither adopts."""
    screen_doc, assignment_doc = mutable
    for profile in assignment_doc["context_profiles"]["payloads"]:
        if profile["id"] == "payload_dev_nominal":
            profile["distal_payload_mass_kg"] = 0.02
    with pytest.raises(pc.PayloadConditioningError,
                       match="Protocol P section 8 pins"):
        pc.compute_payload_conditioning(screen_doc, assignment_doc)


def test_a_tiny_mass_perturbation_is_still_refused(mutable):
    """The tolerance is exact enough that a float which renders the same is caught."""
    screen_doc, assignment_doc = mutable
    for profile in assignment_doc["context_profiles"]["payloads"]:
        if profile["id"] == "payload_dev_0p050kg":
            profile["distal_payload_mass_kg"] = 0.05 + 1e-9
    with pytest.raises(pc.PayloadConditioningError,
                       match="Protocol P section 8 pins"):
        pc.compute_payload_conditioning(screen_doc, assignment_doc)


def test_a_payload_profile_naming_an_unknown_split_is_refused(assignment):
    """Reached by calling ``payload_masses_by_split`` directly.

    On the whole-document path ``require_binary_context_factors`` fires first with its
    own message, so this guard is a direct-call defence and not coverage of the split
    contract.  The two messages are deliberately different so this assertion cannot
    pass on the other raise site.
    """
    document = copy.deepcopy(assignment)
    document["context_profiles"]["payloads"][0]["split"] = "holdout"
    with pytest.raises(pc.PayloadConditioningError,
                       match="is assigned to unknown split"):
        pc.payload_masses_by_split(document)


def test_a_split_reserving_no_payload_profile_is_refused(assignment):
    """Also a direct-call defence; the binary-factor check subsumes it on a document."""
    document = copy.deepcopy(assignment)
    document["context_profiles"]["payloads"] = [
        profile for profile in document["context_profiles"]["payloads"]
        if profile["split"] != "test"]
    with pytest.raises(pc.PayloadConditioningError,
                       match="reserves no distal payload profile"):
        pc.payload_masses_by_split(document)


def test_the_two_split_guards_have_messages_distinct_from_the_binary_check(assignment):
    """A duplicated message would let either test certify the wrong raise site."""
    document = copy.deepcopy(assignment)
    document["context_profiles"]["payloads"][0]["split"] = "holdout"
    with pytest.raises(pc.PayloadConditioningError) as direct:
        pc.payload_masses_by_split(document)
    with pytest.raises(pc.PayloadConditioningError) as via_factors:
        pc.require_binary_context_factors(document)
    assert str(direct.value) != str(via_factors.value)
    assert "is assigned to unknown split" not in str(via_factors.value)


# --------------------------------------------------------------------------
# The ladder, and the two-level contrast it is read through.
# --------------------------------------------------------------------------

def test_a_ladder_of_the_wrong_length_is_refused(mutable):
    screen_doc, assignment_doc = mutable
    screen_doc["results"]["ladder"] = screen_doc["results"]["ladder"][:9]
    with pytest.raises(pc.PayloadConditioningError, match="exactly ten values"):
        pc.compute_payload_conditioning(screen_doc, assignment_doc)


def test_a_ladder_row_that_is_not_an_object_is_refused(mutable):
    screen_doc, assignment_doc = mutable
    screen_doc["results"]["ladder"][0] = 0.35
    with pytest.raises(pc.PayloadConditioningError, match="ladder row must be an object"):
        pc.compute_payload_conditioning(screen_doc, assignment_doc)


def test_a_repeated_remaining_ei_is_refused(mutable):
    screen_doc, assignment_doc = mutable
    screen_doc["results"]["ladder"][1]["remaining_ei"] = (
        screen_doc["results"]["ladder"][0]["remaining_ei"])
    with pytest.raises(pc.PayloadConditioningError, match="ladder repeats remaining_ei"):
        pc.compute_payload_conditioning(screen_doc, assignment_doc)


def test_an_unknown_ladder_verdict_is_refused(mutable):
    screen_doc, assignment_doc = mutable
    screen_doc["results"]["ladder"][0]["verdict"] = "PROBABLY"
    with pytest.raises(pc.PayloadConditioningError, match="unknown verdict"):
        pc.compute_payload_conditioning(screen_doc, assignment_doc)


def test_a_ladder_row_without_per_cell_entries_is_refused(mutable):
    screen_doc, assignment_doc = mutable
    del screen_doc["results"]["ladder"][0]["per_cell"]
    with pytest.raises(pc.PayloadConditioningError, match="carries no per_cell object"):
        pc.compute_payload_conditioning(screen_doc, assignment_doc)


def test_a_ladder_row_missing_a_cell_is_refused(mutable):
    screen_doc, assignment_doc = mutable
    del screen_doc["results"]["ladder"][0]["per_cell"]["7"]
    with pytest.raises(pc.PayloadConditioningError, match="must carry exactly cells"):
        pc.compute_payload_conditioning(screen_doc, assignment_doc)


def test_a_per_cell_entry_that_is_not_an_object_is_refused(mutable):
    screen_doc, assignment_doc = mutable
    screen_doc["results"]["ladder"][0]["per_cell"]["7"] = 1.23
    with pytest.raises(pc.PayloadConditioningError, match="cell 7 must be an object"):
        pc.compute_payload_conditioning(screen_doc, assignment_doc)


def test_a_non_finite_distance_is_refused(mutable):
    screen_doc, assignment_doc = mutable
    screen_doc["results"]["ladder"][0]["per_cell"]["4"]["d"] = None
    with pytest.raises(pc.PayloadConditioningError, match="the distance at remaining_ei"):
        pc.compute_payload_conditioning(screen_doc, assignment_doc)


def test_a_non_finite_margin_is_refused(mutable):
    screen_doc, assignment_doc = mutable
    screen_doc["results"]["ladder"][0]["per_cell"]["4"]["margin"] = None
    with pytest.raises(pc.PayloadConditioningError, match="the margin at remaining_ei"):
        pc.compute_payload_conditioning(screen_doc, assignment_doc)


def test_a_non_finite_threshold_is_refused(mutable):
    screen_doc, assignment_doc = mutable
    screen_doc["results"]["ladder"][0]["per_cell"]["4"]["operative_threshold"] = None
    with pytest.raises(pc.PayloadConditioningError, match="the threshold at remaining_ei"):
        pc.compute_payload_conditioning(screen_doc, assignment_doc)


def _contexts(masses, environments=None, contacts=None):
    """Build a four-cell context map for the direct ``payload_levels`` tests."""
    environments = environments or {4: "e0", 5: "e1", 6: "e0", 7: "e1"}
    contacts = contacts or {4: "c1", 5: "c0", 6: "c0", 7: "c1"}
    return {cell: {"distal_payload_mass_kg": masses[cell],
                   "env_profile_id": environments[cell],
                   "contact_profile_id": contacts[cell]}
            for cell in (4, 5, 6, 7)}


def test_a_single_payload_level_is_refused():
    """With one level there is no contrast; the ratio would be a tautological 1.0.

    Reached by calling ``payload_levels`` directly, and deliberately so: on the
    whole-document path ``cell_contexts`` has already required every cell's mass to
    equal the section-8 pin, so a one-level document dies at that equality check with a
    different reason and this guard is never reached.  Measured -- the whole-document
    attempt reports "Protocol P section 8 pins".  Presenting that as coverage of this
    guard would be the Session-58 mistake of testing a property of the fixture.
    """
    with pytest.raises(pc.PayloadConditioningError,
                       match="exactly two screened payload levels"):
        pc.payload_levels(_contexts({4: 0.0, 5: 0.0, 6: 0.0, 7: 0.0}))


def test_an_unbalanced_two_level_contrast_is_refused():
    """Three cells at one mass and one at the other: the means are not comparable.

    Also forced by the section-8 equality check on the whole-document path, for the
    same reason as the test above.
    """
    with pytest.raises(pc.PayloadConditioningError,
                       match="same number of cells"):
        pc.payload_levels(_contexts({4: 0.0, 5: 0.05, 6: 0.05, 7: 0.05}))


def test_the_two_unreachable_guards_are_forced_by_the_section_8_pin():
    """Pin the reason the two guards above cannot be reached from a document.

    If a future protocol version changed the cell table to something other than two
    masses over two cells each, this test goes red and the guards become live -- which
    is the state in which they would start earning their place.
    """
    pinned = pc.PROTOCOL_CELL_PAYLOAD_KG
    assert sorted(pinned) == [4, 5, 6, 7]
    levels = {}
    for cell, mass in pinned.items():
        levels.setdefault(mass, []).append(cell)
    assert len(levels) == 2
    assert sorted(len(cells) for cells in levels.values()) == [2, 2]


def test_a_mislabelled_payload_split_is_refused_before_the_expansion(mutable):
    """Ordering, not catching: the expansion would raise a foreign IndexError.

    ``expand_reservations`` indexes each split's payload list by the balanced context
    table.  A payload profile relabelled onto another split leaves ``dev`` one profile
    short, and the expansion fails with a bare ``IndexError`` from another module.  The
    read validates the per-split table first, so the caller sees a named error naming
    the document.
    """
    screen_doc, assignment_doc = mutable
    assignment_doc["context_profiles"]["payloads"][0]["split"] = "test"
    with pytest.raises(pc.PayloadConditioningError, match="requires exactly 2"):
        pc.compute_payload_conditioning(screen_doc, assignment_doc)


def test_a_short_environment_list_is_refused_before_the_expansion(mutable):
    """The same foreign-IndexError route exists through the other two factors."""
    screen_doc, assignment_doc = mutable
    assignment_doc["context_profiles"]["environments"] = [
        profile for profile in assignment_doc["context_profiles"]["environments"]
        if profile["id"] != "env_dev_warm2c"]
    with pytest.raises(pc.PayloadConditioningError,
                       match="reserves 1 environments profiles"):
        pc.compute_payload_conditioning(screen_doc, assignment_doc)


def test_a_short_contact_list_is_refused_before_the_expansion(mutable):
    screen_doc, assignment_doc = mutable
    assignment_doc["context_profiles"]["contacts"] = [
        profile for profile in assignment_doc["context_profiles"]["contacts"]
        if profile["id"] != "contact_dev_brief"]
    with pytest.raises(pc.PayloadConditioningError,
                       match="reserves 1 contacts profiles"):
        pc.compute_payload_conditioning(screen_doc, assignment_doc)


def test_an_assignment_without_context_profiles_is_refused(mutable):
    screen_doc, assignment_doc = mutable
    del assignment_doc["context_profiles"]
    with pytest.raises(pc.PayloadConditioningError,
                       match="no context_profiles object"):
        pc.compute_payload_conditioning(screen_doc, assignment_doc)


def test_a_context_profile_entry_that_is_not_an_object_is_refused(mutable):
    screen_doc, assignment_doc = mutable
    assignment_doc["context_profiles"]["environments"][0] = "env_dev_iso25c"
    with pytest.raises(pc.PayloadConditioningError,
                       match=r"environments\[0\] must be an object"):
        pc.compute_payload_conditioning(screen_doc, assignment_doc)


def test_a_context_profile_naming_an_unknown_split_is_refused(mutable):
    screen_doc, assignment_doc = mutable
    assignment_doc["context_profiles"]["contacts"][0]["split"] = "holdout"
    with pytest.raises(pc.PayloadConditioningError,
                       match=r"contacts\[0\] carries unknown split"):
        pc.compute_payload_conditioning(screen_doc, assignment_doc)


def test_a_level_whose_cells_share_an_environment_is_refused_as_confounded(mutable):
    """If environment did not vary inside a level, payload would be confounded."""
    screen_doc, assignment_doc = mutable
    for profile in assignment_doc["context_profiles"]["environments"]:
        if profile["split"] == "dev":
            profile["id"] = "env_dev_single"
    with pytest.raises(pc.PayloadConditioningError, match="is confounded with another"):
        pc.compute_payload_conditioning(screen_doc, assignment_doc)


def test_a_level_whose_cells_share_a_contact_profile_is_refused_as_confounded(mutable):
    screen_doc, assignment_doc = mutable
    for profile in assignment_doc["context_profiles"]["contacts"]:
        if profile["split"] == "dev":
            profile["id"] = "contact_dev_single"
    with pytest.raises(pc.PayloadConditioningError, match="is confounded with another"):
        pc.compute_payload_conditioning(screen_doc, assignment_doc)


def test_a_zero_reference_distance_is_refused_rather_than_dividing(mutable):
    screen_doc, assignment_doc = mutable
    for cell in ("4", "5"):
        screen_doc["results"]["ladder"][0]["per_cell"][cell]["d"] = 0.0
    with pytest.raises(pc.PayloadConditioningError,
                       match="an attenuation ratio needs a"):
        pc.compute_payload_conditioning(screen_doc, assignment_doc)


def test_the_mean_of_an_empty_list_is_refused(mutable):
    with pytest.raises(pc.PayloadConditioningError, match="mean of an empty list"):
        pc.mean([])


# --------------------------------------------------------------------------
# The Stage-C null control.
# --------------------------------------------------------------------------

def test_a_screen_without_stage_c_nulls_is_refused(mutable):
    screen_doc, assignment_doc = mutable
    screen_doc["results"]["stage_c_nulls"] = {}
    with pytest.raises(pc.PayloadConditioningError, match="no stage_c_nulls object"):
        pc.compute_payload_conditioning(screen_doc, assignment_doc)


def test_stage_c_nulls_missing_a_cell_are_refused(mutable):
    screen_doc, assignment_doc = mutable
    del screen_doc["results"]["stage_c_nulls"]["7"]
    with pytest.raises(pc.PayloadConditioningError,
                       match="stage_c_nulls must cover exactly cells"):
        pc.compute_payload_conditioning(screen_doc, assignment_doc)


def test_a_stage_c_null_entry_that_is_not_an_object_is_refused(mutable):
    screen_doc, assignment_doc = mutable
    screen_doc["results"]["stage_c_nulls"]["7"] = 0.42
    with pytest.raises(pc.PayloadConditioningError,
                       match=r"stage_c_nulls\[7\] must be an object"):
        pc.compute_payload_conditioning(screen_doc, assignment_doc)


def test_a_non_finite_stage_c_null_is_refused(mutable):
    screen_doc, assignment_doc = mutable
    screen_doc["results"]["stage_c_nulls"]["7"]["q95_c"] = None
    with pytest.raises(pc.PayloadConditioningError, match="Stage-C null q95_c at cell"):
        pc.compute_payload_conditioning(screen_doc, assignment_doc)


# --------------------------------------------------------------------------
# Both ends of the two branches whose real-data value sits at one end.
# --------------------------------------------------------------------------

def test_a_cell_whose_margin_never_crosses_reports_no_bracket(mutable):
    """The real ladder crosses in every cell, so this branch needs constructing."""
    screen_doc, assignment_doc = mutable
    for row in screen_doc["results"]["ladder"]:
        for cell in ("4", "5", "6", "7"):
            row["per_cell"][cell]["margin"] = 1.0
    report = pc.compute_payload_conditioning(screen_doc, assignment_doc)
    for cell in ("4", "5", "6", "7"):
        entry = report["severity_boundary_by_cell"][cell]
        assert entry["crossing_bracket"] is None
        assert "does not bracket a boundary" in entry["note"]


def test_a_margin_that_recrosses_reports_only_the_first_crossing(mutable):
    """Ascending remaining EI; a later sign change must not overwrite the first."""
    screen_doc, assignment_doc = mutable
    margins = {0.35: 1.0, 0.4: -1.0, 0.45: 1.0, 0.5: -1.0, 0.55: 1.0,
               0.6: 1.0, 0.65: 1.0, 0.75: 1.0, 0.85: 1.0, 0.9: 1.0}
    for row in screen_doc["results"]["ladder"]:
        for cell in ("4", "5", "6", "7"):
            row["per_cell"][cell]["margin"] = margins[row["remaining_ei"]]
    report = pc.compute_payload_conditioning(screen_doc, assignment_doc)
    bracket = report["severity_boundary_by_cell"]["4"]["crossing_bracket"]
    assert bracket["last_positive_remaining_ei"] == 0.35
    assert bracket["first_negative_remaining_ei"] == 0.4


def test_the_crossing_survives_a_ladder_stored_out_of_order(mutable):
    """The committed ladder happens to be ascending, so the sort is untested by it.

    Deleting ``rows.sort`` survived the first mutation sweep for exactly that reason --
    a test asserting a property of the document rather than of the code (Lesson 77).
    This case reverses the stored order and requires the same bracket.
    """
    screen_doc, assignment_doc = mutable
    screen_doc["results"]["ladder"] = list(reversed(screen_doc["results"]["ladder"]))
    report = pc.compute_payload_conditioning(screen_doc, assignment_doc)
    bracket = report["severity_boundary_by_cell"]["7"]["crossing_bracket"]
    assert bracket["last_positive_remaining_ei"] == 0.45
    assert bracket["first_negative_remaining_ei"] == 0.5
    assert [row["remaining_ei"] for row in report["attenuation"]["by_ladder_value"]] == [
        0.35, 0.4, 0.45, 0.5, 0.55, 0.6, 0.65, 0.75, 0.85, 0.9]


def test_a_margin_of_exactly_zero_counts_as_the_last_positive(mutable):
    """The rule is ``>= 0 > next``; the boundary case has to be pinned deliberately."""
    screen_doc, assignment_doc = mutable
    for row in screen_doc["results"]["ladder"]:
        for cell in ("4", "5", "6", "7"):
            value = row["remaining_ei"]
            row["per_cell"][cell]["margin"] = (
                1.0 if value < 0.45 else 0.0 if value == 0.45 else -1.0)
    report = pc.compute_payload_conditioning(screen_doc, assignment_doc)
    bracket = report["severity_boundary_by_cell"]["4"]["crossing_bracket"]
    assert bracket["last_positive_remaining_ei"] == 0.45
    assert report["severity_boundary_by_cell"]["4"]["linear_interpolation"] == 0.45


def test_a_split_reserving_only_screened_masses_is_not_listed(mutable):
    """dev is that split in the real document; construct a second one to prove the
    filter is doing work rather than the document being convenient."""
    screen_doc, assignment_doc = mutable
    for profile in assignment_doc["context_profiles"]["payloads"]:
        if profile["split"] == "test":
            profile["distal_payload_mass_kg"] = 0.05
    report = pc.compute_payload_conditioning(screen_doc, assignment_doc)
    outside = report["confirmatory_payload_coverage"][
        "splits_reserving_unscreened_masses"]
    assert "test" not in outside
    assert "val" in outside


def test_a_mass_below_the_screened_range_is_also_reported_as_unscreened(mutable):
    """The real document only has masses ABOVE the range; the lower arm is dead
    unless it is constructed."""
    screen_doc, assignment_doc = mutable
    for profile in assignment_doc["context_profiles"]["payloads"]:
        if profile["id"] == "payload_pilot_0p025kg":
            profile["distal_payload_mass_kg"] = -0.01
    report = pc.compute_payload_conditioning(screen_doc, assignment_doc)
    assert -0.01 in report["confirmatory_payload_coverage"][
        "splits_reserving_unscreened_masses"]["pilot"]


# --------------------------------------------------------------------------
# Loading, digests and the artifact the script writes.
# --------------------------------------------------------------------------

def test_a_missing_input_file_is_refused_by_name(tmp_path):
    with pytest.raises(pc.PayloadConditioningError, match="screen result does not exist"):
        pc.load_json(tmp_path / "absent.json", "screen result")


def test_a_duplicate_json_key_is_refused(tmp_path):
    path = tmp_path / "dup.json"
    path.write_text('{"a": 1, "a": 2}', encoding="utf-8")
    with pytest.raises(pc.PayloadConditioningError, match="duplicate JSON key"):
        pc.load_json(path, "screen result")


def test_a_non_finite_json_constant_is_refused(tmp_path):
    path = tmp_path / "nan.json"
    path.write_text('{"a": NaN}', encoding="utf-8")
    with pytest.raises(pc.PayloadConditioningError, match="non-finite JSON constant"):
        pc.load_json(path, "screen result")


def test_an_assignment_file_that_is_not_the_approved_bytes_is_refused(tmp_path):
    """The in-memory binding cannot see a re-indented file; only the digest can."""
    reindented = tmp_path / "assignment.json"
    reindented.write_text(
        json.dumps(json.loads(ASSIGNMENT.read_bytes()), indent=4),
        encoding="utf-8", newline="\n")
    with pytest.raises(pc.PayloadConditioningError,
                       match="does not equal the approved canonical state"):
        pc.derive_payload_conditioning(SCREEN, reindented)


def test_a_tracked_protocol_file_that_moved_is_refused(monkeypatch):
    """Move the digest of that ONE path, not the pinned constant.

    Session 59 measured why: monkeypatching ``PROTOCOL_CANONICAL_SHA256`` does not test
    this guard, because the same constant is what the screen-carried digests are
    compared against, so the run refuses several steps earlier and the test passes for
    the wrong reason.  Substituting the measurement of the protocol file alone leaves
    every other comparison intact and reaches this one.
    """
    real = pc.canonical_text_sha256

    def moved(path):
        if Path(path).name == pc.PROTOCOL_FILENAME:
            return "0" * 64
        return real(path)

    monkeypatch.setattr(pc, "canonical_text_sha256", moved)
    with pytest.raises(pc.PayloadConditioningError,
                       match="tracked Protocol P file does not equal"):
        pc.derive_payload_conditioning(SCREEN, ASSIGNMENT)


def test_the_derived_report_records_the_canonical_screen_digest():
    """A raw digest would record this checkout's line endings, not the document."""
    report = pc.derive_payload_conditioning(SCREEN, ASSIGNMENT)
    assert report["inputs"]["screen_result_canonical_sha256"] == (
        pc.canonical_text_sha256(SCREEN))
    assert report["inputs"]["protocol_canonical_sha256"] == pc.PROTOCOL_CANONICAL_SHA256
    assert report["inputs"]["assignment_canonical_sha256"] == (
        pc.ASSIGNMENT_CANONICAL_SHA256)


def test_the_render_names_the_read_as_not_pre_registered(report):
    text = pc.render(report)
    assert "NOT PRE-REGISTERED" in text
    assert "illustration only" in text
    assert "zero rollouts" in text
