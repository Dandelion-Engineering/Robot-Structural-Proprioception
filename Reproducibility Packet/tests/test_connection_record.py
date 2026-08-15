"""Tests for the Slot-8 connection-record contract (read-order steps 1, 2 and 3).

Every refusal in `utils.connection_record` is driven by *constructing the state that
refuses*, never by asserting that a message exists -- that is invariant W2 of
`protocol/slot8-connection-record-v0.1.md` applied to the rows this half of sub-step
4b implements. Two further disciplines the packet already pays for are applied here:

  * where this module pins a fact another module owns -- the 20 schema-A field names,
    the four non-observation role names -- the test asserts **equality** against that
    owner, so a change over there goes red here instead of drifting;
  * the accept side is tested at every boundary the contract names, not only at the
    one boundary the first example happened to use, because a rule with no exercised
    accept side certifies nothing.

Nothing in this file opens a real role tree, a config, a checkpoint or a split. Every
path it builds lives under `tmp_path`.
"""

from __future__ import annotations

import copy
import hashlib
import json
import math
import os
import subprocess
import sys
from pathlib import Path, PurePosixPath
from typing import Any

import pytest

PACKET_ROOT = Path(__file__).resolve().parents[1]
SCRIPTS_DIR = PACKET_ROOT / "scripts"
sys.path.insert(0, str(SCRIPTS_DIR))

from utils.connection_record import (  # noqa: E402
    AUTHORITIES,
    CONNECTION_RECORD_VERSION,
    DEVELOPMENT_OUTPUT_PARENT,
    FINAL_OUTPUT_PARENT,
    LINK_IDS,
    MANIFEST_ROW_FIELDS,
    MANIFEST_ROW_INT_FIELDS,
    OUTPUT_PARENTS,
    RECORD_PARENT,
    ROLE_NAMES,
    SPLITS,
    authenticate_record_bytes,
    bind_root_domains,
    expected_open_set,
    load_connection_record,
    parse_connection_record,
    record_relative_path,
)
from utils.connection_record import (  # noqa: E402
    _freeze,
    _frozen_mapping,
    _resolve_safely,
    _resolve_under,
)
from utils.protocol_p import canonical_json  # noqa: E402
from utils.storage_contract import IDENTITY_MANIFEST_FIELDS  # noqa: E402
from utils.verification_scene import (  # noqa: E402
    DEVELOPMENT_ONLY,
    FINAL,
    SUITE_KEYS,
    SYNTHETIC_FIXTURE,
    VerificationSceneError,
    X_CONNECTION_UNAUTHORIZED,
    X_IDENTITY_MISMATCH,
    X_PROVENANCE_UNRESOLVED,
    X_SPLIT_FORBIDDEN,
)

DATASET_LABEL = "gate3-base-dev-pilot-val-c1-s"

#: 16 ordered bodies per link, so 15 internal deformation bodies and 45 coordinates
#: per link -- 90 in total, which is the `n_def` the machine schema declares.
BODIES_PER_LINK = 16


def _digest(seed: str) -> str:
    """Return one distinct, well-formed lowercase SHA-256 digest for a fixture."""

    return hashlib.sha256(seed.encode("utf-8")).hexdigest()


def _manifest_row(*, suite: str, run_id: str, pair_id: str, split: str) -> dict[str, Any]:
    """Build one complete echoed 20-field schema-A identity row."""

    row: dict[str, Any] = {}
    for index, name in enumerate(MANIFEST_ROW_FIELDS):
        if name in MANIFEST_ROW_INT_FIELDS:
            row[name] = index
        else:
            row[name] = f"{name}-value"
    row["suite"] = suite
    row["run_id"] = run_id
    row["pair_id"] = pair_id
    row["split"] = split
    row["schema_version"] = "1.0"
    row["config_hash"] = _digest("config-hash")
    return row


def _roles(prefix: str) -> dict[str, Any]:
    """Build the four non-observation role references for one arm."""

    return {
        role: {
            "index_sha256": _digest(f"{prefix}-{role}-index"),
            "payload_relative_path": f"{role}/{prefix}.npz",
            "payload_sha256": _digest(f"{prefix}-{role}-payload"),
        }
        for role in ROLE_NAMES
    }


def _arm(*, suite: str, case_id: str, pair_id: str, split: str) -> dict[str, Any]:
    """Build one C1 or S arm."""

    run_id = f"{case_id}-{suite.lower()}"
    return {
        "run_id": run_id,
        "manifest_row": _manifest_row(suite=suite, run_id=run_id, pair_id=pair_id, split=split),
        "checkpoint": {
            "relative_path": f"{run_id}.pt",
            "sha256": _digest(f"{run_id}-checkpoint"),
        },
        "roles": _roles(run_id),
    }


def _case(*, case_id: str, label: str, split: str) -> dict[str, Any]:
    """Build one menu case carrying both arms of one pair."""

    pair_id = f"pair-{case_id}"
    return {
        "case_id": case_id,
        "display_label": label,
        "pair_id": pair_id,
        "arms": {
            suite: _arm(suite=suite, case_id=case_id, pair_id=pair_id, split=split)
            for suite in SUITE_KEYS
        },
    }


def _links() -> dict[str, Any]:
    """Build the two-link chain in the order the producer emits its coordinates."""

    links: dict[str, Any] = {}
    cursor = 0
    for link_id in LINK_IDS:
        triplets = []
        for _ in range(BODIES_PER_LINK - 1):
            triplets.append([cursor, cursor + 1, cursor + 2])
            cursor += 3
        links[link_id] = {
            "segment_lengths_m": [0.02] * BODIES_PER_LINK,
            "deform_triplets": triplets,
        }
    return links


def valid_document(*, authority: str = FINAL, split: str = "val") -> dict[str, Any]:
    """Build one complete, valid connection-record document.

    The document is deliberately *not* a production record: every digest is a
    fixture digest of a label, every path names a file that does not exist, and
    nothing in it is approved. It exists so that each refusal test can perturb one
    field of a state that is otherwise accepted, which is what makes a refusal test a
    statement about that field.
    """

    config_relative = (
        "config.json" if authority == FINAL else "config/draft-config-v0.1.json"
    )
    config_hash = _digest("frozen") if authority == FINAL else f"dev-{_digest('draft')}"
    return {
        "record_version": CONNECTION_RECORD_VERSION,
        "record_label": "demo-record-1",
        "authority": authority,
        "split": split,
        "schema": {
            "relative_path": "schema/schema.json",
            "sha256": _digest("schema"),
        },
        "config": {
            "relative_path": config_relative,
            "sha256": _digest("config-file"),
            "config_hash": config_hash,
        },
        "data_root": {
            "dataset_label": DATASET_LABEL,
            "manifest_sha256": _digest("manifest"),
            "generation_audit": {
                "sha256": _digest("generation-audit"),
                "status": "PASS",
                "assignment_hash": _digest("assignment"),
                "config_hash": config_hash,
            },
            "independent_audit": {
                "sha256": _digest("independent-audit"),
                "status": "PASS",
                "assignment_hash": _digest("assignment"),
                "config_hash": config_hash,
            },
        },
        "established_result": {
            "artifact_relative_path": "results/established/established_result.json",
            "sha256": _digest("established-result"),
            "split_field_path": "inputs.split",
            "config_hash_field_path": "inputs.config_hash",
            "cases_field_path": "results.cases",
        },
        "analysis_window_s": 5.0,
        "thresholds": {
            "abstain_threshold": 0.6,
            "unknown_threshold": 0.8,
            "sources": {
                "abstain_threshold": {
                    "artifact_relative_path": "results/calibration/thresholds.json",
                    "sha256": _digest("thresholds"),
                    "field_path": "values.abstain_threshold",
                },
                "unknown_threshold": {
                    "artifact_relative_path": "results/calibration/thresholds.json",
                    "sha256": _digest("thresholds"),
                    "field_path": "values.unknown_threshold",
                },
            },
        },
        "model_selection": {
            "rung": 1,
            "width": 32,
            "source": {
                "artifact_relative_path": "results/capacity_selection/selection.json",
                "sha256": _digest("selection"),
                "rung_field_path": "selected.rung",
                "width_field_path": "selected.width",
            },
        },
        "render_geometry": {
            "derivation_version": "slot8-centerline-v0.1",
            "source": {
                "producer_relative_path": "scripts/utils/cable_mechanics.py",
                "producer_sha256": _digest("cable-mechanics"),
                "model_id": "cable-arm-v1",
            },
            "planar_convention": {
                "base_xy_m": [0.0, 0.0],
                "q_true_convention": "l1_absolute_l2_relative_to_distal_l1_tangent",
                "rotation_vector_component": 1,
                "projection": "model_xz_to_scene_xy",
            },
            "links": _links(),
            "distal_tolerance_m": 1.0e-4,
            "tolerance_source": {
                "artifact_relative_path": "results/geometry_validation/geometry.json",
                "sha256": _digest("geometry"),
                "maximum_deviation_field_path": "measured.maximum_deviation_m",
                "tolerance_field_path": "declared.distal_tolerance_m",
            },
        },
        "cases": [
            _case(case_id="case-a", label="Soften link 2 by 30%", split=split),
            _case(case_id="case-b", label="Weaken actuator 1", split=split),
        ],
    }


def record_bytes(document: dict[str, Any]) -> bytes:
    """Render one document to the canonical bytes a record file must carry."""

    return canonical_json(document).encode("utf-8")


def write_record(tmp_path: Path, document: dict[str, Any]) -> tuple[Path, str]:
    """Write one record file and return its path and its authorized digest."""

    raw = record_bytes(document)
    path = tmp_path / "connection_record.json"
    path.write_bytes(raw)
    return path, hashlib.sha256(raw).hexdigest()


def mutate(document: dict[str, Any], dotted: str, value: Any) -> dict[str, Any]:
    """Return a deep copy of `document` with one dotted path set to `value`.

    List indices are written as integers in the path, e.g. `cases.0.case_id`.
    """

    out = copy.deepcopy(document)
    cursor: Any = out
    parts = dotted.split(".")
    for part in parts[:-1]:
        cursor = cursor[int(part)] if part.isdigit() else cursor[part]
    last = parts[-1]
    if last.isdigit():
        cursor[int(last)] = value
    else:
        cursor[last] = value
    return out


def drop(document: dict[str, Any], dotted: str) -> dict[str, Any]:
    """Return a deep copy of `document` with one dotted path removed."""

    out = copy.deepcopy(document)
    cursor: Any = out
    parts = dotted.split(".")
    for part in parts[:-1]:
        cursor = cursor[int(part)] if part.isdigit() else cursor[part]
    del cursor[parts[-1]]
    return out


def refuse(document: dict[str, Any]) -> VerificationSceneError:
    """Parse one document and require it to refuse, returning the refusal."""

    with pytest.raises(VerificationSceneError) as excinfo:
        parse_connection_record(record_bytes(document))
    return excinfo.value


# --------------------------------------------------------------------------- #
# Fixtures for the step-3 root domains. Nothing below creates a real role tree:
# `bind_root_domains` resolves paths and opens nothing.
# --------------------------------------------------------------------------- #
@pytest.fixture()
def roots(tmp_path: Path) -> dict[str, Path]:
    """Build an isolated packet/role/checkpoint root triple under `tmp_path`."""

    packet_root = tmp_path / "packet"
    role_root = tmp_path / "roles" / DATASET_LABEL
    checkpoint_root = tmp_path / "checkpoints"
    for path in (packet_root, role_root, checkpoint_root):
        path.mkdir(parents=True)
    return {
        "packet_root": packet_root,
        "role_root": role_root,
        "checkpoint_root": checkpoint_root,
    }


def tracked_record_path(packet_root: Path, record_label: str) -> Path:
    """Return the one tracked location section 3.1 gives a record with this label."""

    return packet_root / Path(*record_relative_path(record_label).parts)


def bind(document: dict[str, Any], roots: dict[str, Path], **overrides: Any):
    """Parse a document and bind it against the isolated roots.

    The `connection_record_path` default is the record's own tracked location under
    the packet root being bound, because that is the only location step 3 accepts.
    """

    record = parse_connection_record(record_bytes(document))
    packet_root = overrides.pop("packet_root", roots["packet_root"])
    kwargs = {
        "packet_root": packet_root,
        "connection_record_path": tracked_record_path(packet_root, record.record_label),
        "config_path": packet_root / Path(*PurePosixPath(document["config"]["relative_path"]).parts),
        "role_root": roots["role_root"],
        "checkpoint_root": roots["checkpoint_root"],
        "output_dir": packet_root / Path(*OUTPUT_PARENTS[record.authority].parts),
    }
    kwargs.update(overrides)
    return record, bind_root_domains(record, **kwargs)


# --------------------------------------------------------------------------- #
# Step 1 -- the record's own identity.
# --------------------------------------------------------------------------- #
def test_step1_accepts_the_authorized_bytes_and_returns_them(tmp_path: Path) -> None:
    document = valid_document()
    path, digest = write_record(tmp_path, document)
    assert authenticate_record_bytes(path, digest) == record_bytes(document)


def test_step1_refuses_a_digest_that_is_not_one_lowercase_sha256(tmp_path: Path) -> None:
    path, digest = write_record(tmp_path, valid_document())
    for bad in ("", digest.upper(), digest[:63], digest + "0", "not-a-digest", None):
        with pytest.raises(VerificationSceneError) as excinfo:
            authenticate_record_bytes(path, bad)  # type: ignore[arg-type]
        assert excinfo.value.code == X_CONNECTION_UNAUTHORIZED
        # The sentence is asserted, not only the code: a bad digest would also fail
        # the byte comparison one line later, so a code-only assertion would pass
        # with this branch deleted and the form rule would be held by nothing.
        assert "--connection-record-sha256 must be one lowercase" in str(excinfo.value)


def test_step1_refuses_an_unreadable_record(tmp_path: Path) -> None:
    with pytest.raises(VerificationSceneError) as excinfo:
        authenticate_record_bytes(tmp_path / "absent.json", _digest("anything"))
    assert excinfo.value.code == X_CONNECTION_UNAUTHORIZED
    assert "could not be read" in str(excinfo.value)


def test_step1_refuses_bytes_that_are_not_the_authorized_ones(tmp_path: Path) -> None:
    path, digest = write_record(tmp_path, valid_document())
    path.write_bytes(record_bytes(mutate(valid_document(), "record_label", "demo-record-2")))
    with pytest.raises(VerificationSceneError) as excinfo:
        authenticate_record_bytes(path, digest)
    assert excinfo.value.code == X_CONNECTION_UNAUTHORIZED
    assert digest in str(excinfo.value)


def test_step1_runs_before_step2_so_an_unauthorized_record_is_never_interpreted(
    tmp_path: Path,
) -> None:
    """A record that is malformed *and* unauthorized refuses on its identity first."""

    malformed = drop(valid_document(), "cases")
    raw = record_bytes(malformed)
    path = tmp_path / "connection_record.json"
    path.write_bytes(raw)
    with pytest.raises(VerificationSceneError) as excinfo:
        load_connection_record(path, _digest("some-other-record"))
    assert "hashes to" in str(excinfo.value)
    assert "cases" not in str(excinfo.value)


def test_load_connection_record_returns_the_parsed_record(tmp_path: Path) -> None:
    document = valid_document()
    path, digest = write_record(tmp_path, document)
    record = load_connection_record(path, digest)
    assert record.record_label == "demo-record-1"
    assert record.authority == FINAL
    assert record.split == "val"
    # The stored document is deeply frozen, so its arrays are tuples and `==` against
    # the source dict is False wherever an array appears. Equality is stated by
    # freezing the source the same way -- a real structural comparison, not a
    # comparison of two renderings that could both be wrong in the same direction.
    assert record.document == _freeze(document)
    assert record.document["record_label"] == "demo-record-1"


# --------------------------------------------------------------------------- #
# Step 2 -- encoding.
# --------------------------------------------------------------------------- #
def test_step2_accepts_the_canonical_rendering_and_exposes_typed_values() -> None:
    record = parse_connection_record(record_bytes(valid_document()))
    assert record.record_version == CONNECTION_RECORD_VERSION
    assert record.analysis_window_s == pytest.approx(5.0)
    assert record.schema.relative_path == PurePosixPath("schema/schema.json")
    assert record.thresholds.sources["abstain_threshold"].field_path == "values.abstain_threshold"
    assert record.model_selection.rung == 1
    assert record.render_geometry.planar_convention.rotation_vector_component == 1
    assert tuple(case.case_id for case in record.cases) == ("case-a", "case-b")
    assert set(record.cases[0].arms) == set(SUITE_KEYS)
    assert set(record.cases[0].arms["C1"].roles) == set(ROLE_NAMES)


def test_step2_refuses_a_byte_order_mark() -> None:
    raw = b"\xef\xbb\xbf" + record_bytes(valid_document())
    with pytest.raises(VerificationSceneError) as excinfo:
        parse_connection_record(raw)
    assert "byte order mark" in str(excinfo.value)


@pytest.mark.parametrize("suffix", [b"\n", b"\r\n", b"\r"])
def test_step2_refuses_a_trailing_newline(suffix: bytes) -> None:
    """The sentence is asserted because the canonical round-trip also refuses this.

    Its message names "no trailing newline" too, so asserting the word alone would
    pass with this branch deleted and hold nothing.
    """

    with pytest.raises(VerificationSceneError) as excinfo:
        parse_connection_record(record_bytes(valid_document()) + suffix)
    assert "must not end with a newline" in str(excinfo.value)


def test_step2_refuses_invalid_utf8() -> None:
    with pytest.raises(VerificationSceneError) as excinfo:
        parse_connection_record(b'{"a"\xff:1}')
    assert "UTF-8" in str(excinfo.value)


def test_step2_refuses_a_duplicate_key() -> None:
    raw = b'{"record_version":"a","record_version":"b"}'
    with pytest.raises(VerificationSceneError) as excinfo:
        parse_connection_record(raw)
    assert "duplicate JSON key" in str(excinfo.value)


@pytest.mark.parametrize("token", ["NaN", "Infinity", "-Infinity"])
def test_step2_refuses_a_non_finite_json_constant(token: str) -> None:
    raw = ('{"analysis_window_s":' + token + "}").encode("utf-8")
    with pytest.raises(VerificationSceneError) as excinfo:
        parse_connection_record(raw)
    assert "non-finite JSON constant" in str(excinfo.value)


def test_step2_refuses_an_overflowing_literal_that_parse_constant_never_sees() -> None:
    """`json.loads('1e9999')` yields `inf` without calling the constant hook.

    This is the Session-67 shape: a value the standard parser accepts and canonical
    JSON cannot represent. The refusal must therefore come from the value walk, not
    from `parse_constant`, and the message says so.
    """

    assert json.loads("1e9999") == float("inf")
    raw = b'{"analysis_window_s":1e9999}'
    with pytest.raises(VerificationSceneError) as excinfo:
        parse_connection_record(raw)
    assert "non-finite number" in str(excinfo.value)
    assert "non-finite JSON constant" not in str(excinfo.value)


def test_step2_refuses_a_pretty_printed_record() -> None:
    raw = json.dumps(valid_document(), indent=2, sort_keys=True).encode("utf-8")
    with pytest.raises(VerificationSceneError) as excinfo:
        parse_connection_record(raw)
    assert "canonical JSON rendering" in str(excinfo.value)


def test_step2_refuses_an_unsorted_record() -> None:
    document = valid_document()
    raw = json.dumps(document, sort_keys=False, separators=(",", ":")).encode("utf-8")
    if raw == record_bytes(document):  # pragma: no cover - the fixture is not sorted
        pytest.skip("the fixture document happens to be in sorted order")
    with pytest.raises(VerificationSceneError) as excinfo:
        parse_connection_record(raw)
    assert "canonical JSON rendering" in str(excinfo.value)


@pytest.mark.parametrize("raw", [b"[]", b'"text"', b"7", b"null"])
def test_step2_refuses_a_document_that_is_not_one_object(raw: bytes) -> None:
    with pytest.raises(VerificationSceneError) as excinfo:
        parse_connection_record(raw)
    assert excinfo.value.code == X_CONNECTION_UNAUTHORIZED


def test_step2_refuses_invalid_json() -> None:
    with pytest.raises(VerificationSceneError) as excinfo:
        parse_connection_record(b"{")
    assert "valid JSON" in str(excinfo.value)


# --------------------------------------------------------------------------- #
# Step 2 -- the field table.
# --------------------------------------------------------------------------- #
@pytest.mark.parametrize(
    "field",
    [
        "record_version",
        "record_label",
        "authority",
        "split",
        "schema",
        "config",
        "data_root",
        "established_result",
        "analysis_window_s",
        "thresholds",
        "model_selection",
        "render_geometry",
        "cases",
    ],
)
def test_step2_refuses_an_absent_top_level_field(field: str) -> None:
    """There is no optional field: an absent one is a refusal, not an empty value."""

    error = refuse(drop(valid_document(), field))
    assert error.code == X_CONNECTION_UNAUTHORIZED
    assert field in str(error)


def test_step2_refuses_an_unexpected_top_level_field() -> None:
    error = refuse(mutate(valid_document(), "approved_by", "codex"))
    assert "unexpected field" in str(error)


def test_step2_refuses_an_approval_shaped_field_anywhere(
) -> None:
    """Invariant W12: a record may not certify its own authorization.

    The exact-key rule is what enforces this, so the check is that an
    approval-shaped field is refused wherever it is added rather than tolerated in
    some block that happens to be loosely validated.
    """

    for dotted in ("authorized", "approval_session", "config.approved_by"):
        error = refuse(mutate(valid_document(), dotted, True))
        assert "unexpected field" in str(error)


def test_step2_refuses_a_wrong_record_version() -> None:
    error = refuse(mutate(valid_document(), "record_version", "slot8-connection-record-v0.2"))
    assert "record_version" in str(error)


@pytest.mark.parametrize("authority", [SYNTHETIC_FIXTURE, "final", "", "DEVELOPMENT", 1])
def test_step2_refuses_an_authority_outside_the_two(authority: Any) -> None:
    """`SYNTHETIC_FIXTURE` is a provenance state, never an authority a record claims."""

    error = refuse(mutate(valid_document(), "authority", authority))
    assert error.code == X_CONNECTION_UNAUTHORIZED


@pytest.mark.parametrize("authority", list(AUTHORITIES))
def test_step2_accepts_both_authorities(authority: str) -> None:
    split = "dev" if authority == DEVELOPMENT_ONLY else "val"
    record = parse_connection_record(record_bytes(valid_document(authority=authority, split=split)))
    assert record.authority == authority


@pytest.mark.parametrize("split", list(SPLITS))
def test_step2_accepts_every_declared_split(split: str) -> None:
    record = parse_connection_record(record_bytes(valid_document(split=split)))
    assert record.split == split


@pytest.mark.parametrize("split", ["train", "DEV", "", "validation"])
def test_step2_refuses_an_undeclared_split(split: str) -> None:
    """Asserted by sentence: an undeclared split also fails the per-arm echo check."""

    error = refuse(mutate(valid_document(), "split", split))
    assert error.code == X_CONNECTION_UNAUTHORIZED
    assert "split must be one of" in str(error) or "must be a non-empty string" in str(error)


@pytest.mark.parametrize("label", ["Demo", "demo_record", "demo record", "", "demo.record"])
def test_step2_refuses_a_record_label_outside_the_pattern(label: str) -> None:
    assert "record_label" in str(refuse(mutate(valid_document(), "record_label", label)))


@pytest.mark.parametrize(
    "dotted",
    [
        "schema.sha256",
        "config.sha256",
        "data_root.manifest_sha256",
        "data_root.generation_audit.sha256",
        "established_result.sha256",
        "model_selection.source.sha256",
        "render_geometry.source.producer_sha256",
        "render_geometry.tolerance_source.sha256",
        "cases.0.arms.C1.checkpoint.sha256",
        "cases.0.arms.C1.roles.plant.index_sha256",
        "cases.0.arms.C1.roles.plant.payload_sha256",
    ],
)
def test_step2_refuses_a_malformed_digest_at_every_declared_position(dotted: str) -> None:
    error = refuse(mutate(valid_document(), dotted, "0" * 63))
    assert "SHA-256" in str(error)


def test_step2_accepts_a_draft_config_hash_and_refuses_a_malformed_one() -> None:
    good = mutate(valid_document(), "config.config_hash", f"dev-{_digest('draft')}")
    assert parse_connection_record(record_bytes(good)).config.config_hash.startswith("dev-")
    assert "SHA-256" in str(refuse(mutate(valid_document(), "config.config_hash", "dev-nope")))


@pytest.mark.parametrize("value", [0.0, -1.0, "5.0", True, None])
def test_step2_refuses_a_non_positive_analysis_window(value: Any) -> None:
    assert refuse(mutate(valid_document(), "analysis_window_s", value)).code == (
        X_CONNECTION_UNAUTHORIZED
    )


def test_step2_accepts_an_integer_literal_for_a_float_field() -> None:
    record = parse_connection_record(record_bytes(mutate(valid_document(), "analysis_window_s", 5)))
    assert record.analysis_window_s == pytest.approx(5.0)


@pytest.mark.parametrize(
    ("path", "phrase"),
    [
        ("/etc/passwd", "must be relative, not rooted"),
        ("/", "must be relative, not rooted"),
        ("C:/packet/schema.json", "must not carry a drive designator"),
        ("c:schema.json", "must not carry a drive designator"),
        ("schema\\schema.json", "must use forward slashes"),
        ("../schema/schema.json", "must not contain a '..' segment"),
        ("schema/../../schema.json", "must not contain a '..' segment"),
        ("schema/./schema.json", "must not contain a '.' segment"),
        ("schema//schema.json", "must not contain an empty path segment"),
        ("schema/schema.json/", "must not end with a separator"),
        ("", "must be a non-empty string"),
    ],
)
def test_step2_refuses_every_forbidden_path_token(path: str, phrase: str) -> None:
    """The schema calls this rule `project_relative_no_parent_traversal`.

    Each case asserts the sentence its own branch raises. Several of the branches
    overlap -- a rooted path also produces an empty first segment -- so a code-only
    assertion stays green with a branch deleted and holds nothing. Measured: the
    rooted branch was a mutation survivor until this test named its sentence.
    """

    error = refuse(mutate(valid_document(), "schema.relative_path", path))
    assert error.code == X_CONNECTION_UNAUTHORIZED
    assert phrase in str(error)


@pytest.mark.parametrize(
    "dotted",
    [
        "schema.relative_path",
        "config.relative_path",
        "established_result.artifact_relative_path",
        "thresholds.sources.abstain_threshold.artifact_relative_path",
        "model_selection.source.artifact_relative_path",
        "render_geometry.source.producer_relative_path",
        "render_geometry.tolerance_source.artifact_relative_path",
        "cases.0.arms.S.checkpoint.relative_path",
        "cases.0.arms.S.roles.labels.payload_relative_path",
    ],
)
def test_step2_applies_the_path_rule_at_every_declared_position(dotted: str) -> None:
    assert refuse(mutate(valid_document(), dotted, "../escape.json")).code == (
        X_CONNECTION_UNAUTHORIZED
    )


# --------------------------------------------------------------------------- #
# Step 2 -- thresholds, selection and geometry.
# --------------------------------------------------------------------------- #
def test_step2_refuses_two_thresholds_proved_by_one_field() -> None:
    document = mutate(
        valid_document(),
        "thresholds.sources.unknown_threshold.field_path",
        "values.abstain_threshold",
    )
    assert "one number" in str(refuse(document))


def test_step2_accepts_two_thresholds_from_one_artifact_at_two_fields() -> None:
    record = parse_connection_record(record_bytes(valid_document()))
    abstain = record.thresholds.sources["abstain_threshold"]
    unknown = record.thresholds.sources["unknown_threshold"]
    assert abstain.artifact_relative_path == unknown.artifact_relative_path
    assert abstain.field_path != unknown.field_path


def test_step2_refuses_a_selection_naming_one_field_for_rung_and_width() -> None:
    document = mutate(valid_document(), "model_selection.source.width_field_path", "selected.rung")
    assert "must differ" in str(refuse(document))


@pytest.mark.parametrize("value", [0, -1, 1.0, "1", True])
def test_step2_refuses_a_non_positive_integer_rung(value: Any) -> None:
    assert refuse(mutate(valid_document(), "model_selection.rung", value)).code == (
        X_CONNECTION_UNAUTHORIZED
    )


@pytest.mark.parametrize("component", [3, -1, 1.0, "1", True])
def test_step2_refuses_a_rotation_vector_component_outside_the_log_map(component: Any) -> None:
    document = mutate(
        valid_document(), "render_geometry.planar_convention.rotation_vector_component", component
    )
    assert refuse(document).code == X_CONNECTION_UNAUTHORIZED


@pytest.mark.parametrize("component", [0, 1, 2])
def test_step2_accepts_every_log_map_component(component: int) -> None:
    document = mutate(
        valid_document(), "render_geometry.planar_convention.rotation_vector_component", component
    )
    record = parse_connection_record(record_bytes(document))
    assert record.render_geometry.planar_convention.rotation_vector_component == component


@pytest.mark.parametrize("base", [[0.0], [0.0, 0.0, 0.0], "0,0", [0.0, "0"]])
def test_step2_refuses_a_base_point_that_is_not_two_numbers(base: Any) -> None:
    document = mutate(valid_document(), "render_geometry.planar_convention.base_xy_m", base)
    assert refuse(document).code == X_CONNECTION_UNAUTHORIZED


@pytest.mark.parametrize("version", ["Slot8", "-v1", "", "slot8 v1"])
def test_step2_refuses_a_derivation_version_outside_the_pattern(version: str) -> None:
    document = mutate(valid_document(), "render_geometry.derivation_version", version)
    assert "derivation_version" in str(refuse(document))


def test_step2_refuses_a_tolerance_source_reading_one_field_twice() -> None:
    document = mutate(
        valid_document(),
        "render_geometry.tolerance_source.maximum_deviation_field_path",
        "declared.distal_tolerance_m",
    )
    assert "vacuous" in str(refuse(document))


@pytest.mark.parametrize("value", [0.0, -1.0e-4])
def test_step2_refuses_a_non_positive_distal_tolerance(value: float) -> None:
    document = mutate(valid_document(), "render_geometry.distal_tolerance_m", value)
    assert refuse(document).code == X_CONNECTION_UNAUTHORIZED


def test_step2_refuses_a_chain_that_is_not_both_links() -> None:
    document = drop(valid_document(), "render_geometry.links.L2")
    assert "L2" in str(refuse(document))


def test_step2_refuses_a_third_link() -> None:
    document = mutate(valid_document(), "render_geometry.links.L3", valid_document()["render_geometry"]["links"]["L1"])
    assert "unexpected field" in str(refuse(document))


def test_step2_refuses_a_link_whose_triplet_count_does_not_match_its_bodies() -> None:
    document = valid_document()
    document["render_geometry"]["links"]["L1"]["deform_triplets"].pop()
    error = refuse(document)
    assert "the first body of each link carries no internal deformation" in str(error)


def test_step2_refuses_a_link_with_fewer_than_two_bodies() -> None:
    document = valid_document()
    document["render_geometry"]["links"]["L1"]["segment_lengths_m"] = [0.02]
    document["render_geometry"]["links"]["L1"]["deform_triplets"] = []
    assert "at least two" in str(refuse(document))


def test_step2_refuses_triplets_that_are_not_the_emitted_layout() -> None:
    """`extract_deformation_coordinates` emits L1's internal bodies, then L2's."""

    document = valid_document()
    first = document["render_geometry"]["links"]["L1"]["deform_triplets"]
    first[0], first[1] = first[1], first[0]
    assert "contiguous zero-based layout" in str(refuse(document))


def test_step2_refuses_triplets_that_restart_per_link() -> None:
    document = valid_document()
    second = document["render_geometry"]["links"]["L2"]["deform_triplets"]
    document["render_geometry"]["links"]["L2"]["deform_triplets"] = [
        [index * 3, index * 3 + 1, index * 3 + 2] for index in range(len(second))
    ]
    assert "contiguous zero-based layout" in str(refuse(document))


def test_step2_accepts_the_ninety_coordinate_chain_the_schema_declares() -> None:
    record = parse_connection_record(record_bytes(valid_document()))
    coordinates = sum(
        len(link.deform_triplets) * 3 for link in record.render_geometry.links.values()
    )
    assert coordinates == 90


@pytest.mark.parametrize("triplet", [[0, 1], [0, 1, 2, 3], [0, 1, -1], [0, 1, "2"], [0, 1, True]])
def test_step2_refuses_a_malformed_triplet(triplet: Any) -> None:
    document = valid_document()
    document["render_geometry"]["links"]["L1"]["deform_triplets"][0] = triplet
    assert refuse(document).code == X_CONNECTION_UNAUTHORIZED


@pytest.mark.parametrize("length", [0.0, -0.02, "0.02"])
def test_step2_refuses_a_non_positive_segment_length(length: Any) -> None:
    document = valid_document()
    document["render_geometry"]["links"]["L1"]["segment_lengths_m"][0] = length
    assert refuse(document).code == X_CONNECTION_UNAUTHORIZED


# --------------------------------------------------------------------------- #
# Step 2 -- cases, arms and the echoed manifest rows.
# --------------------------------------------------------------------------- #
def test_step2_refuses_an_empty_menu() -> None:
    assert "non-empty" in str(refuse(mutate(valid_document(), "cases", [])))


def test_step2_refuses_a_duplicate_case_id() -> None:
    document = mutate(valid_document(), "cases.1.case_id", "case-a")
    assert "duplicates an earlier case" in str(refuse(document))


def test_step2_refuses_a_duplicate_display_label() -> None:
    document = mutate(valid_document(), "cases.1.display_label", "Soften link 2 by 30%")
    assert "duplicates an earlier menu entry" in str(refuse(document))


def test_step2_accepts_a_single_case_menu() -> None:
    document = valid_document()
    document["cases"] = document["cases"][:1]
    assert len(parse_connection_record(record_bytes(document)).cases) == 1


@pytest.mark.parametrize("suite", list(SUITE_KEYS))
def test_step2_refuses_a_case_missing_an_arm(suite: str) -> None:
    document = drop(valid_document(), f"cases.0.arms.{suite}")
    assert suite in str(refuse(document))


def test_step2_refuses_a_third_arm() -> None:
    document = valid_document()
    document["cases"][0]["arms"]["C0"] = document["cases"][0]["arms"]["C1"]
    assert "unexpected field" in str(refuse(document))


@pytest.mark.parametrize("field", list(MANIFEST_ROW_FIELDS))
def test_step2_refuses_an_absent_manifest_field(field: str) -> None:
    """Invariant W4: all 20 schema-A fields are echoed, so all 20 can be compared."""

    error = refuse(drop(valid_document(), f"cases.0.arms.C1.manifest_row.{field}"))
    assert field in str(error)


def test_step2_refuses_an_extra_manifest_field() -> None:
    document = mutate(valid_document(), "cases.0.arms.C1.manifest_row.extra", "value")
    assert "unexpected field" in str(refuse(document))


@pytest.mark.parametrize("field", sorted(MANIFEST_ROW_INT_FIELDS))
def test_step2_refuses_a_seed_field_that_is_not_an_integer(field: str) -> None:
    document = mutate(valid_document(), f"cases.0.arms.C1.manifest_row.{field}", "3")
    assert "JSON integer" in str(refuse(document))


def test_step2_refuses_a_boolean_seed() -> None:
    document = mutate(valid_document(), "cases.0.arms.C1.manifest_row.sim_seed", True)
    assert "JSON integer" in str(refuse(document))


def test_step2_refuses_a_string_field_carrying_a_number() -> None:
    document = mutate(valid_document(), "cases.0.arms.C1.manifest_row.estimator_id", 7)
    assert "non-empty string" in str(refuse(document))


def test_step2_refuses_an_arm_whose_row_echoes_the_other_suite() -> None:
    document = mutate(valid_document(), "cases.0.arms.C1.manifest_row.suite", "S")
    assert "under the 'C1' arm" in str(refuse(document))


def test_step2_refuses_an_arm_whose_row_echoes_a_different_run() -> None:
    document = mutate(valid_document(), "cases.0.arms.C1.manifest_row.run_id", "other-run")
    assert "but the arm names" in str(refuse(document))


def test_step2_refuses_an_arm_whose_row_echoes_a_different_pair() -> None:
    document = mutate(valid_document(), "cases.0.arms.C1.manifest_row.pair_id", "pair-other")
    assert "but the case names" in str(refuse(document))


def test_step2_refuses_an_arm_whose_row_echoes_a_different_split() -> None:
    """Design property 6: one record, one split, one authority."""

    document = mutate(valid_document(), "cases.0.arms.C1.manifest_row.split", "pilot")
    assert "but the record names" in str(refuse(document))


@pytest.mark.parametrize("role", list(ROLE_NAMES))
def test_step2_refuses_an_arm_missing_a_role(role: str) -> None:
    assert role in str(refuse(drop(valid_document(), f"cases.0.arms.C1.roles.{role}")))


def test_step2_refuses_an_observations_role() -> None:
    """The field table names four non-observation roles and no fifth."""

    document = mutate(
        valid_document(),
        "cases.0.arms.C1.roles.observations",
        valid_document()["cases"][0]["arms"]["C1"]["roles"]["plant"],
    )
    assert "unexpected field" in str(refuse(document))


# --------------------------------------------------------------------------- #
# Equality against the modules that own these facts.
# --------------------------------------------------------------------------- #
def test_manifest_fields_equal_the_storage_contract_definition() -> None:
    assert MANIFEST_ROW_FIELDS == IDENTITY_MANIFEST_FIELDS
    assert len(MANIFEST_ROW_FIELDS) == 20


def test_role_names_equal_the_schema_derived_set() -> None:
    """The record's four roles are the schema's roles minus manifest and observations.

    The module states the tuple as a literal because step 2 runs before the schema is
    authenticated at step 4. This test is the equality check that keeps the literal
    honest -- it may open the schema because it is a test, not the adapter's read
    order.
    """

    schema = json.loads((PACKET_ROOT / "schema" / "schema.json").read_text(encoding="utf-8"))
    derived = set(schema["roles"]) - {"identity_manifest", "observations"}
    assert set(ROLE_NAMES) == derived


def test_output_parents_cover_exactly_the_two_authorities() -> None:
    assert set(OUTPUT_PARENTS) == set(AUTHORITIES)


def test_record_tree_is_not_inside_either_output_parent() -> None:
    """Finding CX: the exclusive create is what makes nesting fatal, not untidy.

    Step 21 exclusively creates `<output-dir>/<record_label>/` and refuses a
    non-empty root, while the record has to exist and be reviewed before the
    authorization that names its digest. If the record tree were inside the output
    parent, a `FINAL` invocation could never have reached exit 0.
    """

    record_path = record_relative_path("demo-record-1")
    for parent in OUTPUT_PARENTS.values():
        assert not record_path.is_relative_to(parent)
        assert not parent.is_relative_to(RECORD_PARENT)
    assert RECORD_PARENT.parent == FINAL_OUTPUT_PARENT.parent
    assert not DEVELOPMENT_OUTPUT_PARENT.is_relative_to(RECORD_PARENT.parent)


def test_record_relative_path_refuses_a_label_outside_the_pattern() -> None:
    with pytest.raises(VerificationSceneError):
        record_relative_path("Demo Record")


# --------------------------------------------------------------------------- #
# Step 3 -- root domains.
# --------------------------------------------------------------------------- #
def test_step3_binds_every_declared_path_to_its_own_root(roots: dict[str, Path]) -> None:
    document = valid_document()
    record, bound = bind(document, roots)
    assert bound.packet_root == roots["packet_root"]
    assert bound.schema_path == roots["packet_root"] / "schema" / "schema.json"
    assert bound.config_path == roots["packet_root"] / "config.json"
    assert bound.output_root == (
        roots["packet_root"] / Path(*FINAL_OUTPUT_PARENT.parts) / record.record_label
    )
    assert bound.checkpoints[("case-a", "C1")] == roots["checkpoint_root"] / "case-a-c1.pt"
    assert bound.role_payloads[("case-a", "C1", "plant")] == (
        roots["role_root"] / "plant" / "case-a-c1.npz"
    )
    assert set(bound.packet_artifacts) == {
        "established_result",
        "model_selection.source",
        "render_geometry.source",
        "render_geometry.tolerance_source",
        "thresholds.sources.abstain_threshold",
        "thresholds.sources.unknown_threshold",
    }
    for path in bound.packet_artifacts.values():
        assert path.is_relative_to(roots["packet_root"])


def test_step3_binds_the_development_authority_to_its_own_parent(roots: dict[str, Path]) -> None:
    document = valid_document(authority=DEVELOPMENT_ONLY, split="dev")
    record, bound = bind(document, roots)
    assert bound.output_root == (
        roots["packet_root"] / Path(*DEVELOPMENT_OUTPUT_PARENT.parts) / record.record_label
    )


def test_step3_refuses_a_development_bundle_aimed_at_the_publication_tree(
    roots: dict[str, Path],
) -> None:
    """Invariant W9, driven rather than asserted."""

    document = valid_document(authority=DEVELOPMENT_ONLY, split="dev")
    with pytest.raises(VerificationSceneError) as excinfo:
        bind(
            document,
            roots,
            output_dir=roots["packet_root"] / Path(*FINAL_OUTPUT_PARENT.parts),
        )
    assert excinfo.value.code == X_PROVENANCE_UNRESOLVED


@pytest.mark.parametrize(
    "relative", ["results", "results/other", "results/verification_connection", "."]
)
def test_step3_refuses_every_other_project_relative_destination(
    roots: dict[str, Path], relative: str
) -> None:
    with pytest.raises(VerificationSceneError) as excinfo:
        bind(valid_document(), roots, output_dir=roots["packet_root"] / relative)
    assert excinfo.value.code == X_PROVENANCE_UNRESOLVED


def test_step3_refuses_a_role_root_whose_basename_is_not_the_dataset_label(
    roots: dict[str, Path], tmp_path: Path
) -> None:
    other = tmp_path / "roles" / "some-other-dataset"
    other.mkdir(parents=True)
    with pytest.raises(VerificationSceneError) as excinfo:
        bind(valid_document(), roots, role_root=other)
    assert excinfo.value.code == X_IDENTITY_MISMATCH
    assert "dataset_label" in str(excinfo.value)


def test_step3_refuses_a_config_argument_naming_a_different_file(
    roots: dict[str, Path],
) -> None:
    with pytest.raises(VerificationSceneError) as excinfo:
        bind(valid_document(), roots, config_path=roots["packet_root"] / "other-config.json")
    assert excinfo.value.code == X_IDENTITY_MISMATCH
    assert "--config" in str(excinfo.value)


def test_step3_refuses_a_config_argument_outside_the_packet(
    roots: dict[str, Path], tmp_path: Path
) -> None:
    with pytest.raises(VerificationSceneError) as excinfo:
        bind(valid_document(), roots, config_path=tmp_path / "config.json")
    assert excinfo.value.code == X_IDENTITY_MISMATCH


def test_step3_refuses_a_development_record_naming_a_non_development_split(
    roots: dict[str, Path],
) -> None:
    for split in ("pilot", "val", "test"):
        document = valid_document(authority=DEVELOPMENT_ONLY, split=split)
        with pytest.raises(VerificationSceneError) as excinfo:
            bind(document, roots)
        assert excinfo.value.code == X_SPLIT_FORBIDDEN


def test_step3_refuses_a_final_record_naming_the_development_split(
    roots: dict[str, Path],
) -> None:
    document = valid_document(authority=FINAL, split="dev")
    with pytest.raises(VerificationSceneError) as excinfo:
        bind(document, roots)
    assert excinfo.value.code == X_SPLIT_FORBIDDEN


@pytest.mark.parametrize("split", ["pilot", "val", "test"])
def test_step3_accepts_every_non_development_split_under_final(
    roots: dict[str, Path], split: str
) -> None:
    """`FINAL` is deliberately not narrowed to one named split by this contract."""

    record, _ = bind(valid_document(authority=FINAL, split=split), roots)
    assert record.split == split


def test_step3_takes_the_packet_root_as_an_explicit_parameter(roots: dict[str, Path]) -> None:
    """Invariant W8: one injected root governs every packet-relative resolution.

    Binding an isolated second packet root must move the schema, the config, every
    source artifact and the output parent together. A seam that moved only some of
    them would leave the rest resolving against the live packet, which is the
    root-substitution hazard rather than the cure for it.
    """

    other_packet = roots["packet_root"].parent / "other-packet"
    other_packet.mkdir()
    _, bound = bind(valid_document(), roots, packet_root=other_packet)
    assert bound.packet_root == other_packet
    assert bound.schema_path.is_relative_to(other_packet)
    assert bound.config_path.is_relative_to(other_packet)
    assert bound.output_root.is_relative_to(other_packet)
    for path in bound.packet_artifacts.values():
        assert path.is_relative_to(other_packet)


def test_step3_containment_guard_refuses_a_path_that_escapes_its_root(
    roots: dict[str, Path],
) -> None:
    """The second layer under the step-2 token rule, held by a direct unit test.

    No well-formed record can reach this branch: `_require_relative_path` already
    refuses every `..` segment, rooted form and drive designator. The guard exists
    because a token rule is an argument about spelling while containment is the
    property that matters, and because a future caller could hand this helper a root
    it did not derive. Driving it directly is what keeps it from being a comment --
    it was a mutation survivor until this test existed, and a guard no mutation can
    break is a guard nothing checks.
    """

    with pytest.raises(VerificationSceneError) as excinfo:
        _resolve_under(
            roots["packet_root"],
            PurePosixPath("../escape.json"),
            where="probe",
            code=X_IDENTITY_MISMATCH,
        )
    assert excinfo.value.code == X_IDENTITY_MISMATCH
    assert "outside its declared root" in str(excinfo.value)


def test_step3_containment_guard_accepts_a_path_inside_its_root(
    roots: dict[str, Path],
) -> None:
    resolved = _resolve_under(
        roots["packet_root"],
        PurePosixPath("schema/schema.json"),
        where="probe",
        code=X_IDENTITY_MISMATCH,
    )
    assert resolved == roots["packet_root"] / "schema" / "schema.json"


def test_step3_opens_nothing(roots: dict[str, Path]) -> None:
    """Every path bound above names a file that does not exist, and binding passes."""

    _, bound = bind(valid_document(), roots)
    for path in (
        [bound.schema_path, bound.config_path]
        + list(bound.packet_artifacts.values())
        + list(bound.role_payloads.values())
        + list(bound.checkpoints.values())
    ):
        assert not path.exists()


# --------------------------------------------------------------------------- #
# The section-4.2 allowlist.
# --------------------------------------------------------------------------- #
def test_expected_open_set_is_exactly_the_declared_allowlist(roots: dict[str, Path]) -> None:
    record, bound = bind(valid_document(), roots)
    expected = {bound.record_path, bound.schema_path, bound.config_path}
    expected.update(bound.packet_artifacts.values())
    expected.update(
        bound.role_root / name
        for name in ("manifest.csv", "generation_audit.json", "independent_audit.json")
    )
    for case in record.cases:
        for suite in SUITE_KEYS:
            expected.add(bound.checkpoints[(case.case_id, suite)])
            for role in ROLE_NAMES:
                payload = bound.role_payloads[(case.case_id, suite, role)]
                expected.add(payload)
                expected.add(payload.parent / "index.csv")
    assert expected_open_set(record, bound) == expected


def test_expected_open_set_contains_no_role_root_directory_scan(
    roots: dict[str, Path],
) -> None:
    """Design property 1: there is no glob, no directory scan and no CLI flag."""

    record, bound = bind(valid_document(), roots)
    observed = expected_open_set(record, bound)
    assert all(path.name != "*" for path in observed)
    named_payloads = set(bound.role_payloads.values())
    assert named_payloads <= observed
    assert len(named_payloads) == len(record.cases) * len(SUITE_KEYS) * len(ROLE_NAMES)


def test_expected_open_set_grows_with_the_menu_and_nothing_else(
    roots: dict[str, Path],
) -> None:
    single = valid_document()
    single["cases"] = single["cases"][:1]
    record_one, bound_one = bind(single, roots)
    record_two, bound_two = bind(valid_document(), roots)
    added = expected_open_set(record_two, bound_two) - expected_open_set(record_one, bound_one)
    assert len(added) == len(SUITE_KEYS) * (len(ROLE_NAMES) + 1)


# --------------------------------------------------------------------------- #
# Invariant W11 -- the dependency boundary, measured rather than quoted.
# --------------------------------------------------------------------------- #
def test_w11_the_contract_imports_neither_torch_nor_mujoco() -> None:
    """V18's rule: this surface must open on a laptop that installed the packet.

    An import graph is a property of a checkout and not of a document, so this is
    measured in a *fresh* interpreter rather than read off `sys.modules` in a process
    that pytest has already filled.
    """

    code = (
        "import sys; import utils.connection_record; "
        "print(int('torch' in sys.modules), int('mujoco' in sys.modules))"
    )
    completed = subprocess.run(
        [sys.executable, "-c", code],
        cwd=str(PACKET_ROOT / "scripts"),
        capture_output=True,
        text=True,
        check=True,
    )
    assert completed.stdout.split() == ["0", "0"]


# --------------------------------------------------------------------------- #
# Round-1 finding 1 -- the record's own location is bound and is in the open set.
#
# The authorized bytes were previously accepted from any path, `bind_root_domains`
# never saw the record's path, and `expected_open_set` omitted a file step 1 had
# already opened. Section 3.1 gives a record exactly one tracked location, section
# 4.2 puts the record in the declared set, and finding CX makes the record tree a
# sibling of the bundle tree rather than a child of it. All three needed a mechanism.
# --------------------------------------------------------------------------- #
@pytest.mark.parametrize("authority", list(AUTHORITIES))
def test_step3_binds_the_record_to_its_one_tracked_location(
    roots: dict[str, Path], authority: str
) -> None:
    """The accept side, under both authorities: 3.1's location is not FINAL-only."""

    split = "dev" if authority == DEVELOPMENT_ONLY else "val"
    document = valid_document(authority=authority, split=split)
    record, bound = bind(document, roots)
    assert bound.record_path == tracked_record_path(
        roots["packet_root"], record.record_label
    )
    assert bound.record_path.is_relative_to(roots["packet_root"])
    assert bound.record_path.name == "connection_record.json"


def test_step3_refuses_the_authorized_bytes_presented_from_an_arbitrary_path(
    roots: dict[str, Path],
) -> None:
    """A path is not an identity -- and an identity is not a licence to be anywhere.

    Step 1 hashes whatever file it is handed, because that is what "a path is not an
    identity" means. Step 3 is where the record is required to have come from the
    location section 3.1 tracks it at. Without this, a copy of the approved bytes
    dropped anywhere on the machine drives the whole read order.
    """

    arbitrary = roots["packet_root"].parent / "arbitrary" / "copy.json"
    with pytest.raises(VerificationSceneError) as excinfo:
        bind(valid_document(), roots, connection_record_path=arbitrary)
    assert excinfo.value.code == X_IDENTITY_MISMATCH
    assert "not authorized from an arbitrary location" in str(excinfo.value)


@pytest.mark.parametrize("authority", list(AUTHORITIES))
def test_step3_refuses_a_record_nested_inside_the_output_tree(
    roots: dict[str, Path], authority: str
) -> None:
    """Finding CX made structural: the record may not live where step 21 creates.

    Under either authority, a record placed inside the output parent would sit in the
    directory the adapter must exclusively create, so the invocation could never reach
    exit 0. The location check refuses that arrangement before anything is opened,
    which is the difference between a documented sibling rule and an enforced one.
    """

    split = "dev" if authority == DEVELOPMENT_ONLY else "val"
    document = valid_document(authority=authority, split=split)
    nested = (
        roots["packet_root"]
        / Path(*OUTPUT_PARENTS[authority].parts)
        / document["record_label"]
        / "connection_record.json"
    )
    with pytest.raises(VerificationSceneError) as excinfo:
        bind(document, roots, connection_record_path=nested)
    assert excinfo.value.code == X_IDENTITY_MISMATCH
    assert "not authorized from an arbitrary location" in str(excinfo.value)


def test_step3_refuses_a_record_filed_under_a_different_label(
    roots: dict[str, Path],
) -> None:
    """The label binds the record's directory, not only the output root."""

    wrong = tracked_record_path(roots["packet_root"], "demo-record-2")
    with pytest.raises(VerificationSceneError) as excinfo:
        bind(valid_document(), roots, connection_record_path=wrong)
    assert excinfo.value.code == X_IDENTITY_MISMATCH


def test_step3_refuses_a_record_in_the_right_directory_under_the_wrong_name(
    roots: dict[str, Path],
) -> None:
    """`connection_record.json` is the whole path rule, not just the directory."""

    document = valid_document()
    misnamed = (
        tracked_record_path(roots["packet_root"], document["record_label"]).parent
        / "record.json"
    )
    with pytest.raises(VerificationSceneError) as excinfo:
        bind(document, roots, connection_record_path=misnamed)
    assert excinfo.value.code == X_IDENTITY_MISMATCH


def test_expected_open_set_contains_the_record_itself(roots: dict[str, Path]) -> None:
    """Section 4.2 names the record first, and W3 compares in both directions.

    An expected set that omitted the record would be unequal to any honest observed
    set, because step 1 opens the record. Leaving it out would have made W3's equality
    fail in 4b-ii for a correct adapter, or -- worse -- have been "fixed" there by
    filtering the observed side.
    """

    record, bound = bind(valid_document(), roots)
    observed = expected_open_set(record, bound)
    assert bound.record_path in observed
    assert tracked_record_path(roots["packet_root"], record.record_label) in observed


def test_expected_open_set_moves_with_the_injected_packet_root(
    roots: dict[str, Path],
) -> None:
    """W8 again: the record entry follows the injected root like everything else."""

    other_packet = roots["packet_root"].parent / "other-packet"
    other_packet.mkdir()
    record, bound = bind(valid_document(), roots, packet_root=other_packet)
    assert bound.record_path.is_relative_to(other_packet)
    assert bound.record_path in expected_open_set(record, bound)


# --------------------------------------------------------------------------- #
# Round-1 finding 2 -- an authenticated record is immutable all the way down.
#
# `@dataclass(frozen=True)` rebinds nothing but the attribute. Every mapping reached
# through a frozen attribute was an ordinary dict, so a later caller could replace a
# role reference or a record label after authentication and bind an allowlist that
# never came from the hashed bytes. Each layer below is probed separately, because a
# single spot check would have passed while the others stayed mutable.
# --------------------------------------------------------------------------- #
MAPPING_LAYER_NAMES = (
    "document",
    "document.schema",
    "document.cases[0]",
    "case.arms",
    "arm.roles",
    "arm.manifest_row",
    "render_geometry.links",
    "thresholds.sources",
)


def _mapping_layers(record: Any) -> dict[str, Any]:
    """Return every mapping a caller can reach from a parsed record."""

    case = record.cases[0]
    arm = case.arms["C1"]
    return {
        "document": record.document,
        "document.schema": record.document["schema"],
        "document.cases[0]": record.document["cases"][0],
        "case.arms": case.arms,
        "arm.roles": arm.roles,
        "arm.manifest_row": arm.manifest_row,
        "render_geometry.links": record.render_geometry.links,
        "thresholds.sources": record.thresholds.sources,
    }


@pytest.mark.parametrize("layer", MAPPING_LAYER_NAMES)
def test_every_mapping_reachable_from_a_record_refuses_assignment(layer: str) -> None:
    record = parse_connection_record(record_bytes(valid_document()))
    mapping = _mapping_layers(record)[layer]
    with pytest.raises(TypeError):
        mapping["injected"] = "value"
    assert "injected" not in mapping


@pytest.mark.parametrize("layer", MAPPING_LAYER_NAMES)
def test_every_mapping_reachable_from_a_record_refuses_deletion(layer: str) -> None:
    record = parse_connection_record(record_bytes(valid_document()))
    mapping = _mapping_layers(record)[layer]
    key = next(iter(mapping))
    with pytest.raises(TypeError):
        del mapping[key]
    assert key in mapping


def test_the_exact_probes_the_reviewer_ran_now_refuse() -> None:
    """Two named mutations from the Round-1 ledger, driven as they were driven.

    The reviewer replaced the C1 `plant` role with the `labels` reference and
    overwrote `document["record_label"]`; both succeeded on the Round-1 candidate.
    Re-driving exactly those two is what keeps this repair from being asserted only
    at the layers I happened to think of.
    """

    record = parse_connection_record(record_bytes(valid_document()))
    arm = record.cases[0].arms["C1"]
    original_plant = arm.roles["plant"]
    with pytest.raises(TypeError):
        arm.roles["plant"] = arm.roles["labels"]
    with pytest.raises(TypeError):
        record.document["record_label"] = "some-other-label"
    assert arm.roles["plant"] is original_plant
    assert record.document["record_label"] == "demo-record-1"


def test_record_arrays_are_tuples_rather_than_editable_lists() -> None:
    """A read-only mapping over a mutable list is the appearance of the property."""

    record = parse_connection_record(record_bytes(valid_document()))
    assert isinstance(record.document["cases"], tuple)
    assert isinstance(
        record.document["render_geometry"]["planar_convention"]["base_xy_m"], tuple
    )
    assert isinstance(
        record.document["render_geometry"]["links"]["L1"]["segment_lengths_m"], tuple
    )
    with pytest.raises(AttributeError):
        record.document["cases"].append("extra")


def test_the_frozen_document_is_not_a_view_of_the_callers_dict() -> None:
    """A proxy over a dict the caller still holds is a read-only handle on a mutable
    object. The parse takes a private copy, so mutating the source afterwards cannot
    move what was authenticated."""

    document = valid_document()
    record = parse_connection_record(record_bytes(document))
    document["record_label"] = "mutated-after-the-fact"
    document["cases"][0]["case_id"] = "mutated-case"
    assert record.document["record_label"] == "demo-record-1"
    assert record.document["cases"][0]["case_id"] == "case-a"
    assert record.cases[0].case_id == "case-a"


def test_a_frozen_mapping_copies_rather_than_wrapping_the_callers_dict() -> None:
    """A proxy over a dict its caller still holds is a handle on a mutable object.

    Every call site in the module builds the dict locally, so no input can reach this
    branch -- which is exactly why it is driven directly. It was a mutation survivor
    until this test existed: replacing `MappingProxyType(dict(mapping))` with
    `MappingProxyType(mapping)` changed nothing any other test could observe.
    """

    source = {"a": 1}
    view = _frozen_mapping(source)
    source["b"] = 2
    assert dict(view) == {"a": 1}
    with pytest.raises(TypeError):
        view["c"] = 3


def test_resolve_under_names_a_refusal_when_the_root_itself_cannot_resolve(
    roots: dict[str, Path],
) -> None:
    """`_resolve_under` resolves through the guarded helper, not through `.resolve()`.

    The step-2 grammar makes the relative side unable to reach a resolution failure,
    so the only way to drive this is a root that cannot resolve. Without the guarded
    call the failure escapes as a raw `ValueError` from inside a contract layer, and
    the design's exit code never happens -- a mutation survivor until this test.
    """

    with pytest.raises(VerificationSceneError) as excinfo:
        _resolve_under(
            Path(str(roots["packet_root"]) + "\x00suffix"),
            PurePosixPath("schema/schema.json"),
            where="probe",
            code=X_IDENTITY_MISMATCH,
        )
    assert excinfo.value.code == X_IDENTITY_MISMATCH
    assert "could not be resolved to a path" in str(excinfo.value)


def test_step3_refuses_a_record_tree_a_link_rebinds_outside_the_packet(
    roots: dict[str, Path],
) -> None:
    """The record's tracked location is proved contained, not merely joined.

    Only the record subtree is linked away, so the authority's output parent still
    resolves inside the packet and the earlier destination check passes. What is left
    is a record path that spells out as packet-relative and physically is not, which
    is the state the containment proof exists for -- and, with a plain join in its
    place, `--connection-record` pointed at the linked-away file would have been
    accepted as the tracked location.
    """

    packet_root = roots["packet_root"]
    outside = packet_root.parent / "outside-the-packet-records"
    outside.mkdir()
    records_parent = packet_root / Path(*RECORD_PARENT.parts)
    records_parent.parent.mkdir(parents=True, exist_ok=True)
    _link_directory(records_parent, outside)

    document = valid_document()
    linked_record = records_parent / document["record_label"] / "connection_record.json"
    # The trap: the path spells out exactly as the tracked location, and resolves out.
    assert linked_record.resolve().is_relative_to(outside.resolve())
    with pytest.raises(VerificationSceneError) as excinfo:
        bind(document, roots, connection_record_path=linked_record)
    assert excinfo.value.code == X_IDENTITY_MISMATCH
    assert "outside its declared root" in str(excinfo.value)


def test_bound_path_mappings_refuse_assignment(roots: dict[str, Path]) -> None:
    """The allowlist inputs are values too: `BoundPaths` carries no editable dict."""

    _, bound = bind(valid_document(), roots)
    for mapping in (bound.packet_artifacts, bound.role_payloads, bound.checkpoints):
        with pytest.raises(TypeError):
            mapping["injected"] = Path("anywhere")
        assert "injected" not in mapping


# --------------------------------------------------------------------------- #
# Round-1 finding 3 -- the finite-number gate is total over JSON integers.
#
# `json.loads` parses an unbounded integer literal exactly, the non-finite walk only
# inspects floats, and `float(10 ** 400)` then raised a raw `OverflowError`. The
# existing overflowing-literal test exercises a different path: `1e9999` becomes
# `inf` inside the parser and never reaches the conversion at all.
# --------------------------------------------------------------------------- #
HUGE_INTEGER_LITERAL = 10**400


@pytest.mark.parametrize(
    "dotted",
    [
        "analysis_window_s",
        "thresholds.abstain_threshold",
        "thresholds.unknown_threshold",
        "render_geometry.distal_tolerance_m",
        "render_geometry.planar_convention.base_xy_m.0",
        "render_geometry.links.L1.segment_lengths_m.0",
    ],
)
def test_step2_refuses_an_overflowing_integer_at_every_float_field(dotted: str) -> None:
    error = refuse(mutate(valid_document(), dotted, HUGE_INTEGER_LITERAL))
    assert error.code == X_CONNECTION_UNAUTHORIZED
    # The sentence is asserted because the code alone is satisfied by any refusal,
    # and the state this test exists for previously produced no refusal at all.
    assert "too large to represent as a finite number" in str(error)


def test_step2_refuses_a_negative_overflowing_integer() -> None:
    error = refuse(
        mutate(valid_document(), "thresholds.abstain_threshold", -HUGE_INTEGER_LITERAL)
    )
    assert "too large to represent as a finite number" in str(error)


def test_step2_still_accepts_an_ordinary_large_integer_literal() -> None:
    """The gate is about representability, not about magnitude taste."""

    record = parse_connection_record(
        record_bytes(mutate(valid_document(), "analysis_window_s", 10**300))
    )
    assert math.isfinite(record.analysis_window_s)


def test_an_overflowing_integer_survives_the_canonical_round_trip() -> None:
    """The refusal is the number gate's, not the encoder's -- stated by measurement.

    If canonical JSON could not round-trip `10 ** 400`, the test above would be
    passing on the encoding branch and the conversion branch would still be raw.
    """

    document = mutate(valid_document(), "analysis_window_s", HUGE_INTEGER_LITERAL)
    raw = record_bytes(document)
    assert json.loads(raw.decode("utf-8"))["analysis_window_s"] == HUGE_INTEGER_LITERAL


# --------------------------------------------------------------------------- #
# Round-1 finding 4 -- one portable path grammar, and total containment.
#
# Traversal was refused; portability was not. An embedded NUL reached
# `Path.resolve()` as a raw `ValueError`; `schema.json:stream` names an NTFS
# alternate data stream on Windows and an ordinary file elsewhere; `CON` is a device
# rather than a file; a trailing dot or space is silently stripped by Windows, so two
# distinct records name one file. None of these can be caught by containment --
# resolution raises before the comparison, and a device alias is contained by every
# root.
# --------------------------------------------------------------------------- #
@pytest.mark.parametrize(
    ("token", "phrase"),
    [
        ("schema/sch\x00ema.json", "outside the portable component class"),
        ("schema.json:stream", "outside the portable component class"),
        ("schema/schema.json:$DATA", "outside the portable component class"),
        ("sch ema.json", "outside the portable component class"),
        ("schema/schema .json", "outside the portable component class"),
        ("schema/sch*ema.json", "outside the portable component class"),
        ("schema/sch\nema.json", "outside the portable component class"),
        ("schema/schema.json.", "ends in a dot"),
        ("schema./schema.json", "ends in a dot"),
        ("CON", "reserved device name"),
        ("con.json", "reserved device name"),
        ("schema/NUL.txt", "reserved device name"),
        ("COM1/schema.json", "reserved device name"),
        ("lpt9.json", "reserved device name"),
        ("aux", "reserved device name"),
    ],
)
def test_step2_refuses_every_non_portable_path_component(token: str, phrase: str) -> None:
    error = refuse(mutate(valid_document(), "schema.relative_path", token))
    assert error.code == X_CONNECTION_UNAUTHORIZED
    assert phrase in str(error)


@pytest.mark.parametrize(
    "dotted",
    [
        "schema.relative_path",
        "config.relative_path",
        "established_result.artifact_relative_path",
        "thresholds.sources.abstain_threshold.artifact_relative_path",
        "model_selection.source.artifact_relative_path",
        "render_geometry.source.producer_relative_path",
        "render_geometry.tolerance_source.artifact_relative_path",
        "cases.0.arms.S.checkpoint.relative_path",
        "cases.0.arms.S.roles.labels.payload_relative_path",
    ],
)
def test_step2_applies_the_portable_grammar_at_every_declared_position(dotted: str) -> None:
    assert refuse(mutate(valid_document(), dotted, "artifact.json:stream")).code == (
        X_CONNECTION_UNAUTHORIZED
    )


@pytest.mark.parametrize(
    "token",
    [
        "schema/schema.json",
        "config/draft-config-v0.1.json",
        "scripts/utils/cable_mechanics.py",
        "results/verification_connection/records/demo-record-1/connection_record.json",
        "labels/dev/pair_0001_C1.npz",
        "results/capacity_sweep/stage1-run-2/arm_C1_w32_s0.pt",
        "CONFIGURATION/values.json",
        "conference.json",
        "com10.json",
    ],
)
def test_step2_accepts_the_portable_paths_the_project_actually_uses(token: str) -> None:
    """The accept side, including three near-misses on the device rule.

    `CONFIGURATION`, `conference.json` and `com10.json` all start like a reserved
    name and none of them is one. A grammar that refused these would refuse ordinary
    project files, which is how an over-tight rule gets quietly widened later.
    """

    record = parse_connection_record(
        record_bytes(mutate(valid_document(), "schema.relative_path", token))
    )
    assert record.schema.relative_path == PurePosixPath(token)


def test_resolve_safely_names_a_refusal_where_resolution_would_raise(
    roots: dict[str, Path],
) -> None:
    """A raw exception out of a contract layer is a silent failure by another name.

    The step-2 grammar makes this branch unreachable from a well-formed record, which
    is exactly why it is driven directly: a guard no input can reach is a guard
    nothing checks, and this one is the reason a resolution failure produces the
    design's exit code instead of a traceback.
    """

    with pytest.raises(VerificationSceneError) as excinfo:
        _resolve_safely(
            Path(str(roots["packet_root"]) + "\x00suffix"),
            where="probe",
            code=X_IDENTITY_MISMATCH,
        )
    assert excinfo.value.code == X_IDENTITY_MISMATCH
    assert "could not be resolved to a path" in str(excinfo.value)


def test_resolve_safely_returns_the_resolved_path_for_an_ordinary_argument(
    roots: dict[str, Path],
) -> None:
    resolved = _resolve_safely(
        roots["packet_root"] / "schema" / "schema.json",
        where="probe",
        code=X_IDENTITY_MISMATCH,
    )
    assert resolved == (roots["packet_root"] / "schema" / "schema.json").resolve()


def test_the_output_parent_containment_guard_refuses_with_the_provenance_code(
    roots: dict[str, Path],
) -> None:
    """The output parent is proved contained, not merely joined.

    A junction or symlink at any component of `results/` would let a destination that
    compares equal to the expected parent sit physically outside the packet, and the
    equality check would still pass. This drives the guard the output-parent
    derivation now goes through, with the code that derivation assigns.
    """

    with pytest.raises(VerificationSceneError) as excinfo:
        _resolve_under(
            roots["packet_root"],
            PurePosixPath("../escaped-parent"),
            where="probe",
            code=X_PROVENANCE_UNRESOLVED,
        )
    assert excinfo.value.code == X_PROVENANCE_UNRESOLVED
    assert "outside its declared root" in str(excinfo.value)


def _link_directory(link: Path, target: Path) -> None:
    """Make `link` a directory link to `target`, or skip if the platform refuses.

    A plain symlink needs Developer Mode or elevation on Windows and this machine has
    neither, so the test would have been permanently skipped on the only hardware the
    project has -- a test that never runs holds nothing. A **junction** needs no
    privilege at all and `Path.resolve()` follows it exactly as it follows a symlink,
    which is the whole property under test. Symlink first, junction second, skip only
    if both are unavailable.
    """

    try:
        link.symlink_to(target, target_is_directory=True)
        return
    except (OSError, NotImplementedError):
        pass
    if os.name != "nt":  # pragma: no cover - platform gate
        pytest.skip("this platform will not create a directory link")
    completed = subprocess.run(  # noqa: S603 - fixed argv, no shell
        ["cmd", "/c", "mklink", "/J", str(link), str(target)],
        capture_output=True,
        text=True,
    )
    if completed.returncode != 0 or not link.exists():  # pragma: no cover
        pytest.skip(f"this platform will not create a directory junction: {completed.stderr}")


def test_step3_refuses_an_output_parent_a_link_rebinds_outside_the_packet(
    roots: dict[str, Path],
) -> None:
    """The same property end to end, with the trap actually built.

    `results/` becomes a link to a directory outside the packet, so
    `<packet>/results/verification_connection/bundles` resolves outside the packet
    while every string in the equality comparison still looks right. The unit test
    above holds the guard; this one holds the wiring.
    """

    packet_root = roots["packet_root"]
    outside = packet_root.parent / "outside-the-packet"
    escaped_parent = outside / Path(*FINAL_OUTPUT_PARENT.parts)
    escaped_parent.mkdir(parents=True)
    _link_directory(packet_root / "results", outside / "results")

    # The trap is built so the *equality* still holds: `--output-dir` is exactly what
    # `<packet>/results/verification_connection/bundles` resolves to. Only the
    # containment proof separates this from an accepted destination, so a regression
    # that dropped `_resolve_under` here would make this test green again.
    assert (packet_root / Path(*FINAL_OUTPUT_PARENT.parts)).resolve() == escaped_parent.resolve()

    with pytest.raises(VerificationSceneError) as excinfo:
        bind(valid_document(), roots, output_dir=escaped_parent)
    assert excinfo.value.code == X_PROVENANCE_UNRESOLVED
    assert "outside its declared root" in str(excinfo.value)


# --------------------------------------------------------------------------- #
# Round-1 finding 5 -- `case_id` is written to disk as a filename.
#
# `render_bundle` composes `<destination>/<case_id>.png` and `.json`. While every
# bundle was built in-process by this packet, `case_id` was a key nobody could aim.
# Once a connection record supplies it, `../escape` writes beside the exclusive-
# created output root -- section 4.7 and W10 -- and `Path.name` in the returned
# manifest reports the innocent leaf. Two layers: the record boundary refuses the
# value, and the writer proves containment for whatever it is handed.
# --------------------------------------------------------------------------- #
@pytest.mark.parametrize(
    ("case_id", "phrase"),
    [
        ("../escape", "must be one path component carrying no separator"),
        ("../../escape", "must be one path component carrying no separator"),
        ("sub/escape", "must be one path component carrying no separator"),
        ("sub\\escape", "must be one path component carrying no separator"),
        ("/rooted", "must be one path component carrying no separator"),
        ("..", "must not be '..'"),
        (".", "must not be '.'"),
        ("C:escape", "outside the portable component class"),
        ("case:stream", "outside the portable component class"),
        ("case id", "outside the portable component class"),
        ("case\x00id", "outside the portable component class"),
        ("CON", "reserved device name"),
        ("case.", "ends in a dot"),
        ("", "must be a non-empty string"),
    ],
)
def test_step2_refuses_a_case_id_that_is_not_a_portable_leaf_token(
    case_id: str, phrase: str
) -> None:
    """Each case asserts the sentence its own branch raises, not only the code.

    Measured by the mutation sweep, not reasoned about: with a code-only assertion,
    deleting the separator branch and deleting the `.`/`..` branch each left this
    suite green, because the portable-component grammar one line later refuses the
    same inputs with a different sentence. That is the Session-136 lesson arriving a
    third time -- a branch subsumed by a later check is held by nothing unless the
    assertion names what only that branch says.
    """

    error = refuse(mutate(valid_document(), "cases.0.case_id", case_id))
    assert error.code == X_CONNECTION_UNAUTHORIZED
    assert phrase in str(error)


@pytest.mark.parametrize("case_id", ["case-a", "case_1", "soften.link.2", "CASE-A", "c"])
def test_step2_accepts_a_portable_leaf_case_id(case_id: str) -> None:
    document = mutate(valid_document(), "cases.0.case_id", case_id)
    record = parse_connection_record(record_bytes(document))
    assert record.cases[0].case_id == case_id


def test_the_renderer_refuses_to_write_a_path_outside_its_output_root(
    tmp_path: Path,
) -> None:
    """The second, independent layer, driven at the write boundary itself."""

    import matplotlib

    matplotlib.use("Agg")
    from render_verification_scene import _contained_output_paths

    destination = tmp_path / "bundle"
    destination.mkdir()
    for name in ("../escaped-case.png", "sub/escaped-case.json", ".."):
        with pytest.raises(VerificationSceneError) as excinfo:
            _contained_output_paths(destination, ["bundle.json", name])
        assert excinfo.value.code == X_IDENTITY_MISMATCH
        assert "not a direct child of its output root" in str(excinfo.value)
    accepted = _contained_output_paths(destination, ["bundle.json", "case-a.png"])
    assert accepted == {
        "bundle.json": (destination / "bundle.json").resolve(),
        "case-a.png": (destination / "case-a.png").resolve(),
    }


def test_the_renderer_writes_nothing_outside_its_root_for_an_escaping_case_id(
    tmp_path: Path,
) -> None:
    """The reviewer's probe, re-driven end to end through the approved renderer.

    On the Round-1 candidate this wrote `escaped-case.png` and `escaped-case.json`
    beside the requested directory and nothing inside it. The record boundary now
    refuses the value, and this asserts the writer refuses it too -- so the guarantee
    does not depend on every future producer of a bundle having gone through the
    record.
    """

    import dataclasses

    import matplotlib

    matplotlib.use("Agg")
    from render_verification_scene import render_bundle
    from utils.verification_scene import build_fixture_bundle

    bundle = build_fixture_bundle(seed=7)
    first_id, first_scene = next(iter(bundle.scenes.items()))
    escaped_id = "../escaped-case"
    escaped_scene = dataclasses.replace(
        first_scene,
        body_change=dataclasses.replace(first_scene.body_change, case_id=escaped_id),
    )
    scenes = {escaped_id: escaped_scene}
    scenes.update({key: value for key, value in bundle.scenes.items() if key != first_id})
    escaping_bundle = dataclasses.replace(bundle, scenes=scenes)

    destination = tmp_path / "bundle"
    destination.mkdir()
    with pytest.raises(VerificationSceneError) as excinfo:
        render_bundle(escaping_bundle, destination)
    assert excinfo.value.code == X_IDENTITY_MISMATCH
    # Nothing escaped, and -- because the write set is proved before the first write
    # -- nothing was written at all, not even the two files whose names are constants.
    assert sorted(path.name for path in tmp_path.iterdir()) == ["bundle"]
    assert list(destination.iterdir()) == []
