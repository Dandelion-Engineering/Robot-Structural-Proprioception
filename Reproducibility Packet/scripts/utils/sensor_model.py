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
    FaultSpec,
    IMU_DIM,
    N_GAUGES,
    N_JOINTS,
    OBSERVED_CHANNELS,
    ObservableStepSources,
    SUITE_CHANNELS,
    ObservedRecord,
    PlantStepState,
    PrivilegedRecord,
    SCHEMA_VERSION,
    observable_step_sources,
)


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

    def validate(self) -> None:
        """Fail loudly on non-physical noise, timing, quantization, or dropout values."""

        non_negative = (
            "encoder_noise_rad",
            "encoder_quant_rad",
            "encoder_latency_s",
            "current_noise_floor_nm",
            "current_noise_frac",
            "current_bias_nm",
            "current_latency_s",
            "imu_accel_noise",
            "imu_gyro_noise",
            "imu_accel_bias",
            "imu_gyro_bias",
            "imu_latency_s",
            "gauge_noise_microstrain",
            "thermal_microstrain_per_c",
            "gauge_bias_microstrain",
            "gauge_drift_microstrain_per_rt_s",
            "gauge_quant_microstrain",
            "gauge_latency_s",
        )
        for name in non_negative:
            value = float(getattr(self, name))
            if not np.isfinite(value) or value < 0.0:
                raise ValueError(f"{name} must be finite and non-negative")
        if not 0.0 <= self.gauge_hysteresis_alpha < 1.0:
            raise ValueError("gauge_hysteresis_alpha must be in [0, 1)")
        if not 0.0 <= self.dropout_prob <= 1.0:
            raise ValueError("dropout_prob must be in [0, 1]")
        if not np.isfinite(self.reference_temperature_c):
            raise ValueError("reference_temperature_c must be finite")

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


@dataclass(frozen=True)
class ObservedStep:
    """One causal schema-C observation emitted during an online rollout."""

    step: int
    t_s: float
    suite: str
    values: dict[str, np.ndarray]
    valid_mask: dict[str, np.ndarray]
    measurement_time_s: dict[str, float]
    availability_time_s: dict[str, float]
    latency_age_s: dict[str, float]
    suite_available_mask: dict[str, bool]


class OnlineSensorSession:
    """Stateful one-control-step sensor path for a single deployable rollout.

    The session owns each CRN generator and every causal pathology state (previous
    encoder sample, gauge lag, and gauge drift). `observe_step` therefore consumes
    only the current `PlantStepState` and never replays a completed privileged trace.
    `to_record` stacks the emitted steps into the same role-separated `ObservedRecord`
    used by the persistence layer.
    """

    def __init__(
        self,
        suite: str,
        *,
        pair_id: int | str,
        sensor_seed: int,
        control_dt_s: float,
        config: SensorConfig | None = None,
        fault: FaultSpec | None = None,
        run_id: str = "run",
        config_hash: str = "",
        split: str | None = None,
    ) -> None:
        """Initialize one causal sensor rollout and its independent CRN substreams."""

        if suite not in SUITE_CHANNELS:
            raise ValueError(f"suite must be one of {sorted(SUITE_CHANNELS)}; got {suite!r}")
        if not np.isfinite(control_dt_s) or control_dt_s <= 0.0:
            raise ValueError("control_dt_s must be finite and positive")
        self.config = config or SensorConfig()
        self.config.validate()
        self.suite = suite
        self.pair_id = pair_id
        self.sensor_seed = int(sensor_seed)
        self.control_dt_s = float(control_dt_s)
        self.fault = fault or FaultSpec()
        self.fault.validate()
        self.run_id = str(run_id)
        self.config_hash = str(config_hash)
        self.split = split

        self._generators = {
            (channel, stream): channel_generator(self.sensor_seed, pair_id, channel, stream)
            for channel in ("q_obs", "current_proxy_obs", "imu_obs", "gauge_obs")
            for stream in ("value", "dropout")
        }
        self._generators[("current_proxy_obs", "bias")] = channel_generator(
            self.sensor_seed, pair_id, "current_proxy_obs", "bias"
        )
        self._generators[("imu_obs", "bias")] = channel_generator(
            self.sensor_seed, pair_id, "imu_obs", "bias"
        )
        self._generators[("gauge_obs", "bias")] = channel_generator(
            self.sensor_seed, pair_id, "gauge_obs", "bias"
        )
        self._generators[("gauge_obs", "drift")] = channel_generator(
            self.sensor_seed, pair_id, "gauge_obs", "drift"
        )

        cfg = self.config
        self._current_bias = self._generators[("current_proxy_obs", "bias")].normal(
            0.0, cfg.current_bias_nm, size=N_JOINTS
        )
        imu_bias_std = np.concatenate(
            (np.full(3, cfg.imu_accel_bias), np.full(3, cfg.imu_gyro_bias))
        )
        self._imu_bias = self._generators[("imu_obs", "bias")].normal(0.0, imu_bias_std)
        self._gauge_bias = self._generators[("gauge_obs", "bias")].normal(
            0.0, cfg.gauge_bias_microstrain, size=N_GAUGES
        )

        self._expected_step = 0
        self._previous_time_s: float | None = None
        self._previous_q_obs: np.ndarray | None = None
        self._previous_q_valid: np.ndarray | None = None
        self._sensor_fault_onset_time_s: float | None = None
        self._gauge_lag: np.ndarray | None = None
        self._gauge_drift = np.zeros(N_GAUGES, dtype=float)
        self._history: list[ObservedStep] = []

    def _generator(self, channel: str, stream: str) -> np.random.Generator:
        """Return one persistent per-channel CRN generator."""

        return self._generators[(channel, stream)]

    def _validate_sources(self, sources: ObservableStepSources) -> None:
        """Enforce sequential control-grid input and fixed schema-C source widths."""

        if sources.step != self._expected_step:
            raise ValueError(
                f"expected plant step {self._expected_step}, got {sources.step}"
            )
        if self._previous_time_s is not None and not np.isclose(
            sources.t_s - self._previous_time_s,
            self.control_dt_s,
            rtol=1.0e-7,
            atol=1.0e-12,
        ):
            raise ValueError("plant steps must arrive on the configured control grid")
        expected = (
            (sources.q_true, (N_JOINTS,), "q_true"),
            (sources.tau_cmd, (N_JOINTS,), "tau_cmd"),
            (sources.control_effort, (N_JOINTS,), "control_effort"),
            (sources.imu_true, (IMU_DIM,), "imu_true"),
            (sources.gauge_true, (N_GAUGES,), "gauge_true"),
            (sources.temperature_true, (N_GAUGES,), "temperature_true"),
        )
        if not np.isfinite(sources.t_s):
            raise ValueError("plant observation time must be finite")
        for value, shape, name in expected:
            if np.asarray(value).shape != shape or not np.all(np.isfinite(value)):
                raise ValueError(f"{name} must be a finite shape-{shape} vector")

    def _encoder(self, sources: ObservableStepSources) -> tuple[np.ndarray, np.ndarray]:
        """Emit corrupted encoder angle and its dropout mask for one step."""

        cfg = self.config
        q_obs = sources.q_true + self._generator("q_obs", "value").normal(
            0.0, cfg.encoder_noise_rad, size=N_JOINTS
        )
        dropout_prob = np.full(N_JOINTS, cfg.dropout_prob)
        onset = max(int(self.fault.onset_index), 0)
        if self.fault.source_class == "sensor" and sources.step >= onset:
            if self._sensor_fault_onset_time_s is None:
                self._sensor_fault_onset_time_s = sources.t_s
            joint = self.fault.location
            if self.fault.subtype == "encoder_bias":
                q_obs[joint] += self.fault.severity
            elif self.fault.subtype == "encoder_drift":
                elapsed = sources.t_s - self._sensor_fault_onset_time_s
                q_obs[joint] += self.fault.severity * elapsed
            elif self.fault.subtype == "encoder_dropout":
                dropout_prob[joint] = np.clip(
                    dropout_prob[joint] + self.fault.severity, 0.0, 1.0
                )
        q_obs = quantize(q_obs, cfg.encoder_quant_rad)
        valid = validity_from_dropout(
            self._generator("q_obs", "dropout"), dropout_prob
        )
        return np.where(valid, q_obs, np.nan), valid

    def _encoder_velocity(
        self, q_obs: np.ndarray, q_valid: np.ndarray, current_time_s: float
    ) -> tuple[np.ndarray, np.ndarray]:
        """Emit the past-only backward-difference encoder velocity."""

        if self._previous_q_obs is None:
            qd_obs = np.zeros(N_JOINTS, dtype=float)
            qd_valid = q_valid.copy()
        else:
            assert self._previous_q_valid is not None
            assert self._previous_time_s is not None
            qd_valid = q_valid & self._previous_q_valid
            qd_obs = (q_obs - self._previous_q_obs) / (
                current_time_s - self._previous_time_s
            )
        return np.where(qd_valid, qd_obs, np.nan), qd_valid

    def _current_proxy(self, sources: ObservableStepSources) -> tuple[np.ndarray, np.ndarray]:
        """Emit the upstream nominal-Kt current proxy and dropout mask."""

        cfg = self.config
        std = cfg.current_noise_floor_nm + cfg.current_noise_frac * np.abs(
            sources.control_effort
        )
        value = sources.control_effort + self._generator(
            "current_proxy_obs", "value"
        ).normal(0.0, std) + self._current_bias
        valid = validity_from_dropout(
            self._generator("current_proxy_obs", "dropout"),
            np.full(N_JOINTS, cfg.dropout_prob),
        )
        return np.where(valid, value, np.nan), valid

    def _imu(self, sources: ObservableStepSources) -> tuple[np.ndarray, np.ndarray]:
        """Emit the biased/noisy distal IMU and dropout mask."""

        cfg = self.config
        std = np.concatenate(
            (np.full(3, cfg.imu_accel_noise), np.full(3, cfg.imu_gyro_noise))
        )
        value = sources.imu_true + self._generator("imu_obs", "value").normal(
            0.0, std
        ) + self._imu_bias
        valid = validity_from_dropout(
            self._generator("imu_obs", "dropout"),
            np.full(IMU_DIM, cfg.dropout_prob),
        )
        return np.where(valid, value, np.nan), valid

    def _gauge(self, sources: ObservableStepSources) -> tuple[np.ndarray, np.ndarray]:
        """Emit causal lag/thermal/drift/noise gauge values and dropout mask."""

        cfg = self.config
        if self._gauge_lag is None:
            self._gauge_lag = sources.gauge_true.copy()
        else:
            self._gauge_lag = (
                cfg.gauge_hysteresis_alpha * self._gauge_lag
                + (1.0 - cfg.gauge_hysteresis_alpha) * sources.gauge_true
            )
        drift_increment = self._generator("gauge_obs", "drift").normal(
            0.0,
            cfg.gauge_drift_microstrain_per_rt_s * np.sqrt(self.control_dt_s),
            size=N_GAUGES,
        )
        if sources.step > 0:
            self._gauge_drift += drift_increment
        thermal = cfg.thermal_microstrain_per_c * (
            sources.temperature_true - cfg.reference_temperature_c
        )
        noise = self._generator("gauge_obs", "value").normal(
            0.0, cfg.gauge_noise_microstrain, size=N_GAUGES
        )
        value = quantize(
            self._gauge_lag + thermal + self._gauge_bias + self._gauge_drift + noise,
            cfg.gauge_quant_microstrain,
        )
        valid = validity_from_dropout(
            self._generator("gauge_obs", "dropout"),
            np.full(N_GAUGES, cfg.dropout_prob),
        )
        return np.where(valid, value, np.nan), valid

    def observe_step(self, state: PlantStepState) -> ObservedStep:
        """Map one current plant state to one causal observation and advance state."""

        sources = observable_step_sources(state)
        self._validate_sources(sources)
        q_obs, q_valid = self._encoder(sources)
        qd_obs, qd_valid = self._encoder_velocity(q_obs, q_valid, sources.t_s)
        current, current_valid = self._current_proxy(sources)
        imu, imu_valid = self._imu(sources)
        gauge, gauge_valid = self._gauge(sources)
        measured = {
            "q_obs": (q_obs, q_valid),
            "qd_obs": (qd_obs, qd_valid),
            "tau_cmd": (sources.tau_cmd.copy(), np.ones(N_JOINTS, dtype=bool)),
            "current_proxy_obs": (current, current_valid),
            "imu_obs": (imu, imu_valid),
            "gauge_obs": (gauge, gauge_valid),
        }

        values: dict[str, np.ndarray] = {}
        valid_mask: dict[str, np.ndarray] = {}
        measurement_time_s: dict[str, float] = {}
        availability_time_s: dict[str, float] = {}
        latency_age_s: dict[str, float] = {}
        suite_available_mask: dict[str, bool] = {}
        available = SUITE_CHANNELS[self.suite]
        for name, width in OBSERVED_CHANNELS:
            present = name in available
            suite_available_mask[name] = present
            if present:
                values[name], valid_mask[name] = measured[name]
                latency = self.config.channel_latency_s(name)
                measurement_time_s[name] = sources.t_s
                availability_time_s[name] = sources.t_s + latency
                latency_age_s[name] = latency
            else:
                values[name] = np.full(width, np.nan)
                valid_mask[name] = np.zeros(width, dtype=bool)
                measurement_time_s[name] = np.nan
                availability_time_s[name] = np.nan
                latency_age_s[name] = np.nan

        observed = ObservedStep(
            step=sources.step,
            t_s=sources.t_s,
            suite=self.suite,
            values=values,
            valid_mask=valid_mask,
            measurement_time_s=measurement_time_s,
            availability_time_s=availability_time_s,
            latency_age_s=latency_age_s,
            suite_available_mask=suite_available_mask,
        )
        self._history.append(observed)
        self._previous_q_obs = q_obs.copy()
        self._previous_q_valid = q_valid.copy()
        self._previous_time_s = sources.t_s
        self._expected_step += 1
        return observed

    def to_record(self, *, max_steps: int | None = None) -> ObservedRecord:
        """Stack emitted steps into a persisted record, optionally keeping a tail window."""

        if not self._history:
            raise ValueError("cannot build an ObservedRecord before any step is observed")
        if max_steps is not None and max_steps <= 0:
            raise ValueError("max_steps must be positive when provided")
        history = self._history if max_steps is None else self._history[-max_steps:]
        first = history[0]
        return ObservedRecord(
            suite=self.suite,
            run_id=self.run_id,
            pair_id=str(self.pair_id),
            config_hash=self.config_hash,
            values={
                name: np.stack([step.values[name] for step in history])
                for name, _ in OBSERVED_CHANNELS
            },
            valid_mask={
                name: np.stack([step.valid_mask[name] for step in history])
                for name, _ in OBSERVED_CHANNELS
            },
            measurement_time_s={
                name: np.asarray(
                    [step.measurement_time_s[name] for step in history], dtype=float
                )
                for name, _ in OBSERVED_CHANNELS
            },
            availability_time_s={
                name: np.asarray(
                    [step.availability_time_s[name] for step in history], dtype=float
                )
                for name, _ in OBSERVED_CHANNELS
            },
            latency_age_s={
                name: np.asarray(
                    [step.latency_age_s[name] for step in history], dtype=float
                )
                for name, _ in OBSERVED_CHANNELS
            },
            suite_available_mask=first.suite_available_mask.copy(),
            schema_version=SCHEMA_VERSION,
            split=self.split,
        )

    def available_record(
        self, decision_time_s: float, *, history_steps: int
    ) -> ObservedRecord | None:
        """Return history masked to values delivered by `decision_time_s`.

        The persisted record retains measured values plus their availability times;
        this controller-facing view keeps only the latest ``history_steps`` rows and
        masks any channel row whose latency has not elapsed. The explicit bound is the
        estimator's past-only `W` once frozen and avoids rebuilding an ever-growing
        history at 500 Hz. Returning ``None`` before the first plant step gives a
        policy an initialization state without inventing an observation.
        """

        if not np.isfinite(decision_time_s):
            raise ValueError("decision_time_s must be finite")
        if history_steps <= 0:
            raise ValueError("history_steps must be positive")
        if not self._history:
            return None
        record = self.to_record(max_steps=history_steps)
        values: dict[str, np.ndarray] = {}
        valid_mask: dict[str, np.ndarray] = {}
        for name, _ in OBSERVED_CHANNELS:
            availability = record.availability_time_s[name]
            delivered = np.isfinite(availability) & (availability <= decision_time_s + 1.0e-12)
            channel_valid = record.valid_mask[name] & delivered[:, None]
            valid_mask[name] = channel_valid
            values[name] = np.where(channel_valid, record.values[name], np.nan)
        return ObservedRecord(
            suite=record.suite,
            run_id=record.run_id,
            pair_id=record.pair_id,
            config_hash=record.config_hash,
            values=values,
            valid_mask=valid_mask,
            measurement_time_s={
                name: values.copy() for name, values in record.measurement_time_s.items()
            },
            availability_time_s={
                name: values.copy() for name, values in record.availability_time_s.items()
            },
            latency_age_s={
                name: values.copy() for name, values in record.latency_age_s.items()
            },
            suite_available_mask=record.suite_available_mask.copy(),
            schema_version=record.schema_version,
            split=record.split,
        )


class SensorModel:
    """Map privileged plant state to one suite's observed record (schema C)."""

    def __init__(self, config: SensorConfig | None = None) -> None:
        """Store the pathology configuration (defaults if none supplied)."""

        self.config = config or SensorConfig()
        self.config.validate()

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

        record.validate()
        if record.n_steps > 1:
            control_dt_s = float(np.median(np.diff(record.t_s)))
        else:
            control_dt_s = 1.0
        session = OnlineSensorSession(
            suite,
            pair_id=pair_id,
            sensor_seed=sensor_seed,
            control_dt_s=control_dt_s,
            config=self.config,
            fault=fault,
            run_id=run_id,
            config_hash=config_hash,
            split=split,
        )
        for index in range(record.n_steps):
            session.observe_step(record.slice_step(index))
        return session.to_record()
