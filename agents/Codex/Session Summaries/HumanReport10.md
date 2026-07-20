# Human Report 10 — Codex

**Current Date and Time:** 2026-07-19 22:06 PDT

**Agent:** Codex · **Session:** 10 · **Project phase:** Phase 2 — Execution

---

## Summary

This session reviewed Claude Session 10's synchronous estimator feature and
Safety-regression metrics. The review found one load-bearing information mismatch in the
synchronous feature, corrected it directly, added a narrow fail-loud guard to the paired
safety metric, and handed the edited state back for Claude's genuine owner re-review.

Claude's W=640 full-cycle choice, shared harmonic regression, channel-specific timing,
and phase-invariant amplitude calculation were individually correct. The problem was
that the estimator retained only amplitude. The safe-probe screen's 2.22× development
margin is computed from a harmonic regression on `fault_trace − reference_trace`.
Because the regression is linear, this is the Euclidean distance between the two
cosine/sine coefficient vectors. It is not the difference between their magnitudes.
Keeping only amplitude therefore discarded phase and could hide a change the screen
counted as detectable.

I reproduced the mismatch on the selected 50%-task / 0.05 N MuJoCo candidate at the
exact W=640 / 0.8 Hz state. The actuator-vs-healthy coefficient-vector distance is
0.898 µε, or 2.22× the 0.405 µε development floor. The largest change recoverable from
amplitude alone is 0.716 µε, only 1.77×. On the screen's gauge-1 channel, the amplitude
change is 0.266 µε versus a 0.898 µε coefficient-vector distance, retaining 29.6% of the
screened separation. Thus Claude's statement that the 2.22× margin was exactly what the
deployed estimator computed was too strong.

The edited feature now stores cosine, sine, and amplitude per registry column:
`[last, mean, std, slope, sync_cos, sync_sin, sync_amplitude, valid_fraction]`.
Cosine/sine preserve phase and make the clean paired coefficient distance reconstructible;
amplitude remains the phase-invariant summary. A focused test proves that two equal-
amplitude tones separated by 90° retain identical amplitude entries but distinct
coefficient vectors. The raw `[W,D]` tensor remains unchanged, and W=640 / stride=8
remain pilot proposals rather than frozen configuration.

Claude's safety point metrics were correct for the stated unsafe-step burden and use the
privileged-truth A1 flags. I added one pairing guard: the C1 and S safety traces must have
the same `[T,7]` control-grid shape before their rates are subtracted. This prevents a
truncated or differently sliced trace from silently entering a paired comparison.

The packet now has **102 passing tests** and compiles cleanly. The edited estimator and
metrics are explicitly Codex-approved, but the review loop remains open because Claude
must genuinely re-open and approve the exact edited state. `config.json` remains
unfrozen. The next pilot must evaluate noisy deployable observations against a healthy
reference; it may not promote the clean privileged 2.22× differential-to-null-floor
ratio as the deployed estimator's margin.

## What was accomplished

1. **Completed the AgentPrompt startup and context-first chat pass.** Read all of
   `Project Details/Project Details.md`, Codex continuity, every Codex-including chat
   summary, and the complete active Phase-2 transcript. Read the required review-cycle
   playbook before touching the handed-off artifacts.

2. **Cross-reviewed Claude's latest work.** Read Claude Human Report 10 and commit
   `1929bfa`, then inspected the exact `estimator.py`, `metrics.py`, focused tests,
   shared harmonic utility, schema A1 state, Claim Sheet safety bar, and current stats
   bootstrap implementation.

3. **Reproduced the handed-off baseline.** Ran the complete packet suite at Claude's
   state: **100 passed**. This established that the review finding was a contract/
   information issue rather than a failing existing test.

4. **Audited coefficient-space versus amplitude-space detectability on the real selected
   candidate.** Regenerated healthy, structural, and actuator cases at 17 points / 0.1 ms
   and W=640. Computed each gauge's cosine/sine vector, vector distance, and amplitude
   difference. This showed the exact inequality on actual data and quantified the
   actuator margin drop from 2.22× to 1.77× in the amplitude-only representation.

5. **Corrected the synchronous feature.** Replaced the amplitude-only import/use with
   `harmonic_coefficients`; expanded the per-column layout to retain cosine, sine,
   amplitude, and valid fraction; updated constants, docstrings, feature width, and all
   affected tests. W=640 and the one-period gate remain unchanged.

6. **Added a phase-retention regression.** Two pure 0.8 Hz tones with identical
   amplitude and a 90° phase difference now demonstrate the required contract: the
   amplitude entries match while the coefficient-vector distance remains `sqrt(2)·A`.

7. **Reviewed and hardened the safety metrics.** Approved the privileged-truth any-flag
   rate, per-flag attribution, and positive-means-regression sign convention. Added a
   same-control-grid shape check to `safety_regression_delta` plus a regression test for
   unequal paired extents.

8. **Recorded the review-cycle handoff.** Appended a detailed Session-10 review to the
   active Phase-2 chat, explicitly approving the edited state and leaving Claude owner
   re-review open. The first append again matched an earlier bare speaker signature and
   landed at line 61. I did not delete, move, or rewrite it; I immediately appended a
   dated physical-tail correction that restates the operative handoff and preserves the
   append-only record.

9. **Updated the public live-run status narrowly.** Read the live-run README playbook and
   appended one lean correction: the 2.22× clean coefficient-space margin is not a
   deployed-estimator result; the first amplitude-only handoff preserved only a 1.77×
   actuator margin, and the estimator now retains phase explicitly.

10. **Performed closeout hygiene.** Reviewed `.gitignore` and the ignored file set; all
    caches, virtual environments, local Claude state, and temporary folders remain
    correctly excluded. No dependency or external source was added.

## Important decisions and reasoning

- **Preserve the coefficient vector, not only its norm.** A norm is phase invariant but
  non-invertible. The clean screen's fault-minus-reference amplitude is the norm of a
  coefficient *difference*. Retaining both coefficients is the smallest sufficient
  representation that preserves the screened quantity; retaining amplitude alongside
  them keeps the convenient invariant summary.
- **Narrow the 2.22× claim rather than discarding the candidate.** The mechanics/safety
  screen remains useful as evidence that the plant generates a clean coefficient-space
  signature within the development motion envelope. What does not survive is the claim
  that this clean differential-to-null-floor ratio is already the deployed estimator's
  margin. The candidate remains pilot-eligible, subject to the right noisy/reference
  test.
- **Do not launch the W/stride pilot against the wrong representation.** The review
  changed what the pilot must measure. The next sweep should use noisy per-suite
  observations, a healthy/reference model, retained coefficient space, and explicit
  onset/stride alignment rather than merely rescoring privileged fault-minus-healthy
  mechanics traces.
- **Fail loudly on paired safety extent mismatch.** A difference of proportions is
  numerically defined even when the arrays cover different durations; that does not make
  it a valid paired five-second comparison. The guard catches this class of integration
  mistake early.
- **Keep configuration unfrozen.** This session corrected development machinery. It did
  not settle probe/task scale, W/stride, severity/onset grids, non-load-bearing sensor
  constants, validation-frozen thresholds, contact-enabled cases, learned attribution,
  or recovery control.

## Challenges and how they were handled

- **All handed-off tests passed despite the defect.** The tests proved phase invariance
  of amplitude but did not test whether phase information survived. I went back to the
  exact mathematical relationship between the screen and the estimator, then ran the
  selected plant cases rather than inferring from synthetic tones alone.
- **The transcript append failure recurred.** My first patch again used a non-unique bare
  `— Claude` signature and inserted the full turn near the top. Following the director's
  append-only recovery rule, I preserved every byte, added a dated correction at a
  verified unique physical tail, and re-read the tail immediately. This remains an
  operational failure to carry forward; future appends must patch against a multi-line
  unique tail block, never a signature.
- **The public log already contained the stronger 2.22× wording.** The log is append-only,
  so I did not rewrite that history. I added a new correction entry that narrows the
  earlier statement in place and keeps the public trail honest.

## Files created

- `agents/Codex/Session Summaries/HumanReport10.md`

## Files updated

- `Reproducibility Packet/scripts/utils/estimator.py`
- `Reproducibility Packet/scripts/utils/metrics.py`
- `Reproducibility Packet/tests/test_estimator.py`
- `Reproducibility Packet/tests/test_metrics.py`
- `chats/Claude-Codex/Phase 2 Integration and Config Freeze/Phase 2 Integration and Config Freeze - Active.md`
- `README.md`
- `agents/Codex/README.md`
- `agents/Codex/Summary of Only Necessary Context.md`

## Verification performed

- Baseline at Claude handoff: **100 passed**.
- Current full packet: **102 passed**.
- `compileall` over packet scripts and tests: passed.
- Selected-candidate independent coefficient audit: reproduced the 1.015 / 0.898 /
  1.090 µε clean vector distances and quantified amplitude-only retention per gauge.
- Phase-retention unit test: equal amplitudes remain equal while a 90° phase change is
  preserved as `sqrt(2)·A` coefficient distance.
- Safety pairing test: unequal C1/S control-grid extents fail loudly.
- `git diff --check`: clean (line-ending conversion warnings only).
- Chat physical tail re-read: the 22:06 transcript-order correction is physically last;
  the misplaced 22:04 turn is preserved and appears once.

## Next steps / pending actions

1. **Claude owner re-review:** genuinely re-open the cosine/sine/amplitude feature and
   safety pairing guard; explicitly approve the exact state or edit and hand back.
2. **Pilot contract:** after the loop closes, build/run the deployable noisy/reference
   pilot over probe/task scale, W, stride, onset alignment, and shared fault grids. Do
   not use the clean 2.22× ratio as the deployable margin.
3. **Safety integration:** make the eventual evaluation driver enforce the exact
   `[t_c,t_c+5 s]` control-grid slice before calling the approved point metrics.
4. **Codex plant lane:** continue the interpretable residual/linear-system-ID baseline
   and recovery controller; implement real endpoint-contact extraction before any
   optional-contact pilot.
5. **Shared freeze gates:** settle non-load-bearing sensor constants, severity/onset
   grids, validation-derived class/abstention/selective/OOD thresholds, split/leakage/
   role-hash audits, and complete immutable config/schema hashes before confirmatory
   generation.

No new external sources were used this session; the work was an empirical and code-level
review of the project's existing artifacts.
