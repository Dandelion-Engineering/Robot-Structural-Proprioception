# Summary — Claim Sheet Review and Division of Labor (Claude & Codex)

**Participants:** Claude, Codex
**Date Range:** 2026-07-16 (Claude Session 2 opened) → 2026-07-17 (Claude Session 6 concluded)
**Status:** Concluded — all Phase-1 review loops closed, labor split agreed, Phase 2 open. Concluded at the director's instruction (see `chats/Claude-Codex-Human/Chat Appends`), which also moved active Phase-2 coordination to a new chat.

## What this chat did

It ran the Phase-1 sharpening cross-review and settled the initial division of labor. Over the thread the two agents took four artifacts through the explicit review cycle to same-state approval, agreed the labor split, and carried the project across the Phase 1 → Phase 2 boundary.

## Outcomes (all agreed / in force)

1. **Claim Sheet — AGREED** (both approved same state, Claude S3). The in-force project contract; changes now run through the **amendment protocol**. Codex's five edits held: fixed C0/C1/S composition; encoder-fault *relational* signature (not fictitious strain); auditable abstention (known-class abstention = headline macro-F1 error); locked confirmatory contract (≥0.05 macro-F1, −0.02 per-source recall non-inferiority lower-95%-bound, ≥10% 5-s tracking-error reduction, paired hierarchical bootstrap, ≥5 seeds, config freeze before confirmatory generation); removed construction scaffolding.
2. **Accessible Claim Sheet — AGREED** (loop closed Claude S4).
3. **Study Guide Pass 1 — AGREED** (loop closed Claude S4; PDF 13 pp, clean build).
4. **Shared schema `schema-v1.0.md` — JOINTLY APPROVED AND IN FORCE** (loop closed Claude S5). Provenance chain: Claude v0.1 sketch → Codex v0.2 plant-side contract → Claude v1.0 handoff (resolved §G tracking metric + four [C4] clarifications) → Codex v1.0 edited review state (closed-loop execution order, role-separated storage + identity-manifest leak fix, executable split + CRN substream audits, three-torque semantics) → Claude S5 same-state approval. Changes now run through the amendment protocol.

**Labor split — AGREED:**
- **Codex:** feasibility spike + physics (MuJoCo cable/rod, PyElastica fallback, independent beam/Cosserat validation), virtual-gauge extraction, excitation design, interpretable residual/linear-sysID baseline, recovery controller.
- **Claude:** fault-injection + sensor-realism model, matched temporal attribution estimator + capacity ladder + calibration/abstention, RMA-style latent baseline + oracle, two-layer evaluation harness + metrics + stats, Slot-8 verification demo, default-writer artifacts (Technical Report, Accessible Piece, Study Guide Pass 2 — Codex reviews).
- **Shared:** plant→signals→estimator→controller schema (now in force), fault library, Reproducibility Packet, references reconciliation (Phase 2). The **"does attribution improve control" headline experiment is shared** at the diagnosis→control seam.

## Phase-1 close (Claude S5)

Claude's Session 5 landed the schema convergence and fired the three phase-close triggers exactly once: created `director_requests.md` (entry 1, *Claim Sheet ready for director review*, non-blocking); flipped the Live-Run README banner to **Phase 2 — Execution**; wrote the phase-transition progress report (`agents/Claude/Progress Reports/Progress Report Phase 1 Close.md`). **Phase 2 is open.**

## Phase-2 work started in this chat (now continuing elsewhere)

- **Codex feasibility spike — qualified PASS (Codex S5).** Native MuJoCo cable/rod mechanics clear the differential-signature gate **only with bounded, matched, zero-mean diagnostic excitation** (1.0 N distal load → structural 10.24 µε, actuator 23.87 µε, separation 23.87 µε, all above the unchanged 10 µε floor). Ordinary torque-only excitation **BLOCKS** (1.92 / 5.81 µε, below floor) and is preserved as a first-class negative control. Encoder fault stays relational (q_obs shifts 0.050 rad; physical gauge/IMU change 0). Numerical + independent Euler–Bernoulli checks pass. **Frozen for the config:** `n_def=90` (three-component log-map rotations for 15 internal ball joints on each of two links), gauge stations at (link1: 0.25 L, 0.75 L), (link2: 0.25 L, 0.75 L). Proposed per-step handoff object name: **`PlantStepState`**.

## Operational note (why this chat was concluded when it was)

Codex's S4 and S5 turns were each first inserted mid-file (a patch anchor matched an earlier Claude sign-off) and then corrected with append-only tail notes; no content was lost. The director asked both agents to acknowledge the failure mode, asked Codex to avoid/repair it and Claude to monitor for it, and instructed that this chat be concluded and Phase-2 work move to a new thread. Logged in the Live-Run README running log (2026-07-17).

## Where it goes next

Active Phase-2 coordination continues in **`chats/Claude-Codex/Phase 2 Integration and Config Freeze/`**: freezing the shared `config.json` (Codex's mechanics values + Claude's sensor/eval constants) before any confirmatory generation, aligning the `PlantStepState` interface and role-separated persisted plant trace, and integrating Claude's sensor-realism/fault-injection model with Codex's plant. The in-force contract is `Reproducibility Packet/schema/schema-v1.0.md`; the agreed Claim Sheet is `Claim Sheet.md` (awaiting the director's non-blocking review per `director_requests.md`).
