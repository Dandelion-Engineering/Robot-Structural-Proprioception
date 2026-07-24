# Human Report — Codex Session 28

**Current date and time:** 2026-07-23 20:28 PDT
**Phase:** Phase 2 — Integration and Reproducibility Build
**Session role:** Gate-1 review close and bounded Gate-2 role-write implementation
**Final config state:** **UNFROZEN**
**Governing decision:** `BLOCK_CONFIG_FREEZE_PENDING_PRECONFIRMATORY_BUILD_AND_VALIDATION`

## Summary

Claude Session 28 explicitly approved the exact Session-27 Gate-1 / Gate-2-foundation state. I inspected the live transcript and repository, accepted that same-state approval, and closed the review loop. Gate 1 is now jointly approved as complete.

I then advanced Gate 2 with a deliberately bounded storage-contract increment:

- schema-driven, manifest-bound writers for observations and all four non-observation roles;
- hash-checking schema-validating loaders for plant, labels, estimator outputs, and controller logs;
- hard refusal to materialize any `test` assignment while the config is a draft;
- an explicit `dev|pilot|val` supervised join that exposes only one observation suite plus the exact label target;
- a deterministic role-complete synthetic fixture spanning disjoint `dev` and `val` whole-trajectory/fault groups;
- 11 focused adversarial and integration tests; and
- packet runbook and module-index documentation.

The final full packet rerun passes: **358 tests passed in 9.86 seconds**. Two independent fixture builds produced **30/30 byte-identical files**. The fixture manifest contains **0** `test` assignments and its summary records **0** `test` payloads.

This does not complete Gate 2. The fixture is contract infrastructure, not a Gate-3 assignment or research dataset. The real jointly approved Gate-3-assigned, multi-setting MuJoCo generator and its role-completeness audit remain open. No `config.json`, `test` payload, model fit, validation result, or confirmatory artifact was created.

I appended the exact implementation handoff to the authoritative Phase-2 transcript and requested explicit `APPROVE_GATE2_ROLE_WRITE_PATH` or `BLOCK_GATE2_ROLE_WRITE_PATH`. The review loop is open at closeout.

## Context and review loop

I followed `AgentPrompt.md` from the beginning and read:

- all project details;
- prior Codex continuity;
- every Codex chat summary and active transcript;
- Claude's current continuity and Session-28 human report;
- the actual repository and Git state;
- the full active Phase-2 transcript;
- the reproducibility-packet playbook; and
- the approved Gate-1 storage/config implementation that this increment extends.

The repository began clean on `main` at:

```text
b079772 Claude Session 28
```

Claude's live transcript response explicitly approved the exact unchanged Session-27 foundation. It also reaffirmed:

- Gate 1 is complete;
- Gate 2 remains blocked overall;
- the complete Gate-3 assignment requires joint same-state approval before headline fitting;
- Claude's Gate-4/5/7 lane waits on that assignment; and
- no frozen config or confirmatory role exists.

I acknowledged that approval before changing the owner state. This closed the earlier `APPROVE_GATE1_GATE2_FOUNDATION` loop without treating edits, silence, or downstream use as approval.

## Design decision and evidence boundary

The active critical path called for a live multi-setting data builder, role writers, and supervised join. The full real generator cannot be honestly completed yet because its complete Gate-3 scenario/fault/trajectory assignment is intentionally subject to joint preregistration approval.

I therefore separated two layers:

1. **Generic contract layer now implemented**
   - consumes an already assigned path-free manifest;
   - enforces whole-pair identity through the approved manifest auditor;
   - writes exact role roots and indexes;
   - validates schema dtypes, shapes, dimensions, semantics, and hashes;
   - refuses draft-lifecycle `test`;
   - joins labels only to an explicitly selected deployable observation suite and only on `dev|pilot|val`.

2. **Real experiment layer still blocked**
   - chooses the complete multi-setting scenarios, fault grid, trajectories, profiles, splits, and seeds;
   - receives explicit same-state Gate-3 assignment approval;
   - drives the selected MuJoCo plant;
   - audits the generated research dataset across every role;
   - fits and validation-selects the headline models only after that checkpoint.

This preserves useful forward progress without turning a synthetic fixture into data evidence or silently selecting the preregistered assignment.

## Implementation

### Role contract

Created:

- `Reproducibility Packet/scripts/utils/role_contract.py`

The module adds:

- `validate_role_payload`, which enforces the exact machine-schema key set, dtypes, bound dynamic dimensions, and role-specific semantics;
- `RolePayloadWriter`, which binds non-observation payloads to assigned manifest identities and writes exact non-pickled NPZ files plus SHA-256 index rows;
- `ObservationRoleWriter`, which binds `ObservedRecord` instances to the assigned pair, split, suite, and config;
- `RolePayloadLoader`, which checks index identity, safe in-root paths, hashes, keys, schema declarations, and semantics before returning payloads;
- `DatasetRoleBuilder`, which audits the supplied manifest, requires complete C1/S pairs, constructs exact role roots, and refuses any draft-state `test` assignment; and
- `SupervisedTrainingJoin`, which accepts only `dev`, `pilot`, and/or `val`, verifies both observation and label availability, and yields only the observation plus exact label target.

The deployable boundary remains the previously approved `DeployableObservationLoader`. The new join does not attach the manifest, plant payload, provenance, estimator output, or controller log to a training example.

### Role-complete fixture

Created:

- `Reproducibility Packet/scripts/build_data_contract_fixture.py`

The portable CLI builds two complete C1/S pairs:

- one `dev` healthy pair;
- one `val` structural-fault pair;
- disjoint trajectory, fault-setting, and split-group identities;
- deterministic matched pair truth and suite-specific observations;
- plant, labels, observations, estimator outputs, and controller logs;
- exact role indexes and hashes; and
- a strict JSON build summary.

After writing, the CLI reopens and audits every role and exercises both suite-specific supervised joins. It fails if the output root already exists. Its summary states that the output is a development contract fixture only, not a Gate-3 assignment, model fit, validation result, or confirmatory dataset.

### Tests

Created:

- `Reproducibility Packet/tests/test_role_contract.py`

The 11 tests cover:

- role-complete end-to-end fixture generation;
- target-only supervised joining;
- draft-state `test` assignment refusal;
- refusal to allowlist `test` in the training join;
- extra identity/target-leakage fields;
- dtype drift;
- invalid source classes;
- unassigned runs and wrong role roots;
- payload hash tamper;
- invalid class-probability simplexes; and
- noncontiguous controller grids.

### Documentation

Updated:

- `Reproducibility Packet/README.md`
- `Reproducibility Packet/scripts/utils/__init__.py`

The runbook now includes Step 2A for the contract fixture and names every produced role index. Its current-boundary section distinguishes the generic write/load/join path from the still-missing real Gate-3-assigned generator.

The root `README.md` remains unchanged. This is an infrastructure increment awaiting cross-review, not a scientific result, phase transition, or public milestone.

## Verification

Commands used from `Reproducibility Packet/` with the repository virtual environment included:

```powershell
..\venv\Scripts\python.exe -m pytest tests\test_role_contract.py -q
..\venv\Scripts\python.exe -m pytest tests\ -q
..\venv\Scripts\python.exe -m compileall -q scripts tests
..\venv\Scripts\python.exe scripts\build_data_contract_fixture.py --help
..\venv\Scripts\python.exe scripts\build_data_contract_fixture.py --output-root <fresh-run-1>
..\venv\Scripts\python.exe scripts\build_data_contract_fixture.py --output-root <fresh-run-2>
git diff --check
```

Recorded results:

```text
11 passed in 0.32s
358 passed in 9.86s
30 files compared; byte-identical=True
manifest test assignments=0
summary test_payloads=0
compileall=pass
CLI help=pass
git diff --check=pass
```

One verification command initially looked for `manifest.json`, while the approved contract correctly writes `manifest.csv`. PowerShell reported that missing path as a non-terminating error, so the derived count from that attempt was not accepted as evidence. I corrected the check to import the actual `manifest.csv`; it contains four rows and zero `test` assignments.

No fixture output was written into the repository. At closeout:

- `Reproducibility Packet/config.json` is absent;
- the repository contains zero `.npz` files;
- no secret, credential, virtual environment, or generated binary artifact was introduced; and
- `.gitignore` requires no change.

## Active transcript and append-only verification

Updated:

- `chats/Claude-Codex/Phase 2 Integration and Config Freeze/Phase 2 Integration and Config Freeze - Active.md`

The first append acknowledged Claude's exact approval and closed the Gate-1 foundation loop. The second handed off the bounded Gate-2 write path with its evidence boundary and requested explicit same-state review.

For both appends I used the transcript hard gate:

1. read the physical UTF-8 tail;
2. recorded the pre-write line count;
3. verified a complete multi-line EOF anchor occurred exactly once;
4. patched only against that exact anchor;
5. confirmed the new header occurred once after the recorded boundary;
6. confirmed the new message was physically last; and
7. required a pure-addition transcript diff.

The final Session-28 transcript state is:

```text
physical lines: 2575
last Codex header: line 2551
session transcript delta: +40 / -0
```

No transcript-order recurrence occurred, so the separate monitoring chat was not changed.

## Files created

- `Reproducibility Packet/scripts/build_data_contract_fixture.py`
- `Reproducibility Packet/scripts/utils/role_contract.py`
- `Reproducibility Packet/tests/test_role_contract.py`
- `agents/Codex/Session Summaries/HumanReport28.md`

## Files updated

- `Reproducibility Packet/README.md`
- `Reproducibility Packet/scripts/utils/__init__.py`
- `chats/Claude-Codex/Phase 2 Integration and Config Freeze/Phase 2 Integration and Config Freeze - Active.md`
- `agents/Codex/README.md`
- `agents/Codex/Summary of Only Necessary Context.md`

## Files deliberately not changed

- `Reproducibility Packet/config.json` — absent; final freeze remains blocked.
- Root `README.md` — no reviewed public milestone or scientific result.
- `.gitignore` — no new tracked generated or sensitive material.
- Approved Gate-1 authority files — unchanged in this increment.
- Gate-3 assignment and every `test` role — remain untouched.
- Headline attribution/RMA models — fitting remains unauthorized before Gate-3 same-state approval.

## Review state at closeout

### Closed

- config-freeze readiness review;
- Gate-1 / Gate-2-foundation implementation review;
- all earlier recorded same-state review loops.

### Open

- Claude review of the exact Gate-2 role write/load/join state.

Requested response:

- `APPROVE_GATE2_ROLE_WRITE_PATH`; or
- `BLOCK_GATE2_ROLE_WRITE_PATH` with file/line findings.

Current owner state is `APPROVED_BY_CODEX`. Reviewer edits, handoffs, downstream use, and silence are not approval. If Claude edits the implementation, Codex must inspect and approve the actual new state.

## Next-session instructions

Codex Session 29 should:

1. follow `AgentPrompt.md` from the beginning;
2. read the physical tail of the active Phase-2 transcript and actual repository state;
3. inspect Claude's exact response to the Gate-2 role-write handoff;
4. if Claude approves the unchanged state, explicitly close the loop;
5. if Claude edits or blocks it, perform genuine owner re-review and address supported file/line findings;
6. prepare the complete Gate-3 multi-setting assignment as a reviewable preregistration artifact;
7. obtain explicit same-state approval of that assignment before any headline model fit or real assigned dataset generation;
8. keep `config.json` absent and all `test` roles untouched;
9. preserve the four-arm controller protocol and development/confirmatory claim boundaries; and
10. continue toward the real multi-setting MuJoCo generator only through the approved assignment.

The next regular Codex progress report is Session 32.

## Commit target

The mandated exact closeout commit is:

```text
Codex Session 28
```

Before commit and push, rerun final packet, transcript, diff, staging, and no-generated-artifact hygiene.
