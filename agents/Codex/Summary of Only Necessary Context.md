# Summary of Only Necessary Context — Codex

**Rewritten:** 2026-07-19 21:12 PDT

**Current phase:** Phase 2 — Execution

**Codex session just completed:** Session 9 · **Next:** Session 10

## Current authoritative state

Phase 0 and Phase 1 remain closed. The jointly approved Claim Sheet, Accessible Claim
Sheet, Study Guide Pass 1, and original schema v1.0 remain in force. The Claim Sheet still
awaits Randy's non-blocking review in `director_requests.md`; execution continues.

The authoritative coordination file is
`chats/Claude-Codex/Phase 2 Integration and Config Freeze/Phase 2 Integration and Config Freeze - Active.md`.

Claude Session 9 genuinely re-reviewed and explicitly approved Codex Session-8's exact
`estimator.py`/`test_estimator.py` edited state. That loop is closed.

Two review obligations are now open after Codex Session 9:

1. Claude must genuinely owner-re-review Codex's edits to
   `scripts/analyze_synchronous_detection_floor.py`, new shared
   `scripts/utils/synchronous.py`, the focused tests, and regenerated detector artifact,
   then explicitly approve the same state or edit and hand it back.
2. Claude must review the exact appended schema Amendment A1 plus fixed-width
   `schema_types.py` / `CablePlant` implementation and explicitly approve the same state
   before A1 is jointly in force. The underlying role semantics were approved by Claude
   Session 9, but that does not substitute for exact-state review.

Do not infer either approval from use, silence, or a later unrelated handoff.

## Corrected synchronous detector state

The detector-side concept remains valid, but Session 9 corrected the implementation:

- The old W=512 sequential detrend + raw projection was phase dependent: after its
  phase-zero calibration, a unit tone recovered 0.345–1.159 across phase.
- `utils/synchronous.py` now jointly fits intercept, linear trend, cosine, and sine and
  returns phase-invariant harmonic coefficients/amplitude.
- Default development window is W=640 (1.280 s at 500 Hz), which contains the complete
  1.25 s / 0.8 Hz probe. A one-cycle surrogate rejects a shorter window.
- A linear 3 °C/window path checks modeled trend rejection; it is not claimed as a bound
  on nonlinear or probe-band thermal behavior.
- Injected tone/burst targets in the detector-floor script are explicit surrogates. The
  actual mechanics-coupled margin is evaluated separately.

Regenerated W=640 detector artifact (`results/synchronous_detection_floor/`):

- broadband RMS 17.35 µε; detrended RMS 1.01 µε;
- harmonic NES 0.111 ± 0.059 µε;
- development threshold (mean + 5 standard deviations) 0.405 µε;
- gate-floor / mean-NES ratio 90×;
- harmonic design condition number 4.44, 1.024 cycles in window.

This is detection only, not source attribution. The threshold is development-only and
must later be frozen from validation data.

## Actual-trace safe-probe result — pilot candidate, not freeze

New `scripts/screen_synchronous_safe_probe.py` imports the corrected detector threshold,
measures the same feature on actual four-gauge MuJoCo fault-minus-healthy histories, and
checks development safety across healthy, structural, actuator, and encoder scenarios.

Focused six-row grid selected:

- task torque scale: **0.50** of the ordinary deterministic task waveform;
- diagnostic: **0.05 N peak**, **0.8 Hz**, **one 1.25 s raised-cosine cycle** starting at
  the fault boundary;
- feature window: **W=640**;
- actual harmonic amplitudes: structural **1.015 µε** (gauge 3), actuator **0.898 µε**
  (gauge 1), structure–actuator separation **1.090 µε** (gauge 3);
- minimum detector margin: **2.22×** over 0.405 µε;
- worst all-scenario safety: angle **1.895 rad**, speed **3.909 rad/s**, gauge
  **38.83 µε**, tip radius **0.712 m**; all inside current development limits.

The 0.05 N / 0.40 task-scale row was safe but missed the 2× rule at 1.69×. The 0.15 N
rows violated the angle limit. The selected row advances only to a pilot sweep; no current
trace may enter confirmatory analysis. It still fails the historical 10 µε per-sample
mechanics screen, which remains preserved as the original mechanics-selection record.

## Safety/contact truth and proposed schema Amendment A1

Session 9 found that the original bounded-burst safety code checked only the healthy
rollout. Expanding it across scenarios then exposed a second bug: the encoder bias step
created a false 25 rad/s event when safety read `qd_obs`. `SimulationResult` now preserves
`qd_true_rad_s`; safety reads privileged physical truth across every scenario.

Appended Amendment A1 (Codex-approved, Claude exact-state review pending):

- `contact_state[2]`: `tip_contact_force_n`, `tip_contact_active`;
- `safety_flag[7]`: joint-angle ×2, joint-speed ×2, tip workspace, absolute gauge strain,
  tip contact force; `saturation_flag[2]` remains separate;
- development limits remain `|q|<=pi`, `|qd|<=10 rad/s`, tip radius `<=0.82 m`,
  `|gauge_true|<=500 µε`, tip contact force `<=5 N`.

`CablePlant` and the analytic fixture now emit fixed widths. Collision remains disabled,
so the current plant emits zero contact truth. If contact unexpectedly appears,
`CablePlant` fails; optional-contact pilots require real endpoint-contact extraction.

## Mechanics and config state

The mechanics substrate decision is unchanged:

- native MuJoCo cable/rod primary; volumetric 3-D flex reserve;
- 17 points / 16 segments per link; simulation step 0.0001 s; control 0.002 s / 500 Hz;
- `n_def=90`; shortest log-map rotations for 15 internal ball joints per link;
- gauges at L1/L2 0.25 and 0.75 L;
- development structural fault: link-2 `[0.55,0.85]`, remaining EI 0.50;
- development actuator fault: elbow remaining gain 0.70 downstream of unchanged
  `control_effort`;
- ordinary task-only remains a separate `trajectory_spec_id` negative control.

The original 1.0 N bounded-burst artifact was regenerated through all-scenario true-speed
safety and remains BLOCK: one-cycle 8.18/7.84/12.33 µε at 4.53 rad / 37.74 rad/s;
two-cycle 8.67/13.38/17.49 µε at 21.06 rad / 37.74 rad/s. Continuous load clears the
legacy mechanics floor but fails safety.

**Do not freeze `config.json`.** Current role hashes remain `dev-`. Open fields/work:

- Claude exact-state re-review of detector edits and Amendment A1;
- build synchronous feature into `WindowFeatureExtractor`; pilot-sweep W=640 and stride
  (stride 8 remains proposed, not frozen);
- joint sanity-check of non-load-bearing sensor constants;
- shared severity/onset grids;
- validation-derived class, abstention, selective, and OOD thresholds;
- optional-contact extraction/cases;
- learned attribution heads, interpretable residual/system-ID baseline, and recovery
  controller;
- deployable-loader leakage test, whole-trajectory/fault-setting split audit, role-hash
  rejection, and multi-run storage checks before pilot/confirmatory generation.

## Exact resume path for Codex Session 10

1. Read the UTF-8 physical tail of the active Phase-2 thread. If Claude explicitly
   approves the exact detector edits, close that loop. If Claude edits, inspect the actual
   diff and continue the review cycle.
2. Separately resolve Amendment A1 exact-state review. Do not treat detector approval as
   schema approval or vice versa.
3. Review Claude's synchronous `WindowFeatureExtractor` increment if it lands. Check that
   it uses the shared phase-invariant harmonic implementation or an explicitly equivalent
   version, channel-specific measurement times/masks, and the W=640 full-cycle contract.
4. Implement real endpoint-contact extraction before any optional-contact pilot, or keep
   optional-contact cases blocked explicitly.
5. Continue Codex's interpretable residual/linear-system-ID baseline and recovery
   controller against the online seam; preserve the matched sensor-suite architecture.
6. Run the pilot over probe/task scale + W/stride and remaining shared grids. The current
   0.05 N / 0.50 task-scale row is a candidate, not a frozen value.
7. Before confirmatory generation, freeze/hash complete `schema.json` + `config.json`,
   preserve ordinary/diagnostic conditions separately, and rerun every leakage, split,
   safety, storage, and role-hash gate.

## Verification and session record

- Full packet: **91 passed**.
- `compileall`: passed.
- Detector, bounded-burst, and safe-probe CLI help: passed.
- Corrected detector artifact: 200 modeled sensor realizations, W=640.
- Both mechanics sensitivities regenerated at 17 points / 0.1 ms.
- Public README has one lean correction/safe-candidate heartbeat; no research result claim.
- Packet README contains exact copy-paste run steps for the three development sensitivities.
- Detailed session record: `agents/Codex/Session Summaries/HumanReport9.md`.
- Next regular Codex progress report remains Session 16 unless a phase/amendment trigger
  fires earlier. A1 is not approved yet, so Session 9 did not fire an approved-amendment
  progress report.

## Transcript-order rule

Before every chat append: read the UTF-8 physical tail, patch against unique exact tail
text, and re-read immediately afterward. Session 9's turn is physically last and appears
exactly once. Never use a bare speaker-signature anchor.
