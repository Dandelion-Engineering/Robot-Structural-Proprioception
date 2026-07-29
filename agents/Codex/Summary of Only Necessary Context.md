# Summary of Only Necessary Context — Codex

**Last completed Codex session:** 40

**Date:** 2026-07-29

**Current phase:** Phase 2 — Integration and Reproducibility Build

**Primary active thread:** `chats/Claude-Codex/Phase 2 Integration and Config
Freeze/Phase 2 Integration and Config Freeze - Active.md`

## Resume here

Protocol P remains text-only and blocked:

```text
BLOCK_PROTOCOL_P_V2_3_PENDING_EXACT_FAULT_ONSET_AND_LIFECYCLE_VALID_PROVENANCE
BLOCK_CONFIG_FREEZE_PENDING_PRECONFIRMATORY_BUILD_AND_VALIDATION
```

Claude Session 40 posted Protocol P v2.3. Codex Session 40 approved its
scientific, selection, identity, replay-scope, null, branch, role, OOD,
contact, torque, and interpretation design in substance. Two exact
construction defects still prohibit applying the seam:

1. the direct structural `FaultSpec` omits `onset_index`, so the dataclass
   default `-1` is clamped by `CablePlant` to effective activation step 0
   instead of the dev diagnostic trajectory's declared step 500; and
2. the provenance seam accepts any nonempty string, including the base config
   hash, while the proposed `dev-protocolp-v2.3-<32 hex>` value is not the
   packet's lifecycle-valid `dev-<64 hex>` form.

Claude owns one narrow append-only v2.3 correction, not a fifth full rewrite.
Do not implement or run Protocol P, write Amendment A2, edit either Claim
Sheet, build a replacement assignment, regenerate data, fit Gate-4 models, or
create final `config.json` before that exact correction receives same-state
approval.

## Exact Session-40 correction required

### Fault construction

The inherited direct object is currently equivalent to:

```python
FaultSpec(
    source_class="structure",
    subtype="link_stiffness_loss",
    location=1,
    severity=v,
)
```

That means:

```text
FaultSpec.onset_index = -1
CablePlant effective onset = max(-1, 0) = 0
```

The corrected construction must be exact:

```python
onset_index = _step_index(
    float(trajectory["onset_time_s"]),
    runtime.control_dt_s,
)

physical_faults = (
    ()
    if condition == "healthy"
    else (
        FaultSpec(
            source_class="structure",
            subtype="link_stiffness_loss",
            location=1,
            severity=float(v),
            onset_index=onset_index,
            compound_flag=False,
            ood_flag=False,
        ),
    )
)
```

For the dev Protocol-P universe:

```text
trajectory:       trajectory_dev_diagnostic_b
onset_time_s:     1.0
control_dt_s:     0.002
onset_index:      500
probe start:      step 1000
analysis window:  [1000,1768)
```

The implementation tests must prove the override activates at step 500, not
step 0. The all-None replay remains necessary but does not exercise this
branch.

### Provenance enforcement

The seam must enforce:

```text
active provenance is exactly dev-<64 lowercase hex>
active provenance differs from the supplied base config hash
the caller recomputes the identity from the exact canonical provenance object
```

Use the full digest:

```python
screen_provenance_hash = (
    "dev-" + hashlib.sha256(canonical_json.encode("utf-8")).hexdigest()
)
```

Reject malformed or base-equal active provenance inside
`_generate_reservation`, not only in the Protocol-P calling script.

The canonical provenance object retains:

```text
base config hash
approved assignment identity
complete protocol-spec identity
stage
cell
condition
exact peak / ramp / structural severity / realized-pair override
source and screen reservation identity
```

`protocol_spec_sha256` must bind one tracked canonical artifact containing the
complete operative state, including the seam, replay, gauge-only diagnostic,
branch, and interpretation pins that the compact Protocol-P block references.
“Hash of this block” is not enough without exact byte boundaries and would omit
referenced sections.

The raw assignment file currently hashes to:

```text
LF bytes:
  76255a8089f3e27d893b26d981cbf50e808bd75ba518c44b55c4635ec83514ae
same parsed text rendered CRLF:
  00dacaf6277d6b274e3690ab3d3f68607eb61a22fe0df75ea8688fe4c7d4f87f
```

The file has no `eol=lf` attribute while Windows Git has
`core.autocrlf=true`. Either pin this hash-bound file to LF before relying on
raw bytes or replace the raw-file field with the canonical assignment-byte
hash.

### Label-stamp boundary

The physical override leaves `_generate_reservation`'s returned label payload
describing the healthy source reservation. This is non-blocking for Protocol P
only if the implementation:

- persists no screen `ObservedRecord`, label payload, manifest, or role index;
- keys all results from the explicit Protocol-P condition rather than the
  returned assignment label; and
- tests that the results-only path writes no dataset-role artifact.

The seam remains screen-only. Any future consumer that persists an overridden
record must repair the label and run identity first.

## Protocol P v2.3 content approved in substance

The following should not be redesigned in the narrow correction:

- development diagnostic trajectory only for Protocol P;
- balanced development context cells 4/5/6/7;
- generator-authoritative construction with a typed screen-only override seam;
- C0-driven loop and post-hoc S observation at the same realized identity;
- no online-S construction;
- suffix-free screen-private realized `pair_id`;
- matched `(sensor_seed, realized_pair_id)` in Stage A/B;
- base reservation copied from the cell's healthy dev `t01` reservation, with
  only `sensor_seed` and `base_pair_id` changed;
- config-derived `[w0:w1]` probe-start slice;
- exact measurement-time rank/width/length validation;
- observed `gauge_obs`, `gauge_valid`, measurement time, and 0.8-Hz reduction;
- vector-8 over all four gauges;
- one-row replay gate with pinned local hashes and exact one-row wording;
- 24 declared probe candidates, 15 deterministically excluded by the inclusive
  torque rule, and nine simulated candidates;
- 108-rollout Stage-A maximum;
- Stage-A selection without a sensor-only T1 cutoff;
- safe terminal `NO_ADMISSIBLE_PROBE`;
- ten-value remaining-EI ladder;
- separate terminal `UNSAFE_LADDER_VALUE`;
- Cases A/B/C only after all ten values have safe, valid mechanics verdicts;
- eight healthy Stage-C runs per cell;
- `np.quantile(..., 0.95, method="higher")`;
- operative rule `D(v,c) >= 2 * Q95_c` in every cell;
- stricter scalar rule as a sensitivity only;
- Q95 numeric tripwire as a diagnostic pause only;
- fixed-trace gauge redraw as a conditional descriptive diagnostic only;
- dependent fixed-fault unmatched distances at descriptive scope only;
- ordinary structural rows retained in the primary estimand without a claimed
  direction;
- OOD rows outside known-class macro-F1 and role coverage;
- exact test contact `[1.8,3.3]`;
- preserved severity-to-role allocation;
- known-class role-coverage rule;
- measured thermal near-invariance plus first-order mechanism;
- unchanged success bar; and
- nonterminal cost `1 + 108 + 32 + 28 = 169` rollouts.

## Realized screen identities retained

```text
P_SEED_BASE = 150000
cell c in {4,5,6,7}
r = c - 4

Stage A/B:
  sensor_seed = 150000 + 10*r + 2
  pair_id     = basepair_protocolp_stageAB_c{c}

Stage C k=0:
  exact reuse of selected Stage-A healthy identity

Stage C k>=1:
  sensor_seed = 150000 + 10*r + 1000*k + 2
  pair_id     = basepair_protocolp_stageC_c{c}_k{k}

Stage 0:
  pair_id = 1
  sensor_seed = 0..199
```

The realized band `[150002,157032]` is disjoint from dev and pilot. Under the
normal generator path, `ScenarioReservation.base_pair_id` and realized
`pair_id` remain different objects because `_dataset0` is appended.

## One-row replay scope

Codex and Claude independently replayed:

```text
scenario_dev_t01_f000_r00
```

through the current bound draft config, approved assignment, and default
generator path.

Codex Session 39:

```text
elapsed:              26.971 s
privileged fields:    20 / 20 byte-identical
S npz entries:        38 / 38 byte-identical
safety events:        0
contact steps:        0
```

The retained local references are:

```text
plant:
  data/gate3-base-dev-pilot-val-c1-s/plant/
  scenario_dev_t01_f000_r00_S_dataset0.npz
  ed5b1f39f4ba535c60eb3e1b8587c7b03f59a5c3f9c1189b55635f0d49b65e45

S observation:
  data/gate3-base-dev-pilot-val-c1-s/observations/S/
  scenario_dev_t01_f000_r00_S_dataset0.npz
  cdde17f6d32c5d648249f4a9b343ec3f997b04c83cadacbf9d2c5f1186bb4c83
```

The reference is ignored local development data, not a committed payload.
This proves one retained row, not all 472 reservations, and validates only the
all-None/default path.

## Finding-J and null interpretation retained

The probe-start origin remains approved because it is config-derived, fixed
before response, and contains the declared burst:

```text
w0 = round((onset_time_s + diagnostic_probe.start_offset_s) / control_dt_s)
```

The measured 2.37–3.64× number is only the ratio of total unmatched-row
four-gauge 0.8-Hz differences across two different windows. It is not a clean
fault-effect multiplier; unmatched closed-loop divergence need not cancel
across different time samples and the norm is nonlinear.

The rejected response-selected alternative remains:

```text
step 1208: ||b|| = 2.092897106
step 1000: ||b|| = 1.880585474
gain:      11.2897%
```

Keep step 1000.

The fixed-trace `Q95_c^gauge` secondary may report whether and how much the
full healthy null exceeds the redraw term for one fixed trace. It has zero
authority over selection, thresholds, or verdicts and cannot uniquely classify
a Case-C mechanism.

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
conditions = healthy, remEI 0.75, remEI 0.50
```

Classifier:

```text
0.05 N / ramp 0.5 fails healthy or remEI 0.75:
  implementation-integrity contradiction requiring diagnosis

that candidate passes those conditions but fails remEI 0.35:
  newly observed physical safety/method limit

other candidates' failures:
  record normally
  do not classify prior evidence
```

The replay gate does not localize a later override-path defect.

### UNSAFE_LADDER_VALUE

`unsafe_at_severity` is neither `TESTABLE` nor `SUB-THRESHOLD`. If any ladder
value is unsafe, the branch is terminal, config remains unfrozen, and Cases
A/B/C are unavailable.

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

Count 1 is a thin role but creates no new terminal branch.

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
  blocked on corrected Protocol P v2.3, separately reviewed implementation,
  and later written Amendment A2

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

Do not call this project-hypothesis failure, a whole-band negative, a
pilot/validation confirmation, or proof that fault and healthy distributions
are indistinguishable.

Delivered structural differences are confounded by unmatched control
identities, and the old analysis used mixed post-onset windows. Protocol P
prospectively fixes those issues; it does not rewrite the earlier evidence.

## Forward corrections that must not be lost

`HumanReport33.md` contains an incorrect first row in its measured severity
table. Future reporting must use:

```text
0.90 | 0.0544 microstrain | 0.13x | validation
```

not `0.95 | 0.0090 | 0.02x | development`.

`HumanReport36.md` calls `0.4388` the coherent vector-8 five-sigma threshold.
It is a single-window norm threshold, not the difference statistic. T1 is
retired.

Claude Session 38's empirical-peak location is corrected to:

```text
1208 / 2.0929 / 11.2897%
```

Claude Session 39's “whole dataset rebuilds” public headline is corrected
forward: one retained development row replayed exactly.

Finding J's 2.37–3.64× values must remain labeled total unmatched-row
different-window ratios, not clean fault-signal multipliers.

## Verification baseline

Use the repository venv, never bare system Python:

```powershell
.\venv\Scripts\python.exe -m pytest -q "Reproducibility Packet\tests"
```

Codex Session 40:

```text
399 passed in 11.00s
```

Do not use root-wide `pytest -q`; ignored duplicate test trees under `tmp/` can
pollute collection.

Codex Session 40 opened no development/pilot/validation/test payload content,
generated no Protocol-P identity, computed no Protocol-P statistic, and
changed no packet source or config.

## Transcript-order state

Codex Session 40 appended cleanly:

```text
pre-write lines:          7,769
pre-write bytes:          645,984
post-write lines:         7,951
Session-40 header:        line 7,771
header count:             1
header after boundary:    yes
technical diff:           +182 / -0
physical last author:     Codex
old-prefix SHA-256:       exact match
```

Old-prefix SHA-256:

`CD944A35D1714EB3192D70AC31B2ADEA79A562458F94CC8E56755CC39AB7B6A7`

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

1. Read any new Claude turn and matching HumanReport before acting.
2. Require one narrow correction, explicitly approved by Claude, covering:
   - structural onset step 500;
   - healthy empty physical-fault tuple;
   - full lifecycle-valid base-distinct provenance;
   - complete canonical protocol-spec identity;
   - portable/canonical assignment byte identity; and
   - results-only/no-label-persistence enforcement.
3. Re-review only that exact delta plus retained v2.3 state.
4. Only after exact proposal approval may Claude apply the seam.
5. Review the implementation diff and branch-specific tests before any run.
6. Only after implementation approval may the one-row replay gate run.
7. After a passing replay, Protocol P may run development-only.
8. Review the exact result and selected branch before written amendment work.
9. Then review synchronized Claim Sheet, Accessible Claim Sheet,
   manifest/exclusion, packet amendment, and replacement assignment.
10. Only after written amendment and assignment same-state approval may the
    selected branch regenerate the non-test study from zero.
11. Resume Gate 4 only after the amended development feasibility gate clears.
12. Keep `config.json` absent and test identities/payloads at zero until Gates
    2–7 close.

The regular Codex Session-40 progress report is complete. The next regular
report is due at Codex Session 48 unless a phase transition or approved
amendment triggers an extra report.

## Non-negotiable boundaries

- Development mechanics/screens are not confirmatory results.
- One exact row is not whole-dataset reproduction.
- An all-None replay does not validate a new override branch.
- A typed `FaultSpec` without the correct onset is not the approved fault.
- A nonempty provenance string is not proof of a base-distinct identity.
- Hash-bound raw files require byte-stable line-ending policy.
- A base reservation id is not the realized RNG pair id.
- Do not mutate the approved assignment without explicit hashed provenance.
- Do not run Protocol P before its exact proposal and implementation are
  separately approved.
- Do not persist an overridden record with a stale assignment label.
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
