"""Shared MuJoCo cable/rod mechanics for the spike and plant producer.

The feasibility gate and the schema-facing plant rollout use the same compiled
two-link model, state extraction, fault construction, and diagnostic excitation.
Keeping those operations here prevents the persisted plant trace from drifting
away from the mechanics candidate that actually passed the gate.
"""

from __future__ import annotations

import math
from dataclasses import dataclass

import mujoco
import numpy as np


@dataclass(frozen=True)
class CableModelConfig:
    """Physical, numerical, fault, and excitation values shared by cable runs."""

    link_length_m: float = 0.4
    link_width_m: float = 0.02
    link_thickness_m: float = 0.004
    density_kg_m3: float = 2700.0
    young_pa: float = 69.0e9
    poisson: float = 0.33
    control_dt_s: float = 0.002
    structural_ei_remaining: float = 0.50
    structural_section_start: float = 0.55
    structural_section_end: float = 0.85
    actuator_gain_remaining: float = 0.70
    task_torque_scale: float = 1.0
    diagnostic_tip_load_peak_n: float = 1.0
    diagnostic_tip_load_frequency_hz: float = 0.8
    diagnostic_tip_load_start_s: float = 0.0
    diagnostic_tip_load_duration_s: float | None = None
    diagnostic_tip_load_ramp_s: float = 0.0
    gauge_stations: tuple[float, float] = (0.25, 0.75)
    joint_angle_abs_limit_rad: tuple[float, float] = (math.pi, math.pi)
    joint_speed_abs_limit_rad_s: tuple[float, float] = (10.0, 10.0)
    tip_workspace_radius_limit_m: float = 0.82
    gauge_abs_limit_microstrain: float = 500.0
    tip_contact_force_limit_n: float = 5.0
    endpoint_contact_enabled: bool = False
    endpoint_contact_plane_z_m: float = 0.498


@dataclass(frozen=True)
class ModelHandles:
    """Cached MuJoCo identifiers needed to advance and inspect the cable model."""

    l1_body_ids: tuple[int, ...]
    l2_body_ids: tuple[int, ...]
    l1_tip_site_id: int
    l2_tip_site_id: int
    l2_last_body_id: int
    endpoint_contact_geom_id: int
    endpoint_contact_plane_geom_id: int
    accel_adr: int
    gyro_adr: int
    softened_geoms: tuple[str, ...]


def cable_body_names(prefix: str, point_count: int) -> list[str]:
    """Return generated cable body names in centerline order."""

    segment_count = point_count - 1
    return (
        [f"{prefix}B_first"]
        + [f"{prefix}B_{index}" for index in range(1, segment_count - 1)]
        + [f"{prefix}B_last"]
    )


def model_xml(config: CableModelConfig, point_count: int, timestep_s: float) -> str:
    """Construct the two-link cable/rod MJCF model as a string."""

    half_segment = config.link_length_m / (2.0 * (point_count - 1))
    shear_pa = config.young_pa / (2.0 * (1.0 + config.poisson))
    link2_start = config.link_length_m
    endpoint_contact_plane = ""
    endpoint_contact_pair = ""
    if config.endpoint_contact_enabled:
        endpoint_contact_plane = f"""
    <geom name="endpoint_contact_plane" type="plane"
          pos="0 0 {config.endpoint_contact_plane_z_m:.12g}"
          size="1 1 0.1" contype="0" conaffinity="0"/>
"""
        endpoint_contact_pair = f"""
  <contact>
    <pair name="endpoint_contact_pair" geom1="L2_G{point_count - 2}"
          geom2="endpoint_contact_plane" condim="3"/>
  </contact>
"""
    return f"""
<mujoco model="two_link_cable_spike">
  <compiler autolimits="true" angle="radian"/>
  <option timestep="{timestep_s:.12g}" gravity="0 0 0"
          integrator="implicitfast" solver="Newton" iterations="100"
          tolerance="1e-10"/>
  <size memory="16M"/>
  <extension>
    <plugin plugin="mujoco.elasticity.cable"/>
  </extension>
  <worldbody>
    {endpoint_contact_plane}
    <site name="base_ref" pos="0 0 0.5" size="0.004"/>
    <composite prefix="L1_" type="cable" curve="s"
               count="{point_count} 1 1" size="{config.link_length_m}"
               offset="0 0 0.5" initial="ball">
      <plugin plugin="mujoco.elasticity.cable">
        <config key="twist" value="{shear_pa:.12g}"/>
        <config key="bend" value="{config.young_pa:.12g}"/>
        <config key="flat" value="true"/>
        <config key="vmax" value="0"/>
      </plugin>
      <joint kind="main" damping="0.01" armature="1e-4"/>
      <geom type="box"
            size="{half_segment:.12g} {config.link_width_m / 2.0:.12g} {config.link_thickness_m / 2.0:.12g}"
            density="{config.density_kg_m3:.12g}" contype="0" conaffinity="0"/>
    </composite>
    <composite prefix="L2_" type="cable" curve="s"
               count="{point_count} 1 1" size="{config.link_length_m}"
               offset="{link2_start:.12g} 0 0.5" initial="free">
      <plugin plugin="mujoco.elasticity.cable">
        <config key="twist" value="{shear_pa:.12g}"/>
        <config key="bend" value="{config.young_pa:.12g}"/>
        <config key="flat" value="true"/>
        <config key="vmax" value="0"/>
      </plugin>
      <joint kind="main" damping="0.01" armature="1e-4"/>
      <geom type="box"
            size="{half_segment:.12g} {config.link_width_m / 2.0:.12g} {config.link_thickness_m / 2.0:.12g}"
            density="{config.density_kg_m3:.12g}" contype="0" conaffinity="0"/>
    </composite>
  </worldbody>
  {endpoint_contact_pair}
  <equality>
    <connect name="elbow_joint" site1="L1_S_last" site2="L2_S_first"
             solref="0.003 1" solimp="0.99 0.999 0.001"/>
  </equality>
  <actuator>
    <motor name="shoulder_motor" site="L1_S_first" refsite="base_ref"
           gear="0 0 0 0 1 0" ctrlrange="-1 1"/>
    <motor name="elbow_motor" site="L2_S_first" refsite="L1_S_last"
           gear="0 0 0 0 1 0" ctrlrange="-0.5 0.5"/>
  </actuator>
  <sensor>
    <accelerometer name="distal_accel" site="L2_S_last"/>
    <gyro name="distal_gyro" site="L2_S_last"/>
  </sensor>
</mujoco>
"""


def object_id(model: mujoco.MjModel, object_type: mujoco.mjtObj, name: str) -> int:
    """Resolve a named MuJoCo object and fail clearly if it is absent."""

    identifier = mujoco.mj_name2id(model, object_type, name)
    if identifier < 0:
        raise ValueError(f"MuJoCo object not found: {name}")
    return identifier


def build_two_link_model(
    config: CableModelConfig,
    point_count: int,
    timestep_s: float,
    local_softening: bool = False,
) -> tuple[mujoco.MjModel, ModelHandles]:
    """Compile the nominal or locally softened two-link cable model."""

    if point_count < 3:
        raise ValueError("point_count must be at least 3")
    model = mujoco.MjModel.from_xml_string(model_xml(config, point_count, timestep_s))
    softened: list[str] = []
    if local_softening:
        thickness_scale = config.structural_ei_remaining ** (1.0 / 3.0)
        segment_count = point_count - 1
        for index in range(segment_count):
            normalized_center = (index + 0.5) / segment_count
            if (
                config.structural_section_start
                <= normalized_center
                <= config.structural_section_end
            ):
                geom_name = f"L2_G{index}"
                geom_id = object_id(model, mujoco.mjtObj.mjOBJ_GEOM, geom_name)
                model.geom_size[geom_id, 2] *= thickness_scale
                softened.append(geom_name)

    l1_body_ids = tuple(
        object_id(model, mujoco.mjtObj.mjOBJ_BODY, name)
        for name in cable_body_names("L1_", point_count)
    )
    l2_body_ids = tuple(
        object_id(model, mujoco.mjtObj.mjOBJ_BODY, name)
        for name in cable_body_names("L2_", point_count)
    )
    accel_sensor = object_id(model, mujoco.mjtObj.mjOBJ_SENSOR, "distal_accel")
    gyro_sensor = object_id(model, mujoco.mjtObj.mjOBJ_SENSOR, "distal_gyro")
    endpoint_geom = object_id(
        model, mujoco.mjtObj.mjOBJ_GEOM, f"L2_G{point_count - 2}"
    )
    contact_plane_geom = -1
    if config.endpoint_contact_enabled:
        contact_plane_geom = object_id(
            model, mujoco.mjtObj.mjOBJ_GEOM, "endpoint_contact_plane"
        )
    return model, ModelHandles(
        l1_body_ids=l1_body_ids,
        l2_body_ids=l2_body_ids,
        l1_tip_site_id=object_id(model, mujoco.mjtObj.mjOBJ_SITE, "L1_S_last"),
        l2_tip_site_id=object_id(model, mujoco.mjtObj.mjOBJ_SITE, "L2_S_last"),
        l2_last_body_id=l2_body_ids[-1],
        endpoint_contact_geom_id=endpoint_geom,
        endpoint_contact_plane_geom_id=contact_plane_geom,
        accel_adr=int(model.sensor_adr[accel_sensor]),
        gyro_adr=int(model.sensor_adr[gyro_sensor]),
        softened_geoms=tuple(softened),
    )


def tangent_angle(data: mujoco.MjData, body_id: int) -> float:
    """Return the planar cable tangent angle about +Y from a body frame."""

    x_axis = data.xmat[body_id].reshape(3, 3)[:, 0]
    return math.atan2(-float(x_axis[2]), float(x_axis[0]))


def wrap_angle(angle: float) -> float:
    """Wrap an angle to [-pi, pi)."""

    return (angle + math.pi) % (2.0 * math.pi) - math.pi


def extract_state(
    model: mujoco.MjModel,
    data: mujoco.MjData,
    handles: ModelHandles,
    config: CableModelConfig,
) -> tuple[np.ndarray, np.ndarray, np.ndarray, np.ndarray]:
    """Extract joint angles, ideal virtual gauges, distal IMU, and deformed tip."""

    l1_angles = np.unwrap(
        np.array([tangent_angle(data, body_id) for body_id in handles.l1_body_ids])
    )
    l2_angles = np.unwrap(
        np.array([tangent_angle(data, body_id) for body_id in handles.l2_body_ids])
    )
    q_true = np.array(
        [l1_angles[0], wrap_angle(float(l2_angles[0] - l1_angles[-1]))], dtype=float
    )
    segment_length = config.link_length_m / len(handles.l1_body_ids)
    gauges: list[float] = []
    for angles in (l1_angles, l2_angles):
        for station in config.gauge_stations:
            joint_index = int(round(station * len(angles)))
            joint_index = min(max(joint_index, 1), len(angles) - 1)
            curvature = (angles[joint_index] - angles[joint_index - 1]) / segment_length
            gauges.append(curvature * (config.link_thickness_m / 2.0) * 1.0e6)
    accel = data.sensordata[handles.accel_adr : handles.accel_adr + 3]
    gyro = data.sensordata[handles.gyro_adr : handles.gyro_adr + 3]
    imu = np.concatenate((np.asarray(accel), np.asarray(gyro))).copy()
    tip = np.asarray(data.site_xpos[handles.l2_tip_site_id]).copy()
    return q_true, np.asarray(gauges), imu, tip


def quaternion_to_rotation_vector(quaternion: np.ndarray) -> np.ndarray:
    """Convert a MuJoCo `(w,x,y,z)` unit quaternion to its shortest log-map vector."""

    quat = np.asarray(quaternion, dtype=float).copy()
    norm = float(np.linalg.norm(quat))
    if not np.isfinite(norm) or norm <= 0.0:
        raise ValueError("ball-joint quaternion must be finite and nonzero")
    quat /= norm
    if quat[0] < 0.0:
        quat *= -1.0
    vector_norm = float(np.linalg.norm(quat[1:]))
    if vector_norm < 1.0e-12:
        return 2.0 * quat[1:]
    angle = 2.0 * math.atan2(vector_norm, float(quat[0]))
    return (angle / vector_norm) * quat[1:]


def extract_deformation_coordinates(
    model: mujoco.MjModel, data: mujoco.MjData, handles: ModelHandles
) -> np.ndarray:
    """Return internal cable ball-joint log maps, excluding shoulder and elbow poses."""

    rotation_vectors: list[np.ndarray] = []
    for body_ids in (handles.l1_body_ids, handles.l2_body_ids):
        # The first L1 body carries the shoulder ball joint; the first L2 body
        # carries the elbow-side free pose. Neither is an internal deformation DOF.
        for body_id in body_ids[1:]:
            joint_count = int(model.body_jntnum[body_id])
            if joint_count != 1:
                raise ValueError(
                    f"internal cable body {body_id} has {joint_count} joints; expected one"
                )
            joint_id = int(model.body_jntadr[body_id])
            if int(model.jnt_type[joint_id]) != int(mujoco.mjtJoint.mjJNT_BALL):
                raise ValueError(f"internal cable joint {joint_id} is not a ball joint")
            qpos_address = int(model.jnt_qposadr[joint_id])
            rotation_vectors.append(
                quaternion_to_rotation_vector(data.qpos[qpos_address : qpos_address + 4])
            )
    return np.concatenate(rotation_vectors)


def commanded_torque(time_s: float, scale: float = 1.0) -> np.ndarray:
    """Return the deterministic, bounded two-joint task-excitation command."""

    if not np.isfinite(scale) or scale < 0.0:
        raise ValueError("task torque scale must be finite and non-negative")

    shoulder = 0.25 * math.sin(2.0 * math.pi * 1.1 * time_s)
    shoulder += 0.10 * math.sin(2.0 * math.pi * 2.3 * time_s)
    elbow = 0.12 * math.sin(2.0 * math.pi * 1.7 * time_s + 0.4)
    return scale * np.array([shoulder, elbow], dtype=float)


def validate_safety_config(config: CableModelConfig) -> None:
    """Fail loudly when development safety-role limits are malformed."""

    angle_limits = np.asarray(config.joint_angle_abs_limit_rad, dtype=float)
    speed_limits = np.asarray(config.joint_speed_abs_limit_rad_s, dtype=float)
    if (
        angle_limits.shape != (2,)
        or not np.all(np.isfinite(angle_limits))
        or np.any(angle_limits <= 0.0)
    ):
        raise ValueError("joint_angle_abs_limit_rad must contain two finite positive values")
    if (
        speed_limits.shape != (2,)
        or not np.all(np.isfinite(speed_limits))
        or np.any(speed_limits <= 0.0)
    ):
        raise ValueError("joint_speed_abs_limit_rad_s must contain two finite positive values")
    scalar_limits = {
        "tip_workspace_radius_limit_m": config.tip_workspace_radius_limit_m,
        "gauge_abs_limit_microstrain": config.gauge_abs_limit_microstrain,
        "tip_contact_force_limit_n": config.tip_contact_force_limit_n,
    }
    for name, value in scalar_limits.items():
        if not np.isfinite(value) or value <= 0.0:
            raise ValueError(f"{name} must be finite and positive")
    if not np.isfinite(config.task_torque_scale) or config.task_torque_scale < 0.0:
        raise ValueError("task_torque_scale must be finite and non-negative")
    if not isinstance(config.endpoint_contact_enabled, (bool, np.bool_)):
        raise ValueError("endpoint_contact_enabled must be boolean")
    if not np.isfinite(config.endpoint_contact_plane_z_m):
        raise ValueError("endpoint_contact_plane_z_m must be finite")


def validate_diagnostic_excitation(config: CableModelConfig) -> None:
    """Fail loudly when the diagnostic-load envelope is non-physical or ambiguous."""

    if not np.isfinite(config.diagnostic_tip_load_peak_n) or config.diagnostic_tip_load_peak_n < 0.0:
        raise ValueError("diagnostic_tip_load_peak_n must be finite and non-negative")
    if (
        not np.isfinite(config.diagnostic_tip_load_frequency_hz)
        or config.diagnostic_tip_load_frequency_hz <= 0.0
    ):
        raise ValueError("diagnostic_tip_load_frequency_hz must be finite and positive")
    if not np.isfinite(config.diagnostic_tip_load_start_s) or config.diagnostic_tip_load_start_s < 0.0:
        raise ValueError("diagnostic_tip_load_start_s must be finite and non-negative")
    duration = config.diagnostic_tip_load_duration_s
    ramp = config.diagnostic_tip_load_ramp_s
    if not np.isfinite(ramp) or ramp < 0.0:
        raise ValueError("diagnostic_tip_load_ramp_s must be finite and non-negative")
    if duration is None:
        if ramp != 0.0:
            raise ValueError("a finite ramp requires diagnostic_tip_load_duration_s")
        return
    if not np.isfinite(duration) or duration <= 0.0:
        raise ValueError("diagnostic_tip_load_duration_s must be finite and positive")
    if ramp > duration / 2.0:
        raise ValueError("diagnostic_tip_load_ramp_s cannot exceed half the burst duration")


def diagnostic_tip_load_envelope(time_s: float, config: CableModelConfig) -> float:
    """Return the causal raised-cosine burst envelope in ``[0, 1]``.

    ``duration_s=None`` preserves the continuous gate excitation after ``start_s``.
    A finite duration produces a compact burst. Symmetric raised-cosine ramps make
    the load continuous at both boundaries without changing the declared peak.
    """

    validate_diagnostic_excitation(config)
    local_time = float(time_s) - config.diagnostic_tip_load_start_s
    if local_time < 0.0:
        return 0.0
    duration = config.diagnostic_tip_load_duration_s
    if duration is None:
        return 1.0
    if local_time >= duration:
        return 0.0
    ramp = config.diagnostic_tip_load_ramp_s
    if ramp <= 0.0:
        return 1.0
    if local_time < ramp:
        return 0.5 * (1.0 - math.cos(math.pi * local_time / ramp))
    if local_time > duration - ramp:
        remaining = duration - local_time
        return 0.5 * (1.0 - math.cos(math.pi * remaining / ramp))
    return 1.0


def diagnostic_tip_force_z(time_s: float, config: CableModelConfig) -> float:
    """Return the signed transverse diagnostic force at `time_s` (newtons)."""

    local_time = float(time_s) - config.diagnostic_tip_load_start_s
    return (
        -config.diagnostic_tip_load_peak_n
        * diagnostic_tip_load_envelope(time_s, config)
        * math.sin(2.0 * math.pi * config.diagnostic_tip_load_frequency_hz * local_time)
    )


def apply_diagnostic_tip_load(
    model: mujoco.MjModel,
    data: mujoco.MjData,
    handles: ModelHandles,
    config: CableModelConfig,
) -> None:
    """Apply the matched, zero-mean transverse diagnostic load at the true tip."""

    force_z = diagnostic_tip_force_z(float(data.time), config)
    data.qfrc_applied[:] = 0.0
    mujoco.mj_forward(model, data)
    mujoco.mj_applyFT(
        model,
        data,
        np.array([0.0, 0.0, force_z]),
        np.zeros(3),
        data.site_xpos[handles.l2_tip_site_id],
        handles.l2_last_body_id,
        data.qfrc_applied,
    )


def copy_dynamic_state(source: mujoco.MjData, target: mujoco.MjData) -> None:
    """Copy topology-identical dynamic state at the stiffness-fault onset."""

    target.time = source.time
    target.qpos[:] = source.qpos
    target.qvel[:] = source.qvel
    target.qacc_warmstart[:] = source.qacc_warmstart
    if target.act.size:
        target.act[:] = source.act
    mujoco.mj_forward(target.model, target)
