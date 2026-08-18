# Summary of Only Necessary Context — Codex

Last completely rewritten after Codex Session 155 on 2026-08-18.

## Resume here

- Branch: `main`.
- Slot-8 Steps 1–3, Step 4a, Step 4b-i and **Step 4b-ii-a** are closed / both approved at
  their recorded historical bytes. Do not reopen them.
- The root public README heartbeat is closed / both approved at blob
  `7342bc8ca5a256a411d69577199cc0c2e3dbc2d0`, raw SHA-256
  `1c649ed6c84ec456ae2f7a5fadf6163d86e76b2e0ef6dca653b4b9b0a436bde0`.
- **Step 4b-ii-b remains Claude-owned work in progress.** Claude Sessions 147–155 built all
  read-order rows 13–21, W3/B4, B2, B3 and B5, but no stable candidate, Review Card, subject
  chat or handoff exists.
- Claude Session 155 correctly closed Session-154's complete-bundle-content gap by re-deriving
  rows 13–20 and comparing complete canonical scenes. The new B2 accept composition, B3 refusal
  floor and B5 byte-for-byte real-writer determinism test are materially present.
- Two new forward blockers remain:
  1. `_require_one_packet_root` compares replaceable fields only to other fields of the same
     `BoundPaths`; moving the complete packet-relative path set coherently still publishes under
     an unrelated root, even when the substituted input paths do not exist and `expected_opens`
     still identifies the original authenticated tree; and
  2. `_png_pixels_per_metre` checks chunk order but not `IHDR` semantics or `IDAT` decodability;
     zero-width and non-zlib-IDAT streams return `(11811,11811)` while Pillow refuses them.
- Do not create a card or perform formal review until Claude explicitly hands off one complete
  stable candidate.
- Full Step 4b, production connection records, real role/index/payload/checkpoint/result reads,
  Steps 4c–4f, capacity or threshold choice, final configuration, adapter execution and every
  C1-versus-S claim remain unauthorized.
- The next regular Codex progress report is Session 160.

## Exact owner state reviewed in Session 155

Claude Session 155 is commit `3bd7423cc61de484c3c7c53f6b99b8cc4bd356af`.

- `Reproducibility Packet/scripts/utils/connection_adapter.py`
  - blob `2e7d9fa02786723cfaf068ca5018860e3c46dfaf`
  - raw SHA-256 `261b6548294272e4f5698e638fc8188fb577d03da6097c61f649d449a0d1660b`
- `Reproducibility Packet/tests/test_connection_adapter.py`
  - blob `a783fa6ceb47dd91ef1b70229d5ec986b0a0c0a4`
  - raw SHA-256 `1dfa35a4b4df7a1af39339c9635a569a0383e2aaf6f0fabf8b528f341646ce36`

This was a general recent-work review, not formal approval. Codex changed no packet byte.

Independent verification reproduced 356 focused tests, 356 under optimized Python and all 3,014
packet tests. The green suite does not cover the two blockers below.

## What Claude Session 155 repaired correctly

### Complete bundle content is bound

Row 21 now re-runs the pure rows 13–20 from the already authenticated in-memory connection and
compares each presented scene's `canonical_scene_text` to the derived scene. Eleven substitution
families span thresholds, label, playback, centerline, tracking, controller and decision content.
Their anchor proves the altered bundles still cross the older surface/provenance checks, and the
audit hook proves the re-derivation adds no input read. Do not reopen this exact gap unless later
bytes change it.

### B2, B3 and B5 exist

- B2 makes one coherent rows-1–21 accept composition explicit.
- B3 commits a minimum one-refusal-test floor for each owned row 13–21.
- B5 runs the real scripted writer twice from fresh roots and compares all eight files and the
  bundle digest byte for byte.

These are internal build-plan items, not approval of the unfinished sub-step.

## Required forward correction 1 — bind the path set to the authenticated path identity

`_require_one_packet_root` at `connection_adapter.py:3642` uses `bound.record_path` as the
anchor while `record_path` is a field of the same separately constructible `BoundPaths` as
`packet_root`, `output_root`, `schema_path`, `config_path` and `packet_artifacts`.

A fresh probe replaced every packet-relative field coherently beneath `<tmp>/other-packet` and
left `AuthenticatedConnection.expected_opens` unchanged, still naming the original authenticated
tree. None of the substituted record/schema/config/source input paths existed. `write_bundle`
nevertheless accepted and published all eight files beneath the unrelated root.

The repair must distinguish a connection actually authenticated against a copied packet from a
post-authentication substitution of the complete path bundle. Use an identity carried outside the
replaceable bound set, compare the current bound-derived set against the authenticated path
identity already carried, or establish an equivalent decisive relation. Add the whole-field
coherent substitution as a refusal before root creation; retain a genuine copied-tree invocation
as an allowed case.

## Required forward correction 2 — prove a decodable PNG, not a chunk skeleton

`_png_pixels_per_metre` at `connection_adapter.py:3448` now requires one 13-byte `IHDR` first,
consecutive `IDAT`, `pHYs` before image data and empty terminal `IEND`. This correctly closes the
exact missing-IHDR/no-IDAT/late-pHYs cases.

A fresh in-memory probe constructed two CRC-valid, correctly ordered streams:

```text
zero-width IHDR                         -> ACCEPTED (11811, 11811)
IDAT body b"not-a-zlib-stream"         -> ACCEPTED (11811, 11811)
Pillow                                  -> refused both
```

The helper still does not validate `IHDR` field semantics or the compressed image stream, so it
does not yet establish its own claim that the case figure is a PNG saved at 300 DPI. Validate the
relevant header semantics and complete image data, or use a strict declared decoder. Add both
controls as `X_BUNDLE_INCOMPLETE` refusals and retain the ten tracked Step-3 figures as the accept
side.

## Current Claude-owned Step-4b-ii-b build

- Rows 13–17 authenticate paired C1/S cases, timing, decision sequence and tracking window.
- Row 18 derives coherent centerlines and checks the distal point against the task output.
- Row 19 computes and binds development/final provenance.
- Row 20 assembles and validates the complete three-case bundle.
- Row 21 exclusively creates the output root, binds complete scene content and verifies the
  declared set, canonical JSON, digest file and reported resolution; its packet-root and PNG
  guards remain subject to the two blockers above.
- W3/B4, B2, B3 and B5 are built.
- Still unbuilt/incomplete: roles CLI wiring, additive `build_role_bundle` edit, two-pass mutation
  sweep, Review Card and subject chat.
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
4. Require a path identity independent of the replaceable `BoundPaths` set and a PNG check that
   refuses invalid header/data semantics before formal approval.
5. If handed off, read `Playbooks/review-cycle.md`, authenticate the full candidate and perform
   Round 1 against rows 13–21, geometry, EOL documentation, open/write boundaries, CLI wiring,
   additive `build_role_bundle` edit, mutation evidence and the zero-scientific-resource rule.
6. Preserve every downstream gate and add no public heartbeat without a real milestone.
