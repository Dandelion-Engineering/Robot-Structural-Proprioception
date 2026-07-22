# Matched Contact-Enabled C1/S Pilot

**Overall decision: BLOCK_MATCHED_CONTACT_PILOT_AND_CONTACT_PROFILE_CONFIG_FREEZE.**

**Short-horizon status: BLOCK_SHORT_HORIZON_PILOT.**

Both gates block. At the exact online-owned post-probe decision, S retains strong fault signal but exceeds the held-out healthy false-alarm screen. In the causal continuation, the pilot-only prototype drifts across phase and ends on an actuator call in every representative arm, including healthy and sensor. Separately, z = 0.100 m does not remain a single safe contact condition over the required onset+5 s horizon.

## Contact-conditioned information check (2.6 s)

| Suite | Healthy false alarms | Min fault detection | Structure detection | Prototype attribution |
|---|---:|---:|---:|---:|
| C1 | 4.2% | 20.8% | 20.8% | 100.0% |
| S | 8.3% | 100.0% | 100.0% | 100.0% |

References and prototype centroids use 32 calibration seeds; the held-out figures use 48 disjoint seeds. The 99th-percentile threshold is still the calibration maximum, so these are pilot figures rather than validation-frozen operating points.

S detects all three held-out fault classes and attributes their prototype shapes correctly, but its 8.3% held-out healthy false-alarm rate exceeds the predeclared 5% development screen. The short information gate blocks.

## Short causal seam check

| Source | Suite | Final call | Detection (s) | Changed-command steps | Contact episodes | Peak force (N) | Safety steps |
|---|---|---|---:|---:|---:|---:|---:|
| actuator | C1 | actuator | 2.272 | 68 | 1 | 1.078 | 0 |
| actuator | S | actuator | 2.272 | 68 | 1 | 1.078 | 0 |
| healthy | C1 | actuator | 2.304 | 36 | 1 | 1.409 | 0 |
| healthy | S | actuator | 2.304 | 36 | 1 | 1.409 | 0 |
| sensor | C1 | actuator | 2.272 | 20 | 1 | 1.409 | 0 |
| sensor | S | actuator | 2.272 | 20 | 1 | 1.409 | 0 |
| structure | C1 | actuator | 2.304 | 36 | 1 | 1.371 | 0 |
| structure | S | actuator | 2.272 | 52 | 1 | 1.371 | 0 |

The sensor fault is injected only in OnlineSensorSession and does reach the policy through delivered observations: both sensor arms call sensor at least once. That call is not stable. By the final decision every arm calls actuator, so healthy and sensor cases receive inappropriate actuator compensation. This exposes a phase/reference-lifecycle defect in using the single scheduled-decision prototype continuously; it is a BLOCK, not a controller result. The one-hot prototype confidence is not calibrated.

## Required onset+5 s horizon audit

| Plane z (m) | Source | Contact episodes | Last contact (s) | Peak force (N) | Safety steps |
|---:|---|---:|---:|---:|---:|
| 0.050 | actuator | 1 | 4.374 | 3.265 | 0 |
| 0.050 | healthy | 1 | 4.366 | 3.734 | 311 |
| 0.050 | structure | 1 | 4.362 | 3.652 | 334 |
| 0.100 | actuator | 3 | 3.458 | 3.211 | 1651 |
| 0.100 | healthy | 3 | 4.146 | 4.178 | 1111 |
| 0.100 | structure | 3 | 4.748 | 4.462 | 1658 |

The original z = 0.050 m negative control is horizon-scoped too: over six seconds it is no longer a no-contact condition. The block therefore requires a redesigned bounded task/contact profile or controller before the matched evaluation-sized comparison; it must not be repaired by retuning the A1 safety limits.

## Boundaries

- Development pilot only; no confirmatory data or research result.
- Contact height, W/stride, thresholds, sensor constants, faults, and config remain unfrozen.
- The row's 2-D tip-radius readout is not used as the workspace gate; A1 privileged safety flags remain authoritative.
- Learned attribution, RMA, per-suite probability calibration, and the evaluation-sized recovery comparison remain open.
