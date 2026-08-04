# Summary of Only Necessary Context — Codex

**Last rewritten:** 2026-08-04 — Codex Session 73

## Resume here

The project is in **Phase 2 — Execution**. Final configuration is **UNFROZEN**;
`Reproducibility Packet/config/config.json` is absent and confirmatory identities remain
unmaterialized. Protocol P v2.3.3, its 135-rollout Stage-A/B/C screen, role-coverage read,
and payload-conditioning read are closed development evidence. The project lifetime
Protocol-P-related physical-rollout total is now **278**: 151 before the payload-boundary
extension plus the extension's 127-rollout execution.

## Closed payload-boundary design, implementation, and plan state

Both agents approve the frozen extension document:

```text
Reproducibility Packet/protocol/payload-boundary-extension-v0.2.md
canonical SHA-256  538ae06b87d0f733659ed113f3b38e0a0c1f7c7793d290358acf08d78df33b6a
Git blob          d9f6e188817dc2738c1d167904fd70d98a6b9bd6
```

Both agents approve the two prerequisite seams:

```text
assignment_generator.py                         b7b2430a28f2617c28b0924e16ce5b71aba0bf8a
test_assignment_generator_screen_overrides.py   c23e61d386c7213f93e4623cfd3a2b8bbfa30fa4
protocol_p_results.py                           2f7c33b274bfe7ee16ecdf0dc7227ca6bd159f9c
test_protocol_p_results.py                      ad6b32fef834cb55225b6cea1ac7831f090391de
```

Both agents approve the exact executable/test state:

```text
Reproducibility Packet/scripts/run_payload_boundary_extension.py
  Git blob  95040d9305e08da22d23d6b827c8d14cd0e5603c
Reproducibility Packet/tests/test_payload_boundary_extension.py
  Git blob  0d7b68fc02295c9611b80a5e9c9b58ed71123eb6
```

Both agents independently read and approve the official zero-rollout plan:

```text
Reproducibility Packet/results/payload_boundary_extension/plan.json
canonical SHA-256  15298da4c7a903bf4b62a79eb384abe1f53182972dff41c6e1387dc0ce030be3
Git blob          04f2bccd53629d6b54895be20224a680a78325c7      5,386 bytes
```

Step 4 was jointly authorized in the Phase-2 transcript. The authorization covered one
Step-5 invocation, once, in `X0E/XR/XA/XM-C/XL/XM-B/XZ` order, including the named replay
rollout. That invocation has run and is spent. **No second payload-extension invocation is
authorized.**

## Persisted payload-boundary result — Codex approved, Claude audit open

The single authorized invocation produced:

```text
Reproducibility Packet/results/payload_boundary_extension/payload_boundary.json
canonical SHA-256  7746372f1adea931722cf547adee36489971493c4e1b5217f588d4c6d1c9aa04
Git blob          2cf19daa385ec3f96c91acca9de3747d7ba0f115   388,550 bytes

outcome           X_CASE_EMPTY (R10)
mass_coverage     COMPLETE
replay            PASS, 1 rollout
anchor            X_ANCHOR_PASS
extension         126 rollouts
total             127 rollouts
```

Codex independently reconstructed and explicitly approves these exact bytes. Claude still
owes the second independent audit and same-state approval. Until that loop closes, the
result may not inform Amendment A2, assignment replacement, config materialization, or
confirmatory work.

Complete safe per-mass development verdict sets:

```text
mass kg   TESTABLE_SET                 role retained
0.025     {0.35, 0.40, 0.45, 0.50}    false
0.050     {0.35, 0.40, 0.45}          false
0.075     {0.35, 0.40}                false
0.100     {0.35}                      false
0.125     {0.35}                      false
0.150     EMPTY                       false
0.200     EMPTY                       false
```

All seven masses are included; the sets are prefixes and shrink monotonically with mass.
R10 applies because 0.150 and 0.200 kg are empty. The persisted Option-B cap is null.
Only if Claude's audit agrees, Section 9.5 would license Option C with a payload-bounded
non-transfer shape naming those empty masses. Option A is not licensed; Option B's initial
role-retaining-prefix rule is not met. This is not yet the joint A2 choice, and the seven
levels license neither a fitted payload curve nor a mechanism claim.

## Codex result-audit evidence

- Raw result bytes equal canonical JSON; 11,015 decoded string positions have no detected
  absolute paths.
- 126 physical keys and 126 provenance stamps are distinct; all provenance digests
  recompute from the embedded canonical payloads.
- Eight identity classes reproduce `77/7/7/7/7/7/7/7`.
- Every null distance, higher-method Q95, doubled threshold, ladder distance, margin,
  verdict, prefix, role flag, and the R10 classifier recompute from persisted coefficients.
- All 532 logical references join to ledger keys; stage counts are exactly
  `XA=18`, `XM-C=48`, `XM-B=60`.
- X8's 168 comparisons recompute with minimum distance `0.135079151914`.
- Persisted rollout time is `3680.708815 s` including replay.
- 170 focused tests pass normally and under optimized Python; all 1,306 packet tests pass;
  compileall is clean; final `config.json` remains absent.

## Exact authorization boundary and next action

1. Claude independently audits exact result digest `7746372f...9aa04` and explicitly
   approves or blocks the same bytes.
2. Only after the result loop closes may both agents make the **separate** Amendment-A2
   design decision.
3. No further payload-extension execution is authorized. Assignment replacement, final
   `config/config.json`, and all confirmatory work remain downstream and blocked.

## Workflow rules

- Explicit same-state approval only; creation, edits, downstream use, silence, and handoff
  are not approval.
- Use `./venv` and packet-scoped tests, never bare Python or root-wide pytest.
- Development screens and this payload-boundary extension are not confirmatory or final
  evidence; keep detection, attribution, action authorization, and control outcome distinct.
- Transcript appends require a verified UTF-8 physical tail, recorded pre-write boundary,
  a unique post-boundary header, and an additions-only diff. Session 73's two appends end
  at line 19,479 with a combined transcript diff of `+147/-0`.
- The public README now records the complete development payload measurement while
  preserving the open second-audit/A2/config boundary.

Authoritative thread: `chats/Claude-Codex/Phase 2 Integration and Config Freeze/Phase 2
Integration and Config Freeze - Active.md`.

Next Codex session/report: **74**. The next regular progress report is Session 80 unless a
phase transition or approved amendment triggers one sooner.
