# Human Report 13 — Codex

**Current Date and Time:** 2026-07-20 14:53 PDT

**Agent:** Codex · **Session:** 13 · **Project phase:** Phase 2 — Execution

---

## Summary

This session closed the two review obligations carried from Codex Session 12 and built
the Claim-Sheet-required interpretable residual/linear-system-identification baseline.
Claude Session 13 genuinely re-reviewed and explicitly approved both Codex's corrected
`CoefficientReferenceDetector` state and the new gain-scheduled recovery controller, so
both loops are now closed at same-state approval.

The new `LinearResidualAttributionEstimator` is a deployable-observation-only floor, not
a research result. It fits one normalized, affine, ridge-regularized ARX predictor on
healthy records from a single suite; reduces one-step prediction errors to transparent
signed-mean, RMS, and availability residuals; fits one residual centroid per canonical
source class on a separate labeled development role; and freezes an off-prototype
abstention threshold on a third known-class calibration role. The implementation rejects
fixed-suite mask drift, invalidates downstream calibration state whenever its upstream
model changes, and produces no location or severity estimate, so it cannot trigger active
recovery by itself.

Seven new focused tests pass, including a real six-step MuJoCo causal-seam smoke test.
The full Reproducibility Packet now passes **134 tests**. The baseline state is explicitly
approved by Codex and handed to Claude for genuine first review. `config.json` remains
deliberately unfrozen.

## What was accomplished

1. **Completed the full AgentPrompt startup workflow.** Read `AgentPrompt.md`, all of
   `Project Details/Project Details.md`, Codex's continuity file, every concluded-chat
   `Summary.md` involving Codex, and the complete active Phase-2 transcript before
   replying. Re-read the in-force `Claim Sheet.md` and the Reproducibility Packet,
   review-cycle, and Live-Run README playbooks before touching their governed artifacts.

2. **Reconciled live state against stale memory.** The memory snapshot ended at Codex
   Session 9, while the live repository had already reached Codex Session 12 and Claude
   Session 13. The live tree was clean at the start, and Codex's continuity file plus the
   physical chat tail correctly identified the current state. Live repository and chat
   evidence therefore controlled the session.

3. **Cross-reviewed Claude's latest contribution.** Read Claude Human Report 13 and the
   exact active-thread turn it summarized. Claude independently reproduced Codex's
   estimator lifecycle correction and the recovery controller's deployable/safety
   boundaries, then explicitly approved both exact states. No edits were made, so the
   coefficient-reference owner loop and the recovery-controller first-review loop are
   closed.

4. **Designed the residual baseline around explicit data roles.** The baseline has three
   separate stages rather than one blended fit:
   - `fit_dynamics(...)` receives healthy deployable records only and fits the nominal
     one-step model;
   - `fit_prototypes(...)` receives labeled development records for all four canonical
     classes and fits standardized residual centroids;
   - `calibrate_unknown_threshold(...)` receives a separate known-class calibration map
     and freezes the off-prototype abstention threshold.

   This structure makes the future manifest/split obligations visible in the API and
   prevents confirmatory code from silently fitting an operating point on evaluation
   records.

5. **Implemented normalized affine ARX prediction.** For every non-command scalar channel
   physically present in one suite, the model predicts `x[t]` from:
   - the present suite's sensor vector at `t-1`;
   - explicit validity bits for those prior sensor values;
   - the known exogenous `tau_cmd[t]`; and
   - its validity bits.

   Each scalar target is fit independently with ridge regularization. Invalid inputs are
   zero after healthy normalization and retain their validity bits; invalid targets are
   excluded only from that target's regression and residual, so one dropout does not
   discard an unrelated channel's transition.

6. **Added transparent residual features and attribution.** Each predicted scalar emits
   `[signed_mean_residual, residual_rms, valid_fraction]` over a window. The signed term
   preserves direction, RMS preserves magnitude, and valid fraction makes dropout an
   explicit residual rather than silently losing it. Standardized residual vectors are
   compared with one dimension-normalized centroid per source class. Class scores are a
   softmax over negative distances and are explicitly documented as comparison scores,
   not already-calibrated probabilities.

7. **Implemented honest abstention and detection persistence.** The baseline abstains if
   the window is farther than the known-class calibration threshold from every prototype
   or if the maximum class score does not clear the provisional confidence gate. The
   unknown threshold uses the higher-method `(1 - false_abstention_rate)` quantile and
   refuses a calibration set smaller than
   `ceil(min_tail_count / false_abstention_rate)`. All four known classes must be present.
   A non-healthy, non-abstained class must persist for the configured number of decisions
   before `detection_time_s` latches.

8. **Pinned the lifecycle between stages.** A successful dynamics re-fit atomically
   replaces the nominal model and invalidates old prototypes and the unknown threshold.
   A prototype re-fit invalidates the old unknown threshold. The online path refuses to
   score until all required stages are complete. This prevents residual centroids or an
   operating threshold calibrated under one nominal model from surviving under another.

9. **Enforced the matched-suite leakage boundary.** The baseline accepts only
   `ObservedRecord`, binds each fitted instance to one suite and scalar layout, treats
   `tau_cmd` only as the exogenous input, and checks `suite_available_mask` against the
   fixed C0/C1/S registry. A C1 record with S-only gauges unmasked fails loudly rather
   than gaining hidden structural information.

10. **Kept recovery claims bounded.** The baseline emits source-class scores but leaves
    `location_out=-1`, `severity_out=0`, and `severity_uncertainty=inf`. It therefore
    cannot satisfy the gain-scheduled controller's active-action gates. This is deliberate:
    the new artifact is an attribution floor, not an invented location/severity head and
    not a recovery result.

11. **Added seven focused tests.** They cover:
    - C1/S fixed-suite layouts and gauge exclusion/inclusion;
    - explicit rejection of a C1 mask that exposes S gauges;
    - correct held-out selection of four synthetic residual centroids;
    - tail-resolution and fit/prototype/threshold lifecycle guards;
    - persistence-latched online attribution with no recovery fields;
    - finite missing-target residuals with decreased validity fraction;
    - configuration and under-sized-fit validation; and
    - a real MuJoCo causal-seam smoke through `EstimatorCommandPolicy` and
      `GainScheduledRecoveryController`.

12. **Verified the real causal interface.** The six-step real-plant smoke executes
    `CablePlant → OnlineSensorSession → EstimatorCommandPolicy →
    GainScheduledRecoveryController`. Every applied command equals the nominal 50%-task
    command because the residual floor never supplies actionable location/severity. This
    verifies interface composition and the no-active-compensation boundary only; it is
    not a `J_5s`, safety, or tracking-recovery result.

13. **Updated packet-facing documentation.** Added the residual module to the shared
    utility index, added its test file to the packet's focused-test command, and rewrote
    the packet's current boundary. The runbook now records that the coefficient detector
    and recovery controller are jointly approved, while the new residual baseline awaits
    review and all synthetic/real-seam checks remain mechanism tests.

14. **Completed the public heartbeat check.** Left the root `README.md` unchanged. The
    session built development scaffolding and opened a review loop, but produced no new
    public result, phase transition, or frozen artifact. Adding a per-session log entry
    would violate the Live-Run README's lean running-log rule.

15. **Appended and verified the shared handoff.** Read the physical UTF-8 tail of the
    active Phase-2 transcript, appended the Session-13 turn against a unique multi-line
    tail block, immediately re-read the file, and confirmed the new header occurs exactly
    once and is physically last. Codex explicitly approves the exact new baseline state
    and asks Claude for genuine review; later use or silence is not approval.

## Important decisions and reasoning

- **Use residual system identification rather than another raw-feature novelty score.**
  The project already has observation-statistics and synchronous-reference detectors.
  The Claim Sheet calls for a distinct physics/dynamics-oriented interpretable floor.
  One-step prediction residuals test whether observed behavior departs from a healthy
  dynamical relationship instead of merely asking whether a summary feature moved.
- **Fit one generic architecture per suite, not one hand-coded rule per fault.** This
  preserves the matched-ablation design: C0, C1, and S use the same algorithm, while only
  the physically available channels differ.
- **Keep source prototypes simple and visible.** A nearest-centroid residual classifier is
  inspectable enough to be a genuine floor and expressive enough to produce the required
  four-class output. It does not compete with the future temporal network by quietly
  becoming another large learned model.
- **Make missingness part of the residual.** Encoder dropout is one of the declared sensor
  fault subtypes. Validity fraction must therefore remain visible to the classifier rather
  than being erased by complete-case filtering or silent imputation.
- **Require all known classes during abstention calibration.** A threshold calibrated only
  on healthy windows could reject ordinary in-class fault variability as unknown. The
  API therefore requires a four-class known calibration map, while still leaving the
  exact split and threshold validation-owned.
- **Do not invent location or severity.** Residual centroids demonstrate an interpretable
  attribution path; they do not automatically identify which component failed or by how
  much. Withholding those fields is safer and prevents the controller seam from converting
  a classification-only mechanism test into an active-control claim.

## Challenges and how they were handled

- **Stale memory versus live repository state.** The stored memory described Session 9,
  but the live continuity and transcript had advanced through Session 13. Codex followed
  the workflow rule that the live tree outranks old handoff state and did not redo closed
  work.
- **Encoding-sensitive index patch.** The first combined patch failed because its context
  included a mojibake-rendered section-symbol line in `utils/__init__.py`. The failed patch
  applied nothing. Codex verified the tree, split the additions into isolated patches, and
  anchored the small index change on ASCII-only text.
- **Initial focused-test path.** Running `./venv` from inside the packet folder failed
  because the project venv lives at the repository root. Codex reran the exact required
  root-relative interpreter from the repository root; no bare Python was used.
- **Early unknown-threshold test calibrated only healthy windows.** The first focused test
  correctly showed a held-out actuator window abstaining as off-prototype. That exposed an
  API honesty issue: known-class abstention calibration must represent every known class.
  Codex changed the calibration API to require an exact four-class mapping and updated the
  tests, rather than widening a threshold until the assertion passed.

## Files created

- `Reproducibility Packet/scripts/utils/residual_baseline.py`
- `Reproducibility Packet/tests/test_residual_baseline.py`
- `agents/Codex/Session Summaries/HumanReport13.md`

## Files updated

- `Reproducibility Packet/scripts/utils/__init__.py`
- `Reproducibility Packet/README.md`
- `chats/Claude-Codex/Phase 2 Integration and Config Freeze/Phase 2 Integration and Config Freeze - Active.md`
- `agents/Codex/README.md`
- `agents/Codex/Summary of Only Necessary Context.md`

`agents/Codex/references.md` is unchanged because no new external source informed the
implementation; the baseline follows the already-cited Dixon/Aghili/BIRDy residual and
system-identification rationale. The root `README.md` and `.gitignore` are unchanged after
their required checks.

## Verification performed

- Residual-baseline focused tests: **7 passed**.
- Full Reproducibility Packet: **134 passed**.
- `compileall -q` over packet scripts and tests: passed.
- Real six-step MuJoCo causal-seam smoke: passed; all commands remain exactly nominal.
- Active-chat Session-13 header count: exactly 1; new Codex turn is physically last.
- `git diff --check`: clean apart from line-ending warnings.

## Next steps / pending actions

1. Claude must genuinely first-review `residual_baseline.py`, its tests, the module index,
   and packet wording. If Claude edits, Codex must re-open the exact state and genuinely
   owner-re-review before the loop can close.
2. Add the shared fixed-attribution end-to-end seam regression Claude proposed: a fixed
   deployable stand-in should drive active compensation across multiple real-plant steps,
   while a detection-only/unlocalized arm stays nominal. Keep it labeled an interface
   mechanism, not a tracking result.
3. Build the evaluation-sized development comparison that separates exact actuator
   delivery compensation from `J_5s` tracking recovery and privileged safety. Do not
   promote one-step or short smoke tests into the headline control result.
4. Implement real MuJoCo endpoint-contact extraction before any optional-contact pilot.
5. Before confirmatory generation, settle validation-sized healthy/known calibration
   roles, probability/class/abstention/selective/OOD thresholds, severity/onset grids,
   non-load-bearing sensor constants, split/leakage/storage/role-hash audits, and then
   freeze and hash the complete schema/config.
6. Learned temporal attribution and the RMA-style latent remain post-freeze. The central
   C1-vs-S diagnosis-and-control question remains unanswered.

Next regular Codex progress report: Session 16 unless a Claim-Sheet amendment or phase
transition triggers one earlier.
