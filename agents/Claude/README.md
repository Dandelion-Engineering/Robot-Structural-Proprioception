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
- **`Progress Reports/`** — director-facing progress reports at the Accessible-Piece bar, written on my sessions 8/16/24…, and on any session that closes a phase transition or an approved Claim-Sheet amendment. Contains `Progress Report Phase 0 Close.md` (written Session 2 when the Phase 0 → Phase 1 transition closed).

There are no scratch/temporary files tracked here at present; transient working files go to the session scratchpad outside the repo, not into this folder.

## Files I own or co-own outside this workspace

- **Root [`README.md`](../../README.md) (the Live-Run README)** — I created it in Session 1 (State A). It is the public-facing status page; it is **co-maintained** by both agents and updated per `Playbooks/live-run-readme.md` at phase transitions / finished artifacts / noteworthy events. Updated Session 2 for the Phase 0 → Phase 1 transition.
- **[`Claim Sheet.md`](../../Claim%20Sheet.md)** — the project contract. I drafted it in Session 2 (I'm the default writer); it is **in cross-review** with Codex. Authoritative once both agents approve the same state.
- **Chats with Codex** (co-owned, append-only): [`chats/Claude-Codex/Phase 0 Coordination/`](../../chats/Claude-Codex/Phase%200%20Coordination) — **Concluded** Session 2 (see its `Summary.md`); and [`chats/Claude-Codex/Claim Sheet Review and Division of Labor/`](../../chats/Claude-Codex/Claim%20Sheet%20Review%20and%20Division%20of%20Labor) — **Active**, opened Session 2 for the Claim Sheet review cycle and the labor split.
- Future co-owned deliverables (per the default writer convention): I am the default writer for the Accessible Claim Sheet, Technical Report, Accessible Piece, and both Study Guide passes; Codex is the required reviewer. Both agents contribute to the Reproducibility Packet. These do not exist yet (produced later in Phase 1 / Phase 3).

## How to navigate this folder without prior context

1. Read **`Summary of Only Necessary Context.md`** first — it tells you where I am right now and what's next.
2. Read the latest report in **`Session Summaries/`** for the most recent session's full detail.
3. Read **`Literature Foundation.md`** for my grounding on the problem and **`references.md`** for the evidence behind any claim.
4. For project-wide context (premise, standards, phases), see the root [`Project Details/Project Details.md`](../../Project%20Details/Project%20Details.md) and [`AgentPrompt.md`](../../AgentPrompt.md) — I re-read those every session; they are not duplicated here.
