# Progress Report — Codex, Session 104

**Date:** 2026-08-09
**Covers:** my Sessions 97–104 (previous regular report: Session 96)
**Phase:** 2 — Execution
**Written for:** Randy

---

## The short version

Eight Codex sessions ago, the project had a reviewed program and a corrected plan for a small
development-only capacity sweep, but no permission to run it. Today that entire Stage-1
measurement is complete: the plan was jointly approved, one failed run was preserved and
repaired, one clean retry finished, the result was audited by both agents, a read-only analysis
artifact was built and jointly approved, and the interpretation written before any curve
existed was applied.

The outcome is narrow and honest:

> **the paired curve does not have a readable shape at five points and five seeds**

The pre-registration forbids turning the five points into a trend statement. It does not say
the difference closes, widens, shrinks, or stays unchanged. It does not select a model size,
compare the two sensor suites, or authorize a larger experiment.

That may sound like an unsatisfying answer. It is also the answer the measurement can actually
support.

## What this measurement was trying to learn

Earlier development fitting showed that results varied substantially across random seeds. The
project therefore asked a narrower question before selecting a model: within the already
authorized network-size band, does the in-sample difference between the conventional suite
(C1) and the suite with structural signals (S) have a readable relationship with width?

The frozen protocol in
[`capacity-escalation-v0.1.md`](../../../Reproducibility%20Packet/protocol/capacity-escalation-v0.1.md)
fixed five widths, five seeds per suite, one training procedure, and six interpretation rows
before the new models were fitted. This is what “pre-registration” buys: the allowed reading
is chosen before the curve is visible, so a visually appealing story cannot be substituted
afterward.

## What happened across Sessions 97–104

### 1. The first run failed safely and taught us something about the program

Both agents authorized the original `stage1-run-1` plan. It completed two compatibility fits
and one curve fit, then refused with `X_OUTPUT_DIRTY`. The cause was not scientific: a
clean-directory guard ran once for every arm even though ten arms shared each width directory.
The second arm saw the first arm's checkpoint and treated it as stale output.

The failed root was preserved as evidence. The repair moved the cleanliness check to once per
width, before either the compatibility gate or the curve used that directory. A reviewer test
was strengthened to prove that all four new width directories are checked exactly once; merely
testing that the run completes had not proved that property.

### 2. A fresh plan and fresh authorization produced one clean retry

Because the executable bytes changed, the old plan could no longer authorize them. A new
zero-fit plan under `stage1-run-2` was generated and independently audited. Both agents issued
fresh execution halves, and the one authorized retry completed:

```text
compatibility fits                 2, both exact PASS
new curve fits                    40
new checkpoints                   42
data generation / rollouts         0 / 0
pilot / validation / test reads    0
terminal state                     X_SWEEP_OK
```

Both agents then independently approved the exact result and compatibility artifact bytes.
That approval closed the execution-result loop; it did not interpret the curve.

### 3. A separate read-only analyzer was reviewed before it saw the curve

The analyzer was built only after the result state closed. Its job was descriptive: authenticate
the approved plan and result, hash all fifty model checkpoints, compute the five point summaries,
and emit the primitive fields the pre-written interpretation table needs. It was explicitly
forbidden from choosing a capacity, issuing a verdict, reading reserved data, fitting a model,
or writing anything except one exclusive-create JSON artifact.

Review found and repaired two subtle issues before the real read: reused anchor scores live at
an approved twelve-decimal persistence boundary, while newly completed arms keep exact raw
float equality; and all network construction had to pass through the one builder that enforces
the frozen capacity invariant. The final reader and its tests received explicit same-state
approval from both agents.

One jointly authorized invocation then produced one 89,150-byte artifact. Codex audited and
owner-approved it. Claude independently re-derived its arithmetic from the protocol text,
re-hashed all fifty checkpoints, and deliberately damaged twelve temporary copies to prove the
audit could detect specific failures. Claude approved the same blob and SHA, closing the
artifact loop.

### 4. The pre-written table allowed one sentence

The artifact's paired curve was classified `NON_MONOTONE`. Of the six frozen rows, exactly one
matched. The licensed sentence is the one at the top of this report, with any trend statement
forbidden.

The most tempting alternative would have been “the difference did not move by more than the
anchor's own random-seed spread.” That row fails twice: the shape is not one of the allowed
flat-or-declining shapes, and the measured range is larger than the anchor spread. Either
failure blocks the sentence. This is the clearest reason the pre-registration mattered.

## What is working

- Every gate names exact files and exact byte identities; approvals refer to the same state.
- Failed-run evidence was preserved instead of cleaned up or silently retried.
- The successful retry authenticated every plan, input, code identity, and checkpoint.
- The analyzer was reviewed before it was allowed to read the curve.
- Independent artifact audits agreed on the exact 89,150-byte output.
- Focused verification passes 241 tests normally and under Python optimization; the full packet
  passes 1,792 tests.
- No capacity action crossed into pilot, validation, test, threshold selection, or final-config
  materialization.

## What is not working or not decided

- Five widths and five seeds do not yield a readable paired trend under this fixed protocol.
- The result does not tell us whether a wider network, more seeds, or another architecture would
  resolve the ambiguity.
- No capacity, threshold, or final configuration has been selected.
- Stage 2 is not authorized. A wider ladder or different architecture needs its own reviewed
  design and joint authorization.
- The packet README still needs a capacity-sweep/C7 runbook, and the 55 Git-ignored checkpoints
  need a clean-machine recovery path before Phase 3 can close.
- Analyzer boundary blocks say what the read itself spent, not what the fitted run spent; later
  reporting must state that scope explicitly.
- Your Claim Sheet review in `director_requests.md` remains open and non-blocking. Nothing in
  this report creates a new director-only decision.

## Where the project stands now

Stage 1 of the capacity follow-on is complete as scoped. The exact curve exists, its exact
artifact is jointly approved, and the only pre-registered interpretation has been jointly
applied. The final configuration remains unfrozen and reserved comparison roles remain unread.

The next scientific choice is genuinely open. The current result is not a hidden instruction to
climb the ladder, and it is not evidence that climbing cannot help. The correct next action is
to decide separately whether another capacity experiment is worth its cost and what question it
would answer that this one could not.

The Slot-8 director verification artifact has no new state in this interval, so this report does
not manufacture an update for it.
