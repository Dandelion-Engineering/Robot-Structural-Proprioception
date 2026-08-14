# Review Card — Slot-8 Step-4a Connection-Record Design

**Status:** Approved — Round 2 closed / both agents approved the same design bytes
**Transition basis:** Director ruling, 2026-08-14
**Owner:** Claude
**Reviewer:** Codex
**Subject chat:** `chats/Claude-Codex/Slot-8 Step-4a Connection-Record Design/Slot-8 Step-4a Connection-Record Design - Concluded.md`

## Candidate state and round baseline

This card preserves the review exactly where it stood when the superseding method arrived. Earlier
Phase-2 exchanges are historical and do not consume the new three-round limit.

- Round 1 owner candidate: `Reproducibility Packet/protocol/slot8-connection-record-v0.1.md`, Git
  blob `968fa895fb81a04bfc04f4b743d8d03f3a1af612`, raw SHA-256
  `3fe6255c26a02c8d42e822b881b4d49ab4c5cde84acc2f1d7faf2d9a4e6cfbd4`, 73,640 bytes / 951 LF / 0 CR.
  **Mechanical correction, Claude Session 135:** this line first named blob
  `968fa8959fc3b106895e794589c41954d0c2f901`, which is not an object in this repository —
  `git cat-file -t` refuses it. The correct id is above and is the state Codex's own Round-1 chat
  message and Session-134 report body both authenticate by raw digest. Nothing else about the
  baseline changes.
- Round 1 reviewer response: finding 1 / formerly DE, with proposed integrated artifact Git blob
  `425ce0118bddc44daccfa69b19362aec6ea70d00`, raw SHA-256
  `a270d95d891037f70e5d08fafd15dadfcd1f69c40d95ca978cd9927bdc057400`, 77,105 bytes / 993 LF /
  0 CR. Both digests reproduced independently in Claude Session 135.
- Round-trip 1, owner half (Claude Session 135): finding 1 accepted in substance and integrated.
  Owner candidate Git blob `032db1666efbe00adec5696de70424d531ba33a2`, raw SHA-256
  `f761a673ff8fcca6c58fe530a3faaed57630315a87a5e241d8ca9675a13c4ffc`, 83,181 bytes / 1,062 LF /
  0 CR, LF-pinned (measured with `git check-attr`). Owner audit `DESIGN_REVIEW_OK: 133 checks,
  0 failed`; focused config-contract suite 18/18.
- Round 2 reviewer close (Codex Session 135): delta-only review resolved finding 1 without editing
  the design. Codex explicitly approved the same blob `032db1666efbe00adec5696de70424d531ba33a2`.
  Codex's updated design audit passed 72/72 checks, the focused config-contract suite passed 18/18,
  and `git diff --check` was clean.
- New-method outcome: **Approved**. Step 4a is closed / both approved at the exact owner-candidate
  bytes above. Only the separately reviewed Step-4b adapter-and-test build is now licensed.
- Settled findings from the pre-method review remain settled and are not reopened.

## Purpose

Determine whether the Step-4a connection-record design is sufficiently complete, deterministic,
authority-bounded and testable to freeze as the design prerequisite for a later, separately gated
Step-4b adapter/test implementation.

Approval of this card closes only the Step-4a design review and licenses the bounded Step-4b
adapter-and-test build under its own new Review Card; it does not approve a Step-4b implementation
state or authorize any real-role connection/read, Step 4c–4f, capacity or threshold selection, or
final-configuration work.

## Artifacts and sections in scope

- `Reproducibility Packet/protocol/slot8-connection-record-v0.1.md` in full for Round 1.
- In Round 2 and later, only the owner's response to finding 1, the recorded acceptance tests and
  regressions introduced by that response.
- The B8 config-authority and adapter-path test contract, plus any directly necessary definitions
  or cross-references changed to integrate it.

## Round 1 numbered finding ledger

1. **BLOCKING — the final-config branch is not positively exercised through the real Step-4
   adapter path.** The validator-only final half can pass even if an implementation refuses every
   final configuration. The design must require a positive final-config case through the same
   internal Step-4 helper used by the public roles path, under an isolated temporary packet root,
   while proving that the public path remains bound to the live packet and exposes no override.

   **Disposition: resolved / closed.** Claude accepted the finding in substance in Session 135 and
   integrated. Both authority branches now cross one internal roles-mode entry point entered after
   record authentication; the explicit packet root that entry point accepts governs every
   packet-relative resolution in the read order (step-3 domain binding, step-4 schema/config
   resolution, step-5 sources, section-4.7 output parent), because B8's own stop condition is a
   deliberate step-5 refusal and a step-4-only helper cannot reach it. W8 additionally requires a
   *positive* assertion that the public path's bound root is the live packet root. Section 1.3 is
   scoped to the live packet tree so the document does not both forbid and require a file named
   `config.json`. See section 9.6, "Owner integration, Session 135".

No other Round 1 findings are open. Any newly raised pre-existing blocker is governed by the
LATE-BLOCKER rule.

## Acceptance tests

1. One internal roles-mode entry point entered after record authentication carries the packet root
   through the Step-3 domain binding, Step-4 config resolution/validation/authority check, Step-5
   source resolution and the output-parent check used by the public roles path.
2. The public roles path binds that entry point to the module-derived live packet root and exposes
   no CLI or environment override.
3. An isolated temporary packet root contains exact copies of the tracked schema and draft plus a
   synthetic `config.json` for the final leg.
4. Both matching authority pairs pass Step 4 and stop only at a deliberate Step-5 corruption.
5. Both wrong-authority pairs refuse.
6. The test proves the live packet contains no `config.json` and all test writes remain inside the
   temporary root.
7. Each agent's candidate-state audit passes with zero failures, and the existing focused
   config-contract suite remains 18/18 passing. Instrument-specific check counts are evidence, not
   properties of the candidate.
8. Both agents explicitly approve the same exact design bytes.

## Blocking-severity definition

A finding is blocking only if it can invalidate the scoped purpose by permitting an unauthorized
authority/config pairing, failing to exercise a required adapter branch, allowing production-path
root substitution, making the contract non-deterministic or untestable, or licensing downstream
work without exact-state approval.

## Explicit exclusions and downstream gates

- Step-4b implementation source and tests.
- Any real-role connection, data read or write.
- Steps 4c–4f.
- Capacity or threshold selection.
- Final-configuration creation, freeze or use.
- Re-audit of unchanged, settled pre-method material unless a response introduces a regression.

## Round limit and terminal outcomes

At most three owner-reviewer round-trips begin from this card's baseline. The limit never forces
approval. The card must end as Approved, Approved with Follow-ups, Revisions Required,
Split/Redesign Required, or Escalated.

**Terminal outcome:** Approved in Round 2 on 2026-08-14. Both agents explicitly approved design
blob `032db1666efbe00adec5696de70424d531ba33a2`; no follow-up blocks Step 4b. The stale
`build_role_bundle` docstring gloss is tracked for correction within the additive 4b build and does
not reopen the closed Step-2 state.
