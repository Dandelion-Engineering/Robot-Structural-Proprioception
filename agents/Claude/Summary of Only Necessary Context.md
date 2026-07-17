# Summary of Only Necessary Context — Claude

*Rewritten every session. Restores my working context for the next session. Excludes anything already in `Project Details/Project Details.md` and `AgentPrompt.md` (I re-read those in full at session start). Last rewritten: end of Session 4, 2026-07-16.*

## Where the project is

- **Phase 1 (Sharpening), near close.** Three gates had to close before Phase 1 ends. As of end of Session 4:
  1. **Claim Sheet — AGREED** (both approved same state; closed my Session 3). The contract is in force; changes run through the **amendment protocol**, not casual editing.
  2. **Accessible Claim Sheet — AGREED** (review loop **closed** my Session 4: Codex edited+approved in its S3; I re-reviewed the exact edits against the contract and approved the same state).
  3. **Study Guide Pass 1 — AGREED** (review loop **closed** my Session 4, same way; I also independently recompiled the PDF: 13 pp, clean).
  - **Remaining gate: the shared schema.** I wrote **`Reproducibility Packet/schema/schema-v1.0.md`** (proposed v1.0) and handed it to Codex for final same-state approval. **This loop is still OPEN.**
- **Phase 1 closes when the schema loop closes.** I did **not** fire the phase-close triggers (correct — not all gates are closed).
- I am **Claude**; last session was **Session 4**; next session I run is **Session 5**.
- **Progress-report cadence:** next *regular* one is my **Session 8**. Event triggers (phase transition, approved amendment) can come sooner — in particular, **whoever's session closes Phase 1 writes the phase-transition progress report**. I wrote none in Session 4 (no phase closed). Per-session counter keeps advancing under event-triggered reports.

## The single most important thing to do next session

**Open the active chat and read Codex's response to schema v1.0.** Path: `chats/Claude-Codex/Claim Sheet Review and Division of Labor/…- Active.md`. Two branches:

1. **If Codex approved v1.0 as-is (or I approve its edits) → the schema loop closes → Phase 1 closes.** Whoever's session lands the convergence fires the phase-close triggers **exactly once**:
   - Create **`director_requests.md`** at project root, first entry: *Claim Sheet ready for director review* (non-blocking — read `Playbooks/director-requests.md`).
   - Flip the **Live-Run README** banner to **Phase 2** (read `Playbooks/live-run-readme.md`; overwrite the status banner, keep the log append-only).
   - Write the **phase-transition progress report** in `agents/Claude/Progress Reports/` (read `Playbooks/research-progress-report.md`; Accessible-Piece bar, jargon-free, credible links).
   - Then **Phase 2 begins.**
2. **If Codex edited v1.0 and handed it back → genuinely re-review both its feedback and edits** (read `Playbooks/review-cycle.md`), then approve the same state or edit-and-return. Loop closes only when both approvals name the *same* state. Escalate to the director if a specific point hasn't converged in ~2 round-trips.

**My first Phase-2 actions (once schema is versioned):** build the **sensor-realism + fault-injection model** and the **evaluation-harness skeleton** against the agreed schema. Codex's first action is the **feasibility spike** (the gate — nothing commits until it clears).

## What I did in Session 4 (so I don't redo it)

- **Closed both companion-artifact review loops.** Diffed Codex's edits (`git 3d4000b..4bbd5b6`), re-reviewed each edit against the agreed Claim Sheet + each playbook checklist, verified fidelity (every restored metric matches Slot 7/10/11), re-verified the Silveira citation against my own ledger, and **independently recompiled the Study Guide** (13 pp, 0 box warnings, no LaTeX warnings, no undefined refs). Approved both same states in chat.
- **Approved schema v0.2 in substance, resolved the open tracking-metric decision, wrote v1.0.** Handed `Reproducibility Packet/schema/schema-v1.0.md` to Codex for same-state approval.
- **Flagged the Wensing consistency point** (see below) transparently rather than silently editing the contract.
- **Live-Run README:** one lean log entry (companions approved; schema drafted v1.0) + orientation accuracy. Did **not** flip the phase.
- No new `references.md` entry (no genuinely new source ingested; Silveira already logged).

## The schema v1.0 I proposed (so I can defend/continue it)

File: `Reproducibility Packet/schema/schema-v1.0.md`. It adopts **Codex's v0.2** in substance and adds four clarifications marked **[C4]**. Core structure:
- **§A Identity/pairing/splits:** `scenario_spec_id` (exogenous spec, shared in a pair) · `pair_id` (matched C1-vs-S, shared) · `run_id` (one rollout, distinct per suite — trajectories diverge after adaptation). Manifest = one row per rollout. Splits by whole trajectory×fault-setting group; **suite never an input to the split**. **[C4] Common random numbers within a pair** (shared sim/fault/sensor seeds; shared channels drawn from the same noise stream → S differs from C1 only by the added gauges + causal divergence). **[C4] `estimator_id`/`controller_id` = fixed architecture+protocol across compared suites.**
- **§B Privileged plant record** (per run, fixed control grid): q/qd/qdd_true, tau_cmd, **tau_delivered_true** (actuator fault applied here, downstream of the proxy), deform_coords, curvature_true[4], gauge_true[4] µε, imu_true[6], temperature_true, contact, **task_reference + true_task_output ([C4] the true *deformed* tip, not rigid FK) + tracking_error(+norm)**, effort/saturation/safety.
- **§C Observed record** (deployable suites): corrupted encoder q_obs + causal qd_obs, tau_cmd, current_proxy_obs (C1/S; noisy nominal-Kt current, **upstream** of gain loss), imu_obs (C1/S), **4 signed surface-strain gauge_obs (S only)**. C0⊂C1⊂S via static `suite_available_mask`; per-sample `valid_mask`; explicit latency/age; unavailable channels = NaN. Sensor faults → observation path only; structural/actuator → plant path.
- **§D Labels/outputs/causality/leakage:** labels stored separately; estimator outputs (p_class[4], unknown_score, abstain, location, severity+uncertainty, detection_time) separate from controller logs; **[C4] automated leakage test** must fail the build if a deployable loader can reach privileged/label/other-suite arrays; past-only windows with measurement/availability timestamps; O = separate allowlisted interface.
- **§E Storage:** `manifest.csv` + non-pickled `.npz` per rollout + immutable `schema.json`/`config.json` + SHA-256. No Parquet/YAML dependency. Project-relative paths, argparse `required=True`.
- **§F Frozen constants:** f_ctrl, dt, window W (past-only), stride, onset convention, `[t_c, t_c+5s]` — names/roles here; **values in `config.json`**, frozen before confirmatory generation.
- **§G Tracking metric (RESOLVED):** `J_5s = ∫_{t_c}^{t_c+5} ‖e(t)‖ dt`, e = task_reference − **true deformed tip**, planar (x,y), metres, **L2**, control-grid, **trapezoidal**. Bar = ≥10% reduction vs C1 (paired 95% interval excludes zero, no safety regression).
- **§H Deliberately open** (in frozen config, not pretended settled): exact gauge locations (from the spike), `n_def`, numeric f_ctrl/W/stride, severity grids/onset distribution, diagnostic-excitation budget.

## The agreed contract's load-bearing specifics (carry this mental model)

- **Sensor suites (the controlled variable):** **C0** = joint encoders + commanded actuation · **C1** = C0 + *noisy motor-current* → nominal-constant torque *estimate* + one distal-link 6-axis IMU · **S** = C1 + **four fixed strain/curvature gauge stations (two per link)** · **O** = privileged oracle. External pose/vision and *true delivered torque* excluded from deployable suites.
- **Two correctness fixes from Codex I carry as settled understanding:**
  1. **Actuator-gain fault acts *downstream* of the current proxy** → C1 is *not* handed true delivered torque, so actuator attribution stays non-trivial.
  2. **Encoder (sensor) fault has a *relational* signature**, not a physical strain change: under matched open-loop excitation a lying sensor doesn't deform the structure; it's identified by a repeatable *disagreement* between the corrupted encoder and the independently-evolved gauge/physical history (analytical-redundancy thesis in miniature).
- **Wensing scope (consistency note I raised S4, unresolved-optional):** the theorem is specifically about **rigid-body inertial-parameter** identifiability. Codex correctly narrowed it in *both* derived artifacts; the technical Claim Sheet's narrative (on-ramp + Slot 2) still carries the looser "some structural changes invisible in principle" gloss. That gloss is defensible-as-written (inertial redistributions *are* structural changes in the nullspace), so I recommended **forward-propagation** (carry the precise scoping into the Technical Report) rather than reopening the agreed contract. If Codex wants the technical sheet's two narrative mentions tightened for exact sync, that's an optional non-blocking touch-up — check its S4-reply for a response.
- **MuJoCo caveat:** generic 1-D `flex` is a *stretchable line*; the elasticity extension's **cable model** provides bending/twisting. The spike must test the bending-capable path (slender 3-D solid only if needed). PyElastica Cosserat = fallback + independent validation (**a fallback plant can't validate itself** — needs a separate beam/FEM check). FEM offline only.
- **Success bar (pre-declared, both layers required):** S improves held-out four-way **macro-F1 over C1 by ≥0.05 absolute** (paired 95% interval excludes zero; every source-class recall difference has **lower 95% bound above −0.02**) **and** reduces the **5-s post-change integral of absolute tracking error by ≥10%** (paired interval excludes zero; no safety regression), **under realistic confounds**. Known-class abstention scored as error in headline macro-F1; calibration/selective/OOD reported separately.
- **Failure shapes:** *hypothesis failure* (C1+temporal adaptation matches S — clean negative) vs *method failure* (spike can't produce differential signatures / structural channel is an algebraic echo / label leakage — disclosed, not dressed up). **Inconclusive shapes:** diagnostic-only · fault-specific/bounded · confound-fragile · excitation-dependent.
- **Pre-specification (not "pre-registration"):** bars fixed *before* the pilot; the pilot sizes the test, not the bar. Freeze gauge placement, model/hyperparams, class+abstention thresholds, analysis window, seeds/scenarios in a versioned config before confirmatory generation. Leakage-free splits by whole trajectories/fault settings. ≥5 training seeds. Paired hierarchical bootstrap (SciPy = CI primitive only; the nested resampling is ours).

## Labor split (agreed)

- **Codex:** feasibility spike + physics (MuJoCo cable/rod, PyElastica fallback, independent beam/Cosserat validation), virtual-gauge extraction, excitation design, interpretable residual/linear-sysID baseline, recovery controller (gain-scheduling/MPC).
- **Claude (me):** fault-injection + sensor-realism model (drift/thermal/hysteresis/dropout), matched temporal attribution estimator + capacity ladder + calibration/abstention, RMA-style latent baseline + oracle, two-layer evaluation harness + metrics + stats, Slot-8 verification demo, default-writer artifacts.
- **Shared:** the plant→signals→estimator **schema** (v1.0 in final review), fault library, Reproducibility Packet, references reconciliation (Phase 2). The **"does attribution improve control" headline experiment is shared** at the diagnosis→control seam.

## Constraints / environment (unchanged, load-bearing)

- **Simulation-only, one desktop:** Windows 11, Ryzen 7 8700F (8C/16T), RTX 5060 Ti **16 GB VRAM**, 32 GB RAM, Python **3.12.10** in `./venv` (use `.\venv\Scripts\python.exe` / `pip.exe`, never bare). Free/OSS, commercial-use-friendly only.
- **Tools:** MuJoCo (Apache-2.0), PyElastica (MIT), NumPy/SciPy, PyTorch CUDA build (verify GPU), matplotlib ≥300 DPI. Pin every dep in `requirements.txt` when installed. FEM (SOFA/FEniCSx) offline-only. JAX-GPU needs WSL2 — avoid.
- **Licensing:** code MIT, prose CC BY 4.0. No relaxed standard requested.
- **LaTeX:** MiKTeX pdflatex works. Study Guide preamble has `\usepackage{xcolor}` (needed for hyperref link colors). Direct aux files to scratch (I used the session scratchpad `sgbuild/`); `.gitignore` covers aux and keeps final PDFs tracked. Recompile with two passes for TOC.

## Pointers

- Claim Sheet (agreed contract): `Claim Sheet.md` · plain-language companion (agreed): `Accessible Claim Sheet.md`
- Study Guide Pass 1 (agreed): `Study Guide/Pass 1 - Conceptual Foundation.tex` (+ PDF)
- **Shared schema (v1.0 proposed, awaiting Codex):** `Reproducibility Packet/schema/schema-v1.0.md`
- Active Phase-1 chat: `chats/Claude-Codex/Claim Sheet Review and Division of Labor/…- Active.md`
- Phase 0 chat (concluded) + Summary: `chats/Claude-Codex/Phase 0 Coordination/`
- My foundation: `agents/Claude/Literature Foundation.md` · Codex's: `agents/Codex/Literature Foundation.md`
- My ledger: `agents/Claude/references.md` · Codex's: `agents/Codex/references.md`
- Live-Run README (co-maintained): root `README.md` — Phase 1 / In Progress.
- My Phase-0-close progress report: `agents/Claude/Progress Reports/Progress Report Phase 0 Close.md`
