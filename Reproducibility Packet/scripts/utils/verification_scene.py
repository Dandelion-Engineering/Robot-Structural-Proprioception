"""Slot-8 verification scene contract and synthetic fixture (design step 2).

This module renders `protocol/slot8-verification-artifact-v0.1.md` -- the jointly
approved Slot-8 interface contract -- into the packet's one shared surface object.
It defines the `VerificationScene` / `VerificationBundle` values that both
presentation surfaces consume, the canonical-JSON codec that makes a rendered
figure auditable after the fact, and the explicitly labeled synthetic fixture that
drives the whole interface end to end without a single real number in it.

**What this module is not.** It reads no role, no checkpoint, no config and no
split. It runs no physics, trains nothing, and derives no scientific choice. The
real-result entry path (`build_role_bundle`) is specified and mechanically
unreachable: no connection record exists in the packet, so it refuses with
`X_CONNECTION_UNAUTHORIZED` before opening anything. Building and testing this
module is not permission to connect a real result; that is design step 4 and needs
its own separate joint authorization.

**Where the facts live.** Per the design's property 1 and standing lesson 199, this
module points at the objects that already own a fact rather than copying them:

  * decisions are `utils.estimator.EstimatorOutput` values -- the live schema-D
    struct itself, not a translation of it -- and their per-decision validity is
    established by calling that class's own `validate()`;
  * class order is `utils.metrics.SOURCE_CLASS_ORDER`;
  * a scene's tracking block is established as a valid analysis-window call by
    **calling** `utils.metrics.j_5s` on the scene's own arrays and refusing on
    whatever it raises -- never by re-deriving that function's preconditions
    (design finding CN);
  * canonical JSON is `utils.protocol_p.canonical_json`.

**Two clock facts that are deliberately not bound, because binding them would
reject faithful real data.** Both were measured against live source:

  1. `controller_t_s` is never compared to `playback_t_s`. In
     `utils.online_loop.run_online_rollout` the controller's decision time for step
     *k* is read before the plant advances, while `utils.cable_plant` stamps
     `PlantStepState.t_s` from `data.time` after advancing, so for one `step` index
     the controller acts at `k * dt` and the plant record carries `(k + 1) * dt`.
     What both roles *are* pinned to is the contiguous 0-based step axis, and that
     is what scene construction requires (design finding CI).
  2. `onset_index` is carried verbatim as a label field and is never used to index
     `playback_t_s`. `utils.assignment_generator._step_index` makes the label's
     onset a control-step index (`onset_s / dt`), while `plant.t_s[k]` is
     `(k + 1) * dt`, so `playback_t_s[onset_index]` is one control interval later
     than `onset_time_s` in real data. Only `onset_time_s` is used, and only by the
     live metric.

Nothing here selects a capacity, a rung, a width, a probability threshold, an
abstention threshold or a configuration, and nothing here emits a cross-arm derived
number (design section 6 item 4, invariant V14).
"""

from __future__ import annotations

import json
import math
from dataclasses import dataclass
from typing import Any, Mapping, Sequence

import numpy as np

from utils.estimator import EstimatorOutput
from utils.metrics import SOURCE_CLASS_ORDER, j_5s
from utils.protocol_p import canonical_json

# --------------------------------------------------------------------------- #
# Exit codes (design section 4.3). Twelve fail-closed refusals plus the one
# success code; the CLI in `render_verification_scene.py` imports this mapping
# rather than restating it, so there is one definition of what each refusal means.
# --------------------------------------------------------------------------- #
X_CONNECTION_UNAUTHORIZED = "X_CONNECTION_UNAUTHORIZED"
X_SPLIT_FORBIDDEN = "X_SPLIT_FORBIDDEN"
X_ROLE_ABSENT = "X_ROLE_ABSENT"
X_ROLE_UNAUTHORIZED = "X_ROLE_UNAUTHORIZED"
X_IDENTITY_MISMATCH = "X_IDENTITY_MISMATCH"
X_PAIR_MISMATCH = "X_PAIR_MISMATCH"
X_TIMEBASE_MISMATCH = "X_TIMEBASE_MISMATCH"
X_DECISION_UNSUPPORTED = "X_DECISION_UNSUPPORTED"
X_PROVENANCE_UNRESOLVED = "X_PROVENANCE_UNRESOLVED"
X_BUNDLE_INCOMPLETE = "X_BUNDLE_INCOMPLETE"
X_ARMS_INCOMPLETE = "X_ARMS_INCOMPLETE"
X_WINDOW_UNSUPPORTED = "X_WINDOW_UNSUPPORTED"
X_SCENE_OK = "X_SCENE_OK"

EXIT_CODES: dict[str, int] = {
    X_SCENE_OK: 0,
    X_CONNECTION_UNAUTHORIZED: 3,
    X_SPLIT_FORBIDDEN: 4,
    X_ROLE_ABSENT: 5,
    X_ROLE_UNAUTHORIZED: 6,
    X_IDENTITY_MISMATCH: 7,
    X_PAIR_MISMATCH: 8,
    X_TIMEBASE_MISMATCH: 9,
    X_DECISION_UNSUPPORTED: 10,
    X_PROVENANCE_UNRESOLVED: 11,
    X_BUNDLE_INCOMPLETE: 12,
    X_ARMS_INCOMPLETE: 13,
    X_WINDOW_UNSUPPORTED: 14,
}

# --------------------------------------------------------------------------- #
# Contract constants.
# --------------------------------------------------------------------------- #
BUNDLE_VERSION = "slot8-verification-bundle-v0.1"
SUITE_KEYS: tuple[str, str] = ("C1", "S")
SYNTHETIC_FIXTURE = "SYNTHETIC_FIXTURE"
DEVELOPMENT_ONLY = "DEVELOPMENT_ONLY"
FINAL = "FINAL"
PROVENANCE_STATES: tuple[str, ...] = (SYNTHETIC_FIXTURE, DEVELOPMENT_ONLY, FINAL)
REQUIRED_SOURCE_CLASSES: tuple[str, ...] = ("structure", "actuator", "sensor")

BANNERS: dict[str, str] = {
    SYNTHETIC_FIXTURE: "SYNTHETIC - NOT A RESULT",
    DEVELOPMENT_ONLY: "DEVELOPMENT-ONLY",
    FINAL: "FINAL RESULT INPUTS",
}

FABRICATED_TRUTH_TEXT = "FABRICATED TRUTH"
NO_DECISION_TEXT = "NO DECISION YET"
UNLOCALIZED_TEXT = "UNLOCALIZED"
UNAVAILABLE_TEXT = "UNAVAILABLE"
ABSTAIN_TEXT = "ABSTAIN"
HIGH_UNKNOWN_TEXT = "HIGH UNKNOWN"

# Design section 6, items 1-3: printed by the renderer, defined once here.
DISCLAIMER_NOT_THE_QUESTION = (
    "This demo does not answer the project's research question; the confirmatory "
    "protocol does."
)
DISCLAIMER_FIXTURE_NOT_EVIDENCE = (
    "A synthetic fixture is not evidence: every number on this screen was fabricated "
    "by the packet."
)
DISCLAIMER_DEVELOPMENT_ONLY = (
    "A development-only scene is a record of the development split and nothing else: "
    "not a result, not a baseline, not a validation."
)

# The visualization tolerance named by design property 6 / invariant V16. It is
# declared here so the fixture generator and the future read-only role adapter check
# the same thing with the same number.
CENTERLINE_TASK_OUTPUT_TOL_M = 1.0e-9

# Time tolerance for "this decision lies inside the playback extent". It matches the
# tolerance `utils.metrics.j_5s` uses for grid-alignment so the two layers do not
# disagree at the last significant digit.
_TIME_TOL_S = 1.0e-9

_SENTINEL_ABSENT = "NONE-SYNTHETIC-FIXTURE"

_NON_FINITE_DECODINGS: dict[str, float] = {
    "Infinity": math.inf,
    "-Infinity": -math.inf,
    "NaN": math.nan,
}
NON_FINITE_TOKENS: tuple[str, ...] = ("Infinity", "-Infinity", "NaN")


class VerificationSceneError(RuntimeError):
    """A fail-closed refusal carrying the section-4.3 exit-code name that named it."""

    def __init__(self, code: str, message: str) -> None:
        if code not in EXIT_CODES or code == X_SCENE_OK:
            raise ValueError(f"{code!r} is not one of the twelve refusal codes")
        super().__init__(f"{code}: {message}")
        self.code = code


class VerificationDecodeError(ValueError):
    """A loud codec failure: the document is not a scene this module wrote."""


# --------------------------------------------------------------------------- #
# The non-finite float wire encoding (design section 4.1, invariant V19).
# --------------------------------------------------------------------------- #
def encode_float(value: float) -> float | str:
    """Encode one float position: a JSON number when finite, else a JSON string.

    Args:
        value: any IEEE-754 double, including the schema's `+inf` and `NaN` defaults.

    Returns:
        The float itself when finite, otherwise exactly one of `"Infinity"`,
        `"-Infinity"`, `"NaN"`. The mapping is total and exactly invertible because a
        finite float never encodes as a string, which is what lets `allow_nan=False`
        stay on without the scene becoming unwritable.
    """

    number = float(value)
    if math.isfinite(number):
        return number
    if math.isnan(number):
        return "NaN"
    return "Infinity" if number > 0.0 else "-Infinity"


def decode_float(value: Any) -> float:
    """Decode one float position, refusing anything that is not a permitted form.

    Args:
        value: a decoded JSON value taken from a typed float position.

    Returns:
        The float it denotes.

    Raises:
        VerificationDecodeError: on any other string, on a bool, on a non-finite
            JSON number, or on any non-numeric type. Never a silent zero.
    """

    if isinstance(value, bool):
        raise VerificationDecodeError("a boolean is not a float position")
    if isinstance(value, str):
        try:
            return _NON_FINITE_DECODINGS[value]
        except KeyError:
            raise VerificationDecodeError(
                f"{value!r} is not one of the permitted non-finite encodings "
                f"{NON_FINITE_TOKENS}"
            ) from None
    if isinstance(value, (int, float)):
        number = float(value)
        if not math.isfinite(number):
            raise VerificationDecodeError("a JSON number in a float position must be finite")
        return number
    raise VerificationDecodeError(f"{type(value).__name__} is not a float position")


def _refuse_bare_constant(token: str) -> float:
    """`json.loads` `parse_constant` hook: refuse the bare non-standard tokens."""

    raise VerificationDecodeError(
        f"bare non-standard JSON token {token!r}; scenes encode non-finite floats as "
        f"the quoted strings {NON_FINITE_TOKENS}"
    )


def loads_strict(text: str) -> Any:
    """Parse scene/bundle JSON, refusing Python's bare `NaN`/`Infinity` extensions.

    `json.loads` has no `allow_nan` option -- that belongs to `json.dumps` -- and its
    default loader accepts the three bare tokens. `parse_constant` is the hook that
    fires on exactly them.
    """

    return json.loads(text, parse_constant=_refuse_bare_constant)


def _encode_array(array: np.ndarray) -> list:
    """Encode a float array of any rank as nested lists under the float codec."""

    values = np.asarray(array, dtype=float)
    if values.ndim == 1:
        return [encode_float(item) for item in values.tolist()]
    return [_encode_array(row) for row in values]


def _decode_array(payload: Any, *, name: str) -> np.ndarray:
    """Decode nested lists of encoded floats into a float64 array."""

    if not isinstance(payload, list):
        raise VerificationDecodeError(f"{name} must be a JSON array")
    if payload and isinstance(payload[0], list):
        return np.asarray([_decode_array(row, name=name) for row in payload], dtype=float)
    return np.asarray([decode_float(item) for item in payload], dtype=float)


def _decode_int_array(payload: Any, *, name: str) -> np.ndarray:
    """Decode a JSON array of integers into an int64 array."""

    if not isinstance(payload, list):
        raise VerificationDecodeError(f"{name} must be a JSON array")
    values: list[int] = []
    for item in payload:
        if isinstance(item, bool) or not isinstance(item, int):
            raise VerificationDecodeError(f"{name} must contain JSON integers")
        values.append(int(item))
    return np.asarray(values, dtype=np.int64)


# --------------------------------------------------------------------------- #
# The scene value types.
# --------------------------------------------------------------------------- #
@dataclass(frozen=True)
class LabelFields:
    """The exact schema-D `labels` struct, carried verbatim.

    The eight field *names* are the machine schema's; a test pins them by equality
    against `schema/schema.json` rather than adopting whatever this class happens to
    declare. The value checks below are the minimum the renderer needs in order to
    draw the struct honestly; the authority on a real `labels` payload remains
    `utils.role_contract.validate_role_payload`, which needs an NPZ payload and a
    validated config that the scene layer does not have and must not acquire.
    """

    source_class: str
    subtype: str
    location: int
    severity: float
    onset_index: int
    onset_time_s: float
    compound_flag: bool
    ood_flag: bool

    def validate(self) -> None:
        """Fail loudly if the label struct cannot be rendered honestly."""

        if self.source_class not in SOURCE_CLASS_ORDER:
            raise ValueError(f"source_class must be one of {SOURCE_CLASS_ORDER}")
        if not isinstance(self.subtype, str) or not self.subtype:
            raise ValueError("subtype must be a nonempty string")
        for name in ("location", "onset_index"):
            value = getattr(self, name)
            if isinstance(value, bool) or not isinstance(value, (int, np.integer)):
                raise ValueError(f"{name} must be an integer")
            if int(value) < -1:
                raise ValueError(f"{name} must be >= -1")
        if not math.isfinite(float(self.severity)):
            raise ValueError("severity must be finite")
        if not math.isfinite(float(self.onset_time_s)) or float(self.onset_time_s) < 0.0:
            raise ValueError("onset_time_s must be finite and non-negative")
        for name in ("compound_flag", "ood_flag"):
            if not isinstance(getattr(self, name), (bool, np.bool_)):
                raise ValueError(f"{name} must be boolean")


@dataclass(frozen=True)
class BodyChange:
    """One menu entry: its identity, its display label, and the schema-D label."""

    case_id: str
    label: str
    change: LabelFields

    def validate(self) -> None:
        """Fail loudly if the menu entry cannot be rendered."""

        if not isinstance(self.case_id, str) or not self.case_id:
            raise ValueError("case_id must be a nonempty string")
        if not isinstance(self.label, str) or not self.label:
            raise ValueError("label must be a nonempty string")
        self.change.validate()


@dataclass(frozen=True)
class Thresholds:
    """Display/audit reference thresholds. Never derived and never defaulted."""

    abstain_threshold: float
    unknown_threshold: float

    def validate(self) -> None:
        """Fail loudly if either threshold is unusable as a display reference."""

        for name in ("abstain_threshold", "unknown_threshold"):
            value = float(getattr(self, name))
            if not math.isfinite(value):
                raise ValueError(f"{name} must be finite")


@dataclass(frozen=True)
class ArmIdentity:
    """Per-arm provenance identities. Sentinel strings on the synthetic path."""

    run_id: str
    pair_id: str
    checkpoint_relative_path: str
    checkpoint_sha256: str
    role_index_sha256: tuple[tuple[str, str], ...] = ()
    role_payload_sha256: tuple[tuple[str, str], ...] = ()


@dataclass(frozen=True)
class Provenance:
    """What the picture is made of (design 4.3 / requirement A5).

    `state` is computed by the construction path and is never accepted from a
    caller: a caller-supplied provenance label is a label that can lie.
    """

    state: str
    connection_record_id: str
    connection_record_sha256: str
    config_identity: str
    config_sha256: str
    split: str
    roles_read: tuple[str, ...]
    arms: Mapping[str, ArmIdentity]
    fixture_seed: int | None = None

    def validate(self) -> None:
        """Fail loudly if the provenance struct is not one of the three states."""

        if self.state not in PROVENANCE_STATES:
            raise ValueError(f"provenance state must be one of {PROVENANCE_STATES}")
        if tuple(sorted(self.arms)) != tuple(sorted(SUITE_KEYS)):
            raise ValueError(f"provenance must carry exactly the arms {SUITE_KEYS}")


@dataclass(frozen=True)
class Tracking:
    """The complete argument set `utils.metrics.j_5s` takes, minus the shared grid."""

    task_reference: np.ndarray
    true_task_output: np.ndarray
    window_s: float


@dataclass(frozen=True)
class Arm:
    """One suite's side of the comparison, on the scene's one playback grid.

    `controller_step` and `controller_t_s` are the schema-D `controller_logs` axes.
    Construction binds `controller_mode` to `controller_step` and deliberately does
    not compare `controller_t_s` to `playback_t_s` -- see the module docstring.
    """

    suite: str
    centerline_xy: np.ndarray
    decisions: tuple[EstimatorOutput, ...]
    tracking: Tracking
    controller_step: np.ndarray
    controller_t_s: np.ndarray
    controller_mode: tuple[str, ...]


@dataclass(frozen=True)
class VerificationScene:
    """The complete, serializable description of exactly one side-by-side comparison."""

    bundle_version: str
    provenance: Provenance
    body_change: BodyChange
    playback_t_s: np.ndarray
    arms: Mapping[str, Arm]
    truth: LabelFields | None
    thresholds: Thresholds

    @property
    def case_id(self) -> str:
        """The bundle key this scene is filed under."""

        return self.body_change.case_id

    @property
    def n_frames(self) -> int:
        """The length of the one shared playback grid."""

        return int(np.asarray(self.playback_t_s).shape[0])

    @property
    def window_s(self) -> float:
        """The scene-level analysis window both arms agree on (checked at build)."""

        return float(self.arms[SUITE_KEYS[0]].tracking.window_s)


@dataclass(frozen=True)
class VerificationBundle:
    """An ordered, non-empty mapping of unique `case_id` to scene: the whole menu."""

    bundle_version: str
    provenance_state: str
    scenes: Mapping[str, VerificationScene]

    @property
    def case_ids(self) -> tuple[str, ...]:
        """Menu order, which is bundle order."""

        return tuple(self.scenes)


# --------------------------------------------------------------------------- #
# Construction-time validation (design 4.1 properties 1-8).
# --------------------------------------------------------------------------- #
def _require(condition: bool, code: str, message: str) -> None:
    """Refuse with a named section-4.3 exit code when `condition` is false."""

    if not condition:
        raise VerificationSceneError(code, message)


def _validate_arm_axes(scene_arms: Mapping[str, Arm], n_frames: int) -> None:
    """Bind every frame-bearing array in both arms to the one playback grid."""

    for key in SUITE_KEYS:
        arm = scene_arms[key]
        _require(
            arm.suite == key,
            X_ARMS_INCOMPLETE,
            f"arm filed under {key!r} declares suite {arm.suite!r}",
        )
        centerline = np.asarray(arm.centerline_xy, dtype=float)
        _require(
            centerline.ndim == 3 and centerline.shape[0] == n_frames and centerline.shape[2] == 2,
            X_TIMEBASE_MISMATCH,
            f"arm {key} centerline_xy must be [T,N,2] with T={n_frames}, "
            f"got {centerline.shape}",
        )
        _require(
            centerline.shape[1] >= 2,
            X_TIMEBASE_MISMATCH,
            f"arm {key} centerline_xy must carry at least two body points",
        )
        for name in ("task_reference", "true_task_output"):
            array = np.asarray(getattr(arm.tracking, name), dtype=float)
            _require(
                array.shape == (n_frames, 2),
                X_TIMEBASE_MISMATCH,
                f"arm {key} {name} must be [T,2] with T={n_frames}, got {array.shape}",
            )
        step = np.asarray(arm.controller_step)
        _require(
            np.issubdtype(step.dtype, np.integer)
            and step.ndim == 1
            and step.shape[0] == n_frames
            and np.array_equal(step, np.arange(n_frames)),
            X_TIMEBASE_MISMATCH,
            f"arm {key} controller_logs.step must be the contiguous 0-based grid of "
            f"length {n_frames}",
        )
        controller_t = np.asarray(arm.controller_t_s, dtype=float)
        _require(
            controller_t.shape == (n_frames,) and bool(np.all(np.isfinite(controller_t))),
            X_TIMEBASE_MISMATCH,
            f"arm {key} controller_logs.t_s must be a finite [T] array with T={n_frames}",
        )
        _require(
            n_frames < 2 or bool(np.all(np.diff(controller_t) > 0.0)),
            X_TIMEBASE_MISMATCH,
            f"arm {key} controller_logs.t_s must be strictly increasing",
        )
        _require(
            len(arm.controller_mode) == n_frames
            and all(isinstance(mode, str) and mode for mode in arm.controller_mode),
            X_TIMEBASE_MISMATCH,
            f"arm {key} controller_mode must be {n_frames} nonempty strings",
        )


def _validate_decisions(arm: Arm, key: str, playback_t_s: np.ndarray) -> None:
    """Require a non-empty, strictly ordered decision axis inside the playback extent."""

    _require(
        len(arm.decisions) >= 1,
        X_DECISION_UNSUPPORTED,
        f"arm {key} carries no decision; the live role contract refuses an "
        f"estimator_outputs payload with none",
    )
    first_time = float(playback_t_s[0])
    last_time = float(playback_t_s[-1])
    previous_step = -1
    previous_time = -math.inf
    for index, decision in enumerate(arm.decisions):
        try:
            decision.validate()
        except ValueError as exc:
            raise VerificationSceneError(
                X_DECISION_UNSUPPORTED,
                f"arm {key} decision {index} violates the schema-D contract: {exc}",
            ) from exc
        step = int(decision.step)
        time_s = float(decision.decision_time_s)
        _require(
            step > previous_step and time_s > previous_time,
            X_DECISION_UNSUPPORTED,
            f"arm {key} decision axes must be strictly increasing at index {index}",
        )
        _require(
            first_time - _TIME_TOL_S <= time_s <= last_time + _TIME_TOL_S,
            X_DECISION_UNSUPPORTED,
            f"arm {key} decision {index} at t={time_s} lies outside the playback "
            f"extent [{first_time}, {last_time}]",
        )
        previous_step = step
        previous_time = time_s


def _validate_tracking_window(scene_arms: Mapping[str, Arm], playback_t_s, onset_time_s) -> None:
    """Establish each arm's tracking block by CALLING the live metric (finding CN).

    The section-4.3 `X_WINDOW_UNSUPPORTED` list is explicitly non-exhaustive: this
    routine delegates to `utils.metrics.j_5s` and refuses on whatever it raises, so a
    later change to that function's preconditions cannot leave a stale copy behind.
    """

    for key in SUITE_KEYS:
        arm = scene_arms[key]
        try:
            j_5s(
                playback_t_s,
                arm.tracking.task_reference,
                arm.tracking.true_task_output,
                float(onset_time_s),
                window_s=float(arm.tracking.window_s),
            )
        except ValueError as exc:
            raise VerificationSceneError(
                X_WINDOW_UNSUPPORTED,
                f"arm {key} tracking block is not a valid utils.metrics.j_5s call "
                f"at onset {float(onset_time_s)} s: {exc}",
            ) from exc


def validate_scene(scene: VerificationScene) -> None:
    """Refuse any scene a surface must not be allowed to draw.

    Args:
        scene: an assembled `VerificationScene`.

    Raises:
        VerificationSceneError: with the section-4.3 code naming the refusal.
    """

    _require(
        scene.bundle_version == BUNDLE_VERSION,
        X_BUNDLE_INCOMPLETE,
        f"scene declares bundle_version {scene.bundle_version!r}, expected "
        f"{BUNDLE_VERSION!r}",
    )
    try:
        scene.provenance.validate()
    except ValueError as exc:
        raise VerificationSceneError(X_PROVENANCE_UNRESOLVED, str(exc)) from exc
    try:
        scene.body_change.validate()
        scene.thresholds.validate()
        if scene.truth is not None:
            scene.truth.validate()
    except ValueError as exc:
        raise VerificationSceneError(X_BUNDLE_INCOMPLETE, str(exc)) from exc

    _require(
        tuple(sorted(scene.arms)) == tuple(sorted(SUITE_KEYS)),
        X_ARMS_INCOMPLETE,
        f"a scene carries exactly the two arms {SUITE_KEYS}, got {tuple(scene.arms)}",
    )

    playback = np.asarray(scene.playback_t_s, dtype=float)
    # The grid's own shape rules -- length, uniformity, monotonicity, finiteness --
    # belong to `j_5s` and are delegated below (finding CN). Only its rank is checked
    # here, because every axis-binding comparison that follows needs one.
    _require(
        playback.ndim == 1 and playback.shape[0] >= 1,
        X_TIMEBASE_MISMATCH,
        "playback_t_s must be a non-empty 1-D grid",
    )
    n_frames = int(playback.shape[0])
    _validate_arm_axes(scene.arms, n_frames)

    reference = np.asarray(scene.arms["C1"].tracking.task_reference, dtype=float)
    other_reference = np.asarray(scene.arms["S"].tracking.task_reference, dtype=float)
    _require(
        np.array_equal(reference, other_reference),
        X_PAIR_MISMATCH,
        "both arms must replay the same task_reference",
    )
    _require(
        float(scene.arms["C1"].tracking.window_s) == float(scene.arms["S"].tracking.window_s),
        X_PAIR_MISMATCH,
        "both arms must agree on the analysis window the comparison is read over",
    )
    pair_ids = {scene.provenance.arms[key].pair_id for key in SUITE_KEYS}
    _require(
        len(pair_ids) == 1,
        X_PAIR_MISMATCH,
        f"the two arms must belong to one pair, got {sorted(pair_ids)}",
    )

    for key in SUITE_KEYS:
        _validate_decisions(scene.arms[key], key, playback)

    _validate_tracking_window(scene.arms, playback, scene.body_change.change.onset_time_s)


def validate_bundle(bundle: VerificationBundle) -> None:
    """Refuse an incomplete menu, or one whose scenes do not agree on their context."""

    _require(
        bundle.bundle_version == BUNDLE_VERSION,
        X_BUNDLE_INCOMPLETE,
        f"bundle declares version {bundle.bundle_version!r}",
    )
    _require(len(bundle.scenes) >= 1, X_BUNDLE_INCOMPLETE, "a bundle is non-empty")
    for case_id, scene in bundle.scenes.items():
        _require(
            case_id == scene.body_change.case_id,
            X_BUNDLE_INCOMPLETE,
            f"scene filed under {case_id!r} declares case_id "
            f"{scene.body_change.case_id!r}",
        )
        validate_scene(scene)
    present = {scene.body_change.change.source_class for scene in bundle.scenes.values()}
    missing = [name for name in REQUIRED_SOURCE_CLASSES if name not in present]
    _require(
        not missing,
        X_BUNDLE_INCOMPLETE,
        f"a bundle must contain at least one {'/'.join(REQUIRED_SOURCE_CLASSES)} case; "
        f"missing {missing}",
    )
    states = {scene.provenance.state for scene in bundle.scenes.values()}
    _require(
        states == {bundle.provenance_state},
        X_PROVENANCE_UNRESOLVED,
        f"every scene in a bundle carries one provenance state; got {sorted(states)} "
        f"under bundle state {bundle.provenance_state!r}",
    )
    for name in ("config_identity", "config_sha256", "connection_record_id",
                 "connection_record_sha256", "split"):
        values = {getattr(scene.provenance, name) for scene in bundle.scenes.values()}
        _require(
            len(values) == 1,
            X_PROVENANCE_UNRESOLVED,
            f"every scene in a bundle agrees on {name}; got {sorted(values)}",
        )
    thresholds = {
        (scene.thresholds.abstain_threshold, scene.thresholds.unknown_threshold)
        for scene in bundle.scenes.values()
    }
    _require(
        len(thresholds) == 1,
        X_BUNDLE_INCOMPLETE,
        f"every scene in a bundle agrees on its thresholds; got {sorted(thresholds)}",
    )


def require_distal_point_matches_task_output(
    arm: Arm, *, tolerance: float = CENTERLINE_TASK_OUTPUT_TOL_M
) -> None:
    """Require the drawn body's distal point to be the recorded task output.

    Design property 6 assigns this check to the future read-only role adapter, and
    the section-4.1 field table states it as a property of `arms[k].body`. The
    section-4.3 exit-code table names no code for a geometry mismatch, so this
    routine raises a plain `ValueError` rather than inventing one: the fixture
    generator calls it on every arm it builds, and the adapter round is where the
    refusal code is assigned. Flagged to the reviewer rather than resolved here.

    Args:
        arm: the arm whose centerline and tracking block are being checked.
        tolerance: maximum permitted per-sample Euclidean deviation, in metres.
    """

    centerline = np.asarray(arm.centerline_xy, dtype=float)
    output = np.asarray(arm.tracking.true_task_output, dtype=float)
    deviation = float(np.max(np.linalg.norm(centerline[:, -1, :] - output, axis=1)))
    if not deviation <= tolerance:
        raise ValueError(
            f"arm {arm.suite} distal centerline point departs from true_task_output by "
            f"{deviation} m, above the declared visualization tolerance {tolerance} m"
        )


# --------------------------------------------------------------------------- #
# Frame semantics shared by both surfaces.
# --------------------------------------------------------------------------- #
def require_frame(scene: VerificationScene, frame: Any) -> int:
    """Return `frame` as an index into the scene's playback grid, or refuse.

    The painter never clamps: a frame outside the grid is a defect in the wrapper
    that produced it, and clamping would show the wrong instant while every panel
    still looked consistent (design 4.6).
    """

    if isinstance(frame, bool) or not isinstance(frame, (int, np.integer)):
        raise VerificationSceneError(
            X_TIMEBASE_MISMATCH, f"frame must be an integer index, got {frame!r}"
        )
    index = int(frame)
    if not 0 <= index < scene.n_frames:
        raise VerificationSceneError(
            X_TIMEBASE_MISMATCH,
            f"frame {index} is outside the playback grid [0, {scene.n_frames - 1}]",
        )
    return index


def derived_frame(scene: VerificationScene) -> int:
    """The scripted still's frame: the control sample at `onset + window_s`.

    It is derived from the scene rather than passed in, so the scripted surface stays
    a function of the bundle alone (design 4.6). Its existence is guaranteed by the
    accepted `j_5s` call in `validate_scene`, which already required a sample there.
    """

    playback = np.asarray(scene.playback_t_s, dtype=float)
    target = float(scene.body_change.change.onset_time_s) + scene.window_s
    matches = np.flatnonzero(np.abs(playback - target) <= _TIME_TOL_S)
    if matches.size != 1:
        raise VerificationSceneError(
            X_WINDOW_UNSUPPORTED,
            f"the playback grid does not carry exactly one control sample at "
            f"onset + window_s = {target}",
        )
    return int(matches[0])


def decision_at_frame(scene: VerificationScene, suite: str, frame: int) -> EstimatorOutput | None:
    """The greatest decision no later than `playback_t_s[frame]`, or `None`.

    `None` is the `NO DECISION YET` state. Nothing from a later decision is borrowed
    (design property 4).
    """

    index = require_frame(scene, frame)
    frame_time = float(np.asarray(scene.playback_t_s, dtype=float)[index])
    visible: EstimatorOutput | None = None
    for decision in scene.arms[suite].decisions:
        if float(decision.decision_time_s) <= frame_time + _TIME_TOL_S:
            visible = decision
        else:
            break
    return visible


def banner_text(state: str) -> str:
    """The provenance banner every surface prints for one state."""

    try:
        return BANNERS[state]
    except KeyError:
        raise VerificationSceneError(
            X_PROVENANCE_UNRESOLVED, f"no banner is defined for state {state!r}"
        ) from None


# --------------------------------------------------------------------------- #
# Canonical JSON codec (invariants V12, V19).
# --------------------------------------------------------------------------- #
def _label_to_json(label: LabelFields) -> dict:
    """Encode the schema-D label struct."""

    return {
        "source_class": label.source_class,
        "subtype": label.subtype,
        "location": int(label.location),
        "severity": encode_float(label.severity),
        "onset_index": int(label.onset_index),
        "onset_time_s": encode_float(label.onset_time_s),
        "compound_flag": bool(label.compound_flag),
        "ood_flag": bool(label.ood_flag),
    }


def _label_from_json(payload: Any) -> LabelFields:
    """Decode the schema-D label struct."""

    if not isinstance(payload, dict):
        raise VerificationDecodeError("label struct must be a JSON object")
    return LabelFields(
        source_class=str(payload["source_class"]),
        subtype=str(payload["subtype"]),
        location=int(payload["location"]),
        severity=decode_float(payload["severity"]),
        onset_index=int(payload["onset_index"]),
        onset_time_s=decode_float(payload["onset_time_s"]),
        compound_flag=bool(payload["compound_flag"]),
        ood_flag=bool(payload["ood_flag"]),
    )


def _decision_to_json(decision: EstimatorOutput) -> dict:
    """Encode one schema-D `estimator_outputs` row, field for field."""

    return {
        "step": int(decision.step),
        "decision_time_s": encode_float(decision.decision_time_s),
        "p_class": [encode_float(value) for value in np.asarray(decision.p_class).tolist()],
        "unknown_score": encode_float(decision.unknown_score),
        "abstain_decision": bool(decision.abstain_decision),
        "location_out": int(decision.location_out),
        "severity_out": encode_float(decision.severity_out),
        "severity_uncertainty": encode_float(decision.severity_uncertainty),
        "detection_time_s": encode_float(decision.detection_time_s),
    }


def _decision_from_json(payload: Any) -> EstimatorOutput:
    """Decode one schema-D `estimator_outputs` row."""

    if not isinstance(payload, dict):
        raise VerificationDecodeError("decision must be a JSON object")
    return EstimatorOutput(
        step=int(payload["step"]),
        decision_time_s=decode_float(payload["decision_time_s"]),
        p_class=np.asarray([decode_float(value) for value in payload["p_class"]], dtype=float),
        unknown_score=decode_float(payload["unknown_score"]),
        abstain_decision=bool(payload["abstain_decision"]),
        location_out=int(payload["location_out"]),
        severity_out=decode_float(payload["severity_out"]),
        severity_uncertainty=decode_float(payload["severity_uncertainty"]),
        detection_time_s=decode_float(payload["detection_time_s"]),
    )


def _identity_to_json(identity: ArmIdentity) -> dict:
    """Encode one arm's provenance identities."""

    return {
        "run_id": identity.run_id,
        "pair_id": identity.pair_id,
        "checkpoint_relative_path": identity.checkpoint_relative_path,
        "checkpoint_sha256": identity.checkpoint_sha256,
        "role_index_sha256": {role: digest for role, digest in identity.role_index_sha256},
        "role_payload_sha256": {role: digest for role, digest in identity.role_payload_sha256},
    }


def _identity_from_json(payload: Any) -> ArmIdentity:
    """Decode one arm's provenance identities."""

    if not isinstance(payload, dict):
        raise VerificationDecodeError("arm identity must be a JSON object")
    return ArmIdentity(
        run_id=str(payload["run_id"]),
        pair_id=str(payload["pair_id"]),
        checkpoint_relative_path=str(payload["checkpoint_relative_path"]),
        checkpoint_sha256=str(payload["checkpoint_sha256"]),
        role_index_sha256=tuple(sorted(payload["role_index_sha256"].items())),
        role_payload_sha256=tuple(sorted(payload["role_payload_sha256"].items())),
    )


def _arm_to_json(arm: Arm) -> dict:
    """Encode one arm."""

    return {
        "suite": arm.suite,
        "centerline_xy": _encode_array(arm.centerline_xy),
        "decisions": [_decision_to_json(decision) for decision in arm.decisions],
        "tracking": {
            "task_reference": _encode_array(arm.tracking.task_reference),
            "true_task_output": _encode_array(arm.tracking.true_task_output),
            "window_s": encode_float(arm.tracking.window_s),
        },
        "controller_step": [int(value) for value in np.asarray(arm.controller_step).tolist()],
        "controller_t_s": _encode_array(arm.controller_t_s),
        "controller_mode": list(arm.controller_mode),
    }


def _arm_from_json(payload: Any) -> Arm:
    """Decode one arm."""

    if not isinstance(payload, dict):
        raise VerificationDecodeError("arm must be a JSON object")
    tracking = payload["tracking"]
    return Arm(
        suite=str(payload["suite"]),
        centerline_xy=_decode_array(payload["centerline_xy"], name="centerline_xy"),
        decisions=tuple(_decision_from_json(row) for row in payload["decisions"]),
        tracking=Tracking(
            task_reference=_decode_array(tracking["task_reference"], name="task_reference"),
            true_task_output=_decode_array(tracking["true_task_output"], name="true_task_output"),
            window_s=decode_float(tracking["window_s"]),
        ),
        controller_step=_decode_int_array(payload["controller_step"], name="controller_step"),
        controller_t_s=_decode_array(payload["controller_t_s"], name="controller_t_s"),
        controller_mode=tuple(str(value) for value in payload["controller_mode"]),
    )


def scene_to_json(scene: VerificationScene) -> dict:
    """Encode one scene as a canonical-JSON-ready object."""

    provenance = scene.provenance
    return {
        "bundle_version": scene.bundle_version,
        "provenance": {
            "state": provenance.state,
            "connection_record_id": provenance.connection_record_id,
            "connection_record_sha256": provenance.connection_record_sha256,
            "config_identity": provenance.config_identity,
            "config_sha256": provenance.config_sha256,
            "split": provenance.split,
            "roles_read": list(provenance.roles_read),
            "fixture_seed": provenance.fixture_seed,
            "arms": {key: _identity_to_json(provenance.arms[key]) for key in SUITE_KEYS},
        },
        "body_change": {
            "case_id": scene.body_change.case_id,
            "label": scene.body_change.label,
            "change": _label_to_json(scene.body_change.change),
        },
        "playback_t_s": _encode_array(scene.playback_t_s),
        "arms": {key: _arm_to_json(scene.arms[key]) for key in SUITE_KEYS},
        "truth": None if scene.truth is None else _label_to_json(scene.truth),
        "thresholds": {
            "abstain_threshold": encode_float(scene.thresholds.abstain_threshold),
            "unknown_threshold": encode_float(scene.thresholds.unknown_threshold),
        },
    }


def scene_from_json(payload: Any) -> VerificationScene:
    """Decode one scene.

    Decoding is an audit codec, not a construction path: no CLI argument reads a
    bundle or scene document, so a hand-written document cannot enter a surface
    through the executable. `validate_scene` still runs on everything it returns.
    """

    if not isinstance(payload, dict):
        raise VerificationDecodeError("scene must be a JSON object")
    provenance_payload = payload["provenance"]
    seed = provenance_payload["fixture_seed"]
    scene = VerificationScene(
        bundle_version=str(payload["bundle_version"]),
        provenance=Provenance(
            state=str(provenance_payload["state"]),
            connection_record_id=str(provenance_payload["connection_record_id"]),
            connection_record_sha256=str(provenance_payload["connection_record_sha256"]),
            config_identity=str(provenance_payload["config_identity"]),
            config_sha256=str(provenance_payload["config_sha256"]),
            split=str(provenance_payload["split"]),
            roles_read=tuple(str(role) for role in provenance_payload["roles_read"]),
            arms={
                key: _identity_from_json(provenance_payload["arms"][key]) for key in SUITE_KEYS
            },
            fixture_seed=None if seed is None else int(seed),
        ),
        body_change=BodyChange(
            case_id=str(payload["body_change"]["case_id"]),
            label=str(payload["body_change"]["label"]),
            change=_label_from_json(payload["body_change"]["change"]),
        ),
        playback_t_s=_decode_array(payload["playback_t_s"], name="playback_t_s"),
        arms={key: _arm_from_json(payload["arms"][key]) for key in SUITE_KEYS},
        truth=None if payload["truth"] is None else _label_from_json(payload["truth"]),
        thresholds=Thresholds(
            abstain_threshold=decode_float(payload["thresholds"]["abstain_threshold"]),
            unknown_threshold=decode_float(payload["thresholds"]["unknown_threshold"]),
        ),
    )
    validate_scene(scene)
    return scene


def bundle_to_json(bundle: VerificationBundle) -> dict:
    """Encode the whole menu."""

    return {
        "bundle_version": bundle.bundle_version,
        "provenance_state": bundle.provenance_state,
        "case_order": list(bundle.scenes),
        "scenes": {case_id: scene_to_json(scene) for case_id, scene in bundle.scenes.items()},
    }


def bundle_from_json(payload: Any) -> VerificationBundle:
    """Decode the whole menu, preserving menu order from `case_order`."""

    if not isinstance(payload, dict):
        raise VerificationDecodeError("bundle must be a JSON object")
    order = [str(case_id) for case_id in payload["case_order"]]
    scenes_payload = payload["scenes"]
    if sorted(order) != sorted(scenes_payload):
        raise VerificationDecodeError("case_order and scenes disagree about the menu")
    bundle = VerificationBundle(
        bundle_version=str(payload["bundle_version"]),
        provenance_state=str(payload["provenance_state"]),
        scenes={case_id: scene_from_json(scenes_payload[case_id]) for case_id in order},
    )
    validate_bundle(bundle)
    return bundle


def canonical_scene_text(scene: VerificationScene) -> str:
    """One scene under the packet's canonical-JSON discipline."""

    return canonical_json(scene_to_json(scene))


def canonical_bundle_text(bundle: VerificationBundle) -> str:
    """The whole bundle under the packet's canonical-JSON discipline."""

    return canonical_json(bundle_to_json(bundle))


# --------------------------------------------------------------------------- #
# The synthetic fixture (design 4.4).
# --------------------------------------------------------------------------- #
FIXTURE_CONTROL_DT_S = 0.05
FIXTURE_N_FRAMES = 141
FIXTURE_ONSET_TIME_S = 1.0
FIXTURE_ONSET_INDEX = 20
FIXTURE_WINDOW_S = 5.0
FIXTURE_LINK_LENGTHS_M: tuple[float, float] = (0.25, 0.25)
FIXTURE_ABSTAIN_THRESHOLD = 0.5
FIXTURE_UNKNOWN_THRESHOLD = 0.6
FIXTURE_DECISION_TIMES_S: tuple[float, ...] = (1.5, 3.0)
FIXTURE_DECISION_STEPS: tuple[int, ...] = (30, 60)


def fixture_playback_grid() -> np.ndarray:
    """The fixture's one shared playback grid, on the live plant's stamping convention.

    `plant.t_s[k]` is `(k + 1) * dt` because `utils.cable_plant` stamps `data.time`
    after advancing, so the grid starts at one control interval rather than at zero.
    The onset lands exactly on sample 19 and `onset + window_s` exactly on sample 119.
    """

    return (np.arange(FIXTURE_N_FRAMES, dtype=float) + 1.0) * FIXTURE_CONTROL_DT_S


def fixture_controller_grid() -> np.ndarray:
    """The fixture's controller clock: the pre-advance decision time `k * dt`.

    One control interval earlier than `playback_t_s`, which is the live loop's actual
    convention and is exactly what scene construction must accept without complaint.
    """

    return np.arange(FIXTURE_N_FRAMES, dtype=float) * FIXTURE_CONTROL_DT_S


def _forward_kinematics(q0: np.ndarray, q1: np.ndarray) -> np.ndarray:
    """Planar two-link centerline `[T,5,2]`: base, mid-link-1, joint, mid-link-2, tip."""

    length_1, length_2 = FIXTURE_LINK_LENGTHS_M
    absolute_1 = q0
    absolute_2 = q0 + q1
    zeros = np.zeros_like(q0)
    joint_x = length_1 * np.cos(absolute_1)
    joint_y = length_1 * np.sin(absolute_1)
    tip_x = joint_x + length_2 * np.cos(absolute_2)
    tip_y = joint_y + length_2 * np.sin(absolute_2)
    points = [
        (zeros, zeros),
        (0.5 * joint_x, 0.5 * joint_y),
        (joint_x, joint_y),
        (0.5 * (joint_x + tip_x), 0.5 * (joint_y + tip_y)),
        (tip_x, tip_y),
    ]
    return np.stack([np.stack(pair, axis=1) for pair in points], axis=1)


def _nominal_joint_trajectory(times: np.ndarray) -> tuple[np.ndarray, np.ndarray]:
    """The analytic commanded joint trajectory both arms are compared against."""

    q0 = 0.40 * np.sin(2.0 * np.pi * 0.20 * times)
    q1 = -0.60 + 0.30 * np.cos(2.0 * np.pi * 0.15 * times)
    return q0, q1


def _deviation_profile(times: np.ndarray, amplitude: float, tau_s: float) -> np.ndarray:
    """A zero-before-onset, saturating post-onset joint deviation. Deliberately analytic."""

    elapsed = np.maximum(times - FIXTURE_ONSET_TIME_S, 0.0)
    return amplitude * (1.0 - np.exp(-elapsed / tau_s))


def _fixture_arm(
    suite: str,
    times: np.ndarray,
    reference_xy: np.ndarray,
    amplitude: float,
    decisions: tuple[EstimatorOutput, ...],
    modes: tuple[str, ...],
) -> Arm:
    """Build one fixture arm whose distal body point is exactly its task output."""

    q0_nominal, q1_nominal = _nominal_joint_trajectory(times)
    deviation = _deviation_profile(times, amplitude, tau_s=0.8)
    centerline = _forward_kinematics(q0_nominal + deviation, q1_nominal - 0.6 * deviation)
    arm = Arm(
        suite=suite,
        centerline_xy=centerline,
        decisions=decisions,
        tracking=Tracking(
            task_reference=reference_xy,
            true_task_output=centerline[:, -1, :],
            window_s=FIXTURE_WINDOW_S,
        ),
        controller_step=np.arange(FIXTURE_N_FRAMES, dtype=np.int64),
        controller_t_s=fixture_controller_grid(),
        controller_mode=modes,
    )
    require_distal_point_matches_task_output(arm)
    return arm


def _modes(reconfigure_after_onset: bool) -> tuple[str, ...]:
    """A `controller_logs.controller_mode` array of length T on the step axis."""

    onset_step = FIXTURE_ONSET_INDEX
    if not reconfigure_after_onset:
        return tuple(["nominal"] * FIXTURE_N_FRAMES)
    return tuple(
        "nominal" if step < onset_step else "reconfigured" for step in range(FIXTURE_N_FRAMES)
    )


def _decision(
    index: int,
    p_class: Sequence[float],
    *,
    unknown_score: float,
    abstain: bool,
    location_out: int,
    severity_out: float,
    severity_uncertainty: float,
    detection_time_s: float,
) -> EstimatorOutput:
    """One fabricated schema-D decision row with round, visibly artificial numbers."""

    return EstimatorOutput(
        step=FIXTURE_DECISION_STEPS[index],
        decision_time_s=FIXTURE_DECISION_TIMES_S[index],
        p_class=np.asarray(p_class, dtype=float),
        unknown_score=unknown_score,
        abstain_decision=abstain,
        location_out=location_out,
        severity_out=severity_out,
        severity_uncertainty=severity_uncertainty,
        detection_time_s=detection_time_s,
    )


def _synthetic_provenance(case_id: str, seed: int) -> Provenance:
    """Visibly synthetic identities. `state` is fixed by the construction path."""

    pair_id = f"synthetic-fixture-seed-{seed}-{case_id}"
    return Provenance(
        state=SYNTHETIC_FIXTURE,
        connection_record_id=_SENTINEL_ABSENT,
        connection_record_sha256=_SENTINEL_ABSENT,
        config_identity=_SENTINEL_ABSENT,
        config_sha256=_SENTINEL_ABSENT,
        split=_SENTINEL_ABSENT,
        roles_read=(),
        arms={
            key: ArmIdentity(
                run_id=f"{pair_id}-{key}",
                pair_id=pair_id,
                checkpoint_relative_path=_SENTINEL_ABSENT,
                checkpoint_sha256=_SENTINEL_ABSENT,
            )
            for key in SUITE_KEYS
        },
        fixture_seed=int(seed),
    )


def build_fixture_scene(
    *,
    case_id: str,
    label: str,
    change: LabelFields,
    playback_t_s: np.ndarray,
    arms: Mapping[str, Arm],
    truth: LabelFields | None,
    thresholds: Thresholds,
    fixture_seed: int,
) -> VerificationScene:
    """Assemble and validate one synthetic scene.

    The provenance state is `SYNTHETIC_FIXTURE` by construction: this function takes
    no provenance, authority, split or role argument, and there is no keyword through
    which a caller can relabel what it returns (invariant V7).
    """

    scene = VerificationScene(
        bundle_version=BUNDLE_VERSION,
        provenance=_synthetic_provenance(case_id, fixture_seed),
        body_change=BodyChange(case_id=case_id, label=label, change=change),
        playback_t_s=np.asarray(playback_t_s, dtype=float),
        arms=dict(arms),
        truth=truth,
        thresholds=thresholds,
    )
    validate_scene(scene)
    return scene


def _fixture_cases(seed: int) -> list[dict]:
    """The named menu, as data.

    The tracking deviations deliberately do **not** favour one suite across the menu:
    the structural case gives `S` the smaller deviation, the actuator case gives `C1`
    the smaller one, the sensor case gives both the same, and the fourth case is
    exactly indistinguishable. A fixture whose every case flattered `S` would invite
    the reading this whole design exists to prevent.
    """

    generator = np.random.default_rng(seed)
    # One rounded, visibly artificial jitter per case, so the seed is load-bearing
    # without any fixture number ceasing to be round.
    jitter = np.round(generator.uniform(0.01, 0.05, size=4), 3)
    return [
        {
            "case_id": "soften_link_2",
            "label": "Soften link 2 by 30%",
            "change": LabelFields(
                source_class="structure",
                subtype="link_softening",
                location=1,
                severity=0.30,
                onset_index=FIXTURE_ONSET_INDEX,
                onset_time_s=FIXTURE_ONSET_TIME_S,
                compound_flag=False,
                ood_flag=False,
            ),
            "amplitudes": {"C1": 0.20 + float(jitter[0]), "S": 0.08},
            "modes": {"C1": False, "S": True},
            "decisions": {
                # A confident WRONG call, with the schema's own `+inf` severity scale
                # and pre-detection `NaN` detection time on every decision.
                "C1": (
                    _decision(
                        0,
                        (0.05, 0.10, 0.80, 0.05),
                        unknown_score=0.10,
                        abstain=False,
                        location_out=-1,
                        severity_out=0.0,
                        severity_uncertainty=math.inf,
                        detection_time_s=math.nan,
                    ),
                    _decision(
                        1,
                        (0.05, 0.05, 0.85, 0.05),
                        unknown_score=0.10,
                        abstain=False,
                        location_out=-1,
                        severity_out=0.0,
                        severity_uncertainty=math.inf,
                        detection_time_s=math.nan,
                    ),
                ),
                # A visible state change: an abstention that resolves into a
                # confident correct call at the second decision.
                "S": (
                    _decision(
                        0,
                        (0.25, 0.30, 0.25, 0.20),
                        unknown_score=0.20,
                        abstain=True,
                        location_out=-1,
                        severity_out=0.0,
                        severity_uncertainty=math.inf,
                        detection_time_s=math.nan,
                    ),
                    _decision(
                        1,
                        (0.05, 0.85, 0.05, 0.05),
                        unknown_score=0.10,
                        abstain=False,
                        location_out=1,
                        severity_out=0.30,
                        severity_uncertainty=0.05,
                        detection_time_s=1.20,
                    ),
                ),
            },
        },
        {
            "case_id": "weaken_actuator_1",
            "label": "Weaken actuator 1",
            "change": LabelFields(
                source_class="actuator",
                subtype="actuator_gain_loss",
                location=0,
                severity=0.40,
                onset_index=FIXTURE_ONSET_INDEX,
                onset_time_s=FIXTURE_ONSET_TIME_S,
                compound_flag=False,
                ood_flag=False,
            ),
            "amplitudes": {"C1": 0.10, "S": 0.22 + float(jitter[1])},
            "modes": {"C1": False, "S": True},
            "decisions": {
                # A pure abstention arm: it declines at both decisions.
                "C1": (
                    _decision(
                        0,
                        (0.25, 0.25, 0.25, 0.25),
                        unknown_score=0.20,
                        abstain=True,
                        location_out=-1,
                        severity_out=0.0,
                        severity_uncertainty=math.inf,
                        detection_time_s=math.nan,
                    ),
                    _decision(
                        1,
                        (0.30, 0.20, 0.30, 0.20),
                        unknown_score=0.30,
                        abstain=True,
                        location_out=-1,
                        severity_out=0.0,
                        severity_uncertainty=math.inf,
                        detection_time_s=math.nan,
                    ),
                ),
                "S": (
                    _decision(
                        0,
                        (0.10, 0.10, 0.70, 0.10),
                        unknown_score=0.10,
                        abstain=False,
                        location_out=0,
                        severity_out=0.40,
                        severity_uncertainty=0.10,
                        detection_time_s=1.30,
                    ),
                    _decision(
                        1,
                        (0.05, 0.05, 0.85, 0.05),
                        unknown_score=0.10,
                        abstain=False,
                        location_out=0,
                        severity_out=0.40,
                        severity_uncertainty=0.10,
                        detection_time_s=1.30,
                    ),
                ),
            },
        },
        {
            "case_id": "bias_encoder_1",
            "label": "Bias encoder 1",
            "change": LabelFields(
                source_class="sensor",
                subtype="encoder_bias",
                location=0,
                severity=0.02,
                onset_index=FIXTURE_ONSET_INDEX,
                onset_time_s=FIXTURE_ONSET_TIME_S,
                compound_flag=False,
                ood_flag=True,
            ),
            "amplitudes": {"C1": 0.15 + float(jitter[2]), "S": 0.15 + float(jitter[2])},
            "modes": {"C1": False, "S": False},
            "decisions": {
                # Both arms carry a high unknown score; C1 answers anyway (wrongly),
                # S declines.
                "C1": (
                    _decision(
                        0,
                        (0.31, 0.19, 0.20, 0.30),
                        unknown_score=0.90,
                        abstain=False,
                        location_out=-1,
                        severity_out=0.01,
                        severity_uncertainty=0.50,
                        detection_time_s=1.40,
                    ),
                    _decision(
                        1,
                        (0.35, 0.15, 0.20, 0.30),
                        unknown_score=0.90,
                        abstain=False,
                        location_out=-1,
                        severity_out=0.01,
                        severity_uncertainty=0.50,
                        detection_time_s=1.40,
                    ),
                ),
                "S": (
                    _decision(
                        0,
                        (0.25, 0.25, 0.25, 0.25),
                        unknown_score=0.95,
                        abstain=True,
                        location_out=-1,
                        severity_out=0.0,
                        severity_uncertainty=math.inf,
                        detection_time_s=math.nan,
                    ),
                    _decision(
                        1,
                        (0.20, 0.20, 0.20, 0.40),
                        unknown_score=0.95,
                        abstain=True,
                        location_out=-1,
                        severity_out=0.0,
                        severity_uncertainty=math.inf,
                        detection_time_s=math.nan,
                    ),
                ),
            },
        },
        {
            "case_id": "indistinguishable_softening",
            "label": "Soften link 1 by 10% (the two suites are indistinguishable)",
            "change": LabelFields(
                source_class="structure",
                subtype="link_softening",
                location=0,
                severity=0.10,
                onset_index=FIXTURE_ONSET_INDEX,
                onset_time_s=FIXTURE_ONSET_TIME_S,
                compound_flag=False,
                ood_flag=False,
            ),
            "amplitudes": {"C1": 0.12 + float(jitter[3]), "S": 0.12 + float(jitter[3])},
            "modes": {"C1": False, "S": False},
            "decisions": {
                "C1": (
                    _decision(
                        0,
                        (0.20, 0.40, 0.20, 0.20),
                        unknown_score=0.20,
                        abstain=False,
                        location_out=0,
                        severity_out=0.10,
                        severity_uncertainty=0.20,
                        detection_time_s=1.50,
                    ),
                    _decision(
                        1,
                        (0.15, 0.55, 0.15, 0.15),
                        unknown_score=0.20,
                        abstain=False,
                        location_out=0,
                        severity_out=0.10,
                        severity_uncertainty=0.20,
                        detection_time_s=1.50,
                    ),
                ),
                "S": (
                    _decision(
                        0,
                        (0.20, 0.40, 0.20, 0.20),
                        unknown_score=0.20,
                        abstain=False,
                        location_out=0,
                        severity_out=0.10,
                        severity_uncertainty=0.20,
                        detection_time_s=1.50,
                    ),
                    _decision(
                        1,
                        (0.15, 0.55, 0.15, 0.15),
                        unknown_score=0.20,
                        abstain=False,
                        location_out=0,
                        severity_out=0.10,
                        severity_uncertainty=0.20,
                        detection_time_s=1.50,
                    ),
                ),
            },
        },
    ]


def build_fixture_bundle(seed: int) -> VerificationBundle:
    """Build the complete named fixture menu from one seed.

    Args:
        seed: the required `--fixture-seed`. There is no default anywhere.

    Returns:
        A validated `VerificationBundle` whose every scene is `SYNTHETIC_FIXTURE`.
    """

    if isinstance(seed, bool) or not isinstance(seed, (int, np.integer)):
        raise VerificationSceneError(
            X_BUNDLE_INCOMPLETE, f"fixture seed must be an integer, got {seed!r}"
        )
    times = fixture_playback_grid()
    q0_nominal, q1_nominal = _nominal_joint_trajectory(times)
    reference_xy = _forward_kinematics(q0_nominal, q1_nominal)[:, -1, :]

    scenes: dict[str, VerificationScene] = {}
    for case in _fixture_cases(int(seed)):
        arms = {
            key: _fixture_arm(
                key,
                times,
                reference_xy,
                case["amplitudes"][key],
                case["decisions"][key],
                _modes(case["modes"][key]),
            )
            for key in SUITE_KEYS
        }
        scenes[case["case_id"]] = build_fixture_scene(
            case_id=case["case_id"],
            label=case["label"],
            change=case["change"],
            playback_t_s=times,
            arms=arms,
            truth=case["change"],
            thresholds=Thresholds(
                abstain_threshold=FIXTURE_ABSTAIN_THRESHOLD,
                unknown_threshold=FIXTURE_UNKNOWN_THRESHOLD,
            ),
            fixture_seed=int(seed),
        )
    bundle = VerificationBundle(
        bundle_version=BUNDLE_VERSION,
        provenance_state=SYNTHETIC_FIXTURE,
        scenes=scenes,
    )
    validate_bundle(bundle)
    return bundle


# --------------------------------------------------------------------------- #
# The real-result entry path: specified, and mechanically unreachable (V2).
# --------------------------------------------------------------------------- #
def build_role_bundle(
    *,
    connection_record: str,
    connection_record_sha256: str,
    config: str,
    checkpoint_root: str,
    role_root: str,
) -> VerificationBundle:
    """Refuse, before opening anything, because no connection record exists.

    Args:
        connection_record: path to the separately reviewed connection record.
        connection_record_sha256: the exact record identity the joint approval named.
        config: path to the exact frozen config file.
        checkpoint_root: root for the record's relative C1/S checkpoint paths.
        role_root: root containing the schema-E role layout.

    Raises:
        VerificationSceneError: always, with `X_CONNECTION_UNAUTHORIZED`. No argument
            is read, no path is opened and no default can re-enable this path; the
            later jointly approved connection record is what makes the already
            specified adapter reachable (design 4.2, section 9 step 4).
    """

    raise VerificationSceneError(
        X_CONNECTION_UNAUTHORIZED,
        "no jointly approved Slot-8 connection record exists in this packet, so no "
        "config, checkpoint, role index or role payload may be opened; connecting a "
        "real result is a separate design, review and joint authorization",
    )
