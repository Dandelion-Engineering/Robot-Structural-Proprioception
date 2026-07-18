# Human Report 8 — Codex

**Date/time:** 2026-07-17 17:04 PDT

**Agent:** Codex · **Session:** 8 · **Project phase:** Phase 2 — Execution (prior evaluation/online loops closed; estimator handoff corrected and returned for owner re-review; bounded diagnostic candidates blocked; complete config remains unfrozen)

## Summary

This session completed the required AgentPrompt workflow, closed the record on Claude’s same-state approval of Codex Session 7, reviewed Claude’s new diagnosis-estimator front, ran the highest-priority plant-side bounded-excitation sensitivity, and converted the previously empty contact/safety open item into an explicit field-and-threshold proposal. Because this is Codex Session 8, it also produced the required director-facing regular progress report in addition to the normal session record.

The estimator review found three contract-level defects that green tests had not exposed: the claimed fixed `[W,D]` tensor changed length during startup; every channel’s summary slope used the encoder time grid instead of that channel’s own measurement times; and the privileged oracle reported the run’s known fault class even before the fault onset. Codex corrected all three directly, tightened estimator-output validation and trace ordering, added regressions, and explicitly approved the edited state. The loop is now open for Claude’s genuine owner re-review of the diagnoses and implementations. `W=512` / `stride=8` remain a proposal for pilot sensitivity, not a frozen decision.

The bounded-burst work produced a more important plant/config finding. One- and two-cycle causal raised-cosine probes, starting at the fault boundary rather than conditioning the plant in advance, both failed to preserve every mechanics signature above the unchanged 10-microstrain credibility floor. The one-cycle probe produced structural/actuator/separation RMS values of 8.18/7.84/12.33 microstrain; the two-cycle probe produced 8.67/13.38/17.49. The continuous condition still cleared the mechanics screen at 10.56/23.36/23.36, but it had been active before the fault and drove motion beyond the new provisional safety envelope. The two-cycle healthy trace accumulated roughly 21.06 rad of joint rotation and reached 37.74 rad/s. Therefore the earlier feasibility PASS remains valid for selecting native cable mechanics, but **no current condition is approved as a short safe diagnostic and `config.json` must not freeze**.

The packet now passes **80 tests** and compiles cleanly. No confirmatory configuration or data were created, and no development trace was promoted.

## What was accomplished

1. **Completed the ordered context-first pass.** Read `AgentPrompt.md`, all of `Project Details/Project Details.md`, Codex continuity, every Codex-including chat summary and active transcript, the in-force Claim Sheet, the schema, Claude’s latest Human Report 8, the estimator implementation/tests, and the review-cycle, reproducibility-packet, research-progress-report, and live-run README playbooks. Confirmed a clean `main` at Claude Session 8 (`ce33596`) before edits and reproduced the **74-test** baseline.

2. **Recorded the two prior review loops as closed.** Claude’s Session-8 active-thread turn genuinely re-reviewed the evaluation-core and online-interface edits from Codex Session 7, independently reproduced their load-bearing behaviors, and explicitly approved the same states. Codex accepted those approvals in the new turn; neither loop remains pending.

3. **Reviewed the new estimator front against the contract rather than its test count.** Read all of `utils/estimator.py` and `test_estimator.py`, traced the consumer interface back through `OnlineSensorSession.available_record`, checked schema §§C/D/F, and independently reviewed Claude’s `coverage_at_risk` addition against Claim Sheet Slot 7. `coverage_at_risk` is correct as written: it returns the maximum threshold-realizable coverage whose selective risk stays at or below the pre-registered ceiling.

4. **Made startup tensors genuinely fixed-shape.** `WindowFeatureExtractor.window_tensor()` previously returned a tensor with the record’s current length `T`. During an online rollout that means `[1,D]`, `[2,D]`, …, `[W,D]`, contradicting the stated fixed architecture for the learned rungs. The extractor now receives an explicit positive `window_steps`, left-pads startup history with zero values accompanied by false validity masks, rejects records longer than `W`, validates channel shapes/mask dtypes, and always emits `[W,D]`. A regression verifies a 12-step startup record becomes an 80-step test tensor with 68 fully masked leading rows.

5. **Corrected channel-time semantics.** The summary feature extractor previously used `q_obs` measurement times for the slope of every registry column. Schema C deliberately preserves timing at channel level so asynchronous IMU/gauge samples remain auditable. Each column now uses its own channel’s `measurement_time_s`; valid samples with non-finite measurement times fail loudly. A hand-built test gives the IMU a time grid different from the encoder and verifies the correct per-second slope.

6. **Removed pre-onset oracle leakage.** `OracleInterface` was bound to a true source class and immediately emitted it at every update. That lets an oracle controller “detect” a fault before it physically exists. The interface now accepts `onset_time_s`, emits healthy/no location/no severity before onset, and emits the perfect fault class and parameters only at or after onset. A regression explicitly checks both sides of the boundary.

7. **Tightened estimator-output and trace validation.** Steps must be non-negative integers; decision times finite and non-negative; locations integral and at least `-1`; uncertainty cannot be NaN or negative (positive infinity remains the explicit unknown value); detection time must be NaN or causal; stacked trace steps/times must increase strictly. The `W=512` rationale was also corrected so it no longer claims a 1.02-second history contains a full 1.25-second cycle or creates a detection-latency floor.

8. **Implemented a bounded diagnostic envelope in the authoritative mechanics path.** Extended `CableModelConfig` with diagnostic start, optional duration, and ramp duration. Added validation for peak/frequency/start/duration/ramp, a causal symmetric raised-cosine envelope, and phase reset at burst start. The default (`duration=None`, start zero, ramp zero) preserves the archived continuous feasibility behavior. `CablePlant` validates excitation at construction. Tests verify a one-cycle burst starts/ends at zero, stays within the declared 1 N peak, has numerical net impulse zero, and rejects a ramp longer than half the burst.

9. **Built a portable bounded-burst sensitivity CLI.** Added `scripts/run_bounded_burst_sensitivity.py`, which accepts project-relative output, onset/load/frequency/cycle/ramp/numerical arguments; runs ordinary, continuous, and finite-cycle candidates on the same selected mechanics; evaluates the unchanged differential-signature checks; records force/impulse and healthy motion; writes `summary.json`, `burst_sensitivity.csv`, and a concise report; and never labels the result confirmatory. A focused `--bounded-only` option supports development reruns without repeating controls.

10. **Ran the selected-model sensitivity.** The canonical run used 17 points per link and a 0.1 ms MuJoCo step, with 1 N / 0.8 Hz excitation, fault onset at 1 s, one- and two-cycle bounded candidates, and a one-eighth-period raised-cosine ramp. Results:

    | Condition | Structure | Actuator | Structure–actuator | Mechanics |
    |---|---:|---:|---:|---|
    | Ordinary | 2.17 | 5.92 | 5.93 | BLOCK |
    | Continuous | 10.56 | 23.36 | 23.36 | PASS |
    | Bounded 1 cycle | 8.18 | 7.84 | 12.33 | BLOCK |
    | Bounded 2 cycles | 8.67 | 13.38 | 17.49 | BLOCK |

    Values are maximum gauge RMS microstrain over the candidate’s causal post-onset budget. Encoder relational checks stayed valid and its physical gauge/IMU histories stayed unchanged.

11. **Diagnosed why “make it longer” is not sufficient.** The archived continuous load was active before the fault, so the plant entered the post-fault interval already excited. The bounded candidates start honestly at the fault boundary. The two-cycle candidate recovered actuator/separation information but not the structural floor, while producing much larger accumulated motion. This distinguishes a mechanics-selection PASS from an acceptable diagnostic-control policy.

12. **Prepared explicit contact/safety semantics and thresholds.** Proposed `contact_state[2] = {tip_contact_force_n, tip_contact_active}` and `safety_flag[7]` consisting of two joint-angle, two joint-speed, tip-workspace, absolute-gauge-strain, and tip-contact-force flags; the existing two-wide saturation role stays separate. Provisional review thresholds are `|q|≤π rad`, `|qd|≤10 rad/s`, tip radius `≤0.82 m`, `|gauge_true|≤500 microstrain`, and tip contact force `≤5 N`. These are conservative development screening values, not hardware claims or frozen constants.

13. **Used the proposal to expose, not hide, a second blocker.** Ordinary/continuous/one-cycle/two-cycle healthy traces reached peak accumulated angles of 3.18/9.05/4.53/21.06 rad and speeds of 13.79/40.67/37.74/37.74 rad/s. Every current condition fails the provisional motion screen. Contact remains disabled in the MJCF, so the seventh flag cannot yet be exercised and zero-width contact/safety arrays remain forbidden for pilot/confirmatory generation.

14. **Completed the append-only coordination handoff correctly.** Read the physical UTF-8 tail, appended Codex Session 8 using the final unique Claude paragraph rather than a generic signature anchor, and immediately re-read the tail. The message records the estimator edits and explicit approval/owner handback, exact sensitivity evidence, contact/safety proposal, config BLOCK, and verification. It landed at the physical tail without correction.

15. **Updated the public live-run heartbeat.** The short diagnostic’s failure is a genuinely noteworthy negative method/config finding, so one lean entry was appended to the public README. It preserves the honesty boundary: the mechanics candidate remains selected, the central research question remains unanswered, and the current diagnostic must not be called short/safe or frozen.

16. **Wrote the required Session-8 progress report.** Created `agents/Codex/Progress Reports/Progress Report Session 8.md` at the Accessible-Piece bar, explaining the project’s causal spine, why excitation is an information/safety budget, what the bounded test found, what the estimator review protected, current blockers, and the next work.

## Important decisions and reasoning

### 1. The old mechanics PASS remains valid, but its scope is narrower than the desired diagnostic

The feasibility spike asked whether native cable mechanics can produce differential, credible strain signatures at all. The continuous condition answered yes. This session asked a different implementation question: does a finite post-change probe preserve those signatures inside a safety budget? It answered no for the two tested candidates. Treating that as a contradiction would erase the distinction between selecting a physics substrate and selecting an operational diagnostic policy.

### 2. Pre-fault conditioning is the load-bearing difference

The continuous sine existed before the fault; the bounded sine began at the fault boundary. Longer post-onset duration therefore does not reproduce the same initial state. The next design needs a closed-loop bounded probe/controller rather than an unbounded continuation of the feasibility forcing.

### 3. Safety must be executable before it can constrain the experiment

The schema already carried contact/safety arrays, but zero-width development placeholders could not falsify a “safe” claim. Proposing explicit widths, semantics, and conservative thresholds immediately exposed that all current command conditions exceed the motion screen. This is preferable to choosing thresholds after seeing the traces so that the existing probe passes.

### 4. `W` cannot be frozen merely because its consumer now exists

Claude’s proposed `W=512` is plausible, and the implementation now correctly enforces it as a fixed tensor shape. But 512 samples cover only about 82% of a 0.8 Hz cycle, and the diagnostic waveform itself is being redesigned. The pilot sweep remains necessary; the config should not freeze a window around a probe that just blocked.

### 5. Oracle ceilings must remain causal

An oracle is privileged, not prophetic. It may know the true fault perfectly once the fault exists, but exposing the run label beforehand would contaminate recovery-time and detection-delay ceilings. Adding onset awareness preserves the purpose of an upper bound without giving it future information.

## Challenges and how they were handled

- **The first full four-condition sensitivity exceeded a two-minute command ceiling.** No canonical partial result was trusted. The session reran the scientifically decisive one-cycle condition with controls, then added a bounded-only focused two-cycle run, and finally regenerated the canonical four-condition output under a longer verified timeout.
- **The new envelope test used removed NumPy API `np.trapz`.** NumPy 2 removed that alias. The test was corrected to `np.trapezoid`; the failure was explicit and no result depended on it.
- **An estimator patch initially failed because the patch context carried a mojibake-rendered section sign/em dash.** The tool changed nothing. The change was split into smaller ASCII/true-UTF-8 anchors and each patch was verified by focused tests and diff inspection.
- **The combined final verification command used the packet-relative `..\venv` path while standing at the repo root for the CLI help smoke.** The full 80-test suite and compileall had already passed; only the help subcommand failed to resolve. It was rerun immediately with the required root-relative `.\venv\Scripts\python.exe` and passed.
- **The generated report initially contained mojibake microstrain units and Markdown pipes inside column labels.** The generator and canonical report were corrected to plain `microstrain`, `Peak angle`, and `Peak speed`, keeping future regeneration clean.

## Files created or updated

Created:

- `Reproducibility Packet/scripts/run_bounded_burst_sensitivity.py` — portable selected-mechanics finite-probe sensitivity CLI.
- `Reproducibility Packet/results/bounded_burst_sensitivity/summary.json` — complete machine-readable configs, load budgets, mechanics/safety checks, result, and contact/safety proposal.
- `Reproducibility Packet/results/bounded_burst_sensitivity/burst_sensitivity.csv` — decision-facing candidate comparison.
- `Reproducibility Packet/results/bounded_burst_sensitivity/bounded_burst_report.md` — concise human-readable BLOCK record and role proposal.
- `agents/Codex/Progress Reports/Progress Report Session 8.md` — required regular director progress report.
- `agents/Codex/Session Summaries/HumanReport8.md` — this report.

Updated:

- `Reproducibility Packet/scripts/utils/cable_mechanics.py` — bounded envelope fields, validation, causal envelope, phase-reset force.
- `Reproducibility Packet/scripts/utils/cable_plant.py` — construction-time excitation validation.
- `Reproducibility Packet/scripts/utils/estimator.py` — fixed `[W,D]` startup padding, per-channel timestamps, causal oracle onset, stronger output/trace checks, corrected `W` rationale.
- `Reproducibility Packet/tests/test_estimator.py` — fixed-shape startup, per-channel timing, oracle-onset, validation/order regressions.
- `Reproducibility Packet/tests/test_feasibility_spike.py` — envelope boundary/impulse/validation tests and candidate-contract test.
- `chats/Claude-Codex/Phase 2 Integration and Config Freeze/Phase 2 Integration and Config Freeze - Active.md` — Session-8 review/config handoff at the verified physical tail.
- `README.md` — one lean bounded-probe negative-method heartbeat.
- `agents/Codex/README.md` — Session-8/progress-report map and current review/config states.
- `agents/Codex/Summary of Only Necessary Context.md` — complete rewrite for Session 9.

## Verification performed

- Pre-edit full packet baseline: **74 passed**.
- Focused estimator + mechanics tests after corrections: **24 passed**.
- Final full packet: **80 passed**.
- `compileall` over packet scripts and tests: passed.
- Bounded-envelope numerical contract: smooth zero boundaries, peak ≤1 N, net impulse within `1e-9 N·s`, invalid ramp rejected.
- Canonical sensitivity: ordinary + continuous + one-cycle + two-cycle, selected 17-point plant, 0.1 ms physics step, four matched cases per condition; artifacts regenerated successfully.
- CLI help smoke using the required project-root virtual environment: passed.
- Active chat tail: new turn is physically last and correctly timestamped; no correction required.
- Root and packet `.gitignore`: reviewed; caches, bytecode, virtual environment, logs, large numeric/model payloads, and local outputs are already covered. The small JSON/CSV/Markdown sensitivity evidence is intentionally tracked; no ignore change required.
- `git diff --check`: no whitespace errors; CRLF notices only.

## Progress-report and public-heartbeat decisions

Codex Session 8 is a per-agent every-eighth-session trigger, so the regular progress report was required and created in addition to normal work. No phase transition or Claim Sheet amendment closed, so no additional event-triggered progress report is due.

The public heartbeat was also warranted: a proposed short diagnostic failed both a finite-information sensitivity and a newly executable provisional motion-safety screen. That is exactly the kind of negative/pivot evidence the append-only live log exists to show. The entry explicitly avoids presenting it as a research result.

## Next steps / pending actions

1. Claude must genuinely re-open `estimator.py` and its tests, review the fixed-window, per-channel-time, oracle-onset, validation, and rationale edits, then explicitly approve the same state or edit and hand it back.
2. Claude/shared config review should assess the proposed `contact_state[2]`, `safety_flag[7]`, and provisional thresholds; none is frozen yet.
3. Codex should redesign the diagnostic/controller pair to stay inside an approved motion envelope while clearing the unchanged information floor. Do not merely extend the open-loop sine. Candidate families: closed-loop tip/joint probes, lower-amplitude multi-frequency sequences, or bounded pulse designs with damping/task stabilization.
4. Implement nonzero contact/safety roles in `CablePlant`; add endpoint contact truth and threshold flags before pilot data generation.
5. Jointly sanity-check remaining sensor constants, select severity/onset pilot grids, and run the proposed `W∈{256,512,768}`, `stride∈{4,8,16}` sweep only after the diagnostic design is coherent.
6. Keep `config.json` absent/unfrozen and all hashes `dev-` until every field converges. Before pilot/confirmatory generation, add the deployable-loader leakage test, whole-trajectory/fault-setting split audit, role-hash rejection, and nonzero safety/contact checks.
7. Continue toward Codex’s interpretable residual/linear-system-ID baseline and recovery controller after the shared diagnostic/safety interface converges.
