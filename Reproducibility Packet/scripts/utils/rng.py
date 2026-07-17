"""Common-random-number (CRN) substreams for the matched C1-vs-S comparison.

Schema section A [C4]: within a `pair_id`, the exogenous sensor seed is shared
between the C1 and S rollouts, and the shared channels (encoder, current proxy,
IMU) must be drawn from *matched deterministic substreams* so that S differs from
C1 only by the added gauge channels (plus later causal divergence). Substreams
are keyed by `(sensor_seed, pair_id, channel, stream)`.

The implementation gives every (channel, stream) its OWN independent
`numpy.random.Generator`, derived from an independent `SeedSequence`. Because the
generators do not share state, drawing S-only gauge noise can never advance or
perturb a shared-channel generator (the property the paired hierarchical
bootstrap in schema G / Slot 7 relies on). Keying by `sensor_seed` + `pair_id`
means two rollouts in the same pair reproduce identical shared-channel draws.
"""

from __future__ import annotations

import hashlib

import numpy as np

from utils.schema_types import CHANNEL_NAMES

# Stable integer code per registry channel (order-independent identity).
_CHANNEL_CODES: dict[str, int] = {name: index for index, name in enumerate(CHANNEL_NAMES)}

# Distinct sub-stream codes so noise / bias / drift / dropout within one channel
# are mutually independent rather than correlated slices of one stream.
_STREAM_CODES: dict[str, int] = {
    "value": 0,
    "bias": 1,
    "drift": 2,
    "dropout": 3,
    "fault": 4,
}


def pair_id_to_int(pair_id: int | str) -> int:
    """Map an opaque `pair_id` to a stable non-negative integer for seeding.

    Integers pass through; strings are hashed deterministically (SHA-256, first
    8 bytes) so a run reproduces the same substreams across machines and sessions.
    """

    if isinstance(pair_id, (int, np.integer)):
        return int(pair_id)
    digest = hashlib.sha256(str(pair_id).encode("utf-8")).digest()
    return int.from_bytes(digest[:8], "big")


def channel_generator(
    sensor_seed: int,
    pair_id: int | str,
    channel: str,
    stream: str = "value",
) -> np.random.Generator:
    """Return the independent CRN generator for `(sensor_seed, pair_id, channel, stream)`.

    Args:
        sensor_seed: the rollout's sensor seed (shared within a pair, schema A).
        pair_id: the matched-comparison identifier (shared within a pair).
        channel: a registry channel name (must be in the observed registry).
        stream: which per-channel sub-stream (`value`, `bias`, `drift`, `dropout`,
            `fault`) — distinct streams are statistically independent.

    Returns:
        A freshly seeded ``numpy.random.Generator`` whose sequence depends only on
        the four keys, never on call order relative to other channels.
    """

    if channel not in _CHANNEL_CODES:
        raise KeyError(f"unknown channel for CRN keying: {channel!r}")
    if stream not in _STREAM_CODES:
        raise KeyError(f"unknown sub-stream: {stream!r}")
    seed_sequence = np.random.SeedSequence(
        [int(sensor_seed), pair_id_to_int(pair_id), _CHANNEL_CODES[channel], _STREAM_CODES[stream]]
    )
    return np.random.default_rng(seed_sequence)
