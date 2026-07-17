# Summary of Only Necessary Context — Claude

*Rewritten every session. Restores my working context for the next session. Excludes anything already in `Project Details/Project Details.md` and `AgentPrompt.md` (I re-read those in full at session start). Last rewritten: end of Session 7, 2026-07-17.*

## Where the project is

- **Phase 2 (Execution) is OPEN.** All Phase-1 gates closed and in force (Claim Sheet, Accessible Claim Sheet, Study Guide Pass 1, schema v1.0). Contract changes run through the **amendment protocol**, not casual editing.
- I am **Claude**; last session was **Session 7**; next session I run is **Session 8**.
- **⚠️ SESSION 8 IS A PROGRESS-REPORT SESSION.** My next *regular* director progress report is due at my Session 8 — write it **in addition to** normal session work (not instead of), at the Accessible-Piece bar, into `agents/Claude/Progress Reports/`. See `Playbooks/research-progress-report.md`. (Phase-0-close and Phase-1-close reports already exist and don't reset the per-agent counter.)
- **The two Phase-2 lanes are now integrated at the development level and mutually verified.** A real MuJoCo plant trace flows through my sensor model to produce matched C1/S observations; both agents have signed off the same interface state.

## What I did this session (Session 7)

1. **Closed the review-cycle loop on the shared plant→sensor interface** (Codex handed it back S6 for my genuine owner re-review). I re-reviewed Codex's edits to my sensor code + the new real-plant producer, **reproduced and independently extended the verification**, found no defects, and **explicitly approved the same state**. Loop is CLOSED — both agents approved the same state (committed at `Codex Session 6`, `70e6e4f`, + my S7 closeout). Codex's two corrections were both legitimate:
   - **`PlantStepState` losslessness** — my S6 design error (I made the per-step object only the sensor-readable subset, so `slice_step()` was lossy). Codex expanded it to all §B fields; `observable_sources()` stays the narrow doorway. Correct.
   - **`qd_obs` validity** — real bug in my S6 code: backward-difference velocity was marked valid using only the current encoder sample. Fixed to require current AND previous (`qd_valid[t] = q_valid[t] & q_valid[t-1]`), value forced NaN where invalid. Verified correct even at step-0 dropout.
   - Also: `FaultSpec` moved to `schema_types.py` (shared boundary object); observation output inherits the plant's `config_hash` with a `dev-` prefix (nothing pre-freeze can be mistaken for confirmatory).
2. **Built my next deliverable: the two-layer evaluation harness — metrics + stats core** (plant-independent; no handoff needed). Into the packet, standards-clean, fully tested. **Packet went 25 → 51 tests green.**
3. Session closeout: chat reply, references (added Guo 2017 for ECE), Live-Run README running-log line, this rewrite, human report, git.

## The single most important thing to do next session (Session 8)

**Write the Session-8 progress report (due), and advance Phase-2 execution — my next build is the diagnosis estimator.** Two tracks, either/both fine; the estimator is the higher-leverage one because it unblocks the config freeze:

1. **Build the diagnosis estimator** (my lane): the **matched temporal-attribution model** + the **RMA-style latent baseline** + the **oracle (O)** interface, against the online plant→sensor seam. This is the *consumer* of the window parameters, so **`W` (past-only window length) and `stride` get proposed with it** — which then unblocks the complete `config.json` freeze. Build into the packet with the same standards (argparse for any CLI driver, `utils/`, tests, pins). It reads §D estimator-output structs (`p_class[4]`, `unknown_score`, `abstain_decision`, `location_out`, `severity_out`, `severity_uncertainty`, `detection_time_s`) and produces them; my `utils/metrics.py` already scores them.
2. **Config-freeze coordination (needs Codex).** Assemble the immutable `config.json` once ALL fields converge (see the table in the active chat). **Do not freeze a partial config** — it's immutable once frozen (before pilot/confirmatory generation).

**Deferred deliberately (not forgotten):** the **§D deployable-loader leakage test** and the **executable split audit** — I deferred these because they need *real multi-run data* (post-config-freeze) to bite on. Build them before pilot/confirmatory generation. They must fail the build if a deployable loader can reach identity manifest / privileged / labels / other-suite arrays.

## The evaluation harness core I built (Session 7) — reference for the estimator + confirmatory analysis

Files under `Reproducibility Packet/scripts/utils/` (+ tests in `tests/`):
- **`metrics.py`** — pure functions rendering the pre-declared bars:
  - `SOURCE_CLASS_ORDER = (healthy, structure, actuator, sensor)` (index↔name); `ABSTAIN = -1` sentinel; `resolve_predictions(p_class, abstain)` → hard label or ABSTAIN.
  - Diagnosis: `macro_f1` (four-way, **abstention scored as headline error** via sklearn f1 with out-of-label sentinel), `per_class_recall` (name-keyed dict), `brier_score`, `nll`, `expected_calibration_error` (Guo 2017, 15-bin top-confidence), `risk_coverage_curve` / `selective_risk_at_coverage`, `false_abstention_rate` (in-distribution only), `ood_auroc` / `ood_auprc` / `false_accept_at_id_acceptance` (biometric operating point, default 95% ID accepted).
  - Control: `j_5s(t_s, task_reference, true_task_output, onset_time_s, window_s=5.0)` — planar (x,y) L2 error of the **true deformed tip**, trapezoidal (`np.trapezoid`) over `[t_c, t_c+5s]`, m·s; `tracking_reduction_pct(j_c1, j_s)`.
- **`stats.py`** — `hierarchical_bootstrap_ci(clusters, statistic_fn, *, n_boot, rng, ci_level=0.95)`: two-level cluster bootstrap (resample `pair_id` clusters, then `train_seed` subunits within each; pairing preserved because a subunit carries both suites' data). Returns `BootstrapResult(point, ci_low, ci_high, ci_level, n_boot, excludes_zero)` with `.non_inferior(margin)` (lower bound > −margin) and `.superior_by(effect)` (point ≥ effect AND excludes zero). `mean_difference_statistic(key_s, key_c1)` convenience. NumPy-only (percentile CI); scipy NOT used. **statistic_fn must be robust to resampling (return finite)** — `macro_f1` is (zero_division=0).
- **Uses sklearn** (`f1_score`, `recall_score`, `roc_auc_score`, `average_precision_score`) — pinned `scikit-learn==1.9.0` in packet `requirements.txt`. Statistic pooling for Δmacro-F1 (concatenate y_true/y_pred across resampled runs, then score) is written in the statistic_fn, not in stats.py.

## Coordination state (chats)

- **Active Phase-2 chat:** `chats/Claude-Codex/Phase 2 Integration and Config Freeze/…- Active.md`. My S7 turn: same-state approval (loop closed), independent verification results, the **config-freeze items table**, the **`W`/stride deferral** (comes with the estimator), and the **negative-control commitment** (ordinary-torque BLOCK stays a separate `trajectory_spec_id`; a diagnostic-condition PASS never stands in for ordinary-motion observability). **Codex has not replied to my S7 turn yet — check it next session.**
- **Chat Appends (director) — CONCLUDED** (both agents acknowledged the transcript-order occurrence). **MONITORING DUTY IS STANDING:** if I ever see a reply land anywhere but the physical end of a transcript, flag it in `Claude-Codex-Human`. (I verify my own appends land at the tail — did so S7.)
- **Config-freeze items still open** (from my S7 table): diagnostic **duration/envelope** (Codex — gate validated continuous 3-s sinusoid, not a windowed burst; preserve into pilot or run a bounded-burst sensitivity), contact/safety **array widths + thresholds** (Codex — zero-width in dev), severity/onset grids (shared, pilot-informed), sensor pathology constants (mine — jointly sanity-check the non-load-bearing ones), `W`/stride (mine — with the estimator). Settled: `f_ctrl=500`, `dt=0.002`, sim step `1e-4`, `n_def=90`, 4 gauge stations, diagnostic `1.0 N`/`0.8 Hz`.
- **Non-blocking forward item (carry to Technical Report):** Hendriks et al. 2022 split-leakage cautionary case → Technical Report methods rationale for the whole-group split. In both ledgers.

## Schema v1.0 mental model (in force; partly rendered in `utils/schema_types.py`)

File: `Reproducibility Packet/schema/schema-v1.0.md`. Read `utils/schema_types.py` alongside it — it renders §B/§0/§C/§E into dataclasses (now with Codex's lossless `PlantStepState`).
- **§A identity/pairing/splits:** `scenario_spec_id` (shared in pair) · `pair_id` (matched C1-vs-S) · `run_id` (one rollout). Identity manifest **non-deployable**. Splits by whole trajectory AND whole fault setting; **suite never an input to the split**; enforced by an executable pre-fit audit (to build). **CRN within a pair:** shared seeds + deterministic substreams keyed by (pair_id, channel, step) — `utils/rng.py`.
- **§B privileged plant record** (per run, control grid): q/qd/qdd_true, tau_cmd (pre-limit), **control_effort** (saturated, pre-fault — what the current proxy senses), **tau_delivered_true** (post-fault), deform_coords[90], curvature_true[4], gauge_true[4] µε, imu_true[6], temperature_true[4], contact_state, task_reference + **true_task_output (deformed tip)** + tracking_error(+norm), control_effort/saturation/safety. **`PlantStepState` now carries ALL of these (lossless); `observable_sources()` exposes only the measurable subset** (t_s, q_true, tau_cmd, control_effort, imu_true, gauge_true, temperature_true).
- **§C observed record** (deployable suites, fixed 18-col registry, unavailable = NaN): corrupted q_obs + causal qd_obs, tau_cmd, current_proxy_obs (C1/S; noisy nominal-Kt current, **upstream** of gain loss), imu_obs (C1/S), **4 signed surface-strain gauge_obs (S only)**. Static `suite_available_mask`; per-time-per-channel `valid_mask` + measurement/availability/latency timing.
- **§D labels/outputs/causality/leakage:** labels stored separately (only bridge from truth to target). **Estimator outputs:** `p_class[4]`, `unknown_score`, `abstain_decision`, `location_out`, `severity_out`, `severity_uncertainty`, `detection_time_s`. Controller logs separate. **Automated leakage test fails the build** if a deployable loader reaches identity manifest/privileged/label/other-suite arrays (to build, pre-pilot). Past-only windows. O = separate allowlisted oracle interface.
- **§E storage:** non-deployable `manifest.csv` + per-role roots/indexes (`plant/`, `observations/<suite>/`, `labels/`, `estimator_outputs/<suite>/`, `controller_logs/<suite>/`); each index carries `run_id, schema_version, config_hash, npz_path, sha256`; observation index also carries safe `split`. One non-pickled `.npz` per rollout per role. Immutable `schema.json`/`config.json`.
- **§F frozen constants:** f_ctrl, dt, W, stride, onset convention, `[t_c,t_c+5s]` — names/rules in schema, **values in `config.json`**, frozen before confirmatory generation.
- **§G tracking metric:** `J_5s = ∫‖e(t)‖dt`, e = task_reference − **true deformed tip**, planar (x,y), metres, **L2**, control-grid, **trapezoidal**, m·s. Bar = ≥10% reduction vs C1 (paired 95% interval excludes zero, no safety regression). **Rendered in `utils/metrics.j_5s`.**
- **§H deliberately open** (set in frozen config): gauge locations (frozen =4 stations), n_def (=90), numeric f_ctrl/W/stride, severity grids/onset distribution, diagnostic-excitation budget.

## The agreed contract's load-bearing specifics (carry this)

- **Sensor suites (the controlled variable):** **C0** = joint encoders + commanded actuation · **C1** = C0 + noisy motor-current nominal-Kt torque estimate + one distal 6-axis IMU · **S** = C1 + **four fixed strain/curvature gauge stations** · **O** = privileged oracle. External pose/vision and true delivered torque excluded from deployable suites.
- **Two settled correctness points (both implemented + verified):** (1) actuator-gain fault acts *downstream* of the current proxy → C1 not handed true delivered torque; (2) encoder (sensor) fault has a *relational* signature — a lying sensor doesn't deform the structure; identified by disagreement between corrupted encoder and independently-evolved gauge/physical history (analytical redundancy).
- **Success bar (pre-declared, BOTH layers required):** S improves held-out four-way **macro-F1 over C1 by ≥0.05 absolute** (paired 95% interval excludes zero; every source-class recall difference lower-95%-bound above **−0.02**) **and** reduces the **5-s post-change integral of absolute tracking error by ≥10%** (paired interval excludes zero; no safety regression), **under realistic confounds**. Known-class abstention scored as error in headline macro-F1; calibration/selective/OOD reported separately. **All rendered in `utils/metrics.py` + `utils/stats.py`.**
- **Failure shapes:** *hypothesis failure* (C1+temporal adaptation matches S — clean negative) vs *method failure* (spike can't produce differential signatures / algebraic echo / leakage). **Inconclusive shapes:** diagnostic-only · fault-specific/bounded · confound-fragile · excitation-dependent.
- **Pre-specification:** bars fixed before the pilot; the pilot sizes the test, not the bar. Freeze gauge placement, model/hyperparams, class+abstention thresholds, analysis window, seeds/scenarios in the versioned config before confirmatory generation. Leakage-free splits. ≥5 training seeds. Paired hierarchical bootstrap.

## Labor split (agreed, unchanged)

- **Codex:** feasibility spike + physics (MuJoCo cable/rod done → `CablePlant` producer done; PyElastica fallback + independent beam/Cosserat validation), virtual-gauge extraction, excitation design, interpretable residual/linear-sysID baseline, recovery controller (gain-scheduling/MPC).
- **Claude (me):** fault-injection + sensor-realism model (**done S6**), matched temporal attribution estimator + capacity ladder + calibration/abstention (**next**), RMA-style latent baseline + oracle (**next**), two-layer evaluation harness + metrics + stats (**core done S7**; leakage test + split audit deferred to post-freeze), Slot-8 verification demo, default-writer artifacts (Technical Report, Accessible Piece, Study Guide Pass 2 — Codex reviews).
- **Shared:** the plant→signals→estimator schema (in force), fault library, Reproducibility Packet, references reconciliation (Phase 2). The **"does attribution improve control" headline experiment is shared** at the diagnosis→control seam.

## Constraints / environment (unchanged, load-bearing)

- **Simulation-only, one desktop:** Windows 11, Ryzen 7 8700F (8C/16T), RTX 5060 Ti **16 GB VRAM**, 32 GB RAM, Python **3.12.10** in `./venv` (use `.\venv\Scripts\python.exe` / `pip.exe`, never bare). Free/OSS, commercial-use-friendly only.
- **venv has:** numpy 2.5.1, scipy 1.18.0, scikit-learn 1.9.0, matplotlib 3.11.0, mujoco 3.10.0, pandas 3.0.3, control 0.10.2, gymnasium 1.3.0, pytest 9.1.1. **Packet `requirements.txt` now pins matplotlib/mujoco/numpy/pytest/scikit-learn.** Pin any new dep the moment it's installed. PyTorch CUDA build NOT yet installed — verify GPU at install when the estimator needs it.
- **Packet `.gitignore` ignores `*.npz`** (and caches/logs) — demo/result npz aren't committed; put demo outputs in the scratchpad or `results/`.
- **Tools:** MuJoCo (Apache-2.0), PyElastica (MIT), NumPy/SciPy (BSD), scikit-learn (BSD-3), matplotlib ≥300 DPI. FEM (SOFA/FEniCSx) offline-only. JAX-GPU needs WSL2 — avoid.
- **Licensing:** code MIT, prose CC BY 4.0. No relaxed standard requested.
- **LaTeX (Phase-3 writing / Study Guide Pass 2):** MiKTeX pdflatex works; preamble needs `\usepackage{xcolor}`; aux gitignored, final PDFs tracked; two passes for TOC.
- **Software-engineering standard for every script:** `argparse` with `required=True` for input roots, project-relative outputs, no hard-coded paths, one clear purpose, shared logic in `utils/`, docstrings, prints progress, fails loud. (utils/ library modules are the import-not-CLI exception — no argparse there.)

## Pointers

- Claim Sheet (in-force contract): `Claim Sheet.md` · plain-language companion: `Accessible Claim Sheet.md`
- Study Guide Pass 1: `Study Guide/Pass 1 - Conceptual Foundation.tex` (+ PDF)
- **Shared schema (in force):** `Reproducibility Packet/schema/schema-v1.0.md` — partly rendered in `Reproducibility Packet/scripts/utils/schema_types.py`
- **My sensor lane (S6, now jointly approved S7):** `utils/{schema_types,sensor_model,rng,synthetic_plant}.py`, `scripts/{make_synthetic_plant_trace,run_sensor_model}.py`, `tests/test_sensor_model.py`
- **My evaluation core (S7):** `utils/{metrics,stats}.py`, `tests/{test_metrics,test_stats}.py`
- **Codex's plant lane:** `utils/{cable_mechanics,cable_plant}.py`, `scripts/{make_mujoco_plant_trace,run_feasibility_spike}.py`, `tests/{test_cable_plant,test_feasibility_spike}.py`
- Director requests: `director_requests.md` (root) — entry 1 (Claim Sheet review) non-blocking, awaiting director reply.
- **Active Phase-2 chat:** `chats/Claude-Codex/Phase 2 Integration and Config Freeze/…- Active.md` (Codex reply to my S7 turn pending)
- Concluded chats: `chats/Claude-Codex/Phase 0 Coordination/`, `chats/Claude-Codex/Claim Sheet Review and Division of Labor/`, `chats/Claude-Codex-Human/Chat Appends/` (each has a `Summary.md`)
- My foundation: `agents/Claude/Literature Foundation.md` · My ledger: `agents/Claude/references.md` (Phase-2 eval-metrics mapping + Guo 2017 added S7) · Codex's: `agents/Codex/`
- Live-Run README (co-maintained): root `README.md` — **Phase 2 / In Progress** (running-log line added S7).
- My progress reports: `agents/Claude/Progress Reports/` (Phase 0 Close, Phase 1 Close). **Next regular: Session 8 (DUE).**
