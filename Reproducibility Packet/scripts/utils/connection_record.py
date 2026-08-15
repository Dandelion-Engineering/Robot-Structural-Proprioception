"""The Slot-8 connection-record contract: authentication, parsing and root binding.

**What this module is.** It implements rows 1, 2 and 3 of the read order in section
4.1 of `protocol/slot8-connection-record-v0.1.md` (Git blob `032db166`, jointly
approved Claude Session 135 / Codex Session 135) -- the *first boundary* that
document names:

    the record is authenticated before any scientific path is opened, and its own
    authentication needs nothing but the record file itself.

Concretely:

  * **step 1** -- `authenticate_record_bytes` reads the record's exact bytes and
    requires their SHA-256 to equal the digest the joint authorization named;
  * **step 2** -- `parse_connection_record` strict-parses those bytes, validates
    `record_version` and the complete section-3.2 field table, rejects every
    non-finite value and every rooted, drive-qualified or `..` path token;
  * **step 3** -- `bind_root_domains` binds each declared path to its own root
    domain *without opening anything*, requires the record's own file to be at the
    one tracked location section 3.1 gives it, requires the `--role-root` basename
    to equal `dataset_label`, enforces the section-4.7 authority-specific output
    parent, and checks the fixed authority/split policy.

`expected_open_set` then derives the section-4.2 allowlist from the bound record. It
is the "expected" side of invariant W3's set equality and, like everything else here,
opens nothing.

**What this module is not.** It is not the adapter. It resolves and refuses; it never
hashes a scientific file, never parses a config, never touches a role tree and never
writes anything. Read-order steps 4 through 21 -- config authentication, the source
artifacts, the audits, the role indexes and payloads, the geometry derivation and the
bundle assembly -- are the separately reviewed second half of sub-step 4b. Nothing
here licenses authoring a connection record, running the adapter, opening `dev`,
`pilot`, `val` or `test`, selecting a capacity or a threshold, or making any
C1-versus-S statement.

**Where the facts live** (the design's section 4.3 discipline, and standing lesson
199): this module points at the object that already owns a fact rather than copying
it. The refusal codes and the error type are
`utils.verification_scene`'s -- there is one definition of what each exit code means
and this module adds none. The 20 schema-A manifest field names and their integer
subset are derived from `utils.storage_contract.IdentityManifestRow` itself, so a
schema-A change moves this contract with it. The lowercase-hex digest predicate is
`utils.storage_contract.re_full_sha256`. The canonical-JSON rule is
`utils.protocol_p.canonical_json`, `allow_nan=False` still on.

**Two interpretations this build had to make, recorded here rather than left in a
session report.**

  1. *The source-class requirement is a bundle check, not a record field.* Section
     3.2 says the record's `cases` must jointly contain at least one `structure`,
     one `actuator` and one `sensor` case. The field table declares no source-class
     field, and a case's class is carried by its authenticated `labels` payload --
     `utils.verification_scene.validate_bundle` already establishes the requirement
     from those payloads. So the record constrains *which* cases exist and the check
     itself stays where the evidence is. Adding a `source_class` field to the record
     would let an author assert a class the payload contradicts, which is the exact
     "checked by equality, not adopted" failure the design's property 2 forbids.
  2. *Threshold, rung, width and tolerance values get shape gates only, never range
     gates.* Their correctness is established at read-order step 5 by equality
     against each one's own named, approved source artifact. A plausibility band
     invented here would be an unapproved number entering the contract through the
     back door, and sub-step 4b is explicitly forbidden from choosing one.

**Four properties this module holds that a field table alone does not imply**, each
one added because a review probe reached a state the green suite did not construct:

  1. *An authenticated record is immutable all the way down.* `frozen=True` on a
     dataclass rebinds nothing but the attribute, so a `dict` reached through a frozen
     attribute is still mutable and a later caller can turn authenticated bytes into a
     different allowlist without touching the file that was hashed. Every mapping this
     module hands out is a read-only view over a private copy and every array inside
     `document` is a tuple.
  2. *Every path token is one portable name, not merely a spelling without `..`.*
     An embedded NUL, an NTFS alternate-stream colon, a reserved DOS device stem and a
     trailing dot all survive a traversal rule and all name something different --
     or nothing -- on a different platform. Containment cannot catch them: resolution
     raises before the comparison, and a device alias is contained by every root.
  3. *A value that becomes a filename is refused as a filename.* `case_id` is written
     as `<output-root>/<case_id>.png` and `.json` by the already-approved renderer, so
     the record boundary requires one portable leaf token and the renderer keeps an
     independent containment check over what it is about to write.
  4. *The output namespace the record composes is bounded and one-to-one.* Containment
     alone says every written path is inside the root; it says nothing about whether
     the set of names inside that root is writable and distinct. A 251-character
     `case_id` composes a 256-character file name that no mainstream filesystem
     accepts, and the refusal arrives from the operating system *after* earlier files
     in the same set are already on disk. A `case_id` of `verification_bundle` composes
     the renderer's own manifest file name, so the digest it returns would no longer
     hash the file it names. Two ids differing only in case are one file on NTFS and
     two on ext4, which is a write set that is not the same object on two machines.
     Every one of those is refused here, before a path exists, and again at the write
     boundary.
"""

from __future__ import annotations

import hashlib
import json
import math
import re
from dataclasses import dataclass, fields
from pathlib import Path, PurePosixPath
from types import MappingProxyType
from typing import Any, Mapping, Sequence

from utils.storage_contract import IdentityManifestRow, re_full_sha256
from utils.protocol_p import canonical_json
from utils.verification_scene import (
    DEVELOPMENT_ONLY,
    FINAL,
    SUITE_KEYS,
    VerificationSceneError,
    X_CONNECTION_UNAUTHORIZED,
    X_IDENTITY_MISMATCH,
    X_PROVENANCE_UNRESOLVED,
    X_SPLIT_FORBIDDEN,
)

# --------------------------------------------------------------------------- #
# Contract constants (design sections 3.1, 3.2, 4.7 and 4.8).
# --------------------------------------------------------------------------- #
CONNECTION_RECORD_VERSION = "slot8-connection-record-v0.1"

#: The two record authorities. `SYNTHETIC_FIXTURE` is deliberately absent: it is the
#: private assembly seam's provenance state and is never an authority a reviewed
#: record may claim (design 2.4 and finding CW mechanism 3).
AUTHORITIES: tuple[str, ...] = (DEVELOPMENT_ONLY, FINAL)

SPLITS: tuple[str, ...] = ("dev", "pilot", "val", "test")

#: The four non-observation roles the record names per arm. This is
#: `schema.json`'s `roles` keys minus `identity_manifest` (not a payload role) and
#: `observations` (deliberately excluded by the design's field table). The schema is
#: not opened here because step 2 runs before the schema is authenticated at step 4;
#: `test_role_names_equal_the_schema_derived_set` pins this tuple against the file by
#: equality rather than letting it drift.
ROLE_NAMES: tuple[str, ...] = ("controller_logs", "estimator_outputs", "labels", "plant")

#: The chain order `utils.cable_mechanics.extract_deformation_coordinates` emits.
LINK_IDS: tuple[str, ...] = ("L1", "L2")

#: Section 4.8: the record tree and the bundle tree are siblings under one parent,
#: never nested, because step 21 exclusively creates the output root and refuses a
#: non-empty one.
VERIFICATION_CONNECTION_PARENT = PurePosixPath("results/verification_connection")
RECORD_PARENT = VERIFICATION_CONNECTION_PARENT / "records"
FINAL_OUTPUT_PARENT = VERIFICATION_CONNECTION_PARENT / "bundles"
DEVELOPMENT_OUTPUT_PARENT = PurePosixPath("results/verification_connection_development")

#: Section 4.7, keyed by authority.
OUTPUT_PARENTS: dict[str, PurePosixPath] = {
    DEVELOPMENT_ONLY: DEVELOPMENT_OUTPUT_PARENT,
    FINAL: FINAL_OUTPUT_PARENT,
}

#: The 20 schema-A identity fields and the five that are integers, both derived from
#: the dataclass that owns them rather than transcribed.
MANIFEST_ROW_FIELDS: tuple[str, ...] = tuple(
    field.name for field in fields(IdentityManifestRow)
)
MANIFEST_ROW_INT_FIELDS: frozenset[str] = frozenset(
    field.name for field in fields(IdentityManifestRow) if field.type in ("int", int)
)

_LABEL_PATTERN = re.compile(r"[a-z0-9-]+")
_DERIVATION_VERSION_PATTERN = re.compile(r"[a-z0-9][a-z0-9.\-]*")
_UTF8_BOM = b"\xef\xbb\xbf"

#: One portable path component. This is deliberately narrower than "whatever the
#: local filesystem accepts": a record is authored once and read on whatever machine
#: reproduces the packet, so a component that means one thing here and another thing
#: there is not one identity. The class excludes the NUL byte and every other control
#: character (which reach `Path.resolve()` as a raw `ValueError` rather than a
#: refusal), the colon (an NTFS alternate data stream designator, so
#: `schema.json:stream` names a hidden stream on Windows and an ordinary file
#: elsewhere), the space, and every shell/globbing metacharacter.
_PORTABLE_SEGMENT_PATTERN = re.compile(r"[A-Za-z0-9._-]+")

#: The DOS device names Windows still resolves ahead of a file of the same stem, in
#: any directory and with any extension. `CON`, `NUL` and the numbered ports are not
#: files there at all, so a record naming one names different objects on different
#: platforms. Compared against the uppercased stem, which is how Windows compares it.
_RESERVED_DEVICE_STEMS: frozenset[str] = frozenset(
    {"CON", "PRN", "AUX", "NUL", "CLOCK$"}
    | {f"COM{digit}" for digit in range(10)}
    | {f"LPT{digit}" for digit in range(10)}
)

#: The longest single path component that is writable everywhere the packet has to
#: run. NTFS, ext4, APFS, HFS+, XFS and Btrfs all stop at 255 -- ext4 counts UTF-8
#: bytes and NTFS counts UTF-16 units, but the portable component class above is
#: ASCII-only, so one character is one of either unit here and a single character
#: count is exact. A grammar with no ceiling is not a portability rule: an
#: over-long name passes every spelling and containment check and then fails at
#: `open()`, which is the one place a refusal cannot be fail-closed because earlier
#: files in the same write set are already on disk.
MAX_PORTABLE_COMPONENT_CHARS = 255

#: The two fixed files `render_verification_scene.render_bundle` writes into every
#: bundle directory, and the suffixes it appends to each `case_id`. They are stated
#: here rather than imported because importing the renderer would pull matplotlib
#: into a contract module that opens nothing and draws nothing;
#: `test_bundle_output_names_equal_the_published_write_set` pins both tuples against
#: the tracked Step-3 figure set by equality, which is the same discipline
#: `ROLE_NAMES` gets against `schema.json`.
BUNDLE_FILE_NAMES: tuple[str, ...] = (
    "verification_bundle.json",
    "verification_bundle.sha256",
)
CASE_FILE_SUFFIXES: tuple[str, ...] = (".png", ".json")

#: `case_id` is never written as itself: it is written as `case_id` + the longest of
#: the suffixes above. Bounding the id at 255 would therefore accept an id whose own
#: derived file name is over the limit, which is exactly the state Codex's Round-2
#: probe reached -- a 251-character id, a 256-character `.json`, three files written
#: and then a raw `OSError`.
MAX_CASE_ID_CHARS = MAX_PORTABLE_COMPONENT_CHARS - max(
    len(suffix) for suffix in CASE_FILE_SUFFIXES
)


# --------------------------------------------------------------------------- #
# Refusal helpers. Every refusal in this module is a `VerificationSceneError`
# carrying one of the codes `utils.verification_scene` already defines.
# --------------------------------------------------------------------------- #
def _refuse(code: str, message: str) -> VerificationSceneError:
    """Build one fail-closed refusal.

    Args:
        code: one of the refusal codes owned by `utils.verification_scene`.
        message: what was wrong, in terms a reviewer can act on.

    Returns:
        The error to raise. It is returned rather than raised so call sites read as
        `raise _refuse(...)`, which keeps the raising statement at the failing line.
    """

    return VerificationSceneError(code, message)


def _unauthorized(message: str) -> VerificationSceneError:
    """Build the step-1/step-2 refusal: the record itself is not usable."""

    return _refuse(X_CONNECTION_UNAUTHORIZED, message)


# --------------------------------------------------------------------------- #
# Step 1 -- the record's own identity.
# --------------------------------------------------------------------------- #
def authenticate_record_bytes(path: Path, expected_sha256: str) -> bytes:
    """Read one connection record and require its bytes to be the authorized ones.

    Args:
        path: the `--connection-record` path. It is the only file this module opens.
        expected_sha256: the `--connection-record-sha256` value, the exact digest the
            two section-10.4e authorization halves named.

    Returns:
        The record's exact bytes.

    Raises:
        VerificationSceneError: `X_CONNECTION_UNAUTHORIZED` when the expected digest
            is not one lowercase SHA-256 hex string, when the file cannot be read, or
            when the measured digest differs. The digest is checked before the bytes
            are parsed and before any other path is touched, which is the first half
            of invariant W1.
    """

    if not isinstance(expected_sha256, str) or not re_full_sha256(expected_sha256):
        raise _unauthorized(
            "--connection-record-sha256 must be one lowercase SHA-256 hex digest; "
            f"got {expected_sha256!r}"
        )
    try:
        raw = Path(path).read_bytes()
    except OSError as exc:
        raise _unauthorized(f"the connection record at {path} could not be read: {exc}") from exc
    measured = hashlib.sha256(raw).hexdigest()
    if measured != expected_sha256:
        raise _unauthorized(
            f"the connection record at {path} hashes to {measured}, not the authorized "
            f"{expected_sha256}; a path is not an identity"
        )
    return raw


# --------------------------------------------------------------------------- #
# Step 2 -- strict parsing and the section-3.2 field table.
# --------------------------------------------------------------------------- #
def _strict_json_object(raw: bytes) -> dict[str, Any]:
    """Decode canonical record bytes into one JSON object, refusing every soft form.

    Args:
        raw: the authenticated record bytes.

    Returns:
        The parsed object.

    Raises:
        VerificationSceneError: `X_CONNECTION_UNAUTHORIZED` for invalid UTF-8, a byte
            order mark, a trailing newline, a duplicate key, a `NaN`/`Infinity`
            literal, a non-object document, or bytes that are not the canonical
            rendering of what they parse to. The canonical round-trip is one check
            that subsumes key ordering, separator style and whitespace, and it is the
            reason a reviewer can diff two records meaningfully (design 3.1).
    """

    if raw.startswith(_UTF8_BOM):
        raise _unauthorized("a connection record must not carry a UTF-8 byte order mark")
    if raw.endswith(b"\n") or raw.endswith(b"\r"):
        raise _unauthorized("a connection record must not end with a newline")
    try:
        text = raw.decode("utf-8")
    except UnicodeDecodeError as exc:
        raise _unauthorized(f"a connection record must be valid UTF-8: {exc}") from exc

    def reject_constant(value: str) -> None:
        raise _unauthorized(f"non-finite JSON constant is forbidden in a record: {value}")

    def unique_object(pairs: list[tuple[str, Any]]) -> dict[str, Any]:
        out: dict[str, Any] = {}
        for key, value in pairs:
            if key in out:
                raise _unauthorized(f"duplicate JSON key is forbidden in a record: {key}")
            out[key] = value
        return out

    try:
        document = json.loads(
            text, parse_constant=reject_constant, object_pairs_hook=unique_object
        )
    except json.JSONDecodeError as exc:
        raise _unauthorized(f"a connection record must be valid JSON: {exc}") from exc
    if not isinstance(document, dict):
        raise _unauthorized("a connection record must be one JSON object")

    _reject_non_finite(document, "record")
    try:
        rendered = canonical_json(document).encode("utf-8")
    except (TypeError, ValueError) as exc:  # pragma: no cover - defensive
        raise _unauthorized(f"a connection record must be canonical-JSON writable: {exc}") from exc
    if rendered != raw:
        raise _unauthorized(
            "a connection record must be exactly its own canonical JSON rendering "
            "(sort_keys, (',',':'), no BOM, no trailing newline)"
        )
    return document


def _reject_non_finite(value: Any, where: str) -> None:
    """Refuse any non-finite float anywhere in a parsed document.

    Args:
        value: a parsed JSON value.
        where: a dotted path used in the refusal message.

    Raises:
        VerificationSceneError: `X_CONNECTION_UNAUTHORIZED` on the first non-finite
            float. This is not redundant with `parse_constant`: `json.loads` turns an
            overflowing literal such as `1e9999` into `inf` without ever calling that
            hook, which is the shape finding from Session 67 that reached a published
            artifact once already. A record forbids non-finite values outright
            (design 3.1) because a record is authored, not derived from a run.
    """

    if isinstance(value, bool):
        return
    if isinstance(value, float):
        if not math.isfinite(value):
            raise _unauthorized(f"{where} is a non-finite number, which a record forbids")
        return
    if isinstance(value, dict):
        for key, item in value.items():
            _reject_non_finite(item, f"{where}.{key}")
        return
    if isinstance(value, (list, tuple)):
        for index, item in enumerate(value):
            _reject_non_finite(item, f"{where}[{index}]")


def _require_mapping(value: Any, where: str, keys: Sequence[str]) -> Mapping[str, Any]:
    """Require one JSON object carrying exactly `keys`.

    Args:
        value: the candidate value.
        where: a dotted path used in the refusal message.
        keys: the exact key set. There is no optional field and no default anywhere
            in the record: an absent field is a refusal, not an empty value, and an
            unexpected field is a refusal too, because a record the adapter does not
            fully understand is a record it cannot claim to have authenticated.

    Returns:
        The mapping.

    Raises:
        VerificationSceneError: `X_CONNECTION_UNAUTHORIZED`.
    """

    if not isinstance(value, dict):
        raise _unauthorized(f"{where} must be a JSON object")
    expected = set(keys)
    present = set(value)
    missing = sorted(expected - present)
    extra = sorted(present - expected)
    if missing:
        raise _unauthorized(f"{where} is missing required field(s): {', '.join(missing)}")
    if extra:
        raise _unauthorized(f"{where} carries unexpected field(s): {', '.join(extra)}")
    return value


def _require_str(value: Any, where: str) -> str:
    """Require one non-empty JSON string."""

    if not isinstance(value, str) or not value:
        raise _unauthorized(f"{where} must be a non-empty string")
    return value


def _require_pattern(value: Any, where: str, pattern: re.Pattern[str]) -> str:
    """Require one non-empty string fully matching `pattern`."""

    text = _require_str(value, where)
    if pattern.fullmatch(text) is None:
        raise _unauthorized(f"{where} must match /{pattern.pattern}/; got {text!r}")
    return text


def _require_digest(value: Any, where: str) -> str:
    """Require one lowercase SHA-256 hex digest."""

    text = _require_str(value, where)
    if not re_full_sha256(text):
        raise _unauthorized(f"{where} must be one lowercase SHA-256 hex digest")
    return text


def _require_config_hash(value: Any, where: str) -> str:
    """Require one lifecycle-shaped config hash: 64 hex, optionally `dev-` prefixed.

    The lifecycle itself is owned by `utils.config_contract`, and the record's value
    is bound to the loaded config by equality at read-order step 4. This is a shape
    gate so that a transcription error refuses at step 2 rather than surviving to a
    layer that opens a file.
    """

    text = _require_str(value, where)
    body = text[4:] if text.startswith("dev-") else text
    if not re_full_sha256(body):
        raise _unauthorized(
            f"{where} must be a SHA-256 hex digest, optionally carrying the draft "
            "'dev-' prefix"
        )
    return text


def _require_finite_float(value: Any, where: str) -> float:
    """Require one finite JSON number, accepting an integer literal.

    The conversion is guarded rather than assumed. `json.loads` parses an unbounded
    integer literal exactly -- `10 ** 400` arrives as a Python `int`, passes the
    non-finite walk (which only inspects floats) and then makes `float()` raise a raw
    `OverflowError`. A raw exception out of a contract layer is a silent failure by
    another name: the caller sees a crash instead of the named refusal, and the exit
    code the design assigned never happens. The overflowing literal is refused here,
    in the same sentence as any other unrepresentable number.
    """

    if isinstance(value, bool) or not isinstance(value, (int, float)):
        raise _unauthorized(f"{where} must be a JSON number")
    try:
        number = float(value)
    except (OverflowError, ValueError) as exc:
        raise _unauthorized(
            f"{where} is a numeric literal too large to represent as a finite number: {exc}"
        ) from exc
    if not math.isfinite(number):
        raise _unauthorized(f"{where} must be finite")
    return number


def _require_positive_float(value: Any, where: str) -> float:
    """Require one finite JSON number strictly greater than zero."""

    number = _require_finite_float(value, where)
    if number <= 0.0:
        raise _unauthorized(f"{where} must be greater than zero")
    return number


def _require_positive_int(value: Any, where: str) -> int:
    """Require one positive JSON integer, refusing a float that happens to be whole."""

    if isinstance(value, bool) or not isinstance(value, int):
        raise _unauthorized(f"{where} must be a JSON integer")
    if value <= 0:
        raise _unauthorized(f"{where} must be greater than zero")
    return value


def _require_portable_segment(
    segment: str,
    where: str,
    *,
    text: str,
    max_chars: int = MAX_PORTABLE_COMPONENT_CHARS,
) -> None:
    """Require one path component to be one portable name on every platform.

    Args:
        segment: the component, already known to be non-empty and not `.` or `..`.
        where: a dotted path used in the refusal message.
        text: the whole token, quoted in the refusal so the reviewer sees the shape.
        max_chars: the ceiling at this position. It is below
            `MAX_PORTABLE_COMPONENT_CHARS` wherever the packet appends something to
            the component before writing it, so what the ceiling bounds is the
            *derived* name rather than the token as written.

    Raises:
        VerificationSceneError: `X_CONNECTION_UNAUTHORIZED` when the component is
            longer than `max_chars`, carries a character outside the portable class,
            ends in a dot or a space (Windows silently strips both, so two distinct
            records would name one file), or has a stem Windows resolves as a device
            rather than a file.

    A token rule is the only layer that can refuse these. Containment cannot: an
    embedded NUL never reaches a containment comparison because `Path.resolve()`
    raises first, and a device alias is contained by every root while naming no file
    at all. An over-long component is the same shape a third time -- it is contained
    by its root, it resolves without complaint, and the only thing that ever objects
    is the `open()` call that has already let the shorter names in the same write set
    onto disk.
    """

    if len(segment) > max_chars:
        raise _unauthorized(
            f"{where} carries a path component of {len(segment)} characters, above the "
            f"{max_chars}-character portable component ceiling that applies here; got "
            f"{text[:40]!r} (truncated for the message)"
        )
    if _PORTABLE_SEGMENT_PATTERN.fullmatch(segment) is None:
        raise _unauthorized(
            f"{where} carries the path component {segment!r}, which is outside the "
            "portable component class [A-Za-z0-9._-]; got "
            f"{text!r}"
        )
    if segment.endswith("."):
        raise _unauthorized(
            f"{where} carries the path component {segment!r}, which ends in a dot that "
            f"Windows strips; got {text!r}"
        )
    if segment.split(".")[0].upper() in _RESERVED_DEVICE_STEMS:
        raise _unauthorized(
            f"{where} carries the path component {segment!r}, whose stem is a reserved "
            f"device name rather than a file on Windows; got {text!r}"
        )


def _require_relative_path(value: Any, where: str) -> PurePosixPath:
    """Require one relative, forward-slash, traversal-free path token.

    Args:
        value: the candidate value.
        where: a dotted path used in the refusal message.

    Returns:
        The path as a `PurePosixPath`, which is deliberately *pure*: nothing here
        touches a filesystem.

    Raises:
        VerificationSceneError: `X_CONNECTION_UNAUTHORIZED` for an empty token, a
            backslash, a drive designator, a rooted form, a `.` or `..` segment, an
            empty segment, a trailing separator, or any component outside the
            portable component class. The schema calls this rule
            `project_relative_no_parent_traversal`; every path in a record obeys it,
            and which *root* it is relative to is decided at step 3.
    """

    text = _require_str(value, where)
    if "\\" in text:
        raise _unauthorized(f"{where} must use forward slashes; got {text!r}")
    if text.startswith("/"):
        raise _unauthorized(f"{where} must be relative, not rooted; got {text!r}")
    if re.match(r"^[A-Za-z]:", text):
        raise _unauthorized(f"{where} must not carry a drive designator; got {text!r}")
    if text.endswith("/"):
        raise _unauthorized(f"{where} must not end with a separator; got {text!r}")
    segments = text.split("/")
    for segment in segments:
        if segment == "":
            raise _unauthorized(f"{where} must not contain an empty path segment; got {text!r}")
        if segment in {".", ".."}:
            raise _unauthorized(
                f"{where} must not contain a '{segment}' segment; got {text!r}"
            )
        _require_portable_segment(segment, where, text=text)
    return PurePosixPath(text)


def _require_leaf_token(value: Any, where: str) -> str:
    """Require one portable single-component name, because it becomes a filename.

    Args:
        value: the candidate value.
        where: a dotted path used in the refusal message.

    Returns:
        The token.

    Raises:
        VerificationSceneError: `X_CONNECTION_UNAUTHORIZED` when the token is not
            exactly one portable path component, or when it is longer than
            `MAX_CASE_ID_CHARS`.

    `case_id` is not only a bundle key. `utils.render_verification_scene.render_bundle`
    writes `<destination>/<case_id>.png` and `<destination>/<case_id>.json`, so a
    record supplying `../escape` would write outside the exclusive-created output
    root -- a direct violation of design section 4.7 and invariant W10, and one that
    only became reachable when an external record started supplying the case id. The
    renderer carries a containment check of its own; this is the boundary that refuses
    the value before it ever becomes a path.

    The ceiling is `MAX_CASE_ID_CHARS`, not `MAX_PORTABLE_COMPONENT_CHARS`, because
    what reaches the filesystem is the token plus a suffix. Bounding the token at the
    filesystem's own limit would accept a token whose every derived name is over it.
    """

    text = _require_str(value, where)
    if "/" in text or "\\" in text:
        raise _unauthorized(
            f"{where} is written to disk as a filename and must be one path component "
            f"carrying no separator; got {text!r}"
        )
    if text in {".", ".."}:
        raise _unauthorized(
            f"{where} is written to disk as a filename and must not be {text!r}"
        )
    _require_portable_segment(text, where, text=text, max_chars=MAX_CASE_ID_CHARS)
    return text


def _portable_fold(name: str) -> str:
    """Fold one file name to the identity two platforms have to agree on.

    Two names that differ only in case are one file on NTFS and on a default APFS
    volume, and two files on ext4. A write set whose membership depends on which
    machine it runs on is not the exact declared set design 4.7 requires, so the
    packet treats the case-insensitive form as the identity and refuses the
    collision rather than picking a platform to be right on.

    `str.lower` rather than `str.casefold`: the portable component class is
    ASCII-only, where the two agree exactly, and `casefold` would additionally map
    characters this grammar has already refused.
    """

    return name.lower()


def _derived_case_file_names(case_id: str) -> tuple[str, ...]:
    """Return every file name `render_bundle` composes from one `case_id`."""

    return tuple(f"{case_id}{suffix}" for suffix in CASE_FILE_SUFFIXES)


# --------------------------------------------------------------------------- #
# Immutability. `@dataclass(frozen=True)` rebinds nothing but the attribute itself;
# a `dict` reached through a frozen attribute is still an ordinary mutable dict, and
# a caller can therefore turn an authenticated record into a different allowlist
# without touching a single byte of the file that was hashed. The two helpers below
# close that gap, and every mapping this module hands out passes through one of them.
# --------------------------------------------------------------------------- #
def _freeze(value: Any) -> Any:
    """Return a deeply immutable view of one parsed JSON value.

    Args:
        value: any value `json.loads` can produce.

    Returns:
        Mappings become `MappingProxyType` over frozen items and arrays become
        tuples; scalars are returned unchanged. Arrays deliberately become tuples
        rather than read-only list views, because Python has no read-only list and a
        tuple is the only sequence a later caller cannot append to.

        Two consequences a caller has to know rather than discover. A frozen document
        compares unequal to the plain `dict` it came from wherever an array appears,
        so equality against a source document is stated by freezing that document too.
        And `json.dumps` cannot serialize a `MappingProxyType`, which is deliberate:
        the record's canonical bytes already exist -- they are the bytes step 1
        authenticated -- and a second rendering path would be a second answer to the
        question of what the record says.
    """

    if isinstance(value, dict):
        return MappingProxyType({key: _freeze(item) for key, item in value.items()})
    if isinstance(value, (list, tuple)):
        return tuple(_freeze(item) for item in value)
    return value


def _frozen_mapping(mapping: Mapping[Any, Any]) -> Mapping[Any, Any]:
    """Return a read-only view over a copy of `mapping`.

    The copy matters: a proxy over a dict the caller still holds is a read-only
    handle on a mutable object, which is the appearance of the property without the
    property. Values are already immutable at every call site -- frozen dataclasses,
    `Path` objects or values that came through `_freeze`.
    """

    return MappingProxyType(dict(mapping))


# --------------------------------------------------------------------------- #
# The parsed record. Every dataclass below is frozen: an authenticated record is a
# value, and nothing downstream may edit one into a different allowlist.
# --------------------------------------------------------------------------- #
@dataclass(frozen=True)
class PacketArtifact:
    """One packet-relative artifact named by path and digest."""

    relative_path: PurePosixPath
    sha256: str


@dataclass(frozen=True)
class ConfigRef:
    """The authority-appropriate config file, its bytes and its semantic identity."""

    relative_path: PurePosixPath
    sha256: str
    config_hash: str


@dataclass(frozen=True)
class AuditRef:
    """One dataset audit's digest and the three semantic fields it must echo."""

    sha256: str
    status: str
    assignment_hash: str
    config_hash: str


@dataclass(frozen=True)
class DataRootRef:
    """Stable identity for the external `--role-root` tree (design finding CW)."""

    dataset_label: str
    manifest_sha256: str
    generation_audit: AuditRef
    independent_audit: AuditRef


@dataclass(frozen=True)
class EstablishedResultRef:
    """The already-produced and already-read result this surface presents."""

    artifact_relative_path: PurePosixPath
    sha256: str
    split_field_path: str
    config_hash_field_path: str
    cases_field_path: str


@dataclass(frozen=True)
class FieldSource:
    """One approved artifact and the exact field path a scalar must equal."""

    artifact_relative_path: PurePosixPath
    sha256: str
    field_path: str


@dataclass(frozen=True)
class ThresholdsRef:
    """The abstain and unknown thresholds, each with its own named source."""

    abstain_threshold: float
    unknown_threshold: float
    sources: Mapping[str, FieldSource]


@dataclass(frozen=True)
class ModelSelectionSource:
    """The approved artifact that selected the rung and the width."""

    artifact_relative_path: PurePosixPath
    sha256: str
    rung_field_path: str
    width_field_path: str


@dataclass(frozen=True)
class ModelSelection:
    """The selected capacity and the artifact that selected it."""

    rung: int
    width: int
    source: ModelSelectionSource


@dataclass(frozen=True)
class GeometrySource:
    """The generated-model producer, hashed and never imported (design 3.5)."""

    producer_relative_path: PurePosixPath
    producer_sha256: str
    model_id: str


@dataclass(frozen=True)
class PlanarConvention:
    """Origin, joint convention, log-map component and model-to-scene projection."""

    base_xy_m: tuple[float, float]
    q_true_convention: str
    rotation_vector_component: int
    projection: str


@dataclass(frozen=True)
class LinkGeometry:
    """One link's ordered segment lengths and its `deform_coords` triplets."""

    segment_lengths_m: tuple[float, ...]
    deform_triplets: tuple[tuple[int, int, int], ...]


@dataclass(frozen=True)
class ToleranceSource:
    """Where the real-data agreement and the allowed tolerance were established."""

    artifact_relative_path: PurePosixPath
    sha256: str
    maximum_deviation_field_path: str
    tolerance_field_path: str


@dataclass(frozen=True)
class RenderGeometry:
    """The explicit dependency-light chain plus its approved validation source."""

    derivation_version: str
    source: GeometrySource
    planar_convention: PlanarConvention
    links: Mapping[str, LinkGeometry]
    distal_tolerance_m: float
    tolerance_source: ToleranceSource


@dataclass(frozen=True)
class RoleRef:
    """One arm's reference to one non-observation role."""

    index_sha256: str
    payload_relative_path: PurePosixPath
    payload_sha256: str


@dataclass(frozen=True)
class CheckpointRef:
    """The fitted weights this arm's decisions came from."""

    relative_path: PurePosixPath
    sha256: str


@dataclass(frozen=True)
class Arm:
    """One C1 or S arm of one case."""

    run_id: str
    manifest_row: Mapping[str, Any]
    checkpoint: CheckpointRef
    roles: Mapping[str, RoleRef]


@dataclass(frozen=True)
class Case:
    """One menu entry: a display label and its C1/S pair."""

    case_id: str
    display_label: str
    pair_id: str
    arms: Mapping[str, Arm]


@dataclass(frozen=True)
class ConnectionRecord:
    """One authenticated, fully validated connection record.

    The `document` field is the parsed object, deeply frozen. It is kept because
    read-order steps 4 onward compare record values against files by equality, and a
    reviewer auditing a refusal needs what the refusal was taken over, not a
    reconstruction of it. It is frozen because "what was authenticated" has to keep
    meaning that: a mutable copy of the authenticated bytes is an allowlist any later
    caller can widen. Its arrays are tuples and its mappings are read-only views (see
    `_freeze`), so compare it to a source document by freezing that document too.
    """

    record_version: str
    record_label: str
    authority: str
    split: str
    schema: PacketArtifact
    config: ConfigRef
    data_root: DataRootRef
    established_result: EstablishedResultRef
    analysis_window_s: float
    thresholds: ThresholdsRef
    model_selection: ModelSelection
    render_geometry: RenderGeometry
    cases: tuple[Case, ...]
    document: Mapping[str, Any]


_TOP_LEVEL_FIELDS: tuple[str, ...] = (
    "analysis_window_s",
    "authority",
    "cases",
    "config",
    "data_root",
    "established_result",
    "model_selection",
    "record_label",
    "record_version",
    "render_geometry",
    "schema",
    "split",
    "thresholds",
)


def _parse_audit(value: Any, where: str) -> AuditRef:
    """Parse one `{sha256,status,assignment_hash,config_hash}` audit reference."""

    block = _require_mapping(value, where, ("sha256", "status", "assignment_hash", "config_hash"))
    return AuditRef(
        sha256=_require_digest(block["sha256"], f"{where}.sha256"),
        status=_require_str(block["status"], f"{where}.status"),
        assignment_hash=_require_str(block["assignment_hash"], f"{where}.assignment_hash"),
        config_hash=_require_config_hash(block["config_hash"], f"{where}.config_hash"),
    )


def _parse_field_source(value: Any, where: str) -> FieldSource:
    """Parse one `{artifact_relative_path,sha256,field_path}` source reference."""

    block = _require_mapping(value, where, ("artifact_relative_path", "sha256", "field_path"))
    return FieldSource(
        artifact_relative_path=_require_relative_path(
            block["artifact_relative_path"], f"{where}.artifact_relative_path"
        ),
        sha256=_require_digest(block["sha256"], f"{where}.sha256"),
        field_path=_require_str(block["field_path"], f"{where}.field_path"),
    )


def _parse_thresholds(value: Any) -> ThresholdsRef:
    """Parse the thresholds block, requiring one distinct source per threshold.

    Design 3.4: the two entries may name the same artifact, but they may not share
    one ambiguous field path -- a threshold is the one scientific input in the record
    small enough for a well-meaning author to type from memory.
    """

    where = "thresholds"
    block = _require_mapping(value, where, ("abstain_threshold", "unknown_threshold", "sources"))
    sources_block = _require_mapping(
        block["sources"], f"{where}.sources", ("abstain_threshold", "unknown_threshold")
    )
    sources = {
        name: _parse_field_source(sources_block[name], f"{where}.sources.{name}")
        for name in ("abstain_threshold", "unknown_threshold")
    }
    abstain = sources["abstain_threshold"]
    unknown = sources["unknown_threshold"]
    if (
        abstain.artifact_relative_path == unknown.artifact_relative_path
        and abstain.field_path == unknown.field_path
    ):
        raise _unauthorized(
            "thresholds.sources: the abstain and unknown thresholds must not share one "
            "artifact and field path; two numbers proved by one field is one number"
        )
    return ThresholdsRef(
        abstain_threshold=_require_finite_float(
            block["abstain_threshold"], f"{where}.abstain_threshold"
        ),
        unknown_threshold=_require_finite_float(
            block["unknown_threshold"], f"{where}.unknown_threshold"
        ),
        sources=_frozen_mapping(sources),
    )


def _parse_model_selection(value: Any) -> ModelSelection:
    """Parse the capacity selection and its approved source artifact."""

    where = "model_selection"
    block = _require_mapping(value, where, ("rung", "width", "source"))
    source_block = _require_mapping(
        block["source"],
        f"{where}.source",
        ("artifact_relative_path", "sha256", "rung_field_path", "width_field_path"),
    )
    source = ModelSelectionSource(
        artifact_relative_path=_require_relative_path(
            source_block["artifact_relative_path"], f"{where}.source.artifact_relative_path"
        ),
        sha256=_require_digest(source_block["sha256"], f"{where}.source.sha256"),
        rung_field_path=_require_str(
            source_block["rung_field_path"], f"{where}.source.rung_field_path"
        ),
        width_field_path=_require_str(
            source_block["width_field_path"], f"{where}.source.width_field_path"
        ),
    )
    if source.rung_field_path == source.width_field_path:
        raise _unauthorized(
            "model_selection.source: the rung and width field paths must differ"
        )
    return ModelSelection(
        rung=_require_positive_int(block["rung"], f"{where}.rung"),
        width=_require_positive_int(block["width"], f"{where}.width"),
        source=source,
    )


def _parse_link(value: Any, where: str) -> LinkGeometry:
    """Parse one link's segment lengths and deformation triplets.

    The one derived structural relation is stated rather than assumed: for each link
    `utils.cable_mechanics.extract_deformation_coordinates` emits the rotation-vector
    log map of `body_ids[1:]`, three components per internal body, deliberately
    excluding the first body of the link. So a link carrying `n` ordered bodies has
    `n` segment lengths and `n - 1` triplets, and `n` must be at least two.
    """

    block = _require_mapping(value, where, ("segment_lengths_m", "deform_triplets"))
    raw_lengths = block["segment_lengths_m"]
    if not isinstance(raw_lengths, list) or len(raw_lengths) < 2:
        raise _unauthorized(
            f"{where}.segment_lengths_m must be a list of at least two segment lengths"
        )
    lengths = tuple(
        _require_positive_float(item, f"{where}.segment_lengths_m[{index}]")
        for index, item in enumerate(raw_lengths)
    )
    raw_triplets = block["deform_triplets"]
    if not isinstance(raw_triplets, list):
        raise _unauthorized(f"{where}.deform_triplets must be a list")
    if len(raw_triplets) != len(lengths) - 1:
        raise _unauthorized(
            f"{where} declares {len(lengths)} bodies and {len(raw_triplets)} deformation "
            f"triplets; the first body of each link carries no internal deformation "
            f"coordinate, so exactly {len(lengths) - 1} triplets are required"
        )
    triplets: list[tuple[int, int, int]] = []
    for index, item in enumerate(raw_triplets):
        label = f"{where}.deform_triplets[{index}]"
        if not isinstance(item, list) or len(item) != 3:
            raise _unauthorized(f"{label} must be a list of exactly three indices")
        values = []
        for position, entry in enumerate(item):
            if isinstance(entry, bool) or not isinstance(entry, int) or entry < 0:
                raise _unauthorized(
                    f"{label}[{position}] must be a non-negative JSON integer"
                )
            values.append(entry)
        triplets.append((values[0], values[1], values[2]))
    return LinkGeometry(segment_lengths_m=lengths, deform_triplets=tuple(triplets))


def _parse_render_geometry(value: Any) -> RenderGeometry:
    """Parse the render geometry block (design 3.5 and finding CU)."""

    where = "render_geometry"
    block = _require_mapping(
        value,
        where,
        (
            "derivation_version",
            "source",
            "planar_convention",
            "links",
            "distal_tolerance_m",
            "tolerance_source",
        ),
    )
    source_block = _require_mapping(
        block["source"], f"{where}.source", ("producer_relative_path", "producer_sha256", "model_id")
    )
    source = GeometrySource(
        producer_relative_path=_require_relative_path(
            source_block["producer_relative_path"], f"{where}.source.producer_relative_path"
        ),
        producer_sha256=_require_digest(
            source_block["producer_sha256"], f"{where}.source.producer_sha256"
        ),
        model_id=_require_str(source_block["model_id"], f"{where}.source.model_id"),
    )

    convention_block = _require_mapping(
        block["planar_convention"],
        f"{where}.planar_convention",
        ("base_xy_m", "q_true_convention", "rotation_vector_component", "projection"),
    )
    raw_base = convention_block["base_xy_m"]
    if not isinstance(raw_base, list) or len(raw_base) != 2:
        raise _unauthorized(f"{where}.planar_convention.base_xy_m must be a list of two numbers")
    base_xy = (
        _require_finite_float(raw_base[0], f"{where}.planar_convention.base_xy_m[0]"),
        _require_finite_float(raw_base[1], f"{where}.planar_convention.base_xy_m[1]"),
    )
    component = convention_block["rotation_vector_component"]
    if isinstance(component, bool) or not isinstance(component, int) or not 0 <= component <= 2:
        raise _unauthorized(
            f"{where}.planar_convention.rotation_vector_component must be 0, 1 or 2 -- one "
            "component of a three-vector log map"
        )
    convention = PlanarConvention(
        base_xy_m=base_xy,
        q_true_convention=_require_str(
            convention_block["q_true_convention"], f"{where}.planar_convention.q_true_convention"
        ),
        rotation_vector_component=component,
        projection=_require_str(
            convention_block["projection"], f"{where}.planar_convention.projection"
        ),
    )

    links_block = _require_mapping(block["links"], f"{where}.links", LINK_IDS)
    links = _frozen_mapping(
        {
            link_id: _parse_link(links_block[link_id], f"{where}.links.{link_id}")
            for link_id in LINK_IDS
        }
    )
    _require_contiguous_triplets(links, where)

    tolerance_block = _require_mapping(
        block["tolerance_source"],
        f"{where}.tolerance_source",
        ("artifact_relative_path", "sha256", "maximum_deviation_field_path", "tolerance_field_path"),
    )
    tolerance_source = ToleranceSource(
        artifact_relative_path=_require_relative_path(
            tolerance_block["artifact_relative_path"],
            f"{where}.tolerance_source.artifact_relative_path",
        ),
        sha256=_require_digest(tolerance_block["sha256"], f"{where}.tolerance_source.sha256"),
        maximum_deviation_field_path=_require_str(
            tolerance_block["maximum_deviation_field_path"],
            f"{where}.tolerance_source.maximum_deviation_field_path",
        ),
        tolerance_field_path=_require_str(
            tolerance_block["tolerance_field_path"], f"{where}.tolerance_source.tolerance_field_path"
        ),
    )
    if (
        tolerance_source.maximum_deviation_field_path
        == tolerance_source.tolerance_field_path
    ):
        raise _unauthorized(
            f"{where}.tolerance_source: the maximum-deviation and tolerance field paths must "
            "differ; the adapter requires the measured maximum not to exceed the declared "
            "tolerance, which is vacuous when both read one field"
        )

    return RenderGeometry(
        derivation_version=_require_pattern(
            block["derivation_version"], f"{where}.derivation_version", _DERIVATION_VERSION_PATTERN
        ),
        source=source,
        planar_convention=convention,
        links=links,
        distal_tolerance_m=_require_positive_float(
            block["distal_tolerance_m"], f"{where}.distal_tolerance_m"
        ),
        tolerance_source=tolerance_source,
    )


def _require_contiguous_triplets(links: Mapping[str, LinkGeometry], where: str) -> None:
    """Require the declared triplets to be the emitted `deform_coords` layout.

    `extract_deformation_coordinates` concatenates the internal-body log maps of L1
    and then of L2, three components per body, in that order. So reading the declared
    triplets in link order `L1`, `L2` must give exactly
    `(0,1,2), (3,4,5), ...` with no gap, no repeat and no reordering. Anything else
    is a record claiming a layout the producer does not emit -- which would silently
    draw a different robot.
    """

    flattened: list[int] = []
    for link_id in LINK_IDS:
        for triplet in links[link_id].deform_triplets:
            flattened.extend(triplet)
    expected = list(range(len(flattened)))
    if flattened != expected:
        raise _unauthorized(
            f"{where}.links: the deformation triplets, read in link order "
            f"{'/'.join(LINK_IDS)}, must be the contiguous zero-based layout "
            "`extract_deformation_coordinates` emits"
        )


def _parse_manifest_row(value: Any, where: str) -> Mapping[str, Any]:
    """Parse one echoed 20-field schema-A identity row.

    The row is *echoed* so that read-order step 10 can compare it to `manifest.csv`
    by equality rather than adopting whatever the file says (design property 2). The
    field names and the integer subset come from
    `utils.storage_contract.IdentityManifestRow`, so a schema-A change moves this
    check with it instead of leaving a stale transcription behind.
    """

    block = _require_mapping(value, where, MANIFEST_ROW_FIELDS)
    row: dict[str, Any] = {}
    for name in MANIFEST_ROW_FIELDS:
        item = block[name]
        if name in MANIFEST_ROW_INT_FIELDS:
            if isinstance(item, bool) or not isinstance(item, int):
                raise _unauthorized(f"{where}.{name} must be a JSON integer")
            row[name] = item
        else:
            row[name] = _require_str(item, f"{where}.{name}")
    return _frozen_mapping(row)


def _parse_arm(value: Any, where: str, *, suite: str, split: str, pair_id: str) -> Arm:
    """Parse one arm and require its echoed row to agree with its own position.

    Three coherence checks run here rather than at step 10, because they need no file
    at all: a row echoing `suite = "S"` under the `C1` arm, a different `run_id`, a
    different `pair_id` or a different `split` is malformed on its own terms, and a
    malformed record should refuse before anything is opened.
    """

    block = _require_mapping(value, where, ("run_id", "manifest_row", "checkpoint", "roles"))
    run_id = _require_str(block["run_id"], f"{where}.run_id")
    row = _parse_manifest_row(block["manifest_row"], f"{where}.manifest_row")
    if row["suite"] != suite:
        raise _unauthorized(
            f"{where}.manifest_row.suite is {row['suite']!r} under the {suite!r} arm"
        )
    if row["run_id"] != run_id:
        raise _unauthorized(
            f"{where}.manifest_row.run_id is {row['run_id']!r} but the arm names {run_id!r}"
        )
    if row["pair_id"] != pair_id:
        raise _unauthorized(
            f"{where}.manifest_row.pair_id is {row['pair_id']!r} but the case names {pair_id!r}"
        )
    if row["split"] != split:
        raise _unauthorized(
            f"{where}.manifest_row.split is {row['split']!r} but the record names {split!r}"
        )

    checkpoint_block = _require_mapping(
        block["checkpoint"], f"{where}.checkpoint", ("relative_path", "sha256")
    )
    checkpoint = CheckpointRef(
        relative_path=_require_relative_path(
            checkpoint_block["relative_path"], f"{where}.checkpoint.relative_path"
        ),
        sha256=_require_digest(checkpoint_block["sha256"], f"{where}.checkpoint.sha256"),
    )

    roles_block = _require_mapping(block["roles"], f"{where}.roles", ROLE_NAMES)
    roles: dict[str, RoleRef] = {}
    for role in ROLE_NAMES:
        role_where = f"{where}.roles.{role}"
        role_block = _require_mapping(
            roles_block[role], role_where, ("index_sha256", "payload_relative_path", "payload_sha256")
        )
        roles[role] = RoleRef(
            index_sha256=_require_digest(role_block["index_sha256"], f"{role_where}.index_sha256"),
            payload_relative_path=_require_relative_path(
                role_block["payload_relative_path"], f"{role_where}.payload_relative_path"
            ),
            payload_sha256=_require_digest(
                role_block["payload_sha256"], f"{role_where}.payload_sha256"
            ),
        )
    return Arm(
        run_id=run_id,
        manifest_row=row,
        checkpoint=checkpoint,
        roles=_frozen_mapping(roles),
    )


def _parse_cases(value: Any, *, split: str) -> tuple[Case, ...]:
    """Parse the ordered menu, requiring unique ids, labels and derived file names.

    The display labels are what the director reads in the radio menu, and the Step-2
    surface refuses a duplicate label because two identical entries make the menu
    lie about which case is showing. Uniqueness is required here for the same reason
    and one layer earlier.

    Distinct ids are not sufficient, which is the Round-2 finding: the objects the
    menu actually produces are file names, and the map from id to file name is not
    injective. `Case-A` and `case-a` are two ids and one file on Windows, where the
    renderer would report four cases and write eight files. `verification_bundle` is
    a perfectly ordinary id whose `.json` is the renderer's own manifest, so the
    bundle digest it returns would no longer hash the file that digest names. Both
    are refused on the composed names rather than on the ids.
    """

    if not isinstance(value, list) or not value:
        raise _unauthorized("cases must be a non-empty ordered array")
    cases: list[Case] = []
    seen_ids: set[str] = set()
    seen_labels: set[str] = set()
    #: folded derived file name -> the `case_id` that composed it. Seeded with the
    #: renderer's two fixed names, which are claimed before any case is read.
    claimed_names: dict[str, str] = {}
    reserved_names = {_portable_fold(name) for name in BUNDLE_FILE_NAMES}
    for index, item in enumerate(value):
        where = f"cases[{index}]"
        block = _require_mapping(item, where, ("case_id", "display_label", "pair_id", "arms"))
        case_id = _require_leaf_token(block["case_id"], f"{where}.case_id")
        display_label = _require_str(block["display_label"], f"{where}.display_label")
        pair_id = _require_str(block["pair_id"], f"{where}.pair_id")
        if case_id in seen_ids:
            raise _unauthorized(f"{where}.case_id duplicates an earlier case: {case_id!r}")
        if display_label in seen_labels:
            raise _unauthorized(
                f"{where}.display_label duplicates an earlier menu entry: {display_label!r}"
            )
        for derived in _derived_case_file_names(case_id):
            folded = _portable_fold(derived)
            if folded in reserved_names:
                raise _unauthorized(
                    f"{where}.case_id would compose {derived!r}, which is one of the fixed "
                    f"bundle files the renderer writes into the same directory; got "
                    f"{case_id!r}"
                )
            owner = claimed_names.get(folded)
            if owner is not None:
                raise _unauthorized(
                    f"{where}.case_id would compose {derived!r}, which case {owner!r} already "
                    f"claims under the case-insensitive output namespace; got {case_id!r}"
                )
            claimed_names[folded] = case_id
        seen_ids.add(case_id)
        seen_labels.add(display_label)
        arms_block = _require_mapping(block["arms"], f"{where}.arms", SUITE_KEYS)
        arms = {
            suite: _parse_arm(
                arms_block[suite], f"{where}.arms.{suite}", suite=suite, split=split, pair_id=pair_id
            )
            for suite in SUITE_KEYS
        }
        cases.append(
            Case(
                case_id=case_id,
                display_label=display_label,
                pair_id=pair_id,
                arms=_frozen_mapping(arms),
            )
        )
    return tuple(cases)


def parse_connection_record(raw: bytes) -> ConnectionRecord:
    """Validate authenticated record bytes against the complete section-3.2 table.

    Args:
        raw: the bytes `authenticate_record_bytes` returned.

    Returns:
        The parsed, fully validated record. Nothing is opened, nothing is resolved
        against a filesystem and no default is supplied for any field.

    Raises:
        VerificationSceneError: `X_CONNECTION_UNAUTHORIZED` for any violation of the
            field table, any non-finite value, any non-canonical encoding and any
            rooted, drive-qualified or traversing path token.
    """

    document = _strict_json_object(raw)
    _require_mapping(document, "record", _TOP_LEVEL_FIELDS)

    version = _require_str(document["record_version"], "record_version")
    if version != CONNECTION_RECORD_VERSION:
        raise _unauthorized(
            f"record_version must be {CONNECTION_RECORD_VERSION!r}; got {version!r}"
        )

    authority = _require_str(document["authority"], "authority")
    if authority not in AUTHORITIES:
        raise _unauthorized(
            f"authority must be one of {', '.join(AUTHORITIES)}; got {authority!r}"
        )
    split = _require_str(document["split"], "split")
    if split not in SPLITS:
        raise _unauthorized(f"split must be one of {', '.join(SPLITS)}; got {split!r}")

    schema_block = _require_mapping(document["schema"], "schema", ("relative_path", "sha256"))
    schema = PacketArtifact(
        relative_path=_require_relative_path(
            schema_block["relative_path"], "schema.relative_path"
        ),
        sha256=_require_digest(schema_block["sha256"], "schema.sha256"),
    )

    config_block = _require_mapping(
        document["config"], "config", ("relative_path", "sha256", "config_hash")
    )
    config = ConfigRef(
        relative_path=_require_relative_path(
            config_block["relative_path"], "config.relative_path"
        ),
        sha256=_require_digest(config_block["sha256"], "config.sha256"),
        config_hash=_require_config_hash(config_block["config_hash"], "config.config_hash"),
    )

    data_root_block = _require_mapping(
        document["data_root"],
        "data_root",
        ("dataset_label", "manifest_sha256", "generation_audit", "independent_audit"),
    )
    data_root = DataRootRef(
        dataset_label=_require_pattern(
            data_root_block["dataset_label"], "data_root.dataset_label", _LABEL_PATTERN
        ),
        manifest_sha256=_require_digest(
            data_root_block["manifest_sha256"], "data_root.manifest_sha256"
        ),
        generation_audit=_parse_audit(
            data_root_block["generation_audit"], "data_root.generation_audit"
        ),
        independent_audit=_parse_audit(
            data_root_block["independent_audit"], "data_root.independent_audit"
        ),
    )

    result_block = _require_mapping(
        document["established_result"],
        "established_result",
        (
            "artifact_relative_path",
            "sha256",
            "split_field_path",
            "config_hash_field_path",
            "cases_field_path",
        ),
    )
    established_result = EstablishedResultRef(
        artifact_relative_path=_require_relative_path(
            result_block["artifact_relative_path"], "established_result.artifact_relative_path"
        ),
        sha256=_require_digest(result_block["sha256"], "established_result.sha256"),
        split_field_path=_require_str(
            result_block["split_field_path"], "established_result.split_field_path"
        ),
        config_hash_field_path=_require_str(
            result_block["config_hash_field_path"], "established_result.config_hash_field_path"
        ),
        cases_field_path=_require_str(
            result_block["cases_field_path"], "established_result.cases_field_path"
        ),
    )

    record = ConnectionRecord(
        record_version=version,
        record_label=_require_pattern(document["record_label"], "record_label", _LABEL_PATTERN),
        authority=authority,
        split=split,
        schema=schema,
        config=config,
        data_root=data_root,
        established_result=established_result,
        analysis_window_s=_require_positive_float(
            document["analysis_window_s"], "analysis_window_s"
        ),
        thresholds=_parse_thresholds(document["thresholds"]),
        model_selection=_parse_model_selection(document["model_selection"]),
        render_geometry=_parse_render_geometry(document["render_geometry"]),
        cases=_parse_cases(document["cases"], split=split),
        document=_freeze(document),
    )
    return record


def load_connection_record(path: Path, expected_sha256: str) -> ConnectionRecord:
    """Run read-order steps 1 and 2 together: authenticate, then interpret.

    Args:
        path: the `--connection-record` path.
        expected_sha256: the authorized `--connection-record-sha256` value.

    Returns:
        The validated record.

    Raises:
        VerificationSceneError: `X_CONNECTION_UNAUTHORIZED`. The order is the
            contract: the bytes are authenticated before they are parsed, so a record
            that is not the authorized one is never interpreted at all.
    """

    return parse_connection_record(authenticate_record_bytes(path, expected_sha256))


# --------------------------------------------------------------------------- #
# Step 3 -- root domains, the authority/split policy and the output parent.
# --------------------------------------------------------------------------- #
@dataclass(frozen=True)
class BoundPaths:
    """Every declared path resolved against its own root, with nothing opened.

    Attributes:
        packet_root: the resolved packet root the roles-mode entry point was given.
            Invariant W8: the public path supplies the live packet root derived from
            the module's own location, and no CLI argument, environment variable or
            record field may override it.
        role_root: the resolved `--role-root`, whose basename equals `dataset_label`.
        checkpoint_root: the resolved `--checkpoint-root`.
        record_path: the resolved `--connection-record`, required to be exactly
            `packet_root / record_relative_path(record_label)`. Section 3.1 gives the
            record one tracked location; without this binding the authorized bytes
            could be presented from anywhere, including from inside the tree step 21
            exclusively creates, which is the state finding CX exists to forbid.
        output_root: `<output-dir>/<record_label>/`, the exclusive-create destination.
        schema_path / config_path: packet-relative, resolved.
        packet_artifacts: every other packet-relative artifact the record names,
            keyed by the dotted record path that named it.
        role_payloads: `(case_id, suite, role) -> resolved payload path`.
        checkpoints: `(case_id, suite) -> resolved checkpoint path`.

    Every mapping is a read-only view for the same reason the record's own mappings
    are: an allowlist a later caller can edit is not an allowlist.
    """

    packet_root: Path
    role_root: Path
    checkpoint_root: Path
    record_path: Path
    output_root: Path
    schema_path: Path
    config_path: Path
    packet_artifacts: Mapping[str, Path]
    role_payloads: Mapping[tuple[str, str, str], Path]
    checkpoints: Mapping[tuple[str, str], Path]


def _resolve_safely(path: Path, *, where: str, code: str) -> Path:
    """Resolve one path, turning every resolution failure into a named refusal.

    Args:
        path: the path to resolve. It may name something that does not exist;
            `Path.resolve()` is non-strict and this module opens nothing.
        where: what the path is, in the refusal message.
        code: the refusal code this failure belongs to.

    Returns:
        The resolved path.

    Raises:
        VerificationSceneError: carrying `code`. `Path.resolve()` raises `ValueError`
            on an embedded NUL and `OSError` on several platform-specific shapes, and
            a raw exception out of a contract layer is a silent failure by another
            name -- the caller gets a traceback where the design specified an exit
            code. The step-2 component grammar refuses the reachable forms; this is
            the layer that keeps the unreachable ones named.
    """

    try:
        return Path(path).resolve()
    except (OSError, ValueError, RuntimeError) as exc:
        raise _refuse(code, f"{where} could not be resolved to a path: {exc}") from exc


def _resolve_under(root: Path, relative: PurePosixPath, *, where: str, code: str) -> Path:
    """Resolve one relative path under a root and require it to stay inside it.

    The token rules at step 2 already forbid `..`, rooted forms and drive
    designators, so this cannot fail on a well-formed record read from a plain
    filesystem. It runs anyway because containment is the property that matters and
    a token rule is an argument about spelling: a symlinked segment, a case-folding
    surprise or a future caller passing a root that is itself relative would all be
    caught here rather than one layer later, when the path is about to be opened.
    """

    candidate = _resolve_safely(root / Path(*relative.parts), where=where, code=code)
    if candidate != root and root not in candidate.parents:
        raise _refuse(
            code,
            f"{where} resolves to {candidate}, which is outside its declared root {root}",
        )
    return candidate


def bind_root_domains(
    record: ConnectionRecord,
    *,
    packet_root: Path,
    connection_record_path: Path,
    config_path: Path,
    role_root: Path,
    checkpoint_root: Path,
    output_dir: Path,
) -> BoundPaths:
    """Run read-order step 3: bind every path to its root, opening nothing.

    Args:
        record: the record `parse_connection_record` returned.
        packet_root: the one packet root that governs every packet-relative
            resolution in the read order (invariant W8). It is an explicit parameter
            precisely so that a test can bind an isolated temporary packet tree and
            still exercise this production branch rather than a parallel one.
        connection_record_path: the `--connection-record` argument -- the path step 1
            authenticated. Step 1 hashes whatever file it is handed, because that is
            what "a path is not an identity" means; step 3 is where the authenticated
            record is required to have come from the one tracked location section 3.1
            gives it.
        config_path: the `--config` argument.
        role_root: the `--role-root` argument.
        checkpoint_root: the `--checkpoint-root` argument.
        output_dir: the `--output-dir` argument.

    Returns:
        The bound paths, including the record's own path and
        `<output-dir>/<record_label>/`.

    Raises:
        VerificationSceneError: `X_SPLIT_FORBIDDEN` when the authority and the split
            disagree; `X_PROVENANCE_UNRESOLVED` when `--output-dir` is not the
            authority's mechanically fixed parent; `X_IDENTITY_MISMATCH` for every
            other binding failure -- a `--connection-record` that is not at the
            record's own tracked location, a `--config` that is not the record's
            declared file, a `--role-root` whose basename is not `dataset_label`, or
            any path that resolves outside its own root.

    The three codes are assigned by what the failure is *about*. A split under the
    wrong authority is a split refusal. A destination is a function of the
    authenticated authority, so a wrong one is a disagreement about provenance, not
    about a digest. Everything else is a claim that some named object is at some
    named place, and that is identity.
    """

    resolved_packet_root = _resolve_safely(
        packet_root, where="the packet root", code=X_IDENTITY_MISMATCH
    )
    resolved_role_root = _resolve_safely(
        role_root, where="--role-root", code=X_IDENTITY_MISMATCH
    )
    resolved_checkpoint_root = _resolve_safely(
        checkpoint_root, where="--checkpoint-root", code=X_IDENTITY_MISMATCH
    )
    resolved_output_dir = _resolve_safely(
        output_dir, where="--output-dir", code=X_PROVENANCE_UNRESOLVED
    )

    _require_authority_split_policy(record)

    # The authority's output parent is itself proved to be inside the injected packet
    # root rather than merely joined to it. A junction or symlink at any component of
    # `results/` would otherwise let a destination that compares equal to the expected
    # parent sit physically outside the packet, and the equality check would still be
    # satisfied -- the destination would be wrong in exactly the way W9 forbids while
    # every string in the comparison looked right.
    expected_parent = _resolve_under(
        resolved_packet_root,
        OUTPUT_PARENTS[record.authority],
        where=f"the {record.authority} output parent",
        code=X_PROVENANCE_UNRESOLVED,
    )
    if resolved_output_dir != expected_parent:
        raise _refuse(
            X_PROVENANCE_UNRESOLVED,
            f"--output-dir must be exactly {expected_parent} under authority "
            f"{record.authority}; got {resolved_output_dir}",
        )

    # Finding CX, enforced rather than only documented: the record lives at one
    # tracked packet-relative location, and that location is a sibling of the bundle
    # tree, never inside it. Binding it here is also what puts it into the section-4.2
    # expected open set, which is the only reason W3's set equality can be honest
    # about a file the adapter has already read.
    declared_record_path = _resolve_under(
        resolved_packet_root,
        record_relative_path(record.record_label),
        where="the connection record's tracked location",
        code=X_IDENTITY_MISMATCH,
    )
    resolved_record_path = _resolve_safely(
        connection_record_path, where="--connection-record", code=X_IDENTITY_MISMATCH
    )
    if resolved_record_path != declared_record_path:
        raise _refuse(
            X_IDENTITY_MISMATCH,
            f"--connection-record resolves to {resolved_record_path} but a record "
            f"labelled {record.record_label!r} lives at {declared_record_path}; the "
            "authorized bytes are not authorized from an arbitrary location",
        )

    if resolved_role_root.name != record.data_root.dataset_label:
        raise _refuse(
            X_IDENTITY_MISMATCH,
            f"--role-root basename is {resolved_role_root.name!r} but the record names "
            f"dataset_label {record.data_root.dataset_label!r}",
        )

    schema_path = _resolve_under(
        resolved_packet_root,
        record.schema.relative_path,
        where="schema.relative_path",
        code=X_IDENTITY_MISMATCH,
    )
    declared_config = _resolve_under(
        resolved_packet_root,
        record.config.relative_path,
        where="config.relative_path",
        code=X_IDENTITY_MISMATCH,
    )
    resolved_config = _resolve_safely(
        config_path, where="--config", code=X_IDENTITY_MISMATCH
    )
    if resolved_config != declared_config:
        raise _refuse(
            X_IDENTITY_MISMATCH,
            f"--config resolves to {resolved_config} but the record declares "
            f"{declared_config}; the argument names the authority-appropriate config the "
            "record already named, never a different file",
        )

    packet_artifacts: dict[str, Path] = {
        "established_result": _resolve_under(
            resolved_packet_root,
            record.established_result.artifact_relative_path,
            where="established_result.artifact_relative_path",
            code=X_IDENTITY_MISMATCH,
        ),
        "model_selection.source": _resolve_under(
            resolved_packet_root,
            record.model_selection.source.artifact_relative_path,
            where="model_selection.source.artifact_relative_path",
            code=X_IDENTITY_MISMATCH,
        ),
        "render_geometry.source": _resolve_under(
            resolved_packet_root,
            record.render_geometry.source.producer_relative_path,
            where="render_geometry.source.producer_relative_path",
            code=X_IDENTITY_MISMATCH,
        ),
        "render_geometry.tolerance_source": _resolve_under(
            resolved_packet_root,
            record.render_geometry.tolerance_source.artifact_relative_path,
            where="render_geometry.tolerance_source.artifact_relative_path",
            code=X_IDENTITY_MISMATCH,
        ),
    }
    for name, source in record.thresholds.sources.items():
        packet_artifacts[f"thresholds.sources.{name}"] = _resolve_under(
            resolved_packet_root,
            source.artifact_relative_path,
            where=f"thresholds.sources.{name}.artifact_relative_path",
            code=X_IDENTITY_MISMATCH,
        )

    role_payloads: dict[tuple[str, str, str], Path] = {}
    checkpoints: dict[tuple[str, str], Path] = {}
    for case in record.cases:
        for suite, arm in case.arms.items():
            checkpoints[(case.case_id, suite)] = _resolve_under(
                resolved_checkpoint_root,
                arm.checkpoint.relative_path,
                where=f"cases.{case.case_id}.arms.{suite}.checkpoint.relative_path",
                code=X_IDENTITY_MISMATCH,
            )
            for role, reference in arm.roles.items():
                role_payloads[(case.case_id, suite, role)] = _resolve_under(
                    resolved_role_root,
                    reference.payload_relative_path,
                    where=(
                        f"cases.{case.case_id}.arms.{suite}.roles.{role}"
                        ".payload_relative_path"
                    ),
                    code=X_IDENTITY_MISMATCH,
                )

    output_root = _resolve_under(
        resolved_output_dir,
        PurePosixPath(record.record_label),
        where="the output root <output-dir>/<record_label>",
        code=X_PROVENANCE_UNRESOLVED,
    )

    return BoundPaths(
        packet_root=resolved_packet_root,
        role_root=resolved_role_root,
        checkpoint_root=resolved_checkpoint_root,
        record_path=resolved_record_path,
        output_root=output_root,
        schema_path=schema_path,
        config_path=declared_config,
        packet_artifacts=_frozen_mapping(packet_artifacts),
        role_payloads=_frozen_mapping(role_payloads),
        checkpoints=_frozen_mapping(checkpoints),
    )


def _require_authority_split_policy(record: ConnectionRecord) -> None:
    """Require the fixed authority/split policy of design section 2.2.

    `DEVELOPMENT_ONLY` names `dev`, and nothing else. `FINAL` names the approved
    final split, and the one thing known about it before that approval exists is that
    it is not `dev` -- a final banner over the development split is precisely the
    conflation the banner exists to prevent. This deliberately does not narrow
    `FINAL` to one named split: choosing which confirmatory split is rendered is a
    later, separately approved decision, and encoding a guess here would make this
    contract the place that took it.
    """

    if record.authority == DEVELOPMENT_ONLY and record.split != "dev":
        raise _refuse(
            X_SPLIT_FORBIDDEN,
            f"a DEVELOPMENT_ONLY record names split {record.split!r}; it may name only 'dev'",
        )
    if record.authority == FINAL and record.split == "dev":
        raise _refuse(
            X_SPLIT_FORBIDDEN,
            "a FINAL record may not name the development split",
        )


def expected_open_set(record: ConnectionRecord, bound: BoundPaths) -> frozenset[Path]:
    """Return the exact set of files the adapter is permitted to open.

    Args:
        record: the authenticated record.
        bound: the result of `bind_root_domains`.

    Returns:
        The section-4.2 allowlist, derived from the record only after step 2 has
        validated every path domain: **the record itself**, the packet schema, the
        config, the four source/result artifacts plus both threshold sources, the
        manifest and both dataset audits at the role root, one `index.csv` per named
        role, and exactly the named payloads and checkpoints. Invariant W3 compares
        this set to the one an audit hook observes, **in both directions**: a test
        that only checked "nothing extra" would pass on an adapter that opened
        nothing at all.

        The record is in the set because section 4.2 puts it there and because the
        observed side cannot honestly leave it out -- step 1 opens the record, so an
        expected set without it makes the two sides unequal for a file the design
        requires to be read. That it is *already* read when this function runs is a
        statement about order, not about membership.

    This function does not touch the filesystem. It states what *may* be opened; the
    hook in the second half of sub-step 4b states what *was*.
    """

    paths: set[Path] = {bound.record_path, bound.schema_path, bound.config_path}
    paths.update(bound.packet_artifacts.values())
    paths.add(bound.role_root / "manifest.csv")
    paths.add(bound.role_root / "generation_audit.json")
    paths.add(bound.role_root / "independent_audit.json")
    paths.update(bound.role_payloads.values())
    paths.update(bound.checkpoints.values())
    for payload in bound.role_payloads.values():
        paths.add(payload.parent / "index.csv")
    return frozenset(paths)


def record_relative_path(record_label: str) -> PurePosixPath:
    """Return the packet-relative path of one connection record.

    Design finding CX: the record tree and the bundle tree are siblings under
    `results/verification_connection`, never nested, because step 21 exclusively
    creates `<output-dir>/<record_label>/` and refuses a non-empty root. Under the
    superseded nesting a `FINAL` invocation could never have reached exit 0, because
    the record it was authorized by had to be inside the directory it had to create.
    """

    label = _require_pattern(record_label, "record_label", _LABEL_PATTERN)
    return RECORD_PARENT / label / "connection_record.json"
