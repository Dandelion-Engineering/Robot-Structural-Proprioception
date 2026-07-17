# Summary of Only Necessary Context — Claude

*Rewritten every session. Restores my working context for the next session. Excludes anything already in `Project Details/Project Details.md` and `AgentPrompt.md` (I re-read those in full at session start). Last rewritten: end of Session 6, 2026-07-17.*

## Where the project is

- **Phase 2 (Execution) is OPEN.** All Phase-1 gates closed (Claim Sheet, Accessible Claim Sheet, Study Guide Pass 1, schema v1.0 — all jointly approved and in force). Contract changes run through the **amendment protocol**, not casual editing.
- I am **Claude**; last session was **Session 6**; next session I run is **Session 7**.
- **Two Phase-2 lanes are now underway:**
  - **Codex's plant lane:** feasibility spike is a **qualified PASS** (Codex Session 5). Native MuJoCo cable/rod mechanics clear the differential-signature gate **only with bounded, matched, zero-mean diagnostic excitation** (1.0 N distal load); ordinary torque-only excitation BLOCKS and is preserved as a first-class negative control. **Frozen numbers:** `n_def=90` (3-vector log-map rot for 15 internal ball joints × 2 links), four gauge stations at (link1: 0.25 L, 0.75 L), (link2: 0.25 L, 0.75 L). Per-step handoff object named **`PlantStepState`**. Codex's next step: emit the real persisted privileged trace + online closed-loop path.
  - **My sensor lane:** **built this session** (see next section).
- **Progress-report cadence:** next *regular* one is my **Session 8**. Phase-0-close and Phase-1-close reports already written; they don't reset the counter. No report was due this session (no phase transition, no amendment).

## What I built this session (Session 6) — the sensor lane

The **sensor-realism + fault-injection model** — my agreed first Phase-2 deliverable and the piece Codex named as the next integration need. Written into `Reproducibility Packet/scripts/` (packet-ready as we go), against schema v1.0 + the spike's frozen numbers. **18/18 packet tests green; verified end-to-end on persisted output.** Files:
- `utils/schema_types.py` — `PrivilegedRecord` (§B), `PlantStepState` (§0 per-step slice), `ObservedRecord` (§C), the fixed 18-col channel registry, C0⊂C1⊂S suite masks, and `observable_sources()` (the narrow doorway from privileged truth). Has `PrivilegedRecord.save_npz/load_npz` and `ObservedRecord.save_npz/load_npz`.
- `utils/sensor_model.py` — `SensorModel` + shared `FaultSpec` fault-library type + pathologies: noise (FBG floor 1 µε), thermal apparent strain (10 µε/°C), bias, random-walk drift, first-order-lag hysteresis, quantization, dropout, latency. Encoder faults (bias/drift/dropout) → observation path only.
- `utils/rng.py` — CRN substreams: independent generator per `(sensor_seed, pair_id, channel, stream)`.
- `utils/synthetic_plant.py` + `scripts/make_synthetic_plant_trace.py` — a schema-conforming **synthetic** privileged trace, a **dev stand-in for Codex's real plant** (not confirmatory).
- `scripts/run_sensor_model.py` — CLI: privileged trace → one suite's observed `.npz` + per-suite `index.csv` (§E observations role).
- `tests/test_sensor_model.py` — 14 tests (leakage boundary, CRN, thermal, relational encoder fault, dropout, latency causality, determinism, npz round-trip).

**Two schema properties I made code-level (not just conventional), relevant to Codex:** (1) leakage boundary — `SensorModel.observe` reads only `observable_sources`, so privileged-only fields (`tau_delivered_true`, `deform_coords`, `curvature_true`, task truth, labels) *structurally cannot* enter an observation; (2) actuator fault stays hidden from C1 — the current proxy reads `control_effort` (upstream of gain loss), never `tau_delivered_true`.

## The single most important thing to do next session

Pick up Phase-2 execution. Two independent tracks, either is fine to advance:

1. **Build the two-layer evaluation harness (my next deliverable; plant-independent, so no blocking).** Diagnosis metrics (four-way macro-F1 + the calibration/selective/OOD family — Brier/NLL/ECE, risk-coverage working points, false-abstention, OOD AUROC/AUPRC/false-accept@95%), the control metric `J_5s = ∫_{t_c}^{t_c+5}‖e(t)‖dt` (deformed-tip, planar, L2, trapezoidal), the leakage-free split logic with the **executable split audit** and the **§D leakage test** (must fail the build if a deployable loader can reach identity manifest / privileged / labels / other-suite arrays), and the **paired hierarchical bootstrap** (SciPy = CI primitive only; nested resampling of `pair_id` units + `train_seed`s is ours). Build it into the packet with the same standards (argparse, utils/, tests, numpy/scipy pinned). scipy 1.18.0 and scikit-learn 1.9.0 are in the venv already.
2. **Config-freeze coordination (needs Codex).** Assemble `config.json` from Codex's mechanics values (`n_def`, gauge stations, timestep, control step, diagnostic-excitation params) + my `SensorConfig` sensor constants + the frozen §F windowing constants (`f_ctrl`, `W`, `stride`, onset, 5-s window). **Do not freeze a partial config** — both lanes' values + windowing must be in, and it's immutable once frozen (before pilot/confirmatory generation). I raised this in the new chat; awaiting Codex.

**Also check the new Phase-2 chat for Codex's reply** on (a) reviewing my `PlantStepState`/`PrivilegedRecord` rendering, and (b) the control rate + diagnostic-excitation numbers. When Codex's plant emits a real persisted privileged trace, swap out the synthetic fixture and stand up the online closed-loop path (§0) where C1/S diverge.

## Coordination state (chats)

- **Claim Sheet Review chat — CONCLUDED this session** (director instruction). Renamed to `…- Concluded.md`, `Summary.md` written. All Phase-1 loops were closed.
- **New active Phase-2 chat:** `chats/Claude-Codex/Phase 2 Integration and Config Freeze/…- Active.md`. My opening turn (S6) accepts the spike results + `PlantStepState`, reports the sensor model, proposes the config-freeze sequence, and flags the shared interface for Codex's review. **Codex has not replied yet** — check it next session.
- **`chats/Claude-Codex-Human/Chat Appends/…- Active.md` — director occurrence, awaiting Codex's acknowledgment.** Randy flagged that Codex twice inserted chat replies mid-transcript (auto-patch anchor matched an earlier sign-off), corrected append-only (no loss). I acknowledged (S6) and logged it in the Live-Run README. **This chat can be concluded once Codex also acknowledges.** **MONITORING DUTY:** Randy asked me to watch for the mis-insertion pattern; if I catch a reply landing anywhere but the end of a transcript, flag it in `Claude-Codex-Human`.
- **Non-blocking forward item (carry to Technical Report, not a schema edit):** the Hendriks et al. 2022 split-leakage cautionary case belongs in the Technical Report's methods rationale for the whole-group split. In both ledgers.

## Schema v1.0 mental model (build against it; it is now partly rendered in `utils/schema_types.py`)

File: `Reproducibility Packet/schema/schema-v1.0.md` (in force). My code renders §B/§C/§0/§E into dataclasses — read `utils/schema_types.py` alongside the schema next session. Load-bearing structure:
- **§A identity/pairing/splits:** `scenario_spec_id` (shared in pair) · `pair_id` (matched C1-vs-S) · `run_id` (one rollout; C1 and S each own one). Identity manifest **non-deployable**. Splits by whole trajectory **and** whole fault setting; **suite never an input to the split**; enforced by an executable pre-fit audit. **CRN within a pair:** shared sim/fault/sensor seeds + deterministic substreams keyed by (pair_id, channel, step) — my `utils/rng.py` implements this.
- **§B privileged plant record** (per run, control grid): q/qd/qdd_true, tau_cmd (pre-limit), **control_effort** (saturated, pre-fault, what the current proxy senses), **tau_delivered_true** (post-fault), deform_coords[90], curvature_true[4], gauge_true[4] µε, imu_true[6], **temperature_true[4]**, contact, task_reference + **true_task_output (deformed tip)** + tracking_error(+norm), effort/saturation/safety.
- **§C observed record** (deployable suites, fixed 18-col registry, unavailable channels = NaN): corrupted q_obs + causal qd_obs, tau_cmd, current_proxy_obs (C1/S; noisy nominal-Kt current, **upstream** of gain loss), imu_obs (C1/S), **4 signed surface-strain gauge_obs (S only)**. Static `suite_available_mask`; per-time-per-channel `valid_mask` + measurement/availability/latency timing.
- **§D labels/outputs/causality/leakage:** labels stored separately (only bridge from truth to target); estimator outputs + controller logs separate; **automated leakage test fails the build** if a deployable loader can reach identity manifest/provenance/privileged/label/other-suite arrays; past-only windows; O = separate allowlisted oracle interface.
- **§E storage:** non-deployable `manifest.csv` + per-role roots/indexes (`plant/`, `observations/<suite>/`, `labels/`, `estimator_outputs/<suite>/`, `controller_logs/<suite>/`); each index carries `run_id, schema_version, config_hash, npz_path, sha256`; observation index also carries safe `split`. One non-pickled `.npz` per rollout per role. Immutable `schema.json`/`config.json`. No Parquet/YAML dep. (My `run_sensor_model.py` writes the observations role.)
- **§F frozen constants:** f_ctrl, dt, W (past-only), stride, onset convention, `[t_c, t_c+5s]` — names/rules in schema, **values in `config.json`**, frozen before confirmatory generation.
- **§G tracking metric:** `J_5s = ∫‖e(t)‖dt`, e = task_reference − **true deformed tip**, planar (x,y), metres, **L2**, control-grid, **trapezoidal**. Bar = ≥10% reduction vs C1 (paired 95% interval excludes zero, no safety regression).
- **§H deliberately open** (set in frozen config from the spike): gauge locations (frozen), `n_def` (=90), numeric f_ctrl/W/stride, severity grids/onset distribution, diagnostic-excitation budget.

## The agreed contract's load-bearing specifics (carry this)

- **Sensor suites (the controlled variable):** **C0** = joint encoders + commanded actuation · **C1** = C0 + *noisy motor-current* nominal-Kt torque estimate + one distal 6-axis IMU · **S** = C1 + **four fixed strain/curvature gauge stations** · **O** = privileged oracle. External pose/vision and *true delivered torque* excluded from deployable suites.
- **Two settled correctness points:** (1) actuator-gain fault acts *downstream* of the current proxy → C1 not handed true delivered torque (attribution stays non-trivial); (2) encoder (sensor) fault has a *relational* signature — a lying sensor doesn't deform the structure; identified by repeatable *disagreement* between corrupted encoder and independently-evolved gauge/physical history (analytical redundancy). My sensor model implements both.
- **Success bar (pre-declared, both layers required):** S improves held-out four-way **macro-F1 over C1 by ≥0.05 absolute** (paired 95% interval excludes zero; every source-class recall difference lower-95%-bound above −0.02) **and** reduces the **5-s post-change integral of absolute tracking error by ≥10%** (paired interval excludes zero; no safety regression), **under realistic confounds**. Known-class abstention scored as error in headline macro-F1; calibration/selective/OOD reported separately.
- **Failure shapes:** *hypothesis failure* (C1+temporal adaptation matches S — clean negative) vs *method failure* (spike can't produce differential signatures / algebraic echo / leakage). **Inconclusive shapes:** diagnostic-only · fault-specific/bounded · confound-fragile · excitation-dependent.
- **Pre-specification:** bars fixed before the pilot; the pilot sizes the test, not the bar. Freeze gauge placement, model/hyperparams, class+abstention thresholds, analysis window, seeds/scenarios in the versioned config before confirmatory generation. Leakage-free splits. ≥5 training seeds. Paired hierarchical bootstrap.

## Labor split (agreed, unchanged)

- **Codex:** feasibility spike + physics (MuJoCo cable/rod done; PyElastica fallback + independent beam/Cosserat validation), virtual-gauge extraction, excitation design, interpretable residual/linear-sysID baseline, recovery controller (gain-scheduling/MPC).
- **Claude (me):** fault-injection + sensor-realism model (**done S6**), matched temporal attribution estimator + capacity ladder + calibration/abstention, RMA-style latent baseline + oracle, two-layer evaluation harness + metrics + stats (**next**), Slot-8 verification demo, default-writer artifacts (Technical Report, Accessible Piece, Study Guide Pass 2 — Codex reviews).
- **Shared:** the plant→signals→estimator schema (in force), fault library, Reproducibility Packet, references reconciliation (Phase 2). The **"does attribution improve control" headline experiment is shared** at the diagnosis→control seam.

## Constraints / environment (unchanged, load-bearing)

- **Simulation-only, one desktop:** Windows 11, Ryzen 7 8700F (8C/16T), RTX 5060 Ti **16 GB VRAM**, 32 GB RAM, Python **3.12.10** in `./venv` (use `.\venv\Scripts\python.exe` / `pip.exe`, never bare). Free/OSS, commercial-use-friendly only.
- **venv has:** numpy 2.5.1, scipy 1.18.0, scikit-learn 1.9.0, matplotlib 3.11.0, mujoco 3.10.0, pandas 3.0.3, control 0.10.2, gymnasium 1.3.0, pytest 9.1.1. Packet `requirements.txt` pins matplotlib/mujoco/numpy/pytest (sensor lane is numpy-only). Pin any new dep the moment it's installed; add scipy/sklearn to the packet requirements when the eval harness uses them.
- **Packet `.gitignore` ignores `*.npz`** (and caches/logs) — demo/result npz aren't committed; put demo outputs in the scratchpad or `results/`.
- **Tools:** MuJoCo (Apache-2.0), PyElastica (MIT), NumPy/SciPy, PyTorch CUDA build (verify GPU at install — not yet installed), matplotlib ≥300 DPI. FEM (SOFA/FEniCSx) offline-only. JAX-GPU needs WSL2 — avoid.
- **Licensing:** code MIT, prose CC BY 4.0. No relaxed standard requested.
- **LaTeX (Phase-3 writing / Study Guide Pass 2):** MiKTeX pdflatex works; preamble needs `\usepackage{xcolor}`; aux gitignored, final PDFs tracked; two passes for TOC.
- **Software-engineering standard for every script:** `argparse` with `required=True` for input roots, project-relative outputs, no hard-coded paths, one clear purpose, shared logic in `utils/`, docstrings, prints progress, fails loud.

## Pointers

- Claim Sheet (in-force contract): `Claim Sheet.md` · plain-language companion: `Accessible Claim Sheet.md`
- Study Guide Pass 1: `Study Guide/Pass 1 - Conceptual Foundation.tex` (+ PDF)
- **Shared schema (in force):** `Reproducibility Packet/schema/schema-v1.0.md` — partly rendered in `Reproducibility Packet/scripts/utils/schema_types.py`
- **My sensor lane (S6):** `Reproducibility Packet/scripts/{utils/,make_synthetic_plant_trace.py,run_sensor_model.py}` + `tests/test_sensor_model.py`
- Director requests: `director_requests.md` (root) — entry 1 (Claim Sheet review) non-blocking, awaiting director reply.
- **Active Phase-2 chat:** `chats/Claude-Codex/Phase 2 Integration and Config Freeze/…- Active.md` (Codex reply pending)
- **Director chat awaiting Codex ack:** `chats/Claude-Codex-Human/Chat Appends/…- Active.md`
- Concluded chats: `chats/Claude-Codex/Phase 0 Coordination/` + `chats/Claude-Codex/Claim Sheet Review and Division of Labor/` (each has a `Summary.md`)
- My foundation: `agents/Claude/Literature Foundation.md` · My ledger: `agents/Claude/references.md` (Phase-2 sensor-model mapping added S6) · Codex's: `agents/Codex/`
- Live-Run README (co-maintained): root `README.md` — **Phase 2 / In Progress**.
- My progress reports: `agents/Claude/Progress Reports/` (Phase 0 Close, Phase 1 Close). Next regular: Session 8.
