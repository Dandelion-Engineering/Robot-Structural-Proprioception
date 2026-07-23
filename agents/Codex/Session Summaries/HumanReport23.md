# Human Report 23 — Codex

**Session date and time:** 2026-07-22 21:11 PDT (checked at the shell immediately before creating this report)
**Phase:** Phase 2 — Execution
**Session type:** First review of Claude's cap-boundary action screen, uncertainty-role correction, fail-loud repair, independent reproduction, and owner handback

---

## Summary

This session processed Claude Session 23's same-state approval of my prior severity-grid correction and Claude's new cap-boundary action screen. The prior Session-22 review loop is therefore closed.

Claude's new screen answered the measurement question opened by that correction: at 0.50 remaining actuator gain and the recorded cap of 2.0, the two suites' deployable severity estimates straddle the controller kink on three of four disjoint sensor-noise assessment seeds. Direct paired rollouts show that the resulting tracking difference is small:

- mean paired S-minus-C1 reduction: **−0.1177 percentage points**;
- maximum absolute paired difference: **0.5154 percentage points**;
- mean no-action tracking deficit: **13.11%**;
- mean privileged-oracle recovery: **10.81%**;
- whole measured 1.50–2.00 multiplier-sweep span: **3.8083 percentage points**;
- Claim Sheet bar: **10 percentage points**.

The numerical measurement is reproducible, and `arm_rows.csv` remains byte-for-byte unchanged from Claude's commit. However, genuine review found three load-bearing problems in the handed-off interpretation and integrity boundary:

1. A leave-one-tuning-seed-out residual estimate was labeled as held-out uncertainty and used to claim an absolute suite-ranking inversion, even though the fixed ridge penalty was selected on those same tuning groups. The genuinely disjoint assessment residual standard deviations are **0.008393 C1** and **0.008029 S**, so the claimed absolute ranking inversion does not survive the assessment role. S still has worse assessment MAE because its bias is larger.
2. The 1.50–2.00 multiplier sweep was described as a bound on *any* severity read-out, and a local slope conversion was treated as a bound. The sweep is an empirical envelope for the recorded linear heads; it cannot close an arbitrary future read-out that commands below 1.50. The local calculation is a linearization, while the direct paired rollouts are authoritative.
3. Seven audit booleans were written to the result, but the program aborted only on the Step-15 no-action common-random-number mismatch. A false lifecycle, action/no-action, safety, saturation, or applied-multiplier condition could survive into a positive report.

I corrected those defects in place. The program now reports calibration-role cross-seed and genuinely disjoint assessment diagnostics separately; narrows the conclusion to the recorded linear heads and measured envelope; and fails loudly on every required audit condition. The exact-restoration shortfall is also scoped to the measured 0.50 boundary condition rather than transferred to the selected 0.25 condition.

I approve the current reviewer-corrected state and handed it back to Claude for owner re-review. Because these edits touch Claude-owned screen/report state, the loop remains open until Claude explicitly approves this exact state or edits and returns it. `config.json` remains unfrozen.

---

## Startup and context ingestion

I followed `AgentPrompt.md` as the controlling workflow:

1. Read all of `AgentPrompt.md`.
2. Read all of `Project Details/Project Details.md`.
3. Read Codex continuity.
4. Read every Codex-channel `Summary.md`, then both active transcripts completely through physical UTF-8 EOF.
5. Read the current Claim Sheet, Claude's `HumanReport23.md`, Claude continuity, and the relevant review-cycle, reproducibility-packet, and public-live-run playbooks.
6. Inspected clean synchronized `main` at `ad7d6ba` (`Claude Session 23`) before editing.
7. Re-opened the estimator utility, complete boundary executable, tests, all three artifacts, Step 16, Step 2, Current-boundary text, root heartbeat, and Claude's append before accepting any conclusion.

No director request was pending in the human transcript. No progress report was due; the next regular report is Session 24.

## Review findings

### Prior severity-grid loop closed

Claude explicitly approved my Session-22 corrected severity-grid state without further edits. That loop is closed at same-state approval.

### Estimator utility and runbook test command accepted

`leave_one_group_out_residuals` fits each fold without the held-out group, preserves the ridge-head behavior, and fails loudly on malformed grouping. The utility itself is approved unchanged.

The packet's Step-2 command now runs `pytest tests\ -q` rather than a stale enumerated list. It reached all 21 current test files and is approved unchanged. Focused subsets remain useful for debugging, but the whole-directory form is the durable packet verification command.

### Uncertainty roles separated

Claude's fixed-penalty leave-one-seed-out values are useful calibration diagnostics:

| suite | in-sample std | calibration cross-seed std | ratio |
|---|---:|---:|---:|
| C1 | 0.004237 | 0.006741 | 1.59x |
| S | 0.001951 | 0.011160 | 5.72x |

But the fixed penalty was selected from the same tuning groups. These numbers are not a nested post-selection estimate and do not occupy the disjoint assessment role.

I recomputed residuals from Step 15's recorded disjoint assessment predictions:

| suite | assessment std | in-sample understatement | assessment MAE |
|---|---:|---:|---:|
| C1 | 0.008393 | 1.98x | 0.006472 |
| S | 0.008029 | 4.12x | 0.007633 |

Training dispersion is optimistic for both suites, but the suite ordering changes between the internal calibration diagnostic and the actual assessment dispersion. S's higher assessment MAE comes from its larger residual bias, not a larger residual standard deviation.

The controller continues to use the calibration-role cross-seed values because consuming the assessment role to set the gate would violate role separation. Both values are far below `maximum_severity_uncertainty = 0.25`, so the gate stays open and all 40 arm results remain unchanged. The result is development guidance, not a frozen decision margin.

### Universal-bound claim narrowed

The direct paired arms support the narrow claim that the recorded linear heads produce a sub-bar tracking difference at the 0.50 / cap-2 boundary. The whole 1.50–2.00 sweep also remains below the bar.

They do not support:

- a bound on an arbitrary future read-out whose error commands outside that sweep;
- a mathematical bound from local slope times multiplier spread;
- closure of the cap-4 / 0.25-floor boundary;
- closure of class-probability effects;
- closure of the actuator class or a paired sensor-suite control result.

Code, result-schema names, report headings, Step 16, and Current-boundary text now call this a measured conversion envelope. The direct paired measurement is authoritative; the local-slope value is explicitly a linearization consistent with it.

### Integrity conditions made fail-loud

The screen now aborts unless all of these are true:

1. no-action arms reproduce Step 15;
2. the estimator evaluates exactly once;
3. no-action arms issue zero commands;
4. every action arm acts;
5. no A1 incident occurs;
6. no saturation occurs;
7. applied multipliers match commanded multipliers.

Parameterized regressions force each condition false one at a time and require a runtime failure. Explicit sweep multipliers must also lie strictly above 1 and below the separately supplied cap point, preventing a duplicate or re-clipped cap value from contaminating the local-slope calculation.

### Exact-restoration shortfall scoped to its evidence

At this 0.50 boundary condition, the privileged oracle realizes 93.2% of the analytic exact-restoration ceiling because tracking error accumulated before the held decision cannot be recovered later. The observation is valid for this condition and lifecycle.

It does not establish that the same 0.78-percentage-point shortfall or 93.2% factor applies to the selected 0.25 condition. The report and packet text now keep that transfer explicitly unmeasured.

## Changes made

### Technical implementation

- `Reproducibility Packet/scripts/screen_severity_action_boundary.py`
  - renamed the uncertainty calculation to its calibration role;
  - added disjoint-assessment residual diagnostics;
  - separated calibration and assessment understatement ratios;
  - renamed the universal “bound” object to a measured severity-difference envelope;
  - made direct paired rollouts authoritative over the local linearization;
  - restricted explicit sweep multipliers to the strict cap interior;
  - added a fail-loud audit gate covering all seven integrity conditions;
  - narrowed exact-restoration and route-closure language.
- `Reproducibility Packet/tests/test_severity_action_boundary.py`
  - updated role-safe uncertainty expectations;
  - added assessment-diagnostic coverage;
  - added strict sweep-boundary coverage;
  - added seven parameterized fail-loud audit regressions;
  - focused boundary coverage is now 28 tests.

### Generated and packet artifacts

- Regenerated:
  - `results/severity_action_boundary/summary.json`;
  - `results/severity_action_boundary/severity_action_boundary_report.md`.
- `arm_rows.csv` is unchanged.
- Updated packet Step 16 and Current-boundary text to preserve evidence roles and open gates.
- Root `README.md` deliberately remains unchanged: its latest heartbeat is only the now-jointly-approved Session-22 correction.

### Coordination and closeout

- Appended the formal review and handback to the active Phase-2 transcript under the hard append-only gate.
- Created this Human Report.
- Updated `agents/Codex/README.md` with Session 23 and the boundary-screen pointer.
- Completely rewrote `agents/Codex/Summary of Only Necessary Context.md` for Session 24.

### Deliberately unchanged

- `agents/Codex/references.md`: no external source was used.
- `.gitignore`: reviewed; it already excludes `/tmp/`, virtual environments, caches, logs, build outputs, lock files, secrets, local datasets, and model artifacts.
- `config.json`: remains explicitly unfrozen.

## Verification

### Full and focused checks

- Full Reproducibility Packet: **248 passed**.
- Focused cap-boundary screen: **28 passed**.
- `compileall -q scripts tests`: passed.
- CLI help: passed.
- Strict JSON parsing with non-finite constants rejected: passed.
- Artifact non-finite-value walk: passed.
- Stale universal-bound / ranking-inversion claim scan across executable, artifacts, and packet README: clean.
- No dependency installed.

### Independent numerical audit

- Loaded all 40 CSV arms independently.
- Required all seven summary audit conditions to be true.
- Recomputed the mean and maximum absolute paired S-minus-C1 reduction from per-seed rows.
- Recomputed disjoint-assessment standard deviations and mean absolute errors directly from Step 15's committed predictions.
- All values matched the corrected summary to machine precision.

### Determinism and artifact integrity

- Tracked regeneration: 10 workers.
- Independent rerun: 8 workers.
- All three artifacts matched byte-for-byte across worker counts.
- `arm_rows.csv` also matched Claude Session 23 byte-for-byte.

Current artifact SHA-256 values:

- `arm_rows.csv`: `DC897226E7159FAB42F0E72DFC630124388C72D6D5C8F3833D8F310495870D9E`
- `summary.json`: `4C56721D0323C0ACD870B4E15D67B7167E92639430AC2B60D9195803B6F2E2EC`
- report: `DBD5DF3B86C78637001B122128B11C783432AA76FA8C0EEB56E5F00DCE452E44`

### Append-only transcript hard gate

- pre-write physical line count: 1,944;
- verified 11-line EOF anchor occurrence count: one;
- pre-write hash rechecked immediately before writing;
- Codex Session-23 header occurrence after old boundary: one;
- post-write physical line count: 2,024;
- physical last speaker: Codex;
- transcript diff: **+80 / −0**.

## Review status and next steps

1. **Prior S22 severity-grid correction: closed.** Claude approved the exact corrected state.
2. **Current boundary measurement: Codex-approved after corrections; owner re-review open.** Claude must review the exact executable, tests, two changed artifacts, Step 16, and Current-boundary wording. Silence or downstream use is not approval.
3. **Recorded linear-read-out route: narrow development closure pending owner approval.** The direct paired difference is below the bar on the 0.50 / cap-2 boundary and the wider measured 1.50–2.00 envelope stays below it.
4. **Do not generalize the closure.** Arbitrary future read-outs outside the envelope, probability calibration, cap ≥ 4 / 0.25-floor behavior, the actuator action screen, healthy false authorization, source specificity, and evaluation-sized paired control remain open.
5. **Keep uncertainty roles separate.** Never wire training residual dispersion to the controller gate. Calibration cross-seed values can guide development but are not frozen margins; assessment stays assessment.
6. **Keep evidence lanes separate.** This is development-sized action-boundary evidence, not validation-sized recovery success, a paired Slot-11 win, or confirmatory evidence.
7. **Keep configuration unfrozen.** The action/controller surface, class probability, validation roles, thresholds, fault grids, learned heads, leakage/storage/hash audits, and Phase-3 deliverables remain unresolved.

No regular progress report was due. The next regular Codex progress report is Session 24 unless a phase transition or approved Claim Sheet amendment occurs earlier.
