# Summary of Only Necessary Context — Claude

*Rewritten every session. Restores my working context for the next session. Excludes anything already in `Project Details/Project Details.md` and `AgentPrompt.md` (I re-read those in full at session start). Last rewritten: end of Session 22, 2026-07-22 18:12 PDT.*

## Where the project is

- **Phase 2 (Execution) is OPEN.** All Phase-1 gates closed and in force. **Schema v1.0 + Amendment A1 (contact/safety roles) are jointly in force.** Contract changes run through the **amendment protocol**, not casual editing.
- I am **Claude**; last session was **Session 22**; next session I run is **Session 23**.
- **Next regular director progress report: my Session 24.** (Phase-0-close, Phase-1-close, Session-8, Session-16 reports exist. S17–S22 closed no phase and wrote no Claim-Sheet amendment → no trigger. S23 needs NO progress report unless a phase closes or a Claim-Sheet amendment is approved. **S24 does.**)
- **`config.json` is deliberately NOT frozen.** Current role hashes are `dev-`; no `dev-` trace may enter confirmatory analysis.
- **Packet: 218 tests green** (199 through S21; +19 from my S22 severity-quality screen).

## Review-cycle state (READ THIS FIRST next session)

- **The deficit-screen loop is CLOSED.** Codex owner-re-reviewed my S21 units correction, accepted it, made one narrowing edit to a generated interpretation claim, and approved. In S22 I re-reviewed that edit and **approved same-state.** Do not reopen.
- **ONE LOOP IS OPEN, AND IT IS MINE, HANDED TO CODEX FOR FIRST REVIEW.** My S22 work: `utils/estimator.py` (`SeverityRidgeHead` + `_SCORE_STD_FLOOR` share), `scripts/screen_severity_estimation_quality.py`, `tests/test_severity_estimation_quality.py`, the four artifacts in `results/severity_estimation_quality/`, packet **Step 15** + the 15→19 renumbering, and the root Live-Run entry. **I explicitly approved the state I handed off.**
  - **Next session, first job: read Codex's S22 turn.** If it approved same-state → closed. If it edited and handed back → genuinely re-review its edits *and* its diagnosis, then approve or edit again. Escalate a specific non-converged point to Randy after ~2 round-trips.
- **My S22 turn is the physical tail** of the active Phase-2 chat (posted 2026-07-22 18:11 PDT; file 1705 → **1818 lines**; my header at line 1709, occurs once, physically last). Appended by direct EOF write with hard post-write gates (+113/−0 by `git numstat`).
- **MONITORING DUTY IS STANDING.** It fired twice (Codex's S20 and S21 approvals both landed mid-file at line 1,331; Codex's own verifier caught both and repaired append-only; I verified the S20 one at git level as +72/−0). Both occurrences are logged for Randy in `chats/Claude-Codex-Human/Transcript Order Monitoring/` (Active), with no action requested of him. **The sharpened rule (Codex's S21 lesson): it is not enough to verify a unique multi-line EOF anchor — the patch must use that complete verified block as its context.** My own approach now sidesteps this entirely: `scratchpad/append_turn.py` appends at the true EOF and asserts header-uniqueness, position-after-boundary, Claude-last, and a +N/−0 diff. **Reuse it.**

## THE HEADLINE OF S22 — carry this into everything

**Severity-estimation quality was the last unmeasured route to a non-zero paired S−C1 control quantity on the actuator class. I measured it. It closes, for two independent reasons.**

**(A) The action is severity-blind exactly where it has headroom.** The actuator multiplier is `min(1/max(ŝ, minimum_gain_remaining), maximum_gain_compensation)` — **flat below `1/cap`**. I pinned my analytic version against the real `GainScheduledRecoveryController` over 40 severities × 4 caps: max disagreement **4.4e-16**. At the recorded cap 2.0 the flat region is `ŝ ≤ 0.5`. Crossed against Codex's recorded deficits:

| remaining gain | no-action deficit | exact-restoration ceiling | severity-sensitive? | ceiling ≥ 10% bar? |
|---:|---:|---:|:--:|:--:|
| 0.85 | +2.69% | +2.62% | **yes** | no |
| 0.70 | +6.28% | +5.91% | **yes** | no |
| 0.50 | +13.20% | +11.66% | no | **yes** |
| 0.25 | +23.16% | +18.81% | no | **yes** |
| 0.10 | +65.73% | +39.66% | no | **yes** |

**The two columns never both say yes — the reachable set is EMPTY at the recorded cap.** Smallest cap with any reachable severity = **3.0**, and it reaches only 0.50. **`minimum_gain_remaining = 0.25` bounds the sensitive interval from below**, so cap and floor are a *joint* constraint, not one tunable.

**(B) There is no severity advantage to spend anyway.** 70 no-action arms, severity grid `{1.00, 0.85, 0.70, 0.55, 0.40, 0.25, 0.10}`, tuning seeds 17000–17005, disjoint assessment 17100–17103:

| suite | active features | held-out MAE | RMSE | worst | bias |
|---|---:|---:|---:|---:|---:|
| C1 | 110 / 144 | **0.0060** | 0.0090 | 0.0265 | +0.0048 |
| S | 142 / 144 | **0.0080** | 0.0101 | 0.0184 | +0.0063 |

**C1 is BETTER.** The 32 gauge columns cost accuracy rather than adding it. **Mechanistically expected — and that's why I believe it:** C0 already carries *commanded actuation*, the actuator fault acts *downstream* of it, so commanded torque + resulting encoder motion bracket the remaining gain directly. Strain is redundant there.

**(A×B) Pushed back through the real multiplier:** at cap 2.0 the suites command **identically on all 12 capped-region arms** (both 100% oracle-identical). They differ on 15/28 arms overall but by mean |Δmultiplier| **0.0096** (worst 0.0417), and every difference lands on a setting whose ceiling is below the bar.

**⇒ The recorded 0.0000% paired quantity on the actuator class is a property of the ACTION FAMILY, not an artifact of the pinned stand-in severity. A better severity read-out cannot change it.**

**Two nuances I did NOT predict — carry them:**
1. **At cap ≥ 4 the flat boundary coincides exactly with the 0.25 floor**, and a real estimate of a true 0.25 fault lands at **≈0.256** — just above it. So 4/8 capped-region arms differ at cap 4+, oracle-identity drops to 50%. **Correct narrow statement: 0.10 is severity-blind at every cap; 0.25 is blind only while cap ≤ 3.** Not a path (differences ≈5% of a 3.9× multiplier, and C1 is the more accurate suite), but the cap sweep will hit it. **Argument against reciprocal cap/floor values** — that is what makes the boundary degenerate.
2. **On healthy arms S reproduces the no-action command 75% vs C1's 25%.** S is better at *not* acting on a sound body. A false-authorization difference, not a control-bar one — but that is the axis `safety_incident_rate` has been blind to three times.

## Correction I carried forward in S22 (do not re-litigate)

In S21 I called the paired quantity on the actuator class "arithmetically pinned at zero" because both suites diagnose the class identically. That had a hole: **the action is severity-conditioned**, so suites agreeing on the class can still differ if they size the fault differently — and the recorded 0.0000% came from a stand-in that pins severity identically *by construction*. S22 measured it; the conclusion survives, on better grounds.

## THE SHAPE OF THE CONTROL LAYER (recorded, not inferred)

From Codex's committed `bounded_noisy_information_review/summary.json` — the four representative S-vs-C1 pairs:

| source | C1 gate state | S gate state | suite-informed | `s_tracking_change_pct` |
|---|---|---|---|---:|
| healthy | correct_no_action | correct_no_action | no | 0.0000% |
| **structure** | withheld_actionable_fault | correct_actionable | **yes** | **−18.5762%** |
| **actuator** | correct_actionable | correct_actionable | no | **0.0000%** |
| **sensor** | correct_no_action | correct_no_action | no | **0.0000%** |

C1 per-class recall there: structure **0.083**, actuator **1.000**, sensor **1.000** (S: 1.000 on all three).

**⇒ Where S has exclusive information there is no control headroom; where there is control headroom S has no exclusive information — now established for SEVERITY as well as detection.** Any future control-layer plan must answer this table first.

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

## The single most important things to do next session (Session 23)

1. **Check Codex's S22 turn** for its first review of my severity screen. Approve-same-state → closed; edited-and-handed-back → genuinely re-review both its edits and its diagnosis.
2. **Hold the next action screen to the reachability gate.** Before any rollout, a candidate (condition × cap × floor) must be severity-sensitive **and** clear the bar under exact restoration. That filter excludes every actuator setting on the current grid at the recorded cap, in seconds. **If Codex sweeps the cap alone, point at the floor:** `(maximum_gain_compensation, minimum_gain_remaining)` is the real control surface.
3. **Build the held-out severity uncertainty** — mine. `SeverityRidgeHead.train_residual_std` is an *in-sample* number (C1 0.0024, S 0.0021) and must NOT be handed to `_confident_source`, which gates on `severity_uncertainty ≤ 0.25`. A held-out (e.g. leave-one-seed-out) uncertainty is the missing piece before the read-out can be wired to the controller. **`results/severity_estimation_quality/window_features.csv` holds the extracted features, so this needs NO new rollouts.**
4. **The class-probability channel is now the only unexamined route** to a suite difference on a class both call correctly: multiplier = `1 + p·(capped−1)`. My screen pins `p = 1` on both suites. Nothing has measured a suite difference in *calibrated* class probability, and the recorded one-hot prototype probabilities are explicitly not calibrated.
5. **No progress report due S23** (next regular = S24).
6. **Deferred, still blocked (do NOT build early):**
   - The learned attribution rungs (`TemporalAttributionNet` headline + `RMALatentEncoder`) — need PyTorch CUDA build, GPU-verified sm_120, installed *at that point*; + frozen config + confirmatory data.
   - The §D deployable-loader leakage test + whole-trajectory/fault-setting split audit — need real multi-run storage.
   - The eval **driver** ([t_c, t_c+5 s] slicing → paired C1-vs-S control comparison) — needs the frozen data layout.

**Do NOT freeze a partial config.** Open freeze items: **`minimum_gain_remaining` as a JOINTLY-binding constant with `maximum_gain_compensation` (NEW, S22 — they are not independent knobs)**; **the class-probability channel (NEW, S22)**; the actuator action screen itself; validation-sized healthy threshold calibration (≥~100 values) **with per-suite probability calibration**; the ambiguous-case fault library that makes abstention testable at all (my S19 note); severity/onset grids; joint sanity-check of non-load-bearing sensor constants; validation-frozen class/abstention/selective/OOD thresholds; the reference-lifecycle choice (single held decision vs. a temporal model over the full post-probe trajectory); the **bounded task/contact/controller profile** (`z=0.200 m` + PD gains `(0.05,0.03)`/`(0.005,0.003)` + torque limits `(0.20,0.10)` + timing are *dev candidates*, NOT frozen margins); `W`/stride (**768/16** pilot-advanced, still not frozen); split/leakage/storage/hash audits. *(The S21 "severity-estimation quality" item is now MEASURED for the actuator class under a linear read-out — narrow it, don't delete it.)*

## My lanes — current state (reference for next builds)

`Reproducibility Packet/scripts/utils/estimator.py` (**stable through S13; UNCHANGED S14–S21; S22 added one class + one shared constant, in review**):
- **Window front-end `WindowFeatureExtractor(window_steps=W=768, probe_frequency_hz=0.8)`**: fixed `[W,D]` left-padded tensor + per-column summary `[last, mean, std, slope, sync_cos, sync_sin, sync_amplitude, valid_fraction]`, suite-agnostic over the 18-col registry → **144 features**. Constants: `N_FEATURE_STATS=4`, `N_EXTRA_FEATURES=4`, `SYNC_COS_FEATURE_COL=4`, `SYNC_SIN_FEATURE_COL=5`, `SYNC_AMPLITUDE_FEATURE_COL=6`, `VALID_FRACTION_COL=7`, `DIAGNOSTIC_PROBE_HZ=0.8`, `MIN_SYNC_SAMPLES=8`.
- **`WindowNoveltyDetector`**: interpretable detect + calibrated-abstention; consumes cos/sin as per-feature z-scores. Latches `detection_time_s` after `persistence` consecutive over-threshold windows.
- **`CoefficientReferenceDetector`**: second interpretable detection rung; joint healthy-standardized coefficient distance `‖(coeff_live−mean)/scale‖/√D` (module-level `synchronous_coefficient_vector` + `coefficient_reference_distance`, the canonical statistic every pilot/screen imports). Detection-only, abstains on type. `fit_reference` atomic; re-fit invalidates threshold + resets latch. `calibrate_threshold` FAILS LOUD below `ceil(min_tail/far)` (≥100 at far=0.05).
- **NEW S22 — `_SCORE_STD_FLOOR = 1e-3`** is now a module constant shared by both interpretable rungs (`WindowNoveltyDetector`'s LOO std floor and `CoefficientReferenceDetector.update`'s `null_std`). **This closes the nit I carried from S13 and is provably a NO-OP on every recorded artifact:** the committed `bounded_noisy_information_review/summary.json` records `detect_threshold = 1.2812…` (95th pct) and `calibration_null_max = 1.4710…`; a 100-value set with ≥95 values ≤1.281 and one ≥1.471 has std ≥ ~0.04 by the two-point bound.
- **NEW S22 — `SeverityRidgeHead`** (in review): the project's first *deployable* severity read-out. Standardized closed-form ridge on the `WindowFeatureExtractor` summary; no new dependency, no training loop. **Suite-agnostic structurally**: a channel a suite lacks is all-zero → exactly zero training variance → standardizes to 0 → cannot enter the fit. `fit`/`predict`/`is_fitted`/`n_train`/`train_residual_std`/`active_feature_count`; fails loud on shape/finiteness/<2 windows; clips predictions into `severity_bounds`. **`train_residual_std` is IN-SAMPLE — do not feed it to a confidence gate.**
- **`OracleInterface(onset_time_s)`**: allowlisted privileged ceiling, causal. **`EstimatorCommandPolicy`**: the `run_online_rollout` `CommandPolicy` adapter (diagnosis→control socket; runs estimator every `stride`, **ZOHs the estimator OUTPUT but calls `recovery_command` EVERY step**).
- **`RECOMMENDED_WINDOW` = (W=768, stride=16)** — pilot-advanced, still a pilot proposal.
- **Learned rungs (specified, not built):** `TemporalAttributionNet` (headline) + `RMALatentEncoder`. Post-freeze. Do NOT ship untrained shells.

`Reproducibility Packet/scripts/screen_severity_estimation_quality.py` + tests + results (**S22, mine, in review**). Pure functions: `gain_action_multiplier` (**pinned to the real controller by a regression test — keep that test**), `severity_sensitive_interval`, `exact_restoration_ceiling_pct`, `action_sensitivity_map`, `compare_commanded_actions` (with a capped-region split), `compare_against_oracle_action` (**three regimes: capped / sensitive / identity** — the healthy anchor is its own case, folding it into "flat" understates the capped rate; I caught that by reading my own first run). `WindowCaptureEstimator` grabs the window at `first_decision_step` and returns healthy so no action fires. **One S rollout per arm, projected to C1 via `project_observed_suite` — verified against real C1 sessions on 3 spread arms at 0.000e+00 / 0.000e+00.** Reads Codex's committed `candidate_summary.csv`, so it must run after Step 14.

`Reproducibility Packet/tests/test_recovery_seam.py` (**built S14; jointly approved S15; UNCHANGED S16–S22**): shared end-to-end mechanism regression driving `CablePlant → OnlineSensorSession → EstimatorCommandPolicy → GainScheduledRecoveryController`. 4 tests. Asserts applied/delivered torque only; labeled NOT a `J_5s`/safety result.

`Reproducibility Packet/scripts/utils/metrics.py` + `utils/stats.py` (**jointly approved through S11; unchanged S12–S22**): two-layer success-bar metrics. **`tracking_reduction_pct(j_c1, j_s) = 100·(J_C1−J_S)/J_C1` — the contract's control quantity, C1 in the denominator.** `j_5s` has a fail-loud guard requiring the full `[t_c, t_c+5 s]` window (independently confirmed S20 84 arms, S21 36 arms, both 0.000e+00). **`safety_incident_rate` is a threshold-crossing count and cannot score a graded margin change in either direction** (S19, S20, S21, and S22's healthy false-authorization contrast). `stats.py` = crossed pair×seed paired hierarchical bootstrap. Eval **driver** (argparse CLI) owns the exact slice — build once frozen data layout exists.

## Codex's lanes — current state

`Reproducibility Packet/scripts/screen_fault_tracking_deficit.py` + tests + `results/fault_tracking_deficit_screen/` (**Codex S20; my S21 units correction; Codex's S21 narrowing edit; my S22 same-state approval → JOINTLY APPROVED, loop CLOSED**). No-recovery severity sweep on the fixed bounded condition: structure remaining EI `{0.75,0.50,0.25,0.10,0.05}`, actuator remaining gain `{0.85,0.70,0.50,0.25,0.10}`, fixed sensor control (encoder bias 0.05 rad on a healthy plant). Tuning seeds 16000–16002, disjoint assessment 16100–16103, 12 cases × 7 seeds = 84 arms. **Gate: `required_reduction_pct` = bar+margin = 12%, `required_deficit_pct` = `R/(1−R)` = 13.636%.** Selection = `actuator_gain_remaining_0p25`; decision `ADVANCE_ACTUATOR_DEFICIT_ONLY_BLOCK_STRUCTURAL_DEFICIT`. Artifact hashes: `bfe0eb66…` / `7cfcc104…` / `ed265cfb…` / `a7e2998d…` / report `f8ee1dfd…`.

`Reproducibility Packet/scripts/utils/recovery_control.py` — `GainScheduledRecoveryController` + `RecoveryControlConfig` (S12; approval S13) + `command_from_nominal` (S17; approval S18) + `structural_action ∈ {derate, inverse_stiffness}` × `scope ∈ {global, localized}` (S19; approved S20). `_confident_source` gate = not abstained AND unique argmax==source AND p≥0.5 AND finite uncertainty ≤0.25. **Load-bearing constants: `maximum_gain_compensation = 2.0`, `minimum_gain_remaining = 0.25`, `torque_abs_limit = (1.0, 0.5)`. S22 established these two are a JOINT constraint on whether severity quality can matter at all.**

`screen_structural_recovery_action.py` + tests + results (**Codex S19; my S20 edits; approved S20 → CLOSED**). Recorded `BLOCK_STRUCTURAL_RECOVERY_ACTION_FAMILY`. Robust grounds: ~70% of the selected action's benefit is produced at the *unfaulted* joint, and the structural no-action deficit is ~0.05%. The −0.263 pp specificity margin's sign is NOT established (flips under a legitimate noise replicate).

`run_bounded_noisy_information_review.py` + tests + results (**Codex S18; my S19 edits; approved → CLOSED**). **S PASSES information + action gates (macro-F1 0.995, 100% per-fault detection, 2.1% healthy FA); C1 BLOCKS (0.704, 8.3% structural recall, 4.2% FA); the recovery-control profile BLOCKS.** Holds the four representative S-vs-C1 pairs above.

`utils/task_control.py` (S17; approval S18) — `BoundedTaskProfile` (rest → `(0.30,0.30)` rad by 3.0 s → hold → back to rest by 5.0 s), `ObservedJointControllerConfig` (kp `(0.05,0.03)`, kd `(0.005,0.003)`, torque limits `(0.20,0.10)`), `ObservedJointPDController` (reads ONLY delivered `q_obs`/`qd_obs`; peak command ≈10% of its limits, so the clip never binds), `EstimatorRecoveryTaskPolicy`.

`utils/cable_mechanics.py` + `utils/cable_plant.py` + `make_mujoco_plant_trace.py` — plant lane + endpoint-contact extraction (S14; approval S15). **A1 safety flags** = `|q|>π`, `|qd|>10`, 3-D tip radius > 0.82 from `[0,0,0.5]`, `max|gauge|>500 µε`, `contact_state[0]>5 N`. **The 3-D workspace flag is NOT reconstructable from the record's 2-D `true_task_output`.** **Fault severity is the REMAINING fraction** for both structure (remaining EI) and actuator (remaining gain).

`screen_bounded_task_contact.py` (S17; approval S18) — `BoundedTaskContactSpec`, `cable_config`, `SingleDecisionHoldEstimator` (one evaluation at `first_decision_step` = 1136 = 2.272 s, held causally), `FixedSourceStandIn` + `_output_for_source` (**severities PINNED, do not track the true fault** — that is why the stand-in yields only 6.27% on the 0.50-remaining condition).

`run_noisy_reference_pilot.py` (S11 — also home of **`project_observed_suite`**, which my S22 screen imports), `screen_optional_contact_profile.py` (S15), `run_matched_contact_pilot.py` (S16, superseded) — all jointly approved.

## Coherence worth remembering

`utils/synchronous.py` (Codex, S9) is the **single shared harmonic statistic**. `synchronous_coefficient_vector` + `coefficient_reference_distance` in `utils/estimator.py` are the one canonical definition every pilot, screen, and review imports.

The **recovery seam** has both ends jointly exercised (my `EstimatorCommandPolicy` socket + Codex's `GainScheduledRecoveryController`), pinned by `test_recovery_seam.py`. The bounded screen (S17) established that recovery can act *before* contact; the noisy review (S18/S19) that a *real* estimator can supply the label; **S20 that on this condition there is nothing for the structural label to buy; S21 that on classes where there IS something to buy, C1 already has the label; S22 that C1 also already has the SEVERITY, and that the action could not have spent a severity advantage anyway.**

**Contact + the 7th safety flag:** contact reaches deployable suites only through motion/strain (privileged-only otherwise). In closed loop it is NOT suite-invariant. **Design constraint (my S15 note, honored by every screen since): apply the contact profile identically across each matched C1/S CRN pair.** *(S22 corollary: with NO action and a PD controller reading only `q_obs`/`qd_obs`, an S rollout and its C1 projection are bit-identical — verified 0.000e+00. That equivalence is what makes one-rollout-two-suites legitimate, and it holds only because no recovery fires.)*

**Sensor RNG is keyed on `(sensor_seed, pair_id, channel, stream)`** — the `pair_id` string is load-bearing (my S17 harness bug proved it; S20 turned it into a measurement tool; S21 reused Codex's exact `pair_id` to CRN-pair my arms to its rows; S22 used fresh 17xxx seeds so no substream is shared with any other screen).

## The excitation/detection thread — current status (the project's dominant thread)

- **Settled chain:** S9 reframing → probe co-design → S11 noisy-deployable pilot → S12 `CoefficientReferenceDetector` + recovery floor → S13 residual/linear-sysID baseline → S14 loop pinned end-to-end → S15 optional-contact screen → S16 matched contact pilot BLOCKS → S17 bounded redesign clears mechanics/lifecycle → S18 real noisy instrument → S19 reproduced 53/53, edited, approved → structural-action screen BLOCKS → **S20 I reproduced it (50/50 + 84 arms), fixed the ungated baselines, showed the specificity gate flips under a replicate** → Codex's deficit screen → **S21 I reproduced it (42/42 twice + 36 arms), fixed the gate's units, measured ~10.8% total / ~4.7 pp source-specific against a 10% bar** → **S22 loop closed; severity-quality screen (42/42 audit) closes the severity route both ways.**
- **The deployable S advantage IS the structural fault**, confirmed six times (S12, S16, S19, S20, S21's monotone 19→260 µε sweep, S22's null on actuator severity). **C1 is blind on structure, not weakly sighted** (S19). **The structural fault is dynamically silent and then tracking-improving** (S20, S21).
- **The information question is answered on this bounded development condition. The control question is answered negatively for every class screened so far** — structure has no deficit; actuator and sensor have deficits but no S-over-C1 advantage in *detection, classification, or severity*, and the actuator action's source-specific benefit is <½ the bar.
- **Honesty bounds (keep loud):** (1) the deployable floors are **detection**, NOT learned attribution; (2) all rates come from **one fixed fault setting per class**, held-out over sensor noise only; (3) **abstention is untestable on this fault library** (min margin 0.90); (4) full-horizon continuations are **one seed per source/suite**; (5) one-hot prototype probabilities are **not** calibrated probabilities; (6) reference conditioning assumes a scheduled, phase-reset probe + ONE held decision; (7) every control-layer number comes from a condition where the structural fault causes no measurable tracking deficit; (8) the actuator control numbers come from an *oracle-severity* diagnosis, and under the stand-in's pinned severity the same action yields 6.27%; **(9) NEW S22 — the severity result bounds a LINEAR read-out at 42 fit windows, with `p` pinned at 1 on both suites; a learned head could raise both, and the class-probability channel is unmeasured.**

## The headline experiment design

The "does attribution improve control" comparison is wired at the diagnosis→control seam, its control semantics pinned by `test_recovery_seam.py`, its task/contact mechanics by the bounded screen, its *information* path demonstrated with a real noisy estimator. Post-freeze arms: **detection-only rungs → nominal** (control floor); **learned attribution head → active inverse-gain / derate** (headline arm); **RMA latent → blind adaptation**; **oracle → ceiling**. Scored by `J_5s` reduction + no-safety-regression on frozen confirmatory data. **S22 sharpening: do not build this comparison until some class has BOTH an S-exclusive information advantage AND recoverable control headroom. No screened class has both, and the actuator class now fails on three separate channels (detection, classification, severity).**

## Schema v1.0 + A1 mental model (in force)

File: `Reproducibility Packet/schema/schema-v1.0.md` (rendered in `utils/schema_types.py` §B/§0/§C/§E + `utils/estimator.py` §D). **Amendment A1 (in force):** `contact_state[2] = {tip_contact_force_n, tip_contact_active}`; `safety_flag[7]` order = joint_angle_0, joint_angle_1, joint_speed_0, joint_speed_1, tip_workspace, gauge_abs, tip_contact_force. Safety computed from **privileged truth**. Dev thresholds (config values, not frozen): `|q|≤π`, `|qd|≤10`, tip radius ≤0.82 m, `|gauge_true|≤500 µε`, tip contact force ≤5 N.
- **§A** identity/pairing/splits (splits by whole trajectory AND whole fault setting; suite never a split input; CRN within a pair via `utils/rng.py`) — **the S19 gap stands: held-out axes are sensor-seed only.** **§B** privileged `PlantStepState`/`PrivilegedRecord`. **§C** observed record (fixed 18-col registry, unavailable=NaN; `OnlineSensorSession` authoritative). **§D** labels/outputs/causality/leakage. **§E** storage. **§F** frozen constants. **§G** tracking metric `J_5s`.

## The agreed contract's load-bearing specifics (carry this)

- **Sensor suites (controlled variable):** **C0** = joint encoders + commanded actuation · **C1** = C0 + noisy motor-current nominal-Kt torque estimate + one distal 6-axis IMU · **S** = C1 + **four fixed strain/curvature gauge stations** · **O** = privileged oracle. *(S22: C0 carrying commanded actuation is exactly why C1 nails actuator severity — the fault is downstream of it.)*
- **Two settled correctness points:** (1) actuator-gain fault acts *downstream* of the current proxy → C1 not handed true delivered torque; (2) encoder (sensor) fault has a *relational* signature.
- **Success bar (pre-declared, BOTH layers required):** S improves held-out four-way **macro-F1 over C1 by ≥0.05 absolute** (paired 95% excludes zero; every source-class recall diff lower-95% above **−0.02**) **and** reduces the **5-s post-change integral of absolute tracking error by ≥10%** — `100·(J_C1−J_S)/J_C1`, paired 95% excludes zero, **no safety regression** — **under realistic confounds**. Known-class abstention scored as error in headline macro-F1.
- **Failure shapes:** *hypothesis failure* (C1+temporal adaptation matches S — clean negative) vs *method failure*. **Inconclusive shapes (Slot 13):** **diagnostic-only** (attribution improves, control does not — **S20/S21/S22 together make this the near-certain landing**) · fault-specific/bounded · confound-fragile · excitation-dependent.
- **Pre-specification:** bars fixed before the pilot; freeze gauge placement, model/hyperparams, thresholds, analysis window, seeds/scenarios before confirmatory generation. Leakage-free splits. ≥5 training seeds. Paired hierarchical bootstrap.

## Labor split (agreed, unchanged)

- **Codex:** feasibility spike + physics, virtual-gauge extraction, excitation design, interpretable residual/linear-sysID baseline, recovery controller + external-nominal composition, contact/safety extraction, the contact/bounded screens, the matched pilots, the bounded noisy held-decision information review, the structural recovery action family screen, the per-class deficit screen, **the actuator action screen (next — with achievable source-specific reduction as the gate)**, evaluation-sized closed-loop controller comparison (pending).
- **Claude (me):** fault-injection + sensor-realism model, two-layer evaluation harness + metrics + stats, diagnosis-estimator front + window contract + oracle + seam adapter, synchronous-detection floor analysis, shared recovery-seam regression, **the severity read-out + severity-quality screen (S22)**, matched temporal-attribution net + RMA latent (next, needs torch + frozen data), Slot-8 verification demo, default-writer artifacts (Technical Report, Accessible Piece, Study Guide Pass 2 — Codex reviews).
- **Shared:** the plant→signals→estimator schema (+A1), fault library, Reproducibility Packet, references reconciliation (Phase 2), `utils/synchronous.py`. The **"does attribution improve control" headline experiment is shared** at the diagnosis→control seam.

## Constraints / environment (unchanged, load-bearing)

- **Simulation-only, one desktop:** Windows 11, Ryzen 7 8700F (8C/16T), RTX 5060 Ti **16 GB VRAM** (Blackwell/sm_120), 32 GB RAM, Python **3.12.10** in `./venv` (use `.\venv\Scripts\python.exe` / `pip.exe`, never bare). Free/OSS, commercial-use-friendly only.
- **venv has:** numpy 2.5.1, scipy 1.18.0, scikit-learn 1.9.0, matplotlib 3.11.0, mujoco 3.10.0, pandas 3.0.3, control 0.10.2, gymnasium 1.3.0, pytest 9.1.1. **PyTorch NOT installed** — install CUDA build when building the learned rungs (verify sm_120 actually runs), pin immediately. *(S22 used no new dependency — the ridge head is closed-form numpy on purpose.)*
- **Running packet tests:** from `Reproducibility Packet/`, `..\venv\Scripts\python.exe -m pytest tests/` (each test self-inserts `scripts/` on `sys.path`; no conftest). **Running a script: from `Reproducibility Packet/` as `..\venv\Scripts\python.exe scripts\<name>.py`** (NOT from `scripts/`). **Full packet: 218 tests green (S22).** Set `PYTHONIOENCODING=utf-8` when a script prints unicode.
- **Timings (measured):** `run_bounded_noisy_information_review.py` ~12–20 min; `screen_structural_recovery_action.py` ~8 min (43 rollouts); `screen_fault_tracking_deficit.py` ~20 min (84 arms); **`screen_severity_estimation_quality.py` ~7–9 min (73 arms) at 8–10 workers**. One bounded arm ≈ 27 s solo. Run these in the background; PowerShell `Out-File` buffers, so check the file at the end.
- **HARD-WON S22 LESSON — dry-run the analysis path before spending a rollout budget.** My first run crashed after all 70 arms on a missing `to_dict()`. `scratchpad/s22_dryrun.py` exercises the *entire* post-rollout path (fits, every derived table, artifact writing, report determinism) on synthetic rows in the exact returned shape, in seconds. **Do this first, every time.**
- **The packet runbook uses `.\.venv\Scripts\python.exe` throughout** — that is the *packet's own* self-contained venv convention for an outside reader, not our project root `venv`. Both are correct; do not "fix" one into the other.
- **Packet `.gitignore` ignores `*.npz`** (+ caches/logs); small JSON/CSV/MD result artifacts are intentionally tracked. Root `.gitignore` covers `venv/`, `tmp/`, `MUJOCO_LOG.TXT`, caches, LaTeX aux, OS/IDE noise — **verified accurate S22, no change needed.**
- **Software-engineering standard for every script:** `argparse` with `required=True` for input roots (or defaulted project-relative outputs), no hard-coded paths, one clear purpose, shared logic in `utils/`, docstrings, prints progress, fails loud. (`utils/` library modules + `tests/` are the import-not-CLI exception.)
- **Licensing:** code MIT, prose CC BY 4.0. No relaxed standard requested.

## Pointers

- Claim Sheet (in-force contract): `Claim Sheet.md` · plain-language: `Accessible Claim Sheet.md` · Study Guide Pass 1: `Study Guide/Pass 1 - Conceptual Foundation.tex`
- **Shared schema (in force, +A1):** `Reproducibility Packet/schema/schema-v1.0.md`
- **My lanes:** sensor `utils/{schema_types,sensor_model,rng,synthetic_plant}.py`; eval `utils/{metrics,stats}.py`; estimator `utils/estimator.py`; synchronous floor `scripts/analyze_synchronous_detection_floor.py`; shared seam test `tests/test_recovery_seam.py`; **severity screen `scripts/screen_severity_estimation_quality.py` + `tests/test_severity_estimation_quality.py` + `results/severity_estimation_quality/`**.
- **Codex's plant/control lane:** `utils/{cable_mechanics,cable_plant,online_loop,recovery_control,residual_baseline,task_control}.py`, `scripts/{make_mujoco_plant_trace,run_feasibility_spike,run_bounded_burst_sensitivity,screen_synchronous_safe_probe,run_noisy_reference_pilot,screen_optional_contact_profile,run_matched_contact_pilot,screen_bounded_task_contact,run_bounded_noisy_information_review,screen_structural_recovery_action,screen_fault_tracking_deficit}.py` + matching tests + `results/` artifacts.
- **Active Phase-2 chat:** `chats/Claude-Codex/Phase 2 Integration and Config Freeze/…- Active.md` (my S22 turn = tail, **1818 lines**; **one loop OPEN — my severity screen awaits Codex's first review**). Concluded chats have `Summary.md`s.
- **Active director chat:** `chats/Claude-Codex-Human/Transcript Order Monitoring/…- Active.md` (my S21 note + Codex's S21 note; no action requested of Randy — but if he replies, answer it).
- Director requests: `director_requests.md` (root) — entry 1 (Claim Sheet review) non-blocking, awaiting director reply.
- My foundation `agents/Claude/Literature Foundation.md` · ledger `agents/Claude/references.md` (**no S20–S22 entries — reproduction/construction/measurement sessions, no external sources read**) · progress reports `agents/Claude/Progress Reports/` (Phase 0/1 Close, Session 8, Session 16). **Next regular: Session 24.**
- Live-Run README (co-maintained): root `README.md` — **Phase 2 / In Progress**; **my S22 entry carries the units correction publicly** (Codex's prior entry recorded the superseded 0.50 selection; the log is append-only so the correction was appended, not edited in). It claims nothing about my un-reviewed severity screen — **the next public entry should carry whatever we jointly conclude about it.**
- Scratchpad (not committed, outside repo, session `3ecd13a3…`): **`append_turn.py`** (EOF-append with hard gates — reuse this for every chat turn), **`s22_dryrun.py`** (analysis-path dry run — reuse before every screen), **`s22_verify.py`** (42-check independent audit of a screen's committed artifacts — the reusable audit template), `s22_smoke.py`, `s22_regen.py`, `s22_final3.txt`. Earlier sessions' probes (`s21_probe.py` — the oracle-severity arm driver, `s21_deficit_audit.py`, `s20_*`) are under session `968ad429…`.
