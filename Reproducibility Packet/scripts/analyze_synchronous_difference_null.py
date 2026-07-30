"""Protocol P Stage 0 - the sensor-only difference null (0 rollouts).

Specification: ``protocol/protocol-p-v2.3.3.md`` section 8, "Stage 0 - sensor-only
difference null".  Read the specification before changing anything here; this script is
the executable form of a pre-registered stage and its constants are pins, not defaults
someone may tune.

What this measures
------------------
Protocol P's operative statistic is a *difference* of two four-gauge harmonic-coefficient
vectors::

    D = || concat_{g=0..3} ( b_g(A) - b_g(B) ) ||_2          8 entries

Stage 0 evaluates that statistic where the only thing separating A from B is the sensor
identity: the same zero mechanical strain, the same imposed thermal profile, two
different ``sensor_seed`` values.  It is therefore the part of ``D`` that the observed
sensor path contributes on its own, with no plant in the loop at all.

**One sample is one PAIR of four-gauge windows reduced to one scalar. 100 samples - not
200, and emphatically not 800.**  The 800-sample figure in
``analyze_synchronous_detection_floor.py`` arises because that script appends per gauge
per realization; that is a per-gauge single-window number and a different object.  This
script never aggregates per gauge: the four gauges enter one 8-entry vector, and the
vector reduces to one scalar per pair.

What this does NOT do
---------------------
Stage 0 has no plant, so it holds no reservation, has no window origin, and produces no
mechanics claim.  It sets no threshold and it gates nothing.  The protocol's operative
null is Stage C's ``Q95_c``; the value measured here is a **conditional healthy-null
diagnostic** whose only corroboration is that it sits inside the real-plant fixed-trace
range recorded in section 8.  A reader who treats this file's number as a detection
threshold has misread both this script and the protocol.

Invariant scope (Protocol P section 10)
---------------------------------------
Applies here:

  * **I1**  - the two *text*-domain pins (this protocol file and the approved assignment)
    are verified through ``canonical_text_sha256`` before any measurement.  The binary
    ``.npz`` pins belong to section 7's replay gate and are out of scope: Stage 0 reads
    no retained payload.
  * **I8**  - the written artifact carries one artifact-level identity of the form
    ``dev-<64 lowercase hex>`` that differs from the base config hash, plus the exact
    ``canonical_json`` string it was derived from.
  * **I11** - the harmonic fit requires at least 5 finite valid samples; ``gauge_obs``
    carries real dropout and latency NaNs, so every statistic here is NaN-aware.

Out of scope, and why: **I2** (no replay), **I3-I7** (no reservation and no rollout
identity), **I9/I10** (no plant, therefore no window origin and no measurement-time
array - section 8 exempts Stage 0 explicitly), **I12** (no plant to gate),
**I13a/I13b** (no physical fault is constructed).

Usage (from the Reproducibility Packet directory)
-------------------------------------------------
Single line.  A backtick is the only permitted continuation; ``^`` is a cmd.exe token,
not a PowerShell one::

    ..\\venv\\Scripts\\python.exe scripts\\analyze_synchronous_difference_null.py --window 768 --f-ctrl-hz 500.0 --diagnostic-hz 0.8 --thermal-ramp-c 3.0 --pairs 100 --seed 0 --pair-id 1

Those seven values are the pre-registered invocation and are also this script's
defaults, so the bare command reproduces the pinned run.  Any failure raises
``ProtocolPError``; the protocol never uses ``assert``, because ``python -O`` removes
assertions.

Coupling note (deliberate, flagged for review)
----------------------------------------------
``ProtocolPError``, ``canonical_text_sha256`` and the two text-domain digest pins are
imported from ``protocol_p_replay_gate`` rather than re-declared.  That keeps exactly one
implementation of the two-domain hashing rule and exactly one copy of each pinned digest
across the protocol's scripts - the same reasoning that made the gate import the
producer's ``_plant_payload`` instead of maintaining a second serializer.  If a third
consumer appears (the Stage-A/B/C driver will need all of it), the right move is to
extract them into ``utils/protocol_p.py``; that was not done now because it would edit
the gate at the exact state both agents just approved.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import sys
from collections.abc import Sequence
from pathlib import Path
from typing import Any

import numpy as np

SCRIPT_DIR = Path(__file__).resolve().parent
if str(SCRIPT_DIR) not in sys.path:
    sys.path.insert(0, str(SCRIPT_DIR))

from protocol_p_replay_gate import (  # noqa: E402
    ASSIGNMENT_CANONICAL_SHA256,
    ASSIGNMENT_FILENAME,
    PROTOCOL_CANONICAL_SHA256,
    PROTOCOL_FILENAME,
    ProtocolPError,
    canonical_text_sha256,
)
from utils.assignment_binding import validate_approved_assignment_binding  # noqa: E402
from utils.config_contract import load_config  # noqa: E402
from utils.gate3_assignment import load_assignment  # noqa: E402
from utils.gauge_windows import gauge_window, linear_thermal_profile  # noqa: E402
from utils.schema_types import N_GAUGES  # noqa: E402
from utils.sensor_model import SensorConfig  # noqa: E402
from utils.synchronous import harmonic_coefficients  # noqa: E402

PACKET_ROOT = SCRIPT_DIR.parent

# ---------------------------------------------------------------------------
# Pins.  Every value below is pre-registered in Protocol P section 8 or section 6.
# ---------------------------------------------------------------------------

STAGE = "0"
OUTPUT_FILENAME = "sensor_only_difference_null.json"

# Section 8's statistic: four gauges, each contributing a (cos, sin) pair.
N_STATISTIC_ENTRIES = 2 * N_GAUGES

# The real-plant corroboration recorded in section 8: one delivered healthy trace per
# cell held exactly fixed and redrawn at 8 sensor identities, giving these per-cell 0.95
# quantiles across cells 6/4/7/5.  This is a *conditional healthy-null diagnostic*: it
# sets no threshold and gates nothing.  It is recorded so the containment check in the
# artifact is a like-for-like comparison of one 0.95 quantile against four others.
REAL_PLANT_FIXED_TRACE_Q95_BY_CELL = {"6": 0.3176, "4": 0.3555, "7": 0.3854, "5": 0.4251}

# The top-level key set of the written artifact.  Section 8 / Correction 6 require the
# identity payload to carry "sorted top-level keys the script writes", which is
# self-referential unless the writer and the payload share ONE object.  They do: this
# tuple goes into the identity payload and the document is checked against it before it
# is written, so the recorded schema cannot drift from the file it describes.
OUTPUT_TOP_LEVEL_KEYS = (
    "boundaries",
    "corroboration",
    "inputs",
    "null_distribution",
    "protocol",
    "purpose",
    "samples",
    "stage_0_canonical",
    "stage_0_identity",
    "statistic",
)


def _require(condition: bool, message: str) -> None:
    """Raise ``ProtocolPError(message)`` unless ``condition`` holds.

    Inputs: an already-evaluated boolean and the message to fail with. Outputs: none.
    Purpose: a fail-loud replacement for ``assert``, which ``python -O`` would remove.
    """

    if not condition:
        raise ProtocolPError(message)


def canonical_json(payload: Any) -> str:
    """CANONICAL_JSON - the single serialization rule for every Protocol-P identity.

    Inputs: a JSON-serializable payload. Outputs: its canonical string form.
    Purpose: pinned verbatim by Protocol P Correction 2, matching the packet precedent
    in ``config_contract.canonical_json_bytes``. ``allow_nan=False`` is not decoration:
    plain ``json.dumps`` emits the non-standard tokens ``NaN`` / ``Infinity`` rather
    than raising, so a corrupted float reaching an identity payload would produce a
    valid-looking digest over an unparseable document.
    """

    return json.dumps(
        payload,
        sort_keys=True,
        separators=(",", ":"),
        ensure_ascii=False,
        allow_nan=False,
    )


def pair_seeds(seed: int, pair_index: int) -> tuple[int, int]:
    """Return the two ``sensor_seed`` values of one pair.

    Inputs: the base seed and a zero-based pair index. Outputs: ``(seed_a, seed_b)``.
    Purpose: section 6 pins Stage 0's consumed range as ``sensor_seed = 0..199`` for 100
    pairs at ``--seed 0``. Consecutive pairing is the mapping that produces exactly that
    range with no seed used twice, so it is pinned here explicitly rather than left to
    the reader to infer.
    """

    if pair_index < 0:
        raise ValueError("pair_index must be non-negative")
    return seed + 2 * pair_index, seed + 2 * pair_index + 1


def coefficient_vector(
    values: np.ndarray, valid: np.ndarray, t_s: np.ndarray, f_d: float
) -> np.ndarray:
    """Stack the four gauges' ``(cos, sin)`` harmonic coefficients into one vector.

    Inputs: emitted gauge values and validity, each ``[W, N_GAUGES]``; the window's time
    grid ``[W]``; the diagnostic frequency in Hz. Outputs: an ``[8]`` vector ordered
    gauge-major, matching section 8's ``concat_{g=0..3}``.

    Purpose: the per-gauge fit is the protocol's building block. ``harmonic_coefficients``
    fits an intercept and a centred linear trend jointly with the cosine and sine terms,
    so a linear-in-time thermal ramp contributes exactly zero in exact arithmetic;
    quantization is what breaks that. It requires at least 5 finite valid samples (I11)
    and fails loudly otherwise, which is why no NaN filtering happens here.
    """

    values = np.asarray(values, dtype=float)
    valid = np.asarray(valid, dtype=bool)
    t_s = np.asarray(t_s, dtype=float)
    if values.ndim != 2 or values.shape[1] != N_GAUGES:
        raise ProtocolPError(f"values must be [W, {N_GAUGES}]; got {values.shape}")
    if valid.shape != values.shape:
        raise ProtocolPError(
            f"valid must match values exactly; got {valid.shape} vs {values.shape}"
        )
    if t_s.shape != (values.shape[0],):
        raise ProtocolPError(
            f"time grid must be [W] with W={values.shape[0]}; got {t_s.shape}"
        )

    parts = [
        np.asarray(harmonic_coefficients(values[:, g], valid[:, g], t_s, f_d), dtype=float)
        for g in range(N_GAUGES)
    ]
    vector = np.concatenate(parts)
    _require(
        vector.shape == (N_STATISTIC_ENTRIES,),
        f"the statistic must have exactly {N_STATISTIC_ENTRIES} entries; "
        f"got {vector.shape}",
    )
    return vector


def difference_statistic(vector_a: np.ndarray, vector_b: np.ndarray) -> float:
    """Section 8's ``D``: the L2 norm of the difference of two coefficient vectors.

    Inputs: two ``[8]`` coefficient vectors. Outputs: one non-negative scalar.
    Purpose: reduce one pair of four-gauge windows to the single number the protocol's
    ladder and null are both expressed in. Raises if either vector is the wrong length
    or carries a non-finite entry, because a NaN reaching the statistic would propagate
    into the null silently.
    """

    vector_a = np.asarray(vector_a, dtype=float)
    vector_b = np.asarray(vector_b, dtype=float)
    for name, vector in (("a", vector_a), ("b", vector_b)):
        _require(
            vector.shape == (N_STATISTIC_ENTRIES,),
            f"vector {name} must have {N_STATISTIC_ENTRIES} entries; got {vector.shape}",
        )
        _require(
            bool(np.all(np.isfinite(vector))),
            f"vector {name} carries a non-finite coefficient; the harmonic fit must "
            "fail loudly rather than propagate one into the null",
        )
    return float(np.linalg.norm(vector_a - vector_b))


def verify_text_pins(protocol_path: Path, assignment_path: Path) -> dict[str, str]:
    """Invariant I1, text domain: both tracked text pins present and unchanged.

    Inputs: paths to the protocol specification and the approved assignment. Outputs: the
    two canonical digests. Purpose: Stage 0 records these digests inside its identity, so
    a drifted input would otherwise be silently absorbed into a valid-looking identity
    instead of stopping the stage. Raises ``ProtocolPError`` on a wrong filename, an
    absent file, or a changed digest - never a fallback to whatever is on disk.
    """

    _require(
        protocol_path.name == PROTOCOL_FILENAME,
        f"this script was approved for {PROTOCOL_FILENAME}, not {protocol_path.name}; "
        "a version bump must update the pinned digest in the same commit",
    )
    _require(
        assignment_path.name == ASSIGNMENT_FILENAME,
        f"expected the approved assignment {ASSIGNMENT_FILENAME}, "
        f"not {assignment_path.name}",
    )
    for label, path in (("protocol", protocol_path), ("assignment", assignment_path)):
        _require(path.is_file(), f"I1 [{label}]: {path} is absent")

    protocol_digest = canonical_text_sha256(protocol_path)
    assignment_digest = canonical_text_sha256(assignment_path)
    _require(
        protocol_digest == PROTOCOL_CANONICAL_SHA256,
        f"I1 [protocol]: canonical digest changed\n"
        f"    pinned   {PROTOCOL_CANONICAL_SHA256}\n"
        f"    measured {protocol_digest}",
    )
    _require(
        assignment_digest == ASSIGNMENT_CANONICAL_SHA256,
        f"I1 [assignment]: canonical digest changed\n"
        f"    pinned   {ASSIGNMENT_CANONICAL_SHA256}\n"
        f"    measured {assignment_digest}",
    )
    return {"protocol": protocol_digest, "assignment": assignment_digest}


def require_valid_stage_0_identity(identity: str, base_config_hash: str) -> None:
    """Invariant I8 for Stage 0's artifact-level identity.

    Inputs: the computed identity and the base config hash it was partly derived from.
    Outputs: none. Purpose: I8 requires every generated identity to be
    ``dev-<64 lowercase hex>`` and to differ from the base config hash.

    Reachability, stated honestly. None of these three conditions can fail from
    :func:`stage_0_identity`'s own construction: ``hashlib.sha256().hexdigest()`` always
    returns 64 lowercase hex characters, the ``dev-`` prefix is a literal, and a
    collision with ``base_config_hash`` would require a SHA-256 fixed point over a
    document that contains that very hash. So this guard defends against a **code**
    defect — a future refactor returning the wrong variable, prefixing differently, or
    hashing a different object — not against a data defect. It is a separate function
    precisely so the guard can be fed the states it rejects; asserting it inline would
    have produced a check no test could turn red.
    """

    _require(
        identity.startswith("dev-"),
        f"I8: identity must begin with 'dev-'; got {identity!r}",
    )
    body = identity[4:]
    _require(
        len(body) == 64,
        f"I8: identity body must be 64 characters; got {len(body)}",
    )
    _require(
        all(character in "0123456789abcdef" for character in body),
        f"I8: identity body must be 64 lowercase hex characters; got {body!r}",
    )
    _require(
        identity != base_config_hash,
        "I8: the Stage-0 identity must differ from the base config hash",
    )


def stage_0_identity(
    *,
    base_config_hash: str,
    assignment_canonical_sha256: str,
    assignment_hash: str,
    protocol_spec_sha256: str,
    cli: dict[str, Any],
) -> tuple[str, str]:
    """Protocol P Correction 6: Stage 0's artifact-level identity.

    Inputs: the base config hash, the assignment's canonical digest and document-derived
    hash, this protocol file's canonical digest, and the pre-registered CLI values.
    Outputs: ``(identity, canonical_string)`` - the digest and the exact string it was
    hashed from, in that order.

    Purpose: Stage 0 runs no rollout and holds no reservation, so it has no per-rollout
    provenance hash; one digest identifies the whole artifact. Both values are returned
    together and written together so the artifact records the *same* object that was
    hashed rather than a second call that ought to agree (Correction 8). The ``dev-``
    prefix keeps it permanently ineligible for confirmatory analysis (I8).
    """

    stage_0_identity_payload = {
        "stage": STAGE,
        "base_config_hash": base_config_hash,
        "assignment_canonical_sha256": assignment_canonical_sha256,
        "assignment_hash": assignment_hash,
        "protocol_spec_sha256": protocol_spec_sha256,
        "cli": cli,
        "output_schema": sorted(OUTPUT_TOP_LEVEL_KEYS),
    }
    stage_0_canonical = canonical_json(stage_0_identity_payload)
    identity = "dev-" + hashlib.sha256(stage_0_canonical.encode("utf-8")).hexdigest()
    require_valid_stage_0_identity(identity, base_config_hash)
    return identity, stage_0_canonical


def require_unique_seeds(consumed: Sequence[int]) -> None:
    """Every Stage-0 sensor identity must be consumed exactly once.

    Inputs: the sensor seeds the measurement consumed, in order. Outputs: none.
    Purpose: section 6 pins Stage 0's consumed range as 200 distinct seeds for 100 pairs.
    Two samples drawn at one identity would not be independent, and the null would be
    narrower than it should be while looking perfectly ordinary.

    Reachable, unlike I8: a future change to :func:`pair_seeds` that overlapped
    consecutive pairs would trip this. It is a separate function so that state can be fed
    to it in a test instead of being unconstructable through the real mapping.
    """

    duplicates = sorted({seed for seed in consumed if list(consumed).count(seed) > 1})
    _require(
        not duplicates,
        "every Stage-0 sensor_seed must be consumed exactly once; these repeat: "
        f"{duplicates}",
    )


def summarize_null(distances: Sequence[float]) -> dict[str, Any]:
    """Summarize the null distribution of the difference statistic.

    Inputs: the per-pair ``D`` values. Outputs: the distribution block written into the
    artifact. Purpose: one implementation of the summary, so a caller and a reader cannot
    each compute it slightly differently. ``method="higher"`` makes the 0.95 quantile an
    order statistic of the sample rather than an interpolation between two samples, which
    is what section 8's ``Q95`` means and what the real-plant corroboration values are.
    Raises ``ProtocolPError`` on an empty or non-finite sample.
    """

    array = np.asarray(list(distances), dtype=float)
    _require(array.size >= 2, "a null distribution needs at least 2 samples")
    _require(
        bool(np.all(np.isfinite(array))),
        "the null carries a non-finite sample; refusing to summarize it",
    )
    return {
        "mean": float(array.mean()),
        "std": float(array.std()),
        "min": float(array.min()),
        "median": float(np.median(array)),
        "max": float(array.max()),
        "q95_method_higher": float(np.quantile(array, 0.95, method="higher")),
        "quantile_method": "higher",
    }


def run_null(
    *,
    window: int,
    f_ctrl_hz: float,
    diagnostic_hz: float,
    thermal_ramp_c: float,
    pairs: int,
    seed: int,
    pair_id: int,
) -> dict[str, Any]:
    """Measure the sensor-only difference null over ``pairs`` independent seed pairs.

    Inputs: the seven pre-registered CLI values. Outputs: the per-pair statistics and the
    distribution summary. Purpose: this is Stage 0's measurement. Each pair imposes the
    same zero mechanical strain and the same thermal profile on two different sensor
    identities, so the resulting ``D`` is the sensor path's own contribution to the
    protocol's statistic. Prints progress to stdout so a long run is observable.
    """

    _require(window >= 8, "window must be at least 8 samples")
    _require(pairs >= 2, "a null needs at least 2 pairs")
    _require(
        np.isfinite(f_ctrl_hz) and f_ctrl_hz > 0.0, "f_ctrl_hz must be finite and positive"
    )
    _require(
        np.isfinite(diagnostic_hz) and diagnostic_hz > 0.0,
        "diagnostic_hz must be finite and positive",
    )
    _require(np.isfinite(thermal_ramp_c), "thermal_ramp_c must be finite")

    t_s = np.arange(window) / f_ctrl_hz
    config = SensorConfig()
    temperature = linear_thermal_profile(window, thermal_ramp_c)
    zero_signal = np.zeros((window, N_GAUGES))

    distances: list[float] = []
    consumed: list[int] = []
    for index in range(pairs):
        seed_a, seed_b = pair_seeds(seed, index)
        vectors = []
        for member_seed in (seed_a, seed_b):
            values, valid = gauge_window(
                signal_true=zero_signal,
                temperature_true=temperature,
                f_ctrl=f_ctrl_hz,
                sensor_seed=member_seed,
                pair_id=pair_id,
                config=config,
            )
            vectors.append(coefficient_vector(values, valid, t_s, diagnostic_hz))
        distances.append(difference_statistic(vectors[0], vectors[1]))
        consumed.extend((seed_a, seed_b))
        if (index + 1) % 10 == 0 or index + 1 == pairs:
            print(f"  pair {index + 1:4d}/{pairs}   D = {distances[-1]:.6f}")

    require_unique_seeds(consumed)

    return {
        "samples": {
            "n_pairs": int(pairs),
            "seed_map": "pair p consumes sensor_seed (seed + 2p, seed + 2p + 1)",
            "sensor_seeds_consumed": [int(consumed[0]), int(consumed[-1])],
            "sensor_seeds_consumed_note": "inclusive first and last of a contiguous range",
            "pair_id": int(pair_id),
            "distances": [float(value) for value in distances],
        },
        "null_distribution": summarize_null(distances),
    }


def build_document(
    *,
    measurement: dict[str, Any],
    identity: str,
    canonical: str,
    digests: dict[str, str],
    base_config_hash: str,
    assignment_hash: str,
    cli: dict[str, Any],
) -> dict[str, Any]:
    """Assemble the artifact and check it against the pinned top-level key set.

    Inputs: the measurement, the identity pair, the verified digests, the two input
    hashes, and the CLI values. Outputs: the document to write. Purpose: keep the
    recorded ``output_schema`` and the written file bound to one object; raises
    ``ProtocolPError`` if the document's top-level keys drift from
    ``OUTPUT_TOP_LEVEL_KEYS``, which is what the identity committed to.
    """

    q95 = measurement["null_distribution"]["q95_method_higher"]
    real_plant = REAL_PLANT_FIXED_TRACE_Q95_BY_CELL
    low, high = min(real_plant.values()), max(real_plant.values())

    document = {
        "purpose": (
            "Protocol P Stage 0: the sensor-only component of the difference statistic D, "
            "measured with no plant in the loop. Development artifact, not confirmatory."
        ),
        "protocol": {
            "specification": PROTOCOL_FILENAME,
            "protocol_spec_sha256": digests["protocol"],
            "stage": STAGE,
            "rollouts": 0,
        },
        "stage_0_identity": identity,
        "stage_0_canonical": canonical,
        "inputs": {
            "base_config_hash": base_config_hash,
            "assignment_hash": assignment_hash,
            "assignment_canonical_sha256": digests["assignment"],
            "cli": cli,
        },
        "statistic": {
            "definition": "D = || concat_{g=0..3} ( b_g(A) - b_g(B) ) ||_2",
            "entries": N_STATISTIC_ENTRIES,
            "sample_unit": (
                "one PAIR of four-gauge windows reduced to one scalar; not one gauge and "
                "not one window"
            ),
            "fit": (
                "harmonic_coefficients with intercept and centred linear trend, NaN-aware, "
                "at least 5 finite valid samples required (I11)"
            ),
            "path": "observed sensor path only; no plant, no window origin",
            "units": "microstrain",
        },
        "corroboration": {
            "real_plant_fixed_trace_q95_by_cell": real_plant,
            "real_plant_q95_range": [low, high],
            "stage_0_q95_method_higher": q95,
            "q95_inside_real_plant_range": bool(low <= q95 <= high),
            "comparison": (
                "like-for-like: one 0.95 quantile against four 0.95 quantiles, both "
                "method='higher'"
            ),
            "authority": (
                "NONE. A conditional healthy-null diagnostic. It sets no threshold and "
                "gates nothing; the operative null is Stage C's Q95_c. Containment is a "
                "range statement, never a test."
            ),
        },
        "boundaries": [
            "Purely synthetic sensor path: no plant, no mechanics, no fault, no rollout.",
            "Sets no threshold and gates no decision anywhere in Protocol P.",
            "The identity is dev- prefixed and therefore permanently ineligible for "
            "confirmatory analysis (I8).",
            "Conditional on this pair_id: the sensor RNG is keyed on (sensor_seed, "
            "pair_id, channel, stream) jointly, so these values do not transfer to "
            "another pair_id.",
            "Conditional on this window length, this thermal profile, and the difference "
            "operation. A single-window threshold is a different object and the two are "
            "not interchangeable.",
        ],
    }
    document.update(
        {
            "samples": measurement["samples"],
            "null_distribution": measurement["null_distribution"],
        }
    )

    _require(
        sorted(document) == sorted(OUTPUT_TOP_LEVEL_KEYS),
        "the written document's top-level keys must equal the pinned set the identity "
        f"committed to\n    pinned  {sorted(OUTPUT_TOP_LEVEL_KEYS)}\n"
        f"    actual  {sorted(document)}",
    )
    return document


def parse_args(argv: list[str] | None = None) -> argparse.Namespace:
    """Parse the pre-registered Stage-0 invocation.

    Inputs: an argument vector, or ``None`` for ``sys.argv``. Outputs: the namespace.
    Purpose: every default below is the pre-registered value from Protocol P section 8,
    so the bare command reproduces the pinned run; paths are project-relative and may be
    overridden, never hard-coded.
    """

    parser = argparse.ArgumentParser(
        description="Protocol P Stage 0: the sensor-only difference null (0 rollouts).",
    )
    parser.add_argument("--window", type=int, default=768)
    parser.add_argument("--f-ctrl-hz", type=float, default=500.0)
    parser.add_argument("--diagnostic-hz", type=float, default=0.8)
    parser.add_argument("--thermal-ramp-c", type=float, default=3.0)
    parser.add_argument("--pairs", type=int, default=100)
    parser.add_argument("--seed", type=int, default=0)
    parser.add_argument("--pair-id", type=int, default=1)
    parser.add_argument(
        "--config", type=Path, default=Path("config/draft-config-v0.1.json")
    )
    parser.add_argument("--schema", type=Path, default=Path("schema/schema.json"))
    parser.add_argument(
        "--assignment",
        type=Path,
        default=Path("config/proposed-gate3-assignment-v0.1.json"),
    )
    parser.add_argument(
        "--protocol", type=Path, default=Path(f"protocol/{PROTOCOL_FILENAME}")
    )
    parser.add_argument("--output-dir", type=Path, default=Path("results/protocol_p"))
    return parser.parse_args(argv)


def main(argv: list[str] | None = None) -> int:
    """Verify the pins, measure the null, and write the pinned artifact.

    Inputs: an argument vector, or ``None`` for ``sys.argv``. Outputs: a process exit
    status, 0 only when every pin matched, every invariant held, and the artifact was
    written. Purpose: the executable form of Protocol P Stage 0.
    """

    args = parse_args(argv)

    print("=" * 78)
    print("Protocol P Stage 0 - sensor-only difference null (0 rollouts)")
    print("=" * 78)

    print("\nI1 - text-domain pins")
    digests = verify_text_pins(args.protocol.resolve(), args.assignment.resolve())
    print(f"  protocol    {digests['protocol']}")
    print(f"  assignment  {digests['assignment']}")
    print("  I1 PASS")

    print("\nInputs - base config and approved assignment binding")
    config = load_config(args.config.resolve(), args.schema.resolve())
    assignment = load_assignment(args.assignment.resolve())
    binding = validate_approved_assignment_binding(config, expected_assignment=assignment)
    print(f"  base config hash   {config.config_hash}")
    print(f"  assignment hash    {binding.assignment_hash}")

    cli = {
        "window": int(args.window),
        "f_ctrl_hz": float(args.f_ctrl_hz),
        "diagnostic_hz": float(args.diagnostic_hz),
        "thermal_ramp_c": float(args.thermal_ramp_c),
        "pairs": int(args.pairs),
        "seed": int(args.seed),
        "pair_id": int(args.pair_id),
    }

    print("\nI8 - Stage-0 artifact-level identity")
    identity, canonical = stage_0_identity(
        base_config_hash=config.config_hash,
        assignment_canonical_sha256=digests["assignment"],
        assignment_hash=binding.assignment_hash,
        protocol_spec_sha256=digests["protocol"],
        cli=cli,
    )
    print(f"  identity   {identity}")
    print(f"  canonical  {len(canonical):,d} characters, recorded verbatim in the artifact")
    print("  I8 PASS")

    print(f"\nMeasurement - {args.pairs} pairs, window {args.window}, pair_id {args.pair_id}")
    measurement = run_null(
        window=args.window,
        f_ctrl_hz=args.f_ctrl_hz,
        diagnostic_hz=args.diagnostic_hz,
        thermal_ramp_c=args.thermal_ramp_c,
        pairs=args.pairs,
        seed=args.seed,
        pair_id=args.pair_id,
    )

    document = build_document(
        measurement=measurement,
        identity=identity,
        canonical=canonical,
        digests=digests,
        base_config_hash=config.config_hash,
        assignment_hash=binding.assignment_hash,
        cli=cli,
    )

    distribution = document["null_distribution"]
    corroboration = document["corroboration"]
    print("\nNull distribution")
    for key in ("mean", "std", "min", "median", "max", "q95_method_higher"):
        print(f"  {key:18s} {distribution[key]:.6f}")
    print("\nCorroboration - conditional healthy-null diagnostic, no authority")
    low, high = corroboration["real_plant_q95_range"]
    print(f"  real-plant per-cell Q95 range   [{low:.4f}, {high:.4f}]")
    print(f"  Stage-0 Q95 inside that range   {corroboration['q95_inside_real_plant_range']}")
    print("  This sets no threshold and gates nothing.")

    output_dir = args.output_dir.resolve()
    output_dir.mkdir(parents=True, exist_ok=True)
    output_path = output_dir / OUTPUT_FILENAME
    output_path.write_text(
        json.dumps(document, indent=2, ensure_ascii=False, allow_nan=False) + "\n",
        encoding="utf-8",
    )
    print(f"\nWrote {output_path}")
    print("  Stage 0 complete. It authorizes nothing on its own.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
