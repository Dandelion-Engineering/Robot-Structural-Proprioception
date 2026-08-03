"""Real Gate-3 assignment-driven research-data generation and independent audit.

This module materializes only the draft-authorized ``dev``, ``pilot``, and
``val`` reservations. It deliberately has no path that accepts ``test`` under
the draft lifecycle. Dataset identities use ``train_seed=0``: the five model
training seeds belong to the later fit/evaluation expansion and must not be
invented before those fits exist.
"""

from __future__ import annotations

import dataclasses
import functools
import math
from collections import Counter
from concurrent.futures import ProcessPoolExecutor
from pathlib import Path
from typing import Any, Iterable, Mapping, Sequence

import numpy as np

from .assignment_binding import ApprovedAssignmentBinding
from .cable_mechanics import CableModelConfig
from .cable_plant import CablePlant
from .gate3_assignment import (
    ScenarioReservation,
    expanded_fault_settings,
    expand_reservations,
)
from .online_loop import run_online_rollout
from .role_contract import DatasetRoleBuilder, RolePayloadLoader
from .schema_types import (
    CHANNEL_NAMES,
    FaultSpec,
    ObservedRecord,
    PrivilegedRecord,
)
from .sensor_model import OnlineSensorSession, SensorModel
from .storage_contract import (
    DeployableObservationLoader,
    IdentityManifestRow,
    audit_identity_manifest,
    re_full_sha256,
    read_identity_manifest,
    read_role_index,
)
from .task_control import BoundedTaskProfile, ObservedJointPDController

RESEARCH_SPLITS = ("dev", "pilot", "val")
BASE_DATASET_SUITES = ("C0", "C1", "S")
DATASET_IDENTITY_TRAIN_SEED = 0
ESTIMATOR_ID = "gate4_unfit_shared_capacity_v1"
CONTROLLER_ID = "bounded_observed_pd_no_recovery_v1"


class AssignmentGenerationError(ValueError):
    """Raised when generation could drift from the approved assignment."""


@dataclasses.dataclass(frozen=True)
class GenerationRuntimeParameters:
    """Runtime constants read from the bound draft configuration authority."""

    control_dt_s: float
    f_ctrl_hz: float
    simulation_timestep_s: float
    point_count: int


@dataclasses.dataclass(frozen=True)
class ScreenOverrides:
    """Typed screen-only deviations from the approved assignment document.

    Every field defaults to ``None``, which means "use the approved value", so a
    default-constructed instance is inert and the production path is unchanged.
    ``physical_faults`` distinguishes ``None`` (use the reservation's derived
    fault list) from ``()`` (an explicit healthy body), so every guard on it
    must test ``is not None`` rather than truthiness -- an empty tuple is falsy.

    ``provenance_hash`` is deliberately excluded from :meth:`is_active`: it does
    not itself change what is simulated, it records which screen produced an
    already-deviating rollout.
    """

    probe_peak_force_n: float | None = None
    probe_ramp_fraction_of_duration: float | None = None
    physical_faults: tuple[FaultSpec, ...] | None = None
    realized_pair_id: str | None = None
    distal_payload_mass_kg: float | None = None
    provenance_hash: str | None = None

    def is_active(self) -> bool:
        """Return whether any field deviates the simulated or realized rollout."""

        return any(
            value is not None
            for value in (
                self.probe_peak_force_n,
                self.probe_ramp_fraction_of_duration,
                self.physical_faults,
                self.realized_pair_id,
                self.distal_payload_mass_kg,
            )
        )


def screen_pair_id(
    reservation: ScenarioReservation, overrides: ScreenOverrides | None
) -> str:
    """Return the realized pair id one rollout must use.

    Inputs: the source reservation and its optional screen overrides. Output:
    the override's realized pair id when supplied, else the reservation's
    approved dataset-realized id. The dataset suffix is applied only on the
    unoverridden path, so a screen identity is suffix-free by construction and
    cannot collide with an approved dataset identity.
    """

    if overrides is not None and overrides.realized_pair_id is not None:
        return str(overrides.realized_pair_id)
    return f"{reservation.base_pair_id}_dataset0"


def _screen_stamped_hash(
    overrides: ScreenOverrides | None, config_hash: str
) -> str:
    """Return the configuration hash one rollout must stamp on its artifacts.

    Inputs: the optional screen overrides and the base configuration hash.
    Output: the base hash when no override is active, else the override's
    validated screen provenance hash. Raises ``AssignmentGenerationError``
    unless an active override carries a nonempty ``dev-`` prefixed provenance
    hash whose remainder is one lowercase SHA-256 digest and which differs from
    the base hash, so an overridden rollout can never present itself as an
    approved-configuration rollout.
    """

    if overrides is None:
        return config_hash
    provenance = overrides.provenance_hash
    if not overrides.is_active():
        if provenance is not None:
            raise AssignmentGenerationError(
                "provenance_hash supplied without an active override; an inactive "
                "override must not silently stamp the base config hash"
            )
        return config_hash
    if not isinstance(provenance, str) or not provenance:
        raise AssignmentGenerationError(
            "an active screen override requires a nonempty provenance_hash string"
        )
    if not provenance.startswith("dev-"):
        raise AssignmentGenerationError(
            "screen provenance_hash must carry the dev- lifecycle prefix"
        )
    if not re_full_sha256(provenance[4:]):
        raise AssignmentGenerationError(
            "screen provenance_hash must be dev- plus one lowercase SHA-256 digest"
        )
    if provenance == config_hash:
        raise AssignmentGenerationError(
            "screen provenance_hash must differ from the base config hash"
        )
    return provenance


def _runtime_parameters(
    binding: ApprovedAssignmentBinding,
) -> GenerationRuntimeParameters:
    """Read and cross-check generator timing/mechanics constants from config."""

    values = binding.config.document.get("values")
    timing = values.get("timing") if isinstance(values, Mapping) else None
    plant = values.get("plant") if isinstance(values, Mapping) else None
    if not isinstance(timing, Mapping) or not isinstance(plant, Mapping):
        raise AssignmentGenerationError("bound config lacks timing or plant authority")
    try:
        parameters = GenerationRuntimeParameters(
            control_dt_s=float(timing["control_dt_s"]),
            f_ctrl_hz=float(timing["f_ctrl_hz"]),
            simulation_timestep_s=float(plant["simulation_timestep_s"]),
            point_count=int(plant["point_count_per_link"]),
        )
    except (KeyError, TypeError, ValueError) as exc:
        raise AssignmentGenerationError(
            "bound config timing or plant authority is malformed"
        ) from exc
    numeric = (
        parameters.control_dt_s,
        parameters.f_ctrl_hz,
        parameters.simulation_timestep_s,
    )
    if not all(math.isfinite(value) and value > 0.0 for value in numeric):
        raise AssignmentGenerationError("bound runtime constants must be finite positive")
    if parameters.point_count < 3:
        raise AssignmentGenerationError("bound point_count_per_link must be at least 3")
    if not math.isclose(
        parameters.control_dt_s * parameters.f_ctrl_hz,
        1.0,
        rel_tol=0.0,
        abs_tol=1.0e-12,
    ):
        raise AssignmentGenerationError(
            "bound control_dt_s and f_ctrl_hz are not reciprocal"
        )
    physics_steps = parameters.control_dt_s / parameters.simulation_timestep_s
    if not math.isclose(
        physics_steps,
        round(physics_steps),
        rel_tol=0.0,
        abs_tol=1.0e-12,
    ):
        raise AssignmentGenerationError(
            "bound control_dt_s is not an integer multiple of simulation_timestep_s"
        )
    return parameters


def _step_index(time_s: float, control_dt_s: float) -> int:
    """Convert a nonnegative grid-aligned time to its exact control-step index."""

    if (
        not math.isfinite(time_s)
        or time_s < 0.0
        or not math.isfinite(control_dt_s)
        or control_dt_s <= 0.0
    ):
        raise AssignmentGenerationError("time and control_dt_s must be finite and valid")
    raw_index = time_s / control_dt_s
    index = int(round(raw_index))
    if not math.isclose(raw_index, index, rel_tol=0.0, abs_tol=1.0e-9):
        raise AssignmentGenerationError(
            f"time {time_s} s is not aligned to control_dt_s={control_dt_s}"
        )
    return index


def _catalog(items: Iterable[Mapping[str, Any]]) -> dict[str, Mapping[str, Any]]:
    return {str(item["id"]): item for item in items}


def _selected_reservations(
    assignment: Mapping[str, Any],
    splits: Sequence[str],
    reservation_limit: int | None,
) -> list[ScenarioReservation]:
    if not splits or any(split not in RESEARCH_SPLITS for split in splits):
        raise AssignmentGenerationError(
            f"splits must be a nonempty subset of {RESEARCH_SPLITS}"
        )
    rows = [
        row for row in expand_reservations(assignment) if row.split in set(splits)
    ]
    if reservation_limit is not None:
        if reservation_limit <= 0:
            raise AssignmentGenerationError("reservation_limit must be positive")
        rows = rows[:reservation_limit]
    if not rows:
        raise AssignmentGenerationError("selection produced no research reservation")
    return rows


def build_identity_manifest(
    binding: ApprovedAssignmentBinding,
    *,
    splits: Sequence[str] = RESEARCH_SPLITS,
    suites: Sequence[str] = BASE_DATASET_SUITES,
    reservation_limit: int | None = None,
) -> tuple[list[IdentityManifestRow], list[ScenarioReservation]]:
    """Expand dataset-identity rows without inventing future model-fit seeds."""

    if tuple(binding.authorized_research_splits) != RESEARCH_SPLITS:
        raise AssignmentGenerationError("binding research authorization drifted")
    if (
        not suites
        or len(set(suites)) != len(suites)
        or any(suite not in BASE_DATASET_SUITES for suite in suites)
        or not {"C1", "S"}.issubset(set(suites))
    ):
        raise AssignmentGenerationError(
            "base suites must be unique C0/C1/S values and include matched C1/S"
        )
    reservations = _selected_reservations(
        binding.assignment, splits, reservation_limit
    )
    rows: list[IdentityManifestRow] = []
    for reservation in reservations:
        pair_id = f"{reservation.base_pair_id}_dataset0"
        for suite in suites:
            rows.append(
                IdentityManifestRow(
                    schema_version=reservation.schema_version,
                    config_hash=binding.config.config_hash,
                    scenario_spec_id=reservation.scenario_spec_id,
                    pair_id=pair_id,
                    run_id=f"{reservation.scenario_spec_id}_{suite}_dataset0",
                    trajectory_spec_id=reservation.trajectory_spec_id,
                    fault_setting_id=reservation.fault_setting_id,
                    split_group_id=reservation.split_group_id,
                    split=reservation.split,
                    suite=suite,
                    estimator_id=ESTIMATOR_ID,
                    controller_id=CONTROLLER_ID,
                    payload_id=reservation.payload_id,
                    env_profile_id=reservation.env_profile_id,
                    contact_profile_id=reservation.contact_profile_id,
                    sim_seed=reservation.sim_seed,
                    fault_seed=reservation.fault_seed,
                    sensor_seed=reservation.sensor_seed,
                    controller_seed=reservation.controller_seed,
                    train_seed=DATASET_IDENTITY_TRAIN_SEED,
                )
            )
    audit_manifest_against_assignment(
        rows,
        reservations,
        expected_suites=tuple(suites),
        config_hash=binding.config.config_hash,
    )
    return rows, reservations


def audit_manifest_against_assignment(
    rows: Iterable[IdentityManifestRow],
    reservations: Iterable[ScenarioReservation],
    *,
    expected_suites: tuple[str, ...],
    config_hash: str,
) -> dict[str, Any]:
    """Compare every produced identity field to approved reservations directly."""

    manifest = list(rows)
    approved = {row.base_pair_id: row for row in reservations}
    by_base: dict[str, list[IdentityManifestRow]] = {}
    for row in manifest:
        if row.split == "test":
            raise AssignmentGenerationError("test identity materialization is forbidden")
        suffix = "_dataset0"
        if not row.pair_id.endswith(suffix):
            raise AssignmentGenerationError("dataset pair_id lacks the dataset0 suffix")
        by_base.setdefault(row.pair_id[: -len(suffix)], []).append(row)
    if set(by_base) != set(approved):
        raise AssignmentGenerationError("manifest reservation set differs from selection")

    compared_fields = (
        "scenario_spec_id",
        "trajectory_spec_id",
        "fault_setting_id",
        "split_group_id",
        "split",
        "payload_id",
        "env_profile_id",
        "contact_profile_id",
        "sim_seed",
        "fault_seed",
        "sensor_seed",
        "controller_seed",
    )
    for base_pair_id, group in by_base.items():
        reservation = approved[base_pair_id]
        if tuple(row.suite for row in group) != expected_suites:
            raise AssignmentGenerationError(
                f"{base_pair_id} suite rows do not match {expected_suites}"
            )
        for row in group:
            if row.config_hash != config_hash or row.train_seed != 0:
                raise AssignmentGenerationError("manifest lifecycle identity drifted")
            for field in compared_fields:
                if getattr(row, field) != getattr(reservation, field):
                    raise AssignmentGenerationError(
                        f"{base_pair_id}.{field} differs from approved reservation"
                    )
    return {
        "status": "manifest_matches_approved_research_reservations",
        "reservations": len(approved),
        "manifest_rows": len(manifest),
        "suites": list(expected_suites),
        "splits": dict(Counter(row.split for row in approved.values())),
        "train_seed": DATASET_IDENTITY_TRAIN_SEED,
        "test_rows": 0,
    }


def _profile(
    assignment: Mapping[str, Any], reservation: ScenarioReservation
) -> tuple[BoundedTaskProfile, Mapping[str, Any]]:
    trajectory = _catalog(assignment["trajectory_specs"])[
        reservation.trajectory_spec_id
    ]
    onset = float(trajectory["onset_time_s"])
    events = trajectory["relative_task_events_s"]
    profile = BoundedTaskProfile(
        target_joint_rad=tuple(float(value) for value in trajectory["target_joint_rad"]),
        movement_start_s=onset + float(events["movement_start"]),
        transition_s=float(events["transition"]),
        hold_end_s=onset + float(events["hold_end"]),
        return_end_s=onset + float(events["return_end"]),
    )
    profile.validate()
    return profile, trajectory


def _physical_config(
    assignment: Mapping[str, Any],
    reservation: ScenarioReservation,
    trajectory: Mapping[str, Any],
    *,
    control_dt_s: float,
    overrides: ScreenOverrides | None = None,
) -> CableModelConfig:
    contexts = assignment["context_profiles"]
    payload = _catalog(contexts["payloads"])[reservation.payload_id]
    contact = _catalog(contexts["contacts"])[reservation.contact_profile_id]
    plane = contact["endpoint_plane_z_m"]
    offsets = contact["contact_window_offset_s"]
    onset = float(trajectory["onset_time_s"])
    contact_window = (
        None
        if offsets is None
        else (onset + float(offsets[0]), onset + float(offsets[1]))
    )
    probe = trajectory["diagnostic_probe"]
    peak_override = None if overrides is None else overrides.probe_peak_force_n
    ramp_fraction_override = (
        None if overrides is None else overrides.probe_ramp_fraction_of_duration
    )
    payload_mass_override = (
        None if overrides is None else overrides.distal_payload_mass_kg
    )
    payload_mass_kg = float(payload["distal_payload_mass_kg"])
    if payload_mass_override is not None:
        try:
            override_mass_kg = float(payload_mass_override)
        except (TypeError, ValueError) as exc:
            raise AssignmentGenerationError(
                "distal payload mass override must be finite and nonnegative; got "
                f"{payload_mass_override!r}"
            ) from exc
        if not math.isfinite(override_mass_kg) or override_mass_kg < 0.0:
            raise AssignmentGenerationError(
                "distal payload mass override must be finite and nonnegative; got "
                f"{payload_mass_override!r}"
            )
        payload_mass_kg = override_mass_kg
    if probe is None:
        if peak_override is not None or ramp_fraction_override is not None:
            raise AssignmentGenerationError(
                "probe override supplied for a probe-free trajectory "
                f"{reservation.trajectory_spec_id!r}"
            )
        probe_values = {
            "diagnostic_tip_load_peak_n": 0.0,
            "diagnostic_tip_load_start_s": 0.0,
            "diagnostic_tip_load_duration_s": None,
            "diagnostic_tip_load_ramp_s": 0.0,
        }
    else:
        duration = float(probe["cycles"]) / float(probe["frequency_hz"])
        peak_n = float(probe["peak_force_n"])
        if peak_override is not None:
            override_peak_n = float(peak_override)
            if not math.isfinite(override_peak_n) or override_peak_n <= 0.0:
                raise AssignmentGenerationError(
                    "probe peak override must be finite and positive; got "
                    f"{peak_override!r}"
                )
            peak_n = override_peak_n
        ramp_s = duration / 2.0
        if ramp_fraction_override is not None:
            fraction = float(ramp_fraction_override)
            if not math.isfinite(fraction) or not 0.0 < fraction <= 0.5:
                raise AssignmentGenerationError(
                    "probe ramp fraction override must be finite in (0, 0.5]; got "
                    f"{ramp_fraction_override!r}"
                )
            ramp_s = duration * fraction
        probe_values = {
            "diagnostic_tip_load_peak_n": peak_n,
            "diagnostic_tip_load_frequency_hz": float(probe["frequency_hz"]),
            "diagnostic_tip_load_start_s": onset + float(probe["start_offset_s"]),
            "diagnostic_tip_load_duration_s": duration,
            "diagnostic_tip_load_ramp_s": ramp_s,
        }
    return CableModelConfig(
        control_dt_s=control_dt_s,
        distal_payload_mass_kg=payload_mass_kg,
        endpoint_contact_enabled=plane is not None,
        endpoint_contact_plane_z_m=0.2 if plane is None else float(plane),
        endpoint_contact_window_s=contact_window,
        **probe_values,
    )


def _temperature_function(
    assignment: Mapping[str, Any],
    reservation: ScenarioReservation,
    duration_s: float,
):
    environment = _catalog(assignment["context_profiles"]["environments"])[
        reservation.env_profile_id
    ]
    kind = environment["temperature_kind"]
    parameters = environment["parameters"]

    def temperature(_index: int, time_s: float) -> float:
        if kind == "isothermal":
            return float(parameters["temperature_c"])
        if kind == "linear":
            fraction = np.clip(time_s / duration_s, 0.0, 1.0)
            return float(parameters["start_c"]) + float(parameters["delta_c"]) * fraction
        if kind == "sinusoid":
            return float(parameters["center_c"]) + float(
                parameters["amplitude_c"]
            ) * math.sin(2.0 * math.pi * float(parameters["frequency_hz"]) * time_s)
        raise AssignmentGenerationError(f"unsupported temperature profile {kind!r}")

    return temperature


def _fault_components(
    assignment: Mapping[str, Any],
    reservation: ScenarioReservation,
    *,
    control_dt_s: float,
) -> tuple[list[FaultSpec], FaultSpec | None, Mapping[str, Any]]:
    setting = _catalog(expanded_fault_settings(assignment))[
        reservation.fault_setting_id
    ]
    onset_s = float(
        _catalog(assignment["trajectory_specs"])[
            reservation.trajectory_spec_id
        ]["onset_time_s"]
    )
    onset_index = _step_index(onset_s, control_dt_s)
    physical: list[FaultSpec] = []
    sensor: FaultSpec | None = None
    for component in setting["components"]:
        severity = float(component["severity"])
        if component["source_class"] == "sensor" and component["subtype"] in {
            "encoder_bias",
            "encoder_drift",
        }:
            severity *= 1.0 if reservation.fault_seed % 2 == 0 else -1.0
        fault = FaultSpec(
            source_class=str(component["source_class"]),
            subtype=str(component["subtype"]),
            location=int(component["location"]),
            severity=severity,
            onset_index=onset_index,
            compound_flag=bool(setting["label"]["compound_flag"]),
            ood_flag=bool(setting["label"]["ood_flag"]),
        )
        if fault.source_class == "sensor":
            if sensor is not None:
                raise AssignmentGenerationError("multiple sensor components unsupported")
            sensor = fault
        else:
            physical.append(fault)
    return physical, sensor, setting


def shared_channels_equal(left: ObservedRecord, right: ObservedRecord) -> bool:
    """Return whether two suites share bitwise-identical common channels."""

    for channel in CHANNEL_NAMES:
        if not (
            left.suite_available_mask[channel]
            and right.suite_available_mask[channel]
        ):
            continue
        if not np.array_equal(
            left.values[channel], right.values[channel], equal_nan=True
        ):
            return False
        if not np.array_equal(left.valid_mask[channel], right.valid_mask[channel]):
            return False
    return True


def preflight_assigned_mechanics(
    binding: ApprovedAssignmentBinding,
    reservations: Iterable[ScenarioReservation],
) -> dict[str, Any]:
    """Compile and mass-audit every assigned payload before the first rollout."""

    assignment = binding.assignment
    # Materializing a test identity remains forbidden, but compiling each declared
    # scalar mass is a read-only mechanics check required before research generation.
    if not list(reservations):
        raise AssignmentGenerationError("mechanics preflight requires reservations")
    runtime = _runtime_parameters(binding)
    payload_catalog = _catalog(assignment["context_profiles"]["payloads"])
    payload_ids = sorted(payload_catalog)
    nominal = CablePlant(
        CableModelConfig(control_dt_s=runtime.control_dt_s),
        point_count=runtime.point_count,
        simulation_timestep_s=runtime.simulation_timestep_s,
    )
    nominal_mass = float(np.sum(nominal.model.body_mass))
    checked: dict[str, float] = {}
    for payload_id in payload_ids:
        payload_mass = float(payload_catalog[payload_id]["distal_payload_mass_kg"])
        plant = CablePlant(
            CableModelConfig(
                control_dt_s=runtime.control_dt_s,
                distal_payload_mass_kg=payload_mass,
            ),
            point_count=runtime.point_count,
            simulation_timestep_s=runtime.simulation_timestep_s,
        )
        realized = float(np.sum(plant.model.body_mass)) - nominal_mass
        if not np.isclose(realized, payload_mass, rtol=0.0, atol=1.0e-12):
            raise AssignmentGenerationError(
                f"{payload_id} did not realize exact distal mass"
            )
        checked[payload_id] = payload_mass
    return {"payload_masses_kg": checked, "all_exact": True}


def _plant_payload(record: PrivilegedRecord) -> dict[str, np.ndarray]:
    return {
        field.name: np.asarray(getattr(record, field.name))
        for field in dataclasses.fields(record)
    }


def _generate_reservation(
    assignment: Mapping[str, Any],
    config_hash: str,
    suites: tuple[str, ...],
    max_steps: int | None,
    history_steps: int,
    runtime: GenerationRuntimeParameters,
    reservation: ScenarioReservation,
    *,
    overrides: ScreenOverrides | None = None,
) -> tuple[
    str,
    PrivilegedRecord,
    dict[str, ObservedRecord],
    dict[str, np.ndarray],
    int,
    int,
]:
    """Generate one reservation without writing shared dataset indexes."""

    stamped_hash = _screen_stamped_hash(overrides, config_hash)
    profile, trajectory = _profile(assignment, reservation)
    physical_config = _physical_config(
        assignment,
        reservation,
        trajectory,
        control_dt_s=runtime.control_dt_s,
        overrides=overrides,
    )
    physical_faults, sensor_fault, setting = _fault_components(
        assignment,
        reservation,
        control_dt_s=runtime.control_dt_s,
    )
    faults_override = None if overrides is None else overrides.physical_faults
    if faults_override is not None:
        if sensor_fault is not None:
            raise AssignmentGenerationError(
                "physical_faults override is not supported for a reservation whose "
                f"setting {reservation.fault_setting_id!r} derives a sensor fault"
            )
        physical_faults = list(faults_override)
    primary_fault = physical_faults[0] if physical_faults else None
    plant = CablePlant(
        physical_config,
        point_count=runtime.point_count,
        simulation_timestep_s=runtime.simulation_timestep_s,
        fault=primary_fault,
        additional_faults=tuple(physical_faults[1:]),
    )
    control_pair_id = screen_pair_id(reservation, overrides)
    control_sensors = OnlineSensorSession(
        "C0",
        pair_id=control_pair_id,
        sensor_seed=reservation.sensor_seed,
        control_dt_s=physical_config.control_dt_s,
        fault=sensor_fault,
        run_id=f"{reservation.scenario_spec_id}_control",
        config_hash=stamped_hash,
        split=reservation.split,
    )
    controller = ObservedJointPDController(profile)
    full_steps = _step_index(
        float(trajectory["duration_s"]),
        runtime.control_dt_s,
    )
    n_steps = full_steps if max_steps is None else min(full_steps, max_steps)
    result = run_online_rollout(
        plant,
        control_sensors,
        n_steps=n_steps,
        history_steps=history_steps,
        command_policy=controller,
        reference_fn=profile.task_reference,
        temperature_fn=_temperature_function(
            assignment, reservation, float(trajectory["duration_s"])
        ),
    )
    sensor_model = SensorModel()
    observations = {
        suite: sensor_model.observe(
            result.plant,
            suite,
            pair_id=control_pair_id,
            sensor_seed=reservation.sensor_seed,
            fault=sensor_fault,
            run_id=f"{reservation.scenario_spec_id}_{suite}_dataset0",
            config_hash=stamped_hash,
            split=reservation.split,
        )
        for suite in suites
    }
    if "C1" in observations and "S" in observations and not shared_channels_equal(
        observations["C1"], observations["S"]
    ):
        raise AssignmentGenerationError("C1/S shared-channel CRN audit failed")

    label = setting["label"]
    onset_index = _step_index(
        float(trajectory["onset_time_s"]),
        runtime.control_dt_s,
    )
    label_payload = {
        "source_class": np.asarray(label["source_class"]),
        "subtype": np.asarray(label["subtype"]),
        "location": np.asarray(label["location"], dtype=np.int64),
        "severity": np.asarray(label["severity"], dtype=np.float64),
        "onset_index": np.asarray(onset_index, dtype=np.int64),
        "onset_time_s": np.asarray(
            float(trajectory["onset_time_s"]), dtype=np.float64
        ),
        "compound_flag": np.asarray(label["compound_flag"], dtype=np.bool_),
        "ood_flag": np.asarray(label["ood_flag"], dtype=np.bool_),
    }
    return (
        control_pair_id,
        result.plant,
        observations,
        label_payload,
        int(np.count_nonzero(result.plant.safety_flag)),
        int(np.count_nonzero(result.plant.contact_state[:, 1])),
    )


def materialize_base_dataset(
    binding: ApprovedAssignmentBinding,
    schema: Mapping[str, Any],
    output_root,
    *,
    splits: Sequence[str] = RESEARCH_SPLITS,
    suites: Sequence[str] = BASE_DATASET_SUITES,
    reservation_limit: int | None = None,
    max_steps: int | None = None,
    workers: int = 1,
) -> dict[str, Any]:
    """Generate manifest, plant, observation, and label roles for base identities."""

    rows, reservations = build_identity_manifest(
        binding,
        splits=splits,
        suites=suites,
        reservation_limit=reservation_limit,
    )
    mechanics = preflight_assigned_mechanics(binding, reservations)
    builder = DatasetRoleBuilder(output_root, rows, schema, binding.config)
    builder.publish_manifest()
    plant_writer = builder.make_writer("plant")
    label_writer = builder.make_writer("labels")
    observation_writers = {
        suite: builder.make_observation_writer(suite) for suite in suites
    }
    if workers <= 0:
        raise AssignmentGenerationError("workers must be positive")
    assignment = binding.assignment
    runtime = _runtime_parameters(binding)
    safety_events = 0
    contact_steps = 0
    generate = functools.partial(
        _generate_reservation,
        assignment,
        binding.config.config_hash,
        tuple(suites),
        max_steps,
        int(binding.config.document["values"]["timing"]["window_steps"]),
        runtime,
    )
    if workers == 1:
        generated = map(generate, reservations)
        executor = None
    else:
        executor = ProcessPoolExecutor(max_workers=workers)
        generated = executor.map(generate, reservations, chunksize=1)
    try:
        for (
            control_pair_id,
            plant_record,
            observations,
            label_payload,
            reservation_safety_events,
            reservation_contact_steps,
        ) in generated:
            safety_events += reservation_safety_events
            contact_steps += reservation_contact_steps
            for suite in suites:
                row = next(
                    item
                    for item in rows
                    if item.pair_id == control_pair_id and item.suite == suite
                )
                plant_writer.write(row.run_id, _plant_payload(plant_record))
                label_writer.write(row.run_id, label_payload)
                observation_writers[suite].write(observations[suite])
    finally:
        if executor is not None:
            executor.shutdown(wait=True, cancel_futures=True)

    plant_writer.publish_index()
    label_writer.publish_index()
    for writer in observation_writers.values():
        writer.publish_index()
    manifest_audit = audit_manifest_against_assignment(
        rows,
        reservations,
        expected_suites=tuple(suites),
        config_hash=binding.config.config_hash,
    )
    return {
        "status": (
            "truncated_smoke_not_research_data"
            if max_steps is not None or reservation_limit is not None
            else (
                "complete_base_research_dataset"
                if tuple(suites) == BASE_DATASET_SUITES
                else "complete_primary_c1_s_base_research_dataset"
            )
        ),
        "assignment_hash": binding.assignment_hash,
        "config_hash": binding.config.config_hash,
        "manifest_audit": manifest_audit,
        "mechanics_preflight": mechanics,
        "safety_flag_events": safety_events,
        "contact_active_steps": contact_steps,
        "roles_materialized": ["manifest", "plant", "labels", "observations"],
        "roles_intentionally_pending_gate4_fit": [
            "estimator_outputs",
            "controller_logs",
        ],
        "test_identity_or_payload_rows": 0,
    }


def audit_materialized_base_dataset(
    binding: ApprovedAssignmentBinding,
    schema: Mapping[str, Any],
    output_root: Path,
    *,
    expected_splits: Sequence[str] = RESEARCH_SPLITS,
    expected_suites: tuple[str, ...] = ("C1", "S"),
    allow_partial: bool = False,
) -> dict[str, Any]:
    """Independently load and audit every generated base-role payload and pair."""

    root = Path(output_root)
    rows = read_identity_manifest(root / "manifest.csv")
    identity_audit = audit_identity_manifest(
        rows,
        expected_config=binding.config,
        require_complete_c1_s_pairs=True,
    )
    expected_reservations = _selected_reservations(
        binding.assignment,
        expected_splits,
        None,
    )
    if allow_partial:
        present = {
            row.pair_id.removesuffix("_dataset0")
            for row in rows
        }
        expected_reservations = [
            row for row in expected_reservations if row.base_pair_id in present
        ]
    manifest_audit = audit_manifest_against_assignment(
        rows,
        expected_reservations,
        expected_suites=expected_suites,
        config_hash=binding.config.config_hash,
    )
    if not allow_partial:
        expected_count = len(expected_reservations) * len(expected_suites)
        if len(rows) != expected_count:
            raise AssignmentGenerationError(
                f"complete dataset requires {expected_count} rows; got {len(rows)}"
        )

    mechanics_preflight = preflight_assigned_mechanics(
        binding, expected_reservations
    )
    plant_loader = RolePayloadLoader(
        root / "plant", "plant", schema, binding.config
    )
    label_loader = RolePayloadLoader(
        root / "labels", "labels", schema, binding.config
    )
    plant_count = plant_loader.audit_all()
    label_count = label_loader.audit_all()
    if plant_count != len(rows) or label_count != len(rows):
        raise AssignmentGenerationError("plant/label role count differs from manifest")

    observation_loaders = {
        suite: DeployableObservationLoader(
            root / "observations" / suite,
            suite,
            binding.config,
        )
        for suite in expected_suites
    }
    observation_counts = {
        suite: loader.audit_all()
        for suite, loader in observation_loaders.items()
    }
    expected_by_split = Counter(row.split for row in rows if row.suite == expected_suites[0])
    for suite, counts in observation_counts.items():
        if any(counts[split] != expected_by_split[split] for split in RESEARCH_SPLITS):
            raise AssignmentGenerationError(
                f"{suite} observation counts differ from manifest"
            )
        if counts["test"] != 0:
            raise AssignmentGenerationError("test observation payload detected")

    manifest_by_pair: dict[str, dict[str, IdentityManifestRow]] = {}
    for row in rows:
        manifest_by_pair.setdefault(row.pair_id, {})[row.suite] = row
    shared_channel_pairs = 0
    for pair_id, pair_rows in manifest_by_pair.items():
        c1 = observation_loaders["C1"].load(pair_rows["C1"].run_id)
        structural = observation_loaders["S"].load(pair_rows["S"].run_id)
        if not shared_channels_equal(c1, structural):
            raise AssignmentGenerationError(
                f"{pair_id} C1/S shared-channel equality failed"
            )
        shared_channel_pairs += 1

    plant_rows = {
        row.run_id: row
        for row in read_role_index(root / "plant" / "index.csv", observation=False)
    }
    byte_identical_plant_pairs = 0
    for pair_id, pair_rows in manifest_by_pair.items():
        hashes = {
            plant_rows[pair_rows[suite].run_id].sha256
            for suite in expected_suites
        }
        if len(hashes) != 1:
            raise AssignmentGenerationError(
                f"{pair_id} suite plant payload hashes are not identical"
            )
        byte_identical_plant_pairs += 1

    return {
        "status": (
            "partial_base_dataset_audit_pass"
            if allow_partial
            else "complete_primary_c1_s_base_dataset_audit_pass"
        ),
        "assignment_hash": binding.assignment_hash,
        "config_hash": binding.config.config_hash,
        "identity_audit": identity_audit,
        "manifest_audit": manifest_audit,
        "mechanics_preflight": mechanics_preflight,
        "plant_payloads": plant_count,
        "label_payloads": label_count,
        "observation_counts_by_suite": observation_counts,
        "shared_channel_pairs": shared_channel_pairs,
        "byte_identical_plant_pairs": byte_identical_plant_pairs,
        "test_identity_or_payload_rows": 0,
    }
