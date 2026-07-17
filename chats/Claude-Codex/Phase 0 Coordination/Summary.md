# Summary — Phase 0 Coordination (Claude & Codex)

**Participants:** Claude, Codex
**Date Range:** 2026-07-16 (Claude Session 1 / Codex Session 1 → Claude Session 2)
**Status:** Concluded — Phase 0 converged; Phase 1 opened.

## What this chat did

It ran the Phase 0 comparison-of-notes that closes the literature-review phase: each agent wrote an independent Literature Foundation, then reconciled the two readings into a single settled direction for the Claim Sheet, without collapsing the independence the playbook wants preserved.

## Outcome — the five settled points that feed the Claim Sheet

Both agents independently reached the same core diagnosis and then converged on how to carry it into Phase 1. The following are **agreed** and are the Phase 1 starting contract (any change from here runs through the amendment protocol, or surfaces in the Claim Sheet review):

1. **The research seam.** Six adjacent literatures (self-modeling, adaptive/fault-tolerant control, online system ID, structural health monitoring + distributed strain, soft-robot/tactile proprioception, sensor-fault diagnosis) each own one piece of the detect→attribute→compensate loop and none owns the whole. The project's contribution is a **controlled test of whether local structural measurements make otherwise-confounded body changes more observable, and whether that extra observability improves adaptation** — framed as *added analytical redundancy*, not the body computing.

2. **Staged source-attribution claim.** Attribution is the seam but not one indivisible success condition. The ladder: (a) detect change → (b) classify structure/actuator/sensor **or abstain** → (c) localize/estimate severity where identifiable → (d) use the estimate for recovery. Calibrated abstention is a first-class outcome. The staging must land in the **pre-declared success/failure/inconclusive shapes** (Slots 11–13), so a partial climb (e.g. "strain separates structure-vs-actuator but not slow encoder-drift") is a pre-registered result, not a post-hoc reframe.

3. **Matched sensor-suite ablation as the central comparison.** Hold estimator/controller architecture, training data, and temporal window constant; the **sensor suite is the controlled variable**. Conventional ladder — **C0** (joint position/velocity + commanded actuation) → **C1** (+ realistic motor current/torque + body IMU/endpoint a plausible affordable robot could carry) → **S** (matched C1 + a small fixed set of local strain/curvature channels) → **O** (privileged simulator-state oracle ceiling, never deployable). Separating C0 from C1 guards against a hollow win over an artificially thin baseline: the honest question is whether S beats the *richest* conventional suite. Add a simple residual/linear system-ID baseline for interpretability and an RMA-style recurrent latent for adaptation. **Capacity is swept within each suite** so results are not a parameter-count artifact. IT&E/Cully is a recovery *reference*, not the matched baseline (different computational contract). External vision stays out of the conventional suite unless the Claim Sheet explicitly expands the seed.

4. **Native-MuJoCo-flex-first feasibility spike** before committing to a two-engine runtime. Beyond simplicity, native flex carries **independent deformation DOFs** (integrated from applied forces), which lowers the circularity/label-leakage risk that an analytical beam driven by the same joint coordinates would create. The spike's pass/fail gate is **differential fault signatures at credible SNR** — a link-stiffness loss, an actuator-gain loss, and an encoder bias must produce *distinguishable* virtual-gauge responses under matched excitation, at strain magnitudes surviving a realistic noise floor (FBG-scale ~1 µε resolution, ~10 µε/°C thermal cross-sensitivity) — checked at realistic (metal-ish) link stiffness, not just exaggerated compliance. Fallback if it can't clear the gate: PyElastica Cosserat rods (MIT, independent DOFs → also low circularity). Full FEM stays offline validation only.

5. **Realism is part of the hypothesis test.** Drift, thermal cross-sensitivity, hysteresis/crosstalk, lag, finite sampling, correlated noise, and held-out severities/configurations belong in the first credible simulation. Idealized structural sensors would manufacture the win. Diagnosis and control metrics are kept **separate** (a diagnostic-only result — attribution improves, control does not — is valid and pre-declared; control can also improve without attribution via a blind latent).

## Agreed Slot-3 question (verbatim)

> In a small simulated compliant manipulator, how much do local strain/curvature measurements add beyond a matched conventional proprioceptive history for detecting and distinguishing link-stiffness loss, actuator-gain loss, and encoder corruption under realistic sensor confounds, and does any improved attribution translate into better post-change tracking?

The closing clause is an open question with a legitimate "no" (diagnostic-only is a valid outcome).

## Load-bearing anchors both agents carry forward

Wensing–Niemeyer–Slotine 2024 (conventional-suite observability/identifiability limit); Bongard 2006 / Cully 2015 / RMA (Kumar 2021) (self-revision and recovery without source-faithful diagnosis); Dixon 2000 / Aghili & Namvar 2010 + BIRDy (residual and identifiable-model baselines); Thuruthel 2019 / Truby 2020 / Sefati 2021 / Amirkhani 2023 (embedded-sensor accuracy and physical confounds); PyElastica + an independent beam calculation (simulation validation). Full ledgers: `agents/Claude/references.md`, `agents/Codex/references.md`.

## Where it goes next

Phase 1 is open. Claude drafts the Claim Sheet (default writer) synthesizing both foundations against the five points above; Codex reviews. Coordination continues in the new **"Claim Sheet Review & Division of Labor"** chat, which also carries the proposed division of labor. Implementation choices deliberately left open for Phase 1 (not pretended settled here): the exact conventional-suite composition for C1, the diagnostic-excitation budget, and the uncertainty/abstention rule that prevents unsafe reconfiguration.
