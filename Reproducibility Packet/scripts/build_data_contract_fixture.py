"""Build and audit a small role-complete development/validation storage fixture.

This is a contract fixture, not a Gate-3 assignment and not research data.  It
exercises the same manifest, role roots, indexes, label join, hashes, and draft
``test`` refusal that the eventual multi-setting generator must use.
"""

from __future__ import annotations

import argparse
import json
from dataclasses import asdict
from pathlib import Path

import numpy as np

from utils.config_contract import load_config
from utils.estimator import EstimatorOutput
from utils.role_contract import (
    DatasetRoleBuilder,
    RolePayloadLoader,
    SupervisedTrainingJoin,
)
from utils.schema_types import FaultSpec
from utils.sensor_model import SensorConfig, SensorModel
from utils.storage_contract import (
    DeployableObservationLoader,
    IdentityManifestRow,
)
from utils.synthetic_plant import synthetic_privileged_record


def parse_args() -> argparse.Namespace:
    """Parse portable fixture inputs and output root."""

    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--schema",
        type=Path,
        default=Path("schema/schema.json"),
        help="Machine-readable schema authority.",
    )
    parser.add_argument(
        "--config",
        type=Path,
        default=Path("config/draft-config-v0.1.json"),
        help="Lifecycle-validated draft or frozen config.",
    )
    parser.add_argument(
        "--output-root",
        type=Path,
        default=Path("results/data_contract_fixture"),
        help="Fresh output directory for the fixture.",
    )
    parser.add_argument("--n-steps", type=int, default=96)
    return parser.parse_args()


def fixture_manifest(config_hash: str) -> list[IdentityManifestRow]:
    """Return two C1/S pairs on disjoint dev/val trajectory/fault groups."""

    rows: list[IdentityManifestRow] = []
    specs = (
        ("fixture_dev", "dev", "healthy_none", 101),
        ("fixture_val", "val", "structure_local", 202),
    )
    for pair_id, split, fault_setting_id, seed in specs:
        for suite in ("C1", "S"):
            rows.append(
                IdentityManifestRow(
                    schema_version="1.0",
                    config_hash=config_hash,
                    scenario_spec_id=f"scenario_{split}",
                    pair_id=pair_id,
                    run_id=f"{pair_id}_{suite}",
                    trajectory_spec_id=f"trajectory_{split}",
                    fault_setting_id=fault_setting_id,
                    split_group_id=f"group_{split}",
                    split=split,
                    suite=suite,
                    estimator_id="fixture_estimator_v1",
                    controller_id="fixture_controller_v1",
                    payload_id=f"payload_{pair_id}",
                    env_profile_id="fixture_env",
                    contact_profile_id="no_contact",
                    sim_seed=seed,
                    fault_seed=seed + 1,
                    sensor_seed=seed + 2,
                    controller_seed=seed + 3,
                    train_seed=0,
                )
            )
    return rows


def _fault_for(row: IdentityManifestRow, onset_index: int) -> FaultSpec:
    """Map the fixture's explicit fault-setting ids to one shared fault spec."""

    if row.fault_setting_id == "healthy_none":
        return FaultSpec(onset_index=onset_index)
    if row.fault_setting_id == "structure_local":
        return FaultSpec(
            source_class="structure",
            subtype="link_stiffness_loss",
            location=2,
            severity=0.5,
            onset_index=onset_index,
        )
    raise ValueError(f"unhandled fixture fault setting: {row.fault_setting_id}")


def _label_payload(fault: FaultSpec, f_ctrl_hz: float) -> dict[str, np.ndarray]:
    """Render one exact schema label payload."""

    return {
        "source_class": np.asarray(fault.source_class),
        "subtype": np.asarray(fault.subtype),
        "location": np.asarray(fault.location, dtype=np.int64),
        "severity": np.asarray(fault.severity, dtype=np.float64),
        "onset_index": np.asarray(fault.onset_index, dtype=np.int64),
        "onset_time_s": np.asarray(fault.onset_index / f_ctrl_hz, dtype=np.float64),
        "compound_flag": np.asarray(fault.compound_flag, dtype=np.bool_),
        "ood_flag": np.asarray(fault.ood_flag, dtype=np.bool_),
    }


def _estimator_payload(
    source_class: str,
    step: int,
    decision_time_s: float,
) -> dict[str, np.ndarray]:
    """Render one schema-valid fixture decision without claiming model output."""

    order = ("healthy", "structure", "actuator", "sensor")
    probs = np.zeros((1, 4), dtype=np.float64)
    probs[0, order.index(source_class)] = 1.0
    detection = np.nan if source_class == "healthy" else decision_time_s
    return {
        "step": np.asarray([step], dtype=np.int64),
        "decision_time_s": np.asarray([decision_time_s], dtype=np.float64),
        "p_class": probs,
        "unknown_score": np.asarray([0.0], dtype=np.float64),
        "abstain_decision": np.asarray([False], dtype=np.bool_),
        "location_out": np.asarray([-1], dtype=np.int64),
        "severity_out": np.asarray([0.0], dtype=np.float64),
        "severity_uncertainty": np.asarray([np.inf], dtype=np.float64),
        "detection_time_s": np.asarray([detection], dtype=np.float64),
    }


def _controller_payload(record: object) -> dict[str, np.ndarray]:
    """Render an inert role-complete controller log from the fixture plant trace."""

    n_steps = int(record.n_steps)
    return {
        "step": np.asarray(record.step, dtype=np.int64),
        "t_s": np.asarray(record.t_s, dtype=np.float64),
        "applied_action": np.asarray(record.control_effort, dtype=np.float64),
        "controller_mode": np.full(n_steps, "fixture_nominal", dtype="U15"),
        "gain_schedule": np.ones((n_steps, 2), dtype=np.float64),
        "reconfiguration_event": np.zeros(n_steps, dtype=np.bool_),
    }


def build_fixture(
    schema_path: Path,
    config_path: Path,
    output_root: Path,
    n_steps: int,
) -> dict[str, object]:
    """Build every role, publish indexes, and re-open them through safe loaders."""

    if n_steps < 32:
        raise ValueError("n_steps must be at least 32")
    if output_root.exists():
        raise FileExistsError(f"output root already exists: {output_root}")
    config = load_config(config_path, schema_path)
    schema = json.loads(schema_path.read_text(encoding="utf-8"))
    rows = fixture_manifest(config.config_hash)
    builder = DatasetRoleBuilder(output_root, rows, schema, config)
    builder.publish_manifest()

    plant_writer = builder.make_writer("plant")
    label_writer = builder.make_writer("labels")
    observation_writers = {
        suite: builder.make_observation_writer(suite) for suite in ("C1", "S")
    }
    estimator_writers = {
        suite: builder.make_writer("estimator_outputs", suite=suite)
        for suite in ("C1", "S")
    }
    controller_writers = {
        suite: builder.make_writer("controller_logs", suite=suite)
        for suite in ("C1", "S")
    }

    sensor_config = SensorConfig(**config.document["values"]["sensor_model"])
    sensor_model = SensorModel(sensor_config)
    f_ctrl_hz = float(config.document["values"]["timing"]["f_ctrl_hz"])
    n_def = int(config.document["values"]["plant"]["n_def"])
    onset_index = n_steps // 3

    pair_records: dict[str, object] = {}
    for row in rows:
        fault = _fault_for(row, onset_index)
        if row.pair_id not in pair_records:
            pair_records[row.pair_id] = synthetic_privileged_record(
                n_steps=n_steps,
                f_ctrl=f_ctrl_hz,
                n_def=n_def,
                seed=row.sim_seed,
                fault=fault,
            )
        record = pair_records[row.pair_id]
        plant_writer.write(row.run_id, record.__dict__)
        label_writer.write(row.run_id, _label_payload(fault, f_ctrl_hz))
        observed = sensor_model.observe(
            record,
            row.suite,
            pair_id=row.pair_id,
            sensor_seed=row.sensor_seed,
            fault=fault,
            run_id=row.run_id,
            config_hash=config.config_hash,
            split=row.split,
        )
        observation_writers[row.suite].write(observed)
        estimator_writers[row.suite].write(
            row.run_id,
            _estimator_payload(
                fault.source_class,
                n_steps - 1,
                float(record.t_s[-1]),
            ),
        )
        controller_writers[row.suite].write(row.run_id, _controller_payload(record))

    plant_writer.publish_index()
    label_writer.publish_index()
    for writers in (observation_writers, estimator_writers, controller_writers):
        for writer in writers.values():
            writer.publish_index()

    role_counts = {
        "plant": RolePayloadLoader(
            output_root / "plant", "plant", schema, config
        ).audit_all(),
        "labels": RolePayloadLoader(
            output_root / "labels", "labels", schema, config
        ).audit_all(),
    }
    joined_counts: dict[str, dict[str, int]] = {}
    label_loader = RolePayloadLoader(output_root / "labels", "labels", schema, config)
    for suite in ("C1", "S"):
        observations = DeployableObservationLoader(
            output_root / "observations" / suite,
            suite,
            config,
        )
        observation_counts = observations.audit_all()
        estimator_count = RolePayloadLoader(
            output_root / "estimator_outputs" / suite,
            "estimator_outputs",
            schema,
            config,
            suite=suite,
        ).audit_all()
        controller_count = RolePayloadLoader(
            output_root / "controller_logs" / suite,
            "controller_logs",
            schema,
            config,
            suite=suite,
        ).audit_all()
        join = SupervisedTrainingJoin(observations, label_loader, rows)
        joined_counts[suite] = {
            "dev": len(list(join.examples("dev"))),
            "val": len(list(join.examples("val"))),
            "observations": sum(observation_counts.values()),
            "estimator_outputs": estimator_count,
            "controller_logs": controller_count,
        }

    summary: dict[str, object] = {
        "status": "development_contract_fixture_only",
        "config_hash": config.config_hash,
        "confirmatory": False,
        "manifest_rows": len(rows),
        "pairs": len({row.pair_id for row in rows}),
        "role_counts": role_counts,
        "supervised_join_counts": joined_counts,
        "test_payloads": 0,
        "evidence_boundary": (
            "Synthetic role-completeness fixture only; not a Gate-3 assignment, "
            "model fit, validation result, or confirmatory dataset."
        ),
    }
    (output_root / "build_summary.json").write_text(
        json.dumps(summary, indent=2, sort_keys=True, allow_nan=False) + "\n",
        encoding="utf-8",
    )
    return summary


def main() -> int:
    """Build the fixture and print its role-completeness summary."""

    args = parse_args()
    summary = build_fixture(args.schema, args.config, args.output_root, args.n_steps)
    print(json.dumps(summary, indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
