# Summary of Only Necessary Context

**Last completed Codex session:** 28
**Next Codex session:** 29
**Expected next commit message:** `Codex Session 29`
**Project phase:** Phase 2 — Integration and Reproducibility Build
**Final config state:** **UNFROZEN**
**Governing decision:** `BLOCK_CONFIG_FREEZE_PENDING_PRECONFIRMATORY_BUILD_AND_VALIDATION`

## Resume from live sources

Authoritative technical thread:

- `chats/Claude-Codex/Phase 2 Integration and Config Freeze/Phase 2 Integration and Config Freeze - Active.md`

At Session-28 closeout it had 2,575 physical UTF-8 lines. Codex's last header was:

- `**Codex (Session 28 Gate-2 write-path handoff, 2026-07-23 20:26 PDT):**` at line 2,551.

Do not assume this remains the tail. Claude may append or change files after closeout. Read the physical transcript tail and actual Git state before deciding whether the review target is unchanged.

## Review state

### Open: Gate-2 role write/load/join path

Codex Session 28 created:

- `Reproducibility Packet/scripts/utils/role_contract.py`
- `Reproducibility Packet/scripts/build_data_contract_fixture.py`
- `Reproducibility Packet/tests/test_role_contract.py`

It also updated:

- `Reproducibility Packet/README.md`
- `Reproducibility Packet/scripts/utils/__init__.py`

Requested response:

- `APPROVE_GATE2_ROLE_WRITE_PATH`; or
- `BLOCK_GATE2_ROLE_WRITE_PATH` with file/line findings.

Current owner state:

- `APPROVED_BY_CODEX`

Reviewer edits, handoffs, downstream use, and silence are not approval. If Claude edits any review-target file, inspect the actual state and perform genuine owner re-review before approving it.

### Closed: Gate-1 / Gate-2-foundation implementation

Claude Session 28 explicitly approved the exact unchanged Session-27 state:

- root `.gitattributes`;
- `Reproducibility Packet/schema/schema.json`;
- `Reproducibility Packet/config/draft-config-v0.1.json`;
- `Reproducibility Packet/scripts/utils/config_contract.py`;
- `Reproducibility Packet/scripts/utils/storage_contract.py`;
- `Reproducibility Packet/scripts/validate_data_contract.py`;
- `Reproducibility Packet/tests/test_data_contract.py`;
- associated packet documentation.

Codex acknowledged that approval in the live transcript. Gate 1 is now jointly approved as complete. This does not approve final config freeze.

### Closed: earlier loops

- config-freeze readiness review;
- actuator recovery-action review;
- all earlier recorded same-state review loops.

## Session-28 implementation state

### Generic role contract

`scripts/utils/role_contract.py` provides:

- exact machine-schema key, dtype, shape, dimension, and semantic validation for plant, labels, estimator outputs, and controller logs;
- `RolePayloadWriter` for manifest-bound non-observation NPZ payloads and hash indexes;
- `ObservationRoleWriter` for manifest/pair/split/suite/config-bound `ObservedRecord` payloads;
- `RolePayloadLoader` for safe-root path, SHA-256, exact-key, schema, and semantic revalidation;
- `DatasetRoleBuilder` for already assigned, complete C1/S manifests;
- hard refusal of any `test` assignment while the config remains draft; and
- `SupervisedTrainingJoin` restricted to a nonempty subset of `dev|pilot|val`.

The join yields only:

- `run_id`;
- one suite's `ObservedRecord`; and
- the exact label target.

It does not attach the manifest, privileged plant truth, provenance, estimator outputs, or controller logs. The deployable boundary remains the jointly approved `DeployableObservationLoader`, which receives only one `observations/<suite>` root.

### Synthetic role-completeness fixture

`scripts/build_data_contract_fixture.py`:

- consumes the tracked schema and draft config;
- creates two complete matched C1/S pairs;
- assigns one pair to `dev` and one to `val`;
- keeps trajectory, fault-setting, and split groups disjoint;
- writes plant, observations, labels, estimator outputs, and controller logs;
- publishes the path-free manifest and all exact role indexes;
- reopens and audits every payload;
- exercises both suite-specific supervised joins;
- refuses an existing output root; and
- writes a strict JSON summary with an explicit contract-only evidence boundary.

This fixture is synthetic infrastructure. It is not:

- the complete Gate-3 assignment;
- generated research data;
- a headline model fit;
- a validation result; or
- a confirmatory artifact.

### Verification

Session-28 results from the repository virtual environment:

```text
focused role-contract tests: 11 passed in 0.32s
full packet suite: 358 passed in 9.86s
two independent builds: 30/30 files byte-identical
manifest rows: 4
manifest test assignments: 0
summary test_payloads: 0
compileall: pass
CLI-help smoke test: pass
git diff --check: pass
```

No fixture output was written into the repository. At closeout:

- `Reproducibility Packet/config.json` did not exist;
- the repository contained zero `.npz` files; and
- `.gitignore` required no change.

Use the repository virtual environment explicitly. From `Reproducibility Packet/`:

```powershell
..\venv\Scripts\python.exe -m pytest tests\test_role_contract.py -q
..\venv\Scripts\python.exe -m pytest tests\ -q
..\venv\Scripts\python.exe -m compileall -q scripts tests
```

## Gate status and next dependency

### Gate 1

- jointly approved as complete.

### Gate 2

- still **BLOCKED overall**.

Completed foundation:

- machine schema;
- draft/frozen config lifecycle;
- path-free identity manifest and role indexes;
- whole-group/CRN/audit invariants;
- suite-scoped deployable observation loader;
- generic schema-driven role writers/loaders;
- non-test supervised label join;
- deterministic synthetic role-completeness fixture.

Still required:

- the complete jointly approved Gate-3 scenario/fault/trajectory assignment;
- the real multi-setting MuJoCo generator driven by that assignment;
- role-completeness audit on the generated research data.

Do not claim Gate 2 complete based on the synthetic fixture.

### Gate 3

The complete assignment requires explicit Claude/Codex same-state approval before:

- any headline model is fit; or
- the real assigned dataset is generated.

The reviewable assignment must cover:

- known-class severity/location grids;
- compound/OOD holdout;
- trajectories and payloads;
- environment/contact profiles;
- onset/excitation roles;
- whole trajectory and whole fault-setting splits;
- seeds; and
- suite-matched comparison groups.

The assignment checkpoint is distinct from the later final immutable config freeze.

### Gates 4–7

Claude's model/calibration/evaluation lane waits on the approved Gate-3 assignment. CUDA readiness is already recorded (`torch==2.11.0+cu128`, RTX 5060 Ti, `sm_120`), but toolchain readiness is not model-fit authorization.

The Gate-6 protocol remains the in-contract four arms:

- no-action/detection-only;
- transparent attribution-driven;
- RMA;
- oracle.

Do not narrow the project to information-only or post-hoc retune the blocked action families without an amendment.

## Config and claim boundaries

The tracked draft:

- is `Reproducibility Packet/config/draft-config-v0.1.json`;
- has `status=draft`;
- reports `confirmatory=False`;
- has hash `dev-0211f2e71a473fef3c30cd53fd0a269df45156a3d58e83097bac7a5638bf6180`;
- keeps Gates 2–7 open; and
- cannot authorize confirmatory work.

No `config.json` exists. Keep it absent until every freeze gate closes and both agents explicitly approve the exact final state.

Durable boundaries:

- development screens and synthetic fixtures are not confirmatory results;
- a draft hash is not a frozen config;
- detection, attribution, information authorization, action authorization, and control outcome are distinct;
- fault improvement is not source-specific recovery unless it clears the matched healthy false-authorization gate;
- A1 safety is hard;
- the sampled probability envelope is not a continuous proof;
- physical truth, observations, labels, estimator state, and controller authorization remain role-separated;
- `test` remains untouched until after complete final freeze.

## Immediate next steps

Session 29 should:

1. inspect Claude's exact review response and the actual review-target files;
2. close `APPROVE_GATE2_ROLE_WRITE_PATH` only if approval is explicit and the state is unchanged;
3. otherwise address supported file/line findings and re-hand off the exact corrected state;
4. prepare the complete Gate-3 multi-setting assignment as a reviewable preregistration artifact;
5. obtain explicit same-state assignment approval before model fitting or real assigned generation;
6. then connect the approved assignment to the real multi-setting MuJoCo generator and role-completeness audit;
7. keep `config.json` absent and all `test` roles untouched.

The next regular Codex progress report is Session 32.

## Transcript append hard gate

For every append to the active Phase-2 transcript:

1. read the physical UTF-8 tail;
2. record the pre-write line count;
3. verify the complete multi-line EOF anchor is unique;
4. use `apply_patch` only against that exact anchor;
5. verify the new header occurs exactly once after the boundary;
6. verify it is physically last; and
7. require `git diff --numstat` to show `+N/-0`.

Session-28 transcript delta was `+40/-0`. No recurrence was logged in transcript-order monitoring.

## Public and detailed records

- Root `README.md` was intentionally unchanged because this is an unreviewed infrastructure increment, not a scientific milestone or phase transition.
- Read `agents/Codex/Session Summaries/HumanReport28.md` for the detailed design, verification, and file record.
