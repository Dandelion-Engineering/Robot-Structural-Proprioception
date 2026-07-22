"""Deployable bounded-task feedback and diagnosis-conditioned policy composition.

The original development task used an open-loop multi-sine torque indefinitely. That
was useful for early mechanics screens but drifted beyond the joint-angle envelope over
the Claim Sheet's onset-plus-five-second horizon. This module supplies a deliberately
small replacement: a smooth finite joint-reference excursion tracked from delivered
``q_obs``/``qd_obs`` only, plus a composition adapter that applies the existing
diagnosis-conditioned recovery controller to that nominal task command.

All defaults are development proposals. The task controller never reads privileged
plant state, contact truth, labels, or another suite's channels.
"""

from __future__ import annotations

import math
from dataclasses import dataclass

import numpy as np

from utils.estimator import DiagnosisEstimator, EstimatorCommandPolicy, EstimatorTrace
from utils.recovery_control import GainScheduledRecoveryController
from utils.schema_types import N_JOINTS, ObservedRecord


@dataclass(frozen=True)
class BoundedTaskProfile:
    """Smooth finite joint-reference excursion used by the development screen."""

    target_joint_rad: tuple[float, float] = (0.30, 0.30)
    movement_start_s: float = 2.40
    transition_s: float = 0.60
    hold_end_s: float = 4.40
    return_end_s: float = 5.00
    link_length_m: float = 0.40

    def validate(self) -> None:
        """Fail loudly when the reference timing or geometry is ambiguous."""

        target = np.asarray(self.target_joint_rad, dtype=float)
        if target.shape != (N_JOINTS,) or not np.all(np.isfinite(target)):
            raise ValueError(
                f"target_joint_rad must contain {N_JOINTS} finite values"
            )
        finite_positive = {
            "movement_start_s": self.movement_start_s,
            "transition_s": self.transition_s,
            "hold_end_s": self.hold_end_s,
            "return_end_s": self.return_end_s,
            "link_length_m": self.link_length_m,
        }
        for name, value in finite_positive.items():
            if not np.isfinite(value) or value <= 0.0:
                raise ValueError(f"{name} must be finite and positive")
        arrival_s = self.movement_start_s + self.transition_s
        departure_s = self.return_end_s - self.transition_s
        if arrival_s > self.hold_end_s:
            raise ValueError("movement transition must finish before hold_end_s")
        if departure_s < self.hold_end_s:
            raise ValueError("return transition must start at or after hold_end_s")

    @staticmethod
    def _smoothstep(fraction: float) -> float:
        """Return a clipped cubic smoothstep in ``[0, 1]``."""

        x = float(np.clip(fraction, 0.0, 1.0))
        return x * x * (3.0 - 2.0 * x)

    def joint_reference(self, time_s: float) -> np.ndarray:
        """Return the finite two-joint reference at one decision time."""

        self.validate()
        if not np.isfinite(time_s) or time_s < 0.0:
            raise ValueError("time_s must be finite and non-negative")
        target = np.asarray(self.target_joint_rad, dtype=float)
        arrival_s = self.movement_start_s + self.transition_s
        departure_s = self.return_end_s - self.transition_s
        if time_s < self.movement_start_s or time_s >= self.return_end_s:
            scale = 0.0
        elif time_s < arrival_s:
            scale = self._smoothstep(
                (time_s - self.movement_start_s) / self.transition_s
            )
        elif time_s <= departure_s:
            scale = 1.0
        else:
            scale = 1.0 - self._smoothstep(
                (time_s - departure_s) / self.transition_s
            )
        return scale * target

    def task_reference(self, time_s: float) -> np.ndarray:
        """Map the joint reference to an ideal planar two-link endpoint reference."""

        q0, q1 = self.joint_reference(time_s)
        absolute_q1 = q0 + q1
        length = self.link_length_m
        return np.array(
            [
                length * (math.cos(q0) + math.cos(absolute_q1)),
                -length * (math.sin(q0) + math.sin(absolute_q1)),
            ],
            dtype=float,
        )


@dataclass(frozen=True)
class ObservedJointControllerConfig:
    """Low-authority PD gains and torque limits for the bounded task floor."""

    proportional_gain: tuple[float, float] = (0.05, 0.03)
    derivative_gain: tuple[float, float] = (0.005, 0.003)
    torque_abs_limit: tuple[float, float] = (0.20, 0.10)

    def validate(self) -> None:
        """Fail loudly when gains or limits are non-physical."""

        for name, values, allow_zero in (
            ("proportional_gain", self.proportional_gain, True),
            ("derivative_gain", self.derivative_gain, True),
            ("torque_abs_limit", self.torque_abs_limit, False),
        ):
            array = np.asarray(values, dtype=float)
            if array.shape != (N_JOINTS,) or not np.all(np.isfinite(array)):
                raise ValueError(f"{name} must contain {N_JOINTS} finite values")
            if np.any(array < 0.0) or (not allow_zero and np.any(array == 0.0)):
                qualifier = "non-negative" if allow_zero else "positive"
                raise ValueError(f"{name} values must be {qualifier}")


class ObservedJointPDController:
    """Track a bounded reference using delivered encoder position/velocity only."""

    def __init__(
        self,
        profile: BoundedTaskProfile | None = None,
        config: ObservedJointControllerConfig | None = None,
    ) -> None:
        """Validate and retain the development task profile and feedback gains."""

        self.profile = profile or BoundedTaskProfile()
        self.config = config or ObservedJointControllerConfig()
        self.profile.validate()
        self.config.validate()
        self.reset()

    def reset(self) -> None:
        """Reset zero-order-held encoder estimates for a fresh rollout."""

        self._q_obs = np.zeros(N_JOINTS, dtype=float)
        self._qd_obs = np.zeros(N_JOINTS, dtype=float)

    @staticmethod
    def _update_from_channel(
        record: ObservedRecord, channel: str, held: np.ndarray
    ) -> None:
        """Update each held joint from its newest delivered valid sample."""

        values = np.asarray(record.values[channel], dtype=float)
        valid = np.asarray(record.valid_mask[channel], dtype=bool)
        if values.shape != valid.shape or values.ndim != 2 or values.shape[1] != N_JOINTS:
            raise ValueError(f"{channel} must have matching [T,{N_JOINTS}] values/mask")
        for joint in range(N_JOINTS):
            indices = np.flatnonzero(valid[:, joint])
            if indices.size:
                value = float(values[indices[-1], joint])
                if not np.isfinite(value):
                    raise ValueError(f"valid {channel} samples must be finite")
                held[joint] = value

    def __call__(
        self,
        step_index: int,
        decision_time_s: float,
        available: ObservedRecord | None,
    ) -> np.ndarray:
        """Return one bounded deployable feedback command."""

        if step_index < 0:
            raise ValueError("step_index must be non-negative")
        if not np.isfinite(decision_time_s) or decision_time_s < 0.0:
            raise ValueError("decision_time_s must be finite and non-negative")
        if available is not None:
            self._update_from_channel(available, "q_obs", self._q_obs)
            self._update_from_channel(available, "qd_obs", self._qd_obs)
        q_reference = self.profile.joint_reference(decision_time_s)
        kp = np.asarray(self.config.proportional_gain, dtype=float)
        kd = np.asarray(self.config.derivative_gain, dtype=float)
        limits = np.asarray(self.config.torque_abs_limit, dtype=float)
        command = kp * (q_reference - self._q_obs) - kd * self._qd_obs
        bounded = np.clip(command, -limits, limits)
        if bounded.shape != (N_JOINTS,) or not np.all(np.isfinite(bounded)):
            raise RuntimeError("bounded task controller produced an invalid command")
        return bounded


class EstimatorRecoveryTaskPolicy:
    """Compose deployable task feedback, estimator cadence, and recovery action."""

    def __init__(
        self,
        task_controller: ObservedJointPDController,
        estimator: DiagnosisEstimator,
        *,
        suite: str,
        run_id: str,
        stride: int,
        recovery_controller: GainScheduledRecoveryController | None = None,
    ) -> None:
        """Bind the three matched controller layers for one online rollout."""

        self.task_controller = task_controller
        self.recovery_controller = (
            recovery_controller or GainScheduledRecoveryController()
        )
        self.task_controller.reset()
        self._current_nominal: np.ndarray | None = None
        self._diagnosis_policy = EstimatorCommandPolicy(
            estimator,
            suite=suite,
            run_id=run_id,
            stride=stride,
            recovery_command=self._recover,
        )
        self.nominal_commands: list[np.ndarray] = []
        self.commands: list[np.ndarray] = []

    @property
    def trace(self) -> EstimatorTrace:
        """Expose the schema-section-D estimator trace from the inner policy."""

        return self._diagnosis_policy.trace

    def _recover(self, output, _step_index: int, _decision_time_s: float) -> np.ndarray:
        """Apply recovery to the nominal command computed from the same observation."""

        if self._current_nominal is None:
            raise RuntimeError("task command must be computed before recovery")
        return self.recovery_controller.command_from_nominal(
            output, self._current_nominal
        )

    def __call__(
        self,
        step_index: int,
        decision_time_s: float,
        available: ObservedRecord | None,
    ) -> np.ndarray:
        """Return one task-plus-recovery command through the existing causal seam."""

        nominal = np.asarray(
            self.task_controller(step_index, decision_time_s, available), dtype=float
        )
        if nominal.shape != (N_JOINTS,) or not np.all(np.isfinite(nominal)):
            raise ValueError("task_controller must return a finite N_JOINTS vector")
        self._current_nominal = nominal.copy()
        command = np.asarray(
            self._diagnosis_policy(step_index, decision_time_s, available), dtype=float
        )
        self.nominal_commands.append(nominal.copy())
        self.commands.append(command.copy())
        return command
