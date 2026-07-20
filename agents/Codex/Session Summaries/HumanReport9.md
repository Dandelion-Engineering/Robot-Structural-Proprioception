# Human Report 9 — Codex

**Current Date and Time:** 2026-07-19 21:12 PDT

**Agent:** Codex · **Session:** 9 · **Project phase:** Phase 2 — Execution

---

## Summary

This session independently reviewed Claude Session 9's synchronous-detection claim,
corrected three implementation/honesty problems in that development artifact, implemented
the agreed nonzero contact/safety roles, and converted the detector-side idea into a
mechanics-coupled low-amplitude probe screen.

The detector-side conclusion survived in a narrower and more executable form. The
original W=512 calculation used sequential detrending and a phase-zero gain correction;
the recovered amplitude actually varied from 0.345 to 1.159 for the same unit tone as
phase changed. It also called a waveform a one-cycle burst even though the 1.024 s window
was shorter than the 1.25 s probe period, truncating and renormalizing the early part. I
replaced the statistic with a joint intercept + linear-trend + cosine + sine regression,
moved the development sensitivity to W=640 (1.280 s), and required the burst window to
contain a full period. The regenerated modeled synchronous floor is 0.111 ± 0.059 µε,
with a 0.405 µε development threshold and a 90× gate-floor/mean-floor ratio. The report
now says explicitly that a linear thermal ramp is a trend-rejection check, not an upper
bound on nonlinear or probe-band thermal effects, and that its injected signals are
surrogates rather than replayed mechanics.

I then measured that same feature on the actual four-gauge MuJoCo fault-minus-healthy
histories. A focused, bracketed grid found that 50% of the ordinary task-torque waveform
plus a 0.05 N, 0.8 Hz, one-cycle raised-cosine probe clears a deliberately conservative
2× detector-margin rule: structural 1.015 µε, actuator 0.898 µε, and
structure–actuator 1.090 µε, for a minimum 2.22× margin over 0.405 µε. Across healthy,
structural, actuator, and encoder scenarios, the worst angle was 1.895 rad, speed
3.909 rad/s, absolute gauge strain 38.83 µε, and tip radius 0.712 m, all inside the
unchanged development envelope. The 0.05 N / 40% row was safe but missed the margin at
1.69×; the 0.15 N rows violated the angle limit. The selected row therefore advances
only to the pilot sweep. It is not a config freeze, attribution result, or S-vs-C1 result.

The agreed two-field `contact_state` and seven-field `safety_flag` roles now exist in
the schema-facing types and `CablePlant`. I appended proposed schema Amendment A1 rather
than rewriting v1.0 history. Claude approved the underlying semantics in Session 9, but
the exact amendment text and implementation remain in an open review cycle: Claude must
genuinely re-review and explicitly approve the same state before A1 is jointly in force.

## What was accomplished

1. **Completed the AgentPrompt startup and context pass.** Read all of
   `Project Details/Project Details.md`, Codex continuity, every Codex-including chat
   summary, the physical tail of the active Phase-2 chat, `director_requests.md`, the
   root live-run README, and Claude's latest Human Report 9. Read the review-cycle,
   Reproducibility Packet, and live-run README playbooks before reviewing/editing those
   artifacts.

2. **Independently reviewed Claude's synchronous-floor artifact.** Read the exact
   script, tests, JSON/report outputs, and Session-9 diff. Reproduced the baseline and
   tested the statistic across 16 phases. This exposed the phase-dependent calibration,
   the truncated “one-cycle” surrogate, and the overly strong thermal-bound wording.

3. **Created shared phase-invariant harmonic logic.** Added
   `Reproducibility Packet/scripts/utils/synchronous.py`, which jointly fits intercept,
   linear trend, cosine, and sine on valid samples and returns phase-invariant harmonic
   coefficients/amplitude. Added rank, time-grid, and input validation plus a design
   condition-number diagnostic.

4. **Corrected and regenerated Claude's active artifact.** Updated
   `analyze_synchronous_detection_floor.py`, its focused tests, and
   `results/synchronous_detection_floor/`. The corrected default is W=640; a shorter
   one-cycle surrogate fails loudly. The report distinguishes the detector surrogate
   from the actual mechanics-coupled screen and no longer treats a modeled linear ramp
   as a bound on unmodeled thermal dynamics. I explicitly approved the edited state and
   handed it back for Claude owner re-review.

5. **Fixed safety evaluation at the privileged-truth boundary.** The earlier bounded
   screen checked only healthy motion. Expanding it across all scenarios first produced
   a false 25 rad/s encoder “safety” event, revealing that the mechanics carrier exposed
   only `qd_obs`. Added `SimulationResult.qd_true_rad_s`, computed independently from
   true joint history, and made every safety decision use true physical speed. Sensor
   corruption can no longer manufacture a privileged safety violation.

6. **Implemented contact/safety roles and proposed Amendment A1.** Added fixed role
   names/order and widths (`contact_state[2]`, `safety_flag[7]`) to `schema_types.py`,
   enforced them in record validation, updated the analytic fixture, and made
   `CablePlant` populate/evaluate the roles. The collision-disabled model writes zero
   contact truth; if contact unexpectedly appears, it fails rather than silently writing
   false zeros. Numeric limits live in `CableModelConfig` and remain development values.
   The appended schema amendment is explicitly Codex-approved and pending Claude
   same-state approval.

7. **Built the actual-trace safe-probe screen.** Added
   `scripts/screen_synchronous_safe_probe.py`, focused tests, and
   `results/synchronous_safe_probe/`. It imports the detector artifact's exact threshold,
   uses the same harmonic implementation on actual four-gauge traces, evaluates the
   structural, actuator, and structure–actuator comparisons, checks every safety limit
   across every scenario, and writes JSON/CSV/Markdown decision artifacts.

8. **Kept legacy evidence intact.** Regenerated the original bounded-burst artifact
   through the corrected all-scenario/true-speed safety code. The old 1.0 N one- and
   two-cycle conditions remain BLOCK under the legacy 10 µε per-sample gate and safety
   screen. The new detector-aware pilot candidate is a forward development decision;
   it does not rewrite the mechanics-selection record.

9. **Updated outward-facing and runbook surfaces.** Added one lean append-only root
   README heartbeat describing the independently corrected detector and selected
   development candidate. Expanded `Reproducibility Packet/README.md` with copy-paste
   steps for the bounded blocker, detector floor, and safe-probe screen, and corrected
   its stale online-interface/current-boundary description.

10. **Posted the review/handoff at the verified chat tail.** The Codex Session-9 turn
    appears once at the physical end of the active Phase-2 transcript. It explicitly
    approves the edited detector artifact and proposed A1 implementation, names both
    open owner-review obligations, recommends building Claude's synchronous estimator
    feature now that the probe spectrum is coherent, and keeps config freeze blocked.

## Important decisions and reasoning

- **Use joint harmonic regression, not phase-specific post-detrend projection.** On a
  sub-cycle window, separately detrending and then projecting onto non-orthogonal basis
  functions is phase dependent. One regression solves the nuisance and signal terms
  together and gives a stable feature definition suitable for both sensor and mechanics
  lanes.
- **Require a complete probe cycle in the default feature window.** W=640 covers 1.024
  cycles at 500 Hz/0.8 Hz. This is not because a shorter full-rank regression has a
  mysterious scalar “gain”; it is because the full cycle improves conditioning and
  prevents the bounded waveform from being truncated.
- **Separate generic detectability from executable plant margin.** Injected waveform
  surrogates can characterize the modeled detector floor, but only actual plant traces
  can establish whether a particular excitation produces the needed structure/actuator
  shapes while staying safe.
- **Safety truth cannot use corrupted observations.** The encoder-bias derivative spike
  was useful because it demonstrated exactly why schema-B safety must be computed from
  `q_true`/`qd_true`, never `q_obs`/`qd_obs`.
- **Use a 2× development margin.** The 0.405 µε threshold is modeled and not frozen.
  Requiring at least twice that value avoids advancing a row that clears only through
  numerical proximity. This is a pilot-screen rule, not a pre-registered confirmatory
  success threshold.
- **Append Amendment A1 and leave its review gate visible.** Schema v1.0 is in force and
  append-only. The new fixed widths/order are therefore an appended amendment with an
  explicit pending same-state review, not a silent edit to the earlier table.
- **Do not freeze configuration.** The selected row is eligible for pilot only. Sensor
  constants, severity/onset grids, validation-frozen decision thresholds, contact-enabled
  cases, stride/window sweep, learned attribution, and recovery control remain open.

## Challenges and how they were overcome

- **The initial low-force sweep looked safe only because safety examined healthy motion.**
  I expanded the screen across all scenarios, then discovered the encoder false-speed
  artifact and added true velocity to the mechanics carrier. This produced the correct
  physical safety assessment rather than backing away from the stricter check.
- **The first focused 0.1–0.3 task-scale grid had no 2× detector-margin pass.** I extended
  the grid to 0.4–0.5 task scale and 0.05–0.15 N probe force, then bracketed the selected
  row with a lower-force miss and higher-force safety failure. The result is a supported
  pilot candidate rather than an untested interpolation.
- **Selected-resolution sweeps are slow.** Each four-scenario candidate costs about 21 s
  at 17 points / 0.1 ms. I used short pure-function/unit tests for iteration, then ran the
  final decision artifacts at the exact selected resolution rather than substituting a
  coarser model.
- **The evolving packet README was stale.** I updated the runnable sequence and current
  boundary so an outside reader does not infer that the online seam is absent or miss the
  new development sensitivities.

## Files created

- `Reproducibility Packet/scripts/utils/synchronous.py`
- `Reproducibility Packet/scripts/screen_synchronous_safe_probe.py`
- `Reproducibility Packet/tests/test_safe_probe_screen.py`
- `Reproducibility Packet/results/synchronous_safe_probe/summary.json`
- `Reproducibility Packet/results/synchronous_safe_probe/candidate_comparison.csv`
- `Reproducibility Packet/results/synchronous_safe_probe/synchronous_safe_probe_report.md`
- `agents/Codex/Session Summaries/HumanReport9.md`

## Files updated

- `Reproducibility Packet/scripts/analyze_synchronous_detection_floor.py`
- `Reproducibility Packet/tests/test_synchronous_detection_floor.py`
- `Reproducibility Packet/results/synchronous_detection_floor/summary.json`
- `Reproducibility Packet/results/synchronous_detection_floor/synchronous_detection_floor_report.md`
- `Reproducibility Packet/scripts/run_bounded_burst_sensitivity.py`
- `Reproducibility Packet/scripts/run_feasibility_spike.py`
- `Reproducibility Packet/scripts/utils/cable_mechanics.py`
- `Reproducibility Packet/scripts/utils/cable_plant.py`
- `Reproducibility Packet/scripts/utils/schema_types.py`
- `Reproducibility Packet/scripts/utils/synthetic_plant.py`
- `Reproducibility Packet/tests/test_cable_plant.py`
- `Reproducibility Packet/tests/test_feasibility_spike.py`
- `Reproducibility Packet/results/bounded_burst_sensitivity/{summary.json,burst_sensitivity.csv,bounded_burst_report.md}`
- `Reproducibility Packet/schema/schema-v1.0.md`
- `Reproducibility Packet/README.md`
- `README.md`
- `chats/Claude-Codex/Phase 2 Integration and Config Freeze/Phase 2 Integration and Config Freeze - Active.md`
- `agents/Codex/README.md`
- `agents/Codex/Summary of Only Necessary Context.md`

## Verification performed

- Full packet: **91 passed**.
- `compileall` over packet scripts/tests: passed.
- CLI-help smokes: detector floor, bounded-burst screen, and safe-probe screen passed.
- Corrected detector artifact regenerated with 200 sensor realizations at W=640.
- Original bounded-burst artifact regenerated at 17 points / 0.1 ms.
- Safe-probe six-row focused grid regenerated at 17 points / 0.1 ms.
- Active chat tail re-read after append; Session-9 header appears exactly once and is
  physically last.
- `git diff --check`: clean (CRLF conversion warnings only).

## Next steps / pending actions

1. **Claude owner re-review:** genuinely re-open the edited detector script/utility/tests
   and regenerated artifact; explicitly approve the same state or edit and hand back.
2. **Claude/A1 same-state review:** review the exact appended schema text plus fixed-width
   implementation before any pilot trace relies on those roles.
3. **Claude estimator lane:** implement the synchronous feature in
   `WindowFeatureExtractor` against the settled 0.8 Hz spectrum and W=640 full-cycle
   development window; keep W/stride in the pilot sweep rather than freezing now.
4. **Codex plant lane:** add real endpoint-contact extraction before optional-contact
   pilots and continue the interpretable residual/system-ID baseline and recovery
   controller.
5. **Shared config work:** sanity-check non-load-bearing sensor constants, define
   severity/onset grids, run the W/stride/probe pilot, and freeze validation-derived
   class/abstention/OOD thresholds only on validation data.
6. **Pre-pilot/confirmatory gates:** deployable-loader leakage test, whole-trajectory and
   fault-setting split audit, role-hash rejection, multi-run storage checks, and complete
   immutable `schema.json`/`config.json`. No current `dev-` trace may be promoted.

No new external sources were used this session; the work was an empirical/code review of
the existing plant and sensor-model artifacts.
