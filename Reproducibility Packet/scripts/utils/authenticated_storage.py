"""Bytes-domain entry points into the closed storage and role contracts.

**Why this module exists, and why it is not an edit to those two files.**

Invariant W1 of the Slot-8 connection-record design says the authenticated object and
the interpreted object are one object. A pathname is not an object: two reads of one
name are two reads, they may return different bytes, and every check made across them
is a statement about neither. `utils.storage_contract` and `utils.role_contract` take
paths and open them themselves, so a caller that authenticated a file's bytes had no way
to hand *those bytes* to their parsers -- it could only bracket the call with a second
measurement, which detects a change still present when the call returns and is blind to
one made and reverted inside it.

The obvious repair was to add bytes and rows entry points to those two modules. That
repair is not available, and the reason is measured rather than asserted:
`utils.dev_fit_trainer.training_code_identity` pins the canonical text digest of eight
files as bound 4's training-protocol identity, and `role_contract.py` and
`storage_contract.py` are two of the eight. The approved development-fit ledger, the
approved stage-1 capacity-sweep plan and the approved rung-2 escalation plan each record
`role_contract.py = c50bebe5...` and `storage_contract.py = 40b0f88c...`, and
`capacity_sweep.require_anchor_comparability` refuses when the current tree disagrees --
as do the two read-only analyzers, which compare the recorded identity against the
current one before they will read a completed run. Editing either file therefore makes
three completed, jointly approved, unrepeatable lanes non-comparable and stops the
packet's own runbook from reproducing them. This is the rule decision D4 already applied
to `attribution_net.py`, `dev_fit_trainer.py` and `capacity_sweep.py`, reaching two more
of the same eight files.

So the entry points live here instead, and this module changes no recorded identity.

**What is reused and what is restated.** Every *rule* is reused from the module that
owns it: `audit_identity_manifest` and `_validate_role_index_rows` for the two CSV
documents, `validate_role_payload` for a payload's key allowlist, dtypes, shapes and
role semantics, `_expected_root` for the role layout, and `RolePayloadLoader` itself as
the base class. What is restated is the *reading mechanics* the closed functions perform
before they reach those rules: a strict header comparison and a typing loop over
`csv.DictReader`. That duplication is real and is held closed by equality rather than by
intention -- `tests/test_authenticated_storage.py` requires each parser here to return
exactly what the closed path-based function returns for the same document, so the two
cannot drift without a test going red. That is the same discipline
`utils.connection_adapter.external_bytes_digest` gets against `file_sha256` and that
`ROLE_NAMES` gets against `schema.json`: a copied fact is allowed only when something
mechanical compares it against its owner.

**What this module does not do.** It opens no file. Every entry point takes bytes or
already-parsed rows from a caller that authenticated them, which is the whole point:
the read belongs to the caller that owns the digest.
"""

from __future__ import annotations

import contextlib
import csv
import hashlib
import io
import zipfile
from pathlib import Path
from typing import Any, Iterable, Mapping

import numpy as np

from .config_contract import ValidatedConfig
from .role_contract import RolePayloadLoader, _expected_root, validate_role_payload
from .storage_contract import (
    IDENTITY_MANIFEST_FIELDS,
    OBSERVATION_INDEX_FIELDS,
    ROLE_INDEX_FIELDS,
    IdentityManifestRow,
    RoleIndexRow,
    StorageContractError,
    _validate_role_index_rows,
    audit_identity_manifest,
)

#: The five schema-A manifest columns that are integers rather than opaque strings.
MANIFEST_SEED_FIELDS = (
    "sim_seed",
    "fault_seed",
    "sensor_seed",
    "controller_seed",
    "train_seed",
)


def bytes_sha256(raw: bytes) -> str:
    """Return the lowercase SHA-256 digest of exact bytes.

    This is `utils.storage_contract.file_sha256`'s rule over a value rather than over a
    pathname, and the two are pinned equal by test. A caller that already holds the
    bytes it authenticated must be able to apply the rule to that value: a digest taken
    from a second open is a statement about whatever the name resolved to on that open.
    """

    return hashlib.sha256(raw).hexdigest()


def _strict_header(
    reader: csv.DictReader, expected: tuple[str, ...], source: object
) -> None:
    """Require a CSV header to expose exactly the allowlisted fields and order."""

    actual = tuple(reader.fieldnames or ())
    if actual != expected:
        raise StorageContractError(
            f"{source} header must be exactly {expected}; got {actual}"
        )


def _reader(raw: bytes, source: object) -> csv.DictReader:
    """Return a strict CSV reader over exact bytes, refusing anything but UTF-8.

    `newline=""` matches how the closed readers open their files, so a quoted field
    containing a line break is read identically here and there.
    """

    try:
        text = raw.decode("utf-8")
    except UnicodeDecodeError as exc:
        raise StorageContractError(f"{source} is not valid UTF-8") from exc
    return csv.DictReader(io.StringIO(text, newline=""))


def parse_identity_manifest(
    raw: bytes, *, source: object = "<bytes>"
) -> list[IdentityManifestRow]:
    """Type and audit one exact schema-A identity manifest from exact bytes.

    Args:
        raw: the exact manifest bytes the caller read and digested.
        source: what to name in a refusal message.

    Returns:
        Exactly what `utils.storage_contract.read_identity_manifest` returns for the
        same document, audited by that module's own `audit_identity_manifest`.

    Raises:
        StorageContractError: for non-UTF-8 bytes, a header that is not the exact
            allowlist in the exact order, a row that will not type, or any schema-A
            audit failure.
    """

    reader = _reader(raw, source)
    _strict_header(reader, IDENTITY_MANIFEST_FIELDS, source)
    rows: list[IdentityManifestRow] = []
    for columns in reader:
        try:
            typed = {
                **columns,
                **{name: int(columns[name]) for name in MANIFEST_SEED_FIELDS},
            }
            rows.append(IdentityManifestRow(**typed))
        except (TypeError, ValueError) as exc:
            raise StorageContractError(
                f"invalid identity row in {source}: {columns}"
            ) from exc
    audit_identity_manifest(rows)
    return rows


def parse_role_index(
    raw: bytes, *, observation: bool, source: object = "<bytes>"
) -> list[RoleIndexRow]:
    """Type and validate one exact schema-E role index from exact bytes.

    Args:
        raw: the exact index bytes the caller read and digested.
        observation: whether the split-bearing observation header is required.
        source: what to name in a refusal message.

    Returns:
        Exactly what `utils.storage_contract.read_role_index` returns for the same
        document, validated by that module's own row rules.
    """

    expected = OBSERVATION_INDEX_FIELDS if observation else ROLE_INDEX_FIELDS
    reader = _reader(raw, source)
    _strict_header(reader, expected, source)
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


def validate_role_index_rows(
    rows: Iterable[RoleIndexRow], *, observation: bool
) -> list[RoleIndexRow]:
    """Apply the closed row rules to rows a caller parsed for itself.

    A caller that parsed an index out of authenticated bytes still hands those rows to
    an object that must apply this package's rules to them rather than trust them, and
    `parse_role_index` cannot be that check because it is the step the caller already
    ran.
    """

    materialized = list(rows)
    _validate_role_index_rows(materialized, observation=observation)
    return materialized


@contextlib.contextmanager
def npz_archive_from_bytes(raw: bytes, *, what: str):
    """Open one exact non-pickled NPZ byte string, or refuse by contract.

    Args:
        raw: the exact archive bytes a caller has already authenticated.
        what: what to name in a refusal message.

    Yields:
        The open `NpzFile`.

    Raises:
        StorageContractError: when the bytes are not a readable non-pickled NPZ
            archive, at open **or** at any member read inside the block.

    A payload can carry the digest its record declares and still be an archive numpy
    cannot read: truncation raises `zipfile.BadZipFile` at open, and a member whose
    stored bytes disagree with its CRC raises the same at read. Neither is a
    `ValueError`, so without this translation a caller that handles this package's
    error type takes a raw exception out of the layer whose whole job is to refuse
    unsafe payloads, and the named refusal its contract promised never happens.

    A `StorageContractError` raised by the caller *inside* the block passes through
    untouched. It is a `ValueError`, so without that clause the caller's own refusal --
    a key-allowlist failure, say -- would be caught here and re-described as a broken
    archive.
    """

    try:
        with np.load(io.BytesIO(raw), allow_pickle=False) as archive:
            yield archive
    except StorageContractError:
        raise
    except (ValueError, OSError, EOFError, zipfile.BadZipFile) as exc:
        raise StorageContractError(
            f"{what} is not a readable non-pickled NPZ archive: {exc}"
        ) from exc


class AuthenticatedRolePayloadLoader(RolePayloadLoader):
    """A `RolePayloadLoader` bound to authenticated rows, entered with authenticated bytes.

    It is the closed loader in every respect that is a *rule*: `validate_role_payload`
    applies the key allowlist, the schema's dtypes and shapes and the role's semantics,
    `_validate_role_index_rows` applies the row grammar, `_expected_root` applies the
    schema-E layout, and the index rows are joined to the configuration exactly as the
    base class joins them. What it does not do is open anything.

    **Path containment is not repeated at the bytes entry point, and that is a statement
    rather than an omission.** Containment is a property of an *open*, and `load_bytes`
    performs none: the caller has already read the bytes. The half of the rule that is a
    property of the *row* -- one relative single-component `.npz` name, no traversal, no
    drive letter -- is applied to the given rows at construction. The resolution half
    belongs to the inherited `load`, which is the entry point that resolves and opens.
    Re-resolving a path nothing is about to open would be a guard no input could make
    decisive.
    """

    def __init__(
        self,
        root: Path,
        role: str,
        schema: Mapping[str, Any],
        config: ValidatedConfig,
        index_rows: Iterable[RoleIndexRow],
        *,
        suite: str | None = None,
    ) -> None:
        """Bind one role root to exactly the index rows the caller authenticated.

        Args:
            index_rows: rows parsed from the index bytes the caller digested. They are
                re-validated here and joined to `config`, so this constructor accepts
                nothing the base class reading `index.csv` would have rejected.

        The base class's `__init__` is deliberately not called: its whole body is the
        read this class exists to remove. Everything it does *besides* that read is done
        here, against the same rules from the same owners.
        """

        self.root = Path(root)
        _expected_root(self.root, role, suite)
        self.role = role
        self.schema = schema
        self.config = config
        rows = validate_role_index_rows(index_rows, observation=False)
        for row in rows:
            if row.config_hash != config.config_hash:
                raise StorageContractError(
                    f"{role} index config_hash mismatch for {row.run_id}"
                )
        self._rows = {row.run_id: row for row in rows}

    def load_bytes(self, run_id: str, raw: bytes) -> dict[str, np.ndarray]:
        """Validate one exact payload byte string the caller already authenticated.

        Args:
            run_id: the run whose authenticated index row governs this payload.
            raw: the exact payload bytes the caller read and digested.

        Returns:
            The same normalized payload the inherited `load` returns, having applied the
            same digest, key-allowlist, dtype/shape and role-semantic rules to it.

        Raises:
            KeyError: when no authenticated index row authorises `run_id`.
            StorageContractError: when the bytes do not digest to the row's `sha256`,
                are not a readable non-pickled archive, or fail the schema or the role's
                semantics.
        """

        if run_id not in self._rows:
            raise KeyError(f"run_id not present in {self.role} index: {run_id}")
        row = self._rows[run_id]
        if bytes_sha256(raw) != row.sha256:
            raise StorageContractError(f"{self.role} payload SHA-256 mismatch: {run_id}")
        with npz_archive_from_bytes(
            raw, what=f"{self.role} payload {run_id}"
        ) as archive:
            payload = {name: np.asarray(archive[name]) for name in archive.files}
        return validate_role_payload(self.role, payload, self.schema, self.config)
