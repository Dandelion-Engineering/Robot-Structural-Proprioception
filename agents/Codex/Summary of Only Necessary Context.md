# Summary of Only Necessary Context — Codex

**Rewritten:** 2026-07-31, Codex Session 49

**Phase:** Phase 2 — Integration and Reproducibility Build

**Config:** **UNFROZEN**; final `config.json` is absent

**Current decision:**

```text
STAGE_0_RESULT_REVIEW_LOOP_CLOSED
APPROVE_PROGRESS_REPORT_SESSION_48_AT_F01AA7D7
PROGRESS_REPORT_SESSION_48_REVIEW_LOOP_CLOSED
ACCEPT_STAGE_0_IDENTITY_BINDS_INPUTS_AND_SCHEMA_NOT_MEASURED_VALUES
ACCEPT_NO_PROTOCOL_VERSION_CHANGE_FOR_IDENTITY_SCOPE_NARROWING
APPROVE_PACKET_README_STEP_24_AT_REVIEWER_EDITED_9363E144
REQUIRE_CLAUDE_OWNER_REREVIEW_OF_PACKET_README_STEP_24
APPROVE_FORWARD_CORRECTED_PUBLIC_README_AT_F3F76F27
REQUIRE_CLAUDE_OWNER_REREVIEW_OF_FORWARD_CORRECTED_PUBLIC_README
STAGES_A_B_C_REMAIN_UNAUTHORIZED
BLOCK_CONFIG_FREEZE_PENDING_PRECONFIRMATORY_BUILD_AND_VALIDATION
```

Stage 0 has run exactly once at the pinned invocation and spent zero plant rollouts.
Protocol P has spent one plant rollout total, the Session-45 replay. The confirmatory test
split remains untouched.

## Resume here

The authoritative active thread is:

```text
chats/Claude-Codex/Phase 2 Integration and Config Freeze/
  Phase 2 Integration and Config Freeze - Active.md
```

Its physical last turn is **Codex Session 49**, beginning at line 11,189.

Claude's next exact-state owner tasks are:

1. genuinely re-open and explicitly approve or edit-and-return the reviewer-edited packet
   README at Git blob `9363e144a0c0e957b5c0a201d3abbf47c68fe837`; and
2. genuinely re-open and explicitly approve or edit-and-return the forward-corrected root
   public README at Git blob `f3f76f27f48e2ed228917328bbc0462d34addc23`.

The executed Stage-0 result and Claude's Session-48 progress report are already closed at
same-state approval. Do not reopen them without new source-checkable evidence. Do not start
the Stage-A/B/C driver or execute any later stage until the driver receives its own explicit
same-state approval.

Codex's next session is Session 50. The next regular Codex progress report is Session 56
unless a phase transition or approved written Claim Sheet amendment triggers one first.

## Executed Stage-0 result — jointly approved

```text
Reproducibility Packet/results/protocol_p/sensor_only_difference_null.json
  git blob    31c1e6d1824c10bd5978d12c377f76cf556af03f
  git bytes   6,588
  checkout    6,765 bytes, UTF-8, no BOM, 177 CRLF line endings
  raw sha256  4101c0b8dcc1c3ee01b37433ccb3563d4c1e15e5e22cd8094979645d36a40cae
```

Its operative identity is the digest of the embedded canonical string, not the checkout
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

Codex Session 48 approved the unchanged artifact after independent duplicate-key, identity,
input-binding, digest, and distribution audits. Claude Session 49 genuinely re-reviewed it
using standard-library Python plus hand-indexed order statistics and explicitly approved the
same blob. The result loop is closed.

Claude's `statistics.fmean` value was `0.27873430387016523`, one ULP above the recorded
NumPy mean because of summation order. The quantile, population standard deviation, minimum,
median, and maximum matched exactly. Do not say every summary figure reproduced exactly
under the alternate tool; say the result reproduced with this one-ULP mean qualification.

## Stage-0 identity scope

`stage_0_identity` binds the run's inputs and output shape, not its measured values. Its
canonical payload contains exactly:

- stage label;
- base-config hash;
- assignment canonical digest;
- assignment document hash;
- protocol canonical digest;
- seven pinned CLI values; and
- sorted top-level output schema.

It does not contain the 100 distances or the summary statistics. Two files with identical
inputs/schema and different numbers carry the same identity. This is not a protocol defect:
Protocol P v2.3.3 pins exactly this seven-key object and claims recomputability from the
artifact, which holds. Write it as a provenance identity, never as a result-value seal,
tamper seal, or certification of the measured numbers. Verify values by recomputing them
from `samples.distances`.

## Stage-0 scientific meaning

Stage 0 measures:

```text
D = || concat_{g=0..3} (b_g(A) - b_g(B)) ||_2
```

for 100 pairs of four-gauge windows with zero mechanical strain, the same imposed thermal
profile, and different sensor identities.

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

The executed `0.400881` is 2.790% above Protocol P's approximate `roughly 0.39`, remains
inside the pre-registered range, exceeds three of the four cell values, and is 5.697% below
the range maximum. No Protocol-P version change is needed. The licensed statement is
conditional broad-range containment, not central agreement, population agreement, a test,
a threshold, mechanics evidence, or evidence for the project hypothesis. The operative
null remains Stage C's per-cell `Q95_c`.

## Missing first-run elapsed time

No trustworthy first-run timing was captured. An informal few-seconds note exists but has
unknown provenance and is not a measurement. Protocol P binds no runtime, so this does not
block the artifact. Do not execute Stage 0 again merely to manufacture a first-run number.
The packet README states `First-run elapsed time: not captured`; any future timing must be
labeled as a separate reproduction.

## Packet README Step 24 — reviewer approved, owner review open

```text
Reproducibility Packet/README.md
  Claude handoff blob       e525c7bea92eb259f62368b75c5ecb950e5fd370
  Codex reviewer blob       9363e144a0c0e957b5c0a201d3abbf47c68fe837
  review diff               +3 / -3
```

Codex's three corrections:

1. Step 24 needs no dataset and performs no MuJoCo simulation, but importing the Stage-0
   module loads the `mujoco` Python package transitively through shared input-binding code:
   `protocol_p_replay_gate -> assignment_generator -> cable_plant`. Step 1 installs it.
   Never write that Step 24 needs no physics engine/package; write zero simulation/rollout.
2. The first-run timing paragraph is outsider-clean and no longer references internal
   session records.
3. The no-authority string is named at its exact path, `corroboration.authority`.

The command, pins, output, values, identity, zero-rollout cost, and evidence boundary are
unchanged. Codex explicitly approves blob `9363e144...`. Claude must owner-review this exact
state before the runbook loop closes.

## Session-48 progress report — loop closed

```text
agents/Claude/Progress Reports/Progress Report Session 48.md
  approved blob  f01aa7d7b56b9b30e8279bc221a5f0e60613ab3f
```

Claude's returned edits propagate the prior corrections through the whole director-facing
file: Stage 0 sets no threshold; the mutation target is an input-binding integrity check,
not physical safety; and the reviewed line is not credited with a verification it does not
perform. Claude and Codex explicitly approve this same blob. The loop is closed.

## Public README state

Claude's 2026-07-31 entry announced joint result approval and the identity-scope finding.
It also said every summary figure reproduced exactly and that Step 24 needs no physics
engine. Codex preserved the entry and appended a dated correction:

```text
README.md
  reviewer-edited blob  f3f76f27f48e2ed228917328bbc0462d34addc23
  review diff           +2 / -0
```

The correction names the transitive MuJoCo package dependency and the one-ULP alternate-mean
difference. Codex explicitly approves this forward-corrected state. Claude owner re-review
remains required. Routine approval should not create another public milestone; approval in
the active thread is enough.

Do not rewrite or remove earlier dated entries. Any future public correction propagates
forward append-only.

## Jointly approved Stage-0 implementation

```text
Reproducibility Packet/scripts/analyze_synchronous_difference_null.py
  git blob    8435c764a76cb091278ffa47f14584dbf43b40ce
  raw sha256  4a9fc5955bb5d0f103d258525ee80f5766e0e9a46b01975c76ab895c53815b24

Reproducibility Packet/tests/test_synchronous_difference_null.py
  git blob    9591c91bd6412a9dd60860e05c40fcbcccc9ff74
  raw sha256  2fe39d831fa500d5183108ee4aed6590ac676af8beafec122b9af4919c9402ff
  tests       99
```

Both are UTF-8 without BOM and pure LF in the approved state. The three approved shared
helper/floor files remain:

```text
Reproducibility Packet/scripts/utils/gauge_windows.py
  git blob    7f7c09da3079ff2498a7240922a77b95ed116b7b

Reproducibility Packet/scripts/analyze_synchronous_detection_floor.py
  git blob    b99fe33357701c0a5285773146ec7986db6b7a82

Reproducibility Packet/tests/test_gauge_windows.py
  git blob    925b0bd842a8a2787516753217f28d06d3000c6c
  tests       18
```

The focused total is 117. Do not edit these approved states without a new review loop.

## Jointly approved Protocol P

```text
Reproducibility Packet/protocol/protocol-p-v2.3.3.md
canonical sha256  5689dad7ce4194b9a7dbe381006027df178997adf732f5734a77ef048bdf421f
raw sha256        5689dad7ce4194b9a7dbe381006027df178997adf732f5734a77ef048bdf421f
bytes             54,621
encoding/EOL      UTF-8, no BOM, pure LF
owner approval    Claude Session 43
reviewer approval Codex Session 43
```

The specification loop is closed. Do not edit this file in place. A source-checkable future
defect requires the next version, both exact-state approvals, and a new digest before any
affected stage runs.

## Jointly approved replay gate and result

```text
Reproducibility Packet/scripts/protocol_p_replay_gate.py
  git blob  7d3309b7a114a20a67f5e4adf7504dad0ca0897a

Reproducibility Packet/tests/test_protocol_p_replay_gate.py
  git blob  6a7e7774287d727b78ed3c9d323843c6dc1e37a3
  tests     36
```

The replay result remains one retained development row:

```text
run_id       scenario_dev_t01_f000_r00_S_dataset0
plant        20 / 20 fields equal
S record     38 / 38 entries equal; 531 NaNs matched
identity     20 / 20 fields equal
watched      0 changes
```

This is a construction positive control for one row only. It does not generalize to the
retained 472-reservation dataset.

## Stage-A/B/C driver gates

No Stage-A/B/C driver exists and none is authorized. Its implementation review must require:

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
Stage-0 implementation                                COMPLETE / JOINTLY APPROVED
Stage-0 execution                                     COMPLETE / RUN ONCE
Stage-0 result artifact                               COMPLETE / JOINTLY APPROVED
Stage-0 packet README step                            REVIEWER APPROVED / OWNER REVIEW NEXT
Stage A/B/C driver implementation and review          LATER
Stage A                                               AFTER DRIVER APPROVAL
Stage B                                               AFTER STAGE A
Stage C                                               AFTER STAGE B
result/terminal-branch review                         REQUIRED
written Amendment A2 + replacement assignment         LATER
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
- statistic: four-gauge matched 0.8-Hz cosine/sine coefficient difference, eight entries;
- operative null: per-cell 0.95 quantile with `method="higher"` over 28 healthy distances;
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
Gate 1                                      closed
Gate 2 generic path/current pre-A2 roles   closed
Gate 3 current pre-A2 assignment           closed
Protocol P specification                   jointly approved
Protocol-P seam                            jointly approved
one-row replay result/gate                  jointly approved
Stage-0 implementation                     jointly approved
Stage-0 execution                          run once
Stage-0 result                             jointly approved
Stage-0 packet README                      reviewer approved; owner review open
Stage A/B/C                                unauthorized and unimplemented
Amendment A2                               not written or approved
Gates 4-7                                  open
final config.json                          absent
```

The local ignored retained dataset contains 472 dev/pilot/validation reservations, 944 C1/S
manifest rows, and zero test rows. It was not regenerated. After an approved written
Amendment A2 and replacement assignment, use coherent from-zero regeneration, not an
in-place patch.

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

The replay is a one-row construction positive control. Stage 0 is a sensor-path diagnostic.
Neither establishes mechanics, detection, attribution, action authority, controller outcome,
or the project hypothesis.

## Verification baseline

Use only the repository venv:

```powershell
.\venv\Scripts\python.exe -m pytest -q "Reproducibility Packet\tests"
```

Codex Session 49:

```text
full packet suite            595 passed in 12.26 s
compileall                   clean
config.json                  absent
test-named .npz files        0
.npz under results           0
```

Do not run root-wide `pytest -q`; ignored duplicate trees under `tmp/` can pollute
collection. Before binary replay decisions, use raw hashes only. Before exact-state
approval, compute raw bytes, BOM/EOL state, raw SHA-256, Git blob, and Git attributes.

Before every commit:

```powershell
git diff --check
git diff --cached --check
```

CRLF warnings alone are not a reason to churn unrelated files.

## Transcript-order state

The active transcript is append-only. Session-49 append verification:

```text
pre-write lines       11,185
pre-write bytes       811,471
pre-write sha256      3a13cf6563ce62957a927e161d63ba49dac0aef301ea80f948daaac01f79c66f
Codex header line     11,189
Codex header count    1
old byte prefix       exact
technical diff        +150 / -0
post-write lines      11,335
post-write bytes      818,050
post-write sha256     c64ef573966464af8fb2c71c4fe48188e0943a81e955cd12db997b3ba0828f4b
physical last author  Codex
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

## Required next actions

1. Read controlling instructions, this continuity file, all Codex-relevant chat summaries,
   and the active transcript before replying.
2. Read Claude's newest report and physical-tail owner turn.
3. Verify Claude genuinely re-opened packet README blob `9363e144...` and public README
   blob `f3f76f27...`.
4. If Claude explicitly approves both exact states, record both loops closed.
5. Keep Stages A/B/C unauthorized until a separate driver implementation reaches explicit
   same-state approval.
6. Keep final `config.json` absent and the test split untouched.
7. Close out with HumanReport50, README heartbeat, Codex workspace README, complete
   continuity rewrite, hygiene checks, exact commit message, and push.

## Non-negotiable boundaries

- Approval is explicit and exact-state-specific.
- Preserve owner/reviewer lanes.
- Never treat development, screen, pilot, fixture, replay, or Stage-0 evidence as
  confirmatory.
- Never convert construction correctness or input binding into safety.
- Never convert safety into proof of correct construction.
- Never convert detection into attribution or action authority.
- Never treat the Stage-0 diagnostic as a detection threshold.
- Never describe `stage_0_identity` as sealing or certifying measured result values.
- Never claim Step 24 has no MuJoCo package dependency while the transitive import remains.
- Never silently rewrite a public or transcript-facing overclaim; append a correction.
- Never normalize binary artifacts before exact hashing.
- Never run a stage from unapproved implementation.
- Never run stages out of order.
- Never execute Stage 0 again without separate authorization.
- Never create final `config.json` before all gates close jointly.
- Never touch the test split before confirmatory authorization.
- Use append-only transcript hard gates and preserve exact requested commit messages.
