"""Run the mechanics-only MuJoCo feasibility gate for structural sensing.

The spike uses two first-party MuJoCo cable/rod elements joined at an elbow,
applies matched excitation, and checks whether a local stiffness loss, actuator
gain loss, and encoder bias leave distinct conventional-plus-gauge histories.
It also checks mesh/timestep sensitivity and validates the nominal cable
strain against an independent Euler-Bernoulli cantilever calculation.
"""

from __future__ import annotations

import argparse
import csv
import json
import math
from dataclasses import asdict, dataclass
from pathlib import Path
from typing import Any

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
import mujoco
import numpy as np

from utils.cable_mechanics import (
    CableModelConfig,
    ModelHandles,
    apply_diagnostic_tip_load,
    build_two_link_model,
    cable_body_names,
    commanded_torque,
    copy_dynamic_state,
    extract_state,
    object_id,
    tangent_angle,
    validate_safety_config,
)


@dataclass(frozen=True)
class SpikeConfig(CableModelConfig):
    """Physical, numerical, and fault parameters for the feasibility spike."""

    duration_s: float = 3.0
    fault_onset_s: float = 1.0
    encoder_bias_rad: float = 0.05
    gauge_resolution_microstrain: float = 1.0
    thermal_cross_sensitivity_microstrain_per_c: float = 10.0
    beam_tip_force_n: float = 0.2
    beam_validation_duration_s: float = 4.0
    max_refinement_relative_error: float = 0.25
    max_beam_strain_relative_error: float = 0.10
    max_beam_tip_relative_error: float = 0.15

@dataclass
class SimulationResult:
    """Causal signal histories from one fault scenario."""

    time_s: np.ndarray
    tau_cmd_nm: np.ndarray
    q_true_rad: np.ndarray
    qd_true_rad_s: np.ndarray
    q_obs_rad: np.ndarray
    qd_obs_rad_s: np.ndarray
    imu: np.ndarray
    gauge_microstrain: np.ndarray
    tip_position_m: np.ndarray
    max_connect_residual_m: float


def parse_args() -> argparse.Namespace:
    """Parse command-line arguments for a portable spike run."""

    parser = argparse.ArgumentParser(
        description="Run the native-MuJoCo structural-proprioception feasibility spike."
    )
    parser.add_argument(
        "--output-dir",
        type=Path,
        default=Path("results/feasibility_spike"),
        help="Project-relative output directory (default: results/feasibility_spike).",
    )
    parser.add_argument("--duration-s", type=float, default=3.0)
    parser.add_argument("--fault-onset-s", type=float, default=1.0)
    parser.add_argument("--control-dt-s", type=float, default=0.002)
    parser.add_argument(
        "--diagnostic-tip-load-peak-n",
        type=float,
        default=1.0,
        help=(
            "Peak zero-mean distal diagnostic load in newtons; use 0 to "
            "reproduce the archived ordinary-excitation negative control."
        ),
    )
    parser.add_argument(
        "--quick",
        action="store_true",
        help="Run one coarse configuration for a smoke test; not a gate verdict.",
    )
    return parser.parse_args()


def simulate_case(
    config: SpikeConfig,
    point_count: int,
    timestep_s: float,
    scenario: str,
) -> SimulationResult:
    """Simulate one healthy or single-fault scenario with causal outputs."""

    if scenario not in {"healthy", "structural", "actuator", "encoder"}:
        raise ValueError(f"Unknown scenario: {scenario}")
    validate_safety_config(config)
    ratio = config.control_dt_s / timestep_s
    output_stride = int(round(ratio))
    if not math.isclose(ratio, output_stride, rel_tol=0.0, abs_tol=1e-9):
        raise ValueError("control_dt_s must be an integer multiple of timestep_s")
    total_steps = int(round(config.duration_s / timestep_s))
    onset_step = int(round(config.fault_onset_s / timestep_s))

    model, handles = build_two_link_model(config, point_count, timestep_s, False)
    data = mujoco.MjData(model)
    soft_model: mujoco.MjModel | None = None
    soft_handles: ModelHandles | None = None
    if scenario == "structural":
        soft_model, soft_handles = build_two_link_model(config, point_count, timestep_s, True)

    times: list[float] = []
    commands: list[np.ndarray] = []
    q_true_rows: list[np.ndarray] = []
    q_obs_rows: list[np.ndarray] = []
    gauges: list[np.ndarray] = []
    imus: list[np.ndarray] = []
    tips: list[np.ndarray] = []
    max_connect_residual = 0.0

    for step in range(total_steps):
        if scenario == "structural" and step == onset_step:
            assert soft_model is not None and soft_handles is not None
            soft_data = mujoco.MjData(soft_model)
            copy_dynamic_state(data, soft_data)
            model, data, handles = soft_model, soft_data, soft_handles

        tau_cmd = commanded_torque(float(data.time), scale=config.task_torque_scale)
        delivered = tau_cmd.copy()
        if scenario == "actuator" and step >= onset_step:
            delivered[1] *= config.actuator_gain_remaining
        data.ctrl[:] = delivered
        apply_diagnostic_tip_load(model, data, handles, config)
        mujoco.mj_step(model, data)
        if not np.all(np.isfinite(data.qpos)) or not np.all(np.isfinite(data.qvel)):
            raise RuntimeError(
                f"Non-finite state in {scenario}, points={point_count}, "
                f"dt={timestep_s}, step={step}"
            )
        if data.nefc:
            max_connect_residual = max(
                max_connect_residual, float(np.max(np.abs(data.efc_pos[: data.nefc])))
            )

        if (step + 1) % output_stride == 0:
            q_true, gauge, imu, tip = extract_state(model, data, handles, config)
            q_obs = q_true.copy()
            if scenario == "encoder" and data.time >= config.fault_onset_s:
                q_obs[0] += config.encoder_bias_rad
            times.append(float(data.time))
            commands.append(tau_cmd)
            q_true_rows.append(q_true)
            q_obs_rows.append(q_obs)
            gauges.append(gauge)
            imus.append(imu)
            tips.append(tip)

    time = np.asarray(times)
    q_true_array = np.unwrap(np.asarray(q_true_rows), axis=0)
    q_obs_array = np.unwrap(np.asarray(q_obs_rows), axis=0)
    qd_true = np.zeros_like(q_true_array)
    qd_true[1:] = np.diff(q_true_array, axis=0) / np.diff(time)[:, None]
    qd_true[0] = qd_true[1]
    qd_obs = np.zeros_like(q_obs_array)
    qd_obs[1:] = np.diff(q_obs_array, axis=0) / np.diff(time)[:, None]
    qd_obs[0] = qd_obs[1]
    return SimulationResult(
        time_s=time,
        tau_cmd_nm=np.asarray(commands),
        q_true_rad=q_true_array,
        qd_true_rad_s=qd_true,
        q_obs_rad=q_obs_array,
        qd_obs_rad_s=qd_obs,
        imu=np.asarray(imus),
        gauge_microstrain=np.asarray(gauges),
        tip_position_m=np.asarray(tips),
        max_connect_residual_m=max_connect_residual,
    )


def post_fault_mask(result: SimulationResult, config: SpikeConfig) -> np.ndarray:
    """Return samples in the post-fault analysis interval."""

    return result.time_s >= config.fault_onset_s


def rms(array: np.ndarray, axis: int = 0) -> np.ndarray:
    """Compute root-mean-square magnitude along one axis."""

    return np.sqrt(np.mean(np.square(array), axis=axis))


def signature_metrics(
    healthy: SimulationResult,
    fault: SimulationResult,
    config: SpikeConfig,
) -> dict[str, np.ndarray]:
    """Summarize one fault-minus-healthy causal feature signature."""

    mask = post_fault_mask(healthy, config)
    q_delta = fault.q_obs_rad[mask] - healthy.q_obs_rad[mask]
    imu_delta = fault.imu[mask] - healthy.imu[mask]
    gauge_delta = fault.gauge_microstrain[mask] - healthy.gauge_microstrain[mask]
    return {
        "q_rms": rms(q_delta),
        "imu_rms": rms(imu_delta),
        "gauge_rms": rms(gauge_delta),
        "gauge_peak": np.max(np.abs(gauge_delta), axis=0),
        "feature_vector": np.concatenate(
            (rms(q_delta) / 0.01, rms(imu_delta) / 0.10, rms(gauge_delta) / 10.0)
        ),
    }


def relative_vector_error(candidate: np.ndarray, reference: np.ndarray) -> float:
    """Compute a norm-relative error with a safe zero-reference branch."""

    denominator = float(np.linalg.norm(reference))
    if denominator == 0.0:
        return 0.0 if float(np.linalg.norm(candidate)) == 0.0 else math.inf
    return float(np.linalg.norm(candidate - reference) / denominator)


def isolated_beam_xml(config: SpikeConfig, point_count: int, timestep_s: float) -> str:
    """Construct a single nominal cantilever for independent beam validation."""

    half_segment = config.link_length_m / (2.0 * (point_count - 1))
    shear_pa = config.young_pa / (2.0 * (1.0 + config.poisson))
    return f"""
<mujoco model="cantilever_validation">
  <compiler autolimits="true"/>
  <option timestep="{timestep_s:.12g}" gravity="0 0 0" integrator="implicitfast"/>
  <extension><plugin plugin="mujoco.elasticity.cable"/></extension>
  <worldbody>
    <composite prefix="B_" type="cable" curve="s" count="{point_count} 1 1"
               size="{config.link_length_m}" initial="none">
      <plugin plugin="mujoco.elasticity.cable">
        <config key="twist" value="{shear_pa:.12g}"/>
        <config key="bend" value="{config.young_pa:.12g}"/>
        <config key="flat" value="true"/>
      </plugin>
      <joint kind="main" damping="0.03" armature="1e-5"/>
      <geom type="box"
            size="{half_segment:.12g} {config.link_width_m / 2.0:.12g} {config.link_thickness_m / 2.0:.12g}"
            density="{config.density_kg_m3:.12g}" contype="0" conaffinity="0"/>
    </composite>
  </worldbody>
</mujoco>
"""


def run_beam_validation(
    config: SpikeConfig, point_count: int = 17, timestep_s: float = 1.0e-4
) -> dict[str, Any]:
    """Compare cable strains/deflection with Euler-Bernoulli closed form."""

    model = mujoco.MjModel.from_xml_string(isolated_beam_xml(config, point_count, timestep_s))
    data = mujoco.MjData(model)
    body_ids = tuple(
        object_id(model, mujoco.mjtObj.mjOBJ_BODY, name)
        for name in cable_body_names("B_", point_count)
    )
    tip_site_id = object_id(model, mujoco.mjtObj.mjOBJ_SITE, "B_S_last")
    last_body_id = body_ids[-1]
    step_count = int(round(config.beam_validation_duration_s / timestep_s))
    force = np.array([0.0, 0.0, -config.beam_tip_force_n])
    for step in range(step_count):
        data.qfrc_applied[:] = 0.0
        mujoco.mj_forward(model, data)
        mujoco.mj_applyFT(
            model,
            data,
            force,
            np.zeros(3),
            data.site_xpos[tip_site_id],
            last_body_id,
            data.qfrc_applied,
        )
        mujoco.mj_step(model, data)
        if not np.all(np.isfinite(data.qpos)):
            raise RuntimeError(f"Non-finite cantilever validation state at step {step}")
    mujoco.mj_forward(model, data)
    angles = np.unwrap(np.array([tangent_angle(data, body_id) for body_id in body_ids]))
    segment_length = config.link_length_m / len(body_ids)
    inertia_m4 = (
        config.link_width_m * config.link_thickness_m**3 / 12.0
    )
    measured_strain: list[float] = []
    expected_strain: list[float] = []
    strain_errors: list[float] = []
    for station in config.gauge_stations:
        joint_index = int(round(station * len(angles)))
        curvature = (angles[joint_index] - angles[joint_index - 1]) / segment_length
        measured = curvature * (config.link_thickness_m / 2.0) * 1.0e6
        expected = (
            config.beam_tip_force_n
            * (config.link_length_m - station * config.link_length_m)
            * (config.link_thickness_m / 2.0)
            / (config.young_pa * inertia_m4)
            * 1.0e6
        )
        measured_strain.append(float(measured))
        expected_strain.append(float(expected))
        strain_errors.append(abs(float(measured - expected)) / abs(float(expected)))
    measured_tip_deflection = -float(data.site_xpos[tip_site_id, 2])
    expected_tip_deflection = (
        config.beam_tip_force_n
        * config.link_length_m**3
        / (3.0 * config.young_pa * inertia_m4)
    )
    return {
        "point_count": point_count,
        "timestep_s": timestep_s,
        "tip_force_n": config.beam_tip_force_n,
        "measured_gauge_microstrain": measured_strain,
        "expected_gauge_microstrain": expected_strain,
        "gauge_relative_error": strain_errors,
        "measured_tip_deflection_m": measured_tip_deflection,
        "expected_tip_deflection_m": expected_tip_deflection,
        "tip_relative_error": abs(measured_tip_deflection - expected_tip_deflection)
        / expected_tip_deflection,
    }


def probe_slender_3d_flex(config: SpikeConfig) -> dict[str, Any]:
    """Compile the reserve volumetric-flex candidate and report its state size."""

    mass = (
        config.density_kg_m3
        * config.link_length_m
        * config.link_width_m
        * config.link_thickness_m
    )
    xml = f"""
<mujoco model="slender_3d_flex_probe">
  <compiler autolimits="true"/>
  <option timestep="1e-5" gravity="0 0 0" integrator="implicitfast"/>
  <worldbody>
    <flexcomp name="beam" type="grid" dim="3" dof="full"
              count="9 2 2" spacing="0.05 0.02 0.004"
              pos="0.2 0 0" radius="0" mass="{mass:.12g}">
      <contact selfcollide="none" contype="0" conaffinity="0"/>
      <edge damping="0.01"/>
      <elasticity young="{config.young_pa:.12g}" poisson="{config.poisson:.12g}"
                  damping="1e-5"/>
      <pin gridrange="0 0 0 0 1 1"/>
    </flexcomp>
  </worldbody>
</mujoco>
"""
    model = mujoco.MjModel.from_xml_string(xml)
    data = mujoco.MjData(model)
    for _ in range(10):
        mujoco.mj_step(model, data)
    return {
        "compiled": True,
        "finite_smoke_step": bool(np.all(np.isfinite(data.qpos))),
        "nq": int(model.nq),
        "nv": int(model.nv),
        "nbody": int(model.nbody),
        "nflexvert": int(model.nflexvert),
        "nflexelem": int(model.nflexelem),
        "role": "reserve candidate; full two-link escalation not needed if cable gate passes",
    }


def write_metrics_csv(
    path: Path,
    signatures: dict[str, dict[str, dict[str, np.ndarray]]],
) -> None:
    """Write per-configuration fault signature metrics as a flat CSV."""

    fieldnames = (
        ["configuration", "scenario"]
        + [f"q_rms_{index + 1}_rad" for index in range(2)]
        + [f"imu_rms_{index + 1}" for index in range(6)]
        + [f"gauge_rms_{index + 1}_microstrain" for index in range(4)]
        + [f"gauge_peak_{index + 1}_microstrain" for index in range(4)]
    )
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames)
        writer.writeheader()
        for configuration, cases in signatures.items():
            for scenario, metrics in cases.items():
                row: dict[str, Any] = {
                    "configuration": configuration,
                    "scenario": scenario,
                }
                row.update(
                    {
                        f"q_rms_{index + 1}_rad": float(value)
                        for index, value in enumerate(metrics["q_rms"])
                    }
                )
                row.update(
                    {
                        f"imu_rms_{index + 1}": float(value)
                        for index, value in enumerate(metrics["imu_rms"])
                    }
                )
                row.update(
                    {
                        f"gauge_rms_{index + 1}_microstrain": float(value)
                        for index, value in enumerate(metrics["gauge_rms"])
                    }
                )
                row.update(
                    {
                        f"gauge_peak_{index + 1}_microstrain": float(value)
                        for index, value in enumerate(metrics["gauge_peak"])
                    }
                )
                writer.writerow(row)


def plot_gauge_histories(
    output_path: Path,
    healthy: SimulationResult,
    faults: dict[str, SimulationResult],
    config: SpikeConfig,
) -> None:
    """Plot fine-model fault-minus-healthy gauge histories at 300 DPI."""

    figure, axes = plt.subplots(2, 2, figsize=(10, 7), sharex=True)
    colors = {"structural": "#d55e00", "actuator": "#0072b2", "encoder": "#009e73"}
    for channel, axis in enumerate(axes.flat):
        for scenario, result in faults.items():
            delta = result.gauge_microstrain[:, channel] - healthy.gauge_microstrain[:, channel]
            axis.plot(result.time_s, delta, label=scenario, color=colors[scenario], linewidth=1.1)
        axis.axvline(config.fault_onset_s, color="black", linestyle="--", linewidth=0.8)
        link = 1 if channel < 2 else 2
        station = config.gauge_stations[channel % 2]
        axis.set_title(f"Link {link}, station {station:.2f} L")
        axis.set_ylabel("fault - healthy (µε)")
        axis.grid(alpha=0.25)
    axes[-1, 0].set_xlabel("time (s)")
    axes[-1, 1].set_xlabel("time (s)")
    axes[0, 0].legend(frameon=False)
    figure.suptitle("Native cable/rod virtual-gauge fault signatures")
    figure.tight_layout()
    figure.savefig(output_path, dpi=300, bbox_inches="tight")
    plt.close(figure)


def plot_signature_heatmap(
    output_path: Path, fine_signatures: dict[str, dict[str, np.ndarray]]
) -> None:
    """Plot normalized causal feature RMS signatures at 300 DPI."""

    scenarios = ["structural", "actuator", "encoder"]
    matrix = np.vstack([fine_signatures[name]["feature_vector"] for name in scenarios])
    labels = ["q1", "q2"] + [f"imu{i + 1}" for i in range(6)] + [f"g{i + 1}" for i in range(4)]
    figure, axis = plt.subplots(figsize=(10, 3.4))
    image = axis.imshow(np.log10(1.0 + matrix), aspect="auto", cmap="viridis")
    axis.set_xticks(range(len(labels)), labels, rotation=45, ha="right")
    axis.set_yticks(range(len(scenarios)), scenarios)
    axis.set_title("Fault-minus-healthy RMS signature (log10(1 + normalized magnitude))")
    figure.colorbar(image, ax=axis, label="log10(1 + normalized RMS)")
    figure.tight_layout()
    figure.savefig(output_path, dpi=300, bbox_inches="tight")
    plt.close(figure)


def plain(value: Any) -> Any:
    """Convert NumPy-rich structures into JSON-serializable Python values."""

    if isinstance(value, np.ndarray):
        return value.tolist()
    if isinstance(value, (np.floating, np.integer)):
        return value.item()
    if isinstance(value, dict):
        return {str(key): plain(item) for key, item in value.items()}
    if isinstance(value, (list, tuple)):
        return [plain(item) for item in value]
    return value


def write_report(path: Path, summary: dict[str, Any]) -> None:
    """Write a concise human-readable gate report from the measured summary."""

    gate = summary["gate"]
    verdict = "PASS" if gate["pass"] else "BLOCK"
    selected = bool(gate["pass"])
    beam = summary["beam_validation"]
    convergence = summary["refinement"]
    fine = summary["fine_metrics"]
    lines = [
        "# MuJoCo Cable/Rod Feasibility Spike",
        "",
        f"**Verdict: {verdict}.** The native cable/rod candidate "
        + ("clears" if gate["pass"] else "does not clear")
        + " the mechanics-only gate under the declared thresholds.",
        "",
        "## What was tested",
        "",
        "A planar two-actuator arm was built from two first-party MuJoCo cable/rod elements. "
        "Each 0.4 m aluminium-like link has a 20 mm × 4 mm rectangular section. The elbow "
        "is a positional connect constraint and the shoulder/elbow torques are applied through "
        "relative site transmissions. Four virtual gauges are derived from simulator-integrated "
        "segment orientations at 0.25 L and 0.75 L on each link; no gauge is copied from a fault label.",
        "",
        "The structural case reduces local link-2 bending inertia over the normalized section "
        f"[{summary['config']['structural_section_start']:.2f}, "
        f"{summary['config']['structural_section_end']:.2f}] to "
        f"{100 * summary['config']['structural_ei_remaining']:.0f}% at the fault onset. "
        "The actuator case reduces elbow delivered torque downstream of the unchanged command/current proxy. "
        "The encoder case adds a shoulder bias without changing the physical trajectory. All cases receive "
        f"the same zero-mean {summary['config']['diagnostic_tip_load_peak_n']:.1f} N distal diagnostic load.",
        "",
        (
            "MuJoCo documents the cable plugin as an inextensible 1-D continuum with decoupled bending and twist; "
            "its stiffness and inertia come from material parameters and section shape. The volumetric 3-D flex "
            "candidate also compiled, but "
            + (
                "remains the higher-cost reserve because the cable path cleared the gate. "
                if selected
                else "remains available because this cable run did not clear the gate. "
            )
            + "Sources: [MuJoCo modeling guide](https://mujoco.readthedocs.io/en/latest/modeling.html#composite-objects), "
            + "[first-party elasticity plugin](https://github.com/google-deepmind/mujoco/tree/main/plugin/elasticity)."
        ),
        "",
        "## Gate measurements",
        "",
        "| Check | Measured | Required | Result |",
        "|---|---:|---:|---|",
        f"| Structural: max gauge RMS vs healthy | {gate['structural_max_gauge_rms_microstrain']:.2f} µε | > {gate['credible_floor_microstrain']:.2f} µε | {'PASS' if gate['structural_signal'] else 'BLOCK'} |",
        f"| Actuator: max gauge RMS vs healthy | {gate['actuator_max_gauge_rms_microstrain']:.2f} µε | > {gate['credible_floor_microstrain']:.2f} µε | {'PASS' if gate['actuator_signal'] else 'BLOCK'} |",
        f"| Structural vs actuator: max gauge RMS separation | {gate['structural_actuator_max_gauge_rms_microstrain']:.2f} µε | > {gate['credible_floor_microstrain']:.2f} µε | {'PASS' if gate['structural_actuator_separation'] else 'BLOCK'} |",
        f"| Encoder: q-observation RMS change | {gate['encoder_q_rms_rad']:.4f} rad | ≥ {gate['encoder_required_q_rms_rad']:.4f} rad | {'PASS' if gate['encoder_relational'] else 'BLOCK'} |",
        f"| Encoder: physical gauge RMS change | {gate['encoder_physical_gauge_rms_microstrain']:.3g} µε | ≈ 0 | {'PASS' if gate['encoder_physical_gauge_unchanged'] else 'BLOCK'} |",
        f"| Timestep signature error | {convergence['timestep_relative_error_max']:.3f} | ≤ {summary['config']['max_refinement_relative_error']:.2f} | {'PASS' if convergence['timestep_pass'] else 'BLOCK'} |",
        f"| Mesh signature error | {convergence['mesh_relative_error_max']:.3f} | ≤ {summary['config']['max_refinement_relative_error']:.2f} | {'PASS' if convergence['mesh_pass'] else 'BLOCK'} |",
        f"| Beam gauge relative error (max) | {max(beam['gauge_relative_error']):.3f} | ≤ {summary['config']['max_beam_strain_relative_error']:.2f} | {'PASS' if gate['beam_strain'] else 'BLOCK'} |",
        f"| Beam tip-deflection relative error | {beam['tip_relative_error']:.3f} | ≤ {summary['config']['max_beam_tip_relative_error']:.2f} | {'PASS' if gate['beam_tip'] else 'BLOCK'} |",
        "",
        "The credible floor is deliberately the larger of the 1 µε resolution floor and the "
        "10 µε apparent-strain shift associated with 1 °C of uncompensated temperature change.",
        "",
        "## Fine-model signature summary",
        "",
        f"- Structural gauge RMS (four stations): {', '.join(f'{x:.2f}' for x in fine['structural']['gauge_rms'])} µε.",
        f"- Actuator gauge RMS (four stations): {', '.join(f'{x:.2f}' for x in fine['actuator']['gauge_rms'])} µε.",
        f"- Encoder gauge RMS (four stations): {', '.join(f'{x:.3g}' for x in fine['encoder']['gauge_rms'])} µε; the physical/gauge history remains unchanged while q1 shifts.",
        "",
        "## Candidate decision and limits",
        "",
        (
            (
                "The cable/rod path is selected for the next plant implementation. It has independent integrated "
                "deformation coordinates, clears the conservative signal floor, agrees with the independent beam "
                "calculation, and is materially smaller than the reserve volumetric flex. "
                if selected
                else "The cable/rod path is not selected by this run because at least one mechanics gate failed. "
                "The failed measurements must be diagnosed or the volumetric-flex fallback escalated before commitment. "
            )
            + "The 3-D flex smoke probe "
            + f"compiled with nq={summary['slender_3d_flex_probe']['nq']} and "
            + f"{summary['slender_3d_flex_probe']['nflexelem']} tetrahedral elements; it is retained only if later "
            + "validation exposes a cable-specific failure."
        ),
        "",
        (
            f"The selected fine plant exposes `n_def={summary['candidate_contract']['n_def']}` deformation "
            "coordinates: three-component log-map rotation vectors for the 15 internal cable ball joints "
            "on each link, excluding the shoulder and elbow rigid-joint coordinates. Gauge stations remain "
            "fixed at normalized positions 0.25 and 0.75 on each link."
            if selected
            else "No deformation-coordinate contract is selected by a blocked run."
        ),
        "",
        (
            f"This decision is excitation-conditional: this report includes the matched zero-mean "
            f"{summary['config']['diagnostic_tip_load_peak_n']:.1f} N distal diagnostic load. "
            "The ordinary torque-only condition is a separate negative control and does not inherit this PASS."
            if summary["config"]["diagnostic_tip_load_peak_n"] > 0.0
            else "This is the ordinary torque-only negative control: no distal diagnostic load is applied. "
            "A BLOCK here does not invalidate a separate diagnostic-excitation PASS."
        ),
        "",
        "This is not a claim that the full research hypothesis succeeds. It is only the mechanics feasibility gate. "
        "The spike uses deterministic matched excitation, one local stiffness section, one actuator severity, "
        "one encoder bias, no contact, and noise-floor comparisons rather than trained attribution. The next "
        "plant step must expose the per-step schema object and integrate the full thermal/drift/dropout "
        "sensor model before any pilot or confirmatory conclusion.",
        "",
        "## Outputs",
        "",
        "- `summary.json` — all parameters, measurements, gates, and candidate metadata.",
        "- `signature_metrics.csv` — per-configuration feature/gauge RMS and peak values.",
        "- `gauge_fault_signatures.png` — fine-model fault-minus-healthy gauge histories.",
        "- `feature_signature_heatmap.png` — normalized conventional-plus-gauge RMS patterns.",
    ]
    path.write_text("\n".join(lines) + "\n", encoding="utf-8")


def run_gate(config: SpikeConfig, output_dir: Path, quick: bool = False) -> dict[str, Any]:
    """Run all spike configurations, evaluate gates, and write artifacts."""

    output_dir.mkdir(parents=True, exist_ok=True)
    specifications = (
        [(9, 2.0e-4)]
        if quick
        else [(9, 2.0e-4), (9, 1.0e-4), (17, 1.0e-4)]
    )
    scenarios = ("healthy", "structural", "actuator", "encoder")
    results: dict[str, dict[str, SimulationResult]] = {}
    signatures: dict[str, dict[str, dict[str, np.ndarray]]] = {}
    config_by_label: dict[str, tuple[int, float]] = {}
    for point_count, timestep_s in specifications:
        label = f"points_{point_count}_dt_{timestep_s:.0e}"
        config_by_label[label] = (point_count, timestep_s)
        print(f"Running {label} ...", flush=True)
        results[label] = {
            scenario: simulate_case(config, point_count, timestep_s, scenario)
            for scenario in scenarios
        }
        signatures[label] = {
            scenario: signature_metrics(
                results[label]["healthy"], results[label][scenario], config
            )
            for scenario in scenarios[1:]
        }

    fine_label = list(results)[-1]
    fine_results = results[fine_label]
    fine_signatures = signatures[fine_label]
    beam = run_beam_validation(
        config,
        point_count=17 if not quick else 9,
        timestep_s=1.0e-4 if not quick else 2.0e-4,
    )
    flex_probe = probe_slender_3d_flex(config)

    refinement: dict[str, Any]
    if quick:
        refinement = {
            "evaluated": False,
            "timestep_relative_error": {},
            "mesh_relative_error": {},
            "timestep_relative_error_max": math.nan,
            "mesh_relative_error_max": math.nan,
            "timestep_pass": False,
            "mesh_pass": False,
        }
    else:
        coarse_label, timestep_label, mesh_label = list(results)
        timestep_errors = {
            scenario: relative_vector_error(
                signatures[coarse_label][scenario]["gauge_rms"],
                signatures[timestep_label][scenario]["gauge_rms"],
            )
            for scenario in ("structural", "actuator")
        }
        mesh_errors = {
            scenario: relative_vector_error(
                signatures[timestep_label][scenario]["gauge_rms"],
                signatures[mesh_label][scenario]["gauge_rms"],
            )
            for scenario in ("structural", "actuator")
        }
        refinement = {
            "evaluated": True,
            "timestep_relative_error": timestep_errors,
            "mesh_relative_error": mesh_errors,
            "timestep_relative_error_max": max(timestep_errors.values()),
            "mesh_relative_error_max": max(mesh_errors.values()),
            "timestep_pass": max(timestep_errors.values())
            <= config.max_refinement_relative_error,
            "mesh_pass": max(mesh_errors.values()) <= config.max_refinement_relative_error,
        }

    mask = post_fault_mask(fine_results["healthy"], config)
    structural_actuator_delta = (
        fine_results["structural"].gauge_microstrain[mask]
        - fine_results["actuator"].gauge_microstrain[mask]
    )
    structural_actuator_rms = rms(structural_actuator_delta)
    credible_floor = max(
        config.gauge_resolution_microstrain,
        config.thermal_cross_sensitivity_microstrain_per_c,
    )
    encoder_gauge_rms = float(np.max(fine_signatures["encoder"]["gauge_rms"]))
    encoder_imu_rms = float(np.max(fine_signatures["encoder"]["imu_rms"]))
    encoder_required = 0.8 * config.encoder_bias_rad
    gate: dict[str, Any] = {
        "credible_floor_microstrain": credible_floor,
        "structural_max_gauge_rms_microstrain": float(
            np.max(fine_signatures["structural"]["gauge_rms"])
        ),
        "actuator_max_gauge_rms_microstrain": float(
            np.max(fine_signatures["actuator"]["gauge_rms"])
        ),
        "structural_actuator_max_gauge_rms_microstrain": float(
            np.max(structural_actuator_rms)
        ),
        "encoder_q_rms_rad": float(np.max(fine_signatures["encoder"]["q_rms"])),
        "encoder_required_q_rms_rad": encoder_required,
        "encoder_physical_gauge_rms_microstrain": encoder_gauge_rms,
        "encoder_physical_imu_rms": encoder_imu_rms,
    }
    gate.update(
        {
            "structural_signal": gate["structural_max_gauge_rms_microstrain"]
            > credible_floor,
            "actuator_signal": gate["actuator_max_gauge_rms_microstrain"]
            > credible_floor,
            "structural_actuator_separation": gate[
                "structural_actuator_max_gauge_rms_microstrain"
            ]
            > credible_floor,
            "encoder_physical_gauge_unchanged": encoder_gauge_rms < 1.0e-6
            and encoder_imu_rms < 1.0e-6,
            "encoder_relational": gate["encoder_q_rms_rad"] >= encoder_required,
            "beam_strain": max(beam["gauge_relative_error"])
            <= config.max_beam_strain_relative_error,
            "beam_tip": beam["tip_relative_error"] <= config.max_beam_tip_relative_error,
        }
    )
    required_checks = [
        gate["structural_signal"],
        gate["actuator_signal"],
        gate["structural_actuator_separation"],
        gate["encoder_physical_gauge_unchanged"],
        gate["encoder_relational"],
        gate["beam_strain"],
        gate["beam_tip"],
        flex_probe["compiled"],
        flex_probe["finite_smoke_step"],
    ]
    if not quick:
        required_checks.extend([refinement["timestep_pass"], refinement["mesh_pass"]])
    gate["pass"] = bool(all(required_checks)) and not quick
    fine_point_count, fine_timestep_s = config_by_label[fine_label]
    internal_ball_joints_per_link = fine_point_count - 2

    summary = {
        "mujoco_version": mujoco.__version__,
        "quick": quick,
        "config": asdict(config),
        "simulation_configurations": {
            label: {"point_count": values[0], "timestep_s": values[1]}
            for label, values in config_by_label.items()
        },
        "max_connect_residual_m": {
            label: {
                scenario: result.max_connect_residual_m
                for scenario, result in cases.items()
            }
            for label, cases in results.items()
        },
        "fine_configuration": fine_label,
        "fine_metrics": fine_signatures,
        "structural_actuator_gauge_rms_microstrain": structural_actuator_rms,
        "refinement": refinement,
        "beam_validation": beam,
        "slender_3d_flex_probe": flex_probe,
        "candidate_contract": {
            "mechanics": "mujoco_native_cable_rod",
            "point_count_per_link": fine_point_count,
            "segment_count_per_link": fine_point_count - 1,
            "internal_ball_joints_per_link": internal_ball_joints_per_link,
            "deformation_coordinate_semantics": (
                "three-component log-map rotation vector for every internal "
                "ball joint; shoulder and elbow rigid-joint coordinates excluded"
            ),
            "n_def": 2 * 3 * internal_ball_joints_per_link,
            "gauge_stations": [
                {"link": 1, "normalized_position": 0.25},
                {"link": 1, "normalized_position": 0.75},
                {"link": 2, "normalized_position": 0.25},
                {"link": 2, "normalized_position": 0.75},
            ],
            "simulation_timestep_s": fine_timestep_s,
            "control_timestep_s": config.control_dt_s,
            "selection_condition": (
                "bounded_zero_mean_distal_diagnostic_excitation"
                if gate["pass"]
                else "not_selected"
            ),
        },
        "gate": gate,
        "candidate_decision": (
            "select_native_cable_rod"
            if gate["pass"]
            else "do_not_commit_native_candidate"
        ),
    }
    serializable = plain(summary)
    (output_dir / "summary.json").write_text(
        json.dumps(serializable, indent=2) + "\n", encoding="utf-8"
    )
    write_metrics_csv(output_dir / "signature_metrics.csv", signatures)
    plot_gauge_histories(
        output_dir / "gauge_fault_signatures.png",
        fine_results["healthy"],
        {name: fine_results[name] for name in scenarios[1:]},
        config,
    )
    plot_signature_heatmap(
        output_dir / "feature_signature_heatmap.png", fine_signatures
    )
    if not quick:
        write_report(output_dir / "feasibility_spike_report.md", serializable)
    print(
        f"Gate verdict: {'PASS' if gate['pass'] else 'BLOCK/SMOKE-ONLY'}; "
        f"outputs: {output_dir}",
        flush=True,
    )
    return serializable


def main() -> int:
    """Run the command-line feasibility spike and return a process status."""

    args = parse_args()
    config = SpikeConfig(
        duration_s=args.duration_s,
        fault_onset_s=args.fault_onset_s,
        control_dt_s=args.control_dt_s,
        diagnostic_tip_load_peak_n=args.diagnostic_tip_load_peak_n,
    )
    summary = run_gate(config, args.output_dir, quick=args.quick)
    return 0 if summary["gate"]["pass"] or args.quick else 2


if __name__ == "__main__":
    raise SystemExit(main())
