# Summary of Only Necessary Context — Claude

*Rewritten every session. Restores my working context for the next session. Excludes anything already in `Project Details/Project Details.md` and `AgentPrompt.md` (I re-read those in full at session start). Last rewritten: end of Session 10, 2026-07-19 21:44 PDT.*

## Where the project is

- **Phase 2 (Execution) is OPEN.** All Phase-1 gates closed and in force. **Schema Amendment A1 (contact/safety roles) is now jointly in force** (approved this session). Contract changes run through the **amendment protocol**, not casual editing.
- I am **Claude**; last session was **Session 10**; next session I run is **Session 11**.
- **Next regular director progress report: my Session 16.** (Phase-0-close, Phase-1-close, and Session-8 reports exist; they don't reset the per-agent counter. Session 10 closed no phase; A1 is a **schema** amendment, not a **Claim Sheet** amendment, so it does **not** trigger a progress report — Codex reads it the same way.)
- **`config.json` is deliberately NOT frozen** and cannot be until the open freeze items resolve. Current role hashes are `dev-`; no trace may enter confirmatory analysis.
- **Packet: 100 tests green** (was 91 at S10 start; +5 synchronous-feature, +4 safety-gate).

## Review-cycle state (READ THIS FIRST next session)

- **I closed BOTH loops Codex opened at its S9 turn** (genuine owner re-reviews, evidence reproduced independently):
  1. **Synchronous-floor artifact** — approved same-state. Codex's 3 corrections all right (phase-invariant joint regression in new shared `utils/synchronous.py`; W=640 full cycle; honest thermal/surrogate wording). I reconstructed the *old* statistic and reproduced its 0.345–1.159 phase spread (defect was real), confirmed the new fit is phase-invariant to ~1e-15, and reproduced NES 0.111 µε / 90× bit-for-bit.
  2. **Amendment A1** — approved same-state → **A1 in force**. Independently tripped each of the 7 safety limits (each fires its own flag in order, from privileged truth); contact guard fails loud.
- **I handed back TWO NEW increments for Codex's review** (this OPENS loops on Codex's side — do NOT infer approval; Codex re-reviews in its next session):
  1. `utils/estimator.py` — the synchronous feature + `RECOMMENDED_WINDOW` 512→640.
  2. `utils/metrics.py` — the safety-regression gate.
- **My S10 chat turn is the physical tail** of the active Phase-2 chat (posted 2026-07-19 21:44 PDT). **Codex has not replied yet — check next session.**
- **MONITORING DUTY IS STANDING:** if I ever see a reply land anywhere but the physical end of a transcript, flag it in `Claude-Codex-Human`. (Append by matching the unique physical tail + re-verify. Did so S10 — clean, appears once.)

## What I built this session (Session 10)

1. **Synchronous (lock-in) feature in `WindowFeatureExtractor`** (`utils/estimator.py`, my lane). Per registry column, `window_features` now appends a harmonic amplitude at the 0.8 Hz probe frequency (fixed per-column layout `[last, mean, std, slope, sync, valid_frac]`), computed with the **shared** `utils.synchronous.harmonic_amplitude` on each channel's own measurement grid, **gated to emit only when the column's valid samples span ≥ one full probe period** (else 0.0). The learned rungs still read the raw `[W,D]` tensor (unchanged). This is the interpretable realization of the ~100× detector headroom the S9 floor analysis found.
   - **Coupled decision: `RECOMMENDED_WINDOW` moved W=512 → W=640.** A 512-sample window at 500 Hz spans 1.024 s < the 1.25 s (0.8 Hz) period, so the feature could never resolve a cycle and would be inert by default. 640 (1.278 s) covers a full cycle. **Both W and stride=8 remain pilot-sweep proposals, NOT frozen** (sweep W∈{512,640,768}, stride∈{4,8,16}).
   - New constants in estimator.py: `DIAGNOSTIC_PROBE_HZ=0.8`, `MIN_SYNC_SAMPLES=8`, `SYNC_FEATURE_COL`, `VALID_FRACTION_COL`, `N_EXTRA_FEATURES=2`.
   - Verified on the **real** observation path: adding a 50 µε 0.8 Hz tone to a real gauge channel (691/700 valid, real dropout) shifts the harmonic cosine coefficient by exactly 50.000, sine 0 (linear superposition holds through the full pathology stack).
2. **"No safety regression" gate wired to `safety_flag`** (`utils/metrics.py`, my lane). `safety_incident_rate` (fraction of steps with any active flag), `safety_flag_rates` (per-flag attribution), `safety_regression_delta` (paired `rate(S)−rate(C1)`), all from **privileged-truth** `safety_flag`. Composes with the crossed pair×seed bootstrap: **no regression = paired 95% upper bound ≤ 0**. A tracking win S buys with more unsafe excursions is disqualified even if it clears 10%.
3. Chat turn (2 approvals + 2 builds handed back) at the verified physical tail; references S10 entry; **Live-Run README heartbeat check → no entry** (S9 entries already cover the detector story; this session is follow-through — lean-log rule says skip); human report; README; this rewrite; git.

## Coherence worth remembering

`utils/synchronous.py` (Codex, S9) is now the **single shared harmonic statistic** used by (a) Codex's mechanics safe-probe screen `screen_synchronous_safe_probe.py`, (b) the detector-floor analysis `analyze_synchronous_detection_floor.py`, and (c) my estimator's synchronous feature — all against the **same 0.405 µε development threshold**. So the pilot's 2.22× detector margin is exactly what the deployed estimator computes. The excitation↔detector co-design has closed on one statistic.

## The excitation blocker — current status (the project's dominant thread)

- **S9 finding (mine):** a synchronous detector at 0.8 Hz has NES ~0.11 µε — ~90× below the per-sample 10 µε mechanics-gate floor. So the excitation target moved from "reach 10 µε broadband" (which forced unsafe amplitudes) to "produce a clean ≥1-cycle differential at the known frequency," recoverable ~90× lower.
- **Codex's S9 mechanics follow-through:** on the *actual* four-gauge MuJoCo fault-minus-healthy traces, a **0.05 N, 0.8 Hz, one-cycle raised-cosine probe at 50% ordinary task torque** clears the corrected detector threshold by **2.22×** (structural 1.015, actuator 0.898, separation 1.090 µε) AND stays inside the safety envelope across all 4 scenarios (worst angle 1.895 rad, speed 3.909 rad/s). **This candidate advances to the pilot sweep ONLY — not frozen, not attribution, not an S-vs-C1 result.** It still fails the legacy 10 µε per-sample screen (preserved as the mechanics-selection record). The old 1.0 N bursts remain BLOCK.
- **Honesty bounds (keep loud):** detection floor, NOT attribution (classifying structure-vs-actuator needs the trained head reading differential shape/phase across the 4 stations); the linear thermal ramp is a trend-rejection check, not a bound on nonlinear/probe-band thermal.

## The single most important things to do next session (Session 11)

1. **Check Codex's reply to my S10 turn** in the active Phase-2 chat. If Codex reviewed my synchronous feature / safety metrics, close any loop it opens (genuine re-review of edits if it made any; same-state approval if it just approved).
2. **Deferred, still waiting on the config freeze + confirmatory data:** the learned attribution rungs (matched `TemporalAttributionNet` + `RMALatentEncoder`) — need PyTorch (CUDA build, GPU-verified sm_120) installed *at that point, not before*; and (post-freeze, pre-pilot, needs real multi-run storage) the §D deployable-loader leakage test + whole-trajectory/fault-setting split audit.
3. **If Codex runs the pilot sweep** (its lane): align the synchronous feature / W=640 to whatever the sweep settles; help interpret detector-margin vs safety-vs-tracking tradeoffs.

**Do NOT freeze a partial config.** Open freeze items (all still open): Codex's excitation-redesign pilot outcome; joint sanity-check of non-load-bearing sensor constants; shared severity/onset grids; validation-frozen class/abstention/selective/OOD thresholds; contact-enabled cases; `W`/stride pilot sweep (W now 640-centered).

## My lanes — current state (reference for next builds)

`Reproducibility Packet/scripts/utils/estimator.py` (my S10 edits, handed back for Codex review): `EstimatorOutput`/`EstimatorTrace` (§D contract, validated, causal); `WindowFeatureExtractor(window_steps=W, probe_frequency_hz=0.8)` — fixed `[W,D]` left-padded tensor + summary features per-column `[last, mean, std, slope, **sync**, valid_frac]` (per-channel-time slopes AND per-channel-time synchronous amplitude, ≥1-cycle gated), suite-agnostic over the 18-col registry; `WindowNoveltyDetector` — interpretable detect + calibrated-abstention (now benefits from the sync feature automatically); `OracleInterface(onset_time_s)` — allowlisted privileged ceiling, causal; `EstimatorCommandPolicy` — the `run_online_rollout` `CommandPolicy` adapter. `RECOMMENDED_WINDOW = (W=640, stride=8)` (pilot-sweep proposal).
- **Learned rungs (specified, not built):** `TemporalAttributionNet` (headline; shared temporal encoder over `[W,D]` → class/unknown/location/severity heads) + `RMALatentEncoder` (adapt-without-attribution control comparison). Post-freeze; need PyTorch + confirmatory data. Do NOT ship untrained shells or report performance before frozen data.

`Reproducibility Packet/scripts/utils/metrics.py` (my S10 edits, handed back): two-layer success-bar metrics (macro-F1 w/ abstention-as-error, per-class recall, Brier/NLL/ECE, risk–coverage, false-abstention, OOD AUROC/AUPRC/false-accept, `coverage_at_risk`; control `j_5s` + `tracking_reduction_pct`; **NEW** `safety_incident_rate`/`safety_flag_rates`/`safety_regression_delta`). `utils/stats.py` = crossed pair×seed paired hierarchical bootstrap.

## Schema v1.0 + A1 mental model (in force)

File: `Reproducibility Packet/schema/schema-v1.0.md` (rendered in `utils/schema_types.py` §B/§0/§C/§E + `utils/estimator.py` §D). **Amendment A1 (in force S10):** `contact_state[2] = {tip_contact_force_n, tip_contact_active}`; `safety_flag[7]` order = joint_angle_0, joint_angle_1, joint_speed_0, joint_speed_1, tip_workspace, gauge_abs, tip_contact_force (`saturation_flag[2]` separate). Safety computed from **privileged truth** across every scenario, never a corrupted observed channel. Dev thresholds (config values, not frozen): `|q|≤π`, `|qd|≤10 rad/s`, tip radius ≤0.82 m, `|gauge_true|≤500 µε`, tip contact force ≤5 N. `CablePlant` emits `[0,0]` contact (collision disabled) and **fails loud** if `data.ncon != 0`.
- **§A** identity/pairing/splits (splits by whole trajectory AND whole fault setting; suite never a split input; CRN within a pair via `utils/rng.py`). **§B** privileged `PlantStepState` (lossless); `observable_sources()`/`observable_step_sources()` expose only the measurable subset. **§C** observed record (fixed 18-col registry, unavailable=NaN; `OnlineSensorSession` authoritative stateful path; `available_record` = past-only, availability-masked, bounded window). **§D** labels/outputs/causality/leakage (automated leakage test fails build if a deployable loader reaches identity/privileged/label/other-suite arrays — to build post-freeze). **§E** storage. **§F** frozen constants (f_ctrl, dt, W, stride — values in `config.json`, frozen before confirmatory gen). **§G** tracking metric `J_5s`.

## The agreed contract's load-bearing specifics (carry this)

- **Sensor suites (controlled variable):** **C0** = joint encoders + commanded actuation · **C1** = C0 + noisy motor-current nominal-Kt torque estimate + one distal 6-axis IMU · **S** = C1 + **four fixed strain/curvature gauge stations** · **O** = privileged oracle. External pose/vision + true delivered torque excluded from deployable suites.
- **Two settled correctness points:** (1) actuator-gain fault acts *downstream* of the current proxy → C1 not handed true delivered torque; (2) encoder (sensor) fault has a *relational* signature — a lying sensor doesn't deform the structure; identified by disagreement between corrupted encoder and independently-evolved gauge/physical history.
- **Success bar (pre-declared, BOTH layers required):** S improves held-out four-way **macro-F1 over C1 by ≥0.05 absolute** (paired 95% excludes zero; every source-class recall diff lower-95% above **−0.02**) **and** reduces the **5-s post-change integral of absolute tracking error by ≥10%** (paired excludes zero; **no safety regression** — now wired via `safety_regression_delta`), **under realistic confounds**. Known-class abstention scored as error in headline macro-F1; calibration/selective/OOD reported separately.
- **Failure shapes:** *hypothesis failure* (C1+temporal adaptation matches S — clean negative) vs *method failure*. **Inconclusive shapes:** diagnostic-only · fault-specific/bounded · confound-fragile · **excitation-dependent** (← the live risk; the bounded-burst BLOCK is exactly this; the synchronous finding + safe-probe candidate are the current way out, pending pilot).
- **Pre-specification:** bars fixed before the pilot; freeze gauge placement, model/hyperparams, thresholds, analysis window, seeds/scenarios before confirmatory generation. Leakage-free splits. ≥5 training seeds. Paired hierarchical bootstrap.

## Labor split (agreed, unchanged)

- **Codex:** feasibility spike + physics (MuJoCo cable/rod + online loop done; bounded-excitation envelope + sensitivity done S8; **safe-probe co-design + A1 implementation done S9**; PyElastica fallback), virtual-gauge extraction, **excitation design (0.05 N one-cycle candidate → pilot sweep)**, interpretable residual/linear-sysID baseline, recovery controller, contact/safety implementation + real endpoint-contact extraction (pending, before optional-contact pilots).
- **Claude (me):** fault-injection + sensor-realism model (done S6, approved S7), two-layer evaluation harness + metrics + stats (done S7, corrected+approved S8, **safety gate added S10**), diagnosis-estimator front + window contract + oracle + seam adapter (done S8, approved S9, **synchronous feature added S10**), synchronous-detection floor analysis (done S9, review closed S10), matched temporal-attribution net + RMA latent (next, needs torch + frozen data), Slot-8 verification demo, default-writer artifacts (Technical Report, Accessible Piece, Study Guide Pass 2 — Codex reviews).
- **Shared:** the plant→signals→estimator schema (in force, +A1), fault library, Reproducibility Packet, references reconciliation (Phase 2), **`utils/synchronous.py` shared harmonic statistic**. The **"does attribution improve control" headline experiment is shared** at the diagnosis→control seam (my `EstimatorCommandPolicy` is the socket; Codex's recovery controller is the injected command).

## Constraints / environment (unchanged, load-bearing)

- **Simulation-only, one desktop:** Windows 11, Ryzen 7 8700F (8C/16T), RTX 5060 Ti **16 GB VRAM** (Blackwell/sm_120), 32 GB RAM, Python **3.12.10** in `./venv` (use `.\venv\Scripts\python.exe` / `pip.exe`, never bare). Free/OSS, commercial-use-friendly only.
- **venv has:** numpy 2.5.1, scipy 1.18.0, scikit-learn 1.9.0, matplotlib 3.11.0, mujoco 3.10.0, pandas 3.0.3, control 0.10.2, gymnasium 1.3.0, pytest 9.1.1. **PyTorch NOT installed** — install CUDA build when building the learned rungs (verify sm_120 kernel actually runs), pin immediately.
- **Running packet tests:** from `Reproducibility Packet/`, `..\venv\Scripts\python.exe -m pytest tests/` (each test self-inserts `scripts/` on `sys.path`; no conftest). Running a script: from `Reproducibility Packet/scripts/`. **Full packet: 100 tests green (S10).**
- **Packet `.gitignore` ignores `*.npz`** (+ caches/logs); small JSON/CSV/MD result artifacts are intentionally tracked (`results/synchronous_detection_floor/`, `results/synchronous_safe_probe/`, `results/bounded_burst_sensitivity/`).
- **Software-engineering standard for every script:** `argparse` with `required=True` for input roots (or defaulted project-relative outputs), no hard-coded paths, one clear purpose, shared logic in `utils/`, docstrings, prints progress, fails loud. (`utils/` library modules are the import-not-CLI exception — no argparse there.)
- **Licensing:** code MIT, prose CC BY 4.0. No relaxed standard requested.

## Pointers

- Claim Sheet (in-force contract): `Claim Sheet.md` · plain-language: `Accessible Claim Sheet.md` · Study Guide Pass 1: `Study Guide/Pass 1 - Conceptual Foundation.tex`
- **Shared schema (in force, +A1):** `Reproducibility Packet/schema/schema-v1.0.md` — rendered in `utils/schema_types.py` + `utils/estimator.py`
- **My lanes:** sensor `utils/{schema_types,sensor_model,rng,synthetic_plant}.py`; eval `utils/{metrics,stats}.py`; estimator `utils/estimator.py`; synchronous floor `scripts/analyze_synchronous_detection_floor.py` + `results/synchronous_detection_floor/`. Tests: `tests/test_{sensor_model,metrics,stats,estimator,synchronous_detection_floor}.py`.
- **Codex's plant lane:** `utils/{cable_mechanics,cable_plant,online_loop}.py`, `scripts/{make_mujoco_plant_trace,run_feasibility_spike,run_bounded_burst_sensitivity,screen_synchronous_safe_probe}.py`, `tests/{test_cable_plant,test_feasibility_spike,test_online_loop,test_safe_probe_screen}.py`; artifacts `results/{bounded_burst_sensitivity,synchronous_safe_probe}/`.
- **Shared:** `utils/synchronous.py` (Codex S9) + `tests/test_synchronous*.py`.
- **Active Phase-2 chat:** `chats/Claude-Codex/Phase 2 Integration and Config Freeze/…- Active.md` (my S10 turn = tail; Codex reply pending). Concluded chats have `Summary.md`s.
- Director requests: `director_requests.md` (root) — entry 1 (Claim Sheet review) non-blocking, awaiting director reply.
- My foundation `agents/Claude/Literature Foundation.md` · ledger `agents/Claude/references.md` (S10 entry added) · progress reports `agents/Claude/Progress Reports/` (Phase 0/1 Close, Session 8). **Next regular: Session 16.**
- Live-Run README (co-maintained): root `README.md` — **Phase 2 / In Progress**; last log entries 2026-07-19 (S9). Untouched S10 (heartbeat check → no log-worthy event).
- Scratchpad (not committed): `s10_reverify_sync.py` (18-check synchronous re-review).
