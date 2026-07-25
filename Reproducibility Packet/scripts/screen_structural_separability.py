"""Development-only structure-versus-healthy separability screen (Gate-4 stop/go).

Purpose
-------
Claude's Session-33 measurement showed that the *interpretable* synchronous
coefficient distance produced by a link-stiffness loss sits below the project's
own 2.0x synchronous margin at every reserved structural severity.  That bounds
one rung; it does not establish whether the learned rung, which reads the raw
``[W, D]`` observed tensor, can separate structure from healthy at all.  Fitting
the Gate-4 capacity ladder before answering that question would make a null
result unattributable: hypothesis failure and method failure would look the same.

This screen answers the narrow question, on the delivered **development split
only**, before any validation or test payload is consumed:

    At the two reserved development structural severities (remaining EI 0.75 and
    0.50), can a detector separate structure runs from healthy runs, and does the
    structural suite S do better than the matched conventional suite C1?

It is a screen, not a headline result.  It fits nothing that is carried forward,
selects no hyperparameter that enters the confirmatory protocol, and touches no
split other than ``dev``.

Design
------
The delivered assignment gives, per fault setting, eight development runs whose
context cells (trajectory x payload x environment x contact) are *identical*
run-for-run across fault settings.  Every contrast here is therefore
**context-matched**: healthy run ``t{i}_r{j}`` and structure run ``t{i}_r{j}``
share trajectory, payload, environment and contact profile, and differ only in
the fault and the sensor seed.  Two consequences are used:

* Cross-validation holds out a *cell* (both of its runs), not a run, so a model
  can never be scored on a run whose context twin it was trained on.
* The per-cell score difference is a paired statistic, so an exact paired sign
  test over the eight cells is available and a paired label permutation
  (2^8 = 256 sign patterns) gives an exact null for the learned rung.

Two rungs are screened, both on the identical window set:

* **Interpretable rung** - ``CoefficientReferenceDetector``.  The healthy
  coefficient reference is fitted on the seven training cells' healthy windows;
  held-out healthy and fault windows are scored against it.
* **Learned rung** - an L2 logistic probe on the raw ``[W, D]`` tensor, reduced
  to 16 mean-pooled time bins plus per-column standard deviation and valid
  fraction.  The regularization strength is *maximised over a small grid*, which
  makes the reported separability an optimistic bound: the screening question is
  whether any separability exists, so an upper bound is the useful direction, and
  the permutation null applies the identical max-over-grid rule so the selection
  is inside the null.

Controls
--------
* **Positive control** - actuator gain loss at remaining gain 0.50 versus
  healthy.  Prior development evidence says a conventional suite detects this,
  so a pipeline that cannot separate it is broken rather than informative.
* **Negative control** - the paired label permutation null.  It measures what
  this pipeline reports when the labels carry no information, at this sample
  size, with this feature construction.

Outputs
-------
A JSON result artifact and a human-readable markdown report under the given
output directory.  Nothing is written into the dataset root.
"""

from __future__ import annotations

import argparse
import csv
import itertools
import json
import math
import sys
import time
from pathlib import Path
from typing import Iterable, Sequence

import numpy as np

SCRIPT_DIR = Path(__file__).resolve().parent
if str(SCRIPT_DIR) not in sys.path:
    sys.path.insert(0, str(SCRIPT_DIR))

from utils.estimator import (  # noqa: E402
    CoefficientReferenceDetector,
    WindowFeatureExtractor,
    coefficient_reference_distance,
    synchronous_coefficient_vector,
)
from utils.schema_types import CHANNEL_NAMES, CHANNEL_WIDTH, ObservedRecord  # noqa: E402

# This screen is authorised for the development split and nothing else.  The
# Gate-4 stop it answers exists precisely to avoid spending validation or test
# before the question is settled, so the restriction is enforced in code.
AUTHORISED_SPLIT = "dev"

# Fault settings screened, keyed by the label used throughout the report.
CONTRAST_SETTINGS: dict[str, str] = {
    "healthy": "fault_dev_healthy",
    "structure_rem_ei_0.75": "fault_dev_structure_link_stiffness_loss_loc1_sev0p75",
    "structure_rem_ei_0.50": "fault_dev_structure_link_stiffness_loss_loc1_sev0p5",
    "actuator_rem_gain_0.50": "fault_dev_actuator_actuator_gain_loss_loc1_sev0p5",
}
POSITIVE_CONTROL = "actuator_rem_gain_0.50"
CRITICAL_CONTRAST = "structure_rem_ei_0.75"

# Regularisation grid for the learned probe.  Kept small and fixed; the reported
# statistic is the maximum over it, and the permutation null uses the same rule.
PROBE_C_GRID: tuple[float, ...] = (0.01, 0.1, 1.0)
POOL_BINS = 16


class SeparabilityScreenError(RuntimeError):
    """Raised when the screen cannot run against the delivered data as specified."""


# --------------------------------------------------------------------------- #
# Data access
# --------------------------------------------------------------------------- #


def read_dev_manifest(dataset_root: Path) -> list[dict[str, str]]:
    """Return the development-split manifest rows, refusing any other split.

    Args:
        dataset_root: root of the delivered base dataset (must contain manifest.csv).

    Returns:
        The manifest rows whose ``split`` is the authorised development split.

    Raises:
        SeparabilityScreenError: if the manifest is missing or holds no dev rows.
    """

    manifest_path = dataset_root / "manifest.csv"
    if not manifest_path.is_file():
        raise SeparabilityScreenError(f"manifest.csv not found under {dataset_root}")
    with manifest_path.open(newline="", encoding="utf-8") as handle:
        rows = [row for row in csv.DictReader(handle) if row["split"] == AUTHORISED_SPLIT]
    if not rows:
        raise SeparabilityScreenError(
            f"no rows with split={AUTHORISED_SPLIT!r} in {manifest_path}"
        )
    return rows


def cell_key(row: dict[str, str]) -> str:
    """Return the context-cell key shared by matched runs across fault settings."""

    return (
        f"{row['trajectory_spec_id']}|{row['payload_id']}|"
        f"{row['env_profile_id']}|{row['contact_profile_id']}"
    )


def collect_runs(
    rows: Sequence[dict[str, str]], suite: str, trajectory_filter: str
) -> dict[str, dict[str, dict[str, str]]]:
    """Group the screened fault settings' rows by contrast label and context cell.

    Args:
        rows: development manifest rows.
        suite: deployable suite identifier (``C1`` or ``S``).
        trajectory_filter: ``all``, ``diagnostic`` or ``ordinary``.  The synchronous
            interpretable rung is keyed to the diagnostic probe, so pooling both
            trajectories dilutes it; the filter lets the screen be read either way.

    Returns:
        ``{contrast_label: {cell_key: manifest_row}}`` for every screened setting.

    Raises:
        SeparabilityScreenError: if a setting is missing runs or a cell is not unique.
    """

    grouped: dict[str, dict[str, dict[str, str]]] = {}
    for label, setting_id in CONTRAST_SETTINGS.items():
        selected = [
            row
            for row in rows
            if row["suite"] == suite
            and row["fault_setting_id"] == setting_id
            and (
                trajectory_filter == "all"
                or trajectory_filter in row["trajectory_spec_id"]
            )
        ]
        if not selected:
            raise SeparabilityScreenError(
                f"no {suite} rows for fault setting {setting_id!r}"
            )
        by_cell: dict[str, dict[str, str]] = {}
        for row in selected:
            key = cell_key(row)
            if key in by_cell:
                raise SeparabilityScreenError(
                    f"context cell {key!r} is not unique within {setting_id!r}"
                )
            by_cell[key] = row
        grouped[label] = by_cell
    reference_cells = set(grouped["healthy"])
    for label, by_cell in grouped.items():
        if set(by_cell) != reference_cells:
            raise SeparabilityScreenError(
                f"{label!r} does not span the same context cells as healthy; the "
                "contrast would not be context-matched"
            )
    return grouped


def slice_record(record: ObservedRecord, start: int, stop: int) -> ObservedRecord:
    """Return a copy of ``record`` restricted to control steps ``[start, stop)``.

    Args:
        record: full-length observed trace for one run.
        start: inclusive first control step of the window.
        stop: exclusive last control step of the window.

    Returns:
        An ``ObservedRecord`` carrying the same channel registry over the window.
    """

    if start < 0 or stop <= start or stop > record.n_steps:
        raise SeparabilityScreenError(
            f"window [{start}, {stop}) is outside the {record.n_steps}-step trace"
        )
    return ObservedRecord(
        suite=record.suite,
        run_id=record.run_id,
        pair_id=record.pair_id,
        config_hash=record.config_hash,
        schema_version=record.schema_version,
        split=record.split,
        values={name: record.values[name][start:stop] for name in CHANNEL_NAMES},
        valid_mask={name: record.valid_mask[name][start:stop] for name in CHANNEL_NAMES},
        measurement_time_s={
            name: record.measurement_time_s[name][start:stop] for name in CHANNEL_NAMES
        },
        availability_time_s={
            name: record.availability_time_s[name][start:stop] for name in CHANNEL_NAMES
        },
        latency_age_s={
            name: record.latency_age_s[name][start:stop] for name in CHANNEL_NAMES
        },
        suite_available_mask=dict(record.suite_available_mask),
    )


def onset_step(row: dict[str, str], assignment: dict, control_dt_s: float) -> int:
    """Return the fault-onset control step for a run's trajectory."""

    for spec in assignment["trajectory_specs"]:
        if spec["id"] == row["trajectory_spec_id"]:
            raw = float(spec["onset_time_s"]) / control_dt_s
            index = int(round(raw))
            if not math.isclose(raw, index, rel_tol=0.0, abs_tol=1.0e-9):
                raise SeparabilityScreenError(
                    f"onset {spec['onset_time_s']} s is not on the control grid"
                )
            return index
    raise SeparabilityScreenError(f"unknown trajectory {row['trajectory_spec_id']!r}")


def load_run_windows(
    dataset_root: Path,
    row: dict[str, str],
    suite: str,
    onset: int,
    window_steps: int,
    stride: int,
) -> list[ObservedRecord]:
    """Load one run and cut it into fully post-onset windows of fixed length.

    Args:
        dataset_root: delivered dataset root.
        row: the run's manifest row.
        suite: deployable suite identifier.
        onset: fault-onset control step for the run's trajectory.
        window_steps: fixed window length W.
        stride: step between consecutive window starts.

    Returns:
        Window sub-records, each exactly ``window_steps`` long and starting at or
        after the fault onset, so no window mixes pre- and post-change data.
    """

    path = dataset_root / "observations" / suite / f"{row['run_id']}.npz"
    if not path.is_file():
        raise SeparabilityScreenError(f"observation payload missing: {path}")
    record = ObservedRecord.load_npz(path)
    if record.split != AUTHORISED_SPLIT:
        raise SeparabilityScreenError(
            f"payload {path.name} declares split {record.split!r}, refusing to read it"
        )
    starts = range(onset, record.n_steps - window_steps + 1, stride)
    if not starts:
        raise SeparabilityScreenError(
            f"{row['run_id']}: no post-onset window of {window_steps} steps fits"
        )
    return [slice_record(record, s, s + window_steps) for s in starts]


# --------------------------------------------------------------------------- #
# Statistics
# --------------------------------------------------------------------------- #


def auroc(positive: Sequence[float], negative: Sequence[float]) -> float:
    """Return the rank-based AUROC of ``positive`` scores against ``negative``."""

    pos = np.asarray(positive, dtype=float)
    neg = np.asarray(negative, dtype=float)
    if pos.size == 0 or neg.size == 0:
        raise SeparabilityScreenError("AUROC needs at least one score in each class")
    combined = np.concatenate([pos, neg])
    order = combined.argsort(kind="mergesort")
    ranks = np.empty(combined.size, dtype=float)
    ranks[order] = np.arange(1, combined.size + 1, dtype=float)
    # Average ranks within ties so exact score ties score 0.5 rather than 0 or 1.
    unique, inverse, counts = np.unique(combined, return_inverse=True, return_counts=True)
    if counts.max() > 1:
        sums = np.zeros(unique.size, dtype=float)
        np.add.at(sums, inverse, ranks)
        ranks = (sums / counts)[inverse]
    rank_sum = ranks[: pos.size].sum()
    return float((rank_sum - pos.size * (pos.size + 1) / 2.0) / (pos.size * neg.size))


def paired_sign_test(differences: Sequence[float]) -> dict[str, float]:
    """Exact two-sided sign test on paired per-cell score differences."""

    diffs = np.asarray(differences, dtype=float)
    n_pos = int((diffs > 0).sum())
    n_neg = int((diffs < 0).sum())
    n = n_pos + n_neg
    if n == 0:
        return {"n_pairs": 0, "n_positive": 0, "p_value": 1.0}
    extreme = max(n_pos, n_neg)
    tail = sum(math.comb(n, k) for k in range(extreme, n + 1))
    return {
        "n_pairs": n,
        "n_positive": n_pos,
        "p_value": float(min(1.0, 2.0 * tail / (2.0**n))),
    }


def pool_features(values: np.ndarray, valid: np.ndarray, bins: int) -> np.ndarray:
    """Reduce one raw ``[W, D]`` window to a fixed feature vector.

    The reduction is ``bins`` mean-pooled time segments per registry column, plus
    each column's standard deviation over the window and its valid fraction.  A
    channel the suite lacks contributes zeros and a zero valid fraction, so the
    vector has identical width for C1 and S and the suite ablation stays matched.
    """

    window_steps, width = values.shape
    edges = np.linspace(0, window_steps, bins + 1).astype(int)
    pooled = np.stack(
        [values[edges[i] : edges[i + 1]].mean(axis=0) for i in range(bins)], axis=0
    )
    return np.concatenate(
        [pooled.reshape(-1), values.std(axis=0), valid.mean(axis=0)]
    ).astype(float)


def logistic_probe_scores(
    features: np.ndarray,
    labels: np.ndarray,
    groups: np.ndarray,
    c_value: float,
    max_iter: int,
) -> np.ndarray:
    """Leave-one-cell-out cross-validated decision scores for the linear probe.

    Args:
        features: ``[n_windows, n_features]`` reduced window features.
        labels: ``[n_windows]`` binary window labels (1 = fault).
        groups: ``[n_windows]`` context-cell index; a fold holds out one cell,
            which removes both that cell's healthy run and its fault run.
        c_value: inverse L2 regularisation strength.
        max_iter: solver iteration cap.

    Returns:
        ``[n_windows]`` decision scores, each produced by a model that never saw
        any window from the scored window's context cell.
    """

    from sklearn.linear_model import LogisticRegression

    scores = np.zeros(features.shape[0], dtype=float)
    for held in np.unique(groups):
        test = groups == held
        train = ~test
        train_x = features[train]
        mean = train_x.mean(axis=0)
        std = train_x.std(axis=0)
        keep = std > 0.0
        if not keep.any():
            raise SeparabilityScreenError("no non-constant feature in a training fold")
        scaled_train = (train_x[:, keep] - mean[keep]) / std[keep]
        scaled_test = (features[test][:, keep] - mean[keep]) / std[keep]
        model = LogisticRegression(
            C=c_value, max_iter=max_iter, solver="lbfgs", random_state=0
        )
        model.fit(scaled_train, labels[train])
        scores[test] = model.decision_function(scaled_test)
    return scores


def run_level(scores: np.ndarray, run_index: np.ndarray, n_runs: int) -> np.ndarray:
    """Collapse window scores to one mean score per run."""

    return np.array(
        [float(scores[run_index == i].mean()) for i in range(n_runs)], dtype=float
    )


# --------------------------------------------------------------------------- #
# Screen
# --------------------------------------------------------------------------- #


def screen_contrast(
    windows_by_label: dict[str, dict[str, list[ObservedRecord]]],
    fault_label: str,
    extractor: WindowFeatureExtractor,
    cells: Sequence[str],
    permutations: int,
    max_iter: int,
) -> dict:
    """Screen one fault-versus-healthy contrast on both rungs.

    Args:
        windows_by_label: ``{contrast_label: {cell_key: [window records]}}``.
        fault_label: the non-healthy contrast label being screened.
        extractor: shared window front-end (fixes W and the probe frequency).
        cells: ordered context-cell keys; each becomes one cross-validation fold.
        permutations: number of paired label sign patterns for the exact null
            (0 skips it; otherwise the first ``permutations`` of the 2^n patterns
            in Gray-code-free lexicographic order are used, always including the
            identity so the observed statistic is inside its own null).
        max_iter: logistic solver iteration cap.

    Returns:
        A result dictionary for this contrast.
    """

    healthy = windows_by_label["healthy"]
    fault = windows_by_label[fault_label]

    # ---- interpretable rung: leave-one-cell-out coefficient reference ------- #
    healthy_vectors = {
        cell: [synchronous_coefficient_vector(w, extractor) for w in healthy[cell]]
        for cell in cells
    }
    fault_vectors = {
        cell: [synchronous_coefficient_vector(w, extractor) for w in fault[cell]]
        for cell in cells
    }
    detector = CoefficientReferenceDetector(extractor)
    interp_healthy: list[float] = []
    interp_fault: list[float] = []
    for held in cells:
        train_vectors = np.stack(
            [v for cell in cells if cell != held for v in healthy_vectors[cell]]
        )
        mean = train_vectors.mean(axis=0)
        scale = detector._scale_from(mean, train_vectors.std(axis=0))  # noqa: SLF001
        interp_healthy.append(
            float(
                np.mean(
                    [
                        coefficient_reference_distance(v, mean, scale)
                        for v in healthy_vectors[held]
                    ]
                )
            )
        )
        interp_fault.append(
            float(
                np.mean(
                    [
                        coefficient_reference_distance(v, mean, scale)
                        for v in fault_vectors[held]
                    ]
                )
            )
        )
    interp_diffs = [f - h for f, h in zip(interp_fault, interp_healthy)]
    interpretable = {
        "run_auroc": auroc(interp_fault, interp_healthy),
        "healthy_mean_score": float(np.mean(interp_healthy)),
        "fault_mean_score": float(np.mean(interp_fault)),
        "median_paired_ratio": float(
            np.median([f / h if h > 0 else np.inf for f, h in zip(interp_fault, interp_healthy)])
        ),
        "paired_sign_test": paired_sign_test(interp_diffs),
        "per_cell": [
            {"cell": cell, "healthy": h, "fault": f}
            for cell, h, f in zip(cells, interp_healthy, interp_fault)
        ],
    }

    # ---- learned rung: leave-one-cell-out linear probe on the raw tensor ---- #
    feature_rows: list[np.ndarray] = []
    labels: list[int] = []
    groups: list[int] = []
    run_index: list[int] = []
    run_meta: list[tuple[str, int]] = []
    for cell_i, cell in enumerate(cells):
        for label_value, source in ((0, healthy), (1, fault)):
            run_id = len(run_meta)
            run_meta.append((cell, label_value))
            for window in source[cell]:
                values, valid = extractor.window_tensor(window)
                feature_rows.append(pool_features(values, valid, POOL_BINS))
                labels.append(label_value)
                groups.append(cell_i)
                run_index.append(run_id)
    features = np.stack(feature_rows)
    labels_arr = np.asarray(labels, dtype=int)
    groups_arr = np.asarray(groups, dtype=int)
    run_arr = np.asarray(run_index, dtype=int)
    run_labels = np.asarray([meta[1] for meta in run_meta], dtype=int)
    run_cells = np.asarray([cells.index(meta[0]) for meta in run_meta], dtype=int)

    def probe_auroc(active_labels: np.ndarray) -> tuple[float, float]:
        """Best-over-grid run-level AUROC for one labelling; returns (auroc, C)."""

        best = (-1.0, float("nan"))
        for c_value in PROBE_C_GRID:
            scores = logistic_probe_scores(
                features, active_labels, groups_arr, c_value, max_iter
            )
            per_run = run_level(scores, run_arr, len(run_meta))
            # Score each run under the labelling actually being tested.
            run_active = np.array(
                [active_labels[run_arr == i][0] for i in range(len(run_meta))]
            )
            value = auroc(per_run[run_active == 1], per_run[run_active == 0])
            if value > best[0]:
                best = (value, c_value)
        return best

    observed_auroc, observed_c = probe_auroc(labels_arr)
    observed_scores = logistic_probe_scores(
        features, labels_arr, groups_arr, observed_c, max_iter
    )
    observed_runs = run_level(observed_scores, run_arr, len(run_meta))
    learned_diffs = [
        float(
            observed_runs[(run_cells == i) & (run_labels == 1)][0]
            - observed_runs[(run_cells == i) & (run_labels == 0)][0]
        )
        for i in range(len(cells))
    ]

    learned = {
        "run_auroc_best_over_grid": observed_auroc,
        "selected_C": observed_c,
        "c_grid": list(PROBE_C_GRID),
        "n_windows": int(features.shape[0]),
        "n_features": int(features.shape[1]),
        "paired_sign_test": paired_sign_test(learned_diffs),
        "per_cell_score_difference": [
            {"cell": cell, "fault_minus_healthy": diff}
            for cell, diff in zip(cells, learned_diffs)
        ],
    }

    if permutations > 0:
        patterns = list(itertools.product([0, 1], repeat=len(cells)))
        if permutations < len(patterns):
            step = len(patterns) / permutations
            chosen = {0}
            chosen.update(int(i * step) for i in range(permutations))
            patterns = [patterns[i] for i in sorted(chosen)]
        null_values: list[float] = []
        started = time.time()
        for index, pattern in enumerate(patterns):
            permuted = labels_arr.copy()
            for cell_i, flip in enumerate(pattern):
                if flip:
                    in_cell = groups_arr == cell_i
                    permuted[in_cell] = 1 - permuted[in_cell]
            null_values.append(probe_auroc(permuted)[0])
            if (index + 1) % 32 == 0:
                elapsed = time.time() - started
                print(
                    f"      permutation {index + 1}/{len(patterns)}"
                    f"  ({elapsed:.0f}s elapsed)",
                    flush=True,
                )
        null = np.asarray(null_values, dtype=float)
        learned["permutation_null"] = {
            "n_patterns": int(null.size),
            "mean": float(null.mean()),
            "q95": float(np.quantile(null, 0.95)),
            "max": float(null.max()),
            "p_value": float((null >= observed_auroc).sum() / null.size),
        }

    return {
        "interpretable": interpretable,
        "learned": learned,
        "per_channel": per_channel_attribution(windows_by_label, fault_label, cells),
    }


def per_channel_attribution(
    windows_by_label: dict[str, dict[str, list[ObservedRecord]]],
    fault_label: str,
    cells: Sequence[str],
) -> list[dict]:
    """Paired per-registry-column comparison of a fault arm against healthy.

    For each registry column this reports the paired sign test over context cells
    and the mean absolute paired change expressed in units of the healthy
    across-cell spread.  It answers *which* channel carries whatever structural
    information exists, with no classifier in the loop, so an S-exclusive gauge
    result can be told apart from a C1-visible one.

    The statistic is the post-onset mean of ``|value|`` per column over a run's
    windows.  That is deliberately crude: for the gauges it includes the static
    payload bending and the thermal term, both of which are far larger than any
    fault effect, so this view *understates* the gauges relative to the
    synchronous statistic the interpretable rung uses.  It is reported as
    corroboration of that rung, not as a replacement for it.
    """

    def run_means(records: Iterable[ObservedRecord]) -> np.ndarray:
        stacked = []
        for record in records:
            columns = []
            for name in CHANNEL_NAMES:
                values = np.asarray(record.values[name], dtype=float)
                mask = np.asarray(record.valid_mask[name])
                masked = np.where(mask, np.abs(values), np.nan)
                with np.errstate(invalid="ignore"):
                    columns.append(np.nanmean(masked, axis=0))
            stacked.append(np.concatenate(columns))
        return np.nanmean(np.stack(stacked), axis=0)

    healthy = np.stack(
        [run_means(windows_by_label["healthy"][cell]) for cell in cells]
    )
    fault = np.stack([run_means(windows_by_label[fault_label][cell]) for cell in cells])
    spread = np.nanstd(healthy, axis=0)
    differences = fault - healthy
    labels = [
        f"{name}[{i}]" for name in CHANNEL_NAMES for i in range(CHANNEL_WIDTH[name])
    ]
    rows: list[dict] = []
    for index, label in enumerate(labels):
        column = differences[:, index]
        finite = column[np.isfinite(column)]
        test = paired_sign_test(finite)
        base = float(np.nanmean(np.abs(healthy[:, index])))
        rows.append(
            {
                "column": label,
                "s_exclusive": label.startswith("gauge_obs"),
                "median_relative_change": (
                    float(np.nanmedian(column) / base) if base > 0 else float("nan")
                ),
                "effect_over_healthy_spread": (
                    float(np.nanmean(np.abs(finite)) / spread[index])
                    if spread[index] > 0
                    else float("nan")
                ),
                "paired_sign_test": test,
            }
        )
    return rows


def build_report(results: dict) -> str:
    """Render the human-readable markdown report for the screen."""

    lines = [
        "# Development structural separability screen",
        "",
        f"- Generated: {results['generated_utc']}",
        f"- Dataset root: `{results['dataset_root']}`",
        f"- Config hash: `{results['config_hash']}`",
        f"- Split screened: `{results['split']}` (the script refuses any other split)",
        f"- Trajectory filter: `{results['trajectory_filter']}`",
        f"- Window W = {results['window_steps']} steps, stride {results['stride']}, "
        f"{results['windows_per_run']} post-onset windows per run",
        f"- Context cells (folds): {results['n_cells']}; runs per contrast arm: "
        f"{results['n_cells']}",
        "",
        "Every contrast is context-matched: the healthy run and the fault run in a",
        "fold share trajectory, payload, environment and contact profile, and differ",
        "only in the fault and the sensor seed. Folds hold out a whole cell.",
        "",
        "## Run-level AUROC (held-out, leave-one-cell-out)",
        "",
        "| contrast | suite | interpretable rung | learned probe (best over C grid) | "
        "learned permutation p |",
        "|---|---|---|---|---|",
    ]
    for contrast in results["contrast_order"]:
        for suite in results["suites"]:
            entry = results["contrasts"][contrast][suite]
            perm = entry["learned"].get("permutation_null")
            p_text = f"{perm['p_value']:.3f}" if perm else "not run"
            lines.append(
                f"| {contrast} | {suite} | {entry['interpretable']['run_auroc']:.3f} | "
                f"{entry['learned']['run_auroc_best_over_grid']:.3f} | {p_text} |"
            )
    lines += [
        "",
        "## Paired per-cell sign tests (exact, two-sided)",
        "",
        "| contrast | suite | rung | cells with fault > healthy | p |",
        "|---|---|---|---|---|",
    ]
    for contrast in results["contrast_order"]:
        for suite in results["suites"]:
            entry = results["contrasts"][contrast][suite]
            for rung in ("interpretable", "learned"):
                test = entry[rung]["paired_sign_test"]
                lines.append(
                    f"| {contrast} | {suite} | {rung} | "
                    f"{test['n_positive']}/{test['n_pairs']} | {test['p_value']:.4f} |"
                )
    lines += ["", "## Interpretable rung score scale", "",
              "| contrast | suite | healthy mean | fault mean | median paired ratio |",
              "|---|---|---|---|---|"]
    for contrast in results["contrast_order"]:
        for suite in results["suites"]:
            interp = results["contrasts"][contrast][suite]["interpretable"]
            lines.append(
                f"| {contrast} | {suite} | {interp['healthy_mean_score']:.4f} | "
                f"{interp['fault_mean_score']:.4f} | {interp['median_paired_ratio']:.3f} |"
            )
    lines += [
        "",
        "## Per-channel paired attribution (suite S, all 18 registry columns)",
        "",
        "Columns whose paired sign test clears the exact 8-cell floor (p = 0.0078)",
        "are listed; `S-excl` marks the four gauge columns S alone carries.",
        "",
        "| contrast | column | S-excl | median rel. change | effect / healthy spread | sign p |",
        "|---|---|---|---|---|---|",
    ]
    for contrast in results["contrast_order"]:
        entry = results["contrasts"][contrast].get("S")
        if entry is None:
            continue
        significant = [
            row
            for row in entry["per_channel"]
            if row["paired_sign_test"]["p_value"] <= 0.05
        ]
        if not significant:
            lines.append(f"| {contrast} | *(no column reaches p <= 0.05)* | | | | |")
        for row in significant:
            lines.append(
                f"| {contrast} | `{row['column']}` | "
                f"{'yes' if row['s_exclusive'] else 'no'} | "
                f"{row['median_relative_change']:.2%} | "
                f"{row['effect_over_healthy_spread']:.3f} | "
                f"{row['paired_sign_test']['p_value']:.4f} |"
            )
    lines += [
        "",
        "Largest S-exclusive gauge effect per contrast, whether or not significant:",
        "",
        "| contrast | best gauge column | effect / healthy spread | sign p |",
        "|---|---|---|---|",
    ]
    for contrast in results["contrast_order"]:
        entry = results["contrasts"][contrast].get("S")
        if entry is None:
            continue
        gauges = [row for row in entry["per_channel"] if row["s_exclusive"]]
        best = max(
            gauges,
            key=lambda row: (
                row["effect_over_healthy_spread"]
                if math.isfinite(row["effect_over_healthy_spread"])
                else -1.0
            ),
        )
        lines.append(
            f"| {contrast} | `{best['column']}` | "
            f"{best['effect_over_healthy_spread']:.3f} | "
            f"{best['paired_sign_test']['p_value']:.4f} |"
        )
    lines += ["", "## Reading this screen", "",
              "The learned AUROC is a maximum over a regularisation grid and is therefore",
              "an optimistic bound on what this probe class can do at this sample size.",
              "The permutation null applies the same maximisation, so the selection is",
              "inside the null and the p-value remains interpretable. A positive control",
              f"({POSITIVE_CONTROL}) is included so an all-null table can be told apart",
              "from a broken pipeline.", ""]
    return "\n".join(lines)


def main(argv: Sequence[str] | None = None) -> int:
    """Run the development-only structural separability screen."""

    packet_root = SCRIPT_DIR.parent
    parser = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    parser.add_argument(
        "--dataset-root",
        type=Path,
        required=True,
        help="root of the delivered Gate-3 base dataset (contains manifest.csv)",
    )
    parser.add_argument(
        "--assignment",
        type=Path,
        default=packet_root / "config" / "proposed-gate3-assignment-v0.1.json",
        help="approved Gate-3 assignment, read for trajectory onset times",
    )
    parser.add_argument(
        "--output-dir",
        type=Path,
        required=True,
        help="directory for the JSON result and markdown report",
    )
    parser.add_argument("--window-steps", type=int, default=768, help="fixed window W")
    parser.add_argument("--stride", type=int, default=64, help="window start stride")
    parser.add_argument(
        "--control-dt-s", type=float, default=0.002, help="control step used for onsets"
    )
    parser.add_argument(
        "--permutations",
        type=int,
        default=256,
        help="paired label sign patterns for the exact null on the critical contrast "
        "(0 disables)",
    )
    parser.add_argument(
        "--max-iter", type=int, default=2000, help="logistic solver iteration cap"
    )
    parser.add_argument(
        "--suites",
        nargs="+",
        default=["C1", "S"],
        help="deployable suites to screen",
    )
    parser.add_argument(
        "--trajectory-filter",
        choices=("all", "diagnostic", "ordinary"),
        default="all",
        help="restrict the screen to one trajectory family; the synchronous "
        "interpretable rung is only meaningful under the diagnostic probe",
    )
    args = parser.parse_args(argv)

    dataset_root = args.dataset_root.resolve()
    output_dir = args.output_dir.resolve()
    output_dir.mkdir(parents=True, exist_ok=True)

    print(f"[screen] dataset root  : {dataset_root}", flush=True)
    print(f"[screen] split allowed : {AUTHORISED_SPLIT} (enforced)", flush=True)
    rows = read_dev_manifest(dataset_root)
    print(f"[screen] dev manifest rows: {len(rows)}", flush=True)
    assignment = json.loads(args.assignment.read_text(encoding="utf-8"))

    extractor = WindowFeatureExtractor(args.window_steps)
    config_hashes = {row["config_hash"] for row in rows}
    if len(config_hashes) != 1:
        raise SeparabilityScreenError(f"dev rows carry {len(config_hashes)} config hashes")

    contrast_order = [
        CRITICAL_CONTRAST,
        "structure_rem_ei_0.50",
        POSITIVE_CONTROL,
    ]
    results: dict = {
        "screen": "development_structural_separability",
        "generated_utc": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
        "dataset_root": str(dataset_root),
        "config_hash": config_hashes.pop(),
        "split": AUTHORISED_SPLIT,
        "trajectory_filter": args.trajectory_filter,
        "window_steps": args.window_steps,
        "stride": args.stride,
        "suites": list(args.suites),
        "contrast_order": contrast_order,
        "contrasts": {label: {} for label in contrast_order},
    }

    for suite in args.suites:
        grouped = collect_runs(rows, suite, args.trajectory_filter)
        cells = sorted(grouped["healthy"])
        results["n_cells"] = len(cells)
        windows_by_label: dict[str, dict[str, list[ObservedRecord]]] = {}
        for label, by_cell in grouped.items():
            per_cell: dict[str, list[ObservedRecord]] = {}
            for cell, row in by_cell.items():
                onset = onset_step(row, assignment, args.control_dt_s)
                per_cell[cell] = load_run_windows(
                    dataset_root, row, suite, onset, args.window_steps, args.stride
                )
            windows_by_label[label] = per_cell
            counts = {len(v) for v in per_cell.values()}
            print(
                f"[screen] {suite} {label:<24} runs={len(per_cell)} "
                f"windows/run={sorted(counts)}",
                flush=True,
            )
        results["windows_per_run"] = sorted(
            {len(v) for v in windows_by_label["healthy"].values()}
        )
        for contrast in contrast_order:
            permutations = args.permutations if contrast == CRITICAL_CONTRAST else 0
            print(f"[screen] {suite} :: {contrast} (permutations={permutations})", flush=True)
            started = time.time()
            results["contrasts"][contrast][suite] = screen_contrast(
                windows_by_label,
                contrast,
                extractor,
                cells,
                permutations,
                args.max_iter,
            )
            entry = results["contrasts"][contrast][suite]
            print(
                f"[screen]   interpretable AUROC {entry['interpretable']['run_auroc']:.3f} | "
                f"learned AUROC {entry['learned']['run_auroc_best_over_grid']:.3f} | "
                f"{time.time() - started:.0f}s",
                flush=True,
            )

    json_path = output_dir / "structural_separability_screen.json"
    report_path = output_dir / "structural_separability_screen_report.md"
    json_path.write_text(json.dumps(results, indent=2, sort_keys=True), encoding="utf-8")
    report_path.write_text(build_report(results), encoding="utf-8")
    print(f"[screen] wrote {json_path}", flush=True)
    print(f"[screen] wrote {report_path}", flush=True)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
