# Human Report 7 — Codex

**Date/time:** 2026-07-17 15:42 PDT

**Agent:** Codex · **Session:** 7 · **Project phase:** Phase 2 — Execution (evaluation core corrected; causal online plant→sensor→policy seam implemented; complete config freeze and estimator/controller implementations remain open)

## Summary

This session closed the prior plant/sensor development-interface review loop, cross-reviewed Claude's Session-7 evaluation core, corrected four load-bearing scoring/statistics defects, and replaced batch replay as the sensor execution primitive with a genuinely stateful online path. A generic causal policy loop can now choose the next command from only the sensor values whose declared latency has elapsed, advance the MuJoCo plant one control step, and emit the next noisy observation. The same sensor implementation still serves the batch-facing persistence CLI, so there is one authoritative pathology model rather than separate batch and online versions.

Claude's re-review explicitly approved the exact Session-6 producer/sensor state Codex had approved, so that older loop is closed. The new Session-7 evaluation and online-interface states are explicitly approved by Codex and handed back to Claude because the corrections touch Claude-owned metrics, statistics, and sensor code. Those new loops remain open until Claude genuinely re-reviews the diagnoses and implementations and either approves the same state or edits and returns it.

The packet began the session at 51 passing tests and ends at **59 passing tests**. Python compilation passes. A direct comparison against the pre-session committed batch sensor implementation showed every channel value, validity mask, measurement time, and availability time to be bitwise identical on the same stochastic trace. A real MuJoCo matched C1/S online check also preserved bitwise common-random-number equality for all shared channels while keeping C1 gauge slots absent.

No confirmatory configuration was created. `config.json` remains deliberately unfrozen while the diagnostic excitation duration/envelope, contact/safety flag contract, `W`/`stride`, sensor constants, and severity/onset grids remain open. All current generated data remain development-only.

## What was accomplished

1. **Completed the ordered AgentPrompt context pass.** Read `AgentPrompt.md` in full; all of `Project Details/Project Details.md`; the in-force Claim Sheet; Codex continuity; every Codex-including chat summary and active transcript; the shared schema; the review-cycle, reproducibility-packet, and live-run README playbooks; Claude's latest Human Report 7 and continuity; and the clean repository state before replying or implementing.

2. **Recorded the prior interface loop as genuinely closed.** Claude's Session-7 turn re-opened the exact files and reproduced the evidence from Codex Session 6, then explicitly approved the same committed state (`70e6e4f`). Codex acknowledged that same-state approval at the start of the new chat turn rather than leaving the old handoff state stale.

3. **Reproduced Claude's evaluation baseline before reviewing.** Ran the full packet suite at the Session-7 baseline: **51 passed**. Then reviewed `metrics.py`, `stats.py`, and their tests against Claim Sheet Slot 7 and schema §G rather than inferring correctness from green tests.

4. **Corrected a truncated-window `J_5s` defect.** The original function integrated whichever samples happened to fall before `onset + 5 s`; a trace ending after two seconds still produced a value presented as the frozen five-second metric. `j_5s` now validates finite inputs, a strictly increasing uniform control grid, the exact onset sample, and the exact `onset + window_s` endpoint. It fails loudly when the declared analysis window is truncated.

5. **Made risk–coverage threshold-realizable.** The prior curve sorted samples and emitted a point after every row, so two equal-confidence cases could be split arbitrarily by input order even though no threshold can accept one and reject the other. The curve now emits only tie-group endpoints and is invariant to order inside a confidence tie.

6. **Aligned the OOD operating point with the in-force contract and held-out evaluation.** The prior helper set a threshold at 95% in-distribution acceptance, although Slot 7 specifies false acceptance at 95% unknown-detection sensitivity. It also selected and evaluated the threshold on the same cases. The corrected API selects `unknown_threshold_at_sensitivity` on validation OOD, freezes that threshold, and computes `ood_false_acceptance_rate` on held-out OOD. This preserves the contract's operating point and prevents confirmatory cases from selecting their own threshold.

7. **Corrected the bootstrap's training-seed dependence structure.** The original implementation independently resampled train-seed subunits inside each `pair_id`, treating seed as nested. The actual experiment is crossed: each trained seed is evaluated across all scenario/pair units. `hierarchical_bootstrap_ci` now requires a rectangular `pair_id × train_seed` grid, resamples the pair axis and the global seed axis independently, applies the same sampled seed columns across every sampled pair row, and keeps each C1/S comparison together inside its cell. A regression test fails if global seed alignment is broken.

8. **Tightened fail-loud metric inputs.** Hard predictions must be integer known-class indices (plus the explicit abstain sentinel only where allowed); abstention and OOD flags must be boolean; confidence and thresholds must be finite. These checks keep malformed estimator output from being silently coerced into plausible metrics.

9. **Added a strict one-step observable adapter.** `ObservableStepSources` and `observable_step_sources(PlantStepState)` expose only time, true joint angle as the physical encoder source, requested command, upstream control effort, IMU truth, gauge truth, and temperature. True delivered torque, deformation coordinates, curvature truth, task truth, contact/safety state, and labels remain unreachable from the sensor interface.

10. **Implemented `OnlineSensorSession`.** The new session advances the sensor model one current plant state at a time. It owns persistent CRN generators, constant biases, the previous encoder sample/mask for the causal derivative, gauge hysteresis state, and gauge random-walk drift. Sensor bias/drift/dropout faults activate at the declared control step in the observation path only. Every emitted `ObservedStep` includes values, validity, measurement time, availability time, latency, and the static suite mask.

11. **Kept one authoritative sensor implementation.** `SensorModel.observe()` now validates the complete privileged record, creates an `OnlineSensorSession`, feeds it the trace step by step, and stacks the emissions into an `ObservedRecord`. The obsolete vectorized channel implementations were removed. The batch CLI therefore remains compatible without becoming a second execution path.

12. **Added a bounded controller-facing causal history view.** `OnlineSensorSession.available_record(decision_time_s, history_steps=…)` keeps only an explicit past-only tail, preserves timing metadata, and masks any channel row whose declared availability time lies in the future. The bound prevents quadratic history rebuilding at 500 Hz and is the direct insertion point for the eventually frozen estimator `W`. With the current defaults, zero-latency encoder/current/IMU values become available at their measurement time, while each gauge sample is withheld for its declared 2 ms latency.

13. **Added generic online rollout orchestration.** `utils/online_loop.py:run_online_rollout()` invokes a policy callback before each plant advance, passing only the bounded delivered observation history. Its required `history_steps` parameter becomes Claude's frozen `W`; the development test uses two steps without pretending that value is final. The callback returns the command; `CablePlant.advance()` integrates the next physical step; the sensor session observes the resulting state. This realizes the schema's causal ordering without prematurely choosing the estimator or Codex's recovery controller.

14. **Added sensor-configuration validation.** Non-finite or negative noise, bias, quantization, drift, thermal, and latency values are rejected; hysteresis must be in `[0,1)`; dropout must be in `[0,1]`; reference temperature must be finite. Invalid constants fail before a rollout consumes plant state.

15. **Completed and recorded the explicit review handoff, including append-order recovery.** The main Codex Session-7 turn landed at the verified physical tail and was immediately re-read. A later bounded-window addendum used a broad `— Codex` anchor and landed after the earlier Session-6 turn. No content was removed or moved; Codex appended a timestamped transcript-order correction at the actual tail, repeated the authoritative bounded-window handoff, and re-read the final tail. Claude's genuine owner re-review is requested against that final state.

16. **Updated the public live-run heartbeat.** Added one lean entry noting that the previously connected body/sensor path now runs causally one step at a time with latency enforcement and exact batch-equivalence, while explicitly preserving the honesty boundary that this is scaffolding rather than a research result and that the confirmatory configuration remains unfrozen.

## Important decisions and reasoning

### 1. A green metric test suite is not enough when the tests encode the same mistake

Claude's 51 passing tests accurately exercised the implemented behavior, but three behaviors were not the contract's behavior: accepting a short trace as `J_5s`, splitting tied confidence scores, and selecting the OOD operating point at ID acceptance. Review therefore had to return to the Claim Sheet and schema. The correction tests now pin the contract rather than the previous implementation.

### 2. The OOD threshold must be selected before confirmatory evaluation

At a fixed unknown-detection sensitivity, selecting the threshold from the same held-out cases used to report false acceptance partly conditions the reported result on the test set. Splitting threshold selection from held-out scoring makes the freeze operational: validation OOD chooses the threshold; the confirmatory set only evaluates it.

### 3. Training seed is a global crossed axis, not a private replicate inside each scenario

One trained estimator seed is evaluated across many scenario pairs. Resampling a different seed independently for every pair destroys that shared model realization and can understate seed-level uncertainty. Sampling global seed columns and pair rows separately preserves both sources of variation and the C1/S pairing.

### 4. Online causality belongs in the execution primitive, not only in metadata

Storing `availability_time_s` is insufficient if the controller callback can still inspect the raw current value before that time. The new controller-facing view masks undelivered rows before a policy receives them. Persisted observations keep the raw measured value plus timing metadata for later audit; deployable decisions see only delivered history.

### 5. Batch persistence and online execution should share one pathology model

Maintaining a vectorized batch model and a separate stateful online model would invite subtle drift in random streams, faults, hysteresis, or dropout. Refactoring the batch wrapper to feed the online session step by step makes bitwise equivalence structural. The direct comparison to the previous committed implementation confirmed the refactor did not change established development outputs.

### 6. Do not freeze configuration fields around an absent estimator or untested burst

The generic policy callback creates the integration seam without guessing `W`, `stride`, model outputs, or controller gains. Likewise, the session did not call the existing continuous three-second excitation a short diagnostic burst. The remaining config fields stay visibly open until the responsible evidence exists.

## Challenges and how they were handled

- **The first large evaluation patch did not apply because its context used a mojibake-rendered em dash rather than the file's UTF-8 text.** The tool reported verification failure and changed nothing. The edit was split into smaller UTF-8-anchored patches and then checked with `git diff`.
- **The first old-versus-new sensor comparison differed by roughly `1e-14` in derived velocity.** The cause was not stochastic drift: the prior batch implementation divided each derivative by its actual adjacent timestamp delta, while the initial online version used the nominal median `dt`. The session changed velocity and encoder-drift elapsed time to use actual sequential timestamps (still validated against the configured grid). The rerun was bitwise identical across every array.
- **The online interface had to expose a complete plant state to persistence without widening sensor authority.** The solution was a second narrow adapter for a single step, mirroring the already-approved record-level adapter; the session never receives the privileged-only fields.
- **Latency enforcement could have been left to every future estimator.** Centralizing the delivered-history mask in `OnlineSensorSession.available_record()` prevents each estimator/controller implementation from re-inventing or forgetting the same causality rule.
- **A final addendum repeated the known transcript-anchor failure mode.** The patch matched the first `— Codex` rather than the physical tail. Following the director's standing rule, the misplaced entry was preserved, a correction was appended at the true tail with the exact authoritative state, and the final tail was verified immediately.

## Files created or updated

Created:

- `Reproducibility Packet/scripts/utils/online_loop.py` — causal command-policy → plant → sensor orchestration and role-separated result carrier.
- `Reproducibility Packet/tests/test_online_loop.py` — incremental/batch equivalence, out-of-order rejection, invalid-config rejection, and real causal latency-policy tests.
- `agents/Codex/Session Summaries/HumanReport7.md` — this report.

Updated:

- `Reproducibility Packet/scripts/utils/metrics.py` — full-window `J_5s` enforcement, tie-safe risk–coverage, validation-selected OOD threshold + held-out false acceptance, and stronger input checks.
- `Reproducibility Packet/scripts/utils/stats.py` — crossed pair/seed bootstrap with global seed-axis resampling.
- `Reproducibility Packet/tests/test_metrics.py` — regression tests for tied scores, validation/test OOD separation, and truncated-window rejection.
- `Reproducibility Packet/tests/test_stats.py` — rectangular-grid validation and global seed-alignment regression.
- `Reproducibility Packet/scripts/utils/schema_types.py` — one-step narrow observable-source carrier and adapter.
- `Reproducibility Packet/scripts/utils/sensor_model.py` — sensor-config validation, `ObservedStep`, `OnlineSensorSession`, delivered-history masking, and batch wrapper refactor to the one authoritative stateful path.
- `Reproducibility Packet/scripts/utils/__init__.py` — online-loop module map and corrected crossed-bootstrap description.
- `chats/Claude-Codex/Phase 2 Integration and Config Freeze/Phase 2 Integration and Config Freeze - Active.md` — Session-7 review findings, edits, evidence, explicit approval, and owner handback.
- `README.md` — lean public heartbeat for the causal online execution milestone.
- `agents/Codex/README.md` — workspace map, Session-7 entry, and current review states.
- `agents/Codex/Summary of Only Necessary Context.md` — completely rewritten resume state for Session 8.

## Verification performed

- Baseline before edits: `python -m pytest Reproducibility Packet/tests -q` — **51 passed**.
- Focused corrected metrics/statistics suite — **29 passed**.
- Final full packet suite — **59 passed**.
- `python -m compileall -q Reproducibility Packet/scripts Reproducibility Packet/tests` — passed.
- Pre-session committed batch sensor implementation vs current stateful implementation on a 40-step, 500 Hz S trace with 4 °C thermal ramp and an encoder-drift fault — all channel values, masks, measurement times, and availability times bitwise equal.
- Real MuJoCo online C1/S paired rollout — shared channel values and masks bitwise equal under CRN; C1 gauge arrays all NaN; S gauge values finite where valid.
- Causal policy integration — policy received zero-latency encoder history at the next decision while the 2 ms gauge sample remained unavailable until its declared time.
- `git diff --check` — no whitespace errors; Windows line-ending notices only.
- `.gitignore` review — generated bytecode and pytest caches are ignored by the packet's own rules; no secret, local environment, large binary, or generated numeric artifact needs a new ignore rule.

## Public heartbeat and progress-report decision

This session made the schema's online execution order executable and closed a known batch-only development limitation. That is a genuinely noteworthy public-run milestone, so one lean running-log entry was appended. It explicitly says the work is scaffolding, not a research result, and that config remains unfrozen.

Codex Session 7 is not an every-eighth-session trigger. No phase transition or Claim Sheet amendment was approved, so no separate Codex research progress report is due. Codex Session 8 will require the regular progress report in addition to its normal work.

## Next steps / pending actions

1. Claude must genuinely re-review the four evaluation corrections and the online sensor/interface edits, then explicitly approve the same state or edit and hand it back. Do not infer approval from the handoff or future use.
2. Run the plant-side bounded-burst sensitivity before proposing the diagnostic duration/envelope. Preserve the continuous three-second gate condition and the ordinary-torque BLOCK as separate evidence while testing candidate burst shapes.
3. Propose explicit nonzero contact/safety field widths, semantics, and thresholds for pilot; keep saturation separate from unsafe excursions as schema §B requires.
4. Integrate Claude's estimator proposal into the generic policy callback when it lands, including justified past-only `W`/`stride` values and frozen validation-derived class/abstention/OOD thresholds.
5. Implement Codex's interpretable residual/linear system-ID baseline and recovery controller against the causal online seam once the shared interface/config review converges.
6. Before pilot, add the deployable-loader leakage test, whole-trajectory/fault-setting split audit, role-hash rejection, and multi-run storage checks. Before confirmatory generation, create and hash the complete immutable `schema.json` + `config.json`; reject every `dev-` trace.
