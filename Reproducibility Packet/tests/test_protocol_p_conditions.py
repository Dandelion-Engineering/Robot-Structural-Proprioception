"""Contract tests for the Protocol P Stage A/B/C construction layer.

Every guard in ``utils/protocol_p_conditions.py`` is a precondition: it decides whether
a rollout that has not yet run is the rollout the protocol specified.  A vacuous guard
here is therefore expensive in a way an ordinary bug is not -- it does not produce a
wrong number, it produces a *plausible* number from an experiment nobody specified, and
Session 41 measured that the downstream safety gates pass with roughly 70x margin under
exactly that kind of defect.

So each test below feeds a guard the exact state it was written to reject, and asserts
the **reason** for the refusal through a phrase unique to one raise site, not merely that
some refusal occurred.  Where a guard is unreachable from the construction that will
actually run, that is stated in the test rather than hidden by a test that reaches it
some other way.
"""

from __future__ import annotations

import dataclasses
import hashlib
import json
import sys
from pathlib import Path

import pytest

PACKET_ROOT = Path(__file__).resolve().parents[1]
SCRIPTS_ROOT = PACKET_ROOT / "scripts"
sys.path.insert(0, str(SCRIPTS_ROOT))

from utils import protocol_p_conditions as conditions  # noqa: E402
from utils.assignment_generator import (  # noqa: E402
    ScreenOverrides,
    _screen_stamped_hash,
    screen_pair_id,
)
from utils.cable_mechanics import CableModelConfig, validate_diagnostic_excitation  # noqa: E402
from utils.gate3_assignment import (  # noqa: E402
    ScenarioReservation,
    expand_reservations,
    load_assignment,
)
from utils.protocol_p import ProtocolPError  # noqa: E402
from utils.schema_types import FaultSpec  # noqa: E402
from utils.task_control import ObservedJointControllerConfig  # noqa: E402

BASE_CONFIG_HASH = "dev-712abf27c3f8f3c331ae9b76e3f22c48857334cc15a81e819718165e47753e56"
ASSIGNMENT_DIGEST = "76255a8089f3e27d893b26d981cbf50e808bd75ba518c44b55c4635ec83514ae"
ASSIGNMENT_HASH = "dev-eec59ec8a296a9a4ff4909f8e7f1de91a0a8f4bf289ae1533a427d1a87bc33f1"
PROTOCOL_DIGEST = "5689dad7ce4194b9a7dbe381006027df178997adf732f5734a77ef048bdf421f"
ONSET_INDEX = 500  # dev t01: onset 1.00 s at control_dt_s 0.002


def source_reservation(cell: int = 4, **overrides: object) -> ScenarioReservation:
    """Build a delivered-shaped dev ``t01`` healthy reservation for one screened cell.

    Inputs: a screened cell plus field overrides. Outputs: a ``ScenarioReservation``. Purpose: the screen
    source is a real delivered reservation; this fixture carries all 15 fields with
    delivered-shaped values so that an I3 test can change a third field and see the
    guard object.
    """

    replicate = cell - conditions.FIRST_SCREEN_CELL
    payload = "payload_dev_nominal" if cell in (4, 5) else "payload_dev_0p050kg"
    environment = "env_dev_iso25c" if cell in (4, 6) else "env_dev_warm2c"
    contact = "contact_dev_brief" if cell in (4, 7) else "contact_dev_none"
    seed_base = 110760 + 10 * replicate
    fields: dict[str, object] = {
        "schema_version": "1.0",
        "draft_config_hash": BASE_CONFIG_HASH,
        "scenario_spec_id": f"scenario_dev_t01_f000_r{replicate:02d}",
        "base_pair_id": f"basepair_dev_t01_f000_r{replicate:02d}",
        "trajectory_spec_id": conditions.SCREEN_TRAJECTORY_SPEC_ID,
        "fault_setting_id": conditions.SCREEN_SOURCE_FAULT_SETTING_ID,
        "split_group_id": f"group_dev_t01_f000_r{replicate:02d}",
        "split": conditions.SCREEN_SPLIT,
        "payload_id": payload,
        "env_profile_id": environment,
        "contact_profile_id": contact,
        "sim_seed": seed_base,
        "fault_seed": seed_base + 1,
        "sensor_seed": seed_base + 2,
        "controller_seed": seed_base + 3,
    }
    fields.update(overrides)
    return ScenarioReservation(**fields)  # type: ignore[arg-type]


# ---------------------------------------------------------------------------
# Section 6 -- the realized identity table
# ---------------------------------------------------------------------------


@pytest.mark.parametrize(
    "cell,expected_seed",
    [(4, 150002), (5, 150012), (6, 150022), (7, 150032)],
)
def test_stage_ab_identities_match_the_pinned_table(cell: int, expected_seed: int) -> None:
    """The four Stage A/B identities are pinned literals in section 6."""

    identity = conditions.stage_ab_identity(cell)
    assert identity.sensor_seed == expected_seed
    assert identity.pair_id == f"basepair_protocolp_stageAB_c{cell}"


@pytest.mark.parametrize("cell", conditions.SCREEN_CELLS)
def test_stage_c_k0_is_the_stage_ab_identity_object(cell: int) -> None:
    """I6 holds by construction: ``k=0`` returns the Stage A/B identity itself."""

    assert conditions.stage_c_identity(cell, 0) == conditions.stage_ab_identity(cell)


@pytest.mark.parametrize(
    "cell,k,expected_seed",
    [(4, 1, 151002), (4, 7, 157002), (7, 1, 151032), (7, 7, 157032)],
)
def test_stage_c_identities_match_the_pinned_table(cell: int, k: int, expected_seed: int) -> None:
    """Stage C's ``k>=1`` seeds are ``P_SEED_BASE + 10*r + 1000*k + 2``."""

    identity = conditions.stage_c_identity(cell, k)
    assert identity.sensor_seed == expected_seed
    assert identity.pair_id == f"basepair_protocolp_stageC_c{cell}_k{k}"


def test_every_screen_seed_sits_inside_the_reserved_band() -> None:
    """The reserved band cannot collide with dev, and sits far below pilot.

    Dev occupies ``[110000, 111514)`` and pilot starts at 210000; section 6 reserves
    ``[150002, 157032]``. This is the check that a seed formula change would have to
    survive before it could quietly reach a delivered identity.
    """

    seeds = [
        conditions.stage_c_identity(cell, k).sensor_seed
        for cell in conditions.SCREEN_CELLS
        for k in range(conditions.STAGE_C_REPLICATES)
    ]
    assert min(seeds) == 150002
    assert max(seeds) == 157032
    assert all(not 110000 <= seed < 111514 for seed in seeds)
    assert all(seed < 210000 for seed in seeds)


def test_a_cell_yields_eight_distinct_identities() -> None:
    """Stage C's null is built from the 28 pairs of these eight; duplicates deflate it."""

    identities = conditions.stage_c_cell_identities(5)
    assert len(identities) == conditions.STAGE_C_REPLICATES
    assert len({(item.sensor_seed, item.pair_id) for item in identities}) == 8


@pytest.mark.parametrize("cell", [3, 8, 0, -4])
def test_an_unscreened_cell_is_refused(cell: int) -> None:
    """Section 2 screens cells 4/5/6/7; anything else would leave the reserved band."""

    with pytest.raises(ProtocolPError, match="outside the screened"):
        conditions.stage_ab_identity(cell)


def test_a_bool_is_not_a_cell() -> None:
    """``True`` is an ``int`` in Python and would silently index cell 1."""

    with pytest.raises(ProtocolPError, match="context cell must be an int"):
        conditions.require_screen_cell(True)


@pytest.mark.parametrize("k", [-1, 8, 100])
def test_an_out_of_range_replicate_is_refused(k: int) -> None:
    """Stage C reserves exactly eight replicates per cell."""

    with pytest.raises(ProtocolPError, match="replicate index"):
        conditions.stage_c_identity(4, k)


# ---------------------------------------------------------------------------
# I4 -- suffix-free realized identities
# ---------------------------------------------------------------------------


def test_a_dataset_suffixed_pair_id_is_refused_as_i4() -> None:
    """The rejected state is a realized id that could pass for a dataset identity."""

    with pytest.raises(ProtocolPError, match="I4"):
        conditions.require_suffix_free_pair_id("basepair_protocolp_stageAB_c4_dataset0")


def test_a_delivered_pair_id_is_refused_by_the_prefix_guard() -> None:
    """A delivered id carries no dataset suffix yet must still be refused.

    This is the state the suffix check alone would accept: ``basepair_dev_t01_f000_r00``
    is the *base* id of a delivered reservation, and using it as a realized screen id
    would key a screen rollout onto a delivered identity.
    """

    with pytest.raises(ProtocolPError, match="must start with"):
        conditions.require_suffix_free_pair_id("basepair_dev_t01_f000_r00")


@pytest.mark.parametrize("value", ["", None, 17])
def test_a_non_string_pair_id_is_refused(value: object) -> None:
    """An empty or non-string realized id would stamp an unusable identity."""

    with pytest.raises(ProtocolPError, match="nonempty string"):
        conditions.require_suffix_free_pair_id(value)  # type: ignore[arg-type]


# ---------------------------------------------------------------------------
# I5, I6, I7 -- identity relations
# ---------------------------------------------------------------------------


def test_duplicate_identities_are_refused_as_i5() -> None:
    """Two identical identities would contribute a zero distance to the null."""

    identity = conditions.stage_ab_identity(4)
    with pytest.raises(ProtocolPError, match="I5"):
        conditions.require_unique_cell_identities([identity, identity])


def test_identities_sharing_a_seed_are_refused_by_the_stronger_guard() -> None:
    """Distinct joint identities that share a ``sensor_seed`` are still refused.

    The joint pair is what the RNG keys on, so this state passes I5 proper; the extra
    guard exists for a caller that assembles identities by hand and is unreachable from
    :func:`stage_c_identity`, whose seeds differ by construction.
    """

    first = conditions.RolloutIdentity(sensor_seed=150002, pair_id="basepair_protocolp_a")
    second = conditions.RolloutIdentity(sensor_seed=150002, pair_id="basepair_protocolp_b")
    with pytest.raises(ProtocolPError, match="must not share a sensor_seed"):
        conditions.require_unique_cell_identities([first, second])


def test_an_empty_identity_list_is_refused() -> None:
    """A vacuous uniqueness check would report a clean result over nothing."""

    with pytest.raises(ProtocolPError, match="no identities"):
        conditions.require_unique_cell_identities([])


def test_a_k0_identity_from_another_cell_is_refused_as_i6() -> None:
    """The rejected state is the plausible one: a valid identity from the wrong cell."""

    with pytest.raises(ProtocolPError, match="I6"):
        conditions.require_stage_c_k0_matches_stage_ab(4, conditions.stage_ab_identity(5))


def test_an_unmatched_fault_healthy_pair_is_refused_as_i7() -> None:
    """An unmatched Stage-A/B pair would inflate ``D`` with a sensor difference."""

    with pytest.raises(ProtocolPError, match="I7"):
        conditions.require_matched_identity(
            conditions.stage_ab_identity(4), conditions.stage_ab_identity(5)
        )


# ---------------------------------------------------------------------------
# I13a -- the closed condition vocabulary and the constructed fault tuple
# ---------------------------------------------------------------------------


def test_healthy_requests_an_explicitly_empty_fault_tuple() -> None:
    """``()`` means an explicit healthy body; ``None`` would mean 'use the reservation'."""

    assert conditions.requested_fault_specs("healthy", severity=None, onset_index=ONSET_INDEX) == ()


def test_structural_requests_the_pinned_fault_field_by_field() -> None:
    """Every field I13a pins is checked here, not just the ones that vary."""

    (fault,) = conditions.requested_fault_specs(
        "structural", severity=0.75, onset_index=ONSET_INDEX
    )
    assert fault.source_class == "structure"
    assert fault.subtype == "link_stiffness_loss"
    assert fault.location == 1
    assert fault.severity == 0.75
    assert fault.onset_index == ONSET_INDEX
    assert fault.compound_flag is False
    assert fault.ood_flag is False


def test_the_condition_vocabulary_is_closed_against_its_own_near_miss() -> None:
    """``structure`` is the fault's *source class*; ``structural`` is the condition.

    The two strings differ by two characters and mean different things, which is
    exactly the shape that gets typed by accident.
    """

    with pytest.raises(ProtocolPError, match="vocabulary is closed"):
        conditions.requested_fault_specs("structure", severity=0.75, onset_index=ONSET_INDEX)


def test_a_healthy_condition_with_a_severity_is_refused() -> None:
    """A severity on a healthy request means the caller confused two conditions."""

    with pytest.raises(ProtocolPError, match="takes no severity"):
        conditions.requested_fault_specs("healthy", severity=0.75, onset_index=ONSET_INDEX)


def test_a_structural_condition_without_a_severity_is_refused() -> None:
    """Silently defaulting a severity would run an unspecified ladder value."""

    with pytest.raises(ProtocolPError, match="requires a severity"):
        conditions.requested_fault_specs("structural", severity=None, onset_index=ONSET_INDEX)


@pytest.mark.parametrize("severity", [0.0, -0.5, 1.5, float("nan"), float("inf")])
def test_a_severity_outside_the_plant_constraint_is_refused(severity: float) -> None:
    """``cable_plant`` admits remaining-EI severities in ``(0, 1]`` only."""

    with pytest.raises(ProtocolPError, match="remaining-EI fraction|must be finite"):
        conditions.requested_fault_specs("structural", severity=severity, onset_index=ONSET_INDEX)


@pytest.mark.parametrize("onset", [-1, 1.5, True, "500"])
def test_a_malformed_onset_index_is_refused(onset: object) -> None:
    """The onset is a step index; a float or a bool would misplace the softening step."""

    with pytest.raises(ProtocolPError, match="onset_index must be"):
        conditions.requested_fault_specs("structural", severity=0.75, onset_index=onset)  # type: ignore[arg-type]


def test_the_matching_tuple_passes_i13a() -> None:
    """The accepted state, so the rejections below are not vacuous."""

    faults = conditions.requested_fault_specs("structural", severity=0.5, onset_index=ONSET_INDEX)
    conditions.require_constructed_condition(
        faults, "structural", severity=0.5, onset_index=ONSET_INDEX
    )


@pytest.mark.parametrize(
    "mutation",
    [
        {"source_class": "actuator"},
        {"subtype": "gain_loss"},
        {"location": 0},
        {"location": -1},
        {"severity": 0.5000001},
        {"onset_index": ONSET_INDEX + 1},
        {"compound_flag": True},
        {"ood_flag": True},
    ],
)
def test_one_wrong_field_is_refused_as_i13a(mutation: dict) -> None:
    """Each of the seven pinned fields is checked, one mutation at a time.

    ``location=-1`` is the important case: it is ``FaultSpec``'s own default and is a
    legal structural location in the plant, so a construction that simply forgot to set
    the location would build a valid fault on the *other* link.
    """

    (fault,) = conditions.requested_fault_specs(
        "structural", severity=0.5, onset_index=ONSET_INDEX
    )
    with pytest.raises(ProtocolPError, match="I13a"):
        conditions.require_constructed_condition(
            (dataclasses.replace(fault, **mutation),),
            "structural",
            severity=0.5,
            onset_index=ONSET_INDEX,
        )


def test_an_int_severity_is_refused_by_the_type_check() -> None:
    """``severity=1`` and ``severity=1.0`` compare equal but are not the same request.

    The plant stores what it is given, and an integer severity reaching a float field is
    evidence the construction path was not the one that was reviewed.
    """

    fault = FaultSpec(
        source_class="structure",
        subtype="link_stiffness_loss",
        location=1,
        severity=1,
        onset_index=ONSET_INDEX,
    )
    with pytest.raises(ProtocolPError, match="I13a: physical_faults\\[0\\].severity"):
        conditions.require_constructed_condition(
            (fault,), "structural", severity=1.0, onset_index=ONSET_INDEX
        )


def test_none_is_refused_where_a_condition_was_claimed() -> None:
    """``None`` restores the reservation's derived faults -- silently healthy here."""

    with pytest.raises(ProtocolPError, match="requires an explicit physical_faults tuple"):
        conditions.require_constructed_condition(
            None, "structural", severity=0.5, onset_index=ONSET_INDEX
        )


def test_a_healthy_condition_carrying_a_fault_is_refused() -> None:
    """The dangerous direction: a rollout labelled healthy whose plant is damaged."""

    faults = conditions.requested_fault_specs("structural", severity=0.5, onset_index=ONSET_INDEX)
    with pytest.raises(ProtocolPError, match="requires 0 fault spec"):
        conditions.require_constructed_condition(
            faults, "healthy", severity=None, onset_index=ONSET_INDEX
        )


# ---------------------------------------------------------------------------
# I3 and section 5 -- the screen reservation
# ---------------------------------------------------------------------------


def test_a_screen_reservation_moves_exactly_two_fields() -> None:
    """Everything that makes the screen comparable to the delivered run stays fixed."""

    source = source_reservation()
    identity = conditions.stage_ab_identity(4)
    screen = conditions.screen_reservation(
        source, cell=4, sensor_seed=identity.sensor_seed, base_pair_id=identity.pair_id
    )
    assert screen.sensor_seed == identity.sensor_seed
    assert screen.base_pair_id == identity.pair_id
    for field in dataclasses.fields(ScenarioReservation):
        if field.name not in conditions.SCREEN_RESERVATION_FIELDS:
            assert getattr(screen, field.name) == getattr(source, field.name)


def test_a_source_reservation_from_another_cell_is_refused() -> None:
    """A valid cell-5 source cannot be relabelled as cell 4 before construction."""

    identity = conditions.stage_ab_identity(4)
    with pytest.raises(ProtocolPError, match="cell 4 must use source scenario"):
        conditions.screen_reservation(
            source_reservation(5),
            cell=4,
            sensor_seed=identity.sensor_seed,
            base_pair_id=identity.pair_id,
        )


def test_a_third_changed_field_is_refused_as_i3() -> None:
    """The rejected state is a plausible one: a matching fault seed 'for consistency'."""

    source = source_reservation()
    screen = dataclasses.replace(
        source, sensor_seed=150002, base_pair_id="basepair_protocolp_stageAB_c4", fault_seed=150001
    )
    with pytest.raises(ProtocolPError, match="differ from its source in exactly"):
        conditions.require_screen_reservation(source, screen)


def test_an_unchanged_reservation_is_refused_by_the_exact_set_guard() -> None:
    """A screen that reuses the delivered identity is the leak I3 exists to stop.

    Matched against the phrase unique to the exact-set comparison, not against ``I3``:
    the function has two raise sites and both mention I3, so a weakened set comparison
    would still refuse this state -- for the wrong reason -- and a test that only asked
    for ``I3`` would report a guard it is no longer exercising.
    """

    source = source_reservation()
    with pytest.raises(ProtocolPError, match="differ from its source in exactly"):
        conditions.require_screen_reservation(source, source)


def test_moving_only_the_pair_id_is_refused_by_the_exact_set_guard() -> None:
    """A new name over the delivered sensor seed is not a new identity."""

    source = source_reservation()
    screen = dataclasses.replace(source, base_pair_id="basepair_protocolp_stageAB_c4")
    with pytest.raises(ProtocolPError, match="differ from its source in exactly"):
        conditions.require_screen_reservation(source, screen)


def test_moving_only_the_sensor_seed_is_refused_as_i3() -> None:
    """A fresh seed over the *delivered* base pair id is the state a subset check leaks.

    This case is why the comparison is set equality rather than containment: it is the
    one weakening under which both other refusals still fire -- so nothing else in this
    file would notice -- while a screen reservation still carries a delivered base pair
    id into the screen band.
    """

    source = source_reservation()
    screen = dataclasses.replace(source, sensor_seed=150002)
    with pytest.raises(ProtocolPError, match="differ from its source in exactly"):
        conditions.require_screen_reservation(source, screen)


@pytest.mark.parametrize(
    "mutation,expected",
    [
        ({"split": "pilot"}, "screens the 'dev' split"),
        ({"trajectory_spec_id": "trajectory_dev_ordinary_a"}, "screens 'trajectory_dev_diagnostic_b'"),
        (
            {"fault_setting_id": "fault_dev_structure_link_stiffness_loss_loc1_sev0p5"},
            "requires the healthy source setting",
        ),
    ],
)
def test_an_inadmissible_screen_source_is_refused(mutation: dict, expected: str) -> None:
    """Section 5's source is pinned: dev, the diagnostic trajectory, healthy.

    A faulted source would derive a *second* fault from the assignment on top of the
    override, and the ordinary trajectory carries no probe at all.
    """

    with pytest.raises(ProtocolPError, match=expected):
        conditions.require_screen_source(source_reservation(**mutation))


@pytest.mark.parametrize(
    "mutation,expected",
    [
        ({"base_pair_id": "basepair_dev_t01_f000_r01"}, "must use source base pair"),
        ({"split_group_id": "group_dev_t01_f000_r01"}, "must use source split group"),
    ],
)
def test_one_wrong_cell_field_in_an_otherwise_valid_source_is_refused(
    mutation: dict, expected: str
) -> None:
    """The cell binding is three separate identifiers, and each one must be exercised.

    Swapping a whole source reservation is refused by the ``scenario_spec_id`` check
    alone, so a sweep that only swaps whole sources reports two guards it never runs.
    These are the states that distinguish them: a source whose scenario names cell 4
    while its base pair or split group names cell 5.
    """

    with pytest.raises(ProtocolPError, match=expected):
        conditions.require_screen_source(source_reservation(4, **mutation), cell=4)


def test_the_cell_binding_accepts_the_real_delivered_sources() -> None:
    """Reachability, established against the approved assignment rather than a fixture.

    Every other test in this section feeds the guard a hand-built reservation, which can
    show only that a wrong state is refused. This one shows the complementary and more
    dangerous half: that the four sources the driver will actually select out of the
    I1-pinned assignment document are *accepted* for their own cell and refused for
    every other one. If the assignment's naming or its context-cell rotation ever moves,
    this goes red rather than the screen silently binding to a different body.
    """

    document = load_assignment(PACKET_ROOT / "config" / "proposed-gate3-assignment-v0.1.json")
    delivered = {
        reservation.scenario_spec_id: reservation
        for reservation in expand_reservations(document)
        if reservation.split == conditions.SCREEN_SPLIT
        and reservation.trajectory_spec_id == conditions.SCREEN_TRAJECTORY_SPEC_ID
        and reservation.fault_setting_id == conditions.SCREEN_SOURCE_FAULT_SETTING_ID
    }
    assert len(delivered) == len(conditions.SCREEN_CELLS)
    for cell in conditions.SCREEN_CELLS:
        replicate = cell - conditions.FIRST_SCREEN_CELL
        source = delivered[f"scenario_dev_t01_f000_r{replicate:02d}"]
        conditions.require_screen_source(source, cell=cell)
        for other in conditions.SCREEN_CELLS:
            if other == cell:
                continue
            with pytest.raises(ProtocolPError, match=f"cell {other} must use source scenario"):
                conditions.require_screen_source(source, cell=other)


# ---------------------------------------------------------------------------
# I8 -- provenance
# ---------------------------------------------------------------------------


def provenance_kwargs(**overrides: object) -> dict:
    """Return a complete provenance argument set with optional overrides."""

    cell = int(overrides.get("cell", 4))
    stage = str(overrides.get("stage", "A"))
    if "identity" in overrides:
        identity = overrides["identity"]
    elif stage == "C":
        identity = conditions.stage_c_identity(cell, 1)
    else:
        identity = conditions.stage_ab_identity(cell)
    assert isinstance(identity, conditions.RolloutIdentity)
    reservation = conditions.screen_reservation(
        source_reservation(cell),
        cell=cell,
        sensor_seed=identity.sensor_seed,
        base_pair_id=identity.pair_id,
    )
    condition = str(overrides.get("condition", "structural"))
    severity = overrides.get("severity", 0.75)
    onset_index = int(overrides.get("onset_index", ONSET_INDEX))
    physical_faults = conditions.requested_fault_specs(
        condition,
        severity=severity,  # type: ignore[arg-type]
        onset_index=onset_index,
    )
    kwargs: dict = {
        "stage": stage,
        "cell": cell,
        "condition": condition,
        "severity": severity,
        "identity": identity,
        "reservation": reservation,
        "physical_faults": physical_faults,
        "onset_index": onset_index,
        "probe_peak_force_n": 0.15,
        "probe_ramp_fraction_of_duration": 0.125,
        "base_config_hash": BASE_CONFIG_HASH,
        "assignment_canonical_sha256": ASSIGNMENT_DIGEST,
        "assignment_hash": ASSIGNMENT_HASH,
        "protocol_spec_sha256": PROTOCOL_DIGEST,
    }
    kwargs.update(overrides)
    return kwargs


def test_the_returned_string_is_the_object_that_was_hashed() -> None:
    """Correction 8: the recorded canonical string must re-derive the recorded digest.

    Returning both from one call is what makes this checkable at all; two separate calls
    could agree by luck and diverge later.
    """

    provenance, canonical = conditions.rollout_provenance(**provenance_kwargs())
    assert provenance == "dev-" + hashlib.sha256(canonical.encode("utf-8")).hexdigest()
    assert provenance.startswith("dev-")
    assert len(provenance) == 4 + 64


def test_rollout_provenance_matches_the_protocols_exact_payload_shape() -> None:
    """Correction 2 binds the assignment, reservation and all four override values.

    A flat payload containing only the realized identity and probe values is not an
    equivalent description: it omits the approved assignment hash, the delivered
    scenario/base reservation, and the full fault construction including onset.
    """

    _, canonical = conditions.rollout_provenance(**provenance_kwargs())
    payload = json.loads(canonical)
    assert set(payload) == {
        "base_config_hash",
        "assignment_canonical_sha256",
        "assignment_hash",
        "protocol_spec_sha256",
        "stage",
        "cell",
        "condition",
        "overrides",
        "reservation",
    }
    assert payload["assignment_hash"] == ASSIGNMENT_HASH
    assert payload["reservation"] == {
        "scenario_spec_id": "scenario_dev_t01_f000_r00",
        "base_pair_id": "basepair_protocolp_stageAB_c4",
        "sensor_seed": 150002,
    }
    assert set(payload["overrides"]) == {
        "probe_peak_force_n",
        "probe_ramp_fraction_of_duration",
        "physical_faults",
        "realized_pair_id",
    }
    assert payload["overrides"]["physical_faults"] == [
        {
            "source_class": "structure",
            "subtype": "link_stiffness_loss",
            "location": 1,
            "severity": 0.75,
            "onset_index": ONSET_INDEX,
            "compound_flag": False,
            "ood_flag": False,
        }
    ]


def test_provenance_is_deterministic_for_one_rollout() -> None:
    """The same request must stamp the same identity on every construction."""

    first, _ = conditions.rollout_provenance(**provenance_kwargs())
    second, _ = conditions.rollout_provenance(**provenance_kwargs())
    assert first == second


@pytest.mark.parametrize(
    "mutation",
    [
        {"stage": "B"},
        {"cell": 5},
        {"condition": "healthy", "severity": None},
        {"severity": 0.5},
        {"stage": "C", "identity": conditions.stage_c_identity(4, 3)},
        {"probe_peak_force_n": 0.10},
        {"probe_ramp_fraction_of_duration": 0.25},
        {"base_config_hash": "dev-" + "0" * 64},
        {"assignment_canonical_sha256": "1" * 64},
        {"assignment_hash": "dev-" + "2" * 64},
        {"protocol_spec_sha256": "3" * 64},
        {"onset_index": ONSET_INDEX + 1},
    ],
)
def test_every_distinguishing_input_moves_the_provenance(mutation: dict) -> None:
    """Two different rollouts must never share one provenance identity."""

    baseline, _ = conditions.rollout_provenance(**provenance_kwargs())
    other, _ = conditions.rollout_provenance(**provenance_kwargs(**mutation))
    assert other != baseline


@pytest.mark.parametrize(
    "mutation,expected",
    [
        ({"sensor_seed": 150012}, "sensor_seed must equal"),
        ({"base_pair_id": "basepair_protocolp_stageAB_c5"}, "base_pair_id must equal"),
    ],
)
def test_the_bound_reservation_must_match_the_realized_identity(
    mutation: dict, expected: str
) -> None:
    """The two nested payload objects cannot describe different rollout identities."""

    kwargs = provenance_kwargs()
    kwargs["reservation"] = dataclasses.replace(kwargs["reservation"], **mutation)
    with pytest.raises(ProtocolPError, match=expected):
        conditions.rollout_provenance(**kwargs)


def test_the_bound_reservation_must_retain_the_target_cells_source() -> None:
    """A cell-4 result cannot bind a cell-5 delivered scenario."""

    kwargs = provenance_kwargs()
    kwargs["reservation"] = dataclasses.replace(
        kwargs["reservation"], scenario_spec_id="scenario_dev_t01_f000_r01"
    )
    with pytest.raises(ProtocolPError, match="must retain source scenario"):
        conditions.rollout_provenance(**kwargs)


def test_a_stage_a_rollout_cannot_use_a_stage_c_identity() -> None:
    """A valid screen identity from the wrong stage remains the wrong construction."""

    identity = conditions.stage_c_identity(4, 3)
    kwargs = provenance_kwargs(identity=identity)
    with pytest.raises(ProtocolPError, match="must use its Stage A/B identity"):
        conditions.rollout_provenance(**kwargs)


@pytest.mark.parametrize(
    "identity",
    [
        conditions.stage_c_identity(5, 3),
        conditions.stage_ab_identity(5),
        conditions.RolloutIdentity(sensor_seed=150002, pair_id="basepair_protocolp_stageC_c4_k9"),
    ],
)
def test_a_stage_c_rollout_cannot_use_an_identity_from_outside_its_cell(
    identity: object,
) -> None:
    """The Stage-C branch needs its own rejected states, not the Stage-A/B ones.

    Stage A/B and Stage C are refused by two different raise sites, and only the first
    was exercised. Under a weakened membership test the Stage-C branch would accept any
    identity at all -- including cell 5's -- which is the same wrong-cell composition the
    Stage-A/B case is written to stop, at the stage that supplies the operative null.
    ``stage_c_identity(4, 0)`` is deliberately *not* in this list: I6 makes it the cell's
    own Stage-A identity, so accepting it is correct.
    """

    kwargs = provenance_kwargs(stage="C", condition="healthy", severity=None, identity=identity)
    with pytest.raises(ProtocolPError, match="one of its eight Stage-C identities"):
        conditions.rollout_provenance(**kwargs)


@pytest.mark.parametrize("stage", ["Z", "a", "", "AB", "stage A"])
def test_a_stage_outside_the_closed_vocabulary_is_refused(stage: str) -> None:
    """The vocabulary check is what stops an unknown stage falling into a real branch.

    The identity here is a valid Stage-C one, which is what makes the case
    discriminating: without the vocabulary check an unknown stage does not raise, it
    silently takes the ``else`` branch and is accepted as Stage C, stamping a rollout
    with a stage name the protocol never defined.
    """

    kwargs = provenance_kwargs(
        stage=stage,
        condition="healthy",
        severity=None,
        identity=conditions.stage_c_identity(4, 1),
    )
    with pytest.raises(ProtocolPError, match="stage must be one of"):
        conditions.rollout_provenance(**kwargs)


@pytest.mark.parametrize(
    "faults,expected",
    [
        ((), "requires 1 fault spec"),
        (
            conditions.requested_fault_specs("structural", severity=0.75, onset_index=0),
            "onset_index is 0",
        ),
        (
            conditions.requested_fault_specs("structural", severity=0.50, onset_index=ONSET_INDEX),
            "severity is 0.5",
        ),
    ],
)
def test_the_stamped_fault_tuple_must_match_the_stamped_condition(
    faults: tuple, expected: str
) -> None:
    """I13a is re-checked here, and that is not redundant with ``build_overrides``.

    Both call sites enforce it, so removing either one alone leaves the other standing
    and no test notices. These states go through ``rollout_provenance`` directly, which
    is the function that decides what the provenance digest binds -- and the second case
    is the exact Session-41 defect: a fault that softens the body at step 0 instead of
    the declared step 500.
    """

    kwargs = provenance_kwargs(physical_faults=faults)
    with pytest.raises(ProtocolPError, match=expected):
        conditions.rollout_provenance(**kwargs)


@pytest.mark.parametrize(
    "provenance,expected",
    [
        ("712abf27" + "0" * 56, "must carry the dev- prefix"),
        ("dev-" + "0" * 63, "one lowercase SHA-256 digest"),
        ("dev-" + "A" * 64, "one lowercase SHA-256 digest"),
        ("dev-" + "g" * 64, "one lowercase SHA-256 digest"),
        (BASE_CONFIG_HASH, "must differ from the base config hash"),
    ],
)
def test_a_malformed_or_base_provenance_is_refused_as_i8(provenance: str, expected: str) -> None:
    """The base-distinctness state is unreachable from ``rollout_provenance``.

    The base hash is inside the hashed payload, so the digest could only equal it at a
    SHA-256 fixed point. The guard is separated out precisely so the rejected state can
    be constructed and fed to it here, and so its call site can be wire-tested below.
    """

    with pytest.raises(ProtocolPError, match=expected):
        conditions.require_base_distinct_provenance(provenance, BASE_CONFIG_HASH)


def test_rollout_provenance_actually_calls_the_base_distinctness_guard(monkeypatch) -> None:
    """Unit-testing both ends of a wire does not test the wire.

    Deleting the call site is invisible to every test above, because the rejected state
    cannot be produced through ``rollout_provenance``. Monkeypatching the guard to raise
    is what makes the call itself observable.
    """

    def always_raise(provenance: str, base_config_hash: str) -> None:
        raise ProtocolPError("wire probe reached the guard")

    monkeypatch.setattr(conditions, "require_base_distinct_provenance", always_raise)
    with pytest.raises(ProtocolPError, match="wire probe reached the guard"):
        conditions.rollout_provenance(**provenance_kwargs())


# ---------------------------------------------------------------------------
# The probe envelope and the torque gate
# ---------------------------------------------------------------------------


@pytest.mark.parametrize("ramp", [0.125, 0.25, 0.5])
def test_the_declared_ramp_fractions_are_admissible(ramp: float) -> None:
    """All three candidate ramp fractions must survive the envelope check."""

    conditions.require_admissible_probe(peak_force_n=0.05, ramp_fraction_of_duration=ramp)


@pytest.mark.parametrize(
    "peak,ramp,expected",
    [
        (0.15, 0.0, "ramp fraction must lie in"),
        (0.15, 0.5000001, "ramp fraction must lie in"),
        (0.15, -0.1, "ramp fraction must lie in"),
        (0.15, float("nan"), "ramp fraction must be finite"),
        (0.0, 0.125, "peak force must be finite and > 0"),
        (-0.15, 0.125, "peak force must be finite and > 0"),
        (float("inf"), 0.125, "peak force must be finite and > 0"),
        (True, 0.125, "peak force must be a real number"),
    ],
)
def test_an_inadmissible_probe_is_refused(peak: float, ramp: float, expected: str) -> None:
    """Each rejection names its own reason, so a widened guard cannot pass silently."""

    with pytest.raises(ProtocolPError, match=expected):
        conditions.require_admissible_probe(
            peak_force_n=peak, ramp_fraction_of_duration=ramp
        )


def test_the_ramp_interval_agrees_with_the_mechanics_layer() -> None:
    """The protocol's ``(0, 0.5]`` must be the interval the plant actually admits.

    Checked by **equality with the code**, not by adopting the code's value: a config at
    exactly half the duration validates, and one just past it raises. If the mechanics
    layer ever moved its boundary, this test goes red rather than the protocol silently
    inheriting a new interval.
    """

    duration = 1.25
    at_boundary = CableModelConfig(
        diagnostic_tip_load_peak_n=0.15,
        diagnostic_tip_load_frequency_hz=0.8,
        diagnostic_tip_load_start_s=1.0,
        diagnostic_tip_load_duration_s=duration,
        diagnostic_tip_load_ramp_s=duration * conditions.MAX_RAMP_FRACTION_INCLUSIVE,
    )
    validate_diagnostic_excitation(at_boundary)

    past_boundary = dataclasses.replace(
        at_boundary,
        diagnostic_tip_load_ramp_s=duration * conditions.MAX_RAMP_FRACTION_INCLUSIVE + 1e-6,
    )
    with pytest.raises(ValueError, match="cannot exceed half"):
        validate_diagnostic_excitation(past_boundary)


def test_the_torque_gate_admits_0_15_n_by_exact_equality() -> None:
    """``<=`` rather than ``<`` is load-bearing, and the equality is exact in binary.

    ``0.15 * 2 * 0.40`` and ``0.60 * 0.20`` are both exactly 0.12 as doubles, so the
    strongest admissible candidate is admitted by equality rather than by a tolerance.
    A ``<`` here would silently drop it.
    """

    left = 0.15 * conditions.TORQUE_GATE_MOMENT_ARM_FACTOR * conditions.PINNED_LINK_LENGTH_M
    right = conditions.TORQUE_GATE_FRACTION * conditions.PINNED_TORQUE_ABS_LIMIT_N_M
    assert left == right
    assert conditions.torque_gate_admits(0.15)


@pytest.mark.parametrize("peak", [0.20, 0.25, 0.30, 0.35, 0.40])
def test_the_torque_gate_excludes_every_peak_above_the_limit(peak: float) -> None:
    """Fifteen of the 24 declared candidates are excluded before any simulation."""

    assert not conditions.torque_gate_admits(peak)


def test_the_candidate_grid_admits_exactly_nine() -> None:
    """24 declared, 15 excluded by arithmetic, 9 measured -- 108 rollouts, not 288."""

    admitted = conditions.admissible_candidates()
    assert len(admitted) == 9
    assert {peak for peak, _ in admitted} == {0.05, 0.10, 0.15}
    assert {ramp for _, ramp in admitted} == set(conditions.CANDIDATE_RAMP_FRACTIONS)
    assert len(conditions.CANDIDATE_PEAK_FORCES_N) * len(conditions.CANDIDATE_RAMP_FRACTIONS) == 24


def test_the_pinned_gate_constants_equal_the_live_ones() -> None:
    """Section 8's arithmetic is stated over the plant's and controller's real numbers.

    The pins are checked against the live values by equality; the protocol never adopts
    them, so a mechanics change makes this test red instead of moving the gate.
    """

    conditions.require_torque_gate_constants(
        link_length_m=CableModelConfig().link_length_m,
        torque_abs_limit_n_m=ObservedJointControllerConfig().torque_abs_limit[0],
    )


@pytest.mark.parametrize(
    "kwargs,expected",
    [
        ({"link_length_m": 0.50, "torque_abs_limit_n_m": 0.20}, "link_length_m is"),
        ({"link_length_m": 0.40, "torque_abs_limit_n_m": 0.10}, "torque_abs_limit"),
    ],
)
def test_a_moved_gate_constant_is_refused(kwargs: dict, expected: str) -> None:
    """The rejected state is a mechanics value that drifted away from the pin."""

    with pytest.raises(ProtocolPError, match=expected):
        conditions.require_torque_gate_constants(**kwargs)


# ---------------------------------------------------------------------------
# The override bundle, and its two seam integrations
# ---------------------------------------------------------------------------


def bundle_kwargs(**overrides: object) -> dict:
    """Return a complete ``build_overrides`` argument set with optional overrides."""

    cell = int(overrides.get("cell", 4))
    stage = str(overrides.get("stage", "A"))
    if "identity" in overrides:
        identity = overrides["identity"]
    elif stage == "C":
        identity = conditions.stage_c_identity(cell, 1)
    else:
        identity = conditions.stage_ab_identity(cell)
    assert isinstance(identity, conditions.RolloutIdentity)
    kwargs: dict = {
        "stage": stage,
        "cell": cell,
        "condition": "structural",
        "severity": 0.75,
        "identity": identity,
        "reservation": conditions.screen_reservation(
            source_reservation(cell),
            cell=cell,
            sensor_seed=identity.sensor_seed,
            base_pair_id=identity.pair_id,
        ),
        "probe_peak_force_n": 0.15,
        "probe_ramp_fraction_of_duration": 0.125,
        "onset_index": ONSET_INDEX,
        "base_config_hash": BASE_CONFIG_HASH,
        "assignment_canonical_sha256": ASSIGNMENT_DIGEST,
        "assignment_hash": ASSIGNMENT_HASH,
        "protocol_spec_sha256": PROTOCOL_DIGEST,
    }
    kwargs.update(overrides)
    return kwargs


def test_a_structural_bundle_carries_every_field_explicitly() -> None:
    """Nothing in a screen bundle is left to a default."""

    overrides, canonical = conditions.build_overrides(**bundle_kwargs())
    assert isinstance(overrides, ScreenOverrides)
    assert overrides.probe_peak_force_n == 0.15
    assert overrides.probe_ramp_fraction_of_duration == 0.125
    assert overrides.realized_pair_id == "basepair_protocolp_stageAB_c4"
    assert overrides.is_active()
    (fault,) = overrides.physical_faults
    assert (fault.source_class, fault.subtype, fault.location) == (
        "structure",
        "link_stiffness_loss",
        1,
    )
    assert overrides.provenance_hash == "dev-" + hashlib.sha256(
        canonical.encode("utf-8")
    ).hexdigest()


def test_a_healthy_bundle_is_active_with_an_empty_fault_tuple() -> None:
    """``physical_faults=()`` is falsy, and every guard on it must test ``is not None``.

    A healthy screen rollout still deviates from the approved assignment -- it carries a
    probe override and a screen identity -- so its bundle must be active and must stamp
    a provenance hash rather than the base config hash.
    """

    overrides, _ = conditions.build_overrides(
        **bundle_kwargs(condition="healthy", severity=None)
    )
    assert overrides.physical_faults == ()
    assert overrides.is_active()
    assert overrides.provenance_hash is not None


def test_build_overrides_actually_calls_the_i13a_check(monkeypatch) -> None:
    """The wire, not the ends: the I13a call site must be observable.

    ``build_overrides`` builds the fault tuple from the same function I13a compares
    against, so the check can never fail from inside this function. Deleting the call
    would therefore pass every other test in this file.
    """

    def always_raise(*args: object, **kwargs: object) -> None:
        raise ProtocolPError("wire probe reached I13a")

    monkeypatch.setattr(conditions, "require_constructed_condition", always_raise)
    with pytest.raises(ProtocolPError, match="wire probe reached I13a"):
        conditions.build_overrides(**bundle_kwargs())


def test_the_bundle_stamps_its_provenance_through_the_generator_seam() -> None:
    """The seam's own guard must accept our bundle and return the provenance hash.

    This is the integration that matters: ``_screen_stamped_hash`` is what actually
    reaches ``OnlineSensorSession`` and every ``SensorModel.observe`` call, so a bundle
    the seam rejects is a bundle that cannot run.
    """

    overrides, _ = conditions.build_overrides(**bundle_kwargs())
    assert _screen_stamped_hash(overrides, BASE_CONFIG_HASH) == overrides.provenance_hash


def test_the_bundle_overrides_the_realized_pair_id_at_the_seam() -> None:
    """``screen_pair_id`` must return our suffix-free id, not the dataset fallback."""

    source = source_reservation()
    overrides, _ = conditions.build_overrides(**bundle_kwargs())
    assert screen_pair_id(source, overrides) == "basepair_protocolp_stageAB_c4"
    assert screen_pair_id(source, None) == "basepair_dev_t01_f000_r00_dataset0"


# ---------------------------------------------------------------------------
# Stage composition
# ---------------------------------------------------------------------------


def test_stage_a_runs_healthy_first_then_two_severities() -> None:
    """Stage C reuses the healthy rollout as ``k=0``, so it is built first."""

    order = conditions.iter_stage_ab_conditions()
    assert order == (("healthy", None), ("structural", 0.75), ("structural", 0.35))


def test_the_ladder_is_the_ten_reserved_remaining_ei_values() -> None:
    """Stage B's ladder and Stage A's two severities are the pinned section-8 sets."""

    assert conditions.LADDER_REMAINING_EI == (
        0.35, 0.40, 0.45, 0.50, 0.55, 0.60, 0.65, 0.75, 0.85, 0.90,
    )
    assert set(conditions.STAGE_A_STRUCTURAL_SEVERITIES) <= set(conditions.LADDER_REMAINING_EI)
    ladder = conditions.iter_stage_ab_conditions(conditions.LADDER_REMAINING_EI)
    assert len(ladder) == 11
    assert ladder[0] == ("healthy", None)
