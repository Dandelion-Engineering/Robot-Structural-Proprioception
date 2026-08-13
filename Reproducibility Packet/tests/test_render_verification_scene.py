"""Tests for the Slot-8 verification surfaces: the shared painter and both wrappers.

Every figure under test is painted from the packet's own labeled synthetic fixture.
No test reads a role, an index, a checkpoint, a config or a split, and the CLI's role
subcommand is driven only to watch it refuse before opening anything. All rendering
runs under the non-interactive Agg backend, so no window is ever opened.

Invariants carried in this file (the scene half lives in `test_verification_scene.py`):

    V1  a surface that drops a case refuses      V11 the banner is inside the PNG
    V2  role mode refuses before any read        V13 the scripted path is deterministic
    V4  mode-specific parsers, no defaults       V14 no cross-arm derived scalar (artist half)
    V5  fail closed on roles                     V16 body and call panels share one timeline
    V9  every non-FINAL scene renders a banner   V17 the visible failure branches render
    V10 a renderer opens no scientific input     V19 an infinite scale draws UNAVAILABLE
"""

from __future__ import annotations

import ast
import dataclasses
import filecmp
import hashlib
import json
import re
import struct
import sys
from pathlib import Path

import matplotlib

matplotlib.use("Agg")

import numpy as np  # noqa: E402
import pytest  # noqa: E402

PACKET_ROOT = Path(__file__).resolve().parents[1]
SCRIPTS_DIR = PACKET_ROOT / "scripts"
sys.path.insert(0, str(SCRIPTS_DIR))

import render_verification_scene as rv  # noqa: E402
from utils import verification_scene as vs  # noqa: E402
from utils.metrics import SOURCE_CLASS_ORDER  # noqa: E402

FIXTURE_SEED = 7


@pytest.fixture(scope="module")
def bundle() -> vs.VerificationBundle:
    """The labeled synthetic fixture bundle every test in this file renders."""

    return vs.build_fixture_bundle(FIXTURE_SEED)


@pytest.fixture(scope="module")
def rendered(tmp_path_factory, bundle) -> tuple[Path, dict]:
    """One scripted figure set, rendered once and shared by the read-only checks."""

    destination = tmp_path_factory.mktemp("scripted")
    return destination, rv.render_bundle(bundle, destination)


def _texts(figure) -> list[str]:
    """Every string a reader can see in a painted figure, artists included."""

    found = [artist.get_text() for artist in figure.findobj(match=matplotlib.text.Text)]
    return [text for text in found if text]


def _png_chunks(path: Path) -> list[tuple[bytes, bytes]]:
    """Every (type, payload) chunk of a PNG, parsed from the bytes on disk."""

    data = path.read_bytes()
    assert data[:8] == b"\x89PNG\r\n\x1a\n"
    chunks: list[tuple[bytes, bytes]] = []
    offset = 8
    while offset < len(data):
        (length,) = struct.unpack(">I", data[offset : offset + 4])
        kind = data[offset + 4 : offset + 8]
        payload = data[offset + 8 : offset + 8 + length]
        chunks.append((kind, payload))
        offset += 12 + length
    return chunks


# --------------------------------------------------------------------------- #
# V4 - mode-specific parsers with no scientific defaults.
# --------------------------------------------------------------------------- #
def _subparser_actions(name: str):
    """The `argparse` actions of one subcommand, with the help action excluded."""

    parser = rv.build_parser()
    (subparsers,) = [
        action
        for action in parser._actions
        if isinstance(action, __import__("argparse")._SubParsersAction)
    ]
    subparser = subparsers.choices[name]
    return [
        action
        for action in subparser._actions
        if not isinstance(action, __import__("argparse")._HelpAction)
    ]


@pytest.mark.parametrize(
    ("mode", "expected"),
    [
        ("fixture", {"--fixture-seed", "--output-dir"}),
        (
            "roles",
            {
                "--connection-record",
                "--connection-record-sha256",
                "--config",
                "--checkpoint-root",
                "--role-root",
                "--output-dir",
            },
        ),
    ],
)
def test_v4_each_subcommand_has_exactly_its_declared_argument_set(mode, expected):
    """Equality, not containment: a new flag fails this rather than passing quietly."""

    options = set()
    for action in _subparser_actions(mode):
        options.update(action.option_strings)
    assert options == expected


@pytest.mark.parametrize("mode", ["fixture", "roles"])
def test_v4_every_declared_argument_is_required(mode):
    """No default silently selects today's development state."""

    for action in _subparser_actions(mode):
        assert action.required, action.option_strings
        assert action.default is None


@pytest.mark.parametrize("mode", ["fixture", "roles"])
def test_v4_no_provenance_authority_split_or_allowlist_override_exists(mode):
    """The four overrides that would turn a label into something a caller can assert."""

    forbidden = ("provenance", "authority", "split", "role", "allow", "force", "dev")
    for action in _subparser_actions(mode):
        for option in action.option_strings:
            lowered = option.lower()
            if option in {"--role-root", "--connection-record", "--connection-record-sha256"}:
                continue
            assert not any(token in lowered for token in forbidden), option


def test_v4_mode_selection_is_structural_not_a_flag():
    """Mutual exclusion comes from the subparser boundary, not two `required=True` flags."""

    import argparse

    parser = rv.build_parser()
    subparsers = [a for a in parser._actions if isinstance(a, argparse._SubParsersAction)]
    assert len(subparsers) == 1
    assert subparsers[0].required
    assert set(subparsers[0].choices) == {"fixture", "roles"}
    with pytest.raises(SystemExit):
        rv.parse_args([])


def test_v4_fixture_mode_rejects_every_role_argument():
    """A role argument on the fixture parser is an error, not an ignored extra."""

    for option in (
        "--connection-record",
        "--connection-record-sha256",
        "--config",
        "--checkpoint-root",
        "--role-root",
    ):
        with pytest.raises(SystemExit):
            rv.parse_args(["fixture", "--fixture-seed", "7", "--output-dir", "x", option, "y"])


def test_v4_role_mode_rejects_the_fixture_argument():
    """And the converse."""

    with pytest.raises(SystemExit):
        rv.parse_args(
            [
                "roles",
                "--connection-record",
                "r",
                "--connection-record-sha256",
                "h",
                "--config",
                "c",
                "--checkpoint-root",
                "k",
                "--role-root",
                "o",
                "--output-dir",
                "d",
                "--fixture-seed",
                "7",
            ]
        )


@pytest.mark.parametrize(
    "output_dir",
    [
        str(Path.cwd().resolve() / "absolute-output"),
        "C:\\absolute-output",
        "\\rooted-output",
        "/absolute-output",
        "..\\outside",
        "../outside",
    ],
)
@pytest.mark.parametrize("mode", ["fixture", "roles"])
def test_v4_output_directory_is_project_relative_without_traversal(mode, output_dir):
    """The section-4.2 path rule is enforced by the CLI, not left in prose."""

    if mode == "fixture":
        argv = ["fixture", "--fixture-seed", "7", "--output-dir", output_dir]
    else:
        argv = [
            "roles",
            "--connection-record",
            "record.json",
            "--connection-record-sha256",
            "0" * 64,
            "--config",
            "config.json",
            "--checkpoint-root",
            "checkpoints",
            "--role-root",
            "roles",
            "--output-dir",
            output_dir,
        ]
    with pytest.raises(SystemExit):
        rv.parse_args(argv)


# --------------------------------------------------------------------------- #
# V2 / V5 - fail closed on roles, before anything is opened.
# --------------------------------------------------------------------------- #
def test_v2_role_mode_exits_with_the_connection_code(capsys, tmp_path, monkeypatch):
    """The CLI turns the refusal into its own distinct non-zero exit."""

    monkeypatch.chdir(tmp_path)
    code = rv.main(
        [
            "roles",
            "--connection-record",
            str(tmp_path / "record.json"),
            "--connection-record-sha256",
            "0" * 64,
            "--config",
            str(tmp_path / "config.json"),
            "--checkpoint-root",
            str(tmp_path / "ckpt"),
            "--role-root",
            str(tmp_path / "roles"),
            "--output-dir",
            "out",
        ]
    )
    assert code == vs.EXIT_CODES[vs.X_CONNECTION_UNAUTHORIZED]
    assert code != 0
    assert vs.X_CONNECTION_UNAUTHORIZED in capsys.readouterr().err


def test_v5_role_mode_produces_no_scene_no_figure_and_no_output_directory(tmp_path, monkeypatch):
    """Fail closed: nothing is created, not even the directory it was told to write to."""

    monkeypatch.chdir(tmp_path)
    output = tmp_path / "out"
    rv.main(
        [
            "roles",
            "--connection-record",
            str(tmp_path / "record.json"),
            "--connection-record-sha256",
            "0" * 64,
            "--config",
            str(tmp_path / "config.json"),
            "--checkpoint-root",
            str(tmp_path / "ckpt"),
            "--role-root",
            str(tmp_path / "roles"),
            "--output-dir",
            "out",
        ]
    )
    assert not output.exists()
    assert list(tmp_path.iterdir()) == []


# --------------------------------------------------------------------------- #
# V9 - every non-FINAL scene renders its banner, in the figure.
# --------------------------------------------------------------------------- #
def test_v9_every_fixture_scene_paints_the_synthetic_banner(bundle):
    """The banner is a figure artist, not a caption and not a filename."""

    for scene in bundle.scenes.values():
        figure = rv.draw_scene(scene, frame=vs.derived_frame(scene))
        assert vs.BANNERS[vs.SYNTHETIC_FIXTURE] in _texts(figure)


def test_v9_fixture_truth_renders_only_as_fabricated_truth(bundle):
    """D4: fabricated truth is legible, and never as an unqualified correctness mark."""

    for scene in bundle.scenes.values():
        assert scene.truth is not None
        texts = _texts(rv.draw_scene(scene, frame=vs.derived_frame(scene)))
        marked = [text for text in texts if vs.FABRICATED_TRUTH_TEXT in text]
        assert len(marked) == 1
        assert scene.truth.source_class in marked[0]
        joined = " ".join(texts).upper()
        for verdict in ("CORRECT CALL", "GROUND TRUTH", "VERIFIED", "PASS"):
            assert verdict not in joined


def test_v9_the_three_disclaimers_are_printed_in_the_artifact(bundle):
    """Design section 6 items 1-3 appear in the picture, not only in this repository."""

    scene = next(iter(bundle.scenes.values()))
    texts = _texts(rv.draw_scene(scene, frame=0))
    assert vs.DISCLAIMER_NOT_THE_QUESTION in texts
    assert vs.DISCLAIMER_FIXTURE_NOT_EVIDENCE in texts


def test_v9_provenance_is_on_screen(bundle):
    """A5: what the picture is made of, every time."""

    scene = next(iter(bundle.scenes.values()))
    joined = " ".join(_texts(rv.draw_scene(scene, frame=0)))
    assert vs.SYNTHETIC_FIXTURE in joined
    assert scene.case_id in joined
    assert "roles read: none" in joined


# --------------------------------------------------------------------------- #
# V10 - a renderer opens no scientific input.
# --------------------------------------------------------------------------- #
def test_v10_the_painter_renders_with_no_roles_anywhere(monkeypatch, tmp_path, bundle):
    """Called from an empty working directory, with every read path booby-trapped."""

    monkeypatch.chdir(tmp_path)

    def _forbidden(*args, **kwargs):
        raise AssertionError("the painter opened a file")

    monkeypatch.setattr("builtins.open", _forbidden)
    monkeypatch.setattr(Path, "open", _forbidden)
    monkeypatch.setattr(Path, "read_bytes", _forbidden)
    monkeypatch.setattr(Path, "read_text", _forbidden)
    for scene in bundle.scenes.values():
        assert rv.draw_scene(scene, frame=0) is not None


def test_v10_the_scripted_path_writes_only_its_declared_outputs(rendered, bundle):
    """One PNG and one scene JSON per case, plus the bundle document and its digest."""

    destination, manifest = rendered
    expected = {rv.BUNDLE_JSON_NAME, rv.BUNDLE_DIGEST_NAME}
    for case_id in bundle.scenes:
        expected.add(f"{case_id}.png")
        expected.add(f"{case_id}.json")
    assert {path.name for path in destination.iterdir()} == expected
    assert manifest["bundle_sha256"] == hashlib.sha256(
        (destination / rv.BUNDLE_JSON_NAME).read_bytes()
    ).hexdigest()


def test_v1_both_surfaces_refuse_an_incomplete_menu_before_any_output(tmp_path, bundle):
    """V1 is a surface gate: a builder bypass cannot publish or display a subset."""

    scenes = {
        case_id: scene
        for case_id, scene in bundle.scenes.items()
        if scene.body_change.change.source_class != "sensor"
    }
    partial = dataclasses.replace(bundle, scenes=scenes)
    destination = tmp_path / "partial"
    with pytest.raises(vs.VerificationSceneError) as scripted:
        rv.render_bundle(partial, destination)
    assert scripted.value.code == vs.X_BUNDLE_INCOMPLETE
    assert not destination.exists()
    with pytest.raises(vs.VerificationSceneError) as interactive:
        rv.InteractiveVerificationSurface(partial)
    assert interactive.value.code == vs.X_BUNDLE_INCOMPLETE


def test_v10_the_painter_and_the_interactive_surface_contain_no_write_call():
    """Structurally: only the scripted wrapper is allowed to touch the filesystem."""

    tree = ast.parse((SCRIPTS_DIR / "render_verification_scene.py").read_text(encoding="utf-8"))
    writers = {"savefig", "write_bytes", "write_text", "mkdir", "open", "_write_bytes"}
    for node in ast.walk(tree):
        is_painter = isinstance(node, ast.FunctionDef) and node.name in {
            "draw_scene",
            "_draw_bodies",
            "_draw_call_panel",
            "_draw_tracking_panel",
        }
        is_surface = isinstance(node, ast.ClassDef) and node.name == (
            "InteractiveVerificationSurface"
        )
        if not (is_painter or is_surface):
            continue
        called = set()
        for inner in ast.walk(node):
            if isinstance(inner, ast.Call):
                called.add(getattr(inner.func, "attr", None) or getattr(inner.func, "id", None))
        assert not (called & writers), (node.name, sorted(called & writers))


# --------------------------------------------------------------------------- #
# V11 - the banner is inside the PNG, and the resolution is checked where it is stored.
# --------------------------------------------------------------------------- #
def test_v11_the_banner_survives_into_the_saved_png_bytes(rendered, bundle):
    """A caption is separable from the image the moment someone copies the PNG."""

    destination, _ = rendered
    for case_id in bundle.scenes:
        data = (destination / f"{case_id}.png").read_bytes()
        assert vs.BANNERS[vs.SYNTHETIC_FIXTURE].encode("ascii") in data
        assert vs.DISCLAIMER_FIXTURE_NOT_EVIDENCE.encode("ascii") in data


def test_v11_phys_payload_is_exactly_the_stored_form_of_300_dpi(rendered, bundle):
    """PNG stores integer pixels per metre, so `>= 300` goes red on a correct figure."""

    destination, manifest = rendered
    assert manifest["save_dpi"] == rv.SAVE_DPI == 300
    expected = round(300 / 0.0254)
    assert expected == 11811
    for case_id in bundle.scenes:
        phys = [payload for kind, payload in _png_chunks(destination / f"{case_id}.png")
                if kind == b"pHYs"]
        assert len(phys) == 1
        x_ppm, y_ppm, unit = struct.unpack(">IIB", phys[0])
        assert (x_ppm, y_ppm, unit) == (expected, expected, 1)
        assert x_ppm * 0.0254 < 300.0  # the check that would have failed


# --------------------------------------------------------------------------- #
# V13 - the scripted path is deterministic and complete.
# --------------------------------------------------------------------------- #
def test_v13_the_same_bundle_renders_byte_identically_twice(tmp_path, bundle):
    """Same bundle, same environment, same bytes."""

    first = tmp_path / "a"
    second = tmp_path / "b"
    rv.render_bundle(bundle, first)
    rv.render_bundle(bundle, second)
    names = sorted(path.name for path in first.iterdir())
    assert names == sorted(path.name for path in second.iterdir())
    for name in names:
        assert filecmp.cmp(first / name, second / name, shallow=False), name


def test_v13_output_case_ids_equal_bundle_case_ids_exactly(rendered, bundle):
    """A scripted set that dropped a case would be publishing a subset."""

    _, manifest = rendered
    assert [case["case_id"] for case in manifest["cases"]] == list(bundle.scenes)


def test_v13_every_still_is_drawn_at_the_derived_frame(rendered, bundle):
    """The frame is derived from the scene, so the surface stays a function of the bundle."""

    _, manifest = rendered
    for case in manifest["cases"]:
        assert case["frame"] == vs.derived_frame(bundle.scenes[case["case_id"]])


def test_v13_the_written_scene_documents_are_the_canonical_ones(rendered, bundle):
    """Any figure in any report can be traced to the exact scene that produced it."""

    destination, _ = rendered
    for case_id, scene in bundle.scenes.items():
        written = (destination / f"{case_id}.json").read_bytes()
        assert written == vs.canonical_scene_text(scene).encode("utf-8")
        assert vs.scene_from_json(vs.loads_strict(written.decode("utf-8"))).case_id == case_id


def test_v13_cli_fixture_mode_writes_the_same_set(tmp_path, bundle, capsys, monkeypatch):
    """The one-command reproduction path (A6) produces the reviewed bytes."""

    monkeypatch.chdir(tmp_path)
    output = tmp_path / "cli"
    code = rv.main(["fixture", "--fixture-seed", str(FIXTURE_SEED), "--output-dir", "cli"])
    assert code == vs.EXIT_CODES[vs.X_SCENE_OK] == 0
    reference = tmp_path / "reference"
    rv.render_bundle(bundle, reference)
    for path in reference.iterdir():
        assert filecmp.cmp(path, output / path.name, shallow=False), path.name
    assert vs.X_SCENE_OK in capsys.readouterr().out


# --------------------------------------------------------------------------- #
# V14 (artist half) - no cross-arm derived number is drawn.
# --------------------------------------------------------------------------- #
_CROSS_ARM_PATTERN = re.compile(
    r"reduction|difference|delta|ratio|minus|improvement|advantage|"
    r"c1\s*(?:-|vs|versus|over)\s*s\b|s\s*(?:-|vs|versus|over)\s*c1\b",
    re.IGNORECASE,
)


def test_v14_no_painted_text_carries_a_cross_arm_quantity(bundle):
    """Read off the rendered artists, at several frames, in every case."""

    for scene in bundle.scenes.values():
        for frame in (0, 30, 60, vs.derived_frame(scene), scene.n_frames - 1):
            for text in _texts(rv.draw_scene(scene, frame=frame)):
                assert not _CROSS_ARM_PATTERN.search(text), text


def test_v14_the_renderer_never_references_the_reduction_metric():
    """`tracking_reduction_pct` is not imported, named or called."""

    source = (SCRIPTS_DIR / "render_verification_scene.py").read_text(encoding="utf-8")
    assert "tracking_reduction_pct" not in source


# --------------------------------------------------------------------------- #
# V16 - the body and call panels share one causal timeline.
# --------------------------------------------------------------------------- #
def _body_lines(figure) -> list[np.ndarray]:
    """The vertices of every line drawn in the body panel."""

    axis = figure.axes[0]
    return [line.get_xydata().copy() for line in axis.lines]


def test_v16_two_frames_give_different_body_artists(bundle):
    """Otherwise the animation requirement is satisfied by a still."""

    for scene in bundle.scenes.values():
        early = _body_lines(rv.draw_scene(scene, frame=25))
        late = _body_lines(rv.draw_scene(scene, frame=vs.derived_frame(scene)))
        assert len(early) == len(late)
        assert any(
            first.shape != second.shape or not np.array_equal(first, second)
            for first, second in zip(early, late)
        )


def test_v16_both_arms_identify_the_same_playback_time_at_one_frame(bundle):
    """One frame, one physical time, drawn into the title both arms share."""

    scene = next(iter(bundle.scenes.values()))
    frame = 88
    expected = float(np.asarray(scene.playback_t_s)[frame])
    joined = " ".join(_texts(rv.draw_scene(scene, frame=frame)))
    assert f"t = {expected:.3f} s" in joined


def test_v16_a_frame_before_the_first_decision_renders_no_decision_yet(bundle):
    """And borrows no probability, call, unknown, location or severity from the future."""

    scene = bundle.scenes["soften_link_2"]
    for key in vs.SUITE_KEYS:
        assert rv.call_panel_lines(scene, key, 5) == [f"suite {key}", vs.NO_DECISION_TEXT]
    joined = " ".join(_texts(rv.draw_scene(scene, frame=5)))
    assert joined.count(vs.NO_DECISION_TEXT) == len(vs.SUITE_KEYS)
    # Nothing from either future decision is on screen: no read-out line, no call,
    # no probability, no unknown state, no location, no severity, no detection time.
    # "call " alone would match the panel title "call and confidence - suite C1";
    # the read-out line's absence is already pinned by the equality above.
    for leaked in (
        "confidence 0",
        "unknown score",
        "location ",
        "error scale",
        "first detection",
        "decision step",
        vs.ABSTAIN_TEXT,
        vs.UNAVAILABLE_TEXT,
    ):
        assert leaked not in joined, leaked


def test_v16_an_intermediate_frame_renders_the_greatest_decision_not_later_than_it(bundle):
    """The settled final diagnosis is not shown early."""

    scene = bundle.scenes["soften_link_2"]
    playback = np.asarray(scene.playback_t_s, dtype=float)
    first, second = scene.arms["S"].decisions
    middle = int(np.flatnonzero(playback < float(second.decision_time_s))[-1])
    joined = " ".join(_texts(rv.draw_scene(scene, frame=middle)))
    assert f"decision step {int(first.step)}" in joined
    assert f"decision step {int(second.step)}" not in joined
    assert rv.call_text(scene, "S", middle) == vs.ABSTAIN_TEXT
    assert rv.call_text(scene, "S", scene.n_frames - 1) == "structure"


def test_v16_the_scripted_frame_is_the_shared_sample_at_the_window_close(bundle):
    """Panel 1's pose is the pose at the moment panel 3's shaded window closes."""

    for scene in bundle.scenes.values():
        frame = vs.derived_frame(scene)
        target = float(scene.body_change.change.onset_time_s) + scene.window_s
        assert abs(float(np.asarray(scene.playback_t_s)[frame]) - target) <= 1.0e-9


def test_v16_out_of_range_frames_raise_rather_than_clamp(bundle):
    """A clamped slider shows the wrong instant while every panel still looks consistent."""

    scene = next(iter(bundle.scenes.values()))
    for frame in (-1, scene.n_frames, 2.5, None):
        with pytest.raises(vs.VerificationSceneError) as refusal:
            rv.draw_scene(scene, frame=frame)
        assert refusal.value.code == vs.X_TIMEBASE_MISMATCH


def test_v16_a_non_monotone_decision_axis_refuses_before_a_renderer_sees_it(bundle):
    """`X_DECISION_UNSUPPORTED` fires at construction, not in the painter."""

    import dataclasses

    scene = bundle.scenes["soften_link_2"]
    arm = scene.arms["C1"]
    with pytest.raises(vs.VerificationSceneError) as refusal:
        vs.build_fixture_scene(
            case_id=scene.body_change.case_id,
            label=scene.body_change.label,
            change=scene.body_change.change,
            playback_t_s=scene.playback_t_s,
            arms={
                "C1": dataclasses.replace(arm, decisions=(arm.decisions[1], arm.decisions[0])),
                "S": scene.arms["S"],
            },
            truth=scene.truth,
            thresholds=scene.thresholds,
            fixture_seed=scene.provenance.fixture_seed,
        )
    assert refusal.value.code == vs.X_DECISION_UNSUPPORTED


# --------------------------------------------------------------------------- #
# V17 (artist half) - the visible failure branches actually render.
# --------------------------------------------------------------------------- #
def test_v17_the_rendered_calls_cover_correct_wrong_and_abstain(bundle):
    """Read from the painted panels, compared against the painted fabricated truth."""

    seen = {"correct": False, "wrong": False, "abstain": False}
    for scene in bundle.scenes.values():
        frame = vs.derived_frame(scene)
        texts = " ".join(_texts(rv.draw_scene(scene, frame=frame)))
        truth = scene.truth.source_class
        assert f"{vs.FABRICATED_TRUTH_TEXT}: {truth}" in texts
        for key in vs.SUITE_KEYS:
            call = rv.call_text(scene, key, frame)
            assert f"call {call}" in texts
            if call == vs.ABSTAIN_TEXT:
                seen["abstain"] = True
            elif call == truth:
                seen["correct"] = True
            else:
                seen["wrong"] = True
    assert all(seen.values()), seen


def test_v17_a_high_unknown_state_renders_as_its_own_state(bundle):
    """It does not silently rewrite the stored abstention decision."""

    scene = bundle.scenes["bias_encoder_1"]
    frame = vs.derived_frame(scene)
    texts = " ".join(_texts(rv.draw_scene(scene, frame=frame)))
    assert texts.count(vs.HIGH_UNKNOWN_TEXT) == len(vs.SUITE_KEYS)
    # C1 answers anyway; the high unknown score did not turn its call into an abstention.
    assert rv.call_text(scene, "C1", frame) != vs.ABSTAIN_TEXT
    assert rv.call_text(scene, "S", frame) == vs.ABSTAIN_TEXT


def test_v17_the_indistinguishable_case_renders_the_same_call_for_both_arms(bundle):
    """The honest negative shown *as* a result."""

    scene = bundle.scenes["indistinguishable_softening"]
    frame = vs.derived_frame(scene)
    assert rv.call_text(scene, "C1", frame) == rv.call_text(scene, "S", frame)
    assert rv.call_panel_lines(scene, "C1", frame)[1:] == rv.call_panel_lines(scene, "S", frame)[1:]


def test_v17_every_menu_entry_is_exposed_by_both_surfaces(bundle, rendered):
    """A surface that dropped a case would be publishing a subset."""

    destination, manifest = rendered
    assert [case["case_id"] for case in manifest["cases"]] == list(bundle.scenes)
    surface = rv.InteractiveVerificationSurface(bundle)
    assert list(surface.radio.labels[i].get_text() for i in range(len(surface.case_ids))) == list(
        scene.body_change.label for scene in bundle.scenes.values()
    )
    # Drive every visible entry, not one of them: the claim CP repairs is that the
    # displayed label selects its own case, and one index leaves the rest unexercised.
    for index, case_id in enumerate(bundle.scenes):
        surface.radio.set_active(index)
        assert surface.case_id == case_id


def test_v17_the_class_axis_is_the_canonical_source_class_order(bundle):
    """A reader comparing a figure to a table never has to check the order."""

    scene = next(iter(bundle.scenes.values()))
    figure = rv.draw_scene(scene, frame=vs.derived_frame(scene))
    call_axes = [axis for axis in figure.axes if "call and confidence" in axis.get_title()]
    assert len(call_axes) == len(vs.SUITE_KEYS)
    for axis in call_axes:
        assert [label.get_text() for label in axis.get_xticklabels()] == list(SOURCE_CLASS_ORDER)


# --------------------------------------------------------------------------- #
# V19 (renderer half) - an infinite scale draws UNAVAILABLE, not a plot extent.
# --------------------------------------------------------------------------- #
def test_v19_infinite_severity_scale_renders_unavailable(bundle):
    """The value the fixture carries because a real role will carry it."""

    scene = bundle.scenes["soften_link_2"]
    frame = vs.derived_frame(scene)
    lines = rv.call_panel_lines(scene, "C1", frame)
    assert any(f"error scale {vs.UNAVAILABLE_TEXT}" in line for line in lines)
    joined = " ".join(_texts(rv.draw_scene(scene, frame=frame)))
    assert vs.UNAVAILABLE_TEXT in joined
    for axis in rv.draw_scene(scene, frame=frame).axes:
        assert all(np.isfinite(axis.get_ylim())) and all(np.isfinite(axis.get_xlim()))


def test_v19_a_pre_detection_nan_renders_unavailable_not_a_number(bundle):
    """Never a silent zero, and never a fabricated detection time."""

    scene = bundle.scenes["soften_link_2"]
    lines = rv.call_panel_lines(scene, "C1", vs.derived_frame(scene))
    assert f"first detection {vs.UNAVAILABLE_TEXT}" in lines
    assert not any("nan" in line.lower() for line in lines)


# ASCII-only, like the rest of the packet: the plus-minus sign is written as its escape.
_INTERVAL_TOKENS = ("interval", "coverage", "+/-", "\u00b1")
_CI_WORD = re.compile(r"\bci\b", re.IGNORECASE)


def test_v19_the_severity_scale_is_never_called_an_interval():
    """No frozen contract gives the scale coverage semantics, so no panel may imply one."""

    fixture = vs.build_fixture_bundle(FIXTURE_SEED)
    checked = 0
    for scene in fixture.scenes.values():
        for text in _texts(rv.draw_scene(scene, frame=vs.derived_frame(scene))):
            lowered = text.lower()
            for token in _INTERVAL_TOKENS:
                assert token not in lowered, (token, text)
            assert _CI_WORD.search(text) is None, text
            checked += 1
    assert checked > 0


def test_the_interval_check_is_not_vacuous():
    """The tokens it looks for are ones this rule really would have to catch."""

    for token in _INTERVAL_TOKENS:
        assert token in f"severity 0.100 {token} 0.050".lower()
    assert _CI_WORD.search("severity 0.100, 95% CI") is not None
    assert _CI_WORD.search("confidence 0.850") is None


# --------------------------------------------------------------------------- #
# Decision D2 - the interactive surface really does menu, timeline and play/pause.
# --------------------------------------------------------------------------- #
def test_d2_the_interactive_surface_selects_a_case_without_typing(bundle):
    """A1: the radio menu is the whole selection mechanism."""

    surface = rv.InteractiveVerificationSurface(bundle)
    assert surface.case_id == list(bundle.scenes)[0]
    surface.select_case("bias_encoder_1")
    assert surface.case_id == "bias_encoder_1"
    assert surface.scene is bundle.scenes["bias_encoder_1"]


def test_d2_the_timeline_moves_the_frame(bundle):
    """A2: the slider drives the painter's `frame`, and the painted image changes."""

    surface = rv.InteractiveVerificationSurface(bundle)
    before = surface._image.get_array().copy()
    surface.set_frame(120)
    assert surface.frame == 120
    assert not np.array_equal(before, surface._image.get_array())


def test_d2_play_pause_toggles_and_advances(bundle):
    """A2: play/pause is a state, and playback moves the frame and visible timeline."""

    surface = rv.InteractiveVerificationSurface(bundle)
    assert surface.playing is False
    surface.toggle_play()
    assert surface.playing is True
    surface.toggle_play()
    assert surface.playing is False
    surface.frame = surface.scene.n_frames - 1
    surface.slider.set_val(surface.frame)
    surface.advance_frame()
    assert surface.frame == 0
    assert surface.slider.val == 0


def test_d2_the_interactive_surface_refuses_an_unknown_case(bundle):
    """The menu is data; a case that is not in the bundle is a refusal."""

    surface = rv.InteractiveVerificationSurface(bundle)
    with pytest.raises(vs.VerificationSceneError) as refusal:
        surface.select_case("not_a_case")
    assert refusal.value.code == vs.X_BUNDLE_INCOMPLETE


def test_d2_the_interactive_surface_refuses_an_unknown_display_label(bundle):
    """The label -> case map is data too, and its refusal side is a public branch.

    `select_case` already has this test; `select_label` is the method the radio
    actually calls, so its refusal is the one a director could reach.
    """

    surface = rv.InteractiveVerificationSurface(bundle)
    with pytest.raises(vs.VerificationSceneError) as refusal:
        surface.select_label("not a display label")
    assert refusal.value.code == vs.X_BUNDLE_INCOMPLETE
    # A case ID is not a display label, and must not select a case through this door.
    with pytest.raises(vs.VerificationSceneError):
        surface.select_label(list(bundle.scenes)[0])


def test_d2_launch_under_a_non_interactive_backend_opens_no_window(bundle, capsys):
    """The scaffold is demonstrable headless; a real display is not a test dependency."""

    surface = rv.InteractiveVerificationSurface(bundle)
    surface.launch()
    assert surface._animation is not None
    assert surface.playing is False
    assert "non-interactive" in capsys.readouterr().out


def test_the_interactive_surface_repaints_through_the_shared_painter(monkeypatch, bundle):
    """Both surfaces cannot diverge, because there is only one painter."""

    calls: list[tuple[str, int]] = []
    original = rv.draw_scene

    def _recording(scene, *, frame):
        calls.append((scene.case_id, frame))
        return original(scene, frame=frame)

    monkeypatch.setattr(rv, "draw_scene", _recording)
    surface = rv.InteractiveVerificationSurface(bundle)
    surface.set_frame(42)
    surface.select_case("weaken_actuator_1")
    assert ("soften_link_2", 42) in calls
    assert any(case_id == "weaken_actuator_1" for case_id, _ in calls)


# --------------------------------------------------------------------------- #
# The exit-code surface of the CLI.
# --------------------------------------------------------------------------- #
def test_the_cli_maps_every_refusal_to_its_own_distinct_exit_code():
    """A test can assert *which* refusal fired, which is the point of the table."""

    codes = [code for name, code in vs.EXIT_CODES.items() if name != vs.X_SCENE_OK]
    assert len(set(codes)) == len(codes)
    assert 0 not in codes


def test_the_renderer_imports_the_exit_table_rather_than_restating_it():
    """One definition of what each refusal means."""

    source = (SCRIPTS_DIR / "render_verification_scene.py").read_text(encoding="utf-8")
    assert "EXIT_CODES: dict" not in source
    assert "EXIT_CODES," in source
