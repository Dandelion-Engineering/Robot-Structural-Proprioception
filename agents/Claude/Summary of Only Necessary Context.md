# Summary of Only Necessary Context — Claude

*Rewritten every session. Restores my working context for the next session. Excludes anything already in `Project Details/Project Details.md` and `AgentPrompt.md` (I re-read those in full at session start). Last rewritten: end of Session 27, 2026-07-23 18:38 PDT.*

## Where the project is

- **Phase 2 (Execution) is OPEN.** All Phase-1 gates in force. **Schema v1.0 + Amendment A1 in force.** Contract changes run through the **amendment protocol**.
- I am **Claude**; last session was **Session 27**; next session I run is **Session 28**.
- **`config.json` is deliberately NOT frozen.** Do not freeze a partial config. Role hashes are `dev-`; no `dev-` trace may enter confirmatory analysis.
- **The development-screening arc has reached its natural end.** Both recovery-action families are blocked (structural S20; actuator S25/reviewed-S26), diagnosis is characterized (S macro-F1 0.995 vs C1 0.704), and the evidence keeps landing on the pre-registered **"improves diagnosis, not control"** shape (Slot 13). The project has **pivoted from screening variants to building the confirmatory pipeline** toward a config freeze.
- **The freeze path is now an agreed plan** (see "THE FREEZE PATH" below): Codex's Config-Freeze Readiness Review (owner decision `BLOCK_CONFIG_FREEZE_PENDING_PRECONFIRMATORY_BUILD_AND_VALIDATION`, seven gates, DRAFT-vs-FROZEN sequencing) — I reviewed and **approved it same-state in S27; that loop is CLOSED.**
- **No regular progress report due until my Session 32** — unless a phase transition or an approved Claim-Sheet amendment triggers one sooner. Neither is pending.

## What I did in S27 (two things: closed a review loop + de-risked Gate 4)

**1. Genuine first review of Codex's `agents/Codex/Config Freeze Readiness Review.md` → approved same-state, loop CLOSED.** This is a reasoning/planning artifact (no table to recompute), so genuine review = verify its facts against the repo + test its logic against the contract:
   - **Independently reproduced its ten-item repository audit — all correct.** No `schema/schema.json` (only prose `schema-v1.0.md`); no `config.json` in the packet; no identity manifest; `TemporalAttributionNet`/`RMALatentEncoder` exist only as spec comments in `scripts/utils/estimator.py` (lines 44/51), no class bodies; no `class …Loader`; no `split_audit`/leakage-audit fn; no confirmatory CLI; no eval-driver CLI; no Slot-8 verification artifact. Confirmed toolchain half independently: **0 `torch` imports** in packet.
   - **Checked the seven gates against the Claim Sheet's pre-confirmatory-freeze requirements — faithful and complete decomposition; no missing gate.**
   - **Affirmed the DRAFT-vs-FROZEN sequencing correction** (it fixes a circular shorthand that was in BOTH continuities, incl. mine — see the correction below).
   - My approval turn (Phase-2 chat tail, **+36/−0**) records the verification, my Gate-6 position, and two forward notes. Approval explicitly does NOT pre-decide Gate 6 (an open shared decision).

**2. Verified the CUDA PyTorch toolchain on the RTX 5060 Ti (Gate-4 precondition, my lane, unblocked).** Installed `torch==2.11.0+cu128` (CUDA 12.8) into `venv`; ran a REAL GPU op (not just the flag): capability **sm_120 (12,0)**, wheel arch_list includes `sm_120`, matmul→relu→sum→backward executes + finite, GPU vs CPU match at **0.000e+00**. **Pinned `torch==2.11.0+cu128` in root `requirements.txt`** behind an `--extra-index-url https://download.pytorch.org/whl/cu128` line (keeps the pin installable). Core stack unchanged; `test_recovery_seam.py` green. `scratchpad/verify_torch_sm120.py` is the verifier.

## THE FREEZE PATH — the agreed plan (S27; central reference now)

Codex's readiness review is the roadmap from "development screens done" to "confirmatory experiment." **DECISION: BLOCK freeze until seven gates close.** Sequencing correction (load-bearing): a **versioned DRAFT config** governs development/validation data generation; the **final immutable `config.json` freeze comes AFTER model implementation + validation-only hyperparameter/threshold selection and BEFORE any untouched `test` payload.** ("Learned heads post-freeze" was circular — you can't freeze a model you haven't built/selected. They're built under DRAFT config on dev/pilot/val, selected on validation, then frozen.)

**The seven gates + who owns them (per the Phase-1 labor split):**
1. **Machine schema + config authority** — `schema.json`, draft/frozen `config.json` contract, canonical hashing + loader that refuses `dev-*`/draft/mismatched hashes as confirmatory. *(Codex/shared — Codex's stated next increment.)*
2. **Role-separated storage, deployable loader, leakage/split audits** — identity manifest + role-index builders; C0/C1/S deployable observation loader; allowlisted training-data builder; build-failing leakage/split/path/hash/unavailable-channel audits (schema §A/§D/§E). *(Codex/shared — Codex's next increment covers the foundation.)*
3. **Multi-setting design + manifest** — multi-location/severity known-class grids, ≥1 compound/OOD held-out setting, trajectory/payload/contact/onset/excitation distributions, deterministic `dev|pilot|val|test` assignment by WHOLE trajectory AND WHOLE fault setting (no suite-dependent split). *(Shared.)*
4. **Matched learned models** — `TemporalAttributionNet` + `RMALatentEncoder` behind the shared `[W,D]` interface; within-suite capacity ladder; ≥5 training seeds; identical protocol IDs across C0/C1/S. **(MINE.)** *Toolchain now verified ready (torch cu128 on sm_120).*
5. **Calibration/abstention/OOD/uncertainty authorization** — per-suite calibrated probs (Brier/NLL/ECE), abstention + OOD thresholds selected on validation, `severity_uncertainty` defined as a bias-inclusive predictive error scale (NOT in-sample training residual dispersion — my S24 finding: understates true by 5.72× for S). **(MINE.)**
6. **Confirmatory controller protocol** — freeze the fair comparison arms (no-action, transparent attribution-driven, RMA, oracle); do NOT retune blocked families post-hoc. *(Codex owns controller; the diagnosis→control seam is shared.)* **← the one OPEN shared decision (below).**
7. **Evaluation driver + confirmatory manifest** — one CLI owning the `[t_c,t_c+5s]` slice, role joins, paired C1/S table, exclusions, CIs; sample-size from pilot/val variance; rejects `dev-*`/wrong-hash/cross-role/incomplete-pair/truncated inputs. **(MINE — eval lane.)**

**Recommended order:** (1) persistence foundation [Codex] → (2) draft multi-setting manifest [shared] → (3) models + calibration validation [me] → (4) controller + sample-size decision [shared] → (5) **joint immutable freeze** → (6) one-shot confirmatory generation + eval → Phase 3. **My Gate-4/5/7 work WAITS on Codex's Gate-1/2 foundation + the Gate-3 draft manifest** (pre-registration integrity: splits assigned before any headline fit).

Not freeze blockers (still required before project completion): Slot-8 verification artifact (after confirmatory outputs), Technical Report / Accessible Piece / Study Guide Pass 2 (Phase 3), fresh-environment packet validation.

## THE ONE OPEN SHARED DECISION — Gate 6 (converge with Codex next session)

Both action families blocked; Claim Sheet still requires a pre-declared fair controller comparison. **My position (in my S27 chat turn):**
- **Default (in-contract, NO amendment): build the fair protocol and RUN the pre-registered paired C1-vs-S control comparison** (no-action / transparent-attribution-at-reviewed-floors / RMA / oracle arms). It will very likely return ~no control gain (structural fault → no JOINT deficit; damage at the tip) = the pre-registered Slot-13 "diagnostic-only" landing. Running it and landing there is IN-CONTRACT and yields the clean pre-registered negative.
- **Narrowing the confirmatory scope to information/detection-only (not running a control arm) IS a Claim-Sheet amendment** → director sign-off + progress report.
- **I recommend the default** (pre-registration is exactly the tool for "we expect this to fail"). This is the one place to converge explicitly before the Gate-3 manifest hardens around it.

## The single most important things to do next session (Session 28)

1. **Read Codex's latest first** (its next HumanReport + Phase-2 chat tail). Codex's stated next increment is **Gate 1 + Codex/shared portion of Gate 2** (machine `schema.json`, draft/frozen config contract + canonical hashing, role-manifest/loader/audit foundation). If landed, review it (genuine cross-review).
2. **Converge with Codex on Gate 6** (run the pre-registered comparison vs. narrow-scope+amendment).
3. **My lane, once Codex's Gate-1/2 foundation + the Gate-3 draft manifest exist:** build `TemporalAttributionNet` + `RMALatentEncoder` behind the shared `[W,D]` interface (toolchain verified ready), then Gate-5 calibration/abstention/OOD/uncertainty on validation only. Do NOT build model/data ahead of the jointly-approved draft manifest.
4. **Do NOT freeze a partial config.**

## Review-cycle state (all loops CLOSED)

- **NO open review loops.** The Config-Freeze Readiness Review loop closed at my S27 same-state approval. The actuator-action loop closed (my S26 approval + Codex's S26 ack). The prior class-probability loop closed at my S25 approval. Do not reopen any.

## MONITORING DUTY (standing)

- **S26 check CLEAN** — Codex's S26 append to the Phase-2 chat was a verified **+32/−0** tail addition, Codex physically last (`git show --numstat d93156e`). **Fifth consecutive clean append.** Did NOT post to `Transcript Order Monitoring` (flag only on recurrence; keep the thread lean).
- **REUSE the binary-EOF-append approach for every chat turn.** My previous `append_turn.py` was in a prior (uncommitted) scratchpad and is gone; **I recreated it this session** at `scratchpad/append_turn.py` (binary EOF-append + gates: marker-absent-before / prefix-byte-identical / marker-present-once-after-old-boundary / turn-last). **Pass an ASCII-only unique marker** (the timestamp string, e.g. `Session 27, 2026-07-23 18:35 PDT`). Verify `git diff --numstat` shows `+N/−0` after. *(This session's append: Phase-2 +36/−0.)* If gone again next session, recreate it (the logic is simple; the point is binary EOF append, never string-anchor patching).

## Toolchain state (NEW — Gate-4 precondition DONE)

- **`torch==2.11.0+cu128` installed in `venv` and VERIFIED on the RTX 5060 Ti (Blackwell/sm_120):** kernels + autograd execute, GPU==CPU at 0.000e+00. Pinned in root `requirements.txt` behind the cu128 `--extra-index-url`. **So Gate 4's biggest unknown ("does a free CUDA build run on sm_120?") is a verified YES — no CPU/nightly fallback needed.** `torch` lives in `venv/` (gitignored); `.gitignore` also covers `*.pt/*.pth/*.ckpt/*.onnx` for future model files.

## The actuator recovery-action screen result (Codex's lane; reviewed+approved S26; reference)

`Reproducibility Packet/scripts/screen_actuator_recovery_action.py` (+ test + `results/actuator_recovery_action_screen/`). Selected `actuator_gain_remaining_0p25`, bounded z=0.200 task, location 1. 36 tuning arms (seeds 18000–18002) + 64 disjoint assessment arms (seeds 17100–17103). Cap/floor family {2/.25,3/.25,4/.25,5/.25,5/.20}. Source-specific margin = fault-action benefit − same diagnosis falsely authorized on healthy.

| profile | fault reduction | healthy false-auth | source-specific margin | why BLOCK |
|---|---:|---:|---:|---|
| **cap3/.25 (safe, selected)** | 16.58% | 8.32% | **8.25 pp** [8.09,8.53] | < 10-pp bar |
| cap5/.20 & cap5/.25 (S) | 19.44% | 9.26% | 10.18 pp | fails A1 lifecycle safety (19 candidate A1-incident arms = high-torque healthy, peak\|gauge\|>500 µε) |

Decision `BLOCK_ACTUATOR_ACTION_FAMILY_AT_SOURCE_SPECIFIC_GATE`. Baseline-convention robust (common faulted baseline → 9.81 pp, still <10). At safe cap-3, oracle/C1/S command identically (severity saturates m=3) → NOT a C1-vs-S control result. Development action-mechanism evidence only.

## THE STRUCTURAL RESULT — honest development-evidence boundary (Codex's S20 rows)

| remaining EI | mean peak \|gauge\| | mean **joint** tracking deficit |
|---:|---:|---:|
| healthy | 19.2 µε | — |
| 0.50 | 38.4 µε | +0.08% |
| 0.25 | 72.4 µε | −0.89% |
| 0.10 | 152.8 µε | −2.23% |
| 0.05 | 259.7 µε | −5.00% |

Monotone in information; monotone the WRONG way in joint control (13.5× healthy strain at the severity where joint tracking is 5% *better* than healthy — damage moves to the tip, which the joint score never measures). This is the honest finding that motivated the (withdrawn) redirection; it stays on the record, seed for a future "better-suited task" project.

## The control-layer shape table (Codex's `bounded_noisy_information_review`)

| source | C1 gate | S gate | S exclusive info? | `s_tracking_change_pct` |
|---|---|---|---|---:|
| healthy | correct_no_action | correct_no_action | no | 0.0000% |
| **structure** | withheld_actionable | correct_actionable | **YES** | **−18.5762%** |
| actuator | correct_actionable | correct_actionable | no | 0.0000% |
| sensor | correct_no_action | correct_no_action | no | 0.0000% |

C1 per-class recall: structure **0.083**, actuator/sensor 1.000 (S: 1.000 all). **Where S has exclusive info there's no control headroom; where there's headroom S has no exclusive info.** = the pre-registered Slot-13 diagnostic-only landing.

## My lanes — current state

`Reproducibility Packet/scripts/utils/estimator.py`:
- **`WindowFeatureExtractor(window_steps=W=768, probe_frequency_hz=0.8)`**: `[W,D]` left-padded + per-column `[last,mean,std,slope,sync_cos,sync_sin,sync_amplitude,valid_fraction]` over 18-col registry → 144 features. Constants: `N_FEATURE_STATS=4`, `N_EXTRA_FEATURES=4`, sync cols 4/5/6, `VALID_FRACTION_COL=7`, `DIAGNOSTIC_PROBE_HZ=0.8`, `MIN_SYNC_SAMPLES=8`.
- **`WindowNoveltyDetector`** (detect+abstain) · **`CoefficientReferenceDetector`** (2nd interpretable rung; canonical `synchronous_coefficient_vector`+`coefficient_reference_distance`; `fit_reference` atomic; `calibrate_threshold` fail-loud below `ceil(min_tail/far)`) · **`_SCORE_STD_FLOOR=1e-3`** shared · **`SeverityRidgeHead`** (deployable severity read-out; suite-agnostic; `train_residual_std` is IN-SAMPLE — never feed a confidence gate) · **`leave_one_group_out_residuals`** (CALIBRATION-role diagnostic; group by sensor seed) · **`OracleInterface(onset_time_s)`** (causal privileged ceiling) · **`EstimatorCommandPolicy`** (seam adapter; runs estimator every `stride`, ZOHs OUTPUT) · `RECOMMENDED_WINDOW=(768,16)` pilot proposal · **learned rungs specified-not-built (Gate 4 — MINE; toolchain now ready).**
- **`utils/metrics.py` + `utils/stats.py`** (jointly approved through S11): `tracking_reduction_pct(j_baseline,j_treatment)=100·(j_baseline−j_treatment)/j_baseline`, `j_5s` fail-loud on full `[t_c,t_c+5s]`, `safety_incident_rate`, `safety_regression_delta` (matched `[T,7]` guard), `hierarchical_bootstrap_ci` (crossed pair×seed). **Eval driver (Gate 7) — build once frozen data layout exists.**
- **Screens (all jointly approved/closed; valid joint-space development measurements):** `screen_severity_estimation_quality.py` (80 arms; held-out MAE C1 0.0065/S 0.0076; its `arm_rows.csv` at seeds 17100–17103 is the Step-15 CRN source the actuator-action screen reuses), `screen_severity_action_boundary.py` (40 arms; paired −0.1177% mean), `screen_actuator_probability_channel.py` (36 arms; 5.07 pp graded / 10.85 pp gate-crossing). `tests/test_recovery_seam.py` (shared mechanism regression, 4 tests).

## Codex's lanes — current state

- **`agents/Codex/Config Freeze Readiness Review.md` (NEW S26; I approved same-state S27)** — the seven-gate freeze plan above.
- `screen_actuator_recovery_action.py` (NEW S25; I reviewed/approved S26 — table above). Reuses `screen_bounded_task_contact` harness + `GainScheduledRecoveryController` + Step-15 severity CRN.
- `screen_fault_tracking_deficit.py` + results (CLOSED S22): gate `required_reduction_pct`=12%, `required_deficit_pct`=13.636%; selection `actuator_gain_remaining_0p25`; structural rows produced NO deficit.
- `utils/recovery_control.py` — `GainScheduledRecoveryController`. Actuator: `multiplier=1+p·(capped_compensation−1)`, `capped=min(1/max(remaining,floor),cap)`. Gate `_confident_source`=not-abstained AND unique-argmax==source AND p≥0.5 AND finite σ≤0.25. Constants: `maximum_gain_compensation=2.0`, `minimum_gain_remaining=0.25`, `torque_abs_limit=(1.0,0.5)`.
- `screen_structural_recovery_action.py` (CLOSED S20): `BLOCK_STRUCTURAL_RECOVERY_ACTION_FAMILY`; ~70% of benefit at the *unfaulted* joint.
- `run_bounded_noisy_information_review.py` (CLOSED S19): S PASSES info+action gates (macro-F1 0.995, 100% per-fault detection, 2.1% FA); C1 BLOCKS (0.704, 8.3% structural recall). One-hot mechanism probs (NOT calibrated).
- `utils/task_control.py` (S17/S18): `BoundedTaskProfile` (rest→(0.30,0.30) rad by 3.0s→hold→rest by 5.0s — JOINT-SPACE targets), `ObservedJointPDController` (kp (0.05,0.03), kd (0.005,0.003), torque limits (0.20,0.10); reads ONLY `q_obs`/`qd_obs`) + `EstimatorRecoveryTaskPolicy`.
- `screen_bounded_task_contact.py` — bounded-task-with-contact mechanics harness (`BoundedTaskContactSpec`, `SingleDecisionHoldEstimator`, `cable_config`); plane_heights (0.100, 0.200).
- `utils/cable_mechanics.py` + `utils/cable_plant.py` + `make_mujoco_plant_trace.py` (S14/S15): A1 safety flags = `|q|>π`, `|qd|>10`, 3-D tip radius >0.82 from `[0,0,0.5]`, `max|gauge|>500 µε`, `contact_state[0]>5 N`. **Fault severity = REMAINING fraction.**

## Schema v1.0 + A1 (in force)

`Reproducibility Packet/schema/schema-v1.0.md` (rendered in `utils/schema_types.py` + `utils/estimator.py` §D). A1: `contact_state[2]`, `safety_flag[7]` (order: joint_angle_0/1, joint_speed_0/1, tip_workspace, gauge_abs, tip_contact_force), safety from privileged truth. **§D does NOT define what statistic `severity_uncertainty` is (my S24 RMS proposal, still a dev fixture — Gate 5 must define it as a bias-inclusive predictive error scale, freeze open).** §A splits by whole trajectory AND whole fault setting (suite never a split input; CRN within a pair via `utils/rng.py`) — **S19 gap stands: held-out axes are sensor-seed only (Gate 2/3 fix this).** §G tracking metric `J_5s`. **Gate 1 will render this prose schema as machine `schema.json`.**

## The agreed contract's load-bearing specifics

- **Sensor suites (controlled variable):** C0 = joint encoders + commanded actuation · **C1 = C0 + noisy motor-current nominal-Kt torque estimate + one distal 6-axis IMU** · **S = C1 + four fixed strain/curvature gauge stations** · O = privileged oracle.
- **Two settled correctness points:** actuator-gain fault acts *downstream* of the current proxy (C1 not handed true delivered torque); encoder fault has a *relational* signature.
- **Success bar (pre-declared, BOTH layers):** S improves held-out four-way macro-F1 over C1 by **≥0.05 absolute** (paired 95% excludes zero; every source-class recall diff lower-95% above **−0.02**) AND reduces the **5-s post-change integral of absolute tracking error by ≥10%** (`100·(J_C1−J_S)/J_C1`, paired 95% excludes zero, no safety regression) under realistic confounds. Known-class abstention = error in headline macro-F1.
- **Failure shapes:** hypothesis failure (C1+temporal adaptation matches S — clean negative) vs method failure. **Inconclusive (Slot 13):** diagnostic-only (attribution improves, control doesn't — **the shape the evidence keeps landing on**) · fault-specific/bounded · confound-fragile · excitation-dependent.
- **Pre-specification:** freeze gauge placement, model/hyperparams, thresholds, analysis window, seeds/scenarios before confirmatory generation. Leakage-free splits. ≥5 training seeds. Paired hierarchical bootstrap.

## Coherence / honesty bounds (keep loud)

- `utils/synchronous.py` (Codex S9) = the single shared harmonic statistic; `synchronous_coefficient_vector`+`coefficient_reference_distance` in `estimator.py` = the one canonical definition every pilot/screen/review imports.
- **Sensor RNG keyed on `(sensor_seed, pair_id, channel, stream)`** — `pair_id` load-bearing; screens reuse an upstream screen's `pair_id` verbatim and check CRN at 0.000e+00.
- Deployable floors are *detection*, not learned attribution; all rates from ONE fixed fault setting per class, held out over sensor noise only; abstention untestable on this fault library (min margin 0.90); one-hot prototype probabilities NOT calibrated; **every joint-space control number comes from a condition where the structural fault causes no measurable JOINT deficit — the damage is at the tip, which the joint-space score never charges for.**

## Constraints / environment / ops (load-bearing)

- **Simulation-only, one desktop:** Windows 11, Ryzen 7 8700F (8C/16T), RTX 5060 Ti **16 GB VRAM** (Blackwell/sm_120), 32 GB RAM, Python **3.12.10** in `./venv` (use `.\venv\Scripts\python.exe`/`pip.exe`, never bare). Free/OSS, commercial-use-friendly only.
- **venv has:** numpy 2.5.1, scipy 1.18.0, scikit-learn 1.9.0, matplotlib 3.11.0, mujoco 3.10.0, pandas 3.0.3, control 0.10.2, gymnasium 1.3.0, pytest 9.1.1, **and now `torch 2.11.0+cu128` (CUDA 12.8, sm_120-verified — S27).**
- **Running packet tests:** from `Reproducibility Packet/`, `..\venv\Scripts\python.exe -m pytest tests/`. **Running a script:** from `Reproducibility Packet/` as `..\venv\Scripts\python.exe scripts\<name>.py`. **Full packet: 329 tests green (last full run S26; S27 ran only test_recovery_seam=4 green).** Set `PYTHONIOENCODING=utf-8` for unicode-printing scripts.
- **Timings (measured, 8 workers):** actuator-action screen (100 arms) ~minutes; info review ~12–20 min; deficit ~20 min (84 arms); severity-quality ~7–9 min (80 arms). Run long jobs in background; **a pipe through `tail`/`*>` buffers until exit — poll for the results file.**
- **STANDING LESSON 1 — dry-run the analysis path before spending a rollout budget.**
- **STANDING LESSON 2 — self-audit from row artifacts, not the summary.**
- **STANDING LESSON 3 — restate a proxy in the contract's units before comparing to the bar** (`100·(J_C1−J_S)/J_C1`).
- **STANDING LESSON 4 — for a MuJoCo screen, re-run to scratch + diff against committed** (byte-identical = physics+analysis reproduce).
- **STANDING LESSON 5 (S27) — verify the live git state before trusting continuity.** My continuity predated Codex's S26; reading `git log` (HEAD=`Codex Session 26`) surfaced an unreviewed session + the open loop. For learned-model work, verify the toolchain (real GPU op, not the availability flag) rather than assume support.
- **PowerShell 5.1** primary (no ternary/`??`; parens in unquoted bash break `eval` — quote or use the Grep tool); Bash tool also available. Use `git diff --numstat` to confirm `+N/−0` after every chat turn.
- **Packet runbook uses `.\.venv\Scripts\python.exe`** (the packet's OWN self-contained venv convention) — NOT our project-root `venv`. Both correct; don't "fix" one into the other.
- **Root `.gitignore`** covers `venv/` (where torch lives), `tmp/`, `MUJOCO_LOG.TXT`, caches, model files `*.pt/*.pth/*.ckpt/*.onnx`, LaTeX aux, OS/IDE noise — verified accurate S27. **Packet `.gitignore`** ignores `*.npz` (+ caches/logs); small JSON/CSV/MD artifacts intentionally tracked.
- **Software-engineering standard:** `argparse` (inputs defaulted project-relative in this project's screen convention; outputs project-relative), no hard-coded paths, one purpose, shared logic in `utils/`, docstrings, prints progress, fails loud. Licensing: code MIT, prose CC BY 4.0.

## Pointers

- Claim Sheet (in-force contract): `Claim Sheet.md` · plain-language: `Accessible Claim Sheet.md` · Study Guide Pass 1: `Study Guide/Pass 1 - Conceptual Foundation.tex`
- **Shared schema (in force, +A1):** `Reproducibility Packet/schema/schema-v1.0.md`
- **The freeze plan:** `agents/Codex/Config Freeze Readiness Review.md` (I approved same-state S27).
- **My lanes:** sensor `utils/{schema_types,sensor_model,rng,synthetic_plant}.py`; eval `utils/{metrics,stats}.py`; estimator `utils/estimator.py`; synchronous floor `scripts/analyze_synchronous_detection_floor.py`; shared seam test `tests/test_recovery_seam.py`; the three severity/probability screens + tests + `results/`.
- **Codex's lane:** `utils/{cable_mechanics,cable_plant,online_loop,recovery_control,residual_baseline,task_control}.py`; `scripts/{make_mujoco_plant_trace,run_feasibility_spike,run_bounded_burst_sensitivity,screen_synchronous_safe_probe,run_bounded_noisy_information_review,screen_fault_tracking_deficit,screen_structural_recovery_action,screen_bounded_task_contact,screen_actuator_recovery_action}.py` + its tests/results.
- **Phase-2 chat:** `chats/Claude-Codex/Phase 2 Integration and Config Freeze/…- Active.md` (**2444 lines**; my S27 same-state approval = tail; **NO open loops**).
- **Monitoring chat:** `chats/Claude-Codex-Human/Transcript Order Monitoring/…- Active.md` (S26 clean, no note added; flag only on recurrence).
- **CONCLUDED director chat:** `chats/Claude-Codex-Human/Better Suited Task/…- Concluded.md` + `Summary.md` — the withdrawn task-redesign directive. Read the `Summary.md` if the fairer-task idea resurfaces.
- Director requests: `director_requests.md` (root) — entry 1 (Claim Sheet review) non-blocking, awaiting director reply.
- My foundation `agents/Claude/Literature Foundation.md` · ledger `agents/Claude/references.md` (**no S20–S27 entries — reproduction/construction/measurement/review sessions, no external sources read**) · progress reports `agents/Claude/Progress Reports/` (Phase 0/1 Close, S8, S16, S24). **Next due: my S32, or a phase transition / approved amendment.**
- Live-Run README (co-maintained): root `README.md` — **Phase 2 / In Progress**, banner 2026-07-23. S27 heartbeat: no public entry (internal readiness ratification + toolchain verification; Codex made the same call for its S26). *Low-priority: the screening→confirmatory-build pivot might merit one lean public entry once the first foundation component lands — raise with Codex then.*
- Scratchpad (this session, NOT committed): **`append_turn.py`** (binary EOF-append + gates — REUSE/recreate; pass an ASCII marker), `verify_torch_sm120.py` (GPU verifier), `phase2_turn.md` (my appended turn).
