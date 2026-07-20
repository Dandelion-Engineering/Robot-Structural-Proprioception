# Human Report 13 — Claude

**Date & time (report created):** 2026-07-20 14:22 PDT
**Session:** Claude Session 13
**Phase:** Phase 2 (Execution) — open; nothing frozen

---

## One-paragraph summary

This was a **cross-review session** — no new production code from me, and that was the right call. Codex's Session 12 handed me two things: my own `CoefficientReferenceDetector` estimator increment *after Codex had reviewed and edited it* (which I owed a genuine owner re-review), and a brand-new **recovery-controller floor** (`recovery_control.py`) for first review. I re-read both artifacts in full, wrote an independent 26-check verification script that reproduced their load-bearing properties from scratch (not by re-running Codex's tests), confirmed the full test suite is green (127 passed), and verified that all three of my own S12 "forward nits" were closed in the committed artifacts. Conclusion: both of Codex's corrections to my code are right in diagnosis *and* implementation, and the recovery controller is sound and correctly scoped. I approved both states, which **closes both review loops**, and I recorded the reproduction evidence plus a forward experimental-design note in the shared chat. I deliberately did **not** invent new build work, because my genuinely-next substantial build (the learned attribution head) is correctly blocked behind the config freeze and a PyTorch install, and the framework explicitly warns against manufacturing follow-on tasks.

---

## What I did, in detail

### 1. Context load and a git-state reconciliation

Read the framework docs (`Project Details.md`, `AgentPrompt.md`), my continuity file, my workspace README, all three concluded-chat summaries, and the full active Phase-2 transcript (now 764 lines). The git snapshot in my session prompt was **stale** — it showed HEAD at "Claude Session 11" with the pilot files untracked. I checked the live repo state empirically: HEAD is actually `a049f53 Codex Session 12`, working tree clean. So Codex's entire S12 output (the estimator edits, the new recovery controller, and the pilot forward-fixes) was already committed, and I was reviewing against a clean baseline. Reconciling this first mattered — it told me exactly what state I was reviewing and prevented confusion at the commit step.

### 2. Genuine owner re-review of the coefficient-reference rung (my lane, Codex edited it)

Codex made two corrections to the `CoefficientReferenceDetector` I built in S12. I reproduced each independently rather than trusting the description:

- **Correction 1 — "score coherence is not decision-margin inheritance."** My S12 claim that "the deployed rung's margin *is* the pilot's margin" was an overclaim. The *statistic* (the window→distance function) is shared and pinned bit-equal; the *margin* and *decision rates* are not, because they depend on the threshold, the reference data, and the persistence latch, none of which the pilot and the deployed rung share. I demonstrated this concretely: two detectors sharing one feature extractor return identical `score(window)` on every window, yet **disagree on the decision** once their thresholds differ, and a persistence-1 vs persistence-3 pair latch detection at different times on the same score stream. Codex's narrowed wording (and the qualifier "matched-C1 **minimum per-fault** detection = 0%", which correctly localizes the 0% to the *structural* fault) is exactly the honest level. I approved it.

- **Correction 2 — re-fit lifecycle guard.** A detection threshold calibrated against one healthy reference's noise distribution is meaningless against a *different* reference. Codex made `fit_reference` invalidate any existing threshold and reset the detection latch when it replaces a reference, and made `update` refuse to score until recalibrated. I reproduced the full cycle (fit → calibrate → latch → re-fit → threshold cleared, latch reset, `update` raises, recalibrate → works again) and separately confirmed the **atomicity**: a re-fit that fails partway (I fed an oversized window) leaves the old reference and threshold fully intact, because the new values are computed on local variables before any assignment to the object. The softened tail-guard wording ("can collapse to or sit near the maximum") is the correct general statement.

**Outcome:** I approved the exact edited `estimator.py` + `test_estimator.py` state. **The owner review loop is closed** (both agents have now explicitly approved the same state).

### 3. First review of the interpretable recovery-controller floor (Codex's lane, plugs into my seam)

`utils/recovery_control.py` is the small, auditable controller floor that plugs into my `EstimatorCommandPolicy` seam. I read it and its tests in full and verified independently:

- It consumes **only** the deployable `EstimatorOutput` plus time — no privileged plant state crosses the boundary.
- On the **real** `CablePlant`, a confident actuator diagnosis (joint 1, 50% gain remaining) requests exactly 2× nominal torque at that joint, and the plant's downstream 0.5 gain then delivers the nominal command bit-for-bit with no saturation — the compensation cancels the fault.
- A structural diagnosis applies only a bounded global derate (0.75), explicitly *not* claiming the stiffness was repaired.
- Abstained, unlocalized, over-uncertain, and (via Codex's tail-addendum fix) a non-abstained 50/50 structure-vs-actuator **tie** all fail safe to the nominal command.
- **The cross-lane property I care about most:** I drove my own detection-only `CoefficientReferenceDetector` on a changed window *through* the controller. Because that rung abstains on the fault type, the controller correctly holds nominal. So the "detection-only rungs cannot trigger active compensation" safety boundary holds **end-to-end through the shared seam**, not just in the controller's isolated unit tests.

**Outcome:** I found no defect requiring an edit, so I approved the state Codex approved. **The first-review loop is closed.**

### 4. Verified my three S12 forward nits are closed

- **Dedup:** the pilot script now imports the coefficient functions from `utils.estimator` — confirmed by *object identity*, so there is genuinely one definition, not two copies that agree.
- **Base seed:** both pilot `summary.json` files now record `base_seed` (1000 broad / 5000 follow-up) and the reports print the exact calibration/held-out seed ranges.
- **Symmetric caveat:** the advancing report now states plainly that the 32-seed threshold is still the leave-one-out maximum with 1/48 event resolution — it now reads symmetrically with the more-cautious BLOCK report.

---

## Challenges and how they were handled

- **Stale git snapshot.** The prompt's git status disagreed with my continuity notes (it predated Codex's S11/S12 commits). Rather than reason in circles, I ran `git log`/`git status` directly and reconciled to ground truth before touching anything. Resolved cleanly.
- **The temptation to "produce" something.** The honest state of the project is that my next substantial build (the learned temporal-attribution head) is blocked behind the config freeze and a GPU PyTorch install, and the evaluation driver is blocked behind a frozen data layout. I judged that a thorough, verified cross-review that closes two loops *is* the session's real contribution, and that manufacturing a marginal new test to look busy would violate both the forward-motion discipline and the framework's explicit warning against inventing follow-on work. I did surface one genuinely useful next increment (an end-to-end closed-loop seam test) as a proposal rather than building it, to avoid reopening the loops I was closing.

---

## Important decisions and the reasoning behind them

1. **Approve both states rather than edit-and-hand-back.** Both of Codex's corrections were correct and the controller had no defect. Editing to "participate" would have reopened loops for no reason. The review cycle closes when both agents approve the *same* state; approving as-is is the correct move when the work is right.
2. **Leave the Live-Run README untouched.** Heartbeat check ran; the session closed review loops on development scaffolding, froze nothing, closed no phase, and produced no new research result. The last public-worthy advance (the pilot) is already logged, and Codex deliberately kept the public README untouched for this same controller work. Lean-by-design says leave it.
3. **Record two forward notes, neither blocking:** (a) a tiny robustness consistency nit in my own rung (`unknown_score` floors the null-std at `_EPS` while the sibling novelty detector floors at `1e-3`; I'll align it in my next estimator increment rather than reopen this loop), and (b) an on-the-record note that a constructor-supplied threshold survives the *first* `fit_reference` but is invalidated on re-fit (correct by design, but worth knowing).
4. **Articulate the headline-experiment design now that both seam ends exist.** With my `EstimatorCommandPolicy` socket and Codex's `GainScheduledRecoveryController` both present, the "does attribution improve control" comparison is wireable: detection-only rungs → nominal (floor), learned attribution head → active compensation (headline arm), RMA latent → blind adaptation, oracle → ceiling. Naming this now means the trained head lands into a socket whose control semantics are already fixed.

---

## Insights gained

- **The cleanest way to prove "shared statistic ≠ shared margin" is to build two detectors that share the statistic and watch them disagree.** That single construction (identical `score()`, different decisions) is more convincing than any amount of prose about why the margin isn't inherited — and it is exactly what made Codex's Correction 1 land for me.
- **The recovery controller's safety boundary is enforced twice over.** A detection-only rung can't trigger compensation both because it sets `abstain_decision=True` *and* because its uniform non-healthy mass never lets any fault class become the unique argmax above the probability gate. That redundancy is a good sign the boundary is a real property of the design, not a single fragile check.
- **The project's detect→attribute→compensate loop now exists end-to-end in prototype** — detection (two interpretable rungs), the seam, and the control end (the recovery floor) — with the *attribution* middle deliberately left to the post-freeze trained head. The scaffolding holds together; what remains is the frozen configuration and the learned head that exercises the active paths.

---

## Files created or updated this session

- **Updated:** [`chats/Claude-Codex/Phase 2 Integration and Config Freeze/Phase 2 Integration and Config Freeze - Active.md`](../../../chats/Claude-Codex/Phase%202%20Integration%20and%20Config%20Freeze/Phase%202%20Integration%20and%20Config%20Freeze%20-%20Active.md) — appended my Session 13 review turn (verified at the physical tail, appears once).
- **Created:** [`agents/Claude/Session Summaries/HumanReport13.md`](HumanReport13.md) — this report.
- **Updated:** [`agents/Claude/README.md`](../README.md) — added the Session 13 review-cycle outcome.
- **Rewritten:** [`agents/Claude/Summary of Only Necessary Context.md`](../Summary%20of%20Only%20Necessary%20Context.md) — refreshed for Session 14.
- **Not committed (outside repo):** `scratchpad/s13_reproduce.py` — my independent 26-check reproduction script.
- **Reviewed but not modified by me** (Codex's committed S12 work): `Reproducibility Packet/scripts/utils/estimator.py`, `Reproducibility Packet/scripts/utils/recovery_control.py`, `Reproducibility Packet/tests/test_estimator.py`, `Reproducibility Packet/tests/test_recovery_control.py`, `Reproducibility Packet/scripts/run_noisy_reference_pilot.py`, and the two pilot result directories.

*No production code changed hands from me this session — the deliverable was the verified review that closed two loops.*

---

## Next steps / pending actions

**For my next session (Session 14):**
1. **Check Codex's reply** to my S13 turn. Both review loops are closed from my side; Codex's next move is likely a plant-lane build — the interpretable residual/linear-system-ID baseline, or the evaluation-sized closed-loop recovery comparison, or the validation-sized threshold calibration.
2. If Codex opens a new loop (e.g., the residual baseline), review it.
3. **Fold in the tiny robustness nit** (float the coefficient rung's `null_std` floor to match the novelty detector's `1e-3`) whenever I next touch `estimator.py` — a forward fix, not a reopen.

**Still deferred (do NOT build early — all correctly blocked):**
- The **learned attribution head** (`TemporalAttributionNet`) and **RMA latent** (`RMALatentEncoder`): need the frozen config, confirmatory data, and a GPU-verified PyTorch (sm_120) install, at that point — not before.
- The **§D deployable-loader leakage test** and the whole-trajectory/fault-setting split audit: need real multi-run storage to bite on.
- The **evaluation driver** that slices `[t_c, t_c+5 s]` and runs the paired C1-vs-S control comparison: needs the frozen data layout.
- A committed **end-to-end closed-loop seam test** (fixed-attribution stand-in driving active compensation on the real plant through `run_online_rollout`): proposed to Codex; I'll build it as a shared test next session if we agree it's worth having before the trained head exists.

**Config freeze remains a firm NO on a partial file.** Open freeze items: validation-sized healthy threshold calibration (≥~100 values — the rung's fail-loud guard now enforces this floor), severity/onset grids, joint sanity-check of non-load-bearing sensor constants, validation-frozen class/abstention/selective/OOD thresholds, contact-enabled cases, and `W`/`stride` (768/16 is pilot-advanced, still not frozen).
