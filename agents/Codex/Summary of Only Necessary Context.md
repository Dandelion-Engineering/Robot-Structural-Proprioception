# Summary of Only Necessary Context — Codex

Last completely rewritten after Codex Session 135 on 2026-08-14.

## Resume here

- Branch: `main`.
- The director's Review Card and convergence method governs formal review and supersedes the remainder of `Playbooks/review-cycle.md` where the two conflict.
- Slot-8 Steps 1–3 remain closed / both approved.
- Slot-8 Step 4a is now **CLOSED / BOTH APPROVED**. Both agents approve exact design Git blob `032db1666efbe00adec5696de70424d531ba33a2`, raw SHA-256 `f761a673ff8fcca6c58fe530a3faaed57630315a87a5e241d8ca9675a13c4ffc`, 83,181 bytes / 1,062 LF / 0 CR.
- The closed card is `Review Card/Slot-8 Step-4a Connection-Record Design.md`. The concluded subject chat and its summary are under `chats/Claude-Codex/Slot-8 Step-4a Connection-Record Design/`. Do not append new work to the concluded transcript.
- Only a **new, separately reviewed Step-4b adapter-and-test build** is licensed. Claude owns the next build unless labor is explicitly reassigned. It should begin with a new Step-4b Review Card and subject-scoped chat.
- No production connection record, real role/index/payload/checkpoint/result read, Step 4c–4f work, capacity or threshold choice, final configuration, adapter run, or C1-versus-S claim is authorized.
- The next regular Codex progress report is Session 136.

## Exact Step-4a outcome

- Claude's corrected prior baseline blob is `968fa895fb81a04bfc04f4b743d8d03f3a1af612`; the shorter identifier transcribed in the earlier card did not name a Git object and is corrected in the closed record.
- Codex's Round-1 reviewer proposal was blob `425ce0118bddc44daccfa69b19362aec6ea70d00`.
- Claude's Round-2 candidate `032db166...` changed only the disputed real-adapter branch and directly related acceptance/audit text; the remaining bytes were mechanically compared to the reviewer proposal.
- The accepted seam is one internal roles-mode entry point after record authentication, governed by one explicit packet root for Step-3 domain binding, Step-4 config authentication, Step-5 source lookup, and output-parent derivation.
- B8 must exercise four config branches under an isolated temporary packet root: development/draft pass, final/draft refusal, final/frozen pass, and development/frozen refusal. Both positive legs must reach the deliberate Step-5 corrupted-source refusal.
- W8 must positively prove that the unchanged public path derives and binds the live packet root.
- The broader seam is necessary: a Step-4-only helper would return before Step 5 and could not establish that accepted config state reaches the deliberate later refusal without consulting the live packet.
- Codex's final audit passed `DESIGN_REVIEW_OK: 72 checks`; focused config-contract tests passed 18/18. No executable changed, so the 2,267-test packet suite was not rerun in Session 135.
- The stale `build_role_bundle` docstring gloss is a non-blocking additive Step-4b follow-up, not a defect in the approved design.

## Step-4b implementation boundary

- Create a new Review Card and narrow subject chat; do not reopen Step 4a.
- Implement only the approved adapter seam and its synthetic tests. Keep one explicit packet root authoritative across the roles-mode path.
- All test writes must remain below the isolated temporary packet root. The live `Reproducibility Packet` must never gain `config.json`.
- The public path remains behaviorally unchanged and must be covered by the positive live-root binding test.
- Preserve refusal-before-scientific-read behavior. Passing Step 4 does not authorize a role payload, checkpoint, output or result read.
- Exact-state review of the new adapter/test candidate is required before any downstream use. Step 4b completion will not itself authorize 4c–4f or any real-data action.

## Review protocol refinements adopted in Session 135

- Every candidate named in a Review Card must carry full Git blob ID, raw SHA-256, byte count and EOL state. The card writer verifies each Git identifier with `git cat-file -t` before posting it.
- Acceptance criteria name durable artifact properties. Script names, private audit predicate counts and similar instrumentation belong in the evidence log, not in the acceptance contract.
- A delta response explicitly identifies both changed and byte-identical regions and records mechanical evidence for the comparison.
- These rules are now in both `Review Card/README.md` and the superseding section of `Playbooks/review-cycle.md`.
- The active director-visible feedback chat is `chats/Claude-Codex-Human/Review Boundary and Convergence/Review Boundary and Convergence - Active.md`. Both agents accepted the refinements; no human triage is open.

## Existing durable boundaries

- Stage 1 is complete only as a development screen: no readable paired shape at five points/five seeds, no licensed trend statement, no capacity or threshold selected.
- Rung 2 is complete only as scoped. Its fit and analyzer invocations are spent. All ten arms have zero healthy and structure F1; this observed fact accompanies the weak objective/sign description without a causal claim.
- Packet-runbook and interpreted public-heartbeat loops remain closed / both approved at their recorded exact states.
- The verified synthetic Slot-8 artifact reproduces byte-for-byte, its figures are 300 DPI, and its role path refuses before opening a scientific file.
- Project counters remain 278 rollouts, 67 fits, 67 checkpoints, and zero pilot/validation/test reads.
- Amendment A2, role separation, no-exploratory-recompute rules, and all unspent authorization gates remain in force.

## Session 135 evidence and public state

- The focused command `venv\Scripts\python.exe -m pytest "Reproducibility Packet\tests\test_data_contract.py" -q` passed 18 tests.
- The full design instrument passed 72 checks against the exact approved bytes.
- No role index, role payload, checkpoint, estimator output, controller log or result was opened. No MuJoCo model was built; no rollout, fit, generation or render ran; and no config, connection record or production output was written.
- Root `README.md` now has a lean 2026-08-14 heartbeat: the connection design is approved by both agents, while only the synthetic Step-4b build is open. This Codex-authored heartbeat is available for Claude's general recent-work review; it does not itself open a formal review cycle.
- `agents/Codex/Session Summaries/HumanReport135.md` is the detailed record of the review, evidence, method update, public edit and preserved boundary.

## Chat and continuity routing

- Do not append to concluded `chats/Claude-Codex/Phase 2 Integration and Config Freeze/`.
- Do not append to concluded `chats/Claude-Codex/Slot-8 Step-4a Connection-Record Design/`.
- Use the active Review Boundary and Convergence chat only for method feedback or problems caused by the method.
- Use `chats/Claude-Codex-Human/Transcript Order Monitoring/Transcript Order Monitoring - Active.md` only if the same writer's message again appears after the verified opposite-agent EOF tail. No recurrence occurred in Session 135.
- Formal Step-4b work needs a new subject-scoped chat and Review Card. General recent-work review does not require a formal cycle unless a blocker or substantive disagreement is flagged.

## Append-only transcript discipline

Before any transcript append:

1. read the UTF-8 physical tail and record byte and line counts;
2. patch only against a programmatically verified unique multiline EOF anchor;
3. verify the entire pre-write byte sequence is the new file prefix;
4. verify the new session header occurs exactly once after the old byte boundary; and
5. reread the physical tail and confirm the new message is last.

If any assertion fails, stop and repair with a dated append-only correction before commit.
