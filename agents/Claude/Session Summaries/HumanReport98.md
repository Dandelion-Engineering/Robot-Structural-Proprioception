# Claude — Human Report, Session 98

**Date and time:** 2026-08-08 16:40 PDT

**Phase:** Phase 2 — Execution

**Physical rollouts spent this session:** 0. Project lifetime Protocol-P-related total remains **278**.

**Fits against the delivered dataset: 3** (two C9 equivalence fits and one curve arm) — the first
fits spent since Session 84. **Checkpoint writes: 3. Data generated: 0. Pilot / validation / test
reads: 0.**

**Progress-report session:** no. My next regular report is Session 104 unless a phase transition or
an approved Claim Sheet amendment fires sooner.

---

## Summary

This session did the thing the last thirteen were building toward, and it failed — usefully, and in
a way the structure was built to survive.

Codex had issued its half of the Step-4 execution authorization at the end of its Session 97. I ran
my own independent pre-spend checks (62 of them, plus the full 1,765-test packet suite), issued my
matching half, re-checked everything immediately before the command, and ran the single authorized
execution of the Stage-1 capacity sweep. It terminated after **31.3 seconds** on the **second curve
arm**, having spent 3 of its 42 authorized fits.

The cause is a real defect in the executable, now called **Finding AU**: the guard that checks a
capacity-point output directory for leftovers from an earlier attempt was being called **once per
arm** against a directory that **ten arms share**. The first arm at a given width wrote its
checkpoint; the second arm at the same width found that file and refused, treating the run's own
output as contamination from a previous attempt. **The executable could never have completed a
sweep** — not under any plan, any label, or any destination. Running it was the only way to find
that out.

Two things survived the failure and both are worth more than they look. First, the **C9 equivalence
gate passed** — the new width-parameterized program reproduces two of the ten previously trained
models **byte for byte**, through a complete training run rather than merely at construction. That
is the assumption the entire sweep design rests on, and until 16:16 today it was an assumption.
Second, a whole-project fingerprint taken before and after the run shows **zero changes outside the
run's own folder** — no earlier result, no approved checkpoint, no reserved data.

I repaired the defect, added three tests, verified by mutation that they catch it, and handed the
repaired state to Codex for review. The repair changes the program, which voids the approved plan
and both authorization halves that named it, so the sequence restarts: review the fix, regenerate
the plan at a new run label, both agents approve it, both agents authorize again.

---

## What was accomplished

### 1. The pre-spend checks, run before deciding rather than in exchange for deciding

The project's lesson (oo) says that when a check sits *below* an irreversible spend inside the same
routine, it must be run *before* the authorization rather than treated as covered by it. I built a
two-part probe:

- **Part A (48 checks) imports nothing from the module under test.** The frozen design's digest, the
  approved plan's byte state and canonical-JSON conformance, the clean git tree, the approved blobs,
  the absent run root and refusal sink, the count and location of every `.pt` file in the packet, a
  **three-way** anchor-digest agreement (plan == approved ledger == approved analysis == the raw
  bytes on disk), the plan's bindings to both approved development documents, the budget arithmetic,
  the exact composition of the forty new arms, all 44 declared output destinations, and the delivered
  data's manifest and role-index digests.
- **Part B (14 checks) drives the module's own pre-spend checks in the order execute mode calls
  them**, stopping at the last statement before the first fit. Including a negative control: one
  flipped hex character in the plan digest must be refused, because a gate that accepted everything
  would pass an exact-bytes check identically.

All 62 passed. The full packet suite passed at 1,765 tests, matching Codex's independent count.

### 2. The bracket this design does not have

The earlier payload-boundary extension wrapped its irreversible spend in a whole-tree "nothing else
changed" invariant. I checked whether the capacity-sweep design has an equivalent and **it does
not** — the words do not appear anywhere in the design or the module. So rather than report what a
watch list misses, the honest statement was that *nothing outside the claimed run root is measured
by this executable at all*, and the design substitutes a structural argument about where the code
writes.

I also read the relevant guard at source instead of trusting the design's prose, and found it
**narrower than the prose suggests**: it refuses a destination only at or inside the approved
checkpoint directory. Every other location on the machine is permitted. That is not a defect — but
it means "every write lands under the claimed root" is only as strong as the destination named in
the authorization, so my authorization names it explicitly.

Then I supplied the missing bracket from outside the executable: a two-domain whole-project
fingerprint. 476 files hashed; the 3.86 GB delivered data root stat-ed only (2,997 files), with the
limitation of that second domain stated rather than hidden.

### 3. My Step-4 authorization half

Issued as its own turn, not folded into a review — plan correctness and permission to spend 42 fits
are separate gates, and bundling them converts a review into a spend. It names the plan digest, the
run label, the destination, the executable blob, the maximum budget, and — explicitly — the long
list of things it does *not* authorize. It also named the four residuals no local mechanism closes,
including a concurrent writer, which I measured rather than assumed.

That measurement is worth recording: my first pass reported a concurrent writer and **stopped the
session**. It turned out to be your *Dandelion Station* test suite running in a sibling directory
and system temp, plus — on the next pass — my own probe, because on Windows the venv's `python.exe`
is a launcher that re-executes the base interpreter, so one invocation appears as two processes and
excluding by process id alone leaves the launcher behind. The check was wrong twice before it was
right, and it is better that it failed loudly than that it passed by accident.

### 4. The run

```text
started 16:15:53, ended 16:16:26      exit X_OUTPUT_DIRTY (code 6)
fits 3 of 42 authorized               checkpoints 3 of 42
rollouts 0, generation 0, non-development reads 0
curve arms: 10 REUSED, 1 COMPLETED, 39 UNATTEMPTED
```

The one completed arm — 16 channels, C1, seed 0, in-sample macro-F1 0.463789 — licenses nothing.
The partial-failure contract behaved exactly as designed: the artifact carries the **complete**
50-arm identity set with honest per-arm statuses, so a refusal does not make the unattempted arms
disappear, and the C10 backstop makes it impossible to present one arm as a curve.

### 5. C9 passed — the session's one positive measurement

```text
C1 seed 0   produced 6403e894...  ==  approved 6403e894...   PASS
S  seed 4   produced eb9dbb0c...  ==  approved eb9dbb0c...   PASS
```

Session 90 measured that the width-parameterized constructor reproduces the approved network at 32
channels. What this run adds is the **whole fit path** — the copied training loop, the loss, the
batcher, the precision context, the serializer — reproducing the approved checkpoint **byte for
byte** on real development rows, for both sensor suites and two seeds. That is the justification
for treating the ten existing models and the forty new ones as points on one curve.

### 6. Finding AU, its repair, and the check that the repair is real

The repair moves the guard out of the per-arm loop: it now runs **once per capacity point**, and
**above** the equivalence gate rather than below it, so an output-cleanliness refusal cannot cost
two equivalence fits. I flagged the second property to Codex as a judgment rather than a correctness
fix, and asked for a ruling on it specifically.

Three tests were added (217 in that file, 1,768 in the packet), and then checked by mutation:

```text
M1  the guard back inside the arm loop (the exact defect)   CAUGHT (3 of 3 fail)
M2  once per point but below the equivalence gate           CAUGHT (1 of 3 fails)
M3  comment only (negative control)                         SURVIVED
```

Run twice with identical verdicts; the module's exact bytes restored and digest-verified after each
pass. M2 matters: the two halves of the repair fail independently, so approving one does not
silently approve the other.

I also kept an existing approved test intact rather than weakening it to fit the repair — it pins a
specific variable binding, so the repair keeps that binding.

---

## Challenges, and how they were handled

**The concurrent-writer check failed twice before it was right.** Described above. The rule I took
from it: a precondition check should test the thing it is actually about (does any process name
*this project*), not a proxy that happens to correlate (is anything else running).

**The first preflight reported five failures that were my own probe's wrong guesses at field
names** — I had assumed key names in the plan document instead of reading them. I re-derived them
from the document's own structure and re-ran; all passed. Worth noting because it is the same class
of error the project keeps meeting: a check whose expected value came from memory rather than from
the object.

**The repair invalidates an approved artifact, and that is the correct cost.** Editing the program
moves its fingerprint, which is bound into the plan. I drove the gate rather than asserting the
consequence: the old plan is now refused with *"the authorized plan was written by a different code
state."* Both authorization halves are spent with it. The conforming path is a new run label, a new
plan, a new digest and a new joint act.

**The failed run's folder is preserved, not cleaned up.** The design is explicit that it is the
evidence the diagnosis rests on. Its two JSON artifacts are committed; its three model files are
untracked under the packet's existing rules, which is the same portability question Codex ruled on
this morning, now with three more files in it.

---

## Important decisions

1. **To run at all**, rather than authorize and leave the execution for a later session. The project
   had gone thirteen sessions without a new number, cost was explicitly not the constraint, and both
   halves existed. In hindsight this is clearly right: a later session would have hit the same wall
   with the same three fits.
2. **To repair the defect myself rather than hand the diagnosis over.** I built the module; a repair
   with a test that would have caught the defect is the normal shape, and Codex reviews it.
3. **To place the guard above the equivalence gate**, and to flag that as a separable judgment with
   its own mutation case rather than bundling it into the correctness fix.
4. **To narrow the concurrent-writer check rather than wait out your test suite.** The bracket
   covers what the process listing cannot, and I said so instead of implying the listing was
   sufficient.
5. **Not to write the replacement plan this session.** It would bind an executable that has not been
   reviewed.

---

## Insights

**A claim of unreachability is a claim, and it needs a test like any other.** The guard's docstring
said it could not fire on the ordinary path. It fired on the second arm of the only run there has
ever been. The claim was true of the placement the design described and false of the placement the
code had, and nothing in five design rounds, four executable review rounds or 214 tests compared the
two. This is the project's recurring lesson at a new address: *the dangerous statement is the one
everyone agrees with and nobody drives.*

**Some defects are only reachable by spending.** Every static instrument this project has built —
review rounds, mutation sweeps, AST tests, gate-neighbour sweeps, independent audits — missed this
one, because all of them examine the program and none of them ran forty arms. The three fits were
not waste; they were the measurement.

**The partial-failure machinery earned its cost today.** Codex's Finding AJ (complete arm identity
sets so a refusal cannot make arms disappear), invariant C10, the atomic run-root claim, the
preserved-evidence rule — all of that was argued over for sessions and looked like ceremony. Today a
run failed at arm two and left behind a complete, honest, self-describing record, with nothing
corrupted and nothing ambiguous about what was and was not spent.

---

## Files created or updated

Created:

- `agents/Claude/Session Summaries/HumanReport98.md` — this report.
- `Reproducibility Packet/results/capacity_sweep/stage1-run-1/capacity_sweep_result.json` — the
  failed run's record. Preserved evidence; not to be deleted.
- `Reproducibility Packet/results/capacity_sweep/stage1-run-1/_equivalence/capacity_sweep_equivalence.json`
  — the C9 result, `gate_passed: true`.
- Three untracked model files under that run root (two equivalence, one curve arm).

Updated:

- `Reproducibility Packet/scripts/utils/capacity_sweep.py` — the Finding-AU repair (+31/−10), blob
  `53e5dcb7`, canonical `be07d95e...`. **Open on Codex for review.**
- `Reproducibility Packet/tests/test_capacity_sweep.py` — three tests (+197/−0), blob `2dc93297`,
  canonical `657ffd6b...`, 217 collected. **Open on Codex for review.**
- `chats/Claude-Codex/Phase 2 Integration and Config Freeze/…- Active.md` — three turns (+338/−0):
  the pre-spend measurements and residuals, my authorization half, and the execution record with
  Finding AU.
- `README.md` — one Live-Run log entry (+2/−0) recording the failed run honestly, in plain language.
- `agents/Claude/README.md`, `agents/Claude/Summary of Only Necessary Context.md` — navigation and
  resume state.

Reviewed and deliberately unchanged: the frozen design; the superseded plan artifact (kept, not
regenerated, as the visible state); the approved ledger and analysis; `director_requests.md` (nothing
this session needs you); `.gitignore` (correct as it stands — the run's model files are ignored, its
JSON records are tracked).

---

## Next steps

1. **Codex reviews the repaired executable and tests**, and rules specifically on whether the guard
   belongs above the equivalence gate or below it.
2. Once that loop closes, **a new plan is generated at run label `stage1-run-2`**, both agents
   approve it, and a **fresh Step-4 joint authorization** names its digest. The current plan and both
   authorization halves are spent.
3. Then the sweep runs again — 42 fits, zero rollouts.
4. Then both agents review the exact resulting state, and only then is the pre-registered
   interpretation applied.
5. The read-only analysis script is still unbuilt and is deliberately a separate step after that.
6. **Phase-3 obligation, unchanged and now larger:** the packet needs an authenticated way for a
   clean machine to obtain or reproduce the exact approved model files, or it cannot claim
   fresh-environment completion for this sweep. That was ten files this morning; a completed sweep
   makes it fifty-two.

— Claude
