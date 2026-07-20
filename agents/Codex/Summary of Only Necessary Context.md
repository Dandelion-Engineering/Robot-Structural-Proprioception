# Summary of Only Necessary Context — Codex

**Rewritten:** 2026-07-20 11:35 PDT

**Current phase:** Phase 2 — Execution

**Codex session just completed:** Session 11 · **Next:** Session 12

## Current authoritative state

Phase 0 and Phase 1 remain closed. The jointly approved Claim Sheet, Accessible Claim
Sheet, Study Guide Pass 1, schema v1.0, and appended schema Amendment A1 are in force.
A1 fixes `contact_state[2]` and `safety_flag[7]`. The Claim Sheet still awaits Randy's
non-blocking review in `director_requests.md`; execution continues.

The authoritative coordination file is
`chats/Claude-Codex/Phase 2 Integration and Config Freeze/Phase 2 Integration and Config Freeze - Active.md`.

Claude Session 11 genuinely owner-re-reviewed Codex Session 10's coefficient-preserving
feature and safety-pairing guard and explicitly approved the exact state. That combined
loop is closed.

One new review obligation is open after Codex Session 11: Claude must genuinely review
Codex's noisy healthy-reference pilot script, tests, broad BLOCK, prospective follow-up,
and documentation. Codex explicitly approves the current state and handed it back in the
active thread. Do not infer Claude approval from use, implementation of a later rung,
silence, or an unrelated handoff.

## Noisy healthy-reference pilot

New Codex-owned instrument:
`Reproducibility Packet/scripts/run_noisy_reference_pilot.py`.

It uses causal noisy deployable `ObservedRecord` windows and the same-state-approved
cosine/sine features. It does **not** use a privileged fault-minus-healthy trace as the
detector input and does not edit Claude's permanent estimator rung.

Development convention tested:

- scheduled one-cycle 0.8 Hz probe, phase reset at fault/probe onset;
- first global stride-grid decision at or after probe end;
- healthy calibration reference conditioned on task/probe, W, and decision lag;
- dimension-normalized, healthy-standardized Euclidean distance on retained cosine/sine
  coefficients;
- 99th-percentile higher-method leave-one-out healthy calibration score as the
  development threshold;
- nearest standardized fault-shape centroid as a pilot-only attribution instrument.

W=512 is a required inert negative control: it cannot span a full 0.8 Hz period, so the
production extractor leaves all synchronous coefficients zero.

### Broad sweep — preserved BLOCK

Artifact: `Reproducibility Packet/results/noisy_reference_pilot/`.

Grid: C1/S; task {0.4,0.5}; probe {0.025,0.05 N}; W {512,640,768}; stride
{4,8,16}; onset offsets {0,5,11}; 8 calibration + 12 held-out sensor seeds per
class/suite.

Closest cell: task 0.50 / probe 0.05 N / W=640 / stride=8.

- S minimum per-fault detection: 100%.
- S minimum prototype attribution: 100%.
- matched C1 minimum fault detection: 8.3%.
- S healthy false alarms: 8.3% pooled, 16.7% worst alignment.

Decision: BLOCK. Eight calibration values could not resolve the 5% healthy tail. The
threshold was not retuned on those held-out rows.

### Prospective larger-calibration follow-up — advances to owner review

Artifact:
`Reproducibility Packet/results/noisy_reference_pilot_threshold_followup/`.

Used the already-selected task 0.50 / probe 0.05 N candidate, the same statistic and
threshold rule, new non-overlapping seeds (base 5000), 32 calibration + 48 held-out
seeds per class/suite, and the same three onset alignments.

Advancing development cell: **W=768 / stride=16**.

- S worst per-fault detection: **97.9%**.
- S worst prototype attribution: **100%**.
- S healthy false alarms: **0.7% pooled**, **2.1% worst alignment**.
- matched C1 minimum fault detection: **0%**.
- no healthy/structural/actuator development safety flag.

Decision boundary: advance only to Claude's permanent coefficient-reference-rung
implementation review. This is not the confirmatory C1-vs-S result and freezes nothing.

## Current estimator, detector, safety, and mechanics boundaries

The approved per-column summary remains:

`[last, mean, std, slope, sync_cos, sync_sin, sync_amplitude, valid_fraction]`.

The learned `[W,D]` tensor is unchanged. W=768 / stride=16 now supersedes W=640 /
stride=8 only as the **pilot proposal** for the coefficient-reference rung; neither is
frozen until the review/validation/config gates close.

The selected mechanics candidate remains 50% ordinary task torque plus a 0.05 N,
0.8 Hz, one-cycle raised-cosine probe. It is safe within the current development
envelope across healthy, structural, actuator, and encoder scenarios. The old clean
2.22× differential/floor ratio remains a mechanics-screen fact only, not a deployed
margin.

Safety uses privileged A1 truth: angle×2, speed×2, tip workspace, absolute gauge strain,
and contact force. `safety_regression_delta` requires paired C1/S `[T,7]` shapes; the
future evaluation driver still owns exact `[t_c,t_c+5 s]` slicing.

Current contact remains collision-disabled and `[0,0]`; `CablePlant` fails if contact
unexpectedly appears. Optional-contact pilots remain blocked until real MuJoCo endpoint-
contact extraction exists.

## Config remains explicitly unfrozen

Current role hashes remain `dev-`. Still open:

- Claude review of the noisy-reference pilot and permanent coefficient-distance rung;
- validation-sized healthy reference and validation-frozen class/abstention/selective/
  OOD thresholds;
- shared severity/onset grids;
- joint sanity-check of non-load-bearing sensor constants;
- unscheduled phase drift and nonlinear/probe-band thermal interference;
- optional-contact extraction/cases;
- learned temporal attribution/RMA heads;
- Codex residual/linear-system-ID baseline and recovery controller;
- deployable-loader leakage, whole-trajectory/fault-setting split, role-hash rejection,
  multi-run storage, and immutable schema/config hash gates.

## Exact resume path for Codex Session 12

1. Read the UTF-8 physical tail of the active Phase-2 thread. If Claude explicitly
   approves the exact pilot state, close the loop. If Claude edits, inspect the actual
   diff and genuinely re-review before approving or returning it.
2. If Claude implements the permanent coefficient-distance healthy-reference rung,
   review it against the approved pilot convention and verify it does not treat the
   pilot threshold or W/stride as frozen validation values.
3. Continue Codex's interpretable residual/linear-system-ID baseline and recovery
   controller against the online seam.
4. Implement endpoint-contact extraction before any optional-contact pilot.
5. Before confirmatory generation, complete validation thresholding, fault grids,
   non-load-bearing sensor sanity, leakage/split/storage/role-hash audits, then freeze and
   hash the complete schema/config.

## Verification and session record

- Full packet: **107 passed**.
- `compileall`: passed.
- Pilot CLI help: passed.
- Broad pilot: 216 result rows; follow-up: 54 result rows; both JSON trees contain no
  NaN/Infinity tokens.
- Projected C1 is bit-for-bit identical to native C1 across values, masks, timing
  metadata, and suite flags.
- `git diff --check`: clean (line-ending warnings only).
- Detailed record: `agents/Codex/Session Summaries/HumanReport11.md`.
- Next regular Codex progress report: Session 16 unless a Claim-Sheet amendment or phase
  transition fires earlier.

## Transcript append rule

Before every future chat append: read the UTF-8 physical tail, patch against a unique
multi-line tail block (never a bare speaker signature), then immediately re-read the
written tail and confirm the new header appears exactly once and is physically last.
