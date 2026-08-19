# Summary of Only Necessary Context - Codex

Last completely rewritten after Codex Session 157 on 2026-08-19.

## Resume here

- Branch: `main`.
- Slot-8 Steps 1-3, Step 4a, Step 4b-i and **Step 4b-ii-a** are closed / both
  approved at their recorded historical bytes. Do not reopen them.
- The public README heartbeat remains closed / both approved at blob
  `7342bc8ca5a256a411d69577199cc0c2e3dbc2d0`, raw SHA-256
  `1c649ed6c84ec456ae2f7a5fadf6163d86e76b2e0ef6dca653b4b9b0a436bde0`.
- **Step 4b-ii-b remains open after Codex Session 157 returned Round 2 as Revisions Required. No
  candidate blob is approved.** Claude owns the next complete owner response.
- Round-1 Finding 2 is closed: the PNG repair now refuses the reported invalid streams and the
  widened palette/index/Adam7 cases.
- Round-1 Finding 1 remains blocking through a response-introduced witness defect: the new issued
  witness stores `packet_root`, `record_path`, `record_sha256`, `record_label` and `authority` in
  public slot fields. Public `object.__setattr__` can rewrite an already-issued witness while the
  same object remains in `_ISSUED_WITNESSES`, and `_require_one_packet_root` then reads the mutated
  fields as authority.
- Full Step 4b, production connection records, real role/index/payload/checkpoint/result reads,
  Steps 4c-4f, adapter execution, capacity or threshold choice, final configuration and every
  C1-versus-S claim remain unauthorized.
- The next regular Codex progress report is Session 160.

## Active review record

- Review Card:
  `Review Card/Slot-8 Step-4b-ii-b Coherence Geometry and Output.md`
- Subject chat:
  `chats/Claude-Codex/Slot-8 Step-4b-ii-b Coherence Geometry and Output/Slot-8 Step-4b-ii-b
  Coherence Geometry and Output - Active.md`
- Status: `OPEN - Round 2 Revisions Required`.
- Claude's Session-157 owner handoff explicitly approved the exact Round-2 eight-file state.
- Codex's Session-157 response explicitly approves none of it, closes only the PNG finding, and
  records one blocking response-introduced witness-authority gap.

## Exact owner candidate reviewed in Round 2

Claude Session 157 is commit `e5c0925` (`Claude Session 157`).

| artifact | Git blob | raw SHA-256 | Round-2 state |
|---|---|---|---|
| `Reproducibility Packet/scripts/utils/connection_adapter.py` | `a531011027d29a476c802ec540d1b719bbe921a2` | `be501eb531d38bf02e07a20d8fb2b0c8275544baf9c3fd8bd74ca4300eee8e79` | changed from Round 1; `+583/-70`; 238,496 bytes; 4,962 LF; 0 CR; no BOM; final LF |
| `Reproducibility Packet/tests/test_connection_adapter.py` | `894feea7c92b6cb652e7dfbbdd38646690c3ddde` | `c523d2a09c4608e86762257ed979ed3755db4582c7e9f929234ce6112f1dff4c` | changed from Round 1; `+726/-33`; 392,157 bytes; 9,122 LF; 0 CR; no BOM; final LF |
| `Reproducibility Packet/scripts/utils/verification_scene.py` | `1a614d07d4cb48cf4a40ab7936ddd405c3fb3ac4` | `f3c988ac2e5e5fb32af7be9f23d66d43cfc097d91ed252185e3a331aac9ece6e` | unchanged from Round 1 |
| `Reproducibility Packet/tests/test_verification_scene.py` | `ea7ef4f649f88f2b4b2bf6c1ada8b13c8619295f` | `e5b187682378c66b475cb59c074c382c172c3e2ccd00610cb0a4d5a9c899faa2` | unchanged from Round 1 |
| `Reproducibility Packet/scripts/render_verification_scene.py` | `dc82864f4e121f0c94440f5d7ec26bbb021be5af` | `4dacfc4062ec27a7553b0f52cf42466d61fccbe62272f06d03fe7684f40c457b` | unchanged from Round 1 |
| `Reproducibility Packet/tests/test_render_verification_scene.py` | `9dd4119bb5c31b0dfaa71237e2230bb874664e42` | `39fb153d896ff14fdae0f5790509b3664d992fe6dcab18330016a079f4993dcc` | unchanged from Round 1 |
| `.gitattributes` | `d6f0fa9a2269afe7b88b34dffd3b1a8702754cf4` | `abe4d2164145c68ec76c85533076c8044543ea1618440af632cc55d6e7d33927` | unchanged from Round 1 |
| `Reproducibility Packet/.gitattributes` | `26e32dff725bc866591ad9f52e05b873ab14f7b6` | `d3d8b888b97a69c8edda22186a1a6957c36d07f77b7767c3ffac7bef920359da` | unchanged from Round 1 |

Note: the subject chat's `+674/-33` test-file delta is a transcript-summary typo; Git, the Review
Card and Claude's HumanReport157 agree on `+726/-33`.

## Round-2 blocking finding - issued witness authority is mutable

Claude's repair introduced `_AuthenticationWitness`, issued by `authenticate_connection` and checked
by identity in `_ISSUED_WITNESSES`. The intended property is that row 21 uses the root, record path,
record digest, label and authority that the authentication chain resolved, not fields supplied by a
later `dataclasses.replace`.

The implementation still stores those authority values in public slot fields. Normal
`setattr(witness, "packet_root", ...)` and `delattr(witness, "packet_root")` refuse, but
`object.__setattr__(witness, "packet_root", substitute_root)` and
`object.__setattr__(witness, "record_path", substitute_record)` succeed. Because table membership is
by object identity, the same mutated witness remains issued. `_require_one_packet_root` then reads
the mutated fields back as authority.

Direct probe reproduced by Codex Session 157:

1. Authenticate the ordinary three-case fixture.
2. Copy only the original connection record into a fresh temporary root.
3. Coherently move every packet-relative `BoundPaths` field and every packet-relative
   `expected_opens` member to that root.
4. Mutate the issued witness's `packet_root` and `record_path` with public `object.__setattr__`.
5. Call `write_bundle` with the original authenticated bundle.

Observed result: **accepted**. The substitute root held the copied record plus all eight publication
outputs, while schema, config and packet artifacts were still absent. This is response-introduced;
Round 1 had no witness.

Required Round-3 repair: row 21 must read immutable issued authority state, not rewritable witness
attributes. A private registry keyed by issued witness identity is one acceptable mechanism, but
Claude may choose another. The exact `object.__setattr__` attack must become a committed refusal
test, and after the mutation the publication authority must remain the state originally issued by
`authenticate_connection`.

## Closed Round-2 PNG ruling

Round-1 Finding 2 is closed. The PNG code now:

- refuses unknown critical chunks;
- enforces PLTE presence, order, length and count for the admitted colour type;
- reconstructs indexed scanlines before checking palette index bounds;
- walks every non-empty scanline of the declared non-interlaced or Adam7 layout;
- retains positive controls for valid indexed images and the four tracked Step-3 matplotlib
  figures.

Codex's requested rulings:

1. The four coherence checks below the witness are acceptable diagnostics once authority is no
   longer read from mutable witness fields.
2. The witness mechanism is not itself a W8 protocol amendment; it implements W8's existing one-root
   authority unless the next repair changes the protocol surface.
3. Indexed-image reconstruction is in scope because row 21 claims PNG-format validity.

## Round-2 verification

- Direct witness-mutation probe: **accepted invalid record-only root** (blocking).
- Targeted Round-2 tests: **53 passed, 336 deselected** in **1.45 s**.
- Focused pair: **409 passed** in **31.08 s**.
- Focused pair under `PYTHONOPTIMIZE=1`: **409 passed** in **31.35 s**, plus only pytest's expected
  assertion-disabled warning.
- Packet-wide: **3,068 passed** in **180.97 s**.
- Packet-wide under `PYTHONOPTIMIZE=1`: **3,068 passed** in **183.43 s**, plus only pytest's
  expected warning.
- `git diff --check 0983130 e5c0925` was clean before Codex documentation edits.
- Subject-chat append passed its byte protocol: prior 22,476 bytes at SHA-256
  `8d1de0a3ba0b1435f829b2d55758f2d858a2daa083b0f75aff055891c580d84e` remain exact prefix;
  post-write 25,607 bytes, 394 LF, 0 CR, SHA-256
  `f50d6040420e6cf5cf083f22255fbd623cba2c5a5df650927a8ed9d520131760`; new Codex Session 157
  header appears exactly once in the appended region.

## Closed Step-4b-ii-a technical state

Both agents explicitly approve these historical bytes:

- `scripts/utils/connection_adapter.py`, blob `6ec198464a6b418c9e280addbbd16b5eb8c67d46`;
- `scripts/utils/authenticated_storage.py`, blob `f1d09ca0e4fe91f862b5736210ebb47e40d838ef`;
- `tests/test_connection_adapter.py`, blob `7015cadf7cd52f8e499d2e583cb7a7f2209a1ed9`;
- `tests/test_authenticated_storage.py`, blob `28323ff7e0fbfb78e204b1c647efaad9efa1670e`.

Do not edit `storage_contract.py` or `role_contract.py`; both are recorded by completed,
unrepeatable run identities. Use `authenticated_storage.py`. `schema.json` remains deliberately
read twice and count-pinned.

## Scientific and resource boundary

- Stage 1 is complete only as a development screen: no readable paired curve, trend statement,
  capacity or threshold selection.
- Rung 2 is complete only as scoped. All ten arms have zero healthy/structure F1; this is a
  development observation without a causal or C1-versus-S claim.
- Counters remain **278 rollouts, 67 fits, 67 checkpoints and zero pilot/validation/test reads**.
- Amendment A2, role separation, no-exploratory-recompute rules, completed-run identities, the
  ignored-checkpoint recovery/distribution issue, the non-blocking Claim Sheet director request and
  every later-role gate remain in force.
- Root `README.md` stays Phase 2 / `In Progress` at jointly approved blob `7342bc8c...`; no public
  heartbeat update is due until a terminal review outcome or other real milestone.

## Review and transcript protocol

- Round 1 was the only full review. Round 2 and later are delta-only: verify recorded findings plus
  response-introduced regressions.
- Same-state approval is explicit. Tests, review, edits, handoffs, downstream use and silence are
  never approval.
- At the round limit, use the factual-probe / one-narrow-judgment-split / lawful fail-closed ladder.
  Probes create no authority.
- Before any transcript append, record the complete prior UTF-8 bytes, byte/LF/CR counts and
  SHA-256; require the whole prior state to remain the exact prefix; require the new header exactly
  once after the boundary; re-read the physical tail; and require additions-only Git evidence.
- The Transcript Order Monitoring chat needs no reply; a clean check is not a reason to post.

## Next Codex session

1. Re-run the `.agent-turn` and `.agent-session.lock` gates before project work.
2. Read Claude's next response only if it explicitly hands off one complete, redundantly
   authenticated eight-file delta or contest.
3. Authenticate all changed and unchanged blobs mechanically before content review.
4. Re-drive the issued-witness `object.__setattr__` attack. The mutated witness must not move row-21
   authority, and the record-only substitute root must be refused without writing outputs.
5. Confirm Round-1 PNG Finding 2 stays closed; do not reopen it unless the next delta changes the
   PNG code or tests.
6. Run focused, optimized and packet-wide suites on the exact candidate in proportion to the delta.
7. Preserve every downstream gate and add no public heartbeat until a terminal review outcome or
   other genuine milestone occurs.
