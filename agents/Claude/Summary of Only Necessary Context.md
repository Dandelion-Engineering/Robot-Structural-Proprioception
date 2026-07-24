# Summary of Only Necessary Context — Claude

*Rewritten every session. Restores my working context for the next session. Excludes anything already in `Project Details/Project Details.md` and `AgentPrompt.md` (I re-read those in full at session start). Last rewritten: end of Session 28, 2026-07-23 20:00 PDT.*

## Where the project is

- **Phase 2 (Execution) is OPEN.** All Phase-1 gates in force. **Schema v1.0 + Amendment A1 in force.** Contract changes run through the **amendment protocol**.
- I am **Claude**; last session was **Session 28**; next session I run is **Session 29**.
- **`config.json` is deliberately NOT frozen** and does not exist. Do not freeze a partial config. All hashes are `dev-`; no `dev-` trace may enter confirmatory analysis.
- **The development-screening arc has ended.** Both recovery-action families are blocked (structural S20; actuator S25/reviewed-S26), diagnosis is characterized (S macro-F1 0.995 vs C1 0.704), and the evidence keeps landing on the pre-registered **"improves diagnosis, not control"** shape (Slot 13). The project **pivoted from screening variants to building the confirmatory pipeline** toward a config freeze.
- **The first confirmatory-pipeline component now exists and is JOINTLY APPROVED** (Codex built it in its S27; I reviewed + approved it in my S28 — see "GATE STATUS" below). This is Gate 1 + the Gate-2 *foundation*. **Gate 2 is still BLOCKED overall** (live builder + supervised join + role writers + generator unbuilt).
- **No regular progress report due until my Session 32** — unless a phase transition or an approved Claim-Sheet amendment triggers one sooner. Neither is pending.

## What I did in S28 (one thing: the Gate-1/Gate-2-foundation review → APPROVED)

Codex's S27 ran **after** my S27 (Standing Lesson 5 caught this: startup snapshot was stale; live `git log` HEAD = `Codex Session 27`). Codex built the first persistence-foundation increment and handed me the exact state for genuine review. My S28 was that review.

**Genuine review of Codex's Gate-1/Gate-2-foundation → `APPROVE_GATE1_GATE2_FOUNDATION`, exact state, no edits. Loop CLOSED.** Review target: `schema/schema.json`, `config/draft-config-v0.1.json`, `scripts/utils/config_contract.py`, `scripts/utils/storage_contract.py`, `scripts/validate_data_contract.py`, `tests/test_data_contract.py`, packet `README.md`/`utils/__init__.py` doc updates, **plus** root `.gitattributes` LF rule. What I did beyond reading:
- **Independently recomputed BOTH hashes with my own canonicalization** (`json.dumps(sort_keys=True, separators=(",",":"), ensure_ascii=False, allow_nan=False)` minus top-level `config_hash`, sha256, `dev-` prefix — NOT Codex's functions): `schema_sha256 = 0dae0dd0…942f`, `config_hash = dev-0211f2e7…6180`. Exact match to artifact + report. So the canonicalization is exactly the schema's declared rule and the recorded hashes are honest.
- **Verified the LF hash-guard is effective:** `schema.json` is 15,212 bytes, **no CRLF on disk**; `git check-attr` resolves `eol: lf` on the REAL path (the `?` in `.gitattributes` is a literal glob wildcard byte `0x3F` matching the space — verified, not a corrupted separator). This matters: the config binds to schema bytes via `schema_sha256`.
- **Ran validator** (`Config OK: status=draft, confirmatory=False`) and **full suite (347 passed).**
- **Ran 5 of my own adversarial probes beyond Codex's tests — all pass:** (1) real draft re-flagged frozen w/ nulls → refused; (2) **no forgery by prefix-strip** (frozen digest ≠ draft digest with `dev-` stripped, because `status` is inside the canonical payload); (3) complete frozen validates as `config.json` only; (4) real-sensor-field tamper breaks hash; (5) wrong `schema_sha256` refused.
- **Confirmed honest boundary:** no `config.json`, no committed `.npz`, packet README states Gate 2 incomplete.
- Posted my review turn to the Phase-2 chat: **verified pure append +33/−0**, I'm physically last.
- **Two non-blocking forward notes** (recorded, not conditions): (a) `.gitattributes` `?`-wildcard works; a double-quoted pattern would be marginally tighter *if that file is ever touched*; (b) the Gate-3 draft manifest, when it lands, needs one recorded **joint** pre-registration approval of the whole-trajectory/whole-fault-setting → split assignment before any headline fit.
- **Monitoring duty CLEAN** (Codex's S27 = +58/−0 tail append, physically last; **sixth consecutive clean append**; no note added — flag only on recurrence).
- **Added ONE lean Live-Run README entry** (root `README.md`): the screening→confirmatory-build pivot + approved first component, honesty bound intact ("scaffolding, not a result — config unfrozen"). Banner already current (Phase 2 / In Progress / 2026-07-23).

## GATE STATUS — the freeze path (central reference)

**Governing decision: `BLOCK_CONFIG_FREEZE_PENDING_PRECONFIRMATORY_BUILD_AND_VALIDATION`.** Sequencing (load-bearing): a **versioned DRAFT config** governs development/validation data generation; the **final immutable `config.json` freeze comes AFTER model implementation + validation-only hyperparameter/threshold selection and BEFORE any untouched `test` payload.**

**Seven gates + ownership (Phase-1 labor split):**
1. **Machine schema + config authority** — **DONE, APPROVED S28.** `schema.json`, draft/frozen `config.json` contract, canonical hashing + loader refusing `dev-`/draft/mismatched as confirmatory. *(Codex/shared.)*
2. **Role-separated storage, deployable loader, leakage/split audits** — **FOUNDATION DONE, APPROVED S28** (identity manifest + role indexes; C0/C1/S deployable loader; whole-group split/CRN/leakage/path/hash/mask/dtype/timing audits). **STILL BLOCKED OVERALL:** live multi-setting manifest/data builder, allowlisted supervised training join, non-observation role writers/evaluators, end-to-end generator **unbuilt.** *(Codex/shared — Codex's next increment.)*
3. **Multi-setting design + manifest** — **NEXT, SHARED, NOT STARTED.** Known-class location/severity grids, ≥1 compound/OOD held-out setting, trajectory/payload/contact/onset/excitation distributions, deterministic `dev|pilot|val|test` by WHOLE trajectory AND WHOLE fault setting. **Needs one recorded JOINT approval before any headline fit** (agreed S27; my S28 forward note reaffirms).
4. **Matched learned models** — **MINE.** `TemporalAttributionNet` + `RMALatentEncoder` behind shared `[W,D]` interface; within-suite capacity ladder; ≥5 seeds; identical protocol IDs across C0/C1/S. *Toolchain verified ready (torch cu128 / sm_120).* **WAITS on Gate-2 live layout + Gate-3 manifest.**
5. **Calibration/abstention/OOD/uncertainty** — **MINE.** Per-suite calibrated probs (Brier/NLL/ECE), abstention + OOD thresholds on validation, `severity_uncertainty` defined as a **bias-inclusive predictive error scale** (NOT in-sample residual dispersion — my S24 finding: understates true by 5.72× for S). **WAITS on validation data.**
6. **Confirmatory controller protocol** — **DECIDED S27 (both agents):** freeze the fair four-arm comparison (no-action/detection-only · transparent attribution-driven · RMA · oracle) and **RUN the pre-registered paired C1-vs-S comparison**; do NOT narrow to information-only (would need amendment) and do NOT retune blocked families post-hoc. Likely returns ~no control gain = the pre-registered Slot-13 diagnostic-only landing. *(Codex owns controller; diagnosis→control seam shared.)* **No longer an open decision.**
7. **Evaluation driver + confirmatory manifest** — **MINE.** One CLI owning the `[t_c,t_c+5s]` slice, role joins, paired C1/S table, exclusions, CIs; rejects `dev-`/wrong-hash/cross-role/incomplete-pair/truncated. **Build once frozen data layout exists.**

**Order:** (1)✓ → (2 foundation)✓ → **(2 live builder) [Codex, NEXT]** → **(3 manifest) [shared, needs joint approval]** → (4/5 models+calibration on validation) [me] → (6 controller + sample-size) [shared] → **joint immutable freeze** → one-shot confirmatory generation + eval (7) → Phase 3. **My Gate-4/5/7 work is BLOCKED on Codex's Gate-2 live layout + the Gate-3 manifest** (pre-registration integrity: splits assigned + jointly approved before any headline fit). **Do NOT build models/data ahead of the approved manifest.**

Not freeze blockers (still required before completion): Slot-8 verification artifact (after confirmatory outputs); Technical Report / Accessible Piece / Study Guide Pass 2 (Phase 3); fresh-environment packet validation.

## The single most important things to do next session (Session 29)

1. **Read Codex's latest first** (its next HumanReport + Phase-2 chat tail + continuity). Codex's stated next increment is **Gate 2's live manifest/data builder + allowlisted supervised join**, then the **Gate-3 assignment manifest**. If landed, **review it genuinely** (cross-review; reproduce, don't just read).
2. **If the Gate-3 draft manifest exists: converge with Codex and record the one JOINT pre-registration approval** of the whole-trajectory/whole-fault-setting → `dev|pilot|val|test` assignment **before** anything downstream fits.
3. **My lane, once Codex's Gate-2 live layout + the Gate-3 manifest exist:** build `TemporalAttributionNet` + `RMALatentEncoder` behind the shared `[W,D]` interface (toolchain ready), then Gate-5 calibration/abstention/OOD/uncertainty on validation only (incl. the bias-inclusive `severity_uncertainty` definition). **Do NOT build model/data ahead of the jointly-approved manifest.**
4. **Do NOT freeze a partial config.**

## Review-cycle state (all loops CLOSED)

- **NO open review loops.** The Gate-1/Gate-2-foundation loop closed at my S28 same-state approval; Codex will acknowledge next session (ack is courtesy — both-approve-same-state already closed it). Config-Freeze Readiness Review closed (my S27). Actuator-action loop closed (S26). Class-probability loop closed (S25). Do not reopen any.

## MONITORING DUTY (standing)

- **S27 check CLEAN** — Codex's S27 append to the Phase-2 chat was a verified **+58/−0** tail addition, Codex physically last (`git show --numstat 2eb7b1a`). **Sixth consecutive clean append.** Did NOT post to `Transcript Order Monitoring` (flag only on recurrence; keep the thread lean).
- **REUSE the binary-EOF-append approach for every chat turn.** My `append_turn.py` lives in the (uncommitted) session scratchpad and **will be gone next session — recreate it** (binary EOF-append + gates: marker-absent-before / prefix-byte-identical / marker-once-after-old-boundary / turn-last). **Pass an ASCII-only unique marker** (the timestamp string, e.g. `Session 28, 2026-07-23 19:55 PDT`). Verify `git diff --numstat` shows `+N/−0` after. The transcript is normal text (not byte-hashed), so a benign "LF→CRLF" git warning on append is expected and fine.

## Toolchain state (Gate-4 precondition DONE)

- **`torch==2.11.0+cu128` installed in `venv` and VERIFIED on the RTX 5060 Ti (Blackwell/sm_120):** kernels + autograd execute, GPU==CPU at 0.000e+00. Pinned in root `requirements.txt` behind the cu128 `--extra-index-url`. Gate 4's toolchain unknown is a verified YES. `torch` lives in `venv/` (gitignored); `.gitignore` covers `*.pt/*.pth/*.ckpt/*.onnx`.

## Codex's NEW persistence foundation (built S27, approved my S28) — reference

`Reproducibility Packet/`:
- **`schema/schema.json`** — machine rendering of schema v1.0 + A1. Roles: identity_manifest, plant, observations (deployable), labels, estimator_outputs (`N_decisions` sparse axis), controller_logs. Channel registry: q_obs/qd_obs/tau_cmd (C0/C1/S), current_proxy_obs/imu_obs (C1/S), gauge_obs[4] (S only). A1 field orders exact. `config_contract` block declares canonicalization + freeze rules. **`schema_sha256 = 0dae0dd0fec4269180139efc9a4c9ce38e7f8f23d890d182dc8eb063803e942f`** (LF-pinned via root `.gitattributes`). `severity_uncertainty` left as `config_defined_nonnegative_error_scale` (Gate 5 = mine, still owns the statistic).
- **`config/draft-config-v0.1.json`** — the versioned DRAFT (`status=draft`, `confirmatory_payloads_allowed=false`, gates 2–7 open, `scenario_manifest`/`models`/`calibration`/`evaluation` = null, `controllers.governance="run_pre_registered_control_comparison_no_scope_narrowing"`). Carries frozen candidates: plant (`n_def=90`, gauges [0.25,0.75], A1 safety thresholds, `point_count_per_link=17`, `endpoint_contact_plane_z_m=0.2`), timing (`f_ctrl=500`, `window_steps=768`, `stride=16`, probe 0.05N/0.8Hz/1cyc raised_cosine, `analysis_window_s=5.0`), full sensor_model constants. **`config_hash = dev-0211f2e71a473fef3c30cd53fd0a269df45156a3d58e83097bac7a5638bf6180`**.
- **`scripts/utils/config_contract.py`** — strict JSON (rejects NaN/Inf/dup keys), canonical hashing, draft/frozen lifecycle (`ValidatedConfig`, `load_config`, `expected_config_hash`). Frozen wall requires: name `config.json`, `APPROVE_CONFIG_FREEZE`, `open_gates==[]`, no null/empty in `values.*`, no `dev-` prefix anywhere, 64-hex hash, `require_frozen` refuses draft.
- **`scripts/utils/storage_contract.py`** — `IdentityManifestRow`/`RoleIndexRow`; `audit_identity_manifest` (one config_hash; whole-group split via `_assert_one_mapping` on pair/trajectory/fault_setting/split_group; within-pair CRN seed+protocol sharing; unique run_id); `DeployableObservationLoader` (constructor takes ONLY `observations/<suite>`; exact index header + NPZ key allowlist; `is_relative_to` traversal guard; unavailable channels must be all-NaN + masked; dtype/timing checks).
- **`scripts/validate_data_contract.py`** — CLI (`--schema --config [--manifest --suite-root --suite --require-frozen]`). Run from packet: `..\venv\Scripts\python.exe scripts\validate_data_contract.py --schema schema\schema.json --config config\draft-config-v0.1.json`.
- **`tests/test_data_contract.py`** — 18 adversarial tests (schema-faithfulness pinned to my Python types; key-order-independent + tamper-evident hashing; filename camouflage; partial/unapproved/dev-marked frozen; whole-group split ×4; within-pair CRN; 5 loader leakage/traversal/dtype attacks).
- Packet **`README.md`** + `utils/__init__.py` document the validator + the honest Gate-2/3 boundary. (Packet runbook uses its OWN `.\.venv\Scripts\python.exe` convention — don't "fix" to project-root `venv`.)

## My lanes — current state (unchanged this session)

`Reproducibility Packet/scripts/utils/estimator.py`:
- **`WindowFeatureExtractor(window_steps=W=768, probe_frequency_hz=0.8)`**: `[W,D]` left-padded + per-column `[last,mean,std,slope,sync_cos,sync_sin,sync_amplitude,valid_fraction]` over 18-col registry → 144 features. Constants: `N_FEATURE_STATS=4`, `N_EXTRA_FEATURES=4`, sync cols 4/5/6, `VALID_FRACTION_COL=7`, `DIAGNOSTIC_PROBE_HZ=0.8`, `MIN_SYNC_SAMPLES=8`.
- **`WindowNoveltyDetector`** (detect+abstain) · **`CoefficientReferenceDetector`** (2nd interpretable rung; canonical `synchronous_coefficient_vector`+`coefficient_reference_distance`; `fit_reference` atomic; `calibrate_threshold` fail-loud below `ceil(min_tail/far)`) · **`_SCORE_STD_FLOOR=1e-3`** shared · **`SeverityRidgeHead`** (deployable severity read-out; suite-agnostic; `train_residual_std` is IN-SAMPLE — never feed a confidence gate) · **`leave_one_group_out_residuals`** (CALIBRATION-role diagnostic; group by sensor seed) · **`OracleInterface(onset_time_s)`** (causal privileged ceiling) · **`EstimatorCommandPolicy`** (seam adapter; runs estimator every `stride`, ZOHs OUTPUT) · `RECOMMENDED_WINDOW=(768,16)` pilot proposal · **learned rungs specified-not-built (Gate 4 — MINE; toolchain ready; waits on Gate-3 manifest).**
- **`utils/metrics.py` + `utils/stats.py`** (jointly approved through S11): `tracking_reduction_pct(j_baseline,j_treatment)=100·(j_baseline−j_treatment)/j_baseline`, `j_5s` fail-loud on full `[t_c,t_c+5s]`, `safety_incident_rate`, `safety_regression_delta` (matched `[T,7]` guard), `hierarchical_bootstrap_ci` (crossed pair×seed). **Eval driver (Gate 7) — build once frozen data layout exists.**
- **Screens (all jointly approved/closed):** `screen_severity_estimation_quality.py` (80 arms; held-out MAE C1 0.0065/S 0.0076; its `arm_rows.csv` at seeds 17100–17103 = the Step-15 CRN source), `screen_severity_action_boundary.py` (40 arms; paired −0.1177% mean), `screen_actuator_probability_channel.py` (36 arms; 5.07 pp graded / 10.85 pp gate-crossing). `tests/test_recovery_seam.py` (shared mechanism regression, 4 tests).

## Codex's OTHER lanes — current state

- `screen_actuator_recovery_action.py` (S25; I approved S26). Selected `actuator_gain_remaining_0p25`; safe cap-3 → 8.25 pp source-specific margin [8.09,8.53] < 10-pp bar → `BLOCK_ACTUATOR_ACTION_FAMILY_AT_SOURCE_SPECIFIC_GATE`. cap-5 crosses bar (10.18 pp) but fails A1 lifecycle safety (19 incident arms). At safe cap-3, oracle/C1/S command identically → NOT a C1-vs-S control result.
- `utils/recovery_control.py` — `GainScheduledRecoveryController`. Actuator: `multiplier=1+p·(capped_compensation−1)`, `capped=min(1/max(remaining,floor),cap)`. Gate `_confident_source`=not-abstained AND unique-argmax==source AND p≥0.5 AND finite σ≤0.25. `maximum_gain_compensation=2.0`, `minimum_gain_remaining=0.25`, `torque_abs_limit=(1.0,0.5)`.
- `screen_fault_tracking_deficit.py` (S22): gate `required_reduction_pct`=12%, `required_deficit_pct`=13.636%; selection `actuator_gain_remaining_0p25`; structural rows produced NO joint deficit.
- `screen_structural_recovery_action.py` (S20): `BLOCK_STRUCTURAL_RECOVERY_ACTION_FAMILY`; ~70% of benefit at the *unfaulted* joint.
- `run_bounded_noisy_information_review.py` (S19): S PASSES info+action gates (macro-F1 0.995, 100% per-fault detection, 2.1% FA); C1 BLOCKS (0.704, 8.3% structural recall). One-hot mechanism probs (NOT calibrated).
- `utils/task_control.py` (S17/S18): `BoundedTaskProfile` (rest→(0.30,0.30) rad by 3.0s→hold→rest by 5.0s — JOINT-SPACE targets), `ObservedJointPDController` (kp (0.05,0.03), kd (0.005,0.003), torque limits (0.20,0.10); reads ONLY `q_obs`/`qd_obs`).
- `screen_bounded_task_contact.py`, `utils/cable_mechanics.py` + `utils/cable_plant.py` + `make_mujoco_plant_trace.py` (S14/S15): A1 safety flags = `|q|>π`, `|qd|>10`, 3-D tip radius >0.82 from `[0,0,0.5]`, `max|gauge|>500 µε`, `contact_state[0]>5 N`. **Fault severity = REMAINING fraction.** `agents/Codex/Config Freeze Readiness Review.md` = the seven-gate plan (I approved S27).

## The evidence tables (development-evidence boundary — why we expect diagnostic-only)

**Structural (Codex S20):** remaining EI 0.50/0.25/0.10/0.05 → mean peak |gauge| 38.4/72.4/152.8/259.7 µε (healthy 19.2) but mean **joint** tracking deficit +0.08%/−0.89%/−2.23%/−5.00% — monotone in information, monotone the WRONG way in joint control (damage moves to the TIP, which the joint score never measures).

**Control-layer shape (Codex `bounded_noisy_information_review`):** healthy/actuator/sensor → S has no exclusive info + 0% tracking change; **structure → S exclusive info YES, C1 withholds actionable, `s_tracking_change_pct` −18.58%** (S "correct" action makes joint tracking WORSE). C1 per-class recall: structure **0.083**, else 1.000. **Where S has exclusive info there's no control headroom; where there's headroom S has no exclusive info** = the pre-registered Slot-13 diagnostic-only landing.

## The agreed contract's load-bearing specifics

- **Sensor suites (controlled variable):** C0 = joint encoders + commanded actuation · **C1 = C0 + noisy motor-current nominal-Kt torque estimate + one distal 6-axis IMU** · **S = C1 + four fixed strain/curvature gauge stations** · O = privileged oracle.
- **Two settled correctness points:** actuator-gain fault acts *downstream* of the current proxy (C1 not handed true delivered torque); encoder fault has a *relational* signature.
- **Success bar (pre-declared, BOTH layers):** S improves held-out four-way macro-F1 over C1 by **≥0.05 absolute** (paired 95% excludes zero; every source-class recall diff lower-95% above **−0.02**) AND reduces the **5-s post-change integral of absolute tracking error by ≥10%** (`100·(J_C1−J_S)/J_C1`, paired 95% excludes zero, no safety regression) under realistic confounds. Known-class abstention = error in headline macro-F1.
- **Failure shapes:** hypothesis failure (C1+temporal adaptation matches S — clean negative) vs method failure. **Inconclusive (Slot 13):** diagnostic-only (attribution improves, control doesn't — **the shape the evidence keeps landing on**) · fault-specific/bounded · confound-fragile · excitation-dependent.
- **Pre-specification:** freeze gauge placement, model/hyperparams, thresholds, analysis window, seeds/scenarios before confirmatory generation. Leakage-free splits. ≥5 training seeds. Paired hierarchical bootstrap.

## Coherence / honesty bounds (keep loud)

- `utils/synchronous.py` (Codex S9) = the single shared harmonic statistic; `synchronous_coefficient_vector`+`coefficient_reference_distance` in `estimator.py` = the one canonical definition every pilot/screen/review imports.
- **Sensor RNG keyed on `(sensor_seed, pair_id, channel, stream)`** — `pair_id` load-bearing; screens reuse an upstream screen's `pair_id` verbatim and check CRN at 0.000e+00. (The new `storage_contract` enforces the same CRN idea at the manifest level: within-pair seed/protocol equality.)
- Deployable floors are *detection*, not learned attribution; all rates from ONE fixed fault setting per class, held out over sensor noise only; abstention untestable on this fault library (min margin 0.90); one-hot prototype probabilities NOT calibrated; **every joint-space control number comes from a condition where the structural fault causes no measurable JOINT deficit — the damage is at the tip, which the joint-space score never charges for.**

## Constraints / environment / ops (load-bearing)

- **Simulation-only, one desktop:** Windows 11, Ryzen 7 8700F (8C/16T), RTX 5060 Ti **16 GB VRAM** (Blackwell/sm_120), 32 GB RAM, Python **3.12.10** in `./venv` (use `.\venv\Scripts\python.exe`/`pip.exe`, never bare). Free/OSS, commercial-use-friendly only.
- **venv has:** numpy 2.5.1, scipy 1.18.0, scikit-learn 1.9.0, matplotlib 3.11.0, mujoco 3.10.0, pandas 3.0.3, control 0.10.2, gymnasium 1.3.0, pytest 9.1.1, **torch 2.11.0+cu128** (CUDA 12.8, sm_120-verified).
- **Running packet tests:** from `Reproducibility Packet/`, `..\venv\Scripts\python.exe -m pytest tests/`. **Running a script:** from `Reproducibility Packet/` as `..\venv\Scripts\python.exe scripts\<name>.py`. **Full packet: 347 tests green (S28 re-run; Codex's S27 added +18 data-contract tests over the S26 count of 329).** Set `PYTHONIOENCODING=utf-8` for unicode-printing scripts.
- **Timings (measured, 8 workers):** actuator-action screen (100 arms) ~minutes; info review ~12–20 min; deficit ~20 min (84 arms); severity-quality ~7–9 min (80 arms). Run long jobs in background; **a pipe through `tail`/`*>` buffers until exit — poll for the results file.**
- **STANDING LESSON 1 — dry-run the analysis path before spending a rollout budget.**
- **STANDING LESSON 2 — self-audit from row artifacts / raw bytes, not the summary** (this session: recomputed hashes with my own canonicalizer, not Codex's functions).
- **STANDING LESSON 3 — restate a proxy in the contract's units before comparing to the bar** (`100·(J_C1−J_S)/J_C1`).
- **STANDING LESSON 4 — for a MuJoCo screen, re-run to scratch + diff against committed** (byte-identical = physics+analysis reproduce).
- **STANDING LESSON 5 — verify the live git state before trusting continuity** (this session: startup snapshot said HEAD=Codex S24, live log said Codex S27; the truth surfaced Codex's post-my-S27 session + the open loop). For learned-model work, verify the toolchain (real GPU op, not the flag).
- **PowerShell 5.1** primary (no ternary/`??`; parens in unquoted bash break `eval` — quote or use the Grep tool); Bash tool also available. Use `git diff --numstat` to confirm `+N/−0` after every chat turn.
- **Packet runbook uses `.\.venv\Scripts\python.exe`** (the packet's OWN self-contained venv convention) — NOT our project-root `venv`. Both correct; don't "fix" one into the other.
- **Root `.gitignore`** covers `venv/`, `tmp/`, `MUJOCO_LOG.TXT`, caches, model files `*.pt/*.pth/*.ckpt/*.onnx`, LaTeX aux, OS/IDE noise. **Root `.gitattributes`** (NEW S27) pins `Reproducibility Packet/schema/schema.json` to LF (byte-hash stability). **Packet `.gitignore`** ignores `*.npz` (+ caches/logs); small JSON/CSV/MD artifacts intentionally tracked.
- **Software-engineering standard:** `argparse` (inputs defaulted project-relative in this project's screen convention; outputs project-relative), no hard-coded paths, one purpose, shared logic in `utils/`, docstrings, prints progress, fails loud. Licensing: code MIT, prose CC BY 4.0.

## Pointers

- Claim Sheet (in-force contract): `Claim Sheet.md` · plain-language: `Accessible Claim Sheet.md` · Study Guide Pass 1: `Study Guide/Pass 1 - Conceptual Foundation.tex`
- **Shared schema (in force, +A1):** prose `Reproducibility Packet/schema/schema-v1.0.md`; **machine `schema.json` (NEW, approved S28).**
- **The freeze plan:** `agents/Codex/Config Freeze Readiness Review.md` (I approved same-state S27).
- **My lanes:** sensor `utils/{schema_types,sensor_model,rng,synthetic_plant}.py`; eval `utils/{metrics,stats}.py`; estimator `utils/estimator.py`; synchronous floor `scripts/analyze_synchronous_detection_floor.py`; shared seam test `tests/test_recovery_seam.py`; the three severity/probability screens + tests + `results/`.
- **Codex's lane:** `utils/{cable_mechanics,cable_plant,online_loop,recovery_control,residual_baseline,task_control}.py`; **NEW `utils/{config_contract,storage_contract}.py` + `scripts/validate_data_contract.py` + `tests/test_data_contract.py` + `schema/schema.json` + `config/draft-config-v0.1.json`**; the plant/screen scripts + tests/results.
- **Phase-2 chat:** `chats/Claude-Codex/Phase 2 Integration and Config Freeze/…- Active.md` (**2535 lines**; my S28 same-state approval = tail; **NO open loops**).
- **Monitoring chat:** `chats/Claude-Codex-Human/Transcript Order Monitoring/…- Active.md` (S27 check clean, no note added; flag only on recurrence).
- **CONCLUDED director chat:** `chats/Claude-Codex-Human/Better Suited Task/…- Concluded.md` + `Summary.md` — the withdrawn task-redesign directive. Read its `Summary.md` if the fairer-task idea resurfaces.
- Director requests: `director_requests.md` (root) — entry 1 (Claim Sheet review) non-blocking, awaiting director reply.
- My foundation `agents/Claude/Literature Foundation.md` · ledger `agents/Claude/references.md` (**no S20–S28 entries — reproduction/construction/measurement/review sessions, no external sources read**) · progress reports `agents/Claude/Progress Reports/` (Phase 0/1 Close, S8, S16, S24). **Next due: my S32, or a phase transition / approved amendment.**
- Live-Run README (co-maintained): root `README.md` — **Phase 2 / In Progress**, banner 2026-07-23. **S28 added one lean entry** (screening→confirmatory-build pivot + approved first component).
- Scratchpad (this session, NOT committed): **`append_turn.py`** (binary EOF-append + gates — REUSE/recreate; pass an ASCII marker), `verify_gate1_hashes.py` (independent hash reproduction), `probe_frozen_gate.py` (5 frozen-wall probes), `phase2_turn_s28.md` (my appended turn).
