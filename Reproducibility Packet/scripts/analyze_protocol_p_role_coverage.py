"""Protocol P section 9: the role-coverage read over an executed Stage-A/B/C screen.

Section 9 pre-registers a read that the screen driver does not perform:

    Role coverage -- pre-declared, read before the ladder
    Count known-class testable structural settings per split and report the
    count 0/1/2.  OOD at 0.45/0.55 never counts.

        zero dev    -> no testable structural training support
        zero val    -> structural model selection / calibration unsupported
        zero test   -> four-way testable-stratum confirmatory metric undefined

    Any of those three zeroes yields a named role-coverage-bounded non-transfer
    outcome: the S/C1 secondary remains reportable, and it establishes neither
    success nor hypothesis failure.

The quantity is a deterministic function of two already-persisted documents -- the
executed screen's ladder verdicts and the bound assignment's per-split structural
severity grid -- so this step costs **zero rollouts** and never touches the
simulator.  It is a separate script rather than a driver change on purpose: adding
the read to the driver would leave the executed result artifact unable to carry it
without re-spending 135 physical rollouts to regenerate a number that the existing
artifact already determines.

The ladder is the union of every split's known-class structural severities and the
two structural OOD severities; that correspondence is asserted here rather than
assumed, so a future assignment that moves a severity off the ladder fails loudly
instead of silently reporting a zero count.

Outputs a JSON artifact and prints a human-readable summary to stdout.
"""

from __future__ import annotations

import argparse
import json
import math
from pathlib import Path
from typing import Any

from utils.gate3_assignment import expected_assignment_hash
from utils.protocol_p import (
    ASSIGNMENT_CANONICAL_SHA256,
    PROTOCOL_CANONICAL_SHA256,
    PROTOCOL_FILENAME,
    canonical_text_sha256,
    raw_file_sha256,
)

# Protocol P section 9 pins the OOD severities that never count toward coverage.
# Checked by EQUALITY against the assignment document, never adopted from it.
PROTOCOL_OOD_SEVERITIES = (0.45, 0.55)

# The three splits section 9 keys a named consequence to, and that consequence.
ZERO_CONSEQUENCES = {
    "dev": "no testable structural training support",
    "val": "structural model selection / calibration unsupported",
    "test": "four-way testable-stratum confirmatory metric undefined",
}

TESTABLE = "TESTABLE"
SUB_THRESHOLD = "SUB_THRESHOLD"
LADDER_VERDICTS = {TESTABLE, SUB_THRESHOLD}
SPLITS = ("dev", "pilot", "val", "test")


class RoleCoverageError(RuntimeError):
    """Raised when the inputs cannot support a section-9 role-coverage read."""


def require(condition: bool, message: str) -> None:
    """Raise ``RoleCoverageError`` with ``message`` unless ``condition`` holds.

    Never uses ``assert``: ``python -O`` removes assertions, and every decision
    bearing check in this project must survive optimized execution.
    """
    if not condition:
        raise RoleCoverageError(message)


class _StrictJSONError(ValueError):
    """Internal marker for duplicate keys and non-finite JSON constants."""


def load_json(path: Path, label: str) -> Any:
    """Load strict JSON at ``path``, failing loudly and naming ``label``."""
    if not path.is_file():
        raise RoleCoverageError(f"the {label} does not exist: {path}")

    def reject_constant(value: str) -> None:
        raise _StrictJSONError(f"non-finite JSON constant is forbidden: {value}")

    def unique_object(pairs: list[tuple[str, Any]]) -> dict[str, Any]:
        document: dict[str, Any] = {}
        for key, value in pairs:
            if key in document:
                raise _StrictJSONError(f"duplicate JSON key is forbidden: {key}")
            document[key] = value
        return document

    try:
        return json.loads(
            path.read_text(encoding="utf-8"),
            parse_constant=reject_constant,
            object_pairs_hook=unique_object,
        )
    except (json.JSONDecodeError, UnicodeDecodeError, _StrictJSONError) as exc:
        raise RoleCoverageError(f"the {label} is not strict JSON: {path}: {exc}") from exc


def validate_bound_inputs(screen: dict, assignment: dict) -> None:
    """Require the exact approved protocol/assignment state bound by the screen.

    A coverage count is a join between the ladder and the split assignment.  Without
    this check, a different assignment with the same ten-value union can change which
    split reads zero while the output still reports the approved assignment's hash.
    """
    require(isinstance(screen, dict), "the screen result must be a JSON object")
    require(isinstance(assignment, dict), "the assignment must be a JSON object")
    inputs = screen.get("inputs")
    protocol = screen.get("protocol")
    require(isinstance(inputs, dict), "the screen carries no inputs object")
    require(isinstance(protocol, dict), "the screen carries no protocol object")

    require(
        inputs.get("protocol_spec_sha256") == PROTOCOL_CANONICAL_SHA256,
        "the screen input protocol digest does not equal the approved Protocol P pin",
    )
    require(
        protocol.get("canonical_sha256") == PROTOCOL_CANONICAL_SHA256,
        "the screen protocol digest does not equal the approved Protocol P pin",
    )
    require(
        inputs.get("assignment_canonical_sha256") == ASSIGNMENT_CANONICAL_SHA256,
        "the screen assignment canonical digest does not equal the approved pin",
    )

    actual_assignment_hash = expected_assignment_hash(assignment)
    require(
        assignment.get("assignment_hash") == actual_assignment_hash,
        "the supplied assignment's self-hash is invalid",
    )
    require(
        inputs.get("assignment_hash") == actual_assignment_hash,
        "the supplied assignment does not equal the assignment bound by the screen",
    )


def ladder_verdicts(screen: dict) -> dict[float, str]:
    """Return ``{remaining_ei: verdict}`` from an executed screen artifact.

    Refuses a plan-mode artifact, a terminal run, and any ladder whose values are
    not ten distinct severities, because none of those can support the read.
    """
    require(screen.get("mode") == "execute",
            f"role coverage requires an executed screen; mode is {screen.get('mode')!r}")
    results = screen.get("results")
    require(isinstance(results, dict),
            "the screen artifact carries no results object; it was not executed")
    terminal = results.get("terminal")
    require(terminal is None,
            f"the screen terminated at {terminal!r}; section 9 requires all ten ladder "
            "values to have a safe, valid per-cell verdict before coverage is read")
    ladder = results.get("ladder")
    require(isinstance(ladder, list) and len(ladder) == 10,
            f"the ladder must carry exactly ten values; got "
            f"{len(ladder) if isinstance(ladder, list) else type(ladder).__name__}")

    verdicts: dict[float, str] = {}
    for row in ladder:
        require(isinstance(row, dict), "every ladder row must be an object")
        value = row.get("remaining_ei")
        verdict = row.get("verdict")
        require(isinstance(value, (int, float)) and not isinstance(value, bool),
                f"a ladder row has a non-numeric remaining_ei: {value!r}")
        require(math.isfinite(float(value)),
                f"a ladder row has a non-finite remaining_ei: {value!r}")
        require(isinstance(verdict, str) and verdict,
                f"the ladder row at {value!r} carries no verdict")
        require(verdict in LADDER_VERDICTS,
                f"the ladder row at {value!r} carries unknown verdict {verdict!r}")
        require(float(value) not in verdicts,
                f"the ladder repeats remaining_ei {value!r}")
        verdicts[float(value)] = verdict

    n_testable = sum(verdict == TESTABLE for verdict in verdicts.values())
    expected_case = (
        "CASE_A" if n_testable == len(verdicts)
        else "CASE_C" if n_testable == 0
        else "CASE_B"
    )
    require(results.get("outcome_case") == expected_case,
            f"the ladder verdicts imply {expected_case}, but the screen reports "
            f"{results.get('outcome_case')!r}")
    return verdicts


def structural_severities_by_split(assignment: dict) -> dict[str, list[float]]:
    """Return each split's known-class structural severities, ascending."""
    grid = assignment.get("fault_grid_by_split")
    require(isinstance(grid, dict) and grid,
            "the assignment carries no fault_grid_by_split object")
    require(set(grid) == set(SPLITS),
            f"fault_grid_by_split must define exactly {SPLITS}; got {sorted(grid)}")
    out: dict[str, list[float]] = {}
    for split in SPLITS:
        entry = grid[split]
        require(isinstance(entry, dict), f"split {split!r} must be an object")
        structure = entry.get("structure") or {}
        require(isinstance(structure, dict),
                f"split {split!r} structure must be an object")
        severities = structure.get("severities")
        require(isinstance(severities, list) and severities,
                f"split {split!r} carries no structural severity list")
        parsed: list[float] = []
        for severity in severities:
            require(isinstance(severity, (int, float)) and not isinstance(severity, bool),
                    f"split {split!r} has non-numeric structural severity {severity!r}")
            value = float(severity)
            require(math.isfinite(value),
                    f"split {split!r} has non-finite structural severity {severity!r}")
            parsed.append(value)
        require(len(parsed) == len(set(parsed)),
                f"split {split!r} repeats a structural severity")
        out[split] = sorted(parsed)
    return out


def structural_ood_severities(assignment: dict) -> list[float]:
    """Return the assignment's structural OOD severities, ascending.

    Read from the document and then checked for EQUALITY against the protocol's
    pinned pair by the caller; the document is never allowed to redefine the pin.
    """
    found: set[float] = set()
    for entry in assignment.get("compound_ood_settings") or []:
        label = entry.get("label") or {}
        if label.get("source_class") == "structure" and label.get("ood_flag"):
            found.add(float(label["severity"]))
        for component in entry.get("components") or []:
            if component.get("source_class") == "structure":
                found.add(float(component["severity"]))
    return sorted(found)


def compute_role_coverage(screen: dict, assignment: dict) -> dict:
    """Compute the section-9 role-coverage read. Costs zero rollouts."""
    validate_bound_inputs(screen, assignment)
    verdicts = ladder_verdicts(screen)
    by_split = structural_severities_by_split(assignment)
    ood = structural_ood_severities(assignment)

    require(tuple(ood) == PROTOCOL_OOD_SEVERITIES,
            f"the assignment's structural OOD severities {tuple(ood)} do not equal the "
            f"protocol's pinned {PROTOCOL_OOD_SEVERITIES}; section 9's "
            "'OOD at 0.45/0.55 never counts' no longer applies as written")

    known_union = sorted({s for sev in by_split.values() for s in sev})
    expected_ladder = sorted(set(known_union) | set(ood))
    require(expected_ladder == sorted(verdicts),
            "the ladder is not the union of the per-split known-class structural "
            f"severities and the structural OOD severities; ladder {sorted(verdicts)} "
            f"vs expected {expected_ladder}")

    splits: dict[str, dict] = {}
    for split in SPLITS:
        severities = by_split[split]
        known = [s for s in severities if s not in set(ood)]
        require(len(known) == 2,
                f"split {split!r} must have exactly two distinct known-class "
                f"structural severities; got {known}")
        testable = [s for s in known if verdicts[s] == TESTABLE]
        splits[split] = {
            "known_class_structural_severities": known,
            "testable_severities": testable,
            "count": len(testable),
            "verdicts": {str(s): verdicts[s] for s in known},
        }

    zeroed = [s for s in ("dev", "val", "test") if splits.get(s, {}).get("count") == 0]
    outcome = {
        "role_coverage_bounded_non_transfer": bool(zeroed),
        "zero_count_splits": zeroed,
        "named_consequences": [
            {"split": s, "consequence": ZERO_CONSEQUENCES[s]} for s in zeroed
        ],
        "authority": (
            "the S/C1 secondary remains reportable; a role-coverage-bounded "
            "non-transfer outcome establishes neither success nor hypothesis failure"
            if zeroed else
            "no split of dev/val/test is at zero; no role-coverage-bounded "
            "non-transfer outcome is triggered"
        ),
    }
    if splits.get("pilot", {}).get("count") == 0:
        outcome["pilot_note"] = (
            "zero pilot relabels nothing but disables data-driven downsizing, so the "
            "prospectively allowed maximum test replication is retained and the "
            "limitation is named"
        )
    thin = sorted(s for s, v in splits.items() if v["count"] == 1)
    if thin:
        outcome["thin_single_severity_roles"] = thin
        outcome["thin_note"] = (
            "count 1 is a thin single-severity role and opens no new terminal branch"
        )

    return {
        "purpose": (
            "Protocol P section 9 role-coverage read over an executed Stage-A/B/C "
            "screen. Derived from persisted results; zero rollouts."
        ),
        "inputs": {
            "screen_outcome_case": screen["results"].get("outcome_case"),
            "protocol_canonical_sha256": PROTOCOL_CANONICAL_SHA256,
            "assignment_hash": expected_assignment_hash(assignment),
            "assignment_canonical_sha256": ASSIGNMENT_CANONICAL_SHA256,
        },
        "rule": {
            "source": "Protocol P v2.3.3 section 9, 'Role coverage'",
            "ood_severities_excluded": list(PROTOCOL_OOD_SEVERITIES),
            "statement": (
                "count known-class testable structural settings per split and report "
                "the count 0/1/2; OOD at 0.45/0.55 never counts"
            ),
        },
        "ladder_verdicts": {str(k): verdicts[k] for k in sorted(verdicts)},
        "splits": splits,
        "outcome": outcome,
        "rollouts_spent": 0,
    }


def derive_role_coverage(screen_path: Path, assignment_path: Path) -> dict:
    """Load, bind, and derive one role-coverage artifact from tracked inputs."""
    screen_path = Path(screen_path)
    assignment_path = Path(assignment_path)
    screen = load_json(screen_path, "screen result")
    assignment = load_json(assignment_path, "assignment document")
    report = compute_role_coverage(screen, assignment)

    actual_assignment_digest = canonical_text_sha256(assignment_path)
    require(actual_assignment_digest == ASSIGNMENT_CANONICAL_SHA256,
            "the supplied assignment file does not equal the approved canonical state")
    protocol_path = Path(__file__).resolve().parents[1] / "protocol" / PROTOCOL_FILENAME
    actual_protocol_digest = canonical_text_sha256(protocol_path)
    require(actual_protocol_digest == PROTOCOL_CANONICAL_SHA256,
            "the tracked Protocol P file does not equal the approved canonical state")

    report["inputs"].update({
        "screen_result_raw_sha256": raw_file_sha256(screen_path),
        "assignment_canonical_sha256": actual_assignment_digest,
        "protocol_canonical_sha256": actual_protocol_digest,
    })
    return report


def render(report: dict) -> str:
    """Return the human-readable stdout summary for ``report``."""
    lines = ["Protocol P section 9 -- role coverage (zero rollouts)", ""]
    lines.append(f"screen outcome case: {report['inputs']['screen_outcome_case']}")
    lines.append("")
    lines.append(f"  {'split':>6}  {'known-class severities':<28} {'testable':<18} count")
    for split in ("dev", "pilot", "val", "test"):
        entry = report["splits"].get(split)
        if entry is None:
            continue
        known = ", ".join(f"{s:g}" for s in entry["known_class_structural_severities"])
        testable = ", ".join(f"{s:g}" for s in entry["testable_severities"]) or "-"
        lines.append(f"  {split:>6}  {known:<28} {testable:<18} {entry['count']}")
    lines.append("")
    outcome = report["outcome"]
    if outcome["role_coverage_bounded_non_transfer"]:
        lines.append("ROLE-COVERAGE-BOUNDED NON-TRANSFER OUTCOME")
        for named in outcome["named_consequences"]:
            lines.append(f"  zero {named['split']:<5} -> {named['consequence']}")
    else:
        lines.append("no role-coverage-bounded non-transfer outcome")
    if "pilot_note" in outcome:
        lines.append(f"  pilot: {outcome['pilot_note']}")
    if "thin_note" in outcome:
        lines.append(
            f"  thin single-severity roles {outcome['thin_single_severity_roles']}: "
            f"{outcome['thin_note']}")
    lines.append("")
    lines.append(f"  authority: {outcome['authority']}")
    return "\n".join(lines)


def main() -> None:
    """Parse arguments, compute the read, print it, and write the artifact."""
    parser = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    parser.add_argument("--screen-result", required=True,
                        help="path to an executed stage_abc_screen.json")
    parser.add_argument("--assignment", required=True,
                        help="path to the bound proposed-gate3-assignment JSON")
    parser.add_argument("--output-dir", required=True,
                        help="directory the role_coverage.json artifact is written to")
    args = parser.parse_args()

    report = derive_role_coverage(Path(args.screen_result), Path(args.assignment))
    print(render(report), flush=True)

    out_dir = Path(args.output_dir)
    out_dir.mkdir(parents=True, exist_ok=True)
    out_path = out_dir / "role_coverage.json"
    out_path.write_text(
        json.dumps(report, indent=1, sort_keys=True, ensure_ascii=False,
                   allow_nan=False) + "\n",
        encoding="utf-8", newline="\n")
    print(f"\nwrote {out_path}", flush=True)


if __name__ == "__main__":
    main()
