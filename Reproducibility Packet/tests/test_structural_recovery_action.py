"""Tests for the bounded structural recovery action-family screen."""

from __future__ import annotations

import sys
from pathlib import Path

import pytest

SCRIPTS_DIR = Path(__file__).resolve().parents[1] / "scripts"
sys.path.insert(0, str(SCRIPTS_DIR))

from screen_structural_recovery_action import (  # noqa: E402
    StructuralRecoveryScreenSpec,
    decide_assessment,
    select_candidate,
)


def _row(
    action_id: str,
    seed: int,
    reduction_pct: float,
    *,
    source: str = "structure",
    baseline_j: float = 1.0,
    safe: bool = True,
) -> dict[str, object]:
    """Return one synthetic row whose paired reduction is explicit."""

    is_baseline = action_id == "no_action_1p00"
    return {
        "physical_source": source,
        "sensor_seed": seed,
        "action_id": action_id,
        "predecision_hash": f"{source}-{seed}",
        "tracking_integral_5s_m_s": (
            baseline_j if is_baseline else baseline_j * (1.0 - reduction_pct / 100.0)
        ),
        "classification_evaluations": 1,
        "command_changed_before_decision": False,
        "command_changed_steps": 0 if is_baseline else 100,
        "safety_incident_steps": 0 if safe else 1,
        "saturation_steps": 0,
    }


def test_spec_pins_disjoint_roles_and_explicit_old_and_no_action_floors() -> None:
    """The screen cannot tune on assessment seeds or omit its comparison arms."""

    spec = StructuralRecoveryScreenSpec()
    spec.validate()
    assert set(spec.tuning_seeds).isdisjoint(spec.assessment_seeds)
    identifiers = {candidate.action_id for candidate in spec.candidates}
    assert {"current_derate_0p75", spec.no_action_id} <= identifiers
    with pytest.raises(ValueError, match="disjoint"):
        StructuralRecoveryScreenSpec(
            tuning_seed_start=10,
            tuning_seed_count=3,
            assessment_seed_start=12,
            assessment_seed_count=2,
        ).validate()


def test_selection_uses_minimum_paired_reduction_and_rejects_unsafe_winner() -> None:
    """Mean performance cannot hide a weak seed or an A1/saturation failure."""

    spec = StructuralRecoveryScreenSpec(tuning_seed_count=2)
    rows = []
    for seed in spec.tuning_seeds:
        for candidate in spec.candidates:
            reduction = {
                "no_action_1p00": 0.0,
                "global_1p25": 12.0,
                "global_1p50": 20.0,
            }.get(candidate.action_id, -5.0)
            rows.append(
                _row(
                    candidate.action_id,
                    seed,
                    reduction,
                    safe=candidate.action_id != "global_1p50",
                )
            )
    selected, summaries = select_candidate(spec, rows)
    assert selected == "global_1p25"
    unsafe = next(row for row in summaries if row["action_id"] == "global_1p50")
    assert unsafe["tracking_gate_pass"] and not unsafe["candidate_gate_pass"]


def test_assessment_blocks_a_generic_gain_change_that_helps_healthy_more() -> None:
    """A generally better gain is not mislabeled as structural recovery."""

    spec = StructuralRecoveryScreenSpec(assessment_seed_count=2)
    selected = "global_1p25"
    rows = []
    for seed in spec.assessment_seeds:
        rows.extend(
            [
                _row(spec.no_action_id, seed, 0.0, source="structure"),
                _row(selected, seed, 12.0, source="structure"),
                _row(spec.no_action_id, seed, 0.0, source="healthy"),
                _row(selected, seed, 15.0, source="healthy"),
            ]
        )
    decision = decide_assessment(spec, selected, rows)
    assert decision["structural_tracking_gate_pass"]
    assert decision["healthy_false_authorization_safety_pass"]
    assert not decision["source_specificity_gate_pass"]
    assert decision["overall_decision"] == "BLOCK_STRUCTURAL_RECOVERY_ACTION_FAMILY"


@pytest.mark.parametrize(
    ("field", "value"),
    [("classification_evaluations", 0), ("command_changed_steps", 0)],
)
def test_assessment_requires_the_healthy_false_action_to_be_exercised(
    field: str, value: int
) -> None:
    """A skipped false-action stress cannot support a source-specific advance."""

    spec = StructuralRecoveryScreenSpec(assessment_seed_count=2)
    selected = "global_1p25"
    rows = []
    for seed in spec.assessment_seeds:
        rows.extend(
            [
                _row(spec.no_action_id, seed, 0.0, source="structure"),
                _row(selected, seed, 14.0, source="structure"),
                _row(spec.no_action_id, seed, 0.0, source="healthy"),
                _row(selected, seed, 3.0, source="healthy"),
            ]
        )
    next(
        row
        for row in rows
        if row["physical_source"] == "healthy" and row["action_id"] == selected
    )[field] = value
    decision = decide_assessment(spec, selected, rows)
    assert not decision["healthy_false_authorization_safety_pass"]
    assert decision["overall_decision"] == "BLOCK_STRUCTURAL_RECOVERY_ACTION_FAMILY"


def test_assessment_advances_only_a_safe_source_specific_tracking_action() -> None:
    """The positive path requires disjoint tracking, safety, and specificity passes."""

    spec = StructuralRecoveryScreenSpec(assessment_seed_count=2)
    selected = "global_1p25"
    rows = []
    for seed in spec.assessment_seeds:
        rows.extend(
            [
                _row(spec.no_action_id, seed, 0.0, source="structure"),
                _row(selected, seed, 14.0, source="structure"),
                _row(spec.no_action_id, seed, 0.0, source="healthy"),
                _row(selected, seed, 3.0, source="healthy"),
            ]
        )
    decision = decide_assessment(spec, selected, rows)
    assert decision["structural_tracking_gate_pass"]
    assert decision["healthy_false_authorization_safety_pass"]
    assert decision["source_specificity_gate_pass"]
    assert decision["overall_decision"] == (
        "ADVANCE_STRUCTURAL_INVERSE_STIFFNESS_ACTION_TO_NOISY_REVIEW"
    )
