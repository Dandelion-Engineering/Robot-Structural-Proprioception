# Summary of Only Necessary Context — Claude

*Rewritten every session. Restores my working context for the next session. Excludes anything already in `Project Details/Project Details.md` and `AgentPrompt.md` (I re-read those in full at session start). Last rewritten: end of Session 5, 2026-07-17.*

## Where the project is

- **Phase 2 (Execution) is OPEN. Phase 1 (Sharpening) closed my Session 5.** All Phase-1 gates are closed:
  1. **Claim Sheet — AGREED** (both approved same state, my Session 3). The in-force contract; changes run through the **amendment protocol**, not casual editing.
  2. **Accessible Claim Sheet — AGREED** (loop closed my Session 4).
  3. **Study Guide Pass 1 — AGREED** (loop closed my Session 4; PDF recompiled clean, 13 pp).
  4. **Shared schema `schema-v1.0.md` — JOINTLY APPROVED AND IN FORCE** (loop closed my **Session 5**: Codex edited it in S4 and handed back; I genuinely re-reviewed the diff `3b51d0e..ce9e6bc`, agreed with every edit, gave same-state approval). Changes now run through the amendment protocol.
- **I fired all three Phase-1-close triggers this session (exactly once):** created `director_requests.md` (non-blocking first entry), flipped the Live-Run README banner to **Phase 2 — Execution**, and wrote the **phase-transition progress report** (`Progress Report Phase 1 Close.md`).
- I am **Claude**; last session was **Session 5**; next session I run is **Session 6**.
- **Progress-report cadence:** next *regular* one is my **Session 8**. The Phase-1-close report is already written and does **not** reset the per-agent counter. Event triggers (a phase transition I close, an approved amendment I write) can come sooner.

## The single most important thing to do next session

**Begin Phase 2 implementation.** Implementation and dependency installation are now **UNBLOCKED** (the schema-first gate is satisfied — v1.0 is jointly approved). My agreed first Phase-2 deliverables (build against `Reproducibility Packet/schema/schema-v1.0.md` — re-read it first; it is the contract):

1. **Sensor-realism + fault-injection model** — the observation-path lane (my ownership): corrupts the plant's privileged state into each suite's observed channels. Sensor pathologies: additive noise at the FBG floor (~1 µε), **thermal apparent strain (~10 µε/°C)**, bias/drift, hysteresis, quantization, dropout, latency. Fault injection: **sensor faults → observation path only**; structural/actuator faults are the plant lane's (Codex's) — but I own the fault *library* definitions jointly. Respect the boundary: current proxy is **upstream** of actuator-gain loss.
2. **Evaluation-harness skeleton** — the two-layer metrics (diagnosis: macro-F1 + the calibration/selective/OOD family; control: 5-s post-change tracking-error integral `J_5s` + the rest), the leakage-free split logic with the **executable split audit** and **leakage test** the schema requires, and the **paired hierarchical bootstrap** (SciPy = CI primitive only; nested resampling is ours).
3. **Create `Reproducibility Packet/` working structure + pinned `requirements.txt`** — write surviving scripts *directly into the packet folder* as they finalize (Standards: packet-ready as you go). Every script: `argparse` with `required=True` for input roots, project-relative outputs, no hard-coded paths, one clear purpose, shared logic in `utils/`, docstrings, prints progress, fails loud. Pin each dep the moment it's installed. Use `.\venv\Scripts\python.exe` / `pip.exe`, never bare.

**Depend on Codex's spike for two frozen numbers:** `n_def` (independent deformation-coordinate count) and the four gauge-station locations. Those go in `config.json`, frozen before any confirmatory generation. Until then, build against the schema's declared field shapes/roles with those two as config parameters (don't hard-code them).

**Codex's Phase-2 first action is the feasibility spike (the gate):** MuJoCo cable/rod vs. slender-3D-flex, must show differential fault signatures at credible SNR at realistic (metal-ish) stiffness. Nothing commits until it clears. If it fails → PyElastica Cosserat fallback (a fallback plant can't validate itself — needs a separate beam/FEM check).

## The schema v1.0 mental model (so I can build without re-deriving; still re-read the file to implement)

File: `Reproducibility Packet/schema/schema-v1.0.md` (in force). Structure:
- **§A Identity/pairing/splits:** three ids — `scenario_spec_id` (exogenous spec, shared in a pair) · `pair_id` (matched C1-vs-S) · `run_id` (one rollout; C1 and S each own one — they diverge after acting). **Identity manifest is NON-DEPLOYABLE** (carries `fault_setting_id` → could leak target); payload paths/hashes live in per-role indexes (§E), not here. Splits by whole trajectory **and** whole fault setting; **suite never an input to the split**; enforced by an **executable pre-fit split audit**. **Common random numbers within a pair:** shared sim/fault/sensor seeds + **deterministic substreams keyed by (pair_id, channel, step)** so S-only gauge draws can't perturb shared-channel innovations. `estimator_id`/`controller_id` = fixed architecture+protocol across compared suites.
- **§0 execution:** plant/sensor/estimator/controller **interleave online each control step**; the privileged/observed/label/output/log records are role-separated **persisted traces**, NOT an offline pipeline (C1/S diverge, so you can't generate one plant rollout and replay it through both).
- **§B Privileged plant record** (per run, control grid): q/qd/qdd_true, `tau_cmd` (pre-limit), **`control_effort`** (saturated, pre-fault, what the current proxy senses), **`tau_delivered_true`** (post-fault), deform_coords[n_def], curvature_true[4], gauge_true[4] µε, imu_true[6], **temperature_true[4]**, contact, task_reference + **true_task_output (deformed tip)** + tracking_error(+norm), effort/saturation/safety.
- **§C Observed record** (deployable suites, fixed-width registry, unavailable channels = NaN): corrupted q_obs + causal qd_obs, tau_cmd, current_proxy_obs (C1/S; noisy nominal-Kt current, **upstream** of gain loss), imu_obs (C1/S), **4 signed surface-strain gauge_obs (S only)**. Static `suite_available_mask`; per-time-per-channel `valid_mask` + measurement/availability/latency timing.
- **§D Labels/outputs/causality/leakage:** labels stored separately (only bridge from truth to target); estimator outputs and controller logs separate; **automated leakage test fails the build** if a deployable loader can reach identity manifest/provenance/privileged/label/other-suite arrays; past-only windows; O = separate allowlisted oracle interface.
- **§E Storage:** non-deployable `manifest.csv` (identity/split) + **per-role roots/indexes** (`plant/`, `observations/<suite>/`, `labels/`, `estimator_outputs/<suite>/`, `controller_logs/<suite>/`), each index carries `run_id, schema_version, config_hash, npz_path, sha256`; observation index also carries safe `split`. One non-pickled `.npz` per rollout per role. Immutable `schema.json`/`config.json`. No Parquet/YAML dependency.
- **§F Frozen constants:** f_ctrl, dt, window W (past-only), stride, onset convention, `[t_c, t_c+5s]` — names/rules here, **values in `config.json`**, frozen before confirmatory generation.
- **§G Tracking metric:** `J_5s = ∫_{t_c}^{t_c+5} ‖e(t)‖ dt`, e = task_reference − **true deformed tip**, planar (x,y), metres, **L2**, control-grid, **trapezoidal**. Bar = ≥10% reduction vs C1 (paired 95% interval excludes zero, no safety regression).
- **§H Deliberately open** (set in frozen config from the spike): gauge locations, `n_def`, numeric f_ctrl/W/stride, severity grids/onset distribution, diagnostic-excitation budget.

## The agreed contract's load-bearing specifics (carry this mental model)

- **Sensor suites (the controlled variable):** **C0** = joint encoders + commanded actuation · **C1** = C0 + *noisy motor-current* → nominal-Kt torque *estimate* + one distal 6-axis IMU · **S** = C1 + **four fixed strain/curvature gauge stations (two per link)** · **O** = privileged oracle. External pose/vision and *true delivered torque* excluded from deployable suites.
- **Two correctness fixes from Codex I carry as settled understanding:**
  1. **Actuator-gain fault acts *downstream* of the current proxy** → C1 is *not* handed true delivered torque, so actuator attribution stays non-trivial (the drop reaches C1 only through motion, confoundable with stiffness/load).
  2. **Encoder (sensor) fault has a *relational* signature** — under matched excitation a lying sensor doesn't deform the structure; it's identified by a repeatable *disagreement* between the corrupted encoder and the independently-evolved gauge/physical history (analytical-redundancy in miniature).
- **Success bar (pre-declared, both layers required):** S improves held-out four-way **macro-F1 over C1 by ≥0.05 absolute** (paired 95% interval excludes zero; every source-class recall difference has **lower 95% bound above −0.02**) **and** reduces the **5-s post-change integral of absolute tracking error by ≥10%** (paired interval excludes zero; no safety regression), **under realistic confounds**. Known-class abstention scored as error in headline macro-F1; calibration/selective/OOD reported separately.
- **Failure shapes:** *hypothesis failure* (C1+temporal adaptation matches S — clean negative) vs *method failure* (spike can't produce differential signatures / structural channel is an algebraic echo / label leakage — disclosed, not dressed up). **Inconclusive shapes:** diagnostic-only · fault-specific/bounded · confound-fragile · excitation-dependent.
- **Pre-specification (not "pre-registration"):** bars fixed *before* the pilot; the pilot sizes the test, not the bar. Freeze gauge placement, model/hyperparams, class+abstention thresholds, analysis window, seeds/scenarios in a versioned config before confirmatory generation. Leakage-free splits. ≥5 training seeds. Paired hierarchical bootstrap.
- **MuJoCo caveat:** generic 1-D `flex` is a *stretchable line*; the elasticity extension's **cable model** provides bending/twisting. Spike must test the bending-capable path (slender 3-D solid only if needed). PyElastica Cosserat = fallback + independent validation. FEM offline only.

## Labor split (agreed)

- **Codex:** feasibility spike + physics (MuJoCo cable/rod, PyElastica fallback, independent beam/Cosserat validation), virtual-gauge extraction, excitation design, interpretable residual/linear-sysID baseline, recovery controller (gain-scheduling/MPC).
- **Claude (me):** fault-injection + sensor-realism model (drift/thermal/hysteresis/dropout), matched temporal attribution estimator + capacity ladder + calibration/abstention, RMA-style latent baseline + oracle, two-layer evaluation harness + metrics + stats, Slot-8 verification demo, default-writer artifacts (Technical Report, Accessible Piece, Study Guide Pass 2 — Codex reviews).
- **Shared:** the plant→signals→estimator **schema** (now in force), fault library, Reproducibility Packet, references reconciliation (Phase 2). The **"does attribution improve control" headline experiment is shared** at the diagnosis→control seam.

## Open coordination items to carry into Phase 2

- **Active chat is ready to conclude.** `chats/Claude-Codex/Claim Sheet Review and Division of Labor/` has all Phase-1 loops closed. It should be **concluded** (rename to `…- Concluded.md` + write `Summary.md`) once Codex acknowledges my Session-5 turn — concluding needs both agents' agreement, and my S5 turn opened two forward notes + a coordination point Codex may reply to. **Phase-2 coordination opens as new subject-specific chats** (e.g. spike results; sensor/eval integration).
- **Two non-blocking forward-propagation items I flagged (not edits/amendments):** (a) the Hendriks et al. 2022 split-leakage cautionary case → carry into the **Technical Report** methods rationale; (b) name the **per-step plant→sensor state object** (single-timestep slice of the §B privileged record) at Phase-2 kickoff so both lanes build the same struct.
- **Wensing scope (settled):** the two looser narrative mentions in the agreed Claim Sheet (on-ramp; Slot 2) are defensible as written; both agents agreed **not** to reopen the contract — the precise rigid-body-inertial scope propagates forward into the Technical Report.

## Constraints / environment (unchanged, load-bearing)

- **Simulation-only, one desktop:** Windows 11, Ryzen 7 8700F (8C/16T), RTX 5060 Ti **16 GB VRAM**, 32 GB RAM, Python **3.12.10** in `./venv` (use `.\venv\Scripts\python.exe` / `pip.exe`, never bare). Free/OSS, commercial-use-friendly only.
- **Tools:** MuJoCo (Apache-2.0), PyElastica (MIT), NumPy/SciPy, PyTorch CUDA build (verify GPU at install), matplotlib ≥300 DPI. Pin every dep in `requirements.txt` when installed. FEM (SOFA/FEniCSx) offline-only. JAX-GPU needs WSL2 — avoid.
- **Licensing:** code MIT, prose CC BY 4.0. No relaxed standard requested.
- **LaTeX (for Phase-3 writing / Study Guide Pass 2):** MiKTeX pdflatex works; preamble needs `\usepackage{xcolor}` for hyperref link colors; direct aux to scratch; `.gitignore` covers aux and keeps final PDFs tracked; two passes for TOC.

## Pointers

- Claim Sheet (in-force contract): `Claim Sheet.md` · plain-language companion: `Accessible Claim Sheet.md`
- Study Guide Pass 1: `Study Guide/Pass 1 - Conceptual Foundation.tex` (+ PDF)
- **Shared schema (in force):** `Reproducibility Packet/schema/schema-v1.0.md`
- Director requests: `director_requests.md` (root) — entry 1 non-blocking, awaiting director reply.
- Active Phase-1 chat (all loops closed, ready to conclude): `chats/Claude-Codex/Claim Sheet Review and Division of Labor/…- Active.md`
- Phase 0 chat (concluded) + Summary: `chats/Claude-Codex/Phase 0 Coordination/`
- My foundation: `agents/Claude/Literature Foundation.md` · Codex's: `agents/Codex/Literature Foundation.md`
- My ledger: `agents/Claude/references.md` · Codex's: `agents/Codex/references.md`
- Live-Run README (co-maintained): root `README.md` — **Phase 2 / In Progress**.
- My progress reports: `agents/Claude/Progress Reports/` (Phase 0 Close, Phase 1 Close).
