"""Machine-readable schema and draft/frozen configuration authority.

The prose contract lives in ``schema/schema-v1.0.md``. Its executable rendering
is ``schema/schema.json``. Development and validation may use a separately named
draft configuration with an explicit ``dev-`` hash, but only a complete,
jointly-approved file named exactly ``config.json`` may authorize confirmatory
payload generation.
"""

from __future__ import annotations

import copy
import hashlib
import json
import re
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Mapping

_HEX_64 = re.compile(r"^[0-9a-f]{64}$")
_DRAFT_PREFIX = "dev-"


class ConfigContractError(ValueError):
    """Raised when schema/config state is incomplete, mismatched, or unsafe."""


@dataclass(frozen=True)
class ValidatedConfig:
    """A configuration that passed schema, canonical-hash, and lifecycle checks."""

    source_path: Path
    schema_path: Path
    document: Mapping[str, Any]
    config_hash: str
    status: str

    @property
    def is_frozen(self) -> bool:
        """Return whether this is the final confirmatory-authorizing state."""

        return self.status == "frozen"


def file_sha256(path: Path) -> str:
    """Return the lowercase SHA-256 digest of one file's bytes."""

    return hashlib.sha256(Path(path).read_bytes()).hexdigest()


def _json_load_strict(path: Path) -> dict[str, Any]:
    """Load one JSON object while rejecting NaN/Infinity and duplicate keys."""

    def reject_constant(value: str) -> None:
        raise ConfigContractError(f"non-finite JSON constant is forbidden: {value}")

    def unique_object(pairs: list[tuple[str, Any]]) -> dict[str, Any]:
        out: dict[str, Any] = {}
        for key, value in pairs:
            if key in out:
                raise ConfigContractError(f"duplicate JSON key is forbidden: {key}")
            out[key] = value
        return out

    try:
        loaded = json.loads(
            Path(path).read_text(encoding="utf-8"),
            parse_constant=reject_constant,
            object_pairs_hook=unique_object,
        )
    except json.JSONDecodeError as exc:
        raise ConfigContractError(f"invalid JSON in {path}: {exc}") from exc
    if not isinstance(loaded, dict):
        raise ConfigContractError(f"{path} must contain one JSON object")
    return loaded


def canonical_json_bytes(document: Mapping[str, Any]) -> bytes:
    """Return canonical UTF-8 JSON bytes, omitting the self-referential hash."""

    payload = copy.deepcopy(dict(document))
    payload.pop("config_hash", None)
    try:
        rendered = json.dumps(
            payload,
            sort_keys=True,
            separators=(",", ":"),
            ensure_ascii=False,
            allow_nan=False,
        )
    except (TypeError, ValueError) as exc:
        raise ConfigContractError(f"configuration is not canonical-JSON serializable: {exc}") from exc
    return rendered.encode("utf-8")


def expected_config_hash(document: Mapping[str, Any]) -> str:
    """Return the lifecycle-qualified canonical hash for a config document."""

    digest = hashlib.sha256(canonical_json_bytes(document)).hexdigest()
    status = document.get("status")
    if status == "draft":
        return f"{_DRAFT_PREFIX}{digest}"
    if status == "frozen":
        return digest
    raise ConfigContractError("configuration status must be 'draft' or 'frozen'")


def _value_at_path(document: Mapping[str, Any], dotted_path: str) -> Any:
    """Resolve a dotted mapping path or raise a contract error."""

    value: Any = document
    for part in dotted_path.split("."):
        if not isinstance(value, Mapping) or part not in value:
            raise ConfigContractError(f"missing freeze-required config path: {dotted_path}")
        value = value[part]
    return value


def _contains_null(value: Any) -> bool:
    """Return whether a nested JSON value contains an unresolved null."""

    if value is None:
        return True
    if isinstance(value, Mapping):
        return any(_contains_null(item) for item in value.values())
    if isinstance(value, list):
        return any(_contains_null(item) for item in value)
    return False


def _contains_empty_container(value: Any) -> bool:
    """Return whether a nested JSON value contains an unresolved empty container."""

    if isinstance(value, Mapping):
        return not value or any(_contains_empty_container(item) for item in value.values())
    if isinstance(value, list):
        return not value or any(_contains_empty_container(item) for item in value)
    return False


def _contains_forbidden_string_prefix(value: Any, prefixes: tuple[str, ...]) -> bool:
    """Return whether a nested frozen value retains a development-only marker."""

    if isinstance(value, str):
        return value.startswith(prefixes)
    if isinstance(value, Mapping):
        return any(
            _contains_forbidden_string_prefix(item, prefixes) for item in value.values()
        )
    if isinstance(value, list):
        return any(_contains_forbidden_string_prefix(item, prefixes) for item in value)
    return False


def validate_machine_schema(schema: Mapping[str, Any]) -> None:
    """Validate the executable schema's minimum authority and role declarations."""

    if schema.get("schema_version") != "1.0":
        raise ConfigContractError("machine schema must declare schema_version '1.0'")
    if schema.get("status") != "in_force":
        raise ConfigContractError("machine schema must be in_force")
    roles = schema.get("roles")
    required_roles = {
        "identity_manifest",
        "plant",
        "observations",
        "labels",
        "estimator_outputs",
        "controller_logs",
    }
    if not isinstance(roles, Mapping) or set(roles) != required_roles:
        raise ConfigContractError(
            f"machine schema roles must be exactly {sorted(required_roles)}"
        )
    contract = schema.get("config_contract")
    if not isinstance(contract, Mapping):
        raise ConfigContractError("machine schema is missing config_contract")
    if not contract.get("freeze_required_paths"):
        raise ConfigContractError("machine schema must declare freeze_required_paths")
    if not contract.get("frozen_decision"):
        raise ConfigContractError("machine schema must declare the frozen approval decision")


def validate_config_document(
    document: Mapping[str, Any],
    *,
    source_path: Path,
    schema: Mapping[str, Any],
    schema_path: Path,
    require_frozen: bool = False,
) -> ValidatedConfig:
    """Validate one draft or frozen config against the machine authority."""

    validate_machine_schema(schema)
    contract = schema["config_contract"]
    required = set(contract["required_top_level"])
    actual = set(document)
    missing = required - actual
    if missing:
        raise ConfigContractError(f"configuration is missing top-level fields: {sorted(missing)}")
    unknown = actual - required
    if unknown:
        raise ConfigContractError(f"configuration has unknown top-level fields: {sorted(unknown)}")

    status = document.get("status")
    if status not in {"draft", "frozen"}:
        raise ConfigContractError("configuration status must be 'draft' or 'frozen'")
    if not isinstance(document.get("config_version"), str) or not document["config_version"]:
        raise ConfigContractError("configuration config_version must be a nonempty string")
    if not isinstance(document.get("decision"), str) or not document["decision"]:
        raise ConfigContractError("configuration decision must be a nonempty string")
    if not isinstance(document.get("values"), Mapping):
        raise ConfigContractError("configuration values must be an object")
    if document.get("schema_version") != schema.get("schema_version"):
        raise ConfigContractError("configuration schema_version does not match schema.json")
    if document.get("schema_sha256") != file_sha256(schema_path):
        raise ConfigContractError("configuration schema_sha256 does not match schema.json bytes")

    path = Path(source_path)
    if status == "draft":
        if path.name.lower() == "config.json":
            raise ConfigContractError("a draft configuration must never be named config.json")
        if document.get("confirmatory_payloads_allowed") is not False:
            raise ConfigContractError("draft config must forbid confirmatory payload generation")
        open_gates = document.get("open_gates")
        if not isinstance(open_gates, list) or not open_gates:
            raise ConfigContractError("draft config must name at least one open gate")
        if any(not isinstance(gate, str) or not gate for gate in open_gates):
            raise ConfigContractError("draft open_gates must be unique nonempty strings")
        if len(open_gates) != len(set(open_gates)):
            raise ConfigContractError("draft open_gates must be unique nonempty strings")
    else:
        if path.name != "config.json":
            raise ConfigContractError("the frozen configuration must be named exactly config.json")
        if document.get("confirmatory_payloads_allowed") is not True:
            raise ConfigContractError("frozen config must explicitly allow confirmatory payloads")
        if document.get("open_gates") != []:
            raise ConfigContractError("frozen config cannot retain open gates")
        if document.get("decision") != contract["frozen_decision"]:
            raise ConfigContractError(
                f"frozen config decision must be {contract['frozen_decision']!r}"
            )
        for dotted_path in contract["freeze_required_paths"]:
            value = _value_at_path(document, dotted_path)
            if _contains_null(value):
                raise ConfigContractError(
                    f"frozen config path contains unresolved null: {dotted_path}"
                )
            if _contains_empty_container(value):
                raise ConfigContractError(
                    f"frozen config path contains unresolved empty container: {dotted_path}"
                )
        prefixes = tuple(contract.get("frozen_forbidden_string_prefixes", ()))
        if prefixes and _contains_forbidden_string_prefix(document, prefixes):
            raise ConfigContractError(
                f"frozen config contains a development-only string prefix: {prefixes}"
            )

    supplied_hash = document.get("config_hash")
    expected_hash = expected_config_hash(document)
    if supplied_hash != expected_hash:
        raise ConfigContractError(
            f"config_hash mismatch: supplied {supplied_hash!r}, expected {expected_hash!r}"
        )
    if status == "draft" and not str(supplied_hash).startswith(_DRAFT_PREFIX):
        raise ConfigContractError("draft config_hash must use the dev- prefix")
    if status == "frozen" and not _HEX_64.fullmatch(str(supplied_hash)):
        raise ConfigContractError("frozen config_hash must be one lowercase 64-hex digest")
    if require_frozen and status != "frozen":
        raise ConfigContractError("confirmatory operation refuses draft configuration")

    return ValidatedConfig(
        source_path=path,
        schema_path=Path(schema_path),
        document=document,
        config_hash=str(supplied_hash),
        status=str(status),
    )


def load_config(
    config_path: Path,
    schema_path: Path,
    *,
    require_frozen: bool = False,
) -> ValidatedConfig:
    """Load and validate a config plus its exact schema authority."""

    schema = _json_load_strict(Path(schema_path))
    document = _json_load_strict(Path(config_path))
    return validate_config_document(
        document,
        source_path=Path(config_path),
        schema=schema,
        schema_path=Path(schema_path),
        require_frozen=require_frozen,
    )
