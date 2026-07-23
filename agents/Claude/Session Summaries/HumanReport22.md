# Human Report 22 — Claude

**Current date and time:** 2026-07-22 18:10 PDT (checked at the shell at the moment this report was created)
**Phase:** Phase 2 — Execution
**Session type:** Closed an open review loop, then measured a term that had been sitting unmeasured underneath every control result the project has recorded

---

## Summary — the short version

Two things happened this session.

**First, I closed the open review loop.** Codex had accepted my Session-21 units correction to its tracking-deficit screen but had narrowed one of my interpretive claims before approving. I re-opened its edit, checked it against both the code and my own recorded measurements, and approved the same state. The loop is closed. Codex's narrowing was correct — and more correct than my original wording, by my own Session-21 numbers, which is worth stating plainly rather than glossing.

**Second, I measured severity-estimation quality.** Every recovery number this project has recorded was produced with a severity estimate that came from somewhere other than a real estimator: either a privileged oracle (which is a ceiling, not a capability) or a stand-in constant pinned by hand. The recovery controller's actuator action is *severity-conditioned* — how hard it pushes depends on how bad it thinks the fault is — so "how well can each sensor suite estimate severity?" was an unmeasured term underneath every control result. It was also the last remaining route by which the project's headline comparison could come out non-zero on a fault class the conventional suite already detects.

The answer has two halves, and they point the same way.

- **The action is severity-blind exactly where it has room to help.** The controller's compensation is capped, and below a threshold estimate the cap binds, so *every* severity estimate produces the identical command. Crossing that flat region against the fault severities that actually carry enough tracking deficit to be worth the project's bar: the two sets do not overlap at all. Every severity worth acting on is in the flat region; every severity the action is sensitive to has too little deficit to clear the bar even under a perfect recovery.
- **And there is no severity advantage to spend anyway.** Both suites estimate remaining actuator gain almost exactly — held-out mean absolute error 0.0060 for the conventional suite and 0.0080 for the structural-sensing suite. The conventional suite is *better*. The 32 extra structural-sensing feature columns cost a little accuracy rather than adding any.

The second result is mechanistically expected, which is part of why I believe it: the conventional suite already carries the commanded actuation and the resulting joint motion, and an actuator-gain fault acts downstream of both, so those two signals bracket the remaining gain directly. Strain is a redundant read of the same quantity there. This is the same shape the project keeps landing on, one level deeper: the structural suite's exclusive information is *structural*, and the structural fault class is the one with no control deficit to recover.

**Nothing about this is a failure.** It is the pre-declared "diagnostic-only" outcome getting more precisely characterized, and it is being characterized with measurements rather than assumed.

---

## The context I came in with

The project is in Phase 2 (Execution). The contract — the Claim Sheet — requires two things of the structural-sensing suite `S` against the matched conventional suite `C1`: an information win (≥0.05 absolute macro-F1) **and** a control win (≥10% reduction in post-change tracking error). The information win is already recorded on the bounded development condition (0.995 vs 0.704 macro-F1, driven by 100% vs 8.3% structural-fault recall). The control side has been blocking, class by class, for four sessions.

At session start, one review loop was open and it was mine to answer: in Session 21 I had first-reviewed Codex's per-class deficit screen, found that its gate converted the contract's target into the wrong units, corrected it, and handed it back. Codex had since re-reviewed, accepted the correction, made one edit of its own, and handed it back to me.

---

## Part 1 — Closing the review loop

### What Codex changed, and why I approved it

My Session-21 edit added a generated section to the screen's report bounding what its recorded headroom licenses. One bullet said that a recovery beating the "exact-restoration ceiling" — tracking better than a healthy arm — "is generic under-authority being collected."

Codex narrowed that: an action can beat the ceiling for more than one reason (fault-specific overcompensation, or a nominal controller that was simply under-authorized), and a no-action screen has no arm capable of telling them apart.

**Codex is right, and my own Session-21 measurement is the strongest evidence for it.** I had measured that the same 2× multiplier improves a *healthy* plant's tracking by 6.11% and the faulted plant's by 10.77%. That decomposes the effect into a generic part and a source-specific part of comparable size. My wording asserted a single cause for a two-cause quantity. Codex's version states only what the artifact can support and keeps the operative requirement intact — the later action screen must include a healthy false-authorization arm and report the source-specific margin separately.

### What I verified rather than took on trust

- The report **regenerates byte-for-byte** from its own committed `summary.json` — I ran the generator against the committed summary and compared SHA-256 (`f8ee1dfd…`).
- All five committed artifacts hash to exactly the values Codex recorded.
- The full packet test suite passed at **199 tests** on Codex's state.
- Codex's edit drops the `BLOCK_STRUCTURAL_RECOVERY_ACTION_FAMILY` decision key by name from the Step-14 paragraph. I checked whether a reader loses anything: they do not. Step 13 states that decision and its interpretation in full and physically precedes Step 14. Not worth reopening a loop over.

**Verdict: approved same state. Loop closed.**

### A correction I carried forward rather than reopening

In Session 21 I described the paired structural-minus-conventional control quantity on the actuator class as "arithmetically pinned at zero," attributing that to both suites diagnosing the class identically, and I listed the pinned stand-in severity as a limitation that might be hiding something.

That framing had a hole. The action is severity-conditioned, so two suites that agree on *which* fault it is can still command differently if they disagree on *how bad* it is. The recorded 0.0000% came from a stand-in that pins severity identically for both suites by construction — so it was not evidence about the severity channel at all.

Per the project's forward-propagation rule, I did not reopen the earlier work. I measured the thing instead.

---

## Part 2 — The severity-estimation-quality screen

### What I built

**A deployable severity read-out** (`SeverityRidgeHead`, in my estimator module). It is a standardized closed-form ridge regression on the window summary the estimator already computes — deliberately the smallest sufficient thing, with no new dependency and no training loop. The point is a *matched* comparison: the identical head is fitted on both suites, and it is suite-agnostic structurally rather than by configuration. A channel a suite lacks is all-zero across every training window, has exactly zero variance, and standardizes to zero, so it cannot enter the fit. Only the data differ.

**A two-part screen** (`screen_severity_estimation_quality.py`), 19 tests, and four recorded artifacts.

I also folded in a small consistency fix I had been carrying since Session 13: the two interpretable detector rungs now share one score-scale floor constant instead of one flooring at a numerical epsilon. **I verified this changes nothing recorded**, rather than asserting it: the floor can only bind if a healthy calibration set has a standard deviation below 0.001, and the committed information-review artifact records a 95th percentile of 1.281 with a maximum of 1.471 — which forces a standard deviation of at least about 0.04, more than an order of magnitude above the floor.

### Part A — where a severity difference can change the action at all

This part needs no simulation. The controller's actuator compensation is `min(1 / max(estimate, floor), cap)`. That function is **flat** below `1/cap`: over that whole range, every severity estimate produces the identical command.

I pinned my analytic version of it against the real controller over a 40-point grid at four different caps — maximum disagreement 4.4 × 10⁻¹⁶ — so this describes the controller the project actually runs, not a model of it.

At the recorded cap of 2.0, the flat region is every estimate at or below 0.5. Crossed against the tracking deficits Codex's screen recorded:

| remaining actuator gain | no-action tracking deficit | best possible reduction | is the action severity-sensitive? | is that enough to clear the 10% bar? |
|---:|---:|---:|:--:|:--:|
| 0.85 | +2.69% | +2.62% | **yes** | no |
| 0.70 | +6.28% | +5.91% | **yes** | no |
| 0.50 | +13.20% | +11.66% | no | **yes** |
| 0.25 | +23.16% | +18.81% | no | **yes** |
| 0.10 | +65.73% | +39.66% | no | **yes** |

**The two answer columns never both say yes.** Every fault severe enough to be worth recovering sits in the flat region, where a better severity estimate buys nothing; every severity the action responds to has too little deficit to reach the bar even under a *perfect* recovery.

Two consequences fall out that matter for the screen Codex is about to build:

1. **Raising the compensation cap opens exactly one grid point.** The smallest cap that makes any severity both sensitive and worth the bar is 3.0, and it only ever reaches 0.50 remaining gain.
2. **The two most severe settings can never be opened by the cap at all.** A second constant — the minimum-remaining-gain floor, 0.25 — bounds the sensitive region from below, so 0.25 and 0.10 remaining gain stay severity-blind at *any* cap. Notably that includes the very condition the corrected gate advances. Opening them means moving the floor, which authorizes compensation above 4× on the strength of a diagnosis — a safety argument, not a tuning knob.

### Part B — measured accuracy, conventional versus structural-sensing

70 no-action arms on the same bounded task, contact plane, controller, probe, and one-held-decision lifecycle every recent screen uses. Remaining gain swept over seven levels; six tuning seeds for fitting, four disjoint seeds for evaluation. One structural-suite observation per arm, physically projected down to the conventional suite so the two are exactly paired on the same trajectory and the same noise.

**I verified that projection instead of trusting it:** three arms spread across the severity grid were re-run with a genuine conventional-suite session. Maximum absolute feature difference 0.000e+00; maximum absolute tracking-integral difference 0.000e+00.

| suite | active feature columns | held-out mean abs error | RMSE | worst error | bias |
|---|---:|---:|---:|---:|---:|
| C1 (conventional) | 110 / 144 | **0.0060** | 0.0090 | 0.0265 | +0.0048 |
| S (structural-sensing) | 142 / 144 | **0.0080** | 0.0101 | 0.0184 | +0.0063 |

Both suites recover severity to well under one percentage point of remaining gain. Held-out per-severity means track the truth to the third decimal on both. **The conventional suite is slightly better**, and the 32 structural-sensing columns behave exactly as uninformative features do under ridge regression: a small variance cost.

### Parts A and B together

The severity number is not what the robot acts on — the *command* is. So both suites' held-out estimates were pushed back through the real controller to ask the only question that matters for the contract: would the two suites ever have commanded differently?

| compensation cap | arms where the action could be worth the bar | of those, the suites commanded differently | how often each matched a perfect oracle exactly |
|---:|---:|---:|---:|
| **2.0 (the recorded setting)** | 12 | **0** | **100% both suites** |
| 3.0 | 8 | 0 | 100% both suites |
| 4.0 and above | 8 | 4 | 50% both suites |

**At the setting the project actually runs, on every arm where recovery could have been worth the bar, the two suites issue the identical command — and both match a perfect oracle exactly.** They do differ elsewhere: on 15 of 28 held-out arms overall. But those differences average 0.0096 on a multiplier of order 1–2, and every single one lands on a fault mild enough that its ceiling is below the bar anyway.

That closes the question I opened in Part 1: the recorded zero paired difference on this fault class is a property of the recovery action itself, not an artifact of the hand-pinned severity that produced it. A better severity estimate cannot change it.

**One nuance the run turned up that I had not predicted, and it narrows what I would otherwise have claimed.** At caps of 4 and above, the flat region's boundary lands exactly on the 0.25 gain floor — and a real estimate of a true 0.25-remaining fault comes in at about 0.256, just above that boundary. So differences reappear there. The precise statement is narrower than my prediction: the most severe setting (0.10 remaining gain) is severity-blind at *every* cap, but the 0.25 setting is blind only while the cap stays at or below 3. This does not open a path — the differences are about 5% of a 3.9× multiplier, and the *conventional* suite is the more accurate one — but it is a boundary the planned cap sweep will run into, and it is a concrete argument against setting the cap and the floor to reciprocal values, which is what makes the boundary degenerate in the first place. I would rather have found this before those simulations than after.

**And one small result in the structural suite's favour, on a different axis.** On the healthy arms — where a perfect diagnosis would take no action at all — the structural-sensing suite reproduces the no-action command 75% of the time against the conventional suite's 25%. It is better at *not* intervening on a sound body. That is a false-authorization question rather than a control-bar question, but false authorization is precisely the axis the project's safety statistic has been blind to three times running, so it is recorded rather than dropped.

---

## Challenges, and how they were handled

**A late-failing bug wasted a full simulation run.** My first run crashed after all 70 arms because I called a serialization method on a configuration object that did not have one. The fix was trivial; the lesson was not. I responded by building a dry-run that exercises the *entire* post-simulation analysis path — model fitting, every derived table, artifact writing, and report determinism — on synthetic rows in the exact shape the real ones take. After that, every remaining change was validated in seconds instead of in ten-minute increments. That dry-run is the reusable artifact from the mistake.

**Reading my own results caught a real defect in my own analysis.** The first complete run classified fault severities into two regimes — "flat" and "severity-sensitive" — and reported that the conventional suite reproduced a perfect oracle's command on 81% of flat-region arms. That number looked wrong, and it was: my definition swept the *healthy* anchor at the top of the severity grid into the "flat" bucket, where it does not belong. On a healthy arm the oracle applies no action at all, so a mismatch there is a false-authorization question, not a severity-precision one, and folding it in understated the rate that actually matters. I split the classification into three regimes — capped, sensitive, and healthy — added tests for it, and re-ran.

**And a second, related one.** The comparison between the two suites originally reported a single count of "how often do they command differently," which mixes differences that could move the contract with differences that provably cannot. I split that by regime too, so the report distinguishes "the suites differ somewhere" from "the suites differ where it could matter." That distinction is the whole point of the screen, and the first version buried it.

Both of those cost a re-run each. Both were worth it: they are the difference between an artifact that is defensible and one that merely looks finished.

**A judgement call I made deliberately:** I did not re-derive the achieved recovery under a deployable severity estimate, even though that is the obvious next measurement. Part A makes it unnecessary at the advanced condition — because the multiplier is flat there, any estimate at or below 0.5 produces a command bit-identical to a perfect oracle's, so the achieved reduction is *exactly* the number I already recorded in Session 21 (about 10.8%, against a 10% bar, of which less than half is source-specific). Spending ten minutes of simulation to re-derive a number that follows by identity would have been waste.

---

## Decisions I made, and the reasoning behind them

1. **Build the severity read-out rather than wait for the learned model.** The learned attribution head is blocked behind a configuration freeze and a GPU install. A linear read-out is not a substitute for it, but it answers the *comparison* question cleanly — the same head on both suites — and a learned head could only raise both. It bounds the question honestly instead of leaving it unmeasured.
2. **Make the analytic part a pure function pinned to the real controller by a test.** The alternative — re-deriving the multiplier's behaviour independently — risks describing a controller the project does not run. The regression test is what makes Part A evidence rather than argument.
3. **Generate one structural-suite observation and project it down rather than running both suites.** Halves the simulation cost and makes the pairing exact by construction. Verified, not assumed.
4. **Persist the extracted window features as a fourth artifact.** The simulation is the expensive part and the features are its only durable product. Anyone — including a future session or an outside reader — can now refit the comparison with a different model, penalty, or split in seconds instead of re-running the physics.
5. **Log the units correction publicly, and claim nothing about this session's un-reviewed screen.** The public running log's previous entry recorded the 50%-remaining-gain selection that the jointly-approved correction supersedes. The log is append-only, so the correction had to be appended rather than edited in. I wrote it to show the process working — an error found by the agent that did not write the code, accepted by the one that did, which then corrected the reviewer in return.

---

## Insights worth carrying

- **A severity estimate is not a control input; the *command* is.** Two estimators that differ substantially in accuracy can be behaviourally identical, and two that agree closely can command differently, depending entirely on which region of the compensation curve they land in. Measuring read-out accuracy without mapping it through the actual action would have produced a number that looks meaningful and is not.
- **Saturation is doing more work in this system than anyone had noticed.** Two constants chosen for safety — the compensation cap and the minimum-remaining-gain floor — together determine whether a diagnosis quality difference can influence behaviour at all. They were selected as controller-safety settings, and they turn out to be the binding constraint on the project's central comparison for this fault class. That deserves to be in the write-up.
- **The project's recurring shape reappeared one level deeper.** Information the structural suite has exclusively is structural; the structural fault has no control deficit. Where there *is* a control deficit, the conventional suite already has the information — now demonstrated for severity, not just for detection.

---

## Files created or updated

**Created**

- `Reproducibility Packet/scripts/screen_severity_estimation_quality.py`
- `Reproducibility Packet/tests/test_severity_estimation_quality.py`
- `Reproducibility Packet/results/severity_estimation_quality/summary.json`
- `Reproducibility Packet/results/severity_estimation_quality/arm_rows.csv`
- `Reproducibility Packet/results/severity_estimation_quality/window_features.csv`
- `Reproducibility Packet/results/severity_estimation_quality/severity_estimation_quality_report.md`
- `agents/Claude/Session Summaries/HumanReport22.md` — this report

**Updated**

- `Reproducibility Packet/scripts/utils/estimator.py` — added `SeverityRidgeHead`; shared the score-scale floor between the two interpretable detector rungs
- `Reproducibility Packet/README.md` — new Step 15 for the screen; Steps 15–18 renumbered to 16–19
- `README.md` (root, public Live-Run) — running-log entry for the units correction
- `agents/Claude/README.md` — closed loop, new lane entry, test count
- `agents/Claude/Summary of Only Necessary Context.md` — completely rewritten for Session 23
- `chats/Claude-Codex/Phase 2 Integration and Config Freeze/…- Active.md` — my Session-22 turn, appended at the verified physical end

**Deliberately not updated**

- `agents/Claude/references.md` — no external source was read this session; it was reproduction, construction, and measurement. Fabricating entries to fill the page is exactly what the standard forbids.
- `director_requests.md` — nothing new needs the director. The Claim Sheet review (entry 1) remains open and non-blocking.
- `Claim Sheet.md` — no amendment. Nothing here changes the contract; it characterizes work already inside it.

---

## Next steps

1. **Codex first-reviews this session's work.** The loop is open and explicitly handed off.
2. **The next action screen should gain a predeclared reachability gate.** A candidate condition should have to be severity-sensitive *and* clear the bar under exact restoration before it costs any simulation. That filter would have excluded every actuator setting on the current grid, at the recorded cap, in seconds rather than hours.
3. **Cap sensitivity should sweep the floor alongside the cap.** Sweeping the cap alone leaves the two most severe settings pinned.
4. **A held-out severity uncertainty is the missing piece for wiring the read-out to the controller** — its confidence gate needs one, and what the head currently reports is an in-sample number. That is mine to build.
5. **The class-probability channel is now the only unexamined route** by which the two suites could command differently on a class they both diagnose correctly. Nothing has measured it, and the recorded prototype probabilities are explicitly not calibrated.

**No progress report was due.** My next regular one is Session 24; this session closed no phase and produced no approved Claim-Sheet amendment.
