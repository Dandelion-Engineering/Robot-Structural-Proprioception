# Fault Tracking-Deficit Development Screen

**Decision:** `ADVANCE_ACTUATOR_DEFICIT_ONLY_BLOCK_STRUCTURAL_DEFICIT`

This no-recovery sensitivity keeps the approved bounded task, contact plane, observed-state controller, probe, and six-second audit fixed while sweeping only remaining structural stiffness and actuator gain. Tuning and assessment sensor seeds are disjoint.

## Roles and gate

- Tuning seeds: [16000, 16001, 16002].
- Assessment seeds: [16100, 16101, 16102, 16103].
- Claim Sheet control bar: 10.0% *reduction*, measured against the degraded arm.
- Predeclared development margin: +2.0 percentage points, applied in reduction units.
- Required per-seed reduction: 12.0%. A source-specific action that exactly restores healthy tracking converts a deficit `D` into a reduction `D / (1 + D)`, so the equivalent per-seed no-action deficit gate is 13.64%.
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
| actuator | 0.50 | 13.19% / 13.11% | BLOCK | 13.20% / 13.12% | BLOCK |
| actuator | 0.25 | 23.09% / 22.97% | PASS | 23.16% / 23.03% | PASS |
| actuator | 0.10 | 65.99% / 65.53% | PASS | 65.73% / 65.40% | PASS |

## Disjoint decision

- **Structure: BLOCK.** No tuning severity cleared the 13.6% per-seed headroom gate.
- **Actuator: ADVANCE.** Tuning selected `actuator_gain_remaining_0p25`; disjoint assessment mean/min deficit = 23.16% / 23.03%.

## Observation-side sensor control

The fixed 0.05 rad encoder-bias control keeps a healthy physical plant but corrupts the observed feedback path. Its disjoint mean/min tracking deficit is 15.69% / 15.61%; lifecycle and A1/saturation gates are PASS. It is a fixed control readout, not a selected severity candidate.

## What the recorded headroom does and does not license

- **Headroom is a ceiling, not a result.** `actuator_gain_remaining_0p25` carries a 23.16% mean / 23.03% minimum no-action deficit, so an action that restored healthy tracking exactly would score a 18.81% / 18.72% reduction — +8.72 percentage points over the 10.0% bar at the worst seed. This is the exact-restoration headroom; an action may score higher only by outperforming the healthy arm, and this screen cannot attribute that excess.
- **Performance beyond the exact-restoration ceiling is not licensed by this screen.** An action can beat that ceiling only by tracking better than the healthy arm. That excess could be fault-specific overcompensation or generic nominal-controller under-authority; no-action headroom alone cannot distinguish them. The structural action-family screen already showed why the distinction matters, so an actuator action must be compared against a healthy false-authorization arm and report the source-specific margin separately.
- **The structural block is not a weak signal; it is a strong signal with nowhere to act.** Mean peak |gauge| and mean tracking deficit move in opposite directions across the same sweep (healthy 19.2 µε; 0.75 EI → 25.0 µε / +0.11%; 0.50 EI → 38.4 µε / +0.08%; 0.25 EI → 72.4 µε / -0.89%; 0.10 EI → 152.8 µε / -2.23%; 0.05 EI → 259.7 µε / -5.00%). The strain channel grows monotonically with severity while the tracking deficit falls to zero and then turns negative, which is the diagnostic-only shape Slot 13 reserves rather than a sensing failure.
- **No-action headroom is not S-over-C1 headroom.** The contract's control quantity is the paired difference between the structural and conventional suites on the same fault, not the difference between acting and not acting. A fault class the conventional suite already detects yields no paired control win however much no-action headroom it has, so an advancing class here licenses an action screen, not a Slot-11 comparison.

## Interpretation boundary

No-recovery severity sensitivity on one bounded development task; this is not noisy attribution, action efficacy, validation-sized evidence, or permission to freeze the fault grid, task, controller, or config.
A passing deficit condition establishes only that the fault creates enough control-layer headroom for a later action screen to be meaningful. It does not show that any deployable estimator can identify the setting or that any recovery action can reclaim the deficit. All severity values, task/contact/controller settings, thresholds, W/stride, sensor constants, and config remain unfrozen.
