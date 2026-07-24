# Summary of Only Necessary Context

## Resume point

This is the authoritative Codex resume state after **Codex Session 31**
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
Codex Session 31
```

Read `AgentPrompt.md` from the beginning before any work. Then read current
project details, this file, every relevant chat summary, and every active chat
containing Codex. The live Phase-2 transcript outranks this handoff if newer
messages exist.

Use only:

```powershell
.\venv\Scripts\python.exe
```

Never use bare `python` or `pip`.

## Current review state

### Closed

- all review loops before Gate 3;
- Gate 1;
- Gate-2 role write/load/join foundation; and
- the corrected **656-reservation** Gate-3 assignment at hash
  `dev-70832daabe7968d55c0bf68e713e945ed48ce167f5c54ec186559b9a660765de`.

Claude explicitly approved that exact corrected state in Session 31. Both
agents therefore closed Gate 3 at that state.

### Reopened by owner amendment

Codex then adopted Claude's optional repeat-budget remedy before any generator
or data existed. Because the assignment is self-hashed, this created a new
state and reopened Gate 3 only for exact-state approval.

Codex owner decision:

```text
APPROVE_GATE3_ASSIGNMENT_V0_1
```

Required Claude response:

```text
APPROVE_GATE3_ASSIGNMENT_V0_1
```

or:

```text
BLOCK_GATE3_ASSIGNMENT_V0_1
```

with file/line-specific findings.

New assignment hash:

```text
dev-eec59ec8a296a9a4ff4909f8e7f1de91a0a8f4bf289ae1533a427d1a87bc33f1
```

Exact amended review-target identities:

```text
Reproducibility Packet/config/proposed-gate3-assignment-v0.1.json
76255a8089f3e27d893b26d981cbf50e808bd75ba518c44b55c4635ec83514ae

Reproducibility Packet/scripts/utils/gate3_assignment.py
01ffba74d8b1da32409ef5cea66ba3f74e551735e9705bfadc2819a456d64814

Reproducibility Packet/tests/test_gate3_assignment.py
fe56cbf49dec4fcaf8ab742b4453896d60990901dcfa584d9606c4e3823ff9eb

Reproducibility Packet/README.md
5b855e0fea57aac770d1a005a0d4a784234f152d523eae555b6113d076b5dfa2
```

Bound draft-config hash remains:

```text
dev-0211f2e71a473fef3c30cd53fd0a269df45156a3d58e83097bac7a5638bf6180
```

Reviewer edits, handoffs, downstream use, and silence are not approval.

## Why the assignment was amended after approval

The corrected 656-reservation state completely removed the earlier
fault-conditioned context leak. Claude's Session-31 consequence audit found a
different, non-blocking limitation:

```text
development/pilot payload = deterministic function of trajectory
```

This occurred because dev and pilot had two realizations per trajectory/fault.
At that budget, pairwise context balance and no-trajectory-alias are
mathematically incompatible. The limitation:

- was confined to development and pilot;
- ran conservatively against S rather than in favor of the hypothesis;
- did not contaminate validation or test; and
- therefore correctly did not block the 656-reservation state.

It still weakened null attribution. If S failed later, training-only payload
aliasing would be a live method-failure alternative to hypothesis failure.
Claude measured the exact remedy: raise dev/pilot realizations from two to
four. Codex accepted the +23% reservation cost because the project prioritizes
evidential clarity over speed and no data had yet been generated.

## Amended Gate-3 design

Realizations per trajectory/fault:

```text
dev    4
pilot  4
val    4
test   8
```

Reservation counts:

```text
dev    152
pilot  152
val    168
test   336
total  808
```

Known/compound fault-setting counts remain:

```text
dev     19
pilot   19
val     21
test    21
```

Projected later four-suite/five-seed manifest:

```text
16,160 rows
```

Projection only. Test reservations materialized: `0`.

The same eight-cell context table remains:

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

Lookup remains:

```text
(trajectory_index * realizations_per_trajectory_fault[split] + replicate) mod 8
```

Fault identity is never an input.

Every fault setting in every split now realizes all eight context cells:

```text
dev    8 cells, once each
pilot  8 cells, once each
val    8 cells, once each
test   8 cells, twice each
```

A new validator invariant also requires every
`(split, trajectory_spec_id, fault_setting_id)` group to vary both profiles on
all three axes:

```text
payload
environment
contact
```

This is separate from and stronger than per-fault distribution equality.

## Independent audit

The Session-31 consequence audit, separate from the validator summary:

```text
dev:   152 rows, 8 cells, I(fault;cell)=0.000000000000 bits,
       0/38 aliased trajectory/fault groups
pilot: 152 rows, 8 cells, I(fault;cell)=0.000000000000 bits,
       0/38 aliased trajectory/fault groups
val:   168 rows, 8 cells, I(fault;cell)=0.000000000000 bits,
       0/42 aliased trajectory/fault groups
test:  336 rows, 8 cells, I(fault;cell)=0.000000000000 bits,
       0/42 aliased trajectory/fault groups
unique scenario IDs: 808/808
```

The old fault/context leak remains exactly zero. The training-only
trajectory-context alias is also gone.

## Assignment contents unchanged by the amendment

The proposal still:

- is `status=proposed`;
- requires `PENDING_JOINT_APPROVAL_GATE3_ASSIGNMENT_V0_1`;
- forbids research and test payload generation;
- predeclares `dev`, `pilot`, `val`, and `test`;
- carries two split-exclusive trajectories per split;
- includes ordinary and diagnostic excitation in every split;
- covers the complete onset-plus-five-second window;
- uses the tracked 0.05 N, 0.8 Hz, one-cycle raised-cosine probe;
- assigns whole trajectory, fault-setting, and split-group identities;
- includes 19 known settings per split;
- includes two compound/OOD settings in validation and two in test;
- owns payload, temperature/environment, and endpoint-contact profiles by split;
- carries five model-training seeds;
- assigns deterministic simulation/fault/sensor/controller seed tuples; and
- keeps C1/S common-random-number pairing across every declared field.

Structural location remains executable zero-based `1`, the second compliant
link. Compound/OOD rows remain excluded from known four-way metrics.

## Verification state

Final Session-31 results from the repository virtual environment:

```text
focused Gate-3 tests: 20 passed in 0.16s
full packet suite: 378 passed in 8.86s
compileall: pass
CLI help: pass
read-only validator: pass
canonical assignment hash recomputation: exact match
independent context audit: pass
git diff --check: pass
research generation allowed: false
test generation allowed: false
test reservations materialized: 0
```

No final `config.json`, data directory, manifest, payload, or model fit exists.

Run from `Reproducibility Packet/`:

```powershell
..\venv\Scripts\python.exe -m pytest tests\test_gate3_assignment.py -q
..\venv\Scripts\python.exe -m pytest tests\ -q
..\venv\Scripts\python.exe scripts\validate_gate3_assignment.py
```

## Authorization boundary

The 656-reservation approval does not authorize substituting the amended
808-reservation state. Until Claude explicitly approves the new hash, do not:

- embed the assignment in the draft config;
- recompute the draft config around this assignment;
- start assignment-driven generation;
- materialize any research or test payload;
- fit a headline model; or
- claim Gate 3 is closed at the amended state.

After exact-state approval, authorized next work is:

1. embed the exact amended assignment under `values.scenario_manifest`;
2. remove only the Gate-3 item from the draft open-gate list;
3. recompute the draft-config hash;
4. update the assignment's bound draft-config hash and self-hash coherently if
   the embedding protocol requires the assignment to point at the new draft;
5. build the real assignment-driven generator; and
6. generate/audit dev, pilot, and validation roles only.

The potential draft/assignment circular hash binding must be resolved
deliberately rather than by editing one hash after the other. Inspect the
config-contract and assignment-contract semantics before embedding.

Still unauthorized:

- final `Reproducibility Packet/config.json`;
- confirmatory generation;
- any test identity or payload materialization;
- headline fitting before the live role-complete data/audit gate;
- claiming Gate 2 complete;
- claiming validation or confirmatory evidence.

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
- non-test supervised join; and
- synthetic role-complete contract fixture.

Still required:

- amended Gate-3 exact-state approval;
- real assignment-driven multi-setting MuJoCo generator;
- generated-data role-completeness and leakage audit.

### Gate 3

The 656-reservation corrected state was jointly approved, then intentionally
superseded before generation. The 808-reservation owner-amended candidate is
**OPEN** pending Claude's explicit same-state approval.

### Gates 4–7

Remain open. Claude's model/calibration/evaluation lane waits on the live
Gate-2 data layout after assignment approval.

Gate 6 remains the in-contract four-arm protocol:

- no-action/detection-only;
- transparent attribution-driven;
- RMA; and
- oracle.

Do not narrow to information-only or retune blocked action families outside the
Claim Sheet.

Gate 7 must report the paired C1-vs-S contrast at pilot, validation, and test.
Because the four-repeat amendment removes the dev/pilot alias, the pilot-to-val
step no longer changes alias structure and confound severity simultaneously.

## Immediate next steps

Session 32 should:

1. read the live transcript tail and exact amended target files;
2. inspect Claude's response to assignment hash
   `dev-eec59ec8a296a9a4ff4909f8e7f1de91a0a8f4bf289ae1533a427d1a87bc33f1`;
3. close Gate 3 only if the approval token is explicit and the exact state is
   unchanged;
4. otherwise address supported file/line findings and re-hand off;
5. after approval, inspect the config/assignment hash-binding lifecycle before
   embedding;
6. embed the approved assignment and recompute a coherent draft hash;
7. implement distal payload mass, split-owned environment, contact-window
   scheduling, and compound plant-plus-sensor realization;
8. drive persisted roles through `DatasetRoleBuilder`;
9. run the complete generated-data role/leakage audit while draft-state test
   refusal remains active; and
10. keep final config, headline fitting, and test materialization blocked.

Session 32 also requires the regular Codex progress report.

## Durable claim boundaries

- A proposed or approved assignment is not a frozen config.
- A deterministic reservation is not generated data.
- A synthetic fixture is not research evidence.
- A development screen is not validation or confirmatory evidence.
- Detection, attribution, information authorization, action authorization, and
  control outcome remain distinct.
- Fault improvement is not source-specific recovery without the matched healthy
  false-authorization gate.
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

Session-31 physical state:

```text
pre-session lines: 2948
final lines: 3037
session delta: +89 / -0
new header: line 2952, exactly once
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

The root Live-Run log received one append-only entry stating that the approved
blueprint was reopened before generation to remove the training alias. The
entry records the 808-reservation cost, the new review gate, no data generation,
untouched test, and unfrozen config.

`.gitignore` was reviewed and did not need a change.

Detailed record:

```text
agents/Codex/Session Summaries/HumanReport31.md
```
