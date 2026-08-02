# Summary of Only Necessary Context — Codex

**Last rewritten:** 2026-08-02 — Codex Session 59

## Resume here

The project is in **Phase 2 — Execution**. The final configuration is **UNFROZEN** and
`Reproducibility Packet/config/config.json` does not exist. The confirmatory test split
remains untouched at zero identities and zero payloads.

Protocol P Stages A/B/C ran once under joint authorization in Codex Session 57. The exact
measurement is jointly approved and closed; do not re-run it:

```text
Reproducibility Packet/results/protocol_p/stage_abc_screen.json
  git blob          209a87ae5daa171016d566e07ed14c7c71ef0f18
  tracked-document
    SHA-256         e800ae6c05c0dda0db82e2c94ab6350cd7d9e0bf544a9659fdacf2bad53999fc
    bytes           588,448 LF bytes in Git
  Windows checkout
    raw SHA-256     c48c2e4d3a8a84a5b10127afc2a7c0f4bacc0ae6290712546432058327008756
    bytes           599,841 CRLF bytes
  loop              CLOSED — Claude and Codex both approved blob 209a87ae...
```

The run selected **0.10 N / ramp fraction 0.25** and returned bounded **Case B**:

```text
Stage A                75 physical rollouts
Stage B                32
Stage C                28
physical total        135
logical rows          147 = 135 physical + 12 reuses
rollout elapsed       4,432.155710699968 s
terminal              None
outcome               CASE_B
unsafe Stage B/C      none

TESTABLE              remaining EI 0.35, 0.40, 0.45 in all four cells
SUB_THRESHOLD         0.50, 0.55, 0.60, 0.65, 0.75, 0.85, 0.90
```

Every identity remains `dev-`; the matched-signal / unmatched-null comparison favours S;
`TESTABLE` is necessary, not sufficient; this result is not confirmation.

## Section-9 role coverage — technically approved, owner sentence still required

Protocol P Section 9 requires a zero-rollout role-coverage read over the ladder and the
approved split assignment. The exact measured counts are:

```text
dev       {0.50, 0.75}   testable {}       count 0
pilot     {0.60, 0.85}   testable {}       count 0
val       {0.40, 0.90}   testable {0.40}   count 1
test      {0.35, 0.65}   testable {0.35}   count 1
```

Dev at zero triggers the named **role-coverage-bounded non-transfer outcome: no testable
structural training support**. Zero pilot disables data-driven downsizing and retains the
maximum prospective test replication. Val/test count one are thin single-severity roles.
The S/C1 secondary remains reportable; the outcome establishes neither success nor
hypothesis failure.

Claude Session 58 created the analyzer. Codex Session 58 blocked its original exact state
on three reproduced binding/verdict/split failures and returned a corrected state. Claude
Session 59 confirmed all three, then found that Codex's repair hashed the tracked screen
result through the raw binary-domain helper. That recorded the current Windows checkout,
not the document, and made the derived artifact differ on an LF clone. Claude corrected
the provenance to canonical tracked-text SHA-256 and added tests for the digest plus twelve
previously untested guards.

Current exact states:

```text
Reproducibility Packet/scripts/analyze_protocol_p_role_coverage.py
  blob f911f2f38a4917cc898abf6c0d2a063cfce33842

Reproducibility Packet/tests/test_protocol_p_role_coverage.py
  blob 83c7d6403d218be6d073a39b603ebf73afb45186
  tests 46

Reproducibility Packet/results/protocol_p/role_coverage.json
  blob   6d6d23b9a42baaf81ec558fd21c6bc1148aa6890
  SHA-256 faf66a2aad451c5fb4be13c47f8416f55825925d6a71d8fc334d6f015ab45dbd

Reproducibility Packet/README.md
  blob 4da55bf44eb58036f94ab4e215703106a2f5852f

Codex     EXPLICITLY APPROVED all four in Session 59
Claude    explicit owner approval of these current states NOT STATED
loop      OPEN on the owner sentence only
```

Do not infer Claude approval from the phrases “I corrected the state directly and hand it
back” or “State handed back.” The review-cycle playbook says edits and handoffs are not
approval. Written Amendment A2 remains blocked until Claude explicitly approves the four
current blobs or edits and returns a new state.

## Session-59 portability ruling

Codex independently ran the analyzer against LF and CRLF copies of the screen result. The
two generated artifacts were byte-identical and matched the tracked artifact exactly.
Codex also independently hashed Git's stored screen bytes and reproduced `e800ae6c...`.

Do **not** add a broad `Reproducibility Packet/results/**/*.json eol=lf` rule now. The
canonical document digest fixes portability without changing the closed measurement. A
broad pin would change the checkout rendering of the jointly approved screen result and
make historical `c48c2e4d...` raw-working-tree references impossible to reproduce under
the new checkout rule. Carry `e800ae6c...` as the document digest; qualify
`c48c2e4d...` forward as the CRLF working-tree rendering. A prospective EOL policy can be
considered later.

## Closed supporting review loops

```text
agents/Claude/Progress Reports/Progress Report Session 56.md
  blob 83c527ced4e12ce27cfbf83601c89fc0e670a3cd
  Claude and Codex explicitly approved; loop CLOSED at round five

root README order-correction entry
  Codex approved blob 833040e...; Claude explicitly approved the entry
  Claude later appended a new 2026-08-02 milestone without changing it; loop CLOSED

packet README diagnostic-pause sentence
  both agents explicitly approved blob 17c91d3...
  current packet README blob 4da55bf... adds only the role-coverage determinism sentence
```

All four Stage-C cells set `diagnostic_pause: true`; their `Q95_c` values range
0.3703–0.4277 microstrain, above the 0.30 trigger. The protocol gives this flag no
authority over the ladder verdict or outcome case.

## Physical-run accounting

Primary Session-39 records show Claude and Codex independently spent one replay each. The
pre-Session-57 total is fifteen:

```text
Claude S39  1
Codex  S39  1
Claude S40  1
Claude S41  5
Claude S45  2
Codex  S45  2
Claude S46  2
Claude S51  1
            --
            15

Codex S57 replay + screen = 1 + 135
current Protocol-P-related total = 151
```

Earlier dated reports/public entries are not rewritten. The newest public milestones
correct fourteen/150 forward to fifteen/151. Claude Session 59 also corrected Codex's
test-count correction: Claude's committed Session-58 blob had 24 tests, not 22; the chat
was stale and Claude's report was right.

## Verification from Codex Session 59

```text
focused role-coverage tests       46 passed in 0.33 s
full packet suite              1,021 passed in 121.47 s
compileall                        clean
LF vs CRLF derived artifact       byte-identical
fresh derivation vs tracked       byte-identical
canonical digest vs Git bytes     exact
role counts                        0 / 0 / 1 / 1 unchanged
rollouts spent                     0
config/config.json                absent
```

The authoritative live record is:

`chats/Claude-Codex/Phase 2 Integration and Config Freeze/Phase 2 Integration and Config Freeze - Active.md`

Codex Session 59 is physically last. Its append preserved the complete 1,010,796-byte /
14,914-line Claude Session-59 state as a byte-identical prefix, placed a unique header at
line 14,918, and produced transcript diff `+75/-0`.

## Protocol-P state

Jointly approved and closed:

- Protocol P v2.3.3 at canonical digest
  `5689dad7ce4194b9a7dbe381006027df178997adf732f5734a77ef048bdf421f`;
- permanent I13b step-499/step-500 test;
- generator `ScreenOverrides` seam;
- replay-gate implementation and one-row exact result;
- Stage-0 implementation and result artifact;
- shared primitives and Stage-A/B/C construction layer;
- Stage-A/B/C results layer and driver; and
- exact Stage-A/B/C executed result blob `209a87ae...`.

Open:

- Claude's explicit owner approval of the four current role-coverage/packet blobs;
- written Amendment A2 only after that loop closes;
- replacement assignment/config lineage and coherent regeneration;
- Gates 4–7 and joint final config approval; and
- only then one-shot confirmatory generation/evaluation.

## Next actions

1. Claude explicitly approves blobs `f911f2f...`, `83c7d64...`, `6d6d23b...` and
   `4da55bf...` if accepted unchanged. That one sentence closes the current loop.
2. After closure, write Amendment A2 against both Case B and the 0/0/1/1 role counts; do
   not change assignment/config lineage before amendment review.
3. Produce the replacement assignment and coherently regenerate the superseded 3.9-GB
   development/pilot/validation dataset from zero.
4. Resume Gate-4 estimator/controller roles and Gates 5–7 only after lineage approval.
5. Keep `config.json` absent and the confirmatory split untouched until joint final freeze.

## Standing evidence rules

- Same-state approval is explicit. Creation, edits, handoff, downstream use and silence
  are not approval.
- Development screens, pilots, fixtures and diagnostics remain separate from frozen,
  confirmatory and final results.
- Keep physical rollout accounting separate from logical rows and provenance references.
- Keep detection, attribution, information/action authorization and control outcome
  separate.
- Do not re-run Stage 0 or Stage A/B/C without a new explicit decision.
- Use `./venv` against `Reproducibility Packet/tests`; never root-wide `pytest -q`.
- Never use bare `python` or `pip`.
- The confirmatory test split remains untouched: zero identities, zero payloads.
- Transcript appends use the hard gate: exact UTF-8 physical tail/line count/hash, verified
  unique complete EOF anchor, byte-identical old prefix, one new header after the boundary,
  and additions-only diff.
- The root Live-Run README is append-only while Phase 2 remains live; corrections propagate
  forward and dated entries are never edited.

## Closeout numbering

- Next Codex session: **60**.
- Next Codex human report: `agents/Codex/Session Summaries/HumanReport60.md`.
- Next regular Codex progress report: **Session 64**, unless a phase transition or approved
  amendment triggers one sooner.
