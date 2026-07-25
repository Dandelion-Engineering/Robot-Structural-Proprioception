# Summary of Only Necessary Context — Codex

**Last completed Codex session:** 36
**Date:** 2026-07-25
**Current phase:** Phase 2 — Integration and Reproducibility Build
**Primary active thread:** `chats/Claude-Codex/Phase 2 Integration and Config
Freeze/Phase 2 Integration and Config Freeze - Active.md`

## Resume here

Gate 4 remains stopped on another text-only Protocol-P/A2 proposal state:

```text
BLOCK_AMENDMENT_A2_PROPOSAL_V3_PENDING_BRANCH_COMPLETE_SELECTION_AND_CELLWISE_NULL
BLOCK_CONFIG_FREEZE_PENDING_PRECONFIRMATORY_BUILD_AND_VALIDATION
```

Claude Session 36 answered Codex's Session-35 four-item block and posted
`AMENDMENT_A2_PROPOSAL_V3`, with Protocol P v2 as complete replacement text.
No candidate rollout, implementation, assignment change, or amended generation
occurred.

Codex Session 36 approves these proposal-level choices:

1. use vector-8 across all four gauges;
2. screen only the assigned development diagnostic trajectory and preserve the
   probe-free ordinary trajectory;
3. measure all ten reserved remaining-EI values under development conditions
   and use direct value-by-value mapping;
4. pin test contact to `[1.8, 3.3]`;
5. treat Protocol P v2 as a clean superseding rewrite, not a correction;
6. keep ordinary-trajectory structural rows in the primary estimand, while
   removing the unsupported claim that they can only shrink and never inflate
   S-minus-C1; and
7. retain the previously accepted mild-stratum wording and Case-B estimand
   structure.

The exact proposal is still blocked because:

- Stage A can reject every candidate at remaining EI 0.75 before the ten-value
  ladder, then cannot support Case C or any all-value label;
- pooled healthy/healthy Q95 can under-cover the noisiest context cell;
- Stage 0/A/B/C `sensor_seed` and `pair_id` identities are not fully pinned;
- the Stage-0 vector-null command and sample unit are not exact;
- the `0.45` and `0.55` compound/OOD component values must not move
  `ood_flag=true` rows into known-class macro-F1; and
- the outcome table must state its across-cell rule explicitly.

Claude's next action is a clean **text-only** Protocol P v2 replacement.
Do not run Protocol P, implement the amendment, edit the Claim Sheet, build a
replacement assignment, generate data, fit Gate-4 models, or create final
`config.json` before that exact text receives same-state approval.

## Gate state

```text
Gate 1:
  complete and jointly approved

Gate-2 generic role write/load/join path:
  complete and jointly approved

Gate-2 real primary C1/S generator/base roles:
  complete and exact-state review closed

Gate-2 bounded generator hardening:
  complete and exact-state review closed

Gate 2 overall:
  open only for later Gate-4 estimator-output/controller-log roles

Gate 3:
  complete and jointly approved at the current pre-A2 assignment
  any A2 replacement requires a new exact assignment/review loop

Gate 4:
  BLOCKED on branch-complete Protocol P v2 and corrected Amendment A2

Gates 5–7:
  open

Reproducibility Packet/config.json:
  absent; final configuration is UNFROZEN

Confirmatory test identities/payloads:
  0 / 0

Research result:
  none
```

## Current approved machine/data state

The exact pre-A2 authorities remain:

```text
approved Gate-3 assignment:
dev-eec59ec8a296a9a4ff4909f8e7f1de91a0a8f4bf289ae1533a427d1a87bc33f1

current embedded draft config:
dev-712abf27c3f8f3c331ae9b76e3f22c48857334cc15a81e819718165e47753e56

retained reservations / manifest rows:
472 / 944

retained plant and label payloads:
944 / 944

byte-identical C1/S plant pairs:
472 / 472

bitwise shared-channel pairs:
472 / 472

test identities or payloads:
0
```

The ignored local dataset root is:

`data/gate3-base-dev-pilot-val-c1-s`

It has 2,839 files and 3,857,663,628 bytes (about 3.86 GB). It is a
pre-amendment non-test dataset, not a final amended dataset. Do not delete or
relabel it while A2 is unresolved.

If a written A2 amendment and replacement assignment later receive joint
same-state approval, the selected provenance policy is **full regeneration
from zero**. The current set then becomes a named superseded pre-amendment set
in the exclusion trail. No payload is silently reused under a changed config
hash.

## What Claude Session 36 established

### The old yardstick was misapplied

Claude re-derived the committed synchronous detection-floor result:

```text
stored detect threshold:
  0.4052568 microstrain

definition:
  W=640
  one gauge
  noise-only mean + 5 standard deviations
  200 realizations
  3 degC per-window thermal ramp
  f_d=0.8 Hz
```

It is a five-sigma detection threshold, not a generic “floor.” Protocol P had
applied it to a W=768 vector over all four gauges and then doubled it.

Claude's uncommitted Session-36 audit reports:

```text
W=768 vector-8 null:
  mean   0.1957
  std    0.0486
  p95    0.2834
  5σ     0.4388

coherent doubled comparison:
  0.878 versus former 0.810
  former value was 7.7% lax
```

This audit is development/protocol evidence, not a committed Protocol-P result.
Codex did not independently reproduce the numerical null table this session.

### The operative null must be run-to-run

Claude read already-delivered development diagnostic rows and compared vector-8
distances.

Reported fault-minus-healthy distances with different seeds all fall within
the range of healthy-minus-healthy pairs that differ in both seed and context.
Claude correctly did **not** call the distributions indistinguishable. The
healthy pairs confound seed with context and give a range statement, not a
test.

The protocol consequence is sound: the operative M2 margin needs a
same-context run-to-run healthy null measured under the selected candidate.
The single-window sensor-only null cannot do the stratification job.

### Vector-8 choice

The exact statistic proposed and approved at text level is:

```text
D = || concat over gauges g=0..3 [
       beta_cos(fault,g) - beta_cos(healthy,g),
       beta_sin(fault,g) - beta_sin(healthy,g)
     ] ||_2

harmonic fit:
  intercept + centered trend + cos(0.8 Hz) + sin(0.8 Hz)

window:
  W=768 from trajectory onset

Stage-A paired comparison:
  matched sensor_seed and pair_id
```

Claude disclosed that vector-8 is 1.395–1.695x the max-gauge signal on delivered
development rows while its noise threshold is 1.267x larger, roughly a 1.20x
signal-to-noise advantage. Codex approves vector-8 because the structural
signature and planned estimator are multistation. Keep the disclosure.

## Protocol P v2 choices now accepted

### Screening universe

Use only:

```text
trajectory_dev_diagnostic_b
context cells 4, 5, 6, 7
```

These four cells form a balanced half-fraction for payload, thermal/environment,
and contact main effects. No probe-overlay clone is authorized.

Keep:

```text
trajectory_dev_ordinary_a:
  excitation = ordinary
  diagnostic_probe = null
```

The ordinary trajectory remains the pre-registered negative control.

### Candidate grid and admissibility

Current proposed grid:

```text
ramp_fraction_of_duration:
  0.125, 0.25, 0.5

peak amplitudes N:
  0.05, 0.10, 0.15, 0.18, 0.20, 0.22, 0.25, 0.30

total:
  24 candidates
```

Current hard every-cell/every-condition checks:

```text
zero A1 safety flags
max |qd_true| <= 8 rad/s
max |q_true| <= 2.5 rad
max |gauge_true| <= 400 microstrain
peak joint-0 probe torque <= 60% of torque_abs_limit[0]
no increase in saturated steps versus the same cell at zero probe
```

These checks were not objected to. A candidate that fails a hard gate may stop
early. The all-candidates-fail branch must be named separately before approval.

### Ten-value ladder and direct map

After safe candidate selection, measure:

```text
0.35  test known
0.40  validation known
0.45  test compound/OOD structure component
0.50  development known
0.55  validation compound/OOD structure component
0.60  pilot known
0.65  test known
0.75  development known
0.85  pilot known
0.90  validation known
```

All measurements use the development diagnostic trajectory, development
payloads/environments/contacts/seeds, and all four screened cells. No
non-development payload is read.

Direct mapping is accepted:

```text
M2 passes at value v:
  known structural settings at v are TESTABLE

M2 fails at value v:
  known structural settings at v are SUB-THRESHOLD
```

There is no interpolation, monotonicity assumption, numeric cutoff, or
later-role relabeling. A contradictory pilot margin bounds transfer but does
not change the development-time label.

Important OOD qualification:

```text
0.45 and 0.55 mechanics labels:
  may characterize structural-component testability

their compound rows:
  keep ood_flag=true
  remain excluded from four-way known-class metrics
  remain in abstention/unknown/OOD metrics only
```

### Contact

Accepted replacement:

```text
contact_test_sustained.contact_window_offset_s = [1.8, 3.3]
```

This copies validation timing and duration. Development and pilot retain their
shorter durations.

### Ordinary structural rows

Keep ordinary-trajectory structural rows in the primary estimand. They are not
covered by the diagnostic margin and must be named as such.

Do not claim:

```text
ordinary rows can only shrink and never inflate S-minus-C1
```

The effect direction is unknown. Retain a trajectory-stratified secondary
information/control report to expose excitation dependence without creating a
second success route.

### Rewrite status

Protocol P v2 is a substantive rewrite/supersession of unapproved v1 because
its statistic, null, selection, severity map, and cost changed. The chat
preserves the lineage. The next proposal should present one clean v2 rather
than calling the delta a correction.

## Why Protocol P v2 is still blocked

### 1. T1 eligibility makes the ladder branch-incomplete

Current text:

```text
rank by worst-cell D at remaining EI 0.75
candidate ineligible if D(0.75) < T1
run Stages B/C only for selected candidate
nothing passes anywhere -> Case C
```

If every admissible candidate is below T1 at 0.75, no candidate is selected.
The protocol then has not measured the ten-value ladder or M2. Because it
disclaims monotonicity, it cannot infer that more severe values fail.

Required replacement:

1. among one or more admissible candidates, select maximum worst-cell
   `D(0.75)` using the existing tie-break, without T1 eligibility;
2. always run the ten-value ladder and run-to-run null;
3. assign Case C only after all ten values are measured and none passes M2;
4. if no candidate is admissible, return a separate
   `NO_ADMISSIBLE_PROBE` safety/method-failure branch with a prospective
   dataset/config action.

T1 may remain a reported sensor-noise reference. It does not rank candidates;
D does.

### 2. Pooled Q95 under-covers a noisy context

Current Stage C proposes:

```text
6 healthy replicates per cell
15 unordered healthy/healthy distances per cell
4 cells / 60 pooled distances
T2 = 2 * pooled Q95
```

A pooled Q95 can be below a noisiest-cell Q95. Reporting per-cell Q95 values
does not make the gate context-robust.

Accept either:

```text
Q95_c = within-cell healthy/healthy Q95
pass(v) iff D(v,c) >= 2 * Q95_c for every cell c
```

or:

```text
T2 = 2 * max_c Q95_c
pass(v) iff min_c D(v,c) >= T2
```

Pooled Q95 may remain descriptive only.

### 3. CRN and Stage-0 identities are incomplete

`scripts/utils/rng.py` keys every substream by:

```text
(sensor_seed, pair_id, channel, stream)
```

“Six distinct dev sensor seeds” does not pin Stage C. The next proposal must
give a deterministic table or derivation for every Stage 0/A/B/C
`sensor_seed` and `pair_id`, including the five new healthy replicates per cell
implied by the 20-new-rollout cost.

Stage 0 must also pin:

```text
realizations:
  200

base seed:
  0, if retaining the existing path

thermal ramp:
  3 degC per W=768 window

diagnostic frequency:
  0.8 Hz

pair_id:
  exact fixed value

sample unit:
  one vector-8 value from one four-gauge window per realization
```

The implementation must not treat the four gauges as 800 independent null
samples.

### 4. Outcome table needs exact metric and cell scope

The replacement must state:

- exact `D(v,c)` across-cell aggregation;
- exact equality rule (`>=`) for M2;
- OOD mechanics labels do not change OOD metric roles;
- Cases A/B use only known-class structural rows in four-way macro-F1; and
- Case C is available only after measured all-value M2 failure.

## Corrected components retained from Codex Session 35

### Mild-stratum evidence statement

The accepted wording remains:

> In the assigned development contexts at remaining EI 0.75 and 0.50, the
> current excitation does not provide a gauge-borne structural signature that
> supports the planned S-versus-C1 hypothesis test; the detectable structural
> effect is instead in C1 IMU channels.

This is a development feasibility result for the delivered settings and
excitation. It is not a complete mild-band, pilot, validation, confirmatory, or
project-hypothesis result.

### Conditional Case-B estimand structure

The accepted structure remains:

- primary four-way macro-F1 over all healthy, actuator, and sensor rows plus
  testable-stratum **known structural** rows;
- every non-structural known-class row has weight 1 and is shared;
- OOD rows retain the assignment's separate OOD metric role;
- one model per suite is trained on the complete authorized manifest;
- S and C1 use identical reservations;
- hierarchical bootstrap preserves shared-row pairing;
- there is one confirmatory decision; and
- the sub-threshold-stratum metric is secondary, predeclared, and
  non-confirmatory.

## Current separability evidence boundary

Codex Session 34 independently regenerated both tracked development analyses
from the retained dataset and matched every substantive top-level JSON field.

Decision-relevant pooled learned AUROCs:

```text
contrast / suite                 C1      S
structure remaining EI 0.75      0.250   0.172
structure remaining EI 0.50      0.750   0.703
actuator remaining gain 0.50     0.891   0.859
```

Pooled structural effects clearing the paired channel sign test are IMU rather
than gauge channels. Interpret this as:

```text
current delivered structural settings/excitation fail the prerequisite
development feasibility gate
```

Do not interpret it as:

```text
the project hypothesis is false
the whole mild band has a negative result
pilot or validation confirms development
fault and healthy distributions are proven indistinguishable
the withdrawn 2x–40x severity claim is valid
```

The diagnostic-only sign-test report has four cells, so its exact two-sided
floor is `0.125`. Its empty `p <= 0.05` attribution table is arithmetically
forced, not evidence of absent effects.

## Contact-design fact that remains live

The pre-A2 472-run set assigned contact to 236 runs but realized actual plane
contact in only 11 pilot encoder-bias/drift runs:

```text
development / pilot / validation actual-contact runs:
0 / 11 / 0
```

Assigned contact is balanced, but realized contact is fault-coupled and
loudest in an S-exclusive gauge channel. This is not a headline result. It
makes the confirmatory contact schedule a pre-freeze decision and later
Gate-7/Technical-Report audit item.

## Forward correction that must not be lost

`agents/Codex/Session Summaries/HumanReport33.md` contains an incorrect first
row in its measured severity table. The concluded report stays unchanged, but
the Technical Report/limitations record must use:

```text
0.90 | 0.0544 microstrain | 0.13x | validation
```

not `0.95 | 0.0090 | 0.02x | development`.

## Verification baseline

Use the repository venv, never bare system Python:

```powershell
.\venv\Scripts\python.exe -m pytest -q "Reproducibility Packet\tests"
```

Codex Session-36 result:

```text
399 passed in 9.80 s
```

Do not use root-wide `pytest -q` as the clean packet command. Ignored
`tmp/session6_packet_copy/tests` duplicates three test module names and causes
collection mismatch errors. That is workspace discovery, not a packet test
failure.

Session 36 opened no pilot, validation, test, or confirmatory payload/outcome.
It read only approved design fields, committed development evidence, and code
needed to audit the protocol.

## Transcript-order state

Codex Session 36 appended cleanly to the technical thread:

```text
pre-write lines:        4,982
post-write lines:       5,127
Session-36 header:      line 4,984
header count:           1
EOF-anchor matches:     1
technical diff:         +145 / -0
physical last author:   Codex
git diff --check:       clean
```

The complete verified Claude EOF block was used in the actual patch. No
recurrence occurred, so the monitoring thread was not updated.

For every future transcript append:

1. read the UTF-8 physical tail;
2. record the pre-write line count;
3. use the complete unique EOF block in the actual patch;
4. prove the new header occurs exactly once after that boundary;
5. compare the old prefix and re-read the physical tail; and
6. require `+N / -0` before closeout.

## Public record

Root `README.md` already has Claude's Session-36 append-only correction:

- the old threshold was misapplied across window/statistic definitions;
- the corrected coherent bar differs by about 8%, not a factor;
- delivered fault-versus-healthy development distances lie inside the observed
  healthy-pair range;
- this is a development protocol finding, not a distributional or project
  result; and
- Protocol P/config/test remain untouched.

Codex Session 36 added no public entry because its exact proposal block is an
internal review state, not a new scientific result or completed milestone.
Keep the public log lean until the design converges or another result lands.

## Review-cycle state and next actions

The active technical thread is physically last with Codex's explicit block.

Next:

1. Read any new Claude turn and Claude's latest HumanReport before acting.
2. Review the clean replacement text for exactly:
   - selection that always reaches the ladder when a safe candidate exists;
   - a distinct no-admissible-candidate branch;
   - a cellwise or max-cell M2 null;
   - deterministic Stage 0/A/B/C sensor seeds and pair IDs;
   - exact Stage-0 command/sample unit;
   - preserved OOD metric roles;
   - exact across-cell outcome/equality rules; and
   - ordinary-row wording with no directional guarantee.
3. Approve or block that exact proposal state explicitly.
4. Only after proposal approval, Claude may implement and run Protocol P on the
   authorized development-only diagnostic universe with zero non-development
   payload/outcome reads.
5. Review the exact Protocol-P implementation, result, and selected branch.
6. Then review the branch-specific synchronized written Claim Sheet,
   Accessible Claim Sheet, manifest/exclusion, and packet amendment.
7. Review the replacement hash-bound assignment at exact state.
8. Only after written amendment and assignment same-state approval may the
   selected branch be implemented; if it advances, regenerate the non-test
   study from zero and repeat the identity/role/CRN audit.
9. Resume Gate 4 only after the amended development feasibility gate clears.
10. Keep final `config.json` absent and confirmatory identities/payloads at zero
    until Gates 2–7 close.

No regular Codex progress report is due until Session 40 unless a playbook
trigger fires earlier.

## Key files

- `agents/Codex/Session Summaries/HumanReport36.md`
- `agents/Claude/Session Summaries/HumanReport36.md`
- `chats/Claude-Codex/Phase 2 Integration and Config Freeze/Phase 2 Integration
  and Config Freeze - Active.md`
- `Claim Sheet.md`
- `Accessible Claim Sheet.md`
- `Reproducibility Packet/config/proposed-gate3-assignment-v0.1.json`
- `Reproducibility Packet/config/draft-config-v0.1.json`
- `Reproducibility Packet/scripts/utils/rng.py`
- `Reproducibility Packet/scripts/utils/gate3_assignment.py`
- `Reproducibility Packet/scripts/utils/assignment_generator.py`
- `Reproducibility Packet/scripts/analyze_synchronous_detection_floor.py`
- `Reproducibility Packet/scripts/screen_synchronous_safe_probe.py`
- `Reproducibility Packet/scripts/screen_structural_separability.py`
- `Reproducibility Packet/results/structural_separability/`
- `README.md`

## Non-negotiable boundaries

- Development mechanics/screens are not confirmatory results.
- The current separability failure is a feasibility result, not a hypothesis
  failure.
- Do not restore the withdrawn “2x–40x too mild” characterization.
- Do not call healthy and fault distributions indistinguishable from the
  Session-36 range statement.
- Do not run Protocol P before its exact proposal is approved.
- Do not infer unmeasured ladder values from remaining EI 0.75.
- Do not use pooled Q95 as context-robust when a cellwise null is available.
- Do not let pilot outcomes retroactively define confirmatory stratum
  membership.
- Do not move compound/OOD rows into known-class macro-F1.
- Do not call a metric per stratum until every class, row, weight, cell rule,
  and equality rule is defined.
- Do not inspect non-development outcomes to choose the amended design.
- Do not materialize confirmatory identities or payloads before final freeze.
- Reviewer edits, handoffs, downstream use, or silence are not approval;
  require explicit same-state approval.
- Keep detection, attribution, information/action authorization, and control
  outcome separate.
- Keep `config.json` absent until all remaining gates close.
