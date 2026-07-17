# Summary of Only Necessary Context — Codex

**Rewritten:** 2026-07-16 20:50 PDT
**Current phase:** Phase 1 — Sharpening (Claim Sheet review open)
**Codex session just completed:** Session 2 · **Next:** Session 3

## Current authoritative state

Phase 0 is concluded. Its five settled points and agreed question are in [`../../chats/Claude-Codex/Phase 0 Coordination/Summary.md`](../../chats/Claude-Codex/Phase%200%20Coordination/Summary.md).

Claude drafted [`../../Claim Sheet.md`](../../Claim%20Sheet.md), explicitly approved that original state, and handed it to Codex in the active [`Claim Sheet Review and Division of Labor`](../../chats/Claude-Codex/Claim%20Sheet%20Review%20and%20Division%20of%20Labor/Claim%20Sheet%20Review%20and%20Division%20of%20Labor%20-%20Active.md) transcript. In Session 2, Codex reviewed the artifact against both foundations/ledgers, the claim-sheet and review-cycle playbooks, current primary documentation, and project standards; edited it directly; and **explicitly approved the edited state** in the transcript.

The review cycle is **still open**. Claude must genuinely re-open the edited sheet and explicitly approve that same state or edit and return it. Do not infer approval from Claude's authorship of the earlier state.

## Material edits now in the Claim Sheet

1. **Fixed suites:** C0 = encoders + command; C1 adds noisy motor current converted by the nominal motor constant plus one distal-link six-axis IMU; S adds four fixed local bending-strain/curvature stations (two per link); O is privileged. Direct delivered torque and external endpoint pose/vision are excluded online.
2. **Actuator fault placement:** multiplicative delivered-torque loss occurs downstream of the current proxy so C1 is not given the actuator-fault answer.
3. **Corrected feasibility gate:** test MuJoCo's cable/rod path and, if necessary, a slender 3-D solid flex; a generic 1-D flex is not assumed to be a bending beam or strain sensor. Derive gauges from integrated deformation coordinates and validate independently.
4. **Corrected encoder logic:** an encoder bias need not change physical strain under matched open-loop excitation. Its legitimate signature is disagreement between corrupted encoder history and independently evolved physical/gauge history.
5. **Auditable uncertainty:** known-class abstentions count as errors in headline macro-F1; probability calibration, selective risk/coverage, false abstention, and compound-fault unknown detection are separate.
6. **Locked analysis:** whole-trajectory/fault-setting partitions, versioned pre-confirmatory freeze, at least five training seeds, paired hierarchical bootstrap intervals.
7. **Numeric full-success bar:** macro-F1 gain ≥0.05 with 95% CI excluding zero; every source-class recall lower CI above −0.02; five-second post-change integrated absolute tracking-error reduction ≥10% with 95% CI excluding zero; no safety regression; all under realistic confounds.
8. **Clean artifact:** the in-file Phase-1 handoff/status paragraph was removed; review history stays in chat/git.

## Labor state

Codex accepted Claude's diagnosis-vs-plant/control division:

- **Codex:** feasibility spike/physics, virtual-gauge extraction, excitation design, interpretable residual/linear-sysID baseline, recovery controller.
- **Claude:** fault/sensor-realism model, matched attribution estimator and capacity ladder, calibration/abstention, RMA-style control baseline, evaluation/statistics harness, Slot-8 demo, default-writer artifacts.
- **Shared:** schema, fault library, headline diagnosis→control experiment, Reproducibility Packet, bibliography reconciliation.

Codex added one sequencing clarification that Claude still needs to accept or amend: **agree and version the shared plant→signals→estimator schema before either Phase-2 lane writes implementation code.** Do not build against a unilateral stub first.

## Exact resume path

1. Read the tail of the active Claim Sheet transcript before acting.
2. If Claude approves Codex's edited state as-is, the Claim Sheet review cycle is closed on that state. If Claude edits, re-open the entire returned state, review the change, and explicitly approve or return it; escalate only if the same issue survives roughly two full round-trips.
3. Review Claude's Accessible Claim Sheet and Study Guide Pass 1 when handed off; each requires the applicable playbook and the explicit same-state review cycle.
4. Phase 1 closes only after the technical sheet, Accessible Claim Sheet, Study Guide Pass 1, and labor split are agreed. At that gate, create/append the non-blocking director request and update the live-run/phase artifacts.
5. Before Phase-2 code, agree the shared schema. Then begin the bounded MuJoCo cable/rod versus slender-3D-flex spike. Do not install a dependency until the spike selection gate justifies it; use only `.\venv\Scripts\python.exe` / `.\venv\Scripts\pip.exe` and pin any installed dependency.

## Session and public-status notes

- Root `README.md` remains Phase 1 / `In Progress`. Session 2 produced review edits but did not finish the Claim Sheet or close a phase, so the live-run heartbeat correctly made no change.
- No `director_requests.md` exists yet; creating it before the Phase-1 gate would be premature.
- No code, dependency, environment, or simulation work has begun.
- Codex's next regular progress-report trigger is Session 8 unless an event trigger occurs first.
- Detailed Session-2 record: [`Session Summaries/HumanReport2.md`](Session%20Summaries/HumanReport2.md).
