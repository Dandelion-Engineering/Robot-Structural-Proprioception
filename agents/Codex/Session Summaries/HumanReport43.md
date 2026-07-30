# Human Report — Codex Session 43

**Current date and time:** 2026-07-29 18:12 PDT

**Phase:** Phase 2 — Integration and Reproducibility Build

**Session role:** Exact-state reviewer of Claude's Protocol P v2.3.3
replacement and the permanent I13b plant-contract regression test.

**Final config state:** **UNFROZEN** (`Reproducibility Packet/config.json`
remains absent)

**Decision:**

```text
APPROVE_PROTOCOL_P_V2_3_3_EXACT_STATE
APPROVE_I13B_PERMANENT_PACKET_TEST_CURRENT_STATE
BLOCK_CONFIG_FREEZE_PENDING_PRECONFIRMATORY_BUILD_AND_VALIDATION
```

**Protocol-P execution spent:** zero. No replay or screen stage ran, no
Protocol-P identity or statistic was generated, no Protocol-P artifact was
written, and the confirmatory test split remains untouched at zero identities
and zero payloads.

## Summary

Claude Session 43 accepted Codex Session 42's Stage-0 identity-binding finding,
verified it against the tracked v2.3.2 bytes, and found that its silent failure
route was real: the generic name `payload` had already been used for the
per-rollout identity object, so an implementer could compute a valid digest over
the wrong payload rather than encounter a loud undefined-name failure.

Claude renamed the tracked specification to v2.3.3, preserving the rule that
one version name denotes one byte-state, and explicitly approved:

```text
Reproducibility Packet/protocol/protocol-p-v2.3.3.md
canonical SHA-256:
  5689dad7ce4194b9a7dbe381006027df178997adf732f5734a77ef048bdf421f
raw SHA-256:
  5689dad7ce4194b9a7dbe381006027df178997adf732f5734a77ef048bdf421f
bytes:
  54,621
encoding/EOL:
  UTF-8, no BOM, pure LF
git attributes:
  text set, eol lf
```

The replacement diff deliberately expanded beyond the single reported token.
Claude audited every identifier in an operative expression and corrected four
members of the same binding/authority class:

1. Stage 0 now hashes `stage_0_identity_payload` through a named
   `stage_0_canonical`, and the artifact records that same canonical string
   object.
2. The per-rollout path now uses `rollout_identity_payload` and
   `rollout_canonical`; the only bare `payload` left in the file is the locally
   bound formal parameter of `canonical_json`.
3. The Stage-A/B and Stage-C seed expressions now use the defined
   `P_SEED_BASE` constant rather than repeating its literal. The concrete
   identities remain unchanged.
4. I13a now derives the expected onset with the already-bound
   `control_dt_s`, not an undefined `dt`.

Codex reviewed the complete 1,003-line standalone protocol, the full
v2.3.2-to-v2.3.3 diff, Claude's Session-43 report and continuity, the new test,
and the relevant plant and fault-definition sources. Independent byte checks
reproduced Claude's exact protocol digest, byte count, BOM/EOL state, and git
attributes. The four expanded corrections are coherent, keep every concrete
seed unchanged, and introduce no result-moving change to the universe,
statistic, threshold, selection, stage counts, terminal branches, secondaries,
role coverage, OOD boundary, or success criterion.

Codex therefore explicitly approved the exact v2.3.3 digest. Claude and Codex
now approve the same protocol byte-state, so the Protocol-P specification
review loop is closed.

## I13b permanent plant-contract test

Claude also added:

```text
Reproducibility Packet/tests/test_cable_plant_softening_boundary.py
raw SHA-256:
  712d2165f8bd96d5e88a07e5f76c53313cb5e6aca5c6d0d21af43914c3e26ac7
git blob:
  ca0f44743b3e7b4f4268e596fc82f6e1bbee2411
bytes:
  6,671
encoding/EOL:
  UTF-8, no BOM, pure LF
tests:
  6
```

This was a sequencing deviation. Codex had placed the test after protocol
approval alongside the future seam implementation; Claude implemented it one
session early, disclosed that choice prominently, and offered to revert it if
strict sequencing was required.

Codex accepted the deviation and approved the exact committed test state.
Codex had already approved its permanent location because structural-fault
activation is a `CablePlant` contract rather than a Protocol-P-specific
statistic. The test changes no production source, generator seam, identity,
artifact, dataset role, or Protocol-P result.

Codex read the actual implementation rather than relying on the test's prose:

```text
CablePlant.advance()
  -> _activate_structural_fault_if_needed()
  -> _fault_active()
  -> self._step_index >= max(int(fault.onset_index), 0)
  -> model/data/handles swap to the prebuilt softened model
```

Activation occurs before simulating the current control step. The test matches
that lifecycle correctly: after advancing all pre-onset steps the nominal model
is still active, and the next `advance()` swaps the actual model at the declared
onset. It asserts the model object as well as the `_softened` bookkeeping flag,
covers onsets 1, 5, and 500, pins `_step_index(1.0, 0.002) == 500`, verifies
that an omitted onset activates at step 0, and verifies that a healthy plant
never builds or activates a softened model.

Independent focused and full-suite runs passed:

```text
test_cable_plant_softening_boundary.py:
  6 passed in 0.55 s

Reproducibility Packet/tests:
  405 passed in 11.12 s
```

I13b must remain green through the seam review and before any replay or screen
stage runs.

## Review-cycle decision and authorization boundary

The exact v2.3.3 protocol state is jointly approved. This authorizes Claude to
apply the specified screen-override seam to:

```text
Reproducibility Packet/scripts/utils/assignment_generator.py
```

and to post the exact applied working-tree diff plus focused tests for a
separate implementation review.

It does **not** authorize:

- the one-row replay;
- Stage 0, A, B, or C;
- generation of a Protocol-P identity, statistic, or result artifact;
- a written or executed Amendment A2;
- a replacement Gate-3 assignment;
- regeneration of the retained non-test dataset;
- creation of final `config.json`; or
- any confirmatory test identity or payload.

The settled order is now:

```text
Protocol P v2.3.3 exact-state approval                COMPLETE
permanent I13b exact-state approval                   COMPLETE
Claude applies generator seam and posts exact diff   NEXT
Codex reviews exact implementation state             REQUIRED
one-row replay gate                                   AFTER APPROVAL
Stage 0 -> Stage A -> Stage B -> Stage C             SEQUENTIAL
result/terminal-branch review                         REQUIRED
written Amendment A2 + replacement assignment        LATER
from-zero non-test regeneration and re-audit          LATER
Gates 4-7 -> joint final freeze -> confirmatory run   LATER
```

No director arbitration is needed. Session 43 corrected a new,
source-checkable defect and introduced no repeated disagreement over a settled
scientific choice.

## Challenges and how they were handled

### The replacement diff expanded beyond the promised narrow review

Codex Session 42 offered to limit the next review to the Stage-0 binding and
consequential version references unless the diff expanded. Claude declared the
expansion, itemized all four changes, and explained their common defect class.
Codex therefore reviewed the complete standalone file and the full delta rather
than assuming that the original narrow scope still applied.

The expansion held. Every new name binds to the object the surrounding
specification defines, the seed-base change is arithmetic-preserving, and the
onset expression now uses an already-defined variable.

### The new test arrived ahead of the agreed order

The sequencing deviation was handled as an explicit review decision rather
than silently normalized. The test was already in the approved permanent
location, was independently source-checked, and altered none of the production
or experimental state held behind the gate. Reverting and re-adding it would
create churn without restoring a scientific boundary, so Codex approved it in
place.

### The transcript remains a mixed-EOL append-only artifact

Before appending, Codex read the physical UTF-8 tail and recorded:

```text
pre-write physical lines:
  8,881
pre-write bytes:
  698,078
pre-write SHA-256:
  f97b831f6812d97a50aac776d0b0cadca5e4ae13a5a966c5fb2f7c939505dca7
```

The complete six-line Claude EOF block was verified as unique and physically
last, then used as the exact patch context. Post-write checks established:

```text
old 698,078-byte prefix:
  exact
Codex Session-43 header:
  line 8,885
  one occurrence total
  one occurrence after the old byte boundary
transcript diff:
  +91 / -0
post-write physical lines:
  8,972
post-write bytes:
  701,665
physical last author:
  Codex
```

No transcript-order recurrence occurred, so the director-visible monitoring
thread did not require an entry.

## Important decisions and reasoning

1. **Approve the exact v2.3.3 state rather than reopen settled scientific
   content.** The expanded changes repair binding and authority without moving
   any statistic or branch. Reopening the scientific design would violate the
   review boundary without new evidence.
2. **Approve I13b in place.** The deviation was real, but the test protects an
   already-approved plant contract, changes no production state, and was
   independently verified. Reversion would improve chronological tidiness but
   not correctness.
3. **Keep implementation review separate from specification approval.** The
   written seam is now approved; the future code bytes are not. Replay remains
   unauthorized until Codex reviews the applied diff and both agents explicitly
   approve the same implementation state.
4. **Add a lean public milestone.** The root live-run log now records that the
   fingerprinted screen specification and construction guard reached joint
   approval. It explicitly says this authorizes seam review only and preserves
   the non-confirmatory, unfrozen, untouched-test boundary.
5. **Do not write a progress report.** Codex's next regular progress report is
   Session 48. This session closed an artifact review but did not close a
   project phase or approve a written Claim Sheet amendment.
6. **Leave `.gitignore` unchanged.** The only new tracked artifact was Claude's
   small Python test, already committed before this session. No secret, local
   environment file, generated payload, cache, or large artifact appeared.

## Insights gained

- A declared class audit is reviewable only when its expansion is bounded and
  itemized. "I checked everything" is not a useful handoff; four named changes
  with unchanged consequences are.
- A sequencing rule protects an authorization boundary, not chronology for its
  own sake. When early work stays strictly on the authorized side of every
  substantive boundary, the right response can be explicit acceptance rather
  than mechanical reversion.
- Testing the actual model object is materially stronger than testing a flag
  that describes it. The test now protects the construction that matters, not
  only the implementation's self-report.
- Exact specification approval and implementation approval are different
  states. The protocol can now be approved while every execution path remains
  blocked on the code review.

## Cross-review performed

Codex read and checked:

- Claude's complete Session-43 transcript handoff;
- `agents/Claude/Session Summaries/HumanReport43.md`;
- Claude's rewritten continuity file;
- the full v2.3.2-to-v2.3.3 commit diff;
- the complete `protocol-p-v2.3.3.md`;
- `test_cable_plant_softening_boundary.py`;
- the structural activation path in `cable_plant.py`;
- the `FaultSpec` defaults in `schema_types.py`; and
- the relevant `_step_index` and onset derivation in
  `assignment_generator.py`.

Claude's report is accurate about the four identifier-class corrections, the
protocol bytes, the six-test addition, the unchanged scientific design, and the
absence of any Protocol-P execution. Codex independently reproduced the
decisive byte and test facts rather than relying on the report.

## Files created or updated this session

- `chats/Claude-Codex/Phase 2 Integration and Config Freeze/Phase 2 Integration
  and Config Freeze - Active.md` — appended the exact-state protocol/test
  approval and next implementation gate through the physical-EOF hard gate.
- `README.md` — appended one lean public milestone recording joint Protocol-P
  specification approval while preserving all execution and evidence
  boundaries.
- `agents/Codex/Session Summaries/HumanReport43.md` — this report.
- `agents/Codex/README.md` — updated workspace map and current external-state
  descriptions.
- `agents/Codex/Summary of Only Necessary Context.md` — completely rewritten
  for the seam-implementation review that comes next.

Not changed: Protocol P, the I13b test, any packet source, schema, assignment,
config, result, dataset payload, label, role index, `director_requests.md`,
`.gitignore`, `.gitattributes`, or the monitoring chat.

## Next steps

1. Wait for Claude to apply the specified seam to
   `assignment_generator.py` and hand off the exact working-tree diff plus
   focused tests.
2. Review the exact implementation bytes, including all-`None` replay
   preservation, provenance propagation, fail-loud invalid combinations,
   results-only persistence boundaries, and I13a construction equality.
3. Explicitly approve or block that exact implementation state.
4. Only after implementation approval, authorize the one-row replay.
5. Keep replay, Stage 0/A/B/C, Amendment A2, replacement assignment,
   regeneration, Gates 4–7, final freeze, and confirmatory execution in their
   declared order.
6. Keep `config.json` absent and the confirmatory test split at zero identities
   and zero payloads until the joint freeze and authorization gates close.
