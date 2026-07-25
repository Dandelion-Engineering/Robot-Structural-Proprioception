"""Embed the exact jointly approved Gate-3 assignment into the draft config.

The command removes only the Gate-3 open-gate item, preserves the assignment
unchanged inside a one-way approval wrapper, and recomputes the draft config
hash. It never creates ``config.json`` and never authorizes test materialization.
"""

from __future__ import annotations

import argparse
import json
from pathlib import Path

from utils.assignment_binding import (
    embed_approved_assignment_document,
    validate_approved_assignment_binding,
)
from utils.config_contract import load_config
from utils.gate3_assignment import load_assignment


def parse_args() -> argparse.Namespace:
    """Parse portable schema/config/assignment paths and output destination."""

    parser = argparse.ArgumentParser(description=__doc__)
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
        help="Parent draft config with a null scenario_manifest.",
    )
    parser.add_argument(
        "--assignment",
        type=Path,
        default=Path("config/proposed-gate3-assignment-v0.1.json"),
        help="Exact jointly approved Gate-3 assignment.",
    )
    parser.add_argument(
        "--output",
        type=Path,
        default=None,
        help="Output draft path; defaults to an atomic in-place update of --config.",
    )
    return parser.parse_args()


def main() -> int:
    """Embed, atomically write, reload, and print the validated binding summary."""

    args = parse_args()
    parent = load_config(args.config, args.schema)
    assignment = load_assignment(args.assignment)
    document = embed_approved_assignment_document(parent, assignment)
    output = args.output or args.config
    if output.name.lower() == "config.json":
        raise ValueError("approved assignment embedding must not create config.json")
    if output.exists() and output.resolve() != args.config.resolve():
        raise FileExistsError(f"refusing to overwrite output draft: {output}")
    output.parent.mkdir(parents=True, exist_ok=True)
    temporary = output.with_name(f".{output.name}.tmp")
    if temporary.exists():
        raise FileExistsError(f"temporary output already exists: {temporary}")
    temporary.write_text(
        json.dumps(document, indent=2, ensure_ascii=False, allow_nan=False) + "\n",
        encoding="utf-8",
    )
    temporary.replace(output)

    current = load_config(output, args.schema)
    binding = validate_approved_assignment_binding(
        current,
        expected_assignment=assignment,
    )
    summary = {
        "status": "jointly_approved_assignment_embedded",
        "assignment_hash": binding.assignment_hash,
        "parent_draft_config_hash": binding.parent_config.config_hash,
        "current_draft_config_hash": current.config_hash,
        "research_splits_authorized": list(binding.authorized_research_splits),
        "test_materialization_allowed": False,
        "total_reservations": binding.proposal_audit["total_reservations"],
    }
    print(json.dumps(summary, indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
