# Summary of Only Necessary Context — Codex

**Last rewritten:** 2026-08-02 — Codex Session 63

## Resume here

The project is in **Phase 2 — Execution**. Final configuration is **UNFROZEN**;
`Reproducibility Packet/config/config.json` is absent and confirmatory identities remain
unmaterialized. Protocol P v2.3.3, its 135-rollout Stage-A/B/C screen, role-coverage
read, and payload-conditioning read are closed development evidence.

## Closed payload-boundary document loop

Both agents explicitly approve:

```text
Reproducibility Packet/protocol/payload-boundary-extension-v0.2.md
canonical SHA-256  538ae06b87d0f733659ed113f3b38e0a0c1f7c7793d290358acf08d78df33b6a
Git blob          d9f6e188817dc2738c1d167904fd70d98a6b9bd6
bytes / lines     71,188 / 1,285, LF, no BOM
```

The unified Option-B rule was independently exhaustive over 19,448 monotone states:
R10/R11/R12 = 8,008/3,515/7,925; the weaker rule admitted 4,106 role-losing bands and
3,185 already-licensed cap increases; the unified rule has zero anomalies.

Document approval authorizes **Step-2 build/review only**. It does not authorize plan
mode, replay, execution, Amendment A2, config materialization, or confirmation.

## Open Step-2 seam review

Codex built and explicitly approves these exact partial Step-2 states:

```text
assignment_generator.py                         b7b2430a28f2617c28b0924e16ce5b71aba0bf8a
test_assignment_generator_screen_overrides.py   c23e61d386c7213f93e4623cfd3a2b8bbfa30fa4
protocol_p_results.py                           eaa3379718e37276f39463903eceac6f52ac1db5
test_protocol_p_results.py                      7361bfd8d51351d351539b0a0b0ec0aa1d6863d9
```

`ScreenOverrides.distal_payload_mass_kg` is inert at `None`, active at zero, validated
finite/nonnegative, and the sole mass source when supplied. `PhysicalKey` carries an
additive float-normalized mass and reports it, preventing cross-mass key reuse under CRN.

Claude's exact-state review is **OPEN**. The third prerequisite, the payload-boundary
executable, is unbuilt. Step 2 is therefore incomplete and Step 3 is blocked.

Verification: 121 focused tests; six source mutations killed identically in two passes
with caches cleared and bytecode disabled; full packet 1,133 passed in 133.35 s;
compileall and diff hygiene clean. Zero rollouts and no plan run this session.

## Standing state and next actions

- Stage-A/B/C result remains `CASE_B`, 135 physical / 147 logical, selected 0.10 N /
  0.25 ramp; development-only.
- Payload-conditioning says 0.050 kg roughly halves structural signal; the unmeasured
  masses are 0.025, 0.075, 0.100, 0.125, 0.150, 0.200 kg.
- Protocol-P-related physical executions remain **151**.
- Next: Claude reviews the four seam/test blobs. Then build and review the executable,
  run the corrected mutation sweep, and obtain both agents' exact-state approval.
- Only after all three prerequisites close may plan mode produce a zero-rollout plan.
  Both agents must read it before a separate execution authorization names its digest.

## Evidence rules

- Explicit same-state approval only; edits, downstream use, silence, and handoff are not
  approval.
- Development evidence is not frozen, confirmatory, or final.
- Use `./venv` and packet-scoped tests, never bare Python or root-wide pytest.
- Mutation audits clear `__pycache__`, disable bytecode, run twice, and require identical
  verdict sets.
- Transcript appends require verified UTF-8 tail, byte-identical old prefix, a unique
  post-boundary header, and additions-only diff.

Authoritative thread: `chats/Claude-Codex/Phase 2 Integration and Config Freeze/Phase 2
Integration and Config Freeze - Active.md`.

Next Codex session/report: **64**. Session 64 also requires the regular progress report.
