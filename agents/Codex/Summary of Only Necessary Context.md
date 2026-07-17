# Summary of Only Necessary Context — Codex

**Rewritten:** 2026-07-16 20:08 PDT
**Current phase:** Phase 0 — Literature Review (still open)

## Current state

Both independent Phase 0 foundations now exist:

- Codex: [`Literature Foundation.md`](Literature%20Foundation.md), backed by [`references.md`](references.md)
- Claude: [`../Claude/Literature Foundation.md`](../Claude/Literature%20Foundation.md), backed by [`../Claude/references.md`](../Claude/references.md)

Codex cross-reviewed Claude's latest HumanReport, foundation, and ledger after finishing its own independent survey. The comparison is now live in [`../../chats/Claude-Codex/Phase 0 Coordination/Phase 0 Coordination - Active.md`](../../chats/Claude-Codex/Phase%200%20Coordination/Phase%200%20Coordination%20-%20Active.md). **Phase 0 is not closed:** the thread awaits Claude's explicit approval or amendment of the three convergence points below.

## Convergence proposed in the active chat

1. Keep source attribution as the central seam, but stage the claim: detection → source-family classification or abstention → localization/severity where identifiable → control recovery. Do not make full attribution an all-or-nothing success condition.
2. Make the sensor-suite increment the controlled variable. Compare a matched temporal estimator/controller using a conventional history (encoders, IMU, currents/commands) with the same model plus structural channels. Use an interpretable observer/system-ID baseline, a strong recurrent latent baseline, and an oracle-fault ceiling. Treat IT&E as a recovery reference rather than the matched primary baseline.
3. Start simulation with a small two-link compliant manipulator and a **native MuJoCo flex feasibility spike**. Check whether it exposes stable, auditable strain/curvature signals; validate selected cases against an independent beam or Cosserat calculation. Add a MuJoCo-to-PyElastica/modal bridge only if native outputs are insufficient; reserve full FEM for offline validation.

Proposed smallest question: how much local strain/curvature adds beyond matched conventional proprioceptive history for distinguishing link-stiffness loss, actuator-gain loss, and encoder corruption under realistic sensor confounds, and whether improved attribution yields better post-change tracking.

## Important research bounds

- Wensing et al.'s joint-space unobservability result motivates extra sensing but does not prove strain resolves every ambiguity.
- Structural sensors must include realistic drift, thermal cross-sensitivity, hysteresis/crosstalk, finite sample rate, and held-out fault severities/configurations. Perfect sensors would bias the result.
- Allow `unknown`/abstention and report per-fault outcomes; a mixed result is legitimate.
- External vision is outside the conventional baseline unless Phase 1 explicitly expands the seed.
- No implementation or environment changes were made in Session 1; this was literature and coordination work only.

## Exact resume path

1. Read the tail of the active Phase 0 coordination chat before acting.
2. If Claude agrees on all three points, append the closing comparison note, conclude/rename the chat according to the repository workflow, and advance to Phase 1. If Claude amends a point, resolve the disagreement in the same thread first.
3. In Phase 1, use both independent foundations to draft the Claim Sheet and Accessible Claim Sheet, create Study Guide Pass 1, agree the division of labor, and make the director request only at the gate specified in Project Details.

The detailed record of Session 1 is [`Session Summaries/HumanReport1.md`](Session%20Summaries/HumanReport1.md).
