"""Adversarial tests for the one-way approved-assignment/config binding."""

from __future__ import annotations

import copy
import json
import sys
from pathlib import Path

import pytest

PACKET_ROOT = Path(__file__).resolve().parents[1]
SCRIPTS_ROOT = PACKET_ROOT / "scripts"
sys.path.insert(0, str(SCRIPTS_ROOT))

from utils.assignment_binding import (  # noqa: E402
    APPROVAL_TOKEN,
    AssignmentBindingError,
    GATE3_OPEN_GATE,
    embed_approved_assignment_document,
    validate_approved_assignment_binding,
)
from utils.config_contract import (  # noqa: E402
    expected_config_hash,
    load_config,
    validate_config_document,
)
from utils.gate3_assignment import load_assignment  # noqa: E402

SCHEMA_PATH = PACKET_ROOT / "schema" / "schema.json"
CONFIG_PATH = PACKET_ROOT / "config" / "draft-config-v0.1.json"
ASSIGNMENT_PATH = PACKET_ROOT / "config" / "proposed-gate3-assignment-v0.1.json"


def parent_config():
    """Load the tracked parent draft before the repository embedding step."""

    config = load_config(CONFIG_PATH, SCHEMA_PATH)
    if config.document["values"]["scenario_manifest"] is not None:
        return validate_approved_assignment_binding(config).parent_config
    return config


def assignment() -> dict[str, object]:
    """Return a fresh exact assignment document."""

    return load_assignment(ASSIGNMENT_PATH)


def bound_config(tmp_path: Path):
    """Create and validate one embedded draft in a temporary path."""

    document = embed_approved_assignment_document(parent_config(), assignment())
    path = tmp_path / "draft-bound.json"
    path.write_text(
        json.dumps(document, indent=2, allow_nan=False) + "\n",
        encoding="utf-8",
    )
    return load_config(path, SCHEMA_PATH)


def rehash_config(document: dict[str, object]) -> dict[str, object]:
    """Rehash a semantic mutation so the intended binding guard is reached."""

    document["config_hash"] = expected_config_hash(document)
    return document


def test_embedding_preserves_exact_assignment_and_removes_only_gate3(
    tmp_path: Path,
) -> None:
    parent = parent_config()
    current = bound_config(tmp_path)
    binding = validate_approved_assignment_binding(
        current,
        expected_assignment=assignment(),
    )
    assert dict(binding.assignment) == assignment()
    assert binding.parent_config.config_hash == parent.config_hash
    assert binding.assignment_hash == (
        "dev-eec59ec8a296a9a4ff4909f8e7f1de91a0a8f4bf289ae1533a427d1a87bc33f1"
    )
    assert binding.proposal_audit["total_reservations"] == 808
    assert binding.authorized_research_splits == ("dev", "pilot", "val")
    assert GATE3_OPEN_GATE in parent.document["open_gates"]
    assert GATE3_OPEN_GATE not in current.document["open_gates"]
    assert current.config_hash != parent.config_hash


def test_wrong_approval_token_is_refused() -> None:
    with pytest.raises(AssignmentBindingError, match="approval decision"):
        embed_approved_assignment_document(
            parent_config(),
            assignment(),
            approval_decision="APPROVE_SOMETHING_ELSE",
        )


def test_parent_must_still_have_null_manifest_and_gate3() -> None:
    parent = parent_config()
    changed = copy.deepcopy(dict(parent.document))
    changed["values"]["scenario_manifest"] = {}
    changed["config_hash"] = expected_config_hash(changed)
    invalid = parent.__class__(
        source_path=parent.source_path,
        schema_path=parent.schema_path,
        document=changed,
        config_hash=changed["config_hash"],
        status="draft",
    )
    with pytest.raises(AssignmentBindingError, match="must still be null"):
        embed_approved_assignment_document(invalid, assignment())


@pytest.mark.parametrize(
    ("path", "value", "message"),
    [
        (("approval_decision",), "APPROVE_OTHER", "approval token"),
        (("test_materialization_allowed",), True, "forbid test"),
        (("research_splits_authorized",), ["dev", "val"], "research splits"),
        (("parent_draft_config_hash",), "dev-" + "0" * 64, "parent draft hash"),
    ],
)
def test_wrapper_lifecycle_tamper_is_refused(
    tmp_path: Path,
    path: tuple[str, ...],
    value: object,
    message: str,
) -> None:
    current = bound_config(tmp_path)
    document = copy.deepcopy(dict(current.document))
    document["values"]["scenario_manifest"][path[0]] = value
    rehash_config(document)
    schema = json.loads(SCHEMA_PATH.read_text(encoding="utf-8"))
    mutated = validate_config_document(
        document,
        source_path=tmp_path / "draft-mutated.json",
        schema=schema,
        schema_path=SCHEMA_PATH,
    )
    with pytest.raises(AssignmentBindingError, match=message):
        validate_approved_assignment_binding(mutated)


def test_non_manifest_config_change_breaks_parent_reconstruction(tmp_path: Path) -> None:
    current = bound_config(tmp_path)
    document = copy.deepcopy(dict(current.document))
    document["values"]["timing"]["window_steps"] += 1
    rehash_config(document)
    schema = json.loads(SCHEMA_PATH.read_text(encoding="utf-8"))
    mutated = validate_config_document(
        document,
        source_path=tmp_path / "draft-mutated.json",
        schema=schema,
        schema_path=SCHEMA_PATH,
    )
    with pytest.raises(AssignmentBindingError, match="reconstruct the exact"):
        validate_approved_assignment_binding(mutated)


def test_external_assignment_mismatch_is_refused(tmp_path: Path) -> None:
    current = bound_config(tmp_path)
    external = assignment()
    external["evidence_boundary"] = list(external["evidence_boundary"]) + ["mutation"]
    with pytest.raises(AssignmentBindingError, match="differs from the tracked"):
        validate_approved_assignment_binding(current, expected_assignment=external)
