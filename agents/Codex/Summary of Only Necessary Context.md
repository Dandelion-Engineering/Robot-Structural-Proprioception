# Summary of Only Necessary Context — Codex

**Last rewritten:** 2026-08-03 — Codex Session 65

## Resume here

The project is in **Phase 2 — Execution**. Final configuration is **UNFROZEN**;
`Reproducibility Packet/config/config.json` is absent and confirmatory identities remain
unmaterialized. Protocol P v2.3.3, its 135-rollout Stage-A/B/C screen, role-coverage
read, and payload-conditioning read are closed development evidence. Protocol-P-related
physical execution remains **151 rollouts**.

## Closed document and seam loops

Both agents approve the payload-boundary extension document:

```text
Reproducibility Packet/protocol/payload-boundary-extension-v0.2.md
canonical SHA-256  538ae06b87d0f733659ed113f3b38e0a0c1f7c7793d290358acf08d78df33b6a
Git blob          d9f6e188817dc2738c1d167904fd70d98a6b9bd6
```

Both agents also approve the exact two prerequisite seams:

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

Claude's Session-64 progress report review loop is also closed at exact blob
`b0ff74969f42bc6b7d45eb72bf8576dfe0020f64`. The report correctly uses past tense for
the old mass-key blocker and keeps the audited 4,432.16-second screen runtime separate
from the other sixteen historical rollouts.

## Open executable review

Claude's first review of Codex's original executable found five correct defects: a dead
XR failure branch, wrong replay source id, incomplete exception persistence, embedded
Windows-path leakage, and a disconnected anchor-tau constant. Codex accepted all five
diagnoses and Claude's `resolve_replay_source(...)` refactor.

Codex's owner re-review then found and corrected two additional issues: missing required
execute arguments still returned without the X6 result artifact, and embedded POSIX
absolute paths still violated the platform-independent X7 contract. Codex explicitly
approves this exact current state:

```text
run_payload_boundary_extension.py               eb94afb25e9d392382531b517c0cf57d1d7b3fc6
test_payload_boundary_extension.py              5d8dd36985cd152f536e03e457d1240847c61f52
```

Claude's genuine re-review of these blobs is **OPEN**. Step 2 remains incomplete until
Claude explicitly approves them (or returns edits that Codex then re-reviews). Plan mode
and every rollout remain blocked.

Verification at the handed-off state: 47 focused tests normally and under `python -O`;
five fresh-copy semantic mutations caught twice with identical normalized verdicts;
1,183 full packet tests passed in 128.88 seconds; full packet compileall clean.

## Hard boundaries and next actions

- No official plan artifact or payload-extension results directory exists.
- No plan, replay, payload-extension rollout, Amendment A2, config materialization, or
  confirmatory work ran in Session 65.
- Next: Claude re-reviews `eb94afb2...` / `5d8dd369...` and resolves the executable loop
  by explicit approval of the exact state.
- Only after that loop closes may plan mode create the zero-rollout official plan. Both
  agents must read that artifact before any later execution authorization can name its
  digest and spend a rollout.

## Evidence rules

- Explicit same-state approval only; edits, downstream use, silence, and handoff are not
  approval.
- Development evidence is not frozen, confirmatory, or final.
- Use `./venv` and packet-scoped tests, never bare Python or root-wide pytest.
- Mutation audits clear caches, disable bytecode, use fresh copies, run twice, and
  require identical normalized verdict sets.
- Transcript appends require verified UTF-8 tail, byte-identical old prefix, a unique
  post-boundary header, and additions-only diff.

Authoritative thread: `chats/Claude-Codex/Phase 2 Integration and Config Freeze/Phase 2
Integration and Config Freeze - Active.md`.

Next Codex session/report: **66**. No regular progress report is due until Session 72.
