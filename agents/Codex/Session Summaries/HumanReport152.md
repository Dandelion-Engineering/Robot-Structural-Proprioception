# Human Report — Codex Session 152

**Current date and time:** 2026-08-17 19:13 PDT (taken from the shell immediately before creating this report)

**Agent:** Codex · **Branch:** `main` · **Phase:** 2 (Execution)

---

## Summary

I completed the general recent-work review of Claude Session 152's still-partial Slot-8
Step-4b-ii-b build. This was not a formal Review Card round: Claude has not declared a stable
candidate, created a card or subject chat, or handed the build off.

Claude correctly repaired the production row-20 provenance defect from my previous review.
`resolve_bundle` now requires the separately supplied provenance state to equal the authenticated
record's authority before it builds any scene, and direct tests drive forged `FINAL` and
`SYNTHETIC_FIXTURE` values to `X_PROVENANCE_UNRESOLVED`. Claude also expanded the row-19 test
seam from eleven to eighteen identity joins and added direct row-3 and row-4 policy calls.

Two test-evidence blockers remain before stable handoff:

1. The helper now named `_require_post_row12_state` still accepts a `FINAL` configuration state
   that the production row-4 validator refuses. It changes only the draft document's `status` and
   semantic hash; it retains the draft filename, draft decision, false confirmatory flag, open
   gates and unresolved model/calibration/evaluation values. Therefore the helper's claim that it
   returns a state rows 3–12 could have produced is still false.
2. `_three_case_menu` says it restores every byte it writes when its context exits, but it leaves
   the rewritten connection record behind while restoring the source, audit, manifest and index
   files that record names. The result is an incoherent harness state. The test named for complete
   restoration excludes the record from its snapshot and then restores it manually, so it does not
   prove the context manager's stated property.

The exact current state still passes 277 focused tests, 277 under optimized Python and all 2,935
packet tests. Those green suites establish that Claude introduced no ordinary regression; they do
not discharge either missing witness above.

This is also my regular eighth-session cadence report (Session 152 = 19 × 8), so I wrote
`agents/Codex/Progress Reports/Progress Report Session 152.md` covering Sessions 145–152.

No scientific resource was spent. No packet production or test byte was changed by Codex.

## Startup and context ingestion

- The automation memory was read first. `.agent-turn` then named Codex, the lock was absent, and I
  created `.agent-session.lock`. The second turn read still named Codex.
- Read `AgentPrompt.md`, all of `Project Details/Project Details.md`, Codex continuity, every
  Codex-participant chat summary, and the only active Codex-participant transcript.
- The only active chat is `Transcript Order Monitoring`; its tail requires no response. A clean
  append-order check is not a reason to post.
- Read Claude's `HumanReport152.md`, current continuity, build-plan Appendix F, the exact code/test
  delta, the governing Step-4a design sections and the current production/test implementations.
- Read the research-progress-report and Live-Run README playbooks before closeout.
- Authenticated the owner state at commit
  `8fecaf74c0c2092ccfb377a8d5f685d67dfd7610` (`Claude Session 152`). The tracked worktree was
  clean at review start.

## Exact owner state reviewed

- `Reproducibility Packet/scripts/utils/connection_adapter.py`
  - Git blob `a1236ed937e5deeca8b6aa86cd43f16269ef6139`
  - raw SHA-256 `007b870ee57143a9d1af9a890b54240cd3387ad5053ad5c08445b18630eeeac0`
  - 157,693 bytes / 3,347 LF / 0 CR
- `Reproducibility Packet/tests/test_connection_adapter.py`
  - Git blob `6f6a2b135080764e5eb40bcc89159ca3e8eaadb7`
  - raw SHA-256 `db00779e818fe0e6fc08cbbcb50ec237f237da7b40d3fc9fb79796d500dd6fcd`
  - 247,241 bytes / 5,969 LF / 0 CR

No exact state is approved. The candidate remains unfinished and owner-held.

## What Claude repaired correctly

### Row 20 now binds the visible provenance banner

The new production guard executes before `_scene_for` and compares
`provenance.state` to `connection.record.authority`. That is the correct boundary: row 19 checks
its own computation, while row 20 checks that a separately supplied intermediate was not
substituted before assembly. The two forged values now refuse before any scene exists. I found no
production defect in this change.

### The row-19 identity ledger is materially stronger

The seam now moves and checks the stored/recomputed census, both audit census blocks, the
record-side manifest echoes, role-index config hashes and the config document's own semantic
identity. The two historical partial repairs are preserved as separate negative controls. This
discharges the specific seven missing identity relations from Session 151.

## Finding 1 — the “post-row-12” seam still bypasses the production config validator

`_require_post_row12_state` says it returns a state rows 3 through 12 would have produced. It calls
the authority/config policy, but that policy accepts an already validated `ValidatedConfig`; it
does not replace row 4's full `validate_config_document` call.

The exact Session-152 `_reprovenanced` helper was run against a fresh temporary harness with
`authority=FINAL`, `split=val`, `config_status=frozen` and a non-development assignment hash. The
helper returned successfully. The resulting config reported:

```text
source_path = .../packet/config/draft-config-v0.1.json
status = frozen
decision = BLOCK_CONFIG_FREEZE_PENDING_PRECONFIRMATORY_BUILD_AND_VALIDATION
confirmatory_payloads_allowed = False
values.models = None
```

Passing that exact document and its retained source path to the production validator with
`require_frozen=True` produced:

```text
ConfigContractError: the frozen configuration must be named exactly config.json
```

Correcting only the filename would not make the document valid: it also retains the draft
decision, false confirmatory flag, nonempty open gates, and null freeze-required model,
calibration and evaluation fields. The test file already contains `_synthetic_frozen_document`,
which builds a complete validator-accepted frozen fixture under a temporary `config.json` for B8;
so this is not blocked by an unavailable test mechanism.

The row-19 seam may either use a genuinely validator-accepted synthetic frozen configuration, or
it must narrow its name, docstring and evidence claim so it no longer represents itself as a
complete post-row-12 state. As written, the Session-151 coherence blocker is only partially
discharged.

## Finding 2 — `_three_case_menu` does not restore the record it rewrites

The new context manager saves and restores the manifest, validation/result artifacts, six role
indexes and both audits, and deletes its created payloads and checkpoints. It also calls
`harness.rewrite_record(document)` before yielding, but it neither saves nor restores that record
in its own `finally` block.

A fresh temporary-harness probe measured the exact on-disk record around one context:

```text
before context: 25c94f4197e2b3f3994e85769c1b435db1dc85dbefe38552679f0f36daacc27c
during context: 56a6d1b19548defcb5bcf1698166b809352de03418f2e1282db2f233d36d64b4
after context:  56a6d1b19548defcb5bcf1698166b809352de03418f2e1282db2f233d36d64b4
restored: False
```

After exit, authentication with the context's returned digest fails because the record still
declares the temporary established-result digest while that result file has been restored to its
pre-context bytes. The autouse fixture repairs the record only after the whole test finishes.

`test_the_three_case_menu_restores_every_byte_it_touched` does not see this. Its snapshot
explicitly excludes `harness.record_path`, and after comparing the other files it calls
`harness.restore_record()` manually. That proves the manual restoration method works, not that the
context manager restores every byte it touched on exit. The helper should save the record bytes
and restore them in its own `finally`, and the test should include the record in the before/after
comparison without a manual repair.

## Verification

Executed only with the required project interpreter:

```text
.\venv\Scripts\python.exe -m pytest
  Reproducibility Packet/tests/test_connection_adapter.py
  Reproducibility Packet/tests/test_authenticated_storage.py -q
  -> 277 passed in 45.97 s

.\venv\Scripts\python.exe -O -m pytest
  Reproducibility Packet/tests/test_connection_adapter.py
  Reproducibility Packet/tests/test_authenticated_storage.py -q
  -> 277 passed, 1 expected PytestConfigWarning, in 10.31 s

.\venv\Scripts\python.exe -m pytest Reproducibility Packet/tests -q
  -> 2,935 passed in 247.33 s
```

The two independent probes used fresh temporary harnesses outside the repository. They opened no
delivered role root and spent no scientific resource. `git diff --check` passed before closeout.

## Scientific and authorization boundary

- No MuJoCo model was built, no rollout stepped, no fit or checkpoint created, no figure rendered,
  and no production connection record, delivered role payload or later-role result was opened.
- Counters remain **278 rollouts, 67 fits, 67 checkpoints and zero pilot/validation/test reads**.
- Slot-8 Steps 1–3, Step 4a, Step 4b-i and Step 4b-ii-a remain closed / both approved at their
  recorded historical bytes.
- Step 4b-ii-b remains Claude-owned, incomplete and unapproved. Row 21, open-set observation,
  remaining acceptance tests, CLI wiring, additive `build_role_bundle` change and mutation sweep
  remain unfinished.
- Full Step 4b, production connection records, real-role reads, Steps 4c–4f, capacity or threshold
  choice, final configuration and every C1-versus-S statement remain blocked.

## Live-Run README heartbeat

Checked under the Live-Run README playbook and left unchanged. A partial internal build and a
general review finding are not an artifact closure, phase transition or scientific result. The
public root README remains at jointly approved blob
`7342bc8ca5a256a411d69577199cc0c2e3dbc2d0`.

## Files created or updated by Codex

- `agents/Codex/Session Summaries/HumanReport152.md` — this detailed session record.
- `agents/Codex/Progress Reports/Progress Report Session 152.md` — nineteenth regular director
  update, covering Codex Sessions 145–152.
- `agents/Codex/README.md` — indexed both Session-152 reports and refreshed the active gate map.
- `agents/Codex/Summary of Only Necessary Context.md` — completely rewritten for Session 153.

No packet code, packet test, Review Card, chat transcript, protocol, Claim Sheet, configuration,
result artifact or public README byte was changed.

## Next steps

1. Claude should make the row-19 seam either a genuinely production-validator-accepted synthetic
   post-row-12 state or an explicitly narrower witness that does not claim that equivalence.
2. Claude should make `_three_case_menu` restore its connection record inside the context manager
   and strengthen the restoration test so the record is part of the asserted before/after state.
3. Claude can then continue its owned row 21, audit-hook observer, remaining B2/B3/B5 coverage,
   roles CLI wiring, additive `build_role_bundle` edit and two-pass mutation sweep.
4. Only after a complete stable candidate, Review Card, subject chat and explicit handoff should
   Codex perform formal Round 1.
