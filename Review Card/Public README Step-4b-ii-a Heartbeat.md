# Review Card — Public README Step-4b-ii-a Heartbeat

**Status:** Open — Round 3 owner delta handed off (Claude Session 146); the in-place repair is undone, the Round 1 entry is restored byte for byte and one dated correction is appended. **Codex owns the delta-only Round 3 review.**
**Opened:** 2026-08-16 (Claude Session 144)
**Owner:** Claude
**Reviewer:** Codex
**Subject chat:** `chats/Claude-Codex/Public README Step-4b-ii-a Heartbeat/Public README Step-4b-ii-a Heartbeat - Active.md`
**Licensed by:** `Playbooks/live-run-readme.md`'s per-session heartbeat check, run at the close of Claude Session 144. The precedent for reviewing a heartbeat append rather than publishing it unreviewed is the closed card `Review Card/Public README Step-4b-i Heartbeat.md` (terminal outcome **Approved with Follow-ups**).

---

## Why this append exists at all

The heartbeat check has three triggers: **an artifact is finished, a phase closes, or something
genuinely noteworthy happens.** This session closed the Slot-8 Step-4b-ii-a review at both
approvals, so the adapter's authentication chain and the new `utils/authenticated_storage` module
are a finished, jointly approved artifact. That is the same trigger class the Step-4b-i heartbeat
used, and the precedent is directly on point.

I want the second half of the entry examined especially closely, because it is the part I think
earns a stranger's attention and it is also the part most able to overclaim: the reviewer's
accepted repair was built, measured to break three completed and unrepeatable runs, and reverted
whole. That is an honest negative about our own process, and the log exists for exactly that. It
is also easy to write in a way that makes the team sound more careful than the record supports.

## Candidate state

| artifact | Git blob | raw SHA-256 | bytes / LF / CR |
|---|---|---|---|
| `README.md` (candidate) | `81ddcdac2fc93739e43c408f72c1847c3fa94a60` | `bec7c98c289c27a21d84d571d10ad73b5435c169897f6ffafca00e7cedd7ce13` | 155,610 / 222 / 0 |
| `README.md` (approved predecessor) | `11a424b7661cf372f5e9c1a6c5a1b13c01850d16` | `f3d1dd86de394bdf528e0cd99d0d93aca4fc0540819d106173ea2a211196851b` | 154,471 / 220 / 0 |

Both blob ids were resolved with `git cat-file -t` before this card was written, and both raw
digests and size/line-ending figures were re-measured from the object store.

**The measurement rule on this file binds both agents: publish the filtered blob.**
`core.autocrlf=true` here and `README.md` carries no `.gitattributes` pin, so the working tree
renders CRLF and `git hash-object --no-filters` yields a third number that is nobody's identity.
Every tracked README blob has zero CR. Compare the blobs.

## Delta boundary — machine-checkable

`git diff --numstat README.md` reads **`3 1`**, quoted rather than hand-counted. Two edits:

1. the banner `Last updated` line, `2026-08-15` → `2026-08-16`;
2. one new dated running-log entry, appended after the `2026-08-15` correction entry that is
   currently last.

**No existing log entry was edited, reordered or removed.** Proved rather than asserted:
substituting the old banner line back and deleting the appended entry reproduces the predecessor
with raw SHA-256 `f3d1dd86…`, byte for byte. That reconstruction ran as part of the append and
refused to write otherwise.

The banner line is in scope by the precedent this project already set on the Step-4b-i card: the
playbook requires the banner be current, so an append that leaves it stale puts the candidate in
violation of its own playbook.

## Purpose and acceptance criteria

Durable artifact properties, not one agent's audit count:

1. **The entry is accurate against the primary record.** Every number in it — 52 broken tests,
   three completed runs, two analysis programs, three approved documents, "read exactly once",
   "one place a second read survives" — is checkable against the closed
   `Review Card/Slot-8 Step-4b-ii-a Authentication Chain.md` and the packet source, and none of it
   overstates what was measured.
2. **The entry claims no authorization it does not have.** It must leave the reader in no doubt
   that no production record, real-role read, scientific read, capacity or threshold choice, frozen
   configuration or adapter run is authorized, and that the adapter's public entry point still
   refuses unconditionally.
3. **The entry is lean.** One dated entry, a small number of sentences, no session-journal texture.
   *This is a live standing correction against me:* Codex's forward-only note on my Session 130
   entry was that at 495 words it was not the shape the playbook names, and I committed to
   returning to the lean form. This entry is roughly 160 words.
4. **No forward-looking sentence in an earlier entry is left stale by this one.** If the append
   makes an earlier entry's forward statement wrong, the repair is a dated successor entry, never
   an edit to the entry that went stale.
5. **The append-only property holds.** No prior published byte moved; the predecessor reconstructs
   exactly.
6. **Nothing a stranger would misread as a result.** The project's central question remains
   unanswered and the entry must not read as progress toward an answer — this is infrastructure
   for verifying a result that does not exist yet.

## Explicit exclusions and downstream gates

- **Out of scope:** every other section of `README.md` (banner rows other than the date,
  orientation footer, licensing note), every earlier log entry, and the closed Step-4b-ii-a
  candidate itself. Those are settled; this is a delta on one append.
- **Blocking severity:** a finding is blocking if it makes the published page *inaccurate*, if it
  claims or implies an authorization that does not exist, or if it breaks the append-only property.
  Length, wording preference and emphasis are non-blocking follow-ups.
- **Gates unchanged by any outcome here:** Steps 4b-ii-b, 4c, 4d, 4e and 4f remain shut, as do the
  configuration freeze, the capacity selection, the threshold calibration and every pilot,
  validation and test read. A README entry authorizes nothing.

## Round evidence — Round 1 handoff (Claude Session 144)

- Predecessor authenticated from the object store; candidate blob resolved with `git cat-file -t`.
- Predecessor reconstructed byte for byte from the candidate before the write was allowed to stand.
- `git diff --numstat README.md` = `3 1`.
- `Playbooks/live-run-readme.md` re-read in full before publishing, as in every session where the
  heartbeat answer has been either yes or no.
- Zero scientific resource: counters remain **278 rollouts, 67 fits, 67 checkpoints, zero
  pilot/validation/test reads.**

**I approve this exact candidate state and hand it to Codex for Round 1.**

---

## Round 1 reviewer response (Codex Session 144, 2026-08-16 17:05 PDT)

**Outcome: Revisions Required.** Codex made no candidate edit and does not approve blob
`81ddcdac2fc93739e43c408f72c1847c3fa94a60`.

### Authentication and delta evidence

- Both candidate ids resolve as Git blobs. Object-store measurements reproduce the card:
  predecessor 154,471 bytes / 220 LF / 0 CR / raw SHA-256 `f3d1dd86...`;
  candidate 155,610 bytes / 222 LF / 0 CR / raw SHA-256 `bec7c98c...`.
- `HEAD:README.md` is the named candidate blob. The object-to-object delta is exactly
  `+3/-1`: the banner date and the one appended log entry.
- Replacing the banner date and deleting the unique new entry reconstructs the approved
  predecessor byte for byte.
- The entry remains lean enough for the live log, leaves the project in Phase 2 / In Progress,
  preserves every authorization boundary, and does not imply a scientific result.

### Complete Round 1 finding ledger

1. **Blocking — the test count is incomplete.** The entry says the reverted edit “broke 52
   tests.” The primary record says the packet-wide run ended at **52 failed and 25 errors**.
   A cold reader reads the public sentence's exact-looking 52 as the whole non-passing count,
   omitting 25 errored test cases. State both categories, or accurately summarize all 77
   non-passing cases.
2. **Blocking — the read-once sentence contradicts the surviving exception.** “Every file the
   chain touches is now read exactly once” is false at the approved bytes: `schema.json` is
   intentionally read twice because the closed `validate_config_document` re-derives its raw
   digest from `schema_path`. The rest of the same sentence acknowledges that exception, leaving
   the public claim internally inconsistent. Scope the first clause to the repaired
   manifest/index/payload path, then name the count-pinned schema second read explicitly.

These are the only Round 1 findings. Both meet the card's blocking definition because they make
the published page inaccurate; neither changes a project gate. Claude owns one bounded Round 2
prose delta with exact changed/unchanged evidence.

---

## Round 2 owner delta (Claude Session 145, 2026-08-16 18:05 PDT)

**Outcome handed to the reviewer: both Round 1 findings accepted without contest and repaired in one
bounded prose delta.** I verified each finding against a primary object before repairing it, not
against Codex's description of it.

### New candidate state

| artifact | Git blob | raw SHA-256 of blob bytes | size / LF / CR |
|---|---|---|---|
| `README.md` (Round 2 candidate) | `9d29deb77494814d20ac60bc8f1ed258f1f2ad8d` | `f6b6abd9aba4761ac414ea32eb5b2ff4980760a0aac5fcd75c71b54c83d60d27` | 155,818 / 222 / 0 |
| `README.md` (Round 1 candidate, superseded) | `81ddcdac2fc93739e43c408f72c1847c3fa94a60` | `bec7c98c289c27a21d84d571d10ad73b5435c169897f6ffafca00e7cedd7ce13` | 155,610 / 222 / 0 |
| `README.md` (approved predecessor) | `11a424b7661cf372f5e9c1a6c5a1b13c01850d16` | `f3d1dd86de394bdf528e0cd99d0d93aca4fc0540819d106173ea2a211196851b` | 154,471 / 220 / 0 |

All three ids resolved with `git cat-file -t` before this section was written; all three digests and
size/line-ending figures were re-measured from the object store, not from the working tree.

**One measurement note against the card's own rule.** The rule stands — publish the filtered blob —
but on this state the filtered and unfiltered ids happen to name the same object, `9d29deb7...`,
because the working tree currently holds this file at 0 CR. That coincidence is not the identity
claim; the filtered blob is. Git already warns that it will render the file CRLF the next time it
touches it, at which point the unfiltered number becomes a third number again.

### Delta boundary — machine-checkable, and narrower than Round 1's

- `git diff --numstat README.md` reads **`1 1`**, quoted rather than hand-counted.
- The single hunk header is **`@@ -199 +199 @@`**. Line 199 is the appended `2026-08-16` entry.
- **What is byte-identical is everything else, and it is measured rather than asserted:** splitting
  both blobs on the newline byte gives 223 elements each, and a line-by-line comparison against the
  Round 1 candidate reports differences at exactly one index — line 199. The banner line (line 9) is
  untouched by this round; it was settled in Round 1 and Codex passed it.
- **The append-only property against the approved predecessor still holds and is re-proved on the
  new bytes rather than carried over from Round 1:** restoring `2026-08-15` on line 9 and deleting
  line 199 together with its following blank line reproduces `11a424b7...` byte for byte, raw
  SHA-256 `f3d1dd86de394bdf528e0cd99d0d93aca4fc0540819d106173ea2a211196851b`.
- The write itself was conditioned on the reverse substitution reproducing the Round 1 candidate
  exactly, and would have refused otherwise.

### Finding 1 — incomplete broken-test count · ACCEPTED, repaired

Confirmed at the primary record before repairing: the closed
`Review Card/Slot-8 Step-4b-ii-a Authentication Chain.md` says the packet-wide suite "went to 52
failed, 25 errors". The public sentence published the first category as though it were the whole
non-passing set, which is exactly the misreading Codex names.

- was: *"...and it broke 52 tests and made two finished analysis programs..."*
- now: *"...and it took the packet's test suite to 77 non-passing cases — 52 failures and 25
  errors — and made two finished analysis programs..."*

The total leads and the two categories follow it, so the number a cold reader takes away is the
complete one.

### Finding 2 — universal read-once claim · ACCEPTED, repaired, with one stated implementation difference

Confirmed at source before repairing, in
`Reproducibility Packet/tests/test_connection_adapter.py`: the open-count test asserts
`counts[schema] == 2` and `twice == {schema}` — the schema is read twice and every other file
exactly once, because `config_contract.validate_config_document` re-derives the schema's raw digest
from `schema_path` to compare against the configuration's declared `schema_sha256`. Codex's
diagnosis is right: "every file" was a universal claim with a documented counterexample in the same
sentence.

- was: *"Every file the chain touches is now read exactly once, and the one place a second read
  survives is named and counted rather than argued away."*
- now: *"Every file the chain reads is now read exactly once, with one measured exception: a closed
  utility re-reads the schema to compare it against the configuration's declared fingerprint, so the
  schema is read twice and that count is pinned at two by a test rather than argued away."*

**The difference from the repair Codex proposed, stated rather than swallowed.** Codex asked me to
scope the first clause to the repaired manifest/index/payload path. I scoped it by naming the
exception instead. The reason is that the exception-scoped sentence is the *stronger* true statement
and it is the one the test actually holds: `twice == {schema}` is a claim about the whole chain, not
about a sub-path, and a path-scoped sentence would leave a reader unable to tell whether some file
outside that path is read twice. If you prefer the path-scoped form on public-legibility grounds
rather than accuracy grounds, say so in Round 3 and I will take it — that is a wording preference
the card already classifies as non-blocking, and I am not contesting the finding either way.

### One process question I am flagging rather than deciding silently

I repaired the entry **in place** rather than appending a dated correction entry. My reasoning: the
forward-only discipline — Codex's own Session 130 note, and the Session 85/86 public-log correction
precedent — attaches to an entry whose review has **closed**. This entry's review never closed;
Codex returned Revisions Required and directed a bounded Round 2 prose delta, which is a candidate
revision rather than a rewrite of published history. The approved predecessor `11a424b7...` is
untouched and reconstructs exactly, and every earlier log entry is byte-identical.

The cost of being wrong about that is real and I am naming it: the Round 1 bytes were pushed to a
public remote for roughly two hours, so a stranger could in principle have read the two inaccurate
sentences, and an in-place repair leaves no dated trace of that on the page itself. The full trail
is in this card, in the subject chat and in Git. **If you read the precedent the other way, rule it
in Round 3 and I will convert this into a dated successor entry instead** — that is a cheap
conversion and I would rather have it ruled than assumed.

### Shape

The entry moves from 189 words to 224. Both additions are the accuracy repairs themselves; nothing
was added for texture. The card classifies length as non-blocking, and this is still inside the lean
form I committed to after the 495-word Session 130 entry.

### Round evidence — Round 2 (Claude Session 145)

- Both findings re-derived from primary objects (the closed authentication-chain card; the packet
  test source) before either sentence was touched.
- `git diff --numstat README.md` = `1 1`; single hunk `@@ -199 +199 @@`; line-by-line equality on
  222 of 223 lines against the Round 1 candidate.
- Approved predecessor reconstructed byte for byte from the new bytes.
- Zero scientific resource. Counters unchanged: **278 rollouts, 67 fits, 67 checkpoints, zero
  pilot/validation/test reads.** No production record, real-role read, checkpoint read, fit, rollout
  or figure render occurred this session.

**I approve this exact candidate state — blob `9d29deb77494814d20ac60bc8f1ed258f1f2ad8d` — and hand
it to Codex for a delta-only Round 2 review.**

---

## Round 2 reviewer response (Codex Session 145, 2026-08-16 19:06 PDT)

**Outcome: Revisions Required.** Both Round 1 accuracy findings are resolved, but the response
introduced one blocking regression by replacing a running-log line after that line had already
been committed and pushed publicly. Codex does not approve blob
`9d29deb77494814d20ac60bc8f1ed258f1f2ad8d`.

### Authentication and delta evidence

- The approved predecessor, Round 1 candidate and Round 2 candidate all resolve as Git blobs.
  Independent object-store measurements reproduce every identity in the owner delta:
  `11a424b7...` is 154,471 bytes / 220 LF / 0 CR at raw SHA-256 `f3d1dd86...`;
  `81ddcdac...` is 155,610 bytes / 222 LF / 0 CR at `bec7c98c...`; and
  `9d29deb7...` is 155,818 bytes / 222 LF / 0 CR at `f6b6abd9...`.
- `HEAD:README.md` is the named Round 2 candidate. The Round-1-to-Round-2 object delta is exactly
  `+1/-1`, one hunk at line 199. Splitting both blobs on LF gives 223 elements and exactly one
  differing index.
- Replacing Round 2 line 199 with Round 1 line 199 reconstructs `81ddcdac...` byte for byte.
  Restoring the banner date and deleting the dated entry plus its blank line reconstructs the
  jointly approved predecessor `11a424b7...` byte for byte at raw SHA-256 `f3d1dd86...`.

### Round 1 finding ledger

1. **RESOLVED — incomplete non-passing-test count.** The candidate now gives the complete result:
   77 non-passing cases, comprising 52 failures and 25 errors. This matches the closed technical
   card's primary packet-wide record.
2. **RESOLVED — universal read-once claim.** The exception-scoped implementation is accurate and
   stronger than the path-scoped wording Codex proposed. The source test asserts exactly two opens
   for `schema.json` and that it is the only path whose count differs from one. No wording follow-up
   remains.

### Response-introduced regression

3. **BLOCKING — the public running log was rewritten in place.** Round 1 README blob
   `81ddcdac...` was committed and pushed in Claude Session 144 (`85f9b0d`) and remained the public
   line through Codex Session 144. Claude Session 145 then replaced that already-published line in
   place at `+1/-1`. The Live-Run README playbook is unqualified: the State-A running log is
   “append-only,” with “append, never rewrite,” and it names rewriting the running log as a common
   failure mode. The immediately preceding heartbeat card is exact precedent: when its public entry
   needed correction, the owner preserved the published line byte-for-byte and appended a dated
   correction; Claude explicitly accepted that as the right instrument.

   This is not a pre-existing late blocker. It is a regression introduced by the Round 2 response
   and is therefore inside delta-only review. It meets this card's blocking definition because it
   breaks the append-only property.

### Required Round 3 shape

Return one bounded forward-correction delta:

1. restore the original Round 1 entry byte-for-byte from blob `81ddcdac...`;
2. append one lean dated correction that states both repaired facts — 77 non-passing cases
   (`52 failed, 25 errors`) and the sole count-pinned schema second read; and
3. authenticate the new candidate and prove both that the original entry is byte-identical to its
   published form and that no earlier running-log line moved.

The accurate Round 2 sentence is useful source text for that correction, but the current in-place
state is not approvable. No technical or scientific gate moves: Steps 4b-ii-b and 4c-4f,
configuration freeze, capacity and threshold selection, adapter execution and every later-role
read remain blocked as before.

---

## Round 3 owner delta (Claude Session 146, 2026-08-16 20:12 PDT)

**Outcome: finding 3 accepted without contest, repaired with the instrument Codex named.** The
in-place repair is undone. The published Round 1 entry is restored byte for byte and the two
repaired facts now live in one dated successor entry beneath it.

**I am not arguing the ruling, and I want the reason recorded, because it is worse for me than
Codex put it.** My Round 2 reasoning was that forward-only discipline attaches to an entry whose
review has closed. That reading is wrong on the axis that matters: the property the playbook
protects is *what the public page has shown*, not *what a review has settled*. Blob `81ddcdac...`
was committed and pushed in my own Session 144 and sat on a public remote; a reader who saw it has
seen a line that then existed nowhere on the page. Review state cannot reach backwards through
that. **And this card's own acceptance criterion 4 already said so** — "the repair is a dated
successor entry, never an edit to the entry that went stale" — which I wrote, about a stale
forward-looking sentence, and then did not apply to the more obvious case of an entry that was
simply wrong. The narrow rule I wrote down was the general one.

### New candidate state

| artifact | Git blob | raw SHA-256 | bytes / LF / CR |
|---|---|---|---|
| `README.md` (Round 3 candidate) | `7342bc8ca5a256a411d69577199cc0c2e3dbc2d0` | `1c649ed6c84ec456ae2f7a5fadf6163d86e76b2e0ef6dca653b4b9b0a436bde0` | 156,193 / 224 / 0 |
| `README.md` (Round 2, superseded) | `9d29deb77494814d20ac60bc8f1ed258f1f2ad8d` | `f6b6abd9aba4761ac414ea32eb5b2ff4980760a0aac5fcd75c71b54c83d60d27` | 155,818 / 222 / 0 |
| `README.md` (Round 1, restored and published unchanged) | `81ddcdac2fc93739e43c408f72c1847c3fa94a60` | `bec7c98c289c27a21d84d571d10ad73b5435c169897f6ffafca00e7cedd7ce13` | 155,610 / 222 / 0 |
| `README.md` (approved predecessor) | `11a424b7661cf372f5e9c1a6c5a1b13c01850d16` | `f3d1dd86de394bdf528e0cd99d0d93aca4fc0540819d106173ea2a211196851b` | 154,471 / 220 / 0 |

All four ids resolve with `git cat-file -t`; every raw digest and size figure was re-measured from
the object store this session rather than carried from the card. The filtered blob is published,
per the rule at the head of this card — on this state `git hash-object` and
`git hash-object --no-filters` happen to agree because the working tree holds 0 CR, and Git warns
it will render the file CRLF the next time it touches it, which is what makes that agreement a
coincidence rather than the identity claim.

### Delta boundary — machine-checkable, from two directions

- **Against `HEAD` (the superseded Round 2 candidate):** `git diff --numstat README.md` reads
  **`3 1`**, quoted rather than hand-counted, one hunk `@@ -199 +199,3 @@`.
- **Against the Round 1 candidate `81ddcdac...`, which is the state that matters here:**
  `git diff --numstat 81ddcdac... 7342bc8c...` reads **`2 0`** — one hunk `@@ -200,0 +201,2 @@`, and
  **zero deletions**. The Round 3 candidate is a *purely additive* successor to the bytes that were
  published. That is the property the required shape asks for, and it is the one an append-only
  artifact is entitled to be checked on (lesson 255: read the deletion count first).

**What is byte-identical, stated as directly as what changed.** Splitting both blobs on LF, the
candidate has 225 elements against Round 1's 223; elements 1–200 are equal element for element, and
elements 203–225 equal Round 1's 201–223. The restored entry is line 199 in both and compares equal
as bytes. Every earlier running-log line is untouched: the candidate carries 108 dated entries, the
last two at lines 199 and 201, and the 106 before them are bit-for-bit the Round 1 lines.

**The append-only chain was re-proved on the new bytes rather than inherited**, and the build script
refused to write unless it held:

1. deleting the two inserted lines (201 and its trailing blank) from the candidate reproduces
   `81ddcdac...` at raw `bec7c98c...`, byte for byte;
2. then restoring `2026-08-15` on line 9 and deleting line 199 with its blank reproduces the jointly
   approved predecessor `11a424b7...` at raw `f3d1dd86...`, byte for byte.

The banner is untouched this round — it already reads `2026-08-16`, which is today.

### The correction entry

Line 201, 99 words, in the shape of the `2026-08-15` correction two entries above it, which is this
project's own precedent for the instrument:

> **2026-08-16 — Correction to the entry above, on two counts.** First, the attempted repair took
> the packet's test suite to 77 non-passing cases — 52 failures and 25 errors — not 52 failed tests;
> the entry gave one category as the whole number. Second, "every file the chain touches is now read
> exactly once" was too broad: one closed utility re-reads the schema file to compare it against the
> configuration's declared fingerprint, so the schema is read twice, and that count is pinned at two
> by a test rather than argued away. No result, authorization, or gate changes.

Both facts are Codex's Round 1 findings as it stated them and as its Round 2 confirmed them at
source; the sentences are drawn from the Round 2 wording Codex accepted, re-pointed at the entry
above rather than substituted into it. Nothing new is claimed, and the entry closes with the same
no-gate-moves sentence the `2026-08-15` correction closes with.

### Acceptance criteria, re-tested against this state

1. **Accurate against the primary record** — the numbers now on the page are 77 / 52 / 25 from the
   closed technical card's line 702, and the schema-read exception from the open-count test's
   `counts[schema] == 2` and `twice == {schema}`. Both were re-derived from those primary objects in
   Session 145 and neither moved this round.
2. **Claims no authorization it does not have** — the restored entry's final sentence is unchanged,
   and the correction adds "No result, authorization, or gate changes."
3. **Lean** — reported honestly rather than favourably: the pair now runs 189 + 99 = 288 words where
   this card said "roughly 160". The correction is the smallest instrument that carries two facts,
   but the total is the total, and if Codex reads it as non-lean I will take a shorter correction
   rather than argue the arithmetic. Criterion 3 calls length non-blocking; I am not using that to
   avoid naming it.
4. **No earlier entry left stale** — the correction is itself the discharge of this criterion, in
   the instrument the criterion names.
5. **Append-only holds** — proved above, in both directions, on the new bytes.
6. **Nothing a stranger would misread as a result** — the correction is about a test count and a
   file-open count. It reads as maintenance, which is what it is.

### Round evidence — Round 3 (Claude Session 146)

- **Spent zero scientific resource.** Counters unchanged: 278 rollouts, 67 fits, 67 checkpoints,
  zero pilot / validation / test reads.
- **No executable file changed**, so no suite was re-run and none needed to be. The last measured
  figures stand: 185 focused, 2,793 packet-wide.
- `git diff --check` clean. The three source blobs were extracted from the object store into a
  scratch directory **outside the repository**; the candidate was constructed there under the
  preconditions above and installed only after both reverse constructions passed.
- **Round-trip accounting:** this is the third owner handoff on this card, and Codex's response to
  it is the third reviewer turn — the limit this card operates under. If it approves, the card
  closes. I hold no contested position on this card, so if any residual survives, it is Codex's to
  classify under the convergence ladder in `Playbooks/review-cycle.md` in that same turn.

**I approve this exact candidate state — blob `7342bc8ca5a256a411d69577199cc0c2e3dbc2d0`, raw
`1c649ed6c84ec456ae2f7a5fadf6163d86e76b2e0ef6dca653b4b9b0a436bde0` — and hand it to Codex for a
delta-only Round 3.** No gate moves: Steps 4b-ii-b, 4c, 4d, 4e and 4f remain shut, as do the
configuration freeze, the capacity selection, the threshold calibration and every pilot, validation
and test read.
