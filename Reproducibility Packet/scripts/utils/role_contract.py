"""Schema-driven role writers/loaders and the allowlisted supervised join.

The deployable model boundary remains ``DeployableObservationLoader``: it can
resolve one observation suite and nothing else.  This module is orchestration
code for building and evaluating role-separated datasets.  It writes one
numeric/non-pickled NPZ per rollout, exact role indexes, and exposes labels to
training only through an explicit split-limited join.
"""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from typing import Any, Iterable, Iterator, Mapping

import numpy as np

from .config_contract import ConfigContractError, ValidatedConfig
from .estimator import EstimatorOutput
from .schema_types import ObservedRecord, PrivilegedRecord
from .storage_contract import (
    DeployableObservationLoader,
    IdentityManifestRow,
    RoleIndexRow,
    StorageContractError,
    audit_identity_manifest,
    file_sha256,
    read_role_index,
    write_identity_manifest,
    write_role_index,
)

NON_OBSERVATION_ROLES = ("plant", "labels", "estimator_outputs", "controller_logs")
TRAINING_SPLITS = ("dev", "pilot", "val")
KNOWN_SOURCE_CLASSES = ("healthy", "structure", "actuator", "sensor")


@dataclass(frozen=True)
class SupervisedExample:
    """One feature/target pair with no manifest or privileged payload attached."""

    run_id: str
    observation: Any
    target: Mapping[str, Any]


def _schema_role(schema: Mapping[str, Any], role: str) -> Mapping[str, Any]:
    """Return one non-observation role definition from the machine schema."""

    if role not in NON_OBSERVATION_ROLES:
        raise StorageContractError(f"unsupported non-observation role: {role!r}")
    try:
        definition = schema["roles"][role]
    except (KeyError, TypeError) as exc:
        raise StorageContractError(f"machine schema does not define role {role!r}") from exc
    if definition.get("format") != "npz" or definition.get("deployable") is not False:
        raise StorageContractError(f"role {role!r} must be a non-deployable NPZ role")
    return definition


def _dtype_matches(array: np.ndarray, declared: str) -> bool:
    """Return whether an array exactly satisfies one declared storage dtype."""

    if declared == "float64":
        return array.dtype == np.float64
    if declared == "int64":
        return array.dtype == np.int64
    if declared == "bool":
        return array.dtype == np.bool_
    if declared == "unicode":
        return array.dtype.kind == "U"
    return False


def _shape_matches(
    array: np.ndarray,
    declared: list[Any],
    dimensions: dict[str, int],
) -> bool:
    """Bind dynamic leading dimensions and check a schema-declared shape."""

    if array.ndim != len(declared):
        return False
    for axis, token in enumerate(declared):
        if isinstance(token, int):
            expected = token
        elif token in {"T", "N_decisions"}:
            if token in dimensions and dimensions[token] != array.shape[axis]:
                return False
            dimensions[token] = int(array.shape[axis])
            continue
        elif token == "n_def":
            expected = dimensions["n_def"]
        else:
            raise StorageContractError(f"unsupported schema dimension token: {token!r}")
        if array.shape[axis] != expected:
            return False
    return True


def _semantic_role_checks(role: str, payload: Mapping[str, np.ndarray]) -> None:
    """Enforce role semantics that shape/dtype declarations cannot express."""

    if role == "plant":
        try:
            record = PrivilegedRecord(**{key: np.asarray(value) for key, value in payload.items()})
            record.validate()
        except (TypeError, ValueError) as exc:
            raise StorageContractError(f"invalid plant payload: {exc}") from exc
        return

    if role == "labels":
        source = str(np.asarray(payload["source_class"]).item())
        if source not in KNOWN_SOURCE_CLASSES:
            raise StorageContractError(f"invalid label source_class: {source!r}")
        for name in ("subtype",):
            if not str(np.asarray(payload[name]).item()):
                raise StorageContractError(f"label {name} must be nonempty")
        location = int(np.asarray(payload["location"]).item())
        onset_index = int(np.asarray(payload["onset_index"]).item())
        severity = float(np.asarray(payload["severity"]).item())
        onset_time = float(np.asarray(payload["onset_time_s"]).item())
        if location < -1 or onset_index < -1:
            raise StorageContractError("label location/onset_index must be >= -1")
        if not np.isfinite(severity) or not np.isfinite(onset_time) or onset_time < 0.0:
            raise StorageContractError("label severity/onset_time_s must be finite")
        return

    if role == "estimator_outputs":
        count = int(np.asarray(payload["step"]).shape[0])
        if count < 1:
            raise StorageContractError("estimator_outputs must contain at least one decision")
        previous_step = -1
        previous_time = -np.inf
        for index in range(count):
            output = EstimatorOutput(
                step=int(payload["step"][index]),
                decision_time_s=float(payload["decision_time_s"][index]),
                p_class=np.asarray(payload["p_class"][index]),
                unknown_score=float(payload["unknown_score"][index]),
                abstain_decision=bool(payload["abstain_decision"][index]),
                location_out=int(payload["location_out"][index]),
                severity_out=float(payload["severity_out"][index]),
                severity_uncertainty=float(payload["severity_uncertainty"][index]),
                detection_time_s=float(payload["detection_time_s"][index]),
            )
            try:
                output.validate()
            except ValueError as exc:
                raise StorageContractError(f"invalid estimator output at row {index}: {exc}") from exc
            if output.step <= previous_step or output.decision_time_s <= previous_time:
                raise StorageContractError("estimator decision axes must be strictly increasing")
            previous_step = output.step
            previous_time = output.decision_time_s
        return

    if role == "controller_logs":
        step = np.asarray(payload["step"])
        time = np.asarray(payload["t_s"])
        if step.size < 1 or not np.array_equal(step, np.arange(step.size, dtype=np.int64)):
            raise StorageContractError("controller step must be a nonempty contiguous 0-based grid")
        if time.size > 1 and not np.all(np.diff(time) > 0.0):
            raise StorageContractError("controller time must be strictly increasing")
        for name in ("t_s", "applied_action", "gain_schedule"):
            if not np.all(np.isfinite(payload[name])):
                raise StorageContractError(f"controller field {name} contains non-finite values")
        if np.any(payload["gain_schedule"] < 0.0):
            raise StorageContractError("controller gain_schedule must be non-negative")
        if np.any(np.char.str_len(payload["controller_mode"].astype(str)) == 0):
            raise StorageContractError("controller_mode values must be nonempty")


def validate_role_payload(
    role: str,
    payload: Mapping[str, Any],
    schema: Mapping[str, Any],
    config: ValidatedConfig,
) -> dict[str, np.ndarray]:
    """Return a normalized exact-key payload after schema and semantic validation."""

    definition = _schema_role(schema, role)
    fields = definition["fields"]
    expected = set(fields)
    actual = set(payload)
    if actual != expected:
        raise StorageContractError(
            f"{role} payload key allowlist mismatch; "
            f"missing={sorted(expected - actual)}, forbidden={sorted(actual - expected)}"
        )
    normalized = {name: np.asarray(payload[name]) for name in fields}
    dimensions = {"n_def": int(config.document["values"]["plant"]["n_def"])}
    for name, declared in fields.items():
        array = normalized[name]
        if not _dtype_matches(array, str(declared["dtype"])):
            raise StorageContractError(
                f"{role}.{name} dtype {array.dtype} != {declared['dtype']}"
            )
        if not _shape_matches(array, list(declared["shape"]), dimensions):
            raise StorageContractError(
                f"{role}.{name} shape {array.shape} != {declared['shape']}"
            )
    _semantic_role_checks(role, normalized)
    return normalized


def _expected_root(root: Path, role: str, suite: str | None) -> None:
    """Require every writer/loader root to match schema-E role layout exactly."""

    if role in {"estimator_outputs", "controller_logs"}:
        if suite not in {"C0", "C1", "S", "O"}:
            raise StorageContractError(f"{role} requires an explicit suite")
        if root.name != suite or root.parent.name != role:
            raise StorageContractError(f"{role} root must be exactly {role}/<suite>")
    else:
        if suite is not None or root.name != role:
            raise StorageContractError(f"{role} root must be exactly a {role}/ directory")


class RolePayloadWriter:
    """Write one non-observation role root and its exact hash index."""

    def __init__(
        self,
        root: Path,
        role: str,
        schema: Mapping[str, Any],
        config: ValidatedConfig,
        *,
        suite: str | None = None,
        assigned_rows: Mapping[str, IdentityManifestRow] | None = None,
    ) -> None:
        self.root = Path(root)
        _expected_root(self.root, role, suite)
        self.role = role
        self.schema = schema
        self.config = config
        self.suite = suite
        self._assigned_rows = dict(assigned_rows or {})
        self._rows: list[RoleIndexRow] = []
        self._run_ids: set[str] = set()

    def write(self, run_id: str, payload: Mapping[str, Any]) -> RoleIndexRow:
        """Validate and persist one payload; index publication remains explicit."""

        if run_id in self._run_ids:
            raise StorageContractError(f"duplicate {self.role} payload for run {run_id}")
        if self._assigned_rows:
            if run_id not in self._assigned_rows:
                raise StorageContractError(f"run_id is not assigned in manifest: {run_id}")
            assigned = self._assigned_rows[run_id]
            if self.suite is not None and assigned.suite != self.suite:
                raise StorageContractError(
                    f"run {run_id} is assigned to suite {assigned.suite}, not {self.suite}"
                )
        normalized = validate_role_payload(self.role, payload, self.schema, self.config)
        self.root.mkdir(parents=True, exist_ok=True)
        filename = f"{run_id}.npz"
        path = self.root / filename
        if path.exists():
            raise StorageContractError(f"refusing to overwrite existing role payload: {path}")
        np.savez(path, **normalized)
        row = RoleIndexRow(
            run_id=run_id,
            schema_version=str(self.schema["schema_version"]),
            config_hash=self.config.config_hash,
            npz_path=filename,
            sha256=file_sha256(path),
        )
        self._rows.append(row)
        self._run_ids.add(run_id)
        return row

    def publish_index(self) -> Path:
        """Publish the complete role index after all payloads are present."""

        if not self._rows:
            raise StorageContractError(f"cannot publish an empty {self.role} index")
        index = self.root / "index.csv"
        write_role_index(index, self._rows, observation=False)
        return index


class ObservationRoleWriter:
    """Write one suite's deployable observations and exact split-bearing index."""

    def __init__(
        self,
        root: Path,
        suite: str,
        config: ValidatedConfig,
        assigned_rows: Mapping[str, IdentityManifestRow],
    ) -> None:
        self.root = Path(root)
        if self.root.name != suite or self.root.parent.name != "observations":
            raise StorageContractError("observation root must be exactly observations/<suite>")
        self.suite = suite
        self.config = config
        self._assigned_rows = dict(assigned_rows)
        self._rows: list[RoleIndexRow] = []
        self._run_ids: set[str] = set()

    def write(self, record: ObservedRecord) -> RoleIndexRow:
        """Persist one manifest-bound observation record."""

        if record.run_id in self._run_ids:
            raise StorageContractError(f"duplicate observation payload for {record.run_id}")
        if record.run_id not in self._assigned_rows:
            raise StorageContractError(f"run_id is not assigned in manifest: {record.run_id}")
        assigned = self._assigned_rows[record.run_id]
        if assigned.suite != self.suite or record.suite != self.suite:
            raise StorageContractError("observation suite does not match manifest/root")
        if record.pair_id != assigned.pair_id or record.split != assigned.split:
            raise StorageContractError("observation pair/split does not match manifest")
        if record.config_hash != self.config.config_hash:
            raise StorageContractError("observation config_hash does not match validated config")
        self.root.mkdir(parents=True, exist_ok=True)
        filename = f"{record.run_id}.npz"
        path = self.root / filename
        if path.exists():
            raise StorageContractError(f"refusing to overwrite observation payload: {path}")
        record.save_npz(path)
        row = RoleIndexRow(
            run_id=record.run_id,
            schema_version=record.schema_version,
            config_hash=record.config_hash,
            npz_path=filename,
            sha256=file_sha256(path),
            split=record.split,
        )
        self._rows.append(row)
        self._run_ids.add(record.run_id)
        return row

    def publish_index(self) -> Path:
        """Publish the complete observation index."""

        if not self._rows:
            raise StorageContractError("cannot publish an empty observation index")
        index = self.root / "index.csv"
        write_role_index(index, self._rows, observation=True)
        return index


class RolePayloadLoader:
    """Hash-check and schema-validate one non-observation role root."""

    def __init__(
        self,
        root: Path,
        role: str,
        schema: Mapping[str, Any],
        config: ValidatedConfig,
        *,
        suite: str | None = None,
    ) -> None:
        self.root = Path(root)
        _expected_root(self.root, role, suite)
        self.role = role
        self.schema = schema
        self.config = config
        rows = read_role_index(self.root / "index.csv", observation=False)
        for row in rows:
            if row.config_hash != config.config_hash:
                raise StorageContractError(f"{role} index config_hash mismatch for {row.run_id}")
        self._rows = {row.run_id: row for row in rows}

    @property
    def run_ids(self) -> tuple[str, ...]:
        return tuple(self._rows)

    def load(self, run_id: str) -> dict[str, np.ndarray]:
        """Load one exact allowlisted payload after path and hash checks."""

        if run_id not in self._rows:
            raise KeyError(f"run_id not present in {self.role} index: {run_id}")
        row = self._rows[run_id]
        path = (self.root / row.npz_path).resolve()
        if not path.is_relative_to(self.root.resolve()) or not path.is_file():
            raise StorageContractError(f"{self.role} payload is missing or outside its root")
        if file_sha256(path) != row.sha256:
            raise StorageContractError(f"{self.role} payload SHA-256 mismatch: {run_id}")
        with np.load(path, allow_pickle=False) as archive:
            payload = {name: np.asarray(archive[name]) for name in archive.files}
        return validate_role_payload(self.role, payload, self.schema, self.config)

    def audit_all(self) -> int:
        """Validate every indexed role payload and return its count."""

        for run_id in self._rows:
            self.load(run_id)
        return len(self._rows)


class DatasetRoleBuilder:
    """Materialize role-separated payloads against one already-assigned manifest."""

    def __init__(
        self,
        output_root: Path,
        manifest_rows: Iterable[IdentityManifestRow],
        schema: Mapping[str, Any],
        config: ValidatedConfig,
    ) -> None:
        self.output_root = Path(output_root)
        self.schema = schema
        self.config = config
        self.rows = list(manifest_rows)
        audit_identity_manifest(
            self.rows,
            expected_config=config,
            require_complete_c1_s_pairs=True,
        )
        if not config.is_frozen and any(row.split == "test" for row in self.rows):
            raise ConfigContractError("draft configuration cannot materialize test-role payloads")
        self._by_run = {row.run_id: row for row in self.rows}

    def publish_manifest(self) -> Path:
        """Write the exact path-free assigned identity manifest."""

        path = self.output_root / "manifest.csv"
        write_identity_manifest(path, self.rows)
        return path

    def manifest_row(self, run_id: str) -> IdentityManifestRow:
        """Resolve one run identity without exposing a path."""

        try:
            return self._by_run[run_id]
        except KeyError as exc:
            raise StorageContractError(f"run_id is not assigned in manifest: {run_id}") from exc

    def make_writer(self, role: str, *, suite: str | None = None) -> RolePayloadWriter:
        """Create a role writer at the schema-E root for this dataset."""

        root = self.output_root / role
        if suite is not None:
            root = root / suite
        return RolePayloadWriter(
            root,
            role,
            self.schema,
            self.config,
            suite=suite,
            assigned_rows=self._by_run,
        )

    def make_observation_writer(self, suite: str) -> ObservationRoleWriter:
        """Create one manifest-bound writer for observations/<suite>."""

        return ObservationRoleWriter(
            self.output_root / "observations" / suite,
            suite,
            self.config,
            self._by_run,
        )


class SupervisedTrainingJoin:
    """Join one deployable suite to labels only for explicit non-test splits."""

    def __init__(
        self,
        observations: DeployableObservationLoader,
        labels: RolePayloadLoader,
        manifest_rows: Iterable[IdentityManifestRow],
        *,
        allowed_splits: tuple[str, ...] = TRAINING_SPLITS,
    ) -> None:
        if labels.role != "labels":
            raise StorageContractError("supervised join requires the labels role")
        if not allowed_splits or any(split not in TRAINING_SPLITS for split in allowed_splits):
            raise StorageContractError(
                f"training splits must be a nonempty subset of {TRAINING_SPLITS}"
            )
        self.observations = observations
        self.labels = labels
        self.allowed_splits = tuple(allowed_splits)
        self._rows = {
            row.run_id: row
            for row in manifest_rows
            if row.suite == observations.suite and row.split in self.allowed_splits
        }
        if not self._rows:
            raise StorageContractError("supervised join has no allowlisted rollout")
        expected = set(self._rows)
        if not expected.issubset(set(observations.run_ids)):
            raise StorageContractError("supervised join is missing observation payloads")
        if not expected.issubset(set(labels.run_ids)):
            raise StorageContractError("supervised join is missing label payloads")

    def examples(self, split: str) -> Iterator[SupervisedExample]:
        """Yield observation/target pairs without manifest or privileged fields."""

        if split not in self.allowed_splits:
            raise StorageContractError(f"split {split!r} is not allowlisted for training")
        for run_id, row in self._rows.items():
            if row.split != split:
                continue
            observation = self.observations.load(run_id)
            target_arrays = self.labels.load(run_id)
            target: dict[str, Any] = {
                name: np.asarray(value).item() for name, value in target_arrays.items()
            }
            yield SupervisedExample(run_id, observation, target)
