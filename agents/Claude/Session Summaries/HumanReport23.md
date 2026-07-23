# Human Report 23 — Claude

**Date and time:** 2026-07-22 20:20 PDT

---

## One-paragraph version

Last session I built a screen arguing that a better severity estimate — how badly damaged the robot judges a part to be — could never change what the recovery controller actually commands on the actuator fault class. Codex reviewed it and found a real defect: my test grid had skipped the single setting sitting exactly on the edge of the controller's flat region, which is the one place the argument could fail. It does fail there. I re-checked its correction sixty different ways, agreed, and approved it, closing that loop. Then I did the thing its correction made necessary: I measured what that edge is actually worth in tracking error. **It is worth −0.12% on average and 0.52% at worst, against a 10% bar** — and the more useful result is a bound that does not depend on my particular estimator: across a swept range of commanded responses far wider than any plausible estimation error, the tracking recovery moves by only 3.81 percentage points. So no severity read-out difference, however good, reaches the contract's bar at that boundary. Two side results came out of the same run and both matter more than I expected: the severity read-out's self-reported confidence is not just optimistic but **unevenly** optimistic across the two sensor suites — enough to *invert* which suite looks more reliable — and **exactly restoring a damaged actuator's gain does not exactly restore the tracking**, which means a gate Codex's earlier screen relies on is about 7% more optimistic than it reads.

---

## What I actually did

### 1. Owner re-review of Codex's correction — approved, loop closed

The review cycle requires that when someone edits my work, I genuinely re-open it rather than wave the edits through. Codex's diagnosis was that my `SEVERITY_GRID` omitted 0.50 remaining actuator gain.

The reason that matters takes one sentence of setup. The recovery controller responds to a severity estimate `s` with a multiplier `min(1/s, cap)`, capped at 2.0. For any estimate at or below 0.50 that expression hits the cap, so **every** estimate in that region commands exactly the same thing — the controller is blind to severity there. My screen's whole argument was that the settings with enough damage to be worth recovering all sit inside that blind region, so a better severity estimate can buy nothing.

My grid used 0.55 and 0.40 *specifically because they bracket 0.50*. I chose them to straddle the boundary and then never tested the boundary itself. At exactly 0.50 the controller is flat on one side and sensitive on the other, and 0.50 is a setting the previous screen actually recorded, with enough recovery headroom to clear the project's bar. So my "the reachable set is empty" claim was false at precisely the point my own analysis was built to locate. Bracketing a boundary is not testing it.

I verified Codex's corrected state rather than accepting it: **60 independent checks, zero mismatches.** I refit both estimators from the committed raw features and reproduced every recorded prediction; confirmed both regularization choices were the genuine cross-validation winners; recomputed every error statistic; re-derived every row of the analysis by driving the *real* recovery controller instead of the simplified stand-in; and confirmed the report regenerates byte-for-byte from its own data file. I also checked the one-sidedness claim directly on the controller: it commands 2.000000 at both 0.49 and 0.50, and 1.960784 at 0.51. Flat on one side, sensitive on the other, exactly as claimed.

**I approved Codex's exact state without editing it. That loop is closed.**

### 2. The measurement its correction made necessary

Codex's correction ended with the honest statement that the paired control effect at that boundary "must be measured rather than assumed zero." So I measured it.

The construction is cheap because of a property of our setup: the estimator makes one decision at a fixed moment, *before* any recovery action fires. So the robot's trajectory up to that decision is identical whether or not it later acts. That means the severity estimates already recorded in last session's no-action runs are exactly what a deployed estimator would have produced in an acting run at the same random seed. I do not assume that — I re-run the no-action trajectories and check them against the committed values. **All eight reference runs reproduced the recorded tracking error to zero difference, exactly.**

Forty runs: four random seeds, each under no action, a healthy-body reference, a privileged all-knowing oracle, each sensor suite's actual recorded estimate, and a five-point sweep of fixed commanded responses.

**The result.** The recovery is real on this setting — the damaged robot tracks 13.11% worse with no action, and the oracle recovers 10.81% of that. But the difference between the two sensor suites is:

| seed | conventional suite | structural suite | difference (bar = 10%) |
|---:|---:|---:|---:|
| 17100 | +10.88% | +10.88% | 0.0000% |
| 17101 | +10.56% | +10.65% | +0.1053% |
| 17102 | +10.91% | +10.45% | −0.5154% |
| 17103 | +10.69% | +10.64% | −0.0605% |

Mean **−0.1177%**. The conventional suite is ahead on two seeds, the structural suite on one, and one pair is exactly identical.

There is a structural reason the sign works out this way, and I think it is the more durable point. At this particular setting the capped response (2.0) *is* exactly the right amount of compensation for a 50% gain loss. So the blind side of the boundary happens to command the optimum, and the only direction two suites can disagree is one of them under-compensating. The suite that lands below the boundary more often wins — and that is the conventional suite, because it estimates severity more accurately. A difference at this boundary is not a structural-sensing advantage waiting to be collected; it is a coin flip about which suite sits on the optimal side, weighted toward the more accurate one.

**The bound is stronger than the measurement**, and this is the part that generalizes past my particular estimator. I swept fixed commanded responses from 1.50 up to the cap at 2.00. The tracking recovery moves from +7.00% to +10.81% — a span of **3.81 percentage points across the whole range**. The bottom of that sweep corresponds to a severity estimate roughly fifteen times more wrong than the worse suite's actual measured error, and it *still* recovers 7.00%. To produce a 10-point difference between suites, one of them would have to command essentially no action at all — which is a difference in *what class of fault it thinks this is*, not in how badly it thinks the part is damaged, and both suites identify this class correctly. So: no severity read-out difference reaches the bar at this boundary, for any read-out, not just the linear one I built.

This does not close the actuator fault class — the broader questions about whether the action is worth taking at all belong to Codex's next screen — and it does not cover a raised compensation cap, where a different boundary appears that I did not run.

### 3. Two results I did not go looking for

**The estimator's self-reported confidence is unevenly wrong.** The recovery controller refuses to act on a diagnosis whose reported uncertainty is too high, and my severity read-out only knew how to report its error *on its own training data* — which is always optimistic. I built the honest version (refit the model once per held-out random seed and measure the errors it makes on data it never saw). The result:

| suite | self-reported | actual held-out | understated by |
|---|---:|---:|---:|
| conventional (C1) | 0.004237 | 0.006741 | 1.59× |
| structural (S) | 0.001951 | **0.011160** | **5.72×** |

It is not just that both are optimistic. **The ranking inverts.** On its own training data the structural suite looks like the *more* confident read-out. Measured honestly, it is the less reliable one — the 32 extra strain-gauge inputs fit the training data tighter and generalize worse. Had we wired the training number into the controller's confidence gate, the gate would have systematically over-trusted the worse suite. Both clear the threshold on the honest number, so this changes no result; it changes what we are allowed to hand the controller.

**Exactly restoring the gain does not exactly restore the tracking.** Codex's earlier screen uses a conversion: a damaged robot that tracks `D` worse than healthy can, at best, be improved by `D/(1+D)` if you restore it perfectly. That is arithmetic and it is right as an upper bound. Measured, the privileged oracle commanding the exactly restoring response realizes **93.2%** of it — a 0.78-point shortfall, in the same direction on all four seeds. The gap is the tracking error the fault produces *before* the single decision fires, which no amount of subsequent compensation recovers. So the gate Codex's screen uses to decide which conditions advance is about 7% more optimistic than it reads. That is one condition and four seeds, and I am not proposing anything be re-run — but the condition that advanced was selected against that conversion, so it belongs in front of the next screen rather than behind it.

### 4. A packet-level gap I found and fixed

While adding my step to the reproducibility runbook I checked which test files the runbook actually tells a reader to run. **Seven of twenty-one were unreachable** — including both severity test files, the shared control-seam regression, and the evaluation metrics and statistics tests. The runbook's test step enumerated a file list, and that list has gone stale every time either agent added a screen. An outsider following our instructions would have run two-thirds of our tests and believed they had checked the packet.

I changed that step to run the test directory rather than a hand-maintained list. It is a small change but it is the kind that decides whether the reproducibility packet is honest, so I flagged it explicitly for Codex's review rather than folding it in silently.

---

## Challenges, and how they went

**Being wrong in a way my own audit could not catch.** My previous session's screen ran 42 independent self-checks and all of them passed — because every one of them tested whether the *analysis was faithful to the grid*, and none tested whether the *grid was faithful to the recorded conditions*. A predeclared grid that omits a recorded setting is invisible to any amount of internal consistency checking. I recorded the general guard rather than a one-off test: every setting an upstream artifact records must appear in the downstream grid, or be excluded by name with a reason.

**Not building the wrong thing.** The obvious over-reach here was to build the whole actuator action screen, which sits in Codex's lane and which its last turn explicitly claimed. I deliberately built only the narrow severity term underneath it, and said so plainly in the handoff. The division of labor holds better when the boundary is stated than when it is assumed.

**Spending the compute budget once.** I carried forward last session's lesson and dry-ran the entire post-run analysis path — the statistics, every derived table, the artifact writing, the report determinism, and every audit gate — on synthetic data in the exact shape the real runs return, before spending a single simulation. It caught three interface errors in seconds that would each have cost a full run.

---

## Decisions worth recording

1. **Approve rather than counter-edit.** I had a real addition to Codex's corrected report — that the boundary's flat side is the optimum, so the disagreement is signed against the structural suite. It was an addition, not a defect, so I approved the state and put the observation into new work instead of opening another round-trip. The review cycle exists to converge, not to co-author.
2. **Measure the bound, not just the number.** Four seeds on one setting is a weak result. The swept-response curve converts "multiplier difference" into "tracking difference" for the whole project, and it is what lets me say the route is closed for *any* read-out rather than for mine.
3. **Do not log an unreviewed result publicly.** The public running log entry carries only the jointly-approved correction from Codex's review — including the fact that two consecutive reviews have each caught a real error in the other agent's work, in opposite directions. It claims nothing about this session's screen, which is still in review. That follows the precedent Codex set last session.

---

## Files created or updated

**Created**
- `Reproducibility Packet/scripts/screen_severity_action_boundary.py`
- `Reproducibility Packet/tests/test_severity_action_boundary.py` (20 tests)
- `Reproducibility Packet/results/severity_action_boundary/{summary.json, arm_rows.csv, severity_action_boundary_report.md}`
- `agents/Claude/Session Summaries/HumanReport23.md` (this file)

**Updated**
- `Reproducibility Packet/scripts/utils/estimator.py` — added `leave_one_group_out_residuals`
- `Reproducibility Packet/README.md` — new Step 16, renumbered 16–19 → 17–20, Step 2 now runs the whole test suite, Current-boundary section rewritten
- `README.md` (root, public) — one running-log entry
- `chats/Claude-Codex/Phase 2 Integration and Config Freeze/Phase 2 Integration and Config Freeze - Active.md` — my Session 23 turn (+93 / −0)
- `chats/Claude-Codex-Human/Transcript Order Monitoring/Transcript Order Monitoring - Active.md` — clean-check note (+16 / −0)
- `agents/Claude/README.md`, `agents/Claude/Summary of Only Necessary Context.md`

---

## Verification

- Full packet: **240 tests passed** (220 before this session; +20 from the new screen).
- My own artifacts audited independently: **38/38 checks** — every per-seed and aggregate statistic recomputed from the raw run rows alone, every applied response re-derived against the real controller (largest disagreement 4.4e-16), the swept curve confirmed monotone, the held-out uncertainties recomputed from the previous screen's raw features, and the report regenerating byte-for-byte from its data file.
- Codex's corrected artifacts audited independently: **60/60 checks.**
- The common-random-number reuse the whole construction depends on: **8/8 reference runs reproduce the committed values at exactly 0.000e+00.**
- `compileall` clean; command-line help clean.

---

## Next steps

1. **Read Codex's reply** and either approve its state or edit and hand back. My screen, the estimator addition, packet Step 16, and the runbook change are all in that one open loop.
2. **The class-probability channel is now the only unexamined route** by which two suites that agree on the fault class could still command differently. Every result so far pins that channel at certainty on both suites.
3. **The raised-cap boundary is unmeasured.** At a compensation cap of 4 or above a different setting becomes the sensitive boundary, and all four paired runs differ there. My bound does not cover it.
4. **No progress report is due.** The next scheduled one is my Session 24.

---

## Honest bounds on everything above

Four random seeds, one simulated task, one contact condition, one fault location, one fault setting, held out over sensor noise only, at a configuration that is deliberately not frozen. This is development evidence that shapes what we build next; it is not the project's confirmatory result, and nothing here should be read as one.
