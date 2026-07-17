"""Typed carriers for the shared `plant -> signals -> estimator` data schema (v1.0).

This module renders the schema contract in `../schema/schema-v1.0.md` into Python
dataclasses so both Phase-2 lanes build against the same field names, shapes, and
units. It is deliberately dependency-light (NumPy + stdlib) per the schema's
portability invariant.

Roles (schema section 0):
  * `PrivilegedRecord` / `PlantStepState` -> section B (plant lane, Codex): the
    privileged ground-truth trace / its per-step slice. NON-deployable.
  * `ObservedRecord` -> section C (sensor lane, Claude): one deployable suite's
    corrupted observations, with the full fixed channel registry, per-channel
    validity masks, and measurement/availability timing.

The privileged/observed boundary is physical (schema invariant 1): the sensor
model reads only the observable-source subset of a `PrivilegedRecord` (see
`observable_sources`), so a privileged-only field can never be copied into an
`ObservedRecord` by construction.

NOTE ON SHARED OWNERSHIP: `PrivilegedRecord`/`PlantStepState` describe the plant
lane's output (Codex). They are proposed here as the concrete rendering of
schema section B for the shared interface; the plant lane is the authority on
its own producer struct and may refine field names/shapes through the amendment
protocol. `ObservedRecord` is the sensor lane's output (Claude).
"""

from __future__ import annotations

from dataclasses import dataclass, fields
from pathlib import Path
from typing import Mapping

import numpy as np

SCHEMA_VERSION = "1.0"

# --- Fixed dimensions from the committed plant (Slot 1; frozen by the spike) ---
N_JOINTS = 2  # planar two-link arm
N_GAUGES = 4  # two stations per link at 0.25 L and 0.75 L
IMU_DIM = 6  # distal-link specific force (3) + angular rate (3)
DEFAULT_N_DEF = 90  # spike-frozen: 3-vector log-map rot for 15 internal ball joints x 2 links

# --- Observed channel registry (schema section C), fixed width, fixed order ---
# Every deployable suite writes this full registry; unavailable channels are NaN.
OBSERVED_CHANNELS: tuple[tuple[str, int], ...] = (
    ("q_obs", N_JOINTS),  # corrupted encoder joint angle (rad)
    ("qd_obs", N_JOINTS),  # causally derived joint velocity (rad/s)
    ("tau_cmd", N_JOINTS),  # commanded (pre-limit) joint torque (N*m)
    ("current_proxy_obs", N_JOINTS),  # nominal-Kt noisy current estimate of control_effort (N*m)
    ("imu_obs", IMU_DIM),  # distal-link IMU (m/s^2 x3, rad/s x3)
    ("gauge_obs", N_GAUGES),  # signed surface bending strain (microstrain)
)
CHANNEL_WIDTH: dict[str, int] = {name: width for name, width in OBSERVED_CHANNELS}
CHANNEL_NAMES: tuple[str, ...] = tuple(name for name, _ in OBSERVED_CHANNELS)

# --- Suite -> available channels (schema invariant 2: C0 subset C1 subset S) ---
SUITE_CHANNELS: dict[str, tuple[str, ...]] = {
    "C0": ("q_obs", "qd_obs", "tau_cmd"),
    "C1": ("q_obs", "qd_obs", "tau_cmd", "current_proxy_obs", "imu_obs"),
    "S": ("q_obs", "qd_obs", "tau_cmd", "current_proxy_obs", "imu_obs", "gauge_obs"),
}
DEPLOYABLE_SUITES: tuple[str, ...] = ("C0", "C1", "S")
# "O" is a separate allowlisted oracle interface (schema section D), never built here.


def observed_registry_width() -> int:
    """Return the total scalar width of the fixed observed channel registry."""

    return sum(CHANNEL_WIDTH[name] for name in CHANNEL_NAMES)


@dataclass
class PrivilegedRecord:
    """Privileged plant ground-truth trace on the fixed control grid (schema B).

    One per `run_id`. All arrays share leading axis `T` (control steps). This is
    NON-deployable: only the metric builder, label builder, and oracle interface
    may read it. The sensor model consumes only `observable_sources(self)`.

    Shapes/units follow schema section B exactly. `n_def`, `n_contact`, and
    `n_safety` are model-defined widths carried for completeness.
    """

    step: np.ndarray  # [T] int, 0-based control step
    t_s: np.ndarray  # [T] s, time on the control grid
    q_true: np.ndarray  # [T,2] rad
    qd_true: np.ndarray  # [T,2] rad/s
    qdd_true: np.ndarray  # [T,2] rad/s^2
    tau_cmd: np.ndarray  # [T,2] N*m, controller request before actuator limiting
    tau_delivered_true: np.ndarray  # [T,2] N*m, post-fault delivered (actuator fault applied here)
    deform_coords: np.ndarray  # [T,n_def] independent deformation DOFs
    curvature_true: np.ndarray  # [T,4] 1/m at the four stations
    gauge_true: np.ndarray  # [T,4] microstrain, ideal signed surface bending strain
    imu_true: np.ndarray  # [T,6] distal-link specific force + angular rate
    temperature_true: np.ndarray  # [T,4] deg C at the four gauge stations
    contact_state: np.ndarray  # [T,n_contact] N/flag
    task_reference: np.ndarray  # [T,2] m, commanded task-space endpoint
    true_task_output: np.ndarray  # [T,2] m, true deformed tip position
    tracking_error: np.ndarray  # [T,2] m
    tracking_error_norm: np.ndarray  # [T] m
    control_effort: np.ndarray  # [T,2] N*m, saturated actuator-side effort, pre gain-loss
    saturation_flag: np.ndarray  # [T,2] bool
    safety_flag: np.ndarray  # [T,n_safety] bool

    @property
    def n_steps(self) -> int:
        """Number of control steps in the rollout."""

        return int(self.t_s.shape[0])

    @property
    def n_def(self) -> int:
        """Number of independent deformation coordinates in this record."""

        return int(self.deform_coords.shape[1])

    def validate(self) -> None:
        """Fail loudly if any array violates the schema-B shape/units contract."""

        t = self.n_steps
        expected = {
            "step": (t,),
            "t_s": (t,),
            "q_true": (t, N_JOINTS),
            "qd_true": (t, N_JOINTS),
            "qdd_true": (t, N_JOINTS),
            "tau_cmd": (t, N_JOINTS),
            "tau_delivered_true": (t, N_JOINTS),
            "curvature_true": (t, N_GAUGES),
            "gauge_true": (t, N_GAUGES),
            "imu_true": (t, IMU_DIM),
            "temperature_true": (t, N_GAUGES),
            "task_reference": (t, 2),
            "true_task_output": (t, 2),
            "tracking_error": (t, 2),
            "tracking_error_norm": (t,),
            "control_effort": (t, N_JOINTS),
            "saturation_flag": (t, N_JOINTS),
        }
        for name, shape in expected.items():
            arr = getattr(self, name)
            if arr.shape != shape:
                raise ValueError(
                    f"PrivilegedRecord.{name} has shape {arr.shape}, expected {shape}"
                )
        if self.deform_coords.shape[0] != t:
            raise ValueError("PrivilegedRecord.deform_coords leading axis must be T")
        for name in ("t_s", "q_true", "gauge_true", "imu_true", "temperature_true", "control_effort"):
            arr = getattr(self, name)
            if not np.all(np.isfinite(arr)):
                raise ValueError(f"PrivilegedRecord.{name} contains non-finite values")

    def slice_step(self, index: int) -> "PlantStepState":
        """Return the single-control-step privileged slice for the online loop (schema 0)."""

        return PlantStepState(
            step=int(self.step[index]),
            t_s=float(self.t_s[index]),
            q_true=self.q_true[index].copy(),
            qd_true=self.qd_true[index].copy(),
            tau_cmd=self.tau_cmd[index].copy(),
            control_effort=self.control_effort[index].copy(),
            tau_delivered_true=self.tau_delivered_true[index].copy(),
            gauge_true=self.gauge_true[index].copy(),
            imu_true=self.imu_true[index].copy(),
            temperature_true=self.temperature_true[index].copy(),
        )

    def save_npz(self, path: Path) -> None:
        """Persist the full privileged trace as one non-pickled `.npz` (schema E).

        This is a proposed on-disk rendering of the plant lane's `plant/` role
        payload; the plant lane owns the authoritative producer and may refine it.
        """

        path = Path(path)
        path.parent.mkdir(parents=True, exist_ok=True)
        np.savez(path, **{f.name: np.asarray(getattr(self, f.name)) for f in fields(self)})

    @classmethod
    def load_npz(cls, path: Path) -> "PrivilegedRecord":
        """Load a privileged trace from disk without allowing pickled objects."""

        with np.load(Path(path), allow_pickle=False) as data:
            return cls(**{f.name: np.asarray(data[f.name]) for f in fields(cls)})


@dataclass(frozen=True)
class PlantStepState:
    """Per-control-step privileged slice the plant lane hands to the sensor interface.

    Schema section 0: the plant advances one control step and exposes the current
    privileged state; the sensor model maps it to the suite's observations. This
    is the in-memory handoff object (proposed name `PlantStepState`, agreed at the
    Phase-2 kickoff). Only the observable-source fields (`q_true`, `tau_cmd`,
    `control_effort`, `imu_true`, `gauge_true`, `temperature_true`) are read by the
    sensor lane; `tau_delivered_true`/`qd_true` are carried for the metric/oracle
    path, not for observation.
    """

    step: int
    t_s: float
    q_true: np.ndarray  # [2]
    qd_true: np.ndarray  # [2]
    tau_cmd: np.ndarray  # [2]
    control_effort: np.ndarray  # [2]
    tau_delivered_true: np.ndarray  # [2]
    gauge_true: np.ndarray  # [4]
    imu_true: np.ndarray  # [6]
    temperature_true: np.ndarray  # [4]


@dataclass(frozen=True)
class ObservableSources:
    """The strict subset of privileged state the sensor model is allowed to read.

    Extracting this (via `observable_sources`) makes the schema's leakage boundary
    a code-level property: no privileged-only field (`tau_delivered_true`,
    `deform_coords`, `curvature_true`, labels, task truth) is reachable from here,
    so it cannot be copied into an `ObservedRecord`.
    """

    t_s: np.ndarray  # [T]
    q_true: np.ndarray  # [T,2]
    tau_cmd: np.ndarray  # [T,2]
    control_effort: np.ndarray  # [T,2] (current proxy is taken here, UPSTREAM of gain loss)
    imu_true: np.ndarray  # [T,6]
    gauge_true: np.ndarray  # [T,4]
    temperature_true: np.ndarray  # [T,4]


def observable_sources(record: PrivilegedRecord) -> ObservableSources:
    """Return only the privileged fields a real onboard sensor could measure.

    This is the single doorway from privileged truth to the sensor lane. Note
    `control_effort` (not `tau_delivered_true`) feeds the current proxy, so the
    actuator-gain fault stays invisible to C1 as a direct torque signal (schema C).
    """

    return ObservableSources(
        t_s=record.t_s,
        q_true=record.q_true,
        tau_cmd=record.tau_cmd,
        control_effort=record.control_effort,
        imu_true=record.imu_true,
        gauge_true=record.gauge_true,
        temperature_true=record.temperature_true,
    )


@dataclass
class ObservedRecord:
    """One deployable suite's observed trace (schema section C), one per `run_id`.

    Carries the full fixed channel registry; channels not in the suite are stored
    as all-NaN and marked off in `suite_available_mask`. `valid_mask` carries
    per-time, per-column dropout/validity; `measurement_time_s`/`availability_time_s`/
    `latency_age_s` preserve asynchronous/latent delivery so downstream causal
    windowing can enforce `availability_time <= decision_time` (schema D).
    """

    suite: str
    run_id: str
    pair_id: str
    config_hash: str
    values: dict[str, np.ndarray]  # channel -> [T, width], NaN where unavailable/invalid
    valid_mask: dict[str, np.ndarray]  # channel -> [T, width] bool
    measurement_time_s: dict[str, np.ndarray]  # channel -> [T]
    availability_time_s: dict[str, np.ndarray]  # channel -> [T]
    latency_age_s: dict[str, np.ndarray]  # channel -> [T]
    suite_available_mask: dict[str, bool]  # channel -> present in this suite
    schema_version: str = SCHEMA_VERSION
    split: str | None = None

    @property
    def n_steps(self) -> int:
        """Number of control steps in the observed trace."""

        return int(self.values["q_obs"].shape[0])

    @property
    def available_channels(self) -> tuple[str, ...]:
        """Channels physically present (unmasked) in this suite."""

        return tuple(name for name in CHANNEL_NAMES if self.suite_available_mask[name])

    def to_npz_dict(self) -> dict[str, np.ndarray]:
        """Flatten to a numeric/unicode-only dict for `np.savez` (allow_pickle-free)."""

        out: dict[str, np.ndarray] = {
            "schema_version": np.asarray(self.schema_version),
            "suite": np.asarray(self.suite),
            "run_id": np.asarray(str(self.run_id)),
            "pair_id": np.asarray(str(self.pair_id)),
            "config_hash": np.asarray(self.config_hash),
            "split": np.asarray(self.split if self.split is not None else ""),
            "channel_names": np.asarray(CHANNEL_NAMES),
            "suite_available_mask": np.asarray(
                [self.suite_available_mask[name] for name in CHANNEL_NAMES], dtype=bool
            ),
        }
        for name in CHANNEL_NAMES:
            out[f"values__{name}"] = self.values[name]
            out[f"valid__{name}"] = self.valid_mask[name]
            out[f"meas_time__{name}"] = self.measurement_time_s[name]
            out[f"avail_time__{name}"] = self.availability_time_s[name]
            out[f"latency__{name}"] = self.latency_age_s[name]
        return out

    def save_npz(self, path: Path) -> None:
        """Persist as one non-pickled `.npz` (schema section E storage rule)."""

        path = Path(path)
        path.parent.mkdir(parents=True, exist_ok=True)
        np.savez(path, **self.to_npz_dict())

    @classmethod
    def from_npz_dict(cls, data: Mapping[str, np.ndarray]) -> "ObservedRecord":
        """Reconstruct an `ObservedRecord` from a loaded npz mapping."""

        names = [str(name) for name in data["channel_names"]]
        mask = {name: bool(flag) for name, flag in zip(names, data["suite_available_mask"])}
        split_raw = str(data["split"])
        return cls(
            suite=str(data["suite"]),
            run_id=str(data["run_id"]),
            pair_id=str(data["pair_id"]),
            config_hash=str(data["config_hash"]),
            schema_version=str(data["schema_version"]),
            split=split_raw if split_raw else None,
            values={name: np.asarray(data[f"values__{name}"]) for name in names},
            valid_mask={name: np.asarray(data[f"valid__{name}"]) for name in names},
            measurement_time_s={name: np.asarray(data[f"meas_time__{name}"]) for name in names},
            availability_time_s={name: np.asarray(data[f"avail_time__{name}"]) for name in names},
            latency_age_s={name: np.asarray(data[f"latency__{name}"]) for name in names},
            suite_available_mask=mask,
        )

    @classmethod
    def load_npz(cls, path: Path) -> "ObservedRecord":
        """Load an `ObservedRecord` from disk without allowing pickled objects."""

        with np.load(Path(path), allow_pickle=False) as data:
            return cls.from_npz_dict({key: data[key] for key in data.files})
