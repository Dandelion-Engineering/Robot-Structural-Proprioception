"""Tests for the shared planar centerline derivation and the coherent adapter fixture.

**What this file is for.** It covers the first piece of Slot-8 sub-step 4b-ii-b: the one
forward map that read-order row 18 derives centerlines with, and the dedicated coherent
fixture design section 2.4 requires because the existing contract fixture cannot serve as
a geometry oracle. It does not cover the adapter rows themselves; rows 13 through 21 are
driven in `test_connection_adapter.py` once they exist.

**The standard the refusal tests are written to** is invariant W2, the same one the rest
of the lane uses: build the input the derivation refuses and drive the refusal, rather
than assert that a message exists.

**Three properties here are load-bearing rather than decorative**, and each one is a
specific error that a shape check or a smoke test would pass straight over:

  1. *Every declared triplet must have an effect, including the last internal body of
     L2.* A derivation that applies each body's rotation **after** traversing that body's
     own segment produces a continuous, plausible centerline in which each triplet acts
     on the following segment and the final triplet acts on nothing at all. Nothing about
     the output's shape, finiteness or smoothness reveals it.
  2. *`q_true[1]` is relative to the distal L1 tangent, not absolute.* The absolute
     reading also produces a continuous, plausible and wrong centerline. The separating
     case is a bent L1 with `q_true[1] = 0`.
  3. *The two links' triplet blocks must not be swappable without effect.* A swap is
     invisible to every shape and dtype check and is the one error that draws a
     different robot while looking entirely reasonable.

**What this file does not do.** It authors no connection record, opens no `dev`, `pilot`,
`val` or `test` result, selects no capacity or threshold, freezes no configuration and
makes no C1-versus-S statement. It builds no MuJoCo model and steps no rollout.
"""

from __future__ import annotations

import dataclasses
import json
import math
import subprocess
import sys
from pathlib import Path

import numpy as np
import pytest

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "scripts"))

from utils import centerline_geometry as cg  # noqa: E402
from utils.centerline_geometry import (  # noqa: E402
    DERIVATION_VERSION,
    N_JOINT_ANGLES,
    PROJECTION_SIGNS,
    PROJECTION_TANGENT_ADVANCE_NEGATIVE,
    PROJECTION_TANGENT_ADVANCE_POSITIVE,
    Q_TRUE_CONVENTION,
    ROTATION_VECTOR_WIDTH,
    centerline_point_count,
    derive_centerline,
    distal_deviation_m,
    require_distal_point_within_tolerance,
    require_supported_convention,
    tangent_sign,
)
from utils.coherent_geometry_fixture import (  # noqa: E402
    BODIES_PER_LINK,
    CENTERLINE_POINTS,
    FIXTURE_MAXIMUM_DEVIATION_FIELD_PATH,
    FIXTURE_TOLERANCE_FIELD_PATH,
    FIXTURE_VALIDATION_STATUS,
    INTERNAL_BODIES_PER_LINK,
    LINK_LENGTH_M,
    N_DEF,
    SEGMENT_LENGTH_M,
    chain_summary,
    coherent_deformation,
    coherent_privileged_record,
    coherent_render_geometry,
    fixture_maximum_deviation_m,
    geometry_validation_document,
    render_geometry_document,
    require_chain_arithmetic_closes,
)
from utils.connection_record import LINK_IDS  # noqa: E402
from utils.connection_record import _parse_render_geometry  # noqa: E402
from utils.connection_adapter import value_at_field_path  # noqa: E402
from utils.verification_scene import (  # noqa: E402
    CENTERLINE_TASK_OUTPUT_TOL_M,
    EXIT_CODES,
    VerificationSceneError,
    X_GEOMETRY_UNSUPPORTED,
)

#: Digests are declared as syntactically valid literals so the record parser accepts the
#: serialised block. Nothing here authenticates a file; these tests never open one.
PRODUCER_SHA256 = "a" * 64
TOLERANCE_SHA256 = "b" * 64
PRODUCER_RELATIVE = "scripts/utils/cable_mechanics.py"
TOLERANCE_RELATIVE = "results/coherent_fixture/geometry_validation.json"

#: The trajectory length the fixture tests build at. Short: every property here is
#: structural and none of them needs a long rollout.
N_STEPS = 64


def _geometry(**overrides):
    """Return the coherent fixture's declared geometry, with optional overrides."""

    arguments = {
        "producer_relative_path": PRODUCER_RELATIVE,
        "producer_sha256": PRODUCER_SHA256,
        "tolerance_artifact_relative_path": TOLERANCE_RELATIVE,
        "tolerance_sha256": TOLERANCE_SHA256,
    }
    arguments.update(overrides)
    return coherent_render_geometry(**arguments)


def _refusal(call) -> VerificationSceneError:
    """Drive `call`, require the row-18 refusal, and return it."""

    with pytest.raises(VerificationSceneError) as raised:
        call()
    assert raised.value.code == X_GEOMETRY_UNSUPPORTED
    return raised.value


@pytest.fixture(scope="module")
def geometry():
    """The declared chain every test in this file derives against."""

    return _geometry()


@pytest.fixture(scope="module")
def record(geometry):
    """One built coherent fixture record."""

    return coherent_privileged_record(geometry=geometry, n_steps=N_STEPS)


# --------------------------------------------------------------------------- #
# The exit code (design 4.5).
# --------------------------------------------------------------------------- #
def test_the_geometry_refusal_holds_exit_fifteen():
    """The fourteenth code, at the status design 4.5 assigned it."""

    assert EXIT_CODES[X_GEOMETRY_UNSUPPORTED] == 15


# --------------------------------------------------------------------------- #
# The declared chain.
# --------------------------------------------------------------------------- #
def test_the_chain_constants_are_the_producers_chain():
    """Every constant is pinned as a literal, and the arithmetic closes both ways.

    The values come from `utils.cable_mechanics` and `config/draft-config-v0.1.json`
    read at source: `point_count_per_link` is 17, so `cable_body_names` returns 16 body
    names; `extract_deformation_coordinates` skips the first body of each link, leaving
    15 internal bodies; and `values.plant.n_def` is 90, which is 2 x 15 x 3.
    """

    assert BODIES_PER_LINK == 16
    assert INTERNAL_BODIES_PER_LINK == 15
    assert N_DEF == 90
    assert LINK_LENGTH_M == 0.4
    assert SEGMENT_LENGTH_M == 0.025
    assert CENTERLINE_POINTS == 33
    assert 2 * INTERNAL_BODIES_PER_LINK * ROTATION_VECTOR_WIDTH == N_DEF
    assert BODIES_PER_LINK * SEGMENT_LENGTH_M == pytest.approx(LINK_LENGTH_M)
    assert dict(chain_summary())["n_def"] == N_DEF


def test_the_declared_geometry_is_the_producers_chain(geometry):
    """The generated declaration passes its own arithmetic gate."""

    require_chain_arithmetic_closes(geometry)
    assert centerline_point_count(geometry) == CENTERLINE_POINTS
    for link_id in LINK_IDS:
        link = geometry.links[link_id]
        assert len(link.segment_lengths_m) == BODIES_PER_LINK
        assert len(link.deform_triplets) == INTERNAL_BODIES_PER_LINK


def test_the_triplet_layout_is_the_contiguous_emission_order(geometry):
    """L1's fifteen internal bodies first, then L2's, three components each."""

    flattened: list[int] = []
    for link_id in LINK_IDS:
        for triplet in geometry.links[link_id].deform_triplets:
            flattened.extend(triplet)
    assert flattened == list(range(N_DEF))
    assert geometry.links["L1"].deform_triplets[0] == (0, 1, 2)
    assert geometry.links["L1"].deform_triplets[-1] == (42, 43, 44)
    assert geometry.links["L2"].deform_triplets[0] == (45, 46, 47)
    assert geometry.links["L2"].deform_triplets[-1] == (87, 88, 89)


def test_a_chain_that_is_not_the_producers_chain_is_refused(geometry):
    """`require_chain_arithmetic_closes` is a gate, not a comment."""

    short = dataclasses.replace(
        geometry,
        links={
            "L1": dataclasses.replace(
                geometry.links["L1"],
                segment_lengths_m=geometry.links["L1"].segment_lengths_m[:-1],
                deform_triplets=geometry.links["L1"].deform_triplets[:-1],
            ),
            "L2": geometry.links["L2"],
        },
    )
    with pytest.raises(ValueError, match="declares 15 bodies"):
        require_chain_arithmetic_closes(short)

    stretched = dataclasses.replace(
        geometry,
        links={
            "L1": dataclasses.replace(
                geometry.links["L1"],
                segment_lengths_m=(0.05,) * BODIES_PER_LINK,
            ),
            "L2": geometry.links["L2"],
        },
    )
    with pytest.raises(ValueError, match="segment length"):
        require_chain_arithmetic_closes(stretched)


# --------------------------------------------------------------------------- #
# The forward map.
# --------------------------------------------------------------------------- #
def test_an_undeformed_chain_at_zero_angles_lies_straight(geometry):
    """The whole chain, undeformed, is 0.8 m of straight rod from the declared base."""

    q_true = np.zeros((3, N_JOINT_ANGLES))
    deform = np.zeros((3, N_DEF))
    centerline = derive_centerline(q_true, deform, geometry)

    assert centerline.shape == (3, CENTERLINE_POINTS, 2)
    base = geometry.planar_convention.base_xy_m
    assert centerline[0, 0, 0] == pytest.approx(base[0])
    assert centerline[0, 0, 1] == pytest.approx(base[1])
    assert centerline[0, -1, 0] == pytest.approx(base[0] + 2 * LINK_LENGTH_M)
    assert centerline[0, -1, 1] == pytest.approx(base[1])
    spacing = np.diff(centerline[0, :, 0])
    assert np.allclose(spacing, SEGMENT_LENGTH_M)


def test_the_first_emitted_point_is_always_the_declared_base(geometry, record):
    """The base point is where the chain starts, at every step and under deformation."""

    centerline = derive_centerline(record.q_true, record.deform_coords, geometry)
    base = geometry.planar_convention.base_xy_m
    assert np.all(centerline[:, 0, 0] == base[0])
    assert np.all(centerline[:, 0, 1] == base[1])


def test_every_segment_keeps_its_declared_length(geometry, record):
    """Deformation rotates the chain; it never stretches it."""

    centerline = derive_centerline(record.q_true, record.deform_coords, geometry)
    lengths = np.linalg.norm(np.diff(centerline, axis=1), axis=2)
    assert np.allclose(lengths, SEGMENT_LENGTH_M, rtol=0.0, atol=1.0e-12)


def test_every_declared_triplet_moves_the_distal_point(geometry):
    """Including L2's last internal body -- the off-by-one a plausible map hides.

    A derivation that applied each internal body's rotation *after* traversing that
    body's own segment would shift every triplet onto the following segment and leave
    the final triplet with nothing to act on. This drives all thirty declared triplets
    one at a time and requires each to move the tip, so that error cannot survive.
    """

    q_true = np.zeros((1, N_JOINT_ANGLES))
    zero = np.zeros((1, N_DEF))
    reference = derive_centerline(q_true, zero, geometry)[0, -1, :]
    component = geometry.planar_convention.rotation_vector_component

    displacements = []
    for link_id in LINK_IDS:
        for triplet in geometry.links[link_id].deform_triplets:
            deform = zero.copy()
            deform[0, triplet[component]] = 0.05
            moved = derive_centerline(q_true, deform, geometry)[0, -1, :]
            displacements.append(float(np.linalg.norm(moved - reference)))

    assert len(displacements) == 2 * INTERNAL_BODIES_PER_LINK
    assert min(displacements) > 1.0e-6, "a declared triplet has no effect on the tip"


def test_only_the_declared_rotation_vector_component_is_read(geometry):
    """The other two components of every log map are inert, by declaration."""

    q_true = np.zeros((1, N_JOINT_ANGLES))
    zero = np.zeros((1, N_DEF))
    reference = derive_centerline(q_true, zero, geometry)
    component = geometry.planar_convention.rotation_vector_component

    deform = zero.copy()
    for link_id in LINK_IDS:
        for triplet in geometry.links[link_id].deform_triplets:
            for position, column in enumerate(triplet):
                if position != component:
                    deform[0, column] = 0.5
    assert np.array_equal(derive_centerline(q_true, deform, geometry), reference)


def test_the_second_joint_angle_is_relative_to_the_distal_first_link_tangent(geometry):
    """The separating case: a bent L1 with `q_true[1] = 0`.

    Under the declared relative convention L2 continues straight on from L1's distal
    tangent, so the whole chain is one straight line at angle `q_true[0]`. Under the
    absolute reading L2 would snap back to the base frame and the chain would bend at
    the elbow. Both are continuous and plausible; only one is what the record declares.
    """

    q_true = np.array([[0.7, 0.0]])
    deform = np.zeros((1, N_DEF))
    centerline = derive_centerline(q_true, deform, geometry)[0]

    base = np.asarray(geometry.planar_convention.base_xy_m)
    direction = np.array([math.cos(0.7), math.sin(0.7)])
    expected_tip = base + 2 * LINK_LENGTH_M * direction
    assert centerline[-1] == pytest.approx(expected_tip)

    elbow = centerline[BODIES_PER_LINK]
    assert elbow == pytest.approx(base + LINK_LENGTH_M * direction)


def test_swapping_the_two_links_triplet_blocks_changes_the_centerline(geometry, record):
    """A link swap is invisible to every shape check, so it is driven here.

    The two links carry equal body counts and equal segment lengths, so exchanging their
    declared triplet blocks yields a geometry that passes the record parser's contiguity
    rule in neither direction *and* would pass every dtype and shape gate if it did. The
    property that separates them is the derived centerline itself.
    """

    swapped = dataclasses.replace(
        geometry,
        links={
            "L1": dataclasses.replace(
                geometry.links["L1"],
                deform_triplets=geometry.links["L2"].deform_triplets,
            ),
            "L2": dataclasses.replace(
                geometry.links["L2"],
                deform_triplets=geometry.links["L1"].deform_triplets,
            ),
        },
    )
    original = derive_centerline(record.q_true, record.deform_coords, geometry)
    exchanged = derive_centerline(record.q_true, record.deform_coords, swapped)
    assert not np.allclose(original, exchanged)


def test_the_derivation_is_deterministic(geometry, record):
    """Two derivations of one input are bit-identical (invariant V13's precondition)."""

    first = derive_centerline(record.q_true, record.deform_coords, geometry)
    second = derive_centerline(record.q_true, record.deform_coords, geometry)
    assert np.array_equal(first, second)
    assert first is not second


def test_the_returned_centerline_is_a_fresh_array(geometry, record):
    """The caller owns the result; mutating it cannot reach back into the derivation."""

    first = derive_centerline(record.q_true, record.deform_coords, geometry)
    first[0, 0, 0] = 1234.5
    second = derive_centerline(record.q_true, record.deform_coords, geometry)
    assert second[0, 0, 0] != 1234.5


# --------------------------------------------------------------------------- #
# The declared sign, which this lane does not settle.
# --------------------------------------------------------------------------- #
def test_the_two_declared_projections_are_the_two_signs():
    """The vocabulary is closed at two entries, and they differ only in the sign."""

    assert PROJECTION_SIGNS == {
        PROJECTION_TANGENT_ADVANCE_NEGATIVE: -1.0,
        PROJECTION_TANGENT_ADVANCE_POSITIVE: 1.0,
    }
    assert tangent_sign(_geometry(projection=PROJECTION_TANGENT_ADVANCE_NEGATIVE)) == -1.0
    assert tangent_sign(_geometry(projection=PROJECTION_TANGENT_ADVANCE_POSITIVE)) == 1.0


def test_the_declared_sign_changes_the_derived_centerline(record):
    """The sign is applied, not decorative -- and the two readings are mirror images.

    Deriving under one sign, then under the other with the deformation negated,
    reproduces the first exactly. That is what makes the sign a *declaration*: the map
    is the same map, and the record chooses which way the tangent turns.
    """

    negative = _geometry(projection=PROJECTION_TANGENT_ADVANCE_NEGATIVE)
    positive = _geometry(projection=PROJECTION_TANGENT_ADVANCE_POSITIVE)

    under_negative = derive_centerline(record.q_true, record.deform_coords, negative)
    under_positive = derive_centerline(record.q_true, record.deform_coords, positive)
    assert not np.allclose(under_negative, under_positive)

    mirrored = derive_centerline(record.q_true, -record.deform_coords, positive)
    assert np.allclose(under_negative, mirrored, rtol=0.0, atol=1.0e-15)


# --------------------------------------------------------------------------- #
# Refusals -- invariant W2: build the input, drive the exit.
# --------------------------------------------------------------------------- #
def test_an_unrecognised_projection_is_refused(geometry, record):
    """An unknown projection is a refusal, never a default sign."""

    unknown = dataclasses.replace(
        geometry,
        planar_convention=dataclasses.replace(
            geometry.planar_convention, projection="model_y_to_scene_x"
        ),
    )
    error = _refusal(
        lambda: derive_centerline(record.q_true, record.deform_coords, unknown)
    )
    assert "projection" in str(error)


def test_an_unrecognised_joint_convention_is_refused(geometry, record):
    """The absolute reading of `q_true[1]` cannot be smuggled in as a declaration."""

    unknown = dataclasses.replace(
        geometry,
        planar_convention=dataclasses.replace(
            geometry.planar_convention, q_true_convention="q0_absolute;q1_absolute"
        ),
    )
    error = _refusal(
        lambda: derive_centerline(record.q_true, record.deform_coords, unknown)
    )
    assert "q_true_convention" in str(error)


def test_a_derivation_version_this_module_does_not_implement_is_refused(geometry, record):
    """A version bump means a different map, and this one refuses to guess at it."""

    other = dataclasses.replace(
        geometry, derivation_version="slot8-planar-centerline-v0.2"
    )
    error = _refusal(
        lambda: derive_centerline(record.q_true, record.deform_coords, other)
    )
    assert DERIVATION_VERSION in str(error)


def test_a_rotation_vector_component_outside_the_log_map_is_refused(geometry, record):
    """Row 2 bounds the component; this is the derivation's own independent gate."""

    out_of_range = dataclasses.replace(
        geometry,
        planar_convention=dataclasses.replace(
            geometry.planar_convention, rotation_vector_component=ROTATION_VECTOR_WIDTH
        ),
    )
    _refusal(lambda: require_supported_convention(out_of_range))


def test_a_declared_column_the_payload_does_not_carry_is_refused(geometry, record):
    """A record naming column 89 against an 80-column payload refuses, not indexes."""

    narrow = record.deform_coords[:, : N_DEF - 10]
    error = _refusal(lambda: derive_centerline(record.q_true, narrow, geometry))
    assert "columns" in str(error)


def test_a_non_finite_input_is_refused_before_it_becomes_a_non_finite_centerline(
    geometry, record
):
    """A NaN in the payload refuses here, naming the payload rather than the geometry."""

    broken = record.q_true.copy()
    broken[3, 0] = np.nan
    error = _refusal(
        lambda: derive_centerline(broken, record.deform_coords, geometry)
    )
    assert "q_true" in str(error)

    broken_deform = record.deform_coords.copy()
    broken_deform[2, 7] = np.inf
    error = _refusal(
        lambda: derive_centerline(record.q_true, broken_deform, geometry)
    )
    assert "deform_coords" in str(error)


def test_a_mismatched_grid_or_width_is_refused(geometry, record):
    """Two grids are not one arm, and a three-wide `q_true` is not this chain."""

    _refusal(
        lambda: derive_centerline(
            record.q_true[:-1], record.deform_coords, geometry
        )
    )
    wide = np.zeros((record.q_true.shape[0], N_JOINT_ANGLES + 1))
    error = _refusal(lambda: derive_centerline(wide, record.deform_coords, geometry))
    assert "width" in str(error)


def test_a_rank_that_is_not_a_time_series_is_refused(geometry, record):
    """`[T]` and `[T,N,2]` are both refused where `[T,2]` is required."""

    _refusal(
        lambda: derive_centerline(
            record.q_true[:, 0], record.deform_coords, geometry
        )
    )
    _refusal(
        lambda: derive_centerline(
            record.q_true[:, :, None], record.deform_coords, geometry
        )
    )


# --------------------------------------------------------------------------- #
# The distal check -- and the tolerance it refuses to invent.
# --------------------------------------------------------------------------- #
def test_the_distal_check_supplies_no_default_tolerance():
    """Finding CU: the tolerance is an argument with no default, at every call site."""

    import inspect

    signature = inspect.signature(require_distal_point_within_tolerance)
    assert signature.parameters["tolerance_m"].default is inspect.Parameter.empty


def test_the_distal_check_accepts_the_coherent_fixture(geometry, record):
    """The fixture's own exactness oracle: the tip *is* the distal point."""

    centerline = derive_centerline(record.q_true, record.deform_coords, geometry)
    deviation = require_distal_point_within_tolerance(
        centerline,
        record.true_task_output,
        CENTERLINE_TASK_OUTPUT_TOL_M,
        where="arm C1",
    )
    assert deviation == 0.0


def test_the_distal_check_refuses_a_tip_outside_the_declared_tolerance(geometry, record):
    """A displaced tip refuses under row 18's code and names the measured gap."""

    centerline = derive_centerline(record.q_true, record.deform_coords, geometry)
    displaced = record.true_task_output + np.array([0.0, 1.0e-3])
    error = _refusal(
        lambda: require_distal_point_within_tolerance(
            centerline, displaced, CENTERLINE_TASK_OUTPUT_TOL_M, where="arm S"
        )
    )
    assert "arm S" in str(error)
    assert "true_task_output" in str(error)


def test_the_distal_check_refuses_a_tolerance_that_is_not_a_positive_number(
    geometry, record
):
    """Zero, negative and non-finite tolerances are refused rather than applied."""

    centerline = derive_centerline(record.q_true, record.deform_coords, geometry)
    for tolerance in (0.0, -1.0e-9, float("inf"), float("nan")):
        _refusal(
            lambda tolerance=tolerance: require_distal_point_within_tolerance(
                centerline, record.true_task_output, tolerance, where="arm C1"
            )
        )


def test_the_distal_check_refuses_a_tip_column_on_a_different_grid(geometry, record):
    """A tip column of the wrong length is a grid disagreement, not a near miss."""

    centerline = derive_centerline(record.q_true, record.deform_coords, geometry)
    error = _refusal(
        lambda: distal_deviation_m(centerline, record.true_task_output[:-1])
    )
    assert "one grid" in str(error)


# --------------------------------------------------------------------------- #
# The coherent fixture.
# --------------------------------------------------------------------------- #
def test_the_fixture_reproduces_its_own_tip_exactly(geometry, record):
    """The construction-exactness oracle, measured rather than asserted."""

    assert fixture_maximum_deviation_m(record, geometry) <= CENTERLINE_TASK_OUTPUT_TOL_M


def test_the_fixture_record_validates_against_schema_b(record):
    """`PrivilegedRecord.validate` is called by the generator; it is re-driven here."""

    record.validate()
    assert record.n_steps == N_STEPS
    assert record.n_def == N_DEF
    assert record.q_true.shape == (N_STEPS, N_JOINT_ANGLES)
    assert record.true_task_output.shape == (N_STEPS, 2)


def test_the_fixture_tracking_error_is_the_deformation_deflection(geometry, record):
    """`task_reference` is the same chain with the deformation removed.

    That is what makes the tracking lane consistent with the geometry lane rather than
    merely schema-conforming: the recorded error is exactly what the declared bending
    did to the tip, and it is a millimetre-scale quantity rather than an arbitrary one.
    """

    rigid = derive_centerline(
        record.q_true, np.zeros_like(record.deform_coords), geometry
    )
    assert np.allclose(record.task_reference, rigid[:, -1, :], rtol=0.0, atol=0.0)
    deflection = float(np.max(record.tracking_error_norm))
    assert 1.0e-5 < deflection < 1.0e-2


def test_the_fixture_is_deterministic_and_seed_separated(geometry):
    """One seed gives bit-identical data twice; two seeds give different data."""

    first = coherent_privileged_record(geometry=geometry, n_steps=N_STEPS, seed=0)
    again = coherent_privileged_record(geometry=geometry, n_steps=N_STEPS, seed=0)
    other = coherent_privileged_record(geometry=geometry, n_steps=N_STEPS, seed=1)

    assert np.array_equal(first.deform_coords, again.deform_coords)
    assert np.array_equal(first.true_task_output, again.true_task_output)
    assert not np.allclose(first.deform_coords, other.deform_coords)
    assert not np.allclose(first.true_task_output, other.true_task_output)


def test_every_deformation_column_is_distinct(geometry):
    """A column that duplicates another cannot separate a mis-indexed triplet."""

    t_s = np.arange(N_STEPS) / 500.0
    deform = coherent_deformation(N_STEPS, t_s, seed=0)
    assert deform.shape == (N_STEPS, N_DEF)
    columns = {deform[:, index].tobytes() for index in range(N_DEF)}
    assert len(columns) == N_DEF


def test_the_fixture_deformation_stays_a_gently_bent_rod():
    """Amplitudes are milliradian-scale, so the chain is a rod and not a coil."""

    t_s = np.arange(N_STEPS) / 500.0
    deform = coherent_deformation(N_STEPS, t_s, seed=0)
    assert float(np.max(np.abs(deform))) < 5.0e-3


def test_the_fixture_curvature_comes_from_the_same_deformation(geometry, record):
    """The strain lane cannot contradict the geometry lane, because it is derived.

    The check is an identity rather than a correlation: every station's curvature must
    be exactly one declared `deform_coords` column divided by that body's own segment
    length. That is what separates a derived channel from an independently generated one
    that merely looks plausible beside it -- which is precisely the contract fixture's
    defect, and the reason this fixture exists.
    """

    assert record.curvature_true.shape == (N_STEPS, 4)
    assert np.all(np.isfinite(record.curvature_true))
    assert float(np.max(np.abs(record.curvature_true))) > 0.0

    component = geometry.planar_convention.rotation_vector_component
    matched = 0
    for station in range(record.curvature_true.shape[1]):
        implied = record.curvature_true[:, station] * SEGMENT_LENGTH_M
        for link_id in LINK_IDS:
            for triplet in geometry.links[link_id].deform_triplets:
                if np.allclose(
                    implied,
                    record.deform_coords[:, triplet[component]],
                    rtol=0.0,
                    atol=1.0e-18,
                ):
                    matched += 1
                    break
            else:
                continue
            break
    assert matched == record.curvature_true.shape[1]


def test_the_fixture_curvature_moves_when_the_deformation_does(geometry):
    """A different deformation gives a different strain lane, seed for seed."""

    first = coherent_privileged_record(geometry=geometry, n_steps=N_STEPS, seed=0)
    other = coherent_privileged_record(geometry=geometry, n_steps=N_STEPS, seed=1)
    assert not np.allclose(first.curvature_true, other.curvature_true)
    assert not np.allclose(first.gauge_true, other.gauge_true)


def test_the_generator_refuses_a_chain_that_does_not_cover_every_column(geometry):
    """Right counts, wrong columns: fifteen triplets all naming the same three.

    This is the case a column *count* cannot reach -- two links of fifteen internal
    bodies always declare ninety columns, whatever those columns are. The body counts,
    the segment lengths and the point count all still hold here; only the coverage is
    wrong, and it is wrong in the direction that silently drops fourteen bodies' worth
    of deformation onto one.
    """

    repeated = dataclasses.replace(
        geometry,
        links={
            "L1": dataclasses.replace(
                geometry.links["L1"],
                deform_triplets=((0, 1, 2),) * INTERNAL_BODIES_PER_LINK,
            ),
            "L2": geometry.links["L2"],
        },
    )
    assert len(repeated.links["L1"].deform_triplets) == INTERNAL_BODIES_PER_LINK
    assert centerline_point_count(repeated) == CENTERLINE_POINTS
    with pytest.raises(ValueError, match="deformation columns"):
        require_chain_arithmetic_closes(repeated)


# --------------------------------------------------------------------------- #
# Why this fixture exists: the contract fixture is not a geometry oracle.
# --------------------------------------------------------------------------- #
def test_the_contract_fixture_deformation_does_not_explain_its_own_tip():
    """Design 2.4's measured reason, re-driven here rather than quoted.

    `utils.synthetic_plant` draws `deform_coords` from an independent phase set and
    computes `true_task_output` from `curvature_true`, which carries no relation to it.
    The sharp form of that incoherence is not the size of the gap but its behaviour:
    zeroing the deformation entirely does **not** make the reconstruction worse. If the
    two channels described one body, removing the deformation would move the derived tip
    away from the recorded one at every seed. It does not, and at some seeds the rigid
    reconstruction is the closer of the two.

    Both chains are bound to a common base here, because comparing across two different
    origins would measure the half-metre offset between them instead of this.
    """

    from utils.synthetic_plant import synthetic_privileged_record

    geometry = _geometry(base_xy_m=(0.0, 0.0))
    deformed_gaps: list[float] = []
    rigid_gaps: list[float] = []
    for seed in (0, 1, 2, 3):
        incoherent = synthetic_privileged_record(n_steps=N_STEPS, seed=seed)
        deformed = derive_centerline(
            incoherent.q_true, incoherent.deform_coords, geometry
        )
        rigid = derive_centerline(
            incoherent.q_true, np.zeros_like(incoherent.deform_coords), geometry
        )
        deformed_gaps.append(distal_deviation_m(deformed, incoherent.true_task_output))
        rigid_gaps.append(distal_deviation_m(rigid, incoherent.true_task_output))

    assert min(deformed_gaps) > 1.0e-3, "the gap is millimetre-scale, not float noise"
    assert any(
        rigid <= deformed for rigid, deformed in zip(rigid_gaps, deformed_gaps)
    ), "removing the deformation should not improve a coherent fixture"


def test_the_coherent_fixture_is_the_one_that_closes(geometry, record):
    """The contrast, stated as a single comparison the reviewer can read off."""

    from utils.synthetic_plant import synthetic_privileged_record

    flat = _geometry(base_xy_m=(0.0, 0.0))
    incoherent = synthetic_privileged_record(n_steps=N_STEPS, seed=0)
    incoherent_gap = distal_deviation_m(
        derive_centerline(incoherent.q_true, incoherent.deform_coords, flat),
        incoherent.true_task_output,
    )
    assert fixture_maximum_deviation_m(record, geometry) <= CENTERLINE_TASK_OUTPUT_TOL_M
    assert incoherent_gap > 1.0e6 * CENTERLINE_TASK_OUTPUT_TOL_M


# --------------------------------------------------------------------------- #
# The record block and the fixture's own validation artifact.
# --------------------------------------------------------------------------- #
def test_the_serialised_block_round_trips_through_the_record_parser(geometry):
    """The dataclass is the source; the document is derived; the two must agree.

    `_parse_render_geometry` is imported directly because this file is testing the
    serialiser against the parser as a pair. The public whole-record path exercises the
    same parser and is driven in `test_connection_adapter.py`.
    """

    document = render_geometry_document(geometry)
    encoded = json.loads(json.dumps(document, allow_nan=False))
    assert _parse_render_geometry(encoded) == geometry


def test_the_serialised_block_is_json_with_no_non_finite_value(geometry):
    """A record is strict JSON; a non-finite float would refuse at read-order row 2."""

    text = json.dumps(render_geometry_document(geometry), allow_nan=False, sort_keys=True)
    assert "Infinity" not in text and "NaN" not in text


def test_the_validation_artifact_resolves_at_the_declared_field_paths(geometry):
    """The record names two dotted paths; the artifact must answer at both of them."""

    document = geometry_validation_document(0.0)
    tolerance = value_at_field_path(
        document,
        geometry.tolerance_source.tolerance_field_path,
        where="tolerance_field_path",
    )
    maximum = value_at_field_path(
        document,
        geometry.tolerance_source.maximum_deviation_field_path,
        where="maximum_deviation_field_path",
    )
    assert tolerance == geometry.distal_tolerance_m
    assert maximum == 0.0
    assert geometry.tolerance_source.tolerance_field_path == FIXTURE_TOLERANCE_FIELD_PATH
    assert (
        geometry.tolerance_source.maximum_deviation_field_path
        == FIXTURE_MAXIMUM_DEVIATION_FIELD_PATH
    )


def test_the_validation_artifact_says_in_its_own_bytes_what_it_is_not(geometry):
    """A fixture number must not be readable later as an approved real-data number."""

    document = geometry_validation_document(0.0)
    assert document["status"] == FIXTURE_VALIDATION_STATUS
    scope = document["scope"]
    assert "synthetic fixture" in scope
    assert "manufactures no tolerance" in scope
    assert "does not exist yet" in scope


def test_the_validation_artifact_refuses_numbers_that_refuse_each_other():
    """The generator fails loudly rather than emit an artifact row 5 would reject."""

    with pytest.raises(ValueError, match="above its own"):
        geometry_validation_document(1.0e-3)
    with pytest.raises(ValueError, match="non-negative"):
        geometry_validation_document(-1.0e-12)
    with pytest.raises(ValueError, match="non-negative"):
        geometry_validation_document(float("nan"))
    with pytest.raises(ValueError, match="finite and positive"):
        geometry_validation_document(0.0, tolerance_m=0.0)


def test_the_declared_tolerance_is_the_fixtures_construction_constant(geometry):
    """Finding CU: 1 nm stays the fixture's and never becomes a real-data tolerance."""

    assert geometry.distal_tolerance_m == CENTERLINE_TASK_OUTPUT_TOL_M
    assert CENTERLINE_TASK_OUTPUT_TOL_M == 1.0e-9


def test_the_declared_conventions_are_the_ones_the_derivation_implements(geometry):
    """The fixture declares what it generated under, and nothing else."""

    assert geometry.derivation_version == DERIVATION_VERSION
    assert geometry.planar_convention.q_true_convention == Q_TRUE_CONVENTION
    assert geometry.planar_convention.rotation_vector_component == 1
    assert geometry.planar_convention.projection in PROJECTION_SIGNS
    require_supported_convention(geometry)


# --------------------------------------------------------------------------- #
# Invariant V18.
# --------------------------------------------------------------------------- #
def test_neither_module_imports_mujoco_or_torch():
    """Asserted in a fresh interpreter, because import side effects are what matter.

    `utils.cable_mechanics` imports `mujoco` at module scope, and it is the producer
    this geometry describes. The whole reason design 3.5 put the chain in the record is
    that reading it from a live model would pull that import into the Slot-8 surface.
    """

    scripts = Path(__file__).resolve().parents[1] / "scripts"
    program = (
        "import sys;"
        "sys.path.insert(0, %r);" % str(scripts)
        + "import utils.centerline_geometry, utils.coherent_geometry_fixture;"
        "print('mujoco' in sys.modules, 'torch' in sys.modules)"
    )
    completed = subprocess.run(
        [sys.executable, "-c", program],
        capture_output=True,
        text=True,
        check=True,
    )
    assert completed.stdout.strip() == "False False"
