# Summary of Only Necessary Context — Codex

**Rewritten:** 2026-07-16 22:35 PDT

**Current phase:** Phase 1 — Sharpening (one schema same-state approval gate remains)

**Codex session just completed:** Session 4 · **Next:** Session 5

## Current authoritative state

Phase 0 is concluded. The technical [`../../Claim Sheet.md`](../../Claim%20Sheet.md), [`../../Accessible Claim Sheet.md`](../../Accessible%20Claim%20Sheet.md), and [`../../Study Guide/Pass 1 - Conceptual Foundation.tex`](../../Study%20Guide/Pass%201%20-%20Conceptual%20Foundation.tex) plus [PDF](../../Study%20Guide/Pass%201%20-%20Conceptual%20Foundation.pdf) have each reached explicit dual approval of the same state. Their review loops are closed. The diagnosis-versus-plant/control labor split and schema-first sequencing remain agreed.

The only remaining Phase-1 gate is the co-owned [`../../Reproducibility Packet/schema/schema-v1.0.md`](../../Reproducibility%20Packet/schema/schema-v1.0.md). Claude created and approved a proposed v1.0 in Session 4. Codex genuinely reviewed it in Session 4, edited it, explicitly approved the edited state, and returned it to Claude. Claude must now genuinely re-review this exact edited state and either explicitly approve it or edit and return it.

Do not install/import a project dependency, write implementation code, create `director_requests.md`, flip the live-run README to Phase 2, or write the phase-transition progress report until Claude's same-state schema approval closes the gate.

The authoritative live record is [`../../chats/Claude-Codex/Claim Sheet Review and Division of Labor/Claim Sheet Review and Division of Labor - Active.md`](../../chats/Claude-Codex/Claim%20Sheet%20Review%20and%20Division%20of%20Labor/Claim%20Sheet%20Review%20and%20Division%20of%20Labor%20-%20Active.md). Read its true tail before acting.

## Schema v1.0 decisions already accepted by both agents in substance

- Separate `scenario_spec_id`, `pair_id`, and `run_id`; a matched C1/S pair may causally diverge in closed loop.
- C0/C1/S use one fixed deployable channel registry; S adds exactly four signed surface-bending-strain channels. O is a separate allowlisted oracle.
- Sensor faults enter observations; structural/actuator faults enter plant/actuation; the nominal current proxy remains upstream of actuator-gain loss.
- Estimator windows are past-only and honor per-channel measurement/availability time.
- The headline control quantity is distal-endpoint planar position error in metres, L2 norm, sampled on the control grid and integrated by the trapezoid rule over `[onset, onset + 5 s]`.
- The endpoint is the **true deformed tip**, using joint and deformation state, not rigid-model forward kinematics.
- C1/S pairs use common exogenous randomness; estimator/controller identifiers bind the same architecture + protocol across suites.
- Storage remains dependency-light: CSV, numeric non-pickled NPZ, immutable JSON configuration/schema, and SHA-256.

## Codex Session-4 schema edits awaiting Claude re-review

1. **Online dataflow:** plant → sensing → estimator → controller interleave at every control step. The stored records are role-separated traces, not a complete plant rollout generated before sensing.
2. **Role-separated persistence:** the identity manifest is path-free and non-deployable. Plant, per-suite observations, labels, per-suite estimator outputs, and per-suite controller logs each have separate roots/indexes and per-role NPZ payloads/hashes.
3. **No identity-metadata leakage:** `fault_setting_id` and related provenance can reveal the target, so inference loaders receive only their suite's observation index/root. A separate allowlisted training builder joins labels as targets, never as feature columns.
4. **Executable split audit:** before fitting, assert that `pair_id`, `trajectory_spec_id`, and `fault_setting_id` each map to one split and that no `run_id` is split over time. Suite never determines the split.
5. **Robust common random numbers:** shared-channel innovations use deterministic per-channel/per-step substreams (or equivalent counter-based RNG), so S-only gauge draws cannot shift later shared-channel noise. State-dependent observations may still differ after legitimate causal divergence.
6. **Actuator semantics:** `tau_cmd` is the pre-limit controller request; `control_effort` is the saturated actuator-side effort upstream of gain loss/current proxy; `tau_delivered_true` is post-fault physical torque.
7. **Timing/temperature detail:** validity and measurement/availability/age are per time and channel; temperature truth has four channels at the four gauge stations.

Codex explicitly approves the current edited schema state. If Claude changes any of these, re-open the entire returned schema and genuinely review both the diagnosis and implementation before approving or returning it.

## Labor state after schema approval

- **Codex:** bounded MuJoCo cable/rod versus slender-3D-flex feasibility spike; physics; virtual-gauge extraction; excitation design; interpretable residual/linear-system-ID baseline; recovery controller.
- **Claude:** sensor realism and fault injection; matched attribution estimator/capacity ladder; calibration/abstention; RMA-style comparator; evaluation/statistics harness; Slot-8 demo; default-writer artifacts.
- **Shared:** versioned schema/config, fault library, diagnosis-to-control headline experiment, Reproducibility Packet, bibliography reconciliation.

The feasibility spike remains the Phase-2 critical gate. It must test differential signatures at credible SNR and realistic stiffness using mechanics that actually represent bending; implementation details remain governed by the Claim Sheet.

## Exact resume path

1. Read the true tail of the active Claim Sheet/schema transcript before acting.
2. If Claude explicitly approves Codex's edited `schema-v1.0.md` unchanged, the schema loop and Phase 1 close.
3. On that close, fire the transition exactly once: create/append the non-blocking “Claim Sheet ready for director review” entry in `director_requests.md`, update the root README banner/log to Phase 2, and write the event-triggered phase-transition progress report.
4. Then begin Phase 2. Codex's first technical work is the bounded mechanics-only feasibility spike; install only the dependencies justified by that reviewed need, use the project `venv`, and pin what is committed.
5. If Claude edits the schema, review the full returned state. Escalate only if the same issue survives roughly two complete round-trips.

## Transcript-order note

Codex's substantive Session-4 schema-review turn (timestamp 22:33 PDT) was accidentally inserted after Claude's Session-2 opening turn because a patch anchor matched the first Claude sign-off. No prior transcript content was removed or changed. A timestamped correction at the true tail (22:34 PDT) declares that turn the latest substantive message. Preserve both entries; do not “clean up” the append-only history by deleting or moving them.

## Public and session status

- Root [`../../README.md`](../../README.md) remains Phase 1 / `In Progress`. Its latest lean log entry already says the companion artifacts are approved and schema v1.0 is in final review; Session 4 did not add another heartbeat because the schema and phase remain open.
- No `director_requests.md` exists yet.
- No implementation code, simulation, model training, project Python command, or dependency change has begun.
- Codex's next regular progress-report trigger is Session 8 unless the Phase-1 transition occurs first.
- Detailed Session-4 record: [`Session Summaries/HumanReport4.md`](Session%20Summaries/HumanReport4.md).
