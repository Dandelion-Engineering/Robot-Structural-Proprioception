# Summary of Only Necessary Context — Codex

**Rewritten:** 2026-07-20 21:20 PDT

**Current phase:** Phase 2 — Execution

**Codex session just completed:** Session 15 · **Next:** Session 16

## Current authoritative state

Phase 0 and Phase 1 remain closed. The jointly approved Claim Sheet, Accessible Claim Sheet, Study Guide Pass 1, schema v1.0, and appended schema Amendment A1 are in force. A1 fixes `contact_state[2]` and `safety_flag[7]`. The Claim Sheet still awaits Randy's non-blocking review in `director_requests.md`; execution continues.

The authoritative coordination file is `chats/Claude-Codex/Phase 2 Integration and Config Freeze/Phase 2 Integration and Config Freeze - Active.md`.

Claude Session 15 explicitly approved both Codex Session-14 handoffs at the exact states Codex approved:

1. the resettable first-detection latch in `tests/test_recovery_seam.py`; and
2. the optional endpoint-contact extraction in `utils/cable_mechanics.py`, `utils/cable_plant.py`, `make_mujoco_plant_trace.py`, `tests/test_cable_plant.py`, and the packet README.

Those loops are closed. One new review obligation is open:

- **Optional-contact profile screen first review (Claude owns next).** Codex Session 15 built, ran, explicitly approved, and handed off `screen_optional_contact_profile.py`, `test_optional_contact_profile.py`, `results/optional_contact_profile_screen/`, and the packet-runbook wording. Claude must genuinely first-review that exact state. If Claude edits, Codex must owner-re-review the actual files before approving or returning them. Later use or silence is not approval.

## Optional-contact profile screen — open-review state

The screen applies the advancing development condition (50% task torque plus a 0.05 N, 0.8 Hz, one-cycle raised-cosine probe starting at 1.0 s) over the 2.274 s horizon through the first post-probe W=768 / stride=16 decision. Selected mechanics remain 17 points/link and 0.1 ms simulation timestep.

Predeclared plane grid:

`z ∈ {0.050, 0.075, 0.100, 0.125, 0.150} m`.

The lowest plane must be a zero-contact/zero-safety control. A candidate needs exactly one post-onset episode in every canonical scenario, at least five active steps, no more than 5% active steps, peak force below 5 N, and no A1 safety flag. The lowest passing height advances.

Grid outcome:

- z = 0.050 m: zero-contact control across all scenarios.
- z = 0.075 m: actuator-only contact; fails all-scenario contact.
- z = 0.100 m: first all-scenario pass; advances to matched optional-contact pilot review.
- z = 0.125 m: also passes but is more intrusive.
- z = 0.150 m: actuator case has two episodes; fails the one-episode rule.

At z = 0.100 m:

- healthy: 19 active steps (1.67%), one episode starting 2.044 s, peak 1.409 N, impulse 0.01820 N·s, zero safety steps;
- structure: 19 steps (1.67%), one episode starting 2.044 s, peak 1.371 N, impulse 0.01872 N·s, zero safety steps;
- actuator: 23 steps (2.02%), one episode starting 1.974 s, peak 1.078 N, impulse 0.01538 N·s, zero safety steps;
- sensor-labeled row: physically aliases healthy because encoder corruption enters only in `SensorModel` under open-loop commands.

The old z = 0.498 m value remains a low-level extraction fixture and is explicitly excluded from the candidate grid. The z = 0.100 m state is a development candidate, not frozen and not a contact-enabled C1-vs-S result.

The future matched contact pilot must apply the exact same profile to C1 and S within each CRN pair. The observation-side sensor fault must be tested through the actual closed-loop path because corrupted observations can then alter commands and contact; the current open-loop alias does not answer that question.

## Jointly approved causal and interpretable floors

`utils/residual_baseline.py:LinearResidualAttributionEstimator` is jointly approved. It accepts only `ObservedRecord`, binds to a fixed C0/C1/S layout, uses `tau_cmd` only as an exogenous input, fits healthy normalized affine ARX dynamics, builds transparent `[signed_mean_residual, residual_rms, valid_fraction]` features, fits four labeled development centroids, and calibrates off-prototype abstention on a third known-class role. Re-fit lifecycle invalidation and the ≥100-window default tail guard are approved. It emits no location/severity and cannot activate recovery.

`utils/recovery_control.py:GainScheduledRecoveryController` is jointly approved. Healthy, abstained, tied/ambiguous, unlocalized, invalid-severity, or overly uncertain outputs preserve nominal 50%-task torque. Confident structure applies a bounded global derate; confident localized actuator attribution applies probability-weighted capped inverse-gain scheduling. Detection-only and residual floors cannot activate it.

`utils/estimator.py:CoefficientReferenceDetector` is jointly approved as a detection-only rung. It shares the pilot's coefficient-distance score statistic, not a frozen margin or decision rate. Validation reference data, threshold, and persistence own those quantities.

The jointly approved recovery-seam regression drives the real `CablePlant → OnlineSensorSession → EstimatorCommandPolicy → GainScheduledRecoveryController` path with fixed deployable diagnosis stand-ins. It pins torque/interface mechanics only: localized actuator compensation restores delivered torque; unlocalized/infinite-uncertainty stays nominal and leaves delivery degraded; structural attribution applies a sustained 0.75 derate. It is not trained attribution, `J_5s`, tracking recovery, or safety evidence.

## Pilot and mechanics boundary

The selected mechanics candidate remains 50% ordinary task torque plus a 0.05 N, 0.8 Hz, one-cycle raised-cosine probe. It is safe within the collision-disabled development envelope across healthy, structural, actuator, and encoder scenarios. The old clean 2.22× differential/floor ratio remains a mechanics-screen fact only.

Broad noisy-reference artifact (`base_seed=1000`, 8 calibration + 12 held-out seeds): closest W=640/stride=8 S cell had 100% minimum per-fault detection and 100% prototype attribution but 8.3% pooled / 16.7% worst healthy false alarms; BLOCK.

Prospective follow-up (`base_seed=5000`, 32 calibration + 48 held-out seeds): W=768 / stride=16 had 97.9% S worst per-fault detection, 100% prototype attribution, 0.7% pooled / 2.1% worst healthy false alarms, and matched-C1 minimum per-fault detection 0%. The threshold is still the LOO maximum and the worst false-alarm rate is one event in 48. This is a pilot proposal, not frozen config or the confirmatory C1-vs-S result.

Safety uses privileged A1 truth: angle×2, speed×2, tip workspace, absolute gauge strain, and contact force. Contact extraction is jointly approved; z = 0.100 m now advances only to matched contact-pilot review.

## Config remains explicitly unfrozen

Current role hashes remain `dev-`. Still open:

- Claude's genuine first review of the optional-contact profile screen;
- matched contact-enabled C1/S pilot including the closed-loop sensor-fault path;
- validation-sized healthy/reference and four-class known calibration roles;
- per-suite probability calibration and frozen class/abstention/selective/OOD thresholds;
- shared severity/onset grids and final analysis window;
- joint sanity-check of non-load-bearing sensor constants;
- unscheduled phase drift and nonlinear/probe-band thermal interference;
- learned temporal attribution and RMA heads;
- evaluation-sized closed-loop comparison separating exact delivery from `J_5s` and privileged safety;
- deployable-loader leakage, whole-trajectory/fault-setting split, role-hash rejection, multi-run storage, and immutable schema/config hash gates.

## Exact resume path for Codex Session 16

1. Read the UTF-8 physical tail of the active Phase-2 thread. Process Claude's optional-contact screen review. If Claude approves as-is, close the loop. If Claude edits, inspect and genuinely owner-re-review the actual state before approving or returning it.
2. Session 16 requires the regular director progress report in addition to normal session work.
3. After the review loop settles, choose the next pre-freeze increment from the live thread. Highest-value candidates are the matched contact-enabled C1/S pilot design or the evaluation-sized development controller comparison, but do not call either confirmatory while config is unfrozen.
4. Before confirmatory generation, finish validation roles/thresholds, per-suite calibration, severity/onset grids, sensor-constant sanity, contact cases, and leakage/split/storage/hash audits; then freeze and hash the complete schema/config.
5. Do not build the learned attribution/RMA heads before the agreed post-freeze boundary.

## Verification and session record

- New contact-screen focused suite: **4 passed**.
- Full packet: **143 passed**.
- `compileall`: passed; new CLI help passed.
- Packet-root default screen command reproduced the committed artifact with an identical SHA-256 `summary.json` hash.
- Active-chat append hard gate passed: pre-write 940 lines; Session-15 header once at line 944 and after the old line count; Codex signature physically last.
- Root public README heartbeat checked and intentionally unchanged.
- Detailed record: `agents/Codex/Session Summaries/HumanReport15.md`.
- Next regular Codex progress report: **Session 16** unless a Claim-Sheet amendment or phase transition also fires.

## Transcript append rule

Before every future chat append: read the UTF-8 physical tail, record the pre-write line count, verify a unique multi-line physical-EOF anchor, patch only against that anchor, then assert the new header occurs exactly once after the old line count and is physically last. Never anchor on a repeated signature or heading.
