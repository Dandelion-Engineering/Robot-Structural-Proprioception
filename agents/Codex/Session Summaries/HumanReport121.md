# Human Report - Codex Session 121

**Current date and time:** 2026-08-11 13:10 PDT

## Summary

This session closed the only open rung-2 documentation review loop. I independently reviewed
Claude's second-round owner state of `Reproducibility Packet/README.md`, authenticated the exact
Git object and working-tree bytes, reproduced all three new corrections from primary artifacts
and source, and explicitly approved Git blob
`f5e677c8afdbdfa5c97f3cc53a4a2b92d0a13b9d` / raw SHA-256
`5c83e0d8ad8064ae585bcd5bf38c4b4a31036a2305066c52f578f7073d2482e1`.

Claude's owner approval and Codex's reviewer approval now name the same bytes. The packet-runbook
review is therefore **CLOSED / BOTH APPROVED**. No packet README edit was necessary in this
session.

The public Live-Run README trigger is now satisfied, but Claude explicitly retained ownership of
that next act. I did not publish ahead of the handoff. Claude's next session should add one lean
rung-2 heartbeat that keeps the two jointly applied section-5.4 sentences adjacent to the direct
degeneracy observation and attaches no cause, trend, C1-versus-S conclusion, capacity choice or
threshold.

## Exact state reviewed

```text
Reproducibility Packet/README.md
Git blob       f5e677c8afdbdfa5c97f3cc53a4a2b92d0a13b9d
raw SHA-256    5c83e0d8ad8064ae585bcd5bf38c4b4a31036a2305066c52f578f7073d2482e1
bytes / EOL    118,912 / 1,230 LF / 0 CR / final newline
owner diff     +21 / -14 against Codex reviewer blob 7c9f394d...
```

I confirmed that the fourteen removed lines were exactly the four paragraphs Claude named. No
fifth deletion or undisclosed runbook change was present.

## Findings reviewed and decisions

### Finding BN - accepted

The prior sentence that all ten rung-1 anchors had four non-zero per-class values was false. An
independent direct read of the authenticated analysis artifact reproduced:

```text
rung-2 non-zero F1 counts   healthy 0 / actuator 6 / sensor 10 / structure 0
rung-1 non-zero F1 counts   healthy 8 / actuator 10 / sensor 10 / structure 10
only zero anchor cells      C1 seed 1 healthy; C1 seed 3 healthy
```

The new runbook text is exact: all ten anchors are non-zero on actuator, sensor and structure;
eight are also non-zero on healthy, with only C1 seeds 1 and 3 at zero on that class. The stronger
unanimous contrast is on structure, where every rung-1 anchor is non-zero and every rung-2 arm is
zero.

### Finding BO - accepted, including the Step-28 scope deviation

The Stage-1 and rung-2 equivalence gates authenticate two checkpoint payloads, not ten. A
standalone AST/source audit found:

- the sole `EQUIVALENCE_ARMS` definition is `(("C1", 0), ("S", 4))`;
- rung 2 imports that tuple and defines no second one;
- each executable has one equivalence-gate call carrying `checkpoint_dir`;
- each gate has one `Path(checkpoint_dir)` reference and one `torch.load` call.

The other eight anchors are carried document-to-document by recorded identities and scores; their
checkpoint payloads are not opened by these gates. Correcting Step 30 while preserving the same
false count in its explicit Step-28 parallel would have left the runbook internally inconsistent.
I accepted Claude's narrow Step-28 repair as warranted.

### Finding BP - accepted

The tracked run record carries `elapsed_s = 1272.094000000041`, while Codex's process-level wall
clock measured 1,274.6 seconds. The former starts inside execute mode and excludes interpreter
startup and imports. Naming both values and the clock boundary prevents a reader from treating two
valid measurements as a mismatch.

### The existing roughly-12x statement stays unchanged

Claude asked whether the line saying rung 2 costs roughly 12x per optimizer step needed an inline
provenance clause. I ruled that it does not. The frozen design records 0.2683 versus 0.0220 seconds
per step, a 12.2x ratio, and labels the measurement order-of-magnitude only. In the runbook,
`roughly` and the explicit per-step unit already separate that micro-benchmark from the adjacent
whole-run clocks. Another clause would add bulk without correcting a false claim.

## Verification

- authenticated the README blob, raw digest, size and EOL profile;
- authenticated the analysis artifact at raw SHA-256 `604d7272...`;
- independently reproduced all rung-1/rung-2 per-class counts and the four exact
  majority-baseline arms: C1 seeds 0 and 4, S seeds 0 and 3;
- reproduced the macro sign count as 2 negative / 1 zero / 2 positive;
- statically audited both equivalence-gate checkpoint paths without importing project modules;
- ran the packet-wide regression suite: **2,108 passed in 170.75 seconds**; and
- kept `git diff --check` clean.

No fit, checkpoint, rollout, generation, analyzer or C7 invocation, plan-mode invocation, or
pilot/validation/test-role read occurred. The pytest run used packet tests and their fixtures;
it did not authorize or perform a scientific read.

## Transcript append integrity

Before my append, the active Phase-2 transcript measured:

```text
bytes       2,083,760
SHA-256     223d0e75b8f61635aa296f58ec6d38c3f1362b4df95a4c34343df39e9f15f117
LF / CR     33,826 / 19,709
```

The complete prior byte sequence remains an exact prefix after the append. The new Codex header
occurs once after that boundary, Codex is physically last, and the Git diff is one tail hunk at
`+75 / -0`. The resulting transcript measures 2,087,669 bytes with SHA-256
`d4a05457d2c3f3e4354909e815defdbb2f4322c30dd8ecdfdda43174b07e2112`, 33,901 LF and
19,709 CR. No append-order or byte-prefix recurrence occurred.

## Files created or updated

- `chats/Claude-Codex/Phase 2 Integration and Config Freeze/Phase 2 Integration and Config Freeze - Active.md`
  - appended the exact-state approval, decisions, verification and next-act handoff;
- `agents/Codex/Session Summaries/HumanReport121.md`
  - this detailed session report;
- `agents/Codex/README.md`
  - updated navigation and current gate descriptions for the closed runbook loop; and
- `agents/Codex/Summary of Only Necessary Context.md`
  - completely rewritten for Session 122.

The root public `README.md` and `Reproducibility Packet/README.md` were not edited by Codex.

## Next steps

1. Claude should authenticate the closed packet-runbook state and publish one lean public rung-2
   heartbeat under the Live-Run README playbook.
2. Codex should review the exact public README state if Claude hands it back.
3. Preserve the 67-checkpoint clean-clone limitation: only two original Step-26 checkpoint
   payloads are needed by each equivalence gate, but those two remain absent from a fresh clone.
4. Preserve every scientific boundary: no retry, causal explanation, rung trend, C1-versus-S
   conclusion, later-role read, capacity/threshold choice or final configuration follows from this
   documentation closure.

## Current gate state

```text
rung-2 packet runbook                 CLOSED / BOTH APPROVED at f5e677c8...
public interpreted rung-2 heartbeat  READY FOR CLAUDE'S NEXT ACT
capacity / probability / abstention  VALIDATION-OWNED / UNDECIDED
final configuration                  ABSENT / BLOCKED
```
