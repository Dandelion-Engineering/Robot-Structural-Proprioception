# Summary of Only Necessary Context — Codex

**Last completed Codex session:** 41

**Date:** 2026-07-29

**Current phase:** Phase 2 — Integration and Reproducibility Build

**Primary active thread:** `chats/Claude-Codex/Phase 2 Integration and Config
Freeze/Phase 2 Integration and Config Freeze - Active.md`

## Resume here

Protocol P remains unrun and blocked:

```text
BLOCK_PROTOCOL_P_V2_3_1_PENDING_BINARY_HASH_DOMAIN_AND_COMPLETE_EXECUTION_PINS
BLOCK_CONFIG_FREEZE_PENDING_PRECONFIRMATORY_BUILD_AND_VALIDATION
```

Claude Session 41 verified and corrected Codex Session 40's exact onset,
provenance, protocol-spec, and assignment-text portability findings. The
corrected proposal now lives in a tracked artifact:

```text
Reproducibility Packet/protocol/protocol-p-v2.3.1.md
canonical SHA-256:
  8c268f8f5777923e661cb44c0b6d68991bdf41bf5080ea3e229e4c101d401d76
bytes:
  29,250
line endings:
  LF
owner approval:
  explicit, Claude Session 41
reviewer approval:
  withheld, Codex Session 41
```

Codex Session 41 reviewed that exact file and preserved the scientific,
selection, branch, role, and interpretation design in substance. Four
file-to-execution contradictions still block the exact state.

Claude owns one narrow correction to the same protocol file. After correcting
it, Claude must explicitly approve the new canonical digest and hand it back.
Do not implement the seam, run the replay, run Stage 0/A/B/C, write Amendment
A2, edit either Claim Sheet, replace the assignment, regenerate data, fit
Gate-4 models, or create final `config.json` before the relevant same-state
reviews close.

## Exact Session-41 corrections required

### 1. Separate canonical text hashing from exact binary hashing

The current protocol defines a helper that:

```python
raw = Path(path).read_bytes()
if raw.startswith(b"\xef\xbb\xbf"):
    raw = raw[3:]
hashlib.sha256(raw.replace(b"\r\n", b"\n")).hexdigest()
```

This is correct only for canonical UTF-8 text. Section 7 incorrectly applies it
to the binary `.npz` replay references.

Measured exact state:

```text
plant reference:
  path:
    data/gate3-base-dev-pilot-val-c1-s/plant/
    scenario_dev_t01_f000_r00_S_dataset0.npz
  bytes:
    3,176,122
  embedded CRLF-valued byte pairs:
    18
  raw SHA-256:
    ed5b1f39f4ba535c60eb3e1b8587c7b03f59a5c3f9c1189b55635f0d49b65e45
  text-folded SHA-256:
    638e384f3a75c4cefb360e7b7815e7a1b9f5dcd2e01c2cbb718410db9964c575

S observation reference:
  path:
    data/gate3-base-dev-pilot-val-c1-s/observations/S/
    scenario_dev_t01_f000_r00_S_dataset0.npz
  bytes:
    929,068
  embedded CRLF-valued byte pairs:
    1
  raw SHA-256:
    cdde17f6d32c5d648249f4a9b343ec3f997b04c83cadacbf9d2c5f1186bb4c83
  text-folded SHA-256:
    0051ea132a783264c47a370184f0d328e2ae4c3a95ad227b3cf9c181c599435e
```

Required domains:

```text
canonical_text_sha256:
  protocol-p-v2.3.1.md
  proposed-gate3-assignment-v0.1.json
  UTF-8 BOM strip + CRLF-to-LF fold

raw_file_sha256:
  both retained .npz replay references
  hashlib.sha256(path.read_bytes()).hexdigest()
  no transformation
```

Rewrite I1 so canonical text bytes and exact binary bytes are distinct.

The `.gitattributes` rules are correct defence in depth:

```text
Reproducibility?Packet/config/proposed-gate3-assignment-v0.1.json text eol=lf
Reproducibility?Packet/protocol/*.md text eol=lf
```

They do not apply to ignored binary replay payloads.

### 2. Eliminate the ambiguous `M2` symbol

The standalone protocol currently says:

```text
M2 is Stage 0's first real-plant corroboration
all ten have safe valid M2 verdicts
the same narrowing applies to M2
```

The transcript used “Measurement 2” for a descriptive fixed-trace
gauge-only check and earlier used `M2` for the operative
`D(v,c) >= 2*Q95_c` rule. Those are different:

```text
Q95_c^gauge:
  fixed-trace conditional diagnostic
  zero authority

Q95_c:
  full Stage-C within-cell healthy null
  controls the mechanics verdict
```

Remove the abbreviation. Use direct phrases such as:

```text
prior fixed-trace gauge-only check
safe, valid Stage-C per-cell mechanics verdicts
operative D(v,c) >= 2*Q95_c rule
```

Do not let `Q95_c^gauge` enter any threshold, case, or branch.

### 3. Define three provenance scopes

The all-None replay cannot carry Protocol-P provenance and reproduce the
retained base row. Stage 0 writes an artifact but has no rollout reservation.
State each scope separately:

```text
replay gate:
  overrides=None
  stamps base config hash
  ephemeral
  never persists a screen artifact

Stage A/B/C:
  active overrides
  each rollout stamps a base-distinct dev-<64 lowercase hex>
  records the strict canonical provenance string

Stage 0:
  no plant, rollout, cell, condition, overrides, or reservation
  sensor_only_difference_null.json receives one artifact-level
  dev-<64 lowercase hex>
```

The Stage-0 artifact payload must bind:

```text
base config hash
assignment canonical text SHA-256
assignment_hash
protocol-spec SHA-256
stage = "0"
exact canonical CLI inputs
output schema identity
```

Use strict canonical JSON:

```python
json.dumps(
    payload,
    ensure_ascii=False,
    sort_keys=True,
    separators=(",", ":"),
    allow_nan=False,
)
```

Do not invent a fake plant reservation for Stage 0.

### 4. Make I13 a full runtime construction check plus a separate test

The current helper treats every non-`"healthy"` string as structural and
silently ignores severity on the healthy branch. The runtime invariant must
reject unknown conditions and compare the complete actual construction to the
requested condition.

Exact expected constructions:

```text
healthy:
  severity absent
  physical_faults == ()

structural remaining-EI v:
  exactly one FaultSpec
  source_class == "structure"
  subtype == "link_stiffness_loss"
  location == 1
  severity == float(v)
  onset_index == _step_index(trajectory onset, control_dt)
  compound_flag == False
  ood_flag == False
```

The production check raises `ProtocolPError` before each plant-bearing rollout.
It is the runtime construction precondition before any Stage-A failure can be
called a physical safety/method limit.

Separately, the implementation tests must prove the Protocol-P construction:

```text
fault onset_index:
  500
CablePlant softened state:
  inactive through step 499
  active at step 500
healthy:
  active override with ()
  faultless
```

`_generate_reservation` returns a completed `PrivilegedRecord`, not the plant's
historical `_softened` state. Do not describe the 499/500 behavioural test as a
per-rollout runtime invariant. The physical-limit interpretation requires the
runtime full-object check and the approved implementation-test state.

### 5. Correct the implementation-review order sentence

The protocol currently says the diff is posted before it is applied. The
agreed order is:

```text
same-state protocol approval
-> Claude applies the verified seam
-> Claude posts the exact working-tree diff and focused tests
-> Codex reviews the implementation
-> implementation approval
-> one-row replay gate
-> Stage 0/A/B/C
```

Claude keeps implementation ownership. Codex reviews; Codex does not need to
take over the seam patch.

## Session-41 corrections already accepted

Do not redesign these.

### Fault onset and healthy tuple

The direct v2.3 structural object omitted `onset_index`, so:

```text
FaultSpec.onset_index default:
  -1
CablePlant effective onset:
  max(-1, 0) = 0
declared dev t01 onset:
  1.0 s / 0.002 s = step 500
```

v2.3.1 now requires:

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

Every override guard tests `is not None`, never truthiness. The empty tuple is
falsy but is an active override.

Claude Session 41 measured four onset-consequence rollouts outside the
Protocol-P identity band:

```text
remEI 0.75  step 0    gauge 5.76 ue  qd 0.686  q 0.396  flags 0  sat 0  ADMISSIBLE
remEI 0.75  step 500  gauge 5.56 ue  qd 0.773  q 0.396  flags 0  sat 0  ADMISSIBLE
remEI 0.35  step 0    gauge 5.58 ue  qd 0.752  q 0.396  flags 0  sat 0  ADMISSIBLE
remEI 0.35  step 500  gauge 5.59 ue  qd 0.720  q 0.396  flags 0  sat 0  ADMISSIBLE
```

The gates would not detect the wrong onset. Their large safety margin is
evidence about safety, not construction.

### Lifecycle-valid active provenance

Active plant-bearing override provenance must be:

```text
exactly dev-<64 lowercase hex>
different from the supplied base config hash
validated inside _generate_reservation
recomputed by the caller from the strict canonical object
```

Claude's tested example:

```text
dev-f8dfe2f7a86bcb98f19fd68eda332050405da37b445be46c17d37c5062ae4da5
```

The old `dev-protocolp-v2.3-<32 hex>` form is invalid and retired.

### Portable text identities

The exact assignment identity remains:

```text
assignment_hash:
  dev-eec59ec8a296a9a4ff4909f8e7f1de91a0a8f4bf289ae1533a427d1a87bc33f1
canonical text SHA-256:
  76255a8089f3e27d893b26d981cbf50e808bd75ba518c44b55c4635ec83514ae
CRLF raw rendering SHA-256:
  00dacaf6277d6b274e3690ab3d3f68607eb61a22fe0df75ea8688fe4c7d4f87f
```

The protocol-spec hash binds the entire operative tracked file, not a
transcript block. The file cannot contain its own digest; the implementation
computes it at runtime.

### Label-stamp boundary

The physical override leaves the returned label describing the healthy source
reservation. This remains non-blocking for Protocol P only if:

- no screen `ObservedRecord`, label payload, manifest, or role index is
  persisted;
- every result is keyed from the explicit Protocol-P condition, never the
  returned assignment label; and
- focused tests prove the results-only path writes no dataset-role artifact.

The seam is screen-only. Any future persisted override consumer must repair
the label and identity first.

## Protocol P scientific and selection state approved in substance

The following remains settled:

- development diagnostic trajectory `trajectory_dev_diagnostic_b` only;
- context cells 4/5/6/7;
- generator-authoritative construction through a typed screen-only seam;
- C0-driven loop with post-hoc S at the same realized identity;
- no online-S construction;
- suffix-free screen-private realized pair ids;
- matched `(sensor_seed, realized_pair_id)` in Stage A/B;
- base reservation copied from the cell's healthy dev t01 reservation, changing
  only `sensor_seed` and `base_pair_id`;
- config-derived probe-start window `[1000,1768)`;
- exact measurement-time rank/width/length validation;
- observed `gauge_obs`, `gauge_valid`, measurement time, and 0.8-Hz reduction;
- vector-8 statistic over all four gauges;
- one-row exact replay gate with local retained references;
- 24 declared candidates, 15 torque-excluded, nine simulated;
- Stage-A maximum 108 rollouts;
- Stage-A selection by worst-cell remEI 0.75 `D`, without T1;
- terminal `NO_ADMISSIBLE_PROBE`;
- ten-value remaining-EI ladder;
- terminal `UNSAFE_LADDER_VALUE`;
- Cases A/B/C only after all ten values have safe valid Stage-C verdicts;
- eight healthy Stage-C runs per cell;
- `np.quantile(..., 0.95, method="higher")`;
- operative rule `D(v,c) >= 2*Q95_c` in every cell;
- stricter scalar rule only as a sensitivity;
- numeric Q95 tripwire only as a diagnostic pause;
- fixed-trace gauge redraw only as a conditional diagnostic;
- dependent unmatched distances only as descriptive sensitivity;
- ordinary structural rows retained in the primary estimand without a claimed
  direction;
- OOD rows excluded from known-class macro-F1 and role coverage;
- exact test contact `[1.8,3.3]`;
- preserved severity-to-role allocation;
- known-class role-coverage rule;
- measured thermal near-invariance and first-order mechanism;
- unchanged success bar; and
- maximum nonterminal cost `1 + 108 + 32 + 28 = 169` rollouts.

## Realized screen identities retained

```text
P_SEED_BASE = 150000
cell c in {4,5,6,7}
r = c - 4

Stage A/B:
  sensor_seed = 150000 + 10*r + 2
  pair_id     = basepair_protocolp_stageAB_c{c}

Stage C k=0:
  exact selected Stage-A healthy identity

Stage C k>=1:
  sensor_seed = 150000 + 10*r + 1000*k + 2
  pair_id     = basepair_protocolp_stageC_c{c}_k{k}

Stage 0:
  pair_id = 1
  sensor_seed = 0..199
```

The realized screen band `[150002,157032]` is disjoint from dev and pilot.
`ScenarioReservation.base_pair_id` and realized `pair_id` are different
objects.

## Role and data state

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
  complete at the current pre-A2 assignment
  any A2 replacement requires a new exact assignment/review loop

Gate 4:
  blocked on corrected Protocol P, reviewed seam implementation,
  replay, development-only Protocol-P run, and written Amendment A2

Gates 5-7:
  open

Reproducibility Packet/config.json:
  absent

confirmatory test identities/payloads:
  0 / 0

research result:
  none
```

Exact pre-A2 authorities:

```text
approved Gate-3 assignment:
  dev-eec59ec8a296a9a4ff4909f8e7f1de91a0a8f4bf289ae1533a427d1a87bc33f1

bound draft config:
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
silently reuse it under a changed config. If Amendment A2 and a replacement
assignment later receive joint approval, the selected policy remains full
regeneration from zero.

## Current evidence boundary

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
pilot/validation result, or confirmatory evidence.

Delivered structural differences use unmatched control identities and the old
analysis used mixed post-onset windows. Protocol P prospectively repairs those
issues; it does not rewrite prior evidence.

## Forward corrections that must not be lost

`HumanReport33.md` has an incorrect first row. Future reporting uses:

```text
0.90 | 0.0544 microstrain | 0.13x | validation
```

`HumanReport36.md` calls `0.4388` the vector-8 five-sigma threshold. It is a
single-window norm threshold, not the difference statistic. T1 is retired.

Claude Session 38's empirical peak is:

```text
1208 / 2.092897106 / 11.2897%
```

Claude Session 39's “whole dataset rebuilds” public headline is corrected
forward: one retained development row replayed exactly.

Finding J's 2.37-3.64x values are total unmatched-row different-window ratios,
not clean fault-effect multipliers.

## Verification baseline

Use the repository venv:

```powershell
.\venv\Scripts\python.exe -m pytest -q "Reproducibility Packet\tests"
```

Codex Session 41:

```text
399 passed in 10.05 s
```

Do not use root-wide `pytest -q`; ignored duplicate test trees under `tmp/` can
pollute collection.

Session 41 changed no packet source, protocol, config, schema, assignment,
result, or test. It generated no Protocol-P identity, computed no Protocol-P
statistic, and ran no rollout.

## Transcript-order state

Codex Session 41 appended cleanly:

```text
pre-write lines:
  8,235
pre-write bytes:
  667,359
pre-write SHA-256:
  5C459A638429C30318907DD4E58D3263A36296E223B8D720AAB72660D7F59A3E
post-write lines:
  8,450
Session-41 header:
  line 8,239
header count:
  1
old prefix:
  byte-identical
technical diff:
  +215 / -0
physical last author:
  Codex
```

No monitoring-thread update was needed.

For every future transcript append:

1. read the UTF-8 physical tail;
2. record pre-write line count, byte count, and SHA-256;
3. verify the complete actual EOF anchor is unique;
4. use that complete anchor in the patch;
5. prove the new header occurs exactly once after the old line boundary;
6. hash the old byte prefix through its former final newline;
7. re-read the physical tail; and
8. require `+N / -0`.

## Review-cycle next actions

1. Read Claude's exact corrected protocol artifact and matching HumanReport.
2. Recompute its canonical digest and require Claude's explicit owner approval
   to name that same digest.
3. Review only the Session-41 correction delta plus retained v2.3.1 state.
4. If correct, explicitly approve the same digest and close the protocol loop.
5. Then let Claude apply the verified generator seam.
6. Review the exact implementation diff and focused tests:
   - default path unchanged;
   - healthy empty override is active and faultless;
   - full structural `FaultSpec` matches the condition;
   - onset step 500, not 0;
   - plant inactive at 499 and active at 500;
   - active provenance valid/base-distinct;
   - Stage-0 artifact provenance exact;
   - text and binary hash domains distinct;
   - no dataset-role artifact written.
7. Only after implementation approval run the one-row replay gate.
8. Only after a passing replay may development-only Stage 0/A/B/C run.
9. Review the exact result and selected terminal/nonterminal branch.
10. Only then review written Amendment A2, synchronized Claim Sheets,
    manifest/exclusions, packet amendment, and replacement assignment.
11. Only after same-state amendment/assignment approval may the selected branch
    regenerate non-test data from zero.
12. Resume Gate 4 only if the amended development feasibility gate clears.
13. Keep `config.json` absent and test identities/payloads at zero until Gates
    2-7 close.

The next regular Codex progress report is due at Session 48 unless an approved
amendment or phase transition triggers one earlier.

## Non-negotiable boundaries

- Development mechanics/screens are not confirmatory results.
- One exact row is not whole-dataset reproduction.
- Text canonicalization must never alter a binary payload before exact hashing.
- A symbol with two historical meanings is not an executable standalone pin.
- A no-override replay is not an active-override screen artifact.
- A no-plant Stage-0 artifact must not invent a fake reservation.
- Provenance recording does not replace expected/actual equality checks.
- A typed `FaultSpec` must match the requested condition in every field.
- A runtime construction invariant and a plant-behaviour test are different.
- An all-None replay does not validate a new override branch.
- A nonempty provenance string is not proof of a lifecycle-valid,
  base-distinct identity.
- Hash-bound text artifacts require byte-stability controls.
- A base reservation id is not the realized RNG pair id.
- Do not mutate the approved assignment without explicit hashed provenance.
- Do not run Protocol P before proposal and implementation approval.
- Do not persist an overridden record with a stale assignment label.
- Do not use cmd.exe caret continuations in a PowerShell runbook.
- Do not let permissive coercion or optimizable assertions become gates.
- Do not classify failures of unmeasured candidates as contradictions.
- Do not claim one replay localizes a later override-path defect.
- Do not call fixed-fault unmatched sensitivities empirical bounds.
- Do not claim unmatched divergence cancels across windows.
- Do not call a conditional gauge-null redraw a causal mechanism classifier.
- Do not choose the harmonic window from response magnitude.
- Do not carry a probe after a branch declares it unsafe.
- Do not convert `unsafe_at_severity` into sub-threshold or Case C.
- Do not leave a finite-sample quantile implicit.
- Do not treat a numeric null tripwire as proof of unique identities.
- Do not infer unmeasured ladder values or assume monotonicity.
- Do not use pooled Q95 as the context-robust operative null.
- Do not rebalance severities after development evidence.
- Do not let pilot outcomes retroactively define confirmatory membership.
- Do not move OOD rows into known-class macro-F1 or role coverage.
- Do not inspect non-development outcomes to choose the amended design.
- Do not materialize confirmatory identities or payloads before final freeze.
- Reviewer edits, handoffs, downstream use, or silence are not approval.
- Keep detection, attribution, information/action authorization, and control
  outcome separate.
- Keep `config.json` absent until all remaining gates close.
