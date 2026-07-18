# Summary of Only Necessary Context — Codex

**Rewritten:** 2026-07-17 17:06 PDT

**Current phase:** Phase 2 — Execution

**Codex session just completed:** Session 8 · **Next:** Session 9

## Current authoritative state

Phase 0 and Phase 1 remain closed. The jointly approved Claim Sheet, Accessible Claim Sheet, Study Guide Pass 1, and `Reproducibility Packet/schema/schema-v1.0.md` are in force. The Claim Sheet still awaits Randy’s non-blocking review in `director_requests.md`; Phase-2 execution continues.

The authoritative coordination file is `chats/Claude-Codex/Phase 2 Integration and Config Freeze/Phase 2 Integration and Config Freeze - Active.md`.

Claude Session 8 genuinely re-reviewed and explicitly approved the exact Session-7 evaluation-core and online-interface states. Those two loops are closed. `metrics.py`/`stats.py`, `schema_types.py`, `sensor_model.py`, and `online_loop.py` are not awaiting another response for the Session-7 work.

One review loop is open after Codex Session 8 directly edited and explicitly approved Claude’s estimator front:

- `Reproducibility Packet/scripts/utils/estimator.py`
- `Reproducibility Packet/tests/test_estimator.py`

Claude must genuinely re-open the files, review both the diagnoses and implementations, and explicitly approve the same state or edit and hand it back. Do not infer approval from use, silence, or a future unrelated handoff.

## Estimator state handed back in Session 8

Claude’s detection/abstention front, output contract, oracle boundary, and online policy adapter remain the correct architecture. Codex corrected three contract issues:

1. `WindowFeatureExtractor(window_steps=W)` now left-pads startup with zero values plus false masks, rejects an overlong record, and always emits fixed `[W,D]`; the prior implementation emitted `[T,D]` as startup history grew.
2. Summary slopes now use each channel’s own `measurement_time_s`; the prior implementation used the `q_obs` time grid for every channel despite schema-C channel-level timing.
3. `OracleInterface(onset_time_s=...)` reports healthy/no location/no severity before onset and exposes the perfect class only at/after onset; the prior implementation leaked the run’s known fault class before the change existed.

Estimator-output validation now enforces non-negative integral steps, finite non-negative decision times, integral location, non-NaN/non-negative uncertainty, causal detection time, and increasing trace steps/times. `W=512` / `stride=8` remain a pilot-sweep proposal. The corrected rationale says 512 samples (1.024 s) cover most, not all, of a 1.25 s 0.8-Hz cycle and do not create a detection-latency floor.

`coverage_at_risk` was independently reviewed against Claim Sheet Slot 7 and is correct as written.

## Mechanics/config decision — bounded diagnostic is BLOCKED

The mechanics substrate decision remains binding:

- Native MuJoCo cable/rod selected as the primary plant; volumetric 3-D flex is reserve.
- Selected resolution: 17 points / 16 segments per link; MuJoCo step `0.0001 s`; control step `0.002 s` / 500 Hz.
- `n_def=90`: shortest log-map rotations for 15 internal ball joints on each link; exclude the L1 shoulder pose and L2 elbow-side free pose.
- Gauges: L1 0.25/0.75 L; L2 0.25/0.75 L.
- Development faults: link-2 `[0.55,0.85]`, remaining EI 0.50; elbow remaining actuator gain 0.70 downstream of unchanged `control_effort`.
- Ordinary torque-only remains its own `trajectory_spec_id` negative control.

Session 8 added a finite raised-cosine diagnostic envelope to the same authoritative `cable_mechanics.py` path. Default continuous behavior is preserved when duration is `None`. Canonical selected-model sensitivity artifacts live under `Reproducibility Packet/results/bounded_burst_sensitivity/`.

Exact screen (max gauge RMS microstrain; unchanged 10-microstrain floor):

| Condition | Structure | Actuator | Structure–actuator | Mechanics |
|---|---:|---:|---:|---|
| ordinary | 2.17 | 5.92 | 5.93 | BLOCK |
| continuous gate load | 10.56 | 23.36 | 23.36 | PASS |
| bounded one cycle / 1.25 s | 8.18 | 7.84 | 12.33 | BLOCK |
| bounded two cycles / 2.50 s | 8.67 | 13.38 | 17.49 | BLOCK |

The continuous feasibility load was active before the 1 s fault onset; the honest bounded diagnostic starts at the fault boundary. Therefore the earlier continuous PASS remains valid for selecting the mechanics but does not establish a short post-detection diagnostic budget.

## Contact/safety proposal — explicit, not frozen

The Session-8 development proposal is stored in the bounded-burst summary and active chat:

- `contact_state[2]`: `tip_contact_force_n`, `tip_contact_active`.
- `safety_flag[7]`: joint-angle flags ×2, joint-speed flags ×2, tip-workspace, absolute-gauge-strain, tip-contact-force.
- Keep the existing `saturation_flag[2]` separate.
- Provisional screening thresholds: `|q|≤π rad` and `|qd|≤10 rad/s` per joint; tip radius `≤0.82 m`; `|gauge_true|≤500 microstrain`; tip contact force `≤5 N`.

These are conservative development values for review, not hardware claims or frozen config. They deliberately expose that every current command condition fails the motion screen:

- ordinary: peak accumulated angle 3.18 rad; speed 13.79 rad/s;
- continuous: 9.05 rad; 40.67 rad/s;
- bounded one cycle: 4.53 rad; 37.74 rad/s;
- bounded two cycles: 21.06 rad; 37.74 rad/s.

Contact is still disabled in the selected MJCF, so the contact-force field/flag cannot yet be exercised. Zero-width contact/safety arrays remain development placeholders and are disallowed for pilot/confirmatory generation.

## Complete config state — deliberately not frozen

Settled mechanics values remain ready for eventual inclusion: `f_ctrl=500 Hz`, `dt=0.002 s`, MuJoCo step `0.0001 s`, `n_def=90`, four gauge locations, diagnostic amplitude 1.0 N and frequency 0.8 Hz.

Open/blocking:

- **Diagnostic duration/envelope/controller:** concrete BLOCK; redesign so it clears both signature and approved safety screens. Do not merely lengthen the open-loop sine.
- **Contact/safety roles and thresholds:** explicit proposal awaits review and implementation.
- **`W=512`, `stride=8`:** Claude proposal, now correctly implemented as a fixed tensor interface, but still needs pilot sweep after the probe is coherent.
- **Sensor pathology constants:** two load-bearing FBG values remain reference-grounded; non-load-bearing defaults need joint sanity-check.
- **Severity/onset grids:** shared and pilot-informed.
- **Validation-derived class, abstention, selective, and OOD thresholds:** freeze from validation only.

Do not create a partial immutable `config.json`. Current role hashes remain `dev-`; no current trace may enter confirmatory analysis.

## Exact resume path for Codex Session 9

1. Read the true UTF-8 physical tail of the active Phase-2 thread. If Claude explicitly approves the exact Session-8 estimator edits, record the loop closed. If Claude edits, inspect the actual diff and continue the explicit review cycle.
2. Review Claude’s response to the `contact_state[2]` / `safety_flag[7]` semantics and provisional thresholds. Treat silence as no approval.
3. Highest-value Codex lane: redesign the diagnostic/controller pair so the arm stays inside an approved motion envelope while clearing the unchanged signature floor. Candidate families: closed-loop tip/joint-space probe, lower-amplitude multi-frequency sequence, bounded pulses, increased damping/task stabilization. Preserve ordinary and continuous conditions as evidence, not as approved pilot settings.
4. Implement nonzero contact/safety roles in `CablePlant` once semantics converge; endpoint contact truth must populate the two-wide contact role before optional-contact pilot cases.
5. Continue toward the interpretable residual/linear-system-ID baseline and recovery controller after the diagnostic/safety interface converges.
6. Before pilot: implement deployable-loader leakage test, whole-trajectory/fault-setting split audit, role-hash rejection, multi-run storage checks, and nonzero contact/safety gates. Before confirmatory generation: freeze/hash complete `schema.json` + `config.json`, preserve ordinary/diagnostic conditions separately, and rerun all gates.

## Verification and session record

- Full packet: **80 passed**.
- `compileall` over packet scripts/tests: passed.
- Bounded-burst CLI help: passed using `.\venv\Scripts\python.exe`.
- Canonical four-condition selected-model sensitivity regenerated successfully.
- Public README contains one lean negative-method heartbeat; this is not a research result.
- Detailed session record: `agents/Codex/Session Summaries/HumanReport8.md`.
- Required regular director update: `agents/Codex/Progress Reports/Progress Report Session 8.md`; next regular Codex report is Session 16 unless a phase/amendment trigger fires earlier.

## Transcript-order rule

Before every chat append: read the UTF-8 physical tail, patch against unique exact tail text, and re-read immediately afterward. Session 8’s turn landed correctly at the physical tail; no correction was required. Never use a bare speaker-signature anchor.
