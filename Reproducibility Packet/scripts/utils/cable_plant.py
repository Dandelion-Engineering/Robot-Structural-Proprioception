"""Schema-facing online plant wrapper for the selected MuJoCo cable model.

`CablePlant.advance` applies one controller command, integrates exactly one
control interval, and returns a lossless `PlantStepState`. A caller can therefore
interleave plant, sensor, estimator, and controller work online; stacking the
returned states later produces the role-separated privileged plant trace.
"""

from __future__ import annotations

import math
from dataclasses import replace
from typing import Callable

import mujoco
import numpy as np

from utils.cable_mechanics import (
    CableModelConfig,
    ModelHandles,
    apply_diagnostic_tip_load,
    build_two_link_model,
    commanded_torque,
    copy_dynamic_state,
    extract_deformation_coordinates,
    extract_state,
    validate_diagnostic_excitation,
    wrap_angle,
)
from utils.schema_types import FaultSpec, N_GAUGES, N_JOINTS, PlantStepState, PrivilegedRecord


class CablePlant:
    """Advance the selected two-link cable plant on the fixed control grid."""

    def __init__(
        self,
        config: CableModelConfig | None = None,
        *,
        point_count: int = 17,
        simulation_timestep_s: float = 1.0e-4,
        fault: FaultSpec | None = None,
    ) -> None:
        """Compile the plant and validate the physical fault boundary.

        Args:
            config: physical and excitation constants from the mechanics gate.
            point_count: cable centerline points per link (17 for the selected plant).
            simulation_timestep_s: MuJoCo integration step (0.1 ms when selected).
            fault: healthy, structure, or actuator specification. Sensor faults are
                rejected because they belong exclusively to the observation path.
        """

        self.config = config or CableModelConfig()
        validate_diagnostic_excitation(self.config)
        self.point_count = int(point_count)
        self.simulation_timestep_s = float(simulation_timestep_s)
        self.fault = fault or FaultSpec()
        self.fault.validate()
        self._validate_fault()

        ratio = self.config.control_dt_s / self.simulation_timestep_s
        self._physics_steps_per_control = int(round(ratio))
        if not math.isclose(ratio, self._physics_steps_per_control, rel_tol=0.0, abs_tol=1e-9):
            raise ValueError("control_dt_s must be an integer multiple of simulation_timestep_s")

        physical_config = self.config
        if self.fault.source_class == "structure" and self.fault.severity > 0.0:
            physical_config = replace(
                physical_config, structural_ei_remaining=float(self.fault.severity)
            )
        if self.fault.source_class == "actuator" and self.fault.severity > 0.0:
            physical_config = replace(
                physical_config, actuator_gain_remaining=float(self.fault.severity)
            )
        self._physical_config = physical_config

        self.model, self.handles = build_two_link_model(
            physical_config, self.point_count, self.simulation_timestep_s, False
        )
        self.data = mujoco.MjData(self.model)
        self._soft_model: mujoco.MjModel | None = None
        self._soft_handles: ModelHandles | None = None
        self._softened = False
        if self.fault.source_class == "structure":
            self._soft_model, self._soft_handles = build_two_link_model(
                physical_config, self.point_count, self.simulation_timestep_s, True
            )

        self._step_index = 0
        self._previous_q: np.ndarray | None = None
        self._previous_qd: np.ndarray | None = None

    @property
    def n_def(self) -> int:
        """Number of internal three-component deformation coordinates."""

        return 2 * 3 * (self.point_count - 2)

    @property
    def step_index(self) -> int:
        """Index of the next control step to be advanced."""

        return self._step_index

    def _validate_fault(self) -> None:
        """Reject faults that violate the plant/sensor injection boundary."""

        if self.fault.source_class == "sensor":
            raise ValueError("sensor faults must be injected by SensorModel, not CablePlant")
        if self.fault.source_class == "structure":
            if self.fault.subtype not in {"none", "link_stiffness_loss"}:
                raise ValueError(f"unsupported structural fault subtype: {self.fault.subtype}")
            if self.fault.location not in {-1, 1}:
                raise ValueError("the selected structural fault is the bounded link-2 section")
            severity = self.fault.severity or self.config.structural_ei_remaining
            if not 0.0 < severity <= 1.0:
                raise ValueError("structural severity is the remaining-EI fraction in (0,1]")
        if self.fault.source_class == "actuator":
            if self.fault.subtype not in {"none", "actuator_gain_loss"}:
                raise ValueError(f"unsupported actuator fault subtype: {self.fault.subtype}")
            if not 0 <= self.fault.location < N_JOINTS:
                raise ValueError("actuator fault location must be a joint index")
            severity = self.fault.severity or self.config.actuator_gain_remaining
            if not 0.0 < severity <= 1.0:
                raise ValueError("actuator severity is the remaining-gain fraction in (0,1]")

    def _fault_active(self) -> bool:
        """Whether the physical fault applies to the control step being advanced."""

        if self.fault.source_class == "healthy":
            return False
        onset = max(int(self.fault.onset_index), 0)
        return self._step_index >= onset

    def _activate_structural_fault_if_needed(self) -> None:
        """Swap to the topology-identical softened model at the declared boundary."""

        if self.fault.source_class != "structure" or not self._fault_active() or self._softened:
            return
        assert self._soft_model is not None and self._soft_handles is not None
        soft_data = mujoco.MjData(self._soft_model)
        copy_dynamic_state(self.data, soft_data)
        self.model = self._soft_model
        self.data = soft_data
        self.handles = self._soft_handles
        self._softened = True

    def advance(
        self,
        tau_cmd: np.ndarray,
        *,
        task_reference: np.ndarray | None = None,
        temperature_c: float | np.ndarray = 25.0,
    ) -> PlantStepState:
        """Advance one control interval and return the complete privileged state."""

        command = np.asarray(tau_cmd, dtype=float)
        if command.shape != (N_JOINTS,) or not np.all(np.isfinite(command)):
            raise ValueError(f"tau_cmd must be a finite shape-{(N_JOINTS,)} vector")
        reference = (
            np.asarray(task_reference, dtype=float)
            if task_reference is not None
            else np.array([2.0 * self.config.link_length_m, 0.0])
        )
        if reference.shape != (2,) or not np.all(np.isfinite(reference)):
            raise ValueError("task_reference must be a finite planar shape-(2,) vector")
        temperature = np.asarray(temperature_c, dtype=float)
        if temperature.ndim == 0:
            temperature = np.full(N_GAUGES, float(temperature))
        if temperature.shape != (N_GAUGES,) or not np.all(np.isfinite(temperature)):
            raise ValueError(f"temperature_c must be a finite scalar or shape-{(N_GAUGES,)} vector")

        self._activate_structural_fault_if_needed()
        control_range = np.asarray(self.model.actuator_ctrlrange, dtype=float)
        control_effort = np.clip(command, control_range[:, 0], control_range[:, 1])
        delivered = control_effort.copy()
        if self.fault.source_class == "actuator" and self._fault_active():
            gain = self.fault.severity or self.config.actuator_gain_remaining
            delivered[self.fault.location] *= gain
        self.data.ctrl[:] = delivered

        for _ in range(self._physics_steps_per_control):
            apply_diagnostic_tip_load(
                self.model, self.data, self.handles, self._physical_config
            )
            mujoco.mj_step(self.model, self.data)
        if not np.all(np.isfinite(self.data.qpos)) or not np.all(np.isfinite(self.data.qvel)):
            raise RuntimeError(f"non-finite MuJoCo state at control step {self._step_index}")

        q_raw, gauge_true, imu_true, tip_xyz = extract_state(
            self.model, self.data, self.handles, self._physical_config
        )
        if self._previous_q is None:
            q_true = q_raw
            qd_true = np.zeros(N_JOINTS)
            qdd_true = np.zeros(N_JOINTS)
        else:
            delta = np.array(
                [
                    wrap_angle(float(current - previous))
                    for current, previous in zip(q_raw, self._previous_q)
                ]
            )
            q_true = self._previous_q + delta
            qd_true = delta / self.config.control_dt_s
            qdd_true = (
                np.zeros(N_JOINTS)
                if self._previous_qd is None
                else (qd_true - self._previous_qd) / self.config.control_dt_s
            )
        deform_coords = extract_deformation_coordinates(self.model, self.data, self.handles)
        if deform_coords.shape != (self.n_def,):
            raise RuntimeError(
                f"deformation coordinate width {deform_coords.shape} does not match {(self.n_def,)}"
            )
        curvature_true = gauge_true / ((self.config.link_thickness_m / 2.0) * 1.0e6)
        true_task_output = np.array([tip_xyz[0], tip_xyz[2] - 0.5])
        tracking_error = reference - true_task_output

        state = PlantStepState(
            step=self._step_index,
            t_s=float(self.data.time),
            q_true=q_true.copy(),
            qd_true=qd_true.copy(),
            qdd_true=qdd_true.copy(),
            tau_cmd=command.copy(),
            tau_delivered_true=delivered.copy(),
            deform_coords=deform_coords,
            curvature_true=curvature_true,
            gauge_true=gauge_true.copy(),
            imu_true=imu_true.copy(),
            temperature_true=temperature.copy(),
            contact_state=np.empty(0, dtype=float),
            task_reference=reference.copy(),
            true_task_output=true_task_output,
            tracking_error=tracking_error,
            tracking_error_norm=float(np.linalg.norm(tracking_error)),
            control_effort=control_effort,
            saturation_flag=np.not_equal(command, control_effort),
            safety_flag=np.empty(0, dtype=bool),
        )
        self._previous_q = q_true.copy()
        self._previous_qd = qd_true.copy()
        self._step_index += 1
        return state

    def rollout(
        self,
        n_steps: int,
        *,
        command_fn: Callable[[float], np.ndarray] = commanded_torque,
        reference_fn: Callable[[float], np.ndarray] | None = None,
        temperature_fn: Callable[[int, float], float | np.ndarray] | None = None,
    ) -> PrivilegedRecord:
        """Run an open-loop development rollout and return its privileged trace."""

        if n_steps <= 0:
            raise ValueError("n_steps must be positive")
        states: list[PlantStepState] = []
        for index in range(n_steps):
            time_before_step = float(self.data.time)
            reference = reference_fn(time_before_step) if reference_fn else None
            temperature = temperature_fn(index, time_before_step) if temperature_fn else 25.0
            states.append(
                self.advance(
                    command_fn(time_before_step),
                    task_reference=reference,
                    temperature_c=temperature,
                )
            )
        return PrivilegedRecord.from_steps(states)
