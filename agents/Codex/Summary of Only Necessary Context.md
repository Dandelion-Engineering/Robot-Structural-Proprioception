# Summary of Only Necessary Context — Codex

**Rewritten:** 2026-07-21 17:40 PDT

**Current phase:** Phase 2 — Execution

**Codex session just completed:** Session 16 · **Next:** Session 17

## Current authoritative state

Phase 0 and Phase 1 remain closed. The jointly approved Claim Sheet, Accessible Claim Sheet, Study Guide Pass 1, schema v1.0, and appended schema Amendment A1 remain in force. A1 fixes `contact_state[2]` and `safety_flag[7]`. The Claim Sheet still awaits Randy's non-blocking review in `director_requests.md`; execution continues.

The authoritative coordination file is `chats/Claude-Codex/Phase 2 Integration and Config Freeze/Phase 2 Integration and Config Freeze - Active.md`.

Claude Session 16 independently reproduced and explicitly approved Codex Session 15's optional-contact profile screen at the exact state Codex approved. That loop is closed. One new review obligation is open:

- **Matched contact-enabled pilot first review (Claude owns next).** Codex Session 16 built, ran, explicitly approved, and handed off `run_matched_contact_pilot.py`, `test_matched_contact_pilot.py`, `results/matched_contact_enabled_pilot/`, the packet-runbook/current-boundary wording, and the lean public README blocker entry. Claude must genuinely first-review that exact state. If Claude edits, Codex must owner-re-review the actual files before approving or returning them. Later use or silence is not approval.

## Matched contact-enabled pilot — current BLOCK

The pilot applies the previously screened z = 0.100 m endpoint plane identically to matched C1/S CRN pairs under the 50%-task / 0.05 N / 0.8 Hz one-cycle condition. It separates three gates:

1. contact-conditioned coefficient information at the exact first online-owned post-probe window;
2. a short 2.6 s causal plant→sensor→estimator→controller seam check; and
3. a mandatory 6.0 s audit covering fault onset at 1.0 s plus the Claim Sheet's five-second analysis horizon.

Exact-window reference/evaluation roles:

- W=768, stride=16 remain development proposals;
- policy decision step = 1136; newest owned observation index = 1135;
- calibration seeds = 9000–9031 (32); held-out seeds = 9032–9079 (48);
- 99th-percentile higher-method threshold remains the LOO calibration maximum and is not validation-frozen.

Held-out scheduled-decision outcome:

| Suite | Healthy false alarms | Minimum fault detection | Structure detection | Prototype attribution |
|---|---:|---:|---:|---:|
| C1 | 4.2% | 20.8% | 20.8% | 100% |
| S | 8.3% | 100% | 100% | 100% |

S retains the fault signal, including structural information that C1 mostly misses, but fails the ≤5% held-out healthy false-alarm screen. Do not advance or freeze this operating point.

The short causal layer uses a pilot-only nearest-centroid estimator with a fixed canonical location/severity lookup attached to the predicted class. It consumes only delivered `ObservedRecord` history; its one-hot probability is not calibrated and it is not the learned head. All eight representative arms preserve nominal commands before the first causal decision and have one short contact episode with zero A1 flags. The observation-side sensor fault genuinely reaches the policy and both sensor arms call sensor at least once. The call is unstable: by the final decision all eight arms call actuator, including healthy and sensor, causing inappropriate actuator compensation. This is a phase/reference-lifecycle BLOCK.

Over 6.0 s, z = 0.100 m produces three contact episodes in healthy/structure/actuator and joint-1 angle violations for 1111 / 1658 / 1651 steps. The former z = 0.050 m no-contact control also contacts near 4.32 s; healthy/structure violate the angle limit for 311 / 334 steps. Peak contact forces remain below 5 N. The profile/task/controller condition is blocked from evaluation-horizon use and config freeze. Do not relax A1 thresholds to repair it.

Exact overall decision:

`BLOCK_MATCHED_CONTACT_PILOT_AND_CONTACT_PROFILE_CONFIG_FREEZE`

The earlier open-loop z = 0.100 m screen remains correct within its explicitly bounded 2.274 s horizon. Its one-episode and z = 0.050 no-contact conclusions do not transfer to 6.0 s.

## Jointly approved causal and interpretable floors

`utils/residual_baseline.py:LinearResidualAttributionEstimator` is jointly approved. It accepts only `ObservedRecord`, binds to a fixed C0/C1/S layout, uses `tau_cmd` only as an exogenous input, fits healthy normalized affine ARX dynamics, builds transparent `[signed_mean_residual, residual_rms, valid_fraction]` features, fits four labeled development centroids, and calibrates off-prototype abstention on a third known-class role. Re-fit lifecycle invalidation and the ≥100-window default tail guard are approved. It emits no location/severity and cannot activate recovery.

`utils/recovery_control.py:GainScheduledRecoveryController` is jointly approved. Healthy, abstained, tied/ambiguous, unlocalized, invalid-severity, or overly uncertain outputs preserve nominal 50%-task torque. Confident structure applies a bounded global derate; confident localized actuator attribution applies probability-weighted capped inverse-gain scheduling. Detection-only and residual floors cannot activate it.

`utils/estimator.py:CoefficientReferenceDetector` is jointly approved as a detection-only rung. It shares the pilot score statistic, not a frozen margin or decision rate. Validation reference data, threshold, and persistence own those quantities.

The jointly approved recovery-seam regression drives the real `CablePlant → OnlineSensorSession → EstimatorCommandPolicy → GainScheduledRecoveryController` path with fixed deployable diagnosis stand-ins. It pins torque/interface mechanics only, not trained attribution, `J_5s`, tracking recovery, or safety evidence.

The new `PilotPrototypeEstimator` lives only in `run_matched_contact_pilot.py` and is **not** a jointly approved permanent rung. Its continuous instability is a recorded negative method finding.

## Pilot and mechanics boundary

The selected short mechanics candidate remains 50% ordinary task torque plus a 0.05 N, 0.8 Hz, one-cycle raised-cosine probe. It is safe only within the earlier short collision-disabled/contact-screen envelopes. The old clean 2.22× coefficient-space ratio remains a mechanics-screen fact, not a deployable margin.

The broad noisy-reference artifact (`base_seed=1000`, 8 calibration + 12 held-out seeds) remains the false-alarm BLOCK. The prospective non-contact follow-up (`base_seed=5000`, 32 calibration + 48 held-out seeds) advanced W=768 / stride=16 with 97.9% S worst per-fault detection, 100% prototype attribution, 0.7% pooled / 2.1% worst healthy false alarms, and matched-C1 minimum per-fault detection 0%. That remains a development proposal, not frozen config or the confirmatory C1-vs-S result.

Safety uses privileged A1 truth: angle×2, speed×2, tip workspace, absolute gauge strain, and contact force. The row-level two-dimensional tip-radius readout is not the workspace gate; the plant's three-dimensional base-relative flag is authoritative.

## Config remains explicitly unfrozen

Current role hashes remain `dev-`. Still open:

- Claude's genuine first review of the matched contact pilot BLOCK;
- a bounded/stabilized five-second task/contact/controller redesign;
- an honest diagnosis lifecycle: one scheduled decision/hold, phase/time-conditioned references, or a temporal model across the full trajectory;
- validation-sized healthy/reference and four-class known calibration roles;
- per-suite probability calibration and frozen class/abstention/selective/OOD thresholds;
- shared severity/onset grids and final analysis window;
- joint sanity-check of non-load-bearing sensor constants;
- unscheduled phase drift and nonlinear/probe-band thermal interference;
- learned temporal attribution and RMA heads;
- evaluation-sized closed-loop comparison separating exact delivery from `J_5s` and privileged safety;
- deployable-loader leakage, whole-trajectory/fault-setting split, role-hash rejection, multi-run storage, and immutable schema/config hash gates.

## Exact resume path for Codex Session 17

1. Read the UTF-8 physical tail of the active Phase-2 thread. Process Claude's matched-contact pilot review. If Claude approves as-is, close the loop. If Claude edits, inspect and genuinely owner-re-review the actual state before approving or returning it.
2. Do not treat a reviewer edit, later use, silence, or handoff as approval. Both agents must explicitly approve the same exact state.
3. After the review loop settles, the highest-value next pre-freeze task is the coupled bounded-task/contact/reference-lifecycle redesign. Preserve all three gates: exact information, causal action stability, and onset+5 s privileged safety.
4. Do not tune on the held-out seed range or relax A1 thresholds. New candidate searches need predeclared grids and prospective seed roles.
5. Before confirmatory generation, finish validation roles/thresholds, per-suite calibration, severity/onset grids, sensor-constant sanity, safe contact/task cases, and leakage/split/storage/hash audits; then freeze and hash the complete schema/config.
6. Do not build the learned attribution/RMA heads before the agreed post-freeze boundary.

## Verification and session record

- New matched-contact focused suite: **5 passed**.
- Full packet: **148 passed**.
- `compileall`: passed; new CLI help passed.
- Summary JSON: valid finite JSON; decision parsed exactly.
- Default-command scratch reproduction: all five artifacts byte-identical after generated-report newline normalization.
- First chat append hard gate: pre-write 1036 lines; header once at line 1040 and after the old count; Codex physically last.
- Pilot handoff append hard gate: pre-write 1048 lines; header once at line 1052 and after the old count; Codex physically last.
- Root public README heartbeat updated with one lean matched-pilot BLOCK entry.
- Detailed record: `agents/Codex/Session Summaries/HumanReport16.md`.
- Regular director update: `agents/Codex/Progress Reports/Progress Report Session 16.md`.
- Next regular Codex progress report: **Session 24** unless a Claim-Sheet amendment or phase transition also fires.

## Transcript append rule

Before every future chat append: read the UTF-8 physical tail, record the pre-write line count, verify a unique multi-line physical-EOF anchor, patch only against that anchor, then assert the new header occurs exactly once after the old line count and is physically last. Never anchor on a repeated signature or heading.
