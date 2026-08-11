# Codex — Human Report, Session 120

**Date and time:** 2026-08-11 11:15 PDT

**Phase:** Phase 2 — Execution, with limited Phase-3 Reproducibility Packet assembly

**Progress-report session:** **Yes.** Session 120 is Codex's fifteenth regular every-eighth-session
report. `agents/Codex/Progress Reports/Progress Report Session 120.md` covers Sessions 113–120.

---

## Summary

Claude Session 120 independently re-opened the exact approved rung-2 analysis artifact,
re-derived the ordered success status and five paired signs, and applied the same two frozen
section-5.4 sentences Codex applied in Session 119. I authenticated that handoff and accepted the
matching half. **Rung-2 section 5.4 is now 2/2 and jointly closed.** It selects no rung, capacity or
threshold and licenses no new run or later-role read.

Claude also wrote the agreed two-step rung-2 lane into `Reproducibility Packet/README.md` and
explicitly handed owner-approved blob `9a3a878c...` to Codex for review. I read the full packet
runbook against the Reproducibility Packet and review-cycle playbooks, the frozen design, and the
persisted plan/run/equivalence/analysis records.

I accepted three deliberate choices unchanged:

1. do not print the two `rung2_minus_rung1` figures, because the tracked artifact preserves them
   but no interpretation row licenses a sentence about them;
2. retain Claude's 55-to-67 checkpoint correction and two added table rows, because the packet
   result tree now contains exactly 67 `.pt` files; and
3. retain the new Current-boundary paragraph, which carries the jointly closed interpretation
   and zero-class context without adding a cause, trend, suite comparison or selection.

I found one factual defect. Step 31 said the six non-baseline arms had non-zero `actuator` F1
“and nothing else.” The exact record says all ten arms have non-zero `sensor` F1; six additionally
have non-zero `actuator` F1; all ten are zero on `healthy` and `structure`. I corrected only that
sentence forward and explicitly approved the new README state:

```text
Reproducibility Packet/README.md
Git blob       7c9f394de7b26c3b549eeaedac0b23d98d9aa66a
raw SHA-256    a016d696f8b7dce5e02ee0ca7009e73b1b6d40fc7068e6066fcaa557eed67765
bytes / EOL    118,179 / 1,223 LF / 0 CR
reviewer diff  +3 / -3 against Claude's owner blob 9a3a878c...
```

Claude owns the artifact, so the review loop remains open for Claude's genuine re-review and
same-state approval. The public Live-Run README was deliberately left unchanged until that one
exact runbook state has both approvals.

## Startup and live-state authentication

The required automation gates passed in order:

- `.agent-turn` named `Codex`;
- `.agent-session.lock` did not exist;
- Codex created the lock; and
- the one required post-lock re-read still named `Codex`.

`CODEX_HOME` was unset, so the first environment-relative memory lookup failed without touching
project state. I then used the known Codex home path to read the automation continuity file. The
live files, not memory, controlled every exact identity and gate.

I read `AgentPrompt.md`, all Project Details, Codex continuity, all Codex-participant chat
summaries, the monitoring thread, the authoritative Phase-2 physical tail, Claude's newest report,
and the relevant review, packet and progress-report playbooks.

The repository began clean at:

```text
HEAD == origin/main == 62d8d31649c33e17c1ca8a67783eaa5e707111ec
commit subject          Claude Session 120
packet README blob      9a3a878c862fa0c28de574eec612531a52212dc9
```

Claude's published transcript digest reproduced exactly before Codex appended:

```text
bytes       2,070,673
SHA-256     9167a5433618158fedbe1e81ac60ecaab71e3fc3733311681d6f6b071c8c2c2f
last header Claude Session 120
```

## Section-5.4 closure

The exact artifact remained unchanged:

```text
Reproducibility Packet/results/rung2_escalation_analysis/rung2-run-1/
  rung2_escalation_analysis.json

Git blob       a2fa857b7df14baefc047bf0b8b4b7a4d87c7b43
raw SHA-256    604d72724b4cf11a97ce0af836ecef1163442e9ff7e6423aa2fd0fad9556951c
bytes / EOL    40,270 / 0 LF / 0 CR
```

Claude's independent derivation selected `OPTIMIZATION_CHECK_PASSED` and `MIXED`, matching Codex's
Session-119 derivation. Claude applied and explicitly approved exactly the same frozen pair:

> Slot 9's rung 2 is built and fitted; the ladder has more than one rung on it, and the
> development record contains one rung-2 fit at five seeds under the approved protocol.

> At rung 2, in-sample, the paired sign was not consistent across the five seeds.

I accepted the matching half. The interpretation gate is now closed at the same artifact bytes.
No causal connective, rung trend, capacity claim, C1-versus-S conclusion or held-out implication
is licensed.

## Packet-runbook review

### Full-artifact and diff review

I read the complete 118-kB runbook, not only the new hunk. I then inspected Claude's `+175/-2`
commit diff and cross-checked the new Steps 30–31 against:

- `protocol/rung2-escalation-v0.1.md`;
- the consumed plan at raw/canonical SHA-256 `b51b0009...1040`;
- the raw run at SHA-256 `9d94b03e...996ed`;
- the equivalence record at SHA-256 `ddcb5fed...4e936`; and
- the analysis artifact at SHA-256 `604d7272...6951c`.

The architecture, resource, timing and interpretation statements reproduce. The design itself
records the 219,018 versus 39,594 parameter counts and the order-of-magnitude 12× per-step CPU
cost. The 1,274.6-second figure is the recorded external wall clock for the one authorized run;
the terminal artifact's internal `elapsed_s` is 1,272.094.

### Accepted judgment calls

**Omitting the rung-difference numbers.** Section 5.3 permits their persistence and says quoting a
primitive is not itself a direction statement. It does not require the runbook to print them. In
this context the values' only likely use is the comparison no interpretation row licenses, while
the tracked artifact remains linked and inspectable. I accepted the omission as restraint, not
under-disclosure.

**Expanding 55 checkpoints to 67.** The packet result tree contains 67 ignored `.pt` files: ten
approved anchors, forty Stage-1 curve checkpoints, two Stage-1 equivalence checkpoints, three
preserved failed-run checkpoints, ten rung-2 checkpoints and two rung-2 equivalence checkpoints.
The correction makes the clean-machine limitation current and packet-wide.

**Adding the Current-boundary paragraph.** The paragraph accurately distinguishes a built/fitted
rung from learning, names the zero healthy/structure F1 record, and repeats every downstream
non-authorization. It belongs in the runbook's current summary.

### Finding BM — the actuator-only shorthand was false

Claude's new Step-31 prose said:

> The other six score a non-zero `actuator` F1 and nothing else.

Direct parsing of all ten rung-2 arms shows:

```text
10 / 10   sensor F1 > 0
 6 / 10   actuator F1 > 0
10 / 10   healthy F1 == 0
10 / 10   structure F1 == 0
 4 / 10   exact majority-class accuracy and macro-F1 at six decimals
```

I replaced the sentence with the exact record: the other six add non-zero actuator F1, and all
ten have non-zero sensor F1. The same shorthand appears in Claude's concluded HumanReport120; the
project's forward-correction discipline says not to rewrite a settled session report, so the fix
lives in the active packet artifact and the review chat.

I explicitly approve README blob `7c9f394de7b26c3b549eeaedac0b23d98d9aa66a`. Claude's
owner re-review remains a separate gate.

## Independent verification

### Artifact and record audit

A PowerShell audit independently reproduced:

- all four tracked JSON digests and the three README byte counts;
- the frozen design's canonical SHA-256;
- `X_RUNG2_OK`, ten rung-2 arms, two equivalence arms and the 12/12/0/0/0 resource budget;
- the exact class census above;
- four exact majority-baseline arms; and
- 67 packet-result checkpoints.

One audit assertion initially failed because the PowerShell `String.Split` overload treated the
supplied sentence as a character set rather than a literal substring. I replaced that instrument
check with an escaped regular-expression count. This was an audit-instrument defect, not a README
or artifact defect.

### Zero-fit plan probe

I ran plan mode once under a fresh scratch label and fresh packet-results directory. It returned:

```text
X_PLAN_OK: 10 rung-2 arms + 2 equivalence arms planned ... 0 fits run
```

The scratch plan was inspected and its output directory removed. No data root, checkpoint payload
or fit was used.

### Tests

```text
focused rung-2 normal       316 passed in 5.14 s
focused rung-2 python -O    316 passed in 5.76 s, one expected pytest warning
packet-wide                2,108 passed in 151.60 s
git diff --check           clean
```

The full suite ran through the project-root `venv` and packet-scoped tests. It ran in a hidden
background process so progress could be checked without blocking communication; its temporary
stdout/stderr logs were removed after the clean result.

## Transcript append integrity

The technical handoff was written by carrying the complete asserted Claude prefix as literal
bytes, then concatenating one new payload. No text patch was applied to the mixed-EOL transcript.

The writer passed prefix, payload and header assertions before PowerShell treated Git's standard
“LF will be replaced by CRLF” warning as an exception during the final diff check. I made no
second write. A fresh read-only verification then established:

```text
prior bytes / SHA       2,070,673 / 9167a5433618158fedbe1e81ac60ecaab71e3fc3733311681d6f6b071c8c2c2f
prefix retained         exact
post bytes / SHA        2,074,443 / 7424531488d9131273d5e0eec507c81bb9ceecd96a70968d948c313976987eee
new header              Codex Session 120, unique and physically last
Git diff                +66 / -0, one physical-tail hunk
post EOL census         33,670 LF / 19,709 CR
git diff --check        exit 0
```

The warning was a wrapper-handling problem after the append, not an order, prefix or content
fault. No monitoring-thread entry was warranted because the monitored property held and no
correction append was needed.

## Public heartbeat decision

The Live-Run README heartbeat check ran. The jointly interpreted rung-2 state is noteworthy, but
the packet runbook that would anchor the public entry is still in owner re-review after Codex's
factual correction. I left the public README unchanged. The named trigger is Claude's explicit
approval of the same packet README blob; only then should one lean interpreted-rung-2 heartbeat be
considered.

## Files created or updated

- `Reproducibility Packet/README.md` — one factual per-class correction; reviewer-approved blob
  `7c9f394d...`; Claude owner re-review open.
- `chats/Claude-Codex/Phase 2 Integration and Config Freeze/Phase 2 Integration and Config Freeze - Active.md`
  — appended the section-5.4 closure acknowledgment, runbook review, exact repair, explicit
  approval and handoff; `+66/-0`, one tail hunk.
- `agents/Codex/Progress Reports/Progress Report Session 120.md` — fifteenth regular director
  update, covering Sessions 113–120.
- `agents/Codex/Session Summaries/HumanReport120.md` — this report.
- `agents/Codex/README.md` — workspace index and current authoritative-state descriptions updated.
- `agents/Codex/Summary of Only Necessary Context.md` — completely rewritten for Session 121.

**Not modified:** the public root README; frozen rung-2 design; architecture, executable or
analyzer code/tests; plan; run/equivalence/analysis artifacts; any checkpoint; delivered data;
or any configuration file.

## Resource accounting

```text
fits                              0
checkpoints written               0
rollouts                          0
generation runs                   0
pilot / validation / test reads   0
production analyzer invocations   0
C7 invocations                    0
```

Plan mode wrote and removed one scratch JSON plan. The test suite and audits changed no tracked
scientific artifact.

## Current gate map

```text
Stage-1 capacity measurement                       COMPLETE AS SCOPED
Stage-1 section 5.4                                CLOSED / JOINTLY APPLIED
Stage-1 instrument-precision note                  CLOSED / BOTH APPROVED
rung-2 design                                      CLOSED / BOTH APPROVED
rung-2 architecture module/test                    CLOSED / BOTH APPROVED
rung-2 executable/test                             CLOSED / BOTH APPROVED
rung-2 zero-fit plan                               CLOSED / BOTH APPROVED
rung-2 fitting authorization                       SPENT / ONE INVOCATION
rung-2 raw terminal                                X_RUNG2_OK
rung-2 analyzer code/test                          CLOSED / BOTH APPROVED
rung-2 analyzer authorization                      SPENT / ONE INVOCATION
rung-2 analyzer terminal                           X_ANALYSIS_OK
rung-2 exact derived-state review                  CLOSED / BOTH APPROVED
rung-2 section 5.4                                 CLOSED / JOINTLY APPLIED
rung-2 packet runbook                              REVIEWER APPROVED / CLAUDE RE-REVIEW OPEN
public interpreted rung-2 heartbeat                DEFERRED TO RUNBOOK SAME-STATE APPROVAL
capacity / probability / abstention thresholds     VALIDATION-OWNED / UNDECIDED
final configuration                                ABSENT / BLOCKED
```

## Next steps

1. Claude must genuinely re-open packet README blob `7c9f394d...` and explicitly approve it or
   return a new state. Do not infer approval from the edit or this handoff.
2. After same-state runbook approval, reconsider one lean public rung-2 heartbeat.
3. Any attempt to explain the zero-class result or propose another experiment begins as a new
   reviewed design. No replay, retry or later-role read is currently authorized.
4. Preserve the direct zero healthy/structure F1 observation beside the two frozen sentences in
   later Technical Report work, without attaching a cause or rung trend.
5. Resolve the 67-checkpoint clean-machine recovery/distribution boundary before final packet
   completion.
6. `director_requests.md` entry 1 remains open and non-blocking.

— Codex
