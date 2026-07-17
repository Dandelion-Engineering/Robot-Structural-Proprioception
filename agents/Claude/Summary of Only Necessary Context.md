# Summary of Only Necessary Context — Claude

*Rewritten every session. Restores my working context for the next session. Excludes anything already in `Project Details/Project Details.md` and `AgentPrompt.md` (I re-read those in full at session start). Last rewritten: end of Session 2, 2026-07-16.*

## Where the project is

- **Phase 1 (Sharpening), just opened.** Phase 0 (Literature Review) is **closed** as of my Session 2. Phase 1 closes when the agents agree on the **Claim Sheet**, the **Accessible Claim Sheet**, and **Study Guide Pass 1**, and settle the **division of labor**.
- I am **Claude**; my last session was **Session 2**. Next session I run is **Session 3**.
- **Progress-report cadence:** my sessions 8/16/24…, plus phase transitions and approved amendments. I wrote one at the Phase 0 close this session (`agents/Claude/Progress Reports/Progress Report Phase 0 Close.md`). Next regular one is Session 8. The per-session counter keeps advancing under event-triggered reports.

## The single most important thing to do next session

**Check the Phase 1 chat for Codex's Claim Sheet review and labor-split response**, then continue the review cycle. Path: `chats/Claude-Codex/Claim Sheet Review and Division of Labor/...- Active.md`.
- Per the review cycle: Codex reviews/edits `Claim Sheet.md` and hands it back with explicit approval of a state. I must then **re-open the sheet, genuinely re-review both Codex's feedback and its edits, and either explicitly approve the same state or edit-and-hand-back.** The loop closes only when we've both explicitly approved the *same* state. Read `Playbooks/review-cycle.md` before responding to the review.
- If we converge on the Claim Sheet **and** the labor split → I then write the **Accessible Claim Sheet** (read `Playbooks/accessible-claim-sheet.md`) and **Study Guide Pass 1** (read `Playbooks/study-guide.md`) — both are my default-writer artifacts, deferred deliberately this session (see decision below). Then create `director_requests.md` and log a *"Claim Sheet ready for director review"* entry (read `Playbooks/director-requests.md`) — this begins the non-blocking director review and closes Phase 1 (→ another progress-report trigger for whoever closes it).

## What I did in Session 2 (so I don't redo it)

- **Cross-review** of Codex's Session 1: read its HumanReport1 + full Literature Foundation. Strong convergence.
- **Replied to Codex** in the Phase 0 chat approving its three convergence points (with substantive reinforcement, not rubber-stamp), then **concluded** that chat (renamed to `- Concluded.md`, wrote `Summary.md`). **This closed Phase 0.**
- **Drafted `Claim Sheet.md`** (root) — full 15 slots + orientation header. I'm the default writer; it's handed to Codex for review.
- **Opened the Phase 1 chat** with the Claim Sheet handoff + a proposed division of labor.
- **Wrote the Phase 0-close Progress Report.**
- **Live-Run README heartbeat** (banner → Phase 1; one log entry; footer → Claim Sheet).
- No code/sim/deps this session (Phase 1 planning). No new references consulted (Claim Sheet drew on already-ledgered sources).

## The five settled points from Phase 0 (the Claim Sheet is built on these)

Full detail in `chats/Claude-Codex/Phase 0 Coordination/Summary.md`. In brief:
1. **The seam:** six adjacent literatures each own one piece of detect→attribute→compensate; none owns the whole. Contribution = a *controlled test* of whether local structural sensing adds source-separating information, framed as **added analytical redundancy** (not "the body computes").
2. **Staged attribution claim:** detect → classify structure/actuator/sensor-or-**abstain** → localize/severity → recover. Staging must land in the **pre-declared** success/failure/inconclusive shapes (Slots 11–13). Calibrated abstention is first-class.
3. **Matched sensor-suite ablation** is the central comparison. Nested suites **C0** (encoders+command) ⊂ **C1** (+current/torque+IMU/endpoint) ⊂ **S** (+local strain/curvature), plus **O** oracle ceiling. Sensor suite is the controlled variable; hold estimator/controller/data/window constant. Residual/linear sysID = interpretable floor; RMA-style latent = strong control baseline; IT&E = recovery *reference* only. Sweep capacity within each suite.
4. **Native-MuJoCo-flex-first feasibility spike.** Gate = **differential fault signatures at credible SNR at realistic (metal-ish) stiffness** (FBG-scale: ~1 µε res, ~10 µε/°C thermal). Native flex preferred because its deformation DOFs are **independent** of joint coords → lowers circularity/leakage risk. Fallback: PyElastica Cosserat (MIT). Full FEM offline only.
5. **Realism is part of the test:** drift, thermal cross-sensitivity, hysteresis/crosstalk, lag, finite sampling, correlated noise, held-out severities/configs. Keep **diagnosis and control metrics separate** (diagnostic-only is a valid pre-declared outcome; control can improve without attribution via a blind latent).

**Agreed Slot-3 question (verbatim):** *In a small simulated compliant manipulator, how much do local strain/curvature measurements add beyond a matched conventional proprioceptive history for detecting and distinguishing link-stiffness loss, actuator-gain loss, and encoder corruption under realistic sensor confounds, and does any improved attribution translate into better post-change tracking?* (Closing clause is an open question with a legitimate "no.")

## Key decisions to carry forward

- **Deferred the Accessible Claim Sheet + Study Guide Pass 1** to the Phase-1-close window (after the technical sheet is agreed), rather than writing them this session. Reason: they translate the *agreed* contract; writing them against a draft in review guarantees drift on Codex's first edit and misleads the director. This is a considered decision, not an omission — noted in the Claim Sheet's closing line and the handoff chat. Both are due at Phase 1 close.
- **Proposed division of labor** (open to Codex's counter, in the Phase 1 chat):
  - **Codex:** feasibility spike + physics (MuJoCo flex / PyElastica / independent beam), virtual-gauge extraction, excitation design, interpretable residual/linear-sysID baseline, recovery controller (gain-scheduling/MPC).
  - **Claude (me):** fault-injection + sensor-realism model (drift/thermal/hysteresis/dropout), temporal attribution estimator + capacity ladder + calibration/abstention, RMA-style latent baseline, two-layer evaluation harness + metrics + stats, Slot-8 verification demo, default-writer artifacts.
  - **Shared:** benchmark **data schema** (agree early), fault library, Reproducibility Packet, references reconciliation (Phase 2). The **"does attribution improve control" headline experiment is shared at the diagnosis→control seam** on purpose.
  - **First actions:** Codex → run the spike (the gate). Claude → sensor-realism + eval-harness skeleton vs. a stubbed schema, then the Accessible sheet + Study Guide once the technical sheet is agreed.
  - Flagged as negotiable: who owns the RMA baseline and the evaluation metrics (Codex named RMA as the fair comparator). Escalate to director if no convergence in ~2 round-trips.

## Constraints / environment (unchanged, load-bearing)

- **Simulation-only, one desktop:** Windows 11, Ryzen 7 8700F (8C/16T), RTX 5060 Ti **16 GB VRAM**, 32 GB RAM, Python **3.12.10** in `./venv` (use `.\venv\Scripts\python.exe` / `pip.exe`, never bare). Free/OSS, commercial-use-friendly only.
- **Primary tools:** MuJoCo (Apache-2.0, native-Windows), PyElastica (MIT). PyTorch CUDA build (verify GPU). Pin every dep in `requirements.txt` when installed. JAX-GPU would need WSL2 — avoid unless forced.
- **Licensing:** code MIT, prose CC BY 4.0. No relaxed standard requested.
- **Evaluation discipline:** leakage-free splits (by whole trajectories/fault settings, not time samples), realistic sensor pathologies, environmental confounds in both healthy and faulty data, every exclusion recorded.

## Pointers

- Claim Sheet (contract, draft in review): `Claim Sheet.md`
- Phase 1 chat (active): `chats/Claude-Codex/Claim Sheet Review and Division of Labor/...- Active.md`
- Phase 0 chat (concluded) + its Summary: `chats/Claude-Codex/Phase 0 Coordination/`
- My foundation + Section 5 (my proposed question): `agents/Claude/Literature Foundation.md`
- Codex's foundation (its §2.2 metrics, §5.2 experiment): `agents/Codex/Literature Foundation.md`
- My source ledger: `agents/Claude/references.md` · Codex's: `agents/Codex/references.md`
- Live-Run README (co-maintained): root `README.md` — now Phase 1 / `In Progress`.
- My Phase 0-close progress report: `agents/Claude/Progress Reports/Progress Report Phase 0 Close.md`
