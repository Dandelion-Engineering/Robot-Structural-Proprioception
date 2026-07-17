"""Sensor-realism and fault-injection model (schema section C, Claude's lane).

Maps a privileged plant record (schema B) to one deployable suite's observed
record (schema C) by applying, per channel, the sensor pathologies a real onboard
suite would suffer, and by injecting *sensor-class* faults into the observation
path only. Structural and actuator faults live in the plant lane and reach this
model only through the privileged state it reads.

Design commitments (each traceable to the schema):
  * Leakage boundary in code: the model reads only `observable_sources(record)`,
    so no privileged-only field can enter an observation (schema invariant 1).
  * Suites differ only by available channels: unavailable channels are written as
    all-NaN and masked off (schema invariant 2).
  * Actuator fault stays hidden from C1: the current proxy is built from
    `control_effort` (upstream of the gain loss), never `tau_delivered_true`.
  * Common random numbers: every channel/stream draws from its own independent
    generator keyed by `(sensor_seed, pair_id, channel, stream)` (schema A [C4]),
    so adding the S-only gauge channels cannot perturb the shared-channel draws.
  * Sensor-fault relational signature: an encoder fault corrupts `q_obs` only; it
    does not touch the gauge/IMU histories, which continue to reflect true
    (undeformed-by-the-lie) physical state (schema C fault-injection boundary).

Pathology parameters live in `SensorConfig`; the load-bearing ones (gauge noise
floor ~1 microstrain, thermal apparent strain ~10 microstrain/degC) are grounded
in the project's references ledger (Barrias 2016; Silveira 2021). Their frozen
numeric values will be pinned in the shared `config.json` before confirmatory
generation.
"""

from __future__ import annotations

from dataclasses import dataclass

import numpy as np

from utils.rng import channel_generator
from utils.schema_types import (
    CHANNEL_WIDTH,
    IMU_DIM,
    N_GAUGES,
    N_JOINTS,
    OBSERVED_CHANNELS,
    SUITE_CHANNELS,
    ObservableSources,
    ObservedRecord,
    PrivilegedRecord,
    SCHEMA_VERSION,
    observable_sources,
)

# Sensor-class fault subtypes this model injects into the observation path.
SENSOR_FAULT_SUBTYPES: frozenset[str] = frozenset(
    {"encoder_bias", "encoder_drift", "encoder_dropout"}
)
SOURCE_CLASSES: frozenset[str] = frozenset({"healthy", "structure", "actuator", "sensor"})


@dataclass(frozen=True)
class FaultSpec:
    """Shared fault-library entry (schema D labels are derived from this).

    Covers all four source classes so the library is one object across lanes;
    this model only *applies* `source_class == "sensor"` faults (structure and
    actuator faults are realized by the plant lane and arrive via the privileged
    record). `location` is a joint index for sensor/actuator faults, a segment
    index for structural faults, or -1 when not applicable. `severity` units are
    subtype-specific: rad (encoder_bias), rad/s (encoder_drift), added dropout
    probability (encoder_dropout).
    """

    source_class: str = "healthy"
    subtype: str = "none"
    location: int = -1
    severity: float = 0.0
    onset_index: int = -1  # first affected control step; -1 = healthy / no onset
    compound_flag: bool = False
    ood_flag: bool = False

    def validate(self) -> None:
        """Fail loudly on an ill-formed fault spec."""

        if self.source_class not in SOURCE_CLASSES:
            raise ValueError(f"unknown source_class: {self.source_class!r}")
        if self.source_class == "sensor" and self.subtype not in SENSOR_FAULT_SUBTYPES:
            raise ValueError(
                f"sensor fault subtype {self.subtype!r} not in {sorted(SENSOR_FAULT_SUBTYPES)}"
            )
        if self.source_class == "sensor" and not 0 <= self.location < N_JOINTS:
            raise ValueError(f"sensor fault location {self.location} out of joint range")


@dataclass(frozen=True)
class SensorConfig:
    """Numeric sensor-pathology parameters (frozen into `config.json` later).

    Defaults are plausible engineering values; the two load-bearing ones
    (`gauge_noise_microstrain`, `thermal_microstrain_per_c`) come from the
    references ledger and must not be idealized away (they are what make the
    structural channel's advantage an honest test rather than a manufactured win).
    """

    # Encoder (joint angle)
    encoder_noise_rad: float = 3.0e-4  # ~0.3 mrad RMS
    encoder_quant_rad: float = 2.0 * np.pi / (2 ** 14)  # 14-bit absolute encoder
    encoder_latency_s: float = 0.0
    # Motor-current proxy (estimate of control_effort)
    current_noise_floor_nm: float = 1.0e-3
    current_noise_frac: float = 0.02  # fraction of |control_effort|
    current_bias_nm: float = 2.0e-3
    current_latency_s: float = 0.0
    # Distal IMU
    imu_accel_noise: float = 2.0e-2  # m/s^2 RMS
    imu_gyro_noise: float = 2.0e-3  # rad/s RMS
    imu_accel_bias: float = 1.0e-2
    imu_gyro_bias: float = 1.0e-3
    imu_latency_s: float = 0.0
    # Surface-strain gauges (FBG-scale)
    gauge_noise_microstrain: float = 1.0  # FBG resolution floor (Barrias 2016)
    thermal_microstrain_per_c: float = 10.0  # apparent strain (Silveira 2021)
    reference_temperature_c: float = 25.0
    gauge_bias_microstrain: float = 0.5
    gauge_drift_microstrain_per_rt_s: float = 0.2  # random-walk rate (per sqrt(s))
    gauge_hysteresis_alpha: float = 0.15  # first-order lag coefficient in [0,1)
    gauge_quant_microstrain: float = 0.5
    gauge_latency_s: float = 2.0e-3
    # Baseline dropout probability applied to every measured channel
    dropout_prob: float = 0.01

    def channel_latency_s(self, channel: str) -> float:
        """Return the delivery latency for a registry channel (seconds)."""

        return {
            "q_obs": self.encoder_latency_s,
            "qd_obs": self.encoder_latency_s,
            "tau_cmd": 0.0,
            "current_proxy_obs": self.current_latency_s,
            "imu_obs": self.imu_latency_s,
            "gauge_obs": self.gauge_latency_s,
        }[channel]


# --------------------------------------------------------------------------- #
# Pure pathology helpers (each one causal and single-purpose).
# --------------------------------------------------------------------------- #
def quantize(signal: np.ndarray, step: float) -> np.ndarray:
    """Round `signal` to the nearest multiple of `step` (ADC/interrogator quantization)."""

    if step <= 0.0:
        return signal
    return np.round(signal / step) * step


def first_order_lag(signal: np.ndarray, alpha: float) -> np.ndarray:
    """Causal first-order IIR low-pass emulating gauge hysteresis/creep.

    ``y[0] = x[0]``; ``y[t] = alpha*y[t-1] + (1-alpha)*x[t]``. Larger `alpha` means
    more lag. Past-only dependence keeps the pathology causal. Vectorized across
    columns; O(T) over time.
    """

    if not 0.0 <= alpha < 1.0:
        raise ValueError(f"hysteresis alpha must be in [0, 1), got {alpha}")
    lagged = np.empty_like(signal)
    lagged[0] = signal[0]
    for step_index in range(1, signal.shape[0]):
        lagged[step_index] = alpha * lagged[step_index - 1] + (1.0 - alpha) * signal[step_index]
    return lagged


def random_walk(generator: np.random.Generator, shape: tuple[int, ...], rate_per_rt_s: float,
                dt: float) -> np.ndarray:
    """Return a zero-start random-walk drift of `shape` over the control grid.

    Step standard deviation is ``rate_per_rt_s * sqrt(dt)`` so the walk's variance
    grows linearly in time regardless of the control rate.
    """

    if rate_per_rt_s <= 0.0:
        return np.zeros(shape)
    increments = generator.normal(0.0, rate_per_rt_s * np.sqrt(dt), size=shape)
    increments[0] = 0.0
    return np.cumsum(increments, axis=0)


def causal_derivative(signal: np.ndarray, t_s: np.ndarray) -> np.ndarray:
    """Backward-difference time derivative (past-only, schema D causality).

    The first sample has no past, so its derivative is 0 rather than a future-using
    centered estimate.
    """

    derivative = np.zeros_like(signal)
    dt = np.diff(t_s)[:, None]
    derivative[1:] = np.diff(signal, axis=0) / dt
    return derivative


def validity_from_dropout(generator: np.random.Generator, prob: np.ndarray) -> np.ndarray:
    """Return a boolean valid mask (True = kept) given a per-element dropout prob array."""

    return generator.random(prob.shape) >= prob


class SensorModel:
    """Map privileged plant state to one suite's observed record (schema C)."""

    def __init__(self, config: SensorConfig | None = None) -> None:
        """Store the pathology configuration (defaults if none supplied)."""

        self.config = config or SensorConfig()

    def observe(
        self,
        record: PrivilegedRecord,
        suite: str,
        *,
        pair_id: int | str,
        sensor_seed: int,
        fault: FaultSpec | None = None,
        run_id: str = "run",
        config_hash: str = "",
        split: str | None = None,
    ) -> ObservedRecord:
        """Produce the observed record for `suite` from a privileged rollout.

        Args:
            record: the privileged plant trace (schema B); only its observable
                sources are read.
            suite: one of ``C0`` / ``C1`` / ``S`` (``O`` is the separate oracle).
            pair_id: matched-comparison id (shared across the C1/S pair).
            sensor_seed: sensor seed (shared across the C1/S pair) for CRN.
            fault: the active fault; only ``source_class == "sensor"`` faults are
                applied here.
            run_id/config_hash/split: provenance carried into the observed record.
        """

        if suite not in SUITE_CHANNELS:
            raise ValueError(f"suite must be one of {sorted(SUITE_CHANNELS)}; got {suite!r}")
        fault = fault or FaultSpec()
        fault.validate()
        sources = observable_sources(record)  # the ONLY doorway from privileged truth
        available = SUITE_CHANNELS[suite]

        measured = self._build_measured_channels(sources, fault, pair_id, sensor_seed)

        values: dict[str, np.ndarray] = {}
        valid_mask: dict[str, np.ndarray] = {}
        measurement_time_s: dict[str, np.ndarray] = {}
        availability_time_s: dict[str, np.ndarray] = {}
        latency_age_s: dict[str, np.ndarray] = {}
        suite_available_mask: dict[str, bool] = {}
        n_steps = sources.t_s.shape[0]

        for name, width in OBSERVED_CHANNELS:
            present = name in available
            suite_available_mask[name] = present
            if present:
                channel_values, channel_valid = measured[name]
                latency = self.config.channel_latency_s(name)
                values[name] = channel_values
                valid_mask[name] = channel_valid
                measurement_time_s[name] = sources.t_s.copy()
                latency_age_s[name] = np.full(n_steps, latency)
                availability_time_s[name] = sources.t_s + latency
            else:
                # Channel absent in this suite: all-NaN, masked off (invariant 2).
                values[name] = np.full((n_steps, width), np.nan)
                valid_mask[name] = np.zeros((n_steps, width), dtype=bool)
                measurement_time_s[name] = np.full(n_steps, np.nan)
                latency_age_s[name] = np.full(n_steps, np.nan)
                availability_time_s[name] = np.full(n_steps, np.nan)

        return ObservedRecord(
            suite=suite,
            run_id=str(run_id),
            pair_id=str(pair_id),
            config_hash=config_hash,
            values=values,
            valid_mask=valid_mask,
            measurement_time_s=measurement_time_s,
            availability_time_s=availability_time_s,
            latency_age_s=latency_age_s,
            suite_available_mask=suite_available_mask,
            schema_version=SCHEMA_VERSION,
            split=split,
        )

    # ----------------------------------------------------------------------- #
    # Per-channel construction. Each measured channel is (values, valid_mask).
    # ----------------------------------------------------------------------- #
    def _build_measured_channels(
        self,
        sources: ObservableSources,
        fault: FaultSpec,
        pair_id: int | str,
        sensor_seed: int,
    ) -> dict[str, tuple[np.ndarray, np.ndarray]]:
        """Build every measurable channel; downstream masks decide suite membership."""

        cfg = self.config
        t_s = sources.t_s
        n_steps = t_s.shape[0]
        dt = float(np.median(np.diff(t_s))) if n_steps > 1 else 1.0

        q_obs, q_valid = self._encoder_channel(sources, fault, pair_id, sensor_seed, dt)
        qd_obs = causal_derivative(q_obs, t_s)
        # qd validity inherits q validity (it is derived, not independently sampled).
        qd_valid = q_valid.copy()

        tau_cmd = sources.tau_cmd.copy()  # known command; passes through cleanly
        tau_valid = np.ones((n_steps, N_JOINTS), dtype=bool)

        current = self._current_proxy_channel(sources, pair_id, sensor_seed)
        current_valid = self._dropout_only(pair_id, sensor_seed, "current_proxy_obs", (n_steps, N_JOINTS))
        current = np.where(current_valid, current, np.nan)

        imu = self._imu_channel(sources, pair_id, sensor_seed)
        imu_valid = self._dropout_only(pair_id, sensor_seed, "imu_obs", (n_steps, IMU_DIM))
        imu = np.where(imu_valid, imu, np.nan)

        gauge = self._gauge_channel(sources, pair_id, sensor_seed, dt)
        gauge_valid = self._dropout_only(pair_id, sensor_seed, "gauge_obs", (n_steps, N_GAUGES))
        gauge = np.where(gauge_valid, gauge, np.nan)

        return {
            "q_obs": (q_obs, q_valid),
            "qd_obs": (qd_obs, qd_valid),
            "tau_cmd": (tau_cmd, tau_valid),
            "current_proxy_obs": (current, current_valid),
            "imu_obs": (imu, imu_valid),
            "gauge_obs": (gauge, gauge_valid),
        }

    def _encoder_channel(
        self,
        sources: ObservableSources,
        fault: FaultSpec,
        pair_id: int | str,
        sensor_seed: int,
        dt: float,
    ) -> tuple[np.ndarray, np.ndarray]:
        """Corrupted encoder: noise + optional sensor fault + quantization + dropout."""

        cfg = self.config
        n_steps = sources.t_s.shape[0]
        shape = (n_steps, N_JOINTS)
        noise = channel_generator(sensor_seed, pair_id, "q_obs", "value").normal(
            0.0, cfg.encoder_noise_rad, size=shape
        )
        q_obs = sources.q_true + noise

        dropout_prob = np.full(shape, cfg.dropout_prob)
        if fault.source_class == "sensor":
            q_obs, dropout_prob = self._apply_encoder_fault(
                q_obs, dropout_prob, fault, sources.t_s, sensor_seed, pair_id
            )

        q_obs = quantize(q_obs, cfg.encoder_quant_rad)
        valid = validity_from_dropout(
            channel_generator(sensor_seed, pair_id, "q_obs", "dropout"), dropout_prob
        )
        q_obs = np.where(valid, q_obs, np.nan)
        return q_obs, valid

    def _apply_encoder_fault(
        self,
        q_obs: np.ndarray,
        dropout_prob: np.ndarray,
        fault: FaultSpec,
        t_s: np.ndarray,
        sensor_seed: int,
        pair_id: int | str,
    ) -> tuple[np.ndarray, np.ndarray]:
        """Inject an encoder fault into the observation path only (schema C boundary).

        The gauge/IMU/physical histories are untouched, so the fault is identified
        by a *disagreement* between the corrupted encoder and the independently
        evolved physical channels — the project's analytical-redundancy mechanism.
        """

        onset = fault.onset_index if fault.onset_index >= 0 else 0
        joint = fault.location
        active = np.zeros(t_s.shape[0], dtype=bool)
        active[onset:] = True
        if fault.subtype == "encoder_bias":
            q_obs[active, joint] += fault.severity
        elif fault.subtype == "encoder_drift":
            elapsed = np.clip(t_s - t_s[onset], 0.0, None)
            q_obs[active, joint] += fault.severity * elapsed[active]
        elif fault.subtype == "encoder_dropout":
            dropout_prob[active, joint] = np.clip(dropout_prob[active, joint] + fault.severity, 0.0, 1.0)
        return q_obs, dropout_prob

    def _current_proxy_channel(
        self, sources: ObservableSources, pair_id: int | str, sensor_seed: int
    ) -> np.ndarray:
        """Nominal-Kt noisy current proxy of `control_effort` (upstream of gain loss)."""

        cfg = self.config
        effort = sources.control_effort
        std = cfg.current_noise_floor_nm + cfg.current_noise_frac * np.abs(effort)
        noise = channel_generator(sensor_seed, pair_id, "current_proxy_obs", "value").normal(
            0.0, std
        )
        bias = channel_generator(sensor_seed, pair_id, "current_proxy_obs", "bias").normal(
            0.0, cfg.current_bias_nm, size=(N_JOINTS,)
        )
        return effort + noise + bias

    def _imu_channel(
        self, sources: ObservableSources, pair_id: int | str, sensor_seed: int
    ) -> np.ndarray:
        """Distal IMU: per-axis additive noise + constant bias on accel/gyro."""

        cfg = self.config
        std = np.concatenate(
            (np.full(3, cfg.imu_accel_noise), np.full(3, cfg.imu_gyro_noise))
        )
        noise = channel_generator(sensor_seed, pair_id, "imu_obs", "value").normal(
            0.0, std, size=(sources.t_s.shape[0], IMU_DIM)
        )
        bias_std = np.concatenate(
            (np.full(3, cfg.imu_accel_bias), np.full(3, cfg.imu_gyro_bias))
        )
        bias = channel_generator(sensor_seed, pair_id, "imu_obs", "bias").normal(0.0, bias_std)
        return sources.imu_true + noise + bias

    def _gauge_channel(
        self, sources: ObservableSources, pair_id: int | str, sensor_seed: int, dt: float
    ) -> np.ndarray:
        """Surface strain: hysteresis(strain) + thermal apparent strain + bias + drift + noise + quant."""

        cfg = self.config
        shape = (sources.t_s.shape[0], N_GAUGES)
        strain_response = first_order_lag(sources.gauge_true, cfg.gauge_hysteresis_alpha)
        thermal = cfg.thermal_microstrain_per_c * (
            sources.temperature_true - cfg.reference_temperature_c
        )
        bias = channel_generator(sensor_seed, pair_id, "gauge_obs", "bias").normal(
            0.0, cfg.gauge_bias_microstrain, size=(N_GAUGES,)
        )
        drift = random_walk(
            channel_generator(sensor_seed, pair_id, "gauge_obs", "drift"),
            shape,
            cfg.gauge_drift_microstrain_per_rt_s,
            dt,
        )
        noise = channel_generator(sensor_seed, pair_id, "gauge_obs", "value").normal(
            0.0, cfg.gauge_noise_microstrain, size=shape
        )
        gauge = strain_response + thermal + bias + drift + noise
        return quantize(gauge, cfg.gauge_quant_microstrain)

    def _dropout_only(
        self, pair_id: int | str, sensor_seed: int, channel: str, shape: tuple[int, int]
    ) -> np.ndarray:
        """Baseline (fault-free) dropout mask for a channel."""

        prob = np.full(shape, self.config.dropout_prob)
        return validity_from_dropout(
            channel_generator(sensor_seed, pair_id, channel, "dropout"), prob
        )
