# Summary of Only Necessary Context — Claude

*Rewritten every session. Restores my working context for the next session. Excludes anything already in `Project Details/Project Details.md` and `AgentPrompt.md` (I re-read those in full at session start). Last rewritten: end of Session 25, 2026-07-23 12:20 PDT.*

## Where the project is

- **Phase 2 (Execution) is OPEN.** All Phase-1 gates in force. **Schema v1.0 + Amendment A1 in force.** Contract changes run through the **amendment protocol**.
- I am **Claude**; last session was **Session 25**; next session I run is **Session 26**.
- **A MAJOR REDIRECTION is in progress (see headline below).** The director opened `chats/Claude-Codex-Human/Better Suited Task/` on 2026-07-23 and asked us to design a fairer task. **This is now the dominant thread of the project.**
- **`config.json` is deliberately NOT frozen.** Do not freeze a partial config. Role hashes are `dev-`; no `dev-` trace may enter confirmatory analysis.
- **Packet: 302 tests green** (Codex's S24 review added +3 to the class-probability screen).
- **No regular progress report due until my Session 32** — UNLESS a phase transition or an approved Claim-Sheet amendment triggers one sooner. **The pending amendment will trigger one:** whichever agent's session records the approved amendment writes a progress report at that point.

## THE HEADLINE OF S25 — the director redirected the project to a fairer task, and I opened the discussion

**Randy's directive (`Better Suited Task - Active.md`, 2026-07-23):** we have *not* fairly explored the scientific question, because the current task never lets a softening link degrade performance. He wants a task where **actuator, sensor, AND softening faults each genuinely degrade performance** — but **fair and realistic, NOT designed around the answer we're hoping for**. Both agents discuss in that chat; once agreed, one of us writes the amendment (new success/failure/inconclusive shapes, etc.); the amendment then runs a **review cycle**. Pushback allowed; "the project becoming longer is not a problem."

**I do NOT push back — the direction is correct**, and Randy, Codex (its S22 note: "require the task/fault condition to show a measurable stiffness-loss deficit before screening another structural action"), and I (my standing honesty bound: "every control-layer number comes from a condition where the structural fault causes no measurable tracking deficit") converged on this independently. My S25 turn contributed:

**1. The mechanism — why the current task hides softening.** The task and its score BOTH live in **joint space**: the `ObservedJointPDController` servos joint angles from encoder feedback, and `J_5s` integrates joint-angle error. Softening adds compliance *distal to the actuated joint*. At the task's low speeds this makes strain huge (great for detection — 13.5× at worst severity) but almost certainly **decouples the distal mass from the joint** → the joint PD tracks its reference *better*, not worse (the "−5% deficit" at EI=0.05 = joints tracked 5% better than healthy). **The damage didn't vanish — it moved to the end-effector, which the joint-space score never measures.**

**2. The fix — score the task at the END-EFFECTOR (Cartesian, under load/motion) so all three faults degrade it.** This *removes* a bias, doesn't add one: joint-space scoring was the artificial choice that hid structural faults; a Cartesian tip task is the default realistic manipulator task. Each fault then bites for an independent physical reason: softening → tip droops/lags; actuator loss → can't hold the tip against load; encoder corruption → wrong state estimate → wrong torque.

**3. THREE FAIRNESS SAFEGUARDS (against "designing around the answer" — carry these, they are the crux):**
   - **(a) C1 keeps its distal IMU.** The contract already gives C1 a distal 6-axis IMU — the honest bar is "does strain add observability *beyond a distal inertial channel*," not "beyond blind encoders." A 6-axis IMU sees much link deflection (accelerometer reads droop tilt vs gravity; gyro reads vibration). This single contract choice is what makes a tip task fair rather than rigged.
   - **(b) Don't pick the operating point that maximizes the S−C1 gap.** The trap runs *toward* a positive: the slowest quasi-static droop task flatters strain (encoders+rigid-FK fail hardest, accelerometer integrates worst). Pre-register a *realistic* operating point on engineering grounds BEFORE looking at the gap; don't sweep to widen it.
   - **(c) "All three faults degrade it" is a stop/go GATE, not a target to tune.** Verify on dev conditions that each fault at a reasonable severity produces a measurable *tip*-tracking deficit before any freeze. If softening still doesn't degrade a fair tip task, that is itself an honest result — report it, don't tune until it bites.
   - **Prior negatives stay on the record.** The joint-space screens correctly showed the joint-space task can't test the structural fault (that *motivated* the redirection). Per forward-propagation: amendment appends+dates; superseded screens get **archived, not deleted, not reopened**.

**4. Candidate tasks (Codex's plant/controller lane — I asked for its read):** (A) Cartesian setpoint-hold under payload/gravity (simplest but quasi-static → bounding sub-case only); **(B) Cartesian trajectory tracking at moderate speed (my lean — dynamic enough to keep the IMU honest);** (C) press/hold against the existing contact plane (realistic, A1 machinery exists, but adds contact confounds — defer until B settled).

**5. The tip-servo controller is the most important shared design decision.** The controller drives the tip using ONLY its own suite's observations to estimate tip position (C1: encoders+IMU through its body model; S: + strain). If it assumes a rigid link, softening makes its tip estimate wrong in a way C1 only partly sees and S sees directly — *that* is the diagnosis→control seam where the hypothesis is tested. The softening **recovery action** (update body/FK model? feed-forward the droop? re-tune for the softer link?) is genuinely different from the actuator inverse-gain action. Co-design with Codex (its recovery-controller lane + our shared seam).

**6. The amendment's shape (I'm default writer; Codex reviews):** Slot 3 (question's task clause), Slots 5 & 7 (Cartesian task + tip-servo controller + softening recovery action; `J_5s` → **Cartesian tip-error integral**, the ≥10% reduction bar now on tip error), Slot 8 (verification demo shows tip degradation+recovery), Slots 11–13 (new success/failure/inconclusive shapes; e.g. success = S improves macro-F1 AND ≥10% tip-error reduction on a task where all three faults degrade tip tracking; new *inconclusive* shape "softening degrades the tip but a distal IMU already recovers it"; the all-three-degrade stop/go gate as explicit pre-registration).

## The single most important things to do next session (Session 26)

1. **Read Codex's response in `Better Suited Task`** (it hadn't run a session on this yet as of my S25 — its HumanReport24 predates the directive). Converge on: (a) the joint-vs-tip mechanism, (b) which candidate task is cleanest on the existing MuJoCo flexible-link plant, (c) the tip-servo controller + softening recovery action, (d) any fairness gap.
2. **First shared measurement once we agree:** confirm Cartesian **tip error grows with softening** on existing rollouts even as joint error improves — the clean confirmation of the decoupling mechanism. The **tip-error metric is a small addition to my `utils/metrics.py`**; tip position comes from Codex's plant FK. (I did NOT build this in S25 — plant-side, belongs after we agree, don't pre-empt.)
3. **Write the amendment** once the task is agreed (default writer = me; Codex reviews; then review cycle; then a progress report on approval).
4. **Do NOT build the new task before convergence** (framework discipline) and **do NOT freeze a partial config.**
5. **Deferred, still blocked (do NOT build early):** learned attribution rungs (`TemporalAttributionNet` + `RMALatentEncoder`) — need PyTorch CUDA build (verify sm_120), frozen config, confirmatory data; the §D deployable-loader leakage test + whole-trajectory/fault-setting split audit — need real multi-run storage; the eval **driver** ([t_c, t_c+5 s] slicing → paired C1-vs-S control comparison) — needs frozen data layout. **These are now further downstream: the task/metric changes first.**

## Review-cycle state (all loops CLOSED)

- **NO open review loops in the Phase-2 chat.** The class-probability loop closed at my S25 same-state approval. Do not reopen.
- **What I did to close it (S25):** re-ran full packet (**302 green**) + focused (**54 green**); read the corrected `sampled_pair_extremes` (now searches every ordered pair, not just endpoints — the max pair `(0.50,1.00)` is now *verified* by monotonicity, not assumed); confirmed the interior-max regression genuinely fails the old endpoint-only code; confirmed `arm_grid_complete` is a required fail-loud gate; confirmed no number moved and the doc corrections are append-only/honest. **I approved same-state, no edits.**
- **I AGREE with Codex's two corrections (they narrowed MY overclaims):**
  - **(1) Continuous ≠ sampled.** The *input* multiplier set `[1.50,2.00]` is genuinely closed by constants; the *response* `J_5s(p)` is a nonlinear rollout output that 6 (or Codex's 84-point 0.025 audit) samples characterize *empirically*, not exactly. "Reachable set" was right for the input, wrong for the response. → **"sampled empirical response envelope."**
  - **(2) The actuator class is NOT closed.** The fixture isolates graded probability *by* forcing both suites to agree on class/loc/severity/uncertainty/abstention — so it CANNOT speak to calibrated *authorization*. The **10.82 pp gate-crossing in my own rows** is exactly that unmeasured channel (worth more than the bar). "Fourth and final channel" / "actuator class closed" are RETRACTED.
- **This convergence with Randy's directive is the point:** both say the current task never makes the two suites *diverge* in a way a controller can spend.

## MONITORING DUTY (standing)

- **S25 check CLEAN** — Codex's S24 turn was a verified **+91/−0 tail append** (git-level). Third consecutive clean append. **I did NOT post to `Transcript Order Monitoring`** (duty is to flag *recurrences*; the thread stays lean). Flag only on recurrence.
- **REUSE `scratchpad/append_turn.py`** for every chat turn: **binary EOF-append** (structurally immune to the mid-file-insertion bug, which came from patch-anchor tools) + 5 hard gates (prefix-identical, unique header, header-after-boundary, Claude-last, +N line delta). **Pass an ASCII-only unique marker** (e.g. the timestamp) as the header arg to avoid em-dash argv encoding issues; let the last-line gate default to "— Claude". It now handles a missing trailing newline as a transparent byte-level pure append (git shows a cosmetic −1/+1 on the prior last line only). *(The `Better Suited Task` file lacked a trailing newline — Randy's message — so my BST append shows +52/−1, all content preserved.)*

## The corrected probability-screen numbers (for reference; class NOT closed)

At the selected condition `actuator_gain_remaining_0p25`, cap 2: severity channel structurally flat (`capped = min(1/max(ŝ,0.25),2.0)` = 2.0 for every ŝ ≤ 0.50; true 0.25 is 24.6× the recorded error scale below the boundary). Probability is the only live graded channel there; `m = 1 + p`.

| paired quantity (contract units `100·(J_C1−J_S)/J_C1`) | worst | mean | vs 10 pp bar |
|---|---:|---:|---|
| **graded** (both past the gate) — SAMPLED ENVELOPE | 5.0699 pp | 5.0162 pp | below |
| gate-crossing (one withholds) — AUTHORIZATION, not precision | 10.8509 pp | 10.8204 pp | clears |

Cap realization at 0.25 = **57.5%** of the analytic ceiling (vs 93.2% at 0.50) — cap-saturated (restoration needs m=4, cap allows 2). `maximum_gain_compensation` is the binding limit on recoverable tracking at that condition; `(maximum_gain_compensation, minimum_gain_remaining, source_probability_threshold)` is a JOINT surface. RMS-not-std for `severity_uncertainty` stands as a *development fixture* (not a frozen per-example statistic — Codex agrees; the freeze remains open).

## THE STRUCTURAL RESULT — now the CORE of the redirection argument (Codex's S20 rows)

| remaining EI | mean peak \|gauge\| | mean **joint** tracking deficit |
|---:|---:|---:|
| healthy | 19.2 µε | — |
| 0.75 | 25.0 µε | +0.11% |
| 0.50 | 38.4 µε | +0.08% |
| 0.25 | 72.4 µε | −0.89% |
| 0.10 | 152.8 µε | −2.23% |
| 0.05 | 259.7 µε | −5.00% |

**Monotone in information; monotone the WRONG way in joint control.** 13.5× the healthy strain signature at the severity where *joint* tracking is 5% *better* than healthy. **Read correctly: the damage moved from the joint to the tip.** This is the sentence the redirection is built on — and the tip-error confirmation (next session) is what nails it.

## The control-layer shape table (recorded; what the redesign must change)

From Codex's `bounded_noisy_information_review/summary.json`:

| source | C1 gate state | S gate state | S exclusive info? | `s_tracking_change_pct` |
|---|---|---|---|---:|
| healthy | correct_no_action | correct_no_action | no | 0.0000% |
| **structure** | withheld_actionable | correct_actionable | **YES** | **−18.5762%** |
| actuator | correct_actionable | correct_actionable | no | 0.0000% |
| sensor | correct_no_action | correct_no_action | no | 0.0000% |

C1 per-class recall: structure **0.083**, actuator 1.000, sensor 1.000 (S: 1.000 all). **On the CURRENT task: where S has exclusive info there's no control headroom; where there's headroom S has no exclusive info.** The redirection's entire purpose is to build a task where the structural row has BOTH exclusive info AND recoverable tip-tracking headroom. *(The −18.6% was a structural derate that made joint tracking worse; on a tip task the softening recovery action is different.)*

## My lanes — current state

`Reproducibility Packet/scripts/utils/estimator.py`:
- **`WindowFeatureExtractor(window_steps=W=768, probe_frequency_hz=0.8)`**: `[W,D]` left-padded + per-column `[last,mean,std,slope,sync_cos,sync_sin,sync_amplitude,valid_fraction]` over 18-col registry → 144 features. Constants: `N_FEATURE_STATS=4`, `N_EXTRA_FEATURES=4`, sync cols 4/5/6, `VALID_FRACTION_COL=7`, `DIAGNOSTIC_PROBE_HZ=0.8`, `MIN_SYNC_SAMPLES=8`.
- **`WindowNoveltyDetector`** (detect+abstain) · **`CoefficientReferenceDetector`** (second interpretable detection rung; canonical `synchronous_coefficient_vector` + `coefficient_reference_distance`; `fit_reference` atomic; `calibrate_threshold` fail-loud below `ceil(min_tail/far)`) · **`_SCORE_STD_FLOOR=1e-3`** shared (no-op on every artifact) · **`SeverityRidgeHead`** (deployable severity read-out; suite-agnostic; `train_residual_std` is IN-SAMPLE — never feed a confidence gate) · **`leave_one_group_out_residuals`** (CALIBRATION-role diagnostic per Codex's S23 correction; group by sensor seed) · **`OracleInterface(onset_time_s)`** (causal privileged ceiling) · **`EstimatorCommandPolicy`** (seam adapter; runs estimator every `stride`, ZOHs the OUTPUT, calls `recovery_command` every step) · `RECOMMENDED_WINDOW=(768,16)` pilot proposal · learned rungs specified-not-built.
- **`utils/metrics.py` + `utils/stats.py`** (jointly approved through S11): `tracking_reduction_pct = 100·(J_C1−J_S)/J_C1` (C1 in denominator), `j_5s` fail-loud guard on the full `[t_c,t_c+5s]` window, `safety_incident_rate` (threshold-count, can't score graded margins), `safety_regression_delta` (matched `[T,7]` guard). **NEXT: a Cartesian tip-error metric will be added here once the task is agreed and Codex's plant exposes tip position.** Eval **driver** (argparse CLI owning the exact slice) — build once frozen data layout exists.
- **Screens (all jointly approved/closed; SUPERSEDED-PENDING-AMENDMENT as control-question evidence, but valid joint-space measurements — archive when amendment lands, don't delete/reopen):** `screen_severity_estimation_quality.py` (80 arms; held-out MAE C1 0.0065/S 0.0076; `window_features.csv` durable), `screen_severity_action_boundary.py` (40 arms; paired −0.1177% mean/0.5154% worst), `screen_actuator_probability_channel.py` (36 arms; the corrected sampled-envelope result above). `tests/test_recovery_seam.py` (shared mechanism regression, 4 tests, unchanged S14–S25).

## Codex's lanes — current state

- `screen_fault_tracking_deficit.py` + `results/fault_tracking_deficit_screen/` (CLOSED S22): no-recovery severity sweep. **Gate: `required_reduction_pct`=12%, `required_deficit_pct`=R/(1−R)=13.636%.** Selection = `actuator_gain_remaining_0p25` (mean deficit 23.16%). **The structural rows produced NO deficit (turned negative) — this is the direct evidence Randy is responding to.**
- `utils/recovery_control.py` — `GainScheduledRecoveryController`. `_confident_source` gate = not abstained AND unique argmax==source AND p ≥ `source_probability_threshold`=0.5 AND finite uncertainty ≤ `maximum_severity_uncertainty`=0.25. Actuator branch: `multiplier = 1 + probability*(capped_compensation − 1)`. **Load-bearing constants: `maximum_gain_compensation=2.0`, `minimum_gain_remaining=0.25`, `source_probability_threshold=0.5`, `torque_abs_limit=(1.0,0.5)`, `maximum_severity_uncertainty=0.25`.** *(Drive directly with a small nominal like `[0.01,0.02]` — `torque_abs_limit` clips a unit nominal.)*
- `screen_structural_recovery_action.py` (CLOSED S20): `BLOCK_STRUCTURAL_RECOVERY_ACTION_FAMILY`; ~70% of benefit at the *unfaulted* joint; −0.263 pp specificity margin sign not established. **The softening recovery action needs a fresh design on the tip task.**
- `run_bounded_noisy_information_review.py` (CLOSED S19): S PASSES info+action gates (macro-F1 0.995, 100% per-fault detection, 2.1% FA); C1 BLOCKS (0.704, 8.3% structural recall). One-hot mechanism probabilities (p=1, NOT calibrated).
- `utils/task_control.py` (S17/S18): `BoundedTaskProfile` (rest→(0.30,0.30) rad by 3.0s→hold→rest by 5.0s — **JOINT-SPACE targets; this is what changes**), `ObservedJointPDController` (kp (0.05,0.03), kd (0.005,0.003), torque limits (0.20,0.10); reads ONLY `q_obs`/`qd_obs` — **a tip-servo controller replaces/augments this**).
- `utils/cable_mechanics.py` + `utils/cable_plant.py` + `make_mujoco_plant_trace.py` (S14/S15): A1 safety flags = `|q|>π`, `|qd|>10`, 3-D tip radius >0.82 from `[0,0,0.5]`, `max|gauge|>500 µε`, `contact_state[0]>5 N`. **Fault severity = REMAINING fraction** (remaining EI / remaining gain). **The plant already computes 3-D tip position for the workspace safety flag → tip position IS available for a Cartesian metric.**

**Codex's queued "actuator action screen" is very likely SUPERSEDED by the redirection — settle the task first.**

## Schema v1.0 + A1 (in force)

File `Reproducibility Packet/schema/schema-v1.0.md` (rendered in `utils/schema_types.py` + `utils/estimator.py` §D). A1: `contact_state[2]`, `safety_flag[7]` (order: joint_angle_0/1, joint_speed_0/1, tip_workspace, gauge_abs, tip_contact_force), safety from privileged truth. **§D does NOT define what statistic `severity_uncertainty` is (my S24 RMS proposal, still a dev fixture, freeze open).** §A splits by whole trajectory AND whole fault setting (suite never a split input; CRN within a pair via `utils/rng.py`) — **S19 gap stands: held-out axes are sensor-seed only.** §G tracking metric `J_5s` — **this is what the amendment relocates to the tip.**

## The agreed contract's load-bearing specifics

- **Sensor suites (controlled variable):** C0 = joint encoders + commanded actuation · **C1 = C0 + noisy motor-current nominal-Kt torque estimate + one distal 6-axis IMU** · **S = C1 + four fixed strain/curvature gauge stations** · O = privileged oracle. *(C1's distal IMU is the fairness anchor for the tip-task redesign. C0 carrying commanded actuation is why C1 nails actuator severity.)*
- **Two settled correctness points:** actuator-gain fault acts *downstream* of the current proxy (C1 not handed true delivered torque); encoder fault has a *relational* signature.
- **Success bar (pre-declared, BOTH layers) — the tracking layer moves to the tip via amendment:** S improves held-out four-way macro-F1 over C1 by **≥0.05 absolute** (paired 95% excludes zero; every source-class recall diff lower-95% above **−0.02**) AND reduces the **5-s post-change integral of absolute tracking error by ≥10%** (`100·(J_C1−J_S)/J_C1`, paired 95% excludes zero, no safety regression) under realistic confounds. Known-class abstention = error in headline macro-F1.
- **Failure shapes:** hypothesis failure (C1+temporal adaptation matches S — clean negative) vs method failure. **Inconclusive (Slot 13):** diagnostic-only (attribution improves, control doesn't — *this was the near-certain landing on the joint-space task; the redirection reopens the control question on a fair task*) · fault-specific/bounded · confound-fragile · excitation-dependent.
- **Pre-specification:** freeze gauge placement, model/hyperparams, thresholds, analysis window, seeds/scenarios before confirmatory generation. Leakage-free splits. ≥5 training seeds. Paired hierarchical bootstrap.

## Coherence worth remembering

- `utils/synchronous.py` (Codex S9) = the single shared harmonic statistic; `synchronous_coefficient_vector` + `coefficient_reference_distance` in `estimator.py` = the one canonical definition every pilot/screen/review imports.
- **Sensor RNG keyed on `(sensor_seed, pair_id, channel, stream)`** — `pair_id` is load-bearing; screens reuse an upstream screen's `pair_id` verbatim and check it at 0.000e+00 (CRN).
- **Contact + the 7th safety flag:** contact reaches deployable suites only through motion/strain; NOT suite-invariant in closed loop. Design constraint (my S15 note, honored since): apply the contact profile identically across each matched C1/S CRN pair. *(With NO action + a PD controller reading only q_obs/qd_obs, an S rollout and its C1 projection are bit-identical — 0.000e+00.)*
- **Honesty bounds (keep loud):** deployable floors are *detection*, not learned attribution; all rates from ONE fixed fault setting per class, held out over sensor noise only; abstention untestable on this fault library (min margin 0.90); one-hot prototype probabilities are NOT calibrated; **every joint-space control number comes from a condition where the structural fault causes no measurable JOINT deficit — which is exactly what the redirection fixes by moving to the tip.**

## Constraints / environment / ops (load-bearing)

- **Simulation-only, one desktop:** Windows 11, Ryzen 7 8700F (8C/16T), RTX 5060 Ti **16 GB VRAM** (Blackwell/sm_120), 32 GB RAM, Python **3.12.10** in `./venv` (use `.\venv\Scripts\python.exe` / `pip.exe`, never bare). Free/OSS, commercial-use-friendly only.
- **venv has:** numpy 2.5.1, scipy 1.18.0, scikit-learn 1.9.0, matplotlib 3.11.0, mujoco 3.10.0, pandas 3.0.3, control 0.10.2, gymnasium 1.3.0, pytest 9.1.1. **PyTorch NOT installed** — install CUDA build when building learned rungs (verify sm_120), pin immediately. *(S22–S25 all used no new dependency — closed-form numpy on purpose.)*
- **Running packet tests:** from `Reproducibility Packet/`, `..\venv\Scripts\python.exe -m pytest tests/`. **Running a script:** from `Reproducibility Packet/` as `..\venv\Scripts\python.exe scripts\<name>.py`. **Full packet: 302 tests green (S25).** Set `PYTHONIOENCODING=utf-8` for unicode-printing scripts.
- **Timings (measured, 8 workers):** info review ~12–20 min; structural-action ~8 min; deficit ~20 min (84 arms); severity-quality ~7–9 min (80 arms); severity-boundary ~7 min (40 arms); probability ~6 min (36 arms). Run in background; **a bash pipe through `tail` buffers until exit — poll for the results file.**
- **STANDING LESSON 1 — dry-run the analysis path before spending a rollout budget** (`scratchpad/s24_dryrun.py` template: every derived table + artifact write + audit gate forced false, on synthetic rows, in seconds).
- **STANDING LESSON 2 — self-audit the PROSE, not just numbers** (`scratchpad/s24_selfaudit.py` template: recompute every table from `arm_rows.csv`, grep the report for overreach patterns + presence of the constants that justify each claim — it caught a real one).
- **STANDING LESSON 3 (S25) — before comparing a proxy quantity to the bar, restate it in the contract's units** (`100·(J_C1−J_S)/J_C1`, C1 denominator); a difference of two no-action reductions understates by `1/(1−r_low/100)`.
- **PowerShell 5.1** (no ternary `?:`, no `??`) is the primary shell; Bash tool also available. `git diff` won't show *untracked* files (the `Better Suited Task` folder was untracked until my S25 commit added it).
- **Packet runbook uses `.\.venv\Scripts\python.exe`** (the packet's OWN self-contained venv convention for an outside reader) — NOT our project-root `venv`. Both correct; don't "fix" one into the other.
- **Packet `.gitignore`** ignores `*.npz` (+ caches/logs); small JSON/CSV/MD artifacts intentionally tracked. **Root `.gitignore`** covers `venv/`, `tmp/`, `MUJOCO_LOG.TXT`, caches, LaTeX aux, OS/IDE noise — verified accurate through S25.
- **Software-engineering standard:** `argparse` with `required=True` for input roots (defaulted project-relative outputs), no hard-coded paths, one purpose, shared logic in `utils/`, docstrings, prints progress, fails loud. (`utils/` + `tests/` are the import-not-CLI exception.)
- **Licensing:** code MIT, prose CC BY 4.0.

## Pointers

- Claim Sheet (in-force contract): `Claim Sheet.md` · plain-language: `Accessible Claim Sheet.md` · Study Guide Pass 1: `Study Guide/Pass 1 - Conceptual Foundation.tex`
- **Shared schema (in force, +A1):** `Reproducibility Packet/schema/schema-v1.0.md`
- **My lanes:** sensor `utils/{schema_types,sensor_model,rng,synthetic_plant}.py`; eval `utils/{metrics,stats}.py`; estimator `utils/estimator.py`; synchronous floor `scripts/analyze_synchronous_detection_floor.py`; shared seam test `tests/test_recovery_seam.py`; the three severity/probability screens + their tests + `results/`.
- **Codex's lane:** `utils/{cable_mechanics,cable_plant,online_loop,recovery_control,residual_baseline,task_control}.py` + its scripts/tests/results.
- **THE ACTIVE DIRECTOR THREAD:** `chats/Claude-Codex-Human/Better Suited Task/Better Suited Task - Active.md` — Randy's task-redesign directive + my S25 opening turn. **Read Codex's reply first next session.**
- **Phase-2 chat:** `chats/Claude-Codex/Phase 2 Integration and Config Freeze/…- Active.md` (**2316 lines**; my S25 owner re-review = tail; **NO open loops**). Concluded chats have `Summary.md`s.
- **Monitoring chat:** `chats/Claude-Codex-Human/Transcript Order Monitoring/…- Active.md` (occurrence notes + clean-check notes; no action requested of Randy — but answer if he replies). S25 clean, no note added.
- Director requests: `director_requests.md` (root) — entry 1 (Claim Sheet review) non-blocking, awaiting director reply.
- My foundation `agents/Claude/Literature Foundation.md` · ledger `agents/Claude/references.md` (**no S20–S25 entries — reproduction/construction/measurement/discussion sessions, no external sources read**) · progress reports `agents/Claude/Progress Reports/` (Phase 0/1 Close, S8, S16, S24). **Next due: my S32, or the amendment's approval, whichever first.**
- Live-Run README (co-maintained): root `README.md` — **Phase 2 / In Progress**; my S25 entry logs the redirection (as a pivot) + the probability-loop closure. Banner date 2026-07-23.
- Scratchpad (not committed, session `6b37122a…`): **`append_turn.py`** (binary EOF-append + 5 gates + trailing-newline handling — REUSE for every chat turn), `phase2_turn.md`, `bst_turn.md`. Earlier-session probes under `26d971b9…` (S24: `s24_dryrun.py`, `s24_selfaudit.py`, `s24_verify.py`), `02c1e7b4…` (S23), `968ad429…` (S20–S21).
