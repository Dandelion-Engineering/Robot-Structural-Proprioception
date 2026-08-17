"""The dedicated coherent adapter fixture: one forward map builds it and checks it.

**Why this exists, and why the existing contract fixture could not be used.** Design
section 2.4 of `protocol/slot8-connection-record-v0.1.md` requires sub-step 4b to add a
dedicated deterministic adapter fixture whose `q_true`, `deform_coords`, centerline and
`true_task_output` are all generated from one dependency-light forward map. It requires
this because the existing contract fixture cannot serve as a geometry oracle at all, and
that is a measured fact rather than a preference: `utils.synthetic_plant` draws
`deform_coords` from an independent `rng.uniform` phase set and computes
`true_task_output` from `curvature_true`, which carries no relation to `deform_coords`.
A reconstruction probe at the delivered settings misses the recorded tip by millimetres.
Calibrating a tolerance against that gap would make read-order row 18 meaningless.

**What this fixture proves, stated narrowly on purpose.** It proves the *derivation
logic*: that `utils.centerline_geometry.derive_centerline` walks the declared chain the
way the record says it does, so that data generated under a declared convention is
reproduced by the adapter reading that same declaration. It proves nothing about MuJoCo.
In particular it does **not** establish that the declared tangent sign is the sign a real
rollout would produce -- the generator and the checker share the declaration, so they
would agree with each other under either sign. That question belongs to the separately
approved geometry-validation artifact for real data, which does not exist and which this
module does not manufacture. See `utils.centerline_geometry`'s module docstring.

**The tolerance this fixture carries is the fixture's own.** Design finding CU separates
the two things the one tolerance constant was being asked to be.
`utils.verification_scene.CENTERLINE_TASK_OUTPUT_TOL_M` measures *construction
exactness* -- here the distal point **is** the recorded tip, by construction -- and stays
the fixture's. The production adapter's tolerance comes only from the record's
authenticated geometry-validation artifact. The document
`geometry_validation_document` returns says so in its own bytes, not only in a review
card, so a later reader cannot mistake a fixture number for an approved one.

**No MuJoCo, here or downstream (invariant V18).** This module does not import
`utils.cable_mechanics`, because that module imports `mujoco` at module scope. The two
chain constants that live in the model rather than in the configuration --
`link_length_m` and the body count -- are therefore stated here as literals with their
source recorded, which is the same reason design 3.5 put the chain in the record instead
of reading it from a live model.
"""

from __future__ import annotations

import math
from pathlib import PurePosixPath
from typing import Any, Mapping

import numpy as np

from utils.centerline_geometry import (
    DERIVATION_VERSION,
    PROJECTION_TANGENT_ADVANCE_NEGATIVE,
    Q_TRUE_CONVENTION,
    centerline_point_count,
    derive_centerline,
    distal_deviation_m,
)
from utils.connection_record import (
    LINK_IDS,
    GeometrySource,
    LinkGeometry,
    PlanarConvention,
    RenderGeometry,
    ToleranceSource,
)
from utils.schema_types import (
    IMU_DIM,
    N_CONTACT_STATE,
    N_GAUGES,
    N_JOINTS,
    N_SAFETY_FLAGS,
    PrivilegedRecord,
)
from utils.verification_scene import CENTERLINE_TASK_OUTPUT_TOL_M

#: Ordered bodies per link. `utils.cable_mechanics.cable_body_names` returns
#: `point_count - 1` names, and the packet's `config/draft-config-v0.1.json` declares
#: `values.plant.point_count_per_link = 17`, so a link carries 16 ordered bodies.
BODIES_PER_LINK = 16

#: Internal (deformation) bodies per link. `extract_deformation_coordinates` iterates
#: `body_ids[1:]` for each link, deliberately excluding the first body: the first L1
#: body carries the shoulder ball joint and the first L2 body the elbow-side free pose,
#: and neither is an internal deformation degree of freedom.
INTERNAL_BODIES_PER_LINK = BODIES_PER_LINK - 1

#: The width of `deform_coords`. Two links times fifteen internal bodies times the three
#: components of a rotation-vector log map. It equals `values.plant.n_def = 90` in the
#: packet configuration, and the arithmetic closing is the check that this module's
#: reading of the producer is the producer's own layout.
N_DEF = 2 * INTERNAL_BODIES_PER_LINK * 3

#: One link's total length, in metres. This is the one chain constant the configuration
#: does **not** carry -- design 3.5 measured that `values.plant` holds no segment lengths
#: and no body ordering. It is `utils.cable_mechanics.CableModelConfig.link_length_m`,
#: read at source, and it is stated here as a literal rather than imported because that
#: module imports `mujoco` and invariant V18 forbids pulling it into this surface.
LINK_LENGTH_M = 0.4

#: One body's segment length. `cable_mechanics` computes it as
#: `link_length_m / len(handles.l1_body_ids)`, which is `0.4 / 16`.
SEGMENT_LENGTH_M = LINK_LENGTH_M / BODIES_PER_LINK

#: The number of points one derived centerline carries: one per ordered body across both
#: links, plus the distal point. Written as a literal because a test whose expectation is
#: a re-derivation of the function under test holds the relationship and not the value.
CENTERLINE_POINTS = 33

#: The scene-frame base point. The model's `base_ref` site sits at `(0, 0, 0.5)` and the
#: declared projection sends model x to scene x and model z to scene y.
BASE_XY_M: tuple[float, float] = (0.0, 0.5)

#: The model this chain is a synthetic instance of, echoed from
#: `values.plant.model_id` in the packet configuration.
MODEL_ID = "mujoco-cable-rod-development-candidate"

#: The fixture's own geometry-validation fields, as dotted paths into the document
#: `geometry_validation_document` returns.
FIXTURE_TOLERANCE_FIELD_PATH = "agreement.tolerance_m"
FIXTURE_MAXIMUM_DEVIATION_FIELD_PATH = "agreement.maximum_deviation_m"

#: The loud scope sentence carried inside the fixture's validation artifact.
FIXTURE_VALIDATION_SCOPE = (
    "This artifact authenticates the bytes of a synthetic fixture and nothing else. Its "
    "tolerance is the fixture's construction-exactness constant, not a measured "
    "real-data agreement, and it manufactures no tolerance for any real role payload. "
    "The adapter's production tolerance comes only from a separately approved "
    "geometry-validation artifact, which does not exist yet."
)

#: The status string the fixture's validation artifact carries.
FIXTURE_VALIDATION_STATUS = "synthetic_fixture_geometry_validation"


def coherent_render_geometry(
    *,
    producer_relative_path: str,
    producer_sha256: str,
    tolerance_artifact_relative_path: str,
    tolerance_sha256: str,
    distal_tolerance_m: float = CENTERLINE_TASK_OUTPUT_TOL_M,
    projection: str = PROJECTION_TANGENT_ADVANCE_NEGATIVE,
    model_id: str = MODEL_ID,
    base_xy_m: tuple[float, float] = BASE_XY_M,
) -> RenderGeometry:
    """Return the fixture's `render_geometry`: the declared chain, stated explicitly.

    Args:
        producer_relative_path: packet-relative path of the geometry producer the record
            hashes and never imports (`scripts/utils/cable_mechanics.py`).
        producer_sha256: that file's canonical-domain digest, measured by the caller
            against the tree the record will be read under.
        tolerance_artifact_relative_path: packet-relative path of the fixture's own
            geometry-validation artifact.
        tolerance_sha256: that artifact's canonical-domain digest.
        distal_tolerance_m: the tolerance the record declares. It defaults to the
            fixture's construction-exactness constant and **is not** a real-data
            tolerance; see the module docstring.
        projection: the declared model-to-scene projection, which also carries the
            tangent sign. Both accepted values are exposed by
            `utils.centerline_geometry` so a test can drive either.
        model_id: the configuration's `values.plant.model_id`, echoed by the record.
        base_xy_m: the scene-frame base point. It is a parameter rather than a fixed
            constant so a probe can bind the chain to a different origin -- comparing
            this derivation against the contract fixture's tip needs the two to share a
            base, or the comparison measures the half-metre offset between two origins
            instead of the thing being asked about.

    Returns:
        A `RenderGeometry` whose links are the real chain: 16 ordered bodies per link at
        `SEGMENT_LENGTH_M` each, and the contiguous zero-based `deform_coords` triplet
        layout `extract_deformation_coordinates` emits -- L1's fifteen internal bodies
        first, then L2's.

    The triplets are built from the emission rule rather than transcribed, so a change to
    the rule moves the fixture and the record together. `_require_contiguous_triplets` in
    the record parser independently refuses any layout that is not this one.
    """

    links: dict[str, LinkGeometry] = {}
    next_column = 0
    for link_id in LINK_IDS:
        triplets: list[tuple[int, int, int]] = []
        for _ in range(INTERNAL_BODIES_PER_LINK):
            triplets.append((next_column, next_column + 1, next_column + 2))
            next_column += 3
        links[link_id] = LinkGeometry(
            segment_lengths_m=(SEGMENT_LENGTH_M,) * BODIES_PER_LINK,
            deform_triplets=tuple(triplets),
        )
    if next_column != N_DEF:
        raise ValueError(
            f"the declared chain assigns {next_column} deformation columns; the "
            f"producer emits {N_DEF}"
        )

    return RenderGeometry(
        derivation_version=DERIVATION_VERSION,
        source=GeometrySource(
            producer_relative_path=PurePosixPath(producer_relative_path),
            producer_sha256=producer_sha256,
            model_id=model_id,
        ),
        planar_convention=PlanarConvention(
            base_xy_m=(float(base_xy_m[0]), float(base_xy_m[1])),
            q_true_convention=Q_TRUE_CONVENTION,
            rotation_vector_component=1,
            projection=projection,
        ),
        links=links,
        distal_tolerance_m=distal_tolerance_m,
        tolerance_source=ToleranceSource(
            artifact_relative_path=PurePosixPath(tolerance_artifact_relative_path),
            sha256=tolerance_sha256,
            maximum_deviation_field_path=FIXTURE_MAXIMUM_DEVIATION_FIELD_PATH,
            tolerance_field_path=FIXTURE_TOLERANCE_FIELD_PATH,
        ),
    )


def render_geometry_document(geometry: RenderGeometry) -> dict[str, Any]:
    """Serialise a `RenderGeometry` back into the record's JSON block.

    Args:
        geometry: the geometry to serialise.

    Returns:
        A plain JSON-ready mapping in the shape `_parse_render_geometry` accepts.

    The dataclass is the single source and the document is derived from it, rather than
    both being written out and kept in step by hand. A record built from this document
    and re-parsed must reproduce the same dataclass; that round trip is the property the
    tests pin, and it is what makes "the fixture declares what it generated under" a
    checkable statement instead of an assurance.
    """

    convention = geometry.planar_convention
    return {
        "derivation_version": geometry.derivation_version,
        "distal_tolerance_m": geometry.distal_tolerance_m,
        "links": {
            link_id: {
                "deform_triplets": [
                    list(triplet) for triplet in geometry.links[link_id].deform_triplets
                ],
                "segment_lengths_m": list(geometry.links[link_id].segment_lengths_m),
            }
            for link_id in LINK_IDS
        },
        "planar_convention": {
            "base_xy_m": [convention.base_xy_m[0], convention.base_xy_m[1]],
            "projection": convention.projection,
            "q_true_convention": convention.q_true_convention,
            "rotation_vector_component": convention.rotation_vector_component,
        },
        "source": {
            "model_id": geometry.source.model_id,
            "producer_relative_path": str(geometry.source.producer_relative_path),
            "producer_sha256": geometry.source.producer_sha256,
        },
        "tolerance_source": {
            "artifact_relative_path": str(
                geometry.tolerance_source.artifact_relative_path
            ),
            "maximum_deviation_field_path": (
                geometry.tolerance_source.maximum_deviation_field_path
            ),
            "sha256": geometry.tolerance_source.sha256,
            "tolerance_field_path": geometry.tolerance_source.tolerance_field_path,
        },
    }


def geometry_validation_document(
    maximum_deviation_m: float,
    tolerance_m: float = CENTERLINE_TASK_OUTPUT_TOL_M,
) -> dict[str, Any]:
    """Return the fixture's own geometry-validation artifact.

    Args:
        maximum_deviation_m: the agreement this fixture actually achieved, measured by
            the generator rather than asserted.
        tolerance_m: the fixture's construction-exactness tolerance.

    Returns:
        A JSON-ready mapping carrying the two fields the record's `tolerance_source`
        field paths name, plus the scope sentence and status that keep it from being
        read as a real-data result.

    Raises:
        ValueError: when the measured deviation is not a finite non-negative magnitude
            at or below the tolerance. The generator fails loudly here rather than
            emitting an artifact whose own numbers refuse each other downstream.
    """

    if not math.isfinite(maximum_deviation_m) or maximum_deviation_m < 0.0:
        raise ValueError(
            f"maximum_deviation_m must be a finite non-negative magnitude, got "
            f"{maximum_deviation_m!r}"
        )
    if not math.isfinite(tolerance_m) or tolerance_m <= 0.0:
        raise ValueError(f"tolerance_m must be finite and positive, got {tolerance_m!r}")
    if maximum_deviation_m > tolerance_m:
        raise ValueError(
            f"the fixture achieved {maximum_deviation_m!r} m, above its own "
            f"construction tolerance {tolerance_m!r} m; the generator and the "
            "derivation disagree and the artifact is not written"
        )
    return {
        "agreement": {
            "maximum_deviation_m": maximum_deviation_m,
            "tolerance_m": tolerance_m,
        },
        "scope": FIXTURE_VALIDATION_SCOPE,
        "status": FIXTURE_VALIDATION_STATUS,
    }


def coherent_deformation(n_steps: int, t_s: np.ndarray, seed: int) -> np.ndarray:
    """Return a smooth, deterministic `[T, N_DEF]` deformation field.

    Args:
        n_steps: number of control steps.
        t_s: the `[T]` control-grid time column.
        seed: selects the fixed phase offsets. It indexes a deterministic analytic
            family rather than seeding a generator, so two calls with one seed are
            bit-identical without depending on any NumPy generator's stream stability.

    Returns:
        A `[T, N_DEF]` array of per-body rotation-vector components in radians.

    The amplitude is deliberately small -- each internal body bends by at most a couple
    of milliradians -- so the chain stays a gently deformed rod rather than a coil, and
    the deformation-driven tip deflection stays the millimetre-scale quantity the
    tracking lane is about. Every column is distinct, so a derivation that read the wrong
    column or swapped the two links' blocks produces a different centerline.
    """

    if n_steps < 2:
        raise ValueError("n_steps must be >= 2")
    column = np.arange(N_DEF, dtype=float)
    phase = 0.37 * column + 0.11 * float(seed)
    frequency_hz = 0.6 + 0.013 * column
    amplitude = 2.0e-3 * (1.0 + 0.25 * np.cos(0.21 * column + 0.5 * float(seed)))
    argument = 2.0 * np.pi * frequency_hz[None, :] * t_s[:, None] + phase[None, :]
    return amplitude[None, :] * np.sin(argument)


def coherent_privileged_record(
    *,
    geometry: RenderGeometry,
    n_steps: int = 64,
    f_ctrl: float = 500.0,
    seed: int = 0,
) -> PrivilegedRecord:
    """Return a schema-B record whose tip **is** the derived centerline's distal point.

    Args:
        geometry: the declared chain this record is generated under. The same object
            must travel in the connection record, because the coherence being built here
            is coherence *with a declaration*, not with a hard-coded map.
        n_steps: number of control steps `T`.
        f_ctrl: control rate in Hz, setting the grid `dt = 1 / f_ctrl`.
        seed: selects the deterministic analytic phase family.

    Returns:
        A validated `PrivilegedRecord` whose `q_true`, `deform_coords` and
        `true_task_output` are one coherent geometric state.

    Raises:
        ValueError: when the generated record does not reproduce its own tip through
            `derive_centerline` to within `CENTERLINE_TASK_OUTPUT_TOL_M`. That check is
            the fixture's synthetic exactness oracle and it runs on every build, because
            a fixture that has silently stopped being coherent is worse than no fixture:
            every row-18 test built on it would still pass.

    `task_reference` is the same chain with the deformation removed -- the rigid nominal
    tip -- so `tracking_error` is exactly the deformation-induced deflection rather than
    an unrelated analytic signal. That keeps the tracking lane consistent with the
    geometry lane instead of merely schema-conforming.
    """

    if n_steps < 2:
        raise ValueError("n_steps must be >= 2")
    step = np.arange(n_steps)
    t_s = step / float(f_ctrl)

    frequencies = np.array([1.1, 1.7])
    amplitudes = np.array([0.35, 0.25])
    phases = np.array([0.4 + 0.17 * seed, 1.9 + 0.29 * seed])
    omega = 2.0 * np.pi * frequencies
    argument = omega[None, :] * t_s[:, None] + phases[None, :]
    q_true = amplitudes[None, :] * np.sin(argument)
    qd_true = amplitudes[None, :] * omega[None, :] * np.cos(argument)
    qdd_true = -amplitudes[None, :] * omega[None, :] ** 2 * np.sin(argument)

    deform_coords = coherent_deformation(n_steps, t_s, seed)

    centerline = derive_centerline(q_true, deform_coords, geometry)
    true_task_output = np.ascontiguousarray(centerline[:, -1, :])
    rigid = derive_centerline(q_true, np.zeros_like(deform_coords), geometry)
    task_reference = np.ascontiguousarray(rigid[:, -1, :])

    tracking_error = task_reference - true_task_output
    tracking_error_norm = np.linalg.norm(tracking_error, axis=1)

    tau_cmd = 0.2 * np.sin(
        2.0 * np.pi * 1.3 * t_s[:, None] + np.array([0.0, 0.7])[None, :]
    )
    control_effort = np.clip(tau_cmd, -0.5, 0.5)
    tau_delivered_true = control_effort.copy()

    curvature_true = _station_curvature(deform_coords, geometry)
    surface_offset_m = 0.002
    gauge_true = curvature_true * surface_offset_m * 1.0e6

    imu_true = np.column_stack(
        [
            9.81 * np.ones(n_steps),
            0.2 * np.sin(2.0 * np.pi * 1.4 * t_s),
            0.05 * np.cos(2.0 * np.pi * 1.1 * t_s),
            qd_true[:, 0] + qd_true[:, 1],
            0.01 * np.sin(2.0 * np.pi * 0.9 * t_s),
            0.01 * np.cos(2.0 * np.pi * 0.8 * t_s),
        ]
    )
    assert imu_true.shape == (n_steps, IMU_DIM)

    temperature_true = np.full((n_steps, N_GAUGES), 25.0)
    contact_state = np.zeros((n_steps, N_CONTACT_STATE))
    saturation_flag = np.abs(tau_cmd) >= 0.5
    safety_flag = np.zeros((n_steps, N_SAFETY_FLAGS), dtype=bool)

    record = PrivilegedRecord(
        step=step,
        t_s=t_s,
        q_true=q_true,
        qd_true=qd_true,
        qdd_true=qdd_true,
        tau_cmd=tau_cmd,
        tau_delivered_true=tau_delivered_true,
        deform_coords=deform_coords,
        curvature_true=curvature_true,
        gauge_true=gauge_true,
        imu_true=imu_true,
        temperature_true=temperature_true,
        contact_state=contact_state,
        task_reference=task_reference,
        true_task_output=true_task_output,
        tracking_error=tracking_error,
        tracking_error_norm=tracking_error_norm,
        control_effort=control_effort,
        saturation_flag=saturation_flag,
        safety_flag=safety_flag,
    )
    record.validate()

    deviation = distal_deviation_m(
        derive_centerline(record.q_true, record.deform_coords, geometry),
        record.true_task_output,
    )
    if not deviation <= CENTERLINE_TASK_OUTPUT_TOL_M:
        raise ValueError(
            f"the coherent fixture does not reproduce its own tip: {deviation} m, above "
            f"the construction tolerance {CENTERLINE_TASK_OUTPUT_TOL_M} m"
        )
    return record


def fixture_maximum_deviation_m(
    record: PrivilegedRecord, geometry: RenderGeometry
) -> float:
    """Return the agreement one built fixture record actually achieves.

    Args:
        record: a record from `coherent_privileged_record`.
        geometry: the chain it was generated under.

    Returns:
        The maximum per-step distal deviation in metres -- the number that goes into the
        fixture's own validation artifact, measured rather than asserted.
    """

    centerline = derive_centerline(record.q_true, record.deform_coords, geometry)
    return distal_deviation_m(centerline, record.true_task_output)


def _station_curvature(
    deform_coords: np.ndarray, geometry: RenderGeometry
) -> np.ndarray:
    """Return `[T, N_GAUGES]` curvature at the four stations, from the same deformation.

    Args:
        deform_coords: the `[T, N_DEF]` deformation field.
        geometry: the declared chain, which carries the segment lengths and the triplet
            layout the stations are read through.

    Returns:
        Curvature in 1/m at two stations per link, at roughly a quarter and three
        quarters along each link, matching `utils.schema_types`' comment on `N_GAUGES`.

    Curvature here is the declared bend of one internal body divided by its own segment
    length. It is derived from `deform_coords` rather than generated independently, so
    the fixture's strain lane cannot contradict its geometry lane the way the contract
    fixture's does. It is still synthetic: this is a consistency property of the fixture,
    not a claim that a real gauge would read this.
    """

    component = geometry.planar_convention.rotation_vector_component
    columns: list[int] = []
    lengths: list[float] = []
    for link_id in LINK_IDS:
        link = geometry.links[link_id]
        internal_count = len(link.deform_triplets)
        for fraction in (0.25, 0.75):
            index = min(int(round(fraction * internal_count)), internal_count - 1)
            columns.append(link.deform_triplets[index][component])
            lengths.append(link.segment_lengths_m[index + 1])
    if len(columns) != N_GAUGES:
        raise ValueError(
            f"the declared chain produced {len(columns)} gauge stations, expected "
            f"{N_GAUGES}"
        )
    return deform_coords[:, columns] / np.asarray(lengths, dtype=float)[None, :]


def chain_summary() -> Mapping[str, Any]:
    """Return the chain constants this fixture is built on, for a report or a test.

    Returns:
        A mapping of the measured chain facts, so a reader can check the arithmetic
        closes without reading the generator: two links of 16 bodies, 15 of them
        internal, 90 deformation columns, 0.025 m segments and 33 centerline points.
    """

    return {
        "bodies_per_link": BODIES_PER_LINK,
        "centerline_points": CENTERLINE_POINTS,
        "internal_bodies_per_link": INTERNAL_BODIES_PER_LINK,
        "link_length_m": LINK_LENGTH_M,
        "links": len(LINK_IDS),
        "n_def": N_DEF,
        "n_joints": N_JOINTS,
        "segment_length_m": SEGMENT_LENGTH_M,
    }


def require_chain_arithmetic_closes(geometry: RenderGeometry) -> None:
    """Fail loudly when the declared chain is not the producer's chain.

    Args:
        geometry: the geometry to check.

    Raises:
        ValueError: when the body count, the declared column coverage, the segment
            lengths or the centerline point count do not match the producer this fixture
            claims to be a synthetic instance of.

    The column check is a *coverage* check rather than a count, because a count is not
    reachable independently once the per-link body counts hold: two links of fifteen
    internal bodies always declare ninety columns. What a count cannot see, and this
    can, is fifteen triplets that all name the same columns.

    Design 3.5's whole reason for putting the chain in the record is that the chain is a
    property of the generated model. A fixture that quietly picks a different `n_def` or
    a different segment length is not a synthetic instance of this producer, and
    `render_geometry.links` would then describe a model the hashed producer does not
    build.
    """

    for link_id in LINK_IDS:
        link = geometry.links[link_id]
        if len(link.segment_lengths_m) != BODIES_PER_LINK:
            raise ValueError(
                f"link {link_id} declares {len(link.segment_lengths_m)} bodies, "
                f"expected {BODIES_PER_LINK}"
            )
        if len(link.deform_triplets) != INTERNAL_BODIES_PER_LINK:
            raise ValueError(
                f"link {link_id} declares {len(link.deform_triplets)} internal bodies, "
                f"expected {INTERNAL_BODIES_PER_LINK}"
            )
        for index, length in enumerate(link.segment_lengths_m):
            if length != SEGMENT_LENGTH_M:
                raise ValueError(
                    f"link {link_id} body {index} declares segment length {length} m, "
                    f"expected {SEGMENT_LENGTH_M} m"
                )
    declared: list[int] = []
    for link_id in LINK_IDS:
        for triplet in geometry.links[link_id].deform_triplets:
            declared.extend(triplet)
    if declared != list(range(N_DEF)):
        raise ValueError(
            "the declared chain does not cover the producer's deformation columns "
            f"exactly once in emission order; expected the contiguous layout 0..{N_DEF - 1}"
        )
    if centerline_point_count(geometry) != CENTERLINE_POINTS:
        raise ValueError(
            f"the declared chain produces {centerline_point_count(geometry)} centerline "
            f"points, expected {CENTERLINE_POINTS}"
        )
