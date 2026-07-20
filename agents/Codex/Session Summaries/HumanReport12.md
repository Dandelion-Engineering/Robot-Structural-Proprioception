# Human Report 12 — Codex

**Current Date and Time:** 2026-07-20 13:40 PDT

**Agent:** Codex · **Session:** 12 · **Project phase:** Phase 2 — Execution

---

## Summary

This session reviewed Claude Session 12's permanent coefficient-distance detector,
corrected one overclaim and one reference/threshold lifecycle defect, completed both
forward reproducibility fixes Claude identified in Codex's pilot, and built the first
interpretable recovery-controller floor against the real causal policy seam.

The coefficient detector's numerical core survived review: the pilot and permanent rung
now genuinely share the same joint healthy-standardized cosine/sine score statistic, and
the rung honestly detects change without claiming source attribution. The review narrowed
the surrounding claim, however. Sharing a score does **not** transfer the pilot's margin or
decision rates into the permanent detector because the validation reference, frozen
threshold, and persistence are still open. The implementation also allowed a healthy
reference to be re-fit without invalidating an old threshold or detection latch; that state
could silently combine a new score distribution with an old operating point. The edited
state now fails closed and awaits Claude's genuine owner re-review.

Codex also added `GainScheduledRecoveryController`, an explicit development floor rather
than a final adaptive controller. It preserves the nominal bounded task command unless a
non-abstained, localized, sufficiently certain diagnosis supports a structural safety
derate or actuator inverse-gain compensation. On the real MuJoCo plant, a one-hot diagnosis
of 50% remaining actuator gain caused a 2× request at the affected joint and restored the
nominal delivered torque exactly, without saturation. This is a verified interface/control
mechanism, not a closed-loop tracking result and not evidence on the research hypothesis.

The full Reproducibility Packet now passes **127 tests**. `config.json` remains deliberately
unfrozen.

## What was accomplished

1. **Completed the full AgentPrompt startup and context-first chat pass.** Read
   `Project Details/Project Details.md`, Codex's continuity file, every concluded-chat
   `Summary.md` involving Codex, and the complete active Phase-2 transcript before replying.
   Re-read the in-force `Claim Sheet.md` and the review-cycle, Reproducibility Packet, and
   Live-Run README playbooks before reviewing or editing their governed artifacts.

2. **Cross-reviewed Claude's latest work.** Read Claude Human Report 12, the exact
   `CoefficientReferenceDetector` implementation and tests, and commit `1a659db`'s diff.
   Independently exercised the score formula, quantile behavior, calibration guard, and
   focused estimator suite rather than relying on Claude's reported tests.

3. **Accepted the coefficient detector's core design.** Confirmed that it:
   - uses the retained cosine/sine coefficients jointly through
     `||(vector-mean)/scale|| / sqrt(D)`;
   - replaces the privileged matched counterfactual with a healthy calibration reference;
   - stays detection-only, spreads non-healthy probability uniformly, and abstains on
     structure/actuator/sensor type;
   - preserves W=768 / stride=16 as a pilot proposal, not a frozen value;
   - refuses to calibrate an operating tail without the caller's requested nominal tail
     support.

4. **Corrected the score/margin overclaim.** Claude's module and test wording said the
   permanent detector's deployed margin was the pilot's margin. That was too strong: the
   pilot used a 99th-percentile development threshold at one scheduled decision, while the
   permanent rung leaves the validation reference, false-alarm quantile, and persistence
   configurable. The edited wording now states exactly what is shared — the score
   statistic — and explicitly leaves margin and decision rates validation-owned. The
   W/stride rationale now says the matched C1 **minimum per-fault** detection was 0%, rather
   than implying C1 detected no faults at all.

5. **Fixed stale reference/threshold state.** `fit_reference()` now builds a new healthy
   reference atomically, invalidates any threshold when replacing a prior reference, and
   resets the rolling detection latch. A new regression proves that a detector re-fit to a
   second reference refuses to score until it is recalibrated and no longer carries the
   prior detection time. The tail-guard wording was also corrected: an undersized extreme
   quantile can collapse to or sit near the calibration maximum, but it is not universally
   *exactly* the maximum for every `far`, sample size, and quantile method.

6. **Canonicalized the pilot statistic.** Removed the pilot's duplicated coefficient-vector
   and distance implementations. `run_noisy_reference_pilot.py` now imports the two
   canonical helpers from `utils.estimator`, and a test pins function identity while the
   estimator test independently reconstructs the vector and normalized distance.

7. **Closed Claude's two pilot-forward reproducibility points.** Both pilot summaries now
   record their base seed (`1000` broad, `5000` follow-up), and their reports state the
   exact calibration/evaluation seed ranges. The advancing report now carries the same
   threshold-resolution caveat as the BLOCK report: with 32 calibration seeds the 99th
   percentile is the maximum leave-one-out score, and 2.1% worst-alignment false alarms
   mean one event in 48. Both reports were regenerated to a temporary file from their
   amended JSON summaries and matched the committed report text after newline
   normalization. No grid was rerun and no metric or decision changed.

8. **Built the first interpretable recovery-controller floor.** New
   `scripts/utils/recovery_control.py` contains:
   - `RecoveryControlConfig`, with explicit provisional probability, uncertainty, derate,
     gain-compensation, and torque-limit settings plus fail-loud validation;
   - `GainScheduledRecoveryController`, a callback compatible with
     `EstimatorCommandPolicy` that consumes only deployable `EstimatorOutput` plus time;
   - a safe fallback to nominal command for healthy, abstained, tied/ambiguous,
     unlocalized, invalid-severity, or overly uncertain outputs;
   - an explicit structural global derate (safety response, not claimed repair);
   - probability-weighted, capped inverse-gain compensation for a localized actuator loss.

9. **Verified the recovery path against the actual plant.** The focused unit suite checks
   healthy/abstained fallback, structural derating, missing-location/uncertainty fallback,
   callback compatibility, and malformed configuration. A real `CablePlant` regression
   applies a 50%-remaining joint-1 actuator fault at onset and verifies that the
   controller's 2× request restores nominal delivered torque exactly with no saturation.

10. **Updated the packet runbook and current boundary.** The focused test command now
    includes estimator and recovery-controller tests. The boundary states that the
    coefficient-reference rung and interpretable controller floor exist but remain
    development increments under review, while learned attribution/RMA, validation,
    config freeze, and confirmatory work remain open.

11. **Completed the public heartbeat check.** Left the root `README.md` unchanged. The
    session produced development scaffolding and opened review states, not a completed
    artifact, phase close, pivot, or new public result. The existing 2026-07-20 pilot entry
    already carries the relevant public milestone; another entry would violate the lean
    log rule.

12. **Appended the active-thread handoff safely.** Read the physical UTF-8 tail, appended
    the Session-12 turn against a unique final block, immediately re-read the tail, and
    confirmed the new timestamped header occurs exactly once and is physically last.
    Codex explicitly approved the edited estimator/pilot state and the new recovery floor,
    and handed both to Claude. The estimator owner-re-review and controller first-review
    loops are open; approval is not inferred.

## Important decisions and reasoning

- **Approve the score, not the inherited margin.** Mathematical identity of a statistic is
  useful and worth pinning, but a detector's margin also depends on the fitted reference
  and threshold; its decision behavior additionally depends on persistence. Preserving
  those distinctions prevents the same kind of overclaim previously corrected between the
  clean 2.22× mechanics differential and the noisy deployable detector.
- **Invalidate state when the reference changes.** A threshold belongs to the reference
  distribution that produced it. Keeping it after `fit_reference()` changes the mean,
  scale, and null distribution is a silent calibration leak. Failing closed is the only
  safe lifecycle.
- **Canonicalize forward.** The pilot loop was already closed, so the code duplication was
  removed as a forward implementation increment rather than treating the earlier approved
  result as wrong. Recorded metrics and decisions were preserved exactly.
- **Make recovery conditional on actionable attribution.** The current coefficient and
  novelty detectors abstain on source type, so they cannot trigger active compensation.
  That is intentional: inverse-gain scheduling without fault type, location, and severity
  would turn a detection result into an unsafe control guess.
- **Keep the controller modest.** The new controller is the smallest interpretable
  gain-scheduled floor required to exercise the diagnosis→control seam. It does not claim
  to solve tracking, structural repair, sensor-fault accommodation, or the headline
  comparison; those require the residual baseline, learned/oracle drivers, and controlled
  closed-loop evaluation.

## Challenges and how they were handled

- The initial venv test launch was blocked by the session's restricted execution
  permission even though the required interpreter existed. Randy changed the permission
  profile to full access and explicitly told Codex to continue; the exact required
  `venv\Scripts\python.exe` command then passed. Codex did not substitute bare Python.
- The first real-plant diagnostic used the wrong actuator-fault subtype string
  (`gain_loss`). The plant failed loudly as designed. Codex inspected the canonical fault
  library, reran with `actuator_gain_loss`, and obtained exact nominal delivery.
- Manually patched report text initially differed byte-for-byte from temporary regenerated
  output only because of CRLF/LF. After newline normalization, both reports matched their
  generator exactly; no content drift was present.

## Files created

- `Reproducibility Packet/scripts/utils/recovery_control.py`
- `Reproducibility Packet/tests/test_recovery_control.py`
- `agents/Codex/Session Summaries/HumanReport12.md`

## Files updated

- `Reproducibility Packet/scripts/utils/estimator.py`
- `Reproducibility Packet/tests/test_estimator.py`
- `Reproducibility Packet/scripts/run_noisy_reference_pilot.py`
- `Reproducibility Packet/tests/test_noisy_reference_pilot.py`
- `Reproducibility Packet/results/noisy_reference_pilot/summary.json`
- `Reproducibility Packet/results/noisy_reference_pilot/noisy_reference_pilot_report.md`
- `Reproducibility Packet/results/noisy_reference_pilot_threshold_followup/summary.json`
- `Reproducibility Packet/results/noisy_reference_pilot_threshold_followup/noisy_reference_pilot_report.md`
- `Reproducibility Packet/README.md`
- `chats/Claude-Codex/Phase 2 Integration and Config Freeze/Phase 2 Integration and Config Freeze - Active.md`
- `agents/Codex/README.md`
- `agents/Codex/Summary of Only Necessary Context.md`

`agents/Codex/references.md` is unchanged because no external source informed this
review/implementation session. The root `README.md` and `.gitignore` are unchanged after
their required checks.

## Verification performed

- Focused estimator + pilot tests: **36 passed**.
- Recovery-controller tests, including real MuJoCo plant compensation: **12 passed**.
- Full packet: **127 passed**.
- `compileall -q` over packet scripts and tests: passed.
- Pilot CLI `--help`: passed.
- Pilot result metadata: broad base seed = 1000; follow-up base seed = 5000.
- Both result reports match `write_report(summary)` after newline normalization.
- Active-chat header count = 1; new Codex turn is physically last.
- `git diff --check`: clean apart from line-ending warnings.

## Next steps / pending actions

1. Claude must genuinely owner-re-review Codex's edits to `estimator.py` / tests and the
   forward pilot dedup/metadata/report state. If Claude approves the exact state, that loop
   closes; if Claude edits, Codex must inspect and re-review the actual new state.
2. Claude reviews the new recovery-controller floor. It is explicitly approved by Codex
   but has only one approval today.
3. Codex implements the interpretable residual/linear-system-ID baseline against the same
   causal observation seam.
4. Build a bounded closed-loop development comparison that separates exact actuator
   delivery compensation from tracking recovery and safety; do not promote the current
   one-step plant regression into a control result.
5. Implement real MuJoCo endpoint-contact extraction before any optional-contact pilot.
6. Before confirmatory generation: settle validation-sized healthy references and all
   class/abstention/selective/OOD thresholds; severity/onset grids; non-load-bearing sensor
   constants; split/leakage/storage/role-hash audits; then freeze and hash the complete
   schema/config.
7. Learned temporal attribution and the RMA-style latent remain post-freeze. The central
   C1-vs-S diagnosis-and-control question remains unanswered.

Next regular Codex progress report: Session 16 unless a Claim-Sheet amendment or phase
transition triggers one earlier.
