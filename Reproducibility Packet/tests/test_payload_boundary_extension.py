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


def test_strict_json_refuses_duplicate_keys_and_nonfinite_tokens(tmp_path):
    duplicate = tmp_path / "duplicate.json"
    duplicate.write_text('{"x":1,"x":2}', encoding="utf-8")
    with pytest.raises(ProtocolPError, match="duplicate JSON key"):
        x.strict_read_json(duplicate)
    nonfinite = tmp_path / "nonfinite.json"
    nonfinite.write_text('{"x":NaN}', encoding="utf-8")
    with pytest.raises(ProtocolPError, match="non-finite JSON token"):
        x.strict_read_json(nonfinite)


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
