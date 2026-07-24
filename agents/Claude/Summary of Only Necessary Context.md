# Summary of Only Necessary Context — Claude

*Rewritten every session. Restores my working context for the next session. Excludes anything already in `Project Details/Project Details.md` and `AgentPrompt.md` (I re-read those in full at session start). Last rewritten: end of Session 32, 2026-07-24 16:20 PDT.*

## Where the project is

- **Phase 2 (Execution) is OPEN.** All Phase-1 gates in force. **Schema v1.0 + Amendment A1 in force.** Contract changes run through the **amendment protocol**.
- I am **Claude**; last session was **Session 32**; next session I run is **Session 33**.
- **`config.json` is deliberately NOT frozen** and does not exist. Do not freeze a partial config. All hashes are `dev-`; no `dev-` trace may enter confirmatory analysis.
- **The development-screening arc ended long ago.** Both recovery-action families are blocked (structural S20; actuator S25/reviewed-S26), diagnosis is characterized (S macro-F1 0.995 vs C1 0.704), and the evidence keeps landing on the pre-registered **"improves diagnosis, not control"** shape (Slot 13). The project is building the confirmatory pipeline toward a config freeze.
- **GATE 3 IS CLOSED AGAIN (my S32), at the AMENDED 808-reservation state.** Gates 1, 2-foundation, 2-role-write-path also DONE and jointly approved. **Gate 2 is still BLOCKED overall** — the real multi-setting MuJoCo generator + role-completeness audit are unbuilt. **Codex owns the next turn.**
- **THERE IS NO OPEN REVIEW LOOP.**
- **NO PROGRESS REPORT IS DUE.** I wrote the regular 8-cadence report at S32 (`agents/Claude/Progress Reports/Progress Report Session 32.md`, covers S25–S32). **Next regular: my Session 40**, unless a phase transition or an approved Claim-Sheet amendment fires one sooner.

## What I did in S32 (two things: re-reviewed the amended Gate-3 assignment → APPROVED; wrote the progress report)

Codex's S31 ran after my S31 (**Standing Lesson 5 again — startup snapshot said HEAD=`Codex Session 28`; live `git log` showed `bbce91e Codex Session 31`. FIFTH consecutive lag. Always verify live.**). Codex accepted my S31 approval of the 656 state, then **took the optional 2→4 realizations remedy I had offered**, which changed the self-hashed document and correctly reopened Gate 3 for exact-state review.

**Decision: `APPROVE_GATE3_ASSIGNMENT_V0_1`, no edits to any review-target file. Gate 3 closed at joint same-state approval.**

**The approved state's identity (Gate 3 is locked at these bytes):**
```text
assignment hash        dev-eec59ec8a296a9a4ff4909f8e7f1de91a0a8f4bf289ae1533a427d1a87bc33f1
assignment JSON        76255a8089f3e27d893b26d981cbf50e808bd75ba518c44b55c4635ec83514ae
gate3_assignment.py    01ffba74d8b1da32409ef5cea66ba3f74e551735e9705bfadc2819a456d64814
test_gate3_assignment  fe56cbf49dec4fcaf8ab742b4453896d60990901dcfa584d9606c4e3823ff9eb
packet README          5b855e0fea57aac770d1a005a0d4a784234f152d523eae555b6113d076b5dfa2
bound draft config     dev-0211f2e71a473fef3c30cd53fd0a269df45156a3d58e83097bac7a5638bf6180
```
**Superseded, never approve or embed:** `dev-70832daa…765de` (the 656 state, approved S31 then amended) and `dev-5939ff5f…0cedb` (blocked S30).

**The amendment:** dev and pilot `realizations_per_trajectory_fault` 2 → 4; reservations dev 76→152, pilot 76→152 (val 168, test 336 unchanged); total **656 → 808**; projected manifest rows 13,120 → **16,160**. Plus a new fail-loud invariant `_assert_context_axes_vary_within_trajectories`: every `(split, trajectory_spec_id, fault_setting_id)` group must realize both profiles on payload, environment AND contact.

**What I measured (all clean):** 808/808 row-for-row identical between my independent prose-rule re-derivation and `expand_reservations` (13 identity fields); independent canonical hash matches; all five file digests match; `I(fault ; context cell)` = **0.0000000000 bits** in all four splits; **`I(trajectory ; payload/environment/contact)` = 0.0000000000 bits in all four splits** (was 1.000 bit in dev/pilot); aliased `(trajectory,fault)` groups 0/38, 0/38, 0/42, 0/42; cells per fault **8/8/8/8** (was 4/4/8/8); one distinct cell distribution per split; per-axis marginals exactly balanced; all three S30 leak signatures absent (`payload XOR env` locked 0/19·0/19·0/21·0/21, healthy-impossible 0.00%, no bit separates severity); compound/OOD match the known distribution; 3,232 seeds zero collisions; 808 unique scenario/pair/group IDs; zero cross-split known-fault-tuple reuse. Focused **20 passed**, full packet **378 passed in 9.08 s**, validator PASS, no `config.json`, no `data/`.

**Diagnostic-trajectory-only check (the one that matters most for this project):** temperature reaches observations ONLY through `gauge_obs` (S-exclusive) and the diagnostic trajectory is where S's exclusive signal lives, so I restricted the measurement there: `I(fault ; payload/env/contact)` = 0.00000 in every split, temperature marginal balanced 38/38, 38/38, 42/42, 84/84. Every fault setting evenly split across both trajectories.

**I TESTED THE GUARD BY FEEDING IT THE STATE IT WAS WRITTEN TO CATCH.** The exact 656-reservation state I approved in S31 is now **correctly REJECTED** by the new invariant; the handoff state still validates. Scoping note I recorded honestly: my other three adversarial designs were rejected earlier by the byte-pinned `context_cell_table` equality check and never reached the new invariant, so through the document its only reachable trigger is a repeat-budget change (Codex's monkeypatched regression covers the unreachable path).

### S31's carried limitation #1 is RESOLVED — and the ladder caveat CHANGED

**The dev/pilot payload↔trajectory alias is gone.** Do not carry it forward.

**Measured per-trajectory context design:**
```text
dev   traj 0 -> cells [4,5,6,7]   traj 1 -> cells [0,1,2,3]
pilot traj 0 -> cells [4,5,6,7]   traj 1 -> cells [0,1,2,3]
val   traj 0 -> cells [4,5,6,7]   traj 1 -> cells [0,1,2,3]
test  traj 0 -> cells [0..7]      traj 1 -> cells [0..7]
```
**dev, pilot and val are now structurally identical**, so the **pilot→val rung is a clean single-variable escalation** (confound severity only). My old S31 Gate-7 caveat — "pilot is structurally matched to dev, not to val/test" — **is now FALSE. Do not carry it forward verbatim.** The accurate replacement: *pilot→val moves one variable; val→test additionally moves from a half-fraction per trajectory to the complete factorial.*

**The residual I recorded instead of blocking:** at 4 realizations each trajectory gets one parity coset, so `I(trajectory ; full cell)` = **1 bit** in dev/pilot/val (**0** at test). This is the defining contrast of a **2^(3−1) fractional factorial**: all three main effects and all three two-factor interactions are estimable within every trajectory; only the three-way interaction is confounded with trajectory. **It cannot move the result in either direction** — trajectory is the commanded task, equally visible to C0/C1/S in `tau_cmd`/`q_obs`, and since `I(fault ; cell) = 0` more context knowledge cannot improve a fault prediction. **One honest sentence in the Gate-7 driver and the Technical Report; no amendment.**

## GATE STATUS — the freeze path (central reference)

**Governing decision: `BLOCK_CONFIG_FREEZE_PENDING_PRECONFIRMATORY_BUILD_AND_VALIDATION`.** Sequencing (load-bearing): a **versioned DRAFT config** governs development/validation data generation; the **final immutable `config.json` freeze comes AFTER model implementation + validation-only hyperparameter/threshold selection and BEFORE any untouched `test` payload.**

**Seven gates + ownership (Phase-1 labor split):**
1. **Machine schema + config authority** — **DONE, APPROVED S28.** *(Codex/shared.)*
2. **Role-separated storage, deployable loader, leakage/split audits** — **FOUNDATION DONE (S28) + ROLE-WRITE PATH DONE (S29).** **STILL BLOCKED OVERALL:** the real Gate-3-assigned multi-setting MuJoCo generator + its role-completeness audit are unbuilt. **Unblocked to proceed — Codex's next turn.** *(Codex/shared.)*
3. **Multi-setting design + manifest** — **CLOSED, JOINTLY APPROVED S32 at 808 reservations.** *(shared)*
4. **Matched learned models** — **MINE.** `TemporalAttributionNet` + `RMALatentEncoder` behind shared `[W,D]` interface; within-suite capacity ladder; ≥5 seeds; identical protocol IDs across C0/C1/S. *Toolchain verified ready (torch cu128 / sm_120).* **WAITS on the Gate-2 live data layout.**
5. **Calibration/abstention/OOD/uncertainty** — **MINE.** Per-suite calibrated probs (Brier/NLL/ECE), abstention + OOD thresholds on validation, `severity_uncertainty` as a **bias-inclusive predictive error scale** (NOT in-sample residual dispersion — my S24 finding: understates true by 5.72× for S). **WAITS on validation data.**
6. **Confirmatory controller protocol** — **DECIDED S27 (both agents):** freeze the fair four-arm comparison (no-action/detection-only · transparent attribution-driven · RMA · oracle) and **RUN the pre-registered paired C1-vs-S comparison**; do NOT narrow to information-only, do NOT retune blocked families post-hoc. *(Codex owns controller; diagnosis→control seam shared.)*
7. **Evaluation driver + confirmatory manifest** — **MINE.** One CLI owning the `[t_c,t_c+5s]` slice, role joins, paired C1/S table, exclusions, CIs; rejects `dev-`/wrong-hash/cross-role/incomplete-pair/truncated. **Must implement THREE pre-registered rules:** (a) the `ood_flag` exclusion from known-class metrics; (b) the **degradation-ladder rule** (agreed S30/S31): report the same paired C1-vs-S contrast at pilot, val and test; a test null is hypothesis failure **only if** the contrast is present at earlier rungs; a contrast that decays with the rung is reported as **generalization-limited**, not evidence against structural sensing; (c) **[UPDATED S32]** the caveat that **pilot→val moves one variable (confound severity) while val→test additionally moves from a half-fraction per trajectory to the complete factorial.**

**Order:** (1)✓ → (2 foundation)✓ → (2 role-write path)✓ → (3 assignment)✓✓ → **(2 live generator + role-completeness audit) [Codex] ← WE ARE HERE** → (4/5 models+calibration on validation) [me] → (6 controller + sample-size) [shared] → **joint immutable freeze** → one-shot confirmatory generation + eval (7) → Phase 3. **Do NOT build models against a data layout that does not exist yet.**

Not freeze blockers (still required before completion): Slot-8 verification artifact (after confirmatory outputs); Technical Report / Accessible Piece / Study Guide Pass 2 (Phase 3); fresh-environment packet validation.

## The single most important things to do next session (Session 33)

1. **Verify live `git log` HEAD first** (Standing Lesson 5 — it has now lagged FIVE sessions running). Read Codex's newest HumanReport + the Phase-2 chat tail.
2. **Most likely: Codex hands off the embedded draft config + the real generator + role-completeness audit.** That is a **Gate-2 review**. **The key question is whether the generated data actually realize the approved 808-reservation assignment** — measure the produced manifest against the 656→808 reservations directly; do NOT trust the generator's own report. **Expect a NEW draft-config hash** once Codex embeds the assignment under `values.scenario_manifest` and drops Gate 3 from the open-gate list.
3. **Recreate the probes** (described under "Scratchpad") — they are not committed.
4. **My lane opens once the live data layout exists:** Gate 4 models, then Gate 5 calibration on validation only.
5. **Check whether the packet `.gitignore` needs new rules** the first time Codex commits real generated data.
6. **Do NOT freeze a partial config.**

## Review-cycle state

- **NO OPEN LOOP.** Gate-3 assignment (808) closed at joint same-state approval, my S32.
- **CLOSED, do not reopen:** Gate-3 assignment 808 (S32), Gate-3 assignment 656 (S31; superseded by the S31-Codex amendment, not by a defect), Gate-2 role-write path (S29), Gate-1/Gate-2-foundation (S28), Config-Freeze Readiness Review (S27), actuator-action (S26), class-probability (S25).

## MONITORING DUTY (standing)

- **S32 check CLEAN** — Codex's S31 append was a verified **+89/−0** pure tail addition (2948 → 3037), exactly one S31 header at line 2952, Codex physically last. **Tenth consecutive clean append.** Did NOT post to `Transcript Order Monitoring` (flag only on recurrence; keep the thread lean).
- **REUSE the binary-EOF-append approach for every chat turn.** My `append_turn.py` lives in the (uncommitted) session scratchpad and **will be gone next session — recreate it** (binary EOF-append + 4 gates: marker-absent-before / prior-bytes-exact-prefix / marker-once-after-boundary / turn-physically-last, with rollback on any gate failure). **Pass an ASCII-only unique marker** (the timestamp string, e.g. `Session 32, 2026-07-24 16:08 PDT`). Verify `git diff --numstat` shows `+N/−0` after. My S32 turn recorded **+82/−0** (transcript now **3119 lines**). The transcript is normal text (not byte-hashed), so a benign "LF→CRLF" git warning on append is expected and fine.

## Codex's Gate-1/2/3 layer — reference

`Reproducibility Packet/`:
- **`schema/schema.json`** (approved S28) — machine schema v1.0 + A1. Roles: identity_manifest, plant (20 fields = `PrivilegedRecord`), observations (deployable, fixed 6-channel registry + static suite mask), labels (8), estimator_outputs (9, `N_decisions` sparse axis), controller_logs (6). Channel registry: q_obs/qd_obs/tau_cmd (C0/C1/S), current_proxy_obs/imu_obs (C1/S), gauge_obs[4] (**S only**). **`schema_sha256 = 0dae0dd0…3e942f`** (LF-pinned via root `.gitattributes`).
- **`config/draft-config-v0.1.json`** (approved S28) — the versioned DRAFT (`status=draft`, `confirmatory_payloads_allowed=false`, gates 2–7 open). Frozen candidates: plant (`n_def=90`, gauges [0.25,0.75], A1 safety thresholds, `point_count_per_link=17`, `endpoint_contact_plane_z_m=0.2`), timing (`f_ctrl=500`, `window_steps=768`, `stride=16`, probe 0.05 N / 0.8 Hz / 1 cyc raised_cosine, `analysis_window_s=5.0`), full sensor_model constants. **`config_hash = dev-0211f2e7…6180`**. **Codex embeds the approved Gate-3 assignment into this next and recomputes the hash — expect a NEW draft-config hash after its next session.**
- **`scripts/utils/config_contract.py`** (S28) — strict JSON, canonical hashing, draft/frozen lifecycle; frozen wall requires name `config.json`, `APPROVE_CONFIG_FREEZE`, `open_gates==[]`, no null/empty, no `dev-`, 64-hex hash.
- **`scripts/utils/storage_contract.py`** (S28) — identity manifest + role indexes; whole-group split audit; `DeployableObservationLoader` (suite-scoped, unavailable channels all-NaN + masked, traversal guard, dtype/timing checks).
- **`scripts/utils/role_contract.py`** (S29) — manifest-bound writers/loaders for all four non-observation roles + observations; draft-`test` refusal; allowlisted `dev|pilot|val` `SupervisedTrainingJoin` yielding observation + label only.
- **`scripts/build_data_contract_fixture.py`** (S29) — deterministic synthetic role-completeness fixture (two builds byte-identical). Explicitly NOT a Gate-3 assignment or research data.
- **`scripts/utils/gate3_assignment.py` + `config/proposed-gate3-assignment-v0.1.json` + `scripts/validate_gate3_assignment.py` + `tests/test_gate3_assignment.py`** (S29, corrected S30, amended S31, **approved S32**, 20 tests). **Assignment structure worth remembering:** 19 known settings per split (1 healthy + 2 structure loc1 + 4 actuator loc{0,1} + 12 sensor {bias,drift,dropout}×loc{0,1}×2 severities), +2 compound/OOD in each of val/test (label = first component, `compound_flag`/`ood_flag` true, excluded from four-way metrics); **2 trajectories per split** (one ordinary, one diagnostic), split-exclusive; **realizations 4/4/4/8**; seed bases 110000/210000/310000/410000, seeds `base + 10*ordinal + {0,1,2,3}` (ordinal resets per split); no known fault tuple reused across any split pair; `dataset_identity_train_seed=0`; training-seed pool `[31001…31005]`; reservations **152/152/168/336 = 808**; projection **16,160** manifest rows. Expansion is a nested loop **trajectory → fault setting → replicate**, context cell = `context_cell_table[(trajectory_index * realizations + replicate) % 8]`, and **`fault_index` is not an input to anything**.
- **Validator CLI flags are `--assignment` / `--schema` / `--config`** (NOT `--draft-config`). **`validate_assignment(document, config)` takes a loaded document + a `ValidatedConfig`, not paths** — build the config with `utils.config_contract.load_config(config_path, schema_path)` first.
- Tests: `test_data_contract.py` (18) + `test_role_contract.py` (11) + `test_gate3_assignment.py` (20). **Full packet: 378 tests green (S32 re-run).**
- Packet `README.md` documents Step 2A (fixture) and Step 2B (assignment validator). (Packet runbook uses its OWN `.\.venv\Scripts\python.exe` convention — don't "fix" to project-root `venv`.)

## My lanes — current state (unchanged this session)

`Reproducibility Packet/scripts/utils/estimator.py`:
- **`WindowFeatureExtractor(window_steps=W=768, probe_frequency_hz=0.8)`**: `[W,D]` left-padded + per-column `[last,mean,std,slope,sync_cos,sync_sin,sync_amplitude,valid_fraction]` over 18-col registry → 144 features. Constants: `N_FEATURE_STATS=4`, `N_EXTRA_FEATURES=4`, sync cols 4/5/6, `VALID_FRACTION_COL=7`, `DIAGNOSTIC_PROBE_HZ=0.8`, `MIN_SYNC_SAMPLES=8`.
- **`WindowNoveltyDetector`** (detect+abstain) · **`CoefficientReferenceDetector`** (2nd interpretable rung; canonical `synchronous_coefficient_vector` + `coefficient_reference_distance`; `fit_reference` atomic; `calibrate_threshold` fail-loud below `ceil(min_tail/far)`) · **`_SCORE_STD_FLOOR=1e-3`** shared · **`SeverityRidgeHead`** (deployable severity read-out; `train_residual_std` is IN-SAMPLE — never feed a confidence gate) · **`leave_one_group_out_residuals`** (CALIBRATION-role diagnostic) · **`OracleInterface(onset_time_s)`** · **`EstimatorCommandPolicy`** (seam adapter; runs estimator every `stride`, ZOHs OUTPUT) · `RECOMMENDED_WINDOW=(768,16)` pilot proposal · **learned rungs specified-not-built (Gate 4 — MINE).**
- **`utils/metrics.py` + `utils/stats.py`** (approved through S11): `tracking_reduction_pct(j_baseline,j_treatment)=100·(j_baseline−j_treatment)/j_baseline`, `j_5s` fail-loud on full `[t_c,t_c+5s]`, `safety_incident_rate`, `safety_regression_delta` (matched `[T,7]` guard), `hierarchical_bootstrap_ci` (crossed pair×seed). **Eval driver (Gate 7) — build once the frozen data layout exists.**
- **Screens (all closed):** `screen_severity_estimation_quality.py` (80 arms; held-out MAE C1 0.0065 / S 0.0076), `screen_severity_action_boundary.py` (40 arms; paired −0.1177% mean), `screen_actuator_probability_channel.py` (36 arms; 5.07 pp graded / 10.85 pp gate-crossing). `tests/test_recovery_seam.py` (4 tests).

## Codex's OTHER lanes — current state

- `screen_actuator_recovery_action.py` (S25; I approved S26). Selected `actuator_gain_remaining_0p25`; safe cap-3 → 8.25 pp source-specific margin [8.09,8.53] < 10-pp bar → `BLOCK_ACTUATOR_ACTION_FAMILY_AT_SOURCE_SPECIFIC_GATE`. cap-5 crosses the bar (10.18 pp) but fails A1 lifecycle safety (19 incident arms).
- `utils/recovery_control.py` — `GainScheduledRecoveryController`. Actuator: `multiplier=1+p·(capped_compensation−1)`, `capped=min(1/max(remaining,floor),cap)`. Gate `_confident_source` = not-abstained AND unique-argmax==source AND p≥0.5 AND finite σ≤0.25. `maximum_gain_compensation=2.0`, `minimum_gain_remaining=0.25`, `torque_abs_limit=(1.0,0.5)`.
- `screen_fault_tracking_deficit.py` (S22): gate `required_reduction_pct`=12%, `required_deficit_pct`=13.636%; structural rows produced NO joint deficit.
- `screen_structural_recovery_action.py` (S20): `BLOCK_STRUCTURAL_RECOVERY_ACTION_FAMILY`; ~70% of benefit at the *unfaulted* joint.
- `run_bounded_noisy_information_review.py` (S19): S PASSES info+action gates (macro-F1 0.995, 100% per-fault detection, 2.1% FA); C1 BLOCKS (0.704, 8.3% structural recall). One-hot mechanism probs (NOT calibrated).
- `utils/task_control.py` (S17/S18): `BoundedTaskProfile` (rest→(0.30,0.30) rad by 3.0 s→hold→rest by 5.0 s — JOINT-SPACE targets), `ObservedJointPDController` (kp (0.05,0.03), kd (0.005,0.003), torque limits (0.20,0.10); reads ONLY `q_obs`/`qd_obs`).
- `utils/cable_mechanics.py` + `utils/cable_plant.py` + `make_mujoco_plant_trace.py` (S14/S15): A1 safety flags = `|q|>π`, `|qd|>10`, 3-D tip radius >0.82 from `[0,0,0.5]`, `max|gauge|>500 µε`, `contact_state[0]>5 N`. **Fault severity = REMAINING fraction.** **`cable_plant.py:124-125` restricts structural faults to location `{-1,1}`** (verified S30 — a genuine plant constraint, honestly declared; do not re-litigate). `agents/Codex/Config Freeze Readiness Review.md` = the seven-gate plan (I approved S27).

## The evidence tables (development-evidence boundary — why we expect diagnostic-only)

**Structural (Codex S20):** remaining EI 0.50/0.25/0.10/0.05 → mean peak |gauge| 38.4/72.4/152.8/259.7 µε (healthy 19.2) but mean **joint** tracking deficit +0.08%/−0.89%/−2.23%/−5.00% — monotone in information, monotone the WRONG way in joint control (damage moves to the TIP, which the joint score never measures).

**Control-layer shape (Codex `bounded_noisy_information_review`):** healthy/actuator/sensor → S has no exclusive info + 0% tracking change; **structure → S exclusive info YES, C1 withholds actionable, `s_tracking_change_pct` −18.58%.** C1 per-class recall: structure **0.083**, else 1.000. **Where S has exclusive info there's no control headroom; where there's headroom S has no exclusive info** = the pre-registered Slot-13 diagnostic-only landing.

## The agreed contract's load-bearing specifics

- **Sensor suites (controlled variable):** C0 = joint encoders + commanded actuation · **C1 = C0 + noisy motor-current nominal-Kt torque estimate + one distal 6-axis IMU** · **S = C1 + four fixed strain/curvature gauge stations** · O = privileged oracle. **Temperature is observable ONLY through `gauge_obs`, i.e. only in S** (`sensor_model.py:423-424`, 10 µε/°C) — this fact made the S30 finding blocking and shaped both the S31 and S32 trade-off analyses; keep it in mind for any future confound design.
- **Two settled correctness points:** actuator-gain fault acts *downstream* of the current proxy (C1 not handed true delivered torque); encoder fault has a *relational* signature.
- **Success bar (pre-declared, BOTH layers):** S improves held-out four-way macro-F1 over C1 by **≥0.05 absolute** (paired 95% excludes zero; every source-class recall diff lower-95% above **−0.02**) AND reduces the **5-s post-change integral of absolute tracking error by ≥10%** (`100·(J_C1−J_S)/J_C1`, paired 95% excludes zero, no safety regression) under realistic confounds. Known-class abstention = error in headline macro-F1.
- **Failure shapes:** hypothesis failure (C1+temporal adaptation matches S — clean negative) vs method failure. **Inconclusive (Slot 13):** diagnostic-only (**the shape the evidence keeps landing on**) · fault-specific/bounded · confound-fragile · excitation-dependent.
- **Pre-specification:** freeze gauge placement, model/hyperparams, thresholds, analysis window, seeds/scenarios before confirmatory generation. Leakage-free splits. ≥5 training seeds. Paired hierarchical bootstrap.

## Carried limitations for the Technical Report / Gate 7 (all pre-registered, none blocking)

1. **[REPLACED S32]** The dev/pilot payload↔trajectory alias is **RESOLVED** by the 2→4 amendment. What remains is the **2^(3−1) parity residual**: `I(trajectory ; full cell)` = 1 bit in dev/pilot/val, 0 at test; main effects and two-factor interactions estimable everywhere; cannot favour either suite. **State the ladder honestly:** pilot→val moves one variable; val→test additionally moves half-fraction → full factorial.
2. **The OOD arm rests on only 2 compound settings per split** (16 val runs / 32 test runs, 2 fault types) — thin for any OOD claim.
3. **Test severities sit partly outside the fit hull** (structure/actuator 0.35 more severe than dev's `{0.5,0.75}` or val's `[0.4,0.9]`; `encoder_bias 0.015` rad milder than anything trained) — harmless for classification, but the **severity regression head extrapolates** at test.
4. **`split_group_id` is unique per reservation**, so `_assert_one_mapping(split_group_id → split)` in `audit_identity_manifest` is vacuous — the real whole-group guarantee is trajectory/fault exclusivity, which does hold.
5. **Minor, noted not raised (S32):** `_assert_fault_independent_context_cells` computes `expected_cell_count = min(len(table), trajectory_count * repetitions)`, which is correct only because trajectory blocks are disjoint mod 8 at the actual values. Both the table and the 2-trajectories-per-split structure are pinned, so it cannot silently drift.

## Coherence / honesty bounds (keep loud)

- `utils/synchronous.py` (Codex S9) = the single shared harmonic statistic; `synchronous_coefficient_vector` + `coefficient_reference_distance` in `estimator.py` = the one canonical definition every pilot/screen/review imports.
- **Sensor RNG keyed on `(sensor_seed, pair_id, channel, stream)`** — `pair_id` load-bearing; screens reuse an upstream screen's `pair_id` verbatim and check CRN at 0.000e+00.
- Deployable floors are *detection*, not learned attribution; all rates from ONE fixed fault setting per class, held out over sensor noise only; abstention untestable on this fault library (min margin 0.90); one-hot prototype probabilities NOT calibrated; **every joint-space control number comes from a condition where the structural fault causes no measurable JOINT deficit — the damage is at the tip, which the joint-space score never charges for.**

## Constraints / environment / ops (load-bearing)

- **Simulation-only, one desktop:** Windows 11, Ryzen 7 8700F (8C/16T), RTX 5060 Ti **16 GB VRAM** (Blackwell/sm_120), 32 GB RAM, Python **3.12.10** in `./venv` (use `.\venv\Scripts\python.exe`/`pip.exe`, never bare). Free/OSS, commercial-use-friendly only.
- **venv has:** numpy 2.5.1, scipy 1.18.0, scikit-learn 1.9.0, matplotlib 3.11.0, mujoco 3.10.0, pandas 3.0.3, control 0.10.2, gymnasium 1.3.0, pytest 9.1.1, **torch 2.11.0+cu128** (CUDA 12.8, sm_120-verified).
- **Running packet tests:** from `Reproducibility Packet/`, `..\venv\Scripts\python.exe -m pytest tests/`. **Running a script:** from `Reproducibility Packet/` as `..\venv\Scripts\python.exe scripts\<name>.py`. **From the REPO ROOT the venv is `venv/Scripts/python.exe` (NOT `../venv`).** Set `PYTHONIOENCODING=utf-8` for unicode-printing scripts (the Bash tool mangles non-ASCII in printed output — use ASCII in probe scripts).
- **Timings (measured, 8 workers):** actuator-action screen (100 arms) ~minutes; info review ~12–20 min; deficit ~20 min (84 arms); severity-quality ~7–9 min (80 arms); fixture build ~seconds; full packet suite ~9 s. Run long jobs in background; **a pipe through `tail`/`*>` buffers until exit — poll for the results file.**
- **STANDING LESSON 1 — dry-run the analysis path before spending a rollout budget.**
- **STANDING LESSON 2 — self-audit from row artifacts / raw bytes, not the summary.**
- **STANDING LESSON 3 — restate a proxy in the contract's units before comparing to the bar** (`100·(J_C1−J_S)/J_C1`).
- **STANDING LESSON 4 — for a MuJoCo screen, re-run to scratch + diff against committed.**
- **STANDING LESSON 5 — verify the live git state before trusting continuity** (S28–S32: the startup snapshot lagged EVERY time). For learned-model work, verify the toolchain with a real GPU op, not the flag.
- **STANDING LESSON 6 (S30) — review a design by simulating its consequences, not by verifying its internal consistency.** **Corollary: dead arithmetic hides in small catalogs** — any formula whose behaviour depends on a catalog size must either assert that size or be replaced by an explicit table. **Second corollary: the dangerous confound is the one that favours you** — a leak that hurt the hypothesis would surface as a disappointing result and get investigated; one that helps surfaces as a win.
- **STANDING LESSON 7 (S31) — for any pre-registration, check that the pre-registered TEXT generates the pre-registered DATA.** Re-derive the artifact independently from the document's own prose rule and diff row-for-row against the code that will actually run. Internal-consistency tests verify code against itself and cannot see prose/code divergence. **Corollary: apply ONE consistent blocking standard, and make it direction-of-bias.** **Second corollary: check that a flaw is AVOIDABLE before reporting it as one.**
- **STANDING LESSON 8 (NEW, S32) — test a guard by feeding it the exact state it was written to catch.** The cheapest validation of Codex's new invariant was the previously approved design; it converted "the code looks right" into "the code refuses the design that caused this amendment." **Corollary: check that a flaw is REAL before reporting it at all — my own reviewing tool produced a false positive** (a coarse `(class, location, severity)` tuple that dropped `subtype`, colliding `dev encoder_bias 0.05 rad` with `val encoder_dropout 0.05 probability`). The reviewer's instrument needs the same skepticism as the artifact. **Second corollary: report the scope you actually achieved** — three of my four adversarial cases were caught by an earlier pin and never exercised the new guard; say so rather than implying broader coverage.
- **PowerShell 5.1** primary (no ternary/`??`; parens in unquoted bash break `eval` — quote or use the Grep tool); Bash tool also available (its `cd` persists between calls — check where you are). Use `git diff --numstat` to confirm `+N/−0` after every chat turn.
- **Root `.gitignore`** covers `venv/`, `tmp/`, `MUJOCO_LOG.TXT`, caches, model files `*.pt/*.pth/*.ckpt/*.onnx`, LaTeX aux, OS/IDE noise. **Root `.gitattributes`** pins `Reproducibility Packet/schema/schema.json` to LF. **Packet `.gitignore`** ignores `*.npz` (+ caches/logs); small JSON/CSV/MD artifacts intentionally tracked. **When Codex generates real research data, check whether the packet `.gitignore` needs new rules before committing.**
- **Software-engineering standard:** `argparse`, no hard-coded paths, one purpose, shared logic in `utils/`, docstrings, prints progress, fails loud. Licensing: code MIT, prose CC BY 4.0.

## Pointers

- Claim Sheet (in-force contract): `Claim Sheet.md` · plain-language: `Accessible Claim Sheet.md` · Study Guide Pass 1: `Study Guide/Pass 1 - Conceptual Foundation.tex`
- **Shared schema (in force, +A1):** prose `Reproducibility Packet/schema/schema-v1.0.md`; machine `schema.json`.
- **The freeze plan:** `agents/Codex/Config Freeze Readiness Review.md` (I approved same-state S27).
- **My lanes:** sensor `utils/{schema_types,sensor_model,rng,synthetic_plant}.py`; eval `utils/{metrics,stats}.py`; estimator `utils/estimator.py`; synchronous floor `scripts/analyze_synchronous_detection_floor.py`; shared seam test `tests/test_recovery_seam.py`; the three severity/probability screens + tests + `results/`.
- **Codex's lane:** `utils/{cable_mechanics,cable_plant,online_loop,recovery_control,residual_baseline,task_control}.py`; **`utils/{config_contract,storage_contract,role_contract,gate3_assignment}.py` + `scripts/{validate_data_contract,build_data_contract_fixture,validate_gate3_assignment}.py` + `tests/{test_data_contract,test_role_contract,test_gate3_assignment}.py` + `schema/schema.json` + `config/{draft-config-v0.1,proposed-gate3-assignment-v0.1}.json`**; the plant/screen scripts + tests/results.
- **Phase-2 chat:** `chats/Claude-Codex/Phase 2 Integration and Config Freeze/…- Active.md` (**3119 lines**; my S32 `APPROVE_GATE3_ASSIGNMENT_V0_1` = tail; **NO open loop**).
- **Monitoring chat:** `chats/Claude-Codex-Human/Transcript Order Monitoring/…- Active.md` (S32 check clean, no note added; flag only on recurrence).
- **CONCLUDED director chat:** `chats/Claude-Codex-Human/Better Suited Task/…- Concluded.md` + `Summary.md` — the withdrawn task-redesign directive. Read its `Summary.md` if the fairer-task idea resurfaces.
- Director requests: `director_requests.md` (root) — entry 1 (Claim Sheet review) non-blocking, awaiting director reply.
- My foundation `agents/Claude/Literature Foundation.md` · ledger `agents/Claude/references.md` (**no S20–S32 entries — reproduction/construction/measurement/review sessions, no external sources read**) · progress reports `agents/Claude/Progress Reports/` (Phase 0/1 Close, S8, S16, S24, **S32**). **NEXT DUE: my Session 40.**
- Live-Run README (co-maintained): root `README.md` — **Phase 2 / In Progress**, banner **2026-07-24**. **S32 added one running-log entry** (amended blueprint re-derived and approved; alias zero; guard confirmed to reject the superseded state; ladder rungs now single-variable through val).
- Scratchpad (this session, NOT committed): **`append_turn.py`** (binary EOF-append + 4 gates + rollback — REUSE/recreate; pass an ASCII marker), **`probe_gate3_amendment_v3.py`** (the 6-part audit: independent canonical hash, independent row-for-row re-derivation from the JSON prose, per-split leak measurements incl. `I(trajectory;axis)`, seed/identity hygiene, manifest/interlocks, then the project validator LAST — **recreate it to review any new assignment state or the generated manifest**), **`probe_guard_teeth.py`** (adversarial: feeds the validator the superseded state + degenerate tables, and measures per-trajectory ladder comparability), `turn_s32.md` (my appended turn).
