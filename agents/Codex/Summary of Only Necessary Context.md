# Summary of Only Necessary Context

**Rewritten:** 2026-07-22 18:55 PDT

**Last completed Codex session:** 22

**Next Codex session:** 23

**Current branch:** `main`

**Project phase:** Phase 2 — Execution

**Configuration:** explicitly **unfrozen**

## Resume state

Codex Session 22 first-reviewed Claude's deployable actuator-severity ridge head and severity-estimation-quality screen. The estimator implementation is sound, but the handed-off screen conclusion was not.

Claude's original screen omitted **0.50 remaining actuator gain** from its severity grid. That setting is recorded by the preceding deficit screen, has an **11.66% exact-restoration ceiling**, and lies exactly at the recorded cap-2 action kink. The multiplier is flat only strictly below the boundary. Small C1/S estimation errors can straddle 0.50 and issue different commands, so the original claim that severity could not create a paired action difference was false.

Codex independently reproduced the boundary defect before editing, then corrected the screen, tests, four artifacts, and packet wording. The current result is:

- C1 held-out severity MAE: **0.006472079**;
- S held-out severity MAE: **0.007632765**;
- cap-2 strictly capped interior: **0/12** paired commands differ;
- cap-2 0.50 boundary: **3/4** paired commands differ;
- boundary mean absolute multiplier difference: **0.0330843**;
- boundary maximum absolute multiplier difference: **0.0694032**;
- cap 4 and above: all four paired commands differ at the 0.25 floor boundary.

The defensible interpretation is that both suites estimate actuator severity accurately under this linear read-out and that structural channels do not improve MAE, but severity remains a live action route at the above-bar cap boundary. Its actual paired `J_5s` effect must be measured in the actuator action review.

Codex explicitly approves the current edited screen state and handed it back to Claude for genuine owner re-review. **The loop is open until Claude explicitly approves this exact state or edits and returns it.** Silence, continuity text, or downstream use is not approval.

`SeverityRidgeHead`, the shared `_SCORE_STD_FLOOR`, and Claude's root Live-Run units-correction entry are approved unchanged. The public entry contains no severity-screen claim.

## Current severity-screen state

### Estimator

`SeverityRidgeHead` is a standardized linear ridge read-out with active-column handling, an unpenalized intercept, and atomic fit-state assignment. Independent reconstruction matched predictions to at most `6.4e-14` and reproduced selected penalties:

- C1 penalty: 1.0; 110 active features;
- S penalty: 0.1; 142 active features.

The head currently reports training residual dispersion as `severity_uncertainty`. That is not licensed for the controller's confidence gate. A held-out uncertainty definition remains open.

### Action regimes

For remaining gain `s`, cap `c`, and floor `f`, the actuator multiplier is:

`min(1 / max(s, f), c)`.

The current screen separates four regimes:

1. strictly capped interior: `s < 1/c`;
2. exact cap/floor boundary: `s = 1/c`;
3. severity-sensitive interval: `1/c < s < 1`;
4. identity/healthy boundary: `s = 1`.

Do not group the exact boundary with the flat interior. Estimation error across the one-sided kink changes the command.

### Evidence boundary

This is development-sized evidence from a matched linear severity read-out with class probability pinned to one. It is not:

- validation-sized severity evidence;
- a calibrated class-probability result;
- a held-out uncertainty result;
- evidence about structural or sensor-fault severity;
- a paired tracking/control result;
- confirmatory evidence;
- a frozen configuration.

Class probability remains a separate unmeasured route by which suites agreeing on the class could still command differently.

### Artifact hashes

- `arm_rows.csv`: `03372fd4086a05b5d59cb11b9e968917e3e6990f92fc03550aba39ebce5fb810`
- `window_features.csv`: `1f5e6ae8eb956b6f9406b43ad520afa9590e03336c3e1e57779aa358cd21e25d`
- `summary.json`: `07c6011fb0077649e12a50a412b29c63f9d150512973f3304ff50e8c49b1a1d0`
- report: `6d77c3ccd87cb2719e3fce772a58168b8921c1487088bc7322a10c1b0ce92349`

`summary.json` is strict JSON. Empty regime rates are `null`, not `NaN`, and generation uses `allow_nan=False`.

## Accepted deficit-screen state

The Session-21 deficit-screen review loop is closed and must not be reopened merely because the severity screen cites it.

Decision:

`ADVANCE_ACTUATOR_DEFICIT_ONLY_BLOCK_STRUCTURAL_DEFICIT`

Accepted gate and selection:

- required reduction target: 12%;
- equivalent healthy-relative deficit gate: 13.636%;
- selected actuator condition: 0.25 remaining gain;
- disjoint mean/min deficit: 23.16% / 23.03%;
- structural condition: BLOCK at every remaining-EI setting;
- fixed 0.05 rad encoder-bias control: 15.69% mean deficit.

This is no-action headroom only. It does not establish action efficacy, source specificity, deployable severity, or a sensor-suite control result.

The 0.50 setting remains a recorded physical condition even though it is not the mildest condition selected by the corrected deficit gate. It is valid and necessary in the severity/action boundary analysis because its exact-restoration ceiling clears the Claim Sheet bar.

## Accepted prior structural-action state

Decision:

`BLOCK_STRUCTURAL_RECOVERY_ACTION_FAMILY`

The inverse-stiffness code seam remains reviewed, but no structural action advances. On the current bounded task, structural strain becomes more informative while tracking deficit falls through zero; this is the predeclared diagnostic-only shape, not a control success.

## Control-layer constraint

Current development evidence still has the following shape:

- S has exclusive useful information on the structural class, but this task has no structural tracking deficit to recover;
- actuator and fixed sensor faults have tracking headroom, but C1 already detects those classes;
- actuator recovery can be useful engineering without automatically producing the Claim Sheet's paired S-over-C1 control win;
- the severity boundary and class-probability route prevent assuming the paired actuator effect is structurally zero before measuring it.

Keep detection, attribution, action reachability, action efficacy, source specificity, and paired sensor-suite control separate.

## Next technical gate after Claude's owner re-review

The next actuator action review must measure achievable paired reduction rather than infer it from headroom or multiplier differences.

Minimum requirements:

1. Include 0.50 remaining actuator gain as the recorded cap-2 boundary arm.
2. Use deployable C1/S severity estimates, with an oracle-severity ceiling reported separately.
3. Preserve exact seed-paired pre-fault histories and compare action versus no action over complete `J_5s` windows.
4. Report C1-versus-S paired tracking difference and uncertainty, not only within-suite recovery.
5. Include the same action falsely authorized on healthy and report source-specific margin separately.
6. Keep selection roles separate from assessment roles.
7. Report A1 safety, saturation, contact, and full decision lifecycle.
8. Address held-out severity uncertainty before using the confidence gate.
9. Measure calibrated class probability separately; do not treat one-hot prototype scores as calibrated.
10. Sweep the jointly binding `(maximum_gain_compensation, minimum_gain_remaining)` control surface without changing the Claim Sheet bar after seeing results.

## Verification state

- Full Reproducibility Packet: **220 passed**.
- Focused severity screen: **21 passed**.
- `compileall -q scripts tests`: passed.
- Independent ridge reconstruction: passed to `6.4e-14` maximum prediction difference.
- Independent 0.50-boundary reproduction: passed before production edits.
- Full screen reproduced with 10 and 8 workers.
- Both CSVs and Markdown report: byte-identical across worker counts.
- `summary.json`: byte-identical after deliberate strict `NaN`→`null` normalization.
- Strict JSON parsing: passed.
- Report regeneration from `summary.json`: byte-identical.
- Artifact non-finite-token scan: clean.
- `git diff --check`: clean except expected line-ending conversion warnings.
- No dependency installed.
- Root Live-Run README deliberately unchanged in Session 22.

## Transcript append state

Session-22 Phase-2 append:

- pre-write physical line count: 1,818;
- complete verified EOF anchor: 15 lines, one occurrence;
- Codex Session-22 header: exactly once at line 1,820;
- post-write physical line count: 1,851;
- physical last speaker: Codex;
- transcript diff: +33 / −0.

Operational rule: read the physical UTF-8 tail, record the pre-write line count, verify a complete multi-line EOF anchor is unique, and make the patch itself contain that entire anchor. After writing, assert header count, position after the boundary, physical-last speaker, and append-only diff before committing.

## Open / unfrozen items

- Claude's owner re-review of the corrected severity-screen state;
- actuator action family and paired `J_5s` review including the 0.50 boundary;
- compensation-cap / minimum-gain-floor pair;
- held-out severity uncertainty;
- per-suite calibrated class probability;
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

## Required startup sequence for Session 23

1. Re-read `AgentPrompt.md` and follow it exactly.
2. Read all of `Project Details/Project Details.md` and `Claim Sheet.md`.
3. Read this file.
4. Read every Codex-channel `Summary.md`, then all active transcripts completely to physical EOF before replying.
5. Read Claude's latest Human Report and continuity.
6. Inspect git status/HEAD and actual files before trusting this summary.
7. Process Claude's owner re-review of the exact corrected severity-screen state first. Close only on explicit same-state approval; genuinely re-review any further edit.
8. Keep `config.json` unfrozen unless every remaining gate actually closes.

## Closeout conventions to preserve

- Active chats are append-only under the full hard gate described above.
- Rewrite this continuity file completely at every completed Codex session.
- Add the next `HumanReportN.md` and keep `agents/Codex/README.md` purpose-oriented.
- Keep the public Live-Run README lean, append-only, and milestone-based.
- Review `.gitignore`, stage only intended files, run `git diff --cached --check`, then commit exactly `Codex Session N` and push.
- Next regular Codex progress report: Session 24 unless a Claim Sheet amendment or phase transition triggers one earlier.
