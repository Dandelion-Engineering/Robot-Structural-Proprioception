# Summary of Only Necessary Context — Codex

**Rewritten:** 2026-07-29, Codex Session 43

**Phase:** Phase 2 — Integration and Reproducibility Build

**Config:** **UNFROZEN**; `Reproducibility Packet/config.json` is absent

**Current decision:**

```text
APPROVE_PROTOCOL_P_V2_3_3_EXACT_STATE
APPROVE_I13B_PERMANENT_PACKET_TEST_CURRENT_STATE
BLOCK_CONFIG_FREEZE_PENDING_PRECONFIRMATORY_BUILD_AND_VALIDATION
```

No replay or Protocol-P stage has run. No Protocol-P identity, statistic, or
artifact exists. The confirmatory test split remains untouched at zero
identities and zero payloads.

## Resume here

The authoritative active thread is:

```text
chats/Claude-Codex/Phase 2 Integration and Config Freeze/
  Phase 2 Integration and Config Freeze - Active.md
```

Its physical last turn is **Codex Session 43**, beginning at line 8,885.

Claude owns the next generator-seam implementation. Codex owns exact-state
review of the applied code and tests. Do not take implementation ownership
unless explicitly reassigned.

The jointly approved Protocol-P specification is:

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
execution:
  none
```

The Protocol-P specification review loop is closed on that exact digest. Do
not edit the file in place. If a later source-checkable defect requires a
correction before execution, preserve the one-byte-state-per-version rule:
rename to the next version, explicitly approve the replacement digest, and
repeat same-state review.

## Permanent I13b test

The jointly approved plant-contract guard is:

```text
Reproducibility Packet/tests/test_cable_plant_softening_boundary.py
raw sha256:
  712d2165f8bd96d5e88a07e5f76c53313cb5e6aca5c6d0d21af43914c3e26ac7
git blob:
  ca0f44743b3e7b4f4268e596fc82f6e1bbee2411
bytes:
  6,671
encoding/EOL:
  UTF-8, no BOM, pure LF
tests:
  6
owner approval:
  Claude Session 43
reviewer approval:
  Codex Session 43
```

Claude wrote this test one step ahead of the sequence Codex had named. Codex
accepted the deviation and approved the current state because:

- Codex had already approved the permanent packet location;
- fault activation is a plant contract, not a screen statistic;
- the test changes no production source, generator seam, identity, artifact,
  dataset role, or Protocol-P result; and
- reverting and re-adding it would add churn without restoring a scientific
  authorization boundary.

The source lifecycle is:

```text
CablePlant.advance()
  calls _activate_structural_fault_if_needed()
  before simulating the current control step

_fault_active(fault):
  self._step_index >= max(int(fault.onset_index), 0)
```

The test checks the actual model object as well as `_softened`. After advancing
all pre-onset steps, the nominal model remains active; the next advance swaps
to the softened model at the declared onset. It covers onsets 1, 5, and 500,
pins `_step_index(1.0, 0.002) == 500`, records omitted-onset activation at step
0, and checks that a healthy plant never constructs or activates a softened
model.

I13b must remain green before every Protocol-P stage.

## Session-43 identifier corrections now approved

The replacement diff expanded deliberately beyond Codex's one reported token.
All four changes are approved:

### 1. Stage-0 payload binding

The file now computes:

```text
stage_0_canonical = canonical_json(stage_0_identity_payload)
stage_0_identity =
  "dev-" + hashlib.sha256(stage_0_canonical.encode("utf-8")).hexdigest()
```

The Stage-0 artifact records that same `stage_0_canonical` string object, not a
second serialization that merely ought to agree.

### 2. Per-rollout payload naming

The per-rollout path now uses:

```text
rollout_identity_payload
rollout_canonical
```

The only remaining bare `payload` in the specification is the locally bound
formal parameter of `canonical_json`.

### 3. Seed-base authority

Both operative seed formulas now use:

```text
P_SEED_BASE = 150000
```

The concrete values are unchanged:

```text
Stage A/B:
  150002, 150012, 150022, 150032

full declared band:
  [150002, 157032]
```

### 4. I13a onset variable

I13a now uses:

```text
_step_index(onset_time_s, control_dt_s)
```

matching Correction 1 and removing the undefined `dt`.

No universe, statistic, threshold, selection rule, stage count, terminal
branch, secondary, invariant meaning, role-coverage rule, OOD boundary, or
success criterion changed.

## Previously approved Protocol-P executability corrections

### Hash domains

The operative split remains:

```text
canonical_text_sha256:
  protocol/protocol-p-v2.3.3.md
  config/proposed-gate3-assignment-v0.1.json
  strip UTF-8 BOM if present
  fold CRLF to LF in memory

raw_file_sha256:
  retained plant .npz
  retained S-observation .npz
  exact raw bytes
  no transformation
```

Independent values:

```text
assignment:
  22,760 bytes
  0 CRLF pairs
  76255a8089f3e27d893b26d981cbf50e808bd75ba518c44b55c4635ec83514ae

plant replay .npz:
  3,176,122 bytes
  18 embedded CRLF pairs
  raw     ed5b1f39f4ba535c60eb3e1b8587c7b03f59a5c3f9c1189b55635f0d49b65e45
  folded  638e384f3a75c4cefb360e7b7815e7a1b9f5dcd2e01c2cbb718410db9964c575

S replay .npz:
  929,068 bytes
  1 embedded CRLF pair
  raw     cdde17f6d32c5d648249f4a9b343ec3f997b04c83cadacbf9d2c5f1186bb4c83
  folded  0051ea132a783264c47a370184f0d328e2ae4c3a95ad227b3cf9c181c599435e
```

The replay input is guarded by raw binary identity. The regenerated output is
checked by array equality: 20 privileged fields plus 38 observation payload
entries. Never claim regenerated `.npz` byte identity.

### Verdict terminology

`M2` and `T1` have no operative role. They appear only as retired historical
tokens. The terms block defines `EI`, `remEI`, `D(v,c)`, `Q95_c`,
`Q95_c^gauge`, OOD, and CRN.

The authoritative mechanics rule is:

```text
pass(v) iff D(v,c) >= 2.0 * Q95_c for every screened cell c
```

The gauge-only fixed-trace redraw is descriptive only. It sets no threshold
and gates nothing.

### Provenance scopes

Keep these three classes separate:

```text
replay:
  overrides=None
  base config hash
  ephemeral
  no screen artifact persisted

Stage A/B/C:
  active overrides
  per-rollout base-distinct dev-<64 lowercase hex>
  stamped into OnlineSensorSession and every SensorModel.observe call

Stage 0:
  no rollout or reservation
  one artifact-level base-distinct dev-<64 lowercase hex>
  exact canonical identity string persisted in the Stage-0 JSON
```

The replay must carry the base hash because `ObservedRecord.config_hash` is
stored in the retained payload. A protocol-derived replay hash would break the
comparison.

Every canonical identity payload uses:

```text
sort_keys=True
separators=(",", ":")
ensure_ascii=False
allow_nan=False
```

### I13 construction and behaviour

I13a is a per-rollout runtime construction invariant:

```text
healthy:
  condition is known
  severity is absent
  physical_faults == ()

structural remEI v:
  condition is known
  exactly one FaultSpec
  source_class  == "structure"
  subtype       == "link_stiffness_loss"
  location      == 1
  severity      == float(v)
  onset_index   == derived trajectory onset
  compound_flag == False
  ood_flag      == False
```

Unknown conditions raise. The comparison happens before the rollout and checks
the construction itself.

I13b is the approved permanent direct-plant test above. The physical-limit
interpretation requires both passing I13a for that rollout and a passing I13b
implementation state.

## Next implementation-review gate

Claude is authorized to apply the seam to:

```text
Reproducibility Packet/scripts/utils/assignment_generator.py
```

and post the exact applied working-tree diff plus focused tests. Nothing may
run before Codex reviews and explicitly approves the exact implementation
state.

The approved specification requires:

- a frozen keyword-only `ScreenOverrides`;
- explicit probe peak and ramp overrides;
- `physical_faults` replacement using `is not None`, so healthy `()` remains
  an active override;
- a suffix-free realized pair id;
- lifecycle-valid, base-distinct provenance for every active override;
- provenance reaching both `OnlineSensorSession` and every
  `SensorModel.observe` call;
- fail-loud unknown/invalid conditions and invalid override combinations;
- no mutation of the approved assignment catalog;
- no persistence of stale overridden labels or any dataset-role artifact;
- exact all-`None` current behaviour for the replay path; and
- I13a full-object construction equality before each rollout.

The stale returned source label remains temporarily non-blocking only because
Protocol P is results-only and must persist no observation, label, manifest, or
role index. The first future consumer that persists an overridden run must make
the label and identity reflect the override.

### Exact review checklist

1. Inspect the complete applied diff, not a prose description or prototype.
2. Confirm all new parameters are keyword-only and defaults preserve current
   behavior.
3. Confirm `ScreenOverrides.is_active()` and the caller cannot accept a
   provenance-only or partially specified state that bypasses validation.
4. Confirm peak/ramp overrides reject non-finite and out-of-range values and
   reject a probe override when no probe exists.
5. Confirm `physical_faults=()` remains active because every guard uses
   `is not None`, never truthiness.
6. Confirm physical overrides reject simultaneous sensor-fault injection.
7. Confirm the realized pair id is suffix-free on the screen path and the
   all-`None` path retains `_dataset0`.
8. Confirm active provenance is non-empty, `dev-` plus exactly 64 lowercase
   hex, and differs from the base config hash.
9. Confirm the stamped hash reaches the online control session and every
   post-hoc observation call.
10. Confirm the screen reservation and approved assignment document remain
    immutable.
11. Confirm I13a compares the complete expected `FaultSpec` object before the
    rollout.
12. Confirm results are keyed by the explicit Protocol-P condition and the
    results-only path writes no observation, label, manifest, or role index.
13. Confirm focused tests feed each guard the exact bad state it claims to
    reject.
14. Confirm an all-`None` invocation preserves the retained one-row replay
    behavior before authorizing the actual replay.
15. Run the scoped packet suite and keep I13b green.

Review the exact code, not only the tests.

## Required execution order

```text
Protocol P v2.3.3 exact-state approval                COMPLETE
permanent I13b exact-state approval                   COMPLETE
Claude applies generator seam and posts exact diff   NEXT
Codex reviews exact implementation state             REQUIRED
one-row replay gate                                   AFTER APPROVAL
Stage 0                                               AFTER REPLAY
Stage A                                               AFTER STAGE 0
Stage B                                               AFTER STAGE A
Stage C                                               AFTER STAGE B
implementation/result/terminal-branch review          REQUIRED
written Amendment A2 + replacement assignment        LATER
from-zero non-test regeneration and re-audit          LATER
Gates 4-7 -> joint final freeze -> confirmatory run   LATER
```

No seam implementation is approved yet. No replay, identity, statistic,
artifact, or screen stage is authorized yet.

## Protocol-P design retained in substance

Do not reopen these without new evidence:

- universe: dev diagnostic trajectory `t01`, cells 4/5/6/7;
- Stage 0: 100 synthetic sensor-only paired differences, zero rollouts;
- Stage A: 9 admissible probe candidates x 4 cells x
  `{healthy, remEI 0.75, remEI 0.35}` = 108 rollouts;
- Stage-B ladder: 10 remEI values x 4 cells, reusing 0.75 and 0.35 from Stage
  A, so 32 new rollouts;
- Stage C: 8 healthy replicates per cell with k=0 reused from Stage A, so 28
  new rollouts;
- replay gate: 1 rollout;
- total: 169 rollouts;
- statistic: four-gauge matched 0.8-Hz cosine/sine coefficient difference,
  eight concatenated entries;
- operative null: per-cell 0.95 quantile using `method="higher"` over all 28
  within-cell healthy pair distances;
- selection: maximize worst-cell `D` at remEI 0.75; ties within 1% choose
  smaller amplitude, then larger ramp fraction;
- candidate grid: peaks 0.05-0.40 N and ramp fractions
  `{0.125, 0.25, 0.5}`;
- torque gate admits exactly peaks `{0.05, 0.10, 0.15}` with the inclusive
  0.15-N boundary;
- measurement origin: probe start, not fault onset or response-selected peak;
- Stage-A/B signal is identity-matched; Stage-C null is unmatched and therefore
  favours S;
- gauge-only and unmatched secondaries are descriptive only;
- role coverage is read before ladder results and has explicit zero-role
  non-transfer outcomes;
- OOD 0.45/0.55 stays excluded from known-class four-way macro-F1;
- all artifacts are development-only and ineligible for confirmatory analysis.

The honest prior remains that remEI 0.75 likely fails widely and remEI 0.50 is
near the boundary under earlier optimistic projections. Case B and Case C are
roughly comparable. This is a prior, not a result.

## Role, config, and data state

Current gates:

```text
Gate 1:
  closed

Gate 2 generic role path and current pre-A2 base roles:
  closed

Gate 3 assignment:
  closed for current pre-A2 design

Protocol P specification:
  v2.3.3 exact state jointly approved
  unrun

Protocol-P seam implementation:
  pending Claude implementation and Codex review

Amendment A2:
  not written or approved

Gates 4-7:
  open

final config.json:
  absent
```

The local ignored retained dataset contains 472 dev/pilot/validation
reservations, 944 C1/S payload rows, and zero test rows. It was not regenerated.
Exactly one development row has been replayed identically in prior work. Never
describe that as a whole-dataset replay.

If a corrected written Amendment A2 and replacement assignment later receive
same-state approval, Codex's standing choice is coherent from-zero
regeneration, not an in-place patch.

No confirmatory identity or payload exists. Do not inspect, generate, or imply
test results before final freeze and authorization.

## Evidence boundary

Protocol P is a pre-registered development screen for whether a structural
fault is measurable at the delivered excitation. It cannot establish the
project hypothesis.

Keep separate:

- construction correctness;
- safety/admissibility;
- structural detectability;
- fault attribution;
- information/action authorization;
- controller outcome; and
- confirmatory evidence.

The prior one-row replay is an implementation positive control only.

Prior structural-separability outputs are development diagnostics. They are
not a pilot, validation result, confirmatory result, or frozen decision margin.

The public README is append-only. Codex Session 43 added one lean milestone:
the exact Protocol-P specification and permanent construction guard are jointly
approved. The entry explicitly says that this authorizes seam review only; no
replay or screen stage has run, config remains unfrozen, and the test split is
untouched.

## Verification baseline

Use the repository virtual environment:

```powershell
.\venv\Scripts\python.exe -m pytest -q "Reproducibility Packet\tests"
```

Session 43 result:

```text
405 passed in 11.12 s
```

Focused I13b result:

```text
6 passed in 0.55 s
```

Do not use root-wide `pytest -q`; ignored duplicate trees under `tmp/` can
pollute collection.

Before any exact-state protocol approval, independently compute:

- raw bytes;
- BOM presence;
- CRLF count;
- raw SHA-256;
- canonical text SHA-256; and
- `git check-attr text eol`.

Before any binary replay decision, use raw hashes only.

Before any commit, run:

```powershell
git diff --check
git diff --cached --check
```

CRLF warnings alone are not a reason to churn unrelated files.

## Transcript-order state

The active transcript is append-only. Session-43 append verification:

```text
pre-write physical lines:
  8,881
pre-write bytes:
  698,078
pre-write sha256:
  f97b831f6812d97a50aac776d0b0cadca5e4ae13a5a966c5fb2f7c939505dca7
Codex header:
  line 8,885
  count 1 total
  count 1 after old byte boundary
old byte prefix:
  exact
technical diff:
  +91 / -0
post-write physical lines:
  8,972
post-write bytes:
  701,665
physical last author:
  Codex
```

No recurrence occurred, so the monitoring thread was not updated.

For every future append:

1. read the UTF-8 physical EOF tail;
2. record the pre-write physical line count, byte count, and hash;
3. verify a complete multi-line EOF anchor occurs exactly once;
4. patch only from that complete verified anchor;
5. verify the new header occurs exactly once after the old boundary;
6. verify the old byte prefix is exact;
7. reread the physical tail; and
8. require a transcript diff of additions only.

If any check fails, stop and repair by dated append-only correction.

## Required next actions

1. Read the controlling `AgentPrompt.md`, project details, this continuity file,
   all Codex-relevant chat summaries, and the complete active transcript before
   replying.
2. Read the repository review-cycle playbook before reviewing the applied seam.
3. Read Claude's newest report and inspect the exact implementation diff.
4. Use the implementation checklist above; reproduce source and test facts
   independently.
5. Append an explicit same-state approve/block decision using the physical-EOF
   hard gate.
6. Do not authorize replay until the implementation review closes.
7. Keep `config.json` absent and test identities/payloads at zero.
8. Close out with Codex `HumanReport44.md`, README update if a true public
   milestone occurs, complete continuity rewrite, hygiene checks, exact commit
   message, and push.

The next regular Codex progress report is Session 48 unless a phase transition
or approved written Claim Sheet amendment triggers an earlier report.

## Non-negotiable boundaries

- Approval is explicit and exact-state-specific. An edit, handoff, downstream
  use, or silence is not approval.
- Preserve owner/reviewer lanes.
- Never treat development, screen, pilot, fixture, or replay evidence as
  confirmatory.
- Never convert a safety pass into proof of correct construction.
- Never convert detection into attribution or action authority.
- Never silently rewrite a public or transcript-facing overclaim; append a
  correction.
- Never normalize binary artifacts before exact hashing.
- Never run the protocol from an unapproved implementation, even though the
  specification is now approved.
- Never run the seam, replay, stages, amendment, regeneration, or final freeze
  out of order.
- Never create final `config.json` before all required gates close jointly.
- Never touch the test split before confirmatory authorization.
- Use append-only transcript hard gates and preserve exact requested commit
  messages.
