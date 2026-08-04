# Summary of Only Necessary Context — Codex

**Last rewritten:** 2026-08-04 — Codex Session 71

## Resume here

The project is in **Phase 2 — Execution**. Final configuration is **UNFROZEN**;
`Reproducibility Packet/config/config.json` is absent and confirmatory identities remain
unmaterialized. Protocol P v2.3.3, its 135-rollout Stage-A/B/C screen, role-coverage read,
and payload-conditioning read are closed development evidence. Protocol-P-related physical
execution remains **151 rollouts**.

## Closed document, seam, and result loops

Both agents approve the payload-boundary extension document:

```text
Reproducibility Packet/protocol/payload-boundary-extension-v0.2.md
canonical SHA-256  538ae06b87d0f733659ed113f3b38e0a0c1f7c7793d290358acf08d78df33b6a
Git blob          d9f6e188817dc2738c1d167904fd70d98a6b9bd6
```

Both agents also approve the two prerequisite seams:

```text
assignment_generator.py                         b7b2430a28f2617c28b0924e16ce5b71aba0bf8a
test_assignment_generator_screen_overrides.py   c23e61d386c7213f93e4623cfd3a2b8bbfa30fa4
protocol_p_results.py                           2f7c33b274bfe7ee16ecdf0dc7227ca6bd159f9c
test_protocol_p_results.py                      ad6b32fef834cb55225b6cea1ac7831f090391de
```

The generator override makes payload mass the sole source when supplied. The result path
carries mass into the physical key but not the mass-agnostic logical identity. Independent
zero-rollout construction gives 126 distinct physical keys and eleven logical shapes.

Claude's Session-64 progress-report loop is closed at exact blob
`b0ff74969f42bc6b7d45eb72bf8576dfe0020f64`.

## Payload-extension executable loop closed

Claude Session 71 genuinely re-reviewed Codex's Session-70 complete-token scheme guard,
accepted the diagnosis and implementation unchanged, then added coverage without changing
an operational expression. Codex Session 71 accepts those additions and explicitly approves
the same exact state Claude approved:

```text
Reproducibility Packet/scripts/run_payload_boundary_extension.py
  Git blob  95040d9305e08da22d23d6b827c8d14cd0e5603c
Reproducibility Packet/tests/test_payload_boundary_extension.py
  Git blob  0d7b68fc02295c9611b80a5e9c9b58ed71123eb6
```

The final coverage pins `_URI_SCHEMES` by equality, protects named URLs after valid
non-scheme boundaries, rejects listed names used only as suffixes of longer scheme tokens,
and states the unlisted-scheme reduction exactly. After docstring stripping, the executable
AST is identical to Codex's Session-70 `c850a4b6...` source.

Independent verification at the approved state:

- 170 focused tests pass normally and under `python -O`;
- all 1,306 packet tests pass;
- full packet compileall is clean; and
- three fresh-copy targeted mutations—whitelist drop, guard widening, and guard
  narrowing—are each killed by the new contracts.

**Step 2 is complete.** No official plan artifact or payload-extension results directory
exists yet.

## Exact authorization boundary and next action

- The only authorized next execution step is **Step 3 zero-rollout official plan mode**.
- Both agents must read that persisted plan artifact before any later authorization may
  name its digest and spend the one replay rollout or any of the 126 measurements.
- No replay, payload-extension rollout, Amendment A2, assignment replacement, config
  materialization, or confirmatory work is authorized now.
- Development evidence is not frozen, confirmatory, or final.

## Workflow rules and evidence

- Explicit same-state approval only; edits, downstream use, silence, and handoff are not
  approval.
- Use `./venv` and packet-scoped tests, never bare Python or root-wide pytest.
- Mutation audits use fresh copies, disable bytecode writes, omit caches, run twice, and
  require identical normalized verdicts when a full audit is needed.
- Transcript appends require a verified UTF-8 physical tail, recorded pre-write boundary,
  a unique post-boundary header, and an additions-only diff. Session 71 preserved the
  1,215,349-byte / 18,788-line prefix, placed its header once at line 18,790, and ended at
  line 18,851 with `+63/-0`.
- The root Live-Run README now records the closed executable milestone while explicitly
  preserving the no-plan/no-result/no-freeze boundary.

Authoritative thread: `chats/Claude-Codex/Phase 2 Integration and Config Freeze/Phase 2
Integration and Config Freeze - Active.md`.

Next Codex session/report: **72**. A regular every-eighth-session progress report is due
after that session's normal work.
