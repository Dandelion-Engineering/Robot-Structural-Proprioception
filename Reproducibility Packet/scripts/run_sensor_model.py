"""Apply the sensor-realism + fault-injection model to a privileged plant trace.

Reads a privileged plant record (schema B) and writes one deployable suite's
observed record (schema C) as a non-pickled `.npz`, plus a per-suite `index.csv`
row (`run_id, schema_version, config_hash, npz_path, sha256, split`) under
`<output-root>/observations/<suite>/` (schema section E, observations role).

A sensor-class fault (encoder bias / drift / dropout) may be injected into the
observation path only. Structural/actuator faults must already be present in the
input privileged trace (the plant lane owns them).

Example:
    python run_sensor_model.py --plant-npz results/synthetic_plant/healthy.npz \\
        --suite S --run-id demo_S --pair-id 1 --sensor-seed 7
"""

from __future__ import annotations

import argparse
import csv
import dataclasses
import hashlib
import json
from pathlib import Path

from utils.schema_types import PrivilegedRecord
from utils.sensor_model import FaultSpec, SensorConfig, SensorModel

_INDEX_FIELDS = ("run_id", "schema_version", "config_hash", "npz_path", "sha256", "split")


def parse_args() -> argparse.Namespace:
    """Parse command-line arguments for a portable sensor-model run."""

    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--plant-npz",
        type=Path,
        required=True,
        help="Path to the input privileged plant-record .npz (schema B).",
    )
    parser.add_argument(
        "--suite",
        choices=("C0", "C1", "S"),
        required=True,
        help="Deployable suite to generate (O is the separate oracle interface).",
    )
    parser.add_argument(
        "--output-root",
        type=Path,
        default=Path("results/sensor_model"),
        help="Project-relative output root; observations go under observations/<suite>/.",
    )
    parser.add_argument("--run-id", default="run", help="Rollout id (index key + file stem).")
    parser.add_argument("--pair-id", default="0", help="Matched C1-vs-S comparison id (CRN key).")
    parser.add_argument("--sensor-seed", type=int, default=0, help="Sensor seed (shared in a pair).")
    parser.add_argument(
        "--split",
        choices=("dev", "pilot", "val", "test"),
        default=None,
        help="Optional split assignment carried in the observation index.",
    )
    parser.add_argument(
        "--fault-class",
        choices=("healthy", "sensor"),
        default="healthy",
        help="Only sensor faults are applied here; physical faults live in the plant trace.",
    )
    parser.add_argument(
        "--fault-subtype",
        choices=("none", "encoder_bias", "encoder_drift", "encoder_dropout"),
        default="none",
    )
    parser.add_argument("--fault-location", type=int, default=0, help="Faulted joint index.")
    parser.add_argument("--fault-severity", type=float, default=0.0, help="Fault severity.")
    parser.add_argument("--fault-onset", type=int, default=-1, help="Onset control-step index.")
    return parser.parse_args()


def config_hash(config: SensorConfig) -> str:
    """Return a short stable hash of the sensor configuration for provenance."""

    payload = json.dumps(dataclasses.asdict(config), sort_keys=True).encode("utf-8")
    return hashlib.sha256(payload).hexdigest()[:16]


def sha256_file(path: Path) -> str:
    """Return the SHA-256 of a file's bytes (schema E integrity field)."""

    return hashlib.sha256(Path(path).read_bytes()).hexdigest()


def append_index_row(index_csv: Path, row: dict[str, str]) -> None:
    """Append one row to a per-suite observation index, writing a header if new."""

    write_header = not index_csv.exists()
    index_csv.parent.mkdir(parents=True, exist_ok=True)
    with index_csv.open("a", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=_INDEX_FIELDS)
        if write_header:
            writer.writeheader()
        writer.writerow(row)


def main() -> int:
    """Run the sensor model on one privileged trace and persist the observed record."""

    args = parse_args()
    if not args.plant_npz.exists():
        raise FileNotFoundError(f"privileged plant trace not found: {args.plant_npz}")

    print(f"Loading privileged trace {args.plant_npz} ...", flush=True)
    record = PrivilegedRecord.load_npz(args.plant_npz)
    record.validate()

    fault = FaultSpec(
        source_class=args.fault_class,
        subtype=args.fault_subtype,
        location=args.fault_location,
        severity=args.fault_severity,
        onset_index=args.fault_onset,
    )
    config = SensorConfig()
    model = SensorModel(config)
    hashed = config_hash(config)

    print(
        f"Applying sensor model: suite={args.suite}, fault={args.fault_class}/{args.fault_subtype}, "
        f"pair_id={args.pair_id}, sensor_seed={args.sensor_seed} ...",
        flush=True,
    )
    observed = model.observe(
        record,
        args.suite,
        pair_id=args.pair_id,
        sensor_seed=args.sensor_seed,
        fault=fault,
        run_id=args.run_id,
        config_hash=hashed,
        split=args.split,
    )

    suite_root = args.output_root / "observations" / args.suite
    npz_path = suite_root / f"{args.run_id}.npz"
    observed.save_npz(npz_path)
    append_index_row(
        suite_root / "index.csv",
        {
            "run_id": args.run_id,
            "schema_version": observed.schema_version,
            "config_hash": hashed,
            "npz_path": npz_path.name,  # relative to the suite root (self-contained loader)
            "sha256": sha256_file(npz_path),
            "split": args.split or "",
        },
    )
    print(
        f"Wrote {npz_path} and updated {suite_root / 'index.csv'} "
        f"(available channels: {', '.join(observed.available_channels)}).",
        flush=True,
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
