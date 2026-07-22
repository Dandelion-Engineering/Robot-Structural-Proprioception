# Human Report 18 — Claude

**Current Date and Time:** 2026-07-21 21:17 PDT

**Agent:** Claude · **Session:** 18 · **Project phase:** Phase 2 — Execution

---

## Summary

This was a pure cross-review session, the mirror image of my Session 17. Last session I reviewed Codex's *matched contact pilot* (which blocked on all three of its gates) and left two forward notes for the redesign the block required. This session Codex had built that redesign — a **bounded task/contact/controller screen** — and handed it to me for genuine first review. My whole session was that review, done the way I've done every review this phase: by reproducing the result independently rather than re-running Codex's code, then approving the exact state or handing back edits.

**Outcome: I found no defect. I reproduced the advancement decision independently — driving the physics myself and recomputing every gated number with my own logic — confirmed the three result artifacts are byte-for-byte deterministic, and explicitly approved Codex's exact handed-off state, closing the review loop.** I also left two non-blocking forward notes for the next gate. Nothing was frozen; the central research question remains open; `config.json` stays unfrozen.

### What the redesign did (and I confirmed)

Codex's Session-16 matched pilot failed for three reasons I confirmed last session: the detector tripped too often on healthy runs, a one-shot diagnosis drifted when reused continuously, and the arm's *perpetual open-loop* task swung a joint past its safety limit over the required five-second horizon. Codex's redesign this session takes my two forward notes as its design contract and fixes the mechanics:

1. **The perpetual open-loop task is replaced by a bounded, finite, closed-loop task.** A low-authority PD controller — reading only the robot's *delivered* encoder position/velocity, never privileged truth — follows a smooth finite excursion (rest → a modest joint target → hold → back to rest) that completes inside the horizon. This directly answers my forward note #2: the joint-angle violation was a property of the runaway open-loop task, not the contact, so the fix is a stabilized trajectory. With the bounded task, the worst joint angle is ≈0.36 rad, versus the π-radian limit — an enormous margin where before it was blowing past the limit for a thousand-plus steps.
2. **The diagnosis is made once, after the probe, and held.** This removes the Session-16 drift (a diagnosis fitted for one probe phase, wrongly reused as the probe slid out of the window).
3. **Contact happens only after the diagnosis, under controller authority.** The single held decision lands at 2.272 s; the contact excursion begins at 2.400 s. This answers my forward note #1: for the eventual "does structural sensing improve control" comparison to even be *able* to show a safety advantage, the diagnosis has to land before — and the controller must have authority over — the safety-relevant contact window.

Codex then ran a predeclared five-plane screen (contact plane heights from 0.100 to 0.200 m) across all four development sources (healthy, structural fault, actuator fault, sensor fault) and selected **z = 0.200 m** as the lowest plane where *every* source produces exactly one brief, bounded, safe contact episode after the decision — with **z = 0.100 m** as the all-source no-contact control. Every selected-plane arm clears all seven unchanged safety limits over the full five-second horizon, with peak contact forces of 0.5–2.1 N (limit 5 N).

**The honest boundary, which the artifact states everywhere:** the diagnoses in this screen are *fixed, source-correct stand-ins* — a mechanism instrument, not a trained estimator. So this establishes only that the bounded controller/contact/lifecycle *seam* can safely express source-specific action before contact. It does **not** show that a real estimator can supply those diagnoses, that structural sensing supplies better ones than conventional sensing, or that recovery improves tracking. Those remain the open questions.

### How I verified it independently

I wrote my own reproduction harness (outside the packet) that drove the real physics myself and recomputed every gated quantity with independent logic, then diffed against Codex's committed numbers. **Zero mismatches.**

- **The causal ordering reproduced from scratch.** I recomputed, from the raw timing, that the probe completes and the single decision lands at step 1136 = 2.272 s (and that this step falls exactly on the estimator's decision cadence, so the one evaluation lands precisely on schedule), that the audit runs the full 3000 steps = 6.0 s = onset + 5 s, and that the decision precedes the contact motion.
- **The safety result reproduced independently.** For the selected plane and the no-contact control across all four sources, I recomputed six of the seven safety flags directly from the raw ground-truth signals (joint angle, joint speed, gauge strain, contact force) — the joint-angle flag being exactly the one that blocked Session 16 — and confirmed every one is zero, with large margins. The seventh (a 3-D workspace-radius flag the simulator computes from data the saved record doesn't fully expose) I confirmed via the simulator's own flag column, with the full seven-flag audit reading zero in every arm.
- **The contact and recovery mechanics reproduced.** One bounded episode per arm at the selected plane; peak forces matching to a fraction of a newton; the source-specific recovery action beginning at the decision and therefore *before* contact for the fault arms; and the healthy/sensor arms leaving their command untouched — the changed-step counts matching bit-for-bit (1864 / 1863 / 0).
- **The decision and the plane bracket reproduced.** I re-ran Codex's selection logic on the committed rows and independently counted which sources contact at each plane; both gave the reported answer (advance z = 0.200 m; the bracket opening monotonically from no contact at 0.100 to all-four at 0.200).
- **Determinism.** I regenerated the entire twenty-arm screen to a scratch directory; all three artifacts were SHA-256 identical to the committed ones, and equal to the hashes Codex reported.
- **Tests.** The full Reproducibility Packet suite is **155 passed** on my machine.

## Challenges and how they were overcome

**My first reproduction pass tripped on a bug in my own harness — not the artifact.** I tried to cross-check the 3-D workspace-radius safety flag by reconstructing the tip radius from the saved planar tip position, but that saved field is a 2-D task-space coordinate while the simulator computes the flag from the true 3-D tip position (which the record doesn't store), so my reconstruction was in the wrong coordinate frame and read a false 1.12 m against the 0.82 m limit. I diagnosed it, dropped that mis-framed check, and relied on the six flags I *can* recompute cleanly from raw truth plus the simulator's own column for the seventh. This is the same category of lesson as my Session-17 `pair_id` note: when an independent reproduction disagrees, the first suspect is my own harness, and the decisive checks are the ones computed directly from unambiguous raw data plus the byte-identical regeneration. I record it because honesty about where a discrepancy came from is the whole point of an independent review.

**Keeping the review genuinely independent.** As last session, the temptation is to re-run the author's script and check it doesn't crash — which is not a review. I drove the plant with my own code, recomputed the metrics and the pass/fail decision with my own logic, and recomputed the safety flags from raw ground truth, so that agreement means two independent computations landed on the same answer.

## Important decisions and reasoning

- **Same-state approval, no edits.** The code is correct and cleanly fenced (the task controller structurally cannot read privileged state; the recovery composition copies its input so it can't mutate the caller's command; the single-decision lifecycle evaluates exactly once and holds), the tests are targeted and pass, the results are deterministic, and the wording — report, packet runbook, public status log — matches the numbers and calls this a development mechanics/lifecycle advance rather than a research result. There was nothing to fix, so I explicitly approved the exact state Codex handed me and the loop is closed.
- **Two forward notes instead of edits.** Corrections in this project propagate *forward* into the next piece of work, not by reopening finished work, so I recorded two observations for the next gate rather than changing Codex's artifact (below).
- **Left the public status page untouched.** Codex already logged this bounded-redesign advancement in the public Live-Run README during its Session 17. My session confirmed it; a confirming internal review is not itself a new public-facing event, so a second entry would only add noise to a log that is lean by design. (Same call I made in Sessions 15, 16, and 17.)
- **No progress report this session.** My next scheduled director progress report is Session 24; this session closed no phase and approved no amendment to the contract, so no report was triggered.

## Reasoning paths and insights

The two forward notes are the session's substantive contribution beyond confirming the advance. Both continue the thread of my Session-17 note #1 — they don't change this artifact, they shape the next one:

1. **Recovery now *precedes* the contact window, but this screen doesn't yet let it *change* the outcome.** Every arm lands in the same place — one bounded episode, forces under 5 N, zero safety flags — whether it applies a source-specific recovery (the fault arms) or leaves the command untouched (healthy). So the seam can now *express* source-specific action early, which was the missing prerequisite, but a correct diagnosis isn't yet *needed* for the safety outcome. For the eventual conventional-vs-structural comparison to be *able* to show a control or safety advantage, the task/contact condition has to be designed with enough dynamic range that the wrong-or-absent diagnosis produces a measurably worse outcome than the correct one — otherwise even a perfect structural diagnosis would score the same as conventional sensing's blindness. Worth building that sensitivity in deliberately rather than discovering its absence at the comparison.
2. **The "recovery precedes contact" property depends on the held decision being confident *and* correct — which a real noisy estimator won't always be.** The screen's fixed stand-ins are always right and always confident. The controller's action gate only fires when the estimate is unambiguous and low-uncertainty, so once the stand-in is replaced by a real estimator on noisy observations, it will sometimes withhold action or act on the wrong location. The next gate should therefore report not just detection/attribution accuracy but the *rate at which the action gate fires appropriately* at the single held decision — because that firing behavior, not classification accuracy alone, is what determines whether the safe-mechanics property Codex just established survives real information.

The broader picture, unchanged and reinforced: the project's honest bottleneck is no longer *detecting* the structural signal (that keeps showing up cleanly) — it is embedding that signal in a **safe, stable, closed-loop experiment whose result we could trust**. Last session's review pinned the two reasons the previous attempt wasn't that; this session's review confirms the mechanics of a version that *is* safe and stable, and my forward notes now point at the next requirement: making the experiment one where a correct diagnosis actually *matters* to the measured outcome.

## Files created or updated during the session

**Created:**
- `agents/Claude/Session Summaries/HumanReport18.md` (this report)

**Updated:**
- `chats/Claude-Codex/Phase 2 Integration and Config Freeze/Phase 2 Integration and Config Freeze - Active.md` — appended my Session-18 same-state review approval (loop closed) plus two forward notes, under the append-only transcript hard gate (verified: my header appears once at line 1190, after Codex's handoff at line 1186, physically last; file grew 1186 → 1227 lines).
- `agents/Claude/README.md` — recorded the Session-18 review-loop closure and the 155-test packet count.
- `agents/Claude/Summary of Only Necessary Context.md` — completely rewritten for Session 19.

**Reviewed but deliberately not changed** (Codex's Session-17 artifact, approved as-is): `Reproducibility Packet/scripts/utils/task_control.py`, `Reproducibility Packet/scripts/utils/recovery_control.py` (the `command_from_nominal` extension), `Reproducibility Packet/scripts/screen_bounded_task_contact.py`, `Reproducibility Packet/tests/test_bounded_task_contact.py`, the two new tests in `Reproducibility Packet/tests/test_recovery_control.py`, `Reproducibility Packet/scripts/utils/__init__.py`, `Reproducibility Packet/results/bounded_task_contact_screen/` (summary.json + rows CSV + report), `Reproducibility Packet/README.md` (new Step 11 + renumbered Steps 12–15), and the root `README.md` (Live-Run advancement entry).

No new external sources were read (a review/reproduction session), so `agents/Claude/references.md` was not changed. No `.gitignore` change is required — the session touched only markdown documentation and a chat transcript; my reproduction scripts and scratch outputs live in the session scratchpad outside the repository.

## Verification performed

- Independent reproduction of the advancement decision (my own plant drive + metric recompute across the negative-control and selected planes for all four sources): **zero mismatches** after the harness fix — causal arithmetic, no-contact control, one-episode selected plane, all safety flags zero (six recomputed from raw truth, the seventh confirmed via the simulator column), recovery-before-contact and changed-step counts, and the selection decision and plane bracket.
- Byte-for-byte determinism: all three committed artifacts regenerated SHA-256 identical, equal to Codex's reported hashes.
- Full Reproducibility Packet test suite: **155 passed**.
- `summary.json` scanned: no NaN/Infinity tokens.
- Packet runbook step numbering: consistent (Steps 1–15), cross-reference to Step 14 updated.
- Chat append hard gate: pre-write 1186 lines; my header once at line 1190, after Codex's handoff (line 1186), physically last; post-write 1227 lines.

## Next steps / pending actions

1. **Codex's next increment (its lane):** the **matched noisy held-decision conventional-vs-structural information / reference-lifecycle review** on this exact bounded-mechanics condition — replacing the fixed source-correct stand-ins with a real noisy estimator making one declared held decision on matched (common-random-number) conventional/structural pairs with disjoint calibration/evaluation roles. My two forward notes feed its design directly.
2. **My lane (still post-config-freeze, do not build early):** the learned attribution head + the RMA latent (need a GPU PyTorch build + frozen config + confirmatory data); the leakage test and whole-trajectory split audit (need real multi-run storage); the evaluation driver that slices the five-second post-change window for the paired comparison (needs the frozen data layout). On my next touch of the estimator I will fold in the carried `null_std` floor-consistency nit.
3. **Config freeze remains the gate.** Still open before any confirmatory data: the matched noisy information/lifecycle review, validation-sized healthy/four-class calibration (with per-suite probability calibration), severity/onset grids, non-load-bearing sensor constants, class/abstention/selective/OOD thresholds, the reference-lifecycle choice (single held decision vs. a temporal model), and the split/leakage/storage/hash audits. The selected z = 0.200 m plane, the PD gains/limits, and the task timing are development candidates, not frozen margins.
4. **No progress report due until my Session 24**, unless a phase closes or a contract amendment is approved before then.

The central research question — whether distributed structural sensing gives a real adaptive-control advantage — remains open. This session confirmed, independently, that the bounded controller/contact/lifecycle seam can safely express one source-specific action before contact for every development source, and pinned the next requirement: an experiment in which a correct diagnosis measurably changes the outcome, supplied by a real estimator rather than a stand-in.
