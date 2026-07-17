# Summary of Only Necessary Context — Codex

**Rewritten:** 2026-07-17 15:42 PDT

**Current phase:** Phase 2 — Execution

**Codex session just completed:** Session 7 · **Next:** Session 8

> **Session-8 requirement:** Codex Session 8 is a regular progress-report session. Complete normal work, then also write the director-facing report under `agents/Codex/Progress Reports/` using `Playbooks/research-progress-report.md`. Phase/amendment reports do not reset the every-eighth-session count.

## Current authoritative state

Phase 0 and Phase 1 are closed. The jointly approved Claim Sheet, Accessible Claim Sheet, Study Guide Pass 1, and `Reproducibility Packet/schema/schema-v1.0.md` remain in force. The Claim Sheet is still awaiting Randy's non-blocking review in `director_requests.md`; Phase-2 execution continues.

The authoritative coordination file is `chats/Claude-Codex/Phase 2 Integration and Config Freeze/Phase 2 Integration and Config Freeze - Active.md`. The prior Session-6 development-interface loop is **closed**: Claude genuinely re-reviewed commit `70e6e4f` and explicitly approved the exact producer/sensor state Codex had approved.

Two new Session-7 review loops are **open** after Codex directly edited and explicitly approved the current state:

1. Claude-owned evaluation core: `utils/metrics.py`, `utils/stats.py`, and tests.
2. Claude-owned/co-owned sensor interface: `utils/schema_types.py`, `utils/sensor_model.py`, plus Codex's `utils/online_loop.py` and tests.

Claude must genuinely re-open the files and review both the diagnoses and implementations, then explicitly approve the same state or edit and return it. Do not infer approval from use, silence, or a future handoff.

## Mechanics decision that remains binding

- Native MuJoCo cable/rod selected only under matched diagnostic excitation.
- Ordinary torque-only: **BLOCK** (structural 1.92 µε, actuator 5.81 µε, separation 5.81 µε; all below 10 µε). Preserve as its own `trajectory_spec_id` negative control.
- Diagnostic condition: **PASS** (continuous 3 s development trace, 1.0 N peak, 0.8 Hz zero-mean distal transverse sinusoid; structural 10.24 µε, actuator/separation 23.87 µε).
- Fine model: 17 points / 16 segments per link; MuJoCo step 0.0001 s; control step 0.002 s / 500 Hz.
- `n_def=90`: shortest log-map rotations for 15 internal ball joints on each link; exclude the L1 shoulder pose and L2 elbow-side free pose.
- Gauges: L1 0.25/0.75 L; L2 0.25/0.75 L.
- Development faults: link-2 `[0.55,0.85]`, remaining EI 0.50; elbow remaining actuator gain 0.70 downstream of unchanged `control_effort`.
- Reserve: volumetric 3-D flex; PyElastica only if later cable validation fails.

The mechanics gate is a method decision, not a research-hypothesis result. Its continuous three-second sinusoid does **not** prove a shorter tapered burst works.

## Session-7 evaluation corrections awaiting Claude re-review

Codex reproduced Claude's 51/51 baseline, then found four contract-level issues:

1. `j_5s` previously returned a truncated integral if the trace ended before `onset + 5 s`. It now requires finite inputs, a strictly increasing uniform grid, and exact onset/end coverage.
2. `risk_coverage_curve` previously split equal-confidence ties based on input order. It now reports threshold-realizable tie-group endpoints only.
3. OOD false acceptance previously used a threshold selected at 95% ID acceptance and selected/evaluated on the same cases. It now uses `unknown_threshold_at_sensitivity` on validation OOD and `ood_false_acceptance_rate` at the frozen threshold on held-out OOD, matching Slot 7's 95% unknown-detection-sensitivity contract.
4. The bootstrap previously resampled train seeds independently inside each `pair_id`. Because trained seeds are evaluated across all pair units, the design is crossed. It now requires a rectangular `pair_id × train_seed` grid and resamples pair rows plus global seed columns while preserving each C1/S cell.

Hard predictions/booleans/finite inputs now fail loudly when malformed. Focused metrics/stats tests: 29 passed.

## Stateful online execution seam

`CablePlant.advance()` remains the one-step schema-B producer. Session 7 added:

- `ObservableStepSources` / `observable_step_sources()` — the one-step narrow plant→sensor doorway. It exposes only time, q source, requested command, upstream control effort, IMU/gauge sources, and temperature; privileged delivered torque, deformation, task truth, labels, contact, and safety remain unreachable.
- `OnlineSensorSession.observe_step()` — owns persistent per-rollout CRN generators, biases, previous encoder state, gauge hysteresis, and random-walk drift; emits one `ObservedStep` with values/masks/timing.
- `SensorModel.observe()` — now only a compatibility/persistence wrapper over the same online session, so batch CLI and online execution share one authoritative pathology implementation.
- `OnlineSensorSession.available_record(decision_time, history_steps=…)` — keeps an explicit bounded past-only tail and masks channel rows until declared availability, preventing controller/estimator use before latency elapses and avoiding quadratic history rebuilding.
- `utils/online_loop.py:run_online_rollout()` — causal sequence: bounded delivered history → policy callback → command → plant advance → sensor observation. Required `history_steps` becomes Claude's frozen `W`; the callback otherwise remains generic until estimator outputs arrive.
- `SensorConfig.validate()` — rejects non-physical noise/timing/quantization/hysteresis/dropout constants before rollout.

Verification:

- Full packet: **59 passed**; compileall passed.
- Current stateful path vs pre-session committed batch code: every channel value, validity mask, measurement time, and availability time bitwise identical on a stochastic thermal + encoder-drift trace.
- Real matched online C1/S rollouts: all shared values/masks bitwise identical under CRN; C1 gauges absent; S gauges finite where valid.
- Policy causality: encoder available at the next decision; 2 ms gauge withheld until its availability time.

## Shared config status — deliberately not frozen

Settled plant values ready for eventual complete config: `f_ctrl=500 Hz`, `dt=0.002 s`, MuJoCo step `0.0001 s`, `n_def=90`, four gauge locations, diagnostic amplitude 1.0 N and frequency 0.8 Hz.

Still open:

- Diagnostic duration/envelope — Codex must run bounded-burst sensitivity or retain the continuous gate condition honestly.
- Contact/safety field widths, semantics, and thresholds — Codex must propose before pilot; current development arrays are zero-width.
- `W` and `stride` — Claude will propose with the estimator, not before.
- Remaining sensor-pathology constants — Claude proposed defaults; both agents must sanity-check.
- Severity/onset grids — shared and pilot-informed.
- Validation-derived class, abstention, selective, and OOD thresholds.

Do not create a partial immutable `config.json`. Current role hashes remain `dev-`; no current trace may enter confirmatory analysis.

## Exact resume path for Codex Session 8

1. Read the true UTF-8 physical tail of the active Phase-2 thread. If Claude approved the exact Session-7 edited states, record both loops closed. If Claude edited, inspect the actual diff and continue the explicit review cycle.
2. Perform normal Session-8 work. Highest-value Codex lane: run a bounded-burst excitation sensitivity against the selected mechanics and prepare an explicit contact/safety width + threshold proposal. Keep the ordinary condition separate.
3. If Claude's estimator/`W`/`stride` proposal has landed, review it against the causal `available_record` interface and integrate only after same-state approval.
4. After normal work, write the required Codex Session-8 progress report per `Playbooks/research-progress-report.md`.
5. Continue toward the interpretable residual/linear system-ID baseline and recovery controller only once the relevant shared interface/config values converge.
6. Before pilot: implement the deployable-loader leakage test, whole-trajectory/fault-setting split audit, role-hash rejection, and nonzero safety/contact roles. Before confirmatory generation: freeze/hash complete `schema.json` + `config.json`, preserve ordinary/diagnostic conditions separately, and rerun all gates.

## Transcript-order rule

Before every chat append: read the UTF-8 physical tail, patch against unique exact tail text, and re-read immediately afterward. If an append ever lands mid-file, preserve history and add a tail correction; if safe correction is not possible, report in the Claude–Codex–Human channel. Session 7's main turn landed correctly, but a 15:41 bounded-window addendum matched the earlier Session-6 `— Codex` marker; the misplaced entry was preserved and an explicit 15:42 correction was appended at the verified physical tail. Do not use a bare speaker-signature anchor again.

## Public/session status

- Root README remains Phase 2 / `In Progress`. Session 7 added one lean heartbeat because the schema's causal online execution order became executable; it explicitly says this is scaffolding, not a result, and config remains unfrozen.
- Detailed session record: `agents/Codex/Session Summaries/HumanReport7.md`.
- **Next Codex session is Session 8 and must include the regular progress report in addition to normal work.**
