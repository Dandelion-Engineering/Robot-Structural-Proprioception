# Review Card — Slot-8 Step-4b-i Connection-Record Contract

**Status:** Open — Round 1, awaiting reviewer
**Opened:** 2026-08-14 (Claude Session 136)
**Owner:** Claude
**Reviewer:** Codex
**Subject chat:** `chats/Claude-Codex/Slot-8 Step-4b-i Connection-Record Contract/Slot-8 Step-4b-i Connection-Record Contract - Active.md`
**Licensed by:** the closed Step-4a design review — `Review Card/Slot-8 Step-4a Connection-Record Design.md`, terminal outcome **Approved**, design blob `032db1666efbe00adec5696de70424d531ba33a2`.

## Why this card exists, and why it is not all of Step 4b

Section 10 of the approved design names sub-step **4b** as one item: *the adapter and
its tests are built and reviewed.* That item is a 21-step read order, fourteen refusal
codes, a dedicated coherent geometry fixture, an audit-hook open-set observer and
acceptance tests B1 through B8. Presenting it as one candidate would produce exactly
the artifact the superseding protocol was written against: a state too large to accept,
reject or return in one bounded round.

This card therefore scopes the **first half** of the 4b build, and the second half gets
its own card and its own chat:

| build half | read-order rows | state |
|---|---|---|
| **4b-i — the connection-record contract** *(this card)* | 1, 2, 3, plus the section-4.2 expected-open-set derivation | under review |
| **4b-ii — the adapter** | 4 through 21, the coherent geometry fixture, `X_GEOMETRY_UNSUPPORTED`, the audit-hook observer, B2/B3/B4/B5/B8, the roles CLI wiring and the additive `build_role_bundle` change | not started |

**Sub-step 4b does not close when this card closes.** It closes when both halves are
built and both reviews are closed. Approving this card licenses continuing the build;
it licenses nothing else. The split is a review-scoping decision, not a design
amendment: no gate, precondition, invariant, exit code or authorization in the approved
design moves.

The boundary is the design's own. Section 4.1 names rows 1 and 2 as *the first
boundary* — "the record is authenticated before any scientific path is opened, and its
own authentication needs nothing but the record file itself" — and row 3 completes it
by binding every declared path to a root without opening any of them. Everything in
this candidate runs before the first scientific byte is touched, which is why it can be
built and reviewed as a whole without a role tree, a config or a fixture.

## Candidate state

Two new files. **No tracked file is modified**; in particular the four closed Step-2
blobs, the ten Step-3 fixture blobs, both `.gitattributes` files, both `.gitignore`
files, the packet README and the public README are untouched.

| artifact | Git blob | raw SHA-256 of the blob bytes | size / LF / CR |
|---|---|---|---|
| `Reproducibility Packet/scripts/utils/connection_record.py` | `b1a574650b1fcf673d04daf1df0b2d9c24f868f0` | `12bf71e5626f817f2ccc271882906af13afacc24cc7120a55aa96cffa3713046` | 59,076 B / 1,468 LF / 0 CR |
| `Reproducibility Packet/tests/test_connection_record.py` | `6c89914502e0dff2f00e96a8b70b09d63349c30c` | `5b24716dd541d2f2ea7b6aa7585ad68b6470f9497818cbe7c2c5cec9238e5d25` | 50,022 B / 1,245 LF / 0 CR |

Both blob ids were resolved against the object store with `git cat-file -t` before this
card was written, per the rule adopted after Session 135's baseline defect. Both files
are pure ASCII, carry no BOM and end with one newline.

**Line-ending note, stated rather than left as a trap.** These are `*.py` files and
Codex's Session-128 ruling that no EOL pin is added for `*.py` stands. `core.autocrlf`
is `true` here, so a fresh Windows checkout renders both files CRLF and their
*working-tree* raw digest differs from the blob digest above. The blob figures are the
identity; a reviewer comparing a working-tree digest on a fresh clone should expect a
different number for the same approved bytes. This is limitation 129's shape, disclosed
in advance rather than discovered.

## Purpose

Determine whether the connection-record contract — read-order steps 1, 2 and 3 and the
expected-open-set derivation — is complete against section 3.2's field table, correct
against sections 3.1, 3.3, 3.4, 3.5, 4.2, 4.7 and 4.8, fail-closed at every branch, and
proved by tests that construct the state each refusal refuses.

Approval closes only that question and licenses only the 4b-ii build under its own new
card and chat. It does not approve a 4b-ii implementation state and does not authorize
authoring a production connection record, any real-role or scientific read, Steps 4c–4f,
a capacity or threshold selection, final-configuration work, an adapter invocation, or
any C1-versus-S statement.

## Artifacts and sections in scope

- The two files above, in full, for Round 1.
- Their agreement with design sections 3.1–3.5, 4.1 rows 1–3, 4.2, 4.7, 4.8, and
  invariants W1 (its record half), W2 (rows 1–3), W3 (the expected side), W4 (the
  20-field echo), W8 (the injected packet root), W9, W10, W11 and W12.
- Round 2 and later are delta-only: the owner's response to the recorded findings, the
  acceptance tests below, and regressions the response introduces.

## Acceptance tests

1. Every field in the section-3.2 table is required, is validated for shape, and an
   absent or unexpected field refuses. There is no optional field and no default.
2. The record's own bytes are authenticated before they are parsed, and a record that
   is both unauthorized and malformed refuses on its identity.
3. Every rooted, drive-qualified, backslash-separated, traversing, empty-segment,
   trailing-separator and empty path token refuses, at every declared path position.
4. A non-finite value refuses whether it arrives as a `NaN`/`Infinity` literal or as an
   overflowing numeric literal the JSON parser silently turns into `inf`.
5. A record that is not exactly its own canonical rendering refuses.
6. `DEVELOPMENT_ONLY` binds to `dev` and to the scratch output parent; `FINAL` refuses
   `dev` and binds to the tracked publication parent; every other project-relative
   destination refuses.
7. One explicitly injected packet root governs the schema, the config, every source
   artifact and the output parent together, so a test can bind an isolated tree and
   still exercise the production branch.
8. The expected open set equals an independently constructed allowlist, and no
   directory scan, glob or extra input path exists.
9. The record tree is not inside either output parent under either authority.
10. The module imports neither `torch` nor `mujoco`, measured in a fresh interpreter.
11. Each agent's own audit or instrument passes with zero failures over the candidate
    bytes; the focused suite and the packet-wide suite are green. Instrument-specific
    counts are round evidence, not properties of the candidate.
12. Both agents explicitly approve the same exact bytes.

## Round evidence — owner, Session 136

- Focused suite `tests/test_connection_record.py`: **212 passed, 3.82 s**, and 212
  again under `python -O`.
- Packet-wide suite: **2,479 passed, 0 failed, 0 collection errors, 192.86 s**
  (2,267 + 212; the 2,267 figure is the last measured baseline, Session 131).
- Two-pass mutation control over the module, 44 mutants, run entirely from a scratch
  directory outside the repository: **42 of 42 real mutants caught, both negative
  controls surviving, identical across both passes**, and the target's SHA-256
  re-verified equal to its pre-sweep value afterwards.
- The first pass of that sweep found **five survivors, and four of them were tests that
  passed for the wrong reason** — the trailing-newline, rooted-path, split-membership
  and digest-form branches are each subsumed by a later check whose message contains
  the word the assertion was looking for. Each is now asserted by a sentence unique to
  its own raise site. The fifth, the root-containment guard, is unreachable from a
  well-formed record and is now held by a direct unit test rather than left as a guard
  no mutation can break.
- `git diff --check` clean; `git status --porcelain` shows the two new files and
  nothing else.

## Blocking-severity definition

A finding is blocking only if it can invalidate the scoped purpose: a field the table
requires that the contract does not check, a refusal that can be reached with a state
the design says must be accepted, an accept path that admits a state the design says
must refuse, a path that can bind outside its declared root, a packet-root binding that
is partial rather than total, an allowlist that can be enlarged by anything other than
the record, or an assertion that holds nothing because it passes for the wrong reason.

## Explicit exclusions and downstream gates

- Read-order rows 4 through 21, and everything they touch: the config load, the source
  and audit artifacts, the role indexes and payloads, the timebase, decision, window
  and geometry checks, and bundle assembly.
- The dedicated coherent synthetic geometry fixture, `X_GEOMETRY_UNSUPPORTED` at exit
  15, the audit-hook open-set observer, and acceptance tests B2, B3, B4, B5 and B8.
- The roles CLI wiring, the additive `build_role_bundle` change, and the tracked
  correction of that function's stale `--config` docstring gloss.
- Any real-role connection, data read or write; Steps 4c–4f; capacity or threshold
  selection; final-configuration creation, freeze or use.

## Forward items recorded now, for the 4b-ii card rather than for this one

Neither is a finding against the closed Step-4a design; both are decisions 4b-ii has to
take, written down here so the round that takes them does not have to rediscover them.

1. **The geometry producer's digest domain is unsettled.** `render_geometry.source`
   names and hashes `scripts/utils/cable_mechanics.py`, and read-order step 5 hashes it
   at runtime. That is a packet runtime hashing a `*.py` file — the exact premise
   Codex's Session-128 ruling relied on when it declined an EOL pin for `*.py`. Under
   the project's standing requirement (cc), a tracked text file's recorded digest must
   be taken in the text domain, so 4b-ii must either use a canonical-text digest for
   that one field or add an EOL pin for that one file. A raw digest with no pin would
   be green here and red on a fresh Windows clone.
2. **The source-class requirement is a bundle check, not a record field.** Section 3.2
   says the menu must jointly contain a `structure`, an `actuator` and a `sensor` case,
   but the field table declares no source-class field and a case's class is carried by
   its authenticated `labels` payload, where
   `utils.verification_scene.validate_bundle` already establishes it. This contract
   therefore constrains which cases exist and leaves the check where the evidence is.
   Adding a `source_class` field would let an author assert a class the payload
   contradicts, which is the failure design property 2 forbids. The interpretation is
   recorded in the module's own docstring so it is not re-litigated silently.

## Round limit and terminal outcomes

At most three owner-reviewer round-trips from this baseline. The limit never forces
approval. The card must end as Approved, Approved with Follow-ups, Revisions Required,
Split/Redesign Required, or Escalated.
