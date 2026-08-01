# Human Report — Codex Session 51

**Current date and time:** 2026-07-31 22:23 PDT

**Phase:** Phase 2 — Execution

**Session role:** Exact-state reviewer of Claude Session 51's Protocol-P shared-primitives extraction, Stage-A/B/C construction layer, focused tests, packet runbook correction, and public live-run entry

**Final config state:** **UNFROZEN**; no `config.json` exists

**Protocol-P execution state:** Stage 0 remains executed exactly once and jointly approved. Protocol P has spent one original plant rollout at the Session-45 replay gate; no replay or stage rollout ran this review. Stages A/B/C remain unexecuted and unauthorized. The confirmatory test split remains untouched.

---

## Summary

Claude's Session 51 did two useful things correctly: it treated the new construction layer as the real third consumer that triggered the pre-agreed Protocol-P extraction, and it removed Stage 0's incidental MuJoCo import without changing its approved measurement path. I approve the shared module, both existing consumer refactors, and the packet Step-24 dependency correction unchanged.

The construction handoff could not be approved unchanged. Protocol P v2.3.3 defines the per-rollout provenance payload exactly, but the implementation hashed a different flat object. It omitted the approved assignment hash, the delivered source reservation, and the complete fault override. The missing fault object meant the blocked step-0 structural fault and the approved step-500 construction would receive the same provenance stamp. All 725 handoff-state tests passed because the tests re-described the implementation's payload instead of asserting the protocol's exact object.

A second compositional gap let individually valid pieces form the wrong experiment: a valid cell-5 identity and source reservation could be labelled as cell 4, and a valid Stage-C identity could be used by a Stage-A request. The local I3/I5/I6/I7 checks were each correct but did not bind stage, cell, source and realized identity together at the construction point.

I repaired both classes directly, expanded the tests to assert exact nested payload shape and wrong-stage/wrong-cell failures, and approved the reviewer-edited state. The full packet now passes 736 tests. Because four handoff files were edited, Claude must genuinely re-review and explicitly approve or edit-and-return those exact states before the construction/public-entry loops close. No driver implementation or rollout is authorized by this session.

---

## What I reviewed

I completed the AgentPrompt startup sequence before acting:

- read all project details and the full Codex continuity state;
- read every Codex-involving summary and both active Codex-involving chats in the required two-phase order;
- read the controlling review-cycle, reproducibility-packet, and live-run-README playbooks;
- read Claude's complete `HumanReport51.md`; and
- reviewed the eight exact handed-off artifacts against Protocol P v2.3.3, the approved generator seam, the live assignment/config contracts, and the current public/runbook claims.

The eight handed-off states were:

1. `scripts/utils/protocol_p.py` — new shared primitives;
2. `scripts/utils/protocol_p_conditions.py` — new Stage-A/B/C construction layer;
3. `tests/test_protocol_p_shared.py` — new extraction/dependency tests;
4. `tests/test_protocol_p_conditions.py` — new construction tests;
5. `scripts/protocol_p_replay_gate.py` — imports moved to the shared module;
6. `scripts/analyze_synchronous_difference_null.py` — imports moved to the shared module;
7. `Reproducibility Packet/README.md` — Step-24 dependency sentence; and
8. root `README.md` — new public milestone entry.

---

## Decisions on the three questions

### 1. The construction layer is the third consumer

The trigger was architectural, not a filename test. `protocol_p_conditions.py` is production construction code the future driver consumes, and it uses the exception, fail-loud helper, canonical serialization rule, and protocol input identities. Waiting for the final driver script would make the larger driver land against a known obsolete coupling and combine a closed-gate refactor with a new execution surface.

### 2. Move the binary helper; keep the binary pins in the gate

`raw_file_sha256` belongs beside `canonical_text_sha256` because the two-domain rule is one protocol rule. The four `.npz` digest constants belong in the replay gate because only that gate reads and enforces them. I added a focused identity test requiring the gate's binary helper to be the shared object, while the existing test continues to require the replay-only pins to remain absent from the shared module.

### 3. A separate results module is acceptable, but the driver owns the integration proof

A narrow results module can make the real output root and result schema constructible without invoking `main()`. That does not authorize a unit-test-only boundary. The driver review must invoke the real driver against a real temporary results root and prove that an injected dataset, manifest, role-index, label, `ObservedRecord`, or payload write makes the integration fail. A green module test beside an unwired driver would repeat the project's established D5-class failure.

---

## Blocking finding 1 — the provenance object differed from the protocol

Protocol P Correction 2 requires one nine-key `rollout_identity_payload`:

```text
base_config_hash
assignment_canonical_sha256
assignment_hash
protocol_spec_sha256
stage
cell
condition
overrides   (all four non-provenance ScreenOverrides values)
reservation (scenario_spec_id, base_pair_id, sensor_seed)
```

The handed-off implementation emitted this flat eleven-key object instead:

```text
assignment_canonical_sha256  base_config_hash  cell  condition  pair_id
probe_peak_force_n  probe_ramp_fraction_of_duration  protocol_spec_sha256
sensor_seed  severity  stage
```

Consequences:

- `assignment_hash` was not bound;
- the delivered `scenario_spec_id` and derived reservation `base_pair_id` were not bound;
- `physical_faults` was not bound field by field;
- `onset_index` was not bound at all; and
- the canonical payload under review was not the canonical payload both agents approved in Protocol P.

The onset omission is decision-bearing. The Session-41 defect was precisely an omitted onset that activated the structural fault at step 0. Under the handoff state, that wrong request and the approved step-500 request carried the same provenance hash.

---

## Blocking finding 2 — stage/cell/source composition was not closed

The construction layer correctly generated Stage-A/B and Stage-C identities and correctly checked I3/I5/I6/I7. But `rollout_provenance` accepted any valid suffix-free `RolloutIdentity` next to any screened cell, and `screen_reservation` did not receive a target cell. Therefore:

- cell 5's valid delivered source could be screened and later called cell 4;
- cell 5's valid Stage-A identity could be carried inside a cell-4 result; and
- a valid Stage-C identity could be stamped onto a Stage-A request.

These are coherent wrong states, which is why each local guard can remain green. The construction point must bind the relation, not merely validate each object independently.

---

## Reviewer edits

The corrected code now:

1. closes the stage vocabulary to A/B/C;
2. requires Stage A/B to use that cell's Stage-A/B identity and Stage C to use one of that cell's eight Stage-C identities;
3. makes the target cell explicit when deriving a screen reservation;
4. checks the source scenario, source base pair, and split group against the target cell before derivation;
5. checks the retained source scenario and realized reservation/identity equality before hashing;
6. builds the exact protocol-defined nine-key payload;
7. nests all four override values, including every `FaultSpec` field and `onset_index`;
8. nests the three reservation fields exactly;
9. includes the approved assignment's `assignment_hash`;
10. returns the same named canonical string it hashes; and
11. adds tests for exact shape, every distinguishing input, wrong stage, wrong cell, wrong source, reservation/identity mismatch, and the shared binary-domain helper.

The root public entry was still in active review, so I corrected its intermediate test count from 129/724 to the final reviewer-edited 141 focused / 736 packet state. No settled dated public entry was changed.

---

## Exact review state

Approved unchanged:

```text
scripts/utils/protocol_p.py                         blob 8d9005250769b85739e5be4ddf00280f46acf71c
scripts/protocol_p_replay_gate.py                   blob c6b1674990a46f097a942559fd9077041d8270de
scripts/analyze_synchronous_difference_null.py      blob f104971d426af95ca664826cbc276228adff7963
Reproducibility Packet/README.md                    blob ba9c067a4d7ccce4b6c29edcf588b7eeb0e8150e
```

Reviewer-edited, explicitly approved by Codex, awaiting Claude owner re-review:

```text
scripts/utils/protocol_p_conditions.py              blob 7fdddf0eee5e3b3f02b2db21ecb1b70728234be5
tests/test_protocol_p_conditions.py                 blob 9e9556b073f3d691a4699af3aac9cedffe52d643
tests/test_protocol_p_shared.py                     blob f505877fbc43adb8c3ec2311674008f0c3b0e337
root README.md                                       blob 94e4e2678e63090cde71beac6c8169697cdbdcf4
```

The review diff against Claude Session 51 is +329/−51 across the four edited files. A final docstring-only correction updated the construction module's exact-state handle after the main transcript handoff; the executable logic and test result did not change.

---

## Verification

```text
focused construction + shared tests     141 passed in 0.73 s
full packet suite                        736 passed in 13.04 s
compileall                               clean
git diff --check                         clean (checkout-EOL warnings only)
transcript append                        +233 / -0
transcript old-prefix byte check         exact
Codex Session-51 header after boundary   exactly 1
config.json                              absent
Stage-0 artifact                         unchanged; not re-executed
Protocol-P replay/stage rollouts         none this review
.npz under packet results                0
confirmatory test split                  untouched
```

No protocol specification, assignment, draft config, Stage-0 artifact, generator seam, gauge helper, detection-floor artifact, dataset payload, or confirmatory material was edited.

---

## Current gate and next step

Claude must genuinely re-open and review the four reviewer-edited files, including both findings and their implementations, then explicitly approve the same blobs or edit-and-return a new exact state. Only same-state owner approval closes the construction/public-entry loops.

After closure, Claude may implement and hand off the narrow results module plus Stage-A/B/C driver. That driver still owns:

- I9 window origin/bounds;
- I10 measurement-time shape/length;
- I11 finite valid harmonic-fit sample count;
- I12 every post-rollout safety gate, per cell and condition;
- explicit Protocol-P condition keying, never the stale assignment label;
- no persistence of `ObservedRecord`, label, manifest, role index, or dataset payload; and
- a real wrong-write integration test against the actual output root.

No replay or Stage-A/B/C rollout is authorized. Configuration freeze, Amendment A2, replacement assignment, regeneration, learned-model work, and confirmatory generation remain downstream and blocked.

— Codex
