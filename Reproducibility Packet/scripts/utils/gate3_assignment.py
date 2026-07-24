"""Gate-3 scenario/split assignment contract and deterministic expansion.

The tracked assignment is a proposal for joint review.  It reserves identities
and fixes grids, but it cannot authorize research-payload generation.  Real
generation remains behind the separately validated frozen ``config.json``
lifecycle gate.
"""

from __future__ import annotations

import copy
import hashlib
import json
from collections import Counter
from dataclasses import asdict, dataclass
from pathlib import Path
from typing import Any, Mapping

from .config_contract import ValidatedConfig

SPLITS = ("dev", "pilot", "val", "test")
SUITES = ("C0", "C1", "S", "O")
KNOWN_SOURCE_CLASSES = ("healthy", "structure", "actuator", "sensor")
FAULT_SOURCE_CLASSES = ("structure", "actuator", "sensor")
SENSOR_SUBTYPES = ("encoder_bias", "encoder_drift", "encoder_dropout")
APPROVAL_TOKEN = "APPROVE_GATE3_ASSIGNMENT_V0_1"
PROPOSED_DECISION = "PENDING_JOINT_APPROVAL_GATE3_ASSIGNMENT_V0_1"
BALANCED_CONTEXT_CELL_TABLE = (
    (0, 0, 0),
    (0, 1, 1),
    (1, 0, 1),
    (1, 1, 0),
    (0, 0, 1),
    (0, 1, 0),
    (1, 0, 0),
    (1, 1, 1),
)

TOP_LEVEL_KEYS = {
    "assignment_version",
    "schema_version",
    "status",
    "decision",
    "draft_config_hash",
    "assignment_hash",
    "required_same_state_approval",
    "research_payload_generation_allowed",
    "test_payload_generation_allowed",
    "evidence_boundary",
    "suite_protocol",
    "split_policy",
    "generation_plan",
    "trajectory_specs",
    "fault_grid_by_split",
    "compound_ood_settings",
    "context_profiles",
    "implementation_requirements",
}


class Gate3AssignmentError(ValueError):
    """Raised when the proposed Gate-3 assignment is incomplete or unsafe."""


@dataclass(frozen=True)
class ScenarioReservation:
    """One suite-independent whole scenario/fault realization reservation."""

    schema_version: str
    draft_config_hash: str
    scenario_spec_id: str
    base_pair_id: str
    trajectory_spec_id: str
    fault_setting_id: str
    split_group_id: str
    split: str
    payload_id: str
    env_profile_id: str
    contact_profile_id: str
    sim_seed: int
    fault_seed: int
    sensor_seed: int
    controller_seed: int


def _json_load_strict(path: Path) -> dict[str, Any]:
    """Load one JSON object while rejecting duplicate keys and non-finite values."""

    def reject_constant(value: str) -> None:
        raise Gate3AssignmentError(f"non-finite JSON constant is forbidden: {value}")

    def unique_object(pairs: list[tuple[str, Any]]) -> dict[str, Any]:
        document: dict[str, Any] = {}
        for key, value in pairs:
            if key in document:
                raise Gate3AssignmentError(f"duplicate JSON key is forbidden: {key}")
            document[key] = value
        return document

    try:
        loaded = json.loads(
            Path(path).read_text(encoding="utf-8"),
            parse_constant=reject_constant,
            object_pairs_hook=unique_object,
        )
    except json.JSONDecodeError as exc:
        raise Gate3AssignmentError(f"invalid JSON in {path}: {exc}") from exc
    if not isinstance(loaded, dict):
        raise Gate3AssignmentError(f"{path} must contain one JSON object")
    return loaded


def load_assignment(path: Path) -> dict[str, Any]:
    """Load one strict proposed assignment document."""

    return _json_load_strict(Path(path))


def canonical_assignment_bytes(document: Mapping[str, Any]) -> bytes:
    """Return canonical JSON bytes with the self-referential hash omitted."""

    payload = copy.deepcopy(dict(document))
    payload.pop("assignment_hash", None)
    try:
        rendered = json.dumps(
            payload,
            sort_keys=True,
            separators=(",", ":"),
            ensure_ascii=False,
            allow_nan=False,
        )
    except (TypeError, ValueError) as exc:
        raise Gate3AssignmentError(
            f"assignment is not canonical-JSON serializable: {exc}"
        ) from exc
    return rendered.encode("utf-8")


def expected_assignment_hash(document: Mapping[str, Any]) -> str:
    """Return the development-qualified canonical assignment hash."""

    return f"dev-{hashlib.sha256(canonical_assignment_bytes(document)).hexdigest()}"


def _require_exact_keys(
    value: Mapping[str, Any],
    expected: set[str],
    label: str,
) -> None:
    """Require an exact mapping key allowlist."""

    actual = set(value)
    if actual != expected:
        raise Gate3AssignmentError(
            f"{label} keys mismatch; "
            f"missing={sorted(expected - actual)}, forbidden={sorted(actual - expected)}"
        )


def _require_unique_ids(items: list[Mapping[str, Any]], label: str) -> None:
    """Require nonempty, unique string ids in one catalog."""

    ids = [item.get("id") for item in items]
    if any(not isinstance(item_id, str) or not item_id for item_id in ids):
        raise Gate3AssignmentError(f"{label} ids must be nonempty strings")
    if len(ids) != len(set(ids)):
        raise Gate3AssignmentError(f"{label} ids must be unique")


def _finite_number(value: Any, label: str, *, minimum: float | None = None) -> float:
    """Return one finite numeric value subject to an optional lower bound."""

    if isinstance(value, bool) or not isinstance(value, (int, float)):
        raise Gate3AssignmentError(f"{label} must be numeric")
    number = float(value)
    if not (-float("inf") < number < float("inf")):
        raise Gate3AssignmentError(f"{label} must be finite")
    if minimum is not None and number < minimum:
        raise Gate3AssignmentError(f"{label} must be >= {minimum}")
    return number


def _severity_token(value: float) -> str:
    """Render one compact stable id token for a numeric severity."""

    rendered = format(float(value), ".12g")
    return rendered.replace("-", "m").replace(".", "p")


def expanded_fault_settings(document: Mapping[str, Any]) -> list[dict[str, Any]]:
    """Expand compact known-class grids plus explicit compound/OOD settings."""

    settings: list[dict[str, Any]] = []
    grids = document["fault_grid_by_split"]
    for split in SPLITS:
        grid = grids[split]
        settings.append(
            {
                "id": f"fault_{split}_healthy",
                "split": split,
                "label": {
                    "source_class": "healthy",
                    "subtype": "none",
                    "location": -1,
                    "severity": 0.0,
                    "compound_flag": False,
                    "ood_flag": False,
                },
                "components": [],
            }
        )
        for source_class in ("structure", "actuator"):
            family = grid[source_class]
            for location in family["locations"]:
                for severity in family["severities"]:
                    subtype = family["subtype"]
                    setting_id = (
                        f"fault_{split}_{source_class}_{subtype}"
                        f"_loc{location}_sev{_severity_token(severity)}"
                    )
                    component = {
                        "source_class": source_class,
                        "subtype": subtype,
                        "location": location,
                        "severity": severity,
                    }
                    settings.append(
                        {
                            "id": setting_id,
                            "split": split,
                            "label": {
                                **component,
                                "compound_flag": False,
                                "ood_flag": False,
                            },
                            "components": [component],
                        }
                    )
        for family in grid["sensor"]:
            for location in family["locations"]:
                for severity in family["severities"]:
                    subtype = family["subtype"]
                    setting_id = (
                        f"fault_{split}_sensor_{subtype}"
                        f"_loc{location}_sev{_severity_token(severity)}"
                    )
                    component = {
                        "source_class": "sensor",
                        "subtype": subtype,
                        "location": location,
                        "severity": severity,
                    }
                    settings.append(
                        {
                            "id": setting_id,
                            "split": split,
                            "label": {
                                **component,
                                "compound_flag": False,
                                "ood_flag": False,
                            },
                            "components": [component],
                        }
                    )
    settings.extend(copy.deepcopy(document["compound_ood_settings"]))
    return settings


def _validate_trajectory_specs(
    document: Mapping[str, Any],
    config: ValidatedConfig,
) -> None:
    """Validate split ownership, bounded timing, and both excitation conditions."""

    trajectories = document["trajectory_specs"]
    if not isinstance(trajectories, list) or not trajectories:
        raise Gate3AssignmentError("trajectory_specs must be a nonempty list")
    _require_unique_ids(trajectories, "trajectory_specs")
    expected_keys = {
        "id",
        "split",
        "excitation",
        "target_joint_rad",
        "onset_time_s",
        "duration_s",
        "relative_task_events_s",
        "diagnostic_probe",
    }
    analysis_window_s = float(config.document["values"]["timing"]["analysis_window_s"])
    configured_probe = config.document["values"]["timing"]["diagnostic_probe"]
    excitation_by_split = {split: set() for split in SPLITS}
    for item in trajectories:
        _require_exact_keys(item, expected_keys, f"trajectory {item.get('id')}")
        split = item["split"]
        if split not in SPLITS:
            raise Gate3AssignmentError(f"trajectory {item['id']} has invalid split")
        excitation = item["excitation"]
        if excitation not in {"ordinary", "diagnostic"}:
            raise Gate3AssignmentError(f"trajectory {item['id']} has invalid excitation")
        excitation_by_split[split].add(excitation)
        target = item["target_joint_rad"]
        if (
            not isinstance(target, list)
            or len(target) != 2
            or any(abs(_finite_number(value, "target_joint_rad")) > 0.45 for value in target)
        ):
            raise Gate3AssignmentError(
                f"trajectory {item['id']} target_joint_rad must be two values within +/-0.45"
            )
        onset = _finite_number(item["onset_time_s"], "onset_time_s", minimum=0.0)
        duration = _finite_number(item["duration_s"], "duration_s", minimum=0.0)
        if duration < onset + analysis_window_s:
            raise Gate3AssignmentError(
                f"trajectory {item['id']} does not cover onset plus analysis window"
            )
        events = item["relative_task_events_s"]
        _require_exact_keys(
            events,
            {"movement_start", "transition", "hold_end", "return_end"},
            f"trajectory {item['id']} relative_task_events_s",
        )
        movement = _finite_number(events["movement_start"], "movement_start", minimum=0.0)
        transition = _finite_number(events["transition"], "transition", minimum=0.001)
        hold_end = _finite_number(events["hold_end"], "hold_end", minimum=0.0)
        return_end = _finite_number(events["return_end"], "return_end", minimum=0.0)
        if movement + transition > hold_end or return_end - transition < hold_end:
            raise Gate3AssignmentError(f"trajectory {item['id']} task timing is inconsistent")
        if return_end > analysis_window_s:
            raise Gate3AssignmentError(
                f"trajectory {item['id']} task exceeds the analysis window"
            )
        probe = item["diagnostic_probe"]
        if excitation == "ordinary" and probe is not None:
            raise Gate3AssignmentError("ordinary trajectories must not carry a probe")
        if excitation == "diagnostic":
            if not isinstance(probe, Mapping):
                raise Gate3AssignmentError("diagnostic trajectories require a probe")
            expected_probe = dict(configured_probe)
            expected_probe["start_offset_s"] = probe.get("start_offset_s")
            if dict(probe) != expected_probe:
                raise Gate3AssignmentError(
                    "diagnostic probe must match the draft-config proposal exactly"
                )
            start = _finite_number(
                probe["start_offset_s"], "diagnostic start_offset_s", minimum=0.0
            )
            if start + float(probe["cycles"]) / float(probe["frequency_hz"]) > analysis_window_s:
                raise Gate3AssignmentError("diagnostic probe exceeds the analysis window")
    for split, excitations in excitation_by_split.items():
        if excitations != {"ordinary", "diagnostic"}:
            raise Gate3AssignmentError(
                f"split {split} must contain ordinary and diagnostic trajectories"
            )


def _validate_known_grid(document: Mapping[str, Any]) -> None:
    """Validate multi-location, multi-severity known-class grids and no leakage."""

    grids = document["fault_grid_by_split"]
    if not isinstance(grids, Mapping) or set(grids) != set(SPLITS):
        raise Gate3AssignmentError("fault_grid_by_split must define exactly all four splits")
    known_tuples_by_split: dict[str, set[tuple[Any, ...]]] = {}
    for split in SPLITS:
        grid = grids[split]
        _require_exact_keys(grid, {"structure", "actuator", "sensor"}, f"{split} grid")
        split_tuples: set[tuple[Any, ...]] = set()
        for source_class in ("structure", "actuator"):
            family = grid[source_class]
            _require_exact_keys(
                family,
                {"subtype", "locations", "severities", "severity_semantics"},
                f"{split} {source_class} grid",
            )
            expected_subtype = (
                "link_stiffness_loss"
                if source_class == "structure"
                else "actuator_gain_loss"
            )
            if family["subtype"] != expected_subtype:
                raise Gate3AssignmentError(
                    f"{split} {source_class} subtype must be {expected_subtype}"
                )
            if (
                not isinstance(family["severity_semantics"], str)
                or not family["severity_semantics"]
            ):
                raise Gate3AssignmentError(
                    f"{split} {source_class} severity semantics must be explicit"
                )
            if len(family["severities"]) < 2 or len(set(family["severities"])) < 2:
                raise Gate3AssignmentError(
                    f"{split} {source_class} requires multiple severities"
                )
            expected_locations = [1] if source_class == "structure" else [0, 1]
            if sorted(family["locations"]) != expected_locations:
                raise Gate3AssignmentError(
                    f"{split} {source_class} locations must be {expected_locations}"
                )
            for location in family["locations"]:
                for severity in family["severities"]:
                    numeric = _finite_number(
                        severity, f"{split} {source_class} severity", minimum=0.0
                    )
                    if not 0.0 < numeric < 1.0:
                        raise Gate3AssignmentError(
                            f"{split} {source_class} severities must be in (0, 1)"
                        )
                    split_tuples.add(
                        (source_class, family["subtype"], location, numeric)
                    )
        sensor = grid["sensor"]
        if not isinstance(sensor, list) or len(sensor) != len(SENSOR_SUBTYPES):
            raise Gate3AssignmentError(
                f"{split} sensor grid must define exactly the three sensor subtypes"
            )
        if {family.get("subtype") for family in sensor} != set(SENSOR_SUBTYPES):
            raise Gate3AssignmentError(f"{split} sensor grid subtype coverage is incomplete")
        for family in sensor:
            _require_exact_keys(
                family,
                {"subtype", "locations", "severities", "severity_semantics"},
                f"{split} sensor family",
            )
            if (
                not isinstance(family["severity_semantics"], str)
                or not family["severity_semantics"]
            ):
                raise Gate3AssignmentError(
                    f"{split} sensor severity semantics must be explicit"
                )
            if sorted(family["locations"]) != [0, 1]:
                raise Gate3AssignmentError(f"{split} sensor locations must be [0, 1]")
            if len(family["severities"]) < 2 or len(set(family["severities"])) < 2:
                raise Gate3AssignmentError(
                    f"{split} sensor families require multiple severities"
                )
            for location in family["locations"]:
                for severity in family["severities"]:
                    numeric = _finite_number(
                        severity, f"{split} sensor severity", minimum=0.0
                    )
                    if not 0.0 < numeric < 1.0:
                        raise Gate3AssignmentError(
                            f"{split} sensor severities must be in (0, 1)"
                        )
                    split_tuples.add(("sensor", family["subtype"], location, numeric))
        known_tuples_by_split[split] = split_tuples
    for left_index, left in enumerate(SPLITS):
        for right in SPLITS[left_index + 1 :]:
            overlap = known_tuples_by_split[left] & known_tuples_by_split[right]
            if overlap:
                raise Gate3AssignmentError(
                    f"known fault tuples leak across {left}/{right}: {sorted(overlap)}"
                )


def _validate_compound_ood(document: Mapping[str, Any]) -> None:
    """Validate explicit held-out compound settings and their label convention."""

    settings = document["compound_ood_settings"]
    if not isinstance(settings, list):
        raise Gate3AssignmentError("compound_ood_settings must be a list")
    _require_unique_ids(settings, "compound_ood_settings")
    counts = {"val": 0, "test": 0}
    setting_keys = {"id", "split", "label", "components"}
    label_keys = {
        "source_class",
        "subtype",
        "location",
        "severity",
        "compound_flag",
        "ood_flag",
    }
    component_keys = {"source_class", "subtype", "location", "severity"}
    for setting in settings:
        _require_exact_keys(setting, setting_keys, f"compound {setting.get('id')}")
        split = setting["split"]
        if split not in counts:
            raise Gate3AssignmentError("compound/OOD settings are reserved to val/test")
        counts[split] += 1
        label = setting["label"]
        _require_exact_keys(label, label_keys, f"compound label {setting['id']}")
        if (
            label["source_class"] not in FAULT_SOURCE_CLASSES
            or not str(label["subtype"]).startswith("compound_")
            or label["compound_flag"] is not True
            or label["ood_flag"] is not True
        ):
            raise Gate3AssignmentError(f"compound label convention invalid: {setting['id']}")
        components = setting["components"]
        if not isinstance(components, list) or len(components) < 2:
            raise Gate3AssignmentError(
                f"compound setting {setting['id']} requires at least two components"
            )
        component_sources: set[str] = set()
        for component in components:
            _require_exact_keys(
                component, component_keys, f"compound component {setting['id']}"
            )
            source = component["source_class"]
            if source not in FAULT_SOURCE_CLASSES:
                raise Gate3AssignmentError(f"invalid compound component source: {source}")
            component_sources.add(source)
            severity = _finite_number(
                component["severity"], "compound severity", minimum=0.0
            )
            if not 0.0 < severity < 1.0:
                raise Gate3AssignmentError("compound severities must be in (0, 1)")
            location = component["location"]
            expected_locations = {1} if source == "structure" else {0, 1}
            if location not in expected_locations:
                raise Gate3AssignmentError(
                    f"compound {source} location must be in {sorted(expected_locations)}"
                )
            if source == "structure" and component["subtype"] != "link_stiffness_loss":
                raise Gate3AssignmentError("invalid compound structural subtype")
            if source == "actuator" and component["subtype"] != "actuator_gain_loss":
                raise Gate3AssignmentError("invalid compound actuator subtype")
            if source == "sensor" and component["subtype"] not in SENSOR_SUBTYPES:
                raise Gate3AssignmentError("invalid compound sensor subtype")
        if len(component_sources) < 2:
            raise Gate3AssignmentError(
                f"compound setting {setting['id']} must cross source families"
            )
        primary = components[0]
        for key in ("source_class", "location", "severity"):
            if label[key] != primary[key]:
                raise Gate3AssignmentError(
                    f"compound label {setting['id']} must identify its first component"
                )
    if counts != {"val": 2, "test": 2}:
        raise Gate3AssignmentError("exactly two compound/OOD settings are required per val/test")


def _validate_context_profiles(
    document: Mapping[str, Any],
    config: ValidatedConfig,
) -> None:
    """Validate split-specific payload, environment, and contact confounds."""

    contexts = document["context_profiles"]
    _require_exact_keys(
        contexts,
        {"payloads", "environments", "contacts"},
        "context_profiles",
    )
    expected_keys = {
        "payloads": {"id", "split", "distal_payload_mass_kg"},
        "environments": {"id", "split", "temperature_kind", "parameters"},
        "contacts": {
            "id",
            "split",
            "endpoint_plane_z_m",
            "contact_window_offset_s",
        },
    }
    selected_plane = float(
        config.document["values"]["plant"]["endpoint_contact_plane_z_m"]
    )
    analysis_window_s = float(config.document["values"]["timing"]["analysis_window_s"])
    for catalog_name, keys in expected_keys.items():
        items = contexts[catalog_name]
        if not isinstance(items, list) or not items:
            raise Gate3AssignmentError(f"{catalog_name} must be a nonempty list")
        _require_unique_ids(items, catalog_name)
        counts = {split: 0 for split in SPLITS}
        for item in items:
            _require_exact_keys(item, keys, f"{catalog_name} {item.get('id')}")
            split = item["split"]
            if split not in SPLITS:
                raise Gate3AssignmentError(f"{catalog_name} item has invalid split")
            counts[split] += 1
            if catalog_name == "payloads":
                _finite_number(
                    item["distal_payload_mass_kg"],
                    "distal_payload_mass_kg",
                    minimum=0.0,
                )
            elif catalog_name == "environments":
                if item["temperature_kind"] not in {
                    "isothermal",
                    "linear",
                    "sinusoid",
                }:
                    raise Gate3AssignmentError("unsupported temperature_kind")
                if not isinstance(item["parameters"], Mapping) or not item["parameters"]:
                    raise Gate3AssignmentError("environment parameters cannot be empty")
                for value in item["parameters"].values():
                    _finite_number(value, "environment parameter")
            else:
                plane = item["endpoint_plane_z_m"]
                window = item["contact_window_offset_s"]
                if (plane is None) != (window is None):
                    raise Gate3AssignmentError(
                        "contact plane and window must both be null or both be present"
                    )
                if plane is not None:
                    if float(plane) != selected_plane:
                        raise Gate3AssignmentError(
                            "contact profiles must use the draft-config selected plane"
                        )
                    if not isinstance(window, list) or len(window) != 2:
                        raise Gate3AssignmentError("contact window must be increasing")
                    start = _finite_number(window[0], "contact start", minimum=0.0)
                    end = _finite_number(window[1], "contact end", minimum=0.0)
                    if start >= end or end > analysis_window_s:
                        raise Gate3AssignmentError(
                            "contact window must be increasing within the analysis window"
                        )
        if any(count != 2 for count in counts.values()):
            raise Gate3AssignmentError(
                f"{catalog_name} requires exactly two profiles in every split"
            )


def _context_cell_table(plan: Mapping[str, Any]) -> tuple[tuple[int, int, int], ...]:
    """Return the exact fault-independent balanced context-cell table."""

    raw_cells = plan["context_cell_table"]
    if not isinstance(raw_cells, list):
        raise Gate3AssignmentError("context_cell_table must be a list")
    cells: list[tuple[int, int, int]] = []
    for index, raw_cell in enumerate(raw_cells):
        if (
            not isinstance(raw_cell, list)
            or len(raw_cell) != 3
            or any(
                not isinstance(value, int)
                or isinstance(value, bool)
                or value not in (0, 1)
                for value in raw_cell
            )
        ):
            raise Gate3AssignmentError(
                f"context_cell_table[{index}] must contain three binary indexes"
            )
        cells.append((raw_cell[0], raw_cell[1], raw_cell[2]))
    if tuple(cells) != BALANCED_CONTEXT_CELL_TABLE:
        raise Gate3AssignmentError(
            "context_cell_table must use the exact balanced eight-cell order"
        )
    return tuple(cells)


def expand_reservations(document: Mapping[str, Any]) -> list[ScenarioReservation]:
    """Expand the approved deterministic rotation into suite-independent reservations."""

    trajectories = document["trajectory_specs"]
    faults = expanded_fault_settings(document)
    contexts = document["context_profiles"]
    plan = document["generation_plan"]
    context_cells = _context_cell_table(plan)
    reservations: list[ScenarioReservation] = []
    for split in SPLITS:
        split_trajectories = [item for item in trajectories if item["split"] == split]
        split_faults = [item for item in faults if item["split"] == split]
        payloads = [item for item in contexts["payloads"] if item["split"] == split]
        environments = [
            item for item in contexts["environments"] if item["split"] == split
        ]
        contacts = [item for item in contexts["contacts"] if item["split"] == split]
        repetitions = int(plan["realizations_per_trajectory_fault"][split])
        seed_base = int(plan["seed_base_by_split"][split])
        ordinal = 0
        for trajectory_index, trajectory in enumerate(split_trajectories):
            for fault_index, fault in enumerate(split_faults):
                for replicate in range(repetitions):
                    context_cell = context_cells[
                        (trajectory_index * repetitions + replicate)
                        % len(context_cells)
                    ]
                    stem = (
                        f"{split}_t{trajectory_index:02d}_f{fault_index:03d}"
                        f"_r{replicate:02d}"
                    )
                    seed = seed_base + 10 * ordinal
                    reservations.append(
                        ScenarioReservation(
                            schema_version=str(document["schema_version"]),
                            draft_config_hash=str(document["draft_config_hash"]),
                            scenario_spec_id=f"scenario_{stem}",
                            base_pair_id=f"basepair_{stem}",
                            trajectory_spec_id=str(trajectory["id"]),
                            fault_setting_id=str(fault["id"]),
                            split_group_id=f"group_{stem}",
                            split=split,
                            payload_id=str(payloads[context_cell[0]]["id"]),
                            env_profile_id=str(environments[context_cell[1]]["id"]),
                            contact_profile_id=str(contacts[context_cell[2]]["id"]),
                            sim_seed=seed,
                            fault_seed=seed + 1,
                            sensor_seed=seed + 2,
                            controller_seed=seed + 3,
                        )
                    )
                    ordinal += 1
    return reservations


def _assert_fault_independent_context_cells(
    document: Mapping[str, Any],
    reservations: list[ScenarioReservation],
) -> dict[str, int]:
    """Require identical balanced context-cell distributions for every fault."""

    plan = document["generation_plan"]
    context_cells = _context_cell_table(plan)
    context_cell_counts: dict[str, int] = {}
    for split in SPLITS:
        cells_by_fault: dict[str, Counter[tuple[str, str, str]]] = {}
        for reservation in reservations:
            if reservation.split != split:
                continue
            cells_by_fault.setdefault(
                reservation.fault_setting_id,
                Counter(),
            ).update(
                [
                    (
                        reservation.payload_id,
                        reservation.env_profile_id,
                        reservation.contact_profile_id,
                    )
                ]
            )
        cell_distributions = list(cells_by_fault.values())
        if not cell_distributions or any(
            cells != cell_distributions[0] for cells in cell_distributions[1:]
        ):
            raise Gate3AssignmentError(
                f"{split} faults must realize an identical context-cell distribution"
            )
        trajectory_count = sum(
            item["split"] == split for item in document["trajectory_specs"]
        )
        expected_cell_count = min(
            len(context_cells),
            trajectory_count
            * int(plan["realizations_per_trajectory_fault"][split]),
        )
        if len(cell_distributions[0]) != expected_cell_count:
            raise Gate3AssignmentError(
                f"{split} faults must realize exactly {expected_cell_count} "
                "balanced context cells"
            )
        context_cell_counts[split] = expected_cell_count
    return context_cell_counts


def _assert_context_axes_vary_within_trajectories(
    reservations: list[ScenarioReservation],
) -> None:
    """Reject trajectory/fault groups that alias any context axis."""

    rows_by_group: dict[
        tuple[str, str, str],
        list[ScenarioReservation],
    ] = {}
    for reservation in reservations:
        key = (
            reservation.split,
            reservation.trajectory_spec_id,
            reservation.fault_setting_id,
        )
        rows_by_group.setdefault(key, []).append(reservation)

    for (split, trajectory_id, fault_id), rows in rows_by_group.items():
        axes = {
            "payload": {row.payload_id for row in rows},
            "environment": {row.env_profile_id for row in rows},
            "contact": {row.contact_profile_id for row in rows},
        }
        aliased = [axis for axis, values in axes.items() if len(values) != 2]
        if aliased:
            raise Gate3AssignmentError(
                f"{split} trajectory {trajectory_id!r} and fault {fault_id!r} "
                f"must vary both profiles on every context axis; aliased: {aliased}"
            )


def _validate_protocol_and_plan(document: Mapping[str, Any]) -> None:
    """Validate pairing, split roles, seed policy, and generation interlocks."""

    protocol = document["suite_protocol"]
    _require_exact_keys(
        protocol,
        {
            "suites",
            "primary_comparison",
            "suite_independent_split_assignment",
            "common_random_number_fields",
            "same_algorithm_capacity_rule",
            "oracle_boundary",
        },
        "suite_protocol",
    )
    if protocol["suites"] != list(SUITES):
        raise Gate3AssignmentError("suite order must be exactly C0, C1, S, O")
    if protocol["primary_comparison"] != ["C1", "S"]:
        raise Gate3AssignmentError("primary comparison must be the matched C1/S pair")
    if protocol["suite_independent_split_assignment"] is not True:
        raise Gate3AssignmentError("suite cannot be an input to split assignment")
    required_crn = {
        "scenario_spec_id",
        "trajectory_spec_id",
        "fault_setting_id",
        "payload_id",
        "env_profile_id",
        "contact_profile_id",
        "sim_seed",
        "fault_seed",
        "sensor_seed",
        "controller_seed",
        "train_seed",
    }
    if set(protocol["common_random_number_fields"]) != required_crn:
        raise Gate3AssignmentError("common-random-number field set is incomplete")

    split_policy = document["split_policy"]
    _require_exact_keys(
        split_policy,
        {
            "split_order",
            "assignment_unit",
            "partition_fields",
            "suite_not_split_input",
            "dataset_identity_train_seed",
            "model_training_seed_pool",
            "role_by_split",
            "test_reservations_only_until_frozen",
            "ood_known_metric_rule",
        },
        "split_policy",
    )
    if split_policy["split_order"] != list(SPLITS):
        raise Gate3AssignmentError("split_order must be dev, pilot, val, test")
    if split_policy["suite_not_split_input"] is not True:
        raise Gate3AssignmentError("suite_not_split_input must be true")
    if split_policy["dataset_identity_train_seed"] != 0:
        raise Gate3AssignmentError("pre-fit dataset identities must use train_seed 0")
    seeds = split_policy["model_training_seed_pool"]
    if (
        not isinstance(seeds, list)
        or len(seeds) < 5
        or len(seeds) != len(set(seeds))
        or any(not isinstance(seed, int) or isinstance(seed, bool) or seed <= 0 for seed in seeds)
    ):
        raise Gate3AssignmentError("at least five unique positive model training seeds are required")
    if split_policy["test_reservations_only_until_frozen"] is not True:
        raise Gate3AssignmentError("test identities must remain reservation-only before freeze")
    if set(split_policy["partition_fields"]) != {
        "trajectory_spec_id",
        "fault_setting_id",
        "split_group_id",
    }:
        raise Gate3AssignmentError("whole-group partition fields are incomplete")
    if set(split_policy["role_by_split"]) != set(SPLITS):
        raise Gate3AssignmentError("role_by_split must define every split")

    plan = document["generation_plan"]
    _require_exact_keys(
        plan,
        {
            "expansion_rule",
            "context_cell_table",
            "realizations_per_trajectory_fault",
            "seed_base_by_split",
            "expected_reservations_by_split",
            "future_manifest_rows_per_reservation",
        },
        "generation_plan",
    )
    _context_cell_table(plan)
    for mapping_name in (
        "realizations_per_trajectory_fault",
        "seed_base_by_split",
        "expected_reservations_by_split",
    ):
        if set(plan[mapping_name]) != set(SPLITS):
            raise Gate3AssignmentError(f"{mapping_name} must define every split")
    if any(
        not isinstance(value, int) or isinstance(value, bool) or value <= 0
        for value in plan["realizations_per_trajectory_fault"].values()
    ):
        raise Gate3AssignmentError("realization counts must be positive integers")
    expected_rows_per_reservation = len(SUITES) * len(seeds)
    if plan["future_manifest_rows_per_reservation"] != expected_rows_per_reservation:
        raise Gate3AssignmentError(
            "future manifest multiplier must cover every suite and training seed"
        )


def validate_assignment(
    document: Mapping[str, Any],
    config: ValidatedConfig,
) -> dict[str, Any]:
    """Validate a proposed assignment and return a deterministic audit summary."""

    _require_exact_keys(document, TOP_LEVEL_KEYS, "assignment")
    if document["assignment_version"] != "0.1.0-proposed":
        raise Gate3AssignmentError("assignment_version must be 0.1.0-proposed")
    if document["schema_version"] != "1.0":
        raise Gate3AssignmentError("assignment schema_version must be 1.0")
    if document["status"] != "proposed" or document["decision"] != PROPOSED_DECISION:
        raise Gate3AssignmentError("assignment must retain its proposed pending-review state")
    if document["required_same_state_approval"] != APPROVAL_TOKEN:
        raise Gate3AssignmentError("required approval token is incorrect")
    if document["research_payload_generation_allowed"] is not False:
        raise Gate3AssignmentError("proposed assignment cannot authorize research payloads")
    if document["test_payload_generation_allowed"] is not False:
        raise Gate3AssignmentError("proposed assignment cannot authorize test payloads")
    if config.status != "draft" or config.is_frozen:
        raise Gate3AssignmentError("proposal validation requires the tracked draft config")
    if document["draft_config_hash"] != config.config_hash:
        raise Gate3AssignmentError("assignment draft_config_hash does not match config")
    expected_hash = expected_assignment_hash(document)
    if document["assignment_hash"] != expected_hash:
        raise Gate3AssignmentError(
            f"assignment_hash mismatch: supplied {document['assignment_hash']!r}, "
            f"expected {expected_hash!r}"
        )
    if not isinstance(document["evidence_boundary"], list) or not document["evidence_boundary"]:
        raise Gate3AssignmentError("evidence_boundary must be a nonempty list")
    if any(not isinstance(item, str) or not item for item in document["evidence_boundary"]):
        raise Gate3AssignmentError("evidence_boundary entries must be nonempty strings")
    if (
        not isinstance(document["implementation_requirements"], list)
        or not document["implementation_requirements"]
        or any(
            not isinstance(item, str) or not item
            for item in document["implementation_requirements"]
        )
    ):
        raise Gate3AssignmentError("implementation_requirements must be nonempty strings")

    _validate_protocol_and_plan(document)
    _validate_trajectory_specs(document, config)
    _validate_known_grid(document)
    _validate_compound_ood(document)
    _validate_context_profiles(document, config)

    faults = expanded_fault_settings(document)
    _require_unique_ids(faults, "expanded fault settings")
    reservations = expand_reservations(document)
    context_cell_counts = _assert_fault_independent_context_cells(
        document,
        reservations,
    )
    _assert_context_axes_vary_within_trajectories(reservations)
    ids = {
        "scenario_spec_id": [row.scenario_spec_id for row in reservations],
        "base_pair_id": [row.base_pair_id for row in reservations],
        "split_group_id": [row.split_group_id for row in reservations],
    }
    for field, values in ids.items():
        if len(values) != len(set(values)):
            raise Gate3AssignmentError(f"expanded {field} values must be unique")
    seed_tuples = [
        (row.sim_seed, row.fault_seed, row.sensor_seed, row.controller_seed)
        for row in reservations
    ]
    if len(seed_tuples) != len(set(seed_tuples)):
        raise Gate3AssignmentError("expanded reservation seed tuples must be unique")

    counts = {split: 0 for split in SPLITS}
    used_contexts = {
        "payloads": set(),
        "environments": set(),
        "contacts": set(),
    }
    for reservation in reservations:
        counts[reservation.split] += 1
        used_contexts["payloads"].add(reservation.payload_id)
        used_contexts["environments"].add(reservation.env_profile_id)
        used_contexts["contacts"].add(reservation.contact_profile_id)
    if counts != document["generation_plan"]["expected_reservations_by_split"]:
        raise Gate3AssignmentError(
            f"expanded reservation counts {counts} do not match the preregistration"
        )
    for catalog_name, used in used_contexts.items():
        expected = {item["id"] for item in document["context_profiles"][catalog_name]}
        if used != expected:
            raise Gate3AssignmentError(
                f"deterministic rotation does not cover every {catalog_name} profile"
            )

    fault_counts = {
        split: sum(setting["split"] == split for setting in faults) for split in SPLITS
    }
    future_multiplier = int(
        document["generation_plan"]["future_manifest_rows_per_reservation"]
    )
    return {
        "status": "valid_proposed_assignment",
        "decision": document["decision"],
        "assignment_hash": document["assignment_hash"],
        "draft_config_hash": document["draft_config_hash"],
        "same_state_approval_required": document["required_same_state_approval"],
        "research_payload_generation_allowed": False,
        "test_payload_generation_allowed": False,
        "trajectory_counts": {
            split: sum(item["split"] == split for item in document["trajectory_specs"])
            for split in SPLITS
        },
        "fault_setting_counts": fault_counts,
        "context_cell_counts_by_split": context_cell_counts,
        "reservation_counts": counts,
        "total_reservations": len(reservations),
        "model_training_seeds": len(document["split_policy"]["model_training_seed_pool"]),
        "future_manifest_rows_after_freeze": len(reservations) * future_multiplier,
        "test_reservations_materialized": 0,
    }


def reservation_dicts(document: Mapping[str, Any]) -> list[dict[str, Any]]:
    """Return deterministic serializable reservation dictionaries for review/tests."""

    return [asdict(row) for row in expand_reservations(document)]
