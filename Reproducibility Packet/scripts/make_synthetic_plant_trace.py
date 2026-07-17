"""Generate a synthetic privileged plant trace (schema B) for sensor-lane testing.

DEVELOPMENT / TEST FIXTURE (see `utils/synthetic_plant.py`): writes a
schema-conforming `PrivilegedRecord` built from analytic signals, so the sensor
model can be exercised end-to-end before the plant lane's real MuJoCo trace
exists. This is not part of the confirmatory pipeline and makes no physical claim.

Example:
    python make_synthetic_plant_trace.py --output-npz results/synthetic_plant/healthy.npz
"""

from __future__ import annotations

import argparse
from pathlib import Path

from utils.schema_types import DEFAULT_N_DEF
from utils.sensor_model import FaultSpec
from utils.synthetic_plant import synthetic_privileged_record


def parse_args() -> argparse.Namespace:
    """Parse command-line arguments for the synthetic plant-trace generator."""

    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--output-npz",
        type=Path,
        default=Path("results/synthetic_plant/healthy.npz"),
        help="Project-relative output path for the privileged .npz trace.",
    )
    parser.add_argument("--n-steps", type=int, default=1500, help="Number of control steps T.")
    parser.add_argument("--f-ctrl", type=float, default=500.0, help="Control rate (Hz).")
    parser.add_argument("--n-def", type=int, default=DEFAULT_N_DEF, help="Deformation-coord count.")
    parser.add_argument("--seed", type=int, default=0, help="Deterministic analytic-phase seed.")
    parser.add_argument(
        "--thermal-ramp-c",
        type=float,
        default=0.0,
        help="Linear temperature rise (deg C) over the rollout, for thermal testing.",
    )
    parser.add_argument(
        "--fault-class",
        choices=("healthy", "structure", "actuator"),
        default="healthy",
        help="Physical fault to bake into the privileged truth (sensor faults are "
        "applied by the sensor model, not here).",
    )
    parser.add_argument("--fault-location", type=int, default=-1, help="Joint/station index.")
    parser.add_argument("--fault-severity", type=float, default=0.0, help="Fault severity.")
    parser.add_argument("--fault-onset", type=int, default=-1, help="Onset control-step index.")
    return parser.parse_args()


def main() -> int:
    """Generate and persist one synthetic privileged plant trace."""

    args = parse_args()
    fault = FaultSpec(
        source_class=args.fault_class,
        subtype="none",
        location=args.fault_location,
        severity=args.fault_severity,
        onset_index=args.fault_onset,
    )
    print(
        f"Generating synthetic plant trace: T={args.n_steps}, f_ctrl={args.f_ctrl} Hz, "
        f"n_def={args.n_def}, fault={args.fault_class} ...",
        flush=True,
    )
    record = synthetic_privileged_record(
        n_steps=args.n_steps,
        f_ctrl=args.f_ctrl,
        n_def=args.n_def,
        seed=args.seed,
        fault=fault,
        thermal_ramp_c=args.thermal_ramp_c,
    )
    record.save_npz(args.output_npz)
    print(f"Wrote {args.output_npz} ({record.n_steps} steps, n_def={record.n_def}).", flush=True)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
