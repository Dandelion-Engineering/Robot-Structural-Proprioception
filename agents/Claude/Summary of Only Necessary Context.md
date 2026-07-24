# Summary of Only Necessary Context — Claude

*Rewritten every session. Restores my working context for the next session. Excludes anything already in `Project Details/Project Details.md` and `AgentPrompt.md` (I re-read those in full at session start). Last rewritten: end of Session 26, 2026-07-23 17:00 PDT.*

## Where the project is

- **Phase 2 (Execution) is OPEN.** All Phase-1 gates in force. **Schema v1.0 + Amendment A1 in force.** Contract changes run through the **amendment protocol**.
- I am **Claude**; last session was **Session 26**; next session I run is **Session 27**.
- **THE S25 "REDIRECTION" IS DEAD — do not chase it.** The director opened `Better Suited Task` on 2026-07-23 asking for a fairer end-effector task, I opened the discussion, and then **he withdrew the request the same day** and asked us to finish this project under the already-approved Claim Sheet, deferring a fairer task to a separate follow-on project. That chat is **CONCLUDED**. **The original scope is the whole plan now.** (I am still free to propose small in-scope amendments if the remaining work needs one.)
- **`config.json` is deliberately NOT frozen.** Do not freeze a partial config. Role hashes are `dev-`; no `dev-` trace may enter confirmatory analysis.
- **Packet: 329 tests green** (Codex's S25 added +27 for its actuator recovery-action screen; I reviewed/reproduced them).
- **No regular progress report due until my Session 32** — UNLESS a phase transition or an approved Claim-Sheet amendment triggers one sooner. Neither is pending.

## What I did in S26 (two anchors, both set while I was away)

**1. Acknowledged the director's withdrawal and CONCLUDED `Better Suited Task`.** Codex had acknowledged in its S25; I acknowledged in S26; per Randy's instruction I renamed the transcript to `…- Concluded.md` and wrote its `Summary.md`. No amendment was ever written; the Claim Sheet is unchanged. **The joint-space screens stay as honest development evidence at their boundary — NOT "superseded-pending-amendment" anymore (there is no amendment); they are simply development evidence that this joint-space task can't test the structural fault.**

**2. Reviewed + reproduced + approved (same-state) Codex's actuator recovery-action screen — Phase-2 review loop CLOSED.** This was the technical substance of the session. Codex (owner) handed me `screen_actuator_recovery_action.py` in its S25; I was reviewer. **Decision: `BLOCK_ACTUATOR_ACTION_FAMILY_AT_SOURCE_SPECIFIC_GATE` — correct and honest.** What I did to earn the approval (not rubber-stamp):
   - Recomputed **every** number in `summary.json` from the committed row CSVs with my own arithmetic (5 candidate + 7 assessment summaries, per-seed margins, gates, decision) — all match. (`scratchpad/s26_audit.py`.)
   - Reproduced all 7 paired bootstrap intervals bit-for-bit. (The two cap5-S rows share an interval legitimately: their 4 seed-margins are identical because every S severity estimate exceeds both floors → floor never binds for S.)
   - Re-derived audit counts: **19** candidate A1-incident arms / 0 saturated / 0 multiplier-mismatch; references clean; one predecision hash per (role,seed,source).
   - Confirmed CRN reuse against the **Step-15 source file** independently: no-action refs == severity screen's committed `J_5s` at seeds 17100–17103 (severity 0.25→actuator, 1.0→healthy) at **max delta 0.000e+00**. (`scratchpad/s26_crn_and_robustness.py`.)
   - **Fresh full 100-arm MuJoCo re-run in a separate process → `summary.json` + row CSVs BYTE-IDENTICAL to committed.** 27 focused + **329** packet tests pass.
   - My approval turn is at the tail of the Phase-2 chat (+30/−0). Loop closed at the same committed state; I added one **non-blocking** forward note (the assessment table could gain a `safe?` column so an above-bar-but-BLOCK cap5-S row is self-explanatory).

## The single most important things to do next session (Session 27)

1. **Read Codex's latest first** (HumanReport ≥26 + its continuity + the Phase-2 chat tail). Codex may have started a new gate.
2. **The live strategic question — raise/settle with Codex: what remains before the `config.json` freeze?** The recovery-action side has now landed twice: **actuator** recovery = positive but not *safe + source-specific* (this session's BLOCK), **structural** recovery = blocked (S20). Detection/attribution is characterized (S info review: S macro-F1 0.995 vs C1 0.704). Severity read-out characterized. **On this bounded joint-space task the evidence keeps pointing at the pre-registered "improves diagnosis, not control" landing.** So the real open items are: (a) is the project ready to *specify and freeze* the confirmatory configuration and run the pre-registered confirmatory experiment? (b) if not, which gates remain and who owns them? This is the coordination I should drive next, in the Phase-2 chat.
3. **Do NOT freeze a partial config;** do NOT build the deferred post-freeze work early (see below).
4. **Cross-review:** I reviewed Codex's S25 work this session (the actuator-action screen); next session read its most recent unreviewed human report + the work it points to.

## Deferred work (post-config-freeze; do NOT build early)

- **Learned attribution rungs** (`TemporalAttributionNet` + `RMALatentEncoder`) — need PyTorch CUDA build (verify sm_120), frozen config, confirmatory data.
- **Schema §D deployable-loader leakage test + whole-trajectory/fault-setting split audit** — need real multi-run storage (S19 gap: held-out axes are sensor-seed only).
- **The eval driver** (argparse CLI owning the exact `[t_c, t_c+5 s]` slice → paired C1-vs-S control comparison) — needs the frozen data layout.

## Review-cycle state (all loops CLOSED)

- **NO open review loops in the Phase-2 chat.** The actuator-action loop closed at my S26 same-state approval. The prior class-probability loop closed at my S25 same-state approval. Do not reopen either.
- **The one thing I left as a NON-BLOCKING forward note** (not a reopen): the actuator-action report's assessment table shows cap5-S as "10.18 pp [9.68,10.63] BLOCK" with the lifecycle-safety reason only in the prose — a future rewrite could add an inline `safe?`/lifecycle column. Codex can fold it in whenever; it is not a condition of approval.

## MONITORING DUTY (standing)

- **S26 check CLEAN** — Codex's S25 appends were verified pure tail additions at the git level: **+20/−0** (`Better Suited Task`), **+30/−0** (Phase-2 chat), Codex physically last in both. **Fourth consecutive clean append.** I did NOT post to `Transcript Order Monitoring` (duty is to flag *recurrences*; keep the thread lean). Flag only on recurrence.
- **REUSE `scratchpad/append_turn.py`** for every chat turn: binary EOF-append (structurally immune to the mid-file-insertion bug) + gates (marker-absent-before / present-once-after / after-old-boundary / Claude-last / prefix-preserved). **Pass an ASCII-only unique marker** (the timestamp string, e.g. `Session 26, 2026-07-23 16:57 PDT`) as the marker arg. Verify `git diff --numstat` shows `+N / −0` after. *(This session's two appends: BST +12/−0, Phase-2 +30/−0.)*

## The actuator recovery-action screen result (Codex's lane; reviewed+approved S26; for reference)

`Reproducibility Packet/scripts/screen_actuator_recovery_action.py` (+ test + `results/actuator_recovery_action_screen/`). At the selected `actuator_gain_remaining_0p25`, bounded z=0.200 task, location 1. Role-separated: 36 tuning arms (seeds 18000–18002) + 64 disjoint assessment arms (seeds 17100–17103). Cap/floor family {2/.25, 3/.25, 4/.25, 5/.25, 5/.20}. **Source-specific margin = fault-action benefit − same diagnosis falsely authorized on healthy** (this null is the honest core — it strips out the generic torque-boost that helps even a healthy arm on this torque-limited task).

| profile (selected = cap3) | fault reduction | healthy false-auth benefit | source-specific margin | why BLOCK |
|---|---:|---:|---:|---|
| **cap3/.25 (safe, selected)** | 16.58% | 8.32% | **8.25 pp** [8.09,8.53] | < 10-pp bar |
| cap5/.20 & cap5/.25 (S) | 19.44% | 9.26% | 10.18 pp | fails A1 lifecycle safety |

- Only the profiles that cross the bar (cap5-S) are **unsafe** (19 candidate A1-incident arms = high-torque healthy arms, peak |gauge| >500 µε, tip out of workspace). At the safe cap-3, oracle/C1/S **command identically** (severity saturates at m=3) → **NOT a C1-vs-S control result**.
- **Robustness I verified:** the margin subtracts two %-reductions vs different baselines; recomputed with a common (faulted) baseline it rises to **9.81 pp**, still < 10. The BLOCK does not depend on the baseline convention.
- **Evidence boundary (keep loud):** development action-mechanism only — NOT calibrated authorization (the forced false-auth measures a *consequence*, not a rate), NOT a C1-vs-S control result, NOT validation/confirmatory-sized, NOT a task change. Config unfrozen.

## THE STRUCTURAL RESULT — the honest development-evidence boundary (Codex's S20 rows)

| remaining EI | mean peak \|gauge\| | mean **joint** tracking deficit |
|---:|---:|---:|
| healthy | 19.2 µε | — |
| 0.50 | 38.4 µε | +0.08% |
| 0.25 | 72.4 µε | −0.89% |
| 0.10 | 152.8 µε | −2.23% |
| 0.05 | 259.7 µε | −5.00% |

**Monotone in information; monotone the WRONG way in joint control.** 13.5× the healthy strain signature at the severity where *joint* tracking is 5% *better* than healthy — because on this joint-space task the damage moves from the joint to the tip, which the joint-space score never measures. This is the honest development finding that motivated (the now-withdrawn) redirection; it stays on the record, un-retracted, and is the natural seed for a future "better-suited task" project.

## The control-layer shape table (Codex's `bounded_noisy_information_review`)

| source | C1 gate state | S gate state | S exclusive info? | `s_tracking_change_pct` |
|---|---|---|---|---:|
| healthy | correct_no_action | correct_no_action | no | 0.0000% |
| **structure** | withheld_actionable | correct_actionable | **YES** | **−18.5762%** |
| actuator | correct_actionable | correct_actionable | no | 0.0000% |
| sensor | correct_no_action | correct_no_action | no | 0.0000% |

C1 per-class recall: structure **0.083**, actuator 1.000, sensor 1.000 (S: 1.000 all). **On this task: where S has exclusive info there's no control headroom; where there's headroom S has no exclusive info.** This shape — now reinforced from the actuator side by the S26 BLOCK — is the pre-registered "improves diagnosis, not control" landing (Slot 13 diagnostic-only inconclusive shape).

## My lanes — current state

`Reproducibility Packet/scripts/utils/estimator.py`:
- **`WindowFeatureExtractor(window_steps=W=768, probe_frequency_hz=0.8)`**: `[W,D]` left-padded + per-column `[last,mean,std,slope,sync_cos,sync_sin,sync_amplitude,valid_fraction]` over 18-col registry → 144 features. Constants: `N_FEATURE_STATS=4`, `N_EXTRA_FEATURES=4`, sync cols 4/5/6, `VALID_FRACTION_COL=7`, `DIAGNOSTIC_PROBE_HZ=0.8`, `MIN_SYNC_SAMPLES=8`.
- **`WindowNoveltyDetector`** (detect+abstain) · **`CoefficientReferenceDetector`** (2nd interpretable detection rung; canonical `synchronous_coefficient_vector` + `coefficient_reference_distance`; `fit_reference` atomic; `calibrate_threshold` fail-loud below `ceil(min_tail/far)`) · **`_SCORE_STD_FLOOR=1e-3`** shared · **`SeverityRidgeHead`** (deployable severity read-out; suite-agnostic; `train_residual_std` is IN-SAMPLE — never feed a confidence gate) · **`leave_one_group_out_residuals`** (CALIBRATION-role diagnostic; group by sensor seed) · **`OracleInterface(onset_time_s)`** (causal privileged ceiling) · **`EstimatorCommandPolicy`** (seam adapter; runs estimator every `stride`, ZOHs the OUTPUT) · `RECOMMENDED_WINDOW=(768,16)` pilot proposal · learned rungs specified-not-built.
- **`utils/metrics.py` + `utils/stats.py`** (jointly approved through S11): `tracking_reduction_pct(j_baseline,j_treatment)=100·(j_baseline−j_treatment)/j_baseline` (baseline in denominator), `j_5s` fail-loud on the full `[t_c,t_c+5s]` window, `safety_incident_rate`, `safety_regression_delta` (matched `[T,7]` guard), `hierarchical_bootstrap_ci` (crossed pair×seed). Eval **driver** — build once frozen data layout exists.
- **Screens (all jointly approved/closed; valid joint-space development measurements):** `screen_severity_estimation_quality.py` (80 arms; held-out MAE C1 0.0065/S 0.0076; `window_features.csv` durable — **its `arm_rows.csv` assessment rows at seeds 17100–17103 are the Step-15 CRN source the actuator-action screen reuses**), `screen_severity_action_boundary.py` (40 arms; paired −0.1177% mean/0.5154% worst), `screen_actuator_probability_channel.py` (36 arms; sampled-envelope 5.07 pp graded / 10.85 pp gate-crossing). `tests/test_recovery_seam.py` (shared mechanism regression, 4 tests).

## Codex's lanes — current state

- **`screen_actuator_recovery_action.py` (NEW S25; I reviewed/approved S26 — see result table above).** Reuses `screen_bounded_task_contact` mechanics harness + `GainScheduledRecoveryController` + Step-15 severity CRN.
- `screen_fault_tracking_deficit.py` + `results/fault_tracking_deficit_screen/` (CLOSED S22): gate `required_reduction_pct`=12%, `required_deficit_pct`=13.636%. Selection = `actuator_gain_remaining_0p25`. **Structural rows produced NO deficit (turned negative).**
- `utils/recovery_control.py` — `GainScheduledRecoveryController`. Actuator branch: `multiplier = 1 + p·(capped_compensation − 1)`, `capped=min(1/max(remaining,floor),cap)`. Gate `_confident_source` = not abstained AND unique argmax==source AND p≥0.5 AND finite σ ≤ 0.25. **Load-bearing constants:** `maximum_gain_compensation=2.0` (default), `minimum_gain_remaining=0.25`, `torque_abs_limit=(1.0,0.5)`. *(The action screen overrides cap/floor per candidate; PD nominal torque limits (0.20,0.10) keep applied torque below the recovery clip so multiplier identity holds.)*
- `screen_structural_recovery_action.py` (CLOSED S20): `BLOCK_STRUCTURAL_RECOVERY_ACTION_FAMILY`; ~70% of benefit at the *unfaulted* joint.
- `run_bounded_noisy_information_review.py` (CLOSED S19): S PASSES info+action gates (macro-F1 0.995, 100% per-fault detection, 2.1% FA); C1 BLOCKS (0.704, 8.3% structural recall). One-hot mechanism probabilities (p=1, NOT calibrated).
- `utils/task_control.py` (S17/S18): `BoundedTaskProfile` (rest→(0.30,0.30) rad by 3.0s→hold→rest by 5.0s — **JOINT-SPACE targets**), `ObservedJointPDController` (kp (0.05,0.03), kd (0.005,0.003), torque limits (0.20,0.10); reads ONLY `q_obs`/`qd_obs`). Plus `EstimatorRecoveryTaskPolicy` (used by the action screen).
- `screen_bounded_task_contact.py` — the bounded-task-with-contact mechanics harness (`BoundedTaskContactSpec`, `SingleDecisionHoldEstimator`, `cable_config`); provides onset/decision timing, plane heights, thermal rate, task profile, controller config. The actuator-action screen builds directly on it (plane_heights (0.100, 0.200)).
- `utils/cable_mechanics.py` + `utils/cable_plant.py` + `make_mujoco_plant_trace.py` (S14/S15): A1 safety flags = `|q|>π`, `|qd|>10`, 3-D tip radius >0.82 from `[0,0,0.5]`, `max|gauge|>500 µε`, `contact_state[0]>5 N`. **Fault severity = REMAINING fraction.**

## Schema v1.0 + A1 (in force)

File `Reproducibility Packet/schema/schema-v1.0.md` (rendered in `utils/schema_types.py` + `utils/estimator.py` §D). A1: `contact_state[2]`, `safety_flag[7]` (order: joint_angle_0/1, joint_speed_0/1, tip_workspace, gauge_abs, tip_contact_force), safety from privileged truth. **§D does NOT define what statistic `severity_uncertainty` is (my S24 RMS proposal, still a dev fixture, freeze open).** §A splits by whole trajectory AND whole fault setting (suite never a split input; CRN within a pair via `utils/rng.py`) — **S19 gap stands: held-out axes are sensor-seed only.** §G tracking metric `J_5s`.

## The agreed contract's load-bearing specifics

- **Sensor suites (controlled variable):** C0 = joint encoders + commanded actuation · **C1 = C0 + noisy motor-current nominal-Kt torque estimate + one distal 6-axis IMU** · **S = C1 + four fixed strain/curvature gauge stations** · O = privileged oracle.
- **Two settled correctness points:** actuator-gain fault acts *downstream* of the current proxy (C1 not handed true delivered torque); encoder fault has a *relational* signature.
- **Success bar (pre-declared, BOTH layers):** S improves held-out four-way macro-F1 over C1 by **≥0.05 absolute** (paired 95% excludes zero; every source-class recall diff lower-95% above **−0.02**) AND reduces the **5-s post-change integral of absolute tracking error by ≥10%** (`100·(J_C1−J_S)/J_C1`, paired 95% excludes zero, no safety regression) under realistic confounds. Known-class abstention = error in headline macro-F1.
- **Failure shapes:** hypothesis failure (C1+temporal adaptation matches S — clean negative) vs method failure. **Inconclusive (Slot 13):** diagnostic-only (attribution improves, control doesn't — **this is the shape the evidence keeps landing on**) · fault-specific/bounded · confound-fragile · excitation-dependent.
- **Pre-specification:** freeze gauge placement, model/hyperparams, thresholds, analysis window, seeds/scenarios before confirmatory generation. Leakage-free splits. ≥5 training seeds. Paired hierarchical bootstrap.

## Coherence worth remembering

- `utils/synchronous.py` (Codex S9) = the single shared harmonic statistic; `synchronous_coefficient_vector` + `coefficient_reference_distance` in `estimator.py` = the one canonical definition every pilot/screen/review imports.
- **Sensor RNG keyed on `(sensor_seed, pair_id, channel, stream)`** — `pair_id` load-bearing; screens reuse an upstream screen's `pair_id` verbatim and check CRN at 0.000e+00.
- **Honesty bounds (keep loud):** deployable floors are *detection*, not learned attribution; all rates from ONE fixed fault setting per class, held out over sensor noise only; abstention untestable on this fault library (min margin 0.90); one-hot prototype probabilities are NOT calibrated; **every joint-space control number comes from a condition where the structural fault causes no measurable JOINT deficit — the damage is at the tip, which the joint-space score never charges for.**

## Constraints / environment / ops (load-bearing)

- **Simulation-only, one desktop:** Windows 11, Ryzen 7 8700F (8C/16T), RTX 5060 Ti **16 GB VRAM** (Blackwell/sm_120), 32 GB RAM, Python **3.12.10** in `./venv` (use `.\venv\Scripts\python.exe` / `pip.exe`, never bare). Free/OSS, commercial-use-friendly only.
- **venv has:** numpy 2.5.1, scipy 1.18.0, scikit-learn 1.9.0, matplotlib 3.11.0, mujoco 3.10.0, pandas 3.0.3, control 0.10.2, gymnasium 1.3.0, pytest 9.1.1. **PyTorch NOT installed** — install CUDA build when building learned rungs (verify sm_120), pin immediately.
- **Running packet tests:** from `Reproducibility Packet/`, `..\venv\Scripts\python.exe -m pytest tests/`. **Running a script:** from `Reproducibility Packet/` as `..\venv\Scripts\python.exe scripts\<name>.py`. **Full packet: 329 tests green (S26).** Set `PYTHONIOENCODING=utf-8` for unicode-printing scripts.
- **Timings (measured, 8 workers):** the actuator-action screen (100 arms) ran in a handful of minutes; info review ~12–20 min; deficit ~20 min (84 arms); severity-quality ~7–9 min (80 arms). Run in background; **a pipe through `tail`/`*>` buffers until exit — poll for the results file.**
- **STANDING LESSON 1 — dry-run the analysis path before spending a rollout budget.**
- **STANDING LESSON 2 — self-audit from the row artifacts, not just read the summary** (`scratchpad/s26_audit.py` recomputed every table from the CSVs + reproduced the bootstrap; `s26_crn_and_robustness.py` checked cross-artifact CRN + baseline robustness — this is how I reviewed Codex's screen without rubber-stamping).
- **STANDING LESSON 3 — before comparing a proxy quantity to the bar, restate it in the contract's units** (`100·(J_C1−J_S)/J_C1`).
- **STANDING LESSON 4 (S26) — for the strongest review of a MuJoCo screen, re-run it to a scratch dir and diff against committed** (byte-identical = physics + analysis both reproduce; determinism/CRN in this project makes this reliable).
- **PowerShell 5.1** primary (no ternary/`??`); Bash tool also available. Use `git diff --numstat` to confirm `+N/−0` append-only after every chat turn.
- **Packet runbook uses `.\.venv\Scripts\python.exe`** (the packet's OWN self-contained venv convention) — NOT our project-root `venv`. Both correct; don't "fix" one into the other.
- **Packet `.gitignore`** ignores `*.npz` (+ caches/logs); small JSON/CSV/MD artifacts intentionally tracked. **Root `.gitignore`** covers `venv/`, `tmp/`, `MUJOCO_LOG.TXT`, caches, LaTeX aux, OS/IDE noise — verified accurate through S26 (this session added only markdown/chat files).
- **Software-engineering standard:** `argparse` (input roots defaulted project-relative in this project's screen convention; outputs default project-relative), no hard-coded paths, one purpose, shared logic in `utils/`, docstrings, prints progress, fails loud. Licensing: code MIT, prose CC BY 4.0.

## Pointers

- Claim Sheet (in-force contract): `Claim Sheet.md` · plain-language: `Accessible Claim Sheet.md` · Study Guide Pass 1: `Study Guide/Pass 1 - Conceptual Foundation.tex`
- **Shared schema (in force, +A1):** `Reproducibility Packet/schema/schema-v1.0.md`
- **My lanes:** sensor `utils/{schema_types,sensor_model,rng,synthetic_plant}.py`; eval `utils/{metrics,stats}.py`; estimator `utils/estimator.py`; synchronous floor `scripts/analyze_synchronous_detection_floor.py`; shared seam test `tests/test_recovery_seam.py`; the three severity/probability screens + tests + `results/`.
- **Codex's lane:** `utils/{cable_mechanics,cable_plant,online_loop,recovery_control,residual_baseline,task_control}.py`; `scripts/{make_mujoco_plant_trace,run_feasibility_spike,run_bounded_burst_sensitivity,screen_synchronous_safe_probe,run_bounded_noisy_information_review,screen_fault_tracking_deficit,screen_structural_recovery_action,screen_bounded_task_contact,screen_actuator_recovery_action}.py` + its tests/results.
- **Phase-2 chat:** `chats/Claude-Codex/Phase 2 Integration and Config Freeze/…- Active.md` (**2376 lines**; my S26 same-state approval = tail; **NO open loops**). Concluded chats have `Summary.md`s.
- **Monitoring chat:** `chats/Claude-Codex-Human/Transcript Order Monitoring/…- Active.md` (occurrence + clean-check notes; no action requested of Randy — answer if he replies). S26 clean, no note added.
- **CONCLUDED director chat:** `chats/Claude-Codex-Human/Better Suited Task/Better Suited Task - Concluded.md` + `Summary.md` — the withdrawn task-redesign directive. Read the `Summary.md` if the fairer-task idea ever resurfaces.
- Director requests: `director_requests.md` (root) — entry 1 (Claim Sheet review) non-blocking, awaiting director reply.
- My foundation `agents/Claude/Literature Foundation.md` · ledger `agents/Claude/references.md` (**no S20–S26 entries — reproduction/construction/measurement/review sessions, no external sources read**) · progress reports `agents/Claude/Progress Reports/` (Phase 0/1 Close, S8, S16, S24). **Next due: my S32, or a phase transition / approved amendment, whichever first.**
- Live-Run README (co-maintained): root `README.md` — **Phase 2 / In Progress**; Codex's S25 entries already log the task-redesign withdrawal + the actuator-action BLOCK; my S26 heartbeat check added nothing (confirmatory review is not a public-log event). Banner date 2026-07-23.
- Scratchpad (this session `4f62c96c…`, NOT committed): **`append_turn.py`** (binary EOF-append + gates — REUSE for every chat turn; pass an ASCII-only marker), `s26_audit.py` (recompute-from-CSV audit), `s26_crn_and_robustness.py` (cross-artifact CRN + baseline robustness), `bst_turn.md`, `phase2_turn.md`, `rerun/` (the bit-identical MuJoCo re-run output).
