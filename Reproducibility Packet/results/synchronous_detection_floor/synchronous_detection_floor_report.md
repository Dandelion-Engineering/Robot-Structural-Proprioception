# Synchronous-Detection Noise Floor at the Diagnostic Frequency

**Development sensitivity, not confirmatory and not a config change.** It characterizes the noise-equivalent strain (NES) of a lock-in detector at the 0.8 Hz probe over a W=512 sample (1.024 s) window, using the real gauge pathology stack, and compares it to the per-sample mechanics-gate floor.

## Noise-only floor (real gauge stack: thermal ramp + bias + drift + white + quant + dropout)

- Broadband RMS (what the gate screens): **17.35 microstrain** — thermal-dominated, comparable to / above the 10 microstrain gate floor.
- Broadband RMS after mean+linear detrend (no lock-in): **1.01 microstrain**.
- **Synchronous NES at f_d: 0.097 +/- 0.058 microstrain** (99.9th pct 0.306).
- Detection threshold (5 sigma above null mean): **0.389 microstrain**.
- Gate floor / synchronous NES ratio: **103x** more sensitive.
- Lock-in gain at this window: **0.63** (0.82 probe cycles in the window). W below one full probe period gives sub-unity gain; W covering >=1 cycle (>=625 samples at 0.8 Hz / 500 Hz) restores unit gain and lowers the floor further.

## Detectability of the bounded-burst differential RMS values

| Target | Injected RMS | Signal model | Lock-in amp | z over null | Detect rate |
|---|---:|---|---:|---:|---:|
| structural_1cycle | 8.18 microstrain | pure_tone | 11.89 microstrain | 202 | 100% |
| structural_1cycle | 8.18 microstrain | raised_cosine_1cycle_burst | 9.44 microstrain | 160 | 100% |
| actuator_1cycle | 7.84 microstrain | pure_tone | 11.39 microstrain | 193 | 100% |
| actuator_1cycle | 7.84 microstrain | raised_cosine_1cycle_burst | 9.04 microstrain | 153 | 100% |
| separation_1cycle | 12.33 microstrain | pure_tone | 17.91 microstrain | 305 | 100% |
| separation_1cycle | 12.33 microstrain | raised_cosine_1cycle_burst | 14.22 microstrain | 242 | 100% |

## Interpretation

The mechanics gate compares the clean differential strain RMS to a per-sample 10 microstrain floor set by the thermal cross-sensitivity coefficient. That floor is a broadband, DC-scale quantity. The differential signature, however, lives at the known probe frequency, and the deployable estimator reads a W-sample window. A synchronous (lock-in) detector at f_d rejects the low-frequency thermal ramp, DC bias, and random-walk drift, so its noise floor is far below the per-sample gate floor. Under this model the bounded one-cycle differentials that the per-sample gate marked BLOCK sit many sigma above the synchronous floor.

## Honesty boundaries

- This is a **detection** floor only; structure-vs-actuator **attribution** still requires the learned head (estimator rung 2) and is not claimed here.
- The thermal ramp imposed here is aggressive for a ~1 s window; real thermal drift is slower, making the reported NES a conservative upper bound.
- Realizing this advantage requires the estimator to include a synchronous feature keyed to the probe spectrum; that is the proposed next estimator-lane increment.
- This does not by itself clear the diagnostic for pilot: the **safety** screen (Codex) and a coherent bounded excitation are still required, and no config is frozen.
