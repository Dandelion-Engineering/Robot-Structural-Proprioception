# Summary of Only Necessary Context — Codex

**Rewritten:** 2026-07-17 14:17 PDT

**Current phase:** Phase 2 — Execution

**Codex session just completed:** Session 6 · **Next:** Session 7

## Current authoritative state

Phase 0 and Phase 1 are closed. The jointly approved technical Claim Sheet, Accessible Claim Sheet, Study Guide Pass 1, and `Reproducibility Packet/schema/schema-v1.0.md` remain in force. The Claim Sheet awaits Randy's non-blocking review in `director_requests.md`; Phase-2 work continues.

Active Claude–Codex coordination is now `chats/Claude-Codex/Phase 2 Integration and Config Freeze/Phase 2 Integration and Config Freeze - Active.md`. The old Claim Sheet review thread is concluded. The director's `Chat Appends` thread is also concluded after Codex Session 6 appended its acknowledgment at the verified physical tail and created the summary.

## Mechanics decision that remains binding

The native MuJoCo cable/rod candidate is selected only under bounded matched diagnostic excitation:

- Ordinary torque-only condition: **BLOCK** (structural 1.92 µε, actuator 5.81 µε, separation 5.81 µε; all below 10 µε).
- Diagnostic condition: **PASS** (1.0 N peak, 0.8 Hz zero-mean distal transverse sinusoid; structural 10.24 µε, actuator/separation 23.87 µε).
- Fine model: 17 centerline points / 16 segments per link, 0.1 ms MuJoCo step, 2 ms control step.
- `n_def=90`: shortest three-component log-map rotation for each of 15 internal ball joints per link; exclude the L1 shoulder ball pose and L2 elbow-side free pose.
- Gauges: link 1 at 0.25/0.75 L; link 2 at 0.25/0.75 L.
- Structural development fault: link-2 section `[0.55,0.85]`, remaining EI 0.50.
- Actuator development fault: elbow remaining gain 0.70 downstream of unchanged upstream `control_effort`.
- Reserve: volumetric 3-D flex; PyElastica external fallback only if later cable validation fails.

Do not report the mechanics gate as a research-hypothesis result. Preserve the ordinary BLOCK as its own `trajectory_spec_id` condition.

## Session-6 plant→sensor implementation

`Reproducibility Packet/scripts/utils/cable_mechanics.py` now holds the single selected-model implementation used by both the full gate and runtime producer. The full gate was rerun after refactor and returned PASS; archived `fine_metrics`, refinement, beam-validation, candidate-contract, gate, and decision objects are value-identical.

`Reproducibility Packet/scripts/utils/cable_plant.py:CablePlant` is the schema-facing plant producer. `advance()` integrates one 2 ms control interval (20 × 0.1 ms physics steps), applies structure/actuator faults only in the physical path, and emits a complete `PlantStepState`. `rollout()` stacks those states into a validated `PrivilegedRecord`.

`PlantStepState` is now lossless across all schema-B fields. This corrected Claude's proposed sensor-subset carrier, which had made `PrivilegedRecord.slice_step()` drop `qdd_true`, deformation/curvature, contact/task/tracking fields, and flags. The narrow leakage boundary is still `observable_sources()`; it excludes delivered torque, deformation/curvature, task truth, labels, and other privileged-only fields.

`Reproducibility Packet/scripts/make_mujoco_plant_trace.py` writes a real non-pickled `plant/<run_id>.npz` and `plant/index.csv`. Current hashes are prefixed `dev-`; they are not confirmatory. `run_sensor_model.py` inherits the matching plant-role index hash for its observation role. The analytic synthetic plant remains optional test support only.

## Sensor review state — owner re-review required

Codex reviewed Claude's Session-6 sensor implementation and directly corrected one bug: `qd_obs[t]`, a backward difference, is now valid only if both `q_obs[t]` and `q_obs[t-1]` are valid. Previously the step after encoder dropout could contain `NaN` marked valid.

Codex's 14:13 PDT turn explicitly approves the current edited **development interface state** (`schema_types.py`, shared mechanics/plant producer, corrected `sensor_model.py`) and hands it back to Claude. The review loop is **open** until Claude genuinely re-opens the files and explicitly approves the same state or edits and returns it. Do not infer approval from Claude's initial proposal.

## Verified integration state

- Full packet suite: **25 passed**.
- Python compileall: passed.
- Full mechanics gate after refactor: PASS, value-identical scientific objects.
- Real integration run: 1,500 steps at 500 Hz, `n_def=90`, persisted/loaded successfully.
- Real trace → matched C1/S: C1 gauge arrays all NaN; S gauges present; shared channels and masks bitwise-identical under CRN; valid entries finite; plant/observation role hashes match.
- Packet-only copy: all 25 tests and a real plant-producer smoke run passed without repository-sibling code.

The packet README now documents the real plant trace before sensor generation. It still correctly says the current sensor CLI is batch: `CablePlant.advance()` provides the online seam, but sensing→estimator→controller is not interleaved yet.

## Shared config status — deliberately not frozen

Exact plant-side values ready for the complete config:

- `f_ctrl=500 Hz`; `dt=0.002 s`.
- MuJoCo timestep `0.0001 s`.
- `n_def=90`; four gauge locations above.
- Gate-supported diagnostic amplitude/frequency: 1.0 N peak, 0.8 Hz.

Still open: diagnostic duration/envelope, `W`, `stride`, remaining sensor pathology sanity check, severity/onset grids, contact/safety widths and thresholds. The gate used the sinusoid through its complete 3 s run; it did **not** validate a separately windowed/tapered short burst. Preserve that distinction and either retain the gate condition for pilot or run burst sensitivity before freeze.

Do not create a partial file named the immutable shared `config.json`. Current `dev-` traces must be rejected from confirmatory use.

## Exact resume path

1. Read the true tail of the active Phase-2 integration thread; Claude may have re-reviewed or edited the handed-back state.
2. If Claude approves the same state, record the interface review loop closed. If Claude edits, inspect the actual diff and continue the explicit review cycle.
3. Converge remaining full-config values, especially the diagnostic envelope and Claude's `W`/`stride` proposal. Do not freeze until the complete mechanics + sensor + timing + fault + split/evaluation surface is reviewed.
4. Add a stateful per-step sensor interface so `CablePlant.advance()` → sensing → estimator → controller interleaves online; batch trace replay is development-only and cannot be the confirmatory execution order.
5. Implement Codex's interpretable residual/linear system-ID baseline and recovery controller against the online seam once the interface/config gate closes.
6. Before pilot: define safety/contact role widths, implement the deployable-loader leakage test and whole-group split audit, and reject any role with mismatched or `dev-` config hash.
7. Before confirmatory generation: freeze/hash complete `schema.json` + `config.json`, keep ordinary and diagnostic trajectories separate, and run all focused/full gates.

## Transcript-order rule

Before every chat append: read the UTF-8 physical tail, patch against exact stored tail text, and re-read immediately afterward. If a reply lands elsewhere, preserve history and add a safe tail correction; if that cannot be done without risking prior content, report in the Claude–Codex–Human channel. Session 6 followed this successfully for both the director acknowledgment and Phase-2 handoff.

## Public/session status

- Root README remains Phase 2 / `In Progress`. Session 6 did not add a heartbeat because this was internal integration infrastructure, not a phase close, finished artifact, amendment, or research result.
- No Codex research progress report was due (next regular trigger: Session 8; no event trigger this session).
- Detailed session record: `agents/Codex/Session Summaries/HumanReport6.md`.
