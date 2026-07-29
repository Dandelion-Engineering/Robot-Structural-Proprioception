# Human Report — Codex Session 40

**Current date and time:** 2026-07-29 13:12 PDT

**Phase:** Phase 2 — Integration and Reproducibility Build

**Session role:** Exact-state review of Claude's Protocol P v2.3 proposal,
followed by the regular Session-40 director progress report.

**Final config state:** **UNFROZEN** (`Reproducibility Packet/config.json`
remains absent)

**Decision:**

```text
BLOCK_PROTOCOL_P_V2_3_PENDING_EXACT_FAULT_ONSET_AND_LIFECYCLE_VALID_PROVENANCE
BLOCK_CONFIG_FREEZE_PENDING_PRECONFIRMATORY_BUILD_AND_VALIDATION
```

**Rollouts spent:** zero. No Protocol-P identity was generated and no
Protocol-P statistic was computed.

## Summary

Claude Session 40 posted Protocol P v2.3 after checking and adopting all nine
requirements from Codex Session 39. The new proposal corrected the realized
pair-id construction, narrowed the one-row replay and Finding-J claims, reduced
the gauge-only null to a conditional descriptive diagnostic, removed the
unsupported replay-based defect localization, and specified explicit
fail-loud checks. Claude also prototyped a typed `ScreenOverrides` seam outside
the packet and reported that its all-None path reproduced one retained
development row exactly.

Codex reviewed the proposal against the committed generator, `FaultSpec`
carrier, plant activation rule, storage lifecycle, Git attributes, approved
assignment, bound draft config, and current tests. The scientific and
selection design now substantially converges: no additional defect was found
in the Stage A/B/C candidate grid, matched identity, safe terminal branches,
cellwise healthy null, role coverage, OOD handling, ordinary-row scope, contact
window, torque pruning, or unchanged success bar.

Two exact construction defects still block applying the seam.

First, the structural `FaultSpec` carried forward from v2.2 names source,
subtype, location, and severity but omits `onset_index`. Its dataclass default
is `-1`; `CablePlant._fault_active` converts that to step 0. The committed
generator's normal path instead derives the declared diagnostic trajectory
onset, which is step 500 for `1.0 s / 0.002 s`. Under the proposed override the
link would therefore be soft from the start of the rollout rather than
changing at the pre-registered fault boundary. That would remove the healthy
pre-change segment and change the measurement being authorized.

Second, the proposed provenance guard checks only that a string is nonempty.
It therefore permits a caller to pass the base `config_hash`, contradicting the
proposal's claim that an altered run cannot carry the base identity. The
proposed derived value, `dev-protocolp-v2.3-<32 hex>`, is also not a
lifecycle-valid packet hash: the storage contract accepts an optional `dev-`
followed by a full 64-hex SHA-256.

The same provenance review found two byte-stability gaps. The placeholder
`protocol_spec_sha256` does not define which bytes are hashed and would omit
load-bearing sections referenced from the Protocol-P block. The raw assignment
file digest is currently correct for its LF worktree bytes, but the file is not
LF-pinned while the Windows Git installation uses `core.autocrlf=true`; a CRLF
checkout produces a different raw SHA-256 for the same parsed assignment.

Codex appended one narrow correction handoff rather than asking for a fifth
full protocol rewrite. The next exact state needs to pin the fault onset and
healthy empty tuple, make provenance full-length and base-distinct, bind a
complete canonical protocol-spec artifact, and either LF-pin or canonically
hash the assignment.

## Challenges and how they were handled

### Distinguishing a strong prototype from an approvable construction

Claude's prototype demonstrated that peak, ramp, physical-fault, and realized
identity overrides can reach the intended code paths, and that the all-None
path can preserve one delivered row. Those are valuable positive controls.
They do not prove that the exact fault object has the correct lifecycle.

Codex followed the object from the proposal through:

```text
ScreenOverrides.physical_faults
  -> _generate_reservation
  -> CablePlant
  -> _fault_active
```

That trace exposed the silent `onset_index=-1` default. A zero-cost carrier
inspection confirmed that the exact proposed `FaultSpec` resolves to effective
activation step 0.

### Separating provenance content from provenance syntax

The proposal now contains the right provenance categories: base config,
approved assignment, protocol specification, stage, cell, condition, exact
overrides, and reservation identity. The remaining problem is enforcement.

Codex compared the proposed string against the packet's actual lifecycle
validator and found that the 32-hex descriptive prefix is not accepted as a
config hash. A second direct check showed that the seam's nonempty-string guard
would accept the base hash unchanged. The handoff therefore preserved the
provenance object while narrowing the required implementation to one full
`dev-<64 hex>` digest, validated and required to differ from the supplied base.

### Respecting the label-stamp boundary without leaving a footgun

Claude disclosed that a physical-fault override leaves the returned assignment
label describing the healthy source reservation. Codex agreed this is
non-blocking for Protocol P only because the screen is results-only and does
not persist an `ObservedRecord`, label payload, manifest, or role index.

The handoff made that boundary testable: the implementation must use the
explicit Protocol-P loop condition rather than the returned label and must
prove it writes no dataset-role artifact. Any future consumer that persists an
overridden record must repair both the label and run identity first.

### Preserving the append-only transcript under the known failure mode

Before writing, Codex recorded the active transcript's 7,769-line,
645,984-byte physical state and SHA-256
`CD944A35D1714EB3192D70AC31B2ADEA79A562458F94CC8E56755CC39AB7B6A7`.
The patch used Claude's complete verified EOF block.

After writing:

```text
post-write lines:          7,951
Session-40 header:         line 7,771
header count:              1
header after boundary:     yes
technical diff:            +182 / -0
old-prefix SHA-256:        exact match
physical last author:      Codex
```

No monitoring-thread update was needed because no recurrence occurred.

## Important decisions

1. **Approve the scientific and branch design of v2.3 in substance, but not the
   exact executable state.** The remaining defects are construction identity,
   not a reason to redesign the candidate grid or null.
2. **Require the fault onset explicitly.** The structural override must carry
   `_step_index(trajectory onset, control_dt)`; for dev Protocol P that is step
   500.
3. **Require an explicit healthy physical-fault tuple.** Healthy uses `()`;
   structural conditions use one fully populated known-class `FaultSpec`.
4. **Use a lifecycle-valid provenance hash.** The derived identity must be
   `dev-` plus the full lowercase 64-hex digest.
5. **Reject base-hash reuse inside the seam.** Caller discipline alone cannot
   support the claim that an altered run cannot masquerade as the base state.
6. **Hash the complete operative protocol state.** A tracked canonical spec
   must contain the seam, replay, diagnostic, branch, and interpretation pins
   that the short block references.
7. **Make raw byte hashes portable.** The assignment file must be LF-pinned if
   its raw bytes remain part of the identity, or the canonical assignment hash
   should replace the raw-file digest.
8. **Keep the label gap non-blocking only under a tested no-persistence rule.**
9. **Do not update the public README for this internal gate.** It is not a
   scientific result, public deliverable, phase change, or resolved amendment.
10. **Do not escalate to the director yet.** The new findings are direct source
    contradictions, not a repeated disagreement requiring arbitration.

## Reasoning paths explored

- Checked whether the plant could reconstruct onset from the source reservation
  after the override. It cannot; replacing the physical list bypasses
  `_fault_components`, which is the only committed path that calculates
  `onset_index`.
- Checked whether `-1` meant “use trajectory default.” It does not. The plant
  clamps it to zero.
- Considered whether the all-None byte-identical replay covered the defect. It
  does not exercise `physical_faults`, so it is correctly retained as a
  transparency test rather than treated as override validation.
- Checked whether the provenance hash was merely an opaque screen id. It is
  stamped into `ObservedRecord.config_hash`, whose packet lifecycle defines a
  SHA-256 identity and whose storage validator requires full hex.
- Considered whether caller-side comparison with the base hash was sufficient.
  It would leave the screen-only seam able to violate the exact safety claim,
  so the distinction must also be enforced at the seam boundary.
- Checked the current assignment raw digest independently. It matches Claude's
  value on the current LF bytes, but a simulated CRLF checkout changes it from
  `76255a80...514ae` to `00dacaf6...4f87f`.
- Considered reopening the whole protocol. The remaining fixes are local and
  mechanical, so the handoff requests an append-only correction rather than a
  new design document.

## Insights gained

1. **A typed override can still import a dangerous dataclass default.** Type
   safety proves the object has an `onset_index`; it does not prove the caller
   supplied the experiment's onset.
2. **A positive-control replay validates the default branch only.** It cannot
   authorize a newly added non-default path without branch-specific tests.
3. **A provenance claim needs both content and enforcement.** Naming every
   source in a canonical object is not enough if the seam accepts an unrelated
   nonempty string.
4. **A descriptive prefix is not a lifecycle hash.** Hash-bearing schema fields
   should retain the repository's one existing `dev-<64 hex>` convention.
5. **Raw file hashes become cross-platform contracts.** Once bytes enter the
   scientific identity, line-ending policy is part of the protocol.

## Verification

- Source and contract audit:

  ```text
  proposed FaultSpec onset_index:       -1
  effective plant activation step:       0
  committed dev t01 activation step:   500
  proposed provenance format valid:  false
  nonempty guard accepts base hash:    true
  ```

- Assignment bytes:

  ```text
  current LF SHA-256:
    76255a8089f3e27d893b26d981cbf50e808bd75ba518c44b55c4635ec83514ae
  same parsed text rendered CRLF:
    00dacaf6277d6b274e3690ab3d3f68607eb61a22fe0df75ea8688fe4c7d4f87f
  ```

- Packet regression suite:

  ```text
  399 passed in 11.00s
  ```

- `git diff --check` passed for the transcript append. Line-ending warnings
  were informational and did not change the verified old prefix.

## Files created or updated

- `chats/Claude-Codex/Phase 2 Integration and Config Freeze/Phase 2 Integration and Config Freeze - Active.md`
  — appended the exact-state v2.3 block and narrow correction.
- `agents/Codex/Session Summaries/HumanReport40.md`
  — this report.
- `agents/Codex/Progress Reports/Progress Report Session 40.md`
  — regular eighth-session director update covering Codex Sessions 33–40.
- `agents/Codex/README.md`
  — updated navigation and current active-state description.
- `agents/Codex/Summary of Only Necessary Context.md`
  — completely rewritten for Session 41.

No Reproducibility Packet source, config, schema, result, assignment, or test
file was changed. The public README and `.gitignore` required no update.

## Next steps

Claude owns one narrow append-only correction to v2.3:

1. set the structural `FaultSpec.onset_index` from the trajectory onset and
   make the healthy tuple explicit;
2. emit and validate a full base-distinct `dev-<64 hex>` provenance identity;
3. bind one complete tracked canonical protocol spec;
4. make the assignment byte identity portable or canonical; and
5. explicitly approve the corrected exact state on handoff.

Codex then re-reviews that delta. Only after exact proposal approval may Claude
apply the seam patch and hand the implementation diff back for separate review.
No replay gate or Protocol-P stage runs before implementation approval.

The final `config.json`, written Amendment A2, Claim Sheet edits, replacement
assignment, regeneration, Gate-4 fitting, and all confirmatory material remain
unauthorized.
