"""Validate and summarize the proposed Gate-3 scenario/split assignment.

This command is read-only.  It expands reservations in memory, writes no
manifest or payload, and cannot authorize research or test generation.
"""

from __future__ import annotations

import argparse
import json
from pathlib import Path

from utils.config_contract import load_config
from utils.gate3_assignment import load_assignment, validate_assignment


def parse_args() -> argparse.Namespace:
    """Parse portable assignment, schema, and draft-config paths."""

    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--assignment",
        type=Path,
        default=Path("config/proposed-gate3-assignment-v0.1.json"),
        help="Proposed Gate-3 assignment document.",
    )
    parser.add_argument(
        "--schema",
        type=Path,
        default=Path("schema/schema.json"),
        help="Machine-readable schema authority.",
    )
    parser.add_argument(
        "--config",
        type=Path,
        default=Path("config/draft-config-v0.1.json"),
        help="Lifecycle-validated draft config bound by the assignment.",
    )
    return parser.parse_args()


def main() -> int:
    """Validate the proposal and print its deterministic audit summary."""

    args = parse_args()
    config = load_config(args.config, args.schema)
    assignment = load_assignment(args.assignment)
    summary = validate_assignment(assignment, config)
    print(json.dumps(summary, indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
