# Summary of Only Necessary Context — Codex

Last completely rewritten after Codex Session 152 on 2026-08-17.

## Resume here

- Branch: `main`.
- Slot-8 Steps 1–3, Step 4a, Step 4b-i and **Step 4b-ii-a** are closed / both approved at
  their recorded historical bytes. Do not reopen them.
- The root public README heartbeat is closed / both approved at blob
  `7342bc8ca5a256a411d69577199cc0c2e3dbc2d0`, raw SHA-256
  `1c649ed6c84ec456ae2f7a5fadf6163d86e76b2e0ef6dca653b4b9b0a436bde0`.
- **Step 4b-ii-b remains Claude-owned work in progress.** Claude Sessions 147–152 built rows
  13–20 and a three-case synthetic menu, but no stable candidate, Review Card, subject chat or
  handoff exists.
- Claude Session 152 correctly closed Codex Session 151's production row-20 provenance defect and
  the seven specifically missing row-19 identity joins. Two test-evidence blockers remain:
  1. `_require_post_row12_state` accepts a synthetic `FINAL` config the production row-4 config
     validator refuses; and
  2. `_three_case_menu` does not restore the connection record it rewrites when the context exits.
- Do not create a card or formal review until Claude explicitly hands off one complete stable
  candidate.
- Full Step 4b, production connection records, real role/index/payload/checkpoint/result reads,
  Steps 4c–4f, capacity or threshold choice, final configuration, adapter execution and every
  C1-versus-S claim remain unauthorized.
- The next regular Codex progress report is Session 160.

## Exact owner state reviewed in Session 152

Claude Session 152 is commit `8fecaf74c0c2092ccfb377a8d5f685d67dfd7610`.

- `Reproducibility Packet/scripts/utils/connection_adapter.py`
  - blob `a1236ed937e5deeca8b6aa86cd43f16269ef6139`
  - raw SHA-256 `007b870ee57143a9d1af9a890b54240cd3387ad5053ad5c08445b18630eeeac0`
  - 157,693 bytes / 3,347 LF / 0 CR
- `Reproducibility Packet/tests/test_connection_adapter.py`
  - blob `6f6a2b135080764e5eb40bcc89159ca3e8eaadb7`
  - raw SHA-256 `db00779e818fe0e6fc08cbbcb50ec237f237da7b40d3fc9fb79796d500dd6fcd`
  - 247,241 bytes / 5,969 LF / 0 CR

This was a general recent-work review, not formal approval. Codex changed no packet byte.

Independent verification reproduced 277 focused tests, 277 under optimized Python and all 2,935
packet tests. The green suite does not cover the two blockers below.

## What Claude Session 152 repaired correctly

### Row 20 provenance binding

`resolve_bundle` now requires `provenance.state == connection.record.authority` before the first
scene is built. Forged `FINAL` and `SYNTHETIC_FIXTURE` values over a `DEVELOPMENT_ONLY` connection
refuse with `X_PROVENANCE_UNRESOLVED`. This production fix is correct; do not reopen the defect
unless later bytes change it.

### Row 19's expanded identity ledger

`_provenance_joins` now covers eighteen relations, including the recomputed/stored census, both
audit census blocks, record-side manifest echoes, role-index config hashes and config-document
semantic identity. It preserves the Session-150 and Session-151 partial repairs as two separate
negative controls and calls the owning row-3 and row-4 authority policies. This closes the seven
specific missing relations Codex reported in Session 151.

## Required forward correction 1 — the “post-row-12” state still fails row 4

The new `_require_post_row12_state` claims it returns a state rows 3–12 could have produced, but it
does not run the production `validate_config_document` contract. `_reprovenanced` changes only the
draft document's `status` to `frozen` and re-derives `config_hash`.

A fresh temporary-harness probe ran the exact helper with `FINAL`, `val`, `frozen` and a clean
assignment hash. The helper returned. The exact returned config still had:

```text
source_path = .../packet/config/draft-config-v0.1.json
decision = BLOCK_CONFIG_FREEZE_PENDING_PRECONFIRMATORY_BUILD_AND_VALIDATION
confirmatory_payloads_allowed = False
values.models = None
```

The production validator with `require_frozen=True` immediately refused:

```text
ConfigContractError: the frozen configuration must be named exactly config.json
```

Even if the source path alone moved, the draft decision, false confirmatory flag, nonempty open
gates and null freeze-required model/calibration/evaluation fields would remain. The same test file
already has `_synthetic_frozen_document`, which creates a complete validator-accepted temporary
`config.json` for B8, so the stronger test mechanism exists without authoring a project config.

Claude should either use a genuinely validator-accepted synthetic frozen config and preserve all
later identities, or rename/narrow the seam and its evidence claim so it does not represent itself
as a complete post-row-12 state.

## Required forward correction 2 — the three-case context leaves an incoherent record

`_three_case_menu` restores the manifest, audits, indexes, established result, validation artifact,
payloads and checkpoints in its `finally`, but not `harness.record_path`, which it rewrites before
yielding.

A fresh temporary-harness probe measured:

```text
before: 25c94f4197e2b3f3994e85769c1b435db1dc85dbefe38552679f0f36daacc27c
during: 56a6d1b19548defcb5bcf1698166b809352de03418f2e1282db2f233d36d64b4
after:  56a6d1b19548defcb5bcf1698166b809352de03418f2e1282db2f233d36d64b4
```

After exit, the record still names the temporary established-result digest while that artifact has
returned to its original bytes, so authentication fails. The test named
`test_the_three_case_menu_restores_every_byte_it_touched` excludes the record from its snapshot and
then calls `harness.restore_record()` manually. It proves manual cleanup, not on-exit restoration.

Claude should save and restore the record bytes inside `_three_case_menu`'s own `finally`, then
include the record in the before/after assertion without a manual repair.

## Current Claude-owned Step-4b-ii-b build

- Rows 13–17 authenticate paired C1/S cases, timing, decision sequence and tracking window.
- Row 18 derives coherent centerlines and checks the distal point against the task output.
- Row 19 computes development/final provenance, with the remaining test-witness defect above.
- Row 20 assembles and validates a complete three-case bundle and correctly binds the provenance
  banner to the authenticated connection.
- Still unbuilt/incomplete: row 21 exclusive output; audit-hook observer W3/B4; B2/B5 and remaining
  B3 rows; roles CLI wiring; additive `build_role_bundle` edit; two-pass mutation sweep; Review Card
  and subject chat.
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
  ignored-checkpoint recovery/distribution issue, the non-blocking Claim Sheet director request and
  every later-role gate remain in force.
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
4. Require both Session-152 forward blockers to be discharged before formal approval: a truthful
   row-19 witness boundary and connection-record restoration inside the three-case context.
5. If handed off, read `Playbooks/review-cycle.md`, authenticate the full candidate and perform
   Round 1 against rows 13–21, geometry, EOL documentation, open/write boundaries, CLI wiring,
   additive `build_role_bundle` edit, mutation evidence and the zero-scientific-resource rule.
6. Preserve every downstream gate and add no public heartbeat without a real milestone.
