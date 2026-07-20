# Summary of Only Necessary Context — Codex

**Rewritten:** 2026-07-19 22:06 PDT

**Current phase:** Phase 2 — Execution

**Codex session just completed:** Session 10 · **Next:** Session 11

## Current authoritative state

Phase 0 and Phase 1 remain closed. The jointly approved Claim Sheet, Accessible Claim
Sheet, Study Guide Pass 1, original schema v1.0, and appended schema Amendment A1 are in
force. A1 fixes `contact_state[2]` and `safety_flag[7]`; Claude Session 10 genuinely
re-reviewed Codex Session 9's exact amendment/implementation and explicitly approved it.
The detector-floor review loop is also closed at Codex Session 9's corrected state.

The Claim Sheet still awaits Randy's non-blocking review in `director_requests.md`;
execution continues. The authoritative coordination file is
`chats/Claude-Codex/Phase 2 Integration and Config Freeze/Phase 2 Integration and Config Freeze - Active.md`.

One combined review obligation is open after Codex Session 10: Claude must genuinely
owner-re-review the current cosine/sine/amplitude synchronous feature in `estimator.py`,
the paired safety-shape guard in `metrics.py`, and their focused tests. Codex explicitly
approves this edited state. Do not infer Claude approval from use, silence, or a later
unrelated handoff.

## Session-10 synchronous-feature correction

Claude Session 10 correctly reused `utils.synchronous.harmonic_coefficients`, retained
per-channel measurement grids, and moved the recommended window to W=640 so a 0.8 Hz
probe has a complete 1.25 s period in view. The handed-off feature stored only the
phase-invariant amplitude. That lost information counted by the safe-probe screen:

- the clean screen computes `||coeff(fault) - coeff(reference)||_2` by regressing the
  fault-minus-reference trace;
- amplitude-only exposes `||coeff(run)||_2`, so the largest comparison it can recover is
  `abs(||a||_2 - ||b||_2)`;
- this can be strictly smaller and is zero for a pure phase change.

Independent selected-candidate audit at W=640 / 0.8 Hz:

- clean coefficient-vector distances reproduce structural **1.015 µε**, actuator
  **0.898 µε**, and structure–actuator **1.090 µε**;
- with the 0.405 µε modeled floor, the clean minimum is **2.22×**;
- amplitude-only's best actuator change is **0.716 µε = 1.77×**;
- on the screen's gauge-1 actuator channel, amplitude-only retains 0.266/0.898 = 29.6%.

Current edited per-column summary layout:

`[last, mean, std, slope, sync_cos, sync_sin, sync_amplitude, valid_fraction]`.

Cosine/sine preserve phase and make the clean coefficient distance reconstructible;
amplitude remains a phase-invariant summary. The raw `[W,D]` learned-model tensor is
unchanged. W=640 / stride=8 remain pilot proposals, not frozen values.

## Detector and safe-probe boundaries

The jointly approved modeled detector floor remains:

- W=640, 500 Hz, 0.8 Hz joint intercept/trend/cosine/sine regression;
- harmonic NES **0.111 ± 0.059 µε**;
- development threshold **0.405 µε**;
- gate-floor / mean-NES ratio **90×**.

The selected mechanics candidate remains 50% ordinary task torque plus a 0.05 N, 0.8 Hz,
one-cycle raised-cosine probe. It is safe within the current development envelope across
healthy, structural, actuator, and encoder scenarios. It advances only to a pilot.

Crucial boundary after Session 10: the clean privileged fault-minus-healthy coefficient
distance and modeled null floor do not directly establish the deployable estimator's
margin. The pilot must run noisy per-suite observations against a healthy/reference
model and measure coefficient-space detectability, false alarms, phase/onset/stride
alignment, and attribution. Do not call the clean 2.22× value the deployed margin.

## Safety/contact and metric state

Amendment A1 is jointly in force:

- `contact_state[2]`: `tip_contact_force_n`, `tip_contact_active`;
- `safety_flag[7]`: joint-angle ×2, joint-speed ×2, tip workspace, absolute gauge strain,
  tip contact force; `saturation_flag[2]` stays separate;
- safety is computed from privileged `q_true`, `qd_true`, `gauge_true`, and tip truth,
  never corrupted observations.

Claude Session 10 added `safety_incident_rate`, `safety_flag_rates`, and
`safety_regression_delta`. Codex approves their privileged-truth semantics and positive-
means-regression sign. Codex added a fail-loud requirement that paired C1/S inputs share
the same `[T,7]` control-grid shape. The future evaluation driver must still enforce the
exact `[t_c,t_c+5 s]` slice before calling these point functions. Claude owner re-review
of the guard remains open.

Current plant contact is collision-disabled and writes `[0,0]`; `CablePlant` fails if
contact unexpectedly appears. Optional-contact pilot cases remain blocked until real
MuJoCo endpoint-contact extraction exists.

## Mechanics and config state

Selected mechanics remain unchanged:

- native MuJoCo cable/rod primary; volumetric 3-D flex reserve;
- 17 points / 16 segments per link; simulation step 0.0001 s; control 0.002 s / 500 Hz;
- `n_def=90`; shortest log-map rotations for 15 internal ball joints per link;
- gauges at L1/L2 0.25 and 0.75 L;
- development structural fault: link-2 `[0.55,0.85]`, remaining EI 0.50;
- development actuator fault: elbow remaining gain 0.70 downstream of unchanged
  `control_effort`;
- ordinary task-only remains a separate `trajectory_spec_id` negative control.

**Do not freeze `config.json`.** Current role hashes remain `dev-`. Open fields/work:

- Claude owner re-review of the coefficient-preserving feature and safety pairing guard;
- deployable noisy/reference pilot over probe/task scale, W/stride, onset alignment, and
  shared fault severity/onset grids;
- joint sanity-check of non-load-bearing sensor constants;
- validation-derived class, abstention, selective, and OOD thresholds;
- optional-contact extraction/cases;
- learned temporal attribution/RMA heads, Codex's residual/system-ID baseline, and
  recovery controller;
- deployable-loader leakage test, whole-trajectory/fault-setting split audit, role-hash
  rejection, and multi-run storage checks before confirmatory generation.

## Exact resume path for Codex Session 11

1. Read the UTF-8 physical tail of the active Phase-2 thread. If Claude explicitly
   approves the exact cosine/sine/amplitude layout and safety pairing guard, close that
   loop. If Claude edits, inspect the actual diff and continue the review cycle.
2. Do not begin the pilot by merely rescoring the clean privileged differential. Build
   the pilot around noisy `ObservedRecord` data and a healthy/reference comparison. It
   must preserve coefficient phase, test onset relative to stride, and report false
   positives as well as fault/reference separation.
3. Sweep the current candidate neighborhood over task/probe scale plus
   W∈{512,640,768}, stride∈{4,8,16}; W=512 will intentionally leave the full-cycle
   synchronous entries zero under the current contract and is a negative window control.
4. Continue the interpretable residual/linear-system-ID baseline and recovery controller
   against the online seam; keep estimator architecture matched across suites.
5. Implement endpoint-contact extraction before any optional-contact pilot.
6. Before confirmatory generation, freeze/hash complete schema/config, preserve ordinary
   and diagnostic conditions separately, and rerun leakage, split, safety, storage, and
   role-hash gates.

## Verification and session record

- Full packet: **102 passed**.
- `compileall`: passed.
- `git diff --check`: clean (line-ending warnings only).
- Detailed record: `agents/Codex/Session Summaries/HumanReport10.md`.
- Next regular Codex progress report remains Session 16 unless a Claim Sheet amendment
  or phase transition fires earlier.

## Transcript-order rule and current anomaly

Session 10's first full chat append was mistakenly inserted at line 61 because a bare
`— Claude` signature was used as the patch anchor. No content was deleted, moved, or
rewritten. A dated Session-10 transcript-order correction is physically last and is the
operative handoff; it restates the open owner-review gate and 102-test state.

Before every future chat append: read the UTF-8 physical tail, patch against a unique
multi-line tail block (never a bare speaker signature), then re-read the written tail and
confirm the new header's physical location immediately.
