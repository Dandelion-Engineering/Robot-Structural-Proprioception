# Summary of Only Necessary Context

**Rewritten:** 2026-07-21 18:45 PDT

**Last completed Codex session:** 17

**Next Codex session:** 18

**Current branch:** `main`

**Project phase:** Phase 2 — Execution

**Configuration:** explicitly **unfrozen**

## Resume state

Codex Session 17 closed the prior matched-contact pilot review loop after Claude Session 17 independently reproduced and explicitly approved the exact Session-16 state. Codex then completed the bounded task/contact/controller and held-reference-lifecycle redesign that Claude identified as the next natural task.

The new exact decision is:

`ADVANCE_BOUNDED_TASK_CONTACT_PROFILE_TO_MATCHED_INFORMATION_REVIEW`

This is a development mechanics/controller/lifecycle advance only. It uses fixed source-correct diagnosis stand-ins and therefore does **not** establish attribution accuracy, recovery advantage, validation-sized calibration, evaluation readiness, or permission to freeze `config.json`.

Codex explicitly approved the exact Session-17 implementation and appended the handoff to the active Phase-2 transcript. **Claude now owes genuine first review of this new state.** If Claude edits any handed-off artifact, Codex must inspect the actual edited files and provide a genuine owner re-review before the loop can close.

## What changed in Session 17

- Added `Reproducibility Packet/scripts/utils/task_control.py`:
  - `BoundedTaskProfile` supplies a finite smooth joint target and return;
  - `ObservedJointPDController` uses only delivered `q_obs`/`qd_obs` and zero-order-holds missing observations;
  - `EstimatorRecoveryTaskPolicy` composes observed task feedback, the existing estimator-policy seam, and recovery.
- Extended `GainScheduledRecoveryController` with validated `command_from_nominal()` so recovery modifies the bounded task controller's command instead of replacing it with the old perpetual multi-sine task.
- Added `SingleDecisionHoldEstimator`, which evaluates once at the first scheduled decision and causally holds the result.
- Added `Reproducibility Packet/scripts/screen_bounded_task_contact.py` and five focused tests; added two external-nominal recovery tests.
- Recorded deterministic JSON/CSV/Markdown artifacts under `Reproducibility Packet/results/bounded_task_contact_screen/`.
- Updated the packet runbook and one lean public Live Run Status entry.

## Exact development condition and result

Controller/profile:

- PD gains: `kp=(0.05,0.03)`, `kd=(0.005,0.003)`;
- torque limits: `(0.2,0.1) N·m`;
- finite target: `(0.3,0.3) rad`;
- probe: `1.000–2.250 s`;
- one held decision: step `1136`, time `2.272 s`;
- movement begins: `2.400 s`;
- hold ends: `4.400 s`;
- return ends: `5.000 s`;
- run ends: `6.000 s`.

Predeclared screen: `z={0.100,0.125,0.150,0.175,0.200} m × {healthy,structure,actuator,sensor}`.

- `z=0.100 m`: no contact for any source; retained as negative control.
- `z=0.125 m`: healthy contacts.
- `z=0.150 m`: healthy and actuator contact.
- `z=0.175 m`: healthy, actuator, and sensor contact.
- `z=0.200 m`: every source has exactly one post-decision contact episode and every declared selection gate passes; this is the lowest eligible plane.

Selected-plane rows:

| Source | Contact steps | Contact interval (s) | Peak force (N) | Recovery changes | Recovery start (s) | A1 flags |
|---|---:|---:|---:|---:|---:|---:|
| healthy | 24 | 4.618–4.664 | 2.124707 | 0 | — | 0 |
| structure | 21 | 5.154–5.194 | 0.475619 | 1864 | 2.272 | 0 |
| actuator | 24 | 4.636–4.682 | 1.945662 | 1863 | 2.272 | 0 |
| sensor | 21 | 4.856–4.896 | 1.585253 | 0 | — | 0 |

Every selected row has exactly one classifier evaluation, correct held source after the decision, no pre-decision source-specific recovery, contact duty below 5%, peak force below 5 N, and zero joint-angle/joint-speed/contact-force/contact-duration/gauge/numerical A1 flags. Structure/actuator recovery begins before contact; healthy/sensor remain nominal. Worst selected-plane magnitudes are `max |q|=0.3601 rad`, `max |qd|=1.5640 rad/s`, and `max |gauge|=20.447`.

## Evidence boundary that must survive review

- Structure/actuator faults remain physical plant faults; sensor remains observation-side.
- Task feedback reads delivered observations only. Privileged plant state is for safety scoring.
- Fixed source-correct stand-ins prove only that the mechanism can express the intended source-specific action before contact. They are not a deployable information source.
- Recovery action counts are mechanism checks, not evidence that attribution improves tracking or safety.
- `z=0.200 m`, gains, limits, timing, references, thresholds, and learned components remain development candidates.
- Detection, attribution, and control evidence remain separate. The central Claim Sheet question is still open.

## Verification state

- Focused bounded-task/recovery tests: **19 passed**.
- Full Reproducibility Packet: **155 passed**.
- `compileall -q scripts tests`: passed.
- New CLI `--help`: passed.
- Strict JSON: no `NaN` or `Infinity` tokens.
- Independent default-command rerun: all three outputs byte-identical.
  - summary: `82a388c780f0354ef5f7ba6d75a57c23a9f3a4fd3e92095bc40071ca478d4a0d`
  - rows: `c2db23933affbb7ac0490e6619123b7d2fda3131d41c8faf9df5a5047f8b7e69`
  - report: `ccc1ef5d1cf4cbab6f9f2eb208da49e20bcdd7a704b302d2104654a732f949ad`
- Transcript hard gate: pre-write 1,140 lines; new header exactly once at line 1,144; Codex physically last at line 1,186.

## Open review loop

Claude must first-review this exact state:

- `Reproducibility Packet/scripts/utils/task_control.py`
- `Reproducibility Packet/scripts/utils/recovery_control.py`
- `Reproducibility Packet/scripts/screen_bounded_task_contact.py`
- `Reproducibility Packet/tests/test_bounded_task_contact.py`
- `Reproducibility Packet/tests/test_recovery_control.py`
- `Reproducibility Packet/results/bounded_task_contact_screen/*`
- `Reproducibility Packet/README.md`
- root `README.md` wording
- Codex's appended Session-17 handoff in the active Phase-2 transcript

Silence, a handoff, continuity text, or unrelated edits are not approval. The loop closes only on explicit same-state approval or owner approval after genuine review of reviewer edits.

## Next technical gate after approval

Run a matched noisy held-decision C1-vs-S information/reference-lifecycle review on this bounded mechanics condition:

1. remove fixed source-correct stand-ins;
2. use a declared single scheduled diagnosis and causal hold;
3. keep matched C1/S physical traces and common-random-number pairs;
4. keep calibration/evaluation roles disjoint;
5. test healthy false alarms, per-fault detection/attribution, abstention/selective behavior, and action gating at the exact pre-movement decision;
6. preserve the full six-second A1 contact/safety audit; and
7. do not interpret the result as an evaluation-sized recovery comparison.

Validation-sized healthy/four-class calibration, per-suite probability calibration, severity/onset grids, non-load-bearing sensor constants, class/abstention/selective/OOD thresholds, learned attribution + RMA, whole-trajectory/fault-setting split, deployable-loader leakage, role hashes, multi-run storage, immutable config/schema gates, and the evaluation-sized closed-loop comparison all remain unresolved.

## Required startup sequence for Session 18

1. Re-read `AgentPrompt.md` and follow it exactly.
2. Read all of `Project Details/Project Details.md`.
3. Read this file.
4. Read every relevant `Summary.md`, then the complete active Phase-2 transcript to physical EOF.
5. Read Claude's latest Human Report and continuity.
6. Inspect git status/HEAD and the actual files before trusting this summary if the repo has advanced.
7. Process Claude's review first. If it is explicit same-state approval, close the loop; if Claude edited, genuinely re-review those edits.
8. Keep `config.json` unfrozen unless all remaining gates actually close.

## Closeout conventions to preserve

- Active chat is append-only: read the UTF-8 physical tail, record the pre-write line count, patch only a unique multi-line EOF anchor, then assert the new header occurs exactly once after the old tail and the intended agent is physically last.
- Rewrite this continuity file completely at each Codex closeout.
- Add the next `HumanReportN.md`; keep `agents/Codex/README.md` purpose-oriented.
- Keep public Live Run Status lean and milestone-based.
- Run staged diff hygiene, then commit exactly `Codex Session N` and push.
- Next regular Codex progress report: Session 24 unless a Claim Sheet amendment or phase transition triggers one earlier.
