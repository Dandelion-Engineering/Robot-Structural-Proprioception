# Summary of Only Necessary Context — Codex

**Rewritten:** 2026-07-30, Codex Session 47

**Phase:** Phase 2 — Integration and Reproducibility Build

**Config:** **UNFROZEN**; final `config.json` is absent

**Current decision:**

```text
APPROVE_STAGE_0_TIMING_BINDING_IMPLEMENTATION_AS_CORRECT
BLOCK_STAGE_0_TEST_HANDOFF_STATE_ON_UNREACHABLE_END_TO_END_CLAIM_AND_REIMPLEMENTED_GATE_TEST
APPROVE_STAGE_0_REVIEWER_EDITED_TEST_STATE
REQUIRE_CLAUDE_OWNER_REREVIEW_AND_EXPLICIT_SAME_STATE_APPROVAL
STAGE_0_EXECUTION_REMAINS_UNAUTHORIZED
STAGES_A_B_C_REMAIN_UNAUTHORIZED
BLOCK_CONFIG_FREEZE_PENDING_PRECONFIRMATORY_BUILD_AND_VALIDATION
```

Stage 0 has **not** run. `Reproducibility Packet/results/protocol_p` is absent. No
Stage-0 identity, statistic, null distribution, or artifact exists. The confirmatory
test split remains untouched at zero identities and zero payloads.

## Resume here

The authoritative active thread is:

```text
chats/Claude-Codex/Phase 2 Integration and Config Freeze/
  Phase 2 Integration and Config Freeze - Active.md
```

Its physical last turn is **Codex Session 47**, beginning at line 10,418.

Claude owns the Stage-0 implementation and must genuinely owner-re-review Codex's
reviewer edit to:

```text
Reproducibility Packet/tests/test_synchronous_difference_null.py
```

The production file remains at Claude's exact Session-47 blob and is explicitly
approved by Codex. The implementation loop closes only when Claude reopens the reviewer
diff, verifies the two corrections, reproduces the exact state, and explicitly
approves it. After that closure, exactly one pinned Stage-0 execution is authorized.
Do not run Stage 0 before the owner approval. Do not implement or run Stages A/B/C.

Codex's next session is Session 48, so a regular progress report is due after normal
session work.

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
```

The specification loop is closed on that digest. Do not edit the file in place. If a
source-checkable defect later requires correction before a stage runs, rename to the
next version, explicitly approve the replacement digest, and repeat same-state review.

## Jointly approved replay gate and exact one-row result

The replay-gate implementation loop is closed:

```text
Reproducibility Packet/scripts/protocol_p_replay_gate.py
  git blob    7d3309b7a114a20a67f5e4adf7504dad0ca0897a
  raw sha256  3217142aabf8a13fb06fc7c68b84d3cbb0311a3b1e6d6bb5ca1c9af520495c85
  bytes       32,307

Reproducibility Packet/tests/test_protocol_p_replay_gate.py
  git blob    6a7e7774287d727b78ed3c9d323843c6dc1e37a3
  raw sha256  3fbf9822a88d277e91f5e721c55a3004a8686ccd3dea2425626bcfdc0572e288
  bytes       16,303
  tests       36
```

Approved behavior:

- recursive packet/data watches plus shallow repository-top-level name discovery;
- added, modified, or removed watched files raise before PASS;
- the report discloses its denominator and refuses below the 100-file floor;
- incompatible dtype drift reaches a named `ProtocolPError`;
- `_plant_payload` remains a deliberately private shared serialization import;
- no skip-if-absent integration test is wanted; and
- `embed_approved_assignment.py` remains a one-time Gate-3 transition utility.

The approved result remains exactly one retained development row:

```text
run_id
  scenario_dev_t01_f000_r00_S_dataset0

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

base config hash
  dev-712abf27c3f8f3c331ae9b76e3f22c48857334cc15a81e819718165e47753e56

assignment hash
  dev-eec59ec8a296a9a4ff4909f8e7f1de91a0a8f4bf289ae1533a427d1a87bc33f1

overrides
  None

identity
  20 / 20 fields equal

plant
  20 / 20 fields equal in dtype, shape, and values

S observation
  38 / 38 entries equal in dtype, shape, and values
  531 NaNs matched position-for-position across 5 entries
```

This is a one-row construction positive control only. It never generalizes to the
retained 472-reservation dataset.

## Stage-0 implementation review is open at Claude's owner step

Claude Session 47 accepted Codex's Session-46 production corrections, then added a
timing/config equality guard because three Stage-0 pins are also bound config values:

```text
window         768    <-> values.timing.window_steps
f_ctrl_hz      500.0  <-> values.timing.f_ctrl_hz
diagnostic_hz  0.8    <-> values.timing.diagnostic_probe.frequency_hz
```

The other four pins are deliberately excluded. `pairs`, `seed`, and `pair_id` have no
config counterparts. `thermal_ramp_c = 3.0` is an imposed linear sensor-path excursion,
not the sinusoidal plant-side validation environment that happens to use amplitude
`3.0`.

Codex Session 47 reviewed and explicitly approved the production file unchanged:

```text
Reproducibility Packet/scripts/analyze_synchronous_difference_null.py
  git blob    8435c764a76cb091278ffa47f14584dbf43b40ce
  raw sha256  4a9fc5955bb5d0f103d258525ee80f5766e0e9a46b01975c76ab895c53815b24
  bytes       40,098
  encoding    UTF-8, no BOM, pure LF
```

Approved production behavior:

- one `PINNED_CLI` object owns the seven decision values;
- parser defaults, identity, and executable pin guard share that object;
- tuned decision values raise before input reads or output creation, including under
  `python -O`;
- `sensor_config_from_document()` requires an exact field set and constructs the
  measurement config from the loaded, hash-bound document;
- `run_null()` requires that explicit config and has no default;
- the thermal profile requires the bound `reference_temperature_c`;
- `require_bound_timing_matches_cli()` requires exact equality for the three shared
  timing values and returns what it read for disclosure;
- equality is used instead of adoption so Protocol P remains authoritative;
- the main order is assignment binding, sensor binding, timing binding, identity,
  measurement, then output; and
- no output directory is created on a refused state.

### Current-lineage reachability boundary

`validate_approved_assignment_binding()` reconstructs the pre-embedding parent config
with `scenario_manifest = None`, restores the parent open gates and parent hash, and
recomputes the canonical config hash. Therefore, a rehashed change to either `timing`
or `sensor_model` fails the binding gate before either bound-value guard runs.

Within the current I1-pinned assignment lineage, a later valid sensor-model or timing
change cannot merely move the artifact identity while leaving measurement stale. It
requires a new draft lineage, replacement assignment, and new I1 pin. Both bound-value
guards defend code today — a skipped/reordered binding gate or future caller — and
become live data checks when the pre-confirmatory lineage is legitimately re-derived.
Carry this qualifier into the Technical Report.

### Codex's two test-evidence corrections

Claude's handed-back test blob had two evidence defects:

1. a test described a divergent config as currently constructible end to end even
   though it monkeypatched the real binding gate away; and
2. the test claiming to pin binding-gate behavior reimplemented the parent-hash
   arithmetic locally and never called the production gate.

Codex corrected them:

- the bypass test now explicitly models a skipped/reordered binding gate and disclaims
  a current end-to-end data state; and
- the architectural test now loads the real config/assignment, requires the control
  binding to pass, mutates timing or sensor config, rehashes the current config to avoid
  a stale-self-hash shortcut, and requires the real production binding gate to reject
  parent reconstruction.

The reviewer-edited test state is:

```text
Reproducibility Packet/tests/test_synchronous_difference_null.py
  git blob    9591c91bd6412a9dd60860e05c40fcbcccc9ff74
  raw sha256  2fe39d831fa500d5183108ee4aed6590ac676af8beafec122b9af4919c9402ff
  bytes       44,285
  encoding    UTF-8, no BOM, pure LF
  tests       99
```

The focused total is 117 only when the unchanged 18
`test_gauge_windows.py` tests are included. Claude's Session-47 per-file description
`99 -> 117` is forward-corrected; the actual file moved from 81 to 99.

Claude must owner-review this exact test blob and explicitly approve or edit-and-return
it. The Session-47 handoff did not explicitly approve the extended state as a whole, so
the next owner turn must make approval unambiguous.

### Already-approved helper/floor files

Do not re-review or edit without new evidence:

```text
Reproducibility Packet/scripts/utils/gauge_windows.py
  git blob    7f7c09da3079ff2498a7240922a77b95ed116b7b
  raw sha256  646d8c4e3c4d7dbe76fc8d1523a9a7b4b7ccdbf2d8509589da98af1057e8d5cb

Reproducibility Packet/scripts/analyze_synchronous_detection_floor.py
  git blob    b99fe33357701c0a5285773146ec7986db6b7a82
  raw sha256  ccc58d45fd05c1dab8dbf8886581d165783f9d23e9eebe4e5fc91aa91c422126

Reproducibility Packet/tests/test_gauge_windows.py
  git blob    925b0bd842a8a2787516753217f28d06d3000c6c
  raw sha256  cb6e49d9e6baf4541eafce9ef1c1f450eb03c95e074d380a7a4035cbaf2397f0
  tests       18
```

The closed detection-floor artifacts remain:

```text
summary.json
  4937e885c076f0950fefc3ce813f610028250ea12f9e57436d76324c071c2c67

synchronous_detection_floor_report.md
  1f5cbfea807878a81237e89eabf71f07a8106b5dc111aaf04925fe9801ac08c1
```

Any future edit to `gauge_windows.py` must re-run the closed screen to scratch and
require both published outputs byte-identical unless a new reviewed evidence state is
explicitly intended.

## Stage-0 pins and meaning

After owner approval, the only authorized decision CLI is:

```text
window          768
f_ctrl_hz       500.0
diagnostic_hz   0.8
thermal_ramp_c  3.0
pairs           100
seed            0
pair_id         1
```

Consecutive seed pairing consumes `(0,1), (2,3), ..., (198,199)`. One sample is one
pair of four-gauge windows reduced to:

```text
D = || concat_{g=0..3} (b_g(A) - b_g(B)) ||_2
```

Stage 0 has zero plant rollouts. It measures only the sensor-path contribution to the
difference operation. It sets no threshold, gates nothing, and cannot establish
mechanics, detection, attribution, action authority, controller outcome, or the project
hypothesis. Its artifact identity is `dev-` prefixed and confirmatory-ineligible.

The prior fixed-trace per-cell Q95 range
`0.3176 / 0.3555 / 0.3854 / 0.4251 microstrain` is corroboration only.
`q95_inside_real_plant_range` is a range statement, not a test. The operative null
remains Stage C's `Q95_c`.

## Jointly approved generator seam

The seam implementation-review loop remains closed:

```text
Reproducibility Packet/scripts/utils/assignment_generator.py
  git blob    1c565888edd6e538cbb281894ab6c4cdc418bb6b
  raw sha256  07fbbe563b5a904eba2d57f58e436e84975d2891ea7ebf4cac9f24253ce5b06b

Reproducibility Packet/tests/test_assignment_generator_screen_overrides.py
  git blob    2ec96c9f995fa9e9efad0000af1d3364a4994db4
  raw sha256  69f1df3145e58a68ceccd698e198afa030391e00adc3b8be518335a2924f0635
  tests       37
```

Approved behavior:

- `ScreenOverrides` has five optional fields and `is_active()` uses `is not None`;
- probe peak/ramp overrides reach the real plant and fail on invalid combinations;
- `physical_faults=()` remains an active healthy override;
- active provenance is nonempty, `dev-` plus 64 lowercase hex, and base-distinct;
- provenance reaches online and post-hoc observation construction;
- a supplied realized pair id stays suffix-free;
- `overrides=None` preserves the base hash and `_dataset0` identity;
- the seam mutates no assignment and writes no role artifact; and
- inactive overrides carrying provenance raise rather than discard an identity claim.

I13a, I3-I8 orchestration, and results-only persistence remain stage-driver concerns.

## Permanent I13b test

```text
Reproducibility Packet/tests/test_cable_plant_softening_boundary.py
raw sha256:
  712d2165f8bd96d5e88a07e5f76c53313cb5e6aca5c6d0d21af43914c3e26ac7
git blob:
  ca0f44743b3e7b4f4268e596fc82f6e1bbee2411
tests:
  6
```

It checks actual model swap at onsets 1, 5, and 500, pins
`_step_index(1.0, 0.002) == 500`, records omitted-onset activation at step 0, and checks
that a healthy plant never constructs or activates a softened model. It must remain
green before every stage.

## Stage-driver gates after Stage 0

No Stage-A/B/C driver exists and none is authorized. Its later review must require:

1. a closed-vocabulary `screen_physical_faults` helper;
2. healthy requires severity absent and returns `()`;
3. structural requires finite severity in `(0, 1]` and returns one complete `FaultSpec`
   with onset derived from trajectory time and control timestep;
4. field-by-field I13a equality before each rollout;
5. a complete `ScreenOverrides` bundle, never partial;
6. I3 reservation-difference equality and suffix-free I4;
7. I5-I8 identity/CRN/provenance checks;
8. explicit Protocol-P condition keys, never a stale returned assignment label;
9. no persisted `ObservedRecord`, label, manifest, role index, or dataset payload; and
10. a test around the real results-only output root that fails on a wrong dataset write.

The seam can represent a partial low-level bundle. That is not driver authorization.

## Required execution order

```text
Protocol P v2.3.3 exact-state approval                COMPLETE
permanent I13b exact-state approval                   COMPLETE
generator seam exact-state approval                   COMPLETE
one-row replay result                                 COMPLETE / APPROVED
replay-gate implementation                            COMPLETE / JOINTLY APPROVED
Stage-0 implementation owner re-review                NEXT / REQUIRED
Stage-0 execution                                     AFTER LOOP CLOSE
Stage-0 result/artifact review                        REQUIRED
Stage A/B/C driver implementation and review          LATER
Stage A                                               AFTER DRIVER APPROVAL
Stage B                                               AFTER STAGE A
Stage C                                               AFTER STAGE B
result/terminal-branch review                         REQUIRED
written Amendment A2 + replacement assignment        LATER
from-zero non-test regeneration and re-audit          LATER
Gates 4-7 -> joint final freeze -> confirmatory run   LATER
```

## Protocol-P design retained in substance

Do not reopen without new evidence:

- universe: dev diagnostic trajectory `t01`, cells 4/5/6/7;
- replay gate: one exact row;
- Stage 0: 100 synthetic sensor-only paired differences, zero plant rollouts;
- Stage A: 9 candidates x 4 cells x `{healthy, remEI 0.75, remEI 0.35}` = 108;
- Stage B: 10 remaining-EI values x 4 cells, reusing 0.75 and 0.35 = 32 new;
- Stage C: 8 healthy replicates per cell, reusing k=0 = 28 new;
- total plant rollouts including replay: 169;
- statistic: four-gauge matched 0.8-Hz cosine/sine coefficient difference, eight entries;
- operative null: per-cell 0.95 quantile with `method="higher"` over 28 healthy distances;
- pass: `D(v,c) >= 2.0 * Q95_c` in every screened cell;
- selection: maximize worst-cell `D` at remEI 0.75; 1% ties choose lower amplitude then
  larger ramp fraction;
- candidate peaks 0.05-0.40 N and ramps 0.125/0.25/0.5;
- torque gate admits only 0.05/0.10/0.15 N, including equality at 0.15 N;
- measurement origin: probe start;
- Stage-A/B signal identity-matched; Stage-C null unmatched and favorable to S;
- gauge-only and unmatched secondaries descriptive only;
- OOD 0.45/0.55 excluded from known-class macro-F1; and
- all outputs development-only and confirmatory-ineligible.

The honest prior remains that remEI 0.75 likely fails widely and remEI 0.50 is near the
boundary under earlier optimistic projections. That is a prior, not a result.

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

Protocol-P seam:
  exact state jointly approved

Protocol-P replay result and implementation:
  jointly approved

Stage 0:
  production implementation approved by both agents in substance
  reviewer-edited test state awaiting Claude owner re-review
  not run

Stage A/B/C:
  unauthorized and unimplemented

Amendment A2:
  not written or approved

Gates 4-7:
  open

final config.json:
  absent
```

The local ignored retained dataset contains 472 dev/pilot/validation reservations, 944
C1/S manifest rows, and zero test rows. It was not regenerated. If a written Amendment
A2 and replacement assignment later receive same-state approval, Codex's standing
choice is coherent from-zero regeneration, not an in-place patch.

## Evidence boundary

Keep separate:

- construction correctness;
- safety/admissibility;
- structural detectability;
- fault attribution;
- information/action authorization;
- controller outcome; and
- confirmatory evidence.

The replay is a construction positive control only. Stage 0 will be a sensor-path
diagnostic only. Prior structural-separability outputs are development diagnostics, not
pilot, validation, confirmatory, or frozen margins.

## Verification baseline

Use only the repository venv:

```powershell
.\venv\Scripts\python.exe -m pytest -q "Reproducibility Packet\tests"
```

Codex Session 47:

```text
Stage-0 test file                   99 passed in 1.45 s
Stage-0 + gauge-helper files       117 passed in 1.50 s
full packet suite                  595 passed in 12.56 s
compileall                         clean
accept-all binding-gate mutant     caught
```

Do not run root-wide `pytest -q`; ignored duplicate trees under `tmp/` can pollute
collection.

Before binary replay decisions, use raw hashes only. Before exact-state approval,
independently compute raw bytes, BOM/EOL state, raw SHA-256, git blob, and git attributes.

Before any commit:

```powershell
git diff --check
git diff --cached --check
```

CRLF warnings alone are not a reason to churn unrelated files.

## Transcript-order state

The active transcript is append-only. Session-47 append verification:

```text
pre-write lines:
  10,414
pre-write bytes:
  773,918
pre-write sha256:
  9a600a18950aeda8c884e021b42d2420d5e54b868802b8f94e327786e42c3e01
Codex header:
  line 10,418
  count 1 total
  after old boundary
old byte prefix:
  exact
technical diff:
  +159 / -0
post-write lines:
  10,573
post-write bytes:
  781,095
post-write sha256:
  b266a49416aabd3ccedbf6d12f4dfdf85c6809b38dc16b260d3926c5dd4c6104
physical last author:
  Codex
```

The first patch attempt changed nothing because the terminal-rendered sign-off did not
match the stored Unicode em dash. The hard gate stopped safely; the successful patch
used the literal UTF-8 EOF block. No recurrence occurred, so the monitoring thread was
not updated.

For every future append:

1. read the UTF-8 physical EOF tail;
2. record line count, byte count, and SHA-256;
3. verify a complete multi-line EOF anchor occurs exactly once;
4. patch using that complete verified anchor;
5. verify the new header occurs once after the old boundary;
6. verify the old byte prefix is exact;
7. reread the physical tail; and
8. require additions-only transcript diff.

If any check fails, stop and repair by dated append-only correction.

## Public README

The root README is a public append-only running log. Session 47 changed an internal,
still-open implementation-review state without producing a Stage-0 result, closing an
artifact, or advancing phase. The live-run heartbeat therefore required no update.

Do not add a public entry merely for routine owner approval unless it changes the
publicly meaningful state. Run the heartbeat every session against
`Playbooks/live-run-readme.md`.

## Required next actions

1. Read controlling instructions, this continuity file, all Codex-relevant chat
   summaries, and the active transcript before replying.
2. Read Claude's newest report and owner re-review turn.
3. Verify Claude reopened the reviewer diff and reproduced:

   ```text
   analyze_synchronous_difference_null.py
     8435c764a76cb091278ffa47f14584dbf43b40ce

   test_synchronous_difference_null.py
     9591c91bd6412a9dd60860e05c40fcbcccc9ff74
   ```

4. If Claude explicitly approves that same state, record that the Stage-0 implementation
   loop is closed.
5. Only after loop closure, allow the one pinned Stage-0 execution.
6. Review the Stage-0 identity, canonical string, samples, distribution, output path,
   elapsed time, and no-authority boundaries before any later work.
7. Keep Stage A/B/C and the later driver unauthorized until that result review closes.
8. Keep final `config.json` absent and the test split untouched.
9. Write Codex's regular Session-48 progress report after normal work.
10. Close out with the next HumanReport, README heartbeat, Codex workspace README,
    complete continuity rewrite, hygiene checks, exact commit message, and push.

## Non-negotiable boundaries

- Approval is explicit and exact-state-specific.
- Preserve owner/reviewer lanes.
- Never treat development, screen, pilot, fixture, replay, or Stage-0 evidence as
  confirmatory.
- Never convert construction correctness into detection or attribution.
- Never convert safety into proof of correct construction.
- Never convert detection into attribution or action authority.
- Never silently rewrite a public or transcript-facing overclaim; append a correction.
- Never normalize binary artifacts before exact hashing.
- Never run a stage from unapproved implementation.
- Never run stages out of order.
- Never create final `config.json` before all gates close jointly.
- Never touch the test split before confirmatory authorization.
- Use append-only transcript hard gates and preserve exact requested commit messages.
