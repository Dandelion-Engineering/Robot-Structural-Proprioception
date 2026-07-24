# Summary of Only Necessary Context

## Resume point

This is the authoritative Codex resume state after **Codex Session 29**
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
Codex Session 29
```

Read `AgentPrompt.md` from the beginning before any work. Then read the current
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

- all earlier same-state review loops;
- Gate-1 / Gate-2 foundation review;
- Gate-2 role write/load/join review.

Claude Session 29 explicitly returned:

```text
APPROVE_GATE2_ROLE_WRITE_PATH
```

for the exact unchanged Session-28 target. Codex accepted it in the live
transcript. The generic manifest-bound role writers/loaders, non-test supervised
join, and deterministic contract fixture are jointly approved.

This does **not** complete Gate 2. The real Gate-3-driven multi-setting MuJoCo
generator and its generated-data role/leakage audit remain missing.

### Open

Claude review of the exact Gate-3 assignment candidate.

Codex owner decision:

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

Exact assignment hash:

```text
dev-5939ff5f1f0cc29f75bb4abcd027dbe6ffe84844ad7727ac1e75ca9a0220cedb
```

Replacement review-target code hashes:

```text
scripts/utils/gate3_assignment.py
8d095fea5c86f421634af95b347df370567606f7b0a86f315d9929640c0c1880

tests/test_gate3_assignment.py
00ea52fcf30bf59cfcbf02cdc7999ee7172db6eaa138453db7a5247d17f3569b
```

Bound draft-config hash:

```text
dev-0211f2e71a473fef3c30cd53fd0a269df45156a3d58e83097bac7a5638bf6180
```

The 10:23 owner handoff was explicitly superseded because the two code files
above received final defensive checks afterward. The 10:29 transcript message
is the binding replacement owner handoff. Reviewer edits, handoffs, downstream
use, and silence are not approval. If Claude changes any target file, inspect
and approve the actual new state before closing the loop.

## Gate-3 assignment review target

Primary files:

- `Reproducibility Packet/config/proposed-gate3-assignment-v0.1.json`
- `Reproducibility Packet/scripts/utils/gate3_assignment.py`
- `Reproducibility Packet/scripts/validate_gate3_assignment.py`
- `Reproducibility Packet/tests/test_gate3_assignment.py`

Ancillary exact-state documentation:

- Step 2B and Current boundary in `Reproducibility Packet/README.md`
- `gate3_assignment` entry in
  `Reproducibility Packet/scripts/utils/__init__.py`

The proposal is deliberately separate from the tracked draft config. Its state
is:

```text
status=proposed
decision=PENDING_JOINT_APPROVAL_GATE3_ASSIGNMENT_V0_1
research_payload_generation_allowed=false
test_payload_generation_allowed=false
```

The validator expands reservations in memory only. It writes no manifest,
research payload, or test payload.

## What the assignment fixes

### Split and trajectory ownership

- splits: `dev`, `pilot`, `val`, `test`;
- two split-exclusive trajectories per split;
- one ordinary and one diagnostic trajectory per split;
- bounded finite tasks covering the complete onset-plus-five-second window;
- tracked diagnostic proposal: 0.05 N, 0.8 Hz, one raised-cosine cycle;
- suite is never an input to split assignment;
- whole `trajectory_spec_id`, `fault_setting_id`, and `split_group_id` ownership.

### Fault grid

Every split has 19 known settings:

- healthy;
- two structural severities;
- two actuator severities at joints 0 and 1;
- two encoder-bias severities at joints 0 and 1;
- two encoder-drift severities at joints 0 and 1;
- two encoder-dropout severities at joints 0 and 1.

No exact known fault tuple is reused across splits.

Structural location uses the executable zero-based value `1`, meaning the
selected second compliant link. `CablePlant` rejects structural location `2`.
Do not regress this identity convention.

Validation and test each add two cross-source compound/OOD settings. The first
component supplies the schema-compatible primary label; the full components
remain in the non-deployable assignment. `compound_flag=true` and
`ood_flag=true`. OOD rows are excluded from known four-way metrics and enter
only abstention/unknown/OOD metrics.

### Confounds and seeds

Each split owns:

- two distal payload masses;
- two temperature/environment profiles; and
- no-contact plus one split-specific contact-window profile at plane z = 0.200 m.

The real generator does not yet implement all assigned payload,
contact-window, environment, or compound-fault paths. Those are explicit
post-approval requirements, not generated evidence.

The proposal has five model-training seeds:

```text
31001, 31002, 31003, 31004, 31005
```

Reservations use deterministic simulation/fault/sensor/controller seed tuples
and context rotation. C1 and S must share every declared common-random-number
field within each matched suite/seed pair.

### Counts

Expanded suite-independent reservations:

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

This is a projection only. Test reservations materialized: `0`.

## Lifecycle boundary

Joint Gate-3 approval would authorize:

1. embedding the exact approved assignment in
   `values.scenario_manifest`;
2. recomputing the draft config hash; and
3. building the missing real generator paths against that exact assignment.

It would **not** authorize:

- creating final `Reproducibility Packet/config.json`;
- confirmatory generation;
- any test materialization;
- headline model fitting;
- claiming Gate 2 complete;
- claiming validation or confirmatory evidence.

The complete frozen config remains a later, separate same-state checkpoint.

The tracked draft remains:

- `Reproducibility Packet/config/draft-config-v0.1.json`;
- `status=draft`;
- `confirmatory=False`;
- Gates 2–7 open.

No final `config.json` exists.

## Verification state

Final Session-29 results from the repository virtual environment:

```text
focused Gate-3 tests: 15 passed in 0.13s
full packet suite: 373 passed in 8.93s
compileall: pass
CLI help: pass
read-only validator: pass
assignment hash: valid
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

Historical ignored `.npz` files exist under `tmp/` and dependency sample-data
paths. They predate Session 29. No new assignment manifest, result directory, or
binary payload was created.

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

Complete review candidate exists, but the gate remains **OPEN** pending Claude's
same-state approval of the exact hash above.

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

## Immediate next steps

Session 30 should:

1. read the live Phase-2 transcript tail and actual review-target files;
2. inspect Claude's exact Gate-3 response;
3. close the loop only if the approval token is explicit and the assignment
   hash/state are unchanged;
4. otherwise address supported file/line findings and re-hand off the exact
   corrected state;
5. only after joint approval, embed the approved assignment into the draft
   config and recompute its draft hash;
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

Session-29 physical state:

```text
pre-session lines: 2608
final lines: 2669
session delta: +61 / -0
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

No transcript-order recurrence was logged this session.

## Detailed record

Read:

```text
agents/Codex/Session Summaries/HumanReport29.md
```

The root `README.md` was intentionally unchanged because this is an unreviewed
infrastructure checkpoint, not a public scientific milestone or phase
transition.
