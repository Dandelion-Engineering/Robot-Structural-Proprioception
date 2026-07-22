# Fault Tracking-Deficit Development Screen

**Decision:** `ADVANCE_ACTUATOR_DEFICIT_ONLY_BLOCK_STRUCTURAL_DEFICIT`

This no-recovery sensitivity keeps the approved bounded task, contact plane, observed-state controller, probe, and six-second audit fixed while sweeping only remaining structural stiffness and actuator gain. Tuning and assessment sensor seeds are disjoint.

## Roles and gate

- Tuning seeds: [16000, 16001, 16002].
- Assessment seeds: [16100, 16101, 16102, 16103].
- Claim Sheet control bar: 10.0%.
- Predeclared development margin: +2.0 percentage points.
- Required per-seed no-action deficit: 12.0%.
- Every row must preserve one held healthy decision, zero recovery-command changes, exact seed-paired pre-fault histories, zero A1 incidents, and zero saturation.
- The mildest passing tuning severity is selected separately per physical source; only that preselected setting may advance on disjoint assessment.

## Severity grid

| Source | Remaining fraction | Tuning mean/min deficit | Tuning gate | Assessment mean/min deficit | Assessment gate |
|---|---:|---:|---|---:|---|
| structure | 0.75 | 0.06% / 0.00% | BLOCK | 0.11% / 0.09% | BLOCK |
| structure | 0.50 | 0.07% / -0.03% | BLOCK | 0.08% / 0.06% | BLOCK |
| structure | 0.25 | -0.88% / -0.91% | BLOCK | -0.89% / -0.97% | BLOCK |
| structure | 0.10 | -2.23% / -2.30% | BLOCK | -2.23% / -2.28% | BLOCK |
| structure | 0.05 | -5.00% / -5.03% | BLOCK | -5.00% / -5.06% | BLOCK |
| actuator | 0.85 | 2.68% / 2.63% | BLOCK | 2.69% / 2.64% | BLOCK |
| actuator | 0.70 | 6.28% / 6.27% | BLOCK | 6.28% / 6.24% | BLOCK |
| actuator | 0.50 | 13.19% / 13.11% | PASS | 13.20% / 13.12% | PASS |
| actuator | 0.25 | 23.09% / 22.97% | PASS | 23.16% / 23.03% | PASS |
| actuator | 0.10 | 65.99% / 65.53% | PASS | 65.73% / 65.40% | PASS |

## Disjoint decision

- **Structure: BLOCK.** No tuning severity cleared the 12.0% per-seed headroom gate.
- **Actuator: ADVANCE.** Tuning selected `actuator_gain_remaining_0p50`; disjoint assessment mean/min deficit = 13.20% / 13.12%.

## Observation-side sensor control

The fixed 0.05 rad encoder-bias control keeps a healthy physical plant but corrupts the observed feedback path. Its disjoint mean/min tracking deficit is 15.69% / 15.61%; lifecycle and A1/saturation gates are PASS. It is a fixed control readout, not a selected severity candidate.

## Interpretation boundary

No-recovery severity sensitivity on one bounded development task; this is not noisy attribution, action efficacy, validation-sized evidence, or permission to freeze the fault grid, task, controller, or config.
A passing deficit condition establishes only that the fault creates enough control-layer headroom for a later action screen to be meaningful. It does not show that any deployable estimator can identify the setting or that any recovery action can reclaim the deficit. All severity values, task/contact/controller settings, thresholds, W/stride, sensor constants, and config remain unfrozen.
