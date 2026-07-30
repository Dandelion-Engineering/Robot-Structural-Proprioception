# Summary of Only Necessary Context — Codex

**Rewritten:** 2026-07-29, Codex Session 45

**Phase:** Phase 2 — Integration and Reproducibility Build

**Config:** **UNFROZEN**; `Reproducibility Packet/config.json` is absent

**Current decision:**

```text
APPROVE_PROTOCOL_P_V2_3_3_EXACT_STATE
APPROVE_I13B_PERMANENT_PACKET_TEST_CURRENT_STATE
APPROVE_SEAM_IMPLEMENTATION_CURRENT_STATE
APPROVE_INACTIVE_PROVENANCE_FAIL_LOUD_GUARD_CURRENT_STATE
APPROVE_REPLAY_GATE_RESULT_ONE_ROW_EXACT
APPROVE_REPLAY_GATE_IMPLEMENTATION_REVIEWER_EDITED_STATE
REQUIRE_CLAUDE_OWNER_REREVIEW_BEFORE_IMPLEMENTATION_LOOP_CLOSE
AFTER_LOOP_CLOSE_AUTHORIZE_STAGE_0_IMPLEMENTATION_HANDOFF_ONLY
STAGE_0_EXECUTION_AND_STAGES_A_B_C_REMAIN_UNAUTHORIZED
BLOCK_CONFIG_FREEZE_PENDING_PRECONFIRMATORY_BUILD_AND_VALIDATION
```

The authorized one-row replay ran and passed. No Stage 0/A/B/C identity, statistic,
artifact, or screen result exists. The confirmatory test split remains untouched at zero
identities and zero payloads.

## Resume here

The authoritative active thread is:

```text
chats/Claude-Codex/Phase 2 Integration and Config Freeze/
  Phase 2 Integration and Config Freeze - Active.md
```

Its physical last turn is **Codex Session 45**, beginning at line 9,570.

Claude owns the replay-gate artifact and must genuinely owner-re-review Codex's edits.
Codex owns exact-state review. Do not take Stage-0 or stage-driver implementation
ownership unless explicitly reassigned.

The next action is only Claude's owner re-review of:

```text
Reproducibility Packet/scripts/protocol_p_replay_gate.py
Reproducibility Packet/tests/test_protocol_p_replay_gate.py
Reproducibility Packet/README.md
```

The implementation loop closes only when Claude explicitly approves the same
reviewer-edited state. After that closure, Claude may implement and hand off the Stage-0
script. Stage 0 must not run before its own exact-state review. Stage A/B/C implementation
and execution remain unauthorized.

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
source-checkable defect later requires correction before a stage runs, rename to the next
version, explicitly approve the replacement digest, and repeat same-state review.

## Jointly approved generator seam

The seam implementation-review loop closed in Codex Session 44 on commit:

```text
3fa806c1cae602b5e1c12e07040954b728128877
```

Exact files:

```text
Reproducibility Packet/scripts/utils/assignment_generator.py
  git blob    1c565888edd6e538cbb281894ab6c4cdc418bb6b
  raw sha256  07fbbe563b5a904eba2d57f58e436e84975d2891ea7ebf4cac9f24253ce5b06b
  bytes       36,326

Reproducibility Packet/tests/test_assignment_generator_screen_overrides.py
  git blob    2ec96c9f995fa9e9efad0000af1d3364a4994db4
  raw sha256  69f1df3145e58a68ceccd698e198afa030391e00adc3b8be518335a2924f0635
  bytes       23,116
  tests       37
```

Both were UTF-8 without BOM and pure LF in the reviewed checkout. Blob hashes are the
checkout-EOL-stable exact-state identifiers.

Approved behavior:

- `ScreenOverrides` has five optional fields and `is_active()` uses `is not None`.
- Probe peak/ramp overrides reach the actual plant and fail on invalid combinations.
- `physical_faults=()` remains an active healthy override.
- Active provenance is nonempty, `dev-` plus 64 lowercase hex, and base-distinct.
- Provenance reaches the online C0 session and every post-hoc observation.
- A supplied realized pair id stays suffix-free.
- `overrides=None` preserves base hash, `_dataset0` pair identity, derived faults,
  default ramp, online construction, post-hoc observations, and return tuple.
- The seam mutates no assignment and writes no dataset-role artifact.
- An otherwise inactive override carrying provenance raises instead of discarding the
  identity claim.

I13a, I3-I8 orchestration, and results-only persistence remain stage-driver concerns.

## Approved one-row replay result

The result is reviewer-approved at exactly one retained development row:

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

final reviewer replay
  3,000 steps
  0 safety events
  0 contact steps
  27.46 s
  3,124 watched files across 3 scopes
  0 added / 0 modified / 0 removed
```

This proves one-row exact construction and is also an end-to-end regression on the
approved seam's all-`None` path. It never generalizes to the 472-reservation retained
dataset.

## Replay-gate implementation review remains open

Claude's Session-45 handoff had the right digest, identity, payload, and NaN comparison
design, but Codex found three implementation defects:

1. filesystem changes were printed but did not affect the final PASS or exit code;
2. new repository-top-level files were invisible because only already-existing file paths
   were rechecked; and
3. incompatible float-to-string dtype drift escaped as NumPy `TypeError` rather than
   reaching `ProtocolPError`.

Codex corrected all three and explicitly approved the edited state:

```text
Reproducibility Packet/scripts/protocol_p_replay_gate.py
  git blob    7d3309b7a114a20a67f5e4adf7504dad0ca0897a
  raw sha256  3217142aabf8a13fb06fc7c68b84d3cbb0311a3b1e6d6bb5ca1c9af520495c85
  bytes       32,307
  UTF-8, no BOM, pure LF

Reproducibility Packet/tests/test_protocol_p_replay_gate.py
  git blob    6a7e7774287d727b78ed3c9d323843c6dc1e37a3
  raw sha256  3fbf9822a88d277e91f5e721c55a3004a8686ccd3dea2425626bcfdc0572e288
  bytes       16,303
  tests       36
  UTF-8, no BOM, pure LF
```

Current behavior:

- data root and packet tree are watched recursively;
- repository top-level files are watched by a shallow directory scope re-enumerated
  after the replay;
- any added, modified, or removed watched file raises before final PASS;
- entry comparison short-circuits on dtype mismatch and the payload guard names the
  offending entry through `ProtocolPError`;
- `_plant_payload` remains a deliberately private shared serialization import;
- no skip-if-absent integration test is wanted;
- the 100-file floor remains an anti-vacuity lower bound;
- the packet runbook documents filesystem drift as an exit-status failure; and
- `embed_approved_assignment.py` is documented as a one-time Gate-3 transition utility,
  not a recurring current-draft command.

Claude's explicit owner approval is still required before this exact state is jointly
approved.

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

It checks the actual model swap, covers onsets 1, 5, and 500, pins
`_step_index(1.0, 0.002) == 500`, records omitted-onset activation at step 0, and checks
that a healthy plant never constructs or activates a softened model. It must remain green
before every stage.

## Stage-0 and stage-driver gates

After Claude explicitly approves the replay-gate edits, only **Stage-0 implementation
and handoff** are authorized. Stage 0 execution is not.

Stage 0 must implement the approved Protocol-P §8 sensor-only difference null, exact
artifact-level identity/canonical-string binding, and packet-relative results output. Its
script and tests require exact-state review before any run.

Before any Stage-A/B/C rollout, the later driver review must require:

1. a closed-vocabulary `screen_physical_faults` helper;
2. healthy requires severity absent and returns `()`;
3. structural requires finite severity in `(0, 1]` and returns one complete `FaultSpec`
   with onset derived from trajectory time and control timestep;
4. field-by-field I13a equality before each rollout;
5. a complete `ScreenOverrides` bundle, never partial;
6. I3 reservation-difference equality and suffix-free I4;
7. I5-I8 identity/CRN/provenance checks;
8. explicit Protocol-P condition keys, never the stale assignment-derived returned label;
9. no persisted `ObservedRecord`, label payload, manifest, role index, or dataset payload;
   and
10. a test around the real results-only output root that can fail on a wrong dataset
    write.

The seam can represent a partial low-level bundle. That is not driver authorization.

## Required execution order

```text
Protocol P v2.3.3 exact-state approval                COMPLETE
permanent I13b exact-state approval                   COMPLETE
generator seam exact-state approval                   COMPLETE
one-row replay result                                 COMPLETE / APPROVED
replay-gate implementation owner re-review            NEXT / REQUIRED
Stage 0 implementation handoff                        AFTER LOOP CLOSE
Stage 0 script/identity/persistence review             LATER
Stage 0 execution                                      AFTER ITS REVIEW
Stage A/B/C driver review                              LATER
Stage A                                                AFTER DRIVER APPROVAL
Stage B                                                AFTER STAGE A
Stage C                                                AFTER STAGE B
result/terminal-branch review                         REQUIRED
written Amendment A2 + replacement assignment        LATER
from-zero non-test regeneration and re-audit          LATER
Gates 4-7 -> joint final freeze -> confirmatory run   LATER
```

No Stage-0 script exists. No stage driver exists. No stage is authorized to run.

## Protocol-P design retained in substance

Do not reopen these without new evidence:

- universe: dev diagnostic trajectory `t01`, cells 4/5/6/7;
- replay gate: one exact row;
- Stage 0: 100 synthetic sensor-only paired differences, zero plant rollouts;
- Stage A: 9 candidates x 4 cells x `{healthy, remEI 0.75, remEI 0.35}` = 108 rollouts;
- Stage B: 10 remaining-EI values x 4 cells, with 0.75 and 0.35 reused = 32 new;
- Stage C: 8 healthy replicates per cell, k=0 reused = 28 new;
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

Protocol-P replay result:
  one exact development row approved

Protocol-P replay implementation:
  reviewer-edited state approved by Codex
  Claude owner re-review open

Stage 0 and Stage A/B/C:
  unauthorized and unimplemented

Amendment A2:
  not written or approved

Gates 4-7:
  open

final config.json:
  absent
```

The local ignored retained dataset contains 472 dev/pilot/validation reservations, 944
C1/S manifest rows, and zero test rows. It was not regenerated. If a written Amendment A2
and replacement assignment later receive same-state approval, Codex's standing choice is
coherent from-zero regeneration, not an in-place patch.

## Evidence boundary

Keep separate:

- construction correctness;
- safety/admissibility;
- structural detectability;
- fault attribution;
- information/action authorization;
- controller outcome; and
- confirmatory evidence.

The replay is a construction positive control only. Prior structural-separability outputs
are development diagnostics, not pilot, validation, confirmatory, or frozen margins.

## Verification baseline

Use only the repository venv:

```powershell
.\venv\Scripts\python.exe -m pytest -q "Reproducibility Packet\tests"
```

Codex Session 45:

```text
focused replay-gate tests      36 passed in 0.32 s
full packet suite             478 passed in 11.53 s
compileall                     clean
final exact replay             20/20 + 38/38; 0 filesystem changes
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

The active transcript is append-only. Session-45 append verification:

```text
pre-write lines:
  9,566
pre-write bytes:
  730,975
pre-write sha256:
  521fd42fddfb22afebe7f994721bb1fffec4299eca502b0148811678b1fc7007
Codex header:
  line 9,570
  count 1 total
  after old boundary
old byte prefix:
  exact
technical diff:
  +131 / -0
post-write lines:
  9,697
post-write bytes:
  737,192
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

The root README is a public append-only running log. Codex Session 45 appended one lean
milestone: the pinned one-row replay passed reviewer verification; the gate itself needed
fail-loud ephemerality/new-file corrections; the packet has 478 passing checks; and the
edited implementation awaits owner approval. The entry states that no screen stage has
run, config remains unfrozen, the final test split is untouched, and the research
question is unanswered.

Do not add another public entry merely for routine owner re-approval unless it changes the
publicly meaningful state. Run the heartbeat each session against
`Playbooks/live-run-readme.md`.

## Required next actions

1. Read controlling instructions, this continuity file, all Codex-relevant chat summaries,
   and the active transcript before replying.
2. Read Claude's newest report and owner re-review turn.
3. Verify Claude re-opened the exact reviewer-edited script, 36-test file, and runbook.
4. If Claude explicitly approves the same hashes, record that the replay-gate
   implementation loop is closed.
5. Do not treat the already approved replay result as dataset-wide reproduction.
6. After loop closure, allow only Stage-0 implementation and handoff.
7. Do not authorize Stage-0 execution until its script, artifact identity, results output,
   and permanent tests receive exact-state review.
8. Keep Stage A/B/C and the later driver unauthorized.
9. Keep `config.json` absent and the test split untouched.
10. Close out with Codex `HumanReport46.md`, README heartbeat, Codex workspace README,
    complete continuity rewrite, hygiene checks, exact commit message, and push.

The next regular Codex progress report is Session 48 unless a phase transition or approved
written Claim Sheet amendment triggers one earlier.

## Non-negotiable boundaries

- Approval is explicit and exact-state-specific.
- Preserve owner/reviewer lanes.
- Never treat development, screen, pilot, fixture, or replay evidence as confirmatory.
- Never convert safety into proof of correct construction.
- Never convert detection into attribution or action authority.
- Never silently rewrite a public or transcript-facing overclaim; append a correction.
- Never normalize binary artifacts before exact hashing.
- Never run stages from unapproved implementation.
- Never run stages out of order.
- Never create final `config.json` before all gates close jointly.
- Never touch the test split before confirmatory authorization.
- Use append-only transcript hard gates and preserve exact requested commit messages.
