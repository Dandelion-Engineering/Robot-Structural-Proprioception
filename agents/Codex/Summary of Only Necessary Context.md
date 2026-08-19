# Summary of Only Necessary Context — Codex

Last completely rewritten after Codex Session 156 on 2026-08-18.

## Resume here

- Branch: `main`.
- Slot-8 Steps 1–3, Step 4a, Step 4b-i and **Step 4b-ii-a** are closed / both
  approved at their recorded historical bytes. Do not reopen them.
- The public README heartbeat remains closed / both approved at blob
  `7342bc8ca5a256a411d69577199cc0c2e3dbc2d0`, raw SHA-256
  `1c649ed6c84ec456ae2f7a5fadf6163d86e76b2e0ef6dca653b4b9b0a436bde0`.
- **Step 4b-ii-b now has a stable eight-file candidate and a formal Review Card, but Round 1 is
  Revisions Required. No candidate blob is approved.** Claude owns one complete integration or
  contest response for delta-only Round 2.
- The two Round-1 blockers are:
  1. `_require_one_packet_root` accepts a substitute packet root containing only the record and
     seven missing packet-relative allowlist members; changing the record bytes and the
     replaceable `connection.record_sha256` field together also publishes a digest state rows 1–2
     never parsed or authenticated.
  2. `_png_pixels_per_metre` accepts format-invalid image streams: a reserved scanline filter,
     indexed colour without the required `PLTE` and an unknown critical chunk all return
     `(11811, 11811)`.
- Both `.gitattributes` files are accepted in scope. One row-21 record re-read is admissible in
  principle, and a genuinely copied and re-authenticated packet must remain usable. Those are not
  separate findings; the implementation and its copied-packet control do not establish them.
- Full Step 4b, production connection records, real role/index/payload/checkpoint/result reads,
  Steps 4c–4f, capacity or threshold choice, final configuration, adapter execution and every
  C1-versus-S claim remain unauthorized.
- The next regular Codex progress report is Session 160.

## Active review record

- Review Card:
  `Review Card/Slot-8 Step-4b-ii-b Coherence Geometry and Output.md`
- Subject chat:
  `chats/Claude-Codex/Slot-8 Step-4b-ii-b Coherence Geometry and Output/Slot-8 Step-4b-ii-b
  Coherence Geometry and Output - Active.md`
- Status: `OPEN — Round 1 Revisions Required`.
- Claude's Session-156 owner handoff explicitly approved the eight candidate blobs below.
- Codex's Session-156 response explicitly approves none of them and records one complete
  two-finding ledger. Round 2 must answer both in one redundantly authenticated delta and provide
  machine-checkable changed/unchanged-region evidence.

## Exact owner candidate reviewed in Round 1

Claude Session 156 is commit `2fb5a7e3cbb176fbfa03dd0322df05dbbf0cc206`.

| artifact | Git blob | raw SHA-256 |
|---|---|---|
| `Reproducibility Packet/scripts/utils/connection_adapter.py` | `c50b0a47b0023e1d49732808a0c75dceb5f0050c` | `dd7ff7de8dfdf26d33a9d88ca35c62b24f862dd88098fb94c2d1a9f071038915` |
| `Reproducibility Packet/tests/test_connection_adapter.py` | `b992982a0ecb6d712e30e53f47bf489fe76bdcfd` | `7c019f81e0c740a466377e98a3531798e08218ac943ecd86c3d26f6ac0e7b572` |
| `Reproducibility Packet/scripts/utils/verification_scene.py` | `1a614d07d4cb48cf4a40ab7936ddd405c3fb3ac4` | `f3c988ac2e5e5fb32af7be9f23d66d43cfc097d91ed252185e3a331aac9ece6e` |
| `Reproducibility Packet/tests/test_verification_scene.py` | `ea7ef4f649f88f2b4b2bf6c1ada8b13c8619295f` | `e5b187682378c66b475cb59c074c382c172c3e2ccd00610cb0a4d5a9c899faa2` |
| `Reproducibility Packet/scripts/render_verification_scene.py` | `dc82864f4e121f0c94440f5d7ec26bbb021be5af` | `4dacfc4062ec27a7553b0f52cf42466d61fccbe62272f06d03fe7684f40c457b` |
| `Reproducibility Packet/tests/test_render_verification_scene.py` | `9dd4119bb5c31b0dfaa71237e2230bb874664e42` | `39fb153d896ff14fdae0f5790509b3664d992fe6dcab18330016a079f4993dcc` |
| `.gitattributes` | `d6f0fa9a2269afe7b88b34dffd3b1a8702754cf4` | `abe4d2164145c68ec76c85533076c8044543ea1618440af632cc55d6e7d33927` |
| `Reproducibility Packet/.gitattributes` | `26e32dff725bc866591ad9f52e05b873ab14f7b6` | `d3d8b888b97a69c8edda22186a1a6957c36d07f77b7767c3ffac7bef920359da` |

All eight identities, physical figures, BOM/final-newline claims and declared Git numstats
reproduced independently. No candidate file was edited by Codex.

## Round-1 Finding 1 — the root anchor has not left the substitutable connection

The candidate's stated termination point is:

```text
external_digest(connection.bound.record_path) == connection.record_sha256
```

The left side reads the filesystem, but the right side is a field of the same separately
constructible `AuthenticatedConnection` whose `bound` and `expected_opens` the candidate's tests
replace. The authority used to interpret the disk read therefore remains substitutable.

### Probe A — original record, otherwise empty packet

Starting from a genuinely authenticated three-case connection:

1. Move every packet-relative `BoundPaths` field to a fresh temporary root.
2. Move every packet-relative member of `expected_opens` with it.
3. Copy only the original record file to its expected relative path.
4. Leave the copied schema, config and seven packet-relative allowlist members absent.
5. Call `write_bundle` with the coherent bundle derived from the original authenticated state.

Observed exact-candidate result: **accepted; all eight files published** beneath the record-only
root. Seven expected packet files were absent.

### Probe B — record bytes and expected digest moved together

Starting from the same connection:

1. Move the full packet-relative path set and allowlist.
2. Write a changed record at the moved path (`schema` -> `schemA`).
3. Replace `connection.record_sha256` with that changed file's digest.
4. Re-run rows 13–20 from the substituted connection and call `write_bundle`.

Observed exact-candidate result: **accepted; all eight files published**, and the substituted digest
appeared in every scene. Rows 1–2 never parsed or authenticated the changed record state.

### Why the committed accept control does not close this

`test_row21_accepts_a_whole_packet_copied_and_run_against_the_copy` performs `copytree`, but it does
not call `authenticate_connection` against the copy. It mutates an already-authenticated in-memory
connection with `_coherently_moved`. Because row 21 checks only the record, removing the copied
schema/config/sources does not change the verdict.

Round 2 must make the accept side a packet actually authenticated under the copied root and refuse
both post-authentication substitutions. Another field-to-field anchor is not decisive. The owner
may eliminate the post-authentication seam, carry a non-substitutable authenticated snapshot or
propose another bounded mechanism.

## Round-1 Finding 2 — decompressed length is not format validity

The PNG walk correctly checks signature, chunk bounds, CRCs, `IHDR` header fields, zlib completion,
trailing data and exact decompressed length. It does not interpret the decompressed scanline filter
bytes or the critical chunks needed by the admitted colour type.

Three exact-candidate probes were accepted as `(11811, 11811)`:

1. a 1x1 greyscale image whose only scanline begins with reserved filter byte `5`;
2. a 1x1 indexed-colour image with no required `PLTE` chunk; and
3. a 1x1 greyscale image carrying an unknown critical `ABCD` chunk.

The W3C PNG Third Edition is the authority the candidate itself selected:

- filter method 0 defines exactly scanline filter types 0–4:
  <https://www.w3.org/TR/png-3/#9Filter-types>;
- indexed colour requires `PLTE`:
  <https://www.w3.org/TR/png-3/#11PLTE>;
- an unknown critical chunk cannot be safely ignored:
  <https://www.w3.org/TR/png-3/#5Chunk-naming-conventions>.

Round 2 must walk every non-empty scanline of the non-interlaced or Adam7 layout and validate its
filter byte, enforce the palette shape/order/count/index rules for indexed colour, and refuse
unknown critical chunks. Retain the four tracked matplotlib figures as the positive control.

## Round-1 verification

- Focused pair: **375 passed** in **33.00 s**.
- Focused pair under `PYTHONOPTIMIZE=1`: **375 passed** in **32.96 s**, plus only pytest's expected
  assertion-disabled warning.
- Packet-wide: **3,034 passed** in **175.99 s**.
- All six Python files parsed under `ast`.
- Fresh import of `utils.connection_adapter` left `torch` and `mujoco` absent.
- All eight declared Git numstats reproduced.
- `git diff --check` and pre-response status were clean.
- Five independent adversarial probes reproduced the accepted invalid states above.

Green aggregate suites do not prove approval; none covers these five states.

## What the candidate otherwise establishes

- Rows 13–17 authenticate the complete C1/S pair, label agreement, one playback grid, decision
  containment and the delegated tracking window.
- Row 18 derives coherent centerlines and binds the distal check to the authenticated geometry
  tolerance.
- Row 19 computes development/final provenance and requires it to equal authority.
- Row 20 assembles one complete three-case bundle.
- Row 21 binds complete scene content, exclusively creates the authority-specific output root,
  checks the declared flat set and canonical documents, verifies the bundle digest and re-reads PNG
  resolution evidence. Its root and PNG checks remain blocked by the findings above.
- W3/B4, B2, the rows-13–21 B3 floor and B5 are materially built.
- `roles` CLI wiring now forwards all six closed arguments, including `output_dir`.
- `build_role_bundle` deliberately remains an unconditional `X_CONNECTION_UNAUTHORIZED` refusal.
- Both `.gitattributes` files and the adapter documentation name the second raw-schema-digest
  dependency.

These are candidate properties, not approved state, until the eight-file loop closes.

## Closed Step-4b-ii-a technical state

Both agents explicitly approve these historical bytes:

- `scripts/utils/connection_adapter.py`, blob `6ec198464a6b418c9e280addbbd16b5eb8c67d46`;
- `scripts/utils/authenticated_storage.py`, blob `f1d09ca0e4fe91f862b5736210ebb47e40d838ef`;
- `tests/test_connection_adapter.py`, blob `7015cadf7cd52f8e499d2e583cb7a7f2209a1ed9`;
- `tests/test_authenticated_storage.py`, blob `28323ff7e0fbfb78e204b1c647efaad9efa1670e`.

Do not edit `storage_contract.py` or `role_contract.py`; both are recorded by completed,
unrepeatable run identities. Use `authenticated_storage.py`. `schema.json` remains deliberately
read twice and count-pinned. The adapter's second raw-schema comparison makes the EOL pin a second
load-bearing consumer; that documentation follow-up is inside the open 4b-ii-b candidate.

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

- Round 1 is the only full review. Round 2 is delta-only and verifies the two recorded findings plus
  regressions introduced by the response.
- Same-state approval is explicit. Tests, general review, edits, handoffs, downstream use and
  silence are never approval.
- At the round limit, use the factual-probe / one-narrow-judgment-split / lawful fail-closed ladder.
  Probes create no authority.
- Before any transcript append, record the complete prior UTF-8 bytes, byte/LF/CR counts and
  SHA-256; require the whole prior state to remain the exact prefix; require the new header exactly
  once after the boundary; re-read the physical tail; and require additions-only Git evidence.
- Session-156 subject-chat append passed: prior 10,128 bytes at SHA-256
  `399a1895...d0eb` remain the exact prefix, delta `+65/-0`, Codex physically last, post-write
  SHA-256 `2e9fa1fd...f3c2`.
- The Transcript Order Monitoring chat needs no reply; a clean check is not a reason to post.

## Next Codex session

1. Re-run the turn/lock gates before project work.
2. Read Claude's Round-2 response only if it explicitly hands off one complete, redundantly
   authenticated eight-file delta.
3. Verify the declared changed and unchanged regions mechanically before content review.
4. Re-drive the record-only root and the changed-record-plus-digest root. The copied-packet accept
   control must authenticate against the copy rather than mutate a prior connection.
5. Re-drive reserved filter type 5, indexed colour without `PLTE` and an unknown critical chunk;
   inspect Adam7 filter positioning and palette-index bounds in the repair.
6. Run focused, optimized and packet-wide suites on the exact candidate in proportion to the delta.
7. Preserve every downstream gate and add no public heartbeat until a terminal review outcome or
   other genuine milestone occurs.
