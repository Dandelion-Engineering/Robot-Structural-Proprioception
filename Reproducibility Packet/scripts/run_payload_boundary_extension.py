"""Plan or execute the development-only payload-boundary extension v0.2.

Plan mode is the default and spends zero rollouts.  It compiles the seven declared
payload bodies, audits the common-random-number reservation, writes the exact plan, and
stops.  Execute mode requires a separately authorized plan digest and the retained
development data needed by Protocol P's ordinary-path replay gate.

The extension deliberately owns its X-stage ledger and inventory.  Protocol P's
``ResultsLedger`` accepts only A/B/C origins and its inventory guard pins 180/168/12;
pretending either vocabulary applied here would erase the distinction the extension's
contract requires.
"""

from __future__ import annotations

import argparse
import csv
import dataclasses
import hashlib
import itertools
import json
import math
import re
import sys
import time
from collections import Counter
from collections.abc import Callable, Mapping, Sequence
from pathlib import Path, PurePosixPath, PureWindowsPath
from typing import Any

import numpy as np

SCRIPT_DIR = Path(__file__).resolve().parent
if str(SCRIPT_DIR) not in sys.path:
    sys.path.insert(0, str(SCRIPT_DIR))

from analyze_synchronous_difference_null import verify_text_pins  # noqa: E402
from protocol_p_replay_gate import (  # noqa: E402
    N_OBSERVATION_ENTRIES,
    N_PRIVILEGED_FIELDS,
    REPLAY_SUITE,
    RUN_ID as REPLAY_RUN_ID,
    SCENARIO_SPEC_ID as REPLAY_SCENARIO_SPEC_ID,
    check_pinned_digests,
    compare_manifest_row,
    compare_payload,
    diff_inventory,
    inventory,
    load_npz_entries,
    require_no_inventory_changes,
)
from run_protocol_p_screen import (  # noqa: E402
    SCREEN_SUITE,
    ScreenTiming,
    bound_trajectory,
    derive_screen_timing,
    difference_statistic,
    evaluate_hard_gates,
    execute_rollout,
    observation_coefficients,
    packet_relative_input_path,
    require_preregistered_faults,
    require_probe_torque_gate,
    screen_physical_faults,
    screen_sources,
)
from utils.assignment_binding import validate_approved_assignment_binding  # noqa: E402
from utils.assignment_generator import (  # noqa: E402
    ScreenOverrides,
    _generate_reservation,
    _physical_config,
    _runtime_parameters,
    build_identity_manifest,
    screen_pair_id,
)
from utils.cable_mechanics import CableModelConfig  # noqa: E402
from utils.cable_plant import CablePlant  # noqa: E402
from utils.config_contract import load_config  # noqa: E402
from utils.gate3_assignment import load_assignment  # noqa: E402
from utils.protocol_p import (  # noqa: E402
    ASSIGNMENT_FILENAME,
    PROTOCOL_CANONICAL_SHA256,
    PROTOCOL_FILENAME,
    ProtocolPError,
    canonical_json,
    canonical_text_sha256,
)
from utils.protocol_p import require as _require  # noqa: E402
from utils.protocol_p_conditions import (  # noqa: E402
    CONDITION_HEALTHY,
    CONDITION_STRUCTURAL,
    LADDER_REMAINING_EI,
    RolloutIdentity,
    SCREEN_CELLS,
    screen_reservation,
)
from utils.protocol_p_results import (  # noqa: E402
    PhysicalKey,
    physical_key,
    physical_key_report,
)
from utils.schema_types import FaultSpec, PrivilegedRecord  # noqa: E402

PACKET_ROOT = SCRIPT_DIR.parent
REPO_ROOT = PACKET_ROOT.parent

EXTENSION_FILENAME = "payload-boundary-extension-v0.2.md"
EXTENSION_CANONICAL_SHA256 = (
    "538ae06b87d0f733659ed113f3b38e0a0c1f7c7793d290358acf08d78df33b6a"
)
PLAN_FILENAME = "plan.json"
RESULT_FILENAME = "payload_boundary.json"
AUTHORITY = (
    "DEVELOPMENT ONLY: ineligible for confirmatory analysis; cannot change Protocol P "
    "outcome or role-coverage counts."
)

PROBE_PEAK_FORCE_N = 0.10
PROBE_RAMP_FRACTION = 0.25
SOURCE_CELL = 6
X_SEED_BASE = 160000
TAU_ANCHOR = 0.10
QUANTILE = 0.95
QUANTILE_METHOD = "higher"
NULL_MULTIPLIER = 2.0
DIAGNOSTIC_PAUSE_Q95 = 0.30

CONDITION_STRUCTURE = "structure"
EXTENSION_CONDITIONS = (CONDITION_HEALTHY, CONDITION_STRUCTURE)
STAGE_XA = "XA"
STAGE_XM = "XM"
SUBSTAGE_XC = "XC"
SUBSTAGE_XB = "XB"
EXTENSION_STAGES = (STAGE_XA, STAGE_XM)
EXTENSION_SUBSTAGES = (SUBSTAGE_XC, SUBSTAGE_XB)

OUTCOME_CONSTRUCTION = "X_CONSTRUCTION_UNVERIFIED"
OUTCOME_REPLAY = "X_DEFAULT_PATH_UNVERIFIED"
OUTCOME_INVALID = "X_INVALID_MEASUREMENT"
OUTCOME_UNSAFE_ANCHOR = "X_UNSAFE_ANCHOR"
OUTCOME_ANCHOR_NONPREFIX = "X_ANCHOR_NONPREFIX"
OUTCOME_ANCHOR_FAIL = "X_ANCHOR_FAIL"
OUTCOME_OVERRIDE = "X_OVERRIDE_NOT_REALIZED"
OUTCOME_REDUCED = "X_REDUCED_MASS_COVERAGE"
OUTCOME_NONPREFIX = "X_NONPREFIX_WITHIN_MASS"
OUTCOME_NONMONOTONE = "X_NONMONOTONE_IN_MASS"
OUTCOME_EMPTY = "X_CASE_EMPTY"
OUTCOME_ROLE_LOST = "X_CASE_ROLE_LOST"
OUTCOME_ROLE_HELD = "X_CASE_ROLE_HELD"
OUTCOMES = (
    OUTCOME_CONSTRUCTION,
    OUTCOME_REPLAY,
    OUTCOME_INVALID,
    OUTCOME_UNSAFE_ANCHOR,
    OUTCOME_ANCHOR_NONPREFIX,
    OUTCOME_ANCHOR_FAIL,
    OUTCOME_OVERRIDE,
    OUTCOME_REDUCED,
    OUTCOME_NONPREFIX,
    OUTCOME_NONMONOTONE,
    OUTCOME_EMPTY,
    OUTCOME_ROLE_LOST,
    OUTCOME_ROLE_HELD,
)

ROLE_SEVERITY_MAP: dict[str, tuple[float, ...]] = {
    "dev": (0.50, 0.75),
    "pilot": (0.60, 0.85),
    "val": (0.40, 0.90),
    "test": (0.35, 0.65),
}


@dataclasses.dataclass(frozen=True)
class MassCell:
    """One pre-registered payload mass and the split role whose severities it tests."""

    m: int
    mass_kg: float
    role_split: str


MASS_CELLS: tuple[MassCell, ...] = (
    MassCell(0, 0.050, "dev"),
    MassCell(1, 0.025, "pilot"),
    MassCell(2, 0.075, "pilot"),
    MassCell(3, 0.100, "val"),
    MassCell(4, 0.125, "val"),
    MassCell(5, 0.150, "test"),
    MassCell(6, 0.200, "test"),
)
ASCENDING_MASS_CELLS = tuple(sorted(MASS_CELLS, key=lambda item: item.mass_kg))
LADDER = tuple(float(value) for value in LADDER_REMAINING_EI)
_require(
    LADDER == (0.35, 0.40, 0.45, 0.50, 0.55, 0.60, 0.65, 0.75, 0.85, 0.90),
    f"the inherited ladder drifted: {LADDER}",
)

CELL_6_D = (1.352761, 1.097979, 0.886017, 0.725050, 0.581992,
            0.493738, 0.384587, 0.255447, 0.139496, 0.089858)
CELL_6_Q95 = 0.37033237
CELL_6_THRESHOLD = 0.74066474
CELL_6_MARGINS = (0.612096, 0.357314, 0.145352, -0.015614, -0.158672,
                  -0.246927, -0.356078, -0.485218, -0.601168, -0.650807)
ANCHOR_CONSTRAINED_RUNGS = (0.35, 0.40, 0.45, 0.55, 0.60, 0.65, 0.75, 0.85, 0.90)
ANCHOR_UNCONSTRAINED_RUNGS = (0.50,)


def _tau_anchor_partition(tau: float) -> tuple[tuple[float, ...], tuple[float, ...]]:
    """Split the ladder by section 9.3's rule: |margin| / threshold against tau.

    The ``>=`` boundary is exact but unreachable at the pinned margins: the ratios are
    0.021 and 0.196 either side of tau = 0.10 and none of the ten equals it, so the
    ``<`` / ``<=`` distinction decides nothing here and a mutation of it survives.
    """

    ratios = [abs(margin) / CELL_6_THRESHOLD for margin in CELL_6_MARGINS]
    return (
        tuple(value for value, ratio in zip(LADDER, ratios) if ratio >= tau),
        tuple(value for value, ratio in zip(LADDER, ratios) if ratio < tau),
    )


# TAU_ANCHOR must PRODUCE the partition rather than sit beside it.  A constant that looks
# authoritative and drives nothing is the trap this project has already recorded; without
# this the two tuples could drift from the tau the plan artifact publishes and nothing
# would notice.
_require(
    _tau_anchor_partition(TAU_ANCHOR)
    == (ANCHOR_CONSTRAINED_RUNGS, ANCHOR_UNCONSTRAINED_RUNGS),
    f"the pinned anchor partition is not the one tau_anchor={TAU_ANCHOR} produces from "
    f"the pinned cell-6 margins: {_tau_anchor_partition(TAU_ANCHOR)}",
)


def identity_for(k: int) -> RolloutIdentity:
    """Return section-5's suffix-free common-random-number identity for replicate k."""

    _require(isinstance(k, int) and not isinstance(k, bool) and 0 <= k <= 7,
             f"replicate index must be an int in [0,7]; got {k!r}")
    return RolloutIdentity(
        sensor_seed=X_SEED_BASE + 1000 * k + 2,
        pair_id=f"basepair_payloadext_k{k}",
    )


@dataclasses.dataclass(frozen=True)
class ExtensionRow:
    """One distinct extension rollout and its physical-body identity."""

    mass: MassCell
    condition: str
    severity: float | None
    replicate: int

    def __post_init__(self) -> None:
        """Refuse a condition, severity or replicate outside the planned row vocabulary."""

        _require(self.condition in EXTENSION_CONDITIONS,
                 f"unknown extension condition {self.condition!r}")
        _require(isinstance(self.replicate, int) and not isinstance(self.replicate, bool)
                 and 0 <= self.replicate <= 7,
                 f"replicate must be an int in [0,7]; got {self.replicate!r}")
        if self.condition == CONDITION_HEALTHY:
            _require(self.severity is None, "a healthy extension row takes no severity")
        else:
            _require(self.replicate == 0, "a ladder row must use the matched k=0 identity")
            _require(self.severity in LADDER, f"ladder severity is outside {LADDER}")

    @property
    def stage(self) -> str:
        """Return XA for the anchor and XM for every non-anchor mass."""

        return STAGE_XA if self.mass.m == 0 else STAGE_XM

    @property
    def substage(self) -> str:
        """Return XC for healthy rows and XB for fault rows."""

        return SUBSTAGE_XC if self.condition == CONDITION_HEALTHY else SUBSTAGE_XB

    @property
    def identity(self) -> RolloutIdentity:
        """Return the replicate-only identity shared across all seven masses."""

        return identity_for(self.replicate)

    @property
    def internal_condition(self) -> str:
        """Map the extension's exact 'structure' label to Protocol P's builder label."""

        return CONDITION_HEALTHY if self.condition == CONDITION_HEALTHY else CONDITION_STRUCTURAL

    @property
    def physical(self) -> PhysicalKey:
        """Return the mass-aware key for this distinct physical body."""

        return physical_key(
            identity=self.identity,
            condition=self.internal_condition,
            severity=self.severity,
            probe_peak_force_n=PROBE_PEAK_FORCE_N,
            probe_ramp_fraction_of_duration=PROBE_RAMP_FRACTION,
            distal_payload_mass_kg=self.mass.mass_kg,
        )

    @property
    def key(self) -> tuple[Any, ...]:
        """Return the extension-owned logical identifier, explicitly including mass."""

        return (self.mass.m, self.condition, self.severity, self.replicate)


def planned_rows() -> tuple[ExtensionRow, ...]:
    """Return all 126 rows in the document's per-mass construction order."""

    rows: list[ExtensionRow] = []
    for mass in MASS_CELLS:
        rows.extend(ExtensionRow(mass, CONDITION_HEALTHY, None, k) for k in range(8))
        rows.extend(ExtensionRow(mass, CONDITION_STRUCTURE, value, 0) for value in LADDER)
    return tuple(rows)


def require_plan_shape(rows: Sequence[ExtensionRow]) -> dict[str, Any]:
    """X1/X9/X13: audit the complete planned partition and physical-key budget."""

    rows = tuple(rows)
    _require(len(rows) == 126, f"plan must contain 126 occurrences; got {len(rows)}")
    _require(len({row.key for row in rows}) == 126, "planned logical row keys collide")
    _require(len({row.physical for row in rows}) == 126, "planned physical keys collide")
    classes = Counter(row.replicate for row in rows)
    _require(classes == Counter({0: 77, 1: 7, 2: 7, 3: 7, 4: 7, 5: 7, 6: 7, 7: 7}),
             f"planned identity partition is not section 5's exact partition: {classes}")
    identities = {row.identity for row in rows}
    _require(identities == {identity_for(k) for k in range(8)},
             "planned identity set differs from the eight reserved identities")
    return {
        "occurrences": len(rows),
        "distinct_physical_keys": len({row.physical for row in rows}),
        "distinct_identities": len(identities),
        "identity_class_counts": {str(k): classes[k] for k in range(8)},
    }


@dataclasses.dataclass
class ExtensionContext:
    """All bound inputs needed by zero-rollout planning and later execution."""

    assignment: Mapping[str, Any]
    binding: Any
    base_config_hash: str
    assignment_canonical_sha256: str
    assignment_hash: str
    protocol_spec_sha256: str
    extension_spec_sha256: str
    runtime: Any
    history_steps: int
    timing: ScreenTiming
    source: Any
    inputs: dict[str, Any]


def resolve_context(
    *, config_path: Path, schema_path: Path, assignment_path: Path,
    protocol_path: Path, extension_path: Path,
) -> ExtensionContext:
    """Load and bind every tracked input before a plan can be called valid."""

    digests = verify_text_pins(protocol_path, assignment_path)
    extension_digest = canonical_text_sha256(extension_path)
    _require(extension_digest == EXTENSION_CANONICAL_SHA256,
             f"extension canonical digest {extension_digest} != {EXTENSION_CANONICAL_SHA256}")
    config = load_config(config_path, schema_path)
    assignment = load_assignment(assignment_path)
    binding = validate_approved_assignment_binding(config, expected_assignment=assignment)
    runtime = _runtime_parameters(binding)
    history_steps = int(config.document["values"]["timing"]["window_steps"])
    timing = derive_screen_timing(
        binding.assignment, control_dt_s=runtime.control_dt_s, window_steps=history_steps
    )
    source = screen_sources(binding)[SOURCE_CELL]
    _require(source.env_profile_id == "env_dev_iso25c",
             f"source environment drifted: {source.env_profile_id!r}")
    _require(source.contact_profile_id == "contact_dev_none",
             f"source contact drifted: {source.contact_profile_id!r}")
    _require(source.trajectory_spec_id == "trajectory_dev_diagnostic_b",
             f"source trajectory drifted: {source.trajectory_spec_id!r}")
    inputs = {
        "assignment_canonical_sha256": digests["assignment"],
        "assignment_hash": binding.assignment_hash,
        "base_config_hash": config.config_hash,
        "protocol_spec_sha256": digests["protocol"],
        "extension_spec_sha256": extension_digest,
        "config_path": packet_relative_input_path(config_path),
        "control_dt_s": runtime.control_dt_s,
        "window": [timing.w0, timing.w1],
        "window_steps": history_steps,
        "onset_index": timing.onset_index,
        "onset_time_s": timing.onset_time_s,
        "probe_start_offset_s": timing.probe_start_offset_s,
        "suite": SCREEN_SUITE,
        "probe_peak_force_n": PROBE_PEAK_FORCE_N,
        "probe_ramp_fraction_of_duration": PROBE_RAMP_FRACTION,
        "environment_profile_id": source.env_profile_id,
        "contact_profile_id": source.contact_profile_id,
        "trajectory_spec_id": source.trajectory_spec_id,
        "source_scenario_spec_id": source.scenario_spec_id,
    }
    return ExtensionContext(
        assignment=binding.assignment,
        binding=binding,
        base_config_hash=config.config_hash,
        assignment_canonical_sha256=digests["assignment"],
        assignment_hash=binding.assignment_hash,
        protocol_spec_sha256=digests["protocol"],
        extension_spec_sha256=extension_digest,
        runtime=runtime,
        history_steps=history_steps,
        timing=timing,
        source=source,
        inputs=inputs,
    )


def mechanics_preflight(context: ExtensionContext) -> list[dict[str, Any]]:
    """X0P/X0E: prove the override is the sole mass source and compile all seven bodies."""

    trajectory = bound_trajectory(context.assignment)
    nominal = CablePlant(
        CableModelConfig(control_dt_s=context.runtime.control_dt_s),
        point_count=context.runtime.point_count,
        simulation_timestep_s=context.runtime.simulation_timestep_s,
    )
    nominal_mass = float(np.sum(nominal.model.body_mass))
    reports: list[dict[str, Any]] = []
    for mass in MASS_CELLS:
        overrides = ScreenOverrides(distal_payload_mass_kg=mass.mass_kg)
        config = _physical_config(
            context.assignment,
            context.source,
            trajectory,
            control_dt_s=context.runtime.control_dt_s,
            overrides=overrides,
        )
        _require(config.distal_payload_mass_kg == mass.mass_kg,
                 f"override mass {mass.mass_kg} did not reach the compiled config")
        plant = CablePlant(
            config,
            point_count=context.runtime.point_count,
            simulation_timestep_s=context.runtime.simulation_timestep_s,
        )
        realized = float(np.sum(plant.model.body_mass)) - nominal_mass
        _require(np.isclose(realized, mass.mass_kg, rtol=0.0, atol=1.0e-12),
                 f"mass {mass.mass_kg} realized delta {realized}")
        reports.append({"m": mass.m, "declared_mass_kg": mass.mass_kg,
                        "configured_mass_kg": config.distal_payload_mass_kg,
                        "realized_delta_kg": realized})
    return reports


def require_identity_bands(context: ExtensionContext, rows: Sequence[ExtensionRow]) -> None:
    """X1/X2: refuse collisions without constructing non-dev reservations."""

    manifest, _reservations = build_identity_manifest(
        context.binding, splits=("dev",), suites=("C0", "C1", "S")
    )
    approved_dev = {(int(row.sensor_seed), str(row.pair_id)) for row in manifest}
    planned = {(row.identity.sensor_seed, row.identity.pair_id) for row in rows}
    _require(not (planned & approved_dev), "extension identity collides with a dev dataset identity")
    seeds = {seed for seed, _pair in planned}
    _require(min(seeds) == 160002 and max(seeds) == 167002 and len(seeds) == 8,
             f"extension seed band drifted: {sorted(seeds)}")
    # The approved split seed bases are separated by 100000.  The entire extension band
    # lies between Protocol P's upper seed and the first pilot base, so no pilot/val/test
    # reservation needs to be materialized or read to establish disjointness.
    _require(max(seeds) < 210000 and min(seeds) > 157032,
             "extension seed band overlaps Protocol P or a reserved non-dev band")


def cell_6_margin_rows() -> list[dict[str, Any]]:
    """Return the ten persisted screen-cell-6 anchor references."""

    rows = []
    for value, distance, margin in zip(LADDER, CELL_6_D, CELL_6_MARGINS):
        rows.append({"value": value, "d": distance, "q95": CELL_6_Q95,
                     "threshold": CELL_6_THRESHOLD, "margin": margin,
                     "verdict": "TESTABLE" if margin >= 0.0 else "SUB_THRESHOLD"})
    return rows


def _physical_keys_digest(rows: Sequence[ExtensionRow]) -> str:
    """Hash sorted physical-key reports using §11.1's exact two-stage recipe."""

    reports = [physical_key_report(row.physical) for row in rows]
    ordered = sorted(reports, key=canonical_json)
    return hashlib.sha256(canonical_json(ordered).encode("utf-8")).hexdigest()


def build_plan_document(context: ExtensionContext) -> dict[str, Any]:
    """Run zero-rollout preflight and return the complete valid plan artifact."""

    rows = planned_rows()
    shape = require_plan_shape(rows)
    require_identity_bands(context, rows)
    mechanics = mechanics_preflight(context)
    identities = []
    for k in range(8):
        identity = identity_for(k)
        identities.append({"k": k, "sensor_seed": identity.sensor_seed,
                           "base_pair_id": identity.pair_id,
                           "membership_count": 77 if k == 0 else 7})
    plan = {
        "masses": [dataclasses.asdict(item) for item in MASS_CELLS],
        "ladder": list(LADDER),
        "role_severity_map": {key: list(values) for key, values in ROLE_SEVERITY_MAP.items()},
        "identities": identities,
        "physical_keys": {"count": 126, "canonical_sha256": _physical_keys_digest(rows)},
        "anchor": {"mass_kg": 0.05, "tau_anchor": TAU_ANCHOR,
                   "constrained_rungs": list(ANCHOR_CONSTRAINED_RUNGS),
                   "unconstrained_rungs": list(ANCHOR_UNCONSTRAINED_RUNGS),
                   "cell_6_margins": cell_6_margin_rows()},
        "census": {
            "extension_physical_rollouts": 126,
            "replay_physical_rollouts": 1,
            "total_physical_rollouts": 127,
            "logical_references": 532,
            "rollouts_by_stage": {"XA": 18, "XM-C": 48, "XM-B": 60},
            "exit_costs": {"X0P": 0, "X0E": 0, "XR": 1, "anchor_healthy_max": 9,
                           "anchor_ladder_max": 19, "X8_fail": 67, "full": 127},
            "maximum_cost": 127,
        },
        "stage_order": {
            "plan": ["X0P"],
            "execute": ["X0E", "XR", "XA", "XM-C", "XL", "XM-B", "XZ"],
        },
        "shape_audit": shape,
    }
    return {
        "inputs": context.inputs,
        "protocol": [
            {"file": PROTOCOL_FILENAME, "canonical_sha256": context.protocol_spec_sha256},
            {"file": EXTENSION_FILENAME, "canonical_sha256": context.extension_spec_sha256},
        ],
        "plan_valid": True,
        "preflight": {"ran": True, "passed": True,
                      "checks": ["seven_mass_mechanics_exact", "override_is_payload_source",
                                 "identity_partition_exact", "identity_bands_disjoint",
                                 "physical_keys_126_distinct", "role_map_pinned"],
                      "per_mass_realized_delta": mechanics, "reason": None},
        "terminal": None,
        "plan": plan,
        "authority": AUTHORITY,
        "mode": "plan",
    }


def failed_plan_document(reason: str) -> dict[str, Any]:
    """Return §11.1's persisted plan-mode failure shape."""

    reason = scrub_machine_paths(reason)
    unavailable = {"value": None, "reason": str(reason)}
    return {
        "inputs": unavailable,
        "protocol": unavailable,
        "plan_valid": False,
        "preflight": {"ran": True, "passed": False, "checks": [], "reason": str(reason)},
        "terminal": {"rule": OUTCOME_CONSTRUCTION, "reason": str(reason),
                     "stage_reached": "X0P"},
        "plan": unavailable,
        "authority": AUTHORITY,
        "mode": "plan",
    }


_PLAN_DIGEST = re.compile(r"[0-9a-f]{64}")
MAX_PLAN_JSON_DEPTH = 64
# A backslash-rooted drive needs no token boundary: URI schemes use forward slashes, and
# requiring a boundary lets ``opaque-prefixC:\\private\\row.npz`` publish a real machine
# path inside prose.  It also follows the predicate's ``PureWindowsPath`` semantics:
# ANY one-character drive prefix is accepted, not only A-Z, so an embedded
# ``opaque-prefix1:\\private\\row.npz`` must be caught here as well as when it is the whole
# string.  The forward-slash letter form does not keep an outer token boundary either: it
# refuses a SECOND slash instead.  A URL's scheme separator is always "://", so
# ``[A-Za-z]:/(?!/)`` declines "https://host/x" without needing to know where the token
# began, while a drive path glued to prose is caught.  MEASURED on the state this replaces:
# r"opaque-prefixC:/My Data\PRIVATE\row.npz" published as r"opaque-prefixC:My Data\PRIVATE\row.npz"
# -- the boundary blocked this rule, the POSIX rule then matched only "/My", and the DRIVE
# DESIGNATOR survived with the whole directory path behind it.  A non-letter drive cannot
# begin a URI scheme, so its forward-slash form needs no such refusal.
#
# THE TAIL MAY CROSS A SPACE, and only when a backslash still lies ahead of the next
# whitespace.  Without that the match stops at the first space, so a path CONTAINING one is
# reduced to its first space-free run and the rest is published: MEASURED,
# r"D:\My Data\PRIVATE\row.npz" became r"My Data\PRIVATE\row.npz".  Directory names with
# spaces are the ordinary case -- "Program Files", and this repository's own parent -- so
# this is the likeliest leak here, not an exotic one.  The gate is a BACKSLASH because
# this project's prose vocabulary is forward-slashed ("dev/pilot/val", "C1/S",
# "0.10 N / 0.25"), so no sentence of ours can satisfy it; measured on a prose battery,
# which the gate leaves byte-identical.  Its deliberate cost is that a space-containing
# path written with only forward slashes after that space, or with mixed separators whose
# remaining separators are forward slashes, retains a RELATIVE suffix.  The scrubber
# docstring names and bounds that limitation; widening this gate to either separator would
# consume the ordinary forward-slashed prose it exists to preserve.
_WINDOWS_ABSOLUTE = re.compile(
    r"(?:[^\\/\r\n]:\\|[A-Za-z]:/(?!/)|[^A-Za-z\\/\r\n]:/|\\\\)"
    r"(?:[^\s'\"<>|]|[ ](?=[^\s'\"<>|]*\\))*"
)
# The schemes whose "//" belongs to a URL rather than to a UNC path.  A URL host and a UNC
# host are LEXICALLY IDENTICAL -- "//host/share" and "//example.org/spec" differ in nothing
# a pattern can see -- so the only thing that can separate them is the scheme name, and the
# only honest way to use a scheme name is to NAME the ones being protected.  "file" is
# deliberately absent: "file://host/share" IS a path, and a URL that spells one out should
# be scrubbed like any other.  Everything not listed here is treated as a path; that is the
# disclosed cost, and the scrubber's docstring states it.
_URI_SCHEMES = ("http", "https", "ftp", "ftps", "sftp", "ssh", "git")
_URI_SCHEME_GUARD = "".join(f"(?<!(?i:{scheme}):)" for scheme in _URI_SCHEMES)
# Two POSIX forms, and they need DIFFERENT boundaries.  "//host/share" is the forward-slash
# rendering of a UNC path and both PurePath flavours call it absolute, so it must be
# scrubbed; its OWN lookbehind is what separates it from "scheme://", which must not be.
# An outer token boundary therefore bought nothing and cost the glued form: MEASURED,
# "opaque-prefix//host/PRIVATE/row.npz" was published whole.  The single-slash form KEEPS
# its boundary, and that is a deliberate disclosed gap rather than an oversight -- see the
# scrubber's docstring.  Neither form matches the ratio "0.1 N / 0.25" or the arrow
# "A -> B", because both require a non-space character after the slash.
#
# THE UNC LOOKBEHIND NAMES SCHEMES; it used to refuse ANY alphanumeric followed by a colon.
# That is a wider claim than "this is a URL", and it published a COMPLETE ROOTED PATH:
# MEASURED, "reason://host/PRIVATE/row.npz" survived both patterns AND the writer's guard,
# so the artifact was written with the host, the private directory and the file name intact.
# Nothing about the old lookbehind was recoverable by the guard, because the guard shares
# these patterns on purpose.  The scheme list is the narrowest thing that keeps "https://"
# safe while treating an unrecognised "word://host/..." as what it looks like on this
# machine: a path.
_POSIX_ABSOLUTE = re.compile(
    r"(?P<lead>^|[\s:=('\"\[])(?P<rooted>/(?!/)[^\s'\"<>|)\],;]+)"
    r"|(?P<unc>" + _URI_SCHEME_GUARD + r"//[^\s'\"<>|)\],;/][^\s'\"<>|)\],;]*)"
)


def _final_component(span: str) -> str:
    """Return one matched path span's last component under BOTH separators.

    Inputs: the span a POSIX pattern matched.  Outputs: its final component, or "" when no
    component survives.
    Purpose: ``PurePosixPath`` cannot see a backslash, so its ``name`` for a span written
    r"/PRIVATE\\row.npz" is the whole r"PRIVATE\\row.npz" and the parent directory is
    published.  MEASURED: r"opaque-prefixC:/PRIVATE\\row.npz" reduced to
    r"opaque-prefixC:PRIVATE\\row.npz".  Splitting on both separators also means this
    replacement can never RE-EMIT a separator, which is the state the fixpoint below
    exists to survive.
    """

    parts = [part for part in re.split(r"[\\/]", span) if part]
    return parts[-1] if parts else ""


def _records_absolute_path(text: str) -> bool:
    """Return whether one persisted string records an absolute filesystem path.

    The writer contract concerns the whole recorded string, not only whether that string
    *is itself* a path.  The regex forms detect paths embedded in prose; the ``PurePath``
    forms catch bare roots and path spellings outside those enumerated forms.
    """

    return (
        _WINDOWS_ABSOLUTE.search(text) is not None
        or _POSIX_ABSOLUTE.search(text) is not None
        or PureWindowsPath(text).is_absolute()
        or PurePosixPath(text).is_absolute()
    )


def _substitution_pass(text: str) -> str:
    """Apply each path pattern EXACTLY ONCE, leaving the surrounding prose in place.

    Inputs: one message.  Outputs: the message after a single pass of both patterns.
    Purpose: the caller runs this to a fixpoint, and one pass is measurably not enough.
    It is a separate function so a test can DRIVE one pass and show what it leaves behind,
    rather than asserting the shortfall in a docstring or keeping a second copy of the
    substitution in the test file.
    """

    scrubbed = _WINDOWS_ABSOLUTE.sub(
        lambda match: PureWindowsPath(match.group(0)).name or "<path>", text
    )
    return _POSIX_ABSOLUTE.sub(
        lambda match: (match.group("lead") or "")
        + (_final_component(match.group("rooted") or match.group("unc")) or "<path>"),
        scrubbed,
    )


def substitute_known_path_spellings(text: str) -> str:
    """Apply both path patterns to a FIXPOINT, leaving the surrounding prose in place.

    Inputs: one message.  Outputs: the message with every enumerated path spelling reduced
    to its final component.
    Purpose: one pass is not enough, and the shortfall is not hypothetical.  A repeated
    root is the surviving mechanism: one pass reduces ``///data/gate3.npz`` to
    ``/gate3.npz`` and re-emits it after the boundary character, so the message still
    RECORDS a rooted path while the whole string stays relative -- and the only exit left
    in the caller is to discard the entire message.  MEASURED with a single pass over the
    37,448 enumerated strings: 969 are still absolute afterwards and TEN of them reach
    that discard exit.  A scrubber that silently replaces a reason is worse than one that
    truncates it, because the reader cannot tell.

    The Session-68 mechanism -- the POSIX rule re-emitting ``\\row.npz`` and rebuilding
    ``C:\\row.npz`` inside declined prose -- is closed at its source by
    ``_final_component``, which reduces under both separators; the three sentences that
    demonstrated it now survive a single pass.  The fixpoint is retained because the
    repeated-root family above still needs it and because the guarantee has to hold for
    inputs nobody enumerated.

    This is a separate function so the caller's post-condition is checkable from outside
    without a second copy of the substitution.

    TERMINATION IS ARITHMETIC, not a runtime check.  Every match consumes at least one
    root or drive separator, and NEITHER replacement can contain one: ``PureWindowsPath``'s
    ``name`` and ``_final_component`` both treat "/" and "\\" as separators and return a
    single component.  Each productive pass therefore strictly decreases the total number
    of "/" and "\\" characters, so there cannot be more productive passes than the message
    had separators to begin with.
    """

    scrubbed = str(text)
    for _ in range(scrubbed.count("/") + scrubbed.count("\\") + 1):
        pass_input = scrubbed
        scrubbed = _substitution_pass(scrubbed)
        if scrubbed == pass_input:
            break
    return scrubbed


def scrub_machine_paths(text: str) -> str:
    """Rewrite absolute filesystem paths that appear inside a persisted message.

    Inputs: one message.  Outputs: the same message with machine paths removed.
    Purpose: X7 forbids a result artifact from recording an absolute path, and a refusal
    sentence that quotes one is still a recording.  The writer's own guard asks whether a
    string *is* a path, which no real message is -- every one of them embeds the path in
    prose, so the guard passes and the path is published.

    Paths under the repository become ``<repo>``-relative; any other Windows, UNC, or
    POSIX absolute path -- including the ``//host/share`` rendering -- is reduced to its
    final component.  The forward-slash letter form keeps the URI-safe token boundary;
    the other drive/root forms cannot be URL schemes.  Ordinary prose, ratios, arrows
    and links survive unchanged.

    THREE AMBIGUITIES ARE DELIBERATELY NOT CLOSED, and each is a survivor SHAPE rather
    than a list of spellings.  First, the single-slash POSIX form is not recognized when it
    is glued to a word with no token boundary (``opaque-prefix/private/row.npz``).  Second,
    a path containing WHITESPACE is reduced only through that whitespace unless the
    whitespace is a space AND a backslash still appears before the next one
    (``/mnt/My Data/private/row.npz``, ``D:/My Data/private/row.npz``, and any path whose
    space is a tab); the absolute root is removed and a RELATIVE directory suffix survives.
    Third, a ``//`` preceded by one of the named ``_URI_SCHEMES`` is left alone, so a URL
    that spells out a private path under one of those schemes is published.

    Closing the first means treating a forward slash after an ordinary character as a root.
    Closing the second means treating a forward slash in a later token as proof that the
    preceding space belongs to the path.  Either turns this project's own vocabulary into
    nonsense -- "dev/pilot/val" becomes "val", "C1/S" becomes "C1S", "1/2" becomes "12" --
    and a silently corrupted reason is worse than a leaked relative suffix because nothing
    discloses it.  The third is the residue of a whitelist that has to exist: a URL host and
    a UNC host are lexically identical, so SOME name-based decision is unavoidable, and a
    short list of protected schemes is the version whose cost can be stated.  The converse
    cost is stated too: an unlisted scheme's ``//`` form is reduced like a path, so
    ``myscheme://host/x`` becomes ``x``.

    The cost is bounded on this machine: native Windows paths produced by ``Path`` use
    backslashes and are covered even when they contain spaces, and repository paths are
    replaced exactly before either pattern runs.  Every ambiguity above is shared by the
    writer's guard on purpose; if only the guard widened, X7 would fire while X6 was
    writing the record.  Limitations, not oversights.

    The two patterns are an ENUMERATION of path spellings; the writer's guard is a
    PREDICATE over ``PurePath``.  Where the two disagree the artifact is destroyed, so the
    final step below states the scrubber's contract as that same predicate rather than as
    a third pattern: whatever the patterns missed, the result is not absolute.
    """

    scrubbed = str(text)
    for rendering in (str(REPO_ROOT), REPO_ROOT.as_posix()):
        scrubbed = scrubbed.replace(rendering, "<repo>")
    scrubbed = substitute_known_path_spellings(scrubbed)
    # POST-CONDITION, and it is the writer's own guard verbatim.  A bare root ("/", "//",
    # "///", "/ x") reaches here because no path component follows the separator.  An
    # earlier state also sent non-letter drives here only when the entire string was rooted;
    # the shared pattern now catches those drives even when embedded in prose.  Any survivor
    # is absolute to the guard, so leaving it makes the terminal write raise and persist
    # NOTHING -- X7 defeating X6 again.  Reduce to the final component, which is what both
    # patterns already do, and fall back to "<path>" when no component survives.
    #
    # Each flavour must reduce with ITS OWN parser: PurePosixPath(r"1:\dir") has no
    # separator at all, so its ``name`` is the whole Windows-rooted string and an "or"
    # chain hands the untouched value straight back to the guard.  Measured: that form
    # left 63 of 37,448 enumerated strings absolute.  One reduction per flavour is also
    # not enough -- the POSIX name of "/ :\\" is " :\\", which is absolute to the OTHER
    # flavour -- so this runs to a FIXPOINT.  Each pass is required to shorten the string
    # strictly, which bounds the loop by the input length; a pass that cannot shorten it
    # yields the whole value instead of returning something the writer would refuse.
    while _records_absolute_path(scrubbed):
        windows_rooted = PureWindowsPath(scrubbed).is_absolute()
        posix_rooted = PurePosixPath(scrubbed).is_absolute()
        # An EMBEDDED survivor -- a regex still matches, but the whole string is relative,
        # so ``PurePath.name`` has nothing to take.  Discarding the message is the only
        # way left to keep the writer's guard true, and it costs the reader the entire
        # reason, so it is a last resort rather than a working path.  MEASURED after the
        # substitution fixpoint above: it fires on 0 of the 37,448 enumerated strings and
        # on none of the prose battery, where a single substitution pass left six.  It is
        # kept because the guarantee has to hold for inputs nobody enumerated, and a
        # mutation sweep will report it as a survivor for exactly that reason.
        if not windows_rooted and not posix_rooted:
            scrubbed = "<path>"
            break
        reduced = (
            PureWindowsPath(scrubbed).name
            if windows_rooted
            else PurePosixPath(scrubbed).name
        )
        # ``not reduced`` is the live half: a bare root reduces to the empty string.
        # ``len(reduced) >= len(scrubbed)`` is ARITHMETIC, not a runtime check -- the name
        # of an absolute path is always a strict suffix of it -- and it is kept because it
        # makes termination a property of the code rather than of that argument.  It
        # survives a mutation sweep by construction; never call it a live guard.
        if not reduced or len(reduced) >= len(scrubbed):
            scrubbed = "<path>"
            break
        scrubbed = reduced
    return scrubbed


def describe_error(error: BaseException) -> str:
    """Return one scrubbed ``Type: message`` string safe to persist in an artifact."""

    return scrub_machine_paths(f"{type(error).__name__}: {error}")


def canonical_document_sha256(document: Mapping[str, Any]) -> str:
    """Return SHA-256 over the exact canonical-JSON serialization of a document."""

    return hashlib.sha256(canonical_json(document).encode("utf-8")).hexdigest()


def absolute_path_strings(value: Any) -> list[str]:
    """Return every string in a JSON-shaped value that records an absolute path.

    Inputs: any JSON-shaped value.  Outputs: the offending strings, in document order,
    from BOTH object-member names and values.
    Purpose: two places ask this question -- the writer, which refuses (X7), and the
    authorization gate, which refuses a plan the writer would later choke on.  They ask
    it of ONE function because a second copy could drift, and the gate exists precisely
    to guarantee what the writer will accept.
    """

    found: list[str] = []
    if isinstance(value, Mapping):
        for key, child in value.items():
            found.extend(absolute_path_strings(key))
            found.extend(absolute_path_strings(child))
    elif isinstance(value, Sequence) and not isinstance(value, (str, bytes)):
        for child in value:
            found.extend(absolute_path_strings(child))
    elif isinstance(value, str) and _records_absolute_path(value):
        found.append(value)
    return found


def write_canonical_document(path: Path, document: Mapping[str, Any]) -> Path:
    """Write canonical JSON with no machine path or non-finite token."""

    path.parent.mkdir(parents=True, exist_ok=True)
    offenders = absolute_path_strings(document)
    _require(
        not offenders,
        "X7: result artifact contains an absolute filesystem path: "
        + repr(offenders[0] if offenders else None),
    )
    payload = canonical_json(document)
    path.write_text(payload, encoding="utf-8", newline="")
    return path


def _fault_report(faults: Sequence[FaultSpec]) -> list[dict[str, Any]]:
    """Serialize every FaultSpec field by its exact dataclass name."""

    return [{field.name: getattr(fault, field.name) for field in dataclasses.fields(FaultSpec)}
            for fault in faults]


def build_extension_overrides(
    row: ExtensionRow, context: ExtensionContext,
) -> tuple[Any, ScreenOverrides, str, str]:
    """Build §11.3's exact payload, stamp it, and only then create ScreenOverrides."""

    reservation = screen_reservation(
        context.source,
        cell=SOURCE_CELL,
        sensor_seed=row.identity.sensor_seed,
        base_pair_id=row.identity.pair_id,
    )
    faults = screen_physical_faults(
        row.internal_condition,
        bound_trajectory(context.assignment),
        severity=row.severity,
        control_dt_s=context.timing.control_dt_s,
    )
    payload = {
        "base_config_hash": context.base_config_hash,
        "assignment_canonical_sha256": context.assignment_canonical_sha256,
        "assignment_hash": context.assignment_hash,
        "protocol_spec_sha256": context.protocol_spec_sha256,
        "extension_spec_sha256": context.extension_spec_sha256,
        "stage": row.stage,
        "substage": row.substage,
        "mass_index": row.mass.m,
        "distal_payload_mass_kg": row.mass.mass_kg,
        "condition": row.condition,
        "severity": row.severity,
        "replicate": row.replicate,
        "overrides": {
            "probe_peak_force_n": PROBE_PEAK_FORCE_N,
            "probe_ramp_fraction_of_duration": PROBE_RAMP_FRACTION,
            "physical_faults": _fault_report(faults),
            "realized_pair_id": row.identity.pair_id,
            "distal_payload_mass_kg": row.mass.mass_kg,
        },
        "reservation": {
            "scenario_spec_id": reservation.scenario_spec_id,
            "base_pair_id": reservation.base_pair_id,
            "sensor_seed": reservation.sensor_seed,
        },
    }
    canonical = canonical_json(payload)
    provenance = "dev-" + hashlib.sha256(canonical.encode("utf-8")).hexdigest()
    _require(provenance != context.base_config_hash,
             "extension provenance must differ from the base config hash")
    overrides = ScreenOverrides(
        probe_peak_force_n=PROBE_PEAK_FORCE_N,
        probe_ramp_fraction_of_duration=PROBE_RAMP_FRACTION,
        physical_faults=tuple(faults),
        realized_pair_id=row.identity.pair_id,
        distal_payload_mass_kg=row.mass.mass_kg,
        provenance_hash=provenance,
    )
    require_preregistered_faults(
        overrides.physical_faults,
        row.internal_condition,
        severity=row.severity,
        trajectory=bound_trajectory(context.assignment),
        control_dt_s=context.timing.control_dt_s,
    )
    return reservation, overrides, canonical, provenance


@dataclasses.dataclass(frozen=True)
class ExtensionPhysicalResult:
    """One extension rollout, including failed measurement evidence when necessary."""

    row: ExtensionRow
    extension_rollout_canonical: str
    rollout_provenance: str
    gate_report: Mapping[str, Any] | None
    coefficients: tuple[float, ...] | None
    n_steps: int | None
    elapsed_s: float
    error: str | None = None


class ExtensionLedger:
    """Mass-aware ledger with the extension's XA/XM stage vocabulary."""

    def __init__(self) -> None:
        """Create an empty physical-key and provenance-stamp index."""

        self._entries: dict[PhysicalKey, ExtensionPhysicalResult] = {}
        self._stamps: set[str] = set()

    def record(self, result: ExtensionPhysicalResult) -> None:
        """Record one distinct body after validating its independent key and stamp."""

        _require(result.row.stage in EXTENSION_STAGES, f"unknown origin stage {result.row.stage}")
        _require(result.row.substage in EXTENSION_SUBSTAGES,
                 f"unknown origin substage {result.row.substage}")
        key = result.row.physical
        _require(key not in self._entries, f"physical result already recorded for {key}")
        expected = "dev-" + hashlib.sha256(
            result.extension_rollout_canonical.encode("utf-8")
        ).hexdigest()
        _require(result.rollout_provenance == expected,
                 "rollout provenance does not hash the persisted canonical payload")
        _require(result.rollout_provenance not in self._stamps,
                 "two extension rollouts carry the same provenance stamp")
        self._entries[key] = result
        self._stamps.add(result.rollout_provenance)

    def get(self, row: ExtensionRow) -> ExtensionPhysicalResult:
        """Return the result for row's independently constructed physical key."""

        _require(row.physical in self._entries, f"no result recorded for row {row.key}")
        return self._entries[row.physical]

    def __len__(self) -> int:
        """Return the number of distinct extension physical results."""

        return len(self._entries)

    def values(self) -> tuple[ExtensionPhysicalResult, ...]:
        """Return recorded results in execution order."""

        return tuple(self._entries.values())


def measure_row(
    row: ExtensionRow, context: ExtensionContext, ledger: ExtensionLedger,
    *, execute: Callable[..., Any] = execute_rollout,
) -> ExtensionPhysicalResult:
    """Execute one row and persist even a returned-but-invalid measurement."""

    require_probe_torque_gate(PROBE_PEAK_FORCE_N)
    reservation, overrides, canonical, provenance = build_extension_overrides(row, context)
    started = time.perf_counter()
    try:
        outcome = execute(
            assignment=context.assignment,
            base_config_hash=context.base_config_hash,
            runtime=context.runtime,
            history_steps=context.history_steps,
            reservation=reservation,
            overrides=overrides,
        )
        _require(outcome.control_pair_id == row.identity.pair_id,
                 f"realized pair {outcome.control_pair_id!r} != {row.identity.pair_id!r}")
        gates = evaluate_hard_gates(
            outcome.plant, safety_events=outcome.safety_events,
            contact_steps=outcome.contact_steps,
        )
        coefficients = observation_coefficients(outcome.observation, context.timing)
        result = ExtensionPhysicalResult(
            row=row,
            extension_rollout_canonical=canonical,
            rollout_provenance=provenance,
            gate_report=dataclasses.asdict(gates),
            coefficients=coefficients,
            n_steps=int(outcome.plant.n_steps),
            elapsed_s=float(outcome.elapsed_s),
        )
    except Exception as error:  # persistence is the reason this boundary is broad
        result = ExtensionPhysicalResult(
            row=row,
            extension_rollout_canonical=canonical,
            rollout_provenance=provenance,
            gate_report=None,
            coefficients=None,
            n_steps=None,
            elapsed_s=float(time.perf_counter() - started),
            error=describe_error(error),
        )
    ledger.record(result)
    return result


def is_prefix(values: Sequence[float]) -> bool:
    """Return whether values form an initial prefix of the ascending LADDER."""

    present = set(float(value) for value in values)
    seen_absent = False
    for value in LADDER:
        if value not in present:
            seen_absent = True
        elif seen_absent:
            return False
    return True


def monotonicity_violations(testable: Mapping[float, Sequence[float]]) -> list[dict[str, Any]]:
    """Return every heavier-mass set-inclusion violation, ordered by ascending mass."""

    violations = []
    for light, heavy in itertools.combinations(sorted(testable), 2):
        gained = sorted(set(testable[heavy]) - set(testable[light]))
        if gained:
            violations.append({"lighter_mass_kg": light, "heavier_mass_kg": heavy,
                               "heavier_only_values": gained})
    return violations


def role_retained(mass: MassCell, values: Sequence[float]) -> bool:
    """Return whether a mass retains at least one severity reserved by its own role."""

    return bool(set(values) & set(ROLE_SEVERITY_MAP[mass.role_split]))


def classify_complete(
    testable_by_mass: Mapping[float, Sequence[float]], *, reduced: bool = False,
) -> str:
    """R7-R12: return exactly one ordered classifier outcome."""

    if reduced:
        return OUTCOME_REDUCED
    _require(set(testable_by_mass) == {item.mass_kg for item in MASS_CELLS},
             "complete classification requires all seven masses")
    if any(not is_prefix(values) for values in testable_by_mass.values()):
        return OUTCOME_NONPREFIX
    if monotonicity_violations(testable_by_mass):
        return OUTCOME_NONMONOTONE
    if any(not values for values in testable_by_mass.values()):
        return OUTCOME_EMPTY
    by_value = {item.mass_kg: item for item in MASS_CELLS}
    if any(not role_retained(by_value[mass], values)
           for mass, values in testable_by_mass.items()):
        return OUTCOME_ROLE_LOST
    return OUTCOME_ROLE_HELD


def option_b_cap(testable_by_mass: Mapping[float, Sequence[float]]) -> float | None:
    """Return the single R10/R11 longest role-retaining ascending-mass prefix cap."""

    cap = None
    for mass in ASCENDING_MASS_CELLS:
        values = testable_by_mass[mass.mass_kg]
        if not values or not role_retained(mass, values):
            break
        cap = mass.mass_kg
    return cap


def _empty_mass_entry(mass: MassCell, reason: str) -> dict[str, Any]:
    """Return the complete per-mass schema before that mass has run."""

    return {
        "mass_kg": mass.mass_kg,
        "m": mass.m,
        "role_split": mass.role_split,
        "q95": None,
        "threshold": None,
        "diagnostic_pause": None,
        "ladder_rows": [
            {
                "value": value,
                "ran": False,
                "d": None,
                "margin": None,
                "verdict": None,
                "hard_gates_passed": None,
                "fault_physical_key": physical_key_report(
                    ExtensionRow(mass, CONDITION_STRUCTURE, value, 0).physical
                ),
                "healthy_physical_key": physical_key_report(
                    ExtensionRow(mass, CONDITION_HEALTHY, None, 0).physical
                ),
                "fault_rollout_provenance": None,
                "reason": reason,
            }
            for value in LADDER
        ],
        "null_distances": [],
        "testable_set": None,
        "is_prefix": None,
        "role_retained": None,
        "excluded": False,
        "exclusion_reason": None,
        "reason": reason,
    }


def execute_document_skeleton(
    plan_document: Mapping[str, Any], approved_plan_digest: str,
) -> dict[str, Any]:
    """Return §11.2's complete execute-mode shape before any stage runs."""

    # A refusal artifact may have to carry a foreign, malformed plan.  Keep its raw
    # ``inputs`` field as evidence, but never assume that field is an object merely to
    # build the verdict-scope placeholders: doing so lets malformed content defeat X6.
    raw_inputs = plan_document.get("inputs")
    input_fields = raw_inputs if isinstance(raw_inputs, Mapping) else {}
    return {
        "inputs": raw_inputs,
        "protocol": plan_document.get("protocol"),
        "plan": plan_document.get("plan"),
        "approved_plan_canonical_sha256": approved_plan_digest,
        "mode": "execute",
        "results": {
            "replay_gate": {"ran": False, "passed": False, "elapsed_s": 0.0,
                            "reason": "stage XR has not run"},
            "preflight": {"ran": False, "passed": False, "plan_digest_match": False,
                          "per_mass_realized_delta": None,
                          "reason": "stage X0E has not run"},
            "anchor": {"ran": False, "verdict": None, "margins": [],
                       "cell_6_margins": cell_6_margin_rows(),
                       "constrained_rung_agreement": [], "testable_set": None,
                       "is_prefix": None, "reason": "stage XA has not run"},
            "per_mass": [_empty_mass_entry(mass, "mass has not run") for mass in MASS_CELLS],
            "masses_excluded": [],
            "shape_diagnostics": {"prefix_violations": [],
                                  "monotonicity_violations": []},
            "override_liveness": {"count": 0, "min_pairwise_distance": None,
                                  "passed": False, "reason": "stage XL has not run"},
            "outcome": None,
            "mass_coverage": None,
            "verdict_scope": {
                "environment_profile_id": input_fields.get(
                    "environment_profile_id"
                ),
                "contact_profile_id": input_fields.get(
                    "contact_profile_id"
                ),
                "trajectory_spec_id": input_fields.get(
                    "trajectory_spec_id"
                ),
                "probe_peak_force_n": input_fields.get(
                    "probe_peak_force_n"
                ),
                "probe_ramp_fraction_of_duration": input_fields.get(
                    "probe_ramp_fraction_of_duration"
                ),
                "masses_measured_kg": [],
                "statement": (
                    "development-only verdict over one environment, one contact profile, "
                    "one trajectory, one probe, and only the masses explicitly measured"
                ),
            },
            "terminal": None,
            "physical_ledger": [],
            "ledger_census": {"extension_physical_results": 0,
                              "distinct_stamps": 0, "distinct_identities": 0,
                              "identity_class_counts": {}},
            "census": {"extension_physical_rollouts": 0,
                       "replay_physical_rollouts": 0, "total_physical_rollouts": 0,
                       "logical_references": 0, "rollouts_by_stage": {}},
            "logical_reference_census": {"ladder_fault_references": 0,
                                         "ladder_healthy_references": 0,
                                         "null_endpoint_references": 0, "total": 0},
            "timing": {"extension_rollouts": 0, "replay_rollouts": 0,
                       "total_rollout_elapsed_s": 0.0,
                       "note": "executor wall clock; driver overhead excluded"},
            "step_counts": {},
        },
        "authority": AUTHORITY,
    }


def _ledger_entry(result: ExtensionPhysicalResult) -> dict[str, Any]:
    """Serialize one extension-owned physical result without losing its join fields."""

    return {
        "physical_key": physical_key_report(result.row.physical),
        "extension_rollout_canonical": result.extension_rollout_canonical,
        "rollout_provenance": result.rollout_provenance,
        "gate_report": result.gate_report,
        "coefficients": None if result.coefficients is None else list(result.coefficients),
        "n_steps": result.n_steps,
        "elapsed_s": result.elapsed_s,
        "stage_of_origin": result.row.stage,
        "substage_of_origin": result.row.substage,
        "error": result.error,
    }


def _populate_mass_entry(
    mass: MassCell,
    healthy: Mapping[int, ExtensionPhysicalResult],
    ladder: Mapping[float, ExtensionPhysicalResult],
    *, excluded_reason: str | None,
) -> dict[str, Any]:
    """Build one per-mass result and its 76-reference join when complete."""

    entry = _empty_mass_entry(mass, "ladder value was not run")
    entry["reason"] = None
    if len(healthy) == 8 and all(item.coefficients is not None for item in healthy.values()):
        distances = []
        for left_k, right_k in itertools.combinations(range(8), 2):
            left = healthy[left_k]
            right = healthy[right_k]
            distance = difference_statistic(left.coefficients, right.coefficients)
            distances.append({
                "left_physical_key": physical_key_report(left.row.physical),
                "right_physical_key": physical_key_report(right.row.physical),
                "distance": distance,
            })
        values = [item["distance"] for item in distances]
        q95 = float(np.quantile(values, QUANTILE, method=QUANTILE_METHOD))
        threshold = NULL_MULTIPLIER * q95
        entry["null_distances"] = distances
        entry["q95"] = q95
        entry["threshold"] = threshold
        entry["diagnostic_pause"] = q95 >= DIAGNOSTIC_PAUSE_Q95
    else:
        threshold = None

    rows = []
    healthy_zero = healthy.get(0)
    testable: list[float] = []
    for value in LADDER:
        result = ladder.get(value)
        row = _empty_mass_entry(mass, "unrun")["ladder_rows"][LADDER.index(value)]
        if result is not None:
            row["ran"] = True
            row["hard_gates_passed"] = (
                None if result.gate_report is None else bool(result.gate_report["passed"])
            )
            row["fault_rollout_provenance"] = result.rollout_provenance
            row["reason"] = result.error
            if result.coefficients is not None and healthy_zero is not None \
                    and healthy_zero.coefficients is not None and threshold is not None:
                distance = difference_statistic(result.coefficients, healthy_zero.coefficients)
                margin = distance - threshold
                row["d"] = distance
                row["margin"] = margin
                if row["hard_gates_passed"]:
                    row["verdict"] = "TESTABLE" if margin >= 0.0 else "SUB_THRESHOLD"
                    if margin >= 0.0:
                        testable.append(value)
                else:
                    row["verdict"] = "UNSAFE_LADDER_VALUE"
        rows.append(row)
    entry["ladder_rows"] = rows
    entry["testable_set"] = testable if excluded_reason is None else None
    entry["is_prefix"] = is_prefix(testable) if excluded_reason is None else None
    entry["role_retained"] = role_retained(mass, testable) if excluded_reason is None else None
    entry["excluded"] = excluded_reason is not None
    entry["exclusion_reason"] = excluded_reason
    return entry


def _attach_evidence(
    document: dict[str, Any], ledger: ExtensionLedger, *, replay_rollouts: int,
) -> None:
    """X6/X9: attach actual counts, joins, timing and steps on every execute exit."""

    results = document["results"]
    entries = [_ledger_entry(item) for item in ledger.values()]
    results["physical_ledger"] = entries
    identities = {(item.row.identity.sensor_seed, item.row.identity.pair_id)
                  for item in ledger.values()}
    identity_classes = Counter(item.row.replicate for item in ledger.values())
    results["ledger_census"] = {
        "extension_physical_results": len(entries),
        "distinct_stamps": len({item["rollout_provenance"] for item in entries}),
        "distinct_identities": len(identities),
        "identity_class_counts": {
            str(k): identity_classes[k] for k in sorted(identity_classes)
        },
    }
    ledger_keys = {canonical_json(entry["physical_key"]) for entry in entries}
    for mass in results["per_mass"]:
        for row in mass["ladder_rows"]:
            if row["ran"]:
                _require(canonical_json(row["fault_physical_key"]) in ledger_keys,
                         "a ladder row cites a fault key absent from the physical ledger")
                _require(canonical_json(row["healthy_physical_key"]) in ledger_keys,
                         "a ladder row cites a healthy key absent from the physical ledger")
        for pair in mass["null_distances"]:
            _require(canonical_json(pair["left_physical_key"]) in ledger_keys,
                     "a null distance cites a left key absent from the physical ledger")
            _require(canonical_json(pair["right_physical_key"]) in ledger_keys,
                     "a null distance cites a right key absent from the physical ledger")
    def stage_bucket(row: ExtensionRow) -> str:
        """Map a row to §8's XA, XM-C or XM-B occurrence bucket."""

        if row.mass.m == 0:
            return "XA"
        return "XM-C" if row.condition == CONDITION_HEALTHY else "XM-B"

    by_stage = Counter(stage_bucket(item.row) for item in ledger.values())
    ladder_refs = sum(
        1 for mass in results["per_mass"] for row in mass["ladder_rows"] if row["ran"]
    )
    null_pairs = sum(len(mass["null_distances"]) for mass in results["per_mass"])
    logical = {
        "ladder_fault_references": ladder_refs,
        "ladder_healthy_references": ladder_refs,
        "null_endpoint_references": 2 * null_pairs,
        "total": 2 * ladder_refs + 2 * null_pairs,
    }
    results["logical_reference_census"] = logical
    results["census"] = {
        "extension_physical_rollouts": len(entries),
        "replay_physical_rollouts": replay_rollouts,
        "total_physical_rollouts": len(entries) + replay_rollouts,
        "logical_references": logical["total"],
        "rollouts_by_stage": dict(sorted(by_stage.items())),
    }
    results["timing"] = {
        "extension_rollouts": len(entries),
        "replay_rollouts": replay_rollouts,
        "total_rollout_elapsed_s": float(
            sum(item.elapsed_s for item in ledger.values())
            + float(results["replay_gate"].get("elapsed_s", 0.0))
        ),
        "note": "executor wall clock; driver overhead excluded",
    }
    steps: Counter[str] = Counter()
    for item in ledger.values():
        if item.n_steps is not None:
            steps[stage_bucket(item.row)] += item.n_steps
    results["step_counts"] = dict(sorted(steps.items()))


def _shape_diagnostics(
    per_mass: Sequence[Mapping[str, Any]],
    testable: Mapping[float, Sequence[float]],
) -> dict[str, Any]:
    """Return §9.4's non-classifying magnitude report for every shape violation."""

    by_mass = {float(entry["mass_kg"]): entry for entry in per_mass}
    prefix: list[dict[str, Any]] = []
    for mass, values in testable.items():
        present = set(values)
        rows = {float(row["value"]): row for row in by_mass[mass]["ladder_rows"]}
        q95 = float(by_mass[mass]["q95"])
        for lower, higher in itertools.combinations(LADDER, 2):
            if lower not in present and higher in present:
                left = rows[lower]
                right = rows[higher]
                prefix.append({
                    "mass_kg": mass,
                    "lower_value": lower,
                    "higher_value": higher,
                    "lower_d": left["d"],
                    "higher_d": right["d"],
                    "threshold": by_mass[mass]["threshold"],
                    "absolute_d_difference": abs(float(left["d"]) - float(right["d"])),
                    "difference_in_max_q95_units": (
                        None if q95 == 0.0 else
                        abs(float(left["d"]) - float(right["d"])) / q95
                    ),
                })
    monotone: list[dict[str, Any]] = []
    for light, heavy in itertools.combinations(sorted(testable), 2):
        gained = sorted(set(testable[heavy]) - set(testable[light]))
        light_rows = {float(row["value"]): row for row in by_mass[light]["ladder_rows"]}
        heavy_rows = {float(row["value"]): row for row in by_mass[heavy]["ladder_rows"]}
        max_q95 = max(float(by_mass[light]["q95"]), float(by_mass[heavy]["q95"]))
        for value in gained:
            left_d = float(light_rows[value]["d"])
            right_d = float(heavy_rows[value]["d"])
            monotone.append({
                "lighter_mass_kg": light,
                "heavier_mass_kg": heavy,
                "value": value,
                "lighter_d": left_d,
                "heavier_d": right_d,
                "lighter_threshold": by_mass[light]["threshold"],
                "heavier_threshold": by_mass[heavy]["threshold"],
                "absolute_d_difference": abs(left_d - right_d),
                "difference_in_max_q95_units": (
                    None if max_q95 == 0.0 else abs(left_d - right_d) / max_q95
                ),
            })
    return {"prefix_violations": prefix, "monotonicity_violations": monotone}


def _finish(
    document: dict[str, Any], ledger: ExtensionLedger, *, outcome: str,
    stage: str, reason: str | None, replay_rollouts: int,
    mass_coverage: str | None = None,
) -> dict[str, Any]:
    """Persist exactly one R0-R12 outcome and all evidence accumulated so far."""

    _require(outcome in OUTCOMES, f"X14: unknown classifier result {outcome!r}")
    reason = None if reason is None else scrub_machine_paths(reason)
    results = document["results"]
    results["outcome"] = outcome
    results["mass_coverage"] = mass_coverage
    results["verdict_scope"]["masses_measured_kg"] = sorted({
        item.row.mass.mass_kg for item in ledger.values()
    })
    if outcome in OUTCOMES[:7]:
        results["terminal"] = {"rule": outcome, "reason": reason, "stage_reached": stage}
    else:
        results["terminal"] = None
    _attach_evidence(document, ledger, replay_rollouts=replay_rollouts)
    return document


RunRow = Callable[[ExtensionRow, ExtensionContext, ExtensionLedger], ExtensionPhysicalResult]


def run_extension(
    context: ExtensionContext,
    plan_document: Mapping[str, Any],
    approved_plan_digest: str,
    replay_report: Mapping[str, Any],
    *, run_row: RunRow = measure_row,
) -> dict[str, Any]:
    """Execute XA/XM-C/XL/XM-B/XZ in order using an extension-owned ledger."""

    document = execute_document_skeleton(plan_document, approved_plan_digest)
    results = document["results"]
    results["preflight"] = {
        "ran": True,
        "passed": True,
        "plan_digest_match": True,
        "per_mass_realized_delta": plan_document["preflight"]["per_mass_realized_delta"],
        "reason": None,
    }
    results["replay_gate"] = dict(replay_report)
    ledger = ExtensionLedger()
    healthy: dict[int, dict[int, ExtensionPhysicalResult]] = {mass.m: {} for mass in MASS_CELLS}
    ladders: dict[int, dict[float, ExtensionPhysicalResult]] = {mass.m: {} for mass in MASS_CELLS}
    exclusions: dict[int, str] = {}

    def consume(row: ExtensionRow) -> ExtensionPhysicalResult:
        """Run one planned row and convert a persisted invalid result to R2."""

        item = run_row(row, context, ledger)
        if item.error is not None or item.coefficients is None or item.gate_report is None:
            raise ProtocolPError(item.error or f"invalid measurement at {row.key}")
        return item

    try:
        anchor = MASS_CELLS[0]
        for k in range(8):
            item = consume(ExtensionRow(anchor, CONDITION_HEALTHY, None, k))
            healthy[anchor.m][k] = item
            if not item.gate_report["passed"]:
                results["per_mass"][anchor.m] = _populate_mass_entry(
                    anchor, healthy[anchor.m], ladders[anchor.m], excluded_reason=None
                )
                return _finish(document, ledger, outcome=OUTCOME_UNSAFE_ANCHOR,
                               stage="XA-XC", reason=f"anchor healthy k={k} failed hard gates",
                               replay_rollouts=1)
        for value in LADDER:
            item = consume(ExtensionRow(anchor, CONDITION_STRUCTURE, value, 0))
            ladders[anchor.m][value] = item
            if not item.gate_report["passed"]:
                results["per_mass"][anchor.m] = _populate_mass_entry(
                    anchor, healthy[anchor.m], ladders[anchor.m], excluded_reason=None
                )
                return _finish(document, ledger, outcome=OUTCOME_UNSAFE_ANCHOR,
                               stage="XA-XB", reason=f"anchor ladder {value} failed hard gates",
                               replay_rollouts=1)

        anchor_entry = _populate_mass_entry(
            anchor, healthy[anchor.m], ladders[anchor.m], excluded_reason=None
        )
        results["per_mass"][anchor.m] = anchor_entry
        agreement = []
        ladder_by_value = {row["value"]: row for row in anchor_entry["ladder_rows"]}
        for value in ANCHOR_CONSTRAINED_RUNGS:
            screen_verdict = cell_6_margin_rows()[LADDER.index(value)]["verdict"]
            extension_verdict = ladder_by_value[value]["verdict"]
            agreement.append({"value": value, "screen_verdict": screen_verdict,
                              "extension_verdict": extension_verdict,
                              "agrees": extension_verdict == screen_verdict})
        results["anchor"] = {
            "ran": True,
            "verdict": "X_ANCHOR_PASS" if all(row["agrees"] for row in agreement)
                       and anchor_entry["is_prefix"] else "X_ANCHOR_FAIL",
            "margins": anchor_entry["ladder_rows"],
            "cell_6_margins": cell_6_margin_rows(),
            "constrained_rung_agreement": agreement,
            "testable_set": anchor_entry["testable_set"],
            "is_prefix": anchor_entry["is_prefix"],
            "reason": None,
        }
        if not anchor_entry["is_prefix"]:
            return _finish(document, ledger, outcome=OUTCOME_ANCHOR_NONPREFIX,
                           stage="XA", reason="anchor TESTABLE_SET is not a prefix",
                           replay_rollouts=1)
        if not all(row["agrees"] for row in agreement):
            return _finish(document, ledger, outcome=OUTCOME_ANCHOR_FAIL,
                           stage="XA", reason="anchor disagrees at a constrained rung",
                           replay_rollouts=1)

        # Every non-anchor healthy block runs before liveness and before any ladder.
        for mass in MASS_CELLS[1:]:
            failed: list[int] = []
            for k in range(8):
                item = consume(ExtensionRow(mass, CONDITION_HEALTHY, None, k))
                healthy[mass.m][k] = item
                if not item.gate_report["passed"]:
                    failed.append(k)
            if failed:
                exclusions[mass.m] = f"healthy hard-gate failure at k={failed}"

        liveness_distances = []
        identical = []
        for k in range(8):
            for left_mass, right_mass in itertools.combinations(MASS_CELLS, 2):
                left = healthy[left_mass.m][k]
                right = healthy[right_mass.m][k]
                distance = difference_statistic(left.coefficients, right.coefficients)
                liveness_distances.append(distance)
                if left.coefficients == right.coefficients:
                    identical.append((left_mass.mass_kg, right_mass.mass_kg, k))
        _require(len(liveness_distances) == 168,
                 f"X8 requires 168 comparisons; got {len(liveness_distances)}")
        results["override_liveness"] = {
            "count": len(liveness_distances),
            "min_pairwise_distance": min(liveness_distances),
            "passed": not identical,
            "reason": None if not identical else f"identical vectors: {identical}",
        }
        if identical:
            for mass in MASS_CELLS[1:]:
                results["per_mass"][mass.m] = _populate_mass_entry(
                    mass, healthy[mass.m], ladders[mass.m],
                    excluded_reason=exclusions.get(mass.m),
                )
            return _finish(document, ledger, outcome=OUTCOME_OVERRIDE, stage="XL",
                           reason=f"{len(identical)} cross-mass healthy pairs were identical",
                           replay_rollouts=1)

        for mass in MASS_CELLS[1:]:
            if mass.m in exclusions:
                continue
            for value in LADDER:
                item = consume(ExtensionRow(mass, CONDITION_STRUCTURE, value, 0))
                ladders[mass.m][value] = item
                if not item.gate_report["passed"]:
                    exclusions[mass.m] = f"ladder hard-gate failure at remaining EI {value}"
                    break

        for mass in MASS_CELLS[1:]:
            results["per_mass"][mass.m] = _populate_mass_entry(
                mass, healthy[mass.m], ladders[mass.m],
                excluded_reason=exclusions.get(mass.m),
            )
        results["masses_excluded"] = [
            {"m": mass.m, "mass_kg": mass.mass_kg, "reason": exclusions[mass.m],
             "rollouts_spent": 8 + len(ladders[mass.m])}
            for mass in MASS_CELLS if mass.m in exclusions
        ]
        testable = {
            mass.mass_kg: results["per_mass"][mass.m]["testable_set"]
            for mass in MASS_CELLS if mass.m not in exclusions
        }
        if exclusions:
            outcome = OUTCOME_REDUCED
            coverage = "REDUCED"
        else:
            outcome = classify_complete(testable)
            coverage = "COMPLETE"
        diagnostics = (
            {"prefix_violations": [], "monotonicity_violations": []}
            if exclusions else _shape_diagnostics(results["per_mass"], testable)
        )
        diagnostics["option_b_cap_kg"] = None if exclusions else option_b_cap(testable)
        results["shape_diagnostics"] = diagnostics
        return _finish(document, ledger, outcome=outcome, stage="XZ", reason=None,
                       replay_rollouts=1, mass_coverage=coverage)
    except Exception as error:
        # Broad on purpose: this handler owns the ledger, so it is the only place that can
        # persist the rollouts already spent.  ProtocolPError is not the only class that
        # reaches here -- the override construction raises AssignmentGenerationError,
        # which is a ValueError -- and an escape would discard every rollout's evidence.
        for mass in MASS_CELLS:
            results["per_mass"][mass.m] = _populate_mass_entry(
                mass, healthy[mass.m], ladders[mass.m],
                excluded_reason=exclusions.get(mass.m),
            )
        return _finish(document, ledger, outcome=OUTCOME_INVALID,
                       stage="measurement", reason=describe_error(error),
                       replay_rollouts=1)


class ReplayGateFailure(ProtocolPError):
    """Replay failure carrying whether the one physical rollout was actually spent."""

    def __init__(self, message: str, *, rollout_spent: int, elapsed_s: float) -> None:
        """Preserve the gate's actual count and executor time for the terminal artifact."""

        super().__init__(message)
        self.rollout_spent = int(rollout_spent)
        self.elapsed_s = float(elapsed_s)


def resolve_replay_source(context: ExtensionContext) -> tuple[Any, Any]:
    """Return the delivered reservation and manifest row Protocol P section 7 replays.

    Inputs: the bound extension context.  Outputs: ``(reservation, identity_row)``.
    Purpose: every check that must hold *before* the gate spends its one rollout lives
    here, so the whole pre-rollout surface is reachable by a test at zero cost.

    The scenario id is **imported** from the approved gate rather than re-typed.  A
    pinned literal that also lives in a bound module is checked by equality, never by
    adoption; a re-typed copy names a different delivered row and the divergence is
    invisible until the rollout is already spent.
    """

    # CODE GUARD, not a runtime check: the gate module derives RUN_ID from
    # SCENARIO_SPEC_ID, so while both are imported no reachable state fails this.  It
    # goes live the moment either is re-typed here, which is the defect it exists for.
    # It survives a mutation sweep by construction; never count it as coverage.
    _require(REPLAY_RUN_ID.startswith(f"{REPLAY_SCENARIO_SPEC_ID}_"),
             f"replay run id {REPLAY_RUN_ID!r} does not name the gate's scenario "
             f"{REPLAY_SCENARIO_SPEC_ID!r}")
    rows, reservations = build_identity_manifest(
        context.binding, splits=("dev",), suites=("C0", "C1", "S")
    )
    selected = [
        item for item in reservations
        if item.scenario_spec_id == REPLAY_SCENARIO_SPEC_ID
    ]
    _require(
        len(selected) == 1,
        "replay source reservation is not unique in the dev manifest",
    )
    identity_rows = [row for row in rows if row.run_id == REPLAY_RUN_ID]
    _require(
        len(identity_rows) == 1,
        "replay identity row is not unique in the dev manifest",
    )
    # Live only in combination with the line above: with the scenario id imported the
    # equality is forced, and removing this check alone changes nothing.  Removing BOTH
    # -- a re-typed scenario id and no pair-id check -- is the state that reaches a
    # rollout against the wrong delivered row, and the swept double removal is caught.
    _require(
        screen_pair_id(selected[0], None) == identity_rows[0].pair_id,
        "overrides=None does not reproduce the delivered pair id",
    )
    return selected[0], identity_rows[0]


def run_replay_gate(
    context: ExtensionContext, *, data_root: Path, config_path: Path,
    schema_path: Path, assignment_path: Path, protocol_path: Path,
) -> dict[str, Any]:
    """Run Protocol P's ordinary-path replay gate while constructing dev only."""

    started = time.perf_counter()
    rollout_spent = 0
    rollout_elapsed = 0.0
    try:
        plant_reference = data_root / "plant" / f"{REPLAY_RUN_ID}.npz"
        observation_reference = data_root / "observations" / REPLAY_SUITE / f"{REPLAY_RUN_ID}.npz"
        check_pinned_digests(
            protocol_path, assignment_path, plant_reference, observation_reference
        )
        watched_recursive = [data_root, PACKET_ROOT]
        before = inventory(watched_recursive, shallow_roots=[REPO_ROOT])
        reservation, identity_row = resolve_replay_source(context)
        rollout_started = time.perf_counter()
        rollout_spent = 1
        control_pair_id, plant, observations, _labels, safety_events, contact_steps = (
            _generate_reservation(
                context.assignment,
                context.base_config_hash,
                (REPLAY_SUITE,),
                None,
                context.history_steps,
                context.runtime,
                reservation,
                overrides=None,
            )
        )
        rollout_elapsed = time.perf_counter() - rollout_started
        _require(
            control_pair_id == identity_row.pair_id,
            "replay realized the wrong pair id",
        )
        _require(set(observations) == {REPLAY_SUITE}, "replay returned the wrong suite set")
        retained: dict[str, str] | None = None
        with (data_root / "manifest.csv").open("r", encoding="utf-8", newline="") as handle:
            for item in csv.DictReader(handle):
                if item.get("run_id") == REPLAY_RUN_ID:
                    _require(retained is None, "retained replay manifest row is duplicated")
                    retained = dict(item)
        _require(retained is not None, "retained replay manifest row is absent")
        compare_manifest_row(retained, identity_row)
        observation = observations[REPLAY_SUITE]
        _require(
            observation.config_hash == context.base_config_hash,
            "ordinary replay did not stamp the base config hash",
        )
        plant_payload = {
            field.name: np.asarray(getattr(plant, field.name))
            for field in dataclasses.fields(plant)
        }
        compare_payload(
            "plant", load_npz_entries(plant_reference), plant_payload,
            N_PRIVILEGED_FIELDS,
        )
        compare_payload(
            "observation", load_npz_entries(observation_reference),
            observation.to_npz_dict(), N_OBSERVATION_ENTRIES,
        )
        after = inventory(watched_recursive, shallow_roots=[REPO_ROOT])
        require_no_inventory_changes(diff_inventory(before, after))
        return {"ran": True, "passed": True, "elapsed_s": rollout_elapsed,
                "reason": None, "safety_events": int(safety_events),
                "contact_steps": int(contact_steps),
                "total_gate_elapsed_s": float(time.perf_counter() - started)}
    except Exception as error:
        if rollout_spent and rollout_elapsed == 0.0:
            rollout_elapsed = time.perf_counter() - rollout_started
        raise ReplayGateFailure(
            describe_error(error),
            rollout_spent=rollout_spent,
            elapsed_s=rollout_elapsed,
        ) from error


def strict_read_json(path: Path) -> Any:
    """Read JSON that can be represented by the packet's canonical UTF-8 rule."""

    def pairs(items: Sequence[tuple[str, Any]]) -> dict[str, Any]:
        """Build one object while refusing a repeated member name."""

        result: dict[str, Any] = {}
        for key, value in items:
            if key in result:
                raise ProtocolPError(f"duplicate JSON key {key!r} in {path.name}")
            result[key] = value
        return result

    try:
        document = json.loads(
            path.read_text(encoding="utf-8-sig"),
            object_pairs_hook=pairs,
            parse_constant=lambda token: (_ for _ in ()).throw(
                ProtocolPError(f"non-finite JSON token {token!r}")
            ),
        )
    except (OSError, UnicodeError, json.JSONDecodeError) as error:
        raise ProtocolPError(f"could not read strict JSON {path.name}: {error}") from error
    # The authorization and failure-persistence visitors are deliberately recursive for
    # clarity.  A foreign plan can otherwise sit in the narrow range that Python's JSON
    # decoder accepts but those visitors cannot traverse; the authorization failure then
    # enters the scrubber, raises ``RecursionError`` again, and defeats X6.  Measure depth
    # iteratively here and reject far above the official plan's actual depth.
    stack: list[tuple[Any, int]] = [(document, 0)]
    while stack:
        value, depth = stack.pop()
        _require(
            depth <= MAX_PLAN_JSON_DEPTH,
            f"strict JSON {path.name} exceeds maximum nesting depth "
            f"{MAX_PLAN_JSON_DEPTH}",
        )
        if isinstance(value, Mapping):
            stack.extend((child, depth + 1) for child in value.values())
        elif isinstance(value, Sequence) and not isinstance(value, (str, bytes)):
            stack.extend((child, depth + 1) for child in value)
    # ``json.loads`` accepts two values the packet cannot persist: an exponent that
    # overflows to ``inf`` without using the literal token ``Infinity``, and an escaped
    # lone surrogate that cannot be encoded as UTF-8.  Reject both at the read boundary;
    # otherwise authorization fails later and the X6 failure writer crashes on the same
    # value, leaving no artifact at all.
    try:
        canonical_json(document).encode("utf-8")
    except (TypeError, ValueError, UnicodeError) as error:
        raise ProtocolPError(
            f"strict JSON {path.name} is not canonical UTF-8 data: {error}"
        ) from error
    return document


def require_authorized_plan(
    document: Any, authorized_digest: str,
) -> str:
    """Refuse anything except a passing X0P plan named by its lowercase canonical digest."""

    _require(isinstance(document, Mapping), "approved plan must be a JSON object")
    _require(document.get("mode") == "plan", "approved artifact is not a plan-mode artifact")
    _require(document.get("plan_valid") is True, "only a plan with plan_valid=true may execute")
    _require(document.get("terminal") is None, "a terminal plan artifact may not execute")
    _require(
        isinstance(authorized_digest, str)
        and _PLAN_DIGEST.fullmatch(authorized_digest) is not None,
        "authorized plan digest must be one lowercase SHA-256",
    )
    actual = canonical_document_sha256(document)
    _require(actual == authorized_digest,
             f"plan digest {actual} != authorized digest {authorized_digest}")
    # Everything downstream of this line embeds the approved plan VERBATIM, which is
    # deliberate: silently rewriting content both agents read and named would be worse
    # than the risk it removes.  That decision rests on a premise -- "plan mode's own
    # writer refuses an absolute path, so a plan this tool wrote cannot carry one" -- and
    # a premise a gate relies on is a thing to CHECK, not to assume.  Measured before this
    # existed: a foreign plan carrying an absolute path whose own digest is named passes
    # authorization, and the X0E-mismatch exit then dies inside the terminal write with
    # nothing on disk.  Refusing here is not a rewrite; the refusal routes to the exit
    # that scrubs, so the record still gets written and it names the reason.
    offenders = absolute_path_strings(document)
    _require(
        not offenders,
        "the named plan records an absolute filesystem path and so cannot be an X0P "
        "artifact this tool wrote: " + repr(offenders[0] if offenders else None),
    )
    return actual


def parse_args(argv: Sequence[str] | None = None) -> argparse.Namespace:
    """Parse the zero-rollout-default command line."""

    parser = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    parser.add_argument("--mode", choices=("plan", "execute"), default="plan")
    parser.add_argument("--output-dir", type=Path,
                        default=Path("results/payload_boundary_extension"))
    parser.add_argument("--schema", type=Path, default=Path("schema/schema.json"))
    parser.add_argument("--config", type=Path,
                        default=Path("config/draft-config-v0.1.json"))
    parser.add_argument("--assignment", type=Path,
                        default=Path(f"config/{ASSIGNMENT_FILENAME}"))
    parser.add_argument("--protocol", type=Path,
                        default=Path(f"protocol/{PROTOCOL_FILENAME}"))
    parser.add_argument("--extension", type=Path,
                        default=Path(f"protocol/{EXTENSION_FILENAME}"))
    parser.add_argument("--plan", type=Path, default=None,
                        help="approved plan path; defaults to OUTPUT_DIR/plan.json")
    parser.add_argument("--approved-plan-sha256", default=None,
                        help="required in execute mode and named by joint authorization")
    parser.add_argument("--data-root", type=Path, default=None,
                        help="retained development dataset; required in execute mode")
    return parser.parse_args(argv)


def _scrub_embedded_strings(value: Any) -> tuple[Any, bool]:
    """Scrub every string inside foreign content, reporting whether anything changed.

    Inputs: any JSON-shaped value read from a file this run did not write.  Outputs: the
    same shape with every string scrubbed, and whether any string actually changed.
    Purpose: X6 requires the artifact on every execute exit and X7 makes the writer
    REFUSE an absolute path, so foreign content embedded verbatim turns the terminal
    write into an uncaught refusal that persists nothing -- X7 defeating X6.  The caller
    discloses the redaction rather than performing it silently.
    """

    if isinstance(value, Mapping):
        changed = False
        scrubbed_map: dict[str, Any] = {}
        for key, child in value.items():
            scrubbed_key = scrub_machine_paths(key) if isinstance(key, str) else key
            changed = changed or scrubbed_key != key
            # Two different machine paths can reduce to the same basename.  Preserve
            # both fields deterministically rather than letting redaction erase one.
            candidate = scrubbed_key
            suffix = 2
            while candidate in scrubbed_map:
                candidate = f"{scrubbed_key} [redacted-key-{suffix}]"
                suffix += 1
                changed = True
            scrubbed_map[candidate], child_changed = _scrub_embedded_strings(child)
            changed = changed or child_changed
        return scrubbed_map, changed
    if isinstance(value, Sequence) and not isinstance(value, (str, bytes)):
        pairs = [_scrub_embedded_strings(child) for child in value]
        return [item for item, _ in pairs], any(flag for _, flag in pairs)
    if isinstance(value, str):
        scrubbed_text = scrub_machine_paths(value)
        return scrubbed_text, scrubbed_text != value
    return value, False


def persist_execute_failure(
    output_dir: Path, plan_document: Any, approved_plan_digest: Any,
    *, outcome: str, stage: str, reason: str,
) -> None:
    """X6: write the execute-mode artifact for a failure that precedes any measurement.

    Inputs: the output directory, whatever plan content exists, the digest the caller
    named, and the classified failure.  Outputs: none; the artifact is written.
    Purpose: §11.2 requires the field set on EVERY execute-mode exit, and an exit that
    prints to the console and returns leaves no record that the run was attempted.

    Every failure this function serves is a failure to establish that the named plan is
    the authorized one, so BOTH the plan content and the named digest are attacker- or
    typo-shaped input.  Neither may reach the writer unscrubbed: the plan content is
    scrubbed, and a digest that is not the pinned lowercase SHA-256 shape is recorded as
    null.  Both redactions are named in the persisted reason.
    """

    content, redacted = _scrub_embedded_strings(
        plan_document if isinstance(plan_document, Mapping) else {}
    )
    if redacted:
        reason = (
            reason + "; the named plan carried an absolute filesystem path, so the "
            "content embedded in this artifact was scrubbed (X7)"
        )
    if not (isinstance(approved_plan_digest, str)
            and _PLAN_DIGEST.fullmatch(approved_plan_digest)):
        if approved_plan_digest is not None:
            reason = (
                reason + "; the named authority argument is not one lowercase SHA-256, "
                "so it is recorded as null rather than published (X7)"
            )
        approved_plan_digest = None
    document = execute_document_skeleton(content, approved_plan_digest)
    document["results"]["preflight"] = {
        "ran": True, "passed": False, "plan_digest_match": False,
        "per_mass_realized_delta": None, "reason": reason,
    }
    final = _finish(document, ExtensionLedger(), outcome=outcome, stage=stage,
                    reason=reason, replay_rollouts=0)
    write_canonical_document(output_dir / RESULT_FILENAME, final)


def main(argv: Sequence[str] | None = None) -> int:
    """Write a zero-rollout plan, or execute once against an explicitly named plan."""

    args = parse_args(argv)
    output_dir = args.output_dir.resolve()
    plan_path = (args.plan or (output_dir / PLAN_FILENAME)).resolve()
    try:
        context = resolve_context(
            config_path=args.config.resolve(), schema_path=args.schema.resolve(),
            assignment_path=args.assignment.resolve(), protocol_path=args.protocol.resolve(),
            extension_path=args.extension.resolve(),
        )
    except Exception as error:
        if args.mode == "plan":
            document = failed_plan_document(describe_error(error))
            write_canonical_document(output_dir / PLAN_FILENAME, document)
        else:
            persist_execute_failure(
                output_dir, None, args.approved_plan_sha256,
                outcome=OUTCOME_CONSTRUCTION, stage="X0E", reason=describe_error(error),
            )
        print(f"FAILED: {error}")
        return 1

    if args.mode == "plan":
        try:
            document = build_plan_document(context)
        except Exception as error:
            document = failed_plan_document(describe_error(error))
        written = write_canonical_document(output_dir / PLAN_FILENAME, document)
        print(f"plan_valid={document['plan_valid']} rollouts=0")
        print(f"canonical_sha256={canonical_document_sha256(document)}")
        print(f"wrote {written}")
        return 0 if document["plan_valid"] else 1

    if args.approved_plan_sha256 is None or args.data_root is None:
        missing = [
            name for name, value in (
                ("--approved-plan-sha256", args.approved_plan_sha256),
                ("--data-root", args.data_root),
            )
            if value is None
        ]
        reason = "execute mode requires " + " and ".join(missing)
        persist_execute_failure(
            output_dir, None, args.approved_plan_sha256,
            outcome=OUTCOME_CONSTRUCTION, stage="X0E", reason=reason,
        )
        print(f"FAILED: {reason}")
        return 1
    try:
        approved = strict_read_json(plan_path)
    except Exception as error:
        persist_execute_failure(
            output_dir, None, args.approved_plan_sha256,
            outcome=OUTCOME_CONSTRUCTION, stage="X0E", reason=describe_error(error),
        )
        print(f"FAILED: {error}")
        return 1
    try:
        approved_digest = require_authorized_plan(approved, args.approved_plan_sha256)
    except Exception as error:
        persist_execute_failure(
            output_dir, approved, args.approved_plan_sha256,
            outcome=OUTCOME_CONSTRUCTION, stage="X0E", reason=describe_error(error),
        )
        print(f"FAILED: {error}")
        return 1
    document = execute_document_skeleton(approved, args.approved_plan_sha256)
    try:
        recomputed = build_plan_document(context)
        _require(canonical_json(recomputed) == canonical_json(approved),
                 "X0E recomputed plan content differs from the approved plan")
    except Exception as error:
        document["results"]["preflight"] = {
            "ran": True, "passed": False, "plan_digest_match": False,
            "per_mass_realized_delta": None, "reason": describe_error(error),
        }
        final = _finish(document, ExtensionLedger(), outcome=OUTCOME_CONSTRUCTION,
                        stage="X0E", reason=document["results"]["preflight"]["reason"],
                        replay_rollouts=0)
        write_canonical_document(output_dir / RESULT_FILENAME, final)
        print(f"FAILED: {error}")
        return 1
    try:
        replay = run_replay_gate(
            context, data_root=args.data_root.resolve(), config_path=args.config.resolve(),
            schema_path=args.schema.resolve(), assignment_path=args.assignment.resolve(),
            protocol_path=args.protocol.resolve(),
        )
    except Exception as error:
        # The gate raises ReplayGateFailure carrying whether its one rollout was actually
        # spent.  Read them off THIS exception: taking them from anywhere else reports a
        # cost the run did not incur, or loses one it did.
        replay_rollouts = int(getattr(error, "rollout_spent", 0))
        replay_elapsed = float(getattr(error, "elapsed_s", 0.0))
        document["results"]["preflight"] = {
            "ran": True, "passed": True, "plan_digest_match": True,
            "per_mass_realized_delta": recomputed["preflight"]["per_mass_realized_delta"],
            "reason": None,
        }
        document["results"]["replay_gate"] = {
            "ran": True, "passed": False, "elapsed_s": replay_elapsed,
            "reason": describe_error(error),
        }
        final = _finish(document, ExtensionLedger(), outcome=OUTCOME_REPLAY,
                        stage="XR", reason=document["results"]["replay_gate"]["reason"],
                        replay_rollouts=replay_rollouts)
        write_canonical_document(output_dir / RESULT_FILENAME, final)
        print(f"FAILED: {error}")
        return 1
    try:
        final = run_extension(context, approved, approved_digest, replay)
    except Exception as error:
        # run_extension classifies every measurement failure itself and owns the ledger.
        # Reaching here means the artifact assembly itself failed, so the ledger is gone
        # and the census below is NOT a rollout count -- the reason says so rather than
        # letting a zero be read as "nothing ran".
        document["results"]["preflight"] = {
            "ran": True, "passed": True, "plan_digest_match": True,
            "per_mass_realized_delta": recomputed["preflight"]["per_mass_realized_delta"],
            "reason": None,
        }
        document["results"]["replay_gate"] = dict(replay)
        final = _finish(
            document, ExtensionLedger(), outcome=OUTCOME_INVALID, stage="measurement",
            reason=(
                "result assembly failed after the measurement stages; the rollout counts "
                "in this artifact are UNKNOWN rather than zero: "
                + describe_error(error)
            ),
            replay_rollouts=1,
        )
        write_canonical_document(output_dir / RESULT_FILENAME, final)
        print(f"FAILED: {error}")
        return 1
    written = write_canonical_document(output_dir / RESULT_FILENAME, final)
    print(f"outcome={final['results']['outcome']}")
    print(f"rollouts={final['results']['census']['total_physical_rollouts']}")
    print(f"wrote {written}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
