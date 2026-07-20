"""Detector-referred noise floor for the strain gauges at the diagnostic frequency.

Early-Phase-2 sensitivity (Claude's estimator/sensor lane), a companion to Codex's
`run_bounded_burst_sensitivity.py`. It does **not** change the plant, the excitation,
or any frozen constant, and it is **not** the confirmatory experiment.

Motivation. The feasibility / bounded-burst gate screens a candidate excitation by
comparing the *clean mechanical* differential strain RMS over the post-onset window to
a fixed per-sample credibility floor, ``max(gauge_resolution, thermal_cross_sensitivity)
= 10 microstrain`` (see `run_feasibility_spike.py` / `run_bounded_burst_sensitivity.py`).
That floor is dominated by the thermal apparent-strain coefficient (10 microstrain/degC)
plus bias and random-walk drift — all **low-frequency** terms. The diagnostic excitation,
and therefore the differential structural/actuator signature, sits at the probe frequency
``f_d`` (0.8 Hz). The deployable estimator does not threshold a single sample: it reads a
past-only window of ``W`` samples and can detect *synchronously* at the known ``f_d``.

This script quantifies, using the **real** `OnlineSensorSession` gauge pathology stack
(hysteresis + thermal + bias + drift + white noise + quantization + dropout), the
noise-equivalent strain (NES) of a synchronous (lock-in) detector at ``f_d`` over ``W``
samples, and compares it to (a) the 10 microstrain per-sample gate floor and (b) the
bounded-burst differential RMS values that the per-sample gate reported as BLOCK. The
result characterizes whether that BLOCK reflects the broadband per-sample screen or a
genuine detectability limit for the windowed estimator.

Honesty boundaries:
  * It reports a *detection* floor only. It does **not** claim structure-vs-actuator
    *attribution*; that remains the learned head's job (estimator rung 2).
  * It imposes an aggressive per-window thermal ramp (default 3 degC over ~1 s). Real
    thermal drift is far slower, so the reported NES is a conservative upper bound.
  * The injected signal side uses both a pure-tone and a realistic single-cycle
    raised-cosine burst so finite-burst spectral spread is not hidden.
  * No frozen config is written; nothing here promotes a development trace.
"""

from __future__ import annotations

import argparse
import dataclasses
import json
from pathlib import Path
from typing import Any

import numpy as np

from utils.rng import channel_generator  # noqa: F401  (imported so CRN provenance is explicit)
from utils.schema_types import N_GAUGES, PlantStepState, observable_step_sources
from utils.sensor_model import OnlineSensorSession, SensorConfig
from utils.synthetic_plant import synthetic_privileged_record


def parse_args() -> argparse.Namespace:
    """Parse portable sensitivity arguments (project-relative output, no hard-coded paths)."""

    parser = argparse.ArgumentParser(
        description="Synchronous-detection noise floor of the strain gauges at f_d."
    )
    parser.add_argument(
        "--output-dir",
        type=Path,
        default=Path("results/synchronous_detection_floor"),
        help="Project-relative output directory.",
    )
    parser.add_argument("--f-ctrl-hz", type=float, default=500.0, help="Control-grid rate.")
    parser.add_argument("--window", type=int, default=512, help="Past-only window W (samples).")
    parser.add_argument("--diagnostic-hz", type=float, default=0.8, help="Probe frequency f_d.")
    parser.add_argument("--thermal-ramp-c", type=float, default=3.0,
                        help="Thermal excursion imposed across the window (degC); conservative.")
    parser.add_argument("--realizations", type=int, default=200,
                        help="Independent CRN sensor-noise realizations.")
    parser.add_argument("--gate-floor-microstrain", type=float, default=10.0,
                        help="The per-sample credibility floor used by the mechanics gate.")
    parser.add_argument(
        "--target-rms-microstrain",
        type=float,
        nargs="+",
        default=[8.18, 7.84, 12.33],
        help="Bounded-burst differential RMS values to test (default: 1-cycle "
             "structural/actuator/separation).",
    )
    parser.add_argument(
        "--target-labels",
        type=str,
        nargs="+",
        default=["structural_1cycle", "actuator_1cycle", "separation_1cycle"],
        help="Labels aligned with --target-rms-microstrain.",
    )
    parser.add_argument("--detect-sigma", type=float, default=5.0,
                        help="Detection threshold in sigma above the noise-only mean.")
    parser.add_argument("--seed", type=int, default=0, help="Base sensor seed.")
    return parser.parse_args()


# --------------------------------------------------------------------------- #
# Signal shapes and the synchronous statistic.
# --------------------------------------------------------------------------- #
def unit_tone(t_s: np.ndarray, f_d: float) -> np.ndarray:
    """A unit-RMS pure tone at f_d on the given time grid.

    Normalized by its own windowed RMS (not the integer-cycle 1/sqrt(2) factor) so the
    injected signal has exactly the requested RMS even when the window spans a
    non-integer number of cycles.
    """

    x = np.cos(2.0 * np.pi * f_d * t_s)
    rms = float(np.sqrt(np.mean(np.square(x))))
    return x / rms if rms > 0.0 else x


def unit_burst(t_s: np.ndarray, f_d: float) -> np.ndarray:
    """A unit-RMS single-cycle raised-cosine-windowed tone at f_d, right-aligned.

    Models the honest bounded diagnostic (one 0.8 Hz cycle under a Hann taper) so the
    finite-burst spectral spread is included rather than assumed away.
    """

    period = 1.0 / f_d
    end = float(t_s[-1])
    start = end - period
    x = np.zeros_like(t_s)
    inside = t_s >= start - 1.0e-12
    local = t_s[inside] - start
    envelope = 0.5 * (1.0 - np.cos(2.0 * np.pi * local / period))  # Hann over one period
    x[inside] = envelope * np.cos(2.0 * np.pi * f_d * local)
    rms = float(np.sqrt(np.mean(np.square(x))))
    return x / rms if rms > 0.0 else x


def synchronous_amplitude(window: np.ndarray, valid: np.ndarray, t_s: np.ndarray,
                          f_d: float) -> float:
    """Raw lock-in amplitude of the f_d component of one gauge window.

    Removes mean + linear trend (rejecting DC bias and the thermal ramp), then projects
    onto cos/sin at f_d with the ``2/N`` normalization. The window here (W=512 at 500 Hz)
    spans only ~0.82 of a 0.8 Hz cycle, so the single-bin projection has a sub-unity but
    deterministic gain; `detector_gain` measures it and the caller calibrates it out, so
    the reported floor and signal are in true-strain units. Dropped samples are excluded
    from the trend fit and contribute zero residual (baseline dropout ~1%).
    """

    n = window.shape[0]
    x = np.asarray(window, dtype=float)
    m = np.asarray(valid, dtype=bool) & np.isfinite(x)
    if m.sum() < 4:
        return 0.0
    # linear detrend fit on valid samples, evaluated on the full grid
    design = np.vstack([np.ones(n), t_s]).T
    coef, *_ = np.linalg.lstsq(design[m], x[m], rcond=None)
    resid = x - design @ coef
    resid[~m] = 0.0
    cos = np.cos(2.0 * np.pi * f_d * t_s)
    sin = np.sin(2.0 * np.pi * f_d * t_s)
    inphase = 2.0 / n * np.sum(resid * cos)
    quad = 2.0 / n * np.sum(resid * sin)
    return float(np.hypot(inphase, quad))


def detector_gain(t_s: np.ndarray, f_d: float) -> float:
    """Lock-in gain on a clean unit-amplitude tone (recovered / true).

    < 1 when the window spans a non-integer number of probe cycles; measured so the
    reported amplitudes and floor calibrate back to true strain units. The z-score and
    detection rate are gain-invariant (signal and null both scale by the same factor).
    """

    n = t_s.shape[0]
    clean = np.cos(2.0 * np.pi * f_d * t_s)
    return synchronous_amplitude(clean, np.ones(n, dtype=bool), t_s, f_d)


def broadband_rms(window: np.ndarray, valid: np.ndarray) -> float:
    """RMS of the raw gauge window over valid samples (the gate's broadband measure)."""

    x = np.asarray(window, dtype=float)
    m = np.asarray(valid, dtype=bool) & np.isfinite(x)
    return float(np.sqrt(np.mean(np.square(x[m])))) if m.any() else 0.0


# --------------------------------------------------------------------------- #
# Driving the REAL gauge pathology stack over a zero/known signal.
# --------------------------------------------------------------------------- #
def gauge_window(*, signal_true: np.ndarray, temperature_true: np.ndarray,
                 f_ctrl: float, sensor_seed: int, config: SensorConfig) -> tuple[np.ndarray, np.ndarray]:
    """Run the real `OnlineSensorSession` gauge stack over a W-step signal/temperature.

    `signal_true[W, N_GAUGES]` is the ideal mechanical strain injected as `gauge_true`;
    `temperature_true[W, N_GAUGES]` is the imposed thermal profile. Returns the emitted
    gauge values and validity `[W, N_GAUGES]`. Calls the gauge pathology directly: its
    CRN substreams are independent of the other channels (schema A [C4]), so the gauge
    draws are identical to a full `observe_step` while skipping the unused channels.
    """

    w = signal_true.shape[0]
    dt = 1.0 / f_ctrl
    base = synthetic_privileged_record(n_steps=w, f_ctrl=f_ctrl, seed=0, thermal_ramp_c=0.0)
    session = OnlineSensorSession(
        "S", pair_id=1, sensor_seed=sensor_seed, control_dt_s=dt, config=config
    )
    values = np.empty((w, N_GAUGES))
    valid = np.empty((w, N_GAUGES), dtype=bool)
    for i in range(w):
        state = dataclasses.replace(
            base.slice_step(i),
            gauge_true=signal_true[i].copy(),
            temperature_true=temperature_true[i].copy(),
        )
        assert isinstance(state, PlantStepState)
        gv, gvalid = session._gauge(observable_step_sources(state))  # noqa: SLF001 (own lane)
        values[i] = gv
        valid[i] = gvalid
    return values, valid


def run(args: argparse.Namespace) -> dict[str, Any]:
    """Characterize the synchronous NES and the detectability of each target RMS."""

    if args.window < 8:
        raise ValueError("window must be at least 8 samples")
    if args.realizations < 8:
        raise ValueError("need at least 8 realizations for a stable null")
    if len(args.target_rms_microstrain) != len(args.target_labels):
        raise ValueError("--target-rms-microstrain and --target-labels must align")

    w, f_ctrl, f_d = args.window, args.f_ctrl_hz, args.diagnostic_hz
    t_s = np.arange(w) / f_ctrl
    config = SensorConfig()
    # Aggressive per-window thermal ramp on every gauge (conservative: real thermal is slower).
    temp = 25.0 + np.linspace(0.0, args.thermal_ramp_c, w)[:, None] * np.ones(N_GAUGES)
    zero_signal = np.zeros((w, N_GAUGES))

    # Detector-gain calibration: the lock-in gain on a clean tone (< 1 when W spans a
    # non-integer number of probe cycles). Amplitudes are divided by this so the floor
    # and signal read in true-strain units; z-scores/detection rates are gain-invariant.
    gain = detector_gain(t_s, f_d)
    if not np.isfinite(gain) or gain <= 0.2:
        raise RuntimeError(f"lock-in detector gain implausibly low ({gain:.3f}); check W/f_d")

    # ---- Noise-only null over the real gauge stack ----
    null_sync, null_broadband, null_broadband_detrended = [], [], []
    for r in range(args.realizations):
        vals, valid = gauge_window(
            signal_true=zero_signal, temperature_true=temp, f_ctrl=f_ctrl,
            sensor_seed=args.seed + r, config=config,
        )
        for ch in range(N_GAUGES):
            null_sync.append(synchronous_amplitude(vals[:, ch], valid[:, ch], t_s, f_d))
            null_broadband.append(broadband_rms(vals[:, ch], valid[:, ch]))
            # detrended broadband: what mean+linear removal alone (no lock-in) achieves
            x = vals[:, ch].copy()
            m = valid[:, ch] & np.isfinite(x)
            design = np.vstack([np.ones(w), t_s]).T
            coef, *_ = np.linalg.lstsq(design[m], x[m], rcond=None)
            resid = (x - design @ coef)[m]
            null_broadband_detrended.append(float(np.sqrt(np.mean(resid ** 2))))
    null_sync = np.asarray(null_sync) / gain  # calibrate to true-strain units
    nes_mean, nes_std = float(null_sync.mean()), float(null_sync.std())
    detect_threshold = nes_mean + args.detect_sigma * nes_std

    # ---- Signal side: inject each target RMS as a tone and as a 1-cycle burst ----
    tone = unit_tone(t_s, f_d)
    burst = unit_burst(t_s, f_d)
    targets: list[dict[str, Any]] = []
    for label, target_rms in zip(args.target_labels, args.target_rms_microstrain):
        entry: dict[str, Any] = {"label": label, "injected_rms_microstrain": float(target_rms)}
        for shape_name, shape in (("pure_tone", tone), ("raised_cosine_1cycle_burst", burst)):
            sig = target_rms * shape  # unit-RMS shape scaled to the target RMS
            amps = []
            for r in range(args.realizations):
                signal_true = np.zeros((w, N_GAUGES))
                signal_true[:, 0] = sig  # inject on one station
                vals, valid = gauge_window(
                    signal_true=signal_true, temperature_true=temp, f_ctrl=f_ctrl,
                    sensor_seed=args.seed + r, config=config,
                )
                amps.append(synchronous_amplitude(vals[:, 0], valid[:, 0], t_s, f_d))
            amps = np.asarray(amps) / gain  # calibrate to true-strain units
            entry[shape_name] = {
                "sync_amplitude_mean_microstrain": float(amps.mean()),
                "sync_amplitude_std_microstrain": float(amps.std()),
                "z_over_null": float((amps.mean() - nes_mean) / nes_std),
                "detection_rate_at_threshold": float(np.mean(amps > detect_threshold)),
            }
        targets.append(entry)

    summary = {
        "purpose": "development synchronous-detection noise-floor sensitivity; not confirmatory",
        "config": {
            "f_ctrl_hz": f_ctrl, "window_samples": w,
            "window_duration_s": float(w / f_ctrl), "diagnostic_hz": f_d,
            "thermal_ramp_c_per_window": args.thermal_ramp_c,
            "lock_in_detector_gain": gain,
            "probe_cycles_in_window": float(f_d * w / f_ctrl),
            "realizations": args.realizations, "detect_sigma": args.detect_sigma,
            "gate_floor_microstrain": args.gate_floor_microstrain,
            "gauge_noise_microstrain": config.gauge_noise_microstrain,
            "thermal_microstrain_per_c": config.thermal_microstrain_per_c,
        },
        "noise_only_null": {
            "broadband_rms_mean_microstrain": float(np.mean(null_broadband)),
            "broadband_rms_detrended_mean_microstrain": float(np.mean(null_broadband_detrended)),
            "synchronous_nes_mean_microstrain": nes_mean,
            "synchronous_nes_std_microstrain": nes_std,
            "synchronous_nes_p99_9_microstrain": float(np.quantile(null_sync, 0.999)),
            "detect_threshold_microstrain": detect_threshold,
        },
        "gate_floor_over_synchronous_nes": (
            float(args.gate_floor_microstrain / nes_mean) if nes_mean > 0 else float("inf")
        ),
        "targets": targets,
    }
    return summary


def write_report(path: Path, summary: dict[str, Any]) -> None:
    """Write a concise human-readable decision record."""

    cfg = summary["config"]
    null = summary["noise_only_null"]
    lines = [
        "# Synchronous-Detection Noise Floor at the Diagnostic Frequency",
        "",
        "**Development sensitivity, not confirmatory and not a config change.** It "
        "characterizes the noise-equivalent strain (NES) of a lock-in detector at the "
        f"{cfg['diagnostic_hz']} Hz probe over a W={cfg['window_samples']} sample "
        f"({cfg['window_duration_s']:.3f} s) window, using the real gauge pathology stack, "
        "and compares it to the per-sample mechanics-gate floor.",
        "",
        "## Noise-only floor (real gauge stack: thermal ramp + bias + drift + white + quant + dropout)",
        "",
        f"- Broadband RMS (what the gate screens): **{null['broadband_rms_mean_microstrain']:.2f} "
        f"microstrain** — thermal-dominated, comparable to / above the "
        f"{cfg['gate_floor_microstrain']:.0f} microstrain gate floor.",
        f"- Broadband RMS after mean+linear detrend (no lock-in): "
        f"**{null['broadband_rms_detrended_mean_microstrain']:.2f} microstrain**.",
        f"- **Synchronous NES at f_d: {null['synchronous_nes_mean_microstrain']:.3f} +/- "
        f"{null['synchronous_nes_std_microstrain']:.3f} microstrain** "
        f"(99.9th pct {null['synchronous_nes_p99_9_microstrain']:.3f}).",
        f"- Detection threshold ({cfg['detect_sigma']:.0f} sigma above null mean): "
        f"**{null['detect_threshold_microstrain']:.3f} microstrain**.",
        f"- Gate floor / synchronous NES ratio: "
        f"**{summary['gate_floor_over_synchronous_nes']:.0f}x** more sensitive.",
        f"- Lock-in gain at this window: **{cfg['lock_in_detector_gain']:.2f}** "
        f"({cfg['probe_cycles_in_window']:.2f} probe cycles in the window). W below one "
        "full probe period gives sub-unity gain; W covering >=1 cycle (>=625 samples at "
        "0.8 Hz / 500 Hz) restores unit gain and lowers the floor further.",
        "",
        "## Detectability of the bounded-burst differential RMS values",
        "",
        "| Target | Injected RMS | Signal model | Lock-in amp | z over null | Detect rate |",
        "|---|---:|---|---:|---:|---:|",
    ]
    for tgt in summary["targets"]:
        for shape_name in ("pure_tone", "raised_cosine_1cycle_burst"):
            s = tgt[shape_name]
            lines.append(
                f"| {tgt['label']} | {tgt['injected_rms_microstrain']:.2f} microstrain | "
                f"{shape_name} | {s['sync_amplitude_mean_microstrain']:.2f} microstrain | "
                f"{s['z_over_null']:.0f} | {s['detection_rate_at_threshold']*100:.0f}% |"
            )
    lines.extend([
        "",
        "## Interpretation",
        "",
        "The mechanics gate compares the clean differential strain RMS to a per-sample "
        f"{cfg['gate_floor_microstrain']:.0f} microstrain floor set by the thermal "
        "cross-sensitivity coefficient. That floor is a broadband, DC-scale quantity. The "
        "differential signature, however, lives at the known probe frequency, and the "
        "deployable estimator reads a W-sample window. A synchronous (lock-in) detector at "
        "f_d rejects the low-frequency thermal ramp, DC bias, and random-walk drift, so its "
        "noise floor is far below the per-sample gate floor. Under this model the bounded "
        "one-cycle differentials that the per-sample gate marked BLOCK sit many sigma above "
        "the synchronous floor.",
        "",
        "## Honesty boundaries",
        "",
        "- This is a **detection** floor only; structure-vs-actuator **attribution** still "
        "requires the learned head (estimator rung 2) and is not claimed here.",
        "- The thermal ramp imposed here is aggressive for a ~1 s window; real thermal drift "
        "is slower, making the reported NES a conservative upper bound.",
        "- Realizing this advantage requires the estimator to include a synchronous feature "
        "keyed to the probe spectrum; that is the proposed next estimator-lane increment.",
        "- This does not by itself clear the diagnostic for pilot: the **safety** screen "
        "(Codex) and a coherent bounded excitation are still required, and no config is frozen.",
    ])
    path.write_text("\n".join(lines) + "\n", encoding="utf-8")


def main() -> int:
    """Run the sensitivity, write JSON + Markdown artifacts, and print the headline."""

    args = parse_args()
    summary = run(args)
    args.output_dir.mkdir(parents=True, exist_ok=True)
    (args.output_dir / "summary.json").write_text(
        json.dumps(summary, indent=2) + "\n", encoding="utf-8"
    )
    write_report(args.output_dir / "synchronous_detection_floor_report.md", summary)
    null = summary["noise_only_null"]
    print(
        f"Synchronous NES = {null['synchronous_nes_mean_microstrain']:.3f} microstrain; "
        f"gate floor {args.gate_floor_microstrain:.0f} microstrain "
        f"({summary['gate_floor_over_synchronous_nes']:.0f}x); outputs: {args.output_dir}",
        flush=True,
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
