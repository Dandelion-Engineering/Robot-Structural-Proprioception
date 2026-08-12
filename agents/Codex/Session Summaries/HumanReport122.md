# Human Report - Codex Session 122

**Current date and time:** 2026-08-11 23:11 PDT

## Summary

This session reviewed Claude's published rung-2 Live-Run README heartbeat at exact Git blob
`964231a49d6b94230697cf9a03ad4e9f540b7fd1`, independently reproduced its quantitative claims
from the authenticated tracked artifacts, and found that the scientific description itself was
accurate and properly bounded.

I found one narrow forward documentation defect at the entry's close. The phrases `Nothing is
frozen` and `no research question has been answered` were literally broader than the state: many
development protocols and interpretation states are already frozen, and narrower development
questions have been answered even though the central Claim-Sheet question remains unanswered.
Because the public running log is append-only, I did not rewrite Claude's entry. I appended one
compact scope correction and explicitly approved the resulting root `README.md` state at Git blob
`f00ea0d9f737fd175d62634702c18f4a1647b8bb`. Claude's genuine owner re-review remains open, so the
public-heartbeat loop is not yet closed at both approvals.

I also answered Claude's direction question. The next lane should be Slot 8 first, but bounded to
a packet-local input/output contract and synthetic verification scaffold rather than a demo that
presents development evidence as the final result. After that scaffold closes review, Claude
should begin the Technical Report as an evidence map and section scaffold. The Accessible Piece
should follow once the Technical Report's evidence boundaries and eventual headline structure
are stable. Nothing in that direction opens validation or the final freeze path.

## Exact public states reviewed and approved

Claude's handed-off state reproduced exactly:

```text
README.md original filtered blob   964231a49d6b94230697cf9a03ad4e9f540b7fd1
Claude commit                       d2115f9f781d17301388bfead61dc3dad4547be2
Claude change                       +2 / -0
```

The append-only reviewer correction produced:

```text
README.md reviewer filtered blob   f00ea0d9f737fd175d62634702c18f4a1647b8bb
canonical-LF SHA-256               3e22e4299cb27493b8262a4ddf3dc965d9d206946dc561eab47a02599a7754b4
canonical bytes / LF               150,506 / 212
working-tree raw SHA-256           ede9e505b153aa62bd6967384e39eec8834534fbff8185acc10edffb76e47635
working bytes / CRLF               150,718 / 212
review delta                       +2 / -0; zero deleted lines; final newline
```

The patching mechanism temporarily left five LF-only endings near the inserted correction. I
mechanically restored the README's uniform CRLF working-tree form and rechecked that the filtered
Git blob remained exactly `f00ea0d9...`. This was an EOL-form repair only; the content state did
not change.

## Independent result audit

I wrote no audit artifact and imported no project module. A fresh read-only script used only the
standard library and refused unless these three tracked inputs reproduced their approved raw
SHA-256 identities:

```text
rung2_escalation_analysis.json   604d72724b4cf11a97ce0af836ecef1163442e9ff7e6423aa2fd0fad9556951c
rung2_escalation_result.json     9d94b03ee5825b15c3e09d612a9ebdfdcddb959d068ea35da899dbb35ae996ed
rung2_escalation_equivalence.json
                                 ddcb5fedeafffda5ebf19f6b973b410f95801c407d9af9302a8ecf7268b4e936
```

It independently reproduced:

```text
rung-2 non-zero F1     healthy 0 / actuator 6 / sensor 10 / structure 0
sensor-only arms       C1 seeds 0,4; S seeds 0,3
sensor+actuator arms   C1 seeds 1,2,3; S seeds 1,2,4
rung-1 non-zero F1     healthy 8 / actuator 10 / sensor 10 / structure 10
paired macro sign      negative 2 / zero 1 / positive 2 = MIXED
run terminal/spend     X_RUNG2_OK / 12 fits / 12 checkpoints / 0 generation / 0 rollouts
non-development reads  0
internal elapsed       1272.094000000041 s
parameter ratio        219018 / 39594 = 5.531596
```

The four sensor-only arms are exactly the four majority-baseline arms at accuracy `0.631579` and
macro-F1 `0.193548`. Both equivalence controls carry bit-identical weights and loss histories.
The approved packet runbook independently supports the process wall clock, rough per-optimizer-
step timing, and the sequential-GRU versus dilated-convolution hardware explanation.

The two jointly applied section-5.4 sentences are quoted exactly in the public entry, and the
weak-objective warning precedes the zero-class description. The entry attaches no cause, rung
trend, scientific C1-versus-S conclusion, capacity choice or threshold to the scientific state.

## Finding BQ - public closing scope corrected forward

The heartbeat's final sentence read:

> Nothing is frozen, the final test set remains untouched, and no research question has been
> answered.

The intended boundary was clear from the surrounding paragraph, but the literal sentence did not
state it. The appended correction now says exactly that:

- no capacity, probability threshold, abstention threshold or final configuration has been
  selected or frozen;
- multiple development protocols and interpretation states are already frozen;
- the central Claim-Sheet question remains unanswered; and
- narrower build and measurement questions have been answered by the development record.

No result, gate or authorization changed. The old line remains visible because public history is
append-only.

## Direction decision

Claude proposed three lanes: early Phase-3 writing, Slot 8, or the final-freeze path. I agreed
with Slot 8 then early Phase-3 writing, with the following hard boundary for the next Slot-8
round:

1. Define one packet-local input/output contract shared by the interactive side-by-side view and
   scripted 300-DPI figure path.
2. Keep final config, checkpoint identities, class/abstention thresholds and result roles as
   required external inputs. No default may silently select the current development state.
3. Use only an explicitly labeled synthetic fixture to prove the two-copy visualization,
   confidence/abstain panel and tracking traces.
4. Fail closed on an absent or unauthorized role, and visibly label any non-final fixture
   `DEVELOPMENT-ONLY`.
5. Read no pilot, validation or test outcome and choose no capacity, threshold or configuration.
6. Return the scaffold through the normal exact-state review cycle before connecting a real
   result.

This makes progress on a named completion requirement without implying that the current
development record is the project's result. Once the interface/scaffold review loop closes, the
Technical Report can begin as a record/evidence scaffold. The final freeze path remains a
separate joint design and authorization act.

## Challenges and reasoning

### The handed-off claims were accurate but their closing shorthand was not

The main risk was to mistake two broad closing phrases for harmless style because the preceding
paragraph was careful. A public README is read out of context and often skimmed from its last
sentence. The correction therefore had to live in the public log itself rather than only in this
report or the agent chat.

### Append-only public history constrained the repair shape

Rewriting the published entry would have violated the Live-Run README playbook. The correct
repair was a short later entry stating scope and explicitly saying that no technical state
changed. The resulting Git diff is still additions-only.

### Slot 8 can begin without pretending the result exists

The Claim Sheet requires an interactive C1-versus-S comparison, but the final configuration,
thresholds and result roles do not yet exist. Building a final-looking demo now would either bake
in unauthorized development choices or create a misleading artifact. A contract plus synthetic
scaffold tests the presentation mechanism while leaving every scientific input external and
fail-loud.

## Transcript append integrity

Claude's pre-Codex transcript state measured:

```text
bytes       2,094,915
SHA-256     386b1433a9d0577eac83ece154b03b770ed8eb0477d377a39a5f80d102dd1710
LF / CR     34,024 / 19,709
```

Its first 2,087,669 bytes independently reproduce Codex Session 121's published post-write digest
`d4a05457...`, so the cross-agent prior/post convention also passes. After the Session-122 append:

```text
bytes       2,100,503
SHA-256     b454b335769bb2f12aea66d784af22d0642a0f7a0c96c0b593f19d0f992d5eba
LF / CR     34,128 / 19,709
git delta   +104 / -0
```

The complete 2,094,915-byte prior state remains an exact byte prefix. The new header occurs once
only in the suffix, the permissive header recognizer makes Codex physically last, the suffix
ends in the expected sign-off and separator, and `git diff --check` passes. No append-order or
byte-prefix recurrence occurred.

## Files created or updated

- `README.md`
  - appended the narrow public scope correction; reviewer blob `f00ea0d9...` is approved by
    Codex and awaits Claude owner re-review;
- `chats/Claude-Codex/Phase 2 Integration and Config Freeze/Phase 2 Integration and Config Freeze - Active.md`
  - appended the independent audit, Finding BQ, exact approval and bounded next-lane decision;
- `agents/Codex/Session Summaries/HumanReport122.md`
  - this detailed session report;
- `agents/Codex/README.md`
  - updated navigation and current review/direction state; and
- `agents/Codex/Summary of Only Necessary Context.md`
  - completely rewritten for Session 123.

No code, model, checkpoint, result artifact, packet runbook or configuration was changed.

## Verification and resource boundary

- exact original and reviewer README blob identities reproduced;
- public README diff is additions-only at `+2/-0`;
- three rung-2 artifact hashes authenticated;
- all public quantitative statements above independently derived;
- `git diff --check` passed; and
- transcript prefix/header/tail/additions-only gates passed.

No fit, checkpoint, rollout, generation run, analyzer/C7 invocation, plan-mode invocation or
pilot/validation/test read occurred. The audit read tracked development artifacts only. Both
rung-2 authorizations remain spent, Stage 1 remains complete as scoped, both section-5.4
applications remain closed, and final configuration remains absent.

## Next steps

1. Claude should re-open and genuinely review the appended public correction, then explicitly
   approve blob `f00ea0d9...` or return a new approved state.
2. Once that public loop closes, Claude should draft the Slot-8 input/output contract and
   synthetic scaffold under the bounded direction above.
3. Codex should review that exact Slot-8 state under both the Reproducibility Packet and Review
   Cycle playbooks.
4. After the scaffold loop closes, begin the Technical Report evidence map/scaffold.
5. Preserve the 67-checkpoint clean-clone limitation and every no-later-role/no-final-freeze gate.

## Current gate state

```text
rung-2 packet runbook                 CLOSED / BOTH APPROVED at f5e677c8...
public interpreted rung-2 heartbeat   REVIEWER APPROVED at f00ea0d9... / OWNER RE-REVIEW OPEN
Slot-8 verification artifact          NEXT DESIGN/SYNTHETIC-SCAFFOLD LANE / NOT BUILT
capacity / probability / abstention   VALIDATION-OWNED / UNDECIDED
final configuration                   ABSENT / BLOCKED
```
