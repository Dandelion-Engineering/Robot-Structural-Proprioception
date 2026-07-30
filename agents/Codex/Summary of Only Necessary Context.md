# Summary of Only Necessary Context — Codex

**Rewritten:** 2026-07-29, Codex Session 44

**Phase:** Phase 2 — Integration and Reproducibility Build

**Config:** **UNFROZEN**; `Reproducibility Packet/config.json` is absent

**Current decision:**

```text
APPROVE_PROTOCOL_P_V2_3_3_EXACT_STATE
APPROVE_I13B_PERMANENT_PACKET_TEST_CURRENT_STATE
APPROVE_SEAM_IMPLEMENTATION_CURRENT_STATE
APPROVE_INACTIVE_PROVENANCE_FAIL_LOUD_GUARD_CURRENT_STATE
DEFER_I13A_AND_RESULTS_ONLY_PERSISTENCE_GUARDS_TO_STAGE_DRIVER_REVIEW
AUTHORIZE_ONE_ROW_REPLAY_GATE_ONLY
BLOCK_CONFIG_FREEZE_PENDING_PRECONFIRMATORY_BUILD_AND_VALIDATION
```

No Protocol-P replay, Stage 0/A/B/C rollout, identity, statistic, or artifact has run
since the seam was approved. The confirmatory test split remains untouched at zero
identities and zero payloads.

## Resume here

The authoritative active thread is:

```text
chats/Claude-Codex/Phase 2 Integration and Config Freeze/
  Phase 2 Integration and Config Freeze - Active.md
```

Its physical last turn is **Codex Session 44**, beginning at line 9,211.

Claude owns the next replay execution and later stage-driver implementation. Codex owns
exact-state review. Do not take implementation ownership unless explicitly reassigned.

The next authorized action is **only** the pinned one-row replay gate with
`overrides=None`. Claude must post exact evidence before Stage 0. Stage 0 and Stages
A/B/C remain unauthorized until that replay result is reviewed.

## Jointly approved Protocol P

```text
Reproducibility Packet/protocol/protocol-p-v2.3.3.md
canonical sha256:
  5689dad7ce4194b9a7dbe381006027df178997adf732f5734a77ef048bdf421f
raw sha256:
  5689dad7ce4194b9a7dbe381006027df178997adf732f5734a77ef048bdf421f
bytes:
  54,621
encoding/EOL:
  UTF-8, no BOM, pure LF
git attributes:
  text set, eol lf
owner approval:
  Claude Session 43
reviewer approval:
  Codex Session 43
execution:
  none
```

The specification review loop is closed on that digest. Do not edit the file in place.
If a source-checkable defect later requires correction before execution, rename to the
next version, explicitly approve the replacement digest, and repeat same-state review.

## Jointly approved seam implementation

The implementation-review loop closed in Codex Session 44 on commit:

```text
3fa806c1cae602b5e1c12e07040954b728128877
```

Exact files:

```text
Reproducibility Packet/scripts/utils/assignment_generator.py
  git blob    1c565888edd6e538cbb281894ab6c4cdc418bb6b
  raw sha256  07fbbe563b5a904eba2d57f58e436e84975d2891ea7ebf4cac9f24253ce5b06b
  bytes       36,326
  UTF-8, no BOM, pure LF

Reproducibility Packet/tests/test_assignment_generator_screen_overrides.py
  git blob    2ec96c9f995fa9e9efad0000af1d3364a4994db4
  raw sha256  69f1df3145e58a68ceccd698e198afa030391e00adc3b8be518335a2924f0635
  bytes       23,116
  UTF-8, no BOM, pure LF
  37 tests
```

The blob hashes are the checkout-EOL-stable identifiers. These source files are not
byte-pinned in `.gitattributes`, deliberately: Protocol P does not hash them.

### Approved seam behavior

- `ScreenOverrides` is frozen and has five fields, all defaulting to `None`.
- `is_active()` uses `is not None`; `physical_faults=()` remains active.
- Probe peak must be finite and positive.
- Ramp fraction must be finite in `(0, 0.5]`.
- A probe override on a probe-free trajectory raises.
- `physical_faults` replaces the derived list using `is not None`.
- A physical-fault override on a sensor-fault reservation raises.
- Active provenance must be nonempty, `dev-` plus exactly 64 lowercase hex, and
  base-distinct.
- The stamped provenance reaches both `OnlineSensorSession` and every
  `SensorModel.observe`.
- A supplied realized pair id is used without `_dataset0`.
- The all-`None` path retains the original base hash, base pair plus `_dataset0`,
  derived faults, default ramp, online C0 construction, post-hoc observations, and
  return tuple.
- The seam mutates no assignment catalog and writes no dataset-role artifact.

Codex approved Claude's extra fail-loud guard: an otherwise inert override carrying a
`provenance_hash` raises instead of silently discarding the identity claim and returning
the base hash.

The permanent location of the 37 seam tests is approved. They protect a generator
contract, not a screen-local statistic.

## Permanent I13b test

```text
Reproducibility Packet/tests/test_cable_plant_softening_boundary.py
raw sha256:
  712d2165f8bd96d5e88a07e5f76c53313cb5e6aca5c6d0d21af43914c3e26ac7
git blob:
  ca0f44743b3e7b4f4268e596fc82f6e1bbee2411
bytes:
  6,671
tests:
  6
owner approval:
  Claude Session 43
reviewer approval:
  Codex Session 43
```

The test checks the actual model swap as well as `_softened`, covers onsets 1, 5, and
500, pins `_step_index(1.0, 0.002) == 500`, records omitted-onset activation at step 0,
and checks that a healthy plant never constructs or activates a softened model.

I13b must remain green before every Protocol-P stage.

## The replay-only authorization

The next action may:

1. hash the two retained `.npz` references by exact raw bytes;
2. rebuild only `scenario_dev_t01_f000_r00`;
3. call `_generate_reservation` with `overrides=None`;
4. require base config-hash stamping;
5. compare all 20 privileged fields and all 38 S payload entries by array equality;
6. remain ephemeral and write no Protocol-P screen artifact; and
7. post exact evidence for Codex review before Stage 0.

Pinned binary inputs:

```text
plant reference
  data/gate3-base-dev-pilot-val-c1-s/
    plant/scenario_dev_t01_f000_r00_S_dataset0.npz
  bytes       3,176,122
  raw sha256  ed5b1f39f4ba535c60eb3e1b8587c7b03f59a5c3f9c1189b55635f0d49b65e45

S observation reference
  data/gate3-base-dev-pilot-val-c1-s/
    observations/S/scenario_dev_t01_f000_r00_S_dataset0.npz
  bytes       929,068
  raw sha256  cdde17f6d32c5d648249f4a9b343ec3f997b04c83cadacbf9d2c5f1186bb4c83
```

The previous one-row replay succeeded, but the newly approved seam has not yet passed
the protocol's replay gate. Never generalize one exact row to the 472-reservation
retained dataset.

## Deferred stage-driver gate

I13a, I3-I8 orchestration, and the results-only persistence condition are not part of
the low-level §3 seam. That scope boundary is approved.

Before any Stage-A/B/C rollout, review the actual stage driver and require:

1. a closed-vocabulary `screen_physical_faults` helper;
2. healthy requires severity absent and returns `()`;
3. structural requires finite severity in `(0, 1]` and returns exactly one complete
   `FaultSpec` with onset derived from trajectory time and control timestep;
4. full field-by-field I13a equality before each rollout;
5. a complete `ScreenOverrides` bundle rather than a partial bundle;
6. I3 reservation-difference equality and suffix-free I4;
7. I5-I8 identity/CRN/provenance checks;
8. explicit Protocol-P condition keys, never the stale assignment-derived returned
   label;
9. no persisted `ObservedRecord`, label payload, manifest, role index, or dataset
   payload; and
10. a test around the real results-only output root that can fail on a wrong dataset
    write.

The seam can represent a partial bundle at its low-level API. That is not authorization
for the driver to accept one.

The stale returned source label remains non-blocking only because Protocol P must persist
no observation, label, manifest, or role index and must key results from its explicit
condition. Any future consumer that persists an overridden run must correct both label
and identity before authorization.

## Required execution order

```text
Protocol P v2.3.3 exact-state approval                COMPLETE
permanent I13b exact-state approval                   COMPLETE
generator seam exact-state approval                   COMPLETE
one-row replay gate                                   NEXT / ONLY AUTHORIZED ACTION
replay evidence review                                REQUIRED BEFORE STAGE 0
Stage 0 script and identity/persistence review        LATER
Stage A/B/C driver review                             LATER
Stage A                                                AFTER DRIVER APPROVAL
Stage B                                                AFTER STAGE A
Stage C                                                AFTER STAGE B
result/terminal-branch review                         REQUIRED
written Amendment A2 + replacement assignment        LATER
from-zero non-test regeneration and re-audit          LATER
Gates 4-7 -> joint final freeze -> confirmatory run   LATER
```

No Stage-0 script exists. No stage driver exists. No stage is authorized.

## Protocol-P design retained in substance

Do not reopen these without new evidence:

- universe: dev diagnostic trajectory `t01`, cells 4/5/6/7;
- replay gate: one rollout;
- Stage 0: 100 synthetic sensor-only paired differences, zero rollouts;
- Stage A: 9 admissible probe candidates x 4 cells x
  `{healthy, remEI 0.75, remEI 0.35}` = 108 rollouts;
- Stage B: 10 remaining-EI values x 4 cells, reusing 0.75 and 0.35 from Stage A,
  so 32 new rollouts;
- Stage C: 8 healthy replicates per cell with k=0 reused from Stage A, so 28 new
  rollouts;
- total plant rollouts including replay: 169;
- statistic: four-gauge matched 0.8-Hz cosine/sine coefficient difference, eight
  concatenated entries;
- operative null: per-cell 0.95 quantile with `method="higher"` over all 28 within-cell
  healthy pair distances;
- pass rule: `D(v,c) >= 2.0 * Q95_c` in every screened cell;
- selection: maximize worst-cell `D` at remEI 0.75; ties within 1% choose lower
  amplitude then larger ramp fraction;
- candidate grid: peaks 0.05-0.40 N and ramp fractions 0.125/0.25/0.5;
- torque gate admits exactly 0.05/0.10/0.15 N, with inclusive equality at 0.15 N;
- measurement origin: probe start, not fault onset or response-selected peak;
- Stage-A/B signal is identity-matched; Stage-C null is unmatched and favours S;
- gauge-only and unmatched secondaries are descriptive only;
- OOD 0.45/0.55 stays excluded from known-class four-way macro-F1;
- all outputs are development-only and ineligible for confirmatory analysis.

The honest prior remains that remEI 0.75 likely fails widely and remEI 0.50 is near the
boundary under earlier optimistic projections. Case B and Case C remain roughly
comparable. This is a prior, not a result.

## Role, config, and data state

```text
Gate 1:
  closed

Gate 2 generic role path and current pre-A2 base roles:
  closed

Gate 3 assignment:
  closed for current pre-A2 design

Protocol P specification:
  v2.3.3 exact state jointly approved
  unrun

Protocol-P seam:
  exact state jointly approved

Protocol-P replay:
  authorized, not run

Stage 0 and Stage A/B/C:
  unauthorized, unimplemented

Amendment A2:
  not written or approved

Gates 4-7:
  open

final config.json:
  absent
```

The local ignored retained dataset contains 472 dev/pilot/validation reservations,
944 C1/S manifest rows, and zero test rows. It was not regenerated. Exactly one
development row was replayed in earlier diagnostic work; the approved seam still awaits
its own replay gate.

If a corrected written Amendment A2 and replacement assignment later receive same-state
approval, Codex's standing choice is coherent from-zero regeneration, not an in-place
patch.

## Evidence boundary

Protocol P is a pre-registered development screen for whether a structural fault is
measurable at the delivered excitation. It cannot establish the project hypothesis.

Keep separate:

- construction correctness;
- safety/admissibility;
- structural detectability;
- fault attribution;
- information/action authorization;
- controller outcome; and
- confirmatory evidence.

The replay is an implementation positive control only.

Prior structural-separability outputs are development diagnostics. They are not pilot,
validation, confirmatory, or frozen decision margins.

## Verification baseline

Use the repository virtual environment:

```powershell
.\venv\Scripts\python.exe -m pytest -q "Reproducibility Packet\tests"
```

Codex Session 44:

```text
focused seam tests                    37 passed in 1.37 s
legacy generator + permanent I13b     13 passed in 0.91 s
full packet suite                     442 passed in 12.06 s
```

Do not use root-wide `pytest -q`; ignored duplicate trees under `tmp/` can pollute
collection.

Before binary replay decisions, use raw hashes only. Do not normalize `.npz` bytes.

Before any exact-state approval, independently compute the relevant raw bytes, BOM/EOL
state where applicable, raw SHA-256, git blob, and git attributes.

Before any commit:

```powershell
git diff --check
git diff --cached --check
```

CRLF warnings alone are not a reason to churn unrelated files.

## Transcript-order state

The active transcript is append-only. Session-44 append verification:

```text
pre-write physical lines:
  9,207
pre-write bytes:
  713,382
pre-write sha256:
  fa74b76598595e50d7c887cb0d77b59fa8f2ee32f65596ba76cc1593c7aa13bd
Codex header:
  line 9,211
  count 1 total
  after old boundary
old byte prefix:
  exact
technical diff:
  +129 / -0
post-write physical lines:
  9,336
post-write bytes:
  719,199
physical last author:
  Codex
```

No recurrence occurred, so the monitoring thread was not updated.

For every future append:

1. read the UTF-8 physical EOF tail;
2. record pre-write physical line count, byte count, and SHA-256;
3. verify a complete multi-line EOF anchor occurs exactly once;
4. patch using that complete verified anchor;
5. verify the new header occurs once after the old boundary;
6. verify the old byte prefix is exact;
7. reread the physical tail; and
8. require additions-only transcript diff.

If any check fails, stop and repair by dated append-only correction.

## Public README

The root README is a public append-only running log. Codex Session 44 added one lean
milestone: the generator seam and its permanent guards reached exact-state approval.
The entry explicitly says only the replay gate is next; no replay or stage has run,
config remains unfrozen, the final test split is untouched, and the research question
is unanswered.

Do not add another public entry merely for a routine replay unless it changes the
publicly meaningful state. Run the heartbeat each session against
`Playbooks/live-run-readme.md`.

## Required next actions

1. Read the controlling instructions, this continuity file, all Codex-relevant chat
   summaries, and the active transcript before replying.
2. Read Claude's newest report and exact replay evidence.
3. Verify the two retained input hashes by raw bytes.
4. Confirm the replay used `overrides=None`, base config hash, the pinned reservation,
   and no persistence.
5. Independently check equality counts: 20 privileged fields and 38 S payload entries.
6. Append an explicit approve/block replay decision through the physical-EOF hard gate.
7. Do not authorize Stage 0 if any replay fact differs.
8. If replay passes, authorize only the next bounded implementation gate needed by the
   approved protocol; do not silently authorize unreviewed stage code.
9. Keep `config.json` absent and the test split untouched.
10. Close out with Codex `HumanReport45.md`, README heartbeat, Codex workspace README,
    complete continuity rewrite, hygiene checks, exact commit message, and push.

The next regular Codex progress report is Session 48 unless a phase transition or
approved written Claim Sheet amendment triggers one earlier.

## Non-negotiable boundaries

- Approval is explicit and exact-state-specific.
- Preserve owner/reviewer lanes.
- Never treat development, screen, pilot, fixture, or replay evidence as confirmatory.
- Never convert safety into proof of correct construction.
- Never convert detection into attribution or action authority.
- Never silently rewrite a public or transcript-facing overclaim; append a correction.
- Never normalize binary artifacts before exact hashing.
- Never run the replay or stages from an unapproved implementation.
- Never run stages out of order.
- Never create final `config.json` before all required gates close jointly.
- Never touch the test split before confirmatory authorization.
- Use append-only transcript hard gates and preserve exact requested commit messages.
