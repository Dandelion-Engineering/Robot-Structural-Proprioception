"""Synthetic privileged plant trace -- a schema-conforming stand-in for testing.

DEVELOPMENT / TEST FIXTURE. This generates a `PrivilegedRecord` (schema section B)
from smooth analytic signals so the sensor lane (schema C) can be exercised and
tested in isolation, before the plant lane's real MuJoCo cable/rod trace exists.

It is NOT part of the confirmatory data pipeline and produces no physical claim:
the signals are analytic placeholders, not integrated mechanics. What it *does*
faithfully reproduce is the schema's fault-injection boundary, so the sensor lane
can be verified against it:

  * a STRUCTURAL fault changes the physical strain (`gauge_true`) at a station;
  * an ACTUATOR fault changes `tau_delivered_true` downstream of `control_effort`
    (so the current proxy, built from `control_effort`, cannot see the drop);
  * a SENSOR fault leaves ALL physical truth untouched -- the encoder lie is
    applied later by the sensor model to `q_obs`, not here (relational signature).

The real plant trace comes from the plant lane (Codex); this fixture is replaced
by it, and its on-disk format (`PrivilegedRecord.save_npz`) is a proposal for the
shared `plant/` role payload.
"""

from __future__ import annotations

import numpy as np

from utils.schema_types import (
    DEFAULT_N_DEF,
    IMU_DIM,
    N_CONTACT_STATE,
    N_GAUGES,
    N_JOINTS,
    N_SAFETY_FLAGS,
    PrivilegedRecord,
)
from utils.sensor_model import FaultSpec

# Fixed analytic link geometry for the synthetic tip forward-kinematics (metres).
_LINK_LENGTHS_M = (0.4, 0.4)


def synthetic_privileged_record(
    n_steps: int = 1500,
    f_ctrl: float = 500.0,
    n_def: int = DEFAULT_N_DEF,
    seed: int = 0,
    fault: FaultSpec | None = None,
    thermal_ramp_c: float = 0.0,
) -> PrivilegedRecord:
    """Return a smooth, schema-B-conforming synthetic privileged trace.

    Args:
        n_steps: number of control steps `T`.
        f_ctrl: control rate (Hz); sets the time grid `dt = 1/f_ctrl`.
        n_def: number of independent deformation coordinates (spike-frozen 90).
        seed: deterministic seed for the analytic phases (no measurement noise here).
        fault: optional fault; only STRUCTURAL / ACTUATOR faults alter physical
            truth here (sensor faults are applied by the sensor model, not here).
        thermal_ramp_c: linear temperature rise (deg C) over the rollout, added to
            the reference so the sensor model's thermal apparent strain can be tested.

    Returns:
        A validated `PrivilegedRecord`.
    """

    if n_steps < 2:
        raise ValueError("n_steps must be >= 2")
    fault = fault or FaultSpec()
    rng = np.random.default_rng(seed)
    step = np.arange(n_steps)
    t_s = step / f_ctrl

    # Joint trajectories: superposed sinusoids with analytic velocity/acceleration.
    freqs = np.array([1.1, 1.7])
    amps = np.array([0.4, 0.3])
    phases = rng.uniform(0.0, 2.0 * np.pi, size=N_JOINTS)
    omega = 2.0 * np.pi * freqs
    arg = omega[None, :] * t_s[:, None] + phases[None, :]
    q_true = amps[None, :] * np.sin(arg)
    qd_true = amps[None, :] * omega[None, :] * np.cos(arg)
    qdd_true = -amps[None, :] * omega[None, :] ** 2 * np.sin(arg)

    # Commanded / delivered torque and the actuator-side effort the proxy senses.
    tau_cmd = 0.2 * np.sin(2.0 * np.pi * 1.3 * t_s[:, None] + np.array([0.0, 0.7])[None, :])
    control_effort = np.clip(tau_cmd, -0.5, 0.5)  # saturated actuator-side effort
    tau_delivered_true = control_effort.copy()
    if fault.source_class == "actuator":
        onset = fault.onset_index if fault.onset_index >= 0 else 0
        joint = fault.location if 0 <= fault.location < N_JOINTS else N_JOINTS - 1
        gain_remaining = 1.0 - float(np.clip(fault.severity, 0.0, 1.0))
        tau_delivered_true[onset:, joint] *= gain_remaining  # downstream of the proxy

    # Independent deformation coordinates and physical curvature/strain.
    def_phases = rng.uniform(0.0, 2.0 * np.pi, size=n_def)
    deform_coords = 1.0e-3 * np.sin(
        2.0 * np.pi * 0.9 * t_s[:, None] + def_phases[None, :]
    )
    curvature_true = 0.5 * np.sin(
        2.0 * np.pi * 1.5 * t_s[:, None] + np.linspace(0.0, 1.2, N_GAUGES)[None, :]
    )
    surface_offset_m = 0.002  # half-thickness; curvature (1/m) * offset -> strain
    gauge_true = curvature_true * surface_offset_m * 1.0e6  # microstrain
    if fault.source_class == "structure":
        onset = fault.onset_index if fault.onset_index >= 0 else 0
        station = fault.location if 0 <= fault.location < N_GAUGES else N_GAUGES - 1
        # A local stiffness loss raises strain at the affected station after onset.
        gauge_true[onset:, station] *= 1.0 + float(np.clip(fault.severity, 0.0, 5.0))

    imu_true = np.column_stack(
        [
            9.81 * np.ones(n_steps) + 0.1 * np.sin(2.0 * np.pi * 2.0 * t_s),
            0.2 * np.sin(2.0 * np.pi * 1.4 * t_s),
            0.05 * np.cos(2.0 * np.pi * 1.1 * t_s),
            qd_true[:, 0] + qd_true[:, 1],
            0.01 * np.sin(2.0 * np.pi * 0.9 * t_s),
            0.01 * np.cos(2.0 * np.pi * 0.8 * t_s),
        ]
    )
    assert imu_true.shape == (n_steps, IMU_DIM)

    reference_temperature_c = 25.0
    temperature_true = reference_temperature_c + thermal_ramp_c * (t_s / t_s[-1])[:, None]
    temperature_true = np.repeat(temperature_true, N_GAUGES, axis=1)

    contact_state = np.zeros((n_steps, N_CONTACT_STATE))

    # Task-space tip: forward kinematics through the (deformed) configuration.
    true_task_output = _deformed_tip(q_true, curvature_true)
    task_reference = _deformed_tip(q_true, np.zeros_like(curvature_true))  # rigid nominal target
    tracking_error = task_reference - true_task_output
    tracking_error_norm = np.linalg.norm(tracking_error, axis=1)

    saturation_flag = np.abs(tau_cmd) >= 0.5
    safety_flag = np.zeros((n_steps, N_SAFETY_FLAGS), dtype=bool)

    record = PrivilegedRecord(
        step=step,
        t_s=t_s,
        q_true=q_true,
        qd_true=qd_true,
        qdd_true=qdd_true,
        tau_cmd=tau_cmd,
        tau_delivered_true=tau_delivered_true,
        deform_coords=deform_coords,
        curvature_true=curvature_true,
        gauge_true=gauge_true,
        imu_true=imu_true,
        temperature_true=temperature_true,
        contact_state=contact_state,
        task_reference=task_reference,
        true_task_output=true_task_output,
        tracking_error=tracking_error,
        tracking_error_norm=tracking_error_norm,
        control_effort=control_effort,
        saturation_flag=saturation_flag,
        safety_flag=safety_flag,
    )
    record.validate()
    return record


def _deformed_tip(q_true: np.ndarray, curvature_true: np.ndarray) -> np.ndarray:
    """Planar tip position from joint angles plus a small curvature-driven deflection.

    A deliberately simple analytic map: rigid two-link forward kinematics plus a
    lateral offset proportional to mean curvature, so the deformed tip differs from
    the rigid nominal tip (the honesty point of schema G's true-deformed-tip metric).
    """

    l1, l2 = _LINK_LENGTHS_M
    theta1 = q_true[:, 0]
    theta2 = q_true[:, 0] + q_true[:, 1]
    x = l1 * np.cos(theta1) + l2 * np.cos(theta2)
    y = l1 * np.sin(theta1) + l2 * np.sin(theta2)
    deflection = 0.01 * np.mean(curvature_true, axis=1)
    return np.column_stack([x - deflection * np.sin(theta2), y + deflection * np.cos(theta2)])
