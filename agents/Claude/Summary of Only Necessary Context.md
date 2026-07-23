# Summary of Only Necessary Context — Claude

*Rewritten every session. Restores my working context for the next session. Excludes anything already in `Project Details/Project Details.md` and `AgentPrompt.md` (I re-read those in full at session start). Last rewritten: end of Session 23, 2026-07-22 20:25 PDT.*

## Where the project is

- **Phase 2 (Execution) is OPEN.** All Phase-1 gates closed and in force. **Schema v1.0 + Amendment A1 (contact/safety roles) are jointly in force.** Contract changes run through the **amendment protocol**, not casual editing.
- I am **Claude**; last session was **Session 23**; next session I run is **Session 24**.
- **SESSION 24 OWES A DIRECTOR PROGRESS REPORT.** Regular cadence (my sessions 8/16/24). Phase-0-close, Phase-1-close, Session-8, Session-16 reports exist. Write it *in addition to* normal session work, at the Accessible-Piece bar, into `agents/Claude/Progress Reports/`.
- **`config.json` is deliberately NOT frozen.** Current role hashes are `dev-`; no `dev-` trace may enter confirmatory analysis.
- **Packet: 240 tests green** (220 through Codex's S22; +20 from my S23 cap-boundary screen).

## Review-cycle state (READ THIS FIRST next session)

- **The severity-estimation-quality loop is CLOSED.** Codex's S22 review found a real defect in my S22 screen; I audited its correction 60 ways, agreed, and **approved same-state in S23 without editing.** Do not reopen.
- **ONE LOOP IS OPEN, AND IT IS MINE, HANDED TO CODEX FOR FIRST REVIEW.** My S23 work: `utils/estimator.py` (`leave_one_group_out_residuals`), `scripts/screen_severity_action_boundary.py`, `tests/test_severity_action_boundary.py`, the three artifacts in `results/severity_action_boundary/`, packet **Step 16** + the 16→20 renumbering, the **Step 2 runbook change**, the Current-boundary rewrite, and the root Live-Run entry. **I explicitly approved the state I handed off.**
  - **Next session, first job: read Codex's S23 turn.** Approve-same-state → closed; edited-and-handed-back → genuinely re-review its edits *and* its diagnosis, then approve or edit again. Escalate a specific non-converged point to Randy after ~2 round-trips.
  - **Watch §8 of my turn specifically** — the Step-2 runbook change is a *shared-packet* edit I made outside my own step. I offered to restore an enumerated list if Codex prefers. If it pushes back, that is a legitimate disagreement, not an oversight.
- **My S23 turn is the physical tail** of the active Phase-2 chat (posted 2026-07-22 20:15 PDT; file 1851 → **1944 lines**; header at line 1855, occurs once, physically last; +93/−0).
- **MONITORING DUTY IS STANDING.** It fired twice (Codex's S20 and S21 approvals both landed mid-file at line 1,331; Codex's own verifier caught and repaired both). **S23 logged the first CLEAN check** — Codex's S22 turn landed correctly at the tail — so `chats/Claude-Codex-Human/Transcript Order Monitoring/` now records the rule working, not only its failures. **Reuse `scratchpad/append_turn.py`** (EOF-append + hard gates: prefix-identical, unique header, position-after-boundary, Claude-last, +N/−0).

## THE HEADLINE OF S23 — carry this into everything

**Codex was right that my S22 "the reachable set is empty" claim was false, and the reason is worth remembering. My `SEVERITY_GRID` used 0.55 and 0.40 *because* they bracket the cap-2 kink at 0.50 — and never included 0.50 itself.** The multiplier `min(1/max(ŝ,floor), cap)` is flat for estimates *strictly below* the kink; **at** the kink it is one-sidedly sensitive. 0.50 is a setting Codex's deficit screen records, with an 11.66% exact-restoration ceiling (above the 10% bar). Verified on the real controller: `m(0.49)=m(0.50)=2.000000`, `m(0.51)=1.960784`. **Bracketing a boundary is not testing it.**

**General guard I adopted (state it, don't one-off-test it): every setting an upstream artifact records must appear in the downstream grid, or be excluded by name with a reason.** My S22 screen passed 42 self-checks because all 42 asked "is the analysis faithful to the grid?" and none asked "is the grid faithful to the recorded conditions?"

**Then I measured what the boundary is worth, and it closes anyway — on better grounds.**

**(A) The paired quantity, measured** (4 assessment seeds, each suite's *recorded held-out estimate* driving the real controller):

| seed | C1 est | S est | m(C1) | m(S) | paired S−C1 |
|---:|---:|---:|---:|---:|---:|
| 17100 | 0.4952 | 0.4992 | 2.00000 | 2.00000 | +0.0000% |
| 17101 | 0.5109 | 0.5015 | 1.95741 | 1.99392 | +0.1053% |
| 17102 | 0.4974 | 0.5180 | 2.00000 | 1.93060 | **−0.5154%** |
| 17103 | 0.4983 | 0.5067 | 2.00000 | 1.97358 | −0.0605% |

**Mean −0.1177%, worst 0.5154%, vs a 10% bar.** C1 ahead on 2, S on 1, 1 exactly identical. The action is real here: **+13.11% no-action deficit, +10.81% recovered by oracle.**

**(B) The bound — this is the part that generalizes.** Fixed-multiplier sweep, mean reduction vs no-action:

| m | 1.50 | 1.70 | 1.85 | 1.93 | 1.97 | 2.00 |
|---|---:|---:|---:|---:|---:|---:|
| reduction | +7.00% | +8.70% | +9.86% | +10.37% | +10.58% | +10.81% |

**Span = 3.81 pp across the WHOLE range.** m=1.50 corresponds to ŝ=0.667 on a true 0.50 — ~15× the worse suite's held-out residual std — and still recovers 7.00%. Local slope 7.58 pp/unit × observed 0.0694 spread = **0.53 pp**.

**⇒ The severity route on the actuator class is CLOSED at the recorded cap on this condition — for ANY read-out, not just the linear one.** NOT closed at cap ≥ 4 (the 0.25 floor becomes the boundary there, all 4 paired arms differ; **I did not run it**).

**Why the sign works out (structural, not luck):** at the boundary the flat side commands 2.0, which for a true 0.50 fault **is exact restoration**. So the capped side is the *optimum* and the only direction of disagreement is under-restoration. The suite landing below the kink more often wins — that is C1 (75% vs 25% oracle-identical at the boundary). **A boundary difference is not an S advantage waiting to be collected.**

## TWO S23 SIDE RESULTS THAT MATTER MORE THAN THE HEADLINE

**1. Held-out severity uncertainty — the in-sample number INVERTS the suite ranking.**

| suite | in-sample | held-out (LOSO) | understates by |
|---|---:|---:|---:|
| C1 | 0.004237 | 0.006741 | 1.59× |
| S | 0.001951 | **0.011160** | **5.72×** |

In-sample, **S looks like the more confident read-out.** Held out, it is the **less reliable** one. The 32 gauge columns fit training windows tighter and generalize worse. **Never hand `train_residual_std` to `_confident_source`.** Both clear the 0.25 gate on the held-out figure, so the action fires identically for either. Function: `leave_one_group_out_residuals` in `utils/estimator.py` (group = sensor seed, penalty held fixed across folds).

**2. Exact restoration of the gain does NOT exactly restore the tracking.** Mean deficit 13.11% → analytic `D/(1+D)` ceiling **11.59%**; oracle realizes **10.81%**. Shortfall **0.78 pp = 93.2% of ceiling**, same direction on all 4 seeds (0.66/0.84/0.86/0.78). The gap is error the fault produces *before* the single held decision fires — unrecoverable by any multiplier. **Codex's deficit gate converts `R → R/(1−R)` assuming full realization, so it is optimistic by ~7% relative.** Same *kind* of correction as my S21 units catch, same direction. 0.25 remaining gain advanced against that conversion; flagged to Codex, not proposing a re-run.

## THE SHAPE OF THE CONTROL LAYER (recorded, not inferred)

From Codex's committed `bounded_noisy_information_review/summary.json` — the four representative S-vs-C1 pairs:

| source | C1 gate state | S gate state | suite-informed | `s_tracking_change_pct` |
|---|---|---|---|---:|
| healthy | correct_no_action | correct_no_action | no | 0.0000% |
| **structure** | withheld_actionable_fault | correct_actionable | **yes** | **−18.5762%** |
| **actuator** | correct_actionable | correct_actionable | no | **0.0000%** |
| **sensor** | correct_no_action | correct_no_action | no | **0.0000%** |

C1 per-class recall there: structure **0.083**, actuator **1.000**, sensor **1.000** (S: 1.000 on all three).

**⇒ Where S has exclusive information there is no control headroom; where there is control headroom S has no exclusive information — now established for DETECTION, CLASSIFICATION, SEVERITY ACCURACY, and (S23) the SEVERITY→TRACKING conversion.** Any future control-layer plan must answer this table first.

## The strongest version of the structural result (from Codex's S20 rows, in its generated report)

| remaining EI | mean peak \|gauge\| | mean tracking deficit |
|---:|---:|---:|
| healthy | 19.2 µε | — |
| 0.75 | 25.0 µε | +0.11% |
| 0.50 | 38.4 µε | +0.08% |
| 0.25 | 72.4 µε | −0.89% |
| 0.10 | 152.8 µε | −2.23% |
| 0.05 | 259.7 µε | −5.00% |

**Monotone in information; monotone the wrong way in control.** 13.5× the healthy strain signature at the severity where tracking is 5% *better* than healthy. The Slot-13 diagnostic-only shape measured across a 15× stiffness sweep. **This is the sentence the write-up gets built on.**

## The single most important things to do next session (Session 24)

1. **Check Codex's S23 turn** for its first review. Approve-same-state → closed; edited-and-handed-back → genuinely re-review both its edits and its diagnosis. Pay attention to §8 (the shared-packet runbook change).
2. **WRITE THE SESSION-24 PROGRESS REPORT** — regular cadence, in addition to normal work.
3. **The class-probability channel is now the ONLY unexamined route** to a suite difference on a class both call correctly: multiplier = `1 + p·(capped−1)`. Every screen so far pins `p = 1` on both suites. The recorded one-hot prototype probabilities are explicitly *not* calibrated. **This is the last one — after it, the actuator class is exhausted on every channel the action can spend.**
4. **The cap ≥ 4 boundary (0.25 floor) is unmeasured.** My S23 bound does not cover it. If Codex sweeps the cap, that boundary needs the same treatment — and remember `(maximum_gain_compensation, minimum_gain_remaining)` is a *joint* control surface, not two knobs.
5. **Deferred, still blocked (do NOT build early):**
   - The learned attribution rungs (`TemporalAttributionNet` headline + `RMALatentEncoder`) — need PyTorch CUDA build, GPU-verified sm_120, installed *at that point*; + frozen config + confirmatory data.
   - The §D deployable-loader leakage test + whole-trajectory/fault-setting split audit — need real multi-run storage.
   - The eval **driver** ([t_c, t_c+5 s] slicing → paired C1-vs-S control comparison) — needs the frozen data layout.

**Do NOT freeze a partial config.** Open freeze items: **the class-probability channel**; `minimum_gain_remaining` as a JOINTLY-binding constant with `maximum_gain_compensation`; the actuator action screen itself; validation-sized healthy threshold calibration (≥~100 values) **with per-suite probability calibration**; the ambiguous-case fault library that makes abstention testable at all (my S19 note); severity/onset grids; joint sanity-check of non-load-bearing sensor constants; validation-frozen class/abstention/selective/OOD thresholds; the reference-lifecycle choice (single held decision vs. a temporal model over the full post-probe trajectory); the **bounded task/contact/controller profile** (`z=0.200 m` + PD gains `(0.05,0.03)`/`(0.005,0.003)` + torque limits `(0.20,0.10)` + timing are *dev candidates*, NOT frozen margins); `W`/stride (**768/16** pilot-advanced, still not frozen); split/leakage/storage/hash audits. *(The severity-estimation-quality item is now MEASURED for the actuator class at the recorded cap — narrow it, don't delete it. **Held-out severity uncertainty is now BUILT** — record that the in-sample figure must never reach the gate.)*

## My lanes — current state (reference for next builds)

`Reproducibility Packet/scripts/utils/estimator.py`:
- **Window front-end `WindowFeatureExtractor(window_steps=W=768, probe_frequency_hz=0.8)`**: fixed `[W,D]` left-padded tensor + per-column summary `[last, mean, std, slope, sync_cos, sync_sin, sync_amplitude, valid_fraction]`, suite-agnostic over the 18-col registry → **144 features**. Constants: `N_FEATURE_STATS=4`, `N_EXTRA_FEATURES=4`, `SYNC_COS_FEATURE_COL=4`, `SYNC_SIN_FEATURE_COL=5`, `SYNC_AMPLITUDE_FEATURE_COL=6`, `VALID_FRACTION_COL=7`, `DIAGNOSTIC_PROBE_HZ=0.8`, `MIN_SYNC_SAMPLES=8`.
- **`WindowNoveltyDetector`**: interpretable detect + calibrated-abstention; consumes cos/sin as per-feature z-scores. Latches `detection_time_s` after `persistence` consecutive over-threshold windows.
- **`CoefficientReferenceDetector`**: second interpretable detection rung; joint healthy-standardized coefficient distance `‖(coeff_live−mean)/scale‖/√D` (module-level `synchronous_coefficient_vector` + `coefficient_reference_distance`, the canonical statistic every pilot/screen imports). Detection-only, abstains on type. `fit_reference` atomic; re-fit invalidates threshold + resets latch. `calibrate_threshold` FAILS LOUD below `ceil(min_tail/far)` (≥100 at far=0.05).
- **`_SCORE_STD_FLOOR = 1e-3`** shared by both interpretable rungs (S22; jointly approved S23). Provably a no-op on every recorded artifact.
- **`SeverityRidgeHead`** (S22; jointly approved S23): the project's first *deployable* severity read-out. Standardized closed-form ridge on the `WindowFeatureExtractor` summary; no new dependency, no training loop. **Suite-agnostic structurally**: a channel a suite lacks is all-zero → exactly zero training variance → standardizes to 0 → cannot enter the fit. **`train_residual_std` is IN-SAMPLE — never feed it to a confidence gate; use `leave_one_group_out_residuals` instead.**
- **NEW S23 — `leave_one_group_out_residuals(features, severities, groups, *, regularization, severity_bounds)`** (in review): refits the head once per held-out group and returns `[N]` out-of-sample residuals in input order. Group by **sensor seed** (windows sharing a seed share a noise realization). Fails loud on shape mismatch and on <2 groups.
- **`OracleInterface(onset_time_s)`**: allowlisted privileged ceiling, causal. **`EstimatorCommandPolicy`**: the `run_online_rollout` `CommandPolicy` adapter (diagnosis→control socket; runs estimator every `stride`, **ZOHs the estimator OUTPUT but calls `recovery_command` EVERY step**).
- **`RECOMMENDED_WINDOW` = (W=768, stride=16)** — pilot-advanced, still a pilot proposal.
- **Learned rungs (specified, not built):** `TemporalAttributionNet` (headline) + `RMALatentEncoder`. Post-freeze. Do NOT ship untrained shells.

`scripts/screen_severity_estimation_quality.py` + tests + `results/severity_estimation_quality/` (**S22 mine; Codex's S22 correction; my S23 same-state approval → JOINTLY APPROVED, CLOSED**). Grid now `(1.00, 0.85, 0.70, 0.55, 0.50, 0.40, 0.25, 0.10)`, 80 arms. Corrected held-out MAE **C1 0.0065 / S 0.0076** (C1 better). Four regimes in the oracle comparison: capped / **boundary** / sensitive / identity. `window_features.csv` is the durable product — refits need no rollouts.

`scripts/screen_severity_action_boundary.py` + tests + `results/severity_action_boundary/` (**S23, mine, IN REVIEW**). 40 arms = 4 seeds × {healthy_reference, no_action, oracle, deployable_C1, deployable_S, multiplier_{1.50,1.70,1.85,1.93,1.97}}. Key functions: `holdout_severity_uncertainty`, `load_boundary_estimates`, `FixedDiagnosisEstimator` (None ⇒ healthy/no-action), `build_arm_specs`, `run_action_arm`, `paired_boundary_result` (uses `tracking_reduction_pct`, C1 in denominator), `multiplier_sensitivity_curve`, `bound_from_slope`, `build_audit`. **The construction rests on CRN reuse of Step 15's `pair_id` (`severity-quality-assessment-<seed>`) — checked, not assumed: 8/8 reference arms reproduce the committed `J_5s` at 0.000e+00, and `main()` aborts if not.** Runtime ~7 min at 8 workers.

`tests/test_recovery_seam.py` (**built S14; jointly approved S15; UNCHANGED S16–S23**): shared end-to-end mechanism regression driving `CablePlant → OnlineSensorSession → EstimatorCommandPolicy → GainScheduledRecoveryController`. 4 tests. Asserts applied/delivered torque only; labeled NOT a `J_5s`/safety result.

`utils/metrics.py` + `utils/stats.py` (**jointly approved through S11; unchanged S12–S23**): two-layer success-bar metrics. **`tracking_reduction_pct(j_c1, j_s) = 100·(J_C1−J_S)/J_C1` — the contract's control quantity, C1 in the denominator.** `j_5s` has a fail-loud guard requiring the full `[t_c, t_c+5 s]` window. **`safety_incident_rate` is a threshold-crossing count and cannot score a graded margin change in either direction** (S19–S22). `stats.py` = crossed pair×seed paired hierarchical bootstrap. Eval **driver** (argparse CLI) owns the exact slice — build once frozen data layout exists.

## Codex's lanes — current state

`scripts/screen_fault_tracking_deficit.py` + `results/fault_tracking_deficit_screen/` (**JOINTLY APPROVED, CLOSED S22**). No-recovery severity sweep: structure remaining EI `{0.75,0.50,0.25,0.10,0.05}`, actuator remaining gain `{0.85,0.70,0.50,0.25,0.10}`, fixed sensor control. Tuning 16000–16002, assessment 16100–16103, 84 arms. **Gate: `required_reduction_pct` = 12%, `required_deficit_pct` = `R/(1−R)` = 13.636%.** Selection = `actuator_gain_remaining_0p25`. **S23 caveat: that conversion is an upper bound — measured realization is 93.2%.**

`utils/recovery_control.py` — `GainScheduledRecoveryController` + `RecoveryControlConfig` (S12/S13) + `command_from_nominal` (S17/S18) + `structural_action ∈ {derate, inverse_stiffness}` × `scope ∈ {global, localized}` (S19/S20). `_confident_source` gate = not abstained AND unique argmax==source AND p≥0.5 AND finite uncertainty ≤0.25. **Load-bearing constants: `maximum_gain_compensation = 2.0`, `minimum_gain_remaining = 0.25`, `torque_abs_limit = (1.0, 0.5)`, `maximum_severity_uncertainty = 0.25`.** *(Driving it directly: use a small nominal like `[0.01, 0.02]` — `torque_abs_limit` clips a unit nominal and hides the multiplier.)*

`screen_structural_recovery_action.py` (**CLOSED S20**) — recorded `BLOCK_STRUCTURAL_RECOVERY_ACTION_FAMILY`; ~70% of the selected action's benefit is at the *unfaulted* joint; the −0.263 pp specificity margin's sign is NOT established.

`run_bounded_noisy_information_review.py` (**CLOSED S19**) — **S PASSES information + action gates (macro-F1 0.995, 100% per-fault detection, 2.1% healthy FA); C1 BLOCKS (0.704, 8.3% structural recall, 4.2% FA).** Holds the four representative pairs above.

`utils/task_control.py` (S17/S18) — `BoundedTaskProfile` (rest → `(0.30,0.30)` rad by 3.0 s → hold → back to rest by 5.0 s), `ObservedJointControllerConfig` (kp `(0.05,0.03)`, kd `(0.005,0.003)`, torque limits `(0.20,0.10)`), `ObservedJointPDController` (reads ONLY delivered `q_obs`/`qd_obs`), `EstimatorRecoveryTaskPolicy`.

`utils/cable_mechanics.py` + `utils/cable_plant.py` + `make_mujoco_plant_trace.py` (S14/S15). **A1 safety flags** = `|q|>π`, `|qd|>10`, 3-D tip radius > 0.82 from `[0,0,0.5]`, `max|gauge|>500 µε`, `contact_state[0]>5 N`. **The 3-D workspace flag is NOT reconstructable from the record's 2-D `true_task_output`.** **Fault severity is the REMAINING fraction** for both structure (remaining EI) and actuator (remaining gain).

`screen_bounded_task_contact.py` (S17/S18) — `BoundedTaskContactSpec`, `cable_config`, `SingleDecisionHoldEstimator` (one evaluation at `first_decision_step` = 1136 = 2.272 s, held causally), `FixedSourceStandIn` (**severities PINNED**). `run_noisy_reference_pilot.py` (S11 — home of **`project_observed_suite`**), `screen_optional_contact_profile.py` (S15), `run_matched_contact_pilot.py` (S16, superseded).

## Coherence worth remembering

`utils/synchronous.py` (Codex, S9) is the **single shared harmonic statistic**. `synchronous_coefficient_vector` + `coefficient_reference_distance` in `utils/estimator.py` are the one canonical definition every pilot, screen, and review imports.

The **recovery seam** has both ends jointly exercised, pinned by `test_recovery_seam.py`. **S20: on the bounded condition there is nothing for the structural label to buy; S21: on classes where there IS something to buy, C1 already has the label; S22: C1 also already has the SEVERITY; S23: and even where a severity difference survives, it converts to <0.6 pp of tracking against a 10% bar.**

**Contact + the 7th safety flag:** contact reaches deployable suites only through motion/strain. In closed loop it is NOT suite-invariant. **Design constraint (my S15 note, honored by every screen since): apply the contact profile identically across each matched C1/S CRN pair.** *(With NO action and a PD controller reading only `q_obs`/`qd_obs`, an S rollout and its C1 projection are bit-identical — verified 0.000e+00. That is what makes one-rollout-two-suites legitimate, and it holds only because no recovery fires. **S23 corollary: with a SINGLE held decision, arms that differ only in the commanded severity are also bit-identical up to the decision step — which is what lets a recorded estimate drive a new acting rollout.**)*

**Sensor RNG is keyed on `(sensor_seed, pair_id, channel, stream)`** — the `pair_id` string is load-bearing (my S17 harness bug proved it; S20 turned it into a measurement tool; **S23 reused Step 15's `pair_id` verbatim to make the acting arms share the estimating arms' noise, then checked it at 0.000e+00**).

## The excitation/detection thread — current status (the project's dominant thread)

- **Settled chain:** S9 reframing → probe co-design → S11 noisy-deployable pilot → S12 `CoefficientReferenceDetector` + recovery floor → S13 residual/linear-sysID baseline → S14 loop pinned end-to-end → S15 optional-contact screen → S16 matched contact pilot BLOCKS → S17 bounded redesign → S18 real noisy instrument → S19 reproduced 53/53, approved → structural-action screen BLOCKS → **S20 I reproduced it (50/50 + 84 arms)** → deficit screen → **S21 I reproduced it and fixed the gate's units** → **S22 severity-quality screen** → **S23 Codex's grid correction approved; boundary measured and bounded.**
- **The deployable S advantage IS the structural fault**, confirmed seven times. **C1 is blind on structure, not weakly sighted** (S19). **The structural fault is dynamically silent and then tracking-improving** (S20, S21).
- **The information question is answered on this bounded development condition. The control question is answered negatively for every class screened so far** — structure has no deficit; actuator and sensor have deficits but no S-over-C1 advantage in *detection, classification, severity accuracy, or severity→tracking conversion*.
- **Honesty bounds (keep loud):** (1) the deployable floors are **detection**, NOT learned attribution; (2) all rates come from **one fixed fault setting per class**, held-out over sensor noise only; (3) **abstention is untestable on this fault library** (min margin 0.90); (4) full-horizon continuations are **one seed per source/suite**; (5) one-hot prototype probabilities are **not** calibrated probabilities; (6) reference conditioning assumes a scheduled, phase-reset probe + ONE held decision; (7) every control-layer number comes from a condition where the structural fault causes no measurable tracking deficit; (8) the actuator control numbers come from an *oracle-severity* diagnosis, and under the stand-in's pinned severity the same action yields 6.27%; (9) the severity result bounds a LINEAR read-out at 48 fit windows with `p` pinned at 1 on both suites; **(10) NEW S23 — the boundary bound is 4 seeds at ONE cap; the cap ≥ 4 boundary is unrun, and `deficit→reduction` realizes only 93.2%.**

## The headline experiment design

The "does attribution improve control" comparison is wired at the diagnosis→control seam, its control semantics pinned by `test_recovery_seam.py`, its task/contact mechanics by the bounded screen, its *information* path demonstrated with a real noisy estimator. Post-freeze arms: **detection-only rungs → nominal** (control floor); **learned attribution head → active inverse-gain / derate** (headline arm); **RMA latent → blind adaptation**; **oracle → ceiling**. Scored by `J_5s` reduction + no-safety-regression on frozen confirmatory data. **Sharpening that survives S23: do not build this comparison until some class has BOTH an S-exclusive information advantage AND recoverable control headroom. No screened class has both, and the actuator class now fails on FOUR separate channels (detection, classification, severity accuracy, severity→tracking conversion) with only class-probability unexamined.**

## Schema v1.0 + A1 mental model (in force)

File: `Reproducibility Packet/schema/schema-v1.0.md` (rendered in `utils/schema_types.py` §B/§0/§C/§E + `utils/estimator.py` §D). **Amendment A1 (in force):** `contact_state[2] = {tip_contact_force_n, tip_contact_active}`; `safety_flag[7]` order = joint_angle_0, joint_angle_1, joint_speed_0, joint_speed_1, tip_workspace, gauge_abs, tip_contact_force. Safety computed from **privileged truth**. Dev thresholds (config values, not frozen): `|q|≤π`, `|qd|≤10`, tip radius ≤0.82 m, `|gauge_true|≤500 µε`, tip contact force ≤5 N.
- **§A** identity/pairing/splits (splits by whole trajectory AND whole fault setting; suite never a split input; CRN within a pair via `utils/rng.py`) — **the S19 gap stands: held-out axes are sensor-seed only.** **§B** privileged `PlantStepState`/`PrivilegedRecord`. **§C** observed record (fixed 18-col registry, unavailable=NaN; `OnlineSensorSession` authoritative). **§D** labels/outputs/causality/leakage. **§E** storage. **§F** frozen constants. **§G** tracking metric `J_5s`.

## The agreed contract's load-bearing specifics (carry this)

- **Sensor suites (controlled variable):** **C0** = joint encoders + commanded actuation · **C1** = C0 + noisy motor-current nominal-Kt torque estimate + one distal 6-axis IMU · **S** = C1 + **four fixed strain/curvature gauge stations** · **O** = privileged oracle. *(C0 carrying commanded actuation is exactly why C1 nails actuator severity — the fault is downstream of it.)*
- **Two settled correctness points:** (1) actuator-gain fault acts *downstream* of the current proxy → C1 not handed true delivered torque; (2) encoder (sensor) fault has a *relational* signature.
- **Success bar (pre-declared, BOTH layers required):** S improves held-out four-way **macro-F1 over C1 by ≥0.05 absolute** (paired 95% excludes zero; every source-class recall diff lower-95% above **−0.02**) **and** reduces the **5-s post-change integral of absolute tracking error by ≥10%** — `100·(J_C1−J_S)/J_C1`, paired 95% excludes zero, **no safety regression** — **under realistic confounds**. Known-class abstention scored as error in headline macro-F1.
- **Failure shapes:** *hypothesis failure* (C1+temporal adaptation matches S — clean negative) vs *method failure*. **Inconclusive shapes (Slot 13):** **diagnostic-only** (attribution improves, control does not — **S20–S23 together make this the near-certain landing**) · fault-specific/bounded · confound-fragile · excitation-dependent.
- **Pre-specification:** bars fixed before the pilot; freeze gauge placement, model/hyperparams, thresholds, analysis window, seeds/scenarios before confirmatory generation. Leakage-free splits. ≥5 training seeds. Paired hierarchical bootstrap.

## Labor split (agreed, unchanged)

- **Codex:** feasibility spike + physics, virtual-gauge extraction, excitation design, interpretable residual/linear-sysID baseline, recovery controller + external-nominal composition, contact/safety extraction, the contact/bounded screens, the matched pilots, the bounded noisy held-decision information review, the structural recovery action family screen, the per-class deficit screen, **the actuator action screen (next — action-vs-no-action benefit, healthy false authorization, cap/floor sensitivity, source-specific margin)**, evaluation-sized closed-loop controller comparison (pending).
- **Claude (me):** fault-injection + sensor-realism model, two-layer evaluation harness + metrics + stats, diagnosis-estimator front + window contract + oracle + seam adapter, synchronous-detection floor analysis, shared recovery-seam regression, the severity read-out + severity-quality screen (S22), **the cap-boundary action screen + held-out severity uncertainty (S23)**, matched temporal-attribution net + RMA latent (next, needs torch + frozen data), Slot-8 verification demo, default-writer artifacts (Technical Report, Accessible Piece, Study Guide Pass 2 — Codex reviews).
- **Shared:** the plant→signals→estimator schema (+A1), fault library, Reproducibility Packet, references reconciliation (Phase 2), `utils/synchronous.py`. The **"does attribution improve control" headline experiment is shared** at the diagnosis→control seam.

## Constraints / environment (unchanged, load-bearing)

- **Simulation-only, one desktop:** Windows 11, Ryzen 7 8700F (8C/16T), RTX 5060 Ti **16 GB VRAM** (Blackwell/sm_120), 32 GB RAM, Python **3.12.10** in `./venv` (use `.\venv\Scripts\python.exe` / `pip.exe`, never bare). Free/OSS, commercial-use-friendly only.
- **venv has:** numpy 2.5.1, scipy 1.18.0, scikit-learn 1.9.0, matplotlib 3.11.0, mujoco 3.10.0, pandas 3.0.3, control 0.10.2, gymnasium 1.3.0, pytest 9.1.1. **PyTorch NOT installed** — install CUDA build when building the learned rungs (verify sm_120 actually runs), pin immediately. *(S22 and S23 both used no new dependency — closed-form numpy on purpose.)*
- **Running packet tests:** from `Reproducibility Packet/`, `..\venv\Scripts\python.exe -m pytest tests/` (each test self-inserts `scripts/` on `sys.path`; no conftest). **Running a script: from `Reproducibility Packet/` as `..\venv\Scripts\python.exe scripts\<name>.py`** (NOT from `scripts/`). **Full packet: 240 tests green (S23).** Set `PYTHONIOENCODING=utf-8` when a script prints unicode.
- **Timings (measured):** `run_bounded_noisy_information_review.py` ~12–20 min; `screen_structural_recovery_action.py` ~8 min; `screen_fault_tracking_deficit.py` ~20 min (84 arms); `screen_severity_estimation_quality.py` ~7–9 min (80 arms); **`screen_severity_action_boundary.py` ~7 min (40 arms) at 8 workers**. Run in the background; **a bash pipe through `tail` buffers everything until exit, so the progress file stays empty — poll for the results directory instead.**
- **STANDING LESSON — dry-run the analysis path before spending a rollout budget.** `scratchpad/s23_dryrun.py` exercises the *entire* post-rollout path (every derived table, artifact writing, report determinism, every audit gate) on synthetic rows in the exact returned shape, in seconds. It caught three interface errors this session before any simulation ran. **Do this first, every time.**
- **The packet runbook uses `.\.venv\Scripts\python.exe` throughout** — that is the *packet's own* self-contained venv convention for an outside reader, not our project root `venv`. Both are correct; do not "fix" one into the other.
- **Packet `.gitignore` ignores `*.npz`** (+ caches/logs); small JSON/CSV/MD result artifacts are intentionally tracked. Root `.gitignore` covers `venv/`, `tmp/`, `MUJOCO_LOG.TXT`, caches, LaTeX aux, OS/IDE noise — **verified accurate S23, no change needed.**
- **Software-engineering standard for every script:** `argparse` with `required=True` for input roots (or defaulted project-relative outputs), no hard-coded paths, one clear purpose, shared logic in `utils/`, docstrings, prints progress, fails loud. (`utils/` library modules + `tests/` are the import-not-CLI exception.)
- **Licensing:** code MIT, prose CC BY 4.0. No relaxed standard requested.

## Pointers

- Claim Sheet (in-force contract): `Claim Sheet.md` · plain-language: `Accessible Claim Sheet.md` · Study Guide Pass 1: `Study Guide/Pass 1 - Conceptual Foundation.tex`
- **Shared schema (in force, +A1):** `Reproducibility Packet/schema/schema-v1.0.md`
- **My lanes:** sensor `utils/{schema_types,sensor_model,rng,synthetic_plant}.py`; eval `utils/{metrics,stats}.py`; estimator `utils/estimator.py`; synchronous floor `scripts/analyze_synchronous_detection_floor.py`; shared seam test `tests/test_recovery_seam.py`; severity screen `scripts/screen_severity_estimation_quality.py`; **boundary screen `scripts/screen_severity_action_boundary.py` + `tests/test_severity_action_boundary.py` + `results/severity_action_boundary/`**.
- **Codex's plant/control lane:** `utils/{cable_mechanics,cable_plant,online_loop,recovery_control,residual_baseline,task_control}.py`, `scripts/{make_mujoco_plant_trace,run_feasibility_spike,run_bounded_burst_sensitivity,screen_synchronous_safe_probe,run_noisy_reference_pilot,screen_optional_contact_profile,run_matched_contact_pilot,screen_bounded_task_contact,run_bounded_noisy_information_review,screen_structural_recovery_action,screen_fault_tracking_deficit}.py` + matching tests + `results/` artifacts.
- **Active Phase-2 chat:** `chats/Claude-Codex/Phase 2 Integration and Config Freeze/…- Active.md` (my S23 turn = tail, **1944 lines**; **one loop OPEN — my boundary screen awaits Codex's first review**). Concluded chats have `Summary.md`s.
- **Active director chat:** `chats/Claude-Codex-Human/Transcript Order Monitoring/…- Active.md` (two occurrence notes + my S23 clean-check note; no action requested of Randy — but if he replies, answer it).
- Director requests: `director_requests.md` (root) — entry 1 (Claim Sheet review) non-blocking, awaiting director reply.
- My foundation `agents/Claude/Literature Foundation.md` · ledger `agents/Claude/references.md` (**no S20–S23 entries — reproduction/construction/measurement sessions, no external sources read**) · progress reports `agents/Claude/Progress Reports/` (Phase 0/1 Close, Session 8, Session 16). **NEXT ONE IS DUE: Session 24.**
- Live-Run README (co-maintained): root `README.md` — **Phase 2 / In Progress**; **my S23 entry carries only the jointly-approved severity-grid correction and the fact that two consecutive reviews each caught a real error in the other agent's work.** It claims nothing about my un-reviewed boundary screen — **the next public entry should carry whatever we jointly conclude about it.**
- Scratchpad (not committed, outside repo, session `02c1e7b4…`): **`append_turn.py`** (EOF-append with hard gates — reuse for every chat turn), **`s23_dryrun.py`** (analysis-path dry run — reuse before every screen), **`s23_verify.py`** (60-check audit of Codex's artifacts), **`s23_selfaudit.py`** (38-check audit of my own — the reusable template), `s23_regen.py` (regenerate a report from its committed summary without re-running rollouts). Earlier sessions' probes are under `3ecd13a3…` (S22) and `968ad429…` (S20–S21).
