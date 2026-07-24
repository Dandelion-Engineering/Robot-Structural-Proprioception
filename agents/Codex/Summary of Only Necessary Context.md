# Summary of Only Necessary Context

**Last completed Codex session:** 27
**Next Codex session:** 28
**Expected next commit message:** `Codex Session 28`
**Project phase:** Phase 2 — Integration and Reproducibility Build
**Final config state:** **UNFROZEN**
**Governing decision:** `BLOCK_CONFIG_FREEZE_PENDING_PRECONFIRMATORY_BUILD_AND_VALIDATION`

## Resume from live sources

Follow `AgentPrompt.md` from the beginning. Before substantive work, read:

1. `Project Details/Project Details.md`;
2. this file;
3. all Codex chat summaries;
4. the complete physical tail/current state of every active Codex chat;
5. Claude's latest human report and continuity summary; and
6. the actual repository state.

Authoritative technical thread:

- `chats/Claude-Codex/Phase 2 Integration and Config Freeze/Phase 2 Integration and Config Freeze - Active.md`

At Codex Session-27 closeout it had 2,502 physical UTF-8 lines. Codex's last header was:

- `**Codex (Session 27, 2026-07-23 19:26 PDT):**` at line 2,494.

Do not assume this remains the tail. Claude may append or change implementation after closeout.

## Current review state

### Open: Gate-1 / Gate-2-foundation implementation

Codex Session 27 implemented and handed Claude the exact state of:

- root `.gitattributes` (one LF rule for the byte-hashed schema);
- `Reproducibility Packet/schema/schema.json`;
- `Reproducibility Packet/config/draft-config-v0.1.json`;
- `Reproducibility Packet/scripts/utils/config_contract.py`;
- `Reproducibility Packet/scripts/utils/storage_contract.py`;
- `Reproducibility Packet/scripts/validate_data_contract.py`;
- `Reproducibility Packet/tests/test_data_contract.py`;
- packet runbook and shared-utils documentation.

Requested response:

- `APPROVE_GATE1_GATE2_FOUNDATION`; or
- `BLOCK_GATE1_GATE2_FOUNDATION` with a specific mismatch.

Codex owner assessment:

- **Gate 1 implementation is complete pending Claude's review.**
- **Gate 2 remains BLOCKED overall.**

The Gate-2 foundation now covers the identity manifest, exact role indexes, suite-scoped deployable observation loading, and core split/leakage/path/hash/mask/dtype/timing audits. It does **not** yet include the live multi-setting manifest/data builder, allowlisted supervised training join, non-observation role payload builders/evaluators, or end-to-end generator.

If Claude explicitly approves the exact unchanged state, acknowledge and close the loop. If Claude edits files, inspect the actual diff and perform genuine owner re-review. Edits, downstream use, and silence are not approval.

### Closed: config-freeze readiness review

Claude Session 27 explicitly approved the exact Session-26 state of:

- `agents/Codex/Config Freeze Readiness Review.md`

Codex acknowledged that approval. The loop is closed, but its decision remains:

- `BLOCK_CONFIG_FREEZE_PENDING_PRECONFIRMATORY_BUILD_AND_VALIDATION`

Closing review authorized the implementation backlog; it did not authorize a final config freeze.

## Shared decisions now in force

### Gate-6 controller governance

Run the in-contract four-arm comparison:

- no-action/detection-only;
- transparent attribution-driven;
- RMA; and
- oracle.

Do not narrow the experiment to information-only and do not retune the blocked action families post hoc. An information-only scope would require an amendment; no such amendment is being taken.

### Gate-3 pre-fit checkpoint

The complete scenario/fault/trajectory assignment manifest requires explicit Claude/Codex same-state approval **before any headline model is fit**. This checkpoint must cover the multi-setting grids, compound/OOD holdout, trajectories, payloads, environment/contact profiles, onsets/excitation roles, whole-group splits, and seeds.

It is distinct from the later final immutable config freeze.

### Gate-4 environment

Claude Session 27 recorded a successful CUDA build:

- `torch==2.11.0+cu128`;
- RTX 5060 Ti recognized;
- `sm_120` kernel and autograd verified.

This removes the toolchain uncertainty only. It does not authorize model fitting before the Gate-3 assignment approval.

## Session-27 foundation state

### Machine schema and config

`schema/schema.json` renders schema v1.0 + A1 with exact roles, dtypes, shapes, units, availability, fixed registry/masks, A1 field order, sparse estimator-decision persistence, indexes, and invariants.

The root `.gitattributes` pins this byte-hashed schema file to LF so its hash is stable across Windows, Linux, archives, and fresh clones.

`severity_uncertainty` remains a `config_defined_nonnegative_error_scale`. Gate 5 still owns the exact reviewed statistic.

The tracked draft:

- is named `config/draft-config-v0.1.json`;
- has `status=draft`;
- reports `confirmatory=False`;
- has hash `dev-0211f2e71a473fef3c30cd53fd0a269df45156a3d58e83097bac7a5638bf6180`;
- keeps Gates 2–7 explicit;
- retains unresolved design/model/calibration/evaluation objects as open; and
- cannot authorize confirmatory work.

No `config.json` exists.

The validator rejects draft, wrong-name, wrong-schema, partial/null/empty, hash-mismatched, development-marked, or non-approved frozen-shaped state for confirmatory callers. A frozen state requires the exact decision `APPROVE_CONFIG_FREEZE`, zero open gates, no `dev-` values, complete required objects, and a raw canonical 64-hex hash.

### Storage and leakage boundary

The schema-A identity manifest and role indexes enforce:

- one complete rollout per `run_id`;
- one config identity;
- whole-pair, trajectory, fault-setting, and split-group assignments;
- C1/S CRN and protocol agreement;
- safe path-free identities and role-relative `.npz` paths;
- exact index headers and SHA-256 values.

The deployable loader receives one `observations/<suite>` root. It rejects shared/sibling roots, identity or target columns, label/privileged/extra payload fields, traversal, wrong identities, hash tampering, unavailable-channel values, mask/order violations, dtype drift, and causal-latency inconsistency.

## Verification

Use only `.\venv\Scripts\python.exe`.

Session-27 results:

```text
Config OK: status=draft, config_hash=dev-0211f2e71a473fef3c30cd53fd0a269df45156a3d58e83097bac7a5638bf6180, confirmatory=False
18 passed in 0.17s
347 passed in 8.57s
```

The full packet test command was:

```powershell
..\venv\Scripts\python.exe -m pytest tests\ -q
```

run from `Reproducibility Packet/`.

## Next implementation sequence

After closing or correcting the open foundation review:

1. finish Gate 2 with the live data/manifest builder, allowlisted supervised join, role writers/evaluators, and end-to-end audits;
2. draft the complete Gate-3 multi-setting assignment;
3. obtain explicit same-state approval of that assignment before headline fitting;
4. implement and validation-select the matched temporal/RMA models, capacity ladder, calibration, OOD, abstention, and uncertainty rules;
5. complete the four-arm controller protocol and final sample-size decision;
6. jointly freeze the complete immutable `config.json`;
7. generate/evaluate untouched confirmatory roles; and
8. proceed to Phase-3 statistics and artifacts.

`test` roles remain untouched until after the complete final freeze.

## Durable claim boundaries

- Development screens are not confirmatory results.
- A draft hash or shared candidate is not a frozen config.
- Detection, attribution, information authorization, action authorization, and control outcome are distinct.
- Fault improvement is not source-specific recovery unless it clears the matched healthy false-authorization gate.
- A1 safety is hard.
- The sampled probability envelope is not a continuous proof.
- Physical truth, observations, targets, estimator state, and controller authorization remain role-separated.
- The current foundation is infrastructure, not a research result.

## Transcript append hard gate

For every append to the active Phase-2 transcript:

1. read the physical UTF-8 tail;
2. record the pre-write line count;
3. verify the complete multi-line EOF anchor is unique;
4. use `apply_patch` only against that exact anchor;
5. verify the new header occurs exactly once after the boundary; and
6. require `git diff --numstat` to show `+N/-0`.

Session-27 transcript delta was `+58/-0`. No recurrence was logged in transcript-order monitoring.

## Public and closeout boundary

- Root `README.md` was intentionally unchanged: the foundation is awaiting review, changes no scientific result, and is not a phase transition.
- `.gitignore` required no change; `.gitattributes` contains only the LF rule for the byte-hashed machine schema.
- Next regular Codex progress report is Session 32.
- Read `agents/Codex/Session Summaries/HumanReport27.md` for the detailed implementation and audit record.
