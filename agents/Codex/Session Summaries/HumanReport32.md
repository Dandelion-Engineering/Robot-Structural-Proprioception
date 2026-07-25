# Human Report — Codex Session 32

**Current date and time:** 2026-07-24 17:40 PDT
**Phase:** Phase 2 — Integration and Reproducibility Build
**Session role:** Gate-3 approval close, approved-assignment embedding, and real Gate-2 base-role generation
**Final config state:** **UNFROZEN** (`Reproducibility Packet/config.json` remains absent)
**Governing decision:** `BLOCK_CONFIG_FREEZE_PENDING_PRECONFIRMATORY_BUILD_AND_VALIDATION`
**Session decision:** Hand off the complete primary C1/S base-role generator and independently audited dev/pilot/validation dataset for exact-state review

---

## Summary

### Approval received and Gate 3 closed

I followed the complete `AgentPrompt.md` startup workflow before acting: Project
Details, Codex continuity, every relevant chat summary, all active Codex chats,
Claude's latest session report, and Claude's regular Session-32 progress report.

The active Phase-2 transcript contained Claude's explicit same-state response:

```text
APPROVE_GATE3_ASSIGNMENT_V0_1
```

on the exact amended 808-reservation state from Session 31. Claude independently
re-derived all 808 reservations, reproduced every reviewed digest, verified the
new within-trajectory context invariant actually rejects the old 656 state, and
confirmed the dev/pilot training alias is gone. I accepted that approval. Gate 3
is closed at:

```text
dev-eec59ec8a296a9a4ff4909f8e7f1de91a0a8f4bf289ae1533a427d1a87bc33f1
```

I also accepted Claude's recorded residual limitation without reopening Gate 3:
pilot→validation is a clean confound-severity escalation, while
validation→test also changes from a per-trajectory half fraction to the complete
factorial. The later Gate-7 driver and Technical Report must state that
distinction.

### Exact assignment embedding without a circular hash claim

The assignment was approved against parent draft hash:

```text
dev-0211f2e71a473fef3c30cd53fd0a269df45156a3d58e83097bac7a5638bf6180
```

Embedding the assignment changes the config and therefore changes the config
hash. Rewriting the assignment's `draft_config_hash` to the new value would
change the assignment hash, which would change the config again: a circular
fixed-point problem that would also destroy the exact reviewed bytes.

I implemented a one-way approval wrapper instead:

1. preserve the approved assignment byte-for-byte;
2. record the approved parent hash and parent open-gate list;
3. embed the exact assignment and approval token;
4. remove only the Gate-3 open-gate item;
5. recompute the current draft self-hash;
6. on load, reconstruct the parent document by restoring a null manifest and
   the recorded parent gates;
7. prove the reconstructed canonical parent hash;
8. validate the exact assignment against that parent; and
9. let the current self-hash bind the wrapper and assignment.

The assignment JSON SHA-256 remains:

```text
76255a8089f3e27d893b26d981cbf50e808bd75ba518c44b55c4635ec83514ae
```

The new current draft hash is:

```text
dev-712abf27c3f8f3c331ae9b76e3f22c48857334cc15a81e819718165e47753e56
```

The wrapper authorizes only `dev`, `pilot`, and `val`, and explicitly records
`test_materialization_allowed=false`. `config.json` remains absent.

### Approved mechanics paths implemented

The real generator required four mechanics changes that did not exist in the
generic Gate-2 fixture.

#### Exact distal point mass

`CableModelConfig` now carries `distal_payload_mass_kg`. The implementation adds
the point mass at the actual distal site, recomputes the body's combined center
of mass, applies the parallel-axis theorem to the inertia tensor, diagonalizes
the result into MuJoCo's inertial representation, and calls `mj_setConst`.

All eight declared masses are compiled and checked before the retained full
run:

```text
0.000, 0.025, 0.050, 0.075, 0.100, 0.125, 0.150, 0.200 kg
```

Compiling the two test-owned scalar values is a read-only mechanics check. It
does not materialize a test identity or payload.

#### Scheduled contact without collision-pair widening

`CableModelConfig` now carries an optional absolute contact window. The
generator converts each approved relative offset to:

```text
trajectory onset + contact start/end offset
```

Outside the window, the same plane geom is moved out of reach; inside, it
returns to the fixed approved 0.200 m height. The explicit A1 collision pair
remains the one distal endpoint↔plane pair. Tests prove no pre/post-window
contact and `model.npair == 1`.

#### Compound physical faults

`CablePlant` now accepts at most one structural and one actuator component.
Each component activates at its own declared onset through the existing
physical injection boundary. Sensor components are still rejected by
`CablePlant`.

#### Compound plant-plus-sensor cases

The generator splits each expanded fault setting at the existing boundary:

- structure/actuator components → `CablePlant`;
- encoder bias/drift/dropout → `OnlineSensorSession`.

Bias and drift sign are balanced by `fault_seed`; the label retains the
assignment's absolute severity convention. The full component list remains in
the non-deployable embedded assignment and is joined to a run through
`fault_setting_id`; deployable observations do not receive it.

### Real assignment-driven base dataset

The retained generated dataset is local and ignored:

```text
data/gate3-base-dev-pilot-val-c1-s
```

The generator:

- builds identities directly from the approved reservation expansion;
- rejects any split outside `dev|pilot|val`;
- requires a matched C1/S pair;
- uses a common C0-observable controller session so paired suites share one
  physical plant trajectory;
- batch-renders C1 and S from that plant with common random-number fields;
- checks common observed channels bit-for-bit before writing;
- writes plant and label roles only through
  `DatasetRoleBuilder.make_writer`;
- writes observations only through
  `DatasetRoleBuilder.make_observation_writer`; and
- refuses an existing output root.

Dataset identity uses `train_seed=0`. The assignment's five training seeds are
not expanded before five Gate-4 model fits exist.

The full generation audit reports:

```text
status: complete_primary_c1_s_base_research_dataset
reservations: 472
manifest rows: 944
dev / pilot / val: 152 / 152 / 168
plant payloads: 944
label payloads: 944
C1 / S observations: 472 / 472
contact-active steps: 243
safety-flag events: 0
test rows: 0
dataset bytes: 3,857,662,158
```

Estimator-output and controller-log roles remain intentionally pending the
Gate-4 fits. This is why Gate 2 is not declared complete in this session.

### Independent generated-data audit

The separate audit CLI does not read the generator's summary. It:

- reloads the path-free manifest;
- independently re-expands all authorized assignment reservations;
- compares every identity field directly;
- reloads all 944 plant and 944 label payloads through their hash-checking
  schema loaders;
- reloads 472 C1 and 472 S observations through the suite-scoped deployable
  loaders;
- proves all 472 paired plant NPZ files are byte-identical;
- compares every shared observed channel and validity mask bit-for-bit on all
  472 pairs;
- repeats the eight-mass mechanics preflight; and
- fails on any test row.

It returns:

```text
complete_primary_c1_s_base_dataset_audit_pass
```

with zero test identity or payload rows.

### A partial run was deliberately discarded

The first full attempt used an earlier preflight that checked the six
research-owned masses before generation. During that run I noticed the approved
implementation requirement says every assigned mass must be tested first,
including the two scalar values owned by the still-unmaterialized test split.

The physics code was already correct, the test masses were later compiled
successfully, and no test identity existed. That was still not enough to prove
the required chronology. I stopped the process at 193/472 reservations,
validated the exact ignored output path under the repository `data/` root,
removed only that rebuildable partial dataset and its logs, strengthened the
preflight to all eight masses, and regenerated from zero. The retained dataset
comes solely from the corrected second run.

## Verification

All Python commands used the repository virtual environment:

```text
full packet suite:             397 passed in 9.33 s
focused assignment generator: 6 passed
assignment binding/Gate-3:     29 passed in combined focused run
cable plant focused suite:     12 passed
compileall:                    pass
approved-assignment CLI:       pass
generator serial smoke:        pass
generator multiprocessing:     pass
independent partial audit:     pass
independent full audit:        pass
git diff --check:              pass
```

The line-ending output contains only the repository's recurring LF/CRLF
warnings; no whitespace error is reported.

The tracked assignment still has the reviewed file SHA-256. `config.json`
remains absent. The complete generated manifest contains 944 non-test rows and
zero test rows.

## Cross-review performed

I read Claude's `HumanReport32.md`, `Progress Report Session 32.md`, and the
actual active-thread approval. I independently checked the load-bearing claims:

- all five reviewed file digests reproduce;
- the assignment expands to 808 reservations;
- the amended state has zero fault/context leakage and no within-trajectory
  context-axis alias;
- the new invariant rejects the superseded 656-reservation repeat budget;
- the approved state keeps generation permissions false inside the historical
  proposal; and
- Claude made no review-target edits.

No Claude-owned artifact was changed this session.

## Review-cycle and transcript handling

The Phase-2 transcript has a documented wrong-location-append history, so both
Session-32 appends used the append-only hard gate:

1. read the physical UTF-8 tail;
2. record the pre-write line count;
3. capture a multi-line exact EOF anchor;
4. prove the anchor occurs once;
5. patch against that anchor;
6. prove the new header occurs once after the pre-write boundary;
7. re-read the physical tail; and
8. verify the transcript diff has zero deletions.

The final handoff append used:

```text
pre-write lines: 3146
post-write lines: 3297
new header line: 3150
header count: 1
last line: — Codex
```

The handoff asks Claude to answer:

```text
APPROVE_GATE2_GENERATOR_BASE_ROLES
```

with no review-target edits, or return an artifact/file-specific block.

## Public Live-Run status

The root README received one lean append-only milestone entry. It reports:

- 472 real non-test reservations and 944 C1/S manifest rows;
- independent paired plant/shared-channel audit success;
- 243 contact-active steps and zero safety flags;
- test remains untouched; and
- this is infrastructure, not a model fit, result, or frozen config.

The earlier plan and corrections remain unchanged in the running log.

## Claim boundaries

This session establishes a generated, audited base-role dataset. It does not:

- complete Gate 2 before same-state review and later role completion;
- fit an estimator;
- select a threshold;
- authorize an action;
- create a validation result;
- create final `config.json`;
- materialize test;
- evaluate the C1-versus-S headline;
- close Phase 2; or
- create the Phase-3 verification artifact.

The generated validation split is available for the later preregistered
selection/calibration lifecycle, but no result is inferred merely because it
exists.

## Files created

- `Reproducibility Packet/scripts/utils/assignment_binding.py`
- `Reproducibility Packet/scripts/embed_approved_assignment.py`
- `Reproducibility Packet/scripts/utils/assignment_generator.py`
- `Reproducibility Packet/scripts/generate_assignment_dataset.py`
- `Reproducibility Packet/scripts/audit_assignment_dataset.py`
- `Reproducibility Packet/tests/test_assignment_binding.py`
- `Reproducibility Packet/tests/test_assignment_generator.py`
- `agents/Codex/Progress Reports/Progress Report Session 32.md`
- `agents/Codex/Session Summaries/HumanReport32.md`
- ignored local `data/gate3-base-dev-pilot-val-c1-s/`

## Files updated

- `Reproducibility Packet/config/draft-config-v0.1.json` — exact approved
  assignment wrapper, Gate-3 removal, and current self-hash.
- `Reproducibility Packet/scripts/utils/__init__.py` — shared-module index.
- `Reproducibility Packet/scripts/utils/cable_mechanics.py` — distal point mass
  and contact-window contract.
- `Reproducibility Packet/scripts/utils/cable_plant.py` — scheduled contact and
  compound physical faults.
- `Reproducibility Packet/scripts/validate_gate3_assignment.py` — parent/current
  approval-aware validation summary.
- `Reproducibility Packet/tests/test_cable_plant.py` — mass, window, and compound
  boundary regressions.
- `Reproducibility Packet/tests/test_gate3_assignment.py` — parent-config
  compatibility after embedding.
- `Reproducibility Packet/README.md` — approved assignment, generator, audit,
  and current boundary.
- `README.md` — one lean append-only generated-data milestone.
- `chats/Claude-Codex/Phase 2 Integration and Config Freeze/Phase 2 Integration and Config Freeze - Active.md`
  — append-only approval receipt and exact-state generator handoff.
- `agents/Codex/README.md` — workspace index through Session 32.
- `agents/Codex/Summary of Only Necessary Context.md` — fully rewritten resume
  state.

## Files deliberately unchanged

- `Reproducibility Packet/config/proposed-gate3-assignment-v0.1.json` — exact
  approved bytes preserved.
- `Reproducibility Packet/config.json` — absent.
- `Claim Sheet.md` and `Accessible Claim Sheet.md` — no amendment.
- `director_requests.md` — no director-only dependency.
- `agents/Codex/references.md` — no new project research source.
- transcript-order monitoring thread — no recurrence.

## `.gitignore` review

The root `/data/` rule correctly ignores the 3.86 GB generated dataset, smoke
roots, benchmarks, and generation logs. Global NPZ/model/cache/secret rules
remain adequate. No `.gitignore` change was needed.

## Progress-report trigger

Session 32 is Codex's fourth regular eight-session reporting point. I wrote:

```text
agents/Codex/Progress Reports/Progress Report Session 32.md
```

It covers Sessions 25–32 at the director-facing Accessible-Piece bar, including
what is working, what is blocked, the design-leak corrections, the generator,
the discarded partial-run chronology correction, and the next gates.

## Next steps

1. Claude independently reviews the exact tracked generator/config state and
   the local generated dataset and returns
   `APPROVE_GATE2_GENERATOR_BASE_ROLES` or an artifact-specific block.
2. If approved, Claude owns Gate 4: build and fit the matched C0/C1/S learned
   attribution and RMA comparators across the five preregistered training seeds.
3. Complete estimator-output/controller-log roles only from those real fits.
4. Use validation for calibration, abstention, OOD, and action authorization
   without touching test.
5. Freeze the confirmatory controller protocol and Gate-7 evaluation driver.
6. Create immutable `config.json` only after Gates 2–7 close and immediately
   before untouched test materialization.

## End state

```text
Gate 1: complete and jointly approved
Gate-2 generic write/load/join foundation: complete and jointly approved
Gate-2 real primary C1/S base roles: generated and independently audited;
  exact-state review open
Gate 2 overall: BLOCKED pending review and Gate-4 estimator/controller roles
Gate 3: complete and jointly approved at dev-eec59ec8...bc33f1
Gate 4: open; Claude owns the matched model fits
Gates 5–7: open
Final config: UNFROZEN
Research result: none
Test identity/payload materialized: 0
```
