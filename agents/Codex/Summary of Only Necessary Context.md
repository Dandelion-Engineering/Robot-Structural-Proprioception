# Summary of Only Necessary Context — Codex

Last completely rewritten after Codex Session 134 on 2026-08-14.

## Resume here

- Branch: `main`.
- The director's Review Card and convergence method is now the governing review protocol. It was implemented for Codex in Session 134 and is first applicable to Claude in Session 135. It supersedes the rest of `Playbooks/review-cycle.md`.
- The oversized `Phase 2 Integration and Config Freeze` chat is concluded. Do not append new work there.
- The active three-party governance chat is `chats/Claude-Codex-Human/Review Boundary and Convergence/Review Boundary and Convergence - Active.md`. Read its latest correction for protocol feedback and problems arising from the method.
- Root `Review Card/README.md` defines the required card fields. New formal reviews need a candidate-specific card and a subject-scoped chat.
- Slot-8 Steps 1–3 remain closed / both approved.
- Step-4a is **ACTIVE, NOT YET APPROVED** under `Review Card/Slot-8 Step-4a Connection-Record Design.md` and the narrow active chat `chats/Claude-Codex/Slot-8 Step-4a Connection-Record Design/Slot-8 Step-4a Connection-Record Design - Active.md`.
- The director corrected the transition: start the new method from the current state. Pre-method exchanges do not consume the new three-round limit and do not cause retroactive escalation.
- Claude's Round-1 owner candidate is blob `968fa8959fc3b106895e794589c41954d0c2f901`.
- Codex's completed Round-1 response has one numbered blocker and proposes blob `425ce0118bddc44daccfa69b19362aec6ea70d00`, raw SHA-256 `a270d95d891037f70e5d08fafd15dadfcd1f69c40d95ca978cd9927bdc057400`, 77,105 bytes / 993 LF / 0 CR.
- The reviewer proposal passed `DESIGN_REVIEW_OK: 72 checks`; focused config-contract tests passed 18/18. Claude's owner response begins new-method round-trip 1; Codex's next review is Round 2 / delta-only.
- Step 4b is unauthorized. Steps 4c–4f, every real-role connection/read, capacity or threshold selection, and final-configuration work remain blocked.

## Superseding review protocol

- Before formal review, the owner creates a Review Card naming the candidate state, artifacts and sections in scope, purpose, acceptance tests, blocking-severity definition, exclusions and downstream gates.
- Round 1 is the only full-artifact review and records all reasonably discoverable findings in one numbered ledger.
- Round 2 and later are delta-only: verify recorded findings and response-introduced regressions without re-auditing unchanged material.
- A newly raised pre-existing blocker after Round 1 is a `LATE-BLOCKER`; it must invalidate the scoped purpose and explain why it was missed. A second late blocker, or any new blocker after Round 2, requires human triage or a split. Non-blocking late findings become follow-ups.
- A review has at most three owner-reviewer round-trips. The limit does not force approval; the terminal outcome must be Approved, Approved with Follow-ups, Revisions Required, Split/Redesign Required, or Escalated.
- Once both agents approve the scoped candidate, that review closes. Amendments, implementation, data gates, new sections and new versions get new Review Cards and new subject-scoped chats.
- Reviewers may directly apply mechanical corrections. Substantive scientific, architectural or interpretive changes remain proposed findings or patches for the owner unless ownership is explicitly transferred.
- Transition rule: an in-progress review keeps its current candidate, settled findings and open ledger; earlier exchanges do not consume the new limit. A complete immediately preceding full-artifact review becomes Round 1.
- Interpret `mechanical` by effect, not edit size: a wording change that changes authority, scientific meaning or architecture is substantive.
- An exclusion cannot hide an integration defect that genuinely invalidates the stated scoped purpose.

## Current Step-4 technical state

### Finding DE

Claude's finding-DD repair removed final-config handling from the adapter-path test and left only direct validator checks. That permits an implementation to refuse every final configuration while still passing the proposed suite; the final half no longer positively proves the real Step-4 adapter path.

Codex's B8 repair requires one internal Step-4 helper and an isolated temporary packet root. The public roles path stays bound to the live packet root and exposes no CLI or environment override. The temporary root contains exact copies of the tracked schema and draft plus a synthetic `config.json` for the final leg. Both matching authority pairs must pass Step 4 and then stop only at a deliberate Step-5 corruption; both wrong-authority pairs must refuse. The test also proves that the live packet contains no `config.json` and that all writes stay inside the temporary root.

The current artifact is a reviewer proposal, not same-state joint approval. Claude should respond as owner in the narrow Step-4a chat; Codex then performs a delta-only Round-2 review.

## Chat and transcript state

- Concluded legacy transcript: `chats/Claude-Codex/Phase 2 Integration and Config Freeze/Phase 2 Integration and Config Freeze - Concluded.md`.
- Legacy summary: `chats/Claude-Codex/Phase 2 Integration and Config Freeze/Summary.md`.
- Final legacy transcript state: 2,296,416 bytes, SHA-256 `06508a94430ea91f59037a004cfc74773be3959a97fe131ec894d2a2742bf388`.
- The final Codex close note was appended only after exact-prefix verification; it is 1,158 bytes / 21 LF / 0 CR and is physically last.
- Active protocol chat: `chats/Claude-Codex-Human/Review Boundary and Convergence/Review Boundary and Convergence - Active.md`.
- Active Step-4a review chat: `chats/Claude-Codex/Slot-8 Step-4a Connection-Record Design/Slot-8 Step-4a Connection-Record Design - Active.md`.
- Active transcript-order recurrence log: `chats/Claude-Codex-Human/Transcript Order Monitoring/Transcript Order Monitoring - Active.md`.
- Future chats should be created by bounded subject and concluded when that subject is done. A whole phase is too broad for one active thread.

## Durable scientific boundaries

- The project remains development-only; no final model is frozen and no confirmatory run has occurred.
- Slot-9 Stage 1 and rung-2 are complete only at their bounded development-screen scopes. No capacity or threshold was selected.
- All ten rung-2 arms have zero healthy and structure F1. This persisted-value fact may accompany the weak objective/sign description without a causal claim.
- Slot-8 role use remains synthetic-only. No real role path may connect to or read data without the separate downstream gates.
- Scientific read/run counters are unchanged in Session 134: no artifact reads and no scientific runs.

## Public heartbeat and reports

- Root `README.md` was not changed in Session 134: no scientific artifact finished, phase closed, or public milestone changed.
- No progress report was required in Session 134; it is not an every-eighth Codex session and no scientific phase or amendment closed.
- The governance and review-status changes are recorded in the agent README, HumanReport134, the playbook, the Review Card README and the scoped chats.

## Next-session rules

1. Read `.agent-turn`, honor the session lock gate, then follow `AgentPrompt.md`.
2. Read this continuity file, `agents/Codex/README.md`, `agents/Codex/Session Summaries/HumanReport134.md`, and every active shared chat involving Codex.
3. Read the active Review Boundary and Convergence chat before responding to any Step-4 work.
4. Do not reopen or append to the concluded Phase-2 transcript.
5. Continue Step-4a only in its narrow Review Card and subject chat. The next Codex review is Round 2 / delta-only after Claude's owner response.
6. Do not treat the reviewer candidate as Claude approval or as authorization for Step 4b.
7. If a new Review Card is opened, enforce the one-ledger, delta-only, late-blocker and three-round-trip rules exactly.
8. Preserve append-only transcript writes with physical-tail, line-count, exact-prefix, unique-header and post-write assertions.
9. Keep public claims bounded to direct evidence and preserve all downstream data, capacity, threshold and final-configuration gates.

## Session 134 closeout state

- Codex implemented the superseding review method, established the Review Card directory, opened the active three-party protocol chat and recorded feedback plus the migration correction.
- Codex concluded and summarized the oversized Phase-2 chat.
- Codex reviewed Claude's Step-4 design response, added finding DE/B8, and preserved exact evidence without claiming same-state convergence.
- After the director corrected the initial retroactive escalation, Codex opened the Step-4a transition card and narrow chat at the current state. Round 1 is complete; Claude's owner response is pending.
- Handoff target after commit and push: Claude Session 135.
