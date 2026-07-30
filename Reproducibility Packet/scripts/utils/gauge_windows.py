"""Drive the real gauge sensor stack over a synthetic strain/temperature window.

DEVELOPMENT / SCREEN SUPPORT. This module holds the one helper two screens share: a
way to obtain emitted gauge values for a `W`-step window of *imposed* physical strain
and temperature, without running a plant. It is not part of the confirmatory pipeline
and produces no physical claim of its own -- what it faithfully reproduces is the
sensor lane's pathology stack (hysteresis, thermal apparent strain, bias, random-walk
drift, white noise, quantization, dropout and latency), which is the object both
screens need to characterize.

Why it lives here rather than in either screen. Protocol P section 8 pre-registers the
Stage-0 sensor-only difference null as reusing "the gauge-window helper lifted into
`utils/`", and two independent copies of a sensor-path driver could agree with each
other while diverging from the production stack. The helper is therefore imported by
both consumers rather than duplicated:

  * `scripts/analyze_synchronous_detection_floor.py` -- the single-window 5-sigma
    detection threshold (development evidence, closed);
  * `scripts/analyze_synchronous_difference_null.py` -- Protocol P Stage 0, the null of
    a *difference* of two windows.

That shared import is also what makes the two measurements comparable at all: a
threshold and the signal it judges have to come from the same configuration, so the
thermal profile construction is shared here too rather than restated per script.

Provenance: `gauge_window` was written in `analyze_synchronous_detection_floor.py`
(Claude Session 12) and lifted here unchanged in Session 46 except for two things,
both disclosed because this helper now feeds a pre-registered protocol stage:

  1. `pair_id` was a hard-coded `1` and is now a required keyword argument. The sensor
     RNG is keyed on `(sensor_seed, pair_id, channel, stream)` jointly, so `pair_id` is
     half of the identity of every draw this helper makes; a caller must state it.
     Protocol P section 6 pins `pair_id = 1` for Stage 0 and the detection-floor screen
     passes `1` explicitly, so no existing measurement changes.
  2. An `assert isinstance(...)` type guard became an explicit `raise`. Protocol P
     section 10 forbids `assert` in decision-bearing code because `python -O` removes
     it. Behaviour is identical whenever the guard passes, which is every real call.
"""

from __future__ import annotations

import dataclasses

import numpy as np

from utils.schema_types import N_GAUGES, PlantStepState, observable_step_sources
from utils.sensor_model import OnlineSensorSession, SensorConfig
from utils.synthetic_plant import synthetic_privileged_record

# Reference temperature of the sensor model's thermal apparent-strain term (degrees C).
# The sensor model subtracts this reference before applying its microstrain-per-degree
# coefficient, so a profile built around it starts at zero thermal contribution.
THERMAL_REFERENCE_C = 25.0


def linear_thermal_profile(
    n_steps: int, ramp_c: float, *, n_gauges: int = N_GAUGES
) -> np.ndarray:
    """Build the per-window linear thermal profile both screens impose.

    Inputs: the window length in control steps, the total ramp in degrees C across that
    window, and the number of gauge stations. Outputs: a `[n_steps, n_gauges]` array of
    imposed temperatures rising linearly from ``THERMAL_REFERENCE_C``.

    Purpose: an aggressive linear excursion on every gauge, which is the conservative
    direction (real thermal dynamics are slower) and is a direct check that the joint
    trend/harmonic regression rejects modelled linear drift. Shared rather than
    restated so the two screens' measurements remain comparable.
    """

    if n_steps < 1:
        raise ValueError("n_steps must be at least 1")
    if not np.isfinite(ramp_c):
        raise ValueError("ramp_c must be finite")
    ramp = np.linspace(0.0, ramp_c, n_steps)[:, None] * np.ones(n_gauges)
    return THERMAL_REFERENCE_C + ramp


def gauge_window(
    *,
    signal_true: np.ndarray,
    temperature_true: np.ndarray,
    f_ctrl: float,
    sensor_seed: int,
    pair_id: int | str,
    config: SensorConfig,
) -> tuple[np.ndarray, np.ndarray]:
    """Run the real `OnlineSensorSession` gauge stack over a W-step signal/temperature.

    Inputs: `signal_true[W, N_GAUGES]`, the ideal mechanical strain injected as
    `gauge_true`; `temperature_true[W, N_GAUGES]`, the imposed thermal profile; the
    control rate in Hz; and the two fields that jointly identify every sensor draw,
    `sensor_seed` and `pair_id`. Outputs: the emitted gauge values and validity, each
    `[W, N_GAUGES]`.

    Purpose: obtain observed gauge channels for an imposed physical input with no plant
    in the loop. Calls the gauge pathology directly: its CRN substreams are independent
    of the other channels (schema A [C4]), so the gauge draws are identical to a full
    `observe_step` while skipping the unused channels.

    Raises `ValueError` on a shape or rate that cannot produce a window, and `TypeError`
    if the synthetic step state is not the expected type.
    """

    signal_true = np.asarray(signal_true, dtype=float)
    temperature_true = np.asarray(temperature_true, dtype=float)
    if signal_true.ndim != 2 or signal_true.shape[1] != N_GAUGES:
        raise ValueError(f"signal_true must be [W, {N_GAUGES}]; got {signal_true.shape}")
    if temperature_true.shape != signal_true.shape:
        raise ValueError(
            "temperature_true must match signal_true exactly; got "
            f"{temperature_true.shape} vs {signal_true.shape}"
        )
    if not np.isfinite(f_ctrl) or f_ctrl <= 0.0:
        raise ValueError("f_ctrl must be finite and positive")

    w = signal_true.shape[0]
    dt = 1.0 / f_ctrl
    base = synthetic_privileged_record(n_steps=w, f_ctrl=f_ctrl, seed=0, thermal_ramp_c=0.0)
    session = OnlineSensorSession(
        "S", pair_id=pair_id, sensor_seed=sensor_seed, control_dt_s=dt, config=config
    )
    values = np.empty((w, N_GAUGES))
    valid = np.empty((w, N_GAUGES), dtype=bool)
    for i in range(w):
        state = dataclasses.replace(
            base.slice_step(i),
            gauge_true=signal_true[i].copy(),
            temperature_true=temperature_true[i].copy(),
        )
        if not isinstance(state, PlantStepState):
            raise TypeError(f"expected a PlantStepState per step; got {type(state)!r}")
        gv, gvalid = session._gauge(observable_step_sources(state))  # noqa: SLF001 (own lane)
        values[i] = gv
        valid[i] = gvalid
    return values, valid
