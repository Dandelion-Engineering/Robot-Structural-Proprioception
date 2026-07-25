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
    validate_safety_config,
    wrap_angle,
)
from utils.schema_types import (
    FaultSpec,
    N_CONTACT_STATE,
    N_GAUGES,
    N_JOINTS,
    N_SAFETY_FLAGS,
    PlantStepState,
    PrivilegedRecord,
)


class CablePlant:
    """Advance the selected two-link cable plant on the fixed control grid."""

    def __init__(
        self,
        config: CableModelConfig | None = None,
        *,
        point_count: int = 17,
        simulation_timestep_s: float = 1.0e-4,
        fault: FaultSpec | None = None,
        additional_faults: tuple[FaultSpec, ...] = (),
    ) -> None:
        """Compile the plant and validate the physical fault boundary.

        Args:
            config: physical and excitation constants from the mechanics gate.
            point_count: cable centerline points per link (17 for the selected plant).
            simulation_timestep_s: MuJoCo integration step (0.1 ms when selected).
            fault: healthy, structure, or actuator specification.
            additional_faults: optional second physical fault for preregistered
                compound plant cases. At most one structure and one actuator fault
                are accepted. Sensor faults remain observation-path only.
        """

        self.config = config or CableModelConfig()
        validate_diagnostic_excitation(self.config)
        validate_safety_config(self.config)
        self.point_count = int(point_count)
        self.simulation_timestep_s = float(simulation_timestep_s)
        self.fault = fault or FaultSpec()
        self.physical_faults = (self.fault, *tuple(additional_faults))
        for physical_fault in self.physical_faults:
            physical_fault.validate()
        self._validate_faults()
        self._structural_fault = next(
            (
                item
                for item in self.physical_faults
                if item.source_class == "structure"
            ),
            None,
        )
        self._actuator_fault = next(
            (
                item
                for item in self.physical_faults
                if item.source_class == "actuator"
            ),
            None,
        )

        ratio = self.config.control_dt_s / self.simulation_timestep_s
        self._physics_steps_per_control = int(round(ratio))
        if not math.isclose(ratio, self._physics_steps_per_control, rel_tol=0.0, abs_tol=1e-9):
            raise ValueError("control_dt_s must be an integer multiple of simulation_timestep_s")

        physical_config = self.config
        if self._structural_fault is not None:
            physical_config = replace(
                physical_config,
                structural_ei_remaining=float(self._structural_fault.severity),
            )
        if self._actuator_fault is not None:
            physical_config = replace(
                physical_config,
                actuator_gain_remaining=float(self._actuator_fault.severity),
            )
        self._physical_config = physical_config

        self.model, self.handles = build_two_link_model(
            physical_config, self.point_count, self.simulation_timestep_s, False
        )
        self.data = mujoco.MjData(self.model)
        self._soft_model: mujoco.MjModel | None = None
        self._soft_handles: ModelHandles | None = None
        self._softened = False
        if self._structural_fault is not None:
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

    def _validate_faults(self) -> None:
        """Reject faults that violate the plant/sensor injection boundary."""

        sources = [item.source_class for item in self.physical_faults]
        if "sensor" in sources:
            raise ValueError("sensor faults must be injected by SensorModel, not CablePlant")
        if len(self.physical_faults) > 1 and "healthy" in sources:
            raise ValueError("a healthy fault cannot accompany a physical fault")
        for source in ("structure", "actuator"):
            if sources.count(source) > 1:
                raise ValueError(f"at most one {source} fault may be active")
        if any(source not in {"healthy", "structure", "actuator"} for source in sources):
            raise ValueError(f"unsupported physical fault source set: {sources}")
        for physical_fault in self.physical_faults:
            if physical_fault.source_class == "structure":
                if physical_fault.subtype not in {"none", "link_stiffness_loss"}:
                    raise ValueError(
                        f"unsupported structural fault subtype: {physical_fault.subtype}"
                    )
                if physical_fault.location not in {-1, 1}:
                    raise ValueError(
                        "the selected structural fault is the bounded link-2 section"
                    )
                if not 0.0 < physical_fault.severity <= 1.0:
                    raise ValueError(
                        "structural severity is the remaining-EI fraction in (0,1]"
                    )
            if physical_fault.source_class == "actuator":
                if physical_fault.subtype not in {"none", "actuator_gain_loss"}:
                    raise ValueError(
                        f"unsupported actuator fault subtype: {physical_fault.subtype}"
                    )
                if not 0 <= physical_fault.location < N_JOINTS:
                    raise ValueError("actuator fault location must be a joint index")
                if not 0.0 < physical_fault.severity <= 1.0:
                    raise ValueError(
                        "actuator severity is the remaining-gain fraction in (0,1]"
                    )

    def _fault_active(self, fault: FaultSpec) -> bool:
        """Whether the physical fault applies to the control step being advanced."""

        if fault.source_class == "healthy":
            return False
        onset = max(int(fault.onset_index), 0)
        return self._step_index >= onset

    def _activate_structural_fault_if_needed(self) -> None:
        """Swap to the topology-identical softened model at the declared boundary."""

        fault = self._structural_fault
        if fault is None or not self._fault_active(fault) or self._softened:
            return
        assert self._soft_model is not None and self._soft_handles is not None
        soft_data = mujoco.MjData(self._soft_model)
        copy_dynamic_state(self.data, soft_data)
        self.model = self._soft_model
        self.data = soft_data
        self.handles = self._soft_handles
        self._softened = True

    def _schedule_contact_plane(self) -> None:
        """Enable the unchanged endpoint-plane pair only inside its assigned window."""

        if not self.config.endpoint_contact_enabled:
            return
        window = self.config.endpoint_contact_window_s
        time_s = float(self.data.time)
        tolerance = 1.0e-12
        active = window is None or (
            window[0] - tolerance <= time_s < window[1] - tolerance
        )
        plane_geom = self.handles.endpoint_contact_plane_geom_id
        if plane_geom < 0:
            raise RuntimeError("endpoint-contact plane handle is unavailable")
        target_z = (
            self.config.endpoint_contact_plane_z_m
            if active
            else self.config.endpoint_contact_plane_z_m - 10.0
        )
        if float(self.model.geom_pos[plane_geom, 2]) != target_z:
            self.model.geom_pos[plane_geom, 2] = target_z
            mujoco.mj_forward(self.model, self.data)

    def _contact_state(self) -> np.ndarray:
        """Return endpoint contact force and activity from MuJoCo constraint truth.

        The default development model remains collision-disabled and therefore emits
        ``[0, 0]``. When the optional endpoint-contact profile is enabled, only the
        distal link-2 endpoint geom and the explicit plane can collide. The first role
        field is the sum of the 3-D contact-force magnitudes returned by
        ``mujoco.mj_contactForce`` across that pair's contact points; the second is one
        whenever MuJoCo reports at least one contact for the pair.
        """

        if not self.config.endpoint_contact_enabled:
            if self.data.ncon != 0:
                raise RuntimeError(
                    "contact detected while the endpoint-contact profile is disabled"
                )
            state = np.array([0.0, 0.0], dtype=float)
        else:
            endpoint_geom = self.handles.endpoint_contact_geom_id
            plane_geom = self.handles.endpoint_contact_plane_geom_id
            if endpoint_geom < 0 or plane_geom < 0:
                raise RuntimeError("endpoint-contact geometry handles are unavailable")
            expected_pair = {endpoint_geom, plane_geom}
            total_force_n = 0.0
            active = False
            for contact_index in range(self.data.ncon):
                contact = self.data.contact[contact_index]
                actual_pair = {int(contact.geom1), int(contact.geom2)}
                if actual_pair != expected_pair:
                    raise RuntimeError(
                        "non-endpoint contact reached the endpoint-contact profile"
                    )
                wrench = np.zeros(6, dtype=float)
                mujoco.mj_contactForce(
                    self.model, self.data, contact_index, wrench
                )
                if not np.all(np.isfinite(wrench)):
                    raise RuntimeError("MuJoCo returned a non-finite contact wrench")
                total_force_n += float(np.linalg.norm(wrench[:3]))
                active = True
            state = np.array([total_force_n, float(active)], dtype=float)
        if not np.all(np.isfinite(state)) or state[0] < 0.0:
            raise RuntimeError(
                "contact-state force must be finite and non-negative"
            )
        if state.shape != (N_CONTACT_STATE,):
            raise RuntimeError("contact-state width drifted from the schema amendment")
        return state

    def _safety_flags(
        self,
        q_true: np.ndarray,
        qd_true: np.ndarray,
        gauge_true: np.ndarray,
        tip_xyz: np.ndarray,
        contact_state: np.ndarray,
    ) -> np.ndarray:
        """Evaluate the seven privileged development safety indicators."""

        angle_flags = np.abs(q_true) > np.asarray(self.config.joint_angle_abs_limit_rad)
        speed_flags = np.abs(qd_true) > np.asarray(self.config.joint_speed_abs_limit_rad_s)
        tip_radius = float(np.linalg.norm(tip_xyz - np.array([0.0, 0.0, 0.5])))
        flags = np.concatenate(
            [
                angle_flags,
                speed_flags,
                np.array(
                    [
                        tip_radius > self.config.tip_workspace_radius_limit_m,
                        np.max(np.abs(gauge_true)) > self.config.gauge_abs_limit_microstrain,
                        contact_state[0] > self.config.tip_contact_force_limit_n,
                    ],
                    dtype=bool,
                ),
            ]
        ).astype(bool, copy=False)
        if flags.shape != (N_SAFETY_FLAGS,):
            raise RuntimeError("safety-flag width drifted from the schema amendment")
        return flags

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
        self._schedule_contact_plane()
        control_range = np.asarray(self.model.actuator_ctrlrange, dtype=float)
        control_effort = np.clip(command, control_range[:, 0], control_range[:, 1])
        delivered = control_effort.copy()
        if self._actuator_fault is not None and self._fault_active(
            self._actuator_fault
        ):
            delivered[self._actuator_fault.location] *= self._actuator_fault.severity
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
        contact_state = self._contact_state()
        safety_flag = self._safety_flags(
            q_true, qd_true, gauge_true, tip_xyz, contact_state
        )

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
            contact_state=contact_state,
            task_reference=reference.copy(),
            true_task_output=true_task_output,
            tracking_error=tracking_error,
            tracking_error_norm=float(np.linalg.norm(tracking_error)),
            control_effort=control_effort,
            saturation_flag=np.not_equal(command, control_effort),
            safety_flag=safety_flag,
        )
        self._previous_q = q_true.copy()
        self._previous_qd = qd_true.copy()
        self._step_index += 1
        return state

    def rollout(
        self,
        n_steps: int,
        *,
        command_fn: Callable[[float], np.ndarray] | None = None,
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
            command = (
                command_fn(time_before_step)
                if command_fn is not None
                else commanded_torque(
                    time_before_step, scale=self.config.task_torque_scale
                )
            )
            states.append(
                self.advance(
                    command,
                    task_reference=reference,
                    temperature_c=temperature,
                )
            )
        return PrivilegedRecord.from_steps(states)
