"""Generate the approved draft-authorized Gate-3 base research dataset."""

from __future__ import annotations

import argparse
import json
from pathlib import Path

from utils.assignment_binding import validate_approved_assignment_binding
from utils.assignment_generator import materialize_base_dataset
from utils.config_contract import load_config
from utils.gate3_assignment import load_assignment


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--schema", type=Path, default=Path("schema/schema.json"))
    parser.add_argument(
        "--config", type=Path, default=Path("config/draft-config-v0.1.json")
    )
    parser.add_argument(
        "--assignment",
        type=Path,
        default=Path("config/proposed-gate3-assignment-v0.1.json"),
    )
    parser.add_argument("--output", type=Path, required=True)
    parser.add_argument(
        "--splits",
        nargs="+",
        choices=("dev", "pilot", "val"),
        default=("dev", "pilot", "val"),
    )
    parser.add_argument(
        "--suites",
        nargs="+",
        choices=("C0", "C1", "S"),
        default=("C0", "C1", "S"),
    )
    parser.add_argument(
        "--reservation-limit",
        type=int,
        default=None,
        help="Smoke-only prefix limit; marks output non-research.",
    )
    parser.add_argument(
        "--max-steps",
        type=int,
        default=None,
        help="Smoke-only per-rollout truncation; marks output non-research.",
    )
    parser.add_argument(
        "--workers",
        type=int,
        default=1,
        help="Independent reservation workers; shared indexes are written serially.",
    )
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    if args.output.exists():
        raise FileExistsError(f"refusing to overwrite dataset root: {args.output}")
    schema = json.loads(args.schema.read_text(encoding="utf-8"))
    config = load_config(args.config, args.schema)
    assignment = load_assignment(args.assignment)
    binding = validate_approved_assignment_binding(
        config, expected_assignment=assignment
    )
    args.output.mkdir(parents=True)
    audit = materialize_base_dataset(
        binding,
        schema,
        args.output,
        splits=tuple(args.splits),
        suites=tuple(args.suites),
        reservation_limit=args.reservation_limit,
        max_steps=args.max_steps,
        workers=args.workers,
    )
    audit_path = args.output / "generation_audit.json"
    audit_path.write_text(
        json.dumps(audit, indent=2, sort_keys=True, allow_nan=False) + "\n",
        encoding="utf-8",
    )
    print(json.dumps(audit, indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
