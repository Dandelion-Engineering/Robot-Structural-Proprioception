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
- [`Session Summaries/HumanReport7.md`](Session%20Summaries/HumanReport7.md) — detailed record of Codex Session 7 (evaluation-core corrections, crossed bootstrap, stateful online sensing, and causal policy loop).
- [`Session Summaries/HumanReport8.md`](Session%20Summaries/HumanReport8.md) — detailed record of Codex Session 8 (estimator-interface corrections, bounded-burst BLOCK, contact/safety proposal, and config-freeze decision).
- [`Session Summaries/HumanReport9.md`](Session%20Summaries/HumanReport9.md) — detailed record of Codex Session 9 (phase-invariant detector correction, all-scenario safety truth, fixed contact/safety roles, and actual-trace safe-probe candidate).
- [`Session Summaries/HumanReport10.md`](Session%20Summaries/HumanReport10.md) — detailed record of Codex Session 10 (synchronous-feature phase-retention correction, safety-pairing guard, narrowed pilot-margin claim, and owner handback).
- [`Progress Reports/Progress Report Session 8.md`](Progress%20Reports/Progress%20Report%20Session%208.md) — regular every-eighth-session director update at the Accessible-Piece bar; next regular Codex report is Session 16.

## Shared files outside this folder

- [`../../Claim Sheet.md`](../../Claim%20Sheet.md) — jointly approved Phase-1 technical contract; its same-state review loop is closed.
- [`../../Accessible Claim Sheet.md`](../../Accessible%20Claim%20Sheet.md) — jointly approved plain-language companion; its same-state review loop is closed.
- [`../../Study Guide/Pass 1 - Conceptual Foundation.tex`](../../Study%20Guide/Pass%201%20-%20Conceptual%20Foundation.tex) and [compiled PDF](../../Study%20Guide/Pass%201%20-%20Conceptual%20Foundation.pdf) — jointly approved director-facing conceptual guide; its same-state review loop is closed.
- [`../../Reproducibility Packet/schema/schema-v1.0.md`](../../Reproducibility%20Packet/schema/schema-v1.0.md) — co-owned shared data contract; original v1.0 and appended fixed contact/safety Amendment A1 are jointly approved and in force.
- [`../../Reproducibility Packet/scripts/run_feasibility_spike.py`](../../Reproducibility%20Packet/scripts/run_feasibility_spike.py) — runnable native cable/rod mechanics gate with an ordinary-excitation negative control, diagnostic-excitation decision, refinement checks, beam validation, and a reserve 3-D-flex probe.
- [`../../Reproducibility Packet/scripts/utils/cable_mechanics.py`](../../Reproducibility%20Packet/scripts/utils/cable_mechanics.py) — co-owned shared selected-model mechanics and state extraction used by both the gate and runtime producer.
- [`../../Reproducibility Packet/scripts/utils/cable_plant.py`](../../Reproducibility%20Packet/scripts/utils/cable_plant.py) — Codex-owned one-control-step plant wrapper that emits complete schema-B `PlantStepState` objects.
- [`../../Reproducibility Packet/scripts/run_bounded_burst_sensitivity.py`](../../Reproducibility%20Packet/scripts/run_bounded_burst_sensitivity.py) — Codex-owned finite raised-cosine diagnostic sensitivity; current selected-model result blocks both one- and two-cycle candidates and keeps the diagnostic config field open.
- [`../../Reproducibility Packet/scripts/analyze_synchronous_detection_floor.py`](../../Reproducibility%20Packet/scripts/analyze_synchronous_detection_floor.py) and [`utils/synchronous.py`](../../Reproducibility%20Packet/scripts/utils/synchronous.py) — jointly approved detector sensitivity and shared harmonic utility: phase-invariant joint regression, full-cycle W=640 window, and bounded thermal/surrogate claims; the review loop is closed.
- [`../../Reproducibility Packet/scripts/screen_synchronous_safe_probe.py`](../../Reproducibility%20Packet/scripts/screen_synchronous_safe_probe.py) — Codex-owned actual-four-gauge mechanics/detector co-design screen; selects 50% task torque + 0.05 N one-cycle probe for the pilot sweep only.
- [`../../Reproducibility Packet/scripts/make_mujoco_plant_trace.py`](../../Reproducibility%20Packet/scripts/make_mujoco_plant_trace.py) — portable real-plant development trace CLI with role-separated persistence.
- [`../../Reproducibility Packet/scripts/utils/schema_types.py`](../../Reproducibility%20Packet/scripts/utils/schema_types.py) — co-owned schema-v1.0 carriers and strict record/step observable adapters; its Session-7 review loop is closed at same-state approval.
- [`../../Reproducibility Packet/scripts/utils/sensor_model.py`](../../Reproducibility%20Packet/scripts/utils/sensor_model.py) — Claude-owned sensor-realism model with the same-state-approved stateful per-step session and delivered-history masking.
- [`../../Reproducibility Packet/scripts/utils/online_loop.py`](../../Reproducibility%20Packet/scripts/utils/online_loop.py) — Codex-owned causal policy→plant→sensor orchestration for inserting the matched estimator/controller online.
- [`../../Reproducibility Packet/scripts/utils/metrics.py`](../../Reproducibility%20Packet/scripts/utils/metrics.py) and [`stats.py`](../../Reproducibility%20Packet/scripts/utils/stats.py) — Claude-owned evaluation core with complete `J_5s` windows, tie-safe selective metrics, validation-frozen OOD thresholds, `coverage_at_risk`, crossed pair/seed resampling, and A1 unsafe-step metrics; Codex added a paired `[T,7]` shape guard, so that narrow edited state awaits Claude owner re-review.
- [`../../Reproducibility Packet/scripts/utils/estimator.py`](../../Reproducibility%20Packet/scripts/utils/estimator.py) — Claude-owned diagnosis front with fixed startup tensors, channel-specific clocks, causal oracle onset, and W=640 synchronous features; Codex Session 10 corrected the feature to retain cosine, sine, and amplitude so phase is not discarded, and Claude owner re-review is pending.
- [`../../Reproducibility Packet/results/feasibility_spike/feasibility_spike_report.md`](../../Reproducibility%20Packet/results/feasibility_spike/feasibility_spike_report.md) — qualified-PASS report; native cable/rod selected under bounded diagnostic excitation.
- [`../../Reproducibility Packet/results/feasibility_spike_ordinary_excitation_blocked/feasibility_spike_report.md`](../../Reproducibility%20Packet/results/feasibility_spike_ordinary_excitation_blocked/feasibility_spike_report.md) — preserved torque-only BLOCK showing the selection's excitation boundary.
- [`../../Reproducibility Packet/results/bounded_burst_sensitivity/bounded_burst_report.md`](../../Reproducibility%20Packet/results/bounded_burst_sensitivity/bounded_burst_report.md) — development sensitivity record: one- and two-cycle bounded probes block; continuous mechanics pass exceeds the provisional motion-safety envelope; contact/safety role proposal remains under review.
- [`../../Reproducibility Packet/results/synchronous_detection_floor/synchronous_detection_floor_report.md`](../../Reproducibility%20Packet/results/synchronous_detection_floor/synchronous_detection_floor_report.md) — jointly approved detector-floor record: W=640, phase-invariant harmonic regression, 0.405 µε development threshold.
- [`../../Reproducibility Packet/results/synchronous_safe_probe/synchronous_safe_probe_report.md`](../../Reproducibility%20Packet/results/synchronous_safe_probe/synchronous_safe_probe_report.md) — actual-trace six-row clean coefficient-space screen; 0.05 N / 50% task torque clears 2.22× clean differential margin and all-scenario development safety, advancing only to a noisy/reference pilot rather than establishing a deployable-estimator margin.
- [`../../chats/Claude-Codex/Claim Sheet Review and Division of Labor/Summary.md`](../../chats/Claude-Codex/Claim%20Sheet%20Review%20and%20Division%20of%20Labor/Summary.md) — concluded Phase-1 review/labor summary.
- [`../../chats/Claude-Codex/Phase 2 Integration and Config Freeze/Phase 2 Integration and Config Freeze - Active.md`](../../chats/Claude-Codex/Phase%202%20Integration%20and%20Config%20Freeze/Phase%202%20Integration%20and%20Config%20Freeze%20-%20Active.md) — authoritative active interface/config thread; the coefficient-preserving estimator and safety-pairing guard await Claude owner re-review, the low-force candidate is pilot-only, and config remains explicitly unfrozen.
- [`../../chats/Claude-Codex-Human/Chat Appends/Summary.md`](../../chats/Claude-Codex-Human/Chat%20Appends/Summary.md) — concluded director coordination record for the transcript-tail failure mode and recovery rule.
- [`../../chats/Claude-Codex/Phase 0 Coordination/Summary.md`](../../chats/Claude-Codex/Phase%200%20Coordination/Summary.md) — concluded Phase-0 convergence record that feeds the Claim Sheet.
- [`../../README.md`](../../README.md) — public live-run status, Phase 2 / `In Progress`, including the append-only correction that distinguishes the clean 2.22× coefficient-space screen from a still-unmeasured deployable pilot margin.

## Structure

```text
agents/Codex/
├── Literature Foundation.md
├── Progress Reports/
│   └── Progress Report Session 8.md
├── references.md
├── README.md
├── Summary of Only Necessary Context.md
└── Session Summaries/
    ├── HumanReport1.md
    ├── HumanReport2.md
    ├── HumanReport3.md
    ├── HumanReport4.md
    ├── HumanReport5.md
    ├── HumanReport6.md
    ├── HumanReport7.md
    ├── HumanReport8.md
    ├── HumanReport9.md
    └── HumanReport10.md
```
