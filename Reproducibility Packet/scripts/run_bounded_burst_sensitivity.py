"""Screen bounded diagnostic bursts on the selected MuJoCo cable mechanics.

This is an early-Phase-2 sensitivity, not the confirmatory experiment. It holds the
selected 17-point/0.1-ms plant and fault severities fixed, compares one- and two-cycle
raised-cosine bursts against ordinary and continuous-excitation controls, and asks
whether the mechanics signature floor still clears under a finite probe budget.
"""

from __future__ import annotations

import argparse
import csv
import json
from dataclasses import asdict, dataclass, replace
from pathlib import Path
from typing import Any

import numpy as np

from run_feasibility_spike import SimulationResult, SpikeConfig, rms, simulate_case
from utils.cable_mechanics import diagnostic_tip_force_z


@dataclass(frozen=True)
class BurstCandidate:
    """One excitation condition and the post-onset interval used to screen it."""

    name: str
    config: SpikeConfig
    analysis_duration_s: float


def parse_args() -> argparse.Namespace:
    """Parse portable sensitivity-run arguments."""

    parser = argparse.ArgumentParser(
        description="Screen finite diagnostic bursts on the selected cable plant."
    )
    parser.add_argument(
        "--output-dir",
        type=Path,
        default=Path("results/bounded_burst_sensitivity"),
        help="Project-relative output directory.",
    )
    parser.add_argument("--fault-onset-s", type=float, default=1.0)
    parser.add_argument("--peak-load-n", type=float, default=1.0)
    parser.add_argument("--frequency-hz", type=float, default=0.8)
    parser.add_argument(
        "--cycles",
        type=int,
        nargs="+",
        default=[1, 2],
        help="Positive integer cycle counts to screen (default: 1 2).",
    )
    parser.add_argument(
        "--ramp-period-fraction",
        type=float,
        default=0.125,
        help="Raised-cosine ramp duration as a fraction of one probe period.",
    )
    parser.add_argument("--settle-s", type=float, default=0.25)
    parser.add_argument("--point-count", type=int, default=17)
    parser.add_argument("--simulation-timestep-s", type=float, default=1.0e-4)
    parser.add_argument(
        "--bounded-only",
        action="store_true",
        help="Skip ordinary/continuous controls (for a focused development rerun).",
    )
    return parser.parse_args()


def build_candidates(
    *,
    onset_s: float,
    peak_load_n: float,
    frequency_hz: float,
    cycles: list[int],
    ramp_period_fraction: float,
    settle_s: float,
    include_controls: bool = True,
) -> list[BurstCandidate]:
    """Build ordinary, continuous, and finite-cycle conditions on one duration grid."""

    if onset_s < 0.0 or not np.isfinite(onset_s):
        raise ValueError("onset_s must be finite and non-negative")
    if peak_load_n <= 0.0 or not np.isfinite(peak_load_n):
        raise ValueError("peak_load_n must be finite and positive")
    if frequency_hz <= 0.0 or not np.isfinite(frequency_hz):
        raise ValueError("frequency_hz must be finite and positive")
    if not cycles or any(not isinstance(value, int) or value <= 0 for value in cycles):
        raise ValueError("cycles must contain positive integers")
    if not 0.0 <= ramp_period_fraction <= 0.5:
        raise ValueError("ramp_period_fraction must lie in [0, 0.5]")
    if settle_s < 0.0 or not np.isfinite(settle_s):
        raise ValueError("settle_s must be finite and non-negative")

    period_s = 1.0 / frequency_hz
    max_burst_s = max(cycles) * period_s
    duration_s = onset_s + max_burst_s + settle_s
    base = SpikeConfig(
        duration_s=duration_s,
        fault_onset_s=onset_s,
        diagnostic_tip_load_peak_n=peak_load_n,
        diagnostic_tip_load_frequency_hz=frequency_hz,
    )
    candidates: list[BurstCandidate] = []
    if include_controls:
        candidates.extend(
            [
                BurstCandidate(
                    "ordinary_no_tip_load",
                    replace(base, diagnostic_tip_load_peak_n=0.0),
                    period_s,
                ),
                BurstCandidate("continuous_gate_load", base, period_s),
            ]
        )
    ramp_s = ramp_period_fraction * period_s
    for cycle_count in sorted(set(cycles)):
        burst_s = cycle_count * period_s
        candidates.append(
            BurstCandidate(
                f"bounded_{cycle_count}_cycle",
                replace(
                    base,
                    diagnostic_tip_load_start_s=onset_s,
                    diagnostic_tip_load_duration_s=burst_s,
                    diagnostic_tip_load_ramp_s=ramp_s,
                ),
                burst_s,
            )
        )
    return candidates


def analysis_mask(result: SimulationResult, onset_s: float, duration_s: float) -> np.ndarray:
    """Select the causal post-onset interval budget assigned to a condition."""

    end_s = onset_s + duration_s
    mask = (result.time_s >= onset_s - 1.0e-12) & (result.time_s <= end_s + 1.0e-12)
    if np.count_nonzero(mask) < 2:
        raise ValueError("analysis interval contains fewer than two control samples")
    return mask


def signature_screen(
    cases: dict[str, SimulationResult],
    config: SpikeConfig,
    analysis_duration_s: float,
) -> dict[str, Any]:
    """Evaluate the feasibility signature checks within one finite probe budget."""

    mask = analysis_mask(cases["healthy"], config.fault_onset_s, analysis_duration_s)
    healthy = cases["healthy"]
    deltas: dict[str, dict[str, np.ndarray]] = {}
    for scenario in ("structural", "actuator", "encoder"):
        fault = cases[scenario]
        deltas[scenario] = {
            "q": fault.q_obs_rad[mask] - healthy.q_obs_rad[mask],
            "imu": fault.imu[mask] - healthy.imu[mask],
            "gauge": fault.gauge_microstrain[mask] - healthy.gauge_microstrain[mask],
        }
    structural_actuator = (
        cases["structural"].gauge_microstrain[mask]
        - cases["actuator"].gauge_microstrain[mask]
    )
    floor = max(
        config.gauge_resolution_microstrain,
        config.thermal_cross_sensitivity_microstrain_per_c,
    )
    scenario_safety: dict[str, dict[str, float]] = {}
    for scenario, result in cases.items():
        scenario_mask = analysis_mask(result, config.fault_onset_s, analysis_duration_s)
        scenario_safety[scenario] = {
            "peak_abs_joint_angle_rad": float(np.max(np.abs(result.q_true_rad[scenario_mask]))),
            "peak_abs_joint_speed_rad_s": float(np.max(np.abs(result.qd_true_rad_s[scenario_mask]))),
            "peak_abs_gauge_microstrain": float(
                np.max(np.abs(result.gauge_microstrain[scenario_mask]))
            ),
            "peak_tip_radius_m": float(
                np.max(
                    np.linalg.norm(
                        result.tip_position_m[scenario_mask] - np.array([0.0, 0.0, 0.5]),
                        axis=1,
                    )
                )
            ),
        }
    metrics = {
        "analysis_samples": int(np.count_nonzero(mask)),
        "credible_floor_microstrain": float(floor),
        "structural_max_gauge_rms_microstrain": float(
            np.max(rms(deltas["structural"]["gauge"]))
        ),
        "actuator_max_gauge_rms_microstrain": float(
            np.max(rms(deltas["actuator"]["gauge"]))
        ),
        "structural_actuator_max_gauge_rms_microstrain": float(
            np.max(rms(structural_actuator))
        ),
        "encoder_q_rms_rad": float(np.max(rms(deltas["encoder"]["q"]))),
        "encoder_physical_gauge_rms_microstrain": float(
            np.max(rms(deltas["encoder"]["gauge"]))
        ),
        "encoder_physical_imu_rms": float(np.max(rms(deltas["encoder"]["imu"]))),
        "worst_peak_abs_joint_angle_rad": max(
            item["peak_abs_joint_angle_rad"] for item in scenario_safety.values()
        ),
        "worst_peak_abs_joint_speed_rad_s": max(
            item["peak_abs_joint_speed_rad_s"] for item in scenario_safety.values()
        ),
        "worst_peak_abs_gauge_microstrain": max(
            item["peak_abs_gauge_microstrain"] for item in scenario_safety.values()
        ),
        "worst_peak_tip_radius_m": max(
            item["peak_tip_radius_m"] for item in scenario_safety.values()
        ),
        "scenario_safety": scenario_safety,
    }
    safety_checks = {
        "joint_angle_limit_exceeded": bool(
            any(
                np.any(
                    np.abs(
                        result.q_true_rad[
                            analysis_mask(result, config.fault_onset_s, analysis_duration_s)
                        ]
                    )
                    > np.asarray(config.joint_angle_abs_limit_rad)[None, :]
                )
                for result in cases.values()
            )
        ),
        "joint_speed_limit_exceeded": bool(
            any(
                np.any(
                    np.abs(
                        result.qd_true_rad_s[
                            analysis_mask(result, config.fault_onset_s, analysis_duration_s)
                        ]
                    )
                    > np.asarray(config.joint_speed_abs_limit_rad_s)[None, :]
                )
                for result in cases.values()
            )
        ),
        "gauge_abs_limit_exceeded": bool(
            metrics["worst_peak_abs_gauge_microstrain"]
            > config.gauge_abs_limit_microstrain
        ),
        "tip_workspace_limit_exceeded": bool(
            metrics["worst_peak_tip_radius_m"] > config.tip_workspace_radius_limit_m
        ),
    }
    checks = {
        "structural_signal": metrics["structural_max_gauge_rms_microstrain"] > floor,
        "actuator_signal": metrics["actuator_max_gauge_rms_microstrain"] > floor,
        "structural_actuator_separation": (
            metrics["structural_actuator_max_gauge_rms_microstrain"] > floor
        ),
        "encoder_relational": metrics["encoder_q_rms_rad"] >= 0.8 * config.encoder_bias_rad,
        "encoder_physical_unchanged": (
            metrics["encoder_physical_gauge_rms_microstrain"] < 1.0e-6
            and metrics["encoder_physical_imu_rms"] < 1.0e-6
        ),
    }
    return {
        **metrics,
        "checks": checks,
        "mechanics_pass": bool(all(checks.values())),
        "safety_checks": safety_checks,
        "safety_screen_pass": not any(safety_checks.values()),
        "pass": bool(all(checks.values())) and not any(safety_checks.values()),
    }


def load_budget(config: SpikeConfig, timestep_s: float) -> dict[str, float]:
    """Summarize the declared probe's force/impulse budget on a fine time grid."""

    times = np.arange(0.0, config.duration_s + timestep_s / 2.0, timestep_s)
    force = np.asarray([diagnostic_tip_force_z(time, config) for time in times])
    return {
        "peak_abs_force_n": float(np.max(np.abs(force))),
        "signed_impulse_n_s": float(np.trapezoid(force, times)),
        "absolute_impulse_n_s": float(np.trapezoid(np.abs(force), times)),
        "force_rms_n": float(np.sqrt(np.mean(np.square(force)))),
    }


def plain(value: Any) -> Any:
    """Convert NumPy scalars/arrays recursively for JSON serialization."""

    if isinstance(value, dict):
        return {key: plain(item) for key, item in value.items()}
    if isinstance(value, (list, tuple)):
        return [plain(item) for item in value]
    if isinstance(value, np.ndarray):
        return value.tolist()
    if isinstance(value, np.generic):
        return value.item()
    return value


def write_csv(path: Path, results: list[dict[str, Any]]) -> None:
    """Write the decision-facing comparison table."""

    fields = [
        "name",
        "analysis_duration_s",
        "burst_duration_s",
        "ramp_s",
        "peak_abs_force_n",
        "signed_impulse_n_s",
        "structural_max_gauge_rms_microstrain",
        "actuator_max_gauge_rms_microstrain",
        "structural_actuator_max_gauge_rms_microstrain",
        "worst_peak_abs_joint_angle_rad",
        "worst_peak_abs_joint_speed_rad_s",
        "worst_peak_abs_gauge_microstrain",
        "worst_peak_tip_radius_m",
        "mechanics_pass",
        "safety_screen_pass",
        "pass",
    ]
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=fields)
        writer.writeheader()
        for result in results:
            screen = result["screen"]
            writer.writerow(
                {
                    "name": result["name"],
                    "analysis_duration_s": result["analysis_duration_s"],
                    "burst_duration_s": result["config"]["diagnostic_tip_load_duration_s"],
                    "ramp_s": result["config"]["diagnostic_tip_load_ramp_s"],
                    "peak_abs_force_n": result["load_budget"]["peak_abs_force_n"],
                    "signed_impulse_n_s": result["load_budget"]["signed_impulse_n_s"],
                    "structural_max_gauge_rms_microstrain": screen[
                        "structural_max_gauge_rms_microstrain"
                    ],
                    "actuator_max_gauge_rms_microstrain": screen[
                        "actuator_max_gauge_rms_microstrain"
                    ],
                    "structural_actuator_max_gauge_rms_microstrain": screen[
                        "structural_actuator_max_gauge_rms_microstrain"
                    ],
                    "worst_peak_abs_joint_angle_rad": screen[
                        "worst_peak_abs_joint_angle_rad"
                    ],
                    "worst_peak_abs_joint_speed_rad_s": screen[
                        "worst_peak_abs_joint_speed_rad_s"
                    ],
                    "worst_peak_abs_gauge_microstrain": screen[
                        "worst_peak_abs_gauge_microstrain"
                    ],
                    "worst_peak_tip_radius_m": screen["worst_peak_tip_radius_m"],
                    "mechanics_pass": screen["mechanics_pass"],
                    "safety_screen_pass": screen["safety_screen_pass"],
                    "pass": screen["pass"],
                }
            )


def write_report(path: Path, summary: dict[str, Any]) -> None:
    """Write a concise human-readable sensitivity decision record."""

    recommendation = summary["recommendation"]
    lines = [
        "# Bounded Diagnostic-Burst Sensitivity",
        "",
        f"**Decision: {recommendation['decision']}.** {recommendation['reason']}",
        "",
        "This is a mechanics/config sensitivity, not a research-hypothesis result and not a "
        "config freeze. It uses the already selected 17-point cable plant, fixed fault "
        "severities, and the same 10 microstrain credibility floor as the feasibility gate.",
        "",
        "| Condition | Probe budget | Structural RMS | Actuator RMS | Structure-actuator separation | Peak angle | Peak speed | Mechanics | Safety | Overall |",
        "|---|---:|---:|---:|---:|---:|---:|---|---|---|",
    ]
    for result in summary["results"]:
        screen = result["screen"]
        lines.append(
            f"| {result['name']} | {result['analysis_duration_s']:.3f} s | "
            f"{screen['structural_max_gauge_rms_microstrain']:.2f} microstrain | "
            f"{screen['actuator_max_gauge_rms_microstrain']:.2f} microstrain | "
            f"{screen['structural_actuator_max_gauge_rms_microstrain']:.2f} microstrain | "
            f"{screen['worst_peak_abs_joint_angle_rad']:.2f} rad | "
            f"{screen['worst_peak_abs_joint_speed_rad_s']:.2f} rad/s | "
            f"{'PASS' if screen['mechanics_pass'] else 'BLOCK'} | "
            f"{'PASS' if screen['safety_screen_pass'] else 'BLOCK'} | "
            f"{'PASS' if screen['pass'] else 'BLOCK'} |"
        )
    lines.extend(
        [
            "",
            "## Interpretation",
            "",
            "A bounded candidate passes this screen only if structure, actuator, and their "
            "difference each exceed the unchanged gauge credibility floor, while the encoder "
            "case remains relational (encoder changes; physical gauge/IMU history does not). "
            "The shortest passing bounded candidate is preferred for the pilot because the "
            "Claim Sheet requires informative excitation to be treated as a safety budget, not "
            "as free information.",
            "",
            "The estimator window remains a separate pilot choice: a mechanics PASS does not "
            "prove that `W=512` is optimal, and no current result promotes a development trace "
            "into confirmatory data.",
            "",
            "## Contact and safety role proposal (not frozen)",
            "",
            "- `contact_state` width **2**: `tip_contact_force_n`, `tip_contact_active`. "
            "The current no-contact plant writes zeros only after this role is implemented; "
            "an endpoint-contact pilot must populate both from MuJoCo contact truth.",
            "- `safety_flag` width **7**: two joint-angle flags, two joint-speed flags, "
            "one tip-workspace flag, one absolute-gauge-strain flag, and one tip-contact-force flag. "
            "Actuator saturation stays in the schema's separate two-wide `saturation_flag`.",
            f"- Provisional screening thresholds: `|q| <= pi rad` per joint; `|qd| <= "
            f"{summary['contact_safety_proposal']['thresholds']['joint_speed_abs_limit_rad_s'][0]:.0f} "
            f"rad/s` per joint; tip radius `<= "
            f"{summary['contact_safety_proposal']['thresholds']['tip_radius_limit_m']:.2f} m`; "
            f"`|gauge_true| <= "
            f"{summary['contact_safety_proposal']['thresholds']['gauge_abs_limit_microstrain']:.0f} "
            f"microstrain`; tip contact force `<= "
            f"{summary['contact_safety_proposal']['thresholds']['tip_contact_force_limit_n']:.0f} N`. "
            "These are a review proposal, "
            "not hardware claims or frozen values.",
            "",
            "The present sensitivity can evaluate the first six flags but not contact force, "
            "because the selected development MJCF still disables contact. A complete pilot "
            "configuration must implement the two-wide contact role and the seventh safety flag; "
            "zero-width arrays remain disallowed for pilot/confirmatory generation.",
        ]
    )
    path.write_text("\n".join(lines) + "\n", encoding="utf-8")


def run_sensitivity(
    candidates: list[BurstCandidate],
    output_dir: Path,
    *,
    point_count: int,
    simulation_timestep_s: float,
) -> dict[str, Any]:
    """Run all candidates, write artifacts, and return the serializable summary."""

    if point_count < 3:
        raise ValueError("point_count must be at least 3")
    if simulation_timestep_s <= 0.0 or not np.isfinite(simulation_timestep_s):
        raise ValueError("simulation_timestep_s must be finite and positive")
    output_dir.mkdir(parents=True, exist_ok=True)
    scenarios = ("healthy", "structural", "actuator", "encoder")
    results: list[dict[str, Any]] = []
    for candidate in candidates:
        print(f"Running {candidate.name} ...", flush=True)
        cases = {
            scenario: simulate_case(
                candidate.config, point_count, simulation_timestep_s, scenario
            )
            for scenario in scenarios
        }
        results.append(
            {
                "name": candidate.name,
                "analysis_duration_s": candidate.analysis_duration_s,
                "config": asdict(candidate.config),
                "load_budget": load_budget(candidate.config, simulation_timestep_s),
                "screen": signature_screen(
                    cases, candidate.config, candidate.analysis_duration_s
                ),
            }
        )

    bounded_passes = [
        result
        for result in results
        if result["name"].startswith("bounded_") and result["screen"]["pass"]
    ]
    bounded_passes.sort(key=lambda item: item["analysis_duration_s"])
    if bounded_passes:
        selected = bounded_passes[0]
        recommendation = {
            "decision": f"PILOT {selected['name']}",
            "candidate": selected["name"],
            "reason": (
                "It is the shortest screened finite, zero-mean raised-cosine burst that "
                "retains all mechanics signature checks. Freeze still awaits estimator/sensor "
                "and shared-grid convergence."
            ),
        }
    else:
        recommendation = {
            "decision": "NO BOUNDED CANDIDATE PASSES",
            "candidate": None,
            "reason": (
                "Do not freeze a diagnostic condition. Redesign the bounded probe/controller "
                "and implement the proposed safety roles before the pilot."
            ),
        }
    summary = plain(
        {
            "purpose": "development bounded-burst mechanics sensitivity; not confirmatory",
            "point_count": point_count,
            "simulation_timestep_s": simulation_timestep_s,
            "contact_safety_proposal": {
                "contact_state_fields": ["tip_contact_force_n", "tip_contact_active"],
                "safety_flag_fields": [
                    "joint_angle_0_exceeded",
                    "joint_angle_1_exceeded",
                    "joint_speed_0_exceeded",
                    "joint_speed_1_exceeded",
                    "tip_workspace_exceeded",
                    "gauge_abs_exceeded",
                    "tip_contact_force_exceeded",
                ],
                "thresholds": {
                    "joint_angle_abs_limit_rad": results[0]["config"]["joint_angle_abs_limit_rad"],
                    "joint_speed_abs_limit_rad_s": results[0]["config"]["joint_speed_abs_limit_rad_s"],
                    "tip_radius_limit_m": results[0]["config"]["tip_workspace_radius_limit_m"],
                    "gauge_abs_limit_microstrain": results[0]["config"]["gauge_abs_limit_microstrain"],
                    "tip_contact_force_limit_n": results[0]["config"]["tip_contact_force_limit_n"],
                },
                "status": "development proposal; same-state review and implementation required",
            },
            "results": results,
            "recommendation": recommendation,
        }
    )
    (output_dir / "summary.json").write_text(
        json.dumps(summary, indent=2) + "\n", encoding="utf-8"
    )
    write_csv(output_dir / "burst_sensitivity.csv", results)
    write_report(output_dir / "bounded_burst_report.md", summary)
    print(f"Decision: {recommendation['decision']}; outputs: {output_dir}", flush=True)
    return summary


def main() -> int:
    """Run the command-line sensitivity and return a process status."""

    args = parse_args()
    candidates = build_candidates(
        onset_s=args.fault_onset_s,
        peak_load_n=args.peak_load_n,
        frequency_hz=args.frequency_hz,
        cycles=args.cycles,
        ramp_period_fraction=args.ramp_period_fraction,
        settle_s=args.settle_s,
        include_controls=not args.bounded_only,
    )
    run_sensitivity(
        candidates,
        args.output_dir,
        point_count=args.point_count,
        simulation_timestep_s=args.simulation_timestep_s,
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
