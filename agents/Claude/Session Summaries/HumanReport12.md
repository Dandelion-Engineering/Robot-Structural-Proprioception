# Human Report 12 — Claude

**Current Date and Time:** 2026-07-20 12:08 PDT

**Agent:** Claude · **Session:** 12 · **Project phase:** Phase 2 — Execution

---

## Summary

This session did two things: it **reviewed and approved Codex's noisy-reference pilot** (closing that review loop after independent reproduction), and it **built the permanent "coefficient-distance-to-reference" detection rung** in my estimator lane — the deployable instrument the pilot was settling the convention for — then handed that increment back to Codex for review.

Plain-language framing of what the pilot and rung are about: the whole experiment turns on whether a few strain gauges let the arm tell that its *structure* has changed (a link gone soft) apart from an *actuator* weakening or a *sensor* lying. Codex's pilot (last session) showed, on realistic noisy sensor data, that a detector "tuning in" to the known probe frequency and comparing the live reading to a healthy baseline can separate a faulted body from a healthy one — and that a specific probe/window setting (a gentle 0.05 N one-cycle probe, a 768-sample window) does it with very few false alarms. My job this session was to (a) check that result honestly and (b) build the actual detector into the estimator so the number the pilot measured is the number the deployed detector will compute.

Everything remains development scaffolding: **no configuration is frozen, and the central research question is still open.** Full packet test suite went from 107 to **113 passing**.

## What was accomplished

1. **Completed the AgentPrompt startup and context-first chat pass.** Re-read `Project Details/Project Details.md` and `AgentPrompt.md` in full, my `Summary of Only Necessary Context.md`, all three concluded-chat `Summary.md` files, and the complete active Phase-2 transcript. Read the `Playbooks/review-cycle.md` and `Playbooks/live-run-readme.md` playbooks before doing the work they govern.

2. **Cross-review of Codex's most recent work.** Read Codex's Human Report 11 and the exact current repository state (the pilot script, its tests, both result directories, and the runbook/public wording).

3. **Independently reproduced the pilot's load-bearing properties** with a fresh script (`s12_reproduce_pilot.py`, in the session scratchpad — not committed), exercising Codex's pilot functions directly on the advancing cell rather than re-running the committed grid:
   - **Projected C1 == native C1, bit-for-bit** across all 18 channels (values, valid masks, measurement/availability times, latency ages, suite masks) — the no-gauge-leak / common-random-number guarantee that makes the efficient "generate S once, project C1" trick a genuine matched comparison.
   - **W=512 coefficient vectors are identically zero** — the required inert negative control (a sub-cycle window cannot resolve the probe).
   - **The S-vs-C1 advantage reproduces and is specifically the structural fault.** Suite C1 detected the actuator and sensor faults (they live in channels C1 has — motion, encoder) but detected the *structural* fault at **0.0%**, while the structural-sensing suite S detected it (~92% at my small 8-seed setting; Codex's 32-seed follow-up got 97.9%). So "C1 minimum fault detection 0%" means: the gauges add exactly the structural-deformation observability the conventional suite lacks. This sharpens the eventual S-vs-C1 story — the detection advantage is concentrated on the structural fault, not spread evenly.
   - **The BLOCK pathology reproduces** — with only 8 calibration seeds, S false alarms were 0.333, the same undersized-tail failure Codex's broad sweep preserved as a BLOCK.

4. **Approved the pilot at Codex's handed-off state** (script, tests, both result directories, runbook/public wording). The pilot review loop is **closed** (both agents explicitly approved the same state).

5. **Built the permanent `CoefficientReferenceDetector` rung** in `Reproducibility Packet/scripts/utils/estimator.py` (my lane). It scores the **joint** healthy-standardized coefficient distance of a live window to a healthy calibration reference — the deployable analog of Codex's clean mechanics safe-probe screen. Design choices, each traceable to a standard or a prior decision:
   - **It uses the coefficients jointly** (the whole cosine/sine vector, standardized and compared as one distance), which is exactly the gap I flagged in Session 11: the existing novelty detector consumed the coefficients only as generic independent per-feature scores, which is not the screen's statistic.
   - **It is a detection rung, not attribution.** It abstains on the fault *type* and spreads non-healthy probability uniformly — the same honesty bound the project has held throughout (naming which fault it is needs the trained head reading differential shape/phase across the four gauge stations). Codex's pilot-side nearest-centroid attribution is a pilot instrument; I deliberately did not reproduce it as a deployed diagnosis.
   - **The threshold is frozen on healthy calibration, never on the held-out set**, and `calibrate_threshold` **fails loud** when the calibration set is too small to resolve the requested false-alarm tail (it needs at least `ceil(min_tail_count / false_alarm_rate)` values — ≥100 at a 5% tail). This turns the pilot's central finding (a small calibration set cannot resolve a low false-alarm tail; its "99th percentile" is merely the calibration maximum) into a hard, enforced precondition, so the deployed rung structurally cannot freeze an unresolved threshold.

6. **Added a coherence test** (`test_coefficient_statistic_matches_pilot_definition`) asserting my `synchronous_coefficient_vector` is bit-equal to the pilot's and my `coefficient_reference_distance` equals the pilot's `coefficient_distance` on the same window. This pins the Session-10-to-12 claim that the deployed detector's margin *is* the pilot's margin — the excitation → detector → estimator chain now closes on a single statistic (amplitude → coefficient pair → joint coefficient distance).

7. **Moved the estimator-side window proposal `RECOMMENDED_WINDOW` from W=640/stride=8 to W=768/stride=16**, with a rationale citing Codex's follow-up (the only suite-S cell clearing the ≤5% worst-alignment held-out false-alarm screen; 97.9% detection; 100% attribution; 0% matched-C1) and keeping the honesty loud: still a pilot proposal, the false-alarm margins are single-event-thin at 48 held-out seeds, and a validation-sized healthy calibration set owns the frozen W/stride/threshold. I confirmed this default-window change is inert for the existing detector tests (per-column statistics are computed over valid samples only; the padding-length-dependent `valid_fraction` is constant across equal-length records, so its standardized contribution is ~0).

8. **Handed the estimator increment back to Codex for genuine review** (opening a new review loop), with my explicit approval of the state, in the active Phase-2 chat.

9. **Verification:** full packet suite **113 passed** (107 handed off + 6 new estimator tests); `compileall` clean over the packet scripts; `git diff --check` clean apart from LF→CRLF line-ending warnings. Only `estimator.py` and `test_estimator.py` changed in the packet.

10. **Live-run heartbeat check performed** — the public README's last entry (2026-07-20) already told the public the reference convention advanced with W=768/stride=16; this session is the estimator-side implementation of that convention plus a review-loop closure, i.e. development scaffolding, not a finished artifact, phase close, or new public result. Per the lean-by-design standard I left the README untouched.

## Important decisions and reasoning

- **Approve the pilot rather than edit it.** The pilot is correct and honest, and its threshold is explicitly non-frozen and validation-owned everywhere it matters. Two things I might have edited I instead carried forward as notes (below), because the project's discipline is that corrections to already-sound work propagate forward, not by reopening the reviewed artifact for wording symmetry.

- **Two forward points, not blocking edits.**
  - *(a) Threshold-resolution caveat.* Codex's BLOCK report states plainly that below ~100 calibration values the "99th-percentile" threshold is just the calibration maximum. That is still true in the advancing follow-up (at 32 calibration seeds the 99th percentile lands on the maximum), so its 0.7%/2.1% false-alarm figures rest on a max-based threshold with single-event (1/48) resolution. Not a defect — but the advancing report omits the caveat the blocked one includes, and they should read symmetrically; the real fix is a ≥~100-value healthy calibration at validation. I turned this into the hard guard in my rung, so the lesson is enforced, not merely noted.
  - *(b) Record the base seed in the artifact.* The follow-up's `summary.json` grid records window/stride/onset/seed *counts* but not the base seed (5000), which lives only in the human report and runbook. For the packet's self-contained-reproducibility standard, the grid should carry the seed. Small nit in Codex's lane, a forward fix.

- **Detection-only, not attribution, in the deployed rung.** Reproducing the pilot's nearest-centroid attribution as a deployed diagnosis would present a non-learned heuristic as if it were the attribution answer. The honest deployed rung detects and abstains on type; attribution is the trained head's job, post-freeze. This keeps the standing honesty bound intact.

- **Encode the pilot's lesson as a precondition.** Rather than trust callers to use a large enough calibration set, `calibrate_threshold` refuses to freeze a threshold the calibration size can't resolve. This is the software-engineering "fail loud" standard applied to the exact failure the pilot discovered.

## Challenges and how they were handled

- **Judging whether to move `RECOMMENDED_WINDOW`.** The follow-up's false-alarm margins are single-event-thin, so moving my standing proposal risked overstating. I checked the follow-up's aggregate directly: with the 32-seed calibration, W=768/stride=16 is the *only* suite-S cell that clears the ≤5% worst-alignment screen (every W=640 cell fails it), and it has the best attribution — so within the pilot's controlled sweep the move is evidence-backed, not a coin-flip. I made the move but kept the thinness explicit in the rationale and deferred the frozen choice to validation.

- **Avoiding a duplicate statistic.** The pilot script carries its own copies of the coefficient-vector and distance functions. The natural canonical home is the estimator library the pilot imports, so I put the functions there and pinned equality with a test, but did not reach into Codex's pilot to re-point it (forward-propagation discipline); I flagged the dedup as a future forward fix in Codex's lane.

## Files created

- `agents/Claude/Session Summaries/HumanReport12.md` (this report)
- (scratchpad, not committed) `s12_reproduce_pilot.py` — the independent pilot reproduction

## Files updated

- `Reproducibility Packet/scripts/utils/estimator.py` — new `CoefficientReferenceDetector` rung + shared `synchronous_coefficient_vector` / `coefficient_reference_distance` helpers; `RECOMMENDED_WINDOW` → W=768/stride=16 with pilot-cited rationale; capacity-ladder docstring updated.
- `Reproducibility Packet/tests/test_estimator.py` — 6 new tests (coherence with the pilot statistic, healthy-low/change-high, the calibration fail-loud guard, detection-only/abstain-on-type, persistence latch, reference/threshold preconditions); imports and one stale comment updated.
- `chats/Claude-Codex/Phase 2 Integration and Config Freeze/Phase 2 Integration and Config Freeze - Active.md` — my Session-12 review turn (appended at the physical tail).
- `agents/Claude/README.md` — estimator-lane entry, packet test count, and Session-12 activity.
- `agents/Claude/Summary of Only Necessary Context.md` — fully rewritten for Session 13.

`agents/Claude/references.md` is unchanged — this was a review-plus-implementation session against already-cited methods; no new external source informed it. `requirements.txt` is unchanged (no new dependency; PyTorch still not installed, correctly, until the learned rungs).

## Verification performed

- Independent pilot reproduction: projected-C1 == native-C1 bit-for-bit; W=512 coefficients all-zero; S detects the structural fault where C1 is at 0%; undersized-calibration BLOCK pathology reproduced.
- Estimator-only tests: **29 passed**.
- Full packet suite: **113 passed** (was 107).
- `compileall` over packet scripts: clean.
- `git diff --check`: clean apart from LF→CRLF warnings.
- Active-chat tail: my Session-12 header appears exactly once and the transcript ends with my signature.

## Next steps / pending actions

1. **Codex reviews my estimator increment.** The `CoefficientReferenceDetector` + `RECOMMENDED_WINDOW` move is handed off with my explicit approval; the loop is open. If Codex edits my files, I close it next session with a genuine owner re-review.
2. **Validation-sized threshold calibration** now has a concrete home: my rung's guard refuses any calibration set too small to resolve the target false-alarm tail. Establishing that ≥~100-value healthy calibration (with severity/onset grids and frozen class/abstention/selective/OOD thresholds, on data disjoint from the pilot's held-out rows) is a shared freeze gate.
3. **Codex's plant lane:** the interpretable residual/linear-system-ID baseline and the recovery controller that plugs into `EstimatorCommandPolicy`; MuJoCo endpoint-contact extraction before any optional-contact pilot.
4. **The learned rungs** (`TemporalAttributionNet` headline + `RMALatentEncoder`) remain post-freeze: they need the CUDA PyTorch build (GPU-verified sm_120), installed at that point, and frozen confirmatory data — building untrained shells now would be fabrication.
5. **Shared freeze gates** unchanged: non-load-bearing sensor constants sanity-check; severity/onset grids; contact-enabled cases; then freeze/hash the full schema/config before confirmatory generation. `config.json` stays deliberately unfrozen.

My next regular director progress report remains **Session 16**; this session closed no phase and approved no Claim-Sheet amendment (the pilot convention and the window move are schema/config-adjacent development choices, not amendments to the Claim-Sheet contract), so no progress-report trigger fired.
