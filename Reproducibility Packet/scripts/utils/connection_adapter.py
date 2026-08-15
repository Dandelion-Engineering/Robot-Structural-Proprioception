"""The Slot-8 connection adapter: the authentication chain, read-order rows 4-12.

**What this module is.** It implements rows 4 through 12 of the read order in section
4.1 of `protocol/slot8-connection-record-v0.1.md` (Git blob `032db166`, jointly
approved Claude Session 135 / Codex Session 135) -- the *second boundary* that
document names:

    a schema, artifact, audit, index or payload is hashed before it is parsed or
    loaded.

`utils.connection_record` already implements rows 1, 2 and 3: it authenticates the
record's own bytes, strict-parses the section-3.2 field table, binds every declared
path to its own root domain without opening anything, and derives the section-4.2
allowlist. This module is the layer that starts opening files, and every file it
opens is one the bound record already named.

Concretely:

  * **step 4** -- `authenticate_config` digests the packet schema and the
    authority-appropriate config *before parsing either*, loads the config through
    the authenticated schema, requires the record's declared `config_hash` to equal
    the loaded one, and applies the adapter's own `dev-`/frozen authority rule;
  * **step 5** -- `authenticate_sources` digests and strict-parses the established
    result, the model-selection artifact, both threshold-source artifacts and the
    geometry-validation artifact, digests the geometry producer without importing
    it, resolves every declared field path and requires equality;
  * **step 6** -- `authenticate_dataset` digests and strict-parses `manifest.csv`
    and both dataset audits, recomputes the manifest census from the manifest's own
    rows, and requires both audits' echoes and censuses -- and the established
    result's split, config and case identities -- to agree;
  * **steps 7-12** -- `authenticate_roles` requires the schema-E role layout to
    exist, digests *every* named role index before parsing any of them, resolves
    every named run and payload path against the authenticated index, requires each
    named manifest row to equal the record's 20-field echo, digests every payload
    and checkpoint before loading any payload, and finally loads exactly the
    authenticated payload set through `utils.role_contract.RolePayloadLoader`.

`authenticate_connection` is the single roles-mode entry point invariant W8 names. It
takes the packet root as an explicit parameter, and that one root governs every
packet-relative resolution in the chain: the step-3 domain binding, the step-4 schema
and config resolution, and the step-5 source artifacts. A test binds an isolated
temporary packet tree and thereby exercises this exact production branch rather than a
parallel one.

**What this module is not.** It is not the whole adapter. Read-order rows 13 through
21 -- arm completeness, the C1/S pair check, the timebase binding, the decision
checks, the tracking window, the geometry derivation, the computed provenance state,
the bundle assembly and the exclusive-create write -- are the separately reviewed
second half of sub-step 4b-ii, together with the coherent geometry fixture, the
audit-hook observer of invariant W3, the `roles` CLI wiring and the additive
`build_role_bundle` change. **Nothing here licenses authoring a connection record,
running the adapter, opening `dev`, `pilot`, `val` or `test`, selecting a capacity or
a threshold, freezing a config, or making any C1-versus-S statement.** The public
`roles` subcommand still refuses unconditionally, and that remains the correct state
until the whole of sub-step 4b closes.

**Where the facts live** (design section 4.3, and standing lesson 199). This module
points at the object that already owns a fact rather than copying it:

  * file digests in the *external* domain -- `utils.storage_contract.file_sha256`;
  * file digests in the *tracked-text* domain -- `utils.protocol_p.canonical_text_sha256`;
  * config loading, the schema/config binding and the draft/frozen lifecycle --
    `utils.config_contract.load_config`;
  * the 20 schema-A manifest fields and their parser -- `utils.storage_contract`;
  * role index parsing and its strict header -- `utils.storage_contract.read_role_index`;
  * role payload hashing, path containment and schema/semantic validation --
    `utils.role_contract.RolePayloadLoader`;
  * the refusal codes and the error type -- `utils.verification_scene`;
  * the record contract itself -- `utils.connection_record`.

**Two digest domains, and the split is forced rather than chosen.**

  1. *Every tracked packet text file the adapter digests uses the canonical domain*
     (`canonical_text_sha256`, which strips a UTF-8 BOM and folds CRLF to LF): the
     schema, the config, the established result, the model-selection artifact, both
     threshold sources, the geometry producer and the geometry-validation artifact.
     This repository is developed on Windows with `core.autocrlf=true`, so an
     unpinned tracked text file materialises as CRLF in a fresh clone and a raw
     digest taken from it is a digest of *the copy*, not of *the document*. That is
     not hypothetical here: `config/draft-config-v0.1.json` is CRLF in this working
     tree and LF in the object store, so a raw rule for the config would be green on
     the machine that authored the record and red on a correct fresh checkout. The
     rule follows requirement X11/(cc) -- every digest a result artifact records is
     taken in the domain of the file's kind -- and it is the same domain
     `utils.dev_fit_contract.code_identity` already uses for `.py` files.
     `schema/schema.json` is additionally LF-pinned by both `.gitattributes` files
     because `config_contract` compares the config's declared `schema_sha256` against
     the schema's **raw** bytes; the pin makes the two domains agree on that one file,
     so the canonical rule here does not disturb that closed contract.
  2. *Every file under `--role-root` and `--checkpoint-root` uses the raw domain.*
     Those trees are the byte output of a generation run, are not Git-tracked, and are
     never re-materialised by a checkout, so the line-ending hazard does not reach
     them. For payloads the domain is not merely appropriate but **forced**: the role
     index rows carry `storage_contract.file_sha256` digests, and step 11 must compare
     the record against the authenticated index row, so a different domain there would
     compare two numbers that were never meant to be equal.

**Three interpretations this build had to make, recorded here rather than only in a
session report.** Each is a place where the approved design states a requirement whose
mechanism it deliberately left to the build round.

  1. *The authority rule is the adapter's own, and `require_frozen` is not it.*
     Finding CY's branch B scopes the config lifecycle to the record's authenticated
     `authority`: `DEVELOPMENT_ONLY` validates with `load_config(require_frozen=False)`
     and `FINAL` with `require_frozen=True`. Measured against the live contract,
     `require_frozen=False` **accepts a frozen document** -- it is permissive, not
     draft-only -- so relying on that flag alone would leave one of the four
     authority/lifecycle combinations unchecked. `require_authority_config_policy` is
     therefore a total function over the 2x2 and is tested directly over all four
     cells, independently of which layer happens to refuse first when the two are
     composed.
  2. *"Case and run identities" are checked where their evidence is.* Row 6 requires
     the established result's split, config and case/run identities to agree. The
     record declares a `cases_field_path` into the result artifact, so the case
     identity is checked as an exact set equality against the record's own menu, with
     duplicates refused. The *run* identity is not a field of the result artifact --
     the field table names no `runs_field_path` -- so it is checked where the evidence
     for it exists: every run the record names must be present in the authenticated
     manifest, at step 6, and its complete 20-field row must equal the record's echo,
     at step 10. Adding a run-identity field path to the record would ask an author to
     assert an identity the manifest already carries, which is design property 2's own
     failure mode.
  3. *The census the audits must echo is recomputed, never adopted.* Both delivered
     audits carry a `manifest_audit` block. The adapter recomputes every one of its
     six census fields from `manifest.csv` itself and requires equality, and
     additionally requires the two audits' `manifest_audit` blocks to be equal to each
     other. A digest alone proves only that one nominated file was stable; it does not
     prove that the file says research data were generated (finding CW, mechanism 1).

**One property this module holds that the read-order table alone does not imply.**
Nothing it returns is mutable. An authenticated artifact is a value: the parsed source
documents, the census, the index rows and the loaded payload map are all handed out as
read-only views over private copies, for the same reason `utils.connection_record`
deep-freezes the record. An allowlist -- or a set of authenticated facts derived from
one -- that a later caller can edit is not an allowlist.
"""

from __future__ import annotations

import json
import math
from dataclasses import dataclass
from pathlib import Path
from types import MappingProxyType
from typing import Any, Mapping, Sequence

import numpy as np

from utils.config_contract import ConfigContractError, ValidatedConfig, load_config
from utils.connection_record import (
    Arm,
    BoundPaths,
    Case,
    ConnectionRecord,
    MANIFEST_ROW_FIELDS,
    ROLE_NAMES,
    bind_root_domains,
    expected_open_set,
    load_connection_record,
)
from utils.protocol_p import canonical_text_sha256
from utils.role_contract import RolePayloadLoader
from utils.storage_contract import (
    IdentityManifestRow,
    RoleIndexRow,
    StorageContractError,
    file_sha256,
    read_identity_manifest,
    read_role_index,
)
from utils.verification_scene import (
    DEVELOPMENT_ONLY,
    FINAL,
    VerificationSceneError,
    X_IDENTITY_MISMATCH,
    X_PROVENANCE_UNRESOLVED,
    X_ROLE_ABSENT,
    X_ROLE_UNAUTHORIZED,
    X_SPLIT_FORBIDDEN,
)

# --------------------------------------------------------------------------- #
# Layout constants. Every one of these is a name the schema-E layout or the
# delivered dataset already fixes; none of them is a new convention.
# --------------------------------------------------------------------------- #

#: The role index filename, fixed by `utils.role_contract.RolePayloadWriter`.
ROLE_INDEX_NAME = "index.csv"

#: The identity manifest filename at the role root, fixed by `DatasetRoleBuilder`.
MANIFEST_NAME = "manifest.csv"

#: The two dataset audits at the role root, in the order the record names them.
AUDIT_NAMES: tuple[str, ...] = ("generation_audit", "independent_audit")

#: The roles whose schema-E root is suite-qualified (`<role>/<suite>/`). The other
#: two are flat (`<role>/`). This is `role_contract._expected_root`'s own rule,
#: restated here because the adapter must *build* the path that rule then checks.
SUITE_QUALIFIED_ROLES: frozenset[str] = frozenset({"estimator_outputs", "controller_logs"})

#: The census fields the adapter recomputes from `manifest.csv` and requires both
#: audits' `manifest_audit` blocks to echo exactly.
MANIFEST_CENSUS_FIELDS: tuple[str, ...] = (
    "manifest_rows",
    "reservations",
    "splits",
    "suites",
    "test_rows",
    "train_seed",
)

#: The key inside each audit document that carries the census.
MANIFEST_AUDIT_KEY = "manifest_audit"


# --------------------------------------------------------------------------- #
# Refusals, digests and strict parsing.
# --------------------------------------------------------------------------- #
def _refuse(code: str, message: str) -> VerificationSceneError:
    """Build one refusal carrying the read-order code its row names.

    Args:
        code: one of the refusal codes `utils.verification_scene` defines. There is
            one definition of what each code means and this module adds none.
        message: what was compared and what did not agree.

    Returns:
        The error to raise. It is returned rather than raised so every call site
        reads `raise _refuse(...)` and the raise stays visible at the site.
    """

    return VerificationSceneError(code, message)


def tracked_text_digest(path: Path) -> str:
    """Return the canonical-domain digest of one tracked packet text file.

    Args:
        path: the file to digest. It must exist; a missing file is the caller's
            refusal to name, because the code differs by read-order row.

    Returns:
        `utils.protocol_p.canonical_text_sha256(path)` -- the file's SHA-256 after a
        UTF-8 BOM is stripped and CRLF is folded to LF, which is the digest of the
        *document* rather than of the checkout's copy of it. See this module's
        docstring for why the domain split is forced rather than chosen.
    """

    return canonical_text_sha256(Path(path))


def external_digest(path: Path) -> str:
    """Return the raw-domain digest of one file under a machine-selected root.

    Args:
        path: the file to digest.

    Returns:
        `utils.storage_contract.file_sha256(path)` -- the SHA-256 of the exact bytes,
        with no transformation. This is the domain the role indexes themselves record,
        so it is the only domain in which step 11's comparison against an authenticated
        index row can mean anything.
    """

    return file_sha256(Path(path))


def _require_present(path: Path, *, where: str, code: str) -> Path:
    """Require one named file to exist as a regular file, or refuse with `code`."""

    if not path.is_file():
        raise _refuse(code, f"{where} is not present as a file at {path}")
    return path


def _require_digest_equal(
    path: Path,
    expected: str,
    *,
    where: str,
    digest: str,
) -> None:
    """Require one already-measured digest to equal the record's declared value.

    Args:
        path: the file the digest was taken over, for the message only.
        expected: the digest the authenticated record declares.
        where: the dotted record path that declared it.
        digest: the digest this module measured, in the file's own domain.

    Raises:
        VerificationSceneError: `X_IDENTITY_MISMATCH`. The measurement is passed in
            rather than taken here so that a caller can hash once and compare once;
            hashing inside the comparison would make "hash before parse" a claim about
            this function's body instead of about the caller's order.
    """

    if digest != expected:
        raise _refuse(
            X_IDENTITY_MISMATCH,
            f"{where} declares SHA-256 {expected} but {path} digests to {digest}",
        )


def _reject_non_finite(value: Any, where: str) -> None:
    """Refuse any `inf`/`NaN` reachable inside one parsed source document.

    A record forbids non-finite floats outright (design 3.1) and the artifacts a
    record names are the numbers it is checked against, so the same rule applies to
    them: a threshold, tolerance or maximum deviation of `NaN` compares false against
    everything, including itself, and would turn an equality gate into a silent accept
    on the one input it must refuse.
    """

    if isinstance(value, bool):
        return
    if isinstance(value, float) and not math.isfinite(value):
        raise _refuse(
            X_IDENTITY_MISMATCH,
            f"{where} contains the non-finite value {value!r}; a source artifact the "
            "record is checked against may not carry one",
        )
    if isinstance(value, Mapping):
        for key, item in value.items():
            _reject_non_finite(item, f"{where}.{key}")
        return
    if isinstance(value, (list, tuple)):
        for index, item in enumerate(value):
            _reject_non_finite(item, f"{where}[{index}]")


def strict_json_document(raw: bytes, where: str) -> dict[str, Any]:
    """Strict-parse one source artifact's bytes into a JSON object.

    Args:
        raw: the exact bytes already digested by the caller.
        where: what the artifact is, for the refusal message.

    Returns:
        The parsed top-level object.

    Raises:
        VerificationSceneError: `X_IDENTITY_MISMATCH` if the bytes are not UTF-8, are
            not one JSON object, repeat any key at any depth, or carry a non-finite
            number in any position.

    Why this is not `json.loads` with defaults: `json` accepts `NaN`, `Infinity` and
    `-Infinity` as bare literals, and it silently keeps the *last* of two duplicate
    keys. Either behaviour turns a document a reviewer read into a different document
    at runtime, which is the whole failure mode the digest exists to prevent -- and a
    digest cannot see it, because both readings are the same bytes.
    """

    def reject_constant(value: str) -> float:
        raise _refuse(
            X_IDENTITY_MISMATCH,
            f"{where} carries the bare JSON constant {value!r}, which is not a number",
        )

    def unique_object(pairs: list[tuple[str, Any]]) -> dict[str, Any]:
        seen: set[str] = set()
        for key, _ in pairs:
            if key in seen:
                raise _refuse(
                    X_IDENTITY_MISMATCH,
                    f"{where} repeats the object key {key!r}; a duplicate key makes the "
                    "document a reviewer read and the document a parser sees two "
                    "different objects over identical bytes",
                )
            seen.add(key)
        return dict(pairs)

    try:
        text = raw.decode("utf-8")
    except UnicodeDecodeError as exc:
        raise _refuse(X_IDENTITY_MISMATCH, f"{where} is not valid UTF-8: {exc}") from exc
    try:
        document = json.loads(
            text, parse_constant=reject_constant, object_pairs_hook=unique_object
        )
    except json.JSONDecodeError as exc:
        raise _refuse(X_IDENTITY_MISMATCH, f"{where} is not valid JSON: {exc}") from exc
    if not isinstance(document, dict):
        raise _refuse(
            X_IDENTITY_MISMATCH,
            f"{where} must be a JSON object, not {type(document).__name__}",
        )
    _reject_non_finite(document, where)
    return document


def value_at_field_path(document: Mapping[str, Any], field_path: str, *, where: str) -> Any:
    """Resolve one dotted field path inside an authenticated source document.

    Args:
        document: the strict-parsed artifact.
        field_path: a dotted path. A segment that is a run of digits indexes a JSON
            array; every other segment names an object key. Segments are never empty.
        where: the dotted *record* path that declared this field path.

    Returns:
        The value at that path.

    Raises:
        VerificationSceneError: `X_IDENTITY_MISMATCH` if the path is malformed, or if
            any segment is absent, out of range, or applied to a value of the wrong
            kind. An absent field is a refusal and never a `None`: a record that names
            a field the artifact does not carry has not been checked against anything.
    """

    if not field_path:
        raise _refuse(X_IDENTITY_MISMATCH, f"{where} declares an empty field path")
    segments = field_path.split(".")
    if any(segment == "" for segment in segments):
        raise _refuse(
            X_IDENTITY_MISMATCH,
            f"{where} declares the malformed field path {field_path!r}",
        )
    current: Any = document
    walked: list[str] = []
    for segment in segments:
        walked.append(segment)
        trail = ".".join(walked)
        if segment.isdigit():
            if not isinstance(current, list):
                raise _refuse(
                    X_IDENTITY_MISMATCH,
                    f"{where} indexes {trail} but that position is not a JSON array",
                )
            index = int(segment)
            if index >= len(current):
                raise _refuse(
                    X_IDENTITY_MISMATCH,
                    f"{where} indexes {trail} but that array holds {len(current)} entries",
                )
            current = current[index]
            continue
        if not isinstance(current, Mapping) or segment not in current:
            raise _refuse(
                X_IDENTITY_MISMATCH,
                f"{where} names the field path {field_path!r} but {trail} is absent",
            )
        current = current[segment]
    return current


def _require_numbers_equal(
    observed: Any,
    declared: float,
    *,
    where: str,
    source: str,
) -> None:
    """Require one authenticated artifact field to equal the record's declared number.

    Equality is exact. A tolerance here would be a plausibility band nobody approved,
    and design section 3.4's whole point is that a threshold is the one scientific
    input small enough for an author to transcribe from memory.
    """

    if isinstance(observed, bool) or not isinstance(observed, (int, float)):
        raise _refuse(
            X_IDENTITY_MISMATCH,
            f"{source} is {observed!r}, which is not a number; {where} declares {declared!r}",
        )
    if not math.isfinite(float(observed)):
        raise _refuse(
            X_IDENTITY_MISMATCH, f"{source} is the non-finite value {observed!r}"
        )
    if float(observed) != float(declared):
        raise _refuse(
            X_IDENTITY_MISMATCH,
            f"{where} declares {declared!r} but its named source {source} carries {observed!r}",
        )


def _require_strings_equal(observed: Any, declared: str, *, where: str, source: str) -> None:
    """Require one authenticated artifact field to equal the record's declared string."""

    if not isinstance(observed, str):
        raise _refuse(
            X_IDENTITY_MISMATCH,
            f"{source} is {observed!r}, which is not a string; {where} declares {declared!r}",
        )
    if observed != declared:
        raise _refuse(
            X_IDENTITY_MISMATCH,
            f"{where} declares {declared!r} but its named source {source} carries {observed!r}",
        )


def _frozen(value: Any) -> Any:
    """Return a deeply read-only view of one parsed JSON value.

    Mappings become `MappingProxyType` over a private copy and arrays become tuples,
    exactly as `utils.connection_record._freeze` does for the record itself. The
    reason is the same one finding 2 of the Step-4b-i review established: a frozen
    dataclass rebinds the attribute and not the object, so a `dict` reached through a
    frozen attribute is still editable, and "what was authenticated" has to keep
    meaning that.
    """

    if isinstance(value, Mapping):
        return MappingProxyType({key: _frozen(item) for key, item in value.items()})
    if isinstance(value, (list, tuple)):
        return tuple(_frozen(item) for item in value)
    return value


def _frozen_mapping(mapping: Mapping[Any, Any]) -> Mapping[Any, Any]:
    """Return a read-only view over a private copy of one mapping."""

    return MappingProxyType(dict(mapping))


# --------------------------------------------------------------------------- #
# Step 4 -- the schema, the config and the authority rule.
# --------------------------------------------------------------------------- #
@dataclass(frozen=True)
class AuthenticatedConfig:
    """The schema and config, each digested before either was parsed.

    Attributes:
        schema: the parsed machine schema, deeply frozen. It is kept because step 12
            hands it to `RolePayloadLoader` and a second read would be a second
            document.
        config: the `ValidatedConfig` `utils.config_contract.load_config` returned
            under the authority-appropriate `require_frozen` setting.
        schema_sha256: the canonical-domain digest this module measured.
        config_sha256: the canonical-domain digest this module measured.
    """

    schema: Mapping[str, Any]
    config: ValidatedConfig
    schema_sha256: str
    config_sha256: str


def require_authority_config_policy(authority: str, config: ValidatedConfig) -> None:
    """Require the config's lifecycle state to match the record's authority.

    Args:
        authority: the record's authenticated `authority`, `DEVELOPMENT_ONLY` or
            `FINAL`.
        config: the already-validated config.

    Raises:
        VerificationSceneError: `X_PROVENANCE_UNRESOLVED` when the two disagree.

    This is finding CY's branch B, and it is the adapter's own rule rather than a
    consequence of `load_config`'s `require_frozen` flag. Measured against the live
    contract, `require_frozen=False` **accepts a frozen document**: it refuses a draft
    when set, and permits either when clear. A `DEVELOPMENT_ONLY` record pointed at a
    frozen config would therefore pass the loader and would carry a development banner
    over the confirmatory configuration. This function is total over the 2x2 and is
    tested over all four cells directly, so its coverage does not depend on which
    layer refuses first when the two are composed.
    """

    if authority == DEVELOPMENT_ONLY:
        if config.is_frozen:
            raise _refuse(
                X_PROVENANCE_UNRESOLVED,
                "a DEVELOPMENT_ONLY record names a frozen configuration; the development "
                "authority may name only a draft config, and `require_frozen=False` "
                "accepts a frozen document rather than refusing it",
            )
        if not config.config_hash.startswith("dev-"):
            raise _refuse(
                X_PROVENANCE_UNRESOLVED,
                f"a DEVELOPMENT_ONLY record names config_hash {config.config_hash!r}, "
                "which does not carry the dev- prefix a draft config must carry",
            )
        if config.document.get("confirmatory_payloads_allowed") is not False:
            raise _refuse(
                X_PROVENANCE_UNRESOLVED,
                "a DEVELOPMENT_ONLY record names a config that does not explicitly "
                "forbid confirmatory payload generation",
            )
        return
    if not config.is_frozen:
        raise _refuse(
            X_PROVENANCE_UNRESOLVED,
            f"a FINAL record names a {config.status!r} configuration; the final "
            "authority may name only the frozen config.json",
        )
    if "dev-" in config.config_hash:
        raise _refuse(
            X_PROVENANCE_UNRESOLVED,
            "a FINAL record names a config whose config_hash carries a dev- trace",
        )


def authenticate_config(record: ConnectionRecord, bound: BoundPaths) -> AuthenticatedConfig:
    """Run read-order step 4: authenticate the schema and the config, in that order.

    Args:
        record: the record `parse_connection_record` returned.
        bound: the result of `bind_root_domains`.

    Returns:
        The parsed schema and the validated config.

    Raises:
        VerificationSceneError: `X_IDENTITY_MISMATCH` when either file is absent or
            digests differently from the record's declaration, or when the loaded
            config's semantic `config_hash` is not the one the record declares;
            `X_PROVENANCE_UNRESOLVED` when the config does not validate under the
            authority-appropriate lifecycle, or when it validates but names the wrong
            lifecycle for the record's authority.

    Both digests are measured **before** either file is parsed, which is the second
    boundary of section 4.1 and invariant W1. `load_config` then reads both again;
    that is a second read of two already-authenticated paths, not a second identity.
    """

    schema_path = _require_present(
        bound.schema_path, where="schema.relative_path", code=X_IDENTITY_MISMATCH
    )
    config_path = _require_present(
        bound.config_path, where="config.relative_path", code=X_IDENTITY_MISMATCH
    )
    schema_sha256 = tracked_text_digest(schema_path)
    config_sha256 = tracked_text_digest(config_path)
    _require_digest_equal(
        schema_path, record.schema.sha256, where="schema.sha256", digest=schema_sha256
    )
    _require_digest_equal(
        config_path, record.config.sha256, where="config.sha256", digest=config_sha256
    )

    require_frozen = record.authority == FINAL
    try:
        config = load_config(config_path, schema_path, require_frozen=require_frozen)
    except (ConfigContractError, ValueError, OSError) as exc:
        raise _refuse(
            X_PROVENANCE_UNRESOLVED,
            f"the config at {config_path} did not validate under authority "
            f"{record.authority} (require_frozen={require_frozen}): {exc}",
        ) from exc

    if config.config_hash != record.config.config_hash:
        raise _refuse(
            X_IDENTITY_MISMATCH,
            f"config.config_hash declares {record.config.config_hash!r} but the "
            f"validated config carries {config.config_hash!r}",
        )
    require_authority_config_policy(record.authority, config)

    schema_document = json.loads(schema_path.read_text(encoding="utf-8"))
    return AuthenticatedConfig(
        schema=_frozen(schema_document),
        config=config,
        schema_sha256=schema_sha256,
        config_sha256=config_sha256,
    )


# --------------------------------------------------------------------------- #
# Step 5 -- the source artifacts and every declared field path.
# --------------------------------------------------------------------------- #
@dataclass(frozen=True)
class AuthenticatedSources:
    """Every source artifact the record names, digested and strict-parsed.

    Attributes:
        documents: the parsed artifacts, keyed by the same dotted record paths
            `BoundPaths.packet_artifacts` uses, deeply frozen.
        established_cases: the case identities the established result names, in the
            artifact's own order.
        geometry_producer_sha256: the canonical-domain digest of
            `render_geometry.source.producer_relative_path`. The producer is hashed
            and never imported: importing it would let the file the record is checking
            decide what the check is.
        maximum_deviation_m: the real-data agreement the geometry-validation artifact
            records, already required not to exceed the declared tolerance.
    """

    documents: Mapping[str, Mapping[str, Any]]
    established_cases: tuple[str, ...]
    geometry_producer_sha256: str
    maximum_deviation_m: float


def _authenticate_artifact(
    bound: BoundPaths, key: str, expected_sha256: str
) -> dict[str, Any]:
    """Digest one packet source artifact, then strict-parse the same bytes.

    The bytes are read once and used for both, so the document that is parsed is
    provably the document that was digested rather than whatever the path names on a
    second read.
    """

    path = _require_present(
        bound.packet_artifacts[key], where=f"{key}.artifact", code=X_IDENTITY_MISMATCH
    )
    raw = path.read_bytes()
    _require_digest_equal(
        path,
        expected_sha256,
        where=f"{key}.sha256",
        digest=canonical_text_sha256(path),
    )
    return strict_json_document(raw, key)


def authenticate_sources(
    record: ConnectionRecord, bound: BoundPaths
) -> AuthenticatedSources:
    """Run read-order step 5: authenticate every declared scientific source.

    Args:
        record: the authenticated record.
        bound: the result of `bind_root_domains`.

    Returns:
        The parsed artifacts and the two derived facts later rows need.

    Raises:
        VerificationSceneError: `X_IDENTITY_MISMATCH` for an absent artifact, a digest
            mismatch, an unparseable document, an absent declared field, or a declared
            value that does not equal its named source.

    This is invariant W5: every typed scientific choice equals its named source. Both
    thresholds, the rung, the width, the result's split and config identities and the
    geometry tolerance are checked at their declared field paths. Nothing here supplies
    a default, a plausibility band or a fallback -- sub-step 4b is explicitly forbidden
    from choosing a scientific number, and a value that cannot be checked is a refusal.
    """

    documents: dict[str, Mapping[str, Any]] = {}

    result = _authenticate_artifact(
        bound, "established_result", record.established_result.sha256
    )
    documents["established_result"] = result
    _require_strings_equal(
        value_at_field_path(
            result,
            record.established_result.split_field_path,
            where="established_result.split_field_path",
        ),
        record.split,
        where="split",
        source=(
            f"established_result.{record.established_result.split_field_path}"
        ),
    )
    _require_strings_equal(
        value_at_field_path(
            result,
            record.established_result.config_hash_field_path,
            where="established_result.config_hash_field_path",
        ),
        record.config.config_hash,
        where="config.config_hash",
        source=(
            f"established_result.{record.established_result.config_hash_field_path}"
        ),
    )
    established_cases = _require_case_identity_list(
        value_at_field_path(
            result,
            record.established_result.cases_field_path,
            where="established_result.cases_field_path",
        ),
        source=f"established_result.{record.established_result.cases_field_path}",
    )

    selection = _authenticate_artifact(
        bound, "model_selection.source", record.model_selection.source.sha256
    )
    documents["model_selection.source"] = selection
    _require_numbers_equal(
        value_at_field_path(
            selection,
            record.model_selection.source.rung_field_path,
            where="model_selection.source.rung_field_path",
        ),
        record.model_selection.rung,
        where="model_selection.rung",
        source=f"model_selection.source.{record.model_selection.source.rung_field_path}",
    )
    _require_numbers_equal(
        value_at_field_path(
            selection,
            record.model_selection.source.width_field_path,
            where="model_selection.source.width_field_path",
        ),
        record.model_selection.width,
        where="model_selection.width",
        source=f"model_selection.source.{record.model_selection.source.width_field_path}",
    )

    declared_thresholds = {
        "abstain_threshold": record.thresholds.abstain_threshold,
        "unknown_threshold": record.thresholds.unknown_threshold,
    }
    for name, source in record.thresholds.sources.items():
        key = f"thresholds.sources.{name}"
        document = _authenticate_artifact(bound, key, source.sha256)
        documents[key] = document
        _require_numbers_equal(
            value_at_field_path(
                document, source.field_path, where=f"{key}.field_path"
            ),
            declared_thresholds[name],
            where=f"thresholds.{name}",
            source=f"{key}.{source.field_path}",
        )

    producer = _require_present(
        bound.packet_artifacts["render_geometry.source"],
        where="render_geometry.source.producer_relative_path",
        code=X_IDENTITY_MISMATCH,
    )
    producer_sha256 = tracked_text_digest(producer)
    _require_digest_equal(
        producer,
        record.render_geometry.source.producer_sha256,
        where="render_geometry.source.producer_sha256",
        digest=producer_sha256,
    )

    tolerance_source = record.render_geometry.tolerance_source
    geometry = _authenticate_artifact(
        bound, "render_geometry.tolerance_source", tolerance_source.sha256
    )
    documents["render_geometry.tolerance_source"] = geometry
    _require_numbers_equal(
        value_at_field_path(
            geometry,
            tolerance_source.tolerance_field_path,
            where="render_geometry.tolerance_source.tolerance_field_path",
        ),
        record.render_geometry.distal_tolerance_m,
        where="render_geometry.distal_tolerance_m",
        source=(
            "render_geometry.tolerance_source."
            f"{tolerance_source.tolerance_field_path}"
        ),
    )
    maximum_deviation = value_at_field_path(
        geometry,
        tolerance_source.maximum_deviation_field_path,
        where="render_geometry.tolerance_source.maximum_deviation_field_path",
    )
    maximum_deviation_m = _require_measured_deviation(
        maximum_deviation, record.render_geometry.distal_tolerance_m
    )

    return AuthenticatedSources(
        documents=_frozen_mapping({key: _frozen(value) for key, value in documents.items()}),
        established_cases=established_cases,
        geometry_producer_sha256=producer_sha256,
        maximum_deviation_m=maximum_deviation_m,
    )


def _require_case_identity_list(value: Any, *, source: str) -> tuple[str, ...]:
    """Require one artifact field to be a non-empty list of unique case identities."""

    if not isinstance(value, (list, tuple)) or not value:
        raise _refuse(
            X_IDENTITY_MISMATCH,
            f"{source} must be a non-empty array of case identities, not {value!r}",
        )
    cases: list[str] = []
    for index, entry in enumerate(value):
        if not isinstance(entry, str) or not entry:
            raise _refuse(
                X_IDENTITY_MISMATCH,
                f"{source}[{index}] is {entry!r}; every case identity must be a "
                "non-empty string",
            )
        cases.append(entry)
    if len(set(cases)) != len(cases):
        raise _refuse(
            X_IDENTITY_MISMATCH,
            f"{source} repeats a case identity; the established result names each "
            "case once",
        )
    return tuple(cases)


def _require_measured_deviation(value: Any, tolerance: float) -> float:
    """Require the recorded real-data agreement not to exceed the declared tolerance.

    Design section 4.6: the exact-state record review can reject an unjustified
    margin, and this is the runtime half -- it prevents a different number travelling
    under the approved bytes. A negative deviation is refused because a maximum
    absolute deviation is a magnitude, and a document that reports one as negative is
    not the document the tolerance was justified against.
    """

    if isinstance(value, bool) or not isinstance(value, (int, float)):
        raise _refuse(
            X_IDENTITY_MISMATCH,
            f"the geometry validation artifact's maximum deviation is {value!r}, "
            "which is not a number",
        )
    deviation = float(value)
    if not math.isfinite(deviation) or deviation < 0.0:
        raise _refuse(
            X_IDENTITY_MISMATCH,
            f"the geometry validation artifact's maximum deviation is {value!r}; a "
            "maximum absolute deviation is a finite non-negative magnitude",
        )
    if deviation > float(tolerance):
        raise _refuse(
            X_IDENTITY_MISMATCH,
            f"the geometry validation artifact records a maximum deviation of "
            f"{deviation!r} m, which exceeds the declared tolerance {tolerance!r} m",
        )
    return deviation


# --------------------------------------------------------------------------- #
# Step 6 -- the manifest, both dataset audits and the recomputed census.
# --------------------------------------------------------------------------- #
@dataclass(frozen=True)
class AuthenticatedDataset:
    """The manifest and both audits, digested before parsed, with one census.

    Attributes:
        rows: every manifest row, keyed by `run_id`, as read by
            `utils.storage_contract.read_identity_manifest`.
        census: the census recomputed from those rows, which both audits echoed.
        audits: both parsed audit documents, deeply frozen.
    """

    rows: Mapping[str, IdentityManifestRow]
    census: Mapping[str, Any]
    audits: Mapping[str, Mapping[str, Any]]


def manifest_census(rows: Sequence[IdentityManifestRow]) -> dict[str, Any]:
    """Recompute the census both dataset audits must echo.

    Args:
        rows: every row of `manifest.csv`, already parsed.

    Returns:
        A mapping over `MANIFEST_CENSUS_FIELDS`: the row count, the number of distinct
        reservations (`pair_id`), the per-split row counts, the sorted distinct suites,
        the number of `test` rows, and the single distinct `train_seed`.

    Raises:
        VerificationSceneError: `X_IDENTITY_MISMATCH` if the manifest is empty or
            carries more than one `train_seed`, because the audits report one scalar
            there and a census that silently picked one of several would be an
            adopted value rather than a computed one.

    This is finding CW mechanism 1's computed half. It exists so that the audits are
    *checked* rather than believed: a digest proves that one nominated file was stable
    and proves nothing about whether it describes the tree beside it.
    """

    if not rows:
        raise _refuse(
            X_IDENTITY_MISMATCH, f"{MANIFEST_NAME} carries no rows to take a census over"
        )
    train_seeds = {int(row.train_seed) for row in rows}
    if len(train_seeds) != 1:
        raise _refuse(
            X_IDENTITY_MISMATCH,
            f"{MANIFEST_NAME} carries {len(train_seeds)} distinct train_seed values "
            f"{sorted(train_seeds)}; the dataset audits report exactly one",
        )
    splits: dict[str, int] = {}
    for row in rows:
        splits[row.split] = splits.get(row.split, 0) + 1
    return {
        "manifest_rows": len(rows),
        "reservations": len({row.pair_id for row in rows}),
        "splits": dict(sorted(splits.items())),
        "suites": sorted({row.suite for row in rows}),
        "test_rows": splits.get("test", 0),
        "train_seed": next(iter(train_seeds)),
    }


def _require_census_agrees(audit_name: str, block: Any, census: Mapping[str, Any]) -> None:
    """Require one audit's `manifest_audit` block to echo the recomputed census."""

    if not isinstance(block, Mapping):
        raise _refuse(
            X_IDENTITY_MISMATCH,
            f"{audit_name}.{MANIFEST_AUDIT_KEY} is {block!r}, not an object",
        )
    for field in MANIFEST_CENSUS_FIELDS:
        if field not in block:
            raise _refuse(
                X_IDENTITY_MISMATCH,
                f"{audit_name}.{MANIFEST_AUDIT_KEY} does not carry {field!r}",
            )
        observed = block[field]
        expected = census[field]
        if field == "splits":
            observed = dict(observed) if isinstance(observed, Mapping) else observed
        elif field == "suites":
            observed = list(observed) if isinstance(observed, (list, tuple)) else observed
            expected = list(expected)
        if observed != expected:
            raise _refuse(
                X_IDENTITY_MISMATCH,
                f"{audit_name}.{MANIFEST_AUDIT_KEY}.{field} is {observed!r} but the "
                f"census recomputed from {MANIFEST_NAME} is {expected!r}",
            )


def authenticate_dataset(
    record: ConnectionRecord,
    bound: BoundPaths,
    sources: AuthenticatedSources,
) -> AuthenticatedDataset:
    """Run read-order step 6: authenticate the manifest and both dataset audits.

    Args:
        record: the authenticated record.
        bound: the result of `bind_root_domains`.
        sources: the result of step 5, for the established result's case identities.

    Returns:
        The parsed manifest rows, the recomputed census and both audit documents.

    Raises:
        VerificationSceneError: `X_IDENTITY_MISMATCH` for an absent file, a digest
            mismatch, an unparseable audit, a disagreeing echo or census, an
            established-result case set that is not the record's own, or a named run
            that the manifest does not contain; `X_SPLIT_FORBIDDEN` when a named row
            does not carry the record's split.

    All three files are digested before any of them is parsed. The audits' echoes are
    then required to agree with the record **and with each other**, and their censuses
    to equal a census this module recomputes from the manifest's own rows. That
    combination is finding CW's first mechanism: a schema-conformant fixture tree
    cannot acquire research provenance by having a digest computed over it.
    """

    manifest_path = _require_present(
        bound.role_root / MANIFEST_NAME, where=MANIFEST_NAME, code=X_ROLE_ABSENT
    )
    audit_paths = {
        name: _require_present(
            bound.role_root / f"{name}.json", where=f"{name}.json", code=X_ROLE_ABSENT
        )
        for name in AUDIT_NAMES
    }
    declared_audits = {
        "generation_audit": record.data_root.generation_audit,
        "independent_audit": record.data_root.independent_audit,
    }

    _require_digest_equal(
        manifest_path,
        record.data_root.manifest_sha256,
        where="data_root.manifest_sha256",
        digest=external_digest(manifest_path),
    )
    audit_bytes: dict[str, bytes] = {}
    for name, path in audit_paths.items():
        raw = path.read_bytes()
        _require_digest_equal(
            path,
            declared_audits[name].sha256,
            where=f"data_root.{name}.sha256",
            digest=external_digest(path),
        )
        audit_bytes[name] = raw

    try:
        manifest_rows = read_identity_manifest(manifest_path)
    except (StorageContractError, ValueError, OSError) as exc:
        raise _refuse(
            X_IDENTITY_MISMATCH, f"{MANIFEST_NAME} did not parse: {exc}"
        ) from exc
    census = manifest_census(manifest_rows)

    audits: dict[str, Mapping[str, Any]] = {}
    for name in AUDIT_NAMES:
        document = strict_json_document(audit_bytes[name], f"{name}.json")
        declared = declared_audits[name]
        _require_strings_equal(
            document.get("status"),
            declared.status,
            where=f"data_root.{name}.status",
            source=f"{name}.status",
        )
        _require_strings_equal(
            document.get("assignment_hash"),
            declared.assignment_hash,
            where=f"data_root.{name}.assignment_hash",
            source=f"{name}.assignment_hash",
        )
        _require_strings_equal(
            document.get("config_hash"),
            declared.config_hash,
            where=f"data_root.{name}.config_hash",
            source=f"{name}.config_hash",
        )
        if MANIFEST_AUDIT_KEY not in document:
            raise _refuse(
                X_IDENTITY_MISMATCH,
                f"{name}.json does not carry a {MANIFEST_AUDIT_KEY} block",
            )
        _require_census_agrees(name, document[MANIFEST_AUDIT_KEY], census)
        audits[name] = document

    generation = record.data_root.generation_audit
    independent = record.data_root.independent_audit
    if generation.assignment_hash != independent.assignment_hash:
        raise _refuse(
            X_IDENTITY_MISMATCH,
            "the two dataset audits declare different assignment_hash values; one "
            "dataset has one assignment",
        )
    if generation.config_hash != independent.config_hash:
        raise _refuse(
            X_IDENTITY_MISMATCH,
            "the two dataset audits declare different config_hash values; one dataset "
            "was generated under one config",
        )
    if audits["generation_audit"][MANIFEST_AUDIT_KEY] != audits["independent_audit"][
        MANIFEST_AUDIT_KEY
    ]:
        raise _refuse(
            X_IDENTITY_MISMATCH,
            "the two dataset audits carry different manifest_audit blocks; they are "
            "two reports of one census",
        )

    declared_cases = tuple(case.case_id for case in record.cases)
    if set(sources.established_cases) != set(declared_cases):
        raise _refuse(
            X_IDENTITY_MISMATCH,
            f"the established result names cases {sorted(sources.established_cases)} "
            f"but the record's menu names {sorted(declared_cases)}; the surface "
            "presents exactly the cases the prior read established",
        )

    rows_by_run = {row.run_id: row for row in manifest_rows}
    for case in record.cases:
        for suite, arm in case.arms.items():
            row = rows_by_run.get(arm.run_id)
            if row is None:
                raise _refuse(
                    X_IDENTITY_MISMATCH,
                    f"cases.{case.case_id}.arms.{suite} names run {arm.run_id!r}, which "
                    f"{MANIFEST_NAME} does not contain",
                )
            if row.split != record.split:
                raise _refuse(
                    X_SPLIT_FORBIDDEN,
                    f"run {arm.run_id!r} is a {row.split!r} row but the record names "
                    f"split {record.split!r}",
                )

    return AuthenticatedDataset(
        rows=_frozen_mapping(rows_by_run),
        census=_frozen(census),
        audits=_frozen_mapping({name: _frozen(value) for name, value in audits.items()}),
    )


# --------------------------------------------------------------------------- #
# Steps 7-12 -- the role layout, the indexes, the manifest rows, the payloads.
# --------------------------------------------------------------------------- #
@dataclass(frozen=True)
class AuthenticatedRoles:
    """Exactly the payload set the record named, loaded after every digest agreed.

    Attributes:
        payloads: `(case_id, suite, role) -> the loaded payload`, each one already
            hash-checked, path-contained and schema/semantically validated by
            `utils.role_contract.RolePayloadLoader`.
        index_rows: `(case_id, suite, role) -> the authenticated index row` the
            payload's identity was taken from.
        checkpoint_sha256: `(case_id, suite) -> the raw digest of the checkpoint`.
            The checkpoint is digested and **never loaded**: nothing in this lane runs
            a model, and a `.pt` file is arbitrary code until something decides to
            deserialise it.
    """

    payloads: Mapping[tuple[str, str, str], Mapping[str, np.ndarray]]
    index_rows: Mapping[tuple[str, str, str], RoleIndexRow]
    checkpoint_sha256: Mapping[tuple[str, str], str]


def role_root_for(role_root: Path, role: str, suite: str) -> Path:
    """Return one arm's schema-E role directory.

    Args:
        role_root: the resolved `--role-root`.
        role: one of `utils.connection_record.ROLE_NAMES`.
        suite: `C1` or `S`.

    Returns:
        `<role_root>/<role>` for the flat roles and `<role_root>/<role>/<suite>` for
        the suite-qualified ones. This restates `role_contract._expected_root`'s rule
        because the adapter must *construct* the path that rule then checks; the two
        are held together by a test that drives the constructed path through the
        loader for every role.
    """

    if role in SUITE_QUALIFIED_ROLES:
        return role_root / role / suite
    return role_root / role


def _arm_role_pairs(record: ConnectionRecord) -> tuple[tuple[Case, str, Arm, str], ...]:
    """Return every `(case, suite, arm, role)` the record names, in record order."""

    pairs: list[tuple[Case, str, Arm, str]] = []
    for case in record.cases:
        for suite, arm in case.arms.items():
            for role in ROLE_NAMES:
                if role in arm.roles:
                    pairs.append((case, suite, arm, role))
    return tuple(pairs)


def require_role_layout(record: ConnectionRecord, bound: BoundPaths) -> Mapping[
    tuple[str, str, str], Path
]:
    """Run read-order step 7: require every named role root and index to exist.

    Returns:
        `(case_id, suite, role) -> the role directory`, so later steps resolve the
        layout once rather than each rebuilding it.

    Raises:
        VerificationSceneError: `X_ROLE_ABSENT` when a named role root's `index.csv` is
            not present. This is the one row whose refusal is about the world being
            incomplete rather than about an identity disagreeing, and it is deliberately
            checked before any index is digested: an absent role is not a digest mismatch
            and reporting it as one would send a reader looking for a corrupted file.

    **There is deliberately no separate check that the role directory exists**, and the
    reason is a proof rather than an omission: the index path is a child of the role
    root, so a role root that is absent, or that exists as a file rather than a
    directory, makes `<role root>/index.csv` fail `Path.is_file()` in every case. A
    directory guard above this one could therefore never be the only check to refuse --
    it could only change the wording of a refusal that was already certain. A guard with
    no input it alone decides is the same defect as a duplicated guard, so the message
    carries the role root instead. This was found by the build round's mutation sweep:
    deleting the directory guard changed no verdict on any input.
    """

    roots: dict[tuple[str, str, str], Path] = {}
    for case, suite, _arm, role in _arm_role_pairs(record):
        directory = role_root_for(bound.role_root, role, suite)
        _require_present(
            directory / ROLE_INDEX_NAME,
            where=(
                f"the {role} index of the role root "
                f"cases.{case.case_id}.arms.{suite}.roles.{role} names at {directory}"
            ),
            code=X_ROLE_ABSENT,
        )
        roots[(case.case_id, suite, role)] = directory
    return _frozen_mapping(roots)


def authenticate_role_indexes(
    record: ConnectionRecord,
    roots: Mapping[tuple[str, str, str], Path],
) -> Mapping[Path, str]:
    """Run read-order step 8: digest **every** named index before parsing any of them.

    Args:
        record: the authenticated record.
        roots: the result of step 7.

    Returns:
        `index path -> its raw digest`, one entry per distinct index.

    Raises:
        VerificationSceneError: `X_IDENTITY_MISMATCH` when any index digests
            differently from the `index_sha256` the record declares for it.

    Every index is digested before any is parsed, and that ordering is the row's whole
    content. Two arms of one case share a role root when the role is flat, so a
    distinct index may be named by several references; each reference's declared digest
    is compared, so a record that declared two different digests for one file refuses
    rather than silently taking the first.
    """

    digests: dict[Path, str] = {}
    for case in record.cases:
        for suite, arm in case.arms.items():
            for role, reference in arm.roles.items():
                index_path = roots[(case.case_id, suite, role)] / ROLE_INDEX_NAME
                if index_path not in digests:
                    digests[index_path] = external_digest(index_path)
                _require_digest_equal(
                    index_path,
                    reference.index_sha256,
                    where=(
                        f"cases.{case.case_id}.arms.{suite}.roles.{role}.index_sha256"
                    ),
                    digest=digests[index_path],
                )
    return _frozen_mapping(digests)


def resolve_index_rows(
    record: ConnectionRecord,
    bound: BoundPaths,
    roots: Mapping[tuple[str, str, str], Path],
) -> Mapping[tuple[str, str, str], RoleIndexRow]:
    """Run read-order step 9: parse the authenticated indexes and plan no other open.

    Raises:
        VerificationSceneError: `X_ROLE_UNAUTHORIZED` when a named run is absent from
            its authenticated index -- the adapter may not open a payload no index row
            authorises; `X_IDENTITY_MISMATCH` when an index does not parse, or when the
            row's `npz_path` does not resolve to exactly the payload path the record
            declared.

    The path comparison is against `BoundPaths.role_payloads`, which step 3 already
    resolved and contained under `--role-root`. Comparing the resolved paths rather
    than the two strings is what makes a differently-spelled but identical path agree
    and a same-looking but different path refuse.
    """

    parsed: dict[Path, dict[str, RoleIndexRow]] = {}
    rows: dict[tuple[str, str, str], RoleIndexRow] = {}
    for case in record.cases:
        for suite, arm in case.arms.items():
            for role in arm.roles:
                key = (case.case_id, suite, role)
                index_path = roots[key] / ROLE_INDEX_NAME
                if index_path not in parsed:
                    try:
                        index_rows = read_role_index(index_path, observation=False)
                    except (StorageContractError, ValueError, OSError) as exc:
                        raise _refuse(
                            X_IDENTITY_MISMATCH,
                            f"the {role} index at {index_path} did not parse: {exc}",
                        ) from exc
                    parsed[index_path] = {row.run_id: row for row in index_rows}
                row = parsed[index_path].get(arm.run_id)
                if row is None:
                    raise _refuse(
                        X_ROLE_UNAUTHORIZED,
                        f"cases.{case.case_id}.arms.{suite}.roles.{role} names run "
                        f"{arm.run_id!r}, which the authenticated {role} index does not "
                        "authorise",
                    )
                declared = bound.role_payloads[key]
                indexed = (roots[key] / row.npz_path).resolve()
                if indexed != declared:
                    raise _refuse(
                        X_IDENTITY_MISMATCH,
                        f"cases.{case.case_id}.arms.{suite}.roles.{role} declares payload "
                        f"{declared} but the authenticated index row names {indexed}",
                    )
                rows[key] = row
    return _frozen_mapping(rows)


def require_manifest_rows(record: ConnectionRecord, dataset: AuthenticatedDataset) -> None:
    """Run read-order step 10: require every echoed manifest row to equal the manifest.

    Raises:
        VerificationSceneError: `X_IDENTITY_MISMATCH` when any of the 20 schema-A
            fields disagrees; `X_SPLIT_FORBIDDEN` when the echoed row's own `split`
            field is not the record's split.

    This is invariant W4 and design property 2: the record echoes all 20 fields and the
    adapter compares them, because a record that merely *pointed at* a row would let
    the tree change underneath an approved record with no check noticing. The comparison
    is over `MANIFEST_ROW_FIELDS`, which `utils.connection_record` derives from
    `IdentityManifestRow` itself, so a schema-A change moves both sides together.
    """

    for case in record.cases:
        for suite, arm in case.arms.items():
            row = dataset.rows[arm.run_id]
            where = f"cases.{case.case_id}.arms.{suite}.manifest_row"
            if arm.manifest_row.get("split") != record.split:
                raise _refuse(
                    X_SPLIT_FORBIDDEN,
                    f"{where}.split is {arm.manifest_row.get('split')!r} but the record "
                    f"names split {record.split!r}",
                )
            for field in MANIFEST_ROW_FIELDS:
                echoed = arm.manifest_row[field]
                actual = getattr(row, field)
                if echoed != actual:
                    raise _refuse(
                        X_IDENTITY_MISMATCH,
                        f"{where}.{field} echoes {echoed!r} but {MANIFEST_NAME} carries "
                        f"{actual!r} for run {arm.run_id!r}",
                    )


def authenticate_payload_bytes(
    record: ConnectionRecord,
    bound: BoundPaths,
    index_rows: Mapping[tuple[str, str, str], RoleIndexRow],
) -> Mapping[tuple[str, str], str]:
    """Run read-order step 11: digest every payload and checkpoint before any load.

    Returns:
        `(case_id, suite) -> the checkpoint's raw digest`.

    Raises:
        VerificationSceneError: `X_ROLE_ABSENT` when a named payload or checkpoint is
            not present; `X_IDENTITY_MISMATCH` when a digest disagrees with the record
            **or** with the authenticated index row.

    The payload digest is compared twice on purpose, and the two comparisons are not
    redundant. The record's declaration is what a reviewer approved; the index row is
    what the dataset itself asserts. A payload that matches one and not the other is
    exactly the state where the tree moved underneath an approved record, and a single
    comparison would leave whichever side it omitted unchecked.
    """

    checkpoints: dict[tuple[str, str], str] = {}
    for case in record.cases:
        for suite, arm in case.arms.items():
            for role, reference in arm.roles.items():
                key = (case.case_id, suite, role)
                payload_path = _require_present(
                    bound.role_payloads[key],
                    where=f"cases.{case.case_id}.arms.{suite}.roles.{role} payload",
                    code=X_ROLE_ABSENT,
                )
                digest = external_digest(payload_path)
                _require_digest_equal(
                    payload_path,
                    reference.payload_sha256,
                    where=(
                        f"cases.{case.case_id}.arms.{suite}.roles.{role}.payload_sha256"
                    ),
                    digest=digest,
                )
                if digest != index_rows[key].sha256:
                    raise _refuse(
                        X_IDENTITY_MISMATCH,
                        f"the {role} payload for run {arm.run_id!r} digests to {digest} "
                        f"but its authenticated index row records "
                        f"{index_rows[key].sha256}",
                    )
            checkpoint_path = _require_present(
                bound.checkpoints[(case.case_id, suite)],
                where=f"cases.{case.case_id}.arms.{suite}.checkpoint",
                code=X_ROLE_ABSENT,
            )
            checkpoint_digest = external_digest(checkpoint_path)
            _require_digest_equal(
                checkpoint_path,
                arm.checkpoint.sha256,
                where=f"cases.{case.case_id}.arms.{suite}.checkpoint.sha256",
                digest=checkpoint_digest,
            )
            checkpoints[(case.case_id, suite)] = checkpoint_digest
    return _frozen_mapping(checkpoints)


def load_authenticated_payloads(
    record: ConnectionRecord,
    roots: Mapping[tuple[str, str, str], Path],
    authenticated: AuthenticatedConfig,
) -> Mapping[tuple[str, str, str], Mapping[str, np.ndarray]]:
    """Run read-order step 12: load exactly the authenticated payload set.

    Raises:
        VerificationSceneError: `X_IDENTITY_MISMATCH` when `RolePayloadLoader` refuses
            a payload's identity, path containment, schema or semantics.

    The loader is called rather than reimplemented (design 4.3): it re-derives the
    payload's digest, requires the path to stay under its own role root, and applies the
    schema's dtype and shape declarations plus the role's semantic checks. The adapter
    re-derives none of the three.

    **A scope statement rather than a defect**, recorded here so a later session does
    not rediscover it as one: a payload whose digest is exactly right but whose dtype or
    shape is wrong is not, in plain words, an identity mismatch, and none of the
    thirteen refusal codes fits it precisely. No fourteenth code is invented for it
    here; ruling Q1 forbade inventing a code for a branch nobody had built, and the row
    that builds the branch is the round entitled to propose splitting it.
    """

    loaders: dict[Path, RolePayloadLoader] = {}
    payloads: dict[tuple[str, str, str], Mapping[str, np.ndarray]] = {}
    for case in record.cases:
        for suite, arm in case.arms.items():
            for role in arm.roles:
                key = (case.case_id, suite, role)
                directory = roots[key]
                if directory not in loaders:
                    try:
                        loaders[directory] = RolePayloadLoader(
                            directory,
                            role,
                            authenticated.schema,
                            authenticated.config,
                            suite=suite if role in SUITE_QUALIFIED_ROLES else None,
                        )
                    except (StorageContractError, ValueError, OSError) as exc:
                        raise _refuse(
                            X_IDENTITY_MISMATCH,
                            f"the {role} role root at {directory} did not open: {exc}",
                        ) from exc
                try:
                    payload = loaders[directory].load(arm.run_id)
                except (StorageContractError, KeyError, ValueError, OSError) as exc:
                    raise _refuse(
                        X_IDENTITY_MISMATCH,
                        f"the {role} payload for run {arm.run_id!r} did not load: {exc}",
                    ) from exc
                payloads[key] = _frozen_mapping(payload)
    return _frozen_mapping(payloads)


def authenticate_roles(
    record: ConnectionRecord,
    bound: BoundPaths,
    authenticated: AuthenticatedConfig,
    dataset: AuthenticatedDataset,
) -> AuthenticatedRoles:
    """Run read-order steps 7 through 12 in their normative order."""

    roots = require_role_layout(record, bound)
    authenticate_role_indexes(record, roots)
    index_rows = resolve_index_rows(record, bound, roots)
    require_manifest_rows(record, dataset)
    checkpoints = authenticate_payload_bytes(record, bound, index_rows)
    payloads = load_authenticated_payloads(record, roots, authenticated)
    return AuthenticatedRoles(
        payloads=payloads,
        index_rows=index_rows,
        checkpoint_sha256=checkpoints,
    )


# --------------------------------------------------------------------------- #
# The roles-mode entry point (invariant W8).
# --------------------------------------------------------------------------- #
@dataclass(frozen=True)
class AuthenticatedConnection:
    """Everything read-order rows 1 through 12 established, and nothing more.

    Attributes:
        record: the authenticated, deeply frozen record.
        bound: every declared path, resolved under its own root.
        expected_opens: the section-4.2 allowlist derived from the bound record. It is
            carried here because the second half of sub-step 4b-ii compares it against
            what an audit hook observed, and the expected side must be derived from the
            record rather than from the observation.
        config: the schema and the validated config.
        sources: every declared scientific source artifact.
        dataset: the manifest, the census and both audits.
        roles: exactly the authenticated payload set.

    This value does **not** authorise rendering, writing or publishing anything. It is
    the state rows 13 through 21 begin from.
    """

    record: ConnectionRecord
    bound: BoundPaths
    expected_opens: frozenset[Path]
    config: AuthenticatedConfig
    sources: AuthenticatedSources
    dataset: AuthenticatedDataset
    roles: AuthenticatedRoles


def authenticate_connection(
    *,
    packet_root: Path,
    connection_record_path: Path,
    connection_record_sha256: str,
    config_path: Path,
    role_root: Path,
    checkpoint_root: Path,
    output_dir: Path,
) -> AuthenticatedConnection:
    """Run read-order rows 1 through 12: the complete authentication chain.

    Args:
        packet_root: the one packet root that governs every packet-relative resolution
            in the read order (invariant W8). It is an explicit parameter precisely so
            that a test can bind an isolated temporary packet tree and still exercise
            this production branch rather than a parallel one. The public roles path
            supplies the live packet root derived from the module's own location; no
            CLI argument, environment variable or record field may override it.
        connection_record_path: the `--connection-record` argument.
        connection_record_sha256: the `--connection-record-sha256` argument -- the
            digest the joint authorization named.
        config_path: the `--config` argument.
        role_root: the `--role-root` argument.
        checkpoint_root: the `--checkpoint-root` argument.
        output_dir: the `--output-dir` argument.

    Returns:
        The `AuthenticatedConnection` rows 13 through 21 begin from.

    Raises:
        VerificationSceneError: carrying the code the failing row of section 4.1 names.

    The order here **is** the contract, and it is normative: nothing scientific is
    opened before the record's own bytes are authenticated, and no schema, artifact,
    audit, index or payload is parsed or loaded before it is digested. This function
    exists as one implementation rather than as a sequence a caller assembles, because
    an order a caller can reassemble is not an order.
    """

    record = load_connection_record(Path(connection_record_path), connection_record_sha256)
    bound = bind_root_domains(
        record,
        packet_root=Path(packet_root),
        connection_record_path=Path(connection_record_path),
        config_path=Path(config_path),
        role_root=Path(role_root),
        checkpoint_root=Path(checkpoint_root),
        output_dir=Path(output_dir),
    )
    authenticated = authenticate_config(record, bound)
    sources = authenticate_sources(record, bound)
    dataset = authenticate_dataset(record, bound, sources)
    roles = authenticate_roles(record, bound, authenticated, dataset)
    return AuthenticatedConnection(
        record=record,
        bound=bound,
        expected_opens=expected_open_set(record, bound),
        config=authenticated,
        sources=sources,
        dataset=dataset,
        roles=roles,
    )
