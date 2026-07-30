"""Plant-contract regression guard for the structural-softening activation boundary.

`CablePlant` must swap to the topology-identical softened model at exactly the control
step named by `FaultSpec.onset_index`, and never before it. Protocol P names this test
as invariant I13b and requires it passing before any stage runs
(`protocol/protocol-p-v2.3.3.md`), but the property belongs to the plant rather than to
that screen, so the guard is permanent and outlives the protocol.

Why it is asserted here and not through a downstream gate: a structural fault that
activates at step 0 instead of the declared onset was measured in Session 41 to leave
every safety gate admissible at both remEI 0.75 and remEI 0.35, with roughly 70x margin
and a peak-|gauge| ratio of 1.035 / 0.999. A gate passing with that much headroom is
maximally insensitive to a defect that changes *which body* is being measured, so the
construction has to be asserted directly.

The boundary is a control-step comparison (`self._step_index >= max(onset_index, 0)`)
and is independent of mesh resolution and physics timestep, so these tests run at
reduced fidelity for speed.
"""

from __future__ import annotations

import sys
from pathlib import Path

import numpy as np
import pytest

SCRIPTS_DIR = Path(__file__).resolve().parents[1] / "scripts"
sys.path.insert(0, str(SCRIPTS_DIR))

from utils.assignment_generator import _step_index  # noqa: E402
from utils.cable_mechanics import CableModelConfig  # noqa: E402
from utils.cable_plant import CablePlant  # noqa: E402
from utils.schema_types import N_JOINTS, FaultSpec  # noqa: E402

PROTOCOL_ONSET_TIME_S = 1.0
PROTOCOL_CONTROL_DT_S = 0.002
PROTOCOL_ONSET_INDEX = 500
REDUCED_POINT_COUNT = 9
REDUCED_SIM_TIMESTEP_S = 2.0e-4


def structural_fault(onset_index: int, severity: float = 0.5) -> FaultSpec:
    """Return the link-softening fault Protocol P injects, at a chosen onset step.

    Inputs: the control-step index at which the fault must activate, and the remaining
    flexural-rigidity fraction. Output: a fully specified structural `FaultSpec` with
    every field set explicitly, which is the construction Protocol P I13a requires.
    """

    return FaultSpec(
        source_class="structure",
        subtype="link_stiffness_loss",
        location=1,
        severity=severity,
        onset_index=onset_index,
        compound_flag=False,
        ood_flag=False,
    )


def reduced_plant(fault: FaultSpec | None) -> CablePlant:
    """Return a reduced-fidelity plant carrying the supplied fault, or a healthy one.

    Inputs: an optional `FaultSpec`. Output: a `CablePlant` at reduced mesh resolution
    and physics timestep. Fidelity is reduced deliberately: the activation boundary is
    a control-step index comparison and does not depend on either quantity.
    """

    return CablePlant(
        CableModelConfig(),
        point_count=REDUCED_POINT_COUNT,
        simulation_timestep_s=REDUCED_SIM_TIMESTEP_S,
        fault=fault,
    )


def advance_steps(plant: CablePlant, n_steps: int) -> None:
    """Advance the plant `n_steps` control intervals under zero commanded torque.

    Inputs: a plant and a positive step count. Output: none; the plant is advanced in
    place. `CablePlant.rollout` is deliberately not used here — it returns a
    `PrivilegedRecord` whose validator requires a contiguous 0-based step grid, so it
    cannot be called a second time on the same plant to cross a boundary. The command
    is zero because the activation boundary is a control-step comparison and does not
    depend on the commanded torque.
    """

    if n_steps <= 0:
        raise ValueError("n_steps must be positive")
    command = np.zeros(N_JOINTS, dtype=float)
    for _ in range(n_steps):
        plant.advance(command)


def test_declared_onset_time_derives_to_the_protocol_onset_step() -> None:
    """The declared 1.0 s onset must derive to control step 500 at dt = 0.002 s."""

    assert _step_index(PROTOCOL_ONSET_TIME_S, PROTOCOL_CONTROL_DT_S) == PROTOCOL_ONSET_INDEX


@pytest.mark.parametrize("onset_index", [1, 5, PROTOCOL_ONSET_INDEX])
def test_structural_fault_softens_exactly_at_the_declared_onset(onset_index: int) -> None:
    """The softened model must be unused through onset-1 and in use at onset.

    Both the swap itself and its bookkeeping flag are asserted. The swap is the
    construction; the flag is only a record of it, and asserting a record instead of
    the thing it records is how a construction defect stays invisible.
    """

    plant = reduced_plant(structural_fault(onset_index))
    soft_model = plant._soft_model
    assert soft_model is not None, "a structural fault must build the softened model"
    assert plant._softened is False
    assert plant.model is not soft_model

    advance_steps(plant, onset_index)
    assert plant.step_index == onset_index
    assert plant._softened is False, f"softened before step {onset_index}"
    assert plant.model is not soft_model, f"model swapped before step {onset_index}"

    advance_steps(plant, 1)
    assert plant.step_index == onset_index + 1
    assert plant._softened is True, f"did not soften at step {onset_index}"
    assert plant.model is soft_model, f"model not swapped at step {onset_index}"


def test_omitted_onset_index_softens_at_step_zero() -> None:
    """A `FaultSpec` built without an explicit onset softens the body immediately.

    `FaultSpec.onset_index` defaults to -1 and the plant clamps it with
    `max(int(onset_index), 0)`, so an omitted onset is not "no onset" -- it is step 0,
    with no healthy pre-change segment anywhere in the run. This is the exact
    Session-41 construction defect, pinned here as behaviour so that a caller relying
    on the default is contradicted by a test rather than by a silent result.
    """

    fault = FaultSpec(
        source_class="structure",
        subtype="link_stiffness_loss",
        location=1,
        severity=0.5,
    )
    assert fault.onset_index == -1

    plant = reduced_plant(fault)
    advance_steps(plant, 1)
    assert plant._softened is True
    assert plant.model is plant._soft_model


def test_healthy_plant_builds_no_softened_model_and_never_switches() -> None:
    """A healthy plant must carry no softened model and must never soften.

    This is the companion to the fault cases: it pins that the inert
    `structural_ei_remaining` default on `CableModelConfig` does not reach the healthy
    body, which is built with `softened=False`.
    """

    plant = reduced_plant(None)
    assert plant._soft_model is None
    assert plant._softened is False

    advance_steps(plant, 3)
    assert plant._softened is False
