"""Screen a bounded optional endpoint-contact profile before config freeze.

This development screen applies the pilot-advanced task/probe condition to an
ascending horizontal-plane grid.  It selects the lowest plane that produces one
brief post-onset endpoint-contact episode in every canonical source scenario,
without tripping any privileged A1 safety flag.  The sensor scenario deliberately
reuses the healthy physical trace because encoder corruption belongs exclusively
to the observation path under this open-loop command.  Its closed-loop contact
effect remains an evaluation item, not something this screen can claim.

The result is a profile candidate for matched pilot design only.  It does not
freeze the contact height, task/probe settings, fault grid, or ``config.json``.
"""

from __future__ import annotations

import argparse
import csv
import json
import math
from dataclasses import asdict, dataclass
from pathlib import Path
from typing import Any

import numpy as np

from utils.cable_mechanics import CableModelConfig
from utils.cable_plant import CablePlant
from utils.schema_types import SAFETY_FLAG_FIELDS, FaultSpec, PrivilegedRecord

CANONICAL_SCENARIOS = ("healthy", "structure", "actuator", "sensor")
PHYSICAL_SCENARIOS = ("healthy", "structure", "actuator")
EXTRACTION_FIXTURE_PLANE_Z_M = 0.498


@dataclass(frozen=True)
class ScreenSpec:
    """Portable mechanics and selection settings for the contact-profile screen."""

    plane_heights_z_m: tuple[float, ...] = (0.05, 0.075, 0.10, 0.125, 0.15)
    task_torque_scale: float = 0.50
    diagnostic_tip_load_peak_n: float = 0.05
    diagnostic_tip_load_frequency_hz: float = 0.8
    fault_onset_s: float = 1.0
    duration_s: float = 2.274
    ramp_period_fraction: float = 0.125
    control_dt_s: float = 0.002
    point_count: int = 17
    simulation_timestep_s: float = 1.0e-4
    minimum_contact_active_steps: int = 5
    maximum_contact_active_fraction: float = 0.05

    def validate(self) -> None:
        """Fail loudly when a screen or selection setting is malformed."""

        heights = np.asarray(self.plane_heights_z_m, dtype=float)
        if heights.ndim != 1 or heights.size < 2 or not np.all(np.isfinite(heights)):
            raise ValueError("plane_heights_z_m must contain at least two finite values")
        if not np.all(np.diff(heights) > 0.0):
            raise ValueError("plane_heights_z_m must be unique and strictly increasing")
        finite_positive = {
            "diagnostic_tip_load_frequency_hz": self.diagnostic_tip_load_frequency_hz,
            "duration_s": self.duration_s,
            "control_dt_s": self.control_dt_s,
            "simulation_timestep_s": self.simulation_timestep_s,
        }
        for name, value in finite_positive.items():
            if not np.isfinite(value) or value <= 0.0:
                raise ValueError(f"{name} must be finite and positive")
        if (
            not np.isfinite(self.task_torque_scale)
            or self.task_torque_scale < 0.0
            or not np.isfinite(self.diagnostic_tip_load_peak_n)
            or self.diagnostic_tip_load_peak_n < 0.0
        ):
            raise ValueError("task torque scale and diagnostic peak must be non-negative")
        if not np.isfinite(self.fault_onset_s) or self.fault_onset_s < 0.0:
            raise ValueError("fault_onset_s must be finite and non-negative")
        if not 0.0 <= self.ramp_period_fraction <= 0.5:
            raise ValueError("ramp_period_fraction must lie in [0, 0.5]")
        if self.point_count < 3:
            raise ValueError("point_count must be at least three")
        if self.minimum_contact_active_steps <= 0:
            raise ValueError("minimum_contact_active_steps must be positive")
        if not 0.0 < self.maximum_contact_active_fraction < 1.0:
            raise ValueError("maximum_contact_active_fraction must lie in (0, 1)")
        n_steps = self.duration_s / self.control_dt_s
        onset_steps = self.fault_onset_s / self.control_dt_s
        period_steps = (1.0 / self.diagnostic_tip_load_frequency_hz) / self.control_dt_s
        for name, value in {
            "duration/control_dt": n_steps,
            "fault_onset/control_dt": onset_steps,
            "probe_period/control_dt": period_steps,
        }.items():
            if not math.isclose(value, round(value), rel_tol=0.0, abs_tol=1.0e-10):
                raise ValueError(f"{name} must be an integer number of control steps")
        if self.fault_onset_s + 1.0 / self.diagnostic_tip_load_frequency_hz > self.duration_s:
            raise ValueError("duration_s must cover the complete one-cycle diagnostic probe")

    @property
    def n_steps(self) -> int:
        """Return the exact number of post-integration control samples."""

        return int(round(self.duration_s / self.control_dt_s))

    @property
    def onset_index(self) -> int:
        """Return the first control-step index whose physical fault is active."""

        return int(round(self.fault_onset_s / self.control_dt_s))

    @property
    def probe_period_s(self) -> float:
        """Return one diagnostic-probe period in seconds."""

        return 1.0 / self.diagnostic_tip_load_frequency_hz


def parse_args() -> argparse.Namespace:
    """Parse the portable contact-grid command-line interface."""

    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--output-dir",
        type=Path,
        default=Path("results/optional_contact_profile_screen"),
    )
    parser.add_argument(
        "--plane-heights-z-m",
        type=float,
        nargs="+",
        default=list(ScreenSpec().plane_heights_z_m),
    )
    parser.add_argument("--task-torque-scale", type=float, default=0.50)
    parser.add_argument("--diagnostic-tip-load-peak-n", type=float, default=0.05)
    parser.add_argument("--diagnostic-tip-load-frequency-hz", type=float, default=0.8)
    parser.add_argument("--fault-onset-s", type=float, default=1.0)
    parser.add_argument(
        "--duration-s",
        type=float,
        default=2.274,
        help="Development horizon through the pilot's first post-probe stride decision.",
    )
    parser.add_argument("--ramp-period-fraction", type=float, default=0.125)
    parser.add_argument("--control-dt-s", type=float, default=0.002)
    parser.add_argument("--point-count", type=int, default=17)
    parser.add_argument("--simulation-timestep-s", type=float, default=1.0e-4)
    parser.add_argument("--minimum-contact-active-steps", type=int, default=5)
    parser.add_argument("--maximum-contact-active-fraction", type=float, default=0.05)
    return parser.parse_args()


def spec_from_args(args: argparse.Namespace) -> ScreenSpec:
    """Build and validate a deterministic screen specification from CLI values."""

    spec = ScreenSpec(
        plane_heights_z_m=tuple(float(value) for value in args.plane_heights_z_m),
        task_torque_scale=float(args.task_torque_scale),
        diagnostic_tip_load_peak_n=float(args.diagnostic_tip_load_peak_n),
        diagnostic_tip_load_frequency_hz=float(args.diagnostic_tip_load_frequency_hz),
        fault_onset_s=float(args.fault_onset_s),
        duration_s=float(args.duration_s),
        ramp_period_fraction=float(args.ramp_period_fraction),
        control_dt_s=float(args.control_dt_s),
        point_count=int(args.point_count),
        simulation_timestep_s=float(args.simulation_timestep_s),
        minimum_contact_active_steps=int(args.minimum_contact_active_steps),
        maximum_contact_active_fraction=float(args.maximum_contact_active_fraction),
    )
    spec.validate()
    return spec


def physical_fault(scenario: str, onset_index: int) -> FaultSpec:
    """Return the physical plant fault for one canonical source scenario."""

    if scenario in {"healthy", "sensor"}:
        return FaultSpec()
    if scenario == "structure":
        return FaultSpec(
            source_class="structure",
            subtype="link_stiffness_loss",
            location=1,
            severity=0.50,
            onset_index=onset_index,
        )
    if scenario == "actuator":
        return FaultSpec(
            source_class="actuator",
            subtype="actuator_gain_loss",
            location=1,
            severity=0.70,
            onset_index=onset_index,
        )
    raise ValueError(f"unknown canonical scenario: {scenario}")


def count_contact_episodes(active: np.ndarray) -> int:
    """Count contiguous true runs in a one-dimensional contact-activity trace."""

    values = np.asarray(active)
    if values.ndim != 1 or values.dtype != np.bool_:
        raise ValueError("active must be a one-dimensional boolean array")
    if values.size == 0:
        return 0
    return int(values[0]) + int(np.count_nonzero(values[1:] & ~values[:-1]))


def summarize_record(
    record: PrivilegedRecord,
    *,
    plane_z_m: float,
    scenario: str,
    spec: ScreenSpec,
) -> dict[str, Any]:
    """Summarize contact exposure and all privileged A1 safety indicators."""

    force = np.asarray(record.contact_state[:, 0], dtype=float)
    active = np.asarray(record.contact_state[:, 1] == 1.0, dtype=bool)
    active_indices = np.flatnonzero(active)
    first_contact_s = (
        float(record.t_s[active_indices[0]]) if active_indices.size else None
    )
    last_contact_s = (
        float(record.t_s[active_indices[-1]]) if active_indices.size else None
    )
    contact_active_steps = int(active_indices.size)
    contact_active_fraction = float(np.mean(active))
    episode_count = count_contact_episodes(active)
    peak_force_n = float(np.max(force))
    contact_impulse_n_s = float(np.trapezoid(force, record.t_s))
    flag_counts = {
        name: int(np.count_nonzero(record.safety_flag[:, index]))
        for index, name in enumerate(SAFETY_FLAG_FIELDS)
    }
    any_safety_flag = bool(np.any(record.safety_flag))
    contact_gate_pass = bool(
        contact_active_steps >= spec.minimum_contact_active_steps
        and contact_active_fraction <= spec.maximum_contact_active_fraction
        and episode_count == 1
        and first_contact_s is not None
        and first_contact_s >= spec.fault_onset_s
        and peak_force_n < CableModelConfig().tip_contact_force_limit_n
        and not any_safety_flag
    )
    tip_radius = np.linalg.norm(record.true_task_output, axis=1)
    row: dict[str, Any] = {
        "plane_z_m": float(plane_z_m),
        "scenario": scenario,
        "plant_fault_source_class": physical_fault(scenario, spec.onset_index).source_class,
        "sensor_fault_is_observation_side": scenario == "sensor",
        "n_steps": int(record.n_steps),
        "contact_active_steps": contact_active_steps,
        "contact_active_fraction": contact_active_fraction,
        "contact_episode_count": episode_count,
        "first_contact_time_s": first_contact_s,
        "last_contact_time_s": last_contact_s,
        "peak_contact_force_n": peak_force_n,
        "contact_impulse_n_s": contact_impulse_n_s,
        "max_abs_joint_0_rad": float(np.max(np.abs(record.q_true[:, 0]))),
        "max_abs_joint_1_rad": float(np.max(np.abs(record.q_true[:, 1]))),
        "max_abs_joint_speed_0_rad_s": float(np.max(np.abs(record.qd_true[:, 0]))),
        "max_abs_joint_speed_1_rad_s": float(np.max(np.abs(record.qd_true[:, 1]))),
        "max_tip_workspace_radius_m": float(np.max(tip_radius)),
        "max_abs_gauge_microstrain": float(np.max(np.abs(record.gauge_true))),
        "safety_incident_steps": int(np.count_nonzero(np.any(record.safety_flag, axis=1))),
        "any_safety_flag": any_safety_flag,
        "contact_profile_gate_pass": contact_gate_pass,
    }
    row.update({f"flag_steps_{name}": count for name, count in flag_counts.items()})
    return row


def run_physical_scenario(
    plane_z_m: float, scenario: str, spec: ScreenSpec
) -> dict[str, Any]:
    """Run and summarize one physical open-loop contact-grid scenario."""

    if scenario not in PHYSICAL_SCENARIOS:
        raise ValueError(f"physical scenario must be one of {PHYSICAL_SCENARIOS}")
    config = CableModelConfig(
        control_dt_s=spec.control_dt_s,
        task_torque_scale=spec.task_torque_scale,
        diagnostic_tip_load_peak_n=spec.diagnostic_tip_load_peak_n,
        diagnostic_tip_load_frequency_hz=spec.diagnostic_tip_load_frequency_hz,
        diagnostic_tip_load_start_s=spec.fault_onset_s,
        diagnostic_tip_load_duration_s=spec.probe_period_s,
        diagnostic_tip_load_ramp_s=spec.probe_period_s * spec.ramp_period_fraction,
        endpoint_contact_enabled=True,
        endpoint_contact_plane_z_m=plane_z_m,
    )
    plant = CablePlant(
        config,
        point_count=spec.point_count,
        simulation_timestep_s=spec.simulation_timestep_s,
        fault=physical_fault(scenario, spec.onset_index),
    )
    return summarize_record(
        plant.rollout(spec.n_steps),
        plane_z_m=plane_z_m,
        scenario=scenario,
        spec=spec,
    )


def sensor_alias_row(healthy_row: dict[str, Any]) -> dict[str, Any]:
    """Copy healthy plant metrics for the observation-side sensor-fault scenario."""

    if healthy_row.get("scenario") != "healthy":
        raise ValueError("sensor alias requires a healthy physical row")
    row = dict(healthy_row)
    row["scenario"] = "sensor"
    row["plant_fault_source_class"] = "healthy"
    row["sensor_fault_is_observation_side"] = True
    return row


def select_candidate(rows: list[dict[str, Any]], spec: ScreenSpec) -> dict[str, Any]:
    """Apply the predeclared no-contact-control and lowest-eligible-height rule."""

    heights = list(spec.plane_heights_z_m)
    negative_height = heights[0]
    negative_rows = [row for row in rows if row["plane_z_m"] == negative_height]
    negative_control_pass = bool(
        len(negative_rows) == len(CANONICAL_SCENARIOS)
        and all(row["contact_active_steps"] == 0 for row in negative_rows)
        and all(not row["any_safety_flag"] for row in negative_rows)
    )
    eligible_heights: list[float] = []
    for height in heights[1:]:
        height_rows = [row for row in rows if row["plane_z_m"] == height]
        if (
            len(height_rows) == len(CANONICAL_SCENARIOS)
            and all(row["contact_profile_gate_pass"] for row in height_rows)
        ):
            eligible_heights.append(height)
    selected = eligible_heights[0] if negative_control_pass and eligible_heights else None
    return {
        "decision": (
            "ADVANCE_TO_MATCHED_OPTIONAL_CONTACT_PILOT_REVIEW"
            if selected is not None
            else "BLOCK_OPTIONAL_CONTACT_PROFILE"
        ),
        "selected_plane_z_m": selected,
        "negative_control_plane_z_m": negative_height,
        "negative_control_pass": negative_control_pass,
        "eligible_plane_heights_z_m": eligible_heights,
        "selection_rule": (
            "lowest plane above a zero-contact control with exactly one post-onset "
            "contact episode in every canonical scenario, at least the minimum active "
            "steps, no more than the maximum active fraction, peak force below the A1 "
            "limit, and no privileged safety flag"
        ),
    }


def run_screen(spec: ScreenSpec) -> dict[str, Any]:
    """Run the ascending contact grid and return the complete result payload."""

    spec.validate()
    rows: list[dict[str, Any]] = []
    for plane_z_m in spec.plane_heights_z_m:
        print(f"Screening endpoint plane z={plane_z_m:.3f} m ...", flush=True)
        height_rows: dict[str, dict[str, Any]] = {}
        for scenario in PHYSICAL_SCENARIOS:
            row = run_physical_scenario(plane_z_m, scenario, spec)
            height_rows[scenario] = row
            rows.append(row)
        rows.append(sensor_alias_row(height_rows["healthy"]))
    selection = select_candidate(rows, spec)
    return {
        "artifact_status": "development_only_config_unfrozen",
        "screen_spec": asdict(spec),
        "extraction_fixture_plane_z_m": EXTRACTION_FIXTURE_PLANE_Z_M,
        "extraction_fixture_excluded_from_candidate_grid": True,
        "sensor_scenario_boundary": (
            "encoder corruption is observation-side; under fixed open-loop commands its "
            "physical contact trace equals healthy. Closed-loop sensor-fault contact "
            "effects remain for the matched controller evaluation."
        ),
        "matched_suite_constraint": (
            "apply the selected contact setup identically to C1 and S within every "
            "matched pair; endogenous contact differences may then reflect recovery."
        ),
        "selection": selection,
        "rows": rows,
    }


def write_csv(path: Path, rows: list[dict[str, Any]]) -> None:
    """Write the scenario-level screen rows with a stable header."""

    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(rows[0]))
        writer.writeheader()
        writer.writerows(rows)


def write_report(path: Path, summary: dict[str, Any]) -> None:
    """Write a concise human-readable decision report from the JSON payload."""

    selection = summary["selection"]
    selected = selection["selected_plane_z_m"]
    rows = summary["rows"]
    selected_rows = [row for row in rows if row["plane_z_m"] == selected]
    lines = [
        "# Optional Endpoint-Contact Profile Screen",
        "",
        f"**Decision:** `{selection['decision']}`",
        "",
    ]
    if selected is not None:
        lines.extend(
            [
                (
                    f"The lowest eligible development plane is **z = {selected:.3f} m**. "
                    "It advances to matched optional-contact pilot review only. The height, "
                    "task/probe condition, faults, thresholds, and `config.json` remain unfrozen."
                ),
                "",
            ]
        )
    else:
        lines.extend(
            [
                "No plane in the declared grid cleared the development gate. Nothing advances.",
                "",
            ]
        )
    lines.extend(
        [
            "## Predeclared gate",
            "",
            f"- Grid: `{summary['screen_spec']['plane_heights_z_m']}` m.",
            f"- Lowest plane is a required zero-contact control: **{selection['negative_control_pass']}**.",
            f"- Each candidate scenario needs exactly one post-onset episode, at least "
            f"{summary['screen_spec']['minimum_contact_active_steps']} active steps, no more than "
            f"{100.0 * summary['screen_spec']['maximum_contact_active_fraction']:.1f}% active steps, "
            "peak force below 5 N, and no A1 safety flag.",
            f"- The earlier z = {summary['extraction_fixture_plane_z_m']:.3f} m extraction fixture "
            "is explicitly excluded from this candidate grid.",
            "",
            "## Selected-profile scenario audit",
            "",
            "| Scenario | Active steps | Active fraction | Episode | First contact (s) | Peak force (N) | Impulse (N s) | Safety steps |",
            "|---|---:|---:|---:|---:|---:|---:|---:|",
        ]
    )
    for row in selected_rows:
        first = row["first_contact_time_s"]
        lines.append(
            f"| {row['scenario']} | {row['contact_active_steps']} | "
            f"{100.0 * row['contact_active_fraction']:.2f}% | "
            f"{row['contact_episode_count']} | {first:.3f} | "
            f"{row['peak_contact_force_n']:.3f} | {row['contact_impulse_n_s']:.5f} | "
            f"{row['safety_incident_steps']} |"
        )
    lines.extend(
        [
            "",
            "## Boundaries",
            "",
            "- This is an open-loop mechanics/safety screen under the pilot-advanced task/probe, not a C1-vs-S result.",
            "- The sensor row aliases healthy physical truth because encoder corruption is injected only after the plant. Its closed-loop effect on commands/contact is still open.",
            "- A later matched comparison must apply the same contact profile to C1 and S within each CRN pair.",
            "- No profile, grid, threshold, severity/onset setting, or immutable config is frozen by this artifact.",
            "",
        ]
    )
    path.write_text("\n".join(lines), encoding="utf-8")


def main() -> int:
    """Run the default screen and write JSON, CSV, and Markdown artifacts."""

    args = parse_args()
    spec = spec_from_args(args)
    summary = run_screen(spec)
    args.output_dir.mkdir(parents=True, exist_ok=True)
    summary_path = args.output_dir / "summary.json"
    csv_path = args.output_dir / "contact_profile_grid.csv"
    report_path = args.output_dir / "optional_contact_profile_report.md"
    summary_path.write_text(json.dumps(summary, indent=2) + "\n", encoding="utf-8")
    write_csv(csv_path, summary["rows"])
    write_report(report_path, summary)
    print(
        f"{summary['selection']['decision']}: "
        f"selected z={summary['selection']['selected_plane_z_m']} m; "
        f"wrote {args.output_dir}",
        flush=True,
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
