# Summary of Only Necessary Context — Codex

**Last completed Codex session:** 39

**Date:** 2026-07-29

**Current phase:** Phase 2 — Integration and Reproducibility Build

**Primary active thread:** `chats/Claude-Codex/Phase 2 Integration and Config
Freeze/Phase 2 Integration and Config Freeze - Active.md`

## Resume here

Gate 4 remains stopped on another text-only Protocol-P/A2 proposal:

```text
BLOCK_AMENDMENT_A2_PROPOSAL_V6_PENDING_EXACT_SCREEN_CONSTRUCTION_IDENTITY_REFERENCE_AND_INTERPRETATION
BLOCK_CONFIG_FREEZE_PENDING_PRECONFIRMATORY_BUILD_AND_VALIDATION
```

Claude Session 39 posted `AMENDMENT_A2_PROPOSAL_V6`, Protocol P v2.2. Codex
Session 39 approved all four requested v2.1 corrections, the corrected rejected
peak location, the concept of a generator-authoritative construction, the
bounded one-row replay result, Finding L's unmatched-identity confound and
downward odds correction, and the gauge-only null arithmetic at descriptive
scope.

Protocol P v2.2 remains blocked because:

1. `_generate_reservation` appends `_dataset0`, so the proposal's suffix-free
   screen `pair_id` is not the actual RNG/record identity the named construction
   produces;
2. the current generator has no executable injection seam for the declared
   candidate ramp or direct structural `FaultSpec`;
3. the replay reference is retained local ignored data, not a committed
   payload, and the public claim generalized one exact row to the whole
   retained dataset;
4. Finding L does not cancel from Finding J's different-window ratio merely
   because the same two rows were used;
5. the gauge-only fixed-trace redraw cannot uniquely classify a Case-C
   mechanism; and
6. one zero-override healthy replay cannot locate a later candidate failure
   above the generator.

Claude's next action is one clean **Protocol P v2.3** replacement. Do not
implement or run Protocol P, write Amendment A2, edit either Claim Sheet, build
a replacement assignment, regenerate data, fit Gate-4 models, or create final
`config.json` before that exact proposal receives same-state approval.

## Codex Session-39 decisions

### Exact one-row replay approved

Codex independently replayed:

```text
scenario_dev_t01_f000_r00
```

through the current bound draft config, approved assignment, and
`_generate_reservation`. Result:

```text
elapsed:              26.971 s
privileged fields:    20 / 20 byte-identical
S payload arrays:     38 / 38 byte-identical
safety events:        0
contact steps:        0
```

This is one-row development reproducibility evidence, not whole-dataset
reproduction.

The exact retained local references are:

```text
plant run:
  scenario_dev_t01_f000_r00_S_dataset0
  sha256 ed5b1f39f4ba535c60eb3e1b8587c7b03f59a5c3f9c1189b55635f0d49b65e45

S observation run:
  scenario_dev_t01_f000_r00_S_dataset0
  sha256 cdde17f6d32c5d648249f4a9b343ec3f997b04c83cadacbf9d2c5f1186bb4c83
```

The reference lives under ignored:

`data/gate3-base-dev-pilot-val-c1-s`

The replay gate must hash-check the indexed local reference before comparing
arrays and fail loudly if it is absent or changed.

The public README preserves Claude's broad entry and now carries an append-only
Codex correction: one retained development row replayed exactly; all 472
retained reservations were not regenerated.

### Finding K: construction authority approved, exact interface blocked

The real delivered construction is:

```text
_generate_reservation
  -> C0 OnlineSensorSession drives the closed loop
  -> privileged plant trace is produced
  -> SensorModel.observe(..., "S", ...) produces S post hoc
```

That authority is correct and must be shared by Protocol P and later Gate 7.
An online-S construction remains untested and unauthorized.

The current function does not accept the proposal's four overrides:

```text
peak:
  read from assignment trajectory diagnostic_probe.peak_force_n

ramp:
  _physical_config hard-codes duration / 2.0

structural severity:
  _fault_components derives it from reservation.fault_setting_id

identity:
  reservation.base_pair_id is transformed to
  f"{base_pair_id}_dataset0"
```

Protocol P v2.3 must define a concrete typed override seam for peak, ramp,
structural `FaultSpec`, and screen reservation identity. It must not silently
mutate the approved assignment or stamp an altered screen run as if the base
config hash alone fully described it.

Required provenance:

```text
base config hash
approved assignment hash
protocol-spec hash
exact candidate / cell / condition overrides
```

Decision-bearing checks must use explicit exceptions, not Python `assert`.

### Actual screen identities

`ScenarioReservation.base_pair_id` and the RNG/record `pair_id` are different
objects under the current generator.

Example independently observed:

```text
reservation.base_pair_id:
  basepair_dev_t01_f000_r00

actual returned / ObservedRecord pair_id:
  basepair_dev_t01_f000_r00_dataset0
```

Therefore the proposed Stage-A identity:

```text
basepair_protocolp_stageAB_c4
```

becomes, under the named function:

```text
basepair_protocolp_stageAB_c4_dataset0
```

The same transformation applies to Stage C. v2.3 must either:

1. accept the suffix and update every identity table, RNG tuple, uniqueness
   assertion, and leak explanation; or
2. define and test a distinct suffix-free screen construction.

Under the current generator, a leaked screen row cannot be said to fail because
it lacks `_dataset0`; it has that suffix. The assignment audit should reject it
because its base reservation/seeds/fields are absent from the approved
reservation set.

### Finding L: approved core, narrowed Finding J

Approved facts:

- delivered healthy and structural rows use different
  `(sensor_seed,pair_id)` tuples;
- because C0 sensor noise drives the controller, their plant traces diverge
  from both fault and unmatched control-noise realizations;
- absolute delivered-row differences are not matched fault effects;
- Session-38 odds used an inflated signal estimate and a gauge-only incomplete
  null estimate;
- both errors favoured the hypothesis; and
- Case B with dev coverage 1 and Case C are now roughly comparable rather than
  Case B leading.

Rejected statement:

```text
the confound is common to numerator and denominator,
so the 2.37–3.64x ratio is clean
```

The two norms reduce different time windows:

```text
R = || f_probe_window + n_probe_window ||
    / || f_onset_window + n_onset_window ||
```

The unmatched divergence need not have the same 0.8-Hz content in both
windows, and the norm is nonlinear. Nothing cancels merely because the same
two rows are used.

Finding J's **prospective design conclusion** remains approved:

```text
all plant-bearing Protocol-P windows begin at the config-derived
diagnostic-probe start, not fault onset and not a response-selected peak
```

The 2.37–3.64× numbers may be retained only as descriptive ratios of the total
unmatched-row harmonic differences. Do not call them clean fault-effect
multipliers or say the confound cancels.

The rejected data-selected alternative remains:

```text
step 1208: ||b|| = 2.092897106   actual every-start maximum
step 1000: ||b|| = 1.880585474   prospective probe-start origin
gain:      11.2897%
```

Keep step 1000.

### Gauge-only Stage-C secondary

Approved arithmetic:

```text
one fixed healthy k=0 plant trace per cell
original k=0 observation plus redraws at k=1..7 identities
all 28 within-cell pair distances
Q95_c^gauge with np.quantile(..., 0.95, method="higher")
```

Required label:

```text
conditional descriptive healthy-null diagnostic
one fixed plant trace
zero authority over selection, thresholds, or verdicts
```

It may report whether and how much the full healthy null exceeds the fixed-trace
redraw term. It may not uniquely distinguish:

```text
no mechanical signature
vs
closed-loop divergence dominates
```

Components may interact/cancel and one fixed trace does not identify a
population decomposition.

### Replay gate scope

The replay gate validates one zero-override healthy row. It does not validate:

```text
candidate peak injection
candidate ramp injection
structural severity injection
screen-private identity construction
remEI 0.75
all context cells
```

If the previously measured 0.05 N / ramp-0.5 candidate later contradicts its
delivered-row safety pass, classify an implementation-integrity contradiction
and diagnose it. Do not say the replay proves the defect lies “above the
generator.”

## Protocol P v2.2 content retained for v2.3

The following is substantively approved:

- PowerShell single-line Stage-0 command from packet working directory;
- exact measurement-time rank/width/length validation;
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
- `np.quantile(..., 0.95, method="higher")`;
- operative per-cell rule:
  `D(v,c) >= 2 * Q95_c` in every cell;
- stricter scalar rule as a sensitivity only;
- Q95 numeric tripwire as a diagnostic pause only;
- dependent fixed-fault unmatched distances at descriptive scope only;
- OOD rows kept outside known-class macro-F1 and role coverage;
- ordinary structural rows kept in the primary estimand without a claimed
  direction;
- exact test contact `[1.8,3.3]`;
- preserved severity-to-role allocation;
- known-class role-coverage rule;
- measured thermal near-invariance plus first-order mechanism;
- the unchanged success bar; and
- nonterminal cost `1 + 108 + 32 + 28 = 169` rollouts if the replay remains.

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

Prior delivered-row safety evidence applies only to:

```text
peak = 0.05 N
ramp_fraction_of_duration = 0.5
conditions = healthy, EI 0.75, EI 0.50
```

Classifier:

```text
0.05 N / ramp 0.5 fails healthy or EI 0.75:
  implementation-integrity contradiction with delivered-row evidence
  diagnose without pre-locating the defect

that candidate passes those conditions but fails EI 0.35:
  newly observed physical safety/method limit

other candidates' failures:
  record normally
  do not classify prior evidence
```

### UNSAFE_LADDER_VALUE

`unsafe_at_severity` is not equivalent to M2 failure:

```text
unsafe_at_severity != TESTABLE
unsafe_at_severity != SUB-THRESHOLD
```

If any value is unsafe, the branch is terminal, config remains unfrozen, and
Cases A/B/C are unavailable.

## Role-coverage rule retained

Report known-class testable structural counts `0/1/2` separately for dev,
pilot, validation, and test. OOD 0.45/0.55 components never count.

```text
dev coverage = 0:
  no mechanics-testable structural training support

validation coverage = 0:
  structural selection/calibration unsupported

test coverage = 0:
  four-way testable-stratum confirmatory metric undefined

any of those:
  role-coverage-bounded non-transfer branch
  S/C1 analyses may be secondary
  cannot establish full success or hypothesis failure

pilot coverage = 0:
  no relabeling or data-driven test downsizing
  retain prospectively allowed maximum test replication
  name limitation
```

Count 1 is reported as a thin role but creates no new terminal branch.

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
  BLOCKED on executable Protocol P v2.3 and corrected Amendment A2

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

The ignored dataset is pre-amendment non-test data. Do not delete, relabel, or
silently reuse it under a changed config hash. If a written A2 amendment and
replacement assignment later receive joint approval, the selected provenance
policy remains full regeneration from zero.

## Current development evidence boundary

Pooled learned AUROCs from the delivered development screen:

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
whole-band negative
pilot or validation confirmation
proof fault and healthy distributions are indistinguishable
```

The delivered structural absolute differences are additionally confounded by
unmatched control identities. The old analysis used mixed post-onset windows,
many containing no probe. The future Protocol-P design fixes those issues; it
does not silently rewrite the earlier evidence.

## Forward corrections that must not be lost

`agents/Codex/Session Summaries/HumanReport33.md` contains an incorrect first
row in its measured severity table. Future reporting must use:

```text
0.90 | 0.0544 microstrain | 0.13x | validation
```

not `0.95 | 0.0090 | 0.02x | development`.

`agents/Codex/Session Summaries/HumanReport36.md` calls `0.4388` the coherent
vector-8 five-sigma threshold. It is a single-window norm threshold, not the
difference statistic. T1 is retired.

Claude Session 38's original empirical-peak location is corrected to:

```text
1208 / 2.0929 / 11.2897%
```

Claude Session 39's “whole dataset rebuilds” public headline is corrected
forward: one retained development row replayed exactly.

Finding J's 2.37–3.64× values must be labeled total unmatched-row
different-window ratios, not clean fault-signal multipliers.

## Verification baseline

Use the repository venv, never bare system Python:

```powershell
.\venv\Scripts\python.exe -m pytest -q "Reproducibility Packet\tests"
```

Codex Session 39:

```text
399 passed in 9.94s
```

Do not use root-wide `pytest -q`; ignored
`tmp/session6_packet_copy/tests` duplicates module names and can pollute
collection.

Codex Session 39 opened only development payload content and spent one replay
of an already-delivered healthy development row. It opened no pilot,
validation, or test payload content, generated no Protocol-P identity, and
computed no Protocol-P statistic.

## Transcript-order state

Codex Session 39 appended cleanly:

```text
pre-write lines:          6,853
post-write lines:         7,107
Session-39 header:        line 6,855
header count:             1
header after boundary:    yes
technical diff:           +254 / -0
physical last author:     Codex
old prefix bytes:         605,109
old-prefix SHA-256:       exact match
```

Old-prefix SHA-256:

`52E719C4580851442E87B58A0FF8D5DF26639F54B328528525128966DFB8A38C`

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

## Review-cycle next actions

1. Read any new Claude turn and latest Claude HumanReport before acting.
2. Review Protocol P v2.3 for:
   - an executable typed screen override seam;
   - exact distinction between base and realized pair identities;
   - correct `_dataset0` behavior or a tested suffix-free alternative;
   - honest manifest-leak guards;
   - base-config, assignment, protocol-spec, and per-run override provenance;
   - hash-checked retained local replay references and one-row wording;
   - probe-start origin retained with unmatched-row numeric scope;
   - conditional-only gauge-null interpretation;
   - no unsupported replay-based defect localization;
   - explicit non-optimizable fail-loud checks; and
   - all v2.2 safe branches, quantile, CRN, role, OOD, ordinary-row,
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

Codex Session 40 requires the regular progress report after its normal work.

## Non-negotiable boundaries

- Development mechanics/screens are not confirmatory results.
- One exact row is not whole-dataset reproduction.
- A base reservation id is not the realized RNG pair id.
- Do not mutate the approved assignment without explicit hashed provenance.
- Do not run Protocol P before its exact proposal and implementation are
  approved.
- Do not use `cmd.exe` caret continuations in a PowerShell runbook.
- Do not let permissive shape coercion or optimizable assertions become gates.
- Do not classify failures of unmeasured candidates as contradictions.
- Do not claim one replay localizes a later override-path defect.
- Do not call fixed-fault unmatched sensitivities empirical bounds.
- Do not claim unmatched divergence cancels across different time windows.
- Do not call a conditional gauge-null redraw a causal Case-C classifier.
- Do not choose the harmonic window from response magnitude.
- Do not carry a probe forward after a branch declares it unsafe.
- Do not convert `unsafe_at_severity` into sub-threshold or Case C.
- Do not leave a decision-bearing finite-sample quantile implicit.
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
