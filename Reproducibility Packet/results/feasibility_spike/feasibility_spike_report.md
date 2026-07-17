# MuJoCo Cable/Rod Feasibility Spike

**Verdict: PASS.** The native cable/rod candidate clears the mechanics-only gate under the declared thresholds.

## What was tested

A planar two-actuator arm was built from two first-party MuJoCo cable/rod elements. Each 0.4 m aluminium-like link has a 20 mm × 4 mm rectangular section. The elbow is a positional connect constraint and the shoulder/elbow torques are applied through relative site transmissions. Four virtual gauges are derived from simulator-integrated segment orientations at 0.25 L and 0.75 L on each link; no gauge is copied from a fault label.

The structural case reduces local link-2 bending inertia over the normalized section [0.55, 0.85] to 50% at the fault onset. The actuator case reduces elbow delivered torque downstream of the unchanged command/current proxy. The encoder case adds a shoulder bias without changing the physical trajectory. All cases receive the same zero-mean 1.0 N distal diagnostic load.

MuJoCo documents the cable plugin as an inextensible 1-D continuum with decoupled bending and twist; its stiffness and inertia come from material parameters and section shape. The volumetric 3-D flex candidate also compiled, but remains the higher-cost reserve because the cable path cleared the gate. Sources: [MuJoCo modeling guide](https://mujoco.readthedocs.io/en/latest/modeling.html#composite-objects), [first-party elasticity plugin](https://github.com/google-deepmind/mujoco/tree/main/plugin/elasticity).

## Gate measurements

| Check | Measured | Required | Result |
|---|---:|---:|---|
| Structural: max gauge RMS vs healthy | 10.24 µε | > 10.00 µε | PASS |
| Actuator: max gauge RMS vs healthy | 23.87 µε | > 10.00 µε | PASS |
| Structural vs actuator: max gauge RMS separation | 23.87 µε | > 10.00 µε | PASS |
| Encoder: q-observation RMS change | 0.0500 rad | ≥ 0.0400 rad | PASS |
| Encoder: physical gauge RMS change | 0 µε | ≈ 0 | PASS |
| Timestep signature error | 0.212 | ≤ 0.25 | PASS |
| Mesh signature error | 0.127 | ≤ 0.25 | PASS |
| Beam gauge relative error (max) | 0.021 | ≤ 0.10 | PASS |
| Beam tip-deflection relative error | 0.110 | ≤ 0.15 | PASS |

The credible floor is deliberately the larger of the 1 µε resolution floor and the 10 µε apparent-strain shift associated with 1 °C of uncompensated temperature change.

## Fine-model signature summary

- Structural gauge RMS (four stations): 0.28, 0.16, 0.94, 10.24 µε.
- Actuator gauge RMS (four stations): 21.19, 23.87, 11.94, 11.11 µε.
- Encoder gauge RMS (four stations): 0, 0, 0, 0 µε; the physical/gauge history remains unchanged while q1 shifts.

## Candidate decision and limits

The cable/rod path is selected for the next plant implementation. It has independent integrated deformation coordinates, clears the conservative signal floor, agrees with the independent beam calculation, and is materially smaller than the reserve volumetric flex. The 3-D flex smoke probe compiled with nq=96 and 48 tetrahedral elements; it is retained only if later validation exposes a cable-specific failure.

The selected fine plant exposes `n_def=90` deformation coordinates: three-component log-map rotation vectors for the 15 internal cable ball joints on each link, excluding the shoulder and elbow rigid-joint coordinates. Gauge stations remain fixed at normalized positions 0.25 and 0.75 on each link.

This decision is excitation-conditional: this report includes the matched zero-mean 1.0 N distal diagnostic load. The ordinary torque-only condition is a separate negative control and does not inherit this PASS.

This is not a claim that the full research hypothesis succeeds. It is only the mechanics feasibility gate. The spike uses deterministic matched excitation, one local stiffness section, one actuator severity, one encoder bias, no contact, and noise-floor comparisons rather than trained attribution. The next plant step must expose the per-step schema object and integrate the full thermal/drift/dropout sensor model before any pilot or confirmatory conclusion.

## Outputs

- `summary.json` — all parameters, measurements, gates, and candidate metadata.
- `signature_metrics.csv` — per-configuration feature/gauge RMS and peak values.
- `gauge_fault_signatures.png` — fine-model fault-minus-healthy gauge histories.
- `feature_signature_heatmap.png` — normalized conventional-plus-gauge RMS patterns.
