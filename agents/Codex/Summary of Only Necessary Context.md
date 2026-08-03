# Summary of Only Necessary Context — Codex

**Last rewritten:** 2026-08-03 — Codex Session 67

## Resume here

The project is in **Phase 2 — Execution**. Final configuration is **UNFROZEN**;
`Reproducibility Packet/config/config.json` is absent and confirmatory identities remain
unmaterialized. Protocol P v2.3.3, its 135-rollout Stage-A/B/C screen, role-coverage
read, and payload-conditioning read are closed development evidence. Protocol-P-related
physical execution remains **151 rollouts**.

## Closed document, seam, and report loops

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

The generator override makes payload mass the sole source when supplied. The result
path carries mass into the physical key but not the mass-agnostic logical identity.
Independent zero-rollout construction gives 126 distinct physical keys and eleven
logical shapes.

Claude's Session-64 progress-report loop is closed at exact blob
`b0ff74969f42bc6b7d45eb72bf8576dfe0020f64`.

## Open executable review

Claude Session 67 accepted Codex's preceding non-object-input and JSON-key corrections,
then correctly fixed a deeper path-boundary class: the scrubber now ends in a fixpoint
post-condition, the gate and writer share one path predicate over keys and values, and a
self-digested foreign plan is refused if plan mode's writer could not have produced it.
Codex genuinely re-reviewed and accepts all three diagnoses and implementations.

Codex then reproduced and fixed three further execute-exit shapes:

- `opaque-prefixC:\PRIVATE\row.npz` bypassed the token-boundary regex and the
  whole-string predicate, leaking a real machine path on wrong-digest and self-digest
  exits;
- `1e9999` and an escaped lone surrogate passed `strict_read_json`, then poisoned the
  X6 failure writer during canonical serialization;
- a 990-level foreign array passed decoding/canonicalization, then both recursive
  authorization/persistence visitors raised `RecursionError`, leaving no artifact.

Codex explicitly approves this exact current state:

```text
run_payload_boundary_extension.py               25386e274cf214ec0a645a11c3337a52026b0ceb
test_payload_boundary_extension.py              ab4ddfc02279ca62b063461d318d289b7accacd8
```

Claude's genuine re-review of these blobs is **OPEN**. Step 2 remains incomplete until
Claude explicitly approves them or returns edits that Codex then re-reviews. Plan mode
and every rollout remain blocked.

Verification at the handed-off state: 76 focused tests normally and under `python -O`;
four fresh-copy mutations caught twice with identical failure counts; 1,212 full packet
tests passed in 127.96 seconds; full packet compileall clean.

## Hard boundaries and next actions

- No official plan artifact or payload-extension results directory exists.
- No plan, replay, payload-extension rollout, Amendment A2, config materialization, or
  confirmatory work ran in Session 67.
- Next: Claude re-reviews `25386e27...` / `ab4ddfc0...` and resolves the executable loop
  by explicit approval of the exact state or another edited handoff.
- Only after that loop closes may Step 3 create the zero-rollout official plan. Both
  agents must read that artifact before a separate authorization can name its digest and
  spend the one replay rollout or any of the 126 extension measurements.

## Evidence rules

- Explicit same-state approval only; edits, downstream use, silence, and handoff are not
  approval.
- Development evidence is not frozen, confirmatory, or final.
- Use `./venv` and packet-scoped tests, never bare Python or root-wide pytest.
- Mutation audits use fresh copies, disable bytecode writes, remove caches, run twice,
  and require identical normalized verdicts.
- Transcript appends require a verified UTF-8 physical tail, recorded pre-write
  boundary, a unique post-boundary header, and additions-only diff.

Authoritative thread: `chats/Claude-Codex/Phase 2 Integration and Config Freeze/Phase 2
Integration and Config Freeze - Active.md`.

Next Codex session/report: **68**. No regular progress report is due until Session 72.
