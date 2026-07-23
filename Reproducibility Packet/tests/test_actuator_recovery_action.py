"""Regressions for the actuator recovery-action development screen."""

from __future__ import annotations

import copy
import sys
from pathlib import Path

import numpy as np
import pytest

SCRIPTS = Path(__file__).resolve().parents[1] / "scripts"
sys.path.insert(0, str(SCRIPTS))

import screen_actuator_recovery_action as screen  # noqa: E402


def _row(
    *,
    role: str,
    seed: int,
    source: str,
    diagnosis: str,
    candidate: str,
    j_5s: float,
    multiplier: float = 1.0,
) -> dict:
    """Return one audit-clean synthetic row."""

    return {
        "role": role,
        "seed": seed,
        "physical_source": source,
        "diagnosis": diagnosis,
        "candidate_label": candidate,
        "suite": "S" if diagnosis != "C1" else "C1",
        "maximum_gain_compensation": 4.0,
        "minimum_gain_remaining": 0.25,
        "estimated_severity": None if diagnosis == "no_action" else 0.25,
        "severity_uncertainty": 0.0,
        "expected_multiplier": multiplier,
        "applied_multiplier_mean": multiplier,
        "applied_multiplier_max_error": 0.0,
        "run_id": f"{role}-{seed}-{source}-{diagnosis}-{candidate}",
        "j_5s": j_5s,
        "predecision_hash": f"{role}-{seed}-{source}",
        "classification_evaluations": 1,
        "recovery_command_changed_steps": 0 if diagnosis == "no_action" else 10,
        "predecision_command_changed_steps": 0,
        "a1_incident_steps": 0,
        "saturation_steps": 0,
        "peak_contact_force_n": 1.0,
        "max_abs_gauge_microstrain": 20.0,
    }


def _tuning_rows(
    *,
    candidate_label: str = "cap4_floor0p25",
    fault_reduction_pct: float = 20.0,
    healthy_benefit_pct: float = 5.0,
) -> list[dict]:
    """Return tuning rows for one candidate and all required references."""

    rows: list[dict] = []
    for seed in screen.TUNING_SEEDS:
        fault_no = 1.0
        healthy_no = 0.8
        rows.extend(
            [
                _row(
                    role="tuning",
                    seed=seed,
                    source="actuator",
                    diagnosis="no_action",
                    candidate="reference",
                    j_5s=fault_no,
                ),
                _row(
                    role="tuning",
                    seed=seed,
                    source="healthy",
                    diagnosis="no_action",
                    candidate="reference",
                    j_5s=healthy_no,
                ),
                _row(
                    role="tuning",
                    seed=seed,
                    source="actuator",
                    diagnosis="oracle",
                    candidate=candidate_label,
                    j_5s=fault_no * (1.0 - fault_reduction_pct / 100.0),
                    multiplier=4.0,
                ),
                _row(
                    role="tuning",
                    seed=seed,
                    source="healthy",
                    diagnosis="oracle",
                    candidate=candidate_label,
                    j_5s=healthy_no * (1.0 - healthy_benefit_pct / 100.0),
                    multiplier=4.0,
                ),
            ]
        )
    return rows


def _assessment_rows(
    *,
    candidate_label: str = "cap4_floor0p25",
    fault_reduction_pct: float = 20.0,
    healthy_benefit_pct: float = 5.0,
) -> list[dict]:
    """Return complete selected-profile synthetic assessment rows."""

    rows: list[dict] = []
    for seed in screen.ASSESSMENT_SEEDS:
        fault_no = 1.0
        healthy_no = 0.8
        rows.extend(
            [
                _row(
                    role="assessment",
                    seed=seed,
                    source="actuator",
                    diagnosis="no_action",
                    candidate="reference",
                    j_5s=fault_no,
                ),
                _row(
                    role="assessment",
                    seed=seed,
                    source="healthy",
                    diagnosis="no_action",
                    candidate="reference",
                    j_5s=healthy_no,
                ),
            ]
        )
        for diagnosis in ("oracle", "C1", "S"):
            rows.extend(
                [
                    _row(
                        role="assessment",
                        seed=seed,
                        source="actuator",
                        diagnosis=diagnosis,
                        candidate=candidate_label,
                        j_5s=fault_no * (1.0 - fault_reduction_pct / 100.0),
                        multiplier=4.0,
                    ),
                    _row(
                        role="assessment",
                        seed=seed,
                        source="healthy",
                        diagnosis=diagnosis,
                        candidate=candidate_label,
                        j_5s=healthy_no * (1.0 - healthy_benefit_pct / 100.0),
                        multiplier=4.0,
                    ),
                ]
            )
    return rows


@pytest.mark.parametrize(
    ("cap", "floor", "should_raise"),
    [
        (2.0, 0.25, False),
        (0.9, 0.25, True),
        (2.0, 0.0, True),
        (2.0, 1.1, True),
    ],
)
def test_candidate_validation(cap: float, floor: float, should_raise: bool) -> None:
    """Candidate validation rejects non-physical cap/floor values."""

    candidate = screen.ActuatorActionCandidate("candidate", cap, floor)
    if should_raise:
        with pytest.raises(ValueError):
            candidate.validate()
    else:
        candidate.validate()


def test_expected_multiplier_uses_cap_and_floor() -> None:
    """Expected multiplier mirrors the shipped inverse-gain controller."""

    spec = screen.ActuatorActionArmSpec(
        "assessment",
        1,
        "actuator",
        "S",
        "candidate",
        5.0,
        0.20,
        0.10,
        0.01,
        "S",
    )
    assert screen.expected_multiplier(spec) == pytest.approx(5.0)
    floor_limited = screen.ActuatorActionArmSpec(
        **{**spec.__dict__, "minimum_gain_remaining": 0.25}
    )
    assert screen.expected_multiplier(floor_limited) == pytest.approx(4.0)


def test_tuning_grid_is_complete_and_reference_efficient() -> None:
    """Tuning shares two references per seed instead of duplicating them per candidate."""

    specs = screen.build_tuning_specs()
    assert len(specs) == len(screen.TUNING_SEEDS) * (
        2 + 2 * len(screen.CANDIDATES)
    )
    for seed in screen.TUNING_SEEDS:
        references = [
            spec
            for spec in specs
            if spec.seed == seed and spec.diagnosis == "no_action"
        ]
        assert len(references) == 2


def test_assessment_grid_carries_selected_and_floor_stress_profiles() -> None:
    """Assessment includes oracle/C1/S at selection plus both cap-5 floor stresses."""

    estimates = {
        suite: {seed: 0.25 for seed in screen.ASSESSMENT_SEEDS}
        for suite in ("C1", "S")
    }
    uncertainties = {"C1": 0.01, "S": 0.02}
    specs = screen.build_assessment_specs(
        "cap4_floor0p25", estimates, uncertainties
    )
    assert len(specs) == len(screen.ASSESSMENT_SEEDS) * 16
    labels = {spec.candidate_label for spec in specs}
    assert {
        "reference",
        "cap4_floor0p25",
        "cap5_floor0p25",
        "cap5_floor0p20",
    } <= labels


def test_tuning_summary_credits_only_source_specific_margin() -> None:
    """A large fault benefit is reduced by the identical healthy authorization benefit."""

    candidate = screen.ActuatorActionCandidate("cap4_floor0p25", 4.0, 0.25)
    rows = _tuning_rows(fault_reduction_pct=20.0, healthy_benefit_pct=5.0)
    summary = screen.summarize_tuning_candidates(rows, (candidate,))[0]
    assert summary["mean_fault_reduction_pct"] == pytest.approx(20.0)
    assert summary[
        "mean_healthy_false_authorization_benefit_pct"
    ] == pytest.approx(5.0)
    assert summary["mean_source_specific_margin_pp"] == pytest.approx(15.0)
    assert summary["specificity_gate_pass"] is True


def test_selection_ranks_specificity_before_raw_tracking() -> None:
    """The generic high-tracking arm cannot outrank the more specific arm."""

    summaries = [
        {
            "candidate_label": "generic",
            "maximum_gain_compensation": 5.0,
            "minimum_gain_remaining": 0.2,
            "mean_fault_reduction_pct": 30.0,
            "mean_source_specific_margin_pp": 5.0,
            "tracking_gate_pass": True,
            "specificity_gate_pass": False,
            "lifecycle_safety_gate_pass": True,
        },
        {
            "candidate_label": "specific",
            "maximum_gain_compensation": 4.0,
            "minimum_gain_remaining": 0.25,
            "mean_fault_reduction_pct": 20.0,
            "mean_source_specific_margin_pp": 15.0,
            "tracking_gate_pass": True,
            "specificity_gate_pass": True,
            "lifecycle_safety_gate_pass": True,
        },
    ]
    assert screen.select_candidate(summaries) == ("specific", True)


def test_assessment_summary_requires_point_bar_and_nonzero_interval() -> None:
    """A stable 15-point paired margin passes the development assessment gate."""

    summaries = screen.summarize_assessment(
        _assessment_rows(fault_reduction_pct=20.0, healthy_benefit_pct=5.0),
        "cap4_floor0p25",
    )
    assert {row["diagnosis"] for row in summaries} == {"oracle", "C1", "S"}
    for row in summaries:
        assert row["mean_source_specific_margin_pp"] == pytest.approx(15.0)
        assert row["source_specific_margin_interval"]["excludes_zero"] is True
        assert row["advance_gate_pass"] is True


def test_assessment_summary_blocks_generic_benefit() -> None:
    """A large raw recovery with a sub-bar source-specific margin remains blocked."""

    summaries = screen.summarize_assessment(
        _assessment_rows(fault_reduction_pct=20.0, healthy_benefit_pct=15.0),
        "cap4_floor0p25",
    )
    assert all(not row["advance_gate_pass"] for row in summaries)


def test_bootstrap_interval_is_deterministic() -> None:
    """The paired development interval is reproducible under its recorded seed."""

    first = screen._bootstrap_margin([12.0, 13.0, 14.0, 15.0], rng_seed=7)
    second = screen._bootstrap_margin([12.0, 13.0, 14.0, 15.0], rng_seed=7)
    assert first == second
    assert first["excludes_zero"] is True


def _passing_audit() -> dict:
    """Return a complete passing audit dictionary."""

    return {
        "tuning_arm_grid_complete": True,
        "assessment_arm_grid_complete": True,
        "roles_disjoint": True,
        "one_classification_per_arm": True,
        "no_predecision_action": True,
        "withheld_and_acting_behavior_correct": True,
        "reference_a1_clean": True,
        "reference_saturation_clean": True,
        "reference_multiplier_identity_pass": True,
        "predecision_crn_match": True,
        "recorded_step15_reference_match": True,
        "selected_candidate_present_in_assessment": True,
    }


@pytest.mark.parametrize("field", list(_passing_audit()))
def test_every_audit_field_fails_loudly(field: str) -> None:
    """No computed integrity condition can remain narrative-only."""

    audit = _passing_audit()
    audit[field] = False
    with pytest.raises(RuntimeError, match=field):
        screen.require_passing_audit(audit)


def test_missing_audit_field_fails_loudly() -> None:
    """A dropped audit key cannot default-pass."""

    audit = _passing_audit()
    audit.pop("reference_a1_clean")
    with pytest.raises(RuntimeError, match="reference_a1_clean"):
        screen.require_passing_audit(audit)


def test_build_audit_checks_recorded_reference_and_crn() -> None:
    """The audit pins Step-15 J5 reuse and within-source predecision equality."""

    rows = _assessment_rows()
    recorded = {
        source: {
            seed: next(
                row["j_5s"]
                for row in rows
                if row["seed"] == seed
                and row["physical_source"] == source
                and row["diagnosis"] == "no_action"
            )
            for seed in screen.ASSESSMENT_SEEDS
        }
        for source in ("healthy", "actuator")
    }
    audit = screen.build_audit(
        [],
        rows,
        recorded,
        selected_label="cap4_floor0p25",
        n_tuning_specs=0,
        n_assessment_specs=len(rows),
    )
    assert audit["recorded_step15_reference_match"] is True
    assert audit["predecision_crn_match"] is True

    broken = copy.deepcopy(rows)
    broken[-1]["predecision_hash"] = "different"
    audit = screen.build_audit(
        [],
        broken,
        recorded,
        selected_label="cap4_floor0p25",
        n_tuning_specs=0,
        n_assessment_specs=len(broken),
    )
    assert audit["predecision_crn_match"] is False


def test_candidate_a1_incident_is_a_scientific_block_not_audit_corruption() -> None:
    """A candidate safety failure is recorded while clean references preserve integrity."""

    rows = _assessment_rows()
    candidate = next(
        row for row in rows if row["candidate_label"] != "reference"
    )
    candidate["a1_incident_steps"] = 1
    recorded = {
        source: {
            seed: next(
                row["j_5s"]
                for row in rows
                if row["seed"] == seed
                and row["physical_source"] == source
                and row["diagnosis"] == "no_action"
            )
            for seed in screen.ASSESSMENT_SEEDS
        }
        for source in ("healthy", "actuator")
    }
    audit = screen.build_audit(
        [],
        rows,
        recorded,
        selected_label="cap4_floor0p25",
        n_tuning_specs=0,
        n_assessment_specs=len(rows),
    )
    assert audit["reference_a1_clean"] is True
    assert audit["candidate_a1_incident_arms"] == 1
    screen.require_passing_audit(audit)
