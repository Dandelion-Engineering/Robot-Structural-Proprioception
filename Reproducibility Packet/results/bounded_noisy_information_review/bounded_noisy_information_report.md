# Bounded Noisy Held-Decision Information Review

**Decision:** `ADVANCE_INFORMATION_REFERENCE_LIFECYCLE_ONLY_BLOCK_RECOVERY_CONTROL_PROFILE`

This development review replaces fixed source-correct diagnoses with suite-specific noisy references at the exact first causal post-probe decision. Information, recovery-action gating, and the representative six-second mechanics audit are reported separately.

## Role and lifecycle contract

- Calibration seeds: 100 (14000-14099).
- Held-out seeds: 48 (14100-14147).
- Held decision: step 1136 (2.272 s), before movement at 2.400 s.
- One classification is held for the remainder of each online rollout.
- Accepted prototype calls use one-hot mechanism probabilities; calibrated probabilities and final selective/OOD thresholds remain open.

## Held-out information and action-gate results

| Suite | Macro-F1 | Healthy FA | Min fault detect | Macro correct-confident | Fault abstain | Selective accuracy | Healthy false-actionable | Information gate |
|---|---:|---:|---:|---:|---:|---:|---:|---|
| C1 | 0.704 | 0.042 | 0.083 | 0.694 | 0.000 | 1.000 | 0.042 | BLOCK |
| S | 0.995 | 0.021 | 1.000 | 1.000 | 0.000 | 1.000 | 0.021 | PASS |

## Representative full-horizon online rows

| Source | Suite | Held call | Abstain | Action gate | Contact episodes | Peak force (N) | J5s (m s) | Safety steps |
|---|---|---|---|---|---:|---:|---:|---:|
| actuator | C1 | actuator | False | correct_actionable | 1 | 2.001 | 0.8667 | 0 |
| actuator | S | actuator | False | correct_actionable | 1 | 2.001 | 0.8667 | 0 |
| healthy | C1 | healthy | False | correct_no_action | 1 | 2.128 | 0.8604 | 0 |
| healthy | S | healthy | False | correct_no_action | 1 | 2.128 | 0.8604 | 0 |
| sensor | C1 | sensor | False | correct_no_action | 1 | 1.624 | 0.9937 | 0 |
| sensor | S | sensor | False | correct_no_action | 1 | 1.624 | 0.9937 | 0 |
| structure | C1 | healthy | False | withheld_actionable_fault | 1 | 2.051 | 0.8589 | 0 |
| structure | S | structure | False | correct_actionable | 1 | 0.499 | 1.0184 | 0 |

## Separate gate verdicts

- Information gate: **PASS**.
- Held-out action gate: **PASS**.
- Representative full-horizon A1 safety: **PASS**.
- Representative control sensitivity: **BLOCK**.
- Matched C1/S pre-decision CRN histories: **PASS**.

### Representative paired tracking readout

| Source | C1 gate | S gate | C1 J5s | S J5s | S change | Suite-informed action benefit |
|---|---|---|---:|---:|---:|---|
| healthy | correct_no_action | correct_no_action | 0.8604 | 0.8604 | 0.0% | n/a |
| structure | withheld_actionable_fault | correct_actionable | 0.8589 | 1.0184 | -18.6% | no |
| actuator | correct_actionable | correct_actionable | 0.8667 | 0.8667 | 0.0% | n/a |
| sensor | correct_no_action | correct_no_action | 0.9937 | 0.9937 | 0.0% | n/a |

## Interpretation boundary

The information/reference lifecycle advances, but the current recovery-control profile remains blocked if the suite-informed action does not improve this representative outcome. This is not the confirmatory C1-vs-S result: the prototype probabilities are not calibrated, the full-horizon continuation uses one held-out seed per source/suite, no learned attribution or RMA model is present, and no paired uncertainty interval is computed for tracking or safety. The task/contact/controller profile, sensor constants, severity/onset grids, W/stride, thresholds, and config remain unfrozen.

Every calibration and held-out case also uses the same single development fault setting per class -- fixed subtype, location, severity, and onset -- so the held-out seeds vary only the sensor-noise realization and the noisy closed-loop trajectory it produces. These rates therefore measure separation under noise at one operating point, not generalization across severities, onsets, locations, or compound faults, and the whole-trajectory and whole-fault-setting split the confirmatory result requires is not exercised here. Relatedly, a zero abstention rate is not evidence that abstention works: the smallest held-out prototype margin is 0.90, so no margin threshold below that value would bind on this fault library.
