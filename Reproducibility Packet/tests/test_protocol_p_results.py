"""Contract tests for the Protocol-P results layer in ``utils/protocol_p_results.py``.

The module's whole job is to keep two true statements about one plan from being confused
with each other: section 8 declares 180 logical result rows and section 11 budgets 168
Stage-A/B/C rollouts.  Twelve rows are reuses.  Every test below is either about that
arithmetic, about the reuse citation being real, or about the results-only persistence
boundary.

Two conventions carried from the construction layer's suite:

* every refusal test asserts the **reason** with a ``match=`` phrase unique to one raise
  site, not merely that a refusal occurred -- a function with two raises naming one
  invariant will keep passing a label match after the guard under test is weakened;
* every guard is tested per **branch**, not per guard.
"""

from __future__ import annotations

import dataclasses
import sys
from pathlib import Path

import pytest

PACKET_ROOT = Path(__file__).resolve().parents[1]
SCRIPTS_ROOT = PACKET_ROOT / "scripts"
sys.path.insert(0, str(SCRIPTS_ROOT))

from utils.protocol_p import ProtocolPError  # noqa: E402
from utils.protocol_p_conditions import (  # noqa: E402
    CONDITION_HEALTHY,
    CONDITION_STRUCTURAL,
    LADDER_REMAINING_EI,
    SCREEN_CELLS,
    STAGE_A_STRUCTURAL_SEVERITIES,
    STAGE_C_REPLICATES,
    admissible_candidates,
    stage_ab_identity,
    stage_c_identity,
)
from utils import protocol_p_results as results  # noqa: E402

CANDIDATES = admissible_candidates()
SELECTED = (0.10, 0.25)
BASE_CONFIG_HASH = "dev-" + "a" * 64


def _inventory(selected=SELECTED):
    """Build the full 180-row inventory at one selected candidate."""

    return results.build_logical_inventory(candidates=CANDIDATES, selected=selected)


def _physical_result(row, *, stamp: str, canonical: str = "{}") -> results.PhysicalResult:
    """Build a minimal PhysicalResult for one row, with a caller-chosen stamp."""

    return results.PhysicalResult(
        key=row.physical,
        origin_row_key=row.key,
        stage_of_origin=row.stage,
        cell=row.cell,
        provenance_hash=stamp,
        canonical_payload=canonical,
        coefficients=tuple(0.0 for _ in range(8)),
        gate_report={"passed": True, "failures": ()},
        n_steps=3000,
        elapsed_s=0.0,
    )


def _stamp(index: int) -> str:
    """Return a well-formed, base-distinct provenance stamp for a test."""

    return "dev-" + f"{index:064x}"


def _fill_ledger(rows) -> results.ResultsLedger:
    """Record one physical result per distinct body of ``rows``, in inventory order."""

    ledger = results.ResultsLedger()
    for index, row in enumerate(results.iter_new_rows(rows)):
        ledger.record(_physical_result(row, stamp=_stamp(index + 1)), base_config_hash=BASE_CONFIG_HASH)
    return ledger


# ---------------------------------------------------------------------------
# The census: 180 logical rows, 168 physical bodies, 12 reuses.
# ---------------------------------------------------------------------------


def test_the_inventory_has_the_pre_registered_shape():
    census = results.require_inventory_shape(_inventory())
    assert census["logical_rows"] == results.EXPECTED_LOGICAL_ROWS == 180
    assert census["physical_rollouts"] == results.EXPECTED_PHYSICAL_ROLLOUTS == 168
    assert census["reused_rows"] == results.EXPECTED_REUSED_ROWS == 12
    assert census["rows_by_stage"] == {"A": 108, "B": 40, "C": 32}


def test_the_derived_census_reproduces_the_pre_registered_totals():
    assert results.expected_counts(results.PRE_REGISTERED_CANDIDATE_COUNT) == {
        "logical_rows": 180,
        "physical_rollouts": 168,
        "reused_rows": 12,
    }
    assert len(CANDIDATES) == results.PRE_REGISTERED_CANDIDATE_COUNT == 9


def test_the_derived_census_scales_with_the_candidate_count():
    # Stage A is 12 rows per candidate; Stage B and C contribute a fixed 72 rows and a
    # fixed 12 reuses regardless, because the reuses are all at the selected candidate.
    for count in (1, 2, 5, 9):
        counts = results.expected_counts(count)
        assert counts["logical_rows"] == 12 * count + 72
        assert counts["reused_rows"] == 12
        assert counts["physical_rollouts"] == counts["logical_rows"] - 12


def test_a_divergence_between_the_formula_and_the_pins_is_refused(monkeypatch):
    monkeypatch.setattr(results, "EXPECTED_PHYSICAL_ROLLOUTS", 169)
    with pytest.raises(ProtocolPError, match="disagrees with section 8's pre-registered"):
        results.expected_counts(results.PRE_REGISTERED_CANDIDATE_COUNT)


def test_the_pins_are_only_asserted_at_the_pre_registered_grid(monkeypatch):
    # A wrong pin must not make a legitimate partial plan fail; it must fail at the grid
    # the pin is stated for. Both halves matter.
    monkeypatch.setattr(results, "EXPECTED_LOGICAL_ROWS", 181)
    assert results.expected_counts(2)["logical_rows"] == 96
    with pytest.raises(ProtocolPError, match="disagrees with section 8's pre-registered"):
        results.expected_counts(9)


def test_a_zero_candidate_plan_is_refused():
    with pytest.raises(ProtocolPError, match="needs at least one candidate"):
        results.expected_counts(0)


def test_a_bool_candidate_count_is_refused():
    with pytest.raises(ProtocolPError, match="candidate count must be an int"):
        results.expected_counts(True)


def test_a_two_candidate_plan_audits_cleanly_at_its_own_shape():
    rows = results.build_logical_inventory(candidates=CANDIDATES[:2], selected=CANDIDATES[0])
    census = results.require_inventory_shape(rows)
    assert census["logical_rows"] == 96
    assert census["physical_rollouts"] == 84
    assert census["reused_rows"] == 12


def test_the_gap_between_180_and_168_is_exactly_the_reuse_set():
    rows = _inventory()
    reused = [row for row in rows if row.is_reused]
    assert len(rows) - len({row.physical for row in rows}) == len(reused) == 12


def test_stage_b_reuses_the_two_stage_a_severities_in_every_cell():
    rows = [row for row in _inventory() if row.stage == results.STAGE_B and row.is_reused]
    assert len(rows) == 8
    assert {row.severity for row in rows} == set(results.STAGE_B_REUSED_SEVERITIES)
    assert {row.cell for row in rows} == set(SCREEN_CELLS)


def test_stage_c_reuses_only_k0_in_every_cell():
    rows = [row for row in _inventory() if row.stage == results.STAGE_C and row.is_reused]
    assert len(rows) == 4
    assert {row.replicate for row in rows} == {results.STAGE_C_REUSED_REPLICATE}
    assert {row.cell for row in rows} == set(SCREEN_CELLS)


def test_stage_a_pays_for_every_row_it_reports():
    rows = [row for row in _inventory() if row.stage == results.STAGE_A]
    assert len(rows) == 108
    assert not any(row.is_reused for row in rows)


def test_every_reuse_cites_the_selected_candidate_not_some_other_one():
    selected = (0.15, 0.5)
    for row in _inventory(selected):
        if not row.is_reused:
            continue
        _, _, _, _, _, peak, ramp = row.reused_from
        assert (peak, ramp) == selected


def test_the_reuse_arithmetic_moves_with_the_selection():
    # The same twelve *positions* are reuses under any selection -- Stage-B 0.75/0.35 and
    # Stage-C k=0, in four cells -- but every one of them cites a different Stage-A row,
    # because the origin is the Stage-A row at the selected candidate. A reuse table
    # computed once and carried across a re-selection would be wrong in exactly this way.
    def positions(selected):
        return {
            (row.stage, row.cell, row.condition, row.severity, row.replicate)
            for row in _inventory(selected)
            if row.is_reused
        }

    def origins(selected):
        return {row.reused_from for row in _inventory(selected) if row.is_reused}

    assert positions((0.05, 0.125)) == positions((0.15, 0.5))
    assert len(positions((0.05, 0.125))) == 12
    assert origins((0.05, 0.125)).isdisjoint(origins((0.15, 0.5)))


def test_stage_c_k0_shares_the_stage_a_healthy_body_by_construction():
    for cell in SCREEN_CELLS:
        assert stage_c_identity(cell, 0) == stage_ab_identity(cell)


# ---------------------------------------------------------------------------
# The hazard this module exists to prevent.
# ---------------------------------------------------------------------------


def test_one_body_admits_two_stamps_and_the_physical_key_refuses_the_split():
    # The measured hazard: `stage` is inside the hashed provenance payload, so asking
    # for a Stage-C label on the Stage-A body produces a different hash for the same
    # simulation.  The physical key must not carry `stage`, or the reuse disappears.
    rows = _inventory()
    stage_a_healthy = next(
        row
        for row in rows
        if row.stage == results.STAGE_A
        and row.condition == CONDITION_HEALTHY
        and row.cell == SCREEN_CELLS[0]
        and (row.probe_peak_force_n, row.probe_ramp_fraction_of_duration) == SELECTED
    )
    stage_c_k0 = next(
        row
        for row in rows
        if row.stage == results.STAGE_C and row.cell == SCREEN_CELLS[0] and row.replicate == 0
    )
    assert stage_a_healthy.stage != stage_c_k0.stage
    assert stage_a_healthy.physical == stage_c_k0.physical
    assert "stage" not in {field for field in vars(stage_a_healthy.physical)}


def test_a_reuse_that_cites_a_row_outside_the_inventory_is_refused():
    rows = list(_inventory())
    index = next(i for i, row in enumerate(rows) if row.is_reused)
    rows[index] = type(rows[index])(
        **{**vars(rows[index]), "reused_from": ("A", 99, CONDITION_HEALTHY, None, None, 0.1, 0.25)}
    )
    with pytest.raises(ProtocolPError, match="which is not a row of"):
        results.require_reuse_references(rows)


def test_a_reuse_that_cites_a_different_body_is_refused():
    rows = list(_inventory())
    index = next(i for i, row in enumerate(rows) if row.is_reused)
    victim = rows[index]
    other_cell = next(cell for cell in SCREEN_CELLS if cell != victim.cell)
    rows[index] = type(victim)(
        **{
            **vars(victim),
            "reused_from": results.stage_a_origin_row_key(
                cell=other_cell,
                condition=victim.condition,
                severity=victim.severity,
                selected=SELECTED,
            ),
        }
    )
    with pytest.raises(ProtocolPError, match="whose physical body"):
        results.require_reuse_references(rows)


def test_a_reuse_that_cites_a_stage_b_row_is_refused():
    rows = list(_inventory())
    index = next(i for i, row in enumerate(rows) if row.stage == results.STAGE_C and row.is_reused)
    stage_b_row = next(row for row in rows if row.stage == results.STAGE_B and not row.is_reused)
    rows[index] = type(rows[index])(**{**vars(rows[index]), "reused_from": stage_b_row.key})
    with pytest.raises(ProtocolPError, match="must reuse a Stage-A row"):
        results.require_reuse_references(rows)


def test_a_row_that_cites_a_row_which_is_itself_a_reuse_is_refused():
    # A citation chain leaves no row that actually ran: every link looks sourced, and
    # removing the head is invisible to a per-row check. The degenerate one-link form is
    # a self-citation, which is the shortest state that reaches this branch -- a
    # two-link chain is refused earlier, by the Stage-A check or the body check.
    rows = list(_inventory())
    index = next(i for i, row in enumerate(rows) if row.stage == results.STAGE_A)
    rows[index] = type(rows[index])(**{**vars(rows[index]), "reused_from": rows[index].key})
    with pytest.raises(ProtocolPError, match="which is itself a reuse"):
        results.require_reuse_references(rows)


def test_a_thirteenth_declared_reuse_is_refused_by_the_count():
    rows = list(_inventory())
    index = next(i for i, row in enumerate(rows) if row.stage == results.STAGE_C and row.replicate == 3)
    origin = results.stage_a_origin_row_key(
        cell=rows[index].cell, condition=CONDITION_HEALTHY, severity=None, selected=SELECTED
    )
    rows[index] = type(rows[index])(**{**vars(rows[index]), "reused_from": origin})
    with pytest.raises(ProtocolPError, match="rows must carry reused_from"):
        results.require_inventory_shape(rows)


def test_an_eleventh_declared_reuse_is_refused_by_the_count():
    rows = list(_inventory())
    index = next(i for i, row in enumerate(rows) if row.stage == results.STAGE_B and row.is_reused)
    rows[index] = type(rows[index])(**{**vars(rows[index]), "reused_from": None})
    with pytest.raises(ProtocolPError, match="rows must carry reused_from"):
        results.require_inventory_shape(rows)


def test_a_count_preserving_swap_of_which_rows_are_reuses_is_refused():
    # This is the state the count check cannot see, and the only state that reaches the
    # set-equality check: twelve rows still declare a reuse, but one of them is a row
    # whose body was never measured before, while a genuine duplicate now declares none.
    rows = list(_inventory())
    undeclared = next(
        i for i, row in enumerate(rows) if row.stage == results.STAGE_B and row.is_reused
    )
    victim = rows[undeclared]
    rows[undeclared] = type(victim)(**{**vars(victim), "reused_from": None})
    promoted = next(
        i
        for i, row in enumerate(rows)
        if row.stage == results.STAGE_C and row.cell == victim.cell and row.replicate == 3
    )
    rows[promoted] = type(rows[promoted])(
        **{
            **vars(rows[promoted]),
            "reused_from": results.stage_a_origin_row_key(
                cell=victim.cell, condition=CONDITION_HEALTHY, severity=None, selected=SELECTED
            ),
        }
    )
    assert sum(1 for row in rows if row.is_reused) == 12
    with pytest.raises(ProtocolPError, match="must be the same set"):
        results.require_inventory_shape(rows)


def test_a_short_inventory_is_refused_by_the_logical_count():
    with pytest.raises(ProtocolPError, match="declares 180 logical rows"):
        results.require_inventory_shape(_inventory()[:-1])


def test_a_duplicated_row_is_refused_before_the_count_check():
    rows = list(_inventory())
    rows[1] = rows[0]
    with pytest.raises(ProtocolPError, match="contains a duplicate row"):
        results.require_inventory_shape(rows)


# ---------------------------------------------------------------------------
# The pins that make the reuse statement true.
# ---------------------------------------------------------------------------


def test_stage_bs_reused_severities_equal_stage_as_measured_pair():
    results.require_reuse_severities_match_stage_a()
    assert set(results.STAGE_B_REUSED_SEVERITIES) == {
        float(value) for value in STAGE_A_STRUCTURAL_SEVERITIES
    }


def test_a_divergence_between_the_two_severity_tuples_is_refused(monkeypatch):
    monkeypatch.setattr(results, "STAGE_B_REUSED_SEVERITIES", (0.75, 0.40))
    with pytest.raises(ProtocolPError, match="section 8's reuse statement is only"):
        results.require_reuse_severities_match_stage_a()


def test_a_reuse_severity_off_the_ladder_is_refused(monkeypatch):
    monkeypatch.setattr(results, "STAGE_B_REUSED_SEVERITIES", (0.75, 0.35, 0.77))
    monkeypatch.setattr(results, "STAGE_A_STRUCTURAL_SEVERITIES", (0.75, 0.35, 0.77))
    with pytest.raises(ProtocolPError, match="is not on the ladder"):
        results.require_reuse_severities_match_stage_a()


def test_the_ladder_and_the_stage_a_pair_are_the_documents_own_values():
    assert LADDER_REMAINING_EI == (0.35, 0.40, 0.45, 0.50, 0.55, 0.60, 0.65, 0.75, 0.85, 0.90)
    assert set(STAGE_A_STRUCTURAL_SEVERITIES) <= set(LADDER_REMAINING_EI)
    assert STAGE_C_REPLICATES == 8


def test_a_selection_that_is_not_an_admissible_candidate_is_refused():
    with pytest.raises(ProtocolPError, match="is fabricated"):
        results.build_logical_inventory(candidates=CANDIDATES, selected=(0.40, 0.5))


# ---------------------------------------------------------------------------
# The physical key.
# ---------------------------------------------------------------------------


def test_the_key_records_a_float_severity_whatever_it_was_given():
    # Narrowed after a mutation sweep: removing the ``float(...)`` normalisation left an
    # equality-only assertion green, because Python already has ``1 == 1.0`` and
    # ``hash(1) == hash(1.0)`` -- so the key would have deduplicated either way and the
    # original test could not have gone red. What the normalisation actually guarantees
    # is the recorded *type*, which is what a serialised report shows a reader.
    identity = stage_ab_identity(SCREEN_CELLS[0])
    common = {
        "identity": identity,
        "condition": CONDITION_STRUCTURAL,
        "probe_peak_force_n": 0.1,
        "probe_ramp_fraction_of_duration": 0.25,
    }
    first = results.physical_key(severity=1, **common)
    second = results.physical_key(severity=1.0, **common)
    assert first == second
    assert type(first.severity) is float and type(second.severity) is float
    assert type(first.probe_peak_force_n) is float
    assert type(first.sensor_seed) is int and type(first.pair_id) is str


def test_payload_mass_is_additive_normalised_and_distinguishes_physical_bodies():
    """CRN-identical rollouts at different masses must never share a key."""

    identity = stage_ab_identity(SCREEN_CELLS[0])
    common = {
        "identity": identity,
        "condition": CONDITION_STRUCTURAL,
        "severity": 0.50,
        "probe_peak_force_n": 0.10,
        "probe_ramp_fraction_of_duration": 0.25,
    }
    legacy = results.physical_key(**common)
    light = results.physical_key(distal_payload_mass_kg=0, **common)
    heavy = results.physical_key(distal_payload_mass_kg=0.2, **common)
    assert legacy.distal_payload_mass_kg is None
    assert light.distal_payload_mass_kg == 0.0
    assert type(light.distal_payload_mass_kg) is float
    assert len({legacy, light, heavy}) == 3
    assert results.physical_key_report(heavy)["distal_payload_mass_kg"] == 0.2


def _payload_row(mass, *, severity=0.35, replicate=None):
    """Build one payload-boundary-shaped row: fixed identity, varying only in mass."""

    return results.LogicalRow(
        stage=results.STAGE_A,
        cell=SCREEN_CELLS[0],
        condition=CONDITION_STRUCTURAL,
        severity=severity,
        replicate=replicate,
        probe_peak_force_n=0.10,
        probe_ramp_fraction_of_duration=0.25,
        identity=stage_ab_identity(SCREEN_CELLS[0]),
        distal_payload_mass_kg=mass,
    )


def test_a_logical_row_carries_its_payload_mass_into_its_physical_key():
    """The row is the only producer of a key here, so the mass has to travel through it."""

    row = _payload_row(0.2)
    assert row.physical.distal_payload_mass_kg == 0.2
    assert results.physical_key_report(row.physical)["distal_payload_mass_kg"] == 0.2


def test_rows_that_differ_only_in_payload_mass_are_two_bodies_the_ledger_accepts():
    """Under common random numbers the mass is the *only* thing separating two rollouts.

    This is the state the payload-boundary extension runs in: one identity, one severity,
    one probe, seven masses.  Without the mass on the row the two keys are equal, the
    ledger refuses the second rollout as an unbudgeted re-execution of a body it already
    holds, and 126 planned rollouts resolve to 18 bodies.
    """

    light = _payload_row(0.025)
    heavy = _payload_row(0.200)
    assert light.physical != heavy.physical

    ledger = results.ResultsLedger()
    ledger.record(_physical_result(light, stamp=_stamp(1)), base_config_hash=BASE_CONFIG_HASH)
    ledger.record(_physical_result(heavy, stamp=_stamp(2)), base_config_hash=BASE_CONFIG_HASH)
    assert len(ledger) == 2
    assert ledger.get(light.physical).provenance_hash == _stamp(1)
    assert ledger.get(heavy.physical).provenance_hash == _stamp(2)


def test_the_protocol_p_inventory_keys_exactly_as_it_did_before_the_field_existed():
    """Additive means inert: no Protocol-P row has an override, so every mass is None."""

    rows = _inventory()
    assert all(row.distal_payload_mass_kg is None for row in rows)
    assert all(row.physical.distal_payload_mass_kg is None for row in rows)
    assert len({row.physical for row in rows}) == results.EXPECTED_PHYSICAL_ROLLOUTS == 168
    for row in rows:
        assert row.physical == results.physical_key(
            identity=row.identity,
            condition=row.condition,
            severity=row.severity,
            probe_peak_force_n=row.probe_peak_force_n,
            probe_ramp_fraction_of_duration=row.probe_ramp_fraction_of_duration,
        )


def test_a_healthy_key_with_a_severity_is_refused():
    with pytest.raises(ProtocolPError, match="healthy condition takes no severity"):
        results.physical_key(
            identity=stage_ab_identity(SCREEN_CELLS[0]),
            condition=CONDITION_HEALTHY,
            severity=0.75,
            probe_peak_force_n=0.1,
            probe_ramp_fraction_of_duration=0.25,
        )


def test_a_structural_key_without_a_severity_is_refused():
    with pytest.raises(ProtocolPError, match="requires a severity"):
        results.physical_key(
            identity=stage_ab_identity(SCREEN_CELLS[0]),
            condition=CONDITION_STRUCTURAL,
            severity=None,
            probe_peak_force_n=0.1,
            probe_ramp_fraction_of_duration=0.25,
        )


def test_a_key_built_from_something_other_than_a_rollout_identity_is_refused():
    with pytest.raises(ProtocolPError, match="needs a RolloutIdentity"):
        results.physical_key(
            identity=(150002, "basepair_protocolp_stageAB_c4"),
            condition=CONDITION_HEALTHY,
            severity=None,
            probe_peak_force_n=0.1,
            probe_ramp_fraction_of_duration=0.25,
        )


def test_two_probes_are_two_bodies():
    identity = stage_ab_identity(SCREEN_CELLS[0])
    common = {
        "identity": identity,
        "condition": CONDITION_HEALTHY,
        "severity": None,
        "probe_ramp_fraction_of_duration": 0.25,
    }
    assert results.physical_key(probe_peak_force_n=0.05, **common) != results.physical_key(
        probe_peak_force_n=0.10, **common
    )


# ---------------------------------------------------------------------------
# The ledger: 168 bodies and 168 stamps, a bijection.
# ---------------------------------------------------------------------------


def test_the_ledger_holds_one_entry_and_one_stamp_per_body():
    rows = _inventory()
    ledger = _fill_ledger(rows)
    census = results.require_physical_ledger_complete(ledger, rows)
    assert census == {"physical_results": 168, "distinct_stamps": 168}
    assert len(ledger) == 168


def test_a_second_execution_of_one_body_is_refused():
    rows = _inventory()
    ledger = results.ResultsLedger()
    row = rows[0]
    ledger.record(_physical_result(row, stamp=_stamp(1)), base_config_hash=BASE_CONFIG_HASH)
    with pytest.raises(ProtocolPError, match="a second\nexecution|is already recorded for"):
        ledger.record(_physical_result(row, stamp=_stamp(2)), base_config_hash=BASE_CONFIG_HASH)


def test_two_bodies_sharing_one_stamp_are_refused():
    rows = _inventory()
    ledger = results.ResultsLedger()
    ledger.record(_physical_result(rows[0], stamp=_stamp(1)), base_config_hash=BASE_CONFIG_HASH)
    with pytest.raises(ProtocolPError, match="is already held by"):
        ledger.record(_physical_result(rows[1], stamp=_stamp(1)), base_config_hash=BASE_CONFIG_HASH)


def test_a_stamp_equal_to_the_base_config_hash_is_refused():
    rows = _inventory()
    ledger = results.ResultsLedger()
    with pytest.raises(ProtocolPError, match="must differ from the base config hash"):
        ledger.record(
            _physical_result(rows[0], stamp=BASE_CONFIG_HASH), base_config_hash=BASE_CONFIG_HASH
        )


def test_a_stamp_without_the_dev_prefix_is_refused():
    rows = _inventory()
    ledger = results.ResultsLedger()
    with pytest.raises(ProtocolPError, match="must carry the dev- prefix"):
        ledger.record(_physical_result(rows[0], stamp="f" * 68), base_config_hash=BASE_CONFIG_HASH)


def test_a_stage_of_origin_outside_the_vocabulary_is_refused():
    rows = _inventory()
    ledger = results.ResultsLedger()
    result = _physical_result(rows[0], stamp=_stamp(1))
    broken = type(result)(**{**vars(result), "stage_of_origin": "Z"})
    with pytest.raises(ProtocolPError, match="stage of origin must be one of"):
        ledger.record(broken, base_config_hash=BASE_CONFIG_HASH)


def test_a_missing_body_is_reported_as_missing_not_as_surplus():
    rows = _inventory()
    ledger = _fill_ledger(rows[:-1])
    with pytest.raises(ProtocolPError, match="is missing"):
        results.require_physical_ledger_complete(ledger, rows)


def test_an_unplanned_body_is_reported_as_unplanned():
    rows = _inventory()
    ledger = _fill_ledger(rows)
    other = _inventory((0.05, 0.125))
    extra = next(row for row in other if row.physical not in set(ledger.keys))
    ledger.record(_physical_result(extra, stamp=_stamp(9999)), base_config_hash=BASE_CONFIG_HASH)
    with pytest.raises(ProtocolPError, match="unplanned physical result"):
        results.require_physical_ledger_complete(ledger, rows)


def test_reading_an_unrecorded_body_raises_rather_than_returning_none():
    ledger = results.ResultsLedger()
    with pytest.raises(ProtocolPError, match="no physical result recorded"):
        ledger.get(_inventory()[0].physical)


# ---------------------------------------------------------------------------
# Provenance resolution: the reused row cites, it does not relabel.
# ---------------------------------------------------------------------------


def test_a_reused_row_resolves_to_the_stage_a_stamp_and_payload_verbatim():
    rows = _inventory()
    ledger = _fill_ledger(rows)
    for row in rows:
        if not row.is_reused:
            continue
        origin = next(item for item in rows if item.key == row.reused_from)
        assert results.resolve_row_provenance(ledger, row) == results.resolve_row_provenance(
            ledger, origin
        )
        stamp, canonical, stage_of_origin = results.resolve_row_provenance(ledger, row)
        assert stage_of_origin == results.STAGE_A
        assert stamp == ledger.get(origin.physical).provenance_hash
        assert canonical == ledger.get(origin.physical).canonical_payload


def test_the_report_row_carries_the_consumer_stage_and_the_physical_origin_separately():
    rows = _inventory()
    ledger = _fill_ledger(rows)
    reused = next(row for row in rows if row.stage == results.STAGE_C and row.is_reused)
    report = results.logical_row_report(ledger, reused)
    assert report["stage"] == results.STAGE_C
    assert report["stage_of_origin"] == results.STAGE_A
    assert report["reused_from"] == list(reused.reused_from)


def test_a_measured_row_reports_no_reuse_reference():
    rows = _inventory()
    ledger = _fill_ledger(rows)
    measured = next(row for row in rows if row.stage == results.STAGE_B and not row.is_reused)
    report = results.logical_row_report(ledger, measured)
    assert report["reused_from"] is None
    assert report["stage_of_origin"] == results.STAGE_B


def test_a_reused_row_whose_ledger_entry_was_produced_by_stage_c_is_refused():
    rows = _inventory()
    ledger = results.ResultsLedger()
    reused = next(row for row in rows if row.stage == results.STAGE_C and row.is_reused)
    minted = _physical_result(reused, stamp=_stamp(1))
    ledger.record(minted, base_config_hash=BASE_CONFIG_HASH)
    with pytest.raises(ProtocolPError, match="recorded stage of origin"):
        results.resolve_row_provenance(ledger, reused)


def test_a_reused_row_pointing_at_a_body_produced_by_another_row_is_refused():
    rows = _inventory()
    ledger = _fill_ledger(rows)
    reused = next(row for row in rows if row.stage == results.STAGE_B and row.is_reused)
    broken = type(reused)(
        **{
            **vars(reused),
            "reused_from": results.stage_a_origin_row_key(
                cell=reused.cell,
                condition=CONDITION_STRUCTURAL,
                severity=reused.severity,
                selected=(0.05, 0.125),
            ),
        }
    )
    with pytest.raises(ProtocolPError, match="but the ledger entry for its body"):
        results.resolve_row_provenance(ledger, broken)


def test_a_measured_row_whose_body_was_produced_by_a_different_row_is_refused():
    rows = _inventory()
    ledger = results.ResultsLedger()
    measured = next(row for row in rows if row.stage == results.STAGE_B and not row.is_reused)
    foreign = _physical_result(measured, stamp=_stamp(1))
    foreign = type(foreign)(**{**vars(foreign), "origin_row_key": ("A", 4, "healthy", None, None, 0.1, 0.25)})
    ledger.record(foreign, base_config_hash=BASE_CONFIG_HASH)
    with pytest.raises(ProtocolPError, match="must have\nbeen produced by it|must have been produced by it"):
        results.resolve_row_provenance(ledger, measured)


def test_a_measured_row_whose_ledger_stage_disagrees_with_its_own_is_refused():
    rows = _inventory()
    ledger = results.ResultsLedger()
    measured = next(row for row in rows if row.stage == results.STAGE_C and not row.is_reused)
    entry = _physical_result(measured, stamp=_stamp(1))
    entry = type(entry)(**{**vars(entry), "stage_of_origin": results.STAGE_A})
    ledger.record(entry, base_config_hash=BASE_CONFIG_HASH)
    with pytest.raises(ProtocolPError, match="its stage of origin must be its own"):
        results.resolve_row_provenance(ledger, measured)


def test_the_full_inventory_produces_180_report_rows_over_168_stamps():
    rows = _inventory()
    ledger = _fill_ledger(rows)
    reports = [results.logical_row_report(ledger, row) for row in rows]
    assert len(reports) == 180
    assert len({report["rollout_provenance"] for report in reports}) == 168
    assert sum(1 for report in reports if report["reused_from"] is not None) == 12


# ---------------------------------------------------------------------------
# The results-only persistence boundary.
# ---------------------------------------------------------------------------


def test_a_results_only_root_is_accepted(tmp_path):
    (tmp_path / "stage_abc_screen.json").write_text("{}", encoding="utf-8")
    census = results.require_results_only_root(tmp_path)
    assert census["files"] == ("stage_abc_screen.json",)


def test_a_nested_results_json_is_accepted(tmp_path):
    nested = tmp_path / "protocol_p"
    nested.mkdir()
    (nested / "stage_abc_screen.json").write_text("{}", encoding="utf-8")
    assert results.require_results_only_root(tmp_path)["files"] == (
        "protocol_p/stage_abc_screen.json",
    )


@pytest.mark.parametrize("name", sorted(results.FORBIDDEN_ROOT_DIRECTORY_NAMES))
def test_every_dataset_role_directory_is_refused(tmp_path, name):
    (tmp_path / "stage_abc_screen.json").write_text("{}", encoding="utf-8")
    (tmp_path / name).mkdir()
    with pytest.raises(ProtocolPError, match="dataset-role directory"):
        results.require_results_only_root(tmp_path)


@pytest.mark.parametrize("name", sorted(results.FORBIDDEN_ROOT_FILE_NAMES))
def test_every_dataset_role_file_is_refused(tmp_path, name):
    (tmp_path / "stage_abc_screen.json").write_text("{}", encoding="utf-8")
    (tmp_path / name).write_text("x", encoding="utf-8")
    with pytest.raises(ProtocolPError, match="dataset-role artifact"):
        results.require_results_only_root(tmp_path)


def test_an_npz_payload_is_refused_by_the_suffix_allowlist(tmp_path):
    (tmp_path / "stage_abc_screen.json").write_text("{}", encoding="utf-8")
    (tmp_path / "scenario_protocolp_stageAB_c4.npz").write_bytes(b"PK\x03\x04")
    with pytest.raises(ProtocolPError, match="is not\none of the permitted|is not one of the permitted"):
        results.require_results_only_root(tmp_path)


def test_an_unanticipated_suffix_is_refused_too(tmp_path):
    # The allowlist is the point: a write nobody named is still a write.
    (tmp_path / "stage_abc_screen.json").write_text("{}", encoding="utf-8")
    (tmp_path / "notes.txt").write_text("x", encoding="utf-8")
    with pytest.raises(ProtocolPError, match="permitted result suffixes"):
        results.require_results_only_root(tmp_path)


def test_an_empty_root_is_refused_rather_than_reported_clean(tmp_path):
    with pytest.raises(ProtocolPError, match="holds no result file"):
        results.require_results_only_root(tmp_path)


def test_a_missing_root_is_refused(tmp_path):
    with pytest.raises(ProtocolPError, match="does not exist"):
        results.require_results_only_root(tmp_path / "absent")


def test_a_file_where_the_root_should_be_is_refused(tmp_path):
    path = tmp_path / "root"
    path.write_text("x", encoding="utf-8")
    with pytest.raises(ProtocolPError, match="is not a directory"):
        results.require_results_only_root(path)


def test_a_string_path_is_refused(tmp_path):
    with pytest.raises(ProtocolPError, match="must be a Path"):
        results.require_results_only_root(str(tmp_path))


# ---------------------------------------------------------------------------
# Iteration helpers.
# ---------------------------------------------------------------------------


def test_iter_new_rows_is_the_single_definition_of_which_rows_run():
    rows = _inventory()
    new = results.iter_new_rows(rows)
    assert len(new) == 168
    assert not any(row.is_reused for row in new)
    assert len({row.physical for row in new}) == 168


def test_the_census_of_the_whole_inventory_matches_the_audit():
    rows = _inventory()
    assert results.census(rows) == results.require_inventory_shape(rows)
# ---------------------------------------------------------------------------
# The persisted physical ledger: the I12 audit record, one entry per body.
# ---------------------------------------------------------------------------


def test_the_ledger_report_holds_one_entry_per_body_carrying_its_gate_evidence():
    rows = _inventory()
    ledger = _fill_ledger(rows)
    report = results.ledger_report(ledger)
    assert len(report) == results.EXPECTED_PHYSICAL_ROLLOUTS == 168
    assert [entry["rollout_provenance"] for entry in report] == list(ledger.stamps)
    for entry in report:
        assert set(entry) == {
            "physical_key",
            "cell",
            "stage_of_origin",
            "origin_row_key",
            "rollout_provenance",
            "rollout_canonical",
            "coefficients",
            "gate_report",
            "n_steps",
            "elapsed_s",
        }
        assert entry["gate_report"]["passed"] is True
        assert entry["n_steps"] == 3000


def test_the_ledger_report_normalises_the_failure_tuple_to_a_list():
    # The in-memory document and the parsed-from-disk document must agree on types, or
    # an assertion about one is not an assertion about the other.
    rows = _inventory()
    row = results.iter_new_rows(rows)[0]
    result = dataclasses.replace(
        _physical_result(row, stamp=_stamp(1)),
        gate_report={"passed": False, "failures": ("saturated steps",)},
    )
    ledger = results.ResultsLedger()
    ledger.record(result, base_config_hash=BASE_CONFIG_HASH)
    entry = results.ledger_report(ledger)[0]
    assert entry["gate_report"]["failures"] == ["saturated steps"]
    assert isinstance(entry["gate_report"]["failures"], list)
    # And the source object is not mutated by the report.
    assert result.gate_report["failures"] == ("saturated steps",)


def test_the_ledger_report_and_the_row_report_are_joinable_on_the_stamp():
    rows = _inventory()
    ledger = _fill_ledger(rows)
    by_stamp = {entry["rollout_provenance"]: entry for entry in results.ledger_report(ledger)}
    reported = [results.logical_row_report(ledger, row) for row in rows]
    assert len(reported) == results.EXPECTED_LOGICAL_ROWS == 180
    assert all(row["rollout_provenance"] in by_stamp for row in reported)
    # The join is many-to-one by exactly the reuse count, which is the arithmetic the
    # whole module exists to keep straight.
    assert len(reported) - len(by_stamp) == results.EXPECTED_REUSED_ROWS == 12


def test_the_physical_key_report_writes_out_all_seven_key_fields():
    rows = _inventory()
    row = [item for item in rows if item.condition == CONDITION_STRUCTURAL][0]
    written = results.physical_key_report(row.physical)
    assert written == {
        "sensor_seed": row.identity.sensor_seed,
        "pair_id": row.identity.pair_id,
        "condition": row.condition,
        "severity": row.severity,
        "probe_peak_force_n": row.probe_peak_force_n,
        "probe_ramp_fraction_of_duration": row.probe_ramp_fraction_of_duration,
        "distal_payload_mass_kg": None,
    }
    assert set(written) == {field.name for field in dataclasses.fields(results.PhysicalKey)}


def test_the_physical_key_report_refuses_something_that_is_not_a_key():
    with pytest.raises(ProtocolPError, match="expected a PhysicalKey"):
        results.physical_key_report(("sensor_seed", 1))


def test_the_ledger_report_refuses_something_that_is_not_a_ledger():
    with pytest.raises(ProtocolPError, match="expected a ResultsLedger"):
        results.ledger_report({})
