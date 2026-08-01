"""Protocol P Stage A/B/C construction layer: conditions, identities, overrides.

What this module is
-------------------
Protocol P sections 5, 6 and 8 describe *what* each screen rollout must be before it
runs: which reservation it is derived from, which realized identity it carries, which
physical condition its plant is built for, and which typed override bundle carries all
of that into ``assignment_generator._generate_reservation``.  This module builds those
objects and refuses to build a wrong one.  It runs nothing.

Every invariant here is a **precondition**: it is checked against the constructed
request, before the rollout starts, so a failure costs zero rollouts.  That is the
distinction Correction 7 draws between a construction check and a behavioural test, and
it is why Session 41's finding matters -- the hard safety gates passed with roughly 70x
margin under a construction defect that changed which body was being measured.  A gate
on the *result* cannot see that; a check on the *request* can.

Invariants enforced here
------------------------
  * **I3**  the screen reservation differs from its source in exactly
    ``{sensor_seed, base_pair_id}`` (section 5).
  * **I4**  every realized screen pair id is suffix-free -- it carries no
    ``_dataset0`` -- so it cannot collide with an approved dataset identity.
  * **I5**  the eight Stage-C identities within a cell are distinct.
  * **I6**  Stage C's ``k=0`` identity *is* the selected Stage-A healthy identity.
  * **I7**  a Stage-A/B fault rollout and its healthy partner share one identity.
    Deliberate (common random numbers), and therefore asserted rather than assumed.
  * **I8**  an active override carries a ``dev-<64 lowercase hex>`` provenance hash
    that differs from the base config hash, together with the exact canonical string
    it was derived from (Correction 8).
  * **I13a** the constructed ``physical_faults`` tuple equals the requested condition
    field by field, over a closed condition vocabulary (Correction 1).

Not enforced here, and where it lives instead
---------------------------------------------
  * **I1/I2** belong to the replay gate (``scripts/protocol_p_replay_gate.py``).
  * **I9-I11** are statistic-side and belong to the analysis path.
  * **I12** reads the returned ``PrivilegedRecord`` and therefore belongs to the driver,
    after the rollout.
  * **I13b** is a permanent packet test
    (``tests/test_cable_plant_softening_boundary.py``), not a runtime check: the
    ``CablePlant`` instance is never returned by ``_generate_reservation``.
  * The **results-only persistence boundary** (section 9's label-stamp scope condition)
    is a property of the driver's output root, and can only be tested where that root
    exists.  Nothing in this module writes anything.

Dependency note
---------------
``ScreenOverrides`` lives in ``utils/assignment_generator.py``, which imports the plant
and therefore ``mujoco``.  Importing this module consequently imports MuJoCo.  That is
appropriate here and was not appropriate for Stage 0: every consumer of this module runs
plant rollouts.  The shared protocol primitives it uses -- ``ProtocolPError``,
``require`` and ``canonical_json`` -- come from ``utils/protocol_p.py``, which imports
only the standard library.
"""

from __future__ import annotations

import dataclasses
import hashlib
import math
from typing import Any, Iterable, Sequence

from .assignment_generator import ScreenOverrides
from .gate3_assignment import ScenarioReservation
from .protocol_p import ProtocolPError, canonical_json, require
from .schema_types import FaultSpec

# ---------------------------------------------------------------------------
# Section 2 and section 5 -- the screened universe and its source reservations.
# ---------------------------------------------------------------------------

# Only the dev diagnostic trajectory carries a probe; the ordinary trajectory is the
# pre-registered probe-free negative control and is never screened.
SCREEN_SPLIT = "dev"
SCREEN_TRAJECTORY_SPEC_ID = "trajectory_dev_diagnostic_b"
# Section 5: the source reservation stays healthy so that ``_fault_components``
# derives no physical and no sensor fault; the ladder fault enters only through
# ``overrides.physical_faults``.
SCREEN_SOURCE_FAULT_SETTING_ID = "fault_dev_healthy"

# Section 2: context cells 4/5/6/7 are replicates r00..r03 of that trajectory.
SCREEN_CELLS: tuple[int, ...] = (4, 5, 6, 7)
FIRST_SCREEN_CELL = SCREEN_CELLS[0]

# Section 5: exactly these two reservation fields may differ from the source.
SCREEN_RESERVATION_FIELDS: tuple[str, ...] = ("sensor_seed", "base_pair_id")

# ---------------------------------------------------------------------------
# Section 6 -- the realized identity table.
# ---------------------------------------------------------------------------

P_SEED_BASE = 150000
# The four seeds of a reservation are base+0/1/2/3 for sim/fault/sensor/controller;
# a screen rollout keys its sensor draw on the third of them.
SENSOR_SEED_OFFSET = 2
CELL_SEED_STRIDE = 10
STAGE_C_SEED_STRIDE = 1000
STAGE_C_REPLICATES = 8

SCREEN_PAIR_ID_PREFIX = "basepair_protocolp_"
DATASET_PAIR_ID_SUFFIX = "_dataset0"

# ---------------------------------------------------------------------------
# Section 8 -- the candidate grid, the torque gate, and the ladder.
# ---------------------------------------------------------------------------

CANDIDATE_PEAK_FORCES_N: tuple[float, ...] = (
    0.05, 0.10, 0.15, 0.20, 0.25, 0.30, 0.35, 0.40,
)
CANDIDATE_RAMP_FRACTIONS: tuple[float, ...] = (0.125, 0.25, 0.5)
# The admissible interval for a ramp fraction of the burst duration.  The mechanics
# layer enforces the same interval independently, from ``ramp > duration / 2`` in
# ``cable_mechanics.diagnostic_tip_load_envelope``; the agreement of the two is pinned
# by a test rather than by one adopting the other's value.
MIN_RAMP_FRACTION_EXCLUSIVE = 0.0
MAX_RAMP_FRACTION_INCLUSIVE = 0.5

# Section 8's approved inclusive gate: ``F_peak * 2 * link_length_m <= 0.60 * limit``.
TORQUE_GATE_FRACTION = 0.60
TORQUE_GATE_MOMENT_ARM_FACTOR = 2.0
# Pins, not readings.  A caller passes the live mechanics/controller values to
# :func:`require_torque_gate_constants`, which refuses unless they equal these.
PINNED_LINK_LENGTH_M = 0.40
PINNED_TORQUE_ABS_LIMIT_N_M = 0.20

# Section 8, Stage B.  Stage A measures the first two of these plus healthy.
LADDER_REMAINING_EI: tuple[float, ...] = (
    0.35, 0.40, 0.45, 0.50, 0.55, 0.60, 0.65, 0.75, 0.85, 0.90,
)
STAGE_A_STRUCTURAL_SEVERITIES: tuple[float, ...] = (0.75, 0.35)

# ---------------------------------------------------------------------------
# Correction 1 / I13a -- the closed condition vocabulary.
# ---------------------------------------------------------------------------

CONDITION_HEALTHY = "healthy"
CONDITION_STRUCTURAL = "structural"
CONDITIONS: tuple[str, ...] = (CONDITION_HEALTHY, CONDITION_STRUCTURAL)

# The exact structural fault I13a requires, field by field.  ``location=1`` is one of
# the two locations ``cable_plant`` admits for a structural fault; severity is the
# remaining-EI fraction and must lie in ``(0, 1]``.
STRUCTURAL_SOURCE_CLASS = "structure"
STRUCTURAL_SUBTYPE = "link_stiffness_loss"
STRUCTURAL_LOCATION = 1


@dataclasses.dataclass(frozen=True)
class RolloutIdentity:
    """The two fields that jointly key a screen rollout's sensor draw.

    ``CablePlant`` contains no RNG, so a rollout's identity is exactly
    ``(sensor_seed, realized pair_id)`` (section 6).  Both are carried together in one
    object because quoting either alone has produced a defect before: the sensor RNG is
    keyed on both jointly, and a ``pair_id`` change alone moves ``gauge_obs`` by up to
    6.50 microstrain against ``D`` values of order 0.1-0.5.
    """

    sensor_seed: int
    pair_id: str


def require_screen_cell(cell: int) -> None:
    """Raise unless ``cell`` is one of the four screened context cells.

    Inputs: a context-cell index. Outputs: none. Purpose: section 2 screens cells
    4/5/6/7 only; every identity in section 6 is derived from ``cell - 4``, so an
    out-of-universe cell would silently produce a seed outside the reserved band.
    """

    require(
        isinstance(cell, int) and not isinstance(cell, bool),
        f"context cell must be an int; got {cell!r}",
    )
    require(cell in SCREEN_CELLS, f"context cell {cell} is outside the screened {SCREEN_CELLS}")


def require_suffix_free_pair_id(pair_id: str) -> None:
    """I4: refuse a realized screen pair id that could pass for a dataset identity.

    Inputs: a realized pair id. Outputs: none. Purpose: the ``_dataset0`` suffix is
    what marks an approved dataset realization, and the generator applies it only on
    the unoverridden path. The pinned check is the suffix; the prefix check beside it
    is strictly stronger and is what actually keeps the screen band disjoint from every
    dataset identity (``basepair_dev_*``, ``basepair_pilot_*``, ...).
    """

    require(isinstance(pair_id, str) and pair_id != "", f"pair id must be a nonempty string; got {pair_id!r}")
    require(
        not pair_id.endswith(DATASET_PAIR_ID_SUFFIX),
        f"I4: realized screen pair id {pair_id!r} carries the dataset suffix "
        f"{DATASET_PAIR_ID_SUFFIX!r}",
    )
    require(
        pair_id.startswith(SCREEN_PAIR_ID_PREFIX),
        f"realized screen pair id {pair_id!r} must start with {SCREEN_PAIR_ID_PREFIX!r} "
        "so it cannot collide with an approved dataset identity",
    )


def stage_ab_identity(cell: int) -> RolloutIdentity:
    """Return the section-6 Stage A/B identity for one context cell.

    Inputs: a screened context cell. Outputs: its ``RolloutIdentity``. Purpose: Stage A
    and Stage B share one identity per cell, which is what makes their fault/healthy
    difference seed-matched (I7). The seed is ``P_SEED_BASE + 10*r + 2`` with
    ``r = cell - 4``.
    """

    require_screen_cell(cell)
    replicate = cell - FIRST_SCREEN_CELL
    identity = RolloutIdentity(
        sensor_seed=P_SEED_BASE + CELL_SEED_STRIDE * replicate + SENSOR_SEED_OFFSET,
        pair_id=f"{SCREEN_PAIR_ID_PREFIX}stageAB_c{cell}",
    )
    require_suffix_free_pair_id(identity.pair_id)
    return identity


def stage_c_identity(cell: int, k: int) -> RolloutIdentity:
    """Return the section-6 Stage C identity for one cell and replicate index.

    Inputs: a screened context cell and a replicate index ``k`` in ``0..7``. Outputs:
    its ``RolloutIdentity``. Purpose: ``k=0`` *is* the Stage-A healthy identity rather
    than a value that happens to match it, which is how I6 is satisfied by construction
    instead of by comparison; ``k>=1`` uses ``P_SEED_BASE + 10*r + 1000*k + 2``.
    """

    require_screen_cell(cell)
    require(
        isinstance(k, int) and not isinstance(k, bool),
        f"Stage C replicate index must be an int; got {k!r}",
    )
    require(
        0 <= k < STAGE_C_REPLICATES,
        f"Stage C replicate index {k} outside 0..{STAGE_C_REPLICATES - 1}",
    )
    if k == 0:
        return stage_ab_identity(cell)
    replicate = cell - FIRST_SCREEN_CELL
    identity = RolloutIdentity(
        sensor_seed=(
            P_SEED_BASE
            + CELL_SEED_STRIDE * replicate
            + STAGE_C_SEED_STRIDE * k
            + SENSOR_SEED_OFFSET
        ),
        pair_id=f"{SCREEN_PAIR_ID_PREFIX}stageC_c{cell}_k{k}",
    )
    require_suffix_free_pair_id(identity.pair_id)
    return identity


def stage_c_cell_identities(cell: int) -> tuple[RolloutIdentity, ...]:
    """Return all eight Stage-C identities for one cell, I5-checked.

    Inputs: a screened context cell. Outputs: the eight identities in ``k`` order.
    Purpose: the operative null is built from the 28 within-cell pairs of these eight,
    so a duplicate identity would silently contribute a zero distance and deflate the
    null in the direction that favours the hypothesis.
    """

    identities = tuple(stage_c_identity(cell, k) for k in range(STAGE_C_REPLICATES))
    require_unique_cell_identities(identities)
    require_stage_c_k0_matches_stage_ab(cell, identities[0])
    return identities


def require_unique_cell_identities(identities: Sequence[RolloutIdentity]) -> None:
    """I5: raise unless every identity in one cell is distinct.

    Inputs: the identities of one cell. Outputs: none. Purpose: the sensor RNG is keyed
    on ``(sensor_seed, pair_id)`` jointly, so joint distinctness is the pinned check.
    The separate ``sensor_seed`` check below is strictly stronger; it is unreachable
    from :func:`stage_c_identity`, whose seeds differ by construction, and exists for a
    caller that assembles identities by hand.
    """

    require(len(identities) > 0, "I5: no identities were supplied to check")
    keys = [(identity.sensor_seed, identity.pair_id) for identity in identities]
    require(
        len(set(keys)) == len(keys),
        f"I5: identities within a cell must be distinct; got {keys}",
    )
    seeds = [identity.sensor_seed for identity in identities]
    require(
        len(set(seeds)) == len(seeds),
        f"identities within a cell must not share a sensor_seed; got {seeds}",
    )
    pair_ids = [identity.pair_id for identity in identities]
    require(
        len(set(pair_ids)) == len(pair_ids),
        f"identities within a cell must not share a realized pair_id; got {pair_ids}",
    )


def require_stage_c_k0_matches_stage_ab(cell: int, identity: RolloutIdentity) -> None:
    """I6: raise unless Stage C's ``k=0`` identity is the Stage-A healthy identity.

    Inputs: the cell and the identity used for ``k=0``. Outputs: none. Purpose: the
    protocol reuses the selected Stage-A healthy rollout as the first Stage-C replicate;
    if the two identities diverged, one of the 28 null distances would be computed
    against a trace the driver never ran.
    """

    expected = stage_ab_identity(cell)
    require(
        identity == expected,
        f"I6: Stage C k=0 identity {identity} must be the Stage A/B identity {expected}",
    )


def require_matched_identity(
    fault_identity: RolloutIdentity, healthy_identity: RolloutIdentity
) -> None:
    """I7: raise unless a Stage-A/B fault and its healthy partner share one identity.

    Inputs: the two identities. Outputs: none. Purpose: the match is deliberate -- it
    is what cancels the sensor term from the signal side -- and section 12 records that
    the resulting matched-signal / unmatched-null asymmetry favours S. An accidental
    mismatch would inflate ``D`` with a sensor difference and be indistinguishable from
    a mechanical effect in the reported number.
    """

    require(
        fault_identity == healthy_identity,
        f"I7: Stage A/B fault identity {fault_identity} must equal its healthy "
        f"partner {healthy_identity}",
    )


def requested_fault_specs(
    condition: str, *, severity: float | None, onset_index: int
) -> tuple[FaultSpec, ...]:
    """Build the exact ``physical_faults`` tuple one condition requires.

    Inputs: a condition from the closed vocabulary, the remaining-EI severity (``None``
    for healthy) and the fault's onset step index. Outputs: the tuple to hand to
    ``ScreenOverrides.physical_faults``. Purpose: this is the single place a screen
    condition becomes a plant request, so I13a can compare a constructed tuple against a
    freshly built one rather than against a description of one.
    """

    require(
        condition in CONDITIONS,
        f"I13a: unknown condition {condition!r}; the vocabulary is closed: {CONDITIONS}",
    )
    require(
        isinstance(onset_index, int) and not isinstance(onset_index, bool),
        f"onset_index must be an int; got {onset_index!r}",
    )
    require(onset_index >= 0, f"onset_index must be non-negative; got {onset_index}")

    if condition == CONDITION_HEALTHY:
        require(
            severity is None,
            f"I13a: the healthy condition takes no severity; got {severity!r}",
        )
        return ()

    require(severity is not None, "I13a: the structural condition requires a severity")
    require(
        isinstance(severity, (int, float)) and not isinstance(severity, bool),
        f"structural severity must be a real number; got {severity!r}",
    )
    value = float(severity)
    require(math.isfinite(value), f"structural severity must be finite; got {severity!r}")
    require(
        0.0 < value <= 1.0,
        f"structural severity is a remaining-EI fraction in (0, 1]; got {value}",
    )
    return (
        FaultSpec(
            source_class=STRUCTURAL_SOURCE_CLASS,
            subtype=STRUCTURAL_SUBTYPE,
            location=STRUCTURAL_LOCATION,
            severity=value,
            onset_index=onset_index,
            compound_flag=False,
            ood_flag=False,
        ),
    )


def require_constructed_condition(
    constructed: Sequence[FaultSpec] | None,
    condition: str,
    *,
    severity: float | None,
    onset_index: int,
) -> None:
    """I13a: raise unless the constructed fault tuple equals the requested condition.

    Inputs: the tuple that will actually be handed to the generator, plus the condition
    it claims to be. Outputs: none. Purpose: checks the *construction*, never a
    downstream consequence of it. Session 41 measured that the hard safety gates passed
    with roughly 70x margin under a construction defect that changed which body was
    being measured, so a result-side gate cannot stand in for this check.
    """

    expected = requested_fault_specs(condition, severity=severity, onset_index=onset_index)
    require(
        constructed is not None,
        f"I13a: condition {condition!r} requires an explicit physical_faults tuple; "
        "None means 'use the reservation's derived faults', which is not a screen "
        "condition",
    )
    actual = tuple(constructed)
    require(
        len(actual) == len(expected),
        f"I13a: condition {condition!r} requires {len(expected)} fault spec(s); "
        f"got {len(actual)}",
    )
    for index, (built, want) in enumerate(zip(actual, expected)):
        require(
            isinstance(built, FaultSpec),
            f"I13a: physical_faults[{index}] must be a FaultSpec; got {type(built)!r}",
        )
        for field in dataclasses.fields(FaultSpec):
            got_value = getattr(built, field.name)
            want_value = getattr(want, field.name)
            require(
                got_value == want_value and type(got_value) is type(want_value),
                f"I13a: physical_faults[{index}].{field.name} is {got_value!r} "
                f"({type(got_value).__name__}); condition {condition!r} requires "
                f"{want_value!r} ({type(want_value).__name__})",
            )


def screen_reservation(
    source: ScenarioReservation, *, sensor_seed: int, base_pair_id: str
) -> ScenarioReservation:
    """Section 5: derive a screen reservation from a delivered source reservation.

    Inputs: the source reservation and the two replacement field values. Outputs: the
    screen reservation. Purpose: the source fixes payload, environment and contact by
    being the delivered ``t01`` reservation for the target cell; exactly two fields move,
    and I3 is re-checked on the result rather than trusted from this function's body.
    """

    require_screen_source(source)
    require(
        isinstance(sensor_seed, int) and not isinstance(sensor_seed, bool),
        f"sensor_seed must be an int; got {sensor_seed!r}",
    )
    derived = dataclasses.replace(
        source, sensor_seed=sensor_seed, base_pair_id=base_pair_id
    )
    require_screen_reservation(source, derived)
    return derived


def require_screen_source(source: ScenarioReservation) -> None:
    """Raise unless a reservation is an admissible section-5 screen source.

    Inputs: a candidate source reservation. Outputs: none. Purpose: section 2 screens
    only the dev diagnostic trajectory, and section 5 requires the source to be the
    healthy setting so that no fault is derived from the assignment; the ladder fault
    must enter only through ``overrides.physical_faults``.
    """

    require(
        isinstance(source, ScenarioReservation),
        f"screen source must be a ScenarioReservation; got {type(source)!r}",
    )
    require(
        source.split == SCREEN_SPLIT,
        f"section 5 screens the {SCREEN_SPLIT!r} split; source is {source.split!r}",
    )
    require(
        source.trajectory_spec_id == SCREEN_TRAJECTORY_SPEC_ID,
        f"section 2 screens {SCREEN_TRAJECTORY_SPEC_ID!r} only; source is "
        f"{source.trajectory_spec_id!r}",
    )
    require(
        source.fault_setting_id == SCREEN_SOURCE_FAULT_SETTING_ID,
        f"section 5 requires the healthy source setting "
        f"{SCREEN_SOURCE_FAULT_SETTING_ID!r}; source is {source.fault_setting_id!r}",
    )


def require_screen_reservation(
    source: ScenarioReservation, screen: ScenarioReservation
) -> None:
    """I3: raise unless the screen reservation differs in exactly the two named fields.

    Inputs: the source and derived reservations. Outputs: none. Purpose: every other
    field -- trajectory, fault setting, split, context profiles, and the three other
    seeds -- is what makes the screen rollout comparable to the delivered one. A silent
    change to any of them would move the experiment without moving its description.

    The comparison is set **equality**, not containment, and that is load-bearing: under
    containment a reservation that moved only its ``sensor_seed`` would be accepted while
    still carrying the delivered ``base_pair_id`` into the screen band. The second check
    below is unreachable while the first stands -- an exact-set match already implies the
    seed moved -- so it is a code guard against a future weakening of the first, not a
    live data guard. It is kept because a weakening is exactly what happened to this
    function under a deliberate mutation, and the second check is what kept two of the
    three rejected states rejected.
    """

    changed: list[str] = []
    for field in dataclasses.fields(ScenarioReservation):
        if getattr(source, field.name) != getattr(screen, field.name):
            changed.append(field.name)
    require(
        tuple(sorted(changed)) == tuple(sorted(SCREEN_RESERVATION_FIELDS)),
        f"I3: a screen reservation must differ from its source in exactly "
        f"{sorted(SCREEN_RESERVATION_FIELDS)}; it differs in {sorted(changed)}",
    )
    require(
        screen.sensor_seed != source.sensor_seed,
        "I3: the screen reservation's sensor_seed must actually differ from the source",
    )


def rollout_provenance(
    *,
    stage: str,
    cell: int,
    condition: str,
    severity: float | None,
    identity: RolloutIdentity,
    probe_peak_force_n: float,
    probe_ramp_fraction_of_duration: float,
    base_config_hash: str,
    assignment_canonical_sha256: str,
    protocol_spec_sha256: str,
) -> tuple[str, str]:
    """I8: build one rollout's provenance identity and the string it was hashed from.

    Inputs: everything that distinguishes this rollout from every other one, plus the
    three digests that pin the inputs it was built from. Outputs:
    ``(provenance_hash, canonical_string)`` in that order -- the digest and the exact
    object it was computed over, returned together so the caller records the same object
    that was hashed rather than a second call that ought to agree (Correction 8).

    Purpose: an overridden rollout must never present itself as an approved-configuration
    rollout. The ``dev-`` prefix keeps every screen artifact permanently ineligible for
    confirmatory analysis, and the base-distinctness check is what makes the stamp
    meaningful rather than decorative.

    Scope, stated because it has been misread before: this identity binds the rollout's
    *inputs*. It is provenance, not a tamper seal over anything the rollout produces.
    """

    require(isinstance(stage, str) and stage != "", f"stage must be a nonempty string; got {stage!r}")
    require_screen_cell(cell)
    require(condition in CONDITIONS, f"unknown condition {condition!r}; vocabulary is {CONDITIONS}")
    require_suffix_free_pair_id(identity.pair_id)
    require(
        isinstance(base_config_hash, str) and base_config_hash != "",
        "base_config_hash must be a nonempty string",
    )
    require_admissible_probe(
        peak_force_n=probe_peak_force_n,
        ramp_fraction_of_duration=probe_ramp_fraction_of_duration,
    )

    payload: dict[str, Any] = {
        "stage": stage,
        "cell": cell,
        "condition": condition,
        "severity": None if severity is None else float(severity),
        "sensor_seed": identity.sensor_seed,
        "pair_id": identity.pair_id,
        "probe_peak_force_n": float(probe_peak_force_n),
        "probe_ramp_fraction_of_duration": float(probe_ramp_fraction_of_duration),
        "base_config_hash": base_config_hash,
        "assignment_canonical_sha256": assignment_canonical_sha256,
        "protocol_spec_sha256": protocol_spec_sha256,
    }
    try:
        canonical = canonical_json(payload)
    except (TypeError, ValueError) as exc:
        raise ProtocolPError(
            f"rollout provenance payload must be finite canonical JSON: {exc}"
        ) from exc
    provenance = "dev-" + hashlib.sha256(canonical.encode("utf-8")).hexdigest()
    require_base_distinct_provenance(provenance, base_config_hash)
    return provenance, canonical


def require_base_distinct_provenance(provenance: str, base_config_hash: str) -> None:
    """I8: raise unless a provenance stamp is well-formed and base-distinct.

    Inputs: the constructed provenance hash and the base configuration hash. Outputs:
    none. Purpose: an overridden rollout that stamped the base hash would be
    indistinguishable from an approved-configuration rollout in every artifact it
    touched.

    Reachability, stated because a guard's scope is part of its meaning: from
    :func:`rollout_provenance` this can only fail if SHA-256 produced a fixed point of
    the payload that contains the base hash, so it is a **code** guard there, live for
    any other caller -- a hand-assembled bundle, or a future driver that stamps a hash
    it did not derive here. It is a separate function so that the rejected state can be
    constructed and fed to it, and so the call site can be wire-tested.
    """

    require(
        isinstance(provenance, str) and provenance.startswith("dev-"),
        f"I8: a screen provenance hash must carry the dev- prefix; got {provenance!r}",
    )
    digest = provenance[4:]
    require(
        len(digest) == 64 and all(character in "0123456789abcdef" for character in digest),
        f"I8: a screen provenance hash must be dev- plus one lowercase SHA-256 digest; "
        f"got {provenance!r}",
    )
    require(
        provenance != base_config_hash,
        "I8: a screen provenance hash must differ from the base config hash",
    )


def require_admissible_probe(
    *, peak_force_n: float, ramp_fraction_of_duration: float
) -> None:
    """Raise unless a probe override is inside the admissible envelope.

    Inputs: the candidate peak force and ramp fraction. Outputs: none. Purpose: section
    3 requires a peak override to be finite and positive and a ramp fraction to lie in
    ``(0, 0.5]``. The generator validates the same envelope when it applies the
    override; checking here means an inadmissible candidate is rejected before a rollout
    is scheduled rather than partway through one.
    """

    require(
        isinstance(peak_force_n, (int, float)) and not isinstance(peak_force_n, bool),
        f"probe peak force must be a real number; got {peak_force_n!r}",
    )
    peak = float(peak_force_n)
    require(math.isfinite(peak) and peak > 0.0, f"probe peak force must be finite and > 0; got {peak}")
    require(
        isinstance(ramp_fraction_of_duration, (int, float))
        and not isinstance(ramp_fraction_of_duration, bool),
        f"probe ramp fraction must be a real number; got {ramp_fraction_of_duration!r}",
    )
    ramp = float(ramp_fraction_of_duration)
    require(math.isfinite(ramp), f"probe ramp fraction must be finite; got {ramp}")
    require(
        MIN_RAMP_FRACTION_EXCLUSIVE < ramp <= MAX_RAMP_FRACTION_INCLUSIVE,
        f"probe ramp fraction must lie in ({MIN_RAMP_FRACTION_EXCLUSIVE}, "
        f"{MAX_RAMP_FRACTION_INCLUSIVE}]; got {ramp}",
    )


def require_torque_gate_constants(
    *, link_length_m: float, torque_abs_limit_n_m: float
) -> None:
    """Raise unless the live mechanics/controller constants equal the protocol's pins.

    Inputs: the link length and the first joint's absolute torque limit, read from the
    live ``CableModelConfig`` and ``ObservedJointPDController`` by the caller. Outputs:
    none. Purpose: section 8's admissibility arithmetic is stated over these two
    numbers, so the protocol's copy of them must be checked against the code's by
    **equality**. Adopting the live values instead would make the gate move silently
    whenever the mechanics moved, which is exactly the drift the pin exists to prevent.
    """

    require(
        float(link_length_m) == PINNED_LINK_LENGTH_M,
        f"link_length_m is {link_length_m}; section 8's torque gate is pinned at "
        f"{PINNED_LINK_LENGTH_M}",
    )
    require(
        float(torque_abs_limit_n_m) == PINNED_TORQUE_ABS_LIMIT_N_M,
        f"torque_abs_limit[0] is {torque_abs_limit_n_m}; section 8's torque gate is "
        f"pinned at {PINNED_TORQUE_ABS_LIMIT_N_M}",
    )


def torque_gate_admits(peak_force_n: float) -> bool:
    """Return whether a candidate peak force clears section 8's inclusive torque gate.

    Inputs: a candidate peak force in newtons. Outputs: ``True`` when
    ``F_peak * 2 * L <= 0.60 * torque_abs_limit[0]``. Purpose: the comparison is
    **inclusive** and that is load-bearing -- at 0.15 N both sides equal 0.12 exactly,
    so 0.15 N is admitted by equality and a ``<`` would silently drop the strongest
    admissible candidate.
    """

    moment = float(peak_force_n) * TORQUE_GATE_MOMENT_ARM_FACTOR * PINNED_LINK_LENGTH_M
    return moment <= TORQUE_GATE_FRACTION * PINNED_TORQUE_ABS_LIMIT_N_M


def admissible_candidates() -> tuple[tuple[float, float], ...]:
    """Return the section-8 candidate grid surviving the torque gate.

    Inputs: none. Outputs: ``(peak_force_n, ramp_fraction)`` pairs in grid order.
    Purpose: 24 declared candidates, 15 excluded before any simulation, 9 admitted --
    the exclusion is arithmetic and costs nothing, which is the point of computing it
    here rather than discovering it after 24 rollouts.
    """

    return tuple(
        (peak, ramp)
        for peak in CANDIDATE_PEAK_FORCES_N
        if torque_gate_admits(peak)
        for ramp in CANDIDATE_RAMP_FRACTIONS
    )


def build_overrides(
    *,
    stage: str,
    cell: int,
    condition: str,
    severity: float | None,
    identity: RolloutIdentity,
    probe_peak_force_n: float,
    probe_ramp_fraction_of_duration: float,
    onset_index: int,
    base_config_hash: str,
    assignment_canonical_sha256: str,
    protocol_spec_sha256: str,
) -> tuple[ScreenOverrides, str]:
    """Build the full typed override bundle for one screen rollout.

    Inputs: the rollout's stage, cell, condition and severity, its realized identity,
    the selected probe, the fault onset step index, and the three input digests.
    Outputs: ``(overrides, canonical_string)`` -- the bundle to pass to
    ``_generate_reservation`` and the exact provenance string its hash was computed
    over, so the driver can record the string beside the hash.

    Purpose: this is the single construction point for a screen rollout's deviation
    from the approved assignment. Every field is set explicitly, including the healthy
    case's empty fault tuple: ``physical_faults=()`` means "an explicit healthy body"
    and ``None`` means "use the reservation's derived faults", and only the first is a
    screen condition. I13a is re-checked on the constructed bundle rather than trusted
    from this function's body, so a later edit that builds the tuple differently still
    has to pass the same check.
    """

    faults = requested_fault_specs(condition, severity=severity, onset_index=onset_index)
    provenance, canonical = rollout_provenance(
        stage=stage,
        cell=cell,
        condition=condition,
        severity=severity,
        identity=identity,
        probe_peak_force_n=probe_peak_force_n,
        probe_ramp_fraction_of_duration=probe_ramp_fraction_of_duration,
        base_config_hash=base_config_hash,
        assignment_canonical_sha256=assignment_canonical_sha256,
        protocol_spec_sha256=protocol_spec_sha256,
    )
    overrides = ScreenOverrides(
        probe_peak_force_n=float(probe_peak_force_n),
        probe_ramp_fraction_of_duration=float(probe_ramp_fraction_of_duration),
        physical_faults=faults,
        realized_pair_id=identity.pair_id,
        provenance_hash=provenance,
    )
    require(
        overrides.is_active(),
        "a screen override bundle must be active; an inert bundle would stamp the base "
        "config hash and produce an approved-looking artifact",
    )
    require_constructed_condition(
        overrides.physical_faults, condition, severity=severity, onset_index=onset_index
    )
    require(
        overrides.realized_pair_id == identity.pair_id,
        "the override bundle's realized pair id must be the rollout's identity",
    )
    require_suffix_free_pair_id(str(overrides.realized_pair_id))
    return overrides, canonical


def iter_stage_ab_conditions(
    severities: Iterable[float] = STAGE_A_STRUCTURAL_SEVERITIES,
) -> tuple[tuple[str, float | None], ...]:
    """Return the ``(condition, severity)`` pairs one Stage-A cell must run.

    Inputs: the structural severities for the stage (Stage A's two by default, Stage B's
    ladder when passed). Outputs: the healthy condition followed by one structural
    condition per severity. Purpose: the healthy rollout is first because Stage C reuses
    it as ``k=0`` and Stage A/B difference it at matched identity.
    """

    conditions: list[tuple[str, float | None]] = [(CONDITION_HEALTHY, None)]
    for severity in severities:
        conditions.append((CONDITION_STRUCTURAL, float(severity)))
    return tuple(conditions)
