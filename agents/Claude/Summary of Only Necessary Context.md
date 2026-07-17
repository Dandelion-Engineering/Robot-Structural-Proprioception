# Summary of Only Necessary Context — Claude

*Rewritten every session. Restores my working context for the next session. Excludes anything already in `Project Details/Project Details.md` and `AgentPrompt.md` (I re-read those in full at session start). Last rewritten: end of Session 8, 2026-07-17.*

## Where the project is

- **Phase 2 (Execution) is OPEN.** All Phase-1 gates closed and in force (Claim Sheet, Accessible Claim Sheet, Study Guide Pass 1, schema v1.0). Contract changes run through the **amendment protocol**, not casual editing.
- I am **Claude**; last session was **Session 8**; next session I run is **Session 9**.
- **Session 8 was my progress-report session (done).** Next regular director progress report: **my Session 16.** (Phase-0-close, Phase-1-close, and Session-8 reports exist; they don't reset the per-agent counter.)
- **Both Phase-2 review-cycle loops are now CLOSED** (evaluation core + online interface) at the same state Codex approved — I re-reviewed against the contract, reproduced the evidence independently, and approved. No open review loops right now.

## What I did this session (Session 8)

1. **Closed both open review loops** Codex handed me at the end of S7 (genuine owner re-review — read diagnoses + implementations, reproduced evidence, then same-state approval):
   - **Evaluation core** (`metrics.py`, `stats.py`): Codex's **four** corrections are all correct in diagnosis + implementation. (a) `j_5s` now fails loud on a truncated window; (b) risk–coverage emits only tie-group endpoints (order-invariant); (c) **OOD operating point** = false-acceptance at **95% unknown-detection sensitivity** (Claim Sheet line 118) — my S7 `false_accept_at_id_acceptance` was wrong; corrected to `unknown_threshold_at_sensitivity` (validation) → `ood_false_acceptance_rate` (held-out); (d) bootstrap is **crossed** `pair_id × train_seed` (seed is a global axis, not nested), rectangular grid required. I **verified (c) against the Claim Sheet directly** and reproduced all four with an independent script.
   - **Online interface** (`schema_types.py` step adapter, `sensor_model.py` `OnlineSensorSession`, `online_loop.py`): causally correct (decision uses `plant.data.time` *before* advance; obs emitted *after*), CRN-consistent, latency-enforcing, one authoritative pathology path. Approved same state.
   - Independent verification: full packet **59 passed** + a standalone 17-check script (scratchpad `s8_reverify.py`) touching each load-bearing claim of both loops. All passed.
2. **Built my next deliverable: the diagnosis-estimator lane** (`utils/estimator.py` + `tests/test_estimator.py`). Packet **59 → 74 tests**. Details below.
3. **Added `coverage_at_risk` to `metrics.py`** — a Claim Sheet line-118 metric ("coverage at a pre-registered 5% selective-error ceiling") that was unrendered. Forward fix in my file, hand-computed test.
4. **Proposed `W=512` / `stride=8`** (the last estimator-side config-freeze field).
5. Session closeout: S8 chat turn (both approvals + estimator + W/stride + updated freeze table), references (S8 estimator-lane mapping + forward corrections), Live-Run README running-log line, my README, this rewrite, **Session-8 progress report**, human report, git.

## The estimator lane I built (Session 8) — reference for next builds

File `Reproducibility Packet/scripts/utils/estimator.py` (+ `tests/test_estimator.py`):
- **`EstimatorOutput`** (§D contract, validated): `p_class[4]`, `unknown_score`, `abstain_decision`, `location_out`, `severity_out`, `severity_uncertainty`, `detection_time_s` (+ `step`, `decision_time_s` bookkeeping). Class order `("healthy","structure","actuator","sensor")` == `metrics.SOURCE_CLASS_ORDER` (asserted). **`EstimatorTrace`** stacks per-decision outputs into the §E `estimator_outputs/<suite>` role + run-level reductions (`detection_time_s`, `final_p_class`, `final_abstain`, `final_unknown_score`, `stack()`).
- **`WindowFeatureExtractor`** — past-only window front-end, **suite-agnostic** (fixed shapes over the full 18-wide registry for C0/C1/S): `window_tensor(record) -> (values[T,D], valid[T,D])` (NaN→0 fill + validity, for learned rungs); `window_features(record) -> [D*(4+1)]` summary vector (per-column last/mean/std/slope + valid-fraction, for the interpretable rung). Consumes exactly the `available_record` window Codex's `OnlineSensorSession` exposes.
- **`WindowNoveltyDetector(DiagnosisEstimator)`** — the interpretable **detection + calibrated-abstention** rung (my lane). Fits a healthy reference (per-feature mean/std) + **leave-one-out healthy score calibration** so thresholds read in **sigma-above-healthy** (robust to feature dim). Score = mean of `top_k=8` largest per-feature |z| (sparse-change statistic; RMS-over-all dilutes a localized fault). `detect_threshold=4.0`, `abstain_threshold=2.5` sigma, `persistence=3` (latches `detection_time_s`). Honest output: healthy-vs-not simplex (logistic in the score), **abstains on the fault *type*** and spreads non-healthy mass uniformly — **makes NO source attribution** (that needs the trained head). `location_out=-1`, `severity` unset. Deliberately NOT Codex's residual/linear-sysID baseline (that's a physics residual in the plant lane); this is an observation-statistics gate. Requires `fit_reference([healthy ObservedRecord…])` before scoring.
- **`OracleInterface`** — the separate allowlisted §D oracle `O`; takes privileged `PlantStepState` explicitly (boundary visible in signature), never importable by a deployable loader; returns perfect-knowledge output from the true source index.
- **`EstimatorCommandPolicy`** — adapts (estimator + injected `recovery_command` callback) to the `run_online_rollout` `CommandPolicy` signature `(step_index, decision_time_s, available) -> command`; accumulates the §D trace; runs the estimator every `stride` decisions (zero-order hold between). **Recovery controller stays Codex's lane**; default `passive_command` = zero torque.
- **`RECOMMENDED_WINDOW`** = `W=512` (~1.02 s @ 500 Hz, ~ the 1.25 s / 0.8 Hz diagnostic period), `stride=8` (62.5 Hz diagnosis under 500 Hz ZOH controller). Config-freeze-time, not pilot-blocking; pilot sweep `W∈{256,512,768}`, `stride∈{4,8,16}` offered.

## The single most important thing to do next session (Session 9)

**Advance Phase-2 execution — build the learned attribution rungs and coordinate the config freeze.** Priority order:

1. **Build the learned rungs** (my lane, share the `WindowFeatureExtractor.window_tensor` front-end + `EstimatorOutput` contract + `DiagnosisEstimator` interface):
   - **Matched temporal-attribution net** — shared temporal encoder over `[W, D]` (dilated temporal-conv / GRU) → class/unknown/location/severity heads. The headline method; produces the full §D output (not just detection).
   - **RMA-style latent baseline** — encoder mapping the same `[W, D]` history → adaptation latent for the recovery policy (adapt-without-attribution control comparison).
   - **These need PyTorch** — install the CUDA build (RTX 5060 Ti = Blackwell/sm_120 → needs a recent torch/CUDA-12.8+ wheel; verify `torch.cuda.is_available()` AND that a kernel actually runs on sm_120, not just that CUDA loads). Pin it in the packet `requirements.txt` the moment it installs. **Training itself waits on the config freeze + confirmatory data** — build architecture + forward/backward + shape tests now if useful, but do NOT report performance before frozen data exists.
2. **Config-freeze coordination (needs Codex).** My estimator column is now filled (`W`/stride proposed). Remaining open: Codex's diagnostic **duration/envelope** + contact/safety **widths/thresholds**; shared **severity/onset grids** (pilot-informed); joint sanity-check of the non-load-bearing `SensorConfig` constants. **Do not freeze a partial config** — immutable once frozen (before pilot/confirmatory generation). Check Codex's reply to my S8 chat turn.

**Deferred deliberately (post-config-freeze, before pilot/confirmatory generation — they need real multi-run storage to bite):** the **§D deployable-loader leakage test** and the **whole-trajectory/fault-setting split audit**. Must fail the build if a deployable loader reaches identity manifest / privileged / labels / other-suite arrays. Also the estimator's **location/severity heads** get real content with the trained net.

## Coordination state (chats)

- **Active Phase-2 chat:** `chats/Claude-Codex/Phase 2 Integration and Config Freeze/…- Active.md`. **My S8 turn is the physical tail** (posted 16:12 PDT): same-state approval of both loops, independent verification, estimator delivery, `W`/stride proposal, `coverage_at_risk` note, updated config-freeze table. **Codex has not replied to my S8 turn yet — check it next session.**
- **MONITORING DUTY IS STANDING:** if I ever see a reply land anywhere but the physical end of a transcript, flag it in `Claude-Codex-Human`. (I append via `>>` and verify the tail — did so S8.)
- **Config-freeze items still open** (from my S8 table): diagnostic **duration/envelope** (Codex — gate validated continuous 3-s sinusoid; preserve into pilot or run bounded-burst sensitivity), contact/safety **widths + thresholds** (Codex — zero-width in dev), severity/onset grids (shared, pilot-informed), non-load-bearing sensor pathology constants (mine — jointly sanity-check). **Settled:** `f_ctrl=500`, `dt=0.002`, sim step `1e-4`, `n_def=90`, 4 gauge stations, diagnostic `1.0 N`/`0.8 Hz`, **`W=512`/`stride=8` (proposed S8)**.
- **Non-blocking forward item (carry to Technical Report):** Hendriks et al. 2022 split-leakage cautionary case → Technical Report methods rationale for the whole-group split. In both ledgers.

## Schema v1.0 mental model (in force; rendered in `utils/schema_types.py` + now `utils/estimator.py` for §D)

File: `Reproducibility Packet/schema/schema-v1.0.md`. Read `schema_types.py` (renders §B/§0/§C/§E dataclasses; lossless `PlantStepState`) + `estimator.py` (renders §D estimator outputs) alongside it.
- **§A identity/pairing/splits:** `scenario_spec_id` (shared in pair) · `pair_id` (matched C1-vs-S) · `run_id`. Identity manifest **non-deployable**. Splits by whole trajectory AND whole fault setting; **suite never an input to the split**; enforced by an executable pre-fit audit (to build, post-freeze). **CRN within a pair:** shared seeds + deterministic substreams keyed by (pair_id, channel, step) — `utils/rng.py`.
- **§B privileged plant record** (per run, control grid): q/qd/qdd_true, tau_cmd (pre-limit), **control_effort** (saturated, pre-fault — what the proxy senses), **tau_delivered_true** (post-fault), deform_coords[90], curvature_true[4], gauge_true[4] µε, imu_true[6], temperature_true[4], contact_state, task_reference + **true_task_output (deformed tip)** + tracking_error(+norm), control_effort/saturation/safety. **`PlantStepState` carries ALL (lossless); `observable_sources()`/`observable_step_sources()` expose only the measurable subset.**
- **§C observed record** (deployable suites, fixed 18-col registry, unavailable = NaN): corrupted q_obs + causal qd_obs, tau_cmd, current_proxy_obs (C1/S; noisy nominal-Kt current, **upstream** of gain loss), imu_obs (C1/S), **4 signed surface-strain gauge_obs (S only)**. Static `suite_available_mask`; per-time-per-channel `valid_mask` + measurement/availability/latency timing. **`OnlineSensorSession` is the authoritative stateful path; `available_record(decision_time, history_steps)` = the past-only, availability-masked, bounded window the estimator reads.**
- **§D labels/outputs/causality/leakage:** labels stored separately (only bridge from truth to target). **Estimator outputs (now rendered in `EstimatorOutput`):** `p_class[4]`, `unknown_score`, `abstain_decision`, `location_out`, `severity_out`, `severity_uncertainty`, `detection_time_s`. Controller logs separate. **Automated leakage test fails the build** if a deployable loader reaches identity manifest/privileged/label/other-suite arrays (to build, post-freeze). Past-only windows. **O = separate allowlisted oracle interface (now `OracleInterface`).**
- **§E storage:** non-deployable `manifest.csv` + per-role roots/indexes (`plant/`, `observations/<suite>/`, `labels/`, `estimator_outputs/<suite>/`, `controller_logs/<suite>/`); each index carries `run_id, schema_version, config_hash, npz_path, sha256`; observation index also carries safe `split`. One non-pickled `.npz` per rollout per role. Immutable `schema.json`/`config.json`.
- **§F frozen constants:** f_ctrl, dt, **W, stride** (proposed 512/8), onset convention, `[t_c,t_c+5s]` — names/rules in schema, **values in `config.json`**, frozen before confirmatory generation.
- **§G tracking metric:** `J_5s = ∫‖e(t)‖dt`, e = task_reference − **true deformed tip**, planar (x,y), metres, **L2**, control-grid, **trapezoidal**, m·s. Bar = ≥10% reduction vs C1 (paired 95% interval excludes zero, no safety regression). **Rendered in `utils/metrics.j_5s` (truncation-guarded).**
- **§H deliberately open** (set in frozen config): gauge locations (=4 stations), n_def (=90), numeric f_ctrl/W/stride, severity grids/onset distribution, diagnostic-excitation budget.

## The agreed contract's load-bearing specifics (carry this)

- **Sensor suites (the controlled variable):** **C0** = joint encoders + commanded actuation · **C1** = C0 + noisy motor-current nominal-Kt torque estimate + one distal 6-axis IMU · **S** = C1 + **four fixed strain/curvature gauge stations** · **O** = privileged oracle. External pose/vision and true delivered torque excluded from deployable suites.
- **Two settled correctness points (implemented + verified):** (1) actuator-gain fault acts *downstream* of the current proxy → C1 not handed true delivered torque; (2) encoder (sensor) fault has a *relational* signature — a lying sensor doesn't deform the structure; identified by disagreement between corrupted encoder and independently-evolved gauge/physical history (analytical redundancy).
- **Success bar (pre-declared, BOTH layers required):** S improves held-out four-way **macro-F1 over C1 by ≥0.05 absolute** (paired 95% interval excludes zero; every source-class recall difference lower-95%-bound above **−0.02**) **and** reduces the **5-s post-change integral of absolute tracking error by ≥10%** (paired interval excludes zero; no safety regression), **under realistic confounds**. Known-class abstention scored as error in headline macro-F1; calibration/selective/OOD reported separately. **All rendered in `utils/metrics.py` + `utils/stats.py` (crossed bootstrap).**
- **Failure shapes:** *hypothesis failure* (C1+temporal adaptation matches S — clean negative) vs *method failure* (spike can't produce differential signatures / algebraic echo / leakage). **Inconclusive shapes:** diagnostic-only · fault-specific/bounded · confound-fragile · excitation-dependent.
- **Pre-specification:** bars fixed before the pilot; the pilot sizes the test, not the bar. Freeze gauge placement, model/hyperparams, class+abstention thresholds, analysis window, seeds/scenarios in the versioned config before confirmatory generation. Leakage-free splits. ≥5 training seeds. Paired hierarchical bootstrap.

## Labor split (agreed, unchanged)

- **Codex:** feasibility spike + physics (MuJoCo cable/rod done → `CablePlant` producer + online loop done; PyElastica fallback + independent beam/Cosserat validation), virtual-gauge extraction, excitation design, interpretable residual/linear-sysID baseline, recovery controller (gain-scheduling/MPC).
- **Claude (me):** fault-injection + sensor-realism model (**done S6**, jointly approved S7), two-layer evaluation harness + metrics + stats (**core done S7, corrected+approved S8**; leakage test + split audit deferred post-freeze), **diagnosis-estimator front + window contract + oracle + seam adapter (done S8)**, matched temporal-attribution net + RMA latent (**next, needs torch + frozen data**), Slot-8 verification demo, default-writer artifacts (Technical Report, Accessible Piece, Study Guide Pass 2 — Codex reviews).
- **Shared:** the plant→signals→estimator schema (in force), fault library, Reproducibility Packet, references reconciliation (Phase 2). The **"does attribution improve control" headline experiment is shared** at the diagnosis→control seam (my `EstimatorCommandPolicy` is the socket; Codex's recovery controller is the injected command).

## Constraints / environment (unchanged, load-bearing)

- **Simulation-only, one desktop:** Windows 11, Ryzen 7 8700F (8C/16T), RTX 5060 Ti **16 GB VRAM** (Blackwell/sm_120), 32 GB RAM, Python **3.12.10** in `./venv` (use `.\venv\Scripts\python.exe` / `pip.exe`, never bare). Free/OSS, commercial-use-friendly only.
- **venv has:** numpy 2.5.1, scipy 1.18.0, scikit-learn 1.9.0, matplotlib 3.11.0, mujoco 3.10.0, pandas 3.0.3, control 0.10.2, gymnasium 1.3.0, pytest 9.1.1. **Packet `requirements.txt` pins matplotlib/mujoco/numpy/pytest/scikit-learn.** **PyTorch NOT installed** — install CUDA build when building the learned rungs (verify sm_120 kernel actually runs), pin immediately.
- **Packet `.gitignore` ignores `*.npz`** (and caches/logs) — demo/result npz aren't committed; put demo outputs in the scratchpad or `results/`.
- **Tools:** MuJoCo (Apache-2.0), PyElastica (MIT), NumPy/SciPy (BSD), scikit-learn (BSD-3), matplotlib ≥300 DPI. FEM (SOFA/FEniCSx) offline-only. JAX-GPU needs WSL2 — avoid. PyTorch CUDA build = BSD; check the sm_120 wheel channel.
- **Licensing:** code MIT, prose CC BY 4.0. No relaxed standard requested.
- **LaTeX (Phase-3 writing / Study Guide Pass 2):** MiKTeX pdflatex works; preamble needs `\usepackage{xcolor}`; aux gitignored, final PDFs tracked; two passes for TOC.
- **Software-engineering standard for every script:** `argparse` with `required=True` for input roots, project-relative outputs, no hard-coded paths, one clear purpose, shared logic in `utils/`, docstrings, prints progress, fails loud. (`utils/` library modules are the import-not-CLI exception — no argparse there, e.g. `estimator.py`.)

## Pointers

- Claim Sheet (in-force contract): `Claim Sheet.md` · plain-language companion: `Accessible Claim Sheet.md`
- Study Guide Pass 1: `Study Guide/Pass 1 - Conceptual Foundation.tex` (+ PDF)
- **Shared schema (in force):** `Reproducibility Packet/schema/schema-v1.0.md` — rendered in `utils/schema_types.py` (§B/§0/§C/§E) + `utils/estimator.py` (§D)
- **My sensor lane (S6, jointly approved S7):** `utils/{schema_types,sensor_model,rng,synthetic_plant}.py`, `scripts/{make_synthetic_plant_trace,run_sensor_model}.py`, `tests/test_sensor_model.py`
- **My evaluation core (S7, corrected+approved S8):** `utils/{metrics,stats}.py`, `tests/{test_metrics,test_stats}.py`
- **My estimator lane (S8):** `utils/estimator.py`, `tests/test_estimator.py`
- **Codex's plant lane (+ online loop):** `utils/{cable_mechanics,cable_plant,online_loop}.py`, `scripts/{make_mujoco_plant_trace,run_feasibility_spike}.py`, `tests/{test_cable_plant,test_feasibility_spike,test_online_loop}.py`
- Director requests: `director_requests.md` (root) — entry 1 (Claim Sheet review) non-blocking, awaiting director reply.
- **Active Phase-2 chat:** `chats/Claude-Codex/Phase 2 Integration and Config Freeze/…- Active.md` (my S8 turn is the tail; Codex reply pending)
- Concluded chats: `chats/Claude-Codex/Phase 0 Coordination/`, `chats/Claude-Codex/Claim Sheet Review and Division of Labor/`, `chats/Claude-Codex-Human/Chat Appends/` (each has a `Summary.md`)
- My foundation: `agents/Claude/Literature Foundation.md` · My ledger: `agents/Claude/references.md` (S8 estimator-lane mapping + forward corrections added) · Codex's: `agents/Codex/`
- Live-Run README (co-maintained): root `README.md` — **Phase 2 / In Progress** (running-log line added S8).
- My progress reports: `agents/Claude/Progress Reports/` (Phase 0 Close, Phase 1 Close, **Session 8**). **Next regular: Session 16.**
- Scratchpad (not committed): `s8_reverify.py` (independent re-review checks), `s8_chat_turn.md` (my posted chat turn).
