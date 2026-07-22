# Summary of Only Necessary Context — Claude

*Rewritten every session. Restores my working context for the next session. Excludes anything already in `Project Details/Project Details.md` and `AgentPrompt.md` (I re-read those in full at session start). Last rewritten: end of Session 21, 2026-07-22 16:51 PDT.*

## Where the project is

- **Phase 2 (Execution) is OPEN.** All Phase-1 gates closed and in force. **Schema v1.0 + Amendment A1 (contact/safety roles) are jointly in force.** Contract changes run through the **amendment protocol**, not casual editing.
- I am **Claude**; last session was **Session 21**; next session I run is **Session 22**.
- **Next regular director progress report: my Session 24.** (Phase-0-close, Phase-1-close, Session-8, Session-16 reports exist. S17–S21 closed no phase and wrote no Claim-Sheet amendment → no trigger. S22–S23 need NO progress report unless a phase closes or a Claim-Sheet amendment is approved.)
- **`config.json` is deliberately NOT frozen.** Current role hashes are `dev-`; no `dev-` trace may enter confirmatory analysis.
- **Packet: 199 tests green** (198 from Codex's S20 deficit screen; +1 from my S21 units regression).

## Review-cycle state (READ THIS FIRST next session)

- **My S20 loop is CLOSED** — Codex genuinely owner-re-reviewed my four edits to the structural-action screen and **explicitly approved my exact handed-back state** (its S20 turn, restated at the physical tail at 15:29 PDT). Done; do not reopen.
- **ONE REVIEW LOOP IS OPEN, AND IT IS MINE TO HAVE HANDED BACK.** In S21 I first-reviewed Codex's S20 **per-class fault tracking-deficit screen** and **did not approve same-state. I edited and handed back.** Codex must now genuinely owner-re-review my edits and either approve that same state or edit and hand back.
  - **My edits (all in Codex's lane, all in review):**
    1. `scripts/screen_fault_tracking_deficit.py` — **the headroom gate converted the Claim Sheet's target into the wrong units.** The bar is a *reduction* against the degraded arm (`100·(J_C1−J_S)/J_C1`); the screen measures a *deficit* against the healthy arm (`100·(J_fault−J_healthy)/J_healthy`). An exact restoration turns deficit `D` into reduction `D/(1+D)`, so a 12% deficit gate admits only a **10.714%** reduction — 0.714 of the declared 2 margin points survive. Split into `required_reduction_pct` (= predeclared bar+margin = 12%) and `required_deficit_pct` (= `R/(1−R)` = **13.636%**), plus a `validate()` guard. Both are pure functions of predeclared constants; the fix **tightens** the gate.
    2. Same file — `_ceiling_reduction_pct()` + `_scope_lines()`, a **generated** report section ("What the recorded headroom does and does not license"), every figure recomputed from the recorded rows so it regenerates deterministically. Four bullets: headroom is a ceiling (18.81%/18.72% for the advancing setting); reduction beyond the ceiling is command authority, already blocked once; the strain-vs-deficit contrast; no-action headroom ≠ S-over-C1 headroom.
    3. `tests/test_fault_tracking_deficit.py` — `test_headroom_gate_converts_the_reduction_target_into_deficit_units` + the two fixtures that encoded the old 12% (15 → 16 tests).
    4. `Reproducibility Packet/README.md` Step 14 — two added paragraphs (the conversion; the two bounds) + the Current-boundary rewrite.
  - **Effect:** tuning selection moves `actuator_gain_remaining_0p50` → **`actuator_gain_remaining_0p25`** (tuning min 13.108% < 13.636% ≤ 22.974%); assessment re-passes at 23.16%/23.03%. **Overall decision string UNCHANGED:** `ADVANCE_ACTUATOR_DEFICIT_ONLY_BLOCK_STRUCTURAL_DEFICIT`. Structure blocks everywhere.
  - **Verification of the edits:** full 84-arm re-run at 10 workers (Codex used 8) → `tuning_rows.csv` `bfe0eb66…` and `assessment_rows.csv` `7cfcc104…` **byte-identical to Codex's**. Only the three derived artifacts move: `summary.json` `dbbc44a8…`→`ed265cfb…`, `candidate_summary.csv` `624a1a4e…`→`a7e2998d…`, report `e4c7df4e…`→`c2924e5d…`. New report regenerates deterministically from the new `summary.json`.
  - **I stated the fair counter-argument in the handoff:** 12% was predeclared, and post-hoc gate changes are exactly what the project is disciplined against. My answer: the predeclaration is in *reduction* units and the code never converted; no observed value enters the fix. **If Codex prefers to keep the recorded 0.50 selection with the conversion merely reported, that is a legitimate resolution** — §4 of my turn shows the empirical difference between the two selections is nil. Escalate to Randy if a specific point hasn't converged in ~2 round-trips.
- **My S21 chat turn is the physical tail** of the active Phase-2 chat (posted 2026-07-22 16:48 PDT; file 1562 → **1673 lines**; my header at line 1566, appears once, physically last). Anchored on Codex's unique multi-line tail; re-verified after the write.
- **MONITORING DUTY IS STANDING, AND IT FIRED IN S20/S21.** Codex's S20 approval landed mid-file at line 1,331; Codex's own verifier caught it and appended a dated correction at the true tail. I verified at the git level: **+72 / −0 lines**, so nothing was deleted, moved, or rewritten. I logged it for Randy in the **new** chat `chats/Claude-Codex-Human/Transcript Order Monitoring/` (Active), stating no action is needed from him. Keep watching; keep anchoring appends on the unique multi-line physical tail and re-verifying after the write.

## THE HEADLINE OF S21 — carry this into everything

**I ran the recovery action the deficit screen advances toward. The advanced condition does not survive it.** Assessment seeds, my own drive, the already-approved inverse-gain path in `recovery_control.py`, with an **oracle-severity** diagnosis (the action family's ceiling) plus a healthy false-authorization arm at the same multiplier:

| condition | no-action deficit | ceiling reduction | **achieved reduction** | healthy false-auth | **source-specific margin** |
|---|---:|---:|---:|---:|---:|
| actuator 0.50 (Codex's selection) | 13.20% | 11.66% | **10.77%** | 6.11% | **+4.67 pp** |
| actuator 0.25 (corrected selection) | 23.16% | 18.80% | **10.82%** | 6.11% | **+4.71 pp** |
| actuator 0.10 | 65.73% | 39.66% | **3.10%** | 6.11% | **−3.01 pp** |

- **The units error was about to be load-bearing:** on Codex's selection the best possible next-screen outcome is 10.77% vs a 10% bar — **+0.77 pp**, with a perfect diagnosis.
- **Correcting the units does NOT rescue the advance.** The corrected selection delivers the same ~10.8%, because `maximum_gain_compensation = 2.0` caps the multiplier: at 0.25 remaining gain the action applies 2× against a 4× loss, landing at the 0.50-equivalent point (**+9.83%** residual gap to healthy). At 0.10 the cap is so short the action is worth *less* on the faulted arm than on a healthy one.
- **⇒ Deficit is not the binding variable.** The binding variable is the **achievable source-specific reduction**, set jointly by deficit × action family × cap × severity-estimation quality. A deficit gate sees one of four.
- **The specificity standard that blocked the structural family costs the actuator family more than half its benefit:** the same 2× multiplier on a *healthy* plant improves healthy tracking **6.11%**, so only **+4.67 pp** is source-specific — stable to ±0.1 pp across 4 seeds (unlike the structural margin, which sign-flipped), and **less than half the bar**.
- **With the screen's own `FixedSourceStandIn` (severity pinned 0.70) on the 0.50 condition, the action yields only 6.27%** — below the bar. Severity-estimation quality may be the largest unmeasured term.
- **The action is not free on the axis we cannot score:** peak contact force 1.518 → 1.805 N (0.50) and 0.081 → **0.895 N** (0.25, an 11× rise); `safety_incident_rate` scores all of it zero. Third time this blind spot has been relevant (S19 derate, S20 structural action, S21 actuator action).

## THE SHAPE OF THE CONTROL LAYER (recorded, not inferred)

From Codex's committed `bounded_noisy_information_review/summary.json` — the four representative S-vs-C1 pairs:

| source | C1 gate state | S gate state | suite-informed | `s_tracking_change_pct` |
|---|---|---|---|---:|
| healthy | correct_no_action | correct_no_action | no | 0.0000% |
| **structure** | withheld_actionable_fault | correct_actionable | **yes** | **−18.5762%** |
| **actuator** | correct_actionable | correct_actionable | no | **0.0000%** |
| **sensor** | correct_no_action | correct_no_action | no | **0.0000%** |

C1 per-class recall there: structure **0.083**, actuator **1.000**, sensor **1.000** (S: 1.000 on all three).

**⇒ Where S has exclusive information there is no control headroom; where there is control headroom S has no exclusive information.** The contract's paired control quantity is *already* exactly zero on the two classes with headroom. **Any future control-layer plan must answer this table first.**

## The other S21 finding — the strongest version of the structural result

Two columns from Codex's own 84 rows, never previously put side by side (now in the generated report):

| remaining EI | mean peak \|gauge\| | mean tracking deficit |
|---:|---:|---:|
| healthy | 19.2 µε | — |
| 0.75 | 25.0 µε | +0.11% |
| 0.50 | 38.4 µε | +0.08% |
| 0.25 | 72.4 µε | −0.89% |
| 0.10 | 152.8 µε | −2.23% |
| 0.05 | 259.7 µε | −5.00% |

**Monotone in information; monotone the wrong way in control.** 13.5× the healthy strain signature at the severity where tracking is 5% *better* than healthy. This is the Slot-13 diagnostic-only shape measured across a 15× stiffness sweep, not inferred from one setting. **This is the sentence the write-up gets built on.**

Caveat to carry: the mechanics are held fixed but the *interaction* is not comparable across the grid — peak contact force runs 2.11 N (healthy) → 1.52 (act 0.50) → **0.08** (act 0.25) → 1.52 (act 0.10). At the corrected selection the arm barely touches the plane.

## Reproduction results (S21, for the record)

- **42/42 checks, zero mismatches** against Codex's artifacts (scratchpad `s21_deficit_audit.py`: paired deficits, all three per-case gates, both sensor-control summaries, mildest-selection, decision string, JSON↔CSV, no NaN/Inf, all 10 report grid rows, all 84 raw rows' lifecycle/A1/saturation/contact, CRN one-hash-per-(role,seed), Codex's quoted worst values). **42/42 again** against my regenerated artifacts.
- **36 arms of my own** (`s21_probe.py`, reusable): own case runner, own trapezoidal `J_5s` from §G → vs packet `j_5s()` **max abs diff 0.000e+00**. Reproduced deficits: act 0.50 **+13.2015/+13.1197**, act 0.25 **+23.1609/+23.0314**, str 0.05 **−5.0038/−5.0587**.
- Codex's report regenerates byte-for-byte from its own `summary.json` (`e4c7df4e…`). *(Note: `git show` applies CRLF conversion, so hash a working-tree file, not a `git show` stream.)*
- `compileall` clean; CLI help clean; `git diff --check` clean apart from expected CRLF warnings.

## The single most important things to do next session (Session 22)

1. **Check Codex's S21 turn** for its owner re-review of my four edits. If it approved the same state → loop closed, note it. If it edited and handed back → genuinely re-review its edits *and* its diagnosis (do not wave them through), then approve or edit again. Escalate a specific non-converged point to Randy after ~2 round-trips.
2. **Watch what Codex builds next, and hold it to the right gate.** I proposed the next gate be **achievable source-specific reduction**, screened directly (paired vs no-action *and* vs false-authorization on the same multiplier, credit only the margin, with real uncertainty). Three concrete steps I offered: (a) raise/remove `maximum_gain_compensation` for the screen only, to find out whether the cap or the physics binds; (b) screen under the *deployable noisy estimator's* severity output, not an oracle; (c) then decide honestly whether the control layer has a live path at all. **If Codex instead screens an actuator action on the advanced condition as-is, point at the table above:** the ceiling is ~10.8% total / ~4.7 pp source-specific, and the paired S−C1 quantity on that class is already recorded as 0.0000%.
3. **No progress report due S22** (next regular = S24; only a phase close or approved amendment adds one).
4. **When I next touch `estimator.py`** (the learned head): fold in the carried `null_std` floor consistency nit (`CoefficientReferenceDetector.update` floors at `_EPS` → make it `1e-3` to match `WindowNoveltyDetector`). Forward fix, not a reopen. *(Carried since S13.)*
5. **Deferred, still blocked (do NOT build early):**
   - The learned attribution rungs (`TemporalAttributionNet` headline + `RMALatentEncoder`) — need PyTorch CUDA build, GPU-verified sm_120, installed *at that point*; + frozen config + confirmatory data.
   - The §D deployable-loader leakage test + whole-trajectory/fault-setting split audit — need real multi-run storage.
   - The eval **driver** ([t_c, t_c+5 s] slicing → paired C1-vs-S control comparison) — needs the frozen data layout.

**Do NOT freeze a partial config.** Open freeze items: **the actuator action's `maximum_gain_compensation` cap (NEW, S21)**; **the severity-estimation quality term (NEW, S21 — unmeasured by any artifact)**; the actuator action screen itself; validation-sized healthy threshold calibration (≥~100 values) **with per-suite probability calibration**; the ambiguous-case fault library that makes abstention testable at all (my S19 note); severity/onset grids; joint sanity-check of non-load-bearing sensor constants; validation-frozen class/abstention/selective/OOD thresholds; the reference-lifecycle choice (single held decision vs. a temporal model over the full post-probe trajectory); the **bounded task/contact/controller profile** (`z=0.200 m` + PD gains `(0.05,0.03)`/`(0.005,0.003)` + torque limits `(0.20,0.10)` + timing are *dev candidates*, NOT frozen margins); `W`/stride (**768/16** pilot-advanced, still not frozen); split/leakage/storage/hash audits.

## My lanes — current state (reference for next builds)

`Reproducibility Packet/scripts/utils/estimator.py` (**stable, jointly approved through S13; UNCHANGED in S14–S21**):
- **Window front-end `WindowFeatureExtractor(window_steps=W=768, probe_frequency_hz=0.8)`**: fixed `[W,D]` left-padded tensor + per-column summary `[last, mean, std, slope, sync_cos, sync_sin, sync_amplitude, valid_fraction]`, suite-agnostic over the 18-col registry. Constants: `N_FEATURE_STATS=4`, `N_EXTRA_FEATURES=4`, `SYNC_COS_FEATURE_COL=4`, `SYNC_SIN_FEATURE_COL=5`, `SYNC_AMPLITUDE_FEATURE_COL=6`, `VALID_FRACTION_COL=7`, `DIAGNOSTIC_PROBE_HZ=0.8`, `MIN_SYNC_SAMPLES=8`.
- **`WindowNoveltyDetector`**: interpretable detect + calibrated-abstention; consumes cos/sin as per-feature z-scores; score std floored at `1e-3`. Latches `detection_time_s` after `persistence` consecutive over-threshold windows.
- **`CoefficientReferenceDetector`**: second interpretable detection rung; scores joint healthy-standardized coefficient distance `‖(coeff_live−mean)/scale‖/√D` (module-level `synchronous_coefficient_vector` + `coefficient_reference_distance`, the canonical statistic every pilot/screen imports). Detection-only, abstains on type. `fit_reference` atomic; on re-fit invalidates threshold + resets latch. `calibrate_threshold` FAILS LOUD below `ceil(min_tail/far)` (≥100 at far=0.05). **NIT to fold in next estimator touch:** `update`'s `unknown_score=z` floors `null_std` at `_EPS` → float to `1e-3`.
- **`synchronous_coefficient_vector` drops masked channels physically** (C1's vector is genuinely shorter than S's, not zero-padded); each suite's reference is fit on its own dimension; `/√D` puts suites on one comparable scale — **empirically confirmed S19** (thresholds 1.281 vs 1.263).
- **`OracleInterface(onset_time_s)`**: allowlisted privileged ceiling, causal. **`EstimatorCommandPolicy`**: the `run_online_rollout` `CommandPolicy` adapter (diagnosis→control socket; runs estimator every `stride`, **ZOHs the estimator OUTPUT but calls `recovery_command` EVERY step**). Calls `estimator.reset()` at construction.
- **`RECOMMENDED_WINDOW` = (W=768, stride=16)** — pilot-advanced, still a pilot proposal.
- **Learned rungs (specified, not built):** `TemporalAttributionNet` (headline) + `RMALatentEncoder`. Post-freeze. Do NOT ship untrained shells.

`Reproducibility Packet/tests/test_recovery_seam.py` (**built my S14; jointly approved S15; UNCHANGED S16–S21**): shared end-to-end mechanism regression driving `CablePlant → OnlineSensorSession → EstimatorCommandPolicy → GainScheduledRecoveryController`. 4 tests. Asserts applied/delivered torque only; labeled NOT a `J_5s`/safety result.

`Reproducibility Packet/scripts/utils/metrics.py` + `utils/stats.py` (**jointly approved through S11; unchanged S12–S21**): two-layer success-bar metrics. **`tracking_reduction_pct(j_c1, j_s) = 100·(J_C1−J_S)/J_C1` — the contract's control quantity, C1 in the denominator. This is the definition the S21 units correction turns on.** `j_5s` has a fail-loud guard requiring the full `[t_c, t_c+5 s]` window — independently confirmed twice now (S20: 84 arms; S21: 36 arms; both 0.000e+00). **`safety_incident_rate` is a threshold-crossing count and cannot score a graded margin change in either direction** (S19, S20, S21). `stats.py` = crossed pair×seed paired hierarchical bootstrap. Eval **driver** (argparse CLI) owns the exact slice — build once frozen data layout exists.

## Codex's lanes — current state

`Reproducibility Packet/scripts/screen_fault_tracking_deficit.py` + `tests/test_fault_tracking_deficit.py` + `results/fault_tracking_deficit_screen/` (**Codex S20; my S21 first review → EDITED AND HANDED BACK, loop open**). No-recovery severity sweep on the fixed bounded condition: structure remaining EI `{0.75,0.50,0.25,0.10,0.05}`, actuator remaining gain `{0.85,0.70,0.50,0.25,0.10}`, fixed sensor control (encoder bias 0.05 rad on a healthy plant). Tuning seeds 16000–16002, disjoint assessment 16100–16103, 12 cases × 7 seeds = 84 arms. `_healthy_baseline_gates()` is Codex's correct forward application of my S20 baseline-integrity fix. Sensor control's deficit is **15.69%/15.61%** — above the gate, deliberately not a selected candidate (severity not swept).

`Reproducibility Packet/scripts/utils/recovery_control.py` — `GainScheduledRecoveryController` + `RecoveryControlConfig` (S12; my approval S13) + `command_from_nominal` (S17; approval S18) + `structural_action ∈ {derate, inverse_stiffness}` × `scope ∈ {global, localized}` (S19; my S20 edits approved by Codex S20). `_confident_source` gate = not abstained AND unique argmax==source AND p≥0.5 AND finite uncertainty ≤0.25. **Key constants for the next screen: `maximum_gain_compensation = 2.0`, `minimum_gain_remaining = 0.25`, `torque_abs_limit = (1.0, 0.5)`** (= the plant's own ctrlrange, so saturation can only fire if the plant would clip too).

`Reproducibility Packet/scripts/screen_structural_recovery_action.py` + tests + results (**Codex S19 + correction; my S20 edits; Codex's S20 owner re-review approved same state → JOINTLY APPROVED, loop closed**). Recorded `BLOCK_STRUCTURAL_RECOVERY_ACTION_FAMILY`. The robust grounds: ~70% of the selected action's benefit is produced at the *unfaulted* joint, and the structural no-action deficit is ~0.05%. The −0.263 pp specificity margin's sign is NOT established (it flips under a legitimate noise replicate).

`Reproducibility Packet/scripts/run_bounded_noisy_information_review.py` + tests + results (**Codex S18; my S19 edits; approved same state → loop closed**). **S PASSES information + action gates (macro-F1 0.995, 100% per-fault detection, 2.1% healthy FA); C1 BLOCKS (0.704, 8.3% structural recall, 4.2% FA); the recovery-control profile BLOCKS.** Holds the four representative S-vs-C1 pairs in the table above.

`Reproducibility Packet/scripts/utils/task_control.py` (S17; my approval S18) — `BoundedTaskProfile` (rest → `(0.30,0.30)` rad by 3.0 s → hold → back to rest by 5.0 s), `ObservedJointControllerConfig` (kp `(0.05,0.03)`, kd `(0.005,0.003)`, torque limits `(0.20,0.10)`), `ObservedJointPDController` (reads ONLY delivered `q_obs`/`qd_obs`; **peak command is only ~10% of its limits, so the clip never binds** — S20), `EstimatorRecoveryTaskPolicy`.

`Reproducibility Packet/scripts/utils/cable_mechanics.py` + `utils/cable_plant.py` + `make_mujoco_plant_trace.py` — plant lane + endpoint-contact extraction (S14; approval S15). **A1 safety flags** = `|q|>π`, `|qd|>10`, 3-D tip radius > 0.82 from `[0,0,0.5]`, `max|gauge|>500 µε`, `contact_state[0]>5 N`. **The 3-D workspace flag is NOT reconstructable from the record's 2-D `true_task_output` — recompute the other 6 from raw truth + trust the plant column for the 7th.** **Fault severity is the REMAINING fraction** for both structure (remaining EI) and actuator (remaining gain), validated in `CablePlant`.

`screen_bounded_task_contact.py` (S17; approval S18) — `BoundedTaskContactSpec`, `cable_config`, `SingleDecisionHoldEstimator` (one evaluation at `first_decision_step` = 1136 = 2.272 s, held causally), **`FixedSourceStandIn` + `_output_for_source` (structure → loc 1, sev 0.50; actuator → 1, 0.70; sensor → 0, 0.05 — these severities are PINNED and do not track the true fault; that is why the stand-in yields only 6.27% on the 0.50-remaining condition)**.

`run_noisy_reference_pilot.py` (S11), `screen_optional_contact_profile.py` (S15), `run_matched_contact_pilot.py` (S16, superseded) — all jointly approved. `fault_specs`, `project_observed_suite`, `count_contact_episodes` are reused by the newer screens.

## Coherence worth remembering

`utils/synchronous.py` (Codex, S9) is the **single shared harmonic statistic**. `synchronous_coefficient_vector` + `coefficient_reference_distance` in `utils/estimator.py` are the one canonical definition every pilot, screen, and review imports.

The **recovery seam** has both ends jointly exercised (my `EstimatorCommandPolicy` socket + Codex's `GainScheduledRecoveryController`), pinned by `test_recovery_seam.py`. **`detection_time_s` semantics are consistent everywhere.** The bounded screen (S17) established that recovery can act *before* contact; the noisy review (S18/S19) established that a *real* estimator can supply the label; **S20 established that on this condition there is nothing for the structural label to buy; S21 established that on the classes where there IS something to buy, C1 already has the label.**

**Contact + the 7th safety flag:** contact reaches deployable suites only through motion/strain (privileged-only otherwise). In closed loop it is NOT suite-invariant. **Design constraint (my S15 note, honored by every screen since): apply the contact profile identically across each matched C1/S CRN pair.**

**Sensor RNG is keyed on `(sensor_seed, pair_id, channel, stream)`** — the `pair_id` string is load-bearing (my S17 harness bug proved it; S20 turned it into a measurement tool: changing only the `pair_id` gives a legitimate independent noise replicate of the same design). **S21 used the reverse: reusing Codex's exact `pair_id` makes my own arms CRN-paired to its recorded rows.**

## The excitation/detection thread — current status (the project's dominant thread)

- **Settled chain:** S9 reframing → probe co-design → S11 noisy-deployable pilot → S12 `CoefficientReferenceDetector` + recovery floor → S13 residual/linear-sysID baseline → S14 loop pinned end-to-end → S15 optional-contact screen → S16 matched contact pilot BLOCKS → S17 bounded redesign clears mechanics/lifecycle → S18 real noisy instrument → S19 I reproduced 53/53, edited, handed back; Codex approved → Codex's structural-action screen honestly blocked → **S20 I reproduced it (50/50 + 84 arms), fixed the ungated baselines, showed the specificity gate flips under a replicate, and measured the per-class deficits** → Codex built the deficit screen → **S21 I reproduced it (42/42 twice + 36 arms), fixed the gate's units, and measured that the advanced condition yields ~10.8% total / ~4.7 pp source-specific against a 10% bar.**
- **The deployable S advantage IS the structural fault**, confirmed five times (S12, S16, S19, S20, S21's monotone 19→260 µε sweep). **C1 is blind, not weakly sighted** (S19). **The structural fault is dynamically silent and then tracking-improving** (S20, S21).
- **The information question is answered on this bounded development condition. The control question is answered negatively for every class screened so far** — structure has no deficit; actuator and sensor have deficits but no S-over-C1 information advantage, and the actuator action's source-specific benefit is <½ the bar.
- **Honesty bounds (keep loud):** (1) the deployable floors are **detection**, NOT learned attribution; (2) all rates come from **one fixed fault setting per class**, held-out over sensor noise only; (3) **abstention is untestable on this fault library** (min margin 0.90); (4) full-horizon continuations are **one seed per source/suite**; (5) one-hot prototype probabilities are **not** calibrated probabilities; (6) reference conditioning assumes a scheduled, phase-reset probe + ONE held decision; (7) every control-layer number comes from a condition where the structural fault causes no measurable tracking deficit; **(8) NEW S21 — the actuator control numbers come from an *oracle-severity* diagnosis; under the deployable stand-in's pinned severity the same action yields 6.27%, and no artifact has yet measured real severity-estimation quality.**

## The headline experiment design

The "does attribution improve control" comparison is wired at the diagnosis→control seam, its control semantics pinned by `test_recovery_seam.py`, its task/contact mechanics by the bounded screen, its *information* path demonstrated with a real noisy estimator. Post-freeze arms: **detection-only rungs → nominal** (control floor); **learned attribution head → active inverse-gain / derate** (headline arm); **RMA latent → blind adaptation**; **oracle → ceiling**. Scored by `J_5s` reduction + no-safety-regression on frozen confirmatory data. **S21 sharpening: the paired S−C1 quantity is already recorded as exactly 0.0000% on actuator and sensor and −18.58% (worse) on structure. Do not build this comparison until some class has BOTH an S-exclusive information advantage AND recoverable control headroom. No screened class currently has both.**

## Schema v1.0 + A1 mental model (in force)

File: `Reproducibility Packet/schema/schema-v1.0.md` (rendered in `utils/schema_types.py` §B/§0/§C/§E + `utils/estimator.py` §D). **Amendment A1 (in force):** `contact_state[2] = {tip_contact_force_n, tip_contact_active}`; `safety_flag[7]` order = joint_angle_0, joint_angle_1, joint_speed_0, joint_speed_1, tip_workspace, gauge_abs, tip_contact_force. Safety computed from **privileged truth**. Dev thresholds (config values, not frozen): `|q|≤π`, `|qd|≤10`, tip radius ≤0.82 m, `|gauge_true|≤500 µε`, tip contact force ≤5 N.
- **§A** identity/pairing/splits (splits by whole trajectory AND whole fault setting; suite never a split input; CRN within a pair via `utils/rng.py`) — **the S19 gap stands: held-out axes are sensor-seed only.** **§B** privileged `PlantStepState`/`PrivilegedRecord`. **§C** observed record (fixed 18-col registry, unavailable=NaN; `OnlineSensorSession` authoritative). **§D** labels/outputs/causality/leakage. **§E** storage. **§F** frozen constants. **§G** tracking metric `J_5s`.

## The agreed contract's load-bearing specifics (carry this)

- **Sensor suites (controlled variable):** **C0** = joint encoders + commanded actuation · **C1** = C0 + noisy motor-current nominal-Kt torque estimate + one distal 6-axis IMU · **S** = C1 + **four fixed strain/curvature gauge stations** · **O** = privileged oracle.
- **Two settled correctness points:** (1) actuator-gain fault acts *downstream* of the current proxy → C1 not handed true delivered torque; (2) encoder (sensor) fault has a *relational* signature.
- **Success bar (pre-declared, BOTH layers required):** S improves held-out four-way **macro-F1 over C1 by ≥0.05 absolute** (paired 95% excludes zero; every source-class recall diff lower-95% above **−0.02**) **and** reduces the **5-s post-change integral of absolute tracking error by ≥10%** — `100·(J_C1−J_S)/J_C1`, paired 95% excludes zero, **no safety regression** — **under realistic confounds**. Known-class abstention scored as error in headline macro-F1.
- **Failure shapes:** *hypothesis failure* (C1+temporal adaptation matches S — clean negative) vs *method failure*. **Inconclusive shapes (Slot 13):** **diagnostic-only** (attribution improves, control does not — **S20 and S21 together make this the near-certain landing**) · fault-specific/bounded · confound-fragile · excitation-dependent.
- **Pre-specification:** bars fixed before the pilot; freeze gauge placement, model/hyperparams, thresholds, analysis window, seeds/scenarios before confirmatory generation. Leakage-free splits. ≥5 training seeds. Paired hierarchical bootstrap.

## Labor split (agreed, unchanged)

- **Codex:** feasibility spike + physics, virtual-gauge extraction, excitation design, interpretable residual/linear-sysID baseline, recovery controller + external-nominal composition, contact/safety extraction, the contact/bounded screens, the matched pilots, the bounded noisy held-decision information review, the structural recovery action family screen, **the per-class deficit screen (S20; my S21 edits pending its re-review)**, the actuator action screen (next), evaluation-sized closed-loop controller comparison (pending).
- **Claude (me):** fault-injection + sensor-realism model, two-layer evaluation harness + metrics + stats, diagnosis-estimator front + window contract + oracle + seam adapter, synchronous-detection floor analysis, shared recovery-seam regression, matched temporal-attribution net + RMA latent (next, needs torch + frozen data), Slot-8 verification demo, default-writer artifacts (Technical Report, Accessible Piece, Study Guide Pass 2 — Codex reviews).
- **Shared:** the plant→signals→estimator schema (+A1), fault library, Reproducibility Packet, references reconciliation (Phase 2), `utils/synchronous.py`. The **"does attribution improve control" headline experiment is shared** at the diagnosis→control seam.

## Constraints / environment (unchanged, load-bearing)

- **Simulation-only, one desktop:** Windows 11, Ryzen 7 8700F (8C/16T), RTX 5060 Ti **16 GB VRAM** (Blackwell/sm_120), 32 GB RAM, Python **3.12.10** in `./venv` (use `.\venv\Scripts\python.exe` / `pip.exe`, never bare). Free/OSS, commercial-use-friendly only.
- **venv has:** numpy 2.5.1, scipy 1.18.0, scikit-learn 1.9.0, matplotlib 3.11.0, mujoco 3.10.0, pandas 3.0.3, control 0.10.2, gymnasium 1.3.0, pytest 9.1.1. **PyTorch NOT installed** — install CUDA build when building the learned rungs (verify sm_120 actually runs), pin immediately.
- **Running packet tests:** from `Reproducibility Packet/`, `..\venv\Scripts\python.exe -m pytest tests/` (each test self-inserts `scripts/` on `sys.path`; no conftest). **Running a script: from `Reproducibility Packet/` as `..\venv\Scripts\python.exe scripts\<name>.py`** (NOT from `scripts/`). **Full packet: 199 tests green (S21).** Set `PYTHONIOENCODING=utf-8` when a script prints unicode. My scratchpad reproduction scripts also run **from `Reproducibility Packet/`**. **Timings:** `run_bounded_noisy_information_review.py` ~12–20 min; `screen_structural_recovery_action.py` ~8 min (43 rollouts); **`screen_fault_tracking_deficit.py` ~20 min (84 arms) at 10 workers**; a bare 32-arm probe ~10 min at 10 workers. Run these in the background — piping to `tail` buffers all output until exit, so check the output file only at the end.
- **The packet runbook uses `.\.venv\Scripts\python.exe` throughout** — that is the *packet's own* self-contained venv convention for an outside reader, not our project root `venv`. Both are correct; do not "fix" one into the other.
- **Packet `.gitignore` ignores `*.npz`** (+ caches/logs); small JSON/CSV/MD result artifacts are intentionally tracked. Root `.gitignore` covers `venv/`, `tmp/`, `MUJOCO_LOG.TXT`, caches, LaTeX aux, OS/IDE noise — **verified accurate S21, no change needed.**
- **Software-engineering standard for every script:** `argparse` with `required=True` for input roots (or defaulted project-relative outputs), no hard-coded paths, one clear purpose, shared logic in `utils/`, docstrings, prints progress, fails loud. (`utils/` library modules + `tests/` are the import-not-CLI exception.)
- **Licensing:** code MIT, prose CC BY 4.0. No relaxed standard requested.

## Pointers

- Claim Sheet (in-force contract): `Claim Sheet.md` · plain-language: `Accessible Claim Sheet.md` · Study Guide Pass 1: `Study Guide/Pass 1 - Conceptual Foundation.tex`
- **Shared schema (in force, +A1):** `Reproducibility Packet/schema/schema-v1.0.md`
- **My lanes:** sensor `utils/{schema_types,sensor_model,rng,synthetic_plant}.py`; eval `utils/{metrics,stats}.py`; estimator `utils/estimator.py`; synchronous floor `scripts/analyze_synchronous_detection_floor.py`; shared seam test `tests/test_recovery_seam.py`.
- **Codex's plant/control lane:** `utils/{cable_mechanics,cable_plant,online_loop,recovery_control,residual_baseline,task_control}.py`, `scripts/{make_mujoco_plant_trace,run_feasibility_spike,run_bounded_burst_sensitivity,screen_synchronous_safe_probe,run_noisy_reference_pilot,screen_optional_contact_profile,run_matched_contact_pilot,screen_bounded_task_contact,run_bounded_noisy_information_review,screen_structural_recovery_action,screen_fault_tracking_deficit}.py` + matching tests + `results/` artifacts.
- **Active Phase-2 chat:** `chats/Claude-Codex/Phase 2 Integration and Config Freeze/…- Active.md` (my S21 turn = tail, 1673 lines; **one review loop OPEN — my edits await Codex's owner re-review**). Concluded chats have `Summary.md`s.
- **Active director chat:** `chats/Claude-Codex-Human/Transcript Order Monitoring/…- Active.md` (my S21 note; no action requested of Randy — but if he replies, answer it).
- Director requests: `director_requests.md` (root) — entry 1 (Claim Sheet review) non-blocking, awaiting director reply.
- My foundation `agents/Claude/Literature Foundation.md` · ledger `agents/Claude/references.md` (**no S20/S21 entries — reproduction/measurement sessions, no external sources read**) · progress reports `agents/Claude/Progress Reports/` (Phase 0/1 Close, Session 8, Session 16). **Next regular: Session 24.**
- Live-Run README (co-maintained): root `README.md` — **Phase 2 / In Progress**; last log entry 2026-07-22 (Codex's deficit-screen direction entry). **Untouched S21 deliberately** — the log is append-only, the entry is Codex's, and my findings are mid-loop. **The next public entry should carry whatever we jointly conclude about the control layer.**
- Scratchpad (not committed, outside repo): `s21_deficit_audit.py` (42-check audit — reusable template for auditing a screen's decision function against its own committed rows), `s21_probe.py` (**the important one: a self-contained arm driver with a `SeverityStandIn` that emits an oracle-severity one-hot diagnosis — this is how you measure what an action can actually achieve on a condition; reuse it for the next action screen review**), `s21_probe_rows.json` + `_b2.json`, `s21_codex_hashes.txt`, `s21_rerun.txt`. Earlier: `s20_decision_audit.py`, `s20_probe.py`.
