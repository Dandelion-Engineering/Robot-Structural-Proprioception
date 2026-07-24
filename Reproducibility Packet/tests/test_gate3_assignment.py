"""Adversarial tests for the proposed Gate-3 assignment contract."""

from __future__ import annotations

import copy
import sys
from collections import Counter, defaultdict
from dataclasses import replace
from pathlib import Path

import pytest

PACKET_ROOT = Path(__file__).resolve().parents[1]
SCRIPTS_ROOT = PACKET_ROOT / "scripts"
sys.path.insert(0, str(SCRIPTS_ROOT))

from utils.config_contract import load_config  # noqa: E402
import utils.gate3_assignment as gate3_assignment  # noqa: E402
from utils.gate3_assignment import (  # noqa: E402
    Gate3AssignmentError,
    expected_assignment_hash,
    expanded_fault_settings,
    load_assignment,
    reservation_dicts,
    validate_assignment,
)

SCHEMA_PATH = PACKET_ROOT / "schema" / "schema.json"
CONFIG_PATH = PACKET_ROOT / "config" / "draft-config-v0.1.json"
ASSIGNMENT_PATH = PACKET_ROOT / "config" / "proposed-gate3-assignment-v0.1.json"


def config():
    """Return the lifecycle-validated tracked draft."""

    return load_config(CONFIG_PATH, SCHEMA_PATH)


def assignment() -> dict[str, object]:
    """Return a fresh copy of the tracked proposal."""

    return load_assignment(ASSIGNMENT_PATH)


def rehash(document: dict[str, object]) -> dict[str, object]:
    """Rehash one semantic mutation so its intended guard is reached."""

    document["assignment_hash"] = expected_assignment_hash(document)
    return document


def test_tracked_assignment_validates_without_authorizing_payloads() -> None:
    summary = validate_assignment(assignment(), config())
    assert summary == {
        "assignment_hash": (
            "dev-70832daabe7968d55c0bf68e713e945ed48ce167f5c54ec186559b9a660765de"
        ),
        "decision": "PENDING_JOINT_APPROVAL_GATE3_ASSIGNMENT_V0_1",
        "draft_config_hash": config().config_hash,
        "context_cell_counts_by_split": {
            "dev": 4,
            "pilot": 4,
            "test": 8,
            "val": 8,
        },
        "fault_setting_counts": {"dev": 19, "pilot": 19, "test": 21, "val": 21},
        "future_manifest_rows_after_freeze": 13120,
        "model_training_seeds": 5,
        "research_payload_generation_allowed": False,
        "reservation_counts": {"dev": 76, "pilot": 76, "test": 336, "val": 168},
        "same_state_approval_required": "APPROVE_GATE3_ASSIGNMENT_V0_1",
        "status": "valid_proposed_assignment",
        "test_payload_generation_allowed": False,
        "test_reservations_materialized": 0,
        "total_reservations": 656,
        "trajectory_counts": {"dev": 2, "pilot": 2, "test": 2, "val": 2},
    }


def test_reservation_expansion_is_deterministic_and_whole_group_split() -> None:
    document = assignment()
    first = reservation_dicts(document)
    second = reservation_dicts(document)
    assert first == second
    assert len(first) == 656
    assert not any("suite" in row or "train_seed" in row for row in first)
    for key in (
        "trajectory_spec_id",
        "fault_setting_id",
        "split_group_id",
        "base_pair_id",
    ):
        split_by_value: dict[str, str] = {}
        for row in first:
            previous = split_by_value.setdefault(row[key], row["split"])
            assert previous == row["split"]
    for row in first:
        assert row["fault_seed"] == row["sim_seed"] + 1
        assert row["sensor_seed"] == row["sim_seed"] + 2
        assert row["controller_seed"] == row["sim_seed"] + 3


def test_context_cells_are_fault_independent_and_balanced() -> None:
    rows = reservation_dicts(assignment())
    expected_contexts = {
        "dev": (4, 1),
        "pilot": (4, 1),
        "val": (8, 1),
        "test": (8, 2),
    }
    for split, (expected_count, expected_frequency) in expected_contexts.items():
        cells_by_fault: dict[
            str,
            Counter[tuple[str, str, str]],
        ] = defaultdict(Counter)
        for row in rows:
            if row["split"] != split:
                continue
            cells_by_fault[row["fault_setting_id"]].update(
                [
                    (
                        row["payload_id"],
                        row["env_profile_id"],
                        row["contact_profile_id"],
                    )
                ]
            )
        distributions = list(cells_by_fault.values())
        assert distributions
        assert all(distribution == distributions[0] for distribution in distributions)
        assert len(distributions[0]) == expected_count
        assert set(distributions[0].values()) == {expected_frequency}


def test_validator_rejects_fault_conditioned_context_cells(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    original_expand = gate3_assignment.expand_reservations

    def leaky_expand(document):
        reservations = original_expand(document)
        target_index = next(
            index
            for index, row in enumerate(reservations)
            if row.split == "dev" and "healthy" in row.fault_setting_id
        )
        target = reservations[target_index]
        replacement_env = next(
            item["id"]
            for item in document["context_profiles"]["environments"]
            if item["split"] == "dev" and item["id"] != target.env_profile_id
        )
        reservations[target_index] = replace(
            target,
            env_profile_id=replacement_env,
        )
        return reservations

    monkeypatch.setattr(gate3_assignment, "expand_reservations", leaky_expand)
    with pytest.raises(
        Gate3AssignmentError,
        match="identical context-cell distribution",
    ):
        gate3_assignment.validate_assignment(assignment(), config())


def test_expanded_grid_covers_known_classes_and_held_out_compounds() -> None:
    settings = expanded_fault_settings(assignment())
    structural_locations = {
        setting["label"]["location"]
        for setting in settings
        if setting["label"]["source_class"] == "structure"
        and not setting["label"]["ood_flag"]
    }
    assert structural_locations == {1}
    for split in ("dev", "pilot", "val", "test"):
        known = {
            setting["label"]["source_class"]
            for setting in settings
            if setting["split"] == split and not setting["label"]["ood_flag"]
        }
        assert known == {"healthy", "structure", "actuator", "sensor"}
    for split in ("val", "test"):
        ood = [
            setting
            for setting in settings
            if setting["split"] == split and setting["label"]["ood_flag"]
        ]
        assert len(ood) == 2
        assert all(setting["label"]["compound_flag"] for setting in ood)
        assert all(len(setting["components"]) >= 2 for setting in ood)


def test_assignment_hash_detects_same_state_tamper() -> None:
    document = assignment()
    document["decision"] = "APPROVED_WITHOUT_REVIEW"
    with pytest.raises(Gate3AssignmentError, match="pending-review state"):
        validate_assignment(rehash(document), config())
    document = assignment()
    document["trajectory_specs"][0]["target_joint_rad"][0] = 0.23
    with pytest.raises(Gate3AssignmentError, match="assignment_hash mismatch"):
        validate_assignment(document, config())


@pytest.mark.parametrize(
    "field",
    ["research_payload_generation_allowed", "test_payload_generation_allowed"],
)
def test_proposal_cannot_authorize_generation(field: str) -> None:
    document = assignment()
    document[field] = True
    with pytest.raises(Gate3AssignmentError, match="cannot authorize"):
        validate_assignment(rehash(document), config())


def test_assignment_must_bind_the_exact_draft_config() -> None:
    document = assignment()
    document["draft_config_hash"] = "dev-" + "0" * 64
    with pytest.raises(Gate3AssignmentError, match="does not match config"):
        validate_assignment(rehash(document), config())


def test_known_fault_tuple_cannot_leak_across_splits() -> None:
    document = assignment()
    document["fault_grid_by_split"]["pilot"]["structure"]["severities"][0] = 0.5
    with pytest.raises(Gate3AssignmentError, match="leak across dev/pilot"):
        validate_assignment(rehash(document), config())


def test_every_split_requires_both_excitation_conditions() -> None:
    document = assignment()
    trajectory = next(
        item
        for item in document["trajectory_specs"]
        if item["split"] == "pilot" and item["excitation"] == "diagnostic"
    )
    trajectory["excitation"] = "ordinary"
    trajectory["diagnostic_probe"] = None
    with pytest.raises(Gate3AssignmentError, match="ordinary and diagnostic"):
        validate_assignment(rehash(document), config())


def test_compound_ood_cannot_enter_known_class_metrics() -> None:
    document = assignment()
    document["compound_ood_settings"][0]["label"]["ood_flag"] = False
    with pytest.raises(Gate3AssignmentError, match="compound label convention"):
        validate_assignment(rehash(document), config())


def test_at_least_five_training_seeds_are_required() -> None:
    document = assignment()
    document["split_policy"]["model_training_seed_pool"] = [1, 2, 3, 4]
    document["generation_plan"]["future_manifest_rows_per_reservation"] = 16
    with pytest.raises(Gate3AssignmentError, match="at least five"):
        validate_assignment(rehash(document), config())


def test_each_split_requires_exactly_two_context_profiles() -> None:
    document = assignment()
    document["context_profiles"]["payloads"] = [
        item
        for item in document["context_profiles"]["payloads"]
        if item["id"] != "payload_test_0p200kg"
    ]
    with pytest.raises(Gate3AssignmentError, match="exactly two profiles"):
        validate_assignment(rehash(document), config())


def test_context_cell_table_is_exact_and_self_hashed() -> None:
    document = assignment()
    document["generation_plan"]["context_cell_table"][0] = [0, 1, 0]
    with pytest.raises(Gate3AssignmentError, match="balanced eight-cell order"):
        validate_assignment(rehash(document), config())


def test_declared_reservation_counts_are_audited() -> None:
    document = assignment()
    document["generation_plan"]["expected_reservations_by_split"]["test"] -= 1
    with pytest.raises(Gate3AssignmentError, match="do not match"):
        validate_assignment(rehash(document), config())


def test_strict_loader_rejects_duplicate_json_keys(tmp_path: Path) -> None:
    path = tmp_path / "duplicate.json"
    path.write_text('{"status":"proposed","status":"frozen"}', encoding="utf-8")
    with pytest.raises(Gate3AssignmentError, match="duplicate JSON key"):
        load_assignment(path)


def test_rehashed_deep_copy_does_not_mutate_tracked_assignment() -> None:
    original = assignment()
    mutated = copy.deepcopy(original)
    mutated["evidence_boundary"].append("test-only mutation")
    rehash(mutated)
    assert mutated["assignment_hash"] != original["assignment_hash"]
    assert assignment()["assignment_hash"] == original["assignment_hash"]
