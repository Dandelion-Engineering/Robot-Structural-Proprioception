"""Tests for the role-separated fault tracking-deficit development screen."""

from __future__ import annotations

import copy
import sys
from pathlib import Path

import pytest

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "scripts"))

from screen_fault_tracking_deficit import (  # noqa: E402
    FaultTrackingDeficitSpec,
    _faults_for_case,
    _paired_deficits,
    decide,
    summarize_role,
)


def _row(
    case_id: str,
    source: str,
    seed: int,
    deficit_pct: float,
    *,
    pre_fault_hash: str | None = None,
) -> dict[str, object]:
    """Return one minimal no-recovery row with an exact paired deficit."""

    return {
        "case_id": case_id,
        "source_class": source,
        "sensor_seed": seed,
        "pre_fault_hash": pre_fault_hash or f"paired-{seed}",
        "tracking_integral_5s_m_s": 1.0 + deficit_pct / 100.0,
        "classification_evaluations": 1,
        "recovery_command_changed_steps": 0,
        "recovery_changed_before_decision": False,
        "safety_incident_steps": 0,
        "saturation_steps": 0,
    }


def _role_rows(spec: FaultTrackingDeficitSpec, seed_count: int) -> list[dict[str, object]]:
    """Return a complete grid with known mildest-passing settings."""

    structure_deficits = {0.75: 5.0, 0.50: 13.0, 0.25: 20.0, 0.10: 25.0, 0.05: 30.0}
    actuator_deficits = {0.85: 4.0, 0.70: 11.0, 0.50: 16.0, 0.25: 25.0, 0.10: 35.0}
    rows: list[dict[str, object]] = []
    for seed in range(seed_count):
        rows.append(_row(spec.healthy_case.case_id, "healthy", seed, 0.0))
        for case in spec.candidate_cases("structure"):
            rows.append(
                _row(
                    case.case_id,
                    "structure",
                    seed,
                    structure_deficits[case.severity],
                )
            )
        for case in spec.candidate_cases("actuator"):
            rows.append(
                _row(
                    case.case_id,
                    "actuator",
                    seed,
                    actuator_deficits[case.severity],
                )
            )
    return rows


def test_fault_boundary_keeps_encoder_corruption_out_of_the_plant() -> None:
    """The sensor control uses a healthy plant plus an observation-side fault."""

    spec = FaultTrackingDeficitSpec()
    plant_fault, sensor_fault = _faults_for_case(spec.sensor_control_case, 500)
    assert plant_fault.source_class == "healthy"
    assert sensor_fault is not None
    assert sensor_fault.source_class == "sensor"
    assert sensor_fault.subtype == "encoder_bias"
    structure_fault, no_sensor_fault = _faults_for_case(
        spec.candidate_cases("structure")[0], 500
    )
    assert structure_fault.source_class == "structure"
    assert no_sensor_fault is None


def test_paired_deficit_requires_exact_pre_fault_crn_matching() -> None:
    """A case cannot be compared to a healthy arm with a different pre-fault history."""

    spec = FaultTrackingDeficitSpec()
    case = spec.candidate_cases("structure")[0]
    rows = [
        _row(spec.healthy_case.case_id, "healthy", 1, 0.0),
        _row(case.case_id, "structure", 1, 12.0),
    ]
    deficits = _paired_deficits(rows, spec.healthy_case.case_id)
    assert deficits[case.case_id] == pytest.approx([12.0])
    rows[1]["pre_fault_hash"] = "mismatch"
    with pytest.raises(ValueError, match="pre-fault CRN mismatch"):
        _paired_deficits(rows, spec.healthy_case.case_id)


def test_tuning_selects_the_mildest_setting_with_twelve_percent_headroom() -> None:
    """Selection minimizes fault severity after every lifecycle/safety gate clears."""

    spec = FaultTrackingDeficitSpec(tuning_seed_count=2)
    selected, summaries = summarize_role(
        spec, _role_rows(spec, 2), expected_seed_count=2
    )
    assert selected == {
        "structure": "structure_ei_remaining_0p50",
        "actuator": "actuator_gain_remaining_0p50",
    }
    mild_structure = next(
        row for row in summaries if row["case_id"] == "structure_ei_remaining_0p75"
    )
    selected_structure = next(
        row for row in summaries if row["case_id"] == selected["structure"]
    )
    assert not mild_structure["headroom_gate_pass"]
    assert selected_structure["minimum_tracking_deficit_pct"] == pytest.approx(13.0)
    assert selected_structure["candidate_gate_pass"]


@pytest.mark.parametrize(
    ("field", "value"),
    [
        ("classification_evaluations", 2),
        ("recovery_command_changed_steps", 1),
        ("recovery_changed_before_decision", True),
        ("safety_incident_steps", 1),
        ("saturation_steps", 1),
    ],
)
def test_candidate_cannot_advance_with_a_broken_no_recovery_contract(
    field: str, value: object
) -> None:
    """Headroom alone cannot override lifecycle, A1, or saturation failures."""

    spec = FaultTrackingDeficitSpec(tuning_seed_count=2)
    rows = _role_rows(spec, 2)
    target_id = "structure_ei_remaining_0p50"
    next(row for row in rows if row["case_id"] == target_id)[field] = value
    selected, summaries = summarize_role(spec, rows, expected_seed_count=2)
    target = next(row for row in summaries if row["case_id"] == target_id)
    assert not target["candidate_gate_pass"]
    assert selected["structure"] == "structure_ei_remaining_0p25"


@pytest.mark.parametrize(
    ("field", "value"),
    [
        ("classification_evaluations", 2),
        ("recovery_command_changed_steps", 1),
        ("recovery_changed_before_decision", True),
        ("safety_incident_steps", 1),
        ("saturation_steps", 1),
    ],
)
def test_no_candidate_can_advance_against_an_unsound_healthy_baseline(
    field: str, value: object
) -> None:
    """The denominator rows carry the same no-action lifecycle and safety contract."""

    spec = FaultTrackingDeficitSpec(tuning_seed_count=2)
    rows = _role_rows(spec, 2)
    next(row for row in rows if row["case_id"] == spec.healthy_case.case_id)[
        field
    ] = value
    selected, summaries = summarize_role(spec, rows, expected_seed_count=2)
    assert selected == {"structure": None, "actuator": None}
    assert not any(row["candidate_gate_pass"] for row in summaries)


def test_disjoint_assessment_can_advance_one_source_and_block_the_other() -> None:
    """The final label reflects only tuning-preselected settings that re-pass assessment."""

    spec = FaultTrackingDeficitSpec(tuning_seed_count=2, assessment_seed_count=2)
    tuning_selected, _ = summarize_role(
        spec, _role_rows(spec, 2), expected_seed_count=2
    )
    assessment_rows = _role_rows(spec, 2)
    broken = copy.deepcopy(assessment_rows)
    for row in broken:
        if row["case_id"] == tuning_selected["structure"]:
            row["tracking_integral_5s_m_s"] = 1.05
    _, assessment_summaries = summarize_role(spec, broken, expected_seed_count=2)
    decision = decide(spec, tuning_selected, assessment_summaries)
    assert not decision["source_results"]["structure"]["assessment_gate_pass"]
    assert decision["source_results"]["actuator"]["assessment_gate_pass"]
    assert decision["overall_decision"] == (
        "ADVANCE_ACTUATOR_DEFICIT_ONLY_BLOCK_STRUCTURAL_DEFICIT"
    )


def test_spec_rejects_overlapping_roles_and_unsorted_severity_grid() -> None:
    """Role leakage and ambiguous severity ordering fail before any rollout."""

    with pytest.raises(ValueError, match="disjoint"):
        FaultTrackingDeficitSpec(
            tuning_seed_start=10,
            tuning_seed_count=2,
            assessment_seed_start=11,
            assessment_seed_count=2,
        ).validate()
    with pytest.raises(ValueError, match="strictly descending"):
        FaultTrackingDeficitSpec(
            structural_ei_remaining_grid=(0.50, 0.75)
        ).validate()
