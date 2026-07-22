# Bounded Task / Contact / Controller Screen

**Decision:** `ADVANCE_BOUNDED_TASK_CONTACT_PROFILE_TO_MATCHED_INFORMATION_REVIEW`

This screen replaces the perpetual open-loop task with low-authority encoder feedback, makes one scheduled post-probe diagnosis and holds it, then starts a finite contact excursion under controller authority. It is a mechanics/lifecycle screen, not a C1-vs-S information or control result.

## Causal ordering and fixed development settings

- Fault/probe onset: 1.000 s.
- Held diagnosis: step 1136 (first stride after the probe).
- Contact excursion starts: 2.400 s.
- Full audit: 6.000 s = onset + 5 s.
- Nominal feedback reads only delivered `q_obs` / `qd_obs`.
- The fixed source-correct diagnosis stand-ins are mechanism instruments only.

## Selected-plane rows

| Source | Contact steps | Episodes | First contact (s) | Peak force (N) | Recovery-changed steps | A1 safety steps |
|---|---:|---:|---:|---:|---:|---:|
| actuator | 24 | 1 | 4.636 | 1.946 | 1863 | 0 |
| healthy | 24 | 1 | 4.618 | 2.125 | 0 | 0 |
| sensor | 21 | 1 | 4.856 | 1.585 | 0 | 0 |
| structure | 21 | 1 | 5.154 | 0.476 | 1864 | 0 |

## Full plane bracket

| Plane z (m) | Source | Contact steps | Episodes | Safety steps | Gate |
|---:|---|---:|---:|---:|---|
| 0.100 | actuator | 0 | 0 | 0 | BLOCK |
| 0.100 | healthy | 0 | 0 | 0 | BLOCK |
| 0.100 | sensor | 0 | 0 | 0 | BLOCK |
| 0.100 | structure | 0 | 0 | 0 | BLOCK |
| 0.125 | actuator | 0 | 0 | 0 | BLOCK |
| 0.125 | healthy | 21 | 1 | 0 | PASS |
| 0.125 | sensor | 0 | 0 | 0 | BLOCK |
| 0.125 | structure | 0 | 0 | 0 | BLOCK |
| 0.150 | actuator | 22 | 1 | 0 | PASS |
| 0.150 | healthy | 22 | 1 | 0 | PASS |
| 0.150 | sensor | 0 | 0 | 0 | BLOCK |
| 0.150 | structure | 0 | 0 | 0 | BLOCK |
| 0.175 | actuator | 23 | 1 | 0 | PASS |
| 0.175 | healthy | 24 | 1 | 0 | PASS |
| 0.175 | sensor | 21 | 1 | 0 | PASS |
| 0.175 | structure | 0 | 0 | 0 | BLOCK |
| 0.200 | actuator | 24 | 1 | 0 | PASS |
| 0.200 | healthy | 24 | 1 | 0 | PASS |
| 0.200 | sensor | 21 | 1 | 0 | PASS |
| 0.200 | structure | 21 | 1 | 0 | PASS |

## Interpretation boundary

An advancing plane means only that this bounded feedback/contact setup is safe enough to enter matched information/reference-lifecycle review. The classifier stand-ins use known development sources, so this artifact does not establish attribution, tracking recovery, a suite advantage, or a frozen configuration. The noisy held-decision information gate, validation-sized calibration, learned head/RMA, and evaluation-sized paired C1/S comparison remain open.
