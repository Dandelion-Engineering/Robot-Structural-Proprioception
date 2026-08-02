"""Post-hoc diagnostic: how the Stage-B margin depends on distal payload mass.

**This read is NOT pre-registered.**  Protocol P section 9 pins two reads over the
executed Stage-A/B/C screen -- the ladder outcome case and the role-coverage count --
and this is neither of them.  It classifies nothing, it opens no terminal branch, and
it cannot move any Protocol-P outcome.  Its ``authority`` field says so in the
artifact, on the Stage-0 ``corroboration.authority = "NONE"`` precedent.

What it is for.  Section 8 runs the ladder in four development context cells, and
those four cells are not exchangeable: the balanced context table gives cells 4 and 5
the ``payload_dev_nominal`` (0.000 kg) profile and cells 6 and 7 the
``payload_dev_0p050kg`` (0.050 kg) profile, while temperature environment and contact
profile vary *within* each payload level.  So the screen already contains a two-level
contrast in distal payload mass, balanced against the other two context factors, at
every one of the ten ladder values -- and the aggregation rule is the conjunction over
all four cells, which means the heavier level decides every verdict it loses.

That contrast matters beyond the screen because payload mass is the one context factor
whose reserved values move monotonically across splits: dev {0.000, 0.050},
pilot {0.025, 0.075}, val {0.100, 0.125}, test {0.150, 0.200} kg.  The screen was run,
by section 8's own boundary, on development contexts only.  Any statement that a
ladder value is "testable" is therefore established at 0.000 and 0.050 kg and at no
other mass, and this read exists to make the size of that restriction visible instead
of leaving it as a sentence nobody has attached a number to.

What it computes, all from documents already persisted, at **zero rollouts**:

* each cell's payload / environment / contact profile, derived from the assignment
  through the reservation the screen's own ledger recorded, and then checked for
  EQUALITY against the masses Protocol P section 8 pins in prose;
* per ladder value, the mean structural distance ``d`` at each payload level and the
  ratio between them -- the measured attenuation;
* the operative null ``Q95_c`` at each payload level, which is what tells you whether
  the attenuation is a signal effect or a noise effect;
* per cell, the bracket in which that cell's margin crosses zero, i.e. the severity
  boundary this excitation buys at that payload;
* which splits carry payload masses outside the screened range.

Deliberate non-goals, because each would be a claim the data cannot carry:

* **No functional form.** Two payload levels determine a ratio and nothing else.  The
  artifact reports the ratio; it does not fit, extrapolate, or predict a margin at any
  mass that was not run.
* **No re-classification.** The ladder verdicts stand exactly as the screen recorded
  them.  This read never recomputes a verdict.
* **The zero crossing is reported as a BRACKET.**  A linear interpolation inside the
  bracket is included, labelled as an interpolation of a quantity that is not known to
  be linear in remaining EI, and it is not used for anything.

Outputs a JSON artifact and prints a human-readable summary to stdout.
"""

from __future__ import annotations

import argparse
import json
import math
from pathlib import Path
from typing import Any

from utils.gate3_assignment import expand_reservations
from utils.protocol_p import (
    ASSIGNMENT_CANONICAL_SHA256,
    PROTOCOL_CANONICAL_SHA256,
    PROTOCOL_FILENAME,
    canonical_text_sha256,
)

# Protocol P v2.3.3 section 8, lines 520-523, pins the four screened context cells in
# prose:
#     cell 4 = r00   payload 0.000 kg   iso25c   contact brief
#     cell 5 = r01   payload 0.000 kg   warm2c   contact none
#     cell 6 = r02   payload 0.050 kg   iso25c   contact none
#     cell 7 = r03   payload 0.050 kg   warm2c   contact brief
# These are checked by EQUALITY against the masses derived from the assignment through
# the screen's own ledger, never adopted from either side (the section-47 rule).
PROTOCOL_CELL_PAYLOAD_KG = {4: 0.000, 5: 0.000, 6: 0.050, 7: 0.050}

# The screen's four cells, in section 8's order.
SCREEN_CELLS = (4, 5, 6, 7)

SPLITS = ("dev", "pilot", "val", "test")

TESTABLE = "TESTABLE"
SUB_THRESHOLD = "SUB_THRESHOLD"
LADDER_VERDICTS = {TESTABLE, SUB_THRESHOLD}

# Mass comparisons are made on a fixed grid of reserved profile values, so an exact
# tolerance is appropriate; this guards against a float that merely renders the same.
MASS_TOLERANCE_KG = 1e-12

# Persisted decision-bearing floats are generated from the same operands written into
# the result artifact.  This tolerance accepts serialization round-off while refusing
# a stored margin, threshold, or null that represents a different calculation.
NUMERIC_TOLERANCE = 1e-12


class PayloadConditioningError(RuntimeError):
    """Raised when the inputs cannot support the payload-conditioning read."""


def require(condition: bool, message: str) -> None:
    """Raise ``PayloadConditioningError`` with ``message`` unless ``condition`` holds.

    Never uses ``assert``: ``python -O`` removes assertions, and every decision
    bearing check in this project must survive optimized execution.
    """
    if not condition:
        raise PayloadConditioningError(message)


class _StrictJSONError(ValueError):
    """Internal marker for duplicate keys and non-finite JSON constants."""


def load_json(path: Path, label: str) -> Any:
    """Load strict JSON at ``path``, failing loudly and naming ``label``."""
    if not path.is_file():
        raise PayloadConditioningError(f"the {label} does not exist: {path}")

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
        raise PayloadConditioningError(
            f"the {label} is not strict JSON: {path}: {exc}"
        ) from exc


def require_finite_number(value: Any, description: str) -> float:
    """Return ``value`` as a float, refusing bools, non-numbers and non-finite values."""
    require(isinstance(value, (int, float)) and not isinstance(value, bool),
            f"{description} must be a number; got {value!r}")
    number = float(value)
    require(math.isfinite(number), f"{description} must be finite; got {value!r}")
    return number


def validate_bound_inputs(screen: dict, assignment: dict) -> None:
    """Require the exact approved protocol/assignment state bound by the screen.

    The payload of a cell is a join between the screen's recorded reservation and the
    assignment's context profiles.  Without this check a different assignment could
    supply a different mass for the same reservation id while the artifact still
    reported the approved assignment's hash.
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
    require(
        inputs.get("assignment_hash") == assignment.get("assignment_hash"),
        "the supplied assignment does not equal the assignment bound by the screen",
    )


def executed_results(screen: dict) -> dict:
    """Return the results object of an executed, non-terminal screen artifact."""
    require(screen.get("mode") == "execute",
            "the payload-conditioning read requires an executed screen; mode is "
            f"{screen.get('mode')!r}")
    results = screen.get("results")
    require(isinstance(results, dict),
            "the screen artifact carries no results object; it was not executed")
    terminal = results.get("terminal")
    require(terminal is None,
            f"the screen terminated at {terminal!r}; a terminal run has no complete "
            "per-cell ladder to condition on")
    return results


def cell_reservations(results: dict) -> dict[int, str]:
    """Return ``{cell: scenario_spec_id}`` from the screen's physical ledger.

    The reservation is read from the ledger's canonical rollout payload rather than
    reconstructed from the balanced context table, so the mapping comes from what the
    screen actually ran.  A cell whose entries disagree about their reservation is
    refused rather than resolved by majority.
    """
    ledger = results.get("physical_ledger")
    require(isinstance(ledger, list) and ledger,
            "the screen artifact carries no physical_ledger entries")

    found: dict[int, set[str]] = {}
    for index, entry in enumerate(ledger):
        require(isinstance(entry, dict), f"physical_ledger[{index}] must be an object")
        cell = entry.get("cell")
        require(isinstance(cell, int) and not isinstance(cell, bool),
                f"physical_ledger[{index}] has a non-integer cell: {cell!r}")
        canonical = entry.get("rollout_canonical")
        require(isinstance(canonical, str) and canonical,
                f"physical_ledger[{index}] carries no rollout_canonical string")
        try:
            payload = json.loads(canonical)
        except json.JSONDecodeError as exc:
            raise PayloadConditioningError(
                f"physical_ledger[{index}].rollout_canonical is not JSON: {exc}"
            ) from exc
        require(isinstance(payload, dict),
                f"physical_ledger[{index}].rollout_canonical is not an object")
        reservation = payload.get("reservation")
        require(isinstance(reservation, dict),
                f"physical_ledger[{index}] carries no reservation object")
        scenario = reservation.get("scenario_spec_id")
        require(isinstance(scenario, str) and scenario,
                f"physical_ledger[{index}] carries no scenario_spec_id")
        found.setdefault(cell, set()).add(scenario)

    require(set(found) == set(SCREEN_CELLS),
            f"the ledger must cover exactly cells {list(SCREEN_CELLS)}; "
            f"got {sorted(found)}")
    for cell in SCREEN_CELLS:
        require(len(found[cell]) == 1,
                f"cell {cell} cites more than one reservation: {sorted(found[cell])}")
    return {cell: next(iter(found[cell])) for cell in SCREEN_CELLS}


def payload_masses_by_id(assignment: dict) -> dict[str, float]:
    """Return ``{payload_profile_id: distal_payload_mass_kg}`` from the assignment.

    The first two checks read properties that ``require_binary_context_factors`` and
    ``payload_masses_by_split`` also read, and both of those run ahead of this function
    on the whole-document path -- so these two are reachable only by calling this one
    directly, and their tests do.  Their messages name **this** read rather than the
    shared field, because raise sites that emit the same sentence are individually
    uncertifiable: a reason assertion passes on any of them, and neutralising one
    leaves the others to refuse with a message the test still matches.  Measured in
    Session 61: with one shared sentence the sites survived a mutation sweep while
    looking covered; worded per read, each is caught.
    """
    profiles = (assignment.get("context_profiles") or {}).get("payloads")
    require(isinstance(profiles, list) and profiles,
            "the payload id map needs a non-empty context_profiles.payloads list")
    masses: dict[str, float] = {}
    for index, profile in enumerate(profiles):
        require(isinstance(profile, dict),
                f"the payload id map needs an object at "
                f"context_profiles.payloads[{index}]")
        identifier = profile.get("id")
        require(isinstance(identifier, str) and identifier,
                f"context_profiles.payloads[{index}] carries no id")
        require(identifier not in masses,
                f"context_profiles.payloads repeats the id {identifier!r}")
        masses[identifier] = require_finite_number(
            profile.get("distal_payload_mass_kg"),
            f"payload profile {identifier!r} distal_payload_mass_kg")
    return masses


def payload_masses_by_split(assignment: dict) -> dict[str, list[float]]:
    """Return each split's reserved distal payload masses, ascending.

    Two of the checks below are redundant with ``require_binary_context_factors`` when
    the caller runs both in the order ``compute_payload_conditioning`` uses -- the
    unknown-split check and the empty-split check.  They are kept because this function
    is public and callable on its own, their messages are deliberately distinct from
    the binary-factor ones so a reason assertion can tell which fired, and their tests
    call this function directly.  They are **not** coverage of the split contract; the
    binary-factor check is what enforces it on the whole-document path.

    The first two checks are redundant as well, and with a *third* site rather than a
    second: ``require_binary_context_factors`` reads the same two properties and runs
    ahead of this function, so on the document path neither of them is what a malformed
    ``context_profiles.payloads`` meets.  All three sites once emitted one sentence,
    which meant no reason assertion could distinguish them; they are now worded per
    read and each is reached by a direct-call test.
    """
    profiles = (assignment.get("context_profiles") or {}).get("payloads")
    # ``require_binary_context_factors`` runs before this function on the document path
    # and builds its own message with an f-string over the factor name, which for
    # "payloads" renders the sentence this site used to carry verbatim.  A duplicated
    # message assembled that way is invisible to a text search of the file -- Session 61
    # found it with a mutation sweep, one session after a docstring here claimed these
    # messages were distinct.  Name the read.
    require(isinstance(profiles, list) and profiles,
            "the per-split payload table needs a non-empty "
            "context_profiles.payloads list")
    by_split: dict[str, list[float]] = {split: [] for split in SPLITS}
    for index, profile in enumerate(profiles):
        require(isinstance(profile, dict),
                f"the per-split payload table needs an object at "
                f"context_profiles.payloads[{index}]")
        split = profile.get("split")
        require(split in by_split,
                f"payload profile {profile.get('id')!r} is assigned to unknown split "
                f"{split!r}")
        by_split[split].append(require_finite_number(
            profile.get("distal_payload_mass_kg"),
            f"payload profile {profile.get('id')!r} distal_payload_mass_kg"))
    for split in SPLITS:
        require(by_split[split],
                f"split {split!r} reserves no distal payload profile")
        by_split[split] = sorted(by_split[split])
    return by_split


# The balanced context table addresses each factor with a binary index, so every split
# reserves exactly two profiles of each kind.  ``expand_reservations`` indexes those
# lists positionally and raises a bare IndexError when one is short -- a foreign
# exception type escaping a contract that promises PayloadConditioningError.
CONTEXT_FACTORS = ("payloads", "environments", "contacts")
PROFILES_PER_SPLIT = 2


def require_binary_context_factors(assignment: dict) -> None:
    """Require exactly two profiles per split for each context factor.

    Checked before the reservation expansion, not after, because the expansion is what
    would otherwise fail and it fails in another module's vocabulary.
    """
    profiles = assignment.get("context_profiles")
    require(isinstance(profiles, dict) and profiles,
            "the assignment carries no context_profiles object")
    for factor in CONTEXT_FACTORS:
        entries = profiles.get(factor)
        require(isinstance(entries, list) and entries,
                f"the assignment carries no context_profiles.{factor} list")
        counts = {split: 0 for split in SPLITS}
        for index, entry in enumerate(entries):
            require(isinstance(entry, dict),
                    f"context_profiles.{factor}[{index}] must be an object")
            split = entry.get("split")
            require(split in counts,
                    f"context_profiles.{factor}[{index}] carries unknown split "
                    f"{split!r}")
            counts[split] += 1
        for split in SPLITS:
            require(counts[split] == PROFILES_PER_SPLIT,
                    f"split {split!r} reserves {counts[split]} {factor} profiles; the "
                    f"balanced context table addresses each factor with a binary index "
                    f"and therefore requires exactly {PROFILES_PER_SPLIT}")


def cell_contexts(results: dict, assignment: dict) -> dict[int, dict]:
    """Return each screened cell's context profiles and distal payload mass.

    Two independent sources are joined here and then required to agree: the mass comes
    from the assignment's context profiles, reached through the reservation the screen
    itself recorded, while ``PROTOCOL_CELL_PAYLOAD_KG`` is transcribed from Protocol P
    section 8's prose table.  Neither side adopts the other.
    """
    reservations = cell_reservations(results)
    masses = payload_masses_by_id(assignment)
    expanded = {row.scenario_spec_id: row for row in expand_reservations(assignment)}

    contexts: dict[int, dict] = {}
    for cell in SCREEN_CELLS:
        scenario = reservations[cell]
        require(scenario in expanded,
                f"cell {cell} cites reservation {scenario!r}, which the assignment "
                "does not expand")
        row = expanded[scenario]
        # Forced by arithmetic, not coverage: ``masses`` is keyed by every id in
        # ``context_profiles.payloads`` and ``expand_reservations`` takes the reserved
        # id out of that same list, so no document can reach this refusal once the
        # duplicate-id check above has passed.  Measured -- deleting this line survives
        # the mutation sweep.  Kept because it states the join's precondition where the
        # join happens, and a future expansion that synthesised a payload id would need
        # it; it must never be presented as a runtime verification of the profile set.
        require(row.payload_id in masses,
                f"reservation {scenario!r} names payload profile {row.payload_id!r}, "
                "which the assignment's context profiles do not define")
        mass = masses[row.payload_id]
        pinned = PROTOCOL_CELL_PAYLOAD_KG[cell]
        require(abs(mass - pinned) <= MASS_TOLERANCE_KG,
                f"cell {cell} resolves to {mass} kg through the assignment, but "
                f"Protocol P section 8 pins {pinned} kg for that cell")
        contexts[cell] = {
            "scenario_spec_id": scenario,
            "split": row.split,
            "payload_id": row.payload_id,
            "distal_payload_mass_kg": mass,
            "env_profile_id": row.env_profile_id,
            "contact_profile_id": row.contact_profile_id,
        }
    return contexts


def ladder_rows(results: dict) -> list[dict]:
    """Return ten internally coherent ladder rows and their four per-cell entries.

    The boundary read consumes ``d``, ``margin`` and ``operative_threshold``.  Those
    are duplicated persisted fields, so merely checking that each is finite would let
    a contradictory artifact move the reported zero crossing.  Re-derive every
    decision-bearing relationship before using any of them.
    """
    ladder = results.get("ladder")
    require(isinstance(ladder, list) and len(ladder) == 10,
            "the ladder must carry exactly ten values; got "
            f"{len(ladder) if isinstance(ladder, list) else type(ladder).__name__}")
    rows: list[dict] = []
    seen: set[float] = set()
    for row in ladder:
        require(isinstance(row, dict), "every ladder row must be an object")
        value = require_finite_number(row.get("remaining_ei"), "a ladder remaining_ei")
        require(value not in seen, f"the ladder repeats remaining_ei {value!r}")
        seen.add(value)
        verdict = row.get("verdict")
        require(verdict in LADDER_VERDICTS,
                f"the ladder row at {value!r} carries unknown verdict {verdict!r}")
        per_cell = row.get("per_cell")
        require(isinstance(per_cell, dict),
                f"the ladder row at {value!r} carries no per_cell object")
        require(set(per_cell) == {str(c) for c in SCREEN_CELLS},
                f"the ladder row at {value!r} must carry exactly cells "
                f"{list(SCREEN_CELLS)}; got {sorted(per_cell)}")
        entries: dict[int, dict] = {}
        for cell in SCREEN_CELLS:
            entry = per_cell[str(cell)]
            require(isinstance(entry, dict),
                    f"the ladder row at {value!r} cell {cell} must be an object")
            distance = require_finite_number(
                entry.get("d"), f"the distance at remaining_ei {value} cell {cell}")
            margin = require_finite_number(
                entry.get("margin"),
                f"the margin at remaining_ei {value} cell {cell}")
            threshold = require_finite_number(
                entry.get("operative_threshold"),
                f"the threshold at remaining_ei {value} cell {cell}")
            q95_c = require_finite_number(
                entry.get("q95_c"),
                f"the q95_c at remaining_ei {value} cell {cell}")
            hard_gates_passed = entry.get("hard_gates_passed")
            # The type check is not decoration.  ``hard_gates_passed`` is the field
            # that decides whether a cell's margin may be read at all, and the next
            # check tests it for truth -- so any truthy non-boolean, the string
            # "false" included, would pass that one and admit an unsafe cell's margin
            # into the boundary read.  Measured in Session 61 by neutralising this
            # line: the analyzer then ACCEPTED a document carrying "false".
            require(isinstance(hard_gates_passed, bool),
                    f"the ladder row at {value!r} cell {cell} carries no boolean "
                    "hard_gates_passed")
            # A ladder value whose fault-side rollout failed the hard gates is a
            # legitimate section-9 shape: the driver writes verdict
            # UNSAFE_LADDER_VALUE, margin null, and continues.  This read refuses such
            # an artifact rather than conditioning on it, because a cell with no margin
            # has no place in an attenuation ratio.  The refusal is a scope boundary,
            # not a claim that the artifact is corrupt.
            require(hard_gates_passed,
                    f"the non-terminal ladder row at {value!r} cell {cell} did not "
                    "pass its hard gates")
            cell_verdict = entry.get("verdict")
            # Subsumed by the margin/verdict equality check below in the sense that
            # neutralising it still yields a refusal -- but with a sentence that blames
            # the margin for what is really an unrecognised label.  Kept for the
            # reason a reader sees, and tested against its own message.
            require(cell_verdict in LADDER_VERDICTS,
                    f"the ladder row at {value!r} cell {cell} carries unknown verdict "
                    f"{cell_verdict!r}")
            require(math.isclose(
                        threshold, 2.0 * q95_c,
                        rel_tol=NUMERIC_TOLERANCE,
                        abs_tol=NUMERIC_TOLERANCE),
                    f"the threshold at remaining_ei {value} cell {cell} does not "
                    "equal 2 * q95_c")
            require(math.isclose(
                        margin, distance - threshold,
                        rel_tol=NUMERIC_TOLERANCE,
                        abs_tol=NUMERIC_TOLERANCE),
                    f"the margin at remaining_ei {value} cell {cell} does not equal "
                    "d - operative_threshold")
            expected_cell_verdict = TESTABLE if margin >= 0.0 else SUB_THRESHOLD
            require(cell_verdict == expected_cell_verdict,
                    f"the margin at remaining_ei {value} cell {cell} implies "
                    f"{expected_cell_verdict}, but the per-cell verdict is "
                    f"{cell_verdict!r}")
            entries[cell] = {
                "d": distance,
                "margin": margin,
                "operative_threshold": threshold,
                "q95_c": q95_c,
                "verdict": cell_verdict,
            }
        stored_min_margin = require_finite_number(
            row.get("min_margin"), f"the minimum margin at remaining_ei {value}")
        expected_min_margin = min(entry["margin"] for entry in entries.values())
        require(math.isclose(
                    stored_min_margin, expected_min_margin,
                    rel_tol=NUMERIC_TOLERANCE,
                    abs_tol=NUMERIC_TOLERANCE),
                f"the stored minimum margin at remaining_ei {value} does not equal "
                "the minimum per-cell margin")
        expected_row_verdict = (
            TESTABLE if all(entry["verdict"] == TESTABLE for entry in entries.values())
            else SUB_THRESHOLD)
        require(verdict == expected_row_verdict,
                f"the per-cell conjunction at remaining_ei {value} implies "
                f"{expected_row_verdict}, but the row verdict is {verdict!r}")
        rows.append({"remaining_ei": value, "verdict": verdict, "per_cell": entries})
    rows.sort(key=lambda row: row["remaining_ei"])
    for cell in SCREEN_CELLS:
        reference = rows[0]["per_cell"][cell]["q95_c"]
        require(all(math.isclose(
                        row["per_cell"][cell]["q95_c"], reference,
                        rel_tol=NUMERIC_TOLERANCE,
                        abs_tol=NUMERIC_TOLERANCE)
                    for row in rows[1:]),
                f"the operative q95_c changes across ladder values in cell {cell}")
    return rows


def payload_levels(contexts: dict[int, dict]) -> list[dict]:
    """Group the screened cells by distal payload mass, ascending.

    Refuses anything other than a balanced two-level contrast, because a ratio between
    levels is only interpretable when the two groups are the same size and the other
    context factors vary within each of them rather than across them.

    Two of the four checks here are **not reachable from the whole-document path** and
    are recorded as such rather than presented as coverage.  ``cell_contexts`` has
    already required every cell's mass to equal ``PROTOCOL_CELL_PAYLOAD_KG``, and those
    four pinned values are two distinct masses over two cells each -- so by the time
    this function is called, "exactly two levels" and "the levels are the same size"
    are forced by arithmetic, exactly like the Session-54 physical-body count.  They
    are kept because this function is the one place that states what the contrast
    requires, and a future protocol version with a different cell table would reach
    them; their tests call this function directly.  The two confounding checks below
    are live on the whole-document path, because section 8 pins the masses and says
    nothing about which environment or contact profile a cell carries.
    """
    grouped: dict[float, list[int]] = {}
    for cell in SCREEN_CELLS:
        grouped.setdefault(contexts[cell]["distal_payload_mass_kg"], []).append(cell)
    masses = sorted(grouped)
    require(len(masses) == 2,
            f"the payload contrast requires exactly two screened payload levels; "
            f"got {masses}")
    require(len(grouped[masses[0]]) == len(grouped[masses[1]]),
            "the two payload levels must contain the same number of cells; got "
            f"{ {m: sorted(grouped[m]) for m in masses} }")
    for mass in masses:
        cells = grouped[mass]
        environments = {contexts[c]["env_profile_id"] for c in cells}
        contacts = {contexts[c]["contact_profile_id"] for c in cells}
        require(len(environments) == len(cells) and len(contacts) == len(cells),
                f"the {mass} kg level does not vary environment and contact within "
                "itself, so payload is confounded with another context factor: "
                f"environments {sorted(environments)}, contacts {sorted(contacts)}")
    return [{"distal_payload_mass_kg": mass, "cells": sorted(grouped[mass])}
            for mass in masses]


def mean(values: list[float]) -> float:
    """Return the arithmetic mean of a non-empty list of floats."""
    require(bool(values), "cannot take the mean of an empty list")
    return sum(values) / len(values)


def attenuation_table(rows: list[dict], levels: list[dict]) -> list[dict]:
    """Return one row per ladder value with each level's mean ``d`` and their ratio."""
    light, heavy = levels[0], levels[1]
    table: list[dict] = []
    for row in rows:
        per_cell = row["per_cell"]
        light_d = [per_cell[c]["d"] for c in light["cells"]]
        heavy_d = [per_cell[c]["d"] for c in heavy["cells"]]
        light_mean = mean(light_d)
        require(light_mean > 0.0,
                f"the mean distance at the lighter payload level is {light_mean} at "
                f"remaining_ei {row['remaining_ei']}; an attenuation ratio needs a "
                "positive reference")
        table.append({
            "remaining_ei": row["remaining_ei"],
            "verdict": row["verdict"],
            "mean_d_light": light_mean,
            "mean_d_heavy": mean(heavy_d),
            "attenuation_ratio": mean(heavy_d) / light_mean,
            "within_level_spread_light": (max(light_d) - min(light_d)) / light_mean,
            "within_level_spread_heavy": (
                (max(heavy_d) - min(heavy_d)) / mean(heavy_d) if mean(heavy_d) > 0.0
                else None),
        })
    return table


def severity_boundary_by_cell(rows: list[dict]) -> dict[int, dict]:
    """Return, per cell, the bracket in which that cell's margin crosses zero.

    The bracket is the measurement: the largest remaining-EI whose margin is positive
    and the smallest whose margin is negative, when the two are adjacent on the ladder.
    ``linear_interpolation`` is an illustration inside that bracket, not a measured
    boundary; the margin is not known to be linear in remaining EI and nothing in this
    module consumes the interpolated value.
    """
    boundaries: dict[int, dict] = {}
    for cell in SCREEN_CELLS:
        series = [(row["remaining_ei"], row["per_cell"][cell]["margin"]) for row in rows]
        bracket = None
        for (lower_ei, lower_margin), (upper_ei, upper_margin) in zip(series, series[1:]):
            if lower_margin >= 0.0 > upper_margin:
                bracket = (lower_ei, lower_margin, upper_ei, upper_margin)
                break
        if bracket is None:
            boundaries[cell] = {
                "crossing_bracket": None,
                "note": ("this cell's margin does not change sign between two adjacent "
                         "ladder values, so the ladder does not bracket a boundary"),
            }
            continue
        lower_ei, lower_margin, upper_ei, upper_margin = bracket
        boundaries[cell] = {
            "crossing_bracket": {
                "last_positive_remaining_ei": lower_ei,
                "last_positive_margin": lower_margin,
                "first_negative_remaining_ei": upper_ei,
                "first_negative_margin": upper_margin,
            },
            "linear_interpolation": lower_ei + (upper_ei - lower_ei) * lower_margin / (
                lower_margin - upper_margin),
            "interpolation_authority": (
                "illustration only; the margin is not known to be linear in remaining "
                "EI and the bracket is what was measured"),
        }
    return boundaries


def null_by_payload_level(results: dict, levels: list[dict], rows: list[dict]) -> list[dict]:
    """Return the operative Stage-C null at each payload level.

    This is the control for the attenuation table.  If the null moved with payload the
    same way the signal does, the margin would be unchanged and the contrast would be a
    scale effect rather than a detectability effect.
    """
    nulls = results.get("stage_c_nulls")
    require(isinstance(nulls, dict) and nulls,
            "the screen artifact carries no stage_c_nulls object")
    require(set(nulls) == {str(c) for c in SCREEN_CELLS},
            f"stage_c_nulls must cover exactly cells {list(SCREEN_CELLS)}; "
            f"got {sorted(nulls)}")
    out: list[dict] = []
    for level in levels:
        values = []
        for cell in level["cells"]:
            entry = nulls[str(cell)]
            require(isinstance(entry, dict), f"stage_c_nulls[{cell}] must be an object")
            q95_c = require_finite_number(
                entry.get("q95_c"), f"the Stage-C null q95_c at cell {cell}")
            require(math.isclose(
                        q95_c, rows[0]["per_cell"][cell]["q95_c"],
                        rel_tol=NUMERIC_TOLERANCE,
                        abs_tol=NUMERIC_TOLERANCE),
                    f"the Stage-C null q95_c at cell {cell} does not equal the "
                    "operative q95_c stored with the ladder")
            values.append(q95_c)
        out.append({
            "distal_payload_mass_kg": level["distal_payload_mass_kg"],
            "cells": level["cells"],
            "q95_c": values,
            "mean_q95_c": mean(values),
        })
    return out


def confirmatory_payload_coverage(contexts: dict[int, dict],
                                  by_split: dict[str, list[float]]) -> dict:
    """Report which splits reserve payload masses the screen never ran.

    Section 8's boundary confines the screen to development contexts, so this is not a
    defect in the screen.  It is the scope statement the ladder verdicts have to be
    read with, stated as numbers instead of as a caveat.
    """
    screened = sorted({contexts[cell]["distal_payload_mass_kg"] for cell in SCREEN_CELLS})
    outside: dict[str, list[float]] = {}
    for split in SPLITS:
        beyond = [mass for mass in by_split[split]
                  if not any(abs(mass - observed) <= MASS_TOLERANCE_KG
                             for observed in screened)]
        if beyond:
            outside[split] = beyond
    return {
        "screened_payload_masses_kg": screened,
        "reserved_payload_masses_kg_by_split": by_split,
        "splits_reserving_unscreened_masses": outside,
        "statement": (
            "every ladder verdict in the executed screen was established at "
            f"{screened} kg of distal payload and at no other mass; a split listed in "
            "splits_reserving_unscreened_masses reserves at least one payload the "
            "ladder says nothing about"),
    }


def compute_payload_conditioning(screen: dict, assignment: dict) -> dict:
    """Compute the payload-conditioning read. Costs zero rollouts."""
    validate_bound_inputs(screen, assignment)
    results = executed_results(screen)
    # The per-split payload table is validated BEFORE the reservation expansion.
    # ``expand_reservations`` indexes the split's payload list by the balanced context
    # table, so a document with a mislabelled split or a missing profile dies there
    # with a bare IndexError from another module -- a foreign exception type escaping a
    # function whose contract says PayloadConditioningError.  Measured, then fixed by
    # ordering rather than by catching, so the reason a reader sees names the document.
    require_binary_context_factors(assignment)
    masses_by_split = payload_masses_by_split(assignment)
    contexts = cell_contexts(results, assignment)
    rows = ladder_rows(results)
    levels = payload_levels(contexts)
    table = attenuation_table(rows, levels)
    ratios = [entry["attenuation_ratio"] for entry in table]

    return {
        "purpose": (
            "Post-hoc diagnostic read of an executed Protocol P Stage-A/B/C screen: "
            "how the structural distance and the operative null vary with distal "
            "payload mass across the screen's own balanced two-level contrast. "
            "Derived from persisted results; zero rollouts."
        ),
        "authority": (
            "NOT PRE-REGISTERED. This read classifies nothing, opens no terminal "
            "branch, and cannot change the outcome case or the section-9 role-coverage "
            "count. It reports a scope restriction that already applied to the "
            "executed screen; it is not evidence for or against the hypothesis."
        ),
        "inputs": {
            "screen_outcome_case": results.get("outcome_case"),
            "protocol_canonical_sha256": PROTOCOL_CANONICAL_SHA256,
            "assignment_canonical_sha256": ASSIGNMENT_CANONICAL_SHA256,
            "assignment_hash": assignment.get("assignment_hash"),
        },
        "cells": {str(cell): contexts[cell] for cell in SCREEN_CELLS},
        "payload_levels": levels,
        "attenuation": {
            "definition": (
                "mean structural distance d over the heavier payload level divided by "
                "the mean over the lighter level, at one ladder value; environment and "
                "contact vary within each level, so the ratio is not confounded with "
                "either"),
            "by_ladder_value": table,
            "ratio_min": min(ratios),
            "ratio_max": max(ratios),
            "ratio_mean": mean(ratios),
            "extrapolation_authority": (
                "two payload levels determine a ratio and nothing else; no functional "
                "form in payload mass is fitted, implied, or usable from this artifact"),
        },
        "null_by_payload_level": null_by_payload_level(results, levels, rows),
        "severity_boundary_by_cell": {
            str(cell): value
            for cell, value in severity_boundary_by_cell(rows).items()
        },
        "confirmatory_payload_coverage": confirmatory_payload_coverage(
            contexts, masses_by_split),
        "rollouts_spent": 0,
    }


def derive_payload_conditioning(screen_path: Path, assignment_path: Path) -> dict:
    """Load, bind, and derive one payload-conditioning artifact from tracked inputs.

    Both inputs are hashed through ``canonical_text_sha256`` because both are tracked
    TEXT documents; section 0's two hash domains are disjoint by the kind of file, and
    the raw helper would record this checkout's line-ending rendering rather than the
    document (the Session-59 finding).
    """
    screen_path = Path(screen_path)
    assignment_path = Path(assignment_path)
    screen = load_json(screen_path, "screen result")
    assignment = load_json(assignment_path, "assignment document")
    report = compute_payload_conditioning(screen, assignment)

    actual_assignment_digest = canonical_text_sha256(assignment_path)
    require(actual_assignment_digest == ASSIGNMENT_CANONICAL_SHA256,
            "the supplied assignment file does not equal the approved canonical state")
    protocol_path = Path(__file__).resolve().parents[1] / "protocol" / PROTOCOL_FILENAME
    actual_protocol_digest = canonical_text_sha256(protocol_path)
    require(actual_protocol_digest == PROTOCOL_CANONICAL_SHA256,
            "the tracked Protocol P file does not equal the approved canonical state")

    report["inputs"].update({
        "screen_result_canonical_sha256": canonical_text_sha256(screen_path),
        "assignment_canonical_sha256": actual_assignment_digest,
        "protocol_canonical_sha256": actual_protocol_digest,
    })
    return report


def render(report: dict) -> str:
    """Return the human-readable stdout summary for ``report``."""
    lines = ["Protocol P -- payload conditioning of the Stage-B margin (zero rollouts)",
             "NOT PRE-REGISTERED: this read classifies nothing.", ""]
    lines.append(f"screen outcome case: {report['inputs']['screen_outcome_case']}")
    lines.append("")
    lines.append(f"  {'cell':>4}  {'payload kg':>10}  {'environment':<16} contact")
    for cell in SCREEN_CELLS:
        entry = report["cells"][str(cell)]
        lines.append(f"  {cell:>4}  {entry['distal_payload_mass_kg']:>10.3f}  "
                     f"{entry['env_profile_id']:<16} {entry['contact_profile_id']}")
    lines.append("")
    light, heavy = report["payload_levels"]
    lines.append(f"  attenuation: mean d at {heavy['distal_payload_mass_kg']:g} kg "
                 f"over mean d at {light['distal_payload_mass_kg']:g} kg")
    lines.append(f"  {'remEI':>6}  {'d light':>10}  {'d heavy':>10}  {'ratio':>7}  verdict")
    for entry in report["attenuation"]["by_ladder_value"]:
        lines.append(f"  {entry['remaining_ei']:>6.2f}  {entry['mean_d_light']:>10.6f}  "
                     f"{entry['mean_d_heavy']:>10.6f}  "
                     f"{entry['attenuation_ratio']:>7.4f}  {entry['verdict']}")
    attenuation = report["attenuation"]
    lines.append(f"  ratio over the ladder: min {attenuation['ratio_min']:.4f}  "
                 f"mean {attenuation['ratio_mean']:.4f}  "
                 f"max {attenuation['ratio_max']:.4f}")
    lines.append("")
    lines.append("  operative Stage-C null by payload level (the control):")
    for level in report["null_by_payload_level"]:
        values = ", ".join(f"{value:.6f}" for value in level["q95_c"])
        lines.append(f"    {level['distal_payload_mass_kg']:g} kg  cells "
                     f"{level['cells']}  q95_c {values}")
    lines.append("")
    lines.append("  severity boundary bracket, per cell:")
    for cell in SCREEN_CELLS:
        entry = report["severity_boundary_by_cell"][str(cell)]
        bracket = entry.get("crossing_bracket")
        if bracket is None:
            lines.append(f"    cell {cell}: {entry['note']}")
            continue
        lines.append(
            f"    cell {cell}: last positive at remEI "
            f"{bracket['last_positive_remaining_ei']:g} "
            f"({bracket['last_positive_margin']:+.6f}), first negative at "
            f"{bracket['first_negative_remaining_ei']:g} "
            f"({bracket['first_negative_margin']:+.6f}); "
            f"interpolated {entry['linear_interpolation']:.4f} (illustration only)")
    lines.append("")
    coverage = report["confirmatory_payload_coverage"]
    lines.append(f"  screened payload masses: {coverage['screened_payload_masses_kg']} kg")
    for split, masses in coverage["splits_reserving_unscreened_masses"].items():
        lines.append(f"    {split:>5} reserves unscreened masses {masses} kg")
    lines.append("")
    lines.append(f"  authority: {report['authority']}")
    return "\n".join(lines)


def main() -> None:
    """Parse arguments, compute the read, print it, and write the artifact."""
    parser = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    parser.add_argument("--screen-result", required=True,
                        help="path to an executed stage_abc_screen.json")
    parser.add_argument("--assignment", required=True,
                        help="path to the bound proposed-gate3-assignment JSON")
    parser.add_argument("--output-dir", required=True,
                        help="directory the payload_conditioning.json artifact goes to")
    args = parser.parse_args()

    report = derive_payload_conditioning(Path(args.screen_result), Path(args.assignment))
    print(render(report), flush=True)

    out_dir = Path(args.output_dir)
    out_dir.mkdir(parents=True, exist_ok=True)
    out_path = out_dir / "payload_conditioning.json"
    out_path.write_text(
        json.dumps(report, indent=1, sort_keys=True, ensure_ascii=False,
                   allow_nan=False) + "\n",
        encoding="utf-8", newline="\n")
    print(f"\nwrote {out_path}", flush=True)


if __name__ == "__main__":
    main()
