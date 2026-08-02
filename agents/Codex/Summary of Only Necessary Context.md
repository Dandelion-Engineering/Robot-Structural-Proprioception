# Summary of Only Necessary Context — Codex

**Last rewritten:** 2026-08-02 — Codex Session 61

## Resume here

The project is in **Phase 2 — Execution**. The final configuration is **UNFROZEN**;
`Reproducibility Packet/config/config.json` does not exist. Confirmatory test identities
and payloads remain unmaterialized.

Protocol P v2.3.3, its one-row replay, Stage 0, the Stage-A/B/C executable and executed
Case-B result, the Section-9 role-coverage read, and the zero-rollout payload-conditioning
read are jointly approved and closed. Do not edit or re-run those measurements without a
new explicit decision.

The executed Stage-A/B/C result remains:

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

All identities are development identities. `TESTABLE` is necessary, not sufficient,
and this result is not confirmation.

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

Source-mutation audits must clear `__pycache__` before each case, disable bytecode
writes, run twice, and return identical verdict sets.

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

Claude Session 61 explicitly approved Codex's corrected result and independently
reproduced the exact-mass and arithmetic/verdict-coherence findings. Claude then added
mutation-backed tests for a truthy non-boolean hard-gate field and three colliding refusal
sentences. Codex Session 61 approved Claude's handed-back exact states, closing the loop:

```text
Reproducibility Packet/scripts/analyze_protocol_p_payload_conditioning.py
  Git blob 39048d2658963a345e3a46949a6070d421a155d9

Reproducibility Packet/tests/test_protocol_p_payload_conditioning.py
  Git blob b9e81f6320e1a3b68f952d631795f1d82abca5ff
  focused tests 105

Reproducibility Packet/results/protocol_p/payload_conditioning.json
  unchanged Git blob c11f70673b043ea634481d47ad4137365c0cd12e
  canonical text/document SHA-256
  47ec3571bf207f428c1eb376cfdf7b3f673a94729fa649ba845bca27299d97d1
```

`47ec3571...` is the canonical document digest, not a raw-checkout digest. A fresh
Windows checkout can render CRLF and have a different raw hash. No narrow
`.gitattributes` pin was added; qualify payload and role-coverage JSON digests by
canonical text domain from here forward.

## Current open loop — payload-boundary extension

Claude Session 61 drafted:

```text
Reproducibility Packet/protocol/payload-boundary-extension-v0.1.md
canonical SHA-256 32a0393069615e18d1249ec2ac95526eb188092fcccf596be24ce60ac9bea475
Git blob          903962f8ba31b887764c13e718fe0f92fde0b7a9
Claude            explicit owner approval of this draft NOT STATED
Codex             BLOCKS this exact state
loop              OPEN on Claude revision
```

The direction remains accepted: separate versioned development-only measurement; all six
unmeasured masses; a 0.050 kg control anchor; fixed ten-severity ladder; fixed dev
environment/contact/trajectory/probe; additive payload override; private identities;
honest physical/logical counts; and separate document, executable, plan, and execution
authorization gates.

### Blocker 1 — identity-confounded mass comparison

The draft says payload is the only factor moving, but its `sensor_seed` and `pair_id`
both depend on mass index `m`. Sensor RNG and the C0-driven control path depend on that
identity, so mass and sensor identity move together. The comparison is not payload-only.

Invariant X8 is therefore ineffective: healthy coefficient vectors can stay pairwise
distinct under a dead payload override solely because their sensor identities differ.

Revision requirement: pin an explicit CRN design across masses, preferably one sensor
identity per null replicate `k` shared across all masses, with provenance unique through
mass/stage/condition. Replace the blanket no-identity-collision rule with exact allowed
matching equivalence classes.

### Blocker 2 — incomplete outcome classifier

Cases 1–4 are not exhaustive. The draft omits the exact role-severity lookup, leaves
mass non-monotonicity mathematically undefined, assumes a prefix-shaped within-mass
`TESTABLE_SET` without guarding it, and gives contradictory terminal behavior for
`X_UNSAFE_LADDER_VALUE` and `X_UNSAFE_MASS`.

Revision requirement: one ordered, mutually exclusive, exhaustive classifier with exact
mass ordering/monotonicity, these role sets—
`dev {0.50,0.75}`, `pilot {0.60,0.85}`, `val {0.40,0.90}`,
`test {0.35,0.65}`—plus non-prefix handling and explicit stop/continue/report behavior
on every unsafe/invalid path.

### Blocker 3 — provenance, replay, and persistence not executable

Stage X0 points to a Section-11 plan artifact, but Section 11 contains only cost. No
plan/result/terminal path or schema is named. The `dev-` provenance hash has no exact
identity payload/canonical-string definition. The 0.050 kg anchor is a new-identity
positive control, not the requested default-path replay after changing an approved seam.

Revision requirement: pin exact per-rollout provenance payload fields and canonical
strings; exact plan/result/terminal paths, serialization and required fields; every-exit
persistence; and a pinned one-row `overrides=None` replay or comparably exact
default-path reproduction gate with physical cost and failure branch.

### Blocker 4 — anchor cost not staged

The anchor is terminal but the draft permits all seven masses to run before reading it.
Run/persist the 0.050 kg anchor first and open the other six only on pass. State terminal
and maximum costs, including the replay gate.

No seam implementation, plan-mode run, physical rollout, or Amendment A2 draft is
authorized from v0.1.

## Verification from Codex Session 61

```text
focused payload-conditioning tests     105 passed in 0.69 s
full packet suite                     1,126 passed in 121.48 s
compileall analyzer                      clean
fresh artifact derivation                byte-identical
physical rollouts spent                   0
config/config.json                        absent
```

The active Phase-2 transcript is authoritative:

`chats/Claude-Codex/Phase 2 Integration and Config Freeze/Phase 2 Integration and Config Freeze - Active.md`

Codex Session 61 is physically last. Its append preserved the pre-write 1,050,779 bytes
and 15,662 content lines as a byte-identical prefix, placed the unique header at line
15,664, and produced transcript diff `+146/-0`.

## Physical-run accounting

Protocol-P-related physical executions remain **151**: fifteen before Session 57, one
Codex replay, and the 135-rollout authorized Stage-A/B/C screen. Sessions 58–61 spent
zero rollouts. Keep physical executions separate from logical rows and provenance
references.

## Next actions

1. Claude revises the payload-boundary extension against all four blocker groups and
   hands back one exact canonical digest.
2. Codex reviews that exact document. Approval will authorize only the later seam and
   executable build/review, not execution.
3. After document approval, build/review the payload seam and executable at exact blobs,
   including the corrected two-pass mutation sweep.
4. Run plan mode only after executable approval; both agents read the plan artifact.
5. Issue a separate explicit execution decision naming the plan digest. Until then:
   zero rollouts.
6. Draft Amendment A2 only after an approved extension has run and both agents have read
   the result.

Keep `config.json` absent. Assignment/config lineage, regeneration, Gates 4–7, and
confirmatory materialization remain blocked.

## Standing evidence rules

- Same-state approval is explicit. Creation, edits, handoff, downstream use and silence
  are not approval.
- Development screens, pilots, fixtures and diagnostics remain separate from frozen,
  confirmatory and final results.
- Keep detection, attribution, information/action authorization and control outcome
  separate.
- Never use bare `python` or `pip`; use `./venv` against
  `Reproducibility Packet/tests` and never root-wide `pytest -q`.
- Source-mutation tests must clear `__pycache__`, disable bytecode writes, run twice,
  and return identical verdict sets.
- Transcript appends use the hard gate: exact UTF-8 physical tail/line count/hash,
  verified unique complete EOF anchor, byte-identical old prefix, one new header after
  the boundary, and additions-only diff.
- The root Live-Run README is append-only during Phase 2. Preserve settled history and
  add only lean forward corrections or genuine public milestones.

## Closeout numbering

- Next Codex session/report: **62** / `HumanReport62.md`.
- Next regular Codex progress report: **Session 64**, unless an approved amendment or
  phase transition triggers one sooner.
