# Claude — Human Report, Session 91

**Date and time:** 2026-08-07 12:16 PDT

**Phase:** Phase 2 — Execution

**Physical rollouts spent this session:** 0. Project lifetime Protocol-P-related total remains **278**.

**Fits: 0. Checkpoint writes: 0. Data generated: 0. Pilot / validation / test reads: 0.**

**Real-data touches of any kind: zero.** No manifest, no `.npz`, no checkpoint payload, no
regeneration, and this session not even a read of a tracked results file. The only reads were
source files and one design document.

**Progress-report session:** no. My next regular progress report is Session 96; no phase
transition and no approved Claim-Sheet amendment occurred this session.

---

## Summary

This was a single-purpose session: the owner's same-state re-review of the capacity-escalation
design after Codex edited and approved it in its Session 90. It is round five on that document.
I kept Codex's correction whole, found one defect below it, repaired it, and handed the document
back at my own explicitly approved state.

The document still authorizes nothing. It is a design for a forty-two-fit measurement that
cannot be un-spent, and the whole point of reviewing it before the executable exists is that a
defect found in prose costs a session and a defect found after execution costs the measurement.

### What the document is for, in one paragraph

The project's first learned-model result (Session 84) compared two sensor suites at a single
network width, and the structural suite fit slightly *worse*. That could mean the structural
signal is genuinely weaker, or it could mean the fixed width was the binding constraint rather
than the information. The capacity-escalation design is the plan for telling those apart: fit
the same arms at four widths instead of one and look at the shape of the curve. Forty new fits,
plus two "equivalence" fits whose only job is to prove the new code reproduces the old code's
numbers bit-for-bit before anyone trusts its other outputs.

## What Codex found, and why I accepted it

My Session-90 repair had bound the run's output directory to a name the plan carries, so that
two runs under one destination could not quietly write two unrelated sets of results. Codex's
Session-90 review found that the *guard* I wrote for it was too weak in three ways: it refused
only a directory that already existed **and** had files in it, which lets an empty leftover
directory be silently reused; a check followed by a separate create lets two simultaneous
invocations both pass before either writes; and a pre-existing *file* at that path was not
covered at all. It also found that the design required every refusal to be recorded while
naming nowhere the "this directory is occupied" refusal could legally be written — the
document's own rule forbids a refusal from reporting through the resource whose occupancy
caused it.

Codex's repair: claim the directory with one atomic create that requires the path to be absent,
and persist that particular refusal in a sibling folder alongside the run rather than inside it.

I accepted both halves unedited, and I checked them against objects outside the document rather
than against the document's own argument — the discipline that has caught the last three
rounds' defects:

- **The cited precedent, read at source.** The design leans on the trainer's existing
  "don't write into a dirty directory" function as its precedent. I re-read that function. It
  is a *name-based staleness check followed by later writes*, and its own documentation says
  it deliberately permits plan files to remain so an operator can plan and fit in one place. It
  cannot carry an atomicity claim. Codex is right.
- **The two reserved folder names, checked against the name space they sit in.** Codex's
  refusal sink uses two reserved names beginning with an underscore. A reserved name that a
  legal run name could collide with is a hole, not a namespace. The run-name pattern admits no
  underscore anywhere, so no conforming run can ever produce either reserved name. Safe by
  construction. **That check came back clean and I recorded it so it is not run again.**

**This is the fourth consecutive session in which I went looking for something to push back on
in Codex's work and did not find it.**

## The defect I found: the write location the repair did not reach

The design names three places the program writes during execution. After Codex's repair, two of
them are pinned down: the run's own directory, and the sibling folder for refusals. The third —
the scratch space where those two "equivalence" fits write — is described three times in the
document and located none of them. The only thing ever said about it is where it is *not*.

That matters because two sentences written during this very review loop depend on the unstated
answer:

1. **"The failed run is preserved as evidence and never deleted to make room for a retry."**
   A retry re-runs the equivalence fits. If their scratch space is not inside the run's own
   directory, a retry either overwrites the failed run's equivalence checkpoints and its
   equivalence record — the exact evidence a diagnosis would rest on — or, if the dirty-directory
   guard reaches that space, the retry is *blocked* by leftovers from the run it is retrying,
   and the only way forward is to delete that same evidence. Both outcomes contradict the
   sentence.
2. **"The directory is claimed before any other write."** That is only an exhaustive statement
   if every write is inside the claim. Two of the forty-two budgeted checkpoints were not.

The repair is small and costs nothing: make the equivalence fits write into a reserved
sub-folder of the run's own directory. The directory is created fresh and is provably empty at
the moment those fits run, no machine-specific path enters the plan, and the plan's
byte-for-byte determinism is untouched. It buys four things — the "claimed before any other
write" guarantee becomes true of every write; a new run name gives a fresh scratch space for
free, so the retry rule covers the equivalence fits without a second thing for an operator to
remember; the failed run's equivalence evidence is preserved by the same mechanism that
preserves everything else; and the rule that these checkpoints are "not part of any curve"
becomes a reserved folder name rather than a convention someone has to honor.

## Two things I checked and deliberately did not raise

Recorded here and in the document so a later session does not re-derive them as findings.

- The per-capacity-point dirty-directory guard is now unreachable on the ordinary path, because
  the run directory is created absent and owned. That is defence in depth, not a contradiction.
  A guard that cannot fire is still correct.
- Planning into the run's own directory would now be refused by execution, which diverges from
  the trainer's explicit "plan and fit in one directory" allowance. The divergence is deliberate
  here, and its failure mode is a loud refusal rather than a silent one. A usage note, not a
  defect.

## Challenges, and the judgment call

**The real challenge this session was deciding whether to return the document at all.** The
heuristic I have carried since Session 71 is that a review round finding only wording is the
signal to close a loop, not to hunt for one more finding. This is round five on a document that
authorizes nothing, and each round costs a session.

I returned it because the finding is not wording: a budgeted artifact with no bound location,
and a preservation claim resting on it, is executable. But I also wrote into both the document
and the chat that the finding is the same *shape* as the previous two rounds' findings, which I
read as the sign that this seam is now fully walked rather than the sign that there is more
beneath it — and that if the next round finds only wording, that is the signal to close
regardless. I would rather name the closing condition in advance than discover it after another
two rounds.

The honest counterweight, and the reason five rounds are not obviously wrong here: what is being
designed is a forty-two-fit spend that cannot be un-spent, and every round so far has found
something real.

## Insight worth carrying

**A repair that binds one resource should be checked against the *set* of resources of that
kind, not against the one that was broken.** Codex's repair was correct and complete for the
run directory. My own Session-90 repair was correct and complete for the run directory. Neither
of us asked how many directories this program writes into. The answer was three, and the third
had been sitting in the document unbound since Session 87, mentioned in three separate sections,
invisible because each mention said only what it was *not*. The general form: **when you pin
down a thing, count the things of that kind before you call it pinned.**

## Files created or updated

Updated:

- `Reproducibility Packet/protocol/capacity-escalation-v0.1.md` — owner-edited state, Git blob
  `b45efa477de10331ca61e1af73b2834b22df3fb6`, canonical/raw SHA-256
  `05109d973f1611756456a01aea8a0aebf7c33ec73e5243225f1f733e3c15e002`, 72,630 B / 1,084 lines /
  LF / no BOM, owner delta +86 / -15.
- `chats/Claude-Codex/Phase 2 Integration and Config Freeze/Phase 2 Integration and Config Freeze - Active.md`
  — one append, +132 / -0, header unique at line 24,826.
- `agents/Claude/README.md`
- `agents/Claude/Summary of Only Necessary Context.md`

Created:

- `agents/Claude/Session Summaries/HumanReport91.md`

Deliberately unchanged: every executable, test, result JSON, checkpoint and config artifact;
the root `README.md`; and the Transcript Order Monitoring chat.

## Verification

```text
full packet suite       1,551 passed in 116.98 s (also run pre-edit: 1,551 in 116.72 s)
git diff --check        clean
design digest pinning   none -- "capacity-escalation" / "capacity_sweep" appear nowhere
                        under tests/ or scripts/, so no artifact regeneration is implied
transcript append       pre-write 1,556,240 B / 24,824 lines / sha 194ebb26...;
                        post-write 1,564,456 B / 24,956 lines / sha b7a229df...;
                        prefix byte-identical, asserted inside the writer; +132/-0;
                        turn asserted PURE ASCII before writing; Claude physically last
Codex S90 append        clean, additions only, physically last before this turn --
                        no monitoring note required
FITS 0 | CHECKPOINTS 0 | GENERATION 0 | ROLLOUTS 0 | LIFETIME TOTAL 278
```

## Cross-review

I read Codex's `HumanReport90.md` and its Session-90 chat turn, and re-derived its reported
figures rather than accepting them: the returned blob, the 66,744 B / 1,013-line physical state,
the +84 / -35 delta and the 1,551-test suite all reproduce exactly. Its account of the three
holes in my Session-90 guard is accurate, including the pre-existing-*file* case I had not
considered. No correction to carry forward, so no separate review cycle opened on the report.

## Next steps

1. **Codex genuinely reopens and either approves design blob `b45efa4...` or returns another
   edited state.** This is the only open loop.
2. If it approves unchanged, v0.1 freezes and the **only** thing authorized is writing the
   Route-A executable (`scripts/utils/capacity_sweep.py`) and its tests.
3. That executable then gets its own exact-state review. Then plan mode's zero-fit artifact gets
   a third, separate review. Then execution is a fourth and separate joint authorization.
   **Four gates, not one.**
4. Everything else remains blocked: pilot, validation and test reads; thresholds; Stage 2; the
   final `config/config.json` freeze; generation; and all rollouts.

— Claude
