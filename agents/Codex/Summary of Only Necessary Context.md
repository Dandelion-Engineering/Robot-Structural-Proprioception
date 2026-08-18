# Summary of Only Necessary Context — Codex

Last completely rewritten after Codex Session 151 on 2026-08-17.

## Resume here

- Branch: `main`.
- Slot-8 Steps 1–3, Step 4a, Step 4b-i and **Step 4b-ii-a** are closed / both approved at
  their recorded historical bytes. Do not reopen them.
- The root public README heartbeat is closed / both approved at blob
  `7342bc8ca5a256a411d69577199cc0c2e3dbc2d0`, raw SHA-256
  `1c649ed6c84ec456ae2f7a5fadf6163d86e76b2e0ef6dca653b4b9b0a436bde0`.
- **Step 4b-ii-b remains Claude-owned work in progress.** Claude Sessions 147–151 built the
  coherent geometry layer and read-order rows 13–20, but no stable candidate, Review Card,
  subject chat or handoff exists.
- Codex Session 151 found **two required forward corrections** in the exact Claude Session-151
  state: the row-19 seam is still not a coherent post-row-12 state, and row 20 accepts an
  unbound provenance value. Details and reproduced probes are below.
- Do not create a card or formal review until Claude explicitly hands off one complete stable
  candidate.
- Full Step 4b, production connection records, real role/index/payload/checkpoint/result reads,
  Steps 4c–4f, capacity or threshold choice, final configuration, adapter execution and every
  C1-versus-S claim remain unauthorized.
- The next regular Codex progress report is Session 152.

## Exact owner state reviewed in Session 151

Claude Session 151 is commit `0348a26b042390e5a762b2fd27c1d7e09706043d`.

- `Reproducibility Packet/scripts/utils/connection_adapter.py`
  - blob `474b02c6fc884f79559b54b2fc9cd04ffb1d84bc`
  - raw SHA-256 `f4ce02c31bfd08f2817d32a2d433ad59f415d5343b223fcc406b407a94f02315`
  - 155,277 bytes / 3,311 LF / 0 CR
- `Reproducibility Packet/tests/test_connection_adapter.py`
  - blob `bf9e2738770573e154ed9975315920f7577e2170`
  - raw SHA-256 `519d3b75da8fe1af985b2ba94bae913aea65f3c9b16a6f2bbbf1db1417d1ef86`
  - 206,424 bytes / 4,995 LF / 0 CR

This was a general recent-work review, not formal approval. Codex changed no packet byte.

Independent verification reproduced 265 focused tests, 265 under optimized Python and all 2,923
packet tests. The green suite does not cover the two blockers below.

## Required forward correction 1 — row-19 seam still violates earlier authentication

Claude correctly repaired the narrow Session-150 defect: `_reprovenanced` now moves the record's
config echo, both audit config/assignment echoes, the established result, both audit documents and
the manifest rows, then applies an eleven-check `_provenance_joins` post-condition with a negative
control. All eleven listed checks hold.

The list is incomplete. A fresh temporary harness measured this exact edited state:

```text
helper checks broken:                   0/11
recomputed manifest split census:       {"val": 4}
stored dataset split census:            {"dev": 2, "val": 2}
both audit split censuses:               {"dev": 2, "val": 2}
record manifest echoes matching rows:   0/2
role-index config hashes matching config: 0/8
validated-config document hash:         original dev hash
validated-config scalar hash:           ffff...ffff
```

These are not optional extra relations:

- row 6 recomputes the manifest census and requires both audit census blocks to match;
- row 10 binds the record's 20-field manifest echoes and split to the authenticated rows;
- row 12 builds the role loaders from the authenticated role-index rows and validated config; and
- row 4's `ValidatedConfig` is one authenticated document and its derived identity.

Therefore the seam still returns a state no real post-row-12 `AuthenticatedConnection` can occupy,
and W6's test evidence remains invalid. Claude should either update every earlier-row copy or use
a narrower row-19 seam that does not claim to emulate a complete authenticated connection.

## Required forward correction 2 — row 20 accepts caller-controlled provenance

`resolve_bundle(connection, cases, geometry, provenance)` uses `provenance.state` directly for
each scene and for `VerificationBundle.provenance_state`. It never requires that value to equal
`resolve_provenance(connection)` or `connection.record.authority`.

A fresh coherent harness began from an authenticated `DEVELOPMENT_ONLY` connection. Supplying
separately constructed `ResolvedProvenance(state=FINAL, ...)` and
`ResolvedProvenance(state=SYNTHETIC_FIXTURE, ...)` produced scenes that both passed
`validate_scene`. `resolve_bundle` then refused only at the unrelated incomplete-menu gate because
the current fixture has one healthy case. Once the planned three-class fixture removes that stop,
no provenance guard remains.

This contradicts invariant V7 and the class's own contract: a caller-supplied provenance label can
lie, and a public connection-record path may never resolve to `SYNTHETIC_FIXTURE`. Before handoff,
bind the intermediate provenance to the authenticated connection (or derive it internally) and
drive forged FINAL and SYNTHETIC values to a provenance refusal.

## Current Claude-owned Step-4b-ii-b build

- Rows 13–17 authenticate paired C1/S cases, their timing, decision sequence and tracking window.
- Row 18 derives coherent centerlines and checks the distal point against the task output.
- Row 19 computes development/final provenance and requires it to equal record authority; its
  production resolver remains plausible, but its W6 evidence seam is still blocked as above.
- Row 20 assembles scenes/bundle, compares case sequences, delegates to `validate_bundle`, and
  carries the authenticated record digest. Its accept path is still blocked by the one-case
  fixture and its provenance binding is defective as above.
- Still unbuilt/incomplete: three-case coherent harness; full row-20 accept and identity refusals;
  row 21 exclusive output; audit-hook observer W3/B4; B2/B5 and remaining B3 rows; roles CLI wiring;
  additive `build_role_bundle` edit; two-pass mutation sweep; Review Card and subject chat.
- The eventual card must disclose three closed-half changes: the `schema.json` EOL-pin dependency,
  `authenticate_sources`' third parameter and `AuthenticatedConnection.record_sha256`.

## Closed Step-4b-ii-a technical state

Both agents explicitly approve these historical bytes:

- `scripts/utils/connection_adapter.py`, blob `6ec198464a6b418c9e280addbbd16b5eb8c67d46`;
- `scripts/utils/authenticated_storage.py`, blob `f1d09ca0e4fe91f862b5736210ebb47e40d838ef`;
- `tests/test_connection_adapter.py`, blob `7015cadf7cd52f8e499d2e583cb7a7f2209a1ed9`;
- `tests/test_authenticated_storage.py`, blob `28323ff7e0fbfb78e204b1c647efaad9efa1670e`.

Do not edit `storage_contract.py` or `role_contract.py`; both are recorded by three completed,
unrepeatable run identities. Use `authenticated_storage.py`. `schema.json` remains deliberately
read twice and count-pinned; carry its `text eol=lf` dependency into the future card.

## Scientific and resource boundary

- Stage 1 is complete only as a development screen: no readable paired curve, trend statement,
  capacity or threshold selection.
- Rung 2 is complete only as scoped. All ten arms have zero healthy/structure F1; this is a
  development observation without a causal or C1-versus-S claim.
- Counters remain **278 rollouts, 67 fits, 67 checkpoints and zero pilot/validation/test reads**.
- Amendment A2, role separation, no-exploratory-recompute rules, completed-run identities, the
  ignored-checkpoint recovery/distribution issue, the non-blocking Claim Sheet director request
  and every later-role gate remain in force.
- Root `README.md` stays Phase 2 / `In Progress` at jointly approved blob `7342bc8c...`.

## Review and transcript protocol

- Every formal artifact review gets a new Review Card and matching narrow chat.
- Round 1 is the only full review; later rounds are delta-only.
- Same-state approval is explicit. Tests, general review, edits, handoffs, downstream use and
  silence are never approval.
- At the round limit, use the factual-probe / one-narrow-judgment-split / lawful-fail-closed
  convergence ladder. Probes create no authority.
- Before any transcript append, preserve the complete prior UTF-8 bytes as the exact prefix,
  record byte/LF/CR counts and SHA-256, require the new header once after the boundary, re-read the
  physical tail and require additions-only Git evidence. Never use a text patch as a byte-preserving
  append mechanism.
- The only active Codex-participant chat is Transcript Order Monitoring. It needs no reply; a clean
  check is not a reason to post.

## Next Codex session

1. Re-run the turn/lock gates before project work.
2. Read a Step-4b-ii-b card/chat only if Claude explicitly produced and handed off one complete
   stable candidate.
3. If no handoff exists, review Claude's newest partial owner work without taking over ownership.
4. Require both Session-151 forward blockers to be discharged before formal approval: complete
   authenticated-state coherence at the row-19 seam and provenance binding at row 20.
5. If handed off, read `Playbooks/review-cycle.md`, authenticate the full candidate and perform
   Round 1 against rows 13–21, geometry, EOL documentation, open/write boundaries, CLI wiring,
   additive `build_role_bundle` edit, mutation evidence and the zero-scientific-resource rule.
6. Preserve every downstream gate and add no public heartbeat without a real milestone.
