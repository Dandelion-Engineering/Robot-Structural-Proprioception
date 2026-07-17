# Director Requests

This file is the project's **single source of truth for work only the director (Randy) can do** — reviews that need his judgment, or actions that need his identity, login, or accounts. It is **append-only**: agents add entries, the director replies in place under an entry, and nothing is deleted or rewritten. When an agent hits director-only work it logs it here, names a fallback, and keeps moving so the project never stalls waiting. See `Playbooks/director-requests.md` for the full protocol.

**Format of each entry:** date · what's needed · why · what's blocked · fallback (what the agents do meanwhile). The director appends a brief reply line under an entry when he resolves it.

---

## 1. Claim Sheet ready for director review — *(non-blocking)*

**Date:** 2026-07-17 (logged by Claude, Session 5, at Phase 1 close)

**What's needed:** Randy's review of the project's now-agreed **Claim Sheet** — the contract both agents converged on in Phase 1. His review is the **first invocation of the amendment protocol**: he can approve it as-is, or propose changes (an amendment names what to change and why; it is appended and dated, never overwritten). By design this is **non-blocking** — the agents do not wait on it.

**The director-facing reading path (built for exactly this — you do not need to read the technical contract cold):**
- [`Accessible Claim Sheet.md`](Accessible%20Claim%20Sheet.md) — the plain-language companion: the same commitments, bounds, and success/failure shapes in ordinary language. Start here.
- [`Study Guide/Pass 1 - Conceptual Foundation.tex`](Study%20Guide) (+ compiled PDF) — the conceptual foundation written for you: what the question is, why it's hard, and the ideas you need to follow and judge Phase 2.
- [`Claim Sheet.md`](Claim%20Sheet.md) — the precise technical contract itself (fifteen slots), if you want the exact wording of any commitment.

**Why it's needed:** the amendment protocol makes the director's review the checkpoint that the agreed contract actually matches your intent for the project. The agents own execution from the approved contract, but this review is how you keep the work pointed where you want it — early, when a course correction is cheap. It is deliberately structured so your review can land whenever your schedule allows, without holding up the work.

**What's blocked:** **nothing.** This is non-blocking by design. Phase 2 (execution) is open and proceeding.

**Fallback / what the agents do meanwhile:** the agents proceed with Phase 2 against the agreed contract — Codex runs the bounded physics **feasibility spike** (the gate that decides the simulation path), and Claude builds the **sensor-realism + fault-injection model** and the **evaluation-harness skeleton** against the jointly-approved data schema (`Reproducibility Packet/schema/schema-v1.0.md`). If your review later lands an amendment, it is applied through the protocol — appended and dated, with any work it invalidates moved to a dated `archive/` folder rather than deleted, and corrections propagated forward — so nothing done in the meantime is wasted or silently overwritten.

*Awaiting director reply.*
