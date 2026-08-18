"""The Slot-8 connection adapter: the authentication chain, read-order rows 4-18.

**What this module is.** It implements rows 4 through 18 of the read order in section
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
    authenticated payload set through `utils.role_contract.RolePayloadLoader`;
  * **steps 13-17** -- `resolve_cases` establishes the facts no single payload can
    carry, because each is a relation *between* payloads: that the loaded set covers
    both arms of every case and nothing else, that the two arms describe one body
    change and replay one commanded trajectory, that both arms bind to one playback
    grid, that the decisions the adapter carries forward are ordered and inside that
    grid's extent, and that the tracking block is a valid `utils.metrics.j_5s` call
    at the agreed onset over the record's declared window. It opens nothing: every
    fact it reads was authenticated by the rows above it;
  * **step 18** -- `resolve_geometry` derives each arm's planar centerline from the
    authenticated `q_true` and `deform_coords` under the geometry the record
    declares, by *calling* `utils.centerline_geometry` rather than restating its
    map, and requires the derived distal point to agree with the authenticated
    `true_task_output` to within the tolerance step 5 already bound to the
    authenticated geometry-validation artifact. It supplies no tolerance of its own:
    sub-step 4b chooses no real-data tolerance.

`authenticate_connection` is the single roles-mode entry point invariant W8 names. It
takes the packet root as an explicit parameter, and that one root governs every
packet-relative resolution in the chain: the step-3 domain binding, the step-4 schema
and config resolution, and the step-5 source artifacts. A test binds an isolated
temporary packet tree and thereby exercises this exact production branch rather than a
parallel one.

**What this module is not.** It is not the whole adapter. Read-order rows 19 through
21 -- the computed provenance state, the bundle assembly and the exclusive-create
write -- are still unbuilt, together with the audit-hook observer of invariant W3, the
`roles` CLI wiring and the additive `build_role_bundle` change.
**Nothing here licenses authoring a connection record,
running the adapter, opening `dev`, `pilot`, `val` or `test`, selecting a capacity or
a threshold, freezing a config, or making any C1-versus-S statement.** The public
`roles` subcommand still refuses unconditionally, and that remains the correct state
until the whole of sub-step 4b closes.

**Where the facts live** (design section 4.3, and standing lesson 199). This module
points at the object that already owns a fact rather than copying it:

  * file digests in the *external* domain -- `utils.storage_contract.file_sha256`;
  * file digests in the *tracked-text* domain -- `utils.protocol_p.canonical_text_sha256`;
  * config validation, the schema/config binding and the draft/frozen lifecycle --
    `utils.config_contract.validate_config_document`, the contract's document-level
    entry point. `load_config` is the same contract with a file read in front of it,
    and a chain whose whole subject is *which bytes* were validated cannot delegate
    that read;
  * the 20 schema-A manifest fields and their audit -- `utils.storage_contract`,
    reached over authenticated bytes through
    `utils.authenticated_storage.parse_identity_manifest`;
  * role index row rules -- `utils.storage_contract`, reached over authenticated
    bytes through `utils.authenticated_storage.parse_role_index` and, for rows this
    module already parsed, `validate_role_index_rows`;
  * role payload hashing, the key allowlist and schema/semantic validation --
    `utils.role_contract.RolePayloadLoader`, entered as
    `utils.authenticated_storage.AuthenticatedRolePayloadLoader`: the same class,
    bound to the rows this module authenticated and handed the payload bytes it read;
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
     `authority`: `DEVELOPMENT_ONLY` validates with `require_frozen=False` and
     `FINAL` with `require_frozen=True`. Measured against the live contract,
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
documents, the validated configuration's own document, the census, the index rows and
every loaded payload array are all handed out as read-only views over private copies,
for the same reason `utils.connection_record` deep-freezes the record. An allowlist --
or a set of authenticated facts derived from one -- that a later caller can edit is not
an allowlist, and rows 13 to 21 must not be able to consume facts different from the
facts rows 4 to 12 authenticated.

**And one property the read order states that only a single read can keep.**
Section 4.1's second boundary says a file is hashed *before* it is parsed or loaded.
That is worth something only if the thing that is parsed is the thing that was
hashed, and a pathname is not an object: two reads of one name are two objects that
may differ, and every check made across them is a statement about neither. So every
file this chain interprets is read **exactly once**, `authenticated_bytes` is the one
way in, and the value that read returned is what is digested, parsed, loaded and
compared.

Keeping that through the closed utilities took entry points rather than brackets.
`utils.storage_contract` and `utils.role_contract` take paths and open them
themselves, and this module may not reimplement their parsers (design 4.3), so an
earlier state of this file bracketed each call with a re-measurement. A bracket
detects a change that is *still present* when the utility returns and is blind to one
made and reverted inside the call -- and, as the Round-2 review measured, it does not
even close the persistent case for a loader that hashes a path and then reopens it,
because the second open happens inside the bracket.

`utils.authenticated_storage` supplies those entry points **without editing either
closed file**, and that separation is forced rather than stylistic:
`utils.dev_fit_trainer.training_code_identity` pins the canonical text digest of
`role_contract.py` and `storage_contract.py` as part of bound 4's training-protocol
identity, three approved artifacts record those exact digests, and
`capacity_sweep.require_anchor_comparability` and both read-only analyzers refuse when
the current tree disagrees. Editing either file would make the approved development
fit, the approved stage-1 sweep and the approved rung-2 escalation non-comparable and
would stop the packet's own runbook from reading them -- decision D4's rule, reaching
two more of the same eight files. The new module reuses every rule from its owner and
restates only the reading mechanics, held to its owners by equality tests.

**One second read survives, and the adapter fixes what it can observe.**
`utils.config_contract.validate_config_document` receives the schema as a *document*
-- so every structural rule it applies comes from the bytes this module
authenticated -- but it re-derives the schema's raw digest from `schema_path` itself,
to compare against the configuration's declared `schema_sha256`. This module therefore
first compares that declaration against the raw digest of the exact schema bytes it
authenticated. The closed contract's second read remains code-identity scope, but it
can now only confirm the same raw digest or refuse a later replacement; it cannot make
a configuration naming schema B validate under the rules from schema A. The count is
pinned at two by a test over the whole chain, so any new second read anywhere fails
rather than joining an allowance.

*** AND THAT COMPARISON MAKES THIS MODULE A SECOND CONSUMER OF THE `schema.json` EOL
PIN, WHICH IS THE FOLLOW-UP THE STEP-4b-ii-a CARD CARRIED FORWARD AND THIS IS ITS WHOLE
REPAIR. *** `utils.storage_contract.file_sha256` is the owner of the raw domain the
comparison above matches, and `schema/schema.json text eol=lf` in both `.gitattributes`
files is the reason raw is safe *for that one file*: the pin makes the canonical and raw
domains agree on it, so a fresh Windows checkout cannot materialise a schema whose raw
digest differs from the one the configuration declares. Before Session 143's guard, that
pin had exactly one consumer -- `config_contract` -- and its removal would have broken
only that closed contract. It now has two, and **the second one is silent**: nothing in
this module's behaviour changes when the pin is removed until a fresh clone on a CRLF
platform refuses a schema that is byte-correct in the object store.

**"Add a test" is not available as the answer, and that is the reason this is a
paragraph rather than an assertion.** A test that caught the pin's removal cannot exist
while the pin holds -- it would have to observe a checkout the pin prevents. So the
dependency is documented in the three places a reader could look: here, at the site that
depends on it; in **both** `.gitattributes` files, which now name this module as the
pin's second consumer beside `config_contract` and say that no test can catch the line's
removal; and on the Step-4b-ii-b Review Card as a standing disclosure.
"""

from __future__ import annotations

import hashlib
import json
import math
import zlib
from dataclasses import dataclass, fields as dataclass_fields, replace
from pathlib import Path
from types import MappingProxyType
from typing import Any, Callable, Mapping, Sequence

import numpy as np

from utils.config_contract import (
    ConfigContractError,
    ValidatedConfig,
    validate_config_document,
)
from utils.connection_record import (
    Arm,
    BUNDLE_FILE_NAMES,
    BoundPaths,
    CASE_FILE_SUFFIXES,
    Case,
    ConnectionRecord,
    MANIFEST_ROW_FIELDS,
    OUTPUT_PARENTS,
    ROLE_NAMES,
    bind_root_domains,
    expected_open_set,
    load_connection_record,
    record_relative_path,
)
from utils.protocol_p import canonical_text_sha256
from utils.authenticated_storage import (
    AuthenticatedRolePayloadLoader,
    parse_identity_manifest,
    parse_role_index,
)
from utils.storage_contract import (
    IdentityManifestRow,
    RoleIndexRow,
    StorageContractError,
    file_sha256,
)
from utils.estimator import EstimatorOutput
from utils.metrics import j_5s
from utils.centerline_geometry import (
    derive_centerline,
    require_distal_point_within_tolerance,
)
from utils.verification_scene import (
    BUNDLE_VERSION,
    DEVELOPMENT_ONLY,
    FINAL,
    LabelFields,
    SUITE_KEYS,
    Arm as SceneArm,
    ArmIdentity,
    BodyChange,
    Provenance,
    Thresholds,
    Tracking,
    VerificationBundle,
    VerificationScene,
    VerificationSceneError,
    bundle_from_json,
    canonical_bundle_text,
    canonical_scene_text,
    validate_bundle,
    X_ARMS_INCOMPLETE,
    X_BUNDLE_INCOMPLETE,
    X_DECISION_UNSUPPORTED,
    X_IDENTITY_MISMATCH,
    X_PAIR_MISMATCH,
    X_PROVENANCE_UNRESOLVED,
    X_ROLE_ABSENT,
    X_ROLE_UNAUTHORIZED,
    X_SPLIT_FORBIDDEN,
    X_TIMEBASE_MISMATCH,
    X_WINDOW_UNSUPPORTED,
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

#: Where the generated plant model's identity lives inside the authenticated
#: configuration. Design section 3.5 resolves the render geometry to the *record*
#: and requires `render_geometry.source` to name and hash the actual producer
#: (`scripts/utils/cable_mechanics.py`) **and to echo the config's `model_id`**;
#: step 5 is where that echo becomes a comparison. Without it the record can name a
#: model the configuration never described while every digest in the chain stays
#: valid, because the producer digest speaks for the *source file* and says nothing
#: about which model the run was configured to build. It is spelled as a declared
#: field path so it resolves through `value_at_field_path`, which turns an absent
#: field into this row's named refusal rather than a `None` that compares unequal
#: for the wrong reason.
PLANT_MODEL_ID_FIELD_PATH = "values.plant.model_id"

#: The most decimal digits one array-index segment of a declared field path may
#: carry. A JSON array held in memory cannot hold more than `sys.maxsize` entries,
#: and that number is 19 digits long, so a longer run of digits cannot address an
#: entry that exists -- it is out of range whatever its value. The bound is stated as
#: a literal rather than derived from `sys.maxsize`, because a test whose input is a
#: function of the constant it exercises holds the relationship and not the value.
#: It also keeps the segment far below CPython's 4,300-digit integer-conversion
#: limit, which raises a raw `ValueError` instead of this module's named refusal.
MAX_FIELD_PATH_INDEX_DIGITS = 19

#: The eight schema-D `labels` fields the two arms of one case must agree on. The
#: names are read out of `utils.verification_scene.LabelFields`'s own field list
#: rather than restated here, and that struct's names are themselves pinned by
#: equality against `schema/schema.json`. So this tuple inherits that pin instead of
#: adding a second copy of the same eight names that could drift away from it.
LABEL_FIELDS: tuple[str, ...] = tuple(
    field.name for field in dataclass_fields(LabelFields)
)

#: The frame-bearing `plant` arrays read-order rows 17 through 21 consume. `q_true`
#: and `deform_coords` are the body axes row 18 derives a centerline from;
#: `task_reference` and `true_task_output` are the tracking block row 17 hands to
#: `utils.metrics.j_5s`. Their dtypes, and their shapes *within one payload*, are the
#: schema's and were established at step 12; what step 15 adds is that their leading
#: axis is the same number in both arms and in the controller role.
PLANT_FRAME_ARRAYS: tuple[str, ...] = (
    "q_true",
    "deform_coords",
    "task_reference",
    "true_task_output",
)


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


def canonical_text_digest(raw: bytes) -> str:
    """Return the canonical-domain digest of bytes the caller already holds.

    Args:
        raw: the exact bytes read from a tracked packet text file.

    Returns:
        The SHA-256 of those bytes after a UTF-8 BOM is stripped and CRLF is folded to
        LF -- the same rule `utils.protocol_p.canonical_text_sha256` applies, in the
        one domain that makes a tracked text file's digest a property of the document
        rather than of the checkout's copy of it.

    **Why this exists beside the path-domain function that owns the rule.** The rule
    has one owner and this module does not restate it lightly (design 4.3). But
    `canonical_text_sha256` takes a *path* and opens it, so a chain that digests
    through it and then parses bytes it read separately has authenticated one read and
    interpreted another: the two are the same file only if nothing moved in between,
    which is exactly the assumption the second boundary of section 4.1 exists to
    remove. A bytes-domain digest lets one read serve both. The two are held together
    by `test_the_two_digest_domains_agree_with_the_functions_that_own_them`, which
    requires this function to equal `canonical_text_sha256` over BOM, CRLF, LF and
    mixed inputs on every run -- equality against the owner, not a copy trusted
    because it looks the same.
    """

    body = raw[3:] if raw.startswith(b"\xef\xbb\xbf") else raw
    return hashlib.sha256(body.replace(b"\r\n", b"\n")).hexdigest()


def external_bytes_digest(raw: bytes) -> str:
    """Return the raw-domain digest of bytes the caller already holds.

    This is `utils.storage_contract.file_sha256`'s rule over bytes rather than over a
    path, and it exists for the same reason `canonical_text_digest` does: so that the
    bytes that are authenticated are the bytes that are parsed. The same equality test
    pins it against the function that owns the rule.
    """

    return hashlib.sha256(raw).hexdigest()


def _read_bytes(path: Path, *, where: str, code: str) -> bytes:
    """Read one named file once, translating any read failure into a named refusal.

    A raw `OSError` out of an authentication layer is a silent failure by another
    name: the caller sees a crash instead of the refusal the design assigned to that
    row, and the exit code never happens. An absent file, a directory and an
    unreadable file all arrive here, which is why this is the only presence guard the
    authenticated read needs.
    """

    try:
        return Path(path).read_bytes()
    except OSError as exc:
        raise _refuse(code, f"{where} at {path} could not be read: {exc}") from exc


def authenticated_bytes(
    path: Path,
    expected: str,
    *,
    where: str,
    code: str,
    digest_of_bytes,
    named_by: str | None = None,
) -> bytes:
    """Read one named file **once** and return its bytes only if they authenticate.

    Args:
        path: the file the record names.
        expected: the digest the authenticated record declares for it.
        where: the dotted record path that declared the digest, for the refusal
            message.
        code: the refusal code this read-order row assigns.
        digest_of_bytes: `canonical_text_digest` for a tracked packet text file,
            `external_bytes_digest` for a file under a machine-selected root.
        named_by: the dotted record path that declared the *location*, when it differs
            from the one that declared the digest. An absent file is a complaint about
            where the record pointed and a disagreeing digest is a complaint about
            what it found there, and a reader sent to the wrong field by a message has
            been sent to look for a corrupted file that does not exist.

    Returns:
        The exact bytes that were digested. Every parse in this module is taken from
        the value this function returns, so the object that is interpreted is provably
        the object that was authenticated rather than whatever the same pathname
        happens to name on a later open.

    Raises:
        VerificationSceneError: `code` when the file is absent, is not a file, or
            cannot be read, and `X_IDENTITY_MISMATCH` when its digest disagrees with
            the record.

    There is deliberately no separate `is_file` guard in front of the read. An absent
    path, a directory and an unreadable file all raise `OSError` from the read itself,
    which `_read_bytes` turns into this row's named refusal, so a presence guard above
    it could never be the only check to refuse -- it could only change the wording of a
    refusal that was already certain, which is the defect the Session-141 sweep found
    in `require_role_layout`.
    """

    located = named_by if named_by is not None else where
    raw = _read_bytes(Path(path), where=located, code=code)
    _require_digest_equal(
        Path(path), expected, where=where, digest=digest_of_bytes(raw)
    )
    return raw


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


def _reject_non_finite(value: Any, where: str, code: str = X_IDENTITY_MISMATCH) -> None:
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
            code,
            f"{where} contains the non-finite value {value!r}; a source artifact the "
            "record is checked against may not carry one",
        )
    if isinstance(value, Mapping):
        for key, item in value.items():
            _reject_non_finite(item, f"{where}.{key}", code)
        return
    if isinstance(value, (list, tuple)):
        for index, item in enumerate(value):
            _reject_non_finite(item, f"{where}[{index}]", code)


def strict_json_document(
    raw: bytes, where: str, code: str = X_IDENTITY_MISMATCH
) -> dict[str, Any]:
    """Strict-parse one source artifact's bytes into a JSON object.

    Args:
        raw: the exact bytes already digested by the caller. This function never
            opens a file: the bytes it parses are the bytes the caller authenticated.
        where: what the artifact is, for the refusal message.
        code: the refusal code the calling read-order row assigns to a document that
            digests correctly and then does not parse. It is `X_IDENTITY_MISMATCH`
            for a source artifact and `X_PROVENANCE_UNRESOLVED` at step 4, where an
            unreadable schema or config is a configuration that did not validate
            under the record's authority rather than a disagreeing identity.

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
            code,
            f"{where} carries the bare JSON constant {value!r}, which is not a number",
        )

    def unique_object(pairs: list[tuple[str, Any]]) -> dict[str, Any]:
        seen: set[str] = set()
        for key, _ in pairs:
            if key in seen:
                raise _refuse(
                    code,
                    f"{where} repeats the object key {key!r}; a duplicate key makes the "
                    "document a reviewer read and the document a parser sees two "
                    "different objects over identical bytes",
                )
            seen.add(key)
        return dict(pairs)

    try:
        text = raw.decode("utf-8")
    except UnicodeDecodeError as exc:
        raise _refuse(code, f"{where} is not valid UTF-8: {exc}") from exc
    try:
        document = json.loads(
            text, parse_constant=reject_constant, object_pairs_hook=unique_object
        )
    except json.JSONDecodeError as exc:
        raise _refuse(code, f"{where} is not valid JSON: {exc}") from exc
    if not isinstance(document, dict):
        raise _refuse(
            code,
            f"{where} must be a JSON object, not {type(document).__name__}",
        )
    _reject_non_finite(document, where, code)
    return document


def value_at_field_path(document: Mapping[str, Any], field_path: str, *, where: str) -> Any:
    """Resolve one dotted field path inside an authenticated source document.

    Args:
        document: the strict-parsed artifact.
        field_path: a dotted path. A segment that is a run of **ASCII** digits, at
            most `MAX_FIELD_PATH_INDEX_DIGITS` of them, indexes a JSON array; every
            other segment names an object key. Segments are never empty.
        where: the dotted *record* path that declared this field path.

    Returns:
        The value at that path.

    Raises:
        VerificationSceneError: `X_IDENTITY_MISMATCH` if the path is malformed, or if
            any segment is absent, out of range, or applied to a value of the wrong
            kind. An absent field is a refusal and never a `None`: a record that names
            a field the artifact does not carry has not been checked against anything.

    **Two properties of the index segment that are the refusal rather than a crash.**
    `str.isdigit` is true of characters `int()` cannot convert -- the superscript two
    is a digit to Python and a `ValueError` to `int` -- and it is true of non-ASCII
    decimal digits that convert to a number no JSON author wrote. So an index segment
    is required to be ASCII, and anything else falls through to the object-key branch,
    where a key the artifact does not carry is the ordinary absent-field refusal.
    Length is bounded for the same reason: CPython refuses to convert an integer
    string beyond 4,300 digits and raises a raw `ValueError`, which would leave this
    row with a crash instead of the exit code section 4.1 assigns it. A record is a
    small document and both inputs fit inside one.
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
        if segment.isascii() and segment.isdigit():
            if len(segment) > MAX_FIELD_PATH_INDEX_DIGITS:
                raise _refuse(
                    X_IDENTITY_MISMATCH,
                    f"{where} declares an array index of {len(segment)} digits at "
                    f"segment {len(walked)}; no JSON array holds enough entries for an "
                    f"index longer than {MAX_FIELD_PATH_INDEX_DIGITS} digits, so it is "
                    "out of range whatever its value",
                )
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

    Equality is exact **and non-lossy**. A tolerance here would be a plausibility band
    nobody approved, and design section 3.4's whole point is that a threshold is the
    one scientific input small enough for an author to transcribe from memory.

    **Neither operand is converted to binary64**, and that is the whole content of this
    repair. `json` parses an integer literal exactly, so a source artifact may carry an
    integer no float can represent: `float(2**53 + 1) == float(2**53)` is true while
    the two literals are different numbers, and at around four hundred digits the
    conversion stops returning a wrong answer and starts raising a raw `OverflowError`
    instead. Python compares `int` against `float` exactly in both directions, so
    comparing the parsed values themselves is both correct and total -- no shape the
    record permits reaches a conversion here.

    **One consequence, stated rather than papered over.** `utils.connection_record`
    parses a declared threshold or tolerance through `_require_finite_float`, which
    *does* convert an integer literal to binary64. Where an author declares a value
    binary64 cannot hold exactly, the record's own parsed value is already the rounded
    one and an artifact carrying the unrounded integer refuses here. That is
    fail-closed and it is the correct direction: this function does not re-introduce
    the loss in order to make two different numbers agree.
    """

    if isinstance(observed, bool) or not isinstance(observed, (int, float)):
        raise _refuse(
            X_IDENTITY_MISMATCH,
            f"{source} is {observed!r}, which is not a number; {where} declares {declared!r}",
        )
    if isinstance(observed, float) and not math.isfinite(observed):
        raise _refuse(
            X_IDENTITY_MISMATCH, f"{source} is the non-finite value {observed!r}"
        )
    if isinstance(declared, float) and not math.isfinite(declared):
        raise _refuse(
            X_IDENTITY_MISMATCH,
            f"{where} declares the non-finite value {declared!r}",
        )
    if observed != declared:
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
        config: the `ValidatedConfig` `utils.config_contract.validate_config_document`
            returned under the authority-appropriate `require_frozen` setting, with its
            `document` replaced by a deeply read-only view of the same mapping. The
            contract's own dataclass is frozen, but `@dataclass(frozen=True)` rebinds
            the attribute rather than the object, so the mapping behind it is editable
            unless something makes it not be.
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

    Both files are read **once**, and both documents are parsed from the bytes those
    reads returned -- the second boundary of section 4.1 and invariant W1. This module
    calls `utils.config_contract.validate_config_document`, the contract's own
    document-level entry point, rather than `load_config`, which would reopen both
    paths and validate whatever they named on that later read.

    **The one remaining re-open is narrowed before it happens.**
    `validate_config_document` compares the config's declared `schema_sha256` against
    the schema's raw bytes, so it opens the schema again to hash it. This module first
    compares that declaration against the raw digest of the schema bytes it already
    authenticated. The contract's later read can still refuse a changed path, but it
    cannot make a config that declares a different schema validate under this module's
    authenticated schema document.
    """

    schema_path = Path(bound.schema_path)
    config_path = Path(bound.config_path)
    schema_raw = authenticated_bytes(
        schema_path,
        record.schema.sha256,
        where="schema.sha256",
        named_by="schema.relative_path",
        code=X_IDENTITY_MISMATCH,
        digest_of_bytes=canonical_text_digest,
    )
    config_raw = authenticated_bytes(
        config_path,
        record.config.sha256,
        where="config.sha256",
        named_by="config.relative_path",
        code=X_IDENTITY_MISMATCH,
        digest_of_bytes=canonical_text_digest,
    )
    schema_document = strict_json_document(
        schema_raw, "the machine schema", X_PROVENANCE_UNRESOLVED
    )
    config_document = strict_json_document(
        config_raw, "the configuration", X_PROVENANCE_UNRESOLVED
    )
    declared_schema_digest = config_document.get("schema_sha256")
    authenticated_schema_digest = external_bytes_digest(schema_raw)
    if declared_schema_digest != authenticated_schema_digest:
        raise _refuse(
            X_PROVENANCE_UNRESOLVED,
            "the configuration's schema_sha256 does not match the authenticated "
            f"schema bytes: config declares {declared_schema_digest!r}, "
            f"authenticated schema bytes digest to {authenticated_schema_digest!r}",
        )

    require_frozen = record.authority == FINAL
    try:
        config = validate_config_document(
            config_document,
            source_path=config_path,
            schema=schema_document,
            schema_path=schema_path,
            require_frozen=require_frozen,
        )
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

    return AuthenticatedConfig(
        schema=_frozen(schema_document),
        config=replace(config, document=_frozen(config.document)),
        schema_sha256=canonical_text_digest(schema_raw),
        config_sha256=canonical_text_digest(config_raw),
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
            decide what the check is. The digest is only half of that source's
            identity -- it fixes *which file built the model* and says nothing about
            *which model was configured* -- so step 5 separately joins
            `render_geometry.source.model_id` to `PLANT_MODEL_ID_FIELD_PATH` inside
            the config step 4 authenticated.
        maximum_deviation_m: the real-data agreement the geometry-validation artifact
            records, already required not to exceed the declared tolerance.
    """

    documents: Mapping[str, Mapping[str, Any]]
    established_cases: tuple[str, ...]
    geometry_producer_sha256: str
    maximum_deviation_m: float


def _authenticate_artifact(
    bound: BoundPaths,
    key: str,
    expected_sha256: str,
    opened: dict[Path, tuple[str, Mapping[str, Any]]],
) -> Mapping[str, Any]:
    """Digest one packet source artifact, then strict-parse the same bytes.

    Args:
        bound: the result of step 3.
        key: the dotted record path of the reference being authenticated.
        expected_sha256: the digest that reference declares.
        opened: `resolved path -> (its digest, its parsed document)` for every
            artifact this step has already read. Several references may name **one**
            file -- both threshold sources routinely do -- and a second reference is
            not an occasion to open it again: two reads of one name are two objects,
            and two declarations checked against two different objects are not a
            statement that they agree with each other. The file is read once and
            every declaration is compared against that one measurement, which is
            also what makes a record declaring two different digests for one file
            refuse rather than silently pass on the first.

    Returns:
        The parsed document, deep-frozen by the caller.

    The file is opened exactly once and the digest is taken over the bytes that read
    returned, so the document that is parsed is provably the document that was
    digested rather than whatever the path names on a second read. The earlier state
    of this function read the bytes, reopened the path to hash it, and then parsed the
    first read: two objects, one name, and a digest that spoke for neither of them if
    they differed.
    """

    path = Path(bound.packet_artifacts[key])
    if path not in opened:
        raw = _read_bytes(path, where=f"{key}.artifact", code=X_IDENTITY_MISMATCH)
        opened[path] = (canonical_text_digest(raw), strict_json_document(raw, key))
    digest, document = opened[path]
    _require_digest_equal(
        path, expected_sha256, where=f"{key}.sha256", digest=digest
    )
    return document


def authenticate_sources(
    record: ConnectionRecord, bound: BoundPaths, config: AuthenticatedConfig
) -> AuthenticatedSources:
    """Run read-order step 5: authenticate every declared scientific source.

    Args:
        record: the authenticated record.
        bound: the result of `bind_root_domains`.
        config: the result of step 4. It is required here for exactly one join --
            `render_geometry.source.model_id` -- and it is taken as a parameter
            rather than re-read because the config this row must agree with is the
            one step 4 digested and validated, not whatever the path names now.

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
    opened: dict[Path, tuple[str, Mapping[str, Any]]] = {}

    result = _authenticate_artifact(
        bound, "established_result", record.established_result.sha256, opened
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
        bound, "model_selection.source", record.model_selection.source.sha256, opened
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
        document = _authenticate_artifact(bound, key, source.sha256, opened)
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
    _require_strings_equal(
        value_at_field_path(
            config.config.document,
            PLANT_MODEL_ID_FIELD_PATH,
            where="config.values.plant.model_id",
        ),
        record.render_geometry.source.model_id,
        where="render_geometry.source.model_id",
        source=f"config.{PLANT_MODEL_ID_FIELD_PATH}",
    )

    tolerance_source = record.render_geometry.tolerance_source
    geometry = _authenticate_artifact(
        bound, "render_geometry.tolerance_source", tolerance_source.sha256, opened
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

    Both comparisons are taken on the parsed value and never on a binary64 conversion
    of it, for the reason `_require_numbers_equal` records: `float()` on a 401-digit
    integer literal raises a raw `OverflowError` instead of this row's named refusal,
    and Python compares an `int` against a `float` exactly. The conversion in the
    return is reached only after the value has been proved to lie between zero and the
    declared tolerance, which is itself a float, so it cannot overflow.
    """

    if isinstance(value, bool) or not isinstance(value, (int, float)):
        raise _refuse(
            X_IDENTITY_MISMATCH,
            f"the geometry validation artifact's maximum deviation is {value!r}, "
            "which is not a number",
        )
    if (isinstance(value, float) and not math.isfinite(value)) or value < 0:
        raise _refuse(
            X_IDENTITY_MISMATCH,
            f"the geometry validation artifact's maximum deviation is {value!r}; a "
            "maximum absolute deviation is a finite non-negative magnitude",
        )
    if value > tolerance:
        raise _refuse(
            X_IDENTITY_MISMATCH,
            f"the geometry validation artifact records a maximum deviation of "
            f"{value!r} m, which exceeds the declared tolerance {tolerance!r} m",
        )
    return float(value)


# --------------------------------------------------------------------------- #
# Step 6 -- the manifest, both dataset audits and the recomputed census.
# --------------------------------------------------------------------------- #
@dataclass(frozen=True)
class AuthenticatedDataset:
    """The manifest and both audits, digested before parsed, with one census.

    Attributes:
        rows: every manifest row, keyed by `run_id`, as read by
            `utils.storage_contract.parse_identity_manifest`.
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


def _require_count(value: Any, *, where: str) -> int:
    """Require one JSON integer that is not a boolean.

    Python's `bool` is a subclass of `int` and `True == 1`, so an equality taken
    without this guard accepts `true` wherever a count of one belongs. A census is
    six numbers and a document that reports one of them as a boolean is not the
    document the digest was taken over -- it is a differently shaped document that
    happens to compare equal.
    """

    if isinstance(value, bool) or not isinstance(value, int):
        raise _refuse(
            X_IDENTITY_MISMATCH,
            f"{where} is {value!r}, which is not a JSON integer count",
        )
    return value


def _require_census_agrees(audit_name: str, block: Any, census: Mapping[str, Any]) -> None:
    """Require one audit's `manifest_audit` block to echo the recomputed census.

    Every field is required to carry the JSON type the recomputed census carries
    **before** its value is compared, because Python equality across types is wider
    than agreement: `True == 1`, `False == 0`, and a census whose row count is `true`
    passes a bare `!=` against a manifest holding exactly one row.
    """

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
        trail = f"{audit_name}.{MANIFEST_AUDIT_KEY}.{field}"
        if field == "splits":
            if not isinstance(observed, Mapping):
                raise _refuse(
                    X_IDENTITY_MISMATCH, f"{trail} is {observed!r}, not an object"
                )
            observed = {
                key: _require_count(value, where=f"{trail}.{key}")
                for key, value in observed.items()
            }
        elif field == "suites":
            if not isinstance(observed, (list, tuple)):
                raise _refuse(
                    X_IDENTITY_MISMATCH, f"{trail} is {observed!r}, not an array"
                )
            for index, entry in enumerate(observed):
                if not isinstance(entry, str):
                    raise _refuse(
                        X_IDENTITY_MISMATCH,
                        f"{trail}[{index}] is {entry!r}, which is not a suite name",
                    )
            observed = list(observed)
            expected = list(expected)
        else:
            observed = _require_count(observed, where=trail)
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
    authenticated: AuthenticatedConfig,
) -> AuthenticatedDataset:
    """Run read-order step 6: authenticate the manifest and both dataset audits.

    Args:
        record: the authenticated record.
        bound: the result of `bind_root_domains`.
        sources: the result of step 5, for the established result's case identities.
        authenticated: the result of step 4. The dataset's own account of which
            configuration produced it is joined to the configuration this chain
            authenticated, rather than only to the record's echo of it.

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

    **The config identity is joined here, not merely echoed.** Both audits and every
    manifest row carry a `config_hash`, and requiring those to agree with each other
    while never comparing their common value against the configuration step 4
    validated leaves one state accepted that W6 forbids: a dataset internally
    consistent on one configuration, described by a record whose validated config,
    established result and payloads are on another. Every one of those files digests
    correctly, every echo agrees, and the two halves of the sentence are about
    different experiments. The join is also what the packet's own closed contract
    already requires one level down -- `utils.role_contract.RolePayloadLoader` refuses
    an index row whose `config_hash` is not the loaded config's -- so the manifest and
    the audits are held to the standard the role indexes were already held to.
    """

    # `authenticated_bytes` carries the presence guard for all three files, so there
    # is no second one here: a guard that no input can make decisive is the same
    # defect as a duplicated guard.
    manifest_path = bound.role_root / MANIFEST_NAME
    audit_paths = {name: bound.role_root / f"{name}.json" for name in AUDIT_NAMES}
    declared_audits = {
        "generation_audit": record.data_root.generation_audit,
        "independent_audit": record.data_root.independent_audit,
    }

    manifest_raw = authenticated_bytes(
        manifest_path,
        record.data_root.manifest_sha256,
        where="data_root.manifest_sha256",
        named_by=MANIFEST_NAME,
        code=X_ROLE_ABSENT,
        digest_of_bytes=external_bytes_digest,
    )
    audit_bytes: dict[str, bytes] = {
        name: authenticated_bytes(
            path,
            declared_audits[name].sha256,
            where=f"data_root.{name}.sha256",
            named_by=f"{name}.json",
            code=X_ROLE_ABSENT,
            digest_of_bytes=external_bytes_digest,
        )
        for name, path in audit_paths.items()
    }

    try:
        manifest_rows = parse_identity_manifest(manifest_raw, source=MANIFEST_NAME)
    except (StorageContractError, ValueError) as exc:
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

    rows_by_run = {row.run_id: row for row in manifest_rows}

    config_hash = authenticated.config.config_hash
    for name in AUDIT_NAMES:
        _require_strings_equal(
            audits[name].get("config_hash"),
            config_hash,
            where="the authenticated configuration",
            source=f"{name}.config_hash",
        )
    for run_id, row in rows_by_run.items():
        if row.config_hash != config_hash:
            raise _refuse(
                X_IDENTITY_MISMATCH,
                f"{MANIFEST_NAME} row {run_id!r} was generated under config_hash "
                f"{row.config_hash!r} but the authenticated configuration is "
                f"{config_hash!r}",
            )

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
            hash-checked against its authenticated index row and schema/semantically
            validated by `utils.role_contract.RolePayloadLoader`, from the exact bytes
            step 11 digested. Containment is step 3's and step 9's: the payload path
            was resolved under `--role-root` and then required to be exactly the path
            the authenticated index row names.
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
) -> Mapping[Path, bytes]:
    """Run read-order step 8: read and digest **every** named index before any parse.

    Args:
        record: the authenticated record.
        roots: the result of step 7.

    Returns:
        `index path -> the exact bytes that were digested`, one entry per distinct
        index. Step 9 parses *these* values, so the rows the chain plans from are the
        rows whose bytes this row authenticated.

    Raises:
        VerificationSceneError: `X_ROLE_ABSENT` when a named index cannot be read;
            `X_IDENTITY_MISMATCH` when any index digests differently from the
            `index_sha256` the record declares for it.

    Every index is read and digested before any is parsed, and that ordering is the
    row's whole content. Two arms of one case share a role root when the role is flat,
    so a distinct index may be named by several references; the file is read **once**
    and each reference's declared digest is compared against that one measurement, so
    a record that declared two different digests for one file refuses rather than
    silently taking the first -- and a second reference cannot occasion a second open
    of a file whose bytes are already the chain's.
    """

    raw_by_index: dict[Path, bytes] = {}
    digests: dict[Path, str] = {}
    for case in record.cases:
        for suite, arm in case.arms.items():
            for role, reference in arm.roles.items():
                index_path = roots[(case.case_id, suite, role)] / ROLE_INDEX_NAME
                if index_path not in raw_by_index:
                    raw_by_index[index_path] = _read_bytes(
                        index_path,
                        where=f"the {role} index at {index_path}",
                        code=X_ROLE_ABSENT,
                    )
                    digests[index_path] = external_bytes_digest(raw_by_index[index_path])
                _require_digest_equal(
                    index_path,
                    reference.index_sha256,
                    where=(
                        f"cases.{case.case_id}.arms.{suite}.roles.{role}.index_sha256"
                    ),
                    digest=digests[index_path],
                )
    return _frozen_mapping(raw_by_index)


def resolve_index_rows(
    record: ConnectionRecord,
    bound: BoundPaths,
    roots: Mapping[tuple[str, str, str], Path],
    index_bytes: Mapping[Path, bytes],
) -> tuple[
    Mapping[tuple[str, str, str], RoleIndexRow],
    Mapping[Path, tuple[RoleIndexRow, ...]],
]:
    """Run read-order step 9: parse the authenticated indexes and plan no other open.

    Returns:
        `(case_id, suite, role) -> the row that authorises that payload`, and
        `index path -> every row that index carries`. The second map exists because
        step 12 must hand `RolePayloadLoader` the rows parsed from the authenticated
        bytes rather than let it re-open the same pathname.

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

    **Nothing here re-opens an index.** `utils.storage_contract.parse_role_index` is
    the same parser and the same strict header as `read_role_index`, applied to the
    exact byte string step 8 digested, so the rows this function plans from are the
    rows step 8 authenticated -- not the rows a second open of the same pathname
    would have produced. A bracket around a path-based parser cannot state that: it
    detects a change that is still present when the parser returns and is blind to
    one made and reverted inside the call.
    """

    parsed: dict[Path, dict[str, RoleIndexRow]] = {}
    rows_by_index: dict[Path, tuple[RoleIndexRow, ...]] = {}
    rows: dict[tuple[str, str, str], RoleIndexRow] = {}
    for case in record.cases:
        for suite, arm in case.arms.items():
            for role in arm.roles:
                key = (case.case_id, suite, role)
                index_path = roots[key] / ROLE_INDEX_NAME
                if index_path not in parsed:
                    try:
                        index_rows = parse_role_index(
                            index_bytes[index_path],
                            observation=False,
                            source=f"the {role} index at {index_path}",
                        )
                    except (StorageContractError, ValueError) as exc:
                        raise _refuse(
                            X_IDENTITY_MISMATCH,
                            f"the {role} index at {index_path} did not parse: {exc}",
                        ) from exc
                    parsed[index_path] = {row.run_id: row for row in index_rows}
                    rows_by_index[index_path] = tuple(index_rows)
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
    return _frozen_mapping(rows), _frozen_mapping(rows_by_index)


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
) -> tuple[
    Mapping[tuple[str, str, str], bytes],
    Mapping[tuple[str, str], str],
]:
    """Run read-order step 11: read and digest every payload, digest every checkpoint.

    Returns:
        `(case_id, suite, role) -> the exact authenticated payload bytes`, and
        `(case_id, suite) -> the checkpoint's raw digest`. Step 12 interprets the
        first map, so the arrays rows 13 to 21 consume come from the byte string this
        row digested rather than from a later open of the same pathname.

    Raises:
        VerificationSceneError: `X_ROLE_ABSENT` when a named payload or checkpoint is
            not present; `X_IDENTITY_MISMATCH` when a digest disagrees with the record
            **or** with the authenticated index row.

    The payload digest is compared twice on purpose, and the two comparisons are not
    redundant. The record's declaration is what a reviewer approved; the index row is
    what the dataset itself asserts. A payload that matches one and not the other is
    exactly the state where the tree moved underneath an approved record, and a single
    comparison would leave whichever side it omitted unchecked. Both comparisons are
    made against **one** measurement over **one** read, so they are two statements
    about the same object rather than about two opens that happened to agree.

    **The checkpoint is digested from its path and that is deliberate.** Nothing in
    this lane interprets a checkpoint -- a `.pt` file is arbitrary code until something
    decides to deserialise it, and rows 13 to 21 never do -- so there is no second
    reading of it for a first reading to have to match, and holding an unbounded model
    file in memory to state a property nothing consumes would be cost with no claim
    attached.
    """

    payload_bytes: dict[tuple[str, str, str], bytes] = {}
    checkpoints: dict[tuple[str, str], str] = {}
    for case in record.cases:
        for suite, arm in case.arms.items():
            for role, reference in arm.roles.items():
                key = (case.case_id, suite, role)
                payload_path = bound.role_payloads[key]
                raw = _read_bytes(
                    payload_path,
                    where=f"cases.{case.case_id}.arms.{suite}.roles.{role} payload",
                    code=X_ROLE_ABSENT,
                )
                digest = external_bytes_digest(raw)
                _require_digest_equal(
                    payload_path,
                    reference.payload_sha256,
                    where=(
                        f"cases.{case.case_id}.arms.{suite}.roles.{role}.payload_sha256"
                    ),
                    digest=digest,
                )
                payload_bytes[key] = raw
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
    return _frozen_mapping(payload_bytes), _frozen_mapping(checkpoints)


def _read_only_array(array: np.ndarray) -> np.ndarray:
    """Return one authenticated payload array that cannot be written to.

    `ndarray.flags.writeable = False` alone is not enough, and the reason is worth
    stating where the code is: an array that owns its own buffer may have the flag set
    back to `True` by anyone holding it, so a "frozen" payload straight out of
    `np.load` is frozen only against accident. An array built over an immutable
    `bytes` object cannot be made writeable at all -- NumPy refuses, because the base
    it would have to write through is itself read-only. The copy costs one pass over
    the payload and buys the property the chain actually claims.

    `np.asarray` and not `np.ascontiguousarray`: the contiguous form is documented to
    return an array of at least one dimension, so it turns a zero-dimensional payload
    field into a one-element vector, and a freeze that changes a shape has changed the
    fact it was supposed to preserve -- after the loader validated that shape against
    the schema. `tobytes` already serialises any layout in C order, so the contiguous
    call bought nothing to offset it.
    """

    source = np.asarray(array)
    view = np.frombuffer(source.tobytes(), dtype=source.dtype)
    return view.reshape(source.shape)


def load_authenticated_payloads(
    record: ConnectionRecord,
    roots: Mapping[tuple[str, str, str], Path],
    authenticated: AuthenticatedConfig,
    rows_by_index: Mapping[Path, tuple[RoleIndexRow, ...]],
    payload_bytes: Mapping[tuple[str, str, str], bytes],
) -> Mapping[tuple[str, str, str], Mapping[str, np.ndarray]]:
    """Run read-order step 12: load exactly the authenticated payload set.

    Raises:
        VerificationSceneError: `X_IDENTITY_MISMATCH` when `RolePayloadLoader` refuses
            a payload's identity, path containment, schema or semantics.

    The loader is called rather than reimplemented (design 4.3): it re-derives the
    payload's digest and applies the key allowlist, the schema's dtype and shape
    declarations and the role's semantic checks. The adapter re-derives none of them.

    **The loader opens nothing here, and that is what closes the chain.** It is
    constructed from the index rows step 9 parsed out of the bytes step 8 digested,
    and it is handed the payload bytes step 11 read and digested. So its own hash
    check is a comparison between the byte string this chain authenticated and the
    `row.sha256` this chain authenticated -- not a comparison between two later opens
    of two pathnames, which is a statement about whatever those names resolved to at
    the moment each open happened. The rules stay the loader's: it validates the rows
    it is given exactly as it validates the rows it would have read, and it refuses a
    payload whose bytes do not digest to its row.

    **Path containment stays with the entry point that opens a path.** The row-grammar
    half -- one relative single-component `.npz` name, no traversal, no drive letter --
    is applied to the given rows at construction; the resolution half belongs to
    `RolePayloadLoader.load`, which is the entry point that resolves and opens. Step 9
    has separately required each row's `npz_path` to resolve to exactly the payload
    path step 3 contained under `--role-root`, so the file whose bytes step 11 read is
    the file the record declared and the index authorises.

    **What the payload map holds.** Each array is rebuilt over an immutable buffer, so
    the facts rows 13 to 21 consume cannot be edited after they were authenticated.

    **A scope statement rather than a defect**, recorded here so a later session does
    not rediscover it as one: a payload whose digest is exactly right but whose dtype or
    shape is wrong is not, in plain words, an identity mismatch, and none of the
    thirteen refusal codes fits it precisely. No fourteenth code is invented for it
    here; ruling Q1 forbade inventing a code for a branch nobody had built, and the row
    that builds the branch is the round entitled to propose splitting it.
    """

    loaders: dict[Path, AuthenticatedRolePayloadLoader] = {}
    payloads: dict[tuple[str, str, str], Mapping[str, np.ndarray]] = {}
    for case in record.cases:
        for suite, arm in case.arms.items():
            for role in arm.roles:
                key = (case.case_id, suite, role)
                directory = roots[key]
                if directory not in loaders:
                    try:
                        loaders[directory] = AuthenticatedRolePayloadLoader(
                            directory,
                            role,
                            authenticated.schema,
                            authenticated.config,
                            rows_by_index[directory / ROLE_INDEX_NAME],
                            suite=suite if role in SUITE_QUALIFIED_ROLES else None,
                        )
                    except (StorageContractError, ValueError) as exc:
                        raise _refuse(
                            X_IDENTITY_MISMATCH,
                            f"the {role} role root at {directory} did not open: {exc}",
                        ) from exc
                try:
                    payload = loaders[directory].load_bytes(
                        arm.run_id, payload_bytes[key]
                    )
                except (StorageContractError, KeyError, ValueError) as exc:
                    raise _refuse(
                        X_IDENTITY_MISMATCH,
                        f"the {role} payload for run {arm.run_id!r} did not load: {exc}",
                    ) from exc
                payloads[key] = _frozen_mapping(
                    {name: _read_only_array(array) for name, array in payload.items()}
                )
    return _frozen_mapping(payloads)


def authenticate_roles(
    record: ConnectionRecord,
    bound: BoundPaths,
    authenticated: AuthenticatedConfig,
    dataset: AuthenticatedDataset,
) -> AuthenticatedRoles:
    """Run read-order steps 7 through 12 in their normative order."""

    roots = require_role_layout(record, bound)
    index_bytes = authenticate_role_indexes(record, roots)
    index_rows, rows_by_index = resolve_index_rows(record, bound, roots, index_bytes)
    require_manifest_rows(record, dataset)
    payload_bytes, checkpoints = authenticate_payload_bytes(record, bound, index_rows)
    payloads = load_authenticated_payloads(
        record, roots, authenticated, rows_by_index, payload_bytes
    )
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
        record_sha256: the record identity this chain authenticated, carried because
            row 20 puts it on every scene's provenance block and a provenance
            identity a caller supplies at assembly time is an identity that can lie
            (invariant V7). It is the digest `load_connection_record` checked, not a
            second measurement of the path.
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
    record_sha256: str
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
    sources = authenticate_sources(record, bound, authenticated)
    dataset = authenticate_dataset(record, bound, sources, authenticated)
    roles = authenticate_roles(record, bound, authenticated, dataset)
    return AuthenticatedConnection(
        record=record,
        record_sha256=connection_record_sha256,
        bound=bound,
        expected_opens=expected_open_set(record, bound),
        config=authenticated,
        sources=sources,
        dataset=dataset,
        roles=roles,
    )


# --------------------------------------------------------------------------- #
# Steps 13-17 -- the cross-arm and cross-role facts, over the authenticated set.
#
# **What these five rows add, and what they deliberately do not restate.** Step 12
# ran every payload through `utils.role_contract`, whose `_semantic_role_checks`
# already establishes, *within one payload*: that a `labels` struct names a known
# source class with a non-empty subtype and a finite, non-negative onset; that an
# `estimator_outputs` payload carries at least one decision, that every row of it
# satisfies `utils.estimator.EstimatorOutput.validate`, and that its two decision
# axes are strictly increasing; and that a `controller_logs` payload's `step` is a
# non-empty contiguous 0-based grid whose `t_s` is strictly increasing and finite.
# None of that is repeated here. Rows 13 to 17 are exactly the facts a single
# payload cannot carry, because each one is a relation *between* two payloads:
#
#   * 13 -- the loaded set covers both arms of every case and nothing else;
#   * 14 -- the two arms describe **one** body change and replay **one** commanded
#     trajectory;
#   * 15 -- both arms' plant grids are the same grid, and every frame-bearing array
#     in both arms and in the controller role has that grid's length;
#   * 16 -- the decisions the adapter *carries forward* are ordered, stamped at
#     control steps this replay contains, and not timed after it ended;
#   * 17 -- the tracking block is a valid `utils.metrics.j_5s` call at the agreed
#     onset over the record's declared window.
#
# Row 16's per-decision `validate()` call is not a second copy of step 12's: it is
# applied to the `EstimatorOutput` values *this module constructs*, so what it holds
# is the adapter's own column-by-column construction, which step 12 cannot see.
# --------------------------------------------------------------------------- #
@dataclass(frozen=True)
class ArmSeries:
    """One suite's authenticated series, on the case's one playback grid.

    Attributes:
        suite: `C1` or `S`, the key this arm is filed under.
        run_id: the record's run identifier for this arm, carried so a later row
            can name the run a refusal is about without re-deriving it.
        q_true: `[T,2]` joint angles, one of row 18's two body inputs.
        deform_coords: `[T,n_def]` internal deformation coordinates, the other.
        task_reference: `[T,2]` commanded planar endpoint.
        true_task_output: `[T,2]` true deformed tip.
        decisions: the schema-D decisions in payload order, as live
            `utils.estimator.EstimatorOutput` values rather than a local mirror of
            their nine fields.
        controller_step: `[T]` the contiguous 0-based control-step grid.
        controller_t_s: `[T]` the controller's own clock. It is **never** compared
            to the playback grid: the one-control-interval offset a live loop
            produces is faithful real data, and two closed tests hold both
            conventions open (finding CI).
        controller_mode: `T` non-empty mode strings, bound to `controller_step`.

    Every array here is a reference to the read-only array step 12 built over an
    immutable buffer. Nothing is copied, and nothing downstream can edit a fact that
    was authenticated.
    """

    suite: str
    run_id: str
    q_true: np.ndarray
    deform_coords: np.ndarray
    task_reference: np.ndarray
    true_task_output: np.ndarray
    decisions: tuple[EstimatorOutput, ...]
    controller_step: np.ndarray
    controller_t_s: np.ndarray
    controller_mode: tuple[str, ...]


@dataclass(frozen=True)
class CaseSeries:
    """One menu entry's two arms, after rows 13 through 17 agreed about them.

    Attributes:
        case_id: the record's case identity.
        display_label: the record's menu label for it.
        pair_id: the pair both arms belong to. The record already required each
            arm's echoed manifest row to carry this same value at step 2, so this
            field carries it rather than re-establishing it.
        playback_t_s: the one grid both arms' `plant.t_s` agreed on.
        truth: the schema-D label struct both arms agreed on, as the live
            `utils.verification_scene.LabelFields`.
        window_s: the record's declared `analysis_window_s`, carried because it is
            the window row 17 established the tracking block over.
        arms: exactly `C1` and `S`.

    **The label struct's own value contract is step 12's, not this row's.** Whether a
    `subtype` is non-empty or an `onset_time_s` non-negative was settled by
    `utils.role_contract` before these bytes arrived, and whether the struct can be
    *drawn* honestly is `utils.verification_scene.validate_scene`'s, at the row that
    assembles a scene. Row 14 establishes only that the two arms agree, which is the
    one thing neither of those layers can see.
    """

    case_id: str
    display_label: str
    pair_id: str
    playback_t_s: np.ndarray
    truth: LabelFields
    window_s: float
    arms: Mapping[str, ArmSeries]


@dataclass(frozen=True)
class AuthenticatedCases:
    """Every case rows 13 through 17 agreed about, in record order.

    This value authorises nothing. It is the state row 18 -- the geometry
    derivation -- begins from, and it carries no cross-arm scalar of any kind
    (invariant W13): the adapter presents two arms side by side and computes no
    comparison between them.
    """

    cases: tuple[CaseSeries, ...]


def require_complete_arms(record: ConnectionRecord, roles: AuthenticatedRoles) -> None:
    """Run read-order step 13: the loaded set is exactly both arms of every case.

    Args:
        record: the authenticated record.
        roles: the payload set step 12 loaded.

    Raises:
        VerificationSceneError: `X_ARMS_INCOMPLETE` when a case does not carry
            exactly the two suites, when a named `(case, suite, role)` payload or a
            `(case, suite)` checkpoint is missing from the loaded set, or when the
            loaded set carries a key the record did not name.

    **This is a post-condition across a module boundary, and that is the whole
    reason it exists.** On the production path it cannot fail: `connection_record`
    parses `cases[*].arms` as a mapping whose keys are exactly `SUITE_KEYS` and
    `cases[*].arms[*].roles` as one whose keys are exactly `ROLE_NAMES`, so step 12
    can only ever have loaded the complete set. That guarantee lives in a *different
    module*, and a row that inherits it silently is a row that turns into a wrong
    picture rather than a refusal if that module's parse rule is ever relaxed. So the
    dependency is written down as a named refusal instead, and its test drives this
    function directly with a deficient set -- the same in-memory validator seam
    finding DD's repair used, and for the same reason: the state the guard refuses is
    one the production path is designed never to produce.

    The comparison is two-directional. A one-directional check would be satisfied by
    a loaded set that carried extra keys, and "the adapter loaded something the
    record did not name" is exactly the failure the section-4.2 allowlist exists to
    make impossible.
    """

    expected_payloads = {
        (case.case_id, suite, role)
        for case in record.cases
        for suite in SUITE_KEYS
        for role in ROLE_NAMES
    }
    expected_checkpoints = {
        (case.case_id, suite) for case in record.cases for suite in SUITE_KEYS
    }
    for case in record.cases:
        present = tuple(sorted(case.arms))
        if present != tuple(sorted(SUITE_KEYS)):
            raise _refuse(
                X_ARMS_INCOMPLETE,
                f"case {case.case_id!r} names the arms {present} rather than "
                f"exactly {tuple(sorted(SUITE_KEYS))}",
            )
    missing_payloads = sorted(expected_payloads - set(roles.payloads))
    if missing_payloads:
        raise _refuse(
            X_ARMS_INCOMPLETE,
            f"the loaded payload set is missing {missing_payloads}",
        )
    unnamed_payloads = sorted(set(roles.payloads) - expected_payloads)
    if unnamed_payloads:
        raise _refuse(
            X_ARMS_INCOMPLETE,
            f"the loaded payload set carries {unnamed_payloads}, which the record "
            f"did not name",
        )
    missing_checkpoints = sorted(expected_checkpoints - set(roles.checkpoint_sha256))
    if missing_checkpoints:
        raise _refuse(
            X_ARMS_INCOMPLETE,
            f"the authenticated checkpoint set is missing {missing_checkpoints}",
        )
    unnamed_checkpoints = sorted(set(roles.checkpoint_sha256) - expected_checkpoints)
    if unnamed_checkpoints:
        raise _refuse(
            X_ARMS_INCOMPLETE,
            f"the authenticated checkpoint set carries {unnamed_checkpoints}, which "
            f"the record did not name",
        )


def _label_scalars(payload: Mapping[str, np.ndarray]) -> dict[str, Any]:
    """Return one `labels` payload's eight fields as Python scalars.

    `numpy.ndarray.item()` is what converts each 0-d array to the Python type the
    schema declares -- `str` for the two unicode fields, `int`, `float` and `bool`
    for the rest -- so no per-field type table is written here and none can fall out
    of step with `LabelFields`.
    """

    return {name: np.asarray(payload[name]).item() for name in LABEL_FIELDS}


def require_pair_agreement(
    record: ConnectionRecord, roles: AuthenticatedRoles
) -> Mapping[str, LabelFields]:
    """Run read-order step 14: the two arms are one pair.

    Args:
        record: the authenticated record.
        roles: the payload set step 12 loaded.

    Returns:
        `case_id -> the agreed label struct`, built from the payloads rather than
        from the record: the record names *which* runs a case is made of, and the
        `labels` payload is where the body change itself is written.

    Raises:
        VerificationSceneError: `X_PAIR_MISMATCH` when any of the eight schema-D
            label fields differs between the arms, or when the two arms do not
            replay the same `task_reference`.

    **What this row does not check, because an earlier one already did.** The pair
    identity itself -- each arm's echoed `manifest_row.pair_id` equalling the case's
    `pair_id`, and each arm's `suite` and `split` equalling the ones it is filed
    under -- is settled at step 2 by `connection_record._parse_arm`, before any file
    is opened. Restating it here would be a branch no input can reach.

    **A deliberate consequence of the normative order.** Two arms whose plant
    payloads carry different frame counts have unequal `task_reference` arrays, so
    they refuse here as a pair mismatch rather than one row later as a timebase
    mismatch. That is the right code for it: the two arms are not replaying one
    commanded trajectory, which is what makes them a pair at all. Step 15 then binds
    the agreed grid to everything else.
    """

    truths: dict[str, LabelFields] = {}
    first_suite, second_suite = SUITE_KEYS
    for case in record.cases:
        scalars = {
            suite: _label_scalars(roles.payloads[(case.case_id, suite, "labels")])
            for suite in SUITE_KEYS
        }
        for name in LABEL_FIELDS:
            first = scalars[first_suite][name]
            second = scalars[second_suite][name]
            if first != second:
                raise _refuse(
                    X_PAIR_MISMATCH,
                    f"case {case.case_id!r} arms disagree about the body change: "
                    f"labels.{name} is {first!r} in {first_suite} and {second!r} "
                    f"in {second_suite}",
                )
        references = {
            suite: np.asarray(
                roles.payloads[(case.case_id, suite, "plant")]["task_reference"]
            )
            for suite in SUITE_KEYS
        }
        if not np.array_equal(references[first_suite], references[second_suite]):
            raise _refuse(
                X_PAIR_MISMATCH,
                f"case {case.case_id!r} arms do not replay one commanded "
                f"task_reference",
            )
        truths[case.case_id] = LabelFields(**scalars[first_suite])
    return _frozen_mapping(truths)


def bind_playback_timebase(
    record: ConnectionRecord, roles: AuthenticatedRoles
) -> Mapping[str, np.ndarray]:
    """Run read-order step 15: one playback grid, and everything bound to it.

    Args:
        record: the authenticated record.
        roles: the payload set step 12 loaded.

    Returns:
        `case_id -> the one playback grid` both arms agreed on.

    Raises:
        VerificationSceneError: `X_TIMEBASE_MISMATCH` when the two arms' `plant.t_s`
            are not the same array, when a frame-bearing plant array's leading axis
            is not the grid's length, or when a `controller_logs` axis is not.

    **Only the grid's rank is checked here, and that is deliberate** (finding CN).
    Whether it is uniform, monotonic, finite and long enough belongs to
    `utils.metrics.j_5s`, which step 17 calls; a copy of those rules here would
    pre-empt the delegation for exactly the shapes the delegation exists to cover,
    and would go stale the moment that function's preconditions changed.

    **`controller_t_s` is bound by shape and by nothing else.** It is never compared
    to the playback grid: `assignment_generator._step_index` makes a label's onset
    `onset_s / dt` while `cable_plant` stamps `t_s` *after* advancing, so a live
    controller clock sits one control interval later than the plant's and a
    comparison here would refuse faithful real data (finding CI).
    """

    playback: dict[str, np.ndarray] = {}
    first_suite, second_suite = SUITE_KEYS
    for case in record.cases:
        grids = {
            suite: np.asarray(roles.payloads[(case.case_id, suite, "plant")]["t_s"])
            for suite in SUITE_KEYS
        }
        grid = grids[first_suite]
        if grid.ndim != 1 or grid.shape[0] < 1:
            raise _refuse(
                X_TIMEBASE_MISMATCH,
                f"case {case.case_id!r} plant.t_s must be a non-empty "
                f"one-dimensional grid, got shape {grid.shape}",
            )
        if not np.array_equal(grid, grids[second_suite]):
            raise _refuse(
                X_TIMEBASE_MISMATCH,
                f"case {case.case_id!r} arms do not share one playback grid",
            )
        frames = int(grid.shape[0])
        for suite in SUITE_KEYS:
            plant = roles.payloads[(case.case_id, suite, "plant")]
            for name in PLANT_FRAME_ARRAYS:
                array = np.asarray(plant[name])
                if array.shape[0] != frames:
                    raise _refuse(
                        X_TIMEBASE_MISMATCH,
                        f"case {case.case_id!r} arm {suite} plant.{name} carries "
                        f"{array.shape[0]} frames against the playback grid's "
                        f"{frames}",
                    )
            controller = roles.payloads[(case.case_id, suite, "controller_logs")]
            step = np.asarray(controller["step"])
            if not np.array_equal(step, np.arange(frames)):
                raise _refuse(
                    X_TIMEBASE_MISMATCH,
                    f"case {case.case_id!r} arm {suite} controller_logs.step is not "
                    f"the contiguous 0-based grid of length {frames}",
                )
            for name in ("t_s", "controller_mode"):
                array = np.asarray(controller[name])
                if array.shape != (frames,):
                    raise _refuse(
                        X_TIMEBASE_MISMATCH,
                        f"case {case.case_id!r} arm {suite} controller_logs.{name} "
                        f"has shape {array.shape} against the playback grid's "
                        f"({frames},)",
                    )
        playback[case.case_id] = grid
    return _frozen_mapping(playback)


def resolve_decisions(
    record: ConnectionRecord,
    roles: AuthenticatedRoles,
    playback: Mapping[str, np.ndarray],
) -> Mapping[tuple[str, str], tuple[EstimatorOutput, ...]]:
    """Run read-order step 16: carry the decisions, ordered and inside the extent.

    Args:
        record: the authenticated record.
        roles: the payload set step 12 loaded.
        playback: step 15's `case_id -> playback grid`.

    Returns:
        `(case_id, suite) -> the decisions in payload order`, as live
        `utils.estimator.EstimatorOutput` values.

    Raises:
        VerificationSceneError: `X_DECISION_UNSUPPORTED` when a constructed decision
            does not satisfy the live schema-D contract, when the carried axes stop
            increasing, when a decision's `step` is not a control step of this
            replay, or when a decision is timed after the replay ended.

    **The `validate()` call holds this module's construction, not the payload.**
    Step 12 already drove every row of the payload through the same struct's
    `validate` inside `utils.role_contract`, so a bad *payload* cannot reach here.
    What can reach here is a bad *transcription* -- a column read at the wrong index,
    a whole array passed where one row belongs -- and that is a defect in this
    function that no earlier row can see.

    **The two axes are bounded differently, and the reason is the live producer's
    chronology rather than a reading of the phrase "inside the playback extent".**
    `utils.online_loop.run_online_rollout` iterates `step_index` over
    `range(n_steps)`, measures `decision_time_s` as the plant's clock **before** the
    step's advance, calls the policy, and only then advances; `utils.cable_plant`
    stamps each `PlantStepState.t_s` from the clock **after** that advance. So on a
    faithful trace of `T` control steps:

      * every estimator `step` is one of `0` through `T-1` -- it is literally the loop
        variable `EstimatorCommandPolicy` persists, and `schema/schema.json` gives
        the field the unit `control_step_index`; and
      * every `decision_time_s` lies one control interval *below* the playback
        sample of the same index, so the first decision is stamped `0.0 s` while
        `playback_t_s[0]` is one interval later.

    **The step axis is therefore bound to the control-step domain, and the time axis
    is bounded only above.** A `step` at or past `T` is a state the producer cannot
    emit, and refusing it is what makes the field's declared unit mean something. A
    lower bound on `decision_time_s` at `playback_t_s[0]` is the opposite: it refuses
    the one decision every faithful run necessarily emits. The non-negativity of both
    axes is already total, established inside the payload at step 12 and re-driven
    over this module's own transcription by the `validate()` call above, so this row
    adds no second comparison there -- a guard no input can reach is worse than none.

    **Containment above is compared with no tolerance.** A decision after the last
    playback sample has no frame to be drawn against, and refusing it is the
    fail-closed reading. The upper bound is deliberately *not* tightened to the
    per-decision pairing `decision_time_s <= playback_t_s[step]`: that would bind the
    estimator's clock to the plant's grid sample by sample, which is the class of
    binding finding CI forbids for `onset_index` and step 15 forbids for
    `controller_t_s`, both because a faithful producer offsets the axis.

    *This replaces the Session-149 reading, which bounded the time axis only and
    accepted `step == T`. Codex's Session-149 cross-review drove the live producer
    and showed that reading accepts a step no producer can emit while refusing the
    step-0 decision every producer does emit; the correction is recorded here rather
    than in the earlier session's files.* If a later artifact makes the estimator's
    cadence something other than the control-step grid, that is a change to the
    record design and belongs in an amendment.
    """

    resolved: dict[tuple[str, str], tuple[EstimatorOutput, ...]] = {}
    for case in record.cases:
        grid = playback[case.case_id]
        step_count = int(np.asarray(grid).shape[0])
        last_time = float(grid[-1])
        for suite in SUITE_KEYS:
            payload = roles.payloads[(case.case_id, suite, "estimator_outputs")]
            count = int(np.asarray(payload["step"]).shape[0])
            decisions: list[EstimatorOutput] = []
            previous_step = -1
            previous_time = -math.inf
            for index in range(count):
                decision = EstimatorOutput(
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
                    decision.validate()
                except ValueError as exc:
                    raise _refuse(
                        X_DECISION_UNSUPPORTED,
                        f"case {case.case_id!r} arm {suite} decision {index} as "
                        f"this adapter carried it violates the schema-D contract: "
                        f"{exc}",
                    ) from exc
                if (
                    decision.step <= previous_step
                    or decision.decision_time_s <= previous_time
                ):
                    raise _refuse(
                        X_DECISION_UNSUPPORTED,
                        f"case {case.case_id!r} arm {suite} carried decision axes "
                        f"that stopped increasing at index {index}",
                    )
                if decision.step >= step_count:
                    raise _refuse(
                        X_DECISION_UNSUPPORTED,
                        f"case {case.case_id!r} arm {suite} decision {index} is "
                        f"stamped at control step {decision.step}, which this "
                        f"replay of {step_count} control steps does not contain",
                    )
                if decision.decision_time_s > last_time:
                    raise _refuse(
                        X_DECISION_UNSUPPORTED,
                        f"case {case.case_id!r} arm {suite} decision {index} at "
                        f"t={decision.decision_time_s} s is timed after the replay "
                        f"ended at {last_time} s",
                    )
                previous_step = decision.step
                previous_time = decision.decision_time_s
                decisions.append(decision)
            resolved[(case.case_id, suite)] = tuple(decisions)
    return _frozen_mapping(resolved)


def require_tracking_window(
    record: ConnectionRecord,
    roles: AuthenticatedRoles,
    playback: Mapping[str, np.ndarray],
    truths: Mapping[str, LabelFields],
) -> None:
    """Run read-order step 17: establish the window by **calling** `j_5s`.

    Args:
        record: the authenticated record, whose `analysis_window_s` is the window.
        roles: the payload set step 12 loaded.
        playback: step 15's `case_id -> playback grid`.
        truths: step 14's `case_id -> agreed label struct`, whose `onset_time_s` is
            the onset the window opens at.

    Raises:
        VerificationSceneError: `X_WINDOW_UNSUPPORTED` carrying whatever
            `utils.metrics.j_5s` refused.

    The metric is called and its refusal re-raised; its rules are not copied. That is
    the same shape `verification_scene._validate_tracking_window` already has, and it
    is what finding CN bought: a later change to that function's preconditions cannot
    leave a stale duplicate of them behind in this module.

    **The returned integral is deliberately discarded.** Invariant W13 says the
    adapter carries no cross-arm scalar; computing `J` for both arms and keeping it
    would be the beginning of one. What this row establishes is that the window
    *exists* over this grid at this onset -- that the onset sample is present and the
    window is not truncated -- so the surface can draw the tracking block honestly.

    The onset is taken from the agreed label struct and never from `onset_index`.
    `assignment_generator._step_index` makes the label's onset `onset_s / dt` while
    `cable_plant` stamps `t_s` after advancing, so in real data
    `plant.t_s[onset_index]` is one control interval later than `onset_time_s`, and
    indexing the grid by it would move the window (finding CI).
    """

    window_s = float(record.analysis_window_s)
    for case in record.cases:
        grid = playback[case.case_id]
        onset_time_s = float(truths[case.case_id].onset_time_s)
        for suite in SUITE_KEYS:
            plant = roles.payloads[(case.case_id, suite, "plant")]
            try:
                j_5s(
                    grid,
                    plant["task_reference"],
                    plant["true_task_output"],
                    onset_time_s,
                    window_s=window_s,
                )
            except ValueError as exc:
                raise _refuse(
                    X_WINDOW_UNSUPPORTED,
                    f"case {case.case_id!r} arm {suite} is not a valid "
                    f"utils.metrics.j_5s call at onset {onset_time_s} s over a "
                    f"{window_s} s window: {exc}",
                ) from exc


def resolve_cases(connection: AuthenticatedConnection) -> AuthenticatedCases:
    """Run read-order rows 13 through 17 in their normative order.

    Args:
        connection: everything rows 1 through 12 established.

    Returns:
        The `AuthenticatedCases` row 18 begins from.

    Raises:
        VerificationSceneError: carrying the code the failing row of section 4.1
            names -- `X_ARMS_INCOMPLETE`, `X_PAIR_MISMATCH`, `X_TIMEBASE_MISMATCH`,
            `X_DECISION_UNSUPPORTED` or `X_WINDOW_UNSUPPORTED`.

    The order is the contract, exactly as it is for rows 1 through 12, and for the
    same reason: an order a caller can reassemble is not an order. Nothing here opens
    a file. Every fact it reads was authenticated before it arrived, which is why
    these five rows can be pure functions over the loaded set.
    """

    record = connection.record
    roles = connection.roles
    require_complete_arms(record, roles)
    truths = require_pair_agreement(record, roles)
    playback = bind_playback_timebase(record, roles)
    decisions = resolve_decisions(record, roles, playback)
    require_tracking_window(record, roles, playback, truths)

    window_s = float(record.analysis_window_s)
    cases: list[CaseSeries] = []
    for case in record.cases:
        arms: dict[str, ArmSeries] = {}
        for suite in SUITE_KEYS:
            plant = roles.payloads[(case.case_id, suite, "plant")]
            controller = roles.payloads[(case.case_id, suite, "controller_logs")]
            arms[suite] = ArmSeries(
                suite=suite,
                run_id=case.arms[suite].run_id,
                q_true=plant["q_true"],
                deform_coords=plant["deform_coords"],
                task_reference=plant["task_reference"],
                true_task_output=plant["true_task_output"],
                decisions=decisions[(case.case_id, suite)],
                controller_step=controller["step"],
                controller_t_s=controller["t_s"],
                controller_mode=tuple(
                    str(mode) for mode in controller["controller_mode"]
                ),
            )
        cases.append(
            CaseSeries(
                case_id=case.case_id,
                display_label=case.display_label,
                pair_id=case.pair_id,
                playback_t_s=playback[case.case_id],
                truth=truths[case.case_id],
                window_s=window_s,
                arms=_frozen_mapping(arms),
            )
        )
    return AuthenticatedCases(cases=tuple(cases))


# --------------------------------------------------------------------------- #
# Step 18 -- the centerline derivation, one arm at a time.
#
# **This row owns exactly two things, and it owns them because nothing earlier
# can.** It derives each arm's planar centerline from the authenticated `q_true`
# and `deform_coords` under the geometry the *record* declares, and it requires the
# derived distal point to agree with the authenticated `true_task_output` to within
# the tolerance read-order step 5 already proved equal to the named field of the
# authenticated geometry-validation artifact. Every payload involved was
# authenticated at step 12 and every declared field at steps 2 and 5; what has
# never been established until here is that the two *agree* -- that the body the
# payload describes and the chain the record declares are one body.
#
# **The derivation is not written here and its refusals are not translated here.**
# `utils.centerline_geometry` owns the map, owns the closed convention vocabularies
# and raises `X_GEOMETRY_UNSUPPORTED` itself, so this row is a call and not a copy
# -- the same shape row 17 has against `utils.metrics.j_5s`, and for the same
# reason finding CN bought there: a second statement of a rule is a statement that
# can go stale while still looking authoritative.
#
# **Nothing is re-checked that an earlier row established, and the omissions are
# deliberate rather than accidental** (the rule the rows-13-17 build settled). The
# derivation refuses a `q_true` of the wrong rank or width, a `deform_coords` on a
# different grid, a non-finite entry and a declared triplet column the payload does
# not carry. On the path through this function none of those is reachable: step 12
# ran both arrays through the schema's own role contract, and step 15 bound every
# frame-bearing plant array's leading axis to the one playback grid. The reachable
# refusals here are the record-level ones -- a derivation version, joint convention
# or projection this adapter does not implement -- and the distal comparison, which
# is the only refusal that is about a particular arm and the only place this row
# names one.
# --------------------------------------------------------------------------- #
@dataclass(frozen=True)
class ArmGeometry:
    """One arm's derived centerline and the agreement it actually achieved.

    Attributes:
        suite: `C1` or `S`.
        centerline: the `[T, N, 2]` scene-frame centerline, read-only. `N` is a
            property of the declared chain -- one point at the proximal end of
            every ordered body across every link, plus the distal point -- and
            `utils.centerline_geometry.centerline_point_count` is the one place
            that number is derived.
        distal_deviation_m: the measured maximum over steps of the distance
            between the derived distal point and the recorded `true_task_output`.

    **The deviation is carried rather than discarded because a number a reader can
    see is worth more than a boolean.** "The geometry check passed" and "the
    geometry agreed to 0.0 m against a declared tolerance of 1e-9 m" are the same
    outcome and a very different piece of evidence, and the second is what lets a
    later row put the agreement on the scene instead of asserting it in prose.
    """

    suite: str
    centerline: np.ndarray
    distal_deviation_m: float


@dataclass(frozen=True)
class CaseGeometry:
    """One menu entry's two derived centerlines.

    Attributes:
        case_id: the record's case identity.
        arms: exactly `C1` and `S`.

    It carries no cross-arm scalar (invariant W13). The two arms' deviations sit
    side by side and this module computes no comparison between them: an adapter
    that reported "S agreed better than C1" would be doing the analysis the
    verification artifact exists to let a reader do for themselves.
    """

    case_id: str
    arms: Mapping[str, ArmGeometry]


@dataclass(frozen=True)
class AuthenticatedGeometry:
    """Every case's derived geometry, in record order.

    Attributes:
        tolerance_m: the record's declared `distal_tolerance_m`, carried because it
            is the number every deviation above was measured against and a reader of
            this value should not have to return to the record to find it.
        cases: one `CaseGeometry` per record case, in record order.

    This value authorises nothing. It is the state rows 19 through 21 -- the
    provenance decision, the bundle assembly and the write -- begin from.
    """

    tolerance_m: float
    cases: tuple[CaseGeometry, ...]


def resolve_geometry(
    connection: AuthenticatedConnection, cases: AuthenticatedCases
) -> AuthenticatedGeometry:
    """Run read-order step 18: derive each arm's centerline and check its distal point.

    Args:
        connection: everything rows 1 through 12 established. The record's
            `render_geometry` is taken from here rather than from a caller, so the
            geometry applied is the authenticated one by construction.
        cases: the result of rows 13 through 17, whose `ArmSeries` carry the
            authenticated `q_true`, `deform_coords` and `true_task_output`.

    Returns:
        The `AuthenticatedGeometry` rows 19 through 21 begin from.

    Raises:
        VerificationSceneError: `X_GEOMETRY_UNSUPPORTED`, raised by
            `utils.centerline_geometry` and **passed through untouched** -- neither
            its code nor its message is rewritten here. Catching each refusal to
            prefix it with the arm it came from would put this module in the
            business of reformatting another module's diagnosis, and the one
            refusal that genuinely varies by arm is reached through
            `require_distal_point_within_tolerance`, which takes the arm's name as
            an argument and names it itself.

    **The tolerance comes from the record and from nowhere else.** It is
    `render_geometry.distal_tolerance_m`, which step 5 required to equal the field
    the record's `tolerance_source` names inside the authenticated
    geometry-validation artifact, and whose recorded maximum deviation step 5
    separately required not to exceed it. This row supplies no default and holds no
    constant of its own: `utils.centerline_geometry.CENTERLINE_TASK_OUTPUT_TOL_M`
    measures a *fixture generator's* construction exactness, and reusing it here
    would demand that two different computations of the same geometry agree to a
    nanometre on real data (design finding CU). Sub-step 4b chooses no real-data
    tolerance.

    **The derived arrays are made read-only before they are carried.** The
    derivation allocates a fresh array and hands ownership to its caller, so
    freezing it is this module's job rather than the derivation's, and it is the
    rule every authenticated array in this adapter already travels under: nothing
    downstream can edit a fact that was established here.
    """

    geometry = connection.record.render_geometry
    tolerance_m = float(geometry.distal_tolerance_m)
    resolved: list[CaseGeometry] = []
    for case in cases.cases:
        arms: dict[str, ArmGeometry] = {}
        for suite in SUITE_KEYS:
            arm = case.arms[suite]
            centerline = derive_centerline(arm.q_true, arm.deform_coords, geometry)
            deviation_m = require_distal_point_within_tolerance(
                centerline,
                arm.true_task_output,
                tolerance_m,
                where=f"case {case.case_id!r} arm {suite}",
            )
            arms[suite] = ArmGeometry(
                suite=suite,
                centerline=_read_only_array(centerline),
                distal_deviation_m=deviation_m,
            )
        resolved.append(CaseGeometry(case_id=case.case_id, arms=_frozen_mapping(arms)))
    return AuthenticatedGeometry(tolerance_m=tolerance_m, cases=tuple(resolved))


# --------------------------------------------------------------------------- #
# Step 19 -- the provenance state, computed and then required to equal `authority`.
#
# **This row computes; it does not accept.** Design property 3.3.3 and frozen
# invariant V7 both say the same thing: a caller may not supply provenance, because
# a caller-supplied label is a label that can lie. The record's `authority` is not
# an exception to that -- it is a *constraint on the outcome*, and this row is where
# the constraint is checked against a state derived from the authenticated facts.
#
# **What this row does not restate, and who owns each piece instead.** Row 3 already
# refuses a `DEVELOPMENT_ONLY` record whose split is not `dev` and a `FINAL` record
# whose split is `dev` (`_require_authority_split_policy`), and binds the
# authority's mechanically fixed output parent. Row 4 already refuses a
# `DEVELOPMENT_ONLY` record naming a frozen config, one whose `config_hash` lacks
# the `dev-` prefix, one that does not forbid confirmatory payloads, and a `FINAL`
# record naming a draft config or a `config_hash` carrying a `dev-` trace
# (`require_authority_config_policy`). Row 6 already binds every manifest row's
# `config_hash` to the authenticated config's, so a development trace in the
# manifest implies one in the config and is caught two rows earlier.
#
# **What is left is exactly one identity, and it is reachable.** The dataset's
# `assignment_hash` is checked at row 6 for agreement -- record against both audits,
# and the two audits against each other -- and nowhere for what it *says*. A
# delivered research root records the assignment that produced it, and this
# project's assignments carry the `dev-` prefix while the config freeze is blocked.
# So a record claiming `FINAL`, naming a frozen clean config, a non-`dev` split and
# a dataset whose audits both honestly echo a `dev-` assignment passes rows 1
# through 18 today: every digest agrees, every echo agrees, and the scene would
# carry a `FINAL RESULT INPUTS` banner over data generated under a development
# assignment. That is the exact input set invariant W6 asks for, and it is what this
# row refuses.
# --------------------------------------------------------------------------- #

#: The prefix every development-lane identity in this project carries. It is the
#: same string `require_authority_config_policy` tests the config hash against, and
#: it is a project-wide convention rather than this module's invention: the standing
#: rule is that no `dev-` trace may enter confirmatory analysis.
DEVELOPMENT_TRACE_PREFIX = "dev-"


@dataclass(frozen=True)
class ResolvedProvenance:
    """The provenance state this adapter computed, and what it computed it from.

    Attributes:
        state: `DEVELOPMENT_ONLY` or `FINAL`. `SYNTHETIC_FIXTURE` is never computed
            here: it is the private assembly seam's state, supplied by the
            construction path that never opens a connection record at all, and a
            public invocation that could resolve to it would be a public path able
            to disclaim its own inputs.
        development_traces: the authenticated identities carrying a development
            trace, each as `name -> value`, in a fixed order. It is carried rather
            than reduced to a boolean because the refusal has to be able to say
            *which* identity disagreed with the claimed authority, and because a
            later row puts the resolved state on the scene beside the evidence for
            it.

    This value authorises nothing. A resolved `FINAL` state means the authenticated
    bytes carry no development trace; the exact-state approval of the config, the
    review of the record and the two transcript authorization halves are separate
    social gates in sub-steps 4c through 4e and none of them is a runtime fact.
    """

    state: str
    development_traces: Mapping[str, str]


def resolve_provenance(connection: AuthenticatedConnection) -> ResolvedProvenance:
    """Run read-order step 19: compute the provenance state and bind it to `authority`.

    Args:
        connection: everything rows 1 through 12 established. The identities are
            taken from here rather than from a caller, so the state is computed from
            the authenticated bytes by construction.

    Returns:
        The `ResolvedProvenance` rows 20 and 21 begin from.

    Raises:
        VerificationSceneError: `X_PROVENANCE_UNRESOLVED` when the computed state is
            not the `authority` the record claims.

    **The computation is total over the two public states and its inputs are named.**
    A development trace in any authenticated identity, or a `dev` split, computes
    `DEVELOPMENT_ONLY`; their joint absence computes `FINAL`. There is no third
    outcome and no default: an input this function cannot classify would be a state
    the surface could draw without having decided what it is a picture of.

    **Three of the four inputs are already decisive earlier, and that is written
    down rather than hidden.** Under `DEVELOPMENT_ONLY` the split is `dev` by row 3
    and the config hash carries the prefix by row 4, so the computation cannot
    return anything else and the equality below is a post-condition -- the same
    shape row 13 has, and named the same way. The one input that can move the answer
    on its own is the dataset assignment, checked at row 6 for agreement and never
    for content. The refusal names every trace it found, not the first, because a
    record whose dataset *and* whose config both disagree with a claimed `FINAL` is
    a different report from one where only the dataset does.
    """

    record = connection.record
    candidates: tuple[tuple[str, str], ...] = (
        ("config.config_hash", connection.config.config.config_hash),
        (
            "data_root.generation_audit.assignment_hash",
            record.data_root.generation_audit.assignment_hash,
        ),
        (
            "data_root.independent_audit.assignment_hash",
            record.data_root.independent_audit.assignment_hash,
        ),
    )
    traces = {
        name: value
        for name, value in candidates
        if DEVELOPMENT_TRACE_PREFIX in value
    }
    state = (
        DEVELOPMENT_ONLY
        if traces or record.split == "dev"
        else FINAL
    )
    if state != record.authority:
        detail = (
            ", ".join(f"{name} = {value!r}" for name, value in traces.items())
            if traces
            else f"split = {record.split!r}"
        )
        raise _refuse(
            X_PROVENANCE_UNRESOLVED,
            f"the record claims authority {record.authority} but this adapter "
            f"computed {state} from its authenticated identities: {detail}",
        )
    return ResolvedProvenance(state=state, development_traces=_frozen_mapping(traces))


# --------------------------------------------------------------------------- #
# Step 20 -- the bundle assembly, and the one comparison it exists to make.
#
# **What this row adds, and what it deliberately delegates.** Rows 13 through 19
# established the facts; this row is where they become the object the two surfaces
# draw. Four of its five checks are relations between *separately produced* values
# -- the record's menu, `resolve_cases`' output, `resolve_geometry`'s output, the
# established result's declared case list, and the provenance state `resolve_provenance`
# returned -- and that is exactly the class of fault no earlier row can see, because
# each earlier row saw only its own output. The fifth is `validate_bundle`, the
# surface gate both surfaces run as the first statement of their own entry points,
# called here so a bundle that no surface would draw never leaves this module.
#
# **The provenance check is the one that guards a claim rather than a shape**, and it
# runs before any scene exists. Every other value crossing this seam is checked
# against another authenticated value of the same kind; the provenance state is
# checked against the record's `authority` because the state *is* the banner, and a
# banner nothing compares is a sentence the surface prints on the strength of whoever
# built the argument list.
#
# **One check is deliberately absent and the reason is written down rather than
# left to be rediscovered.** The interactive surface exposes cases through a
# `display label -> case_id` mapping, and it would be natural to require that
# mapping to be a bijection over the menu. It always is: `validate_bundle` already
# refuses duplicate labels, and a duplicate label is the only way `dict(zip(...))`
# can lose a case. A guard no input can make decisive is the same defect as no guard
# at all (lesson 242), so the exposure property is held where it is decidable --
# label uniqueness, in the surface gate -- and not restated here.
# --------------------------------------------------------------------------- #
def _arm_identity(case: Case, suite: str) -> ArmIdentity:
    """Return one arm's provenance identities, taken from the authenticated record.

    Every value is the record's own declaration, which rows 2, 6, 8, 10 and 11
    already bound to the bytes on disk. Nothing is re-measured here: a second
    measurement at assembly time would be a second document, and the identities a
    reader is shown must be the ones the chain authenticated.
    """

    arm = case.arms[suite]
    return ArmIdentity(
        run_id=arm.run_id,
        pair_id=case.pair_id,
        checkpoint_relative_path=str(arm.checkpoint.relative_path),
        checkpoint_sha256=arm.checkpoint.sha256,
        role_index_sha256=tuple(
            (role, arm.roles[role].index_sha256) for role in ROLE_NAMES
        ),
        role_payload_sha256=tuple(
            (role, arm.roles[role].payload_sha256) for role in ROLE_NAMES
        ),
    )


def _provenance_for(
    connection: AuthenticatedConnection, case: Case, state: str
) -> Provenance:
    """Return the provenance block this connection produces for one case.

    Args:
        connection: everything rows 1 through 12 established.
        case: the record's own entry for the case being described.
        state: row 19's resolved provenance state.

    Returns:
        The `Provenance` every scene of this case must carry.

    **This is one function because two rows need the same object, and the second one
    needs it as a comparand.** Row 20 puts it on every scene it assembles; row 21
    receives the assembled bundle as a *separately constructible value* and requires
    the scene it is about to publish to carry exactly this. Building the comparand
    from the code that builds the original is what makes that comparison total: a
    field added here is compared there without anyone remembering to add it, which is
    the failure mode a hand-listed field set has and this does not.

    Nothing is measured here. Every value is an identity rows 1 through 12 already
    bound to the bytes on disk, and `state` is row 19's own result.
    """

    return Provenance(
        state=state,
        connection_record_id=connection.record.record_label,
        connection_record_sha256=connection.record_sha256,
        config_identity=connection.config.config.config_hash,
        config_sha256=connection.config.config_sha256,
        split=connection.record.split,
        roles_read=tuple(ROLE_NAMES),
        arms=_frozen_mapping(
            {suite: _arm_identity(case, suite) for suite in SUITE_KEYS}
        ),
    )


def _scene_for(
    connection: AuthenticatedConnection,
    case: Case,
    series: CaseSeries,
    geometry: CaseGeometry,
    state: str,
) -> VerificationScene:
    """Assemble exactly one scene from what rows 13 through 19 established.

    The centerline comes from row 18, every series array from rows 13 through 17,
    every identity from the authenticated record, and the provenance state from row
    19. This function takes no value from a caller that is not one of those, which
    is invariant V7 at the assembly seam: there is no keyword through which a caller
    can relabel what it returns.
    """

    arms = {
        suite: SceneArm(
            suite=suite,
            centerline_xy=geometry.arms[suite].centerline,
            decisions=series.arms[suite].decisions,
            tracking=Tracking(
                task_reference=series.arms[suite].task_reference,
                true_task_output=series.arms[suite].true_task_output,
                window_s=series.window_s,
            ),
            controller_step=series.arms[suite].controller_step,
            controller_t_s=series.arms[suite].controller_t_s,
            controller_mode=series.arms[suite].controller_mode,
        )
        for suite in SUITE_KEYS
    }
    return VerificationScene(
        bundle_version=BUNDLE_VERSION,
        provenance=_provenance_for(connection, case, state),
        body_change=BodyChange(
            case_id=series.case_id,
            label=series.display_label,
            change=series.truth,
        ),
        playback_t_s=series.playback_t_s,
        arms=_frozen_mapping(arms),
        truth=series.truth,
        thresholds=Thresholds(
            abstain_threshold=connection.record.thresholds.abstain_threshold,
            unknown_threshold=connection.record.thresholds.unknown_threshold,
        ),
    )


def resolve_bundle(
    connection: AuthenticatedConnection,
    cases: AuthenticatedCases,
    geometry: AuthenticatedGeometry,
    provenance: ResolvedProvenance,
) -> VerificationBundle:
    """Run read-order step 20: assemble the menu and bind it to the established result.

    Args:
        connection: everything rows 1 through 12 established.
        cases: the result of rows 13 through 17.
        geometry: the result of row 18.
        provenance: the result of row 19.

    Returns:
        The validated `VerificationBundle` row 21 writes.

    Raises:
        VerificationSceneError: `X_PROVENANCE_UNRESOLVED` when the supplied
            provenance state is not the authenticated record's own `authority`;
            `X_BUNDLE_INCOMPLETE` when the three case sequences are not one
            sequence, when the assembled menu is not the case list the established
            result declares, or when a scene's arm identities are not the record's
            own; and whatever code `validate_bundle` names for a menu no surface may
            draw.

    **The four inputs are produced by four separate calls, and that is what makes
    this row's checks decidable.** `resolve_cases`, `resolve_geometry` and
    `resolve_provenance` each take the connection and return their own value; a
    caller assembling them is a caller who can pair the geometry of one record with
    the series of another. So the case identities and their order are required to
    agree across the record's menu, the series and the geometry before a single
    scene is built. That is the same post-condition-across-a-seam shape rows 13 and
    19 carry, and it is stated here rather than trusted because the seam is real.

    **The provenance state crosses that same seam, and it is the one value on it a
    reader is shown as a claim about the whole scene.** `provenance` is a separately
    constructible value: a caller can build a `ResolvedProvenance` this connection
    never produced, and `_scene_for` puts its `state` on every scene's provenance
    block as the banner the surface draws. Nothing downstream can see that the label
    and the record disagree, because by then the label is the only statement of the
    fact. So the state is bound back to the authenticated record's `authority`
    **before the first scene is built**. That is not a second copy of row 19's rule:
    row 19 computes a state from the authenticated identities and requires *its own
    result* to equal the authority; this row requires *the value it was handed* to
    be that same authority, which is a statement about the seam rather than about
    the computation, and the two separate exactly when a caller substitutes.
    `SYNTHETIC_FIXTURE` is refused here as a consequence rather than as a special
    case: `utils.connection_record` admits only `DEVELOPMENT_ONLY` and `FINAL` as an
    `authority`, so no authenticated record can ever make that equality hold, and a
    public connection-record invocation therefore cannot resolve to the private
    seam's state (invariant V7).

    **The established result is the authority on which cases the surface presents,
    and this is its second appearance rather than a repeat of its first.** Row 6
    compared the established result's case list against the *record's menu*. This
    row compares it against the *assembled bundle*, which is a different object: an
    assembly that dropped, duplicated or reordered a case would pass row 6 and fail
    here. The comparison is ordered, because menu order is bundle order and the
    order a reader is shown is part of what the prior read established.
    """

    if provenance.state != connection.record.authority:
        raise _refuse(
            X_PROVENANCE_UNRESOLVED,
            f"the assembly was handed provenance state {provenance.state!r} but the "
            f"authenticated record's authority is "
            f"{connection.record.authority!r}; the banner every scene carries is "
            "the record's own resolved state and never a value supplied beside it",
        )

    declared = tuple(case.case_id for case in connection.record.cases)
    series_ids = tuple(series.case_id for series in cases.cases)
    geometry_ids = tuple(entry.case_id for entry in geometry.cases)
    if series_ids != declared or geometry_ids != declared:
        raise _refuse(
            X_BUNDLE_INCOMPLETE,
            f"the record's menu names cases {list(declared)}, the resolved series "
            f"names {list(series_ids)} and the derived geometry names "
            f"{list(geometry_ids)}; one connection has one menu",
        )
    if declared != tuple(connection.sources.established_cases):
        raise _refuse(
            X_BUNDLE_INCOMPLETE,
            f"the assembled menu is {list(declared)} but the established result "
            f"declares {list(connection.sources.established_cases)}; the surface "
            "presents exactly the cases the prior read established, in that order",
        )

    scenes: dict[str, VerificationScene] = {}
    for case, series, entry in zip(connection.record.cases, cases.cases, geometry.cases):
        scenes[case.case_id] = _scene_for(
            connection, case, series, entry, provenance.state
        )
    bundle = VerificationBundle(
        bundle_version=BUNDLE_VERSION,
        provenance_state=provenance.state,
        scenes=_frozen_mapping(scenes),
    )
    validate_bundle(bundle)

    for case in connection.record.cases:
        identities = bundle.scenes[case.case_id].provenance.arms
        for suite in SUITE_KEYS:
            if identities[suite].run_id != case.arms[suite].run_id:
                raise _refuse(
                    X_BUNDLE_INCOMPLETE,
                    f"case {case.case_id!r} arm {suite} is presented as run "
                    f"{identities[suite].run_id!r} but the record names "
                    f"{case.arms[suite].run_id!r}",
                )
            if identities[suite].pair_id != case.pair_id:
                raise _refuse(
                    X_BUNDLE_INCOMPLETE,
                    f"case {case.case_id!r} arm {suite} is presented under pair "
                    f"{identities[suite].pair_id!r} but the record names "
                    f"{case.pair_id!r}",
                )
    return bundle


# --------------------------------------------------------------------------- #
# Step 21 -- the exclusive create, the declared write set, and nothing else.
# --------------------------------------------------------------------------- #

#: The two fixed bundle filenames, selected from the contract module's pinned tuple
#: **by suffix rather than by position**, so a later reordering of that tuple cannot
#: silently swap the document for its digest file. The tuple itself is pinned against
#: the tracked Step-3 figure set by equality in `utils.connection_record`.
BUNDLE_JSON_NAME = next(name for name in BUNDLE_FILE_NAMES if name.endswith(".json"))
BUNDLE_DIGEST_NAME = next(
    name for name in BUNDLE_FILE_NAMES if name.endswith(".sha256")
)

#: The resolution design section 4.7 requires of every case figure.
REQUIRED_FIGURE_DPI = 300

#: The eight bytes every PNG begins with, and the `pHYs` unit byte that means metres.
_PNG_SIGNATURE = b"\x89PNG\r\n\x1a\n"
_PNG_PHYS_CHUNK = b"pHYs"
_PNG_PHYS_METRE_UNIT = 1

#: The chunk that ends a PNG datastream, the fixed body length the format gives
#: `pHYs`, and the twelve bytes every chunk spends on its own length, type and CRC.
_PNG_IEND_CHUNK = b"IEND"
_PNG_PHYS_BODY_BYTES = 9
_PNG_CHUNK_OVERHEAD_BYTES = 12

#: The two chunks that make a datastream an *image* rather than a container carrying a
#: resolution: the header the format requires first, and the image data itself. A
#: `pHYs` chunk inside a byte string with neither is a resolution nobody rendered
#: anything at, which is Codex's Session-154 finding 3.
_PNG_IHDR_CHUNK = b"IHDR"
_PNG_IDAT_CHUNK = b"IDAT"
_PNG_IHDR_BODY_BYTES = 13

#: The format's own colour-type table: how many samples each pixel carries, and which
#: bit depths that colour type is defined for. A pair outside this table is not an
#: under-specified image, it is not an image -- which is why the table is the check
#: rather than a decoder's willingness to guess (Codex's Session-155 finding 2).
_PNG_COLOUR_TYPES: Mapping[int, tuple[int, tuple[int, ...]]] = MappingProxyType(
    {
        0: (1, (1, 2, 4, 8, 16)),
        2: (3, (8, 16)),
        3: (1, (1, 2, 4, 8)),
        4: (2, (8, 16)),
        6: (4, (8, 16)),
    }
)

#: The one compression method and the one filter method the format defines, the two
#: interlace methods it defines, and the largest dimension it permits.
_PNG_COMPRESSION_METHOD = 0
_PNG_FILTER_METHOD = 0
_PNG_INTERLACE_METHODS = (0, 1)
_PNG_MAX_DIMENSION = 2**31 - 1

#: Adam7, as the format states it: seven passes, each `(x_start, y_start, x_step,
#: y_step)`. It is here so the expected raw size of an interlaced image can be derived
#: rather than excused; matplotlib writes non-interlaced files, and a check that simply
#: skipped the interlaced case would be a hole shaped like a legal PNG.
_PNG_ADAM7_PASSES = (
    (0, 0, 8, 8),
    (4, 0, 8, 8),
    (0, 4, 4, 8),
    (2, 0, 4, 4),
    (0, 2, 2, 4),
    (1, 0, 2, 2),
    (0, 1, 1, 2),
)

#: Metres per inch. The `pHYs` chunk counts pixels per metre, so this is what turns a
#: declared DPI into the integer the file must carry.
_METRES_PER_INCH = 0.0254


@dataclass(frozen=True)
class WrittenBundle:
    """Exactly what read-order step 21 published, and where.

    Attributes:
        output_root: the exclusively created `<output-dir>/<record_label>/`.
        file_names: every file written, sorted, relative to that root.
        bundle_sha256: the digest of the bundle document's bytes **as they are on
            disk**, re-measured here rather than taken from the renderer's report.
        cases: the case ids the published menu presents, in published order.
        figure_dpi: the resolution every case figure declares in its own `pHYs`
            chunk, which this row required to equal the renderer's declaration and
            `REQUIRED_FIGURE_DPI`.
    """

    output_root: Path
    file_names: tuple[str, ...]
    bundle_sha256: str
    cases: tuple[str, ...]
    figure_dpi: int


def _png_header_fields(body: bytes, *, where: str) -> dict[str, int]:
    """Return one PNG header's fields, refusing every value the format does not define.

    Args:
        body: the thirteen bytes of the `IHDR` chunk, already bounded and CRC-checked
            by the walk that calls this.
        where: the file's name, for the refusal message.

    Returns:
        `width`, `height`, `bit_depth`, `colour_type` and `interlace`.

    Raises:
        VerificationSceneError: `X_BUNDLE_INCOMPLETE` when either dimension is zero or
            larger than the format permits; when the colour type is not one of the five
            the format defines; when the bit depth is not one that colour type is
            defined for; or when the compression, filter or interlace method is not one
            the format defines.

    **A header is not a formality here, because the resolution is read out of a file
    this row calls a figure.** Codex's Session-155 review drove a zero-width `IHDR`
    through the previous walk and it returned `(11811, 11811)` while a strict decoder
    refused the same bytes; my own re-drive widened that to a zero *height*, to a
    colour type the format does not define, and to a compression method it does not
    define -- and that last one is the case worth keeping, because a lenient decoder
    *accepted* it. **So the standard applied here is the format, not a decoder's
    willingness to guess**: a decoder that renders something is not evidence that what
    it rendered is what the file declared.

    The dimensions are also what makes the image-data length check downstream possible
    at all, which is why they are validated before that check rather than beside it.
    """

    width = int.from_bytes(body[0:4], "big")
    height = int.from_bytes(body[4:8], "big")
    bit_depth = body[8]
    colour_type = body[9]
    compression = body[10]
    filter_method = body[11]
    interlace = body[12]
    for name, value in (("width", width), ("height", height)):
        if value < 1 or value > _PNG_MAX_DIMENSION:
            raise _refuse(
                X_BUNDLE_INCOMPLETE,
                f"{where} declares an image {name} of {value}; the format requires "
                f"1 to {_PNG_MAX_DIMENSION}, and a figure with no pixels in it is not "
                "a figure saved at any resolution",
            )
    if colour_type not in _PNG_COLOUR_TYPES:
        raise _refuse(
            X_BUNDLE_INCOMPLETE,
            f"{where} declares colour type {colour_type}; the format defines only "
            f"{sorted(_PNG_COLOUR_TYPES)}",
        )
    if bit_depth not in _PNG_COLOUR_TYPES[colour_type][1]:
        raise _refuse(
            X_BUNDLE_INCOMPLETE,
            f"{where} declares bit depth {bit_depth} for colour type {colour_type}, "
            f"which the format defines only for {list(_PNG_COLOUR_TYPES[colour_type][1])}",
        )
    if compression != _PNG_COMPRESSION_METHOD:
        raise _refuse(
            X_BUNDLE_INCOMPLETE,
            f"{where} declares compression method {compression}; the format defines "
            f"only {_PNG_COMPRESSION_METHOD}",
        )
    if filter_method != _PNG_FILTER_METHOD:
        raise _refuse(
            X_BUNDLE_INCOMPLETE,
            f"{where} declares filter method {filter_method}; the format defines only "
            f"{_PNG_FILTER_METHOD}",
        )
    if interlace not in _PNG_INTERLACE_METHODS:
        raise _refuse(
            X_BUNDLE_INCOMPLETE,
            f"{where} declares interlace method {interlace}; the format defines only "
            f"{list(_PNG_INTERLACE_METHODS)}",
        )
    return {
        "width": width,
        "height": height,
        "bit_depth": bit_depth,
        "colour_type": colour_type,
        "interlace": interlace,
    }


def _png_expected_raw_bytes(
    *, width: int, height: int, bit_depth: int, colour_type: int, interlace: int
) -> int:
    """Return the exact size of one PNG's decompressed image data, in bytes.

    Args:
        width: the header's declared image width, in pixels.
        height: the header's declared image height, in pixels.
        bit_depth: the header's declared bits per sample.
        colour_type: the header's declared colour type, already known to the table.
        interlace: 0 for no interlacing, 1 for Adam7.

    Returns:
        The number of bytes a conforming encoder produces before compression: for each
        scanline of each pass, one filter-type byte plus the packed samples of that
        scanline. Passes with no pixels contribute nothing, which is the reason each
        pass is summed rather than the total being divided.

    **This is a derivation, not a bound, and that is what makes it an instrument.** A
    length check that only required "some" decompressed data would accept a zlib stream
    carrying three bytes for a 4x4 image; requiring the exact figure means the
    compressed stream has to describe an image of the size the header declares. The
    arithmetic is the format's own, so nothing here is pinned to a magic number.
    """

    samples = _PNG_COLOUR_TYPES[colour_type][0]
    passes = (
        ((0, 0, 1, 1),) if interlace == 0 else _PNG_ADAM7_PASSES
    )
    total = 0
    for x_start, y_start, x_step, y_step in passes:
        pass_width = (width - x_start + x_step - 1) // x_step
        pass_height = (height - y_start + y_step - 1) // y_step
        if pass_width <= 0 or pass_height <= 0:
            continue
        stride = (pass_width * samples * bit_depth + 7) // 8
        total += pass_height * (1 + stride)
    return total


def _png_pixels_per_metre(raw: bytes, *, where: str) -> tuple[int, int]:
    """Return one PNG's declared `(x, y)` resolution in pixels per metre.

    Args:
        raw: the complete file bytes.
        where: the file's name, for the refusal message.

    Returns:
        The `pHYs` chunk's two axis resolutions.

    Raises:
        VerificationSceneError: `X_BUNDLE_INCOMPLETE` when the bytes do not begin with
            the PNG signature; when the file ends inside a chunk header or inside a
            chunk body a header declared; when any chunk's CRC-32 does not cover the
            bytes it is written beside; when the datastream does not begin with a
            single `IHDR` chunk of the fixed length the format gives it; when it
            carries no `IDAT` chunk, or carries them non-consecutively; when the
            `pHYs` chunk does not precede the image data; when the sequence does not
            end at a zero-length `IEND` chunk with nothing after it; when there is no
            `pHYs` chunk or more than one; when that chunk is not the nine bytes the
            format fixes; when its unit is not metres; when the header declares a
            dimension, colour type, bit depth, compression method, filter method or
            interlace method the format does not define; when the `IDAT` run is not a
            zlib stream, does not end inside the run, or carries bytes after the
            stream ends; or when that stream does not decompress to exactly the number
            of bytes the declared image is.

    **The walk is total, and it is total because the alternative is a raw exception.**
    Codex's Session-153 review drove two inputs through the previous version: a figure
    whose `pHYs` CRC had been corrupted was *accepted* as 300-DPI evidence, and a
    `pHYs` header declaring nine bytes over a one-byte body escaped as an `IndexError`
    rather than this row's named refusal. Both are the same fault -- a parser that
    indexes into bytes it has not proved are there, and believes a chunk it has not
    proved is intact. So every chunk is now bounded before it is read and checked
    before it is believed, and the structure is walked to its end rather than
    abandoned at the first tag that matches.

    **The chunk is still located by walking rather than by searching**, because the
    four bytes `pHYs` may legitimately occur inside a compressed image stream and a
    search would find that first. What is new is that the walk cannot be steered off
    the end of the file by a length nobody bounded, and that a chunk whose CRC does
    not cover its own bytes is not evidence of the resolution it states -- a decoder
    is entitled to discard such a chunk, so this row must not accept it.

    **Exactly one `pHYs` chunk is permitted.** Two of them disagreeing would make the
    figure's declared DPI a function of which one a reader's decoder happened to keep,
    and returning the first would be this row making that choice on the reader's
    behalf.

    *** AND CHUNK INTEGRITY IS NOT IMAGE STRUCTURE, WHICH IS THE OTHER HALF OF THE
    CLAIM. *** Codex's Session-154 review built a byte string of validly CRC'd chunks
    carrying the signature, one `pHYs` and `IEND` -- no `IHDR`, no `IDAT`, no image at
    all -- and the previous version of this walk returned `(11811, 11811)` for it while
    a strict decoder refused the same bytes outright. My own re-drive found two more of
    the same family: a header with no image data behind it, and a `pHYs` chunk written
    *after* the image data, which the format forbids precisely because a decoder that
    has already begun rendering cannot honour it. **The row's claim is not that a byte
    string contains a resolution chunk; it is that a case figure is a PNG saved at 300
    DPI**, so the walk now also requires the mandatory structure that claim rests on: a
    single `IHDR` first at its fixed length, at least one `IDAT`, the `IDAT` run
    unbroken, `pHYs` before it, and a zero-length `IEND` last. That is enforced here
    rather than delegated to a decoder because a decoder is a dependency this packet
    does not declare, and because the walk was already visiting every chunk -- the
    structure was the part it was not asserting.

    *** AND PRESENT, ORDERED CHUNKS ARE STILL NOT A DECODABLE IMAGE, WHICH IS CODEX'S
    SESSION-155 FINDING 2 AND THE LAST STEP OF THE SAME ARGUMENT. *** A zero-width
    `IHDR` and an `IDAT` body reading `not-a-zlib-stream` both crossed the Session-154
    walk at `(11811, 11811)` while a strict decoder refused both; my re-drive widened
    that to a zero *height*, an undefined colour type, an undefined compression method
    and a zlib-valid stream carrying three bytes for a sixteen-pixel image. **The claim
    is that the published file is a figure saved at 300 DPI, so the walk now settles
    the whole of it**: `_png_header_fields` refuses every header value the format does
    not define, and the `IDAT` run must decompress to *exactly* the byte count
    `_png_expected_raw_bytes` derives from that header. The one case worth carrying is
    the undefined compression method, because a lenient decoder **accepted** it: the
    standard here is the format, and a decoder that renders something is not evidence
    that what it rendered is what the file declared.

    *** THE DECOMPRESSION GOES THROUGH A `decompressobj` RATHER THAN THROUGH
    `zlib.decompress`, AND THAT IS FORCED RATHER THAN STYLISTIC. *** Measured while
    writing this repair: `zlib.decompress(zlib.compress(body) + b"GARBAGE")` returns
    `body` and raises nothing, so the one-call form cannot tell a compressed image from
    a compressed image with something appended to it. The object form exposes `eof` and
    `unused_data`, which is how this row requires the image data to be **the whole of
    the IDAT run rather than a prefix of it**. Nobody reported this one; it came out of
    asking what else could make the claim false, which is lesson 287's own procedure
    applied by the owner before a reviewer applies it.
    """

    if not raw.startswith(_PNG_SIGNATURE):
        raise _refuse(
            X_BUNDLE_INCOMPLETE,
            f"{where} does not begin with the PNG signature, so the declared "
            "300-DPI figure is not a PNG at all",
        )
    offset = len(_PNG_SIGNATURE)
    resolution: tuple[int, int] | None = None
    chunk_index = 0
    image_data_seen = False
    image_data_closed = False
    image_data: list[bytes] = []
    header: dict[str, int] = {}
    while True:
        if offset + _PNG_CHUNK_OVERHEAD_BYTES > len(raw):
            raise _refuse(
                X_BUNDLE_INCOMPLETE,
                f"{where} ends {len(raw) - offset} bytes into a chunk header at byte "
                f"{offset}; a chunk is at least {_PNG_CHUNK_OVERHEAD_BYTES} bytes, and "
                "a truncated figure is not evidence of the resolution it was saved at",
            )
        length = int.from_bytes(raw[offset : offset + 4], "big")
        kind = raw[offset + 4 : offset + 8]
        end = offset + _PNG_CHUNK_OVERHEAD_BYTES + length
        if end > len(raw):
            raise _refuse(
                X_BUNDLE_INCOMPLETE,
                f"{where} declares a {length}-byte {kind!r} chunk at byte {offset} but "
                f"only {len(raw) - offset - _PNG_CHUNK_OVERHEAD_BYTES} bytes of body "
                "remain; the file is truncated",
            )
        body = raw[offset + 8 : offset + 8 + length]
        if zlib.crc32(kind + body) != int.from_bytes(raw[end - 4 : end], "big"):
            raise _refuse(
                X_BUNDLE_INCOMPLETE,
                f"{where} carries a {kind!r} chunk at byte {offset} whose CRC-32 does "
                "not cover its own bytes, so the chunk is corrupt and a decoder is "
                "entitled to discard it",
            )
        if chunk_index == 0:
            if kind != _PNG_IHDR_CHUNK:
                raise _refuse(
                    X_BUNDLE_INCOMPLETE,
                    f"{where} opens with a {kind!r} chunk; every PNG datastream opens "
                    "with IHDR, and a resolution declared inside something that is not "
                    "an image is not evidence a figure was saved at that resolution",
                )
            if length != _PNG_IHDR_BODY_BYTES:
                raise _refuse(
                    X_BUNDLE_INCOMPLETE,
                    f"{where} carries an IHDR chunk of {length} bytes; the format "
                    f"fixes it at {_PNG_IHDR_BODY_BYTES}",
                )
            header = _png_header_fields(body, where=where)
        elif kind == _PNG_IHDR_CHUNK:
            raise _refuse(
                X_BUNDLE_INCOMPLETE,
                f"{where} carries a second IHDR chunk at byte {offset}; a PNG "
                "datastream describes one image once",
            )
        if kind == _PNG_IDAT_CHUNK:
            if image_data_closed:
                raise _refuse(
                    X_BUNDLE_INCOMPLETE,
                    f"{where} resumes its image data at byte {offset} after another "
                    "chunk interrupted it; the format requires the IDAT run to be "
                    "consecutive, and a decoder is entitled to stop at the break",
                )
            image_data_seen = True
            image_data.append(body)
        elif image_data_seen:
            image_data_closed = True
        if kind == _PNG_IEND_CHUNK and length != 0:
            raise _refuse(
                X_BUNDLE_INCOMPLETE,
                f"{where} ends with an IEND chunk carrying {length} bytes; the format "
                "fixes it as empty",
            )
        if kind == _PNG_PHYS_CHUNK:
            if resolution is not None:
                raise _refuse(
                    X_BUNDLE_INCOMPLETE,
                    f"{where} carries more than one pHYs chunk; which resolution the "
                    "figure declares would then depend on which one a reader's decoder "
                    "kept",
                )
            if image_data_seen:
                raise _refuse(
                    X_BUNDLE_INCOMPLETE,
                    f"{where} declares its resolution at byte {offset}, after its "
                    "image data has begun; the format requires pHYs to precede IDAT, "
                    "and a decoder that has already started rendering is entitled to "
                    "ignore it",
                )
            if length != _PNG_PHYS_BODY_BYTES:
                raise _refuse(
                    X_BUNDLE_INCOMPLETE,
                    f"{where} carries a pHYs chunk of {length} bytes; the format "
                    f"fixes it at {_PNG_PHYS_BODY_BYTES}",
                )
            unit = body[8]
            if unit != _PNG_PHYS_METRE_UNIT:
                raise _refuse(
                    X_BUNDLE_INCOMPLETE,
                    f"{where} declares its resolution in unit {unit} rather than in "
                    "metres, so no DPI can be read from it",
                )
            resolution = (
                int.from_bytes(body[0:4], "big"),
                int.from_bytes(body[4:8], "big"),
            )
        offset = end
        chunk_index += 1
        if kind == _PNG_IEND_CHUNK:
            break
    if offset != len(raw):
        raise _refuse(
            X_BUNDLE_INCOMPLETE,
            f"{where} carries {len(raw) - offset} bytes after its IEND chunk; the "
            "figure is the datastream itself and not a container something else was "
            "appended to",
        )
    if not image_data_seen:
        raise _refuse(
            X_BUNDLE_INCOMPLETE,
            f"{where} carries no IDAT chunk, so it holds no image; a resolution "
            "declared over nothing is not evidence of a rendered figure",
        )
    stream = zlib.decompressobj()
    try:
        decompressed = stream.decompress(b"".join(image_data)) + stream.flush()
    except zlib.error as exc:
        raise _refuse(
            X_BUNDLE_INCOMPLETE,
            f"{where} carries an IDAT run that is not a zlib stream ({exc}); the "
            "format compresses image data with zlib, so bytes that do not decompress "
            "are not the image the resolution is claimed for",
        ) from exc
    if not stream.eof:
        raise _refuse(
            X_BUNDLE_INCOMPLETE,
            f"{where} carries an IDAT run whose zlib stream never ends; the image data "
            "is the whole of the run rather than a prefix of it",
        )
    if stream.unused_data:
        raise _refuse(
            X_BUNDLE_INCOMPLETE,
            f"{where} carries {len(stream.unused_data)} bytes in its IDAT run after "
            "the zlib stream ends; a decoder stops at the end of the stream, so those "
            "bytes are not image data and this file is not the figure it claims to be",
        )
    expected_raw = _png_expected_raw_bytes(
        width=header["width"],
        height=header["height"],
        bit_depth=header["bit_depth"],
        colour_type=header["colour_type"],
        interlace=header["interlace"],
    )
    if len(decompressed) != expected_raw:
        raise _refuse(
            X_BUNDLE_INCOMPLETE,
            f"{where} decompresses to {len(decompressed)} bytes of image data, but "
            f"the {header['width']}x{header['height']} image its header declares at "
            f"bit depth {header['bit_depth']} and colour type {header['colour_type']} "
            f"is {expected_raw} bytes; the compressed stream does not describe the "
            "image the header describes",
        )
    if resolution is None:
        raise _refuse(
            X_BUNDLE_INCOMPLETE,
            f"{where} carries no pHYs chunk, so it does not state the resolution "
            f"section 4.7 requires it to have been saved at",
        )
    return resolution


def _require_one_packet_root(connection: AuthenticatedConnection) -> Path:
    """Return the one packet root every packet-relative path in this chain sits under.

    Args:
        connection: everything rows 1 through 12 established.

    Returns:
        `connection.bound.packet_root`, resolved, once it has been shown to be the root
        the authenticated packet-relative paths were actually resolved against.

    Raises:
        VerificationSceneError: `X_PROVENANCE_UNRESOLVED` when the bound record path is
            not the one packet-relative location section 3.1 gives a record under that
            root; when the schema, the configuration or any named source artifact
            resolves outside it; when any of those paths is one the section-4.2
            allowlist row 3 derived does not name; when the allowlist itself names a
            path outside the root; or when the file at the bound record path is not,
            on disk, the record whose digest rows 1 and 2 authenticated.

    **This exists because `BoundPaths` is one value and therefore moves as one.**
    Row 21's destination check re-derives the publication root from
    `connection.bound.packet_root`, and Codex's Session-154 review pointed out that the
    root and the destination are two fields of the same substitutable object: replacing
    *both* coherently moves the derived expectation with the substitution, and the
    check that catches a moved parent catches nothing at all. Measured before this was
    written: with every authenticated record, config, source, dataset and role path
    left pointing into the real packet tree, a substituted `packet_root` and a matching
    `output_root` published the whole set beneath an unrelated temporary directory.

    **So the anchor cannot be a field of the value under suspicion, and this is the one
    invariant W8 already names.** W8 says one root governs every packet-relative
    resolution in the read order -- the step-3 domain binding, the step-4 schema and
    config, the step-5 source artifacts and the section-4.7 output parent. A
    substitution that moves the root without moving what the root resolved is a chain
    with *two* roots, which is exactly what W8 forbids, and it is decidable here from
    values whose bytes rows 1 through 5 actually read. The record path is compared by
    equality rather than by containment because section 3.1 gives a record one location
    and finding CX is about a record presented from somewhere else inside the same
    tree; the remaining paths are compared by containment because their positions are
    the record's to declare.

    *** AND EVERY ANCHOR INSIDE THE VALUE IS EXACTLY ONE SUBSTITUTION WIDER, WHICH IS
    CODEX'S SESSION-155 FINDING 1 AND THE END OF A THREE-SESSION PATTERN. *** The
    Session-153 repair anchored the provenance block to the connection; Session 154
    moved `output_root` and defeated it. The Session-154 repair anchored `output_root`
    to `packet_root`; Session 155 moved both and defeated it. This helper's first
    version anchored `packet_root` to `record_path` -- and `record_path` is a field of
    the same `BoundPaths`, so moving the whole packet-relative set together defeated it
    in turn. **Measured before this was written**: with `packet_root`, `output_root`,
    `record_path`, `schema_path`, `config_path` and every `packet_artifacts` value
    moved coherently to a temporary tree that *did not exist*, all eight files
    published beneath it.

    **The regress terminates at bytes that were actually read, and nowhere before
    that.** Any field of a separately constructible value can be replaced coherently
    with its neighbours, so a check that consults only such fields can always be
    widened by one more substitution; that is the shape of all three findings. The
    claim this helper supports -- that one root holds the packet this chain
    authenticated -- is a claim about the filesystem, and it is settled by looking:
    `external_digest(record_path)` must equal `connection.record_sha256`, the digest
    the CLI authorization named and `load_connection_record` checked. There is no
    in-memory field that closes this, and the two earlier repairs failing the same way
    is the evidence for that rather than an assumption about it.

    **The allowlist is checked first because it costs no I/O and it is the sharper
    message.** `expected_opens` is derived at row 3 from the bound record, so it is a
    second witness to the paths this chain resolved, and a substitution that moves
    `bound` alone leaves it naming the authenticated tree. It does not *terminate* the
    regress -- it can be substituted too -- which is precisely why the digest check
    below it is not optional.

    **This helper therefore opens exactly one file, and that is disclosed rather than
    hidden.** It is the record, which section 4.2's allowlist already names and rows 1
    and 2 already read; it is opened before row 21 creates anything;
    `test_row21_opens_nothing_outside_the_tree_it_created` states the widened property
    and bounds it to this one path.

    **A whole tree moved together is not what this refuses.** Copying a complete packet
    and running the chain against the copy leaves every one of these paths under the
    copy's root, *and the record's bytes are there too* -- so the digest check passes,
    which is the accept side landing exactly where W8 says it should. What is refused
    is a root that claims to govern paths it does not contain.
    """

    packet_root = Path(connection.bound.packet_root).resolve()
    expected_record = packet_root.joinpath(
        *record_relative_path(connection.record.record_label).parts
    ).resolve()
    observed_record = Path(connection.bound.record_path).resolve()
    if observed_record != expected_record:
        raise _refuse(
            X_PROVENANCE_UNRESOLVED,
            f"the packet root {packet_root} does not hold the authenticated record, "
            f"which is bound at {observed_record} while that root would place it at "
            f"{expected_record}; one connection is resolved against one packet root, "
            "and a root that does not contain the record it authenticated cannot fix "
            "where the publication goes",
        )
    named: list[tuple[str, Path]] = [
        ("the schema", Path(connection.bound.schema_path)),
        ("the configuration", Path(connection.bound.config_path)),
    ]
    named.extend(
        (f"the source artifact {key}", Path(value))
        for key, value in connection.bound.packet_artifacts.items()
    )
    for where, path in named:
        resolved = path.resolve()
        if packet_root not in resolved.parents:
            raise _refuse(
                X_PROVENANCE_UNRESOLVED,
                f"{where} is bound at {resolved}, which is outside the packet root "
                f"{packet_root} this chain claims to have run under; the read order "
                "resolves every packet-relative path against one root",
            )
    allowed = {Path(path).resolve() for path in connection.expected_opens}
    for where, path in [("the connection record", observed_record), *named]:
        resolved = Path(path).resolve()
        if resolved not in allowed:
            raise _refuse(
                X_PROVENANCE_UNRESOLVED,
                f"{where} is bound at {resolved}, which the allowlist row 3 derived "
                "from this record does not name; the paths this chain resolved and the "
                "paths it was permitted to open are the same paths",
            )
    for path in sorted(allowed):
        if packet_root not in path.parents and not _is_under(path, connection.bound):
            raise _refuse(
                X_PROVENANCE_UNRESOLVED,
                f"the allowlist row 3 derived names {path}, which is neither inside "
                f"the packet root {packet_root} nor under the role or checkpoint root "
                "this chain was given; one connection resolves against one packet",
            )
    try:
        measured = external_digest(observed_record)
    except OSError as exc:
        raise _refuse(
            X_PROVENANCE_UNRESOLVED,
            f"the record bound at {observed_record} could not be read ({exc}); a "
            "packet root that does not hold the record this chain authenticated is "
            "not the root it ran under",
        ) from exc
    if measured != connection.record_sha256:
        raise _refuse(
            X_PROVENANCE_UNRESOLVED,
            f"the record bound at {observed_record} hashes to {measured}, not the "
            f"authenticated {connection.record_sha256}; the packet root this chain "
            "publishes under is the root that holds the record it authenticated, and "
            "that is decided by the bytes on disk rather than by the paths beside them",
        )
    return packet_root


def _is_under(path: Path, bound: BoundPaths) -> bool:
    """Say whether one allowlisted path sits under the role or checkpoint root.

    Args:
        path: a resolved member of the section-4.2 allowlist.
        bound: the bound paths, for the two machine-selected roots.

    Returns:
        True when the path is inside `role_root` or `checkpoint_root`.

    **The role and checkpoint roots are machine-selected and deliberately not
    packet-relative** -- the dataset is git-ignored and lives wherever the director put
    it, which is why `--role-root` and `--checkpoint-root` are CLI arguments at all. So
    the allowlist legitimately reaches outside the packet for exactly those two trees,
    and the containment sweep above has to say so rather than refuse every real
    connection. W8 governs *packet-relative* resolution; it has never governed these.
    """

    for root in (Path(bound.role_root).resolve(), Path(bound.checkpoint_root).resolve()):
        if root == path or root in path.parents:
            return True
    return False


def _authority_output_root(connection: AuthenticatedConnection) -> Path:
    """Return the one destination this connection's authenticated identities fix.

    Args:
        connection: everything rows 1 through 12 established.

    Returns:
        `<packet-root>/<authority output parent>/<record_label>/`, resolved.

    Raises:
        VerificationSceneError: `X_PROVENANCE_UNRESOLVED` when that path does not
            resolve to somewhere inside the packet root the chain ran under -- a
            junction or symlink at any component of the output parent would otherwise
            put the publication physically outside the packet while every string in
            the comparison still looked right.

    **This re-derives what row 3 already bound, and that is not a second copy of row
    3's rule.** `BoundPaths` reaches this row as a *separately constructible value*:
    a caller can hand row 21 a connection whose `output_root` no row bound, and the
    previous version of this check compared only that path's basename, so a correct
    label under a wrong parent was accepted and populated (Codex's Session-153
    review). Row 3 states a rule about an *argument*; this states the same rule about
    the *value that arrives here*, and the two separate exactly when a caller
    substitutes. The derivation uses only the authenticated authority, the
    authenticated record label and the one packet root invariant W8 names.

    *** AND THE PACKET ROOT IS ITSELF A FIELD OF THAT SAME SUBSTITUTABLE VALUE, WHICH
    IS CODEX'S SESSION-154 FINDING 2. *** Deriving the destination from
    `bound.packet_root` catches a moved destination only while the root stays put;
    moving both together moves the expectation with them. `_require_one_packet_root`
    is what makes the derivation mean something -- it establishes, from the paths whose
    bytes rows 1 through 5 read, that this root is the root those paths were resolved
    against.
    """

    packet_root = _require_one_packet_root(connection)
    parent = OUTPUT_PARENTS[connection.record.authority]
    candidate = packet_root.joinpath(
        *parent.parts, connection.record.record_label
    ).resolve()
    if packet_root not in candidate.parents:
        raise _refuse(
            X_PROVENANCE_UNRESOLVED,
            f"the {connection.record.authority} publication root resolves to "
            f"{candidate}, which is outside the packet root {packet_root} the chain "
            "ran under",
        )
    return candidate


def write_bundle(
    connection: AuthenticatedConnection,
    bundle: VerificationBundle,
    *,
    render: Callable[[VerificationBundle, Path], Mapping[str, Any]],
) -> WrittenBundle:
    """Run read-order step 21: create the output root exclusively and publish the set.

    Args:
        connection: everything rows 1 through 12 established. It supplies the
            destination, the menu, and every identity the published scenes must carry.
        bundle: the validated menu row 20 returned. It arrives as a separately
            constructible value, so it is bound back to `connection` before anything
            is created.
        render: the scripted figure writer, injected rather than imported. See below.

    Returns:
        A `WrittenBundle` describing exactly what is now on disk.

    Raises:
        VerificationSceneError: `X_PROVENANCE_UNRESOLVED` when the bound output root
            is not the destination this connection's own authority and record label
            fix, when it already exists, or when the bundle's own state is not the
            authenticated authority; `X_IDENTITY_MISMATCH` when a scene's provenance
            block is not the one this connection produces for that case;
            `X_BUNDLE_INCOMPLETE` when the bundle's menu is not the record's, when its
            declared version is not this module's, when a presented scene is not the
            scene this connection assembles from its own authenticated payloads, when
            what the writer left on disk is not exactly the declared set, when a published document is not the
            canonical rendering of the object this chain assembled, when the digest a
            reader is told to check is not the digest of the file beside it, or when a
            figure does not declare the required resolution; and
            `X_IDENTITY_MISMATCH` when an identity the writer *reports* disagrees with
            the one this chain authenticated. The read-order table names only the
            success code for this row, so the refusals reuse the codes the rows above
            already use for the same kinds of disagreement rather than adding a
            fifteenth exit that design section 4.5 has not opened.

    **The writer is a parameter, and the reason is a cycle rather than a preference.**
    `scripts/render_verification_scene.py` is the entry point that will call into this
    module, so importing it here would close a loop; it is also the only module on this
    surface that imports matplotlib, and this one opens nothing and draws nothing.
    Injecting it keeps both properties.

    *** AND AN INJECTED WRITER IS A SEAM, WHICH IS THE FAULT THIS REVIEW HAS FOUND
    TWICE. *** A value reaching a checked object from beside it rather than from inside
    it is exactly what row 19's test seam and row 20's provenance argument each got
    wrong. So nothing the writer *reports* is adopted. Its report is compared, field by
    field, against what this row already knows and against the bytes it finds on disk:

      * the file set is derived from the bundle's own case ids and compared to the tree
        by **set equality in both directions**, so an extra file is as fatal as a
        missing one, and no directory may appear below the root at all;
      * the bundle document on disk must be byte-identical to
        `canonical_bundle_text(bundle)`, must parse back through `bundle_from_json`
        into the same canonical text, and its digest is **re-measured here** rather
        than read from the report;
      * `verification_bundle.sha256` must hold that re-measured digest, because that
        file is the one instruction a reader is given and a digest that names some
        other bytes is worse than none;
      * every scene document must be byte-identical to `canonical_scene_text` of the
        scene this chain assembled for that case;
      * every figure must be a PNG whose own `pHYs` chunk states the resolution the
        report claims it was saved at, and that resolution must be
        `REQUIRED_FIGURE_DPI`. A report of a DPI is not a DPI.

    *** AND THE BUNDLE IS THE SECOND SEPARATELY CONSTRUCTIBLE VALUE ON THIS ROW. ***
    `bundle` and `connection` are two arguments, and nothing in the signature makes
    them come from one chain. Codex's Session-153 review built two genuinely
    authenticated connections over one tree -- same authority, same menu, different
    labels and different record digests -- resolved rows 13 through 20 under the first
    and published the result under the second; every scene still identified the first
    connection while the tree it was published into was named for the second. So
    before anything is created, the menu, the declared version, the bundle's own
    provenance state and **every field of every scene's provenance block** are
    required to be what this connection produces. The comparand is built by
    `_provenance_for`, the same function row 20 assembles with, and the comparison
    walks `Provenance`'s own fields rather than a hand-listed set, so a field added to
    that dataclass is bound here without anyone remembering to bind it.

    *** AND BINDING THE PROVENANCE BLOCK IS NOT BINDING THE BUNDLE. *** Codex's
    Session-154 review took the same seam one width deeper: a scene carries
    thresholds, a body-change description, a playback grid, decisions, controller
    series, tracking arrays and a centerline, and every one of them arrives through the
    same separately constructible `bundle`. Replacing the authenticated
    `abstain_threshold` on *every* scene keeps `validate_bundle`'s cross-scene
    agreement true and leaves every provenance block byte-for-byte authentic, and the
    altered bundle published. **The provenance block states what the picture was drawn
    from; it does not make the picture be that.** So this row now re-derives rows 13
    through 20 from the connection and requires each presented scene's canonical
    rendering to equal the derived one, which binds every field of every scene at once
    and stays total as the scene type grows. The re-derivation opens nothing -- rows 13
    through 18 are pure functions of payloads row 12 already loaded -- and the
    audit-hook observer over this row is what says so.

    **The provenance walk is kept above it rather than folded into it**, because the
    two answer different questions and say so with different codes: a bundle assembled
    under another connection is an identity disagreement and names the field, while a
    bundle whose content is not what these sources produce is an incomplete bundle.
    Deleting either changes what a caller is told, which is the test lesson 286 sets
    for a guard that overlaps another.

    **The exclusive create runs before anything is written and nothing is cleaned up
    after a refusal.** A second invocation at the same `record_label` therefore refuses
    without touching the first publication, which is invariant W10; and a post-condition
    that fires after the writer has run leaves the partial tree standing as evidence,
    where the same exclusive create makes a later run at that label refuse rather than
    silently overwrite it. That is the discipline finding AU left behind: a failed root
    is kept, not swept.
    """

    output_root = Path(connection.bound.output_root).resolve()
    expected_root = _authority_output_root(connection)
    if output_root != expected_root:
        raise _refuse(
            X_PROVENANCE_UNRESOLVED,
            f"the bound output root {output_root} is not the destination this "
            f"connection fixes, which is {expected_root}; the publication tree is "
            "the record label's own child of the authority's own parent, and both "
            "halves of that are authenticated values rather than arguments",
        )

    declared_cases = tuple(case.case_id for case in connection.record.cases)
    if tuple(bundle.scenes) != declared_cases:
        raise _refuse(
            X_BUNDLE_INCOMPLETE,
            f"the bundle presents cases {list(bundle.scenes)} but this connection's "
            f"record declares {list(declared_cases)}, in that order; the menu that is "
            "published is the menu that was authenticated",
        )
    if bundle.bundle_version != BUNDLE_VERSION:
        raise _refuse(
            X_BUNDLE_INCOMPLETE,
            f"the bundle declares version {bundle.bundle_version!r} but this module "
            f"assembles {BUNDLE_VERSION!r}",
        )
    if bundle.provenance_state != connection.record.authority:
        raise _refuse(
            X_PROVENANCE_UNRESOLVED,
            f"the bundle carries provenance state {bundle.provenance_state!r} but "
            f"this connection's authenticated authority is "
            f"{connection.record.authority!r}",
        )
    for case in connection.record.cases:
        presented = bundle.scenes[case.case_id].provenance
        assembled = _provenance_for(connection, case, connection.record.authority)
        for field in dataclass_fields(Provenance):
            if getattr(presented, field.name) != getattr(assembled, field.name):
                raise _refuse(
                    X_IDENTITY_MISMATCH,
                    f"case {case.case_id!r} is presented with provenance "
                    f"{field.name} {getattr(presented, field.name)!r}, but this "
                    f"connection authenticated {getattr(assembled, field.name)!r}; a "
                    "bundle is published only under the connection that assembled it",
                )

    derived_cases = resolve_cases(connection)
    derived = resolve_bundle(
        connection,
        derived_cases,
        resolve_geometry(connection, derived_cases),
        resolve_provenance(connection),
    )
    for case_id in declared_cases:
        if canonical_scene_text(bundle.scenes[case_id]) != canonical_scene_text(
            derived.scenes[case_id]
        ):
            raise _refuse(
                X_BUNDLE_INCOMPLETE,
                f"the scene presented for case {case_id!r} is not the scene this "
                "connection assembles from the payloads it authenticated; the "
                "provenance block a reader is shown states what the picture was drawn "
                "from, and the picture must be the one those sources produce",
            )

    try:
        output_root.mkdir(parents=True, exist_ok=False)
    except FileExistsError as exc:
        raise _refuse(
            X_PROVENANCE_UNRESOLVED,
            f"the output root {output_root} already exists; step 21 creates it "
            "exclusively so a second run at one record label refuses and the first "
            "publication survives the refusal",
        ) from exc
    except OSError as exc:
        raise _refuse(
            X_PROVENANCE_UNRESOLVED,
            f"the output root {output_root} could not be created: {exc}",
        ) from exc

    expected_names = set(BUNDLE_FILE_NAMES)
    for case_id in declared_cases:
        for suffix in CASE_FILE_SUFFIXES:
            expected_names.add(f"{case_id}{suffix}")

    report = render(bundle, output_root)

    entries = sorted(output_root.rglob("*"))
    directories = [entry for entry in entries if entry.is_dir()]
    if directories:
        raise _refuse(
            X_BUNDLE_INCOMPLETE,
            f"step 21 wrote {len(directories)} directory entries below "
            f"{output_root}; the declared output set is flat",
        )
    observed_names = {entry.name for entry in entries}
    if observed_names != expected_names:
        raise _refuse(
            X_BUNDLE_INCOMPLETE,
            f"the published set is {sorted(observed_names)} but the record's menu "
            f"declares {sorted(expected_names)}; step 21 writes exactly the declared "
            "set and nothing else",
        )

    bundle_bytes = _read_bytes(
        output_root / BUNDLE_JSON_NAME,
        where="the published bundle document",
        code=X_BUNDLE_INCOMPLETE,
    )
    canonical = canonical_bundle_text(bundle).encode("utf-8")
    if bundle_bytes != canonical:
        raise _refuse(
            X_BUNDLE_INCOMPLETE,
            "the published bundle document is not the canonical rendering of the "
            "menu this chain assembled",
        )
    reparsed = canonical_bundle_text(
        bundle_from_json(
            strict_json_document(
                bundle_bytes, "the published bundle document", X_BUNDLE_INCOMPLETE
            )
        )
    ).encode("utf-8")
    if reparsed != bundle_bytes:
        raise _refuse(
            X_BUNDLE_INCOMPLETE,
            "the published bundle document does not reproduce itself when it is read "
            "back, so what a reader parses is not what was assembled",
        )
    digest = external_bytes_digest(bundle_bytes)
    declared_digest = _read_bytes(
        output_root / BUNDLE_DIGEST_NAME,
        where="the published bundle digest",
        code=X_BUNDLE_INCOMPLETE,
    )
    if declared_digest != f"{digest}\n".encode("utf-8"):
        raise _refuse(
            X_BUNDLE_INCOMPLETE,
            f"{BUNDLE_DIGEST_NAME} does not hold the digest of the bundle document "
            "beside it; the one instruction a reader is given must name the bytes it "
            "is written next to",
        )
    _require_strings_equal(
        report.get("bundle_sha256"),
        digest,
        where="the writer's reported bundle_sha256",
        source="the digest of the published bytes",
    )
    _require_strings_equal(
        report.get("provenance_state"),
        connection.record.authority,
        where="the writer's reported provenance_state",
        source="the authenticated record's authority",
    )
    _require_strings_equal(
        report.get("bundle_version"),
        bundle.bundle_version,
        where="the writer's reported bundle_version",
        source="the assembled bundle",
    )
    reported_cases = tuple(
        str(entry.get("case_id")) for entry in report.get("cases", ())
    )
    if reported_cases != declared_cases:
        raise _refuse(
            X_BUNDLE_INCOMPLETE,
            f"the writer reports cases {list(reported_cases)} but the record's menu "
            f"declares {list(declared_cases)}, in that order",
        )

    reported_dpi = report.get("save_dpi")
    if reported_dpi != REQUIRED_FIGURE_DPI:
        raise _refuse(
            X_BUNDLE_INCOMPLETE,
            f"the writer reports {reported_dpi!r} DPI but section 4.7 requires "
            f"{REQUIRED_FIGURE_DPI}",
        )
    expected_pixels_per_metre = round(REQUIRED_FIGURE_DPI / _METRES_PER_INCH)
    for case_id in declared_cases:
        scene_name = f"{case_id}.json"
        scene_bytes = _read_bytes(
            output_root / scene_name,
            where=f"the published scene document {scene_name}",
            code=X_BUNDLE_INCOMPLETE,
        )
        expected_scene = canonical_scene_text(bundle.scenes[case_id]).encode("utf-8")
        if scene_bytes != expected_scene:
            raise _refuse(
                X_BUNDLE_INCOMPLETE,
                f"{scene_name} is not the canonical rendering of the scene this "
                f"chain assembled for case {case_id!r}",
            )
        figure_name = f"{case_id}.png"
        horizontal, vertical = _png_pixels_per_metre(
            _read_bytes(
                output_root / figure_name,
                where=f"the published figure {figure_name}",
                code=X_BUNDLE_INCOMPLETE,
            ),
            where=figure_name,
        )
        if (horizontal, vertical) != (
            expected_pixels_per_metre,
            expected_pixels_per_metre,
        ):
            raise _refuse(
                X_BUNDLE_INCOMPLETE,
                f"{figure_name} declares {horizontal}x{vertical} pixels per metre "
                f"but {REQUIRED_FIGURE_DPI} DPI is {expected_pixels_per_metre}",
            )

    return WrittenBundle(
        output_root=output_root,
        file_names=tuple(sorted(observed_names)),
        bundle_sha256=digest,
        cases=declared_cases,
        figure_dpi=REQUIRED_FIGURE_DPI,
    )
