# Human Report — Claude Session 36

**Current date and time:** 2026-07-25 15:41 PDT
**Phase:** Phase 2 — Execution
**Session role:** Answer Codex's four-item block on Amendment A2 v2; audit the margin yardstick that pinning the scalar exposed
**Final config state:** **UNFROZEN** (`Reproducibility Packet/config.json` remains absent)
**Governing decision:** `BLOCK_CONFIG_FREEZE_PENDING_PRECONFIRMATORY_BUILD_AND_VALIDATION`
**Session output:** `AMENDMENT_A2_PROPOSAL_V3` — text only. Protocol P remains unrun.
**Progress report due?** No. Last regular was Session 32; next regular is my Session 40. Neither event trigger (phase transition, approved Claim Sheet amendment) fired — A2 is still blocked, not approved.

---

## Summary

### Where the session started

Codex returned `BLOCK_AMENDMENT_A2_PROPOSAL_V2_PENDING_EXECUTABLE_PROTOCOL_AND_STRATUM_MAP` in its Session 35. It accepted both of its original Session-34 objections as closed — the mild-stratum wording and the Case-B estimand structure — and then blocked the new state on four narrower items: two design gaps that made Protocol P non-executable, and two definitions that were left to interpretation.

1. **Blocking issue 1** — P required its margin in "both development trajectories," but the approved assignment gives the ordinary trajectory no diagnostic probe and the validator forbids one. Not jointly executable.
2. **Blocking issue 2** — P measures only the two development damage levels, but Cases A and B refer to "every reserved structural severity" across all four splits. Nothing outside development was ever classified.
3. **Exact pin 3** — "synchronous gauge coefficient L2 distance" says how to combine cosine and sine within a gauge but not how to combine four gauges. Also: define "gentlest ramp" mechanically.
4. **Exact pin 4** — having the test contact window inherit validation's *length* leaves its start phase undefined and does not make duration constant across rungs, as my wording had claimed.

Codex asked for a text-only replacement pinning those four items, explicitly stating that no implementation or P run was needed first. All four objections are correct and I accepted all four without argument.

### The session's real finding: pinning the scalar broke the threshold

Three of the four items I could answer by reading the assignment. The fourth I could not, because answering "which scalar?" forced the prior question — **what is the `0.405 microstrain` number that Protocol P compares everything against actually a null of?**

I re-derived it from its own code rather than quoting it. `analyze_synchronous_detection_floor.py` reproduces the committed artifact exactly (`0.4053` against the stored `0.4052568`), so the artifact is sound. What Protocol P did with it was not. Three mismatches, all mine:

- **It is not a floor.** It is `nes_mean + 5 * nes_std` — a five-sigma *detection threshold*. The noise-only mean is `0.1108`. My protocol called it a floor and doubled it, so "2x the floor" was really about twelve sigma.
- **It is a `W=640` quantity and Protocol P specifies `W=768`.** The null narrows with the longer window.
- **It is a *per-gauge* amplitude, and P's statistic aggregated four gauges.** The existing safe-probe screen takes the max across gauges, which keeps it per-gauge-referred and internally coherent with `0.405`. My Session-35 sweep used the L2 norm of all eight entries instead — a different statistic with a different null.

Measured, same code path, same real gauge pathology stack, 200 noise-only realizations:

```text
                       null mean   null std   p95      5-sigma
W=640  per gauge         0.1108     0.0589    0.2169    0.4053   <- the committed number
       max over gauges   0.1756     0.0527    0.2655    0.4390
       vector norm (8)   0.2429     0.0631    0.3494    0.5583

W=768  per gauge         0.0891     0.0473    0.1779    0.3256
       max over gauges   0.1424     0.0408    0.2125    0.3464
       vector norm (8)   0.1957     0.0486    0.2834    0.4388   <- what P actually measured
```

The two errors ran in opposite directions and mostly cancelled. The coherent bar for the statistic P actually used is `2 x 0.4388 = 0.878` against the `0.810` I pre-registered — **7.7% lax, not a factor.** I want that recorded in both directions: the mistake was real, and the mistake was small. Reporting an error at its true size is part of reporting it honestly.

### The measurement that matters more than the arithmetic

Pinning the scalar exposed something worse than an aggregation mismatch. The sensor-only null describes the noise the sensor adds to *one* run. The quantity that decides whether the estimator can see a structural fault is the spread between *two* runs that differ only in sensor seed — and the closed loop amplifies seed differences into trajectory differences.

Measured on the delivered development diagnostic rows, `W=768` from onset, `f_d = 0.8 Hz`, unmatched seeds (which is what the estimator faces):

```text
fault minus healthy, same context cell, different seed
  rep  remEI  context                  max-gauge  vector-8
  r00   0.50  nominal / iso25c / brief    0.3017    0.4693
  r01   0.50  nominal / warm2c / none     0.3975    0.6737
  r02   0.50  0.050kg / iso25c / none     0.2088    0.3257
  r03   0.50  0.050kg / warm2c / brief    0.1328    0.2084
  r00   0.75  nominal / iso25c / brief    0.2808    0.3956
  r01   0.75  nominal / warm2c / none     0.2338    0.3262
  r02   0.75  0.050kg / iso25c / none     0.1360    0.2082
  r03   0.75  0.050kg / warm2c / brief    0.1468    0.2143

healthy minus healthy, NO FAULT AT ALL, different seed and different cell
  r00-r01  0.3687 / 0.4436      r01-r02  0.2941 / 0.4479
  r00-r02  0.2580 / 0.3773      r01-r03  0.2301 / 0.3503
  r00-r03  0.3186 / 0.3913      r02-r03  0.1760 / 0.2654
```

**Every fault-minus-healthy value lies inside the range spanned by pairs of healthy runs carrying no fault at all.** I deliberately did not call that "indistinguishable" in the chat turn and I will not here: the healthy-healthy pairs differ in context cell as well as seed, so they bound seed-and-context jointly and overstate the pure seed null. It is a range statement, not a test.

But it is decisive for protocol design, because it says the operative null is not the sensor-only null Protocol P imported — it is a run-to-run null that has never been measured, and it is plainly the larger of the two. For scale against my Session-35 sweep: matched-seed, cell r00, remaining EI 0.50, 0.05 N gave `0.175`. The same comparison unmatched gives `0.469`. **Seed noise is roughly 2.7x the fault effect at the delivered amplitude.** That is the same negative Session 34 reported, now with a mechanism and a number attached.

### What the replacement proposal pins

**Pin 3 — the scalar and its two thresholds.** The statistic is the L2 norm over all four gauge stations x `(cos, sin)` of the matched-seed fault-minus-healthy difference in observed-path harmonic-regression coefficients, `W=768` from onset, `f_d = 0.8 Hz`. I then split the single threshold into two, because it was being asked to do two different jobs with one number:

- `M1`, the **selection** gate: the five-sigma point of that statistic under the noise-only sensor stack at `W=768`, recomputed and committed as a packet artifact before any candidate runs. Candidate-independent, so it ranks the 24 candidates fairly and costs no rollouts.
- `M2`, the **stratification** gate: `2.0 x Q95`, where `Q95` is the 95th percentile of the same statistic over unmatched-seed healthy-versus-healthy pairs *within the same context cell*, measured under the selected candidate. This is the operative gate and it is strictly the harder one.

The `2.0` is a pre-declared adequacy margin, not a statistical test. Its only job is to decide which severities enter the primary estimand so we never run the confirmatory comparison on rows the data cannot carry. The confirmatory decision remains the four-way macro-F1 with its unchanged bar. "Gentlest ramp" is pinned as the **largest** `ramp_fraction_of_duration`, on the ground that at fixed peak force a longer raised-cosine ramp has lower peak `|dF/dt|` and narrower spectral content.

**Blocking issue 1 — the screening universe.** Protocol P is restricted to `trajectory_dev_diagnostic_b`; no probe-overlay clones; the ordinary trajectory stays probe-free. Not for convenience: `trajectory_dev_ordinary_a` is the pre-registered **negative control** — the feasibility spike established that ordinary torque-only excitation blocks — and overlaying a candidate probe would delete that control to screen a condition the dataset will never contain. Verified against the delivered manifest rather than inferred from the formula: `t01` occupies context cells `{4,5,6,7}`, which is a *balanced* half-fraction (payload, environment and contact each appear at both levels exactly twice), so every main effect is represented even though the worst-cell minimum now ranges over four cells instead of eight.

**Blocking issue 2 — the stratum map.** Instead of extrapolating from two development values, the selected candidate is run at **all ten** structural remaining-EI values reserved anywhere in the assignment (`0.35, 0.40, 0.45, 0.50, 0.55, 0.60, 0.65, 0.75, 0.85, 0.90`, including both compound/OOD structure components), in all four screened cells, under development payloads, environments, contacts and seeds. The mapping is then a direct table lookup — pass at value `v` makes every setting at `v` testable in every split, fail makes it sub-threshold. Branch-complete by construction, and it requires **no cutoff, no direction convention, no equality rule and no monotonicity assumption**: I removed the assumption Codex asked me to state rather than stating it. Stratum labels are fixed at development time and never relabelled; a contradicting pilot margin is reported as a payload-bounded transfer limitation under the existing degradation-ladder rule.

This is not a leak. A remaining-EI value is a plant stiffness parameter fully determined by the config; measuring mechanics at that stiffness under development conditions instantiates no non-development reservation, seed, payload, context or manifest row, and reads no non-development outcome.

**Pin 4 — the test contact window.** `contact_test_sustained.contact_window_offset_s = [1.8, 3.3]` — validation's complete pair, copied, not its length alone. Rationale corrected: this does **not** make duration constant across all four rungs (dev stays 0.5 s, pilot 0.6 s, and that escalating ladder is deliberate); it makes the val-to-test contrast carry no change in contact timing or duration, so that step moves only the pre-declared variables. It matters because Session-33 Finding 2 established that realized contact is an *effect of the fault* and is loudest in the S-exclusive gauge channel — it favours S — so lengthening exposure at the final rung would increase an S-favouring confound exactly where the confirmatory claim rests.

### Decisions I made, and the ones I handed back

**Made:** restrict the screening universe rather than clone trajectories; measure the full ten-value ladder rather than interpolate; split one threshold into two with distinct jobs; copy validation's full contact pair; keep ordinary-trajectory structural rows in the estimand.

**Handed back to Codex, deliberately:**

1. **Vector-8 versus max-across-gauges.** My argument for vector-8 is architectural — `synchronous_coefficient_vector` hands the estimator every live channel's pair and nothing downstream ever sees the max station alone, so a gate certifying the max would certify the wrong thing. **But the choice favours me and I measured how much before making it:** on delivered rows the vector norm is 1.395-1.695x larger than the max-gauge statistic while its noise is only 1.267x larger, so it has roughly 1.20x better signal-to-noise. That is a real property, not an artifact — the structural signature is spread across stations rather than concentrated in one — but it is exactly the shape my own Standing Lesson 6 says to distrust. I said so plainly and offered to adopt max-across-gauges without argument if Codex prefers continuity with the existing screen. I cannot de-bias myself here; Codex is the disinterested party.
2. **Whether the P v1 to v2 delta is a correction or a rewrite.** I treated it as a disclosed pre-execution correction and offered to re-post with no lineage if Codex disagrees.
3. **Whether ordinary-trajectory structural rows stay in the estimand** under a margin rule that only certifies the diagnostic trajectory.

### The consequence Codex did not raise, which I think matters most

If the margin is certified only on the diagnostic trajectory, then **half of every structural setting's rows — the ordinary-trajectory half — are not covered by the margin rule at all**, and they stay in the confirmatory estimand. I propose keeping them, because excluding them would mean selecting the estimand's population on excitation grounds after the fact, and because their effect is conservative: on ordinary excitation the gauge channel sits at or below the per-sample gate floor, so those rows are hard for both suites and can only shrink the S-minus-C1 contrast, never inflate it. Either way it needs naming in the amendment and in the Technical Report rather than being discovered later.

### On the honest odds

I stated in the turn, before running anything, that **Case C — this arm cannot test the question at safe excitation — is a live outcome and may well be the likely one.** `T2` is bounded above at about `0.90` microstrain and its lower end is unmeasured. Against that, my Session-35 sweep reached only `0.552` at 0.15 N, and that is the friendly number: matched seed, a single cell, at the more severe of the two development damage levels. The worst-cell value at the milder level will be lower, and 0.30 N was already violently unstable. A protocol whose most probable branch is a declared failure is still the right protocol if that is what is true, and saying so before the run is the only way the statement is worth anything.

I also declined to claim the threshold correction runs in the safe direction. The cross-cell healthy-healthy values bracket `Q95` from above, but the pure within-cell seed null is smaller by an unmeasured amount, so `T2` could land either side of the `0.810` originally pre-registered. Which side is exactly what the protocol's Stage C is for.

## Challenges and how they were resolved

**The yardstick problem recurred one session after I wrote the lesson about it.** Standing Lesson 11, written at the end of Session 35, says a threshold and the signal it judges must be measured in the same configuration. Session 36 found that my own Protocol P — written in the same session as that lesson — violated it three ways. The lesson was correct and I still did not apply it to the protocol I was writing while writing it. What worked was mechanical, not intentional: Codex's Pin 3 forced me to name the aggregation, and naming it made the mismatch unavoidable. The generalization is in the new lessons below.

**Distinguishing a correction from post-hoc protocol drift.** Protocol P explicitly said not to modify it after seeing results. I modified it. I resolved this by being precise about what "results" means: no P rollout has been run, so there are no selection results for the change to be post-hoc with respect to; the quantities that forced it are noise-only nulls and delivered-data range statements that cannot favour one candidate over another, because every candidate is judged against the same `T1` and the ladder runs only after selection closes. Then I handed the judgement to Codex rather than deciding it myself.

**Choosing a statistic whose better performance I had already measured.** Resolved by disclosure rather than by cleverness: state the architectural ground, state the measured advantage, state that it favours me, and offer to take the other option. This is the only honest handling I know of when the person choosing is not disinterested.

## Reasoning paths explored and rejected

- **Probe-overlay clones of the ordinary trajectory** (Codex's option 2 for issue 1). Rejected: it would delete a first-class pre-registered negative control to screen a condition that will not exist in the regenerated dataset.
- **A numerical cutoff rule with a stated monotonicity assumption** for the stratum map. Rejected in favour of measuring all ten values, which removes the assumption entirely rather than documenting it. Monotonicity is still reported as a diagnostic; nothing depends on it.
- **Matching the existing screen exactly** (`W=640`, max-across-gauges, imported threshold). Rejected because `W=768` is what the estimator actually reads; internal consistency with a screen is worth less than consistency with the consumer.
- **Keeping one threshold.** Rejected once it was clear selection and stratification need different nulls and one of those nulls is candidate-dependent and expensive.
- **Running Protocol P this session.** Rejected: Codex explicitly asked for text-only, and running a protocol whose threshold derivation I had just invalidated would have burned about 2.7 hours of rollouts on the wrong yardstick.

## Insights gained

1. **A threshold's *name* can hide its definition as effectively as an unpinned parameter can.** `detect_threshold_microstrain` was called "the floor" for sixteen sessions. The artifact was right; the word was wrong; and the word is what propagated into a protocol.
2. **Two configuration errors can cancel, and that is dangerous rather than lucky.** Had the window and aggregation mismatches not nearly cancelled, the 12-sigma bar would have been obviously absurd and caught sooner.
3. **The cleanest statement of a negative is often a comparison you have not made yet.** "The signal is below threshold" had been the framing for three sessions. "The signal is smaller than the difference between two healthy runs" is the same fact, needs no threshold at all, and is far harder to argue with.
4. **A protocol that cannot be executed by someone other than its author is not pre-registered.** Every one of Codex's four items was of this kind, and none of them were wrong-answer problems — they were unstated-choice problems.

## New standing lessons (carried into the context file)

- **Standing Lesson 12 — when you import a number, import its definition, not its name.** Re-derive it from the code that produced it before it becomes load-bearing.
- **Standing Lesson 13 — when a choice you must make favours you, measure how much, say so, and offer the alternative to the reviewer.** Disclosure is the only available de-biasing when the chooser is interested.
- **Standing Lesson 14 — a pre-registered protocol must be executable by someone who did not write it.** The test is whether an implementer would have to make a choice the text does not make for them.

## Files created

- `agents/Claude/Session Summaries/HumanReport36.md` — this report.

## Files updated

- `chats/Claude-Codex/Phase 2 Integration and Config Freeze/Phase 2 Integration and Config Freeze - Active.md` — appended `AMENDMENT_A2_PROPOSAL_V3` at the physical tail. Pre-write 4,541 lines; header at line 4,542, occurring exactly once, after the recorded boundary; diff **+441 / -0**; Claude physically last.
- `README.md` — one running-log entry (**+2 / -0**, append-only) recording the yardstick correction at its true 8% size and the healthy-versus-healthy range finding. Banner already current at Phase 2 / In Progress / 2026-07-25; not touched.
- `agents/Claude/README.md` — workspace index through Session 36.
- `agents/Claude/Summary of Only Necessary Context.md` — completely rewritten.

## Files deliberately unchanged

- `Claim Sheet.md` and `Accessible Claim Sheet.md` — A2 is not approved.
- All Reproducibility Packet scripts, results, configs and assignments — this was a text-only turn.
- `Reproducibility Packet/config.json` — still absent.
- The retained pre-amendment dataset under `data/` — read only.
- `chats/Claude-Codex-Human/Transcript Order Monitoring/` — no recurrence to flag (see below).
- `agents/Claude/references.md` — no external sources were read this session.

## Verification

All Python ran through `./venv/Scripts/python.exe`.

```text
packet suite (scoped):                399 passed in 9.58 s
config.json:                          absent
Protocol P:                           not run
rollouts spent on candidates:         0
non-development payloads read:        0
confirmatory identities / payloads:   0 / 0
committed floor reproduction:         0.4053 vs stored 0.4052568
```

The yardstick audit ran two checks, neither of which is Protocol P: a sensor-model-only null (no MuJoCo, no mechanics) and a read of already-delivered development rows. No rollout was generated.

**Transcript-order monitoring.** Codex's Session-35 append verified clean at the git level rather than on its report's word: `git show --numstat 29669c4` reports **+161 / -0** on the technical transcript, so nothing was deleted, moved or truncated. That is the first clean append since the Session-34 recurrence reset the streak. No recurrence occurred and none was manufactured, so I added nothing to the monitoring thread — its purpose is flagging failures, and I already put one clean check on the record in Session 23 to keep the thread from showing only failures. **Clean-append streak: two (Codex S35, Claude S36).**

## `.gitignore` review

Reviewed before staging. The root `/data/` rule still covers the retained 3.86 GB pre-amendment dataset; `/tmp/` still covers the duplicate Session-6 packet copy; venv, cache, model, LaTeX-aux, log and OS/IDE rules remain appropriate. This session's scratch work lived entirely in the session scratchpad outside the repository, so no new untracked artifact appeared. **No change required.**

## Next steps

1. **Codex owns the next turn.** It must approve `AMENDMENT_A2_PROPOSAL_V3` at exact state or block specifically, and decide the four questions handed to it — chiefly vector-8 versus max-across-gauges.
2. On approval, I implement and run Protocol P v2 on the authorized development-only universe: Stage 0 (pin the ramp field, re-derive and commit `T1`), Stage A (288 rollouts worst case), Stage B (the ten-value ladder), Stage C (the run-to-run null and `T2`). Approximately 2.7 hours as a background job.
3. Codex reviews the implementation, the result and the selected branch.
4. Only then: the written Amendment A2, the replacement hash-bound assignment, same-state approval by both agents, and full regeneration from zero.
5. Gate 4 (matched learned models) stays blocked behind all of the above.

## Claim boundaries

This session **does**: accept all four of Codex's objections; establish that the committed `0.405` figure is a five-sigma detection threshold at `W=640` on a per-gauge statistic, and that Protocol P applied it to a `W=768` four-gauge statistic; quantify that error at 7.7%; measure that delivered fault-minus-healthy gauge differences fall inside the range spanned by fault-free healthy pairs; and pin all four items into a replacement proposal.

It does **not**: run Protocol P; select a probe envelope, amplitude or severity; establish which severities are testable; certify Findings B-C from Session 35 numerically; prove the fault and healthy distributions are statistically indistinguishable (the healthy pairs confound seed with context); read any non-development payload; approve Amendment A2; generate or regenerate any data; fit any model; freeze `config.json`; or answer the project's research question.

## End state

```text
Gate 1: complete and jointly approved
Gate 2 foundation / role-write / generator / hardening: exact-state reviews closed
Gate 2 overall: open pending Gate-4 estimator and controller roles
Gate 3: complete at the pre-A2 assignment; reopened by A2
Gate 4: BLOCKED on approval of AMENDMENT_A2_PROPOSAL_V3, then Protocol P v2
Gates 5-7: open
Final config: UNFROZEN
Research result: none
Confirmatory identities / payloads materialized: 0 / 0
```
