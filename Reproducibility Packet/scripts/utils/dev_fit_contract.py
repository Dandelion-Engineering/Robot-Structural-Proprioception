"""Gate-4's development-only fitting contract: what a dev fit may read, and what it must record.

Codex ruled in its Session 77 that fitting Gate-4 rung 1 against the **already
delivered** `dev` partition is authorized as *development evidence*, because training
consumes persisted rows and generates nothing. The authority is deliberately narrow, and
its five bounds are:

1. only rows whose persisted role is exactly `dev`, from the jointly approved delivered
   base dataset; no pilot, validation or test outcome may be read in this step;
2. no new plant, sensor, label or role payload — zero physical rollouts;
3. the same architecture and training protocol across the matched suites, over a
   predeclared set of at least five independent training seeds (Slot 7);
4. every checkpoint and result is development-only, carries the exact authority string,
   and records at least the dev data root, the manifest / config / assignment digests,
   the suite, the training seed, the training-protocol code identity, and the checkpoint
   digest; and
5. a dev fit may show that the implementation learns and may expose failure modes, but
   may not set validation-owned probability, detection, abstention, OOD or calibrated
   uncertainty thresholds, may not select a headline capacity, and may not become a
   research result.

This module is the executable form of bounds 1, 3 and 4. Bound 2 is a property of what
the trainer does *not* import (no generator, no plant); bound 5 lives in
`utils.attribution_net`, whose thresholds default to `None` and whose
`severity_uncertainty` stays `+inf` until Gate 5 calibrates it.

Why this is a separate module from the trainer
----------------------------------------------
The refusals here have to be reviewable on their own. A role check buried inside a
training loop is exercised only by running the loop, and the exit paths of a program are
the region no test enters (Session 65). Everything below is a pure function over data a
test can construct, so the state each refusal exists to catch can be built directly.

Two names that must not be confused
-----------------------------------
`IdentityManifestRow.train_seed` is the **data-generation** seed already stamped on every
delivered row. `PREDECLARED_TRAINING_SEEDS` here are **network-initialization** seeds in
an independent namespace, chosen before any fit and shared across suites so that a
matched C1-vs-S comparison pairs seed to seed. They are different quantities with similar
names, which is exactly the shape that travels into a write-up unnoticed.
"""

from __future__ import annotations

import re
from dataclasses import dataclass, field
from pathlib import Path, PureWindowsPath
from typing import Iterable, Mapping, Sequence

from .protocol_p import ASSIGNMENT_CANONICAL_SHA256, canonical_json, canonical_text_sha256
from .storage_contract import IdentityManifestRow, read_identity_manifest

# The exact authority every development-only artifact in this project carries. It is
# reproduced here as a literal and pinned by EQUALITY against the payload-boundary
# extension's own constant in `tests/test_dev_fit_contract.py` — requirement (r): a
# literal copied from another file is a second COPY, not a second source, so the copy is
# only safe while something compares the two.
DEVELOPMENT_ONLY_AUTHORITY = (
    "DEVELOPMENT ONLY: ineligible for confirmatory analysis; cannot change Protocol P "
    "outcome or role-coverage counts."
)

# Bound 1. `dev` is the only role a fit may read; the other three are withheld.
AUTHORIZED_FIT_SPLIT = "dev"
WITHHELD_SPLITS = ("pilot", "val", "test")

# Bound 3. The matched pair the confirmatory comparison is about, and the only two
# suites the delivered base dataset carries. C0 is a Claim-Sheet suite with no delivered
# observations, so a fit naming it would be reading data that does not exist.
MATCHED_FIT_SUITES = ("C1", "S")

# Bound 3. Five explicitly named integers rather than "five seeds" — a range decided at
# run time is not predeclared. The same five are used in BOTH suites so the paired
# comparison pairs seed to seed and both arms start from identical initial weights.
PREDECLARED_TRAINING_SEEDS = (0, 1, 2, 3, 4)

_HEX64 = re.compile(r"^[0-9a-f]{64}$")
_DEV_HEX64 = re.compile(r"^dev-[0-9a-f]{64}$")

# `require_bare_name`'s one name-based exception, written out rather than hidden in a
# pattern (Session 70). `PurePath("..").name` is `".."`, so the "equals its own final
# component" predicate accepts it — while joining it to a root walks *up* the tree.
# `PurePath(".").name` is `""` and is already refused by the same predicate; the pair is
# listed together anyway so the rule reads as one decision instead of two accidents.
RESERVED_COMPONENT_NAMES = (".", "..")


class DevFitContractError(RuntimeError):
    """A development-only fitting bound was violated.

    Raised rather than asserted: `python -O` removes assertions, and a bound that
    disappears under an optimization flag is not a bound (Protocol P section 10).
    """


def require(condition: bool, message: str) -> None:
    """Raise `DevFitContractError(message)` unless `condition` holds.

    Inputs: an already-evaluated boolean and the message to fail with.
    Outputs: none. Purpose: a fail-loud replacement for `assert`.
    """

    if not condition:
        raise DevFitContractError(message)


def require_bare_name(value: str, field_name: str) -> str:
    """Return `value` unchanged if it is a bare name; refuse anything path-shaped.

    Inputs: a candidate string and the name of the field it will be recorded under.
    Outputs: the same string. Purpose: no result artifact in this packet may record an
    absolute filesystem path (requirement (z), Session 56), and the way that rule has
    failed before is a value that is *nearly* a name. The predicate is total rather than
    a list of spellings: a string is a bare name only if it equals its own final
    component, which refuses `/a/b`, `C:\\a\\b`, `//host/share`, a bare drive designator
    and a trailing separator alike (Session 67 — make the predicate the post-condition,
    do not enumerate spellings).

    `PureWindowsPath` alone, deliberately. The obvious form of this check is a
    conjunction over both flavours, and that conjunction was written first — but
    `PureWindowsPath` is a *pure* path type whose parsing does not depend on the host,
    and it is strictly the stronger parser: it treats both separators, drive designators
    and UNC roots as structure while `PurePosixPath` treats `\\` and `C:` as ordinary
    name characters. Measured over a 3,564-string enumeration (11 cores crossed with 18
    prefixes and 18 suffixes) in Session 78: 1,009 strings the Windows parser refuses and
    the POSIX parser accepts, and **zero** the other way. The POSIX conjunct rejected
    nothing, so it was removed rather than left looking authoritative (Session 61 —
    ask of adjacent guards what the first one alone rejects, and delete it if the answer
    is "nothing").

    The refusal names the field and the rejected value's final component only, never the
    value, because a message that quotes the offending path is the leak the rule exists
    to prevent.
    """

    require(
        isinstance(value, str) and value.strip() != "",
        f"{field_name} must be a non-empty string",
    )
    require(
        value not in RESERVED_COMPONENT_NAMES,
        f"{field_name} must not be a reserved path component "
        f"{list(RESERVED_COMPONENT_NAMES)}",
    )
    final_component = PureWindowsPath(value).name
    require(
        value == final_component,
        f"{field_name} must be a bare name, not a path "
        f"(final component {final_component or '<empty>'!r})",
    )
    return value


def require_predeclared_seed(seed: int) -> int:
    """Return `seed` if it is one of the predeclared training seeds, else refuse.

    Inputs: a candidate network-initialization seed. Outputs: the same seed as `int`.
    Purpose: bound 3. A seed invented at run time is not predeclared, and a fit at an
    unlisted seed is a fit nobody agreed to before seeing its result.
    """

    require(
        isinstance(seed, int) and not isinstance(seed, bool),
        "training_seed must be an int (bool is not an int here)",
    )
    require(
        seed in PREDECLARED_TRAINING_SEEDS,
        f"training seed {seed} is not predeclared; the set is "
        f"{list(PREDECLARED_TRAINING_SEEDS)}",
    )
    return int(seed)


def require_matched_fit_suite(suite: str) -> str:
    """Return `suite` if it is one of the matched suites, else refuse.

    Inputs: a candidate suite label. Outputs: the same label. Purpose: bound 3 and
    Slot 5's matched ablation — the delivered base dataset carries C1 and S only.
    """

    require(
        suite in MATCHED_FIT_SUITES,
        f"suite {suite!r} is not one of the matched fit suites "
        f"{list(MATCHED_FIT_SUITES)}",
    )
    return suite


def matched_fit_plan() -> tuple[tuple[str, int], ...]:
    """Return the full predeclared `(suite, seed)` plan, in a fixed order.

    Inputs: none. Outputs: every matched suite crossed with every predeclared seed —
    the complete set of fits bound 3 authorizes, and nothing else. Purpose: the plan is
    a value the trainer iterates rather than a loop it writes, so "what was supposed to
    run" is readable without reading the trainer.
    """

    return tuple(
        (suite, seed) for suite in MATCHED_FIT_SUITES for seed in PREDECLARED_TRAINING_SEEDS
    )


def require_complete_matched_plan(completed: Iterable[tuple[str, int]]) -> None:
    """Refuse a fit set that is not balanced across the matched suites.

    Inputs: the `(suite, seed)` pairs actually completed. Outputs: none.
    Purpose: a paired C1-vs-S comparison is only paired if both arms ran the same seeds.
    An unbalanced set still produces a difference — it is simply a difference between two
    different seed populations, which is the confound Slot 5 holds everything else fixed
    to avoid. Refusing here means the trainer cannot report a comparison it did not earn.
    """

    done = set(completed)
    expected = set(matched_fit_plan())
    missing = sorted(expected - done)
    unexpected = sorted(done - expected)
    require(
        not unexpected,
        f"fits ran outside the predeclared plan: {unexpected}",
    )
    require(
        not missing,
        f"the matched plan is incomplete; missing {missing}",
    )


@dataclass(frozen=True)
class DevRowCensus:
    """The denominator of a dev selection: what was there, and what was withheld.

    A filter that silently drops rows reports a clean number over an undisclosed
    denominator (requirement (p), Session 45). Every count a selection implies is
    therefore carried out of the selection rather than recomputed by whoever reads it.
    """

    total_rows: int
    rows_by_split: Mapping[str, int]
    rows_by_suite: Mapping[str, int]
    selected_rows: int
    withheld_rows: int

    def disclosure(self) -> str:
        """Return the one-line denominator sentence a result artifact must carry."""

        by_split = ", ".join(f"{name} {count}" for name, count in sorted(self.rows_by_split.items()))
        by_suite = ", ".join(f"{name} {count}" for name, count in sorted(self.rows_by_suite.items()))
        return (
            f"{self.selected_rows} of {self.total_rows} manifest rows selected "
            f"(split: {by_split}; suite of selected: {by_suite}); "
            f"{self.withheld_rows} withheld as non-{AUTHORIZED_FIT_SPLIT}."
        )


def select_dev_rows(
    manifest_path: Path | str, *, suites: Sequence[str] = MATCHED_FIT_SUITES
) -> tuple[list[IdentityManifestRow], DevRowCensus]:
    """Select the `dev` rows of `suites` from one identity manifest, with its census.

    Inputs: a path to a schema-A identity manifest and the suites to keep.
    Outputs: the selected rows and a `DevRowCensus` naming every count the selection
    implies. Purpose: bound 1, made into the only supported way a fit obtains rows.

    Refuses rather than returns an empty list when the manifest carries no `dev` row of
    the requested suites: a fit over zero rows is a defect, and a silent empty selection
    is how it reaches the training loop looking like data.
    """

    for suite in suites:
        require_matched_fit_suite(suite)
    rows = read_identity_manifest(Path(manifest_path))
    by_split: dict[str, int] = {}
    for row in rows:
        by_split[row.split] = by_split.get(row.split, 0) + 1
    selected = [
        row for row in rows if row.split == AUTHORIZED_FIT_SPLIT and row.suite in suites
    ]
    by_suite: dict[str, int] = {}
    for row in selected:
        by_suite[row.suite] = by_suite.get(row.suite, 0) + 1
    census = DevRowCensus(
        total_rows=len(rows),
        rows_by_split=dict(sorted(by_split.items())),
        rows_by_suite=dict(sorted(by_suite.items())),
        selected_rows=len(selected),
        withheld_rows=len(rows) - len(selected),
    )
    require(
        selected != [],
        f"no {AUTHORIZED_FIT_SPLIT} row of suites {list(suites)} in the manifest; "
        f"{census.disclosure()}",
    )
    return selected, census


def require_dev_only(rows: Iterable[IdentityManifestRow]) -> None:
    """Refuse a row set that contains any withheld role.

    Inputs: the rows a fit is about to consume. Outputs: none. Purpose: bound 1 checked
    at the point of consumption rather than only at the point of selection, because the
    selection is not the only way rows can arrive — a caller can pass a list it built
    itself, and that is the path no filter guards.
    """

    offenders: dict[str, int] = {}
    for row in rows:
        if row.split != AUTHORIZED_FIT_SPLIT:
            offenders[row.split] = offenders.get(row.split, 0) + 1
    require(
        not offenders,
        "a development-only fit may read no withheld role; found "
        + ", ".join(f"{name} x{count}" for name, count in sorted(offenders.items())),
    )


def code_identity(paths: Mapping[str, Path | str]) -> dict[str, str]:
    """Return `{label: canonical text digest}` for the files defining a training protocol.

    Inputs: a mapping from a bare label to a path. Outputs: the same labels mapped to
    the Protocol-P text-domain digest of each file, which is invariant to the checkout's
    line-ending convention (a raw digest of a tracked text file is a digest of the copy,
    not of the document — Session 59/61).
    Purpose: bound 4's "training-protocol/code identity", so a checkpoint names the code
    that produced it and not merely the data it read.
    """

    identity: dict[str, str] = {}
    for label, path in paths.items():
        require_bare_name(label, "code identity label")
        resolved = Path(path)
        require(resolved.is_file(), f"code identity {label!r} does not name a file")
        identity[label] = canonical_text_sha256(resolved)
    return dict(sorted(identity.items()))


@dataclass(frozen=True)
class DevFitProvenance:
    """Bound 4's record: everything a development-only checkpoint must be able to say.

    Every field is a value a reader can check against something outside the checkpoint.
    `data_root_name` is deliberately a bare directory name rather than a path, so the
    record locates the dataset without recording this machine.
    """

    data_root_name: str
    manifest_sha256: str
    config_hash: str
    assignment_sha256: str
    suite: str
    training_seed: int
    checkpoint_sha256: str
    code_identity: Mapping[str, str] = field(default_factory=dict)
    row_disclosure: str = ""
    authority: str = DEVELOPMENT_ONLY_AUTHORITY

    def validate(self) -> "DevFitProvenance":
        """Refuse any record that would not survive an audit; return self when valid."""

        require(
            self.authority == DEVELOPMENT_ONLY_AUTHORITY,
            "authority must be the exact development-only string",
        )
        require_bare_name(self.data_root_name, "data_root_name")
        require(
            bool(_HEX64.match(self.manifest_sha256)),
            "manifest_sha256 must be 64 lowercase hex characters",
        )
        require(
            bool(_DEV_HEX64.match(self.config_hash)),
            "config_hash must be a dev- hash: config.json is deliberately not frozen, "
            "and a frozen hash on a development checkpoint would misstate its status",
        )
        require(
            self.assignment_sha256 == ASSIGNMENT_CANONICAL_SHA256,
            "assignment_sha256 does not equal the pinned approved assignment digest",
        )
        require_matched_fit_suite(self.suite)
        require_predeclared_seed(self.training_seed)
        require(
            bool(_HEX64.match(self.checkpoint_sha256)),
            "checkpoint_sha256 must be 64 lowercase hex characters",
        )
        require(
            bool(self.code_identity),
            "code_identity must name at least the module that defines the network",
        )
        for label, digest in self.code_identity.items():
            require_bare_name(label, "code identity label")
            require(
                bool(_HEX64.match(digest)),
                f"code identity digest for {label!r} must be 64 lowercase hex characters",
            )
        require(
            bool(self.row_disclosure.strip()),
            "row_disclosure must carry the selection's denominator sentence",
        )
        return self

    def as_document(self) -> dict[str, object]:
        """Return the canonical-JSON-serializable record, authority first in sort order."""

        self.validate()
        return {
            "authority": self.authority,
            "assignment_sha256": self.assignment_sha256,
            "checkpoint_sha256": self.checkpoint_sha256,
            "code_identity": dict(sorted(self.code_identity.items())),
            "config_hash": self.config_hash,
            "data_root_name": self.data_root_name,
            "manifest_sha256": self.manifest_sha256,
            "row_disclosure": self.row_disclosure,
            "suite": self.suite,
            "training_seed": self.training_seed,
        }

    def canonical_string(self) -> str:
        """Return the canonical JSON string of `as_document()` (one serialization rule)."""

        return canonical_json(self.as_document())

    def provenance_string(self) -> str:
        """Return the single traceable line handed to `attach_trained_weights`.

        `TemporalAttributionEstimator.attach_trained_weights` requires a non-empty
        description a reader can trace. This is that description: it leads with the
        authority, so an estimator carrying these weights answers the question "may this
        be reported?" before it answers any other.
        """

        self.validate()
        return (
            f"{self.authority} "
            f"suite={self.suite} seed={self.training_seed} "
            f"data_root={self.data_root_name} manifest={self.manifest_sha256[:12]} "
            f"config={self.config_hash[:16]} checkpoint={self.checkpoint_sha256[:12]}"
        )
