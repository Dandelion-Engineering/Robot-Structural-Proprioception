# Summary of Only Necessary Context — Codex

**Rewritten:** 2026-07-20 13:40 PDT

**Current phase:** Phase 2 — Execution

**Codex session just completed:** Session 12 · **Next:** Session 13

## Current authoritative state

Phase 0 and Phase 1 remain closed. The jointly approved Claim Sheet, Accessible Claim
Sheet, Study Guide Pass 1, schema v1.0, and appended schema Amendment A1 are in force.
A1 fixes `contact_state[2]` and `safety_flag[7]`. The Claim Sheet still awaits Randy's
non-blocking review in `director_requests.md`; execution continues.

The authoritative coordination file is
`chats/Claude-Codex/Phase 2 Integration and Config Freeze/Phase 2 Integration and Config Freeze - Active.md`.

Claude Session 12 genuinely reviewed and explicitly approved Codex Session 11's full
noisy healthy-reference pilot state. That pilot loop is closed.

Two new review obligations are open after Codex Session 12:

1. Claude must owner-re-review Codex's edits to Claude's `CoefficientReferenceDetector`
   and tests, plus the forward pilot canonicalization/metadata/report state. Codex
   explicitly approves the current edited state.
2. Claude must first-review Codex's new `GainScheduledRecoveryController` and tests.
   Codex explicitly approves the current state.

Do not infer either approval from later use, implementation, silence, or an unrelated
handoff.

## Coefficient-reference detector: current edited state

`Reproducibility Packet/scripts/utils/estimator.py` contains the permanent
`CoefficientReferenceDetector` and proposes W=768 / stride=16. The core is sound:

- joint healthy-standardized cosine/sine distance
  `||(coeff_live-mean)/scale|| / sqrt(D)`;
- healthy calibration reference replaces the privileged matched counterfactual;
- detection only: non-healthy mass is uniform and the source-type call is abstained;
- calibration tail guard requires at least `ceil(min_tail_count/far)` nominal tail
  support; thresholds remain validation-owned.

Codex Session 12 made two load-bearing corrections:

- the pilot and permanent rung share the **score statistic**, not an already-frozen
  margin or decision rate; validation reference, threshold, and persistence still own
  those quantities;
- a successful `fit_reference()` that replaces an existing reference now atomically
  installs the new reference, invalidates the old threshold, and resets the detection
  latch. Scoring then fails until recalibration.

The W=768 / stride=16 rationale now says matched C1's **minimum per-fault** detection was
0%, not that C1 detected no faults. This remains a pilot proposal, not frozen config.

## Noisy healthy-reference pilot: closed loop plus forward hygiene

The broad BLOCK and prospective follow-up decisions are unchanged.

- Broad artifact: `results/noisy_reference_pilot/`, base seed **1000**, 8 calibration +
  12 held-out seeds. Closest W=640/stride=8 cell: S 100% minimum per-fault detection,
  100% attribution, 8.3% pooled / 16.7% worst healthy false alarms; BLOCK.
- Follow-up artifact: `results/noisy_reference_pilot_threshold_followup/`, base seed
  **5000**, 32 calibration + 48 held-out seeds. W=768/stride=16: S 97.9% worst
  per-fault detection, 100% prototype attribution, 0.7% pooled / 2.1% worst healthy
  false alarms; matched C1 minimum per-fault detection 0%.

The follow-up report now states the missing caveat: 32 values leave its 99th-percentile
higher-method threshold at the LOO maximum, and 2.1% is one event in 48. Both summaries
record their base seeds and exact report seed ranges. The pilot now imports the canonical
coefficient vector/distance from `utils.estimator`; duplicated definitions are gone. No
metrics or decision changed and nothing is frozen.

## Interpretable recovery-controller floor

New `Reproducibility Packet/scripts/utils/recovery_control.py` implements
`GainScheduledRecoveryController` for the existing `EstimatorCommandPolicy` callback.
It consumes only deployable `EstimatorOutput` and time.

- Healthy, type-abstained, tied/ambiguous, unlocalized, invalid-severity, or overly
  uncertain outputs preserve the nominal 50%-task command. An actionable source must be
  the unique highest-probability class as well as clear the configured threshold.
- A confident structural diagnosis applies an explicit bounded global derate. This is a
  safety response, not a claim that stiffness is repaired.
- A confident localized actuator diagnosis applies probability-weighted, capped inverse-
  gain scheduling using `severity_out` as remaining gain.
- Detection-only rungs cannot trigger active compensation because they abstain on type.

On the real `CablePlant`, a one-hot joint-1 estimate with 50% gain remaining requested
2× nominal at that joint; the plant's downstream fault delivered nominal torque exactly
with no saturation. This is an interface/mechanism regression, **not** a closed-loop
tracking result or research result. Controller defaults are provisional and unfrozen.

## Current estimator, detector, safety, and mechanics boundaries

The approved per-column summary remains
`[last, mean, std, slope, sync_cos, sync_sin, sync_amplitude, valid_fraction]`.
The learned `[W,D]` tensor is unchanged.

The selected mechanics candidate remains 50% ordinary task torque plus a 0.05 N,
0.8 Hz, one-cycle raised-cosine probe. It is safe within the current development
envelope across healthy, structural, actuator, and encoder scenarios. The old clean
2.22× differential/floor ratio remains a mechanics-screen fact only, not a deployed
margin.

Safety uses privileged A1 truth: angle×2, speed×2, tip workspace, absolute gauge strain,
and contact force. The contact role remains collision-disabled `[0,0]`; `CablePlant`
fails if contact unexpectedly appears. Optional-contact pilots require real endpoint-
contact extraction first.

## Config remains explicitly unfrozen

Current role hashes remain `dev-`. Still open:

- Claude owner-re-review of the edited coefficient-reference state and first review of
  the recovery-controller floor;
- validation-sized healthy reference and validation-frozen class/abstention/selective/
  OOD thresholds;
- shared severity/onset grids;
- joint sanity-check of non-load-bearing sensor constants;
- unscheduled phase drift and nonlinear/probe-band thermal interference;
- optional-contact extraction/cases;
- learned temporal attribution and RMA heads;
- Codex residual/linear-system-ID baseline and controlled recovery comparison;
- deployable-loader leakage, whole-trajectory/fault-setting split, role-hash rejection,
  multi-run storage, and immutable schema/config hash gates.

## Exact resume path for Codex Session 13

1. Read the UTF-8 physical tail of the active Phase-2 thread. If Claude explicitly
   approves the exact edited coefficient-reference/pilot state, close that loop. If
   Claude edits, inspect the actual diff and genuinely re-review it.
2. Review Claude's response to `recovery_control.py`; if Claude edits, reproduce the
   real-plant compensation and genuinely re-review before approving or returning it.
3. Implement the interpretable residual/linear-system-ID baseline against the causal
   observation seam.
4. Design a bounded development closed-loop comparison that separates exact actuator
   delivery compensation from tracking recovery and safety. Do not call the one-step
   compensation regression a control result.
5. Implement endpoint-contact extraction before any optional-contact pilot.
6. Before confirmatory generation, complete validation thresholding, fault grids,
   non-load-bearing sensor sanity, leakage/split/storage/role-hash audits, then freeze and
   hash the complete schema/config.

## Verification and session record

- Full packet: **127 passed**.
- Focused estimator + pilot: **36 passed**.
- Recovery controller: **12 passed**, including real MuJoCo compensation and ambiguous-
  source fallback.
- `compileall`: passed; pilot CLI help: passed.
- Pilot base-seed metadata: 1000 broad / 5000 follow-up.
- Both report files reproduce exactly from amended JSON summaries after newline
  normalization.
- `git diff --check`: clean (line-ending warnings only).
- Detailed record: `agents/Codex/Session Summaries/HumanReport12.md`.
- Next regular Codex progress report: Session 16 unless a Claim-Sheet amendment or phase
  transition fires earlier.

## Transcript append rule

Before every future chat append: read the UTF-8 physical tail, patch against a unique
multi-line tail block (never a bare speaker signature), then immediately re-read the
written tail and confirm the new header appears exactly once and is physically last.
