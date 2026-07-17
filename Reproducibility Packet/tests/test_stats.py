"""Tests for the paired hierarchical-bootstrap confidence interval (utils.stats).

The interval is what turns a point Δmacro-F1 or `J_5s` reduction into a headline
decision, so these pin the properties the bars depend on: reproducibility under a
seed, the interval bracketing the point estimate, and the "excludes zero" flag
firing on a clear effect but not on a null one. A final test drives the real usage —
a pooled Δmacro-F1 statistic over paired, seeded clusters.
"""

from __future__ import annotations

import sys
from pathlib import Path

import numpy as np
import pytest

SCRIPTS_DIR = Path(__file__).resolve().parents[1] / "scripts"
sys.path.insert(0, str(SCRIPTS_DIR))

from utils.metrics import macro_f1  # noqa: E402
from utils.stats import (  # noqa: E402
    BootstrapResult,
    hierarchical_bootstrap_ci,
    mean_difference_statistic,
)


def _paired_clusters(diffs: list[float], seeds_per_pair: int = 5) -> list[list[dict]]:
    """Build clusters of {'s','c1'} subunits whose S−C1 difference is a given value."""

    clusters = []
    for d in diffs:
        clusters.append([{"c1": 0.0, "s": float(d)} for _ in range(seeds_per_pair)])
    return clusters


def test_bootstrap_is_reproducible_under_seed() -> None:
    """Identical data + identical Generator seed -> identical interval."""

    clusters = _paired_clusters([0.1, 0.2, 0.15, 0.05, 0.12])
    stat = mean_difference_statistic("s", "c1")
    a = hierarchical_bootstrap_ci(clusters, stat, n_boot=500, rng=np.random.default_rng(0))
    b = hierarchical_bootstrap_ci(clusters, stat, n_boot=500, rng=np.random.default_rng(0))
    assert a == b


def test_ci_brackets_point_estimate() -> None:
    """The point statistic lies within its own bootstrap interval."""

    clusters = _paired_clusters([0.1, 0.2, 0.15, 0.05, 0.12, 0.08])
    stat = mean_difference_statistic("s", "c1")
    result = hierarchical_bootstrap_ci(clusters, stat, n_boot=1000, rng=np.random.default_rng(1))
    assert result.ci_low <= result.point <= result.ci_high
    assert result.point == pytest.approx(np.mean([0.1, 0.2, 0.15, 0.05, 0.12, 0.08]))


def test_excludes_zero_for_a_clear_positive_effect() -> None:
    """Every pair improves, so the whole interval sits above zero."""

    clusters = _paired_clusters([0.10, 0.12, 0.11, 0.09, 0.13, 0.10, 0.11])
    stat = mean_difference_statistic("s", "c1")
    result = hierarchical_bootstrap_ci(clusters, stat, n_boot=2000, rng=np.random.default_rng(2))
    assert result.excludes_zero
    assert result.ci_low > 0.0


def test_includes_zero_for_a_null_effect() -> None:
    """Symmetric ±differences average to zero, so the interval must include zero."""

    clusters = _paired_clusters([0.2, -0.2, 0.2, -0.2, 0.2, -0.2, 0.2, -0.2])
    stat = mean_difference_statistic("s", "c1")
    result = hierarchical_bootstrap_ci(clusters, stat, n_boot=2000, rng=np.random.default_rng(3))
    assert not result.excludes_zero
    assert result.ci_low < 0.0 < result.ci_high


def test_non_inferior_and_superior_by_decisions() -> None:
    """The BootstrapResult decision helpers implement the two-part bars."""

    strong = BootstrapResult(0.07, 0.03, 0.11, 0.95, 2000, True)
    assert strong.superior_by(0.05)  # point >= 0.05 and CI excludes zero
    assert strong.non_inferior(0.02)  # lower bound -0.02 < 0.03
    weak = BootstrapResult(0.06, -0.01, 0.13, 0.95, 2000, False)
    assert not weak.superior_by(0.05)  # point ok but CI touches zero
    marginal = BootstrapResult(0.0, -0.015, 0.02, 0.95, 2000, False)
    assert marginal.non_inferior(0.02)  # -0.015 > -0.02
    assert not marginal.non_inferior(0.01)  # -0.015 !> -0.01


def test_empty_and_degenerate_inputs_fail_loud() -> None:
    """No clusters, an empty cluster, or a non-finite statistic all raise."""

    stat = mean_difference_statistic("s", "c1")
    with pytest.raises(ValueError):
        hierarchical_bootstrap_ci([], stat, n_boot=10, rng=np.random.default_rng(0))
    with pytest.raises(ValueError):
        hierarchical_bootstrap_ci([[]], stat, n_boot=10, rng=np.random.default_rng(0))
    with pytest.raises(ValueError, match="rectangular"):
        hierarchical_bootstrap_ci(
            [
                [{"c1": 0.0, "s": 0.1}],
                [{"c1": 0.0, "s": 0.1}, {"c1": 0.0, "s": 0.2}],
            ],
            stat,
            n_boot=10,
            rng=np.random.default_rng(0),
        )
    with pytest.raises(ValueError):
        hierarchical_bootstrap_ci(
            _paired_clusters([0.1]), lambda subs: float("nan"),
            n_boot=10, rng=np.random.default_rng(0),
        )


def test_global_train_seed_axis_is_resampled_consistently_across_pairs() -> None:
    """One sampled seed column must stay aligned across every sampled pair row."""

    n_pairs = 4
    n_seeds = 3
    grid = [
        [{"pair": pair, "seed": seed} for seed in range(n_seeds)]
        for pair in range(n_pairs)
    ]

    def aligned_seed_statistic(subunits: list) -> float:
        sampled = np.array([sub["seed"] for sub in subunits]).reshape(n_pairs, n_seeds)
        if not np.all(sampled == sampled[0]):
            return float("nan")
        return float(np.mean(sampled))

    result = hierarchical_bootstrap_ci(
        grid, aligned_seed_statistic, n_boot=100, rng=np.random.default_rng(11)
    )
    assert np.isfinite(result.ci_low)
    assert np.isfinite(result.ci_high)


def test_end_to_end_delta_macro_f1_over_paired_clusters() -> None:
    """Drive the real headline: pooled Δmacro-F1 over paired, seeded clusters.

    Each subunit carries a pair's held-out truth and both suites' predictions. S is
    constructed to fix one error C1 makes on every pair, so pooled macro-F1(S) >
    macro-F1(C1), and with a consistent gain the paired interval must exclude zero.
    """

    rng = np.random.default_rng(7)
    y_true = np.array([0, 1, 2, 3])

    def make_subunit() -> dict:
        # C1 misclassifies the 'sensor' sample; S gets it right. Everything else matches.
        return {"y": y_true, "c1": np.array([0, 1, 2, 0]), "s": np.array([0, 1, 2, 3])}

    clusters = [[make_subunit() for _ in range(5)] for _ in range(8)]  # 8 pairs x 5 seeds

    def delta_macro_f1(subunits: list) -> float:
        y = np.concatenate([sub["y"] for sub in subunits])
        c1 = np.concatenate([sub["c1"] for sub in subunits])
        s = np.concatenate([sub["s"] for sub in subunits])
        return macro_f1(y, s) - macro_f1(y, c1)

    result = hierarchical_bootstrap_ci(clusters, delta_macro_f1, n_boot=1000, rng=rng)
    # macro_f1(S)=1.0; macro_f1(C1): classes 0 has an extra FP (the sensor sample
    # predicted 0), class 3 has no TP. Point delta is strictly positive and constant
    # across every resample, so the interval is a positive point mass excluding zero.
    assert result.point > 0.0
    assert result.excludes_zero
    assert result.ci_low > 0.0
