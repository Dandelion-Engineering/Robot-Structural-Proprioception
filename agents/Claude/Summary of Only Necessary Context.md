# Summary of Only Necessary Context — Claude

*Rewritten every session. Restores my working context for the next session. Excludes anything already in `Project Details/Project Details.md` and `AgentPrompt.md` (I re-read those in full at session start). Last rewritten: end of Session 9, 2026-07-19 20:21 PDT.*

## Where the project is

- **Phase 2 (Execution) is OPEN.** All Phase-1 gates closed and in force (Claim Sheet, Accessible Claim Sheet, Study Guide Pass 1, schema v1.0). Contract changes run through the **amendment protocol**, not casual editing.
- I am **Claude**; last session was **Session 9**; next session I run is **Session 10**.
- **Next regular director progress report: my Session 16.** (Phase-0-close, Phase-1-close, and Session-8 reports exist; they don't reset the per-agent counter. Session 9 closed no phase and made no amendment → no report.)
- **No open review-cycle loops right now.** I closed the estimator loop this session (same-state approval of Codex's S8 edits). Do not infer any pending approval.
- **`config.json` is deliberately NOT frozen**, and cannot be until the excitation blocker is resolved. Current role hashes are `dev-`; no trace may enter confirmatory analysis.

## The one thing that dominates the project right now: the excitation blocker (and my S9 reframing)

**The blocker (Codex, S8).** The experiment needs strain gauges to show a *differential* signature (structure vs actuator vs sensor). Codex's bounded-burst sensitivity (`results/bounded_burst_sensitivity/`) found that an **honest bounded diagnostic probe** (starting at fault onset) produces a structural signature (~8 µε RMS) **below** the mechanics gate's **10 µε per-sample floor** → BLOCK. The only excitation that clears the floor (continuous, pre-fault) drives the arm past a provisional **safety envelope** (|q|≤π rad, |qd|≤10 rad/s: continuous hit 9.05 rad / 40.67 rad/s). So no current excitation is both informative AND safe. `config.json` cannot freeze.

**My S9 reframing (the key new context).** The 10 µε floor is a **per-sample, broadband** number, dominated by the **thermal cross-sensitivity** (10 µε/°C — a slow, low-frequency error), plus DC bias and random-walk drift. But the differential signature is at the **known 0.8 Hz probe frequency**, and the estimator reads a **W-sample window**. A **synchronous / lock-in detector at 0.8 Hz** rejects the thermal ramp, bias, and drift. I measured its noise-equivalent strain (NES) against the **real** `OnlineSensorSession` gauge stack: **NES ≈ 0.10 µε — ~103× below the 10 µε gate floor.** The bounded-burst differentials the gate marked BLOCK (structural 8.18, actuator 7.84, separation 12.33 µε) detect at **100%**, z ≈ 150–305. Artifact: `scripts/analyze_synchronous_detection_floor.py` + `results/synchronous_detection_floor/` + `tests/test_synchronous_detection_floor.py`.
- **What it changes:** the excitation target moved from "reach 10 µε broadband" (which forced unsafe amplitudes) to "produce a clean ≥1-cycle differential at the known frequency," recoverable ~100× lower → real amplitude headroom, and amplitude is the lever on the safety violation. Whether a reduced-amplitude ≥1-cycle probe clears both screens is **Codex's mechanics call**.
- **Sub-finding:** W=512 spans only 0.82 of a 0.8 Hz cycle (lock-in gain 0.63); **W should cover ≥1 full probe period** (≥625 samples; W=640 → gain 1.02, NES 0.074 µε). Feeds the W/excitation co-design + pilot sweep.
- **Honesty bounds (keep loud):** this is a **detection** floor, NOT **attribution** (classifying structure-vs-actuator still needs the trained head reading differential shape/phase across the 4 stations); rejection assumes thermal/drift energy stays well below the probe band (true for the modeled slow thermal; real deployment must verify).

## What I did this session (Session 9)

1. **Closed the estimator review-cycle loop** — genuine owner re-review of Codex's three S8 corrections to `estimator.py`, reproduced with my own 27-check script (scratchpad `s9_reverify.py`), then same-state approval:
   - **Fixed-shape `[W,D]` startup** (left-pad older rows zero+masked, real data right-aligned, reject T>W) — correct; padded rows masked so they never leak into features/learned rungs.
   - **Per-channel measurement-time slopes** (each channel uses its own `measurement_time_s`, not the q_obs grid) — correct per schema §C.
   - **Causal oracle onset** (`OracleInterface(onset_time_s=…)`: healthy/-1/NaN/+inf before onset, perfect + `detection_time_s=onset` after) — correct; an oracle is privileged, not prophetic.
   - Plus validation hardening (causal `detection_time_s ≤ decision_time_s`, strictly-increasing trace) and the honest `W=512` rationale correction — confirmed compatible with the real online seam.
2. **Approved Codex's contact/safety role proposal** (`contact_state[2]`, `safety_flag[7]`, conservative thresholds) as the development state. Noted: the eval's "no safety regression" clause will consume `safety_flag` (I wire it when widths land); the 500 µε gauge over-range flag is a genuine over-range guard.
3. **Built the synchronous-detection noise-floor analysis** (the session's main contribution — see above). Packet **80 → 85 tests**.
4. **Chat turn** posted at the physical tail (approval + contact/safety + finding + proposals). **Live-Run README** running-log entry + banner date. references, README, this rewrite, human report, git.

## The single most important thing to do next session (Session 10)

**Advance the shared excitation↔detector co-design, and keep my lane moving on what's unblocked.** Priority order:

1. **Check Codex's reply to my S9 turn** in the active Phase-2 chat. Two things I proposed and Codex may respond to: (a) build a **synchronous (lock-in) feature** into `WindowFeatureExtractor` keyed to the probe frequency — this is the estimator increment that *realizes* the ~100× floor advantage; I'll build it once we agree it's the right response and the probe spectrum is settling; (b) fold **"W ≥ one probe cycle"** into the config/pilot.
2. **If Codex has redesigned the probe** (its lane), align the synchronous feature to the new probe spectrum and re-run the floor analysis against it.
3. **Wire the eval's "no safety regression" check to `safety_flag`** once Codex lands the nonzero contact/safety roles + schema-width amendment.
4. **Deferred, still waiting on the config freeze + confirmatory data:** the learned attribution rungs (matched temporal-attribution net + RMA latent) — need PyTorch (CUDA build, GPU-verified sm_120) installed *at that point, not before*; and (post-freeze, pre-pilot, needs real multi-run storage) the §D deployable-loader leakage test + whole-trajectory/fault-setting split audit.

**Do NOT freeze a partial config.** Open freeze items (all still open): Codex's excitation redesign + safety implementation; joint sanity-check of non-load-bearing sensor constants; shared severity/onset grids; `W`/stride pilot sweep (now include W≥1 cycle); validation-derived class/abstention/selective/OOD thresholds.

## Coordination state (chats)

- **Active Phase-2 chat:** `chats/Claude-Codex/Phase 2 Integration and Config Freeze/…- Active.md`. **My S9 turn is the physical tail** (posted 2026-07-19 20:21 PDT): estimator same-state approval (loop closed), contact/safety approval, synchronous-detection finding + 3 proposals. **Codex has not replied to my S9 turn yet — check it next session.**
- **MONITORING DUTY IS STANDING:** if I ever see a reply land anywhere but the physical end of a transcript, flag it in `Claude-Codex-Human`. (I append via matching the unique physical tail and re-verify. Did so S9 — landed clean, appears once.)
- **Config-freeze table (current):** *Settled:* `f_ctrl=500`, `dt=0.002`, sim step `1e-4`, `n_def=90`, 4 gauge stations, diagnostic `1.0 N`/`0.8 Hz` amplitude/freq (as mechanics parameters). *Open/blocking:* diagnostic **duration/envelope/controller** (Codex — concrete BLOCK; redesign for both signature + safety; my synchronous finding moves the signature target), contact/safety **widths+thresholds** (Codex — proposed S8, I approved S9; implement nonzero roles), severity/onset grids (shared, pilot-informed), non-load-bearing sensor constants (mine — joint sanity-check), `W=512`/`stride=8` (mine — pilot sweep, now W≥1 cycle).
- **Non-blocking forward item (carry to Technical Report):** Hendriks et al. 2022 split-leakage cautionary case → methods rationale for the whole-group split. In both ledgers.

## My estimator lane — current state (reference for next builds)

`Reproducibility Packet/scripts/utils/estimator.py` (jointly approved S9): `EstimatorOutput`/`EstimatorTrace` (§D contract, validated, causal); `WindowFeatureExtractor(window_steps=W)` — **fixed `[W,D]` left-padded** tensor + summary features (per-channel-time slopes), suite-agnostic over the 18-col registry; `WindowNoveltyDetector` — interpretable detect + calibrated-abstention (top-k sigma-above-healthy, persistence-latched detection, honest healthy-vs-not simplex, **abstains on fault type**); `OracleInterface(onset_time_s)` — allowlisted privileged ceiling, causal; `EstimatorCommandPolicy` — the `run_online_rollout` `CommandPolicy` adapter (estimator every `stride` decisions, ZOH between; recovery command injected, defaults to passive zero — **recovery controller stays Codex's lane**).
- **Next estimator increment (proposed, not built):** a **synchronous/lock-in feature** at the probe frequency added to `WindowFeatureExtractor` — this is what turns the ~100× floor headroom into a real detector capability. Build once agreed + probe spectrum settling.
- **Learned rungs (specified, not built):** `TemporalAttributionNet` (headline; shared temporal encoder over `[W,D]` → class/unknown/location/severity heads) + `RMALatentEncoder` (adapt-without-attribution control comparison). Post-freeze; need PyTorch + confirmatory data. Do NOT ship untrained shells or report performance before frozen data.

## Schema v1.0 mental model (in force; rendered in `utils/schema_types.py` §B/§0/§C/§E + `utils/estimator.py` §D)

File: `Reproducibility Packet/schema/schema-v1.0.md`.
- **§A identity/pairing/splits:** `scenario_spec_id` (shared in pair) · `pair_id` (matched C1-vs-S) · `run_id`. Identity manifest **non-deployable**. Splits by whole trajectory AND whole fault setting; **suite never a split input**; enforced by an executable pre-fit audit (to build, post-freeze). CRN within a pair: shared seeds + deterministic substreams keyed by (pair_id, channel, step) — `utils/rng.py`.
- **§B privileged plant record** (lossless `PlantStepState`; `observable_sources()`/`observable_step_sources()` expose only the measurable subset): q/qd/qdd_true, tau_cmd (pre-limit), **control_effort** (saturated, pre-fault — what the proxy senses), **tau_delivered_true** (post-fault), deform_coords[90], curvature_true[4], gauge_true[4] µε, temperature_true[4], imu_true[6], contact_state, task_reference + true deformed tip + tracking_error, safety/saturation.
- **§C observed record** (deployable suites, fixed 18-col registry, unavailable=NaN): corrupted q_obs + causal qd_obs, tau_cmd, current_proxy_obs (C1/S; noisy nominal-Kt current, **upstream** of gain loss), imu_obs (C1/S), **4 signed surface-strain gauge_obs (S only)**. `OnlineSensorSession` is the authoritative stateful path; `available_record(decision_time, history_steps)` = the past-only, availability-masked, bounded window the estimator reads.
- **§D labels/outputs/causality/leakage:** labels stored separately. Estimator outputs rendered in `EstimatorOutput`. **Automated leakage test fails the build** if a deployable loader reaches identity/privileged/label/other-suite arrays (to build, post-freeze). Past-only windows. **O = separate allowlisted `OracleInterface`.**
- **§E storage:** non-deployable `manifest.csv` + per-role roots/indexes (`plant/`, `observations/<suite>/`, `labels/`, `estimator_outputs/<suite>/`, `controller_logs/<suite>/`); each index carries provenance + sha256; observation index carries safe `split`.
- **§F frozen constants:** f_ctrl, dt, **W, stride**, onset convention, `[t_c,t_c+5s]` — names/rules in schema, **values in `config.json`**, frozen before confirmatory generation.
- **§G tracking metric:** `J_5s = ∫‖e(t)‖dt`, e = task_reference − **true deformed tip**, planar (x,y), L2, control-grid, trapezoidal, m·s. Rendered in `utils/metrics.j_5s`. Bar = ≥10% reduction vs C1.

## The agreed contract's load-bearing specifics (carry this)

- **Sensor suites (controlled variable):** **C0** = joint encoders + commanded actuation · **C1** = C0 + noisy motor-current nominal-Kt torque estimate + one distal 6-axis IMU · **S** = C1 + **four fixed strain/curvature gauge stations** · **O** = privileged oracle. External pose/vision + true delivered torque excluded from deployable suites.
- **Two settled correctness points (implemented + verified):** (1) actuator-gain fault acts *downstream* of the current proxy → C1 not handed true delivered torque; (2) encoder (sensor) fault has a *relational* signature — a lying sensor doesn't deform the structure; identified by disagreement between corrupted encoder and independently-evolved gauge/physical history.
- **Success bar (pre-declared, BOTH layers required):** S improves held-out four-way **macro-F1 over C1 by ≥0.05 absolute** (paired 95% interval excludes zero; every source-class recall difference lower-95%-bound above **−0.02**) **and** reduces the **5-s post-change integral of absolute tracking error by ≥10%** (paired interval excludes zero; no safety regression), **under realistic confounds**. Known-class abstention scored as error in headline macro-F1; calibration/selective/OOD reported separately. Rendered in `utils/metrics.py` + `utils/stats.py` (crossed pair×seed bootstrap).
- **Failure shapes:** *hypothesis failure* (C1+temporal adaptation matches S — clean negative) vs *method failure*. **Inconclusive shapes:** diagnostic-only · fault-specific/bounded · confound-fragile · **excitation-dependent** (← the current live risk; the bounded-burst BLOCK is exactly this, and my S9 finding is a candidate way out of it).
- **Pre-specification:** bars fixed before the pilot; freeze gauge placement, model/hyperparams, thresholds, analysis window, seeds/scenarios before confirmatory generation. Leakage-free splits. ≥5 training seeds. Paired hierarchical bootstrap.

## Labor split (agreed, unchanged)

- **Codex:** feasibility spike + physics (MuJoCo cable/rod done → `CablePlant` + online loop done; bounded-excitation envelope + sensitivity done S8; PyElastica fallback), virtual-gauge extraction, **excitation design (currently redesigning the probe — the live blocker)**, interpretable residual/linear-sysID baseline, recovery controller, contact/safety implementation.
- **Claude (me):** fault-injection + sensor-realism model (done S6, approved S7), two-layer evaluation harness + metrics + stats (done S7, corrected+approved S8), diagnosis-estimator front + window contract + oracle + seam adapter (done S8, **approved S9**), **synchronous-detection noise-floor analysis (done S9)**, matched temporal-attribution net + RMA latent (next, needs torch + frozen data), synchronous feature (proposed), Slot-8 verification demo, default-writer artifacts (Technical Report, Accessible Piece, Study Guide Pass 2 — Codex reviews).
- **Shared:** the plant→signals→estimator schema (in force), fault library, Reproducibility Packet, references reconciliation (Phase 2). The **"does attribution improve control" headline experiment is shared** at the diagnosis→control seam (my `EstimatorCommandPolicy` is the socket; Codex's recovery controller is the injected command). The **excitation↔detector co-design is now an active shared thread** (my synchronous finding meets Codex's probe redesign).

## Constraints / environment (unchanged, load-bearing)

- **Simulation-only, one desktop:** Windows 11, Ryzen 7 8700F (8C/16T), RTX 5060 Ti **16 GB VRAM** (Blackwell/sm_120), 32 GB RAM, Python **3.12.10** in `./venv` (use `.\venv\Scripts\python.exe` / `pip.exe`, never bare). Free/OSS, commercial-use-friendly only.
- **venv has:** numpy 2.5.1, scipy 1.18.0, scikit-learn 1.9.0, matplotlib 3.11.0, mujoco 3.10.0, pandas 3.0.3, control 0.10.2, gymnasium 1.3.0, pytest 9.1.1. **PyTorch NOT installed** — install CUDA build when building the learned rungs (verify sm_120 kernel actually runs), pin immediately.
- **Running packet tests:** from `Reproducibility Packet/`, `..\venv\Scripts\python.exe -m pytest tests/` (each test self-inserts `scripts/` on `sys.path`; no conftest). Running a script: from `Reproducibility Packet/scripts/`. **Full packet: 85 tests green (S9).**
- **Packet `.gitignore` ignores `*.npz`** (+ caches/logs); small JSON/CSV/MD result artifacts are intentionally tracked (my `results/synchronous_detection_floor/`, Codex's `results/bounded_burst_sensitivity/`).
- **Software-engineering standard for every script:** `argparse` with `required=True` for input roots (or defaulted project-relative outputs), no hard-coded paths, one clear purpose, shared logic in `utils/`, docstrings, prints progress, fails loud. (`utils/` library modules are the import-not-CLI exception — no argparse there.)
- **Licensing:** code MIT, prose CC BY 4.0. No relaxed standard requested.

## Pointers

- Claim Sheet (in-force contract): `Claim Sheet.md` · plain-language: `Accessible Claim Sheet.md` · Study Guide Pass 1: `Study Guide/Pass 1 - Conceptual Foundation.tex`
- **Shared schema (in force):** `Reproducibility Packet/schema/schema-v1.0.md` — rendered in `utils/schema_types.py` + `utils/estimator.py`
- **My lanes:** sensor `utils/{schema_types,sensor_model,rng,synthetic_plant}.py`; eval `utils/{metrics,stats}.py`; estimator `utils/estimator.py`; **synchronous floor `scripts/analyze_synchronous_detection_floor.py`** + `results/synchronous_detection_floor/`. Tests: `tests/test_{sensor_model,metrics,stats,estimator,synchronous_detection_floor}.py`.
- **Codex's plant lane:** `utils/{cable_mechanics,cable_plant,online_loop}.py`, `scripts/{make_mujoco_plant_trace,run_feasibility_spike,run_bounded_burst_sensitivity}.py`, `tests/{test_cable_plant,test_feasibility_spike,test_online_loop}.py`; bounded-burst artifact `results/bounded_burst_sensitivity/`.
- **Active Phase-2 chat:** `chats/Claude-Codex/Phase 2 Integration and Config Freeze/…- Active.md` (my S9 turn = tail; Codex reply pending). Concluded chats have `Summary.md`s.
- Director requests: `director_requests.md` (root) — entry 1 (Claim Sheet review) non-blocking, awaiting director reply.
- My foundation `agents/Claude/Literature Foundation.md` · ledger `agents/Claude/references.md` (S9 synchronous-floor mapping added) · progress reports `agents/Claude/Progress Reports/` (Phase 0/1 Close, Session 8). **Next regular: Session 16.**
- Live-Run README (co-maintained): root `README.md` — **Phase 2 / In Progress** (S9 running-log line added).
- Scratchpad (not committed): `s9_reverify.py` (27-check estimator re-review), `sync_smoke/`, `sync_w640/` (W=640 cross-check).
