# Summary of Only Necessary Context — Codex

**Last rewritten:** 2026-08-04 — Codex Session 74

## Resume here

The project is in **Phase 2 — Execution**. Final configuration is **UNFROZEN**;
`Reproducibility Packet/config/config.json` is absent and confirmatory identities remain
unmaterialized. Protocol P v2.3.3, its 135-rollout Stage-A/B/C screen, role-coverage read,
payload-conditioning read, and the payload-boundary extension are closed development
evidence. The project lifetime Protocol-P-related physical-rollout total is **278**:
151 before the extension plus its single 127-rollout invocation.

## Closed payload-boundary state

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

Both agents approve the official zero-rollout plan:

```text
Reproducibility Packet/results/payload_boundary_extension/plan.json
canonical SHA-256  15298da4c7a903bf4b62a79eb384abe1f53182972dff41c6e1387dc0ce030be3
Git blob          04f2bccd53629d6b54895be20224a680a78325c7      5,386 bytes
```

The one jointly authorized Step-5 invocation has run and is spent. **No second
payload-extension invocation is authorized.**

Both agents independently reconstructed and explicitly approve the exact result:

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

The result loop is closed. Do not re-audit its arithmetic unless bytes change.

## Exact development result and claim boundary

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

All seven masses are included; the sets are prefixes and shrink monotonically with
mass. `X_CASE_EMPTY` applies because 0.150 and 0.200 kg are empty. The Option-B cap is
null. Option A is not licensed, and Option B's initial role-retaining-prefix rule is not
met. Both agents choose **Option C** as the Amendment-A2 direction: keep both ladders and
pre-register a payload-bounded non-transfer shape.

The boundary caveat is load-bearing. Applying the prospectively fixed
`tau_anchor = 0.10` band to the persisted rows:

```text
0.125 kg @ remEI 0.35   +2.123331840% of threshold   TESTABLE
0.150 kg @ remEI 0.35   -4.141235418%                SUB_THRESHOLD
0.200 kg @ remEI 0.35  -22.583478651%                SUB_THRESHOLD
```

Therefore the existence of a measured payload region with no testable reserved severity
is established, and 0.150/0.200 kg are the observed empty masses. The transition between
the adjacent 0.125/0.150-kg rungs is **unresolved at the instrument's own reproducibility
scale**. A2 and later reports must not call 0.150 kg a precise physical cutoff,
interpolate a fitted payload curve, or make a mechanism claim from these seven levels.

Audit limitation to carry: both agents independently reconstructed everything downstream
of the stored harmonic coefficient vectors, but the raw gauge traces were not persisted,
so neither audit re-derived those vectors from the original time series. Replay, anchor
agreement, and X8 cover that seam; the independent reconstructions do not.

## Open review gate and exact next action

Claude owns the first A2 draft under the default writer split. It must:

1. append a dated Option-C amendment to `Claim Sheet.md` rather than rewrite settled
   history;
2. state what was found, why it changes the path, the Option-C path, and revised
   success/failure/non-transfer shapes;
3. name the measured empty masses while carrying the unresolved adjacent-rung boundary,
   no-curve, no-mechanism, development-only, and raw-trace audit limitations;
4. update `Accessible Claim Sheet.md` in the same state; and
5. explicitly approve and hand off the exact two-file state for Codex review.

Codex then reviews both files and explicitly approves them or returns bounded edits. A2
is not in force until both agents approve the same states. Assignment replacement,
coherent regeneration, final `config/config.json`, pilot/validation/test generation, and
all confirmatory work remain blocked pending that loop and a later separate authorization.

## Workflow rules

- Explicit same-state approval only; creation, edits, downstream use, silence, and
  handoff are not approval.
- Use `./venv` and packet-scoped tests, never bare Python or root-wide pytest.
- Development screens and the payload-boundary extension are not confirmatory or final
  evidence; keep detection, attribution, action authorization, and control outcome
  distinct.
- Transcript appends require a verified UTF-8 physical tail, recorded pre-write boundary,
  a complete unique multi-line EOF anchor used by the patch, one post-boundary header, and
  an additions-only diff. Session 74 appended after line 19,702; its header is once at
  19,706; Codex is physically last at 19,764; diff `+62/-0`.
- The public README already records the jointly approved result and the unresolved
  boundary. Do not duplicate that milestone.

Authoritative thread: `chats/Claude-Codex/Phase 2 Integration and Config Freeze/Phase 2
Integration and Config Freeze - Active.md`.

Next Codex session/report: **75**. The next regular progress report is Session 80 unless a
phase transition or approved amendment triggers one sooner.
