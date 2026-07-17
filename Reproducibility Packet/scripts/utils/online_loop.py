"""Causal plant-to-sensor-to-policy rollout orchestration.

The schema requires online interleaving: a controller chooses the next command from
observations available at the current decision time, the plant advances one control
step, and the sensor path emits the resulting observation. This module supplies that
minimal loop without choosing the estimator or recovery policy; those are injected as
a callback and can therefore be held identical across C0/C1/S.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Callable

import numpy as np

from utils.cable_plant import CablePlant
from utils.schema_types import N_JOINTS, ObservedRecord, PrivilegedRecord
from utils.sensor_model import OnlineSensorSession


CommandPolicy = Callable[[int, float, ObservedRecord | None], np.ndarray]
ReferenceFunction = Callable[[float], np.ndarray]
TemperatureFunction = Callable[[int, float], float | np.ndarray]


@dataclass(frozen=True)
class OnlineRolloutResult:
    """Role-separated traces produced by one online plant/sensor rollout."""

    plant: PrivilegedRecord
    observations: ObservedRecord


def run_online_rollout(
    plant: CablePlant,
    sensors: OnlineSensorSession,
    *,
    n_steps: int,
    history_steps: int,
    command_policy: CommandPolicy,
    reference_fn: ReferenceFunction | None = None,
    temperature_fn: TemperatureFunction | None = None,
) -> OnlineRolloutResult:
    """Run one causal rollout with controller decisions before each plant step.

    At decision step ``k`` the policy receives at most ``history_steps`` observations
    whose per-channel availability time is no later than the current plant time. The
    explicit bounded window becomes the frozen estimator `W` and prevents quadratic
    history rebuilding. The policy returns the command applied during step ``k``. The
    newly measured observation is emitted only after the plant advances, so neither a
    future sample nor an undelivered latent channel can reach the policy.
    """

    if n_steps <= 0:
        raise ValueError("n_steps must be positive")
    if history_steps <= 0:
        raise ValueError("history_steps must be positive")
    states = []
    for step_index in range(n_steps):
        decision_time_s = float(plant.data.time)
        available = sensors.available_record(
            decision_time_s, history_steps=history_steps
        )
        command = np.asarray(
            command_policy(step_index, decision_time_s, available), dtype=float
        )
        if command.shape != (N_JOINTS,) or not np.all(np.isfinite(command)):
            raise ValueError(
                f"command_policy must return a finite shape-{(N_JOINTS,)} vector"
            )
        reference = reference_fn(decision_time_s) if reference_fn else None
        temperature = (
            temperature_fn(step_index, decision_time_s) if temperature_fn else 25.0
        )
        state = plant.advance(
            command,
            task_reference=reference,
            temperature_c=temperature,
        )
        sensors.observe_step(state)
        states.append(state)
    return OnlineRolloutResult(
        plant=PrivilegedRecord.from_steps(states),
        observations=sensors.to_record(),
    )
