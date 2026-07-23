# Human Report 22 — Codex

**Session date and time:** 2026-07-22 18:55 PDT (checked at the shell immediately before creating this report)
**Phase:** Phase 2 — Execution
**Session type:** First review of Claude's severity-estimation-quality screen, boundary correction, independent reproduction, and review-cycle handback

---

## Summary

This session processed Claude's Session-22 handoff of a deployable actuator-severity ridge head and a two-part screen intended to decide whether severity-estimation quality could create different C1/S recovery commands. Claude's handed-off conclusion was that the route was closed at the recorded compensation cap: its analytic grid said no severity was both action-sensitive and above the Claim Sheet bar, and its empirical comparison found identical C1/S commands throughout the capped region.

I genuinely re-opened the estimator implementation, screen, tests, all four generated artifacts, packet Step 15/current-boundary text, root Live-Run entry, latest Claude report/continuity, and the Claim Sheet control definition. The new `SeverityRidgeHead` is sound, as is sharing `_SCORE_STD_FLOOR`; I approved those unchanged estimator edits. The root public entry also remains sound because it records only the already-approved deficit-units correction and makes no claim from the unreviewed severity screen.

The screen's central conclusion was not sound. `SEVERITY_GRID` omitted **0.50 remaining actuator gain**, even though the preceding deficit screen recorded that setting. At the recorded cap of 2.0, 0.50 is not inside the flat region: it is exactly the one-sided kink. Its exact-restoration ceiling is **11.66%**, above the Claim Sheet's 10% control bar. Estimation errors on opposite sides of the kink issue different commands, so omitting the boundary turned a live action route into a false structural-zero claim.

Before editing, I independently replayed the committed tuning features through Claude's handed-off heads on four new 0.50-gain assessment seeds. Three of four C1/S pairs straddled the kink, producing absolute multiplier differences of 0.0548, 0.0579, and 0.0368. I then added 0.50 to the screen, represented the exact boundary separately from the strictly capped interior, corrected the reachability and action analyses, expanded the regressions, and regenerated the artifacts.

The corrected result is narrow:

- held-out severity MAE is **0.006472 for C1** and **0.007633 for S**;
- at cap 2, all **12/12 strictly capped-interior** C1/S pairs still command identically;
- at the 0.50 boundary, **3/4** pairs command differently, with mean absolute multiplier difference **0.033084** and maximum **0.069403**;
- at caps 4 and above, all four pairs differ at the corresponding 0.25 floor boundary;
- therefore severity quality remains a live actuator-control route and its paired `J_5s` effect must be measured rather than assumed zero.

A final artifact-hygiene pass also found two non-standard JSON `NaN` tokens for empty boundary regimes. I changed absent rates to `null`, made JSON serialization fail loudly with `allow_nan=False`, and preserved `n/a` in the human report.

I explicitly approved the resulting edited state and handed it back to Claude for genuine owner re-review. Because I changed Claude-owned screen/report state, the loop remains open until Claude explicitly approves this exact state or edits and returns it. `config.json` remains unfrozen.

---

## Startup and context ingestion

I followed `AgentPrompt.md` in its required order:

1. Read all of `AgentPrompt.md` and treated it as the controlling workflow.
2. Read all of `Project Details/Project Details.md` and the current `Claim Sheet.md`.
3. Read Codex continuity.
4. Read every Codex-channel `Summary.md`, followed by all active transcripts through physical UTF-8 EOF.
5. Read Claude's latest `HumanReport22.md` and continuity.
6. Inspected clean synchronized `main` at `59701e2` (`Claude Session 22`) before editing.
7. Read the review-cycle, reproducibility-packet, and live-run-README playbooks relevant to the handoff.

No director request was pending in the active human transcript. No progress report was due; the next regular report is Codex Session 24.

## Review findings

### Estimator implementation accepted

`SeverityRidgeHead` standardizes active columns, solves ridge regression with an unpenalized intercept, writes fit state atomically after the solve, and zeroes inactive coefficients. Its current uncertainty is training residual dispersion and is not yet suitable for the controller confidence gate, but that limitation is reported and does not invalidate the read-out accuracy screen.

I independently reconstructed the fits and predictions. The selected penalties matched the recorded CV choices (1.0 for C1 and 0.1 for S), the prediction differences were at most `6.4e-14`, and both reported held-out MAEs reproduced.

The `_SCORE_STD_FLOOR = 1e-3` sharing is acceptable and does not alter the recorded detector-null state.

### Load-bearing boundary omission corrected

For the actuator multiplier,

`min(1 / max(severity, minimum_gain_remaining), maximum_gain_compensation)`,

the cap-2 command is constant only below 0.50. At exactly 0.50, an estimate on one side commands 2.0 while an estimate on the other commands less than 2.0. The boundary therefore needs its own regime; it cannot be grouped with the strictly capped interior.

The preceding deficit screen includes 0.50 and gives it an 11.66% exact-restoration ceiling. The handed-off grid jumped from 0.55 to 0.40, so the only recorded above-bar cap-2 boundary was absent. The claim that the smallest reachable cap was 3.0 and that no cap-2 severity could matter was therefore unsupported.

### Scope after correction

The structural conclusion is no longer “severity cannot create a paired effect.” The supported conclusion is:

- severity is already estimated accurately from both suites under this linear read-out;
- the additional structural channels make MAE slightly worse, not better;
- strictly capped-interior arms are behaviorally identical;
- a meaningful boundary arm remains live because small estimation differences can cross the kink;
- class probability remains another unmeasured route;
- neither route is yet a validation-sized or confirmatory sensor-suite control result.

## Changes made

### Technical and generated artifacts

- `Reproducibility Packet/scripts/screen_severity_estimation_quality.py`
  - added 0.50 to `SEVERITY_GRID`;
  - added explicit boundary reachability and action regimes;
  - updated oracle and C1/S command comparisons;
  - corrected report wording and MAE direction;
  - emits JSON `null` for absent rates and uses `allow_nan=False`.
- `Reproducibility Packet/tests/test_severity_estimation_quality.py`
  - added boundary reachability and command-difference regressions;
  - updated oracle-regime and absent-rate expectations;
  - focused screen coverage is now 21 tests.
- Regenerated:
  - `arm_rows.csv`;
  - `window_features.csv`;
  - `summary.json`;
  - `severity_estimation_quality_report.md`.
- `Reproducibility Packet/README.md`
  - corrected Step 15 and the current boundary so severity is narrowed, not closed.

### Coordination and closeout

- Appended the review decision and handback to the active Phase-2 transcript.
- Created this Human Report.
- Updated `agents/Codex/README.md` with Session 22 and the new severity-screen pointers.
- Completely rewrote `agents/Codex/Summary of Only Necessary Context.md` for Session 23.

### Deliberately unchanged

- Root `README.md`: Claude's current entry is an accurate append-only record of the already-approved units correction. The corrected severity screen is still in an open review loop, so no new public milestone was added.
- `agents/Codex/references.md`: no external source was used.
- `.gitignore`: reviewed and already correctly excludes the local `/tmp/` audit/rerun products and normal generated noise.
- `config.json`: remains explicitly unfrozen.

## Verification

### Independent numerical audit

- Refit/prediction reconstruction matched the implementation to at most `6.4e-14`.
- Initial independent 0.50-boundary audit reproduced command differences on three of four pairs before the production screen was edited.
- Corrected production results reproduced the MAEs, 3/4 cap-2 boundary differences, 0/12 interior differences, and cap-4 boundary differences.

### Determinism and artifact integrity

- Tracked run: 10 workers, 80 arms plus three projection checks.
- Independent rerun: 8 workers, 80 arms plus three projection checks.
- `arm_rows.csv`, `window_features.csv`, and the Markdown report matched byte-for-byte.
- `summary.json` matched byte-for-byte after the deliberate strict `NaN`→`null` normalization.
- Strict JSON parsing with non-finite constants rejected: passed.
- No `NaN`, `Infinity`, or `-Infinity` tokens remain in the four artifacts.
- The report regenerated byte-for-byte from strict `summary.json`.

Current artifact SHA-256 values:

- `arm_rows.csv`: `03372fd4086a05b5d59cb11b9e968917e3e6990f92fc03550aba39ebce5fb810`
- `window_features.csv`: `1f5e6ae8eb956b6f9406b43ad520afa9590e03336c3e1e57779aa358cd21e25d`
- `summary.json`: `07c6011fb0077649e12a50a412b29c63f9d150512973f3304ff50e8c49b1a1d0`
- report: `6d77c3ccd87cb2719e3fce772a58168b8921c1487088bc7322a10c1b0ce92349`

### Code and repository checks

- Full Reproducibility Packet: **220 passed**.
- `compileall -q scripts tests`: passed.
- `git diff --check`: clean apart from expected line-ending conversion warnings.
- No dependency installed.

### Append-only transcript hard gate

- pre-write physical line count: 1,818;
- verified 15-line EOF anchor occurrence count: one;
- new header occurrence count: one;
- new header line: 1,820, after the old boundary;
- post-write physical line count: 1,851;
- physical last speaker: Codex;
- transcript diff: **+33 / −0**.

## Review status and next steps

1. **Claude's original severity-screen conclusion is blocked and superseded.** It omitted the only recorded above-bar cap-2 boundary arm.
2. **Codex approves the current edited state.** Claude must genuinely owner-re-review the exact screen, tests, four artifacts, and packet wording. Silence or downstream use is not approval.
3. **Estimator and root entry are approved.** The unchanged `SeverityRidgeHead`, score-floor sharing, and public units-correction entry do not need reopening absent a new edit.
4. **Severity remains in the actuator action review.** The next screen must include 0.50 remaining gain, use deployable severity estimates, and measure the paired C1/S `J_5s` effect rather than infer it from multiplier differences.
5. **Uncertainty and probability remain open.** Replace in-sample severity residual dispersion before using the controller confidence gate; separately measure calibrated class probability.
6. **Keep evidence lanes separate.** This is development-sized linear-read-out and action-reachability evidence, not validation-sized attribution, recovery-control success, a paired sensor-suite result, or confirmatory evidence.
7. **Do not freeze partial configuration.** The cap/floor pair, probability and uncertainty channels, validation roles, thresholds, fault grids, controller/task/contact settings, learned heads, leakage/storage/hash audits, and evaluation-sized comparison remain unresolved.

No regular progress report was due. The next regular Codex progress report is Session 24 unless a phase transition or approved Claim Sheet amendment occurs earlier.
