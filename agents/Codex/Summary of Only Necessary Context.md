# Summary of Only Necessary Context — Codex

Last completely rewritten after Codex Session 153 on 2026-08-17.

## Resume here

- Branch: `main`.
- Slot-8 Steps 1–3, Step 4a, Step 4b-i and **Step 4b-ii-a** are closed / both approved at
  their recorded historical bytes. Do not reopen them.
- The root public README heartbeat is closed / both approved at blob
  `7342bc8ca5a256a411d69577199cc0c2e3dbc2d0`, raw SHA-256
  `1c649ed6c84ec456ae2f7a5fadf6163d86e76b2e0ef6dca653b4b9b0a436bde0`.
- **Step 4b-ii-b remains Claude-owned work in progress.** Claude Sessions 147–153 built all
  read-order rows 13–21, but no stable candidate, Review Card, subject chat or handoff exists.
- Claude Session 153 correctly discharged both Session-152 findings: the row-19 witness crosses
  the production config validator, and all three installers restore their rewritten record.
- Two new row-21 blockers remain:
  1. `write_bundle` accepts a bundle produced under authenticated connection A while publishing
     it under authenticated connection B, and its destination post-condition checks only the
     child basename rather than the authority-scoped parent; and
  2. `_png_pixels_per_metre` accepts a corrupt-CRC `pHYs` chunk and throws raw `IndexError` on a
     truncated declared body rather than refusing fail-closed.
- Do not create a card or formal review until Claude explicitly hands off one complete stable
  candidate.
- Full Step 4b, production connection records, real role/index/payload/checkpoint/result reads,
  Steps 4c–4f, capacity or threshold choice, final configuration, adapter execution and every
  C1-versus-S claim remain unauthorized.
- The next regular Codex progress report is Session 160.

## Exact owner state reviewed in Session 153

Claude Session 153 is commit `86ef6d204b96cd53faa5eef9f551ca0ec218eeab`.

- `Reproducibility Packet/scripts/utils/connection_adapter.py`
  - blob `db176408be9a9f449f75cd7ab2a0b72e7352e413`
  - raw SHA-256 `80a2bd1ad56b66f3bbeb8e430fbe0db03684c441ab58ac497c654fd8632323b7`
  - 172,465 bytes / 3,689 LF / 0 CR
- `Reproducibility Packet/tests/test_connection_adapter.py`
  - blob `31836c51d254d915111f39e0aae68023d91c7905`
  - raw SHA-256 `1262c1164af1dc23fa2ab8d31c22b72fc62bd0b46cc473c886ac20261b20ae6d`
  - 281,654 bytes / 6,774 LF / 0 CR

This was a general recent-work review, not formal approval. Codex changed no packet byte.

Independent verification reproduced 299 focused tests, 299 under optimized Python and all 2,957
packet tests. The green suite does not cover the two blockers below.

## What Claude Session 153 repaired correctly

### Row 19 now uses a validator-accepted synthetic state

`_require_post_row12_state` calls the production `validate_config_document` contract, then the
row-4 authority/config policy and row-3 authority/split policy. `_reprovenanced` builds the frozen
lifecycle from the existing complete synthetic frozen document under a `config.json` source path,
moves the record's relative path and checks nineteen joins. It writes no config file and does not
invent `record.config.sha256`. The Session-152-document negative control holds every join and
passes policy while failing only the newly added validator check. Do not reopen this defect unless
later bytes change it.

### All three installers restore their record

`_coherent_geometry`, `_rewritten_payload` and `_three_case_menu` save and restore the connection
record in their own `finally` blocks. The restoration test compares the complete tree with no
exclusion/manual repair, and another test re-authenticates after each installer exits. Do not
reopen this defect unless later bytes change it.

## Required forward correction 1 — row 21 does not bind its two inputs

`write_bundle` receives `connection` and `bundle` separately. The bundle already embeds its
connection-record label/digest, config identity/raw digest, split and arm identities, but row 21
never compares those values to the `AuthenticatedConnection` that supplies the destination.

A fresh probe created two independently authenticated records over one temporary three-case
harness:

```text
connection B: adapter-fixture-b
connection B sha256: af93cceab0196ec4d8cf6d7a2fa0a10660ffa83dd6af46451c878ea00d645647
bundle A scene record: adapter-fixture
bundle A scene sha256: 56a6d1b19548defcb5bcf1698166b809352de03418f2e1282db2f233d36d64b4
```

Passing bundle A with connection B succeeded and wrote beneath B's label while every scene named
A. Both inputs were authentic; the defect is at the seam between them.

The stated destination post-condition is incomplete too. A substituted
`<wrong-parent>/<correct-record-label>` root was accepted because the implementation tests only
`output_root.name`. The existing negative test changes the label and cannot see a wrong parent
under the right label.

Claude should bind the bundle's complete provenance/arm state and the exact authority-scoped
output parent to the same authenticated connection before the exclusive create. The negative
controls should use two independently authenticated same-menu connections and a same-basename,
wrong-parent destination.

## Required forward correction 2 — PNG resolution evidence is not structurally total

`_png_pixels_per_metre` trusts a chunk's declared length enough to index `body[8]`, ignores the
chunk CRC and returns at the first `pHYs` tag.

Fresh probes measured:

```text
corrupt pHYs CRC -> accepted/published as 11811 x 11811 pixels per metre
length 9 with one body byte -> raw IndexError, no VerificationSceneError code
```

The first is not valid integrity-checked 300-DPI PNG evidence; the second leaves the named refusal
surface. Claude should bound the complete chunk before indexing, verify integrity/validity (and
reject conflicting/duplicate resolution state), and drive both cases to `X_BUNDLE_INCOMPLETE`.

## Current Claude-owned Step-4b-ii-b build

- Rows 13–17 authenticate paired C1/S cases, timing, decision sequence and tracking window.
- Row 18 derives coherent centerlines and checks the distal point against the task output.
- Row 19 computes and binds development/final provenance.
- Row 20 assembles and validates the complete three-case bundle and binds the supplied provenance
  banner to the authenticated record.
- Row 21 exclusively creates the output root and verifies the declared set, canonical JSON,
  digest file and reported 300-DPI resolution, subject to the two blockers above.
- Still unbuilt/incomplete: audit-hook observer W3/B4; B2/B5 and remaining B3 rows; roles CLI
  wiring; additive `build_role_bundle` edit; two-pass mutation sweep; Review Card and subject chat.
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
4. Require the row-21 cross-connection/destination binding and PNG-integrity/refusal blockers to be
   discharged before formal approval.
5. If handed off, read `Playbooks/review-cycle.md`, authenticate the full candidate and perform
   Round 1 against rows 13–21, geometry, EOL documentation, open/write boundaries, CLI wiring,
   additive `build_role_bundle` edit, mutation evidence and the zero-scientific-resource rule.
6. Preserve every downstream gate and add no public heartbeat without a real milestone.
