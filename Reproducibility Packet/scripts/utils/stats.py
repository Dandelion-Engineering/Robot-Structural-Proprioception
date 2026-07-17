"""Paired hierarchical-bootstrap confidence intervals for the S-vs-C1 headline.

The confirmatory comparison is *paired* (each `pair_id` yields a matched C1 and S
rollout, schema §A) and *hierarchical* (each pair is evaluated under several
estimator `train_seed`s, Slot 7 requires >= 5). A flat bootstrap over runs would
ignore both structures and understate the interval. This module resamples the two
levels in the right order — pair units first, then the seed replicates within each
resampled pair — and returns a percentile interval and the "excludes zero" decision
the success bars turn on.

`scipy` is intentionally not used: the nested/paired resampling is the project's
own, and a percentile interval needs only `numpy`. The *statistic* (Δmacro-F1 on
pooled predictions, %-reduction in `J_5s`, a per-class recall difference, ...) is
supplied by the caller as a pure function of the resampled subunits, so this
primitive never has to know which headline it is serving. See `utils.metrics` for
the point statistics themselves.

Terminology: a **cluster** is one top-level unit (a `pair_id`); a **subunit** is one
lower-level replicate within it (one `train_seed`'s evaluation of that pair, carrying
whatever the statistic needs — e.g. the matched C1 and S predictions). Pairing is
preserved because a subunit carries *both* suites' data, so resampling never splits a
C1 from its S.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Callable, Sequence, TypeVar

import numpy as np

Subunit = TypeVar("Subunit")
Statistic = Callable[[list], float]


@dataclass(frozen=True)
class BootstrapResult:
    """A percentile bootstrap interval and the headline decision it supports."""

    point: float  # statistic on the full (un-resampled) data
    ci_low: float
    ci_high: float
    ci_level: float  # e.g. 0.95
    n_boot: int
    excludes_zero: bool  # the whole interval is on one side of 0

    def non_inferior(self, margin: float) -> bool:
        """True if the lower CI bound sits above ``-margin`` (one-sided guard).

        Used for the per-source-class recall check: every class's S−C1 recall
        difference must have its lower 95% bound above ``-0.02`` (Slot 7 / §G).
        """

        if margin < 0.0:
            raise ValueError("margin must be non-negative")
        return self.ci_low > -margin

    def superior_by(self, effect: float) -> bool:
        """True if the point estimate meets ``>= effect`` *and* the CI excludes zero.

        The headline bars are two-part: an effect-size floor on the point estimate
        (Δmacro-F1 >= 0.05; `J_5s` reduction >= 10%) *and* a paired interval that
        excludes zero. This bundles both so a caller cannot check one and forget the
        other.
        """

        return self.point >= effect and self.excludes_zero


def hierarchical_bootstrap_ci(
    clusters: Sequence[Sequence[Subunit]],
    statistic_fn: Statistic,
    *,
    n_boot: int,
    rng: np.random.Generator,
    ci_level: float = 0.95,
) -> BootstrapResult:
    """Two-level cluster bootstrap CI for a statistic over paired, seeded data.

    Args:
        clusters: one entry per `pair_id`; each entry is that pair's subunits (its
            `train_seed` replicates). Every cluster must be non-empty.
        statistic_fn: pure function mapping a flat list of resampled subunits to a
            scalar (e.g. pooled Δmacro-F1). Must return a finite value; it is the
            caller's job to make it robust to resampling (e.g. `zero_division=0`).
        n_boot: number of bootstrap replicates (>= 1).
        rng: a seeded ``numpy`` Generator, so intervals are reproducible.
        ci_level: two-sided interval mass (default 0.95 -> the 2.5/97.5 percentiles).

    Returns:
        A `BootstrapResult` with the point statistic, percentile interval, and whether
        the interval excludes zero.
    """

    if n_boot < 1:
        raise ValueError("n_boot must be >= 1")
    if not 0.0 < ci_level < 1.0:
        raise ValueError("ci_level must be in (0, 1)")
    materialized: list[list[Subunit]] = [list(cluster) for cluster in clusters]
    if not materialized:
        raise ValueError("at least one cluster (pair unit) is required")
    if any(len(cluster) == 0 for cluster in materialized):
        raise ValueError("every cluster must contain at least one subunit")

    point = float(statistic_fn([sub for cluster in materialized for sub in cluster]))
    if not np.isfinite(point):
        raise ValueError("statistic_fn returned a non-finite value on the full data")

    n_clusters = len(materialized)
    replicates = np.empty(n_boot, dtype=float)
    for b in range(n_boot):
        chosen = rng.integers(0, n_clusters, size=n_clusters)
        resample: list[Subunit] = []
        for cluster_index in chosen:
            cluster = materialized[cluster_index]
            size = len(cluster)
            picks = rng.integers(0, size, size=size)
            resample.extend(cluster[j] for j in picks)
        value = float(statistic_fn(resample))
        if not np.isfinite(value):
            raise ValueError(
                f"statistic_fn returned a non-finite value on bootstrap replicate {b}"
            )
        replicates[b] = value

    alpha = 1.0 - ci_level
    ci_low, ci_high = np.percentile(replicates, [100.0 * alpha / 2.0, 100.0 * (1.0 - alpha / 2.0)])
    excludes_zero = bool(ci_low > 0.0 or ci_high < 0.0)
    return BootstrapResult(
        point=point,
        ci_low=float(ci_low),
        ci_high=float(ci_high),
        ci_level=ci_level,
        n_boot=n_boot,
        excludes_zero=excludes_zero,
    )


def mean_difference_statistic(key_s: str, key_c1: str) -> Statistic:
    """Build a statistic computing the mean paired difference ``mean(sub[s] − sub[c1])``.

    A convenience for headlines that *are* a mean of per-subunit paired values (e.g. a
    per-pair `J_5s` difference). Statistics that must pool raw predictions before
    scoring (macro-F1) are not of this form and should be written directly.
    """

    def statistic(subunits: list) -> float:
        if not subunits:
            raise ValueError("cannot take a mean difference over an empty resample")
        return float(np.mean([sub[key_s] - sub[key_c1] for sub in subunits]))

    return statistic
