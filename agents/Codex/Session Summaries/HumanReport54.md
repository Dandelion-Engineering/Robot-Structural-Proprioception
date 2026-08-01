# Human Report — Codex Session 54

**Current date and time:** 2026-08-01 10:12 PDT

**Phase:** Phase 2 — Execution

**Session role:** Exact-state reviewer of Claude Session 54's Protocol-P Stage-A/B/C results layer and screen driver

**Final config state:** **UNFROZEN**; `Reproducibility Packet/config/config.json` does not exist

**Protocol-P execution state:** Stage 0 remains executed exactly once and jointly approved. No replay, Stage-A/B/C rollout, or Stage-0 re-execution occurred this session. Stages A/B/C remain unexecuted and unauthorized. The confirmatory test split remains untouched.

---

## Summary

Claude Session 54 implemented the Stage-A/B/C results layer and driver as four new files and explicitly approved those exact states. The implementation correctly realizes the provenance ruling from Codex Session 53: 180 logical rows resolve to 168 physical executions, exactly twelve Stage-B/Stage-C rows cite selected Stage-A measurements, reused rows never call the construction layer or generator, and their hash/canonical payload remains the immutable Stage-A origin.

I reproduced all four handed-off Git blobs, independently ran the 906-test packet suite, compiled the packet scripts/tests, and accepted two open design decisions: `--mode plan` remains the safe default, and the driver may temporarily import three pure helpers from the Stage-0 script until those helpers gain a third consumer.

The four-file executable state is nevertheless **blocked**. Two no-simulation integration probes reached valid branches the committed tests do not cover:

1. A mixed Stage-A drop/survivor run spends 73 stubbed physical executions and then fails because the report filter excludes the physically executed row from the dropped candidate, causing the ledger completeness check to call that planned result “unplanned.”
2. A Stage-B remEI-0.40 row with one saturated step is measured as gate-failing but still receives a `TESTABLE` verdict and contributes to `CASE_B`; the pre-registered `UNSAFE_LADDER_VALUE` branch is unreachable.

The same review found that persisted logical rows omit the `gate_report`, `n_steps`, and `elapsed_s` already held in memory, that the all-dropped terminal discards the ledger view of spent rollouts, that the `NO_ADMISSIBLE_PROBE` sub-branch distinction is not implemented, and that Stage-C gate reports are computed but never used before construction of the operative null.

I did not edit Claude-owned implementation or tests. I appended the exact block and discriminating correction requirements to the authoritative Phase-2 transcript. The origin-provenance design is approved in substance and does not need redesign; Claude owns the corrected executable state and tests for the next review round.

---

## What I reviewed

Following `AgentPrompt.md`, I read the complete project details, Codex continuity, every Codex-including chat summary, the transcript-monitoring thread, and the append-only Phase-2 delta after the byte-verified Codex Session-53 checkpoint. I also read:

- Claude's `HumanReport54.md`;
- `Playbooks/review-cycle.md` and `Playbooks/reproducibility-packet.md`;
- Protocol P v2.3.3 sections 8–11 and invariants I9–I13;
- all of `protocol_p_results.py` and `run_protocol_p_screen.py`;
- the integration, persistence, reuse, drop, and terminal tests in both new test files; and
- the current commit scope and exact Git blob identities.

The handed-off blobs matched Claude's record:

```text
scripts/utils/protocol_p_results.py   ef197b783290db6f3892f724e9c905b21ca63cdb
scripts/run_protocol_p_screen.py      6c745d073cb1f83b88e5420ba80f787b0f7b5dfe
tests/test_protocol_p_results.py      96b1376ad142ab0445eef04a59554265db49c361
tests/test_protocol_p_driver.py       7a443354ff10c4bcb9ce7696fdc984acf1435245
```

All four were UTF-8 without BOM and pure LF.

---

## Decisions

### Accepted: origin-provenance design

The physical ledger/logical inventory split implements the jointly settled rule correctly on the full clean path:

- 180 logical rows;
- 168 physical executions and distinct provenance stamps;
- twelve explicit reuse references;
- no construction/generator call for a reuse;
- exact Stage-A hash/canonical reuse without relabelling; and
- a selected candidate produced by Stage A, not a planning placeholder.

This approval is **in substance**, not approval of the blocked four-file state.

### Accepted: safe CLI default

`--mode plan` as the default is safer than making an expensive action the implicit path. It audits the input pins, timing, inventory, and budget while running zero rollouts. `--mode execute` remains explicit.

### Accepted: temporary Stage-0 helper imports

`coefficient_vector`, `sensor_config_from_document`, and `verify_text_pins` each have two consumers: their Stage-0 owner and this driver. The earlier extraction convention fires at a real third consumer, so the current import is acceptable. It does not alter Stage 0's no-plant/no-rollout behavior.

### Blocked: mixed Stage-A drop reporting

`run_stage_a` correctly records the first failing rollout and skips the remainder of that candidate. Later, `run_screen` defines reportable Stage-A rows as all rows of surviving candidates. The already-recorded failure row is excluded, then rejected as a surplus ledger entry.

The required full-driver regression state is one dropped first row plus one complete survivor:

```text
physical executions                     73
logical report rows                      85
physical ledger/stamps represented       73 / 73
dropped row provenance/gates persisted   yes
```

### Blocked: I12 is not wired into Stage B/C outcomes

Every rollout produces a `GateReport`, but only Stage A reads `passed`. Stage B therefore cannot reach `UNSAFE_LADDER_VALUE`, and Stage C can feed an unsafe healthy replicate into `Q95_c`. Direct tests of `evaluate_hard_gates` are insufficient; the corrected state needs real-driver tests whose executor returns a failing `PrivilegedRecord`.

### Blocked: persisted evidence and terminal semantics

`PhysicalResult` holds gate evidence, step count, and elapsed time, but `logical_row_report` drops all three. The result document cannot audit I12 or runtime. The terminal path also needs to preserve every spent physical result and distinguish the Protocol-P `NO_ADMISSIBLE_PROBE` integrity branch from its physical safety/method-limit branch.

One non-blocking cleanup was included in the handoff: the `physical_key` docstring still claims integer `1` and float `1.0` hash differently, although Claude's mutation sweep correctly established that Python treats them as equal with equal hashes. The normalization preserves the serialized numeric type, not ledger-key uniqueness.

---

## Verification

```text
full packet suite                         906 passed in 55.13 s
compileall                                clean
mixed Stage-A drop/survivor probe         block reproduced; 73 stub calls
unsafe Stage-B remEI-0.40 probe           terminal=None, CASE_B, TESTABLE
Protocol-P plant rollouts                 zero
Stage-0 artifact                          unchanged; not re-executed
replay                                    not re-run
config.json                               absent
confirmatory test split                   untouched
```

The green suite and the blocks are both real: the suite does not contain the two full-driver states used by the probes.

The transcript append passed the hard gate:

```text
pre-write lines                           13,001
pre-write bytes                           902,416
old-prefix SHA-256                        70b948040836447966ee926d942637a51f59900a326553e69db30d87f87704b6
old prefix after append                   exact
Codex Session-54 header                   exactly once, line 13,005
header after pre-write boundary           yes
transcript diff                           +134 / -0
post-write lines                          13,135
post-write bytes                          908,639
post-write SHA-256                        543758a8de87a5a486ee9d0024dc76018d7756798db11403d26ef17e64c335e5
```

---

## Files created or updated

- `chats/Claude-Codex/Phase 2 Integration and Config Freeze/Phase 2 Integration and Config Freeze - Active.md` — appended the exact-state block, reproduced evidence, accepted design decisions, and owner correction requirements.
- `agents/Codex/Session Summaries/HumanReport54.md` — this report.
- `agents/Codex/README.md` — adds Session 54 and updates the active driver-review routing.
- `agents/Codex/Summary of Only Necessary Context.md` — completely rewritten for the next session.

No public README, implementation module, test, protocol specification, assignment, config, dataset payload, result artifact, or confirmatory material changed in Codex Session 54.

No progress report was due: Session 54 is not an every-eighth session, and no phase transition or approved Claim Sheet amendment occurred. The next regular Codex progress report remains Session 56.

---

## Next steps

1. Claude corrects the mixed-drop ledger/report path, Stage-B unsafe terminal, Stage-C gate wire, persisted gate evidence, and terminal-ledger/classification paths, with full-driver tests.
2. Claude returns an explicitly approved exact state for Codex review. The origin-provenance design remains unchanged.
3. No Stage-A/B/C rollout may run until both agents explicitly approve the same executable state.
4. Config remains unfrozen; Amendment A2, replacement assignment/config lineage, coherent regeneration, Gates 4–7, joint freeze, and one-shot confirmatory generation remain downstream.

— Codex
