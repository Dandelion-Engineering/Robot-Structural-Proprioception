"""Tests for the bounded noisy held-decision information/lifecycle review."""

from __future__ import annotations

import sys
from pathlib import Path

import numpy as np
import pytest

SCRIPTS_DIR = Path(__file__).resolve().parents[1] / "scripts"
sys.path.insert(0, str(SCRIPTS_DIR))

from run_bounded_noisy_information_review import (  # noqa: E402
    BoundedNoisyInformationSpec,
    SelectivePrototypeReference,
    action_gate_state,
    classify_vector,
    decide,
    fit_selective_reference,
)


def test_spec_resolves_tail_and_pins_disjoint_exact_decision_roles() -> None:
    """The review cannot reuse seeds or fit an unresolved healthy tail."""

    spec = BoundedNoisyInformationSpec()
    spec.validate()
    mechanics = spec.mechanics_spec()
    assert spec.minimum_calibration_size == 100
    assert spec.calibration_seed_values[-1] == 14099
    assert spec.evaluation_seed_values[0] == spec.representative_seed == 14100
    assert set(spec.calibration_seed_values).isdisjoint(spec.evaluation_seed_values)
    assert mechanics.first_decision_step == 1136
    assert mechanics.first_decision_time_s == pytest.approx(2.272)
    assert mechanics.first_decision_time_s < mechanics.movement_start_s
    with pytest.raises(ValueError, match="cannot resolve"):
        BoundedNoisyInformationSpec(calibration_seeds=99).validate()


def test_reference_uses_resolved_detection_tail_and_low_risk_margin() -> None:
    """Detection and type-abstention thresholds use calibration samples only."""

    rng = np.random.default_rng(12)
    n_samples = 100
    healthy = rng.normal(0.0, 0.08, size=(n_samples, 2))
    samples = {
        "healthy": healthy,
        "structure": rng.normal((2.0, 0.0), 0.08, size=(n_samples, 2)),
        "actuator": rng.normal((-2.0, 0.0), 0.08, size=(n_samples, 2)),
        "sensor": rng.normal((0.0, 2.0), 0.08, size=(n_samples, 2)),
    }
    reference = fit_selective_reference(samples, BoundedNoisyInformationSpec())
    reference.validate()
    assert reference.detect_threshold < reference.calibration_null_scores.max()
    assert reference.calibration_selective_coverage == pytest.approx(1.0)
    assert reference.calibration_selective_error == pytest.approx(0.0)
    assert classify_vector(np.array([2.0, 0.0]), reference).predicted_source == "structure"


def test_ambiguous_fault_abstains_and_never_authorizes_recovery() -> None:
    """A detected low-margin type call must be explicit abstention, not action."""

    reference = SelectivePrototypeReference(
        healthy_mean=np.zeros(2),
        healthy_scale=np.ones(2),
        detect_threshold=0.01,
        fault_centroids={
            "structure": np.array([1.0, 0.0]),
            "actuator": np.array([-1.0, 0.0]),
            "sensor": np.array([0.0, 1.0]),
        },
        abstain_margin_threshold=0.50,
        calibration_null_scores=np.array([0.001, 0.002]),
        calibration_selective_coverage=0.8,
        calibration_selective_error=0.0,
    )
    ambiguous = classify_vector(np.array([0.0, 0.1]), reference)
    assert ambiguous.detected
    assert ambiguous.predicted_source == "sensor"
    assert ambiguous.abstained
    assert action_gate_state("structure", ambiguous) == "withheld_actionable_fault"

    clear = classify_vector(np.array([1.0, 0.0]), reference)
    assert clear.detected and not clear.abstained
    assert action_gate_state("structure", clear) == "correct_actionable"
    assert action_gate_state("healthy", clear) == "false_actionable"


def test_decision_does_not_merge_information_action_and_mechanics_gates() -> None:
    """An information pass cannot silently override an unsafe action/mechanics path."""

    spec = BoundedNoisyInformationSpec()
    information = [
        {"suite": "C1", "information_gate_pass": False, "action_gate_pass": True},
        {"suite": "S", "information_gate_pass": True, "action_gate_pass": False},
    ]
    heldout = [
        {"suite": suite, "action_gate_state": "false_actionable"}
        for suite in ("C1", "S")
    ]
    online = []
    for source in ("healthy", "structure", "actuator", "sensor"):
        for suite in ("C1", "S"):
            gate_state = (
                "correct_actionable"
                if source == "structure" and suite == "S"
                else "withheld_actionable_fault"
                if source == "structure"
                else "correct_no_action"
            )
            online.append(
                {
                    "source": source,
                    "suite": suite,
                    "predecision_plant_hash": source,
                    "predecision_shared_observation_hash": source,
                    "any_safety_flag": False,
                    "command_changed_before_decision": False,
                    "classification_evaluations": 1,
                    "action_gate_state": gate_state,
                    "tracking_integral_5s_m_s": (
                        1.2 if source == "structure" and suite == "S" else 1.0
                    ),
                    "safety_incident_steps": 0,
                }
            )
    predecision = [
        {"any_safety_flag": False, "contact_active_steps": 0}
        for _ in range(2)
    ]
    result = decide(spec, information, heldout, online, predecision)
    assert result["information_gate_pass"]
    assert not result["action_gate_pass"]
    assert result["representative_full_horizon_safety_pass"]
    assert not result["representative_control_sensitivity_pass"]
    assert result["matched_predecision_crn_pass"]
    assert result["overall_decision"] == (
        "ADVANCE_INFORMATION_REFERENCE_LIFECYCLE_ONLY_"
        "BLOCK_RECOVERY_CONTROL_PROFILE"
    )
