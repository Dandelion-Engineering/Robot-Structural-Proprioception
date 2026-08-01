# Summary of Only Necessary Context — Codex

**Last rewritten:** 2026-08-01 — Codex Session 54

## Resume here

The project is in **Phase 2 — Execution**. The final configuration is **UNFROZEN** and `Reproducibility Packet/config/config.json` does not exist. Stage 0 remains the only screen stage that has run. Stage-A/B/C execution is unauthorized; the replay and Stage 0 were not rerun in Codex Session 54; the confirmatory split is untouched.

The shared Protocol-P primitives, construction layer, and tests remain jointly approved at the exact states recorded in Codex Session 53. Claude Session 54 added:

```text
Reproducibility Packet/scripts/utils/protocol_p_results.py
  blob ef197b783290db6f3892f724e9c905b21ca63cdb

Reproducibility Packet/scripts/run_protocol_p_screen.py
  blob 6c745d073cb1f83b88e5420ba80f787b0f7b5dfe

Reproducibility Packet/tests/test_protocol_p_results.py
  blob 96b1376ad142ab0445eef04a59554265db49c361

Reproducibility Packet/tests/test_protocol_p_driver.py
  blob 7a443354ff10c4bcb9ce7696fdc984acf1435245
```

These four exact states are **BLOCKED**. The physical-origin provenance design is accepted in substance, but the executable driver does not yet implement all Protocol-P gate/drop/terminal branches correctly. Claude owns the corrected next state.

The authoritative live record is:

`chats/Claude-Codex/Phase 2 Integration and Config Freeze/Phase 2 Integration and Config Freeze - Active.md`

Codex Session 54 is physically last. The append passed the hard gate: the 902,416-byte / 13,001-line pre-write prefix remained byte-identical at SHA-256 `70b948040836447966ee926d942637a51f59900a326553e69db30d87f87704b6`; the new header appears exactly once at line 13,005; and the transcript diff is +134/−0. The post-append file is 908,639 bytes / 13,135 lines at SHA-256 `543758a8de87a5a486ee9d0024dc76018d7756798db11403d26ef17e64c335e5`.

## Session-54 accepted decisions

### Origin provenance

The results-layer rule from Session 53 is correct:

- 180 logical rows resolve to 168 physical executions;
- exactly twelve Stage-B/Stage-C rows cite selected Stage-A measurements;
- reused rows never call `build_overrides` or the generator and mint no stamp;
- a reused row carries its Stage-A origin hash and canonical payload unchanged; and
- the report distinguishes the consumer stage from the physical stage of origin.

Do not redesign this while correcting the blocked driver paths.

### CLI and helper import

`--mode plan` is accepted as the default because it runs zero rollouts. `--mode execute` remains explicit.

The driver may temporarily import `coefficient_vector`, `sensor_config_from_document`, and `verify_text_pins` from `analyze_synchronous_difference_null.py`. Each helper currently has two consumers; extract only when a real third consumer appears, through exact-state review.

## Blocking findings

### 1. Mixed Stage-A drop/survivor path

`run_stage_a` records a failing row and skips the remainder of that candidate. Later, `run_screen` excludes every row belonging to a dropped candidate from `executed_rows`, including the row that physically ran and entered the ledger. The completeness check then calls it surplus.

Codex reproduced this with the committed no-MuJoCo stub:

```text
two candidates: first fails its first healthy row, second survives
physical stub calls                         73
final error                                 ledger holds 1 unplanned physical result
```

The corrected full-driver test must reach persistence and show 73 physical results/stamps over 85 report rows (one measured drop row plus the 84-row complete one-candidate path), with the dropped row's provenance and gate evidence preserved.

### 2. Stage-B and Stage-C I12 wiring

`run_logical_row` computes `GateReport`; only `run_stage_a` consumes `passed`. `run_reuse_aware_rows` discards the returned result.

Codex injected one saturated step at Stage-B remEI 0.40. The current driver returned:

```text
terminal                    None
outcome_case                CASE_B
remEI 0.40 verdict          TESTABLE
gate_report in rows         absent
physical stub calls         72
```

This must instead reach Protocol P's `UNSAFE_LADDER_VALUE` terminal and exclude the value from TESTABLE/SUB_THRESHOLD. Add a real-driver Stage-B test. Add the companion Stage-C test: a failing healthy replicate must be refused before it enters operative `Q95_c`.

### 3. Persisted evidence and terminal paths

`PhysicalResult` holds `gate_report`, `n_steps`, and `elapsed_s`; `logical_row_report` persists none. The result must carry those fields through each physical origin (either on logical rows or in an explicit 168-entry physical ledger).

The all-dropped `NO_ADMISSIBLE_PROBE` return currently discards the ledger view of every rollout spent. Preserve those rows/provenance and implement the section-9 sub-branch from the 0.05-N / 0.5-ramp candidate:

- healthy or remEI 0.75 failure → implementation-integrity branch;
- remEI 0.35 failure → physical safety/method-limit branch, subject to I13a/I13b.

Minor cleanup: correct `physical_key`'s docstring. Python integer `1` and float `1.0` are equal and hash identically; normalization preserves the serialized numeric type, not key uniqueness.

## Verification from Session 54

```text
handed-off blobs                         exact
full packet suite                        906 passed in 55.13 s
compileall                               clean
mixed Stage-A probe                      block reproduced, no MuJoCo
unsafe Stage-B probe                     block reproduced, no MuJoCo
Protocol-P stage rollouts                zero
Stage-0/replay                           not re-run
config.json                              absent
confirmatory split                       untouched
```

The green suite is real but does not cover the two blocking full-driver states.

## Protocol-P state unchanged

Jointly approved and closed:

- Protocol P v2.3.3 at canonical digest `5689dad7ce4194b9a7dbe381006027df178997adf732f5734a77ef048bdf421f`;
- permanent I13b step-499/step-500 test;
- generator `ScreenOverrides` seam;
- one-row replay gate/result;
- Stage-0 implementation, result artifact, and packet README Step 24;
- shared Protocol-P primitives;
- Stage-A/B/C construction layer; and
- public README through the currently settled live entry.

The public README now accurately says the driver is built, unreviewed, and unauthorized to run. Codex Session 54 did not edit it because the internal review block is not a public milestone.

## Next actions

1. Claude corrects the five named paths: mixed drop, Stage-B unsafe terminal, Stage-C gate wire, persisted gate/elapsed evidence, and terminal ledger/sub-branch classification.
2. Claude adds discriminating full-driver tests and hands over an explicitly approved exact state.
3. Codex re-reviews the returned bytes and must explicitly approve before any Stage-A/B/C execution.
4. Only after the driver loop closes may the agents separately decide whether to authorize the 168 Stage-A/B/C physical executions. Implementation review is not execution permission.

Downstream remains unchanged: written Amendment A2, replacement approved assignment/config lineage, coherent regeneration, Gates 4–7, joint final config approval, and only then one-shot confirmatory generation/evaluation.

## Review and evidence rules

- Same-state approval is explicit. Creation, edits, handoff, downstream use, and silence are not approval.
- Development screens, pilots, fixtures, diagnostics, and regression checks remain separate from frozen/confirmatory/final results.
- Keep detection, attribution, information/action authorization, and control outcome separate.
- Do not use root-wide `pytest -q`; use `./venv`'s interpreter against `Reproducibility Packet/tests`.
- Never use bare `python` or `pip`.
- The confirmatory test split remains untouched: zero identities, zero payloads.
- Transcript appends use the hard gate: capture the UTF-8 physical tail/line count/hash, patch only a verified unique complete EOF block, then assert exact old prefix, one new header after the boundary, and additions-only diff.

## Closeout numbering

- Next Codex session: **55**.
- Next Codex human report: `agents/Codex/Session Summaries/HumanReport55.md`.
- Next regular Codex progress report: **Session 56**, unless a phase transition or approved amendment triggers one sooner.
