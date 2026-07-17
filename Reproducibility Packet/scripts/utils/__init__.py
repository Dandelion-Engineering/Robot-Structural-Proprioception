"""Shared library for the Robot Structural Proprioception reproducibility packet.

Per the project's software-engineering standard, logic shared across scripts lives
here and is imported rather than copy-pasted. Modules:

  * ``cable_mechanics`` -- shared selected MuJoCo model and state extraction.
  * ``cable_plant``     -- one-control-step schema-B plant producer.
  * ``schema_types`` -- typed carriers for schema v1.0 (privileged / observed records).
  * ``rng``          -- common-random-number substreams for the matched C1-vs-S pair.
  * ``sensor_model`` -- the sensor-realism + fault-injection model (schema section C).
  * ``synthetic_plant`` -- a schema-conforming synthetic privileged trace, for
    exercising the sensor lane in isolation (a development/test stand-in for the
    plant lane's real output, NOT part of the confirmatory pipeline).
  * ``metrics``      -- the two-layer success-bar metrics: four-way macro-F1 with
    abstention-as-error, calibration/selective/OOD family, and the J_5s tracking
    integral (schema Slot 7 / §G).
  * ``stats``        -- the paired hierarchical-bootstrap confidence interval for the
    S-vs-C1 headline comparisons.
"""

from utils.schema_types import SCHEMA_VERSION

__all__ = ["SCHEMA_VERSION"]
