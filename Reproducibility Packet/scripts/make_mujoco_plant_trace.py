"""Generate a real schema-B privileged trace from the selected MuJoCo plant.

This is an open-loop development producer for interface integration, not a
confirmatory rollout and not the final closed-loop controller. It persists only
the privileged `plant/` role; faults/labels remain separate by construction.
"""

from __future__ import annotations

import argparse
import csv
import dataclasses
import hashlib
import json
import math
from pathlib import Path

import numpy as np

from utils.cable_mechanics import CableModelConfig
from utils.cable_plant import CablePlant
from utils.schema_types import FaultSpec, SCHEMA_VERSION

_INDEX_FIELDS = ("run_id", "schema_version", "config_hash", "npz_path", "sha256")


def parse_args() -> argparse.Namespace:
    """Parse portable development-rollout arguments."""

    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--output-root",
        type=Path,
        default=Path("results/mujoco_plant"),
        help="Output root; the privileged role is written under plant/.",
    )
    parser.add_argument("--run-id", default="plant_dev", help="Opaque rollout id / file stem.")
    parser.add_argument("--duration-s", type=float, default=3.0)
    parser.add_argument("--control-dt-s", type=float, default=0.002)
    parser.add_argument("--simulation-timestep-s", type=float, default=1.0e-4)
    parser.add_argument("--point-count", type=int, default=17)
    parser.add_argument(
        "--scenario", choices=("healthy", "structure", "actuator"), default="healthy"
    )
    parser.add_argument(
        "--fault-onset-s",
        type=float,
        default=1.0,
        help="Time of the first affected persisted control sample.",
    )
    parser.add_argument(
        "--fault-severity",
        type=float,
        default=None,
        help="Remaining EI/gain fraction; defaults to 0.50 (structure) or 0.70 (actuator).",
    )
    parser.add_argument("--diagnostic-tip-load-peak-n", type=float, default=1.0)
    parser.add_argument("--diagnostic-tip-load-frequency-hz", type=float, default=0.8)
    parser.add_argument(
        "--endpoint-contact-plane-z-m",
        type=float,
        default=None,
        help=(
            "Enable the development endpoint-contact profile against a horizontal "
            "plane at this world-z coordinate; omitted keeps collision disabled."
        ),
    )
    parser.add_argument(
        "--thermal-ramp-c",
        type=float,
        default=0.0,
        help="Linear temperature rise across the development trace.",
    )
    return parser.parse_args()


def file_sha256(path: Path) -> str:
    """Return the SHA-256 digest of a persisted payload."""

    return hashlib.sha256(Path(path).read_bytes()).hexdigest()


def development_config_hash(config: CableModelConfig, args: argparse.Namespace) -> str:
    """Hash shared plant-development config, excluding the selected run/fault spec."""

    payload = {
        "config": dataclasses.asdict(config),
        "point_count": args.point_count,
        "simulation_timestep_s": args.simulation_timestep_s,
    }
    digest = hashlib.sha256(json.dumps(payload, sort_keys=True).encode("utf-8")).hexdigest()
    return f"dev-{digest[:16]}"


def append_index_row(index_csv: Path, row: dict[str, str]) -> None:
    """Append one schema-E plant-role index row, adding the header if needed."""

    write_header = not index_csv.exists()
    index_csv.parent.mkdir(parents=True, exist_ok=True)
    with index_csv.open("a", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=_INDEX_FIELDS)
        if write_header:
            writer.writeheader()
        writer.writerow(row)


def fault_from_args(args: argparse.Namespace, onset_index: int) -> FaultSpec:
    """Build the physical fault specification without creating a label payload."""

    if args.scenario == "healthy":
        return FaultSpec()
    if args.scenario == "structure":
        return FaultSpec(
            source_class="structure",
            subtype="link_stiffness_loss",
            location=1,
            severity=args.fault_severity if args.fault_severity is not None else 0.50,
            onset_index=onset_index,
        )
    return FaultSpec(
        source_class="actuator",
        subtype="actuator_gain_loss",
        location=1,
        severity=args.fault_severity if args.fault_severity is not None else 0.70,
        onset_index=onset_index,
    )


def main() -> int:
    """Run the real plant producer and persist one role-separated trace."""

    args = parse_args()
    if args.duration_s <= 0.0 or args.control_dt_s <= 0.0:
        raise ValueError("duration-s and control-dt-s must be positive")
    n_steps = int(round(args.duration_s / args.control_dt_s))
    if n_steps <= 0:
        raise ValueError("duration is shorter than one control interval")
    # The plant stores post-integration samples: step 0 is at dt, so the sample
    # at 1.000 s is index 499 for dt=0.002 s.
    onset_index = max(0, int(math.ceil(args.fault_onset_s / args.control_dt_s)) - 1)
    fault = fault_from_args(args, onset_index)
    default_config = CableModelConfig()
    config = CableModelConfig(
        control_dt_s=args.control_dt_s,
        diagnostic_tip_load_peak_n=args.diagnostic_tip_load_peak_n,
        diagnostic_tip_load_frequency_hz=args.diagnostic_tip_load_frequency_hz,
        endpoint_contact_enabled=args.endpoint_contact_plane_z_m is not None,
        endpoint_contact_plane_z_m=(
            args.endpoint_contact_plane_z_m
            if args.endpoint_contact_plane_z_m is not None
            else default_config.endpoint_contact_plane_z_m
        ),
    )
    plant = CablePlant(
        config,
        point_count=args.point_count,
        simulation_timestep_s=args.simulation_timestep_s,
        fault=fault,
    )

    def temperature(index: int, _time_s: float) -> np.ndarray:
        """Return the requested deterministic four-station development ramp."""

        fraction = index / max(n_steps - 1, 1)
        return np.full(4, 25.0 + args.thermal_ramp_c * fraction)

    print(
        f"Generating {args.scenario} MuJoCo plant trace: {n_steps} steps, "
        f"f_ctrl={1.0 / args.control_dt_s:.1f} Hz, n_def={plant.n_def} ...",
        flush=True,
    )
    record = plant.rollout(n_steps, temperature_fn=temperature)
    hashed = development_config_hash(config, args)
    plant_root = args.output_root / "plant"
    npz_path = plant_root / f"{args.run_id}.npz"
    record.save_npz(npz_path)
    append_index_row(
        plant_root / "index.csv",
        {
            "run_id": args.run_id,
            "schema_version": SCHEMA_VERSION,
            "config_hash": hashed,
            "npz_path": npz_path.name,
            "sha256": file_sha256(npz_path),
        },
    )
    print(
        f"Wrote {npz_path} and {plant_root / 'index.csv'} "
        f"(config_hash={hashed}; development/unfrozen).",
        flush=True,
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
