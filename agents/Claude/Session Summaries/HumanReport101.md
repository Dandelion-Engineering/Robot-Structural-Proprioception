# Claude Human Report — Session 101

**Date and time:** 2026-08-09 04:33 PDT

**Phase:** Phase 2 — Execution

**Physical rollouts spent this session:** 0. Project lifetime Protocol-P-related total remains **278**.

**Fits against the delivered dataset:** 0. **Checkpoint writes:** 0. **Data generation:** 0.
**Pilot / validation / test outcome reads:** 0. No `--mode execute` invocation was made and no
tracked artifact was created, edited or deleted. The only writes this session are two append-only
ones (the Phase-2 transcript and the public README log) plus my own workspace's closeout files.

**Progress-report session:** no. My next regular progress report is Session 104, unless a phase
transition or an approved Claim-Sheet amendment fires sooner.

---

## Summary

Between my last session and this one, the thing the project has been building toward for roughly
fifteen sessions actually happened: **the capacity sweep ran, and it completed.** Codex issued the
second half of the joint authorization at 02:08 and ran the single authorized command; it finished
at 02:24 with all forty-two model fits done, both reproducibility checks passing, and zero
simulation rollouts spent. Codex then audited the result and approved it, and handed it to me.

My job this session was the one step the design reserves for the second agent: **section 12 step
5, the independent exact-state review of the terminal record.** I did it, and **I approved both
artifacts at the exact bytes.** With Codex's approval already on the record naming the same state,
step 5 is closed and the sweep is finished as a measurement.

I ran **176 checks in three parts**, all green, plus the two test suites (217 focused, 1,768 whole
packet). Part A imports nothing from the program that produced the record — every digest is
recomputed from bytes on disk, and the list of arms the run was supposed to produce is rebuilt by
parsing the frozen design document's own table rather than typed from memory. Part B drives the
program's own gates, each one paired with a deliberately damaged input so that "it accepted this"
means something more than "it accepts everything." Part C rebuilds the results directory's shape in
a throwaway copy and drives the real directory-claiming code at it, so the claim that the failed
run's evidence cannot be overwritten is measured rather than read.

**The most important thing I did not do is compute what the numbers mean.** The design deliberately
splits the run from the reading: the program emits per-model measurements and no verdict at all,
and the reading — which curves rise, which points are arithmetically constrained, which of six
pre-written sentences applies — belongs to a separate analysis program that has not been built yet.
Those sentences were written down and frozen *before* any of these numbers existed, and the whole
point of that ordering is lost the moment somebody peeks. So I checked something narrower and more
useful instead: that the record contains **every primitive that reading will need**, in the right
shape, and that both constants it must source are retrievable at the field paths the plan names.
The analysis can be built. It has not been.

One thing I want to flag for you specifically, because it is the kind of small correctness detail
that is easy to get backwards and impossible to notice later: **the ten reused reference models are
still credited to the eight-module program that actually fitted them, not to this run's nine.**
Adding the sweep program to their provenance would have back-dated a file that did not exist when
they were made. The record does not do it, and I checked.

## What was accomplished

### 1. The exact-state review, in three parts

**Part A — 141 checks, importing nothing from the producer.** Both artifacts are canonical compact
JSON at the exact sizes and digests Codex named: 85,079 B / `0d8a1c2d…` and 3,354 B / `605b35fd…`,
with zero carriage returns, zero line feeds at all, no byte-order mark, no trailing newline, pure
ASCII, and a re-emission under the project's canonical settings that reproduces each file byte for
byte. Both Git blob ids were computed here and compared with what Git itself reports.

The bindings were re-derived rather than trusted: the record's plan digest equals the plan file's
own recomputed digest and equals the state gate 2 closed on; the design digest equals the frozen
design's recomputed digest; the nine code identities equal the plan's entry by entry, the eight
historical ones equal the approved ledger's exactly, and the single permitted addition is the sweep
module, whose recorded identity equals the module's recomputed digest.

The arm sets were rebuilt, not remembered — the width set was grepped out of the design's own prose
— and they are exactly right: forty completed arms at `{16,24,40,48} × {C1,S} × seeds 0-4`, ten
reused anchors at 32 channels, nothing else, and no 32-channel arm refitted. Every reused arm's
scores equal the approved analysis artifact's for that arm and its checkpoint digest equals the
approved ledger's, with the two approved sources agreeing with each other.

Forty-two distinct declared checkpoint names, forty-two distinct digests, exactly forty-two `.pt`
files under the claimed root, the set on disk equal to the declared set, and every recorded digest
matching the file it names. Every completed arm's short name is the plan's long name with the
namespace prefix removed — checked as an equality rather than by reading a list.

I also drove section 5.3 as a *search* rather than an assertion: I walked every member name and
every string in both documents looking for a verdict, a recommendation, a licence, a conclusion or
the two forbidden values, and for any absolute path, drive letter or backslash. Nothing.

And the preserved evidence is intact: the failed `stage1-run-1` root is byte-unchanged with its
three checkpoints, the consumed pre-repair plan is byte-unchanged, `config.json` is still absent,
no refusal artifact exists, and all fifty-five checkpoints in the packet are ignored by Git rather
than tracked.

**Part B — 24 checks, the program's own gates with controls.** `require_complete_sweep` — the gate
that will stand between this record and any future reading of it — **accepts** the record, and
refuses all four damaged variants: one completed arm flipped to refused, thirty-nine arms instead
of forty, one reproducibility check flipped to fail, and one anchor presented as newly completed.
The plan authenticator still accepts the consumed plan, refuses a single flipped hex character, and
still refuses the superseded pre-repair plan. The shape map **constructs** all five networks and
its parameter counts match every arm's, so that invariant is confirmed against built networks and
not only against the table I parsed.

**Part C — 11 checks, in a throwaway replica.** I rebuilt the results directory's shape under a
temporary directory (names only, no payload) and drove the real claiming code at it. Re-claiming
the completed run, the failed run, or the reserved plan-history name is refused at the same exit;
a fresh label is claimable beside them; the preserved root was never entered. Afterwards the real
tree has no new directory and still holds its forty-two checkpoints.

### 2. The review turn, and the public log

I appended the review to the Phase-2 transcript as a single additions-only turn (`+176 / −0`,
header unique at line 27,963, physically last, prior 1,741,321 bytes retained as an exact prefix
under an asserted digest, header timestamp measured inside the writer at the write). I then added
one entry to the public README log, because Codex's own entry from two hours earlier ends on "the
second agent's independent review is still open" — leaving that standing when it has closed would
have been worse than a lean log. The banner was already current at 2026-08-09 and I did not touch
it.

### 3. Cross-review

I read Codex's Session-100 report in full and the work it points to — the two authorization halves,
the execution record, and the artifacts themselves, which are the work. Its account is accurate
against my own independent measurement in every figure I checked. I have no correction to carry
forward.

## Challenges, and how they were handled

### My first audit pass reported three failures, and all three were mine

None of them was a property of the record. I computed a Git blob id with SHA-256 when blob ids are
SHA-1. I read the approved ledger's identity map under a key I remembered (`training_code_identity`)
rather than one that exists (`code_identity`), and its arms key their seed as `training_seed`. And
my Git-ignore probe drove `check-ignore --stdin`, mis-scored its output, and reported that fifty-
four of fifty-five checkpoints were tracked when in fact none is.

The first two are the same "remembered instead of read" family that already has several entries in
this project's ledger. **The third is the more interesting one and I want it recorded as its own
lesson: a probe that mis-scores a passing property is one edit away from mis-scoring a failing
one.** I replaced it with two `git ls-files` listings — tracked, and untracked-but-not-ignored —
which between them cover every file and need no parsing of quoted paths. I disclosed all three in
the review turn rather than quietly fixing them, because a review's credibility rests on the
instrument and the instrument's failures are part of its description.

### Deciding where the line sits between "reviewing the record" and "reading the result"

This was the real judgment call of the session and it took longer than the mechanics did. The
design's invariant C6 says the derived label must be *recomputable from the persisted primitives*,
and the most direct way to verify recomputability is to recompute it. But doing that would have
performed the section-5 read ahead of the program that is supposed to perform it, and would have
put the curve in front of me before the pre-registered sentences were applied. I decided that C6's recomputability is a property the analysis program's own tests will
pin when it is built, and that the strongest thing available to me *now* is a sufficiency check:
every primitive present, in the right shape and domain, on all fifty arms, and both sourced
constants retrievable at the field paths the plan names. I said so explicitly in the review turn,
with the reasoning, so it can be overruled as a judgment rather than discovered as an omission.

## Important decisions

1. **Approve at the exact bytes.** 176 checks with no failure, both suites green, and every
   negative control firing. There was nothing to return.
2. **Do not compute the descriptive read.** Reasoning above. This is the second time in this
   project that the right move was to *stop short* of a measurement I was capable of taking.
3. **Raise the equivalence artifact's self-identification as a scope statement, not a defect.**
   Measured: the two runs' equivalence artifacts are the same size, are not byte-identical, and
   differ in exactly two members — both moved only by the code-state change the repair caused.
   Everything else in them is invariant across runs, so two conforming runs at an unchanged code
   state *would* produce byte-identical equivalence files. I did not ask for a repair: the run root
   is claimed atomically and named by the run label, so the file's location is a structural
   identifier that cannot be lost without losing the file, and the terminal record carries the same
   contents member for member. Adding a field would mean version-bumping a frozen design to supply
   something location already supplies. I put the reasoning in the chat so Codex can overrule the
   argument and not only the observation.
4. **Add one public log entry.** Codex's entry left the second review "open"; it has closed.
5. **Record the packet-README gap rather than fix it here.** The Reproducibility Packet's own
   README does not mention the capacity sweep at all — zero occurrences — and the fifty-five
   git-ignored checkpoints still have no documented clean-machine recovery path. That is a Phase-3
   assembly obligation, now with two halves instead of one. Fixing it mid-review would have mixed a
   packet edit into a review session.

## Files created or updated

- `chats/Claude-Codex/Phase 2 Integration and Config Freeze/Phase 2 Integration and Config Freeze - Active.md`
  — one additions-only review turn, `+176 / −0`.
- `README.md` — one appended public log entry, `+2 / −0`; banner untouched.
- `agents/Claude/Session Summaries/HumanReport101.md` — this report.
- `agents/Claude/README.md` — workspace index refreshed.
- `agents/Claude/Summary of Only Necessary Context.md` — rewritten.

No source file, test, frozen document, plan, result artifact, checkpoint, delivered data file,
threshold or configuration was created, modified or deleted this session.

## Verification

```text
Part A  (imports nothing from the producer)      141 / 141
Part B  (the module's gates, with controls)        24 / 24
Part C  (temporary-replica namespace probe)        11 / 11
tests/test_capacity_sweep.py                      217 passed
full Reproducibility Packet suite               1,768 passed
transcript append                              +176 / −0, header unique, physically last
README append                                    +2 / −0, prefix and suffix byte-identical
git tree before the closeout writes              clean; HEAD == origin/main
```

Transcript order monitoring: **no recurrence, and verified at the Git level rather than assumed.**
Codex's Session-100 commit touches the Phase-2 transcript as a single tail hunk
`@@ -27836,3 +27836,126 @@`, additions only, and does not touch the monitoring file at all. My own
append is likewise a single tail hunk. A clean session adds no note, so I added none.

## Next steps

1. **Build invariant C7 — the read-only analysis script** — and run it through the review cycle.
   It is a new file, not an edit to `analyze_dev_fit.py`, and it should import `headroom`,
   `pair_constraint`, `classify_shape`, `quantize`, `derived_label` and `require_complete_sweep`
   from `capacity_sweep.py` rather than restating any of them.
2. **Then run it, then apply section 5.4 jointly.** Three separate gates, in that order. None of
   them is inferred from this approval.
3. Nothing else moves until then: no capacity choice, no threshold, no Stage 2, no configuration
   freeze, no generation, no rollout, and no pilot, validation or test read.
4. **Phase 3, when it comes:** the packet README owes the capacity sweep a section, and the
   fifty-five checkpoints owe a clean-machine recovery path.

**Next Claude session number:** 102.
