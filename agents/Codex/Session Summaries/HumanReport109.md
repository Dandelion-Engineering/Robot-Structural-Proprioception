# Codex — Human Report, Session 109

**Date and time:** 2026-08-10 13:08 PDT

**Phase:** Phase 2 — Execution, with limited Phase-3 packet assembly

**Progress-report session:** No. The next regular Codex progress report is Session 112 unless a phase transition or approved Claim Sheet amendment fires one sooner.

---

## Summary

Claude Session 109 genuinely re-reviewed the Stage-1 instrument-precision note that Codex had
corrected in Session 108. Claude accepted all four prior findings, independently reproduced the
changed statistics, found three additional issues, repaired them, explicitly approved the new
state and handed it back.

Two of Claude's repairs were correct as written: the per-width confidence-interval column now
uses the full declared Student-*t* quantile, and the pooled dispersion is now defined explicitly
as the equal-weight root-mean-square of the five variances. Claude's third diagnosis was also
correct: dividing whole-invocation elapsed time by the 42 fitted arms does not recover a pure
fit-time average because the invocation also handled ten reused anchors and performed
authentication, scoring, hashing and output work.

The conclusion attached to that diagnosis was not correct. The returned note called
`439.594 / 42 = 10.467` seconds an upper bound on future marginal fit cost and declared every
projected runtime an overestimate. No per-arm or per-width timing exists, and the candidate
designs change the width mix; widths 64 / 96 / 128 were never timed and may cost more than the
recorded mixed-width average. Fixed overhead can push the proxy upward while a changed width
mix can push a future design above it. The record cannot compare those effects.

I corrected that one boundary directly. The note now calls 10.467 seconds a loose
whole-invocation-rate proxy and says the projected elapsed times may err in either direction.
I explicitly approve the reviewer-edited state at Git blob
`bc803294610f834900f5671ca0606caf42b21fc4`. Claude owner re-review remains open. Nothing in
the note licenses Stage 2, a capacity, a threshold, a fit, a later-role read or a final
configuration.

## What was accomplished

### 1. Reviewed Claude's Session-109 return at exact state

The owner-approved input was opened and authenticated before review:

```text
Git blob                 7877b33527afdd5bcceed41e0d8e9c630e4aefd5
raw SHA-256              e71baae9793adb282d0be33385d478a612076bd0201e2a639966339391828bf1
size / encoding          24,697 B / UTF-8 / LF / final newline
owner status             CLAUDE APPROVED / CODEX REVIEW OPEN
```

The review used only `agents/Claude/Stage-1 Instrument Precision.md` and the same two tracked
Stage-1 JSON records named by the note. It did not invoke either packet producer.

### 2. Independently reproduced the three new repairs

Using the project virtual environment and a scratch calculation imported from neither
`analyze_capacity_sweep.py` nor `utils/capacity_sweep.py`, I reproduced:

```text
full t_0.975,4                         2.7764451052
CI_half, widths 16 / 24 / 32          0.136286 / 0.202802 / 0.185797
CI_half, widths 40 / 48               0.238118 / 0.192995

equal-weight RMS paired SD            0.156237889748
arithmetic-mean paired SD             0.153986554461
RMS MDD@5 / n@0.05                    0.262792 / 79
mean-SD MDD@5 / n@0.05                0.259005 / 77
pooled variance degrees of freedom    20

curve arms                            50 = 40 fitted + 10 reused
equivalence arms                      2 fitted
fits attempted                        42
whole-invocation elapsed              439.594 s
```

All five paired SDs continued to match the persisted fields exactly. The maximum
correlated-difference variance-identity residual was `1.735e-18`. The exact noncentral-*t*
MDDs, seed thresholds, chi-square interval, Bartlett result and all seven candidate fit counts
also re-passed.

### 3. Corrected the cost-direction overclaim

The valid part of Claude's finding is that the denominator is impure: whole-run elapsed time
includes non-fit work. What cannot be recovered is how much of the elapsed time belongs to
training at each width. Therefore:

- `10.467 s` is not measured fit-only time;
- it is not a global upper bound on future marginal fit cost;
- a design with a different width mix may be faster or slower than the projection; and
- the table remains useful only as a rough order-of-magnitude comparison on this machine.

I updated sections 4 and 5.5, attached a forward reviewer correction to Claude's historical
BE finding, and updated the exact-state gate. The resulting state is:

```text
Git blob                 bc803294610f834900f5671ca0606caf42b21fc4
raw SHA-256              75a462f73c02397237eac345bbddb7ad0fbf3896fa2e8370173fb1d783c2a2c9
size / encoding          25,697 B / UTF-8 / LF / final newline
review status            CODEX APPROVED / CLAUDE RE-REVIEW OPEN
```

### 4. Recorded the review under the append-only hard gate

The Phase-2 transcript append was made only after reading the physical UTF-8 tail and
verifying a unique multi-line EOF anchor:

```text
pre-write bytes / physical lines      1,877,489 / 30,318
pre-write SHA-256                     3130f28b...ca828b15
Codex header                          unique at line 30,320
old prefix                            byte-identical
transcript diff                       +77 / -0
last recognized agent header          Codex Session 109
header-to-verification time           under 2 minutes
```

No Transcript Order Monitoring note or append-only repair was needed.

## Challenges and how they were handled

The first scratch calculation assumed the per-suite macro-F1 values inside `pairs` were
objects; they are raw floats. I inspected one persisted record, corrected the access path and
reran the independent derivation. A second attempt used an unnecessarily wide noncentrality
bracket while iterating seed counts and encountered the same SciPy `NaN` boundary both agents
had already documented. I avoided the extreme region by bracketing each MDD around the central-
*t* approximation and computed the integer seed threshold directly from exact power at the
fixed target. The final drive passed every recorded value.

The more substantive challenge was separating two cost effects that point in opposite
directions. Whole-invocation overhead contaminates the denominator, but candidate width mix is
different and untimed. Naming only the first effect created a false one-sided bound. The
repair states both effects and declines to assign a net direction the record cannot support.

## Decisions and reasoning

1. **Accept the confidence-interval and pooling repairs.** Both are exact, independently
   reproducible and improve the note's stated-method-to-number correspondence.
2. **Accept the denominator diagnosis but reject its directional conclusion.** The records
   prove whole-run timing is not fit-only timing; they do not prove every future candidate is
   faster than the proxy.
3. **Edit rather than only comment.** The review-cycle playbook permits direct reviewer edits,
   and the correction is narrow, local and independently auditable.
4. **Approve the reviewer-edited state explicitly.** Exact blob `bc803294...` now holds the
   instrument-only boundary without making an unsupported timing guarantee.
5. **Keep owner re-review open.** Claude has not reviewed the new cost-direction bytes.
6. **Do not update the public Live-Run README.** An internal planning note still inside an
   exact-state review loop is not a phase close, public result or finished artifact.
7. **Do not propose Stage 2.** The note remains decision input only. The three design questions
   are deliberately unanswered and any Stage-2 proposal and authorization stay separate.

## Resource and evidence boundary

No fit, checkpoint write, simulator generation, physical rollout, C7 invocation, plan action
or pilot/validation/test read occurred. No manifest, `.npz`, label payload or checkpoint was
opened. The review read only the note and its two tracked Stage-1 JSON inputs. Lifetime
Protocol-P-related physical rollouts remain 278. The one-shot C7 authorization remains spent.
`Reproducibility Packet/config/config.json` remains absent.

## Files created or updated

- `agents/Claude/Stage-1 Instrument Precision.md` — corrected the unsupported upper-bound /
  overestimate claim; reviewer-approved, owner re-review open.
- `chats/Claude-Codex/Phase 2 Integration and Config Freeze/Phase 2 Integration and Config Freeze - Active.md`
  — appended the exact review, independent drive, finding BF and same-state gate.
- `agents/Codex/Session Summaries/HumanReport109.md` — this report.
- `agents/Codex/README.md` — updated current authority, shared-file state, report index and tree.
- `agents/Codex/Summary of Only Necessary Context.md` — completely rewritten for the new open
  owner re-review.
- `.gitignore` — adopted the already-present `.agent-turn` ignore rule required by the new
  automation turn-handoff lifecycle; no other ignore rule changed.

The root `.gitignore` already contained the unstaged `.agent-turn` addition when session work
began. Because `.agent-turn` is the explicit mutable handoff file for this automation and must
not enter Git, I reviewed the exact two-line addition and adopted it into this session's
commit. Packet code, tests, protocols, plans, results, checkpoints, packet documentation,
Claim Sheet, director requests, final config and public Live-Run README were not changed.

## Next steps

1. Claude should genuinely re-open exact note blob `bc803294...` and explicitly approve it or
   return another state.
2. Preserve the distinction between whole-invocation elapsed per fit attempted and measured
   fit-only or future marginal cost.
3. Keep the elapsed projections as rough, directionless order-of-magnitude comparisons.
4. Do not infer or propose Stage 2, capacity selection, threshold selection, later-role reads
   or final configuration from the note.
5. The next Codex session number is 110. The next regular progress report is Session 112.
