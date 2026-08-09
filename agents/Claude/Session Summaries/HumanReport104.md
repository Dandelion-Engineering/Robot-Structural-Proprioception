# Claude — Human Report, Session 104

**Date and time:** 2026-08-09 16:22 PDT

**Phase:** Phase 2 — Execution.

**What this session spent:** **zero of everything.** No fit, no checkpoint, no data
generation, no physical rollout, no plan artifact, no C7 invocation, and no artifact written
into the repository except this session's own closeout documents, three appended chat turns
and one Live-Run README log entry. The project's lifetime rollout count is **unchanged at
278** and the fit counter is **unchanged at 13**. Real-data touches were **reads only**, and
narrower than last session's: the fifty approved `.pt` checkpoints were opened only to hash
their bytes, and **no observation payload and no label payload was opened at all** — my
audit re-derives every figure from persisted JSON and from the checkpoints' digests, so it
never needed the 304 development rows. **Pilot / validation / test reads: 0.**

**Progress-report session:** **yes.** This is my regular eighth-session report point. The
normal session work was completed first; the progress report covering Sessions 97–104 is an
addition to it and lives at `agents/Claude/Progress Reports/Progress Report Session 104.md`.

---

## Summary

Three gates stood between the project and the first pre-registered reading of the capacity
sweep. Two sessions ago the first one closed. Last session I issued half of the second.
**This session both remaining gates closed, and the measurement the last twenty sessions
were built to produce has now been read.**

What happened between my last session and this one is that Codex did its half. It issued its
matching execution authorization, ran the one authorized command once, and produced the
analysis artifact — one JSON file, 89,150 bytes — then audited and approved its own exact
bytes and handed them to me. My job this session was the other half of that review loop: an
**independent** audit of those exact bytes.

**The audit found nothing, and the interesting part is what "nothing" cost to establish.**
Seventy-three checks, none of which imported the program that produced the artifact. That
constraint is the whole design of the thing. If I had audited the file by importing the
analyzer's own functions and re-running them, agreement would have been guaranteed and
meaningless — the file would have been compared against itself. So every quantity in the
artifact was re-implemented from the frozen design's own prose: the shape classifier, the
arithmetic-headroom bound, the six-decimal rounding rule, the per-seed and per-point
constraint logic, the crossing fields, the range, and the derived label. The design's
parameter table was **parsed out of the design document's text** and matched against every
arm. All fifty model checkpoint files were re-hashed from disk. All four of the artifact's
bindings — to the sweep result, the approved plan, the approved anchor analysis, and the
frozen design itself — were recomputed from the files they name.

**Then I tried to make the audit fail.** A probe that only ever prints PASS is not evidence,
and this project has already been bitten once by a probe that mis-scored a *passing* property
— which, as I wrote at the time, is one edit away from mis-scoring a failing one. So twelve
deliberately damaged copies of the artifact were written into a temporary directory and run
through the same audit: a perturbed score, a flipped label, a constraint forced on, a boolean
inverted, a curve relabelled as a trend, a rounding moved, a checkpoint digest replaced, a
forbidden verdict token smuggled in, a binding replaced, a crossing asserted, a
"capacity_selected" flag set true, and one arm's number swapped for its neighbour's. **Every
one was caught, and caught by the specific check that names that property** — not merely by
some check firing somewhere. The real file's digest was measured before and after and is
unchanged; it was never opened for writing.

Both agents now name one state, so the result loop is closed. I posted that approval as its
own turn, and then — as a separate turn, deliberately not folded into the approval — applied
the pre-registered interpretation.

## The result, stated exactly as the pre-registration permits

The frozen design contains six rows. Each row names an observation, what may be said if that
observation occurs, and what may not be said. **All six were written in Session 88, before a
single one of these fifty models existed.** I evaluated all six against the artifact's
persisted fields mechanically, and **exactly one matched:**

> **the paired curve does not have a readable shape at five points and five seeds**

with an explicit prohibition on **any trend statement**.

That is the entire licensed reading, and I have not added a sentence to it. The five
per-point numbers are persisted, audited and exact, and they may be quoted as record
contents — but they may not be strung together into a direction, a slope, a "closes," a
"widens," or a "does not move."

**The near-miss is the part I would point the director at.** One of the six rows —
the one that would have licensed *"across this band, the difference did not move by more
than the anchor's own seed spread"* — is exactly the sentence a person eyeballing these
numbers would reach for. It fails **two of its three conditions independently**: the curve's
shape is not flat-or-declining, and the spread comparison comes out the opposite way. Either
failure alone blocks it. Had the reading been chosen after the curve was seen, that sentence
is very plausibly the one that would have been written. It was not written, because the
choosing happened sixteen sessions earlier. That is not a technicality; it is the single
clearest demonstration this project has produced of why pre-registration is worth its
overhead.

A quieter second observation: **no pair at any width was arithmetically constrained**, so the
design's saturation guard never engaged and the readable domain was all five widths. The
sweep produced a fully readable domain and the shape read still came out unreadable. That is
a statement about the design's resolution at five points and five seeds — not about the
robot, the sensor suites, or the hypothesis.

## Three things in this session I would point the director at

**1. The reading is a real outcome, and it is not the outcome anyone was hoping for.** The
honest characterization is that this measurement was built to answer a specific narrow
question — does the S-versus-C1 in-sample difference behave differently as the network gets
wider within the already-authorized size band? — and the answer is that at this resolution
the question cannot be answered from this design. Five widths and five seeds do not produce
a curve with a readable shape. That is a limit of the instrument, disclosed by the
instrument, and it is worth more than a confident answer the instrument could not actually
support. It also means the next decision is genuinely open rather than implied.

**2. My own error from last session, corrected by Codex, and the general form of it.** In my
Session 103 authorization I stated that the capacity-sweep base directory "holds exactly
plans, stage1-run-1 and stage1-run-2." Codex corrected this before spending: the base has
**four** entries, not three — I had silently dropped the preserved pre-repair plan file
sitting alongside those three directories. It changed no input and no destination, but it
was a measurement stated as a fact and it was wrong. The general form is worth keeping: *a
listing of the things I was thinking about is not a census.* The census question is "what is
in this directory," and the answer has to come from the directory.

**3. A control of mine had quietly expired, and I only found out because I needed it.** In
Session 100 I built a gate that refuses a chat append whose header timestamp disagrees with
the clock at the moment of the write — built after my own header landed sixteen minutes in
the future. This session I went to use it and **it was gone**: it had lived in an untracked
scratch directory, and untracked scratch does not survive a session. I rebuilt it from my
own summary's description before writing anything, and all three of this session's appends
passed it (41 s, 27 s and 54 s of skew against a 120 s limit). But the general point is
uncomfortable and I have recorded it in the monitoring chat: **a control that lives outside
version control is a control that expires.** It survived this session on the strength of a
prose description, which is a thinner thread than a safeguard should hang on.

## Challenges, and how they were handled

**The audit had to be independent without being weaker.** The obvious way to audit a
computed artifact is to recompute it with the producer, which proves nothing. The way that
proves something is to re-derive it from the specification, which risks re-deriving it
*wrongly* and producing a false alarm — and a false alarm in a review loop is expensive,
because it consumes a round-trip and erodes the value of the next real finding. The
resolution was the twelve-mutant sweep: it establishes that my re-implementation is
discriminating before its agreement with the artifact is treated as evidence. Running the
mutants required suppressing three checks — the pinned size, digest and blob id — because
otherwise every mutant would trivially fail on the hash and the sweep would be evidence
about hashing rather than about the recomputations. That suppression is stated in the chat
turn rather than left implicit, since a suppressed check that nobody mentions is how a
mutation sweep becomes decoration.

**Deciding whether to apply the interpretation in the same message as the approval.** Codex
had explicitly asked that the review loop close before the interpretation is applied. Folding
both into one message would have satisfied the letter of that and violated its point: the
turn that closes a review should not also be the turn that spends the pre-registration. But
splitting them across *sessions* would have cost a round-trip for no benefit. I split them
across two physical turns inside this session instead, the second strictly after the first,
which satisfies the ordering exactly and loses nothing.

**One field in the artifact reads backwards out of context, and I chose not to call it a
defect.** The artifact's boundary block says `fits_run: 0` — true of the *reader*, false of
the 42-fit *run* it describes. I checked whether this was the analyzer inventing a
convention, and it is not: the already-approved development-fit analysis carries the same
field with the same meaning for a run that spent ten fits. So it is an approved precedent
followed exactly, not a defect, and it cannot be repaired for this artifact in any case (the
reader is closed and its write is a one-shot exclusive create). What it *is* is a Phase-3
obligation: when the Technical Report or the packet README quotes an analyzer's boundary
block, it has to name whose spend the block describes. I logged it as that rather than as a
finding, and stated the reasoning in the chat so Codex can overrule the reasoning and not
only the observation.

## Decisions I made

- **Approve the exact artifact bytes** at blob `3c963059…982d` / SHA-256 `e381d12e…42736`,
  89,150 bytes, closing the result loop with Codex's Session-103 owner approval of the same
  bytes.
- **Accept Codex's four-entry correction in full**, without reservation, and record the
  general lesson rather than only the correction.
- **Apply section 5.4 as a separate turn**, and report only the one row whose exact
  predicates match — adding no sentence to what the pre-registration licenses.
- **Do not propose Stage 2 in the same turn as the interpretation.** Every row of the frozen
  design says Stage 2 is a separate joint decision, including the row that matched.
- **Record two observations rather than raise them as findings** (the boundary-block scope,
  and the re-scored loss terms on the reused anchors), with the reasoning exposed in the chat
  in both cases so it can be overruled on the reasoning.
- **Rebuild the timestamp-gate writer from its gate list** rather than looking for the file,
  and write that rule into my summary so the next session does not repeat the discovery.

## Files created or updated

- `chats/Claude-Codex/Phase 2 Integration and Config Freeze/Phase 2 Integration and Config Freeze - Active.md`
  — two appended turns (the audit and approval; the section 5.4 half).
- `chats/Claude-Codex-Human/Transcript Order Monitoring/Transcript Order Monitoring - Active.md`
  — one appended monitoring entry.
- `README.md` — one Live-Run running-log entry (the joint approval and the pre-registered
  reading).
- `agents/Claude/Session Summaries/HumanReport104.md` — this report.
- `agents/Claude/Progress Reports/Progress Report Session 104.md` — the regular progress
  report covering Sessions 97–104.
- `agents/Claude/README.md` and `agents/Claude/Summary of Only Necessary Context.md` — the
  standard closeout updates.
- **No packet file, no script, no test, no result artifact and no protocol document was
  touched.** The audit probes were written to a session scratch directory outside the
  repository, deliberately, so a review session cannot become a packet edit.

## Next steps

1. **Codex owes its half of the section 5.4 application.** If it reads the row set the same
   way, the Stage-1 measurement is complete as scoped. If it reads it differently, that
   disagreement should be settled before either of us writes another line about this curve.
2. **What comes after Stage 1 is genuinely undecided**, and the frozen design forbids
   treating this reading as a licence for any of it. Stage 2 (widths past the authorized
   band, or a different architecture rung) would need its own reviewed document and its own
   joint authorization. So would any change to the number of seeds or widths.
3. **Three Phase-3 assembly obligations are now open and none blocks anything:** the packet
   README does not mention the capacity sweep at all; the 55 git-ignored checkpoints have no
   documented clean-machine recovery path; and analyzer boundary blocks need their scope
   named wherever they are quoted.
4. **My next regular progress report is Session 112**, unless a phase transition or an
   approved written Claim-Sheet amendment fires sooner.
