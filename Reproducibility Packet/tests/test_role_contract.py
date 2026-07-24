"""Adversarial tests for role writers and the allowlisted supervised join."""

from __future__ import annotations

import json
import sys
from dataclasses import replace
from pathlib import Path

import numpy as np
import pytest

PACKET_ROOT = Path(__file__).resolve().parents[1]
SCRIPTS_ROOT = PACKET_ROOT / "scripts"
sys.path.insert(0, str(SCRIPTS_ROOT))

from build_data_contract_fixture import build_fixture, fixture_manifest  # noqa: E402
from utils.config_contract import ConfigContractError, load_config  # noqa: E402
from utils.role_contract import (  # noqa: E402
    DatasetRoleBuilder,
    RolePayloadLoader,
    RolePayloadWriter,
    StorageContractError,
    SupervisedTrainingJoin,
    validate_role_payload,
)
from utils.storage_contract import DeployableObservationLoader  # noqa: E402

SCHEMA_PATH = PACKET_ROOT / "schema" / "schema.json"
CONFIG_PATH = PACKET_ROOT / "config" / "draft-config-v0.1.json"


def schema() -> dict[str, object]:
    """Return the tracked machine schema."""

    return json.loads(SCHEMA_PATH.read_text(encoding="utf-8"))


def config():
    """Return the lifecycle-validated tracked draft."""

    return load_config(CONFIG_PATH, SCHEMA_PATH)


@pytest.fixture(scope="module")
def complete_fixture(tmp_path_factory: pytest.TempPathFactory) -> Path:
    """Build one reusable role-complete fixture."""

    root = tmp_path_factory.mktemp("role-contract") / "dataset"
    build_fixture(SCHEMA_PATH, CONFIG_PATH, root, 48)
    return root


def valid_label() -> dict[str, np.ndarray]:
    """Return one exact scalar label payload."""

    return {
        "source_class": np.asarray("structure"),
        "subtype": np.asarray("link_stiffness_loss"),
        "location": np.asarray(2, dtype=np.int64),
        "severity": np.asarray(0.5, dtype=np.float64),
        "onset_index": np.asarray(16, dtype=np.int64),
        "onset_time_s": np.asarray(0.032, dtype=np.float64),
        "compound_flag": np.asarray(False, dtype=np.bool_),
        "ood_flag": np.asarray(False, dtype=np.bool_),
    }


def test_end_to_end_fixture_writes_every_role_without_test_payload(
    complete_fixture: Path,
) -> None:
    summary = json.loads((complete_fixture / "build_summary.json").read_text(encoding="utf-8"))
    assert summary["manifest_rows"] == 4
    assert summary["pairs"] == 2
    assert summary["test_payloads"] == 0
    assert summary["role_counts"] == {"labels": 4, "plant": 4}
    for suite in ("C1", "S"):
        assert summary["supervised_join_counts"][suite] == {
            "controller_logs": 2,
            "dev": 1,
            "estimator_outputs": 2,
            "observations": 2,
            "val": 1,
        }
        assert (complete_fixture / "observations" / suite / "index.csv").is_file()
        assert (complete_fixture / "estimator_outputs" / suite / "index.csv").is_file()
        assert (complete_fixture / "controller_logs" / suite / "index.csv").is_file()


def test_supervised_join_exposes_only_observation_and_exact_label_target(
    complete_fixture: Path,
) -> None:
    cfg = config()
    rows = fixture_manifest(cfg.config_hash)
    labels = RolePayloadLoader(complete_fixture / "labels", "labels", schema(), cfg)
    observations = DeployableObservationLoader(
        complete_fixture / "observations" / "S", "S", cfg
    )
    join = SupervisedTrainingJoin(observations, labels, rows)
    example = next(join.examples("val"))
    assert set(example.target) == {
        "source_class",
        "subtype",
        "location",
        "severity",
        "onset_index",
        "onset_time_s",
        "compound_flag",
        "ood_flag",
    }
    assert not hasattr(example, "manifest")
    assert not hasattr(example, "plant")
    assert example.observation.suite == "S"
    assert example.target["source_class"] == "structure"


def test_draft_config_refuses_any_test_assignment(tmp_path: Path) -> None:
    cfg = config()
    rows = fixture_manifest(cfg.config_hash)
    rows = [
        replace(row, split="test", split_group_id="group_test")
        if row.pair_id == "fixture_dev"
        else row
        for row in rows
    ]
    with pytest.raises(ConfigContractError, match="cannot materialize test"):
        DatasetRoleBuilder(tmp_path / "dataset", rows, schema(), cfg)


def test_training_join_cannot_allowlist_test(complete_fixture: Path) -> None:
    cfg = config()
    rows = fixture_manifest(cfg.config_hash)
    labels = RolePayloadLoader(complete_fixture / "labels", "labels", schema(), cfg)
    observations = DeployableObservationLoader(
        complete_fixture / "observations" / "C1", "C1", cfg
    )
    with pytest.raises(StorageContractError, match="training splits"):
        SupervisedTrainingJoin(observations, labels, rows, allowed_splits=("test",))


@pytest.mark.parametrize(
    ("mutation", "message"),
    [
        (lambda payload: {**payload, "fault_setting_id": np.asarray("leak")}, "key allowlist"),
        (
            lambda payload: {**payload, "severity": np.asarray(0.5, dtype=np.float32)},
            "dtype",
        ),
        (
            lambda payload: {**payload, "source_class": np.asarray("oracle")},
            "source_class",
        ),
    ],
)
def test_label_writer_rejects_extra_identity_dtype_drift_and_bad_class(
    mutation, message: str
) -> None:
    with pytest.raises(StorageContractError, match=message):
        validate_role_payload("labels", mutation(valid_label()), schema(), config())


def test_role_writer_rejects_unassigned_run_and_wrong_suite_root(tmp_path: Path) -> None:
    cfg = config()
    rows = fixture_manifest(cfg.config_hash)
    assigned = {row.run_id: row for row in rows}
    writer = RolePayloadWriter(
        tmp_path / "labels",
        "labels",
        schema(),
        cfg,
        assigned_rows=assigned,
    )
    with pytest.raises(StorageContractError, match="not assigned"):
        writer.write("forged_run", valid_label())
    with pytest.raises(StorageContractError, match="must be exactly"):
        RolePayloadWriter(
            tmp_path / "wrong" / "C1",
            "estimator_outputs",
            schema(),
            cfg,
            suite="C1",
        )


def test_role_loader_detects_payload_hash_tamper(tmp_path: Path) -> None:
    root = tmp_path / "dataset"
    build_fixture(SCHEMA_PATH, CONFIG_PATH, root, 48)
    cfg = config()
    loader = RolePayloadLoader(root / "labels", "labels", schema(), cfg)
    run_id = loader.run_ids[0]
    payload = root / "labels" / f"{run_id}.npz"
    payload.write_bytes(payload.read_bytes() + b"tamper")
    with pytest.raises(StorageContractError, match="SHA-256 mismatch"):
        loader.load(run_id)


def test_estimator_role_rejects_invalid_probability_simplex() -> None:
    payload = {
        "step": np.asarray([0], dtype=np.int64),
        "decision_time_s": np.asarray([0.0], dtype=np.float64),
        "p_class": np.asarray([[0.8, 0.8, 0.0, 0.0]], dtype=np.float64),
        "unknown_score": np.asarray([0.0], dtype=np.float64),
        "abstain_decision": np.asarray([False], dtype=np.bool_),
        "location_out": np.asarray([-1], dtype=np.int64),
        "severity_out": np.asarray([0.0], dtype=np.float64),
        "severity_uncertainty": np.asarray([np.inf], dtype=np.float64),
        "detection_time_s": np.asarray([np.nan], dtype=np.float64),
    }
    with pytest.raises(StorageContractError, match="sum to 1"):
        validate_role_payload("estimator_outputs", payload, schema(), config())


def test_controller_role_rejects_noncontiguous_grid() -> None:
    payload = {
        "step": np.asarray([0, 2], dtype=np.int64),
        "t_s": np.asarray([0.0, 0.004], dtype=np.float64),
        "applied_action": np.zeros((2, 2), dtype=np.float64),
        "controller_mode": np.asarray(["nominal", "nominal"]),
        "gain_schedule": np.ones((2, 2), dtype=np.float64),
        "reconfiguration_event": np.zeros(2, dtype=np.bool_),
    }
    with pytest.raises(StorageContractError, match="contiguous"):
        validate_role_payload("controller_logs", payload, schema(), config())
