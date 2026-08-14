# Review Card — Slot-8 Step-4a Connection-Record Design

**Status:** Active — owner response to Round 1 pending
**Transition basis:** Director ruling, 2026-08-14
**Owner:** Claude
**Reviewer:** Codex
**Subject chat:** `chats/Claude-Codex/Slot-8 Step-4a Connection-Record Design/Slot-8 Step-4a Connection-Record Design - Active.md`

## Candidate state and round baseline

This card preserves the review exactly where it stood when the superseding method arrived. Earlier
Phase-2 exchanges are historical and do not consume the new three-round limit.

- Round 1 owner candidate: `Reproducibility Packet/protocol/slot8-connection-record-v0.1.md`, Git
  blob `968fa8959fc3b106895e794589c41954d0c2f901`.
- Round 1 reviewer response: finding 1 / formerly DE, with proposed integrated artifact Git blob
  `425ce0118bddc44daccfa69b19362aec6ea70d00`, raw SHA-256
  `a270d95d891037f70e5d08fafd15dadfcd1f69c40d95ca978cd9927bdc057400`, 77,105 bytes / 993 LF /
  0 CR.
- New-method position: Round 1 full-artifact review is complete. Claude's next response is the
  owner half of round-trip 1. Codex's next review is Round 2 and is delta-only.
- Settled findings from the pre-method review remain settled and are not reopened.

## Purpose

Determine whether the Step-4a connection-record design is sufficiently complete, deterministic,
authority-bounded and testable to freeze as the design prerequisite for a later, separately gated
Step-4b adapter/test implementation.

Approval of this card closes only the Step-4a design review. It does not authorize Step 4b, any
real-role connection or read, Step 4c–4f, capacity or threshold selection, or final-configuration
work.

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

No other Round 1 findings are open. Any newly raised pre-existing blocker is governed by the
LATE-BLOCKER rule.

## Acceptance tests

1. One internal Step-4 helper implements the config-resolution, validation and authority check used
   by the public roles path.
2. The public roles path binds that helper to the live packet root and exposes no CLI or environment
   override.
3. An isolated temporary packet root contains exact copies of the tracked schema and draft plus a
   synthetic `config.json` for the final leg.
4. Both matching authority pairs pass Step 4 and stop only at a deliberate Step-5 corruption.
5. Both wrong-authority pairs refuse.
6. The test proves the live packet contains no `config.json` and all test writes remain inside the
   temporary root.
7. The design audit passes all 72 checks and the existing focused config-contract suite remains
   18/18 passing.
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
