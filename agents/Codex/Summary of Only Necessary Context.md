# Summary of Only Necessary Context — Codex

**Rewritten:** 2026-07-31, Codex Session 50

**Phase:** Phase 2 — Integration and Reproducibility Build

**Config:** **UNFROZEN**; final `config.json` is absent

**Current decision:**

```text
STAGE_0_RESULT_REVIEW_LOOP_CLOSED
PACKET_README_STEP_24_REVIEW_LOOP_CLOSED_AT_9363E144
APPROVE_PUBLIC_README_AT_REVIEWER_APPROVED_73B124FD
REQUIRE_CLAUDE_OWNER_REREVIEW_OF_PUBLIC_README_AT_73B124FD
ACCEPT_STAGE_0_IDENTITY_BINDS_INPUTS_AND_SCHEMA_NOT_MEASURED_VALUES
ACCEPT_TRANSITIVE_MUJOCO_IMPORT_IS_INCIDENTAL_NOT_INTRINSIC
STAGE_A_B_C_DRIVER_IS_NEXT_IMPLEMENTATION_ARTIFACT
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

Its physical last turn is the **Codex Session 50 review-state correction**, beginning at
line 11,582. One artifact review loop is open. Claude Session 50 approved packet README
Step 24 at Codex's exact reviewer state and returned one scope edit to the public README.
Codex Session 50 independently reproduced that edit's claims and approved the exact
returned public state. Claude explicitly said she had **not** approved the returned state,
so her genuine owner re-review and explicit same-state approval or edit-and-return is next.

After the public README loop closes, the next technical artifact is the **Stage-A/B/C
driver implementation**. No Stage A, B, or C rollout is authorized until that driver has
completed its own explicit exact-state review loop. Do not recreate or rerun Stage 0 merely
to obtain elapsed time.

Codex's next session is Session 51. The next regular Codex progress report is Session 56
unless a phase transition or approved written Claim Sheet amendment triggers one first.

## Closed Stage-0 result

```text
Reproducibility Packet/results/protocol_p/sensor_only_difference_null.json
  git blob    31c1e6d1824c10bd5978d12c377f76cf556af03f
  git bytes   6,588
  checkout    6,765 bytes, UTF-8, no BOM, 177 CRLF line endings
  raw sha256  4101c0b8dcc1c3ee01b37433ccb3563d4c1e15e5e22cd8094979645d36a40cae
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

Codex Session 48 approved the unchanged artifact after independent duplicate-key,
identity, input-binding, digest, and distribution audits. Claude Session 49 genuinely
re-reviewed it with standard-library Python plus hand-indexed order statistics and
explicitly approved the same blob. The result loop is closed.

Claude's `statistics.fmean` value was `0.27873430387016523`, one ULP above the recorded
NumPy mean because of summation order. The quantile, population standard deviation,
minimum, median, and maximum matched exactly. Never say every summary figure reproduced
exactly under the alternate tool; state the one-ULP mean qualification.

## Stage-0 identity and scientific scope

```text
stage_0_identity
  dev-71b332893d007036625f666589f8c74b0ac3b946b47b5186ddf8de6a2d8ce31e

stage_0_canonical
  650 characters

identity rule
  dev- + sha256(stage_0_canonical UTF-8)
```

`stage_0_identity` binds the run's inputs and output shape, not its measured values. The
canonical payload contains the stage label, base-config hash, assignment canonical digest,
assignment document hash, protocol digest, seven pinned CLI values, and sorted top-level
output schema. It does **not** contain the 100 distances or summary statistics. This is a
provenance identity, not a result-value seal, tamper seal, or certification of the
measurements. Verify values from `samples.distances`.

Stage 0 measures:

```text
D = || concat_{g=0..3} (b_g(A) - b_g(B)) ||_2
```

for 100 pairs of four-gauge windows with zero mechanical strain, the same imposed thermal
profile, and different sensor identities. It has no plant, mechanics, fault, reservation,
rollout, threshold, or verdict authority. Its `dev-` identity is permanently ineligible
for confirmatory analysis. The operative null remains Stage C's per-cell `Q95_c`.

The four prior fixed-trace per-cell values are `0.3176`, `0.3555`, `0.3854`, and `0.4251`.
The executed `0.400881` is conditionally inside that pre-registered range, above three of
the four values, 2.790% above the earlier approximate `roughly 0.39`, and 5.697% below the
range maximum. Licensed claim: conditional broad-range containment under this bound setup.
Do not call it central agreement, population agreement, a detection threshold, mechanics
evidence, or evidence for the project hypothesis.

No trustworthy first-run elapsed time was captured. Protocol P binds no runtime. The
packet runbook says `First-run elapsed time: not captured`; any future timing is a
separate reproduction.

## Closed documentation states

### Packet README Step 24

```text
Reproducibility Packet/README.md
  approved blob  9363e144a0c0e957b5c0a201d3abbf47c68fe837
  reviewer       Codex Session 49
  owner          Claude Session 50
  state          REVIEW LOOP CLOSED
```

The approved step records the pinned Stage-0 command and boundary. It says Stage 0 needs
no dataset and performs no MuJoCo simulation, not that it has no MuJoCo package dependency.
Importing the Stage-0 module currently loads `mujoco` transitively through:

```text
protocol_p_replay_gate -> assignment_generator -> cable_plant -> import mujoco
```

The package is pinned in the packet requirements installed by Step 1. The transitive
dependency is incidental: exactly one of Stage 0's eight project imports loads MuJoCo,
and Stage 0 consumes only four fixed constants, `ProtocolPError`, and a pure-text hash
helper across that boundary. Session 46 planned extraction to `utils/protocol_p.py` when
the Stage-A/B/C driver becomes the third consumer. Describe current behavior until that
reviewed extraction actually lands.

The runbook also remains outsider-clean about missing elapsed time and names the exact
no-authority field path `corroboration.authority`.

### Public live-run README

```text
README.md
  reviewer-approved blob 73b124fd5e85c4cd0ebef8cce9a16c37c8e465e5
  owner                  Claude Session 50
  reviewer               Codex Session 50
  state                  OWNER RE-REVIEW REQUIRED; LOOP OPEN
```

The returned correction applies to both the 2026-07-30 and 2026-07-31 Stage-0 entries that
published “needs no physics engine,” explicitly withdraws the phrase from both, and
preserves both dated entries unchanged. It also retains the one-ULP alternate mean
qualification. Codex approves this exact state. Claude's handoff expressly withheld owner
approval, so do not infer loop closure from her edit or return.

Do not silently rewrite or remove an earlier dated entry. Any future public correction
propagates forward under a new active review state.

## Jointly approved implementation/specification states

```text
Reproducibility Packet/protocol/protocol-p-v2.3.3.md
  canonical/raw sha256  5689dad7ce4194b9a7dbe381006027df178997adf732f5734a77ef048bdf421f
  git blob              a622709ad802c88a71ca87d0257238a50083b66d
  bytes                 54,621
  encoding/EOL          UTF-8, no BOM, pure LF
  state                 jointly approved; edit only as a new reviewed version
```

```text
Reproducibility Packet/scripts/analyze_synchronous_difference_null.py
  git blob    8435c764a76cb091278ffa47f14584dbf43b40ce
  raw sha256  4a9fc5955bb5d0f103d258525ee80f5766e0e9a46b01975c76ab895c53815b24

Reproducibility Packet/tests/test_synchronous_difference_null.py
  git blob    9591c91bd6412a9dd60860e05c40fcbcccc9ff74
  raw sha256  2fe39d831fa500d5183108ee4aed6590ac676af8beafec122b9af4919c9402ff
  tests       99

Reproducibility Packet/scripts/utils/gauge_windows.py
  git blob    7f7c09da3079ff2498a7240922a77b95ed116b7b

Reproducibility Packet/scripts/analyze_synchronous_detection_floor.py
  git blob    b99fe33357701c0a5285773146ec7986db6b7a82

Reproducibility Packet/tests/test_gauge_windows.py
  git blob    925b0bd842a8a2787516753217f28d06d3000c6c
  tests       18
```

These five implementation/helper states are jointly approved. Do not edit them without a
new review loop. The focused total is 117.

The replay gate/result are also jointly approved:

```text
Reproducibility Packet/scripts/protocol_p_replay_gate.py
  git blob  7d3309b7a114a20a67f5e4adf7504dad0ca0897a

Reproducibility Packet/tests/test_protocol_p_replay_gate.py
  git blob  6a7e7774287d727b78ed3c9d323843c6dc1e37a3
  tests     36

retained replay row
  run_id       scenario_dev_t01_f000_r00_S_dataset0
  plant        20 / 20 fields equal
  S record     38 / 38 entries equal; 531 NaNs matched
  identity     20 / 20 fields equal
  watched      0 changes
```

The replay is one-row construction evidence only, not dataset-wide reproduction or a
research result.

## Stage-A/B/C driver gate

No Stage-A/B/C driver exists and none is authorized. The implementation/review must require:

1. a closed-vocabulary `screen_physical_faults` helper;
2. healthy requires severity absent and returns `()`;
3. structural requires finite severity in `(0, 1]` and returns one complete `FaultSpec`
   with onset derived from trajectory time and control timestep;
4. field-by-field I13a equality before every rollout;
5. a complete `ScreenOverrides` bundle, never a partial bundle;
6. I3 reservation-difference equality and suffix-free I4;
7. I5–I8 identity, CRN, and provenance checks;
8. explicit Protocol-P condition keys, never a stale returned-assignment label;
9. no persisted `ObservedRecord`, label, manifest, role index, or dataset payload; and
10. a test around the real results-only output root that fails on a wrong dataset write.

The low-level generator seam can represent a partial override bundle. That does not
authorize the driver to construct or accept one.

Likely implementation opportunity: extracting the shared Protocol-P constants/hash/error
surface to `utils/protocol_p.py` when the driver becomes the third consumer. Because that
edits the closed replay gate and Stage-0 import path, treat the extraction as part of the
driver's exact-state review, update the runbook dependency sentence when current behavior
actually changes, and re-run all affected closed tests.

## Required execution order

```text
Protocol P v2.3.3 exact-state approval                COMPLETE
permanent I13b exact-state approval                   COMPLETE
generator seam exact-state approval                   COMPLETE
one-row replay result/gate                            COMPLETE / JOINTLY APPROVED
Stage-0 implementation                               COMPLETE / JOINTLY APPROVED
Stage-0 execution                                    COMPLETE / RUN ONCE
Stage-0 result artifact                              COMPLETE / JOINTLY APPROVED
Stage-0 packet README step                           COMPLETE / JOINTLY APPROVED
public Stage-0 corrections                           REVIEWER APPROVED / OWNER REVIEW NEXT
Stage-A/B/C driver implementation and review         AFTER PUBLIC README LOOP CLOSE
Stage A                                               AFTER DRIVER APPROVAL
Stage B                                               AFTER STAGE A
Stage C                                               AFTER STAGE B
result/terminal-branch review                         REQUIRED
written Amendment A2 + replacement assignment         LATER
from-zero non-test regeneration and re-audit           LATER
Gates 4–7 -> joint final freeze -> confirmatory run   LATER
```

## Protocol-P retained design

Do not reopen without new evidence:

- universe: development diagnostic trajectory `t01`, cells 4/5/6/7;
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
- gauge-only and unmatched secondaries are descriptive only;
- OOD 0.45/0.55 excluded from known-class macro-F1; and
- all outputs are development-only and confirmatory-ineligible.

The honest prior remains that remEI 0.75 likely fails widely and remEI 0.50 is near the
boundary under earlier optimistic projections. That is a prior, not a result.

## Role, config, and data state

```text
Gate 1                                      closed
Gate 2 generic path/current pre-A2 roles   closed
Gate 3 current pre-A2 assignment           closed
Protocol P specification                   jointly approved
Protocol-P generator seam                  jointly approved
one-row replay result/gate                  jointly approved
Stage-0 implementation/result/docs         jointly approved
Stage A/B/C driver                          unauthorized and unimplemented
Stage A/B/C                                 unauthorized and unexecuted
Amendment A2                                not written or approved
Gates 4–7                                  open
final config.json                          absent
```

The local ignored retained dataset contains 472 dev/pilot/validation reservations, 944 C1/S
manifest rows, and zero test rows. It was not regenerated. After an approved written
Amendment A2 and replacement assignment, use coherent from-zero regeneration rather than
an in-place patch.

## Evidence boundaries

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

Codex Session 50:

```text
full packet suite            595 passed in 12.61 s
config.json                  absent
test-named .npz in packet    0
.npz under packet results    0
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

The active transcript is append-only. Session-50 review and correction verification:

```text
initial pre-write lines        11,484
initial pre-write bytes        825,459
initial pre-write sha256       cdb31666bb5bb83540768a822dc7e56e4c0f2a65bd0f782f30ccd1cafc887cfe
review header line             11,488
review-state correction line   11,582
each new header count          1
original prefix                exact
first-append prefix            exact
final technical diff           +131 / -0
final lines                    11,615
final bytes                    831,253
final sha256                   7d512e299f770e7ee0b8b34380ead3f9f4241dc76dc4904fc2d4184e132a1f96
physical last author           Codex
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
8. require an additions-only transcript diff.

If any assertion fails, stop and repair with a dated append-only correction.

## Required next actions

1. Read controlling instructions, this continuity file, every Codex-relevant chat summary,
   and the active transcripts before replying.
2. Read Claude's newest human report and the physical-tail owner/reviewer turn.
3. Treat the Stage-0 result and packet Step-24 loops as closed; do not reopen them without
   new source-checkable evidence.
4. Verify Claude genuinely owner-re-reviewed and explicitly approved public README blob
   `73b124fd...` or inspect any edit-and-return she makes; do not infer approval.
5. After that loop closes, design/implement the Stage-A/B/C driver against the ten
   fail-loud requirements above and open its explicit exact-state review loop before any
   Stage A execution.
6. Keep final `config.json` absent and the confirmatory test split untouched.
7. Close out with HumanReport51, public README heartbeat, Codex workspace README, complete
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
- Never silently rewrite a public or transcript-facing overclaim; correct it forward.
- Never normalize binary artifacts before exact hashing.
- Never run a stage from unapproved implementation or out of order.
- Never execute Stage 0 again without separate authorization.
- Never create final `config.json` before all gates close jointly.
- Never touch the confirmatory test split before authorization.
- Use append-only transcript hard gates and preserve exact requested commit messages.
