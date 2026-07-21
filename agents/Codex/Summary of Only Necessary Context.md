# Summary of Only Necessary Context — Codex

**Rewritten:** 2026-07-20 19:51 PDT

**Current phase:** Phase 2 — Execution

**Codex session just completed:** Session 14 · **Next:** Session 15

## Current authoritative state

Phase 0 and Phase 1 remain closed. The jointly approved Claim Sheet, Accessible Claim
Sheet, Study Guide Pass 1, schema v1.0, and appended schema Amendment A1 are in force.
A1 fixes `contact_state[2]` and `safety_flag[7]`. The Claim Sheet still awaits Randy's
non-blocking review in `director_requests.md`; execution continues.

The authoritative coordination file is
`chats/Claude-Codex/Phase 2 Integration and Config Freeze/Phase 2 Integration and Config Freeze - Active.md`.

Claude Session 14 genuinely approved Codex Session 13's
`LinearResidualAttributionEstimator` at the exact handed-off state. That first-review
loop is closed. The coefficient-reference detector and gain-scheduled recovery-controller
loops also remain closed at same-state approval.

Two review obligations are now open, both owned next by Claude:

1. **Recovery-seam owner re-review.** Claude built and approved
   `tests/test_recovery_seam.py`. Codex independently reproduced the mechanism but edited
   the fixed-diagnosis fixture so `detection_time_s` really latches at the first decision,
   as schema §D and the fixture documentation require. Codex explicitly approves the
   edited state. Claude must re-open the exact file and explicitly approve or edit/return
   it; later use or silence is not approval.
2. **Endpoint-contact first review.** Codex implemented and explicitly approved the
   optional endpoint-contact model/extraction/CLI/test/runbook state in
   `utils/cable_mechanics.py`, `utils/cable_plant.py`,
   `make_mujoco_plant_trace.py`, `tests/test_cable_plant.py`, and the packet README.
   Claude must genuinely first-review that exact state. If Claude edits, Codex must
   owner-re-review the actual files before the loop can close.

## Recovery seam: edited open-review state

`tests/test_recovery_seam.py` drives the real
`CablePlant → OnlineSensorSession → EstimatorCommandPolicy → GainScheduledRecoveryController`
path over multiple steps using fixed deployable estimator-output stand-ins.

- A localized one-hot actuator diagnosis with 50% remaining gain requests 2× nominal at
  the affected joint; the downstream plant fault restores delivered torque to nominal.
- An otherwise-identical unlocalized/infinite-uncertainty diagnosis remains nominal and
  leaves delivery degraded to 0.5×.
- A structural diagnosis applies the sustained 0.75 global derate on a healthy plant.
- These are torque/interface mechanism assertions only, not trained attribution,
  `J_5s`, tracking recovery, or a safety result.

Codex's only edit is a resettable first-detection latch. Before the edit the four-step
fixture emitted detection times `[0.000, 0.002, 0.004, 0.006]` despite claiming to retain
the first flag time. It now emits `0.0` for every output and has an explicit regression.
Focused file: 4 passed. Independent 12-step reproduction: seven load-bearing properties
passed.

## Endpoint-contact extraction: current open-review state

The default selected model remains collision-disabled and still writes `[0,0]` to the
contact role. An explicit development-only profile is available:

- `CableModelConfig.endpoint_contact_enabled` controls the profile;
  `endpoint_contact_plane_z_m` supplies its horizontal plane height.
- `model_xml` creates a plane and one predefined MuJoCo contact pair between that plane
  and the expanded distal link-2 endpoint segment. All ordinary cable geoms keep
  collision disabled, so other link/body contacts cannot enter the endpoint field.
- `CablePlant._contact_state()` filters every reported contact to that exact pair,
  calls `mujoco.mj_contactForce`, sums the finite 3-D contact-force magnitudes across
  contact points, and writes `[tip_contact_force_n, tip_contact_active]`.
- Unexpected geom pairs, missing handles, contact in disabled mode, and invalid forces
  fail loud.
- The already-approved privileged safety path sets
  `tip_contact_force_exceeded = tip_contact_force_n > configured_limit`; no contact field
  crosses into `ObservedRecord`.
- `make_mujoco_plant_trace.py --endpoint-contact-plane-z-m <z>` enables the profile in a
  role-separated development trace and includes the setting in the `dev-` config hash.
  Omitting the flag preserves the old no-contact path.

The 0.498 m plane is only an extraction fixture. It is not a frozen profile/grid and no
optional-contact pilot has run. Verification: focused plant suite 8 passed; a 100-step
low-limit regression peaked at 0.844 N and exactly matched the seventh flag to the force
comparison; a portable 10-step CLI smoke recorded 10 active steps and 0.574 N peak force
with no trip at the normal 5 N development limit.

First-party MuJoCo 3.10.0 contact-pair and `mj_contactForce` documentation is recorded in
`agents/Codex/references.md`.

## Jointly approved interpretable floors and causal seam

`utils/residual_baseline.py:LinearResidualAttributionEstimator` is now jointly approved.
It accepts only `ObservedRecord`, binds to a fixed C0/C1/S layout, uses `tau_cmd` only as
an exogenous input, fits healthy normalized affine ARX dynamics, builds transparent
`[signed_mean_residual, residual_rms, valid_fraction]` features, fits four labeled
development centroids, and calibrates off-prototype abstention on a third known-class
role. Re-fit lifecycle invalidation and the ≥100-window default tail guard are approved.
It emits no location/severity and therefore cannot activate recovery.

`utils/recovery_control.py:GainScheduledRecoveryController` remains jointly approved.
Healthy, abstained, tied/ambiguous, unlocalized, invalid-severity, or overly uncertain
outputs preserve nominal 50%-task torque. Confident structure applies a bounded global
derate; confident localized actuator attribution applies probability-weighted capped
inverse-gain scheduling. Detection-only and residual floors cannot activate it.

`utils/estimator.py:CoefficientReferenceDetector` remains jointly approved as a
detection-only rung. It shares the pilot's coefficient-distance score statistic, not a
frozen margin or decision rate. Validation reference data, threshold, and persistence own
those quantities.

## Pilot and mechanics boundary

The selected mechanics candidate remains 50% ordinary task torque plus a 0.05 N, 0.8 Hz,
one-cycle raised-cosine probe. It is safe within the current collision-disabled
development envelope across healthy, structural, actuator, and encoder scenarios. The
old clean 2.22× differential/floor ratio remains a mechanics-screen fact only.

Broad noisy-reference artifact (`base_seed=1000`, 8 calibration + 12 held-out seeds):
closest W=640/stride=8 S cell had 100% minimum per-fault detection and 100% prototype
attribution but 8.3% pooled / 16.7% worst healthy false alarms; BLOCK.

Prospective follow-up (`base_seed=5000`, 32 calibration + 48 held-out seeds): W=768 /
stride=16 had 97.9% S worst per-fault detection, 100% prototype attribution, 0.7% pooled /
2.1% worst healthy false alarms, and matched-C1 minimum per-fault detection 0%. The
threshold is still the LOO maximum and the worst false-alarm rate is one event in 48.
This is a pilot proposal, not frozen config or the confirmatory C1-vs-S result.

Safety uses privileged A1 truth: angle×2, speed×2, tip workspace, absolute gauge strain,
and contact force. Optional contact truth now exists, but a scenario grid must still be
designed and screened before it can enter any pilot.

## Config remains explicitly unfrozen

Current role hashes remain `dev-`. Still open:

- Claude's two review obligations above;
- actual optional-contact profile/grid selection and all-scenario screening;
- validation-sized healthy/reference and four-class known calibration roles;
- per-suite probability calibration and frozen class/abstention/selective/OOD thresholds;
- shared severity/onset grids;
- joint sanity-check of non-load-bearing sensor constants;
- unscheduled phase drift and nonlinear/probe-band thermal interference;
- learned temporal attribution and RMA heads;
- evaluation-sized closed-loop comparison separating exact delivery from `J_5s` and
  privileged safety;
- deployable-loader leakage, whole-trajectory/fault-setting split, role-hash rejection,
  multi-run storage, and immutable schema/config hash gates.

## Exact resume path for Codex Session 15

1. Read the UTF-8 physical tail of the active Phase-2 thread. If Claude explicitly
   approves the exact edited recovery-seam file, close that loop. If Claude edits it,
   inspect and genuinely reviewer-re-review the new state.
2. Process Claude's endpoint-contact first review. If Claude approves as-is, close the
   loop. If Claude edits, inspect the actual diff and genuinely owner-re-review before
   approving or returning it.
3. If both review loops are settled, choose the next Codex-owned increment from the live
   thread: either design/screen the actual optional-contact profile/grid across all fault
   scenarios or build the evaluation-sized development controller comparison. Do not
   promote the 0.498 m fixture or the short torque seam into a frozen/control result.
4. Before confirmatory generation, finish validation roles/thresholds, severity/onset
   grids, sensor-constant sanity, contact cases, and leakage/split/storage/hash audits;
   then freeze and hash the complete schema/config.
5. Do not build the learned attribution/RMA heads before the agreed post-freeze boundary.

## Verification and session record

- Recovery seam focused: **4 passed**; independent reproduction **7/7**.
- Plant/contact focused: **8 passed**.
- Full packet: **139 passed**.
- `compileall`: passed; contact CLI help and persisted-trace smoke passed.
- `git diff --check`: clean apart from line-ending warnings.
- Root public README: heartbeat checked and intentionally unchanged.
- Detailed record: `agents/Codex/Session Summaries/HumanReport14.md`.
- Next regular Codex progress report: Session 16 unless a Claim-Sheet amendment or phase
  transition fires earlier.

## Transcript append rule

Before every future chat append: read the UTF-8 physical tail, patch against a unique
multi-line tail block (never a bare speaker signature), then immediately re-read the
written tail and confirm the new header appears exactly once and is physically last.
