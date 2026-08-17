"""The one planar centerline derivation, shared by the fixture and read-order row 18.

**Why this is a module of its own.** Read-order row 18 of the connection-record design
(`protocol/slot8-connection-record-v0.1.md`, section 4.1) requires the adapter to derive
each arm's centerline from the authenticated `q_true`, `deform_coords` and the record's
`render_geometry`, and to check the distal point against the authenticated
`true_task_output`. Design section 2.4 separately requires sub-step 4b to add a
*dedicated deterministic adapter fixture* whose `q_true`, `deform_coords`, centerline and
`true_task_output` all come from **one** forward map -- because the existing contract
fixture's `deform_coords` and `true_task_output` come from independent synthetic maps and
so cannot serve as a geometry oracle at all.

Those two requirements are the same map used twice: once by the generator that builds the
fixture data, once by the adapter that checks it. Writing it once, here, is what makes the
fixture's agreement a statement about the derivation rather than a statement about two
copies of it happening to match. A second copy would agree with the first for exactly as
long as nobody edited either.

**What this module refuses to do.** It does not import `mujoco` and must not: invariant
V18 requires the whole Slot-8 surface to be openable by a reader who installed the packet
on a laptop, and design 3.5 records that reading the chain out of a live model at runtime
is the specific thing V18 forbids. The chain arrives instead as declared, record-carried
geometry that read-order row 2 has already structurally validated. This module applies
what the record declares and invents nothing:

  * it does not guess a tolerance -- the tolerance arrives from the record's authenticated
    geometry-validation artifact, bound at row 5;
  * it does not guess a convention -- `q_true_convention` and `projection` are matched
    against closed vocabularies and an unrecognised value is a refusal, not a default.

**The sign, stated plainly because it is the one thing here that is not settled.** Both
actuators in `utils.cable_mechanics.model_xml` are `gear="0 0 0 0 1 0"`, torque about the
model y axis, so the driven motion is planar in model x--z and the rotation-vector
component that advances a planar tangent is the y component. Which *sign* that component
carries in the scene frame is a convention this module cannot settle: settling it needs a
comparison against a stepped MuJoCo rollout, which V18 forbids the adapter from doing. So
the record declares the sign, this module applies the declared one, and the real-data
check that would catch a wrong declaration is the geometry-validation artifact's
maximum-deviation field -- a flipped tangent misses the distal point by centimetres, not
by nanometres. That artifact is not built in 4b and this module does not manufacture it.
"""

from __future__ import annotations

import math
from typing import Any, Mapping

import numpy as np

from utils.connection_record import LINK_IDS, RenderGeometry
from utils.verification_scene import (
    VerificationSceneError,
    X_GEOMETRY_UNSUPPORTED,
)

#: The derivation this module implements. `render_geometry.derivation_version` names it
#: so that a change to the map is a visible version change rather than a silent
#: difference between two figures (design 3.5).
DERIVATION_VERSION = "slot8-planar-centerline-v0.1"

#: The one accepted `planar_convention.q_true_convention`. Design 3.5 states the
#: convention in terms: `q_true[0]` is the first L1 body's **absolute** tangent
#: orientation and `q_true[1]` is the first L2 body's orientation **relative** to the
#: distal L1 tangent. The vocabulary is closed at one entry rather than left free
#: because the alternative reading -- treating `q_true[1]` as absolute -- produces a
#: centerline that is continuous, plausible and wrong, which is precisely the class of
#: error a declared-but-unchecked string would let through.
Q_TRUE_CONVENTION = "q0_absolute_first_body_tangent;q1_relative_to_distal_previous_tangent"

#: The two accepted `planar_convention.projection` values. Both carry the same
#: model-to-scene axis mapping, which design 3.5 settles: model x becomes scene x and
#: model z becomes scene y. They differ only in the sign with which the selected
#: rotation-vector component advances the scene-frame tangent angle, because that sign
#: is genuinely undetermined until the geometry-validation artifact exists (see the
#: module docstring). A record must say which one it means; neither is a default.
PROJECTION_TANGENT_ADVANCE_NEGATIVE = (
    "model_x_to_scene_x;model_z_to_scene_y;tangent_advance_negative"
)
PROJECTION_TANGENT_ADVANCE_POSITIVE = (
    "model_x_to_scene_x;model_z_to_scene_y;tangent_advance_positive"
)

#: `declared projection -> the sign the selected component carries`.
PROJECTION_SIGNS: Mapping[str, float] = {
    PROJECTION_TANGENT_ADVANCE_NEGATIVE: -1.0,
    PROJECTION_TANGENT_ADVANCE_POSITIVE: 1.0,
}

#: The width of one `deform_coords` log map. A triplet is a rotation vector, not a
#: quaternion and not an Euler triple, so it carries exactly three components and
#: `planar_convention.rotation_vector_component` selects one of them.
ROTATION_VECTOR_WIDTH = 3

#: The number of joint angles `q_true` carries -- one per link, in link order.
N_JOINT_ANGLES = 2


def _refuse(message: str) -> VerificationSceneError:
    """Return row 18's named refusal (design 4.5).

    Args:
        message: what could not be established, in terms of the declared geometry.

    Returns:
        The `VerificationSceneError` carrying `X_GEOMETRY_UNSUPPORTED`.

    It is returned rather than raised so every call site reads `raise _refuse(...)`,
    which keeps the raising statement at the site that failed.
    """

    return VerificationSceneError(X_GEOMETRY_UNSUPPORTED, message)


def centerline_point_count(geometry: RenderGeometry) -> int:
    """Return the number of points one derived centerline carries.

    Args:
        geometry: the record's validated `render_geometry`.

    Returns:
        One point at the proximal end of every ordered body across every link, plus
        the distal point -- so `sum(bodies per link) + 1`.

    The count is a property of the declared chain and never a choice: a fixture that
    emits a different number would still satisfy `utils.verification_scene`'s `[T,N,2]`
    shape gate, which requires only `N >= 2`. Callers that need to pin it should pin it
    as a literal, not as a re-derivation of this function.
    """

    return sum(len(geometry.links[link_id].segment_lengths_m) for link_id in LINK_IDS) + 1


def tangent_sign(geometry: RenderGeometry) -> float:
    """Return the declared sign of the tangent advance, or refuse.

    Args:
        geometry: the record's validated `render_geometry`.

    Returns:
        `-1.0` or `+1.0`, from `PROJECTION_SIGNS`.

    Raises:
        VerificationSceneError: `X_GEOMETRY_UNSUPPORTED` when the declared projection is
            not one this derivation implements.
    """

    projection = geometry.planar_convention.projection
    if projection not in PROJECTION_SIGNS:
        raise _refuse(
            f"render_geometry.planar_convention.projection is {projection!r}, which is "
            f"not a projection this derivation implements; the accepted values are "
            f"{sorted(PROJECTION_SIGNS)!r}"
        )
    return PROJECTION_SIGNS[projection]


def require_supported_convention(geometry: RenderGeometry) -> float:
    """Validate the declared conventions and the derivation version; return the sign.

    Args:
        geometry: the record's validated `render_geometry`.

    Returns:
        The declared tangent sign, so a caller that has validated the convention does
        not then have to look it up a second time.

    Raises:
        VerificationSceneError: `X_GEOMETRY_UNSUPPORTED` when the record declares a
            derivation version, joint convention, log-map component or projection this
            module does not implement.

    Every check here is an equality against a closed vocabulary rather than a parse.
    Row 2 has already established that these fields are well-formed strings and that
    the component is one of 0, 1 or 2; what is established here is the different and
    stronger property that they name *this* derivation.
    """

    if geometry.derivation_version != DERIVATION_VERSION:
        raise _refuse(
            f"render_geometry.derivation_version is {geometry.derivation_version!r}; "
            f"this adapter implements {DERIVATION_VERSION!r} and will not derive a "
            "centerline under a version whose map it does not carry"
        )
    convention = geometry.planar_convention
    if convention.q_true_convention != Q_TRUE_CONVENTION:
        raise _refuse(
            f"render_geometry.planar_convention.q_true_convention is "
            f"{convention.q_true_convention!r}; this derivation implements only "
            f"{Q_TRUE_CONVENTION!r}"
        )
    if not 0 <= convention.rotation_vector_component < ROTATION_VECTOR_WIDTH:
        raise _refuse(
            "render_geometry.planar_convention.rotation_vector_component is "
            f"{convention.rotation_vector_component}, which is not a component of a "
            f"{ROTATION_VECTOR_WIDTH}-vector log map"
        )
    return tangent_sign(geometry)


def _require_finite_array(value: Any, *, name: str, ndim: int) -> np.ndarray:
    """Return `value` as a finite float64 array of the stated rank, or refuse.

    Args:
        value: the authenticated payload column.
        name: the column's name, for the refusal message.
        ndim: the required number of dimensions.

    Returns:
        A float64 `np.ndarray`.

    Raises:
        VerificationSceneError: `X_GEOMETRY_UNSUPPORTED` when the array is the wrong
            rank or carries a non-finite value.

    A non-finite entry is refused here rather than allowed to propagate because a NaN
    in `q_true` produces a NaN centerline, and a NaN distal point fails the tolerance
    comparison with a message about geometry rather than about the payload that
    actually caused it.
    """

    array = np.asarray(value, dtype=float)
    if array.ndim != ndim:
        raise _refuse(
            f"{name} has {array.ndim} dimensions, expected {ndim}; the declared "
            "geometry cannot produce a centerline for it"
        )
    if not np.all(np.isfinite(array)):
        raise _refuse(f"{name} carries a non-finite value; a centerline cannot be derived from it")
    return array


def derive_centerline(
    q_true: Any, deform_coords: Any, geometry: RenderGeometry
) -> np.ndarray:
    """Derive the planar centerline for one arm (read-order row 18).

    Args:
        q_true: the authenticated `[T, 2]` joint-angle column.
        deform_coords: the authenticated `[T, n_def]` deformation column.
        geometry: the record's validated `render_geometry`.

    Returns:
        A `[T, N, 2]` float64 array of scene-frame points, where `N` is
        `centerline_point_count(geometry)`. The array is C-contiguous and freshly
        allocated; the caller owns it.

    Raises:
        VerificationSceneError: `X_GEOMETRY_UNSUPPORTED` when the declared geometry
            cannot produce a centerline for this pair -- an unimplemented convention, a
            rank or width mismatch, a non-finite input, or a declared triplet index the
            payload's `deform_coords` does not carry.

    **The map.** Starting at the declared base point with the tangent angle
    `q_true[0]`, the chain walks each link's ordered bodies in turn. Every body emits
    the point at its proximal end and then advances along its own segment length. Each
    internal body's declared `deform_coords` triplet rotates the tangent **before** that
    body's segment is traversed, because the ball joint that carries the triplet sits at
    that body's proximal end and orients that body -- the joint orients its own segment,
    not the next one. At the start of each link after the first, the corresponding
    `q_true` entry is added to the running angle rather than replacing it, which is what
    `q_true_convention` means by *relative to the distal previous tangent*. The distal
    point is emitted last and is the point row 18 compares against `true_task_output`.

    The loop runs over bodies and vectorises over time, because which body carries which
    triplet is the same at every step: the per-step work is a handful of `[T]`-shaped
    array operations rather than a Python iteration per sample.
    """

    sign = require_supported_convention(geometry)
    component = geometry.planar_convention.rotation_vector_component

    angles = _require_finite_array(q_true, name="q_true", ndim=2)
    deformation = _require_finite_array(deform_coords, name="deform_coords", ndim=2)
    if angles.shape[1] != N_JOINT_ANGLES:
        raise _refuse(
            f"q_true has width {angles.shape[1]}, expected {N_JOINT_ANGLES} -- one "
            "angle per link, in link order"
        )
    if angles.shape[0] != deformation.shape[0]:
        raise _refuse(
            f"q_true carries {angles.shape[0]} steps and deform_coords carries "
            f"{deformation.shape[0]}; one centerline cannot be derived from two grids"
        )
    if len(LINK_IDS) != N_JOINT_ANGLES:
        raise _refuse(
            f"the declared chain carries {len(LINK_IDS)} links but q_true carries "
            f"{N_JOINT_ANGLES} angles"
        )

    n_steps = angles.shape[0]
    n_points = centerline_point_count(geometry)
    centerline = np.empty((n_steps, n_points, 2), dtype=float)

    angle = angles[:, 0].copy()
    point = np.empty((n_steps, 2), dtype=float)
    point[:, 0] = geometry.planar_convention.base_xy_m[0]
    point[:, 1] = geometry.planar_convention.base_xy_m[1]

    emitted = 0
    for link_index, link_id in enumerate(LINK_IDS):
        link = geometry.links[link_id]
        if link_index > 0:
            angle = angle + angles[:, link_index]
        for body_index, segment_length_m in enumerate(link.segment_lengths_m):
            if body_index > 0:
                triplet = link.deform_triplets[body_index - 1]
                column = triplet[component]
                if column >= deformation.shape[1]:
                    raise _refuse(
                        f"render_geometry.links.{link_id} assigns internal body "
                        f"{body_index} the deform_coords column {column}, but the "
                        f"authenticated payload carries only {deformation.shape[1]} "
                        "columns"
                    )
                angle = angle + sign * deformation[:, column]
            centerline[:, emitted, 0] = point[:, 0]
            centerline[:, emitted, 1] = point[:, 1]
            emitted += 1
            point[:, 0] += segment_length_m * np.cos(angle)
            point[:, 1] += segment_length_m * np.sin(angle)

    centerline[:, emitted, 0] = point[:, 0]
    centerline[:, emitted, 1] = point[:, 1]
    emitted += 1
    if emitted != n_points:
        raise _refuse(
            f"the derivation emitted {emitted} points where the declared chain carries "
            f"{n_points}"
        )
    return centerline


def distal_deviation_m(centerline: np.ndarray, true_task_output: Any) -> float:
    """Return the largest per-step distance between the distal point and the tip.

    Args:
        centerline: a `[T, N, 2]` derived centerline.
        true_task_output: the authenticated `[T, 2]` true deformed tip column.

    Returns:
        The maximum over steps of the Euclidean distance, in metres.

    Raises:
        VerificationSceneError: `X_GEOMETRY_UNSUPPORTED` when the tip column is the
            wrong rank, width or length, or carries a non-finite value.
    """

    output = _require_finite_array(true_task_output, name="true_task_output", ndim=2)
    if output.shape != (centerline.shape[0], 2):
        raise _refuse(
            f"true_task_output has shape {output.shape}, expected "
            f"{(centerline.shape[0], 2)}; the derived centerline and the recorded tip "
            "are not on one grid"
        )
    return float(np.max(np.linalg.norm(centerline[:, -1, :] - output, axis=1)))


def require_distal_point_within_tolerance(
    centerline: np.ndarray,
    true_task_output: Any,
    tolerance_m: float,
    *,
    where: str,
) -> float:
    """Require the derived distal point to agree with the recorded tip; return the gap.

    Args:
        centerline: a `[T, N, 2]` derived centerline.
        true_task_output: the authenticated `[T, 2]` true deformed tip column.
        tolerance_m: the tolerance the record declares and read-order row 5 has already
            required to equal the named field of the authenticated geometry-validation
            artifact. **This routine never supplies a default**, and that is design
            finding CU's whole point: `CENTERLINE_TASK_OUTPUT_TOL_M` measures the
            fixture generator's construction exactness, and reusing it here would demand
            that two different computations of the same geometry agree to a nanometre.
        where: the arm being checked, for the refusal message.

    Returns:
        The measured maximum deviation in metres, so a caller can record what the
        agreement actually was rather than only that it passed.

    Raises:
        VerificationSceneError: `X_GEOMETRY_UNSUPPORTED` when the deviation exceeds the
            declared tolerance, or when the tolerance is not a finite positive number.
    """

    if not isinstance(tolerance_m, float) or not math.isfinite(tolerance_m) or tolerance_m <= 0.0:
        raise _refuse(
            f"{where}: the declared distal tolerance is {tolerance_m!r}; a tolerance is "
            "a finite positive number of metres"
        )
    deviation = distal_deviation_m(centerline, true_task_output)
    if not deviation <= tolerance_m:
        raise _refuse(
            f"{where}: the derived distal centerline point departs from "
            f"true_task_output by {deviation} m, above the declared tolerance "
            f"{tolerance_m} m"
        )
    return deviation
