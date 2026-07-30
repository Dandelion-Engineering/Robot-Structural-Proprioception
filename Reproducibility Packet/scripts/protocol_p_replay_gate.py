"""Protocol P section 7 replay gate: one-row exact reproduction, stop-or-go.

Purpose
-------
Protocol P is a pre-registered screen that will spend 169 MuJoCo rollouts deciding
whether the delivered diagnostic probe can make a structural stiffness-loss fault
measurable above the healthy run-to-run null.  Every one of those rollouts is built
through ``assignment_generator._generate_reservation``.  Before any of them runs, this
gate answers one narrow question about that construction path:

    Does rebuilding a single delivered reservation from the committed inputs reproduce
    the retained artifact exactly?

If it does not, the instrument that will produce the screen's numbers is not the
instrument that produced the development dataset, and no Protocol-P result would be
interpretable.  Section 7 therefore makes this a **stop-or-go precondition**: failure
means Stage A does not start.

What is checked
---------------
**I1 - pinned digests, each through its own hash domain.**  Protocol P pins files of
two disjoint kinds and applying the wrong helper to either one breaks the protocol:

* ``canonical_text_sha256`` (strip UTF-8 BOM, fold CRLF to LF) applies to exactly the
  protocol text and the approved assignment JSON.  The fold makes the digest invariant
  to the checkout convention; this repository is developed on Windows with
  ``core.autocrlf=true``, so an unpinned text file materializes as CRLF in a fresh
  clone.
* ``raw_file_sha256`` (exact bytes, no transformation) applies to exactly the two
  retained ``.npz`` replay references.  A ``.npz`` is a ZIP archive of NumPy buffers,
  and byte pairs equal to ``0d 0a`` occur inside that payload as *data*.  The two
  retained references contain 18 and 1 such pairs, so folding them changes both
  digests and would fail this gate deterministically.

The gate additionally recomputes the wrong-domain digest of each reference as a
**reported diagnostic** - never as an identity check - so that the domain split is
demonstrated live rather than asserted.

**I2 - array equality on replay.**  All 20 privileged plant fields and all 38 observed
``.npz`` payload entries must be equal.  The input is guarded by exact binary identity;
the output is guarded by array equality.  Byte-identity of a *regenerated* ``.npz`` is
not claimed, because ZIP container bytes are not a property of the data.

Provenance scope
----------------
The replay runs with ``overrides=None`` and therefore stamps the **base** config hash.
This is a requirement, not a default: ``config_hash`` is a stored field of the
``ObservedRecord``, so stamping anything else would change the artifact's bytes and
fail the 38-entry comparison by construction.  The replay rollout is explicitly out of
scope for invariant I8, which requires a base-distinct ``dev-`` provenance hash on
Stage A/B/C rollouts.

Ephemerality
------------
Section 7 and the reviewer's authorization both require this run to write no screen
artifact.  ``_generate_reservation`` writes no manifest, role index, observation, label
or dataset payload, and this script writes nothing at all - the evidence is stdout.
That claim is not taken on trust: the script inventories the data root, the packet tree
and the repository's top-level files before and after the rollout and reports every
difference, which is how a stray write from any layer of the stack would surface.

Deliberately out of scope
-------------------------
Invariant I13a (the runtime construction-equality check over the requested condition)
and the results-only persistence boundary belong to the Stage driver, not here.  Both
were deferred there by explicit reviewer decision, because this gate constructs no
override bundle and defines no output root.

Usage (from the Reproducibility Packet directory)
-------------------------------------------------
    ..\\venv\\Scripts\\python.exe scripts\\protocol_p_replay_gate.py \\
        --data-root <path to the retained dev/pilot/val dataset root>

Exit status is 0 only when every pinned digest matches and every one of the 58 compared
entries is equal.  Any failure raises ``ProtocolPError``; the protocol never uses
``assert``, because ``python -O`` removes assertions.
"""

from __future__ import annotations

import argparse
import csv
import dataclasses
import hashlib
import sys
import time
from pathlib import Path
from typing import Any, Iterable, Mapping, Sequence

import numpy as np

SCRIPT_DIR = Path(__file__).resolve().parent
if str(SCRIPT_DIR) not in sys.path:
    sys.path.insert(0, str(SCRIPT_DIR))

from utils.assignment_binding import validate_approved_assignment_binding  # noqa: E402
from utils.assignment_generator import (  # noqa: E402
    _generate_reservation,
    _plant_payload,
    _runtime_parameters,
    build_identity_manifest,
    screen_pair_id,
)
from utils.config_contract import load_config  # noqa: E402
from utils.gate3_assignment import load_assignment  # noqa: E402
from utils.schema_types import ObservedRecord, PrivilegedRecord  # noqa: E402

PACKET_ROOT = SCRIPT_DIR.parent
REPO_ROOT = PACKET_ROOT.parent

# ---------------------------------------------------------------------------
# Pinned identities.  Every value below is a pre-registered constant, not a
# tunable: changing one changes what this gate certifies.
# ---------------------------------------------------------------------------

# Text domain.  The protocol file cannot contain its own digest, so the expected
# value is carried here; it is the digest both agents independently computed and
# jointly approved (Claude Session 43 handoff, Codex Session 43 approval).
PROTOCOL_FILENAME = "protocol-p-v2.3.3.md"
PROTOCOL_CANONICAL_SHA256 = (
    "5689dad7ce4194b9a7dbe381006027df178997adf732f5734a77ef048bdf421f"
)
# Pinned by Protocol P Correction 3.
ASSIGNMENT_FILENAME = "proposed-gate3-assignment-v0.1.json"
ASSIGNMENT_CANONICAL_SHA256 = (
    "76255a8089f3e27d893b26d981cbf50e808bd75ba518c44b55c4635ec83514ae"
)

# Binary domain.  Pinned by Protocol P section 7.
PLANT_REFERENCE_RAW_SHA256 = (
    "ed5b1f39f4ba535c60eb3e1b8587c7b03f59a5c3f9c1189b55635f0d49b65e45"
)
OBSERVATION_REFERENCE_RAW_SHA256 = (
    "cdde17f6d32c5d648249f4a9b343ec3f997b04c83cadacbf9d2c5f1186bb4c83"
)

# Wrong-domain digests of the two binary references, recorded in Protocol P
# section 0 as the measurement that justifies the domain split.  Reproduced here
# as a diagnostic only.  These values must NEVER be accepted as an identity.
PLANT_REFERENCE_TEXT_FOLDED_SHA256 = (
    "638e384f3a75c4cefb360e7b7815e7a1b9f5dcd2e01c2cbb718410db9964c575"
)
OBSERVATION_REFERENCE_TEXT_FOLDED_SHA256 = (
    "0051ea132a783264c47a370184f0d328e2ae4c3a95ad227b3cf9c181c599435e"
)
PLANT_REFERENCE_CRLF_PAIRS = 18
OBSERVATION_REFERENCE_CRLF_PAIRS = 1

# The replayed row (Protocol P section 7).
SCENARIO_SPEC_ID = "scenario_dev_t01_f000_r00"
REPLAY_SUITE = "S"
RUN_ID = f"{SCENARIO_SPEC_ID}_{REPLAY_SUITE}_dataset0"

# The delivered dataset was materialized over these splits and suites.  They are
# passed explicitly rather than defaulted because the generator's suite default is
# ("C0", "C1", "S"), which is not what produced the retained references.
DELIVERED_SPLITS = ("dev", "pilot", "val")
DELIVERED_SUITES = ("C1", "S")

N_PRIVILEGED_FIELDS = 20
N_OBSERVATION_ENTRIES = 38

# Floor on the ephemerality snapshot. The retained dataset alone holds thousands of
# files, so anything near zero means the watch list resolved to nothing and the
# "wrote nothing" report would be certifying an empty set.
MIN_WATCHED_FILES = 100


class ProtocolPError(RuntimeError):
    """A Protocol-P invariant failed.

    Protocol P section 10 requires every decision-bearing invariant to raise rather
    than assert, because ``python -O`` removes assertions and would silently disable
    the guard.
    """


def _require(condition: bool, message: str) -> None:
    """Raise ``ProtocolPError(message)`` unless ``condition`` holds.

    Inputs: a already-evaluated boolean and the message to fail with.
    Outputs: none. Purpose: a fail-loud replacement for ``assert``.
    """

    if not condition:
        raise ProtocolPError(message)


def canonical_text_sha256(path: Path) -> str:
    """Protocol P text-domain digest of ``path``.

    Inputs: a path to a tracked text file. Outputs: hex SHA-256 of the file's bytes
    after stripping a UTF-8 BOM and folding CRLF to LF, which makes the digest
    invariant to the checkout line-ending convention.
    """

    raw = path.read_bytes()
    if raw.startswith(b"\xef\xbb\xbf"):
        raw = raw[3:]
    return hashlib.sha256(raw.replace(b"\r\n", b"\n")).hexdigest()


def raw_file_sha256(path: Path) -> str:
    """Protocol P binary-domain digest of ``path``.

    Inputs: a path to a binary artifact. Outputs: hex SHA-256 of its exact bytes with
    no transformation whatsoever. Purpose: identity for the retained ``.npz``
    references, whose payloads contain CRLF byte pairs as data.
    """

    return hashlib.sha256(path.read_bytes()).hexdigest()


def check_pinned_digests(
    protocol_path: Path, assignment_path: Path, plant_path: Path, observation_path: Path
) -> dict[str, Any]:
    """Invariant I1: every pinned digest present and unchanged, in its own domain.

    Inputs: the four pinned paths. Outputs: a report mapping of the computed digests
    and the wrong-domain diagnostics. Purpose: refuse to run the replay against inputs
    that are not the pre-registered ones. Raises ``ProtocolPError`` on any absence,
    filename drift, or digest mismatch.
    """

    for path in (protocol_path, assignment_path, plant_path, observation_path):
        _require(path.is_file(), f"I1: pinned input is absent: {path}")

    # A version bump must fail loudly here rather than silently compare a digest
    # against a different file than the one it was approved for.
    _require(
        protocol_path.name == PROTOCOL_FILENAME,
        f"I1: expected protocol file {PROTOCOL_FILENAME!r}, got {protocol_path.name!r}",
    )
    _require(
        assignment_path.name == ASSIGNMENT_FILENAME,
        f"I1: expected assignment file {ASSIGNMENT_FILENAME!r}, "
        f"got {assignment_path.name!r}",
    )

    text_pins = (
        ("protocol", protocol_path, PROTOCOL_CANONICAL_SHA256),
        ("assignment", assignment_path, ASSIGNMENT_CANONICAL_SHA256),
    )
    binary_pins = (
        ("plant_reference", plant_path, PLANT_REFERENCE_RAW_SHA256),
        ("observation_reference", observation_path, OBSERVATION_REFERENCE_RAW_SHA256),
    )

    report: dict[str, Any] = {"text": {}, "binary": {}, "domain_diagnostic": {}}

    for name, path, expected in text_pins:
        actual = canonical_text_sha256(path)
        _require(
            actual == expected,
            f"I1: {name} canonical text digest mismatch\n"
            f"    path     {path}\n"
            f"    expected {expected}\n"
            f"    actual   {actual}",
        )
        raw = raw_file_sha256(path)
        report["text"][name] = {
            "path": str(path),
            "bytes": path.stat().st_size,
            "canonical_sha256": actual,
            "raw_sha256": raw,
            "raw_equals_canonical": raw == actual,
        }

    for name, path, expected in binary_pins:
        actual = raw_file_sha256(path)
        _require(
            actual == expected,
            f"I1: {name} raw byte digest mismatch\n"
            f"    path     {path}\n"
            f"    expected {expected}\n"
            f"    actual   {actual}",
        )
        report["binary"][name] = {
            "path": str(path),
            "bytes": path.stat().st_size,
            "raw_sha256": actual,
        }

    # Domain-separation diagnostic.  Recomputes the wrong-domain digest of each
    # binary reference and requires it to reproduce the value Protocol P section 0
    # records AND to differ from the pinned identity.  This is evidence that the
    # split is real in this run; it is never used as an identity.
    folded_expectations = (
        ("plant_reference", plant_path, PLANT_REFERENCE_TEXT_FOLDED_SHA256,
         PLANT_REFERENCE_CRLF_PAIRS, PLANT_REFERENCE_RAW_SHA256),
        ("observation_reference", observation_path,
         OBSERVATION_REFERENCE_TEXT_FOLDED_SHA256,
         OBSERVATION_REFERENCE_CRLF_PAIRS, OBSERVATION_REFERENCE_RAW_SHA256),
    )
    for name, path, expected_folded, expected_pairs, pinned_raw in folded_expectations:
        folded = canonical_text_sha256(path)
        pairs = path.read_bytes().count(b"\r\n")
        _require(
            folded == expected_folded,
            f"I1 diagnostic: {name} text-folded digest does not reproduce the value "
            f"recorded in Protocol P section 0\n"
            f"    expected {expected_folded}\n"
            f"    actual   {folded}",
        )
        _require(
            pairs == expected_pairs,
            f"I1 diagnostic: {name} CRLF pair count changed: "
            f"expected {expected_pairs}, got {pairs}",
        )
        _require(
            folded != pinned_raw,
            f"I1 diagnostic: {name} folded digest equals the pinned raw digest, "
            "so this run cannot demonstrate the domain split",
        )
        report["domain_diagnostic"][name] = {
            "crlf_pairs": pairs,
            "text_folded_sha256": folded,
            "differs_from_pinned_raw": True,
        }

    return report


def load_npz_entries(path: Path) -> dict[str, np.ndarray]:
    """Read every entry of a non-pickled ``.npz`` into an in-memory mapping.

    Inputs: a path to an ``.npz`` archive. Outputs: ``{key: ndarray}`` materialized
    before the archive handle closes. Purpose: give the comparison a plain mapping so
    it cannot accidentally hold a lazy handle open.
    """

    with np.load(path, allow_pickle=False) as data:
        return {key: data[key] for key in data.files}


def compare_entry(expected: np.ndarray, actual: np.ndarray) -> dict[str, Any]:
    """Compare one array entry exactly, treating NaN as equal to NaN.

    Inputs: the retained expected array and the regenerated actual array.
    Outputs: a mapping with dtype/shape/value equality and the NaN count.
    Purpose: NaN-aware exact equality. ``gauge_obs`` carries real NaNs from dropout
    and latency, so a plain ``==`` comparison would report a correct replay as failed.
    """

    expected = np.asarray(expected)
    actual = np.asarray(actual)
    dtype_equal = expected.dtype == actual.dtype
    shape_equal = expected.shape == actual.shape
    nan_count = (
        int(np.count_nonzero(np.isnan(expected))) if expected.dtype.kind in "fc" else 0
    )
    if not shape_equal:
        values_equal = False
    elif expected.dtype.kind in "fc":
        values_equal = bool(np.array_equal(expected, actual, equal_nan=True))
    else:
        values_equal = bool(np.array_equal(expected, actual))
    return {
        "dtype": str(expected.dtype),
        "shape": tuple(expected.shape),
        "nan_count": nan_count,
        "dtype_equal": dtype_equal,
        "shape_equal": shape_equal,
        "values_equal": values_equal,
        "equal": bool(dtype_equal and shape_equal and values_equal),
    }


def compare_payload(
    label: str,
    expected: Mapping[str, np.ndarray],
    actual: Mapping[str, np.ndarray],
    expected_count: int,
) -> dict[str, Any]:
    """Invariant I2 for one payload: exact key set and exact per-entry equality.

    Inputs: a human label, the retained mapping, the regenerated mapping, and the
    pre-registered entry count. Outputs: a per-entry report. Purpose: an extra or
    missing key is a failure in its own right, so the key sets are compared before
    any array is touched. Raises ``ProtocolPError`` on key-set drift, on a count that
    does not match the pre-registered number, or on any unequal entry.
    """

    expected_keys = set(expected)
    actual_keys = set(actual)
    _require(
        expected_keys == actual_keys,
        f"I2 [{label}]: key sets differ\n"
        f"    only in retained:    {sorted(expected_keys - actual_keys)}\n"
        f"    only in regenerated: {sorted(actual_keys - expected_keys)}",
    )
    _require(
        len(expected_keys) == expected_count,
        f"I2 [{label}]: expected {expected_count} entries, found {len(expected_keys)}",
    )

    entries = {
        key: compare_entry(expected[key], actual[key]) for key in sorted(expected_keys)
    }
    mismatched = [key for key, entry in entries.items() if not entry["equal"]]
    _require(
        not mismatched,
        f"I2 [{label}]: {len(mismatched)} of {expected_count} entries differ: "
        f"{mismatched}",
    )
    return {
        "entries": entries,
        "entry_count": len(entries),
        "nan_entries": sum(1 for e in entries.values() if e["nan_count"]),
        "total_nan": sum(e["nan_count"] for e in entries.values()),
    }


def inventory(roots: Sequence[Path]) -> dict[str, tuple[int, int]]:
    """Snapshot ``{path: (size_bytes, mtime_ns)}`` for an ephemerality check.

    Inputs: directories (walked recursively) and/or individual files. Outputs: a flat
    mapping. Purpose: the section-7 replay must write nothing; comparing two snapshots
    across the rollout is what makes that claim falsifiable rather than assumed.
    """

    found: dict[str, tuple[int, int]] = {}
    for root in roots:
        if root.is_file():
            stat = root.stat()
            found[str(root)] = (stat.st_size, stat.st_mtime_ns)
            continue
        if not root.is_dir():
            continue
        for path in root.rglob("*"):
            if path.is_file():
                stat = path.stat()
                found[str(path)] = (stat.st_size, stat.st_mtime_ns)
    # An empty or near-empty snapshot would report "nothing was written" while
    # watching nothing.  A green check that cannot go red is worse than none, so
    # refuse to certify ephemerality from a snapshot that cannot carry the claim.
    _require(
        len(found) >= MIN_WATCHED_FILES,
        f"ephemerality snapshot covers only {len(found)} files across "
        f"{len(roots)} roots, below the {MIN_WATCHED_FILES} required for the "
        "no-write claim to mean anything",
    )
    return found


def diff_inventory(
    before: Mapping[str, tuple[int, int]], after: Mapping[str, tuple[int, int]]
) -> dict[str, list[str]]:
    """Report added, removed and modified files between two inventories.

    Inputs: two mappings from :func:`inventory`. Outputs: sorted path lists per
    category. Purpose: surface every filesystem effect of the rollout so it can be
    reported honestly rather than claimed away.
    """

    before_keys = set(before)
    after_keys = set(after)
    return {
        "added": sorted(after_keys - before_keys),
        "removed": sorted(before_keys - after_keys),
        "modified": sorted(
            key for key in before_keys & after_keys if before[key] != after[key]
        ),
    }


def read_manifest_row(manifest_path: Path, run_id: str) -> dict[str, str]:
    """Return the single retained manifest row for ``run_id``.

    Inputs: the delivered ``manifest.csv`` path and the target run identifier.
    Outputs: the row as a string mapping. Purpose: bind the replayed reservation to
    the identity that actually produced the retained references, instead of trusting
    the run-identifier naming convention. Raises if the row is absent or duplicated.
    """

    with open(manifest_path, newline="", encoding="utf-8") as handle:
        rows = [row for row in csv.DictReader(handle) if row["run_id"] == run_id]
    _require(
        len(rows) == 1,
        f"expected exactly one retained manifest row for run_id {run_id!r}, "
        f"found {len(rows)}",
    )
    return rows[0]


def compare_manifest_row(
    retained: Mapping[str, str], regenerated: Any
) -> dict[str, Any]:
    """Compare the regenerated identity row against the retained manifest row.

    Inputs: the retained CSV row and the regenerated ``IdentityManifestRow``.
    Outputs: a per-field report. Purpose: prove the reservation being replayed is the
    one that produced the pinned references. CSV values are text, so each regenerated
    field is compared through ``str``; that is the same rendering the writer used.
    """

    fields = [field.name for field in dataclasses.fields(regenerated)]
    _require(
        set(fields) == set(retained),
        f"identity field sets differ\n"
        f"    only in regenerated: {sorted(set(fields) - set(retained))}\n"
        f"    only in retained:    {sorted(set(retained) - set(fields))}",
    )
    values = {name: str(getattr(regenerated, name)) for name in fields}
    mismatched = [name for name in fields if values[name] != retained[name]]
    _require(
        not mismatched,
        "regenerated identity row differs from the retained manifest row in "
        f"{mismatched}",
    )
    return {"field_count": len(fields), "values": values}


def run_replay(
    config_path: Path, schema_path: Path, assignment_path: Path
) -> dict[str, Any]:
    """Rebuild the pinned reservation through the Protocol P section 4 path.

    Inputs: the draft config, the machine schema and the approved assignment.
    Outputs: a mapping carrying the regenerated plant record, the regenerated ``S``
    observation, the identity row, the base config hash and the wall-clock cost.
    Purpose: this is the section 4 construction path verbatim - the closed loop is
    driven by a ``C0`` session and ``S`` is produced afterwards from the privileged
    record at the same realized identity. No online-``S`` variant is authorized.
    """

    config = load_config(config_path, schema_path)
    assignment = load_assignment(assignment_path)
    binding = validate_approved_assignment_binding(config, expected_assignment=assignment)
    runtime = _runtime_parameters(binding)
    history_steps = int(config.document["values"]["timing"]["window_steps"])

    rows, reservations = build_identity_manifest(
        binding, splits=DELIVERED_SPLITS, suites=DELIVERED_SUITES
    )
    selected = [
        item for item in reservations if item.scenario_spec_id == SCENARIO_SPEC_ID
    ]
    _require(
        len(selected) == 1,
        f"expected exactly one reservation for {SCENARIO_SPEC_ID!r}, "
        f"found {len(selected)}",
    )
    reservation = selected[0]

    selected_rows = [row for row in rows if row.run_id == RUN_ID]
    _require(
        len(selected_rows) == 1,
        f"expected exactly one regenerated identity row for {RUN_ID!r}, "
        f"found {len(selected_rows)}",
    )
    identity_row = selected_rows[0]

    # With overrides=None the seam must fall back to the delivered dataset identity.
    derived_pair_id = screen_pair_id(reservation, None)
    _require(
        derived_pair_id == identity_row.pair_id,
        "the overrides=None identity path does not reproduce the delivered pair id: "
        f"{derived_pair_id!r} != {identity_row.pair_id!r}",
    )

    started = time.perf_counter()
    (
        control_pair_id,
        plant_record,
        observations,
        _label_payload,
        safety_events,
        contact_steps,
    ) = _generate_reservation(
        binding.assignment,
        config.config_hash,
        (REPLAY_SUITE,),
        None,
        history_steps,
        runtime,
        reservation,
        overrides=None,
    )
    elapsed_s = time.perf_counter() - started

    _require(
        control_pair_id == identity_row.pair_id,
        f"regenerated pair id {control_pair_id!r} != {identity_row.pair_id!r}",
    )
    _require(
        set(observations) == {REPLAY_SUITE},
        f"expected only the {REPLAY_SUITE!r} observation, got {sorted(observations)}",
    )

    return {
        "config_hash": config.config_hash,
        "assignment_hash": binding.assignment_hash,
        "history_steps": history_steps,
        "reservation": reservation,
        "identity_row": identity_row,
        "plant": plant_record,
        "observation": observations[REPLAY_SUITE],
        "safety_events": safety_events,
        "contact_steps": contact_steps,
        "elapsed_s": elapsed_s,
    }


def parse_args(argv: Sequence[str] | None = None) -> argparse.Namespace:
    """Parse command-line arguments.

    Inputs: an optional argument vector. Outputs: the parsed namespace. Purpose:
    packet-relative defaults for committed inputs; ``--data-root`` is required
    because the retained references are machine-local and git-ignored.
    """

    parser = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    parser.add_argument(
        "--data-root",
        type=Path,
        required=True,
        help="root of the retained dev/pilot/val dataset holding the pinned references",
    )
    parser.add_argument("--schema", type=Path, default=Path("schema/schema.json"))
    parser.add_argument(
        "--config", type=Path, default=Path("config/draft-config-v0.1.json")
    )
    parser.add_argument(
        "--assignment",
        type=Path,
        default=Path(f"config/{ASSIGNMENT_FILENAME}"),
    )
    parser.add_argument(
        "--protocol",
        type=Path,
        default=Path(f"protocol/{PROTOCOL_FILENAME}"),
    )
    return parser.parse_args(argv)


def _print_header(title: str) -> None:
    """Print a section banner. Inputs: a title. Outputs: none."""

    print()
    print(title)
    print("-" * len(title))


def main(argv: Sequence[str] | None = None) -> int:
    """Run the section 7 replay gate end to end.

    Inputs: an optional argument vector. Outputs: process exit status, 0 only when
    every pinned digest matches and all 58 compared entries are equal.
    """

    args = parse_args(argv)
    data_root = args.data_root.resolve()
    plant_reference = data_root / "plant" / f"{RUN_ID}.npz"
    observation_reference = data_root / "observations" / REPLAY_SUITE / f"{RUN_ID}.npz"

    print("Protocol P section 7 - replay gate")
    print("=" * 34)
    print(f"run_id      {RUN_ID}")
    print(f"data root   {data_root}")
    print(f"packet root {PACKET_ROOT}")

    _print_header("I1 - pinned digests, each through its own domain")
    digests = check_pinned_digests(
        args.protocol.resolve(),
        args.assignment.resolve(),
        plant_reference,
        observation_reference,
    )
    for name, entry in digests["text"].items():
        print(f"  text   {name:22s} {entry['bytes']:>9,d} B  {entry['canonical_sha256']}")
        print(
            f"         {'':22s} {'raw':>9s}    {entry['raw_sha256']}"
            f"   raw==canonical {entry['raw_equals_canonical']}"
        )
    for name, entry in digests["binary"].items():
        print(f"  binary {name:22s} {entry['bytes']:>9,d} B  {entry['raw_sha256']}")
    print("  domain-separation diagnostic (reported, never used as an identity):")
    for name, entry in digests["domain_diagnostic"].items():
        print(
            f"    {name:22s} CRLF pairs {entry['crlf_pairs']:>3d}  "
            f"text-folded {entry['text_folded_sha256']}"
        )
    print("  I1 PASS")

    watched = [data_root, PACKET_ROOT] + [
        path for path in REPO_ROOT.iterdir() if path.is_file()
    ]
    before = inventory(watched)

    _print_header("Replay - Protocol P section 4 construction path, overrides=None")
    replay = run_replay(
        args.config.resolve(), args.schema.resolve(), args.assignment.resolve()
    )
    after = inventory(watched)
    plant: PrivilegedRecord = replay["plant"]
    observation: ObservedRecord = replay["observation"]
    print(f"  base config hash   {replay['config_hash']}")
    print(f"  assignment hash    {replay['assignment_hash']}")
    print(f"  history_steps      {replay['history_steps']}")
    print(f"  steps simulated    {plant.n_steps}")
    print(f"  safety events      {replay['safety_events']}")
    print(f"  contact steps      {replay['contact_steps']}")
    print(f"  rollout wall clock {replay['elapsed_s']:.2f} s")

    _print_header("Identity binding - replayed reservation vs retained manifest row")
    retained_row = read_manifest_row(data_root / "manifest.csv", RUN_ID)
    identity = compare_manifest_row(retained_row, replay["identity_row"])
    print(f"  all {identity['field_count']} identity fields equal")
    for name in ("pair_id", "sensor_seed", "fault_setting_id", "config_hash"):
        print(f"    {name:18s} {identity['values'][name]}")

    # Provenance scope (Protocol P section 0): the replay MUST stamp the base hash.
    _require(
        observation.config_hash == replay["config_hash"],
        "provenance scope: the replay stamped "
        f"{observation.config_hash!r} instead of the base config hash "
        f"{replay['config_hash']!r}",
    )
    _require(
        retained_row["config_hash"] == replay["config_hash"],
        "the retained row was generated under a different config hash than the one "
        "this replay loaded",
    )
    print("  provenance scope   base config hash stamped, as section 0 requires")

    _print_header("I2 - array equality on replay")
    plant_report = compare_payload(
        "plant, 20 privileged fields",
        load_npz_entries(plant_reference),
        _plant_payload(plant),
        N_PRIVILEGED_FIELDS,
    )
    print(
        f"  plant        {plant_report['entry_count']}/{N_PRIVILEGED_FIELDS} "
        f"fields equal (dtype, shape and values)"
    )
    observation_report = compare_payload(
        "observation, 38 npz entries",
        load_npz_entries(observation_reference),
        observation.to_npz_dict(),
        N_OBSERVATION_ENTRIES,
    )
    print(
        f"  observation  {observation_report['entry_count']}/{N_OBSERVATION_ENTRIES} "
        f"entries equal (dtype, shape and values)"
    )
    print(
        f"  NaN-bearing entries compared: {observation_report['nan_entries']} "
        f"({observation_report['total_nan']:,d} NaN values, matched position for "
        "position)"
    )
    print("  I2 PASS")

    _print_header("Ephemerality - filesystem effect of this run")
    print(
        f"  watched {len(before):,d} files across {len(watched)} roots "
        "(retained data root, packet tree, repository top-level files)"
    )
    changes = diff_inventory(before, after)
    for category in ("added", "modified", "removed"):
        paths = changes[category]
        print(f"  {category:9s} {len(paths)}")
        for path in paths:
            print(f"    {path}")
    print("  (no screen artifact is written; this gate's output is stdout only)")

    _print_header("Result")
    print("  REPLAY_GATE_PASS - one row, exact. Stage A's precondition is met.")
    print("  Achieved scope is ONE ROW. No dataset-wide reproduction is claimed.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
