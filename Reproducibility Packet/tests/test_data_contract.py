"""Tests for the machine schema, config lifecycle, and role-storage boundary."""

from __future__ import annotations

import copy
import csv
import json
import sys
from dataclasses import replace
from pathlib import Path

import numpy as np
import pytest

PACKET_ROOT = Path(__file__).resolve().parents[1]
SCRIPTS_ROOT = PACKET_ROOT / "scripts"
sys.path.insert(0, str(SCRIPTS_ROOT))

from utils.config_contract import (  # noqa: E402
    ConfigContractError,
    canonical_json_bytes,
    expected_config_hash,
    file_sha256,
    load_config,
    validate_config_document,
    validate_machine_schema,
)
from utils.schema_types import (  # noqa: E402
    CHANNEL_NAMES,
    CHANNEL_WIDTH,
    CONTACT_STATE_FIELDS,
    SAFETY_FLAG_FIELDS,
    SCHEMA_VERSION,
    SUITE_CHANNELS,
)
from utils.estimator import EstimatorOutput, EstimatorTrace  # noqa: E402
from utils.sensor_model import SensorModel  # noqa: E402
from utils.storage_contract import (  # noqa: E402
    IDENTITY_MANIFEST_FIELDS,
    OBSERVATION_INDEX_FIELDS,
    DeployableObservationLoader,
    IdentityManifestRow,
    RoleIndexRow,
    StorageContractError,
    audit_identity_manifest,
    file_sha256 as payload_sha256,
    read_identity_manifest,
    write_identity_manifest,
    write_role_index,
)
from utils.synthetic_plant import synthetic_privileged_record  # noqa: E402

SCHEMA_PATH = PACKET_ROOT / "schema" / "schema.json"
DRAFT_CONFIG_PATH = PACKET_ROOT / "config" / "draft-config-v0.1.json"


def load_schema() -> dict[str, object]:
    """Load the tracked machine schema as a strict test fixture."""

    return json.loads(SCHEMA_PATH.read_text(encoding="utf-8"))


def tracked_config():
    """Return the validated tracked draft configuration."""

    return load_config(DRAFT_CONFIG_PATH, SCHEMA_PATH)


def manifest_row(
    suite: str,
    run_id: str,
    *,
    pair_id: str = "pair-a",
    split: str = "dev",
    trajectory_spec_id: str = "traj-a",
    fault_setting_id: str = "fault-a",
    split_group_id: str = "group-a",
) -> IdentityManifestRow:
    """Build one valid path-free identity row."""

    config = tracked_config()
    return IdentityManifestRow(
        schema_version=SCHEMA_VERSION,
        config_hash=config.config_hash,
        scenario_spec_id="scenario-a",
        pair_id=pair_id,
        run_id=run_id,
        trajectory_spec_id=trajectory_spec_id,
        fault_setting_id=fault_setting_id,
        split_group_id=split_group_id,
        split=split,
        suite=suite,
        estimator_id="temporal-protocol-a",
        controller_id="controller-protocol-a",
        payload_id="payload-a",
        env_profile_id="env-a",
        contact_profile_id="contact-a",
        sim_seed=1,
        fault_seed=2,
        sensor_seed=3,
        controller_seed=4,
        train_seed=5,
    )


def write_observation_fixture(
    tmp_path: Path,
    *,
    suite: str = "S",
    payload_extra: dict[str, np.ndarray] | None = None,
    mutate_payload=None,
) -> tuple[Path, str]:
    """Persist one indexed observation payload under observations/<suite>."""

    config = tracked_config()
    observed = SensorModel().observe(
        synthetic_privileged_record(n_steps=20),
        suite,
        pair_id="pair-a",
        sensor_seed=3,
        run_id=f"run-{suite}",
        config_hash=config.config_hash,
        split="dev",
    )
    payload = observed.to_npz_dict()
    if mutate_payload is not None:
        mutate_payload(payload)
    if payload_extra:
        payload.update(payload_extra)

    suite_root = tmp_path / "observations" / suite
    suite_root.mkdir(parents=True)
    npz_path = suite_root / f"run-{suite}.npz"
    np.savez(npz_path, **payload)
    write_role_index(
        suite_root / "index.csv",
        [
            RoleIndexRow(
                run_id=f"run-{suite}",
                schema_version=SCHEMA_VERSION,
                config_hash=config.config_hash,
                npz_path=npz_path.name,
                sha256=payload_sha256(npz_path),
                split="dev",
            )
        ],
        observation=True,
    )
    return suite_root, f"run-{suite}"


def test_machine_schema_matches_in_force_python_contract() -> None:
    """The machine authority faithfully renders schema v1.0 plus Amendment A1."""

    schema = load_schema()
    validate_machine_schema(schema)
    plant_fields = schema["roles"]["plant"]["fields"]
    assert plant_fields["contact_state"]["shape"] == ["T", 2]
    assert tuple(plant_fields["contact_state"]["field_order"]) == CONTACT_STATE_FIELDS
    assert plant_fields["safety_flag"]["shape"] == ["T", 7]
    assert tuple(plant_fields["safety_flag"]["field_order"]) == SAFETY_FLAG_FIELDS

    registry = schema["roles"]["observations"]["channel_registry"]
    assert tuple(registry) == CHANNEL_NAMES
    for channel in CHANNEL_NAMES:
        assert registry[channel]["width"] == CHANNEL_WIDTH[channel]
        expected = [suite for suite, names in SUITE_CHANNELS.items() if channel in names]
        assert registry[channel]["available_in"] == expected
    assert tuple(schema["roles"]["identity_manifest"]["fields"]) == IDENTITY_MANIFEST_FIELDS
    trace = EstimatorTrace(suite="S", run_id="run-s")
    trace.append(
        EstimatorOutput(
            step=10,
            decision_time_s=0.02,
            p_class=np.asarray([1.0, 0.0, 0.0, 0.0]),
            unknown_score=0.0,
            abstain_decision=False,
        )
    )
    estimator_fields = schema["roles"]["estimator_outputs"]["fields"]
    assert tuple(estimator_fields) == tuple(trace.stack())
    assert estimator_fields["p_class"]["shape"] == ["N_decisions", 4]
    assert (
        estimator_fields["severity_uncertainty"]["unit"]
        == "config_defined_nonnegative_error_scale"
    )


def test_tracked_draft_is_self_hashed_and_confirmatory_refuses_it() -> None:
    """The tracked draft is valid but cannot authorize a confirmatory operation."""

    config = tracked_config()
    assert config.status == "draft"
    assert config.config_hash.startswith("dev-")
    assert config.document["schema_sha256"] == file_sha256(SCHEMA_PATH)
    assert expected_config_hash(config.document) == config.config_hash
    with pytest.raises(ConfigContractError, match="refuses draft"):
        load_config(DRAFT_CONFIG_PATH, SCHEMA_PATH, require_frozen=True)


def test_canonical_hash_is_key_order_independent_and_tamper_evident() -> None:
    """Canonical JSON ignores mapping order but changes for a semantic edit."""

    document = json.loads(DRAFT_CONFIG_PATH.read_text(encoding="utf-8"))
    reordered = dict(reversed(list(document.items())))
    assert canonical_json_bytes(document) == canonical_json_bytes(reordered)
    assert expected_config_hash(document) == expected_config_hash(reordered)

    tampered = copy.deepcopy(document)
    tampered["values"]["timing"]["window_steps"] = 769
    assert expected_config_hash(tampered) != document["config_hash"]
    with pytest.raises(ConfigContractError, match="config_hash mismatch"):
        validate_config_document(
            tampered,
            source_path=DRAFT_CONFIG_PATH,
            schema=load_schema(),
            schema_path=SCHEMA_PATH,
        )


def test_draft_named_config_json_and_partial_frozen_state_fail_loud(tmp_path: Path) -> None:
    """Neither filename camouflage nor unresolved frozen fields can pass."""

    draft = json.loads(DRAFT_CONFIG_PATH.read_text(encoding="utf-8"))
    with pytest.raises(ConfigContractError, match="must never be named"):
        validate_config_document(
            draft,
            source_path=tmp_path / "config.json",
            schema=load_schema(),
            schema_path=SCHEMA_PATH,
        )

    frozen = copy.deepcopy(draft)
    frozen.update(
        config_version="1.0.0",
        status="frozen",
        confirmatory_payloads_allowed=True,
        decision="APPROVE_CONFIG_FREEZE",
        open_gates=[],
    )
    frozen["config_hash"] = expected_config_hash(frozen)
    with pytest.raises(ConfigContractError, match="unresolved null"):
        validate_config_document(
            frozen,
            source_path=tmp_path / "config.json",
            schema=load_schema(),
            schema_path=SCHEMA_PATH,
        )


def test_complete_frozen_shape_requires_exact_filename_and_non_dev_hash(tmp_path: Path) -> None:
    """A complete frozen-shaped fixture uses the reserved filename and hash form."""

    frozen = json.loads(DRAFT_CONFIG_PATH.read_text(encoding="utf-8"))
    frozen.update(
        config_version="1.0.0",
        status="frozen",
        confirmatory_payloads_allowed=True,
        decision="APPROVE_CONFIG_FREEZE",
        open_gates=[],
    )
    frozen["values"]["scenario_manifest"] = {
        "manifest_sha256": "a" * 64,
        "joint_approval_id": "review-state-a",
    }
    frozen["values"]["models"] = {"temporal_id": "t", "rma_id": "r"}
    frozen["values"]["calibration"] = {"protocol_id": "cal-a"}
    frozen["values"]["controllers"]["protocol_ids"] = ["none", "transparent", "rma", "oracle"]
    frozen["values"]["evaluation"] = {"driver_id": "eval-a", "test_manifest_sha256": "b" * 64}
    frozen["config_hash"] = expected_config_hash(frozen)

    validated = validate_config_document(
        frozen,
        source_path=tmp_path / "config.json",
        schema=load_schema(),
        schema_path=SCHEMA_PATH,
        require_frozen=True,
    )
    assert validated.is_frozen
    assert len(validated.config_hash) == 64
    assert not validated.config_hash.startswith("dev-")


def test_frozen_config_rejects_unapproved_or_development_marked_state(
    tmp_path: Path,
) -> None:
    """A hash-valid file still cannot freeze without approval or with dev ids."""

    frozen = json.loads(DRAFT_CONFIG_PATH.read_text(encoding="utf-8"))
    frozen.update(
        config_version="1.0.0",
        status="frozen",
        confirmatory_payloads_allowed=True,
        open_gates=[],
    )
    frozen["values"]["scenario_manifest"] = {"manifest_sha256": "a" * 64}
    frozen["values"]["models"] = {"temporal_id": "t", "rma_id": "r"}
    frozen["values"]["calibration"] = {"protocol_id": "cal-a"}
    frozen["values"]["controllers"]["protocol_ids"] = ["none", "transparent", "rma", "oracle"]
    frozen["values"]["evaluation"] = {"driver_id": "eval-a"}
    frozen["config_hash"] = expected_config_hash(frozen)
    with pytest.raises(ConfigContractError, match="decision must be"):
        validate_config_document(
            frozen,
            source_path=tmp_path / "config.json",
            schema=load_schema(),
            schema_path=SCHEMA_PATH,
        )

    frozen["decision"] = "APPROVE_CONFIG_FREEZE"
    frozen["values"]["models"]["temporal_id"] = "dev-temporal"
    frozen["config_hash"] = expected_config_hash(frozen)
    with pytest.raises(ConfigContractError, match="development-only"):
        validate_config_document(
            frozen,
            source_path=tmp_path / "config.json",
            schema=load_schema(),
            schema_path=SCHEMA_PATH,
        )


def test_identity_manifest_round_trip_and_complete_pair_audit(tmp_path: Path) -> None:
    """The path-free manifest preserves one matched C1/S whole-rollout pair."""

    rows = [manifest_row("C1", "run-c1"), manifest_row("S", "run-s")]
    path = tmp_path / "manifest.csv"
    write_identity_manifest(path, rows)
    restored = read_identity_manifest(path)
    assert restored == rows
    counts = audit_identity_manifest(
        restored,
        expected_config=tracked_config(),
        require_complete_c1_s_pairs=True,
    )
    assert counts == {"rows": 2, "pairs": 1, "trajectories": 1, "fault_settings": 1}
    assert tuple(next(csv.reader(path.open(encoding="utf-8")))) == IDENTITY_MANIFEST_FIELDS


@pytest.mark.parametrize(
    ("field_name", "message"),
    [
        ("pair_id", "pair_id must map to one split"),
        ("trajectory_spec_id", "trajectory_spec_id must map to one split"),
        ("fault_setting_id", "fault_setting_id must map to one split"),
        ("split_group_id", "split_group_id must map to one split"),
    ],
)
def test_whole_group_split_audits_fail_loud(field_name: str, message: str) -> None:
    """Every schema-A grouping axis maps to exactly one split."""

    first = manifest_row("C1", "run-a", pair_id="pair-a")
    second = manifest_row(
        "C1",
        "run-b",
        pair_id="pair-b",
        trajectory_spec_id="traj-b",
        fault_setting_id="fault-b",
        split_group_id="group-b",
    )
    if field_name == "pair_id":
        second = replace(second, pair_id=first.pair_id)
    elif field_name == "trajectory_spec_id":
        second = replace(second, trajectory_spec_id=first.trajectory_spec_id)
    elif field_name == "fault_setting_id":
        second = replace(second, fault_setting_id=first.fault_setting_id)
    else:
        second = replace(second, split_group_id=first.split_group_id)
    second = replace(second, split="val")
    with pytest.raises(StorageContractError, match=message):
        audit_identity_manifest([first, second])


def test_manifest_rejects_time_divided_run_and_pair_seed_or_protocol_mismatch() -> None:
    """Run duplication and within-pair CRN/protocol divergence are build failures."""

    c1 = manifest_row("C1", "run-c1")
    duplicate = replace(c1, suite="S")
    with pytest.raises(StorageContractError, match="appears more than once"):
        audit_identity_manifest([c1, duplicate])

    for changed in (
        replace(manifest_row("S", "run-s"), sensor_seed=999),
        replace(manifest_row("S", "run-s"), estimator_id="other-estimator"),
        replace(manifest_row("S", "run-s"), controller_id="other-controller"),
    ):
        with pytest.raises(StorageContractError, match="must share"):
            audit_identity_manifest([c1, changed])

    mixed_config = replace(manifest_row("S", "run-s"), config_hash="f" * 64)
    with pytest.raises(StorageContractError, match="exactly one config_hash"):
        audit_identity_manifest([c1, mixed_config])


def test_deployable_loader_reads_one_exact_suite_and_audits_all(tmp_path: Path) -> None:
    """A valid one-suite root round-trips through the strict deployable loader."""

    suite_root, run_id = write_observation_fixture(tmp_path, suite="S")
    loader = DeployableObservationLoader(suite_root, "S", tracked_config())
    assert loader.suite == "S"
    assert loader.run_ids == (run_id,)
    loaded = loader.load(run_id)
    assert loaded.suite == "S"
    assert loaded.available_channels == SUITE_CHANNELS["S"]
    assert loader.audit_all() == {"dev": 1, "pilot": 0, "val": 0, "test": 0}
    with pytest.raises(ConfigContractError, match="refuses a draft"):
        DeployableObservationLoader(
            suite_root,
            "S",
            tracked_config(),
            require_frozen=True,
        )


def test_loader_rejects_identity_column_or_shared_parent_root(tmp_path: Path) -> None:
    """Deployable indexes cannot expose provenance or resolve a sibling suite."""

    suite_root, _ = write_observation_fixture(tmp_path, suite="C1")
    index_path = suite_root / "index.csv"
    rows = list(csv.DictReader(index_path.open(encoding="utf-8")))
    with index_path.open("w", newline="", encoding="utf-8") as handle:
        fields_out = OBSERVATION_INDEX_FIELDS + ("fault_setting_id",)
        writer = csv.DictWriter(handle, fieldnames=fields_out)
        writer.writeheader()
        writer.writerow({**rows[0], "fault_setting_id": "secret-target"})
    with pytest.raises(StorageContractError, match="header must be exactly"):
        DeployableObservationLoader(suite_root, "C1", tracked_config())

    with pytest.raises(StorageContractError, match="exactly observations"):
        DeployableObservationLoader(tmp_path / "observations", "C1", tracked_config())


def test_loader_rejects_privileged_or_label_field_inside_observation_payload(
    tmp_path: Path,
) -> None:
    """An extra target/provenance/privileged NPZ field fails the exact allowlist."""

    suite_root, run_id = write_observation_fixture(
        tmp_path,
        suite="S",
        payload_extra={"fault_setting_id": np.asarray("secret-target")},
    )
    loader = DeployableObservationLoader(suite_root, "S", tracked_config())
    with pytest.raises(StorageContractError, match="forbidden=.*fault_setting_id"):
        loader.load(run_id)


def test_loader_rejects_unavailable_channel_value_or_mask_leak(tmp_path: Path) -> None:
    """A C1 payload cannot hide an S gauge value behind its static mask."""

    def leak_gauge(payload: dict[str, np.ndarray]) -> None:
        payload["values__gauge_obs"] = payload["values__gauge_obs"].copy()
        payload["valid__gauge_obs"] = payload["valid__gauge_obs"].copy()
        payload["values__gauge_obs"][0, 0] = 123.0
        payload["valid__gauge_obs"][0, 0] = True

    suite_root, run_id = write_observation_fixture(
        tmp_path,
        suite="C1",
        mutate_payload=leak_gauge,
    )
    loader = DeployableObservationLoader(suite_root, "C1", tracked_config())
    with pytest.raises(StorageContractError, match="unavailable channel gauge_obs"):
        loader.load(run_id)


def test_loader_rejects_schema_dtype_drift(tmp_path: Path) -> None:
    """A numerically readable float32 channel cannot violate schema float64."""

    def narrow_dtype(payload: dict[str, np.ndarray]) -> None:
        payload["values__q_obs"] = payload["values__q_obs"].astype(np.float32)

    suite_root, run_id = write_observation_fixture(
        tmp_path,
        suite="S",
        mutate_payload=narrow_dtype,
    )
    loader = DeployableObservationLoader(suite_root, "S", tracked_config())
    with pytest.raises(StorageContractError, match="values must be float64"):
        loader.load(run_id)


def test_loader_rejects_hash_mismatch_and_role_path_traversal(tmp_path: Path) -> None:
    """Payload tampering and paths outside the role root fail before loading."""

    suite_root, run_id = write_observation_fixture(tmp_path, suite="S")
    payload = suite_root / f"{run_id}.npz"
    payload.write_bytes(payload.read_bytes() + b"tamper")
    loader = DeployableObservationLoader(suite_root, "S", tracked_config())
    with pytest.raises(StorageContractError, match="SHA-256 mismatch"):
        loader.load(run_id)

    index_path = suite_root / "index.csv"
    row = list(csv.DictReader(index_path.open(encoding="utf-8")))[0]
    row["npz_path"] = "../labels/secret.npz"
    with index_path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=OBSERVATION_INDEX_FIELDS)
        writer.writeheader()
        writer.writerow(row)
    with pytest.raises(StorageContractError, match="without traversal"):
        DeployableObservationLoader(suite_root, "S", tracked_config())
