# Summary of Only Necessary Context — Codex

**Last rewritten:** 2026-08-02 — Codex Session 58

## Resume here

The project is in **Phase 2 — Execution**. The final configuration is **UNFROZEN** and
`Reproducibility Packet/config/config.json` does not exist. The confirmatory test split
remains untouched at zero identities and zero payloads.

Protocol P Stages A/B/C ran once under joint authorization in Codex Session 57. The exact
result is now jointly approved and closed:

```text
Reproducibility Packet/results/protocol_p/stage_abc_screen.json
  git blob   209a87ae5daa171016d566e07ed14c7c71ef0f18
  SHA-256    c48c2e4d3a8a84a5b10127afc2a7c0f4bacc0ae6290712546432058327008756
  bytes      599,841
  Codex      APPROVED (Session 57)
  Claude     APPROVED (Session 58)
  loop       CLOSED — do not re-run
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

## Section-9 role coverage — accepted science, edited implementation under review

Claude Session 58 found that Protocol P Section 9 pre-registered a role-coverage read that
the approved screen driver/results layer never implemented. The ladder is exactly the
union of each split's known-class structural severities plus OOD 0.45/0.55, so the result
already determines the count at zero rollout cost:

```text
dev       {0.50, 0.75}   testable {}       count 0
pilot     {0.60, 0.85}   testable {}       count 0
val       {0.40, 0.90}   testable {0.40}   count 1
test      {0.35, 0.65}   testable {0.35}   count 1
```

Codex agrees this read belongs to the screen now, not Gate 7. Dev at zero triggers the
named **role-coverage-bounded non-transfer outcome: no testable structural training
support**. Zero pilot disables data-driven downsizing and retains the maximum prospective
test replication. Val/test count one are thin single-severity roles. The secondary remains
reportable; the outcome establishes neither success nor hypothesis failure.

Claude's original analyzer output had the correct 0/0/1/1 result but its exact executable
state was blocked in Codex Session 58. Three reproduced failures were decision-bearing:

1. a different split assignment with the same ladder union changed the named consequence
   while the output still reported the approved assignment hash;
2. an unknown ladder verdict silently behaved as not testable; and
3. a missing dev split silently cleared the zero-dev outcome.

Codex corrected those failures plus strict-JSON, finite-value, verdict/case consistency,
and exact tracked-input digest guards. Current reviewer-edited states:

```text
Reproducibility Packet/scripts/analyze_protocol_p_role_coverage.py
  blob 980397ad2de7b044a6691b31881c79774b9736db

Reproducibility Packet/tests/test_protocol_p_role_coverage.py
  blob a7e317b1aaa59742264678ccc25280c92eeb3ad2
  31 focused tests

Reproducibility Packet/results/protocol_p/role_coverage.json
  blob   c97e794eb93ecad7298bdb34edb76b9f85404460
  SHA-256 f54d6c3aa59994adcca2e9a088e8e5c591df123e72461f93de8e8f58d9fbe1ed
  result 0/0/1/1 unchanged; rollouts_spent 0

Codex     APPROVED
Claude    OWNER RE-REVIEW REQUIRED
```

The artifact now records the exact Stage-A/B/C result SHA-256 and proves the tracked
assignment/protocol state it joins. Claude's completed `HumanReport58.md` says 24 focused
tests, but the committed handoff had 22; the reviewer-edited state has 31. This was
corrected forward in the live transcript, not by rewriting Claude's completed report.

## Other open exact review states

```text
Reproducibility Packet/README.md
  blob 17c91d3e3c323e11fe316d825687e79de195b990
  role-coverage Step-25 addition retained
  Codex added four-cell diagnostic-pause clause
  Codex approved; Claude owner re-review required

root README.md
  blob 833040e9a6d23a5b0399021cd1917da632878f34
  Claude's role-coverage/cost/readback milestone retained
  Codex appended running-log order correction; no dated entry edited
  Codex approved; Claude owner re-review required

agents/Claude/Progress Reports/Progress Report Session 56.md
  blob 83c527ced4e12ce27cfbf83601c89fc0e670a3cd
  fifteen pre-Session-57 physical runs
  Codex approved unchanged
  Claude must explicitly approve exact blob; edited handoff did not do so
```

All four Stage-C cells set `diagnostic_pause: true`; their `Q95_c` values range
0.3703–0.4277 microstrain, above the 0.30 trigger. The protocol gives this flag no
authority over the ladder verdict or outcome case. Packet Step 25 now states that boundary.

## Physical-run accounting

Primary Session-39 records show Claude and Codex independently spent one replay each. The
pre-Session-57 total is therefore fifteen:

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

Earlier dated reports/public entries are not rewritten. The newest public milestone
corrects fourteen/150 forward to fifteen/151.

## Verification from Session 58

```text
focused role-coverage tests       31 passed in 0.24 s
full packet suite              1,006 passed in 122.47 s
compileall                        clean
wrong-assignment repro            refused after correction
unknown-verdict repro             refused after correction
missing-dev repro                 refused after correction
role counts                        0 / 0 / 1 / 1 unchanged
rollouts spent                     0
config/config.json                absent
confirmatory identities/payloads   0 / 0
```

The authoritative live record is:

`chats/Claude-Codex/Phase 2 Integration and Config Freeze/Phase 2 Integration and Config Freeze - Active.md`

Codex Session 58 is physically last. Its append preserved the complete 990,381-byte /
14,554-line Claude Session-58 state as a byte-identical prefix, header unique at line
14,558, and transcript diff `+104/-0`.

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

- Claude owner re-review of the corrected role-coverage code/tests/artifact;
- Claude owner re-review of packet README blob `17c91d3...`;
- Claude owner re-review of root README blob `833040e...`;
- Claude explicit same-state approval of Progress Report Session 56 blob `83c527c...`;
- written Amendment A2 only after those loops close;
- replacement assignment/config lineage and coherent regeneration;
- Gates 4–7 and joint final config approval; and
- only then one-shot confirmatory generation/evaluation.

## Next actions

1. Claude genuinely re-reviews the exact reviewer-edited role-coverage script, tests,
   artifact, packet README and root README; approve unchanged or return new exact states.
2. Claude explicitly approves the current Progress Report Session 56 blob if accepted.
3. After all loops close, write Amendment A2 against both Case B and the 0/0/1/1 role
   counts; do not change assignment/config lineage before amendment review.
4. Produce the replacement assignment and coherently regenerate the superseded 3.9-GB
   development/pilot/validation dataset from zero.
5. Resume Gate-4 estimator/controller roles and Gates 5–7 only after lineage approval.
6. Keep `config.json` absent and the confirmatory split untouched until joint final freeze.

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

- Next Codex session: **59**.
- Next Codex human report: `agents/Codex/Session Summaries/HumanReport59.md`.
- Next regular Codex progress report: **Session 64**, unless a phase transition or approved
  amendment triggers one sooner.
