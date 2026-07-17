# Codex workspace

This folder contains Codex-owned research, source records, and continuity for the **Robot Structural Proprioception** project.

## Authoritative research and sources

- [`Literature Foundation.md`](Literature%20Foundation.md) — Codex's independent Phase-0 field survey. It is a concluded research input; corrections discovered later propagate into current artifacts rather than rewriting the foundation.
- [`references.md`](references.md) — living source ledger for Codex's project work, including Phase-1 review sources. Reconcile it with Claude's independent ledger when the project bibliography is assembled.

## Continuity and session record

- [`Summary of Only Necessary Context.md`](Summary%20of%20Only%20Necessary%20Context.md) — authoritative Codex resume state. It is completely rewritten at each completed session.
- [`Session Summaries/HumanReport1.md`](Session%20Summaries/HumanReport1.md) — detailed record of Codex Session 1 (independent literature foundation and Phase-0 comparison).
- [`Session Summaries/HumanReport2.md`](Session%20Summaries/HumanReport2.md) — detailed record of Codex Session 2 (Claim Sheet review, edits, approval, and labor response).
- [`Session Summaries/HumanReport3.md`](Session%20Summaries/HumanReport3.md) — detailed record of Codex Session 3 (companion-artifact review, PDF verification, and schema v0.2).
- [`Session Summaries/HumanReport4.md`](Session%20Summaries/HumanReport4.md) — detailed record of Codex Session 4 (schema v1.0 review, implementation-boundary edits, approval, and owner handback).
- [`Session Summaries/HumanReport5.md`](Session%20Summaries/HumanReport5.md) — detailed record of Codex Session 5 (native MuJoCo mechanics spike, excitation-dependent gate, candidate selection, and runnable packet).
- [`Session Summaries/HumanReport6.md`](Session%20Summaries/HumanReport6.md) — detailed record of Codex Session 6 (lossless plant-interface review, real MuJoCo privileged trace, plant→sensor integration, and sensor-validity correction).

## Shared files outside this folder

- [`../../Claim Sheet.md`](../../Claim%20Sheet.md) — jointly approved Phase-1 technical contract; its same-state review loop is closed.
- [`../../Accessible Claim Sheet.md`](../../Accessible%20Claim%20Sheet.md) — jointly approved plain-language companion; its same-state review loop is closed.
- [`../../Study Guide/Pass 1 - Conceptual Foundation.tex`](../../Study%20Guide/Pass%201%20-%20Conceptual%20Foundation.tex) and [compiled PDF](../../Study%20Guide/Pass%201%20-%20Conceptual%20Foundation.pdf) — jointly approved director-facing conceptual guide; its same-state review loop is closed.
- [`../../Reproducibility Packet/schema/schema-v1.0.md`](../../Reproducibility%20Packet/schema/schema-v1.0.md) — co-owned shared data contract, jointly approved and in force.
- [`../../Reproducibility Packet/scripts/run_feasibility_spike.py`](../../Reproducibility%20Packet/scripts/run_feasibility_spike.py) — runnable native cable/rod mechanics gate with an ordinary-excitation negative control, diagnostic-excitation decision, refinement checks, beam validation, and a reserve 3-D-flex probe.
- [`../../Reproducibility Packet/scripts/utils/cable_mechanics.py`](../../Reproducibility%20Packet/scripts/utils/cable_mechanics.py) — co-owned shared selected-model mechanics and state extraction used by both the gate and runtime producer.
- [`../../Reproducibility Packet/scripts/utils/cable_plant.py`](../../Reproducibility%20Packet/scripts/utils/cable_plant.py) — Codex-owned one-control-step plant wrapper that emits complete schema-B `PlantStepState` objects.
- [`../../Reproducibility Packet/scripts/make_mujoco_plant_trace.py`](../../Reproducibility%20Packet/scripts/make_mujoco_plant_trace.py) — portable real-plant development trace CLI with role-separated persistence.
- [`../../Reproducibility Packet/scripts/utils/schema_types.py`](../../Reproducibility%20Packet/scripts/utils/schema_types.py) — co-owned schema-v1.0 carriers and the shared fault/interface boundary; current edited state awaits Claude's owner re-review.
- [`../../Reproducibility Packet/scripts/utils/sensor_model.py`](../../Reproducibility%20Packet/scripts/utils/sensor_model.py) — Claude-owned sensor-realism model; Codex's Session-6 validity correction awaits Claude's owner re-review with the shared interface.
- [`../../Reproducibility Packet/results/feasibility_spike/feasibility_spike_report.md`](../../Reproducibility%20Packet/results/feasibility_spike/feasibility_spike_report.md) — qualified-PASS report; native cable/rod selected under bounded diagnostic excitation.
- [`../../Reproducibility Packet/results/feasibility_spike_ordinary_excitation_blocked/feasibility_spike_report.md`](../../Reproducibility%20Packet/results/feasibility_spike_ordinary_excitation_blocked/feasibility_spike_report.md) — preserved torque-only BLOCK showing the selection's excitation boundary.
- [`../../chats/Claude-Codex/Claim Sheet Review and Division of Labor/Summary.md`](../../chats/Claude-Codex/Claim%20Sheet%20Review%20and%20Division%20of%20Labor/Summary.md) — concluded Phase-1 review/labor summary.
- [`../../chats/Claude-Codex/Phase 2 Integration and Config Freeze/Phase 2 Integration and Config Freeze - Active.md`](../../chats/Claude-Codex/Phase%202%20Integration%20and%20Config%20Freeze/Phase%202%20Integration%20and%20Config%20Freeze%20-%20Active.md) — authoritative active interface-integration/config-freeze thread; current producer/sensor edited state is handed back for Claude re-review.
- [`../../chats/Claude-Codex-Human/Chat Appends/Summary.md`](../../chats/Claude-Codex-Human/Chat%20Appends/Summary.md) — concluded director coordination record for the transcript-tail failure mode and recovery rule.
- [`../../chats/Claude-Codex/Phase 0 Coordination/Summary.md`](../../chats/Claude-Codex/Phase%200%20Coordination/Summary.md) — concluded Phase-0 convergence record that feeds the Claim Sheet.
- [`../../README.md`](../../README.md) — public live-run status, now Phase 2 / `In Progress`, including the mechanics gate's excitation-dependent heartbeat.

## Structure

```text
agents/Codex/
├── Literature Foundation.md
├── references.md
├── README.md
├── Summary of Only Necessary Context.md
└── Session Summaries/
    ├── HumanReport1.md
    ├── HumanReport2.md
    ├── HumanReport3.md
    ├── HumanReport4.md
    ├── HumanReport5.md
    └── HumanReport6.md
```
