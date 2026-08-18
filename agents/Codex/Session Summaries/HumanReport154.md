# Human Report — Codex Session 154

**Current date and time:** 2026-08-18 12:23 PDT (taken from the shell during final creation of this report)

**Agent:** Codex · **Branch:** `main` · **Phase:** 2 (Execution)

---

## Summary

I completed the general recent-work review of Claude Session 154's still-partial Slot-8
Step-4b-ii-b build. This was not a formal Review Card round: Claude has not declared a stable
candidate, created the card or subject chat, or handed the build off.

Claude correctly discharged the exact two cases from my Session-153 review. Row 21 now rejects a
bundle assembled under a second authenticated connection and rejects a correct record-label child
under the wrong authority parent. The PNG walk now bounds chunks before indexing, verifies CRCs,
rejects duplicate resolution chunks and refuses the two reported corrupt/truncated inputs through
the named surface. Claude also built the audit-hook observer required by W3/B4; it measures the
interpreter's complete open set without filtering and pins `schema.json` as the sole second read.

Three adjacent forward blockers remain before stable handoff:

1. Row 21 binds only the bundle's menu/version/state and scene provenance to the connection, not
   the rest of the separately supplied bundle. Replacing every scene's authenticated
   `abstain_threshold` from `0.55` to `0.56` produced a still-valid bundle and published
   successfully. The public artifact can therefore carry display/audit facts that the record did
   not authenticate while retaining the correct provenance block.
2. `_authority_output_root` derives the destination from `connection.bound.packet_root`, but that
   root is part of the same replaceable `BoundPaths` value as `output_root`. Replacing both fields
   coherently published beneath an unrelated temporary packet root. The new check catches a moved
   parent only when the old packet root is retained; it does not yet preserve W8 against a coherent
   root/destination substitution.
3. `_png_pixels_per_metre` verifies CRCs and termination but does not establish the mandatory PNG
   structure. A CRC-valid byte string containing only the PNG signature, one `pHYs` chunk and
   `IEND` was accepted as `(11811, 11811)` even though it has no `IHDR` or image data and Pillow
   refuses it as `UnidentifiedImageError`. A resolution chunk inside a non-image is not evidence
   of a 300-DPI figure.

The exact current state passes 329 focused tests, 329 under optimized Python and all 2,987 packet
tests. Those suites show no ordinary regression; fresh probes demonstrate the three uncovered
boundaries above.

No scientific resource was spent, and Codex changed no packet implementation or test byte.

## Startup and context ingestion

- Read the automation continuity and `.agent-turn`; the turn named Codex. The lock was absent, so
  I created `.agent-session.lock`; the second turn read still named Codex.
- Read `AgentPrompt.md`, all of `Project Details/Project Details.md`, Codex continuity, every
  Codex-participant chat summary, and the only active Codex-participant transcript.
- The only active chat is `Transcript Order Monitoring`; no response was required. A clean check
  is not a reason to post there.
- Read Claude's `HumanReport154.md`, current continuity, the changed code/test state, the governing
  Step-4a design sections and the Session-154 build-plan append.
- Authenticated the owner state at commit
  `123a38a06d23825b605d625b68d67c2a7322118a` (`Claude Session 154`). The tracked worktree was
  clean at review start.

## Exact owner state reviewed

- `Reproducibility Packet/scripts/utils/connection_adapter.py`
  - Git blob `3baa01781b03d71ace9f9b99eb69f676c16ca4ed`
  - raw SHA-256 `438b3059cb6de99069dfe4f9828f9ef1cd00b9fd22a4412ab3e0b03851ef99fa`
  - 182,777 bytes / 3,886 LF / 0 CR
- `Reproducibility Packet/tests/test_connection_adapter.py`
  - Git blob `fd841d520a5a9cf4301f23e2609b0a1c7c67e046`
  - raw SHA-256 `ba08534123f3adeea0df31f38449c9c8714adfb26488f64196136690d5f75ca5`
  - 307,187 bytes / 7,334 LF / 0 CR

No exact state is approved; the candidate remains unfinished and owner-held.

## What Claude repaired correctly

### The reported cross-connection and wrong-parent cases now refuse

`_provenance_for` is now the single assembler/comparand for the scene provenance block. Row 21
checks every current `Provenance` dataclass field, the record-ordered menu, bundle version and
bundle authority before it creates the output root. The test substitution ledger is itself pinned
to the complete dataclass field set. This closes the exact two-authenticated-connection case I
reported in Session 153.

`_authority_output_root` also replaces the former basename-only guard. With the authenticated
packet root held fixed, a correct record-label child beneath a wrong parent is refused before any
directory exists. This closes the exact wrong-parent case I reported.

### The reported PNG corrupt/truncated cases now refuse

The parser bounds each chunk before reading its body, verifies CRC-32 over the chunk type and body,
requires exactly one `pHYs`, requires metre units, rejects trailing bytes after `IEND`, and returns
only after walking the datastream. The corrupt-CRC and one-byte-body cases from Session 153 both
reach `X_BUNDLE_INCOMPLETE` rather than acceptance or a raw exception. The tracked ten-figure set
also passes the stricter walk.

### The audit-hook observer is materially built

The W3/B4 tests install one inert-unless-recording `sys.addaudithook` callback, prove it observes
both builtin `open` and `os.open`, and compare the actual authentication-chain open set to the
record-derived allowlist in both directions with no filtered observed paths. A separate count test
pins `schema/schema.json` as the only path opened twice, and the row-21 observer requires every
writer/readback open to remain inside the created publication tree. I found no forward defect in
this observer work.

## Finding 1 — the separately supplied bundle is only provenance-bound

The new row-21 preflight correctly binds every field of `scene.provenance`, but a
`VerificationBundle` carries substantially more than provenance: thresholds, body-change facts,
playback grids, decisions, controller series, tracking arrays and centerlines. All of these arrive
through the same separately constructible `bundle` argument.

I resolved rows 13–20 normally in a fresh temporary three-case harness, then replaced the
`abstain_threshold` on every scene from the authenticated record's `0.55` to `0.56`. Altering all
three scenes keeps `validate_bundle`'s cross-scene agreement true, and the provenance blocks remain
byte-for-byte authentic. Row 21 accepted the altered bundle, rendered it and returned success:

```text
authenticated abstain_threshold  0.55
published abstain_threshold      0.56
result                           ACCEPTED
```

This is the same seam as the Session-153 cross-connection finding at a deeper width. Binding the
complete provenance block proves what sources the picture claims, but it does not prove the
picture's non-provenance content came from those sources. At minimum every record-derived display
fact must be compared back to the connection; the remaining B3 work should drive each row-13–20
output substitution so the final repair is complete rather than threshold-specific.

## Finding 2 — packet root and destination can move together

`_authority_output_root` recomputes the expected destination from three inputs:
`connection.bound.packet_root`, the record authority and the record label. This catches a changed
`output_root` while the packet root stays fixed. It does not catch a coherent replacement of both
path fields, because the expected value moves with the substituted root.

In a fresh authenticated harness I replaced only these two `BoundPaths` fields:

```text
packet_root  -> <temporary>/other-packet
output_root  -> <temporary>/other-packet/results/verification_connection_development/adapter-fixture
```

All authenticated record/config/source/dataset/role values remained those from the original
packet tree. `write_bundle` accepted the replacement and populated the unrelated root. This
contradicts W8's single-root property at the same post-authentication seam the new destination
guard is intended to defend.

Row 21 needs an independent packet-root anchor from the authenticated path set, rather than
deriving the complete destination from two fields of the same substitutable `BoundPaths` value.
The negative control should move packet root and output root together while leaving the previously
authenticated record/config/source paths intact.

## Finding 3 — CRC-valid non-images still count as PNG evidence

The new PNG walk establishes chunk bounds, CRC integrity, exactly one resolution declaration and
an `IEND` terminator. It does not establish the mandatory image structure. I constructed a byte
string from validly CRC'd chunks:

```text
PNG signature
pHYs(11811, 11811, metres)
IEND
```

There is no `IHDR`, no `IDAT` and therefore no image. `_png_pixels_per_metre` returned
`(11811, 11811)`. Pillow's `Image.open(...).verify()` refused the same bytes as
`UnidentifiedImageError`.

The row's claim is not merely that a byte stream contains a resolution chunk; it is that a case
figure is a PNG saved at 300 DPI. The parser must at least enforce the mandatory PNG datastream
structure relevant to that claim—`IHDR` first with its fixed length, valid image data ordering,
zero-length `IEND` last, and the permitted position of `pHYs`—or delegate validation to a strict
decoder while retaining the exact resolution check. A missing-IHDR case should reach
`X_BUNDLE_INCOMPLETE`.

## Verification

Executed only with the required project interpreter:

```text
.\venv\Scripts\python.exe -m pytest -q
  Reproducibility Packet/tests/test_connection_adapter.py
  Reproducibility Packet/tests/test_authenticated_storage.py
  -> 329 passed in 17.83 s

PYTHONOPTIMIZE=1 .\venv\Scripts\python.exe -m pytest -q
  Reproducibility Packet/tests/test_connection_adapter.py
  Reproducibility Packet/tests/test_authenticated_storage.py
  -> 329 passed, 1 expected PytestConfigWarning, in 16.72 s

.\venv\Scripts\python.exe -m pytest -q Reproducibility Packet/tests
  -> 2,987 passed in 164.88 s
```

All three adversarial probes used fresh temporary harnesses outside the repository and were
deleted. They opened no delivered role root and spent no scientific resource. `git diff --check`
was clean before the Codex closeout edits.

## Scientific and authorization boundary

- No MuJoCo model was built, no rollout stepped, no fit or checkpoint created, and no real-data
  figure rendered. No production connection record, delivered role payload or later-role result
  was opened.
- Counters remain **278 rollouts, 67 fits, 67 checkpoints and zero pilot/validation/test reads**.
- Slot-8 Steps 1–3, Step 4a, Step 4b-i and Step 4b-ii-a remain closed / both approved at their
  recorded historical bytes.
- Step 4b-ii-b remains Claude-owned, incomplete and unapproved. The exact Session-153 cases and
  W3/B4 observer are discharged, but the three findings above, B2/B5, remaining B3 rows, CLI
  wiring, additive `build_role_bundle` change and mutation sweep remain before stable handoff.
- Full Step 4b, production records, real-role reads, Steps 4c–4f, capacity or threshold choice,
  final configuration and every C1-versus-S statement remain blocked.

## Live-Run README heartbeat

Checked and left unchanged. Repairing internal findings, adding an observer and finding new
forward blockers in an unreviewed build are not an artifact closure, phase transition or
scientific result. The public root README remains at jointly approved blob
`7342bc8ca5a256a411d69577199cc0c2e3dbc2d0`.

## Files created or updated by Codex

- `agents/Codex/Session Summaries/HumanReport154.md` — this detailed session record.
- `agents/Codex/README.md` — indexed Session 154 and refreshed the active gate map.
- `agents/Codex/Summary of Only Necessary Context.md` — completely rewritten for Session 155.

No packet code, packet test, Review Card, chat transcript, protocol, Claim Sheet, configuration,
result artifact or public README byte was changed.

## Next steps

1. Claude should bind the complete row-20 bundle content, not only its provenance, back to the
   authenticated row-13–20 facts; the all-scenes threshold substitution is the minimal control.
2. Claude should bind row 21's packet root independently of the replaceable destination so a
   coherent packet-root/output-root move refuses.
3. Claude should require mandatory PNG image structure in addition to chunk integrity, starting
   with the CRC-valid missing-`IHDR` control.
4. Claude can then continue B2/B5, remaining B3 coverage, roles CLI wiring, the additive
   `build_role_bundle` edit and the two-pass mutation sweep.
5. Only after a complete stable candidate, Review Card, subject chat and explicit handoff should
   Codex perform formal Round 1.
