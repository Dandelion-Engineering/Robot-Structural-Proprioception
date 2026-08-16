# Review Card — Public README Step-4b-ii-a Heartbeat

**Status:** Open — Round 1 handed off (Claude Session 144)
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
