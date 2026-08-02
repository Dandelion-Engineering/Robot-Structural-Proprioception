# Summary of Only Necessary Context — Codex

**Last rewritten:** 2026-08-01 — Codex Session 56

## Resume here

The project is in **Phase 2 — Execution**. The final configuration is **UNFROZEN** and `Reproducibility Packet/config/config.json` does not exist. Stage 0 remains the only screen stage that has run. Stage-A/B/C execution is unauthorized; the replay and Stage 0 were not rerun in Codex Session 56; the confirmatory split is untouched.

The Protocol-P specification, replay/seam, Stage 0, shared primitives, construction layer, results layer, and Stage-A/B/C driver are now jointly approved. Claude Session 56 and Codex Session 56 explicitly approve the same revised executable states:

```text
Reproducibility Packet/scripts/run_protocol_p_screen.py
  blob 7668793e147a2776cb003ea90c79e76247d9b4de

Reproducibility Packet/tests/test_protocol_p_driver.py
  blob 23222d0ed03c26f57cfff5f53267ca8186a8d31a
```

The unchanged results states remain jointly approved:

```text
Reproducibility Packet/scripts/utils/protocol_p_results.py
  blob e84e5f9f4e6d10408873d87b81b2baef9535d50e

Reproducibility Packet/tests/test_protocol_p_results.py
  blob cbac30ed3d41c961f7d5c54c306c8a09fa1be1cd
```

Packet README Step 25 is open for owner re-review. Claude handed off blob `9191d4ab...`; Codex changed one phrase from “180 stamps over 168 rollouts” to “180 provenance references comprising 168 distinct stamps” and approves the reviewer-edited state:

```text
Reproducibility Packet/README.md
  blob 9c9fa7f03de8b000580704330755f232cfdb8ef1
```

Claude must reopen that exact blob and explicitly approve it unchanged or return a new state. This is a runbook wording loop, not an executable code block.

The required recent-work review also found that Claude's Session-56 progress report conflated one official replay result with the physical replay count. Codex corrected the report to state that the one-row replay gate physically ran four times: Session 45's original result, Session 46's clean and injected-stray-write verification runs, and Session 51's regression run after the shared-import edit. Codex approves the reviewer-edited report at blob `39c592422639b84005a2dd7d9539171be541a84c`; Claude must genuinely owner-review it too. Stage 0 used no physics and Stages A/B/C still spent zero rollouts.

The separate Stage-A/B/C execution-authorization decision has not been made.

The authoritative live record is:

`chats/Claude-Codex/Phase 2 Integration and Config Freeze/Phase 2 Integration and Config Freeze - Active.md`

Codex Session 56 is physically last. Two appends passed the hard gate. The main review append preserved the 945,410-byte / 13,628-line prefix at SHA-256 `a652d4df4db0ef9772d72a199cd10267f40d4541bdad7658c1496d2b3d4d3ea0` and placed its unique header at line 13,632. The later progress-report correction preserved the complete 950,681-byte / 13,741-line first-append state at SHA-256 `6c44700e277621e9706f0fad8e7b961a16326ae902efb5ebb67ce7175799141a` and placed its unique header at line 13,745. The final transcript diff is +151/−0; the file is 952,348 bytes / 13,779 lines at SHA-256 `5f127b2608f982b32f2c549a9992582fccaffea3efbd8b7b2810761adec564ef`.

## Session-56 approved decisions

### Document-derived I13a onset check

The construction layer's `require_constructed_condition` compares a built fault tuple against a fresh tuple produced by the same builder from the same caller-supplied onset. It can catch mutation after construction but cannot prove the shared onset came from the bound trajectory document.

The revised driver closes that gap:

- `screen_onset_index` reads `onset_time_s` directly from the bound trajectory and converts it with `_step_index`, which refuses off-grid times;
- `screen_physical_faults` exists at Correction 1's pre-registered signature and builds the expected tuple from that document-derived onset;
- `require_preregistered_faults` compares the constructed tuple field by field and type by type immediately before execution; and
- `run_logical_row` calls the check only for physical rows, before the executor. Reused rows construct nothing and never reach it.

The discriminating test builds a real step-0 override bundle. The old same-input comparison accepts it when given onset 0; the new document-derived check refuses it because the trajectory requires step 500. The wire test proves the executor receives zero calls on refusal.

### One production field authority plus an independent specification test

The helper delegates fault-field construction to `requested_fault_specs`; it does not repeat the seven field literals in production. The test quotes Correction 1's exact fields and binds that shared builder to the specification. Runtime comparison remains live against a mutated constructed tuple, while a mutation to the shared builder's own constants is caught by the independent specification test.

### Keep the redundant helper vocabulary guard

`screen_physical_faults` keeps its own unknown-condition refusal because Correction 1's executable sketch places the closed-set check inside the named helper. `SCREEN_CONDITIONS` is an alias of the construction layer's one tuple, not a second definition. The code and tests explicitly state that the helper line is a specification-fidelity/message guard, not load-bearing outcome coverage.

### Portable artifact path

Plan/results documents no longer record the producer's absolute config path. An in-packet config is recorded as `config/draft-config-v0.1.json`; an outside-packet config is reduced to a filename marker. The same input block retains the canonical base-config hash as the identity-bearing field.

### Replay sequencing accepted for the later round

Codex accepted Claude's proposal in principle: the dedicated execution round should first explicitly authorize one replay-gate check, run and review that bit-level positive control, and then separately decide whether to authorize the 168 Stage-A/B/C rollouts. No replay ran in Session 56.

## Verification from Session 56

```text
handed-off driver/test blobs              exact
independent plan mode                     0.287 s; zero rollouts
plan census                               9 candidates / 180 logical rows /
                                          168 physical rollouts / 12 reuses
derived onset and window                  500 / [1000, 1768)
plan results                              null
recorded config path                      config/draft-config-v0.1.json
drive-letter path in plan artifact        absent
focused driver suite                      148 passed in 96.43 s
full packet suite                         975 passed in 110.92 s
compileall                                clean
Protocol-P stage rollouts                 zero
Stage-0/replay                            not re-run
physical replay-gate executions to date   four (none in Session 56)
config.json                               absent
test-named / results NPZ                  0 / 0
confirmatory split                        untouched
```

Codex also wrote the required regular `Progress Reports/Progress Report Session 56.md`.

## Protocol-P state

Jointly approved and closed:

- Protocol P v2.3.3 at canonical digest `5689dad7ce4194b9a7dbe381006027df178997adf732f5734a77ef048bdf421f`;
- permanent I13b step-499/step-500 test;
- generator `ScreenOverrides` seam;
- one-row replay gate/result;
- Stage-0 implementation, result artifact, and packet README Step 24;
- shared Protocol-P primitives;
- Stage-A/B/C construction layer;
- Stage-A/B/C results layer; and
- Stage-A/B/C driver including the document-derived onset check and portable input-path reporting at the blobs above.

Open:

- packet README Step 25 owner re-review;
- Claude Session-56 progress-report owner re-review after the replay-count correction;
- the separate replay/execution-authorization round;
- the Stage-A/B/C result itself; and
- all downstream Amendment-A2/regeneration/final-freeze work.

The public README already contains Claude's Session-56 milestone. It accurately says the document-derived onset check and Step-25 plan audit exist, while all 168 physical executions remain unauthorized. Codex made no additional public entry because the reviewer wording change did not create a second public milestone.

## Next actions

1. Claude reopens packet README blob `9c9fa7f03de8b000580704330755f232cfdb8ef1` and progress-report blob `39c592422639b84005a2dd7d9539171be541a84c`, explicitly approving each unchanged or returning a new exact state.
2. After the Step-25 loop closes, the agents enter the separate execution-authorization round; the reporting loop is not an execution prerequisite but should close normally.
3. In that round, explicitly authorize and run the one-row replay gate immediately before measurement, then review its result.
4. Only after a separate explicit decision may the 168 Stage-A/B/C physical rollouts run once under the approved driver.
5. Poll the result JSON rather than a buffered log while a long execution is active.
6. Downstream remains written Amendment A2, replacement assignment/config lineage, coherent regeneration, Gates 4–7, joint final config approval, and only then one-shot confirmatory generation/evaluation.

## Review and evidence rules

- Same-state approval is explicit. Creation, edits, handoff, downstream use, and silence are not approval.
- Development screens, pilots, fixtures, diagnostics, and regression checks remain separate from frozen/confirmatory/final results.
- Keep physical rollout accounting separate from logical analysis rows; reuses cite immutable origin provenance and do not mint stamps.
- Keep detection, attribution, information/action authorization, and control outcome separate.
- Do not use root-wide `pytest -q`; use `./venv`'s interpreter against `Reproducibility Packet/tests`.
- Never use bare `python` or `pip`.
- The confirmatory test split remains untouched: zero identities, zero payloads.
- Transcript appends use the hard gate: capture the UTF-8 physical tail/line count/hash, patch only a verified unique complete EOF block, then assert exact old prefix, one new header after the boundary, and additions-only diff.
- The root Live-Run README is append-only while Phase 2 remains live; do not edit earlier dated entries to make the history cleaner.

## Closeout numbering

- Next Codex session: **57**.
- Next Codex human report: `agents/Codex/Session Summaries/HumanReport57.md`.
- Next regular Codex progress report: **Session 64**, unless a phase transition or approved amendment triggers one sooner.
