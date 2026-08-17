# Human Report — Claude Session 146

**Current date and time:** 2026-08-16 20:13 PDT (measured with the shell immediately before writing
this report)

**Agent:** Claude · **Branch:** `main` · **Phase:** 2 (Execution)

---

## Outcome in one paragraph

Codex ruled against me, and it was right. In my Session 145 I repaired a public running-log entry in
the project's live README *in place*, on the reading that append-only discipline attaches to an entry
whose review has closed and this one never had. Codex's Round-2 review returned **Revisions
Required** on exactly that, and this session I accepted it without contest and rebuilt the repair the
way the playbook and this project's own precedent require: the published entry is restored byte for
byte, and the two corrected facts now live in a dated correction entry beneath it. The new candidate
is a **purely additive** successor to the bytes that were public — zero deletions — and both reverse
constructions were re-proved on the new bytes rather than inherited. I then spent the rest of the
session on the only unbuilt half of the connection adapter, Step 4b-ii-b, deriving the row-18 forward
kinematic map **from the producer source rather than from memory** and writing it into my build plan
as a measured appendix, so the next session starts from numbers instead of re-deriving them. **Zero
scientific resource was spent.**

---

## 1. What I did, in order

### 1.1 Read the state and found a ruling waiting for me

`.agent-turn` named Claude; no session lock existed; I created one, re-read the turn file, and began.
I read `AgentPrompt.md` and `Project Details/Project Details.md` in full, my continuity file, both
active chats, the governing Review Card including Codex's full Round-2 section, and Codex's
`HumanReport145.md`.

My own continuity file had recorded the open question honestly and had pre-committed my response to
either outcome: *"If Codex rules the other way in Round 2, convert it to a dated successor entry —
that is cheap and it is the whole remedy."* Codex ruled the other way. That pre-commitment is the
reason this session's response took no argument and no extra round: the decision had been made when
I could still see both sides, not after a ruling had gone against me.

### 1.2 Authenticated everything before touching a byte

I extracted all three README states from the Git object store into a scratch directory **outside the
repository** and re-measured every identity rather than carrying the card's figures forward:

| state | Git blob | raw SHA-256 | bytes / LF / CR |
|---|---|---|---|
| approved predecessor | `11a424b7…` | `f3d1dd86…` | 154,471 / 220 / 0 |
| Round 1 candidate (the published one) | `81ddcdac…` | `bec7c98c…` | 155,610 / 222 / 0 |
| Round 2 candidate (superseded) | `9d29deb7…` | `f6b6abd9…` | 155,818 / 222 / 0 |

All three digests reproduced exactly. Every blob id resolved with `git cat-file -t`.

### 1.3 Built the Round-3 candidate under preconditions, not by editing

Rather than hand-editing the file, I wrote a short build script that **refuses to write unless every
precondition holds**: the two source blobs hash to their recorded digests, the entry sits at the
expected line, the blank line and section rule sit where expected, and — the important one —
**deleting the inserted range reproduces the published Round-1 bytes byte for byte**. Only then does
it write. That inverts the usual order: the proof runs before the change, not after it.

The result:

| state | Git blob | raw SHA-256 | bytes / LF / CR |
|---|---|---|---|
| **Round 3 candidate** | `7342bc8ca5a256a411d69577199cc0c2e3dbc2d0` | `1c649ed6c84ec456ae2f7a5fadf6163d86e76b2e0ef6dca653b4b9b0a436bde0` | 156,193 / 224 / 0 |

**The delta, measured from both directions, and the second is the one that matters:**

- against `HEAD` (the superseded Round-2 state): `git diff --numstat` = **`3 1`**, one hunk;
- against the **published** Round-1 blob: **`2 0`** — one hunk, **zero deletions**.

The second number is the whole point. Append-only is a property of what the public page has shown, so
the delta that has to be purely additive is the one against the bytes that were public — not the one
against whatever `HEAD` happens to hold. That became a standing lesson (258).

I also proved the *unchanged* side as directly as the changed side: split on LF, the candidate has
225 elements to Round 1's 223, elements 1–200 are equal element for element and 203–225 equal Round
1's 201–223. The candidate carries 108 dated log entries; the 106 before the restored one are
bit-for-bit identical.

### 1.4 Handed off Round 3

I appended the Round-3 owner delta to `Review Card/Public README Step-4b-ii-a Heartbeat.md` (`117 0`,
purely additive) and the matching turn to the subject chat (`62 0`, purely additive, prefix-verified
against Codex's own published post-write digest `2cf85937…`, my header appearing exactly once and my
turn physically last). I approved the exact state and handed it back for a delta-only Round 3 review.
**Codex owns the next turn.**

### 1.5 Then moved to the actual build work

With the review turn spent, I went to the one piece of unbuilt connection-adapter work — Step
4b-ii-b — and did the part of it that is settled by *reading the packet* rather than by writing code.
Section 6 of my build plan sequences the coherent geometry fixture first, because row 18 is the row
most likely to move the design. I derived its forward map from the producer source and wrote it into
the plan as **Appendix A**, measured this session:

- 17 points per link → **16 bodies**, **15 internal deformation bodies** per link;
- `n_def` = **90**, and 2 links × 15 bodies × 3 rotation-vector components = 90 — the arithmetic
  closes;
- segment length **0.025 m** (0.4 m ÷ 16), matching `half_segment` = 0.0125 in the MJCF;
- `deform_coords` emitted as **L1 internal bodies 1–15 then L2 internal bodies 1–15**, each a
  **log map**, so triplet *k* belongs to a specific body of a specific link;
- both actuators geared about the **model y axis**, so the motion is planar in model **x–z**, the
  planar advance is the **y component (index 1)** of each triplet, and the scene projection is
  model *x* → scene *x*, model *z* → scene *y*;
- the base point is model `(0, 0, 0.5)`;
- and I **re-measured** that exit status 15 is free — `X_SCENE_OK` → 0 and the twelve refusals →
  3…14 contiguously — by importing the live table on this checkout rather than reading it off the
  design.

None of those are free parameters. A "coherent" fixture that picks a different `n_def` or segment
length is not a synthetic instance of this chain at all, and the record's geometry block would then
describe a model the producer digest does not name.

---

## 2. The one thing I deliberately did **not** settle, and why that is the right answer

Everything above came out of the source. One thing could not: **the sign**.

A positive rotation about `+y` carries `+x` toward `−z`, so under the obvious reading of the
projection the scene-frame tangent angle advances by *minus* the y component. That is a plausible
derivation and I refused to assert it, because settling it properly means running the real model and
the adapter is **forbidden from importing MuJoCo** (invariant V18 — the point being that a reader who
installed the packet on a laptop must be able to open the verification surface).

The structurally correct answer is not to guess and not to stall:

1. the connection record **declares** the component and the sign, and the adapter applies what is
   declared and invents nothing;
2. the coherent fixture generates and checks under **one** declared convention, which proves the
   **derivation logic** — it does not and cannot prove the convention matches MuJoCo;
3. **a flipped sign is exactly the failure the geometry-validation artifact's maximum-deviation field
   catches**, because a flip misses by centimetres rather than nanometres. That artifact does not
   exist yet and Step 4b does not build it.

So the question is not *open* inside 4b — it is **assigned**, and to the round that owns the
instrument that can decide it. That is a meaningfully safer state than "unresolved," and naming the
difference is the third standing lesson from this session (259).

---

## 3. Challenges, and how they were handled

**A ruling that went against me on an axis I had not looked at.** My Round-2 argument was not
careless — it distinguished a candidate under review from published history, and it named the cost of
being wrong. It was simply aimed at the wrong property. Append-only protects *what a reader has been
able to see*, not *what a review has settled*, and blob `81ddcdac…` had been committed, pushed and
public for hours. Review state cannot reach backwards through publication.

**The part that stings, and that I put in the card rather than leaving out.** The rule I broke was
one I had written myself, in the same Review Card, two screens above the violation: acceptance
criterion 4 says the repair for an entry made wrong is "a dated successor entry, never an edit to the
entry that went stale." I wrote that about a stale *forward-looking* sentence and did not apply it to
the plainer case of an entry that was simply *wrong*. A rule you wrote for a narrow case is the first
place to look when the broad case arrives, and its author is the reader least likely to notice that
it generalises.

**Reporting a criterion against myself.** My own card said the entry should be "roughly 160 words."
The restored entry plus its correction now runs 189 + 99 = 288. The correction is the smallest
instrument that carries two facts, but the total is the total, so I stated the arithmetic in the card
and the chat and offered to take a shorter correction — rather than leaning on the card's own
classification of length as non-blocking to avoid mentioning it.

**Judging how much build work to start.** Step 4b-ii-b is the largest single build left in the
project, and this project's bar for a new module is high (the last two builds shipped 109 and 185
focused tests, each with a two-pass mutation sweep before handoff). Starting the module with the
budget left after a full review round would have produced something below that bar and left the
packet in a half-built state. I chose the piece that is genuinely bounded, verifiable now, and
de-risks the build — the measured derivation — and left the code for a session that can finish it
properly.

---

## 4. Decisions I made

1. **Accept finding 3 without contest.** It was correct, my continuity file had pre-committed to
   this outcome, and arguing it would have spent a round on a question already settled by the
   playbook's own text.
2. **Restore the published entry byte for byte and append a dated correction** — the instrument this
   project's immediately preceding heartbeat card already established, and the one my own card's
   criterion 4 names.
3. **Quote the delta against the published state as well as against `HEAD`**, and lead with the
   purely additive one, because that is the number the append-only property is a claim about.
4. **Build the candidate under preconditions rather than by editing**, so the append-only proof runs
   before the write and the write cannot happen if the proof fails.
5. **Do not add a heartbeat entry for this session.** The check ran and answered *no*: this session
   finished no artifact, closed no phase and produced no result, and the README is itself the
   candidate under review. A log entry about revising a log entry is exactly the session-journal
   texture the playbook forbids.
6. **Do not assert the geometry sign convention**, and instead name the artifact that can settle it.
7. **Carry Codex's non-blocking wording correction forward rather than rewriting the sentence** —
   4b-ii-b is the only unbuilt *connection-adapter half*, not the only unbuilt work in the project;
   Steps 4c–4f are unbuilt too, they are merely blocked rather than startable.

---

## 5. Resource spend — zero, and stated exactly

**Counters unchanged: 278 rollouts, 67 fits, 67 checkpoints, zero pilot / validation / test reads.**

This session opened no role index, role payload, checkpoint, estimator output, controller log,
production configuration or pilot/validation/test result; built no MuJoCo model; stepped no rollout;
ran no fit; and rendered no figure. **No executable packet file changed**, so no test suite was re-run
and none needed to be — the last measured figures stand at 185 focused and 2,793 packet-wide.

**The disclosed reads**, all of tracked development text, none opening a payload behind it:
`scripts/utils/cable_mechanics.py`, `scripts/utils/synthetic_plant.py` (line references only),
`scripts/utils/verification_scene.py` (exit table and the centerline contract),
`config/draft-config-v0.1.json` (`values.plant`), `schema/schema.json` (`deform_coords` declaration),
and sections 2.4, 3.5, 4.5 and 4.6 of the approved Step-4a design. I imported
`utils.verification_scene` in the project's own virtual environment solely to print its exit-code
table.

All scratch work — the three extracted README blobs, the build script, the chain proof and the
prepared append blocks — lived **outside the repository** in the session scratch directory.

---

## 6. Files created or updated

| path | change |
|---|---|
| `README.md` | Round-3 candidate: published entry restored byte for byte, one dated correction appended. `3 1` vs `HEAD`, **`2 0` vs the published blob** |
| `Review Card/Public README Step-4b-ii-a Heartbeat.md` | Round-3 owner delta appended (`117 0`); status header updated to name Codex's turn |
| `chats/Claude-Codex/Public README Step-4b-ii-a Heartbeat/… - Active.md` | Round-3 owner turn appended (`62 0`, prefix-verified) |
| `agents/Claude/Slot-8 Step-4b-ii-b Build Plan.md` | **Appendix A** — the row-18 forward map measured at source, plus A.6 carrying Codex's wording correction forward (`117 0` + `9 0`) |
| `agents/Claude/Permanent Instruments.md` | standing lessons **257, 258, 259** (`44 0`) |
| `agents/Claude/Session Summaries/HumanReport146.md` | this report |
| `agents/Claude/README.md` | workspace guide refreshed |
| `agents/Claude/Summary of Only Necessary Context.md` | rewritten for Session 147 |

---

## 7. What happens next

**Codex owns the delta-only Round 3 review of the README candidate.** This is the third owner
handoff, so its response is the third reviewer turn — the limit this card operates under. If it
approves, the card closes. I hold no contested position on it, so any residual would be Codex's to
classify under the convergence ladder, which has still never fired.

**The next build session starts at Appendix A of the build plan** and writes the coherent geometry
fixture and its fixture-scoped geometry-validation artifact, then rows 13–21, the audit-hook
observer, the acceptance tests, the CLI wiring, and the two-pass mutation sweep **before** the
handoff. The Review Card and subject chat for 4b-ii-b are still deliberately unopened: a card names a
candidate, and there is no candidate yet.

**Nothing about the project's scientific position moved, and that is correct.** Every scientific lane
remains spent or shut. No configuration is frozen, no capacity is selected, no threshold is
calibrated, no pilot, validation or test data has ever been read, and the project's central question
remains unanswered. What moved this session is the honesty of one public page and the readiness of
one build.
