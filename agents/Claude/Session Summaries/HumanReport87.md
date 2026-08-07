# Claude — Human Report, Session 87

**Date and time:** 2026-08-06 20:23 PDT *(taken from the shell at the moment of writing, not estimated)*

**Phase:** Phase 2 — Execution

**Physical rollouts spent this session:** **0.** Project lifetime Protocol-P-related total remains **278.**

**Fits run:** **0.** Checkpoints written: **0.** Data generated: **0.** Real-data touches: **zero of every kind.**

**Progress-report session:** no. My next regular progress report is Session **88** — i.e. my next session.

---

## Summary

Two things happened this session, and the second one is the more important of the two.

**First, I contested Codex's approved test state — over a comment, with a measurement.**
Codex's Session 86 reviewed the fixture repairs I returned in Session 86, accepted all three,
and found a genuinely false comment in my bytes: I had written that the majority class in the
test fixture was "neither the first nor the last key" of the count mapping, and it is in fact
the last key. Codex was right, and it was right to refuse to approve bytes carrying a false
statement about the executable contract — that is exactly the standard I applied to Codex's
work the session before.

What I found on re-review is that Codex's *replacement* comment has the same defect one notch
smaller. It says the fixture "pins the selector rather than an iteration-order or tie
accident." A selector that simply takes the **last** key of the mapping is an iteration-order
accident, and it is not pinned. I rebuilt the mutation harness and measured it: against
Codex's approved bytes, replacing the production `max(...)` with `list(counts)[-1]` **survived
the whole focused suite**, while first-key, `min`, and a mutated accuracy baseline were all
caught.

The cause is structural rather than accidental, which is why it is worth the round. The class
census is built in the canonical order `(healthy, structure, actuator, sensor)`, so a fixture
with ascending counts puts the majority at the last key, and "take the largest" is then
indistinguishable from "take the last." **And the delivered data cannot rescue it**: the real
census is 8/16/32/96, also peaked on `sensor`, also last. There is no state of the real dataset
and no other fixture in the packet that can tell those two implementations apart.

I repaired it by reordering the fixture's counts from `(1, 2, 3, 4)` to `(1, 2, 4, 3)`, which
moves the majority to `actuator` — neither the first key nor the last. All four mutants now
die. Because the proportions are the same multiset, every number the test pins is unchanged.
The test count stayed at **35**: I added no test, I made one able to fail.

**Second, I designed the next real piece of science and handed it over.** With the dev-fit lane
otherwise closed, the identified next work is the Slot-9 capacity sweep that carried limitation
127 says must be run before any C1-vs-S reading is drawn from rung 1. I wrote a v0.1
pre-registration for it, `Reproducibility Packet/protocol/capacity-escalation-v0.1.md`, and
handed it to Codex. It authorizes nothing. Its most useful content is the three things it
settles before any number exists: that no Claim Sheet amendment is needed, that the dev-fit
contract's bound 5 permits this measurement and forbids the use it would most easily be put
to, and that an in-sample capacity sweep on 152 examples has a saturation trap that would
otherwise have produced a confident and circular answer.

**I deviated from Codex's stated sequencing to do that, and flagged it as a deviation at the
top of its own section in the handoff**, with the reasoning and with the decision handed back
to Codex rather than taken.

---

## Work completed

### 1. Owner re-review of `4481ba32` — contested, with the measurement

Codex's change to my Session-86 state was two comment lines. My review of it:

- **Codex's correction is accepted without reservation.** `sensor` is the last key of
  `SOURCE_CLASS_ORDER = ("healthy", "structure", "actuator", "sensor")`; my comment said it was
  not; the comment was false and the correction was owed.
- **Codex's replacement is narrower but still overclaims**, and I established that by
  measurement rather than by reading.

The sweep, run twice with identical results:

```text
AGAINST 4481ba32 (fixture counts 1,2,3,4)
  majority = list(counts)[-1]            *** SURVIVED ***
  majority = next(iter(counts))              caught
  majority = min(..., key=...get)            caught
  majority_class_accuracy = min(props)       caught
  NEGATIVE CONTROL blank line                SURVIVED   (must survive)
  NEGATIVE CONTROL reworded comment          SURVIVED   (must survive)

AGAINST 6f29bf05 (fixture counts 1,2,4,3 — the state I return)
  all four mutants                           caught
  both negative controls                     SURVIVED
```

Zero bad anchors in both sweeps. The restore digest was re-verified in a `finally`. The
byte-identity tripwire `test_tracked_analysis_names_the_current_analyzer` was deselected **and
the deselection was asserted** — the harness raises `SystemExit` if the word "deselected" is
absent from pytest's output, because `pytest --deselect` silently ignores a node id that
matches nothing. That rule exists because it fooled me in Session 85.

### 2. The repair, and the choice behind it

Two options were available: weaken the comment to describe exactly what the fixture pins, or
strengthen the fixture so both comments become true. I chose the second. Weakening would have
been accurate, cheaper, and would have left a real coverage gap sitting behind a sentence that
had stopped claiming to cover it. I said so explicitly in the handoff and noted that it is a
two-line revert if Codex disagrees.

I also rewrote the fixture's docstring to carry **both** measured survivors — Codex's from
Session 86 (a uniform census makes `max` and `min` the same answer) and this session's (an
ascending census makes `max` and last-key the same answer). A fixture property with no recorded
reason beside it is the first thing a later session deletes.

### 3. The capacity-escalation design, v0.1

`Reproducibility Packet/protocol/capacity-escalation-v0.1.md` — 21,576 bytes, 385 lines, LF,
raw digest equal to canonical, git blob `b86d46aa`, canonical sha256 `2250add1…`. It is a
**draft**, approved by nobody.

Its substantive content:

- **No amendment is required.** Slot 9's ladder says escalate when "there is no signal yet but
  a larger-capacity model could plausibly capture one the smaller model cannot," which is
  limitation 127 restated in measurements; and Slot 14 already requires the Technical Report to
  contain "the within-suite capacity sweep." The document is that sweep's implementation
  pre-registration, not a new activity.
- **Bound 5 is the real tension, and it is resolved in a table rather than finessed.** A dev fit
  "may expose failure modes" and "may not select a headline capacity." So the sweep answers *is
  the rung-1 deficit capacity-bound?* and does **not** choose what the project ships, which
  stays validation-owned at Gate 5/6. If the executable is ever used to pick the shipped
  capacity, bound 5 has been violated regardless of the numbers.
- **Stage 1 does not climb the ladder at all.** The four proposed capacity points — 10,586 /
  22,786 / 39,594 / 87,034 parameters — all sit inside Slot 9's declared rung-1 band
  `[10⁴, 10⁵]`, so the `enforce_rung1_band` guard I built in Session 77 stays *on* for every
  arm. Escalation past the band is Stage 2, is not proposed, and needs its own document.
- **Width, not depth.** `n_blocks` sets the parameter count *and* the receptive field, so a
  depth sweep would vary capacity and how much of the window the network can see at the same
  time. Varying width holds the receptive field at 1,023 samples at every point — measured, and
  the constant column is in the table.
- **The saturation trap, named before any number exists.** There are 152 training examples per
  arm and no held-out set. As capacity grows, both arms approach a perfect in-sample fit and the
  paired difference goes to zero *for reasons that have nothing to do with information*. A sweep
  run far enough would therefore always show the deficit closing. The read is conditioned on a
  pre-declared saturation criterion, and a deficit that closes only at or above the first
  saturated point is explicitly **not** evidence that the deficit was capacity-bound.
- **The ten existing arms are reused, never re-run** — partly for cost, mostly because
  re-fitting would produce a second set of checkpoints claiming to be the same arms, and the
  existing ledger is the sole provenance record for ten git-ignored weight files.
- **Cost, measured on synthetic tensors** (no data read, no fit, no checkpoint): 0.015–0.026 s
  per optimizer step across the band, so the thirty new fits are roughly four minutes of
  optimizer time. Two qualifications are in the document: it excludes row loading, and **the
  approved ledger records no elapsed time for the ten Session-84 fits**, so there is no measured
  whole-run figure to calibrate against and none should be invented.

Section 9 poses five open questions I deliberately did not answer. Two are labelled as
favouring me: the four-point grid over a denser one, and my decision *not* to add a within-dev
held-out split by trajectory. The second is the one I most want Codex's read on — it would give
a genuine generalization signal and stay inside the contract's bound 1, and I declined it
because it halves the training set to 76 examples and breaks comparability with my own approved
ledger. That is exactly the shape of reason that deserves a second pair of eyes.

### 4. Cross-review and chat duties

- Read Codex's `HumanReport86.md` and the work it points at, and its Session-86 chat turn in
  full before touching anything.
- **Transcript-order monitoring, verified at the git level rather than assumed:** Codex's
  Session-86 commit touches the Phase-2 transcript as a single tail hunk
  `@@ -23525,3 +23525,92 @@`, additions only, and touches the monitoring file not at all. **No
  recurrence, so no note was added** — the duty is to flag recurrences.
- My own Phase-2 append: `+176/−0`, single tail hunk, header unique at line 23,618, Claude
  physically last, the pre-write state asserted byte-identical *inside* the writer, the turn
  asserted pure ASCII before writing, and the prefix re-verified byte-identical afterwards.

---

## Challenges and how they were handled

- **The finding is a comment, and comments are where a round can become theatre.** The
  discipline that kept this honest was refusing to argue about the sentence and measuring the
  behaviour instead. If the last-key mutant had died, I would have approved Codex's bytes and
  said so.
- **I nearly took the cheap repair.** Weakening the comment would have closed the loop this
  session and left the gap. I recorded the choice and the revert path rather than presenting the
  stronger repair as the only option.
- **The design document risked being an amendment when it did not need to be.** The first draft
  of my reasoning had this as a Slot-9 change. Reading Slot 14 showed the within-suite capacity
  sweep is already a contracted deliverable, which turns a proposed amendment into an
  implementation pre-registration — a much smaller and much better-supported thing.
- **Bound 5 and "climb the ladder" genuinely conflict on their face.** I resolved it by
  separating the two questions and naming their owners, rather than by quoting whichever clause
  suited the work I wanted to do.
- **Costing the sweep with no elapsed time in the ledger.** The approved fit ledger records no
  wall-clock, so there was nothing to calibrate against. I measured the per-step cost directly
  on synthetic tensors and stated both what that excludes and that the missing ledger figure
  must not be reconstructed.

---

## Important decisions and reasoning

1. **Contest rather than approve.** The state carried a comment I had measured to be false. I
   applied to Codex exactly the standard Codex applied to me one session earlier.
2. **Strengthen the fixture rather than weaken the comment**, because the second leaves a real
   gap behind an accurate sentence. Flagged as reversible.
3. **Reorder the counts rather than change their values**, so the cross-entropy, the majority
   accuracy and every other pinned number stay bit-identical and the diff is about one property
   only.
4. **Design the capacity sweep now, against Codex's stated sequencing** — flagged as a
   deviation, with the reasoning stated and the sequencing decision handed back.
5. **Propose Stage 1 inside the rung-1 band.** It answers limitation 127's question at the
   cheapest rung, needs no ladder-escalation decision, and leaves Slot 9's rung 2 to arrive with
   a measured reason if it arrives at all.
6. **Do not go straight to rung 2.** It changes size and architecture family at once; if the
   deficit vanished there, nothing would say which change removed it.
7. **Leave the Live-Run README untouched.** Heartbeat check run: no artifact finished (the test
   loop is contested, the design is a draft), no phase closed. An open review round is work in
   progress, which the lean log is explicitly not for.

---

## Insights gained

- **A fixture can be non-degenerate in one dimension and degenerate in another, and fixing the
  first makes the second look handled.** Unequal counts fixed the `max`-vs-`min` blindness and
  left `max`-vs-last-key untouched, because ascending counts put the answer at the boundary. The
  general move: *name every wrong implementation the fixture is supposed to exclude, then check
  the expected answer is not producible by any of them.* Preferring an answer that is neither
  the first nor the last element is a cheap way to get most of that for free.
- **"The real data has this shape too" is not a defence — it can be the same blind spot.** The
  delivered census is peaked on `sensor`, so reality shares the fixture's degeneracy exactly.
  When a fixture and the production data agree on an accidental property, nothing in the project
  can see past it.
- **The saturation trap is the design lesson I would keep.** An in-sample capacity sweep on a
  small training set is *guaranteed* to show the gap closing. Writing that down before running
  anything is the difference between a measurement and a self-fulfilling one — and it is the
  same shape as the project's older rule that a control which varies the thing it controls for
  is not a control.
- **Eighth consecutive round with the defect one layer below the repair**, and the second in a
  row inside a repair the other agent made to my work. It is no longer an observation; it is
  where to look first, and it does not weaken because the repair came from the reviewer.
- **A round that finds only coverage is usually the signal to close** — but not when the state
  being approved makes a claim the coverage measurement contradicts. The deciding factor was not
  the size of the gap; it was that the bytes asserted a property I had measured to be false.

---

## Files created or updated

Created:

- `Reproducibility Packet/protocol/capacity-escalation-v0.1.md` *(draft, approved by nobody)*
- `agents/Claude/Session Summaries/HumanReport87.md`

Updated:

- `Reproducibility Packet/tests/test_dev_fit_analysis.py` — `4481ba32` → `6f29bf05`
- `chats/Claude-Codex/Phase 2 Integration and Config Freeze/Phase 2 Integration and Config Freeze - Active.md`
- `agents/Claude/README.md`
- `agents/Claude/Summary of Only Necessary Context.md`

Reviewed and deliberately unchanged:

- `README.md` (root, Live-Run — heartbeat check run, no entry warranted)
- `chats/Claude-Codex-Human/Transcript Order Monitoring/…- Active.md` (no recurrence)
- `Reproducibility Packet/scripts/analyze_dev_fit.py`, `results/dev_fit/dev_fit_analysis.json`,
  `results/dev_fit/dev_fit_result.json`, `Reproducibility Packet/README.md`

---

## Verification

```text
mutation sweep, 4481ba32             4 cases | 3 caught | 1 SURVIVOR (last-key) | 0 bad anchors
mutation sweep, 6f29bf05             4 cases | 4 caught | 0 survivors | 0 bad anchors
                                     two passes agreed in both; restore digest re-verified;
                                     tripwire deselected AND the deselection ASSERTED
negative control                     2 semantically inert edits, both SURVIVED, in BOTH sweeps
analysis focused suite               35 passed (count UNCHANGED from Codex's 35)
trainer + contract + analysis        177 passed under python -O, expected warning only
FULL PACKET SUITE                    1,551 passed in 119.94 s  (Codex S86: 1,551 — no change)
compileall                           clean
git diff --check                     clean (expected autocrlf notices only)
analysis_code_identity()             nine production modules, NO test file — checked, not assumed,
                                     so NO artifact regeneration was required
production blobs unchanged           analyze_dev_fit.py 31381b18 | dev_fit_analysis.json 0d00b5ca
                                     dev_fit_result.json d4cefb61 | packet README eb4a58e4
design document                      b86d46aa | canonical 2250add1… | 21,576 B / 385 lines / LF
                                     raw == canonical, no BOM, eol=lf confirmed via git check-attr
transcript, Codex S86 append         single tail hunk @@ -23525,3 +23525,92 @@, additions only,
                                     monitoring file untouched — NO RECURRENCE
transcript, my S87 append            +176/-0, single tail hunk, header unique at line 23,618,
                                     pre-write sha asserted inside the writer, prefix re-verified
FITS 0 | CHECKPOINTS 0 | GENERATION 0 | ROLLOUTS 0
lifetime Protocol-P physical execution unchanged at 278
REAL-DATA TOUCHES                    ZERO of every kind. No manifest, no .npz, no checkpoint,
                                     no regeneration. PILOT / VAL / TEST: 0
config/config.json                   absent
```

---

## Next steps

1. **Codex approves or contests `6f29bf05ddebae9f33817381f4713089f99ee7e4`.** If it approves,
   every Gate-4 dev-fit loop is closed.
2. **Codex rules on sequencing for the capacity-escalation design** — reviewable now, or held
   until the test loop closes. Either is fine; the call is Codex's because the deviation was
   mine.
3. **The design's five open questions**, of which question 2 (a within-dev held-out split by
   trajectory) is the one with real scientific weight.
4. **My Session 88 is a regular progress report session** — covering Sessions 81–88 — in
   addition to whatever the work is.
5. Unchanged and still blocked: reading pilot, validation or test rows; any threshold or
   calibration work; the config freeze; confirmatory generation; any rollout.
