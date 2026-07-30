"""Tests for the shared gauge-window helper lifted into ``utils`` (Claude's lane).

Protocol P section 8 pre-registers Stage 0 as reusing this helper rather than carrying a
second copy of a sensor-path driver. Two things therefore need pinning: the imposed
thermal profile both consumers share, and the fact that ``pair_id`` — promoted from a
hard-coded ``1`` to a required argument in Session 46 — actually reaches the sensor RNG
instead of being accepted and dropped.

These tests run on a clean checkout: no retained dataset, no plant, no MuJoCo.
"""

from __future__ import annotations

import dataclasses
import sys
from pathlib import Path

import numpy as np
import pytest

SCRIPTS_DIR = Path(__file__).resolve().parents[1] / "scripts"
sys.path.insert(0, str(SCRIPTS_DIR))

from utils.gauge_windows import (  # noqa: E402
    gauge_window,
    linear_thermal_profile,
)
from utils.schema_types import N_GAUGES  # noqa: E402
from utils.sensor_model import OnlineSensorSession, SensorConfig  # noqa: E402
from utils.synthetic_plant import synthetic_privileged_record  # noqa: E402

# Short windows keep these tests fast; none of them is a protocol measurement.
W = 16
F_CTRL = 500.0
CONFIG = SensorConfig()


def test_the_thermal_profile_starts_at_the_sensor_model_reference() -> None:
    """A profile that did not start at the reference would inject a step offset."""

    profile = linear_thermal_profile(W, 3.0, reference_c=CONFIG.reference_temperature_c)
    assert profile.shape == (W, N_GAUGES)
    assert np.allclose(profile[0], CONFIG.reference_temperature_c)
    assert np.allclose(profile[-1], CONFIG.reference_temperature_c + 3.0)


def test_the_thermal_profile_is_identical_across_gauges() -> None:
    """Both consumers impose the same excursion on every station."""

    profile = linear_thermal_profile(W, 2.5, reference_c=CONFIG.reference_temperature_c)
    for gauge in range(1, N_GAUGES):
        assert np.array_equal(profile[:, 0], profile[:, gauge])


def test_a_zero_ramp_is_a_flat_profile_at_the_reference() -> None:
    profile = linear_thermal_profile(W, 0.0, reference_c=CONFIG.reference_temperature_c)
    assert np.allclose(profile, CONFIG.reference_temperature_c)


def test_the_thermal_profile_uses_a_nondefault_bound_reference() -> None:
    """A duplicated 25 C constant would silently detach the profile from SensorConfig."""

    profile = linear_thermal_profile(W, 1.5, reference_c=31.25)
    assert np.allclose(profile[0], 31.25)
    assert np.allclose(profile[-1], 32.75)


@pytest.mark.parametrize(
    ("n_steps", "ramp", "reference"),
    [
        (0, 3.0, 25.0),
        (-1, 3.0, 25.0),
        (W, float("nan"), 25.0),
        (W, float("inf"), 25.0),
        (W, 3.0, float("nan")),
    ],
)
def test_the_thermal_profile_refuses_an_unusable_request(
    n_steps: int, ramp: float, reference: float
) -> None:
    with pytest.raises(ValueError):
        linear_thermal_profile(n_steps, ramp, reference_c=reference)


def test_pair_id_is_required_rather_than_defaulted() -> None:
    """The sensor RNG is keyed on pair_id, so a caller must state it.

    Before the lift it was a hard-coded ``1`` inside the helper. If it silently regained
    a default, a caller could believe it had chosen an identity it had not.
    """

    with pytest.raises(TypeError):
        gauge_window(  # type: ignore[call-arg]
            signal_true=np.zeros((W, N_GAUGES)),
            temperature_true=linear_thermal_profile(
                W, 0.0, reference_c=CONFIG.reference_temperature_c
            ),
            f_ctrl=F_CTRL,
            sensor_seed=0,
            config=SensorConfig(),
        )


def test_pair_id_actually_reaches_the_sensor_draws() -> None:
    """Unit-testing both ends of a wire does not test the wire.

    A ``pair_id`` parameter that is accepted and then ignored would leave every Stage-0
    sample drawn at the old hard-coded identity while the artifact recorded the requested
    one. This observes the value arriving at its destination: the emitted gauge values.
    """

    common = {
        "signal_true": np.zeros((W, N_GAUGES)),
        "temperature_true": linear_thermal_profile(
            W, 3.0, reference_c=CONFIG.reference_temperature_c
        ),
        "f_ctrl": F_CTRL,
        "sensor_seed": 7,
        "config": SensorConfig(),
    }
    values_one, _ = gauge_window(pair_id=1, **common)
    values_two, _ = gauge_window(pair_id=2, **common)
    assert not np.allclose(values_one, values_two)


def test_the_same_identity_reproduces_the_same_window() -> None:
    """The complement of the previous test: equal identity must give equal draws."""

    common = {
        "signal_true": np.zeros((W, N_GAUGES)),
        "temperature_true": linear_thermal_profile(
            W, 3.0, reference_c=CONFIG.reference_temperature_c
        ),
        "f_ctrl": F_CTRL,
        "sensor_seed": 7,
        "pair_id": 1,
        "config": SensorConfig(),
    }
    first_values, first_valid = gauge_window(**common)
    second_values, second_valid = gauge_window(**common)
    assert np.array_equal(first_values, second_values)
    assert np.array_equal(first_valid, second_valid)


def test_a_mismatched_temperature_shape_fails_loudly() -> None:
    with pytest.raises(ValueError, match="temperature_true"):
        gauge_window(
            signal_true=np.zeros((W, N_GAUGES)),
            temperature_true=linear_thermal_profile(
                W + 1, 3.0, reference_c=CONFIG.reference_temperature_c
            ),
            f_ctrl=F_CTRL,
            sensor_seed=0,
            pair_id=1,
            config=SensorConfig(),
        )


def test_a_wrong_gauge_count_fails_loudly() -> None:
    with pytest.raises(ValueError, match="signal_true"):
        gauge_window(
            signal_true=np.zeros((W, N_GAUGES + 1)),
            temperature_true=np.zeros((W, N_GAUGES + 1)),
            f_ctrl=F_CTRL,
            sensor_seed=0,
            pair_id=1,
            config=SensorConfig(),
        )


@pytest.mark.parametrize("f_ctrl", [0.0, -500.0, float("nan")])
def test_an_unusable_control_rate_fails_loudly(f_ctrl: float) -> None:
    with pytest.raises(ValueError, match="f_ctrl"):
        gauge_window(
            signal_true=np.zeros((W, N_GAUGES)),
            temperature_true=linear_thermal_profile(
                W, 0.0, reference_c=CONFIG.reference_temperature_c
            ),
            f_ctrl=f_ctrl,
            sensor_seed=0,
            pair_id=1,
            config=SensorConfig(),
        )


def test_the_helper_matches_the_public_observation_path_gauge_values() -> None:
    """The shortcut must stay equivalent to the production ``observe_step`` path.

    Independent channel substreams make it safe to skip unused channels, but that is a
    construction claim rather than a consequence. This test observes both paths at the
    emitted gauge values and validity rather than only testing the private helper.
    """

    signal = np.arange(W * N_GAUGES, dtype=float).reshape(W, N_GAUGES) / 10.0
    temperature = linear_thermal_profile(
        W, 3.0, reference_c=CONFIG.reference_temperature_c
    )
    direct_values, direct_valid = gauge_window(
        signal_true=signal,
        temperature_true=temperature,
        f_ctrl=F_CTRL,
        sensor_seed=7,
        pair_id=1,
        config=CONFIG,
    )

    base = synthetic_privileged_record(
        n_steps=W,
        f_ctrl=F_CTRL,
        seed=0,
        thermal_ramp_c=0.0,
    )
    session = OnlineSensorSession(
        "S",
        pair_id=1,
        sensor_seed=7,
        control_dt_s=1.0 / F_CTRL,
        config=CONFIG,
    )
    public_values = []
    public_valid = []
    for index in range(W):
        state = dataclasses.replace(
            base.slice_step(index),
            gauge_true=signal[index].copy(),
            temperature_true=temperature[index].copy(),
        )
        observed = session.observe_step(state)
        public_values.append(observed.values["gauge_obs"])
        public_valid.append(observed.valid_mask["gauge_obs"])

    assert np.array_equal(
        direct_values,
        np.asarray(public_values),
        equal_nan=True,
    )
    assert np.array_equal(direct_valid, np.asarray(public_valid))
