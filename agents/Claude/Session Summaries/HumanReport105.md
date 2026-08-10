# Claude — Human Report, Session 105

**Date and time:** 2026-08-09 20:28 PDT

**Phase:** Phase 2 — Execution

**Progress-report session:** No. My next regular progress report is Session 112, unless a phase
transition or an approved written Claim-Sheet amendment fires one sooner.

---

## Summary

Session 104 ended with one thing outstanding: Codex owed the second half of the joint
application of the frozen interpretation table to the capacity-sweep result. It delivered that
half at 18:11 PDT, reading the row set exactly as I had. **That closes the last of the three
gates, and the Stage-1 capacity measurement is complete as scoped.** Nothing about the sweep,
its plan, its executable, its reader or its terminal artifact is open from either side.

That left this session with no review round to run — which is the right moment to do the work
that a review session must never be mixed with. I took the first of the three Phase-3 assembly
obligations both agents had recorded, and it was the one explicitly logged as mine: **the
Reproducibility Packet's runbook did not mention the capacity sweep at all.** Zero occurrences
of `capacity_sweep` in a 92 KB document whose entire job is telling a stranger how to reproduce
what the packet holds — while the sweep's plan, its terminal record and its analysis were all
sitting in the packet, tracked and committed.

I wrote the two steps that close that gap, re-measured every number in them rather than
carrying one forward, and disclosed — rather than papered over — the one part of the recovery
story the packet genuinely cannot promise.

**This session spent nothing.** No fit, no checkpoint, no simulator generation run, no physical
rollout, no invocation of the one-shot analyzer, no published plan artifact, and no read of any
pilot, validation or test row. It touched no packet source file, no test, no protocol, no plan,
no result and no checkpoint. The rollout count is unchanged at 278; the fit counter is unchanged
at 13.

## What was accomplished

### 1. Codex's half of the interpretation accepted; Stage 1 closed

Codex evaluated all six rows of the frozen table directly from the persisted artifact fields,
without calling the analyzer or importing either capacity-sweep implementation, and got the same
answer I did: rows 1, 2, 3, 4 and 6 false, row 5 true. The licensed reading is one sentence —
*the paired curve does not have a readable shape at five points and five seeds* — and any trend
statement is forbidden. I accepted it without qualification and added nothing to it.

The part worth the director's attention is the row that *nearly* matched. Row 4 would have
licensed "the difference did not move by more than the anchor's own seed spread" — the sentence
a person looking at these five numbers for the first time would reach for. It fails on both of
its conditions, independently: the curve's shape is non-monotone rather than flat-or-declining,
**and** the spread across the five points (0.156930) exceeds the 32-channel anchor's own
five-seed spread (0.149636). Either failure alone blocks it. The table was written in Session
88, before any of these fifty models existed. It blocked the comfortable reading twice over.

### 2. The packet runbook now covers the sweep — Steps 28 and 29

Appended before the Data section, **`+207 / -0`, additions only**:

**Step 28 — Audit or reproduce the Stage-1 capacity-sweep plan.** The frozen design and its
digest; why only width varies and depth does not (every arm keeps the same 1,023-step receptive
field, so a deeper network would be a different experiment); the parameter table across the five
widths; the plan-mode invocation, which a reader can run for free because it takes no data root
and runs no fit; the execute-mode invocation with the fresh-label rule; the recorded run's cost;
the 55-checkpoint census; and why a failed run and a superseded plan are deliberately preserved
in the tree rather than cleaned up.

**Step 29 — Read the completed sweep against its pre-registered interpretation.** The eight
required arguments (none has a default, and the result's own digest is supplied at the
invocation so the result and the plan cannot end up authenticating only each other); the
exclusive-create destination; the five per-point means as exact record contents; the row that
matched and the row that nearly did; and what the step does not do.

### 3. Every number in those steps was measured this session

The determinism claim is the one that is a measurement rather than a citation, so I re-drove it
rather than repeat a figure from Session 99: plan mode at run label `stage1-run-2`, three
independent destinations outside the repository, **one digest**, byte-identical to the tracked
live plan. I also drove the supporting claim instead of asserting it — the plan document
contains no backslash, no drive-letter path form, no `Users`, and none of its 413 leaf values is
time-shaped. That is what makes "byte-deterministic" a checkable statement rather than a boast.

### 4. The checkpoint gap is disclosed, not closed

Codex had named the second obligation: the 55 model files this project has produced are all
git-ignored, and the packet had no clean-machine recovery story for them. Step 28 now carries
the census by directory and the recovery path, but it states it as a **disclosed limitation**,
and the reasoning is the part that matters:

- The tracked JSON records are mutually bound by digest, so their consistency is checkable on
  any machine with no checkpoint present.
- Rebuilding the checkpoints is a **new run, not a restoration**. The honest bound is that the
  recorded run's two equivalence arms establish bitwise reproduction of the 32-channel network
  *on the recorded machine*; that is not a cross-machine claim and I did not let it become one.
- Therefore **Step 29 cannot be re-driven against the tracked analysis on a machine that lacks
  those checkpoints**, because the reader reloads and re-scores all fifty from disk and
  authenticates each by digest.

I could have written a paragraph that reads like a recovery procedure. The third point is why I
did not: a rebuilt checkpoint that differs by one byte does not reproduce this analysis, it
produces a different one. A runbook implying otherwise would be wrong in the direction that
actually costs a reader their afternoon.

### 5. The boundary-block obligation discharged where it can be

The third recorded obligation was subtle and worth stating plainly, because it is the kind of
thing that quietly becomes a false claim in a written report. Every analysis document in this
project carries a small block reporting how much the run spent: fits, generation runs, rollouts,
restricted-data reads. In the capacity analysis all four read zero — **and that is true of the
program that did the reading, not of the sweep it read.** The sweep spent 42 fits and wrote 42
checkpoints. Step 29 now says exactly that, states it as a general rule covering Step 27's block
as well, and points the reader at the producing run's own record for the producing run's cost.

### 6. `.gitignore` corrected

The runbook instructs a reader to create three reproduction output directories. Two of them have
been in the runbook since Session 84 with no ignore rule; the third is new this session. All
three are now ignored, all three verified matching, and no tracked file is affected —
`git ls-files` returns zero under all of them.

## Challenges, and how they were handled

**A stale fact in my own continuity notes, caught by measuring.** My carried notes said the
public README's log tail is bare-LF while the file overall is mixed, with an instruction to
anchor carefully because of it. I measured before writing anything: the file is now **200 CRLF
pairs and zero bare LF** — it has been renormalised since that note was written. Nothing was
harmed, because the measurement came first, but it is a clean example of why the standing rule
in this project is to measure the thing rather than recall it.

**A shell that ate a document.** My first attempt to write the new runbook steps went through a
shell heredoc and was mangled before it reached disk. This is the same failure family I have
recorded twice before — building text inside a shell command instead of writing it to a file.
I abandoned the shell path immediately rather than fighting it, wrote the block with a file
writer, and did every subsequent edit through a small Python script that asserts its anchor is
unique *before* writing and re-asserts the prefix, the suffix and the byte accounting
afterwards. Every edit this session came out `+N / -0`.

**A rebuilt tool that had to be rebuilt correctly.** The chat writer that enforces the
transcript's append gates lives in session scratch and does not survive a session. Last session
I rebuilt it from my notes and it came back *weaker* than what it replaced, because the notes
described an older five-gate version. That improvement had since been moved into the block that
owns the lesson, so this time the rebuild came back at full strength: seven gates, with the
timestamp **built from the clock inside the writer at the moment of the write** rather than
parsed from an argument, which makes a false timestamp unconstructible rather than merely
refused. Declared 20:25, written 20:25:10. All seven gates passed, plus a character-domain check
that lists every non-ASCII code point in the turn and refuses anything outside a declared
whitelist.

## Decisions I made

1. **Do the packet work now, because no review is open.** A packet edit mixed into a review
   session is how a review stops being one. With Stage 1 closed and nothing contested, this was
   the correct session for it.
2. **Disclose the checkpoint limitation rather than write a recovery procedure that cannot be
   honoured.** Reasoning stated in full in the chat so Codex can overrule the *reasoning*, not
   just the wording.
3. **Add no entry to the public Live-Run README, and do not advance its banner date.** The
   result was already published there in the 2026-08-09 entry I wrote last session. Codex
   agreeing with a reading already on the log is a process fact, and the packet is not a
   finished artifact. Neither clears the playbook's three triggers. I re-read the playbook
   rather than reasoning from memory.
4. **Record, rather than repair, a missed obligation.** My own notes said the log entry
   reporting the sweep's result owed readers the story of the reader's own near-miss defect —
   that as first written it could not have read the finished sweep at all, because ten of its
   fifty models were described in numbers rounded by a different program, and that this was
   settled by arithmetic on already-published values before any measurement was touched. I
   wrote that entry last session and it does not tell that story; I verified the public log has
   no occurrence of it. Dated entries are never edited, so the obligation propagates forward to
   the Technical Report and, if it earns a place, the Accessible Piece. It is written down in
   both the chat and my continuity notes so it cannot be lost between the note that created it
   and the artifact that should carry it.

## Verification

```text
capacity executable + analyzer suites          241 passed
full packet suite                            1,792 passed
plan-mode reproduction, 3 destinations         1 digest, byte-identical to the tracked plan
working tree at session start                  clean
chat append                                    7/7 gates, +125/-0, single tail hunk
Codex Session 104 transcript append            +52/-0, single tail hunk, no order recurrence
```

## Files created or updated

- `Reproducibility Packet/README.md` — Steps 28 and 29 plus a Current-boundary paragraph,
  `+207/-0`. New state: 104,852 B, canonical SHA-256
  `21c2e7fead4e7418907b20c9d95c534e791bcdec14fa7b7fbb6e63b56d76d1ce`.
- `.gitignore` — three reproduction-output directories, `+6/-0`.
- `chats/Claude-Codex/Phase 2 Integration and Config Freeze/Phase 2 Integration and Config Freeze - Active.md`
  — one appended turn, `+125/-0`.
- `agents/Claude/README.md` — the packet runbook added to the co-owned list, `+1/-0`.
- `agents/Claude/Session Summaries/HumanReport105.md` — this report.
- `agents/Claude/Summary of Only Necessary Context.md` — rewritten.

Not touched: any packet script, test, protocol, plan, result or checkpoint; the root Live-Run
README; the Claim Sheet; `director_requests.md`; the transcript-order monitoring chat (verified
clean at the git level, so the duty to flag a recurrence did not fire).

## Next steps

1. **Codex may review the two new runbook steps when convenient.** They are documentation, not
   a gate, so nothing waits on them — but the packet's public runbook is worth disagreeing about
   now rather than at Phase-3 assembly. The two specific questions I put to it: whether the
   cross-machine reproduction claim should be stronger than I allowed, and whether Step 29
   should print the five per-point means at all.
2. **The remaining Phase-3 assembly obligation is the checkpoint recovery path**, which is
   currently disclosed rather than closed and will need a decision at assembly time.
3. **Stage 2 does not exist and must not be inferred from an unreadable curve.** A wider ladder,
   a larger seed count or an architecture change is a separate design with its own review and
   its own authorization.
4. Final `config.json`, threshold selection, capacity selection, later-role reads, confirmatory
   generation and confirmatory claims all remain behind their existing gates.
5. `director_requests.md` entry 1 (Claim Sheet review) remains open and non-blocking. Nothing
   else is blocked on the director.
