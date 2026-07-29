# Summary of Only Necessary Context — Codex

**Last completed Codex session:** 37

**Date:** 2026-07-28

**Current phase:** Phase 2 — Integration and Reproducibility Build

**Primary active thread:** `chats/Claude-Codex/Phase 2 Integration and Config
Freeze/Phase 2 Integration and Config Freeze - Active.md`

## Resume here

Gate 4 remains stopped on another text-only Protocol-P/A2 proposal state:

```text
BLOCK_AMENDMENT_A2_PROPOSAL_V4_PENDING_SAFE_TERMINAL_BRANCHES_ROLE_COVERAGE_AND_EXECUTION_PINS
BLOCK_CONFIG_FREEZE_PENDING_PRECONFIRMATORY_BUILD_AND_VALIDATION
```

Claude Session 37 posted `AMENDMENT_A2_PROPOSAL_V4`, a complete Protocol P v2
replacement. Codex Session 37 reviewed that exact text and approved:

1. vector-8 across all four gauges;
2. screening only the development diagnostic trajectory and four balanced
   development context cells;
3. Stage-A selection without a sensor-only T1 cutoff;
4. direct measurement of all ten reserved remaining-EI values;
5. the per-cell Stage-C rule
   `D(v,c) >= 2 * Q95_c` in every screened cell;
6. eight healthy null replicates per cell;
7. retaining all 24 declared candidates while the inclusive torque gate
   eliminates 15 arithmetically, leaving a 108-rollout Stage-A worst case;
8. exact test contact `[1.8, 3.3]`;
9. OOD mechanics labels that never change OOD metric roles;
10. ordinary structural rows remaining in the primary estimand with no claimed
    direction on S-minus-C1;
11. Protocol P v2 as a clean supersession of unapproved v1; and
12. preserving the preregistered severity-to-role allocation rather than
    rebalancing after development evidence.

Protocol P v4 is still blocked because:

- `NO_ADMISSIBLE_PROBE` carries the 0.05 N / ramp-0.5 probe forward after the
  branch says all candidates, including that one, failed a hard safety gate;
- Stage B can label a value `unsafe_at_severity` but the outcome table can then
  silently treat it as sub-threshold or let it contribute to Case C;
- the finite-sample 95th-percentile estimator is not pinned;
- the stated CRN-collapse mechanism contradicts the implementation;
- the proposed observed-data reduction omits the validity mask and measurement
  time arguments required by `harmonic_coefficients`;
- the Stage-0 command writes to a root-level results path rather than the named
  packet results path;
- the thermal term is called exactly cancelling despite post-sum quantization;
  and
- the Case-B role-coverage rule is not yet integrated into the clean protocol.

Claude's next action is another **clean text-only** Protocol P v2 replacement.
Do not implement or run Protocol P, write Amendment A2, edit either Claim Sheet,
build a replacement assignment, regenerate data, fit Gate-4 models, or create
final `config.json` before that exact proposal receives same-state approval.

## Codex Session-37 arbitration

### Stage-C operative rule

Approved:

```text
Q95_c = within-cell healthy/healthy 95th percentile
pass(v) iff D(v,c) >= 2 * Q95_c for c = 4, 5, 6, 7
```

This is the operative per-cell rule. Keep the stricter scalar form:

```text
min_c D(v,c) >= 2 * max_c Q95_c
```

as a predeclared sensitivity only. It is not a second success route.

### Eight replicates

Eight healthy runs per cell are approved. They produce 28 dependent unordered
pairwise distances from eight independent runs. The cost increase is eight
rollouts, about four minutes.

Pin the exact quantile:

```python
Q95_c = np.quantile(within_cell_distances, 0.95, method="higher")
```

Use the same `method="higher"` for descriptive pooled and scalar-sensitivity
quantities. With 28 values this selects the 27th order statistic; with 15 it is
the maximum. This makes the eight-replicate rationale exact.

### Torque pruning

The candidate grid remains:

```text
ramp_fraction_of_duration: 0.125, 0.25, 0.5
peak amplitude N:           0.05, 0.10, 0.15, 0.18,
                            0.20, 0.22, 0.25, 0.30
```

The already-approved inclusive torque gate is:

```text
F_peak * 2 * link_length_m <= 0.60 * torque_abs_limit[0]
```

At link length 0.40 m and joint-0 torque limit 0.20 N m, the boundary is exactly
0.15 N. Values 0.18–0.30 fail before simulation at every ramp fraction.

Treat this as logged evaluation of all 24 candidates, not a grid amendment.
Nine candidates remain; Stage-A worst case is 9 x 4 cells x 3 conditions =
108 rollouts.

### Severity allocation and role coverage

Do **not** rebalance severities. Existing development evidence already points
toward the severe end, so changing which values belong to which roles could
select the final comparison toward an S advantage.

Preserve:

```text
dev:    0.50, 0.75
pilot:  0.60, 0.85
val:    0.40, 0.90
test:   0.35, 0.65
OOD structural components: 0.45 test, 0.55 validation
```

After the direct map, compute known-class testable structural coverage
separately by role. OOD components never count toward known-class coverage.

Prospective boundary:

```text
dev coverage = 0:
  no mechanics-testable structural training support

validation coverage = 0:
  structural selection/calibration unsupported

test coverage = 0:
  four-way testable-stratum confirmatory metric undefined

any of the above:
  named role-coverage-bounded non-transfer branch
  S/C1 analyses may be secondary
  cannot establish full success or hypothesis failure

pilot coverage = 0:
  no relabeling
  no data-driven structural-stratum test downsizing
  retain prospectively allowed maximum test replication
  name the pilot coverage limitation
```

This rule must be inside the next clean proposal before the ladder is measured.

## Safe terminal branches required

### NO_ADMISSIBLE_PROBE

Current v4 text is invalid:

```text
all 24 candidates fail a hard gate
then keep 0.05 N / ramp 0.5 and regenerate
```

The retained probe is one of the failed candidates. It cannot be carried
forward as safe.

Required terminal action:

```text
keep config.json absent
authorize no regeneration
record safety/method or implementation-integrity failure
diagnose or write a separately reviewed fallback amendment
do not automatically pin any failed probe
```

Delivered development rows show 0.05 N / ramp 0.5 passing with wide margin, so
this branch is unlikely. If it occurs anyway, that discrepancy strengthens the
need to stop and diagnose.

### UNSAFE_LADDER_VALUE

`unsafe_at_severity` is not equivalent to M2 fail:

```text
unsafe_at_severity != TESTABLE
unsafe_at_severity != SUB-THRESHOLD
```

It lacks a safe, valid M2 result. The next proposal must give it a separate
terminal method/safety branch with config remaining unfrozen and no automatic
regeneration. Cases A/B/C are available only after all ten values have safe,
valid M2 verdicts.

Do not let unsafe rows silently enter Case B or let “none pass” become Case C
when any value lacked an admissible M2 measurement.

## Exact identity and observed-path pins

### Approved identity namespace

The proposed screen-private identities are sound:

```text
Stage A/B by cell c:
  sensor_seed = 150000 + 10*(c-4) + 2
  pair_id = "basepair_protocolp_stageAB_c{c}"

Stage C:
  k=0 reuses the selected Stage-A healthy identity
  k>=1 uses:
    sensor_seed = 150000 + 10*(c-4) + 1000*k + 2
    pair_id = "basepair_protocolp_stageC_c{c}_k{k}"

Stage 0:
  pair_id = 1
  sensor_seed = 0..199
```

The namespace is disjoint from dataset sensor-seed ranges and deliberately
lacks the dataset-only `_dataset0` pair-id suffix.

### Correct CRN mechanism

`scripts/utils/rng.py` seeds on:

```text
(sensor_seed, pair_id, channel, stream)
```

Changing either `sensor_seed` or `pair_id` changes the generator. Only reusing
the complete `(sensor_seed, pair_id)` pair collapses a replicate onto the same
substreams.

Before Stage-C null statistics, assert:

```text
all eight (sensor_seed, pair_id) tuples unique within each cell
k=0 exactly equals the selected Stage-A healthy identity
k=1..7 distinct from k=0 and one another
```

`Q95_c >= 0.30 microstrain` may remain a diagnostic pause, not an identity
proof or scientific gate. The sensor-only reference is not a mathematical
lower bound on a realized vector distance.

### Exact harmonic reduction

Pin the actual observed-data inputs:

```python
b_g = harmonic_coefficients(
    gauge_obs[:768, g],
    gauge_valid[:768, g],
    gauge_measurement_time_s[:768],
    0.8,
)
```

Use the same onset/index convention for every Stage 0/A/B/C window. The validity
mask preserves dropout handling; measurement time preserves the actual gauge
grid/latency contract.

### Stage-0 output path

If the command starts at the repository root with:

```text
./venv/Scripts/python.exe
```

then the output must be:

```text
--output-dir "Reproducibility Packet/results/protocol_p"
```

not `results/protocol_p`, which would create a root-level artifact. An exact
packet-directory command with `../venv` is also acceptable.

### Thermal wording

Claude measured the difference null as nearly invariant over 0–3 °C. Preserve
that result.

Do not say the thermal term cancels exactly on the realized observed path.
`sensor_model.py` sums thermal, bias, drift, and noise and then quantizes at
0.5 microstrain. The deterministic linear thermal component is removed by the
intercept/trend fit and matched differencing in exact unquantized arithmetic;
post-sum quantization prevents literal samplewise exact cancellation.

State measured insensitivity and the first-order mechanism.

## Findings from Claude Session 37 that remain useful

### T1 is retired as a threshold

Protocol P's statistic is a difference:

```text
D = ||b_fault - b_healthy||_2
```

The former `0.4388` value was the five-sigma point of a single noise-only
vector norm, not a difference. Claude measured:

```text
single-window vector norm:
  mean 0.1957
  p95 0.2834
  5 sigma 0.4388

unmatched difference of two windows:
  mean 0.2787
  p95 0.3958
  5 sigma 0.6526
```

Substituting `0.6526` would still be wrong for matched Stage-A/B differences,
because CRN cancels the sensor path. T1 must not rank candidates or gate the
ladder.

The sensor-only unmatched difference is useful only as a Stage-C reference and
diagnostic.

### Protocol-P statistic

Approved:

```text
D = || concat over gauges g=0..3 [
       beta_cos(fault,g) - beta_cos(healthy,g),
       beta_sin(fault,g) - beta_sin(healthy,g)
     ] ||_2

harmonic fit:
  intercept + centered trend + cos(0.8 Hz) + sin(0.8 Hz)

window:
  W=768 from the exact pinned onset

Stage-A/B comparison:
  matched sensor_seed and pair_id
```

### Stage-A conditions and selection

After closed-form torque pruning, each of the nine remaining candidates runs in
four screened cells at:

```text
healthy
remaining EI 0.75
remaining EI 0.35
```

Hard checks in every cell/condition:

```text
zero A1 safety flags
max |qd_true| <= 8 rad/s
max |q_true| <= 2.5 rad
max |gauge_true| <= 400 microstrain
inclusive torque gate above
no increase in saturated steps versus zero probe
```

Among admissible candidates, select maximum worst-cell `D(0.75)`. Keep the
existing tie-break:

```text
within 1% -> smallest amplitude -> largest ramp fraction
```

No T1 cutoff.

### Direct ladder and OOD boundary

Measure under development conditions:

```text
0.35  test known
0.40  validation known
0.45  test compound/OOD structural component
0.50  development known
0.55  validation compound/OOD structural component
0.60  pilot known
0.65  test known
0.75  development known
0.85  pilot known
0.90  validation known
```

For every safe valid value:

```text
M2 pass -> TESTABLE
M2 fail -> SUB-THRESHOLD
```

No interpolation, monotonicity assumption, numerical cutoff, or later-role
relabeling.

Values 0.45/0.55 characterize mechanics testability only. Their compound rows:

```text
retain ood_flag=true
stay excluded from four-way known-class macro-F1
remain in abstention/unknown/OOD metrics only
do not count for known-class role coverage
```

## Conditional Case-B estimand retained

If all ten values are safe and valid and a proper subset passes:

- primary four-way macro-F1 contains all healthy, actuator, and sensor rows plus
  testable-stratum **known structural** rows;
- every non-structural known-class row has weight 1 and is shared;
- OOD rows retain their separate OOD role;
- one model per suite is trained on the complete authorized manifest;
- S and C1 use identical reservations;
- hierarchical bootstrap preserves shared-row pairing;
- there is one confirmatory decision; and
- the sub-threshold-stratum report is secondary and non-confirmatory.

Apply the role-coverage rule above before deciding whether the branch can support
full success/hypothesis-failure inference.

Ordinary-trajectory structural rows stay in the primary estimand. They are not
certified by the diagnostic margin. Their contribution to S-minus-C1 has no
predeclared direction. Keep a trajectory-stratified secondary report.

## Current gate and data state

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
  BLOCKED on safe, branch-complete Protocol P v2 and corrected Amendment A2

Gates 5–7:
  open

Reproducibility Packet/config.json:
  absent; final configuration is UNFROZEN

Confirmatory test identities/payloads:
  0 / 0

Research result:
  none
```

Exact pre-A2 authorities:

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
same-state approval, the selected provenance policy is **full regeneration from
zero**. The current dataset then becomes a named superseded pre-amendment set in
the exclusion trail. No payload is silently reused under a changed config hash.

## Current separability evidence boundary

Codex Session 34 independently regenerated both tracked development analyses
from the retained dataset and matched every substantive top-level JSON field.

Decision-relevant pooled learned AUROCs:

```text
contrast / suite                  C1      S
structure remaining EI 0.75      0.250   0.172
structure remaining EI 0.50      0.750   0.703
actuator remaining gain 0.50     0.891   0.859
```

Pooled structural effects clearing the paired channel sign test are IMU rather
than gauge channels.

Interpretation:

```text
current delivered structural settings/excitation fail the prerequisite
development feasibility gate
```

Do not interpret this as:

```text
the project hypothesis is false
the whole mild band has a negative result
pilot or validation confirms development
fault and healthy distributions are proven indistinguishable
the withdrawn 2x–40x severity claim is valid
```

The diagnostic-only sign-test report has four cells, so its exact two-sided
floor is 0.125. Its empty `p <= 0.05` attribution table is arithmetically forced.

## Contact-design fact that remains live

The pre-A2 472-run set assigned contact to 236 runs but realized actual plane
contact in only 11 pilot encoder-bias/drift runs:

```text
development / pilot / validation actual-contact runs:
0 / 11 / 0
```

Assigned contact is balanced, but realized contact is fault-coupled and loudest
in an S-exclusive gauge channel. This is not a headline result. It makes the
confirmatory contact schedule a pre-freeze decision and later Gate-7/Technical
Report audit item.

Approved replacement:

```text
contact_test_sustained.contact_window_offset_s = [1.8, 3.3]
```

## Forward corrections that must not be lost

`agents/Codex/Session Summaries/HumanReport33.md` contains an incorrect first
row in its measured severity table. The concluded report stays unchanged, but
the Technical Report/limitations record must use:

```text
0.90 | 0.0544 microstrain | 0.13x | validation
```

not `0.95 | 0.0090 | 0.02x | development`.

`agents/Codex/Session Summaries/HumanReport36.md` calls `0.4388` the coherent
vector-8 five-sigma threshold. Claude Session 37 showed that it is a
single-window norm threshold, not the difference statistic used by Protocol P.
Do not carry that old wording forward. T1 is retired as described above.

## Verification baseline

Use the repository venv, never bare system Python:

```powershell
.\venv\Scripts\python.exe -m pytest -q "Reproducibility Packet\tests"
```

The last full packet result before this closeout remains:

```text
399 passed
```

Do not use root-wide `pytest -q` as the clean packet command. Ignored
`tmp/session6_packet_copy/tests` duplicates three test module names and causes
collection mismatch errors. That is workspace discovery, not a packet failure.

Codex Session 37 ran no project rollout. Its only Python execution before
closeout was a read-only NumPy quantile-method check under the repository venv.
It read zero non-development payloads and generated zero confirmatory identities.

## Transcript-order state

Codex Session 37 appended cleanly to the technical thread:

```text
pre-write lines:          5,632
post-write lines:         5,805
Session-37 header:        line 5,634
header count:             1
header after boundary:    yes
technical diff:           +173 / -0
physical last author:     Codex
old-prefix SHA-256:       exact match through former final newline
```

The first prefix calculation accidentally included the newly appended separator
newline. Recomputing immediately before that new byte reproduced the exact
pre-write SHA-256:

`49923045DBF2615FDD6EC6BA65352B9625FB8759BC0ABCE31E4D054E0C6C7032`

No prior byte changed. No monitoring-thread update was needed.

For every future transcript append:

1. read the UTF-8 physical tail;
2. record the pre-write line count and hash;
3. use the complete unique EOF block in the actual patch;
4. prove the new header occurs exactly once after that boundary;
5. hash the old prefix through its former final newline, excluding any newly
   appended separator byte;
6. re-read the physical tail; and
7. require `+N / -0` before closeout.

## Public record

Codex Session 37 added no public entry. The session produced an internal
same-state protocol block, not a new scientific result, completed artifact, or
phase transition. Keep the public Live-Run README lean.

## Review-cycle state and next actions

The active technical thread is physically last with Codex's explicit v4 block.

Next:

1. Read any new Claude turn and latest Claude HumanReport before acting.
2. Review the clean replacement for:
   - terminal `NO_ADMISSIBLE_PROBE` with no failed probe carried forward;
   - separate terminal `UNSAFE_LADDER_VALUE`;
   - Cases A/B/C only after ten safe valid M2 verdicts;
   - `np.quantile(..., method="higher")`;
   - correct complete-tuple CRN explanation;
   - deterministic Stage-C tuple assertions;
   - exact `gauge_obs`, validity-mask, measurement-time, window, and onset
     reduction;
   - packet-correct Stage-0 output path;
   - measured/first-order thermal-insensitivity wording;
   - preserved severity-to-role assignments;
   - dev/pilot/validation/test role-coverage handling; and
   - all previously approved OOD, ordinary-row, contact, vector-8, and direct-map
     boundaries.
3. Approve or block that exact proposal state explicitly.
4. Only after proposal approval may Claude implement Protocol P.
5. Review the exact implementation before execution.
6. After an approved development-only run, review the exact result and selected
   branch.
7. Then review the synchronized written Claim Sheet, Accessible Claim Sheet,
   manifest/exclusion, packet amendment, and replacement hash-bound assignment.
8. Only after written amendment and assignment same-state approval may the
   selected branch regenerate the non-test study from zero.
9. Resume Gate 4 only after the amended development feasibility gate clears.
10. Keep final `config.json` absent and test identities/payloads at zero until
    Gates 2–7 close.

No regular Codex progress report is due until Session 40 unless a playbook
trigger fires earlier.

## Non-negotiable boundaries

- Development mechanics/screens are not confirmatory results.
- The current separability failure is a feasibility result, not a hypothesis
  failure.
- Do not restore the withdrawn “2x–40x too mild” characterization.
- Do not call healthy and fault distributions indistinguishable from a range
  statement.
- Do not run Protocol P before its exact proposal is approved.
- Do not carry a probe forward after a branch declares it unsafe.
- Do not convert `unsafe_at_severity` into sub-threshold or Case C.
- Do not leave a decision-bearing finite-sample quantile method implicit.
- Do not treat a numeric null tripwire as proof of unique RNG identities.
- Do not infer unmeasured ladder values or assume monotonicity.
- Do not use pooled Q95 as the operative context-robust null.
- Do not rebalance severities after development evidence toward predicted
  detectability.
- Do not let pilot outcomes retroactively define confirmatory membership.
- Do not move compound/OOD rows into known-class macro-F1 or known-class role
  coverage.
- Do not call a metric per stratum until every class, row, weight, cell rule,
  equality rule, and role-coverage rule is defined.
- Do not inspect non-development outcomes to choose the amended design.
- Do not materialize confirmatory identities or payloads before final freeze.
- Reviewer edits, handoffs, downstream use, or silence are not approval; require
  explicit same-state approval.
- Keep detection, attribution, information/action authorization, and control
  outcome separate.
- Keep `config.json` absent until all remaining gates close.
