"""Role-separated storage, manifest, loader, and audit foundation (schema A/D/E).

This module intentionally stops before the Gate-3 experimental design. It can
write/read and audit a path-free identity manifest, validate role indexes, and
load exactly one deployable observation suite. It cannot see privileged, label,
identity, or other-suite roots through the deployable loader interface.
"""

from __future__ import annotations

import csv
import hashlib
from dataclasses import asdict, dataclass, fields
from pathlib import Path
from typing import Iterable, Mapping

import numpy as np

from .config_contract import ConfigContractError, ValidatedConfig
from .schema_types import (
    CHANNEL_NAMES,
    CHANNEL_WIDTH,
    DEPLOYABLE_SUITES,
    SCHEMA_VERSION,
    SUITE_CHANNELS,
    ObservedRecord,
)

SPLITS = ("dev", "pilot", "val", "test")
ALL_SUITES = ("C0", "C1", "S", "O")
ROLE_INDEX_FIELDS = ("run_id", "schema_version", "config_hash", "npz_path", "sha256")
OBSERVATION_INDEX_FIELDS = ROLE_INDEX_FIELDS + ("split",)


class StorageContractError(ValueError):
    """Raised when role separation, pairing, paths, hashes, or payloads are unsafe."""


@dataclass(frozen=True)
class IdentityManifestRow:
    """One path-free schema-A rollout identity row."""

    schema_version: str
    config_hash: str
    scenario_spec_id: str
    pair_id: str
    run_id: str
    trajectory_spec_id: str
    fault_setting_id: str
    split_group_id: str
    split: str
    suite: str
    estimator_id: str
    controller_id: str
    payload_id: str
    env_profile_id: str
    contact_profile_id: str
    sim_seed: int
    fault_seed: int
    sensor_seed: int
    controller_seed: int
    train_seed: int


IDENTITY_MANIFEST_FIELDS = tuple(field.name for field in fields(IdentityManifestRow))


@dataclass(frozen=True)
class RoleIndexRow:
    """One schema-E payload-index row; observations additionally carry split."""

    run_id: str
    schema_version: str
    config_hash: str
    npz_path: str
    sha256: str
    split: str | None = None


def file_sha256(path: Path) -> str:
    """Return one payload's lowercase SHA-256 digest."""

    return hashlib.sha256(Path(path).read_bytes()).hexdigest()


def _strict_header(reader: csv.DictReader, expected: tuple[str, ...], path: Path) -> None:
    """Require a CSV header to expose exactly the allowlisted fields and order."""

    actual = tuple(reader.fieldnames or ())
    if actual != expected:
        raise StorageContractError(
            f"{path} header must be exactly {expected}; got {actual}"
        )


def _opaque_id(value: str, field_name: str) -> str:
    """Validate a nonempty path-free opaque identifier."""

    text = str(value)
    if not text or "/" in text or "\\" in text or text in {".", ".."}:
        raise StorageContractError(f"{field_name} must be a nonempty path-free opaque id")
    return text


def _valid_config_hash(value: str) -> bool:
    """Return whether a hash is either lifecycle-valid draft or frozen form."""

    text = str(value)
    if text.startswith("dev-"):
        text = text[4:]
    return re_full_sha256(text)


def write_identity_manifest(path: Path, rows: Iterable[IdentityManifestRow]) -> None:
    """Write a complete path-free identity manifest after auditing it."""

    materialized = list(rows)
    audit_identity_manifest(materialized)
    path = Path(path)
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=IDENTITY_MANIFEST_FIELDS)
        writer.writeheader()
        for row in materialized:
            writer.writerow(asdict(row))


def read_identity_manifest(path: Path) -> list[IdentityManifestRow]:
    """Read and type one exact schema-A identity manifest."""

    path = Path(path)
    with path.open("r", newline="", encoding="utf-8") as handle:
        reader = csv.DictReader(handle)
        _strict_header(reader, IDENTITY_MANIFEST_FIELDS, path)
        rows: list[IdentityManifestRow] = []
        for raw in reader:
            try:
                typed = {
                    **raw,
                    **{
                        name: int(raw[name])
                        for name in (
                            "sim_seed",
                            "fault_seed",
                            "sensor_seed",
                            "controller_seed",
                            "train_seed",
                        )
                    },
                }
                rows.append(IdentityManifestRow(**typed))
            except (TypeError, ValueError) as exc:
                raise StorageContractError(f"invalid identity row in {path}: {raw}") from exc
    audit_identity_manifest(rows)
    return rows


def _assert_one_mapping(
    rows: Iterable[IdentityManifestRow], key_name: str, value_name: str
) -> None:
    """Require every key to map to exactly one value."""

    mapping: dict[str, set[str]] = {}
    for row in rows:
        mapping.setdefault(str(getattr(row, key_name)), set()).add(
            str(getattr(row, value_name))
        )
    broken = {key: sorted(values) for key, values in mapping.items() if len(values) != 1}
    if broken:
        raise StorageContractError(
            f"{key_name} must map to one {value_name}; conflicts: {broken}"
        )


def audit_identity_manifest(
    rows: Iterable[IdentityManifestRow],
    *,
    expected_config: ValidatedConfig | None = None,
    require_complete_c1_s_pairs: bool = False,
) -> dict[str, int]:
    """Enforce schema-A whole-group splits, pairing, and CRN invariants."""

    materialized = list(rows)
    if not materialized:
        raise StorageContractError("identity manifest must contain at least one rollout")

    run_ids: set[str] = set()
    config_hashes: set[str] = set()
    for row in materialized:
        for name in (
            "scenario_spec_id",
            "pair_id",
            "run_id",
            "trajectory_spec_id",
            "fault_setting_id",
            "split_group_id",
            "estimator_id",
            "controller_id",
            "payload_id",
            "env_profile_id",
            "contact_profile_id",
        ):
            _opaque_id(getattr(row, name), name)
        if row.run_id in run_ids:
            raise StorageContractError(
                f"run_id {row.run_id!r} appears more than once; rollouts cannot be split by time"
            )
        run_ids.add(row.run_id)
        if row.schema_version != SCHEMA_VERSION:
            raise StorageContractError(
                f"run {row.run_id} schema_version {row.schema_version!r} != {SCHEMA_VERSION!r}"
            )
        if not _valid_config_hash(row.config_hash):
            raise StorageContractError(f"run {row.run_id} has an invalid config_hash")
        config_hashes.add(row.config_hash)
        if row.split not in SPLITS:
            raise StorageContractError(f"run {row.run_id} has invalid split {row.split!r}")
        if row.suite not in ALL_SUITES:
            raise StorageContractError(f"run {row.run_id} has invalid suite {row.suite!r}")
        for seed_name in (
            "sim_seed",
            "fault_seed",
            "sensor_seed",
            "controller_seed",
            "train_seed",
        ):
            if int(getattr(row, seed_name)) < 0:
                raise StorageContractError(f"{seed_name} must be non-negative")
        if expected_config is not None and row.config_hash != expected_config.config_hash:
            raise StorageContractError(
                f"run {row.run_id} config_hash does not match validated config"
            )
    if len(config_hashes) != 1:
        raise StorageContractError(
            f"identity manifest must use exactly one config_hash; got {sorted(config_hashes)}"
        )

    for key in ("pair_id", "trajectory_spec_id", "fault_setting_id", "split_group_id"):
        _assert_one_mapping(materialized, key, "split")

    pairs: dict[str, list[IdentityManifestRow]] = {}
    for row in materialized:
        pairs.setdefault(row.pair_id, []).append(row)
    for pair_id, pair_rows in pairs.items():
        suites = [row.suite for row in pair_rows]
        if len(suites) != len(set(suites)):
            raise StorageContractError(f"pair {pair_id} contains duplicate suite rows")
        for field_name in (
            "scenario_spec_id",
            "trajectory_spec_id",
            "fault_setting_id",
            "split_group_id",
            "split",
            "sim_seed",
            "fault_seed",
            "sensor_seed",
            "controller_seed",
            "train_seed",
            "estimator_id",
            "controller_id",
            "payload_id",
            "env_profile_id",
            "contact_profile_id",
        ):
            values = {getattr(row, field_name) for row in pair_rows}
            if len(values) != 1:
                raise StorageContractError(
                    f"pair {pair_id} must share {field_name}; got {sorted(values, key=str)}"
                )
        if require_complete_c1_s_pairs and not {"C1", "S"}.issubset(set(suites)):
            raise StorageContractError(f"pair {pair_id} is missing a matched C1 or S rollout")

    return {
        "rows": len(materialized),
        "pairs": len(pairs),
        "trajectories": len({row.trajectory_spec_id for row in materialized}),
        "fault_settings": len({row.fault_setting_id for row in materialized}),
    }


def write_role_index(
    path: Path, rows: Iterable[RoleIndexRow], *, observation: bool
) -> None:
    """Write one exact schema-E role index."""

    materialized = list(rows)
    _validate_role_index_rows(materialized, observation=observation)
    path = Path(path)
    path.parent.mkdir(parents=True, exist_ok=True)
    fields_out = OBSERVATION_INDEX_FIELDS if observation else ROLE_INDEX_FIELDS
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=fields_out)
        writer.writeheader()
        for row in materialized:
            raw = asdict(row)
            if not observation:
                raw.pop("split")
            else:
                raw["split"] = row.split or ""
            writer.writerow(raw)


def read_role_index(path: Path, *, observation: bool) -> list[RoleIndexRow]:
    """Read one exact role index without accepting provenance columns."""

    path = Path(path)
    expected = OBSERVATION_INDEX_FIELDS if observation else ROLE_INDEX_FIELDS
    with path.open("r", newline="", encoding="utf-8") as handle:
        reader = csv.DictReader(handle)
        _strict_header(reader, expected, path)
        rows = [
            RoleIndexRow(
                run_id=row["run_id"],
                schema_version=row["schema_version"],
                config_hash=row["config_hash"],
                npz_path=row["npz_path"],
                sha256=row["sha256"],
                split=row.get("split") or None,
            )
            for row in reader
        ]
    _validate_role_index_rows(rows, observation=observation)
    return rows


def _validate_role_index_rows(rows: list[RoleIndexRow], *, observation: bool) -> None:
    """Validate role-index identities, hashes, relative paths, and split fields."""

    if not rows:
        raise StorageContractError("role index must contain at least one payload")
    seen: set[str] = set()
    for row in rows:
        _opaque_id(row.run_id, "run_id")
        if row.run_id in seen:
            raise StorageContractError(f"duplicate run_id in role index: {row.run_id}")
        seen.add(row.run_id)
        if row.schema_version != SCHEMA_VERSION:
            raise StorageContractError("role index schema_version mismatch")
        candidate = Path(row.npz_path)
        if (
            candidate.is_absolute()
            or candidate.drive
            or ".." in candidate.parts
            or candidate.suffix != ".npz"
        ):
            raise StorageContractError(
                f"role payload path must be relative .npz without traversal: {row.npz_path}"
            )
        if len(candidate.parts) != 1:
            raise StorageContractError("role payload path must be relative to its own role root")
        if not re_full_sha256(row.sha256):
            raise StorageContractError(f"invalid payload sha256 for run {row.run_id}")
        if not _valid_config_hash(row.config_hash):
            raise StorageContractError(f"invalid config_hash for run {row.run_id}")
        if observation:
            if row.split not in SPLITS:
                raise StorageContractError(
                    f"observation index row {row.run_id} needs a safe split assignment"
                )
        elif row.split is not None:
            raise StorageContractError("non-observation indexes must not carry split")


def re_full_sha256(value: str) -> bool:
    """Return whether a value is one lowercase SHA-256 hex digest."""

    return len(value) == 64 and all(char in "0123456789abcdef" for char in value)


def _expected_observation_keys() -> set[str]:
    """Return the exact allowlist for one ObservedRecord NPZ payload."""

    keys = {
        "schema_version",
        "suite",
        "run_id",
        "pair_id",
        "config_hash",
        "split",
        "channel_names",
        "suite_available_mask",
    }
    for name in CHANNEL_NAMES:
        keys.update(
            {
                f"values__{name}",
                f"valid__{name}",
                f"meas_time__{name}",
                f"avail_time__{name}",
                f"latency__{name}",
            }
        )
    return keys


def _validate_observed_record(
    record: ObservedRecord,
    *,
    suite: str,
    row: RoleIndexRow,
) -> None:
    """Enforce suite masks, NaN missingness, timing, and index/payload identity."""

    if record.schema_version != row.schema_version or record.schema_version != SCHEMA_VERSION:
        raise StorageContractError("observation payload schema_version mismatch")
    if record.suite != suite:
        raise StorageContractError("observation payload suite mismatch")
    if record.run_id != row.run_id:
        raise StorageContractError("observation payload run_id mismatch")
    if record.config_hash != row.config_hash:
        raise StorageContractError("observation payload config_hash mismatch")
    if record.split != row.split:
        raise StorageContractError("observation payload split mismatch")
    if tuple(record.values) != CHANNEL_NAMES:
        raise StorageContractError("observation payload channel registry/order mismatch")
    _opaque_id(record.pair_id, "pair_id")
    expected_available = set(SUITE_CHANNELS[suite])
    if set(record.available_channels) != expected_available:
        raise StorageContractError("suite_available_mask does not match the fixed suite contract")

    t = record.n_steps
    if t < 1:
        raise StorageContractError("observation payload must contain at least one step")
    for name in CHANNEL_NAMES:
        width = CHANNEL_WIDTH[name]
        values = np.asarray(record.values[name])
        valid = np.asarray(record.valid_mask[name])
        measurement = np.asarray(record.measurement_time_s[name])
        availability = np.asarray(record.availability_time_s[name])
        latency = np.asarray(record.latency_age_s[name])
        if values.shape != (t, width) or valid.shape != (t, width):
            raise StorageContractError(f"observation channel {name} has the wrong value/mask shape")
        if values.dtype != np.float64:
            raise StorageContractError(f"observation channel {name} values must be float64")
        if valid.dtype != np.bool_:
            raise StorageContractError(f"observation channel {name} valid mask must be bool")
        if measurement.shape != (t,) or availability.shape != (t,) or latency.shape != (t,):
            raise StorageContractError(f"observation channel {name} timing arrays must have shape [T]")
        if any(
            array.dtype != np.float64
            for array in (measurement, availability, latency)
        ):
            raise StorageContractError(
                f"observation channel {name} timing arrays must be float64"
            )
        if name not in expected_available:
            if not np.all(np.isnan(values)) or np.any(valid):
                raise StorageContractError(
                    f"unavailable channel {name} must be all-NaN and fully masked"
                )
            continue
        if np.any(~valid & ~np.isnan(values)) or np.any(valid & ~np.isfinite(values)):
            raise StorageContractError(
                f"available channel {name} values and validity mask are inconsistent"
            )
        if not (
            np.all(np.isfinite(measurement))
            and np.all(np.isfinite(availability))
            and np.all(np.isfinite(latency))
        ):
            raise StorageContractError(f"available channel {name} timing must be finite")
        if np.any(availability < measurement) or np.any(latency < 0.0):
            raise StorageContractError(f"available channel {name} violates causal timing")
        if not np.allclose(
            latency, availability - measurement, rtol=0.0, atol=1.0e-12
        ):
            raise StorageContractError(f"available channel {name} latency metadata is inconsistent")


class DeployableObservationLoader:
    """Load exactly one suite from one safe observation index/root.

    The constructor has no identity-manifest, plant, label, oracle, or sibling
    observation-root argument. Exact index headers and exact NPZ key allowlists
    make provenance or privileged leakage a build failure.
    """

    def __init__(
        self,
        suite_root: Path,
        suite: str,
        config: ValidatedConfig,
        *,
        require_frozen: bool = False,
    ) -> None:
        """Validate one suite root/index against one lifecycle-qualified config."""

        if suite not in DEPLOYABLE_SUITES:
            raise StorageContractError(f"deployable suite must be one of {DEPLOYABLE_SUITES}")
        if require_frozen and not config.is_frozen:
            raise ConfigContractError("confirmatory loader refuses a draft configuration")
        root = Path(suite_root)
        if root.name != suite or root.parent.name != "observations":
            raise StorageContractError(
                "suite_root must be exactly observations/<suite>, not a shared parent"
            )
        index_path = root / "index.csv"
        rows = read_role_index(index_path, observation=True)
        for row in rows:
            if row.config_hash != config.config_hash:
                raise StorageContractError(
                    f"observation index run {row.run_id} config_hash mismatch"
                )
        self._root = root
        self._suite = suite
        self._config = config
        self._rows = {row.run_id: row for row in rows}

    @property
    def run_ids(self) -> tuple[str, ...]:
        """Return the indexed deployable rollout ids."""

        return tuple(self._rows)

    @property
    def suite(self) -> str:
        """Return the single suite this loader can resolve."""

        return self._suite

    def load(self, run_id: str) -> ObservedRecord:
        """Hash-check, key-audit, load, and validate one observation payload."""

        if run_id not in self._rows:
            raise KeyError(f"run_id not present in deployable index: {run_id}")
        row = self._rows[run_id]
        path = (self._root / row.npz_path).resolve()
        root = self._root.resolve()
        if not path.is_relative_to(root):
            raise StorageContractError("observation payload resolves outside its suite root")
        if not path.is_file():
            raise StorageContractError(f"observation payload not found: {path}")
        if file_sha256(path) != row.sha256:
            raise StorageContractError(f"observation payload SHA-256 mismatch: {run_id}")
        with np.load(path, allow_pickle=False) as payload:
            actual_keys = set(payload.files)
            expected_keys = _expected_observation_keys()
            if actual_keys != expected_keys:
                raise StorageContractError(
                    f"observation payload key allowlist mismatch; "
                    f"missing={sorted(expected_keys - actual_keys)}, "
                    f"forbidden={sorted(actual_keys - expected_keys)}"
                )
            record = ObservedRecord.from_npz_dict(
                {key: np.asarray(payload[key]) for key in payload.files}
            )
        _validate_observed_record(record, suite=self._suite, row=row)
        return record

    def audit_all(self) -> dict[str, int]:
        """Load and validate every indexed payload, failing on the first breach."""

        counts = {split: 0 for split in SPLITS}
        for run_id, row in self._rows.items():
            self.load(run_id)
            counts[str(row.split)] += 1
        return counts
