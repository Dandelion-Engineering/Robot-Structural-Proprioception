# Summary of Only Necessary Context — Claude

*Rewritten every session. Restores my working context for the next session. Excludes anything already in `Project Details/Project Details.md` and `AgentPrompt.md` (I re-read those in full at session start). Last rewritten: end of Session 24, 2026-07-22 21:50 PDT.*

## Where the project is

- **Phase 2 (Execution) is OPEN.** All Phase-1 gates closed and in force. **Schema v1.0 + Amendment A1 (contact/safety roles) are jointly in force.** Contract changes run through the **amendment protocol**, not casual editing.
- I am **Claude**; last session was **Session 24**; next session I run is **Session 25**.
- **The Session-24 progress report is WRITTEN.** Next regular one is **Session 32** (cadence 8/16/24/32), unless a phase transition or approved amendment triggers one sooner.
- **`config.json` is deliberately NOT frozen.** Current role hashes are `dev-`; no `dev-` trace may enter confirmatory analysis.
- **Packet: 299 tests green** (248 through Codex's S23; +51 from my S24 probability-channel screen).

## Review-cycle state (READ THIS FIRST next session)

- **The cap-boundary loop is CLOSED.** I re-reviewed Codex's three S23 corrections, reproduced all three from upstream artifacts (40/40 checks), and **approved same-state without editing.** Do not reopen.
- **ONE LOOP IS OPEN, AND IT IS MINE, HANDED TO CODEX FOR FIRST REVIEW.** My S24 work: `scripts/screen_actuator_probability_channel.py`, `tests/test_actuator_probability_channel.py` (51 tests), the three artifacts in `results/actuator_probability_channel/`, packet **Step 17** + the 17→21 renumbering + two stale cross-reference fixes, the Current-boundary update, and the root Live-Run entry. **I explicitly approved the state I handed off.**
  - **Next session, first job: read Codex's S24 turn.** Approve-same-state → closed; edited-and-handed-back → genuinely re-review its edits *and* its diagnosis, then approve or edit again. Escalate a specific non-converged point to Randy after ~2 round-trips.
  - I posted **two** turns in S24: the owner re-review (2026-07-22 21:25 PDT, +96/−0) and the handoff (21:44 PDT, +175/−0). File **2024 → 2199 lines**; handoff header at line 2124, occurs once, physically last.
- **MONITORING DUTY IS STANDING.** S24's check was **clean** (Codex's S23 turn at the tail, header line 1948 of 2024) — the second consecutive clean append. I did **not** add a note to `chats/Claude-Codex-Human/Transcript Order Monitoring/`, because the duty is to flag *recurrences* and that thread is meant to stay lean. **Reuse `scratchpad/append_turn.py`** (EOF-append + hard gates: prefix-identical, unique header, position-after-boundary, Claude-last, +N/−0).

## THE HEADLINE OF S24 — the actuator class is now closed on every channel

**`multiplier = 1 + p·(capped − 1)`, and `_confident_source` withholds below `p = 0.5`. At the deficit screen's SELECTED condition (`actuator_gain_remaining_0p25`):**

**(a) The severity channel is STRUCTURALLY DEAD there.** `capped = min(1/max(ŝ,0.25), 2.0)` returns exactly 2.0 for **every** estimate ≤ **0.50**. The true 0.25 sits **24.6× the recorded severity error scale** below that boundary. Verified against the shipped controller across ŝ ∈ {0.01…0.50}; 0.55 leaves the flat region.

**(b) The probability channel is CLOSED AT BOTH ENDS BY RECORDED CONSTANTS** — `source_probability_threshold = 0.5` below, `maximum_gain_compensation = 2.0` above. So `m = 1 + p` exactly, reachable set `[1.50, 2.00]`. **That is why this is a reachable-set span, not an envelope.**

| p | 0.50 | 0.60 | 0.70 | 0.80 | 0.90 | 1.00 |
|---|---:|---:|---:|---:|---:|---:|
| reduction vs no-action | +6.11% | +7.17% | +8.17% | +9.14% | +10.00% | +10.82% |

**In CONTRACT units `100·(J_C1−J_S)/J_C1`:**

| paired quantity | worst | mean | vs 10 pp bar |
|---|---:|---:|---|
| **graded** (both past the gate) | **5.0699 pp** | 5.0162 pp | **below — CLOSED** |
| gate-crossing (one withholds) | 10.8204 pp | 10.8204 pp | clears |

**⇒ Detection, classification, severity accuracy, severity→tracking, AND class probability are ALL closed on the actuator class.** The gate crossing is an *authorization* difference, not a probability-precision one, and both suites call this class correctly with one-hot recorded probabilities.

*(Side observation: my S23 sweep range [1.50, 2.00], which I called "generously wide," is **exactly** the reachable probability range at that condition. I had already measured the probability channel there without noticing.)*

## S24's OTHER RESULT — the cap is the binding limit at the selected condition

**Codex's S23 §5 question answered. The 93.2% realization does NOT carry to 0.25:**

| condition | deficit | analytic ceiling | realized | realization |
|---|---:|---:|---:|---:|
| 0.50 (S23) | 13.11% | 11.59% | 10.81% | **93.2%** |
| **0.25 (selected)** | 23.16% | 18.81% | 10.82% | **57.5%** |

Same direction on all 4 seeds. **Mechanism is structural: at 0.25 exact restoration needs m = 4.00, cap allows 2.00 — cap-saturated throughout.** So `maximum_gain_compensation` is the binding limit on recoverable tracking at the condition Codex's action screen will run on: **42% of recoverable error unrecovered.** Flagged, NOT proposed — raising the cap to 4 recovers more *and* re-opens the severity channel this screen closes. **`(maximum_gain_compensation, minimum_gain_remaining, source_probability_threshold)` is a JOINT surface.**

## THE TWO LESSONS FROM S23→S24 — carry these

**1. Envelope vs. reachable set.** A sweep across a range *I chose* is an **envelope** ("across what I tried, nothing much happened"). A sweep across a range the *system's own constants* close is a **reachable set** ("the machine cannot go outside these, and across all of them nothing much happened"). Codex correctly killed my S23 "bounds ANY read-out" claim — **the counterexample was in my own `arm_rows.csv`**: swept [1.50,2.00] spans 3.81 pp, but full [1.00,2.00] spans **10.81 pp, ABOVE the bar.** In S24 I was entitled to the stronger claim *and could name the two constants that earned it*. **Never claim a bound without naming what closes the range.**

**2. Units, again — and it was mine this time.** I nearly compared the channel's span to the bar in the wrong units. The response curve is reduction-vs-no-action; the contract divides by the **conventional arm**. A difference of two reductions is smaller by `1/(1 − r_low/100)`: **4.7097 pp vs the true 5.0162 pp, understating by 6.5%.** Same class as the S21 catch in Codex's deficit gate, pointed the other way. Caught pre-handoff. **Always restate a proxy quantity in the contract's units before comparing to the bar.**

## S24 FREEZE PROPOSAL — `severity_uncertainty` is an RMS, not a std

`_confident_source` compares `output.severity_uncertainty` to `maximum_severity_uncertainty = 0.25`, and **the schema does not say what statistic that scalar is.** From the Step-15 assessment residuals:

| statistic | C1 | S | better |
|---|---:|---:|---|
| in-sample std | 0.004237 | 0.001951 | S |
| calibration std | 0.006741 | 0.011160 | C1 |
| **assessment std** | 0.008393 | **0.008029** | **S** |
| calibration / assessment MAE | 0.005306 / 0.006472 | 0.009029 / 0.007633 | C1 |
| calibration / assessment RMS | 0.006897 / **0.008585** | 0.011394 / **0.010183** | C1 |

**Std is the ONLY statistic that flips the ranking, because it discards bias — S's assessment bias is +0.006422 vs C1's +0.002336 (2.75×).** Every bias-inclusive statistic agrees across both roles. **A biased-but-tight estimator passes an std gate it should fail, and S is exactly that shape.** My S24 screen implements the RMS choice (`recorded_assessment_rms` + `gate_uncertainty_from_scales`, conservative max across suites = 0.010183, clears the gate by 25×). **Not yet reviewed by Codex.**

## THE SHAPE OF THE CONTROL LAYER (recorded, not inferred)

From Codex's committed `bounded_noisy_information_review/summary.json` — the four representative S-vs-C1 pairs:

| source | C1 gate state | S gate state | suite-informed | `s_tracking_change_pct` |
|---|---|---|---|---:|
| healthy | correct_no_action | correct_no_action | no | 0.0000% |
| **structure** | withheld_actionable_fault | correct_actionable | **yes** | **−18.5762%** |
| **actuator** | correct_actionable | correct_actionable | no | **0.0000%** |
| **sensor** | correct_no_action | correct_no_action | no | **0.0000%** |

C1 per-class recall there: structure **0.083**, actuator **1.000**, sensor **1.000** (S: 1.000 on all three).

**⇒ Where S has exclusive information there is no control headroom; where there is control headroom S has no exclusive information.** Now established for DETECTION, CLASSIFICATION, SEVERITY ACCURACY, SEVERITY→TRACKING (S23), and CLASS PROBABILITY (S24). **Any future control-layer plan must answer this table first.**

## The strongest version of the structural result (from Codex's S20 rows)

| remaining EI | mean peak \|gauge\| | mean tracking deficit |
|---:|---:|---:|
| healthy | 19.2 µε | — |
| 0.75 | 25.0 µε | +0.11% |
| 0.50 | 38.4 µε | +0.08% |
| 0.25 | 72.4 µε | −0.89% |
| 0.10 | 152.8 µε | −2.23% |
| 0.05 | 259.7 µε | −5.00% |

**Monotone in information; monotone the wrong way in control.** 13.5× the healthy strain signature at the severity where tracking is 5% *better* than healthy. The Slot-13 diagnostic-only shape measured across a 15× stiffness sweep. **This is the sentence the write-up gets built on.**

## The single most important things to do next session (Session 25)

1. **Check Codex's S24 turn** for its first review of the probability-channel screen. Watch for pushback on (a) the reachable-set framing, (b) the RMS-not-std freeze proposal, (c) the cap flag.
2. **The actuator class has NO unexamined channels left.** Any future claim that S helps control on this class must come from somewhere other than the action's own parameters — a different action family, a different condition, or a different cap.
3. **The cap ≥ 4 boundary (0.25 floor) is still unmeasured.** At cap 4 the flat severity region shrinks to ŝ ≤ 0.25 and the floor becomes the boundary; all 4 paired arms differ there. If Codex sweeps the cap, that boundary needs the same treatment.
4. **Deferred, still blocked (do NOT build early):**
   - The learned attribution rungs (`TemporalAttributionNet` headline + `RMALatentEncoder`) — need PyTorch CUDA build, GPU-verified sm_120, installed *at that point*; + frozen config + confirmatory data.
   - The §D deployable-loader leakage test + whole-trajectory/fault-setting split audit — need real multi-run storage.
   - The eval **driver** ([t_c, t_c+5 s] slicing → paired C1-vs-S control comparison) — needs the frozen data layout.

**Do NOT freeze a partial config.** Open freeze items: **`severity_uncertainty` = RMS not std (S24, unreviewed)**; `maximum_gain_compensation` / `minimum_gain_remaining` / `source_probability_threshold` as a **JOINTLY** binding triple; the actuator action screen itself; validation-sized healthy threshold calibration (≥~100 values) **with per-suite probability calibration**; the ambiguous-case fault library that makes abstention testable at all (my S19 note); severity/onset grids; joint sanity-check of non-load-bearing sensor constants; validation-frozen class/abstention/selective/OOD thresholds; the reference-lifecycle choice (single held decision vs. a temporal model over the full post-probe trajectory); the **bounded task/contact/controller profile** (`z=0.200 m` + PD gains `(0.05,0.03)`/`(0.005,0.003)` + torque limits `(0.20,0.10)` + timing are *dev candidates*, NOT frozen margins); `W`/stride (**768/16** pilot-advanced, still not frozen); split/leakage/storage/hash audits. *(Severity-estimation quality and the class-probability channel are now MEASURED for the actuator class at the recorded cap — narrow those items, don't delete them.)*

## My lanes — current state (reference for next builds)

`Reproducibility Packet/scripts/utils/estimator.py`:
- **Window front-end `WindowFeatureExtractor(window_steps=W=768, probe_frequency_hz=0.8)`**: fixed `[W,D]` left-padded tensor + per-column summary `[last, mean, std, slope, sync_cos, sync_sin, sync_amplitude, valid_fraction]`, suite-agnostic over the 18-col registry → **144 features**. Constants: `N_FEATURE_STATS=4`, `N_EXTRA_FEATURES=4`, `SYNC_COS_FEATURE_COL=4`, `SYNC_SIN_FEATURE_COL=5`, `SYNC_AMPLITUDE_FEATURE_COL=6`, `VALID_FRACTION_COL=7`, `DIAGNOSTIC_PROBE_HZ=0.8`, `MIN_SYNC_SAMPLES=8`.
- **`WindowNoveltyDetector`**: interpretable detect + calibrated-abstention; consumes cos/sin as per-feature z-scores. Latches `detection_time_s` after `persistence` consecutive over-threshold windows.
- **`CoefficientReferenceDetector`**: second interpretable detection rung; joint healthy-standardized coefficient distance `‖(coeff_live−mean)/scale‖/√D` (module-level `synchronous_coefficient_vector` + `coefficient_reference_distance`, the canonical statistic every pilot/screen imports). Detection-only, abstains on type. `fit_reference` atomic; re-fit invalidates threshold + resets latch. `calibrate_threshold` FAILS LOUD below `ceil(min_tail/far)` (≥100 at far=0.05).
- **`_SCORE_STD_FLOOR = 1e-3`** shared by both interpretable rungs (S22; jointly approved S23). Provably a no-op on every recorded artifact.
- **`SeverityRidgeHead`** (S22; jointly approved S23): the project's first *deployable* severity read-out. Standardized closed-form ridge on the `WindowFeatureExtractor` summary; no new dependency, no training loop. **Suite-agnostic structurally**: a channel a suite lacks is all-zero → exactly zero training variance → standardizes to 0 → cannot enter the fit. **`train_residual_std` is IN-SAMPLE — never feed it to a confidence gate.**
- **`leave_one_group_out_residuals(features, severities, groups, *, regularization, severity_bounds)`** (S23; **APPROVED UNCHANGED by Codex**): refits the head once per held-out group, returns `[N]` out-of-sample residuals in input order. Group by **sensor seed**. **Codex's S23 correction: with the penalty selected on the same groups, this is a CALIBRATION-ROLE diagnostic, not a disjoint held-out estimate.** The disjoint role is Step 15's recorded assessment `predictions`.
- **`OracleInterface(onset_time_s)`**: allowlisted privileged ceiling, causal. **`EstimatorCommandPolicy`**: the `run_online_rollout` `CommandPolicy` adapter (diagnosis→control socket; runs estimator every `stride`, **ZOHs the estimator OUTPUT but calls `recovery_command` EVERY step**).
- **`RECOMMENDED_WINDOW` = (W=768, stride=16)** — pilot-advanced, still a pilot proposal.
- **Learned rungs (specified, not built):** `TemporalAttributionNet` (headline) + `RMALatentEncoder`. Post-freeze. Do NOT ship untrained shells.

`scripts/screen_severity_estimation_quality.py` + tests + `results/severity_estimation_quality/` (**JOINTLY APPROVED, CLOSED S23**). Grid `(1.00, 0.85, 0.70, 0.55, 0.50, 0.40, 0.25, 0.10)`, 80 arms. Held-out MAE **C1 0.0065 / S 0.0076**. `window_features.csv` is the durable product — refits need no rollouts.

`scripts/screen_severity_action_boundary.py` + tests + `results/severity_action_boundary/` (**S23 mine; Codex's S23 corrections; my S24 same-state approval → JOINTLY APPROVED, CLOSED**). 40 arms. Post-correction names: `cross_seed_calibration_uncertainty`, `disjoint_assessment_residual_diagnostics`, `severity_difference_envelope` (**not** `bound_from_slope`), `require_passing_audit` (7 gates). Paired **−0.1177%** mean / 0.5154% worst.

`scripts/screen_actuator_probability_channel.py` + `tests/test_actuator_probability_channel.py` + `results/actuator_probability_channel/` (**S24, mine, IN REVIEW**). 36 arms = 4 seeds × {no_action, healthy_reference, gate_probe, probability_{0.50,0.60,0.70,0.80,0.90,1.00}}. Key functions: `recorded_assessment_rms`, `gate_uncertainty_from_scales`, `reachable_multiplier_set`, `expected_multiplier`, `severity_channel_is_flat`, `ProbabilityDiagnosisEstimator` (spreads `1−p` over the other 3 classes so actuator stays unique argmax; **rejects p too small for that**), `build_arm_specs`, `run_probability_arm`, `probability_response_curve`, `gate_discontinuity`, **`paired_channel_extremes`** (the contract-units function), `restoration_realization`, `build_audit` + `require_passing_audit` (7 gates). **CRN: reuses the deficit screen's `pair_id` (`fault-deficit-assessment-<seed>`) — 8/8 reference arms at 0.000e+00, `main()` aborts otherwise.** Runtime ~6 min at 8 workers.

`tests/test_recovery_seam.py` (**built S14; jointly approved S15; UNCHANGED S16–S24**): shared end-to-end mechanism regression driving `CablePlant → OnlineSensorSession → EstimatorCommandPolicy → GainScheduledRecoveryController`. 4 tests. Asserts applied/delivered torque only; labeled NOT a `J_5s`/safety result.

`utils/metrics.py` + `utils/stats.py` (**jointly approved through S11; unchanged S12–S24**): **`tracking_reduction_pct(j_c1, j_s) = 100·(J_C1−J_S)/J_C1` — the contract's control quantity, C1 in the denominator.** `j_5s` has a fail-loud guard requiring the full `[t_c, t_c+5 s]` window. **`safety_incident_rate` is a threshold-crossing count and cannot score a graded margin change.** `stats.py` = crossed pair×seed paired hierarchical bootstrap. Eval **driver** (argparse CLI) owns the exact slice — build once frozen data layout exists.

## Codex's lanes — current state

`scripts/screen_fault_tracking_deficit.py` + `results/fault_tracking_deficit_screen/` (**JOINTLY APPROVED, CLOSED S22**). No-recovery severity sweep: structure remaining EI `{0.75,0.50,0.25,0.10,0.05}`, actuator remaining gain `{0.85,0.70,0.50,0.25,0.10}`, fixed sensor control. Tuning 16000–16002, **assessment 16100–16103**, 84 arms. **Gate: `required_reduction_pct` = 12%, `required_deficit_pct` = `R/(1−R)` = 13.636%.** Selection = **`actuator_gain_remaining_0p25`** (mean deficit 23.16%). *(S23 caveat: the conversion is an upper bound — realization is 93.2% at 0.50 and, per S24, **57.5% at 0.25**.)*

`utils/recovery_control.py` — `GainScheduledRecoveryController` + `RecoveryControlConfig` (S12/S13) + `command_from_nominal` (S17/S18) + `structural_action ∈ {derate, inverse_stiffness}` × `scope ∈ {global, localized}` (S19/S20). `_confident_source` gate = not abstained AND unique argmax==source AND **p ≥ `source_probability_threshold` = 0.5** AND finite uncertainty ≤ `maximum_severity_uncertainty` = 0.25. **Actuator branch verbatim: `multiplier = 1.0 + probability * (capped_compensation - 1.0)`.** **Load-bearing constants: `maximum_gain_compensation = 2.0`, `minimum_gain_remaining = 0.25`, `source_probability_threshold = 0.5`, `torque_abs_limit = (1.0, 0.5)`, `maximum_severity_uncertainty = 0.25`.** *(Driving it directly: use a small nominal like `[0.01, 0.02]` — `torque_abs_limit` clips a unit nominal and hides the multiplier.)*

`screen_structural_recovery_action.py` (**CLOSED S20**) — recorded `BLOCK_STRUCTURAL_RECOVERY_ACTION_FAMILY`; ~70% of the selected action's benefit is at the *unfaulted* joint; the −0.263 pp specificity margin's sign is NOT established.

`run_bounded_noisy_information_review.py` (**CLOSED S19**) — **S PASSES information + action gates (macro-F1 0.995, 100% per-fault detection, 2.1% healthy FA); C1 BLOCKS (0.704, 8.3% structural recall, 4.2% FA).** Holds the four representative pairs above. **Accepted prototype calls use one-hot mechanism probabilities — `p = 1` on both suites, explicitly NOT calibrated.**

`utils/task_control.py` (S17/S18) — `BoundedTaskProfile` (rest → `(0.30,0.30)` rad by 3.0 s → hold → back to rest by 5.0 s), `ObservedJointControllerConfig` (kp `(0.05,0.03)`, kd `(0.005,0.003)`, torque limits `(0.20,0.10)`), `ObservedJointPDController` (reads ONLY delivered `q_obs`/`qd_obs`), `EstimatorRecoveryTaskPolicy`.

`utils/cable_mechanics.py` + `utils/cable_plant.py` + `make_mujoco_plant_trace.py` (S14/S15). **A1 safety flags** = `|q|>π`, `|qd|>10`, 3-D tip radius > 0.82 from `[0,0,0.5]`, `max|gauge|>500 µε`, `contact_state[0]>5 N`. **The 3-D workspace flag is NOT reconstructable from the record's 2-D `true_task_output`.** **Fault severity is the REMAINING fraction** for both structure (remaining EI) and actuator (remaining gain).

`screen_bounded_task_contact.py` (S17/S18) — `BoundedTaskContactSpec`, `cable_config`, `SingleDecisionHoldEstimator` (one evaluation at `first_decision_step` = 1136 = 2.272 s, held causally), `FixedSourceStandIn`. `run_noisy_reference_pilot.py` (S11 — home of **`project_observed_suite`**), `screen_optional_contact_profile.py` (S15), `run_matched_contact_pilot.py` (S16, superseded).

**Codex's next: the actuator action screen** — action-vs-no-action benefit, healthy false authorization, cap/floor sensitivity, source-specific margin.

## Coherence worth remembering

`utils/synchronous.py` (Codex, S9) is the **single shared harmonic statistic**. `synchronous_coefficient_vector` + `coefficient_reference_distance` in `utils/estimator.py` are the one canonical definition every pilot, screen, and review imports.

The **recovery seam** has both ends jointly exercised, pinned by `test_recovery_seam.py`. **S20: on the bounded condition there is nothing for the structural label to buy; S21: on classes where there IS something to buy, C1 already has the label; S22: C1 also already has the SEVERITY; S23: even where a severity difference survives, it converts to <0.6 pp of tracking; S24: and the probability channel's ENTIRE reachable set is worth 5.07 pp against a 10 pp bar.**

**Contact + the 7th safety flag:** contact reaches deployable suites only through motion/strain. In closed loop it is NOT suite-invariant. **Design constraint (my S15 note, honored by every screen since): apply the contact profile identically across each matched C1/S CRN pair.** *(With NO action and a PD controller reading only `q_obs`/`qd_obs`, an S rollout and its C1 projection are bit-identical — verified 0.000e+00. **S23 corollary: with a SINGLE held decision, arms that differ only in the commanded diagnosis are bit-identical up to the decision step** — which is what lets a recorded estimate drive a new acting rollout, and what makes the S24 gate probe bitwise identical to no-action.)*

**Sensor RNG is keyed on `(sensor_seed, pair_id, channel, stream)`** — the `pair_id` string is load-bearing (my S17 harness bug proved it; S20 turned it into a measurement tool; **S23 and S24 both reused an upstream screen's `pair_id` verbatim and checked it at 0.000e+00**).

## The excitation/detection thread — current status (the project's dominant thread)

- **Settled chain:** S9 reframing → probe co-design → S11 noisy-deployable pilot → S12 `CoefficientReferenceDetector` + recovery floor → S13 residual/linear-sysID baseline → S14 loop pinned end-to-end → S15 optional-contact screen → S16 matched contact pilot BLOCKS → S17 bounded redesign → S18 real noisy instrument → S19 reproduced 53/53 → structural-action screen BLOCKS → **S20 I reproduced it** → deficit screen → **S21 I reproduced it and fixed the gate's units** → **S22 severity-quality screen** → **S23 boundary measured** → **S24 Codex's three corrections approved; probability channel closed.**
- **The deployable S advantage IS the structural fault**, confirmed seven times. **C1 is blind on structure, not weakly sighted** (S19). **The structural fault is dynamically silent and then tracking-improving** (S20, S21).
- **The information question is answered on this bounded development condition. The control question is answered negatively for every class screened so far** — structure has no deficit; actuator and sensor have deficits but no S-over-C1 advantage in *detection, classification, severity accuracy, severity→tracking conversion, or class probability*.
- **Honesty bounds (keep loud):** (1) the deployable floors are **detection**, NOT learned attribution; (2) all rates come from **one fixed fault setting per class**, held-out over sensor noise only; (3) **abstention is untestable on this fault library** (min margin 0.90); (4) full-horizon continuations are **one seed per source/suite**; (5) one-hot prototype probabilities are **not** calibrated probabilities; (6) reference conditioning assumes a scheduled, phase-reset probe + ONE held decision; (7) every control-layer number comes from a condition where the structural fault causes no measurable tracking deficit; (8) the actuator control numbers come from an *oracle-severity* diagnosis, and under the stand-in's pinned severity the same action yields 6.27%; (9) the severity result bounds a LINEAR read-out at 48 fit windows; (10) the S23 boundary result is 4 seeds at ONE cap, and `deficit→reduction` realizes only 93.2% there; **(11) NEW S24 — the probability result is 4 seeds at ONE cap and ONE condition; the reachable-set claim is only as good as the two constants that close it, and at cap ≥ 4 both the flat severity region and the reachable set change.**

## The headline experiment design

The "does attribution improve control" comparison is wired at the diagnosis→control seam, its control semantics pinned by `test_recovery_seam.py`, its task/contact mechanics by the bounded screen, its *information* path demonstrated with a real noisy estimator. Post-freeze arms: **detection-only rungs → nominal** (control floor); **learned attribution head → active inverse-gain / derate** (headline arm); **RMA latent → blind adaptation**; **oracle → ceiling**. Scored by `J_5s` reduction + no-safety-regression on frozen confirmatory data. **Sharpening that survives S24: do not build this comparison until some class has BOTH an S-exclusive information advantage AND recoverable control headroom. No screened class has both, and the actuator class is now exhausted on EVERY channel the action can spend.**

## Schema v1.0 + A1 mental model (in force)

File: `Reproducibility Packet/schema/schema-v1.0.md` (rendered in `utils/schema_types.py` §B/§0/§C/§E + `utils/estimator.py` §D). **Amendment A1 (in force):** `contact_state[2] = {tip_contact_force_n, tip_contact_active}`; `safety_flag[7]` order = joint_angle_0, joint_angle_1, joint_speed_0, joint_speed_1, tip_workspace, gauge_abs, tip_contact_force. Safety computed from **privileged truth**. Dev thresholds (config values, not frozen): `|q|≤π`, `|qd|≤10`, tip radius ≤0.82 m, `|gauge_true|≤500 µε`, tip contact force ≤5 N.
- **§A** identity/pairing/splits (splits by whole trajectory AND whole fault setting; suite never a split input; CRN within a pair via `utils/rng.py`) — **the S19 gap stands: held-out axes are sensor-seed only.** **§B** privileged `PlantStepState`/`PrivilegedRecord`. **§C** observed record (fixed 18-col registry, unavailable=NaN; `OnlineSensorSession` authoritative). **§D** labels/outputs/causality/leakage — **note: it does NOT define what statistic `severity_uncertainty` is; that is my S24 freeze proposal.** **§E** storage. **§F** frozen constants. **§G** tracking metric `J_5s`.

## The agreed contract's load-bearing specifics (carry this)

- **Sensor suites (controlled variable):** **C0** = joint encoders + commanded actuation · **C1** = C0 + noisy motor-current nominal-Kt torque estimate + one distal 6-axis IMU · **S** = C1 + **four fixed strain/curvature gauge stations** · **O** = privileged oracle. *(C0 carrying commanded actuation is exactly why C1 nails actuator severity — the fault is downstream of it.)*
- **Two settled correctness points:** (1) actuator-gain fault acts *downstream* of the current proxy → C1 not handed true delivered torque; (2) encoder (sensor) fault has a *relational* signature.
- **Success bar (pre-declared, BOTH layers required):** S improves held-out four-way **macro-F1 over C1 by ≥0.05 absolute** (paired 95% excludes zero; every source-class recall diff lower-95% above **−0.02**) **and** reduces the **5-s post-change integral of absolute tracking error by ≥10%** — `100·(J_C1−J_S)/J_C1`, paired 95% excludes zero, **no safety regression** — **under realistic confounds**. Known-class abstention scored as error in headline macro-F1.
- **Failure shapes:** *hypothesis failure* (C1+temporal adaptation matches S — clean negative) vs *method failure*. **Inconclusive shapes (Slot 13):** **diagnostic-only** (attribution improves, control does not — **S20–S24 together make this the near-certain landing**) · fault-specific/bounded · confound-fragile · excitation-dependent.
- **Pre-specification:** bars fixed before the pilot; freeze gauge placement, model/hyperparams, thresholds, analysis window, seeds/scenarios before confirmatory generation. Leakage-free splits. ≥5 training seeds. Paired hierarchical bootstrap.

## Labor split (agreed, unchanged)

- **Codex:** feasibility spike + physics, virtual-gauge extraction, excitation design, interpretable residual/linear-sysID baseline, recovery controller + external-nominal composition, contact/safety extraction, the contact/bounded screens, the matched pilots, the bounded noisy held-decision information review, the structural recovery action family screen, the per-class deficit screen, **the actuator action screen (next)**, evaluation-sized closed-loop controller comparison (pending).
- **Claude (me):** fault-injection + sensor-realism model, two-layer evaluation harness + metrics + stats, diagnosis-estimator front + window contract + oracle + seam adapter, synchronous-detection floor analysis, shared recovery-seam regression, the severity read-out + severity-quality screen (S22), the cap-boundary action screen + held-out severity uncertainty (S23), **the class-probability channel screen (S24)**, matched temporal-attribution net + RMA latent (next, needs torch + frozen data), Slot-8 verification demo, default-writer artifacts (Technical Report, Accessible Piece, Study Guide Pass 2 — Codex reviews).
- **Shared:** the plant→signals→estimator schema (+A1), fault library, Reproducibility Packet, references reconciliation (Phase 2), `utils/synchronous.py`. The **"does attribution improve control" headline experiment is shared** at the diagnosis→control seam.

## Constraints / environment (unchanged, load-bearing)

- **Simulation-only, one desktop:** Windows 11, Ryzen 7 8700F (8C/16T), RTX 5060 Ti **16 GB VRAM** (Blackwell/sm_120), 32 GB RAM, Python **3.12.10** in `./venv` (use `.\venv\Scripts\python.exe` / `pip.exe`, never bare). Free/OSS, commercial-use-friendly only.
- **venv has:** numpy 2.5.1, scipy 1.18.0, scikit-learn 1.9.0, matplotlib 3.11.0, mujoco 3.10.0, pandas 3.0.3, control 0.10.2, gymnasium 1.3.0, pytest 9.1.1. **PyTorch NOT installed** — install CUDA build when building the learned rungs (verify sm_120 actually runs), pin immediately. *(S22, S23, and S24 all used no new dependency — closed-form numpy on purpose.)*
- **Running packet tests:** from `Reproducibility Packet/`, `..\venv\Scripts\python.exe -m pytest tests/` (each test self-inserts `scripts/` on `sys.path`; no conftest). **Running a script: from `Reproducibility Packet/` as `..\venv\Scripts\python.exe scripts\<name>.py`** (NOT from `scripts/`). **Full packet: 299 tests green (S24).** Set `PYTHONIOENCODING=utf-8` when a script prints unicode.
- **Timings (measured):** `run_bounded_noisy_information_review.py` ~12–20 min; `screen_structural_recovery_action.py` ~8 min; `screen_fault_tracking_deficit.py` ~20 min (84 arms); `screen_severity_estimation_quality.py` ~7–9 min (80 arms); `screen_severity_action_boundary.py` ~7 min (40 arms); **`screen_actuator_probability_channel.py` ~6 min (36 arms)** — all at 8 workers. Run in the background; **a bash pipe through `tail` buffers everything until exit, so the progress file stays empty — poll for the results file instead** (confirmed again in S24).
- **STANDING LESSON — dry-run the analysis path before spending a rollout budget.** `scratchpad/s24_dryrun.py` exercises the *entire* post-rollout path (every derived table, artifact writing, report determinism, every audit gate forced false) on synthetic rows in the exact returned shape, in seconds. **Do this first, every time.**
- **SECOND STANDING LESSON (new S24) — self-audit the PROSE, not just the numbers.** `s24_selfaudit.py` greps the generated report for overreach patterns ("any read-out", "any possible") and for the presence of the constants that justify each claim. **It caught a real one in my own report.**
- **The packet runbook uses `.\.venv\Scripts\python.exe` throughout** — that is the *packet's own* self-contained venv convention for an outside reader, not our project root `venv`. Both are correct; do not "fix" one into the other.
- **Packet `.gitignore` ignores `*.npz`** (+ caches/logs); small JSON/CSV/MD result artifacts are intentionally tracked. Root `.gitignore` covers `venv/`, `tmp/`, `MUJOCO_LOG.TXT`, caches, LaTeX aux, OS/IDE noise — **verified accurate S24, no change needed.**
- **Software-engineering standard for every script:** `argparse` with `required=True` for input roots (or defaulted project-relative outputs), no hard-coded paths, one clear purpose, shared logic in `utils/`, docstrings, prints progress, fails loud. (`utils/` library modules + `tests/` are the import-not-CLI exception.)
- **Licensing:** code MIT, prose CC BY 4.0. No relaxed standard requested.

## Pointers

- Claim Sheet (in-force contract): `Claim Sheet.md` · plain-language: `Accessible Claim Sheet.md` · Study Guide Pass 1: `Study Guide/Pass 1 - Conceptual Foundation.tex`
- **Shared schema (in force, +A1):** `Reproducibility Packet/schema/schema-v1.0.md`
- **My lanes:** sensor `utils/{schema_types,sensor_model,rng,synthetic_plant}.py`; eval `utils/{metrics,stats}.py`; estimator `utils/estimator.py`; synchronous floor `scripts/analyze_synchronous_detection_floor.py`; shared seam test `tests/test_recovery_seam.py`; severity screen `scripts/screen_severity_estimation_quality.py`; boundary screen `scripts/screen_severity_action_boundary.py`; **probability screen `scripts/screen_actuator_probability_channel.py` + `tests/test_actuator_probability_channel.py` + `results/actuator_probability_channel/`**.
- **Codex's plant/control lane:** `utils/{cable_mechanics,cable_plant,online_loop,recovery_control,residual_baseline,task_control}.py`, `scripts/{make_mujoco_plant_trace,run_feasibility_spike,run_bounded_burst_sensitivity,screen_synchronous_safe_probe,run_noisy_reference_pilot,screen_optional_contact_profile,run_matched_contact_pilot,screen_bounded_task_contact,run_bounded_noisy_information_review,screen_structural_recovery_action,screen_fault_tracking_deficit}.py` + matching tests + `results/` artifacts.
- **Active Phase-2 chat:** `chats/Claude-Codex/Phase 2 Integration and Config Freeze/…- Active.md` (**2199 lines**; my S24 handoff = tail at line 2124; **one loop OPEN — my probability-channel screen awaits Codex's first review**). Concluded chats have `Summary.md`s.
- **Active director chat:** `chats/Claude-Codex-Human/Transcript Order Monitoring/…- Active.md` (two occurrence notes + my S23 clean-check note; no action requested of Randy — but if he replies, answer it).
- Director requests: `director_requests.md` (root) — entry 1 (Claim Sheet review) non-blocking, awaiting director reply.
- My foundation `agents/Claude/Literature Foundation.md` · ledger `agents/Claude/references.md` (**no S20–S24 entries — reproduction/construction/measurement sessions, no external sources read**) · progress reports `agents/Claude/Progress Reports/` (Phase 0/1 Close, Session 8, 16, **24**). **NEXT ONE DUE: Session 32.**
- Live-Run README (co-maintained): root `README.md` — **Phase 2 / In Progress**; **my S24 entry carries the closed fourth channel, the reachable-set-vs-envelope distinction, the 42%-unrecovered cap finding, and my own units catch.**
- Scratchpad (not committed, outside repo, session `26d971b9…`): **`append_turn.py`** (EOF-append with hard gates — reuse for every chat turn), **`s24_dryrun.py`** (analysis-path dry run — reuse before every screen), **`s24_verify.py`** (40-check audit of Codex's corrections), **`s24_selfaudit.py`** (55-check audit of my own, now including prose scanning — **the reusable template**). Earlier sessions' probes are under `02c1e7b4…` (S23), `3ecd13a3…` (S22), `968ad429…` (S20–S21).
