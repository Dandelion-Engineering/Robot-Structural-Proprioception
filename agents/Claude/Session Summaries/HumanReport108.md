# Claude — Human Report, Session 108

**Date and time:** 2026-08-10 08:18 PDT

**Phase:** Phase 2 — Execution

**Progress-report session:** No. My next regular progress report is Session 112, unless a phase
transition or an approved Claim-Sheet amendment fires one sooner.

---

## Summary

Nothing was open on me at the start of this session. Codex's Session 107 approved the exact
`.gitattributes` bytes I handed it, which closed Finding BB and, with it, the entire
Sessions 105–107 packet rule-file stretch — packet README, packet `.gitignore` and packet
`.gitattributes` are all now jointly approved and closed. That left me with a free session and
a project sitting on a decision nobody had the numbers to take.

So I took a measurement of a different kind. Stage 1 of the capacity escalation is finished,
and the frozen interpretation licensed exactly one sentence: *the paired curve does not have a
readable shape at five points and five seeds.* What happens next is a separate joint decision
the protocol deliberately refuses to license from any Stage-1 observation — which means the
decision has been sitting there with nothing measured behind it. I measured the one thing that
can be measured without touching the forbidden question: **not what the curve says, but what
this design was ever capable of resolving.**

The answer is sharper than I expected. **The design's minimum detectable difference at five
seeds is about 0.26 macro-F1. The project's pre-declared bar is 0.05.** The instrument is
roughly five times coarser than the ruler it exists to serve, and it could not have resolved a
difference of the size this project was built around, whatever the fits had returned. And the
consequence that matters for the decision: **a Stage 2 that adds widths 64/96/128 at five seeds
each costs about five minutes of compute and moves the resolution from 0.2597 to 0.2597**,
because resolution is a function of seeds and dispersion, not of how many points sit on the
axis. Seeds are the axis that buys resolution, and they are affordable — bringing all five
existing widths to the ~79 seeds that would reach 0.05 is about 2.2 hours on this machine, zero
rollouts, zero generation.

That is written up as `agents/Claude/Stage-1 Instrument Precision.md`, handed to Codex for
review, and it **licenses nothing**. I deliberately did not propose a Stage-2 design, because
proposing one is exactly the act the protocol reserves for a joint decision.

Separately, and unplanned: the gated chat writer I rebuilt at the start of the session turned
out to have a real defect, and reconciling two disagreeing header counts is what found it.

## What was accomplished

### 1. Cross-review — Codex Session 107, accepted without contest

Codex re-opened the packet-local `.gitattributes`, reproduced the load-bearing Windows checkout
behaviour in isolated Git fixtures (LF checkout → validator accepts; CRLF checkout → validator
refuses with the schema-digest mismatch), ruled on both questions I had asked it to rule on
rather than accept, and approved the exact blob unchanged.

I accept both rulings. The second one I accept on Codex's ground rather than my own: it kept
the two defence-in-depth pins because they preserve the packet's `raw_equals_canonical`
diagnostics, which is a better reason than the one I had offered ("they agree with the root
file"). The closed state:

```text
Reproducibility Packet/README.md         a985108ec4fecb028a7c2636424aaa0ea0128feb   closed
Reproducibility Packet/.gitignore        5082c2fc2c2277eef586c442b50a52881f6e5c95   closed
Reproducibility Packet/.gitattributes    76976c108853b5a9ff6712b8e5aac4345606f0bb   closed
repository-root .gitattributes           756958cf…  unchanged, and deliberately so
```

### 2. The measurement: what the Stage-1 design can resolve

**The question, and why it is askable at all.** Two prohibitions govern anything touching
Stage 1: do not add a sentence to what the frozen interpretation licenses, and do not infer
Stage 2 from an unreadable curve. Both are about the *curve*. Neither says anything about the
*dispersion*, and dispersion is not shape. So I built the note to use the per-point standard
deviations and **not to use the five per-point means anywhere at all** — which makes the
boundary checkable by inspection rather than something I merely assert.

**Method.** From the five per-seed records at each of the five capacity points, I recomputed
the paired standard deviation, each arm's own standard deviation, their correlation across the
shared seeds, the standard error, the 95% confidence half-width, the minimum detectable
difference at 80% power, and the seed count that would reach the pre-declared 0.05 scale. Two
exact self-checks had to pass before any number was recorded:

- my recomputed paired SD reproduces the artifact's own recorded field at all five points to
  better than 1e-12 (at 32 channels that field is also the recorded anchor SD,
  `0.149635726834`);
- the correlated-difference variance identity `sd_pair² = sd_C1² + sd_S² − 2·r·sd_C1·sd_S`
  holds at all five points to better than 1e-12.

The second is the one that matters. Without it, the correlation and the two per-arm SDs would
be three numbers computed alongside the difference rather than three numbers *consistent with*
it. Nothing is imported from either producer module — the Session-104 rule that an audit which
imports the producer compares a file against itself.

**The result.**

```text
 chan   n   sd_pair  sd_unpair        SE   CI_half     MDD@5   n@0.05
   16   5  0.109761   0.109319  0.049086  0.136264  0.182454       40
   24   5  0.163331   0.150037  0.073044  0.202770  0.271504       86
   32   5  0.149636   0.156027  0.066919  0.185768  0.248738       73
   40   5  0.191773   0.160623  0.085763  0.238079  0.318783      118
   48   5  0.155432   0.122338  0.069511  0.192964  0.258374       78

pooled paired sd 0.156238    MDD at n=5  0.259713    seeds to reach 0.05  79
```

**Three things it says.**

1. **The instrument is about five times coarser than the ruler.** Pooled minimum detectable
   difference at five seeds is 0.26; per point, 0.18 to 0.32. The pre-declared scale is 0.05.
2. **Pairing on seed is buying no variance reduction.** The ratio of the unpaired to the paired
   SD is 0.996, 0.919, 1.043, 0.838, 0.787 — never above 1.05, and below 1 at four of five,
   meaning the paired SD was *larger* than an unpaired one would have been. The practical
   consequence, and the reason it is in the note: the usual way to sharpen a paired design is
   to strengthen the coupling between its arms, and here there is no coupling to strengthen. So
   **there is no cheap statistical fix hiding in the pairing**; seeds are the only lever on the
   standard error.
3. **The finding the note exists for.** Priced at the run's own recorded average rate — 42 fits
   in 439.594 s, so 10.467 s per fit:

```text
design                                       new fits   hours      MDD
width-only: add 64/96/128 at 5 seeds               30    0.09   0.2597
seed-only: existing 5 widths to 20 seeds          150    0.44   0.1032
seed-only: existing 5 widths to 40 seeds          350    1.02   0.0710
seed-only: existing 5 widths to 79 seeds          740    2.15   0.0499
```

A width-only Stage 2 spends fits on an axis that does not move the quantity limiting the read,
and that is knowable **before** it runs rather than after. This is not an argument from the
Stage-1 curve — the arithmetic would read identically under any shape, which is precisely the
property I was after — and it is not a claim that width is scientifically uninteresting. It is
the narrower statement that the design as sketched would not be able to read its own result.

### 3. The defect in the control I had just rebuilt

The gated chat writer is session tooling that lives outside version control, so it has to be
rebuilt from a written list of gates each time it disappears. This was the fourth rebuild.
Gate 5 requires my header to be the physically last header in the file, and I wrote the
recognizer as a strict pattern. It reported **215** headers in the Phase-2 transcript. My own
Session-107 entry recorded **254**.

I went to reconcile the two rather than assume one was stale. The difference is not the file —
it is the recognizer. A permissive pattern finds **255**, and the 40 headers the strict one
cannot see all carry a qualifier where it demanded a comma (`Session 7 tail addendum`,
`Session 16 pilot handoff`, and so on).

That is a real defect, not a cosmetic count. A recognizer blind to 40 of this file's genuine
header forms would let gate 5 pass while one of those forms sat *underneath* my turn — and it
would pass quietly, because the gate prints a number and the number would look fine. I verified
that this session's result is sound (under the permissive pattern the last header is still mine
at the same byte offset), corrected the writer, and wrote the recognizer into the gate list so
the next rebuild inherits it.

**The lesson is the same one this block has now taught three times running, each time one level
further down.** After Session 104 the rebuild came back weaker and the fix was to write
improvements back into the block that owns the lesson. Session 107 confirmed that worked. This
time it came back weaker again for a different reason: **the list described the gates but not
the recognizer the gates are applied through.** A control is its predicate as much as its rule,
and a list carrying only the rule regenerates a control whose accept side nobody specified.

A second, smaller thing happened in the same stretch and it is worth recording as a success
rather than a defect: **gate 4 refused my first attempt at the monitoring entry**, because that
entry quotes header examples and the gate cannot tell a quoted header inside a code fence from
a real one. The right response was to indent the quotation so it is not at column 0 — not to
relax the gate. A control that has to be weakened to let a document *about the control* through
is a control that stops holding the week someone is in a hurry.

## Challenges and how they were overcome

**The main one was staying inside two prohibitions while still saying something.** The
temptation with an unreadable curve is to explain it, and every explanation available is
forbidden. The way out was to change the object: stop asking what the curve means and ask what
the instrument could have resolved. That question has an answer, the answer is decision-relevant,
and it can be computed without the means. Excluding the means from the document entirely was
the deliberate part — it converts "I did not make a trend statement" from a claim into
something a reviewer can check by searching the file.

**The second was resisting the obvious next move.** Having found that width-at-five-seeds buys
nothing, the natural thing is to write the Stage-2 design that does buy something. I did not,
and I think that is right rather than a gap: proposing a design is the act the protocol reserves
for a joint decision, and I would rather Codex and I agree on what the numbers mean before
either of us writes a document that spends fits. I left three questions explicitly open instead.

**The third was the header-count discrepancy**, which was easy to wave away. Two numbers
disagreed and neither looked wrong on its own; the strict count was only wrong *against another
number*, in a file I had written myself six hours earlier.

## Important decisions

1. **Measure the instrument, not the result.** The only line of enquiry into Stage 1 that is
   both open and useful.
2. **Use 0.05 as the reference scale, and say clearly that it is a ruler and not a target.** It
   is Claim Sheet Slot 11, pre-declared, and already carried as a field of the analysis artifact
   itself — the only effect scale in this project fixed before these numbers existed. But it is
   a *held-out* bar and the quantity measured here is *in-sample*; resolving 0.05 here is not
   clearing 0.05 there, and the note says so at length rather than in a footnote.
3. **Exclude the five per-point means from the document entirely**, to make the licence boundary
   checkable rather than asserted.
4. **Do not propose a Stage-2 design.** Left three questions open instead: whether the
   32-channel anchor may be deepened at all (its ten arms are *reused*, an invariant forbids
   writing into the development-fit tree, and that ledger is their sole provenance record);
   whether more seeds is the right instrument at all, since sharpening an in-sample statistic is
   not the same as making it the interesting one; and whether anything happens on this line at
   all, since the critical path to the configuration freeze runs elsewhere.
5. **Report the per-arm SDs and correlations but draw nothing from them.** They are present
   because the variance identity needs them. Individually, a correlation from five points is
   close to uninformative.
6. **Leave the public Live-Run README untouched.** This session produced a real finding, but an
   *unreviewed* one that is an input to a decision nobody has taken — and the log's last entry
   already tells the reader the next step is a separate joint decision. Publishing an unreviewed
   input as public status would say more than the project knows.
7. **Keep the probes out of the packet.** They are scratch instruments feeding a decision, not
   project artifacts. If the decision later needs this arithmetic published, it gets its own
   design, review cycle and `argparse` build inside the packet like everything else.

## Reasoning paths explored

I considered three other uses for a free session and rejected each. **Building toward the
Slot-8 verification artifact** — required for completion and explicitly meant to be paced in
rather than assembled at the end — turns out to depend on trained estimators and controllers
that do not exist yet; its interactive side-by-side comparison has nothing to compare. **A
Stage-2 design document** is the literal named blocker, but writing one presupposes the joint
decision that Stage 2 happens, which is the one thing the protocol reserves. **More packet
documentation** would have been safe and nearly worthless; the three rule-file loops had just
closed and there was no finding driving it.

Within the measurement itself I considered pricing the designs against the observed
differences, which would have been a much more pointed document — and rejected it, because that
is precisely the trend statement the licence forbids, wearing a lab coat.

## Insights gained

- **An instrument's resolution is measurable independently of its reading, and it is often the
  more actionable of the two.** "The curve is unreadable" and "no arm of this design could
  resolve anything smaller than 0.26" are very different sentences: the first forbids
  conclusions, the second directs the next spend.
- **The cheap axis and the useful axis were opposites here.** Width is thirty fits and five
  minutes; seeds are hundreds of fits and hours. The cheap one buys nothing measurable and the
  expensive one is still an afternoon. Cost intuitions formed on the wrong axis would have sent
  the project to the wrong place at a price that felt reassuringly small.
- **Excluding an input is stronger than promising not to use it.** Keeping the five means out
  of the document makes the compliance claim checkable by search.
- **A control is its predicate as much as its rule.** A rebuild list that specifies what a gate
  requires but not what it recognizes regenerates a gate whose accept side nobody has ever
  specified — and the accept side is where the damage is invisible. This is the same shape as
  the scrubber lesson from the Session 69–71 rounds, arriving in a completely different place.
- **Two disagreeing counts of the same object are worth more than either count.** Neither was
  self-evidently wrong. The discrepancy was the whole signal.
- **A gate that refuses a document about itself is working.** The fix belongs in the document.

## Files created or updated

- `agents/Claude/Stage-1 Instrument Precision.md` — **new**; the measurement note, handed to
  Codex for review.
- `chats/Claude-Codex/Phase 2 Integration and Config Freeze/Phase 2 Integration and Config Freeze - Active.md`
  — appended my Session-108 turn (+9,348 B).
- `chats/Claude-Codex-Human/Transcript Order Monitoring/Transcript Order Monitoring - Active.md`
  — appended the transcript-integrity entry and the writer defect (+4,226 B).
- `agents/Claude/Session Summaries/HumanReport108.md` — this report.
- `agents/Claude/README.md` — workspace tree, the new file's purpose entry, and the Live-Run
  README non-action.
- `agents/Claude/Summary of Only Necessary Context.md` — rewritten.

**Not changed:** the public Live-Run README, the packet README, either `.gitignore`, either
`.gitattributes`, any script, test, protocol, plan, result or checkpoint, the Claim Sheet, the
director requests file, or the final configuration.

## Verification and resource boundary

```text
recomputed paired SD vs the artifact's own field    5/5 points agree to < 1e-12
variance identity sd_pair² = sd_C1²+sd_S²−2r·sd_C1·sd_S   5/5 points hold to < 1e-12
imports from analyze_capacity_sweep.py / utils/capacity_sweep.py   none
pooled SD 95% χ² interval (20 df)                   [0.119531, 0.225618]
seeds at 0.05 across that interval                  47 … 162   (point estimate 79)
Bartlett homogeneity across the five widths          1.1061,  p = 0.8933
chat appends                                        2, all seven gates printed, prefixes re-asserted
gate 4                                              refused one attempt, correctly
working tree                                        clean before; only the files listed above after
```

**Zero of everything.** No fit, no checkpoint, no simulator generation, no physical rollout, no
invocation of the capacity-sweep reader, no plan mode, and no edit to any executable, test,
protocol, plan or result. **No real data was touched at all** — no manifest, no `.npz`, no label
payload, and not even a hash of a `.pt` checkpoint. The probes read exactly two tracked JSON
files and write nothing. Every probe lives in the session scratch directory outside the
repository. Pilot / validation / test reads: 0. **Lifetime physical rollouts remain 278; the
lifetime fit counter remains 13.**

Stage 1 is finished as scoped. Nothing here selects a capacity, sets a threshold, opens Stage 2,
licenses a data read, or adds a sentence to what the frozen interpretation permits.

## Next steps

1. **Codex reviews `Stage-1 Instrument Precision.md`** and rules on four things: whether the
   licence boundary is genuinely held (specifically, whether §4.1 reads as a Stage-2 argument
   dressed as arithmetic — the failure mode I am most exposed to); whether the two self-checks
   are the right ones and the recomputation genuinely independent; whether the pairing
   observation is safe to state or drifts into a suite-level claim; and whether the three open
   questions are the right three. **If Codex returns edits, the owner re-review is mine.**
2. **The joint decision itself** — what, if anything, happens next on the capacity line —
   remains untaken and is not implied by anything in this session.
3. Preserve the three closed packet rule-file states; reopen only on a genuinely new finding.
4. The disclosed clean-machine checkpoint limitation stays open by design, not by oversight.
5. My next session is 109. My next regular progress report is Session 112.
