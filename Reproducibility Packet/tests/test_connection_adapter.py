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
import inspect
import io
import json
import os
import shutil
import sys
from contextlib import contextmanager
from dataclasses import asdict, fields as dataclass_fields, replace
from pathlib import Path, PurePosixPath
from types import MappingProxyType
from typing import Any, Callable, Mapping, Sequence

import numpy as np
import pytest

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "scripts"))

from build_data_contract_fixture import build_fixture  # noqa: E402
from utils.config_contract import (  # noqa: E402
    ConfigContractError,
    expected_config_hash,
    load_config,
    validate_config_document,
)
from utils import connection_adapter  # noqa: E402
from utils.connection_adapter import (  # noqa: E402
    AUDIT_NAMES,
    DEVELOPMENT_TRACE_PREFIX,
    LABEL_FIELDS,
    MANIFEST_AUDIT_KEY,
    MANIFEST_CENSUS_FIELDS,
    MANIFEST_NAME,
    MAX_FIELD_PATH_INDEX_DIGITS,
    PLANT_FRAME_ARRAYS,
    PLANT_MODEL_ID_FIELD_PATH,
    ROLE_INDEX_NAME,
    SUITE_QUALIFIED_ROLES,
    ArmGeometry,
    ArmSeries,
    AuthenticatedCases,
    AuthenticatedConnection,
    AuthenticatedGeometry,
    CaseGeometry,
    ResolvedProvenance,
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
    resolve_bundle,
    resolve_cases,
    resolve_decisions,
    resolve_geometry,
    resolve_provenance,
    role_root_for,
    strict_json_document,
    tracked_text_digest,
    value_at_field_path,
    write_bundle,
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
    expected_open_set,
    load_connection_record,
    record_relative_path,
    # The row-19 seam's post-condition calls the function that OWNS read-order row
    # 3's authority/split policy rather than restating the rule, for the same reason
    # the module points at owners instead of copying them: a restated rule is a
    # second rule, and two rules disagree on the inputs nobody enumerated. It is
    # private to that module and imported here deliberately and only for that.
    _require_authority_split_policy,
)
from utils.metrics import SOURCE_CLASS_ORDER  # noqa: E402
from utils.protocol_p import canonical_json  # noqa: E402
from utils.role_contract import validate_role_payload  # noqa: E402
from utils.storage_contract import (  # noqa: E402
    IdentityManifestRow,
    RoleIndexRow,
    read_identity_manifest,
    read_role_index,
    write_identity_manifest,
    write_role_index,
)
from utils.verification_scene import (  # noqa: E402
    CENTERLINE_TASK_OUTPUT_TOL_M,
    DEVELOPMENT_ONLY,
    FINAL,
    PROVENANCE_STATES,
    REQUIRED_SOURCE_CLASSES,
    SUITE_KEYS,
    SYNTHETIC_FIXTURE,
    LabelFields,
    Provenance,
    VerificationBundle,
    VerificationSceneError,
    canonical_bundle_text,
    canonical_scene_text,
    validate_bundle,
    validate_scene,
    X_ARMS_INCOMPLETE,
    X_BUNDLE_INCOMPLETE,
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

#: The generated plant model's identity, as the draft config declares it at
#: `PLANT_MODEL_ID_FIELD_PATH`. It is written here as a **literal** and pinned by
#: equality against the loaded config in
#: `test_the_fixture_model_id_is_the_configuration_s_own`, rather than being read out
#: of the config at fixture-build time: a fixture whose input is a function of the
#: value under test would keep agreeing with the config however the config moved,
#: which is the defect shape the mutation sweep has already caught twice on this
#: lane. Until Session 150 the record below declared `"cable-two-link"`, which the
#: configuration has never carried; nothing noticed because nothing compared them.
PLANT_MODEL_ID = "mujoco-cable-rod-development-candidate"

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
                    "model_id": PLANT_MODEL_ID,
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


def test_the_fixture_model_id_is_the_configuration_s_own(harness: Harness) -> None:
    """`PLANT_MODEL_ID` is the value the draft config actually declares.

    The literal above is what the harness record echoes, so if it drifted away from
    the configuration every model-identity test in this file would be exercising a
    private agreement between two copies of the same wrong string. This reads the
    config the harness loaded and compares the two directly.
    """

    document = json.loads(
        (harness.packet_root / CONFIG_RELATIVE).read_text(encoding="utf-8")
    )
    assert document["values"]["plant"]["model_id"] == PLANT_MODEL_ID
    assert PLANT_MODEL_ID_FIELD_PATH == "values.plant.model_id"


def test_row5_refuses_a_geometry_model_the_configuration_never_described(
    harness: Harness, record: dict[str, Any]
) -> None:
    """Design 3.5: the geometry source **echoes** the config's `model_id`.

    **This is Codex's Session-149 cross-review finding, driven end to end.** The
    producer digest fixes which *file* built the model and says nothing about which
    *model* the run was configured to build, so before this join a record could name
    any model at all and rows 1 through 18 would accept it: Codex's probe changed
    only this field, and the chain returned one case while reporting the record's
    `model_id` and the config's side by side. The whole point of the echo is that a
    scene cannot claim to be a picture of a body the configuration never described.
    """

    record["render_geometry"]["source"]["model_id"] = "not-the-config-model"
    error = _drive(harness, record)
    assert error.code == X_IDENTITY_MISMATCH
    assert "render_geometry.source.model_id" in str(error)
    assert PLANT_MODEL_ID in str(error)


def test_row5_refuses_a_configuration_that_carries_no_plant_model_id(
    harness: Harness, tmp_path: Path
) -> None:
    """An absent config field is this row's refusal, never a `None` that compares.

    The comparison runs through `value_at_field_path` precisely so a configuration
    missing the field refuses by name instead of silently comparing a record string
    against nothing. Driven by deleting `values.plant.model_id` from a copy of the
    draft config, with the record's declared `config_hash` regenerated so the chain
    reaches step 5 rather than refusing at step 4 for an unrelated reason.
    """

    packet = tmp_path / "packet"
    shutil.copytree(harness.packet_root, packet)
    config_path = packet / CONFIG_RELATIVE
    document = json.loads(config_path.read_text(encoding="utf-8"))
    del document["values"]["plant"]["model_id"]
    document["config_hash"] = expected_config_hash(document)
    _write_json(config_path, document)
    reloaded = load_config(config_path, packet / SCHEMA_RELATIVE)
    edited = copy.deepcopy(harness.document)
    edited["config"]["config_hash"] = reloaded.config_hash
    edited["config"]["sha256"] = tracked_text_digest(config_path)
    _write_json(
        packet / RESULT_RELATIVE,
        {
            "read": {
                "cases": [CASE_ID],
                "config_hash": reloaded.config_hash,
                "split": SPLIT,
            },
            "status": "synthetic_fixture_established_result",
        },
    )
    edited["established_result"]["sha256"] = tracked_text_digest(
        packet / RESULT_RELATIVE
    )
    record_path = packet / record_relative_path(RECORD_LABEL)
    digest = _write_record(record_path, edited)
    error = _refusal(
        lambda: authenticate_connection(
            packet_root=packet,
            connection_record_path=record_path,
            connection_record_sha256=digest,
            config_path=config_path,
            role_root=harness.role_root,
            checkpoint_root=harness.checkpoint_root,
            output_dir=packet / "results" / "verification_connection_development",
        )
    )
    assert error.code == X_IDENTITY_MISMATCH
    assert PLANT_MODEL_ID_FIELD_PATH in str(error)


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
    sources = authenticate_sources(record_value, bound, config)
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
    saved_record = harness.record_path.read_bytes()
    try:
        buffer = io.BytesIO()
        np.savez(buffer, **{name: np.asarray(value) for name, value in payload.items()})
        payload_path.write_bytes(buffer.getvalue())
        _reindex(index_path, run_id, external_digest(payload_path))
        yield harness.rewrite_record(harness._record_document())
    finally:
        payload_path.write_bytes(saved_payload)
        index_path.write_bytes(saved_index)
        harness.record_path.write_bytes(saved_record)


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
    assert "is timed after the replay ended" in str(error)


def test_row16_accepts_the_step_zero_decision_the_live_producer_always_emits(
    harness: Harness,
) -> None:
    """The first decision is stamped *before* the first plant advance, and it stands.

    **This is Codex's Session-149 cross-review finding, driven on a live-shaped
    grid.** `utils.online_loop.run_online_rollout` reads `plant.data.time` and calls
    the policy *before* `plant.advance`, while `utils.cable_plant` stamps each
    `PlantStepState.t_s` from the clock *after* the advance. So on real data the
    first decision is at 0.0 s and `playback_t_s[0]` is one control interval later,
    and the Session-149 lower bound at `playback_t_s[0]` refused the one decision
    every faithful run necessarily emits.

    The contract fixture's own `plant.t_s` starts at 0.000 s and therefore cannot
    show this -- on that grid the two conventions coincide -- so the grid is shifted
    here to the live shape, exactly as the superseded refusal test had to. What
    changed is the expected outcome, not the construction.
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
    payloads[key] = _decision_payload(payloads[key], [0], [0.0])
    edited = replace(connection, roles=replace(connection.roles, payloads=payloads))
    playback = bind_playback_timebase(edited.record, edited.roles)
    assert float(playback[CASE_ID][0]) == 0.002
    carried = resolve_decisions(edited.record, edited.roles, playback)[(CASE_ID, "S")]
    assert len(carried) == 1
    assert carried[0].step == 0
    assert carried[0].decision_time_s == 0.0


def test_row16_leaves_the_lower_time_bound_to_the_schema_contract(
    harness: Harness,
) -> None:
    """A negative decision time refuses, and it refuses one branch earlier.

    Declining a lower bound of this row's own is not the same as leaving the low
    side open, and this drives which layer holds it: `EstimatorOutput.validate`
    requires `decision_time_s` to be finite and non-negative, so the refusal message
    is the schema-D one rather than an extent message this row would have had to
    invent. Adding a second comparison here would be a branch no input can reach.
    """

    connection = harness.authenticate()
    key = _payload_key(CASE_ID, "C1", "estimator_outputs")
    payload = _decision_payload(connection.roles.payloads[key], [0], [-0.001])
    edited = _with_payload(connection, key, payload)
    playback = bind_playback_timebase(edited.record, edited.roles)
    error = _refusal(
        lambda: resolve_decisions(edited.record, edited.roles, playback)
    )
    assert error.code == X_DECISION_UNSUPPORTED
    assert "violates the schema-D contract" in str(error)
    assert "decision_time_s must be finite and non-negative" in str(error)


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


def test_row16_refuses_a_step_this_replay_does_not_contain(
    harness: Harness,
) -> None:
    """`step` is a control-step index, and a replay of `T` steps contains `0 .. T-1`.

    **This reverses the Session-149 reading, and the reason is a measurement rather
    than a preference.** That session settled row 16 as bounding the time axis only
    and pinned `step == T` as *accepted*, on the argument that the schema ties the
    estimator's counter to no grid. Codex's Session-149 cross-review read the live
    producer instead: `run_online_rollout` iterates `step_index` over
    `range(n_steps)` and `EstimatorCommandPolicy` persists that exact integer in
    every `EstimatorOutput`, and `schema/schema.json` gives the field the unit
    `control_step_index`. So `step == T` is a state no faithful producer can emit,
    and accepting it was the error.

    The grid here carries 32 samples numbered 0 to 31; the decision is stamped at
    step 32, one past the last control step, at a time well inside the extent -- so
    the refusal is about the step axis and cannot be the time bound firing.
    """

    connection = harness.authenticate()
    key = _payload_key(CASE_ID, "S", "estimator_outputs")
    payload = _decision_payload(connection.roles.payloads[key], [FIXTURE_N_STEPS], [0.020])
    edited = _with_payload(connection, key, payload)
    playback = bind_playback_timebase(edited.record, edited.roles)
    assert int(np.asarray(playback[CASE_ID]).shape[0]) == FIXTURE_N_STEPS
    error = _refusal(
        lambda: resolve_decisions(edited.record, edited.roles, playback)
    )
    assert error.code == X_DECISION_UNSUPPORTED
    assert "does not contain" in str(error)
    assert "control step 32" in str(error)


def test_row16_accepts_the_last_control_step_the_replay_does_contain(
    harness: Harness,
) -> None:
    """The bound is `T`, not `T - 1`, and the accept side is driven beside it.

    A refusal test alone cannot separate "refuses step 32" from "refuses every step
    near the end", and the boundary is exactly where an off-by-one lives. `31` is
    the last step a 32-step replay contains and it is carried.
    """

    connection = harness.authenticate()
    key = _payload_key(CASE_ID, "S", "estimator_outputs")
    payload = _decision_payload(
        connection.roles.payloads[key], [FIXTURE_N_STEPS - 1], [0.020]
    )
    edited = _with_payload(connection, key, payload)
    playback = bind_playback_timebase(edited.record, edited.roles)
    carried = resolve_decisions(edited.record, edited.roles, playback)[(CASE_ID, "S")]
    assert len(carried) == 1
    assert carried[0].step == FIXTURE_N_STEPS - 1


def test_row16_does_not_pair_each_decision_to_the_sample_of_its_own_index(
    harness: Harness,
) -> None:
    """The upper time bound is the replay's end, not `playback_t_s[step]`.

    **This pins a bound that was deliberately not tightened.** With `step` now bound
    to the control-step domain, the per-decision pairing
    `decision_time_s <= playback_t_s[step]` becomes writable -- and it would bind the
    estimator's clock to the plant's grid sample by sample, which is the class of
    binding finding CI forbids for `onset_index` and step 15 forbids for
    `controller_t_s`, in both cases because a faithful producer offsets the axis.

    The decision below is stamped at step 0 with a time of 0.020 s, far past
    `playback_t_s[0] = 0.000 s` and far inside the replay. It is carried. A later
    session that adds the pairing will fail this test and read the reason rather
    than rediscovering it.
    """

    connection = harness.authenticate()
    key = _payload_key(CASE_ID, "S", "estimator_outputs")
    payload = _decision_payload(connection.roles.payloads[key], [0], [0.020])
    edited = _with_payload(connection, key, payload)
    playback = bind_playback_timebase(edited.record, edited.roles)
    assert float(playback[CASE_ID][0]) == 0.0
    carried = resolve_decisions(edited.record, edited.roles, playback)[(CASE_ID, "S")]
    assert len(carried) == 1
    assert carried[0].step == 0
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
    # The record is restored here for the same reason `_three_case_menu` restores it:
    # this installer rewrites it, and a context that exits leaving a record the read
    # order refuses has not restored the tree it says it restores.
    saved: list[tuple[Path, bytes]] = [
        (validation_path, validation_path.read_bytes()),
        (harness.record_path, harness.record_path.read_bytes()),
    ]
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


# -- row 19 ------------------------------------------------------------------ #
#
# **Row 19 is driven at the in-memory seam, and that is forced rather than chosen.**
# Invariant W7 says production `FINAL` is unreachable from every input this packet
# contains -- no frozen config satisfies final P1, no established final result
# exists, and the downstream roles are absent -- and that unreachability is a
# property the project is deliberately maintaining, not a gap to be filled by a
# fixture. So the one input set invariant W6 asks for, a state that computes
# `DEVELOPMENT_ONLY` under a record claiming `FINAL`, cannot be built end to end
# today without manufacturing the very reachability W7 exists to deny. The seam is
# the only instrument that reaches it, exactly as it is for row 13.
def _with_field_path_value(
    document: Mapping[str, Any], field_path: str, value: Any
) -> Mapping[str, Any]:
    """Return one authenticated source document with a single object path replaced.

    Only object-key segments are handled, and a segment that is not a key of a
    mapping is a loud failure rather than a silent no-op: this seam exists to keep
    a state coherent, and a setter that quietly writes nothing is the exact shape of
    the defect it is here to repair. Each rebuilt level is a fresh read-only view, so
    the edited document keeps the deeply frozen shape `authenticate_sources` returns.
    """

    segments = field_path.split(".")

    def rebuilt(node: Any, depth: int) -> Any:
        if depth == len(segments):
            return value
        segment = segments[depth]
        if not isinstance(node, Mapping) or segment not in node:
            trail = ".".join(segments[: depth + 1])
            raise AssertionError(
                f"the seam cannot set {field_path!r}: {trail} is not an object key "
                "of this document"
            )
        return MappingProxyType({**node, segment: rebuilt(node[segment], depth + 1)})

    return rebuilt(document, 0)


def _provenance_joins(connection: AuthenticatedConnection) -> dict[str, bool]:
    """Return every identity equality rows 4 through 12 establish, as `name -> it holds`.

    **This is the one statement of the post-row-12 identity coherence the seam has to
    preserve**, and it is written once so the helper below and the tests that assert
    it cannot drift apart. The nineteen entries are the joins the earlier rows put in
    place, each one an equality between *separately authenticated* facts:

      * row 3 binds the record's `config.relative_path` to the path row 4 then opens,
        so the validated config's `source_path` is that packet-relative path resolved
        under the injected packet root and never some other file;
      * row 4 binds the record's `config.config_hash` echo to the config it
        validated, and binds the validated config's `config_hash` to the canonical
        digest of the document it was taken over (`expected_config_hash`);
      * row 5 binds the established result's split and config identity to the
        record's;
      * row 6 binds both audit documents to the record's echoes of them, both audits'
        `config_hash` and every manifest row's to the validated config, every named
        run's split to the record's, and both audits' `manifest_audit` census to the
        census recomputed from the manifest rows -- which the adapter also keeps on
        `AuthenticatedDataset.census`;
      * row 10 binds every one of the record's 20-field `manifest_row` echoes to the
        authenticated manifest row it names, and that echo's own `split` to the
        record's split;
      * row 12 binds every authenticated role-index row's `config_hash` to the
        validated config, through `utils.role_contract`'s own index check.

    **The last three groups are Codex's Session-151 finding**, measured before it was
    accepted: the Session-151 seam left the recomputed census, both audit census
    blocks, both record manifest echoes and all eight role-index config hashes behind
    when it moved the split and the config identity, while the post-condition's
    message said it recognised every state a post-row-12 connection can occupy.
    """

    record = connection.record
    validated = connection.config.config.config_hash
    established = connection.sources.documents["established_result"]
    result_split = value_at_field_path(
        established,
        record.established_result.split_field_path,
        where="established_result.split_field_path",
    )
    result_config_hash = value_at_field_path(
        established,
        record.established_result.config_hash_field_path,
        where="established_result.config_hash_field_path",
    )
    audits = connection.dataset.audits
    census = manifest_census(list(connection.dataset.rows.values()))
    joins = {
        "the validated config's source_path resolves record config.relative_path": (
            Path(connection.config.config.source_path).parts[
                -len(record.config.relative_path.parts):
            ]
            == record.config.relative_path.parts
        ),
        "record config.config_hash == the validated config": (
            record.config.config_hash == validated
        ),
        "the validated config_hash == its own document's canonical digest": (
            validated == expected_config_hash(_plain(connection.config.config.document))
        ),
        "established_result split == the record's split": result_split == record.split,
        "established_result config_hash == the record's config.config_hash": (
            result_config_hash == record.config.config_hash
        ),
        "every manifest row config_hash == the validated config": all(
            row.config_hash == validated for row in connection.dataset.rows.values()
        ),
        "every named run's split == the record's split": all(
            connection.dataset.rows[arm.run_id].split == record.split
            for case in record.cases
            for arm in case.arms.values()
        ),
        "the carried census == the census recomputed from the manifest rows": (
            _plain(connection.dataset.census) == census
        ),
        "every echoed manifest_row == the authenticated manifest row": all(
            arm.manifest_row[field] == getattr(connection.dataset.rows[arm.run_id], field)
            for case in record.cases
            for arm in case.arms.values()
            for field in MANIFEST_ROW_FIELDS
        ),
        "every echoed manifest_row split == the record's split": all(
            arm.manifest_row.get("split") == record.split
            for case in record.cases
            for arm in case.arms.values()
        ),
        "every authenticated role index row's config_hash == the validated config": all(
            row.config_hash == validated
            for row in connection.roles.index_rows.values()
        ),
    }
    for name in AUDIT_NAMES:
        declared = getattr(record.data_root, name)
        joins[f"record {name}.assignment_hash == {name}.json"] = (
            declared.assignment_hash == audits[name]["assignment_hash"]
        )
        joins[f"record {name}.config_hash == {name}.json"] = (
            declared.config_hash == audits[name]["config_hash"]
        )
        joins[f"{name}.json config_hash == the validated config"] = (
            audits[name]["config_hash"] == validated
        )
        joins[f"{name}.json {MANIFEST_AUDIT_KEY} == the recomputed census"] = all(
            _plain(audits[name][MANIFEST_AUDIT_KEY])[field] == census[field]
            for field in MANIFEST_CENSUS_FIELDS
        )
    return joins


def _require_post_row12_state(
    connection: AuthenticatedConnection,
    *,
    where: str,
    split_policy_violated: bool = False,
) -> AuthenticatedConnection:
    """Return `connection` when it is a state rows 3 through 12 would have produced.

    Four separate things are required, and naming them separately is the point --
    each cross-review so far has found the one this helper's message claimed and did
    not run:

      1. every identity join `_provenance_joins` lists;
      2. row 4's *validator*, run by calling `validate_config_document` at the
         authority-appropriate `require_frozen` -- the same call `authenticate_config`
         makes, over the same document, source path and schema. This is Codex's
         Session-152 finding: the Session-152 seam ran row 4's policy and skipped row
         4's validation, and the `frozen` state it built was refused by that validator
         on the filename, the decision, the confirmatory flag, the open gates and all
         eight freeze-required paths;
      3. row 4's authority/config *policy*, run by calling
         `require_authority_config_policy` rather than restating it -- a `FINAL`
         record naming a draft config is a state row 4 refuses, and the Session-151
         seam produced exactly that one. It is kept beside the validator rather than
         folded into it because the policy is the adapter's own rule and is total over
         the 2x2 the validator does not see (finding CY's branch B);
      4. row 3's authority/split *policy*, run by calling
         `connection_record._require_authority_split_policy`, the function that owns
         the rule.

    Args:
        split_policy_violated: declares that this caller is deliberately building the
            one state row 3 forbids -- a `FINAL` record naming the `dev` split, which
            is the only way to reach row 19's split input. The flag does not skip the
            check: it *inverts* it, so a caller that sets it on a state row 3 would
            accept fails here. A declared exception nothing verifies is a bypass.

    **What this post-condition still does not claim, and it is now exactly one echo.**
    It does not require `record.config.sha256` -- the digest of the config file's
    *bytes* -- to be the digest of the document the state carries. An in-memory
    document has no byte rendering row 4 would have hashed, and computing one here
    would put an identity into the state that no read produced, which is the precise
    defect shape both Session-152 findings had. So the seam leaves that one echo
    where the harness put it, and a test pins that it is unmoved rather than
    silently re-derived.

    *** THIS REPLACES A WIDER NON-CLAIM AND THE REPLACEMENT IS THE POINT. *** Session
    152 declined the whole of row 4's validation on the ground that invariant W7
    forbids manufacturing a frozen `config.json`. Measured: `validate_config_document`
    uses `source_path` **only for its name**, so a validator-accepted frozen state
    needs no file at all, and this file has built a complete frozen fixture document
    since acceptance test B8. W7 is about what the packet contains; it was never a
    reason to skip a check that opens nothing.

    The failure is raised rather than asserted so it survives `python -O`, which this
    file's suite is deliberately re-run under.
    """

    failures = sorted(
        f"join broken: {name}"
        for name, holds in _provenance_joins(connection).items()
        if not holds
    )
    validated_config = connection.config.config
    try:
        revalidated = validate_config_document(
            _plain(validated_config.document),
            source_path=validated_config.source_path,
            schema=_plain(connection.config.schema),
            schema_path=validated_config.schema_path,
            require_frozen=connection.record.authority == FINAL,
        )
    except (ConfigContractError, ValueError, OSError) as exc:
        failures.append(f"row 4's own validator refuses the config document: {exc}")
    else:
        if revalidated.config_hash != validated_config.config_hash:
            failures.append(
                f"row 4's validator derives config_hash "
                f"{revalidated.config_hash!r} but the state carries "
                f"{validated_config.config_hash!r}"
            )
        if revalidated.status != validated_config.status:
            failures.append(
                f"row 4's validator reads status {revalidated.status!r} but the "
                f"state carries {validated_config.status!r}"
            )
    try:
        require_authority_config_policy(
            connection.record.authority, connection.config.config
        )
    except VerificationSceneError as exc:
        failures.append(f"row 4 authority/config policy refuses: {exc}")
    try:
        _require_authority_split_policy(connection.record)
    except VerificationSceneError as exc:
        if not split_policy_violated:
            failures.append(f"row 3 authority/split policy refuses: {exc}")
    else:
        if split_policy_violated:
            failures.append(
                "row 3 authority/split policy accepts, but this caller declared it "
                "deliberately violated"
            )
    if failures:
        raise AssertionError(
            f"{where} produced a state rows 3 through 12 would not have produced: "
            f"{'; '.join(failures)}"
        )
    return connection


def _reprovenanced(
    connection: AuthenticatedConnection,
    *,
    authority: str,
    split: str,
    config_status: str,
    assignment_hash: str,
    split_policy_violated: bool = False,
    config_document: Callable[[AuthenticatedConnection], Mapping[str, Any]] | None = None,
) -> AuthenticatedConnection:
    """Return the same connection re-provenanced, with every earlier-row copy moved with it.

    **The provenance identities are not a handful of fields, and each cross-review
    has found the copy the last version left behind.** Session 150's version edited
    the record's authority and split, both audit `assignment_hash` echoes and the
    validated config's hash; Codex measured that eight of the eleven joins rows 4
    through 6 establish were false in the object the row-19 tests then handed to
    `resolve_provenance`. Session 151 moved those eleven; Codex measured that the
    recomputed census, both audit census blocks, both record `manifest_row` echoes
    and all eight role-index `config_hash` values were still left behind, and that a
    `FINAL` authority over an unchanged *draft* config document is a state row 4's
    own policy refuses. Both findings are the same finding at different widths, and
    both were re-driven at source in Session 152 before being accepted.

    Session 152's version moved all eighteen of those and still built a `frozen`
    configuration by flipping one field on the *draft* document; Codex measured that
    row 4's own validator refuses it, and re-driving that here found the refusal is
    not one clause but five -- the filename, the decision, the confirmatory flag, the
    open gates and **all eight** freeze-required paths. Each generation of this seam
    has been partial in a way the previous post-condition could not see, which is why
    the post-condition now runs row 4's validator rather than approximating it.

    So every copy moves together here:

      * the config **document**. For `draft` it is the harness's own document with its
        `status` restated; for `frozen` it is `_synthetic_frozen_document`, the
        complete validator-accepted fixture this file has built since acceptance test
        B8, together with the `config.json` source path the frozen lifecycle requires.
        **No file is written for it** -- `validate_config_document` uses `source_path`
        only for its name -- so invariant W7's rule that this packet contains no
        frozen configuration is untouched;
      * the config `config_hash`, which is *re-derived* by `expected_config_hash`
        rather than supplied. That is the structural half of the repair: an identity a
        caller hands in is an identity no document produced, which is the same shape as
        the row-20 defect Codex found in the same review;
      * the record's `config.relative_path`, which follows the source path so that
        rows 3 and 4 still name one file;
      * the record's authority, split, `config.config_hash` echo, both audit
        `assignment_hash` and `config_hash` echoes, and every arm's 20-field
        `manifest_row`, rebuilt from the edited manifest row it names;
      * the established result's split and config identity at their declared field
        paths;
      * every manifest row's `config_hash` and `split`, the census recomputed from
        them, and both audits' `manifest_audit` blocks;
      * every authenticated role-index row's `config_hash`.

    The result is required to satisfy `_require_post_row12_state` before it is
    returned, so a later edit that reintroduces a partial shape fails here rather
    than passing quietly.

    Args:
        config_status: `'draft'` or `'frozen'`. It is the *document's* lifecycle
            field, and the config identity follows from it, which is why there is no
            `config_hash` parameter: a `frozen` document yields a bare 64-hex digest
            and a `draft` one the `dev-` prefixed form, exactly as
            `utils.config_contract` derives them.
        split_policy_violated: passed through to the post-condition; see its Args.
        config_document: **the negative controls' entry point, and it exists for
            nothing else.** It replaces the document this helper would have built,
            while every dependent copy below still moves coherently -- which is what
            lets a control reproduce a superseded generation's *document* without
            also reproducing that generation's broken joins, so the check the control
            is aimed at is the only one left standing. The post-condition still runs,
            and catching the substitution is its job.
    """

    validated_config = connection.config.config
    relative = connection.record.config.relative_path
    packet_root = Path(validated_config.source_path).parents[len(relative.parts) - 1]
    if config_status == "frozen":
        # The frozen lifecycle requires the name `config.json`; nothing is written
        # there, because `validate_config_document` reads `source_path` for its name
        # and never opens it.
        config_relative = PurePosixPath("config.json")
        document = _synthetic_frozen_document(
            _plain(connection.config.schema), Path(validated_config.schema_path)
        )
    else:
        config_relative = relative
        document = _plain(validated_config.document)
    if config_document is not None:
        document = _plain(config_document(connection))
    document["status"] = config_status
    document.pop("config_hash", None)
    config_hash = expected_config_hash(document)
    document["config_hash"] = config_hash
    config = replace(
        connection.config,
        config=replace(
            validated_config,
            source_path=packet_root / Path(str(config_relative)),
            document=connection_adapter._frozen(document),
            config_hash=config_hash,
            status=config_status,
        ),
    )

    rows = {
        run_id: replace(row, config_hash=config_hash, split=split)
        for run_id, row in connection.dataset.rows.items()
    }
    census = manifest_census(list(rows.values()))
    dataset = replace(
        connection.dataset,
        rows=MappingProxyType(rows),
        census=connection_adapter._frozen(census),
        audits=MappingProxyType(
            {
                name: _with_field_path_value(
                    _with_field_path_value(
                        _with_field_path_value(
                            document_,
                            MANIFEST_AUDIT_KEY,
                            connection_adapter._frozen(
                                {**_plain(document_[MANIFEST_AUDIT_KEY]), **census}
                            ),
                        ),
                        "assignment_hash",
                        assignment_hash,
                    ),
                    "config_hash",
                    config_hash,
                )
                for name, document_ in connection.dataset.audits.items()
            }
        ),
    )

    data_root = connection.record.data_root
    record = replace(
        connection.record,
        authority=authority,
        split=split,
        config=replace(
            connection.record.config,
            config_hash=config_hash,
            relative_path=config_relative,
        ),
        data_root=replace(
            data_root,
            generation_audit=replace(
                data_root.generation_audit,
                assignment_hash=assignment_hash,
                config_hash=config_hash,
            ),
            independent_audit=replace(
                data_root.independent_audit,
                assignment_hash=assignment_hash,
                config_hash=config_hash,
            ),
        ),
        cases=tuple(
            replace(
                case,
                arms=MappingProxyType(
                    {
                        suite: replace(
                            arm,
                            manifest_row=MappingProxyType(
                                {
                                    field: getattr(rows[arm.run_id], field)
                                    for field in MANIFEST_ROW_FIELDS
                                }
                            ),
                        )
                        for suite, arm in case.arms.items()
                    }
                ),
            )
            for case in connection.record.cases
        ),
    )

    established = connection.sources.documents["established_result"]
    established = _with_field_path_value(
        established, record.established_result.split_field_path, split
    )
    established = _with_field_path_value(
        established, record.established_result.config_hash_field_path, config_hash
    )
    sources = replace(
        connection.sources,
        documents=MappingProxyType(
            {**connection.sources.documents, "established_result": established}
        ),
    )

    roles = replace(
        connection.roles,
        index_rows=MappingProxyType(
            {
                key: replace(row, config_hash=config_hash)
                for key, row in connection.roles.index_rows.items()
            }
        ),
    )

    return _require_post_row12_state(
        replace(
            connection,
            record=record,
            config=config,
            sources=sources,
            dataset=dataset,
            roles=roles,
        ),
        where="_reprovenanced",
        split_policy_violated=split_policy_violated,
    )


def test_row19_resolves_the_harness_record_to_development_only(
    harness: Harness,
) -> None:
    """The accept path, and the traces it computed the state from are carried."""

    connection = harness.authenticate()
    resolved = resolve_provenance(connection)
    assert resolved.state == DEVELOPMENT_ONLY
    assert set(resolved.development_traces) == {
        "config.config_hash",
        "data_root.generation_audit.assignment_hash",
        "data_root.independent_audit.assignment_hash",
    }
    for value in resolved.development_traces.values():
        assert value.startswith(DEVELOPMENT_TRACE_PREFIX)


def test_row19_refuses_a_final_claim_over_a_development_assignment(
    harness: Harness,
) -> None:
    """Invariant W6's input set: computes `DEVELOPMENT_ONLY`, claims `FINAL`.

    **This is the one provenance fact no earlier row holds.** The config is frozen
    and clean, so row 4 is satisfied; the split is `val`, so row 3 is satisfied; and
    every digest and every echo in the chain still agrees, because `_reprovenanced`
    moves every earlier-row copy with the four identities and refuses to return a
    state in which any of the eleven joins rows 4 through 6 establish is broken. Row
    6 checks the dataset assignment for *agreement* -- record against both audits,
    and the two audits against each other -- and never for what it says. What is left
    is a `FINAL RESULT INPUTS` banner over data generated under a development
    assignment, and this row is where that refuses.
    """

    connection = harness.authenticate()
    edited = _reprovenanced(
        connection,
        authority=FINAL,
        split="val",
        config_status="frozen",
        assignment_hash=f"{DEVELOPMENT_TRACE_PREFIX}{'a' * 64}",
    )
    error = _refusal(lambda: resolve_provenance(edited))
    assert error.code == X_PROVENANCE_UNRESOLVED
    assert "claims authority FINAL" in str(error)
    assert f"computed {DEVELOPMENT_ONLY}" in str(error)
    assert "data_root.generation_audit.assignment_hash" in str(error)
    assert "data_root.independent_audit.assignment_hash" in str(error)
    assert "config.config_hash" not in str(error)


def test_row19_resolves_final_when_no_authenticated_identity_carries_a_trace(
    harness: Harness,
) -> None:
    """The accept side of the same construction, so the refusal above separates.

    Without this the refusal test would pass on an implementation that refused every
    `FINAL` claim, which is branch A -- the branch finding CY's ruling rejected.
    """

    connection = harness.authenticate()
    edited = _reprovenanced(
        connection,
        authority=FINAL,
        split="val",
        config_status="frozen",
        assignment_hash="c" * 64,
    )
    resolved = resolve_provenance(edited)
    assert resolved.state == FINAL
    assert dict(resolved.development_traces) == {}


def test_row19_names_the_split_when_no_identity_carries_a_trace(
    harness: Harness,
) -> None:
    """A `dev` split alone computes `DEVELOPMENT_ONLY`, and the message says so.

    Row 3 forbids this pairing in production (`_require_authority_split_policy`), so
    like row 13 this branch is a post-condition across a module boundary; the seam is
    what reaches it. It is kept because the split is one of the four named inputs to
    the computation and a computation with an unreachable input is a computation
    whose inputs nobody has checked.
    """

    connection = harness.authenticate()
    edited = _reprovenanced(
        connection,
        authority=FINAL,
        split="dev",
        config_status="frozen",
        assignment_hash="c" * 64,
        split_policy_violated=True,
    )
    error = _refusal(lambda: resolve_provenance(edited))
    assert error.code == X_PROVENANCE_UNRESOLVED
    assert "split = 'dev'" in str(error)


def test_row19_never_computes_the_synthetic_state(harness: Harness) -> None:
    """`SYNTHETIC_FIXTURE` belongs to the private seam and no public input reaches it.

    The private assembly seam supplies that state and never opens a connection
    record; a public invocation able to resolve to it would be a public path able to
    disclaim its own inputs. This drives both public outcomes and asserts the third
    state is not among them.
    """

    connection = harness.authenticate()
    states = {
        resolve_provenance(connection).state,
        resolve_provenance(
            _reprovenanced(
                connection,
                authority=FINAL,
                split="val",
                config_status="frozen",
                assignment_hash="c" * 64,
            )
        ).state,
    }
    assert states == {DEVELOPMENT_ONLY, FINAL}
    assert SYNTHETIC_FIXTURE not in states
    assert SYNTHETIC_FIXTURE in PROVENANCE_STATES


def test_row19_carries_a_read_only_trace_mapping(harness: Harness) -> None:
    """Nothing downstream can edit the evidence this row computed the state from."""

    resolved = resolve_provenance(harness.authenticate())
    with pytest.raises(TypeError):
        resolved.development_traces["config.config_hash"] = "x"  # type: ignore[index]


def test_row19_the_authenticated_harness_satisfies_every_earlier_row_join(
    harness: Harness,
) -> None:
    """The join set is measured against a real post-row-12 state before it is used.

    `_provenance_joins` is only worth anything if it describes the state the read
    order actually produces. This drives it against the connection rows 1 through 12
    built, so a join written down wrongly fails here rather than silently weakening
    the seam's post-condition into something the production path does not satisfy
    either.
    """

    joins = _provenance_joins(harness.authenticate())
    assert len(joins) == 19
    assert [name for name, holds in joins.items() if not holds] == []


def test_row19_the_seam_preserves_every_earlier_row_join(harness: Harness) -> None:
    """A re-provenanced connection is still a state the earlier rows would accept."""

    edited = _reprovenanced(
        harness.authenticate(),
        authority=FINAL,
        split="val",
        config_status="frozen",
        assignment_hash="c" * 64,
    )
    assert [name for name, holds in _provenance_joins(edited).items() if not holds] == []
    assert edited.record.authority == FINAL
    assert edited.record.split == "val"
    assert edited.config.config.status == "frozen"
    assert DEVELOPMENT_TRACE_PREFIX not in edited.config.config.config_hash
    assert edited.config.config.config_hash == expected_config_hash(
        _plain(edited.config.config.document)
    )
    assert edited.config.config.config_hash != harness.config_hash


def test_row19_the_seam_derives_the_config_identity_rather_than_adopting_one(
    harness: Harness,
) -> None:
    """The seam has no `config_hash` parameter, and that is the structural half of the repair.

    An identity a caller hands in is an identity no document produced -- the same
    shape as the row-20 defect the same cross-review found. Driving both lifecycle
    values here is what says the derivation is the contract's own: the draft form
    carries the `dev-` prefix and the frozen form does not, and `expected_config_hash`
    reproduces each from the document the seam actually left behind.
    """

    assert "config_hash" not in _seam_parameter_names()
    assert "config_status" in _seam_parameter_names()
    connection = harness.authenticate()
    for status, prefixed in (("frozen", False), ("draft", True)):
        edited = _reprovenanced(
            connection,
            authority=DEVELOPMENT_ONLY if prefixed else FINAL,
            split="dev" if prefixed else "val",
            config_status=status,
            assignment_hash="c" * 64,
        )
        document = _plain(edited.config.config.document)
        assert document["status"] == status
        assert edited.config.config.config_hash == expected_config_hash(document)
        assert (
            edited.config.config.config_hash.startswith(DEVELOPMENT_TRACE_PREFIX)
            is prefixed
        )


def _seam_parameter_names() -> frozenset[str]:
    """Return the keyword names `_reprovenanced` accepts."""

    return frozenset(inspect.signature(_reprovenanced).parameters)


def _session_150_partial(connection: AuthenticatedConnection) -> AuthenticatedConnection:
    """Reconstruct Session 150's re-provenancing exactly, as an input to be caught."""

    data_root = connection.record.data_root
    return replace(
        connection,
        record=replace(
            connection.record,
            authority=FINAL,
            split="val",
            data_root=replace(
                data_root,
                generation_audit=replace(
                    data_root.generation_audit, assignment_hash="c" * 64
                ),
                independent_audit=replace(
                    data_root.independent_audit, assignment_hash="c" * 64
                ),
            ),
        ),
        config=replace(
            connection.config,
            config=replace(connection.config.config, config_hash="f" * 64),
        ),
    )


def _session_151_partial(connection: AuthenticatedConnection) -> AuthenticatedConnection:
    """Reconstruct Session 151's re-provenancing exactly, as an input to be caught.

    This is the Session-150 edit plus the eleven joins that version *did* move: the
    record's own config echo, both audit `config_hash` echoes, the established
    result's two field paths, both audit documents and every manifest row's
    `config_hash` and split. What it does not touch is what Codex's Session-151
    cross-review measured as left behind -- the recomputed census, both audit census
    blocks, the record's 20-field manifest echoes, every role-index `config_hash`,
    and the config *document*, whose canonical digest still derives the original
    `dev-` identity while the scalar beside it says otherwise.
    """

    config_hash = "f" * 64
    assignment_hash = "c" * 64
    split = "val"
    data_root = connection.record.data_root
    record = replace(
        connection.record,
        authority=FINAL,
        split=split,
        config=replace(connection.record.config, config_hash=config_hash),
        data_root=replace(
            data_root,
            generation_audit=replace(
                data_root.generation_audit,
                assignment_hash=assignment_hash,
                config_hash=config_hash,
            ),
            independent_audit=replace(
                data_root.independent_audit,
                assignment_hash=assignment_hash,
                config_hash=config_hash,
            ),
        ),
    )
    established = connection.sources.documents["established_result"]
    established = _with_field_path_value(
        established, record.established_result.split_field_path, split
    )
    established = _with_field_path_value(
        established, record.established_result.config_hash_field_path, config_hash
    )
    return replace(
        connection,
        record=record,
        config=replace(
            connection.config,
            config=replace(connection.config.config, config_hash=config_hash),
        ),
        sources=replace(
            connection.sources,
            documents=MappingProxyType(
                {**connection.sources.documents, "established_result": established}
            ),
        ),
        dataset=replace(
            connection.dataset,
            rows=MappingProxyType(
                {
                    run_id: replace(row, config_hash=config_hash, split=split)
                    for run_id, row in connection.dataset.rows.items()
                }
            ),
            audits=MappingProxyType(
                {
                    name: _with_field_path_value(
                        _with_field_path_value(
                            document, "assignment_hash", assignment_hash
                        ),
                        "config_hash",
                        config_hash,
                    )
                    for name, document in connection.dataset.audits.items()
                }
            ),
        ),
    )


@pytest.mark.parametrize(
    "build, expected_broken_joins",
    [
        (_session_150_partial, 11),
        (_session_151_partial, 7),
    ],
    ids=["session-150", "session-151"],
)
def test_row19_the_seam_post_condition_refuses_a_partial_re_provenancing(
    harness: Harness,
    build: Callable[[AuthenticatedConnection], AuthenticatedConnection],
    expected_broken_joins: int,
) -> None:
    """The negative controls, and each one is a shipped defect written back as an input.

    A post-condition no input can make fail is the same defect as no post-condition at
    all -- lesson 242, on the seam that carries invariant W6's only evidence, which is
    the last place it should be allowed to happen twice. Session 150's partial edit is
    the first control and has been one since Session 151. **Session 151's own partial
    edit is the second, added here** because the joins this session added are exactly
    the ones that version left standing, and a new post-condition whose only witness
    is the *previous* generation's defect has never been shown to see the current one.

    Both are also required to fail row 4's authority/config policy, which is the half
    of a post-row-12 state the join list does not express: a `FINAL` record over an
    unedited draft config document is a state row 4 refuses outright.
    """

    partial = build(harness.authenticate())
    broken = [name for name, holds in _provenance_joins(partial).items() if not holds]
    assert len(broken) == expected_broken_joins
    with pytest.raises(AssertionError) as raised:
        _require_post_row12_state(partial, where="the negative control")
    message = str(raised.value)
    assert "the negative control" in message
    assert "row 4 authority/config policy refuses" in message
    for name in broken:
        assert name in message


def _session_152_config_document(
    connection: AuthenticatedConnection,
) -> Mapping[str, Any]:
    """Reconstruct Session 152's config document exactly, as an input to be caught.

    Session 152 built a `frozen` configuration by taking the harness's own **draft**
    document and setting one field. Everything else it moved coherently, which is why
    every join and both policies still hold over it: the only thing wrong with that
    state is that row 4's validator would never have produced it.
    """

    return {**_plain(connection.config.config.document), "status": "frozen"}


def test_row19_the_seam_post_condition_runs_row_4s_own_validator(
    harness: Harness,
) -> None:
    """The third negative control, and the first one no join and no policy can catch.

    Lesson 272 said a widened post-condition must be shown to see the *current*
    generation's defect, and this is that check applied to the widening itself. Both
    controls below leave **all nineteen joins standing and both policies accepting**,
    so a post-condition that had merely gained joins would pass them. Only the call
    into `validate_config_document` refuses, and the two controls separate its two
    halves: what the document *says*, and what the file it is read from is *named*.
    """

    connection = harness.authenticate()

    # Control A -- Session 152's own document, under the correct frozen filename.
    with pytest.raises(AssertionError) as content:
        _reprovenanced(
            connection,
            authority=FINAL,
            split="val",
            config_status="frozen",
            assignment_hash="c" * 64,
            config_document=_session_152_config_document,
        )
    message = str(content.value)
    assert "row 4's own validator refuses the config document" in message
    assert "join broken" not in message
    assert "policy refuses" not in message

    # Control B -- a genuinely frozen document under the draft filename.
    accepted = _reprovenanced(
        connection,
        authority=FINAL,
        split="val",
        config_status="frozen",
        assignment_hash="c" * 64,
    )
    misnamed = replace(
        accepted,
        config=replace(
            accepted.config,
            config=replace(
                accepted.config.config,
                source_path=Path(connection.config.config.source_path),
            ),
        ),
        record=replace(
            accepted.record,
            config=replace(
                accepted.record.config,
                relative_path=connection.record.config.relative_path,
            ),
        ),
    )
    assert [
        name for name, holds in _provenance_joins(misnamed).items() if not holds
    ] == []
    with pytest.raises(AssertionError) as named:
        _require_post_row12_state(misnamed, where="the filename control")
    assert "must be named exactly config.json" in str(named.value)
    assert "join broken" not in str(named.value)


def test_row19_the_seam_builds_a_configuration_row_4s_validator_accepts(
    harness: Harness,
) -> None:
    """The accept side of the same call, measured clause by clause rather than assumed.

    A post-condition that ran the validator and could only ever refuse would be the
    same defect as one that never ran it. So the frozen state the seam now builds is
    driven through `validate_config_document` at `require_frozen=True` here, and every
    clause the frozen lifecycle names is checked against the document independently --
    because a single accept could come from a validator that had stopped checking.

    **And nothing is written for it.** `source_path` is read for its name and never
    opened, so the frozen state exists only in memory: neither the live packet nor the
    harness's own temporary packet gains a `config.json`, which is invariant W7's rule
    and finding DD's boundary.
    """

    connection = harness.authenticate()
    edited = _reprovenanced(
        connection,
        authority=FINAL,
        split="val",
        config_status="frozen",
        assignment_hash="c" * 64,
    )
    config = edited.config.config
    document = _plain(config.document)
    schema = _plain(edited.config.schema)
    contract = schema["config_contract"]

    assert Path(config.source_path).name == "config.json"
    validated = validate_config_document(
        document,
        source_path=config.source_path,
        schema=schema,
        schema_path=config.schema_path,
        require_frozen=True,
    )
    assert validated.config_hash == config.config_hash
    assert validated.is_frozen
    assert document["decision"] == contract["frozen_decision"]
    assert document["confirmatory_payloads_allowed"] is True
    assert document["open_gates"] == []
    assert document["schema_sha256"] == _raw_digest(Path(config.schema_path))
    unresolved = [
        dotted
        for dotted in contract["freeze_required_paths"]
        if _contains_null_value(_value_at_dotted_path(document, dotted))
    ]
    assert unresolved == []
    assert len(contract["freeze_required_paths"]) == 8

    assert not (PACKET_ROOT / "config.json").exists()
    assert not (harness.packet_root / "config.json").exists()


def _value_at_dotted_path(document: Mapping[str, Any], dotted: str) -> Any:
    """Return the value one dotted config path names, or `None` when it is absent."""

    cursor: Any = document
    for segment in dotted.split("."):
        if not isinstance(cursor, Mapping) or segment not in cursor:
            return None
        cursor = cursor[segment]
    return cursor


def test_row19_the_seam_leaves_the_config_byte_digest_where_the_harness_put_it(
    harness: Harness,
) -> None:
    """The one echo the post-condition still does not establish, pinned as unmoved.

    `record.config.sha256` is the digest of the config file's *bytes*. The seam writes
    no file, so there is no byte rendering row 4 would have hashed, and computing one
    would put an identity into the state that no read produced -- the exact defect
    shape both of the Session-152 findings had. Leaving it is therefore the correct
    behaviour rather than an omission, and pinning it here is what stops a later
    session from "completing" the seam by deriving it.
    """

    connection = harness.authenticate()
    for authority, split, status, assignment in (
        (FINAL, "val", "frozen", "c" * 64),
        (DEVELOPMENT_ONLY, "dev", "draft", harness.assignment_hash),
    ):
        edited = _reprovenanced(
            connection,
            authority=authority,
            split=split,
            config_status=status,
            assignment_hash=assignment,
        )
        assert edited.record.config.sha256 == connection.record.config.sha256
        assert edited.record.config.config_hash != edited.record.config.sha256


def test_row19_the_seam_post_condition_checks_the_declared_split_violation(
    harness: Harness,
) -> None:
    """A declared exception nothing verifies is a bypass, so the flag is inverted rather than skipped.

    One row-19 test needs the one state row 3 forbids -- `FINAL` over the `dev` split
    -- because that is the only way to reach the split input of row 19's computation.
    It declares the violation, and the post-condition then *requires* the violation to
    be real. Setting the flag on a state row 3 would accept fails here.
    """

    connection = harness.authenticate()
    with pytest.raises(AssertionError) as raised:
        _reprovenanced(
            connection,
            authority=FINAL,
            split="val",
            config_status="frozen",
            assignment_hash="c" * 64,
            split_policy_violated=True,
        )
    assert "row 3 authority/split policy accepts" in str(raised.value)
    with pytest.raises(AssertionError) as undeclared:
        _reprovenanced(
            connection,
            authority=FINAL,
            split="dev",
            config_status="frozen",
            assignment_hash="c" * 64,
        )
    assert "row 3 authority/split policy refuses" in str(undeclared.value)


def test_row19_the_seam_field_path_setter_refuses_a_path_it_cannot_write(
    harness: Harness,
) -> None:
    """A setter that quietly writes nothing would rebuild the defect it repairs."""

    established = harness.authenticate().sources.documents["established_result"]
    with pytest.raises(AssertionError) as raised:
        _with_field_path_value(established, "read.absent.deeper", "x")
    assert "read.absent" in str(raised.value)


# -- row 20 ------------------------------------------------------------------ #
#
# **The reachability boundary Session 151 measured here is closed, and how it was
# closed is the part to keep.** `utils.verification_scene.validate_bundle` requires a
# menu to carry at least one `structure`, one `actuator` and one `sensor` case. The
# contract fixture writes exactly two C1/S pairs -- one `dev` pair whose labels are
# `healthy` and one `val` pair whose labels are `structure` -- and read-order row 6
# refuses a run whose split is not the record's, so the `val` pair cannot enter a
# `dev` record's menu at all. No menu that tree can build satisfies the surface gate,
# which is why Session 151 shipped this row with its accept path and its two identity
# refusals untested and the boundary written down here.
#
# **The repair was a fixture, never a rule change**, and `_three_case_menu` below is
# it: three additional `dev` pairs whose `labels` and `estimator_outputs` payloads
# carry `structure`, `actuator` and `sensor` coherently, installed over the harness
# tree and removed byte for byte on exit. A menu that cannot show a reader all three
# source classes side by side cannot support the comparison the whole artifact exists
# to let a reader make, so relaxing the gate to reach green would have been a repair
# to the wrong object.
def _resolved(harness: Harness, arguments: Mapping[str, Any]):
    """Drive rows 1 through 19 and return everything row 20 takes."""

    connection = authenticate_connection(**arguments)
    cases = resolve_cases(connection)
    return (
        connection,
        cases,
        resolve_geometry(connection, cases),
        resolve_provenance(connection),
    )


# -- the three-case coherent menu, which is what makes row 20's accept path reachable #
#
# **This is a fixture, not a rule change, and the distinction is the whole reason it
# exists.** The surface gate refuses a menu that cannot show a reader a structure, an
# actuator and a sensor change side by side, and that refusal is correct: such a menu
# cannot support the comparison the artifact exists to let a reader make. The contract
# fixture cannot build one -- its only `dev` pair is `healthy` -- so the repair is a
# menu that satisfies the gate, built here rather than in
# `scripts/build_data_contract_fixture.py`, whose two-pair / four-run census is pinned
# by closed tests.
#
# **What it installs, and what it deliberately reuses.** Three additional `dev` pairs,
# each carrying the *same* coherent plant record row 18 needs, its own `labels` payload
# naming one required source class, and an `estimator_outputs` payload whose `p_class`
# names that same class. `controller_logs` is copied byte for byte from the pair the
# contract fixture already wrote, because nothing in it is per-case and rows 15 to 17
# already accept it. `observations` is not written at all: `ROLE_NAMES` is
# `controller_logs`, `estimator_outputs`, `labels`, `plant`, so no connection record
# names an observation payload and none is opened.
#
# **Every byte it writes is restored on exit** -- the manifest, both audits, the six
# affected role indexes and the established-result artifact are saved and rewritten,
# and every created payload, checkpoint and directory is removed.

#: The three menu entries: case id, pair id, source class, label subtype, location,
#: severity, seed and display label. The display labels must stay distinct, because
#: `validate_bundle` refuses duplicates and the interactive surface keys on them.
MENU_CASES: tuple[tuple[str, str, str, str, int, float, int, str], ...] = (
    (
        "menu-structure",
        "menu_structure",
        "structure",
        "link_stiffness_loss",
        2,
        0.50,
        301,
        "Soften link 2 by 50%",
    ),
    (
        "menu-actuator",
        "menu_actuator",
        "actuator",
        "actuator_torque_loss",
        1,
        0.40,
        401,
        "Weaken actuator 1 by 40%",
    ),
    (
        "menu-sensor",
        "menu_sensor",
        "sensor",
        "encoder_bias",
        0,
        0.30,
        501,
        "Bias encoder 1",
    ),
)

#: The four roles a connection record names, split by whether the schema-E layout
#: qualifies their directory by suite. Taken from the module that owns each fact.
_MENU_FLAT_ROLES = tuple(role for role in ROLE_NAMES if role not in SUITE_QUALIFIED_ROLES)
_MENU_SUITE_ROLES = tuple(role for role in ROLE_NAMES if role in SUITE_QUALIFIED_ROLES)


def _menu_manifest_row(
    pair_id: str, suite: str, source_class: str, seed: int, config_hash: str
) -> IdentityManifestRow:
    """Return one schema-A manifest row for a menu pair, on the `dev` split."""

    return IdentityManifestRow(
        schema_version="1.0",
        config_hash=config_hash,
        scenario_spec_id="scenario_dev",
        pair_id=pair_id,
        run_id=f"{pair_id}_{suite}",
        trajectory_spec_id="trajectory_dev",
        fault_setting_id=f"{source_class}_menu",
        split_group_id="group_dev",
        split=SPLIT,
        suite=suite,
        estimator_id="fixture_estimator_v1",
        controller_id="fixture_controller_v1",
        payload_id=f"payload_{pair_id}",
        env_profile_id="fixture_env",
        contact_profile_id="no_contact",
        sim_seed=seed,
        fault_seed=seed + 1,
        sensor_seed=seed + 2,
        controller_seed=seed + 3,
        train_seed=0,
    )


def _menu_label_payload(
    source_class: str, subtype: str, location: int, severity: float
) -> dict[str, np.ndarray]:
    """Return one schema-D label payload naming the case's source class."""

    onset_index = FIXTURE_N_STEPS // 3
    return {
        "source_class": np.asarray(source_class),
        "subtype": np.asarray(subtype),
        "location": np.asarray(location, dtype=np.int64),
        "severity": np.asarray(severity, dtype=np.float64),
        "onset_index": np.asarray(onset_index, dtype=np.int64),
        "onset_time_s": np.asarray(
            onset_index / FIXTURE_F_CTRL_HZ, dtype=np.float64
        ),
        "compound_flag": np.asarray(False, dtype=np.bool_),
        "ood_flag": np.asarray(False, dtype=np.bool_),
    }


def _menu_estimator_payload(
    source_class: str, step: int, decision_time_s: float
) -> dict[str, np.ndarray]:
    """Return one decision whose `p_class` names the same class the labels do.

    The coherence is the point: a menu whose estimator payloads all named one class
    while the labels named three would satisfy the surface gate and show a reader
    three identical panels.
    """

    probabilities = np.zeros((1, len(SOURCE_CLASS_ORDER)), dtype=np.float64)
    probabilities[0, SOURCE_CLASS_ORDER.index(source_class)] = 1.0
    return {
        "step": np.asarray([step], dtype=np.int64),
        "decision_time_s": np.asarray([decision_time_s], dtype=np.float64),
        "p_class": probabilities,
        "unknown_score": np.asarray([0.0], dtype=np.float64),
        "abstain_decision": np.asarray([False], dtype=np.bool_),
        "location_out": np.asarray([-1], dtype=np.int64),
        "severity_out": np.asarray([0.0], dtype=np.float64),
        "severity_uncertainty": np.asarray([np.inf], dtype=np.float64),
        "detection_time_s": np.asarray([decision_time_s], dtype=np.float64),
    }


def _menu_arm(harness: Harness, row: Any, suite: str) -> dict[str, Any]:
    """Return one record arm for a menu pair, digesting what is on disk now."""

    roles: dict[str, Any] = {}
    for role in ROLE_NAMES:
        directory = role_root_for(harness.role_root, role, suite)
        relative = (
            f"{role}/{suite}/{row.run_id}.npz"
            if role in SUITE_QUALIFIED_ROLES
            else f"{role}/{row.run_id}.npz"
        )
        roles[role] = {
            "index_sha256": external_digest(directory / ROLE_INDEX_NAME),
            "payload_relative_path": relative,
            "payload_sha256": external_digest(harness.role_root / relative),
        }
    checkpoint = harness.checkpoint_root / row.pair_id / f"{suite}.pt"
    return {
        "checkpoint": {
            "relative_path": f"{row.pair_id}/{suite}.pt",
            "sha256": external_digest(checkpoint),
        },
        "manifest_row": {name: getattr(row, name) for name in MANIFEST_ROW_FIELDS},
        "roles": roles,
        "run_id": row.run_id,
    }


@contextmanager
def _three_case_menu(
    harness: Harness,
    *,
    seed: int = 0,
    tolerance_m: float = CENTERLINE_TASK_OUTPUT_TOL_M,
    edit_document: Callable[[dict], dict] | None = None,
):
    """Install a complete structure/actuator/sensor menu, then restore every byte.

    *** THE CONNECTION RECORD IS PART OF "EVERY BYTE", AND IT WAS NOT UNTIL SESSION
    153. *** Codex's Session-152 review measured that this installer rewrote the
    record and restored everything the record *names*, so the state it left behind
    declared the temporary established-result digest against the restored artifact.
    Re-driven at source: the post-exit record does not merely go stale, it is
    **refused** -- `authenticate_connection` raises `X_IDENTITY_MISMATCH` on
    `established_result.sha256`. The autouse `_restored_record` fixture repaired that
    only at the end of the whole test, so a context manager whose docstring promised a
    restored tree handed back a tree no read order accepts. The record is in `saved`
    now, and the same repair is applied to this file's two other installers.

    Args:
        edit_document: given the assembled record document, returns the one to write.
            Used to drive row 20's identity refusals, which need a record whose menu
            the surface gate accepts before the identity check is reached at all.
    """

    config = load_config(
        harness.packet_root / CONFIG_RELATIVE, harness.packet_root / SCHEMA_RELATIVE
    )
    schema = json.loads(
        (harness.packet_root / SCHEMA_RELATIVE).read_text(encoding="utf-8")
    )
    geometry, coherent, validation = _coherent_geometry_and_record(
        harness, seed, tolerance_m
    )
    plant_payload = dict(coherent.__dict__)
    decision_step = FIXTURE_N_STEPS - 1
    decision_time_s = float(np.asarray(coherent.t_s)[-1])

    manifest_path = harness.role_root / MANIFEST_NAME
    validation_path = harness.packet_root / GEOMETRY_RELATIVE
    result_path = harness.packet_root / RESULT_RELATIVE
    touched = [
        harness.role_root / role / ROLE_INDEX_NAME for role in _MENU_FLAT_ROLES
    ]
    touched += [
        harness.role_root / role / suite / ROLE_INDEX_NAME
        for role in _MENU_SUITE_ROLES
        for suite in SUITE_KEYS
    ]
    touched += [harness.role_root / f"{name}.json" for name in AUDIT_NAMES]

    saved = [
        (path, path.read_bytes())
        for path in [
            manifest_path,
            validation_path,
            result_path,
            harness.record_path,
            *touched,
        ]
    ]
    created: list[Path] = []

    try:
        _write_json(validation_path, validation)
        geometry = replace(
            geometry,
            tolerance_source=replace(
                geometry.tolerance_source, sha256=tracked_text_digest(validation_path)
            ),
        )

        rows = read_identity_manifest(manifest_path)
        menu_rows: dict[str, Any] = {}
        for case_id, pair_id, source_class, subtype, location, severity, seed_, _ in (
            MENU_CASES
        ):
            for suite in SUITE_KEYS:
                row = _menu_manifest_row(
                    pair_id, suite, source_class, seed_, config.config_hash
                )
                menu_rows[row.run_id] = row
                rows.append(row)
        write_identity_manifest(manifest_path, rows)

        census = manifest_census(rows)
        for name in AUDIT_NAMES:
            _write_json(
                harness.role_root / f"{name}.json",
                _audit_document(
                    status=harness.audit_status[name],
                    assignment_hash=harness.assignment_hash,
                    config_hash=harness.config_hash,
                    census=census,
                ),
            )

        new_index_rows: dict[Path, list[Any]] = {}
        for case_id, pair_id, source_class, subtype, location, severity, _, _ in (
            MENU_CASES
        ):
            for suite in SUITE_KEYS:
                row = menu_rows[f"{pair_id}_{suite}"]
                payloads = {
                    "plant": plant_payload,
                    "labels": _menu_label_payload(
                        source_class, subtype, location, severity
                    ),
                    "estimator_outputs": _menu_estimator_payload(
                        source_class, decision_step, decision_time_s
                    ),
                }
                for role in ROLE_NAMES:
                    directory = role_root_for(harness.role_root, role, suite)
                    path = directory / f"{row.run_id}.npz"
                    if role == "controller_logs":
                        source = directory / f"{PAIR_ID}_{suite}.npz"
                        path.write_bytes(source.read_bytes())
                    else:
                        normalized = validate_role_payload(
                            role, payloads[role], schema, config
                        )
                        buffer = io.BytesIO()
                        np.savez(buffer, **normalized)
                        path.write_bytes(buffer.getvalue())
                    created.append(path)
                    new_index_rows.setdefault(
                        directory / ROLE_INDEX_NAME, []
                    ).append(
                        RoleIndexRow(
                            run_id=row.run_id,
                            schema_version="1.0",
                            config_hash=config.config_hash,
                            npz_path=f"{row.run_id}.npz",
                            sha256=external_digest(path),
                        )
                    )
                checkpoint = harness.checkpoint_root / pair_id / f"{suite}.pt"
                checkpoint.parent.mkdir(parents=True, exist_ok=True)
                checkpoint.write_bytes(
                    f"inert-menu-checkpoint-{pair_id}-{suite}".encode("utf-8")
                )
                created.append(checkpoint)

        for index_path, extra in new_index_rows.items():
            existing = read_role_index(index_path, observation=False)
            write_role_index(index_path, [*existing, *extra], observation=False)

        case_ids = [case_id for case_id, *_ in MENU_CASES]
        _write_json(
            result_path,
            {
                "read": {
                    "cases": case_ids,
                    "config_hash": harness.config_hash,
                    "split": SPLIT,
                },
                "status": "synthetic_fixture_established_result",
            },
        )

        # `_record_document` re-digests the manifest, both audits and every source
        # artifact from what is on disk at the moment it is called, so the rewritten
        # files above are picked up rather than restated here.
        document = harness._record_document()
        document["render_geometry"] = render_geometry_document(geometry)
        document["cases"] = [
            {
                "arms": {
                    suite: _menu_arm(harness, menu_rows[f"{pair_id}_{suite}"], suite)
                    for suite in SUITE_KEYS
                },
                "case_id": case_id,
                "display_label": display_label,
                "pair_id": pair_id,
            }
            for case_id, pair_id, _, _, _, _, _, display_label in MENU_CASES
        ]
        if edit_document is not None:
            document = edit_document(document)
        yield harness.rewrite_record(document)
    finally:
        for path in created:
            path.unlink(missing_ok=True)
        for _, pair_id, *_ in MENU_CASES:
            directory = harness.checkpoint_root / pair_id
            if directory.exists() and not any(directory.iterdir()):
                directory.rmdir()
        for path, raw in saved:
            path.write_bytes(raw)


def test_row20_refuses_a_series_sequence_that_is_not_the_record_s_menu(
    harness: Harness,
) -> None:
    """`resolve_cases` and `resolve_geometry` are separate calls, so the pairing is an input.

    A caller holding two connections can hand this row the series of one and the
    geometry of the other, and no earlier row can see it: each of them saw only its
    own output. That is why the agreement is a check here and not an assumption.
    """

    with _coherent_geometry(harness) as arguments:
        connection, cases, geometry, provenance = _resolved(harness, arguments)
    relabelled = AuthenticatedCases(
        cases=(replace(cases.cases[0], case_id="not-the-menu"),)
    )
    error = _refusal(
        lambda: resolve_bundle(connection, relabelled, geometry, provenance)
    )
    assert error.code == X_BUNDLE_INCOMPLETE
    assert "not-the-menu" in str(error)
    assert "one connection has one menu" in str(error)


def test_row20_refuses_a_geometry_sequence_that_is_not_the_record_s_menu(
    harness: Harness,
) -> None:
    """The same seam, on the other side of it."""

    with _coherent_geometry(harness) as arguments:
        connection, cases, geometry, provenance = _resolved(harness, arguments)
    relabelled = AuthenticatedGeometry(
        tolerance_m=geometry.tolerance_m,
        cases=(replace(geometry.cases[0], case_id="not-the-menu"),),
    )
    error = _refusal(
        lambda: resolve_bundle(connection, cases, relabelled, provenance)
    )
    assert error.code == X_BUNDLE_INCOMPLETE
    assert "not-the-menu" in str(error)


def test_row20_refuses_a_menu_the_established_result_does_not_declare(
    harness: Harness,
) -> None:
    """Row 6 bound the established result to the record's menu; this binds it to the bundle.

    The two comparisons are about different objects. An assembly that dropped,
    duplicated or reordered a case would satisfy row 6 -- which never sees the
    assembly -- and fail here.
    """

    with _coherent_geometry(harness) as arguments:
        connection, cases, geometry, provenance = _resolved(harness, arguments)
    reordered = replace(
        connection,
        sources=replace(
            connection.sources, established_cases=(CASE_ID, "a-second-case")
        ),
    )
    error = _refusal(
        lambda: resolve_bundle(reordered, cases, geometry, provenance)
    )
    assert error.code == X_BUNDLE_INCOMPLETE
    assert "a-second-case" in str(error)
    assert "the prior read established" in str(error)


@pytest.mark.parametrize("forged", [FINAL, SYNTHETIC_FIXTURE])
def test_row20_refuses_a_provenance_state_the_connection_did_not_resolve(
    harness: Harness, forged: str
) -> None:
    """Codex's Session-151 finding, and the measurement that says the check belongs here.

    `provenance` is a separately constructible value and `_scene_for` puts its state
    on every scene as the banner the surface draws. This drives the whole shape: the
    harness record's authenticated authority is `DEVELOPMENT_ONLY`, a forged
    `ResolvedProvenance` is built beside it, and the scene that forgery produces is
    shown to be one `validate_scene` **accepts** -- so nothing downstream of the
    assembly can see the disagreement, because by then the label is the only statement
    of the fact. `resolve_bundle` refuses it, with row 19's own code and before the
    surface gate the one-case harness would otherwise stop at.

    `SYNTHETIC_FIXTURE` is in the parametrization because it is the state invariant V7
    says a public connection-record invocation must never resolve to, and it is
    refused here as a consequence of the same equality rather than as a special case:
    `utils.connection_record` admits only the two public authorities, so no
    authenticated record can make it hold.
    """

    with _coherent_geometry(harness) as arguments:
        connection, cases, geometry, provenance = _resolved(harness, arguments)
    assert connection.record.authority == DEVELOPMENT_ONLY
    assert provenance.state == DEVELOPMENT_ONLY
    lie = ResolvedProvenance(state=forged, development_traces={})

    forged_scene = connection_adapter._scene_for(
        connection,
        connection.record.cases[0],
        cases.cases[0],
        geometry.cases[0],
        lie.state,
    )
    validate_scene(forged_scene)
    assert forged_scene.provenance.state == forged

    error = _refusal(lambda: resolve_bundle(connection, cases, geometry, lie))
    assert error.code == X_PROVENANCE_UNRESOLVED
    assert forged in str(error)
    assert DEVELOPMENT_ONLY in str(error)
    assert "never a value supplied beside it" in str(error)
    assert "structure/actuator/sensor" not in str(error)


def test_row20_binds_the_provenance_state_before_it_builds_any_scene(
    harness: Harness,
) -> None:
    """The banner is checked before the assembly runs, not after it.

    A scene carrying a state the record did not resolve must not exist even
    transiently inside this module, because the next row writes what this one built.
    The observer counts `_scene_for` calls: the accept path builds one per case and
    the forged path builds none.
    """

    with _coherent_geometry(harness) as arguments:
        connection, cases, geometry, provenance = _resolved(harness, arguments)
    calls: list[str] = []
    original = connection_adapter._scene_for

    def counted(*args: Any, **kwargs: Any):
        calls.append(args[1].case_id)
        return original(*args, **kwargs)

    connection_adapter._scene_for = counted  # type: ignore[assignment]
    try:
        _refusal(
            lambda: resolve_bundle(
                connection,
                cases,
                geometry,
                ResolvedProvenance(state=FINAL, development_traces={}),
            )
        )
        assert calls == []
        _refusal(lambda: resolve_bundle(connection, cases, geometry, provenance))
        assert calls == [CASE_ID]
    finally:
        connection_adapter._scene_for = original  # type: ignore[assignment]


def test_row20_refuses_a_menu_the_surface_gate_will_not_draw(harness: Harness) -> None:
    """The surface gate is called here, and today it is what the harness's menu meets.

    This is the end-to-end statement of the reachability boundary above: rows 1
    through 19 all accept, the assembly builds a scene that
    `utils.verification_scene.validate_scene` accepts, and the *menu* is refused
    because one `healthy` case cannot show a reader a structure, an actuator and a
    sensor change side by side. The refusal is the surface gate's own, re-raised
    untouched: this row assigns no second code to a rule another module owns.
    """

    with _coherent_geometry(harness) as arguments:
        connection, cases, geometry, provenance = _resolved(harness, arguments)
    error = _refusal(
        lambda: resolve_bundle(connection, cases, geometry, provenance)
    )
    assert error.code == X_BUNDLE_INCOMPLETE
    assert "structure/actuator/sensor" in str(error)
    for name in ("structure", "actuator", "sensor"):
        assert name in str(error)


def test_row20_assembles_a_scene_the_scene_gate_accepts(harness: Harness) -> None:
    """The per-case assembly is exercised even though the menu gate refuses the set.

    `_scene_for` is the whole of this row's construction work, and it is reachable
    today: `validate_scene` is what a scene must pass and it is a different gate from
    the menu-completeness rule that blocks the bundle. Driving it here means the
    assembly's field-by-field mapping -- centerline from row 18, series from rows 13
    to 17, identities from the record, state from row 19 -- is measured now rather
    than only when the three-case harness lands.
    """

    with _coherent_geometry(harness) as arguments:
        connection, cases, geometry, provenance = _resolved(harness, arguments)
    scene = connection_adapter._scene_for(
        connection,
        connection.record.cases[0],
        cases.cases[0],
        geometry.cases[0],
        provenance.state,
    )
    validate_scene(scene)
    assert scene.provenance.state == provenance.state
    assert scene.provenance.connection_record_sha256 == arguments[
        "connection_record_sha256"
    ]
    assert scene.provenance.connection_record_id == connection.record.record_label
    assert scene.provenance.config_identity == connection.record.config.config_hash
    assert scene.provenance.split == connection.record.split
    assert scene.body_change.case_id == CASE_ID
    assert scene.truth is cases.cases[0].truth
    assert scene.n_frames == cases.cases[0].playback_t_s.shape[0]
    for suite in SUITE_KEYS:
        declared = connection.record.cases[0].arms[suite]
        identity = scene.provenance.arms[suite]
        assert identity.run_id == declared.run_id
        assert identity.pair_id == connection.record.cases[0].pair_id
        assert identity.checkpoint_sha256 == declared.checkpoint.sha256
        assert dict(identity.role_payload_sha256) == {
            role: declared.roles[role].payload_sha256 for role in ROLE_NAMES
        }
        assert np.array_equal(
            scene.arms[suite].centerline_xy, geometry.cases[0].arms[suite].centerline
        )


def test_the_three_case_menu_is_the_menu_the_surface_gate_asks_for(
    harness: Harness,
) -> None:
    """The fixture's own accept side, driven before anything is claimed about row 20.

    A fixture that quietly failed to satisfy the gate would make every test below it
    pass for the wrong reason, so what the gate actually requires -- one case per
    required source class, distinct display labels -- is measured here against the
    authenticated record rather than assumed from how the tree was written.
    """

    with _three_case_menu(harness) as arguments:
        connection = authenticate_connection(**arguments)
        cases = resolve_cases(connection)
    assert [case.case_id for case in connection.record.cases] == [
        case_id for case_id, *_ in MENU_CASES
    ]
    assert {series.truth.source_class for series in cases.cases} == set(
        REQUIRED_SOURCE_CLASSES
    )
    labels = [series.display_label for series in cases.cases]
    assert len(set(labels)) == len(labels)
    for series in cases.cases:
        for suite in SUITE_KEYS:
            decisions = series.arms[suite].decisions
            assert len(decisions) == 1
            index = SOURCE_CLASS_ORDER.index(series.truth.source_class)
            assert float(np.asarray(decisions[0].p_class)[index]) == 1.0


def test_the_three_case_menu_restores_every_byte_it_touched(harness: Harness) -> None:
    """The fixture writes into a session-scoped tree, so its restoration is a property.

    `_coherent_geometry` restores four files; this installer rewrites the manifest,
    both audits, six role indexes and the established-result artifact, and creates
    twelve payloads and six checkpoints. A leak there would not fail here -- it would
    quietly change what every later test in this file is measuring. So the whole of
    both trees is digested before and after, path by path, and required to be equal.

    *** THE CONNECTION RECORD IS IN THE COMPARISON AND NOTHING IS REPAIRED BY HAND. ***
    Until Session 153 this snapshot excluded `harness.record_path` and then called
    `harness.restore_record()` before checking it, which proved that the *manual*
    restoration method works and said nothing about the property the context manager's
    own docstring claims. That is Codex's Session-152 finding, and the exclusion was
    the reason no test could see it.
    """

    def snapshot() -> dict[str, str]:
        return {
            str(path.relative_to(harness.root)): external_digest(path)
            for root in (harness.packet_root, harness.role_root, harness.checkpoint_root)
            for path in sorted(root.rglob("*"))
            if path.is_file()
        }

    before = snapshot()
    with _three_case_menu(harness) as arguments:
        during = snapshot()
        assert authenticate_connection(**arguments) is not None
    after = snapshot()
    assert during != before
    assert set(during) - set(before)
    assert during[str(harness.record_path.relative_to(harness.root))] != before[
        str(harness.record_path.relative_to(harness.root))
    ]
    assert after == before
    assert external_digest(harness.record_path) == harness.record_sha256


def test_every_installer_leaves_a_record_the_read_order_still_accepts(
    harness: Harness,
) -> None:
    """The sharp form of Codex's Session-152 finding, driven over all three installers.

    Each of this file's context managers rewrites the connection record and then
    restores the files that record *names*. Before Session 153 none of them restored
    the record itself, so what each one handed back was not a stale record but a
    **refused** one: the record still declared the digests of the temporary artifacts
    while those artifacts had been put back. Measured against the Session-152 bytes,
    the exit was `X_IDENTITY_MISMATCH` on `established_result.sha256`.

    The autouse `_restored_record` fixture repaired that only after the whole test
    finished, which is why a leak was invisible inside one. This drives the property
    the installers now carry -- exit leaves a tree the read order accepts -- rather
    than comparing a digest, because accepting is the thing the tree is for.
    """

    accepted = harness.record_sha256
    connection = harness.authenticate()
    key = _payload_key(CASE_ID, "S", "labels")
    payload = dict(connection.roles.payloads[key])
    payload["severity"] = np.asarray(0.25, dtype=np.float64)

    installers = (
        ("_rewritten_payload", lambda: _rewritten_payload(
            harness, "labels", "S", f"{PAIR_ID}_S", payload
        )),
        ("_coherent_geometry", lambda: _coherent_geometry(harness)),
        ("_three_case_menu", lambda: _three_case_menu(harness)),
    )
    for name, open_installer in installers:
        with open_installer() as arguments:
            assert arguments["connection_record_sha256"] != accepted, name
        assert external_digest(harness.record_path) == accepted, name
        assert authenticate_connection(**harness.arguments()) is not None, name


def test_row20_accepts_the_three_case_menu_and_returns_one_bundle(
    harness: Harness,
) -> None:
    """Row 20's accept path, reachable for the first time.

    Everything this row exists to assemble is measured here: one scene per declared
    case, filed under the case id the record names, every scene carrying the state row
    19 resolved and the record digest rows 1 and 2 authenticated, and the whole bundle
    passing the gate both surfaces run before they draw anything.
    """

    with _three_case_menu(harness) as arguments:
        connection, cases, geometry, provenance = _resolved(harness, arguments)
        bundle = resolve_bundle(connection, cases, geometry, provenance)

    declared = [case_id for case_id, *_ in MENU_CASES]
    assert list(bundle.scenes) == declared
    assert bundle.provenance_state == DEVELOPMENT_ONLY
    assert bundle.bundle_version == connection_adapter.BUNDLE_VERSION
    validate_bundle(bundle)
    for case_id, scene in bundle.scenes.items():
        assert scene.body_change.case_id == case_id
        assert scene.provenance.state == DEVELOPMENT_ONLY
        assert scene.provenance.connection_record_sha256 == arguments[
            "connection_record_sha256"
        ]
        assert scene.provenance.split == SPLIT
    assert {
        scene.body_change.change.source_class for scene in bundle.scenes.values()
    } == set(REQUIRED_SOURCE_CLASSES)


def test_row20_refuses_an_arm_run_id_the_record_does_not_name(
    harness: Harness,
) -> None:
    """The first identity refusal, reachable now that a menu can pass the surface gate.

    `_arm_identity` reads the record, so the only way the presented run can differ
    from the declared one is a defect in this row's own assembly. The check is driven
    by patching that one function, which is the same shape the delegation tests in
    `utils.verification_scene` use: the guard is a post-condition over this module's
    construction, and a post-condition is tested by breaking the construction.
    """

    with _three_case_menu(harness) as arguments:
        connection, cases, geometry, provenance = _resolved(harness, arguments)
        original = connection_adapter._arm_identity

        def relabelled(case: Any, suite: str):
            identity = original(case, suite)
            return replace(identity, run_id="not-the-declared-run")

        connection_adapter._arm_identity = relabelled  # type: ignore[assignment]
        try:
            error = _refusal(
                lambda: resolve_bundle(connection, cases, geometry, provenance)
            )
        finally:
            connection_adapter._arm_identity = original  # type: ignore[assignment]
    assert error.code == X_BUNDLE_INCOMPLETE
    assert "not-the-declared-run" in str(error)
    assert "but the record names" in str(error)


def test_row20_refuses_an_arm_pair_id_the_record_does_not_name(
    harness: Harness,
) -> None:
    """The second identity refusal, on the other field of the same block."""

    with _three_case_menu(harness) as arguments:
        connection, cases, geometry, provenance = _resolved(harness, arguments)
        original = connection_adapter._arm_identity

        def relabelled(case: Any, suite: str):
            identity = original(case, suite)
            return replace(identity, pair_id="not-the-declared-pair")

        connection_adapter._arm_identity = relabelled  # type: ignore[assignment]
        try:
            error = _refusal(
                lambda: resolve_bundle(connection, cases, geometry, provenance)
            )
        finally:
            connection_adapter._arm_identity = original  # type: ignore[assignment]
    assert error.code == X_BUNDLE_INCOMPLETE
    assert "not-the-declared-pair" in str(error)
    assert "is presented under pair" in str(error)


def test_row20_refuses_a_menu_the_established_result_orders_differently(
    harness: Harness,
) -> None:
    """The ordered comparison, which only a menu with more than one case can separate.

    With one case the established-result check could not tell an ordered comparison
    from an unordered one. Three cases can: the same set in a different order is the
    input that separates them, and menu order is what a reader is shown.
    """

    with _three_case_menu(harness) as arguments:
        connection, cases, geometry, provenance = _resolved(harness, arguments)
    declared = tuple(case.case_id for case in connection.record.cases)
    reordered = replace(
        connection,
        sources=replace(
            connection.sources,
            established_cases=(declared[1], declared[0], declared[2]),
        ),
    )
    error = _refusal(lambda: resolve_bundle(reordered, cases, geometry, provenance))
    assert error.code == X_BUNDLE_INCOMPLETE
    assert "in that order" in str(error)


def test_row20_carries_the_authenticated_record_digest_rather_than_a_second_read(
    harness: Harness,
) -> None:
    """The provenance identity is the digest the chain checked, not a later measurement.

    A provenance block a caller supplies is a provenance block that can lie (V7), and
    a digest re-taken at assembly time is a statement about the file as it is then,
    not about the bytes rows 1 and 2 authenticated.
    """

    connection = harness.authenticate()
    assert connection.record_sha256 == harness.record_sha256
    assert "record_sha256" in {
        field.name for field in dataclass_fields(AuthenticatedConnection)
    }


# -- row 21 ------------------------------------------------------------------ #
#
# **Row 21 is the first row that writes anything, and it is the last row of the read
# order.** Everything above it authenticates, resolves or assembles; this one creates
# `<output-dir>/<record_label>/` exclusively and publishes the declared set into it.
# The scripted figure writer is injected rather than imported, because
# `render_verification_scene` is the entry point that calls *into* the adapter and
# because it is the only module on this surface that imports matplotlib -- so the
# tests below drive both the real writer and a stub, and one test pins the stub
# against the real one so the refusal tests are not measuring a fiction.


def _scripted_writer():
    """Return the packet's own scripted figure writer, under a headless backend."""

    import matplotlib

    matplotlib.use("Agg")
    from render_verification_scene import render_bundle

    return render_bundle


def _png_chunk(kind: bytes, body: bytes) -> bytes:
    """Return one length-prefixed, CRC-suffixed PNG chunk."""

    import zlib

    return (
        len(body).to_bytes(4, "big")
        + kind
        + body
        + zlib.crc32(kind + body).to_bytes(4, "big")
    )


def _stub_png(pixels_per_metre: int | None) -> bytes:
    """Return a real one-pixel PNG, optionally without its `pHYs` chunk."""

    import zlib

    chunks = [
        _png_chunk(
            b"IHDR",
            (1).to_bytes(4, "big") + (1).to_bytes(4, "big") + bytes([8, 0, 0, 0, 0]),
        )
    ]
    if pixels_per_metre is not None:
        chunks.append(
            _png_chunk(
                b"pHYs",
                pixels_per_metre.to_bytes(4, "big") * 2 + bytes([1]),
            )
        )
    chunks.append(_png_chunk(b"IDAT", zlib.compress(b"\x00\x00")))
    chunks.append(_png_chunk(b"IEND", b""))
    return connection_adapter._PNG_SIGNATURE + b"".join(chunks)


_STUB_PIXELS_PER_METRE = round(
    connection_adapter.REQUIRED_FIGURE_DPI / connection_adapter._METRES_PER_INCH
)


def _malformed_png(kind: str) -> bytes:
    """Return a figure that is malformed in exactly one way.

    Every case here is a file whose resolution claim cannot be believed, and each one
    is a separate reason: the chunk carrying the claim is corrupt, the file stops
    inside it, the header lies about how long it is, something is appended after the
    datastream ends, or the file states its resolution twice. Codex's Session-153
    review drove the first two through the previous parser: one was **accepted** as
    300-DPI evidence and the other escaped as a raw `IndexError`.

    **The second group is structure rather than integrity, and it is Codex's
    Session-154 finding 3.** Every one of those cases has valid chunk bounds and valid
    CRCs and is still not a figure: no image header, two of them, a header of the wrong
    fixed length, no image data at all, a resolution declared after the image data the
    format requires it to precede, an interrupted `IDAT` run, and a non-empty `IEND`.
    Measured before the repair, `signature + pHYs + IEND` returned `(11811, 11811)`
    while a strict decoder refused the same bytes as `UnidentifiedImageError`; my own
    re-drive added the no-`IDAT` and `pHYs`-after-`IDAT` cases, which were accepted
    too.

    **The third group is the image itself, and it is Codex's Session-155 finding 2.**
    Ordered, CRC-valid chunks still are not a decodable image. Measured before the
    repair: a zero-width `IHDR` and an `IDAT` body reading `not-a-zlib-stream` were
    both **accepted** at `(11811, 11811)` while a strict decoder refused both, and my
    re-drive widened that to a zero *height*, a colour type the format does not define,
    a compression method it does not define, and a zlib-valid stream carrying three
    bytes for a sixteen-pixel image. *** THE COMPRESSION-METHOD CASE IS THE ONE TO KEEP:
    a lenient decoder ACCEPTED it, so the standard applied here is the format and not a
    decoder's willingness to guess. ***
    """

    import zlib

    signature = connection_adapter._PNG_SIGNATURE
    header = _png_chunk(
        b"IHDR",
        (1).to_bytes(4, "big") + (1).to_bytes(4, "big") + bytes([8, 0, 0, 0, 0]),
    )
    body = _STUB_PIXELS_PER_METRE.to_bytes(4, "big") * 2 + bytes([1])
    phys = _png_chunk(b"pHYs", body)
    tail = _png_chunk(b"IDAT", zlib.compress(b"\x00\x00")) + _png_chunk(b"IEND", b"")
    if kind == "corrupt-phys-crc":
        corrupt = phys[:-4] + bytes(byte ^ 0xFF for byte in phys[-4:])
        return signature + header + corrupt + tail
    if kind == "truncated-phys-body":
        return signature + header + (9).to_bytes(4, "big") + b"pHYs" + bytes([7])
    if kind == "truncated-chunk-header":
        return signature + header + b"\x00\x00\x00"
    if kind == "length-overruns-the-file":
        return signature + header + (4096).to_bytes(4, "big") + b"pHYs" + body
    if kind == "trailing-bytes":
        return signature + header + phys + tail + b"appended\n"
    if kind == "two-phys-chunks":
        return signature + header + phys + phys + tail
    if kind == "wrong-phys-length":
        return signature + header + _png_chunk(b"pHYs", body + b"\x00") + tail
    if kind == "non-metre-unit":
        return signature + header + _png_chunk(b"pHYs", body[:8] + bytes([0])) + tail
    data = _png_chunk(b"IDAT", zlib.compress(b"\x00\x00"))
    end = _png_chunk(b"IEND", b"")
    if kind == "no-image-header":
        return signature + phys + end
    if kind == "second-image-header":
        return signature + header + header + phys + tail
    if kind == "wrong-image-header-length":
        return (
            signature
            + _png_chunk(
                b"IHDR",
                (1).to_bytes(4, "big") + (1).to_bytes(4, "big") + bytes([8, 0, 0, 0]),
            )
            + phys
            + tail
        )
    if kind == "no-image-data":
        return signature + header + phys + end
    if kind == "resolution-after-the-image-data":
        return signature + header + data + phys + end
    if kind == "interrupted-image-data":
        return (
            signature
            + header
            + phys
            + data
            + _png_chunk(b"tEXt", b"key\x00value")
            + data
            + end
        )
    if kind == "non-empty-iend":
        return signature + header + phys + data + _png_chunk(b"IEND", b"x")

    def headed(width: int, height: int, *, fields: bytes) -> bytes:
        return signature + _png_chunk(
            b"IHDR", width.to_bytes(4, "big") + height.to_bytes(4, "big") + fields
        ) + phys + tail

    if kind == "zero-width-image":
        return headed(0, 1, fields=bytes([8, 0, 0, 0, 0]))
    if kind == "zero-height-image":
        return headed(1, 0, fields=bytes([8, 0, 0, 0, 0]))
    if kind == "undefined-colour-type":
        return headed(1, 1, fields=bytes([8, 7, 0, 0, 0]))
    if kind == "undefined-bit-depth-for-the-colour-type":
        return headed(1, 1, fields=bytes([2, 2, 0, 0, 0]))
    if kind == "undefined-compression-method":
        return headed(1, 1, fields=bytes([8, 0, 1, 0, 0]))
    if kind == "undefined-filter-method":
        return headed(1, 1, fields=bytes([8, 0, 0, 1, 0]))
    if kind == "undefined-interlace-method":
        return headed(1, 1, fields=bytes([8, 0, 0, 0, 2]))
    if kind == "image-data-that-is-not-a-zlib-stream":
        return (
            signature
            + header
            + phys
            + _png_chunk(b"IDAT", b"not-a-zlib-stream")
            + end
        )
    if kind == "image-data-of-the-wrong-length":
        return (
            signature
            + header
            + phys
            + _png_chunk(b"IDAT", zlib.compress(b"\x00\x00\x00"))
            + end
        )
    if kind == "image-data-shorter-than-the-declared-image":
        return (
            signature
            + header
            + phys
            + _png_chunk(b"IDAT", zlib.compress(b"\x00"))
            + end
        )
    if kind == "bytes-appended-after-the-image-stream":
        return (
            signature
            + header
            + phys
            + _png_chunk(b"IDAT", zlib.compress(b"\x00\x00") + b"GARBAGE")
            + end
        )
    if kind == "image-stream-that-never-ends":
        return (
            signature
            + header
            + phys
            + _png_chunk(b"IDAT", zlib.compress(b"\x00\x00")[:-2])
            + end
        )
    raise AssertionError(f"unknown malformed-PNG case {kind!r}")


def _stub_writer(
    *,
    extra_file: str | None = None,
    omit_case: str | None = None,
    bundle_bytes: Callable[[bytes], bytes] | None = None,
    digest_text: Callable[[str], str] | None = None,
    scene_bytes: Callable[[bytes], bytes] | None = None,
    png: bytes | None = None,
    report_edit: Callable[[dict], dict] | None = None,
    subdirectory: str | None = None,
):
    """Return a writer that publishes the declared set, with one property perturbed.

    Every keyword breaks exactly one of the things row 21 checks, so each refusal test
    below names the single property it is about. With no keyword the writer is the
    faithful one, and `test_row21_the_stub_writer_publishes_what_the_real_writer_does`
    is what says so.
    """

    def write(bundle: VerificationBundle, destination: Path) -> dict[str, Any]:
        text = canonical_bundle_text(bundle)
        raw = text.encode("utf-8")
        if bundle_bytes is not None:
            raw = bundle_bytes(raw)
        (destination / connection_adapter.BUNDLE_JSON_NAME).write_bytes(raw)
        digest = external_bytes_digest(raw)
        rendered_digest = digest if digest_text is None else digest_text(digest)
        (destination / connection_adapter.BUNDLE_DIGEST_NAME).write_bytes(
            f"{rendered_digest}\n".encode("utf-8")
        )
        cases: list[dict[str, Any]] = []
        for case_id, scene in bundle.scenes.items():
            if case_id == omit_case:
                continue
            scene_raw = canonical_scene_text(scene).encode("utf-8")
            if scene_bytes is not None:
                scene_raw = scene_bytes(scene_raw)
            (destination / f"{case_id}.json").write_bytes(scene_raw)
            (destination / f"{case_id}.png").write_bytes(
                _stub_png(_STUB_PIXELS_PER_METRE) if png is None else png
            )
            cases.append(
                {
                    "case_id": case_id,
                    "frame": 0,
                    "png": f"{case_id}.png",
                    "scene_json": f"{case_id}.json",
                }
            )
        if extra_file is not None:
            (destination / extra_file).write_bytes(b"unnamed\n")
        if subdirectory is not None:
            (destination / subdirectory).mkdir()
        report = {
            "bundle_version": bundle.bundle_version,
            "provenance_state": bundle.provenance_state,
            "bundle_json": connection_adapter.BUNDLE_JSON_NAME,
            "bundle_sha256": external_bytes_digest(raw),
            "save_dpi": connection_adapter.REQUIRED_FIGURE_DPI,
            "cases": cases,
        }
        return report if report_edit is None else report_edit(report)

    return write


@contextmanager
def _publication_root(harness: Harness):
    """Yield the exclusive-create destination, and remove the tree afterwards.

    The harness is session-scoped, so a publication left behind would make every later
    row-21 test refuse at the exclusive create rather than exercise what it is named
    for. The entry assertion is what turns a leak into a failure at its own site.
    """

    root = harness.output_dir / RECORD_LABEL
    assert not root.exists(), f"a previous test left {root} behind"
    try:
        yield root
    finally:
        shutil.rmtree(root, ignore_errors=True)


def _published(harness: Harness, writer, *, arguments: Mapping[str, Any]):
    """Drive rows 1 through 20 and hand row 21 the assembled bundle."""

    connection, cases, geometry, provenance = _resolved(harness, arguments)
    bundle = resolve_bundle(connection, cases, geometry, provenance)
    return connection, bundle, write_bundle(connection, bundle, render=writer)


def test_row21_publishes_exactly_the_declared_set_with_the_packets_own_writer(
    harness: Harness,
) -> None:
    """The accept path, driven end to end through the real scripted writer.

    This is the only row that puts anything on disk, so what is asserted here is the
    published tree itself rather than a return value: the two fixed bundle files and
    one scene document plus one figure per declared case, in the record's order, with
    the digest file naming the bundle document beside it and every figure carrying the
    resolution section 4.7 requires.
    """

    declared = [case_id for case_id, *_ in MENU_CASES]
    with _publication_root(harness) as root:
        with _three_case_menu(harness) as arguments:
            connection, bundle, written = _published(
                harness, _scripted_writer(), arguments=arguments
            )
        assert written.output_root == root
        assert written.cases == tuple(declared)
        assert written.figure_dpi == connection_adapter.REQUIRED_FIGURE_DPI
        assert written.file_names == tuple(
            sorted(
                [*connection_adapter.BUNDLE_FILE_NAMES]
                + [f"{case_id}{suffix}" for case_id in declared for suffix in (".json", ".png")]
            )
        )
        assert len(written.file_names) == 8
        published = sorted(path.name for path in root.rglob("*"))
        assert published == list(written.file_names)

        bundle_path = root / connection_adapter.BUNDLE_JSON_NAME
        assert bundle_path.read_bytes() == canonical_bundle_text(bundle).encode("utf-8")
        assert external_digest(bundle_path) == written.bundle_sha256
        assert (root / connection_adapter.BUNDLE_DIGEST_NAME).read_text(
            encoding="utf-8"
        ) == f"{written.bundle_sha256}\n"
        for case_id in declared:
            assert (root / f"{case_id}.json").read_bytes() == canonical_scene_text(
                bundle.scenes[case_id]
            ).encode("utf-8")
            horizontal, vertical = connection_adapter._png_pixels_per_metre(
                (root / f"{case_id}.png").read_bytes(), where=f"{case_id}.png"
            )
            assert horizontal == vertical == _STUB_PIXELS_PER_METRE
        assert connection.record.authority == DEVELOPMENT_ONLY


def test_row21_the_stub_writer_publishes_what_the_real_writer_does(
    harness: Harness,
) -> None:
    """The stub the refusal tests use is bound to the real writer, not trusted beside it.

    A refusal test whose writer differs from the shipped one in some *other* way than
    the property under test measures nothing about the shipped path. So the two are
    driven over the same bundle here and compared where they are supposed to agree:
    the file set, the report's identity fields, the published bundle and scene bytes,
    and the resolution each figure declares. The figure *content* is not compared --
    the stub draws nothing, and drawing is the renderer's own tested property.
    """

    with _three_case_menu(harness) as arguments:
        connection, cases, geometry, provenance = _resolved(harness, arguments)
        bundle = resolve_bundle(connection, cases, geometry, provenance)

    with _publication_root(harness) as root:
        root.mkdir(parents=True)
        real_report = _scripted_writer()(bundle, root)
        real_names = sorted(path.name for path in root.rglob("*"))
        real_bundle = (root / connection_adapter.BUNDLE_JSON_NAME).read_bytes()
        real_scenes = {
            case_id: (root / f"{case_id}.json").read_bytes() for case_id in bundle.scenes
        }
        real_resolution = {
            case_id: connection_adapter._png_pixels_per_metre(
                (root / f"{case_id}.png").read_bytes(), where=f"{case_id}.png"
            )
            for case_id in bundle.scenes
        }

    with _publication_root(harness) as root:
        root.mkdir(parents=True)
        stub_report = _stub_writer()(bundle, root)
        assert sorted(path.name for path in root.rglob("*")) == real_names
        assert (root / connection_adapter.BUNDLE_JSON_NAME).read_bytes() == real_bundle
        assert {
            case_id: (root / f"{case_id}.json").read_bytes() for case_id in bundle.scenes
        } == real_scenes
        assert {
            case_id: connection_adapter._png_pixels_per_metre(
                (root / f"{case_id}.png").read_bytes(), where=f"{case_id}.png"
            )
            for case_id in bundle.scenes
        } == real_resolution

    for field in ("bundle_version", "provenance_state", "bundle_json", "bundle_sha256", "save_dpi"):
        assert stub_report[field] == real_report[field], field
    assert [case["case_id"] for case in stub_report["cases"]] == [
        case["case_id"] for case in real_report["cases"]
    ]


def test_row21_refuses_a_second_run_at_the_same_record_label(
    harness: Harness,
) -> None:
    """Invariant W10, and the half of it that matters is what survives the refusal.

    An exclusive create that refused *after* touching the destination would make a
    second run destroy the first publication, which is the state the invariant exists
    to forbid. So the first tree is digested file by file, the second run is driven,
    and the tree is required to be byte-identical afterwards -- and the writer is a
    counting stub, so the refusal is also shown to happen before the writer is reached
    at all.
    """

    calls: list[Path] = []

    def counting(bundle: VerificationBundle, destination: Path) -> dict[str, Any]:
        calls.append(destination)
        return _stub_writer()(bundle, destination)

    with _publication_root(harness) as root:
        with _three_case_menu(harness) as arguments:
            _published(harness, counting, arguments=arguments)
            assert len(calls) == 1
            before = {
                path.name: external_digest(path) for path in sorted(root.rglob("*"))
            }
            connection, cases, geometry, provenance = _resolved(harness, arguments)
            bundle = resolve_bundle(connection, cases, geometry, provenance)
            error = _refusal(
                lambda: write_bundle(connection, bundle, render=counting)
            )
        assert error.code == X_PROVENANCE_UNRESOLVED
        assert "already exists" in str(error)
        assert len(calls) == 1
        assert {
            path.name: external_digest(path) for path in sorted(root.rglob("*"))
        } == before


@pytest.mark.parametrize(
    "writer_kwargs, code, fragment",
    [
        (
            {"extra_file": "notes.txt"},
            X_BUNDLE_INCOMPLETE,
            "writes exactly the declared",
        ),
        (
            {"omit_case": MENU_CASES[1][0]},
            X_BUNDLE_INCOMPLETE,
            "writes exactly the declared",
        ),
        (
            {"subdirectory": "figures"},
            X_BUNDLE_INCOMPLETE,
            "the declared output set is flat",
        ),
        (
            {"bundle_bytes": lambda raw: raw + b"\n"},
            X_BUNDLE_INCOMPLETE,
            "not the canonical rendering of the menu",
        ),
        (
            {"digest_text": lambda digest: "0" * 64},
            X_BUNDLE_INCOMPLETE,
            "does not hold the digest of the bundle document",
        ),
        (
            {"scene_bytes": lambda raw: raw.replace(b"structure", b"actuator", 1)},
            X_BUNDLE_INCOMPLETE,
            "not the canonical rendering of the scene",
        ),
        (
            {"png": b"not a png at all\n"},
            X_BUNDLE_INCOMPLETE,
            "does not begin with the PNG signature",
        ),
        ({"png": _stub_png(None)}, X_BUNDLE_INCOMPLETE, "carries no pHYs chunk"),
        ({"png": _stub_png(2000)}, X_BUNDLE_INCOMPLETE, "pixels per metre"),
        (
            {"png": _malformed_png("corrupt-phys-crc")},
            X_BUNDLE_INCOMPLETE,
            "does not cover its own bytes",
        ),
        (
            {"png": _malformed_png("truncated-phys-body")},
            X_BUNDLE_INCOMPLETE,
            "into a chunk header",
        ),
        (
            {"report_edit": lambda report: {**report, "save_dpi": 150}},
            X_BUNDLE_INCOMPLETE,
            "section 4.7 requires",
        ),
        (
            {"report_edit": lambda report: {**report, "bundle_sha256": "e" * 64}},
            X_IDENTITY_MISMATCH,
            "the writer's reported bundle_sha256",
        ),
        (
            {"report_edit": lambda report: {**report, "provenance_state": FINAL}},
            X_IDENTITY_MISMATCH,
            "the writer's reported provenance_state",
        ),
        (
            {"report_edit": lambda report: {**report, "cases": report["cases"][::-1]}},
            X_BUNDLE_INCOMPLETE,
            "in that order",
        ),
    ],
    ids=[
        "extra-file",
        "missing-case",
        "subdirectory",
        "bundle-bytes",
        "digest-file",
        "scene-bytes",
        "not-a-png",
        "no-phys-chunk",
        "wrong-resolution",
        "corrupt-phys-crc",
        "truncated-phys-body",
        "reported-dpi",
        "reported-digest",
        "reported-state",
        "reported-order",
    ],
)
def test_row21_refuses_every_way_an_injected_writer_can_disagree_with_it(
    harness: Harness,
    writer_kwargs: dict,
    code: str,
    fragment: str,
) -> None:
    """The injected writer is checked, never trusted -- one case per thing row 21 knows.

    Codex's Session-151 and Session-152 findings were one fault at two sites: a value
    reaching a checked object from beside it rather than from inside it. An injected
    writer is that same seam by construction, so every field of its report and every
    byte it leaves behind is compared against something this row derived itself, and
    each row of this table breaks exactly one of those comparisons.
    """

    with _publication_root(harness):
        with _three_case_menu(harness) as arguments:
            connection, cases, geometry, provenance = _resolved(harness, arguments)
            bundle = resolve_bundle(connection, cases, geometry, provenance)
            error = _refusal(
                lambda: write_bundle(
                    connection, bundle, render=_stub_writer(**writer_kwargs)
                )
            )
    assert error.code == code
    assert fragment in str(error)


def test_row21_writes_nothing_outside_the_root_row_3_bound(harness: Harness) -> None:
    """The destination is row 3's, and row 21 resolves nothing of its own.

    The output root is `<output-dir>/<record_label>/` under the authority's own parent,
    and the packet ignore rule covers the development parent (W9). This asserts the
    root row 21 created is that bound path, that it sits under the development parent,
    and that the whole packet tree gained nothing but the eight declared files.
    """

    def snapshot() -> set[str]:
        return {
            str(path.relative_to(harness.packet_root))
            for path in harness.packet_root.rglob("*")
            if path.is_file()
        }

    with _publication_root(harness) as root:
        with _three_case_menu(harness) as arguments:
            connection, cases, geometry, provenance = _resolved(harness, arguments)
            bundle = resolve_bundle(connection, cases, geometry, provenance)
            before = snapshot()
            written = write_bundle(connection, bundle, render=_stub_writer())
        assert written.output_root == Path(connection.bound.output_root)
        assert written.output_root.parent == harness.output_dir
        assert written.output_root.name == connection.record.record_label
        gained = snapshot() - before
        assert gained == {
            str((root / name).relative_to(harness.packet_root))
            for name in written.file_names
        }


def test_row21_refuses_a_bound_root_that_is_not_named_for_the_record_label(
    harness: Harness,
) -> None:
    """A post-condition over row 3's own binding, driven by breaking that binding.

    Row 3 binds the output root to `record_label`; row 21 is the row that would create
    it. Restating the check here is not duplication -- it is the last point at which a
    destination that stopped being the label's own can be refused before a directory
    exists, and the guard is driven by substituting the bound value rather than by
    trusting that row 3 always agrees with it.

    This is one of the two directions the destination equality separates on, and
    `test_row21_refuses_a_destination_under_the_wrong_parent` is the other. Until
    Session 154 only this one was checked, and the check was a basename comparison, so
    the other direction was accepted and populated.
    """

    with _three_case_menu(harness) as arguments:
        connection, cases, geometry, provenance = _resolved(harness, arguments)
        bundle = resolve_bundle(connection, cases, geometry, provenance)
        moved = replace(
            connection,
            bound=replace(
                connection.bound,
                output_root=harness.output_dir / "some-other-label",
            ),
        )
        error = _refusal(lambda: write_bundle(moved, bundle, render=_stub_writer()))
    assert error.code == X_PROVENANCE_UNRESOLVED
    assert "is not the destination this connection fixes" in str(error)
    assert not (harness.output_dir / "some-other-label").exists()


# --------------------------------------------------------------------------- #
# Row 21, second pass -- the two seams Codex's Session-153 review measured.
#
# Both findings are the shape this review keeps returning: a value that reaches a
# checked object from *beside* it rather than from inside it. Row 21 takes two such
# values -- the `bundle` and the `BoundPaths` inside the connection -- and a third
# arrives as bytes the injected writer left on disk. The tests below drive each of
# them, and the PNG table drives the file-level one at its own function so a
# malformed figure is refused rather than trusted or raised over.
# --------------------------------------------------------------------------- #

#: One substitution per field of `Provenance`, each producing a value this connection
#: did not authenticate. The table is required to be total by the test below it: a
#: field added to that dataclass has to arrive here, or the coverage test fails.
_PROVENANCE_SUBSTITUTIONS: dict[str, Callable[[Any], Any]] = {
    "state": lambda value: FINAL,
    "connection_record_id": lambda value: "some-other-record",
    "connection_record_sha256": lambda value: "0" * 64,
    "config_identity": lambda value: "dev-0000000000000000",
    "config_sha256": lambda value: "1" * 64,
    "split": lambda value: "val",
    "roles_read": lambda value: tuple(reversed(value)),
    "arms": lambda value: MappingProxyType(
        {SUITE_KEYS[0]: value[SUITE_KEYS[1]], SUITE_KEYS[1]: value[SUITE_KEYS[0]]}
    ),
    "fixture_seed": lambda value: 7,
}


def _rebuilt(bundle: VerificationBundle, case_id: str, provenance: Provenance):
    """Return the bundle with one case's provenance block replaced.

    The result is a value no chain produced, which is the point: row 21 receives the
    bundle as a parameter, so a bundle nothing assembled is exactly what a caller can
    hand it.
    """

    scenes = dict(bundle.scenes)
    scenes[case_id] = replace(scenes[case_id], provenance=provenance)
    return replace(bundle, scenes=connection_adapter._frozen_mapping(scenes))


def test_the_provenance_substitution_table_covers_every_provenance_field() -> None:
    """The binding is total, and this is what makes that claim checkable.

    Row 21 compares the published provenance against the assembled one by walking
    `Provenance`'s own fields, so the code needs no maintenance when the dataclass
    grows. The table above is written by hand, so it does. This test is the join
    between the two: a new field with no substitution fails here rather than passing
    silently with one fewer case than it looks like it has.
    """

    assert set(_PROVENANCE_SUBSTITUTIONS) == {
        field.name for field in dataclass_fields(Provenance)
    }


@pytest.mark.parametrize("field_name", sorted(_PROVENANCE_SUBSTITUTIONS))
def test_row21_binds_every_field_of_the_provenance_block_it_publishes(
    harness: Harness, field_name: str
) -> None:
    """No field of a published scene's provenance may be one this chain did not build.

    The provenance block is the whole of what a reader is told the picture is made of,
    and by the time it is on disk it is the only statement of those facts. So it is
    compared against `_provenance_for` -- the same function row 20 assembles with --
    field by field, before the output root exists.
    """

    with _publication_root(harness) as root:
        with _three_case_menu(harness) as arguments:
            connection, cases, geometry, provenance = _resolved(harness, arguments)
            bundle = resolve_bundle(connection, cases, geometry, provenance)
            case_id = MENU_CASES[0][0]
            original = bundle.scenes[case_id].provenance
            substituted = replace(
                original,
                **{
                    field_name: _PROVENANCE_SUBSTITUTIONS[field_name](
                        getattr(original, field_name)
                    )
                },
            )
            forged = _rebuilt(bundle, case_id, substituted)
            error = _refusal(
                lambda: write_bundle(connection, forged, render=_stub_writer())
            )
        assert error.code == X_IDENTITY_MISMATCH
        assert f"provenance {field_name} " in str(error)
        assert not root.exists()


def test_row21_refuses_a_bundle_assembled_under_a_different_connection(
    harness: Harness,
) -> None:
    """Two genuine connections, one bundle -- the finding, driven exactly as reported.

    *** THIS IS CODEX'S SESSION-153 FINDING 1, AND NOTHING ABOUT IT IS SYNTHETIC. ***
    Both connections are authenticated by the production entry point over the same
    tree, both carry `DEVELOPMENT_ONLY` authority and the same three-case menu, and
    they differ only in the record label and therefore in the record digest. Rows 13
    through 20 run under the first; row 21 is handed the result together with the
    second. Before this session it published: every scene identified connection A
    while the tree was named for connection B, and a reader would have had no way to
    see it.

    The second record is written to *its own* tracked location, because row 3 requires
    a record labelled `L` to be presented from `record_relative_path(L)`; a record
    that skipped that would be refused four rows earlier and would measure nothing
    about this one.
    """

    other_label = f"{RECORD_LABEL}-b"
    other_path = harness.packet_root / record_relative_path(other_label)
    other_root = harness.output_dir / other_label
    with _publication_root(harness) as root:
        with _three_case_menu(harness) as arguments:
            first, cases, geometry, provenance = _resolved(harness, arguments)
            bundle = resolve_bundle(first, cases, geometry, provenance)
            document = copy.deepcopy(
                json.loads(harness.record_path.read_text(encoding="utf-8"))
            )
            document["record_label"] = other_label
            try:
                digest = _write_record(other_path, document)
                second = authenticate_connection(
                    **{
                        **arguments,
                        "connection_record_path": other_path,
                        "connection_record_sha256": digest,
                    }
                )
                assert second.record.record_label != first.record.record_label
                assert second.record_sha256 != first.record_sha256
                assert second.record.authority == first.record.authority
                assert tuple(case.case_id for case in second.record.cases) == tuple(
                    case.case_id for case in first.record.cases
                )
                error = _refusal(
                    lambda: write_bundle(second, bundle, render=_stub_writer())
                )
            finally:
                other_path.unlink(missing_ok=True)
                shutil.rmtree(other_root, ignore_errors=True)
    assert error.code == X_IDENTITY_MISMATCH
    assert "connection_record_id" in str(error)
    assert not root.exists()
    assert not other_root.exists()


def test_row21_refuses_a_destination_under_the_wrong_parent(harness: Harness) -> None:
    """The basename is right and the place is wrong -- the other half of finding 1.

    The previous check compared `output_root.name` against the record label, so a
    correct label under any parent at all was accepted; the existing refusal test
    moves the basename and therefore could not see it. Row 21 now re-derives the whole
    destination from the authenticated authority, the authenticated record label and
    the one packet root invariant W8 names, and requires the bound value to equal it.
    """

    wrong_parent = harness.root / "wrong-parent"
    with _three_case_menu(harness) as arguments:
        connection, cases, geometry, provenance = _resolved(harness, arguments)
        bundle = resolve_bundle(connection, cases, geometry, provenance)
        moved = replace(
            connection,
            bound=replace(
                connection.bound,
                output_root=wrong_parent / connection.record.record_label,
            ),
        )
        error = _refusal(lambda: write_bundle(moved, bundle, render=_stub_writer()))
    assert error.code == X_PROVENANCE_UNRESOLVED
    assert "is not the destination this connection fixes" in str(error)
    assert not wrong_parent.exists()


def test_row21_refuses_a_menu_that_is_not_the_records(harness: Harness) -> None:
    """A bundle covering the wrong cases is refused, and is no longer a `KeyError`.

    The published file set is derived from the record's menu, so a bundle missing a
    case used to reach the scene loop and index `bundle.scenes` with a case id it does
    not hold. That is a raw exception rather than a named refusal, and it is the same
    class of hole as the PNG parser's: an index taken before the thing indexed was
    proved to be there.
    """

    with _publication_root(harness) as root:
        with _three_case_menu(harness) as arguments:
            connection, cases, geometry, provenance = _resolved(harness, arguments)
            bundle = resolve_bundle(connection, cases, geometry, provenance)
            scenes = dict(bundle.scenes)
            del scenes[MENU_CASES[-1][0]]
            short = replace(
                bundle, scenes=connection_adapter._frozen_mapping(scenes)
            )
            error = _refusal(
                lambda: write_bundle(connection, short, render=_stub_writer())
            )
        assert error.code == X_BUNDLE_INCOMPLETE
        assert "the menu that is published is the menu that was authenticated" in str(
            error
        )
        assert not root.exists()


def test_row21_refuses_a_bundle_version_this_module_does_not_assemble(
    harness: Harness,
) -> None:
    """The version a reader is shown is the one this chain writes, not one handed in."""

    with _publication_root(harness) as root:
        with _three_case_menu(harness) as arguments:
            connection, cases, geometry, provenance = _resolved(harness, arguments)
            bundle = resolve_bundle(connection, cases, geometry, provenance)
            error = _refusal(
                lambda: write_bundle(
                    connection,
                    replace(bundle, bundle_version="slot8-verification-bundle-v9.9"),
                    render=_stub_writer(),
                )
            )
        assert error.code == X_BUNDLE_INCOMPLETE
        assert "but this module assembles" in str(error)
        assert not root.exists()


def test_row21_refuses_a_bundle_state_that_is_not_the_authenticated_authority(
    harness: Harness,
) -> None:
    """Row 20 binds the state it is handed; row 21 binds the state it publishes.

    The two are separate objects at separate seams. Row 20's check is about the
    `ResolvedProvenance` a caller supplies it; this one is about the assembled bundle
    that arrives here, which row 20 need never have produced.
    """

    with _publication_root(harness) as root:
        with _three_case_menu(harness) as arguments:
            connection, cases, geometry, provenance = _resolved(harness, arguments)
            bundle = resolve_bundle(connection, cases, geometry, provenance)
            error = _refusal(
                lambda: write_bundle(
                    connection,
                    replace(bundle, provenance_state=FINAL),
                    render=_stub_writer(),
                )
            )
        assert error.code == X_PROVENANCE_UNRESOLVED
        assert "authenticated authority" in str(error)
        assert not root.exists()


# --------------------------------------------------------------------------- #
# B3 -- one refusal case per row of section 4.1, stated as a property of this file.
# --------------------------------------------------------------------------- #
def test_b3_every_row_this_sub_step_owns_has_a_committed_refusal_case() -> None:
    """B3's completeness, written as an artifact property rather than an audit count.

    Sub-step 4b-ii-b owns rows 13 through 21, and B3 asks for one driven refusal per
    row. A count taken in a session is that session's private number and disappears
    with it; this reads the committed test names out of the module itself, so a row
    that later loses its last refusal case turns this red instead of leaving a hole
    nobody is looking for.

    **It is a floor, not a census.** Naming a test `test_rowNN_refuses_...` is the
    convention this file has used since row 13 was built, and this requires the
    convention to have been followed at least once per row. It cannot see a refusal
    test written under some other name, so it under-counts rather than over-counts --
    which is the direction a completeness floor has to err in.
    """

    owned = range(13, 22)
    names = [name for name in globals() if name.startswith("test_row")]
    assert names, "the naming convention this reads would then be gone"
    missing = [
        row
        for row in owned
        if not any(name.startswith(f"test_row{row}_refuses") for name in names)
    ]
    assert missing == [], f"rows with no committed refusal case: {missing}"


# --------------------------------------------------------------------------- #
# B2 -- the accept-side census.
#
# Every refusal test in this file says what one row rejects. None of them says the row
# *produced* anything, and a chain of rows that all refuse correctly and establish
# nothing would satisfy the whole refusal set. B2 is the other half: one pass through
# rows 1 to 21 over the coherent three-case menu, asserting each applicable row's own
# output. It is deliberately one test rather than twenty-one, because what it claims is
# that the rows compose -- that each one's output is the next one's input on a single
# run -- and twenty-one separate tests would each re-establish the chain and none of
# them would claim that.
# --------------------------------------------------------------------------- #
def test_b2_every_applicable_row_of_section_4_1_produces_its_own_output(
    harness: Harness,
) -> None:
    """The accept-side pass that makes the refusal set mean something.

    Row by row, on one run: the record identity rows 1 and 2 authenticated; the paths
    row 3 bound, including the destination row 21 will insist on; the schema and config
    digests row 4 took before parsing either; the source artifacts row 5 resolved; the
    manifest census and both audits row 6 agreed on; the role indexes, payload set and
    checkpoint digests rows 7 to 12 established; the two-arm series rows 13 to 17 agreed
    about; the centerlines row 18 derived; the state row 19 computed; the menu row 20
    assembled; and the tree row 21 published.

    **Rows 1 to 12 are asserted through the value they produced rather than re-driven**,
    because `authenticate_connection` is their one composition and driving them
    separately here would be a second composition -- exactly what
    `test_the_entry_point_is_the_only_composition_of_the_read_order` exists to forbid.

    Row 13 is the one row with nothing to assert on the accept side beyond the shape
    rows 14 to 17 depend on, and that is by construction rather than by omission: it
    cannot fail on the production path, which is written down rather than hidden.
    """

    declared = [case_id for case_id, *_ in MENU_CASES]
    with _publication_root(harness) as root:
        with _three_case_menu(harness) as arguments:
            connection = authenticate_connection(**arguments)

            # Rows 1-2: the record, and the identity the chain authenticated.
            assert connection.record.record_label == RECORD_LABEL
            assert connection.record_sha256 == arguments["connection_record_sha256"]
            assert connection.record.authority == DEVELOPMENT_ONLY
            assert [case.case_id for case in connection.record.cases] == declared

            # Row 3: every declared path bound under its own root.
            bound = connection.bound
            assert bound.packet_root == harness.packet_root.resolve()
            assert bound.record_path == (
                harness.packet_root
                / Path(*record_relative_path(RECORD_LABEL).parts)
            ).resolve()
            assert bound.output_root == root.resolve()
            assert bound.role_root.name == DATASET_LABEL
            assert set(bound.role_payloads) and set(bound.checkpoints)
            assert connection.expected_opens

            # Row 4: schema and config, each digested before either was parsed.
            assert connection.config.schema_sha256 == tracked_text_digest(
                harness.packet_root / SCHEMA_RELATIVE
            )
            assert connection.config.config_sha256 == tracked_text_digest(
                harness.packet_root / CONFIG_RELATIVE
            )
            assert connection.config.config.config_hash.startswith(
                DEVELOPMENT_TRACE_PREFIX
            )

            # Row 5: the source artifacts, and the two numbers row 18 later needs.
            assert connection.sources.established_cases == tuple(declared)
            assert connection.sources.geometry_producer_sha256 == tracked_text_digest(
                harness.packet_root / PRODUCER_RELATIVE
            )
            assert connection.sources.maximum_deviation_m <= DISTAL_TOLERANCE_M

            # Row 6: the manifest, its census, and both audits echoing it.
            assert connection.dataset.rows
            assert set(connection.dataset.audits) == set(AUDIT_NAMES)
            for audit in connection.dataset.audits.values():
                block = audit[MANIFEST_AUDIT_KEY]
                for field in MANIFEST_CENSUS_FIELDS:
                    observed = block[field]
                    expected = connection.dataset.census[field]
                    if isinstance(expected, (list, tuple)):
                        assert list(observed) == list(expected), field
                    else:
                        assert observed == expected, field

            # Rows 7-12: exactly the named payload set, loaded and hash-checked.
            expected_keys = {
                (case.case_id, suite, role)
                for case in connection.record.cases
                for suite in SUITE_KEYS
                for role in ROLE_NAMES
            }
            assert set(connection.roles.payloads) == expected_keys
            assert set(connection.roles.index_rows) == expected_keys
            assert set(connection.roles.checkpoint_sha256) == {
                (case.case_id, suite)
                for case in connection.record.cases
                for suite in SUITE_KEYS
            }

            # Rows 13-17: both arms, one grid, decisions inside it, one window.
            cases = resolve_cases(connection)
            assert [series.case_id for series in cases.cases] == declared
            for series in cases.cases:
                assert set(series.arms) == set(SUITE_KEYS)
                assert series.window_s == ANALYSIS_WINDOW_S
                assert series.playback_t_s.shape == (FIXTURE_N_STEPS,)
                for suite in SUITE_KEYS:
                    arm = series.arms[suite]
                    assert arm.decisions
                    assert float(arm.decisions[0].decision_time_s) <= float(
                        series.playback_t_s[-1]
                    )
                    assert arm.controller_step.shape == series.playback_t_s.shape

            # Row 18: one centerline per arm, closing on the declared tolerance.
            geometry = resolve_geometry(connection, cases)
            assert [entry.case_id for entry in geometry.cases] == declared
            for entry in geometry.cases:
                for suite in SUITE_KEYS:
                    centerline = entry.arms[suite].centerline
                    assert centerline.ndim == 3
                    assert centerline.shape[0] == FIXTURE_N_STEPS
                    assert centerline.shape[2] == 2

            # Row 19: the computed state, which is the record's own authority.
            provenance = resolve_provenance(connection)
            assert provenance.state == DEVELOPMENT_ONLY

            # Row 20: the menu, in the record's order, through the surface gate.
            bundle = resolve_bundle(connection, cases, geometry, provenance)
            assert list(bundle.scenes) == declared
            validate_bundle(bundle)

            # Row 21: the tree, published exactly once.
            written = write_bundle(connection, bundle, render=_scripted_writer())

        assert written.output_root == root
        assert written.cases == tuple(declared)
        assert written.figure_dpi == connection_adapter.REQUIRED_FIGURE_DPI
        assert sorted(path.name for path in root.rglob("*")) == list(
            written.file_names
        )


# --------------------------------------------------------------------------- #
# B5 -- V13 determinism, measured on the published tree rather than on the renderer.
# --------------------------------------------------------------------------- #
def test_b5_the_same_connection_publishes_byte_identical_trees_twice(
    harness: Harness,
) -> None:
    """V13, driven through row 21 twice and compared byte for byte.

    **The measurement is the published tree, not the renderer's return value.** V13 is
    a claim about the files a reader downloads: the same bundle rendered twice under
    the pinned environment produces byte-identical PNG and JSON sets. So this runs the
    whole of rows 1 through 21 twice -- including a fresh installation of the coherent
    three-case menu each time, which is the stronger reading of the invariant, since it
    puts the fixture's own regeneration inside the claim -- and compares every
    published file's bytes.

    **The tree is removed between the two runs, and that is required rather than
    convenient.** Row 21 creates its destination exclusively and
    `_authority_output_root` fixes that destination from authenticated values, so a
    connection has exactly one place to publish and a second run cannot go beside the
    first. Invariant W10 is about a second run while the first publication *stands*;
    determinism is about two runs that each start from nothing, which is what this
    does.

    The digest file is compared with everything else deliberately: it is a function of
    the bundle document's bytes, so if the two documents agree and the two digest files
    do not, the writer is the thing that moved.
    """

    published: list[dict[str, bytes]] = []
    digests: list[str] = []
    for _ in range(2):
        with _publication_root(harness) as root:
            with _three_case_menu(harness) as arguments:
                _connection, _bundle, written = _published(
                    harness, _scripted_writer(), arguments=arguments
                )
            published.append(
                {name: (root / name).read_bytes() for name in written.file_names}
            )
            digests.append(written.bundle_sha256)

    first, second = published
    assert set(first) == set(second)
    assert len(first) == 8, "three cases plus the two fixed bundle files"
    assert any(name.endswith(".png") for name in first)
    for name in sorted(first):
        assert first[name] == second[name], f"{name} is not byte-identical across runs"
    assert digests[0] == digests[1]
    assert (
        external_bytes_digest(first[connection_adapter.BUNDLE_JSON_NAME]) == digests[0]
    )


# --------------------------------------------------------------------------- #
# Codex's Session-154 finding 1 -- the bundle is bound by more than its provenance.
#
# Session 153 bound every field of every scene's provenance block, which proves what
# sources the picture claims. It does not prove the picture. A `VerificationScene`
# also carries thresholds, a body-change description, the playback grid, decisions,
# controller series, tracking arrays and a centerline, and all of them arrive through
# the same separately constructible `bundle` argument. Measured before the repair, on
# the harness below: moving the authenticated `abstain_threshold` from 0.55 to 0.56 on
# **every** scene kept `validate_bundle` satisfied, left every provenance block
# byte-for-byte authentic, and published.
#
# The repair re-derives rows 13 through 20 from the connection and compares canonical
# renderings, so the instrument is total by construction rather than by enumeration.
# The table below is what says the repair is not threshold-specific: one substitution
# per family of scene content, each landing on the same named guard.
# --------------------------------------------------------------------------- #
def _first_arm(scene: Any, **changes: Any) -> Any:
    """Return `scene` with the first suite's arm rebuilt from `changes`."""

    suite = SUITE_KEYS[0]
    arms = dict(scene.arms)
    arms[suite] = replace(arms[suite], **changes)
    return replace(scene, arms=connection_adapter._frozen_mapping(arms))


def _both_arms(scene: Any, edit: Callable[[Any], Any]) -> Any:
    """Return `scene` with `edit` applied to both suites' arms.

    Some scene content is required to agree *across* arms -- the analysis window is
    one -- so a one-arm edit of it would be refused by the surface gate and would say
    nothing about row 21.
    """

    arms = {suite: edit(scene.arms[suite]) for suite in SUITE_KEYS}
    return replace(scene, arms=connection_adapter._frozen_mapping(arms))


SCENE_SUBSTITUTIONS: tuple[tuple[str, Callable[[Any], Any]], ...] = (
    (
        "abstain-threshold",
        lambda scene: replace(
            scene,
            thresholds=replace(
                scene.thresholds,
                abstain_threshold=scene.thresholds.abstain_threshold + 0.01,
            ),
        ),
    ),
    (
        "unknown-threshold",
        lambda scene: replace(
            scene,
            thresholds=replace(
                scene.thresholds,
                unknown_threshold=scene.thresholds.unknown_threshold + 0.01,
            ),
        ),
    ),
    (
        "display-label",
        lambda scene: replace(
            scene,
            body_change=replace(
                scene.body_change, label=f"{scene.body_change.label} (relabelled)"
            ),
        ),
    ),
    (
        "playback-grid",
        lambda scene: replace(
            scene, playback_t_s=np.asarray(scene.playback_t_s) + 1.0e-9
        ),
    ),
    (
        "centerline",
        lambda scene: _first_arm(
            scene,
            centerline_xy=np.asarray(scene.arms[SUITE_KEYS[0]].centerline_xy) + 1.0,
        ),
    ),
    (
        "tracking-reference",
        lambda scene: _both_arms(
            scene,
            lambda arm: replace(
                arm,
                tracking=replace(
                    arm.tracking,
                    task_reference=np.asarray(arm.tracking.task_reference) + 1.0,
                ),
            ),
        ),
    ),
    (
        "tracking-output",
        lambda scene: _first_arm(
            scene,
            tracking=replace(
                scene.arms[SUITE_KEYS[0]].tracking,
                true_task_output=np.asarray(
                    scene.arms[SUITE_KEYS[0]].tracking.true_task_output
                )
                + 1.0,
            ),
        ),
    ),
    (
        "tracking-window",
        lambda scene: _both_arms(
            scene,
            lambda arm: replace(
                arm, tracking=replace(arm.tracking, window_s=arm.tracking.window_s / 2)
            ),
        ),
    ),
    (
        "controller-clock",
        lambda scene: _first_arm(
            scene,
            controller_t_s=np.asarray(scene.arms[SUITE_KEYS[0]].controller_t_s) + 1.0,
        ),
    ),
    (
        "controller-mode",
        lambda scene: _first_arm(
            scene,
            controller_mode=tuple(
                "relabelled" for _ in scene.arms[SUITE_KEYS[0]].controller_mode
            ),
        ),
    ),
    (
        "decision",
        lambda scene: _first_arm(
            scene,
            decisions=(
                replace(
                    scene.arms[SUITE_KEYS[0]].decisions[0],
                    severity_out=scene.arms[SUITE_KEYS[0]].decisions[0].severity_out
                    + 0.01,
                ),
                *scene.arms[SUITE_KEYS[0]].decisions[1:],
            ),
        ),
    ),
)


def _substituted(bundle: VerificationBundle, edit: Callable[[Any], Any]):
    """Return `bundle` with `edit` applied to every scene.

    Every scene rather than one, because that is the shape Codex's control had and it
    is the harder one: `validate_bundle` compares thresholds and grids *across* scenes,
    so a single-scene edit could be refused by the cross-scene gate and would then say
    nothing about this row.
    """

    return VerificationBundle(
        bundle_version=bundle.bundle_version,
        provenance_state=bundle.provenance_state,
        scenes=connection_adapter._frozen_mapping(
            {case_id: edit(scene) for case_id, scene in bundle.scenes.items()}
        ),
    )


def test_the_scene_substitutions_are_all_still_valid_bundles(harness: Harness) -> None:
    """The anchor, and it comes before the refusals it makes meaningful.

    Ten refusals prove nothing if the altered bundles are refused by something that
    already existed. This drives every substitution through the surface gate and
    through the provenance comparison row 21 ran before this session: each altered
    bundle still passes `validate_bundle`, still presents the record's own menu,
    version and state, and still carries provenance blocks identical to the ones this
    connection produces. **So the only thing left that can refuse them is the new
    comparison**, which is what the table below then measures. The last assertion is
    the other half of the anchor: each edit has to actually change the rendering, or
    the refusal it is named for could not fire for the reason claimed.
    """

    with _three_case_menu(harness) as arguments:
        connection, cases, geometry, provenance = _resolved(harness, arguments)
        bundle = resolve_bundle(connection, cases, geometry, provenance)
        for name, edit in SCENE_SUBSTITUTIONS:
            altered = _substituted(bundle, edit)
            validate_bundle(altered)
            assert tuple(altered.scenes) == tuple(bundle.scenes), name
            assert altered.bundle_version == bundle.bundle_version, name
            assert altered.provenance_state == bundle.provenance_state, name
            for case in connection.record.cases:
                presented = altered.scenes[case.case_id].provenance
                assembled = connection_adapter._provenance_for(
                    connection, case, connection.record.authority
                )
                for field in dataclass_fields(Provenance):
                    assert getattr(presented, field.name) == getattr(
                        assembled, field.name
                    ), f"{name}/{field.name}"
                assert canonical_scene_text(
                    altered.scenes[case.case_id]
                ) != canonical_scene_text(bundle.scenes[case.case_id]), name


@pytest.mark.parametrize("name, edit", SCENE_SUBSTITUTIONS, ids=[
    name for name, _ in SCENE_SUBSTITUTIONS
])
def test_row21_refuses_a_scene_this_connection_did_not_assemble(
    harness: Harness, name: str, edit: Callable[[Any], Any]
) -> None:
    """One substitution per family of scene content, all landing on the same guard.

    `abstain-threshold` is Codex's reported control verbatim. The rest are what says
    the repair is a binding of the bundle rather than a patch on one field: the other
    threshold, the menu entry's display label, the shared playback grid, the derived
    centerline, both halves of the tracking argument set, the controller clock, the
    controller mode series and one decision's own score. Every one of them is a value
    rows 13 through 20 derive from payloads row 12 authenticated, and none of them is
    reachable from the provenance block.

    The refusal is required to fire **before** anything is created, which is what the
    root assertion is for: a check that ran after the writer would leave a published
    tree carrying content the record never authenticated.
    """

    with _publication_root(harness) as root:
        with _three_case_menu(harness) as arguments:
            connection, cases, geometry, provenance = _resolved(harness, arguments)
            bundle = resolve_bundle(connection, cases, geometry, provenance)
            altered = _substituted(bundle, edit)
            error = _refusal(
                lambda: write_bundle(connection, altered, render=_stub_writer())
            )
        assert error.code == X_BUNDLE_INCOMPLETE
        assert "is not the scene this connection assembles" in str(error)
        assert not root.exists()


def test_the_scene_rendering_covers_every_field_of_the_scene_type(
    harness: Harness,
) -> None:
    """Why the comparison is total, stated as a property of the instrument.

    Row 21 compares canonical renderings rather than a hand-listed field set, for the
    same reason the provenance comparison walks `dataclasses.fields`: a field added to
    `VerificationScene` must be bound without anyone remembering to bind it. **That
    argument holds only while the rendering covers the type**, so this is where it is
    checked, against the encoder itself. A field added to the scene without a matching
    key here turns the totality claim false, and this test is what says so.
    """

    from utils.verification_scene import scene_to_json

    with _three_case_menu(harness) as arguments:
        connection, cases, geometry, provenance = _resolved(harness, arguments)
        bundle = resolve_bundle(connection, cases, geometry, provenance)
    scene = next(iter(bundle.scenes.values()))
    rendered = set(scene_to_json(scene))
    declared = {field.name for field in dataclass_fields(type(scene))}
    assert declared, "a scene type with no fields would make this vacuous"
    assert rendered == declared


# --------------------------------------------------------------------------- #
# Codex's Session-154 finding 2 -- the packet root moves with the destination.
# --------------------------------------------------------------------------- #
def test_the_packet_root_anchor_accepts_the_chain_it_is_written_for(
    harness: Harness,
) -> None:
    """The anchor for the three refusals below, and it comes first.

    A helper that refused everything would satisfy every refusal test under it and
    would take the accept path down with it. This drives `_require_one_packet_root` on
    the genuine authenticated connection and requires it to return the harness packet
    root -- the same lesson-285 shape the audit-hook observer's own anchor has.

    *** THE CALL IS INSIDE THE INSTALLER'S BLOCK NOW, AND THAT MOVE IS THE SESSION-155
    REPAIR SHOWING ITS TEETH ON THE ACCEPT SIDE. *** The helper reads the record's bytes
    off disk, and `_three_case_menu` restores every byte it touched -- the record
    included -- when its block exits. Driving the helper afterwards therefore measured a
    *restored* record against a digest authenticated over the *installed* one, and it
    refused, correctly. A connection is only meaningful while the tree it authenticated
    still stands; that was always true and is only now observable.
    """

    with _three_case_menu(harness) as arguments:
        connection = authenticate_connection(**arguments)
        assert (
            connection_adapter._require_one_packet_root(connection)
            == harness.packet_root.resolve()
        )


def test_row21_refuses_a_packet_root_moved_together_with_its_destination(
    harness: Harness, tmp_path: Path
) -> None:
    """Codex's Session-154 finding 2, driven exactly as reported.

    `_authority_output_root` derives the publication root from
    `connection.bound.packet_root`, and that field sits in the same substitutable
    `BoundPaths` value as `output_root`. Measured before the repair: moving **both**
    coherently -- and leaving every authenticated record, config, source, dataset and
    role path pointing into the real packet tree -- published the whole declared set
    beneath an unrelated temporary directory, because the expected value moved with the
    substitution.

    The anchor is now the record path, whose bytes rows 1 and 2 actually read, so a
    root that does not contain the record it authenticated cannot fix where the
    publication goes. Nothing appears under the substituted root, which is the second
    half of the assertion.
    """

    other = (tmp_path / "other-packet").resolve()
    with _three_case_menu(harness) as arguments:
        connection, cases, geometry, provenance = _resolved(harness, arguments)
        bundle = resolve_bundle(connection, cases, geometry, provenance)
        parent = connection_adapter.OUTPUT_PARENTS[connection.record.authority]
        moved = replace(
            connection,
            bound=replace(
                connection.bound,
                packet_root=other,
                output_root=other.joinpath(
                    *parent.parts, connection.record.record_label
                ),
            ),
        )
        error = _refusal(lambda: write_bundle(moved, bundle, render=_stub_writer()))
    assert error.code == X_PROVENANCE_UNRESOLVED
    assert "does not hold the authenticated record" in str(error)
    assert not other.exists()


def test_row21_refuses_a_record_bound_somewhere_else_inside_the_packet(
    harness: Harness,
) -> None:
    """The other direction, which containment alone would accept.

    Section 3.1 gives a connection record exactly one packet-relative location, and
    finding CX is about a record presented from somewhere else -- including from inside
    the tree step 21 exclusively creates. A record moved to a different path under the
    *same* root is still inside the packet root, so a containment test would pass it;
    the comparison is an equality for that reason.
    """

    with _publication_root(harness) as root:
        with _three_case_menu(harness) as arguments:
            connection, cases, geometry, provenance = _resolved(harness, arguments)
            bundle = resolve_bundle(connection, cases, geometry, provenance)
            relocated = replace(
                connection,
                bound=replace(
                    connection.bound,
                    record_path=harness.packet_root / "connection_record.json",
                ),
            )
            error = _refusal(
                lambda: write_bundle(relocated, bundle, render=_stub_writer())
            )
        assert error.code == X_PROVENANCE_UNRESOLVED
        assert "does not hold the authenticated record" in str(error)
        assert not root.exists()


def test_row21_refuses_a_source_artifact_bound_outside_the_packet_root(
    harness: Harness, tmp_path: Path
) -> None:
    """The containment direction, on a path the record itself declares.

    The record path pins one location; every other packet-relative path is the
    record's to declare, so those are required to be *inside* the root rather than at
    a derived place. This moves one authenticated source artifact out of the packet and
    requires the row to refuse, which is invariant W8's one-root property stated over
    the whole bound set rather than over the destination alone.
    """

    with _publication_root(harness) as root:
        with _three_case_menu(harness) as arguments:
            connection, cases, geometry, provenance = _resolved(harness, arguments)
            bundle = resolve_bundle(connection, cases, geometry, provenance)
            artifacts = dict(connection.bound.packet_artifacts)
            moved_key = sorted(artifacts)[0]
            artifacts[moved_key] = (tmp_path / "elsewhere" / "artifact.json").resolve()
            outside = replace(
                connection,
                bound=replace(
                    connection.bound,
                    packet_artifacts=MappingProxyType(artifacts),
                ),
            )
            error = _refusal(
                lambda: write_bundle(outside, bundle, render=_stub_writer())
            )
        assert error.code == X_PROVENANCE_UNRESOLVED
        assert "outside the packet root" in str(error)
        assert moved_key in str(error)
        assert not root.exists()


# --------------------------------------------------------------------------- #
# Codex's Session-155 finding 1 -- the whole packet-relative bound set moves at once.
#
# Three sessions running, the repair anchored one field of `BoundPaths` to another
# field of `BoundPaths`, and each time the next substitution simply moved both. The
# tests below are written around the one boundary that is not a field: the record's
# bytes on disk. The accept-side case comes **first**, because a helper that refused a
# copied packet would satisfy every refusal here and would break the one invocation
# invariant W8 explicitly permits.
# --------------------------------------------------------------------------- #
def _coherently_moved(connection, new_root: Path, *, move_allowlist: bool):
    """Return the connection with every packet-relative bound path under `new_root`.

    Args:
        connection: the genuinely authenticated connection.
        new_root: the tree to move the whole packet-relative set into.
        move_allowlist: whether `expected_opens` moves with it. False is Codex's
            reported substitution; True is the strictly wider one my re-drive ran, and
            it is the case that says the allowlist check is not the anchor.

    **Nothing here moves the role root or the checkpoint root**, because those are
    machine-selected and W8 has never governed them. Moving them would make the control
    refuse for a reason that has nothing to do with the finding.
    """

    old = Path(connection.bound.packet_root).resolve()

    def moved(path: Path) -> Path:
        resolved = Path(path).resolve()
        if old != resolved and old not in resolved.parents:
            return resolved
        return new_root.joinpath(*resolved.relative_to(old).parts)

    bound = connection.bound
    substituted = replace(
        connection,
        bound=replace(
            bound,
            packet_root=new_root,
            record_path=moved(bound.record_path),
            output_root=moved(bound.output_root),
            schema_path=moved(bound.schema_path),
            config_path=moved(bound.config_path),
            packet_artifacts=MappingProxyType(
                {key: moved(value) for key, value in bound.packet_artifacts.items()}
            ),
        ),
    )
    if move_allowlist:
        substituted = replace(
            substituted,
            expected_opens=frozenset(moved(path) for path in connection.expected_opens),
        )
    return substituted


def test_row21_accepts_a_whole_packet_copied_and_run_against_the_copy(
    harness: Harness, tmp_path: Path
) -> None:
    """The accept side W8 permits, and it is the anchor for the three refusals below.

    A packet copied whole and run against the copy has **one** root: every
    packet-relative path is under it, the allowlist names those paths, and the record's
    own bytes are there too. That is the invocation invariant W8 allows, and it is
    exactly what a check anchored to "the paths agree with one another" cannot tell
    apart from a substitution -- and what a check anchored to the record's bytes can.

    So this publishes, from a root no row bound, purely because the bytes are there.
    """

    destination = (tmp_path / "copied-packet").resolve()
    with _three_case_menu(harness) as arguments:
        connection, cases, geometry, provenance = _resolved(harness, arguments)
        bundle = resolve_bundle(connection, cases, geometry, provenance)
        shutil.copytree(harness.packet_root, destination)
        shutil.rmtree(
            destination / "results" / "verification_connection_development",
            ignore_errors=True,
        )
        written = write_bundle(
            _coherently_moved(connection, destination, move_allowlist=True),
            bundle,
            render=_stub_writer(),
        )
    assert written.output_root.is_relative_to(destination)
    assert len(written.file_names) == 8
    assert not (harness.output_dir / RECORD_LABEL).exists()


def test_row21_refuses_a_packet_root_moved_with_its_whole_bound_path_set(
    harness: Harness, tmp_path: Path
) -> None:
    """Codex's Session-155 finding 1, driven exactly as reported.

    Measured before the repair, with `packet_root`, `output_root`, `record_path`,
    `schema_path`, `config_path` and every `packet_artifacts` value moved coherently
    into a temporary tree **that did not exist**: all eight files published beneath it.
    The Session-154 helper proved only that the fields of one `BoundPaths` agreed with
    each other, and a substitution that moves them all together keeps them agreeing.

    Here the allowlist is deliberately left alone, which is the substitution as
    reported; the wider one is the test below.
    """

    destination = (tmp_path / "other-packet").resolve()
    with _publication_root(harness) as root:
        with _three_case_menu(harness) as arguments:
            connection, cases, geometry, provenance = _resolved(harness, arguments)
            bundle = resolve_bundle(connection, cases, geometry, provenance)
            moved = _coherently_moved(connection, destination, move_allowlist=False)
            error = _refusal(lambda: write_bundle(moved, bundle, render=_stub_writer()))
        assert error.code == X_PROVENANCE_UNRESOLVED
        assert "the allowlist row 3 derived from this record does not name" in str(error)
        assert not destination.exists()
        assert not root.exists()


def test_row21_refuses_a_packet_root_whose_allowlist_moved_with_it(
    harness: Harness, tmp_path: Path
) -> None:
    """The strictly wider substitution, which is what says where the anchor really is.

    `expected_opens` is derived at row 3 and is a second witness to the paths this
    chain resolved -- but it is still a field of a value a caller can rebuild, so
    moving it too is one more substitution and a check that stopped there would be one
    more object-bounded check. **This moves it, and the refusal comes from the record's
    bytes**: there is no record at the substituted path to read.

    *** THIS IS THE TEST THAT WOULD GO GREEN FOR THE WRONG REASON IF THE DIGEST CHECK
    WERE DELETED AND ONLY THE ALLOWLIST CHECK KEPT. *** Its message fragment names the
    read, not the allowlist, for that reason.
    """

    destination = (tmp_path / "other-packet").resolve()
    with _publication_root(harness) as root:
        with _three_case_menu(harness) as arguments:
            connection, cases, geometry, provenance = _resolved(harness, arguments)
            bundle = resolve_bundle(connection, cases, geometry, provenance)
            moved = _coherently_moved(connection, destination, move_allowlist=True)
            error = _refusal(lambda: write_bundle(moved, bundle, render=_stub_writer()))
        assert error.code == X_PROVENANCE_UNRESOLVED
        assert "could not be read" in str(error)
        assert not destination.exists()
        assert not root.exists()


def test_row21_refuses_a_packet_root_holding_a_different_record(
    harness: Harness, tmp_path: Path
) -> None:
    """A complete, coherent, existing packet copy -- carrying one other record.

    This is the case that separates "the bytes are there" from "some bytes are there",
    and it is why the check is a digest comparison rather than an existence test. The
    copy is real, every path resolves, the allowlist names all of them, and one byte of
    the record differs from the record rows 1 and 2 authenticated.
    """

    destination = (tmp_path / "copied-packet").resolve()
    with _publication_root(harness) as root:
        with _three_case_menu(harness) as arguments:
            connection, cases, geometry, provenance = _resolved(harness, arguments)
            bundle = resolve_bundle(connection, cases, geometry, provenance)
            shutil.copytree(harness.packet_root, destination)
            shutil.rmtree(
                destination / "results" / "verification_connection_development",
                ignore_errors=True,
            )
            moved = _coherently_moved(connection, destination, move_allowlist=True)
            record = Path(moved.bound.record_path)
            record.write_bytes(record.read_bytes().replace(b"schema", b"schemA", 1))
            error = _refusal(lambda: write_bundle(moved, bundle, render=_stub_writer()))
        assert error.code == X_PROVENANCE_UNRESOLVED
        assert "not the authenticated" in str(error)
        assert not root.exists()


def test_the_packet_root_anchor_permits_the_role_and_checkpoint_roots_outside_it(
    harness: Harness,
) -> None:
    """The one place the allowlist legitimately reaches outside the packet.

    `--role-root` and `--checkpoint-root` are CLI arguments precisely because the
    dataset is git-ignored and lives wherever the director put it, so the section-4.2
    allowlist names paths under two trees W8 has never governed. This states that as a
    measurement rather than as a comment: the harness really does put both roots
    outside the packet, so the containment sweep really is exercising `_is_under`
    rather than passing vacuously.
    """

    assert not harness.role_root.resolve().is_relative_to(harness.packet_root.resolve())
    assert not harness.checkpoint_root.resolve().is_relative_to(
        harness.packet_root.resolve()
    )
    with _three_case_menu(harness) as arguments:
        connection = authenticate_connection(**arguments)
        outside = [
            path
            for path in connection.expected_opens
            if not Path(path).resolve().is_relative_to(harness.packet_root.resolve())
        ]
        assert outside, "the allowlist must reach the role and checkpoint trees"
        assert (
            connection_adapter._require_one_packet_root(connection)
            == harness.packet_root.resolve()
        )


def test_the_packet_root_anchor_refuses_an_allowlist_entry_under_no_bound_root(
    harness: Harness, tmp_path: Path
) -> None:
    """The refusal side of that permission, so the sweep is not a formality.

    `_is_under` exists to let the role and checkpoint trees through. A test that only
    drove the accept side could not tell it apart from a sweep that let *everything*
    through, so this adds one allowlist entry under neither root and requires the
    refusal.
    """

    with _three_case_menu(harness) as arguments:
        connection = authenticate_connection(**arguments)
        stranger = (tmp_path / "stranger" / "payload.npz").resolve()
        widened = replace(
            connection,
            expected_opens=frozenset({*connection.expected_opens, stranger}),
        )
        error = _refusal(
            lambda: connection_adapter._require_one_packet_root(widened)
        )
    assert error.code == X_PROVENANCE_UNRESOLVED
    assert "neither inside the packet root" in str(error)
    assert str(stranger) in str(error)


@pytest.mark.parametrize(
    "case, fragment",
    [
        ("corrupt-phys-crc", "does not cover its own bytes"),
        ("truncated-phys-body", "into a chunk header"),
        ("truncated-chunk-header", "into a chunk header"),
        ("length-overruns-the-file", "the file is truncated"),
        ("trailing-bytes", "after its IEND chunk"),
        ("two-phys-chunks", "more than one pHYs chunk"),
        ("wrong-phys-length", "the format fixes it at 9"),
        ("non-metre-unit", "rather than in metres"),
        ("no-image-header", "opens with"),
        ("second-image-header", "second IHDR chunk"),
        ("wrong-image-header-length", "the format fixes it at 13"),
        ("no-image-data", "carries no IDAT chunk"),
        ("resolution-after-the-image-data", "after its image data has begun"),
        ("interrupted-image-data", "resumes its image data"),
        ("non-empty-iend", "fixes it as empty"),
        ("zero-width-image", "declares an image width of 0"),
        ("zero-height-image", "declares an image height of 0"),
        ("undefined-colour-type", "declares colour type 7"),
        ("undefined-bit-depth-for-the-colour-type", "declares bit depth 2 for colour type 2"),
        ("undefined-compression-method", "declares compression method 1"),
        ("undefined-filter-method", "declares filter method 1"),
        ("undefined-interlace-method", "declares interlace method 2"),
        ("image-data-that-is-not-a-zlib-stream", "is not a zlib stream"),
        ("image-data-of-the-wrong-length", "does not describe the image the header describes"),
        ("image-data-shorter-than-the-declared-image", "decompresses to 1 bytes"),
        ("bytes-appended-after-the-image-stream", "after the zlib stream ends"),
        ("image-stream-that-never-ends", "zlib stream never ends"),
    ],
)
def test_the_png_walk_refuses_every_malformed_resolution_claim(
    case: str, fragment: str
) -> None:
    """Twenty-seven malformed figures, and the named refusal each one lands on.

    *** THIS IS CODEX'S SESSION-153 FINDING 2. *** Re-driven at source before the
    repair: the corrupt-CRC file was **accepted** and published as `(11811, 11811)`
    pixels per metre, and the truncated body left the adapter's refusal surface
    entirely as `IndexError("index out of range")`. The rest of this table is what
    making the walk total rather than patching those two inputs buys: a header the
    file cannot honour, bytes after the datastream ends, and a file that states its
    resolution twice were all reachable through the same parser.

    **Two rows land on the same guard, and that is the measurement rather than a
    duplicate.** Codex's reported input -- a `pHYs` header declaring nine bytes over a
    one-byte body -- is refused because the file ends inside a chunk header, not
    because a `pHYs` body was short; the parser never gets far enough to know which
    chunk it was about to read. Keeping that exact input beside the bare truncation
    case is what pins the reported defect rather than a neighbour of it.

    **The last eleven rows are Codex's Session-155 finding 2, my re-drive of it, and one more
    the owner found afterwards by asking the same question of the repair.**
    Each has correct chunk bounds, correct CRCs and correct chunk order, and each still
    fails to be an image: two with no pixels in them, four declaring a header value the
    format does not define, one whose image data is not a compressed stream at all, and
    one whose stream decompresses to a length no image of the declared size has.

    *** THE LAST TWO WERE NOT REPORTED BY ANYONE AND ARE THE REASON THE DECOMPRESSION
    GOES THROUGH A `decompressobj`. *** `zlib.decompress` returns the payload and raises
    nothing when bytes are appended after a complete stream, so the one-call form cannot
    tell a compressed image from a compressed image with something stuck on the end; and
    a truncated stream has to be refused as *unfinished* rather than accepted for the
    prefix it did produce. `eof` and `unused_data` are what say which.

    *** AND `image-data-shorter-than-the-declared-image` IS HERE BECAUSE THE MUTATION
    SWEEP FOUND IT MISSING, WHICH IS THE ONLY SURVIVOR THE SWEEP PRODUCED. *** The
    mutant turned `len(decompressed) != expected_raw` into `len(decompressed) >
    expected_raw` and **survived**, because the wrong-length fixture above compresses
    three bytes for a two-byte image -- it is *longer* than expected, so a
    greater-than test refuses it too and the row's equality was never the reason that
    case was green. A fixture *shorter* than the declared image is what separates the
    two, and it is the direction that matters more: a decoder handed too little data
    produces a partial image, not an error. **The pair is the instrument; either one
    alone measures half of it.**
    """

    error = _refusal(
        lambda: connection_adapter._png_pixels_per_metre(
            _malformed_png(case), where="case.png"
        )
    )
    assert error.code == X_BUNDLE_INCOMPLETE
    assert fragment in str(error)


def test_the_png_image_size_derivation_is_the_formats_own_arithmetic() -> None:
    """The length check's own instrument, driven against hand-derived literals.

    The image-data length check is only as good as the size it compares against, and
    that size is computed rather than read out of the file -- so it needs its own
    control, and the control has to be a literal. Every figure below is worked out from
    the format's rules by hand, not from the function under test:

      * 1x1 grey at depth 8: one scanline of one byte, plus its filter byte -> **2**.
        That is the size the malformed-PNG fixtures above are built to, which is why
        their header cases refuse for a header reason and not for a length one.
      * 4x4 RGBA at depth 8: four scanlines of 4x4=16 bytes, plus one filter byte
        each -> 4 * 17 = **68**.
      * 8x1 grey at depth 1: one scanline of ceil(8/8)=1 byte plus a filter byte
        -> **2**. Sub-byte packing is where a naive `width * depth // 8` goes wrong.
      * 9x1 grey at depth 1: ceil(9/8)=2 bytes plus a filter byte -> **3**.
      * 8x8 grey at depth 8, Adam7: the seven passes carry 1x1, 1x1, 2x1, 2x2, 4x2,
        4x4 and 8x4 pixels, so 2+2+3+6+10+20+36 -> **79**, which is larger than the
        non-interlaced 8*(1+8)=**72** because each pass pays its own filter bytes.

    *** THE INTERLACED CASE IS DERIVED RATHER THAN EXCUSED. *** matplotlib writes
    non-interlaced files, so nothing this packet produces exercises Adam7 -- and a
    length check that quietly skipped the interlaced branch would be a hole shaped
    exactly like a legal PNG. There is no interlaced fixture to measure against because
    this packet declares no PNG encoder; the literal above is the arithmetic instead.
    """

    derive = connection_adapter._png_expected_raw_bytes
    assert derive(width=1, height=1, bit_depth=8, colour_type=0, interlace=0) == 2
    assert derive(width=4, height=4, bit_depth=8, colour_type=6, interlace=0) == 68
    assert derive(width=8, height=1, bit_depth=1, colour_type=0, interlace=0) == 2
    assert derive(width=9, height=1, bit_depth=1, colour_type=0, interlace=0) == 3
    assert derive(width=8, height=8, bit_depth=8, colour_type=0, interlace=0) == 72
    assert derive(width=8, height=8, bit_depth=8, colour_type=0, interlace=1) == 79
    assert derive(width=1, height=1, bit_depth=8, colour_type=0, interlace=1) == 2


def test_the_png_walk_accepts_the_tracked_step_3_figure_set() -> None:
    """The strict walk is measured against real matplotlib output, not only stubs.

    A parser made stricter is only correct if it still accepts the files the packet
    actually produces, and the tracked Step-3 fixture figures are the only PNGs in the
    repository that were written by the renderer this row calls. Every one of them must
    pass a full CRC-checked walk, satisfy every header and image-data check the walk
    now makes, and declare the resolution `REQUIRED_FIGURE_DPI` derives -- which is
    also where that integer came from (Session 153), rather than from a pinned
    constant.

    *** THE COUNT IS FOUR, AND THIS CORRECTS A NUMBER I PUBLISHED. *** Session 154 said
    "the ten tracked Step-3 figures" here and in its report; ten is the number of
    tracked *files* under `results/verification_fixture` -- four figures, four scene
    documents, the bundle and its digest -- and four is the number of figures. The
    count is asserted as a literal below rather than measured from the same glob it
    guards, because a count taken from the thing under test cannot notice the thing
    under test going missing.

    This reads tracked development artifacts for their bytes. It opens no role
    payload, no checkpoint and no result.
    """

    figures = sorted((PACKET_ROOT / "results" / "verification_fixture").glob("*.png"))
    assert len(figures) == 4, f"the tracked Step-3 figure set is {len(figures)} files"
    expected = round(
        connection_adapter.REQUIRED_FIGURE_DPI / connection_adapter._METRES_PER_INCH
    )
    for figure in figures:
        assert connection_adapter._png_pixels_per_metre(
            figure.read_bytes(), where=figure.name
        ) == (expected, expected)


# --------------------------------------------------------------------------- #
# W3 / B4 -- the audit-hook observer.
#
# Every test above establishes what the chain does with the files it opens. This is
# the one that establishes *which files it opens at all*, and it does so from outside
# the module rather than from inside it: `sys.addaudithook` sees the interpreter's own
# `open` event, so an open through `numpy`, through `csv`, through a closed utility or
# through a bare builtin call all arrive here identically. A test that patched
# `Path.read_bytes` -- which is what the Step-4b-ii-a review's `_open_counts`
# instrument does -- can only see the opens that go through that one door.
#
# **The hook is process-wide and cannot be removed, so it is written to cost nothing
# when it is not recording**: one truth test on an empty list, and a return. It records
# only while an `_observed_opens()` block is active.
# --------------------------------------------------------------------------- #

#: The stack of active recorders. Empty means the hook is inert.
_AUDIT_RECORDERS: list[list[Any]] = []


def _audit_open_hook(event: str, args: tuple) -> None:
    """Record the path of every `open` event raised while a recorder is active.

    The hook must not raise: an exception from an audit hook propagates into whatever
    the interpreter was doing, so a bug here would be indistinguishable from a bug in
    the code under test. It therefore appends and does nothing else -- no resolution,
    no filtering and no I/O of its own, all of which happen in the test.
    """

    if not _AUDIT_RECORDERS:
        return
    if event == "open":
        _AUDIT_RECORDERS[-1].append(args[0])


sys.addaudithook(_audit_open_hook)


@contextmanager
def _observed_opens():
    """Yield the list of paths every `open` event names while the block runs."""

    recorder: list[Any] = []
    _AUDIT_RECORDERS.append(recorder)
    try:
        yield recorder
    finally:
        _AUDIT_RECORDERS.pop()


def _resolved_opens(recorder: Sequence[Any]) -> list[Path]:
    """Resolve every recorded open, keeping duplicates and dropping file descriptors.

    `open` is raised for `os.open` too, and that form can name an already-open file
    descriptor rather than a path. An integer is not a claim about a file's location,
    so it is not comparable to the allowlist; this asserts none appeared rather than
    silently discarding it.
    """

    assert not [entry for entry in recorder if isinstance(entry, int)]
    return [Path(entry).resolve() for entry in recorder]


def test_the_open_observer_records_an_open_the_allowlist_does_not_name(
    tmp_path: Path,
) -> None:
    """The instrument's own anchor, and it comes before the measurement it supports.

    An observer that records nothing satisfies a set-equality test against an empty
    expected set, and satisfies a one-directional containment test against any
    expected set at all. So the first thing established is that this one sees an open
    -- and that it sees one taken through a door the adapter does not use, because the
    property being measured is about the interpreter's opens rather than about
    `pathlib`'s.
    """

    stray = tmp_path / "unnamed.txt"
    stray.write_text("not in any allowlist\n", encoding="utf-8")
    with _observed_opens() as recorder:
        with open(stray, "rb") as handle:
            handle.read()
        os.close(os.open(stray, os.O_RDONLY))
    observed = _resolved_opens(recorder)
    assert observed.count(stray.resolve()) == 2

    with _observed_opens() as inert:
        pass
    assert inert == []


def test_w3_the_chain_opens_exactly_the_allowlist_and_nothing_else(
    harness: Harness,
) -> None:
    """Acceptance test B4: the observed open set equals the section-4.2 allowlist.

    *** THE EQUALITY IS IN BOTH DIRECTIONS AND THE OBSERVED SIDE IS NOT FILTERED. ***
    Containment one way passes on an adapter that opens nothing; containment the other
    way passes on an adapter that opens half the packet as long as the allowlist is
    generous. And a filtered observed side is the shape of Codex's Round-1 finding on
    Step-4b-ii-a: the record's own path was missing from `expected_open_set`, and the
    repair that would have "fixed" the resulting failure by dropping it from the
    observed side would have removed the only evidence that step 1 opens the record.

    Measured: the chain raises 48 `open` events over 47 distinct paths, and every one
    of those paths is named by the record.
    """

    with _three_case_menu(harness) as arguments:
        record = load_connection_record(
            arguments["connection_record_path"],
            arguments["connection_record_sha256"],
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
        expected = set(expected_open_set(record, bound))
        with _observed_opens() as recorder:
            authenticate_connection(**arguments)
        observed = _resolved_opens(recorder)

    assert expected, "an empty allowlist would make this test vacuous"
    assert set(observed) - expected == set()
    assert expected - set(observed) == set()
    assert set(observed) == expected


def test_w3_the_schema_is_the_only_file_the_chain_opens_more_than_once(
    harness: Harness,
) -> None:
    """The pinned second read, pinned again at the interpreter rather than at one door.

    The Step-4b-ii-a review closed with `schema.json` read exactly twice and the count
    pinned rather than excused: `config_contract.validate_config_document` receives the
    schema as a document but re-derives its raw digest from the path itself. That pin
    was measured through a patched `Path.read_bytes`. This measures the same fact from
    the audit hook, so a future second read taken through any other door -- `numpy`, a
    bare `open`, a closed utility -- fails here instead of joining an allowance.
    """

    with _three_case_menu(harness) as arguments:
        with _observed_opens() as recorder:
            authenticate_connection(**arguments)
        observed = _resolved_opens(recorder)

    repeated = {path for path in observed if observed.count(path) > 1}
    assert repeated == {(harness.packet_root / SCHEMA_RELATIVE).resolve()}
    assert observed.count((harness.packet_root / SCHEMA_RELATIVE).resolve()) == 2


def test_row21_opens_nothing_outside_the_tree_it_created(harness: Harness) -> None:
    """The publishing row's own open set, which the allowlist deliberately does not name.

    Section 4.2's allowlist is about the files the chain *reads to authenticate*; the
    output tree is not one of them, because it does not exist until row 21 creates it.
    So the property here is the complementary one: once the chain has been
    authenticated, the only files row 21 and its writer touch are inside the root row 3
    bound, and the writer being a parameter does not change that -- the observed opens
    include the stub writer's own writes.

    *** THIS IS ALSO THE INSTRUMENT THAT SAYS THE SESSION-155 RE-DERIVATION IS FREE OF
    I/O. *** Row 21 now re-runs rows 13 through 20 to bind the bundle it was handed,
    and the claim that this opens nothing is exactly what fails here if it is false:
    the re-derivation runs *before* the exclusive create, so any file it opened would
    be outside the tree this test requires every open to be inside.

    *** AND THE PROPERTY IS WIDENED BY EXACTLY ONE FILE THIS SESSION, WHICH IS DISCLOSED
    HERE RATHER THAN ABSORBED. *** `_require_one_packet_root` re-reads the connection
    record to settle, from bytes rather than from paths, that the packet root holds the
    record this chain authenticated -- the anchor Codex's Session-155 finding 1 showed
    could not live inside `BoundPaths`. So row 21 now opens one file outside the tree it
    creates, and the widening is bounded here rather than stated loosely: **exactly one
    such path, it is `bound.record_path`, it is a member of the section-4.2 allowlist,
    and it is opened exactly once.** The last clause matters on its own -- a check that
    quietly became a re-read per case would still satisfy a set comparison, and would
    not satisfy this.

    The file is not a new input by any reading: rows 1 and 2 opened it, section 4.2
    names it, and it is the one file whose digest the CLI authorization pinned.
    """

    with _publication_root(harness) as root:
        with _three_case_menu(harness) as arguments:
            connection, cases, geometry, provenance = _resolved(harness, arguments)
            bundle = resolve_bundle(connection, cases, geometry, provenance)
            with _observed_opens() as recorder:
                written = write_bundle(connection, bundle, render=_stub_writer())
            observed = _resolved_opens(recorder)
            record_path = Path(connection.bound.record_path).resolve()
            assert record_path in {Path(p).resolve() for p in connection.expected_opens}
        assert observed, "row 21 both writes and reads back, so it must open something"
        outside = [path for path in observed if path.parent != root.resolve()]
        assert outside == [record_path], (
            "row 21 may open exactly one file outside the tree it creates, and it is "
            f"the record it was authenticated by; observed {outside}"
        )
        assert _resolved_opens(recorder).count(record_path) == 1
        inside = [path for path in observed if path.parent == root.resolve()]
        assert {path.name for path in inside} == set(written.file_names)
