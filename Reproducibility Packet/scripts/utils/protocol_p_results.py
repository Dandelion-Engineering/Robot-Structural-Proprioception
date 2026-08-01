"""Protocol P Stage A/B/C results layer: logical rows, physical ledger, reuse.

What this module is
-------------------
Protocol P section 8 declares 180 logical result rows (Stage A 108, Stage B 40, Stage
C 32) and section 11 budgets 168 Stage-A/B/C rollouts.  The two numbers are both true
and they describe different objects: twelve logical rows *consume* a measurement that
an earlier row already paid for -- eight Stage-B ladder values at remaining-EI 0.75 and
0.35, and four Stage-C ``k=0`` replicates.  This module carries that distinction as
data so the driver cannot lose it.

Why it exists at all
--------------------
``stage`` is inside the hashed provenance payload (``protocol_p_conditions
.rollout_provenance``), and ``stage_c_identity(c, 0)`` *is* the Stage-A/B identity by
design (I6).  So one physical body admits two well-formed stamps depending on the label
it is asked for::

    cell 4, identity (150002, 'basepair_protocolp_stageAB_c4')
      stage='A'  ->  dev-d732ceb4ff2a8bc6a42932ff567586ea6d0c32afafe57aecbef9028db82e1892
      stage='C'  ->  dev-31089076be232e32b089ab21d44532183fe2b0c5ac4a1361e4c94a529a9339ca

A driver that mints a fresh stamp for a reused row records twelve hashes that no
artifact carries, while a per-row provenance audit still reports 180 of 180 complete.
The ruling both agents settled (Claude Session 53 proposal, Codex Session 53 decision)
is that **the physical rollout owns the provenance**: a reused row cites its origin's
hash and canonical payload verbatim and mints nothing.

The rule, stated once
---------------------
1. A **physical result** is keyed by what makes the body distinct: the realized
   identity, the condition, the severity, and the selected probe.  There are 168 of
   them and 168 distinct stamps.
2. A **logical row** is a reporting row.  There are 180.  Exactly twelve carry
   ``reused_from``, which names the Stage-A logical row whose physical result they
   consume.
3. A reused row never calls the construction layer and never mints a stamp.  Its
   provenance hash and canonical payload are the origin's, byte for byte, still
   labelled ``stage="A"`` -- because that is what ran.

Not enforced here, and where it lives instead
---------------------------------------------
  * **I3-I8, I13a** are construction-time preconditions in
    ``utils/protocol_p_conditions.py``.
  * **I9-I12** read a rollout's returned records and belong to the driver.
  * The **reuse rule's behavioural half** -- that the driver really does skip the
    construction layer for those twelve rows -- can only be tested where the driver
    is, by counting calls.  This module makes the wrong state *representable and
    refusable*; the driver's tests are what show it is not entered.

Dependency note
---------------
This module imports ``utils/protocol_p_conditions.py`` for the screened universe, the
identity table and the ladder, rather than restating them.  That module imports
``ScreenOverrides`` from the generator and therefore MuJoCo.  The coupling is
appropriate here for the same reason it is appropriate there: every consumer of this
module runs plant rollouts.
"""

from __future__ import annotations

import dataclasses
from pathlib import Path
from typing import Any, Iterable, Mapping, Sequence

from .protocol_p import ProtocolPError, require
from .protocol_p_conditions import (
    CONDITION_HEALTHY,
    CONDITION_STRUCTURAL,
    CONDITIONS,
    LADDER_REMAINING_EI,
    RolloutIdentity,
    SCREEN_CELLS,
    SCREEN_STAGES,
    STAGE_A_STRUCTURAL_SEVERITIES,
    STAGE_C_REPLICATES,
    require_base_distinct_provenance,
    require_screen_cell,
    stage_ab_identity,
    stage_c_identity,
)

STAGE_A = "A"
STAGE_B = "B"
STAGE_C = "C"

# Section 8 / section 11.  These are the pre-registered totals *for the nine admissible
# candidates*, and they are pins rather than derivations: :func:`expected_counts` builds
# the same numbers from the plan's own shape, and the two are reconciled by equality at
# the pre-registered candidate count.  Deriving alone would silently follow a changed
# grid; pinning alone would make the census unusable for any smaller run.
PRE_REGISTERED_CANDIDATE_COUNT = 9
EXPECTED_LOGICAL_ROWS = 180
EXPECTED_PHYSICAL_ROLLOUTS = 168
EXPECTED_REUSED_ROWS = 12

# Section 8, Stage B: "The values 0.75 and 0.35 are reused from Stage A at matched
# identity, so 32 rollouts are new."  Stage A measures exactly those two severities, so
# the two tuples must agree -- and they are checked by EQUALITY rather than by this
# module adopting the other's value, because a silent divergence would change which
# rows are reuses without changing either statement (Session 47's lesson).
STAGE_B_REUSED_SEVERITIES: tuple[float, ...] = (0.75, 0.35)

# Section 8, Stage C: "8 healthy replicates per cell (k=0 reused from the selected
# Stage-A healthy rollout)".
STAGE_C_REUSED_REPLICATE = 0

# The results-only persistence boundary (section 9's label-stamp scope condition).
# Any of these under the driver's output root means a dataset-role artifact was
# written, which is the exact condition that makes the stale returned label blocking.
FORBIDDEN_ROOT_DIRECTORY_NAMES: frozenset[str] = frozenset(
    {
        "plant",
        "observations",
        "labels",
        "estimator_outputs",
        "controller_logs",
    }
)
FORBIDDEN_ROOT_FILE_NAMES: frozenset[str] = frozenset(
    {
        "manifest.csv",
        "index.csv",
        "generation_audit.json",
        "independent_audit.json",
    }
)
ALLOWED_RESULT_SUFFIXES: tuple[str, ...] = (".json",)


def require_reuse_severities_match_stage_a() -> None:
    """Raise unless Stage B's reused severities are exactly Stage A's structural pair.

    Inputs: none. Outputs: none. Purpose: section 8 states the reuse in prose ("the
    values 0.75 and 0.35 are reused from Stage A"), and that prose is only true while
    Stage A actually measures those two severities. Checking by equality means a change
    to either tuple fails loudly instead of silently changing which twelve rows are
    reuses.
    """

    require(
        tuple(sorted(STAGE_B_REUSED_SEVERITIES))
        == tuple(sorted(float(value) for value in STAGE_A_STRUCTURAL_SEVERITIES)),
        f"Stage B reuses {sorted(STAGE_B_REUSED_SEVERITIES)} but Stage A measures "
        f"{sorted(STAGE_A_STRUCTURAL_SEVERITIES)}; section 8's reuse statement is only "
        "true while the two agree",
    )
    for severity in STAGE_B_REUSED_SEVERITIES:
        require(
            severity in LADDER_REMAINING_EI,
            f"Stage B reuse severity {severity} is not on the ladder "
            f"{LADDER_REMAINING_EI}",
        )


def expected_counts(candidate_count: int) -> dict[str, int]:
    """Return the plan's expected census for a given number of Stage-A candidates.

    Inputs: how many probe candidates Stage A measures. Outputs: the expected logical,
    physical and reused counts. Purpose: the pre-registered totals are stated for the
    nine admissible candidates, but a partial run is a legitimate object (a two-candidate
    integration test, or a screen resumed after drops) and it still has to satisfy the
    same arithmetic. The formula is derived once here and reconciled with section 8's
    stated totals by **equality** at ``PRE_REGISTERED_CANDIDATE_COUNT`` -- so a change to
    either the formula or the pins fails loudly instead of one quietly following the
    other.

    Stage A is ``candidates x 4 cells x 3 conditions``; Stage B is 40 rows of which 8 are
    reuses; Stage C is 32 rows of which 4 are reuses. The reuse count does not depend on
    the candidate count, because the reuses are all at the *selected* candidate.
    """

    require(
        isinstance(candidate_count, int) and not isinstance(candidate_count, bool),
        f"the candidate count must be an int; got {candidate_count!r}",
    )
    require(candidate_count > 0, f"a plan needs at least one candidate; got {candidate_count}")
    cells = len(SCREEN_CELLS)
    stage_a = candidate_count * cells * (1 + len(STAGE_A_STRUCTURAL_SEVERITIES))
    stage_b = cells * len(LADDER_REMAINING_EI)
    stage_c = cells * STAGE_C_REPLICATES
    reused = cells * len(STAGE_B_REUSED_SEVERITIES) + cells
    counts = {
        "logical_rows": stage_a + stage_b + stage_c,
        "physical_rollouts": stage_a + stage_b + stage_c - reused,
        "reused_rows": reused,
    }
    if candidate_count == PRE_REGISTERED_CANDIDATE_COUNT:
        require(
            counts["logical_rows"] == EXPECTED_LOGICAL_ROWS
            and counts["physical_rollouts"] == EXPECTED_PHYSICAL_ROLLOUTS
            and counts["reused_rows"] == EXPECTED_REUSED_ROWS,
            "the derived census disagrees with section 8's pre-registered totals at the "
            f"{PRE_REGISTERED_CANDIDATE_COUNT}-candidate grid: derived {counts}, pinned "
            f"{{'logical_rows': {EXPECTED_LOGICAL_ROWS}, 'physical_rollouts': "
            f"{EXPECTED_PHYSICAL_ROLLOUTS}, 'reused_rows': {EXPECTED_REUSED_ROWS}}}",
        )
    return counts


@dataclasses.dataclass(frozen=True)
class PhysicalKey:
    """What makes one screen rollout a distinct physical body.

    Two logical rows with the same key are the same simulation: same plant, same
    identity, same probe. That is why 180 rows resolve to 168 executions, and why the
    key -- not the ``(stage, cell, condition)`` triple -- is what the ledger is indexed
    by.

    ``stage`` is deliberately absent. Including it would make every Stage-C ``k=0`` key
    distinct from its Stage-A origin and the reuse would disappear, which is precisely
    the defect this module exists to prevent.
    """

    sensor_seed: int
    pair_id: str
    condition: str
    severity: float | None
    probe_peak_force_n: float
    probe_ramp_fraction_of_duration: float


def physical_key(
    *,
    identity: RolloutIdentity,
    condition: str,
    severity: float | None,
    probe_peak_force_n: float,
    probe_ramp_fraction_of_duration: float,
) -> PhysicalKey:
    """Build a :class:`PhysicalKey`, normalising the numeric fields.

    Inputs: the rollout identity, its condition and severity, and the selected probe.
    Outputs: the key. Purpose: normalisation is not cosmetic -- an ``int`` 1 severity
    and a ``float`` 1.0 severity would hash to different dataclass keys and split one
    physical body into two ledger entries.
    """

    require(
        isinstance(identity, RolloutIdentity),
        f"physical key needs a RolloutIdentity; got {type(identity)!r}",
    )
    require(condition in CONDITIONS, f"unknown condition {condition!r}; vocabulary is {CONDITIONS}")
    if condition == CONDITION_HEALTHY:
        require(
            severity is None,
            f"the healthy condition takes no severity; got {severity!r}",
        )
    else:
        require(
            severity is not None,
            f"condition {condition!r} requires a severity",
        )
    return PhysicalKey(
        sensor_seed=int(identity.sensor_seed),
        pair_id=str(identity.pair_id),
        condition=str(condition),
        severity=None if severity is None else float(severity),
        probe_peak_force_n=float(probe_peak_force_n),
        probe_ramp_fraction_of_duration=float(probe_ramp_fraction_of_duration),
    )


@dataclasses.dataclass(frozen=True)
class LogicalRow:
    """One reporting row of the screen, and where its measurement comes from.

    ``stage`` is the *consumer* stage -- the section-8 stage this row is reported
    under. ``reused_from`` is ``None`` for the 168 rows that pay for their own rollout,
    and the origin Stage-A row's key for the twelve that do not. The separation is the
    whole point: a reused row is reported under Stage B or Stage C while its
    measurement, its provenance hash and its canonical payload remain Stage A's.
    """

    stage: str
    cell: int
    condition: str
    severity: float | None
    replicate: int | None
    probe_peak_force_n: float
    probe_ramp_fraction_of_duration: float
    identity: RolloutIdentity
    reused_from: tuple[Any, ...] | None = None

    @property
    def key(self) -> tuple[Any, ...]:
        """Return this row's own identifier, unique across the 180 logical rows."""

        return (
            self.stage,
            self.cell,
            self.condition,
            self.severity,
            self.replicate,
            self.probe_peak_force_n,
            self.probe_ramp_fraction_of_duration,
        )

    @property
    def physical(self) -> PhysicalKey:
        """Return the physical body this row reports on."""

        return physical_key(
            identity=self.identity,
            condition=self.condition,
            severity=self.severity,
            probe_peak_force_n=self.probe_peak_force_n,
            probe_ramp_fraction_of_duration=self.probe_ramp_fraction_of_duration,
        )

    @property
    def is_reused(self) -> bool:
        """Return whether this row consumes an earlier row's measurement."""

        return self.reused_from is not None


@dataclasses.dataclass(frozen=True)
class PhysicalResult:
    """One executed rollout: what ran, what stamped it, and what it measured.

    ``stage_of_origin`` is the stage under which the rollout physically ran, and it is
    what appears inside ``canonical_payload``. A reused row's report must not relabel
    it; :func:`resolve_row_provenance` is what refuses the relabelling.

    ``coefficients`` is the eight-entry gauge harmonic vector the statistic differences
    (section 8). It is stored on the physical result rather than recomputed per logical
    row so a reused row cannot silently be measured from a second, differently windowed
    read of the same trace.
    """

    key: PhysicalKey
    origin_row_key: tuple[Any, ...]
    stage_of_origin: str
    cell: int
    provenance_hash: str
    canonical_payload: str
    coefficients: tuple[float, ...]
    gate_report: Mapping[str, Any]
    n_steps: int
    elapsed_s: float


class ResultsLedger:
    """The physical ledger: one entry per executed rollout, keyed by body.

    Refuses a second entry for a key it already holds, and refuses two keys that share
    a provenance stamp. Both refusals are the same claim from opposite sides -- the
    ledger's 168 entries and 168 stamps must be a bijection -- and a driver defect
    breaks it in one direction or the other.
    """

    def __init__(self) -> None:
        self._entries: dict[PhysicalKey, PhysicalResult] = {}
        self._stamps: dict[str, PhysicalKey] = {}

    def __len__(self) -> int:
        return len(self._entries)

    @property
    def keys(self) -> tuple[PhysicalKey, ...]:
        """Return every recorded physical key, in insertion order."""

        return tuple(self._entries)

    @property
    def stamps(self) -> tuple[str, ...]:
        """Return every recorded provenance stamp, in insertion order."""

        return tuple(self._stamps)

    def record(self, result: PhysicalResult, *, base_config_hash: str) -> None:
        """Add one executed rollout to the ledger.

        Inputs: the result and the base configuration hash it must differ from.
        Outputs: none. Purpose: this is the only way a stamp enters the record, so it is
        where the bijection is enforced. The duplicate-key refusal also catches a subtler
        defect than a repeated run: two rows that should share a body but were built with
        different onsets produce the same key and different stamps, and land here.
        """

        require(
            isinstance(result, PhysicalResult),
            f"ledger entries must be PhysicalResult; got {type(result)!r}",
        )
        require(
            result.stage_of_origin in SCREEN_STAGES,
            f"stage of origin must be one of {SCREEN_STAGES}; got {result.stage_of_origin!r}",
        )
        require_base_distinct_provenance(result.provenance_hash, base_config_hash)
        require(
            result.key not in self._entries,
            f"a physical result is already recorded for {result.key}; a second "
            "execution of one body is not budgeted and would double-count the screen",
        )
        held = self._stamps.get(result.provenance_hash)
        require(
            held is None,
            f"provenance {result.provenance_hash!r} is already held by {held}; two "
            "physical bodies cannot share one stamp",
        )
        self._entries[result.key] = result
        self._stamps[result.provenance_hash] = result.key

    def get(self, key: PhysicalKey) -> PhysicalResult:
        """Return the recorded result for one physical key, or raise.

        Inputs: a physical key. Outputs: its result. Purpose: fail loudly rather than
        returning ``None``, so a missing measurement cannot be differenced against as a
        zero vector.
        """

        require(key in self._entries, f"no physical result recorded for {key}")
        return self._entries[key]

    def has(self, key: PhysicalKey) -> bool:
        """Return whether a physical key has been recorded."""

        return key in self._entries


def build_stage_a_inventory(
    candidates: Sequence[tuple[float, float]],
) -> tuple[LogicalRow, ...]:
    """Return Stage A's logical rows: candidates x cells x conditions.

    Inputs: the admissible ``(peak, ramp)`` candidates. Outputs: the rows in
    candidate-major, cell, condition order. Purpose: Stage A pays for every row it
    reports -- none of these carries ``reused_from`` -- and the healthy condition is
    emitted first in each cell because Stage C reuses it.
    """

    require(len(candidates) > 0, "Stage A needs at least one admissible candidate")
    rows: list[LogicalRow] = []
    for peak, ramp in candidates:
        for cell in SCREEN_CELLS:
            identity = stage_ab_identity(cell)
            rows.append(
                LogicalRow(
                    stage=STAGE_A,
                    cell=cell,
                    condition=CONDITION_HEALTHY,
                    severity=None,
                    replicate=None,
                    probe_peak_force_n=float(peak),
                    probe_ramp_fraction_of_duration=float(ramp),
                    identity=identity,
                )
            )
            for severity in STAGE_A_STRUCTURAL_SEVERITIES:
                rows.append(
                    LogicalRow(
                        stage=STAGE_A,
                        cell=cell,
                        condition=CONDITION_STRUCTURAL,
                        severity=float(severity),
                        replicate=None,
                        probe_peak_force_n=float(peak),
                        probe_ramp_fraction_of_duration=float(ramp),
                        identity=identity,
                    )
                )
    return tuple(rows)


def stage_a_origin_row_key(
    *,
    cell: int,
    condition: str,
    severity: float | None,
    selected: tuple[float, float],
) -> tuple[Any, ...]:
    """Return the Stage-A row key a reused row cites.

    Inputs: the cell, the origin condition and severity, and the selected candidate.
    Outputs: the Stage-A row's key. Purpose: a reuse reference is only meaningful if it
    names a row that exists; building it here from the same fields Stage A's builder
    uses is what keeps the two in step.
    """

    require_screen_cell(cell)
    peak, ramp = selected
    return (
        STAGE_A,
        cell,
        condition,
        None if severity is None else float(severity),
        None,
        float(peak),
        float(ramp),
    )


def build_stage_b_inventory(
    selected: tuple[float, float],
) -> tuple[LogicalRow, ...]:
    """Return Stage B's forty logical rows, eight of them reuses.

    Inputs: the selected ``(peak, ramp)`` candidate. Outputs: the ladder rows, cell
    major. Purpose: the ladder is ten remaining-EI values in four cells; the two values
    Stage A already measured at the selected candidate are emitted as citations rather
    than as new requests.
    """

    require_reuse_severities_match_stage_a()
    peak, ramp = selected
    rows: list[LogicalRow] = []
    for cell in SCREEN_CELLS:
        identity = stage_ab_identity(cell)
        for value in LADDER_REMAINING_EI:
            severity = float(value)
            reused_from = None
            if severity in STAGE_B_REUSED_SEVERITIES:
                reused_from = stage_a_origin_row_key(
                    cell=cell,
                    condition=CONDITION_STRUCTURAL,
                    severity=severity,
                    selected=selected,
                )
            rows.append(
                LogicalRow(
                    stage=STAGE_B,
                    cell=cell,
                    condition=CONDITION_STRUCTURAL,
                    severity=severity,
                    replicate=None,
                    probe_peak_force_n=float(peak),
                    probe_ramp_fraction_of_duration=float(ramp),
                    identity=identity,
                    reused_from=reused_from,
                )
            )
    return tuple(rows)


def build_stage_c_inventory(
    selected: tuple[float, float],
) -> tuple[LogicalRow, ...]:
    """Return Stage C's thirty-two logical rows, four of them reuses.

    Inputs: the selected ``(peak, ramp)`` candidate. Outputs: eight healthy replicates
    per cell. Purpose: ``k=0`` *is* the Stage-A healthy identity (I6), so its row is a
    citation of the Stage-A healthy rollout; ``k>=1`` are new bodies that differ only in
    their sensor identity.
    """

    peak, ramp = selected
    rows: list[LogicalRow] = []
    for cell in SCREEN_CELLS:
        for k in range(STAGE_C_REPLICATES):
            identity = stage_c_identity(cell, k)
            reused_from = None
            if k == STAGE_C_REUSED_REPLICATE:
                reused_from = stage_a_origin_row_key(
                    cell=cell,
                    condition=CONDITION_HEALTHY,
                    severity=None,
                    selected=selected,
                )
            rows.append(
                LogicalRow(
                    stage=STAGE_C,
                    cell=cell,
                    condition=CONDITION_HEALTHY,
                    severity=None,
                    replicate=k,
                    probe_peak_force_n=float(peak),
                    probe_ramp_fraction_of_duration=float(ramp),
                    identity=identity,
                    reused_from=reused_from,
                )
            )
    return tuple(rows)


def build_logical_inventory(
    *,
    candidates: Sequence[tuple[float, float]],
    selected: tuple[float, float],
) -> tuple[LogicalRow, ...]:
    """Return the whole pre-registered inventory, Stage A then B then C.

    Inputs: the admissible candidate grid and the selected candidate. Outputs: 180 rows.
    Purpose: assembling the entire plan in one object is what makes the whole-set
    questions -- total cost, stamp collisions, reuse arithmetic -- answerable at all.
    Per-row checks cannot see them.
    """

    require(
        tuple(float(value) for value in selected) in tuple(
            tuple(float(value) for value in candidate) for candidate in candidates
        ),
        f"the selected candidate {selected} is not one of the admissible candidates; a "
        "selection that is not a measured Stage-A candidate is fabricated",
    )
    rows = (
        build_stage_a_inventory(candidates)
        + build_stage_b_inventory(selected)
        + build_stage_c_inventory(selected)
    )
    return rows


def require_inventory_shape(rows: Sequence[LogicalRow]) -> dict[str, Any]:
    """Raise unless the inventory has the pre-registered shape; return its census.

    Inputs: the logical rows. Outputs: a census mapping. Purpose: section 8's 180 and
    section 11's 168 are two statements about one plan, and the twelve-row gap between
    them is load-bearing. This checks the declared reuse set against the set the
    physical keys actually duplicate, which is the only way to catch a reuse that is
    declared but does not collide, or collides but is not declared.
    """

    require(len(rows) > 0, "the inventory is empty")
    row_keys = [row.key for row in rows]
    require(
        len(set(row_keys)) == len(row_keys),
        "logical row keys must be unique; the inventory contains a duplicate row",
    )

    candidate_count = len(
        {
            (row.probe_peak_force_n, row.probe_ramp_fraction_of_duration)
            for row in rows
            if row.stage == STAGE_A
        }
    )
    expected = expected_counts(candidate_count)
    require(
        len(rows) == expected["logical_rows"],
        f"a {candidate_count}-candidate plan declares {expected['logical_rows']} logical "
        f"rows; the inventory has {len(rows)}",
    )

    physical_keys = [row.physical for row in rows]
    distinct_physical = {key: None for key in physical_keys}
    # Reachability, measured by a Session-54 mutation sweep: this check is a **code**
    # guard, not a live one. Once the row keys are unique, the logical count is right,
    # the declared reuse count is right, and the declared reuse set equals the set of
    # rows whose body was already seen, the distinct-body count is forced to
    # logical - reused by arithmetic and cannot disagree. Removing it survives both new
    # test files. It is kept because it states section 11's budget in the census the
    # driver prints, and because it is the check that would still stand if the set
    # comparison below were ever weakened.
    require(
        len(distinct_physical) == expected["physical_rollouts"],
        f"a {candidate_count}-candidate plan budgets {expected['physical_rollouts']} "
        f"Stage-A/B/C rollouts; the inventory resolves to {len(distinct_physical)} "
        "distinct physical bodies",
    )

    declared_reuse = {row.key for row in rows if row.is_reused}
    require(
        len(declared_reuse) == expected["reused_rows"],
        f"exactly {expected['reused_rows']} rows must carry reused_from; "
        f"{len(declared_reuse)} do",
    )

    seen: dict[PhysicalKey, tuple[Any, ...]] = {}
    collided: set[tuple[Any, ...]] = set()
    for row in rows:
        first = seen.get(row.physical)
        if first is None:
            seen[row.physical] = row.key
        else:
            collided.add(row.key)
    require(
        collided == declared_reuse,
        "the declared reuse set and the set of rows whose physical body was already "
        f"measured must be the same set; declared-only {sorted(declared_reuse - collided)}, "
        f"collided-only {sorted(collided - declared_reuse)}",
    )
    require_reuse_references(rows)
    return {
        "logical_rows": len(rows),
        "physical_rollouts": len(distinct_physical),
        "reused_rows": len(declared_reuse),
        "rows_by_stage": {
            stage: sum(1 for row in rows if row.stage == stage) for stage in SCREEN_STAGES
        },
    }


def require_reuse_references(rows: Sequence[LogicalRow]) -> None:
    """Raise unless every reuse cites a Stage-A row with the identical physical body.

    Inputs: the logical rows. Outputs: none. Purpose: a reuse reference that points at a
    row which does not exist, or at one whose body differs, would produce a report that
    looks complete while citing a measurement that was never taken at that body.
    """

    by_key = {row.key: row for row in rows}
    for row in rows:
        if not row.is_reused:
            continue
        require(
            row.reused_from in by_key,
            f"row {row.key} cites reused_from {row.reused_from}, which is not a row of "
            "this inventory",
        )
        origin = by_key[row.reused_from]
        require(
            origin.stage == STAGE_A,
            f"row {row.key} must reuse a Stage-A row; it cites stage {origin.stage!r}",
        )
        require(
            not origin.is_reused,
            f"row {row.key} cites {origin.key}, which is itself a reuse; a citation "
            "chain would leave no row that actually ran",
        )
        require(
            origin.physical == row.physical,
            f"row {row.key} cites {origin.key}, whose physical body "
            f"{origin.physical} differs from its own {row.physical}",
        )


def resolve_row_provenance(
    ledger: ResultsLedger, row: LogicalRow
) -> tuple[str, str, str]:
    """Return ``(provenance_hash, canonical_payload, stage_of_origin)`` for one row.

    Inputs: the physical ledger and one logical row. Outputs: the origin's stamp, the
    exact canonical string it was hashed from, and the stage that actually ran. Purpose:
    this is the single read path for a row's provenance, so a reused row cannot acquire
    one by any other route. For a reused row it additionally refuses a payload whose
    recorded ``stage_of_origin`` is not Stage A -- which is what "never relabel an origin
    canonical payload" means when checked rather than intended.
    """

    result = ledger.get(row.physical)
    if row.is_reused:
        require(
            result.stage_of_origin == STAGE_A,
            f"row {row.key} reuses a measurement whose recorded stage of origin is "
            f"{result.stage_of_origin!r}; a reused row must cite a Stage-A rollout",
        )
        require(
            result.origin_row_key == row.reused_from,
            f"row {row.key} cites {row.reused_from} but the ledger entry for its body "
            f"was produced by {result.origin_row_key}",
        )
    else:
        require(
            result.origin_row_key == row.key,
            f"row {row.key} is not a reuse, so the ledger entry for its body must have "
            f"been produced by it; it was produced by {result.origin_row_key}",
        )
        require(
            result.stage_of_origin == row.stage,
            f"row {row.key} is not a reuse, so its stage of origin must be its own "
            f"stage; the ledger records {result.stage_of_origin!r}",
        )
    return result.provenance_hash, result.canonical_payload, result.stage_of_origin


def require_physical_ledger_complete(
    ledger: ResultsLedger, rows: Sequence[LogicalRow]
) -> dict[str, Any]:
    """Raise unless the ledger holds exactly one entry per distinct body in ``rows``.

    Inputs: the ledger and the logical inventory. Outputs: a census mapping. Purpose: the
    two failure directions are different defects -- a missing entry means a row will be
    reported from a measurement that was never taken, and a surplus entry means a rollout
    was spent that the plan does not account for. Both are named separately so the
    message says which happened.
    """

    wanted = {row.physical for row in rows}
    held = set(ledger.keys)
    missing = wanted - held
    surplus = held - wanted
    require(not missing, f"the ledger is missing {len(missing)} physical result(s): {sorted(missing)[:3]}")
    require(not surplus, f"the ledger holds {len(surplus)} unplanned physical result(s): {sorted(surplus)[:3]}")
    require(
        len(ledger.stamps) == len(held),
        f"the ledger holds {len(held)} bodies and {len(ledger.stamps)} stamps; the two "
        "must be a bijection",
    )
    return {"physical_results": len(held), "distinct_stamps": len(set(ledger.stamps))}


def require_results_only_root(root: Path) -> dict[str, Any]:
    """Raise unless everything under ``root`` is a results artifact; return its census.

    Inputs: the driver's output root. Outputs: a mapping naming what was inspected.
    Purpose: section 9's label-stamp scope condition is non-blocking only if the
    implementation persists no screen ``ObservedRecord``, label payload, manifest or role
    index. That is a property of the directory, not of the code, so it is checked by
    looking at the directory -- which is the only form of the check that can fail on a
    real wrong write.

    The check is an allowlist, not a blocklist: an unexpected suffix is refused even if
    it is not one of the named dataset-role artifacts, because the failure mode is a
    write nobody anticipated.
    """

    require(isinstance(root, Path), f"the results root must be a Path; got {type(root)!r}")
    require(root.exists(), f"the results root {root} does not exist")
    require(root.is_dir(), f"the results root {root} is not a directory")

    inspected: list[str] = []
    for path in sorted(root.rglob("*")):
        relative = path.relative_to(root).as_posix()
        if path.is_dir():
            require(
                path.name not in FORBIDDEN_ROOT_DIRECTORY_NAMES,
                f"the results root holds a dataset-role directory {relative!r}; the "
                "screen persists results only",
            )
            continue
        inspected.append(relative)
        require(
            path.name not in FORBIDDEN_ROOT_FILE_NAMES,
            f"the results root holds a dataset-role artifact {relative!r}; the screen "
            "persists results only",
        )
        require(
            path.suffix in ALLOWED_RESULT_SUFFIXES,
            f"the results root holds {relative!r}, whose suffix {path.suffix!r} is not "
            f"one of the permitted result suffixes {ALLOWED_RESULT_SUFFIXES}",
        )
    require(
        inspected,
        f"the results root {root} holds no result file; a screen that wrote nothing "
        "cannot be reported as having persisted its results",
    )
    return {"root": str(root), "files": tuple(inspected)}


def logical_row_report(
    ledger: ResultsLedger, row: LogicalRow
) -> dict[str, Any]:
    """Return one serialisable report row, provenance resolved through the ledger.

    Inputs: the ledger and one logical row. Outputs: a JSON-ready mapping. Purpose: the
    reported object carries the consumer stage and the physical origin separately, so a
    reader can tell a measured row from a cited one without recomputing anything.
    """

    provenance, canonical, stage_of_origin = resolve_row_provenance(ledger, row)
    result = ledger.get(row.physical)
    return {
        "stage": row.stage,
        "cell": row.cell,
        "condition": row.condition,
        "severity": row.severity,
        "replicate": row.replicate,
        "probe_peak_force_n": row.probe_peak_force_n,
        "probe_ramp_fraction_of_duration": row.probe_ramp_fraction_of_duration,
        "sensor_seed": row.identity.sensor_seed,
        "realized_pair_id": row.identity.pair_id,
        "reused_from": None if row.reused_from is None else list(row.reused_from),
        "stage_of_origin": stage_of_origin,
        "rollout_provenance": provenance,
        "rollout_canonical": canonical,
        "coefficients": list(result.coefficients),
    }


def census(rows: Sequence[LogicalRow]) -> dict[str, Any]:
    """Return a small human-readable census of an inventory.

    Inputs: the logical rows. Outputs: counts by stage, reuse and physical body.
    Purpose: the driver prints this before it runs anything, so the plan's cost is
    visible before it is spent rather than after.
    """

    return {
        "logical_rows": len(rows),
        "physical_rollouts": len({row.physical for row in rows}),
        "reused_rows": sum(1 for row in rows if row.is_reused),
        "rows_by_stage": {
            stage: sum(1 for row in rows if row.stage == stage) for stage in SCREEN_STAGES
        },
    }


def iter_new_rows(rows: Iterable[LogicalRow]) -> tuple[LogicalRow, ...]:
    """Return the rows that must actually execute, in inventory order.

    Inputs: the logical rows. Outputs: the non-reused rows. Purpose: the driver iterates
    this rather than filtering inline, so "which rows run" has one definition and the
    reuse rule cannot be half-applied at one of two call sites.
    """

    return tuple(row for row in rows if not row.is_reused)


__all__ = [
    "ALLOWED_RESULT_SUFFIXES",
    "EXPECTED_LOGICAL_ROWS",
    "EXPECTED_PHYSICAL_ROLLOUTS",
    "EXPECTED_REUSED_ROWS",
    "PRE_REGISTERED_CANDIDATE_COUNT",
    "FORBIDDEN_ROOT_DIRECTORY_NAMES",
    "FORBIDDEN_ROOT_FILE_NAMES",
    "LogicalRow",
    "PhysicalKey",
    "PhysicalResult",
    "ProtocolPError",
    "ResultsLedger",
    "STAGE_A",
    "STAGE_B",
    "STAGE_B_REUSED_SEVERITIES",
    "STAGE_C",
    "STAGE_C_REUSED_REPLICATE",
    "build_logical_inventory",
    "build_stage_a_inventory",
    "build_stage_b_inventory",
    "build_stage_c_inventory",
    "census",
    "expected_counts",
    "iter_new_rows",
    "logical_row_report",
    "physical_key",
    "require_inventory_shape",
    "require_physical_ledger_complete",
    "require_results_only_root",
    "require_reuse_references",
    "require_reuse_severities_match_stage_a",
    "resolve_row_provenance",
    "stage_a_origin_row_key",
]
