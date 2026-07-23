# Human Report 24 — Codex

**Session date and time:** 2026-07-22 23:02 PDT (checked at the shell immediately before creating this report)

**Phase:** Phase 2 — Execution

**Session type:** First review of Claude's actuator class-probability screen, continuous-response scope correction, independent dense audit, and owner handback

---

## Summary

This session followed `AgentPrompt.md` and processed Claude Session 24's same-state approval of the prior cap-boundary measurement plus Claude's new actuator class-probability screen.

The prior cap-boundary loop is now closed.

I independently reproduced the new screen's numerical finding:

- largest sampled gate-clearing S-over-C1 difference: **5.0698636256 percentage points**;
- mean sampled difference: **5.0162118584 points**;
- maximum separate gate-crossing authorization difference: **10.8508760759 points**;
- mean gate-crossing difference: **10.8203657342 points**;
- cap realization at 0.25 remaining gain: **57.5%** of the analytic exact-restoration ceiling.

The handed-off interpretation overclaimed what those rows establish. The controller constants exactly define a continuous probability interval, but the screen rolls out only six probabilities. Six samples do not exhaust a continuous nonlinear response. The implementation also compared only the endpoints while calling them the widest possible graded pair, so a worse non-monotone interior sample would have been missed.

A second boundary was also collapsed into the probability claim. The fixture holds class, location, severity, severity uncertainty, and abstention fixed. It therefore isolates graded probability sensitivity but cannot close calibrated probability-gate, abstention, or uncertainty-gate authorization. The measured 10.85-point gate crossing clears the bar and demonstrates why authorization must remain separate.

I corrected the implementation, tests, report, runbook, packet boundary, and public Live-Run state. The screen now searches every ordered sampled pair, records the probabilities producing the extrema, reports sampled monotonicity, requires the complete arm grid, and calls the result a sampled empirical envelope. A synthetic regression proves an interior non-monotone maximum is found. The root Live-Run log remains append-only; a correction follows Claude's earlier closure claim instead of rewriting it.

I approve the current reviewer-corrected probability-screen state and handed it back to Claude for owner re-review. Because the edits touch Claude-owned screen state, the loop remains open until Claude explicitly approves this exact state or edits and returns it. `config.json` remains unfrozen.

## Startup and controlling context

I completed the required startup sequence:

1. Read all 334 lines of `AgentPrompt.md`.
2. Read the complete Project Details file and current Claim Sheet.
3. Read Codex continuity and every Codex-channel `Summary.md`.
4. Read both active transcripts completely through their physical UTF-8 tails.
5. Read Claude Session 24's Human Report and continuity.
6. Inspected clean synchronized `main` at `8eb3557` (`Claude Session 24`).
7. Read the applicable review-cycle, reproducibility-packet, Live-Run README, and research-progress-report playbooks.
8. Re-opened the complete probability executable, tests, all three artifacts, Step 17, packet Current boundary, and root Live-Run entry before accepting any conclusion.

No human transcript message changed the task. Codex Session 24 triggered the regular every-eighth-session progress report, which was written during closeout.

## Review findings

### Prior cap-boundary loop closed

Claude explicitly approved the exact Session-23 reviewer-corrected cap-boundary state. That same-state loop is closed.

### Numerical result reproduced

The official screen contains 36 arms: no-action, healthy-reference, gate-probe, and six gate-clearing probability arms for each of four assessment seeds. All required arms are present.

The six-point curves are strictly monotone on every seed. Searching every ordered sampled pair preserves Claude's numerical endpoint result: the largest positive S-over-C1 value is 5.0698636256 points, below the 10-point Claim Sheet bar.

The gate crossing remains a separate authorization quantity. Comparing a withheld action with the best sampled acting arm reaches 10.8508760759 points and clears the bar.

### Exact input interval did not imply exact response closure

The recorded `source_probability_threshold`, probability upper bound, and capped compensation exactly determine the input and commanded-multiplier endpoints. The simulation response between those endpoints is still sampled.

The original implementation and prose treated p = 0.50, 0.60, ..., 1.00 as the whole reachable response and called the endpoint pair the widest possible difference. That conclusion required either:

- an analytical monotonicity/bounding proof for the full nonlinear rollout; or
- a claim restricted to the sampled grid.

The current evidence provides the second. I changed the screen and artifacts to say so.

### Dense reviewer audit strengthened but did not universalize the result

I created an ignored reviewer-only audit that rolled out p = 0.50 through 1.00 at 0.025 spacing on each assessment seed:

- 21 acting probabilities per seed;
- 84 MuJoCo arms total;
- every dense per-seed curve strictly monotone;
- largest paired value exactly 5.0698636256 points.

This is useful independent evidence that the six-point result is not hiding an obvious interior reversal on a 0.025 grid. It remains a finite empirical grid, not a continuous proof, and is not committed as a new approval surface.

### Sampled extrema and arm completeness made fail-loud

The corrected analysis now:

1. constructs all sampled acting arms for each seed;
2. searches every ordered conventional/structural probability pair;
3. records the probabilities producing the largest positive paired value;
4. separately searches the withheld-versus-acting authorization comparisons;
5. reports whether each sampled per-seed curve is monotone;
6. requires every exact expected arm label for every seed.

Tests now include a synthetic non-monotone curve where the worst pair uses an interior p = 0.70 point, plus an incomplete-grid failure.

### Calibrated authorization remains open

The fixture gives both suites the same actuator class, location, severity, common RMS severity uncertainty, and non-abstaining state. That is appropriate for isolating graded probability.

It does not establish that future suite-specific calibrated outputs will:

- both clear the class-probability threshold;
- both avoid abstention;
- both clear the `severity_uncertainty` gate.

Those are authorization outcomes. They cannot be reported as closed by a fixed-action probability sweep, especially when the screen's own gate-crossing quantity clears the development bar.

The common RMS is a development fixture choice. It is not a frozen per-example predictive-uncertainty definition or decision margin.

### Cap and floor remain a joint action surface

At 0.25 remaining actuator gain, exact restoration needs a multiplier of 4.0 while the current cap allows 2.0. The action realizes 57.5% of the analytic ceiling. Raising the cap could recover more tracking, but it would also alter which severity estimates are behaviorally identical. The cap therefore remains an open joint control surface rather than a free improvement or settled constant.

## Changes made

### Probability executable

- Narrowed the module and report purpose to a sampled class-probability response.
- Replaced endpoint-only extrema with an all-ordered-sampled-pairs search.
- Recorded the probabilities producing per-seed graded and gate-crossing maxima.
- Added sampled per-seed monotonicity and aggregate monotonicity.
- Added an exact arm-grid completeness audit and fail-loud requirement.
- Renamed result fields from reachable/universal language to sampled language.
- Separated the exact input interval from the empirical rollout response.
- Removed last-channel, final-route, continuous-closure, and actuator-class closure claims.
- Preserved probability, abstention, uncertainty, cap/floor, and action-screen boundaries.

### Tests

- Updated result-schema and report expectations.
- Added an interior non-monotone sampled-extremum regression.
- Added an incomplete-arm-grid failure.
- Retained all prior lifecycle, CRN, gate, multiplier, safety, saturation, strict-JSON, and report tests.

### Artifacts and documentation

- Regenerated `summary.json` and the Markdown report.
- `arm_rows.csv` remained byte-identical.
- Updated packet Step 17.
- Added an explicit superseding reviewer correction after the packet's stale long Current-boundary paragraph.
- Appended a correction to the root Live-Run running log without editing the earlier entry.
- Appended the formal review and owner handback to the active Phase-2 transcript.
- Created `Progress Report Session 24.md`.
- Created this Human Report.
- Updated Codex README and completely rewrote Codex continuity.

### Deliberately unchanged

- `config.json`: explicitly unfrozen.
- `agents/Codex/references.md`: added the verified scikit-learn macro-F1 teaching source used in the regular director report; the MuJoCo documentation family was already logged.
- `.gitignore`: `/tmp/` already excludes both reviewer-only rerun directories and the dense-audit script.
- No dependency was installed.

## Verification

### Tests and executable gates

- Focused probability-screen tests: **54 passed**.
- Full Reproducibility Packet: **302 passed**.
- `compileall -q scripts tests`: passed.
- CLI help: passed and describes a sampled response.
- Strict JSON parse: passed.
- Stale claim/key scan: clean except the intentionally preserved historical public entry and superseded packet paragraph, both followed by explicit corrections.

### Official and independent regeneration

- Official regeneration: 8 workers.
- Independent scratch reproduction: 4 workers.
- All three files match byte-for-byte across worker counts:
  - `summary.json`: `EA377BD0BCCD23CE3D7BDDC17B9C0107F16D9C36D8D2D0AB58AC10506D76AE3A`
  - `arm_rows.csv`: `F4E2D43B998BA9CAA46470E7313DBF6D2422D4CFC734E141887206F2751DDB60`
  - report: `44F39F4B665B7A4EB5DF9274D5A511508FBF1AE179376D8ED7508240C07D414B`

### Independent dense audit

- 84 reviewer-only arms.
- p = 0.50 through 1.00 in increments of 0.025.
- All four curves strictly monotone.
- Same 5.0698636256-point maximum.

### Append-only transcript hard gate

- pre-write physical line count: **2,199**;
- verified eight-line EOF anchor occurrence count: **one**;
- pre-write SHA-256 rechecked immediately before the patch;
- Codex Session-24 header occurrence after the old boundary: **one**;
- post-write physical line count: **2,290**;
- physical last speaker: **Codex**;
- transcript diff: **+91 / −0**.

## Review status and next steps

1. **Cap-boundary loop: closed.** Claude approved the exact Session-23 corrected state.
2. **Probability screen: Codex-approved after corrections; owner re-review open.** Claude must review the exact executable, tests, regenerated summary/report, Step 17, packet Current-boundary correction, and root Live-Run correction.
3. **Sampled graded result: below the bar.** The largest six-point sampled comparison is 5.07 points.
4. **Authorization: open and above-bar in the fixture.** The separate withheld-versus-acting comparison reaches 10.85 points.
5. **Continuous response: open between samples.** The dense audit strengthens the empirical envelope but does not prove a universal bound.
6. **Actuator class: open.** Healthy false authorization, action-versus-no-action benefit, cap/floor sensitivity, source specificity, sensor-fault recovery, and evaluation-sized paired control remain unresolved.
7. **Evidence lane: development only.** Four seeds, one task, one location, and one setting are not validation or confirmatory evidence.
8. **Configuration: unfrozen.** No shared configuration value changed this session.
