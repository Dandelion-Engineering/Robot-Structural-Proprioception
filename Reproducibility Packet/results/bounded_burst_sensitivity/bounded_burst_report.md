# Bounded Diagnostic-Burst Sensitivity

**Decision: NO BOUNDED CANDIDATE PASSES.** Do not freeze a diagnostic condition. Redesign the bounded probe/controller and implement the proposed safety roles before the pilot.

This is a mechanics/config sensitivity, not a research-hypothesis result and not a config freeze. It uses the already selected 17-point cable plant, fixed fault severities, and the same 10 microstrain credibility floor as the feasibility gate.

| Condition | Probe budget | Structural RMS | Actuator RMS | Structure-actuator separation | Peak angle | Peak speed | Mechanics | Safety | Overall |
|---|---:|---:|---:|---:|---:|---:|---|---|---|
| ordinary_no_tip_load | 1.250 s | 2.17 microstrain | 5.92 microstrain | 5.93 microstrain | 3.18 rad | 13.79 rad/s | BLOCK | BLOCK | BLOCK |
| continuous_gate_load | 1.250 s | 10.56 microstrain | 23.36 microstrain | 23.36 microstrain | 9.10 rad | 40.67 rad/s | PASS | BLOCK | BLOCK |
| bounded_1_cycle | 1.250 s | 8.18 microstrain | 7.84 microstrain | 12.33 microstrain | 4.53 rad | 37.74 rad/s | BLOCK | BLOCK | BLOCK |
| bounded_2_cycle | 2.500 s | 8.67 microstrain | 13.38 microstrain | 17.49 microstrain | 21.06 rad | 37.74 rad/s | BLOCK | BLOCK | BLOCK |

## Interpretation

A bounded candidate passes this screen only if structure, actuator, and their difference each exceed the unchanged gauge credibility floor, while the encoder case remains relational (encoder changes; physical gauge/IMU history does not). The shortest passing bounded candidate is preferred for the pilot because the Claim Sheet requires informative excitation to be treated as a safety budget, not as free information.

The estimator window remains a separate pilot choice: a mechanics PASS does not prove that `W=512` is optimal, and no current result promotes a development trace into confirmatory data.

## Contact and safety role proposal (not frozen)

- `contact_state` width **2**: `tip_contact_force_n`, `tip_contact_active`. The current no-contact plant writes zeros only after this role is implemented; an endpoint-contact pilot must populate both from MuJoCo contact truth.
- `safety_flag` width **7**: two joint-angle flags, two joint-speed flags, one tip-workspace flag, one absolute-gauge-strain flag, and one tip-contact-force flag. Actuator saturation stays in the schema's separate two-wide `saturation_flag`.
- Provisional screening thresholds: `|q| <= pi rad` per joint; `|qd| <= 10 rad/s` per joint; tip radius `<= 0.82 m`; `|gauge_true| <= 500 microstrain`; tip contact force `<= 5 N`. These are a review proposal, not hardware claims or frozen values.

The present sensitivity can evaluate the first six flags but not contact force, because the selected development MJCF still disables contact. A complete pilot configuration must implement the two-wide contact role and the seventh safety flag; zero-width arrays remain disallowed for pilot/confirmatory generation.
