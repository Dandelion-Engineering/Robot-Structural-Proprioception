"""Independently audit an approved Gate-3 base dataset already on disk."""

from __future__ import annotations

import argparse
import json
from pathlib import Path

from utils.assignment_binding import validate_approved_assignment_binding
from utils.assignment_generator import audit_materialized_base_dataset
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
    parser.add_argument("--dataset-root", type=Path, required=True)
    parser.add_argument(
        "--output",
        type=Path,
        default=None,
        help="Optional JSON audit artifact; refuses to overwrite.",
    )
    parser.add_argument(
        "--allow-partial",
        action="store_true",
        help="Audit a smoke prefix without claiming complete research data.",
    )
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    schema = json.loads(args.schema.read_text(encoding="utf-8"))
    config = load_config(args.config, args.schema)
    assignment = load_assignment(args.assignment)
    binding = validate_approved_assignment_binding(
        config, expected_assignment=assignment
    )
    audit = audit_materialized_base_dataset(
        binding,
        schema,
        args.dataset_root,
        allow_partial=args.allow_partial,
    )
    rendered = json.dumps(audit, indent=2, sort_keys=True) + "\n"
    if args.output is not None:
        if args.output.exists():
            raise FileExistsError(f"refusing to overwrite audit artifact: {args.output}")
        args.output.parent.mkdir(parents=True, exist_ok=True)
        args.output.write_text(rendered, encoding="utf-8")
    print(rendered, end="")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
