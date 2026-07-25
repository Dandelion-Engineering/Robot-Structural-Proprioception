"""Bind one jointly approved Gate-3 assignment into a later draft config.

The assignment was reviewed against a parent draft hash. Embedding the exact
assignment necessarily changes the draft config hash, so a direct
``assignment.draft_config_hash == current_config.config_hash`` requirement
would be circular. This module makes the lifecycle one-way and auditable:

1. the exact approved assignment remains byte-for-byte unchanged;
2. the current draft records the parent open-gate state and parent hash;
3. validation reconstructs that parent document from the current draft and
   proves its canonical hash;
4. the current draft self-hash then binds the approval wrapper and assignment.

Only ``dev``, ``pilot``, and ``val`` materialization is authorized. Test
identity and payload materialization remains forbidden until final freeze.
"""

from __future__ import annotations

import copy
from dataclasses import dataclass, replace
from typing import Any, Mapping

from .config_contract import ValidatedConfig, expected_config_hash
from .gate3_assignment import (
    APPROVAL_TOKEN,
    Gate3AssignmentError,
    expected_assignment_hash,
    validate_assignment,
)

GATE3_OPEN_GATE = "gate_3_jointly_approved_multi_setting_manifest"
AUTHORIZED_RESEARCH_SPLITS = ("dev", "pilot", "val")
WRAPPER_KEYS = (
    "approval_status",
    "approval_decision",
    "approved_assignment_hash",
    "parent_draft_config_hash",
    "parent_open_gates",
    "research_splits_authorized",
    "test_materialization_allowed",
    "assignment",
)


class AssignmentBindingError(ValueError):
    """Raised when an embedded approval is circular, stale, or over-authorized."""


@dataclass(frozen=True)
class ApprovedAssignmentBinding:
    """Validated one-way binding between parent draft, assignment, and new draft."""

    config: ValidatedConfig
    parent_config: ValidatedConfig
    assignment: Mapping[str, Any]
    proposal_audit: Mapping[str, Any]
    authorized_research_splits: tuple[str, ...]

    @property
    def assignment_hash(self) -> str:
        """Return the exact jointly approved assignment hash."""

        return str(self.assignment["assignment_hash"])


def _exact_keys(value: Mapping[str, Any], expected: tuple[str, ...], label: str) -> None:
    """Require one mapping to expose exactly the lifecycle-declared keys."""

    actual = set(value)
    required = set(expected)
    if actual != required:
        raise AssignmentBindingError(
            f"{label} keys mismatch; missing={sorted(required - actual)}, "
            f"unknown={sorted(actual - required)}"
        )


def embed_approved_assignment_document(
    parent_config: ValidatedConfig,
    assignment: Mapping[str, Any],
    *,
    approval_decision: str = APPROVAL_TOKEN,
) -> dict[str, Any]:
    """Return a rehashed draft document containing the exact approved assignment."""

    if parent_config.status != "draft" or parent_config.is_frozen:
        raise AssignmentBindingError("assignment embedding requires a draft parent config")
    values = parent_config.document.get("values")
    if not isinstance(values, Mapping) or values.get("scenario_manifest") is not None:
        raise AssignmentBindingError("parent draft scenario_manifest must still be null")
    parent_open_gates = parent_config.document.get("open_gates")
    if not isinstance(parent_open_gates, list) or parent_open_gates.count(GATE3_OPEN_GATE) != 1:
        raise AssignmentBindingError("parent draft must contain the Gate-3 open gate exactly once")
    if approval_decision != APPROVAL_TOKEN:
        raise AssignmentBindingError(f"approval decision must be {APPROVAL_TOKEN!r}")

    proposal_audit = validate_assignment(assignment, parent_config)
    if proposal_audit["same_state_approval_required"] != approval_decision:
        raise AssignmentBindingError("approval decision does not match assignment requirement")

    current = copy.deepcopy(dict(parent_config.document))
    wrapper = {
        "approval_status": "jointly_approved",
        "approval_decision": approval_decision,
        "approved_assignment_hash": str(assignment["assignment_hash"]),
        "parent_draft_config_hash": parent_config.config_hash,
        "parent_open_gates": list(parent_open_gates),
        "research_splits_authorized": list(AUTHORIZED_RESEARCH_SPLITS),
        "test_materialization_allowed": False,
        "assignment": copy.deepcopy(dict(assignment)),
    }
    current["values"]["scenario_manifest"] = wrapper
    current["open_gates"] = [
        gate for gate in parent_open_gates if gate != GATE3_OPEN_GATE
    ]
    if not current["open_gates"]:
        raise AssignmentBindingError("draft must retain at least one non-Gate-3 open gate")
    current["config_hash"] = expected_config_hash(current)
    return current


def validate_approved_assignment_binding(
    config: ValidatedConfig,
    *,
    expected_assignment: Mapping[str, Any] | None = None,
) -> ApprovedAssignmentBinding:
    """Validate and return the exact approved assignment embedded in a draft."""

    if config.status != "draft" or config.is_frozen:
        raise AssignmentBindingError("approved research generation requires a draft config")
    values = config.document.get("values")
    wrapper = values.get("scenario_manifest") if isinstance(values, Mapping) else None
    if not isinstance(wrapper, Mapping):
        raise AssignmentBindingError("draft scenario_manifest must contain an approval wrapper")
    _exact_keys(wrapper, WRAPPER_KEYS, "scenario_manifest approval wrapper")

    if wrapper["approval_status"] != "jointly_approved":
        raise AssignmentBindingError("scenario manifest is not jointly approved")
    if wrapper["approval_decision"] != APPROVAL_TOKEN:
        raise AssignmentBindingError("scenario manifest approval token is incorrect")
    if wrapper["test_materialization_allowed"] is not False:
        raise AssignmentBindingError("approved draft must still forbid test materialization")
    if tuple(wrapper["research_splits_authorized"]) != AUTHORIZED_RESEARCH_SPLITS:
        raise AssignmentBindingError(
            f"approved research splits must be exactly {AUTHORIZED_RESEARCH_SPLITS}"
        )

    assignment = wrapper["assignment"]
    if not isinstance(assignment, Mapping):
        raise AssignmentBindingError("embedded assignment must be an object")
    if assignment.get("assignment_hash") != wrapper["approved_assignment_hash"]:
        raise AssignmentBindingError("wrapper assignment hash does not match embedded assignment")
    if expected_assignment_hash(assignment) != assignment.get("assignment_hash"):
        raise AssignmentBindingError("embedded assignment self-hash is invalid")
    if expected_assignment is not None and dict(assignment) != dict(expected_assignment):
        raise AssignmentBindingError("embedded assignment differs from the tracked approved file")

    parent_hash = wrapper["parent_draft_config_hash"]
    if parent_hash != assignment.get("draft_config_hash"):
        raise AssignmentBindingError("parent draft hash does not match assignment binding")
    parent_open_gates = wrapper["parent_open_gates"]
    if not isinstance(parent_open_gates, list) or parent_open_gates.count(GATE3_OPEN_GATE) != 1:
        raise AssignmentBindingError("recorded parent open gates must contain Gate 3 once")
    expected_current_gates = [
        gate for gate in parent_open_gates if gate != GATE3_OPEN_GATE
    ]
    if config.document.get("open_gates") != expected_current_gates:
        raise AssignmentBindingError("current open gates are not the parent gates minus Gate 3")

    parent_document = copy.deepcopy(dict(config.document))
    parent_document["values"]["scenario_manifest"] = None
    parent_document["open_gates"] = list(parent_open_gates)
    parent_document["config_hash"] = parent_hash
    reconstructed_hash = expected_config_hash(parent_document)
    if reconstructed_hash != parent_hash:
        raise AssignmentBindingError(
            "current draft cannot reconstruct the exact approved parent config"
        )
    parent_config = replace(
        config,
        document=parent_document,
        config_hash=str(parent_hash),
        status="draft",
    )
    try:
        proposal_audit = validate_assignment(assignment, parent_config)
    except Gate3AssignmentError as exc:
        raise AssignmentBindingError(f"embedded assignment is not parent-valid: {exc}") from exc
    if config.config_hash == parent_hash:
        raise AssignmentBindingError("embedded draft hash must differ from its parent hash")

    return ApprovedAssignmentBinding(
        config=config,
        parent_config=parent_config,
        assignment=assignment,
        proposal_audit=proposal_audit,
        authorized_research_splits=AUTHORIZED_RESEARCH_SPLITS,
    )
