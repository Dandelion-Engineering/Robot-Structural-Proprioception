"""Contract tests for the generator's typed screen-override seam.

The seam lets a screen deviate the approved assignment's probe, physical fault
list, realized identity, and distal payload mass
-- and requires any deviating rollout to carry a suffix-free realized identity
and a base-distinct ``dev-`` provenance hash. These are generator-contract
guards, not screen-local measurements: any future consumer of
``ScreenOverrides`` needs them, so they live in the permanent packet suite for
the same reason the plant's softening-boundary guard does.

Every guard below is exercised with the exact state it was written to reject,
not only with the state it should accept.
"""

from __future__ import annotations

import dataclasses
import hashlib
import sys
from pathlib import Path

import pytest

PACKET_ROOT = Path(__file__).resolve().parents[1]
SCRIPTS_ROOT = PACKET_ROOT / "scripts"
sys.path.insert(0, str(SCRIPTS_ROOT))

from utils.assignment_binding import validate_approved_assignment_binding  # noqa: E402
from utils.assignment_generator import (  # noqa: E402
    AssignmentGenerationError,
    ScreenOverrides,
    _generate_reservation,
    _physical_config,
    _profile,
    _runtime_parameters,
    _screen_stamped_hash,
    screen_pair_id,
)
from utils.config_contract import load_config  # noqa: E402
from utils.gate3_assignment import expand_reservations, load_assignment  # noqa: E402
from utils.schema_types import FaultSpec  # noqa: E402
from utils.storage_contract import _valid_config_hash  # noqa: E402

SCHEMA_PATH = PACKET_ROOT / "schema" / "schema.json"
CONFIG_PATH = PACKET_ROOT / "config" / "draft-config-v0.1.json"
ASSIGNMENT_PATH = PACKET_ROOT / "config" / "proposed-gate3-assignment-v0.1.json"

PROBED_SCENARIO = "scenario_dev_t01_f000_r00"
PROBE_FREE_SCENARIO = "scenario_dev_t00_f000_r00"
SENSOR_FAULT_SETTING = "fault_dev_sensor_encoder_bias_loc0_sev0p05"
SCREEN_PROVENANCE = "dev-" + hashlib.sha256(b"screen-override-test").hexdigest()


def binding():
    """Return the validated draft-config / approved-assignment binding."""

    config = load_config(CONFIG_PATH, SCHEMA_PATH)
    assignment = load_assignment(ASSIGNMENT_PATH)
    return validate_approved_assignment_binding(
        config, expected_assignment=assignment
    )


def reservation_for(document, predicate):
    """Return the first expanded reservation satisfying ``predicate``."""

    return next(row for row in expand_reservations(document) if predicate(row))


def structural_override_faults(severity=0.75, onset_index=500):
    """Return a one-element structural fault tuple in the screen's shape."""

    return (
        FaultSpec(
            source_class="structure",
            subtype="link_stiffness_loss",
            location=1,
            severity=severity,
            onset_index=onset_index,
            compound_flag=False,
            ood_flag=False,
        ),
    )


# --------------------------------------------------------------------------
# ScreenOverrides semantics
# --------------------------------------------------------------------------


def test_default_overrides_are_inert_and_an_empty_fault_tuple_is_active() -> None:
    """An empty fault tuple is falsy but is still an explicit override."""

    assert not ScreenOverrides().is_active()
    assert ScreenOverrides(physical_faults=()).is_active()
    assert ScreenOverrides(physical_faults=structural_override_faults()).is_active()
    assert ScreenOverrides(probe_peak_force_n=0.05).is_active()
    assert ScreenOverrides(probe_ramp_fraction_of_duration=0.125).is_active()
    assert ScreenOverrides(realized_pair_id="basepair_screen_c4").is_active()
    assert ScreenOverrides(distal_payload_mass_kg=0.0).is_active()
    # provenance_hash records which screen produced a deviating rollout; it does
    # not itself deviate one, so it must not make an inert override active.
    assert not ScreenOverrides(provenance_hash=SCREEN_PROVENANCE).is_active()


# --------------------------------------------------------------------------
# screen_pair_id
# --------------------------------------------------------------------------


def test_screen_pair_id_suffixes_only_the_unoverridden_path() -> None:
    """The dataset suffix is applied only when no realized id is supplied."""

    source = reservation_for(
        binding().assignment, lambda row: row.scenario_spec_id == PROBED_SCENARIO
    )
    expected = f"{source.base_pair_id}_dataset0"
    assert screen_pair_id(source, None) == expected
    assert screen_pair_id(source, ScreenOverrides()) == expected
    assert (
        screen_pair_id(source, ScreenOverrides(physical_faults=())) == expected
    )
    screened = screen_pair_id(
        source, ScreenOverrides(realized_pair_id="basepair_protocolp_stageAB_c4")
    )
    assert screened == "basepair_protocolp_stageAB_c4"
    assert not screened.endswith("_dataset0")


# --------------------------------------------------------------------------
# Provenance validation and the stamped hash
# --------------------------------------------------------------------------


def test_stamped_hash_is_the_base_hash_without_an_active_override() -> None:
    """Absent and inert overrides both stamp the approved configuration hash."""

    base = binding().config.config_hash
    assert _screen_stamped_hash(None, base) == base
    assert _screen_stamped_hash(ScreenOverrides(), base) == base


def test_inactive_override_carrying_provenance_is_refused() -> None:
    """A provenance hash that cannot take effect raises instead of being dropped."""

    base = binding().config.config_hash
    with pytest.raises(AssignmentGenerationError, match="without an active override"):
        _screen_stamped_hash(
            ScreenOverrides(provenance_hash=SCREEN_PROVENANCE), base
        )


def test_valid_provenance_is_stamped_and_passes_the_packet_hash_validator() -> None:
    """An active override stamps a lifecycle-valid, base-distinct screen hash."""

    base = binding().config.config_hash
    overrides = ScreenOverrides(
        physical_faults=(), provenance_hash=SCREEN_PROVENANCE
    )
    stamped = _screen_stamped_hash(overrides, base)
    assert stamped == SCREEN_PROVENANCE
    assert stamped != base
    assert stamped.startswith("dev-")
    assert _valid_config_hash(stamped)


@pytest.mark.parametrize(
    ("provenance", "expected"),
    [
        (None, "nonempty provenance_hash"),
        ("", "nonempty provenance_hash"),
        (hashlib.sha256(b"no-prefix").hexdigest(), "dev- lifecycle prefix"),
        ("protocolp-" + hashlib.sha256(b"x").hexdigest(), "dev- lifecycle prefix"),
        ("dev-" + hashlib.sha256(b"short").hexdigest()[:63], "lowercase SHA-256"),
        ("dev-" + hashlib.sha256(b"long").hexdigest() + "0", "lowercase SHA-256"),
        ("dev-" + hashlib.sha256(b"upper").hexdigest().upper(), "lowercase SHA-256"),
        ("dev-" + "z" * 64, "lowercase SHA-256"),
    ],
)
def test_active_override_refuses_a_lifecycle_invalid_provenance(
    provenance, expected
) -> None:
    """Every rejected provenance form named by the seam contract raises."""

    base = binding().config.config_hash
    overrides = ScreenOverrides(physical_faults=(), provenance_hash=provenance)
    with pytest.raises(AssignmentGenerationError, match=expected):
        _screen_stamped_hash(overrides, base)


def test_active_override_refuses_the_base_config_hash_as_provenance() -> None:
    """The base hash satisfies every format rule, so it needs its own guard."""

    base = binding().config.config_hash
    assert _valid_config_hash(base) and base.startswith("dev-")
    overrides = ScreenOverrides(physical_faults=(), provenance_hash=base)
    with pytest.raises(AssignmentGenerationError, match="differ from the base"):
        _screen_stamped_hash(overrides, base)


# --------------------------------------------------------------------------
# _physical_config probe overrides
# --------------------------------------------------------------------------


def probed_physical_config(overrides=None):
    """Build the probed dev trajectory's mechanics config under ``overrides``."""

    document = binding().assignment
    control_dt_s = _runtime_parameters(binding()).control_dt_s
    source = reservation_for(
        document, lambda row: row.scenario_spec_id == PROBED_SCENARIO
    )
    _, trajectory = _profile(document, source)
    return _physical_config(
        document,
        source,
        trajectory,
        control_dt_s=control_dt_s,
        overrides=overrides,
    ), trajectory


def test_probe_overrides_default_to_current_behaviour() -> None:
    """No override, an inert override, and fraction 0.5 all agree exactly."""

    baseline, trajectory = probed_physical_config(None)
    inert, _ = probed_physical_config(ScreenOverrides())
    duration = float(trajectory["diagnostic_probe"]["cycles"]) / float(
        trajectory["diagnostic_probe"]["frequency_hz"]
    )
    assert baseline == inert
    assert baseline.diagnostic_tip_load_ramp_s == duration / 2.0
    assert baseline.diagnostic_tip_load_peak_n == float(
        trajectory["diagnostic_probe"]["peak_force_n"]
    )
    # Fraction 0.5 is the boundary the current computed default already sits at,
    # so the override path must reproduce it bit-for-bit rather than merely
    # approximate it.
    boundary, _ = probed_physical_config(
        ScreenOverrides(probe_ramp_fraction_of_duration=0.5)
    )
    assert boundary.diagnostic_tip_load_ramp_s == duration / 2.0
    assert boundary == baseline


def test_probe_ramp_fraction_override_reaches_the_screen_only_value() -> None:
    """Fraction 0.125 is reachable by no assignment-document input at all."""

    baseline, _ = probed_physical_config(None)
    duration = baseline.diagnostic_tip_load_duration_s
    assert duration == pytest.approx(1.25)
    screened, _ = probed_physical_config(
        ScreenOverrides(probe_ramp_fraction_of_duration=0.125)
    )
    assert screened.diagnostic_tip_load_ramp_s == duration * 0.125
    assert screened.diagnostic_tip_load_ramp_s == pytest.approx(0.15625)
    assert screened.diagnostic_tip_load_ramp_s != baseline.diagnostic_tip_load_ramp_s
    # Nothing else may move with it.
    assert screened.diagnostic_tip_load_peak_n == baseline.diagnostic_tip_load_peak_n
    assert screened.diagnostic_tip_load_start_s == baseline.diagnostic_tip_load_start_s
    assert screened.diagnostic_tip_load_duration_s == duration


def test_probe_peak_override_applies_and_leaves_the_rest_fixed() -> None:
    """A peak override changes only the peak force."""

    baseline, _ = probed_physical_config(None)
    screened, _ = probed_physical_config(ScreenOverrides(probe_peak_force_n=0.15))
    assert screened.diagnostic_tip_load_peak_n == 0.15
    assert screened.diagnostic_tip_load_ramp_s == baseline.diagnostic_tip_load_ramp_s
    assert screened.diagnostic_tip_load_start_s == baseline.diagnostic_tip_load_start_s
    assert (
        screened.diagnostic_tip_load_duration_s
        == baseline.diagnostic_tip_load_duration_s
    )


def test_payload_mass_override_is_the_sole_mass_source() -> None:
    """The explicit scalar replaces the catalog mass and changes nothing else."""

    baseline, _ = probed_physical_config(None)
    screened, _ = probed_physical_config(
        ScreenOverrides(distal_payload_mass_kg=0.123)
    )
    assert screened.distal_payload_mass_kg == 0.123
    assert screened != baseline
    assert dataclasses.replace(
        screened, distal_payload_mass_kg=baseline.distal_payload_mass_kg
    ) == baseline


@pytest.mark.parametrize("mass", [-0.001, float("nan"), float("inf"), "not-a-mass"])
def test_payload_mass_override_refuses_negative_or_nonfinite(mass) -> None:
    """An invalid payload must fail before the plant is built."""

    with pytest.raises(AssignmentGenerationError, match="finite and nonnegative"):
        probed_physical_config(ScreenOverrides(distal_payload_mass_kg=mass))


def test_zero_payload_mass_override_is_valid_and_reaches_the_config() -> None:
    """Zero is a physical mass and must not be mistaken for an absent override."""

    screened, _ = probed_physical_config(
        ScreenOverrides(distal_payload_mass_kg=0.0)
    )
    assert screened.distal_payload_mass_kg == 0.0


@pytest.mark.parametrize("peak", [0.0, -0.05, float("nan"), float("inf")])
def test_probe_peak_override_refuses_nonpositive_or_nonfinite(peak) -> None:
    """A peak that is not finite and positive raises before the plant is built."""

    with pytest.raises(AssignmentGenerationError, match="finite and positive"):
        probed_physical_config(ScreenOverrides(probe_peak_force_n=peak))


@pytest.mark.parametrize(
    "fraction", [0.0, -0.125, 0.5001, 1.0, float("nan"), float("inf")]
)
def test_probe_ramp_fraction_override_refuses_values_outside_the_envelope(
    fraction,
) -> None:
    """The admissible fraction is (0, 0.5], matching the mechanics envelope."""

    with pytest.raises(AssignmentGenerationError, match=r"finite in \(0, 0.5\]"):
        probed_physical_config(
            ScreenOverrides(probe_ramp_fraction_of_duration=fraction)
        )


def probe_free_physical_config(overrides):
    """Build the probe-free dev trajectory's mechanics config under ``overrides``."""

    document = binding().assignment
    control_dt_s = _runtime_parameters(binding()).control_dt_s
    source = reservation_for(
        document, lambda row: row.scenario_spec_id == PROBE_FREE_SCENARIO
    )
    _, trajectory = _profile(document, source)
    assert trajectory["diagnostic_probe"] is None
    return _physical_config(
        document,
        source,
        trajectory,
        control_dt_s=control_dt_s,
        overrides=overrides,
    )


@pytest.mark.parametrize(
    "overrides",
    [
        ScreenOverrides(probe_peak_force_n=0.05),
        ScreenOverrides(probe_ramp_fraction_of_duration=0.125),
        ScreenOverrides(probe_peak_force_n=0.05, probe_ramp_fraction_of_duration=0.5),
    ],
)
def test_probe_override_on_a_probe_free_trajectory_raises(overrides) -> None:
    """A probe override that cannot take effect must not be silently discarded."""

    with pytest.raises(AssignmentGenerationError, match="probe-free trajectory"):
        probe_free_physical_config(overrides)


def test_non_probe_overrides_are_allowed_on_a_probe_free_trajectory() -> None:
    """The probe-free guard is narrow: only probe fields trigger it."""

    config = probe_free_physical_config(
        ScreenOverrides(
            physical_faults=structural_override_faults(),
            realized_pair_id="basepair_protocolp_negative_control",
            distal_payload_mass_kg=0.075,
            provenance_hash=SCREEN_PROVENANCE,
        )
    )
    assert config.diagnostic_tip_load_peak_n == 0.0
    assert config.diagnostic_tip_load_duration_s is None
    assert config.distal_payload_mass_kg == 0.075


# --------------------------------------------------------------------------
# _generate_reservation
# --------------------------------------------------------------------------


def test_physical_faults_override_is_refused_on_a_sensor_fault_reservation() -> None:
    """A sensor fault would survive the override and confound the screen body."""

    current = binding()
    runtime = _runtime_parameters(current)
    source = reservation_for(
        current.assignment,
        lambda row: row.fault_setting_id == SENSOR_FAULT_SETTING,
    )
    overrides = ScreenOverrides(
        physical_faults=structural_override_faults(),
        realized_pair_id="basepair_protocolp_sensorclash",
        provenance_hash=SCREEN_PROVENANCE,
    )
    with pytest.raises(AssignmentGenerationError, match="derives a sensor fault"):
        _generate_reservation(
            current.assignment,
            current.config.config_hash,
            ("S",),
            8,
            int(current.config.document["values"]["timing"]["window_steps"]),
            runtime,
            source,
            overrides=overrides,
        )


def test_active_override_stamps_provenance_on_every_produced_artifact() -> None:
    """The stamped hash, not the base hash, reaches the observed record.

    ``config_hash`` is a stored ``ObservedRecord`` field, so this is what keeps
    a screen artifact permanently distinguishable from an approved-configuration
    artifact. A truncated rollout is used because the property is an identity
    property and does not depend on run length.
    """

    current = binding()
    runtime = _runtime_parameters(current)
    history = int(current.config.document["values"]["timing"]["window_steps"])
    source = reservation_for(
        current.assignment, lambda row: row.scenario_spec_id == PROBED_SCENARIO
    )
    overrides = ScreenOverrides(
        probe_peak_force_n=0.05,
        probe_ramp_fraction_of_duration=0.125,
        physical_faults=structural_override_faults(),
        realized_pair_id="basepair_protocolp_stageAB_c4",
        provenance_hash=SCREEN_PROVENANCE,
    )
    pair_id, plant, observations, _, _, _ = _generate_reservation(
        current.assignment,
        current.config.config_hash,
        ("S",),
        24,
        history,
        runtime,
        source,
        overrides=overrides,
    )
    assert pair_id == "basepair_protocolp_stageAB_c4"
    assert plant.step.shape[0] == 24
    observed = observations["S"]
    assert observed.config_hash == SCREEN_PROVENANCE
    assert observed.config_hash != current.config.config_hash
    assert observed.pair_id == "basepair_protocolp_stageAB_c4"
    assert not observed.pair_id.endswith("_dataset0")


def test_unoverridden_generation_stamps_the_base_hash_and_dataset_identity() -> None:
    """The negative control that makes the assertion above discriminating."""

    current = binding()
    runtime = _runtime_parameters(current)
    history = int(current.config.document["values"]["timing"]["window_steps"])
    source = reservation_for(
        current.assignment, lambda row: row.scenario_spec_id == PROBED_SCENARIO
    )
    pair_id, _, observations, _, _, _ = _generate_reservation(
        current.assignment,
        current.config.config_hash,
        ("S",),
        24,
        history,
        runtime,
        source,
    )
    assert pair_id == f"{source.base_pair_id}_dataset0"
    observed = observations["S"]
    assert observed.config_hash == current.config.config_hash
    assert observed.config_hash != SCREEN_PROVENANCE
    assert observed.pair_id.endswith("_dataset0")


def test_probe_overrides_reach_the_plant_that_is_actually_simulated(
    monkeypatch,
) -> None:
    """The seam must forward overrides to the mechanics config, not just accept them.

    Testing ``_physical_config`` directly cannot see this: those tests supply the
    overrides themselves, so a ``_generate_reservation`` that never forwards them
    passes every one of them while silently simulating the delivered probe. The
    probe begins 2.0 s into the run, so observing its effect on the gauges would
    cost a full-length rollout; the constructed config is captured at the plant
    construction site instead, which is where the wire either exists or does not.
    """

    import utils.assignment_generator as generator_module

    current = binding()
    runtime = _runtime_parameters(current)
    history = int(current.config.document["values"]["timing"]["window_steps"])
    source = reservation_for(
        current.assignment, lambda row: row.scenario_spec_id == PROBED_SCENARIO
    )
    built: list[object] = []
    real_plant = generator_module.CablePlant

    def capturing_plant(physical_config, **kwargs):
        built.append(physical_config)
        return real_plant(physical_config, **kwargs)

    monkeypatch.setattr(generator_module, "CablePlant", capturing_plant)

    def run(overrides):
        _generate_reservation(
            current.assignment,
            current.config.config_hash,
            ("S",),
            8,
            history,
            runtime,
            source,
            overrides=overrides,
        )

    run(
        ScreenOverrides(
            probe_peak_force_n=0.15,
            probe_ramp_fraction_of_duration=0.125,
            physical_faults=(),
            realized_pair_id="basepair_protocolp_wire_c4",
            provenance_hash=SCREEN_PROVENANCE,
        )
    )
    run(None)
    screened, delivered = built
    assert screened.diagnostic_tip_load_peak_n == 0.15
    assert screened.diagnostic_tip_load_ramp_s == pytest.approx(0.15625)
    # The delivered values differ, so the assertions above discriminate.
    assert delivered.diagnostic_tip_load_peak_n != 0.15
    assert delivered.diagnostic_tip_load_ramp_s == pytest.approx(0.625)


def test_stamped_hash_also_reaches_the_closed_loop_sensor_session(
    monkeypatch,
) -> None:
    """The session's stamp is unreachable downstream, so capture it at the call.

    ``_generate_reservation`` discards ``result.observations``, which is the only
    object carrying ``OnlineSensorSession.config_hash``, so the session half of
    the stamping requirement cannot be asserted from the return value -- the
    same unreachability that moved the plant's softening boundary into its own
    test. The wiring is therefore captured where it happens.
    """

    import utils.assignment_generator as generator_module

    current = binding()
    runtime = _runtime_parameters(current)
    history = int(current.config.document["values"]["timing"]["window_steps"])
    source = reservation_for(
        current.assignment, lambda row: row.scenario_spec_id == PROBED_SCENARIO
    )
    stamped: list[str] = []
    real_session = generator_module.OnlineSensorSession

    def capturing_session(*args, **kwargs):
        stamped.append(kwargs["config_hash"])
        return real_session(*args, **kwargs)

    monkeypatch.setattr(
        generator_module, "OnlineSensorSession", capturing_session
    )

    def run(overrides):
        _generate_reservation(
            current.assignment,
            current.config.config_hash,
            ("S",),
            8,
            history,
            runtime,
            source,
            overrides=overrides,
        )

    run(
        ScreenOverrides(
            physical_faults=(),
            realized_pair_id="basepair_protocolp_session_c4",
            provenance_hash=SCREEN_PROVENANCE,
        )
    )
    assert stamped == [SCREEN_PROVENANCE]
    run(None)
    assert stamped == [SCREEN_PROVENANCE, current.config.config_hash]


def test_physical_faults_override_replaces_the_derived_healthy_list() -> None:
    """A healthy reservation's plant carries the override's structural fault.

    The derived list for ``fault_dev_healthy`` is empty, so the softened model
    exists only if the override reached ``CablePlant``. Whether the softening
    activates at the declared onset is the separate plant-contract property
    covered by ``test_cable_plant_softening_boundary``.
    """

    current = binding()
    runtime = _runtime_parameters(current)
    history = int(current.config.document["values"]["timing"]["window_steps"])
    source = reservation_for(
        current.assignment, lambda row: row.scenario_spec_id == PROBED_SCENARIO
    )
    assert source.fault_setting_id == "fault_dev_healthy"
    healthy_pair, healthy_plant, _, _, _, _ = _generate_reservation(
        current.assignment,
        current.config.config_hash,
        ("S",),
        24,
        history,
        runtime,
        source,
        overrides=ScreenOverrides(
            physical_faults=(),
            realized_pair_id="basepair_protocolp_healthy_c4",
            provenance_hash=SCREEN_PROVENANCE,
        ),
    )
    faulted_pair, faulted_plant, _, _, _, _ = _generate_reservation(
        current.assignment,
        current.config.config_hash,
        ("S",),
        24,
        history,
        runtime,
        source,
        overrides=ScreenOverrides(
            physical_faults=structural_override_faults(severity=0.35, onset_index=0),
            realized_pair_id="basepair_protocolp_healthy_c4",
            provenance_hash=SCREEN_PROVENANCE,
        ),
    )
    # Same identity, same probe, same context: the only difference is the
    # override's fault list, so any divergence is attributable to it.
    assert healthy_pair == faulted_pair
    assert healthy_plant.gauge_true.shape == faulted_plant.gauge_true.shape
    assert abs(faulted_plant.gauge_true).max() != abs(healthy_plant.gauge_true).max()
