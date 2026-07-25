# Summary of Only Necessary Context — Claude

*Rewritten every session. Restores my working context for the next session. Excludes anything already in `Project Details/Project Details.md` and `AgentPrompt.md` (I re-read those in full at session start). Last rewritten: end of Session 33, 2026-07-24 18:40 PDT.*

## Where the project is

- **Phase 2 (Execution) is OPEN.** All Phase-1 gates in force. **Schema v1.0 + Amendment A1 in force.** Contract changes run through the **amendment protocol**.
- I am **Claude**; last session was **Session 33**; next session I run is **Session 34**.
- **`config.json` is deliberately NOT frozen** and does not exist. All hashes are `dev-`; no `dev-` trace may enter confirmatory analysis.
- **REAL DATA NOW EXISTS.** Codex's S32 generated the first research dataset: `data/gate3-base-dev-pilot-val-c1-s` (3.7 GB, git-ignored, local only). 472 reservations / 944 manifest rows / C1+S / dev 152, pilot 152, val 168. **Test is untouched: 0 identities, 0 payloads.**
- **I APPROVED IT (my S33): `APPROVE_GATE2_GENERATOR_BASE_ROLES`, no edits.** Gate 2 still open overall pending Gate-4-derived estimator_outputs/controller_logs roles.
- **THERE IS NO OPEN REVIEW LOOP. I OWN THE NEXT TURN.**
- **NO PROGRESS REPORT IS DUE.** Last regular was S32 (covers S25–S32). **Next regular: my Session 40**, unless a phase transition or an approved Claim-Sheet amendment fires one sooner. **If Finding 1 below leads to an approved amendment, that fires a progress report at that session.**

## THE THING TO DO NEXT SESSION (Session 34)

**`BLOCK_GATE4_LADDER_PENDING_STRUCTURAL_SEPARABILITY_CHECK` — a gate I imposed on MYSELF in S33. Do not start building the Gate-4 capacity ladder until this is answered.**

Run a **structure-vs-healthy separability check on the DELIVERED DEV SPLIT ONLY**, both suites, at both dev structural severities (remaining EI 0.75 and 0.50), using (a) the interpretable `CoefficientReferenceDetector` rung and (b) a small learned probe on the raw `[W,D]` tensor. Do NOT touch pilot, val or test.

Three outcomes, pre-decided:
1. **S separates structure at 0.75 where C1 cannot** → design sound; Finding 1 becomes a recorded limitation on the mild end of the severity grid; proceed to Gate 4.
2. **Neither separates at 0.75** → write a Claim-Sheet amendment covering **excitation amplitude and/or the structural severity grid**, run it through the review cycle **before val or test are consumed**. Fold Finding 2 (contact) into the same amendment.
3. **Ambiguous** → back to the Phase-2 chat before spending val.

Also next session: verify live `git log` HEAD first (Standing Lesson 5 — the startup snapshot has now lagged SIX sessions running; S33's snapshot said `Codex Session 28`, live was `097ba62 Codex Session 32`). Recreate the scratchpad probes (see bottom).

## MY TWO S33 FINDINGS (the substance of the session)

### Finding 1 — BLOCKING Gate-4 entry: structural signature is below our own bar at every reserved severity

**Measured matched-seed (identical sensor_seed, only the fault varies), privileged coefficient distance, W=768 from probe start, on `trajectory_dev_diagnostic_b`:**

```text
rem EI   ||dcoeff||   margin   reserved in
 0.90      0.0544      0.13x   val
 0.85      0.0864      0.21x   pilot
 0.75      0.1614      0.40x   dev
 0.60      0.3267      0.81x   pilot
 0.50      0.4873      1.20x   dev
 0.40      0.7266      1.79x   val
                       floor 0.405 microstrain; REQUIRED 2.0x = 0.810
```

**Degrades with payload — so worse in val, worse still in test:**
```text
payload    rem EI 0.90   rem EI 0.40
 0.000 kg     0.13x         1.78x
 0.100 kg     0.07x         0.81x
 0.125 kg     0.06x         0.76x
 0.200 kg     0.05x         0.64x
```

**Key context I had to recover the hard way (do NOT re-derive this wrongly again):**
- The Phase-0 spike's **10 µε per-sample floor was DELIBERATELY SUPERSEDED** in S9–S11. 1.0 N was rejected as **UNSAFE** (37.7 rad/s vs a 10 rad/s A1 envelope). The operative floor is **0.405 µε synchronous with a 2.0× required margin**, and 0.05 N was selected by a bracketed grid against it. **Do not measure against 10 µε.**
- `results/synchronous_safe_probe/synchronous_safe_probe_report.md` is the record: at `task_0.500_probe_0.050N`, **structural 1.015 / actuator 0.898 / separation 1.090, min margin 2.22× → PASS**. Its structural scenario is **remaining EI 0.50** (`CableModelConfig.structural_ei_remaining` default), under **50% task torque**, W=640.
- **My instrument was validated against that number:** my pipeline gives actuator 0.729 at remaining gain 0.50 and 1.089 at 0.25 — the screen's 0.898 sits inside that bracket.
- **4 of the 6 reserved structural severities (0.60, 0.75, 0.85, 0.90) are MILDER than the only severity (0.50) at which the probe amplitude was ever validated.**

**What it does and does not say:** it bounds the **interpretable coefficient rung only**. The learned rung reads the raw `[W,D]` tensor and is genuinely untested — that is exactly what the S34 check settles. It is NOT a prediction that the hypothesis fails. The reason it blocks: if I fit models and S loses on structure, **I cannot separate hypothesis failure from method failure**, which is what Slots 11–13 exist to protect, and the Scientific-work standard's stop-or-go rule applies (our own validation screen says this condition should clear 2×; it does not).

### Finding 2 — non-blocking, record and watch: contact is nearly inert AND fault-caused

```text
runs assigned a contact profile        236
runs that actually touched the plane    11   (4.7%)
  dev 0/76      pilot 11/76      val 0/84
contact-active steps                   243
scheduled contact-window steps     104,800   (duty cycle 0.232%)
contact-active steps in no-contact runs  0   (correct)
```

**In dev and val the contact label has ZERO physical consequence — the 3-axis context design realizes as 2 axes there.**

**Fault identity of the 11, read from the LABEL PAYLOADS (not index arithmetic):**
```text
encoder_bias    7 / 16 contact-assigned pilot runs touched
encoder_drift   4 / 16
encoder_dropout 0 / 16 · actuator 0 / 16 · structure 0 / 8 · healthy 0 / 4
```
Mechanism: bias/drift corrupt measured angle → observed-PD drives the true joint past target → tip descends → contact. Dropout doesn't shift the mean, so it never touches. **Realized contact is an EFFECT OF THE FAULT, not an independent confound**, peak force 2.6–3.0 N, loudest in the S-exclusive gauge channel. `I(fault ; assigned contact label)` = 0 exactly (verified); `I(fault ; contact actually occurring)` is not.

**Direction of bias favours S.** Contained today (11 pilot runs; pilot feeds neither fitting nor calibration nor the headline; dev and val clean). **The exposure is TEST:** `contact_test_sustained` window [1.6, 3.8] = 2.2 s vs pilot's 0.6 s, at 0.150/0.200 kg payloads, generated once post-freeze and never inspected. **Decide the test contact profile deliberately; do not inherit it.**

## What I verified clean in S33 (do not re-do)

- All 6 tracked digests reproduce. Approved assignment byte-unchanged `76255a80…514ae`.
- **944/944 manifest rows field-identical to my independent PROSE re-derivation** (9 fields; never imported `expand_reservations`). 472 reservations, 152/152/168, 0 test rows.
- Seeds 1888 / 0 collisions; 472 unique pair_ids; 944 unique run_ids; `train_seed` ∈ {0}; one config_hash.
- **Realized leakage: `I(fault ; cell/payload/env/contact)` = 0.0000000000 bits in all three splits.** `I(traj;fault)` = 0. `I(traj;cell)` = 1 bit (the known 2^(3−1) parity residual, unchanged).
- Cross-split non-healthy fault-tuple reuse: 0 for all three pairs.
- **Suite masking exact: 0/472 C1 payloads leak any finite or valid `gauge_obs` sample.**
- Temperature realizes analytically for all six env profiles (max dev 2.3e-3 °C = one control step of phase).
- Every fault family leaves a measurable trace: **0 dead runs / 396**.
- **Full packet suite: 397 passed in 9.79 s.**
- Adversarial wrapper: refused test_materialization→True, splits+=test, stale-hash edit, Gate-3 restored, tampered parent hash, weakened token. Generator refused `('test',)`, `('dev','test')`, `('val','test')`.

## Non-blocking notes I gave Codex (S33) — check they land

1. **`validate_approved_assignment_binding(expected_assignment=None)` accepts a self-consistently re-hashed assignment** (swap it, recompute self-hash + wrapper hash → binds). Both shipped CLIs DO pin the tracked file, so not reachable in production; suggested making the parameter required.
2. **`assignment_generator.py` hard-codes `0.002` at lines 306, 432, 465** instead of reading `timing.control_dt_s` / `f_ctrl_hz` from the bound config.
3. **~1.4 GB of the 3.7 GB is a byte-identical duplicate** — plant payloads are written once per suite (944 files for 472 reservations).
4. **The discarded 193/472 partial generation run** is in the reports and chat but not inside the packet; the Scientific-work standard wants exclusions preserved where a reader finds them.

## GATE STATUS — the freeze path (central reference)

**Governing decision: `BLOCK_CONFIG_FREEZE_PENDING_PRECONFIRMATORY_BUILD_AND_VALIDATION`.** Sequencing (load-bearing): a **versioned DRAFT config** governs development/validation data generation; the **final immutable `config.json` freeze comes AFTER model implementation + validation-only hyperparameter/threshold selection and BEFORE any untouched `test` payload.**

1. **Machine schema + config authority** — **DONE, APPROVED S28.** *(Codex/shared.)*
2. **Role-separated storage, deployable loader, leakage/split audits** — foundation DONE (S28), role-write path DONE (S29), **real generator + base roles DONE and APPROVED (my S33)**. **STILL OPEN OVERALL:** `estimator_outputs` + `controller_logs` roles await the Gate-4 fits. *(Codex/shared.)*
3. **Multi-setting design + manifest** — **CLOSED, JOINTLY APPROVED S32 at 808 reservations** (472 non-test now materialized). *(shared)*
4. **Matched learned models** — **MINE. GATED by `BLOCK_GATE4_LADDER_PENDING_STRUCTURAL_SEPARABILITY_CHECK`.** `TemporalAttributionNet` + `RMALatentEncoder` behind shared `[W,D]`; within-suite capacity ladder; ≥5 seeds; identical protocol IDs across C0/C1/S. Toolchain verified (torch cu128 / sm_120). **Data layout now EXISTS — the old "waits on Gate 2" blocker is gone.**
5. **Calibration/abstention/OOD/uncertainty** — **MINE.** Per-suite calibrated probs (Brier/NLL/ECE), abstention + OOD thresholds on validation, `severity_uncertainty` as a **bias-inclusive predictive error scale** (NOT in-sample residual dispersion — S24: understates true by 5.72× for S). Validation data now exists but must NOT be touched until Gate 4 opens.
6. **Confirmatory controller protocol** — **DECIDED S27 (both agents):** freeze the fair four-arm comparison (no-action/detection-only · transparent attribution-driven · RMA · oracle) and **RUN the pre-registered paired C1-vs-S comparison**; do NOT narrow to information-only, do NOT retune blocked families post-hoc. *(Codex owns controller; diagnosis→control seam shared.)*
7. **Evaluation driver + confirmatory manifest** — **MINE.** One CLI owning the `[t_c,t_c+5s]` slice, role joins, paired C1/S table, exclusions, CIs; rejects `dev-`/wrong-hash/cross-role/incomplete-pair/truncated. **Must implement FOUR pre-registered statements:** (a) `ood_flag` exclusion from known-class metrics; (b) the **degradation-ladder rule** (S30/S31): same paired contrast at pilot, val and test; a test null is hypothesis failure **only if** the contrast is present at earlier rungs; decay with rung = **generalization-limited**, not evidence against structural sensing; (c) **pilot→val moves one variable (confound severity) while val→test additionally moves half-fraction → complete factorial**; (d) **[NEW S33]** the two findings above — the structural severity grid sits below the 2× synchronous margin, and realized contact is fault-caused and near-absent in dev/val.

**Order:** (1)✓ → (2 foundation)✓ → (2 role-write)✓ → (3 assignment)✓✓ → (2 real generator + base roles)✓✓ → **(structural separability check on dev) [ME] ← WE ARE HERE** → (4/5 models+calibration) [me] → (2 remaining roles from real fits) [Codex] → (6 controller + sample-size) [shared] → **joint immutable freeze** → one-shot confirmatory generation + eval (7) → Phase 3.

Not freeze blockers (still required before completion): Slot-8 verification artifact; Technical Report / Accessible Piece / Study Guide Pass 2 (Phase 3); fresh-environment packet validation.

## The delivered dataset — layout and how to read it

`data/gate3-base-dev-pilot-val-c1-s/` (git-ignored):
```text
manifest.csv        945 lines (header + 944 rows)
plant/              945 files (index.csv + 944 npz)   2.8 GB  <- half is duplicate
labels/             945 files                          4.4 MB
observations/C1/    473 files (index.csv + 472 npz)
observations/S/     473 files                          835 MB total
generation_audit.json · independent_audit.json
```
- **Plant fields (20):** step, t_s, q_true, qd_true, qdd_true, tau_cmd, tau_delivered_true, deform_coords[90], curvature_true[4], gauge_true[4], imu_true[6], temperature_true[4], contact_state[2], task_reference, true_task_output, tracking_error, tracking_error_norm, control_effort, saturation_flag, safety_flag[7]. **`contact_state[:,0]` = summed force N, `[:,1]` = active flag.**
- **Observation fields:** `channel_names[6]`, `suite_available_mask[6]`, then per channel `values__X`, `valid__X`, `meas_time__X`, `avail_time__X`, `latency__X`. **C1's `gauge_obs` is all-NaN with mask False. S `gauge_obs` CONTAINS NaNs (dropout/latency) — use nan-aware statistics.**
- **Label fields:** source_class, subtype, location, severity, onset_index, onset_time_s, compound_flag, ood_flag.
- Run length 2900 steps (dev diagnostic; varies by trajectory duration / 0.002).
- **Two runs in the same context cell differ in sensor_seed, and the closed loop amplifies that into ~0.8 µε RMS of run-to-run gauge variation — which EXCEEDS the structural fault signature.** Any fault-effect measurement MUST use matched seeds, or it measures noise. (This is how I first got a flat-across-severity false reading.)

## Codex's Gate-1/2/3 layer — reference

`Reproducibility Packet/`:
- **`schema/schema.json`** (S28) — machine schema v1.0 + A1. Roles: identity_manifest, plant (20 fields = `PrivilegedRecord`), observations (deployable, fixed 6-channel registry + static suite mask), labels (8), estimator_outputs (9, `N_decisions` sparse axis), controller_logs (6). Channel registry: q_obs/qd_obs/tau_cmd (C0/C1/S), current_proxy_obs/imu_obs (C1/S), gauge_obs[4] (**S only**). `schema_sha256 = 0dae0dd0…3e942f` (LF-pinned via root `.gitattributes`).
- **`config/draft-config-v0.1.json`** — the DRAFT. **NEW HASH after S32 embedding: `config_hash = dev-712abf27c3f8f3c331ae9b76e3f22c48857334cc15a81e819718165e47753e56`** (parent was `dev-0211f2e7…6180`). File SHA-256 `8d89f0b7…6fc2`. Contains the **one-way approval wrapper** under `values.scenario_manifest`: approval_status/approval_decision/approved_assignment_hash/parent_draft_config_hash/parent_open_gates/research_splits_authorized/test_materialization_allowed/assignment. Gate 3 removed from `open_gates`. Frozen candidates: plant (`n_def=90`, gauges [0.25,0.75], A1 thresholds, `point_count_per_link=17`, `endpoint_contact_plane_z_m=0.2`), timing (`f_ctrl=500`, `control_dt_s=0.002`, `window_steps=768`, `stride=16`, **probe 0.05 N / 0.8 Hz / 1 cyc raised_cosine**, `analysis_window_s=5.0`), sensor_model (**gauge noise 1.0 µε, thermal 10 µε/°C, ref temp 25 °C, bias 0.5 µε, drift 0.2 µε/√s, hysteresis 0.15, quant 0.5 µε, latency 0.002 s**).
- **`config/proposed-gate3-assignment-v0.1.json`** — byte-unchanged, SHA-256 `76255a80…514ae`, `assignment_hash = dev-eec59ec8…bc33f1`. **Superseded, never approve or embed:** `dev-70832daa…765de` (656) and `dev-5939ff5f…0cedb` (blocked S30).
- **`scripts/utils/assignment_binding.py`** (S32) — the one-way wrapper. `embed_approved_assignment_document` / `validate_approved_assignment_binding(config, *, expected_assignment=None)`. Reconstructs the parent by nulling `scenario_manifest` + restoring `parent_open_gates`, proves its canonical hash, then validates the assignment against that parent.
- **`scripts/utils/assignment_generator.py`** (S32, 718 lines) — `build_identity_manifest`, `audit_manifest_against_assignment`, `preflight_assigned_mechanics` (compiles all 8 declared payload masses BEFORE the first rollout — Codex discarded a 193/472 partial run to establish that chronology), `materialize_base_dataset`, `audit_materialized_base_dataset`, `shared_channels_equal`. `ESTIMATOR_ID="gate4_unfit_shared_capacity_v1"`, `CONTROLLER_ID="bounded_observed_pd_no_recovery_v1"`, `DATASET_IDENTITY_TRAIN_SEED=0`.
- **`scripts/{embed_approved_assignment,generate_assignment_dataset,audit_assignment_dataset,validate_gate3_assignment,build_data_contract_fixture}.py`**; **`scripts/utils/{config_contract,storage_contract,role_contract,gate3_assignment}.py`**; tests `test_{data_contract,role_contract,gate3_assignment,assignment_binding,assignment_generator,cable_plant}.py`.
- `ValidatedConfig` fields are **`source_path, schema_path, document, config_hash, status`** (`is_frozen` is a property, NOT a constructor arg).
- Validator CLI flags are `--assignment` / `--schema` / `--config` (NOT `--draft-config`).
- **Assignment structure:** 19 known settings per split (1 healthy + 2 structure loc1 + 4 actuator loc{0,1} + 12 sensor {bias,drift,dropout}×loc{0,1}×2 severities), +2 compound/OOD in each of val/test (label = first component, `compound_flag`/`ood_flag` true, excluded from four-way metrics); **2 trajectories per split** (one ordinary, one diagnostic), split-exclusive; **realizations 4/4/4/8**; seed bases 110000/210000/310000/410000, seeds `base + 10*ordinal + {0,1,2,3}` (ordinal resets per split); reservations **152/152/168/336 = 808**. Expansion is trajectory → fault setting → replicate; context cell = `context_cell_table[(trajectory_index * realizations + replicate) % 8]`; **`fault_index` is not an input to context selection**.
- **Structural severities by split: dev {0.75, 0.50}, pilot {0.85, 0.60}, val {0.90, 0.40} + OOD 0.55; test {0.65, 0.35} + OOD 0.45.** Payloads: dev {0.000, 0.050}, pilot {0.025, 0.075}, val {0.100, 0.125}, test {0.150, 0.200} kg.

## My lanes — current state

`Reproducibility Packet/scripts/utils/estimator.py`:
- **`WindowFeatureExtractor(window_steps=W=768, probe_frequency_hz=0.8)`**: `[W,D]` left-padded + per-column `[last,mean,std,slope,sync_cos,sync_sin,sync_amplitude,valid_fraction]` over 18-col registry → 144 features. `N_FEATURE_STATS=4`, `N_EXTRA_FEATURES=4`, sync cols 4/5/6, `VALID_FRACTION_COL=7`, `DIAGNOSTIC_PROBE_HZ=0.8`, `MIN_SYNC_SAMPLES=8`.
- **`WindowNoveltyDetector`** (detect+abstain) · **`CoefficientReferenceDetector`** (canonical `synchronous_coefficient_vector` + `coefficient_reference_distance`; `fit_reference` atomic; `calibrate_threshold` fail-loud below `ceil(min_tail/far)`) · `_SCORE_STD_FLOOR=1e-3` shared · **`SeverityRidgeHead`** (`train_residual_std` is IN-SAMPLE — never feed a confidence gate) · `leave_one_group_out_residuals` (CALIBRATION-role diagnostic) · `OracleInterface(onset_time_s)` · `EstimatorCommandPolicy` (runs estimator every `stride`, ZOHs OUTPUT) · `RECOMMENDED_WINDOW=(768,16)` · **learned rungs specified-not-built (Gate 4).**
- **`utils/metrics.py` + `utils/stats.py`** (approved through S11): `tracking_reduction_pct(j_baseline,j_treatment)=100·(j_baseline−j_treatment)/j_baseline`, `j_5s` fail-loud on full `[t_c,t_c+5s]`, `safety_incident_rate`, `safety_regression_delta` (matched `[T,7]` guard), `hierarchical_bootstrap_ci` (crossed pair×seed). **Eval driver (Gate 7) — build once the frozen layout exists.**
- **Screens (all closed):** `screen_severity_estimation_quality.py`, `screen_severity_action_boundary.py`, `screen_actuator_probability_channel.py`, `tests/test_recovery_seam.py`.

## Codex's OTHER lanes — current state

- `utils/cable_mechanics.py` — **NEW S32:** `distal_payload_mass_kg` (point mass at the distal site, COM + parallel-axis inertia recompute, `mj_setConst`), optional absolute `endpoint_contact_window_s`. `structural_ei_remaining` default **0.50**; `endpoint_contact_plane_z_m` default 0.498 (assignment uses 0.2).
- `utils/cable_plant.py` — **NEW S32:** scheduled contact (plane moved −10 m outside the window; A1 pair stays exactly endpoint↔plane, `model.npair == 1`), compound physical faults (`additional_faults`, at most one structure + one actuator; sensor rejected). **`cable_plant.py:124-125` restricts structural faults to location `{-1,1}`** (verified S30 — a genuine plant constraint; do not re-litigate).
- `utils/task_control.py` (S17/S18): `BoundedTaskProfile`, `ObservedJointPDController` (kp (0.05,0.03), kd (0.005,0.003), torque limits (0.20,0.10); reads ONLY `q_obs`/`qd_obs`).
- `utils/recovery_control.py` — `GainScheduledRecoveryController`; `screen_actuator_recovery_action.py` (S25, I approved S26) → `BLOCK_ACTUATOR_ACTION_FAMILY_AT_SOURCE_SPECIFIC_GATE`; `screen_structural_recovery_action.py` (S20) → `BLOCK_STRUCTURAL_RECOVERY_ACTION_FAMILY`; `screen_fault_tracking_deficit.py` (S22); `run_bounded_noisy_information_review.py` (S19): S macro-F1 0.995 / C1 0.704.
- `agents/Codex/Config Freeze Readiness Review.md` = the seven-gate plan (I approved S27).

## The evidence tables (development-evidence boundary)

**Structural (Codex S20):** remaining EI 0.50/0.25/0.10/0.05 → mean peak |gauge| 38.4/72.4/152.8/259.7 µε (healthy 19.2) but mean **joint** tracking deficit +0.08%/−0.89%/−2.23%/−5.00% — monotone in information, monotone the WRONG way in joint control (damage moves to the TIP, which the joint score never measures). **NOTE: those severities are 0.50 and BELOW; the assignment reserves 0.40–0.90, i.e. mostly milder — this is the same gap Finding 1 measures.**

**Control-layer shape (Codex `bounded_noisy_information_review`):** healthy/actuator/sensor → S has no exclusive info + 0% tracking change; **structure → S exclusive info YES, C1 withholds actionable, `s_tracking_change_pct` −18.58%.** C1 per-class recall: structure **0.083**, else 1.000. **Where S has exclusive info there's no control headroom; where there's headroom S has no exclusive info** = the pre-registered Slot-13 diagnostic-only landing.

## The agreed contract's load-bearing specifics

- **Sensor suites (controlled variable):** C0 = joint encoders + commanded actuation · **C1 = C0 + noisy motor-current nominal-Kt torque estimate + one distal 6-axis IMU** · **S = C1 + four fixed strain/curvature gauge stations** · O = privileged oracle. **Temperature is observable ONLY through `gauge_obs`, i.e. only in S** (`sensor_model.py:423-424`, 10 µε/°C).
- **Two settled correctness points:** actuator-gain fault acts *downstream* of the current proxy; encoder fault has a *relational* signature.
- **Success bar (pre-declared, BOTH layers):** S improves held-out four-way macro-F1 over C1 by **≥0.05 absolute** (paired 95% excludes zero; every source-class recall diff lower-95% above **−0.02**) AND reduces the **5-s post-change integral of absolute tracking error by ≥10%** (`100·(J_C1−J_S)/J_C1`, paired 95% excludes zero, no safety regression) under realistic confounds. Known-class abstention = error in headline macro-F1.
- **Failure shapes:** hypothesis failure (C1+temporal adaptation matches S — clean negative) vs **method failure**. **Inconclusive (Slot 13):** diagnostic-only (**the shape the evidence keeps landing on**) · fault-specific/bounded · confound-fragile · excitation-dependent. **Finding 1 is precisely a method-failure risk — that is why it gates.**
- **Pre-specification:** freeze gauge placement, model/hyperparams, thresholds, analysis window, seeds/scenarios before confirmatory generation. Leakage-free splits. ≥5 training seeds. Paired hierarchical bootstrap.

## Carried limitations for the Technical Report / Gate 7

1. **2^(3−1) parity residual:** `I(trajectory ; full cell)` = 1 bit in dev/pilot/val, 0 at test; main effects and two-factor interactions estimable everywhere; cannot favour either suite. **Ladder:** pilot→val moves one variable; val→test additionally moves half-fraction → full factorial.
2. **The OOD arm rests on only 2 compound settings per split** (16 val runs / 32 test runs, 2 fault types) — thin for any OOD claim.
3. **Test severities sit partly outside the fit hull** (structure/actuator 0.35 more severe than dev's `{0.5,0.75}`; `encoder_bias 0.015` rad milder than anything trained) — harmless for classification, but the **severity regression head extrapolates** at test.
4. **`split_group_id` is unique per reservation**, so `_assert_one_mapping(split_group_id → split)` in `audit_identity_manifest` is vacuous — the real guarantee is trajectory/fault exclusivity, which does hold.
5. **`_assert_fault_independent_context_cells`** computes `expected_cell_count = min(len(table), trajectory_count * repetitions)`, correct only because trajectory blocks are disjoint mod 8 at the actual values. Both pinned; cannot silently drift.
6. **[NEW S33] Finding 1** — structural severity grid below the 2× synchronous margin at every reserved severity, worsening with payload.
7. **[NEW S33] Finding 2** — realized contact is fault-caused (100% encoder bias/drift) and absent in dev/val; the contact axis is effectively inert in the splits that feed fitting and calibration.

## Coherence / honesty bounds (keep loud)

- `utils/synchronous.py` (Codex S9) = the single shared harmonic statistic; `synchronous_coefficient_vector` + `coefficient_reference_distance` in `estimator.py` = the one canonical definition every pilot/screen/review imports.
- **Sensor RNG keyed on `(sensor_seed, pair_id, channel, stream)`** — `pair_id` load-bearing; screens reuse an upstream screen's `pair_id` verbatim and check CRN at 0.000e+00.
- Deployable floors are *detection*, not learned attribution; all S19 rates from ONE fixed fault setting per class, held out over sensor noise only; abstention untestable on this fault library (min margin 0.90); one-hot prototype probabilities NOT calibrated; **every joint-space control number comes from a condition where the structural fault causes no measurable JOINT deficit.**

## Constraints / environment / ops (load-bearing)

- **Simulation-only, one desktop:** Windows 11, Ryzen 7 8700F (8C/16T), RTX 5060 Ti **16 GB VRAM** (Blackwell/sm_120), 32 GB RAM, Python **3.12.10** in `./venv`. Free/OSS, commercial-use-friendly only.
- **venv has:** numpy 2.5.1, scipy 1.18.0, scikit-learn 1.9.0, matplotlib 3.11.0, mujoco 3.10.0, pandas 3.0.3, control 0.10.2, gymnasium 1.3.0, pytest 9.1.1, **torch 2.11.0+cu128** (CUDA 12.8, sm_120-verified).
- **Running packet tests:** from `Reproducibility Packet/`, `..\venv\Scripts\python.exe -m pytest tests/`. **From the REPO ROOT the venv is `venv/Scripts/python.exe` (NOT `../venv`).** Set `PYTHONIOENCODING=utf-8` for unicode; use ASCII in probe scripts.
- **To import packet utils from a scratchpad probe:** `sys.path.insert(0, "<repo>/Reproducibility Packet/scripts")` then `from utils.X import Y`.
- **Timings (measured):** full packet suite ~9–10 s; one MuJoCo rollout (2900 steps, 0.1 ms sim step) ~35–45 s; my S33 A/B probes (9–12 rollouts) ~7–10 min each. Reading `contact_state`/`temperature_true` from all 472 plant npz ~2 min. Run long jobs in background; **a pipe through `tail`/`*>` buffers until exit — poll for the results file.**
- **STANDING LESSON 1 — dry-run the analysis path before spending a rollout budget.**
- **STANDING LESSON 2 — self-audit from row artifacts / raw bytes, not the summary.**
- **STANDING LESSON 3 — restate a proxy in the contract's units before comparing to the bar.**
- **STANDING LESSON 4 — for a MuJoCo screen, re-run to scratch + diff against committed.**
- **STANDING LESSON 5 — verify the live git state before trusting continuity** (S28–S33: the startup snapshot lagged EVERY time, six running).
- **STANDING LESSON 6 — review a design by simulating its consequences, not by verifying its internal consistency.** Corollaries: dead arithmetic hides in small catalogs; **the dangerous confound is the one that favours you**.
- **STANDING LESSON 7 — for any pre-registration, check that the pre-registered TEXT generates the pre-registered DATA.** Corollaries: apply ONE consistent blocking standard, direction-of-bias; check a flaw is AVOIDABLE before reporting it.
- **STANDING LESSON 8 (S32) — test a guard by feeding it the exact state it was written to catch.** Corollaries: check a flaw is REAL before reporting it; report the scope you actually achieved.
- **STANDING LESSON 9 (NEW, S33) — a design review that reads the design cannot find what the design does.** I reviewed this assignment twice, measured its label distributions to ten decimals, and every measurement was correct — yet none could see that the contact axis fires on 4.7% of the runs declaring it, or that the structural signal sits below our own bar. **A pre-registration is a claim about data and stays unverified until data exist to check it against.** Corollary: **audit the yardstick before the artifact** — I used a superseded floor and got a dramatic wrong answer, then a confounded pairing and got a flat wrong answer; validating my instrument against a number the team had already published is what separated the real finding from two false ones. Second corollary: **before calling a settled parameter a defect, search the history for why it was chosen** — the 0.05 N probe took ~10 minutes of grepping to reveal a careful safety-driven decision I was about to re-litigate.
- **PowerShell 5.1** primary (no ternary/`??`); Bash tool also available (its `cd` persists — check where you are). Use `git diff --numstat` to confirm `+N/−0` after every chat turn.
- **Root `.gitignore`** covers `venv/`, `/data/` (**correctly ignores the 3.7 GB dataset — verified S33**), `tmp/`, `MUJOCO_LOG.TXT`, caches, model files, LaTeX aux, OS/IDE noise. **Root `.gitattributes`** pins `Reproducibility Packet/schema/schema.json` to LF. **Packet `.gitignore`** ignores `*.npz` + caches/logs.
- **Software-engineering standard:** `argparse`, no hard-coded paths, one purpose, shared logic in `utils/`, docstrings, prints progress, fails loud. Licensing: code MIT, prose CC BY 4.0.

## Pointers

- Claim Sheet (in-force contract): `Claim Sheet.md` · plain-language: `Accessible Claim Sheet.md` · Study Guide Pass 1: `Study Guide/Pass 1 - Conceptual Foundation.tex`
- **Shared schema (in force, +A1):** prose `Reproducibility Packet/schema/schema-v1.0.md`; machine `schema.json`.
- **The freeze plan:** `agents/Codex/Config Freeze Readiness Review.md`.
- **The probe-amplitude record (READ BEFORE QUESTIONING 0.05 N):** `Reproducibility Packet/results/synchronous_safe_probe/synchronous_safe_probe_report.md` + Phase-2 chat lines ~425–465.
- **My lanes:** sensor `utils/{schema_types,sensor_model,rng,synthetic_plant}.py`; eval `utils/{metrics,stats}.py`; estimator `utils/estimator.py`; synchronous floor `scripts/analyze_synchronous_detection_floor.py`; shared seam test `tests/test_recovery_seam.py`; the three severity/probability screens + tests + `results/`.
- **Phase-2 chat:** `chats/Claude-Codex/Phase 2 Integration and Config Freeze/…- Active.md` (**3517 lines**; my S33 `APPROVE_GATE2_GENERATOR_BASE_ROLES` = tail, +220/−0; **NO open loop; I own the next turn**).
- **Monitoring chat:** `chats/Claude-Codex-Human/Transcript Order Monitoring/…- Active.md` (S33 check clean — Codex's two S32 turns were `+178/−0`, headers 3123 and 3150, Codex last; **eleventh consecutive clean append**, no note added; flag only on recurrence).
- **CONCLUDED director chat:** `chats/Claude-Codex-Human/Better Suited Task/…- Concluded.md` + `Summary.md` — the withdrawn task-redesign directive. **Read its `Summary.md` if Finding 1 leads toward changing the task or the score** — it is closely related and the director deferred that idea to a future project.
- Director requests: `director_requests.md` (root) — entry 1 (Claim Sheet review) non-blocking, awaiting director reply.
- My foundation `agents/Claude/Literature Foundation.md` · ledger `agents/Claude/references.md` (**no S20–S33 entries — reproduction/construction/measurement/review sessions, no external sources read**) · progress reports `agents/Claude/Progress Reports/` (Phase 0/1 Close, S8, S16, S24, S32). **NEXT DUE: my Session 40.**
- Live-Run README (co-maintained): root `README.md` — **Phase 2 / In Progress**, banner **2026-07-24**. **S33 added one running-log entry** (first real dataset approved; both findings stated plainly).
- **Scratchpad (S33, NOT committed — recreate what you need):** `append_turn.py` (binary EOF-append + 4 gates + rollback; pass an ASCII marker — worked first try, +220/−0), `probe_s33_identity.py` (independent prose re-derivation vs manifest + realized-leakage MI), `probe_s33_physics.py` (temperature/contact/payload/fault realization over all 472 runs), `probe_s33_signal_budget.py` (suite masking + paired signatures — **note: needs nan-aware stats, S gauge_obs has NaNs**), `probe_s33_ab_probe_force.py` (matched-seed A/B over probe force), `probe_s33_synchronous_margin.py` (**the one that produced Finding 1**), `probe_s33_instrument_check.py` (**the instrument validation + payload stress — reuse this pattern before trusting any new measurement**), `probe_s33_binding_teeth.py` (adversarial wrapper teeth), `turn_s33.md`.
