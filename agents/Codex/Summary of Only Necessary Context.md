# Summary of Only Necessary Context — Codex

**Rewritten:** 2026-07-20 14:53 PDT

**Current phase:** Phase 2 — Execution

**Codex session just completed:** Session 13 · **Next:** Session 14

## Current authoritative state

Phase 0 and Phase 1 remain closed. The jointly approved Claim Sheet, Accessible Claim
Sheet, Study Guide Pass 1, schema v1.0, and appended schema Amendment A1 are in force.
A1 fixes `contact_state[2]` and `safety_flag[7]`. The Claim Sheet still awaits Randy's
non-blocking review in `director_requests.md`; execution continues.

The authoritative coordination file is
`chats/Claude-Codex/Phase 2 Integration and Config Freeze/Phase 2 Integration and Config Freeze - Active.md`.

Claude Session 13 genuinely approved the exact edited coefficient-reference detector
state and the recovery-controller floor, including the unique-source gate. Both loops are
closed at same-state approval.

One review obligation is now open: Claude must first-review Codex Session 13's
`LinearResidualAttributionEstimator`, tests, module-index entry, and packet-boundary
wording. Codex explicitly approves the current state. If Claude edits it, Codex must
re-open the actual files and genuinely owner-re-review before the loop can close. Do not
infer approval from use, silence, or later handoff.

## Linear residual attribution floor: current open-review state

New `Reproducibility Packet/scripts/utils/residual_baseline.py` implements the simple
residual/linear-system-ID baseline required by Claim Sheet Slot 5.

- It accepts only deployable `ObservedRecord` and binds each fit to one exact C0/C1/S
  suite layout. A fixed-suite guard rejects a C1 record that exposes S-only gauges.
- `tau_cmd` is the known exogenous input. For every physically present non-command sensor
  scalar, a normalized affine ridge-ARX model predicts `x[t]` from the sensor vector and
  validity mask at `t-1` plus `tau_cmd[t]` and its validity.
- Missing inputs are zero only after healthy normalization and retain explicit mask bits;
  invalid targets are excluded per scalar rather than dropping a whole transition.
- Each scalar yields `[signed_mean_residual, residual_rms, valid_fraction]`.
- Data roles are explicit and ordered: healthy dynamics fit → four-class labeled residual
  prototypes → separate four-class known calibration for off-prototype abstention.
- The unknown-threshold guard requires at least
  `ceil(min_tail_count / false_abstention_rate)` calibration windows and refuses missing
  known classes.
- A dynamics re-fit invalidates prototypes and threshold; a prototype re-fit invalidates
  the threshold. Online scoring fails until all required roles are installed.
- Outputs contain four-class scores, low-confidence/off-prototype abstention, and a
  persistence-latched detection time, but no location or severity. The baseline therefore
  cannot trigger active recovery by itself.

Synthetic centroid separation and the real six-step MuJoCo seam smoke are implementation
tests only. They are not an S-vs-C1 performance result, a tracking result, a calibration
result, or evidence on the research hypothesis. Ridge, temperature, confidence/unknown
thresholds, persistence, and every data-role manifest remain validation/freeze-owned.

## Approved coefficient-reference detector and pilot boundary

`CoefficientReferenceDetector` in `utils/estimator.py` is now same-state approved. The
pilot and permanent rung share the score statistic
`||(coeff_live-mean)/scale|| / sqrt(D)`, not a frozen margin or decision rate. Validation
reference data, threshold, and persistence own those quantities. The rung is detection
only and abstains on fault type. Its calibration-tail guard and atomic reference/threshold
lifecycle are approved.

The noisy healthy-reference pilot remains development-only:

- Broad artifact: `results/noisy_reference_pilot/`, base seed 1000, 8 calibration + 12
  held-out seeds. Closest W=640/stride=8 cell: S 100% minimum per-fault detection, 100%
  prototype attribution, 8.3% pooled / 16.7% worst healthy false alarms; BLOCK.
- Prospective follow-up: `results/noisy_reference_pilot_threshold_followup/`, base seed
  5000, 32 calibration + 48 held-out seeds. W=768/stride=16: S 97.9% worst per-fault
  detection, 100% prototype attribution, 0.7% pooled / 2.1% worst healthy false alarms;
  matched-C1 minimum per-fault detection 0%.
- The follow-up threshold is still the leave-one-out maximum and 2.1% is one event in 48.
  W=768/stride=16 is a pilot proposal, not frozen config.

## Approved recovery-controller floor

`utils/recovery_control.py:GainScheduledRecoveryController` is now jointly approved. It
consumes only `EstimatorOutput` plus time.

- Healthy, abstained, tied/ambiguous, unlocalized, invalid-severity, or overly uncertain
  outputs preserve the nominal 50%-task command.
- A uniquely confident structural diagnosis applies a bounded global derate, a safety
  response rather than claimed stiffness repair.
- A uniquely confident localized actuator diagnosis applies probability-weighted, capped
  inverse-gain scheduling using remaining gain.
- Detection-only and the new unlocalized residual floor cannot activate compensation.
- The one-step exact actuator-delivery regression and six-step nominal-path smoke are
  interface/mechanism tests, not `J_5s` or research results.

## Current mechanics, sensor, and safety boundary

The selected mechanics candidate remains 50% ordinary task torque plus a 0.05 N, 0.8 Hz,
one-cycle raised-cosine probe. It is safe within the current development envelope across
healthy, structural, actuator, and encoder scenarios. The old clean 2.22×
differential/floor ratio remains a mechanics-screen fact only, not a deployed margin.

Safety uses privileged A1 truth: angle×2, speed×2, tip workspace, absolute gauge strain,
and contact force. The contact role remains collision-disabled `[0,0]`; `CablePlant` fails
if contact unexpectedly appears. Optional-contact pilots require real endpoint-contact
extraction first.

The approved estimator per-column summary remains
`[last, mean, std, slope, sync_cos, sync_sin, sync_amplitude, valid_fraction]`. The learned
`[W,D]` tensor is unchanged.

## Config remains explicitly unfrozen

Current role hashes remain `dev-`. Still open:

- Claude first review of the residual baseline state;
- validation-sized healthy/reference and four-class known calibration roles;
- validation-frozen class/probability/abstention/selective/OOD thresholds and persistence;
- shared severity/onset grids;
- joint sanity-check of non-load-bearing sensor constants;
- unscheduled phase drift and nonlinear/probe-band thermal interference;
- optional-contact extraction and cases;
- learned temporal attribution and RMA heads;
- fixed-attribution multi-step seam regression and evaluation-sized recovery comparison;
- deployable-loader leakage, whole-trajectory/fault-setting split, role-hash rejection,
  multi-run storage, and immutable schema/config hash gates.

## Exact resume path for Codex Session 14

1. Read the UTF-8 physical tail of the active Phase-2 thread. If Claude approves the
   exact residual-baseline state, close that loop. If Claude edits, inspect the actual
   diff and genuinely owner-re-review before approving or returning it.
2. Review or build the shared fixed-attribution multi-step causal-seam regression: an
   actionable fixed deployable stand-in drives active compensation, while a
   detection-only/unlocalized arm remains nominal. Keep it explicitly below a tracking
   result.
3. Design the evaluation-sized development comparison that separates exact actuator
   delivery from `J_5s` tracking recovery and privileged safety.
4. Implement endpoint-contact extraction before any optional-contact pilot.
5. Before confirmatory generation, finish validation roles/thresholds, severity/onset
   grids, non-load-bearing sensor sanity, leakage/split/storage/role-hash audits, then
   freeze and hash the complete schema/config.

## Verification and session record

- Residual baseline: **7 passed**, including fixed-suite leakage rejection and real
  MuJoCo causal-seam composition.
- Full packet: **134 passed**.
- `compileall`: passed.
- `git diff --check`: clean apart from line-ending warnings.
- Root public README: heartbeat checked and intentionally unchanged.
- Detailed record: `agents/Codex/Session Summaries/HumanReport13.md`.
- Next regular Codex progress report: Session 16 unless a Claim-Sheet amendment or phase
  transition fires earlier.

## Transcript append rule

Before every future chat append: read the UTF-8 physical tail, patch against a unique
multi-line tail block (never a bare speaker signature), then immediately re-read the
written tail and confirm the new header appears exactly once and is physically last.
