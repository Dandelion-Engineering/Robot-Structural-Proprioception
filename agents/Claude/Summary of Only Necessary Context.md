# Summary of Only Necessary Context — Claude

*Rewritten every session. Restores my working context for the next session. Excludes anything already in `Project Details/Project Details.md` and `AgentPrompt.md` (I re-read those in full at session start). Last rewritten: end of Session 31, 2026-07-24 14:10 PDT.*

## Where the project is

- **Phase 2 (Execution) is OPEN.** All Phase-1 gates in force. **Schema v1.0 + Amendment A1 in force.** Contract changes run through the **amendment protocol**.
- I am **Claude**; last session was **Session 31**; next session I run is **Session 32**.
- **`config.json` is deliberately NOT frozen** and does not exist. Do not freeze a partial config. All hashes are `dev-`; no `dev-` trace may enter confirmatory analysis.
- **The development-screening arc ended long ago.** Both recovery-action families are blocked (structural S20; actuator S25/reviewed-S26), diagnosis is characterized (S macro-F1 0.995 vs C1 0.704), and the evidence keeps landing on the pre-registered **"improves diagnosis, not control"** shape (Slot 13). The project is building the confirmatory pipeline toward a config freeze.
- **GATE 3 IS CLOSED (my S31).** Gates 1, 2-foundation, 2-role-write-path also DONE and jointly approved. **Gate 2 is still BLOCKED overall** — the real multi-setting MuJoCo generator + role-completeness audit are unbuilt. **Codex owns the next turn.**
- **THERE IS NO OPEN REVIEW LOOP.** First time in many sessions. If Codex hands off a new state (e.g. the 2→4 amendment below), a new loop opens.
- **A PROGRESS REPORT IS DUE AT MY SESSION 32 — i.e. NEXT SESSION** (regular 8-cadence: 8/16/24/32). Write it *in addition to* normal session work, at the Accessible-Piece bar, into `agents/Claude/Progress Reports/`. Read `Playbooks/research-progress-report.md` first. It covers Sessions 25–32; the arc is: screening ended → the seven-gate freeze plan → Gates 1/2 built and reviewed → Gate 3 blocked for a hypothesis-favouring leak → corrected, measured, and approved.

## What I did in S31 (one thing: re-reviewed Codex's corrected Gate-3 assignment → APPROVED it)

Codex's S30 ran after my S30 (Standing Lesson 5 again — startup snapshot said HEAD=`Codex Session 28`; live `git log` showed `fc6c028 Codex Session 30`). Codex accepted my `BLOCK_GATE3_ASSIGNMENT_V0_1`, fixed the context rotation, and re-handed off. My S31 was that re-review.

**Decision: `APPROVE_GATE3_ASSIGNMENT_V0_1`, no edits to any review-target file. Gate 3 closed at joint same-state approval.**

**The approved state's identity (Gate 3 is locked at these bytes):**
```text
assignment hash        dev-70832daabe7968d55c0bf68e713e945ed48ce167f5c54ec186559b9a660765de
assignment JSON        dcee3e6c9d52f7d36a84c06f0e3b1e5f39e89448c8b81940ca2728d9d9f98192
gate3_assignment.py    040cfe15ed6ffd70d9c5be32edfa418f4fb0ba98606e2dd7d85eb2f898897cef
test_gate3_assignment  e4749f67a98033b7d6e8223e8dad4c885b60ee96d9eac57f65910cbf270c1c9d
bound draft config     dev-0211f2e71a473fef3c30cd53fd0a269df45156a3d58e83097bac7a5638bf6180
```
The superseded S29 hash `dev-5939ff5f…0cedb` **must never be approved or embedded.**

**The fix Codex implemented:** an explicit balanced 8-cell `(payload, environment, contact)` table stored *inside* the self-hashed JSON; context selected by `(trajectory_index * realizations + replicate) % 8`; `fault_index` is not an input to anything; every split must carry exactly 2 profiles per axis; and the validator fails unless every fault setting in a split realizes the **identical context-cell count distribution** (stronger than the set-equality invariant I asked for — equal sets with unequal frequencies still leak).

**What I measured (the S30 defect is exactly gone):** per split, one distinct cell distribution; **I(fault setting ; context cell) = 0.0000000000 bits in all four splits**; `payload XOR env` locked in **0/19, 0/19, 0/21, 0/21** settings (was 19/19, 19/19, 21/21, 21/21); `healthy`-impossible fraction **0.00%** everywhere (was ~47.6%); the alignment bit no longer separates severity (every setting sees both values); cells per fault improved to **4/4/8/8**; per-axis marginals exactly balanced; compound/OOD settings share the identical distribution; 656 unique scenario IDs; 2624 seeds, zero collisions; zero known fault tuples reused across splits. Focused **18 passed**, full packet **376 passed in 9.11 s**, validator reproduces every field, no `config.json`, no `data/`.

**THE NEW CHECK I INVENTED — REUSE IT ON EVERY PRE-REGISTRATION REVIEW.** I re-derived the whole 656-row expansion straight from the JSON with my own loop, reading the table and index rule out of the document's own `expansion_rule` prose, then diffed row-for-row against `expand_reservations`: **identical, 656/656.** This proves the pre-registered *text* and the *generating code* are the same object. That property was silently FALSE in the blocked state (prose said "decorrelating rotation"; arithmetic said otherwise) and no internal-consistency test could have caught it.

### THE DECLARED LIMITATION I recorded instead of blocking (carry forward — it lands in Gate 7 and the Technical Report)

**In dev and pilot ONLY, payload is a deterministic function of trajectory** — `I(trajectory ; payload) = 1.000 bit`; **val and test measure 0.000 on all three axes.** Cause: at 2 realizations, `k = trajectory*2 + replicate` gives trajectory 0 the table's cells 0–1 (both payload 0) and trajectory 1 the cells 2–3 (both payload 1).

**It is unavoidable at 2 realizations — I proved this by brute force, don't re-litigate it.** Of all 4-cell designs over the 2×2×2 space: **0** satisfy both pairwise balance and no-trajectory-alias; 2 satisfy balance only; 6 satisfy no-alias only. Reason: pairwise balance forces a constant-parity coset (only 2 exist), while breaking the alias on all three axes forces each trajectory's cells to be bitwise complements, which flips parity. **And the alternative is worse for this experiment** — the best no-alias design aliases payload with *environment*, and environment reaches observations only through `gauge_obs`, the S-exclusive channel.

**Why it is a note not a block:** payload is far more legible in S than C1, so a payload↔trajectory shortcut learned on dev breaks at val/test and degrades S more. **It can only bias the paired S−C1 contrast AGAINST the hypothesis, never for it.** That is the same standard I applied when I blocked in S30 (the disqualifying property there was that the leak *favoured* us).

**Its real cost — carry this into Gate 7:** it makes a **null harder to attribute** (hypothesis failure vs training-split aliasing), and the null is this project's likely landing. **Plus it interacts with the ladder rule:** pilot shares dev's aliasing, val/test do not, so the pilot→val step changes *two* things at once (confound severity escalates AND aliasing disappears). **State this explicitly in the Gate-7 driver** — do not report the ladder as a clean single-variable escalation.

**The clean remedy I offered as an explicitly NON-BLOCKING amendment Codex owns:** raise `realizations_per_trajectory_fault` for dev and pilot from **2 to 4**. Measured on the existing table: each trajectory then gets its own parity coset, all three axes vary within every trajectory, and each split is a complete factorial. Cost 656 → **808** reservations (+23%), manifest rows 13,120 → 16,160. I recommended it and approve either way. **If Codex takes it, that is a new state needing a new joint approval — re-review it by measuring, same as this session.**

## GATE STATUS — the freeze path (central reference)

**Governing decision: `BLOCK_CONFIG_FREEZE_PENDING_PRECONFIRMATORY_BUILD_AND_VALIDATION`.** Sequencing (load-bearing): a **versioned DRAFT config** governs development/validation data generation; the **final immutable `config.json` freeze comes AFTER model implementation + validation-only hyperparameter/threshold selection and BEFORE any untouched `test` payload.**

**Seven gates + ownership (Phase-1 labor split):**
1. **Machine schema + config authority** — **DONE, APPROVED S28.** *(Codex/shared.)*
2. **Role-separated storage, deployable loader, leakage/split audits** — **FOUNDATION DONE (S28) + ROLE-WRITE PATH DONE (S29).** **STILL BLOCKED OVERALL:** the real Gate-3-assigned multi-setting MuJoCo generator + its role-completeness audit are unbuilt. **Now unblocked to proceed — Codex's next turn.** *(Codex/shared.)*
3. **Multi-setting design + manifest** — **CLOSED, JOINTLY APPROVED S31.** *(shared)*
4. **Matched learned models** — **MINE.** `TemporalAttributionNet` + `RMALatentEncoder` behind shared `[W,D]` interface; within-suite capacity ladder; ≥5 seeds; identical protocol IDs across C0/C1/S. *Toolchain verified ready (torch cu128 / sm_120).* **WAITS on the Gate-2 live data layout.**
5. **Calibration/abstention/OOD/uncertainty** — **MINE.** Per-suite calibrated probs (Brier/NLL/ECE), abstention + OOD thresholds on validation, `severity_uncertainty` as a **bias-inclusive predictive error scale** (NOT in-sample residual dispersion — my S24 finding: understates true by 5.72× for S). **WAITS on validation data.**
6. **Confirmatory controller protocol** — **DECIDED S27 (both agents):** freeze the fair four-arm comparison (no-action/detection-only · transparent attribution-driven · RMA · oracle) and **RUN the pre-registered paired C1-vs-S comparison**; do NOT narrow to information-only, do NOT retune blocked families post-hoc. *(Codex owns controller; diagnosis→control seam shared.)*
7. **Evaluation driver + confirmatory manifest** — **MINE.** One CLI owning the `[t_c,t_c+5s]` slice, role joins, paired C1/S table, exclusions, CIs; rejects `dev-`/wrong-hash/cross-role/incomplete-pair/truncated. **Must implement THREE pre-registered rules:** (a) the `ood_flag` exclusion from known-class metrics; (b) the **degradation-ladder rule** (agreed by both agents S30/S31): report the same paired C1-vs-S contrast at pilot, val and test; a test null is hypothesis failure **only if** the contrast is present at earlier rungs; a contrast that decays with the rung is reported as **generalization-limited**, not evidence against structural sensing; (c) the caveat that **pilot is structurally matched to dev, not to val/test**, on the aliasing axis.

**Order:** (1)✓ → (2 foundation)✓ → (2 role-write path)✓ → (3 assignment)✓ → **(2 live generator + role-completeness audit) [Codex] ← WE ARE HERE** → (4/5 models+calibration on validation) [me] → (6 controller + sample-size) [shared] → **joint immutable freeze** → one-shot confirmatory generation + eval (7) → Phase 3. **Do NOT build models against a data layout that does not exist yet.**

Not freeze blockers (still required before completion): Slot-8 verification artifact (after confirmatory outputs); Technical Report / Accessible Piece / Study Guide Pass 2 (Phase 3); fresh-environment packet validation.

## The single most important things to do next session (Session 32)

1. **Verify live `git log` HEAD first** (Standing Lesson 5 — it has now lagged FOUR sessions running). Read Codex's newest HumanReport + the Phase-2 chat tail.
2. **WRITE THE PROGRESS REPORT** — regular 8-cadence, due at my S32. Normal session work first, then the report. `Playbooks/research-progress-report.md`, Accessible-Piece bar, credible-source link for any concept the director isn't expected to know.
3. **If Codex took the 2→4 amendment:** re-review the new state by measuring — expand all reservations, recompute `I(fault;cell)`, re-derive the expansion from the JSON and diff row-for-row, re-verify hashes. Recreate the probes (described under "Scratchpad").
4. **If Codex declined:** record the alias as settled pre-registration and carry it into the Gate-7 plan.
5. **If Codex handed off the live generator + role-completeness audit:** that is a Gate-2 review — same discipline, and the key question is whether generated data actually realize the approved assignment (measure the produced manifest against the 656 reservations, don't trust the generator's own report).
6. **My lane opens once the live data layout exists:** Gate 4 models, then Gate 5 calibration on validation only.
7. **Do NOT freeze a partial config.**

## Review-cycle state

- **NO OPEN LOOP.** Gate-3 assignment closed at joint same-state approval (my S31).
- **CLOSED, do not reopen:** Gate-3 assignment (S31), Gate-2 role-write path (S29), Gate-1/Gate-2-foundation (S28), Config-Freeze Readiness Review (S27), actuator-action (S26), class-probability (S25).

## MONITORING DUTY (standing)

- **S31 check CLEAN** — Codex's S30 append was a verified **+90/−0** pure tail addition (2765 → 2855), hunk anchored at 2763, exactly one S30 header at line 2769, Codex physically last. **Ninth consecutive clean append.** Did NOT post to `Transcript Order Monitoring` (flag only on recurrence; keep the thread lean).
- **REUSE the binary-EOF-append approach for every chat turn.** My `append_turn.py` lives in the (uncommitted) session scratchpad and **will be gone next session — recreate it** (binary EOF-append + 4 gates: marker-absent-before / prior-bytes-exact-prefix / marker-once-after-boundary / turn-physically-last, with rollback on any gate failure). **Pass an ASCII-only unique marker** (the timestamp string, e.g. `Session 31, 2026-07-24 13:58 PDT`). Verify `git diff --numstat` shows `+N/−0` after. My S31 turn recorded **+93/−0**. The transcript is normal text (not byte-hashed), so a benign "LF→CRLF" git warning on append is expected and fine.

## Codex's Gate-1/2/3 layer — reference

`Reproducibility Packet/`:
- **`schema/schema.json`** (approved S28) — machine schema v1.0 + A1. Roles: identity_manifest, plant (20 fields = `PrivilegedRecord`), observations (deployable, fixed 6-channel registry + static suite mask), labels (8), estimator_outputs (9, `N_decisions` sparse axis), controller_logs (6). Channel registry: q_obs/qd_obs/tau_cmd (C0/C1/S), current_proxy_obs/imu_obs (C1/S), gauge_obs[4] (**S only**). **`schema_sha256 = 0dae0dd0…3e942f`** (LF-pinned via root `.gitattributes`).
- **`config/draft-config-v0.1.json`** (approved S28) — the versioned DRAFT (`status=draft`, `confirmatory_payloads_allowed=false`, gates 2–7 open). Frozen candidates: plant (`n_def=90`, gauges [0.25,0.75], A1 safety thresholds, `point_count_per_link=17`, `endpoint_contact_plane_z_m=0.2`), timing (`f_ctrl=500`, `window_steps=768`, `stride=16`, probe 0.05 N / 0.8 Hz / 1 cyc raised_cosine, `analysis_window_s=5.0`), full sensor_model constants. **`config_hash = dev-0211f2e7…6180`**. **Codex embeds the approved Gate-3 assignment into this next and recomputes the hash — expect a NEW draft-config hash after its next session.**
- **`scripts/utils/config_contract.py`** (S28) — strict JSON, canonical hashing, draft/frozen lifecycle; frozen wall requires name `config.json`, `APPROVE_CONFIG_FREEZE`, `open_gates==[]`, no null/empty, no `dev-`, 64-hex hash.
- **`scripts/utils/storage_contract.py`** (S28) — identity manifest + role indexes; whole-group split audit; `DeployableObservationLoader` (suite-scoped, unavailable channels all-NaN + masked, traversal guard, dtype/timing checks).
- **`scripts/utils/role_contract.py`** (S29) — manifest-bound writers/loaders for all four non-observation roles + observations; draft-`test` refusal; allowlisted `dev|pilot|val` `SupervisedTrainingJoin` yielding observation + label only.
- **`scripts/build_data_contract_fixture.py`** (S29) — deterministic synthetic role-completeness fixture (two builds byte-identical). Explicitly NOT a Gate-3 assignment or research data.
- **`scripts/utils/gate3_assignment.py` + `config/proposed-gate3-assignment-v0.1.json` + `scripts/validate_gate3_assignment.py` + `tests/test_gate3_assignment.py`** (S29, corrected S30, **approved S31**, 18 tests). **Assignment structure worth remembering:** 19 known settings per split (1 healthy + 2 structure loc1 + 4 actuator loc{0,1} + 12 sensor {bias,drift,dropout}×loc{0,1}×2 severities), +2 compound/OOD in each of val/test (label = first component, `compound_flag`/`ood_flag` true, excluded from four-way metrics); 2 trajectories per split (one ordinary, one diagnostic), split-exclusive; realizations 2/2/4/8; seed bases 110000/210000/310000/410000, seeds `base + 10*ordinal + {0,1,2,3}`; no known fault tuple reused across any split pair; `dataset_identity_train_seed=0`; training-seed pool `[31001…31005]`; reservations **76/76/168/336 = 656**; projection **13,120** manifest rows.
- **Validator CLI flags are `--assignment` / `--schema` / `--config`** (NOT `--draft-config` — I got this wrong once; it failed loudly, which is the standard working).
- Tests: `test_data_contract.py` (18) + `test_role_contract.py` (11) + `test_gate3_assignment.py` (18). **Full packet: 376 tests green (S31 re-run).**
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

- **Sensor suites (controlled variable):** C0 = joint encoders + commanded actuation · **C1 = C0 + noisy motor-current nominal-Kt torque estimate + one distal 6-axis IMU** · **S = C1 + four fixed strain/curvature gauge stations** · O = privileged oracle. **Temperature is observable ONLY through `gauge_obs`, i.e. only in S** (`sensor_model.py:423-424`, 10 µε/°C) — this fact made the S30 finding blocking and shaped the S31 trade-off analysis; keep it in mind for any future confound design.
- **Two settled correctness points:** actuator-gain fault acts *downstream* of the current proxy (C1 not handed true delivered torque); encoder fault has a *relational* signature.
- **Success bar (pre-declared, BOTH layers):** S improves held-out four-way macro-F1 over C1 by **≥0.05 absolute** (paired 95% excludes zero; every source-class recall diff lower-95% above **−0.02**) AND reduces the **5-s post-change integral of absolute tracking error by ≥10%** (`100·(J_C1−J_S)/J_C1`, paired 95% excludes zero, no safety regression) under realistic confounds. Known-class abstention = error in headline macro-F1.
- **Failure shapes:** hypothesis failure (C1+temporal adaptation matches S — clean negative) vs method failure. **Inconclusive (Slot 13):** diagnostic-only (**the shape the evidence keeps landing on**) · fault-specific/bounded · confound-fragile · excitation-dependent.
- **Pre-specification:** freeze gauge placement, model/hyperparams, thresholds, analysis window, seeds/scenarios before confirmatory generation. Leakage-free splits. ≥5 training seeds. Paired hierarchical bootstrap.

## Carried limitations for the Technical Report / Gate 7 (all pre-registered, none blocking)

1. **dev/pilot payload↔trajectory alias** (S31, above) — unavoidable at 2 realizations, conservative in direction, complicates null attribution, and breaks the pilot↔val comparability of the ladder.
2. **The OOD arm rests on only 2 compound settings per split** (16 val runs / 32 test runs, 2 fault types) — thin for any OOD claim.
3. **Test severities sit partly outside the fit hull** (structure/actuator 0.35 more severe than dev's `{0.5,0.75}` or val's `[0.4,0.9]`; `encoder_bias 0.015` rad milder than anything trained) — harmless for classification, but the **severity regression head extrapolates** at test.
4. **`split_group_id` is unique per reservation**, so `_assert_one_mapping(split_group_id → split)` in `audit_identity_manifest` is vacuous — the real whole-group guarantee is trajectory/fault exclusivity, which does hold.

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
- **STANDING LESSON 5 — verify the live git state before trusting continuity** (S28, S29, S30 AND S31: the startup snapshot lagged every time). For learned-model work, verify the toolchain with a real GPU op, not the flag.
- **STANDING LESSON 6 (S30) — review a design by simulating its consequences, not by verifying its internal consistency.** **Corollary: dead arithmetic hides in small catalogs** — any formula whose behaviour depends on a catalog size must either assert that size or be replaced by an explicit table. **Second corollary: the dangerous confound is the one that favours you** — a leak that hurt the hypothesis would surface as a disappointing result and get investigated; one that helps surfaces as a win.
- **STANDING LESSON 7 (NEW, S31) — for any pre-registration, check that the pre-registered TEXT generates the pre-registered DATA.** Re-derive the artifact independently from the document's own prose rule and diff row-for-row against the code that will actually run. Internal-consistency tests verify code against itself and cannot see prose/code divergence. **Corollary: apply ONE consistent blocking standard, and make it direction-of-bias.** I blocked in S30 because the flaw favoured the hypothesis; I approved in S31 despite a real flaw because it is conservative. **Second corollary: check that a flaw is AVOIDABLE before reporting it as one** — the brute-force search turned "you should have avoided this" into "this is a forced trade-off and you took the right side", which cost five minutes and was both more accurate and more useful.
- **PowerShell 5.1** primary (no ternary/`??`; parens in unquoted bash break `eval` — quote or use the Grep tool); Bash tool also available (its `cd` persists between calls — check where you are). Use `git diff --numstat` to confirm `+N/−0` after every chat turn.
- **Root `.gitignore`** covers `venv/`, `tmp/`, `MUJOCO_LOG.TXT`, caches, model files `*.pt/*.pth/*.ckpt/*.onnx`, LaTeX aux, OS/IDE noise. **Root `.gitattributes`** pins `Reproducibility Packet/schema/schema.json` to LF. **Packet `.gitignore`** ignores `*.npz` (+ caches/logs); small JSON/CSV/MD artifacts intentionally tracked. **When Codex generates real research data, check whether the packet `.gitignore` needs new rules before committing.**
- **Software-engineering standard:** `argparse`, no hard-coded paths, one purpose, shared logic in `utils/`, docstrings, prints progress, fails loud. Licensing: code MIT, prose CC BY 4.0.

## Pointers

- Claim Sheet (in-force contract): `Claim Sheet.md` · plain-language: `Accessible Claim Sheet.md` · Study Guide Pass 1: `Study Guide/Pass 1 - Conceptual Foundation.tex`
- **Shared schema (in force, +A1):** prose `Reproducibility Packet/schema/schema-v1.0.md`; machine `schema.json`.
- **The freeze plan:** `agents/Codex/Config Freeze Readiness Review.md` (I approved same-state S27).
- **My lanes:** sensor `utils/{schema_types,sensor_model,rng,synthetic_plant}.py`; eval `utils/{metrics,stats}.py`; estimator `utils/estimator.py`; synchronous floor `scripts/analyze_synchronous_detection_floor.py`; shared seam test `tests/test_recovery_seam.py`; the three severity/probability screens + tests + `results/`.
- **Codex's lane:** `utils/{cable_mechanics,cable_plant,online_loop,recovery_control,residual_baseline,task_control}.py`; **`utils/{config_contract,storage_contract,role_contract,gate3_assignment}.py` + `scripts/{validate_data_contract,build_data_contract_fixture,validate_gate3_assignment}.py` + `tests/{test_data_contract,test_role_contract,test_gate3_assignment}.py` + `schema/schema.json` + `config/{draft-config-v0.1,proposed-gate3-assignment-v0.1}.json`**; the plant/screen scripts + tests/results.
- **Phase-2 chat:** `chats/Claude-Codex/Phase 2 Integration and Config Freeze/…- Active.md` (**2948 lines**; my S31 `APPROVE_GATE3_ASSIGNMENT_V0_1` = tail; **NO open loop**).
- **Monitoring chat:** `chats/Claude-Codex-Human/Transcript Order Monitoring/…- Active.md` (S31 check clean, no note added; flag only on recurrence).
- **CONCLUDED director chat:** `chats/Claude-Codex-Human/Better Suited Task/…- Concluded.md` + `Summary.md` — the withdrawn task-redesign directive. Read its `Summary.md` if the fairer-task idea resurfaces.
- Director requests: `director_requests.md` (root) — entry 1 (Claim Sheet review) non-blocking, awaiting director reply.
- My foundation `agents/Claude/Literature Foundation.md` · ledger `agents/Claude/references.md` (**no S20–S31 entries — reproduction/construction/measurement/review sessions, no external sources read**) · progress reports `agents/Claude/Progress Reports/` (Phase 0/1 Close, S8, S16, S24). **NEXT DUE: my S32 — i.e. NEXT SESSION.**
- Live-Run README (co-maintained): root `README.md` — **Phase 2 / In Progress**, banner **2026-07-24**. **S31 added one running-log entry** (the corrected blueprint approved; leak exactly zero; conservative limitation declared; generation authorized for dev/pilot/val only).
- Scratchpad (this session, NOT committed): **`append_turn.py`** (binary EOF-append + 4 gates + rollback — REUSE/recreate; pass an ASCII marker), **`probe_gate3_context_v2.py`** (the 5-part audit: independent canonical-hash recomputation, independent row-for-row re-derivation from the JSON, the three S30 leak signatures, `I(fault;cell)`, trajectory/replicate coupling, compound-OOD distribution match, seed hygiene — **recreate it to review any new assignment state**), **`probe_alias_tradeoff.py`** (the brute-force proof that pairwise balance and no-trajectory-alias are mutually exclusive at 2 realizations, plus the 4-realization resolution), `turn_s31.md` (my appended turn).
