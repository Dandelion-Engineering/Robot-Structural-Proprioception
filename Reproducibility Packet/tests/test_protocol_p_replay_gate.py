"""Contract tests for the Protocol P section 7 replay gate.

The replay gate is a stop-or-go precondition: it decides whether the generator that
will produce 169 screen rollouts is the same instrument that produced the retained
development dataset.  Its dangerous failure mode is therefore not a false alarm but a
**vacuous pass** -- a comparison that reports equality because it compared nothing, or
because NaN handling swallowed a real difference.

Every guard below is exercised with the exact state it was written to reject, not only
with the state it should accept.  The two pinned binary references live outside the
repository (git-ignored retained data), so nothing here depends on them: the binary
domain is covered by its *property* -- that folding CRLF changes a digest -- on a
synthetic file, and the two committed text pins are checked against the real files.
"""

from __future__ import annotations

import dataclasses
import sys
from pathlib import Path

import numpy as np
import pytest

PACKET_ROOT = Path(__file__).resolve().parents[1]
SCRIPTS_ROOT = PACKET_ROOT / "scripts"
sys.path.insert(0, str(SCRIPTS_ROOT))

import protocol_p_replay_gate as gate  # noqa: E402
from utils.schema_types import CHANNEL_NAMES, PrivilegedRecord  # noqa: E402

N_OBSERVATION_METADATA_ENTRIES = 8
N_PER_CHANNEL_DICTS = 5


# ---------------------------------------------------------------------------
# Hash domains (Protocol P section 0)
# ---------------------------------------------------------------------------


def test_canonical_text_sha256_strips_a_utf8_bom(tmp_path: Path) -> None:
    """A BOM must not change a text file's canonical identity."""

    plain = tmp_path / "plain.md"
    with_bom = tmp_path / "with_bom.md"
    plain.write_bytes(b"protocol\n")
    with_bom.write_bytes(b"\xef\xbb\xbfprotocol\n")
    assert gate.canonical_text_sha256(plain) == gate.canonical_text_sha256(with_bom)


def test_canonical_text_sha256_is_invariant_to_the_checkout_line_ending(
    tmp_path: Path,
) -> None:
    """CRLF and LF renderings of the same text share one canonical digest.

    This is what makes a text pin survive a fresh Windows clone, where an unpinned
    file materializes as CRLF under ``core.autocrlf=true``.
    """

    lf = tmp_path / "lf.md"
    crlf = tmp_path / "crlf.md"
    lf.write_bytes(b"line one\nline two\n")
    crlf.write_bytes(b"line one\r\nline two\r\n")
    assert gate.canonical_text_sha256(lf) == gate.canonical_text_sha256(crlf)


def test_raw_file_sha256_never_folds(tmp_path: Path) -> None:
    """The binary helper must report the two renderings as different files."""

    lf = tmp_path / "lf.bin"
    crlf = tmp_path / "crlf.bin"
    lf.write_bytes(b"line one\nline two\n")
    crlf.write_bytes(b"line one\r\nline two\r\n")
    assert gate.raw_file_sha256(lf) != gate.raw_file_sha256(crlf)


def test_the_two_domains_disagree_on_a_payload_containing_crlf_bytes(
    tmp_path: Path,
) -> None:
    """The property that makes the domain split load-bearing.

    A ``.npz`` is a ZIP archive whose payload contains ``0d 0a`` byte pairs as data.
    Routing one through the text helper changes its digest, which is why applying the
    wrong helper is itself an I1 failure rather than a harmless equivalent.
    """

    archive = tmp_path / "payload.bin"
    archive.write_bytes(b"\x50\x4b\x03\x04" + b"\r\n" * 9 + b"\x00\x01\x02")
    assert gate.raw_file_sha256(archive) != gate.canonical_text_sha256(archive)


def test_committed_protocol_file_still_matches_its_jointly_approved_digest() -> None:
    """The pre-registration must not drift from the state both agents approved.

    The protocol file cannot contain its own digest, so this is where the approved
    value is bound to the committed bytes.
    """

    protocol = PACKET_ROOT / "protocol" / gate.PROTOCOL_FILENAME
    assert protocol.is_file()
    assert gate.canonical_text_sha256(protocol) == gate.PROTOCOL_CANONICAL_SHA256


def test_committed_assignment_file_still_matches_its_pinned_digest() -> None:
    """The approved assignment document must not drift from its Correction 3 pin."""

    assignment = PACKET_ROOT / "config" / gate.ASSIGNMENT_FILENAME
    assert assignment.is_file()
    assert gate.canonical_text_sha256(assignment) == gate.ASSIGNMENT_CANONICAL_SHA256


def test_check_pinned_digests_raises_when_an_input_is_absent(tmp_path: Path) -> None:
    """Never fall back to whatever is on disk."""

    with pytest.raises(gate.ProtocolPError, match="absent"):
        gate.check_pinned_digests(
            PACKET_ROOT / "protocol" / gate.PROTOCOL_FILENAME,
            PACKET_ROOT / "config" / gate.ASSIGNMENT_FILENAME,
            tmp_path / "missing_plant.npz",
            tmp_path / "missing_observation.npz",
        )


def test_check_pinned_digests_raises_on_protocol_filename_drift(tmp_path: Path) -> None:
    """A version bump must fail loudly instead of comparing the wrong file.

    Without this, a renamed protocol revision would be silently checked against the
    previous revision's approved digest.
    """

    impostor = tmp_path / "protocol-p-v9.9.9.md"
    impostor.write_bytes(
        (PACKET_ROOT / "protocol" / gate.PROTOCOL_FILENAME).read_bytes()
    )
    # The absence guard runs first, so the binary slots must exist for the filename
    # guard to be the thing under test here.
    plant = tmp_path / "plant.npz"
    observation = tmp_path / "observation.npz"
    plant.write_bytes(b"\x50\x4b\x03\x04")
    observation.write_bytes(b"\x50\x4b\x03\x04")
    with pytest.raises(gate.ProtocolPError, match="expected protocol file"):
        gate.check_pinned_digests(
            impostor,
            PACKET_ROOT / "config" / gate.ASSIGNMENT_FILENAME,
            plant,
            observation,
        )


# ---------------------------------------------------------------------------
# Pre-registered entry counts, bound to the schema rather than to a literal
# ---------------------------------------------------------------------------


def test_privileged_field_count_tracks_the_record_definition() -> None:
    """If the plant record gains a field, the gate must fail rather than compare 20/21."""

    assert gate.N_PRIVILEGED_FIELDS == len(dataclasses.fields(PrivilegedRecord))


def test_observation_entry_count_tracks_the_channel_registry() -> None:
    """38 = 5 per-channel dicts x 6 registry channels + 8 metadata entries."""

    assert gate.N_OBSERVATION_ENTRIES == (
        N_PER_CHANNEL_DICTS * len(CHANNEL_NAMES) + N_OBSERVATION_METADATA_ENTRIES
    )


def test_run_id_is_composed_from_the_pinned_scenario_and_suite() -> None:
    """The replayed row identity is derived, not retyped."""

    assert gate.RUN_ID == f"{gate.SCENARIO_SPEC_ID}_{gate.REPLAY_SUITE}_dataset0"
    assert gate.REPLAY_SUITE in gate.DELIVERED_SUITES


# ---------------------------------------------------------------------------
# Entry comparison, including both NaN directions
# ---------------------------------------------------------------------------


def _float_entry() -> np.ndarray:
    values = np.arange(12, dtype=np.float64).reshape(6, 2)
    values[2, 1] = np.nan
    values[4, 0] = np.nan
    return values


def test_matched_nan_positions_compare_equal() -> None:
    """``gauge_obs`` carries real NaNs; a plain ``==`` would fail a correct replay."""

    entry = gate.compare_entry(_float_entry(), _float_entry())
    assert entry["equal"]
    assert entry["nan_count"] == 2


def test_a_nan_replaced_by_a_number_is_caught() -> None:
    """NaN-tolerance must not become NaN-blindness."""

    actual = _float_entry()
    actual[2, 1] = 0.0
    assert not gate.compare_entry(_float_entry(), actual)["equal"]


def test_a_number_replaced_by_a_nan_is_caught() -> None:
    """The other direction: a dropout that should not be there."""

    actual = _float_entry()
    actual[0, 0] = np.nan
    assert not gate.compare_entry(_float_entry(), actual)["equal"]


def test_a_one_ulp_difference_is_caught() -> None:
    """The gate claims exact reproduction, so the tolerance is zero."""

    actual = _float_entry()
    actual[0, 1] = np.nextafter(actual[0, 1], np.inf)
    assert not gate.compare_entry(_float_entry(), actual)["equal"]


def test_a_dtype_change_is_caught() -> None:
    """A narrowed dtype can compare equal by value and is still a different artifact."""

    entry = gate.compare_entry(_float_entry(), _float_entry().astype(np.float32))
    assert not entry["equal"]
    assert not entry["dtype_equal"]


def test_a_shape_change_is_caught() -> None:
    """A truncated array must never be compared element-wise and called equal."""

    entry = gate.compare_entry(_float_entry(), _float_entry()[:-1])
    assert not entry["equal"]
    assert not entry["shape_equal"]


def test_integer_and_string_entries_compare_without_nan_handling() -> None:
    """Non-float dtypes must not raise when NaN tolerance is unavailable."""

    assert gate.compare_entry(np.arange(4), np.arange(4))["equal"]
    assert not gate.compare_entry(np.arange(4), np.arange(4) + 1)["equal"]
    assert gate.compare_entry(np.asarray("dev-abc"), np.asarray("dev-abc"))["equal"]
    assert not gate.compare_entry(np.asarray("dev-abc"), np.asarray("dev-xyz"))["equal"]


# ---------------------------------------------------------------------------
# Payload comparison
# ---------------------------------------------------------------------------


def _payload() -> dict[str, np.ndarray]:
    return {
        "values__gauge_obs": _float_entry(),
        "valid__gauge_obs": np.asarray([True, False, True, True, False, True]),
        "config_hash": np.asarray("dev-" + "a" * 64),
        "step": np.arange(6),
    }


def test_an_identical_payload_passes() -> None:
    report = gate.compare_payload("payload", _payload(), _payload(), 4)
    assert report["entry_count"] == 4
    assert report["total_nan"] == 2


def test_a_missing_key_is_caught_before_any_array_is_touched() -> None:
    actual = _payload()
    del actual["values__gauge_obs"]
    with pytest.raises(gate.ProtocolPError, match="key sets differ"):
        gate.compare_payload("payload", _payload(), actual, 4)


def test_an_extra_key_is_caught() -> None:
    actual = _payload()
    actual["values__unexpected"] = np.zeros(6)
    with pytest.raises(gate.ProtocolPError, match="key sets differ"):
        gate.compare_payload("payload", _payload(), actual, 4)


def test_a_payload_of_the_wrong_size_is_refused() -> None:
    """The entry count is pre-registered; a payload that is not that size is a failure."""

    with pytest.raises(gate.ProtocolPError, match="expected 38 entries"):
        gate.compare_payload("payload", _payload(), _payload(), 38)


def test_a_changed_value_names_the_offending_entry() -> None:
    actual = _payload()
    actual["values__gauge_obs"] = actual["values__gauge_obs"] + 1.0
    with pytest.raises(gate.ProtocolPError, match="values__gauge_obs"):
        gate.compare_payload("payload", _payload(), actual, 4)


def test_a_restamped_provenance_hash_is_caught() -> None:
    """The replay must stamp the base config hash; a screen hash changes the bytes."""

    actual = _payload()
    actual["config_hash"] = np.asarray("dev-" + "b" * 64)
    with pytest.raises(gate.ProtocolPError, match="config_hash"):
        gate.compare_payload("payload", _payload(), actual, 4)


# ---------------------------------------------------------------------------
# Identity binding
# ---------------------------------------------------------------------------


@dataclasses.dataclass
class _Row:
    run_id: str
    sensor_seed: int
    pair_id: str


def test_a_matching_identity_row_passes() -> None:
    """CSV values are text, so the regenerated row is compared through ``str``."""

    retained = {"run_id": "r", "sensor_seed": "110762", "pair_id": "p"}
    report = gate.compare_manifest_row(retained, _Row("r", 110762, "p"))
    assert report["field_count"] == 3


def test_a_changed_identity_field_is_caught() -> None:
    """A different sensor seed is a different rollout, however similar the trace."""

    retained = {"run_id": "r", "sensor_seed": "110762", "pair_id": "p"}
    with pytest.raises(gate.ProtocolPError, match="sensor_seed"):
        gate.compare_manifest_row(retained, _Row("r", 999999, "p"))


def test_identity_field_set_drift_is_caught() -> None:
    retained = {"run_id": "r", "sensor_seed": "110762"}
    with pytest.raises(gate.ProtocolPError, match="identity field sets differ"):
        gate.compare_manifest_row(retained, _Row("r", 110762, "p"))


# ---------------------------------------------------------------------------
# Ephemerality snapshot
# ---------------------------------------------------------------------------


def test_an_undersized_snapshot_cannot_certify_that_nothing_was_written(
    tmp_path: Path,
) -> None:
    """A watch list that resolves to nothing would report a clean run forever.

    This is the guard against the failure mode the whole ephemerality check exists to
    avoid: reporting "no files changed" while watching no files.
    """

    with pytest.raises(gate.ProtocolPError, match="below the"):
        gate.inventory([])
    with pytest.raises(gate.ProtocolPError, match="below the"):
        gate.inventory([tmp_path])


def test_the_snapshot_diff_reports_additions_modifications_and_removals(
    tmp_path: Path,
) -> None:
    """A stray write from any layer of the stack has to be visible, not assumed away."""

    before = {"a": (1, 1), "b": (2, 2), "c": (3, 3)}
    after = {"a": (1, 1), "b": (2, 9), "d": (4, 4)}
    changes = gate.diff_inventory(before, after)
    assert changes["added"] == ["d"]
    assert changes["removed"] == ["c"]
    assert changes["modified"] == ["b"]


def test_the_snapshot_sees_a_real_file_appearing_under_a_watched_root(
    tmp_path: Path,
) -> None:
    """End-to-end on the filesystem, not only on hand-built mappings."""

    for index in range(gate.MIN_WATCHED_FILES):
        (tmp_path / f"f{index}.bin").write_bytes(b"x")
    before = gate.inventory([tmp_path])
    (tmp_path / "stray_artifact.json").write_text("{}", encoding="utf-8")
    after = gate.inventory([tmp_path])
    changes = gate.diff_inventory(before, after)
    assert [Path(path).name for path in changes["added"]] == ["stray_artifact.json"]
