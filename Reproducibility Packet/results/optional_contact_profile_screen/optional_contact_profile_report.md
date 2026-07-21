# Optional Endpoint-Contact Profile Screen

**Decision:** `ADVANCE_TO_MATCHED_OPTIONAL_CONTACT_PILOT_REVIEW`

The lowest eligible development plane is **z = 0.100 m**. It advances to matched optional-contact pilot review only. The height, task/probe condition, faults, thresholds, and `config.json` remain unfrozen.

## Predeclared gate

- Grid: `(0.05, 0.075, 0.1, 0.125, 0.15)` m.
- Lowest plane is a required zero-contact control: **True**.
- Each candidate scenario needs exactly one post-onset episode, at least 5 active steps, no more than 5.0% active steps, peak force below 5 N, and no A1 safety flag.
- The earlier z = 0.498 m extraction fixture is explicitly excluded from this candidate grid.

## Selected-profile scenario audit

| Scenario | Active steps | Active fraction | Episode | First contact (s) | Peak force (N) | Impulse (N s) | Safety steps |
|---|---:|---:|---:|---:|---:|---:|---:|
| healthy | 19 | 1.67% | 1 | 2.044 | 1.409 | 0.01820 | 0 |
| structure | 19 | 1.67% | 1 | 2.044 | 1.371 | 0.01872 | 0 |
| actuator | 23 | 2.02% | 1 | 1.974 | 1.078 | 0.01538 | 0 |
| sensor | 19 | 1.67% | 1 | 2.044 | 1.409 | 0.01820 | 0 |

## Boundaries

- This is an open-loop mechanics/safety screen under the pilot-advanced task/probe, not a C1-vs-S result.
- The sensor row aliases healthy physical truth because encoder corruption is injected only after the plant. Its closed-loop effect on commands/contact is still open.
- A later matched comparison must apply the same contact profile to C1 and S within each CRN pair.
- No profile, grid, threshold, severity/onset setting, or immutable config is frozen by this artifact.
