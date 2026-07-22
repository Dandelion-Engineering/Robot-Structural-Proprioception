# Human Report 17 — Codex

**Current Date and Time:** 2026-07-21 18:45 PDT

**Agent:** Codex · **Session:** 17 · **Project phase:** Phase 2 — Execution

---

## Summary

This session closed the Session-16 matched-contact pilot review loop, replaced the unsafe perpetual open-loop task with an observed-state bounded task controller, introduced a one-decision/held-estimate lifecycle, and completed a predeclared five-plane contact-mechanics screen over all four canonical sources.

Claude Session 17 independently reproduced the prior matched-contact artifact and explicitly approved Codex's exact Session-16 state. Codex accepted that genuine same-state approval in the active Phase-2 thread, closing the old loop. Claude's two forward findings became the direct design contract for this session: recovery must have authority before the safety-relevant contact window, and the repeated joint-angle violation must be fixed as an open-loop-task problem rather than hidden by lowering the contact plane.

The new bounded task uses only delivered `q_obs`/`qd_obs`, follows a finite smooth target, makes one scheduled diagnosis after the probe, holds that diagnosis, begins movement only after the diagnosis, and returns toward the initial target before the six-second horizon ends. Recovery now modifies this observed-controller nominal command rather than generating the previous time-only multi-sine task.

The complete `z={0.100,0.125,0.150,0.175,0.200} m × {healthy,structure,actuator,sensor}` grid selects `z=0.200 m` as the lowest plane producing one bounded contact episode for every source. `z=0.100 m` is the all-source no-contact negative control. Every selected row clears all unchanged A1 development safety flags, remains below 5 N peak force and 5% contact duty, evaluates the diagnosis fixture once, and begins any source-specific recovery before contact.

The exact decision is `ADVANCE_BOUNDED_TASK_CONTACT_PROFILE_TO_MATCHED_INFORMATION_REVIEW`. This is a mechanics/controller/lifecycle advancement using fixed source-correct diagnosis stand-ins. It is not attribution evidence, a recovery advantage, validation-sized calibration, an evaluation-sized comparison, or a config-freeze result. `config.json` remains unfrozen.

Codex explicitly approved the complete state and handed it to Claude for genuine first review. That new review loop is open.

## What was accomplished

### 1. Followed the controlling workflow and closed the prior review loop

The full `AgentPrompt.md` workflow was followed:

- read all of `Project Details/Project Details.md`;
- read Codex's continuity file and every relevant chat summary;
- ingested the complete 1,140-line active Phase-2 transcript before writing;
- read Claude's latest Human Report and continuity, the Claim Sheet, and the relevant reproducibility, review-cycle, and Live-Run README playbooks;
- verified the clean `main...origin/main` starting state; and
- treated Claude's explicit same-state Session-16 approval as the only basis for closing the old review loop.

No stale handoff text was allowed to override the live transcript. The old matched-contact loop is closed; this session's new bounded-redesign loop is open for Claude's first review.

### 2. Diagnosed the task-level source of the long-horizon safety failure

The existing `commanded_torque()` task is a perpetual open-loop multi-sine. Over the honest six-second horizon it continues driving joint 1, eventually exceeding the unchanged joint-angle limit and producing repeat contact. That failure persists even at low contact planes and therefore cannot be fixed by contact-height selection alone.

Initial scratch trials with a high-gain joint PD controller destabilized the flexible cable plant. Those exploratory settings were not recorded as project artifacts. A lower-authority observed-state controller was then screened and selected for the bounded mechanism test:

- proportional gains `(0.05, 0.03)`;
- derivative gains `(0.005, 0.003)`;
- torque limits `(0.2, 0.1) N·m`;
- finite target `(0.3, 0.3) rad`;
- probe `1.000–2.250 s`;
- held decision at step 1136 / `2.272 s`;
- movement beginning at `2.400 s`;
- hold ending at `4.400 s`;
- return ending at `5.000 s`; and
- full horizon ending at `6.000 s`.

The deliberately low authority was necessary to keep the cable plant bounded while still allowing the plane contact to occur after the estimator decision.

### 3. Added a bounded observed-state task-control utility

New `Reproducibility Packet/scripts/utils/task_control.py` defines:

- `BoundedTaskProfile`, which supplies a finite smooth joint reference and its ideal endpoint-task reference;
- `ObservedJointControllerConfig`, which validates the fixed development gains, limits, and observation-hold behavior;
- `ObservedJointPDController`, which reads only delivered `q_obs`/`qd_obs`, zero-order-holds the last valid observations, and never reads privileged plant state; and
- `EstimatorRecoveryTaskPolicy`, which composes the task-feedback controller, the existing `EstimatorCommandPolicy`, and source-specific recovery while recording nominal and applied commands.

`Reproducibility Packet/scripts/utils/recovery_control.py` now exposes `command_from_nominal(output, nominal_command)`. The legacy callable retains its prior behavior by generating the old time-dependent nominal command and delegating to the new method. The external nominal command is shape/finite validated and copied, so the recovery controller cannot mutate the caller's input.

### 4. Corrected the estimator/reference lifecycle for the mechanism screen

New `SingleDecisionHoldEstimator` evaluates its wrapped estimator exactly once at the first scheduled decision and causally holds that result for the remainder of the run. This removes the Session-16 failure mode in which a reference designed for one probe phase was repeatedly applied out of phase and drifted toward actuator classifications.

For this screen, `FixedSourceStandIn` supplies the known source-correct diagnosis at the held decision. This is deliberately an information-mechanism fixture, not a deployable estimator. It lets the screen answer a narrow prerequisite question: if correct source information is available before movement, can the controller/contact seam express the intended source-specific action without violating safety?

The physical structure and actuator faults remain plant-side. The sensor fault remains observation-side and reaches both task feedback and estimator history through the real `CablePlant -> OnlineSensorSession(C1) -> policy` path. No privileged plant measurement enters task control.

### 5. Built and ran the predeclared bounded contact screen

New `Reproducibility Packet/scripts/screen_bounded_task_contact.py` runs the full five-plane/four-source grid for six seconds and records strict JSON, CSV, and Markdown outputs. Its selection contract requires the chosen plane to be the lowest plane that satisfies all of the following in every canonical source:

- exactly one contact episode;
- contact begins after both movement start and the held diagnosis;
- at least five active contact steps but no more than 5% duty;
- peak contact force below 5 N;
- zero joint-angle, joint-speed, contact-force, contact-duration, gauge, and numerical A1 flags;
- no source-specific recovery before the decision;
- the correct held source throughout the post-decision window;
- structure/actuator recovery action begins before contact;
- healthy/sensor commands remain nominal; and
- exactly one classifier evaluation.

The selected-plane rows are:

| Source | Contact steps | First–last contact (s) | Peak force (N) | Recovery changes | Recovery start (s) | A1 flags |
|---|---:|---:|---:|---:|---:|---:|
| healthy | 24 | 4.618–4.664 | 2.124707 | 0 | — | 0 |
| structure | 21 | 5.154–5.194 | 0.475619 | 1864 | 2.272 | 0 |
| actuator | 24 | 4.636–4.682 | 1.945662 | 1863 | 2.272 | 0 |
| sensor | 21 | 4.856–4.896 | 1.585253 | 0 | — | 0 |

The contact bracket is informative rather than optimized after the fact:

- `z=0.100 m`: no source contacts;
- `z=0.125 m`: healthy contacts;
- `z=0.150 m`: healthy and actuator contact;
- `z=0.175 m`: healthy, actuator, and sensor contact; and
- `z=0.200 m`: all four sources contact and all selection gates pass.

At the selected plane the worst magnitudes remain bounded: `max |q|=0.3601 rad`, `max |qd|=1.5640 rad/s`, and `max |gauge|=20.447`. All recorded A1 flag counts are zero.

### 6. Added regressions and recorded deterministic artifacts

New `Reproducibility Packet/tests/test_bounded_task_contact.py` adds five tests for:

- exact causal ordering and the complete six-second horizon;
- finite/smooth task-profile movement and return;
- one evaluation followed by a held estimate;
- absence of source-specific recovery before the decision; and
- the all-source/lowest-plane selection rule.

`Reproducibility Packet/tests/test_recovery_control.py` adds two tests for external nominal commands and malformed input shape.

New `Reproducibility Packet/results/bounded_task_contact_screen/` contains:

- `summary.json` — full spec, rows, selection gates, and exact decision;
- `bounded_task_contact_rows.csv` — all 20 full-horizon rows; and
- `bounded_task_contact_report.md` — concise decision, selected rows, bracket, and evidence limits.

An independent scratch rerun produced byte-identical outputs:

- summary SHA-256: `82a388c780f0354ef5f7ba6d75a57c23a9f3a4fd3e92095bc40071ca478d4a0d`;
- rows SHA-256: `c2db23933affbb7ac0490e6619123b7d2fda3131d41c8faf9df5a5047f8b7e69`; and
- report SHA-256: `ccc1ef5d1cf4cbab6f9f2eb208da49e20bcdd7a704b302d2104654a732f949ad`.

### 7. Updated packet and public status surfaces

`Reproducibility Packet/README.md` now includes the copy-paste screen command, output paths, exact development decision, evidence boundary, and corrected downstream step numbering. The current-boundary section distinguishes the bounded mechanics/lifecycle advance from an information or recovery claim.

The root public `README.md` received one lean Live Run Status entry because the redesign resolves the previously public long-horizon mechanics blocker. It states the selected plane and negative control while explicitly retaining the fixed-stand-in, no-attribution, no-recovery-advantage, and no-freeze boundary.

## Challenges and how they were handled

### A conventional high-gain controller destabilized the flexible plant

The first scratch controller settings were too aggressive for the cable/rod dynamics. Rather than hiding that instability through saturated commands or relaxed safety thresholds, the controller authority was reduced and its target was bounded. Only the stable low-authority profile entered the committed screen.

### Controller timing and contact timing had to answer the causal question

The prior pilot contacted before the first diagnosis, making a recovery effect structurally untestable on the safety axis. This screen schedules one diagnosis at `2.272 s`, begins movement at `2.400 s`, and requires contact strictly later. The structure/actuator recovery actions therefore have authority before their respective contact episodes.

### One generated report line initially used the wrong held-step expression

The first generated Markdown report stated the wrong held step even though the row data and implementation used step 1136. The report generator was corrected to derive the value from the recorded row rather than reconstructing it with a separate formula. The committed artifacts were regenerated, then reproduced byte-for-byte.

### The mechanism screen needed a hard information boundary

Source-correct stand-ins are useful for proving that a controller can express an action, but they cannot support an attribution or performance claim. The code, report, packet runbook, public heartbeat, and handoff all carry that limitation explicitly. The next gate must replace the stand-ins with a matched noisy held-decision C1/S information mechanism.

## Important decisions and reasoning

- **Fix the task before retuning contact.** The angle violations were caused by the perpetual open-loop trajectory, so lowering the plane would not solve the actual safety failure.
- **Use delivered observations for task control.** Privileged plant truth remains limited to scoring; controller feasibility must survive the same sensor-delivery seam as the eventual experiment.
- **Make the diagnosis precede motion.** This is required for source-specific control to be capable of affecting the contact/safety outcome.
- **Evaluate once and hold.** The mechanism screen tests the explicit lifecycle correction identified by the prior pilot. It does not pretend that continuous phase-conditioned estimation has been solved.
- **Select the lowest all-source contact plane from the declared grid.** `z=0.200 m` is a development candidate because every lower declared plane misses at least one source, not because it maximizes a favorable metric.
- **Preserve unchanged A1 safety gates.** The redesign clears the existing limits; no threshold was relaxed to create a pass.
- **Separate mechanism, information, and control evidence.** This session advances only the mechanics/controller/lifecycle prerequisite. Attribution accuracy and recovery advantage remain open.
- **Keep configuration unfrozen.** The selected values are development candidates pending noisy information review, validation-sized calibration, leakage/storage/hash audits, and an evaluation-sized comparison.

## Files created

- `Reproducibility Packet/scripts/utils/task_control.py`
- `Reproducibility Packet/scripts/screen_bounded_task_contact.py`
- `Reproducibility Packet/tests/test_bounded_task_contact.py`
- `Reproducibility Packet/results/bounded_task_contact_screen/summary.json`
- `Reproducibility Packet/results/bounded_task_contact_screen/bounded_task_contact_rows.csv`
- `Reproducibility Packet/results/bounded_task_contact_screen/bounded_task_contact_report.md`
- `agents/Codex/Session Summaries/HumanReport17.md`

## Files updated

- `Reproducibility Packet/scripts/utils/recovery_control.py` — added validated external-nominal recovery composition.
- `Reproducibility Packet/scripts/utils/__init__.py` — indexed the new task-control module.
- `Reproducibility Packet/tests/test_recovery_control.py` — added external-nominal regressions.
- `Reproducibility Packet/README.md` — added the bounded screen runbook, result boundary, and corrected step numbering.
- `README.md` — appended one lean public bounded-redesign advancement entry.
- `chats/Claude-Codex/Phase 2 Integration and Config Freeze/Phase 2 Integration and Config Freeze - Active.md` — appended the exact owner-approved handoff under the transcript hard gate.
- `agents/Codex/README.md` — updated the workspace map and active review state.
- `agents/Codex/Summary of Only Necessary Context.md` — completely rewritten for Session 18.

No `.gitignore` change is required: packet-root `tmp/` is already ignored and the new tracked source, tests, small text/CSV/JSON artifacts, and documentation are intentional project records. No environment, cache, secret, scratch rerun, or large binary belongs in the commit.

## Verification performed

- New bounded-task/recovery focused tests: **19 passed**.
- Full Reproducibility Packet: **155 passed**.
- `compileall -q scripts tests`: passed.
- New CLI `--help`: passed.
- Default bounded-screen command with four workers: passed in 187.8 s and returned the exact advancement decision.
- Independent scratch reproduction: passed in 186.5 s; all three artifacts matched byte-for-byte.
- Strict-JSON audit: no `NaN` or `Infinity` tokens.
- Generated Markdown/CSV/JSON inspected; report, selection, and rows agree.
- Handoff append hard gate: pre-write 1,140 lines; new header exactly once at line 1,144; after the old tail; Codex physically last at line 1,186.
- Root Live-Run README heartbeat: updated with one lean development-only advancement entry.
- Final staged diff and repository synchronization are completed at closeout.

## Next steps / pending actions

1. **Claude first-reviews the exact new state.** The open loop covers the task controller, external-nominal recovery composition, bounded screen, tests, all three result artifacts, packet/public wording, and explicit evidence boundary. If Claude edits, Codex must genuinely owner-re-review the actual files before approval.
2. **Run the matched noisy held-decision information/reference-lifecycle review after approval.** Use this exact bounded mechanics condition, one declared held decision, matched C1/S common-random-number pairs, disjoint calibration/evaluation roles, and no source-correct stand-ins.
3. **Do not interpret stand-in control differences as a recovery result.** The evaluation-sized experiment must estimate tracking/safety differences with a real deployable information mechanism and the declared uncertainty reporting.
4. **Complete validation-sized calibration and action gating.** Healthy/four-class calibration, per-suite probability calibration, class/abstention/selective/OOD thresholds, persistence, and severity/onset grids remain open.
5. **Complete remaining pre-freeze audits.** Non-load-bearing sensor constants, final analysis window, whole-trajectory/fault-setting split, deployable-loader leakage, role hashes, multi-run storage, and immutable config/schema gates remain unresolved.
6. **Keep learned attribution and RMA post-freeze.** The fixed stand-in is not the learned head and cannot be promoted by wording or reuse.
7. **Keep `config.json` unfrozen.** `z=0.200 m`, task gains/limits/timing, references, thresholds, and learned components are still development candidates.
8. **Next regular Codex progress report:** Session 24, unless a Claim Sheet amendment or phase transition triggers an additional report first.

The central research question remains open. This session establishes that the bounded mechanics/controller/lifecycle seam is capable of one safe post-decision contact episode for every canonical source under known correct information; it does not establish that structural sensing supplies that information or improves control.
