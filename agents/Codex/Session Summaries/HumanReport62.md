# Codex Human Report — Session 62

**Date:** 2026-08-02 18:30 PDT

**Phase:** Phase 2 — Execution

**Decision:** Codex explicitly approves the reviewer-edited payload-boundary extension
v0.2 at canonical SHA-256
`e5192eaacef004469cfba5bcc4ff7da692e6fb828e5c33a7a2be5d8976a11a52`, Git blob
`3d72e1f468f30dfea7101181558720853202f293`. The review loop remains open until
Claude genuinely re-reviews and explicitly approves that same state. No seam build,
plan mode, replay, payload-boundary rollout, Amendment A2, or config materialization is
authorized yet.

## What happened

Claude Session 62 accepted all four blockers from Codex Session 61, superseded v0.1
with a much more complete v0.2, and explicitly approved its handoff state. The new draft
correctly introduced common random numbers across mass, a mass-aware `PhysicalKey`
prerequisite, an ordered classifier, exact plan/result paths, a default-path replay,
and anchor-first staging. Claude also corrected the physical interpretation of payload:
the plant has zero gravity, so the mass is tip inertia rather than a static hanging
weight.

I reviewed v0.2 against Protocol P v2.3.3, the approved generator seam, the approved
results layer, the assignment document, the executed Stage-A/B/C result, and the
payload-conditioning artifact. The high-level design was sound, but the exact handoff
still had several connected executability and authority defects. Under the review-cycle
playbook I edited the document directly, then explicitly approved the resulting exact
state and handed it back to Claude.

## Reviewer corrections

### 1. Circular provenance construction

The handed-off §11.3 required the identity payload to include all six
`ScreenOverrides` values. After adding distal mass, the six fields include
`provenance_hash`, but that hash was defined as SHA-256 of the identity payload. This is
a circular self-hash with no executable construction.

The reviewer-edited state pins exactly the five non-provenance inputs: probe peak,
probe ramp fraction, a field-by-field `FaultSpec` list, realized pair id, and distal
payload mass. It explicitly excludes `ScreenOverrides.provenance_hash`, derives the
canonical string and `dev-` digest first, and inserts the digest into the override
bundle afterwards. This matches the existing Protocol-P construction pattern.

### 2. Zero-rollout plan versus replay authorization

The draft placed the one-rollout replay gate before Stage X0, while §13 required both
agents to read a zero-rollout plan before issuing the authorization that would permit
that replay. Both statements could not be true in one stage order.

The approved reviewer state now has two explicit paths:

```text
plan mode     X0P only, zero rollouts, passing or failed plan persisted
execute mode  X0E -> XR -> XA -> XM-C -> XL -> XM-B -> XZ
```

X0E recomputes the passing plan and must match the separately authorized plan digest
before the replay can spend one rollout. Execute-mode terminal results and plan-mode
failures now each have a persistence path. Document approval, after Claude re-approves,
will authorize only the Step-2 build/review; executable approval will authorize only
zero-rollout plan mode; the plan digest still requires a separate rollout decision.

### 3. Anchor authority and payload liveness

The source reservation for the 0.050 kg anchor is
`scenario_dev_t01_f000_r02`, and that reservation already carries 0.050 kg. A dead
distal-mass override therefore still gives the anchor the requested body. The anchor is
a real control for the rebuilt probe/fault/identity instrument, but it is not a positive
control for the new payload field.

The corrected document states that boundary explicitly. After the anchor passes, all
six non-anchor healthy blocks run before any non-anchor ladder. X8 then compares the
seven healthy coefficient vectors within each of the eight CRN identity classes. A
dead payload seam produces identical bodies and identical vectors, so X8 stops before
any non-anchor attenuation is computed or up to sixty ladder rollouts are spent.

### 4. Result joins and replay accounting

The draft claimed 532 logical references but did not persist the joins needed to audit
them: ladder rows named only the fault provenance, null rows stored only scalar
distances, and a prose sentence stood in for the row-to-ledger mapping. It also called
the extension ledger one entry per distinct physical rollout without separating the
ordinary replay, which inherits a base hash and cannot carry an extension identity
payload.

The corrected schema makes the join executable:

- each ladder row cites both fault and healthy physical keys;
- each null distance cites both endpoint physical keys;
- the result counts actual ladder-fault, ladder-healthy, and null-endpoint references;
- the extension ledger excludes the replay as Protocol P requires;
- replay evidence remains under `replay_gate`; and
- extension, replay, total-rollout, logical-reference, stamp, and identity counts are
  separate fields.

The full-plan arithmetic is now mechanically auditable: 126 extension rollouts, one
replay, eight identities, and 532 logical references.

### 5. Reduced coverage and option authority

Claude's permissive rule allowed a reduced-coverage outcome to license the option
associated with the measured masses. That was still too permissive for a measurement
whose purpose is to settle all six unmeasured masses. It also allowed Option B to use
the heaviest mass retaining its own split role even when a lighter mass had lost a
different split's role; a heavier role regain cannot repair a lighter loss.

The corrected ordered classifier adds:

- `X_INVALID_MEASUREMENT` for invalid windows, time shapes, finite-sample counts,
  coefficients, distances, or thresholds;
- `X_REDUCED_MASS_COVERAGE` before every shape/case rule; and
- a rule that reduced coverage preserves scoped partial evidence but licenses no A2
  option.

At complete coverage, Option B is licensed only by the longest ascending lower-mass
prefix in which every mass retains its own role. For `X_CASE_EMPTY`, Option A is not
licensed inside the measured ladder because no tested severity clears an empty mass; a
lower grid would need a new prospective measurement.

The split severity map remains pinned as literals. A focused test, not the measurement
executable, reads `fault_grid_by_split` and asserts equality, preserving the
development-only boundary.

## Judgments on Claude's four requested questions

1. **CRN cost statement — accepted.** The seven per-mass nulls are matched rather than
   independent, but each per-mass null still has eight identities and no classifier
   treats cross-mass nulls as independent. Common random numbers are the right design
   for isolating mass in the set-valued contrast.
2. **`PhysicalKey` prerequisite — accepted.** Without mass in the key, CRN causes
   different bodies to collide and permits silent cross-mass reuse.
3. **Permissive exclusion — accepted only after narrowing.** Partial safe evidence may
   be preserved, but reduced coverage has no A2 decision authority.
4. **Nine-rung anchor — accepted.** The constrained/unconstrained partition is
   unchanged for every `tau_anchor` in `(0.021, 0.196)`. Requiring the 0.50 rung to keep
   its sign would require reproduction of a 2.1%-of-threshold edge.

## Independent verification

Static and zero-rollout checks reproduced:

```text
source reservation        scenario_dev_t01_f000_r02
source payload            0.050 kg
role map                  dev .50/.75; pilot .60/.85; val .40/.90; test .35/.65
planned extension keys    126 / 126 distinct with mass in the key
CRN identities            8
full logical references   532
monotone prefix states    19,448 / 19,448 classified exactly once
role-lost states where
  Option B is unavailable 330 (the lighter-role-loss case the old rule missed)
gravity                   [0, 0, 0]
qfrc_bias                 exactly zero at the initial state
nominal total body mass   0.17280000257492067 kg
declared mass deltas      all eight exact within atol 1e-12
cell-6 margins            reproduced from stage_abc_screen.json
```

The full packet suite passed:

```text
1,126 passed in 124.04 s
```

The first test invocation was interrupted by an overly short tool timeout and ended in
an output-stream error; it was not a test failure. The clean rerun above completed with
exit code zero.

No Protocol-P scenario, plan mode, replay, or physical rollout ran. The direct plant
checks compiled models and inspected static mechanics only. `config/config.json`
remains absent.

## Exact reviewed state and transcript integrity

```text
Reproducibility Packet/protocol/payload-boundary-extension-v0.2.md
  canonical SHA-256 e5192eaacef004469cfba5bcc4ff7da692e6fb828e5c33a7a2be5d8976a11a52
  Git blob          3d72e1f468f30dfea7101181558720853202f293
  69,428 bytes; 1,257 content lines; LF; no BOM; raw == canonical
```

The Phase-2 transcript append passed the hard gate. Its pre-write 1,074,068-byte,
16,064-line state remains a byte-identical prefix with raw SHA-256 `b3a6f10e...`; the
new Codex Session-62 header occurs exactly once at line 16,068; and the transcript diff
is `+95/-0`.

## Files created or updated

- `Reproducibility Packet/protocol/payload-boundary-extension-v0.2.md` — direct
  reviewer edits and Codex exact-state approval.
- `chats/Claude-Codex/Phase 2 Integration and Config Freeze/Phase 2 Integration and
  Config Freeze - Active.md` — append-only review decision and owner handback.
- `agents/Codex/Session Summaries/HumanReport62.md` — this report.
- `agents/Codex/README.md` — session index and current review state.
- `agents/Codex/Summary of Only Necessary Context.md` — complete continuity rewrite.

The root Live-Run README remains unchanged because this is an internal review handback,
not a new public scientific milestone. `.gitignore` already covers
`.agent-session.lock`; no update is needed. No regular progress report is due until
Codex Session 64.

## Next action

Claude must genuinely re-open the reviewer edits and either explicitly approve exact
canonical digest `e5192eaa...` or hand back a new state. If Claude approves the same
state, the document review loop closes and only the Step-2 build/review becomes
authorized. Plan mode, replay, payload-boundary execution, Amendment A2,
`config.json`, assignment/config regeneration, Gates 4–7, and confirmatory
materialization remain blocked behind their separate gates.
