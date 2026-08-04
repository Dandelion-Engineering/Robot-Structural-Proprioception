"""Focused tests for the zero-rollout payload-boundary extension executable."""

from __future__ import annotations

import dataclasses
import hashlib
import importlib.util
import itertools
import json
import re
import sys
from collections import Counter
from pathlib import Path, PurePosixPath, PureWindowsPath

import pytest

PACKET = Path(__file__).resolve().parents[1]
SCRIPTS = PACKET / "scripts"
if str(SCRIPTS) not in sys.path:
    sys.path.insert(0, str(SCRIPTS))

SPEC = importlib.util.spec_from_file_location(
    "run_payload_boundary_extension", SCRIPTS / "run_payload_boundary_extension.py"
)
assert SPEC is not None and SPEC.loader is not None
x = importlib.util.module_from_spec(SPEC)
sys.modules[SPEC.name] = x
SPEC.loader.exec_module(x)

from utils.protocol_p import ProtocolPError, canonical_json  # noqa: E402


@pytest.fixture(scope="module")
def context():
    return x.resolve_context(
        config_path=PACKET / "config" / "draft-config-v0.1.json",
        schema_path=PACKET / "schema" / "schema.json",
        assignment_path=PACKET / "config" / "proposed-gate3-assignment-v0.1.json",
        protocol_path=PACKET / "protocol" / "protocol-p-v2.3.3.md",
        extension_path=PACKET / "protocol" / "payload-boundary-extension-v0.2.md",
    )


@pytest.fixture(scope="module")
def plan(context):
    return x.build_plan_document(context)


def test_extension_spec_digest_is_the_jointly_approved_state():
    assert x.canonical_text_sha256(
        PACKET / "protocol" / "payload-boundary-extension-v0.2.md"
    ) == x.EXTENSION_CANONICAL_SHA256


def test_mass_index_order_is_not_silently_treated_as_ascending_mass_order():
    assert [item.mass_kg for item in x.MASS_CELLS] == [
        0.050, 0.025, 0.075, 0.100, 0.125, 0.150, 0.200
    ]
    assert [item.mass_kg for item in x.ASCENDING_MASS_CELLS] == [
        0.025, 0.050, 0.075, 0.100, 0.125, 0.150, 0.200
    ]


def test_ladder_and_role_map_are_the_document_literals():
    assert x.LADDER == (0.35, 0.40, 0.45, 0.50, 0.55, 0.60, 0.65, 0.75, 0.85, 0.90)
    assert x.ROLE_SEVERITY_MAP == {
        "dev": (0.50, 0.75),
        "pilot": (0.60, 0.85),
        "val": (0.40, 0.90),
        "test": (0.35, 0.65),
    }


def test_role_map_equals_the_assignment_but_runtime_never_reads_the_grid():
    assignment = json.loads(
        (PACKET / "config" / "proposed-gate3-assignment-v0.1.json").read_text(
            encoding="utf-8"
        )
    )
    actual = {
        split: tuple(assignment["fault_grid_by_split"][split]["structure"]["severities"])
        for split in x.ROLE_SEVERITY_MAP
    }
    assert actual == x.ROLE_SEVERITY_MAP
    source = (SCRIPTS / "run_payload_boundary_extension.py").read_text(encoding="utf-8")
    assert source.count('"fault_grid_by_split"') == 0


def test_exact_identity_band_and_common_random_number_classes():
    rows = x.planned_rows()
    audit = x.require_plan_shape(rows)
    assert audit == {
        "occurrences": 126,
        "distinct_physical_keys": 126,
        "distinct_identities": 8,
        "identity_class_counts": {
            "0": 77, "1": 7, "2": 7, "3": 7,
            "4": 7, "5": 7, "6": 7, "7": 7,
        },
    }
    assert sorted({row.identity.sensor_seed for row in rows}) == [
        160002, 161002, 162002, 163002, 164002, 165002, 166002, 167002
    ]


def test_mass_is_in_the_physical_key_and_in_the_extension_logical_key():
    light = x.ExtensionRow(x.MASS_CELLS[1], x.CONDITION_STRUCTURE, 0.35, 0)
    heavy = x.ExtensionRow(x.MASS_CELLS[6], x.CONDITION_STRUCTURE, 0.35, 0)
    assert light.identity == heavy.identity
    assert light.physical != heavy.physical
    assert light.key != heavy.key
    assert light.physical.distal_payload_mass_kg == 0.025
    assert heavy.physical.distal_payload_mass_kg == 0.2


def test_row_vocabulary_maps_exact_payload_label_to_existing_builder_label():
    row = x.ExtensionRow(x.MASS_CELLS[0], x.CONDITION_STRUCTURE, 0.35, 0)
    assert row.condition == "structure"
    assert row.internal_condition == "structural"
    assert row.stage == "XA"
    assert row.substage == "XB"


@pytest.mark.parametrize(
    "condition,severity,replicate,message",
    [
        ("unknown", None, 0, "unknown extension condition"),
        (x.CONDITION_HEALTHY, 0.35, 0, "healthy extension row takes no severity"),
        (x.CONDITION_STRUCTURE, 0.35, 1, "matched k=0"),
        (x.CONDITION_STRUCTURE, 0.37, 0, "outside"),
    ],
)
def test_invalid_rows_fail_loud(condition, severity, replicate, message):
    with pytest.raises(ProtocolPError, match=message):
        x.ExtensionRow(x.MASS_CELLS[0], condition, severity, replicate)


def test_plan_is_valid_zero_rollout_and_has_both_orders(plan):
    assert plan["mode"] == "plan"
    assert plan["plan_valid"] is True
    assert plan["preflight"]["passed"] is True
    assert plan["plan"]["stage_order"] == {
        "plan": ["X0P"],
        "execute": ["X0E", "XR", "XA", "XM-C", "XL", "XM-B", "XZ"],
    }
    assert plan["plan"]["census"]["maximum_cost"] == 127


def test_plan_mechanics_are_exact_for_all_seven_masses(plan):
    reports = plan["preflight"]["per_mass_realized_delta"]
    assert len(reports) == 7
    for report in reports:
        assert report["configured_mass_kg"] == report["declared_mass_kg"]
        assert report["realized_delta_kg"] == pytest.approx(
            report["declared_mass_kg"], abs=1e-12, rel=0.0
        )


def test_plan_physical_key_digest_recomputes_from_the_exact_recipe(plan):
    reports = [x.physical_key_report(row.physical) for row in x.planned_rows()]
    ordered = sorted(reports, key=canonical_json)
    expected = hashlib.sha256(canonical_json(ordered).encode("utf-8")).hexdigest()
    assert plan["plan"]["physical_keys"] == {
        "count": 126,
        "canonical_sha256": expected,
    }


def test_plan_contains_every_required_input_without_an_absolute_path(plan):
    assert set(plan["inputs"]) == {
        "assignment_canonical_sha256", "assignment_hash", "base_config_hash",
        "protocol_spec_sha256", "extension_spec_sha256", "config_path",
        "control_dt_s", "window", "window_steps", "onset_index", "onset_time_s",
        "probe_start_offset_s", "suite", "probe_peak_force_n",
        "probe_ramp_fraction_of_duration", "environment_profile_id",
        "contact_profile_id", "trajectory_spec_id", "source_scenario_spec_id",
    }
    assert not Path(plan["inputs"]["config_path"]).is_absolute()


def test_build_extension_overrides_has_the_exact_non_circular_payload(context):
    row = x.ExtensionRow(x.MASS_CELLS[6], x.CONDITION_STRUCTURE, 0.35, 0)
    reservation, overrides, canonical, provenance = x.build_extension_overrides(row, context)
    payload = json.loads(canonical)
    assert set(payload) == {
        "base_config_hash", "assignment_canonical_sha256", "assignment_hash",
        "protocol_spec_sha256", "extension_spec_sha256", "stage", "substage",
        "mass_index", "distal_payload_mass_kg", "condition", "severity",
        "replicate", "overrides", "reservation",
    }
    assert set(payload["overrides"]) == {
        "probe_peak_force_n", "probe_ramp_fraction_of_duration", "physical_faults",
        "realized_pair_id", "distal_payload_mass_kg",
    }
    assert "provenance_hash" not in payload["overrides"]
    assert payload["condition"] == "structure"
    assert payload["distal_payload_mass_kg"] == 0.2
    assert payload["overrides"]["distal_payload_mass_kg"] == 0.2
    assert provenance == "dev-" + hashlib.sha256(canonical.encode("utf-8")).hexdigest()
    assert overrides.provenance_hash == provenance
    assert overrides.distal_payload_mass_kg == 0.2
    assert reservation.base_pair_id == "basepair_payloadext_k0"


def test_healthy_payload_has_empty_fault_list_and_null_severity(context):
    row = x.ExtensionRow(x.MASS_CELLS[0], x.CONDITION_HEALTHY, None, 7)
    _reservation, overrides, canonical, _provenance = x.build_extension_overrides(row, context)
    payload = json.loads(canonical)
    assert overrides.physical_faults == ()
    assert payload["overrides"]["physical_faults"] == []
    assert payload["severity"] is None
    assert payload["replicate"] == 7


def _result(row, *, coefficients=None, gate=True, error=None):
    canonical = canonical_json({"row": row.key})
    return x.ExtensionPhysicalResult(
        row=row,
        extension_rollout_canonical=canonical,
        rollout_provenance="dev-" + hashlib.sha256(canonical.encode("utf-8")).hexdigest(),
        gate_report=None if error else {"passed": gate},
        coefficients=coefficients,
        n_steps=None if error else 1500,
        elapsed_s=0.01,
        error=error,
    )


def test_extension_ledger_accepts_x_stages_and_refuses_duplicate_body_or_stamp():
    ledger = x.ExtensionLedger()
    row = x.ExtensionRow(x.MASS_CELLS[0], x.CONDITION_HEALTHY, None, 0)
    result = _result(row, coefficients=(0.0,) * 8)
    ledger.record(result)
    with pytest.raises(ProtocolPError, match="already recorded"):
        ledger.record(result)
    other = x.ExtensionRow(x.MASS_CELLS[1], x.CONDITION_HEALTHY, None, 0)
    duplicate_stamp = dataclasses.replace(result, row=other)
    with pytest.raises(ProtocolPError, match="same provenance stamp"):
        ledger.record(duplicate_stamp)


def test_prefix_rule_is_exact_and_tolerance_free():
    assert x.is_prefix(())
    assert x.is_prefix((0.35, 0.40, 0.45))
    assert not x.is_prefix((0.35, 0.45))
    assert not x.is_prefix((0.90,))


def test_monotonicity_is_set_inclusion_over_ascending_mass():
    good = {0.025: (0.35, 0.40), 0.050: (0.35,), 0.075: ()}
    assert x.monotonicity_violations(good) == []
    bad = {0.025: (0.35,), 0.050: (0.35, 0.40)}
    assert x.monotonicity_violations(bad) == [
        {"lighter_mass_kg": 0.025, "heavier_mass_kg": 0.05,
         "heavier_only_values": [0.4]}
    ]


def test_shape_diagnostic_carries_both_measurements_thresholds_and_q95_units(plan):
    per_mass = x.execute_document_skeleton(plan, "a" * 64)["results"]["per_mass"]
    for entry in per_mass:
        entry["q95"] = 1.0
        entry["threshold"] = 2.0
        for index, row in enumerate(entry["ladder_rows"]):
            row["d"] = 1.0 + index
    testable = {entry["mass_kg"]: (0.35,) for entry in per_mass}
    testable[0.05] = (0.35, 0.45)  # prefix violation at the anchor
    testable[0.075] = (0.35, 0.40, 0.45)  # heavier-only 0.40 against 0.050
    report = x._shape_diagnostics(per_mass, testable)
    prefix = [item for item in report["prefix_violations"] if item["mass_kg"] == 0.05]
    assert prefix
    assert {"lower_d", "higher_d", "threshold", "absolute_d_difference",
            "difference_in_max_q95_units"} <= set(prefix[0])
    monotone = [
        item for item in report["monotonicity_violations"]
        if item["lighter_mass_kg"] == 0.05 and item["heavier_mass_kg"] == 0.075
    ]
    assert monotone
    assert {"lighter_d", "heavier_d", "lighter_threshold", "heavier_threshold",
            "absolute_d_difference", "difference_in_max_q95_units"} <= set(monotone[0])


def _prefix(length):
    return x.LADDER[:length]


def test_classifier_is_exhaustive_over_all_19448_monotone_prefix_states():
    counts = Counter()
    for lengths in itertools.combinations_with_replacement(range(11), 7):
        # combinations are ascending; reversing makes prefix length non-increasing as
        # payload mass increases, which is exactly set-inclusion monotonicity.
        values = list(reversed(lengths))
        state = {
            mass.mass_kg: _prefix(length)
            for mass, length in zip(x.ASCENDING_MASS_CELLS, values)
        }
        outcome = x.classify_complete(state)
        assert outcome in {x.OUTCOME_EMPTY, x.OUTCOME_ROLE_LOST, x.OUTCOME_ROLE_HELD}
        counts[outcome] += 1
    assert sum(counts.values()) == 19448
    assert counts == Counter({
        x.OUTCOME_EMPTY: 8008,
        x.OUTCOME_ROLE_LOST: 3515,
        x.OUTCOME_ROLE_HELD: 7925,
    })


def test_classifier_orders_reduced_prefix_and_monotone_before_cases():
    full = {mass.mass_kg: x.LADDER for mass in x.MASS_CELLS}
    assert x.classify_complete(full, reduced=True) == x.OUTCOME_REDUCED
    nonprefix = dict(full)
    nonprefix[0.05] = (0.35, 0.45)
    assert x.classify_complete(nonprefix) == x.OUTCOME_NONPREFIX
    nonmonotone = {mass.mass_kg: (0.35,) for mass in x.MASS_CELLS}
    nonmonotone[0.2] = (0.35, 0.40)
    assert x.classify_complete(nonmonotone) == x.OUTCOME_NONMONOTONE


def test_option_b_cap_uses_one_role_retaining_initial_prefix_rule():
    state = {mass.mass_kg: x.LADDER for mass in x.MASS_CELLS}
    assert x.option_b_cap(state) == 0.2
    state[0.05] = (0.35,)  # dev loses both 0.50 and 0.75 at the second ascending mass
    assert x.option_b_cap(state) == 0.025
    state[0.025] = ()
    assert x.option_b_cap(state) is None


def _fake_runner(*, identical_across_mass=False, unsafe=None, invalid=None, anchor_all=False):
    unsafe = unsafe or set()
    invalid = invalid or set()

    def run(row, _context, ledger):
        if row.key in invalid:
            item = _result(row, coefficients=None, error="synthetic invalid measurement")
        else:
            base = 0.0 if identical_across_mass else row.mass.mass_kg * 100.0
            if row.condition == x.CONDITION_HEALTHY:
                signal = row.replicate * 0.1
            else:
                signal = 2.0 if (anchor_all or row.severity <= 0.50) else 0.5
            coefficients = (base + signal,) + (0.0,) * 7
            item = _result(row, coefficients=coefficients, gate=row.key not in unsafe)
        ledger.record(item)
        return item

    return run


def _replay():
    return {"ran": True, "passed": True, "elapsed_s": 0.5, "reason": None}


def test_full_synthetic_run_preserves_126_physical_and_532_logical_counts(context, plan):
    document = x.run_extension(
        context, plan, x.canonical_document_sha256(plan), _replay(),
        run_row=_fake_runner(),
    )
    results = document["results"]
    assert results["outcome"] == x.OUTCOME_ROLE_LOST
    assert results["mass_coverage"] == "COMPLETE"
    assert results["override_liveness"] == {
        "count": 168,
        "min_pairwise_distance": pytest.approx(2.5),
        "passed": True,
        "reason": None,
    }
    assert results["census"] == {
        "extension_physical_rollouts": 126,
        "replay_physical_rollouts": 1,
        "total_physical_rollouts": 127,
        "logical_references": 532,
        "rollouts_by_stage": {"XA": 18, "XM-B": 60, "XM-C": 48},
    }
    assert results["logical_reference_census"] == {
        "ladder_fault_references": 70,
        "ladder_healthy_references": 70,
        "null_endpoint_references": 392,
        "total": 532,
    }
    assert len(results["physical_ledger"]) == 126
    assert results["ledger_census"] == {
        "extension_physical_results": 126,
        "distinct_stamps": 126,
        "distinct_identities": 8,
        "identity_class_counts": {
            "0": 77, "1": 7, "2": 7, "3": 7,
            "4": 7, "5": 7, "6": 7, "7": 7,
        },
    }
    assert results["verdict_scope"]["masses_measured_kg"] == [
        0.025, 0.05, 0.075, 0.1, 0.125, 0.15, 0.2
    ]


def test_dead_payload_override_stops_at_x8_before_nonanchor_ladders(context, plan):
    document = x.run_extension(
        context, plan, x.canonical_document_sha256(plan), _replay(),
        run_row=_fake_runner(identical_across_mass=True),
    )
    results = document["results"]
    assert results["outcome"] == x.OUTCOME_OVERRIDE
    assert results["terminal"]["stage_reached"] == "XL"
    assert results["census"]["extension_physical_rollouts"] == 66
    assert results["census"]["total_physical_rollouts"] == 67
    assert results["census"]["rollouts_by_stage"] == {
        "XA": 18, "XM-C": 48
    }


def test_anchor_disagreement_is_terminal_after_18_extension_rollouts(context, plan):
    document = x.run_extension(
        context, plan, x.canonical_document_sha256(plan), _replay(),
        run_row=_fake_runner(anchor_all=True),
    )
    assert document["results"]["outcome"] == x.OUTCOME_ANCHOR_FAIL
    assert document["results"]["census"]["extension_physical_rollouts"] == 18


def test_unsafe_anchor_stops_at_detection(context, plan):
    row = x.ExtensionRow(x.MASS_CELLS[0], x.CONDITION_HEALTHY, None, 2)
    document = x.run_extension(
        context, plan, x.canonical_document_sha256(plan), _replay(),
        run_row=_fake_runner(unsafe={row.key}),
    )
    assert document["results"]["outcome"] == x.OUTCOME_UNSAFE_ANCHOR
    assert document["results"]["census"]["extension_physical_rollouts"] == 3


def test_invalid_measurement_is_persisted_and_stops(context, plan):
    row = x.ExtensionRow(x.MASS_CELLS[0], x.CONDITION_HEALTHY, None, 0)
    document = x.run_extension(
        context, plan, x.canonical_document_sha256(plan), _replay(),
        run_row=_fake_runner(invalid={row.key}),
    )
    results = document["results"]
    assert results["outcome"] == x.OUTCOME_INVALID
    assert results["census"]["extension_physical_rollouts"] == 1
    assert results["physical_ledger"][0]["error"] == "synthetic invalid measurement"


def test_nonanchor_unsafe_mass_finishes_liveness_and_returns_reduced(context, plan):
    row = x.ExtensionRow(x.MASS_CELLS[6], x.CONDITION_HEALTHY, None, 3)
    document = x.run_extension(
        context, plan, x.canonical_document_sha256(plan), _replay(),
        run_row=_fake_runner(unsafe={row.key}),
    )
    results = document["results"]
    assert results["outcome"] == x.OUTCOME_REDUCED
    assert results["mass_coverage"] == "REDUCED"
    assert results["override_liveness"]["count"] == 168
    assert results["census"]["extension_physical_rollouts"] == 116
    assert results["masses_excluded"] == [
        {"m": 6, "mass_kg": 0.2, "reason": "healthy hard-gate failure at k=[3]",
         "rollouts_spent": 8}
    ]


def test_execute_skeleton_has_every_required_field(plan):
    document = x.execute_document_skeleton(plan, "a" * 64)
    assert set(document) == {
        "inputs", "protocol", "plan", "approved_plan_canonical_sha256",
        "mode", "results", "authority",
    }
    assert set(document["results"]) == {
        "replay_gate", "preflight", "anchor", "per_mass", "masses_excluded",
        "shape_diagnostics", "override_liveness", "outcome", "mass_coverage",
        "verdict_scope", "terminal", "physical_ledger", "ledger_census", "census",
        "logical_reference_census", "timing", "step_counts",
    }
    assert len(document["results"]["per_mass"]) == 7
    assert all(len(item["ladder_rows"]) == 10 for item in document["results"]["per_mass"])


def test_default_cli_mode_is_plan_and_execute_requires_explicit_inputs():
    args = x.parse_args([])
    assert args.mode == "plan"
    assert args.approved_plan_sha256 is None
    assert args.data_root is None
    assert args.output_dir.as_posix() == "results/payload_boundary_extension"


def test_only_a_passing_plan_named_by_exact_lowercase_digest_is_authorized(plan):
    digest = x.canonical_document_sha256(plan)
    assert x.require_authorized_plan(plan, digest) == digest
    with pytest.raises(ProtocolPError, match="lowercase SHA-256"):
        x.require_authorized_plan(plan, digest.upper())
    with pytest.raises(ProtocolPError, match="!= authorized digest"):
        x.require_authorized_plan(plan, "0" * 64)
    failed = x.failed_plan_document("synthetic")
    with pytest.raises(ProtocolPError, match="plan_valid=true"):
        x.require_authorized_plan(failed, x.canonical_document_sha256(failed))


def test_failed_plan_persists_a_classified_reason():
    plan = x.failed_plan_document("synthetic preflight failure")
    assert plan["plan_valid"] is False
    assert plan["terminal"] == {
        "rule": x.OUTCOME_CONSTRUCTION,
        "reason": "synthetic preflight failure",
        "stage_reached": "X0P",
    }
    canonical_json(plan)


def test_strict_json_refuses_duplicate_nonfinite_non_utf8_and_deep_values(tmp_path):
    duplicate = tmp_path / "duplicate.json"
    duplicate.write_text('{"x":1,"x":2}', encoding="utf-8")
    with pytest.raises(ProtocolPError, match="duplicate JSON key"):
        x.strict_read_json(duplicate)
    nonfinite = tmp_path / "nonfinite.json"
    nonfinite.write_text('{"x":NaN}', encoding="utf-8")
    with pytest.raises(ProtocolPError, match="non-finite JSON token"):
        x.strict_read_json(nonfinite)
    overflow = tmp_path / "overflow.json"
    overflow.write_text('{"x":1e9999}', encoding="utf-8")
    with pytest.raises(ProtocolPError, match="not canonical UTF-8 data"):
        x.strict_read_json(overflow)
    surrogate = tmp_path / "surrogate.json"
    surrogate.write_text('{"x":"\\ud800"}', encoding="ascii")
    with pytest.raises(ProtocolPError, match="not canonical UTF-8 data"):
        x.strict_read_json(surrogate)
    too_deep = tmp_path / "too-deep.json"
    too_deep.write_text(
        '{"x":' + '[' * (x.MAX_PLAN_JSON_DEPTH + 1) + '0'
        + ']' * (x.MAX_PLAN_JSON_DEPTH + 1) + '}',
        encoding="ascii",
    )
    with pytest.raises(ProtocolPError, match="exceeds maximum nesting depth"):
        x.strict_read_json(too_deep)


def test_the_depth_gate_still_admits_the_plan_this_tool_writes(tmp_path, plan):
    """The ACCEPT side.  A guard that refuses everything is not a guard.

    Nothing above can fail if ``MAX_PLAN_JSON_DEPTH`` is tightened to a value below the
    plan document's own depth -- the refuse tests all construct one level past whatever
    the constant says, so they stay green while execute mode begins refusing the only
    plan it will ever legitimately be handed.  Measured: the plan document is 5 levels
    deep and the execute skeleton is 7, against a gate of 64.
    """

    at_gate = tmp_path / "at-gate.json"
    at_gate.write_text(
        '{"x":' + '[' * (x.MAX_PLAN_JSON_DEPTH - 1) + '0'
        + ']' * (x.MAX_PLAN_JSON_DEPTH - 1) + '}',
        encoding="ascii",
    )
    x.strict_read_json(at_gate)

    official = tmp_path / "plan.json"
    official.write_text(canonical_json(plan), encoding="utf-8", newline="")
    assert x.strict_read_json(official) == json.loads(canonical_json(plan))


def test_canonical_writer_refuses_absolute_windows_path(tmp_path):
    with pytest.raises(ProtocolPError, match="absolute filesystem path"):
        x.write_canonical_document(tmp_path / "bad.json", {"path": r"C:\\Users\\person"})


# --- Session 65 review additions -------------------------------------------------
#
# Every test below constructs a state the previous state of this executable accepted,
# and each one is red against it.  They cover main()'s execute-mode exits, which no
# test reached before: the whole region was unexercised, which is exactly where an
# unbound name and a re-typed scenario id survived.


def test_replay_source_is_the_approved_gate_scenario_not_a_retyped_literal(context):
    """The pre-rollout half of the replay gate, driven at zero rollout cost."""

    from protocol_p_replay_gate import RUN_ID, SCENARIO_SPEC_ID
    from utils.assignment_generator import screen_pair_id

    assert x.REPLAY_SCENARIO_SPEC_ID is SCENARIO_SPEC_ID
    assert x.REPLAY_RUN_ID.startswith(f"{SCENARIO_SPEC_ID}_")
    reservation, identity_row = x.resolve_replay_source(context)
    assert reservation.scenario_spec_id == SCENARIO_SPEC_ID == "scenario_dev_t01_f000_r00"
    assert identity_row.run_id == RUN_ID
    # This equality is the check the gate makes before it spends its rollout.  Selecting
    # any other delivered reservation fails here, one step after a unique-match check
    # that a wrong-but-existing scenario id passes.
    assert screen_pair_id(reservation, None) == identity_row.pair_id


def test_no_scenario_id_is_retyped_anywhere_in_the_executable():
    source = (SCRIPTS / "run_payload_boundary_extension.py").read_text(encoding="utf-8")
    assert "scenario_dev_t0" not in source


def _write_plan(tmp_path, plan):
    path = tmp_path / "plan.json"
    x.write_canonical_document(path, plan)
    return path, x.canonical_document_sha256(plan)


def test_replay_failure_persists_the_terminal_artifact_and_the_true_rollout_count(
    tmp_path, plan
):
    """R1 must leave a record; the previous state raised UnboundLocalError instead."""

    plan_path, digest = _write_plan(tmp_path, plan)
    code = x.main([
        "--mode", "execute",
        "--output-dir", str(tmp_path),
        "--plan", str(plan_path),
        "--approved-plan-sha256", digest,
        "--data-root", str(tmp_path / "absent_data_root"),
        "--config", str(PACKET / "config" / "draft-config-v0.1.json"),
        "--schema", str(PACKET / "schema" / "schema.json"),
        "--assignment", str(PACKET / "config" / "proposed-gate3-assignment-v0.1.json"),
        "--protocol", str(PACKET / "protocol" / "protocol-p-v2.3.3.md"),
        "--extension", str(PACKET / "protocol" / "payload-boundary-extension-v0.2.md"),
    ])
    assert code == 1
    written = json.loads((tmp_path / x.RESULT_FILENAME).read_text(encoding="utf-8"))
    results = written["results"]
    assert results["outcome"] == x.OUTCOME_REPLAY
    assert results["terminal"]["stage_reached"] == "XR"
    assert results["preflight"] == {
        "ran": True, "passed": True, "plan_digest_match": True,
        "per_mass_realized_delta": plan["preflight"]["per_mass_realized_delta"],
        "reason": None,
    }
    assert results["replay_gate"]["ran"] is True
    assert results["replay_gate"]["passed"] is False
    # The gate failed on an absent pinned input, so its rollout was never spent.  A
    # hard-coded 1 here would report a cost the run did not incur.
    assert results["replay_gate"]["elapsed_s"] == 0.0
    assert results["census"]["replay_physical_rollouts"] == 0
    assert results["census"]["total_physical_rollouts"] == 0
    assert set(results) == set(
        x.execute_document_skeleton(plan, digest)["results"]
    )


def test_no_execute_mode_exit_leaves_the_run_unrecorded(tmp_path, plan):
    """Both pre-X0E execute exits persist an R0 artifact rather than only printing."""

    missing = tmp_path / "no_plan_here" / "plan.json"
    missing.parent.mkdir()
    assert x.main([
        "--mode", "execute", "--output-dir", str(tmp_path / "a"),
        "--plan", str(missing), "--approved-plan-sha256", "0" * 64,
        "--data-root", str(tmp_path),
        "--config", str(PACKET / "config" / "draft-config-v0.1.json"),
        "--schema", str(PACKET / "schema" / "schema.json"),
        "--assignment", str(PACKET / "config" / "proposed-gate3-assignment-v0.1.json"),
        "--protocol", str(PACKET / "protocol" / "protocol-p-v2.3.3.md"),
        "--extension", str(PACKET / "protocol" / "payload-boundary-extension-v0.2.md"),
    ]) == 1
    absent_plan = json.loads(
        (tmp_path / "a" / x.RESULT_FILENAME).read_text(encoding="utf-8")
    )
    assert absent_plan["results"]["outcome"] == x.OUTCOME_CONSTRUCTION
    assert absent_plan["results"]["terminal"]["stage_reached"] == "X0E"

    assert x.main([
        "--mode", "execute", "--output-dir", str(tmp_path / "b"),
        "--plan", str(missing), "--approved-plan-sha256", "0" * 64,
        "--data-root", str(tmp_path),
        "--config", str(PACKET / "config" / "draft-config-v0.1.json"),
        "--schema", str(PACKET / "schema" / "schema.json"),
        "--assignment", str(PACKET / "config" / "proposed-gate3-assignment-v0.1.json"),
        "--protocol", str(PACKET / "protocol" / "protocol-p-v2.3.3.md"),
        "--extension", str(tmp_path / "not-the-extension.md"),
    ]) == 1
    unbound = json.loads((tmp_path / "b" / x.RESULT_FILENAME).read_text(encoding="utf-8"))
    assert unbound["results"]["outcome"] == x.OUTCOME_CONSTRUCTION
    assert unbound["results"]["terminal"]["stage_reached"] == "X0E"


_FOREIGN_PLAN_HEAD = '{"mode":"plan","plan_valid":true,"terminal":null,"inputs":{"note":'


@pytest.mark.parametrize(
    "payload", [
        _FOREIGN_PLAN_HEAD + '1e9999}}',
        _FOREIGN_PLAN_HEAD + '"\\ud800"}}',
        _FOREIGN_PLAN_HEAD
        + '[' * (x.MAX_PLAN_JSON_DEPTH + 1) + '0'
        + ']' * (x.MAX_PLAN_JSON_DEPTH + 1) + '}}',
    ],
    ids=("overflowing-number", "lone-surrogate", "one-past-the-depth-gate"),
)
def test_an_unserializable_foreign_plan_still_persists_the_refusal(tmp_path, payload):
    """A read must fail before foreign content can poison the X6 failure writer.

    THE OFFENDING VALUE HAS TO SIT UNDER ``inputs``.  ``execute_document_skeleton``
    carries only ``inputs``, ``protocol`` and ``plan`` into the artifact, so a bad value
    under any other member name never reaches ``canonical_json`` and the pre-fix code
    writes a perfectly good artifact.  Measured against the reviewed state
    ``5a5b0562``: ``{"x":1e9999}`` returned rc=1 WITH an artifact, while the same value
    under ``inputs`` returned rc=None with none at all, and the lone surrogate left a
    truncated file behind.  A fixture has to be shaped for the defect it exposes.

    The depth case is a gate-existence regression, not a reproduction of a crash: the
    recursion threshold is a property of how deep the AMBIENT stack already is, not of
    this code.  Measured on the reviewed state: at zero extra frames a depth-960 plan
    under ``inputs`` still wrote its artifact; at 300 extra frames depth 800 returned
    rc=None with none.  The gate is what makes the outcome independent of the caller.
    """

    plan_path = tmp_path / "foreign.json"
    plan_path.write_text(payload, encoding="ascii")
    output = tmp_path / "out"
    assert x.main([
        "--mode", "execute", "--output-dir", str(output),
        "--plan", str(plan_path), "--approved-plan-sha256", "0" * 64,
        "--data-root", str(tmp_path),
        "--config", str(PACKET / "config" / "draft-config-v0.1.json"),
        "--schema", str(PACKET / "schema" / "schema.json"),
        "--assignment", str(PACKET / "config" / "proposed-gate3-assignment-v0.1.json"),
        "--protocol", str(PACKET / "protocol" / "protocol-p-v2.3.3.md"),
        "--extension", str(PACKET / "protocol" / "payload-boundary-extension-v0.2.md"),
    ]) == 1
    written = json.loads((output / x.RESULT_FILENAME).read_text(encoding="utf-8"))
    assert written["results"]["outcome"] == x.OUTCOME_CONSTRUCTION
    assert written["results"]["terminal"]["stage_reached"] == "X0E"
    reason = written["results"]["terminal"]["reason"]
    assert (
        "not canonical UTF-8 data" in reason
        or "exceeds maximum nesting depth" in reason
    )


@pytest.mark.parametrize(
    "required_args,missing_name",
    [
        (["--data-root", "unused"], "--approved-plan-sha256"),
        (["--approved-plan-sha256", "0" * 64], "--data-root"),
    ],
)
def test_missing_execute_authority_or_data_root_is_persisted(
    tmp_path, required_args, missing_name
):
    """X6 includes CLI refusals before the plan is read, not only later failures."""

    output = tmp_path / missing_name.removeprefix("--")
    code = x.main([
        "--mode", "execute", "--output-dir", str(output),
        "--config", str(PACKET / "config" / "draft-config-v0.1.json"),
        "--schema", str(PACKET / "schema" / "schema.json"),
        "--assignment", str(PACKET / "config" / "proposed-gate3-assignment-v0.1.json"),
        "--protocol", str(PACKET / "protocol" / "protocol-p-v2.3.3.md"),
        "--extension", str(PACKET / "protocol" / "payload-boundary-extension-v0.2.md"),
        *required_args,
    ])
    assert code == 1
    written = json.loads((output / x.RESULT_FILENAME).read_text(encoding="utf-8"))
    assert written["results"]["outcome"] == x.OUTCOME_CONSTRUCTION
    assert written["results"]["terminal"]["stage_reached"] == "X0E"
    assert missing_name in written["results"]["terminal"]["reason"]


_FOREIGN_PLANS = [
    ("windows", {"mode": "plan", "plan_valid": True, "terminal": None,
                 "inputs": {"config_path": r"C:\Users\person\config.json"}}),
    ("posix", {"mode": "plan", "plan_valid": True, "terminal": None,
               "inputs": {"config_path": "config/draft-config-v0.1.json"},
               "plan": {"note": "/home/person/plan.json"}}),
    ("windows-key", {"mode": "plan", "plan_valid": True, "terminal": None,
                     "inputs": {r"C:\Users\person\config.json": "foreign"}}),
    ("posix-key", {"mode": "plan", "plan_valid": True, "terminal": None,
                    "inputs": {"/home/person/plan.json": "foreign"}}),
    ("embedded-windows", {"mode": "plan", "plan_valid": True, "terminal": None,
                           "inputs": {"note":
                                      r"opaque-prefixC:\Users\person\config.json"}}),
    ("embedded-digit-drive", {"mode": "plan", "plan_valid": True, "terminal": None,
                               "inputs": {"note":
                                          r"opaque-prefix1:\Users\person\config.json"}}),
    # A UNC path glued to prose: the forward-slash rendering carried an outer token
    # boundary that the backslash rendering had already been shown not to need.
    ("embedded-unc-forward", {"mode": "plan", "plan_valid": True, "terminal": None,
                              "inputs": {"note":
                                         "opaque-prefix//host/person/config.json"}}),
    # A path with a SPACE in it -- "Program Files", "My Documents", and this repository's
    # own parent.  The match stopped at the space, so the reduction published everything
    # after it.
    ("windows-path-with-a-space", {"mode": "plan", "plan_valid": True, "terminal": None,
                                   "inputs": {"note":
                                              r"D:\My Documents\person\config.json"}}),
]


@pytest.mark.parametrize("flavour,foreign", _FOREIGN_PLANS, ids=[p[0] for p in _FOREIGN_PLANS])
def test_a_named_plan_carrying_a_machine_path_still_persists_the_refusal(
    tmp_path, flavour, foreign
):
    """X7 must not defeat X6: the terminal write cannot be the thing that fails.

    ``persist_execute_failure`` embeds the named plan's own content, and the writer
    refuses an absolute path anywhere in the document.  A plan this tool did not write
    can carry one, so before this test the refusal escaped ``main`` uncaught and NOTHING
    was persisted -- on the one exit whose entire purpose is "you named the wrong plan".
    """

    plan_path = tmp_path / "foreign.json"
    plan_path.write_text(json.dumps(foreign), encoding="utf-8")
    output = tmp_path / flavour
    assert x.main([
        "--mode", "execute", "--output-dir", str(output),
        "--plan", str(plan_path), "--approved-plan-sha256", "0" * 64,
        "--data-root", str(tmp_path),
        "--config", str(PACKET / "config" / "draft-config-v0.1.json"),
        "--schema", str(PACKET / "schema" / "schema.json"),
        "--assignment", str(PACKET / "config" / "proposed-gate3-assignment-v0.1.json"),
        "--protocol", str(PACKET / "protocol" / "protocol-p-v2.3.3.md"),
        "--extension", str(PACKET / "protocol" / "payload-boundary-extension-v0.2.md"),
    ]) == 1
    raw = (output / x.RESULT_FILENAME).read_text(encoding="utf-8")
    written = json.loads(raw)
    assert written["results"]["outcome"] == x.OUTCOME_CONSTRUCTION
    assert written["results"]["terminal"]["stage_reached"] == "X0E"
    # The redaction is disclosed rather than silent, and the path itself is gone.
    assert "was scrubbed (X7)" in written["results"]["terminal"]["reason"]
    assert "person" not in raw
    assert not re.search(r"[A-Za-z]:[\\/]", raw)


@pytest.mark.parametrize("foreign_inputs", ["foreign", ["foreign"], None])
def test_a_foreign_plan_with_nonobject_inputs_still_persists_the_refusal(
    tmp_path, foreign_inputs
):
    """Malformed foreign content must not raise outside the X6 persistence boundary."""

    foreign = {
        "mode": "plan", "plan_valid": True, "terminal": None,
        "inputs": foreign_inputs,
    }
    plan_path = tmp_path / "foreign.json"
    plan_path.write_text(json.dumps(foreign), encoding="utf-8")
    output = tmp_path / "nonobject"
    assert x.main([
        "--mode", "execute", "--output-dir", str(output),
        "--plan", str(plan_path), "--approved-plan-sha256", "0" * 64,
        "--data-root", str(tmp_path),
        "--config", str(PACKET / "config" / "draft-config-v0.1.json"),
        "--schema", str(PACKET / "schema" / "schema.json"),
        "--assignment", str(PACKET / "config" / "proposed-gate3-assignment-v0.1.json"),
        "--protocol", str(PACKET / "protocol" / "protocol-p-v2.3.3.md"),
        "--extension", str(PACKET / "protocol" / "payload-boundary-extension-v0.2.md"),
    ]) == 1
    written = json.loads((output / x.RESULT_FILENAME).read_text(encoding="utf-8"))
    assert written["inputs"] == foreign_inputs
    assert written["results"]["outcome"] == x.OUTCOME_CONSTRUCTION
    assert written["results"]["terminal"]["stage_reached"] == "X0E"


def test_a_nondigest_authority_argument_is_recorded_as_null_not_published(tmp_path):
    """The authority argument reaches the artifact before anything validates its shape."""

    output = tmp_path / "authority"
    assert x.main([
        "--mode", "execute", "--output-dir", str(output),
        "--approved-plan-sha256", r"C:\Users\person\not-a-digest",
        "--config", str(PACKET / "config" / "draft-config-v0.1.json"),
        "--schema", str(PACKET / "schema" / "schema.json"),
        "--assignment", str(PACKET / "config" / "proposed-gate3-assignment-v0.1.json"),
        "--protocol", str(PACKET / "protocol" / "protocol-p-v2.3.3.md"),
        "--extension", str(PACKET / "protocol" / "payload-boundary-extension-v0.2.md"),
    ]) == 1
    raw = (output / x.RESULT_FILENAME).read_text(encoding="utf-8")
    written = json.loads(raw)
    assert written["approved_plan_canonical_sha256"] is None
    assert "recorded as null" in written["results"]["terminal"]["reason"]
    assert "person" not in raw


def test_the_scrubber_removes_a_double_slash_rooted_path(tmp_path):
    """``//host/share`` is absolute to BOTH PurePath flavours, so it must be scrubbed."""

    scrubbed = x.scrub_machine_paths(
        "ProtocolPError: pinned input is absent: //server/share/data/row.npz"
    )
    assert "server" not in scrubbed
    assert scrubbed.endswith("row.npz")
    # Nothing absolute may survive, in either flavour, for any of these renderings.
    for raw in (r"C:\Users\person\row.npz", "C:/Users/person/row.npz",
                r"\\server\share\row.npz", "//server/share/row.npz",
                "/home/person/row.npz", "//home//person/row.npz"):
        tail = x.scrub_machine_paths(f"absent: {raw}").split(": ")[-1]
        assert not PureWindowsPath(tail).is_absolute()
        assert not PurePosixPath(tail).is_absolute()
        # and the writer, whose guard reads whole strings, accepts the result
        x.write_canonical_document(tmp_path / "probe.json", {"reason": tail})


def test_the_scrubber_leaves_a_url_intact():
    """A URL scheme separator is not a drive letter and ``//`` is not a UNC root."""

    for url in ("see https://example.org/spec#x for the definition",
                "mirror http://host/a/b listed",
                "clone git+ssh://host/repo.git now"):
        assert x.scrub_machine_paths(url) == url
        # Pin the mechanism, not only the outcome: the drive-letter form must not match
        # inside a word, which is what turned "https://" into drive "s" before.
        assert x._WINDOWS_ABSOLUTE.sub("<W>", url) == url
        assert x._POSIX_ABSOLUTE.sub("<P>", url) == url


def test_no_execute_exit_is_silent_on_the_console(tmp_path, plan, capsys):
    """The X0E-mismatch and XR exits returned 1 with nothing printed at all.

    Silent failure is the packet's named worst case.  Both branches persisted their
    artifact correctly and told the operator nothing, and the XR one is the exit that has
    already spent the replay rollout.  The X0E-mismatch branch had no test of any kind:
    a plan whose OWN digest is named passes the authorization check and still fails the
    recompute, which is exactly the state that branch exists for.
    """

    mismatched = dict(plan)
    mismatched["plan"] = dict(mismatched["plan"])
    mismatched["plan"]["ladder"] = list(reversed(mismatched["plan"]["ladder"]))
    mismatched_path = tmp_path / "mismatched.json"
    x.write_canonical_document(mismatched_path, mismatched)
    assert x.main([
        "--mode", "execute", "--output-dir", str(tmp_path / "x0e"),
        "--plan", str(mismatched_path),
        "--approved-plan-sha256", x.canonical_document_sha256(mismatched),
        "--data-root", str(tmp_path / "absent_data_root"),
        "--config", str(PACKET / "config" / "draft-config-v0.1.json"),
        "--schema", str(PACKET / "schema" / "schema.json"),
        "--assignment", str(PACKET / "config" / "proposed-gate3-assignment-v0.1.json"),
        "--protocol", str(PACKET / "protocol" / "protocol-p-v2.3.3.md"),
        "--extension", str(PACKET / "protocol" / "payload-boundary-extension-v0.2.md"),
    ]) == 1
    x0e = json.loads((tmp_path / "x0e" / x.RESULT_FILENAME).read_text(encoding="utf-8"))
    assert x0e["results"]["outcome"] == x.OUTCOME_CONSTRUCTION
    assert x0e["results"]["terminal"]["stage_reached"] == "X0E"
    assert "differs from the approved plan" in x0e["results"]["terminal"]["reason"]
    assert "FAILED" in capsys.readouterr().out

    plan_path, digest = _write_plan(tmp_path, plan)
    assert x.main([
        "--mode", "execute", "--output-dir", str(tmp_path / "xr"),
        "--plan", str(plan_path), "--approved-plan-sha256", digest,
        "--data-root", str(tmp_path / "absent_data_root"),
        "--config", str(PACKET / "config" / "draft-config-v0.1.json"),
        "--schema", str(PACKET / "schema" / "schema.json"),
        "--assignment", str(PACKET / "config" / "proposed-gate3-assignment-v0.1.json"),
        "--protocol", str(PACKET / "protocol" / "protocol-p-v2.3.3.md"),
        "--extension", str(PACKET / "protocol" / "payload-boundary-extension-v0.2.md"),
    ]) == 1
    xr = json.loads((tmp_path / "xr" / x.RESULT_FILENAME).read_text(encoding="utf-8"))
    assert xr["results"]["outcome"] == x.OUTCOME_REPLAY
    assert "FAILED" in capsys.readouterr().out


def test_persisted_reasons_carry_no_machine_path(tmp_path, plan):
    """X7 is about what the artifact records, not about whether a string IS a path."""

    plan_path, digest = _write_plan(tmp_path, plan)
    x.main([
        "--mode", "execute", "--output-dir", str(tmp_path),
        "--plan", str(plan_path), "--approved-plan-sha256", digest,
        "--data-root", str(tmp_path / "absent_data_root"),
        "--config", str(PACKET / "config" / "draft-config-v0.1.json"),
        "--schema", str(PACKET / "schema" / "schema.json"),
        "--assignment", str(PACKET / "config" / "proposed-gate3-assignment-v0.1.json"),
        "--protocol", str(PACKET / "protocol" / "protocol-p-v2.3.3.md"),
        "--extension", str(PACKET / "protocol" / "payload-boundary-extension-v0.2.md"),
    ])
    raw = (tmp_path / x.RESULT_FILENAME).read_text(encoding="utf-8")
    # The reason quotes the absent pinned input, which is an absolute path mid-sentence.
    # The writer's own guard asks whether a string IS a path and passes every such
    # sentence, so the artifact is what has to be checked.
    assert "absent" in raw
    assert not re.search(r"[A-Za-z]:[\\/]", raw)
    assert str(PACKET.drive) not in raw or PACKET.drive == ""


def test_scrubber_rewrites_a_path_inside_a_sentence_and_leaves_prose_alone():
    quoted = rf"ProtocolPError: pinned input is absent: {PACKET}\plant\row.npz"
    assert not Path(quoted).is_absolute()  # the writer's guard cannot see this
    scrubbed = x.scrub_machine_paths(quoted)
    assert "<repo>" in scrubbed
    assert not re.search(r"[A-Za-z]:[\\/]", scrubbed)
    assert x.scrub_machine_paths("XA -> XM-C -> XL -> XM-B -> XZ") == (
        "XA -> XM-C -> XL -> XM-B -> XZ"
    )
    posix = "ProtocolPError: pinned input is absent: /home/person/data/plant/row.npz"
    posix_scrubbed = x.scrub_machine_paths(posix)
    assert "/home/person" not in posix_scrubbed
    assert not re.search(r"(?:^|[\s:=('])/(?!/)", posix_scrubbed)
    # A Windows path can follow opaque prose with no delimiter.  A boundary on the drive
    # letter misses it even though the backslash makes this unambiguously a filesystem
    # path rather than a URI scheme.
    embedded = r"ProtocolPError: opaque-prefixC:\Users\person\plant\row.npz"
    embedded_scrubbed = x.scrub_machine_paths(embedded)
    assert "person" not in embedded_scrubbed
    assert embedded_scrubbed.endswith("row.npz")
    # The shared predicate deliberately follows ``PureWindowsPath``, which accepts any
    # one-character drive prefix, not only A-Z.  The embedded form must follow the same
    # rule; otherwise the scrubber, authorization gate and writer all publish it.
    digit_drive = r"ProtocolPError: opaque-prefix1:\PRIVATE\plant\row.npz"
    digit_drive_scrubbed = x.scrub_machine_paths(digit_drive)
    assert "PRIVATE" not in digit_drive_scrubbed
    assert digit_drive_scrubbed.endswith("row.npz")
    # A UNC path glued to prose.  The backslash rendering never needed a token boundary;
    # the forward-slash one carried one, and its OWN scheme lookbehind is what keeps
    # "https://" safe, so the boundary was only hiding this.
    unc = "ProtocolPError: opaque-prefix//host/PRIVATE/plant/row.npz"
    unc_scrubbed = x.scrub_machine_paths(unc)
    assert "PRIVATE" not in unc_scrubbed
    assert unc_scrubbed.endswith("row.npz")
    # A mixed-separator path.  ``PurePosixPath`` cannot see the backslash, so its ``name``
    # kept the parent directory; the reduction has to split on BOTH separators.
    mixed = r"ProtocolPError: opaque-prefixC:/PRIVATE\plant\row.npz"
    mixed_scrubbed = x.scrub_machine_paths(mixed)
    assert "PRIVATE" not in mixed_scrubbed
    assert mixed_scrubbed.endswith("row.npz")
    # THE SAME REDUCTION, REACHED THROUGH THE POSIX RULE.  The drive-rendered case above
    # stopped exercising ``_final_component`` the moment the forward-slash drive form
    # dropped its token boundary: the Windows rule now consumes it first, so the test
    # passes for a reason that has nothing to do with the split.  A mutation sweep found
    # exactly that -- splitting on "/" alone SURVIVED the whole focused suite.  This case
    # carries no drive letter, so only the POSIX rule can match it, and the parent
    # directory comes back if the reduction stops seeing backslashes.
    posix_mixed = r"OSError: cannot open /mnt/PRIVATE\plant\row.npz"
    posix_mixed_scrubbed = x.scrub_machine_paths(posix_mixed)
    assert "PRIVATE" not in posix_mixed_scrubbed, posix_mixed_scrubbed
    assert posix_mixed_scrubbed.endswith("row.npz")
    assert x._final_component(r"/mnt/PRIVATE\row.npz") == "row.npz"


_PATHS_CONTAINING_A_SPACE = [
    r"ProtocolPError: pinned input is absent: D:\My Data\PRIVATE\row.npz",
    r"C:\Program Files\PRIVATE\row.npz",
    r"OSError: cannot open \\host\My Share\PRIVATE\row.npz",
    r"E:\A B\C D\PRIVATE\row.npz",
]


@pytest.mark.parametrize("sentence", _PATHS_CONTAINING_A_SPACE)
def test_a_path_containing_a_space_is_reduced_to_its_final_component(sentence):
    """The likeliest leak in this file, because directory names with spaces are ordinary.

    The tail stopped at the first whitespace, so the substitution only ever saw the first
    space-free RUN of the path and everything after the space stayed in the message.
    MEASURED before the fix: r"D:\\My Data\\PRIVATE\\row.npz" became
    r"My Data\\PRIVATE\\row.npz" -- which is RELATIVE, so neither the writer's guard nor
    the post-condition can see it, and it is published.  "Program Files" and this
    repository's own parent directory both contain a space.

    The tail may cross a space only when a BACKSLASH still lies ahead of the next
    whitespace.  That gate cannot fire on this project's prose, which is forward-slashed,
    and the accept side of that claim is the next test rather than this one.
    """

    scrubbed = x.scrub_machine_paths(sentence)
    assert "PRIVATE" not in scrubbed
    assert scrubbed.endswith("row.npz")
    assert scrubbed != "<path>"
    assert not x._records_absolute_path(scrubbed)


_PROSE_THE_SPACE_GATE_MUST_NOT_TOUCH = [
    "XA -> XM-C -> XL -> XM-B -> XZ",
    "probe 0.10 N / 0.25 ramp",
    "reserved for dev/pilot/val and test",
    "suites C1/S differ in what is observed",
    "the ratio is 1/2 and the duty cycle 24/7",
    "healthy/faulted readback distinguishes a measured null",
    "see https://example.org/spec#x for the definition",
    "no path here at all, just prose about a\\b escapes",
]


@pytest.mark.parametrize("sentence", _PROSE_THE_SPACE_GATE_MUST_NOT_TOUCH)
def test_the_space_gate_leaves_this_project_s_own_vocabulary_alone(sentence):
    """A false positive in a scrubber is worse than a leak: nothing discloses the loss."""

    assert x.scrub_machine_paths(sentence) == sentence


_PROSE_AFTER_A_REAL_PATH = [
    (r"absent: C:\a\row.npz over dev/pilot/val", "row.npz over dev/pilot/val"),
    (r"absent: C:\a\row.npz and/or the other one", "row.npz and/or the other one"),
    (r"absent: C:\a\row.npz see a\b", r"row.npz see a\b"),
    (r"absent: C:\a\row.npz vs D:\b\row.npz", "row.npz vs row.npz"),
]


@pytest.mark.parametrize("sentence,expected_tail", _PROSE_AFTER_A_REAL_PATH)
def test_the_space_gate_stops_at_the_end_of_a_real_path(sentence, expected_tail):
    """The adversarial side: a REAL path followed by a token that contains a slash.

    The gate is a BACKSLASH lookahead precisely so this project's forward-slashed
    vocabulary cannot extend a match past the end of the path.  A gate on any separator
    would swallow "and/or" and "dev/pilot/val" here and leave a reason that reads as
    though it had always been that short.
    """

    scrubbed = x.scrub_machine_paths(sentence)
    assert scrubbed.endswith(expected_tail), scrubbed
    assert not x._records_absolute_path(scrubbed)


def test_ambiguous_forward_slash_boundaries_stay_disclosed_and_symmetric():
    """DISCLOSED limitations, pinned so nobody closes them by corrupting vocabulary.

    Every other rooted form lost its outer token boundary once it was shown that a path
    glued to a word is published whole.  The single-slash POSIX form keeps its boundary,
    and a space-containing rooted path crosses the space only when a backslash still lies
    ahead.  The spellings below are therefore NOT fully covered.  The reason is measurable:
    a boundary-free single-slash rule matches the "/" in "dev/pilot/val" and reduces the
    whole phrase to "val"; a space gate widened to either separator consumes the same
    vocabulary when it follows a real path.

    The gap is bounded and it is symmetric on purpose -- the writer's guard uses the same
    pattern, so after reduction it does not refuse these relative survivors either.  If
    only one side were widened, X7 would fire while X6 was writing the record, which is the
    failure this whole family of fixes exists to prevent.
    """

    # What the boundary buys, and why it is not negotiable.
    for phrase in ("dev/pilot/val", "C1/S", "1/2", "and/or"):
        assert x.scrub_machine_paths(phrase) == phrase
    # What it costs.  The first two remain as written and the other three retain a
    # relative suffix; the scrubber and the guard AGREE on each survivor, which is what
    # keeps the record writable.
    uncovered = (
        "opaque-prefix/PRIVATE/row.npz",
        "OSError: cannot open /mnt/My Data/PRIVATE/row.npz",
        "opaque-prefixD:/My Data/PRIVATE/row.npz",
        r"opaque-prefixD:\My Data/PRIVATE/row.npz",
        "opaque-prefix//host/My Share/PRIVATE/row.npz",
    )
    for source in uncovered:
        scrubbed = x.scrub_machine_paths(source)
        assert "PRIVATE" in scrubbed
        assert not x._records_absolute_path(scrubbed)
    # And the covered shapes of the same family, so the gap is not read wider than it is.
    assert x.scrub_machine_paths("at /PRIVATE/row.npz") == "at row.npz"
    assert x.scrub_machine_paths("opaque-prefix//host/PRIVATE/row.npz").endswith("row.npz")
    assert "PRIVATE" not in x.scrub_machine_paths(r"opaque-prefixC:\PRIVATE\row.npz")


_A_UNC_PATH_AFTER_A_LETTER_COLON = [
    ("reason://host/PRIVATE/row.npz", True),
    ("ProtocolPError: reason://host/PRIVATE/row.npz was rejected", True),
    ("input://host/PRIVATE/row.npz", True),
    ("file://host/PRIVATE/row.npz", True),
    # A space puts this one in the DISCLOSED whitespace family, so the marker survives in a
    # relative suffix.  It is here because the root must go even so: this exact sentence
    # used to be published whole, host included.
    ("note://host/My Share/PRIVATE/row.npz", False),
]


@pytest.mark.parametrize("sentence,marker_gone", _A_UNC_PATH_AFTER_A_LETTER_COLON)
def test_a_unc_path_after_a_letter_colon_is_not_mistaken_for_a_url(sentence, marker_gone):
    """A COMPLETE ROOTED PATH used to be published here, and both sides agreed to it.

    The forward-UNC lookbehind refused any alphanumeric-plus-colon, which is a much wider
    claim than "this is a URL".  Glue a real UNC path onto a word ending in a colon and
    the pattern declined, the writer's guard -- which shares the pattern -- also declined,
    and the artifact was written with the host, the private directory and the file name
    intact.  What makes this test red is restoring that lookbehind: the sentence comes back
    unchanged and the assertion below sees the marker.

    ``file`` is in this list on purpose.  It is a real URI scheme and it is deliberately
    NOT protected, because ``file://host/share`` is a path spelled as a URL.
    """

    scrubbed = x.scrub_machine_paths(sentence)
    assert "//host" not in scrubbed, scrubbed
    if marker_gone:
        assert "PRIVATE" not in scrubbed, scrubbed
    assert scrubbed != "<path>"
    assert not x._records_absolute_path(scrubbed)


@pytest.mark.parametrize("scheme", x._URI_SCHEMES)
@pytest.mark.parametrize("case", (str.lower, str.upper, str.title))
def test_every_protected_scheme_survives_the_scrub(scheme, case):
    """The accept side of the whitelist, asserted over the CONSTANT rather than examples.

    Dropping a scheme from ``_URI_SCHEMES`` makes exactly this red, which is the point: the
    list is the whole decision, so the test has to read it rather than restate it.  The
    scheme match is case-insensitive because a URL's scheme is, and a reason string may
    quote one in any case.
    """

    url = f"{case(scheme)}://example.org/dir/file.txt"
    sentence = f"see {url} for the definition"
    assert x.scrub_machine_paths(url) == url
    assert x.scrub_machine_paths(sentence) == sentence


@pytest.mark.parametrize("scheme", ("myscheme", "note", "reason", "file"))
def test_an_unlisted_scheme_is_reduced_like_a_path_and_that_is_the_disclosed_cost(scheme):
    """THE CONVERSE COST OF THE WHITELIST, pinned so it is not discovered later as a bug.

    A URL host and a UNC host are lexically identical, so a name-based decision cannot be
    avoided -- only stated.  Everything outside ``_URI_SCHEMES`` is treated as a path, which
    means an unlisted scheme's URL loses everything but its final component.  The scrubber's
    docstring says so; this is the test that keeps the two together.
    """

    scrubbed = x.scrub_machine_paths(f"{scheme}://host/dir/file.txt")
    assert scrubbed == f"{scheme}:file.txt"


_A_DRIVE_PATH_GLUED_TO_PROSE = [
    r"opaque-prefixC:/My Data\PRIVATE\row.npz",
    r"run1C:/My Data\PRIVATE\row.npz",
    r"opaque-prefixC:/PRIVATE\row.npz",
    r"prefixD:/Program Files\PRIVATE\row.npz",
]


@pytest.mark.parametrize("sentence", _A_DRIVE_PATH_GLUED_TO_PROSE)
def test_a_drive_path_glued_to_prose_leaves_no_drive_designator(sentence):
    """The forward-slash drive form refuses a SECOND slash instead of demanding a boundary.

    With the old token boundary this rule could not fire inside a word, the POSIX rule then
    matched only the first space-free run after the drive colon, and the output kept the
    DRIVE DESIGNATOR with the whole directory path behind it
    (r"opaque-prefixC:My Data\\PRIVATE\\row.npz").  Restoring ``(?<![A-Za-z0-9])`` is what
    makes this red.  A URL is still safe because its scheme separator is always "://",
    which ``(?!/)`` declines -- that property is asserted by the scheme tests above.
    """

    scrubbed = x.scrub_machine_paths(sentence)
    assert "PRIVATE" not in scrubbed, scrubbed
    assert ":" not in scrubbed, scrubbed
    assert not x._records_absolute_path(scrubbed)


_RENDERINGS_OF_ONE_PRIVATE_PATH = (
    r"C:\PRIVATE\row.npz", r"C:\My Data\PRIVATE\row.npz",
    r"D:\My Data\Program Files\PRIVATE\row.npz", "C:/PRIVATE/row.npz",
    r"C:/PRIVATE\row.npz", r"C:/My Data\PRIVATE\row.npz",
    r"1:\PRIVATE\row.npz", r"1:\My Data\PRIVATE\row.npz", "1:/PRIVATE/row.npz",
    r"\\host\PRIVATE\row.npz", r"\\host\My Share\PRIVATE\row.npz",
    "//host/PRIVATE/row.npz", "///mnt/PRIVATE/row.npz",
)
_THINGS_THAT_CAN_PRECEDE_A_PATH = (
    "", "opaque-prefix", "at ", "OSError: cannot open ", "reason:", "run1",
    "ProtocolPError: pinned input is absent: ", "'", "(", "path=", "[",
)
_THINGS_THAT_CAN_FOLLOW_A_PATH = ("", " was rejected", ".", " for dev/pilot/val and C1/S")


def test_no_rendering_of_a_private_path_survives_rooted_in_any_company():
    """THE PROPERTY OVER THE SPACE, not another example.

    Six consecutive review rounds found this same class one input family further out, and
    every individual fix was correct; what was missing each time was an assertion over the
    space of inputs.  This is that assertion: every rendering above, crossed with everything
    that can precede and follow it in a real refusal sentence, must come back with no rooted
    private path in it and must satisfy the writer's guard.

    Deliberately NOT asserted here: that the marker is gone.  Three ambiguities are
    disclosed in ``scrub_machine_paths`` and they leave a RELATIVE suffix; those are pinned
    by the disclosure test above.  What this pins is the stronger property that nothing
    ROOTED survives -- which is what X7 exists for -- so a future widening that trades a
    disclosed relative suffix for a published root fails here.
    """

    rooted = re.compile(r"(?:[A-Za-z0-9]:[\\/]|\\\\|(?:^|[^A-Za-z0-9])//?)[^\s]*PRIVATE")
    offenders = []
    for rendering in _RENDERINGS_OF_ONE_PRIVATE_PATH:
        for prefix in _THINGS_THAT_CAN_PRECEDE_A_PATH:
            for suffix in _THINGS_THAT_CAN_FOLLOW_A_PATH:
                source = prefix + rendering + suffix
                scrubbed = x.scrub_machine_paths(source)
                if rooted.search(scrubbed) or x._records_absolute_path(scrubbed):
                    offenders.append((source, scrubbed))
    assert not offenders, offenders[:5]


_PROSE_LOSING_ITS_WHOLE_TEXT = [
    (r"read row1C:/plant/\row.npz", "read "),
    (r"ProtocolPError: pinned input absent at run1C:/data/\gate3.npz",
     "ProtocolPError: pinned input absent at "),
    (r"value 1C:/\ was rejected", "value "),
    ("ProtocolPError: pinned input absent at ///data/gate3.npz",
     "ProtocolPError: pinned input absent at "),
]


@pytest.mark.parametrize("sentence,surviving_prefix", _PROSE_LOSING_ITS_WHOLE_TEXT)
def test_a_reason_survives_the_substitution_instead_of_being_thrown_away(
    sentence, surviving_prefix
):
    """A rewriting rule can build the path another rule already declined, and then the
    only exit left discards the whole reason.

    The first three sentences are the Session-68 mechanism: the POSIX rule reduced
    ``/plant/\\row.npz`` to ``\\row.npz`` and re-emitted it after the boundary character,
    rebuilding ``C:\\row.npz`` inside prose the Windows rule had been offered and
    declined.  That mechanism is now closed at its source -- ``_final_component`` splits
    on BOTH separators, so the replacement cannot re-emit one -- and those three sentences
    survive a single pass.  They are kept as regression cases, not as the demonstration.

    The fourth is the mechanism that is still live and is why the fixpoint stays: a
    repeated root reduces to ``/gate3.npz``, which is still recorded and still relative
    as a whole.  MEASURED over the 37,448 enumerated strings with one pass: 969 remain
    absolute and ten reach the discard exit.  Whichever the mechanism, the cost is the
    same and it is the worst kind -- the reader gets ``"<path>"`` and nothing tells them
    a reason was lost.
    """

    scrubbed = x.scrub_machine_paths(sentence)
    assert scrubbed != "<path>"
    assert scrubbed.startswith(surviving_prefix)
    assert not x._records_absolute_path(scrubbed)


def test_one_substitution_pass_is_measurably_not_enough():
    """The fixpoint's reason is DRIVEN, not asserted in a docstring.

    ``_substitution_pass`` exists so this test can run exactly one pass and look at what
    it leaves behind, rather than keeping a second copy of the substitution here (which
    would agree with itself) or claiming the shortfall in prose (which stops being true
    the moment the substitution changes -- and it did change this session).
    """

    once = x._substitution_pass("ProtocolPError: pinned input absent at ///data/gate3.npz")
    # Still recorded, and relative as a whole -- which is the state whose ONLY exit in
    # ``scrub_machine_paths`` throws the entire message away.
    assert x._records_absolute_path(once)
    assert not PureWindowsPath(once).is_absolute()
    assert not PurePosixPath(once).is_absolute()
    # The fixpoint takes the same input to a reason a reader can still use.
    assert x.substitute_known_path_spellings(once) != once
    assert x.scrub_machine_paths(once).endswith("gate3.npz")


_SCRUBBER_ALPHABET = ("/", "\\", "C", ":", "x", " ", ".", "1")


def test_the_scrubber_output_is_never_absolute_to_either_flavour():
    """The scrubber's contract is the WRITER'S GUARD, so state it as that predicate.

    The two patterns are an enumeration of path spellings and the guard is a predicate
    over ``PurePath``.  Wherever they disagree, X7 fires while X6 is writing the record
    and the artifact is destroyed -- so the property is a post-condition, and the way to
    check a post-condition is to enumerate the input space rather than pick examples.
    Over 37,448 strings this was measured at 1,358 counterexamples before the fix.
    """

    for length in range(1, 6):
        for combo in itertools.product(_SCRUBBER_ALPHABET, repeat=length):
            scrubbed = x.scrub_machine_paths("".join(combo))
            assert not x._records_absolute_path(scrubbed), combo
            assert not PureWindowsPath(scrubbed).is_absolute(), combo
            assert not PurePosixPath(scrubbed).is_absolute(), combo


def test_the_whole_message_discard_is_a_last_resort_and_not_a_working_path():
    """The enumeration above is satisfied by returning "<path>" for everything.

    ``scrub_machine_paths`` ends with a branch that throws the WHOLE message away when a
    pattern still matches but the string is not itself rooted, because nothing can be
    reduced at that point.  It keeps the writer's guard true and it costs the reader the
    entire reason, so the property worth pinning is that no input reaches it -- not that
    the output is clean, which the discard guarantees trivially.  Measured with a single
    substitution pass: six of these strings reached it.  With the fixpoint: none.
    """

    reached = []
    for length in range(1, 6):
        for combo in itertools.product(_SCRUBBER_ALPHABET, repeat=length):
            source = "".join(combo)
            after = x.substitute_known_path_spellings(source)
            if (
                x._records_absolute_path(after)
                and not PureWindowsPath(after).is_absolute()
                and not PurePosixPath(after).is_absolute()
            ):
                reached.append((source, after))
    assert reached == [], reached[:6]


def test_bare_roots_and_nonletter_drive_prefixes_are_reduced_not_left_alone():
    """Pin the MECHANISM of the fallback and the shared drive-prefix semantics.

    A later edit could satisfy the enumeration above by making the fallback swallow
    everything.  These cases fix what each input family must become.
    """

    # (1) A bare root: no path component follows the separator, so neither pattern has
    # anything to match, and nothing survives the reduction either.
    for root in ("/", "//", "///", "\\\\"):
        assert x.scrub_machine_paths(root) == "<path>"
    # (2) A non-letter drive prefix that PureWindowsPath accepts.  The shared pattern now
    # catches both whole-string and embedded forms; the directory must not be published.
    for drive in ("1", ".", ":", " "):
        assert x.scrub_machine_paths(rf"{drive}:\PRIVATE\row.npz") == "row.npz"
    # The reduction must use the flavour that calls the string absolute: the POSIX parser
    # sees no separator at all in a Windows-rooted string, so ITS name is the whole value.
    assert PurePosixPath(r"1:\PRIVATE\row.npz").name == r"1:\PRIVATE\row.npz"
    # And one reduction per flavour is not enough -- the POSIX name of "/ :\\" is " :\\",
    # which is absolute to the OTHER flavour.  This is why the post-condition is a fixpoint.
    assert PurePosixPath("/ :\\").name == " :\\"
    assert PureWindowsPath(" :\\").is_absolute()
    assert x.scrub_machine_paths("/ :\\") == "<path>"
    # Prose, ratios, arrows and URLs are untouched by the fallback, because none of them
    # is absolute as a whole string.
    for intact in ("probe 0.10 N / 0.25 ramp", "XA -> XM-C -> XZ",
                   "see https://example.org/spec#x for the definition"):
        assert x.scrub_machine_paths(intact) == intact


_ROOTED_PLANS = [
    ("bare-root-value", {"inputs": {"note": "/"}}),
    ("bare-root-key", {"inputs": {"/": "note"}}),
    ("double-slash-value", {"inputs": {"note": "//"}}),
    ("digit-drive-value", {"inputs": {"note": r"1:\PRIVATE\row.npz"}}),
    ("digit-drive-key", {"inputs": {r"1:\PRIVATE\row.npz": "note"}}),
    ("nested-in-list", {"plan": {"rows": [{"note": "/"}]}}),
]


@pytest.mark.parametrize("flavour,foreign", _ROOTED_PLANS, ids=[p[0] for p in _ROOTED_PLANS])
def test_a_plan_carrying_a_root_the_patterns_miss_still_persists_the_refusal(
    tmp_path, flavour, foreign
):
    """X7 defeating X6 again, one layer below the scrub that was added to prevent it.

    The scrub closed every path spelling the two patterns recognise.  These six shapes
    are absolute to the writer's guard and invisible to both patterns, so before this the
    guard raised while persisting the record it was protecting: return code ``None``, a
    traceback, and nothing on disk.
    """

    document = {"mode": "plan", "plan_valid": True, "terminal": None}
    document.update(foreign)
    plan_path = tmp_path / "foreign.json"
    plan_path.write_text(json.dumps(document), encoding="utf-8")
    output = tmp_path / flavour
    assert x.main([
        "--mode", "execute", "--output-dir", str(output),
        "--plan", str(plan_path), "--approved-plan-sha256", "0" * 64,
        "--data-root", str(tmp_path),
        "--config", str(PACKET / "config" / "draft-config-v0.1.json"),
        "--schema", str(PACKET / "schema" / "schema.json"),
        "--assignment", str(PACKET / "config" / "proposed-gate3-assignment-v0.1.json"),
        "--protocol", str(PACKET / "protocol" / "protocol-p-v2.3.3.md"),
        "--extension", str(PACKET / "protocol" / "payload-boundary-extension-v0.2.md"),
    ]) == 1
    raw = (output / x.RESULT_FILENAME).read_text(encoding="utf-8")
    written = json.loads(raw)
    assert written["results"]["outcome"] == x.OUTCOME_CONSTRUCTION
    assert written["results"]["terminal"]["stage_reached"] == "X0E"
    # The redaction stays disclosed, and the directory portion is gone.
    assert "was scrubbed (X7)" in written["results"]["terminal"]["reason"]
    assert "PRIVATE" not in raw


def test_two_paths_with_one_basename_keep_both_members_of_the_evidence_record():
    """The key-collision loop had no test that could make it red.

    Redaction reduces a path to its final component, so two different machine paths used
    as member names collapse onto one key.  Without the loop the second member overwrites
    the first and a field of the persisted evidence disappears with no error and no
    disclosure -- a silent exclusion inside a record whose only job is to be evidence.
    """

    collide = {r"C:\DIR_A\row.npz": 1, r"C:\DIR_B\row.npz": 2, "/DIR_C/row.npz": 3}
    scrubbed, changed = x._scrub_embedded_strings(collide)
    assert changed is True
    assert len(scrubbed) == len(collide), "a member was silently dropped"
    assert list(scrubbed.values()) == [1, 2, 3]
    assert list(scrubbed) == [
        "row.npz", "row.npz [redacted-key-2]", "row.npz [redacted-key-3]"
    ]
    # Deterministic: the same input must produce the same record every time.
    assert x._scrub_embedded_strings(collide)[0] == scrubbed
    # And the disclosure survives the collision path: nothing here is silent.
    assert "DIR_A" not in json.dumps(scrubbed)


_AUTHORIZED_SHAPED_PLANS = [
    ("value", {"inputs": {"config_path": r"C:\PRIVATE\config.json"}}),
    ("key", {"inputs": {r"C:\PRIVATE\config.json": "foreign"}}),
    ("posix-value", {"plan": {"note": "/PRIVATE/plan.json"}}),
    ("embedded-windows", {"inputs": {
        "note": r"opaque-prefixC:\PRIVATE\config.json"
    }}),
    ("embedded-digit-drive", {"inputs": {
        "note": r"opaque-prefix1:\PRIVATE\config.json"
    }}),
    ("embedded-unc-forward", {"inputs": {
        "note": "opaque-prefix//host/PRIVATE/config.json"
    }}),
    ("windows-path-with-a-space", {"inputs": {
        "note": r"D:\My Documents\PRIVATE\config.json"
    }}),
]


@pytest.mark.parametrize(
    "flavour,foreign", _AUTHORIZED_SHAPED_PLANS,
    ids=[p[0] for p in _AUTHORIZED_SHAPED_PLANS],
)
def test_a_plan_named_by_its_own_digest_is_refused_before_it_reaches_the_writer(
    tmp_path, flavour, foreign
):
    """The authorized path embeds the plan VERBATIM, so the gate owes it a check.

    Authorization is "the operator named this document's canonical digest", which a
    foreign document can satisfy.  Everything past that point copies the plan into the
    artifact unscrubbed, and the terminal write then raises X7 and persists nothing --
    return code ``None``, a traceback, no record.  Refusing at the gate is not a rewrite
    of approved content: the refusal routes to the exit that scrubs, so X6 still holds.
    """

    document = {"mode": "plan", "plan_valid": True, "terminal": None}
    document.update(foreign)
    digest = x.canonical_document_sha256(document)
    plan_path = tmp_path / "authorized.json"
    plan_path.write_text(json.dumps(document), encoding="utf-8")
    output = tmp_path / flavour
    assert x.main([
        "--mode", "execute", "--output-dir", str(output),
        "--plan", str(plan_path), "--approved-plan-sha256", digest,
        "--data-root", str(tmp_path),
        "--config", str(PACKET / "config" / "draft-config-v0.1.json"),
        "--schema", str(PACKET / "schema" / "schema.json"),
        "--assignment", str(PACKET / "config" / "proposed-gate3-assignment-v0.1.json"),
        "--protocol", str(PACKET / "protocol" / "protocol-p-v2.3.3.md"),
        "--extension", str(PACKET / "protocol" / "payload-boundary-extension-v0.2.md"),
    ]) == 1
    raw = (output / x.RESULT_FILENAME).read_text(encoding="utf-8")
    written = json.loads(raw)
    assert written["results"]["outcome"] == x.OUTCOME_CONSTRUCTION
    assert written["results"]["terminal"]["stage_reached"] == "X0E"
    # Requirement (ee): the sentence must be the GATE'S, not the writer's, as rendered.
    reason = written["results"]["terminal"]["reason"]
    assert "cannot be an X0P artifact this tool wrote" in reason
    assert "result artifact contains" not in reason
    assert "PRIVATE" not in raw


def test_the_gate_and_the_writer_ask_one_function_the_same_question():
    """Requirement (r): the gate exists to guarantee what the writer will accept.

    Two copies of "is this absolute" would drift, and the drift is invisible until a
    document passes one and fails the other -- which is the exact shape that destroyed
    the artifact in the first place.
    """

    for probe in ({"a": r"C:\dir\row.npz"}, {r"C:\dir\row.npz": "a"},
                  {"a": ["b", {"c": "/dir/row.npz"}]}, {"a": "//host/share"},
                  {"a": r"opaque-prefixC:\PRIVATE\row.npz"},
                  {"a": r"opaque-prefix1:\PRIVATE\row.npz"},
                  {"a": "opaque-prefix//host/PRIVATE/row.npz"},
                  {"a": r"D:\My Documents\PRIVATE\row.npz"}):
        assert x.absolute_path_strings(probe), probe
        with pytest.raises(ProtocolPError, match="X7: result artifact contains"):
            x.write_canonical_document(Path("unused"), probe)
    # A legitimate plan trips neither, and that is the accept side.
    assert x.absolute_path_strings({"a": "row.npz", "b": ["0.10 N / 0.25", "A -> B"]}) == []


def test_a_non_protocolp_error_still_persists_the_rollouts_already_spent(context, plan):
    """The measurement loop owns the ledger, so its handler has to be broad.

    ``AssignmentGenerationError`` is a ``ValueError``, not a ``ProtocolPError``, and the
    override construction raises it for real.  A narrow handler discards every rollout
    already spent -- up to 126 of them, roughly an hour of simulation.
    """

    from utils.assignment_generator import AssignmentGenerationError

    base = _fake_runner()
    stop = x.ExtensionRow(x.MASS_CELLS[0], x.CONDITION_HEALTHY, None, 5)

    def run(row, ctx, ledger):
        if row.key == stop.key:
            raise AssignmentGenerationError("synthetic construction failure")
        return base(row, ctx, ledger)

    document = x.run_extension(
        context, plan, x.canonical_document_sha256(plan), _replay(), run_row=run
    )
    results = document["results"]
    assert results["outcome"] == x.OUTCOME_INVALID
    assert results["terminal"]["stage_reached"] == "measurement"
    assert "synthetic construction failure" in results["terminal"]["reason"]
    assert results["census"]["extension_physical_rollouts"] == 5
    assert len(results["physical_ledger"]) == 5


def test_tau_anchor_produces_the_partition_rather_than_sitting_beside_it():
    assert x._tau_anchor_partition(x.TAU_ANCHOR) == (
        x.ANCHOR_CONSTRAINED_RUNGS, x.ANCHOR_UNCONSTRAINED_RUNGS
    )
    # The document's stability claim: any tau in (0.021, 0.196) gives this partition,
    # and a tau outside it does not.  Both directions are constructed, not asserted.
    assert x._tau_anchor_partition(0.022) == x._tau_anchor_partition(0.195)
    assert x._tau_anchor_partition(0.195) == (
        x.ANCHOR_CONSTRAINED_RUNGS, x.ANCHOR_UNCONSTRAINED_RUNGS
    )
    # Outside the stable interval the partition really does move: at tau = 0.30 the
    # 0.196 rung at 0.45 and the 0.214 rung at 0.55 drop out of the constrained set.
    assert x._tau_anchor_partition(0.30)[1] == (0.45, 0.50, 0.55)
    assert x._tau_anchor_partition(0.0)[1] == ()


def test_cell_6_anchor_pins_equal_the_approved_screen_artifact():
    """Requirement (r): a literal that also lives in a bound document is checked."""

    screen = json.loads(
        (PACKET / "results" / "protocol_p" / "stage_abc_screen.json").read_text(
            encoding="utf-8"
        )
    )
    cell = screen["results"]["stage_c_nulls"]["6"]
    assert round(cell["q95_c"], 8) == x.CELL_6_Q95
    assert round(cell["operative_threshold"], 8) == x.CELL_6_THRESHOLD
    ladder = screen["results"]["ladder"]
    assert len(ladder) == len(x.LADDER)
    for index, entry in enumerate(ladder):
        row = entry["per_cell"]["6"]
        assert round(row["d"], 6) == x.CELL_6_D[index]
        assert round(row["margin"], 6) == x.CELL_6_MARGINS[index]
        # The anchor comparison uses only the sign, so the sign is what must be exact.
        assert (x.CELL_6_MARGINS[index] >= 0.0) == (row["margin"] >= 0.0)
        assert x.cell_6_margin_rows()[index]["verdict"] == row["verdict"]
