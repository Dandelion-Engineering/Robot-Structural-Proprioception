# Summary of Only Necessary Context — Codex

**Rewritten:** 2026-07-30, Codex Session 48

**Phase:** Phase 2 — Integration and Reproducibility Build

**Config:** **UNFROZEN**; final `config.json` is absent

**Current decision:**

```text
APPROVE_STAGE_0_RESULT_ARTIFACT_UNCHANGED_AT_EXACT_COMMITTED_STATE
ACCEPT_NO_PROTOCOL_VERSION_CHANGE_FOR_ROUGHLY_0_39_VS_EXECUTED_0_400881
REQUIRE_CLAUDE_EXPLICIT_OWNER_APPROVAL_OF_THE_EXACT_RESULT_ARTIFACT
STAGE_0_RESULT_REVIEW_REMAINS_OPEN
REQUIRE_OWNER_REREVIEW_OF_REVIEWER_EDITED_PROGRESS_REPORT
STAGES_A_B_C_REMAIN_UNAUTHORIZED
BLOCK_CONFIG_FREEZE_PENDING_PRECONFIRMATORY_BUILD_AND_VALIDATION
```

Stage 0 **has run exactly once** at the pinned invocation and spent zero plant
rollouts. Protocol P's plant-rollout count remains **one**, the Session-45 replay. The
confirmatory test split remains untouched.

## Resume here

The authoritative active thread is:

```text
chats/Claude-Codex/Phase 2 Integration and Config Freeze/
  Phase 2 Integration and Config Freeze - Active.md
```

Its physical last turn is **Codex Session 48**, beginning at line 10,829.

Claude's next turn has two exact-state owner tasks:

1. re-open and explicitly approve or edit-and-return the unchanged Stage-0 result
   artifact at Git blob
   `31c1e6d1824c10bd5978d12c377f76cf556af03f`; and
2. genuinely re-review and explicitly approve or edit-and-return Codex's three
   corrections to Claude's Session-48 progress report at Git blob
   `36ba0221540582b04f7f35029f7a38f3649a60ff`.

The result artifact is technically approved by Codex unchanged. The result loop remains
open only because Claude's initial result turn created, audited, and handed off the file
without explicitly approving that exact state. Creation, self-audit, handoff, and
silence are not approval.

Do not start the Stage-A/B/C driver or add the Stage-0 packet README step until the
result artifact receives Claude's explicit same-state approval.

Codex's next session is Session 49. The next regular Codex progress report is Session 56
unless a phase transition or approved written Claim Sheet amendment triggers one first.

## Stage-0 implementation loop is closed

The jointly approved implementation state is:

```text
Reproducibility Packet/scripts/analyze_synchronous_difference_null.py
  git blob    8435c764a76cb091278ffa47f14584dbf43b40ce
  raw sha256  4a9fc5955bb5d0f103d258525ee80f5766e0e9a46b01975c76ab895c53815b24
  bytes       40,098

Reproducibility Packet/tests/test_synchronous_difference_null.py
  git blob    9591c91bd6412a9dd60860e05c40fcbcccc9ff74
  raw sha256  2fe39d831fa500d5183108ee4aed6590ac676af8beafec122b9af4919c9402ff
  bytes       44,285
  tests       99
```

Both are UTF-8 without BOM and pure LF in the approved state.

Claude Session 48 genuinely re-reviewed Codex's two test-evidence corrections through a
five-case mutation sweep and explicitly approved the exact two-file state before
execution. The implementation loop is closed at round three.

The three already-approved helper/floor files remain:

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

The focused total is 117 across the 99-test Stage-0 file and unchanged 18-test helper
file.

## Executed Stage-0 artifact

```text
Reproducibility Packet/results/protocol_p/sensor_only_difference_null.json
  git blob    31c1e6d1824c10bd5978d12c377f76cf556af03f
  git bytes   6,588
  checkout    6,765 bytes, UTF-8, no BOM, 177 CRLF line endings
  raw sha256  4101c0b8dcc1c3ee01b37433ccb3563d4c1e15e5e22cd8094979645d36a40cae
```

The JSON is not raw-byte pinned; Git normalizes the checkout to the blob above. Its
operative identity is the digest of the embedded canonical string, not the checkout
file hash:

```text
stage_0_identity
  dev-71b332893d007036625f666589f8c74b0ac3b946b47b5186ddf8de6a2d8ce31e

stage_0_canonical
  650 characters

identity rule
  dev- + sha256(stage_0_canonical UTF-8)
```

The pinned invocation was:

```powershell
Set-Location "Reproducibility Packet"
..\venv\Scripts\python.exe scripts\analyze_synchronous_difference_null.py --window 768 --f-ctrl-hz 500.0 --diagnostic-hz 0.8 --thermal-ramp-c 3.0 --pairs 100 --seed 0 --pair-id 1
```

The executed distribution is:

```text
n pairs             100
sensor seeds        0..199, consumed once by consecutive pairing
pair_id             1
mean                0.2787343038701652
population std      0.0747731492497055
minimum             0.11499432424888396
median              0.2797011174389474
maximum             0.5698763540282215
q95, higher         0.4008810868833315
values > q95        4
values >= q95       5
```

Codex Session 48 independently parsed the artifact with duplicate-key rejection and
reproduced:

- the top-level schema;
- canonical JSON rendering;
- `dev-` identity;
- all seven CLI pins;
- config self-hash;
- assignment self-hash;
- production assignment/config binding;
- protocol and assignment canonical digests;
- protocol filename, stage, and zero-rollout fields;
- sample count, finiteness, seed range, and pair id;
- mean, population standard deviation, min, median, max, and manual `higher` Q95;
- fixed-trace constants and range containment; and
- the no-authority boundary text.

Codex did not call `run_null()` or execute Stage 0 again.

## Stage-0 scientific meaning

Stage 0 measures:

```text
D = || concat_{g=0..3} (b_g(A) - b_g(B)) ||_2
```

for 100 pairs of four-gauge windows with zero mechanical strain, the same imposed
thermal profile, and different sensor identities.

It has:

- no plant;
- no mechanics;
- no fault;
- no reservation;
- no rollout;
- no threshold;
- no verdict authority; and
- a `dev-` identity permanently ineligible for confirmatory analysis.

It is conditional on this pair id, window, thermal profile, bound sensor model, and
difference operation. A single-window threshold is a different object.

The prior fixed-trace per-cell values are:

```text
cell 6  0.3176
cell 4  0.3555
cell 7  0.3854
cell 5  0.4251
```

The executed `0.400881`:

- is 2.790% above Protocol P's approximate `roughly 0.39`;
- is inside the pre-registered `[0.3176, 0.4251]` range;
- exceeds three of the four cell values; and
- is 5.697% below the range maximum.

No Protocol-P version change is needed. `roughly 0.39` is an approximation, not a pin;
range containment is the pre-registered corroboration; and Stage 0 gates nothing.

The only licensed language is **conditional broad-range containment**. Do not call it
central agreement, population agreement, a test, a detection threshold, mechanics
evidence, or evidence for the project hypothesis.

The operative null remains Stage C's per-cell `Q95_c`.

## Missing first-run elapsed time

Session 47 said elapsed time would be recorded when the approved implementation ran.
It was not captured in the artifact, result turn, human report, or progress report.

The first-run wall clock is unknown and cannot be reconstructed from commit or transcript
timestamps. Protocol P does not bind runtime, so this does not block the artifact.

Do not execute Stage 0 again merely to manufacture a first-run number. When the packet
README step is written after result approval, say:

```text
first-run elapsed time: not captured
```

unless a later, separately authorized reproduction is timed and clearly labeled as a
later reproduction.

## Public and director-facing corrections

Claude's new public README entry said:

- any damage signal smaller than `0.401` is invisible; and
- the assignment/config binding check was a safety gate.

Both crossed a project boundary. Stage 0 sets no detection threshold, and input
integrity is not physical safety or admissibility.

The root public README is append-only. Codex preserved the prior entry and appended a
dated correction that:

- says `0.401` is not a detection threshold;
- names Stage C's per-cell null and `D(v,c) >= 2 × Q95_c` rule as the later screen
  authority;
- calls the mutated check an assignment/configuration binding-integrity gate;
- separates it from physical safety; and
- clarifies that the implementation passed review before execution while the result
  artifact is in a separate exact-state review.

Codex also directly edited:

```text
agents/Claude/Progress Reports/Progress Report Session 48.md
  reviewer-edited git blob  36ba0221540582b04f7f35029f7a38f3649a60ff
  review diff               +9 / -6
```

The report edits:

1. replace "noise floor / smaller is invisible" with the no-threshold boundary;
2. replace "two routes agree" with limited broad-range containment; and
3. correct "five exceed" to "five are at or above; four exceed."

Codex explicitly approved the reviewer-edited report. Claude must genuinely owner-review
and explicitly approve or edit-and-return that exact state.

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

The specification loop is closed on that digest. Do not edit the file in place. A
source-checkable future defect requires the next version by `git mv`, both exact-state
approvals, and a new digest before any affected stage runs.

## Jointly approved replay gate and one-row result

```text
Reproducibility Packet/scripts/protocol_p_replay_gate.py
  git blob    7d3309b7a114a20a67f5e4adf7504dad0ca0897a
  raw sha256  3217142aabf8a13fb06fc7c68b84d3cbb0311a3b1e6d6bb5ca1c9af520495c85

Reproducibility Packet/tests/test_protocol_p_replay_gate.py
  git blob    6a7e7774287d727b78ed3c9d323843c6dc1e37a3
  raw sha256  3fbf9822a88d277e91f5e721c55a3004a8686ccd3dea2425626bcfdc0572e288
  tests       36
```

The replay result remains exactly one retained development row:

```text
run_id
  scenario_dev_t01_f000_r00_S_dataset0

plant
  20 / 20 fields equal in dtype, shape, and values

S observation
  38 / 38 entries equal in dtype, shape, and values
  531 NaNs matched position-for-position across 5 entries

identity
  20 / 20 fields equal

watched changes
  0
```

This is a construction positive control for one row only. It does not generalize to the
retained 472-reservation dataset.

## Jointly approved generator seam

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
  git blob    ca0f44743b3e7b4f4268e596fc82f6e1bbee2411
  raw sha256  712d2165f8bd96d5e88a07e5f76c53313cb5e6aca5c6d0d21af43914c3e26ac7
  tests       6
```

It checks model swap at onsets 1, 5, and 500, pins
`_step_index(1.0, 0.002) == 500`, records omitted-onset activation at step 0, and checks
that a healthy plant never constructs or activates a softened model. It must stay green
before every plant-bearing stage.

## Stage-A/B/C driver gates

No Stage-A/B/C driver exists and none is authorized.

Its later implementation review must require:

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

The low-level seam can represent a partial bundle. That is not driver authorization.

## Required execution order

```text
Protocol P v2.3.3 exact-state approval                COMPLETE
permanent I13b exact-state approval                   COMPLETE
generator seam exact-state approval                   COMPLETE
one-row replay result                                 COMPLETE / APPROVED
replay-gate implementation                            COMPLETE / JOINTLY APPROVED
Stage-0 implementation                               COMPLETE / JOINTLY APPROVED
Stage-0 execution                                    COMPLETE / RUN ONCE
Stage-0 result artifact reviewer approval             COMPLETE / CODEX
Stage-0 result artifact owner approval                NEXT / REQUIRED
Stage-0 packet README step                            AFTER RESULT LOOP CLOSE
Stage A/B/C driver implementation and review          LATER
Stage A                                               AFTER DRIVER APPROVAL
Stage B                                               AFTER STAGE A
Stage C                                               AFTER STAGE B
result/terminal-branch review                         REQUIRED
written Amendment A2 + replacement assignment        LATER
from-zero non-test regeneration and re-audit          LATER
Gates 4-7 -> joint final freeze -> confirmatory run   LATER
```

## Protocol-P retained design

Do not reopen without new evidence:

- universe: dev diagnostic trajectory `t01`, cells 4/5/6/7;
- replay gate: one exact row;
- Stage 0: 100 synthetic sensor-only paired differences, zero plant rollouts;
- Stage A: 9 candidates × 4 cells × `{healthy, remEI 0.75, remEI 0.35}` = 108;
- Stage B: 10 remaining-EI values × 4 cells, reusing 0.75 and 0.35 = 32 new;
- Stage C: 8 healthy replicates per cell, reusing k=0 = 28 new;
- total plant rollouts including replay: 169;
- statistic: four-gauge matched 0.8-Hz cosine/sine coefficient difference, eight
  entries;
- operative null: per-cell 0.95 quantile with `method="higher"` over 28 healthy
  distances;
- pass: `D(v,c) >= 2.0 × Q95_c` in every screened cell;
- selection: maximize worst-cell `D` at remEI 0.75; 1% ties choose lower amplitude then
  larger ramp fraction;
- candidate peaks 0.05–0.40 N and ramps 0.125/0.25/0.5;
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

Stage 0 implementation:
  jointly approved

Stage 0 execution:
  run once

Stage 0 result:
  reviewer approved unchanged
  awaiting explicit owner same-state approval

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
C1/S manifest rows, and zero test rows. It was not regenerated. After an approved written
Amendment A2 and replacement assignment, Codex's standing choice is coherent from-zero
regeneration, not an in-place patch.

## Evidence boundary

Keep separate:

- construction correctness;
- input/configuration binding;
- safety/admissibility;
- structural detectability;
- fault attribution;
- information/action authorization;
- controller outcome; and
- confirmatory evidence.

The replay is a one-row construction positive control. Stage 0 is a sensor-path
diagnostic. Neither establishes mechanics, detection, attribution, action authority,
controller outcome, or the project hypothesis.

## Verification baseline

Use only the repository venv:

```powershell
.\venv\Scripts\python.exe -m pytest -q "Reproducibility Packet\tests"
```

Codex Session 48:

```text
Stage-0 + gauge-helper files       117 passed in 1.36 s
full packet suite                  595 passed in 12.51 s
compileall                         clean
strict artifact audit             20 / 20 PASS
config.json                        absent
test-named payload files           0
.npz under results                 0
```

Do not run root-wide `pytest -q`; ignored duplicate trees under `tmp/` can pollute
collection.

Before binary replay decisions, use raw hashes only. Before exact-state approval,
independently compute raw bytes, BOM/EOL state, raw SHA-256, Git blob, and Git
attributes.

Before every commit:

```powershell
git diff --check
git diff --cached --check
```

CRLF warnings alone are not a reason to churn unrelated files.

## Transcript-order state

The active transcript is append-only. Session-48 append verification:

```text
pre-write lines:
  10,825
pre-write bytes:
  793,417
pre-write sha256:
  312d55ed78c292b66d2c1cec55d12d4aee0cb4f53ba69737cbb251684baa11a5
Codex header:
  line 10,829
  count 1 total
  after old boundary
old byte prefix:
  exact
technical diff:
  +170 / -0
post-write lines:
  10,995
post-write bytes:
  801,046
post-write sha256:
  17649439674b3aef51317cd11270fe527c3b89cc094ac216d2c8039034308460
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

## Public README state

The Session-48 Stage-0 milestone qualified for a public entry. Claude added it before
result review. Codex preserved it and appended a dated correction for the threshold,
binding-versus-safety, and implementation-review-versus-result-review distinctions.

Do not rewrite or remove either entry. Future public state should advance only for a
finished artifact, phase close, or genuinely noteworthy result. Routine owner approval
alone probably does not need another public entry unless it changes the public-facing
meaning.

## Required next actions

1. Read controlling instructions, this continuity file, all Codex-relevant chat
   summaries, and the active transcript before replying.
2. Read Claude's newest report and physical-tail owner turn.
3. Verify Claude genuinely re-opened:

   ```text
   Reproducibility Packet/results/protocol_p/sensor_only_difference_null.json
     31c1e6d1824c10bd5978d12c377f76cf556af03f

   agents/Claude/Progress Reports/Progress Report Session 48.md
     36ba0221540582b04f7f35029f7a38f3649a60ff
   ```

4. If Claude explicitly approves the unchanged result artifact, record the Stage-0
   result loop closed.
5. If Claude explicitly approves the reviewer-edited progress report, record that
   collateral report loop closed.
6. After result closure, allow Claude to write the Stage-0 packet README step with
   `first-run elapsed time: not captured`.
7. Keep Stage A/B/C unauthorized until a separate driver implementation receives
   explicit same-state approval.
8. Keep final `config.json` absent and the test split untouched.
9. Close out with the next HumanReport, README heartbeat, Codex workspace README,
   complete continuity rewrite, hygiene checks, exact commit message, and push.

## Non-negotiable boundaries

- Approval is explicit and exact-state-specific.
- Preserve owner/reviewer lanes.
- Never treat development, screen, pilot, fixture, replay, or Stage-0 evidence as
  confirmatory.
- Never convert construction correctness or input binding into safety.
- Never convert safety into proof of correct construction.
- Never convert detection into attribution or action authority.
- Never treat the Stage-0 diagnostic as a detection threshold.
- Never silently rewrite a public or transcript-facing overclaim; append a correction.
- Never normalize binary artifacts before exact hashing.
- Never run a stage from unapproved implementation.
- Never run stages out of order.
- Never execute Stage 0 again without separate authorization.
- Never create final `config.json` before all gates close jointly.
- Never touch the test split before confirmatory authorization.
- Use append-only transcript hard gates and preserve exact requested commit messages.
