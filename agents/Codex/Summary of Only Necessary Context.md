# Summary of Only Necessary Context

## Resume point

This is the authoritative Codex resume state after **Codex Session 30**
(2026-07-24).

Current phase:

```text
Phase 2 — Integration and Reproducibility Build
```

Current final-config state:

```text
UNFROZEN
BLOCK_CONFIG_FREEZE_PENDING_PRECONFIRMATORY_BUILD_AND_VALIDATION
```

Expected closeout commit:

```text
Codex Session 30
```

Read `AgentPrompt.md` from the beginning before any work. Then read current
project details, this file, every relevant chat summary, and every active chat
containing Codex. The live Phase-2 transcript outranks this handoff if newer
messages exist.

Use only the repository virtual environment:

```powershell
.\venv\Scripts\python.exe
```

Never use bare `python` or `pip`.

## Current review state

### Closed

- all review loops before Gate 3;
- Gate 1;
- Gate-2 role write/load/join foundation.

### Open

Claude exact-state review of the corrected Gate-3 assignment.

Codex replacement owner decision:

```text
APPROVE_GATE3_ASSIGNMENT_V0_1
```

Required reviewer response:

```text
APPROVE_GATE3_ASSIGNMENT_V0_1
```

or:

```text
BLOCK_GATE3_ASSIGNMENT_V0_1
```

with file/line-specific findings.

Replacement assignment hash:

```text
dev-70832daabe7968d55c0bf68e713e945ed48ce167f5c54ec186559b9a660765de
```

Exact replacement file identities:

```text
Reproducibility Packet/config/proposed-gate3-assignment-v0.1.json
dcee3e6c9d52f7d36a84c06f0e3b1e5f39e89448c8b81940ca2728d9d9f98192

Reproducibility Packet/scripts/utils/gate3_assignment.py
040cfe15ed6ffd70d9c5be32edfa418f4fb0ba98606e2dd7d85eb2f898897cef

Reproducibility Packet/tests/test_gate3_assignment.py
e4749f67a98033b7d6e8223e8dad4c885b60ee96d9eac57f65910cbf270c1c9d
```

Bound draft-config hash:

```text
dev-0211f2e71a473fef3c30cd53fd0a269df45156a3d58e83097bac7a5638bf6180
```

The Session-29 assignment hash
`dev-5939ff5f1f0cc29f75bb4abcd027dbe6ffe84844ad7727ac1e75ca9a0220cedb`
is superseded and must not be approved, embedded, or treated as current.

Reviewer edits, handoffs, downstream use, and silence are not approval. If
Claude changes any review-target file, inspect and approve the actual new state
before closing the loop.

## Why Session 29 was blocked

The original deterministic context rotation used `fault_index` while every
split had two payload, environment, and contact profiles. Under modulo 2:

```text
payload XOR environment = fault_index mod 2
```

That locked payload/environment alignment to fault identity in all 80 fault
settings and transferred the same polarity from development into test.
Temperature is visible through S-only gauge strain, and payload is especially
legible in structural channels, so the shortcut could inflate paired S-minus-C1
macro-F1 in the direction of the hypothesis.

Claude returned:

```text
BLOCK_GATE3_ASSIGNMENT_V0_1
```

with a tested balanced-table remedy. Codex reproduced the leak and accepted the
finding.

## Corrected Gate-3 context assignment

The replacement self-hashed assignment carries this exact context-cell table,
in `(payload_index, environment_index, contact_index)` order:

```text
(0,0,0)
(0,1,1)
(1,0,1)
(1,1,0)
(0,0,1)
(0,1,0)
(1,0,0)
(1,1,1)
```

Lookup is:

```text
(trajectory_index * realizations_per_trajectory_fault[split] + replicate) mod 8
```

Fault identity is never an input.

Every split must carry exactly two profiles on each context axis. The validator
fails unless every fault setting within a split receives the identical
context-cell **count distribution**.

Realized distributions:

```text
dev    4 unique cells, each once per fault
pilot  4 unique cells, each once per fault
val    8 unique cells, each once per fault
test   8 unique cells, each twice per fault
```

This removes the fault-conditioned context cue and increases validation/test
coverage to the complete eight-cell factorial.

## Gate-3 assignment contents

The proposal remains separate from the tracked draft config. Its lifecycle is:

```text
status=proposed
decision=PENDING_JOINT_APPROVAL_GATE3_ASSIGNMENT_V0_1
research_payload_generation_allowed=false
test_payload_generation_allowed=false
```

It predeclares:

- splits `dev`, `pilot`, `val`, `test`;
- two split-exclusive trajectories per split;
- ordinary and diagnostic excitation in every split;
- bounded finite tasks covering the complete onset-plus-five-second window;
- tracked diagnostic proposal: 0.05 N, 0.8 Hz, one raised-cosine cycle;
- whole `trajectory_spec_id`, `fault_setting_id`, and `split_group_id`
  ownership;
- 19 known settings per split;
- two compound/OOD settings in validation and two in test;
- split-owned payload, temperature/environment, and endpoint-contact profiles;
- five model-training seeds:
  `31001, 31002, 31003, 31004, 31005`;
- deterministic simulation/fault/sensor/controller seed tuples; and
- C1/S common-random-number pairing across every declared field.

Structural location uses executable zero-based `1`, meaning the second
compliant link. `CablePlant` rejects structural location `2`. Do not regress
this identity convention.

Compound/OOD rows use the first component as the schema-compatible primary
label, retain full components in the non-deployable assignment, set
`compound_flag=true` and `ood_flag=true`, and are excluded from known four-way
metrics.

Counts:

```text
dev     76
pilot   76
val    168
test   336
total  656
```

Known/compound fault-setting counts:

```text
dev     19
pilot   19
val     21
test    21
```

Projected later four-suite/five-seed manifest:

```text
13,120 rows
```

Projection only. Test reservations materialized: `0`.

## Verification state

Final Session-30 results from the repository virtual environment:

```text
focused Gate-3 tests: 18 passed in 0.12s
full packet suite: 376 passed in 8.73s
compileall: pass
CLI help: pass
read-only validator: pass
canonical assignment hash recomputation: exact match
context-cell distributions: identical per fault, 4/4/8/8 unique
reservations: 656
test reservations materialized: 0
research generation allowed: false
test generation allowed: false
```

Run from `Reproducibility Packet/`:

```powershell
..\venv\Scripts\python.exe -m pytest tests\test_gate3_assignment.py -q
..\venv\Scripts\python.exe -m pytest tests\ -q
..\venv\Scripts\python.exe scripts\validate_gate3_assignment.py
```

No manifest or payload was written by the validator. No final `config.json`
exists.

## Lifecycle boundary

Claude's exact-state Gate-3 approval would authorize:

1. embedding the exact approved replacement assignment in
   `values.scenario_manifest`;
2. recomputing the draft config hash; and
3. building the missing real generator paths against that exact assignment.

It would **not** authorize:

- creating final `Reproducibility Packet/config.json`;
- confirmatory generation;
- test materialization;
- headline model fitting;
- claiming Gate 2 complete;
- claiming validation or confirmatory evidence.

The tracked draft remains:

- `Reproducibility Packet/config/draft-config-v0.1.json`;
- `status=draft`;
- `confirmatory=False`;
- Gates 2–7 open.

## Gate map

### Gate 1

Jointly approved complete.

### Gate 2

Still **BLOCKED overall**.

Completed:

- machine schema;
- draft/frozen lifecycle;
- path-free identity manifest and role indexes;
- whole-group/CRN audits;
- suite-scoped deployable loader;
- manifest-bound writers/loaders;
- non-test supervised join;
- synthetic role-complete contract fixture.

Still required:

- joint Gate-3 assignment approval;
- real assignment-driven multi-setting MuJoCo generator;
- generated-data role-completeness and leakage audit.

### Gate 3

Corrected review candidate exists. Gate remains **OPEN** pending Claude's
explicit same-state approval of the replacement hash.

### Gates 4–7

Remain open. Claude's model/calibration/evaluation lane waits on Gate 3.
Toolchain readiness (`torch==2.11.0+cu128`, RTX 5060 Ti, `sm_120`) is not
model-fit authorization.

Gate 6 remains the in-contract four-arm controller protocol:

- no-action/detection-only;
- transparent attribution-driven;
- RMA;
- oracle.

Do not narrow the project to information-only and do not silently retune a
blocked action family outside the Claim Sheet.

Claude proposed a Gate-7 interpretation rule that Codex accepted: report the
paired C1-vs-S contrast at pilot, validation, and test; distinguish a contrast
that decays as confounds become more extreme from one absent at every rung.
This is agreed direction for the future Gate-7 driver, not an implemented or
frozen artifact.

## Immediate next steps

Session 31 should:

1. read the live Phase-2 transcript tail and actual replacement target files;
2. inspect Claude's exact response to hash
   `dev-70832daabe7968d55c0bf68e713e945ed48ce167f5c54ec186559b9a660765de`;
3. close Gate 3 only if the approval token is explicit and the exact state is
   unchanged;
4. otherwise address supported file/line findings and re-hand off the exact
   corrected state;
5. only after joint approval, embed the assignment into the draft config and
   recompute the draft hash;
6. implement distal payload mass, split-owned environment, contact-window
   scheduling, and compound plant-plus-sensor realization;
7. drive all persisted roles through `DatasetRoleBuilder`;
8. run the complete generated-data role/leakage audit while draft-state test
   refusal remains active;
9. keep headline fitting and test materialization blocked; and
10. keep final `config.json` absent until every later freeze gate closes.

The next regular Codex progress report is Session 32.

## Durable claim boundaries

- A proposed assignment is not a frozen config.
- A deterministic reservation is not generated data.
- A synthetic fixture is not research evidence.
- A development screen is not validation or confirmatory evidence.
- Detection, attribution, information authorization, action authorization, and
  control outcome remain distinct.
- Fault improvement is not source-specific recovery unless it clears the
  matched healthy false-authorization gate.
- A1 safety is hard.
- Physical truth, observations, labels, estimator state, and controller
  authorization remain role-separated.
- Test remains untouched until after complete final freeze.

## Transcript append hard gate

Authoritative live chat:

```text
chats/Claude-Codex/Phase 2 Integration and Config Freeze/
Phase 2 Integration and Config Freeze - Active.md
```

Session-30 physical state:

```text
pre-session lines: 2765
final lines: 2855
session delta: +90 / -0
last line: — Codex
```

For every future append:

1. read the physical UTF-8 tail;
2. record the pre-write line count;
3. verify a complete multi-line EOF anchor is unique;
4. use `apply_patch` only against that exact anchor;
5. verify the new header occurs exactly once after the boundary;
6. verify the new signature is physically last; and
7. require `git diff --numstat` to show additions only.

No transcript-order recurrence occurred this session.

## Public status and closeout

The root `README.md` was intentionally unchanged. Claude Session 30 already
logged the noteworthy blocked pre-registration and its evidence boundary. The
replacement assignment remains inside an open review loop, so another entry
would be premature and would bloat the lean append-only log.

`.gitignore` was reviewed and did not need a change.

Detailed record:

```text
agents/Codex/Session Summaries/HumanReport30.md
```
