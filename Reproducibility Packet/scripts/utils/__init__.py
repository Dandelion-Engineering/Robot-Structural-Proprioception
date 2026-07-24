"""Shared library for the Robot Structural Proprioception reproducibility packet.

Per the project's software-engineering standard, logic shared across scripts lives
here and is imported rather than copy-pasted. Modules:

  * ``cable_mechanics`` -- shared selected MuJoCo model and state extraction.
  * ``cable_plant``     -- one-control-step schema-B plant producer.
  * ``schema_types`` -- typed carriers for schema v1.0 (privileged / observed records).
  * ``rng``          -- common-random-number substreams for the matched C1-vs-S pair.
  * ``config_contract`` -- strict draft/frozen config lifecycle, canonical hashing,
    and pre-confirmatory readiness validation.
  * ``storage_contract`` -- identity-manifest, role-index, whole-group split, and
    suite-scoped deployable observation loading/auditing.
  * ``sensor_model`` -- the sensor-realism + fault-injection model (schema section C).
  * ``online_loop``  -- causal plant/sensor/policy interleaving on the control grid.
  * ``synthetic_plant`` -- a schema-conforming synthetic privileged trace, for
    exercising the sensor lane in isolation (a development/test stand-in for the
    plant lane's real output, NOT part of the confirmatory pipeline).
  * ``metrics``      -- the two-layer success-bar metrics: four-way macro-F1 with
    abstention-as-error, calibration/selective/OOD family, and the J_5s tracking
    integral (schema Slot 7 / §G).
  * ``stats``        -- paired crossed pair-id/train-seed bootstrap intervals for the
    S-vs-C1 headline comparisons.
  * ``estimator``    -- the diagnosis-estimator lane (schema §D): the estimator-output
    contract, the past-only windowed front-end (the concrete W/stride realization), the
    detection/calibrated-abstention rung, the allowlisted oracle interface, and the
    online-seam command-policy adapter. The learned attribution/RMA rungs share this
    front-end and are trained post-config-freeze.
  * ``residual_baseline`` -- the deployable linear-ARX residual attribution floor:
    healthy nominal system identification, transparent residual-pattern prototypes,
    and separately calibrated off-prototype abstention.
  * ``recovery_control`` -- bounded diagnosis-conditioned derating / inverse-gain
    scheduling, applicable to either the legacy time-indexed task or an externally
    supplied deployable nominal command.
  * ``task_control`` -- low-authority encoder-feedback tracking of a smooth finite task
    reference and composition with the estimator/recovery policy seam.
"""

from utils.schema_types import SCHEMA_VERSION

__all__ = ["SCHEMA_VERSION"]
