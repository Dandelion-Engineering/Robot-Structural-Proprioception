# Synchronous Safe-Probe Co-Design Screen

**Decision: ADVANCE task_0.500_probe_0.050N TO PILOT SWEEP.** It is the smallest screened force/task pair that clears the actual-trace detector margin and all four-scenario development safety checks.

Development sensitivity only: no config is frozen and no trace is confirmatory. Unlike the detector-floor surrogate, this screen measures the synchronous feature on the actual four-gauge MuJoCo fault-minus-healthy histories and checks safety across healthy, structural, actuator, and encoder cases.

Detector contract: W=640 at 500 Hz, f_d=0.8 Hz, development threshold 0.405 microstrain, required margin 2.0x.

| Candidate | Structural | Actuator | Separation | Min margin | Worst angle | Worst speed | Safety | Detector | Advance |
|---|---:|---:|---:|---:|---:|---:|---|---|---|
| task_0.400_probe_0.050N | 0.940 | 0.686 | 0.985 | 1.69x | 1.77 rad | 3.89 rad/s | PASS | BLOCK | NO |
| task_0.400_probe_0.100N | 1.719 | 1.375 | 2.059 | 3.39x | 1.54 rad | 5.29 rad/s | PASS | PASS | YES |
| task_0.400_probe_0.150N | 0.700 | 2.421 | 2.421 | 1.73x | 4.10 rad | 8.42 rad/s | BLOCK | BLOCK | NO |
| task_0.500_probe_0.050N | 1.015 | 0.898 | 1.090 | 2.22x | 1.90 rad | 3.91 rad/s | PASS | PASS | YES |
| task_0.500_probe_0.100N | 1.500 | 1.158 | 1.770 | 2.86x | 1.80 rad | 7.04 rad/s | PASS | PASS | YES |
| task_0.500_probe_0.150N | 0.626 | 1.968 | 1.968 | 1.55x | 4.68 rad | 9.91 rad/s | BLOCK | BLOCK | NO |

## Boundaries

- This is a mechanics/detector development screen, not fault attribution and not evidence that S beats C1.
- The threshold comes from the current modeled sensor path and must be frozen on validation data later; nonlinear or probe-band thermal interference remains open.
- The selected row advances only to the pilot sweep. Contact is disabled in this plant, so optional-contact cases still require endpoint-contact extraction.
- The legacy 10-microstrain per-sample gate remains preserved as the mechanics-selection record; this screen does not rewrite it.
