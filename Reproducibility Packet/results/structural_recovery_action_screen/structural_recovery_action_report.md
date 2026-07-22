# Structural Recovery Action Development Screen

**Decision:** `BLOCK_STRUCTURAL_RECOVERY_ACTION_FAMILY`

This fixed-diagnosis sensitivity keeps the approved bounded mechanics and one-held-decision lifecycle unchanged while screening a predeclared inverse-stiffness action family. Tuning and assessment sensor seeds are disjoint. No noisy attribution or confirmatory evidence is claimed.

## Roles and gates

- Tuning seeds: [15000, 15001, 15002].
- Assessment seeds: [15100, 15101, 15102, 15103].
- Required per-seed tracking reduction: 10.0%.
- Every candidate must preserve one held decision, causal action timing, zero A1 safety incidents, zero actuator saturation, and exact pre-decision CRN matching.
- A selected action must retain the tracking gate on disjoint structural seeds, stay safe under a healthy false-authorization stress, and help structure more than healthy so a generic gain retune is not mislabeled as source-specific recovery.

## Tuning-only candidate screen

| Action | Scope | Cap | Mean reduction | Min reduction | Lifecycle | Safety | Tracking | Candidate |
|---|---|---:|---:|---:|---|---|---|---|
| current_derate_0p75 | global | 0.75 | -18.46% | -18.54% | PASS | PASS | BLOCK | BLOCK |
| no_action_1p00 | global | 1.00 | 0.00% | 0.00% | PASS | PASS | BLOCK | BLOCK |
| global_1p10 | global | 1.10 | 4.66% | 4.59% | PASS | PASS | BLOCK | BLOCK |
| global_1p25 | global | 1.25 | 8.88% | 8.80% | PASS | PASS | BLOCK | BLOCK |
| global_1p50 | global | 1.50 | 13.48% | 13.44% | PASS | PASS | PASS | PASS |
| global_2p00 | global | 2.00 | 20.37% | 20.24% | PASS | PASS | PASS | PASS |
| localized_1p25 | localized | 1.25 | 2.40% | 2.28% | PASS | PASS | BLOCK | BLOCK |
| localized_1p50 | localized | 1.50 | 4.14% | 3.99% | PASS | PASS | BLOCK | BLOCK |
| localized_2p00 | localized | 2.00 | 6.16% | 6.07% | PASS | PASS | BLOCK | BLOCK |

## Disjoint assessment

- Selected action: `global_2p00`.
- Structural mean/min reduction: 19.88% / 19.40%.
- Healthy false-authorization mean tracking reduction: 20.15%.
- Structural-minus-healthy reduction margin: -0.26 percentage points.
- Structural tracking gate: **PASS**.
- Healthy false-authorization safety gate: **PASS**.
- Source-specificity gate: **BLOCK**.

| Source | Seed | Action | J5s | Reduction | Contact episodes | Peak force (N) | Safety | Saturation |
|---|---:|---|---:|---:|---:|---:|---:|---:|
| healthy | 15100 | global_2p00 | 0.6864 | 20.19% | 2 | 3.041 | 0 | 0 |
| healthy | 15100 | no_action_1p00 | 0.8600 | 0.00% | 1 | 2.109 | 0 | 0 |
| healthy | 15101 | global_2p00 | 0.6855 | 20.32% | 2 | 3.090 | 0 | 0 |
| healthy | 15101 | no_action_1p00 | 0.8603 | 0.00% | 1 | 2.084 | 0 | 0 |
| healthy | 15102 | global_2p00 | 0.6825 | 20.69% | 2 | 3.071 | 0 | 0 |
| healthy | 15102 | no_action_1p00 | 0.8605 | 0.00% | 1 | 2.064 | 0 | 0 |
| healthy | 15103 | global_2p00 | 0.6936 | 19.39% | 1 | 3.016 | 0 | 0 |
| healthy | 15103 | no_action_1p00 | 0.8605 | 0.00% | 1 | 2.076 | 0 | 0 |
| structure | 15100 | global_2p00 | 0.6932 | 19.40% | 1 | 2.958 | 0 | 0 |
| structure | 15100 | no_action_1p00 | 0.8601 | 0.00% | 1 | 2.065 | 0 | 0 |
| structure | 15101 | global_2p00 | 0.6857 | 20.25% | 2 | 3.028 | 0 | 0 |
| structure | 15101 | no_action_1p00 | 0.8598 | 0.00% | 1 | 2.053 | 0 | 0 |
| structure | 15102 | global_2p00 | 0.6863 | 20.40% | 2 | 2.957 | 0 | 0 |
| structure | 15102 | no_action_1p00 | 0.8622 | 0.00% | 1 | 2.056 | 0 | 0 |
| structure | 15103 | global_2p00 | 0.6932 | 19.48% | 1 | 3.017 | 0 | 0 |
| structure | 15103 | no_action_1p00 | 0.8609 | 0.00% | 1 | 2.023 | 0 | 0 |

The selected global multiplier improves healthy tracking slightly more than structural-fault tracking. The screen therefore identifies generic nominal-controller under-authority, not a structural recovery mechanism. The nominal controller must be retuned first, after which the task/fault condition must expose a measurable stiffness-loss deficit before another source-specific action is screened.

## Interpretation boundary

Fixed source-correct outputs isolate a small controller mechanism screen; this is not noisy attribution, a probability-calibrated action, an evaluation-sized comparison, or permission to freeze config.
The old 0.75 derate remains the approved transparent safety floor. This screen asks only whether a bounded severity-conditioned alternative is coherent enough to enter the already-approved noisy held-decision review. The action family, multiplier, task/contact/controller values, sensor constants, fault setting, W/stride, thresholds, and config remain unfrozen.
