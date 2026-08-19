# Human Report - Codex Session 157

**Current date and time:** 2026-08-19 02:31 PDT (taken from the shell while finalizing this report)

**Agent:** Codex · **Branch:** `main` · **Phase:** 2 (Execution)

---

## Summary

I completed the formal Round-2 delta review of Claude's Slot-8 Step-4b-ii-b candidate. The exact
eight-file state is authenticated: six blobs are bit-identical to Round 1, and the two changed files
match Claude's declared module/test identities. The standard evidence is green, including the
focused adapter/authenticated-storage pair and the whole packet suite both normally and under
`PYTHONOPTIMIZE=1`.

The candidate is nevertheless **not approved**. Round-1 Finding 2 is closed by the PNG repair, but
Round-1 Finding 1 remains open through a response-introduced witness defect: the new issued witness
stores its authority in public slot fields, and `object.__setattr__` can rewrite those fields while
the same witness object remains in the issued-witness table. I reproduced the record-only substitute
root acceptance through that route.

I recorded the blocking Round-2 response in the Review Card, appended the matching handoff to the
active subject chat, updated Codex continuity and preserved every downstream gate. Claude owns the
next complete owner response, limited to the witness-authority repair and directly required tests or
contest.

## Startup and context

The automation gates had already passed in the required order before project work continued:
`.agent-turn` named `Codex`, no `.agent-session.lock` existed, the lock was created exclusively, and
the second turn read still named Codex. I followed `AgentPrompt.md`: read the current project
details, Codex continuity, relevant Codex-participant summaries, both active transcripts, the review
playbook, the reproducibility-packet playbook, Claude's latest report and the full Review Card.

Repository state before review was clean at `e5c0925` (`Claude Session 157`), with `main` equal to
`origin/main`. I made no edit to any candidate source, test, schema, renderer, `.gitattributes` or
scientific file.

## Candidate authentication

The two changed Round-2 artifacts match the declared object identities and physical-byte claims:

```text
Reproducibility Packet/scripts/utils/connection_adapter.py
  Git blob:       a531011027d29a476c802ec540d1b719bbe921a2
  raw SHA-256:    be501eb531d38bf02e07a20d8fb2b0c8275544baf9c3fd8bd74ca4300eee8e79
  physical bytes: 238,496 bytes; 4,962 LF; 0 CR; no BOM; final LF

Reproducibility Packet/tests/test_connection_adapter.py
  Git blob:       894feea7c92b6cb652e7dfbbdd38646690c3ddde
  raw SHA-256:    c523d2a09c4608e86762257ed979ed3755db4582c7e9f929234ce6112f1dff4c
  physical bytes: 392,157 bytes; 9,122 LF; 0 CR; no BOM; final LF
```

The six unchanged artifacts are bit-identical to Round 1:

```text
verification_scene.py              1a614d07d4cb48cf4a40ab7936ddd405c3fb3ac4
test_verification_scene.py         ea7ef4f649f88f2b4b2bf6c1ada8b13c8619295f
render_verification_scene.py       dc82864f4e121f0c94440f5d7ec26bbb021be5af
test_render_verification_scene.py  9dd4119bb5c31b0dfaa71237e2230bb874664e42
.gitattributes                     d6f0fa9a2269afe7b88b34dffd3b1a8702754cf4
Reproducibility Packet/.gitattributes
                                    26e32dff725bc866591ad9f52e05b873ab14f7b6
```

Actual changed-file numstats are `+583/-70` for the adapter module and `+726/-33` for the adapter
tests. The subject chat's `+674/-33` line is a transcript-summary typo; the Review Card and
Claude's HumanReport157 state `+726/-33`, and Git agrees.

## Finding 1R2 - issued witness authority is mutable

Claude's Round-2 repair correctly moved away from comparing the record bytes to another replaceable
field of `AuthenticatedConnection`, but the new authority is still rewritable. `_AuthenticationWitness`
stores `packet_root`, `record_path`, `record_sha256`, `record_label` and `authority` directly in
slots. The class refuses ordinary `setattr` and `delattr`, but public Python can still write slots
with `object.__setattr__`.

The direct probe:

1. Authenticated the ordinary three-case fixture.
2. Copied only the original connection record into a fresh substitute root.
3. Coherently moved every packet-relative bound path and expected-open path to that root.
4. Mutated the already-issued `connection.witness` with `object.__setattr__` for `packet_root` and
   `record_path`.
5. Called `write_bundle` with the bundle derived from the original authenticated state.

Observed result: **accepted**. The substitute root contained the copied record plus all eight
publication outputs. It still lacked the copied schema, config and packet artifacts. The same
witness object remained in `_ISSUED_WITNESSES` by identity, and `_require_one_packet_root` read its
mutated fields back as authority.

The existing witness test checks normal assignment and deletion only, so it misses this public
mutation path. The next repair must ensure row 21 reads immutable issued state rather than
rewritable witness attributes. A private registry keyed by witness identity is one acceptable
shape, but the mechanism is Claude's choice. The attack above must become a committed refusal test.

## Finding 2 - PNG format validation closed

Round-1 Finding 2 is closed. The PNG walk now refuses unknown critical chunks, enforces the relevant
PLTE presence/order/length/count constraints, verifies indexed palette indices after reconstructing
filtered scanlines, and walks the non-interlaced or Adam7 pass layout that the decompressed-length
derivation counts.

The committed tests cover the three reported malformed streams, the widened palette/index/Adam7
cases, positive indexed controls, palette-boundary acceptance and scanline reconstruction. I found
no response-introduced PNG blocker in the Round-2 delta.

Claude's three requested rulings:

1. The four coherence checks below the witness are acceptable as diagnostics once the authority
   state is no longer mutable.
2. The witness mechanism is not itself a W8 protocol amendment; it implements W8's existing one-root
   authority unless the next repair changes the protocol surface.
3. Indexed-image reconstruction is in scope because row 21 claims PNG-format validity, and palette
   index bounds belong to that format.

## Verification

```text
direct witness-mutation probe                  ACCEPTED invalid record-only root (blocking)
targeted Round-2 tests                         53 passed, 336 deselected / 1.45 s
focused pair (adapter + authenticated storage) 409 passed / 31.08 s
focused pair under PYTHONOPTIMIZE=1            409 passed / 31.35 s, expected pytest warning
packet-wide                                    3,068 passed / 180.97 s
packet-wide under PYTHONOPTIMIZE=1             3,068 passed / 183.43 s, expected pytest warning
```

`git diff --check 0983130 e5c0925` was clean before documentation edits. The appended subject-chat
boundary was verified: prior 22,476 bytes at SHA-256
`8d1de0a3ba0b1435f829b2d55758f2d858a2daa083b0f75aff055891c580d84e` remain the exact prefix,
post-write size is 25,607 bytes with 394 LF, 0 CR and SHA-256
`f50d6040420e6cf5cf083f22255fbd623cba2c5a5df650927a8ed9d520131760`, and the new Codex Session 157
header occurs exactly once in the appended region.

## Scientific and gate boundary

No scientific resource was spent. No MuJoCo model was built, no rollout stepped, no fit run, no
checkpoint written, no figure rendered, no production connection record read and no real
role/index/payload/checkpoint/result was opened. Counters remain **278 rollouts, 67 fits, 67
checkpoints and zero pilot / validation / test reads**.

Step 4b-ii-b remains open. Full Step 4b, production connection records, real role/index/payload
reads, later-role reads, adapter execution, capacity or threshold choice, final configuration and
every C1-versus-S claim remain unauthorized. The public README heartbeat remains unchanged; no
terminal technical milestone occurred.
