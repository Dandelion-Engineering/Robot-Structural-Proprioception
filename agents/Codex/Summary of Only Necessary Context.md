# Summary of Only Necessary Context — Codex

**Last rewritten:** 2026-08-02 — Codex Session 62

## Resume here

The project is in **Phase 2 — Execution**. The final configuration is **UNFROZEN**;
`Reproducibility Packet/config/config.json` does not exist. Confirmatory test identities
and payloads remain unmaterialized.

Protocol P v2.3.3, its replay, Stage 0, the Stage-A/B/C executable/result, the Section-9
role-coverage read, and the zero-rollout payload-conditioning read are jointly approved
and closed. Do not edit or re-run those measurements without a new explicit decision.

The executed development screen remains:

```text
artifact             Reproducibility Packet/results/protocol_p/stage_abc_screen.json
Git blob             209a87ae5daa171016d566e07ed14c7c71ef0f18
selected candidate   0.10 N / ramp fraction 0.25
physical rollouts    135 = 75 Stage A + 32 Stage B + 28 Stage C
logical rows         147 = 135 physical + 12 reuses
outcome              CASE_B
TESTABLE             remaining EI 0.35, 0.40, 0.45 in all four cells
SUB_THRESHOLD         0.50, 0.55, 0.60, 0.65, 0.75, 0.85, 0.90
```

Every identity and result here is development-only. `TESTABLE` is necessary, not
sufficient, and nothing is confirmation.

## Closed role-coverage loop

```text
dev       {0.50, 0.75}   testable {}       count 0
pilot     {0.60, 0.85}   testable {}       count 0
val       {0.40, 0.90}   testable {0.40}   count 1
test      {0.35, 0.65}   testable {0.35}   count 1
```

This is the named **role-coverage-bounded non-transfer outcome: no testable structural
training support**. It neither establishes success nor rejects the hypothesis.

Current jointly approved states:

```text
analyzer       blob b7d39538...
tests          blob 04f5d71b...   86 focused tests
artifact       blob fa655083...
packet README  blob b51196c30b909dbf8c89a9704ed2a966d1ae0fa2
```

Source-mutation audits clear `__pycache__` before each case, disable bytecode writes,
run twice, and require identical verdict sets.

## Closed payload-conditioning loop

The zero-rollout read over the closed screen shows that 0.050 kg reduces the structural
signal to about half across the ten-value ladder:

```text
minimum ratio   0.4867076148
mean ratio      0.5054909695
maximum ratio   0.5365918313
```

The exact unmeasured scalar masses are:

```text
pilot-associated       0.025, 0.075 kg
validation-associated  0.100, 0.125 kg
test-associated        0.150, 0.200 kg
```

This is conditioning evidence, not attribution, a pilot, or confirmation. Payload affects
the feasibility boundary and must be measured before Amendment A2 is drafted.

The approved code/result states are:

```text
Reproducibility Packet/scripts/analyze_protocol_p_payload_conditioning.py
  Git blob 39048d2658963a345e3a46949a6070d421a155d9

Reproducibility Packet/tests/test_protocol_p_payload_conditioning.py
  Git blob b9e81f6320e1a3b68f952d631795f1d82abca5ff
  focused tests 105

Reproducibility Packet/results/protocol_p/payload_conditioning.json
  Git blob c11f70673b043ea634481d47ad4137365c0cd12e
  canonical document SHA-256
  47ec3571bf207f428c1eb376cfdf7b3f673a94729fa649ba845bca27299d97d1
```

`47ec3571...` and the role-coverage document digest are canonical text/document
digests, not raw-checkout digests.

## Current open loop — payload-boundary extension v0.2

Claude Session 62 accepted every Session-61 blocker, superseded v0.1 with v0.2, and
explicitly approved its handoff state. Codex Session 62 found further connected
executability/authority defects, directly edited the document under the review-cycle
playbook, and explicitly approved this exact reviewer state:

```text
Reproducibility Packet/protocol/payload-boundary-extension-v0.2.md
canonical SHA-256  e5192eaacef004469cfba5bcc4ff7da692e6fb828e5c33a7a2be5d8976a11a52
Git blob          3d72e1f468f30dfea7101181558720853202f293
bytes             69,428
content lines     1,257
line endings      LF
Codex             EXPLICITLY APPROVES this exact state
Claude            owner re-review of this exact state NOT YET STATED
loop              OPEN on Claude owner re-review
```

Until Claude genuinely re-opens and explicitly approves that digest, **Step 2 is not
authorized**. No seam build, `PhysicalKey` edit, executable, plan mode, replay,
payload-boundary rollout, or Amendment A2 may start.

### Load-bearing reviewer corrections

1. **No circular provenance.** The identity payload contains the five non-provenance
   override inputs. `ScreenOverrides.provenance_hash` is derived from that canonical
   payload and inserted only afterwards.
2. **Plan and replay are separate gates.** Plan mode runs X0P at zero rollouts and
   persists pass or failure. Execute mode, only after authorization naming the plan,
   runs `X0E -> XR -> XA -> XM-C -> XL -> XM-B -> XZ`.
3. **The anchor does not prove the new payload field.** Its source reservation already
   carries 0.050 kg. The anchor checks the rebuilt probe/fault/identity instrument; X8
   is the sole payload-liveness check.
4. **Payload liveness precedes non-anchor ladders.** All six non-anchor healthy blocks
   run first; X8 compares seven masses within each of eight CRN identity classes; only
   then may a non-anchor ladder run.
5. **Replay is outside the extension ledger.** Replay stamps the base hash and is
   recorded under `replay_gate`; explicit extension/replay/total counts preserve its
   physical cost.
6. **Logical joins are persisted data.** Ladder rows cite fault and healthy keys; null
   distances cite both endpoint keys. The full plan is 126 extension rollouts, one
   replay, eight identities, and 532 logical references.
7. **Reduced coverage has no A2 authority.** Unsafe non-anchor masses may be preserved
   as scoped partial evidence, but any exclusion yields
   `X_REDUCED_MASS_COVERAGE` before shape/case rules and licenses no Option A/B/C.
8. **Invalid statistics are explicit.** `X_INVALID_MEASUREMENT` catches invalid
   windows, time shapes, finite-sample counts, coefficients, distances, or thresholds.
9. **Option B uses an initial role-retaining mass prefix.** A heavier split-specific
   role regain cannot repair a lighter role loss.
10. **The split grid stays out of the executable.** The executable consumes pinned role
    literals; a focused test is the sole reader that asserts equality to
    `fault_grid_by_split`.

### Accepted design judgments

- CRN across masses is appropriate. Per-mass nulls still use eight identities; the
  cross-mass nulls are matched and no inference treats them as independent.
- `PhysicalKey.distal_payload_mass_kg` is necessary to stop silent cross-mass reuse.
- The nine-rung anchor is accepted. The partition is identical for every
  `tau_anchor` in `(0.021, 0.196)`; the excluded 0.50 rung lies only 2.1% of its
  threshold from the screen boundary.
- Safe partial evidence may continue to be collected after a non-anchor exclusion, but
  the aggregate decision remains non-authoritative.

## Codex Session-62 verification

```text
source reservation        scenario_dev_t01_f000_r02
source payload            0.050 kg
role map                  dev .50/.75; pilot .60/.85; val .40/.90; test .35/.65
planned extension keys    126 / 126 distinct with mass
CRN identities            8
full logical references   532
monotone prefix states    19,448 / 19,448 classified exactly once
role-lost states with no
  valid Option-B cap      330
gravity                   [0, 0, 0]
qfrc_bias                 exactly zero at the initial state
nominal body mass         0.17280000257492067 kg
declared mass deltas      exact within atol 1e-12
cell-6 margins            reproduced from stage_abc_screen.json
full packet suite         1,126 passed in 124.04 s
physical rollouts spent   0
plan mode run             no
config/config.json        absent
```

The first pytest invocation was interrupted by an overly short tool timeout and emitted
an output-stream error; it was not a test failure. The clean full rerun above passed.

## Physical-run accounting

Protocol-P-related physical executions remain **151**: fifteen before Session 57, one
Codex replay, and the 135-rollout Stage-A/B/C screen. Sessions 58–62 spent zero
rollouts. Keep physical executions separate from logical rows and provenance references.

The payload-boundary extension's *planned* maximum is 126 extension rollouts plus one
replay, but none has been authorized or spent.

## Next actions

1. Claude genuinely re-reviews Codex's document edits at canonical `e5192eaa...`.
2. If Claude approves that exact state, the document loop closes and **only** the
   Step-2 build/review becomes authorized.
3. Build and exact-state review the additive `ScreenOverrides` mass field, additive
   `PhysicalKey` mass field, and the new executable. Run the corrected two-pass
   mutation sweep.
4. After both agents approve the executable, run **plan mode only** (X0P, zero
   rollouts), and both agents read the plan artifact.
5. Issue a separate explicit execution decision naming the plan's canonical digest and
   authorizing the one-row replay. Until then: zero rollouts.
6. Execute once only after that decision; both agents read the result.
7. Draft Amendment A2 only after the approved result is jointly interpreted.

Keep `config.json` absent. Assignment/config lineage, regeneration, Gates 4–7, and
confirmatory materialization remain blocked.

## Standing evidence rules

- Same-state approval is explicit. Creation, edits, handoff, downstream use, and silence
  are not approval.
- Development screens, pilots, fixtures, diagnostics, and mechanics probes remain
  separate from frozen, confirmatory, and final results.
- Keep detection, attribution, information/action authorization, and control outcome
  separate.
- Never use bare `python` or `pip`; use `./venv` against
  `Reproducibility Packet/tests` and never root-wide `pytest -q`.
- Source-mutation tests clear `__pycache__`, disable bytecode writes, run twice, and
  return identical verdict sets.
- Transcript appends use the hard gate: exact UTF-8 physical tail/line count/hash,
  verified unique complete EOF anchor, byte-identical old prefix, one new header after
  the boundary, and additions-only diff.
- The root Live-Run README is append-only during Phase 2. Preserve settled history and
  add only lean forward corrections or genuine public milestones.

## Transcript state

The authoritative active thread is:

`chats/Claude-Codex/Phase 2 Integration and Config Freeze/Phase 2 Integration and Config Freeze - Active.md`

Codex Session 62 is physically last. Its append preserved the pre-write 1,074,068 bytes
and 16,064 content lines as a byte-identical prefix, placed the unique header at line
16,068, and produced transcript diff `+95/-0`.

## Closeout numbering

- Next Codex session/report: **63** / `HumanReport63.md`.
- Next regular Codex progress report: **Session 64**, unless an approved amendment or
  phase transition triggers one sooner.
