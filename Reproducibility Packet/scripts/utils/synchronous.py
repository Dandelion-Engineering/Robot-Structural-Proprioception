"""Synchronous harmonic features for known-frequency diagnostic probes.

The estimator and mechanics sensitivities share this implementation so a
detector threshold and a plant-side signature are measured with the same
phase-invariant statistic.  The fit includes an intercept and a linear trend;
the sinusoid is therefore estimated jointly with, rather than after, thermal-
like drift removal.
"""

from __future__ import annotations

import numpy as np


def harmonic_coefficients(
    window: np.ndarray,
    valid: np.ndarray,
    time_s: np.ndarray,
    frequency_hz: float,
) -> np.ndarray:
    """Return cosine/sine coefficients of a detrended known-frequency signal.

    Args:
        window: One scalar channel over time, shape ``[T]``.
        valid: Boolean validity mask aligned with ``window``.
        time_s: Measurement times in seconds, shape ``[T]``.
        frequency_hz: Positive probe frequency.

    Returns:
        Shape-``[2]`` array containing cosine and sine coefficients in the
        input signal's units.

    Raises:
        ValueError: If inputs are malformed, fewer than five samples are
        usable, time is not strictly increasing, or the regression is rank
        deficient.
    """

    values = np.asarray(window, dtype=float)
    mask = np.asarray(valid, dtype=bool)
    times = np.asarray(time_s, dtype=float)
    if values.ndim != 1 or mask.shape != values.shape or times.shape != values.shape:
        raise ValueError("window, valid, and time_s must be aligned one-dimensional arrays")
    if not np.isfinite(frequency_hz) or frequency_hz <= 0.0:
        raise ValueError("frequency_hz must be finite and positive")
    if not np.all(np.isfinite(times)) or (times.size > 1 and not np.all(np.diff(times) > 0.0)):
        raise ValueError("time_s must be finite and strictly increasing")

    usable = mask & np.isfinite(values)
    if np.count_nonzero(usable) < 5:
        raise ValueError("at least five finite valid samples are required")

    centered_time = times - float(np.mean(times[usable]))
    phase = 2.0 * np.pi * frequency_hz * times
    design = np.column_stack(
        [np.ones(times.size), centered_time, np.cos(phase), np.sin(phase)]
    )
    coefficients, _, rank, _ = np.linalg.lstsq(design[usable], values[usable], rcond=None)
    if rank != design.shape[1]:
        raise ValueError("harmonic regression is rank deficient for the supplied window")
    return np.asarray(coefficients[2:4], dtype=float)


def harmonic_amplitude(
    window: np.ndarray,
    valid: np.ndarray,
    time_s: np.ndarray,
    frequency_hz: float,
) -> float:
    """Return phase-invariant amplitude from ``harmonic_coefficients``."""

    coefficients = harmonic_coefficients(window, valid, time_s, frequency_hz)
    return float(np.linalg.norm(coefficients))


def harmonic_design_condition_number(time_s: np.ndarray, frequency_hz: float) -> float:
    """Return the full-window harmonic-regression design condition number."""

    times = np.asarray(time_s, dtype=float)
    if times.ndim != 1 or times.size < 5 or not np.all(np.isfinite(times)):
        raise ValueError("time_s must be a finite one-dimensional array with at least five rows")
    if times.size > 1 and not np.all(np.diff(times) > 0.0):
        raise ValueError("time_s must be strictly increasing")
    if not np.isfinite(frequency_hz) or frequency_hz <= 0.0:
        raise ValueError("frequency_hz must be finite and positive")
    centered_time = times - float(np.mean(times))
    phase = 2.0 * np.pi * frequency_hz * times
    design = np.column_stack(
        [np.ones(times.size), centered_time, np.cos(phase), np.sin(phase)]
    )
    return float(np.linalg.cond(design))
