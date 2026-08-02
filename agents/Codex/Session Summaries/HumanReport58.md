# Human Report — Codex Session 58

**Current date and time:** 2026-08-02 02:15 PDT

**Phase:** Phase 2 — Integration and Reproducibility Build

**Session role:** Exact-state owner/reviewer response to Claude Session 58: close the
Stage-A/B/C result loop, review the zero-rollout Section-9 role-coverage analysis,
verify the corrected historical simulation count, and return any edited states under the
explicit review cycle.

**Final config state:** **UNFROZEN**
(`Reproducibility Packet/config/config.json` remains absent)

**Rollouts spent:** **zero.** This session did not execute the replay gate, Stage 0,
Stages A/B/C, or any plant path. The confirmatory test split remains untouched at zero
identities and zero payloads.

## Summary

Claude Session 58 genuinely reviewed Codex's executed Stage-A/B/C result and independently
reconstructed every decision-bearing number from the persisted JSON rather than importing
the producing driver/results layer. Claude explicitly approved the exact result blob
`209a87ae5daa171016d566e07ed14c7c71ef0f18`, the same state Codex approved in Session 57.
That supplies the required two explicit same-state approvals: the result loop is closed and
no rollout needs to be re-spent.

Claude also recovered a required Protocol-P Section-9 read that neither agent had noticed
was missing before execution: count each split's known-class structural severities that
the ladder found `TESTABLE`. The persisted ladder and assignment imply:

```text
dev       0   no testable structural training support
pilot     0   no data-driven downsizing; retain maximum test replication
val       1   thin single-severity role
test      1   thin single-severity role
```

Codex agrees that this is a required output of the screen rather than a later Gate-7
obligation. Dev at zero triggers the pre-registered role-coverage-bounded non-transfer
outcome. It does not invalidate Case B, but Case B alone is incomplete: together they say
the signature is measurable only at damage more severe than every known-class structural
setting reserved for development or pilot. The secondary remains reportable; the outcome
establishes neither success nor hypothesis failure.

The scientific count was right. The handed-off analyzer was not yet an approvable exact
state.

## Exact-state review findings

### 1. The analyzer did not bind the supplied assignment to the screen

The artifact copied `assignment_hash` from the screen but never verified that the passed
assignment document matched it or even carried a valid self-hash. Codex reproduced the
consequence by swapping the dev and test structural grids while preserving the same ten-
value union. The analyzer accepted the document, changed the named consequence from
zero-dev to zero-test, and still reported the original approved assignment hash.

This is decision-bearing provenance failure: the count is a join between the ladder and
the split map, so both exact inputs must be bound.

### 2. Unknown ladder verdicts silently became non-testable

Replacing the 0.35 verdict with `UNRECOGNIZED` was accepted. Because the analyzer counted
only exact `TESTABLE` strings, the unknown value silently behaved like `SUB_THRESHOLD` and
added a zero-test consequence. The verdict vocabulary therefore needed a closed-domain
guard, not only a nonempty-string guard.

### 3. A missing dev split silently cleared the named outcome

Deleting dev and moving its severities into pilot preserved the ladder union. The analyzer
accepted the document, omitted dev from the report, and reported no zero-dev outcome. The
protocol defines exactly four roles; their presence is decision-bearing.

### 4. Two supporting fail-loud claims were weaker than stated

The loader called its input strict JSON but Python's default parser accepts `NaN`,
`Infinity`, and duplicate keys. The analyzer also trusted the screen's declared
`outcome_case` without checking it against the ten verdicts. Both were corrected while the
review loop was open.

## Reviewer edits and approval

Codex edited `analyze_protocol_p_role_coverage.py`, its tests, and regenerated the derived
artifact without executing a rollout. The corrected state now:

- verifies the assignment self-hash and equality to the assignment bound by the screen;
- verifies the approved assignment and protocol canonical digests carried by the screen;
- checks the actual tracked assignment and protocol file digests at CLI time;
- records the exact raw SHA-256 of `stage_abc_screen.json` in `role_coverage.json`;
- requires exactly `dev/pilot/val/test` and exactly two distinct known-class structural
  settings per split;
- requires finite ladder/assignment values, the closed verdict set
  `{TESTABLE, SUB_THRESHOLD}`, and `CASE_A/B/C` consistency;
- rejects duplicate JSON keys and non-finite JSON constants; and
- preserves the exact 0/0/1/1 scientific result and zero-rollout scope.

The original handed-off blobs are blocked:

```text
script    dc0950a483d6f103c990120daeaf0eb1e59713f3
tests     eec5adc9f789b88f2da03102635997de67fa794e
artifact  639e4e45cd648b329cbaec8ae9e44b80b0b56e1b
```

Codex explicitly approves and handed back these exact reviewer-edited states:

```text
script    980397ad2de7b044a6691b31881c79774b9736db
tests     a7e317b1aaa59742264678ccc25280c92eeb3ad2
artifact  c97e794eb93ecad7298bdb34edb76b9f85404460
artifact SHA-256
          f54d6c3aa59994adcca2e9a088e8e5c591df123e72461f93de8e8f58d9fbe1ed
```

Claude must genuinely re-review and explicitly approve these same states before the loop
closes. Claude's completed `HumanReport58.md` says the focused file grew from 22 to 24
tests, but the committed handoff still contains 22 test functions; the reviewer-edited
state contains 31. The correction was recorded forward in the active transcript rather
than rewriting Claude's completed session report.

## Documentation review

Claude's packet Step-25 role-coverage addition is correct. Codex added one omitted
pre-registered result clause: all four Stage-C cells set `diagnostic_pause: true` because
their `Q95_c` values are 0.3703–0.4277 microstrain, above the protocol's 0.30 trigger.
The new sentence explicitly preserves the flag's no-authority boundary. Codex approves
packet README blob `17c91d3e3c323e11fe316d825687e79de195b990` and returned it for
Claude owner re-review.

Claude's new root Live-Run entry was additions-only but landed immediately before the
physically later existing 2026-08-01 Stage-A/B/C result entry. Codex preserved both dated
entries and appended a short order correction at the logical end of the running log. No
dated history was edited. Codex approves root README blob
`833040e9a6d23a5b0399021cd1917da632878f34` and returned it for owner re-review.

## Historical rollout accounting

Codex re-read both primary Session-39 reports. Claude's report records one from-scratch
development replay; Codex's independent Session-39 report records a separate 26.971-second
replay. The pre-Session-57 total is therefore fifteen, not fourteen:

```text
Claude S39   1
Codex  S39   1
Claude S40   1
Claude S41   5
Claude S45   2
Codex  S45   2
Claude S46   2
Claude S51   1
             --
             15
Codex S57 replay + Stage A/B/C = 1 + 135
current total                  = 151
```

Codex explicitly approves Claude Progress Report Session 56 blob
`83c527ced4e12ce27cfbf83601c89fc0e670a3cd` unchanged. Claude's edited handoff did
not explicitly approve that exact blob, so Claude should state same-state owner approval
on re-review before the report loop is treated as closed.

## Verification

```text
focused role-coverage tests       31 passed in 0.24 s
full packet suite              1,006 passed in 122.47 s
compileall                        clean
CLI help                          clean
wrong-assignment adversarial      refused
unknown-verdict adversarial       refused
missing-dev adversarial           refused
artifact scientific counts        0 / 0 / 1 / 1 unchanged
artifact rollouts_spent            0
config/config.json                absent
confirmatory identities/payloads   0 / 0
```

The active transcript append passed the hard gate: the complete 990,381-byte /
14,554-line prior state remained a byte-identical prefix with SHA-256
`4aeb873232635ef025e055f2b4c016e8484584da3ed486263d2a54dc4e0ddb31`; the new
header occurs once at line 14,558, after the recorded boundary; the transcript diff is
`+104/-0`.

## Files created or updated

### Created

- `agents/Codex/Session Summaries/HumanReport58.md` — this report.

### Updated

- `Reproducibility Packet/scripts/analyze_protocol_p_role_coverage.py` — input binding,
  verdict/case/split/finiteness guards, strict JSON, and exact source evidence.
- `Reproducibility Packet/tests/test_protocol_p_role_coverage.py` — 31 focused tests,
  including all reproduced failure modes and exact source-hash evidence.
- `Reproducibility Packet/results/protocol_p/role_coverage.json` — regenerated zero-rollout
  artifact with the exact Stage-A/B/C result SHA-256.
- `Reproducibility Packet/README.md` — added the four-cell diagnostic-pause clause.
- `README.md` — appended the running-log order correction; no historical entry edited.
- `chats/Claude-Codex/Phase 2 Integration and Config Freeze/Phase 2 Integration and
  Config Freeze - Active.md` — appended the exact-state review and handoff.
- `agents/Codex/README.md` — added this report and current ownership/review state.
- `agents/Codex/Summary of Only Necessary Context.md` — fully rewritten for Session 59.

## Decisions and next steps

1. The exact Stage-A/B/C result is jointly approved and closed. Do not re-run it.
2. Section-9 role coverage is required now; 0/0/1/1 and the zero-dev named outcome stand.
3. The corrected analyzer/tests/artifact and packet/root documentation await Claude's
   genuine owner re-review and explicit exact-state approval.
4. Claude should explicitly approve the current Progress Report Session 56 blob to close
   that loop.
5. Written Amendment A2 remains blocked until these reviewer-edited states close.
6. Assignment/config lineage, regeneration, Gates 4–7, final freeze and confirmatory
   materialization remain unauthorized.
