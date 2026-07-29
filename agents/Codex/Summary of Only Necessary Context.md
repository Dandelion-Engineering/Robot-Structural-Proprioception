# Summary of Only Necessary Context — Codex

**Last completed Codex session:** 38

**Date:** 2026-07-28

**Current phase:** Phase 2 — Integration and Reproducibility Build

**Primary active thread:** `chats/Claude-Codex/Phase 2 Integration and Config
Freeze/Phase 2 Integration and Config Freeze - Active.md`

## Resume here

Gate 4 remains stopped on another text-only Protocol-P/A2 proposal state:

```text
BLOCK_AMENDMENT_A2_PROPOSAL_V5_PENDING_EXECUTABLE_COMMAND_SHAPE_GUARD_TERMINAL_CLASSIFIER_AND_UNMATCHED_SCOPE_PINS
BLOCK_CONFIG_FREEZE_PENDING_PRECONFIRMATORY_BUILD_AND_VALIDATION
```

Claude Session 38 posted `AMENDMENT_A2_PROPOSAL_V5`, a clean Protocol P v2.1
replacement. Codex Session 38 independently reproduced and approved the main
new scientific correction: all plant-bearing Protocol-P windows must begin at
the config-derived diagnostic-probe start, not at fault onset.

Codex also explicitly approved:

1. refusing a response-selected peak-aligned window;
2. carrying the probe-start rule into the written amendment and later
   hash-bound assignment;
3. retaining seven zero-rollout unmatched distances as a descriptive
   sensitivity only; and
4. reporting known-class structural role coverage as `0/1/2` separately for
   development, pilot, validation, and test.

Protocol P v2.1 remains blocked because:

- the Stage-0 command uses `cmd.exe` caret continuations in a PowerShell
  project;
- the measurement-time reduction silently accepts any `[T,M]` array and drops
  columns rather than enforcing an exact shape;
- the `NO_ADMISSIBLE_PROBE` contradiction classifier attributes every
  healthy/EI-0.75 candidate failure to implementation integrity even though
  prior same-configuration evidence exists only for the 0.05 N / ramp-0.5
  candidate;
- the unmatched secondary is incorrectly described as bounding a general
  one-shot unmatched comparison despite sharing one fixed fault-side
  realization; and
- the rejected empirical-peak disclosure says step 1216 / 2.088, while an
  every-start reproduction gives step 1208 / 2.0929. This does not change the
  operative window.

Claude's next action is one clean **Protocol P v2.2** replacement. Do not
implement or run Protocol P, write Amendment A2, edit either Claim Sheet, build
a replacement assignment, regenerate data, fit Gate-4 models, or create final
`config.json` before that exact proposal receives same-state approval.

## Codex Session-38 decisions

### Finding J: probe-start origin approved

The delivered generator computes:

```text
diagnostic_tip_load_start_s = onset_time_s + diagnostic_probe.start_offset_s
```

For development `t01`:

```text
fault onset:   1.0 s / step 500
probe start:   2.0 s / step 1000
probe end:     step 1625
correct W=768: [1000,1768)
```

The plant applies the probe while advancing step 1000. Stored rows are
post-integration, so the first probe-affected record row is step 1000 at
`t_s=2.002`. Do not shift the slice to 999 merely because row 999 has stored
time 2.000; it is the result of the interval ending at probe start.

Codex independently recomputed privileged vector-8 differences from delivered
development rows:

```text
remaining EI  cell   D @ step 500   D @ step 1000   ratio
0.75          r00       0.0649          0.1584       2.44
0.75          r01       0.0598          0.1593       2.67
0.75          r02       0.0368          0.0872       2.37
0.75          r03       0.0266          0.0968       3.64
0.50          r00       0.1868          0.4787       2.56
0.50          r01       0.1847          0.4755       2.58
0.50          r02       0.0841          0.2755       3.28
0.50          r03       0.0778          0.2798       3.60
```

The old origin suppressed the privileged structural difference by roughly
2.4–3.6 times.

The probe-free ordinary trajectory reproduced at its own onset, step 400:

```text
healthy ||b||:  0.4771  0.4850  0.4993  0.5075
D at EI 0.75:   0.0129  0.0155  0.0200  0.0246
D at EI 0.50:   0.0257  0.0256  0.0488  0.0531
```

This is development mechanics evidence, not a learned, pilot, validation,
confirmatory, or project-hypothesis result.

Prospective origins:

```text
dev:    [1000,1768) of 3000
pilot:  [1150,1918) of 3050
val:    [1025,1793) of 3075
test:   [1175,1943) of 3125
```

All are config-derived, on-grid, and in-bounds. This check read assignment text
only for non-development splits; no non-development outcome was opened.

The rejected data-selected alternative was independently checked on the r00
healthy development trace:

```text
step 1208: ||b|| = 2.092897106   actual every-start maximum
step 1216: ||b|| = 2.088070233
step 1000: ||b|| = 1.880585474
```

Keep the principled step-1000 probe start. Correct or remove the nonoperative
peak number.

### Unmatched sensitivity boundary

Approved arithmetic:

```text
D_unmatched(v,c,k) =
  || b(fault at v, identity_AB) - b(healthy_k, identity_k) ||
for k = 1..7
```

Required interpretation:

```text
conditional descriptive sensitivity
seven dependent distances sharing one fixed fault-side identity
no quantile, gate, pass/fail route, or inferential bound
```

These values do not bound a general one-shot unmatched comparison because the
fault side is unreplicated. The matched statistic remains the only mechanics
verdict. `TESTABLE` means a necessary mechanical signature, not guaranteed
learnability by S or C1.

### Role-coverage counts

Report known-class testable structural counts `0/1/2` by role. OOD components
at 0.45/0.55 never count.

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

Count 1 is reported as a thin single-severity role but is not a new terminal
branch.

## Four exact corrections required in Protocol P v2.2

### 1. PowerShell-executable Stage-0 command

Current `^` line continuations are `cmd.exe` syntax. PowerShell passes them as
literal arguments:

```text
.\venv\Scripts\python.exe -c "import sys; print(sys.argv)" ^
-> ['-c', '^']
```

Use one PowerShell-executable line, PowerShell backticks, or a PowerShell
argument array. Retain:

```text
working directory: Reproducibility Packet
venv path:         ..\venv\Scripts\python.exe
output default:    results/protocol_p
```

### 2. Exact measurement-time shape

Current text:

```python
t_g = tm if tm.ndim == 1 else tm[:, 0]
```

silently accepts `[T,M]`. The current `ObservedRecord` contract and delivered
development records use `[T]`. Prefer requiring `[T]` only. If `[T,1]` legacy
support is deliberately retained, accept exactly:

```python
if tm.ndim == 1:
    t_g = tm
elif tm.ndim == 2 and tm.shape[1] == 1:
    t_g = tm[:, 0]
else:
    raise ValueError(...)
```

Then assert its length equals `gauge_obs.shape[0]` and
`gauge_valid.shape[0]`. `harmonic_coefficients` already enforces final
one-dimensional alignment, finite/strictly increasing times, and sufficient
valid samples.

### 3. Scope the terminal contradiction

Prior delivered-row safety evidence applies only to:

```text
peak = 0.05 N
ramp_fraction_of_duration = 0.5
conditions = healthy, EI 0.75, EI 0.50
```

Required classifier:

```text
0.05 N / ramp 0.5 fails healthy or EI 0.75:
  contradicts its delivered-row pass
  implementation-integrity failure

that candidate passes those conditions but fails EI 0.35:
  newly observed physical safety/method limit

other candidates' failures:
  record normally
  do not by themselves classify a prior-evidence contradiction
```

The terminal action is unchanged in every case:

```text
config.json stays absent
no probe is pinned
no regeneration is authorized
diagnose or write a separately reviewed fallback amendment
```

### 4. Remove unmatched “bound” language

Keep the seven arithmetic values, but label them with the conditional,
dependent, descriptive scope above.

## Protocol P v2.1 content retained for v2.2

The following is substantively approved:

- vector-8 over all four gauges;
- development diagnostic trajectory only for Protocol P;
- balanced development context cells 4/5/6/7;
- config-derived `[w0:w1]` probe-start slice;
- observed `gauge_obs`, `gauge_valid`, measurement time, and 0.8-Hz reduction;
- matched `(sensor_seed,pair_id)` identity in Stage A/B;
- screen-private identity namespace;
- Stage-A selection without a sensor-only T1 cutoff;
- all 24 candidates declared, with 15 deterministically excluded under the
  inclusive torque gate;
- nine simulated candidates and 108-rollout Stage-A worst case;
- direct measurement of ten remaining-EI values;
- safe terminal `NO_ADMISSIBLE_PROBE`;
- separate terminal `UNSAFE_LADDER_VALUE`;
- Cases A/B/C only after ten safe, valid M2 verdicts;
- eight healthy Stage-C runs per cell;
- deterministic tuple assertions;
- `np.quantile(..., 0.95, method="higher")`;
- operative per-cell rule:
  `D(v,c) >= 2 * Q95_c` in every cell;
- stricter scalar rule as a sensitivity only;
- Q95 numeric tripwire as a diagnostic pause only;
- OOD rows kept outside known-class macro-F1 and role coverage;
- ordinary structural rows kept in the primary estimand without a claimed
  direction;
- exact test contact `[1.8,3.3]`;
- preserved severity-to-role allocation;
- known-class role-coverage rule;
- measured thermal near-invariance plus first-order mechanism;
- the unchanged success bar; and
- nonterminal worst-case cost:
  `108 + 32 + 28 = 168 rollouts`.

## Safe terminal branches retained

### NO_ADMISSIBLE_PROBE

If all declared candidates fail a hard gate:

```text
keep config.json absent
authorize no regeneration
pin no failed probe
record method/safety and applicable integrity facts
diagnose or write a new same-state-reviewed fallback amendment
```

### UNSAFE_LADDER_VALUE

`unsafe_at_severity` is not equivalent to M2 failure:

```text
unsafe_at_severity != TESTABLE
unsafe_at_severity != SUB-THRESHOLD
```

It lacks a safe, valid M2 result. If any value is unsafe, the branch is
terminal, config remains unfrozen, and Cases A/B/C are unavailable.

## Exact identity and statistic state retained

Screen identities:

```text
Stage A/B by cell c:
  sensor_seed = 150000 + 10*(c-4) + 2
  pair_id = "basepair_protocolp_stageAB_c{c}"

Stage C:
  k=0 reuses selected Stage-A healthy identity
  k>=1:
    sensor_seed = 150000 + 10*(c-4) + 1000*k + 2
    pair_id = "basepair_protocolp_stageC_c{c}_k{k}"

Stage 0:
  pair_id = 1
  sensor_seed = 0..199
```

RNG key:

```text
(sensor_seed, pair_id, channel, stream)
```

Changing either `sensor_seed` or `pair_id` changes the generator. Only reusing
the complete tuple collapses a replicate. Deterministically assert all eight
Stage-C tuples unique within cell, k=0 equal to selected Stage-A healthy, and
k=1..7 distinct from k=0 and one another.

Statistic:

```text
D = || concat over gauges g=0..3 [
       beta_cos(fault,g) - beta_cos(healthy,g),
       beta_sin(fault,g) - beta_sin(healthy,g)
     ] ||_2
```

Use `harmonic_coefficients` with the observed signal, validity mask,
measurement-time slice, and 0.8 Hz. Do not restore T1 as a gate.

## Broader gate and data state

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
  BLOCKED on executable Protocol P v2.2 and corrected Amendment A2

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

Ignored local dataset:

`data/gate3-base-dev-pilot-val-c1-s`

It is a pre-amendment non-test dataset, not a final amended dataset. Do not
delete, relabel, or silently reuse it under a changed config hash. If a written
A2 amendment and replacement assignment later receive joint approval, the
selected provenance policy is full regeneration from zero.

## Current development evidence boundary

Codex Session 34 independently reproduced Claude's tracked development
separability outputs.

Pooled learned AUROCs:

```text
contrast / suite                  C1      S
structure remaining EI 0.75      0.250   0.172
structure remaining EI 0.50      0.750   0.703
actuator remaining gain 0.50     0.891   0.859
```

Interpretation:

```text
the delivered structural settings/excitation fail the prerequisite
development feasibility gate under that analysis
```

Do not call this:

```text
project-hypothesis failure
a whole-band negative
pilot or validation confirmation
proof that fault and healthy distributions are indistinguishable
```

Read it beside Findings F–J: the old screen used a mixture of post-onset
windows, many of which contained no probe. Finding J corrects future
Protocol-P measurement; it does not silently rewrite the earlier analysis.

## Contact fact retained

The pre-A2 472-run set assigned contact to 236 runs but realized actual plane
contact in only 11 pilot encoder-bias/drift runs:

```text
development / pilot / validation actual-contact runs:
0 / 11 / 0
```

Assigned contact is balanced; realized contact is fault-coupled and loudest in
an S-exclusive gauge channel. This is not a headline result. The approved
replacement contact pin remains:

```text
contact_test_sustained.contact_window_offset_s = [1.8, 3.3]
```

## Forward corrections that must not be lost

`agents/Codex/Session Summaries/HumanReport33.md` contains an incorrect first
row in its measured severity table. Keep the concluded report unchanged, but
future technical reporting must use:

```text
0.90 | 0.0544 microstrain | 0.13x | validation
```

not `0.95 | 0.0090 | 0.02x | development`.

`agents/Codex/Session Summaries/HumanReport36.md` calls `0.4388` the coherent
vector-8 five-sigma threshold. It is a single-window norm threshold, not the
difference statistic. T1 is retired.

Claude Session 38's rejected empirical-peak location must be corrected from
`1216 / 2.088` to `1208 / 2.0929`, or reduced to an approximately 11% statement.

## Verification baseline

Use the repository venv, never bare system Python:

```powershell
.\venv\Scripts\python.exe -m pytest -q "Reproducibility Packet\tests"
```

The last full packet baseline before this closeout remains:

```text
399 passed
```

Do not use root-wide `pytest -q`; ignored `tmp/session6_packet_copy/tests`
duplicates module names and causes collection mismatches.

Codex Session 38 ran no project rollout. It read development payload values
only. A broad filename listing printed non-development filenames while locating
role roots, but no non-development payload content or outcome was opened.

## Transcript-order state

Codex Session 38 appended cleanly:

```text
pre-write lines:          6,169
post-write lines:         6,425
Session-38 header:        line 6,171
header count:             1
header after boundary:    yes
technical diff:           +256 / -0
physical last author:     Codex
old prefix bytes:         563,382
old-prefix SHA-256:       exact match
```

Old-prefix SHA-256:

`2F9900273CE7CCE6B0D47FBBD911D5CE1D573D2C53272950FEFB861685520BC4`

No monitoring-thread update was needed.

For every future transcript append:

1. read the UTF-8 physical tail;
2. record pre-write line count, byte count, and hash;
3. verify the complete actual EOF anchor is unique;
4. use that complete anchor in the patch;
5. prove the new header occurs exactly once after the old line boundary;
6. hash the old byte prefix through its former final newline;
7. re-read the physical tail; and
8. require `+N / -0`.

## Public record

Claude Session 38 already added the public Finding-J correction. Codex Session
38 added no public entry because it produced an internal same-state text block,
not a new scientific result, completed artifact, or phase transition. Keep the
Live-Run README lean.

## Review-cycle next actions

1. Read any new Claude turn and latest Claude HumanReport before acting.
2. Review Protocol P v2.2 for:
   - a PowerShell-executable Stage-0 command;
   - exact measurement-time rank/shape/length guards;
   - contradiction classification scoped to 0.05 N / ramp-0.5 prior evidence;
   - unmatched values labeled dependent fixed-fault descriptive sensitivity;
   - corrected or removed rejected-peak location;
   - all v2.1 safe branches, quantile, CRN, origin, role, OOD, ordinary-row,
     contact, torque, and success-bar pins retained.
3. Explicitly approve or block that exact proposal state.
4. Only after proposal approval may Claude implement Protocol P.
5. Review the exact implementation before execution.
6. After an approved development-only run, review the exact result and selected
   branch.
7. Then review synchronized written Claim Sheet, Accessible Claim Sheet,
   manifest/exclusion, packet amendment, and replacement assignment.
8. Only after written amendment and assignment same-state approval may the
   selected branch regenerate the non-test study from zero.
9. Resume Gate 4 only after the amended development feasibility gate clears.
10. Keep `config.json` absent and test identities/payloads at zero until Gates
    2–7 close.

No regular Codex progress report is due until Session 40 unless a playbook
trigger fires earlier.

## Non-negotiable boundaries

- Development mechanics/screens are not confirmatory results.
- The current separability failure is a feasibility result, not a hypothesis
  failure.
- Do not run Protocol P before its exact proposal and implementation are
  approved.
- Do not use `cmd.exe` caret continuations in a PowerShell runbook.
- Do not let a permissive shape coercion become an analyst choice.
- Do not classify failures of unmeasured candidates as contradictions of prior
  evidence.
- Do not call fixed-fault unmatched sensitivities empirical bounds.
- Do not choose the harmonic window from response magnitude.
- Do not carry a probe forward after a branch declares it unsafe.
- Do not convert `unsafe_at_severity` into sub-threshold or Case C.
- Do not leave a decision-bearing finite-sample quantile method implicit.
- Do not treat a numeric null tripwire as proof of unique RNG identities.
- Do not infer unmeasured ladder values or assume monotonicity.
- Do not use pooled Q95 as the operative context-robust null.
- Do not rebalance severities after development evidence toward predicted
  detectability.
- Do not let pilot outcomes retroactively define confirmatory membership.
- Do not move OOD rows into known-class macro-F1 or role coverage.
- Do not inspect non-development outcomes to choose the amended design.
- Do not materialize confirmatory identities or payloads before final freeze.
- Reviewer edits, handoffs, downstream use, or silence are not approval.
- Keep detection, attribution, information/action authorization, and control
  outcome separate.
- Keep `config.json` absent until all remaining gates close.
