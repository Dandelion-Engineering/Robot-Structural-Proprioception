# Summary of Only Necessary Context — Codex

**Last rewritten:** 2026-08-04 — Codex Session 70

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

## Open executable review

Claude Session 70 genuinely re-reviewed Codex's Session-69 disclosure-only edit and kept
it. Claude then correctly fixed two additional path-enumerator families: the former
alphanumeric-colon UNC exemption could publish `reason://host/...` intact, and the former
forward-drive boundary could retain a drive designator in glued prose. Claude also repaired
a final-component test that had become green through the wrong matcher. Codex accepts all
three diagnoses, implementations, and Claude's whitelist judgment, including keeping
`file` outside the protected scheme list.

Codex's genuine return review found one narrower implementation defect in the new
whitelist. Each fixed lookbehind protected an allowed name merely as the suffix of a longer,
unlisted scheme token. Thus `reasonhttps://host/PRIVATE/row.npz`,
`prefixgit://host/PRIVATE/row.npz`, and `myssh://host/PRIVATE/row.npz` survived unchanged,
while the shared writer predicate found no offender. This contradicted the documented rule
that all unlisted schemes are reduced. The existing `git+ssh://` accept-side test was also
passing only through the accidental `ssh` suffix match.

Codex corrected the guard to protect complete RFC scheme tokens, explicitly added
`git+ssh` to the whitelist, updated the stale drive-boundary documentation, and added a
red-checked parameterized suffix contract. Codex explicitly approves this exact state:

```text
run_payload_boundary_extension.py               c850a4b62bf7f401fb0f0c0da65174811419690f
test_payload_boundary_extension.py              150870f494fb6e9a57bf9678762fda29cccb8eb1
```

Claude's genuine re-review of these blobs is **OPEN**. Step 2 remains incomplete until
Claude explicitly approves them or returns edits that Codex then re-reviews. Plan mode and
every rollout remain blocked.

Verification at the handed-off state:

- the new contract was red for all seven schemes present in Claude's exact source state;
- a 312-cell scheme/boundary/case matrix has zero errors;
- 152 focused tests pass normally and under `python -O`;
- all 1,288 packet tests pass;
- full packet compileall is clean; and
- an eleven-case fresh-copy mutation audit kills every deliberate fault in two identical
  normalized passes with bytecode writes disabled and caches omitted.

## Hard boundaries and next actions

- No official plan artifact or payload-extension results directory exists.
- No plan, replay, payload-extension rollout, Amendment A2, config materialization, or
  confirmatory work ran in Session 70.
- Next: Claude re-reviews `c850a4b6...` / `150870f4...` and resolves the executable loop by
  explicit approval of the exact state or another edited handoff.
- Only after that loop closes may Step 3 create the zero-rollout official plan. Both agents
  must read that artifact before a separate authorization can name its digest and spend the
  one replay rollout or any of the 126 extension measurements.

## Evidence and workflow rules

- Explicit same-state approval only; edits, downstream use, silence, and handoff are not
  approval.
- Development evidence is not frozen, confirmatory, or final.
- Use `./venv` and packet-scoped tests, never bare Python or root-wide pytest.
- Mutation audits use fresh copies, disable bytecode writes, omit caches, run twice, and
  require identical normalized verdicts.
- Transcript appends require a verified UTF-8 physical tail, recorded pre-write boundary,
  a unique post-boundary header, and an additions-only diff. Session 70 preserved the exact
  1,200,793-byte prefix, placed its header once at line 18,514, and ended at line 18,620.
- The root Live-Run README stays unchanged while this internal review loop remains open.

Authoritative thread: `chats/Claude-Codex/Phase 2 Integration and Config Freeze/Phase 2
Integration and Config Freeze - Active.md`.

Next Codex session/report: **71**. No regular progress report is due until Session 72.
