# Summary of Only Necessary Context — Codex

**Last rewritten:** 2026-08-02 — Codex Session 60

## Resume here

The project is in **Phase 2 — Execution**. The final configuration is **UNFROZEN**;
`Reproducibility Packet/config/config.json` does not exist. The confirmatory test split
remains untouched at zero identities and zero payloads.

Protocol P v2.3.3, its one-row replay, Stage 0, the Stage-A/B/C implementation and
executed Case-B result, and the Section-9 role-coverage read are jointly approved and
closed. Do not edit or re-run those measurements without a new explicit decision.

The executed Stage-A/B/C result remains:

```text
artifact             Reproducibility Packet/results/protocol_p/stage_abc_screen.json
Git blob             209a87ae5daa171016d566e07ed14c7c71ef0f18
selected candidate   0.10 N / ramp fraction 0.25
physical rollouts    135 = 75 Stage A + 32 Stage B + 28 Stage C
logical rows         147 = 135 physical + 12 reuses
outcome              CASE_B
TESTABLE              remaining EI 0.35, 0.40, 0.45 in all four cells
SUB_THRESHOLD         0.50, 0.55, 0.60, 0.65, 0.75, 0.85, 0.90
```

All identities are development identities. `TESTABLE` is necessary, not sufficient, and
this result is not confirmation.

## Latest closed loop — role coverage

The zero-rollout Section-9 role read remains:

```text
dev       {0.50, 0.75}   testable {}       count 0
pilot     {0.60, 0.85}   testable {}       count 0
val       {0.40, 0.90}   testable {0.40}   count 1
test      {0.35, 0.65}   testable {0.35}   count 1
```

This is the named **role-coverage-bounded non-transfer outcome: no testable structural
training support**. It neither establishes success nor rejects the project hypothesis.

Claude Session 60 explicitly approved the four exact states returned by Codex Session 59,
closing that review loop. Claude then hardened the mutation audit after reproducing stale
same-size/same-second imports from `__pycache__`. The corrected harness clears the cache
before each case and sets `PYTHONDONTWRITEBYTECODE=1`; it caught all 28 source mutations.
Keep that isolation rule for all future source-mutation audits.

Current role-coverage states:

```text
analyzer       blob b7d39538...
tests          blob 04f5d71b...   86 focused tests
artifact       blob fa655083...
packet README  blob b51196c30b909dbf8c89a9704ed2a966d1ae0fa2
loop           CLOSED
```

## Current open loop — payload conditioning

Claude Session 60 created a zero-rollout read comparing the 0 kg and 0.05 kg payload rows
already present in the closed Stage-A/B/C result. The measured 50 g payload reduces the
structural signal to about half across the ladder:

```text
minimum ratio   0.4867076148
mean ratio      0.5054909695
maximum ratio   0.5365918313
```

Payload therefore affects the feasibility boundary and must be measured before Amendment
A2 is written. This is a conditioning result, not an attribution result, a pilot, or a
confirmatory result.

Codex Session 60 blocked Claude's original payload exact state on two reproduced defects:

1. the analyzer treated the pilot payload range as continuously screened and omitted the
   exact unmeasured 0.025 kg reserved pilot mass; and
2. duplicated margin and verdict fields were trusted without checking their arithmetic and
   logical coherence.

Codex corrected those defects, added eight adversarial tests, and regenerated the artifact
without rollouts. The exact unmeasured reserved-role masses are now:

```text
pilot       0.025, 0.075 kg
validation  0.100, 0.125 kg
test        0.150, 0.200 kg
```

Reviewer-edited exact state:

```text
Reproducibility Packet/scripts/analyze_protocol_p_payload_conditioning.py
  Git blob 7f9ed558fe173a7ec859a3335eeb6a5989fb5a3e

Reproducibility Packet/tests/test_protocol_p_payload_conditioning.py
  Git blob 6fc5f158921f67e4eeb24a9d5c4165d0cf0047eb
  tests 94

Reproducibility Packet/results/protocol_p/payload_conditioning.json
  Git blob c11f70673b043ea634481d47ad4137365c0cd12e
  SHA-256 47ec3571bf207f428c1eb376cfdf7b3f673a94729fa649ba845bca27299d97d1

Codex     EXPLICITLY APPROVED these three states
Claude    explicit owner approval of these reviewer-edited states NOT STATED
loop      OPEN on Claude same-state review
```

The packet README (`b51196c...`) and root README (`9d1cae71...`) remain unchanged and are
approved as accurate. Do not infer Claude approval of Codex's three edited blobs from their
creation, downstream use, or handoff.

## Payload-boundary measurement ruling

**Measure first, but do not execute yet.** The measurement must not revise or re-open the
closed Protocol P v2.3.3 execution. It needs a separate, versioned, development-only
pre-registration with a new private development identity and seed band.

Claude's initial five-mass / 50-rollout sketch is not execution-ready. Six exact reserved
masses remain unmeasured, and one structural severity at each mass cannot locate the joint
payload/severity boundary. Before any execution decision, the new protocol must pin:

- all six exact masses: 0.025, 0.075, 0.10, 0.125, 0.15, and 0.20 kg;
- development-only construction that does not materialize pilot, validation, or test
  identities, labels, manifests, or outcome payloads;
- a predeclared severity ladder or exact adaptive bracketing branches and stop rules;
- logical versus physical counts, provenance, replay, persistence, safety, and terminal
  behavior; and
- a zero-rollout plan review followed by separate explicit execution authorization.

No rollout is authorized. Amendment A2 text, replacement assignment/config lineage,
regeneration, Gates 4–7, and confirmation remain blocked.

## Verification from Codex Session 60

```text
focused payload-conditioning tests     94 passed in 0.74 s
full packet suite                    1,115 passed in 121.83 s
compileall                              clean
LF vs CRLF derived artifact             byte-identical
fresh derivation vs tracked artifact     byte-identical
physical rollouts spent                 0
config/config.json                      absent
```

The active Phase-2 transcript is authoritative:

`chats/Claude-Codex/Phase 2 Integration and Config Freeze/Phase 2 Integration and Config Freeze - Active.md`

Codex Session 60 is physically last. Its append preserved the pre-write 1,030,187 bytes and
15,270 content lines as a byte-identical prefix, placed the unique new header after that
boundary, and produced transcript diff `+150/-0`.

## Physical-run accounting

Protocol-P-related physical executions remain **151**: fifteen before Session 57, then one
Codex replay plus the 135-rollout authorized screen. Sessions 58–60 spent zero rollouts.
Keep physical executions separate from logical rows and provenance references.

## Next actions

1. Claude explicitly approves payload blobs `7f9ed558...`, `6fc5f158...`, and `c11f7067...`
   if accepted unchanged. That sentence closes the current exact-state loop.
2. After closure, Claude drafts the separate development-only payload-boundary protocol
   with all six masses and the safeguards above. Do not draft Amendment A2 yet.
3. Review that zero-rollout protocol at the exact-state bar.
4. Only after protocol approval, make a separate explicit execute/do-not-execute decision.
5. Keep `config.json` absent and all reserved/confirmatory identities and payloads untouched.

## Standing evidence rules

- Same-state approval is explicit. Creation, edits, handoff, downstream use and silence are
  not approval.
- Development screens, pilots, fixtures and diagnostics remain separate from frozen,
  confirmatory and final results.
- Keep detection, attribution, information/action authorization and control outcome
  separate.
- Never use bare `python` or `pip`; use `./venv` against `Reproducibility Packet/tests` and
  never root-wide `pytest -q`.
- Source-mutation tests must clear `__pycache__` before every mutation, disable bytecode
  writes for imports, run twice, and return identical verdict sets.
- Transcript appends use the hard gate: exact UTF-8 physical tail/line count/hash, verified
  unique complete EOF anchor, byte-identical old prefix, one new header after the boundary,
  and additions-only diff.
- The root Live-Run README is append-only during Phase 2. Preserve settled history and add
  only lean forward corrections or real milestones.

## Closeout numbering

- Next Codex session: **61**.
- Next Codex human report: `agents/Codex/Session Summaries/HumanReport61.md`.
- Next regular Codex progress report: **Session 64**, unless an approved amendment or phase
  transition triggers one sooner.
