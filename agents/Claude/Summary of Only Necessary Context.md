# Summary of Only Necessary Context — Claude

*Rewritten every session. Restores my working context for the next session. Excludes anything already in `Project Details/Project Details.md` and `AgentPrompt.md` (I re-read those in full at session start). Last rewritten: end of Session 34, 2026-07-24 19:50 PDT.*

## Where the project is

- **Phase 2 (Execution) is OPEN.** All Phase-1 gates in force. **Schema v1.0 + Amendment A1 in force.** Contract changes run through the **amendment protocol**.
- I am **Claude**; last session was **Session 34**; next session I run is **Session 35**.
- **`config.json` is deliberately NOT frozen** and does not exist. All hashes are `dev-`; no `dev-` trace may enter confirmatory analysis.
- Real data exists: `data/gate3-base-dev-pilot-val-c1-s` (3.86 GB, git-ignored, local only). 472 reservations / 944 manifest rows / C1+S / dev 152, pilot 152, val 168. **Test untouched: 0 identities, 0 payloads.** Approved (my S33 base roles + my S34 hardening).
- **THERE IS AN OPEN REVIEW LOOP AND CODEX OWNS THE NEXT TURN: `AMENDMENT_A2` (my S34 proposal).** Do not start Gate-4 work until it settles.
- **NO PROGRESS REPORT IS DUE at S35.** Last regular was S32 (covers S25–S32). **Next regular: my Session 40.** **BUT: if A2 is approved, the approving turn fires a progress report — if I write that turn, I write the report that session.**

## THE HEADLINE RESULT OF SESSION 34 — read this before anything else

**`BLOCK_GATE4_LADDER_PENDING_STRUCTURAL_SEPARABILITY_CHECK` is ANSWERED, and the answer is outcome 2: neither suite separates structure at either dev severity.**

New packet script `Reproducibility Packet/scripts/screen_structural_separability.py`; results in `Reproducibility Packet/results/structural_separability/{pooled_trajectories,diagnostic_trajectory_only}/`. **It refuses any split but `dev` in code.** Dev only was read; pilot/val/test never opened.

**Design property I discovered and should reuse:** every fault setting's 8 dev runs occupy the **same 8 context cells, run for run** (r00 = nominal/iso25c/none, r01 = nominal/warm2c/brief, r02 = 0.050kg/iso25c/brief, r03 = 0.050kg/warm2c/none, mirrored across both trajectories). So healthy `tXX_rYY` and structure `tXX_rYY` differ **only in the fault and the sensor seed**. That gives context-matched contrasts, leave-one-CELL-out folds, a paired per-cell statistic, and an exact 2^8 permutation null. **Use this pairing for any future fault-effect measurement on this dataset.**

**Held-out run-level AUROC, both dev trajectories pooled (8 v 8):**
```text
contrast                 suite  interpretable  learned(best over C)  perm p
structure rem EI 0.75     C1        0.453           0.250            0.914
structure rem EI 0.75     S         0.469           0.172            0.945
structure rem EI 0.50     C1        0.469           0.750              -
structure rem EI 0.50     S         0.578           0.703              -
actuator  rem gain 0.50   C1        0.594           0.891   <- POSITIVE CONTROL
actuator  rem gain 0.50   S         0.500           0.859   <- POSITIVE CONTROL
```
**Diagnostic trajectory only (4 v 4), where the 0.8 Hz probe exists:**
```text
structure 0.75   C1 0.375/0.000    S 0.500/0.000
structure 0.50   C1 0.375/0.375    S 0.625/0.500
actuator  0.50   C1 0.875/0.875    S 0.875/0.750
```

**Per-column paired attribution (S, all 18 registry columns) — the most important table:**
```text
structure 0.75   imu_obs[2]   NOT S-exclusive   -12.34%   0.223x spread   p=0.0078
structure 0.50   imu_obs[0]   NOT S-exclusive    -9.37%   0.597x spread   p=0.0078
structure 0.50   imu_obs[2]   NOT S-exclusive   -29.34%   0.502x spread   p=0.0078
actuator  0.50   tau_cmd[1]            +62.82%  6.027x   ·  current_proxy_obs[1] +55.12% 7.430x
best S-EXCLUSIVE gauge column, any arm:  0.099-0.134x spread, sign p >= 0.2891  (NONE significant)
```
**No gauge column reaches significance in any arm. The only consistent structural signature is `imu_obs[2]` — a C1 channel.** At the reserved severities the conventional suite sees structure and the structural suite does not.

**Matched-seed severity ladder below the reserved grid** (seed 110802, `trajectory_dev_diagnostic_b`, nominal payload, W=768 from onset; privileged = the quantity the 0.405 µε floor was defined on; observed = what S actually sees):
```text
rem EI   privileged µε   margin   clears 2.0x   observed µε   obs/priv
 0.75       0.0604        0.15x       no          0.0677        1.12
 0.50       0.1867        0.46x       no          0.1972        1.06
 0.40       0.2784        0.69x       no          0.2832        1.02
 0.30       0.4318        1.07x       no          0.4342        1.01
 0.25       0.5552        1.37x       no          0.5575        1.00
 0.20       0.7396        1.83x       no          0.7230        0.98
 0.15       1.0486        2.59x      YES          1.0523        1.00
 0.10       1.6653        4.11x      YES          1.6684        1.00
                    floor 0.405 µε; required 2.0x = 0.810 µε
```
**Three conclusions:** (1) the 2× margin is first met between remaining EI **0.20 and 0.15** — an 80–85% stiffness loss — while the reserved grid is 0.35–0.90, i.e. **2× to 40× too mild**; (2) **the sensor model is NOT the bottleneck** (observed ≈ privileged to within 0–12%; matched-seed noise cancels) — the mechanics are; (3) the same severity varies by context (S33 gave 0.1614 at 0.75 in a different cell vs 0.0604 here) — **never quote a severity's µε value without naming its cell**.

**Honest bounds on the screen:** n = 8/arm pooled, 4 diagnostic-only. The learned probe is linear on a mean-pooled tensor = a lower bound on the learned rung. The positive control establishes sensitivity to effects at 2–7× the healthy across-context spread, **not** to effects at 0.1–0.5× it. The per-column statistic is post-onset mean |value|, which for gauges includes payload bending + thermal and therefore *understates* them — which is why the interpretable rung is reported beside it and says the same thing.

## AMENDMENT PROPOSAL A2 — the open loop

Posted in the Phase-2 chat, S34. Codex must reply `APPROVE_AMENDMENT_A2_PROPOSAL` or block. Four parts:

1. **Keep the existing severity grid and the delivered 472 runs as the pre-registered *mild band*** and report their negative result as a finding: at remaining EI ≥ 0.50, under this task and excitation, distributed strain adds nothing over C1, and the structural signature that exists is in the distal IMU.
2. **Add a second, more severe structural band per split** (from the ladder above), preserving split-exclusivity and the disjoint dev/pilot/val/test ordering. The headline confirmatory comparison moves to this band.
3. **Re-derive the diagnostic probe amplitude** against the new mildest reserved severity by a bracketed grid on the 0.405 µε floor at 2.0×, **A1 angular-rate envelope (10 rad/s) as the hard ceiling**. 0.05 N was selected against rem EI 0.50 under 50% task torque; 1.0 N was rejected as unsafe (37.7 rad/s); the interval between has never been searched against the *reserved* severities.
4. **Decide the confirmatory test contact profile deliberately** (S33 Finding 2) instead of inheriting `contact_test_sustained`.

**New Slot 11–13 shapes proposed:** success keeps its form but is stated **per band**, severe band carries the headline; **new failure shape** = S failing to beat C1 where the margin *is* met is a clean hypothesis failure; **new Slot-13 non-transfer shape** = **severity-bounded** ("structural sensing helps only above a measured severity threshold").

**Why it is not designing around the answer:** the failing gate is one we declared before execution (the safe-probe screen's 2.0× margin); the mild band stays in the design with its negative result reported; and if nothing inside A1 clears the margin at any admissible severity, the honest conclusion is that this plant cannot test the hypothesis. **It is explicitly NOT the task/score redesign the director withdrew** in `chats/Claude-Codex-Human/Better Suited Task/` — the joint-space task, controller and tracking score are untouched.

**The implementation constraint I raised for Codex to decide (real, verified):** `expanded_fault_settings` (in `utils/gate3_assignment.py`, ~line 190) expands **healthy → structure → actuator → sensor** per split. Extending `grid["structure"]["severities"]` inserts settings **ahead** of every actuator and sensor setting, shifting their ordinals and therefore their seeds (`base + 10*ordinal + {0..3}`) — **which invalidates the delivered 472 runs.** Options: full regeneration under one coherent rule (my recommendation), or change the expansion order. Codex owns the generator.

## What I verified in S34 (do not re-do)

- All six of Codex's published digests reproduce. **Full packet suite 399 passed** (re-run twice).
- **The "no regeneration needed" claim holds on all three legs:** config `control_dt_s`=0.002 == `CableModelConfig` default; `simulation_timestep_s`=0.0001 == `CablePlant` default; `point_count_per_link`=17 == `CablePlant` default. Reciprocal exact, physics ratio exactly 20.
- **Independent on-disk audit under the NEW code passes:** `complete_primary_c1_s_base_dataset_audit_pass`, 472/944, byte-identical plant pairs 472/472, bitwise shared channels 472/472, **0 test rows**.
- **`_step_index` has no latent trigger at test:** all 8 trajectories grid-aligned, worst error 4.55e-13 vs 1e-9 tolerance, **including both test trajectories**.
- **23 adversarial guard cases all behaved.** Notably: a self-rehashed assignment swap is refused *both* by the required pin (tracked file) *and*, when the attacker pins its own bytes, by `validate_assignment` against the reconstructed parent — **the binding has two independent layers.**
- Two non-blocking notes given to Codex: `expected_assignment=None` refuses with an uninformative `TypeError: 'NoneType' object is not iterable` (a one-line `isinstance` would name it); `scripts/run_feasibility_spike.py:648` still hard-codes `point_count=17` (Phase-0 spike, outside the generation path).
- **Cross-review catch:** Codex's `HumanReport33.md` renders my S33 severity table's first row as `0.95 / 0.0090 / 0.02x / development`; the row I measured was `0.90 / 0.0544 / 0.13x / validation`. Flagged forward in chat; concluded record not reopened. **Do not let the wrong value reach the Technical Report.**

## Carried from S33 — still live

**Finding 2 (contact), non-blocking, record and watch.** 236 runs assigned a contact profile; **11 actually touched** (4.7%) — dev 0/76, pilot 11/76, val 0/84. All 11 are encoder **bias (7) or drift (4)**; 0 dropout/actuator/structure/healthy. Mechanism: bias/drift corrupt measured angle → observed-PD overdrives → tip descends. **Realized contact is an EFFECT OF THE FAULT**, peak 2.6–3.0 N, loudest in the S-exclusive gauge channel — direction of bias **favours S**. `I(fault; assigned contact label)` = 0 exactly; `I(fault; contact actually occurring)` is not. Exposure is **test**: `contact_test_sustained` window 2.2 s vs pilot 0.6 s at 0.150/0.200 kg. Folded into A2 part (4).

## GATE STATUS — the freeze path (central reference)

**Governing decision: `BLOCK_CONFIG_FREEZE_PENDING_PRECONFIRMATORY_BUILD_AND_VALIDATION`.** A **versioned DRAFT config** governs dev/val generation; the **final immutable `config.json` freeze comes AFTER model implementation + validation-only hyperparameter/threshold selection and BEFORE any untouched `test` payload.**

1. **Machine schema + config authority** — **DONE, APPROVED S28.** *(Codex/shared.)*
2. **Role-separated storage, deployable loader, leakage/split audits** — foundation DONE (S28), role-write DONE (S29), **real generator + base roles APPROVED (my S33)**, **generator hardening APPROVED (my S34)**. **STILL OPEN OVERALL:** `estimator_outputs` + `controller_logs` roles await the Gate-4 fits. *(Codex/shared.)*
3. **Multi-setting design + manifest** — **CLOSED, JOINTLY APPROVED S32 at 808 reservations** (472 non-test materialized). **A2 would reopen this.** *(shared)*
4. **Matched learned models** — **MINE. NOW GATED BY `AMENDMENT_A2`** (the separability check is answered). `TemporalAttributionNet` + `RMALatentEncoder` behind shared `[W,D]`; within-suite capacity ladder; ≥5 seeds; identical protocol IDs across C0/C1/S. Toolchain verified (torch cu128 / sm_120).
5. **Calibration/abstention/OOD/uncertainty** — **MINE.** Per-suite calibrated probs (Brier/NLL/ECE), abstention + OOD thresholds on validation, `severity_uncertainty` as a **bias-inclusive predictive error scale** (NOT in-sample residual dispersion — S24: understates true by 5.72× for S). **Validation must NOT be touched until Gate 4 opens.**
6. **Confirmatory controller protocol** — **DECIDED S27 (both agents):** freeze the fair four-arm comparison (no-action/detection-only · transparent attribution-driven · RMA · oracle) and **RUN the pre-registered paired C1-vs-S comparison**; do NOT narrow to information-only, do NOT retune blocked families post-hoc. *(Codex owns controller; diagnosis→control seam shared.)*
7. **Evaluation driver + confirmatory manifest** — **MINE.** One CLI owning the `[t_c,t_c+5s]` slice, role joins, paired C1/S table, exclusions, CIs; rejects `dev-`/wrong-hash/cross-role/incomplete-pair/truncated. **Must implement pre-registered statements:** (a) `ood_flag` exclusion from known-class metrics; (b) the **degradation-ladder rule** (S30/S31): same paired contrast at pilot, val and test; a test null is hypothesis failure **only if** the contrast is present at earlier rungs; decay with rung = **generalization-limited**; (c) **pilot→val moves one variable (confound severity) while val→test additionally moves half-fraction → complete factorial**; (d) S33's two findings; (e) **[NEW S34]** the mild-band negative result and the per-channel attribution — that at reserved severities the structural signature is C1-visible and gauge-invisible.

**Order:** (1)✓ → (2 foundation)✓ → (2 role-write)✓ → (3 assignment)✓✓ → (2 generator + base roles)✓✓ → (2 hardening)✓✓ → (dev separability check)✓ **[ANSWERED — NEGATIVE]** → **AMENDMENT A2 [CODEX OWNS THE TURN] ← WE ARE HERE** → (4/5 models+calibration) [me] → (2 remaining roles) [Codex] → (6 controller + sample-size) [shared] → **joint immutable freeze** → one-shot confirmatory generation + eval (7) → Phase 3.

Not freeze blockers (still required before completion): Slot-8 verification artifact; Technical Report / Accessible Piece / Study Guide Pass 2 (Phase 3); fresh-environment packet validation.

## The delivered dataset — layout and how to read it

`data/gate3-base-dev-pilot-val-c1-s/` (git-ignored):
```text
manifest.csv        945 lines (header + 944 rows)
plant/              945 files (index.csv + 944 npz)   2.8 GB  <- half is duplicate (documented)
labels/             945 files                          4.4 MB
observations/C1/    473 files (index.csv + 472 npz)
observations/S/     473 files                          835 MB total
generation_audit.json · independent_audit.json
```
- **Load one observation:** `ObservedRecord.load_npz(root/"observations"/suite/f"{run_id}.npz")`. Slice a window by slicing `values/valid_mask/measurement_time_s/availability_time_s/latency_age_s` per channel in `CHANNEL_NAMES` (see `slice_record` in my S34 screen).
- **Plant fields (20):** step, t_s, q_true, qd_true, qdd_true, tau_cmd, tau_delivered_true, deform_coords[90], curvature_true[4], gauge_true[4], imu_true[6], temperature_true[4], contact_state[2], task_reference, true_task_output, tracking_error, tracking_error_norm, control_effort, saturation_flag, safety_flag[7]. **`contact_state[:,0]` = summed force N, `[:,1]` = active flag.**
- **Registry D = 18:** q_obs[2], qd_obs[2], tau_cmd[2], current_proxy_obs[2], imu_obs[6], gauge_obs[4]. **C1's `gauge_obs` is all-NaN, mask False. S `gauge_obs` CONTAINS NaNs (dropout/latency) — use nan-aware statistics.**
- **Label fields:** source_class, subtype, location, severity, onset_index, onset_time_s, compound_flag, ood_flag.
- **Run lengths:** `trajectory_dev_ordinary_a` 2900 steps (onset 400); `trajectory_dev_diagnostic_b` 3000 steps (onset 500). Both dev trajectories carry 76 rows per suite.
- **Two runs in the same context cell differ in sensor_seed, and the closed loop amplifies that into ~0.8 µε RMS of run-to-run gauge variation — which EXCEEDS the structural fault signature.** Any fault-effect *magnitude* measurement MUST use matched seeds. Separability measurement must NOT (that is the point — it must beat the noise).

## Codex's Gate-1/2/3 layer — reference

`Reproducibility Packet/`:
- **`schema/schema.json`** (S28) — machine schema v1.0 + A1. Roles: identity_manifest, plant (20 fields = `PrivilegedRecord`), observations (deployable, fixed 6-channel registry + static suite mask), labels (8), estimator_outputs (9), controller_logs (6). `schema_sha256 = 0dae0dd0…3e942f` (LF-pinned via root `.gitattributes`).
- **`config/draft-config-v0.1.json`** — the DRAFT. **`config_hash = dev-712abf27c3f8f3c331ae9b76e3f22c48857334cc15a81e819718165e47753e56`** (parent `dev-0211f2e7…6180`). Contains the **one-way approval wrapper** under `values.scenario_manifest`. Frozen candidates: plant (`n_def=90`, gauges [0.25,0.75], A1 thresholds, `point_count_per_link=17`, `simulation_timestep_s=1e-4`, `endpoint_contact_plane_z_m=0.2`), timing (`f_ctrl=500`, `control_dt_s=0.002`, `window_steps=768`, `stride=16`, **probe 0.05 N / 0.8 Hz / 1 cyc raised_cosine**, `analysis_window_s=5.0`), sensor_model (**gauge noise 1.0 µε, thermal 10 µε/°C, ref 25 °C, bias 0.5 µε, drift 0.2 µε/√s, hysteresis 0.15, quant 0.5 µε, latency 0.002 s**).
- **`config/proposed-gate3-assignment-v0.1.json`** — SHA-256 `76255a80…514ae`, `assignment_hash = dev-eec59ec8…bc33f1`. **Superseded, never approve:** `dev-70832daa…765de` (656) and `dev-5939ff5f…0cedb` (blocked S30).
- **`scripts/utils/assignment_binding.py`** (S32, hardened S33) — `embed_approved_assignment_document` / `validate_approved_assignment_binding(config, *, expected_assignment)` — **`expected_assignment` is now REQUIRED.**
- **`scripts/utils/assignment_generator.py`** (S32, hardened S33) — `GenerationRuntimeParameters` + `_runtime_parameters(binding)` read `timing.control_dt_s`/`f_ctrl_hz` and `plant.simulation_timestep_s`/`point_count_per_link` from the bound config; `_step_index(time_s, dt)` fails loud off-grid. `build_identity_manifest`, `audit_manifest_against_assignment`, `preflight_assigned_mechanics`, `materialize_base_dataset`, `audit_materialized_base_dataset`, `shared_channels_equal`. `ESTIMATOR_ID="gate4_unfit_shared_capacity_v1"`, `CONTROLLER_ID="bounded_observed_pd_no_recovery_v1"`, `DATASET_IDENTITY_TRAIN_SEED=0`.
- **`utils/config_contract.py`: the loader is `load_config(config_path, schema_path, *, require_frozen=False)`** (NOT `load_validated_config`). `ValidatedConfig` fields: `source_path, schema_path, document, config_hash, status` (`is_frozen` is a property). Validator CLI flags are `--assignment` / `--schema` / `--config`.
- **Assignment structure:** 19 known settings per split (1 healthy + 2 structure loc1 + 4 actuator loc{0,1} + 12 sensor {bias,drift,dropout}×loc{0,1}×2 sev), +2 compound/OOD in val/test; **2 trajectories per split** (ordinary + diagnostic), split-exclusive; realizations 4/4/4/8; seed bases 110000/210000/310000/410000, seeds `base + 10*ordinal + {0,1,2,3}` (ordinal resets per split); reservations **152/152/168/336 = 808**. Expansion order **healthy → structure → actuator → sensor**; context cell = `context_cell_table[(trajectory_index * realizations + replicate) % 8]`; `fault_index` is NOT an input to context selection.
- **Structural severities by split: dev {0.75, 0.50}, pilot {0.85, 0.60}, val {0.90, 0.40} + OOD 0.55; test {0.65, 0.35} + OOD 0.45.** Payloads: dev {0.000, 0.050}, pilot {0.025, 0.075}, val {0.100, 0.125}, test {0.150, 0.200} kg. **All of these are 2×–40× milder than the measured 2× margin threshold (~0.17).**

## My lanes — current state

`Reproducibility Packet/scripts/utils/estimator.py`:
- **`WindowFeatureExtractor(window_steps=W=768, probe_frequency_hz=0.8)`**: `window_tensor(record)` → `(values[W,D], valid[W,D])` NaN→0 + mask; `window_features(record)` → per-column `[last,mean,std,slope,sync_cos,sync_sin,sync_amplitude,valid_fraction]` over the 18-col registry → 144 features. `N_FEATURE_STATS=4`, `N_EXTRA_FEATURES=4`, sync cols 4/5/6, `VALID_FRACTION_COL=7`, `DIAGNOSTIC_PROBE_HZ=0.8`, `MIN_SYNC_SAMPLES=8`.
- **`synchronous_coefficient_vector(record, extractor)`** → the suite's live channels' (cos,sin) pairs; **the last `2*4=8` entries are the gauge columns for S**. **`coefficient_reference_distance(v, mean, scale)`** is scaled/normalized — for raw µε use `np.linalg.norm(v_fault[-8:] - v_healthy[-8:])`.
- **`WindowNoveltyDetector`** · **`CoefficientReferenceDetector`** (`fit_reference` atomic; `calibrate_threshold` fail-loud below `ceil(min_tail/far)`; `_scale_from(mean,std)` is the reference-scale helper) · `_SCORE_STD_FLOOR=1e-3` shared · **`SeverityRidgeHead`** (`train_residual_std` is IN-SAMPLE — never feed a confidence gate) · `leave_one_group_out_residuals` (CALIBRATION-role diagnostic) · `OracleInterface` · `EstimatorCommandPolicy` · `RECOMMENDED_WINDOW=(768,16)` · **learned rungs specified-not-built (Gate 4).**
- **`utils/metrics.py` + `utils/stats.py`** (approved through S11): `tracking_reduction_pct`, `j_5s` fail-loud on full `[t_c,t_c+5s]`, `safety_incident_rate`, `safety_regression_delta`, `hierarchical_bootstrap_ci` (crossed pair×seed). **Eval driver (Gate 7) — build once the frozen layout exists.**
- **Screens (all closed):** `screen_severity_estimation_quality.py`, `screen_severity_action_boundary.py`, `screen_actuator_probability_channel.py`, `tests/test_recovery_seam.py`, **`screen_structural_separability.py` (NEW S34)**.

## Codex's OTHER lanes — current state

- `utils/cable_mechanics.py` — `distal_payload_mass_kg`, optional absolute `endpoint_contact_window_s`; `structural_ei_remaining` default **0.50**; `control_dt_s` default **0.002**; `endpoint_contact_plane_z_m` default 0.498 (assignment uses 0.2).
- `utils/cable_plant.py` — `CablePlant(config, *, point_count=17, simulation_timestep_s=1e-4, fault=None, additional_faults=())`; scheduled contact; compound physical faults. **`cable_plant.py:124-125` restricts structural faults to location `{-1,1}`** (verified S30 — a genuine plant constraint; do not re-litigate).
- `utils/task_control.py`: `BoundedTaskProfile`, `ObservedJointPDController` (kp (0.05,0.03), kd (0.005,0.003), torque limits (0.20,0.10); reads ONLY `q_obs`/`qd_obs`).
- `utils/recovery_control.py` — `GainScheduledRecoveryController`; `screen_actuator_recovery_action.py` (S25) → `BLOCK_ACTUATOR_ACTION_FAMILY_AT_SOURCE_SPECIFIC_GATE`; `screen_structural_recovery_action.py` (S20) → `BLOCK_STRUCTURAL_RECOVERY_ACTION_FAMILY`; `screen_fault_tracking_deficit.py` (S22); `run_bounded_noisy_information_review.py` (S19): S macro-F1 0.995 / C1 0.704.
- `agents/Codex/Config Freeze Readiness Review.md` = the seven-gate plan (I approved S27).

## The evidence tables (development-evidence boundary)

**Structural (Codex S20):** remaining EI 0.50/0.25/0.10/0.05 → mean peak |gauge| 38.4/72.4/152.8/259.7 µε (healthy 19.2) but mean **joint** tracking deficit +0.08%/−0.89%/−2.23%/−5.00% — monotone in information, monotone the WRONG way in joint control (damage moves to the TIP, which the joint score never measures). **My S34 ladder is consistent with this and pins the detection threshold at ~0.17 remaining EI.**

**Control-layer shape (Codex `bounded_noisy_information_review`):** healthy/actuator/sensor → S has no exclusive info + 0% tracking change; **structure → S exclusive info YES, C1 withholds actionable, `s_tracking_change_pct` −18.58%.** C1 per-class recall: structure **0.083**, else 1.000. **NOTE: that screen used ONE fixed fault setting per class at a severity far more severe than the reserved grid — my S34 result does not contradict it, it bounds where it applies.**

## The agreed contract's load-bearing specifics

- **Sensor suites (controlled variable):** C0 = joint encoders + commanded actuation · **C1 = C0 + noisy motor-current nominal-Kt torque estimate + one distal 6-axis IMU** · **S = C1 + four fixed strain/curvature gauge stations** · O = privileged oracle. **Temperature is observable ONLY through `gauge_obs`, i.e. only in S** (`sensor_model.py:423-424`, 10 µε/°C).
- **Two settled correctness points:** actuator-gain fault acts *downstream* of the current proxy; encoder fault has a *relational* signature.
- **Success bar (pre-declared, BOTH layers):** S improves held-out four-way macro-F1 over C1 by **≥0.05 absolute** (paired 95% excludes zero; every source-class recall diff lower-95% above **−0.02**) AND reduces the **5-s post-change integral of absolute tracking error by ≥10%** (`100·(J_C1−J_S)/J_C1`, paired 95% excludes zero, no safety regression) under realistic confounds. Known-class abstention = error in headline macro-F1.
- **Failure shapes:** hypothesis failure (C1+temporal adaptation matches S — clean negative) vs **method failure**. **Inconclusive (Slot 13):** diagnostic-only · fault-specific/bounded · confound-fragile · excitation-dependent. **A2 adds a severity-bounded shape.**
- **Pre-specification:** freeze gauge placement, model/hyperparams, thresholds, analysis window, seeds/scenarios before confirmatory generation. Leakage-free splits. ≥5 training seeds. Paired hierarchical bootstrap.

## Carried limitations for the Technical Report / Gate 7

1. **2^(3−1) parity residual:** `I(trajectory ; full cell)` = 1 bit in dev/pilot/val, 0 at test; main effects and two-factor interactions estimable everywhere; cannot favour either suite.
2. **The OOD arm rests on only 2 compound settings per split** (16 val / 32 test runs, 2 fault types) — thin for any OOD claim.
3. **Test severities sit partly outside the fit hull**; the severity regression head extrapolates at test.
4. **`split_group_id` is unique per reservation**, so `_assert_one_mapping(split_group_id → split)` is vacuous — the real guarantee is trajectory/fault exclusivity, which does hold.
5. **`_assert_fault_independent_context_cells`** uses `expected_cell_count = min(len(table), trajectory_count * repetitions)`, correct only because trajectory blocks are disjoint mod 8 at the actual values. Both pinned; cannot silently drift.
6. **[S33] Finding 1** — structural severity grid below the 2× synchronous margin at every reserved severity, worsening with payload.
7. **[S33] Finding 2** — realized contact is fault-caused (100% encoder bias/drift) and absent in dev/val.
8. **[NEW S34] The mild-band negative result** — neither suite separates structure at dev severities; no gauge column is significant; the only consistent structural signature is a C1 IMU channel; the 2× margin is first met near remaining EI 0.17.

## Coherence / honesty bounds (keep loud)

- `utils/synchronous.py` (Codex S9) = the single shared harmonic statistic (`harmonic_coefficients(window, valid, time_s, frequency_hz)`); `synchronous_coefficient_vector` + `coefficient_reference_distance` in `estimator.py` = the one canonical definition every pilot/screen/review imports.
- **Sensor RNG keyed on `(sensor_seed, pair_id, channel, stream)`** — `pair_id` load-bearing; screens reuse an upstream screen's `pair_id` verbatim and check CRN at 0.000e+00.
- Deployable floors are *detection*, not learned attribution; all S19 rates from ONE fixed fault setting per class; abstention untestable on this fault library; one-hot prototype probabilities NOT calibrated; **every joint-space control number comes from a condition where the structural fault causes no measurable JOINT deficit.**

## Constraints / environment / ops (load-bearing)

- **Simulation-only, one desktop:** Windows 11, Ryzen 7 8700F (8C/16T), RTX 5060 Ti **16 GB VRAM** (sm_120), 32 GB RAM, Python **3.12.10** in `./venv`. Free/OSS, commercial-use-friendly only.
- **venv has:** numpy 2.5.1, scipy 1.18.0, scikit-learn 1.9.0, matplotlib 3.11.0, mujoco 3.10.0, pandas 3.0.3, control 0.10.2, gymnasium 1.3.0, pytest 9.1.1, **torch 2.11.0+cu128**.
- **Running packet tests:** from `Reproducibility Packet/`, `..\venv\Scripts\python.exe -m pytest tests/`. **From the REPO ROOT the venv is `./venv/Scripts/python.exe` (NOT `../venv`).** Set `PYTHONIOENCODING=utf-8`; use ASCII in probe scripts.
- **To import packet utils from a scratchpad probe:** `sys.path.insert(0, "<repo>/Reproducibility Packet/scripts")` then `from utils.X import Y`.
- **Timings (measured S34):** full packet suite ~10–12 s; one MuJoCo rollout (3000 steps) ~26–30 s; the 9-rollout severity ladder ~4 min; the separability screen with a 256-pattern permutation null ~1 min per suite; reading 64 observation npz ~seconds.
- **Background jobs:** `run_in_background: true` and wait for the notification. **Python buffers stdout when redirected to a file — the log stays EMPTY until exit. Poll the results file, not the log.**
- **STANDING LESSON 1 — dry-run the analysis path before spending a rollout budget.**
- **STANDING LESSON 2 — self-audit from row artifacts / raw bytes, not the summary.**
- **STANDING LESSON 3 — restate a proxy in the contract's units before comparing to the bar.** *(S34: I nearly compared an observed-path µε distance to a floor defined on the privileged differential; measuring both is what made the ladder quotable.)*
- **STANDING LESSON 4 — for a MuJoCo screen, re-run to scratch + diff against committed.**
- **STANDING LESSON 5 — verify the live git state before trusting continuity** (S28–S34: the startup snapshot lagged EVERY time, **seven running**).
- **STANDING LESSON 6 — review a design by simulating its consequences, not by verifying its internal consistency.** Corollaries: dead arithmetic hides in small catalogs; **the dangerous confound is the one that favours you**.
- **STANDING LESSON 7 — for any pre-registration, check that the pre-registered TEXT generates the pre-registered DATA.** Corollaries: apply ONE consistent blocking standard, direction-of-bias; check a flaw is AVOIDABLE before reporting it.
- **STANDING LESSON 8 — test a guard by feeding it the exact state it was written to catch.** Corollaries: **check a flaw is REAL before reporting it** (S34: two of my "leaks" were no-op mutations in my own harness — assert your test actually changed something); report the scope you actually achieved.
- **STANDING LESSON 9 (S33) — a design review that reads the design cannot find what the design does.** A pre-registration is a claim about data and stays unverified until data exist to check it against. Corollary: **audit the yardstick before the artifact**. Second corollary: **before calling a settled parameter a defect, search the history for why it was chosen.**
- **STANDING LESSON 10 (NEW, S34) — a negative result is only readable if the same instrument produced a positive one.** The separability screen's whole value rests on the actuator positive control clearing 0.86–0.89 through the identical folds, probe class and feature construction; without it the empty structural table would have been indistinguishable from a broken pipeline. Corollary: **name what the instrument is sensitive to, not just what it found** — mine detects effects at 2–7× the healthy across-context spread and says nothing about 0.1–0.5×. Second corollary: **when the design gives you a matched pairing for free, take it** — the delivered cell structure turned an underpowered 8-vs-8 comparison into a paired one with an exact permutation null.
- **PowerShell 5.1** primary (no ternary/`??`); Bash tool also available (its `cd` persists). Use `git diff --numstat` to confirm `+N/−0` after every chat turn.
- **Root `.gitignore`** covers `venv/`, `/data/`, `tmp/`, `MUJOCO_LOG.TXT`, caches, model files, LaTeX aux, OS/IDE noise. **Root `.gitattributes`** pins `schema.json` to LF. **Packet `.gitignore`** ignores `*.npz` + caches/logs (so `results/*.json` and `*.md` ARE tracked — correct, 140 KB).

## Pointers

- Claim Sheet (in-force contract): `Claim Sheet.md` · plain-language: `Accessible Claim Sheet.md` · Study Guide Pass 1: `Study Guide/Pass 1 - Conceptual Foundation.tex`
- **Shared schema (in force, +A1):** prose `Reproducibility Packet/schema/schema-v1.0.md`; machine `schema.json`.
- **The freeze plan:** `agents/Codex/Config Freeze Readiness Review.md`.
- **The probe-amplitude record (READ BEFORE QUESTIONING 0.05 N):** `Reproducibility Packet/results/synchronous_safe_probe/synchronous_safe_probe_report.md` + Phase-2 chat lines ~425–465.
- **My S34 screen:** `Reproducibility Packet/scripts/screen_structural_separability.py` + `results/structural_separability/`.
- **CONCLUDED director chat:** `chats/Claude-Codex-Human/Better Suited Task/…- Concluded.md` + `Summary.md` — the withdrawn task-redesign directive. **A2 must stay clear of it; read its `Summary.md` if A2 discussion drifts toward changing the task or the score.**
- Director requests: `director_requests.md` (root) — entry 1 (Claim Sheet review) non-blocking, awaiting director reply.
- My foundation `agents/Claude/Literature Foundation.md` · ledger `agents/Claude/references.md` (**no S20–S34 entries — reproduction/construction/measurement/review sessions, no external sources read**) · progress reports `agents/Claude/Progress Reports/` (Phase 0/1 Close, S8, S16, S24, S32). **NEXT DUE: my Session 40, or the session that writes an approving turn on A2.**
- Live-Run README (co-maintained): root `README.md` — **Phase 2 / In Progress**, banner **2026-07-24**. **S34 added one running-log entry** (the negative separability result, stated plainly).
- **Phase-2 chat:** `chats/Claude-Codex/Phase 2 Integration and Config Freeze/…- Active.md` (**3969 lines**; my S34 turn header at line 3645, `+326/−0`; **A2 is OPEN and Codex owns the next turn**). *Note: my S34 append landed without the usual `---` separator before its header (my prepend step failed its own assertion on CRLF and was skipped); the turn itself is intact and append-only was preserved. Fix the separator step before the next append: read bytes, handle `\r\n`.*
- **Monitoring chat:** `chats/Claude-Codex-Human/Transcript Order Monitoring/…- Active.md` (S34 check clean — Codex's two S33 turns `+126/−0`, headers 3521 and 3564, Codex last; **twelfth consecutive clean append**, no note added; flag only on recurrence).
- **Scratchpad (S34, NOT committed — recreate what you need):** `append_turn.py` (binary EOF-append + 4 gates + rollback — **its CRLF prepend helper needs fixing**), `probe_s34_hardening_teeth.py` (23 adversarial guard cases), `probe_s34_swap_depth2.py` (two-layer binding proof), `probe_s34_severity_ladder.py` (**the matched-seed privileged+observed ladder — reuse this for A2 part (3), the probe-amplitude re-derivation**), `probe_s34_inventory.py` (dev run inventory + context-balance check), `probe_s34_per_channel.py` (superseded by the packet script's `per_channel_attribution`), `chk_timing.py` (trajectory grid alignment), `turn_s34.md`.
