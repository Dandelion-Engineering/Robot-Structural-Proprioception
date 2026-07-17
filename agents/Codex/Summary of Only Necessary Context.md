# Summary of Only Necessary Context — Codex

**Rewritten:** 2026-07-16 21:49 PDT

**Current phase:** Phase 1 — Sharpening (companion-artifact and schema review open)

**Codex session just completed:** Session 3 · **Next:** Session 4

## Current authoritative state

Phase 0 is concluded. The technical [`../../Claim Sheet.md`](../../Claim%20Sheet.md) same-state review loop is also **closed**: Claude genuinely re-reviewed Codex's Session-2 edits and explicitly approved the same state. The diagnosis-vs-plant/control labor split and schema-first sequencing are agreed.

The authoritative live record is [`../../chats/Claude-Codex/Claim Sheet Review and Division of Labor/Claim Sheet Review and Division of Labor - Active.md`](../../chats/Claude-Codex/Claim%20Sheet%20Review%20and%20Division%20of%20Labor/Claim%20Sheet%20Review%20and%20Division%20of%20Labor%20-%20Active.md). In Session 3, Codex reviewed and directly edited both companion artifacts, regenerated and visually verified the Study Guide PDF, explicitly approved those edited states, and returned them to Claude. Codex also revised schema v0.1 into v0.2, explicitly approved it, and handed it to Claude.

Three gates remain:

1. Claude must genuinely re-review and explicitly approve the current edited [`../../Accessible Claim Sheet.md`](../../Accessible%20Claim%20Sheet.md), or edit and return it.
2. Claude must do the same for [`../../Study Guide/Pass 1 - Conceptual Foundation.tex`](../../Study%20Guide/Pass%201%20-%20Conceptual%20Foundation.tex) and the regenerated [PDF](../../Study%20Guide/Pass%201%20-%20Conceptual%20Foundation.pdf).
3. Schema v0.2 must reach same-state approval, including the exact tracking-error convention, then be written as v1.0 under `Reproducibility Packet/schema/` before either lane installs dependencies or writes implementation code.

Do not close Phase 1, create the director request, flip the live-run phase, or start implementation until those gates close.

## Companion-artifact edits now awaiting Claude re-review

### Accessible Claim Sheet

- Wensing et al. is scoped to rigid-body inertial-parameter observability; it is not proof that this project's stiffness, actuator, or encoder faults are invisible to C1.
- Sravani & Venkata is labeled as a process-control illustration, not a robotics proof.
- Restored balanced accuracy; per-cause precision/recall; detection delay; Brier/NLL/ECE/reliability; fixed selective-risk working points; false abstention; OOD metrics; control effort/saturation; and the exact per-cause lower-95%-recall-bound > −0.02 guard.
- Hierarchical inference now explicitly resamples training seeds and then whole scenario/trajectory units while preserving C1/S pairs; SciPy is only a confidence-interval primitive.
- MuJoCo wording/links, gauge resolution/thermal bounds, CLI/config requirements, environment/hardware, licenses, and publication-output requirements now match the technical contract.

### Study Guide Pass 1

- Narrowed the Wensing theorem and analytical-redundancy claims to defensible source scopes.
- Corrected generic MuJoCo flex versus cable/rod mechanics and required independent validation if PyElastica becomes the plant.
- Known-class abstention counts as headline error; companion diagnosis/selective metrics and exact statistics are restored.
- The single tracking-error equation remains, but the guide says the schema/configuration must freeze its tracking space, units, norm, sampling, and numerical integration.
- “Pre-registration” was replaced by the project's actual commitment: pre-specification and a versioned configuration freeze.
- Final PDF: 13 letter-size pages, no LaTeX layout/package warnings, all pages visually inspected. The TOC was compacted to remove an orphaned one-line page.

## Shared schema v0.2 awaiting Claude review

The full proposal is at the tail of the active thread. Its load-bearing decisions are:

- `scenario_spec_id` = exogenous specification; `pair_id` = matched C1/S comparison; `run_id` = actual rollout. A pair may diverge in closed loop.
- Rollout-level manifest with grouped split keys, config hash, suite/estimator/controller identity, payload/environment/contact identifiers, and separate seeds. Suite never determines split.
- Privileged numeric fixed-grid plant arrays with declared shapes/units.
- Exactly four deployable signed surface-bending-strain channels in microstrain; privileged curvature is separate.
- Static suite availability mask and separate per-sample validity/dropout plus latency/age; on-disk missing values are `NaN`, and loaders pair any fill with masks.
- Sensor faults enter observations; structural/actuator faults enter plant/actuation; current proxy stays upstream of actuator loss; temperature truth is not deployable input.
- Labels, estimator outputs, and controller logs are physically separated; deployable loader gets an automated privilege-leakage test; O uses a separate allowlist.
- Past-only causal windows with measurement/availability times and frozen control/window/onset conventions.
- `manifest.csv` + numeric non-pickled `.npz` + immutable `schema.json`/`config.json` + SHA-256; no Parquet/YAML dependency without a reviewed measured need.
- Codex's tracking default: distal-endpoint planar position error in metres, L2 norm, control-grid sampling, trapezoidal integration over `[onset, onset + 5 s]`. Claude must explicitly approve or counter this before v1.0.

## Labor state

- **Codex:** feasibility spike/physics, virtual-gauge extraction, excitation design, interpretable residual/linear-sysID baseline, recovery controller.
- **Claude:** fault/sensor-realism model, matched attribution estimator/capacity ladder, calibration/abstention, RMA-style comparator, evaluation/statistics harness, Slot-8 demo, default-writer artifacts.
- **Shared:** versioned schema, fault library, headline diagnosis→control experiment, Reproducibility Packet, bibliography reconciliation.

Neither lane writes implementation code before schema v1.0 exists.

## Exact resume path

1. Read the true tail of the active Claim Sheet/review transcript before acting.
2. If Claude approves both companion artifacts unchanged, those loops close. If Claude edits either, re-open the entire returned state, genuinely review both diagnosis and implementation, and explicitly approve or return it. Escalate only if the same issue survives roughly two complete round-trips.
3. Review Claude's schema response the same way. Do not let the tracking-error convention, channel semantics, pairing/split rule, or privilege boundary become implicit in v1.0.
4. Once same-state approvals exist, write the approved schema artifact under `Reproducibility Packet/schema/`. Re-read the live tail before deciding which agent should write it.
5. If and only if both companion artifacts and schema v1.0 are closed, fire the Phase-1 transition once: create/append the non-blocking director request, update root `README.md`, and create the event-triggered progress report required by Project Details.
6. Then start Phase 2: Codex runs the bounded MuJoCo cable/rod versus slender-3D-flex feasibility spike; Claude starts the sensor/evaluation lane against the same schema. Do not install dependencies until the spike or reviewed lane need justifies them; use only `.\venv\Scripts\python.exe` / `.\venv\Scripts\pip.exe` and pin additions.

## Session and public-status notes

- Root `README.md` remains Phase 1 / `In Progress`. Session 3 completed Codex-side reviews but did not close a companion artifact or the phase, so no public heartbeat entry was added.
- No `director_requests.md` exists yet; creating it before the remaining Phase-1 gates close would be premature.
- No implementation code, project Python command, simulation, or dependency change has begun.
- Codex's next regular progress-report trigger is Session 8 unless an event trigger occurs first.
- Detailed Session-3 record: [`Session Summaries/HumanReport3.md`](Session%20Summaries/HumanReport3.md).
