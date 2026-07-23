# Human Report 25 — Codex

**Session date and time:** 2026-07-23 16:19 PDT (checked at the shell immediately before creating this report)

**Phase:** Phase 2 — Execution

**Session type:** Probability-loop close, task-redesign withdrawal acknowledgement, role-separated actuator action-mechanism screen, development BLOCK, and owner handback

---

## Summary

This session followed `AgentPrompt.md`, closed the prior probability-screen review loop after Claude's explicit same-state approval, acknowledged Randy's withdrawal of the proposed task redesign, and resumed the original Claim Sheet path.

I implemented the next Codex-owned gate: a bounded actuator inverse-gain action screen at the already selected 0.25 remaining-gain condition. The screen uses 36 tuning arms and 64 disjoint assessment arms. It measures fault-action benefit against the identical actuator diagnosis falsely authorized on a healthy plant, reuses the exact Step-15 no-action references, and keeps tuning, assessment, oracle, recorded C1/S severity, cap/floor sensitivity, safety, and action lifecycle explicit.

The action family blocks:

- tuning selected the lifecycle-safe cap-3/floor-0.25 profile;
- disjoint oracle, C1, and S arms all produced **16.576%** mean fault reduction;
- the identical false authorization improved healthy tracking by **8.322%**;
- the resulting source-specific margin was **8.254 percentage points**, with a four-seed paired development interval of **[8.093, 8.532]**, below the predeclared 10-point gate;
- cap-4/5 profiles reached about **19.7%** raw fault recovery, but violated the A1 lifecycle/safety gate;
- C1 and S are action-identical at the selected cap.

The decision is `BLOCK_ACTUATOR_ACTION_FAMILY_AT_SOURCE_SPECIFIC_GATE`. This is development action-mechanism evidence, not calibrated authorization, a C1-versus-S control result, validation-sized evidence, a result on another task, or a frozen configuration. False-authorization rates still require calibrated class, abstention, and uncertainty outputs.

The first full run exposed an audit-boundary defect in my new screen: candidate A1 incidents were treated as execution corruption and suppressed the negative artifact. I corrected the audit so clean references remain fail-loud integrity evidence while candidate incidents remain visible scientific block evidence. A regression protects that distinction. The corrected 100-arm rerun completed and all 329 packet tests pass.

The exact script, regression, strict artifacts, and interpretation are now handed to Claude for genuine owner review. `config.json` remains unfrozen.

## Startup and controlling context

I completed the required startup sequence:

1. Read all of `AgentPrompt.md`.
2. Read the complete Project Details file, Claim Sheet, Codex continuity, every Codex-channel summary, and every active transcript through its physical UTF-8 tail.
3. Read Claude Session 25's Human Report and continuity.
4. Read the applicable review-cycle, Live-Run README, reproducibility-packet, and research-progress-report playbooks.
5. Inspected the working tree before editing and preserved Randy's pre-existing append in `Better Suited Task`.
6. Re-opened the approved probability artifact, the active Phase-2 record, the action/recovery utilities, Step-15 severity artifacts, and the current public boundary before designing the next gate.

Randy's latest active-chat message controls the proposed redesign: continue the current project under the original approved scope and reserve a different task for a separately scoped follow-on project.

## Prior review and coordination

### Probability loop closed

Claude explicitly approved the exact Session-24 reviewer-corrected probability-screen state:

- the six-point graded result remains a sampled empirical envelope;
- the continuous response between samples is not analytically closed;
- calibrated probability, abstention, and uncertainty authorization remain open;
- the actuator class is not declared closed;
- the common RMS remains a development isolation fixture, not a frozen predictive-uncertainty statistic.

That same-state review loop is closed.

### Proposed task redesign withdrawn

Randy withdrew the proposed Cartesian end-effector/task amendment before it was drafted or approved. I acknowledged that decision in the human-visible active chat and resumed the original Claim Sheet path. The root Live-Run log remains append-only: its earlier redesign entry is preserved and followed by an explicit superseding correction.

Claude still needs to acknowledge Randy's withdrawal before the `Better Suited Task` chat can be concluded.

## Actuator action screen

### Question and design

At 0.25 remaining actuator gain, can a bounded inverse-gain action recover tracking source-specifically, rather than merely improve any arm that is authorized to act?

The screen predeclares:

- tuning seeds 18000–18002;
- assessment seeds 17100–17103;
- cap/floor candidates 2/0.25, 3/0.25, 4/0.25, 5/0.25, and 5/0.20;
- a 12% tuning fault-recovery target;
- the Claim Sheet's 10% assessment recovery bar;
- a 10-point source-specific margin;
- the identical action falsely authorized on healthy;
- oracle severity plus the exact recorded held-out C1/S severity estimates;
- a 20,000-replicate deterministic paired seed bootstrap;
- one held classification, no pre-decision recovery, within-source CRN equality, reference safety, saturation, and commanded/applied multiplier identity audits.

Candidate selection reads tuning only. Assessment remains disjoint.

### Tuning result

| candidate | fault reduction | healthy false-auth benefit | source-specific margin | lifecycle |
|---|---:|---:|---:|---|
| cap-2/floor-0.25 | 10.852% | 6.177% | 4.675 pp | pass |
| cap-3/floor-0.25 | 16.657% | 8.174% | 8.483 pp | pass |
| cap-4/floor-0.25 | 19.711% | 9.987% | 9.723 pp | block |
| cap-5/floor-0.25 | 19.711% | 9.987% | 9.723 pp | block |
| cap-5/floor-0.20 | 19.711% | 9.987% | 9.723 pp | block |

Cap-2 misses the tuning recovery target. Cap-3 is the best lifecycle-safe tracking-capable candidate, but misses the specificity gate. Cap-4/5 reach the same raw plateau and fail A1 safety.

### Disjoint result

For the selected cap-3 profile, oracle, recorded C1 severity, and recorded S severity all saturate at multiplier 3.0 and are action-identical:

- mean fault reduction: **16.5764759355%**;
- minimum fault reduction: **16.4891729362%**;
- mean healthy false-authorization benefit: **8.3224227983%**;
- mean source-specific margin: **8.2540531371 pp**;
- paired four-seed interval: **[8.0926910414, 8.5316317311] pp**.

The interval excludes zero, so the effect is positive and sign-stable on these four development seeds. It remains below the 10-point magnitude gate.

The cap-5 sensitivity demonstrates the safety/magnitude trade:

- S cap-5/floor-0.20 reaches 10.179 pp;
- S cap-5/floor-0.25 reaches the same 10.179 pp;
- both fail lifecycle safety;
- C1 cap-5 arms remain below 10 pp and also fail lifecycle safety.

The complete candidate audit records 19 A1-incident arms, zero saturated arms, and zero commanded/applied multiplier mismatches. Every reference arm remains A1-clean and saturation-clean.

### Audit correction

The first 100-arm execution reached the correct scientific data but aborted before artifact creation because `a1_clean` was global over both references and deliberately stressed candidates. That collapsed two different statements:

1. whether the run/reference path is trustworthy; and
2. whether a candidate is safe enough to advance.

The corrected audit requires reference A1/saturation/multiplier cleanliness as execution integrity. Candidate violations are counted in the artifact and feed the candidate lifecycle gate. The new regression injects a candidate A1 incident, requires the reference audit to remain passing, and proves the candidate incident is recorded rather than erased.

## Changes made

### New executable and regression

- Added `Reproducibility Packet/scripts/screen_actuator_recovery_action.py`.
- Added `Reproducibility Packet/tests/test_actuator_recovery_action.py`.
- Added strict tuning/assessment summaries, deterministic bootstrap, fail-loud grid/reference/CRN/action-lifecycle audit, CSV/JSON/report generation, and source-specific decision logic.
- Added 27 focused regressions covering candidate validation, action multipliers, recorded-input loading, selection, assessment gates, bootstrap determinism, audit failure, and candidate-safety versus integrity separation.

### New artifacts

- Added `results/actuator_recovery_action_screen/summary.json`.
- Added `tuning_rows.csv` and `assessment_rows.csv`.
- Added `candidate_summary.csv`.
- Added `actuator_recovery_action_report.md`.

### Coordination and continuity

- Added packet runbook Step 17A and the current actuator-action boundary.
- Acknowledged Randy's withdrawal in `Better Suited Task`.
- Accepted Claude's same-state probability approval and closed that loop in the Phase-2 chat.
- Appended the actuator-action BLOCK and exact review request to the Phase-2 chat.
- Appended public Live-Run corrections/results without rewriting prior log entries.
- Created this Human Report.
- Updated Codex README and completely rewrote Codex continuity.

### Deliberately unchanged

- `config.json`: remains unfrozen.
- Claim Sheet and companions: no amendment.
- `agents/Codex/references.md`: no new external source was needed.
- Dependencies: none installed.

## Verification

### Executable and tests

- Corrected official run: **100 MuJoCo arms** with 8 workers.
- Focused actuator-action regressions: **27 passed**.
- Full Reproducibility Packet: **329 passed**.
- `compileall -q` on the new executable and regression: passed.
- Strict JSON parse: passed.
- Every required integrity audit field: passed.
- Exact Step-15 assessment-reference match: maximum `J_5s` delta **0.0**.

### Artifact hashes

- `summary.json`: `B9D50165F0712CCCF6F6CB63B25A37BFCFBEF07E95DE22F3D58EDC6A3D38433F`
- `tuning_rows.csv`: `31519382FA5B0FB9EA1C1EB2401833F07D7D691377E1003714A26EEDCCC945AE`
- `assessment_rows.csv`: `78F36EE91B6D02D9B92C1A585101203977DC4D71A7F74F4B19C68FDAD34B82A2`
- `candidate_summary.csv`: `9AC060A8FFA09F3171C04E73FE82901C5F4A30BC14130450EA76A5F562108E0E`
- report: `71E919FD6CA5BD106B9268C13F5698807CAAC771699C3DFB4ABFF486DBECB282`

### Append-only transcript hard gates

`Better Suited Task` acknowledgement:

- pre-write physical line count: **74**;
- unique verified EOF anchor: **one occurrence**;
- Session-25 header after the old boundary: **one**;
- post-write physical line count: **84**;
- physical last speaker after the write: **Codex**.

Initial Phase-2 acknowledgement:

- pre-write physical line count: **2,316**;
- unique verified EOF anchor: **one occurrence**;
- Session-25 header after the old boundary: **one**;
- post-write physical line count: **2,328**;
- physical last speaker after the write: **Codex**.

Final Phase-2 technical handoff:

- pre-write physical line count: **2,328**;
- unique verified EOF anchor: **one occurrence**;
- new Session-25 header after the old boundary: **one** at line 2,332;
- post-write physical line count: **2,346**;
- physical last speaker: **Codex**.

## Review status and next steps

1. **Probability screen: closed.** Claude approved the exact reviewer-corrected state.
2. **Task redesign: withdrawn.** The project continues under the approved Claim Sheet; Claude's acknowledgement is still required before the dedicated chat concludes.
3. **Actuator action family: blocked in development.** Safe cap-3 misses the source-specific magnitude gate; higher caps violate A1 safety.
4. **Actuator action review: open.** Claude must review the exact new executable, regression, strict artifact, and interpretation.
5. **Authorization: still separate and open.** This screen measures consequences of a forced false authorization, not future calibrated false-authorization rates.
6. **Evidence lane: development only.** Four assessment seeds, one task, one actuator location, and one severity are not validation or confirmatory evidence.
7. **Configuration: unfrozen.** No shared configuration value changed.
