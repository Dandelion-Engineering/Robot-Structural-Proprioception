# Codex -- Human Report, Session 87

**Date and time:** 2026-08-06 22:12 PDT

**Phase:** Phase 2 -- Execution

**Physical rollouts spent this session:** **0.** Project lifetime Protocol-P-related total
remains **278**.

**Fits run this session:** **0.** Checkpoints written: **0.** Data generated: **0.**

**Progress-report session:** no. My next regular progress report is Session **88**.

---

## Summary

Claude Session 87 returned a stronger exact state for the development-fit analysis tests and
opened a new capacity-escalation design draft. I reviewed both.

I approve the strengthened test blob `6f29bf05...`. Reordering the synthetic class census
from `(1, 2, 3, 4)` to `(1, 2, 4, 3)` preserves every numerical baseline while moving the
majority from the last canonical key to the interior `actuator` key. That makes first-key,
last-key, minimum-selector and tie accidents observably distinct. The focused file passes all
35 tests under `python -O`, and the full packet remains at 1,551 passing tests.

The test loop is not formally closed. Claude's edited handoff names a returned state and asks
me to approve or contest it, but never explicitly says that Claude approves exact blob
`6f29bf05...`. The review playbook forbids inferring approval from an edit or handoff. I
explicitly approved the exact blob, leaving Claude's literal unchanged owner approval as the
only missing gate.

I accepted Claude's sequencing deviation and reviewed the capacity document now because it
authorizes no execution and is orthogonal to the fixture loop. I blocked
`capacity-escalation-v0.1.md` at blob `b86d46aa...`. Its width-sweep spine is useful, but its
`CAPACITY_BOUND` verdict overclaims what a fixed-20-epoch in-sample sweep can establish; its
outcome rules are not executable or internally consistent; it calls identical seed numbers
cross-width common random numbers even though differently shaped networks cannot share
initial weights; its grid has only one point above the fitted state; and it lacks an aggregate
plan/partial-failure contract for the proposed fits.

I ruled against adding a two-trajectory within-dev holdout to this measurement. The two dev
trajectories are different regimes -- one diagnostic-probe and one ordinary -- with different
onsets, origins and run lengths. Holding one out would measure cross-regime transfer, halve the
training set and break comparability with the approved 32-channel ledger. That may deserve a
separate symmetric design later, but it is not generic held-out generalization and does not
belong inside this width sweep.

## Work completed

### 1. Completed the required context-first startup

I read the full project details, Codex continuity, every chat summary involving Codex, the
active transcript-order monitor, the live Phase-2 tail, Claude's latest report and the review
and reproducibility-packet playbooks before responding. Live state showed Session 86/87 as
authoritative; the automation memory lagged several sessions.

No transcript-order recurrence required a monitoring note. Claude's Session-87 turn was at
the physical tail.

### 2. Approved the strengthened exact test state

The exact reviewed transition is:

```text
Reproducibility Packet/tests/test_dev_fit_analysis.py
  Codex Session-86 blob   4481ba32bd18e314094d37afc46cb8b653faddfb
  Claude Session-87 blob  6f29bf05ddebae9f33817381f4713089f99ee7e4
```

The substantive change is correct:

- class counts remain the same multiset, so total count, proportions, empirical-prior
  cross-entropy and majority accuracy are unchanged;
- `actuator` becomes the unique majority at an interior mapping position;
- the expected majority class changes from `sensor` to `actuator`; and
- the comments/docstring now accurately explain both measured fixture failures: uniform
  counts hid `max` versus `min`, and ascending counts hid `max` versus last-key selection.

The test file is outside `analysis_code_identity()`, so production analyzer blob
`31381b18...`, tracked analysis blob `0d00b5ca...`, canonical analysis digest
`7bec34a1...`, the fit ledger and all checkpoints remain unchanged. No regeneration is owed.

I did not reconstruct Claude's untracked mutation harness and do not claim an independent
mutation score. My approval rests on the exact diff, direct inspection of the production
selector, the now-distinguishing expected answer and independent focused/full test execution.

### 3. Preserved the explicit owner-approval gate

Claude's Session-87 transcript contains `Claude-returned blob 6f29bf05...` and asks me to
approve or contest it. It does not contain an explicit Claude approval of those bytes.
Under the review playbook, a returned state is not approval. I explicitly approved the blob
and asked Claude to approve the same unchanged state in chat. No file edit is needed to record
approval.

### 4. Accepted immediate design review but blocked v0.1

The capacity draft's useful choices are worth keeping:

- no Claim Sheet amendment is needed;
- Stage 1 stays inside the declared rung-1 parameter band;
- width varies while depth and the 1,023-sample receptive field stay fixed;
- the ten approved 32-channel arms are reused and never rerun;
- only dev rows are eligible, with zero rollout/generation/later-role reads;
- document, executable, plan and execution authorization remain separate gates; and
- protocol-folder placement plus approved-version immutability are appropriate.

The document is nevertheless blocked on the following decision-bearing issues.

#### Causal label

A fixed-epoch width sweep measures width sensitivity under one training protocol. It cannot
separate representational capacity from width-dependent optimization/trainability. A rising
paired difference can also result from C1 worsening rather than S improving. I required raw
absolute C1/S curves and descriptive observation labels rather than `CAPACITY_BOUND`.

#### Incomplete outcome function

Terms such as "increasing," "no upward trend" and "small relative to the seed spread" are
undefined. Suite-mean saturation can hide seed-level saturation. The current positive and
negative branches also both license Stage 2, while Section 4.2 says a within-band crossing
would make Stage 2 unnecessary for this diagnostic. I recommended removing executable
verdicts and reserving interpretation for a later joint exact-state review; any retained
classifier must be exhaustive, mutually exclusive and defined by exact inequalities.

#### Cross-width seed claim

At fixed width and seed, C1 and S do receive identical same-shaped initial weights, so their
pairing is real. The NumPy permutation also gives the same row order. Across widths, parameter
tensors have different shapes, so reusing integer seed `k` does not produce common initial
weights or make the initialization contribution common. The design may say it uses a fixed
seed set and row-order seed, but not that the width axis uses common random numbers.

#### Capacity grid

I required adding `channels = 40`. An independent constructor-only probe measured:

```text
channels 40 | parameters 61,010 | receptive field 1,023 | inside rung-1 band
```

With only 48 above the fitted 32-channel state, a saturated 48-channel point leaves no
unsaturated observation above the anchor. The revised grid `{16, 24, 32, 40, 48}` has 50
total arms, ten reused and forty new. Its 40-channel cost must be measured, not interpolated.

#### Technical-report boundary

Slot 14 requires the within-suite capacity sweep in the Technical Report, while dev-fit bound
5 forbids it from becoming the research result or selecting capacity. The draft's blanket
ban on a Technical Report C1-versus-S sentence obscures that reconciliation. I required the
sweep to be disclosed as development-only instrument diagnosis and capacity-search history,
never as held-out evidence, a headline result or capacity selection.

#### Aggregate execution state

Before any fit authorization, the design needs a canonical zero-fit plan binding every new
and reused arm, source/data/protocol identities, a fresh output root, exact output names and
the maximum fit/checkpoint budget. A run-level terminal artifact must record completed,
refused and unattempted arms plus checkpoint digests. Retry/resume behavior must forbid silent
overwrite, a second 32-channel fit, or a partial directory masquerading as a complete curve.

### 5. Preserved transcript and public-history discipline

The Session-87 response used the complete programmatically verified unique physical EOF
anchor. Post-write checks established:

```text
pre-write bytes          1,496,410
pre-write lines          23,792
pre-write SHA-256        32bc9961821a95f6f79207a258f2e09747ce3f003d314eac101c5c0d52ab3fe6
final bytes              1,506,399
final lines              23,975
header line              23,794; unique after the line boundary
old prefix               byte-identical under the pre-write SHA-256
diff                     +183 / -0
last agent               Codex
```

The public Live-Run README remained unchanged. No artifact closed, no phase changed and no
new result was produced; the lean milestone log does not need an open design-review round.

## Challenges and how they were handled

- **Automation memory lagged live state.** I treated the current repository, continuity,
  latest reports and physical transcript tail as authoritative.
- **`CODEX_HOME` was unset.** I used the known absolute local Codex path for the required
  automation memory read.
- **A technically correct handoff omitted literal approval.** I separated exact-state merit
  from process closure: approve the bytes, but do not infer the missing owner approval.
- **The capacity draft used a plausible but causal-sounding label.** I traced the actual RNG,
  network-construction and training paths before ruling. The sweep changes width under fixed
  optimization; it does not isolate representational capacity.
- **A proposed held-out split sounded stronger than it was.** Reading the approved window
  schedule showed that the two trajectories differ by regime, not just identity.
- **The transcript is append-sensitive and mixed-EOL.** I verified a complete unique LF EOF
  block, patched against that exact block and re-hashed the entire old byte prefix.

## Important decisions and reasoning

1. **Approve `6f29bf05...`.** The interior-majority fixture closes the measured last-key
   blind spot without moving any baseline number.
2. **Keep the loop open for literal owner approval.** Handoffs are not approval, even when
   the intended next action is obvious.
3. **Review the capacity draft now.** Text-only design review is orthogonal to the remaining
   fixture approval and crosses no execution boundary.
4. **Reject `CAPACITY_BOUND`.** The proposed experiment does not isolate capacity from
   optimization and cannot support that causal label.
5. **Add the 40-channel point.** It creates a second observation above the fitted anchor and
   protects the design if 48 channels is already saturated.
6. **Reject the in-draft trajectory holdout.** It measures probe-regime transfer and breaks
   anchor comparability; it is not generic held-out generalization.
7. **Require aggregate plan/failure state before fits.** Forty new checkpoints need a
   complete run identity and partial-failure story before execution, not after one fails.
8. **Leave the root README unchanged.** This session changed review state, not public
   scientific state.

## Insights gained

- Same seed labels are not common random numbers when the model tensors change shape. Pairing
  must be claimed only at the level the implementation actually preserves.
- A relative curve needs its two absolute component curves. Otherwise a crossing caused by
  baseline deterioration can be misread as target improvement.
- "Held out" names a separation, not automatically a useful generalization test. When the two
  folds are different experimental regimes, the estimand is transfer between regimes.
- A review-cycle omission can be narrower than a technical defect and still remain a real
  gate. The clean response is to approve the state and name the missing literal action.
- A small-cost run can still need a canonical plan. Checkpoint identity and partial completion
  matter independently of compute expense.

## Files created or updated

Created:

- `agents/Codex/Session Summaries/HumanReport87.md`

Updated:

- `chats/Claude-Codex/Phase 2 Integration and Config Freeze/Phase 2 Integration and Config Freeze - Active.md`
- `agents/Codex/README.md`
- `agents/Codex/Summary of Only Necessary Context.md`

Reviewed and unchanged:

- `Reproducibility Packet/tests/test_dev_fit_analysis.py`
- `Reproducibility Packet/protocol/capacity-escalation-v0.1.md`
- `Reproducibility Packet/scripts/analyze_dev_fit.py`
- `Reproducibility Packet/results/dev_fit/dev_fit_analysis.json`
- `Reproducibility Packet/results/dev_fit/dev_fit_result.json`
- `README.md` (root)
- `.gitignore`
- `chats/Claude-Codex-Human/Transcript Order Monitoring/Transcript Order Monitoring - Active.md`

## Verification

```text
test blob                             6f29bf05ddebae9f33817381f4713089f99ee7e4
analysis focused under python -O      35 passed; expected warning only
full packet suite                     1,551 passed in 129.39 s
compileall                            clean
git diff --check                      clean; expected autocrlf notices only
40-channel constructor probe          61,010 parameters / receptive field 1,023
transcript append                     old prefix byte-identical; +183/-0
fits / checkpoint writes              0 / 0
generation / rollouts                 0 / 0
pilot / validation / test reads       0
config/config.json                    absent
```

## Next steps

1. Claude explicitly approves or contests exact test blob
   `6f29bf05ddebae9f33817381f4713089f99ee7e4` unchanged. A literal approval closes the
   remaining Gate-4 test loop.
2. Claude revises capacity-escalation v0.1, addresses the causal-verdict/outcome/seed/grid/
   report/partial-state findings, and explicitly approves the state handed back.
3. Codex reviews that exact document state. Even same-state document approval will authorize
   only executable construction, not a plan execution or fit.
4. Keep every pilot/validation/test outcome, threshold, config-freeze, generation and
   confirmatory boundary closed.
