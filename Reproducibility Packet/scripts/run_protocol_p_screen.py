"""Protocol P Stages A, B and C -- the screen driver.

What this script is
-------------------
Protocol P sections 8 and 9 declare a three-stage development screen: Stage A measures
nine admissible probe candidates in four context cells under three conditions and
selects one; Stage B walks the ten-value remaining-EI ladder at the selected candidate;
Stage C builds the operative null from eight healthy replicates per cell.  This script
is the executable form of that plan.

It is deliberately split from the two layers beneath it:

* ``utils/protocol_p_conditions.py`` builds each rollout's request and refuses a wrong
  one *before* it runs (I3-I8, I13a);
* ``utils/protocol_p_results.py`` carries the 180-logical / 168-physical distinction and
  the origin-provenance rule for the twelve reused rows;
* this driver owns everything that can only be known once a rollout has returned --
  the window (I9), the measurement-time shape (I10), the fit's sample count (I11), the
  hard safety gates (I12) -- plus the results-only output root.

Two things this driver derives rather than carries
--------------------------------------------------
**The fault onset.** ``requested_fault_specs`` takes ``onset_index`` as a parameter and
the screen's source setting is ``fault_dev_healthy``, so ``_fault_components`` derives
nothing for us.  The driver reads ``onset_time_s`` from the bound trajectory and
converts it with the generator's own ``_step_index``, then asserts equality with the
value it passes.  A hard-coded 500 would be numerically right today and would be the
Session-41 defect wearing a correct value: Correction 1 exists because a missing onset
made a step-0 and a step-500 structural request indistinguishable.

**The window origin.** Section 8 pins ``w0 = round((onset_time_s + start_offset_s) /
control_dt_s)`` and nothing in the codebase fixes it -- ``window_tensor`` refuses a full
run and right-aligns, so the caller owns the origin.  The driver derives it through the
same off-grid-refusing helper and checks ``w1 <= n_steps`` (I9).

The reuse rule, in one line
---------------------------
Twelve of the 180 logical rows consume a measurement an earlier row paid for.  They cite
the origin's provenance hash and canonical payload verbatim and never call the
construction layer.  See ``utils/protocol_p_results.py`` for why, and Codex Session 53
for the ruling.

Execution authority
-------------------
``--mode plan`` (the default) builds and audits the entire inventory, verifies every
pin, derives the timing, and exits **having run zero rollouts**.  ``--mode execute``
runs the screen.  The default is the cheap one on purpose: at the time this script was
written, implementation was authorized and execution was not, and a CLI whose default
spends 169 rollouts is one keystroke away from spending them.
"""

from __future__ import annotations

import argparse
import dataclasses
import json
import sys
import time
from collections.abc import Mapping, Sequence
from pathlib import Path
from typing import Any, Callable

import numpy as np

SCRIPT_DIR = Path(__file__).resolve().parent
if str(SCRIPT_DIR) not in sys.path:
    sys.path.insert(0, str(SCRIPT_DIR))

from analyze_synchronous_difference_null import (  # noqa: E402
    coefficient_vector,
    sensor_config_from_document,
    verify_text_pins,
)
from utils.assignment_binding import validate_approved_assignment_binding  # noqa: E402
from utils.assignment_generator import (  # noqa: E402
    AssignmentGenerationError,
    _generate_reservation,
    _runtime_parameters,
    _step_index,
    build_identity_manifest,
)
from utils.cable_mechanics import CableModelConfig  # noqa: E402
from utils.config_contract import load_config  # noqa: E402
from utils.gate3_assignment import load_assignment  # noqa: E402
from utils.protocol_p import (  # noqa: E402
    ASSIGNMENT_FILENAME,
    PROTOCOL_CANONICAL_SHA256,
    PROTOCOL_FILENAME,
    ProtocolPError,
)
from utils.protocol_p import require as _require  # noqa: E402
from utils.protocol_p_conditions import (  # noqa: E402
    CONDITION_HEALTHY,
    CONDITION_STRUCTURAL,
    LADDER_REMAINING_EI,
    PINNED_LINK_LENGTH_M,
    PINNED_TORQUE_ABS_LIMIT_N_M,
    RolloutIdentity,
    SCREEN_CELLS,
    SCREEN_SOURCE_FAULT_SETTING_ID,
    SCREEN_SPLIT,
    SCREEN_TRAJECTORY_SPEC_ID,
    STAGE_A_STRUCTURAL_SEVERITIES,
    STAGE_C_REPLICATES,
    admissible_candidates,
    build_overrides,
    require_matched_identity,
    require_screen_cell,
    require_torque_gate_constants,
    screen_reservation,
    stage_ab_identity,
    stage_c_identity,
    torque_gate_admits,
)
from utils.protocol_p_results import (  # noqa: E402
    LogicalRow,
    PhysicalResult,
    ResultsLedger,
    STAGE_A,
    STAGE_B,
    STAGE_C,
    build_logical_inventory,
    census,
    iter_new_rows,
    logical_row_report,
    physical_key,
    require_inventory_shape,
    require_physical_ledger_complete,
    require_results_only_root,
    resolve_row_provenance,
)
from utils.schema_types import N_GAUGES, PrivilegedRecord  # noqa: E402
from utils.sensor_model import SensorModel  # noqa: E402
from utils.task_control import ObservedJointPDController  # noqa: E402

PACKET_ROOT = SCRIPT_DIR.parent

# ---------------------------------------------------------------------------
# Pins.  Every value below is pre-registered in Protocol P section 8 or section 9.
# ---------------------------------------------------------------------------

OUTPUT_FILENAME = "stage_abc_screen.json"

# Section 4: the closed loop is driven by a C0 session and S is produced from the
# privileged record afterwards.  ``_generate_reservation`` is asked for S only.
SCREEN_SUITE = "S"

# Section 8's window.  768 is also ``values.timing.window_steps`` in the bound draft
# config; the two are reconciled by EQUALITY in :func:`derive_screen_timing`, never by
# this module adopting the document's value.
WINDOW_STEPS = 768
DIAGNOSTIC_HZ = 0.8

# Section 8's hard gates, all computed from the returned PrivilegedRecord.
MAX_ABS_JOINT_RATE_RAD_S = 8.0
MAX_ABS_JOINT_ANGLE_RAD = 2.5
MAX_ABS_GAUGE_MICROSTRAIN = 400.0
# "no increase in saturated steps against zero probe amplitude (baseline 0)": the
# baseline count at zero probe amplitude is zero, so the admissible count is zero.
SATURATED_STEP_BASELINE = 0
SAFETY_FLAG_BUDGET = 0

# Section 8's selection rule.
SELECTION_SEVERITY = 0.75
SELECTION_TIE_TOLERANCE = 0.01

# Section 8, Stage C.
STAGE_C_QUANTILE = 0.95
STAGE_C_QUANTILE_METHOD = "higher"
OPERATIVE_NULL_MULTIPLIER = 2.0
# Section 8: "Q95_c >= 0.30 triggers a diagnostic pause only."
STAGE_C_DIAGNOSTIC_PAUSE_Q95 = 0.30

TERMINAL_NO_ADMISSIBLE_PROBE = "NO_ADMISSIBLE_PROBE"
VERDICT_TESTABLE = "TESTABLE"
VERDICT_SUB_THRESHOLD = "SUB_THRESHOLD"


@dataclasses.dataclass(frozen=True)
class ScreenTiming:
    """The screen's derived time grid: onset, window, and where both came from.

    Every field is derived from the bound assignment and the bound control timestep.
    Nothing here is a literal, which is the point: a literal that is correct today is
    indistinguishable from a literal that stopped being correct.
    """

    control_dt_s: float
    onset_time_s: float
    probe_start_offset_s: float
    onset_index: int
    w0: int
    w1: int


def bound_trajectory(assignment: Mapping[str, Any]) -> Mapping[str, Any]:
    """Return the screened trajectory specification from the approved assignment.

    Inputs: the approved assignment document. Outputs: the ``trajectory_dev_diagnostic_b``
    specification. Purpose: ``assignment["trajectory_specs"]`` is a *list* of dicts keyed
    by ``"id"``, not a mapping, and indexing it as a mapping is a mistake that has been
    made in this project before. Exactly one match is required.
    """

    specs = assignment.get("trajectory_specs")
    _require(
        isinstance(specs, Sequence) and not isinstance(specs, (str, bytes)),
        "assignment['trajectory_specs'] must be a list of specifications",
    )
    matched = [
        spec
        for spec in specs
        if isinstance(spec, Mapping) and spec.get("id") == SCREEN_TRAJECTORY_SPEC_ID
    ]
    _require(
        len(matched) == 1,
        f"expected exactly one {SCREEN_TRAJECTORY_SPEC_ID!r} trajectory spec, found "
        f"{len(matched)}",
    )
    spec = matched[0]
    _require(
        spec.get("split") == SCREEN_SPLIT,
        f"the screened trajectory must belong to the {SCREEN_SPLIT!r} split; got "
        f"{spec.get('split')!r}",
    )
    return spec


def derive_screen_timing(
    assignment: Mapping[str, Any], *, control_dt_s: float, window_steps: int
) -> ScreenTiming:
    """Derive the fault onset and the section-8 window from the bound documents.

    Inputs: the approved assignment, the bound control timestep, and the bound window
    length. Outputs: the derived :class:`ScreenTiming`. Purpose: both the onset index and
    the window origin are grid conversions the driver owns, and both must refuse an
    off-grid time rather than round it away -- ``_step_index`` raises on a mismatch
    larger than 1e-9, which is what makes an assignment edit fail loudly here instead of
    shifting the measurement silently.

    ``window_steps`` is checked against section 8's pinned 768 by equality; the bound
    document's value is not adopted.
    """

    _require(
        int(window_steps) == WINDOW_STEPS,
        f"the bound config's window_steps is {window_steps}; section 8's window is "
        f"pinned at {WINDOW_STEPS}",
    )
    spec = bound_trajectory(assignment)
    onset_time_s = float(spec["onset_time_s"])
    probe = spec.get("diagnostic_probe")
    _require(
        isinstance(probe, Mapping),
        f"{SCREEN_TRAJECTORY_SPEC_ID!r} must carry a diagnostic probe; the probe-free "
        "ordinary trajectory is the pre-registered negative control and is never screened",
    )
    start_offset_s = float(probe["start_offset_s"])

    # ``_step_index`` refuses an off-grid time. The two conversions are wrapped
    # separately so the message says which one drifted: an off-grid onset moves the
    # fault, an off-grid window origin moves the measurement, and they are different
    # defects with different consequences.
    try:
        onset_index = _step_index(onset_time_s, control_dt_s)
    except AssignmentGenerationError as error:
        raise ProtocolPError(f"I13a: the derived fault onset is off-grid: {error}") from error
    try:
        w0 = _step_index(onset_time_s + start_offset_s, control_dt_s)
    except AssignmentGenerationError as error:
        raise ProtocolPError(f"I9: the derived window origin is off-grid: {error}") from error
    return ScreenTiming(
        control_dt_s=float(control_dt_s),
        onset_time_s=onset_time_s,
        probe_start_offset_s=start_offset_s,
        onset_index=int(onset_index),
        w0=int(w0),
        w1=int(w0) + WINDOW_STEPS,
    )


def require_derived_onset(passed_onset_index: int, timing: ScreenTiming) -> None:
    """Raise unless the onset a rollout is being built with is the derived one.

    Inputs: the onset index about to be passed into the construction layer, and the
    derived timing. Outputs: none. Purpose: deriving a value and then passing a different
    one is a two-line defect that no construction check can see, because the construction
    layer validates whatever onset it is given. The equality assertion is what closes the
    gap between the derivation and the call.
    """

    _require(
        isinstance(passed_onset_index, int) and not isinstance(passed_onset_index, bool),
        f"the onset index must be an int; got {passed_onset_index!r}",
    )
    _require(
        passed_onset_index == timing.onset_index,
        f"the onset index passed to the construction layer is {passed_onset_index}; the "
        f"onset derived from {SCREEN_TRAJECTORY_SPEC_ID!r} "
        f"(onset_time_s={timing.onset_time_s}, control_dt_s={timing.control_dt_s}) is "
        f"{timing.onset_index}",
    )


def require_window_on_grid(timing: ScreenTiming, n_steps: int) -> None:
    """I9: raise unless the derived window fits inside the rollout.

    Inputs: the derived timing and the returned rollout's step count. Outputs: none.
    Purpose: ``w1 > n_steps`` would silently produce a short window whose harmonic fit
    still succeeds, which is the failure mode section 8 names explicitly.
    """

    _require(timing.w0 >= 0, f"I9: window origin {timing.w0} is negative")
    _require(
        timing.w1 <= int(n_steps),
        f"I9: window [{timing.w0}, {timing.w1}) does not fit a {n_steps}-step rollout",
    )


def gauge_window_from_observation(
    observation: Any, timing: ScreenTiming
) -> tuple[np.ndarray, np.ndarray, np.ndarray]:
    """Slice one observed record's gauge channel to the section-8 window.

    Inputs: an ``ObservedRecord`` for suite ``S`` and the derived timing. Outputs:
    ``(values, valid, t_g)`` over ``[w0, w1)``. Purpose: this is where I10 lives --
    ``measurement_time_s['gauge_obs']`` is checked with an explicit if / elif / else so
    an unexpected rank raises instead of broadcasting into a plausible-looking fit.
    """

    values = np.asarray(observation.values["gauge_obs"], dtype=float)
    valid = np.asarray(observation.valid_mask["gauge_obs"], dtype=bool)
    tm = np.asarray(observation.measurement_time_s["gauge_obs"], dtype=float)

    if tm.ndim == 1:
        t_g = tm
    elif tm.ndim == 2 and tm.shape[1] == 1:
        t_g = tm[:, 0]
    else:
        raise ProtocolPError(
            f"I10: measurement_time_s['gauge_obs'] must be [T] or [T,1]; got {tm.shape}"
        )

    _require(
        values.ndim == 2 and values.shape[1] == N_GAUGES,
        f"I10: gauge_obs must be [T, {N_GAUGES}]; got {values.shape}",
    )
    _require(
        valid.shape == values.shape,
        f"I10: gauge validity {valid.shape} must match gauge values {values.shape}",
    )
    _require(
        t_g.shape[0] == values.shape[0] == valid.shape[0],
        f"I10: measurement time length {t_g.shape[0]} must equal the gauge trace length "
        f"{values.shape[0]}",
    )
    require_window_on_grid(timing, values.shape[0])
    window = slice(timing.w0, timing.w1)
    return values[window, :], valid[window, :], t_g[window]


def observation_coefficients(observation: Any, timing: ScreenTiming) -> tuple[float, ...]:
    """Return one rollout's eight-entry gauge harmonic vector.

    Inputs: an observed record and the derived timing. Outputs: the ``[8]`` vector as a
    tuple of floats. Purpose: the per-gauge stack is section 8's building block and is
    imported from the Stage-0 script rather than re-implemented, so the protocol's
    statistic has exactly one definition in the packet. I11 (at least five finite valid
    samples) is enforced inside ``harmonic_coefficients`` and fails loudly there.
    """

    values, valid, t_g = gauge_window_from_observation(observation, timing)
    vector = coefficient_vector(values, valid, t_g, DIAGNOSTIC_HZ)
    return tuple(float(entry) for entry in np.asarray(vector, dtype=float))


def difference_statistic(
    fault: Sequence[float], healthy: Sequence[float]
) -> float:
    """Return ``D = || b(fault) - b(healthy) ||_2`` over the eight-entry vectors.

    Inputs: the two coefficient vectors. Outputs: the scalar distance. Purpose: section
    8's statistic, kept as a named function so every stage computes it the same way and
    a reader can find the one place it is defined.
    """

    left = np.asarray(fault, dtype=float)
    right = np.asarray(healthy, dtype=float)
    _require(
        left.shape == right.shape == (2 * N_GAUGES,),
        f"the statistic is over two [{2 * N_GAUGES}] vectors; got {left.shape} and "
        f"{right.shape}",
    )
    _require(
        bool(np.all(np.isfinite(left))) and bool(np.all(np.isfinite(right))),
        "the statistic requires finite coefficient vectors; a non-finite entry means the "
        "harmonic fit did not converge and must not be reduced to a distance",
    )
    return float(np.linalg.norm(left - right))


@dataclasses.dataclass(frozen=True)
class GateReport:
    """One rollout's I12 hard-gate measurements, kept whether or not they passed."""

    safety_events: int
    max_abs_q_true: float
    max_abs_qd_true: float
    max_abs_gauge_true: float
    saturated_steps: int
    contact_steps: int
    passed: bool
    failures: tuple[str, ...]


def evaluate_hard_gates(
    record: PrivilegedRecord, *, safety_events: int, contact_steps: int
) -> GateReport:
    """I12: measure section 8's hard gates on one returned privileged record.

    Inputs: the returned ``PrivilegedRecord`` and the generator's own safety/contact
    counts. Outputs: a :class:`GateReport` carrying every measured value and the list of
    failures. Purpose: the gates are *measured* rather than raised on, because Stage A
    drops a failing candidate and continues -- a raise would end the screen on the first
    inadmissible candidate, which is not what section 8 says to do. The values are kept
    for passing rollouts too, so the report can show the margins rather than assert them.

    Section 41's finding is why this is not the construction check: these gates passed
    with roughly 70x margin under a defect that changed which body was being measured. A
    gate on the result cannot see the construction; ``I13a`` is what does.
    """

    failures: list[str] = []
    safety_flag = np.asarray(record.safety_flag, dtype=bool)
    flagged = int(np.count_nonzero(safety_flag))
    if flagged > SAFETY_FLAG_BUDGET:
        failures.append(f"safety_flag set on {flagged} entries (budget {SAFETY_FLAG_BUDGET})")
    if int(safety_events) > SAFETY_FLAG_BUDGET:
        failures.append(
            f"the generator counted {safety_events} safety events (budget "
            f"{SAFETY_FLAG_BUDGET})"
        )

    max_q = float(np.max(np.abs(np.asarray(record.q_true, dtype=float))))
    if not max_q <= MAX_ABS_JOINT_ANGLE_RAD:
        failures.append(f"max|q_true| {max_q} exceeds {MAX_ABS_JOINT_ANGLE_RAD}")

    max_qd = float(np.max(np.abs(np.asarray(record.qd_true, dtype=float))))
    if not max_qd <= MAX_ABS_JOINT_RATE_RAD_S:
        failures.append(f"max|qd_true| {max_qd} exceeds {MAX_ABS_JOINT_RATE_RAD_S}")

    max_gauge = float(np.max(np.abs(np.asarray(record.gauge_true, dtype=float))))
    if not max_gauge <= MAX_ABS_GAUGE_MICROSTRAIN:
        failures.append(
            f"max|gauge_true| {max_gauge} microstrain exceeds {MAX_ABS_GAUGE_MICROSTRAIN}"
        )

    saturated = int(
        np.count_nonzero(np.any(np.asarray(record.saturation_flag, dtype=bool), axis=1))
    )
    if saturated > SATURATED_STEP_BASELINE:
        failures.append(
            f"{saturated} saturated steps against the zero-probe baseline of "
            f"{SATURATED_STEP_BASELINE}"
        )

    return GateReport(
        safety_events=int(safety_events),
        max_abs_q_true=max_q,
        max_abs_qd_true=max_qd,
        max_abs_gauge_true=max_gauge,
        saturated_steps=saturated,
        contact_steps=int(contact_steps),
        passed=not failures,
        failures=tuple(failures),
    )


def require_probe_torque_gate(peak_force_n: float) -> None:
    """Raise unless a probe amplitude clears section 8's inclusive torque gate.

    Inputs: the probe's peak force. Outputs: none. Purpose: the torque gate is both a
    pre-simulation candidate filter and one of the per-rollout hard gates; it appears
    here so the second reading is a real check rather than an assumption inherited from
    the first.
    """

    _require(
        torque_gate_admits(peak_force_n),
        f"the torque gate refuses a probe peak of {peak_force_n} N: "
        f"{peak_force_n} * 2 * {PINNED_LINK_LENGTH_M} exceeds 0.60 * "
        f"{PINNED_TORQUE_ABS_LIMIT_N_M}",
    )


@dataclasses.dataclass(frozen=True)
class RolloutOutcome:
    """What one executed rollout returns to the driver.

    Deliberately narrow: the label payload the generator also returns is *not* carried,
    because section 9's label-stamp scope condition is only non-blocking while no screen
    label payload is persisted, and the cheapest way to guarantee that is to never hold
    one.
    """

    control_pair_id: str
    plant: PrivilegedRecord
    observation: Any
    safety_events: int
    contact_steps: int
    elapsed_s: float


def execute_rollout(
    *,
    assignment: Mapping[str, Any],
    base_config_hash: str,
    runtime: Any,
    history_steps: int,
    reservation: Any,
    overrides: Any,
) -> RolloutOutcome:
    """Run one screen rollout through the section-4 construction path.

    Inputs: the approved assignment, the base configuration hash, the runtime parameters,
    the history length, the derived screen reservation and its override bundle. Outputs:
    the :class:`RolloutOutcome`. Purpose: this is the single place the driver touches the
    generator, which is what makes "did a reused row call the generator?" a countable
    question. Only suite ``S`` is requested; the closed loop is still driven by a ``C0``
    session inside ``_generate_reservation`` (section 4).

    The returned label payload is discarded here rather than downstream, so no call site
    can accidentally persist it.
    """

    started = time.perf_counter()
    (
        control_pair_id,
        plant_record,
        observations,
        _label_payload,
        safety_events,
        contact_steps,
    ) = _generate_reservation(
        assignment,
        base_config_hash,
        (SCREEN_SUITE,),
        None,
        history_steps,
        runtime,
        reservation,
        overrides=overrides,
    )
    elapsed_s = time.perf_counter() - started
    _require(
        set(observations) == {SCREEN_SUITE},
        f"expected only the {SCREEN_SUITE!r} observation; got {sorted(observations)}",
    )
    return RolloutOutcome(
        control_pair_id=str(control_pair_id),
        plant=plant_record,
        observation=observations[SCREEN_SUITE],
        safety_events=int(safety_events),
        contact_steps=int(contact_steps),
        elapsed_s=float(elapsed_s),
    )


ExecuteRollout = Callable[..., RolloutOutcome]


@dataclasses.dataclass
class ScreenContext:
    """Everything a row needs in order to run, resolved once before any rollout."""

    assignment: Mapping[str, Any]
    base_config_hash: str
    assignment_canonical_sha256: str
    assignment_hash: str
    protocol_spec_sha256: str
    runtime: Any
    history_steps: int
    timing: ScreenTiming
    sources: Mapping[int, Any]
    sensor_config: Any


def screen_sources(binding: Any) -> dict[int, Any]:
    """Return the delivered source reservation for each screened context cell.

    Inputs: the validated assignment binding. Outputs: ``cell -> ScenarioReservation``.
    Purpose: the driver **obtains** its sources from the I1-pinned assignment document
    and never constructs one. That is what binds the physical body: the construction
    layer's cell check is over three identifier strings, and it is the assignment's bytes
    plus its context-cell rotation that make those strings mean a payload, an environment
    and a contact profile.
    """

    _, reservations = build_identity_manifest(binding, splits=(SCREEN_SPLIT,))
    sources: dict[int, Any] = {}
    for cell in SCREEN_CELLS:
        require_screen_cell(cell)
        replicate = cell - SCREEN_CELLS[0]
        expected = f"scenario_{SCREEN_SPLIT}_t01_f000_r{replicate:02d}"
        matched = [item for item in reservations if item.scenario_spec_id == expected]
        _require(
            len(matched) == 1,
            f"expected exactly one delivered reservation {expected!r} for cell {cell}; "
            f"found {len(matched)}",
        )
        source = matched[0]
        _require(
            source.fault_setting_id == SCREEN_SOURCE_FAULT_SETTING_ID,
            f"cell {cell}'s source must be the healthy setting "
            f"{SCREEN_SOURCE_FAULT_SETTING_ID!r}; got {source.fault_setting_id!r}",
        )
        sources[cell] = source
    return sources


def run_logical_row(
    row: LogicalRow,
    context: ScreenContext,
    ledger: ResultsLedger,
    *,
    execute: ExecuteRollout,
    retain_plant: bool = False,
) -> tuple[PhysicalResult, PrivilegedRecord | None]:
    """Construct, run and record one non-reused logical row.

    Inputs: the row, the resolved context, the ledger, the executor, and whether to hand
    the privileged record back. Outputs: the recorded :class:`PhysicalResult` and,
    optionally, the plant trace. Purpose: this is the only path by which a provenance
    stamp is minted, which is what makes the reuse rule enforceable -- a reused row does
    not reach this function, and the driver's tests count that rather than trust it.

    Raises ``ProtocolPError`` if called with a reused row.
    """

    _require(
        not row.is_reused,
        f"row {row.key} is a reuse and must cite its origin rather than run; minting a "
        "stamp for it would record a hash no artifact carries",
    )
    require_derived_onset(context.timing.onset_index, context.timing)
    require_probe_torque_gate(row.probe_peak_force_n)

    source = context.sources[row.cell]
    reservation = screen_reservation(
        source,
        cell=row.cell,
        sensor_seed=row.identity.sensor_seed,
        base_pair_id=row.identity.pair_id,
    )
    overrides, canonical = build_overrides(
        stage=row.stage,
        cell=row.cell,
        condition=row.condition,
        severity=row.severity,
        identity=row.identity,
        reservation=reservation,
        probe_peak_force_n=row.probe_peak_force_n,
        probe_ramp_fraction_of_duration=row.probe_ramp_fraction_of_duration,
        onset_index=context.timing.onset_index,
        base_config_hash=context.base_config_hash,
        assignment_canonical_sha256=context.assignment_canonical_sha256,
        assignment_hash=context.assignment_hash,
        protocol_spec_sha256=context.protocol_spec_sha256,
    )
    outcome = execute(
        assignment=context.assignment,
        base_config_hash=context.base_config_hash,
        runtime=context.runtime,
        history_steps=context.history_steps,
        reservation=reservation,
        overrides=overrides,
    )
    _require(
        outcome.control_pair_id == row.identity.pair_id,
        f"the rollout realized pair id {outcome.control_pair_id!r} is not the row's "
        f"identity {row.identity.pair_id!r}",
    )
    gates = evaluate_hard_gates(
        outcome.plant,
        safety_events=outcome.safety_events,
        contact_steps=outcome.contact_steps,
    )
    coefficients = observation_coefficients(outcome.observation, context.timing)
    result = PhysicalResult(
        key=row.physical,
        origin_row_key=row.key,
        stage_of_origin=row.stage,
        cell=row.cell,
        provenance_hash=str(overrides.provenance_hash),
        canonical_payload=canonical,
        coefficients=coefficients,
        gate_report=dataclasses.asdict(gates),
        n_steps=int(outcome.plant.n_steps),
        elapsed_s=outcome.elapsed_s,
    )
    ledger.record(result, base_config_hash=context.base_config_hash)
    return result, (outcome.plant if retain_plant else None)


def stage_a_rows_for_candidate(
    rows: Sequence[LogicalRow], candidate: tuple[float, float]
) -> tuple[LogicalRow, ...]:
    """Return the Stage-A rows belonging to one candidate, in inventory order."""

    peak, ramp = float(candidate[0]), float(candidate[1])
    return tuple(
        row
        for row in rows
        if row.stage == STAGE_A
        and row.probe_peak_force_n == peak
        and row.probe_ramp_fraction_of_duration == ramp
    )


def run_stage_a(
    rows: Sequence[LogicalRow],
    candidates: Sequence[tuple[float, float]],
    context: ScreenContext,
    ledger: ResultsLedger,
    *,
    execute: ExecuteRollout,
) -> dict[str, Any]:
    """Run Stage A candidate by candidate, dropping any candidate that fails a gate.

    Inputs: the full inventory, the admissible candidates, the context, the ledger and
    the executor. Outputs: a mapping of surviving candidates, drops with reasons, and the
    per-candidate worst-cell statistic at the selection severity. Purpose: section 8 says
    a failing candidate is dropped, its remaining cells skipped, and the drop count
    logged -- so the loop is candidate-major and a gate failure breaks out of that
    candidate rather than out of the stage.
    """

    survivors: list[tuple[float, float]] = []
    drops: list[dict[str, Any]] = []
    retained_healthy: dict[tuple[float, float, int], PrivilegedRecord] = {}

    for candidate in candidates:
        candidate_rows = stage_a_rows_for_candidate(rows, candidate)
        _require(
            len(candidate_rows) == len(SCREEN_CELLS) * (1 + len(STAGE_A_STRUCTURAL_SEVERITIES)),
            f"candidate {candidate} has {len(candidate_rows)} Stage-A rows; each candidate "
            f"must have {len(SCREEN_CELLS) * (1 + len(STAGE_A_STRUCTURAL_SEVERITIES))}",
        )
        dropped: dict[str, Any] | None = None
        for row in candidate_rows:
            result, plant = run_logical_row(
                row,
                context,
                ledger,
                execute=execute,
                retain_plant=row.condition == CONDITION_HEALTHY,
            )
            if plant is not None:
                retained_healthy[(float(candidate[0]), float(candidate[1]), row.cell)] = plant
            if not result.gate_report["passed"]:
                dropped = {
                    "candidate": [float(candidate[0]), float(candidate[1])],
                    "cell": row.cell,
                    "condition": row.condition,
                    "severity": row.severity,
                    "failures": list(result.gate_report["failures"]),
                }
                break
        if dropped is None:
            survivors.append((float(candidate[0]), float(candidate[1])))
        else:
            drops.append(dropped)

    return {
        "survivors": tuple(survivors),
        "drops": drops,
        "drop_count": len(drops),
        "retained_healthy_plants": retained_healthy,
    }


def worst_cell_statistic(
    ledger: ResultsLedger,
    candidate: tuple[float, float],
    *,
    severity: float,
) -> float:
    """Return ``min_c D(candidate, c)`` at one structural severity.

    Inputs: the ledger, a candidate and the severity to evaluate at. Outputs: the
    worst-cell distance. Purpose: selection maximises the *worst* cell, not the mean --
    section 9's aggregation is the conjunction over all four cells and no pooled quantity
    enters any verdict, so the selection rule uses the same shape.
    """

    peak, ramp = float(candidate[0]), float(candidate[1])
    distances: list[float] = []
    for cell in SCREEN_CELLS:
        identity = stage_ab_identity(cell)
        healthy = ledger.get(
            physical_key(
                identity=identity,
                condition=CONDITION_HEALTHY,
                severity=None,
                probe_peak_force_n=peak,
                probe_ramp_fraction_of_duration=ramp,
            )
        )
        fault = ledger.get(
            physical_key(
                identity=identity,
                condition=CONDITION_STRUCTURAL,
                severity=float(severity),
                probe_peak_force_n=peak,
                probe_ramp_fraction_of_duration=ramp,
            )
        )
        require_matched_identity(identity, identity)
        distances.append(difference_statistic(fault.coefficients, healthy.coefficients))
    return float(min(distances))


def select_candidate(
    ledger: ResultsLedger, survivors: Sequence[tuple[float, float]]
) -> dict[str, Any]:
    """Apply section 8's selection rule to the surviving candidates.

    Inputs: the ledger and the candidates that cleared every gate. Outputs: a mapping
    carrying the selected candidate, every candidate's worst-cell score, and the tie set.
    Purpose: "maximise worst-cell ``D`` at remEI 0.75. Ties within 1% resolve to the
    smallest amplitude, then the largest ramp fraction." The tie band is applied to the
    best score, and the two tie-breaks are applied in that order, because the order is
    part of the pre-registration.
    """

    _require(
        len(survivors) > 0,
        f"{TERMINAL_NO_ADMISSIBLE_PROBE}: no candidate cleared the Stage-A hard gates",
    )
    scores = {
        candidate: worst_cell_statistic(ledger, candidate, severity=SELECTION_SEVERITY)
        for candidate in survivors
    }
    best = max(scores.values())
    _require(
        best > 0.0,
        f"the best worst-cell statistic at remEI {SELECTION_SEVERITY} is {best}; a "
        "non-positive best score makes the 1% tie band meaningless and must be diagnosed "
        "rather than resolved by a tie-break",
    )
    threshold = best * (1.0 - SELECTION_TIE_TOLERANCE)
    tied = [candidate for candidate in survivors if scores[candidate] >= threshold]
    selected = min(tied, key=lambda candidate: (candidate[0], -candidate[1]))
    return {
        "selected": (float(selected[0]), float(selected[1])),
        "selection_severity": SELECTION_SEVERITY,
        "worst_cell_scores": {
            f"{candidate[0]}|{candidate[1]}": scores[candidate] for candidate in survivors
        },
        "best_worst_cell": best,
        "tie_band_threshold": threshold,
        "tied_candidates": [[float(a), float(b)] for a, b in tied],
    }


def run_reuse_aware_rows(
    rows: Sequence[LogicalRow],
    context: ScreenContext,
    ledger: ResultsLedger,
    *,
    execute: ExecuteRollout,
    retain_healthy_plants: bool = False,
) -> dict[tuple[Any, ...], PrivilegedRecord]:
    """Run the non-reused rows of a stage; skip the reused ones entirely.

    Inputs: the stage's rows, the context, the ledger, the executor, and whether to keep
    the healthy plant traces. Outputs: retained plants keyed by row key. Purpose: the
    reuse rule's behavioural half. A reused row is not merely stamped differently here --
    it never reaches the construction layer or the generator at all, which is why the
    driver's tests can assert a call count of zero for those twelve rows.
    """

    retained: dict[tuple[Any, ...], PrivilegedRecord] = {}
    for row in iter_new_rows(rows):
        _, plant = run_logical_row(
            row,
            context,
            ledger,
            execute=execute,
            retain_plant=retain_healthy_plants and row.condition == CONDITION_HEALTHY,
        )
        if plant is not None:
            retained[row.key] = plant
    for row in rows:
        if row.is_reused:
            resolve_row_provenance(ledger, row)
    return retained


def gauge_only_null(
    plant: PrivilegedRecord,
    context: ScreenContext,
    cell: int,
) -> dict[str, Any]:
    """Section 9's Stage-C gauge-only decomposition for one cell (0 rollouts).

    Inputs: the cell's retained ``k=0`` plant trace, the context and the cell. Outputs:
    the 28 within-cell distances of that one trace redrawn at the eight Stage-C
    identities, and their ``Q95``. Purpose: the sensor model contains the only RNG on the
    path, so an existing plant trace can be re-observed at any identity for free.

    Scope, stated because it has been misread before: this is a **conditional healthy-null
    diagnostic** conditional on one fixed trace. It identifies no population
    decomposition, attributes no mechanism, sets no threshold and gates nothing. Only
    Stage C's ``Q95_c`` has authority.
    """

    identities = tuple(stage_c_identity(cell, k) for k in range(STAGE_C_REPLICATES))
    model = SensorModel(context.sensor_config)
    vectors: list[tuple[float, ...]] = []
    for identity in identities:
        observed = model.observe(
            plant,
            SCREEN_SUITE,
            pair_id=identity.pair_id,
            sensor_seed=identity.sensor_seed,
            fault=None,
            run_id=f"screen_gauge_only_c{cell}",
            config_hash=context.base_config_hash,
            split=SCREEN_SPLIT,
        )
        vectors.append(observation_coefficients(observed, context.timing))
    distances = [
        difference_statistic(vectors[i], vectors[j])
        for i in range(len(vectors))
        for j in range(i + 1, len(vectors))
    ]
    # A code guard, not a live one: C(8,2) is 28 whenever ``STAGE_C_REPLICATES`` is 8, so
    # no data can make this fire. Its twin in :func:`stage_c_null` is the one exercised
    # by a test (with the constant moved); this copy is deliberately left untested,
    # because reaching it costs eight synthetic re-observations to assert the identical
    # arithmetic. Recorded rather than claimed covered.
    _require(
        len(distances) == 28,
        f"the within-cell decomposition must have 28 distances; got {len(distances)}",
    )
    return {
        "cell": cell,
        "distances": [float(value) for value in distances],
        "q95_gauge_only": float(
            np.quantile(distances, STAGE_C_QUANTILE, method=STAGE_C_QUANTILE_METHOD)
        ),
        "authority": "NONE",
        "scope": (
            "conditional healthy-null diagnostic on one fixed trace; no mechanism "
            "attribution, sets no threshold, gates nothing"
        ),
    }


def stage_c_null(
    ledger: ResultsLedger, selected: tuple[float, float], cell: int
) -> dict[str, Any]:
    """Build the operative null ``Q95_c`` for one cell from its eight healthy replicates.

    Inputs: the ledger, the selected candidate and the cell. Outputs: the 28 within-cell
    distances, ``Q95_c`` and ``2*Q95_c``. Purpose: this is the protocol's only operative
    null. Carried limitation, restated wherever it is reported: 28 distances come from 8
    independent runs, so this is a U-statistic, and ``method="higher"`` places ``Q95_c``
    at the 27th of 28 order statistics.
    """

    peak, ramp = float(selected[0]), float(selected[1])
    vectors: list[tuple[float, ...]] = []
    for k in range(STAGE_C_REPLICATES):
        identity = stage_c_identity(cell, k)
        result = ledger.get(
            physical_key(
                identity=identity,
                condition=CONDITION_HEALTHY,
                severity=None,
                probe_peak_force_n=peak,
                probe_ramp_fraction_of_duration=ramp,
            )
        )
        vectors.append(result.coefficients)
    distances = [
        difference_statistic(vectors[i], vectors[j])
        for i in range(len(vectors))
        for j in range(i + 1, len(vectors))
    ]
    _require(
        len(distances) == 28,
        f"Stage C's within-cell null must have 28 distances; got {len(distances)}",
    )
    q95 = float(np.quantile(distances, STAGE_C_QUANTILE, method=STAGE_C_QUANTILE_METHOD))
    return {
        "cell": cell,
        "n_distances": len(distances),
        "n_independent_runs": STAGE_C_REPLICATES,
        "distances": [float(value) for value in distances],
        "q95_c": q95,
        "operative_threshold": OPERATIVE_NULL_MULTIPLIER * q95,
        "diagnostic_pause": q95 >= STAGE_C_DIAGNOSTIC_PAUSE_Q95,
        "u_statistic_note": (
            "28 pairwise distances from 8 independent runs; method='higher' places Q95 "
            "at the 27th of 28 order statistics"
        ),
    }


def unmatched_secondary(
    ledger: ResultsLedger,
    selected: tuple[float, float],
    *,
    cell: int,
    severity: float,
) -> dict[str, Any]:
    """Section 9's unmatched secondary: seven dependent distances, no authority.

    Inputs: the ledger, the selected candidate, the cell and the ladder value. Outputs:
    the seven ``D_unmatched`` values. Purpose: they share one fixed fault-side identity
    and have no fault-side replication, so **no quantile, gate, route or bound** is
    derived from them. Descriptive sensitivity only.
    """

    peak, ramp = float(selected[0]), float(selected[1])
    fault = ledger.get(
        physical_key(
            identity=stage_ab_identity(cell),
            condition=CONDITION_STRUCTURAL,
            severity=float(severity),
            probe_peak_force_n=peak,
            probe_ramp_fraction_of_duration=ramp,
        )
    )
    values: list[float] = []
    for k in range(1, STAGE_C_REPLICATES):
        healthy = ledger.get(
            physical_key(
                identity=stage_c_identity(cell, k),
                condition=CONDITION_HEALTHY,
                severity=None,
                probe_peak_force_n=peak,
                probe_ramp_fraction_of_duration=ramp,
            )
        )
        values.append(difference_statistic(fault.coefficients, healthy.coefficients))
    return {
        "values": values,
        "authority": "NONE",
        "scope": (
            "seven dependent distances sharing one fault-side identity, with no "
            "fault-side replication; no quantile, gate, route or bound"
        ),
    }


def build_ladder_table(
    ledger: ResultsLedger,
    selected: tuple[float, float],
    nulls: Mapping[int, Mapping[str, Any]],
    gauge_only: Mapping[int, Mapping[str, Any]],
) -> list[dict[str, Any]]:
    """Build section 9's results table: one row per ladder value.

    Inputs: the ledger, the selected candidate, the per-cell operative nulls and the
    per-cell gauge-only decompositions. Outputs: ten rows, each carrying ``D(v,c)`` for
    all four cells, ``Q95_c``, ``2*Q95_c``, ``Q95_c^gauge``, the seven ``D_unmatched``, a
    per-cell verdict and a value verdict. Purpose: section 9's aggregation is the
    conjunction over all four cells -- ``testable iff min_c [D(v,c) - 2*Q95_c] >= 0`` --
    and no mean, median or pooled quantity enters any verdict.
    """

    peak, ramp = float(selected[0]), float(selected[1])
    table: list[dict[str, Any]] = []
    for value in LADDER_REMAINING_EI:
        severity = float(value)
        per_cell: dict[str, Any] = {}
        margins: list[float] = []
        for cell in SCREEN_CELLS:
            identity = stage_ab_identity(cell)
            healthy = ledger.get(
                physical_key(
                    identity=identity,
                    condition=CONDITION_HEALTHY,
                    severity=None,
                    probe_peak_force_n=peak,
                    probe_ramp_fraction_of_duration=ramp,
                )
            )
            fault = ledger.get(
                physical_key(
                    identity=identity,
                    condition=CONDITION_STRUCTURAL,
                    severity=severity,
                    probe_peak_force_n=peak,
                    probe_ramp_fraction_of_duration=ramp,
                )
            )
            require_matched_identity(identity, identity)
            distance = difference_statistic(fault.coefficients, healthy.coefficients)
            threshold = float(nulls[cell]["operative_threshold"])
            margin = distance - threshold
            margins.append(margin)
            per_cell[str(cell)] = {
                "d": distance,
                "q95_c": float(nulls[cell]["q95_c"]),
                "operative_threshold": threshold,
                "margin": margin,
                "verdict": VERDICT_TESTABLE if margin >= 0.0 else VERDICT_SUB_THRESHOLD,
                "q95_c_gauge_only": float(gauge_only[cell]["q95_gauge_only"]),
                "d_unmatched": unmatched_secondary(
                    ledger, selected, cell=cell, severity=severity
                ),
            }
        table.append(
            {
                "remaining_ei": severity,
                "per_cell": per_cell,
                "min_margin": float(min(margins)),
                "verdict": VERDICT_TESTABLE if min(margins) >= 0.0 else VERDICT_SUB_THRESHOLD,
                "aggregation": "conjunction over all four cells; no pooled quantity",
            }
        )
    return table


def classify_outcome(table: Sequence[Mapping[str, Any]]) -> str:
    """Return section 9's case label for a completed ladder table.

    Inputs: the ladder table. Outputs: ``"CASE_A"``, ``"CASE_B"`` or ``"CASE_C"``.
    Purpose: the three cases are exhaustive only once every ladder value has a safe,
    valid per-cell verdict; this function is therefore called after that has been
    established, never as a way of establishing it.
    """

    passes = [row["verdict"] == VERDICT_TESTABLE for row in table]
    if all(passes):
        return "CASE_A"
    if any(passes):
        return "CASE_B"
    return "CASE_C"


def build_plan(
    context: ScreenContext, candidates: Sequence[tuple[float, float]]
) -> dict[str, Any]:
    """Build and audit the full pre-registered inventory without running anything.

    Inputs: the resolved context and the admissible candidates. Outputs: the plan census.
    Purpose: whole-set questions -- total cost, provenance collisions, the reuse
    arithmetic -- are invisible to per-rollout checks by construction, and they are
    exactly the questions a driver gets wrong. Building the whole plan first costs
    nothing and answers them from code rather than from the specification's prose.

    The selected candidate is not known before Stage A runs, so the plan is audited at a
    *placeholder* selection. That placeholder never leaves this function and never
    reaches a persisted result; it exists only to make the reuse arithmetic concrete.
    """

    placeholder = tuple(float(value) for value in candidates[-1])
    rows = build_logical_inventory(candidates=candidates, selected=placeholder)
    shape = require_inventory_shape(rows)
    return {
        "admissible_candidates": [[float(a), float(b)] for a, b in candidates],
        "census": shape,
        "placeholder_selection_note": (
            "the inventory shape is audited at a placeholder selection because the real "
            "selection is a Stage-A result; the placeholder is never persisted"
        ),
        "onset_index": context.timing.onset_index,
        "window": [context.timing.w0, context.timing.w1],
    }


def resolve_context(
    *,
    config_path: Path,
    schema_path: Path,
    assignment_path: Path,
    protocol_path: Path,
) -> tuple[ScreenContext, dict[str, Any]]:
    """Load and validate every bound input the screen depends on.

    Inputs: the four committed input paths. Outputs: the :class:`ScreenContext` and a
    mapping of the inputs for the results document. Purpose: everything that can fail
    before a rollout is scheduled fails here -- the I1 text pins, the assignment binding,
    the window/timestep agreement, the torque-gate constants and the four delivered
    sources.
    """

    digests = verify_text_pins(protocol_path, assignment_path)
    config = load_config(config_path, schema_path)
    assignment = load_assignment(assignment_path)
    binding = validate_approved_assignment_binding(config, expected_assignment=assignment)
    runtime = _runtime_parameters(binding)
    timing_block = config.document["values"]["timing"]
    history_steps = int(timing_block["window_steps"])

    require_torque_gate_constants(
        link_length_m=CableModelConfig().link_length_m,
        # The generator builds ``ObservedJointPDController(profile)`` with no config
        # override (assignment_generator.py:668), so the default-constructed
        # controller's own config is the limit that actually runs.
        torque_abs_limit_n_m=ObservedJointPDController().config.torque_abs_limit[0],
    )
    timing = derive_screen_timing(
        binding.assignment,
        control_dt_s=runtime.control_dt_s,
        window_steps=history_steps,
    )
    context = ScreenContext(
        assignment=binding.assignment,
        base_config_hash=config.config_hash,
        assignment_canonical_sha256=digests["assignment"],
        assignment_hash=binding.assignment_hash,
        protocol_spec_sha256=digests["protocol"],
        runtime=runtime,
        history_steps=history_steps,
        timing=timing,
        sources=screen_sources(binding),
        sensor_config=sensor_config_from_document(config.document),
    )
    inputs = {
        "config_path": str(config_path),
        "base_config_hash": config.config_hash,
        "assignment_hash": binding.assignment_hash,
        "assignment_canonical_sha256": digests["assignment"],
        "protocol_spec_sha256": digests["protocol"],
        "control_dt_s": runtime.control_dt_s,
        "window_steps": history_steps,
        "onset_time_s": timing.onset_time_s,
        "probe_start_offset_s": timing.probe_start_offset_s,
        "onset_index": timing.onset_index,
        "window": [timing.w0, timing.w1],
        "suite": SCREEN_SUITE,
    }
    return context, inputs


def run_screen(
    context: ScreenContext,
    *,
    candidates: Sequence[tuple[float, float]],
    execute: ExecuteRollout,
) -> dict[str, Any]:
    """Run Stages A, B and C end to end and return the results document body.

    Inputs: the resolved context, the admissible candidates and the rollout executor.
    Outputs: the results body. Purpose: the stage order is fixed by the reuse rule --
    Stage A must be recorded before Stage B or C can cite it -- and the ledger's
    completeness check at the end is what turns "every row reported" into "every reported
    row resolves to a body that ran".
    """

    ledger = ResultsLedger()
    plan_rows = build_logical_inventory(
        candidates=candidates, selected=tuple(float(v) for v in candidates[-1])
    )
    plan_census = require_inventory_shape(plan_rows)

    stage_a = run_stage_a(plan_rows, candidates, context, ledger, execute=execute)
    if not stage_a["survivors"]:
        return {
            "terminal": TERMINAL_NO_ADMISSIBLE_PROBE,
            "plan_census": plan_census,
            "stage_a": {
                "drops": stage_a["drops"],
                "drop_count": stage_a["drop_count"],
                "survivors": [],
            },
            "scope": (
                "terminal and pins nothing: config.json stays absent and no regeneration "
                "is triggered; the label is scoped strictly to the measured candidates"
            ),
        }

    selection = select_candidate(ledger, stage_a["survivors"])
    selected = tuple(selection["selected"])

    rows = build_logical_inventory(candidates=candidates, selected=selected)
    require_inventory_shape(rows)
    stage_b_rows = tuple(row for row in rows if row.stage == STAGE_B)
    stage_c_rows = tuple(row for row in rows if row.stage == STAGE_C)

    run_reuse_aware_rows(stage_b_rows, context, ledger, execute=execute)
    run_reuse_aware_rows(stage_c_rows, context, ledger, execute=execute)

    healthy_plants = stage_a["retained_healthy_plants"]
    nulls: dict[int, Mapping[str, Any]] = {}
    gauge_only: dict[int, Mapping[str, Any]] = {}
    for cell in SCREEN_CELLS:
        nulls[cell] = stage_c_null(ledger, selected, cell)
        key = (float(selected[0]), float(selected[1]), cell)
        _require(
            key in healthy_plants,
            f"the Stage-A healthy plant trace for cell {cell} at the selected candidate "
            "was not retained; the gauge-only secondary cannot be computed without it",
        )
        gauge_only[cell] = gauge_only_null(healthy_plants[key], context, cell)

    table = build_ladder_table(ledger, selected, nulls, gauge_only)

    executed_rows = tuple(
        row
        for row in rows
        if row.stage != STAGE_A
        or (row.probe_peak_force_n, row.probe_ramp_fraction_of_duration)
        in {(float(a), float(b)) for a, b in stage_a["survivors"]}
    )
    ledger_census = require_physical_ledger_complete(ledger, executed_rows)

    return {
        "terminal": None,
        "plan_census": plan_census,
        "stage_a": {
            "drops": stage_a["drops"],
            "drop_count": stage_a["drop_count"],
            "survivors": [[float(a), float(b)] for a, b in stage_a["survivors"]],
            "selection": selection,
        },
        "stage_c_nulls": {str(cell): nulls[cell] for cell in SCREEN_CELLS},
        "stage_c_gauge_only": {str(cell): gauge_only[cell] for cell in SCREEN_CELLS},
        "ladder": table,
        "outcome_case": classify_outcome(table),
        "ledger_census": ledger_census,
        "rows": [logical_row_report(ledger, row) for row in executed_rows],
        "executed_census": census(executed_rows),
    }


def write_results(document: Mapping[str, Any], output_dir: Path) -> Path:
    """Write the results document and verify the output root holds results only.

    Inputs: the document and the output directory. Outputs: the written path. Purpose:
    the persistence check runs *after* the write, over the real directory, so it can fail
    on a real wrong write rather than on an intention.
    """

    output_dir.mkdir(parents=True, exist_ok=True)
    path = output_dir / OUTPUT_FILENAME
    path.write_text(
        json.dumps(document, indent=2, sort_keys=True, allow_nan=False) + "\n",
        encoding="utf-8",
    )
    require_results_only_root(output_dir)
    return path


def parse_args(argv: Sequence[str] | None = None) -> argparse.Namespace:
    """Parse command-line arguments.

    Inputs: an optional argument vector. Outputs: the parsed namespace. Purpose:
    packet-relative defaults for the committed inputs; ``--output-dir`` is required so no
    result is ever written to an unstated place; ``--mode`` defaults to ``plan`` so the
    zero-rollout path is the one a mistyped command takes.
    """

    parser = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    parser.add_argument(
        "--output-dir",
        type=Path,
        required=True,
        help="results-only output root; nothing but result JSON may appear under it",
    )
    parser.add_argument(
        "--mode",
        choices=("plan", "execute"),
        default="plan",
        help="plan audits the inventory and runs zero rollouts; execute runs the screen",
    )
    parser.add_argument("--schema", type=Path, default=Path("schema/schema.json"))
    parser.add_argument(
        "--config", type=Path, default=Path("config/draft-config-v0.1.json")
    )
    parser.add_argument(
        "--assignment", type=Path, default=Path(f"config/{ASSIGNMENT_FILENAME}")
    )
    parser.add_argument(
        "--protocol", type=Path, default=Path(f"protocol/{PROTOCOL_FILENAME}")
    )
    return parser.parse_args(argv)


def main(argv: Sequence[str] | None = None) -> int:
    """Run the Stage-A/B/C screen, or audit its plan.

    Inputs: an optional argument vector. Outputs: process exit status, 0 only when every
    pin matched, the plan audited, and -- in execute mode -- every reported row resolved
    to a recorded physical rollout.
    """

    args = parse_args(argv)
    print("Protocol P sections 8-9 - Stage A/B/C screen")
    print("=" * 44)
    print(f"mode        {args.mode}")
    print(f"output dir  {args.output_dir}")
    print(f"packet root {PACKET_ROOT}")

    try:
        context, inputs = resolve_context(
            config_path=args.config.resolve(),
            schema_path=args.schema.resolve(),
            assignment_path=args.assignment.resolve(),
            protocol_path=args.protocol.resolve(),
        )
        candidates = admissible_candidates()
        plan = build_plan(context, candidates)
        print()
        print(f"admissible candidates   {len(candidates)}")
        print(f"logical rows            {plan['census']['logical_rows']}")
        print(f"physical rollouts       {plan['census']['physical_rollouts']}")
        print(f"reused rows             {plan['census']['reused_rows']}")
        print(f"derived onset index     {context.timing.onset_index}")
        print(f"window                  [{context.timing.w0}, {context.timing.w1})")

        document: dict[str, Any] = {
            "purpose": (
                "Protocol P sections 8-9: the Stage A/B/C development screen. Every "
                "artifact carries a dev- provenance hash and is permanently ineligible "
                "for confirmatory analysis."
            ),
            "protocol": {
                "file": PROTOCOL_FILENAME,
                "canonical_sha256": PROTOCOL_CANONICAL_SHA256,
            },
            "mode": args.mode,
            "inputs": inputs,
            "plan": plan,
        }
        if args.mode == "execute":
            document["results"] = run_screen(
                context, candidates=candidates, execute=execute_rollout
            )
        else:
            document["results"] = None
            print()
            print("plan mode: zero rollouts were run and no stage was measured")

        written = write_results(document, args.output_dir.resolve())
        print()
        print(f"wrote {written}")
    except ProtocolPError as error:
        print()
        print(f"FAILED: {error}")
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
