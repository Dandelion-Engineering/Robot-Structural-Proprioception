"""Tests for the Slot-8 connection adapter's authentication chain (rows 4-12).

**What this file holds.** One complete, isolated packet tree and one complete role
tree, and every read-order refusal from row 4 through row 12 driven against them.
Invariant W2 is the standard the file is written to: not a test that asserts a message
exists, but a test that *builds the input the row refuses* and drives the exit.

**Why the harness is built the way it is.** Three properties of the harness are
load-bearing rather than convenient, and each one comes from a finding the design
already recorded:

  1. *The packet root is a temporary tree, and the entry point takes it as a
     parameter* (invariant W8). Every packet-relative resolution in the read order --
     the step-3 domain binding, the step-4 schema and config resolution and the step-5
     source artifacts -- runs under that one injected root, so these tests exercise the
     production branch rather than a parallel one. Nothing here writes into the live
     packet, and `test_the_live_packet_holds_no_config_json` asserts the boundary from
     both ends.
  2. *The schema and the draft config are byte-exact copies, never re-serialisations*
     (acceptance test B8). `utils.config_contract.validate_config_document` requires
     the config's declared `schema_sha256` to equal the schema's **raw** bytes, so a
     re-serialised schema would refuse for the wrong reason and the authority tests
     would prove nothing about authority.
  3. *The role tree is the existing contract fixture* (design 2.4). It drives storage,
     index, authentication and refusal plumbing and nothing else. It is explicitly
     **not** a geometry oracle -- its `deform_coords` and `true_task_output` come from
     independent synthetic maps -- and nothing in this file uses it as one. Geometry is
     read-order row 18 and belongs to the second half of sub-step 4b-ii.

**What this file does not do.** It authors no production connection record, runs no
adapter invocation against real data, opens no `dev`, `pilot`, `val` or `test` result,
selects no capacity or threshold, freezes no config and makes no C1-versus-S statement.
Every path it binds is inside a `tmp_path` tree.
"""

from __future__ import annotations

import copy
import json
import shutil
import sys
from dataclasses import asdict
from pathlib import Path
from typing import Any, Callable, Mapping

import pytest

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "scripts"))

from build_data_contract_fixture import build_fixture  # noqa: E402
from utils.config_contract import load_config  # noqa: E402
from utils.connection_adapter import (  # noqa: E402
    AUDIT_NAMES,
    MANIFEST_AUDIT_KEY,
    MANIFEST_CENSUS_FIELDS,
    MANIFEST_NAME,
    ROLE_INDEX_NAME,
    SUITE_QUALIFIED_ROLES,
    AuthenticatedConnection,
    authenticate_config,
    authenticate_connection,
    authenticate_dataset,
    authenticate_roles,
    authenticate_sources,
    external_digest,
    manifest_census,
    require_authority_config_policy,
    role_root_for,
    strict_json_document,
    tracked_text_digest,
    value_at_field_path,
)
from utils.connection_record import (  # noqa: E402
    MANIFEST_ROW_FIELDS,
    ROLE_NAMES,
    bind_root_domains,
    load_connection_record,
    record_relative_path,
)
from utils.protocol_p import canonical_json  # noqa: E402
from utils.storage_contract import read_identity_manifest  # noqa: E402
from utils.verification_scene import (  # noqa: E402
    DEVELOPMENT_ONLY,
    FINAL,
    VerificationSceneError,
    X_CONNECTION_UNAUTHORIZED,
    X_IDENTITY_MISMATCH,
    X_PROVENANCE_UNRESOLVED,
    X_ROLE_ABSENT,
    X_ROLE_UNAUTHORIZED,
    X_SPLIT_FORBIDDEN,
)

PACKET_ROOT = Path(__file__).resolve().parents[1]
LIVE_SCHEMA = PACKET_ROOT / "schema" / "schema.json"
LIVE_DRAFT_CONFIG = PACKET_ROOT / "config" / "draft-config-v0.1.json"
LIVE_GEOMETRY_PRODUCER = PACKET_ROOT / "scripts" / "utils" / "cable_mechanics.py"

#: Every path below is packet-root-relative and lives only inside the temporary tree.
SCHEMA_RELATIVE = "schema/schema.json"
CONFIG_RELATIVE = "config/draft-config-v0.1.json"
PRODUCER_RELATIVE = "scripts/utils/cable_mechanics.py"
SOURCE_PARENT = "results/adapter_fixture_sources"
RESULT_RELATIVE = f"{SOURCE_PARENT}/established_result.json"
SELECTION_RELATIVE = f"{SOURCE_PARENT}/model_selection.json"
CALIBRATION_RELATIVE = f"{SOURCE_PARENT}/calibration.json"
GEOMETRY_RELATIVE = f"{SOURCE_PARENT}/geometry_validation.json"

RECORD_LABEL = "adapter-fixture"
DATASET_LABEL = "adapter-fixture-root"
CASE_ID = "fixture-dev"
PAIR_ID = "fixture_dev"
SPLIT = "dev"
ABSTAIN_THRESHOLD = 0.55
UNKNOWN_THRESHOLD = 0.75
SELECTED_RUNG = 2
SELECTED_WIDTH = 32
DISTAL_TOLERANCE_M = 0.002
MAXIMUM_DEVIATION_M = 0.0011

#: The contract fixture's minimum trajectory length. It is stated as a literal rather
#: than derived from the builder's own guard, because a test whose input is a function
#: of the constant it exercises holds the relationship and not the value.
FIXTURE_N_STEPS = 32


# --------------------------------------------------------------------------- #
# The harness.
# --------------------------------------------------------------------------- #
def _write_json(path: Path, document: Mapping[str, Any]) -> None:
    """Write one source artifact as ordinary indented JSON, refusing non-finite."""

    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(
        json.dumps(document, indent=2, sort_keys=True, allow_nan=False) + "\n",
        encoding="utf-8",
    )


def _write_record(path: Path, document: Mapping[str, Any]) -> str:
    """Write one connection record as canonical JSON and return its raw digest."""

    import hashlib

    path.parent.mkdir(parents=True, exist_ok=True)
    raw = canonical_json(document).encode("utf-8")
    path.write_bytes(raw)
    return hashlib.sha256(raw).hexdigest()


def _audit_document(
    *, status: str, assignment_hash: str, config_hash: str, census: Mapping[str, Any]
) -> dict[str, Any]:
    """Return one dataset audit in the shape the delivered audits actually carry.

    The delivered `generation_audit.json` and `independent_audit.json` each carry a
    top-level `status`, `assignment_hash` and `config_hash`, plus a `manifest_audit`
    block holding the census. This helper reproduces that shape so the adapter's
    step-6 checks are exercised against the structure they will meet, without any
    test depending on the delivered tree existing (finding DB).
    """

    block = dict(census)
    block["status"] = "manifest_matches_fixture_reservations"
    return {
        "assignment_hash": assignment_hash,
        "config_hash": config_hash,
        "manifest_audit": block,
        "status": status,
    }


class Harness:
    """One isolated packet root, role root and checkpoint root, plus a record."""

    def __init__(self, root: Path) -> None:
        self.root = root
        self.packet_root = root / "packet"
        self.role_root = root / DATASET_LABEL
        self.checkpoint_root = root / "checkpoints"
        self.output_dir = (
            self.packet_root / "results" / "verification_connection_development"
        )

    # -- construction ------------------------------------------------------- #
    def build(self) -> None:
        """Materialise every tree the authentication chain reads."""

        self._copy_packet_files()
        summary_config = load_config(
            self.packet_root / CONFIG_RELATIVE, self.packet_root / SCHEMA_RELATIVE
        )
        self.config_hash = summary_config.config_hash
        build_fixture(
            self.packet_root / SCHEMA_RELATIVE,
            self.packet_root / CONFIG_RELATIVE,
            self.role_root,
            FIXTURE_N_STEPS,
        )
        self.manifest_rows = {
            row.run_id: row for row in read_identity_manifest(self.role_root / MANIFEST_NAME)
        }
        self.census = manifest_census(list(self.manifest_rows.values()))
        self._write_audits()
        self._write_checkpoints()
        self._write_sources()
        self.document = self._record_document()
        self.record_path = self.packet_root / record_relative_path(RECORD_LABEL)
        self.record_sha256 = _write_record(self.record_path, self.document)

    def _copy_packet_files(self) -> None:
        """Copy the schema, draft config and geometry producer byte for byte.

        Byte-exactness is the contract fact acceptance test B8 names: the config's
        declared `schema_sha256` is compared against the schema's raw bytes, so a
        re-serialised schema refuses for the wrong reason.
        """

        for relative, live in (
            (SCHEMA_RELATIVE, LIVE_SCHEMA),
            (CONFIG_RELATIVE, LIVE_DRAFT_CONFIG),
            (PRODUCER_RELATIVE, LIVE_GEOMETRY_PRODUCER),
        ):
            destination = self.packet_root / relative
            destination.parent.mkdir(parents=True, exist_ok=True)
            destination.write_bytes(live.read_bytes())

    def _write_audits(self) -> None:
        """Write both dataset audits so their echoes and census agree with the tree."""

        self.assignment_hash = f"dev-{'a' * 64}"
        self.audit_status = {
            "generation_audit": "complete_synthetic_contract_fixture",
            "independent_audit": "independent_synthetic_contract_fixture",
        }
        for name in AUDIT_NAMES:
            _write_json(
                self.role_root / f"{name}.json",
                _audit_document(
                    status=self.audit_status[name],
                    assignment_hash=self.assignment_hash,
                    config_hash=self.config_hash,
                    census=self.census,
                ),
            )

    def _write_checkpoints(self) -> None:
        """Write one inert byte blob per arm. Nothing in this lane loads a checkpoint."""

        for suite in ("C1", "S"):
            path = self.checkpoint_root / PAIR_ID / f"{suite}.pt"
            path.parent.mkdir(parents=True, exist_ok=True)
            path.write_bytes(f"inert-fixture-checkpoint-{suite}".encode("utf-8"))

    def _write_sources(self) -> None:
        """Write the four synthetic source artifacts the record names."""

        _write_json(
            self.packet_root / RESULT_RELATIVE,
            {
                "read": {
                    "cases": [CASE_ID],
                    "config_hash": self.config_hash,
                    "split": SPLIT,
                },
                "status": "synthetic_fixture_established_result",
            },
        )
        _write_json(
            self.packet_root / SELECTION_RELATIVE,
            {"selected": {"rung": SELECTED_RUNG, "width": SELECTED_WIDTH}},
        )
        _write_json(
            self.packet_root / CALIBRATION_RELATIVE,
            {
                "values": {
                    "abstain": ABSTAIN_THRESHOLD,
                    "unknown": UNKNOWN_THRESHOLD,
                }
            },
        )
        _write_json(
            self.packet_root / GEOMETRY_RELATIVE,
            {
                "agreement": {
                    "maximum_deviation_m": MAXIMUM_DEVIATION_M,
                    "tolerance_m": DISTAL_TOLERANCE_M,
                }
            },
        )

    # -- the record --------------------------------------------------------- #
    def _payload_relative(self, role: str, suite: str, run_id: str) -> str:
        """Return one payload's role-root-relative path at the schema-E layout."""

        if role in SUITE_QUALIFIED_ROLES:
            return f"{role}/{suite}/{run_id}.npz"
        return f"{role}/{run_id}.npz"

    def _arm(self, suite: str) -> dict[str, Any]:
        run_id = f"{PAIR_ID}_{suite}"
        row = asdict(self.manifest_rows[run_id])
        roles: dict[str, Any] = {}
        for role in ROLE_NAMES:
            relative = self._payload_relative(role, suite, run_id)
            payload = self.role_root / relative
            index = role_root_for(self.role_root, role, suite) / ROLE_INDEX_NAME
            roles[role] = {
                "index_sha256": external_digest(index),
                "payload_relative_path": relative,
                "payload_sha256": external_digest(payload),
            }
        checkpoint = self.checkpoint_root / PAIR_ID / f"{suite}.pt"
        return {
            "checkpoint": {
                "relative_path": f"{PAIR_ID}/{suite}.pt",
                "sha256": external_digest(checkpoint),
            },
            "manifest_row": {name: row[name] for name in MANIFEST_ROW_FIELDS},
            "roles": roles,
            "run_id": run_id,
        }

    def _record_document(self) -> dict[str, Any]:
        """Return the complete section-3.2 record for this harness."""

        return {
            "analysis_window_s": 5.0,
            "authority": DEVELOPMENT_ONLY,
            "cases": [
                {
                    "arms": {"C1": self._arm("C1"), "S": self._arm("S")},
                    "case_id": CASE_ID,
                    "display_label": "Fixture development pair",
                    "pair_id": PAIR_ID,
                }
            ],
            "config": {
                "config_hash": self.config_hash,
                "relative_path": CONFIG_RELATIVE,
                "sha256": tracked_text_digest(self.packet_root / CONFIG_RELATIVE),
            },
            "data_root": {
                "dataset_label": DATASET_LABEL,
                "generation_audit": {
                    "assignment_hash": self.assignment_hash,
                    "config_hash": self.config_hash,
                    "sha256": external_digest(
                        self.role_root / "generation_audit.json"
                    ),
                    "status": self.audit_status["generation_audit"],
                },
                "independent_audit": {
                    "assignment_hash": self.assignment_hash,
                    "config_hash": self.config_hash,
                    "sha256": external_digest(
                        self.role_root / "independent_audit.json"
                    ),
                    "status": self.audit_status["independent_audit"],
                },
                "manifest_sha256": external_digest(self.role_root / MANIFEST_NAME),
            },
            "established_result": {
                "artifact_relative_path": RESULT_RELATIVE,
                "cases_field_path": "read.cases",
                "config_hash_field_path": "read.config_hash",
                "sha256": tracked_text_digest(self.packet_root / RESULT_RELATIVE),
                "split_field_path": "read.split",
            },
            "model_selection": {
                "rung": SELECTED_RUNG,
                "source": {
                    "artifact_relative_path": SELECTION_RELATIVE,
                    "rung_field_path": "selected.rung",
                    "sha256": tracked_text_digest(self.packet_root / SELECTION_RELATIVE),
                    "width_field_path": "selected.width",
                },
                "width": SELECTED_WIDTH,
            },
            "record_label": RECORD_LABEL,
            "record_version": "slot8-connection-record-v0.1",
            "render_geometry": {
                "derivation_version": "v0.1",
                "distal_tolerance_m": DISTAL_TOLERANCE_M,
                "links": {
                    "L1": {
                        "deform_triplets": [[0, 1, 2], [3, 4, 5]],
                        "segment_lengths_m": [0.2, 0.2, 0.2],
                    },
                    "L2": {
                        "deform_triplets": [[6, 7, 8], [9, 10, 11]],
                        "segment_lengths_m": [0.2, 0.2, 0.2],
                    },
                },
                "planar_convention": {
                    "base_xy_m": [0.0, 0.0],
                    "projection": "xz",
                    "q_true_convention": "absolute",
                    "rotation_vector_component": 1,
                },
                "source": {
                    "model_id": "cable-two-link",
                    "producer_relative_path": PRODUCER_RELATIVE,
                    "producer_sha256": tracked_text_digest(
                        self.packet_root / PRODUCER_RELATIVE
                    ),
                },
                "tolerance_source": {
                    "artifact_relative_path": GEOMETRY_RELATIVE,
                    "maximum_deviation_field_path": "agreement.maximum_deviation_m",
                    "sha256": tracked_text_digest(self.packet_root / GEOMETRY_RELATIVE),
                    "tolerance_field_path": "agreement.tolerance_m",
                },
            },
            "schema": {
                "relative_path": SCHEMA_RELATIVE,
                "sha256": tracked_text_digest(self.packet_root / SCHEMA_RELATIVE),
            },
            "split": SPLIT,
            "thresholds": {
                "abstain_threshold": ABSTAIN_THRESHOLD,
                "sources": {
                    "abstain_threshold": {
                        "artifact_relative_path": CALIBRATION_RELATIVE,
                        "field_path": "values.abstain",
                        "sha256": tracked_text_digest(
                            self.packet_root / CALIBRATION_RELATIVE
                        ),
                    },
                    "unknown_threshold": {
                        "artifact_relative_path": CALIBRATION_RELATIVE,
                        "field_path": "values.unknown",
                        "sha256": tracked_text_digest(
                            self.packet_root / CALIBRATION_RELATIVE
                        ),
                    },
                },
                "unknown_threshold": UNKNOWN_THRESHOLD,
            },
        }

    # -- driving ------------------------------------------------------------ #
    def arguments(self) -> dict[str, Any]:
        """Return the six CLI-shaped arguments plus the injected packet root."""

        return {
            "packet_root": self.packet_root,
            "connection_record_path": self.record_path,
            "connection_record_sha256": self.record_sha256,
            "config_path": self.packet_root / CONFIG_RELATIVE,
            "role_root": self.role_root,
            "checkpoint_root": self.checkpoint_root,
            "output_dir": self.output_dir,
        }

    def authenticate(self) -> AuthenticatedConnection:
        """Drive read-order rows 1 through 12 end to end."""

        return authenticate_connection(**self.arguments())

    def rewrite_record(self, document: Mapping[str, Any]) -> dict[str, Any]:
        """Write one edited record over the harness's own path and return arguments."""

        digest = _write_record(self.record_path, document)
        arguments = self.arguments()
        arguments["connection_record_sha256"] = digest
        return arguments

    def restore_record(self) -> None:
        """Put the accepted record back, so one mutation cannot leak into the next."""

        _write_record(self.record_path, self.document)


@pytest.fixture(scope="session")
def harness(tmp_path_factory: pytest.TempPathFactory) -> Harness:
    """Build the isolated packet, role and checkpoint trees exactly once."""

    built = Harness(tmp_path_factory.mktemp("connection-adapter"))
    built.build()
    return built


@pytest.fixture(autouse=True)
def _restored_record(harness: Harness):
    """Put the accepted record back after **every** test in this file.

    The harness is session-scoped because building the role tree is the expensive
    part, so a refusal test that writes an edited record over the harness path would
    otherwise leak into every later test. Restoration is autouse rather than attached
    to the `record` fixture because several tests edit a deep copy of
    `harness.document` directly, and a fixture only some tests request cannot hold an
    invariant that all of them can break.
    """

    yield
    harness.restore_record()


@pytest.fixture()
def record(harness: Harness) -> dict[str, Any]:
    """Return a deep copy of the accepted record for one refusal test to edit."""

    return copy.deepcopy(harness.document)


def _plain(value: Any) -> Any:
    """Return one deeply read-only value as ordinary mutable Python.

    The adapter hands back frozen views -- mappings as proxies and arrays as tuples --
    so an equality against a freshly computed expectation has to be taken over the same
    shapes. Coercing here rather than loosening the module is deliberate: the
    immutability is the property under test elsewhere in this file.
    """

    if isinstance(value, Mapping):
        return {key: _plain(item) for key, item in value.items()}
    if isinstance(value, tuple):
        return [_plain(item) for item in value]
    return value


def _refusal(call: Callable[[], Any]) -> VerificationSceneError:
    """Drive one call, require it to refuse, and return the refusal."""

    with pytest.raises(VerificationSceneError) as excinfo:
        call()
    return excinfo.value


def _drive(harness: Harness, document: Mapping[str, Any]) -> VerificationSceneError:
    """Write one edited record and require the entry point to refuse."""

    return _refusal(lambda: authenticate_connection(**harness.rewrite_record(document)))


# --------------------------------------------------------------------------- #
# Boundaries. These do not test a row; they test that the tests are honest.
# --------------------------------------------------------------------------- #
def test_the_live_packet_holds_no_config_json() -> None:
    """The live packet must contain no frozen config, before and after these tests.

    Finding DD: a contract can make a *filename* an authority, and a synthetic instance
    of an authority is the authority. Nothing in this file may create `config.json`
    anywhere in the live packet, and the frozen-authority tests below therefore write
    their frozen document only into an isolated temporary packet root.
    """

    assert not (PACKET_ROOT / "config.json").exists()
    assert list(PACKET_ROOT.rglob("config.json")) == []


def test_every_harness_path_is_inside_the_temporary_root(harness: Harness) -> None:
    """Every path the harness binds is under `tmp_path` and none is under the packet."""

    live = PACKET_ROOT.resolve()
    for path in harness.arguments().values():
        if not isinstance(path, Path):
            continue
        resolved = Path(path).resolve()
        assert resolved.is_relative_to(harness.root.resolve())
        assert not resolved.is_relative_to(live)


def test_the_adapter_imports_neither_torch_nor_mujoco() -> None:
    """Invariant W11 and V18, re-measured in a fresh interpreter rather than quoted.

    An import graph is a property of a checkout and not of a document, so this is
    measured on every run instead of being carried forward from the session that
    first established it.
    """

    import subprocess

    probe = (
        "import sys; import utils.connection_adapter; "
        "print(int('torch' in sys.modules), int('mujoco' in sys.modules), "
        "int('numpy' in sys.modules))"
    )
    completed = subprocess.run(
        [sys.executable, "-c", probe],
        cwd=str(PACKET_ROOT / "scripts"),
        capture_output=True,
        text=True,
        check=True,
    )
    assert completed.stdout.split() == ["0", "0", "1"]


# --------------------------------------------------------------------------- #
# The accept side. Every applicable row of 4.1 is crossed at least once, which is
# what makes the refusal tests below mean anything.
# --------------------------------------------------------------------------- #
def test_the_authentication_chain_accepts_the_complete_fixture(harness: Harness) -> None:
    """Rows 1 through 12 complete on a coherent, fully authenticated input set."""

    result = harness.authenticate()
    assert result.record.record_label == RECORD_LABEL
    assert result.record.authority == DEVELOPMENT_ONLY
    assert result.config.config.config_hash.startswith("dev-")
    assert result.sources.established_cases == (CASE_ID,)
    assert result.sources.maximum_deviation_m == MAXIMUM_DEVIATION_M
    assert _plain(result.dataset.census) == harness.census
    assert set(result.dataset.audits) == set(AUDIT_NAMES)
    assert len(result.roles.payloads) == len(ROLE_NAMES) * 2
    assert set(result.roles.checkpoint_sha256) == {(CASE_ID, "C1"), (CASE_ID, "S")}


def test_the_accepted_result_is_read_only_all_the_way_down(harness: Harness) -> None:
    """Nothing the chain returns can be edited into a different set of facts."""

    result = harness.authenticate()
    with pytest.raises(TypeError):
        result.dataset.audits["generation_audit"]["status"] = "other"  # type: ignore[index]
    with pytest.raises(TypeError):
        result.sources.documents["established_result"]["read"] = {}  # type: ignore[index]
    with pytest.raises(TypeError):
        result.roles.payloads[(CASE_ID, "C1", "plant")] = {}  # type: ignore[index]
    with pytest.raises(TypeError):
        result.dataset.census["manifest_rows"] = 0  # type: ignore[index]


def test_the_expected_open_set_is_carried_and_covers_every_named_file(
    harness: Harness,
) -> None:
    """The section-4.2 allowlist is derived from the record and travels forward.

    The observed side -- an audit-hook observation of one complete adapter call -- is
    invariant W3 and belongs to the second half of sub-step 4b-ii, which is the round
    that can make one complete call. What this row can hold is that the expected side
    is derived here, names every file the chain actually opens, and is not silently
    empty.
    """

    result = harness.authenticate()
    expected = set(result.expected_opens)
    assert harness.record_path.resolve() in expected
    assert (harness.packet_root / SCHEMA_RELATIVE).resolve() in expected
    assert (harness.packet_root / CONFIG_RELATIVE).resolve() in expected
    assert (harness.role_root / MANIFEST_NAME).resolve() in expected
    for name in AUDIT_NAMES:
        assert (harness.role_root / f"{name}.json").resolve() in expected
    for relative in (
        RESULT_RELATIVE,
        SELECTION_RELATIVE,
        CALIBRATION_RELATIVE,
        GEOMETRY_RELATIVE,
        PRODUCER_RELATIVE,
    ):
        assert (harness.packet_root / relative).resolve() in expected
    assert len(expected) >= 13


# --------------------------------------------------------------------------- #
# Row 4 -- the schema, the config and the authority rule.
# --------------------------------------------------------------------------- #
def test_row4_refuses_a_schema_digest_that_does_not_agree(
    harness: Harness, record: dict[str, Any]
) -> None:
    """A record naming a different schema digest refuses before the config is parsed."""

    record["schema"]["sha256"] = "0" * 64
    error = _drive(harness, record)
    assert error.code == X_IDENTITY_MISMATCH
    assert "schema.sha256" in str(error)


def test_row4_refuses_a_config_digest_that_does_not_agree(
    harness: Harness, record: dict[str, Any]
) -> None:
    """A record naming a different config digest refuses at the same boundary."""

    record["config"]["sha256"] = "1" * 64
    error = _drive(harness, record)
    assert error.code == X_IDENTITY_MISMATCH
    assert "config.sha256" in str(error)


def test_row4_refuses_a_config_hash_the_validated_config_does_not_carry(
    harness: Harness, record: dict[str, Any]
) -> None:
    """The record's semantic `config_hash` is compared, not adopted."""

    record["config"]["config_hash"] = "dev-" + "b" * 64
    error = _drive(harness, record)
    assert error.code == X_IDENTITY_MISMATCH
    # The phrase is unique to row 4. Without it this test stays green on a build that
    # never compares the two hashes, because the established result at row 5 echoes the
    # record's declared hash and refuses the same input one layer later. Found by the
    # mutation sweep.
    assert "but the validated config carries" in str(error)


def test_row4_refuses_an_absent_schema(harness: Harness, record: dict[str, Any]) -> None:
    """A schema path that names nothing refuses rather than raising an OSError."""

    record["schema"]["relative_path"] = "schema/absent-schema.json"
    error = _drive(harness, record)
    assert error.code == X_IDENTITY_MISMATCH


def test_row4_refuses_a_config_that_does_not_validate(
    harness: Harness, tmp_path: Path
) -> None:
    """A structurally broken config refuses as unresolved provenance, not a traceback."""

    broken = tmp_path / "packet"
    shutil.copytree(harness.packet_root, broken)
    document = json.loads((broken / CONFIG_RELATIVE).read_text(encoding="utf-8"))
    del document["values"]
    (broken / CONFIG_RELATIVE).write_text(
        json.dumps(document, indent=2, sort_keys=True), encoding="utf-8"
    )
    edited = copy.deepcopy(harness.document)
    edited["config"]["sha256"] = tracked_text_digest(broken / CONFIG_RELATIVE)
    record_path = broken / record_relative_path(RECORD_LABEL)
    digest = _write_record(record_path, edited)
    error = _refusal(
        lambda: authenticate_connection(
            packet_root=broken,
            connection_record_path=record_path,
            connection_record_sha256=digest,
            config_path=broken / CONFIG_RELATIVE,
            role_root=harness.role_root,
            checkpoint_root=harness.checkpoint_root,
            output_dir=broken / "results" / "verification_connection_development",
        )
    )
    assert error.code == X_PROVENANCE_UNRESOLVED


class _StubConfig:
    """A minimal stand-in for `ValidatedConfig` for the authority 2x2.

    The authority rule reads four properties and nothing else. Driving it against a
    stub rather than against four materialised configurations is what makes the 2x2
    total: the frozen half of the matrix is otherwise reachable only by creating a file
    named `config.json`, and finding DD's whole point is that creating that file is the
    hazard rather than the test.
    """

    def __init__(self, *, status: str, config_hash: str, confirmatory: bool) -> None:
        self.status = status
        self.config_hash = config_hash
        self.document = {"confirmatory_payloads_allowed": confirmatory}

    @property
    def is_frozen(self) -> bool:
        return self.status == "frozen"


DRAFT_STUB = dict(status="draft", config_hash="dev-" + "c" * 64, confirmatory=False)
FROZEN_STUB = dict(status="frozen", config_hash="d" * 64, confirmatory=True)


def test_the_authority_rule_accepts_a_draft_under_development_only() -> None:
    """Cell (DEVELOPMENT_ONLY, draft) is the one accepting cell of its row."""

    require_authority_config_policy(DEVELOPMENT_ONLY, _StubConfig(**DRAFT_STUB))


def test_the_authority_rule_accepts_a_frozen_config_under_final() -> None:
    """Cell (FINAL, frozen) is the one accepting cell of its row."""

    require_authority_config_policy(FINAL, _StubConfig(**FROZEN_STUB))


def test_the_authority_rule_refuses_a_frozen_config_under_development_only() -> None:
    """Cell (DEVELOPMENT_ONLY, frozen) is the cell `require_frozen` cannot hold.

    Measured against the live contract, `load_config(require_frozen=False)` **accepts**
    a frozen document, so this refusal is owed to the adapter's own rule and to nothing
    else. Deleting that rule leaves a development banner over the confirmatory config.
    """

    error = _refusal(
        lambda: require_authority_config_policy(DEVELOPMENT_ONLY, _StubConfig(**FROZEN_STUB))
    )
    assert error.code == X_PROVENANCE_UNRESOLVED


def test_the_authority_rule_refuses_a_draft_under_final() -> None:
    """Cell (FINAL, draft) refuses on the adapter's own rule, independently of loading."""

    error = _refusal(
        lambda: require_authority_config_policy(FINAL, _StubConfig(**DRAFT_STUB))
    )
    assert error.code == X_PROVENANCE_UNRESOLVED
    # The message is asserted, not merely the code. A realistic draft also carries a
    # `dev-` hash, and the dev-trace check one line below refuses the same input -- so a
    # code-only assertion stays green on a build whose lifecycle check is deleted. Found
    # by the mutation sweep.
    assert "may name only the frozen config.json" in str(error)


def test_the_authority_rule_refuses_a_draft_without_the_dev_prefix() -> None:
    """A draft whose semantic hash carries no `dev-` prefix is not a draft identity."""

    stub = _StubConfig(status="draft", config_hash="e" * 64, confirmatory=False)
    error = _refusal(lambda: require_authority_config_policy(DEVELOPMENT_ONLY, stub))
    assert error.code == X_PROVENANCE_UNRESOLVED
    assert "dev-" in str(error)


def test_the_authority_rule_refuses_a_draft_that_permits_confirmatory_payloads() -> None:
    """A development record may not name a config that allows confirmatory generation."""

    stub = _StubConfig(
        status="draft", config_hash="dev-" + "f" * 64, confirmatory=True
    )
    error = _refusal(lambda: require_authority_config_policy(DEVELOPMENT_ONLY, stub))
    assert error.code == X_PROVENANCE_UNRESOLVED


def test_the_authority_rule_refuses_a_frozen_config_carrying_a_dev_trace() -> None:
    """No `dev-` string may travel into a final configuration identity."""

    stub = _StubConfig(status="frozen", config_hash="dev-" + "0" * 64, confirmatory=True)
    error = _refusal(lambda: require_authority_config_policy(FINAL, stub))
    assert error.code == X_PROVENANCE_UNRESOLVED


def test_require_frozen_false_accepts_a_frozen_document(tmp_path: Path) -> None:
    """The measured premise the authority rule exists for, pinned rather than quoted.

    `load_config(require_frozen=False)` is permissive, not draft-only. This test writes
    the frozen document **only** into an isolated temporary packet root and asserts the
    live packet is untouched, which is finding DD's boundary.
    """

    packet = tmp_path / "packet"
    (packet / "schema").mkdir(parents=True)
    (packet / "schema" / "schema.json").write_bytes(LIVE_SCHEMA.read_bytes())
    schema = json.loads(LIVE_SCHEMA.read_text(encoding="utf-8"))
    document = _synthetic_frozen_document(schema, packet / "schema" / "schema.json")
    (packet / "config.json").write_text(
        json.dumps(document, indent=2, sort_keys=True), encoding="utf-8"
    )
    validated = load_config(
        packet / "config.json", packet / "schema" / "schema.json", require_frozen=False
    )
    assert validated.is_frozen
    assert not (PACKET_ROOT / "config.json").exists()


def _synthetic_frozen_document(schema: Mapping[str, Any], schema_path: Path) -> dict[str, Any]:
    """Return a complete synthetic frozen configuration document.

    Every freeze-required path is filled from the draft config's own values where the
    draft has one and with an explicit placeholder where it is null, and the semantic
    hash is recomputed. These bytes are a **fixture**: their name and digest
    authenticate only themselves, and exact-state config approval remains a separate
    social gate that no test can reach.
    """

    from utils.config_contract import expected_config_hash

    contract = schema["config_contract"]
    draft = json.loads(LIVE_DRAFT_CONFIG.read_text(encoding="utf-8"))
    document = copy.deepcopy(draft)
    document["status"] = "frozen"
    document["confirmatory_payloads_allowed"] = True
    document["open_gates"] = []
    document["decision"] = contract["frozen_decision"]
    document["schema_sha256"] = _raw_digest(schema_path)
    document["config_version"] = "synthetic-frozen-fixture-v0"
    for dotted in contract["freeze_required_paths"]:
        _fill_path(document, dotted)
    document["config_hash"] = expected_config_hash(document)
    return document


def _raw_digest(path: Path) -> str:
    """Return one file's raw SHA-256, which is the domain `config_contract` compares."""

    import hashlib

    return hashlib.sha256(path.read_bytes()).hexdigest()


def _fill_path(document: dict[str, Any], dotted: str) -> None:
    """Replace one freeze-required path's null or empty value with a placeholder."""

    segments = dotted.split(".")
    cursor: Any = document
    for segment in segments[:-1]:
        cursor = cursor.setdefault(segment, {})
    leaf = segments[-1]
    value = cursor.get(leaf)
    if value is None or value == {} or value == [] or _contains_null_value(value):
        cursor[leaf] = {"synthetic_frozen_fixture": True}


def _contains_null_value(value: Any) -> bool:
    """Return whether one value carries a `None` anywhere inside it."""

    if value is None:
        return True
    if isinstance(value, Mapping):
        return any(_contains_null_value(item) for item in value.values())
    if isinstance(value, (list, tuple)):
        return any(_contains_null_value(item) for item in value)
    return False


# --------------------------------------------------------------------------- #
# Row 5 -- the source artifacts and every declared field path.
# --------------------------------------------------------------------------- #
@pytest.mark.parametrize(
    "pointer",
    [
        ("established_result", "sha256"),
        ("model_selection", "source", "sha256"),
        ("render_geometry", "tolerance_source", "sha256"),
    ],
)
def test_row5_refuses_a_source_digest_that_does_not_agree(
    harness: Harness, record: dict[str, Any], pointer: tuple[str, ...]
) -> None:
    """Every declared source artifact is hashed before it is parsed."""

    cursor: Any = record
    for segment in pointer[:-1]:
        cursor = cursor[segment]
    cursor[pointer[-1]] = "2" * 64
    error = _drive(harness, record)
    assert error.code == X_IDENTITY_MISMATCH


def test_row5_refuses_a_geometry_producer_digest_that_does_not_agree(
    harness: Harness, record: dict[str, Any]
) -> None:
    """The producer is hashed and never imported; a moved producer refuses."""

    record["render_geometry"]["source"]["producer_sha256"] = "3" * 64
    error = _drive(harness, record)
    assert error.code == X_IDENTITY_MISMATCH
    assert "producer_sha256" in str(error)


def test_row5_refuses_a_threshold_its_named_source_does_not_carry(
    harness: Harness, record: dict[str, Any]
) -> None:
    """Design 3.4: a typed threshold must equal its own approved source, exactly."""

    record["thresholds"]["abstain_threshold"] = ABSTAIN_THRESHOLD + 0.01
    error = _drive(harness, record)
    assert error.code == X_IDENTITY_MISMATCH
    assert "thresholds.abstain_threshold" in str(error)


def test_row5_refuses_an_unknown_threshold_its_named_source_does_not_carry(
    harness: Harness, record: dict[str, Any]
) -> None:
    """The second threshold is checked at its own distinct field path."""

    record["thresholds"]["unknown_threshold"] = UNKNOWN_THRESHOLD + 0.01
    error = _drive(harness, record)
    assert error.code == X_IDENTITY_MISMATCH
    assert "thresholds.unknown_threshold" in str(error)


@pytest.mark.parametrize("field", ["rung", "width"])
def test_row5_refuses_a_capacity_its_named_source_does_not_carry(
    harness: Harness, record: dict[str, Any], field: str
) -> None:
    """The rung and the width are each checked at their own declared field path."""

    record["model_selection"][field] = record["model_selection"][field] + 1
    error = _drive(harness, record)
    assert error.code == X_IDENTITY_MISMATCH
    assert f"model_selection.{field}" in str(error)


def test_row5_refuses_a_tolerance_its_validation_artifact_does_not_carry(
    harness: Harness, record: dict[str, Any]
) -> None:
    """Finding CU: no universal tolerance is guessed; it equals its approved source."""

    record["render_geometry"]["distal_tolerance_m"] = DISTAL_TOLERANCE_M * 2
    error = _drive(harness, record)
    assert error.code == X_IDENTITY_MISMATCH
    assert "distal_tolerance_m" in str(error)


def test_row5_refuses_an_established_result_naming_a_different_split(
    harness: Harness, record: dict[str, Any]
) -> None:
    """The result's own split must be the split the record names."""

    record["established_result"]["split_field_path"] = "read.config_hash"
    error = _drive(harness, record)
    assert error.code == X_IDENTITY_MISMATCH


def test_row5_refuses_an_absent_declared_field_path(
    harness: Harness, record: dict[str, Any]
) -> None:
    """A field path the artifact does not carry is a refusal, never a `None`."""

    record["thresholds"]["sources"]["abstain_threshold"]["field_path"] = "values.absent"
    error = _drive(harness, record)
    assert error.code == X_IDENTITY_MISMATCH
    assert "values.absent" in str(error)


def test_row5_refuses_a_maximum_deviation_above_the_declared_tolerance(
    harness: Harness, tmp_path: Path
) -> None:
    """The runtime half of finding CU: an unjustified margin cannot travel silently."""

    packet = tmp_path / "packet"
    shutil.copytree(harness.packet_root, packet)
    _write_json(
        packet / GEOMETRY_RELATIVE,
        {
            "agreement": {
                "maximum_deviation_m": DISTAL_TOLERANCE_M * 10,
                "tolerance_m": DISTAL_TOLERANCE_M,
            }
        },
    )
    edited = copy.deepcopy(harness.document)
    edited["render_geometry"]["tolerance_source"]["sha256"] = tracked_text_digest(
        packet / GEOMETRY_RELATIVE
    )
    record_path = packet / record_relative_path(RECORD_LABEL)
    digest = _write_record(record_path, edited)
    error = _refusal(
        lambda: authenticate_connection(
            packet_root=packet,
            connection_record_path=record_path,
            connection_record_sha256=digest,
            config_path=packet / CONFIG_RELATIVE,
            role_root=harness.role_root,
            checkpoint_root=harness.checkpoint_root,
            output_dir=packet / "results" / "verification_connection_development",
        )
    )
    assert error.code == X_IDENTITY_MISMATCH
    assert "exceeds the declared tolerance" in str(error)


# --------------------------------------------------------------------------- #
# Row 6 -- the manifest, both audits and the recomputed census.
# --------------------------------------------------------------------------- #
def test_row6_refuses_a_manifest_digest_that_does_not_agree(
    harness: Harness, record: dict[str, Any]
) -> None:
    """`manifest.csv` is hashed before it is parsed."""

    record["data_root"]["manifest_sha256"] = "4" * 64
    error = _drive(harness, record)
    assert error.code == X_IDENTITY_MISMATCH
    assert "manifest_sha256" in str(error)


@pytest.mark.parametrize("name", list(AUDIT_NAMES))
def test_row6_refuses_an_audit_digest_that_does_not_agree(
    harness: Harness, record: dict[str, Any], name: str
) -> None:
    """Both dataset audits are hashed before either is parsed."""

    record["data_root"][name]["sha256"] = "5" * 64
    error = _drive(harness, record)
    assert error.code == X_IDENTITY_MISMATCH
    assert name in str(error)


@pytest.mark.parametrize("name", list(AUDIT_NAMES))
@pytest.mark.parametrize("field", ["status", "assignment_hash", "config_hash"])
def test_row6_refuses_an_audit_echo_that_does_not_agree(
    harness: Harness, record: dict[str, Any], name: str, field: str
) -> None:
    """Each of the three declared echoes is compared against the audit itself."""

    record["data_root"][name][field] = (
        "dev-" + "6" * 64 if field != "status" else "unexpected_status"
    )
    error = _drive(harness, record)
    assert error.code == X_IDENTITY_MISMATCH


def test_row6_refuses_two_audits_that_disagree_about_the_assignment(
    harness: Harness, record: dict[str, Any], tmp_path: Path
) -> None:
    """One dataset has one assignment; two audits claiming two refuse."""

    role_root = tmp_path / DATASET_LABEL
    shutil.copytree(harness.role_root, role_root)
    other = "dev-" + "7" * 64
    document = json.loads(
        (role_root / "independent_audit.json").read_text(encoding="utf-8")
    )
    document["assignment_hash"] = other
    _write_json(role_root / "independent_audit.json", document)
    record["data_root"]["independent_audit"]["assignment_hash"] = other
    record["data_root"]["independent_audit"]["sha256"] = external_digest(
        role_root / "independent_audit.json"
    )
    arguments = harness.rewrite_record(record)
    arguments["role_root"] = role_root
    error = _refusal(lambda: authenticate_connection(**arguments))
    assert error.code == X_IDENTITY_MISMATCH
    assert "assignment_hash" in str(error)


@pytest.mark.parametrize("field", list(MANIFEST_CENSUS_FIELDS))
def test_row6_refuses_an_audit_census_the_manifest_does_not_support(
    harness: Harness, tmp_path: Path, field: str
) -> None:
    """Finding CW mechanism 1: the census is recomputed, never adopted."""

    role_root = tmp_path / DATASET_LABEL
    shutil.copytree(harness.role_root, role_root)
    document = json.loads(
        (role_root / "generation_audit.json").read_text(encoding="utf-8")
    )
    block = document[MANIFEST_AUDIT_KEY]
    value = block[field]
    if isinstance(value, int) and not isinstance(value, bool):
        block[field] = value + 1
    elif isinstance(value, list):
        block[field] = value + ["O"]
    else:
        block[field] = dict(value)
        block[field]["test"] = 1
    _write_json(role_root / "generation_audit.json", document)
    edited = copy.deepcopy(harness.document)
    edited["data_root"]["generation_audit"]["sha256"] = external_digest(
        role_root / "generation_audit.json"
    )
    arguments = harness.rewrite_record(edited)
    arguments["role_root"] = role_root
    error = _refusal(lambda: authenticate_connection(**arguments))
    assert error.code == X_IDENTITY_MISMATCH
    assert field in str(error)


def test_row6_refuses_an_established_result_naming_other_cases(
    harness: Harness, tmp_path: Path
) -> None:
    """The surface presents exactly the cases the prior read established."""

    packet = tmp_path / "packet"
    shutil.copytree(harness.packet_root, packet)
    _write_json(
        packet / RESULT_RELATIVE,
        {
            "read": {
                "cases": [CASE_ID, "another-case"],
                "config_hash": harness.config_hash,
                "split": SPLIT,
            },
            "status": "synthetic_fixture_established_result",
        },
    )
    edited = copy.deepcopy(harness.document)
    edited["established_result"]["sha256"] = tracked_text_digest(packet / RESULT_RELATIVE)
    record_path = packet / record_relative_path(RECORD_LABEL)
    digest = _write_record(record_path, edited)
    error = _refusal(
        lambda: authenticate_connection(
            packet_root=packet,
            connection_record_path=record_path,
            connection_record_sha256=digest,
            config_path=packet / CONFIG_RELATIVE,
            role_root=harness.role_root,
            checkpoint_root=harness.checkpoint_root,
            output_dir=packet / "results" / "verification_connection_development",
        )
    )
    assert error.code == X_IDENTITY_MISMATCH
    assert "the record's menu names" in str(error)


def test_row6_refuses_a_run_the_manifest_does_not_contain(
    harness: Harness, record: dict[str, Any]
) -> None:
    """A named run identity must exist in the authenticated manifest."""

    arm = record["cases"][0]["arms"]["C1"]
    arm["run_id"] = "fixture_dev_absent"
    arm["manifest_row"]["run_id"] = "fixture_dev_absent"
    error = _drive(harness, record)
    assert error.code == X_IDENTITY_MISMATCH
    assert MANIFEST_NAME in str(error)


def test_row6_refuses_a_run_that_belongs_to_another_split(harness: Harness) -> None:
    """A `val` row named by a `dev` record refuses with the split code.

    The record layer already refuses an echoed row whose own `split` field disagrees
    with the record, so this drives the deeper state: the echo is internally coherent
    and the *manifest* disagrees. That is the state a record approved against one tree
    and pointed at another would reach.
    """

    edited = copy.deepcopy(harness.document)
    case = edited["cases"][0]
    case["pair_id"] = "fixture_val"
    for suite in ("C1", "S"):
        arm = case["arms"][suite]
        arm["run_id"] = f"fixture_val_{suite}"
        row = dict(arm["manifest_row"])
        row["run_id"] = f"fixture_val_{suite}"
        row["pair_id"] = "fixture_val"
        arm["manifest_row"] = row
    error = _drive(harness, edited)
    assert error.code == X_SPLIT_FORBIDDEN


def test_the_census_refuses_a_manifest_carrying_two_train_seeds(
    harness: Harness,
) -> None:
    """The audits report one `train_seed`; a census that picked one would adopt it."""

    rows = list(harness.manifest_rows.values())
    import dataclasses

    mutated = [rows[0]] + [dataclasses.replace(row, train_seed=9) for row in rows[1:]]
    error = _refusal(lambda: manifest_census(mutated))
    assert error.code == X_IDENTITY_MISMATCH
    assert "train_seed" in str(error)


def test_the_census_refuses_an_empty_manifest() -> None:
    """A census over nothing is not a census."""

    error = _refusal(lambda: manifest_census([]))
    assert error.code == X_IDENTITY_MISMATCH


def test_the_census_reproduces_the_fixture_tree(harness: Harness) -> None:
    """The recomputed census is the fixture's own shape, stated as literals."""

    census = harness.census
    assert census["manifest_rows"] == 4
    assert census["reservations"] == 2
    assert census["splits"] == {"dev": 2, "val": 2}
    assert census["suites"] == ["C1", "S"]
    assert census["test_rows"] == 0
    assert census["train_seed"] == 0


# --------------------------------------------------------------------------- #
# Rows 7-12 -- the role layout, the indexes, the manifest rows, the payloads.
# --------------------------------------------------------------------------- #
def test_row7_refuses_an_absent_role_root(harness: Harness, tmp_path: Path) -> None:
    """An absent role directory is `X_ROLE_ABSENT`, never a digest complaint."""

    role_root = tmp_path / DATASET_LABEL
    shutil.copytree(harness.role_root, role_root)
    shutil.rmtree(role_root / "plant")
    arguments = harness.arguments()
    arguments["role_root"] = role_root
    error = _refusal(lambda: authenticate_connection(**arguments))
    assert error.code == X_ROLE_ABSENT
    assert "the plant index of the role root" in str(error)


def test_row7_refuses_an_absent_role_index(harness: Harness, tmp_path: Path) -> None:
    """A role directory without its index cannot authorise any payload."""

    role_root = tmp_path / DATASET_LABEL
    shutil.copytree(harness.role_root, role_root)
    (role_root / "labels" / ROLE_INDEX_NAME).unlink()
    arguments = harness.arguments()
    arguments["role_root"] = role_root
    error = _refusal(lambda: authenticate_connection(**arguments))
    assert error.code == X_ROLE_ABSENT
    assert ROLE_INDEX_NAME in str(error)


@pytest.mark.parametrize("role", list(ROLE_NAMES))
def test_row8_refuses_an_index_digest_that_does_not_agree(
    harness: Harness, record: dict[str, Any], role: str
) -> None:
    """Every named index is hashed before any of them is parsed."""

    record["cases"][0]["arms"]["C1"]["roles"][role]["index_sha256"] = "8" * 64
    error = _drive(harness, record)
    assert error.code == X_IDENTITY_MISMATCH
    assert "index_sha256" in str(error)


def test_row9_refuses_a_run_the_authenticated_index_does_not_authorise(
    harness: Harness, tmp_path: Path
) -> None:
    """A run absent from its own index is `X_ROLE_UNAUTHORIZED`, not a mismatch.

    The index is edited and the record re-declares the new index digest, so the
    refusal cannot come from row 8: the state under test is an authenticated index
    that does not carry the row the record names.
    """

    role_root = tmp_path / DATASET_LABEL
    shutil.copytree(harness.role_root, role_root)
    index = role_root / "plant" / ROLE_INDEX_NAME
    lines = index.read_text(encoding="utf-8").splitlines(keepends=True)
    kept = [lines[0]] + [line for line in lines[1:] if "fixture_dev_C1" not in line]
    index.write_text("".join(kept), encoding="utf-8", newline="")
    edited = copy.deepcopy(harness.document)
    for suite in ("C1", "S"):
        edited["cases"][0]["arms"][suite]["roles"]["plant"]["index_sha256"] = (
            external_digest(index)
        )
    arguments = harness.rewrite_record(edited)
    arguments["role_root"] = role_root
    error = _refusal(lambda: authenticate_connection(**arguments))
    assert error.code == X_ROLE_UNAUTHORIZED


def test_row9_refuses_a_payload_path_the_index_row_does_not_name(
    harness: Harness, record: dict[str, Any]
) -> None:
    """The declared payload path must be exactly the one the index row authorises."""

    roles = record["cases"][0]["arms"]["C1"]["roles"]
    roles["plant"]["payload_relative_path"] = "plant/fixture_val_C1.npz"
    roles["plant"]["payload_sha256"] = external_digest(
        harness.role_root / "plant" / "fixture_val_C1.npz"
    )
    error = _drive(harness, record)
    assert error.code == X_IDENTITY_MISMATCH
    assert "the authenticated index row names" in str(error)


@pytest.mark.parametrize(
    "field", ["scenario_spec_id", "estimator_id", "sim_seed", "fault_seed"]
)
def test_row10_refuses_an_echoed_manifest_field_that_does_not_agree(
    harness: Harness, record: dict[str, Any], field: str
) -> None:
    """Invariant W4: all 20 fields are compared, not adopted."""

    row = record["cases"][0]["arms"]["C1"]["manifest_row"]
    row[field] = row[field] + 1 if isinstance(row[field], int) else row[field] + "-x"
    error = _drive(harness, record)
    assert error.code == X_IDENTITY_MISMATCH
    assert field in str(error)


def test_row10_compares_every_one_of_the_twenty_schema_a_fields(
    harness: Harness,
) -> None:
    """The comparison is over the schema-A field list itself, not a transcription.

    A test that mutated only a chosen few fields would hold nothing about the ones it
    did not name, so this drives every field the contract declares and requires each
    one to refuse. `MANIFEST_ROW_FIELDS` is derived from `IdentityManifestRow`, so a
    schema-A change moves this test with the contract rather than leaving it stale.
    """

    assert len(MANIFEST_ROW_FIELDS) == 20
    for field in MANIFEST_ROW_FIELDS:
        edited = copy.deepcopy(harness.document)
        row = edited["cases"][0]["arms"]["C1"]["manifest_row"]
        value = row[field]
        row[field] = value + 1 if isinstance(value, int) else f"{value}-mutated"
        error = _drive(harness, edited)
        assert error.code in {X_IDENTITY_MISMATCH, X_SPLIT_FORBIDDEN, X_CONNECTION_UNAUTHORIZED}
    harness.restore_record()


@pytest.mark.parametrize("role", list(ROLE_NAMES))
def test_row11_refuses_a_payload_digest_that_does_not_agree(
    harness: Harness, record: dict[str, Any], role: str
) -> None:
    """Every payload is hashed before any payload is loaded."""

    record["cases"][0]["arms"]["S"]["roles"][role]["payload_sha256"] = "9" * 64
    error = _drive(harness, record)
    assert error.code == X_IDENTITY_MISMATCH


def test_row11_refuses_a_checkpoint_digest_that_does_not_agree(
    harness: Harness, record: dict[str, Any]
) -> None:
    """The checkpoint is digested and never loaded; a moved one refuses."""

    record["cases"][0]["arms"]["C1"]["checkpoint"]["sha256"] = "a" * 64
    error = _drive(harness, record)
    assert error.code == X_IDENTITY_MISMATCH
    assert "checkpoint.sha256" in str(error)


def test_row11_refuses_an_absent_checkpoint(
    harness: Harness, record: dict[str, Any]
) -> None:
    """A checkpoint path naming nothing is an absent role, not a digest complaint."""

    record["cases"][0]["arms"]["S"]["checkpoint"]["relative_path"] = (
        f"{PAIR_ID}/absent.pt"
    )
    error = _drive(harness, record)
    assert error.code == X_ROLE_ABSENT


def test_row11_refuses_a_payload_that_disagrees_with_its_index_row(
    harness: Harness, tmp_path: Path
) -> None:
    """The two comparisons at row 11 are not redundant, and this is the state that shows it.

    The record and the payload agree; the *index row* does not. That is the tree
    moving underneath an approved record, and a single comparison against the record
    alone would accept it.
    """

    role_root = tmp_path / DATASET_LABEL
    shutil.copytree(harness.role_root, role_root)
    index = role_root / "labels" / ROLE_INDEX_NAME
    text = index.read_text(encoding="utf-8")
    original = external_digest(role_root / "labels" / "fixture_dev_C1.npz")
    index.write_text(text.replace(original, "b" * 64), encoding="utf-8", newline="")
    edited = copy.deepcopy(harness.document)
    for suite in ("C1", "S"):
        edited["cases"][0]["arms"][suite]["roles"]["labels"]["index_sha256"] = (
            external_digest(index)
        )
    arguments = harness.rewrite_record(edited)
    arguments["role_root"] = role_root
    error = _refusal(lambda: authenticate_connection(**arguments))
    assert error.code == X_IDENTITY_MISMATCH
    assert "its authenticated index row records" in str(error)


def test_row12_loads_exactly_the_named_payload_set(harness: Harness) -> None:
    """Step 12 loads the eight named payloads and nothing else."""

    result = harness.authenticate()
    assert set(result.roles.payloads) == {
        (CASE_ID, suite, role) for suite in ("C1", "S") for role in ROLE_NAMES
    }
    plant = result.roles.payloads[(CASE_ID, "C1", "plant")]
    assert "q_true" in plant
    labels = result.roles.payloads[(CASE_ID, "C1", "labels")]
    assert "source_class" in labels


def test_row12_refuses_a_payload_the_role_loader_rejects(
    harness: Harness, tmp_path: Path
) -> None:
    """A schema-invalid payload refuses through the loader rather than crashing.

    Every earlier digest is re-declared so the refusal is owed to the loader's own
    schema and semantic checks and not to row 11.
    """

    import numpy as np

    role_root = tmp_path / DATASET_LABEL
    shutil.copytree(harness.role_root, role_root)
    original = external_digest(harness.role_root / "labels" / "fixture_dev_C1.npz")
    # The two arms of one pair share a label payload byte for byte -- the label is a
    # property of the fault, not of the suite -- so both files and both index rows
    # move together. Editing one and leaving the other would refuse at row 11 for the
    # arm that did not move, and this test would then never reach the loader.
    for suite in ("C1", "S"):
        payload_path = role_root / "labels" / f"fixture_dev_{suite}.npz"
        with np.load(payload_path, allow_pickle=False) as archive:
            payload = {name: np.asarray(archive[name]) for name in archive.files}
        payload["severity"] = np.asarray("not-a-number")
        np.savez(payload_path, **payload)
    mutated = external_digest(role_root / "labels" / "fixture_dev_C1.npz")
    assert external_digest(role_root / "labels" / "fixture_dev_S.npz") == mutated
    index = role_root / "labels" / ROLE_INDEX_NAME
    index.write_text(
        index.read_text(encoding="utf-8").replace(original, mutated),
        encoding="utf-8",
        newline="",
    )
    edited = copy.deepcopy(harness.document)
    for suite in ("C1", "S"):
        edited["cases"][0]["arms"][suite]["roles"]["labels"]["index_sha256"] = (
            external_digest(index)
        )
        edited["cases"][0]["arms"][suite]["roles"]["labels"]["payload_sha256"] = mutated
    arguments = harness.rewrite_record(edited)
    arguments["role_root"] = role_root
    error = _refusal(lambda: authenticate_connection(**arguments))
    assert error.code == X_IDENTITY_MISMATCH
    assert "did not load" in str(error)


# --------------------------------------------------------------------------- #
# The digest domains and the field-path grammar, pinned as contract facts.
# --------------------------------------------------------------------------- #
def test_the_tracked_text_domain_is_invariant_to_line_endings(tmp_path: Path) -> None:
    """The canonical domain digests the document, not the checkout's copy of it.

    This is why every tracked packet text file is hashed in this domain: the same
    document written LF and CRLF is one digest here and two under a raw rule, and this
    repository materialises unpinned tracked text as CRLF on a fresh clone.
    """

    lf = tmp_path / "lf.json"
    crlf = tmp_path / "crlf.json"
    lf.write_bytes(b'{\n  "a": 1\n}\n')
    crlf.write_bytes(b'{\r\n  "a": 1\r\n}\r\n')
    assert tracked_text_digest(lf) == tracked_text_digest(crlf)
    assert external_digest(lf) != external_digest(crlf)


def test_the_live_draft_config_is_a_file_whose_two_domains_can_disagree() -> None:
    """The concrete reason the canonical rule is forced rather than preferred.

    `config/draft-config-v0.1.json` is not end-of-line pinned. Whether the two domains
    agree is a property of the checkout, so this asserts the durable half: the canonical
    digest of the live file equals the canonical digest of its own LF rendering, which
    a raw rule cannot promise.
    """

    raw = LIVE_DRAFT_CONFIG.read_bytes()
    folded = raw.replace(b"\r\n", b"\n")
    import hashlib

    assert tracked_text_digest(LIVE_DRAFT_CONFIG) == hashlib.sha256(folded).hexdigest()


def test_the_role_tree_domain_is_the_domain_its_indexes_record(harness: Harness) -> None:
    """Payload identity is forced into the raw domain by the index contract itself."""

    from utils.storage_contract import read_role_index

    rows = read_role_index(harness.role_root / "plant" / ROLE_INDEX_NAME, observation=False)
    for row in rows:
        assert external_digest(harness.role_root / "plant" / row.npz_path) == row.sha256


@pytest.mark.parametrize(
    "path,expected",
    [
        ("a", 1),
        ("b.c", 2),
        ("b.d.0", 3),
        ("b.d.1.e", 4),
    ],
)
def test_the_field_path_grammar_resolves_objects_and_array_indices(
    path: str, expected: int
) -> None:
    """A digit segment indexes an array; every other segment names an object key."""

    document = {"a": 1, "b": {"c": 2, "d": [3, {"e": 4}]}}
    assert value_at_field_path(document, path, where="probe") == expected


@pytest.mark.parametrize("path", ["", "a..b", "b.z", "b.d.9", "a.b", "b.d.x"])
def test_the_field_path_grammar_refuses_every_malformed_or_absent_path(path: str) -> None:
    """Malformed, absent and mis-kinded paths all refuse rather than returning `None`."""

    document = {"a": 1, "b": {"c": 2, "d": [3, {"e": 4}]}}
    error = _refusal(lambda: value_at_field_path(document, path, where="probe"))
    assert error.code == X_IDENTITY_MISMATCH


def test_strict_json_refuses_a_duplicate_key() -> None:
    """A duplicate key makes one byte string two documents, and a digest cannot see it."""

    error = _refusal(lambda: strict_json_document(b'{"a": 1, "a": 2}', "probe"))
    assert error.code == X_IDENTITY_MISMATCH
    assert "repeats the object key" in str(error)


@pytest.mark.parametrize("literal", [b'{"a": NaN}', b'{"a": Infinity}', b'{"a": -Infinity}'])
def test_strict_json_refuses_every_bare_non_finite_constant(literal: bytes) -> None:
    """`json` accepts these by default; a source artifact carrying one is a defect."""

    error = _refusal(lambda: strict_json_document(literal, "probe"))
    assert error.code == X_IDENTITY_MISMATCH


@pytest.mark.parametrize(
    "raw",
    [
        b'{"a": 1e9999}',
        b'{"a": -1e9999}',
        b'{"a": {"b": 1e9999}}',
        b'{"a": [0, 1e9999]}',
    ],
)
def test_strict_json_refuses_a_non_finite_the_parser_produces_itself(raw: bytes) -> None:
    """The reachable non-finite path is an exponent overflow, not a bare constant.

    `parse_constant` never sees `1e9999`: `json` turns it into `inf` inside its own
    number parser, so the bare-constant hook cannot refuse it and only the recursive
    finiteness walk can. A suite that tested `NaN` and `Infinity` literals alone would
    stay green on a build with no walk at all -- measured by this build round's mutation
    sweep, which is also the round that found this test missing.
    """

    error = _refusal(lambda: strict_json_document(raw, "probe"))
    assert error.code == X_IDENTITY_MISMATCH
    assert "non-finite" in str(error)


@pytest.mark.parametrize("raw", [b"[1, 2]", b'"text"', b"{", b"\xff\xfe"])
def test_strict_json_refuses_every_document_that_is_not_one_json_object(raw: bytes) -> None:
    """A source artifact is one JSON object; anything else refuses."""

    error = _refusal(lambda: strict_json_document(raw, "probe"))
    assert error.code == X_IDENTITY_MISMATCH


def test_the_role_layout_rule_matches_the_loader_it_hands_paths_to(
    harness: Harness,
) -> None:
    """`role_root_for` and `role_contract._expected_root` agree on every role.

    The adapter constructs the path that the loader's own rule then checks, so the two
    are held together here rather than by a comment. A role whose constructed root the
    loader refuses would surface as an unexplained storage error inside step 12.
    """

    from utils.role_contract import RolePayloadLoader

    schema = json.loads((harness.packet_root / SCHEMA_RELATIVE).read_text(encoding="utf-8"))
    config = load_config(
        harness.packet_root / CONFIG_RELATIVE, harness.packet_root / SCHEMA_RELATIVE
    )
    for role in ROLE_NAMES:
        for suite in ("C1", "S"):
            directory = role_root_for(harness.role_root, role, suite)
            loader = RolePayloadLoader(
                directory,
                role,
                schema,
                config,
                suite=suite if role in SUITE_QUALIFIED_ROLES else None,
            )
            assert loader.run_ids


def test_the_suite_qualified_roles_are_exactly_the_two_schema_e_names() -> None:
    """Stated as literals, because the value is the decision and not the relationship."""

    assert SUITE_QUALIFIED_ROLES == frozenset({"estimator_outputs", "controller_logs"})
    assert set(ROLE_NAMES) == {"plant", "labels", "estimator_outputs", "controller_logs"}


def test_the_census_field_list_is_exactly_the_six_audited_names() -> None:
    """The audited census is a fixed list; adding or dropping one changes the check."""

    assert MANIFEST_CENSUS_FIELDS == (
        "manifest_rows",
        "reservations",
        "splits",
        "suites",
        "test_rows",
        "train_seed",
    )
    assert AUDIT_NAMES == ("generation_audit", "independent_audit")


# --------------------------------------------------------------------------- #
# Acceptance test B8 -- both authority-scoped P1 branches cross the one entry point.
# --------------------------------------------------------------------------- #
def _b8_packet(harness: Harness, destination: Path, *, corrupt_source: bool) -> Path:
    """Copy the harness packet and optionally corrupt the step-5 stopping source."""

    shutil.copytree(harness.packet_root, destination)
    if corrupt_source:
        _write_json(
            destination / SELECTION_RELATIVE,
            {"selected": {"rung": SELECTED_RUNG + 5, "width": SELECTED_WIDTH}},
        )
    return destination


def _b8_drive(
    harness: Harness, packet: Path, document: Mapping[str, Any]
) -> VerificationSceneError:
    """Drive one B8 leg through the one roles-mode entry point.

    The corrupted step-5 source is re-declared at its new digest, so the positive
    legs stop on the source's *value* rather than on its identity. That distinction
    matters: a digest refusal proves only that the file moved, while a value refusal
    proves the artifact was digested, parsed and compared -- which is the evidence
    that step 4 accepted the configuration and handed control onward.
    """

    document = copy.deepcopy(dict(document))
    document["model_selection"]["source"]["sha256"] = tracked_text_digest(
        packet / SELECTION_RELATIVE
    )
    record_path = packet / record_relative_path(RECORD_LABEL)
    digest = _write_record(record_path, document)
    return _refusal(
        lambda: authenticate_connection(
            packet_root=packet,
            connection_record_path=record_path,
            connection_record_sha256=digest,
            config_path=packet / document["config"]["relative_path"],
            role_root=harness.role_root,
            checkpoint_root=harness.checkpoint_root,
            output_dir=packet
            / (
                "results/verification_connection_development"
                if document["authority"] == DEVELOPMENT_ONLY
                else "results/verification_connection/bundles"
            ),
        )
    )


def test_b8_leg1_development_only_with_the_draft_passes_step_four(
    harness: Harness, tmp_path: Path
) -> None:
    """Leg 1: the draft under `DEVELOPMENT_ONLY` clears step 4 and stops at step 5.

    The stop condition is a *deliberately corrupted step-5 source*, which is what makes
    the leg positive: a refusal at step 4 and a refusal at step 5 are different
    outcomes, and only the second proves the config was accepted.
    """

    packet = _b8_packet(harness, tmp_path / "packet", corrupt_source=True)
    error = _b8_drive(harness, packet, harness.document)
    assert error.code == X_IDENTITY_MISMATCH
    assert "model_selection.rung" in str(error)


def test_b8_leg2_the_same_draft_under_final_refuses_at_step_four(
    harness: Harness, tmp_path: Path
) -> None:
    """Leg 2: the same bytes under `FINAL` never reach step 5.

    This leg refuses inside `load_config`, because `require_frozen=True` does refuse a
    draft. Leg 4 refuses in the adapter's own rule, because `require_frozen=False` does
    **not** refuse a frozen document. The two opposite-authority legs therefore fire at
    different layers, and that is exactly why the 2x2 is also driven directly against
    `require_authority_config_policy`: composed behaviour that happens to refuse is not
    evidence that every cell is checked.
    """

    packet = _b8_packet(harness, tmp_path / "packet", corrupt_source=True)
    document = copy.deepcopy(harness.document)
    document["authority"] = FINAL
    _retarget_split(document, "val", harness, packet)
    error = _b8_drive(harness, packet, document)
    assert error.code == X_PROVENANCE_UNRESOLVED
    assert "confirmatory operation refuses draft configuration" in str(error)
    assert "model_selection" not in str(error)


def test_b8_leg3_a_frozen_document_under_final_passes_step_four(
    harness: Harness, tmp_path: Path
) -> None:
    """Leg 3: a synthetic frozen `config.json` under `FINAL` reaches the same stop.

    The frozen bytes are written **only** as `<temporary-packet-root>/config.json`.
    They are a fixture: their name and digest authenticate only themselves, and
    exact-state config approval remains a separate social gate.
    """

    packet = _b8_packet(harness, tmp_path / "packet", corrupt_source=True)
    frozen_path = _write_frozen_fixture(packet)
    document = copy.deepcopy(harness.document)
    document["authority"] = FINAL
    _point_at_frozen(document, packet, frozen_path)
    _retarget_split(document, "val", harness, packet)
    error = _b8_drive(harness, packet, document)
    assert error.code == X_IDENTITY_MISMATCH
    assert "model_selection.rung" in str(error)
    assert not (PACKET_ROOT / "config.json").exists()


def test_b8_leg4_the_frozen_document_under_development_only_refuses_at_step_four(
    harness: Harness, tmp_path: Path
) -> None:
    """Leg 4: the frozen document under `DEVELOPMENT_ONLY` refuses before step 5.

    This is the cell `require_frozen=False` accepts, so the refusal is the adapter's
    own rule doing the work.
    """

    packet = _b8_packet(harness, tmp_path / "packet", corrupt_source=True)
    frozen_path = _write_frozen_fixture(packet)
    document = copy.deepcopy(harness.document)
    _point_at_frozen(document, packet, frozen_path)
    error = _b8_drive(harness, packet, document)
    assert error.code == X_PROVENANCE_UNRESOLVED
    assert "names a frozen configuration" in str(error)
    assert "model_selection" not in str(error)


def _write_frozen_fixture(packet: Path) -> Path:
    """Write the synthetic frozen document as `<packet>/config.json` and return it."""

    schema = json.loads((packet / SCHEMA_RELATIVE).read_text(encoding="utf-8"))
    document = _synthetic_frozen_document(schema, packet / SCHEMA_RELATIVE)
    path = packet / "config.json"
    path.write_text(json.dumps(document, indent=2, sort_keys=True), encoding="utf-8")
    return path


def _point_at_frozen(document: dict[str, Any], packet: Path, frozen_path: Path) -> None:
    """Repoint one record at the temporary frozen configuration."""

    frozen = json.loads(frozen_path.read_text(encoding="utf-8"))
    document["config"] = {
        "config_hash": frozen["config_hash"],
        "relative_path": "config.json",
        "sha256": tracked_text_digest(frozen_path),
    }


def _retarget_split(
    document: dict[str, Any], split: str, harness: Harness, packet: Path
) -> None:
    """Move one record onto the fixture's other split, keeping every echo coherent.

    The established result names the split it was read over, so moving the record
    without moving the artifact would stop the leg at row 5 for a reason that has
    nothing to do with authority. The artifact is rewritten inside the temporary
    packet only.
    """

    _write_json(
        packet / RESULT_RELATIVE,
        {
            "read": {
                "cases": [CASE_ID],
                "config_hash": document["config"]["config_hash"],
                "split": split,
            },
            "status": "synthetic_fixture_established_result",
        },
    )
    document["established_result"] = dict(document["established_result"])
    document["established_result"]["sha256"] = tracked_text_digest(
        packet / RESULT_RELATIVE
    )
    document["split"] = split
    case = document["cases"][0]
    case["pair_id"] = f"fixture_{split}"
    for suite in ("C1", "S"):
        arm = case["arms"][suite]
        run_id = f"fixture_{split}_{suite}"
        arm["run_id"] = run_id
        row = asdict(harness.manifest_rows[run_id])
        arm["manifest_row"] = {name: row[name] for name in MANIFEST_ROW_FIELDS}
        for role in ROLE_NAMES:
            relative = (
                f"{role}/{suite}/{run_id}.npz"
                if role in SUITE_QUALIFIED_ROLES
                else f"{role}/{run_id}.npz"
            )
            arm["roles"][role]["payload_relative_path"] = relative
            arm["roles"][role]["payload_sha256"] = external_digest(
                harness.role_root / relative
            )

def test_the_entry_point_binds_only_the_packet_root_it_is_given(
    harness: Harness,
) -> None:
    """Invariant W8: one injected root governs every packet-relative resolution.

    Every packet-relative path the chain resolves is asserted to be under the injected
    root, which is the positive statement -- an absent override argument is not a bound
    root, and only naming the root the resolution actually used can show which one it
    was.
    """

    result = harness.authenticate()
    bound = result.bound
    assert bound.packet_root == harness.packet_root.resolve()
    for path in (bound.schema_path, bound.config_path, bound.record_path, bound.output_root):
        assert path.is_relative_to(harness.packet_root.resolve())
    for path in bound.packet_artifacts.values():
        assert path.is_relative_to(harness.packet_root.resolve())
    assert not bound.role_root.is_relative_to(harness.packet_root.resolve())
    assert not bound.checkpoint_root.is_relative_to(harness.packet_root.resolve())


def test_the_entry_point_is_the_only_composition_of_the_read_order(
    harness: Harness,
) -> None:
    """The staged functions compose into exactly what the entry point returns.

    The order is the contract, so the pieces are also driven in sequence here and the
    two results compared. If a later refactor let a caller reassemble a different
    order, this test would still pass and the entry point would still be the only
    supported composition -- which is why the entry point exists as one implementation
    rather than as a sequence a caller assembles.
    """

    arguments = harness.arguments()
    record_value = load_connection_record(
        arguments["connection_record_path"], arguments["connection_record_sha256"]
    )
    bound = bind_root_domains(
        record_value,
        packet_root=arguments["packet_root"],
        connection_record_path=arguments["connection_record_path"],
        config_path=arguments["config_path"],
        role_root=arguments["role_root"],
        checkpoint_root=arguments["checkpoint_root"],
        output_dir=arguments["output_dir"],
    )
    config = authenticate_config(record_value, bound)
    sources = authenticate_sources(record_value, bound)
    dataset = authenticate_dataset(record_value, bound, sources)
    roles = authenticate_roles(record_value, bound, config, dataset)
    whole = harness.authenticate()
    assert whole.config.config_sha256 == config.config_sha256
    assert whole.sources.established_cases == sources.established_cases
    assert _plain(whole.dataset.census) == _plain(dataset.census)
    assert set(whole.roles.payloads) == set(roles.payloads)
