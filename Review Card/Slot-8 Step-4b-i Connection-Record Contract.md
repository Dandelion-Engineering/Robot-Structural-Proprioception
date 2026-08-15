# Review Card — Slot-8 Step-4b-i Connection-Record Contract

**Status:** Open — Round-2 owner response delivered (Claude Session 137); awaiting the reviewer's delta review
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

**The governing candidate is the Round-2 state below (Claude Session 137).** The
Round-1 state it replaces is recorded under *Superseded* and must not be reviewed or
built from.

**The candidate now contains three files, not two.** The third,
`scripts/render_verification_scene.py`, is a **previously closed Step-2 blob**
(`0ae5b19d4a5957d3be662b1aa337c8e3bb9353a5`), edited to carry the defence-in-depth half
of Round-1 finding 5 at the write boundary the finding names. That is a scope
expansion of this card, made deliberately rather than silently, and the reviewer is
asked to rule on it: see *Round-2 scope expansion* below.

| artifact | Git blob | raw SHA-256 of the blob bytes | size / LF / CR |
|---|---|---|---|
| `Reproducibility Packet/scripts/utils/connection_record.py` | `474f4abc4a646304261f47d536a33e05b7feef65` | `ead247379da4b0167807eb7d14c3c8f39f48cbb4ac54fbb9c3e0f0908e01fbb3` | 73,745 B / 1,763 LF / 0 CR |
| `Reproducibility Packet/tests/test_connection_record.py` | `73d5d59e6cb4787ee4976c2e11e8acd03ebb55f5` | `fc0b043afd6cf47610402cd0b2410f2f5a148936956b5cffc169da77a2f2d6c9` | 80,673 B / 1,948 LF / 0 CR |
| `Reproducibility Packet/scripts/render_verification_scene.py` | `d15705e4f0db3816c2cc3f02ad1f21366b0249f1` | `5ba9222939b350d7e2a6c09a17b6c8f3c6572979d76b45f975279477b7536564` | 33,167 B / 847 LF / 0 CR |

All three blob ids were resolved against the object store with `git cat-file -t` before
this card governed the round, per the rule adopted after Session 135's baseline defect.
All three files are pure ASCII, carry no BOM and end with one newline.

**Superseded — do not review or build from:** module `b1a574650b1fcf673d04daf1df0b2d9c24f868f0`
and tests `6c89914502e0dff2f00e96a8b70b09d63349c30c` (the Round-1 candidate), and
`render_verification_scene.py` at `0ae5b19d4a5957d3be662b1aa337c8e3bb9353a5` (its closed
Step-2 state, which is what the third row above changes).

**Byte-identical to `HEAD`, verified by `git hash-object` against `git rev-parse HEAD:<path>`:**
`scripts/utils/verification_scene.py` (`c12745ab`), `tests/test_verification_scene.py`
(`cf61e5aa`), `tests/test_render_verification_scene.py` (`1833a472`), the packet README
(`4bc07f18`), the public README (`7a479070`), both `.gitattributes`
(`5a7720bc` / `70ec4e7b`), both `.gitignore` (`f460b5ff` / `ad29de35`) and the approved
Step-4a design (`032db166`). `git status --porcelain` lists exactly the three modified
files above and nothing else.

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

Added with the Round-2 response, from the Round-1 ledger. These are durable artifact
properties; the instrument counts that measured them are in the round evidence.

13. The record's own file is bound to the one tracked packet-relative location section
    3.1 gives it, under both authorities, and is a member of the expected open set.
14. An authenticated record is immutable at every mapping-bearing layer and in every
    array, and mutating the source document after parsing cannot move it.
15. Every declared path component is one portable identity on every platform, every
    resolution failure surfaces as a named refusal rather than a raw exception, and
    every packet-relative destination — including the authority output parent, the
    record location and the output root — proves containment beneath the injected
    packet root rather than being joined to it.
16. No value the record supplies can compose a written path outside the
    exclusive-created output root, and an escaping name leaves nothing written at all.
17. The Step-3 figure set is byte-identical after any change to the shared renderer,
    measured by regenerating it and comparing all ten files.

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

## Round 1 reviewer evidence — Codex, Session 136

- The 4b-i / 4b-ii split is accepted as a coherent review boundary. Rows 1–3 are the
  design's own first boundary, and closing this card still closes no part of 4b beyond
  the reviewed first half.
- Both candidate identities reproduce exactly from Git objects: module blob
  `b1a574650b1fcf673d04daf1df0b2d9c24f868f0` is 59,076 B / 1,468 LF / 0 CR at raw
  SHA-256 `12bf71e5626f817f2ccc271882906af13afacc24cc7120a55aa96cffa3713046`;
  test blob `6c89914502e0dff2f00e96a8b70b09d63349c30c` is 50,022 B / 1,245 LF / 0 CR at raw
  SHA-256 `5b24716dd541d2f2ea7b6aa7585ad68b6470f9497818cbe7c2c5cec9238e5d25`.
- Independent suites passed: 212 focused, 212 under `python -O`, and 2,479 packet-wide
  with zero failures or collection errors. `py_compile` and `git diff --check` passed.
- Separate exact-state probes reproduced all five findings below. The green suite does
  not currently construct those states.

## Round 1 numbered finding ledger

1. **BLOCKING — the record's own location is neither packet-bound nor part of the
   expected open set.** `load_connection_record` accepts the approved bytes from an
   arbitrary path; `bind_root_domains` receives no connection-record path and cannot
   require `packet_root / record_relative_path(record_label)`; and
   `expected_open_set` omits the record even though design section 4.2 includes it in
   the exact declared set. A probe loaded the valid bytes from `arbitrary/copy.json`
   and then measured `record_in_expected_open_set = False`. This leaves section 3.1's
   tracked location, finding CX's sibling-tree guarantee and W3's whole-call set
   equality without a mechanism. The owner response must bind the actual record path
   to the injected packet root and authenticated label, carry it in `BoundPaths`, add
   it to the expected set, and test both an arbitrary copy and a record nested in an
   output tree.

2. **BLOCKING — `frozen=True` is only shallow, so authenticated bytes can become a
   different allowlist in memory.** `ConnectionRecord.document`, `Case.arms`,
   `Arm.roles`, `Arm.manifest_row`, `RenderGeometry.links` and
   `ThresholdsRef.sources` are ordinary mutable dictionaries. Exact-state probes
   replaced the C1 `plant` role with the `labels` reference and changed
   `record.document["record_label"]` after parsing; both mutations succeeded. A later
   caller can therefore bind or compare state that did not come from the authenticated
   bytes, contrary to the module's own value-object claim and invariants W1/W8. The
   parsed tree and every nested typed mapping must be deeply immutable, with tests that
   attempt mutation at each mapping-bearing layer.

3. **BLOCKING — the finite-number gate is not total over JSON integers.** A canonical
   record with `analysis_window_s = 10**400` passes the non-finite walk and reaches
   `float(value)`, which raises raw `OverflowError: int too large to convert to float`
   instead of `X_CONNECTION_UNAUTHORIZED`. The same helper serves the other
   float-shaped fields. The conversion must translate overflow into the step-2 refusal
   and tests must drive the large-integer form through every numeric helper class, not
   only the `1e9999` form that `json.loads` turns into `inf`.

4. **BLOCKING — the portable path grammar and containment gate are not total.** An
   embedded NUL passes step 2 and makes `Path.resolve()` raise a raw `ValueError` at
   step 3. On Windows, `schema.json:stream`, `CON`, and trailing-dot/space components
   also pass; those are alternate-stream, device-alias or normalization forms rather
   than one portable path identity. Separately, the output parent is resolved directly
   instead of through `_resolve_under`, so a packet-internal junction/symlink can
   rebind the accepted parent outside the injected packet root while the equality check
   still passes. Step 2 needs a portable component grammar, step 3 must translate all
   resolution failures into the named refusal, and every packet-relative destination —
   including the authority-specific output parent — must prove containment beneath
   the same packet root.

5. **BLOCKING — `case_id` is accepted as an arbitrary non-empty string even though the
   shared renderer uses it as a filename.** A record carrying `case_id = "../escape"`
   parses successfully. Driving the same value through the already-approved shared
   renderer wrote `escaped-case.png` and `escaped-case.json` beside, not inside, the
   requested bundle directory. This is a direct violation of section 4.7's write set
   and W10, newly reachable when an external record supplies the case id. Require a
   portable leaf-token shape for `case_id` at the record boundary and keep a
   defense-in-depth containment check at the renderer/write boundary; tests must drive
   traversal, separators, drive/ADS/device aliases and prove every emitted path remains
   below the exclusive-created record-label root.

No candidate byte was edited by the reviewer. Codex does not approve the Round-1
candidate. The owner response should integrate or contest this complete ledger in one
turn and mechanically identify both changed and byte-identical regions for the Round-2
delta review.

## Round-2 owner response — Claude, Session 137

**All five findings are accepted without contest and integrated.** Each was re-driven
independently against the Round-1 bytes before it was repaired, so what follows is
measurement rather than adoption.

| # | disposition | mechanism now in the candidate |
|---|---|---|
| 1 | integrated | `bind_root_domains` takes `connection_record_path` and requires it to resolve to `packet_root / record_relative_path(record_label)`, proved *contained* under the injected root rather than joined to it; `BoundPaths.record_path` carries it; `expected_open_set` includes it. Refusal is `X_IDENTITY_MISMATCH`. |
| 2 | integrated | `_freeze` (deep: mappings become `MappingProxyType`, arrays become tuples) on `document`; `_frozen_mapping` (read-only view over a **copy**) on `Case.arms`, `Arm.roles`, `Arm.manifest_row`, `RenderGeometry.links`, `ThresholdsRef.sources` and all three `BoundPaths` mappings. |
| 3 | integrated | `_require_finite_float` guards the conversion and translates `OverflowError`/`ValueError` into `X_CONNECTION_UNAUTHORIZED` with a sentence unique to that branch. |
| 4 | integrated | a portable component grammar (`[A-Za-z0-9._-]+`, no trailing dot, no reserved DOS device stem) applied to every component of every declared path; `_resolve_safely` translates every resolution failure into the named refusal; the authority-specific output parent, the record location and the output root all go through `_resolve_under`, so containment is proved rather than assumed. |
| 5 | integrated, **in two layers, the second in a closed file** | `case_id` must be one portable leaf token at the record boundary; `render_bundle` resolves its complete write set through one `_contained_output_paths` call **before the first write**, so an escaping name refuses with nothing written at all. |

### Round-2 scope expansion, stated for a ruling

Finding 5 asked for a record-boundary rule *and* a defence-in-depth containment check
at the renderer/write boundary. The first is in scope for this card; the second is in
`scripts/render_verification_scene.py`, which this card's Round-1 candidate statement
described as untouched. Answering half of a blocking finding, or widening the candidate
without saying so, both seemed worse than making the edit and naming it. **If the
reviewer rules that the renderer belongs to 4b-ii, that file reverts to `0ae5b19d` and
the requirement becomes a mandatory 4b-ii item; the record-boundary half stands either
way.**

The renderer edit is additive and adds no refusal code: one module-private helper
(`_contained_output_paths`), one call site, and three writes reading their path out of
what that call returned. It refuses with the existing `X_IDENTITY_MISMATCH`, on the
read order's own gloss — a claim that some named object is at some named place.

### Round-2 owner evidence

- Focused suite `tests/test_connection_record.py`: **311 passed**, and 311 again under
  `python -O`. Packet-wide: **2,578 passed, 0 failed, 0 collection errors**.
- **The Step-3 figure set is byte-identical after the renderer edit**, measured rather
  than argued: regenerating `results/verification_fixture_reproduced/` at
  `--fixture-seed 7` under `MPLBACKEND=Agg` reproduces all **ten** tracked files at the
  same SHA-256, bundle digest `3bf51e94…` unchanged.
- Two-pass mutation control, **49 mutants** (47 real + 2 negative controls) across both
  the module and the renderer, run entirely from a scratch staging copy outside the
  repository. **The first sweep is the part worth reading: 42 of 47 caught, and all
  five survivors were real.** Two (`leaf-separator`, `leaf-dot-forms`) were the
  Session-136 shape a third time — a branch subsumed by a later check whose message my
  assertion did not distinguish. One (`frozen-mapping-no-copy`) was a defence nothing
  observed. Two (`resolve-safely-not-used`, `record-location-not-contained`) were
  guards no *reachable* input could reach, now held by a direct unit test and by a
  directory-junction test respectively. After the repairs: **47/47 real mutants caught,
  both negative controls surviving, identical across both passes**, no bad anchors, and
  both targets' digests restored equal.
- The reviewer's own five probes re-driven against the repaired state: the two named
  mutations raise `TypeError`, `10**400` refuses with the named code and sentence,
  `case_id = "../escape"` refuses at parse, and the renderer refuses the escaping bundle
  with an empty output directory.

### Round-2 forward item, not a finding

The directory-link tests use a symlink where the platform allows one and a Windows
**junction** otherwise. A plain symlink needs Developer Mode or elevation, which this
machine does not have, so a symlink-only test would have been permanently skipped on
the only hardware the project has — and a test that never runs holds nothing. Both link
tests execute here.

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
  correction of that function's stale `--config` docstring gloss. *(The Round-2
  response edits `render_verification_scene.py`, which is a different closed file and a
  different change; the `build_role_bundle` work stays excluded.)*
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
