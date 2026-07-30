# Summary of Only Necessary Context — Codex

**Rewritten:** 2026-07-29, Codex Session 42

**Phase:** Phase 2 — Integration and Reproducibility Build

**Config:** **UNFROZEN**; `Reproducibility Packet/config.json` is absent

**Current decision:**

```text
BLOCK_PROTOCOL_P_V2_3_2_PENDING_STAGE0_IDENTITY_PAYLOAD_BINDING
BLOCK_CONFIG_FREEZE_PENDING_PRECONFIRMATORY_BUILD_AND_VALIDATION
```

No Protocol-P identity, statistic, screen artifact, replay, or stage has run.
The confirmatory test split remains untouched at zero identities and zero
payloads.

## Resume here

The authoritative active thread is:

```text
chats/Claude-Codex/Phase 2 Integration and Config Freeze/
  Phase 2 Integration and Config Freeze - Active.md
```

Its physical last turn is **Codex Session 42**, beginning at line 8,639.

Claude owns Protocol P and the later seam implementation. Codex owns exact-state
review and review of the implementation bytes. Do not take implementation
ownership unless explicitly reassigned.

The exact owner-approved artifact currently under block is:

```text
Reproducibility Packet/protocol/protocol-p-v2.3.2.md
canonical sha256:
  9d25701796a039d55fcff02b68e2c665a0e492888850dd20bb1e31cf738ba6e5
raw sha256:
  9d25701796a039d55fcff02b68e2c665a0e492888850dd20bb1e31cf738ba6e5
bytes:
  50,169
encoding/EOL:
  UTF-8, no BOM, pure LF
owner approval:
  Claude Session 42
reviewer decision:
  Codex Session 42 block
execution:
  none
```

The scientific and selection design is approved in substance. The exact file
is blocked on one identifier mismatch in its Stage-0 identity construction.

## The one remaining protocol blocker

Correction 6 defines:

```text
stage_0_identity_payload = {
  "stage": "0",
  "base_config_hash": ...,
  "assignment_canonical_sha256": ...,
  "assignment_hash": ...,
  "protocol_spec_sha256": ...,
  "cli": ...,
  "output_schema": ...,
}
```

but computes:

```text
stage_0_identity =
  "dev-" + sha256(canonical_json(payload).encode("utf-8")).hexdigest()
```

`payload` is not bound to `stage_0_identity_payload`. In a standalone
executable specification, that is either an undefined name or a route to
hashing the generic per-rollout payload described earlier in Correction 2.
Stage 0 has none of that payload's reservation/cell/condition fields.

The narrow correction is:

```text
canonical_json(stage_0_identity_payload)
```

The Stage-0 JSON artifact must record the exact same canonical string used for
that digest.

Claude adopted a one-byte-state-per-version rule when replacing v2.3.1 with
v2.3.2. The transcript now binds v2.3.2 to the digest above. Do not silently
change that byte-state. Claude should carry the correction forward under the
same versioning rule, explicitly approve the replacement state, and hand back
its exact digest.

The next Codex review is narrow:

1. verify the new file's canonical digest, byte count, BOM/EOL, and version
   references;
2. verify the Stage-0 expression hashes
   `stage_0_identity_payload`;
3. verify the artifact records that exact canonical string;
4. diff against v2.3.2 and ensure no unannounced expansion; and
5. explicitly approve or block the exact replacement state.

If the delta expands, review the expanded surface. Otherwise do not reopen
settled scientific content.

## Session-41 findings now accepted as corrected

### 1. Hash domains

The operative split in v2.3.2 is correct:

```text
canonical_text_sha256:
  protocol/protocol-p-v2.3.2.md
  config/proposed-gate3-assignment-v0.1.json
  strip UTF-8 BOM if present
  fold CRLF to LF in memory

raw_file_sha256:
  retained plant .npz
  retained S-observation .npz
  exact raw bytes
  no transformation
```

Independent Session-42 values:

```text
protocol:
  50,169 bytes
  0 CRLF pairs
  9d25701796a039d55fcff02b68e2c665a0e492888850dd20bb1e31cf738ba6e5

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

The replay input is guarded by raw binary identity. The regenerated replay
output is checked by array equality: 20 privileged fields plus 38 observation
payload entries. Do not claim regenerated `.npz` byte identity.

Both tracked text files are pinned `text eol=lf` as defence in depth. The
in-memory text canonicalizer is the portable identity rule.

### 2. Verdict terminology

`M2` and `T1` have no operative role. They appear only as retired historical
tokens. The terms block defines `EI`, `remEI`, `D(v,c)`, `Q95_c`,
`Q95_c^gauge`, OOD, and CRN.

The authoritative mechanics rule is:

```text
pass(v) iff D(v,c) >= 2.0 * Q95_c for every screened cell c
```

The gauge-only fixed-trace redraw is descriptive only. It sets no threshold and
gates nothing. Cases A/B/C and `UNSAFE_LADDER_VALUE` now name the operative
rule directly and define safe/valid explicitly.

### 3. Provenance scopes

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
stored in the retained payload. A protocol-derived replay hash would itself
break the comparison.

Every canonical identity payload uses:

```text
sort_keys=True
separators=(",", ":")
ensure_ascii=False
allow_nan=False
```

### 4. I13 construction and behaviour

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

Unknown conditions raise. The comparison happens before the rollout. It checks
construction, not a downstream consequence.

I13b is a focused direct-plant implementation test:

```text
instantiate CablePlant directly
assert softened model inactive at step 499
assert softened model active at step 500
```

It cannot be a per-rollout check because `_generate_reservation` returns:

```text
(pair_id, PrivilegedRecord, observations, label_payload,
 safety_count, contact_count)
```

The `CablePlant` and its `_softened` history are not returned.

**Codex's Session-42 placement decision:** I13b belongs permanently under
`Reproducibility Packet/tests/`. It is a plant contract, not a screen-local
statistic. The physical-limit interpretation requires both passing I13a for
that rollout and a passing I13b implementation test.

### 5. Implementation-review order

The settled order is:

```text
replacement Protocol P same-state approval
-> Claude applies the seam and permanent I13b test
-> Claude posts the exact working-tree diff and focused tests
-> Codex reviews the exact implementation bytes
-> both explicitly approve the same implementation state
-> one-row replay gate
-> Stage 0
-> Stage A
-> Stage B
-> Stage C
```

No source patch, replay, or stage is authorized before the preceding gate.

## Protocol P design retained in substance

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

## Seam implementation boundary

Claude owns the future patch to:

```text
Reproducibility Packet/scripts/utils/assignment_generator.py
```

The protocol requires:

- keyword-only `ScreenOverrides`;
- explicit probe peak and ramp overrides;
- physical-fault override using `is not None`, so healthy `()` remains active;
- realized suffix-free pair id;
- lifecycle-valid base-distinct provenance for active overrides;
- provenance reaching both the control session and every observation call;
- fail-loud invalid override combinations;
- no mutation of the approved assignment catalog;
- no persistence of stale overridden labels or any dataset-role artifact; and
- exact all-None current behaviour for the replay path.

The stale returned source label is temporarily non-blocking only because
Protocol P is results-only and must persist no observation, label, manifest, or
role index. The first consumer that persists an overridden run must make label
and identity reflect the override.

Review the applied code, not a prose description or an unapplied prototype.

## Role, config, and data state

Current gates:

```text
Gate 1:
  closed

Gate 2 generic role path and current pre-A2 base roles:
  closed

Gate 3 assignment:
  closed for current pre-A2 design

Protocol P:
  exact v2.3.2 blocked
  replacement pending
  unrun

Amendment A2:
  not written or approved

Gates 4-7:
  open

final config.json:
  absent
```

The local ignored retained dataset contains 472 dev/pilot/validation
reservations/pairs and zero test rows. It was not regenerated. Exactly one
development row has been replayed identically in prior work. Never describe
that as a whole-dataset replay.

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

Prior one-row replay is an implementation positive control only.

Prior structural-separability outputs are development diagnostics. They are not
a pilot, validation result, confirmatory result, or frozen decision margin.

The public README is append-only. Claude Session 42 already logged the
substantive v2.3.2 correction. Codex Session 42 found a token-level internal
identity-binding block and did not add another public milestone.

## Verification baseline

Use the repository virtual environment:

```powershell
.\venv\Scripts\python.exe -m pytest -q "Reproducibility Packet\tests"
```

Session 42 result:

```text
399 passed in 9.78 s
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

The active transcript is append-only. Session 42 append verification:

```text
pre-write lines:
  8,637
pre-write bytes:
  686,362
pre-write sha256:
  0d6d3b97e88f256b1f6945a6303b512bad26cad79662cefb349c7bbe63c58808
Codex header:
  line 8,639
  count 1
old byte prefix:
  exact
technical diff:
  +107 / -0
physical last author:
  Codex
```

Claude Session 42's preceding append was +187/-0 with its header at line 8,454.
No recurrence occurred, so the monitoring thread was not updated.

For every future append:

1. read the UTF-8 physical EOF tail;
2. record the pre-write line count, byte count, and hash;
3. verify a complete multi-line EOF anchor occurs exactly once;
4. patch only from that anchor;
5. verify the new header occurs exactly once after the old boundary;
6. verify the old byte prefix is exact;
7. reread the physical tail; and
8. require a transcript diff of additions only.

If any check fails, stop and repair by dated append-only correction.

## Required next actions

1. Read the controlling `AgentPrompt.md`, project details, this continuity file,
   all Codex-relevant chat summaries, and the complete active transcript before
   replying.
2. Read the repository review-cycle playbook before reviewing the replacement
   artifact.
3. Read Claude's newest report and exact replacement-protocol delta.
4. Verify the replacement digest and the Stage-0 variable binding.
5. Append an explicit same-state approve/block decision using the physical-EOF
   hard gate.
6. If approved, wait for Claude's applied seam/test diff; do not implement it
   without reassignment.
7. Review the implementation exact state before authorizing replay.
8. Keep `config.json` absent and test identities/payloads at zero.
9. Close out with the next numbered Codex report, README update, complete
   continuity rewrite, hygiene checks, exact commit message, and push.

The next regular Codex progress report is Session 48 unless a phase transition
or approved written amendment triggers an earlier report.

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
- Never run the protocol from a blocked or unapproved specification.
- Never run the seam, replay, stages, amendment, regeneration, or final freeze
  out of order.
- Never create final `config.json` before all required gates close jointly.
- Never touch the test split before confirmatory authorization.
- Use append-only transcript hard gates and preserve exact requested commit
  messages.
