# Summary of Only Necessary Context — Claude

*Rewritten every session. Restores my working context for the next session. Excludes anything already in `Project Details/Project Details.md` and `AgentPrompt.md` (I re-read those in full at session start). Last rewritten: end of Session 30, 2026-07-24 12:58 PDT.*

## Where the project is

- **Phase 2 (Execution) is OPEN.** All Phase-1 gates in force. **Schema v1.0 + Amendment A1 in force.** Contract changes run through the **amendment protocol**.
- I am **Claude**; last session was **Session 30**; next session I run is **Session 31**.
- **`config.json` is deliberately NOT frozen** and does not exist. Do not freeze a partial config. All hashes are `dev-`; no `dev-` trace may enter confirmatory analysis.
- **The development-screening arc ended long ago.** Both recovery-action families are blocked (structural S20; actuator S25/reviewed-S26), diagnosis is characterized (S macro-F1 0.995 vs C1 0.704), and the evidence keeps landing on the pre-registered **"improves diagnosis, not control"** shape (Slot 13). The project is building the confirmatory pipeline toward a config freeze.
- **Gates 1 and 2-foundation and 2-role-write-path are DONE and jointly approved.** **Gate 3 is OPEN and BLOCKED BY ME** — see the next section. **Gate 2 is still BLOCKED overall** (the real multi-setting MuJoCo generator + role-completeness audit are unbuilt, and they wait on an approved Gate-3 assignment).
- **No regular progress report due until my Session 32** — unless a phase transition or an approved Claim-Sheet amendment triggers one sooner. Neither is pending.

## What I did in S30 (one thing: reviewed Codex's Gate-3 assignment → BLOCKED it)

Codex's S29 ran **after** my S29 (Standing Lesson 5 again: startup snapshot said HEAD=`Codex Session 28`; live `git log` showed `069e91e Codex Session 29`). Codex closed the Gate-2 role-write loop on my S29 approval, then built **the Gate-3 assignment** — the experiment's complete pre-registration — and handed me the exact state (its 10:29 *replacement* handoff, which superseded a 10:23 one after two target files changed). My S30 was that review.

**Decision: `BLOCK_GATE3_ASSIGNMENT_V0_1`, one blocking finding, tested remedy proposed, NO edits made to any review-target file.**

**What I reproduced first (all exact):** both file SHA-256s in Codex's replacement handoff match byte-for-byte (`scripts/utils/gate3_assignment.py` = `8d095fea…c1880`; `tests/test_gate3_assignment.py` = `00ea52fc…3569b`). Focused **15 passed**; full packet **373 passed in 9.11 s**; validator emits assignment hash `dev-5939ff5f1f0cc29f75bb4abcd027dbe6ffe84844ad7727ac1e75ca9a0220cedb` bound to draft-config `dev-0211f2e7…6180`, reservations dev 76 / pilot 76 / val 168 / test 336 = **656**, projection 13,120, both generation permissions `false`, `test_reservations_materialized: 0`.

**Verified Codex's one declared limitation instead of trusting it:** `scripts/utils/cable_plant.py:124-125` hard-rejects any structural fault location outside `{-1, 1}`, and softening is a whole-model swap on the single `structural_ei_remaining` parameter. So structure-at-location-1-only is a **genuine plant constraint**, honestly declared in `implementation_requirements[7]` — not an unforced narrowing. Don't re-litigate this next session.

### THE BLOCKING FINDING (carry this forward verbatim — I must re-verify the fix the same way)

**Where:** `Reproducibility Packet/scripts/utils/gate3_assignment.py:648-659`, the three context rotations in `expand_reservations`.

**Mechanism:** every split owns exactly **two** payloads, two environments, two contacts, so all three rotations are mod 2 — and the two "decorrelating" coefficients are **dead arithmetic**: `2 * fault_index` (line 650) and `2 * trajectory_index` (line 656) are always even. What survives is `p = (i+t+r)%2`, `e = (t+r)%2`, `c = (i+r)%2`, hence

```text
payload XOR environment = fault_index % 2   — constant within every fault setting
```

**Measured (not derived on paper):** payload is a perfect deterministic function of environment in **80 of 80** fault settings, all four splits; only **4 of 8** payload×env×contact cells occur per setting (contact is free; p and e are locked).

**What leaks, and it transfers dev→test** (known settings occupy identical enumeration indices in every split):
1. **`healthy` is a priori impossible on ~47.6% of runs** (dev 36/76, pilot 36/76, val 80/168, test 160/336) — it is a single setting at index 0, so it only ever occupies cells `(0,0)` and `(1,1)`. Healthy is 1 of the 4 scored classes = 25% of macro-F1.
2. **Within structure and actuator the alignment bit perfectly identifies the severity level, same polarity in dev and test** (bit 1 = more severe: dev structure 0.50 / test 0.35 → bit 1; dev 0.75 / test 0.65 → bit 0). Contaminates the severity rung that feeds the recovery controller.

**Why it is asymmetric and therefore blocking:** temperature enters the observation stream in exactly one place — thermal apparent strain, 10 µε/°C, at `scripts/utils/sensor_model.py:423-424`, applied to `gauge_obs` — and `gauge_obs` is **S-exclusive** (`scripts/utils/schema_types.py:108-111`; C0/C1 have no temperature channel at all). So **S can read the alignment bit and C1 structurally cannot.** The pre-registered bar is a paired `S − C1` macro-F1 improvement ≥0.05 absolute; this hands S a free fault-identity cue on ~half the runs, inflating the estimand **in the hypothesis's own favour**, unfalsifiably after the fact.

**Remedy I proposed and measured:** drop `fault_index` from all three rotations; index a fixed balanced cell table by `k = trajectory_index * realizations + replicate`, e.g. `((0,0,0),(0,1,1),(1,0,1),(1,1,0),(0,0,1),(0,1,0),(1,0,0),(1,1,1))`. Prototype result: every fault setting sees an **identical** context-cell set (association → exactly zero), and coverage *improves* from 4/8 per setting to the **full 8/8 in val and test**. I also asked for a validator invariant: *per split, the realized `(payload, env, contact)` cell set must be identical across every fault setting* (today `gate3_assignment.py:862-867` only checks each profile is **used**, not how profiles combine).

**Three non-blocking notes I also handed over (not conditions):** (a) `split_group_id` is unique per reservation (line 641), so `_assert_one_mapping(split_group_id → split)` in `audit_identity_manifest` is vacuous — the real whole-group guarantee is trajectory/fault exclusivity, which does hold; (b) the OOD arm rests on only **2 compound settings per split** (16 val runs / 32 test runs, 2 fault types) — thin for any OOD claim, and a limitation for my Gate-5/7 lane and the Technical Report; (c) test severities sit partly outside the fit hull (structure/actuator 0.35 is more severe than dev's `{0.5,0.75}` or val's `[0.4,0.9]`; `encoder_bias 0.015` rad is milder than anything trained) — harmless for classification, but the **severity regression head extrapolates** at test.

**One thing I asked to pre-register in MY lane (awaiting Codex's response):** every confound axis escalates monotonically dev→pilot→val→test (payload 0–0.05 → 0.025–0.075 → 0.10–0.125 → 0.15–0.20 kg; thermal ±2 → ±3 → ±5 → ±6 °C; contact 0.5 → 0.6 → 1.5 → 2.2 s) and test is the most extreme rung on all three at once. So a null at test has two causes — hypothesis failure or generalization failure — and the Claim Sheet requires separating them. **Proposed rule, to be implemented in the Gate-7 driver:** report the same paired C1-vs-S contrast at every rung (pilot, val, test); a test null counts as **hypothesis failure only if the contrast is present at the earlier rungs**; a contrast that decays with the rung is reported as **generalization-limited**, not as evidence against structural sensing. Pilot is untouched by model selection, so it is the honest method-failure gate its own `role_by_split` entry declares. **If Codex agrees next session, this is settled pre-registration; if it objects, settle it before any fit.**

## GATE STATUS — the freeze path (central reference)

**Governing decision: `BLOCK_CONFIG_FREEZE_PENDING_PRECONFIRMATORY_BUILD_AND_VALIDATION`.** Sequencing (load-bearing): a **versioned DRAFT config** governs development/validation data generation; the **final immutable `config.json` freeze comes AFTER model implementation + validation-only hyperparameter/threshold selection and BEFORE any untouched `test` payload.**

**Seven gates + ownership (Phase-1 labor split):**
1. **Machine schema + config authority** — **DONE, APPROVED S28.** *(Codex/shared.)*
2. **Role-separated storage, deployable loader, leakage/split audits** — **FOUNDATION DONE (S28) + ROLE-WRITE PATH DONE (S29).** **STILL BLOCKED OVERALL:** the real Gate-3-assigned multi-setting MuJoCo generator + its role-completeness audit are unbuilt, and now wait on an approved Gate-3 assignment. *(Codex/shared.)*
3. **Multi-setting design + manifest** — **OPEN, BLOCKED BY ME AT S30.** A complete v0.1 candidate exists (`Reproducibility Packet/config/proposed-gate3-assignment-v0.1.json` + `scripts/utils/gate3_assignment.py` + `scripts/validate_gate3_assignment.py` + `tests/test_gate3_assignment.py`, 15 tests). **Codex owns the next turn:** fix the context rotation, ideally add the cell-set invariant, recompute the assignment hash, re-hand off. **Still needs one recorded JOINT approval before any headline fit.** *(shared)*
4. **Matched learned models** — **MINE.** `TemporalAttributionNet` + `RMALatentEncoder` behind shared `[W,D]` interface; within-suite capacity ladder; ≥5 seeds; identical protocol IDs across C0/C1/S. *Toolchain verified ready (torch cu128 / sm_120).* **WAITS on the approved Gate-3 assignment + Gate-2 live layout.**
5. **Calibration/abstention/OOD/uncertainty** — **MINE.** Per-suite calibrated probs (Brier/NLL/ECE), abstention + OOD thresholds on validation, `severity_uncertainty` as a **bias-inclusive predictive error scale** (NOT in-sample residual dispersion — my S24 finding: understates true by 5.72× for S). **WAITS on validation data.**
6. **Confirmatory controller protocol** — **DECIDED S27 (both agents):** freeze the fair four-arm comparison (no-action/detection-only · transparent attribution-driven · RMA · oracle) and **RUN the pre-registered paired C1-vs-S comparison**; do NOT narrow to information-only, do NOT retune blocked families post-hoc. *(Codex owns controller; diagnosis→control seam shared.)* **No longer an open decision.**
7. **Evaluation driver + confirmatory manifest** — **MINE.** One CLI owning the `[t_c,t_c+5s]` slice, role joins, paired C1/S table, exclusions, CIs; rejects `dev-`/wrong-hash/cross-role/incomplete-pair/truncated. **Must also implement the `ood_flag` exclusion rule from known-class metrics and (if agreed) the degradation-ladder interpretation rule above.** Build once the frozen data layout exists.

**Order:** (1)✓ → (2 foundation)✓ → (2 role-write path)✓ → **(3 assignment) [Codex revises, I re-review, then JOINT approval] ← WE ARE HERE** → (2 live generator + role-completeness audit) [Codex] → (4/5 models+calibration on validation) [me] → (6 controller + sample-size) [shared] → **joint immutable freeze** → one-shot confirmatory generation + eval (7) → Phase 3. **Do NOT build models or data ahead of the approved assignment.**

Not freeze blockers (still required before completion): Slot-8 verification artifact (after confirmatory outputs); Technical Report / Accessible Piece / Study Guide Pass 2 (Phase 3); fresh-environment packet validation.

## The single most important things to do next session (Session 31)

1. **Verify live `git log` HEAD first** (Standing Lesson 5 — it has lagged three sessions running). Read Codex's newest HumanReport + the Phase-2 chat tail.
2. **If Codex has re-handed off a corrected Gate-3 assignment: re-review it the same way I found the defect** — do NOT re-read the formulas and call it fixed. **Expand all reservations and measure directly:** per split, is the realized `(payload, env, contact)` cell set identical across every fault setting? Is `payload XOR env` still constant within a setting? Can `healthy` occur in every cell? Does the alignment bit still separate severities? My probe script is described under "Scratchpad" below — recreate it. Also re-verify the new assignment hash and both file SHA-256s.
3. **If it holds: record the one JOINT pre-registration approval** (`APPROVE_GATE3_ASSIGNMENT_V0_*`) — that is what unblocks Gate 3, and nothing downstream may fit before it.
4. **Settle the degradation-ladder interpretation rule with Codex** (my proposal above) while no numbers exist.
5. **My lane opens only after that:** Gate 4 models, then Gate 5 calibration on validation only. **Do NOT build model or data ahead of the approved assignment.**
6. **Do NOT freeze a partial config.**

## Review-cycle state

- **ONE OPEN LOOP: the Gate-3 assignment**, blocked at my S30 review. **Codex owns the next turn.** I made no edits, so the tracked state is still Codex's exact handoff.
- **CLOSED, do not reopen:** Gate-2 role-write path (my S29), Gate-1/Gate-2-foundation (my S28), Config-Freeze Readiness Review (S27), actuator-action (S26), class-probability (S25).

## MONITORING DUTY (standing)

- **S30 check CLEAN** — Codex's three S29 appends to the Phase-2 chat were a verified **+61/−0** pure tail addition (2608 → 2669), Codex physically last. **Eighth consecutive clean append.** Did NOT post to `Transcript Order Monitoring` (flag only on recurrence; keep the thread lean).
- **REUSE the binary-EOF-append approach for every chat turn.** My `append_turn.py` lives in the (uncommitted) session scratchpad and **will be gone next session — recreate it** (binary EOF-append + 4 gates: marker-absent-before / prior-bytes-exact-prefix / marker-once-after-boundary / turn-physically-last, with rollback on any gate failure). **Pass an ASCII-only unique marker** (the timestamp string, e.g. `Session 30, 2026-07-24 12:45 PDT`). Verify `git diff --numstat` shows `+N/−0` after. My S30 turn recorded **+96/−0**. The transcript is normal text (not byte-hashed), so a benign "LF→CRLF" git warning on append is expected and fine.

## Codex's Gate-1/2/3 layer — reference

`Reproducibility Packet/`:
- **`schema/schema.json`** (approved S28) — machine schema v1.0 + A1. Roles: identity_manifest, plant (20 fields = `PrivilegedRecord`), observations (deployable, fixed 6-channel registry + static suite mask), labels (8), estimator_outputs (9, `N_decisions` sparse axis), controller_logs (6). Channel registry: q_obs/qd_obs/tau_cmd (C0/C1/S), current_proxy_obs/imu_obs (C1/S), gauge_obs[4] (**S only**). **`schema_sha256 = 0dae0dd0…3e942f`** (LF-pinned via root `.gitattributes`).
- **`config/draft-config-v0.1.json`** (approved S28) — the versioned DRAFT (`status=draft`, `confirmatory_payloads_allowed=false`, gates 2–7 open). Frozen candidates: plant (`n_def=90`, gauges [0.25,0.75], A1 safety thresholds, `point_count_per_link=17`, `endpoint_contact_plane_z_m=0.2`), timing (`f_ctrl=500`, `window_steps=768`, `stride=16`, probe 0.05 N / 0.8 Hz / 1 cyc raised_cosine, `analysis_window_s=5.0`), full sensor_model constants. **`config_hash = dev-0211f2e7…6180`**.
- **`scripts/utils/config_contract.py`** (S28) — strict JSON, canonical hashing, draft/frozen lifecycle; frozen wall requires name `config.json`, `APPROVE_CONFIG_FREEZE`, `open_gates==[]`, no null/empty, no `dev-`, 64-hex hash.
- **`scripts/utils/storage_contract.py`** (S28) — identity manifest + role indexes; whole-group split audit; `DeployableObservationLoader` (suite-scoped, unavailable channels all-NaN + masked, traversal guard, dtype/timing checks).
- **`scripts/utils/role_contract.py`** (S29) — manifest-bound writers/loaders for all four non-observation roles + observations; draft-`test` refusal; allowlisted `dev|pilot|val` `SupervisedTrainingJoin` yielding observation + label only.
- **`scripts/build_data_contract_fixture.py`** (S29) — deterministic synthetic role-completeness fixture (two builds byte-identical). Explicitly NOT a Gate-3 assignment or research data.
- **`scripts/utils/gate3_assignment.py` + `config/proposed-gate3-assignment-v0.1.json` + `scripts/validate_gate3_assignment.py` + `tests/test_gate3_assignment.py`** (S29) — **the artifact I blocked.** Assignment structure worth remembering: 19 known settings per split (1 healthy + 2 structure loc1 + 4 actuator loc{0,1} + 12 sensor {bias,drift,dropout}×loc{0,1}×2 severities), +2 compound/OOD in each of val/test (label = first component, `compound_flag`/`ood_flag` true, excluded from four-way metrics); 2 trajectories per split (one ordinary, one diagnostic), split-exclusive; realizations 2/2/4/8; seed bases 110000/210000/310000/410000, seeds `base + 10*ordinal + {0,1,2,3}`; no known fault tuple reused across any split pair; `dataset_identity_train_seed=0`; training-seed pool `[31001…31005]`.
- Tests: `test_data_contract.py` (18) + `test_role_contract.py` (11) + `test_gate3_assignment.py` (15). **Full packet: 373 tests green (S30 re-run).**
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
- `utils/cable_mechanics.py` + `utils/cable_plant.py` + `make_mujoco_plant_trace.py` (S14/S15): A1 safety flags = `|q|>π`, `|qd|>10`, 3-D tip radius >0.82 from `[0,0,0.5]`, `max|gauge|>500 µε`, `contact_state[0]>5 N`. **Fault severity = REMAINING fraction.** **`cable_plant.py:124-125` restricts structural faults to location `{-1,1}`** (verified S30). `agents/Codex/Config Freeze Readiness Review.md` = the seven-gate plan (I approved S27).

## The evidence tables (development-evidence boundary — why we expect diagnostic-only)

**Structural (Codex S20):** remaining EI 0.50/0.25/0.10/0.05 → mean peak |gauge| 38.4/72.4/152.8/259.7 µε (healthy 19.2) but mean **joint** tracking deficit +0.08%/−0.89%/−2.23%/−5.00% — monotone in information, monotone the WRONG way in joint control (damage moves to the TIP, which the joint score never measures).

**Control-layer shape (Codex `bounded_noisy_information_review`):** healthy/actuator/sensor → S has no exclusive info + 0% tracking change; **structure → S exclusive info YES, C1 withholds actionable, `s_tracking_change_pct` −18.58%.** C1 per-class recall: structure **0.083**, else 1.000. **Where S has exclusive info there's no control headroom; where there's headroom S has no exclusive info** = the pre-registered Slot-13 diagnostic-only landing.

## The agreed contract's load-bearing specifics

- **Sensor suites (controlled variable):** C0 = joint encoders + commanded actuation · **C1 = C0 + noisy motor-current nominal-Kt torque estimate + one distal 6-axis IMU** · **S = C1 + four fixed strain/curvature gauge stations** · O = privileged oracle. **Temperature is observable ONLY through `gauge_obs`, i.e. only in S** (`sensor_model.py:423-424`, 10 µε/°C) — this fact is what made the S30 finding blocking; keep it in mind for any future confound design.
- **Two settled correctness points:** actuator-gain fault acts *downstream* of the current proxy (C1 not handed true delivered torque); encoder fault has a *relational* signature.
- **Success bar (pre-declared, BOTH layers):** S improves held-out four-way macro-F1 over C1 by **≥0.05 absolute** (paired 95% excludes zero; every source-class recall diff lower-95% above **−0.02**) AND reduces the **5-s post-change integral of absolute tracking error by ≥10%** (`100·(J_C1−J_S)/J_C1`, paired 95% excludes zero, no safety regression) under realistic confounds. Known-class abstention = error in headline macro-F1.
- **Failure shapes:** hypothesis failure (C1+temporal adaptation matches S — clean negative) vs method failure. **Inconclusive (Slot 13):** diagnostic-only (**the shape the evidence keeps landing on**) · fault-specific/bounded · confound-fragile · excitation-dependent.
- **Pre-specification:** freeze gauge placement, model/hyperparams, thresholds, analysis window, seeds/scenarios before confirmatory generation. Leakage-free splits. ≥5 training seeds. Paired hierarchical bootstrap.

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
- **STANDING LESSON 5 — verify the live git state before trusting continuity** (S28, S29 AND S30: the startup snapshot lagged every time). For learned-model work, verify the toolchain with a real GPU op, not the flag.
- **STANDING LESSON 6 (NEW, S30) — review a design by simulating its consequences, not by verifying its internal consistency.** Codex's 15 adversarial tests, hashes, interlocks and counts were all correct; the defect was in what the correct rules *jointly implied*. I only found it by expanding all 656 reservations and asking "for each fault setting, which context cells actually occur?" **Corollary: dead arithmetic hides in small catalogs** — `2 * fault_index` reads as decorrelation and is identically zero mod 2, so any formula whose behaviour depends on a catalog size must either assert that size or be replaced by an explicit table. **Second corollary: the dangerous confound is the one that favours you** — a leak that hurt the hypothesis would have surfaced as a disappointing result and been investigated; this one would have surfaced as a win.
- **PowerShell 5.1** primary (no ternary/`??`; parens in unquoted bash break `eval` — quote or use the Grep tool); Bash tool also available (its `cd` persists between calls — check where you are). Use `git diff --numstat` to confirm `+N/−0` after every chat turn.
- **Root `.gitignore`** covers `venv/`, `tmp/`, `MUJOCO_LOG.TXT`, caches, model files `*.pt/*.pth/*.ckpt/*.onnx`, LaTeX aux, OS/IDE noise. **Root `.gitattributes`** pins `Reproducibility Packet/schema/schema.json` to LF. **Packet `.gitignore`** ignores `*.npz` (+ caches/logs); small JSON/CSV/MD artifacts intentionally tracked.
- **Software-engineering standard:** `argparse`, no hard-coded paths, one purpose, shared logic in `utils/`, docstrings, prints progress, fails loud. Licensing: code MIT, prose CC BY 4.0.

## Pointers

- Claim Sheet (in-force contract): `Claim Sheet.md` · plain-language: `Accessible Claim Sheet.md` · Study Guide Pass 1: `Study Guide/Pass 1 - Conceptual Foundation.tex`
- **Shared schema (in force, +A1):** prose `Reproducibility Packet/schema/schema-v1.0.md`; machine `schema.json`.
- **The freeze plan:** `agents/Codex/Config Freeze Readiness Review.md` (I approved same-state S27).
- **My lanes:** sensor `utils/{schema_types,sensor_model,rng,synthetic_plant}.py`; eval `utils/{metrics,stats}.py`; estimator `utils/estimator.py`; synchronous floor `scripts/analyze_synchronous_detection_floor.py`; shared seam test `tests/test_recovery_seam.py`; the three severity/probability screens + tests + `results/`.
- **Codex's lane:** `utils/{cable_mechanics,cable_plant,online_loop,recovery_control,residual_baseline,task_control}.py`; **`utils/{config_contract,storage_contract,role_contract,gate3_assignment}.py` + `scripts/{validate_data_contract,build_data_contract_fixture,validate_gate3_assignment}.py` + `tests/{test_data_contract,test_role_contract,test_gate3_assignment}.py` + `schema/schema.json` + `config/{draft-config-v0.1,proposed-gate3-assignment-v0.1}.json`**; the plant/screen scripts + tests/results.
- **Phase-2 chat:** `chats/Claude-Codex/Phase 2 Integration and Config Freeze/…- Active.md` (**2765 lines**; my S30 `BLOCK_GATE3_ASSIGNMENT_V0_1` = tail; **ONE open loop, Codex's turn**).
- **Monitoring chat:** `chats/Claude-Codex-Human/Transcript Order Monitoring/…- Active.md` (S30 check clean, no note added; flag only on recurrence).
- **CONCLUDED director chat:** `chats/Claude-Codex-Human/Better Suited Task/…- Concluded.md` + `Summary.md` — the withdrawn task-redesign directive. Read its `Summary.md` if the fairer-task idea resurfaces.
- Director requests: `director_requests.md` (root) — entry 1 (Claim Sheet review) non-blocking, awaiting director reply.
- My foundation `agents/Claude/Literature Foundation.md` · ledger `agents/Claude/references.md` (**no S20–S30 entries — reproduction/construction/measurement/review sessions, no external sources read**) · progress reports `agents/Claude/Progress Reports/` (Phase 0/1 Close, S8, S16, S24). **Next due: my S32**, or a phase transition / approved amendment.
- Live-Run README (co-maintained): root `README.md` — **Phase 2 / In Progress**, banner **2026-07-24**. **S30 added one running-log entry** (the blocked pre-registration, in plain language).
- Scratchpad (this session, NOT committed): **`append_turn.py`** (binary EOF-append + 4 gates + rollback — REUSE/recreate; pass an ASCII marker), **`probe_gate3_context.py`** (the 6-probe context-leak audit that found the blocking defect — **recreate it to verify Codex's fix**: it expands reservations, maps each to local `(payload,env,contact)` indices per split, and reports cells-per-fault, `p XOR e` constancy, per-class alignment values, healthy-impossible fraction, and the dev↔test polarity table), `turn_s30.md` (my appended turn).
