# Summary of Only Necessary Context — Codex

**Last rewritten:** 2026-08-01 — Codex Session 55

## Resume here

The project is in **Phase 2 — Execution**. The final configuration is **UNFROZEN** and `Reproducibility Packet/config/config.json` does not exist. Stage 0 remains the only screen stage that has run. Stage-A/B/C execution is unauthorized; the replay and Stage 0 were not rerun in Codex Session 55; the confirmatory split is untouched.

The Protocol-P specification, replay/seam, Stage 0, shared primitives, construction layer, and Stage-A/B/C driver/results implementation are now jointly approved. Claude Session 55 and Codex Session 55 explicitly approve the same four exact states:

```text
Reproducibility Packet/scripts/utils/protocol_p_results.py
  blob e84e5f9f4e6d10408873d87b81b2baef9535d50e

Reproducibility Packet/scripts/run_protocol_p_screen.py
  blob 99e2d44744eaf7ecd2bda1a21acce1ec9ce435c4

Reproducibility Packet/tests/test_protocol_p_results.py
  blob cbac30ed3d41c961f7d5c54c306c8a09fa1be1cd

Reproducibility Packet/tests/test_protocol_p_driver.py
  blob 3f1a81067116f2815f8680e6307e15e06c629db6
```

The Session-54 block is closed. This is implementation approval only, not permission to spend the screen's 168 physical rollouts.

The authoritative live record is:

`chats/Claude-Codex/Phase 2 Integration and Config Freeze/Phase 2 Integration and Config Freeze - Active.md`

Codex Session 55 is physically last. The append passed the hard gate: the 919,779-byte / 13,337-line pre-write prefix remained byte-identical at SHA-256 `3eef7390912f6ee636c242763725796164db7fef969ab2da46f44d1f4e42cd3f`; the new header appears exactly once at line 13,341; and the transcript diff is +64/−0. The post-append file is 922,425 bytes / 13,401 lines at SHA-256 `529da52e56e1b424d80b9acc308bfb494690840feafc469cf6418110a81a0724`.

## Session-55 approved decisions

### Corrected driver state

The exact four-file state now correctly implements:

- 180 logical rows over 168 physical origins on the clean nine-candidate path;
- twelve Stage-B/Stage-C reuse rows that cite immutable selected Stage-A origins;
- measured Stage-A reporting, including a gate-failing row from a dropped candidate;
- complete evidence on mixed drop/survivor and all-dropped terminal paths;
- per-rollout I12 hard-gate propagation through Stage B and Stage C;
- `UNSAFE_LADDER_VALUE` without a margin or Case-A/B/C classification;
- refusal of an unsafe Stage-C healthy replicate before construction of `Q95_c`;
- section-9 `NO_ADMISSIBLE_PROBE` integrity, physical-limit, and unclassified sub-branches;
- one persisted physical ledger entry per executed rollout with full gate report, step count, elapsed time, provenance, canonical payload, and coefficients; and
- one evidence attachment path shared by normal and terminal results.

### Driver-side Stage-C label

`UNSAFE_STAGE_C_REPLICATE` is accepted without a Protocol-P v2.3.3 bump.

It is explicitly a driver-side fail-closed label, not a pre-registered scientific outcome. It builds no operative null, assigns no Case A/B/C, reopens no probe selection, freezes no config, and authorizes no downstream result. Section 9 already requires safe, valid per-cell mechanics verdicts before any case exists. The label merely records why that prerequisite failed while preserving the rollouts already spent.

### I13b remains an external precondition

The physical-limit `NO_ADMISSIBLE_PROBE` branch names:

- I13a as asserted for the specific rollout by the construction layer before execution; and
- I13b as the permanent packet test `tests/test_cable_plant_softening_boundary.py`, which the driver does not run or claim to assert.

That division matches Protocol P v2.3.3. The full packet suite must be passing before any stage is authorized.

## Verification from Session 55

```text
handed-off blobs                         exact
full packet suite                        938 passed in 112.07 s
compileall                               clean
Protocol-P stage rollouts                zero
Stage-0/replay                           not re-run
config.json                              absent
test-named / results .npz                0 / 0
confirmatory split                       untouched
```

No implementation, test, protocol, assignment, config, dataset, or result artifact changed in Codex Session 55. Codex appended the same-state approval to the active transcript and appended one public README milestone recording joint driver approval while preserving the no-execution boundary.

## Protocol-P state

Jointly approved and closed:

- Protocol P v2.3.3 at canonical digest `5689dad7ce4194b9a7dbe381006027df178997adf732f5734a77ef048bdf421f`;
- permanent I13b step-499/step-500 test;
- generator `ScreenOverrides` seam;
- one-row replay gate/result;
- Stage-0 implementation, result artifact, and packet README Step 24;
- shared Protocol-P primitives;
- Stage-A/B/C construction layer; and
- Stage-A/B/C driver/results implementation at the four blobs above.

The public README now accurately says the corrected driver is jointly approved but has not run. The 168 physical screen executions remain unauthorized. Stage 0 remains the only measured screen stage.

## Next actions

1. Claude may add the packet runbook step for the approved driver and implement `screen_physical_faults`, returning any review-bearing exact state normally.
2. The agents separately review/close the remaining pre-execution work.
3. Only after that closure may they make an explicit Stage-A/B/C execution-authorization decision. Implementation approval is not execution permission.
4. If execution is authorized, the screen runs once under the approved driver; poll the result JSON rather than a buffered log, per Protocol P.
5. Downstream remains: written Amendment A2, replacement approved assignment/config lineage, coherent regeneration, Gates 4–7, joint final config approval, and only then one-shot confirmatory generation/evaluation.

## Review and evidence rules

- Same-state approval is explicit. Creation, edits, handoff, downstream use, and silence are not approval.
- Development screens, pilots, fixtures, diagnostics, and regression checks remain separate from frozen/confirmatory/final results.
- Keep detection, attribution, information/action authorization, and control outcome separate.
- Do not use root-wide `pytest -q`; use `./venv`'s interpreter against `Reproducibility Packet/tests`.
- Never use bare `python` or `pip`.
- The confirmatory test split remains untouched: zero identities, zero payloads.
- Transcript appends use the hard gate: capture the UTF-8 physical tail/line count/hash, patch only a verified unique complete EOF block, then assert exact old prefix, one new header after the boundary, and additions-only diff.
- The root Live-Run README is append-only while Phase 2 remains live; do not edit earlier dated entries to make the history cleaner.

## Closeout numbering

- Next Codex session: **56**.
- Next Codex human report: `agents/Codex/Session Summaries/HumanReport56.md`.
- Next regular Codex progress report: **Session 56**, unless a phase transition or approved amendment triggers one sooner.
