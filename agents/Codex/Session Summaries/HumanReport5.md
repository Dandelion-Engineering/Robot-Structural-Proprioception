# Human Report 5 — Codex

**Date/time:** 2026-07-17 12:38 PDT

**Agent:** Codex · **Session:** 5 · **Project phase:** Phase 2 — Execution (mechanics feasibility gate completed; plant integration next)

## Summary

This session executed Codex's first Phase-2 assignment: a bounded mechanics spike deciding whether the smaller native MuJoCo cable/rod route can produce physically evolved, distinguishable structural, actuator, and encoder-fault signatures above the project's declared sensor credibility floor, or whether the project must escalate to volumetric 3-D flex or PyElastica.

The result is a **qualified PASS**. Native cable/rod mechanics clear the gate when the matched experiment includes a bounded, zero-mean 1.0 N distal diagnostic load. The first ordinary joint-torque-only run correctly **BLOCKS**: its structural and actuator gauge signatures remain below the unchanged 10 µε credibility floor. Both conditions are preserved and reproducible from the same script. The native cable route is selected for the next plant implementation because the declared diagnostic-excitation condition clears signal, separation, numerical-refinement, and independent-beam checks; volumetric 3-D flex remains the reserve. This is a mechanics-method decision, not evidence that the research hypothesis succeeds.

The selected fine candidate uses 17 centerline points / 16 cable segments per link and exposes `n_def=90`: three-component log-map rotations for 15 internal ball joints on each of two links, excluding the shoulder and elbow rigid-joint coordinates. The four gauge stations remain fixed at 0.25 L and 0.75 L on each link. These values are machine-readable in the PASS summary and are ready for the shared configuration freeze once the sensor/evaluation constants are integrated.

## What was accomplished

1. **Reconstructed the authoritative state and closed the cross-review obligation.** Read `AgentPrompt.md`, all controlling project context, Codex continuity, both chat records, the complete live Claude–Codex thread, the Claim Sheet, schema v1.0, Claude's latest Human Report and phase-close report, the Reproducibility Packet and live-run playbooks, and current repository state. Claude Session 5's same-state schema approval and Phase-1 close matched the actual files and transcript; no discrepancy required a review response.

2. **Verified the candidate mechanics against current first-party documentation.** Re-checked the current MuJoCo modeling and elasticity documentation and the first-party plugin source. The native cable model represents large-deformation 1-D bending/twist mechanics with material/cross-section stiffness; generic 1-D flex was not treated as a beam. The volumetric candidate was exercised only as the specified reserve. The source ledger now records the exact Phase-2 implementation decision.

3. **Implemented the native two-link mechanics spike.** `run_feasibility_spike.py` builds two 0.4 m aluminum-like cable links with 20 mm × 4 mm rectangular sections, a shoulder and connected elbow, two site-transmission motors, a distal IMU, and four virtual gauges. Gauge output is derived from simulator-integrated segment orientation/curvature at fixed stations; no fault label or encoder value is copied into a gauge channel.

4. **Implemented physically separated fault boundaries.** The structural case reduces link-2 bending inertia to 50% over normalized section `[0.55, 0.85]`; the actuator case applies 70% delivered elbow torque downstream of an unchanged command/current proxy; the encoder case adds a 0.05 rad observation bias without changing the plant, gauge, or IMU history. This directly realizes the schema's plant-versus-observation fault boundary.

5. **Preserved the ordinary-excitation negative result.** With the distal diagnostic load disabled, structural max gauge RMS was 1.92 µε, actuator max was 5.81 µε, and structural-versus-actuator max gauge separation was 5.81 µε. All are below the 10 µε floor. The script returns exit code 2 and the complete report, summary, metrics, and figures remain under `results/feasibility_spike_ordinary_excitation_blocked/`.

6. **Cleared the diagnostic-excitation gate without weakening its thresholds.** Adding the same zero-mean 1.0 N, 0.8 Hz distal load to every matched scenario raised the structural max gauge RMS to 10.24 µε, actuator max to 23.87 µε, and structural-versus-actuator max separation to 23.87 µε. The encoder case changed observed joint angle by 0.050 rad while physical gauge and IMU changes remained exactly zero. Every original threshold remained unchanged.

7. **Passed numerical and independent-physics checks.** The full run compares 9-point models at 0.2 ms and 0.1 ms plus a 17-point model at 0.1 ms. Maximum signature error was 0.212 across the timestep comparison and 0.127 across the mesh comparison, both within the predeclared 0.25 limit. Against an Euler–Bernoulli cantilever check, maximum gauge-strain error was 2.06% (limit 10%) and tip-deflection error was 10.97% (limit 15%).

8. **Exercised the reserve candidate.** A slender volumetric 3-D flex compiled and remained finite for a smoke step with 36 flex vertices, 48 tetrahedral elements, and 96 generalized coordinates. It remains a reserve rather than an added runtime dependency or second full plant because the native route cleared the gate.

9. **Made the result reproducible and reviewable.** Added a pinned packet requirements file, packet-local `.gitignore`, outsider-facing sequential runbook, `DATA.md`, one-purpose script, focused tests, machine-readable JSON/CSV, human reports, and two 300-DPI figures per condition. The command line now exposes `--diagnostic-tip-load-peak-n 0` so the ordinary negative control is reproducible rather than merely archived.

10. **Published the qualifying heartbeat and handed off the result.** Appended one lean, honest live-run README entry naming the excitation dependence; appended a detailed Claude handoff with metrics, `n_def`, gauge locations, and the proposed per-step object name `PlantStepState`; and preserved an append-only transcript-order correction after the substantive chat patch matched an earlier Claude sign-off.

## Important decisions and reasoning

### 1. Select native cable mechanics, but only with the excitation condition attached

The diagnostic condition passes the same credibility, separation, convergence, and validation gates that the ordinary condition fails. The smallest sufficient mechanics route is therefore justified for the next implementation, but its selection must always carry the condition that active diagnostic excitation is available. Ordinary operation does not inherit the PASS.

### 2. Preserve the failed ordinary condition as a first-class output

The ordinary run is scientifically useful: it demonstrates that joint-torque excitation alone does not reliably lift the structural signature above a conservative thermal-cross-sensitivity floor in this candidate plant. Deleting or overwriting it after the diagnostic run passed would hide the reason active excitation matters. Both output trees and both exact commands are retained.

### 3. Use internal relative rotations as `deform_coords`

The selected model has 15 internal cable ball joints per link after excluding each link's rigid attachment coordinate. Representing each internal joint by a three-component quaternion log-map gives 90 fixed-width deformation coordinates. This is independent of the four gauge readouts and preserves 3-D bending/twist information while keeping the shoulder and elbow joint state in the separate `q` fields.

### 4. Do not freeze a partial shared `config.json`

The spike now supplies exact mechanics values, `n_def`, gauge locations, timestep, and control step in machine-readable form. The shared configuration also needs Claude's exact sensor/fault/evaluation values and is contractually immutable once frozen. Creating a partial file labeled as the shared frozen config would be misleading; integration and freeze should occur once the full values are present, before pilot or confirmatory generation.

## Challenges and how they were handled

- **The first full run blocked.** Rather than lowering the 10 µε floor or exaggerating sub-floor patterns, the ordinary result was preserved and the already-allowed diagnostic-excitation condition was evaluated with a bounded matched load. That produced a transparent excitation-dependent decision.
- **The structural fault needed to affect mechanics, not labels.** Local cable section thickness is modified over a proper subset of link-2 segments, exploiting the cubic thickness dependence of bending inertia. A focused test verifies the bounded subset and 50% EI scale; measured gauge histories then arise from the evolved model.
- **A smaller engine-native model still needed independent validation.** Mesh/timestep refinement alone can converge to the wrong physics. The spike therefore includes a separate Euler–Bernoulli strain/deflection calculation with explicit limits and a volumetric-flex smoke probe.
- **The live transcript patch matched an earlier sign-off.** No existing transcript text was moved or deleted. A tail correction identifies the Session-5 mechanics handoff as the latest substantive turn, preserving the append-only record.
- **Generated MuJoCo logging appeared during an unstable exploratory model.** The local log was inspected and removed, then `MUJOCO_LOG.TXT` was added to both the project and packet ignore boundaries so machine-local diagnostics cannot leak into commits.

## Files created or updated

Created:

- `Reproducibility Packet/scripts/run_feasibility_spike.py`
- `Reproducibility Packet/tests/test_feasibility_spike.py`
- `Reproducibility Packet/README.md`
- `Reproducibility Packet/DATA.md`
- `Reproducibility Packet/requirements.txt`
- `Reproducibility Packet/.gitignore`
- `Reproducibility Packet/results/feasibility_spike/` — qualified-PASS JSON, CSV, report, and figures.
- `Reproducibility Packet/results/feasibility_spike_ordinary_excitation_blocked/` — ordinary-condition BLOCK JSON, CSV, report, and figures.
- `agents/Codex/Session Summaries/HumanReport5.md` — this report.

Updated:

- `.gitignore` — ignores MuJoCo's machine-local log.
- `README.md` — one qualifying live-run heartbeat for the mechanics decision.
- `agents/Codex/references.md` — current first-party MuJoCo implementation sources and their decision role.
- `chats/Claude-Codex/Claim Sheet Review and Division of Labor/Claim Sheet Review and Division of Labor - Active.md` — mechanics handoff plus tail order correction.
- `agents/Codex/README.md` — workspace map and current state.
- `agents/Codex/Summary of Only Necessary Context.md` — completely rewritten for Session 6.

## Verification performed

- `python -m py_compile Reproducibility Packet/scripts/run_feasibility_spike.py` — passed.
- `python -m pytest Reproducibility Packet/tests -q` — **4 passed**.
- Full diagnostic command — **PASS, exit 0**, reproduced after final script changes.
- Full ordinary negative-control command — **BLOCK, expected exit 2**, reproduced after final script changes.
- All diagnostic gate booleans in `summary.json` — true.
- 3-D flex compile/finite smoke checks — true.
- Both 300-DPI diagnostic figures — visually inspected and legible; no clipping or misleading scale issue found.
- Packet-only isolation check — copied only `Reproducibility Packet/` to a temporary directory, ran all four tests and a quick smoke command from that copy, then removed the verified temporary directory; passed without reaching any repository sibling file.
- `git diff --check` — no whitespace errors before closeout; Windows line-ending notices only.
- No dependency was installed this session: MuJoCo 3.10.0 and the other pinned packet dependencies were already present in the project `venv`.

## Next steps

1. Integrate the exact mechanics candidate fields into the complete shared `config.json` alongside the sensor/evaluation constants, then freeze it before pilot or confirmatory generation.
2. Implement the schema-facing per-step plant handoff (`PlantStepState`) and the role-separated persisted plant trace.
3. Connect the full thermal, drift, lag, dropout, and sensor-fault map without changing the plant/observation fault boundary verified here.
4. Preserve active diagnostic excitation as a separate declared condition; do not treat the ordinary torque-only BLOCK as erased by the diagnostic PASS.
5. Escalate to volumetric 3-D flex or PyElastica only if later plant validation reveals a cable-specific failure; do not add that complexity preemptively.
