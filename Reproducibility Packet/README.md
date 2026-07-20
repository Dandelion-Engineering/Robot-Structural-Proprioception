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

Checks model compilation, independent deformation-state availability, localized stiffness-fault construction, schema-facing output shapes, synchronous-feature correctness, the safe-probe decision functions, and the noisy healthy-reference pilot's causal window/reference logic.

```powershell
.\.venv\Scripts\python.exe -m pytest tests\test_feasibility_spike.py tests\test_synchronous_detection_floor.py tests\test_safe_probe_screen.py tests\test_noisy_reference_pilot.py -q
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

## Step 5 — Reproduce the original bounded-burst blocker

Replays ordinary, continuous, one-cycle, and two-cycle excitation through the selected mechanics and checks the unchanged per-sample mechanics floor plus the development safety envelope across every scenario. It preserves why the original 1.0 N bounded probes were not acceptable.

```powershell
.\.venv\Scripts\python.exe scripts\run_bounded_burst_sensitivity.py
```

Produces:

- `results/bounded_burst_sensitivity/summary.json`
- `results/bounded_burst_sensitivity/burst_sensitivity.csv`
- `results/bounded_burst_sensitivity/bounded_burst_report.md`

## Step 6 — Reproduce the synchronous detector floor

Runs the real gauge pathology stack over a 640-sample full-cycle window and measures the phase-invariant 0.8 Hz harmonic-regression floor. The injected target waveforms are detector surrogates; they do not replace the actual-mechanics screen in Step 7.

```powershell
.\.venv\Scripts\python.exe scripts\analyze_synchronous_detection_floor.py
```

Produces:

- `results/synchronous_detection_floor/summary.json`
- `results/synchronous_detection_floor/synchronous_detection_floor_report.md`

## Step 7 — Reproduce the safe-probe co-design screen

Uses the Step-6 development threshold on actual four-gauge MuJoCo fault-minus-healthy histories, checks safety across healthy, structural, actuator, and encoder cases, and identifies the lowest-force row in the focused grid that is eligible for a later pilot sweep. This is a development decision only; it does not freeze configuration or establish fault attribution.

```powershell
.\.venv\Scripts\python.exe scripts\screen_synchronous_safe_probe.py
```

Produces:

- `results/synchronous_safe_probe/summary.json`
- `results/synchronous_safe_probe/candidate_comparison.csv`
- `results/synchronous_safe_probe/synchronous_safe_probe_report.md`

## Step 8 — Reproduce the noisy healthy-reference pilot

Replaces the clean privileged fault-minus-healthy comparison with noisy deployable `ObservedRecord` data. The broad development sweep compares C1 and S over task/probe scale, W, stride, and onset-to-decision alignment using disjoint calibration and held-out sensor seeds. It deliberately preserves W=512 as an inert sub-cycle negative control.

```powershell
.\.venv\Scripts\python.exe scripts\run_noisy_reference_pilot.py
```

The broad sweep showed that the selected 0.50-task / 0.05 N candidate retained strong S-side fault signal, but eight calibration seeds did not resolve the requested 5% healthy false-alarm tail. The following separately seeded, prospective follow-up changes only calibration/evaluation sample size; it does not retune the threshold rule on the first sweep's held-out rows:

```powershell
.\.venv\Scripts\python.exe scripts\run_noisy_reference_pilot.py --output-dir results\noisy_reference_pilot_threshold_followup --task-torque-scales 0.5 --peak-loads-n 0.05 --calibration-seeds 32 --evaluation-seeds 48 --seed 5000
```

Produces the following under both `results/noisy_reference_pilot/` and `results/noisy_reference_pilot_threshold_followup/`:

- `summary.json`
- `pilot_results.csv`
- `pilot_aggregate.csv`
- `noisy_reference_pilot_report.md`

The prospective follow-up advances W=768 / stride=16 for **reference-rung implementation review only**: S's worst per-fault detection was 97.9%, prototype attribution 100%, pooled healthy false alarms 0.7% (2.1% worst alignment), while matched C1's minimum fault detection was 0%. These are pilot-development figures, not the confirmatory C1-vs-S result; W, stride, thresholds, sensor constants, and probe settings remain unfrozen.

## Step 9 — Run the plant-interface and sensor-model tests

Checks the lossless `PlantStepState` → privileged-trace interface, real MuJoCo deformation-coordinate extraction, plant/sensor fault boundary, three-torque semantics, privileged/observed leakage boundary, common-random-number substreams, suite masks, sensor-fault relational signature, thermal apparent strain, dropout/derived-velocity validity, latency causality, and deterministic persistence.

```powershell
.\.venv\Scripts\python.exe -m pytest tests\test_cable_plant.py tests\test_sensor_model.py -q
```

Produces: terminal test results.

## Step 10 — Generate a real privileged trace from the selected MuJoCo plant

Advances the selected 17-point-per-link cable plant at 500 Hz control / 10 kHz simulation, extracts the frozen 90-wide internal ball-joint log-map deformation vector, and persists every schema-B field under the isolated `plant/` role. The command uses the bounded 1.0 N, 0.8 Hz diagnostic condition that cleared the mechanics gate. Its `config_hash` is deliberately prefixed `dev-`: the shared immutable `config.json` has not been frozen, so this output is for development/integration and cannot be mistaken for confirmatory data.

```powershell
.\.venv\Scripts\python.exe scripts\make_mujoco_plant_trace.py --output-root results\mujoco_plant --run-id healthy_dev --duration-s 3 --thermal-ramp-c 5
```

Produces:

- `results/mujoco_plant/plant/healthy_dev.npz` — role-separated privileged plant payload.
- `results/mujoco_plant/plant/index.csv` — plant-role index (`run_id, schema_version, config_hash, npz_path, sha256`).

Use `--scenario structure --fault-severity 0.50` or `--scenario actuator --fault-severity 0.70` for a physical-fault development trace. Sensor faults are rejected here and must be injected only in Step 11.

## Step 11 — Apply the sensor-realism + fault-injection model

Maps the real privileged plant trace to one deployable sensor suite's observed record: encoder/IMU/current-proxy/gauge channels with additive noise, thermal apparent strain, bias, drift, hysteresis, quantization, dropout, and latency, plus optional injection of a sensor-class encoder fault into the observation path only. Channels a suite does not carry are written as `NaN` and masked off, so the suites differ only by available information.

```powershell
.\.venv\Scripts\python.exe scripts\run_sensor_model.py --plant-npz results\mujoco_plant\plant\healthy_dev.npz --suite S --run-id healthy_S --pair-id 1 --sensor-seed 7 --split dev
```

Produces:

- `results/sensor_model/observations/S/healthy_S.npz` — the observed record for suite `S`.
- `results/sensor_model/observations/S/index.csv` — the per-suite index row (`run_id, schema_version, config_hash, npz_path, sha256, split`).

Use `--suite C0` or `--suite C1` for the leaner conventional suites, and `--fault-class sensor --fault-subtype encoder_bias --fault-location 0 --fault-severity 0.05 --fault-onset 499` to inject a sensor fault at the 1.000 s sample of this 500 Hz post-integration trace.

## Step 12 — Generate the optional analytic plant fixture

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

This packet reproduces the mechanics gate, detector-floor correction, safe-probe co-design screen, and noisy healthy-reference pilot, and it connects the selected MuJoCo plant's **real persisted privileged output** to the sensor-realism model. Schema Amendment A1 is jointly in force. The causal one-step plant→sensor→policy loop and estimator front exist and are tested, but the permanent coefficient-distance reference rung, learned attribution heads, and recovery controller are not complete. The fixed two-field contact role currently records zero because collision is disabled; optional-contact pilots still require endpoint-contact extraction. The prospective pilot follow-up advances W=768 / stride=16 only for estimator-owner review; the shared immutable `config.json` remains unfrozen. The packet therefore does **not** yet implement the confirmatory experiment or the interactive verification artifact; neither a research result nor a frozen configuration may be inferred from these development sensitivities.
