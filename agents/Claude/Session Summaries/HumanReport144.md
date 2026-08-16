# Human Report — Claude Session 144

**Current date and time:** 2026-08-16 16:16 PDT (measured with the shell at the time this report was started; the session ran 16:02–16:5x PDT)

**Agent:** Claude · **Branch:** `main` · **Phase:** 2 (Execution) · **Session type:** owner same-state re-review, review closure, and a regular progress-report session (144 = 18 × 8)

---

## Outcome in one paragraph

I performed the delta-only owner re-review of Codex's Round-3 reviewer-edited bytes on Slot-8
Step-4b-ii-a, re-drove every figure it published, ran an independent two-pass mutation control on
its delta, and **approved the exact same bytes**. The Review Card closed with terminal outcome
**Approved with Follow-ups** and its subject chat is concluded with a `Summary.md`. I recorded one
non-blocking tracked follow-up rather than opening a fourth round-trip. I also confirmed Codex's
self-disclosed transcript-order fault independently against primary Git objects and posted the
monitor entry, published one lean public-README heartbeat entry with its own new Review Card and
chat, and wrote the Session-144 progress report. **Zero scientific resource was spent.** Counters
unchanged: 278 rollouts, 67 fits, 67 checkpoints, zero pilot/validation/test reads.

---

## What was accomplished

### 1. The owner re-review, and the decision it turned on

Codex's Session 143 returned Round 3 with two **mechanical reviewer corrections** applied directly
to my candidate and approved its own edited state. Under the superseding review method the owner
must then genuinely re-review both the feedback and the edits and either explicitly approve or edit
and hand back. Round 3 is the ordinary final round, so this was the turn that either closed the
card or entered the convergence ladder.

**I approved.** Both corrections are right, and the first of them corrects a claim I made.

**Correction 1 — the schema-digest guard.** `authenticate_config` now compares the configuration's
declared raw `schema_sha256` against the raw digest of the schema bytes the adapter authenticated,
*before* calling `validate_config_document`. My Round-3 docstring had argued that such a comparison
"would be a guard no input could make decisive," invoking my own lesson 242. That reasoning was on
the wrong axis. What matters is not that the config's declaration is fixed for the call, but which
object it is compared against: the closed contract compares it against a **second read of the
path**, the guard compares it against **the bytes this module authenticated**. Those separate on
exactly the residual state I had already written down in my own handoff and then argued around — a
config declaring schema B while the record authenticates schema A, with the file swapped between
the two reads. That is lesson 238's shape landing on the agent who wrote lesson 238.

I checked that the new regression separates the guard **for the reason claimed** rather than by
message text: it asserts the refusal names `schema_sha256`, a phrase the closed contract's own
refusal message also contains (the lesson-223 trap). It is not the trap here — with the guard
deleted, the swapped file and the config agree, the contract *accepts*, and no refusal is raised at
all. Mutant `m01` confirms it in both passes.

I also verified the **domain** is right rather than lucky: `config_contract.validate_config_document`
compares against `file_sha256(schema_path)` — raw bytes, no folding — so `external_bytes_digest` is
the only comparand that agrees with the rule this guard anticipates.

**Correction 2 — the `.npy` kind check.** `np.load` on a single-array stream returns an ndarray,
which has no context-manager protocol, so `with np.load(...)` leaked a raw `TypeError` out of the
layer whose whole contract is to refuse unsafe payloads. Same defect shape as the `BadZipFile` pair
I closed in Round 3; I missed the third member of the set. Accepted without contest. I confirmed
`np.lib.npyio.NpzFile` resolves under the pinned `numpy==2.5.1` and is the packet's only use of that
path.

### 2. Independent verification of the reviewer's evidence

Every figure Codex published reproduces:

| check | Codex | me |
|---|---|---|
| focused suite | 185 passed | **185 passed (5.75 s)** |
| focused suite under `PYTHONOPTIMIZE=1` | 185 passed | **185 passed (5.82 s)** |
| packet-wide suite | 2,793 passed / 154.90 s | **2,793 passed / 151.61 s** |
| `py_compile` | clean | clean |
| `git diff --check` | clean | clean |
| fresh-interpreter import | clean | clean, `torch` and `mujoco` both absent |

All four candidate blob ids resolved with `git cat-file -t`; all twelve identity numbers (blob, raw
SHA-256, bytes/LF/CR) re-measured from the object store and matching. `git status --porcelain` empty,
so the working tree **is** the approved state. `git diff --numstat` quoted rather than hand-counted:
`13/6`, `22/18`, `10/3`, `65/5`. The arithmetic that says the delta adds one test and changes no
existing one holds: 2,792 + 1 = 2,793.

### 3. My own mutation control on Codex's delta — and its two survivors

I budgeted a two-pass sweep **before** responding, because the sweep has now changed the tests on six
consecutive builds and a reviewer's edit is not exempt from that. **8 real mutants + 3 negative
controls**, staged entirely in a scratch directory outside the repository, green anchor confirmed at
185 before any mutant ran, target digests restored and re-verified after every mutant, identical
across both passes, 2m 05s.

**6 of 8 real mutants caught.** The two survivors — the schema comparand changed to
`canonical_text_digest`, and changed to `record.schema.sha256` — are **equivalent mutants**, and I
settled that by measurement rather than by argument:

- `schema/schema.json` carries no BOM and no CR byte, so its canonical and raw digests are the same
  number. Driven at source, `canonical_text_digest(raw)`, `external_bytes_digest(raw)` and
  `config_contract.file_sha256(path)` all return
  `0dae0dd0fec4269180139efc9a4c9ce38e7f8f23d890d182dc8eb063803e942f`.
- `authenticated_bytes` has already proved `record.schema.sha256` equals the canonical digest of
  those bytes, so the second mutant collapses into the first.
- A fixture that separated the two domains would have to be a CRLF `schema.json`, which the packet
  forbids by pin.

**And I used the instrument that sees this class rather than another test** (lesson 232).
`git checkout-index` into a scratch path outside the repository under `core.autocrlf=true`:
`schema.json` materialises at 15,212 B / 670 LF / **0 CR** with a raw digest identical to the tracked
blob — the pin holds on a fresh Windows checkout. The same probe rendered `connection_adapter.py`
with 2,115 CR, which is what says the probe was actually exercising CRLF conversion and that the
schema result is the pin working rather than the measurement failing.

### 4. One control I got wrong, reported rather than quietly rebuilt

My first sweep reported one of two negative controls **caught**, and the control was malformed rather
than the suite being sensitive. My "inert rename" of a local variable renamed three references and
missed `type(loaded).__name__` inside an f-string, so the mutant was a `NameError`. A control that
fails to compile measures nothing, in exactly the way a red anchor measures nothing — and it reports
as a *result*. I rebuilt it as a complete rename, added a third control, and re-ran: all three
survive in both passes. This is in the Review Card and the chat turn, because the sweep is the
instrument both agents rely on and a silent repair to it is a silent repair to the shared evidence
base. Lesson 251.

### 5. The tracked follow-up, and why it is not a fourth round

**The adapter's raw-domain schema comparison is silently dependent on the
`schema/schema.json text eol=lf` pin.** Both `.gitattributes` files already call that pin
load-bearing and name `config_contract`'s raw comparison as the reason; Codex's guard makes it
load-bearing for a **second** consumer, and nothing in the candidate says so. The dependency is
undetectable from inside the packet precisely because the pin makes the two domains the same number
— so "add a test" is not available as an answer, and documentation is the whole repair.

I registered it as a follow-up carried into the 4b-ii-b card rather than a Round-4 finding. Under the
card's own blocking-severity definition it cannot invalidate the scoped purpose and the behaviour is
correct on every conforming checkout. The round limit never forces approval — and it equally does not
license spending a fourth round-trip to add a docstring sentence. Lessons 253 and 256.

### 6. Transcript-order recurrence — independently confirmed

Codex disclosed against itself that its first Session-143 chat append matched a repeated
`— Claude` / `---` delimiter and landed at line 193 instead of the physical EOF; its own post-write
prefix check caught it in-turn, it left the misplaced entry standing and appended a dated correction
at the physical tail. I confirmed the whole account against primary Git objects:

- my Round-3 state measures **38,317 B / 578 LF / 0 CR / `8f7b3a9be32eb2ea…`** — exactly the prior
  tail Codex named;
- `git diff --numstat` reads **`106 0`** — two hunks at `+193` (47 lines) and `+626` (59 lines),
  **zero deletions**;
- deleting exactly those two line ranges reproduces my blob **byte for byte** (`cmp` silent);
- the first 38,317 bytes of the current file hash to `0fb95f854abf2107…`, the number Codex published
  as proof the entry landed before the old boundary;
- both headers occur exactly once and Codex is physically last.

The transferable point I posted is one step to the side of lesson 206 rather than below it: **a
mis-anchored append is exactly recoverable if and only if it is purely additive**, so the monitor
should read the *deletion* count first. Codex's S119 recurrence normalised fifteen CRLF endings and
had no such property. That is now three consecutive recurrences caught in-turn and disclosed by the
agent that caused them. Lesson 255.

### 7. Public README heartbeat — one lean entry, published under a new card

The heartbeat check answered *yes* for the first time since Codex's Step-4b-i entry: a finished,
jointly approved artifact. One dated log entry (~160 words, the lean shape I committed to after
Codex's forward-only note on my 495-word Session-130 entry) plus the banner date. The entry leads
with the artifact and spends most of its length on the repair that had to be undone, because that is
the honest negative a stranger would actually care about.

`git diff --numstat README.md` reads `3 1`, and **the write was conditioned on reconstructing the
predecessor byte for byte** — substituting the old banner line back and deleting the appended entry
reproduces `f3d1dd86…` exactly, so no prior published byte can have moved. Candidate blob
`81ddcdac`, 155,610 B / 222 LF / 0 CR. New card `Review Card/Public README Step-4b-ii-a Heartbeat.md`
and new chat, handed to Codex for Round 1.

### 8. The Session-144 progress report

Written per the eight-session cadence, covering S137–S144, at the Accessible-Piece bar:
`agents/Claude/Progress Reports/Progress Report Session 144.md`. Its spine is the repair we built and
undid, the six-consecutive-builds record of the mutation sweep changing tests rather than confirming
them, and one number I put where Randy cannot miss it — **eight consecutive sessions of mine with
zero scientific measurements**, with the reason and the risk both stated.

---

## Challenges, and how they were handled

**The decision this session actually turned on was whether to open a fourth round.** I had a real
finding (the pin dependency) at a spent round limit. Opening Round 4 would have been defensible on
"the limit never forces approval," and it would also have spent a Codex session to add a sentence to
a docstring. The card's own blocking-severity definition is what settled it, not my appetite to keep
editing — and `Approved with Follow-ups` exists for exactly this shape.

**Two surviving mutants looked like a test gap and were not.** The tempting move was to report "6/8
caught, two gaps, here is the test I'll add." The measurement said otherwise: the pin makes the two
digest domains the same number, so no test can separate them and the survivors are equivalent
mutants. Getting this right required the fresh-checkout probe rather than more test-writing.

**One of my own instruments was broken and reported a false result.** Covered above. The honest
version costs a paragraph; the quiet version would have left a wrong number in the record.

---

## Important decisions

1. **Approve Codex's exact reviewer-edited bytes; close the card at `Approved with Follow-ups`.**
2. **Register the EOL-pin dependency as a tracked follow-up into the 4b-ii-b card**, not as a
   Round-4 finding.
3. **Conclude the 4b-ii-a chat** with a `Summary.md` carrying the load-bearing state, since the
   review closed.
4. **Post the monitor entry**, because a fault reported by the other agent is a reason to post and a
   clean check is not.
5. **Publish one lean README heartbeat entry under its own new Review Card**, following the
   precedent both prior heartbeats set — each of which found a real correction under review.
6. **Do not start 4b-ii-b this session.** It is the only unbuilt work in the project and it needs a
   new card, a new chat and a budgeted mutation sweep, all written before the handoff. Starting it
   after the closeout work would have produced a rushed half-build; the framework is explicit that a
   session does not have to finish anything but does have to hand off cleanly.

---

## Reasoning paths explored

- I initially read the two surviving mutants as a coverage gap and drafted the separating test —
  a CRLF `schema.json` fixture. Reading the `.gitattributes` files stopped that: the pin exists
  specifically so `schema.json` is never CRLF, and a fixture that violated it would be testing a
  state the packet forbids. That inverted the finding from "missing test" to "undocumented
  dependency," which is a different repair in a different place.
- I considered whether the new guard duplicates the closed contract's check (my own lessons 231 and
  242 warn against exactly that shape). It does not: the two compare against different objects and
  separate on a real input. Recorded as lesson 254 because I was the one who invoked 242 wrongly.
- I considered leaving the README heartbeat unpublished on the grounds that 4b-ii-a is half of a
  review split rather than a design sub-step (my own lesson 224). The Step-4b-i precedent settled it
  the other way: that entry was also published on a review-split closure, and the artifact is
  genuinely finished and jointly approved.

---

## Insights gained (standing lessons 251–256)

- **251** A negative control that fails to compile measures nothing — and reports as a result.
- **252** A surviving mutant is not automatically a test gap; ask whether it is equivalent, and
  settle it by measurement.
- **253** When a pin makes two rules indistinguishable, the pin becomes load-bearing for every new
  consumer, and nothing inside the artifact can detect its removal.
- **254** "A guard no input can make decisive" is about *which object is compared*, not *when the
  value is fixed*.
- **255** A mis-anchored append is exactly recoverable if and only if it is purely additive — read
  the deletion count first.
- **256** The round limit never forces approval, and equally does not license turning a documentation
  item into a fourth round-trip.

---

## Files created or updated

**Created**
- `agents/Claude/Progress Reports/Progress Report Session 144.md`
- `agents/Claude/Session Summaries/HumanReport144.md` (this file)
- `Review Card/Public README Step-4b-ii-a Heartbeat.md`
- `chats/Claude-Codex/Public README Step-4b-ii-a Heartbeat/Public README Step-4b-ii-a Heartbeat - Active.md`
- `chats/Claude-Codex/Slot-8 Step-4b-ii-a Authentication Chain/Summary.md`

**Updated**
- `Review Card/Slot-8 Step-4b-ii-a Authentication Chain.md` — closure section, status → CLOSED
- `chats/Claude-Codex/Slot-8 Step-4b-ii-a Authentication Chain/…- Active.md` → **renamed** to
  `…- Concluded.md` (owner re-review turn appended first)
- `chats/Claude-Codex-Human/Transcript Order Monitoring/Transcript Order Monitoring - Active.md`
- `README.md` (root, public) — banner date + one log entry
- `agents/Claude/Permanent Instruments.md` — lessons 251–256
- `agents/Claude/README.md`
- `agents/Claude/Summary of Only Necessary Context.md` — rewritten

**Not changed, deliberately:** every packet script, test, schema, protocol document, configuration
and result. The four candidate files are Codex's approved bytes and this session added no edit to
them.

---

## Scientific resource spent

**Zero.** No production connection record, real role index, real role payload, checkpoint, estimator
output, controller log, production config or pilot/validation/test result was opened. No MuJoCo model
built, no rollout stepped, no fit run, no figure rendered. Counters unchanged: **278 rollouts, 67
fits, 67 checkpoints, zero pilot/validation/test reads.** Checkpoint count not re-read — no fit ran;
it stands at 67.

**Disclosed reads:** `Reproducibility Packet/schema/schema.json` (tracked packet text file, read for
its digest and EOL shape to settle the equivalence claim) and both `.gitattributes` files. The
mutation control ran against a staged copy of `scripts`, `tests`, `schema`, `config` and a trimmed
`results` subset in a scratch directory outside the repository; that tree and the `git checkout-index`
probe tree were both deleted.

---

## Next steps

1. **Codex reviews the README heartbeat card (Round 1).**
2. **4b-ii-b is the only unbuilt work in the project** — read-order rows 13–21, the coherent geometry
   fixture, `X_GEOMETRY_UNSUPPORTED` at exit 15, the audit-hook observer (W3/B4), B2, B5, the
   remaining B3 rows, the roles CLI wiring and the additive `build_role_bundle` change. It needs a
   **new Review Card and a new subject chat written before the handoff**, and its **mutation sweep
   budgeted before the handoff**, not after.
3. **Carry the follow-up into that card:** name `config_contract.file_sha256` as the owner of the
   raw domain the schema guard matches, and name the `schema/schema.json text eol=lf` pin as the
   reason the raw domain is safe there while the record's own authentication stays canonical.
4. **Use `utils.authenticated_storage`; add no entry point to the two closed files.** Editing either
   is an amendment against three approved artifacts and needs its own card.
5. `build_role_bundle` still refuses unconditionally with `X_CONNECTION_UNAUTHORIZED`, and that stays
   correct until the whole of sub-step 4b closes. Every downstream gate remains shut.
