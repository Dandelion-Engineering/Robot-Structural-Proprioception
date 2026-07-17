# Robot Structural Proprioception

> **The question.** Can a simulated robot use distributed, physically grounded measurements of its own structural state — strain, curvature, shear, torsion, vibration, temperature — to recognize and compensate for changes in its body or sensors, and does that information provide an adaptive-control advantage beyond a more conventional robot sensor suite?

| | |
|---|---|
| **Phase** | Phase 2 — Execution |
| **Public state** | 🟡 `In Progress` |
| **Last updated** | 2026-07-17 |

This is a **public live research run** by [Dandelion Engineering](https://github.com/Dandelion-Engineering). You are watching the work happen. This page is the honest status of the project and — once it concludes — a way for you to check the result yourself. It is not a marketing pitch. While the run is live, expect pivots, dead ends, and negative findings to be recorded here in real time; that transparency is the point.

---

## What we are asking, in plainer terms

Most robots run on a fixed factory model of their own body. But real bodies change — parts wear, loosen, heat up, go slightly compliant, develop friction or backlash, lose actuator strength, or get partially damaged; sensors drift and go noisy. A robot that keeps trusting its original model can become inaccurate or unsafe even when it is still physically capable of the task.

Humans handle this with a dense, distributed sense of their own bodies — signals from skin, muscles, tendons, joints, and balance organs — continuously updating an internal body model. This project asks whether giving a robot an analogous stream of **internal structural sensing** (the kind of strain/vibration/deformation signals aerospace structures are already instrumented for) lets it (1) notice that its body or its sensors have changed, (2) tell *what* changed — structure, actuator, or the sensor watching them — and (3) keep as much useful capability as possible instead of treating every deviation as a terminal failure.

The whole project runs **in simulation**. We are not building a sensor. We are testing whether the *information* such sensors could provide is valuable enough to justify deeper research. A clean negative result — "these structural signals add little beyond a conventional sensor suite" — would be a real and publishable outcome.

---

## Running log

*Append-only. Lean by design — entries mark finished artifacts, phase closes, and genuinely noteworthy moments, not every session.*

- **2026-07-16 — Project went public; Phase 0 (Literature Review) opened.** Repository initialized, framework and playbooks in place, `venv` (Python 3.12) provisioned. The two AI agents (Claude, Codex) begin independent field surveys spanning robot self-modeling and body-schema learning, adaptive and fault-tolerant control, online system identification, structural health monitoring, distributed strain sensing, soft-robot and tactile proprioception, sensor-fault diagnosis, and embodied/morphological intelligence.
- **2026-07-16 — Both independent literature surveys completed; comparison opened.** Claude and Codex finished separate Phase 0 foundations and are reconciling the smallest defensible question, matched baselines, and simulation path before the Claim Sheet is drafted. Phase 0 remains open until that comparison converges.
- **2026-07-16 — Phase 0 closed; Phase 1 (Sharpening) opened.** The two surveys converged on the smallest defensible question — whether a few local strain/curvature channels help a small compliant manipulator tell a *structural* change from an *actuator* change from a *sensor* change, and whether that improves recovery — and on a matched-comparison design that varies only the sensor suite so any advantage is attributable to information, not algorithm. The project **Claim Sheet** (the contract) has been drafted and is in cross-review.
- **2026-07-16 — Claim Sheet converged.** Both agents approved the same contract state, so the project's commitments — the matched C0/C1/S/O sensor-suite comparison, the pre-declared success/failure/inconclusive shapes, and the exact effect-size bars — are now fixed. The plain-language [Accessible Claim Sheet](Accessible%20Claim%20Sheet.md) and the director's [Study Guide (Pass 1)](Study%20Guide) are drafted and in review. Phase 1 stays open until those companions are approved and the shared plant→signals→estimator data schema is versioned.
- **2026-07-16 — Companion artifacts approved; shared data schema drafted (v1.0).** Both agents closed the review loops on the [Accessible Claim Sheet](Accessible%20Claim%20Sheet.md) and the [Study Guide (Pass 1)](Study%20Guide) — same-state approval on both. The shared plant→signals→estimator→controller data schema — the interface both execution lanes build against — is now written as a proposed v1.0 and in final review. Phase 1 closes once that schema is jointly versioned; Phase 2 (execution) then opens with the physics feasibility spike.
- **2026-07-17 — Phase 1 closed; Phase 2 (Execution) opened.** The shared plant→signals→estimator→controller data schema — the last Phase-1 gate — reached same-state approval by both agents, so the full contract-and-interface layer is now fixed and in force. The agreed Claim Sheet has been logged for the director's (non-blocking) review. Phase 2 begins with a bounded physics **feasibility spike** — can a few simulated strain gauges actually tell a stiffness change from an actuator change from a sensor fault, above a realistic noise floor? — which gates the full benchmark, alongside the sensor-realism/fault-injection model and the evaluation harness.

---

## Follow along / what will be here

This project will produce four artifacts. All are **pending** while the run is live:

- **Technical Report** *(pending)* — the rigorous, field-facing account.
- **Accessible Piece** *(pending)* — the same work written for a general reader, with no technical background assumed.
- **Reproducibility Packet** *(pending)* — code, configs, data references, a runbook, and the hands-on **verification artifact** so anyone can re-run and check the result on their own machine.
- **Study Guide** *(pending, director-facing)* — a two-pass guide that keeps the project's director able to follow and judge the work.

The project's full premise, strategy, and standards live in [`Project Details/Project Details.md`](Project%20Details/Project%20Details.md). How each artifact is built lives in [`Playbooks/`](Playbooks). The project's contract — the **Claim Sheet** — is now agreed by both agents: [`Claim Sheet.md`](Claim%20Sheet.md), along with its plain-language companion, the [`Accessible Claim Sheet.md`](Accessible%20Claim%20Sheet.md), and the director-facing [Study Guide (Pass 1)](Study%20Guide).

---

## Public, licensing, and how this is made

**Public run.** This repository is public and updated as the work proceeds. The agents' session-by-session reports live under [`agents/`](agents); coordination between agents lives under [`chats/`](chats).

**Licensing.** Code is released under **MIT** ([`LICENSE`](LICENSE)); prose and narrative artifacts under **CC BY 4.0** ([`LICENSE-docs`](LICENSE-docs)). The scope map and citation guidance are in [`LICENSING.md`](LICENSING.md). Third-party datasets, if any are used, are not redistributed here — each will be documented with its own source and license in the Reproducibility Packet's `DATA.md`.

**How it's made.** Dandelion Engineering does real research and turns what it learns into affordable technology aimed at problems that matter for everyday people. It is one human director and a small team of AI agents working in short sessions that compound over time. The strategy is patience, not speed, and a clean negative result is treated as just as publishable as a positive one. A fuller account of the method resolves onto this page when the project concludes.
