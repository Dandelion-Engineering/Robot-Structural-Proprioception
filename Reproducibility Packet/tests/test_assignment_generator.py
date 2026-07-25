"""Contract and smoke tests for the approved assignment-driven generator."""

from __future__ import annotations

import json
import sys
from dataclasses import replace
from pathlib import Path

import pytest

PACKET_ROOT = Path(__file__).resolve().parents[1]
SCRIPTS_ROOT = PACKET_ROOT / "scripts"
sys.path.insert(0, str(SCRIPTS_ROOT))

from utils.assignment_binding import validate_approved_assignment_binding  # noqa: E402
from utils.assignment_generator import (  # noqa: E402
    AssignmentGenerationError,
    _fault_components,
    _physical_config,
    _profile,
    _runtime_parameters,
    _step_index,
    audit_materialized_base_dataset,
    audit_manifest_against_assignment,
    build_identity_manifest,
    materialize_base_dataset,
    preflight_assigned_mechanics,
)
from utils.config_contract import load_config  # noqa: E402
from utils.gate3_assignment import expand_reservations, load_assignment  # noqa: E402
from utils.role_contract import RolePayloadLoader  # noqa: E402
from utils.storage_contract import (  # noqa: E402
    DeployableObservationLoader,
    read_identity_manifest,
)

SCHEMA_PATH = PACKET_ROOT / "schema" / "schema.json"
CONFIG_PATH = PACKET_ROOT / "config" / "draft-config-v0.1.json"
ASSIGNMENT_PATH = PACKET_ROOT / "config" / "proposed-gate3-assignment-v0.1.json"


def binding():
    config = load_config(CONFIG_PATH, SCHEMA_PATH)
    assignment = load_assignment(ASSIGNMENT_PATH)
    return validate_approved_assignment_binding(
        config, expected_assignment=assignment
    )


def schema():
    return json.loads(SCHEMA_PATH.read_text(encoding="utf-8"))


def test_base_identity_expansion_is_complete_non_test_and_seed_zero() -> None:
    rows, reservations = build_identity_manifest(binding())
    assert len(reservations) == 152 + 152 + 168
    assert len(rows) == len(reservations) * 3
    assert {row.suite for row in rows} == {"C0", "C1", "S"}
    assert {row.train_seed for row in rows} == {0}
    assert {row.split for row in rows} == {"dev", "pilot", "val"}
    assert not any("test" in row.run_id for row in rows)


def test_test_selection_and_missing_matched_suite_are_refused() -> None:
    with pytest.raises(AssignmentGenerationError, match="subset"):
        build_identity_manifest(binding(), splits=("test",))
    with pytest.raises(AssignmentGenerationError, match="matched C1/S"):
        build_identity_manifest(binding(), suites=("C1",))


def test_direct_manifest_audit_rejects_approved_field_tamper() -> None:
    current = binding()
    rows, reservations = build_identity_manifest(
        current, splits=("dev",), suites=("C1", "S"), reservation_limit=1
    )
    rows[0] = replace(rows[0], payload_id="payload_tampered")
    with pytest.raises(AssignmentGenerationError, match="payload_id differs"):
        audit_manifest_against_assignment(
            rows,
            reservations,
            expected_suites=("C1", "S"),
            config_hash=current.config.config_hash,
        )


def test_all_authorized_payload_masses_pass_real_mujoco_preflight() -> None:
    current = binding()
    _, reservations = build_identity_manifest(current)
    audit = preflight_assigned_mechanics(current, reservations)
    assert audit["all_exact"]
    assert set(audit["payload_masses_kg"].values()) == {
        0.0,
        0.025,
        0.05,
        0.075,
        0.1,
        0.125,
        0.15,
        0.2,
    }


def test_generator_runtime_constants_come_from_the_bound_config() -> None:
    """Use config timing/mechanics authority rather than duplicate literals."""

    current = binding()
    runtime = _runtime_parameters(current)
    timing = current.config.document["values"]["timing"]
    plant = current.config.document["values"]["plant"]
    assert runtime.control_dt_s == timing["control_dt_s"]
    assert runtime.f_ctrl_hz == timing["f_ctrl_hz"]
    assert runtime.simulation_timestep_s == plant["simulation_timestep_s"]
    assert runtime.point_count == plant["point_count_per_link"]
    assert _step_index(1.0, runtime.control_dt_s) == 500
    assert _step_index(1.0, 0.004) == 250
    with pytest.raises(AssignmentGenerationError, match="not aligned"):
        _step_index(1.001, 0.004)


def test_assigned_contact_window_and_compound_injection_boundaries() -> None:
    document = load_assignment(ASSIGNMENT_PATH)
    control_dt_s = _runtime_parameters(binding()).control_dt_s
    reservations = expand_reservations(document)
    contacts = {
        item["id"]: item
        for item in document["context_profiles"]["contacts"]
        if item["endpoint_plane_z_m"] is not None
    }
    for contact_id, contact in contacts.items():
        reservation = next(
            row for row in reservations if row.contact_profile_id == contact_id
        )
        _, trajectory = _profile(document, reservation)
        physical_config = _physical_config(
            document,
            reservation,
            trajectory,
            control_dt_s=control_dt_s,
        )
        assert physical_config.control_dt_s == control_dt_s
        offsets = contact["contact_window_offset_s"]
        assert physical_config.endpoint_contact_enabled
        assert physical_config.endpoint_contact_plane_z_m == 0.2
        assert physical_config.endpoint_contact_window_s == pytest.approx(
            (
                float(trajectory["onset_time_s"]) + float(offsets[0]),
                float(trajectory["onset_time_s"]) + float(offsets[1]),
            )
        )

    plant_sensor = next(
        row
        for row in reservations
        if row.fault_setting_id == "fault_val_ood_structure_sensor_bias"
    )
    physical, sensor, setting = _fault_components(
        document,
        plant_sensor,
        control_dt_s=control_dt_s,
    )
    _, plant_sensor_trajectory = _profile(document, plant_sensor)
    expected_onset_index = _step_index(
        float(plant_sensor_trajectory["onset_time_s"]),
        control_dt_s,
    )
    assert [fault.source_class for fault in physical] == ["structure"]
    assert physical[0].onset_index == expected_onset_index
    assert sensor is not None and sensor.source_class == "sensor"
    assert sensor.onset_index == expected_onset_index
    assert abs(sensor.severity) == pytest.approx(0.055)
    assert setting["label"]["ood_flag"] is True

    plant_plant = next(
        row
        for row in reservations
        if row.fault_setting_id == "fault_test_ood_structure_actuator"
    )
    physical, sensor, _ = _fault_components(
        document,
        plant_plant,
        control_dt_s=control_dt_s,
    )
    assert [fault.source_class for fault in physical] == [
        "structure",
        "actuator",
    ]
    assert sensor is None


def test_truncated_smoke_writes_real_roles_and_hash_checked_loaders(
    tmp_path: Path,
) -> None:
    current = binding()
    output = tmp_path / "dataset"
    audit = materialize_base_dataset(
        current,
        schema(),
        output,
        splits=("dev",),
        suites=("C1", "S"),
        reservation_limit=1,
        max_steps=8,
    )
    assert audit["status"] == "truncated_smoke_not_research_data"
    assert audit["test_identity_or_payload_rows"] == 0
    manifest = read_identity_manifest(output / "manifest.csv")
    assert len(manifest) == 2
    for suite in ("C1", "S"):
        observations = DeployableObservationLoader(
            output / "observations" / suite,
            suite,
            current.config,
        )
        assert observations.audit_all() == {
            "dev": 1,
            "pilot": 0,
            "val": 0,
            "test": 0,
        }
    for role in ("plant", "labels"):
        loader = RolePayloadLoader(
            output / role,
            role,
            schema(),
            current.config,
        )
        assert loader.audit_all() == 2
    independent = audit_materialized_base_dataset(
        current,
        schema(),
        output,
        expected_splits=("dev",),
        allow_partial=True,
    )
    assert independent["status"] == "partial_base_dataset_audit_pass"
    assert independent["shared_channel_pairs"] == 1
    assert independent["byte_identical_plant_pairs"] == 1
