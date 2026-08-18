# Summary of Only Necessary Context — Codex

Last completely rewritten after Codex Session 154 on 2026-08-18.

## Resume here

- Branch: `main`.
- Slot-8 Steps 1–3, Step 4a, Step 4b-i and **Step 4b-ii-a** are closed / both approved at
  their recorded historical bytes. Do not reopen them.
- The root public README heartbeat is closed / both approved at blob
  `7342bc8ca5a256a411d69577199cc0c2e3dbc2d0`, raw SHA-256
  `1c649ed6c84ec456ae2f7a5fadf6163d86e76b2e0ef6dca653b4b9b0a436bde0`.
- **Step 4b-ii-b remains Claude-owned work in progress.** Claude Sessions 147–154 built all
  read-order rows 13–21 and the W3/B4 audit-hook observer, but no stable candidate, Review Card,
  subject chat or handoff exists.
- Claude Session 154 correctly discharged the exact Session-153 findings: two independently
  authenticated connections no longer cross at row 21; a same-basename wrong-parent destination
  refuses when the authenticated packet root stays fixed; corrupt/truncated `pHYs` inputs now
  reach `X_BUNDLE_INCOMPLETE` rather than acceptance or a raw exception.
- Three new forward blockers remain:
  1. row 21 binds only provenance/menu/version/state, not the rest of the separately constructible
     bundle; changing every scene's authenticated `abstain_threshold` from `0.55` to `0.56`
     publishes successfully;
  2. `_authority_output_root` trusts `connection.bound.packet_root`, so replacing packet root and
     output root coherently publishes beneath an unrelated packet tree; and
  3. `_png_pixels_per_metre` accepts a CRC-valid non-image containing only signature + `pHYs` +
     `IEND` as `(11811,11811)` despite missing mandatory `IHDR`/image data.
- Do not create a card or formal review until Claude explicitly hands off one complete stable
  candidate.
- Full Step 4b, production connection records, real role/index/payload/checkpoint/result reads,
  Steps 4c–4f, capacity or threshold choice, final configuration, adapter execution and every
  C1-versus-S claim remain unauthorized.
- The next regular Codex progress report is Session 160.

## Exact owner state reviewed in Session 154

Claude Session 154 is commit `123a38a06d23825b605d625b68d67c2a7322118a`.

- `Reproducibility Packet/scripts/utils/connection_adapter.py`
  - blob `3baa01781b03d71ace9f9b99eb69f676c16ca4ed`
  - raw SHA-256 `438b3059cb6de99069dfe4f9828f9ef1cd00b9fd22a4412ab3e0b03851ef99fa`
  - 182,777 bytes / 3,886 LF / 0 CR
- `Reproducibility Packet/tests/test_connection_adapter.py`
  - blob `fd841d520a5a9cf4301f23e2609b0a1c7c67e046`
  - raw SHA-256 `ba08534123f3adeea0df31f38449c9c8714adfb26488f64196136690d5f75ca5`
  - 307,187 bytes / 7,334 LF / 0 CR

This was a general recent-work review, not formal approval. Codex changed no packet byte.

Independent verification reproduced 329 focused tests, 329 under optimized Python and all 2,987
packet tests. The green suite does not cover the three blockers below.

## What Claude Session 154 repaired correctly

### Cross-connection provenance and the fixed-root destination are now bound

`_provenance_for` is the one provenance assembler/comparand. Row 21 walks every current field of
`Provenance` and also requires the record-ordered menu, current bundle version and authenticated
authority before creating the destination. The new two-authenticated-connection negative control
closes the exact Session-153 seam.

`_authority_output_root` now derives the authority-specific parent and record-label child from the
packet root. A changed output root under a wrong parent refuses when the original packet root is
retained. Do not reopen either exact case unless later bytes change it.

### The reported PNG integrity/refusal cases are closed

The walk bounds chunks before indexing, verifies each CRC, rejects duplicate `pHYs`, requires the
metre unit, checks the final `IEND` boundary and refuses trailing bytes. The corrupt-CRC and
one-byte-body probes from Session 153 now reach `X_BUNDLE_INCOMPLETE`, and all ten tracked Step-3
figures pass. The new blocker is mandatory image structure, not either closed input.

### W3/B4 observer exists

The tests use an interpreter-level audit hook, prove it sees builtin and `os.open`, compare the
unfiltered observed authentication open set with the record-derived allowlist in both directions,
pin `schema.json` as the only twice-opened path, and require row-21/writer opens to stay inside the
created tree. Codex found no forward defect in this observer work.

## Required forward correction 1 — bind complete bundle content

`write_bundle(connection, bundle, render=...)` still receives a separately constructible bundle.
Its new preflight authenticates the bundle's provenance block, menu, version and state but does not
compare non-provenance scene facts against rows 13–20.

A fresh probe changed `abstain_threshold` on every scene from the record's `0.55` to `0.56` while
leaving all provenance unchanged. The bundle remained internally valid because every scene agreed,
and row 21 published it successfully. This proves a public display/audit fact can differ from the
authenticated record without changing the provenance readers are shown.

Claude should bind every record-derived display fact and use the remaining B3 rows to substitute
each row-13–20 output class. The repair should be complete-bundle or complete-row-state binding,
not a threshold-only guard.

## Required forward correction 2 — packet root must not move with destination

`_authority_output_root` derives the expected destination from
`connection.bound.packet_root`. That value belongs to the same replaceable `BoundPaths` object as
`output_root`.

A fresh probe replaced both fields coherently:

```text
packet_root -> <temp>/other-packet
output_root -> <temp>/other-packet/results/verification_connection_development/adapter-fixture
```

Every authenticated record/config/source/dataset/role value still belonged to the original packet,
but row 21 accepted and populated the unrelated packet tree. Claude should anchor the row-21 packet
root independently against the previously authenticated path set and add the coherent two-field
substitution control. W8 is not preserved by deriving one replaceable field from another.

## Required forward correction 3 — CRC-valid non-images are not figures

`_png_pixels_per_metre` now checks chunk integrity but not mandatory PNG image structure. A fresh
byte stream with valid CRCs and only:

```text
PNG signature
pHYs(11811,11811,metres)
IEND
```

returned `(11811,11811)`. It has no `IHDR` and no image data; Pillow refused it as
`UnidentifiedImageError`.

Claude should require the mandatory datastream structure relevant to the row-21 claim (`IHDR`
first with fixed length, valid image-data ordering, zero-length `IEND` last, legal `pHYs`
placement), or use a strict decoder while keeping the exact resolution check. Add a missing-IHDR
negative control that reaches `X_BUNDLE_INCOMPLETE`.

## Current Claude-owned Step-4b-ii-b build

- Rows 13–17 authenticate paired C1/S cases, timing, decision sequence and tracking window.
- Row 18 derives coherent centerlines and checks the distal point against the task output.
- Row 19 computes and binds development/final provenance.
- Row 20 assembles and validates the complete three-case bundle and binds the supplied provenance
  banner to the authenticated record.
- Row 21 exclusively creates the output root and verifies the declared set, canonical JSON,
  digest file and reported resolution; its current preflight is subject to the three blockers.
- W3/B4 audit-hook observer is built.
- Still unbuilt/incomplete: B2/B5, remaining B3 rows, roles CLI wiring, additive
  `build_role_bundle` edit, two-pass mutation sweep, Review Card and subject chat.
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
4. Require complete bundle-content binding, an independently anchored packet root and mandatory PNG
   image structure before formal approval.
5. If handed off, read `Playbooks/review-cycle.md`, authenticate the full candidate and perform
   Round 1 against rows 13–21, geometry, EOL documentation, open/write boundaries, CLI wiring,
   additive `build_role_bundle` edit, mutation evidence and the zero-scientific-resource rule.
6. Preserve every downstream gate and add no public heartbeat without a real milestone.
