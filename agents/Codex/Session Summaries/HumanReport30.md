# Human Report — Codex Session 30

**Current date and time:** 2026-07-24 13:09 PDT
**Phase:** Phase 2 — Integration and Reproducibility Build
**Session role:** Owner re-review and correction of the blocked Gate-3 assignment
**Final config state:** **UNFROZEN** (`config.json` remains absent)
**Governing decision:** `BLOCK_CONFIG_FREEZE_PENDING_PRECONFIRMATORY_BUILD_AND_VALIDATION`

---

## Summary

This session followed the complete `AgentPrompt.md` startup and closeout
workflow. I read the project details, Codex continuity, every Codex-including
chat summary, both active Codex chats, Claude's latest report, and the relevant
review-cycle, reproducibility-packet, and live-run playbooks. The live Phase-2
transcript superseded the Session-29 handoff: Claude Session 30 had explicitly
returned `BLOCK_GATE3_ASSIGNMENT_V0_1` on the exact replacement state I handed
off last session.

Claude's blocker was correct. The original modular context rotation used
`fault_index` while every split had two payload, environment, and contact
profiles. Under modulo 2, the nominally decorrelating coefficients collapsed,
leaving payload/environment alignment as a deterministic fault-index bit in all
80 fault settings. That bit could transfer from development to test and was
disproportionately readable by suite S, because temperature enters observations
through S-only gauge strain and payload is strongly legible in structural
channels. The assignment therefore risked inflating the paired S-minus-C1
headline result in the direction of the hypothesis.

I reproduced the leak directly before changing code. Every split had two
fault-conditioned context-cell sets, and payload/environment parity was locked
within every fault setting. I accepted Claude's diagnosis and implemented the
tested remedy:

- the self-hashed assignment JSON now contains the explicit balanced eight-cell
  `(payload, environment, contact)` table;
- context selection depends only on trajectory and replicate:
  `(trajectory_index * realizations_per_trajectory_fault[split] + replicate)
  % 8`;
- `fault_index` is no longer an input to any context selection;
- each split must carry exactly two profiles on each context axis, matching the
  binary table the assignment pre-registers; and
- the validator now fails unless every fault setting in a split receives the
  identical context-cell **count distribution**.

The last condition is deliberately stronger than the requested set-equality
invariant. Equal sets with unequal frequencies can still leak fault identity;
equal count distributions close that route too. Development and pilot now give
every fault the same four pairwise-balanced cells once each. Validation gives
every fault the complete eight-cell factorial once, and test gives every fault
the complete factorial twice.

The semantic change produced a new canonical assignment hash:

```text
dev-70832daabe7968d55c0bf68e713e945ed48ce167f5c54ec186559b9a660765de
```

The old Session-29 assignment hash
`dev-5939ff5f1f0cc29f75bb4abcd027dbe6ffe84844ad7727ac1e75ca9a0220cedb`
is superseded and must not be approved or embedded.

I added three adversarial regressions:

1. the tracked expansion must have one identical balanced distribution per
   split, with 4/4/8/8 unique cells and frequencies 1/1/1/2;
2. a monkeypatched fault-conditioned reservation must make the validator fail
   loudly; and
3. the assignment must carry the exact self-hashed balanced table.

I independently recomputed the canonical hash without calling the packet's
hash helper, reproduced the new context distributions from the expanded
reservations, and ran the focused and complete packet suites.

The replacement owner decision is:

```text
APPROVE_GATE3_ASSIGNMENT_V0_1
```

on the exact new state. The review loop remains open until Claude explicitly
approves that same state or returns a new file/line-specific block. No downstream
work may be treated as approval.

## Verification

Final verification from the repository virtual environment:

```text
focused Gate-3 tests: 18 passed in 0.12s
full packet suite: 376 passed in 8.73s
compileall: pass
CLI help: pass
read-only validator: pass
canonical assignment hash recomputation: exact match
git diff --check: pass (line-ending warnings only)
```

The read-only validator reports:

```text
context cells per fault: dev 4 / pilot 4 / val 8 / test 8
reservations: dev 76 / pilot 76 / val 168 / test 336
total reservations: 656
projected later manifest rows: 13,120
research generation allowed: false
test generation allowed: false
test reservations materialized: 0
```

Exact replacement-state identities:

```text
assignment hash
dev-70832daabe7968d55c0bf68e713e945ed48ce167f5c54ec186559b9a660765de

assignment JSON SHA-256
dcee3e6c9d52f7d36a84c06f0e3b1e5f39e89448c8b81940ca2728d9d9f98192

scripts/utils/gate3_assignment.py SHA-256
040cfe15ed6ffd70d9c5be32edfa418f4fb0ba98606e2dd7d85eb2f898897cef

tests/test_gate3_assignment.py SHA-256
e4749f67a98033b7d6e8223e8dad4c885b60ee96d9eac57f65910cbf270c1c9d

bound draft-config hash
dev-0211f2e71a473fef3c30cd53fd0a269df45156a3d58e83097bac7a5638bf6180
```

## Important decisions

### The assignment, not only the implementation, binds the context table

The balanced table is stored inside
`config/proposed-gate3-assignment-v0.1.json`, so its order and lookup rule are
part of the canonical self-hash. This avoids relying on an untracked code
convention for a pre-registration property.

### The validator checks distributions, not merely catalog coverage

The previous validator proved that every profile was used somewhere, which did
not prevent profiles from encoding fault identity through their combinations.
The new invariant is per split and per fault setting: every fault must receive
the same multiset of context cells. This is the property the headline comparison
actually needs.

### Non-blocking review notes did not silently widen the correction

Claude's notes about `split_group_id`, OOD breadth, and severity extrapolation
are carried as limitations/design considerations, but they were explicitly not
conditions of the block and were not changed here. I accepted Claude's proposed
Gate-7 interpretation rule—report the paired C1-vs-S contrast at pilot,
validation, and test and distinguish a contrast that decays with confound
severity from one absent at every rung—but no Gate-7 file was created or edited.

### Public status was intentionally unchanged

Claude Session 30 had already appended a public Live-Run entry explaining that
the blueprint was blocked before data generation because it favored the
hypothesis. This replacement state is still awaiting exact-state review, so
another public entry would turn the lean running log into a session journal and
would publicize an unapproved infrastructure checkpoint. The root `README.md`
was therefore left unchanged.

## Challenges and how they were handled

The main challenge was that the original assignment was internally consistent:
its self-hash, counts, split ownership, lifecycle interlocks, and all 15
adversarial tests were correct. The defect appeared only when the expansion's
consequences were measured. I handled this by reproducing the association from
the actual 656 reservations before editing, then auditing the replacement the
same way rather than trusting the new formula.

The second challenge was preventing a narrow fix from becoming another
arithmetic accident. A code-only rotation change could pass today while leaving
the assignment document vague. Binding the table in the JSON and enforcing its
realized distribution makes the correction reviewable, self-hashed, and
defended by tests.

## Cross-review performed

I read Claude's latest report,
`agents/Claude/Session Summaries/HumanReport30.md`, and the exact Gate-3 block in
the active Phase-2 transcript. I checked the implicated `CablePlant` structural
location constraint, the sensor thermal path, suite channel availability, and
the expanded reservation artifact rather than relying only on Claude's summary.
The blocker and remedy survived that independent owner re-review.

## Transcript append hard gate

Authoritative active transcript:

```text
chats/Claude-Codex/Phase 2 Integration and Config Freeze/
Phase 2 Integration and Config Freeze - Active.md
```

Verified physical state:

```text
pre-write lines: 2765
final lines: 2855
session delta: +90 / -0
Session-30 header after boundary: exactly 1
last physical line: — Codex
```

The 15-line EOF anchor was verified unique and physically last before the patch.
The patch used that complete verified block. Post-write assertions confirmed the
new header exactly once after the boundary, Codex physically last, and a pure
addition diff.

## Files created

- `agents/Codex/Session Summaries/HumanReport30.md` — this report.

## Files updated

- `Reproducibility Packet/config/proposed-gate3-assignment-v0.1.json` — balanced
  context table, fault-independent lookup rule, new canonical assignment hash.
- `Reproducibility Packet/scripts/utils/gate3_assignment.py` — balanced context
  expansion and per-fault distribution invariant.
- `Reproducibility Packet/tests/test_gate3_assignment.py` — three new
  adversarial regressions and updated hash/audit expectations.
- `Reproducibility Packet/README.md` — Step 2B and Current-boundary wording for
  the replacement review state.
- `chats/Claude-Codex/Phase 2 Integration and Config Freeze/Phase 2 Integration
  and Config Freeze - Active.md` — append-only replacement owner handoff.
- `agents/Codex/README.md` — workspace index and current Gate-3 status.
- `agents/Codex/Summary of Only Necessary Context.md` — completely rewritten
  resume state.

## Files deliberately not changed

- `README.md` — Claude already logged the noteworthy public block; the corrected
  replacement remains unapproved.
- `Reproducibility Packet/config/draft-config-v0.1.json` — no embedding before
  joint Gate-3 approval.
- final `Reproducibility Packet/config.json` — remains absent.
- `Reproducibility Packet/scripts/validate_gate3_assignment.py` and
  `scripts/utils/__init__.py` — byte-unchanged.
- `.gitignore` — reviewed; no new artifact class or untracked output required a
  rule.
- `agents/Codex/references.md` — no external source was used.

## Review and gate state at closeout

### Open

- Claude exact-state review of the corrected Gate-3 assignment.
- Gate 2 overall: real Gate-3-driven multi-setting MuJoCo generator and
  generated-data role/leakage audit.
- Gates 4–7 as listed in the approved Config Freeze Readiness Review.

### Closed

- Gate 1.
- Gate-2 role write/load/join foundation.
- Every earlier screen/review loop listed in continuity.

### Still forbidden

- embedding the replacement assignment before Claude's approval;
- generating assigned research data;
- materializing any test identity or payload;
- fitting headline models;
- creating final `config.json`;
- claiming Gate 2 or config freeze complete.

## Next steps

1. Read Claude's exact response to the replacement hash in the live transcript.
2. If Claude returns `APPROVE_GATE3_ASSIGNMENT_V0_1` with no edits, close Gate 3
   at that exact state.
3. Only after that approval, embed the exact assignment into the draft config
   and recompute the draft config hash.
4. Build the real assignment-driven generator paths for distal payload,
   split-owned environment, contact-window scheduling, and compound plant-plus-
   sensor faults.
5. Persist every role through `DatasetRoleBuilder`, then run the complete
   generated-data role/leakage audit with draft-state test refusal still active.
6. Keep headline fitting, test materialization, and final config freeze blocked
   until their later gates close.

The next regular Codex progress report remains Session 32.
