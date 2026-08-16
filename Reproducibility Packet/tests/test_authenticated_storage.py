"""Tests for the bytes-domain entry points into the closed storage/role contracts.

**What this file is for.** `utils.authenticated_storage` exists so an authenticated
caller can hand the exact bytes it digested to the parsers that own their rules, instead
of handing over a pathname and hoping the second open returns the same object. Two
properties have to hold for that to be worth anything, and this file is organised around
them:

  1. *The entry points here agree exactly with the closed path-based functions.* The
     reading mechanics -- the strict header and the typing loop -- are restated in the
     new module, and a restated fact is allowed in this project only when something
     mechanical compares it against its owner. Every parser here is pinned by equality
     against `utils.storage_contract`'s own function over the same document, and the
     refusals are driven on both sides.
  2. *Moving the read out did not move the checks out with it.* Every rule the closed
     functions apply is driven through the new entry points: the schema-A audit, the
     role-index row grammar, the configuration join, the payload digest, the key
     allowlist and the role semantics.

**Why the module is not simply an edit to those two files.**
`utils.dev_fit_trainer.training_code_identity` pins the canonical text digest of
`role_contract.py` and `storage_contract.py`, among six others, as bound 4's
training-protocol identity, and three approved artifacts record those exact digests.
`test_the_closed_utilities_keep_the_identity_three_approved_artifacts_record` is that
fact stated as a test, so a later session that "simplifies" this module by folding it
back into those files finds out here rather than by making three completed lanes
non-comparable.

Nothing in this file opens a scientific payload, a checkpoint or a held-out split. Every
tree it builds is under `tmp_path` or is the tracked contract fixture.
"""

from __future__ import annotations

import io
import json
import sys
from dataclasses import replace
from pathlib import Path

import numpy as np
import pytest

PACKET_ROOT = Path(__file__).resolve().parents[1]
SCRIPTS_ROOT = PACKET_ROOT / "scripts"
sys.path.insert(0, str(SCRIPTS_ROOT))

from build_data_contract_fixture import build_fixture  # noqa: E402
from utils.authenticated_storage import (  # noqa: E402
    AuthenticatedRolePayloadLoader,
    bytes_sha256,
    npz_archive_from_bytes,
    parse_identity_manifest,
    parse_role_index,
    validate_role_index_rows,
)
from utils.config_contract import load_config  # noqa: E402
from utils.dev_fit_trainer import training_code_identity  # noqa: E402
from utils.protocol_p import canonical_text_sha256  # noqa: E402
from utils.role_contract import RolePayloadLoader  # noqa: E402
from utils.schema_types import SCHEMA_VERSION  # noqa: E402
from utils.storage_contract import (  # noqa: E402
    RoleIndexRow,
    StorageContractError,
    file_sha256,
    read_identity_manifest,
    read_role_index,
)

SCHEMA_PATH = PACKET_ROOT / "schema" / "schema.json"
CONFIG_PATH = PACKET_ROOT / "config" / "draft-config-v0.1.json"
FIXTURE_N_STEPS = 48

#: The two files this module exists in order not to edit, and the digests three approved
#: artifacts record for them. Stated as literals: a test whose expected value is read
#: from the same place as its actual value holds nothing about either.
PINNED_CODE_IDENTITY = {
    "role_contract.py": "c50bebe5dfab8685b16f421928c0774dddd24e4a6f87542954b65ddc48810a21",
    "storage_contract.py": (
        "40b0f88c75d4f283197011f2470f8b97af639b78573734130c07bcafbc1a20fa"
    ),
}

#: Every approved artifact whose recorded code identity contains those two files.
ARTIFACTS_RECORDING_CODE_IDENTITY = (
    "results/dev_fit/dev_fit_result.json",
    "results/capacity_sweep/plans/stage1-run-2/capacity_sweep_plan.json",
    "results/rung2_escalation/plans/rung2-run-1/rung2_escalation_plan.json",
)


def schema() -> dict[str, object]:
    """Return the tracked machine schema."""

    return json.loads(SCHEMA_PATH.read_text(encoding="utf-8"))


def config():
    """Return the lifecycle-validated tracked draft configuration."""

    return load_config(CONFIG_PATH, SCHEMA_PATH)


@pytest.fixture(scope="module")
def fixture_root(tmp_path_factory: pytest.TempPathFactory) -> Path:
    """Build one reusable role-complete contract fixture."""

    root = tmp_path_factory.mktemp("authenticated-storage") / "dataset"
    build_fixture(SCHEMA_PATH, CONFIG_PATH, root, FIXTURE_N_STEPS)
    return root


def _index_rows(root: Path, role: str) -> list[RoleIndexRow]:
    """Return one role index's rows, read through the closed path-based reader."""

    return read_role_index(root / role / "index.csv", observation=False)


# --------------------------------------------------------------------------- #
# Why this module is separate from the two files it wraps.
# --------------------------------------------------------------------------- #
def test_the_closed_utilities_keep_the_identity_three_approved_artifacts_record() -> None:
    """Editing either file makes three completed, unrepeatable lanes non-comparable.

    `training_code_identity` names eight files; two of them are the ones this module
    exists in order to leave alone. `capacity_sweep.require_anchor_comparability` and
    both read-only analyzers compare the recorded identity against the current tree, so
    a change here does not merely annotate history -- it stops the approved development
    fit, the approved stage-1 sweep and the approved rung-2 escalation from being read
    by the packet's own runbook. This is decision D4's rule reaching two more of the
    same eight files.
    """

    identity = training_code_identity()
    for name, digest in PINNED_CODE_IDENTITY.items():
        assert identity[name] == digest
        assert canonical_text_sha256(SCRIPTS_ROOT / "utils" / name) == digest

    for relative in ARTIFACTS_RECORDING_CODE_IDENTITY:
        recorded = json.loads((PACKET_ROOT / relative).read_text(encoding="utf-8"))
        for name, digest in PINNED_CODE_IDENTITY.items():
            assert recorded["code_identity"][name] == digest


def test_this_module_is_not_part_of_any_recorded_code_identity() -> None:
    """The new module may change freely, and that is the whole point of its being new."""

    assert "authenticated_storage.py" not in training_code_identity()


# --------------------------------------------------------------------------- #
# Property 1 -- the restated reading mechanics agree with their owners.
# --------------------------------------------------------------------------- #
def test_the_bytes_digest_is_the_closed_path_digest(tmp_path: Path) -> None:
    """`bytes_sha256` is `file_sha256` with the read taken out, by equality."""

    path = tmp_path / "payload.bin"
    for raw in (b"", b"the exact bytes\r\n\x00 and a NUL", bytes(range(256))):
        path.write_bytes(raw)
        assert bytes_sha256(raw) == file_sha256(path)


def test_the_manifest_parser_agrees_with_the_closed_reader(fixture_root: Path) -> None:
    """One document, two entry points, one answer -- or the move changed the meaning."""

    manifest = fixture_root / "manifest.csv"
    assert parse_identity_manifest(manifest.read_bytes()) == read_identity_manifest(
        manifest
    )


def test_the_index_parser_agrees_with_the_closed_reader(fixture_root: Path) -> None:
    """The same equality for every role index the contract fixture publishes."""

    for role in ("plant", "labels"):
        index = fixture_root / role / "index.csv"
        assert parse_role_index(
            index.read_bytes(), observation=False
        ) == read_role_index(index, observation=False)


def test_the_index_parser_agrees_on_split_bearing_observation_indexes(
    fixture_root: Path,
) -> None:
    """The observation header carries a column the role header does not.

    Without this the `split` field is never compared across the two entry points, and a
    parser here that dropped it would still satisfy every non-observation equality --
    the column only exists in this shape.
    """

    index = fixture_root / "observations" / "C1" / "index.csv"
    over_bytes = parse_role_index(index.read_bytes(), observation=True)
    assert over_bytes == read_role_index(index, observation=True)
    assert all(row.split is not None for row in over_bytes)
    with pytest.raises(StorageContractError, match="header must be exactly"):
        parse_role_index(index.read_bytes(), observation=False)


def test_both_parsers_refuse_where_the_closed_readers_refuse(
    fixture_root: Path, tmp_path: Path
) -> None:
    """A refusal must be a property of the document, not of which door it came through.

    Each malformed document is driven through *both* entry points and required to raise
    the same message, which is what stops the restated header and typing loop from
    quietly becoming more permissive than the closed ones.
    """

    cases = (
        ("manifest", fixture_root / "manifest.csv"),
        ("index", fixture_root / "plant" / "index.csv"),
    )
    for label, source in cases:
        text = source.read_text(encoding="utf-8")
        broken = ("wrong_column" + text[text.index(",") :]).encode("utf-8")
        path = tmp_path / f"{label}.csv"
        path.write_bytes(broken)

        if label == "manifest":
            over_bytes = lambda: parse_identity_manifest(broken, source=path)  # noqa: E731
            over_path = lambda: read_identity_manifest(path)  # noqa: E731
        else:
            over_bytes = lambda: parse_role_index(  # noqa: E731
                broken, observation=False, source=path
            )
            over_path = lambda: read_role_index(path, observation=False)  # noqa: E731

        with pytest.raises(StorageContractError) as from_bytes:
            over_bytes()
        with pytest.raises(StorageContractError) as from_path:
            over_path()
        assert "header must be exactly" in str(from_bytes.value)
        assert str(from_bytes.value) == str(from_path.value)


def test_both_parsers_refuse_bytes_that_are_not_utf8() -> None:
    """The closed readers decode as UTF-8; a bytes caller must not get a raw decode error."""

    for call in (
        lambda: parse_identity_manifest(b"\xff\xfe not utf-8"),
        lambda: parse_role_index(b"\xff\xfe not utf-8", observation=False),
    ):
        with pytest.raises(StorageContractError, match="is not valid UTF-8"):
            call()


def test_a_bytes_parser_names_the_source_it_was_given() -> None:
    """A refusal about bytes must still tell a reader which document failed."""

    with pytest.raises(StorageContractError, match="the plant index at nowhere"):
        parse_role_index(
            b"wrong\nrow\n", observation=False, source="the plant index at nowhere"
        )


# --------------------------------------------------------------------------- #
# Property 2 -- moving the read out did not move the checks out with it.
# --------------------------------------------------------------------------- #
def test_the_manifest_parser_still_runs_the_schema_a_audit() -> None:
    """The audit is the manifest's real content, and it is reused rather than restated."""

    header = ",".join(
        (
            "schema_version,config_hash,scenario_spec_id,pair_id,run_id",
            "trajectory_spec_id,fault_setting_id,split_group_id,split,suite",
            "estimator_id,controller_id,payload_id,env_profile_id,contact_profile_id",
            "sim_seed,fault_seed,sensor_seed,controller_seed,train_seed",
        )
    )
    with pytest.raises(StorageContractError, match="at least one rollout"):
        parse_identity_manifest((header + "\n").encode("utf-8"))


def test_the_index_parser_and_the_row_validator_share_one_rule() -> None:
    """The row grammar binds a rows caller exactly as it binds a file."""

    def row(run_id: str, npz_path: str) -> RoleIndexRow:
        return RoleIndexRow(
            run_id=run_id,
            schema_version=SCHEMA_VERSION,
            config_hash=config().config_hash,
            npz_path=npz_path,
            sha256="b" * 64,
        )

    assert validate_role_index_rows([row("r0", "r0.npz")], observation=False) == [
        row("r0", "r0.npz")
    ]
    with pytest.raises(StorageContractError, match="without traversal"):
        validate_role_index_rows([row("r0", "../secret.npz")], observation=False)
    with pytest.raises(StorageContractError, match="relative to its own role root"):
        validate_role_index_rows([row("r0", "nested/r0.npz")], observation=False)
    with pytest.raises(StorageContractError, match="duplicate run_id"):
        validate_role_index_rows(
            [row("r0", "r0.npz"), row("r0", "r0.npz")], observation=False
        )


def test_an_unreadable_archive_refuses_by_contract_rather_than_by_zipfile() -> None:
    """A payload can carry its declared digest and still not be a readable archive.

    Truncation raises `zipfile.BadZipFile` at open and a member whose stored bytes
    disagree with its CRC raises the same at read. A valid `.npy` stream returns an
    ndarray rather than an `NpzFile`. Without these translations, a caller that handles
    this package's error type takes a raw exception out of the layer whose job is to
    refuse unsafe payloads.
    """

    buffer = io.BytesIO()
    np.savez(buffer, values=np.arange(64, dtype=np.float64))
    raw = buffer.getvalue()

    with pytest.raises(StorageContractError, match="not a readable non-pickled NPZ"):
        with npz_archive_from_bytes(raw[: len(raw) // 2], what="probe"):
            pass

    corrupted = bytearray(raw)
    corrupted[len(raw) // 2] ^= 0xFF
    with pytest.raises(StorageContractError, match="not a readable non-pickled NPZ"):
        with npz_archive_from_bytes(bytes(corrupted), what="probe") as archive:
            {name: np.asarray(archive[name]) for name in archive.files}

    single_array = io.BytesIO()
    np.save(single_array, np.arange(4, dtype=np.float64))
    with pytest.raises(StorageContractError, match="not a readable non-pickled NPZ"):
        with npz_archive_from_bytes(single_array.getvalue(), what="probe"):
            pass


def test_a_refusal_raised_inside_the_archive_block_is_not_rewrapped() -> None:
    """The translation must not swallow the caller's own contract refusal.

    `StorageContractError` is a `ValueError`, so without the pass-through clause a
    caller's key-allowlist refusal would be caught here and re-described as a broken
    archive -- a message pointing a reader at the wrong defect.

    **The assertion is object identity, not a phrase.** The wrapper interpolates the
    original exception into its own message, so matching on the caller's wording is
    satisfied by the wrapped form too: the Session-143 mutation sweep deleted the
    pass-through clause and this test stayed green until it stopped asking whether the
    text appeared and started asking which object arrived.
    """

    buffer = io.BytesIO()
    np.savez(buffer, values=np.arange(4, dtype=np.float64))
    sentinel = StorageContractError("the caller's own refusal")
    with pytest.raises(StorageContractError) as excinfo:
        with npz_archive_from_bytes(buffer.getvalue(), what="probe"):
            raise sentinel
    assert excinfo.value is sentinel
    assert "not a readable non-pickled NPZ" not in str(excinfo.value)


def test_the_index_parser_applies_the_row_rules_and_not_only_the_header(
    fixture_root: Path, tmp_path: Path
) -> None:
    """A well-formed header over an inadmissible row must still refuse.

    Every other refusal in this file reaches the row grammar through
    `validate_role_index_rows` or through the loader, so `parse_role_index`'s own call
    to it was unmeasured: the Session-143 sweep deleted that call and nothing went red.
    Driving a traversal row through both entry points is what holds it.
    """

    index = fixture_root / "plant" / "index.csv"
    lines = index.read_text(encoding="utf-8").splitlines()
    columns = lines[1].split(",")
    columns[3] = "../secret.npz"
    broken = "\n".join((lines[0], ",".join(columns), "")).encode("utf-8")
    path = tmp_path / "index.csv"
    path.write_bytes(broken)

    with pytest.raises(StorageContractError, match="without traversal") as from_bytes:
        parse_role_index(broken, observation=False, source=path)
    with pytest.raises(StorageContractError, match="without traversal") as from_path:
        read_role_index(path, observation=False)
    assert str(from_bytes.value) == str(from_path.value)


# --------------------------------------------------------------------------- #
# The loader -- the same object, entered with bytes instead of a pathname.
# --------------------------------------------------------------------------- #
def test_the_rows_bound_loader_matches_one_bound_to_the_index_file(
    fixture_root: Path,
) -> None:
    """Handing the loader authenticated rows must not change what it accepts."""

    cfg = config()
    root = fixture_root / "labels"
    from_file = RolePayloadLoader(root, "labels", schema(), cfg)
    from_rows = AuthenticatedRolePayloadLoader(
        root, "labels", schema(), cfg, _index_rows(fixture_root, "labels")
    )

    assert from_rows.run_ids == from_file.run_ids
    run_id = from_file.run_ids[0]
    expected = from_file.load(run_id)
    actual = from_rows.load_bytes(run_id, (root / f"{run_id}.npz").read_bytes())
    assert set(actual) == set(expected)
    assert all(np.array_equal(actual[name], expected[name]) for name in expected)


def test_the_loader_validates_the_rows_it_is_given(fixture_root: Path) -> None:
    """The rules stay owned by the closed contracts; only the read moves out.

    A caller that parsed rows from authenticated bytes is not thereby trusted with which
    rows are admissible: traversal, duplication, a foreign configuration and a wrong
    role root all refuse exactly as they do when the base class reads the file itself.
    """

    cfg = config()
    root = fixture_root / "labels"
    rows = _index_rows(fixture_root, "labels")

    with pytest.raises(StorageContractError, match="without traversal"):
        AuthenticatedRolePayloadLoader(
            root, "labels", schema(), cfg, [replace(rows[0], npz_path="../secret.npz")]
        )
    with pytest.raises(StorageContractError, match="duplicate run_id"):
        AuthenticatedRolePayloadLoader(
            root, "labels", schema(), cfg, [rows[0], rows[0]]
        )
    with pytest.raises(StorageContractError, match="config_hash mismatch"):
        AuthenticatedRolePayloadLoader(
            root,
            "labels",
            schema(),
            cfg,
            [replace(rows[0], config_hash=f"dev-{'c' * 64}")],
        )
    with pytest.raises(StorageContractError, match="must be exactly a labels"):
        AuthenticatedRolePayloadLoader(
            fixture_root / "plant", "labels", schema(), cfg, rows
        )


def test_load_bytes_returns_what_the_bytes_say_not_what_the_path_says(
    tmp_path: Path,
) -> None:
    """The property the whole module exists for, stated at the object that provides it.

    The file on disk is replaced with a different, schema-valid payload before the call,
    and the call still returns the authenticated original. The closed `load` on the same
    row refuses the replaced file -- which is the correct behaviour for a path entry
    point, and is exactly the guarantee a path entry point cannot give the adapter.
    """

    root = tmp_path / "dataset"
    build_fixture(SCHEMA_PATH, CONFIG_PATH, root, FIXTURE_N_STEPS)
    cfg = config()
    rows = read_role_index(root / "plant" / "index.csv", observation=False)
    loader = AuthenticatedRolePayloadLoader(
        root / "plant", "plant", schema(), cfg, rows
    )
    run_id = rows[0].run_id
    payload = root / "plant" / f"{run_id}.npz"
    authenticated = payload.read_bytes()

    with np.load(payload, allow_pickle=False) as archive:
        arrays = {name: np.array(archive[name]) for name in archive.files}
    original_q_true = np.array(arrays["q_true"])
    arrays["q_true"] = arrays["q_true"] + 1.0
    buffer = io.BytesIO()
    np.savez(buffer, **arrays)
    payload.write_bytes(buffer.getvalue())

    loaded = loader.load_bytes(run_id, authenticated)

    assert payload.read_bytes() != authenticated
    assert np.array_equal(loaded["q_true"], original_q_true)
    assert not np.array_equal(loaded["q_true"], original_q_true + 1.0)
    with pytest.raises(StorageContractError, match="SHA-256 mismatch"):
        loader.load(run_id)


def test_load_bytes_still_applies_the_digest_the_index_row_records(
    fixture_root: Path,
) -> None:
    """Supplying the bytes is not the same as choosing which bytes are authentic."""

    cfg = config()
    root = fixture_root / "labels"
    rows = _index_rows(fixture_root, "labels")
    loader = AuthenticatedRolePayloadLoader(root, "labels", schema(), cfg, rows)
    run_id = rows[0].run_id
    raw = (root / f"{run_id}.npz").read_bytes()

    assert loader.load_bytes(run_id, raw)
    with pytest.raises(StorageContractError, match="SHA-256 mismatch"):
        loader.load_bytes(run_id, raw + b"tamper")
    with pytest.raises(KeyError, match="not present in labels index"):
        loader.load_bytes("no_such_run", raw)


def test_load_bytes_applies_the_schema_and_semantic_rules(fixture_root: Path) -> None:
    """Digest agreement is not payload validity, and the bytes entry point knows it.

    The bytes carry a `source_class` no label may carry, and the index row is given the
    digest of those exact bytes, so nothing but the role's own semantic rule can refuse
    them.
    """

    cfg = config()
    root = fixture_root / "labels"
    rows = _index_rows(fixture_root, "labels")
    run_id = rows[0].run_id
    with np.load(root / f"{run_id}.npz", allow_pickle=False) as archive:
        arrays = {name: np.array(archive[name]) for name in archive.files}
    arrays["source_class"] = np.asarray("not_a_known_class")
    buffer = io.BytesIO()
    np.savez(buffer, **arrays)
    raw = buffer.getvalue()

    loader = AuthenticatedRolePayloadLoader(
        root,
        "labels",
        schema(),
        cfg,
        [replace(rows[0], sha256=bytes_sha256(raw))],
    )
    with pytest.raises(StorageContractError, match="invalid label source_class"):
        loader.load_bytes(run_id, raw)


def test_load_bytes_opens_nothing(fixture_root: Path) -> None:
    """The read belongs to the caller that owns the digest, and to nobody else."""

    cfg = config()
    root = fixture_root / "labels"
    rows = _index_rows(fixture_root, "labels")
    run_id = rows[0].run_id
    raw = (root / f"{run_id}.npz").read_bytes()

    reads: list[Path] = []
    real = Path.read_bytes

    def counting(self: Path) -> bytes:
        reads.append(self)
        return real(self)

    with pytest.MonkeyPatch.context() as patch:
        patch.setattr(Path, "read_bytes", counting)
        loader = AuthenticatedRolePayloadLoader(root, "labels", schema(), cfg, rows)
        loader.load_bytes(run_id, raw)

    assert reads == []
