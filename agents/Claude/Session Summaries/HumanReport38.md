# Human Report — Claude Session 38

**Current date and time:** 2026-07-28 20:50 PDT

**Phase:** Phase 2 — Execution

**Session role:** Owner response to Codex's block of `AMENDMENT_A2_PROPOSAL_V4`; verification of its five corrections; clean replacement protocol.

**Final config state:** **UNFROZEN** (`Reproducibility Packet/config.json` remains absent)

**Governing decision:** `BLOCK_CONFIG_FREEZE_PENDING_PRECONFIRMATORY_BUILD_AND_VALIDATION`

**Session decision:** `AMENDMENT_A2_PROPOSAL_V5` — posted; Codex owns the next turn.

**Rollouts spent:** zero. Everything below came from source reading, closed-form arithmetic, and re-reading data that already exists.

---

## Summary

### What this session was for

Codex opened its Session 37 by blocking my Amendment A2 proposal on five specific defects, approving everything else, and asking for one thing: a single clean replacement of Protocol P carrying only those corrections plus a new rule it wrote to settle the open design problem I had handed it. My job this session was to verify each correction was actually right, apply them, and post the replacement.

Four of those five corrections were straightforward and I confirmed them at source. The fifth — "pin the exact data reduction so it is analyst-independent" — is the one that mattered, because carrying it out is what exposed a defect neither of us had seen.

### The headline: Protocol P was going to measure the wrong second and a half

The measurement at the centre of this whole amendment works like this. The arm gives itself a small, deliberate nudge — a 1.25-second push at a known frequency — and the four strain gauges are read to see how the body answers. Damage changes the answer. The protocol compares a damaged run's answer to a healthy one's, and asks whether the difference is bigger than the difference between two healthy runs.

That comparison needs a window: which stretch of the run do you read? Protocol P said "768 steps starting at the moment the fault appears."

**In the delivered data, the nudge does not start when the fault appears. It starts a full second later.** The generator computes the probe's start as `onset + start_offset_s`, and for the development split that offset is 1.0 second — 500 control steps. So the specified window ran from step 500 to step 1268, while the nudge ran from step 1000 to step 1625. It began half a second's worth of steps *before* the nudge existed, and it ended 357 steps before the nudge finished. It captured 268 of the nudge's 625 steps — 43% — and padded the rest with ordinary task motion.

**Why it survived four sessions of review by two agents:** the convention is correct everywhere it came from. I checked every script that places a probe. All four pre-dataset screens set the probe start *equal to* the fault onset. In that configuration "window from onset" and "window from probe start" are the same window, and the screen that established our probe amplitude is internally correct. Only the dataset generator introduced the offset — deliberately, to decorrelate probe timing across splits. Protocol P inherited a screen-only convention and applied it to dataset-shaped runs.

**Why nothing failed loudly:** the one guard in that code path checks that the window is at least one probe period long. A window can satisfy that and contain no probe whatsoever.

**What it cost, measured rather than argued.** Using the privileged noise-free strain path — which is matched by construction, so it isolates the window effect exactly — on the delivered development runs:

| severity | cell | at onset (step 500) | at probe start (step 1000) | ratio |
|---|---|---|---|---|
| 25% stiffness loss | r00 | 0.0649 | 0.1584 | 2.44× |
| 25% stiffness loss | r01 | 0.0598 | 0.1593 | 2.66× |
| 25% stiffness loss | r02 | 0.0368 | 0.0872 | 2.37× |
| 25% stiffness loss | r03 | 0.0266 | 0.0968 | 3.64× |
| 50% stiffness loss | r00 | 0.1868 | 0.4787 | 2.56× |
| 50% stiffness loss | r01 | 0.1847 | 0.4755 | 2.57× |
| 50% stiffness loss | r02 | 0.0841 | 0.2755 | 3.28× |
| 50% stiffness loss | r03 | 0.0778 | 0.2798 | 3.60× |

The signal was being suppressed by a factor of roughly three.

**The single line that settles it.** I measured the healthy runs' response magnitude at the nudge's frequency in three windows:

| window | r00 | r01 | r02 | r03 |
|---|---|---|---|---|
| diagnostic run, from onset | 0.4145 | 0.4134 | 0.1500 | 0.1599 |
| diagnostic run, from probe start | 1.8806 | 1.8795 | 1.2542 | 1.2543 |
| ordinary run — **has no probe at all** | 0.4771 | 0.4850 | 0.4993 | 0.5075 |

The mis-timed window on the run that *has* a nudge showed **less** content at the nudge's frequency than the trajectory that has no nudge in it. What the protocol would have measured was the arm's ordinary movement.

**The direction is the uncomfortable part, and it is why I disclosed it the way I did.** The three previous corrections in this series all made the picture worse or merely clarified it. This one moves in the project's favour. The noise level the signal is judged against is measured with the plant switched off, so it does not move at all — the correction raises the signal by ~2.9× against an unchanged bar. I therefore led the chat turn with it, gave Codex the full measurement table, and explicitly asked for a yes/no rather than folding it in quietly.

**A better window exists and I declined it.** Sliding the window across the whole run, the response peaks 11% higher at step 1216 rather than 1000. Probe start is derivable from the configuration without looking at any measurement; step 1216 can only be found by looking at the data, and it selects in the direction that favours our hypothesis. Declined, disclosed, and left available to Codex if it disagrees.

**A quiet bonus: the negative control checked out for the first time.** The design has always relied on the probe-free ordinary trajectory as a control — the claim that without a nudge, damage barely registers in this statistic. That had been an argument, never a measurement. It is now measured: on the ordinary trajectory the same damage produces differences 3.9× to 18.6× smaller than on the probed one. The control behaves as designed.

### Verifying Codex's five corrections

I read each one against source rather than accepting it. All five were right.

1. **A failed safety branch cannot authorize the failed probe.** My protocol said that if all 24 candidate probes fail their safety gate, keep the current probe and proceed. But the current probe is one of the 24 — in that branch it failed too. Clean logical catch, accepted. I added one refinement: the delivered data already measured that probe passing every gate at healthy and at both development damage levels, but *not* at the more severe level the screen adds. So a failure at the already-measured conditions would indicate a broken harness, while a failure only at the new severity would be a genuine physical limit. The branch now has to record which.

2. **Pin the finite-sample quantile.** "95th percentile" is ambiguous at small sample sizes. Verified on the project's numpy: with 28 values the default gives 26.65 and `method="higher"` gives the 27th; with 15 values, 14.3 versus the maximum. Exactly Codex's numbers. Accepted, with an honesty note attached — `method="higher"` at 28 samples is the *second largest* value, one step off the maximum, not a robust interior quantile. It is still right, because it always sits at or above the default and therefore raises the bar, which is conservative against our own hypothesis.

3. **My explanation of a failure mode was factually wrong.** I had written that varying one of two random-seed fields but not the other would collapse the noise estimate toward zero. Codex said the code seeds on all four keys jointly, so changing either one changes the stream. I read `utils/rng.py:76-78` and it is correct: the seed sequence takes all four. Codex's counterexample is decisive — one stage of my own protocol holds one field fixed and varies the other, and gets a perfectly non-degenerate result. Accepted in full; its replacement (deterministic assertions that the identity tuples are unique) is better than the statistical tripwire it replaces, and my tripwire is demoted to a diagnostic with no authority.

4. **Pin the exact data reduction and fix the output path.** Accepted, and completed in two places. Codex's pinned code slice starts at step zero, which is neither the old convention nor the correct one — that ambiguity is what led me to check the timing at all. And its note about the output path was right; I took its second option, which is to run from the packet directory, because that is what all 25 sibling scripts and the packet's own runbook already do.

5. **Narrow the thermal claim.** Last session I reported that temperature drift "cancels exactly" from this comparison. Codex pointed out the gauges quantize their readings, and rounding breaks exact cancellation. It is right — and worse, my own three-row table from last session already showed values that differed slightly across temperature ramps, which exact cancellation would have made identical. **I published a claim my own data falsified.** Corrected to "measured near-invariance plus the first-order mechanism," with the mechanism stated more precisely than either of us had it.

### The design problem from last session — Codex solved it better than my three options

Last session I found that if only severe damage turns out to be detectable, every damage level reserved for *training* is below the threshold, and a negative result becomes unreadable: we could not distinguish "strain does not help" from "the model never saw a detectable example." I handed Codex three options without advocating for any, because the timing was the whole point — after the measurement, any fix would look chosen.

Codex rejected the option I was most worried about (moving damage levels between splits, which selects the final exam in light of the practice results) and produced a fourth I had not considered: **pre-declare a role-coverage boundary.** Before the ladder runs, commit to counting how many detectable damage settings each split ends up with, and to what we will conclude if any of training, tuning, or the final test ends up with zero. It resolves the timing problem without letting the measurement choose the population, and it generalizes correctly — I had framed the problem as being about training data, and validation and test carry distinct load-bearing roles too.

Adopted as written, with one addition: report the count itself (0, 1, or 2) per split, not only whether it is zero. Each split holds exactly two structural settings, so a count of 1 means the model trains or is graded on a single damage level — materially different from 2, and a later reader should not have to infer it from a boundary that did not fire.

### One asymmetry I had never stated, and a free fix

Working through the protocol I noticed that the signal and the noise are not the same kind of object. The signal is measured between two runs that deliberately share their random seeds, so the sensor noise largely cancels. The noise is measured between runs with different seeds, so it does not. We are comparing a noise-cancelled signal against a non-cancelled null — and that asymmetry favours our hypothesis, because a deployed robot never gets a seed-matched healthy twin of the run it is judging.

I think the design is still right for what this screen is *for* — deciding which damage levels carry a mechanical signature worth keeping. But it means "detectable" here is a necessary condition, not a sufficient one, and that is now written into the pre-registration so no later reader can read it as "the model will find this."

The fix costs zero extra simulation: the runs needed to compute the unmatched version are runs the protocol already generates. It is arithmetic on windows we will have anyway, reported as a pre-declared secondary.

### What the corrections do to the expected outcome

Last session's honest odds said the two development damage levels were unlikely to clear the bar, making a coverage-bounded result the most likely branch. The window correction changes that. Worst-cell signal at 50% stiffness loss goes from 0.0778 to 0.2755, and scaling to the strongest safe probe puts it near the bar rather than well below it.

So the most likely outcome moves from "no detectable damage in the training data" to "one of the two development levels is detectable." I wrote this into the chat turn as an estimate that moved, explicitly not a result, with its two weakest links named: it uses the noise-free path, and it imports an amplitude scaling factor measured in a different configuration — which is precisely the class of mistake the last four sessions have been finding. The protocol measures both directly.

---

## Challenges and how they were overcome

**The instruction and the finding conflicted.** Codex asked for "one clean replacement with *only* these corrections." Finding J is not one of them, and it materially changes the measurement. Suppressing it to comply would have been absurd; folding it in silently would have violated the same review discipline I have been insisting on. I did the third thing: led the turn with it, flagged explicitly that I was exceeding the instruction and why, gave the full measurement table, and offered to revert without argument. The reviewer keeps the decision; the disclosure costs one paragraph.

**Verifying a correction is not the same as trusting it.** The temptation with five corrections from a careful reviewer is to accept and move on. Reading each against source is what turned correction 4 from a formatting note into the session's main finding. This is now the fourth consecutive session where the act of making something *executable* — rather than reviewing it — produced the defect.

**Distinguishing a defect in the reviewer's fix from a defect in my protocol.** Codex's pinned code slice started at step zero. It would have been easy to file that as "Codex got it wrong." It is more accurate to say the pin was shorthand and the ambiguity is exactly what correction 4 existed to remove — and that both of our conventions were wrong for the same underlying reason. I wrote it that way.

---

## Important decisions

1. **Post the window-origin correction as a lead finding rather than fold it in.** It changes the measurement by ~3× in our favour; that requires explicit reviewer consent, not silent adoption.
2. **Decline the 11%-better peak-aligned window.** Data-selected, favours us, and no principled derivation. Disclosed and left with the reviewer.
3. **Label the replacement v2.1, not v3.** These are corrections to v2, not a supersession; v2 was never run, so there is no data trail to preserve. Codex had earlier ruled that the v1→v2 transition *was* a supersession, and the distinction is worth keeping sharp.
4. **Run Protocol P's new script from the packet directory.** Consistency with all 25 sibling scripts and the packet's own runbook beats the alternative, and it keeps the packet self-contained.
5. **Add the unmatched comparison as a pre-declared secondary.** Zero simulation cost, closes an asymmetry that favours us.
6. **Report role-coverage counts, not just zeroes.** One line, and it prevents a thin result reading as a full one.

---

## Reasoning paths explored

- **Whether the window should start at fault onset, probe start, or the empirical peak.** Settled on probe start: it is the only one derivable from the configuration without touching a measurement, and it makes the instrument identical across all four splits (625 probe steps plus 143 of ringdown in every case, because both the window length and the probe duration are constant).
- **Whether the matched/unmatched asymmetry should be fixed by changing the signal or by reporting both.** Changing the signal to unmatched would make the screen internally coherent but would answer a different question — "can one pair of runs tell them apart" rather than "does the mechanics carry a signature at all" — and would almost certainly return a null that reflects one-shot noise rather than physics. Reporting both, with the matched one operative, keeps the question intact and bounds it honestly.
- **Whether Finding J invalidates anything earlier.** Checked each: the three previous findings are sensor-model-only or pure arithmetic and are untouched, and I re-measured last session's thermal numbers over the corrected window and got identical values. The pre-dataset screens are correct in their own configuration. My own separability screen slides across all post-onset starts rather than taking one, so it dilutes rather than misses — a characterization for the report, not a correction. Per the project's forward-propagation rule I reopened none of it.

---

## Insights gained

- **The same error has now appeared at four increasing depths: window length, aggregation, operation, and time origin.** Every one was a number or convention imported from a configuration where it was correct into one where it was not. The general lesson has sharpened into something I can state precisely: when you import a measurement convention, import the *configuration that makes it true*, and check each of its assumptions still holds. A convention is not portable just because the code that implements it is.
- **A guard that checks a necessary condition can license the sufficient one.** The only check on this path asked whether the window was long enough to hold a probe. It passed, every time, on windows containing no probe. Guards written against the shape of a thing do not catch the placement of it.
- **The corrections that favour you are the ones worth the most process.** Three sessions of corrections that made the picture worse went in with a paragraph each. This one gets a lead position, a full measurement table, an explicitly declined alternative, and a request for a yes/no. That asymmetry in handling is not politeness — it is the only thing standing between a real finding and a result that was quietly tuned into existence.
- **My own published data can falsify my own published claim, and I will not notice unless I look.** The "cancels exactly" claim sat directly above a three-row table whose rows differed. Codex found it by reading the mechanism; the table was sitting right there.

---

## Files created or updated

**Created**
- `agents/Claude/Session Summaries/HumanReport38.md` — this report.

**Updated**
- `chats/Claude-Codex/Phase 2 Integration and Config Freeze/Phase 2 Integration and Config Freeze - Active.md` — appended my Session 38 turn (`AMENDMENT_A2_PROPOSAL_V5`), **+364 / −0**, header unique at line 5806, after the recorded 5805-line physical tail. Contains Finding J, the disposition of all five corrections, and the complete Protocol P v2.1 replacement text.
- `README.md` (Live-Run README) — one running-log entry for Finding J, written at the Accessible-Piece bar; banner date to 2026-07-28.
- `agents/Claude/README.md` — workspace guide refreshed.
- `agents/Claude/Summary of Only Necessary Context.md` — completely rewritten for Session 39.

**Read and verified at source (not modified)**
- `Reproducibility Packet/scripts/utils/rng.py`, `utils/synchronous.py`, `utils/sensor_model.py`, `utils/assignment_generator.py`, `utils/estimator.py`
- `Reproducibility Packet/scripts/screen_synchronous_safe_probe.py`, `analyze_synchronous_detection_floor.py`, `screen_structural_separability.py`
- `Reproducibility Packet/config/proposed-gate3-assignment-v0.1.json`, packet `README.md`
- `data/gate3-base-dev-pilot-val-c1-s/` — delivered development runs (read-only)

**Scratchpad (not committed)** — `probe_s38_window.py` (locates the probe empirically and profiles the sliding window), `probe_s38_origin_cost.py` (the origin-cost table and the probe-free control), `append_turn.py` (rebuilt append-only writer with four gates and rollback), `turn_s38.md`.

---

## Cross-review performed

Read Codex's Session 37 chat turn in full and its `HumanReport37.md`. Verified its transcript append at the git level: **+173 / −0**, a pure insertion at the physical tail. That is the **fourth consecutive clean append**; no recurrence of the misplacement failure mode, so no entry was needed in the monitoring thread, whose purpose is to flag recurrences.

---

## Next steps

**Codex owns the next turn.** `AMENDMENT_A2_PROPOSAL_V5` is open. I asked for explicit yes/no on the three items that are mine rather than Codex's: the corrected window origin (and the declined peak-aligned alternative), the zero-cost unmatched secondary, and reporting role-coverage counts. Everything else in v2.1 is Codex's correction applied or its rule adopted.

**Blocked until that settles:** implementing or running Protocol P, writing Amendment A2, the replacement assignment, regeneration, the config freeze, and my own Gate 4/5 model work.

**When it clears, in order:** implement Protocol P v2.1 (Stage 0 first, which costs no simulation) → Codex reviews the implementation and the result → written amendment and replacement assignment, both agents approving → full regeneration from zero → re-audit → my learned models and calibration → Codex's remaining storage roles → the shared controller protocol → joint config freeze → one-shot confirmatory generation and evaluation → Phase 3.

**Progress report:** none due. Last regular was Session 32; next is my Session 40. The event trigger is a *written* approved amendment, which has not happened — approving a proposal text is not the same event.

**For the director:** nothing is blocked on you. `director_requests.md` entry 1 (Claim Sheet review) remains open and non-blocking.

---

## Honest state of the project

Still no research result. Nothing is frozen, no configuration exists, the final test set has never been touched, and the central question is open.

What this session added is a defect caught before it cost 168 simulation runs and, more importantly, before it produced a negative result that would have been an artifact of a mis-timed window rather than a fact about strain sensing. Four sessions in a row have now found errors in how this project measures itself, each deeper than the last, and each found by trying to make the procedure executable by someone who did not write it. That is the process working, and it is also a fair warning about how much of the last several sessions' apparent progress was built on numbers that did not mean what they said.
