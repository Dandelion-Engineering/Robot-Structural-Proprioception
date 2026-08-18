# Human Report — Codex Session 155

**Current date and time:** 2026-08-18 14:16 PDT (taken from the shell while writing this report)

**Agent:** Codex · **Branch:** `main` · **Phase:** 2 (Execution)

---

## Summary

I completed the required general recent-work review of Claude Session 155 at commit
`3bd7423cc61de484c3c7c53f6b99b8cc4bd356af`. This is still a partial, Claude-owned
Step-4b-ii-b build: no stable candidate, Review Card, subject chat or formal handoff exists, so
this was not an artifact review and I changed no packet implementation or test byte.

Claude correctly discharged the complete-bundle-content finding from Session 154. Row 21 now
re-derives rows 13–20 from the authenticated connection and compares each complete canonical
scene, and the new coverage test binds that comparison to every `VerificationScene` field. The
new B2 accept-side composition test, B3 refusal floor and B5 byte-for-byte determinism test are
also sensible additions. I independently reproduced all declared green counts: **356 focused,
356 under optimized Python and 3,014 packet-wide**.

Two definite forward blockers remain outside that green suite:

1. `_require_one_packet_root` still anchors one replaceable `BoundPaths` field to other fields
   of the same replaceable value. Replacing the packet root, output root, record path, schema
   path, config path and every packet-artifact path coherently allowed all eight files to publish
   beneath an unrelated tree even though none of those substituted input paths existed and
   `AuthenticatedConnection.expected_opens` still named the original authenticated tree.
2. `_png_pixels_per_metre` now checks chunk order but still accepts byte streams that are not
   decodable PNG images. A zero-width `IHDR` and a CRC-valid but non-zlib `IDAT` each returned
   `(11811, 11811)`; Pillow refused the first as `UnidentifiedImageError` and the second as a
   broken data stream.

No scientific resource was spent. Counters remain 278 rollouts, 67 fits, 67 checkpoints and
zero pilot/validation/test reads. All production, configuration and downstream gates remain
closed.

## Exact owner state reviewed

Claude Session 155 is commit `3bd7423cc61de484c3c7c53f6b99b8cc4bd356af`, equal to
`origin/main` when reviewed.

- `Reproducibility Packet/scripts/utils/connection_adapter.py`
  - Git blob `2e7d9fa02786723cfaf068ca5018860e3c46dfaf`
  - raw SHA-256 `261b6548294272e4f5698e638fc8188fb577d03da6097c61f649d449a0d1660b`
- `Reproducibility Packet/tests/test_connection_adapter.py`
  - Git blob `a783fa6ceb47dd91ef1b70229d5ec986b0a0c0a4`
  - raw SHA-256 `1dfa35a4b4df7a1af39339c9635a569a0383e2aaf6f0fabf8b528f341646ce36`

The session delta from Codex Session 154 is `+218/-7` in the module and `+680/-1` in the
test file. `git diff --check` passed. The root public README remains at jointly approved blob
`7342bc8ca5a256a411d69577199cc0c2e3dbc2d0`.

## What Claude Session 155 repaired correctly

### Complete bundle content is now bound

The prior row-21 check authenticated every provenance field but did not bind the scene content
the provenance described. The new implementation re-runs the pure rows 13–20 from the already
authenticated in-memory payloads and compares the canonical rendering of every presented scene
to the newly derived scene.

The eleven substitution families are a useful width check: both thresholds, display label,
playback grid, centerline, tracking reference/output/window, controller clock/mode and decision
content. Their anchor proves each altered bundle still crosses the pre-existing bundle and
provenance checks. The audit-hook test also confirms the new re-derivation adds no input read.
I found no forward defect in this repair.

### B2, B3 and B5 are materially present

- B2 drives one coherent rows-1–21 composition and asserts the output each applicable row
  establishes rather than relying only on refusal tests.
- B3 turns the minimum one-refusal-per-row requirement for rows 13–21 into a committed floor.
  Its documented under-counting direction is appropriate for a floor.
- B5 runs the real scripted writer twice from fresh publication roots and compares all eight
  files and the bundle digest byte for byte.

These close the named internal test-plan items, but they do not make the unfinished adapter a
stable candidate or approve it.

## Forward blocker 1 — the packet-root anchor still moves coherently

The new helper begins at
`Reproducibility Packet/scripts/utils/connection_adapter.py:3642`. Its stated lesson is that an
anchor cannot be a field of the value under suspicion, but it uses `bound.record_path` as the
anchor while `record_path`, `packet_root`, `output_root`, `schema_path`, `config_path` and
`packet_artifacts` are all fields of that same separately constructible `BoundPaths` value.

I re-drove the completed three-case harness and replaced every packet-relative `BoundPaths`
field coherently:

```text
packet_root      -> <tmp>/other-packet
output_root      -> <tmp>/other-packet/results/verification_connection_development/adapter-fixture
record_path      -> <tmp>/other-packet/results/verification_connection/records/adapter-fixture/connection_record.json
schema/config/source paths -> same record-relative locations under <tmp>/other-packet
expected_opens   -> unchanged; still names the original authenticated tree
substituted input paths before write -> do not exist
outcome          -> ACCEPTED; all eight files published beneath <tmp>/other-packet
```

The helper proves only that the current `BoundPaths` fields agree with one another. It does not
prove they are the paths rows 1–5 authenticated. The repair needs an identity outside the
replaceable path bundle—one already carried from authentication—or an equivalent comparison
between the current bound-derived set and the authenticated path identity. The new control must
move the entire packet-relative bound set together, leave the authenticated evidence unchanged,
and require refusal before the publication root is created. A genuine invocation run against a
copied packet remains a distinct allowed case; substituting the paths after authentication is
not that invocation.

## Forward blocker 2 — valid chunk order is not a valid PNG image

The stricter walk begins at
`Reproducibility Packet/scripts/utils/connection_adapter.py:3448`. It now requires `IHDR`
first at length 13, one consecutive `IDAT` run, `pHYs` before image data and an empty terminal
`IEND`. That closes the exact signature-plus-`pHYs`-plus-`IEND`, no-`IDAT` and late-`pHYs`
cases.

It still validates neither the `IHDR` fields nor the `IDAT` stream. Two independent byte streams
with correct chunk bounds and CRCs crossed the helper:

```text
IHDR width = 0, otherwise ordered chunks       -> ACCEPTED (11811, 11811)
IDAT body = b"not-a-zlib-stream"               -> ACCEPTED (11811, 11811)
strict decoder on zero-width stream             -> UnidentifiedImageError
strict decoder on invalid-IDAT stream            -> OSError: broken data stream
```

A zero-width header is forbidden by the PNG format, and a non-decodable IDAT payload is not image
data. Therefore the helper still proves only the presence and order of named chunks, not its own
claim that the published file is a PNG figure saved at 300 DPI. The forward repair should either
validate the relevant `IHDR` semantics and the complete compressed image stream or use a strict
decoder already declared by the packet. At minimum, the zero-dimension and invalid-compressed-
stream controls should refuse as `X_BUNDLE_INCOMPLETE`, while the ten tracked Step-3 figures
remain the accept side.

## Verification

Every Python command used the required project interpreter.

```text
.\venv\Scripts\python.exe -m pytest -q \
  Reproducibility Packet/tests/test_connection_adapter.py \
  Reproducibility Packet/tests/test_authenticated_storage.py
356 passed in 20.53 s

PYTHONOPTIMIZE=1, same focused pair
356 passed in 20.48 s

.\venv\Scripts\python.exe -m pytest -q Reproducibility Packet/tests
3,014 passed in 161.03 s
```

The two probes ran from standard input outside the repository, created only temporary trees and
left no project artifact. Their acceptance is why the green suite does not settle the two new
boundaries.

## Chats and public heartbeat

I read all eleven Codex-participant chat summaries and the complete active Transcript Order
Monitoring transcript before replying anywhere. Its physical tail is Claude Session 144's
independent confirmation; no response is owed, and a clean check is not a reason to append.

There is still no Step-4b-ii-b Review Card or subject chat. I did not create either. The public
README heartbeat was checked and left unchanged because a general review of an incomplete build
is not an artifact closure, phase transition or scientific result.

## Scientific and authorization boundary

- No MuJoCo model was built, no rollout stepped, no fit run and no checkpoint written.
- No production connection record, role index, role payload, checkpoint, estimator output,
  controller log or later-role scientific artifact was opened.
- The only figure bytes read were the tracked synthetic Step-3 fixtures exercised by the packet
  tests; the independent malformed-PNG inputs were created in memory.
- Full Step 4b, production records, real-role reads, Steps 4c–4f, capacity or threshold choice,
  final configuration, adapter execution and every C1-versus-S claim remain unauthorized.
- Step 4b-ii-b remains wholly unreviewed and Claude-owned.

## Files created or updated

- `agents/Codex/Session Summaries/HumanReport155.md` — this report.
- `agents/Codex/README.md` — Session-155 index and current Step-4b-ii-b review boundary.
- `agents/Codex/Summary of Only Necessary Context.md` — completely rewritten for Session 156.

No packet code/test, Review Card, chat transcript, protocol document, Claim Sheet, configuration,
result artifact or public README byte was changed.

## Next steps

1. Claude should re-drive both probes before editing and repair the full coherent-root
   substitution and invalid-image acceptance at their claim boundaries.
2. Claude should then finish the already-planned roles CLI wiring and additive
   `build_role_bundle` change.
3. The two-pass mutation sweep should remain after the implementation pair is finished.
4. Only then should Claude create the Review Card and narrow subject chat, authenticate the
   complete candidate and hand it off with explicit owner approval.
5. Codex should not perform formal review or approve any Step-4b-ii-b state before that handoff.
