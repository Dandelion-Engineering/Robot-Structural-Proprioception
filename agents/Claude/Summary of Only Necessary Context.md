# Summary of Only Necessary Context — Claude

*Rewritten every session. This restores my working context for the next session. It excludes anything already in `Project Details/Project Details.md` and `AgentPrompt.md` (I re-read those in full at session start). Last rewritten: end of Session 1, 2026-07-16.*

## Where the project is

- **Phase 0 (Literature Review), not yet closed.** Phase 0 closes only when **both** agents have written their Literature Foundation **and** we've compared notes in the Claude-Codex chat. As of end of Session 1: **my** foundation is done; **Codex's is not yet written** (Codex had done no work when I started). The director is *not* involved in Phase 0.
- I am **Claude, and this was my Session 1.** Next session I run is Session 2. (Progress report is due on my sessions 8/16/24…, or on any session that closes a phase or an approved amendment — not yet.)

## What I did in Session 1 (so I don't redo it)

- Created the root **Live-Run README** (State A, public run) — `README.md`.
- Wrote my **Literature Foundation** (`agents/Claude/Literature Foundation.md`) and a ~55-source verified **`references.md`** ledger.
- Wrote my workspace **`README.md`**.
- Opened the **Claude-Codex "Phase 0 Coordination"** chat and posted (a) a kickoff and (b) a completion message with my central finding + three questions for Codex.
- `.gitignore` reviewed — already comprehensive, no change.
- Committed + pushed as "Claude Session 1."

## My central research finding (the spine of my reading)

The seed's question lives at an **under-occupied intersection**: six adjacent literatures each own one piece and none owns the whole. The unifying gap is **source attribution** — when command→sensor→motion shifts, was it the **structure**, an **actuator**, or the **sensor**?
- Self-modeling revises a body model but **trusts its sensors**.
- Fast adaptation (RMA etc.) **conflates all change into one control-latent** (no attribution).
- Online sysID has a **proven identifiability nullspace** from joint-space data (Wensing–Niemeyer–Slotine 2024).
- SHM reads dense strain but **stops before control**; soft/tactile proprioception senses distributed internal state but for **shape/contact, not health**; FDI **can't separate sensor-vs-plant** without added redundancy.

**My proposed Slot-3 direction:** distributed structural sensing as physically-grounded analytical redundancy → detect + localize + **attribute** a change (structure/actuator/sensor) with calibrated uncertainty → feed a revisable self-model for adaptive control. **Proposed smallest-sufficient question and a pre-declared clean-negative shape are written out in Section 5 of my Literature Foundation** — start there next time.

## Key constraints / assumptions to carry forward

- **Simulation-only, one desktop** (Windows 11, Ryzen 7 8700F, RTX 5060 Ti **16 GB**, 32 GB RAM, Python 3.12 in `./venv`). Free/OSS, commercial-use-friendly tools only.
- **Simulation architecture I landed on:** *hybrid* — fast rigid-body engine (MuJoCo is the strong native-Windows candidate; Apache-2.0) → **reduced-order structural model** (PyElastica Cosserat rods [MIT] for slender links, or an analytical modal/Euler–Bernoulli beam) → synthetic distributed strain/curvature/vibration, **with credible sensor drift + thermal cross-sensitivity (~10 µε/°C) and environmental drift injected**. Reserve true FEM (SOFA/FEniCSx) for *offline ground-truth/validation* only. Differentiable sim is immature at contact — don't depend on it. (Isaac Sim runs native-Windows but sits at the 16 GB VRAM floor; JAX GPU stacks need WSL2.)
- **Credible sim numbers** to keep signals honest: FBG ~1 µε / 1.2 pm/µε, 12 pm/°C; OFDR ~1 mm / ~1 µε; Z24-scale environmental frequency drift of several %; soft-sensor drift up to ~18° uncorrected. (All sourced in `references.md`.)
- **Baseline discipline:** an "advantage beyond a conventional suite" claim is only meaningful against a *strong* baseline (RMA-style latent adaptation from encoders+IMU, or Cully-style repertoire). Weak baseline = hollow result.
- **Evaluation discipline:** leakage-free (cf. CWRU caveat), include environmental confounds, model sensor pathologies rather than idealize them.

## Open questions (unsettled — resolve with Codex before/at Phase 1)

1. Is **source-attribution-with-calibrated-uncertainty** the right load-bearing claim, or too ambitious for a small first project? Leaner fallbacks: detection+localization only; or just "does distributed structural sensing beat a conventional suite at detecting a body change at all."
2. Which **baseline** is fairest?
3. Does the **hybrid simulation architecture** hold up, or is there a cleaner path to physically-credible distributed signals on this hardware?

(These three are posted to Codex in the coordination chat.)

## Next steps (in order)

1. **Cross-review:** read Codex's most recent human report + the work it points to + our active chat, and respond substantively (this is the required per-session cross-review; the review cycle only kicks in if I flag a problem in an artifact).
2. If Codex's **Literature Foundation** is up: compare load-bearing sources, settle any disagreement on the central gap, **converge on the Slot-3 question**, then **close Phase 0** (note it in chat).
3. **Open Phase 1:** read `Playbooks/claim-sheet.md`, draft the **Claim Sheet** (I'm the default writer; Codex reviews), then the **Accessible Claim Sheet**, then **Study Guide Pass 1**; agree the **division of labor**; log a **"Claim Sheet ready for director review"** entry in `director_requests.md` (create that file — it doesn't exist yet) to begin the non-blocking director review. Phase 1 close triggers a progress report from whoever closes it.
4. If Codex's foundation is **not** yet up, I can still advance: deepen a specific thread (e.g., a concrete MuJoCo+PyElastica feasibility sketch, or a sharper draft of the Slot-3 question and success/failure/inconclusive shapes) without pre-empting the Claim Sheet, and keep the chat moving.

## Pointers

- My foundation + its Section 5 (the proposed question): `agents/Claude/Literature Foundation.md`
- My source ledger: `agents/Claude/references.md`
- Coordination with Codex: `chats/Claude-Codex/Phase 0 Coordination/Phase 0 Coordination - Active.md`
- Live-Run README (I co-maintain it): root `README.md` — currently Phase 0 / `In Progress`.
