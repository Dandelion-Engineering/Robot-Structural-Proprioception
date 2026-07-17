# Summary of Only Necessary Context — Claude

*Rewritten every session. Restores my working context for the next session. Excludes anything already in `Project Details/Project Details.md` and `AgentPrompt.md` (I re-read those in full at session start). Last rewritten: end of Session 3, 2026-07-16.*

## Where the project is

- **Phase 1 (Sharpening).** The **Claim Sheet is AGREED** — both agents explicitly approved the same state (Codex edited+approved in its Session 2; I re-reviewed and approved the same state in my Session 3). The contract is now in force; changes from here run through the **amendment protocol**, not casual editing.
- **Phase 1 has NOT closed.** It closes when **both** of these land: (a) Codex reviews and approves my two companion artifacts — **`Accessible Claim Sheet.md`** and **`Study Guide/Pass 1 - Conceptual Foundation.tex`** (both **in review** as of Session 3) — through the explicit-approval review cycle; and (b) we **version the shared plant→signals→estimator schema** (I proposed a v0.1; Codex revises).
- I am **Claude**; last session was **Session 3**; next session I run is **Session 4**.
- **Progress-report cadence:** next *regular* one is my **Session 8**. Event triggers (phase transition, approved amendment) can come sooner. I did **not** write one in Session 3 (no phase closed). The per-session counter keeps advancing under event-triggered reports.

## The single most important thing to do next session

**Open the Claim Sheet chat and read Codex's latest turns**, then continue the open loops. Path: `chats/Claude-Codex/Claim Sheet Review and Division of Labor/...- Active.md`. Three things may be waiting:
1. **Codex's review of the two companion artifacts.** Per the review cycle, Codex may edit each and hand it back with explicit approval of a state. For each, I must then **re-open the artifact, genuinely re-review both feedback and edits, and either explicitly approve the same state or edit-and-hand-back.** A loop closes only when we've both approved the *same* state. (Read `Playbooks/review-cycle.md` before responding.) Keep the Accessible Claim Sheet in **exact sync** with the Claim Sheet if either changes.
2. **Codex's revision of the schema v0.1.** Converge and version it as v1.0 before either lane writes Phase-2 code.
3. **If both converge → close Phase 1.** Whoever's session lands the convergence: create `director_requests.md` and log the first entry (*Claim Sheet ready for director review*, non-blocking — read `Playbooks/director-requests.md`); flip the Live-Run README banner to **Phase 2** (read `Playbooks/live-run-readme.md`); and write the **phase-transition progress report** (read `Playbooks/research-progress-report.md`).

## What I did in Session 3 (so I don't redo it)

- **Closed the Claim Sheet review loop.** Diffed Codex's five edits (`git 293af3e..3996f55`), genuinely re-reviewed each against physics/stats/playbook/Phase-0 agreements, found no defect needing a counter-edit, and **explicitly approved the same state** in chat. Two approvals now name the same state.
- **Accepted the labor split** and the **schema-first sequencing**; **proposed a shared schema v0.1** in chat (for Codex to revise — not a committed stub).
- **Wrote `Accessible Claim Sheet.md`** (root) — full plain-language translation, all 15 slots + on-ramp + monetization, exact bounds preserved, verified concept links. Handed off for review.
- **Wrote `Study Guide/Pass 1 - Conceptual Foundation.tex`** (+ compiled 14-page PDF, clean build, 0 overfull boxes) — director-facing, for Randy specifically. Handed off for review.
- **Live-Run README heartbeat:** one lean log entry (Claim Sheet converged) + footer update; **did not** flip the phase (still Phase 1 / In Progress).
- **references.md:** logged Traub 2024 (my angle) + scikit-learn F1/calibration + SciPy bootstrap docs.
- Verified the general-concept explainer links before using them (nothing cited from memory).

## The agreed contract's load-bearing specifics (carry this mental model)

- **Sensor suites (the controlled variable):** **C0** = joint encoders + commanded actuation · **C1** = C0 + *noisy motor-current* converted with nominal motor constant to a torque *estimate* + one distal-link 6-axis IMU · **S** = C1 + **four fixed strain/curvature gauge stations (two per link)** · **O** = privileged oracle. External pose/vision and *true delivered torque* are excluded from deployable suites.
- **Two correctness fixes from Codex I now carry as settled understanding:**
  1. **Actuator-gain fault acts *downstream* of the current proxy** → C1 is *not* handed the true delivered torque, so the actuator-attribution question stays non-trivial.
  2. **Encoder (sensor) fault has a *relational* signature**, not a physical strain change: under matched open-loop excitation a lying sensor doesn't deform the structure; it's identified by a repeatable *disagreement* between the corrupted encoder and the independently-evolved gauge/physical history. This is the analytical-redundancy thesis in miniature.
- **MuJoCo caveat:** generic 1-D `flex` is a *stretchable line*, not automatically a bending beam/strain sensor. The spike must test the **cable/rod elasticity path** (and a slender 3-D solid flex only if needed). PyElastica Cosserat = fallback + independent validation. FEM offline only.
- **Success bar (pre-declared, both layers required):** S improves held-out four-way **macro-F1 over C1 by ≥0.05 absolute** (paired 95% hierarchical-bootstrap interval excludes zero; every source-class recall difference has lower 95% bound above **−0.02**) **and** reduces the **5-second post-change integral of absolute tracking error by ≥10%** (paired interval excludes zero; no safety regression), **under realistic confounds**. Known-class abstention scored as error in headline macro-F1; calibration/selective/OOD reported separately.
- **Failure shapes:** *hypothesis failure* (C1+temporal adaptation matches S — clean negative) vs *method failure* (spike can't produce differential signatures / structural channel is an algebraic echo / label leakage — disclosed, not dressed up). **Inconclusive shapes:** diagnostic-only · fault-specific/bounded · confound-fragile · excitation-dependent.
- **Pre-registration:** bars fixed *before* the pilot; the pilot sizes the test, not the bar. Freeze gauge placement, model/hyperparams, thresholds, analysis window, seeds/scenarios before confirmatory generation. Leakage-free splits by whole trajectories/fault settings. ≥5 training seeds.

## The schema v0.1 I proposed (so I can reference/defend it)

Plant lane (Codex) emits privileged ground truth; sensor/fault lane (me) consumes it and emits per-suite *observed* records; estimator (shared) consumes causal windows → attribution posterior + control. Parts: **(a)** scenario manifest (id, schema_version, seed, trajectory, suite, fault_spec, payload, env, split); **(b)** plant record (privileged: q/qd/qdd_true, tau_cmd, tau_delivered_true, deform_coords, gauge_true[4], imu_true, temperature, contact); **(c)** observation record per suite with a **channel mask** so C0/C1/S/O are the same schema with channels masked (sensor model applies noise/bias/drift/thermal/hysteresis/dropout/latency); **(d)** labels (source_class, location, severity, onset_index, compound_flag, ood_flag); **(e)** frozen windowing/timing constants (f_ctrl, window W causal, stride, 5-s post-change window); **(f)** storage: per-scenario npz/parquet + manifest + config.yaml with schema_version, project-relative paths, argparse `required=True`.

## Labor split (agreed)

- **Codex:** feasibility spike + physics (MuJoCo cable/rod, PyElastica fallback, independent beam/Cosserat validation), virtual-gauge extraction, excitation design, interpretable residual/linear-sysID baseline, recovery controller (gain-scheduling/MPC).
- **Claude (me):** fault-injection + sensor-realism model (drift/thermal/hysteresis/dropout), matched temporal attribution estimator + capacity ladder + calibration/abstention, RMA-style latent baseline + oracle, two-layer evaluation harness + metrics + stats, Slot-8 verification demo, default-writer artifacts.
- **Shared:** the plant→signals→estimator **schema** (agree before code), fault library, Reproducibility Packet, references reconciliation (Phase 2). The **"does attribution improve control" headline experiment is shared** at the diagnosis→control seam.
- **First Phase-2 actions (after schema versioned):** Codex → run the spike (the gate; nothing commits until it clears). Claude → sensor-realism + fault-injection model and the eval-harness skeleton against the agreed schema.

## Constraints / environment (unchanged, load-bearing)

- **Simulation-only, one desktop:** Windows 11, Ryzen 7 8700F (8C/16T), RTX 5060 Ti **16 GB VRAM**, 32 GB RAM, Python **3.12.10** in `./venv` (use `.\venv\Scripts\python.exe` / `pip.exe`, never bare). Free/OSS, commercial-use-friendly only.
- **Tools:** MuJoCo (Apache-2.0), PyElastica (MIT), NumPy/SciPy, PyTorch CUDA build (verify GPU), matplotlib ≥300 DPI. Pin every dep in `requirements.txt` when installed. FEM (SOFA/FEniCSx) offline-only. JAX-GPU needs WSL2 — avoid.
- **Licensing:** code MIT, prose CC BY 4.0. No relaxed standard requested.
- **LaTeX:** MiKTeX pdflatex works. Study Guide preamble needs `\usepackage{xcolor}` (added) for hyperref link colors. Direct aux files to scratch; `.gitignore` covers aux and keeps final PDFs tracked.

## Pointers

- Claim Sheet (agreed contract): `Claim Sheet.md` · plain-language companion (in review): `Accessible Claim Sheet.md`
- Study Guide Pass 1 (in review): `Study Guide/Pass 1 - Conceptual Foundation.tex` (+ PDF)
- Active Phase-1 chat: `chats/Claude-Codex/Claim Sheet Review and Division of Labor/...- Active.md`
- Phase 0 chat (concluded) + Summary: `chats/Claude-Codex/Phase 0 Coordination/`
- My foundation: `agents/Claude/Literature Foundation.md` · Codex's: `agents/Codex/Literature Foundation.md`
- My ledger: `agents/Claude/references.md` (now has a Phase-1 section) · Codex's: `agents/Codex/references.md`
- Live-Run README (co-maintained): root `README.md` — Phase 1 / In Progress.
- My Phase-0-close progress report: `agents/Claude/Progress Reports/Progress Report Phase 0 Close.md`
