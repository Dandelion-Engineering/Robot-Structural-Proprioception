# Human Report 19 — Codex

**Current Date and Time:** 2026-07-22 14:43 PDT

**Agent:** Codex · **Session:** 19 · **Project phase:** Phase 2 — Execution

---

## Summary

This session closed Claude's corrective review of the noisy held-decision information artifact, made the Claim Sheet's existing tracking objective the explicit structural-action direction, and completed a role-separated development screen of the first tracking-directed action family.

Claude Session 19 independently reproduced the Session-18 evidence, then edited the verdict guard, interpretation boundary, and tests rather than approving the original state. Codex genuinely re-opened those exact edits. The new guard correctly requires information, action authorization, representative safety/lifecycle, matched pre-decision histories, and clean decision windows before either advancing label can be emitted; only the representative control result may separate full advance from information-only advance. The added report language correctly limits the result to one fixed fault setting per class and quantifies the minimum held-out prototype margin as 0.90. Codex independently ran the focused and full tests, regenerated the report byte-for-byte, and explicitly approved Claude's exact handed-back state. That review loop is closed.

The structural-action direction is now explicit: preserve the existing Claim Sheet tracking metric and seek a tracking-directed action rather than amending the contract after observing a graded contact-force reduction. The already-approved 0.75 global derate remains the transparent safety floor, but it cannot advance as the tracking-recovery action because it worsened the representative `J_5s` result.

Codex added a bounded inverse-stiffness action seam and screened a predeclared global/local multiplier family on the exact approved bounded mechanics. Tuning seeds selected the global 2.00 multiplier, which improved structural tracking by about 20%. Disjoint assessment reproduced that improvement safely, but a healthy false-authorization stress improved slightly more. The exact decision is:

`BLOCK_STRUCTURAL_RECOVERY_ACTION_FAMILY`

The screen therefore identifies generic nominal-controller under-authority, not a structural-specific recovery mechanism. No candidate advances. The inverse-stiffness implementation remains proposed code under Claude review, the default derate remains unchanged, and `config.json` remains unfrozen.

## What was accomplished

### 1. Closed Claude's Session-19 corrective review

Codex inspected the actual changed script, tests, report, and transcript rather than relying on Claude's summary. The accepted corrections are:

- a complete `lifecycle_pass` guard over information, action authorization, representative safety/lifecycle, matched pre-decision histories, and clean decision windows;
- verdict semantics in which only control sensitivity can separate full advance from information-only advance;
- a fixed-one-setting evidence boundary for the held-out sensor-noise result;
- generated quantification of the minimum held-out prototype margin, 0.90; and
- five explicit counterfactual failure tests while preserving the recorded split-advance fixture.

The recorded decision and four data artifacts remained unchanged; the report changed only to add the evidence boundary. Codex reproduced the focused file at 5 passed, the then-current packet at 160 passed, clean compilation/CLI/diff checks, and a byte-identical regenerated report. The active transcript contains Codex's explicit same-state approval, so that review loop is closed.

### 2. Preserved the approved floor while adding an explicit proposed action

`Reproducibility Packet/scripts/utils/recovery_control.py` now declares the structural action rather than hard-coding only one response:

- default `structural_action="derate"` preserves the unchanged 0.75 global command derate;
- proposed `structural_action="inverse_stiffness"` requires confident structural attribution plus valid location and remaining-stiffness estimates;
- compensation is probability-weighted, bounded by a declared maximum, and explicitly global or localized;
- missing or nonphysical location/severity returns the nominal command; and
- torque limits at the existing controller seam still bound the applied command.

This does not approve the proposed alternative. It exposes one auditable mechanism family for a development screen while leaving the jointly approved default intact.

`Reproducibility Packet/tests/test_recovery_control.py` now verifies global and localized compensation, the declared cap, fail-safe invalid estimates, configuration validation, and preservation of the old behavior.

### 3. Built a role-separated structural-action family screen

New `Reproducibility Packet/scripts/screen_structural_recovery_action.py` keeps the previously approved bounded task/contact/controller timing and fixed source-correct structural diagnosis constant. This isolates the controller mechanism; it does not test noisy attribution, probability calibration, or evaluation-sized recovery.

The predeclared candidate family is:

- current global derate 0.75;
- no action 1.00;
- global inverse-stiffness caps 1.10, 1.25, 1.50, and 2.00; and
- localized caps 1.25, 1.50, and 2.00.

Role separation is explicit:

- tuning-only sensor seeds 15000–15002 select at most one candidate; and
- disjoint assessment seeds 15100–15103 test both correct structural authorization and healthy false authorization.

Every advancing candidate must satisfy:

- at least 10% paired `J_5s` reduction on every structural seed;
- exactly one held diagnosis and no pre-decision action;
- exact paired pre-decision common-random-number hashes;
- zero A1 safety incidents;
- zero actuator saturation; and
- strictly greater mean benefit on structural-fault cases than healthy cases.

The last gate prevents a generic gain change from being mislabeled as structural recovery.

### 4. Recorded a deterministic, informative block

Tuning-only results were:

| Candidate | Mean `J_5s` reduction | Minimum reduction | Tracking gate |
|---|---:|---:|---|
| current derate 0.75 | -18.46% | -18.54% | BLOCK |
| no action 1.00 | 0.00% | 0.00% | BLOCK |
| global 1.10 | 4.66% | 4.59% | BLOCK |
| global 1.25 | 8.88% | 8.80% | BLOCK |
| global 1.50 | 13.48% | 13.44% | PASS |
| global 2.00 | 20.37% | 20.24% | PASS / selected |
| localized 1.25 | 2.40% | 2.28% | BLOCK |
| localized 1.50 | 4.14% | 3.99% | BLOCK |
| localized 2.00 | 6.16% | 6.07% | BLOCK |

On disjoint assessment, global 2.00 produced:

- structural mean reduction: 19.8837%;
- structural minimum reduction: 19.4002%;
- healthy false-authorization mean reduction: 20.1463%;
- structural-minus-healthy margin: -0.2626 percentage points;
- zero A1 safety incidents; and
- zero actuator saturation.

The structural tracking and healthy safety gates pass, but the source-specificity gate blocks. The controller is under-authorized on this task generally; the multiplier is not compensating a distinct structure-induced deficit. The correct next technical gate is to retune the common nominal controller first, then require a task/fault condition with a measurable structure-induced tracking deficit before screening another source-specific action.

### 5. Added tests, results, and runbook documentation

New `Reproducibility Packet/tests/test_structural_recovery_action.py` covers:

- disjoint seed roles and required comparison arms;
- selection by minimum paired reduction with safety overriding a numerically stronger candidate;
- blocking a generic gain change that helps healthy more; and
- blocking when the healthy false-authorization arm does not evaluate once or actually apply the selected action; and
- the positive path requiring tracking, safety, and source-specificity together.

New `Reproducibility Packet/results/structural_recovery_action_screen/` contains:

- `summary.json`;
- `candidate_rows.csv`;
- `tuning_rows.csv`;
- `assessment_rows.csv`; and
- `structural_recovery_action_report.md`.

Artifact SHA-256 values are:

- assessment rows: `4f3acb81cb6ba1df888a48bc3e0731c0620bcef5ce739b51129eaebfd9195aca`;
- candidate rows: `824e6de83be0cceea6c186d3f741af9fe1be23bb2beb693890debb8c89da01ce`;
- report: `3c4dc4587d2ba1f2c831d21ed33fcc055daf87179adb48ae5561fb0f4aa8f210`;
- summary: `bb29ad055a75e5ef954870ee6fcf90c89a48afd21056846369796ed7bc4b7b28`; and
- tuning rows: `acf4afc6cea52f96fa00661742bed968dc3a5fb5780018568d4d6ada91803054`.

The packet README now includes copy-paste Step 13, all output paths, the exact block, and downstream numbering through Step 17. Its current boundary keeps the fixed-source mechanism screen separate from noisy information and confirmatory evidence.

The root Live Run Status received one lean append-only milestone entry. It states that the first tracking-directed family blocked as a generic controller retune and records the next development gate without presenting the screen as a research result.

## Challenges and how they were handled

### A tracking improvement was not enough to establish structural recovery

The selected multiplier improved every structural assessment seed by more than the declared 10% floor, and did so without A1 or saturation failures. A structural-only screen would therefore have advanced it. The healthy false-authorization stress exposed the confound: the same action improved healthy tracking slightly more. Source specificity was made an explicit advancement gate, so the result blocks rather than relabeling a generic nominal-gain correction as fault recovery.

### The action screen needed to preserve the original safety floor

The new controller fields could have silently changed prior behavior. The default remains `derate` with the same 0.75 multiplier, and tests exercise that original path. The inverse-stiffness path must be explicitly selected and remains under review.

### Determinism needed to survive parallel scheduling

The recorded screen used eight workers. A complete independent regeneration used ten workers and produced byte-identical JSON, CSV, and Markdown artifacts. The temporary regeneration directory was deleted only after its exact path was resolved under the packet's `tmp` directory and all five hashes matched.

## Important decisions and reasoning

- **Keep the Claim Sheet's tracking metric.** The session did not amend the contract after observing the old derate's contact-force effect; the recovery action was instead re-aimed toward the declared control objective.
- **Keep the old derate as a floor, not a tracking result.** It remains transparent and approved, but its 18% tracking degradation prevents advancement to the evaluation-sized comparison.
- **Require source specificity.** A generic controller retune is useful engineering evidence, but it is not evidence that structural sensing enabled fault-specific recovery.
- **Retune the common baseline before another action family.** The healthy comparison shows the current nominal controller leaves generic tracking improvement available. That confound should be removed before interpreting a structural action.
- **Require an observable structural deficit.** A task/fault condition that does not make stiffness loss measurably harm the tracked outcome cannot demonstrate compensation for that loss.
- **Do not enlarge the information claim.** The S information result remains one fixed fault setting per class with sensor-noise variation, prototype outputs, and unresolved calibrated/OOD behavior.
- **Keep configuration unfrozen.** No action advanced and major validation/freeze gates remain open.

## Files created

- `Reproducibility Packet/scripts/screen_structural_recovery_action.py`
- `Reproducibility Packet/tests/test_structural_recovery_action.py`
- `Reproducibility Packet/results/structural_recovery_action_screen/summary.json`
- `Reproducibility Packet/results/structural_recovery_action_screen/candidate_rows.csv`
- `Reproducibility Packet/results/structural_recovery_action_screen/tuning_rows.csv`
- `Reproducibility Packet/results/structural_recovery_action_screen/assessment_rows.csv`
- `Reproducibility Packet/results/structural_recovery_action_screen/structural_recovery_action_report.md`
- `agents/Codex/Session Summaries/HumanReport19.md`

## Files updated

- `Reproducibility Packet/scripts/utils/recovery_control.py` — explicit unchanged default derate plus proposed bounded inverse-stiffness path.
- `Reproducibility Packet/tests/test_recovery_control.py` — new action and validation coverage.
- `Reproducibility Packet/README.md` — Step 13 runbook, results, evidence boundary, and downstream numbering.
- `README.md` — one lean append-only Live Run Status milestone.
- `chats/Claude-Codex/Phase 2 Integration and Config Freeze/Phase 2 Integration and Config Freeze - Active.md` — same-state approval of Claude's corrections and append-gated handoff of the new blocked family.
- `agents/Codex/README.md` — workspace map and current review state.
- `agents/Codex/Summary of Only Necessary Context.md` — completely rewritten for Session 20.

No `.gitignore` change is required. The new compact code, tests, JSON, CSV, Markdown, and documentation are intended project records. The independent regeneration was removed; ignored caches, the environment, and scratch data remain untracked.

## Verification performed

- Claude-edit focused review: **5 passed**.
- Structural controller plus screen focused tests: **27 passed**.
- Full Reproducibility Packet: **173 passed**.
- `compileall -q scripts tests`: passed.
- New CLI `--help`: passed.
- Recorded eight-worker screen: completed and returned `BLOCK_STRUCTURAL_RECOVERY_ACTION_FAMILY`.
- Independent ten-worker screen: all five artifacts byte-identical to the recorded outputs.
- Strict JSON: no `NaN` or `Infinity` tokens.
- Diff hygiene: clean; line-ending notices only.
- First transcript hard gate: pre-write 1,327 lines; approval header exactly once at line 1,331; Codex physically last at line 1,356.
- Second transcript hard gate: pre-write 1,356 lines; handoff header exactly once at line 1,360; Codex physically last at line 1,385.
- Final correction hard gate: pre-write 1,385 lines; correction header exactly once at line 1,389; Codex physically last at line 1,397.
- Root Live-Run README heartbeat: updated with one lean development-only blocker.
- Final staged diff hygiene and repository synchronization are completed at closeout.

## Next steps / pending actions

1. **Claude genuinely first-reviews the exact Session-19 action-screen state.** The loop covers the proposed recovery-controller changes, new screen and tests, five generated artifacts, runbook/public wording, and the block semantics. If Claude edits, Codex must genuinely owner-re-review the actual files.
2. **After approval, retune the common nominal controller.** Use healthy and physical-source development cases without turning the structural diagnosis into a tuning oracle.
3. **Require a measurable structure-induced tracking deficit.** Only then screen another structural action family against no action and a healthy false-authorization control.
4. **Preserve the noisy information boundary.** One fixed setting per class, uncalibrated prototype calls, compound/OOD faults, and selective-threshold validation remain open.
5. **Complete remaining pre-freeze audits.** Severity/onset grids, non-load-bearing sensor constants, final analysis window, whole-trajectory/fault-setting split, deployable-loader leakage, role hashes, multi-run storage, and immutable config/schema gates remain unresolved.
6. **Keep learned attribution and RMA post-freeze.** The prototype instrument is not the learned head.
7. **Keep `config.json` unfrozen.** Neither a structurally specific action nor the confirmatory design is approved.
8. **Next regular Codex progress report:** Session 24, unless a Claim Sheet amendment or phase transition triggers one first.

The central research question remains open. This session establishes that a large apparent tracking improvement can still be the wrong recovery result when it is not specific to the structural fault, and it turns that distinction into an executable gate before the evaluation-sized comparison.
