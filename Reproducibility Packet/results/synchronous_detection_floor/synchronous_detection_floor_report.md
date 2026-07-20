# Synchronous-Detection Noise Floor at the Diagnostic Frequency

**Development sensitivity, not confirmatory and not a config change.** It characterizes the noise-equivalent strain (NES) of a lock-in detector at the 0.8 Hz probe over a W=640 sample (1.280 s) window, using the real gauge pathology stack, and compares it to the per-sample mechanics-gate floor. The target waveforms below are detector surrogates, not replayed mechanics traces.

## Noise-only floor (real gauge stack: thermal ramp + bias + drift + white + quant + dropout)

- Broadband RMS (what the gate screens): **17.35 microstrain** — thermal-dominated, comparable to / above the 10 microstrain gate floor.
- Broadband RMS after mean+linear detrend (no lock-in): **1.01 microstrain**.
- **Synchronous NES at f_d: 0.111 +/- 0.059 microstrain** (99.9th pct 0.340).
- Detection threshold (5 sigma above null mean): **0.405 microstrain**.
- Gate floor / synchronous NES ratio: **90x** more sensitive.
- Harmonic-regression gain: **1.00**; design condition number: **4.44** (1.02 probe cycles). The joint regression is phase invariant; covering at least one cycle improves conditioning and includes the complete bounded probe.

## Detectability of the bounded-burst differential RMS values

| Target | Injected RMS | Signal model | Lock-in amp | z over null | Detect rate |
|---|---:|---|---:|---:|---:|
| structural_1cycle | 8.18 microstrain | pure_tone | 11.44 microstrain | 192 | 100% |
| structural_1cycle | 8.18 microstrain | raised_cosine_1cycle_burst | 8.69 microstrain | 146 | 100% |
| actuator_1cycle | 7.84 microstrain | pure_tone | 10.96 microstrain | 184 | 100% |
| actuator_1cycle | 7.84 microstrain | raised_cosine_1cycle_burst | 8.33 microstrain | 140 | 100% |
| separation_1cycle | 12.33 microstrain | pure_tone | 17.24 microstrain | 291 | 100% |
| separation_1cycle | 12.33 microstrain | raised_cosine_1cycle_burst | 13.10 microstrain | 221 | 100% |

## Interpretation

The mechanics gate compares the clean differential strain RMS to a per-sample 10 microstrain floor set by the thermal cross-sensitivity coefficient. That floor is a broadband, DC-scale quantity. The differential signature, however, lives at the known probe frequency, and the deployable estimator reads a W-sample window. A synchronous (lock-in) detector at f_d rejects the low-frequency thermal ramp, DC bias, and random-walk drift, so its noise floor is far below the per-sample gate floor. Under this model the bounded one-cycle differentials that the per-sample gate marked BLOCK sit many sigma above the synchronous floor in this surrogate calculation. Executable margin is owned by the separate screen that analyzes the actual mechanics traces.

## Honesty boundaries

- This is a **detection** floor only; structure-vs-actuator **attribution** still requires the learned head (estimator rung 2) and is not claimed here.
- The imposed thermal path is linear and is rejected by construction. It verifies trend rejection but does not bound nonlinear or probe-band thermal dynamics.
- Realizing this advantage requires the estimator to include a synchronous feature keyed to the probe spectrum; that is the proposed next estimator-lane increment.
- This does not by itself clear the diagnostic for pilot: the **safety** screen (Codex) and a coherent bounded excitation are still required, and no config is frozen.
