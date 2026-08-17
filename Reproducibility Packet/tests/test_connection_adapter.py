"""Tests for the Slot-8 connection adapter's authentication chain (rows 4-18).

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
     independent synthetic maps -- and nothing in this file uses it as one. Row 18's
     accept path is driven instead by the dedicated coherent fixture, installed over
     this harness by `_coherent_geometry`; the contract fixture's own toy declaration
     is what row 18's record-level refusals are driven against, which is the only role
     design 2.4 leaves it.

**What this file does not do.** It authors no production connection record, runs no
adapter invocation against real data, opens no `dev`, `pilot`, `val` or `test` result,
selects no capacity or threshold, freezes no config and makes no C1-versus-S statement.
Every path it binds is inside a `tmp_path` tree.
"""

from __future__ import annotations

import copy
import io
import json
import shutil
import sys
from contextlib import contextmanager
from dataclasses import asdict, fields as dataclass_fields, replace
from pathlib import Path
from typing import Any, Callable, Mapping, Sequence

import numpy as np
import pytest

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "scripts"))

from build_data_contract_fixture import build_fixture  # noqa: E402
from utils.config_contract import expected_config_hash, load_config  # noqa: E402
from utils import connection_adapter  # noqa: E402
from utils.connection_adapter import (  # noqa: E402
    AUDIT_NAMES,
    LABEL_FIELDS,
    MANIFEST_AUDIT_KEY,
    MANIFEST_CENSUS_FIELDS,
    MANIFEST_NAME,
    MAX_FIELD_PATH_INDEX_DIGITS,
    PLANT_FRAME_ARRAYS,
    ROLE_INDEX_NAME,
    SUITE_QUALIFIED_ROLES,
    ArmGeometry,
    ArmSeries,
    AuthenticatedCases,
    AuthenticatedConnection,
    AuthenticatedGeometry,
    CaseGeometry,
    authenticate_config,
    authenticate_connection,
    authenticate_dataset,
    authenticate_roles,
    authenticate_sources,
    bind_playback_timebase,
    canonical_text_digest,
    external_bytes_digest,
    external_digest,
    manifest_census,
    require_authority_config_policy,
    require_complete_arms,
    require_pair_agreement,
    require_tracking_window,
    resolve_cases,
    resolve_decisions,
    resolve_geometry,
    role_root_for,
    strict_json_document,
    tracked_text_digest,
    value_at_field_path,
)
from utils.coherent_geometry_fixture import (  # noqa: E402
    coherent_privileged_record,
    coherent_render_geometry,
    fixture_maximum_deviation_m,
    geometry_validation_document,
    render_geometry_document,
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
    CENTERLINE_TASK_OUTPUT_TOL_M,
    DEVELOPMENT_ONLY,
    FINAL,
    SUITE_KEYS,
    LabelFields,
    VerificationSceneError,
    X_ARMS_INCOMPLETE,
    X_CONNECTION_UNAUTHORIZED,
    X_DECISION_UNSUPPORTED,
    X_GEOMETRY_UNSUPPORTED,
    X_IDENTITY_MISMATCH,
    X_PAIR_MISMATCH,
    X_PROVENANCE_UNRESOLVED,
    X_ROLE_ABSENT,
    X_ROLE_UNAUTHORIZED,
    X_SPLIT_FORBIDDEN,
    X_TIMEBASE_MISMATCH,
    X_WINDOW_UNSUPPORTED,
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

#: The record's declared `analysis_window_s` for this fixture, in seconds. The
#: contract fixture runs 32 control steps at the draft config's 500 Hz, so its
#: playback grid spans 0.000 s to 0.062 s in 0.002 s samples and its label onset is
#: at 0.020 s. A window has to close on a control sample at or before the last one,
#: so the largest window this grid can close is **0.042 s**, which closes on the
#: last sample; 0.040 s is chosen instead, and the convention that owns the choice
#: is *the largest whole multiple of 0.01 s inside that bound*. Two reasons, both
#: about the fixture rather than about the metric: a window at exactly the grid's
#: maximum sits on a boundary, so any later change to `FIXTURE_N_STEPS` would turn
#: a passing fixture into a refusal for a reason that has nothing to do with the row
#: under test; and a round constant is one a reader can check against the grid in
#: their head. It closes on the sample at 0.060 s, one sample inside the end. It is
#: a *fixture* window and it manufactures no approved number: `analysis_window_s` is
#: shape-gated by the record contract and nothing in this lane selects an analysis
#: window. The frozen 5 s headline is what
#: `test_row17_refuses_a_window_this_grid_cannot_close` drives, because this grid
#: cannot close it.
ANALYSIS_WINDOW_S = 0.04


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
            "analysis_window_s": ANALYSIS_WINDOW_S,
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
    dataset = authenticate_dataset(record_value, bound, sources, config)
    roles = authenticate_roles(record_value, bound, config, dataset)
    whole = harness.authenticate()
    assert whole.config.config_sha256 == config.config_sha256
    assert whole.sources.established_cases == sources.established_cases
    assert _plain(whole.dataset.census) == _plain(dataset.census)
    assert set(whole.roles.payloads) == set(roles.payloads)


# --------------------------------------------------------------------------- #
# The Round-1 findings, each driven at the state it named.
#
# Every test below builds the input the finding described and drives the chain
# against it. Where a repair makes a previously accepted state refuse, the test
# drives the refusal; where a repair makes the chain *ignore* something it used to
# be steered by -- a file that changes after it was authenticated -- the test drives
# the acceptance and pins the interpreted value, with a counterfactual beside it
# showing the same bytes are detected when they are present before the read. An
# acceptance test with no counterfactual would pass on a module that stopped
# checking.
# --------------------------------------------------------------------------- #
def _seam_swap(
    monkeypatch: pytest.MonkeyPatch,
    attribute: str,
    path: Path,
    replacement: bytes,
    *,
    when: Callable[[tuple[Any, ...]], bool] | None = None,
    after: bool = False,
) -> dict[str, Any]:
    """Make one adapter seam overwrite `path` the first time it is called.

    This is how a swap between authenticating a file and interpreting it is driven
    deterministically: the seam is the module's own reference to whatever reopens the
    path, so the write lands at one exact point in the chain with no timing involved.
    `after=True` puts the write *after* the seam returns, which is the only way to
    separate a digest taken over bytes already in hand from a digest taken over a
    second read of the same path -- a swap that fires before both is invisible to the
    difference. The original bytes are restored by the fixture that requests this
    helper, because the harness tree is session-scoped and a leaked mutation would
    silently retarget every later test.
    """

    real = getattr(connection_adapter, attribute)
    state: dict[str, Any] = {"fired": False, "original": path.read_bytes()}

    def wrapper(*args: Any, **kwargs: Any) -> Any:
        if state["fired"] or (when is not None and not when(args)):
            return real(*args, **kwargs)
        state["fired"] = True
        if after:
            result = real(*args, **kwargs)
            path.write_bytes(replacement)
            return result
        path.write_bytes(replacement)
        return real(*args, **kwargs)

    monkeypatch.setattr(connection_adapter, attribute, wrapper)
    return state


@pytest.fixture()
def restore_bytes():
    """Put back every file a swap test edited, whatever the test did."""

    saved: list[tuple[Path, bytes]] = []

    def remember(path: Path) -> Path:
        saved.append((Path(path), Path(path).read_bytes()))
        return Path(path)

    yield remember
    for path, original in reversed(saved):
        path.write_bytes(original)


# -- finding 1: the bytes interpreted are the bytes authenticated ------------- #
def test_finding1_a_source_artifact_swapped_at_parse_time_does_not_change_the_facts(
    harness: Harness, monkeypatch: pytest.MonkeyPatch, restore_bytes
) -> None:
    """Step 5 parses the bytes it digested, not what the path names afterwards."""

    path = restore_bytes(harness.packet_root / RESULT_RELATIVE)
    replacement = json.dumps(
        {
            "read": {"cases": ["some-other-case"], "config_hash": "dev-" + "e" * 64,
                     "split": "val"},
            "status": "a document nobody authenticated",
        },
        indent=2,
        sort_keys=True,
    ).encode("utf-8") + b"\n"
    state = _seam_swap(
        monkeypatch,
        "strict_json_document",
        path,
        replacement,
        when=lambda args: len(args) > 1 and args[1] == "established_result",
    )

    result = harness.authenticate()

    assert state["fired"]
    assert path.read_bytes() == replacement
    assert result.sources.established_cases == (CASE_ID,)
    assert _plain(result.sources.documents["established_result"])["read"]["split"] == SPLIT


def test_finding1_the_same_swapped_source_refuses_when_it_is_there_before_the_read(
    harness: Harness, restore_bytes
) -> None:
    """The counterfactual: those bytes are detected, so the acceptance above means something."""

    path = restore_bytes(harness.packet_root / RESULT_RELATIVE)
    path.write_bytes(
        json.dumps({"read": {"cases": ["x"], "config_hash": "dev-" + "e" * 64,
                             "split": "val"}}, indent=2, sort_keys=True).encode("utf-8")
    )
    error = _refusal(harness.authenticate)
    assert error.code == X_IDENTITY_MISMATCH
    assert "established_result.sha256" in str(error)


def test_finding1_a_source_artifact_swapped_before_it_is_digested_is_still_one_read(
    harness: Harness, monkeypatch: pytest.MonkeyPatch, restore_bytes
) -> None:
    """The digest is taken over the bytes in hand, not over a second open.

    This is the other half of the boundary from the parse-time swap below it. There
    the file changed after it was digested; here it changes the instant the read
    returns, so a chain that reopened the path to hash it would refuse a file it had
    already read correctly. The acceptance is the assertion: one read served both.
    """

    path = restore_bytes(harness.packet_root / RESULT_RELATIVE)
    replacement = json.dumps(
        {"read": {"cases": ["x"], "config_hash": "dev-" + "e" * 64, "split": "val"}},
        indent=2,
        sort_keys=True,
    ).encode("utf-8")
    state = _seam_swap(
        monkeypatch,
        "_read_bytes",
        path,
        replacement,
        when=lambda args: bool(args) and Path(args[0]) == path,
        after=True,
    )

    result = harness.authenticate()

    assert state["fired"]
    assert path.read_bytes() == replacement
    assert result.sources.established_cases == (CASE_ID,)


def test_finding1_an_audit_swapped_before_it_is_digested_is_still_one_read(
    harness: Harness, monkeypatch: pytest.MonkeyPatch, restore_bytes
) -> None:
    """The same property in the raw domain, where the audits are digested."""

    path = restore_bytes(harness.role_root / "generation_audit.json")
    original = path.read_bytes()
    replacement = original.replace(b"manifest_matches", b"manifest_mismatched", 1)
    assert replacement != original
    state = _seam_swap(
        monkeypatch,
        "_read_bytes",
        path,
        replacement,
        when=lambda args: bool(args) and Path(args[0]) == path,
        after=True,
    )

    result = harness.authenticate()

    assert state["fired"]
    assert path.read_bytes() == replacement
    assert set(result.dataset.audits) == set(AUDIT_NAMES)


def test_finding4_a_boolean_capacity_is_not_the_integer_one(harness: Harness) -> None:
    """`True == 1`, so the rung a record declares as 1 is not satisfied by `true`."""

    document = {"selected": {"rung": True, "width": SELECTED_WIDTH}}
    with _with_source(harness, SELECTION_RELATIVE, document) as digest:
        edited = copy.deepcopy(harness.document)
        edited["model_selection"]["source"]["sha256"] = digest
        edited["model_selection"]["rung"] = 1
        error = _drive(harness, edited)
    assert error.code == X_IDENTITY_MISMATCH
    assert "which is not a number" in str(error)


def test_finding1_a_config_swapped_before_it_is_parsed_is_still_one_read(
    harness: Harness, monkeypatch: pytest.MonkeyPatch, restore_bytes
) -> None:
    """Step 4 parses the config bytes it read, not a second read of the same path.

    The replacement is a different valid JSON object whose `config_hash` no longer
    describes its own values, so a chain that reparsed the path would refuse. The
    acceptance, with the authenticated hash carried out, is the assertion.

    There is deliberately no companion test on the *schema* side, and the reason is
    the same proof that removed the post-validation bracket: any schema change between
    this module's read and the contract's own read changes the schema's raw digest and
    refuses inside `validate_config_document`, so no input can distinguish a schema
    parsed from bytes in hand from one parsed from a second read.
    """

    path = restore_bytes(harness.packet_root / CONFIG_RELATIVE)
    document = json.loads(path.read_text(encoding="utf-8"))
    document["values"] = {**document["values"], "an_unapproved_key": 1}
    state = _seam_swap(
        monkeypatch,
        "_read_bytes",
        path,
        json.dumps(document, indent=2, sort_keys=True).encode("utf-8"),
        when=lambda args: bool(args) and Path(args[0]) == path,
        after=True,
    )

    result = harness.authenticate()

    assert state["fired"]
    assert result.config.config.config_hash == harness.config_hash
    assert "an_unapproved_key" not in _plain(result.config.config.document)["values"]


def test_finding1_a_config_swapped_at_validation_time_does_not_change_the_config(
    harness: Harness, monkeypatch: pytest.MonkeyPatch, restore_bytes
) -> None:
    """Step 4 validates the document it digested, not the file the contract reopens.

    The replacement is a config whose `config_hash` no longer matches its own values,
    so a chain that validated whatever the path named on the second read would refuse.
    """

    path = restore_bytes(harness.packet_root / CONFIG_RELATIVE)
    document = json.loads(path.read_text(encoding="utf-8"))
    document["values"] = {**document["values"], "an_unapproved_key": 1}
    state = _seam_swap(
        monkeypatch,
        "validate_config_document",
        path,
        json.dumps(document, indent=2, sort_keys=True).encode("utf-8"),
    )

    result = harness.authenticate()

    assert state["fired"]
    assert result.config.config.config_hash == harness.config_hash
    assert "an_unapproved_key" not in _plain(result.config.config.document)["values"]


def _read_once_seam(
    monkeypatch: pytest.MonkeyPatch,
    path: Path,
    replacement: bytes,
    *,
    after: bool = True,
) -> dict[str, Any]:
    """Overwrite `path` around the one read the chain makes of it.

    `_read_bytes` is the module's single named read, so patching it puts the write at
    the exact instant the chain has the bytes of that file in hand and will never open
    it again. With `after=True` the replacement lands *after* that read returns and is
    **left in place**, which is the state a bracket around a path-based parser could
    detect and the state a re-open would silently interpret. The chain must accept and
    must hand back the value it authenticated; the swap must change nothing.

    With `after=False` the write lands before the read, so the read returns the
    replacement -- and the digest must refuse it. The two directions together are what
    say the read moved rather than that the check was dropped.
    """

    real = connection_adapter._read_bytes
    state: dict[str, Any] = {"fired": False, "original": path.read_bytes()}

    def wrapper(target: Path, **kwargs: Any) -> bytes:
        if state["fired"] or Path(target) != path:
            return real(target, **kwargs)
        state["fired"] = True
        if after:
            raw = real(target, **kwargs)
            path.write_bytes(replacement)
            return raw
        path.write_bytes(replacement)
        return real(target, **kwargs)

    monkeypatch.setattr(connection_adapter, "_read_bytes", wrapper)
    return state


def _alternate_plant_payload(path: Path) -> bytes:
    """Return a different, schema-valid plant payload for the same run.

    Only `q_true` moves, and it moves by a value no rounding could produce, so a chain
    that interpreted these bytes rather than the authenticated ones is caught by an
    exact comparison rather than by a tolerance.
    """

    import numpy as np

    with np.load(path, allow_pickle=False) as archive:
        arrays = {name: np.array(archive[name]) for name in archive.files}
    arrays["q_true"] = arrays["q_true"] + 1.0
    buffer = io.BytesIO()
    np.savez(buffer, **arrays)
    return buffer.getvalue()


def test_finding1_a_manifest_replaced_after_its_one_read_changes_nothing(
    harness: Harness, monkeypatch: pytest.MonkeyPatch, restore_bytes
) -> None:
    """Row 6 parses the bytes it digested, so a later replacement is not read at all.

    The replacement renames a run the record names, so a chain that re-opened
    `manifest.csv` would either refuse or plan from a row the record never approved.
    The replacement is still on disk when the chain accepts -- this is the persistent
    state, not a swap-and-revert -- and the census and rows are the authenticated ones.
    """

    path = restore_bytes(harness.role_root / MANIFEST_NAME)
    text = path.read_text(encoding="utf-8")
    replacement = text.replace("fixture_dev_C1", "fixture_dev_C9", 1).encode("utf-8")
    assert replacement != path.read_bytes()
    state = _read_once_seam(monkeypatch, path, replacement)

    result = harness.authenticate()

    assert state["fired"]
    assert path.read_bytes() == replacement
    assert "fixture_dev_C1" in result.dataset.rows
    assert "fixture_dev_C9" not in result.dataset.rows


def test_finding1_a_manifest_replaced_before_its_one_read_refuses(
    harness: Harness, monkeypatch: pytest.MonkeyPatch, restore_bytes
) -> None:
    """The digest still guards row 6: bytes that reach the parse must authenticate."""

    path = restore_bytes(harness.role_root / MANIFEST_NAME)
    text = path.read_text(encoding="utf-8")
    replacement = text.replace("fixture_dev_C1", "fixture_dev_C9", 1).encode("utf-8")
    state = _read_once_seam(monkeypatch, path, replacement, after=False)

    error = _refusal(harness.authenticate)

    assert state["fired"]
    assert error.code == X_IDENTITY_MISMATCH
    assert "data_root.manifest_sha256" in str(error)


def test_finding1_a_role_index_replaced_after_its_one_read_changes_nothing(
    harness: Harness, monkeypatch: pytest.MonkeyPatch, restore_bytes
) -> None:
    """Rows 9 and 12 both plan from the index bytes row 8 digested.

    The replacement changes the payload digest an index row records. A chain that
    re-opened the index anywhere -- at the parse, or inside `RolePayloadLoader` --
    would compare a payload against a digest the record never approved.
    """

    path = restore_bytes(harness.role_root / "plant" / ROLE_INDEX_NAME)
    text = path.read_text(encoding="utf-8")
    original_sha = external_digest(harness.role_root / "plant" / "fixture_dev_C1.npz")
    replacement = text.replace(original_sha, "0" + original_sha[1:], 1).encode("utf-8")
    assert replacement != path.read_bytes()
    state = _read_once_seam(monkeypatch, path, replacement)

    result = harness.authenticate()

    assert state["fired"]
    assert path.read_bytes() == replacement
    assert result.roles.index_rows[(CASE_ID, "C1", "plant")].sha256 == original_sha


def test_finding1_a_role_index_replaced_before_its_one_read_refuses(
    harness: Harness, monkeypatch: pytest.MonkeyPatch, restore_bytes
) -> None:
    """The digest still guards row 8."""

    path = restore_bytes(harness.role_root / "plant" / ROLE_INDEX_NAME)
    text = path.read_text(encoding="utf-8")
    original_sha = external_digest(harness.role_root / "plant" / "fixture_dev_C1.npz")
    replacement = text.replace(original_sha, "0" + original_sha[1:], 1).encode("utf-8")
    state = _read_once_seam(monkeypatch, path, replacement, after=False)

    error = _refusal(harness.authenticate)

    assert state["fired"]
    assert error.code == X_IDENTITY_MISMATCH
    assert "index_sha256" in str(error)


def test_finding1_a_payload_replaced_after_its_one_read_changes_nothing(
    harness: Harness, monkeypatch: pytest.MonkeyPatch, restore_bytes
) -> None:
    """Row 12 interprets the payload bytes row 11 digested, not a second open.

    This is the exact state the Round-2 candidate accepted: the payload file is
    replaced with a different schema-valid archive immediately after its digest is
    taken, and the replacement is **left present**. The chain must accept -- nothing
    it authenticated has changed -- and every array it returns must be the original's.
    """

    import numpy as np

    path = restore_bytes(harness.role_root / "plant" / "fixture_dev_C1.npz")
    with np.load(path, allow_pickle=False) as archive:
        original_q_true = np.array(archive["q_true"])
    replacement = _alternate_plant_payload(path)
    assert replacement != path.read_bytes()
    state = _read_once_seam(monkeypatch, path, replacement)

    result = harness.authenticate()

    assert state["fired"]
    assert path.read_bytes() == replacement
    returned = result.roles.payloads[(CASE_ID, "C1", "plant")]["q_true"]
    assert np.array_equal(returned, original_q_true)
    assert not np.array_equal(returned, original_q_true + 1.0)


def test_finding1_a_payload_replaced_before_its_one_read_refuses(
    harness: Harness, monkeypatch: pytest.MonkeyPatch, restore_bytes
) -> None:
    """The digest still guards row 11."""

    path = restore_bytes(harness.role_root / "plant" / "fixture_dev_C1.npz")
    replacement = _alternate_plant_payload(path)
    state = _read_once_seam(monkeypatch, path, replacement, after=False)

    error = _refusal(harness.authenticate)

    assert state["fired"]
    assert error.code == X_IDENTITY_MISMATCH
    assert "payload_sha256" in str(error)


def _open_counts(harness: Harness) -> dict[Path, int]:
    """Return how many times the chain reads each file, keyed by resolved path.

    Every file access anywhere in this chain -- `_read_bytes`, `canonical_text_sha256`,
    `storage_contract.file_sha256`, `config_contract.file_sha256` and the record's own
    load -- goes through `Path.read_bytes`, so counting calls per resolved path measures
    the whole chain rather than one row at a time.
    """

    counts: dict[Path, int] = {}
    real = Path.read_bytes

    def counting(self: Path) -> bytes:
        resolved = self.resolve()
        counts[resolved] = counts.get(resolved, 0) + 1
        return real(self)

    with pytest.MonkeyPatch.context() as patch:
        patch.setattr(Path, "read_bytes", counting)
        result = harness.authenticate()
    assert result.record.record_label == RECORD_LABEL
    return counts


def test_finding1_the_chain_reads_every_file_it_interprets_exactly_once(
    harness: Harness,
) -> None:
    """The whole property, stated once: nothing the chain interprets is opened twice.

    A swap-and-revert hides in the interval between two reads of one name. A bracket
    around the second read narrows that interval; only *removing* the second read closes
    it. This is the measurement no per-row test can make -- each row can only say that
    it read once -- and it is the one that fails if any future row reintroduces a
    hash-then-reopen anywhere in rows 1 through 12.

    **One file is read twice and the count is pinned at two rather than excused.**
    `config_contract.validate_config_document` takes the schema as a *document* but
    re-derives the schema's raw digest from `schema_path` itself, to compare against the
    configuration's declared `schema_sha256`. That read belongs to a closed utility this
    card's accepted scope does not reach, and closing it needs a `schema_sha256`
    parameter on that contract rather than anything the adapter can do. What the window
    can and cannot do is measured rather than assumed, in the two tests below. Pinning
    the number here is what makes a *new* second read anywhere else fail this test
    instead of hiding inside an allowance.
    """

    counts = _open_counts(harness)
    schema = (harness.packet_root / SCHEMA_RELATIVE).resolve()

    assert counts[schema] == 2
    twice = {str(path) for path, count in counts.items() if count != 1}
    assert twice == {str(schema)}
    for expected in (
        harness.record_path,
        harness.packet_root / CONFIG_RELATIVE,
        harness.packet_root / RESULT_RELATIVE,
        harness.packet_root / CALIBRATION_RELATIVE,
        harness.packet_root / GEOMETRY_RELATIVE,
        harness.packet_root / PRODUCER_RELATIVE,
        harness.role_root / MANIFEST_NAME,
        harness.role_root / "generation_audit.json",
        harness.role_root / "plant" / ROLE_INDEX_NAME,
        harness.role_root / "plant" / "fixture_dev_C1.npz",
        harness.checkpoint_root / PAIR_ID / "C1.pt",
    ):
        assert counts[expected.resolve()] == 1


def test_finding1_one_file_named_by_two_threshold_references_is_read_once(
    harness: Harness,
) -> None:
    """Both thresholds name one artifact, and one artifact is one read.

    This is the second-read the open count found: each reference authenticated the file
    for itself, so two declarations were checked against two objects that happened to
    carry one name. That is not a statement that the two declarations agree with each
    other, which is the whole point of declaring both.
    """

    sources = harness.document["thresholds"]["sources"]
    assert (
        sources["abstain_threshold"]["artifact_relative_path"]
        == sources["unknown_threshold"]["artifact_relative_path"]
    )
    counts = _open_counts(harness)
    assert counts[(harness.packet_root / CALIBRATION_RELATIVE).resolve()] == 1


def test_finding1_two_disagreeing_digests_for_one_artifact_still_refuse(
    harness: Harness,
) -> None:
    """Reading once must not become believing the first declaration.

    The single read is only safe if every declaration is compared against that one
    measurement. A record that declares one digest for the abstain source and a
    different one for the unknown source names the same file twice and contradicts
    itself, and the second comparison is what catches it.
    """

    document = copy.deepcopy(dict(harness.document))
    sources = document["thresholds"]["sources"]
    truthful = sources["abstain_threshold"]["sha256"]
    sources["unknown_threshold"]["sha256"] = "0" + truthful[1:]

    error = _refusal(lambda: authenticate_connection(**harness.rewrite_record(document)))

    assert error.code == X_IDENTITY_MISMATCH
    assert "thresholds.sources.unknown_threshold.sha256" in str(error)


def test_finding1_a_schema_replaced_after_the_adapter_read_refuses(
    harness: Harness, monkeypatch: pytest.MonkeyPatch, restore_bytes
) -> None:
    """The schema's second read is guarded, and this measures by what.

    The adapter reads the schema once and interprets *those* bytes; the config contract
    then re-derives the schema's raw digest from the path. A replacement left in place
    after the adapter's read therefore reaches the contract, whose comparison against
    the configuration's declared `schema_sha256` refuses it. So the window cannot admit
    arbitrary bytes -- which is the half that is closed, and the half the disclosure in
    the module docstring rests on.
    """

    path = restore_bytes(harness.packet_root / SCHEMA_RELATIVE)
    replacement = path.read_bytes() + b"\n"
    state = _read_once_seam(monkeypatch, path, replacement)

    error = _refusal(harness.authenticate)

    assert state["fired"]
    assert path.read_bytes() == replacement
    assert error.code == X_PROVENANCE_UNRESOLVED
    assert "schema_sha256" in str(error)


def test_finding1_the_adapter_interprets_its_own_schema_read(
    harness: Harness, monkeypatch: pytest.MonkeyPatch, restore_bytes
) -> None:
    """What the schema window can reach: the contract's digest, never the adapter's rules.

    Every structural rule applied to the configuration comes from the document the
    adapter parsed out of the bytes it authenticated -- `validate_config_document`
    receives that document and re-opens the path only to hash it. So a schema swapped
    after the adapter's read cannot change which rules ran, and the adapter-side
    `schema_sha256` comparison prevents the second read from making a different schema
    declaration agree with those already-selected rules. This test fixes that boundary
    so a later reader does not have to re-derive it, and so a change that widened the
    window would fail here rather than pass quietly.
    """

    path = restore_bytes(harness.packet_root / SCHEMA_RELATIVE)
    permissive = json.loads(path.read_text(encoding="utf-8"))
    permissive["config_contract"] = {
        **permissive["config_contract"],
        "required_top_level": ["status"],
    }
    replacement = json.dumps(permissive, indent=2, sort_keys=True).encode("utf-8")
    state = _read_once_seam(monkeypatch, path, replacement)

    error = _refusal(harness.authenticate)

    assert state["fired"]
    assert error.code == X_PROVENANCE_UNRESOLVED
    assert "schema_sha256" in str(error)


def test_finding1_the_config_schema_digest_is_checked_against_the_authenticated_schema(
    harness: Harness, monkeypatch: pytest.MonkeyPatch, restore_bytes
) -> None:
    """A schema split cannot be hidden inside the contract's second schema read.

    The record authenticates schema A and the adapter interprets schema A. The config
    declares schema B, and the schema path is swapped from A to B after the adapter's
    read but before `validate_config_document` reopens the path for its raw digest
    comparison. Without an adapter-side comparison between the config declaration and
    the authenticated schema bytes, the closed contract can accept a config whose
    declared schema is not the schema whose rules ran.
    """

    schema_path = restore_bytes(harness.packet_root / SCHEMA_RELATIVE)
    config_path = restore_bytes(harness.packet_root / CONFIG_RELATIVE)
    schema_a = json.loads(schema_path.read_text(encoding="utf-8"))
    schema_b = copy.deepcopy(schema_a)
    schema_b["config_contract"] = {
        **schema_b["config_contract"],
        "required_top_level": [
            *schema_b["config_contract"]["required_top_level"],
            "codex_session_143_missing_key",
        ],
    }
    schema_b_raw = (
        json.dumps(schema_b, indent=2, sort_keys=True, allow_nan=False) + "\n"
    ).encode("utf-8")

    config_document = json.loads(config_path.read_text(encoding="utf-8"))
    config_document["schema_sha256"] = external_bytes_digest(schema_b_raw)
    config_document["config_hash"] = expected_config_hash(config_document)
    _write_json(config_path, config_document)

    record_document = copy.deepcopy(dict(harness.document))
    record_document["config"]["sha256"] = tracked_text_digest(config_path)
    record_document["config"]["config_hash"] = config_document["config_hash"]
    arguments = harness.rewrite_record(record_document)
    record = load_connection_record(
        arguments["connection_record_path"], arguments["connection_record_sha256"]
    )
    bound = bind_root_domains(
        record,
        packet_root=arguments["packet_root"],
        connection_record_path=arguments["connection_record_path"],
        config_path=arguments["config_path"],
        role_root=arguments["role_root"],
        checkpoint_root=arguments["checkpoint_root"],
        output_dir=arguments["output_dir"],
    )
    state = _read_once_seam(monkeypatch, schema_path, schema_b_raw)

    error = _refusal(lambda: authenticate_config(record, bound))

    assert state["fired"]
    assert schema_path.read_bytes() == schema_b_raw
    assert error.code == X_PROVENANCE_UNRESOLVED
    assert "schema_sha256" in str(error)


# -- finding 2: nothing the chain returns can be edited ---------------------- #
def test_finding2_the_accepted_config_document_is_read_only_below_its_dataclass(
    harness: Harness,
) -> None:
    """`@dataclass(frozen=True)` rebinds the attribute; the mapping is frozen here."""

    result = harness.authenticate()
    with pytest.raises(TypeError):
        result.config.config.document["status"] = "frozen"  # type: ignore[index]
    with pytest.raises(TypeError):
        result.config.config.document["values"]["plant"]["n_def"] = 0  # type: ignore[index]


def test_finding2_the_accepted_payload_arrays_cannot_be_written_to(
    harness: Harness,
) -> None:
    """A payload array is a fact, and a fact that can be edited is not one.

    Both halves matter: the assignment refuses, and the flag cannot be set back --
    an array that owns its buffer would allow exactly that, which is why the payload
    is rebuilt over an immutable one.
    """

    import numpy as np

    result = harness.authenticate()
    array = result.roles.payloads[(CASE_ID, "C1", "plant")]["q_true"]
    with pytest.raises(ValueError):
        array[...] = 0
    with pytest.raises(ValueError):
        array.flags.writeable = True
    with np.load(
        harness.role_root / "plant" / "fixture_dev_C1.npz", allow_pickle=False
    ) as archive:
        assert np.array_equal(array, archive["q_true"])
        assert array.dtype == archive["q_true"].dtype
        assert array.shape == archive["q_true"].shape


@pytest.mark.parametrize(
    "builder",
    [
        lambda np_: np_.zeros(0),
        lambda np_: np_.array(3.5),
        lambda np_: np_.array(["ab", "cde"]),
        lambda np_: np_.zeros((2, 3)),
        lambda np_: np_.arange(6).reshape(3, 2)[::2],
        lambda np_: np_.array([], dtype="<U3"),
    ],
    ids=["empty", "zero-dimensional", "text", "matrix", "non-contiguous-view", "empty-text"],
)
def test_finding2_freezing_a_payload_array_changes_nothing_about_it(builder) -> None:
    """A freeze that alters dtype, shape or values has replaced the fact it protects.

    The zero-dimensional case is here because it is the one this repair got wrong
    first: `np.ascontiguousarray` is documented to return at least one dimension, so a
    scalar payload field came back as a one-element vector -- after the loader had
    validated its shape against the schema.
    """

    import numpy as np

    original = builder(np)
    frozen = connection_adapter._read_only_array(original)
    assert frozen.dtype == original.dtype
    assert frozen.shape == original.shape
    assert np.array_equal(frozen, original)
    assert not frozen.flags.writeable
    with pytest.raises(ValueError):
        frozen.flags.writeable = True


# -- finding 3: the dataset's configuration is joined to the authenticated one - #
def _reconfigured(
    harness: Harness,
    tmp_path: Path,
    *,
    move_manifest: bool,
    move_audits: bool,
) -> dict[str, Any]:
    """Copy the role tree onto a second, internally consistent config hash.

    Every digest and every record echo is updated, so the tree and the record agree
    with each other about a configuration that is not the one step 4 validated. This
    is the state finding 3 named: each file authenticates, and the two halves of the
    sentence are about different experiments.
    """

    other_hash = "dev-" + "b" * 64
    role_root = tmp_path / DATASET_LABEL
    shutil.copytree(harness.role_root, role_root)
    manifest_path = role_root / MANIFEST_NAME
    if move_manifest:
        manifest_path.write_text(
            manifest_path.read_text(encoding="utf-8").replace(
                harness.config_hash, other_hash
            ),
            encoding="utf-8",
            newline="",
        )
    if move_audits:
        for name in AUDIT_NAMES:
            _write_json(
                role_root / f"{name}.json",
                _audit_document(
                    status=harness.audit_status[name],
                    assignment_hash=harness.assignment_hash,
                    config_hash=other_hash,
                    census=harness.census,
                ),
            )

    edited = copy.deepcopy(harness.document)
    edited["data_root"]["manifest_sha256"] = external_digest(manifest_path)
    for name in AUDIT_NAMES:
        echo = edited["data_root"][name]
        echo["sha256"] = external_digest(role_root / f"{name}.json")
        if move_audits:
            echo["config_hash"] = other_hash
    if move_manifest:
        for suite in ("C1", "S"):
            arm = edited["cases"][0]["arms"][suite]
            arm["manifest_row"] = {**arm["manifest_row"], "config_hash": other_hash}

    arguments = harness.rewrite_record(edited)
    arguments["role_root"] = role_root
    return arguments


@pytest.mark.parametrize(
    "move_manifest,move_audits",
    [(True, True), (True, False), (False, True)],
)
def test_finding3_a_dataset_on_another_config_refuses_however_consistent_it_is(
    harness: Harness, tmp_path: Path, move_manifest: bool, move_audits: bool
) -> None:
    """Row 6 joins both audit echoes and the manifest rows to the validated config."""

    arguments = _reconfigured(
        harness, tmp_path, move_manifest=move_manifest, move_audits=move_audits
    )
    error = _refusal(lambda: authenticate_connection(**arguments))
    assert error.code == X_IDENTITY_MISMATCH
    assert harness.config_hash in str(error)


# -- finding 4: exact, non-lossy numeric equality ---------------------------- #
@contextmanager
def _with_source(harness: Harness, relative: str, document: Mapping[str, Any]):
    """Write one source artifact, yield its canonical digest, and restore it after."""

    path = harness.packet_root / relative
    original = path.read_bytes()
    try:
        _write_json(path, document)
        yield tracked_text_digest(path)
    finally:
        path.write_bytes(original)


@pytest.mark.parametrize(
    "field,artifact_value,declared",
    [
        ("rung", 2 ** 53, 2 ** 53 + 1),
        ("width", 10 ** 100, 10 ** 100 + 1),
        ("rung", 10 ** 401, 2),
    ],
    ids=["binary64-collision", "unequal-101-digit-integers", "401-digit-overflow"],
)
def test_finding4_unequal_integers_refuse_rather_than_agreeing_or_crashing(
    harness: Harness, field: str, artifact_value: int, declared: int
) -> None:
    """Two integers binary64 cannot tell apart are two numbers, and the row says so.

    The third case is the one that used to leave the row with a raw `OverflowError`
    instead of the exit code section 4.1 assigns it.
    """

    selected = {"rung": SELECTED_RUNG, "width": SELECTED_WIDTH}
    selected[field] = artifact_value
    with _with_source(harness, SELECTION_RELATIVE, {"selected": selected}) as digest:
        edited = copy.deepcopy(harness.document)
        edited["model_selection"]["source"]["sha256"] = digest
        edited["model_selection"][field] = declared
        error = _drive(harness, edited)
    assert error.code == X_IDENTITY_MISMATCH
    assert f"model_selection.{field}" in str(error)


def test_finding4_a_measured_deviation_no_float_can_hold_refuses(
    harness: Harness,
) -> None:
    """The maximum-deviation path carried the same raw overflow and now refuses."""

    document = {
        "agreement": {
            "maximum_deviation_m": 10 ** 401,
            "tolerance_m": DISTAL_TOLERANCE_M,
        }
    }
    with _with_source(harness, GEOMETRY_RELATIVE, document) as digest:
        edited = copy.deepcopy(harness.document)
        edited["render_geometry"]["tolerance_source"]["sha256"] = digest
        error = _drive(harness, edited)
    assert error.code == X_IDENTITY_MISMATCH
    assert "exceeds the declared tolerance" in str(error)


def test_finding4_a_negative_measured_deviation_still_refuses(harness: Harness) -> None:
    """The magnitude rule survives the move off binary64 conversion."""

    document = {
        "agreement": {"maximum_deviation_m": -1, "tolerance_m": DISTAL_TOLERANCE_M}
    }
    with _with_source(harness, GEOMETRY_RELATIVE, document) as digest:
        edited = copy.deepcopy(harness.document)
        edited["render_geometry"]["tolerance_source"]["sha256"] = digest
        error = _drive(harness, edited)
    assert error.code == X_IDENTITY_MISMATCH
    assert "non-negative magnitude" in str(error)


# -- finding 5: a boolean is not a count ------------------------------------- #
_ONE_ROW_CENSUS: dict[str, Any] = {
    "manifest_rows": 1,
    "reservations": 1,
    "splits": {"dev": 1},
    "suites": ["C1"],
    "test_rows": 0,
    "train_seed": 1,
}


@pytest.mark.parametrize(
    "field,substitute",
    [
        ("manifest_rows", True),
        ("reservations", True),
        ("test_rows", False),
        ("train_seed", True),
    ],
)
def test_finding5_a_boolean_census_count_refuses(field: str, substitute: bool) -> None:
    """`True == 1` and `False == 0`, so the type is checked before the value is."""

    block = {**_ONE_ROW_CENSUS, field: substitute}
    error = _refusal(
        lambda: connection_adapter._require_census_agrees(
            "generation_audit", block, _ONE_ROW_CENSUS
        )
    )
    assert error.code == X_IDENTITY_MISMATCH
    assert "not a JSON integer count" in str(error)


def test_finding5_a_boolean_inside_the_split_counts_refuses() -> None:
    """The nested counts are checked too; one dict of them is still six numbers."""

    block = {**_ONE_ROW_CENSUS, "splits": {"dev": True}}
    error = _refusal(
        lambda: connection_adapter._require_census_agrees(
            "independent_audit", block, _ONE_ROW_CENSUS
        )
    )
    assert error.code == X_IDENTITY_MISMATCH
    assert "splits.dev" in str(error)


@pytest.mark.parametrize("field", ["test_rows", "train_seed"])
def test_finding5_a_boolean_census_count_refuses_end_to_end(
    harness: Harness, record: dict[str, Any], restore_bytes, field: str
) -> None:
    """Both fixture census fields that hold zero are driven through the whole chain."""

    assert harness.census[field] == 0
    path = restore_bytes(harness.role_root / "generation_audit.json")
    document = json.loads(path.read_text(encoding="utf-8"))
    document[MANIFEST_AUDIT_KEY][field] = False
    _write_json(path, document)
    record["data_root"]["generation_audit"]["sha256"] = external_digest(path)
    error = _drive(harness, record)
    assert error.code == X_IDENTITY_MISMATCH
    assert "not a JSON integer count" in str(error)


def test_finding5_the_census_the_manifest_produces_is_all_plain_integers(
    harness: Harness,
) -> None:
    """The recomputed side is what the type rule is stated against."""

    for field in ("manifest_rows", "reservations", "test_rows", "train_seed"):
        assert type(harness.census[field]) is int
    for count in harness.census["splits"].values():
        assert type(count) is int


# -- finding 6: an index segment is bounded and ASCII ------------------------ #
_INDEXABLE = {"a": [{"b": 1}]}


@pytest.mark.parametrize(
    "segment", ["0" * 5000, "0" * (MAX_FIELD_PATH_INDEX_DIGITS + 1)]
)
def test_finding6_an_over_long_index_segment_refuses_rather_than_raising(
    segment: str,
) -> None:
    """CPython refuses to convert a long integer string; this row refuses first."""

    error = _refusal(
        lambda: value_at_field_path(_INDEXABLE, f"a.{segment}", where="probe")
    )
    assert error.code == X_IDENTITY_MISMATCH
    assert "digits" in str(error)


def test_finding6_an_index_segment_at_the_bound_is_still_range_checked() -> None:
    """The length rule is not the range rule, and the longest legal one still refuses."""

    segment = "9" * MAX_FIELD_PATH_INDEX_DIGITS
    error = _refusal(
        lambda: value_at_field_path(_INDEXABLE, f"a.{segment}", where="probe")
    )
    assert error.code == X_IDENTITY_MISMATCH
    assert "that array holds 1 entries" in str(error)


@pytest.mark.parametrize(
    "segment",
    ["\u00b2", "\u0663"],
    ids=["superscript-two", "arabic-indic-three"],
)
def test_finding6_a_non_ascii_digit_is_a_key_and_not_an_index(segment: str) -> None:
    """`str.isdigit` is true of characters `int()` cannot convert, and of digits no
    JSON author wrote; both fall through to the ordinary absent-key refusal."""

    error = _refusal(
        lambda: value_at_field_path(_INDEXABLE, f"a.{segment}", where="probe")
    )
    assert error.code == X_IDENTITY_MISMATCH
    assert "is absent" in str(error)


def test_finding6_the_index_digit_bound_is_the_number_it_is_meant_to_be() -> None:
    """One place states the value, with the reason attached to it.

    The bound is the decimal length of `sys.maxsize`, which is the most entries any
    in-memory JSON array could have. It is pinned as a literal here because a test
    whose input is a function of the constant it exercises holds the relationship and
    not the value.
    """

    assert MAX_FIELD_PATH_INDEX_DIGITS == 19
    assert len(str(sys.maxsize)) == MAX_FIELD_PATH_INDEX_DIGITS


# -- the bytes-domain digests answer to the functions that own the rules ----- #
@pytest.mark.parametrize(
    "raw",
    [
        b'{"a": 1}\n',
        b'{"a": 1}\r\n',
        b'\xef\xbb\xbf{"a": 1}\n',
        b'\xef\xbb\xbf{"a": 1}\r\n',
        b"",
        b"\r\n\r\n",
        b"binary\x00\xff\xfe bytes",
    ],
)
def test_the_two_digest_domains_agree_with_the_functions_that_own_them(
    tmp_path: Path, raw: bytes
) -> None:
    """A bytes-domain digest is a copy of a rule unless something holds it to the rule.

    The path-domain functions are the owners; these two exist only so that one read
    can serve both the digest and the parse. Equality against the owner is measured
    on every run rather than assumed from the two bodies looking alike.
    """

    from utils.protocol_p import canonical_text_sha256
    from utils.storage_contract import file_sha256

    path = tmp_path / "probe.bin"
    path.write_bytes(raw)
    assert canonical_text_digest(raw) == canonical_text_sha256(path)
    assert external_bytes_digest(raw) == file_sha256(path)


# --------------------------------------------------------------------------- #
# Read-order rows 13-17 -- the cross-arm and cross-role facts.
#
# Two kinds of test live below and the difference between them is deliberate.
#
# *Production-path* tests drive `authenticate_connection` over real bytes and then
# `resolve_cases`, so what they exercise is the whole chain. They are the ones that
# prove a row is reachable from the outside.
#
# *Seam* tests call one row's function directly with a value the production path is
# designed never to produce -- a loaded set with a payload missing, an arm whose
# labels disagree. That is the in-memory validator seam finding DD's repair
# introduced, and it is the only instrument that can drive a post-condition. A file
# holding only seam tests would prove nothing about the adapter, which is why every
# row that *can* be reached end to end has at least one test that reaches it that
# way: row 14 through a rewritten labels payload, row 15 through a rewritten
# controller payload, row 17 through the record's own declared window.
# --------------------------------------------------------------------------- #
def _resolve(arguments: Mapping[str, Any]) -> AuthenticatedCases:
    """Drive rows 1 through 17 end to end."""

    return resolve_cases(authenticate_connection(**arguments))


def _payload_key(case_id: str, suite: str, role: str) -> tuple[str, str, str]:
    """Return one loaded-payload key."""

    return (case_id, suite, role)


def _edited(payload: Mapping[str, np.ndarray], **changes: np.ndarray) -> dict:
    """Return a mutable copy of one loaded payload with some arrays replaced."""

    edited = dict(payload)
    edited.update(changes)
    return edited


def _with_payload(
    connection: AuthenticatedConnection,
    key: tuple[str, str, str],
    payload: Mapping[str, np.ndarray],
) -> AuthenticatedConnection:
    """Return the same connection with exactly one loaded payload replaced."""

    payloads = dict(connection.roles.payloads)
    payloads[key] = payload
    return replace(connection, roles=replace(connection.roles, payloads=payloads))


def _reindex(index_path: Path, run_id: str, digest: str) -> None:
    """Rewrite one role index row's `sha256` in place, preserving every other byte."""

    text = index_path.read_text(encoding="utf-8")
    lines = text.splitlines(keepends=True)
    columns = lines[0].rstrip("\r\n").split(",")
    digest_column = columns.index("sha256")
    rewritten = [lines[0]]
    for line in lines[1:]:
        body = line.rstrip("\r\n")
        terminator = line[len(body):]
        fields = body.split(",")
        if fields[0] == run_id:
            fields[digest_column] = digest
            line = ",".join(fields) + terminator
        rewritten.append(line)
    index_path.write_text("".join(rewritten), encoding="utf-8", newline="")


@contextmanager
def _rewritten_payload(
    harness: Harness,
    role: str,
    suite: str,
    run_id: str,
    payload: Mapping[str, np.ndarray],
):
    """Rewrite one payload on disk, re-index it, reinstall the record, then restore.

    This is what makes a row-14 or row-15 refusal a statement about the *production*
    path rather than about a value handed straight to one function. Rewriting a
    payload moves three identities -- the payload digest, its index row and the
    record's echo of both -- and all three are regenerated here from the files
    themselves, so the chain still authenticates and the refusal comes from the row
    under test rather than from step 8 or step 11.
    """

    directory = role_root_for(harness.role_root, role, suite)
    payload_path = directory / f"{run_id}.npz"
    index_path = directory / ROLE_INDEX_NAME
    saved_payload = payload_path.read_bytes()
    saved_index = index_path.read_bytes()
    try:
        buffer = io.BytesIO()
        np.savez(buffer, **{name: np.asarray(value) for name, value in payload.items()})
        payload_path.write_bytes(buffer.getvalue())
        _reindex(index_path, run_id, external_digest(payload_path))
        yield harness.rewrite_record(harness._record_document())
    finally:
        payload_path.write_bytes(saved_payload)
        index_path.write_bytes(saved_index)


# -- the accept side, which is what makes every refusal below mean something --- #
def test_rows13_to_17_accept_the_complete_fixture(harness: Harness) -> None:
    """The whole chain, rows 1 through 17, over the contract fixture."""

    cases = _resolve(harness.arguments())
    assert isinstance(cases, AuthenticatedCases)
    assert len(cases.cases) == 1
    case = cases.cases[0]
    assert case.case_id == CASE_ID
    assert case.pair_id == PAIR_ID
    assert case.display_label == "Fixture development pair"
    assert tuple(sorted(case.arms)) == tuple(sorted(SUITE_KEYS))
    assert case.window_s == ANALYSIS_WINDOW_S
    for suite in SUITE_KEYS:
        arm = case.arms[suite]
        assert isinstance(arm, ArmSeries)
        assert arm.suite == suite
        assert arm.run_id == f"{PAIR_ID}_{suite}"


def test_the_resolved_series_are_the_authenticated_arrays_themselves(
    harness: Harness,
) -> None:
    """No copy is taken, so nothing downstream can edit an authenticated fact."""

    connection = harness.authenticate()
    cases = resolve_cases(connection)
    case = cases.cases[0]
    for suite in SUITE_KEYS:
        plant = connection.roles.payloads[_payload_key(CASE_ID, suite, "plant")]
        controller = connection.roles.payloads[
            _payload_key(CASE_ID, suite, "controller_logs")
        ]
        arm = case.arms[suite]
        assert arm.q_true is plant["q_true"]
        assert arm.deform_coords is plant["deform_coords"]
        assert arm.task_reference is plant["task_reference"]
        assert arm.true_task_output is plant["true_task_output"]
        assert arm.controller_step is controller["step"]
        assert arm.controller_t_s is controller["t_s"]
        for array in (arm.q_true, arm.deform_coords, arm.controller_step):
            assert array.flags.writeable is False


def test_the_resolved_playback_grid_is_the_plants_own_grid(harness: Harness) -> None:
    """The scene's one clock is `plant.t_s`, not a grid this module reconstructed."""

    connection = harness.authenticate()
    case = resolve_cases(connection).cases[0]
    for suite in SUITE_KEYS:
        plant = connection.roles.payloads[_payload_key(CASE_ID, suite, "plant")]
        assert np.array_equal(case.playback_t_s, plant["t_s"])
    assert case.playback_t_s.shape == (FIXTURE_N_STEPS,)


def test_the_resolved_truth_is_the_labels_payload_field_by_field(
    harness: Harness,
) -> None:
    """The agreed body change is read out of the payload, not out of the record."""

    connection = harness.authenticate()
    case = resolve_cases(connection).cases[0]
    labels = connection.roles.payloads[_payload_key(CASE_ID, "C1", "labels")]
    assert isinstance(case.truth, LabelFields)
    for name in LABEL_FIELDS:
        assert getattr(case.truth, name) == np.asarray(labels[name]).item()


def test_the_resolved_decisions_are_live_schema_d_values(harness: Harness) -> None:
    """Decisions are `utils.estimator.EstimatorOutput`s, not a local mirror."""

    from utils.estimator import EstimatorOutput

    connection = harness.authenticate()
    case = resolve_cases(connection).cases[0]
    for suite in SUITE_KEYS:
        payload = connection.roles.payloads[
            _payload_key(CASE_ID, suite, "estimator_outputs")
        ]
        decisions = case.arms[suite].decisions
        assert len(decisions) == int(np.asarray(payload["step"]).shape[0])
        for index, decision in enumerate(decisions):
            assert isinstance(decision, EstimatorOutput)
            assert decision.step == int(payload["step"][index])
            assert decision.decision_time_s == float(payload["decision_time_s"][index])
            assert np.array_equal(decision.p_class, payload["p_class"][index])


def test_the_resolved_controller_mode_is_bound_to_the_step_grid(
    harness: Harness,
) -> None:
    """Every frame carries a non-empty mode string, as the surface will draw it."""

    case = _resolve(harness.arguments()).cases[0]
    for suite in SUITE_KEYS:
        arm = case.arms[suite]
        assert len(arm.controller_mode) == FIXTURE_N_STEPS
        assert all(isinstance(mode, str) and mode for mode in arm.controller_mode)


# -- row 13 ------------------------------------------------------------------ #
def test_row13_refuses_a_loaded_set_missing_one_payload(harness: Harness) -> None:
    """A named arm role that never arrived is an incomplete arm, not a silent gap."""

    connection = harness.authenticate()
    payloads = dict(connection.roles.payloads)
    del payloads[_payload_key(CASE_ID, "S", "plant")]
    deficient = replace(connection.roles, payloads=payloads)
    error = _refusal(lambda: require_complete_arms(connection.record, deficient))
    assert error.code == X_ARMS_INCOMPLETE
    assert "is missing" in str(error)
    assert "'S', 'plant'" in str(error)


def test_row13_refuses_a_loaded_set_carrying_a_payload_no_case_named(
    harness: Harness,
) -> None:
    """The comparison is two-directional; an unnamed extra is the allowlist failure."""

    connection = harness.authenticate()
    payloads = dict(connection.roles.payloads)
    payloads[("other-case", "C1", "plant")] = payloads[
        _payload_key(CASE_ID, "C1", "plant")
    ]
    widened = replace(connection.roles, payloads=payloads)
    error = _refusal(lambda: require_complete_arms(connection.record, widened))
    assert error.code == X_ARMS_INCOMPLETE
    assert "which the record did not name" in str(error)


def test_row13_refuses_a_missing_checkpoint(harness: Harness) -> None:
    """Both arms' checkpoints are part of what makes a case complete."""

    connection = harness.authenticate()
    checkpoints = dict(connection.roles.checkpoint_sha256)
    del checkpoints[(CASE_ID, "C1")]
    deficient = replace(connection.roles, checkpoint_sha256=checkpoints)
    error = _refusal(lambda: require_complete_arms(connection.record, deficient))
    assert error.code == X_ARMS_INCOMPLETE
    assert "checkpoint set is missing" in str(error)


def test_row13_refuses_a_checkpoint_no_case_named(harness: Harness) -> None:
    """The checkpoint comparison is two-directional for the same reason."""

    connection = harness.authenticate()
    checkpoints = dict(connection.roles.checkpoint_sha256)
    checkpoints[("other-case", "S")] = checkpoints[(CASE_ID, "S")]
    widened = replace(connection.roles, checkpoint_sha256=checkpoints)
    error = _refusal(lambda: require_complete_arms(connection.record, widened))
    assert error.code == X_ARMS_INCOMPLETE
    assert "checkpoint set carries" in str(error)


def test_row13_refuses_a_case_that_names_one_arm(harness: Harness) -> None:
    """A one-armed case is refused before any payload key is compared."""

    connection = harness.authenticate()
    case = connection.record.cases[0]
    lone = replace(case, arms={"C1": case.arms["C1"]})
    record = replace(connection.record, cases=(lone,))
    error = _refusal(lambda: require_complete_arms(record, connection.roles))
    assert error.code == X_ARMS_INCOMPLETE
    assert "names the arms ('C1',)" in str(error)


def test_row13_is_a_post_condition_the_production_path_cannot_reach(
    harness: Harness, record: dict[str, Any]
) -> None:
    """The reason row 13 has only seam tests, measured rather than asserted.

    A record naming one arm never reaches step 12 at all: `connection_record` parses
    `cases[*].arms` as a mapping whose keys are exactly the two suites, so the record
    is refused at step 2. Row 13 exists to make that other module's guarantee a named
    refusal here instead of an inherited assumption -- and this test is what records
    that the guarantee is real today.
    """

    del record["cases"][0]["arms"]["S"]
    error = _drive(harness, record)
    assert error.code == X_CONNECTION_UNAUTHORIZED


# -- row 14 ------------------------------------------------------------------ #
@pytest.mark.parametrize("field_name", LABEL_FIELDS)
def test_row14_refuses_arms_that_disagree_about_any_label_field(
    harness: Harness, field_name: str
) -> None:
    """All eight schema-D fields are compared, one case per field."""

    connection = harness.authenticate()
    key = _payload_key(CASE_ID, "S", "labels")
    original = np.asarray(connection.roles.payloads[key][field_name])
    if original.dtype.kind == "U":
        changed = np.array("disagreeing-fixture-value", dtype=original.dtype.kind)
    elif original.dtype.kind == "b":
        changed = np.array(not bool(original.item()))
    else:
        changed = np.asarray(original.item() + 1, dtype=original.dtype)
    edited = _with_payload(
        connection, key, _edited(connection.roles.payloads[key], **{field_name: changed})
    )
    error = _refusal(
        lambda: require_pair_agreement(edited.record, edited.roles)
    )
    assert error.code == X_PAIR_MISMATCH
    assert f"labels.{field_name} is " in str(error)


def test_row14_refuses_arms_that_do_not_replay_one_task_reference(
    harness: Harness,
) -> None:
    """Two arms replaying different commanded trajectories are not one pair."""

    connection = harness.authenticate()
    key = _payload_key(CASE_ID, "S", "plant")
    reference = np.array(connection.roles.payloads[key]["task_reference"], copy=True)
    reference[0, 0] += 1.0
    edited = _with_payload(
        connection, key, _edited(connection.roles.payloads[key], task_reference=reference)
    )
    error = _refusal(lambda: require_pair_agreement(edited.record, edited.roles))
    assert error.code == X_PAIR_MISMATCH
    assert "one commanded task_reference" in str(error)


def test_row14_refuses_a_rewritten_labels_payload_on_the_production_path(
    harness: Harness,
) -> None:
    """The same refusal, driven from bytes through the whole authenticated chain."""

    connection = harness.authenticate()
    key = _payload_key(CASE_ID, "S", "labels")
    payload = dict(connection.roles.payloads[key])
    payload["severity"] = np.asarray(0.25, dtype=np.float64)
    run_id = f"{PAIR_ID}_S"
    with _rewritten_payload(harness, "labels", "S", run_id, payload) as arguments:
        error = _refusal(lambda: _resolve(arguments))
    assert error.code == X_PAIR_MISMATCH
    assert "labels.severity is " in str(error)


# -- row 15 ------------------------------------------------------------------ #
def test_row15_refuses_arms_that_do_not_share_one_playback_grid(
    harness: Harness,
) -> None:
    """One case has one clock, and both arms have to be on it."""

    connection = harness.authenticate()
    key = _payload_key(CASE_ID, "S", "plant")
    grid = np.array(connection.roles.payloads[key]["t_s"], copy=True) + 1.0
    edited = _with_payload(connection, key, _edited(connection.roles.payloads[key], t_s=grid))
    error = _refusal(lambda: bind_playback_timebase(edited.record, edited.roles))
    assert error.code == X_TIMEBASE_MISMATCH
    assert "do not share one playback grid" in str(error)


def test_row15_refuses_a_plant_grid_that_is_not_one_dimensional(
    harness: Harness,
) -> None:
    """Only the grid's rank is checked here; every property *of* it is `j_5s`'s."""

    connection = harness.authenticate()
    key = _payload_key(CASE_ID, "C1", "plant")
    grid = np.asarray(connection.roles.payloads[key]["t_s"]).reshape(-1, 1)
    edited = _with_payload(connection, key, _edited(connection.roles.payloads[key], t_s=grid))
    error = _refusal(lambda: bind_playback_timebase(edited.record, edited.roles))
    assert error.code == X_TIMEBASE_MISMATCH
    assert "non-empty one-dimensional grid" in str(error)


@pytest.mark.parametrize("array_name", PLANT_FRAME_ARRAYS)
def test_row15_binds_every_frame_bearing_plant_array_to_the_grid(
    harness: Harness, array_name: str
) -> None:
    """One case per frame-bearing array rows 17 to 21 consume."""

    connection = harness.authenticate()
    key = _payload_key(CASE_ID, "C1", "plant")
    payload = connection.roles.payloads[key]
    shortened = np.asarray(payload[array_name])[:-1]
    edited = _with_payload(connection, key, _edited(payload, **{array_name: shortened}))
    error = _refusal(lambda: bind_playback_timebase(edited.record, edited.roles))
    assert error.code == X_TIMEBASE_MISMATCH
    assert f"plant.{array_name} carries {FIXTURE_N_STEPS - 1} frames" in str(error)


def test_row15_refuses_a_controller_step_grid_of_the_wrong_length(
    harness: Harness,
) -> None:
    """The contiguity rule is `role_contract`'s; the *length* is this row's."""

    connection = harness.authenticate()
    key = _payload_key(CASE_ID, "S", "controller_logs")
    payload = connection.roles.payloads[key]
    edited_arrays = {
        name: np.asarray(value)[:-1] for name, value in payload.items()
    }
    edited_arrays["step"] = np.arange(FIXTURE_N_STEPS - 1, dtype=np.int64)
    edited = _with_payload(connection, key, edited_arrays)
    error = _refusal(lambda: bind_playback_timebase(edited.record, edited.roles))
    assert error.code == X_TIMEBASE_MISMATCH
    assert "controller_logs.step is not the contiguous 0-based grid" in str(error)


@pytest.mark.parametrize("array_name", ["t_s", "controller_mode"])
def test_row15_binds_the_controller_axes_to_the_grid(
    harness: Harness, array_name: str
) -> None:
    """A controller axis of the wrong length cannot be drawn against the playback."""

    connection = harness.authenticate()
    key = _payload_key(CASE_ID, "S", "controller_logs")
    payload = connection.roles.payloads[key]
    shortened = np.asarray(payload[array_name])[:-1]
    edited = _with_payload(connection, key, _edited(payload, **{array_name: shortened}))
    error = _refusal(lambda: bind_playback_timebase(edited.record, edited.roles))
    assert error.code == X_TIMEBASE_MISMATCH
    assert f"controller_logs.{array_name} has shape" in str(error)


def test_row15_refuses_a_rewritten_controller_payload_on_the_production_path(
    harness: Harness,
) -> None:
    """The timebase refusal, driven from bytes.

    `controller_logs` is the role a shortened payload can be written to without also
    tripping row 14: nothing in the controller role is compared between arms one row
    earlier, so this refusal is unambiguously step 15's.
    """

    connection = harness.authenticate()
    key = _payload_key(CASE_ID, "S", "controller_logs")
    payload = {
        name: np.asarray(value)[:-1]
        for name, value in connection.roles.payloads[key].items()
    }
    payload["step"] = np.arange(FIXTURE_N_STEPS - 1, dtype=np.int64)
    run_id = f"{PAIR_ID}_S"
    with _rewritten_payload(
        harness, "controller_logs", "S", run_id, payload
    ) as arguments:
        error = _refusal(lambda: _resolve(arguments))
    assert error.code == X_TIMEBASE_MISMATCH
    assert "controller_logs.step is not the contiguous 0-based grid" in str(error)


def test_row15_never_compares_the_controller_clock_to_the_playback_grid(
    harness: Harness,
) -> None:
    """Finding CI's accept side: a shifted controller clock is faithful real data.

    `assignment_generator._step_index` makes a label's onset `onset_s / dt` while
    `cable_plant` stamps `t_s` after advancing, so a live controller clock runs one
    control interval ahead of the plant's. Binding the two would refuse exactly that
    data, so this test requires the offset grid to be **accepted**.
    """

    connection = harness.authenticate()
    key = _payload_key(CASE_ID, "S", "controller_logs")
    payload = connection.roles.payloads[key]
    offset = np.asarray(payload["t_s"]) + 0.002
    edited = _with_payload(connection, key, _edited(payload, t_s=offset))
    playback = bind_playback_timebase(edited.record, edited.roles)
    assert np.array_equal(
        playback[CASE_ID],
        np.asarray(connection.roles.payloads[_payload_key(CASE_ID, "C1", "plant")]["t_s"]),
    )


# -- row 16 ------------------------------------------------------------------ #
def _decision_payload(
    payload: Mapping[str, np.ndarray], steps: Sequence[int], times: Sequence[float]
) -> dict:
    """Return an `estimator_outputs` payload carrying the given decision axes."""

    count = len(steps)
    built = {
        name: np.repeat(np.asarray(value)[:1], count, axis=0)
        for name, value in payload.items()
    }
    built["step"] = np.asarray(steps, dtype=np.int64)
    built["decision_time_s"] = np.asarray(times, dtype=np.float64)
    return built


def test_row16_refuses_a_decision_after_the_last_playback_sample(
    harness: Harness,
) -> None:
    """A decision with no frame to be drawn against is refused, not clipped."""

    connection = harness.authenticate()
    key = _payload_key(CASE_ID, "C1", "estimator_outputs")
    payload = _decision_payload(connection.roles.payloads[key], [31], [0.5])
    edited = _with_payload(connection, key, payload)
    playback = bind_playback_timebase(edited.record, edited.roles)
    error = _refusal(
        lambda: resolve_decisions(edited.record, edited.roles, playback)
    )
    assert error.code == X_DECISION_UNSUPPORTED
    assert "lies outside the playback extent" in str(error)


def test_row16_refuses_a_decision_before_the_first_playback_sample(
    harness: Harness,
) -> None:
    """The extent has two ends and both are compared.

    **This case needs a live-shaped grid, and finding that out is the point.** The
    contract fixture's `plant.t_s` starts at 0.000 s, so on that grid every time
    below the first sample is negative and `EstimatorOutput.validate` refuses it one
    branch earlier -- the lower bound would look covered while nothing had reached
    it. A real plant grid starts at one control interval, because `cable_plant`
    stamps `t_s` *after* advancing, so the grid is shifted here to the live shape and
    the decision placed inside the first interval.
    """

    connection = harness.authenticate()
    payloads = dict(connection.roles.payloads)
    for suite in SUITE_KEYS:
        plant_key = _payload_key(CASE_ID, suite, "plant")
        payloads[plant_key] = _edited(
            payloads[plant_key],
            t_s=np.asarray(payloads[plant_key]["t_s"]) + 0.002,
        )
    key = _payload_key(CASE_ID, "S", "estimator_outputs")
    payloads[key] = _decision_payload(payloads[key], [0], [0.001])
    edited = replace(connection, roles=replace(connection.roles, payloads=payloads))
    playback = bind_playback_timebase(edited.record, edited.roles)
    assert float(playback[CASE_ID][0]) == 0.002
    error = _refusal(
        lambda: resolve_decisions(edited.record, edited.roles, playback)
    )
    assert error.code == X_DECISION_UNSUPPORTED
    assert "lies outside the playback extent" in str(error)


def test_row16_refuses_carried_axes_that_stop_increasing(harness: Harness) -> None:
    """Order is a property of what this module carried, not only of the payload."""

    connection = harness.authenticate()
    key = _payload_key(CASE_ID, "C1", "estimator_outputs")
    payload = _decision_payload(
        connection.roles.payloads[key], [5, 5], [0.010, 0.020]
    )
    edited = _with_payload(connection, key, payload)
    playback = bind_playback_timebase(edited.record, edited.roles)
    error = _refusal(
        lambda: resolve_decisions(edited.record, edited.roles, playback)
    )
    assert error.code == X_DECISION_UNSUPPORTED
    assert "stopped increasing at index 1" in str(error)


def test_row16_refuses_a_decision_this_module_transcribed_wrongly(
    harness: Harness,
) -> None:
    """`validate()` here guards the adapter's own construction, not the payload.

    A `p_class` row that is not a simplex could never have passed step 12, so the
    only way this branch is reachable in production is a transcription defect in
    `resolve_decisions` itself -- which is exactly what it is there to catch.
    """

    connection = harness.authenticate()
    key = _payload_key(CASE_ID, "C1", "estimator_outputs")
    payload = dict(connection.roles.payloads[key])
    payload["p_class"] = np.zeros_like(np.asarray(payload["p_class"]))
    edited = _with_payload(connection, key, payload)
    playback = bind_playback_timebase(edited.record, edited.roles)
    error = _refusal(
        lambda: resolve_decisions(edited.record, edited.roles, playback)
    )
    assert error.code == X_DECISION_UNSUPPORTED
    assert "violates the schema-D contract" in str(error)


def test_row16_carries_every_decision_in_payload_order(harness: Harness) -> None:
    """More than one decision, and the accept side of the ordering rule."""

    connection = harness.authenticate()
    key = _payload_key(CASE_ID, "C1", "estimator_outputs")
    payload = _decision_payload(
        connection.roles.payloads[key], [3, 11, 29], [0.006, 0.022, 0.058]
    )
    edited = _with_payload(connection, key, payload)
    playback = bind_playback_timebase(edited.record, edited.roles)
    resolved = resolve_decisions(edited.record, edited.roles, playback)
    carried = resolved[(CASE_ID, "C1")]
    assert [decision.step for decision in carried] == [3, 11, 29]
    assert [decision.decision_time_s for decision in carried] == [0.006, 0.022, 0.058]


def test_row16_bounds_the_time_axis_only_and_that_is_the_settled_reading(
    harness: Harness,
) -> None:
    """A step at or past the grid's length is accepted when its time is in the extent.

    **This pins an interpretation, and it exists because the interpretation was
    inferred before it was stated.** Codex's Session-148 cross-review observed that
    row 16 binds `decision_time_s` to the playback extent while accepting
    `step == T`, and asked which reading of design 4.1's "inside the playback
    extent" the adapter means. The settled answer is *time only*, and the argument
    is in `resolve_decisions`' docstring: schema section D calls `step` bookkeeping
    and ties it to no grid, the design already refuses two bindings of exactly this
    shape because a faithful producer offsets the axis, nothing downstream uses
    `step` as an index, and step 12 plus the checks above still hold everything
    about `step` except the grid binding.

    So the acceptance below is a decision rather than an accident, and a later
    session that tightens it will fail this test and read the reason rather than
    discovering it. The grid here carries 32 samples numbered 0 to 31; the decision
    is stamped at step 32 -- one past the last control step -- at a time inside the
    extent.
    """

    connection = harness.authenticate()
    key = _payload_key(CASE_ID, "S", "estimator_outputs")
    payload = _decision_payload(connection.roles.payloads[key], [32], [0.020])
    edited = _with_payload(connection, key, payload)
    playback = bind_playback_timebase(edited.record, edited.roles)
    assert int(np.asarray(playback[CASE_ID]).shape[0]) == FIXTURE_N_STEPS
    carried = resolve_decisions(edited.record, edited.roles, playback)[(CASE_ID, "S")]
    assert len(carried) == 1
    assert carried[0].step == FIXTURE_N_STEPS
    assert carried[0].decision_time_s == 0.020


# -- row 17 ------------------------------------------------------------------ #
def test_row17_refuses_a_window_this_grid_cannot_close(
    harness: Harness, record: dict[str, Any]
) -> None:
    """The frozen 5 s headline over a 0.062 s fixture grid, driven end to end."""

    record["analysis_window_s"] = 5.0
    arguments = harness.rewrite_record(record)
    error = _refusal(lambda: _resolve(arguments))
    assert error.code == X_WINDOW_UNSUPPORTED
    assert "utils.metrics.j_5s" in str(error)
    assert "truncated before onset" in str(error)


def test_row17_re_raises_whatever_the_live_metric_refused(
    harness: Harness, monkeypatch: pytest.MonkeyPatch
) -> None:
    """Only a monkeypatch can hold a delegation (lesson 201).

    An AST test that asserts the call exists is satisfied by a function that calls
    and ignores. This one replaces the metric with one that raises a sentence no
    design document contains, and requires that sentence to be carried out of the
    row -- which is false unless the refusal really comes from the metric.
    """

    sentinel = "sentinel-refusal-no-design-document-contains-this"

    def _refusing_metric(*args: Any, **kwargs: Any) -> float:
        raise ValueError(sentinel)

    monkeypatch.setattr(connection_adapter, "j_5s", _refusing_metric)
    connection = harness.authenticate()
    truths = require_pair_agreement(connection.record, connection.roles)
    playback = bind_playback_timebase(connection.record, connection.roles)
    error = _refusal(
        lambda: require_tracking_window(
            connection.record, connection.roles, playback, truths
        )
    )
    assert error.code == X_WINDOW_UNSUPPORTED
    assert sentinel in str(error)


def test_row17_opens_the_window_at_onset_time_and_never_at_onset_index(
    harness: Harness,
) -> None:
    """Finding CI again, on the axis that would move the window.

    `onset_index` and `onset_time_s` do not agree in real data, so a row that indexed
    the grid by `onset_index` would open the window at the wrong sample. Here the two
    are driven apart deliberately: the onset *time* still lands on a sample and the
    window still closes, so the row must accept -- and it must accept for the reason
    that it never read the index.
    """

    connection = harness.authenticate()
    playback = bind_playback_timebase(connection.record, connection.roles)
    payloads = dict(connection.roles.payloads)
    for suite in SUITE_KEYS:
        key = _payload_key(CASE_ID, suite, "labels")
        payloads[key] = _edited(
            payloads[key], onset_index=np.asarray(0, dtype=np.int64)
        )
    edited = replace(
        connection, roles=replace(connection.roles, payloads=payloads)
    )
    truths = require_pair_agreement(edited.record, edited.roles)
    assert truths[CASE_ID].onset_index == 0
    assert truths[CASE_ID].onset_time_s == 0.02
    require_tracking_window(edited.record, edited.roles, playback, truths)


# -- the order is the contract ------------------------------------------------ #
def test_the_rows_run_in_their_normative_order(harness: Harness) -> None:
    """A state that breaks two rows refuses with the earlier row's code."""

    connection = harness.authenticate()
    labels_key = _payload_key(CASE_ID, "S", "labels")
    plant_key = _payload_key(CASE_ID, "S", "plant")
    payloads = dict(connection.roles.payloads)
    payloads[labels_key] = _edited(
        payloads[labels_key], severity=np.asarray(0.5, dtype=np.float64)
    )
    grid = np.asarray(payloads[plant_key]["t_s"]) + 1.0
    payloads[plant_key] = _edited(payloads[plant_key], t_s=grid)
    edited = replace(connection, roles=replace(connection.roles, payloads=payloads))
    error = _refusal(lambda: resolve_cases(edited))
    assert error.code == X_PAIR_MISMATCH


def test_rows13_to_17_open_no_file_at_all(harness: Harness) -> None:
    """Every fact these five rows read was authenticated before they ran."""

    connection = harness.authenticate()
    opened: list[str] = []
    real_read_bytes = Path.read_bytes

    def _counting_read_bytes(self: Path) -> bytes:
        opened.append(str(self))
        return real_read_bytes(self)

    original = Path.read_bytes
    Path.read_bytes = _counting_read_bytes  # type: ignore[method-assign]
    try:
        resolve_cases(connection)
    finally:
        Path.read_bytes = original  # type: ignore[method-assign]
    assert opened == []


# -- the constants answer to the objects that own them ------------------------ #
def test_the_label_field_names_are_the_live_structs_own_field_list() -> None:
    """`LABEL_FIELDS` inherits `LabelFields`'s pin instead of adding a second copy."""

    from dataclasses import fields as dataclass_fields

    assert LABEL_FIELDS == tuple(field.name for field in dataclass_fields(LabelFields))
    schema = json.loads(LIVE_SCHEMA.read_text(encoding="utf-8"))
    assert set(LABEL_FIELDS) == set(schema["roles"]["labels"]["fields"])
    assert len(LABEL_FIELDS) == 8


def test_the_frame_bearing_plant_arrays_are_declared_over_the_playback_axis() -> None:
    """Every array row 15 binds is one the schema declares with a leading `T`."""

    schema = json.loads(LIVE_SCHEMA.read_text(encoding="utf-8"))
    declared = schema["roles"]["plant"]["fields"]
    for name in PLANT_FRAME_ARRAYS:
        assert declared[name]["shape"][0] == "T"
    assert PLANT_FRAME_ARRAYS == (
        "q_true",
        "deform_coords",
        "task_reference",
        "true_task_output",
    )


def test_the_fixture_window_is_a_literal_and_its_bound_is_measured_not_claimed(
    harness: Harness,
) -> None:
    """Pin the constant, and measure the bound it sits under rather than asserting it.

    The value is stated as a literal so a change to the grid cannot silently carry
    the constant with it. The three calls beside it are the measurement: 0.040 s and
    0.042 s both close on this grid and 0.044 s does not, so the largest window this
    grid can close is 0.042 s and **the fixture's 0.040 s is deliberately not the
    maximum**. Codex's Session-148 cross-review found an earlier version of this test
    claiming maximality in its name and docstring, and that claim was false; this is
    its forward correction, and the reason 0.040 s is kept is the convention recorded
    beside `ANALYSIS_WINDOW_S` -- the largest whole multiple of 0.01 s inside the
    bound, chosen so the fixture window does not sit on a boundary.
    """

    from utils.metrics import j_5s

    assert ANALYSIS_WINDOW_S == 0.04
    connection = harness.authenticate()
    plant = connection.roles.payloads[_payload_key(CASE_ID, "C1", "plant")]
    grid = np.asarray(plant["t_s"])
    for window_s in (0.040, 0.042):
        j_5s(
            grid,
            plant["task_reference"],
            plant["true_task_output"],
            0.02,
            window_s=window_s,
        )
    with pytest.raises(ValueError):
        j_5s(
            grid,
            plant["task_reference"],
            plant["true_task_output"],
            0.02,
            window_s=0.044,
        )


# --------------------------------------------------------------------------- #
# Row 18 -- the centerline derivation.
#
# **The contract fixture cannot be the accept path here, and that is measured
# rather than assumed** (design 2.4). Its `deform_coords` and its
# `true_task_output` come from two independent synthetic maps -- the deformation
# from an `rng.uniform` phase set, the tip from `_deformed_tip(q_true,
# curvature_true)` with `deform_coords` entering nowhere -- so a derivation that
# walked its declared chain would miss its recorded tip by millimetres for reasons
# that say nothing about the derivation. Its declared `render_geometry` is a toy
# three-segment chain under an unimplemented derivation version, which is exactly
# what row 18 must refuse, so the fixture stays the *refusal* instrument it always
# was.
#
# The accept path is the dedicated coherent fixture: one forward map generates
# `q_true`, `deform_coords`, the centerline and `true_task_output` together, and
# `_coherent_geometry` installs that data and its declaration over the contract
# harness -- both arms' `plant` payloads on disk, the geometry-validation artifact
# the record's `tolerance_source` names, and the record's whole `render_geometry`
# block. Every identity the rewrite moves is regenerated from the files themselves,
# so the chain still authenticates end to end and a refusal comes from row 18 and
# not from step 8 or step 11.
# --------------------------------------------------------------------------- #
#: The draft config's `values.timing.f_ctrl_hz`, as a literal. The coherent record's
#: grid has to be the grid the contract fixture already wrote, or step 15 refuses the
#: rewrite before row 18 is reached.
#: `test_the_coherent_fixture_grid_is_the_config_grid` pins the literal against the
#: config the harness actually loaded, so a config change fails loudly here instead of
#: quietly moving the fixture.
FIXTURE_F_CTRL_HZ = 500.0

#: The number of points one derived centerline carries on this chain, as a literal:
#: sixteen ordered bodies in each of two links, plus the distal point. Written out
#: rather than re-derived because `utils.verification_scene`'s `[T,N,2]` gate requires
#: only `N >= 2`, so a wrong `N` is invisible to every shape check downstream, and a
#: test written as a function of the chain would move with the mutation (lesson 229).
COHERENT_CENTERLINE_POINTS = 33


def _coherent_geometry_and_record(harness: Harness, seed: int, tolerance_m: float):
    """Return the coherent `RenderGeometry`, its record, and its validation document.

    The geometry is built twice on purpose. The first build cannot carry the
    validation artifact's digest, because that artifact reports the agreement the
    generator achieves and the generator has not run yet; the second is
    `dataclasses.replace` of exactly that one field, which is what says the chain the
    record declares is the chain the data was generated under rather than a second
    chain that happens to look the same.
    """

    provisional = coherent_render_geometry(
        producer_relative_path=PRODUCER_RELATIVE,
        producer_sha256=tracked_text_digest(harness.packet_root / PRODUCER_RELATIVE),
        tolerance_artifact_relative_path=GEOMETRY_RELATIVE,
        tolerance_sha256="0" * 64,
        distal_tolerance_m=tolerance_m,
    )
    record = coherent_privileged_record(
        geometry=provisional,
        n_steps=FIXTURE_N_STEPS,
        f_ctrl=FIXTURE_F_CTRL_HZ,
        seed=seed,
    )
    validation = geometry_validation_document(
        fixture_maximum_deviation_m(record, provisional), tolerance_m=tolerance_m
    )
    return provisional, record, validation


@contextmanager
def _coherent_geometry(
    harness: Harness,
    *,
    seed: int = 0,
    tolerance_m: float = CENTERLINE_TASK_OUTPUT_TOL_M,
    edit_plant: Callable[[dict], dict] | None = None,
    edit_geometry: Callable[[dict], dict] | None = None,
):
    """Install the coherent fixture over the harness, then restore every byte.

    Args:
        harness: the built contract harness.
        seed: selects the coherent generator's deterministic analytic phase family.
        tolerance_m: the tolerance the record declares *and* the one the validation
            artifact states, kept as one parameter so the two cannot drift apart and
            refuse each other at step 5 for a reason row 18 is not about.
        edit_plant: given `{suite: payload dict}`, returns the payloads to write. Used
            to drive row 18's one arm-specific refusal.
        edit_geometry: given the serialised `render_geometry` block, returns the block
            to declare. Used to drive the record-level refusals.

    **Both arms get the same plant record.** Read-order row 14 requires the two arms
    to agree about `task_reference`, so two independently generated trajectories would
    be refused a row before the one under test -- and the contract fixture already
    writes one record per pair for the same reason.
    """

    geometry, coherent, validation = _coherent_geometry_and_record(
        harness, seed, tolerance_m
    )
    payloads = {suite: dict(coherent.__dict__) for suite in SUITE_KEYS}
    if edit_plant is not None:
        payloads = edit_plant(payloads)

    validation_path = harness.packet_root / GEOMETRY_RELATIVE
    saved: list[tuple[Path, bytes]] = [(validation_path, validation_path.read_bytes())]
    for suite in SUITE_KEYS:
        directory = role_root_for(harness.role_root, "plant", suite)
        run_id = f"{PAIR_ID}_{suite}"
        saved.append((directory / f"{run_id}.npz", (directory / f"{run_id}.npz").read_bytes()))
        saved.append((directory / ROLE_INDEX_NAME, (directory / ROLE_INDEX_NAME).read_bytes()))
    try:
        _write_json(validation_path, validation)
        geometry = replace(
            geometry,
            tolerance_source=replace(
                geometry.tolerance_source,
                sha256=tracked_text_digest(validation_path),
            ),
        )
        for suite in SUITE_KEYS:
            directory = role_root_for(harness.role_root, "plant", suite)
            run_id = f"{PAIR_ID}_{suite}"
            payload_path = directory / f"{run_id}.npz"
            buffer = io.BytesIO()
            np.savez(
                buffer,
                **{
                    name: np.asarray(value)
                    for name, value in payloads[suite].items()
                },
            )
            payload_path.write_bytes(buffer.getvalue())
            _reindex(directory / ROLE_INDEX_NAME, run_id, external_digest(payload_path))
        document = harness._record_document()
        block = render_geometry_document(geometry)
        document["render_geometry"] = block if edit_geometry is None else edit_geometry(block)
        yield harness.rewrite_record(document)
    finally:
        for path, raw in saved:
            path.write_bytes(raw)


def _geometry(arguments: Mapping[str, Any]):
    """Drive rows 1 through 18 end to end."""

    connection = authenticate_connection(**arguments)
    return connection, resolve_geometry(connection, resolve_cases(connection))


# -- the accept side, which is what makes every refusal below mean something --- #
def test_the_coherent_fixture_grid_is_the_config_grid(harness: Harness) -> None:
    """The literal control rate is the one the harness's own config declares."""

    config = load_config(
        harness.packet_root / CONFIG_RELATIVE, harness.packet_root / SCHEMA_RELATIVE
    )
    assert float(config.document["values"]["timing"]["f_ctrl_hz"]) == FIXTURE_F_CTRL_HZ


def test_row18_accepts_the_coherent_fixture_end_to_end(harness: Harness) -> None:
    """Rows 1 through 18 over data and a declaration that describe one body."""

    with _coherent_geometry(harness) as arguments:
        connection, geometry = _geometry(arguments)
    assert isinstance(geometry, AuthenticatedGeometry)
    assert geometry.tolerance_m == connection.record.render_geometry.distal_tolerance_m
    assert len(geometry.cases) == 1
    case = geometry.cases[0]
    assert case.case_id == CASE_ID
    assert tuple(sorted(case.arms)) == tuple(sorted(SUITE_KEYS))
    for suite in SUITE_KEYS:
        arm = case.arms[suite]
        assert isinstance(arm, ArmGeometry)
        assert arm.suite == suite
        assert arm.centerline.shape == (
            FIXTURE_N_STEPS,
            COHERENT_CENTERLINE_POINTS,
            2,
        )
        assert arm.distal_deviation_m == 0.0


def test_row18_reproduces_the_recorded_tip_exactly_on_the_coherent_fixture(
    harness: Harness,
) -> None:
    """The measured agreement is exactly zero, and that is a property not a threshold.

    The generator sets `true_task_output` to the derived distal point itself, so the
    adapter recomputing the same map has to land on the same bytes. A non-zero value
    here would mean the two copies of the map had diverged -- which is the failure the
    shared `utils.centerline_geometry` module exists to make impossible.
    """

    with _coherent_geometry(harness) as arguments:
        connection, geometry = _geometry(arguments)
        for suite in SUITE_KEYS:
            plant = connection.roles.payloads[_payload_key(CASE_ID, suite, "plant")]
            distal = geometry.cases[0].arms[suite].centerline[:, -1, :]
            assert np.array_equal(distal, np.asarray(plant["true_task_output"]))


def test_row18_carries_read_only_centerlines(harness: Harness) -> None:
    """Nothing downstream can edit a geometry this row established."""

    with _coherent_geometry(harness) as arguments:
        _, geometry = _geometry(arguments)
    for suite in SUITE_KEYS:
        centerline = geometry.cases[0].arms[suite].centerline
        assert centerline.flags.writeable is False
        with pytest.raises(ValueError):
            centerline[0, 0, 0] = 0.0


def test_row18_carries_no_cross_arm_scalar(harness: Harness) -> None:
    """Invariant W13, read off the value's own field set rather than asserted."""

    fields = {field.name for field in dataclass_fields(CaseGeometry)}
    assert fields == {"case_id", "arms"}
    fields = {field.name for field in dataclass_fields(AuthenticatedGeometry)}
    assert fields == {"tolerance_m", "cases"}


def test_row18_uses_the_declared_tolerance_and_not_the_fixture_constant(
    harness: Harness,
) -> None:
    """The tolerance the row applies is the record's, and the two are different numbers.

    Design finding CU: `CENTERLINE_TASK_OUTPUT_TOL_M` measures the fixture generator's
    construction exactness and is never the adapter's comparand. Here the record
    declares a tolerance three orders of magnitude looser, and it is that number the
    result carries -- so a later edit that reached for the module constant instead
    would fail this test rather than pass silently on a fixture where both happen to
    hold.
    """

    with _coherent_geometry(harness, tolerance_m=1.0e-6) as arguments:
        _, geometry = _geometry(arguments)
    assert geometry.tolerance_m == 1.0e-6
    assert geometry.tolerance_m != CENTERLINE_TASK_OUTPUT_TOL_M
    assert CENTERLINE_TASK_OUTPUT_TOL_M == 1.0e-9


# -- the refusals ------------------------------------------------------------- #
def test_row18_refuses_the_contract_fixtures_own_declared_geometry(
    harness: Harness,
) -> None:
    """The contract fixture is a refusal instrument here, and this drives it.

    Its record declares `derivation_version: "v0.1"`, a toy three-segment chain and an
    `absolute` joint convention -- none of which this adapter implements. The refusal
    arrives before any arithmetic, which is the point: an adapter that derived a
    plausible centerline under a version whose map it does not carry would produce a
    picture rather than an error.
    """

    connection = authenticate_connection(**harness.arguments())
    cases = resolve_cases(connection)
    error = _refusal(lambda: resolve_geometry(connection, cases))
    assert error.code == X_GEOMETRY_UNSUPPORTED
    assert "derivation_version" in str(error)


def test_row18_refuses_a_projection_this_derivation_does_not_implement(
    harness: Harness,
) -> None:
    """The projection carries the tangent sign, so an unknown one has no default."""

    def unknown(block: dict) -> dict:
        block["planar_convention"]["projection"] = "model_x_to_scene_x;model_z_to_scene_y"
        return block

    with _coherent_geometry(harness, edit_geometry=unknown) as arguments:
        error = _refusal(lambda: _geometry(arguments))
    assert error.code == X_GEOMETRY_UNSUPPORTED
    assert "projection" in str(error)


def test_row18_refuses_a_q_true_convention_this_derivation_does_not_implement(
    harness: Harness,
) -> None:
    """The absolute reading draws a continuous, plausible, wrong centerline.

    It is refused by name rather than defaulted, because nothing about the output
    reveals which reading produced it.
    """

    def absolute(block: dict) -> dict:
        block["planar_convention"]["q_true_convention"] = "absolute"
        return block

    with _coherent_geometry(harness, edit_geometry=absolute) as arguments:
        error = _refusal(lambda: _geometry(arguments))
    assert error.code == X_GEOMETRY_UNSUPPORTED
    assert "q_true_convention" in str(error)


def test_row18_refuses_a_distal_point_outside_the_declared_tolerance(
    harness: Harness,
) -> None:
    """The one refusal that is about a particular arm, and it names that arm.

    One arm's recorded tip is displaced by a millimetre. **The displacement has to
    carry `tracking_error` and its norm with it, and finding that out is worth
    recording:** `utils.role_contract` requires `tracking_error` to equal
    `task_reference - true_task_output`, so moving the tip alone is refused at step
    12 as an inconsistent payload rather than at row 18 as a geometry disagreement.
    Carried consistently, the payload is internally impeccable and still describes a
    body the declared chain does not produce -- which is exactly the fault this row
    exists to see, and exactly the fault no single-payload check can. The pair still
    agrees about `task_reference` at row 14 and still shares one grid at row 15.
    """

    def displace(payloads: dict) -> dict:
        payload = dict(payloads["S"])
        tip = np.asarray(payload["true_task_output"]) + 1.0e-3
        tracking_error = np.asarray(payload["task_reference"]) - tip
        payload["true_task_output"] = tip
        payload["tracking_error"] = tracking_error
        payload["tracking_error_norm"] = np.linalg.norm(tracking_error, axis=1)
        payloads["S"] = payload
        return payloads

    with _coherent_geometry(harness, edit_plant=displace) as arguments:
        error = _refusal(lambda: _geometry(arguments))
    assert error.code == X_GEOMETRY_UNSUPPORTED
    assert "arm S" in str(error)
    assert "above the declared tolerance" in str(error)


def test_row18_refuses_a_triplet_column_the_payload_does_not_carry(
    harness: Harness,
) -> None:
    """The declared chain and the payload's width must describe one body.

    This one is driven through the in-memory seam rather than end to end, and the
    reason is the same one row 13's test records: `utils.role_contract` fixes
    `deform_coords` at the configuration's `n_def`, so a payload narrower than the
    declaration cannot reach step 12 on the production path. The guard is a
    post-condition across a module boundary, and its test drives the boundary.
    """

    with _coherent_geometry(harness) as arguments:
        connection = authenticate_connection(**arguments)
        cases = resolve_cases(connection)
    narrowed = replace(
        cases.cases[0].arms["C1"],
        deform_coords=np.asarray(cases.cases[0].arms["C1"].deform_coords)[:, :3],
    )
    case = replace(
        cases.cases[0],
        arms={"C1": narrowed, "S": cases.cases[0].arms["S"]},
    )
    error = _refusal(
        lambda: resolve_geometry(connection, AuthenticatedCases(cases=(case,)))
    )
    assert error.code == X_GEOMETRY_UNSUPPORTED
    assert "columns" in str(error)
