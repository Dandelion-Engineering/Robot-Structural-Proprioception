"""Slot-8 verification surfaces: one pure painter, two wrappers (design step 2).

This is the executable half of `protocol/slot8-verification-artifact-v0.1.md`. It
carries the shared scene painter

    draw_scene(scene, *, frame) -> matplotlib.figure.Figure

and the two surfaces that are functions of a `VerificationBundle` and nothing else:
the director's interactive menu (`InteractiveVerificationSurface`) and the scripted
300-DPI figure path (`render_bundle`). Both call the same painter, so "the same
comparison" is a single source rather than a property maintained by hand across two
code paths.

**A renderer opens no scientific input.** The painter and the interactive wrapper do
no file I/O at all; the scripted wrapper writes only its declared PNG / scene-JSON /
bundle-JSON / digest outputs beneath the `--output-dir` it was given. Neither surface
can reach a role, a checkpoint or a config: the only reachable construction path in
this round is the synthetic fixture, and `roles` mode refuses with
`X_CONNECTION_UNAUTHORIZED` before opening anything.

**No cross-arm derived number appears anywhere.** Both arms' quantities are drawn
side by side, which is what Slot 8 asks for; a C1-minus-S difference, ratio or
reduction is not drawn, computed or labelled (design section 6 item 4, invariant
V14). The confirmatory comparison that would license one has not been run.

Usage (from the packet directory):

    ..\\venv\\Scripts\\python.exe scripts\\render_verification_scene.py fixture \\
        --fixture-seed 7 --output-dir results\\verification_fixture

Fixture mode writes the deterministic figure set and then opens the interactive menu
when the active matplotlib backend is an interactive one; under a non-interactive
backend it reports that and returns.
"""

from __future__ import annotations

import argparse
import hashlib
import sys
from pathlib import Path, PurePosixPath, PureWindowsPath
from typing import Any, Mapping, Sequence

import matplotlib
import numpy as np
from matplotlib.backends.backend_agg import FigureCanvasAgg
from matplotlib.figure import Figure

from utils.metrics import SOURCE_CLASS_ORDER
from utils.verification_scene import (
    ABSTAIN_TEXT,
    BUNDLE_VERSION,
    DISCLAIMER_DEVELOPMENT_ONLY,
    DISCLAIMER_FIXTURE_NOT_EVIDENCE,
    DISCLAIMER_NOT_THE_QUESTION,
    EXIT_CODES,
    FABRICATED_TRUTH_TEXT,
    HIGH_UNKNOWN_TEXT,
    NO_DECISION_TEXT,
    SUITE_KEYS,
    SYNTHETIC_FIXTURE,
    DEVELOPMENT_ONLY,
    UNAVAILABLE_TEXT,
    UNLOCALIZED_TEXT,
    VerificationBundle,
    VerificationScene,
    VerificationSceneError,
    X_BUNDLE_INCOMPLETE,
    X_IDENTITY_MISMATCH,
    X_SCENE_OK,
    banner_text,
    build_fixture_bundle,
    build_role_bundle,
    canonical_bundle_text,
    canonical_scene_text,
    decision_at_frame,
    derived_frame,
    require_frame,
    validate_bundle,
)

FIGURE_SIZE_IN: tuple[float, float] = (12.0, 8.5)
FIGURE_DPI = 100
SAVE_DPI = 300
BUNDLE_JSON_NAME = "verification_bundle.json"
BUNDLE_DIGEST_NAME = "verification_bundle.sha256"

# Suite styling. Two visually distinguishable bodies, labelled by suite (A2).
SUITE_STYLE: dict[str, dict[str, Any]] = {
    "C1": {"color": "#1f4e79", "linestyle": "-", "marker": "o"},
    "S": {"color": "#b8531a", "linestyle": "--", "marker": "s"},
}

# Pinned so the scripted path is byte-reproducible under the pinned matplotlib.
_RC_PARAMS: dict[str, Any] = {
    "font.family": "DejaVu Sans",
    "font.size": 8.0,
    "axes.titlesize": 9.0,
    "axes.labelsize": 8.0,
    "xtick.labelsize": 7.0,
    "ytick.labelsize": 7.0,
    "figure.autolayout": False,
    "savefig.transparent": False,
    "path.simplify": False,
}

_NON_INTERACTIVE_BACKENDS = {"agg", "cairo", "pdf", "pgf", "ps", "svg", "template"}


def _project_relative_output_dir(value: str) -> Path:
    """Parse the section-4.2 output directory without letting it escape the packet.

    Both Windows and POSIX rooted forms are refused so the same CLI contract holds
    on either platform. Parent traversal is refused for the same reason: a path can
    be lexically relative while still naming a destination outside the copied
    packet. This is CLI validation, before any output is written.
    """

    windows = PureWindowsPath(value)
    posix = PurePosixPath(value)
    if (
        windows.is_absolute()
        or posix.is_absolute()
        or bool(windows.drive)
        or bool(windows.root)
        or ".." in windows.parts
        or ".." in posix.parts
    ):
        raise argparse.ArgumentTypeError(
            "output directory must be project-relative and contain no parent traversal"
        )
    return Path(value)


# --------------------------------------------------------------------------- #
# Panel text. Derived from the scene alone, so a test can read what a director
# reads without scraping pixels.
# --------------------------------------------------------------------------- #
def call_text(scene: VerificationScene, suite: str, frame: int) -> str:
    """The known-class call for one arm at one frame, following the packet scorer.

    A stored `abstain_decision=True` renders `ABSTAIN`; otherwise the call is
    `SOURCE_CLASS_ORDER[argmax(p_class)]`. Before the first decision the panel is in
    the `NO DECISION YET` state and borrows nothing from the future.
    """

    decision = decision_at_frame(scene, suite, frame)
    if decision is None:
        return NO_DECISION_TEXT
    if bool(decision.abstain_decision):
        return ABSTAIN_TEXT
    return SOURCE_CLASS_ORDER[int(np.argmax(np.asarray(decision.p_class, dtype=float)))]


def _severity_text(severity_out: float, severity_uncertainty: float) -> str:
    """Severity beside its non-negative, config-defined error scale.

    The scale is never called an interval: no frozen contract gives it coverage
    semantics, and an infinite scale renders as `UNAVAILABLE` rather than as a plot
    extent.
    """

    scale = float(severity_uncertainty)
    if not np.isfinite(scale):
        return f"severity {float(severity_out):.3f}, error scale {UNAVAILABLE_TEXT}"
    return f"severity {float(severity_out):.3f}, error scale {scale:.3f}"


def call_panel_lines(scene: VerificationScene, suite: str, frame: int) -> list[str]:
    """Every line the call/confidence panel prints for one arm at one frame."""

    decision = decision_at_frame(scene, suite, frame)
    if decision is None:
        return [f"suite {suite}", NO_DECISION_TEXT]
    probabilities = np.asarray(decision.p_class, dtype=float)
    unknown = float(decision.unknown_score)
    unknown_state = (
        HIGH_UNKNOWN_TEXT
        if unknown >= float(scene.thresholds.unknown_threshold)
        else "unknown below threshold"
    )
    location = int(decision.location_out)
    location_text = UNLOCALIZED_TEXT if location < 0 else f"joint {location}"
    detection = float(decision.detection_time_s)
    detection_text = (
        UNAVAILABLE_TEXT if np.isnan(detection) else f"{detection:.3f} s"
    )
    return [
        f"suite {suite}",
        f"call {call_text(scene, suite, frame)}",
        f"confidence {float(np.max(probabilities)):.3f}",
        f"unknown score {unknown:.3f} ({unknown_state})",
        f"location {location_text}",
        _severity_text(decision.severity_out, decision.severity_uncertainty),
        f"first detection {detection_text}",
        f"decision step {int(decision.step)} at {float(decision.decision_time_s):.3f} s",
    ]


def provenance_lines(scene: VerificationScene) -> list[str]:
    """What the picture is made of (A5). On screen and in every saved figure."""

    provenance = scene.provenance
    roles = ", ".join(provenance.roles_read) if provenance.roles_read else "none"
    identities = "  |  ".join(
        f"{key} run {provenance.arms[key].run_id}" for key in SUITE_KEYS
    )
    return [
        f"provenance {provenance.state}  |  bundle {scene.bundle_version}  |  "
        f"case {scene.case_id}",
        f"config {provenance.config_identity}  |  connection record "
        f"{provenance.connection_record_id}  |  split {provenance.split}  |  "
        f"roles read: {roles}",
        f"{identities}  |  fixture seed {provenance.fixture_seed}",
    ]


def disclaimer_lines(scene: VerificationScene) -> list[str]:
    """Design section 6 items 1-3, printed in the artifact rather than in a caption."""

    lines = [DISCLAIMER_NOT_THE_QUESTION]
    if scene.provenance.state == SYNTHETIC_FIXTURE:
        lines.append(DISCLAIMER_FIXTURE_NOT_EVIDENCE)
    if scene.provenance.state == DEVELOPMENT_ONLY:
        lines.append(DISCLAIMER_DEVELOPMENT_ONLY)
    return lines


def truth_text(scene: VerificationScene) -> str | None:
    """The label struct, marked as fabricated on a synthetic scene (D4, V9)."""

    if scene.truth is None:
        return None
    truth = scene.truth
    prefix = f"{FABRICATED_TRUTH_TEXT}: " if scene.provenance.state == SYNTHETIC_FIXTURE else ""
    location = UNLOCALIZED_TEXT if int(truth.location) < 0 else f"joint {int(truth.location)}"
    return (
        f"{prefix}{truth.source_class} / {truth.subtype} at {location}, severity "
        f"{float(truth.severity):.3f}, onset {float(truth.onset_time_s):.3f} s"
    )


# --------------------------------------------------------------------------- #
# The three panels (design 4.5).
# --------------------------------------------------------------------------- #
def _draw_bodies(axis, scene: VerificationScene, frame: int) -> None:
    """Panel 1: both arms' planar centerlines at `frame`, over their faint sweep."""

    playback = np.asarray(scene.playback_t_s, dtype=float)
    reference = np.asarray(scene.arms[SUITE_KEYS[0]].tracking.task_reference, dtype=float)
    axis.plot(
        reference[:, 0],
        reference[:, 1],
        color="#555555",
        linewidth=0.8,
        alpha=0.5,
        label="task reference path",
    )
    axis.plot(
        [reference[frame, 0]],
        [reference[frame, 1]],
        color="#555555",
        marker="*",
        markersize=9.0,
        linestyle="none",
        label="reference at this frame",
    )
    for key in SUITE_KEYS:
        arm = scene.arms[key]
        style = SUITE_STYLE[key]
        centerline = np.asarray(arm.centerline_xy, dtype=float)
        tip = np.asarray(arm.tracking.true_task_output, dtype=float)
        axis.plot(
            tip[:, 0],
            tip[:, 1],
            color=style["color"],
            linewidth=0.7,
            alpha=0.25,
            linestyle=style["linestyle"],
        )
        axis.plot(
            centerline[frame, :, 0],
            centerline[frame, :, 1],
            color=style["color"],
            linewidth=2.2,
            linestyle=style["linestyle"],
            marker=style["marker"],
            markersize=4.0,
            label=f"suite {key} body",
        )
    onset = float(scene.body_change.change.onset_time_s)
    axis.set_title(
        f"{scene.case_id}: {scene.body_change.label}\n"
        f"body change onset {onset:.3f} s   |   frame {frame} of {scene.n_frames - 1} "
        f"at t = {float(playback[frame]):.3f} s"
    )
    axis.set_xlabel("x (m)")
    axis.set_ylabel("y (m)")
    points = np.concatenate(
        [np.asarray(scene.arms[key].centerline_xy, dtype=float).reshape(-1, 2)
         for key in SUITE_KEYS]
        + [reference]
    )
    span = float(np.max(np.abs(points))) * 1.15 or 1.0
    axis.set_xlim(-span, span)
    axis.set_ylim(-span, span)
    axis.set_aspect("equal", adjustable="box")
    axis.grid(True, linewidth=0.3, alpha=0.4)
    axis.legend(
        loc="center left", bbox_to_anchor=(1.02, 0.5), fontsize=7.0, framealpha=0.9
    )


def _draw_call_panel(axis, scene: VerificationScene, suite: str, frame: int) -> None:
    """Panel 2 for one arm: class probabilities, the call, and the abstain/unknown state."""

    decision = decision_at_frame(scene, suite, frame)
    style = SUITE_STYLE[suite]
    positions = np.arange(len(SOURCE_CLASS_ORDER), dtype=float)
    if decision is None:
        axis.bar(positions, np.zeros(len(SOURCE_CLASS_ORDER)), color="#cccccc")
    else:
        probabilities = np.asarray(decision.p_class, dtype=float)
        colors = [
            "#999999" if bool(decision.abstain_decision) else style["color"]
            for _ in SOURCE_CLASS_ORDER
        ]
        axis.bar(positions, probabilities, color=colors)
    axis.axhline(
        float(scene.thresholds.abstain_threshold),
        color="#000000",
        linewidth=0.8,
        linestyle=":",
    )
    axis.set_xticks(positions)
    axis.set_xticklabels(SOURCE_CLASS_ORDER, rotation=20.0, ha="right")
    # Headroom above the simplex so the read-out block never sits over a bar.
    axis.set_ylim(0.0, 1.55)
    axis.set_yticks([0.0, 0.25, 0.5, 0.75, 1.0])
    axis.set_ylabel("class probability")
    axis.set_title(f"call and confidence - suite {suite}")
    axis.text(
        0.02,
        0.98,
        "\n".join(call_panel_lines(scene, suite, frame)[1:]),
        transform=axis.transAxes,
        va="top",
        ha="left",
        fontsize=6.5,
        bbox={"boxstyle": "round", "facecolor": "#ffffff", "alpha": 0.85, "linewidth": 0.4},
    )


def _draw_tracking_panel(axis, scene: VerificationScene, suite: str, frame: int, ymax: float) -> None:
    """Panel 3 for one arm: the per-sample quantity `j_5s` integrates, on shared axes."""

    playback = np.asarray(scene.playback_t_s, dtype=float)
    arm = scene.arms[suite]
    error = np.linalg.norm(
        np.asarray(arm.tracking.task_reference, dtype=float)
        - np.asarray(arm.tracking.true_task_output, dtype=float),
        axis=1,
    )
    onset = float(scene.body_change.change.onset_time_s)
    window_end = onset + float(arm.tracking.window_s)
    axis.axvspan(onset, window_end, color="#f0d58c", alpha=0.45)
    axis.axvline(onset, color="#000000", linewidth=0.8, linestyle="-")
    axis.axvline(float(playback[frame]), color=SUITE_STYLE[suite]["color"], linewidth=1.0)
    axis.plot(playback, error, color=SUITE_STYLE[suite]["color"], linewidth=1.2)
    axis.set_xlim(float(playback[0]), float(playback[-1]))
    axis.set_ylim(0.0, ymax)
    axis.set_xlabel("t (s)")
    axis.set_ylabel("tracking error norm (m)")
    axis.set_title(f"tracking error - suite {suite}")
    axis.text(
        0.97,
        0.05,
        f"shaded band [{onset:.3f}, {window_end:.3f}] s\nis the analysis window",
        transform=axis.transAxes,
        va="bottom",
        ha="right",
        fontsize=6.0,
    )
    axis.grid(True, linewidth=0.3, alpha=0.4)


def draw_scene(scene: VerificationScene, *, frame: int) -> Figure:
    """Paint one scene at one playback frame. The one source both surfaces share.

    Args:
        scene: a validated `VerificationScene`.
        frame: an integer index into `scene.playback_t_s`.

    Returns:
        A new `matplotlib.figure.Figure`. The painter is pure: it opens nothing,
        writes nothing, and holds no state between calls.

    Raises:
        VerificationSceneError: `X_TIMEBASE_MISMATCH` when `frame` is not an integer
            index inside the playback grid. It never clamps -- a clamped slider shows
            the wrong instant while every panel still looks consistent -- and the CLI
            is what turns this exception into the exit code.
    """

    index = require_frame(scene, frame)
    with matplotlib.rc_context(_RC_PARAMS):
        figure = Figure(figsize=FIGURE_SIZE_IN, dpi=FIGURE_DPI)
        grid = figure.add_gridspec(
            2,
            4,
            left=0.055,
            right=0.985,
            top=0.815,
            bottom=0.115,
            hspace=0.45,
            wspace=0.42,
            height_ratios=[1.55, 1.0],
        )
        _draw_bodies(figure.add_subplot(grid[0, :]), scene, index)

        ymax = 0.0
        for key in SUITE_KEYS:
            arm = scene.arms[key]
            error = np.linalg.norm(
                np.asarray(arm.tracking.task_reference, dtype=float)
                - np.asarray(arm.tracking.true_task_output, dtype=float),
                axis=1,
            )
            ymax = max(ymax, float(np.max(error)))
        ymax = ymax * 1.15 if ymax > 0.0 else 1.0

        for column, key in enumerate(SUITE_KEYS):
            _draw_call_panel(figure.add_subplot(grid[1, column]), scene, key, index)
            _draw_tracking_panel(
                figure.add_subplot(grid[1, 2 + column]), scene, key, index, ymax
            )

        banner = banner_text(scene.provenance.state)
        figure.text(
            0.5,
            0.988,
            banner,
            ha="center",
            va="top",
            fontsize=15.0,
            fontweight="bold",
            color="#7a1010" if scene.provenance.state != "FINAL" else "#103a10",
            bbox={"boxstyle": "square", "facecolor": "#ffe9e9", "linewidth": 0.6},
        )
        for offset, line in enumerate(provenance_lines(scene)):
            figure.text(0.5, 0.952 - 0.016 * offset, line, ha="center", va="top", fontsize=6.5)
        marked_truth = truth_text(scene)
        if marked_truth is not None:
            figure.text(
                0.5,
                0.952 - 0.016 * len(provenance_lines(scene)),
                marked_truth,
                ha="center",
                va="top",
                fontsize=7.0,
                fontweight="bold",
            )
        for offset, line in enumerate(disclaimer_lines(scene)):
            figure.text(0.5, 0.055 - 0.019 * offset, line, ha="center", va="top", fontsize=7.0)
        return figure


# --------------------------------------------------------------------------- #
# The scripted surface (design 4.6). Writes only its declared outputs.
# --------------------------------------------------------------------------- #
def _write_bytes(path: Path, payload: bytes) -> None:
    """Write exact bytes, so no platform newline translation can reach an artifact."""

    with open(path, "wb") as handle:
        handle.write(payload)


def _contained_output_paths(destination: Path, names: Sequence[str]) -> dict[str, Path]:
    """Resolve every file this bundle will write, proving each is a direct child.

    Args:
        destination: the bundle output directory.
        names: every file name the bundle is about to write, in any order.

    Returns:
        `name -> resolved path`, for every name.

    Raises:
        VerificationSceneError: `X_IDENTITY_MISMATCH` when any composed path is not a
            direct child of `destination`. **This build adds no refusal code**, per
            the standing ruling that a code is not invented for a branch nobody has
            built. The existing code is the right one on its own terms: the read
            order gives `X_IDENTITY_MISMATCH` to every claim that some named object
            is at some named place, and a write that lands outside its declared root
            is exactly that claim failing.

    Design 4.7 says the adapter writes exactly the declared output set under
    `<output-dir>/<record_label>/` and nothing outside that root, and W10 makes the
    root exclusive-create. Both statements are about *paths*, and every per-case path
    here is composed from `case_id`. While the only bundles that existed were built
    in-process by this packet, `case_id` was a key nobody could aim; once a connection
    record supplies it, a value such as `../escape` writes beside the requested
    directory rather than inside it -- and `Path.name` in the returned manifest would
    report the innocent leaf. `utils.connection_record` refuses that value at the
    record boundary. This is the second, independent layer, held where the write
    actually happens, so the guarantee does not depend on every future producer of a
    bundle having applied the first one.

    The whole write set is resolved *before* the first byte is written, and there is
    exactly one call site. Both properties are deliberate: a per-write guard would
    leave earlier files already on disk when a later name refused, and a guard
    duplicated at each write would have branches no test could distinguish -- delete
    the second one and every observable behaviour stays the same, which is a check
    that holds nothing.
    """

    resolved_destination = destination.resolve()
    outputs: dict[str, Path] = {}
    for name in names:
        candidate = (destination / name).resolve()
        if candidate.parent != resolved_destination:
            raise VerificationSceneError(
                X_IDENTITY_MISMATCH,
                f"the scripted figure set would write {candidate}, which is not a "
                f"direct child of its output root {destination}",
            )
        outputs[name] = candidate
    return outputs


def render_bundle(bundle: VerificationBundle, output_dir: Path) -> dict[str, Any]:
    """Write the deterministic figure set for a whole bundle.

    Args:
        bundle: the validated menu. Every case in it is rendered; a scripted set that
            dropped a case would refuse rather than silently publish a subset.
        output_dir: the supplied, project-relative destination.

    Returns:
        A manifest naming every written file, the derived frame each still was drawn
        at, and the canonical bundle digest.
    """

    # V1 applies to the surfaces, not only to the builders. Validate before the
    # destination exists so an incomplete menu cannot leave a partial publication.
    validate_bundle(bundle)
    destination = Path(output_dir)
    destination.mkdir(parents=True, exist_ok=True)

    # The complete write set, proved contained before anything is written.
    names = [BUNDLE_JSON_NAME, BUNDLE_DIGEST_NAME]
    for case_id in bundle.scenes:
        names.extend((f"{case_id}.png", f"{case_id}.json"))
    outputs = _contained_output_paths(destination, names)

    bundle_text = canonical_bundle_text(bundle)
    bundle_bytes = bundle_text.encode("utf-8")
    digest = hashlib.sha256(bundle_bytes).hexdigest()
    _write_bytes(outputs[BUNDLE_JSON_NAME], bundle_bytes)
    _write_bytes(outputs[BUNDLE_DIGEST_NAME], (digest + "\n").encode("utf-8"))

    cases: list[dict[str, Any]] = []
    for case_id, scene in bundle.scenes.items():
        frame = derived_frame(scene)
        figure = draw_scene(scene, frame=frame)
        FigureCanvasAgg(figure)
        png_path = outputs[f"{case_id}.png"]
        figure.savefig(
            png_path,
            format="png",
            dpi=SAVE_DPI,
            metadata={
                "Title": f"{BUNDLE_VERSION} {case_id}",
                "Description": (
                    f"{banner_text(scene.provenance.state)} | "
                    f"{' | '.join(provenance_lines(scene))} | "
                    f"{' '.join(disclaimer_lines(scene))}"
                ),
            },
        )
        _write_bytes(
            outputs[f"{case_id}.json"], canonical_scene_text(scene).encode("utf-8")
        )
        cases.append(
            {
                "case_id": case_id,
                "frame": frame,
                "png": png_path.name,
                "scene_json": f"{case_id}.json",
            }
        )
    if [case["case_id"] for case in cases] != list(bundle.scenes):
        raise VerificationSceneError(
            X_BUNDLE_INCOMPLETE, "the scripted figure set does not cover every bundle case"
        )
    return {
        "bundle_version": bundle.bundle_version,
        "provenance_state": bundle.provenance_state,
        "bundle_json": BUNDLE_JSON_NAME,
        "bundle_sha256": digest,
        "save_dpi": SAVE_DPI,
        "cases": cases,
    }


# --------------------------------------------------------------------------- #
# The interactive surface (design 4.5 panel 1, requirements A1/A2, decision D2).
# --------------------------------------------------------------------------- #
class InteractiveVerificationSurface:
    """The director's menu: pick a case, scrub or play the timeline, no typing.

    The surface never paints anything itself. Every update calls the same
    `draw_scene(scene, frame=...)` the scripted path calls and displays the result,
    so the two surfaces cannot diverge. It performs no file I/O.
    """

    def __init__(self, bundle: VerificationBundle, *, frame_interval_ms: int = 120) -> None:
        # V1 and property 8 are surface gates too. In particular, duplicate human-
        # readable labels cannot safely back a radio-button label -> case mapping.
        validate_bundle(bundle)

        import matplotlib.pyplot as plt
        from matplotlib.widgets import Button, RadioButtons, Slider

        self.bundle = bundle
        self.case_ids = list(bundle.scenes)
        self.case_labels = [bundle.scenes[case_id].body_change.label for case_id in self.case_ids]
        self._case_id_by_label = dict(zip(self.case_labels, self.case_ids))
        self.case_id = self.case_ids[0]
        self.frame = 0
        self.playing = False
        self.frame_interval_ms = int(frame_interval_ms)
        self._animation = None

        self.figure = plt.figure(figsize=(FIGURE_SIZE_IN[0], FIGURE_SIZE_IN[1] + 1.1),
                                 dpi=FIGURE_DPI)
        self._canvas_axis = self.figure.add_axes((0.0, 0.16, 1.0, 0.84))
        self._canvas_axis.set_axis_off()
        self._image = self._canvas_axis.imshow(self._paint())

        self._radio_axis = self.figure.add_axes((0.03, 0.01, 0.30, 0.13))
        self._radio_axis.set_title("body change", fontsize=8.0)
        self.radio = RadioButtons(self._radio_axis, tuple(self.case_labels))
        self.radio.on_clicked(self.select_label)

        self._slider_axis = self.figure.add_axes((0.42, 0.075, 0.44, 0.03))
        self.slider = Slider(
            self._slider_axis,
            "frame",
            0,
            self._n_frames() - 1,
            valinit=0,
            valstep=1,
        )
        self.slider.on_changed(self.set_frame)

        self._button_axis = self.figure.add_axes((0.90, 0.06, 0.08, 0.06))
        self.button = Button(self._button_axis, "play / pause")
        self.button.on_clicked(self.toggle_play)

    # -- state ------------------------------------------------------------- #
    @property
    def scene(self) -> VerificationScene:
        """The scene the menu currently selects."""

        return self.bundle.scenes[self.case_id]

    def _n_frames(self) -> int:
        """The playback length of the selected scene."""

        return self.scene.n_frames

    def _paint(self) -> np.ndarray:
        """Render the shared painter's figure to an RGBA buffer for display."""

        figure = draw_scene(self.scene, frame=self.frame)
        canvas = FigureCanvasAgg(figure)
        canvas.draw()
        return np.asarray(canvas.buffer_rgba())

    def _refresh(self) -> None:
        """Repaint through the shared painter and push the result to the display."""

        self._image.set_data(self._paint())
        self.figure.canvas.draw_idle()

    # -- widget callbacks --------------------------------------------------- #
    def select_case(self, case_id: str) -> None:
        """Select one case by its stable internal ID."""

        if case_id not in self.bundle.scenes:
            raise VerificationSceneError(
                X_BUNDLE_INCOMPLETE, f"{case_id!r} is not a case in this bundle"
            )
        self.case_id = case_id
        self.frame = min(self.frame, self._n_frames() - 1)
        self.slider.valmax = self._n_frames() - 1
        self.slider.ax.set_xlim(0, self._n_frames() - 1)
        self.slider.set_val(self.frame)
        self._refresh()

    def select_label(self, label: str) -> None:
        """Radio callback: choose the human-readable body change shown in the menu (A1)."""

        try:
            case_id = self._case_id_by_label[label]
        except KeyError:
            raise VerificationSceneError(
                X_BUNDLE_INCOMPLETE, f"{label!r} is not a display label in this bundle"
            ) from None
        self.select_case(case_id)

    def set_frame(self, value: Any) -> None:
        """Slider callback: move the timeline (A2)."""

        self.frame = require_frame(self.scene, int(value))
        self._refresh()

    def advance_frame(self, *_: Any) -> None:
        """One animation step: wrap and move the visible timeline with the picture."""

        self.slider.set_val((self.frame + 1) % self._n_frames())

    def toggle_play(self, *_: Any) -> None:
        """Button callback: play/pause the animation (A2)."""

        self.playing = not self.playing
        if self._animation is None:
            return
        if self.playing:
            self._animation.resume()
        else:
            self._animation.pause()

    def launch(self) -> None:
        """Attach the animation and, on an interactive backend, show the window."""

        import matplotlib.pyplot as plt
        from matplotlib.animation import FuncAnimation

        self._animation = FuncAnimation(
            self.figure,
            self.advance_frame,
            interval=self.frame_interval_ms,
            cache_frame_data=False,
        )
        # Draw once so the animation actually starts before it is paused; an
        # animation that is discarded without ever drawing warns at collection.
        self.figure.canvas.draw()
        self._animation.pause()
        self.playing = False
        if matplotlib.get_backend().lower() in _NON_INTERACTIVE_BACKENDS:
            print(
                f"interactive menu built for {len(self.case_ids)} cases; the active "
                f"matplotlib backend {matplotlib.get_backend()!r} is non-interactive, "
                f"so no window is shown"
            )
            return
        plt.show()


def launch_interactive(bundle: VerificationBundle) -> InteractiveVerificationSurface:
    """Build and launch the director's interactive surface."""

    surface = InteractiveVerificationSurface(bundle)
    surface.launch()
    return surface


# --------------------------------------------------------------------------- #
# CLI (design 4.2). Two subcommands, no scientific default anywhere.
# --------------------------------------------------------------------------- #
def build_parser() -> argparse.ArgumentParser:
    """The two mode-specific parsers. Mode selection is structural, not a flag."""

    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    modes = parser.add_subparsers(dest="mode", required=True)

    fixture = modes.add_parser(
        "fixture", help="build and render the labeled synthetic fixture bundle"
    )
    fixture.add_argument("--fixture-seed", type=int, required=True)
    fixture.add_argument("--output-dir", type=_project_relative_output_dir, required=True)

    roles = modes.add_parser(
        "roles", help="specified real-result path; refuses without a connection record"
    )
    roles.add_argument("--connection-record", type=Path, required=True)
    roles.add_argument("--connection-record-sha256", type=str, required=True)
    roles.add_argument("--config", type=Path, required=True)
    roles.add_argument("--checkpoint-root", type=Path, required=True)
    roles.add_argument("--role-root", type=Path, required=True)
    roles.add_argument("--output-dir", type=_project_relative_output_dir, required=True)
    return parser


def parse_args(argv: Sequence[str] | None = None) -> argparse.Namespace:
    """Parse the CLI arguments for one mode."""

    return build_parser().parse_args(argv)


def _fixture_mode(args: argparse.Namespace) -> int:
    """Build the fixture bundle, write the figure set, then open the menu."""

    bundle = build_fixture_bundle(int(args.fixture_seed))
    manifest = render_bundle(bundle, Path(args.output_dir))
    print(
        f"wrote {len(manifest['cases'])} scripted cases at {SAVE_DPI} DPI to "
        f"{Path(args.output_dir)}"
    )
    for case in manifest["cases"]:
        print(f"  {case['case_id']}: {case['png']} at frame {case['frame']}")
    print(f"bundle sha256 {manifest['bundle_sha256']}")
    launch_interactive(bundle)
    print(f"{X_SCENE_OK}: fixture bundle rendered")
    return EXIT_CODES[X_SCENE_OK]


def _roles_mode(args: argparse.Namespace) -> int:
    """Refuse before opening anything: no connection record exists in this packet."""

    build_role_bundle(
        connection_record=str(args.connection_record),
        connection_record_sha256=str(args.connection_record_sha256),
        config=str(args.config),
        checkpoint_root=str(args.checkpoint_root),
        role_root=str(args.role_root),
    )
    raise AssertionError("unreachable: build_role_bundle always refuses in this round")


def main(argv: Sequence[str] | None = None) -> int:
    """Run one mode and return the exit code of the terminal exit it took."""

    args = parse_args(argv)
    try:
        if args.mode == "fixture":
            return _fixture_mode(args)
        return _roles_mode(args)
    except VerificationSceneError as refusal:
        print(str(refusal), file=sys.stderr)
        return EXIT_CODES[refusal.code]


if __name__ == "__main__":  # pragma: no cover - exercised through main(argv)
    sys.exit(main())
