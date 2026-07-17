# Claude — Workspace

This is Claude's personal workspace for the **Robot Structural Proprioception** project. It holds my continuity documents, my Phase-0 field survey, my running source ledger, and my per-session and progress reports. Everything here is visible to the human director and to Codex.

## Folder tree

```
agents/Claude/
├── README.md                          ← you are here: guide to this workspace
├── Summary of Only Necessary Context.md  ← rewritten every session; restores my working context
├── Literature Foundation.md           ← Phase-0 six-section field survey (authoritative)
├── references.md                      ← running, verified source ledger (authoritative, grows all project)
├── Session Summaries/                 ← per-session human-readable reports (HumanReport1.md, 2, …)
└── Progress Reports/                  ← director-facing progress reports (every 8th session, phase/amendment events)
```

## What each file is for (purpose, not contents)

- **`Summary of Only Necessary Context.md`** — the first thing I read at the start of a session after the framework docs. It is **completely rewritten each session** and contains only what I need to resume smoothly: current phase, what I was doing, decisions and why, open questions, next steps. Authoritative for continuity, but always current-only — it is not a history.
- **`Literature Foundation.md`** — my independent Phase-0 reading of the field (six sections: domain/methods, benchmarks, datasets/resources, failure modes, open questions, references). **Authoritative** and stable; it grounds the Claim Sheet and feeds Study Guide Pass 1. Codex maintains a separate, independent one — the divergence is intentional.
- **`references.md`** — my running source ledger (verified links/DOIs, summary + how-it-informed per entry), clustered by subfield. **Authoritative** and append-mostly; grows across the whole project and reconciles into the Technical Report bibliography at Phase 2.
- **`Session Summaries/`** — thorough, timestamped, human-readable reports, one per session (`HumanReport1.md`, `HumanReport2.md`, …). The director's audit trail of how the work evolved.
- **`Progress Reports/`** — director-facing progress reports at the Accessible-Piece bar, written on my sessions 8/16/24…, and on any session that closes a phase transition or an approved Claim-Sheet amendment. Contains `Progress Report Phase 0 Close.md` (Session 2, Phase 0 → Phase 1) and `Progress Report Phase 1 Close.md` (Session 5, Phase 1 → Phase 2). Next regular report: my Session 8.

There are no scratch/temporary files tracked here at present; transient working files go to the session scratchpad outside the repo, not into this folder.

## Files I own or co-own outside this workspace

- **Root [`README.md`](../../README.md) (the Live-Run README)** — I created it in Session 1 (State A). It is the public-facing status page; it is **co-maintained** by both agents and updated per `Playbooks/live-run-readme.md` at phase transitions / finished artifacts / noteworthy events. Updated Session 2 (Phase 0 → Phase 1), Session 3 (Claim Sheet converged), Session 4 (companions approved; schema drafted), Session 5 (banner flipped to Phase 2 — Execution; still In Progress), Session 6 (running-log entry for the chat-coordination occurrence), and **Session 7 (running-log entry: plant↔sensor lanes connected and mutually verified + evaluation-harness core built; banner unchanged — still Phase 2 / In Progress)**.
- **[`director_requests.md`](../../director_requests.md) (project root)** — the project's single append-only record of director-only work. I created it in Session 5 at Phase-1 close; first entry is the non-blocking *Claim Sheet ready for director review*. Co-owned (either agent appends; the director replies in place).
- **[`Claim Sheet.md`](../../Claim%20Sheet.md)** — the project contract. I drafted it (Session 2, default writer); Codex reviewed and edited it (its Session 2); I re-reviewed and approved the same state (Session 3). It is now **agreed by both agents** — the authoritative contract. Changes from here run through the amendment protocol.
- **[`Accessible Claim Sheet.md`](../../Accessible%20Claim%20Sheet.md)** — plain-language companion to the contract. I wrote it Session 3 (default writer); Codex reviewed/edited it (its Session 3); I re-reviewed and approved the same state (Session 4). **Agreed by both agents** — review loop closed. Kept in exact sync with the Claim Sheet.
- **[`Study Guide/`](../../Study%20Guide)** — director-facing study guide. `Pass 1 - Conceptual Foundation.tex` (+ compiled PDF) written Session 3; Codex reviewed/edited (its Session 3); I re-reviewed, independently rebuilt the PDF, and approved the same state (Session 4). **Agreed** — review loop closed. Pass 2 is produced at Phase 3.
- **[`Reproducibility Packet/schema/schema-v1.0.md`](../../Reproducibility%20Packet/schema/schema-v1.0.md)** — the shared `plant → signals → estimator → controller` data contract both Phase-2 lanes build against. Co-owned: my v0.1 sketch → Codex's v0.2 plant-side revision → my v1.0 handoff (S4) → Codex's v1.0 edited review state (S4) → my **same-state approval (Session 5)**. **Jointly approved and in force**; changes now run through the amendment protocol. I built the sensor lane against it in Session 6.
- **[`Reproducibility Packet/scripts/`](../../Reproducibility%20Packet/scripts) — sensor lane + evaluation core (mine):**
  - **Sensor lane (Session 6):** the sensor-realism + fault-injection model — `utils/schema_types.py`, `utils/sensor_model.py`, `utils/rng.py`, `utils/synthetic_plant.py`, `scripts/make_synthetic_plant_trace.py`, `scripts/run_sensor_model.py`, `tests/test_sensor_model.py`. Built against schema v1.0. The shared interface structs in `schema_types.py` (`PlantStepState`/`PrivilegedRecord`/`observable_sources`/`FaultSpec`) went through the review cycle with Codex in **Session 7 and are now jointly approved (loop closed)** — Codex edited them (lossless `PlantStepState`, `qd_obs` validity fix, shared `FaultSpec`) and I re-reviewed, verified end-to-end, and approved the same state.
  - **Evaluation harness core (Session 7):** `utils/metrics.py` (two-layer success-bar metrics: macro-F1 w/ abstention-as-error, per-class recall, Brier/NLL/ECE, risk–coverage, false-abstention, OOD AUROC/AUPRC/false-accept; control `J_5s` + tracking-reduction %), `utils/stats.py` (paired hierarchical bootstrap), `tests/test_metrics.py`, `tests/test_stats.py`.
  - Codex owns the plant lane in the same folder (`utils/cable_mechanics.py`, `utils/cable_plant.py`, `scripts/make_mujoco_plant_trace.py`, `scripts/run_feasibility_spike.py`, `tests/test_cable_plant.py`, `tests/test_feasibility_spike.py`). Both lanes share `utils/` and the Reproducibility Packet. **Full packet suite: 51 tests green.**
- **Chats with Codex** (co-owned, append-only): [`Phase 0 Coordination/`](../../chats/Claude-Codex/Phase%200%20Coordination) — **Concluded** Session 2; [`Claim Sheet Review and Division of Labor/`](../../chats/Claude-Codex/Claim%20Sheet%20Review%20and%20Division%20of%20Labor) — **Concluded Session 6** (all Phase-1 loops closed; see its `Summary.md`), concluded at the director's instruction; and [`Phase 2 Integration and Config Freeze/`](../../chats/Claude-Codex/Phase%202%20Integration%20and%20Config%20Freeze) — **Active**, opened Session 6, carries the plant↔sensor integration + `config.json` freeze coordination. In **Session 7** I closed the review-cycle loop on the shared interface here (same-state approval) and posted the remaining config-freeze items; my next post will carry the estimator + `W`/stride proposal.
- **Chat with the director** (co-owned, append-only): [`chats/Claude-Codex-Human/Chat Appends/`](../../chats/Claude-Codex-Human/Chat%20Appends) — **Concluded** (Session 6): the director flagged Codex's chat-misplacement occurrence; both agents acknowledged and are watching for it. **Monitoring duty is standing:** if I ever see a reply land anywhere but the physical end of a transcript, I flag it in `Claude-Codex-Human`.
- Future co-owned deliverables (per the default writer convention): I remain default writer for the Technical Report, Accessible Piece, and Study Guide Pass 2; Codex is the required reviewer. Both agents contribute to the Reproducibility Packet. These do not exist yet (produced in Phase 3).

## How to navigate this folder without prior context

1. Read **`Summary of Only Necessary Context.md`** first — it tells you where I am right now and what's next.
2. Read the latest report in **`Session Summaries/`** for the most recent session's full detail.
3. Read **`Literature Foundation.md`** for my grounding on the problem and **`references.md`** for the evidence behind any claim.
4. For project-wide context (premise, standards, phases), see the root [`Project Details/Project Details.md`](../../Project%20Details/Project%20Details.md) and [`AgentPrompt.md`](../../AgentPrompt.md) — I re-read those every session; they are not duplicated here.
