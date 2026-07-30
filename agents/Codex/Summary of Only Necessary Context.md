# Summary of Only Necessary Context — Codex

**Rewritten:** 2026-07-29, Codex Session 46

**Phase:** Phase 2 — Integration and Reproducibility Build

**Config:** **UNFROZEN**; `Reproducibility Packet/config.json` is absent

**Current decision:**

```text
ACKNOWLEDGE_REPLAY_GATE_IMPLEMENTATION_LOOP_CLOSED
BLOCK_STAGE_0_IMPLEMENTATION_CLAUDE_HANDOFF_STATE_ON_CONFIG_TO_MEASUREMENT_BINDING
APPROVE_STAGE_0_IMPLEMENTATION_REVIEWER_EDITED_STATE
REQUIRE_CLAUDE_OWNER_REREVIEW_BEFORE_STAGE_0_EXECUTION
AFTER_LOOP_CLOSE_AUTHORIZE_STAGE_0_EXECUTION_ONLY
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

Its physical last turn is **Codex Session 46**, beginning at line 10,035.

Claude owns the Stage-0 implementation and must genuinely owner-re-review Codex's
five-file reviewer-edited state. Codex owns exact-state review. Do not run Stage 0 and
do not take Stage-A/B/C driver ownership unless the active thread explicitly changes
that authorization.

The next action is only Claude's owner re-review of:

```text
Reproducibility Packet/scripts/analyze_synchronous_difference_null.py
Reproducibility Packet/scripts/utils/gauge_windows.py
Reproducibility Packet/scripts/analyze_synchronous_detection_floor.py
Reproducibility Packet/tests/test_synchronous_difference_null.py
Reproducibility Packet/tests/test_gauge_windows.py
```

The implementation loop closes only when Claude explicitly approves the same reviewer-
edited state. After that closure, exactly one pinned Stage-0 execution is authorized.
The result/artifact must be reviewed before any later driver work. Stage A/B/C
implementation and execution remain unauthorized.

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

Claude Session 46 genuinely re-reviewed Codex's corrections and approved them. The
replay-gate implementation loop is closed:

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

- data root and packet tree are watched recursively;
- repository top-level files are watched as a shallow namespace re-enumerated after
  replay;
- any added, modified, or removed watched file raises before final PASS;
- the report discloses a denominator and refuses a snapshot below the 100-file
  anti-vacuity floor;
- incompatible dtype drift reaches a named `ProtocolPError`;
- `_plant_payload` remains a deliberately private shared serialization import;
- no skip-if-absent integration test is wanted; and
- `embed_approved_assignment.py` remains a one-time Gate-3 transition utility.

Claude additionally verified the real CLI wire by creating a new repository-top-level
file eight seconds into a replay. The gate discovered the previously unknown name,
raised `ProtocolPError`, omitted PASS, and exited 1. That scratchpad technique should be
rebuilt when this gate or the later stage driver changes; it should not become a
skip-by-default permanent test.

The approved replay result remains exactly one retained development row:

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

This proves one-row exact construction and is an end-to-end regression on the approved
seam's all-`None` path. It never generalizes to the retained 472-reservation dataset.

## Stage-0 implementation review is open at the owner step

Claude's handoff correctly implemented the four-gauge difference statistic, exact seed
universe, Stage-0 identity/canonical string, output-schema binding, `method="higher"`
Q95, no-authority corroboration, and a shared gauge-window helper. Codex found a blocking
configuration wire:

```text
identity:
  bound loaded base_config_hash

measurement:
  independently constructed SensorConfig() defaults
```

The current draft's sensor block equals the defaults exactly, so the defect changed no
current number and all 565 handoff-state checks passed. Under a future valid sensor-model
change, however, the identity would move while the measurement silently remained on old
defaults.

Codex corrected that class and explicitly approved this exact state:

```text
Reproducibility Packet/scripts/analyze_synchronous_difference_null.py
  git blob    d68b622baac53335ad4b7c58d6a8440e5dbf8904
  raw sha256  624f3a304853a6ef25ef795f26356df2243ded16176867f8f3261bcaacf61f0e
  bytes       34,791

Reproducibility Packet/scripts/utils/gauge_windows.py
  git blob    7f7c09da3079ff2498a7240922a77b95ed116b7b
  raw sha256  646d8c4e3c4d7dbe76fc8d1523a9a7b4b7ccdbf2d8509589da98af1057e8d5cb
  bytes       6,806

Reproducibility Packet/scripts/analyze_synchronous_detection_floor.py
  git blob    b99fe33357701c0a5285773146ec7986db6b7a82
  raw sha256  ccc58d45fd05c1dab8dbf8886581d165783f9d23e9eebe4e5fc91aa91c422126
  bytes       19,540

Reproducibility Packet/tests/test_synchronous_difference_null.py
  git blob    2dc659926090a968e07a7e7da8e65a99c7659b5f
  raw sha256  77530d416f866df6db943b84bce3cd86bd00a6d6f9ff9d13945eeb92ab00064c
  bytes       33,075
  tests       81

Reproducibility Packet/tests/test_gauge_windows.py
  git blob    925b0bd842a8a2787516753217f28d06d3000c6c
  raw sha256  cb6e49d9e6baf4541eafce9ef1c1f450eb03c95e074d380a7a4035cbaf2397f0
  bytes       8,225
  tests       18
```

All five were UTF-8 without BOM and pure LF in the reviewed checkout. Protocol P does
not hash source files, so git blobs are the checkout-EOL-stable review handles and
`.gitattributes` remains unchanged.

Current corrected behavior:

- one `PINNED_CLI` object owns the seven decision values;
- parser defaults, the identity, and the executable guard share that object;
- tuned decision values raise before input reads or output creation, including under
  `python -O`;
- `sensor_config_from_document()` requires an exact field set and constructs the
  measurement config from the loaded, hash-bound document;
- `run_null()` requires that explicit config and has no default;
- the thermal profile requires the bound `reference_temperature_c`; the duplicated
  25 °C constant is gone;
- the closed detection-floor screen passes its existing reference explicitly;
- the main config→measurement→document→writer wire is tested with a deliberately
  non-default sensor value;
- `run_null()` is tested to respond to the supplied config;
- the helper shortcut is compared with public `OnlineSensorSession.observe_step` gauge
  values and validity; and
- the helper claims the value/validity path only. Latency remains availability metadata
  outside this helper.

Verification:

```text
focused Stage-0/helper files    99 passed in 1.45 s
full packet suite              577 passed in 12.58 s
compileall                      clean
semantic mutation sweep         9 / 9 caught
tuned --pairs 99               exit 1; no output
tuned under python -O          exit 1; no output
```

The shared helper feeds a closed screen. Any future edit must re-run
`analyze_synchronous_detection_floor.py` to scratch and require both published outputs
byte-identical unless a new reviewed evidence state is explicitly intended. Session 46
verified:

```text
summary.json
  4937e885c076f0950fefc3ce813f610028250ea12f9e57436d76324c071c2c67

synchronous_detection_floor_report.md
  1f5cbfea807878a81237e89eabf71f07a8106b5dc111aaf04925fe9801ac08c1
```

## Stage-0 pins and meaning

The only authorized decision CLI after owner approval is:

```text
window          768
f_ctrl_hz       500.0
diagnostic_hz   0.8
thermal_ramp_c  3.0
pairs           100
seed            0
pair_id         1
```

Consecutive seed pairing consumes `(0,1), (2,3), ..., (198,199)`. One sample is one pair
of four-gauge windows reduced to:

```text
D = || concat_{g=0..3} (b_g(A) - b_g(B)) ||_2
```

Stage 0 has zero plant rollouts. It measures only the sensor-path contribution to the
difference operation. It sets no threshold, gates nothing, and cannot establish
mechanics, detection, attribution, action authority, controller outcome, or the project
hypothesis. Its artifact identity is `dev-` prefixed and confirmatory-ineligible.

The prior fixed-trace per-cell Q95 range `0.3176 / 0.3555 / 0.3854 / 0.4251 µε` is
corroboration only. The artifact's `q95_inside_real_plant_range` is a range statement,
not a test. The operative null remains Stage C's `Q95_c`.

## Jointly approved generator seam

The seam implementation-review loop remains closed on:

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
owner approval:
  Claude Session 43
reviewer approval:
  Codex Session 43
```

It checks actual model swap at onsets 1, 5, and 500, pins
`_step_index(1.0, 0.002) == 500`, records omitted-onset activation at step 0, and checks
that a healthy plant never constructs or activates a softened model. It must remain
green before every stage.

## Stage-driver gates after Stage 0

No stage driver exists and none is authorized yet. Its later review must require:

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
- Stage A: 9 candidates × 4 cells × `{healthy, remEI 0.75, remEI 0.35}` = 108;
- Stage B: 10 remaining-EI values × 4 cells, reusing 0.75 and 0.35 = 32 new;
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
- Stage-A/B signal identity-matched; Stage-C null unmatched and favourable to S;
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
  implemented in reviewer-edited state
  Claude owner re-review open
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

Codex Session 46:

```text
focused Stage-0/helper tests    99 passed in 1.45 s
full packet suite              577 passed in 12.58 s
compileall                      clean
semantic mutations              9 / 9 caught
closed floor outputs            byte-identical
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

The active transcript is append-only. Session-46 append verification:

```text
pre-write lines:
  10,031
pre-write bytes:
  755,841
pre-write sha256:
  0099d4d7b08476663e9bced9deea1491f31ea826d1aad4276326a763660adde3
Codex header:
  line 10,035
  count 1 total
  after old boundary
old byte prefix:
  exact
technical diff:
  +177 / -0
post-write lines:
  10,208
post-write bytes:
  764,050
post-write sha256:
  094565356bdf1d4028b18ac20fb607e4265dca1468bed66633ee0f95f42785c8
physical last author:
  Codex
```

No recurrence occurred, so the monitoring thread was not updated.

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

The root README is a public append-only running log. Claude Session 46 already added the
publicly meaningful state: the replay-gate loop closed, 565 checks were green at handoff,
and Stage 0 was written but not run. Codex Session 46 changed an internal implementation
review state without changing that public truth, producing a result, completing an
artifact, or advancing phase. The live-run heartbeat therefore required no new entry.

Do not add a public entry merely for routine owner re-approval unless it changes the
publicly meaningful state. Run the heartbeat each session against
`Playbooks/live-run-readme.md`.

## Required next actions

1. Read controlling instructions, this continuity file, all Codex-relevant chat summaries,
   and the active transcript before replying.
2. Read Claude's newest report and owner re-review turn.
3. Verify Claude reopened the exact five reviewer-edited files and reproduced their blobs.
4. If Claude explicitly approves those same hashes, record that the Stage-0 implementation
   loop is closed.
5. Only after loop closure, allow the one pinned Stage-0 execution.
6. Review the Stage-0 identity, canonical string, samples, distribution, output path,
   elapsed time, and no-authority boundaries before any later work.
7. Keep Stage A/B/C and the later driver unauthorized until that result review closes.
8. Keep `config.json` absent and the test split untouched.
9. Close out with Codex `HumanReport47.md`, README heartbeat, Codex workspace README,
   complete continuity rewrite, hygiene checks, exact commit message, and push.

The next regular Codex progress report is Session 48 unless a phase transition or
approved written Claim Sheet amendment triggers one earlier.

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
