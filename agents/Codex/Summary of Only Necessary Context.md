# Summary of Only Necessary Context — Codex

**Rewritten:** 2026-07-17 12:38 PDT

**Current phase:** Phase 2 — Execution

**Codex session just completed:** Session 5 · **Next:** Session 6

## Current authoritative state

Phase 0 and Phase 1 are closed. The technical [`../../Claim Sheet.md`](../../Claim%20Sheet.md), [`../../Accessible Claim Sheet.md`](../../Accessible%20Claim%20Sheet.md), [`../../Study Guide/Pass 1 - Conceptual Foundation.tex`](../../Study%20Guide/Pass%201%20-%20Conceptual%20Foundation.tex) plus [PDF](../../Study%20Guide/Pass%201%20-%20Conceptual%20Foundation.pdf), and co-owned [`../../Reproducibility Packet/schema/schema-v1.0.md`](../../Reproducibility%20Packet/schema/schema-v1.0.md) are jointly approved. Schema v1.0 is in force; changes require the append-and-date amendment protocol.

Claude Session 5 genuinely re-reviewed and approved Codex's edited schema state, closed the last Phase-1 gate, created the non-blocking Claim Sheet director request, flipped the public README to Phase 2, and wrote the phase-transition report. Codex Session 5 then completed the bounded mechanics feasibility spike assigned as the first plant-side Phase-2 gate.

The authoritative live record remains [`../../chats/Claude-Codex/Claim Sheet Review and Division of Labor/Claim Sheet Review and Division of Labor - Active.md`](../../chats/Claude-Codex/Claim%20Sheet%20Review%20and%20Division%20of%20Labor/Claim%20Sheet%20Review%20and%20Division%20of%20Labor%20-%20Active.md). Read its true tail before acting.

## Mechanics gate decision — qualified PASS

The runnable spike is [`../../Reproducibility Packet/scripts/run_feasibility_spike.py`](../../Reproducibility%20Packet/scripts/run_feasibility_spike.py). It uses two first-party MuJoCo cable elements, four curvature-derived gauges, a localized structural stiffness loss, downstream actuator-gain loss, and observation-only encoder bias.

The decision is **excitation-dependent**:

- **Ordinary joint-torque excitation: BLOCK.** Structural max gauge RMS 1.92 µε; actuator max 5.81 µε; structural-versus-actuator max separation 5.81 µε. All remain below the unchanged 10 µε credibility floor. Preserve this result; report and machine-readable outputs are in [`../../Reproducibility Packet/results/feasibility_spike_ordinary_excitation_blocked/`](../../Reproducibility%20Packet/results/feasibility_spike_ordinary_excitation_blocked/).
- **Matched bounded diagnostic excitation: PASS.** Adding the same zero-mean 1.0 N, 0.8 Hz distal load to every scenario gives structural max 10.24 µε, actuator max 23.87 µε, and structural-versus-actuator separation 23.87 µε. Encoder observation RMS changes 0.050 rad while the physical gauge and IMU histories remain unchanged. Outputs are in [`../../Reproducibility Packet/results/feasibility_spike/`](../../Reproducibility%20Packet/results/feasibility_spike/).

Native MuJoCo cable/rod mechanics are selected for the next plant implementation **only with this diagnostic-excitation condition attached**. Volumetric 3-D flex remains the compiled reserve; PyElastica remains the external fallback. This gate is not a research-hypothesis result and must never be reported as one.

## Validation state

- Timestep relative signature error max: 0.212 ≤ 0.25.
- Mesh relative signature error max: 0.127 ≤ 0.25.
- Independent Euler–Bernoulli maximum gauge-strain error: 2.06% ≤ 10%.
- Independent tip-deflection error: 10.97% ≤ 15%.
- Reserve 3-D flex: compiled and finite; 36 vertices, 48 tetrahedra, `nq=96`.
- Focused tests: 4 passed.
- Full diagnostic run returns exit 0; full ordinary negative control returns the expected exit 2.
- Both diagnostic 300-DPI figures were visually inspected and are legible.

## Selected plant contract to integrate

- Candidate mechanics: first-party MuJoCo native cable/rod.
- Each link: 0.4 m, aluminum-like `E=69 GPa`, density 2700 kg/m³, 20 mm × 4 mm rectangular section.
- Fine discretization: 17 points / 16 segments per link; simulation timestep 0.1 ms; control timestep 2 ms.
- `n_def=90`: three-component log-map rotation vector for each of 15 internal cable ball joints per link; shoulder and elbow rigid-joint coordinates excluded.
- Gauge stations: link 1 at 0.25 L / 0.75 L and link 2 at 0.25 L / 0.75 L.
- Structural spike fault: link-2 section `[0.55, 0.85]` at 50% remaining EI.
- Actuator spike fault: elbow delivered-torque gain 0.70 downstream of the unchanged upstream proxy.
- Encoder spike fault: +0.05 rad shoulder observation bias, plant unchanged.

These values are machine-readable under `candidate_contract` and `config` in the PASS `summary.json`. Do **not** create an incomplete file called the immutable shared `config.json`. Integrate Claude's exact sensor/fault/evaluation values and freeze the complete config before pilot or confirmatory generation.

## Runtime and storage invariants that remain binding

- Plant, sensing, estimator, and controller interleave online at each control step; stored records are role-separated traces, not an offline plant-first replay.
- Sensor faults enter observations only. Structural and actuator faults enter plant/actuation. The current proxy remains upstream of actuator gain loss.
- The next plant-side interface should be a single-step schema slice. Codex recommended the explicit name `PlantStepState`; implement it rather than continuing with spike-only full-history objects.
- `tau_cmd` is pre-limit request; `control_effort` is saturated upstream proxy/actuator-side effort; `tau_delivered_true` is post-fault physical torque.
- Deployable loaders receive only their suite's observation index/root. Identity manifest, labels, privileged plant truth, oracle, and other-suite payloads remain unreachable.
- Before fitting: audit that each `pair_id`, `trajectory_spec_id`, and `fault_setting_id` belongs to exactly one split and no `run_id` is split over time.
- Shared-channel random innovations use deterministic pair/channel/step substreams so S-only gauge draws cannot shift later C1/S shared noise.

## Exact resume path

1. Read the true tail of the active Claude–Codex transcript and inspect current repo state; Claude may have integrated sensor/evaluation work after this handoff.
2. If the complete shared config is ready, genuinely review all mechanics, sensor, timing, window, split, and evaluation values before freezing it. Do not accept a partial immutable config.
3. Implement Codex's schema-facing `PlantStepState` and plant-trace persistence against v1.0, using the selected cable candidate and `n_def=90`.
4. Connect Claude's sensor-realism/fault map and evaluation harness through the per-step boundary; verify encoder faults remain relational and that shared-channel CRN substreams remain matched.
5. Keep diagnostic and ordinary excitation as separate `trajectory_spec_id` conditions. The ordinary BLOCK remains visible and is not superseded.
6. Before any pilot, run focused unit tests plus the full mechanics gate. Before confirmatory generation, freeze complete `schema.json`/`config.json`, validate role-separated storage and loader leakage tests, and hash the artifacts.
7. Escalate to volumetric 3-D flex or PyElastica only if later validation reveals a cable-specific failure.

## Transcript-order note

Codex's substantive Session-5 mechanics handoff (12:38 PDT) was accidentally inserted near the beginning of the active transcript because a generic patch anchor matched an earlier Claude sign-off. No prior transcript content was removed or moved. A correction at the true tail declares that handoff the latest substantive turn. Preserve both entries; do not clean up the append-only history.

The same pattern exists for Codex Session 4: its substantive review turn is physically earlier than Claude Session 4, with a tail correction naming the intended order. Read correction notes, not physical position alone.

## Public and session status

- Root [`../../README.md`](../../README.md) is Phase 2 / `In Progress` and includes one lean mechanics-gate heartbeat naming both the ordinary BLOCK and diagnostic PASS.
- [`../../director_requests.md`](../../director_requests.md) contains the non-blocking Claim Sheet review request; work continues while it awaits the director.
- The Reproducibility Packet working surface now has a self-contained runbook, pinned requirements, packet-local ignore file, `DATA.md`, code, tests, both condition outputs, and reports/figures. It is still a Phase-2 working packet, not the final Phase-3 verification artifact.
- Detailed Session-5 record: [`Session Summaries/HumanReport5.md`](Session%20Summaries/HumanReport5.md).
- Codex's next regular research-progress trigger is Session 8 unless a material event triggers one earlier.
