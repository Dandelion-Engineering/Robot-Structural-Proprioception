# Claude — Human Report, Session 92

**Date and time:** 2026-08-07 16:35 PDT

**Phase:** Phase 2 — Execution

**Physical rollouts spent this session:** 0. Project lifetime Protocol-P-related total remains **278**.

**Fits against the delivered dataset: 0. Checkpoint writes: 0. Plan artifacts: 0. Data generated: 0. Pilot / validation / test reads: 0.**

**Progress-report session:** no. My next regular progress report is Session 96; no phase transition and no Claim-Sheet amendment occurred this session.

---

## Summary in one paragraph

Codex froze the capacity-escalation design at the end of its Session 91, closing a five-round
review loop, and authorized exactly one thing: writing the executable that design specifies, plus
its tests. That is what this session did. `scripts/utils/capacity_sweep.py` (1,821 lines) and
`tests/test_capacity_sweep.py` (1,561 lines, 189 tests) now exist and the full packet suite is
green at 1,740 tests. Nothing was run against the real data — no plan artifact, no fit, no
checkpoint, no rollout. The session's most useful hour was not the building: it was discovering
that my first attempt to *measure* how good the tests are was itself broken, and that the honest
measurement, once the instrument worked, found five real holes. Those are closed. The work is
handed to Codex for its own exact-state review, with six decisions named explicitly as its to rule
on rather than buried in the code.

---

## What this executable is, in plain terms

The project's learned attribution model has been fitted exactly once, at one size: 39,594
parameters. That first fit produced an awkward result — the richer sensor suite (S) fitted
*worse* than the leaner one (C1) at that fixed size. Both agents agreed early that this cannot be
read as evidence against the project's hypothesis, because S is C1 plus four extra input channels
at an identical parameter budget: a network can fit worse while the extra channels carry real
information, simply because it does not have the capacity to use them.

The measurement that follows from that is a **width sweep**: fit the same model at five sizes
(16, 24, 32, 40 and 48 channels), both suites, five seeds each, and look at how the S-minus-C1
difference moves with size. Fifty arms in total, of which the ten at 32 channels already exist and
are read rather than re-run — so forty new fits, plus two more that exist only to prove the new
code fits the same way the old code did. Forty-two fits, about six minutes of computation, zero
physical simulation.

The executable built this session is the program that will do that. **It has not been run.** The
project's sequencing puts four separate gates between a design and a spent measurement: freeze the
design, review the program, review the program's plan, and then authorize the run as its own joint
act. This session cleared the second of those four and handed it to Codex.

---

## What was accomplished

### 1. Read the frozen design end to end and built to it

I re-read all 1,084 lines of `Reproducibility Packet/protocol/capacity-escalation-v0.1.md` rather
than working from my own summary of it, and read the four approved modules the design says to
import from at source. The module implements every invariant the design numbers:

- **C1** — the ten existing arms are read from the approved ledger and analysis artifact, never
  re-fitted, and the program refuses a destination inside `results/dev_fit`.
- **C2** — the run root `<base>/<run_label>/` is claimed by one atomic create that requires the
  path to be absent, with refusals persisted in a sibling sink outside it.
- **C3** — the eight historical code-identity entries must match the approved ledger's exactly,
  entry by entry, with this module as the one permitted addition.
- **C4** — parameter count and receptive field are read off the constructed network and required
  to match the design's table.
- **C5** — the rung-1 band guard stays on, and there is no argument anywhere that can turn it off.
- **C6** — the constraint criterion's inputs are persisted per arm.
- **C8** — zero rollouts, generation and non-dev reads asserted and recorded on every exit.
- **C9** — the equivalence gate: two 32-channel arms fitted through the new code path and required
  to be bit-identical to the approved checkpoints and loss histories.
- **C10** — no partial run may present itself as a curve.

### 2. Measured the things a review would otherwise have to take on faith

- **The new code path really is the approved network at 32 channels.** Constructing the network
  through this module's one construction site produces a bit-identical parameter set to the
  approved constructor at both equivalence seeds, 39,594 parameters each. Without that, the
  equivalence gate would be comparing two different things and a pass would mean nothing.
- **The approved anchor is still comparable.** All eight historical code-identity digests still
  match the current files, and the recorded training protocol matches the constants this module
  will run under. Checked against the real ledger, not a fixture.
- **The capacity table is correct by construction.** Building each of the five networks reproduces
  the design's published parameter counts exactly — 10,586 / 22,786 / 39,594 / 61,010 / 87,034 —
  with the receptive field held at 1,023 samples at every point, which is the property that keeps
  the sweep a capacity sweep rather than a "how much of the window can it see" sweep.
- **The design's own stated anchor measurement.** The test recomputes the per-seed headroom at
  rung 1 from the approved artifact's published numbers (0.3157 to 0.5133) rather than quoting the
  design's figure, and confirms the anchor point is not arithmetically constrained.

### 3. Measured what the tests actually catch — badly at first, and that is the story

The way this project checks whether a test suite is any good is to break the code on purpose, one
small edit at a time, and count how often the tests notice. I ran 36 such edits — the atomic
directory claim silently becoming a reuse, the size guard turned off, a `min` becoming a `max` in
the arithmetic bound, exact weight comparison becoming approximate, the authorization gate
skipping its check, and so on — and got back **36 caught, 0 survivors.**

That number was false, and I should have been suspicious of it precisely because it was perfect.

The project's own written rules for running this kind of sweep require, among other things, a
*negative control*: an edit that changes nothing real, which the tests **must not** notice. If the
harness reports that one as "caught", the harness is broken. I had skipped that rule, along with
three others. When I went back and added the controls, all three of them came back "caught" —
impossible if the instrument works.

The cause: I had run each test in a stripped-down environment, and two of the tests reach deep
enough into PyTorch that a stripped environment makes them fail on their own, regardless of what I
had edited. So every single case failed, and every single case scored as "caught". **The harness
was incapable of ever saying "survived."**

### 4. The corrected measurement found five real holes, and they are closed

Rebuilt properly — real environment, a green baseline asserted before anything is touched,
negative controls in the case list, two independent passes required to agree — the honest first
answer was **31 caught out of 36**. The five survivors were real:

1. A check that no two model sizes report the same parameter count could be deleted with nothing
   going red, because my test asserted the *property of the real grid* rather than the *behaviour
   of the check*. That is a test of the world, not of the code. Fixed in the module, by making the
   check its own routine that a test can drive directly. **This is the session's one module
   change.**
2. A rule reading "all five seeds are constrained" could be weakened to "at least four" and
   survive, because no case in my table had exactly four. That weakening silently discards a
   seed's worth of real evidence.
3. A shape check inside the bit-identity comparison could be deleted, because a shape mismatch
   also fails the next comparison down and my test only checked the verdict, not the reason.
4. The comparison that has to be *bit*-exact could be loosened to a tolerance and survive, because
   my test fixture differed by far more than that tolerance. Bit-identity has to be tested at bit
   scale.
5. The "create this file exclusively, never overwrite" rule could be changed to a plain overwrite
   and survive, because with unique filenames the two behave identically. It only matters on a
   name collision, so the test now forces one.

**Four of the five were defects in my tests and one in the module, and all five are the same
shape: the test watched the outcome the guard produces on good input instead of driving the guard
itself.** After the repairs: 36 of 36 caught, controls still surviving, both passes agreeing. Both
handed-over files therefore moved, and I appended a correction to the transcript withdrawing the
false number and naming the new state, rather than quietly editing over it.

### 5. One more real defect, in a test rather than in the module

With the destination guard weakened to an exact-equality check, the run wrote a refusal document
into `results/dev_fit/sweep/` before the test that guards it went red, and that debris outlived
the sweep that produced it. The test now cleans up after itself. The shape is worth carrying:
*a test whose subject is a protected directory pollutes the thing it protects when the guard is
broken* — which is exactly the moment the pollution is hardest to notice.

---

## Decisions I made, and why

**1. One terminal exit deliberately writes no artifact, and I said so out loud.** The design
requires every terminal exit to persist a document. It also forbids writing into the approved
checkpoint directory. Those two rules collide on exactly one input: an operator pointing the
program's destination at that directory. Every place the program could write its refusal is
*under* the destination, so persisting it would itself be the forbidden write. I resolved it in
favour of the prohibition, named the exit, documented it in the module, and drove it with a test
that proves the protected directory gained nothing. Codex may rule the other way; the point is
that the conflict is on the record rather than resolved silently.

**2. The read's classification functions live in the executable but are never called by it.** The
criterion that decides which points of the curve are readable is a pure function of numbers the
program persists. I put it in this module so the not-yet-built analysis script imports it rather
than writing a second definition of the quantity the entire measurement turns on. Two definitions
of one criterion is how two guards drift apart.

**3. I did not build the analysis script.** Codex's authorization named the executable and its
tests. The analysis reads an artifact that execution produces, and execution is two gates away.
Building it now would mean reviewing it against a document that does not exist yet. It is the next
separate piece of work, and I have said so rather than quietly leaving it undone.

**4. The module now pins the frozen design's digest, which retires something I reported last
session.** In Session 91 I measured that no test pinned the design document, so editing it forced
no regeneration. That is deliberately no longer true. The program checks the design file against
its frozen digest and refuses on a mismatch. The version discipline — an approved document is
bumped and moved, never edited in place — is now enforced by the code rather than by memory.

**5. The optimization settings are constants, not command-line flags.** This is stricter than the
approved trainer, which accepts epochs, batch size, learning rate and device on the command line.
The design holds all four exactly fixed and lets width and nothing else vary; a flag would move
that decision to the moment of invocation. The constants are then checked against the approved
ledger's recorded protocol, so the check has two independent sides.

**6. I did not run plan mode.** Codex's authorization excluded it and the sequencing makes it a
separate step. The tests exercise the plan-mode code paths into temporary directories only —
the same precedent the trainer's tests set when they drove every trainer exit before any fit was
authorized. No plan artifact exists anywhere in the packet.

---

## Challenges, and how they were handled

- **The executable's write locations were the hardest part of the design and the easiest place to
  get wrong.** Three sessions of review argued about where this program is allowed to write.
  Implementing it surfaced the conflict described in decision 1, which no round of the design
  review had reached, because it only appears when a real program has to choose a directory for a
  refusal before it knows whether it is allowed to write there at all.
- **My first measurement of the tests was itself unmeasured.** This is the one I would most want
  a reader to notice, because it is the failure mode this project keeps finding in itself: the
  instrument that checks the work is a piece of work too, and it gets no free pass. A perfect
  score should have read as a warning rather than as a result. The rules that catch it were
  already written down in my own notes from an earlier session; I did not apply them until the
  answer looked too good.
- **My mutation harness silently rewrote the module's line endings.** Restoring the file through
  Python's default text write converted every line ending on Windows. The content was unchanged
  and the module's own identity digest is line-ending-immune by design, so nothing downstream
  moved, but I normalized the file back and re-verified rather than leaving a file whose raw bytes
  disagreed with its neighbours.
- **I put a wrong timestamp on my chat message.** The header reads 16:44 while the actual write was
  at 16:31 — I estimated while drafting instead of reading the clock before posting, which is the
  procedure the project specifies. Nothing technical depends on it, but a *forward* timestamp is
  the one error that can make a physically later message look earlier, so I appended a dated
  correction to the transcript rather than editing the header. Recorded here too.

---

## Files created or updated

**Created:**

- `Reproducibility Packet/scripts/utils/capacity_sweep.py` — the Route-A executable
  (blob `9f2cc0ab`, canonical/raw SHA-256 `e89cc791…`, 77,231 B / 1,821 lines, LF)
- `Reproducibility Packet/tests/test_capacity_sweep.py` — 189 tests
  (blob `d8a8c86c`, canonical/raw SHA-256 `09defd75…`, 63,255 B / 1,561 lines, LF)
- `agents/Claude/Session Summaries/HumanReport92.md` — this report

**Updated:**

- `chats/Claude-Codex/Phase 2 Integration and Config Freeze/Phase 2 Integration and Config Freeze - Active.md`
  — three appended turns (+255 / −0): the handover, a timestamp correction, and the correction
  withdrawing the false mutation number and naming the corrected state
- `agents/Claude/README.md`
- `agents/Claude/Summary of Only Necessary Context.md`

**Reviewed and deliberately unchanged:**

- `Reproducibility Packet/protocol/capacity-escalation-v0.1.md` — frozen; the module verifies it
- `scripts/utils/dev_fit_trainer.py`, `dev_fit_contract.py`, `attribution_net.py`,
  `scripts/analyze_dev_fit.py` — read at source, imported from, not edited
- every result JSON, every checkpoint, both READMEs, `.gitignore`
- the root Live-Run README: this session closed no artifact loop, so the log stays lean. Codex
  logged the design freeze in its own Session 91.

`.gitignore` needed no change: the sweep's future checkpoints are `.pt` files, which it already
excludes, and the mutation harness lived outside the repository.

---

## Verification

```text
full packet suite    1,740 passed in 121.17 s   (1,551 before + 189 new)
new-file suite       189 passed in 3.39 s
mutation sweep       FIRST HARNESS INVALID (see above). Corrected harness, two agreeing
                     passes, 3/3 negative controls surviving: 31/36 before repairs,
                     36/36 after.
git diff --check     clean
chat append          +255 / −0 over three turns; five gates passed on each (prior digest
                     asserted inside the writer, byte-identical prefix, unique header,
                     pure ASCII, Claude physically last)
FITS 0 | CHECKPOINTS 0 | PLAN ARTIFACTS 0 | GENERATION 0 | ROLLOUTS 0
REAL-DATA TOUCHES    zero of every kind. The only tracked results files read were
                     dev_fit_result.json and dev_fit_analysis.json.  PILOT/VAL/TEST: 0.
```

---

## Cross-review

I read Codex's `HumanReport91.md` in full and its Session-91 turn in the Phase-2 transcript. Its
account is accurate against the objects I checked independently: the design file is at the state
it names, its digest is the one it published, and the two claims it made about the approved
trainer — that the fitting loop has one fixed-width construction site, and that the existing
output guard is a staleness check rather than an atomic claim — are both true at source, which I
had verified separately in Session 91. I found nothing to correct and had no reason to open a
review cycle on it. Its judgment not to rewrite the frozen document's status line after approval
is right: the chat and git history are the approval record, and another byte state would have
created another review obligation for no gain.

---

## Next steps

1. **Codex reviews the two exact states above.** That is the only open loop.
2. If it approves them, the next act is **plan mode** — zero fits — and a review of the plan
   artifact it produces. Separate.
3. Only after that may the forty-two fits be authorized, as a fourth and separate joint act.
4. The read-only analysis script the design requires is the next separate build after the
   executable's loop closes.
5. Still blocked, and not moved by anything this session: pilot, validation and test reads;
   thresholds; capacity selection; Stage 2; the final frozen config; generation; and all rollouts.
