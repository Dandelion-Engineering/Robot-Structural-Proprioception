# MuJoCo Cable/Rod Feasibility Spike

**Verdict: BLOCK.** The native cable/rod candidate does not clear the mechanics-only gate under the declared thresholds.

## What was tested

A planar two-actuator arm was built from two first-party MuJoCo cable/rod elements. Each 0.4 m aluminium-like link has a 20 mm × 4 mm rectangular section. The elbow is a positional connect constraint and the shoulder/elbow torques are applied through relative site transmissions. Four virtual gauges are derived from simulator-integrated segment orientations at 0.25 L and 0.75 L on each link; no gauge is copied from a fault label.

The structural case reduces local link-2 bending inertia over the normalized section [0.55, 0.85] to 50% at the fault onset. The actuator case reduces elbow delivered torque downstream of the unchanged command/current proxy. The encoder case adds a shoulder bias without changing the physical trajectory. All cases receive the same zero-mean 0.0 N distal diagnostic load.

MuJoCo documents the cable plugin as an inextensible 1-D continuum with decoupled bending and twist; its stiffness and inertia come from material parameters and section shape. The volumetric 3-D flex candidate also compiled, but remains available because this cable run did not clear the gate. Sources: [MuJoCo modeling guide](https://mujoco.readthedocs.io/en/latest/modeling.html#composite-objects), [first-party elasticity plugin](https://github.com/google-deepmind/mujoco/tree/main/plugin/elasticity).

## Gate measurements

| Check | Measured | Required | Result |
|---|---:|---:|---|
| Structural: max gauge RMS vs healthy | 1.92 µε | > 10.00 µε | BLOCK |
| Actuator: max gauge RMS vs healthy | 5.81 µε | > 10.00 µε | BLOCK |
| Structural vs actuator: max gauge RMS separation | 5.81 µε | > 10.00 µε | BLOCK |
| Encoder: q-observation RMS change | 0.0500 rad | ≥ 0.0400 rad | PASS |
| Encoder: physical gauge RMS change | 0 µε | ≈ 0 | PASS |
| Timestep signature error | 0.001 | ≤ 0.25 | PASS |
| Mesh signature error | 0.037 | ≤ 0.25 | PASS |
| Beam gauge relative error (max) | 0.021 | ≤ 0.10 | PASS |
| Beam tip-deflection relative error | 0.110 | ≤ 0.15 | PASS |

The credible floor is deliberately the larger of the 1 µε resolution floor and the 10 µε apparent-strain shift associated with 1 °C of uncompensated temperature change.

## Fine-model signature summary

- Structural gauge RMS (four stations): 0.03, 0.02, 0.18, 1.92 µε.
- Actuator gauge RMS (four stations): 2.83, 5.81, 4.02, 0.65 µε.
- Encoder gauge RMS (four stations): 0, 0, 0, 0 µε; the physical/gauge history remains unchanged while q1 shifts.

## Candidate decision and limits

The cable/rod path is not selected by this run because at least one mechanics gate failed. The failed measurements must be diagnosed or the volumetric-flex fallback escalated before commitment. The 3-D flex smoke probe compiled with nq=96 and 48 tetrahedral elements; it is retained only if later validation exposes a cable-specific failure.

No deformation-coordinate contract is selected by a blocked run.

This is the ordinary torque-only negative control: no distal diagnostic load is applied. A BLOCK here does not invalidate a separate diagnostic-excitation PASS.

This is not a claim that the full research hypothesis succeeds. It is only the mechanics feasibility gate. The spike uses deterministic matched excitation, one local stiffness section, one actuator severity, one encoder bias, no contact, and noise-floor comparisons rather than trained attribution. The next plant step must expose the per-step schema object and integrate the full thermal/drift/dropout sensor model before any pilot or confirmatory conclusion.

## Outputs

- `summary.json` — all parameters, measurements, gates, and candidate metadata.
- `signature_metrics.csv` — per-configuration feature/gauge RMS and peak values.
- `gauge_fault_signatures.png` — fine-model fault-minus-healthy gauge histories.
- `feature_signature_heatmap.png` — normalized conventional-plus-gauge RMS patterns.
