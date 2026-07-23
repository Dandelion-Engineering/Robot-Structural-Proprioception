# Summary of Only Necessary Context

**Last completed Codex session:** 23
**Phase:** Phase 2 — Execution
**Branch:** `main`
**Session-23 target commit:** `Codex Session 23`
**Initial reviewed Claude state:** `ad7d6ba` (`Claude Session 23`)
**Configuration:** `Reproducibility Packet/config.json` remains **UNFROZEN**
**Next regular Codex progress report:** Session 24

This file is the authoritative Codex resume state. Re-read the live repository and active transcripts before relying on it.

## Resume state

Claude Session 23 explicitly approved Codex Session 22's corrected severity-estimation-quality screen. That prior loop is closed.

Claude then supplied the cap-boundary action measurement opened by the correction. Codex Session 23 reproduced it, found three review-significant interpretation/integrity problems, corrected them in place, approved the reviewer-corrected state, and handed it back to Claude for owner re-review.

**Current review loop: OPEN.**

Claude must explicitly review and approve the exact current state of:

- `Reproducibility Packet/scripts/screen_severity_action_boundary.py`;
- `Reproducibility Packet/tests/test_severity_action_boundary.py`;
- `Reproducibility Packet/results/severity_action_boundary/summary.json`;
- `Reproducibility Packet/results/severity_action_boundary/severity_action_boundary_report.md`;
- packet Step 16 and Current-boundary text.

The following parts of Claude Session 23 are approved unchanged:

- `leave_one_group_out_residuals` in `scripts/utils/estimator.py`;
- packet Step 2's whole-directory `pytest tests\ -q` command;
- all 40 simulated arms and `arm_rows.csv`;
- the root Live-Run heartbeat, which contains only the now-jointly-approved Session-22 correction.

Do not treat Codex's reviewer edits, this continuity file, downstream use, or silence as Claude approval.

## Current cap-boundary result

### Direct measurement

Condition:

- true remaining actuator gain: 0.50;
- recorded maximum compensation: 2.0;
- one scheduled held decision;
- four disjoint sensor-noise assessment seeds;
- deployable C1/S severity estimates recorded by Step 15;
- complete onset+5 s `J_5s` windows.

Recorded outcome:

- mean no-action healthy-relative deficit: **13.11%**;
- mean privileged-oracle recovery: **10.81%**;
- mean paired S-minus-C1 reduction: **−0.1177 percentage points**;
- maximum absolute paired difference: **0.5154 percentage points**;
- C1 ahead on two seeds, S ahead on one, one pair identical;
- whole measured 1.50–2.00 multiplier-sweep reduction span: **3.8083 percentage points**;
- Claim Sheet paired-control bar: **10 percentage points**.

This supports a narrow development conclusion: the **recorded linear-read-out severity route** is below the bar at the 0.50 / cap-2 boundary, subject to Claude owner re-review.

It does not close:

- arbitrary future read-outs whose commands leave the 1.50–2.00 measured envelope;
- the cap ≥ 4 / 0.25-floor boundary;
- calibrated class-probability effects;
- the actuator class;
- healthy false authorization or source-specific action benefit;
- an evaluation-sized paired C1/S control comparison;
- Claim Sheet Slot 11 or a confirmatory result.

### Severity-uncertainty roles

The `SeverityRidgeHead` training residual dispersion is optimistic and must not reach the confidence gate.

| suite | in-sample std | calibration cross-seed std | disjoint assessment std | assessment MAE |
|---|---:|---:|---:|---:|
| C1 | 0.004237 | 0.006741 | 0.008393 | 0.006472 |
| S | 0.001951 | 0.011160 | 0.008029 | 0.007633 |

Role boundary:

- The cross-seed values use a fixed penalty selected on the same tuning groups. They are **calibration-role development diagnostics**, not nested post-selection or frozen margins.
- The assessment values come directly from Step 15's disjoint predictions and must remain assessment evidence.
- The absolute suite ranking is not stable across the two diagnostics. S has the larger internal cross-seed dispersion but a slightly smaller assessment standard deviation; its assessment MAE is larger because its bias is larger.
- The controller uses the calibration-role values to avoid consuming the assessment role. Both are far below the current 0.25 confidence threshold, so the gate and all action arms are unchanged.

### Measured conversion envelope

The 1.50–2.00 sweep is an empirical conversion envelope for the recorded linear heads on this condition. It is not a mathematical bound on any future read-out. Local slope multiplied by observed multiplier spread is a linearization only; the direct paired rollouts are authoritative.

### Integrity and lifecycle

The current screen fails loudly unless all seven conditions pass:

1. no-action arms reproduce Step 15;
2. exactly one estimator evaluation occurs;
3. no-action arms issue zero commands;
4. action arms act;
5. A1 incident count is zero;
6. saturation count is zero;
7. applied multipliers match commands.

Explicit sweep multipliers must be strictly above 1 and below the separately supplied cap point.

### Exact-restoration scope

At the measured 0.50 boundary, the oracle realizes 93.2% of the analytic exact-restoration ceiling. Error accumulated before the held decision cannot be recovered by later compensation.

Do not transfer that 0.78-percentage-point shortfall or 93.2% factor to the selected 0.25 condition. That condition has not been measured under this screen.

## Accepted upstream state

### Severity-estimation-quality screen

Claude approved Codex Session 22's exact corrected state:

- held-out MAE: **0.006472 C1 / 0.007633 S**;
- all 12 strictly capped-interior pairs command identically at cap 2;
- the 0.50 cap-2 boundary differs on 3 of 4 pairs;
- cap ≥ 4 moves the boundary to the 0.25 floor, where all four recorded pairs differ;
- severity quality is narrow development evidence, not a sensor-suite control result.

### Fault tracking-deficit screen

The jointly accepted conversion is:

`required_deficit = target_reduction / (1 - target_reduction)`.

For a 12% target reduction, the healthy-relative deficit gate is **13.636%**. The accepted screen selects **0.25 remaining actuator gain** with a 23.03% minimum disjoint deficit. The 0.50 condition remains useful as the cap-2 boundary measurement, not as the selected action-screen condition.

No structural setting from 0.75 through 0.05 remaining EI reaches the gate on this task. The fixed 0.05 rad encoder-bias condition shows a 15.69% mean deficit but does not automatically create an S-over-C1 control opportunity.

### Structural-action result

The first inverse-stiffness family remains blocked as a generic nominal-controller retune:

- structural tracking improves 19–20%;
- healthy tracking improves slightly more;
- source-specific margin fails;
- code mechanics are preserved, but no structural recovery action advances.

The bounded noisy held-decision review advances S information/action authorization only. Keep detection, attribution, authorization, action efficacy, source specificity, and paired control outcome separate.

## Next technical gates

First process Claude's owner re-review of the exact Session-23 corrected boundary state. Close only on explicit same-state approval; genuinely re-review any owner edit.

After that, the actuator action review remains the next control task. It must:

1. use the selected 0.25 remaining-gain condition and preserve the 0.50 cap-2 boundary as a separate recorded sensitivity;
2. use deployable C1/S diagnoses and report oracle ceilings separately;
3. preserve seed-paired pre-fault histories and complete `J_5s` windows;
4. report action versus no action within suite and paired C1-versus-S tracking with uncertainty;
5. include healthy false authorization and source-specific margin;
6. preserve tuning/calibration/assessment roles;
7. report all A1, saturation, contact, and decision-lifecycle checks;
8. keep training residual dispersion out of the confidence gate;
9. measure calibrated class probability separately from one-hot prototype scores;
10. sweep the jointly binding `(maximum_gain_compensation, minimum_gain_remaining)` surface without moving the Claim Sheet bar after results are known.

Session 24 must also create the regular director progress report unless a phase transition or Claim Sheet amendment changes that requirement.

## Verification state

- Full Reproducibility Packet: **248 passed**.
- Focused cap-boundary tests: **28 passed**.
- `compileall -q scripts tests`: passed.
- CLI help: passed.
- Strict JSON and recursive finite-value checks: passed.
- Independent summary audit: 40 arms, all seven gates true, paired statistics exact, assessment diagnostics exact.
- Tracked ten-worker regeneration and independent eight-worker rerun: all three artifacts byte-identical.
- `arm_rows.csv`: byte-identical to Claude Session 23.
- Stale universal-bound / ranking-inversion scan: clean.
- No dependency installed.
- Root Live-Run README unchanged by Codex Session 23.

Artifact hashes:

- `arm_rows.csv`: `DC897226E7159FAB42F0E72DFC630124388C72D6D5C8F3833D8F310495870D9E`
- `summary.json`: `4C56721D0323C0ACD870B4E15D67B7167E92639430AC2B60D9195803B6F2E2EC`
- report: `DBD5DF3B86C78637001B122128B11C783432AA76FA8C0EEB56E5F00DCE452E44`

## Transcript append state

Session-23 Phase-2 append:

- pre-write physical line count: 1,944;
- complete verified EOF anchor: 11 lines, one occurrence;
- pre-write hash rechecked immediately before writing;
- Codex Session-23 header: exactly once after the old boundary;
- post-write physical line count: 2,024;
- physical last speaker: Codex;
- transcript diff: **+80 / −0**.

Operational rule: read the physical UTF-8 tail, record the pre-write line count, verify a complete multi-line EOF anchor is unique, and make the patch itself contain that entire anchor. After writing, assert header count, position after the boundary, physical-last speaker, and append-only diff before committing.

## Open / unfrozen items

- Claude owner re-review of the corrected cap-boundary screen;
- selected-condition actuator action review;
- compensation-cap / minimum-gain-floor pair, including cap ≥ 4 behavior;
- per-suite calibrated class probability;
- calibration-role uncertainty lifecycle and future frozen margin;
- sensor-fault recovery action;
- validation-sized healthy/four-class calibration;
- ambiguous known-class cases that make abstention bind;
- compound/OOD faults and held-out subtype/location/severity/onset grids;
- non-load-bearing sensor constants;
- class/abstention/selective/OOD thresholds;
- learned temporal attribution head plus RMA baseline;
- whole-trajectory/fault-setting splits and deployable-loader leakage audits;
- role hashes, multi-run storage, and immutable config/schema gates;
- reference lifecycle beyond the scheduled held-decision development condition;
- task/contact/controller profile and W=768 / stride=16;
- evaluation-sized paired control comparison;
- interactive Slot-8 verification artifact and all Phase-3 deliverables.

## Required startup sequence for Session 24

1. Re-read `AgentPrompt.md` and follow it exactly.
2. Read all of `Project Details/Project Details.md` and the current Claim Sheet.
3. Read this file.
4. Read every Codex-channel `Summary.md`, then all active transcripts completely to physical EOF before replying.
5. Read Claude's latest Human Report and continuity.
6. Inspect git status, branch tip, and actual files before trusting this summary.
7. Process Claude's owner re-review of the exact corrected cap-boundary state first.
8. Close only on explicit same-state approval; genuinely re-review any further edit.
9. Create `Progress Report Session 24.md` at closeout using the project's regular reporting standard.
10. Keep `config.json` unfrozen unless every remaining gate actually closes.

## Closeout conventions to preserve

- Active chats are append-only under the full hard gate described above.
- Rewrite this continuity file completely at every completed Codex session.
- Add the next `HumanReportN.md` and keep `agents/Codex/README.md` purpose-oriented.
- Keep the public Live-Run README lean, append-only, and milestone-based.
- Review `.gitignore`, stage only intended files, run `git diff --cached --check`, then commit exactly `Codex Session N` and push.
- Next regular Codex progress report: Session 24.
