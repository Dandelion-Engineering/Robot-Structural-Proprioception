"""Interpretable gain-scheduled recovery commands for the online policy seam.

The Claim Sheet requires a recovery path driven by the estimated fault distribution,
with an RMA-style control latent retained as the stronger comparison. This module is the
small, auditable floor: it preserves the nominal bounded task command while diagnosis is
healthy, ambiguous, unlocalized, or too uncertain; it applies only two explicit actions
when a source estimate is confident enough to support them:

* derate the task command after a localized-or-global structural diagnosis; and
* compensate an attributed actuator-gain loss by increasing the requested torque at the
  affected joint, within conservative controller and plant limits.

The defaults are development proposals, not frozen configuration. The module consumes
only schema-section-D ``EstimatorOutput`` values plus either the legacy time-indexed
nominal command or an explicitly supplied deployable nominal command. It therefore
plugs into ``EstimatorCommandPolicy`` and into observation-feedback task policies
without crossing the deployable/privileged boundary.
"""

from __future__ import annotations

from dataclasses import dataclass

import numpy as np

from utils.cable_mechanics import commanded_torque
from utils.estimator import EstimatorOutput, SOURCE_CLASS_ORDER
from utils.schema_types import N_JOINTS


STRUCTURE_INDEX = SOURCE_CLASS_ORDER.index("structure")
ACTUATOR_INDEX = SOURCE_CLASS_ORDER.index("actuator")


@dataclass(frozen=True)
class RecoveryControlConfig:
    """Development settings for the interpretable gain-scheduled controller.

    ``severity_out`` is interpreted as the remaining physical fraction for the known
    structure/actuator fault conventions (for example, 0.7 means 70% actuator gain
    remains). Active recovery is withheld when the estimator abstains, the source
    probability is below ``source_probability_threshold``, or the severity uncertainty
    exceeds ``maximum_severity_uncertainty``.
    """

    nominal_task_scale: float = 0.5
    source_probability_threshold: float = 0.5
    maximum_severity_uncertainty: float = 0.25
    structural_command_derate: float = 0.75
    minimum_gain_remaining: float = 0.25
    maximum_gain_compensation: float = 2.0
    torque_abs_limit: tuple[float, float] = (1.0, 0.5)

    def validate(self) -> None:
        """Fail loudly when a controller setting is non-physical or ambiguous."""

        finite_positive = {
            "maximum_severity_uncertainty": self.maximum_severity_uncertainty,
            "minimum_gain_remaining": self.minimum_gain_remaining,
            "maximum_gain_compensation": self.maximum_gain_compensation,
        }
        for name, value in finite_positive.items():
            if not np.isfinite(value) or value <= 0.0:
                raise ValueError(f"{name} must be finite and positive")
        if not np.isfinite(self.nominal_task_scale) or self.nominal_task_scale < 0.0:
            raise ValueError("nominal_task_scale must be finite and non-negative")
        if not 0.0 < self.source_probability_threshold <= 1.0:
            raise ValueError("source_probability_threshold must lie in (0, 1]")
        if not 0.0 < self.structural_command_derate <= 1.0:
            raise ValueError("structural_command_derate must lie in (0, 1]")
        if self.minimum_gain_remaining > 1.0:
            raise ValueError("minimum_gain_remaining must be <= 1")
        if self.maximum_gain_compensation < 1.0:
            raise ValueError("maximum_gain_compensation must be >= 1")
        limits = np.asarray(self.torque_abs_limit, dtype=float)
        if limits.shape != (N_JOINTS,) or not np.all(np.isfinite(limits)) or np.any(limits <= 0.0):
            raise ValueError(
                f"torque_abs_limit must contain {N_JOINTS} finite positive values"
            )


class GainScheduledRecoveryController:
    """Return bounded nominal or diagnosis-conditioned recovery torque commands.

    This is intentionally a transparent floor, not the final adaptive controller. It
    never compensates a type-abstained result, never invents a missing actuator location,
    and never uses privileged fault truth. A future learned attribution head and the
    oracle ceiling can drive the same callback for matched controller comparisons.
    """

    def __init__(self, config: RecoveryControlConfig | None = None) -> None:
        """Validate and retain the provisional recovery-controller settings."""

        self.config = config or RecoveryControlConfig()
        self.config.validate()

    def _confident_source(self, output: EstimatorOutput, source_index: int) -> bool:
        """Return whether one source estimate is actionable under the safety gates."""

        probabilities = np.asarray(output.p_class, dtype=float)
        maximum = float(np.max(probabilities))
        unique_best = bool(
            np.count_nonzero(np.isclose(probabilities, maximum)) == 1
            and int(np.argmax(probabilities)) == source_index
        )
        return bool(
            not output.abstain_decision
            and unique_best
            and probabilities[source_index]
            >= self.config.source_probability_threshold
            and np.isfinite(output.severity_uncertainty)
            and output.severity_uncertainty
            <= self.config.maximum_severity_uncertainty
        )

    def __call__(
        self, output: EstimatorOutput, _step_index: int, decision_time_s: float
    ) -> np.ndarray:
        """Apply recovery to the legacy time-indexed nominal task command."""

        if not np.isfinite(decision_time_s) or decision_time_s < 0.0:
            raise ValueError("decision_time_s must be finite and non-negative")
        nominal = commanded_torque(
            decision_time_s, scale=self.config.nominal_task_scale
        )
        return self.command_from_nominal(output, nominal)

    def command_from_nominal(
        self, output: EstimatorOutput, nominal_command: np.ndarray
    ) -> np.ndarray:
        """Apply diagnosis-conditioned recovery to one deployable nominal command.

        Args:
            output: Current schema-section-D diagnosis.
            nominal_command: Command produced by the matched task controller before
                diagnosis-conditioned recovery. It must contain no privileged truth.

        Returns:
            A finite command clipped to the controller's development torque limits.
        """

        output.validate()
        command = np.asarray(nominal_command, dtype=float)
        if command.shape != (N_JOINTS,) or not np.all(np.isfinite(command)):
            raise ValueError(
                f"nominal_command must be a finite shape-{(N_JOINTS,)} vector"
            )
        command = command.copy()

        if self._confident_source(output, STRUCTURE_INDEX):
            # A structural diagnosis does not justify pretending the stiffness estimate
            # restores the plant. The auditable safe action is a bounded global derate.
            command *= self.config.structural_command_derate

        if self._confident_source(output, ACTUATOR_INDEX):
            location = int(output.location_out)
            remaining = float(output.severity_out)
            if 0 <= location < N_JOINTS and 0.0 < remaining <= 1.0:
                effective_remaining = max(
                    remaining, self.config.minimum_gain_remaining
                )
                ideal_compensation = 1.0 / effective_remaining
                capped_compensation = min(
                    ideal_compensation, self.config.maximum_gain_compensation
                )
                # Weight the correction by the calibrated source probability. At a
                # one-hot oracle diagnosis this is exact inverse-gain scheduling; near the
                # action threshold it approaches the nominal command continuously.
                probability = float(output.p_class[ACTUATOR_INDEX])
                multiplier = 1.0 + probability * (capped_compensation - 1.0)
                command[location] *= multiplier

        limits = np.asarray(self.config.torque_abs_limit, dtype=float)
        bounded = np.clip(command, -limits, limits)
        if bounded.shape != (N_JOINTS,) or not np.all(np.isfinite(bounded)):
            raise RuntimeError("recovery controller produced an invalid command")
        return bounded
