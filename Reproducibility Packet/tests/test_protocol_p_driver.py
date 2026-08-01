"""Contract tests for the Protocol-P Stage A/B/C driver, ``run_protocol_p_screen.py``.

The driver owns what only exists once a rollout has returned: the derived onset, the
section-8 window (I9), the measurement-time shape (I10), the fit's sample count (I11),
the hard safety gates (I12), the selection rule, and the results-only output root.  It
also owns the *behavioural* half of the reuse rule -- that twelve of the 180 logical
rows never reach the construction layer at all.

How the executable path is exercised without spending a rollout
---------------------------------------------------------------
``run_screen`` takes its rollout executor as a parameter.  The stub below builds a
synthetic ``PrivilegedRecord`` and then produces its observation through the **real**
``SensorModel``, which is section 4's construction path with MuJoCo replaced: plant
first, suite ``S`` observed from the privileged record afterwards.  Nothing about the
driver's own arithmetic is reimplemented in the stub -- the gates, the window, the
statistic, the ledger and the persistence check are the production ones, running over
records the stub only had to shape.  A stub that returned gate verdicts or distances
would be a second copy of the driver that agrees with itself.

Conventions carried from the construction and results suites: assert the **reason** for
a refusal with a phrase unique to one raise site, and test per **branch** rather than
per guard.
"""

from __future__ import annotations

import json
import sys
from pathlib import Path

import numpy as np
import pytest

PACKET_ROOT = Path(__file__).resolve().parents[1]
SCRIPTS_ROOT = PACKET_ROOT / "scripts"
sys.path.insert(0, str(SCRIPTS_ROOT))

import run_protocol_p_screen as driver  # noqa: E402
from utils.assignment_generator import AssignmentGenerationError, _step_index  # noqa: E402
from utils.protocol_p import ProtocolPError  # noqa: E402
from utils.protocol_p_conditions import (  # noqa: E402
    CONDITION_HEALTHY,
    CONDITION_STRUCTURAL,
    SCREEN_CELLS,
    admissible_candidates,
    stage_ab_identity,
)
from utils import protocol_p_results as results  # noqa: E402
from utils.schema_types import PrivilegedRecord  # noqa: E402
from utils.sensor_model import SensorModel  # noqa: E402

CONFIG_PATH = PACKET_ROOT / "config" / "draft-config-v0.1.json"
SCHEMA_PATH = PACKET_ROOT / "schema" / "schema.json"
ASSIGNMENT_PATH = PACKET_ROOT / "config" / "proposed-gate3-assignment-v0.1.json"
PROTOCOL_PATH = PACKET_ROOT / "protocol" / "protocol-p-v2.3.3.md"

# Long enough to contain the section-8 window [1000, 1768) and nothing more.
STUB_STEPS = 1800
CANDIDATES = admissible_candidates()


@pytest.fixture(scope="module")
def context():
    """Resolve the real driver context once: pins, binding, timing, sources."""

    resolved, _inputs = driver.resolve_context(
        config_path=CONFIG_PATH,
        schema_path=SCHEMA_PATH,
        assignment_path=ASSIGNMENT_PATH,
        protocol_path=PROTOCOL_PATH,
    )
    return resolved


def _synthetic_plant(
    *,
    n_steps: int = STUB_STEPS,
    control_dt_s: float = 0.002,
    amplitude: float = 6.0,
    seed: int = 0,
    max_q: float = 0.3,
    max_qd: float = 0.5,
    saturated_steps: int = 0,
    safety_steps: int = 0,
) -> PrivilegedRecord:
    """Build a schema-valid privileged trace with a controllable 0.8 Hz gauge response.

    Inputs: the trace length, control step, gauge amplitude, a seed, and the three knobs
    the gate tests need. Outputs: a validated ``PrivilegedRecord``. Purpose: the tests
    need a body whose *measured* properties they control; every check that reads it is
    the driver's own.
    """

    rng = np.random.default_rng(seed)
    t_s = np.arange(n_steps, dtype=float) * control_dt_s
    gauge = amplitude * np.sin(2.0 * np.pi * 0.8 * t_s)[:, None] * np.array(
        [1.0, 0.9, 1.1, 0.95]
    )
    gauge = gauge + rng.normal(0.0, 0.05, size=gauge.shape)
    saturation = np.zeros((n_steps, 2), dtype=bool)
    if saturated_steps:
        saturation[:saturated_steps, 0] = True
    safety = np.zeros((n_steps, 7), dtype=bool)
    if safety_steps:
        safety[:safety_steps, 0] = True
    record = PrivilegedRecord(
        step=np.arange(n_steps, dtype=int),
        t_s=t_s,
        q_true=np.full((n_steps, 2), max_q),
        qd_true=np.full((n_steps, 2), max_qd),
        qdd_true=np.zeros((n_steps, 2)),
        tau_cmd=np.full((n_steps, 2), 0.01),
        tau_delivered_true=np.full((n_steps, 2), 0.01),
        deform_coords=np.zeros((n_steps, 8)),
        curvature_true=np.zeros((n_steps, 4)),
        gauge_true=gauge,
        imu_true=np.zeros((n_steps, 6)),
        temperature_true=np.full((n_steps, 4), 25.0),
        contact_state=np.zeros((n_steps, 2)),
        task_reference=np.zeros((n_steps, 2)),
        true_task_output=np.zeros((n_steps, 2)),
        tracking_error=np.zeros((n_steps, 2)),
        tracking_error_norm=np.zeros(n_steps),
        control_effort=np.full((n_steps, 2), 0.01),
        saturation_flag=saturation,
        safety_flag=safety,
    )
    record.validate()
    return record


class StubExecutor:
    """A rollout executor that builds a synthetic body and observes it for real.

    Counts its calls, because "did a reused row run?" is a countable question and the
    reuse rule is only enforced if the answer is measured rather than intended.
    """

    def __init__(self, context, *, amplitude_for=None, plant_for=None):
        self.context = context
        self.calls: list[dict] = []
        self._amplitude_for = amplitude_for
        self._plant_for = plant_for

    def __call__(self, *, assignment, base_config_hash, runtime, history_steps, reservation, overrides):
        self.calls.append(
            {
                "pair_id": overrides.realized_pair_id,
                "sensor_seed": reservation.sensor_seed,
                "peak": overrides.probe_peak_force_n,
                "ramp": overrides.probe_ramp_fraction_of_duration,
                "faults": overrides.physical_faults,
                "provenance": overrides.provenance_hash,
            }
        )
        severity = (
            None if not overrides.physical_faults else float(overrides.physical_faults[0].severity)
        )
        if self._plant_for is not None:
            plant = self._plant_for(overrides, reservation)
        else:
            amplitude = (
                self._amplitude_for(overrides, reservation)
                if self._amplitude_for is not None
                # A structural fault raises the gauge response; a stronger probe raises
                # it further. The exact law does not matter -- only that the fault and
                # healthy bodies differ and that the difference grows with the probe.
                else 4.0
                + 40.0 * float(overrides.probe_peak_force_n) * (0.0 if severity is None else (1.0 - severity))
            )
            plant = _synthetic_plant(amplitude=amplitude, seed=int(reservation.sensor_seed) % 100_000)
        observation = SensorModel(self.context.sensor_config).observe(
            plant,
            driver.SCREEN_SUITE,
            pair_id=str(overrides.realized_pair_id),
            sensor_seed=int(reservation.sensor_seed),
            fault=None,
            run_id=f"screen_{overrides.realized_pair_id}",
            config_hash=str(overrides.provenance_hash),
            split="dev",
        )
        return driver.RolloutOutcome(
            control_pair_id=str(overrides.realized_pair_id),
            plant=plant,
            observation=observation,
            safety_events=0,
            contact_steps=0,
            elapsed_s=0.0,
        )


# ---------------------------------------------------------------------------
# The derived onset and the derived window.
# ---------------------------------------------------------------------------


def test_the_onset_is_derived_from_the_bound_trajectory_not_carried(context):
    timing = context.timing
    assert timing.onset_time_s == 1.0
    assert timing.control_dt_s == 0.002
    assert timing.onset_index == _step_index(timing.onset_time_s, timing.control_dt_s)
    # The literal it happens to equal today. Asserting the derivation *and* the value is
    # what distinguishes a derived 500 from a hard-coded one that is currently correct.
    assert timing.onset_index == 500


def test_the_window_is_the_section_8_pin_for_the_dev_diagnostic_trajectory(context):
    assert (context.timing.w0, context.timing.w1) == (1000, 1768)
    assert context.timing.probe_start_offset_s == 1.0
    assert context.timing.w1 - context.timing.w0 == driver.WINDOW_STEPS == 768


def test_the_window_origin_is_onset_plus_offset_not_onset(context):
    timing = context.timing
    assert timing.w0 == _step_index(
        timing.onset_time_s + timing.probe_start_offset_s, timing.control_dt_s
    )
    assert timing.w0 != timing.onset_index


@pytest.mark.parametrize("passed", [0, 499, 501, 1000])
def test_passing_an_onset_other_than_the_derived_one_is_refused(context, passed):
    with pytest.raises(ProtocolPError, match="the onset derived from"):
        driver.require_derived_onset(passed, context.timing)


def test_a_non_integer_onset_is_refused_by_its_own_branch(context):
    with pytest.raises(ProtocolPError, match="onset index must be an int"):
        driver.require_derived_onset(500.0, context.timing)


def test_a_bool_onset_is_refused_too(context):
    with pytest.raises(ProtocolPError, match="onset index must be an int"):
        driver.require_derived_onset(True, context.timing)


def test_an_off_grid_onset_is_refused_as_an_onset_not_as_a_window(context):
    assignment = json.loads(json.dumps(dict(context.assignment)))
    for spec in assignment["trajectory_specs"]:
        if spec["id"] == driver.SCREEN_TRAJECTORY_SPEC_ID:
            spec["onset_time_s"] = 1.0001
    with pytest.raises(ProtocolPError, match="derived fault onset is off-grid"):
        driver.derive_screen_timing(assignment, control_dt_s=0.002, window_steps=768)


def test_an_off_grid_probe_offset_is_refused_as_a_window_not_as_an_onset(context):
    assignment = json.loads(json.dumps(dict(context.assignment)))
    for spec in assignment["trajectory_specs"]:
        if spec["id"] == driver.SCREEN_TRAJECTORY_SPEC_ID:
            spec["diagnostic_probe"]["start_offset_s"] = 1.0001
    with pytest.raises(ProtocolPError, match="derived window origin is off-grid"):
        driver.derive_screen_timing(assignment, control_dt_s=0.002, window_steps=768)


def test_the_bound_window_length_is_checked_by_equality_not_adopted(context):
    with pytest.raises(ProtocolPError, match="section 8's window is"):
        driver.derive_screen_timing(context.assignment, control_dt_s=0.002, window_steps=640)


def test_a_probe_free_trajectory_cannot_be_screened(context):
    assignment = json.loads(json.dumps(dict(context.assignment)))
    for spec in assignment["trajectory_specs"]:
        if spec["id"] == driver.SCREEN_TRAJECTORY_SPEC_ID:
            spec["diagnostic_probe"] = None
    with pytest.raises(ProtocolPError, match="must carry a diagnostic probe"):
        driver.derive_screen_timing(assignment, control_dt_s=0.002, window_steps=768)


def test_the_screened_trajectory_must_exist_exactly_once(context):
    assignment = json.loads(json.dumps(dict(context.assignment)))
    assignment["trajectory_specs"] = [
        spec for spec in assignment["trajectory_specs"] if spec["id"] != driver.SCREEN_TRAJECTORY_SPEC_ID
    ]
    with pytest.raises(ProtocolPError, match="expected exactly one"):
        driver.bound_trajectory(assignment)


def test_trajectory_specs_is_read_as_a_list_not_a_mapping(context):
    with pytest.raises(ProtocolPError, match="must be a list of specifications"):
        driver.bound_trajectory({"trajectory_specs": {"a": 1}})


# ---------------------------------------------------------------------------
# I9 / I10 / I11 on a real observed record.
# ---------------------------------------------------------------------------


def _observation(context, *, seed=1, amplitude=6.0, n_steps=STUB_STEPS):
    plant = _synthetic_plant(seed=seed, amplitude=amplitude, n_steps=n_steps)
    return SensorModel(context.sensor_config).observe(
        plant, driver.SCREEN_SUITE, pair_id="basepair_protocolp_test", sensor_seed=seed
    )


def test_the_coefficient_vector_has_the_section_8_shape(context):
    vector = driver.observation_coefficients(_observation(context), context.timing)
    assert len(vector) == 8
    assert all(np.isfinite(vector))


def test_i9_refuses_a_window_that_does_not_fit_the_rollout(context):
    short = _observation(context, n_steps=1500)
    with pytest.raises(ProtocolPError, match="does not fit a"):
        driver.observation_coefficients(short, context.timing)


def test_i9_refuses_a_negative_window_origin(context):
    timing = type(context.timing)(**{**vars(context.timing), "w0": -1, "w1": 767})
    with pytest.raises(ProtocolPError, match="window origin -1 is negative"):
        driver.require_window_on_grid(timing, STUB_STEPS)


def test_i10_accepts_a_rank_one_measurement_time(context):
    observation = _observation(context)
    assert observation.measurement_time_s["gauge_obs"].ndim == 1
    driver.gauge_window_from_observation(observation, context.timing)


def test_i10_accepts_the_legacy_column_vector_shape(context):
    observation = _observation(context)
    observation.measurement_time_s["gauge_obs"] = observation.measurement_time_s["gauge_obs"][:, None]
    values, valid, t_g = driver.gauge_window_from_observation(observation, context.timing)
    assert t_g.ndim == 1 and t_g.shape[0] == values.shape[0] == valid.shape[0] == 768


def test_i10_refuses_a_rank_three_measurement_time(context):
    observation = _observation(context)
    observation.measurement_time_s["gauge_obs"] = observation.measurement_time_s["gauge_obs"][
        :, None, None
    ]
    with pytest.raises(ProtocolPError, match=r"must be \[T\] or \[T,1\]"):
        driver.gauge_window_from_observation(observation, context.timing)


def test_i10_refuses_a_two_column_measurement_time(context):
    observation = _observation(context)
    column = observation.measurement_time_s["gauge_obs"][:, None]
    observation.measurement_time_s["gauge_obs"] = np.concatenate([column, column], axis=1)
    with pytest.raises(ProtocolPError, match=r"must be \[T\] or \[T,1\]"):
        driver.gauge_window_from_observation(observation, context.timing)


def test_i10_refuses_a_measurement_time_of_the_wrong_length(context):
    observation = _observation(context)
    observation.measurement_time_s["gauge_obs"] = observation.measurement_time_s["gauge_obs"][:-1]
    with pytest.raises(ProtocolPError, match="must equal the gauge trace length"):
        driver.gauge_window_from_observation(observation, context.timing)


def test_i10_refuses_a_gauge_channel_of_the_wrong_width(context):
    observation = _observation(context)
    observation.values["gauge_obs"] = observation.values["gauge_obs"][:, :3]
    with pytest.raises(ProtocolPError, match=r"gauge_obs must be \[T, 4\]"):
        driver.gauge_window_from_observation(observation, context.timing)


def test_i10_refuses_a_validity_mask_that_does_not_match_the_values(context):
    observation = _observation(context)
    observation.valid_mask["gauge_obs"] = observation.valid_mask["gauge_obs"][:, :3]
    with pytest.raises(ProtocolPError, match="must match gauge values"):
        driver.gauge_window_from_observation(observation, context.timing)


def test_i11_refuses_a_window_with_too_few_finite_valid_samples(context):
    observation = _observation(context)
    mask = observation.valid_mask["gauge_obs"]
    mask[:, :] = False
    mask[:4, :] = True
    with pytest.raises(Exception):
        driver.observation_coefficients(observation, context.timing)


def test_the_statistic_refuses_a_wrong_length_vector():
    with pytest.raises(ProtocolPError, match="the statistic is over two"):
        driver.difference_statistic((0.0,) * 7, (0.0,) * 7)


def test_the_statistic_refuses_a_non_finite_entry():
    good = tuple(0.0 for _ in range(8))
    bad = (float("nan"),) + tuple(0.0 for _ in range(7))
    with pytest.raises(ProtocolPError, match="requires finite coefficient vectors"):
        driver.difference_statistic(bad, good)


def test_the_statistic_is_the_euclidean_norm_of_the_difference():
    left = tuple(float(index) for index in range(8))
    right = tuple(0.0 for _ in range(8))
    assert driver.difference_statistic(left, right) == pytest.approx(
        float(np.linalg.norm(np.arange(8, dtype=float)))
    )


def test_a_matched_pair_of_identical_bodies_gives_a_zero_distance():
    vector = tuple(float(index) for index in range(8))
    assert driver.difference_statistic(vector, vector) == 0.0


# ---------------------------------------------------------------------------
# I12 -- one test per gate branch.
# ---------------------------------------------------------------------------


def test_a_clean_rollout_passes_every_gate_and_records_its_margins():
    report = driver.evaluate_hard_gates(_synthetic_plant(), safety_events=0, contact_steps=0)
    assert report.passed and report.failures == ()
    assert report.max_abs_q_true == pytest.approx(0.3)
    assert report.max_abs_qd_true == pytest.approx(0.5)
    assert report.saturated_steps == 0


def test_a_set_safety_flag_fails_the_gate():
    report = driver.evaluate_hard_gates(
        _synthetic_plant(safety_steps=1), safety_events=0, contact_steps=0
    )
    assert not report.passed
    assert any("safety_flag set on" in failure for failure in report.failures)


def test_a_generator_reported_safety_event_fails_the_gate():
    report = driver.evaluate_hard_gates(_synthetic_plant(), safety_events=3, contact_steps=0)
    assert not report.passed
    assert any("counted 3 safety events" in failure for failure in report.failures)


def test_an_excessive_joint_angle_fails_the_gate():
    report = driver.evaluate_hard_gates(
        _synthetic_plant(max_q=2.6), safety_events=0, contact_steps=0
    )
    assert not report.passed
    assert any("max|q_true|" in failure for failure in report.failures)


def test_an_excessive_joint_rate_fails_the_gate():
    report = driver.evaluate_hard_gates(
        _synthetic_plant(max_qd=8.1), safety_events=0, contact_steps=0
    )
    assert not report.passed
    assert any("max|qd_true|" in failure for failure in report.failures)


def test_an_excessive_gauge_magnitude_fails_the_gate():
    report = driver.evaluate_hard_gates(
        _synthetic_plant(amplitude=401.0), safety_events=0, contact_steps=0
    )
    assert not report.passed
    assert any("max|gauge_true|" in failure for failure in report.failures)


def test_a_single_saturated_step_fails_the_gate_against_the_zero_baseline():
    report = driver.evaluate_hard_gates(
        _synthetic_plant(saturated_steps=1), safety_events=0, contact_steps=0
    )
    assert not report.passed
    assert any("saturated steps against the zero-probe baseline" in f for f in report.failures)
    assert driver.SATURATED_STEP_BASELINE == 0


def test_the_gate_boundaries_are_inclusive_on_the_passing_side():
    report = driver.evaluate_hard_gates(
        _synthetic_plant(max_q=driver.MAX_ABS_JOINT_ANGLE_RAD, max_qd=driver.MAX_ABS_JOINT_RATE_RAD_S),
        safety_events=0,
        contact_steps=0,
    )
    assert report.passed


def test_a_gate_failure_is_measured_and_reported_not_raised():
    # Section 8 drops a failing candidate and continues; a raise here would end the
    # screen on the first inadmissible candidate instead.
    report = driver.evaluate_hard_gates(
        _synthetic_plant(max_q=99.0, max_qd=99.0, saturated_steps=5, safety_steps=5),
        safety_events=7,
        contact_steps=0,
    )
    assert not report.passed
    assert len(report.failures) == 5


def test_the_probe_torque_gate_admits_the_strongest_admissible_candidate():
    driver.require_probe_torque_gate(0.15)
    with pytest.raises(ProtocolPError, match="torque gate refuses"):
        driver.require_probe_torque_gate(0.20)


# ---------------------------------------------------------------------------
# The sources come from the assignment, never constructed.
# ---------------------------------------------------------------------------


def test_the_four_screen_sources_are_the_delivered_dev_diagnostic_reservations(context):
    assert set(context.sources) == set(SCREEN_CELLS)
    for cell in SCREEN_CELLS:
        source = context.sources[cell]
        assert source.scenario_spec_id == f"scenario_dev_t01_f000_r{cell - 4:02d}"
        assert source.fault_setting_id == "fault_dev_healthy"
        assert source.split == "dev"


def _binding(context):
    """Re-resolve the assignment binding the source lookup needs."""

    from utils.assignment_binding import validate_approved_assignment_binding
    from utils.config_contract import load_config
    from utils.gate3_assignment import load_assignment

    config = load_config(CONFIG_PATH, SCHEMA_PATH)
    return validate_approved_assignment_binding(
        config, expected_assignment=load_assignment(ASSIGNMENT_PATH)
    )


def test_two_reservations_matching_one_cell_are_refused(context, monkeypatch):
    # Added after a mutation sweep: removing the uniqueness check survived both test
    # files, because the real assignment always yields exactly one match. The rejected
    # state is unconstructible from the document and reachable only by making the lookup
    # return it, which is what a duplicated reservation would look like.
    binding = _binding(context)
    real = driver.build_identity_manifest

    def duplicating(*args, **kwargs):
        rows, reservations = real(*args, **kwargs)
        return rows, list(reservations) + list(reservations)

    monkeypatch.setattr(driver, "build_identity_manifest", duplicating)
    with pytest.raises(ProtocolPError, match="expected exactly one delivered reservation"):
        driver.screen_sources(binding)


def test_a_cell_with_no_delivered_reservation_is_refused(context, monkeypatch):
    binding = _binding(context)
    real = driver.build_identity_manifest

    def dropping(*args, **kwargs):
        rows, reservations = real(*args, **kwargs)
        return rows, [
            item
            for item in reservations
            if item.scenario_spec_id != "scenario_dev_t01_f000_r02"
        ]

    monkeypatch.setattr(driver, "build_identity_manifest", dropping)
    with pytest.raises(ProtocolPError, match="expected exactly one delivered reservation"):
        driver.screen_sources(binding)


def test_a_source_whose_setting_is_not_healthy_is_refused(context, monkeypatch):
    import dataclasses as _dataclasses

    binding = _binding(context)
    real = driver.build_identity_manifest

    def faulted(*args, **kwargs):
        rows, reservations = real(*args, **kwargs)
        return rows, [
            _dataclasses.replace(item, fault_setting_id="fault_dev_structure_x")
            if item.scenario_spec_id == "scenario_dev_t01_f000_r00"
            else item
            for item in reservations
        ]

    monkeypatch.setattr(driver, "build_identity_manifest", faulted)
    with pytest.raises(ProtocolPError, match="source must be the healthy setting"):
        driver.screen_sources(binding)


# ---------------------------------------------------------------------------
# The reuse rule's behavioural half.
# ---------------------------------------------------------------------------


def test_running_a_reused_row_directly_is_refused(context):
    rows = results.build_logical_inventory(candidates=CANDIDATES, selected=CANDIDATES[0])
    reused = next(row for row in rows if row.is_reused)
    with pytest.raises(ProtocolPError, match="must cite its origin rather than run"):
        driver.run_logical_row(reused, context, results.ResultsLedger(), execute=StubExecutor(context))


def test_one_row_runs_once_and_stamps_a_dev_prefixed_base_distinct_hash(context):
    rows = results.build_logical_inventory(candidates=CANDIDATES, selected=CANDIDATES[0])
    row = next(row for row in rows if row.stage == results.STAGE_A)
    ledger = results.ResultsLedger()
    stub = StubExecutor(context)
    result, plant = driver.run_logical_row(row, context, ledger, execute=stub)
    assert len(stub.calls) == 1
    assert plant is None
    assert result.provenance_hash.startswith("dev-")
    assert result.provenance_hash != context.base_config_hash
    assert result.stage_of_origin == results.STAGE_A
    assert len(ledger) == 1


def test_the_construction_layer_receives_the_derived_onset_for_a_structural_row(context):
    rows = results.build_logical_inventory(candidates=CANDIDATES, selected=CANDIDATES[0])
    row = next(
        r for r in rows if r.stage == results.STAGE_A and r.condition == CONDITION_STRUCTURAL
    )
    stub = StubExecutor(context)
    driver.run_logical_row(row, context, results.ResultsLedger(), execute=stub)
    (fault,) = stub.calls[0]["faults"]
    assert fault.onset_index == context.timing.onset_index == 500
    assert fault.source_class == "structure"
    assert fault.severity == row.severity


def test_a_healthy_row_carries_an_explicit_empty_fault_tuple(context):
    rows = results.build_logical_inventory(candidates=CANDIDATES, selected=CANDIDATES[0])
    row = next(r for r in rows if r.stage == results.STAGE_A and r.condition == CONDITION_HEALTHY)
    stub = StubExecutor(context)
    driver.run_logical_row(row, context, results.ResultsLedger(), execute=stub)
    assert stub.calls[0]["faults"] == ()


def test_the_torque_gate_is_actually_called_on_the_row_about_to_run(context):
    # Added after a mutation sweep: deleting the call site survived both test files,
    # because the gate itself was only ever tested directly. A peak of 0.20 N is finite
    # and positive, so ``require_admissible_probe`` inside the construction layer admits
    # it -- this call site is the only thing between an over-torque probe and a rollout.
    identity = stage_ab_identity(SCREEN_CELLS[0])
    over_torque = results.LogicalRow(
        stage=results.STAGE_A,
        cell=SCREEN_CELLS[0],
        condition=CONDITION_HEALTHY,
        severity=None,
        replicate=None,
        probe_peak_force_n=0.20,
        probe_ramp_fraction_of_duration=0.25,
        identity=identity,
    )
    stub = StubExecutor(context)
    with pytest.raises(ProtocolPError, match="torque gate refuses"):
        driver.run_logical_row(over_torque, context, results.ResultsLedger(), execute=stub)
    assert stub.calls == []


def test_the_derived_onset_is_actually_asserted_on_the_row_about_to_run(context, monkeypatch):
    # The companion wire test: the equality check is exercised directly elsewhere, this
    # shows ``run_logical_row`` reaches it before it constructs anything.
    called: list[int] = []

    def recording(passed_onset_index, timing):
        called.append(passed_onset_index)
        raise ProtocolPError("wire-test refusal from require_derived_onset")

    monkeypatch.setattr(driver, "require_derived_onset", recording)
    rows = results.build_logical_inventory(candidates=CANDIDATES, selected=CANDIDATES[0])
    row = next(row for row in rows if row.stage == results.STAGE_A)
    stub = StubExecutor(context)
    with pytest.raises(ProtocolPError, match="wire-test refusal"):
        driver.run_logical_row(row, context, results.ResultsLedger(), execute=stub)
    assert called == [context.timing.onset_index]
    assert stub.calls == []


def test_a_rollout_that_realizes_the_wrong_pair_id_is_refused(context):
    rows = results.build_logical_inventory(candidates=CANDIDATES, selected=CANDIDATES[0])
    row = next(row for row in rows if row.stage == results.STAGE_A)

    class WrongPair(StubExecutor):
        def __call__(self, **kwargs):
            outcome = super().__call__(**kwargs)
            return type(outcome)(**{**vars(outcome), "control_pair_id": "basepair_protocolp_other"})

    with pytest.raises(ProtocolPError, match="is not the row's"):
        driver.run_logical_row(row, context, results.ResultsLedger(), execute=WrongPair(context))


def test_a_reused_stage_b_row_calls_neither_the_construction_layer_nor_the_generator(
    context, monkeypatch
):
    rows = results.build_logical_inventory(candidates=CANDIDATES, selected=CANDIDATES[0])
    stage_b = tuple(row for row in rows if row.stage == results.STAGE_B)
    reused = tuple(row for row in stage_b if row.is_reused)
    assert len(reused) == 8

    # Record Stage A's origins first, then run only the reused rows.
    ledger = results.ResultsLedger()
    stub = StubExecutor(context)
    for row in rows:
        if row.stage == results.STAGE_A and (
            row.probe_peak_force_n,
            row.probe_ramp_fraction_of_duration,
        ) == CANDIDATES[0]:
            driver.run_logical_row(row, context, ledger, execute=stub)
    before = len(stub.calls)

    calls = {"build_overrides": 0}
    real_build = driver.build_overrides

    def counting(*args, **kwargs):
        calls["build_overrides"] += 1
        return real_build(*args, **kwargs)

    monkeypatch.setattr(driver, "build_overrides", counting)
    driver.run_reuse_aware_rows(reused, context, ledger, execute=stub)
    assert calls["build_overrides"] == 0
    assert len(stub.calls) == before


def test_a_reused_row_resolves_to_its_origins_stamp_and_canonical_payload(context):
    rows = results.build_logical_inventory(candidates=CANDIDATES, selected=CANDIDATES[0])
    ledger = results.ResultsLedger()
    stub = StubExecutor(context)
    for row in rows:
        if row.stage == results.STAGE_A and (
            row.probe_peak_force_n,
            row.probe_ramp_fraction_of_duration,
        ) == CANDIDATES[0]:
            driver.run_logical_row(row, context, ledger, execute=stub)
    checked = 0
    for row in rows:
        if not row.is_reused:
            continue
        origin = next(item for item in rows if item.key == row.reused_from)
        stamp, canonical, stage_of_origin = results.resolve_row_provenance(ledger, row)
        origin_stamp, origin_canonical, _ = results.resolve_row_provenance(ledger, origin)
        assert stamp == origin_stamp
        assert canonical == origin_canonical
        assert stage_of_origin == results.STAGE_A
        # CANONICAL_JSON uses compact separators, so the payload the reused row cites
        # still literally says Stage A. A relabelled payload would say B or C here.
        assert f'"stage":"{results.STAGE_A}"' in canonical
        assert '"stage":"B"' not in canonical and '"stage":"C"' not in canonical
        checked += 1
    assert checked == 12


def test_minting_a_second_stamp_for_a_reused_body_is_what_the_ledger_refuses(context):
    # The hazard, demonstrated: asking the construction layer for a Stage-C label on the
    # Stage-A body produces a different, well-formed hash. The ledger's duplicate-key
    # refusal is what stops that hash from entering the record.
    rows = results.build_logical_inventory(candidates=CANDIDATES, selected=CANDIDATES[0])
    origin = next(
        row
        for row in rows
        if row.stage == results.STAGE_A
        and row.condition == CONDITION_HEALTHY
        and row.cell == SCREEN_CELLS[0]
        and (row.probe_peak_force_n, row.probe_ramp_fraction_of_duration) == CANDIDATES[0]
    )
    reused = next(
        row
        for row in rows
        if row.stage == results.STAGE_C and row.cell == SCREEN_CELLS[0] and row.replicate == 0
    )
    ledger = results.ResultsLedger()
    stub = StubExecutor(context)
    driver.run_logical_row(origin, context, ledger, execute=stub)
    minted = type(reused)(**{**vars(reused), "reused_from": None})
    with pytest.raises(ProtocolPError, match="is already recorded for"):
        driver.run_logical_row(minted, context, ledger, execute=stub)


# ---------------------------------------------------------------------------
# Selection.
# ---------------------------------------------------------------------------


class _FakeLedger:
    """A ledger stand-in whose worst-cell scores the test chooses directly."""

    def __init__(self, scores):
        self._scores = scores


def _selection_with(scores, monkeypatch, survivors):
    monkeypatch.setattr(
        driver,
        "worst_cell_statistic",
        lambda ledger, candidate, *, severity: scores[tuple(candidate)],
    )
    return driver.select_candidate(_FakeLedger(scores), survivors)


def test_selection_maximises_the_worst_cell_statistic(monkeypatch):
    survivors = [(0.05, 0.125), (0.10, 0.25), (0.15, 0.5)]
    scores = {(0.05, 0.125): 0.10, (0.10, 0.25): 0.40, (0.15, 0.5): 0.20}
    outcome = _selection_with(scores, monkeypatch, survivors)
    assert outcome["selected"] == (0.10, 0.25)
    assert outcome["tied_candidates"] == [[0.10, 0.25]]


def test_a_tie_within_one_percent_resolves_to_the_smallest_amplitude(monkeypatch):
    survivors = [(0.05, 0.125), (0.15, 0.5)]
    scores = {(0.05, 0.125): 0.399, (0.15, 0.5): 0.400}
    outcome = _selection_with(scores, monkeypatch, survivors)
    assert outcome["selected"] == (0.05, 0.125)
    assert len(outcome["tied_candidates"]) == 2


def test_a_tie_at_one_amplitude_resolves_to_the_largest_ramp(monkeypatch):
    survivors = [(0.05, 0.125), (0.05, 0.5)]
    scores = {(0.05, 0.125): 0.400, (0.05, 0.5): 0.399}
    outcome = _selection_with(scores, monkeypatch, survivors)
    assert outcome["selected"] == (0.05, 0.5)


def test_a_difference_outside_the_tie_band_is_not_a_tie(monkeypatch):
    survivors = [(0.05, 0.125), (0.15, 0.5)]
    scores = {(0.05, 0.125): 0.30, (0.15, 0.5): 0.40}
    outcome = _selection_with(scores, monkeypatch, survivors)
    assert outcome["selected"] == (0.15, 0.5)


def test_selection_with_no_survivors_is_the_terminal_branch():
    with pytest.raises(ProtocolPError, match=driver.TERMINAL_NO_ADMISSIBLE_PROBE):
        driver.select_candidate(_FakeLedger({}), [])


def test_a_non_positive_best_score_is_diagnosed_rather_than_tie_broken(monkeypatch):
    survivors = [(0.05, 0.125)]
    scores = {(0.05, 0.125): 0.0}
    monkeypatch.setattr(
        driver, "worst_cell_statistic", lambda ledger, candidate, *, severity: scores[tuple(candidate)]
    )
    with pytest.raises(ProtocolPError, match="makes the 1% tie band meaningless"):
        driver.select_candidate(_FakeLedger(scores), survivors)


def test_the_selection_severity_is_the_pre_registered_one():
    assert driver.SELECTION_SEVERITY == 0.75
    assert driver.SELECTION_TIE_TOLERANCE == 0.01


# ---------------------------------------------------------------------------
# The results-only persistence boundary, wired to the real driver.
# ---------------------------------------------------------------------------


def test_the_driver_writes_a_results_json_and_the_boundary_accepts_it(tmp_path):
    written = driver.write_results({"mode": "plan", "results": None}, tmp_path)
    assert written.name == driver.OUTPUT_FILENAME
    assert json.loads(written.read_text(encoding="utf-8"))["mode"] == "plan"


def test_a_dataset_role_write_into_the_output_root_fails_the_real_driver(tmp_path, monkeypatch):
    # A real wrong write by the code under test: the write step is made to also persist
    # an observation payload, exactly as a driver that forgot the results-only rule
    # would. The gate must fail on the directory, after the write.
    real_write_text = Path.write_text

    def leaking_write_text(self, *args, **kwargs):
        outcome = real_write_text(self, *args, **kwargs)
        if self.suffix == ".json":
            (self.parent / "observations").mkdir(exist_ok=True)
            (self.parent / "observations" / "scenario_protocolp_stageAB_c4.npz").write_bytes(
                b"PK\x03\x04"
            )
        return outcome

    monkeypatch.setattr(Path, "write_text", leaking_write_text)
    with pytest.raises(ProtocolPError, match="dataset-role directory"):
        driver.write_results({"mode": "plan"}, tmp_path)
    assert (tmp_path / "observations" / "scenario_protocolp_stageAB_c4.npz").exists()


def test_the_boundary_check_runs_after_the_write_not_before(tmp_path):
    driver.write_results({"mode": "plan"}, tmp_path)
    (tmp_path / "manifest.csv").write_text("x", encoding="utf-8")
    with pytest.raises(ProtocolPError, match="dataset-role artifact"):
        results.require_results_only_root(tmp_path)


def test_main_in_plan_mode_runs_zero_rollouts_and_writes_a_results_json(tmp_path, monkeypatch):
    def refuse(**kwargs):
        raise AssertionError("plan mode must not execute a rollout")

    monkeypatch.setattr(driver, "execute_rollout", refuse)
    status = driver.main(
        [
            "--output-dir",
            str(tmp_path),
            "--config",
            str(CONFIG_PATH),
            "--schema",
            str(SCHEMA_PATH),
            "--assignment",
            str(ASSIGNMENT_PATH),
            "--protocol",
            str(PROTOCOL_PATH),
        ]
    )
    assert status == 0
    document = json.loads((tmp_path / driver.OUTPUT_FILENAME).read_text(encoding="utf-8"))
    assert document["mode"] == "plan"
    assert document["results"] is None
    assert document["plan"]["census"] == {
        "logical_rows": 180,
        "physical_rollouts": 168,
        "reused_rows": 12,
        "rows_by_stage": {"A": 108, "B": 40, "C": 32},
    }
    assert document["inputs"]["onset_index"] == 500
    assert document["inputs"]["window"] == [1000, 1768]


def test_the_default_mode_is_the_zero_rollout_one():
    args = driver.parse_args(["--output-dir", "x"])
    assert args.mode == "plan"


def test_the_output_directory_is_required():
    with pytest.raises(SystemExit):
        driver.parse_args([])


def test_the_plan_placeholder_selection_never_reaches_the_document(tmp_path, monkeypatch):
    monkeypatch.setattr(driver, "execute_rollout", lambda **kwargs: pytest.fail("no rollout"))
    driver.main(
        [
            "--output-dir",
            str(tmp_path),
            "--config",
            str(CONFIG_PATH),
            "--schema",
            str(SCHEMA_PATH),
            "--assignment",
            str(ASSIGNMENT_PATH),
            "--protocol",
            str(PROTOCOL_PATH),
        ]
    )
    document = json.loads((tmp_path / driver.OUTPUT_FILENAME).read_text(encoding="utf-8"))
    assert "selected" not in json.dumps(document["plan"])
    assert "placeholder" in document["plan"]["placeholder_selection_note"]


# ---------------------------------------------------------------------------
# End to end: 180 rows over 168 executions, on real records, zero MuJoCo rollouts.
# ---------------------------------------------------------------------------


@pytest.fixture(scope="module")
def screened(context):
    """Run the whole screen once through the stub executor and share the result."""

    stub = StubExecutor(context)
    document = driver.run_screen(context, candidates=CANDIDATES, execute=stub)
    return document, stub


def test_the_screen_executes_exactly_one_rollout_per_physical_body(screened):
    document, stub = screened
    assert len(stub.calls) == results.EXPECTED_PHYSICAL_ROLLOUTS == 168
    assert document["ledger_census"] == {"physical_results": 168, "distinct_stamps": 168}


def test_the_screen_reports_180_rows_over_those_168_executions(screened):
    document, _stub = screened
    assert len(document["rows"]) == 180
    assert len({row["rollout_provenance"] for row in document["rows"]}) == 168


def test_exactly_twelve_reported_rows_are_reuses_and_each_cites_a_stage_a_row(screened):
    document, _stub = screened
    reused = [row for row in document["rows"] if row["reused_from"] is not None]
    assert len(reused) == 12
    assert all(row["stage_of_origin"] == results.STAGE_A for row in reused)
    assert {row["stage"] for row in reused} == {results.STAGE_B, results.STAGE_C}
    selected = tuple(document["stage_a"]["selection"]["selected"])
    for row in reused:
        assert tuple(row["reused_from"][-2:]) == selected


def test_no_stamp_was_minted_for_a_reused_row(screened):
    document, stub = screened
    minted = {call["provenance"] for call in stub.calls}
    reported = {row["rollout_provenance"] for row in document["rows"]}
    assert reported == minted
    assert len(minted) == 168


def test_every_executed_rollout_used_the_derived_onset(screened):
    _document, stub = screened
    onsets = {
        int(call["faults"][0].onset_index) for call in stub.calls if call["faults"]
    }
    assert onsets == {500}


def test_the_ladder_table_has_one_row_per_ladder_value_with_all_four_cells(screened):
    document, _stub = screened
    table = document["ladder"]
    assert len(table) == 10
    for row in table:
        assert set(row["per_cell"]) == {str(cell) for cell in SCREEN_CELLS}
        for cell in SCREEN_CELLS:
            entry = row["per_cell"][str(cell)]
            assert {"d", "q95_c", "operative_threshold", "margin", "verdict"} <= set(entry)
            assert entry["operative_threshold"] == pytest.approx(2.0 * entry["q95_c"])
            assert len(entry["d_unmatched"]["values"]) == 7
            assert entry["d_unmatched"]["authority"] == "NONE"
            assert "q95_c_gauge_only" in entry


def test_the_value_verdict_is_the_conjunction_over_all_four_cells(screened):
    document, _stub = screened
    for row in document["ladder"]:
        margins = [row["per_cell"][str(cell)]["margin"] for cell in SCREEN_CELLS]
        assert row["min_margin"] == pytest.approx(min(margins))
        expected = driver.VERDICT_TESTABLE if min(margins) >= 0.0 else driver.VERDICT_SUB_THRESHOLD
        assert row["verdict"] == expected


def test_one_failing_cell_is_enough_to_deny_testable(screened):
    document, _stub = screened
    # No pooled quantity enters the verdict: a row whose cells disagree must be
    # SUB_THRESHOLD regardless of how well the other three did.
    mixed = [
        row
        for row in document["ladder"]
        if len({row["per_cell"][str(cell)]["verdict"] for cell in SCREEN_CELLS}) > 1
    ]
    for row in mixed:
        assert row["verdict"] == driver.VERDICT_SUB_THRESHOLD


def test_the_operative_null_has_28_distances_from_8_runs_per_cell(screened):
    document, _stub = screened
    for cell in SCREEN_CELLS:
        null = document["stage_c_nulls"][str(cell)]
        assert null["n_distances"] == 28
        assert null["n_independent_runs"] == 8
        assert len(null["distances"]) == 28
        assert null["q95_c"] == pytest.approx(
            float(np.quantile(null["distances"], 0.95, method="higher"))
        )


def test_the_gauge_only_secondary_is_marked_as_having_no_authority(screened):
    document, _stub = screened
    for cell in SCREEN_CELLS:
        secondary = document["stage_c_gauge_only"][str(cell)]
        assert secondary["authority"] == "NONE"
        assert len(secondary["distances"]) == 28
        assert "no mechanism" in secondary["scope"]


def test_the_selected_candidate_is_one_that_actually_ran(screened):
    document, stub = screened
    selected = tuple(document["stage_a"]["selection"]["selected"])
    executed = {(call["peak"], call["ramp"]) for call in stub.calls}
    assert selected in executed


def test_the_document_is_json_serialisable_without_nan(screened):
    document, _stub = screened
    json.dumps(document, allow_nan=False, sort_keys=True)


def test_the_whole_screen_result_survives_the_persistence_boundary(screened, tmp_path):
    document, _stub = screened
    written = driver.write_results({"results": document}, tmp_path)
    assert written.exists()
    assert results.require_results_only_root(tmp_path)["files"] == (driver.OUTPUT_FILENAME,)


def test_a_candidate_that_fails_a_gate_is_dropped_and_its_remaining_cells_skipped(context):
    # The first candidate's very first row saturates; section 8 says drop the candidate
    # and skip its remaining cells, so it must contribute far fewer than its 12 rollouts.
    failing = CANDIDATES[0]

    def plant_for(overrides, reservation):
        saturate = (
            float(overrides.probe_peak_force_n),
            float(overrides.probe_ramp_fraction_of_duration),
        ) == failing
        return _synthetic_plant(
            seed=int(reservation.sensor_seed) % 100_000,
            saturated_steps=1 if saturate else 0,
        )

    stub = StubExecutor(context, plant_for=plant_for)
    ledger = results.ResultsLedger()
    rows = results.build_logical_inventory(candidates=CANDIDATES, selected=CANDIDATES[-1])
    stage_a = driver.run_stage_a(rows, CANDIDATES[:2], context, ledger, execute=stub)
    assert stage_a["drop_count"] == 1
    assert stage_a["drops"][0]["candidate"] == [failing[0], failing[1]]
    assert tuple(stage_a["survivors"]) == (CANDIDATES[1],)
    # 1 dropped row for the failing candidate + 12 for the survivor.
    assert len(stub.calls) == 13


def test_a_candidate_absent_from_the_inventory_is_refused_by_its_row_count(context):
    # Added after a mutation sweep: the per-candidate row-count check survived, because
    # every candidate drawn from a validated inventory has its twelve rows by
    # construction. The reachable state is a caller whose candidate list and inventory
    # disagree, which produces zero rows and would otherwise silently "pass" the
    # candidate without measuring it.
    rows = results.build_logical_inventory(candidates=CANDIDATES, selected=CANDIDATES[0])
    stub = StubExecutor(context)
    with pytest.raises(ProtocolPError, match="Stage-A rows; each candidate"):
        driver.run_stage_a(rows, [(0.05, 0.4)], context, results.ResultsLedger(), execute=stub)
    assert stub.calls == []


def test_a_within_cell_null_of_the_wrong_size_is_refused(context, monkeypatch):
    # The 28-distance check is a code guard: C(8,2) is 28 whenever the replicate count is
    # 8, so no *data* can make it fire. It becomes live the moment that constant moves,
    # and this is the state that shows it -- the ledger is fully populated, so the
    # refusal is the size check and not a missing lookup.
    candidate = CANDIDATES[0]
    cell = SCREEN_CELLS[0]
    rows = results.build_logical_inventory(candidates=CANDIDATES, selected=candidate)
    ledger = results.ResultsLedger()
    stub = StubExecutor(context)
    for row in rows:
        if row.stage == results.STAGE_A and row.cell == cell and (
            row.probe_peak_force_n,
            row.probe_ramp_fraction_of_duration,
        ) == candidate:
            driver.run_logical_row(row, context, ledger, execute=stub)
    for row in rows:
        if row.stage == results.STAGE_C and row.cell == cell and not row.is_reused:
            driver.run_logical_row(row, context, ledger, execute=stub)

    assert driver.stage_c_null(ledger, candidate, cell)["n_distances"] == 28
    monkeypatch.setattr(driver, "STAGE_C_REPLICATES", 4)
    with pytest.raises(ProtocolPError, match="must have 28 distances"):
        driver.stage_c_null(ledger, candidate, cell)


def test_every_candidate_failing_yields_the_terminal_branch(context):
    def plant_for(overrides, reservation):
        return _synthetic_plant(
            seed=int(reservation.sensor_seed) % 100_000, saturated_steps=1
        )

    stub = StubExecutor(context, plant_for=plant_for)
    document = driver.run_screen(context, candidates=CANDIDATES[:2], execute=stub)
    assert document["terminal"] == driver.TERMINAL_NO_ADMISSIBLE_PROBE
    assert document["stage_a"]["drop_count"] == 2
    assert document["stage_a"]["survivors"] == []
    assert "pins nothing" in document["scope"]
