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

Checks model compilation, independent deformation-state availability, localized stiffness-fault construction, schema-facing output shapes, synchronous-feature and coefficient-reference correctness, the safe-probe, optional-contact-profile, matched-contact-pilot, bounded-task/contact, and bounded noisy held-decision functions, the noisy healthy-reference pilot's causal window/reference logic, the interpretable recovery-controller seam, and the linear system-ID residual baseline's role separation, suite-leakage guard, and real causal-seam integration.

```powershell
.\.venv\Scripts\python.exe -m pytest tests\test_feasibility_spike.py tests\test_synchronous_detection_floor.py tests\test_safe_probe_screen.py tests\test_optional_contact_profile.py tests\test_noisy_reference_pilot.py tests\test_matched_contact_pilot.py tests\test_bounded_task_contact.py tests\test_bounded_noisy_information_review.py tests\test_estimator.py tests\test_recovery_control.py tests\test_residual_baseline.py -q
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

## Step 9 — Reproduce the optional endpoint-contact profile screen

Screens an ascending horizontal-plane grid under the pilot-advanced 0.50-task / 0.05 N one-cycle condition. The predeclared rule selects the lowest plane above a zero-contact control that produces one brief post-onset contact episode in every canonical scenario without any A1 safety flag. The sensor scenario reuses healthy physical truth because encoder corruption is observation-side under this open-loop screen; its closed-loop contact effect remains for the later matched controller evaluation.

```powershell
.\.venv\Scripts\python.exe scripts\screen_optional_contact_profile.py
```

Produces:

- `results/optional_contact_profile_screen/summary.json`
- `results/optional_contact_profile_screen/contact_profile_grid.csv`
- `results/optional_contact_profile_screen/optional_contact_profile_report.md`

The grid advances **z = 0.100 m** to matched optional-contact pilot review: healthy/structure/sensor have 19 active steps and actuator has 23, all in one episode, with 1.08–1.41 N peak force and zero A1 safety flags. This is an open-loop development profile candidate, not a frozen height or a C1-vs-S result. The 0.498 m low-level extraction fixture remains excluded from the candidate grid.

## Step 10 — Reproduce the matched contact-enabled C1/S pilot

Applies z = 0.100 m identically to matched C1/S pairs. It fits contact-conditioned coefficient references on 32 calibration seeds, evaluates 48 disjoint held-out seeds at the exact observation window owned by the first online post-probe decision, drives one held-out pair per source through the real causal plant→sensor→estimator→controller seam, and separately audits both z = 0.100 m and the former z = 0.050 m control over the required onset+5 s horizon.

```powershell
.\.venv\Scripts\python.exe scripts\run_matched_contact_pilot.py
```

Produces:

- `results/matched_contact_enabled_pilot/summary.json`
- `results/matched_contact_enabled_pilot/contact_information_rows.csv`
- `results/matched_contact_enabled_pilot/online_seam_rows.csv`
- `results/matched_contact_enabled_pilot/extended_horizon_rows.csv`
- `results/matched_contact_enabled_pilot/matched_contact_pilot_report.md`

The recorded development decision is **BLOCK**. S retains 100% minimum per-fault detection and 100% prototype attribution at the scheduled contact-conditioned decision, but its 8.3% held-out healthy false-alarm rate exceeds the 5% screen. In the short causal continuation the single-decision prototype becomes phase/reference-unstable and every representative arm ends on an actuator call, including healthy and observation-side sensor-fault cases. Over onset+5 s, z = 0.100 m produces three contact episodes and joint-angle safety violations in every physical source scenario; z = 0.050 m also ceases to be a no-contact control. These are development blockers, not confirmatory results. The profile, W/stride, prototype, thresholds, controller settings, faults, sensor constants, and `config.json` remain unfrozen.

## Step 11 — Reproduce the bounded task/contact/controller redesign screen

Replaces the matched pilot's perpetual open-loop task torque with a low-authority controller that reads only delivered encoder position/velocity. The one-cycle probe completes first; one fixed source-correct diagnosis stand-in is then evaluated and held; only afterward does a smooth finite task excursion create contact under controller authority. The screen audits a predeclared five-plane bracket across healthy, structural, actuator, and observation-side sensor faults over the full onset+5 s horizon.

```powershell
.\.venv\Scripts\python.exe scripts\screen_bounded_task_contact.py
```

Produces:

- `results/bounded_task_contact_screen/summary.json`
- `results/bounded_task_contact_screen/bounded_task_contact_rows.csv`
- `results/bounded_task_contact_screen/bounded_task_contact_report.md`

The recorded mechanics/lifecycle screen advances **z = 0.200 m** to matched information/reference-lifecycle review. The held decision occurs at 2.272 s, the contact excursion begins at 2.400 s, and every selected-plane arm produces exactly one contact episode at 4.618–5.194 s with 0.476–2.125 N peak force and zero A1 safety steps. z = 0.100 m is the all-source no-contact control. Structural derating and actuator inverse-gain scheduling begin at the held decision and therefore precede contact; healthy and sensor arms preserve their nominal feedback command. The stand-ins use known development sources, so this is **not** an attribution, tracking-recovery, C1-vs-S, or frozen-config result.

## Step 12 — Reproduce the bounded noisy held-decision information review

Replaces the fixed source-correct mechanics stand-ins with suite-specific noisy coefficient references at the exact first causal post-probe decision. It fits detection and prototype-margin abstention separately for C1 and S on 100 calibration-only sensor seeds, evaluates 48 disjoint held-out seeds, reports false alarms, per-fault detection/attribution, known-class abstention, and recovery-action gating, then holds one predeclared held-out diagnosis through the full six-second bounded task for each source/suite. Information, action authorization, representative tracking, and A1 safety remain separate gates.

```powershell
.\.venv\Scripts\python.exe scripts\run_bounded_noisy_information_review.py
```

Produces:

- `results/bounded_noisy_information_review/summary.json`
- `results/bounded_noisy_information_review/information_rows.csv`
- `results/bounded_noisy_information_review/heldout_decision_rows.csv`
- `results/bounded_noisy_information_review/representative_online_rows.csv`
- `results/bounded_noisy_information_review/bounded_noisy_information_report.md`

The recorded decision is split: **advance the information/reference lifecycle only; block the current recovery-control profile.** S reaches 0.995 held-out four-way macro-F1 versus C1's 0.704, with 100% versus 8.3% structural recall, 100% minimum per-fault detection, and 2.1% held-out healthy false alarms. C1 and S share bit-identical pre-decision physical/shared-observation histories, and every representative six-second arm keeps one bounded contact episode with zero A1 safety steps. But the only suite-informed representative action — S correctly calling the structural fault while C1 stays healthy/no-action — worsens `J_5s` by 18.6% (1.0184 versus 0.8589 m·s), so the structural derating policy fails the control-sensitivity gate. The probabilities are one-hot mechanism instruments and the full-horizon continuation uses one held-out seed per source/suite; this is neither confirmatory evidence nor permission to freeze any setting.

## Step 13 — Run the plant-interface and sensor-model tests

Checks the lossless `PlantStepState` → privileged-trace interface, real MuJoCo deformation-coordinate and optional endpoint-contact-force extraction, the contact-profile selection rule, plant/sensor fault boundary, three-torque semantics, privileged/observed leakage boundary, common-random-number substreams, suite masks, sensor-fault relational signature, thermal apparent strain, dropout/derived-velocity validity, latency causality, and deterministic persistence.

```powershell
.\.venv\Scripts\python.exe -m pytest tests\test_cable_plant.py tests\test_optional_contact_profile.py tests\test_sensor_model.py -q
```

Produces: terminal test results.

## Step 14 — Generate a real privileged trace from the selected MuJoCo plant

Advances the selected 17-point-per-link cable plant at 500 Hz control / 10 kHz simulation, extracts the frozen 90-wide internal ball-joint log-map deformation vector, and persists every schema-B field under the isolated `plant/` role. The command uses the bounded 1.0 N, 0.8 Hz diagnostic condition that cleared the mechanics gate. Its `config_hash` is deliberately prefixed `dev-`: the shared immutable `config.json` has not been frozen, so this output is for development/integration and cannot be mistaken for confirmatory data.

```powershell
.\.venv\Scripts\python.exe scripts\make_mujoco_plant_trace.py --output-root results\mujoco_plant --run-id healthy_dev --duration-s 3 --thermal-ramp-c 5
```

For a low-level development check of the A1 endpoint-contact role, supply the original
extraction-fixture plane height. This enables only the distal endpoint-segment/plane
collision pair and records MuJoCo constraint-force truth. It is distinct from Step 9's
screened 0.100 m profile candidate and does not freeze either value:

```powershell
.\.venv\Scripts\python.exe scripts\make_mujoco_plant_trace.py --output-root results\mujoco_contact_dev --run-id contact_dev --duration-s 0.2 --endpoint-contact-plane-z-m 0.498
```

Produces:

- `results/mujoco_plant/plant/healthy_dev.npz` — role-separated privileged plant payload.
- `results/mujoco_plant/plant/index.csv` — plant-role index (`run_id, schema_version, config_hash, npz_path, sha256`).
- Optional contact command: `results/mujoco_contact_dev/plant/contact_dev.npz` and its
  adjacent `index.csv`, with the same role/index schema.

Use `--scenario structure --fault-severity 0.50` or `--scenario actuator --fault-severity 0.70` for a physical-fault development trace. Sensor faults are rejected here and must be injected only in Step 15.

## Step 15 — Apply the sensor-realism + fault-injection model

Maps the real privileged plant trace to one deployable sensor suite's observed record: encoder/IMU/current-proxy/gauge channels with additive noise, thermal apparent strain, bias, drift, hysteresis, quantization, dropout, and latency, plus optional injection of a sensor-class encoder fault into the observation path only. Channels a suite does not carry are written as `NaN` and masked off, so the suites differ only by available information.

```powershell
.\.venv\Scripts\python.exe scripts\run_sensor_model.py --plant-npz results\mujoco_plant\plant\healthy_dev.npz --suite S --run-id healthy_S --pair-id 1 --sensor-seed 7 --split dev
```

Produces:

- `results/sensor_model/observations/S/healthy_S.npz` — the observed record for suite `S`.
- `results/sensor_model/observations/S/index.csv` — the per-suite index row (`run_id, schema_version, config_hash, npz_path, sha256, split`).

Use `--suite C0` or `--suite C1` for the leaner conventional suites, and `--fault-class sensor --fault-subtype encoder_bias --fault-location 0 --fault-severity 0.05 --fault-onset 499` to inject a sensor fault at the 1.000 s sample of this 500 Hz post-integration trace.

## Step 16 — Generate the optional analytic plant fixture

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

This packet reproduces the mechanics gate, detector-floor correction, safe-probe co-design screen, noisy healthy-reference pilot, optional endpoint-contact profile screen, matched contact-enabled development pilot, bounded task/contact/controller redesign, and bounded noisy held-decision information review, and it connects the selected MuJoCo plant's **real persisted privileged output** to the sensor-realism model. Schema Amendment A1 is jointly in force. The causal one-step plant→sensor→policy loop and estimator front exist and are tested. The permanent `CoefficientReferenceDetector` uses the pilot's canonical score statistic with fail-loud reference/threshold lifecycle guards, and the jointly approved interpretable gain-scheduled recovery-controller floor plugs into the same seam; neither is a completed control result. A new `LinearResidualAttributionEstimator` supplies the Claim-Sheet-required interpretable baseline: it fits healthy deployable one-step ARX dynamics, builds four transparent residual-pattern prototypes in a separate development role, and calibrates off-prototype abstention on a third role. Its synthetic separation and real-seam checks are mechanism tests only. The learned attribution and RMA heads are still unbuilt. The fixed two-field contact role enables collision solely between the distal endpoint segment and an explicit plane, extracts MuJoCo's constraint-force truth, and drives the seventh privileged safety flag; the default model remains collision-disabled. The earlier short open-loop grid advanced z = 0.100 m to matched pilot review, but the matched pilot **blocked** it: S's contact-conditioned scheduled-decision signal came with 8.3% healthy false alarms, the pilot-only continuous prototype was phase/reference-unstable, and the selected plane produced repeated contacts plus privileged joint-angle safety violations over onset+5 s. The bounded redesign advanced z = 0.200 m as the lowest all-source mechanics/lifecycle candidate under deployable encoder feedback, one held scheduled diagnosis, a post-decision finite contact excursion, and zero A1 flags over onset+5 s. Replacing its fixed diagnoses with resolved-tail noisy references now advances the **information/reference lifecycle only**: S reaches 0.995 held-out macro-F1 and 100% structural recall versus C1's 0.704 and 8.3%, with 2.1% versus 4.2% healthy false alarms. The current recovery-control profile remains blocked because the representative suite-informed structural action worsens `J_5s` by 18.6% despite zero safety flags. Probability calibration, the recovery action itself, validation-sized multi-setting evidence, and the evaluation-sized paired control comparison remain open. The prospective non-contact noisy-reference follow-up still advances W=768 / stride=16 only as a development proposal; the shared immutable `config.json` remains unfrozen. The packet therefore does **not** yet implement the confirmatory experiment or the interactive verification artifact; neither a research result nor a frozen configuration may be inferred from these development sensitivities.
