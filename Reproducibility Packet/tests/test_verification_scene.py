"""Tests for the Slot-8 verification scene contract and synthetic fixture.

No test here reads a role payload, a role index, a checkpoint, a config or any
split. Every scene under test is built by the packet's own labeled synthetic fixture
generator or is a deliberate mutation of one, and every refusal is driven rather than
asserted from the source text.

Invariants carried in this file (the renderer half lives in
`test_render_verification_scene.py`):

    V1  complete menu, two arms per case            V12 canonical JSON round trip
    V2  real roles unreachable (module half)        V13 fixture determinism (bundle half)
    V3  no scientific choice is derived             V14 no cross-arm derived scalar (schema half)
    V6  identities, pairing and the playback clock  V15 the metric is actually called
    V7  provenance is computed, never supplied      V17 fixture branch coverage (array half)
    V8  real provenance is provably unreachable     V18 no torch, no mujoco
                                                    V19 non-finite floats survive
"""

from __future__ import annotations

import ast
import copy
import dataclasses
import inspect
import json
import math
import subprocess
import sys
from pathlib import Path

import numpy as np
import pytest

PACKET_ROOT = Path(__file__).resolve().parents[1]
SCRIPTS_DIR = PACKET_ROOT / "scripts"
sys.path.insert(0, str(SCRIPTS_DIR))

from utils import verification_scene as vs  # noqa: E402
from utils.estimator import EstimatorOutput  # noqa: E402
from utils.metrics import SOURCE_CLASS_ORDER, j_5s  # noqa: E402

FIXTURE_SEED = 7


@pytest.fixture(scope="module")
def bundle() -> vs.VerificationBundle:
    """The labeled synthetic fixture bundle every test in this file works from."""

    return vs.build_fixture_bundle(FIXTURE_SEED)


def _scene(bundle: vs.VerificationBundle, case_id: str = "soften_link_2") -> vs.VerificationScene:
    """One fixture scene by name."""

    return bundle.scenes[case_id]


def _rebuild(scene: vs.VerificationScene, **changes) -> vs.VerificationScene:
    """Re-run construction on a mutated scene, so the refusal comes from the builder."""

    return vs.build_fixture_scene(
        case_id=changes.get("case_id", scene.body_change.case_id),
        label=changes.get("label", scene.body_change.label),
        change=changes.get("change", scene.body_change.change),
        playback_t_s=changes.get("playback_t_s", scene.playback_t_s),
        arms=changes.get("arms", scene.arms),
        truth=changes.get("truth", scene.truth),
        thresholds=changes.get("thresholds", scene.thresholds),
        fixture_seed=changes.get("fixture_seed", scene.provenance.fixture_seed),
    )


def _arm_with(arm: vs.Arm, **changes) -> vs.Arm:
    """A copy of one arm with named fields replaced."""

    return dataclasses.replace(arm, **changes)


def _tracking_with(arm: vs.Arm, **changes) -> vs.Arm:
    """A copy of one arm whose tracking block has named fields replaced."""

    return dataclasses.replace(arm, tracking=dataclasses.replace(arm.tracking, **changes))


def _module_source(name: str) -> ast.Module:
    """The parsed source of one of the two Slot-8 modules."""

    if name == "verification_scene":
        return ast.parse((SCRIPTS_DIR / "utils" / "verification_scene.py").read_text(encoding="utf-8"))
    return ast.parse((SCRIPTS_DIR / f"{name}.py").read_text(encoding="utf-8"))


# --------------------------------------------------------------------------- #
# V1 - a complete menu, with two arms per case, or nothing.
# --------------------------------------------------------------------------- #
def test_v1_bundle_case_ids_are_unique_and_ordered(bundle):
    """The menu is data: unique ids, stable order, one key per scene."""

    assert bundle.case_ids == (
        "soften_link_2",
        "weaken_actuator_1",
        "bias_encoder_1",
        "indistinguishable_softening",
    )
    assert len(set(bundle.case_ids)) == len(bundle.case_ids)
    for case_id, scene in bundle.scenes.items():
        assert scene.body_change.case_id == case_id


def test_v1_bundle_covers_every_required_source_class(bundle):
    """At least one structure, actuator and sensor case."""

    present = {scene.body_change.change.source_class for scene in bundle.scenes.values()}
    for required in vs.REQUIRED_SOURCE_CLASSES:
        assert required in present


def test_v1_interactive_menu_display_labels_must_be_unique(bundle):
    """Property 8: a human-readable radio label must select exactly one case."""

    scenes = dict(bundle.scenes)
    first_id, second_id = list(scenes)[:2]
    scenes[second_id] = dataclasses.replace(
        scenes[second_id],
        body_change=dataclasses.replace(
            scenes[second_id].body_change,
            label=scenes[first_id].body_change.label,
        ),
    )
    duplicate = vs.VerificationBundle(
        bundle_version=bundle.bundle_version,
        provenance_state=bundle.provenance_state,
        scenes=scenes,
    )
    with pytest.raises(vs.VerificationSceneError) as refusal:
        vs.validate_bundle(duplicate)
    assert refusal.value.code == vs.X_BUNDLE_INCOMPLETE


def test_v1_missing_required_source_class_refuses(bundle):
    """A menu with no sensor case is X_BUNDLE_INCOMPLETE, not a smaller menu."""

    partial = vs.VerificationBundle(
        bundle_version=vs.BUNDLE_VERSION,
        provenance_state=vs.SYNTHETIC_FIXTURE,
        scenes={
            case_id: scene
            for case_id, scene in bundle.scenes.items()
            if scene.body_change.change.source_class != "sensor"
        },
    )
    with pytest.raises(vs.VerificationSceneError) as refusal:
        vs.validate_bundle(partial)
    assert refusal.value.code == vs.X_BUNDLE_INCOMPLETE


def test_v1_empty_bundle_refuses():
    """A bundle is non-empty."""

    with pytest.raises(vs.VerificationSceneError) as refusal:
        vs.validate_bundle(
            vs.VerificationBundle(
                bundle_version=vs.BUNDLE_VERSION,
                provenance_state=vs.SYNTHETIC_FIXTURE,
                scenes={},
            )
        )
    assert refusal.value.code == vs.X_BUNDLE_INCOMPLETE


@pytest.mark.parametrize("keys", [("C1",), ("S",), ("C1", "S", "C0"), ()])
def test_v1_wrong_arm_set_refuses(bundle, keys):
    """A scene that could carry one arm is a scene that can draw a one-sided picture."""

    scene = _scene(bundle)
    arms = {key: scene.arms.get(key, scene.arms["C1"]) for key in keys}
    with pytest.raises(vs.VerificationSceneError) as refusal:
        _rebuild(scene, arms=arms)
    assert refusal.value.code == vs.X_ARMS_INCOMPLETE


def test_v1_arm_filed_under_the_wrong_key_refuses(bundle):
    """The key and the arm's own suite label must agree."""

    scene = _scene(bundle)
    arms = {"C1": scene.arms["S"], "S": scene.arms["S"]}
    with pytest.raises(vs.VerificationSceneError) as refusal:
        _rebuild(scene, arms=arms)
    assert refusal.value.code == vs.X_ARMS_INCOMPLETE


# --------------------------------------------------------------------------- #
# V2 - real roles are unreachable in this round (module half).
# --------------------------------------------------------------------------- #
def test_v2_role_bundle_refuses_before_opening_anything(tmp_path):
    """Role mode refuses with its own code, whatever it is pointed at."""

    with pytest.raises(vs.VerificationSceneError) as refusal:
        vs.build_role_bundle(
            connection_record=str(tmp_path / "record.json"),
            connection_record_sha256="0" * 64,
            config=str(PACKET_ROOT / "config"),
            checkpoint_root=str(PACKET_ROOT / "results"),
            role_root=str(tmp_path),
        )
    assert refusal.value.code == vs.X_CONNECTION_UNAUTHORIZED


def test_v2_role_bundle_refuses_even_with_real_packet_paths():
    """Pointing it at objects that do exist changes nothing."""

    with pytest.raises(vs.VerificationSceneError) as refusal:
        vs.build_role_bundle(
            connection_record=str(PACKET_ROOT / "schema" / "schema.json"),
            connection_record_sha256="0" * 64,
            config=str(PACKET_ROOT / "schema" / "schema.json"),
            checkpoint_root=str(PACKET_ROOT / "results"),
            role_root=str(PACKET_ROOT / "results"),
        )
    assert refusal.value.code == vs.X_CONNECTION_UNAUTHORIZED


def test_v2_role_bundle_opens_no_file(monkeypatch, tmp_path):
    """The refusal fires before any read: `open` is never reached."""

    def _forbidden(*args, **kwargs):
        raise AssertionError("role mode opened a file before refusing")

    monkeypatch.setattr("builtins.open", _forbidden)
    monkeypatch.setattr(Path, "open", _forbidden)
    monkeypatch.setattr(Path, "read_bytes", _forbidden)
    monkeypatch.setattr(Path, "read_text", _forbidden)
    with pytest.raises(vs.VerificationSceneError):
        vs.build_role_bundle(
            connection_record=str(tmp_path / "r.json"),
            connection_record_sha256="0" * 64,
            config=str(tmp_path / "c.json"),
            checkpoint_root=str(tmp_path),
            role_root=str(tmp_path),
        )


def test_v2_no_role_override_keyword_exists():
    """No caller-supplied allowlist, split flag or environment escape hatch."""

    parameters = set(inspect.signature(vs.build_role_bundle).parameters)
    assert parameters == {
        "connection_record",
        "connection_record_sha256",
        "config",
        "checkpoint_root",
        "role_root",
    }
    source = (SCRIPTS_DIR / "utils" / "verification_scene.py").read_text(encoding="utf-8")
    assert "os.environ" not in source and "getenv" not in source


# --------------------------------------------------------------------------- #
# V3 - the module derives no scientific choice.
# --------------------------------------------------------------------------- #
def test_v3_thresholds_are_fixture_data_not_derived(bundle):
    """Both thresholds are round fabricated fixture fields, identical across the menu."""

    for scene in bundle.scenes.values():
        assert scene.thresholds.abstain_threshold == vs.FIXTURE_ABSTAIN_THRESHOLD
        assert scene.thresholds.unknown_threshold == vs.FIXTURE_UNKNOWN_THRESHOLD


def test_v3_module_imports_no_model_capacity_or_fitting_module():
    """Nothing that selects a capacity, a rung, a width or a threshold is imported."""

    tree = _module_source("verification_scene")
    imported: set[str] = set()
    for node in ast.walk(tree):
        if isinstance(node, ast.Import):
            imported.update(alias.name for alias in node.names)
        elif isinstance(node, ast.ImportFrom) and node.module:
            imported.add(node.module)
    forbidden = {
        "torch",
        "mujoco",
        "utils.capacity_sweep",
        "utils.dev_fit_trainer",
        "utils.attribution_net",
        "utils.attribution_net_rung2",
        "utils.rung2_escalation",
        "utils.role_contract",
        "utils.config_contract",
        "utils.storage_contract",
    }
    assert not (imported & forbidden), sorted(imported & forbidden)


# --------------------------------------------------------------------------- #
# V6 - identities, pairing and the playback clock travel.
# --------------------------------------------------------------------------- #
def test_v6_every_frame_bearing_array_binds_to_one_playback_grid(bundle):
    """One grid, and every arm array indexed by it."""

    for scene in bundle.scenes.values():
        n_frames = scene.n_frames
        assert np.asarray(scene.playback_t_s).shape == (n_frames,)
        for key in vs.SUITE_KEYS:
            arm = scene.arms[key]
            assert np.asarray(arm.centerline_xy).shape[0] == n_frames
            assert np.asarray(arm.tracking.task_reference).shape == (n_frames, 2)
            assert np.asarray(arm.tracking.true_task_output).shape == (n_frames, 2)
            assert len(arm.controller_mode) == n_frames
            assert np.array_equal(arm.controller_step, np.arange(n_frames))


def test_v6_one_frame_names_one_physical_time_in_both_arms(bundle):
    """There is only one clock, so a frame cannot mean two times."""

    scene = _scene(bundle)
    frame = 77
    times = {
        key: float(np.asarray(scene.playback_t_s, dtype=float)[frame]) for key in vs.SUITE_KEYS
    }
    assert times["C1"] == times["S"]


def test_v6_short_body_axis_refuses_with_timebase_code(bundle):
    """A body array that is not on the playback grid is a timebase refusal."""

    scene = _scene(bundle)
    arm = scene.arms["C1"]
    truncated = _arm_with(arm, centerline_xy=np.asarray(arm.centerline_xy)[:-1])
    with pytest.raises(vs.VerificationSceneError) as refusal:
        _rebuild(scene, arms={"C1": truncated, "S": scene.arms["S"]})
    assert refusal.value.code == vs.X_TIMEBASE_MISMATCH


def test_v6_non_contiguous_controller_step_axis_refuses(bundle):
    """`controller_logs.step` is the contiguous 0-based grid, in both arms."""

    scene = _scene(bundle)
    arm = scene.arms["S"]
    broken = np.arange(scene.n_frames, dtype=np.int64)
    broken[10] = 999
    with pytest.raises(vs.VerificationSceneError) as refusal:
        _rebuild(
            scene,
            arms={"C1": scene.arms["C1"], "S": _arm_with(arm, controller_step=broken)},
        )
    assert refusal.value.code == vs.X_TIMEBASE_MISMATCH


def test_v6_controller_mode_length_is_bound_to_the_step_axis(bundle):
    """A `controller_mode` array of the wrong length refuses."""

    scene = _scene(bundle)
    arm = scene.arms["C1"]
    with pytest.raises(vs.VerificationSceneError) as refusal:
        _rebuild(
            scene,
            arms={
                "C1": _arm_with(arm, controller_mode=arm.controller_mode[:-1]),
                "S": scene.arms["S"],
            },
        )
    assert refusal.value.code == vs.X_TIMEBASE_MISMATCH


def test_v6_the_fixture_controller_clock_is_one_control_interval_early(bundle):
    """The fixture carries the live loop's actual pre-advance controller convention."""

    scene = _scene(bundle)
    playback = np.asarray(scene.playback_t_s, dtype=float)
    for key in vs.SUITE_KEYS:
        controller = np.asarray(scene.arms[key].controller_t_s, dtype=float)
        offsets = playback - controller
        assert np.allclose(offsets, vs.FIXTURE_CONTROL_DT_S)
        assert not np.allclose(controller, playback)


def test_v6_offset_controller_grid_is_accepted(bundle):
    """THE ACCEPT SIDE. Deleting this test is how finding CI comes back.

    A controller payload whose `t_s` is one control interval earlier than the plant
    grid -- which is what `run_online_rollout` actually records -- must be accepted.
    """

    scene = _scene(bundle)
    playback = np.asarray(scene.playback_t_s, dtype=float)
    offset = playback - vs.FIXTURE_CONTROL_DT_S
    rebuilt = _rebuild(
        scene,
        arms={
            key: _arm_with(scene.arms[key], controller_t_s=offset) for key in vs.SUITE_KEYS
        },
    )
    assert rebuilt.provenance.state == vs.SYNTHETIC_FIXTURE


def test_v6_controller_grid_equal_to_playback_is_also_accepted(bundle):
    """The rule pins the step axis, not the timestamp, so equality is not forbidden either."""

    scene = _scene(bundle)
    playback = np.asarray(scene.playback_t_s, dtype=float)
    rebuilt = _rebuild(
        scene,
        arms={
            key: _arm_with(scene.arms[key], controller_t_s=playback.copy())
            for key in vs.SUITE_KEYS
        },
    )
    assert rebuilt.n_frames == scene.n_frames


def test_v6_disagreeing_task_reference_is_a_pair_refusal(bundle):
    """Both arms replay the same paired task against the same reference."""

    scene = _scene(bundle)
    arm = scene.arms["S"]
    moved = np.asarray(arm.tracking.task_reference, dtype=float).copy()
    moved[0, 0] += 0.001
    with pytest.raises(vs.VerificationSceneError) as refusal:
        _rebuild(
            scene,
            arms={"C1": scene.arms["C1"], "S": _tracking_with(arm, task_reference=moved)},
        )
    assert refusal.value.code == vs.X_PAIR_MISMATCH


def test_v6_disagreeing_analysis_window_is_a_pair_refusal(bundle):
    """One comparison has one analysis window; the derived still's frame depends on it."""

    scene = _scene(bundle)
    with pytest.raises(vs.VerificationSceneError) as refusal:
        _rebuild(
            scene,
            arms={
                "C1": scene.arms["C1"],
                "S": _tracking_with(scene.arms["S"], window_s=4.0),
            },
        )
    assert refusal.value.code == vs.X_PAIR_MISMATCH


# --------------------------------------------------------------------------- #
# Decision axis refusals (X_DECISION_UNSUPPORTED).
# --------------------------------------------------------------------------- #
def test_decisions_must_be_strictly_increasing(bundle):
    """A non-monotone decision axis cannot support the causal at-or-before rule."""

    scene = _scene(bundle)
    arm = scene.arms["C1"]
    reversed_pair = (arm.decisions[1], arm.decisions[0])
    with pytest.raises(vs.VerificationSceneError) as refusal:
        _rebuild(
            scene,
            arms={"C1": _arm_with(arm, decisions=reversed_pair), "S": scene.arms["S"]},
        )
    assert refusal.value.code == vs.X_DECISION_UNSUPPORTED


def test_decision_outside_the_playback_extent_refuses(bundle):
    """A decision after the last frame is not a decision this playback can show."""

    scene = _scene(bundle)
    arm = scene.arms["C1"]
    late = dataclasses.replace(arm.decisions[-1], step=999, decision_time_s=99.0)
    with pytest.raises(vs.VerificationSceneError) as refusal:
        _rebuild(
            scene,
            arms={
                "C1": _arm_with(arm, decisions=arm.decisions + (late,)),
                "S": scene.arms["S"],
            },
        )
    assert refusal.value.code == vs.X_DECISION_UNSUPPORTED


def test_empty_decision_trace_refuses(bundle):
    """The live role contract refuses an empty `estimator_outputs` payload; so does this."""

    scene = _scene(bundle)
    with pytest.raises(vs.VerificationSceneError) as refusal:
        _rebuild(
            scene,
            arms={"C1": _arm_with(scene.arms["C1"], decisions=()), "S": scene.arms["S"]},
        )
    assert refusal.value.code == vs.X_DECISION_UNSUPPORTED


def test_decision_failing_the_schema_contract_refuses(bundle):
    """Per-decision validity is established by calling `EstimatorOutput.validate`."""

    scene = _scene(bundle)
    arm = scene.arms["C1"]
    broken = dataclasses.replace(
        arm.decisions[0], p_class=np.asarray([0.9, 0.9, 0.9, 0.9], dtype=float)
    )
    with pytest.raises(vs.VerificationSceneError) as refusal:
        _rebuild(
            scene,
            arms={
                "C1": _arm_with(arm, decisions=(broken,) + arm.decisions[1:]),
                "S": scene.arms["S"],
            },
        )
    assert refusal.value.code == vs.X_DECISION_UNSUPPORTED


def test_decision_at_frame_is_causal_and_borrows_nothing_from_the_future(bundle):
    """Before the first decision there is no decision; after it, the greatest at-or-before."""

    scene = _scene(bundle)
    playback = np.asarray(scene.playback_t_s, dtype=float)
    first = scene.arms["S"].decisions[0]
    second = scene.arms["S"].decisions[1]
    early = int(np.flatnonzero(playback < float(first.decision_time_s))[-1])
    middle = int(np.flatnonzero(playback < float(second.decision_time_s))[-1])
    assert vs.decision_at_frame(scene, "S", early) is None
    assert vs.decision_at_frame(scene, "S", middle) is first
    assert vs.decision_at_frame(scene, "S", scene.n_frames - 1) is second


# --------------------------------------------------------------------------- #
# V7 / V8 - provenance is computed, and the real states are unreachable.
# --------------------------------------------------------------------------- #
@pytest.mark.parametrize(
    "builder", [vs.build_fixture_bundle, vs.build_fixture_scene, vs.build_role_bundle]
)
def test_v7_no_public_builder_takes_a_provenance_keyword(builder):
    """There is no keyword through which a caller can label what it gets back."""

    forbidden = {"provenance", "state", "authority", "split", "roles", "role_allowlist"}
    assert not (set(inspect.signature(builder).parameters) & forbidden)


def test_v7_a_fixture_scene_cannot_be_relabelled(bundle):
    """The value is frozen: relabelling raises rather than silently succeeding."""

    scene = _scene(bundle)
    with pytest.raises(dataclasses.FrozenInstanceError):
        scene.provenance.state = vs.FINAL  # type: ignore[misc]
    with pytest.raises(dataclasses.FrozenInstanceError):
        scene.provenance = dataclasses.replace(scene.provenance, state=vs.FINAL)  # type: ignore[misc]


def test_v7_the_only_provenance_construction_names_the_synthetic_state():
    """Structurally: the module builds `Provenance` in exactly two places.

    One is the synthetic construction path, which hard-codes the state. The other is
    the audit codec, which reads back a state this module already computed and wrote;
    no CLI argument reaches it, which `test_v4_...` on the renderer side pins.
    """

    tree = _module_source("verification_scene")
    built: set[tuple[str, str]] = set()
    for function in ast.walk(tree):
        if not isinstance(function, ast.FunctionDef):
            continue
        for node in ast.walk(function):
            if isinstance(node, ast.Call) and getattr(node.func, "id", None) == "Provenance":
                keywords = {kw.arg: kw.value for kw in node.keywords}
                assert "state" in keywords
                built.add((function.name, ast.unparse(keywords["state"])))
    assert built == {
        ("_synthetic_provenance", "SYNTHETIC_FIXTURE"),
        ("scene_from_json", "str(provenance_payload['state'])"),
    }


def test_v8_no_input_in_this_packet_yields_a_real_provenance_state(bundle):
    """When either state becomes reachable this goes red, and it should."""

    for scene in bundle.scenes.values():
        assert scene.provenance.state == vs.SYNTHETIC_FIXTURE
        assert scene.provenance.roles_read == ()
    with pytest.raises(vs.VerificationSceneError):
        vs.build_role_bundle(
            connection_record="",
            connection_record_sha256="",
            config="",
            checkpoint_root="",
            role_root="",
        )


def test_bundle_scenes_must_agree_on_their_provenance_state(bundle):
    """A mixed-state bundle is unresolved, not a partly-real menu."""

    scenes = dict(bundle.scenes)
    first = next(iter(scenes))
    scenes[first] = dataclasses.replace(
        scenes[first],
        provenance=dataclasses.replace(scenes[first].provenance, state=vs.FINAL),
    )
    with pytest.raises(vs.VerificationSceneError) as refusal:
        vs.validate_bundle(
            vs.VerificationBundle(
                bundle_version=vs.BUNDLE_VERSION,
                provenance_state=vs.SYNTHETIC_FIXTURE,
                scenes=scenes,
            )
        )
    assert refusal.value.code == vs.X_PROVENANCE_UNRESOLVED


# --------------------------------------------------------------------------- #
# V12 / V19 - the canonical JSON codec.
# --------------------------------------------------------------------------- #
def test_v12_bundle_round_trips_byte_identically(bundle):
    """Serialize, strict-parse, serialize is byte-identical."""

    text = vs.canonical_bundle_text(bundle)
    decoded = vs.bundle_from_json(vs.loads_strict(text))
    assert vs.canonical_bundle_text(decoded) == text


def test_v12_scene_round_trips_byte_identically(bundle):
    """The per-case scene document round-trips too, since figures cite it."""

    for scene in bundle.scenes.values():
        text = vs.canonical_scene_text(scene)
        assert vs.canonical_scene_text(vs.scene_from_json(vs.loads_strict(text))) == text


def test_v12_canonical_text_uses_the_packet_rules(bundle):
    """Sorted keys, tight separators, no non-standard token, `allow_nan` still on."""

    text = vs.canonical_bundle_text(bundle)
    assert ", " not in text and '": ' not in text
    for token in ("NaN,", "Infinity,", "-Infinity,"):
        assert token not in text
    assert '"NaN"' in text and '"Infinity"' in text


@pytest.mark.parametrize("token", ["NaN", "Infinity", "-Infinity"])
def test_v19_bare_non_standard_tokens_refuse_through_parse_constant(token):
    """The default loader accepts these; `parse_constant` is what refuses them."""

    assert json.loads(f'{{"a": {token}}}')  # the behaviour being guarded against
    with pytest.raises(vs.VerificationDecodeError):
        vs.loads_strict(f'{{"a": {token}}}')


@pytest.mark.parametrize(
    ("value", "encoded"),
    [(math.inf, "Infinity"), (-math.inf, "-Infinity"), (math.nan, "NaN")],
)
def test_v19_codec_pins_all_three_string_mappings(value, encoded):
    """Total and exactly invertible, negative infinity included."""

    assert vs.encode_float(value) == encoded
    decoded = vs.decode_float(encoded)
    if encoded == "NaN":
        assert math.isnan(decoded)
    else:
        assert math.isinf(decoded) and math.copysign(1.0, decoded) == math.copysign(1.0, value)


def test_v19_a_finite_float_never_encodes_as_a_string():
    """This is what makes the mapping unambiguous."""

    for value in (0.0, -0.0, 1.0, -2.5, 1e300, 5e-324):
        assert isinstance(vs.encode_float(value), float)


@pytest.mark.parametrize("bad", ["inf", "nan", "1.0", "", "Infinity ", "NAN", "None"])
def test_v19_any_other_string_in_a_float_position_refuses_loudly(bad):
    """Never a silent zero."""

    with pytest.raises(vs.VerificationDecodeError):
        vs.decode_float(bad)


def test_v19_scene_carrying_infinite_scale_and_nan_detection_round_trips(bundle):
    """The schema's own defaults survive the write and are never silently repaired."""

    scene = _scene(bundle)
    decision = scene.arms["C1"].decisions[0]
    assert math.isinf(float(decision.severity_uncertainty))
    assert math.isnan(float(decision.detection_time_s))

    text = vs.canonical_scene_text(scene)
    decoded = vs.scene_from_json(vs.loads_strict(text))
    restored = decoded.arms["C1"].decisions[0]
    assert math.isinf(float(restored.severity_uncertainty))
    assert math.copysign(1.0, float(restored.severity_uncertainty)) > 0.0
    assert math.isnan(float(restored.detection_time_s))
    # Object equality is not the oracle: IEEE-754 NaN is unequal to itself.
    assert vs.canonical_scene_text(decoded) == text


def test_v19_mutant_documents_with_bare_tokens_refuse(bundle):
    """A document rewritten to use the bare tokens does not decode."""

    text = vs.canonical_scene_text(_scene(bundle))
    for quoted, bare in (('"Infinity"', "Infinity"), ('"NaN"', "NaN")):
        mutant = text.replace(quoted, bare, 1)
        assert mutant != text
        with pytest.raises(vs.VerificationDecodeError):
            vs.loads_strict(mutant)


# --------------------------------------------------------------------------- #
# V13 (bundle half) - the fixture is deterministic and the seed is load-bearing.
# --------------------------------------------------------------------------- #
def test_v13_fixture_at_a_fixed_seed_is_byte_identical():
    """Same seed, same bytes."""

    first = vs.canonical_bundle_text(vs.build_fixture_bundle(FIXTURE_SEED))
    second = vs.canonical_bundle_text(vs.build_fixture_bundle(FIXTURE_SEED))
    assert first == second


def test_v13_a_different_seed_gives_a_different_bundle():
    """`--fixture-seed` is required because it is load-bearing, not decorative."""

    assert vs.canonical_bundle_text(vs.build_fixture_bundle(7)) != vs.canonical_bundle_text(
        vs.build_fixture_bundle(8)
    )


def test_v13_seed_must_be_an_integer():
    """No default seed, and no silent coercion of a non-integer one."""

    for bad in (None, "7", 7.0, True):
        with pytest.raises(vs.VerificationSceneError) as refusal:
            vs.build_fixture_bundle(bad)  # type: ignore[arg-type]
        assert refusal.value.code == vs.X_BUNDLE_INCOMPLETE


# --------------------------------------------------------------------------- #
# V14 (schema half) - no cross-arm derived scalar exists.
# --------------------------------------------------------------------------- #
_CROSS_ARM_TOKENS = (
    "reduction",
    "difference",
    "delta",
    "ratio",
    "minus",
    "improvement",
    "advantage",
    "gain_over",
    "versus",
    "_vs_",
)


def test_v14_no_scene_field_name_carries_a_cross_arm_quantity():
    """The scene schema itself has no place to put a C1-versus-S number."""

    for name in dir(vs):
        candidate = getattr(vs, name)
        if not dataclasses.is_dataclass(candidate):
            continue
        for field in dataclasses.fields(candidate):
            lowered = field.name.lower()
            assert not any(token in lowered for token in _CROSS_ARM_TOKENS), field.name


def test_v14_module_never_references_the_reduction_metric():
    """`tracking_reduction_pct` exists in `utils.metrics`; it is not reachable from here."""

    tree = _module_source("verification_scene")
    names = {node.id for node in ast.walk(tree) if isinstance(node, ast.Name)}
    names |= {node.attr for node in ast.walk(tree) if isinstance(node, ast.Attribute)}
    for node in ast.walk(tree):
        if isinstance(node, ast.ImportFrom):
            names |= {alias.name for alias in node.names}
    assert "tracking_reduction_pct" not in names


# --------------------------------------------------------------------------- #
# V15 - schema and metric mappings are exact, and the metric is actually called.
# --------------------------------------------------------------------------- #
def test_v15_decision_fields_equal_the_machine_schema_estimator_output_fields():
    """Pinned by EQUALITY against the bound document, never adopted from it."""

    schema = json.loads((PACKET_ROOT / "schema" / "schema.json").read_text(encoding="utf-8"))
    declared = tuple(schema["roles"]["estimator_outputs"]["fields"])
    carried = tuple(field.name for field in dataclasses.fields(EstimatorOutput))
    assert carried == declared


def test_v15_label_fields_equal_the_machine_schema_label_fields():
    """The scene's label struct is the schema's, name for name and in order."""

    schema = json.loads((PACKET_ROOT / "schema" / "schema.json").read_text(encoding="utf-8"))
    declared = tuple(schema["roles"]["labels"]["fields"])
    carried = tuple(field.name for field in dataclasses.fields(vs.LabelFields))
    assert carried == declared


def test_v15_the_metric_returns_a_finite_value_on_every_fixture_arm(bundle):
    """THE UNCONDITIONAL HALF. Property 2 is only checkable if `j_5s` accepts the inputs."""

    for scene in bundle.scenes.values():
        for key in vs.SUITE_KEYS:
            arm = scene.arms[key]
            value = j_5s(
                scene.playback_t_s,
                arm.tracking.task_reference,
                arm.tracking.true_task_output,
                float(scene.body_change.change.onset_time_s),
                window_s=float(arm.tracking.window_s),
            )
            assert np.isfinite(value) and value >= 0.0


def test_v15_construction_delegates_to_the_live_metric(monkeypatch, bundle):
    """A refusal invented inside `j_5s` must surface as `X_WINDOW_UNSUPPORTED`.

    Deleting this test is how finding CN comes back: an enumeration of the metric's
    preconditions passes every named check and still lets the picture and the number
    drift apart.
    """

    scene = _scene(bundle)
    sentinel = "a precondition this design has never heard of"

    def _refusing_metric(*args, **kwargs):
        raise ValueError(sentinel)

    monkeypatch.setattr(vs, "j_5s", _refusing_metric)
    with pytest.raises(vs.VerificationSceneError) as refusal:
        _rebuild(scene)
    assert refusal.value.code == vs.X_WINDOW_UNSUPPORTED
    assert sentinel in str(refusal.value)


def test_v15_the_window_check_is_a_call_and_not_a_checklist():
    """Structurally: the validator calls `j_5s` rather than re-deriving its rules."""

    tree = _module_source("verification_scene")
    validators = [
        node
        for node in ast.walk(tree)
        if isinstance(node, ast.FunctionDef) and node.name == "_validate_tracking_window"
    ]
    assert len(validators) == 1
    called = {
        getattr(node.func, "id", None)
        for node in ast.walk(validators[0])
        if isinstance(node, ast.Call)
    }
    assert "j_5s" in called


def _window_mutants(scene: vs.VerificationScene) -> dict[str, dict]:
    """The six refusal shapes V15 requires to be asserted individually."""

    playback = np.asarray(scene.playback_t_s, dtype=float)
    non_uniform = playback.copy()
    non_uniform[50] += 0.01
    unfinite = np.asarray(scene.arms["C1"].tracking.true_task_output, dtype=float).copy()
    unfinite[0, 0] = math.inf
    return {
        "non_uniform_grid": {"playback_t_s": non_uniform},
        "off_sample_onset": {
            "change": dataclasses.replace(scene.body_change.change, onset_time_s=1.025)
        },
        "grid_ends_before_window_close": {
            "arms": {
                key: _tracking_with(scene.arms[key], window_s=6.5) for key in vs.SUITE_KEYS
            }
        },
        "non_finite_tracking_sample": {
            "arms": {
                "C1": _tracking_with(scene.arms["C1"], true_task_output=unfinite),
                "S": scene.arms["S"],
            }
        },
        "non_positive_window": {
            "arms": {
                key: _tracking_with(scene.arms[key], window_s=0.0) for key in vs.SUITE_KEYS
            }
        },
        "window_shorter_than_one_interval": {
            "arms": {
                key: _tracking_with(scene.arms[key], window_s=0.001) for key in vs.SUITE_KEYS
            }
        },
    }


@pytest.mark.parametrize(
    "shape",
    [
        "non_uniform_grid",
        "off_sample_onset",
        "grid_ends_before_window_close",
        "non_finite_tracking_sample",
        "non_positive_window",
        "window_shorter_than_one_interval",
    ],
)
def test_v15_six_window_refusal_shapes_each_refuse_at_construction(bundle, shape):
    """Each is asserted individually; the last two are caught only by the call."""

    scene = _scene(bundle)
    with pytest.raises(vs.VerificationSceneError) as refusal:
        _rebuild(scene, **_window_mutants(scene)[shape])
    assert refusal.value.code == vs.X_WINDOW_UNSUPPORTED


def test_v15_the_last_two_shapes_pass_every_other_named_check(bundle):
    """Measured, not assumed: they are why the enumeration was replaced by the call."""

    scene = _scene(bundle)
    playback = np.asarray(scene.playback_t_s, dtype=float)
    onset = float(scene.body_change.change.onset_time_s)
    steps = np.diff(playback)
    assert np.all(np.isfinite(playback))
    assert np.all(steps > 0.0)
    assert np.allclose(steps, steps[0], rtol=1.0e-7, atol=1.0e-12)
    assert np.min(np.abs(playback - onset)) <= 1.0e-9
    for window in (0.0, -1.0, 0.001):
        with pytest.raises(ValueError):
            j_5s(
                playback,
                scene.arms["C1"].tracking.task_reference,
                scene.arms["C1"].tracking.true_task_output,
                onset,
                window_s=window,
            )


# --------------------------------------------------------------------------- #
# V17 (array half) - the fixture exercises the visible branches.
# --------------------------------------------------------------------------- #
def test_v17_every_fixture_arm_has_a_non_empty_decision_trace(bundle):
    """The pre-decision branch can never be satisfied by an empty trace."""

    for scene in bundle.scenes.values():
        for key in vs.SUITE_KEYS:
            assert len(scene.arms[key].decisions) >= 1


def test_v17_at_least_one_case_has_two_ordered_decisions_after_the_grid_starts(bundle):
    """A grid that begins before the first decision is what drives `NO DECISION YET`."""

    found = False
    for scene in bundle.scenes.values():
        for key in vs.SUITE_KEYS:
            decisions = scene.arms[key].decisions
            if len(decisions) >= 2:
                first = float(decisions[0].decision_time_s)
                assert float(np.asarray(scene.playback_t_s)[0]) < first
                found = True
    assert found


def test_v17_fixture_covers_confident_correct_wrong_abstain_and_high_unknown(bundle):
    """The unflattering branches are present in the arrays, at the settled frame."""

    seen = {"correct": False, "wrong": False, "abstain": False, "high_unknown": False}
    for scene in bundle.scenes.values():
        truth = scene.truth
        for key in vs.SUITE_KEYS:
            final = scene.arms[key].decisions[-1]
            if bool(final.abstain_decision):
                seen["abstain"] = True
            else:
                call = SOURCE_CLASS_ORDER[int(np.argmax(np.asarray(final.p_class)))]
                confident = float(np.max(np.asarray(final.p_class))) >= float(
                    scene.thresholds.abstain_threshold
                )
                if confident and truth is not None and call == truth.source_class:
                    seen["correct"] = True
                if confident and truth is not None and call != truth.source_class:
                    seen["wrong"] = True
            if float(final.unknown_score) >= float(scene.thresholds.unknown_threshold):
                seen["high_unknown"] = True
    assert all(seen.values()), seen


def test_v17_fixture_has_an_indistinguishable_case(bundle):
    """Slot 8 names the honest negative by name; a demo that cannot draw it shows only wins."""

    indistinguishable = []
    for case_id, scene in bundle.scenes.items():
        arms_equal = np.array_equal(
            np.asarray(scene.arms["C1"].centerline_xy),
            np.asarray(scene.arms["S"].centerline_xy),
        ) and vs.canonical_scene_text(scene).count(
            json.dumps(
                [vs.encode_float(v) for v in np.asarray(scene.arms["C1"].decisions[-1].p_class).tolist()],
                separators=(",", ":"),
            )
        ) >= 2
        if arms_equal:
            indistinguishable.append(case_id)
    assert "indistinguishable_softening" in indistinguishable


def test_v17_fixture_carries_the_schema_default_non_finite_values(bundle):
    """`+inf` severity scale and a pre-detection `NaN`: what a real role will carry."""

    found_inf = False
    found_nan = False
    for scene in bundle.scenes.values():
        for key in vs.SUITE_KEYS:
            for decision in scene.arms[key].decisions:
                found_inf |= math.isinf(float(decision.severity_uncertainty))
                found_nan |= math.isnan(float(decision.detection_time_s))
    assert found_inf and found_nan


def test_v17_fixture_does_not_flatter_one_suite_across_the_menu(bundle):
    """A fixture whose every case favoured S would invite the reading this design prevents."""

    smaller_for = {"C1": 0, "S": 0}
    for scene in bundle.scenes.values():
        integrals = {
            key: j_5s(
                scene.playback_t_s,
                scene.arms[key].tracking.task_reference,
                scene.arms[key].tracking.true_task_output,
                float(scene.body_change.change.onset_time_s),
                window_s=float(scene.arms[key].tracking.window_s),
            )
            for key in vs.SUITE_KEYS
        }
        if integrals["C1"] < integrals["S"]:
            smaller_for["C1"] += 1
        elif integrals["S"] < integrals["C1"]:
            smaller_for["S"] += 1
    assert smaller_for["C1"] >= 1 and smaller_for["S"] >= 1


def test_fixture_distal_body_point_is_the_recorded_task_output(bundle):
    """Design property 6 / V16: the drawn body ends where the recorded output is."""

    for scene in bundle.scenes.values():
        for key in vs.SUITE_KEYS:
            vs.require_distal_point_matches_task_output(scene.arms[key])


def test_the_distal_point_check_has_a_failing_side(bundle):
    """The check is not vacuous: a displaced body refuses."""

    scene = _scene(bundle)
    arm = scene.arms["C1"]
    displaced = np.asarray(arm.centerline_xy, dtype=float).copy()
    displaced[:, -1, 0] += 0.01
    with pytest.raises(ValueError):
        vs.require_distal_point_matches_task_output(_arm_with(arm, centerline_xy=displaced))


# --------------------------------------------------------------------------- #
# The derived frame and the frame guard.
# --------------------------------------------------------------------------- #
def test_derived_frame_is_the_control_sample_at_the_window_close(bundle):
    """The scripted still is drawn where the shaded band closes, not at an arbitrary frame."""

    for scene in bundle.scenes.values():
        frame = vs.derived_frame(scene)
        target = float(scene.body_change.change.onset_time_s) + scene.window_s
        assert abs(float(np.asarray(scene.playback_t_s)[frame]) - target) <= 1.0e-9


@pytest.mark.parametrize("frame", [-1, 141, 10**6, 1.0, "3", None, True])
def test_frame_guard_refuses_and_never_clamps(bundle, frame):
    """An out-of-range or non-integer frame raises; nothing is silently moved into range."""

    with pytest.raises(vs.VerificationSceneError) as refusal:
        vs.require_frame(_scene(bundle), frame)
    assert refusal.value.code == vs.X_TIMEBASE_MISMATCH


def test_frame_guard_accepts_every_in_range_index(bundle):
    """The accept side, at both boundaries."""

    scene = _scene(bundle)
    assert vs.require_frame(scene, 0) == 0
    assert vs.require_frame(scene, scene.n_frames - 1) == scene.n_frames - 1
    assert vs.require_frame(scene, np.int64(5)) == 5


# --------------------------------------------------------------------------- #
# Exit-code table and V18.
# --------------------------------------------------------------------------- #
def test_exit_code_table_has_twelve_refusals_and_one_success():
    """The section-4.3 table, pinned by count and by the one zero exit."""

    assert len(vs.EXIT_CODES) == 13
    zero = [name for name, code in vs.EXIT_CODES.items() if code == 0]
    assert zero == [vs.X_SCENE_OK]
    assert len(set(vs.EXIT_CODES.values())) == 13


def test_a_refusal_cannot_be_raised_under_the_success_code():
    """`X_SCENE_OK` is not a refusal and cannot be used as one."""

    with pytest.raises(ValueError):
        raise vs.VerificationSceneError(vs.X_SCENE_OK, "not a refusal")
    with pytest.raises(ValueError):
        raise vs.VerificationSceneError("X_NOT_A_CODE", "not a code")


def test_v18_neither_module_imports_torch_or_mujoco():
    """Asserted in a fresh interpreter, because import side effects are what matter."""

    probe = (
        "import sys;"
        f"sys.path.insert(0, {str(SCRIPTS_DIR)!r});"
        "import matplotlib;matplotlib.use('Agg');"
        "import utils.verification_scene, render_verification_scene;"
        "print('torch' in sys.modules, 'mujoco' in sys.modules)"
    )
    completed = subprocess.run(
        [sys.executable, "-c", probe], capture_output=True, text=True, check=True
    )
    assert completed.stdout.strip() == "False False"
