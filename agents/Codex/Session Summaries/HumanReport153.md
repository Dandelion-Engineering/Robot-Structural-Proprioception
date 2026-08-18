# Human Report — Codex Session 153

**Current date and time:** 2026-08-17 21:16 PDT (taken from the shell during final creation of this report)

**Agent:** Codex · **Branch:** `main` · **Phase:** 2 (Execution)

---

## Summary

I completed the general recent-work review of Claude Session 153's still-partial Slot-8
Step-4b-ii-b build. This was not a formal Review Card round: Claude has not declared a stable
candidate, created the card or subject chat, or handed the build off.

Claude correctly discharged both findings from my Session-152 review. The row-19 seam now runs
the production config validator over a complete validator-accepted synthetic frozen document,
and all three test installers restore the connection record they rewrite inside their own cleanup.
Row 21 is also materially built: the adapter exclusively creates the publication root and checks
the declared file set, canonical bundle and scene bytes, bundle digest, reported identities and
figure resolution.

Two new forward blockers remain before stable handoff:

1. `write_bundle` accepts the row-20 bundle from one genuinely authenticated connection while
   publishing it under a second genuinely authenticated connection. It never binds the bundle's
   record label, record digest, config identities, split and arm identities back to the
   `AuthenticatedConnection` that supplies the output root. Its stated destination post-condition
   is also only a basename check: a substituted root under the wrong parent is accepted when the
   child still equals `record_label`.
2. `_png_pixels_per_metre` does not validate the PNG chunk it treats as resolution evidence. A
   figure whose `pHYs` CRC was corrupted was accepted as 300 DPI, while a length-9 `pHYs` chunk
   with a one-byte body escaped as a raw `IndexError` rather than the row's named fail-closed
   refusal.

The exact current state passes 299 focused tests, 299 under optimized Python and all 2,957 packet
tests. Those suites show no ordinary regression; independent probes demonstrate the two missing
boundaries above.

No scientific resource was spent, and Codex changed no packet implementation or test byte.

## Startup and context ingestion

- Read `.agent-turn` first as the automation required; it named Codex. The lock was absent, so I
  created `.agent-session.lock`; the second turn read still named Codex.
- Read `AgentPrompt.md`, the automation continuity, all of `Project Details/Project Details.md`,
  Codex continuity, every Codex-participant chat summary, and the only active Codex-participant
  transcript.
- The only active chat is `Transcript Order Monitoring`; no response was required. A clean check
  is not a reason to post there.
- Read Claude's `HumanReport153.md`, current continuity, build-plan Appendix G, the exact code/test
  delta, the governing Step-4a design sections, and the changed production/test implementations.
- Authenticated the owner state at commit
  `86ef6d204b96cd53faa5eef9f551ca0ec218eeab` (`Claude Session 153`). The tracked worktree was
  clean at review start.

## Exact owner state reviewed

- `Reproducibility Packet/scripts/utils/connection_adapter.py`
  - Git blob `db176408be9a9f449f75cd7ab2a0b72e7352e413`
  - raw SHA-256 `80a2bd1ad56b66f3bbeb8e430fbe0db03684c441ab58ac497c654fd8632323b7`
  - 172,465 bytes / 3,689 LF / 0 CR
- `Reproducibility Packet/tests/test_connection_adapter.py`
  - Git blob `31836c51d254d915111f39e0aae68023d91c7905`
  - raw SHA-256 `1262c1164af1dc23fa2ab8d31c22b72fc62bd0b46cc473c886ac20261b20ae6d`
  - 281,654 bytes / 6,774 LF / 0 CR

Both files have no BOM and end in LF. No exact state is approved; the candidate remains unfinished
and owner-held.

## What Claude repaired correctly

### The row-19 witness now crosses the production config validator

`_require_post_row12_state` now calls `validate_config_document` at the authority-appropriate
`require_frozen` setting before it checks the row-4 and row-3 policies. `_reprovenanced` uses the
existing complete synthetic frozen document with a `config.json` source path, updates the record's
relative path, and adds the nineteenth join between that source path and the record. It does not
write a `config.json` or invent a raw-byte digest for a file no read produced. The third negative
control isolates the previous generation's defect: all joins hold and policy accepts, leaving the
validator as the only refusing check. This discharges Session-152 finding 1.

### Each installer now restores its own record

`_coherent_geometry`, `_rewritten_payload` and `_three_case_menu` save the connection-record bytes
and restore them in `finally`. The complete-tree restoration test no longer excludes the record or
repairs it manually, and a second test re-authenticates after all three installers exit. This
discharges Session-152 finding 2.

## Finding 1 — row 21 does not bind the bundle to the connection that publishes it

`write_bundle(connection, bundle, render=...)` receives two separately constructible values. It
uses `connection` for the output root, expected cases and reported authority, but it does not
compare the bundle's scene provenance back to that connection's record label, record digest,
config identity/raw digest, split or arm identities.

I built two real authenticated records over one fresh temporary harness. Both named the same
three-case menu and `DEVELOPMENT_ONLY` authority, but they had distinct labels and raw digests:

```text
connection B label: adapter-fixture-b
connection B sha256: af93cceab0196ec4d8cf6d7a2fa0a10660ffa83dd6af46451c878ea00d645647
bundle A scene label: adapter-fixture
bundle A scene sha256: 56a6d1b19548defcb5bcf1698166b809352de03418f2e1282db2f233d36d64b4
```

I resolved rows 13–20 under connection A, then passed the resulting bundle with authenticated
connection B to row 21. `write_bundle` returned successfully and published under
`.../verification_connection_development/adapter-fixture-b/`, while every scene still identified
connection A. This is the same separately supplied intermediate-value seam row 20 correctly guards
for provenance, now one row later.

The destination post-condition is incomplete too. The docstring says row 21 refuses a root that is
not the named child of the authority's parent, but the implementation checks only
`output_root.name == record_label`. Replacing `bound.output_root` with
`<temporary-root>/wrong-parent/adapter-fixture` was accepted and populated. The existing negative
test changes the basename and therefore cannot see a correct basename under the wrong parent.

Before creating anything, row 21 should bind the complete bundle provenance and destination back
to the exact authenticated connection. A direct negative control should use two independently
authenticated connections with the same authority/menu, and the destination control should keep
the basename correct while moving the parent.

## Finding 2 — corrupted or truncated `pHYs` evidence is not fail-closed

`_png_pixels_per_metre` walks chunk lengths but does not verify that the declared body and CRC are
present, does not verify the chunk CRC, and returns as soon as it sees the first `pHYs` tag.

Two direct probes reproduce the consequences:

```text
corrupted pHYs CRC: accepted and published as (11811, 11811) pixels/metre
length=9, one-byte pHYs body: IndexError("index out of range"), no refusal code
```

The first file is not valid 300-DPI PNG evidence: the integrity check for the ancillary resolution
chunk is wrong, so a decoder may discard it. The second leaves the adapter's named refusal surface
entirely. Row 21 should strictly bound each chunk before indexing, verify the relevant CRC (or use a
strict PNG decoder), reject malformed/duplicate resolution state, and drive both the corrupt-CRC
and truncated-body cases to `X_BUNDLE_INCOMPLETE`.

## Verification

Executed only with the required project interpreter:

```text
.\venv\Scripts\python.exe -m pytest -q
  Reproducibility Packet/tests/test_connection_adapter.py
  Reproducibility Packet/tests/test_authenticated_storage.py
  -> 299 passed in 13.92 s

PYTHONOPTIMIZE=1 .\venv\Scripts\python.exe -m pytest -q
  Reproducibility Packet/tests/test_connection_adapter.py
  Reproducibility Packet/tests/test_authenticated_storage.py
  -> 299 passed, 1 expected PytestConfigWarning, in 13.77 s

.\venv\Scripts\python.exe -m pytest -q Reproducibility Packet/tests
  -> 2,957 passed in 162.77 s
```

All adversarial probes used fresh temporary harnesses outside the repository. They opened no
delivered role root and spent no scientific resource. Targeted `py_compile` passed, and
`git diff --check` was clean before the Codex closeout edits.

## Scientific and authorization boundary

- No MuJoCo model was built, no rollout stepped, no fit or checkpoint created, and no real-data
  figure rendered. No production connection record, delivered role payload or later-role result
  was opened.
- Counters remain **278 rollouts, 67 fits, 67 checkpoints and zero pilot/validation/test reads**.
- Slot-8 Steps 1–3, Step 4a, Step 4b-i and Step 4b-ii-a remain closed / both approved at their
  recorded historical bytes.
- Step 4b-ii-b remains Claude-owned, incomplete and unapproved. The read-order rows now exist, but
  the two findings above, audit-hook observer, remaining B2/B3/B5 coverage, CLI wiring, additive
  `build_role_bundle` change and mutation sweep remain before stable handoff.
- Full Step 4b, production records, real-role reads, Steps 4c–4f, capacity or threshold choice,
  final configuration and every C1-versus-S statement remain blocked.

## Live-Run README heartbeat

Checked and left unchanged. Completing an internal read-order row in an unreviewed build and
finding forward blockers are not an artifact closure, phase transition or scientific result. The
public root README remains at jointly approved blob
`7342bc8ca5a256a411d69577199cc0c2e3dbc2d0`.

## Files created or updated by Codex

- `agents/Codex/Session Summaries/HumanReport153.md` — this detailed session record.
- `agents/Codex/README.md` — indexed Session 153 and refreshed the active gate map.
- `agents/Codex/Summary of Only Necessary Context.md` — completely rewritten for Session 154.

No packet code, packet test, Review Card, chat transcript, protocol, Claim Sheet, configuration,
result artifact or public README byte was changed.

## Next steps

1. Claude should bind the complete row-20 bundle provenance and exact authority-scoped output
   parent back to the authenticated connection before row 21 creates anything.
2. Claude should make PNG resolution parsing structurally total and integrity-checked, with
   corrupt-CRC and truncated-chunk controls producing the named refusal.
3. Claude can then continue its owned observer, B2/B3/B5 coverage, roles CLI wiring, additive
   `build_role_bundle` edit and two-pass mutation sweep.
4. Only after a complete stable candidate, Review Card, subject chat and explicit handoff should
   Codex perform formal Round 1.
