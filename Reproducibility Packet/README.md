# Reproducibility Packet

This is the self-contained working packet for the Robot Structural Proprioception project. The current runnable surface reproduces the mechanics feasibility gate, emits a schema-v1.0 privileged trace from the selected MuJoCo cable plant, and turns that trace into a deployable sensor suite's noisy observations. Later pipeline stages will be added here as they become final.

## Requirements

- Python 3.12
- A 64-bit Windows, Linux, or macOS machine supported by the pinned MuJoCo wheel

The feasibility spike is CPU-only and does not require a GPU or an external dataset.

## Step 1 — Create the environment

Creates a local virtual environment and installs the exact dependency versions used for the recorded result.

```powershell
python -m venv .venv
.\.venv\Scripts\python.exe -m pip install --requirement requirements.txt
```

Produces: `.venv/` (local, ignored).

## Step 2 — Run the focused tests

Checks model compilation, independent deformation-state availability, localized stiffness-fault construction, and schema-facing output shapes.

```powershell
.\.venv\Scripts\python.exe -m pytest tests\test_feasibility_spike.py -q
```

Produces: terminal test results.

## Step 3 — Reproduce the mechanics gate

Runs healthy, localized structural-fault, actuator-gain-fault, and encoder-bias scenarios at three mesh/timestep settings; performs an independent cantilever-beam check; probes the reserve volumetric-flex candidate; and writes the gate artifacts.

```powershell
.\.venv\Scripts\python.exe scripts\run_feasibility_spike.py --output-dir results\feasibility_spike
```

Produces:

- `results/feasibility_spike/summary.json`
- `results/feasibility_spike/signature_metrics.csv`
- `results/feasibility_spike/feasibility_spike_report.md`
- `results/feasibility_spike/gauge_fault_signatures.png`
- `results/feasibility_spike/feature_signature_heatmap.png`

The command exits with code 0 only when every full-run gate passes. `--quick` is available for a smoke test, but it deliberately does not issue a PASS verdict.

## Step 4 — Reproduce the ordinary-excitation negative control

Repeats the same gate with the distal diagnostic load disabled. This condition is expected to block because its structural and actuator gauge signatures remain below the declared 10 µε credibility floor; exit code 2 is therefore the expected result, not a script failure.

```powershell
& .\.venv\Scripts\python.exe scripts\run_feasibility_spike.py --diagnostic-tip-load-peak-n 0 --output-dir results\feasibility_spike_ordinary_excitation_blocked
$ordinaryGateExit = $LASTEXITCODE
if ($ordinaryGateExit -ne 2) { throw "Expected BLOCK exit code 2; received $ordinaryGateExit." }
```

Produces the same five artifact types under `results/feasibility_spike_ordinary_excitation_blocked/`.

## Step 5 — Run the plant-interface and sensor-model tests

Checks the lossless `PlantStepState` → privileged-trace interface, real MuJoCo deformation-coordinate extraction, plant/sensor fault boundary, three-torque semantics, privileged/observed leakage boundary, common-random-number substreams, suite masks, sensor-fault relational signature, thermal apparent strain, dropout/derived-velocity validity, latency causality, and deterministic persistence.

```powershell
.\.venv\Scripts\python.exe -m pytest tests\test_cable_plant.py tests\test_sensor_model.py -q
```

Produces: terminal test results.

## Step 6 — Generate a real privileged trace from the selected MuJoCo plant

Advances the selected 17-point-per-link cable plant at 500 Hz control / 10 kHz simulation, extracts the frozen 90-wide internal ball-joint log-map deformation vector, and persists every schema-B field under the isolated `plant/` role. The command uses the bounded 1.0 N, 0.8 Hz diagnostic condition that cleared the mechanics gate. Its `config_hash` is deliberately prefixed `dev-`: the shared immutable `config.json` has not been frozen, so this output is for development/integration and cannot be mistaken for confirmatory data.

```powershell
.\.venv\Scripts\python.exe scripts\make_mujoco_plant_trace.py --output-root results\mujoco_plant --run-id healthy_dev --duration-s 3 --thermal-ramp-c 5
```

Produces:

- `results/mujoco_plant/plant/healthy_dev.npz` — role-separated privileged plant payload.
- `results/mujoco_plant/plant/index.csv` — plant-role index (`run_id, schema_version, config_hash, npz_path, sha256`).

Use `--scenario structure --fault-severity 0.50` or `--scenario actuator --fault-severity 0.70` for a physical-fault development trace. Sensor faults are rejected here and must be injected only in Step 7.

## Step 7 — Apply the sensor-realism + fault-injection model

Maps the real privileged plant trace to one deployable sensor suite's observed record: encoder/IMU/current-proxy/gauge channels with additive noise, thermal apparent strain, bias, drift, hysteresis, quantization, dropout, and latency, plus optional injection of a sensor-class encoder fault into the observation path only. Channels a suite does not carry are written as `NaN` and masked off, so the suites differ only by available information.

```powershell
.\.venv\Scripts\python.exe scripts\run_sensor_model.py --plant-npz results\mujoco_plant\plant\healthy_dev.npz --suite S --run-id healthy_S --pair-id 1 --sensor-seed 7 --split dev
```

Produces:

- `results/sensor_model/observations/S/healthy_S.npz` — the observed record for suite `S`.
- `results/sensor_model/observations/S/index.csv` — the per-suite index row (`run_id, schema_version, config_hash, npz_path, sha256, split`).

Use `--suite C0` or `--suite C1` for the leaner conventional suites, and `--fault-class sensor --fault-subtype encoder_bias --fault-location 0 --fault-severity 0.05 --fault-onset 499` to inject a sensor fault at the 1.000 s sample of this 500 Hz post-integration trace.

## Step 8 — Generate the optional analytic plant fixture

Writes a schema-conforming privileged plant record built from analytic signals. This is a **development stand-in** used to exercise the sensor model on its own; it is not integrated mechanics and makes no physical claim. The `--thermal-ramp-c` option adds a temperature rise so the gauge channel's thermal apparent-strain pathology is visible.

```powershell
.\.venv\Scripts\python.exe scripts\make_synthetic_plant_trace.py --output-npz results\synthetic_plant\healthy.npz --thermal-ramp-c 5
```

Produces: `results/synthetic_plant/healthy.npz`

## Data

No external dataset is required. The simulator generates every value used by the spike. See [`DATA.md`](DATA.md) for the data and licensing boundary.

## Dependency licenses

| Dependency | Version | License | Role |
|---|---:|---|---|
| MuJoCo | 3.10.0 | Apache-2.0 | Cable/rod and volumetric-flex dynamics |
| NumPy | 2.5.1 | BSD-3-Clause and bundled permissive notices | Numeric arrays and metrics |
| Matplotlib | 3.11.0 | PSF-based/BSD-compatible | 300-DPI figures |
| pytest | 9.1.1 | MIT | Focused tests |

All are free and commercial-use-permitting. Project-owned code and configurations are MIT-licensed; packet prose and figures are CC BY 4.0. The copy-ready attribution and exact scope statement are in [`DATA.md`](DATA.md).

## Current boundary

This packet reproduces the mechanics gate and now connects the selected MuJoCo plant's **real persisted privileged output** to the sensor-realism model. `CablePlant.advance()` is a one-control-step interface suitable for the required online loop, but Step 7 currently consumes a completed development trace in batch; the estimator/controller have not yet been inserted between steps. The shared immutable `config.json` is also not frozen. The packet therefore does **not** yet implement the online closed-loop plant→sensor→estimator→controller experiment, learned attribution, recovery control, confirmatory statistics, or the interactive verification artifact. Those capabilities must not be inferred from what runs here.
