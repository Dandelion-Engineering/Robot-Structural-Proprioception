"""Tests for Protocol P Stage 0 — the sensor-only difference null (Claude's lane).

These cover the layers that decide whether Stage 0's *result* would be interpretable:
the canonical serialization rule, the pinned seed mapping, the statistic, the two
text-domain pins, the artifact-level identity, and the binding between the identity's
recorded ``output_schema`` and the document actually written.

Deliberately portable, and deliberately NOT an execution of Stage 0. They run on a clean
checkout with no retained dataset and no plant: none of them performs the pinned 100-pair
measurement or writes the pinned artifact. Stage 0 itself remains unauthorized until its
own exact-state review.
"""

from __future__ import annotations

import json
import math
import sys
from pathlib import Path

import numpy as np
import pytest

PACKET_ROOT = Path(__file__).resolve().parents[1]
SCRIPTS_DIR = PACKET_ROOT / "scripts"
sys.path.insert(0, str(SCRIPTS_DIR))

import analyze_synchronous_difference_null as mod  # noqa: E402
from utils.schema_types import N_GAUGES  # noqa: E402

PROTOCOL_PATH = PACKET_ROOT / "protocol" / mod.PROTOCOL_FILENAME
ASSIGNMENT_PATH = PACKET_ROOT / "config" / mod.ASSIGNMENT_FILENAME

BASE_CONFIG_HASH = "dev-712abf27c3f8f3c331ae9b76e3f22c48857334cc15a81e819718165e47753e56"
ASSIGNMENT_HASH = "dev-eec59ec8a296a9a4ff4909f8e7f1de91a0a8f4bf289ae1533a427d1a87bc33f1"

PINNED_CLI = {
    "window": 768,
    "f_ctrl_hz": 500.0,
    "diagnostic_hz": 0.8,
    "thermal_ramp_c": 3.0,
    "pairs": 100,
    "seed": 0,
    "pair_id": 1,
}


def _identity_kwargs(**overrides: object) -> dict[str, object]:
    """Build the identity call's arguments, with per-test overrides."""

    kwargs: dict[str, object] = {
        "base_config_hash": BASE_CONFIG_HASH,
        "assignment_canonical_sha256": mod.ASSIGNMENT_CANONICAL_SHA256,
        "assignment_hash": ASSIGNMENT_HASH,
        "protocol_spec_sha256": mod.PROTOCOL_CANONICAL_SHA256,
        "cli": dict(PINNED_CLI),
    }
    kwargs.update(overrides)
    return kwargs


def _measurement(distances: list[float]) -> dict[str, object]:
    """A measurement block shaped like ``run_null``'s output, without measuring.

    The distribution block comes from the production ``summarize_null`` rather than a
    second copy of that arithmetic. A duplicate here would agree with itself while the
    real summary drifted — which is exactly how the first version of this file failed to
    notice a mutated quantile method.
    """

    return {
        "samples": {
            "n_pairs": len(distances),
            "seed_map": "pair p consumes sensor_seed (seed + 2p, seed + 2p + 1)",
            "sensor_seeds_consumed": [0, 2 * len(distances) - 1],
            "sensor_seeds_consumed_note": "inclusive first and last of a contiguous range",
            "pair_id": 1,
            "distances": [float(value) for value in distances],
        },
        "null_distribution": mod.summarize_null(distances),
    }


def _document(distances: list[float]) -> dict[str, object]:
    """Assemble a document through the real builder."""

    identity, canonical = mod.stage_0_identity(**_identity_kwargs())  # type: ignore[arg-type]
    return mod.build_document(
        measurement=_measurement(distances),
        identity=identity,
        canonical=canonical,
        digests={
            "protocol": mod.PROTOCOL_CANONICAL_SHA256,
            "assignment": mod.ASSIGNMENT_CANONICAL_SHA256,
        },
        base_config_hash=BASE_CONFIG_HASH,
        assignment_hash=ASSIGNMENT_HASH,
        cli=dict(PINNED_CLI),
    )


# --------------------------------------------------------------------------- #
# CANONICAL_JSON (Protocol P Correction 2)
# --------------------------------------------------------------------------- #
def test_canonical_json_sorts_keys_and_uses_compact_separators() -> None:
    assert mod.canonical_json({"b": 1, "a": [1, 2]}) == '{"a":[1,2],"b":1}'


def test_canonical_json_preserves_non_ascii() -> None:
    """``ensure_ascii=False`` is part of the rule; escaping would change the digest."""

    assert mod.canonical_json({"unit": "µε"}) == '{"unit":"µε"}'


@pytest.mark.parametrize("bad", [float("nan"), float("inf"), float("-inf")])
def test_canonical_json_refuses_a_non_finite_float(bad: float) -> None:
    """The load-bearing half of the rule.

    Plain ``json.dumps`` emits the non-standard tokens ``NaN`` / ``Infinity`` rather than
    raising, which would produce a valid-looking digest over an unparseable document.
    """

    with pytest.raises(ValueError):
        mod.canonical_json({"value": bad})


# --------------------------------------------------------------------------- #
# The pinned seed mapping (Protocol P section 6)
# --------------------------------------------------------------------------- #
def test_the_pinned_invocation_consumes_exactly_sensor_seeds_0_through_199() -> None:
    """Section 6 pins Stage 0's consumed range; the mapping must reproduce it exactly."""

    consumed: list[int] = []
    for index in range(PINNED_CLI["pairs"]):
        consumed.extend(mod.pair_seeds(PINNED_CLI["seed"], index))
    assert consumed == list(range(200))
    assert len(set(consumed)) == 200


def test_pair_seeds_never_reuses_a_seed_within_a_pair() -> None:
    seed_a, seed_b = mod.pair_seeds(0, 5)
    assert (seed_a, seed_b) == (10, 11)


def test_pair_seeds_rejects_a_negative_index() -> None:
    with pytest.raises(ValueError):
        mod.pair_seeds(0, -1)


# --------------------------------------------------------------------------- #
# The statistic (Protocol P section 8)
# --------------------------------------------------------------------------- #
def test_the_statistic_has_exactly_two_entries_per_gauge() -> None:
    """Schema growth must fail loudly rather than silently reshape the statistic."""

    assert mod.N_STATISTIC_ENTRIES == 2 * N_GAUGES


def test_the_statistic_is_zero_for_two_identical_vectors() -> None:
    vector = np.arange(mod.N_STATISTIC_ENTRIES, dtype=float)
    assert mod.difference_statistic(vector, vector) == 0.0


def test_the_statistic_is_the_l2_norm_of_the_difference() -> None:
    a = np.zeros(mod.N_STATISTIC_ENTRIES)
    b = np.zeros(mod.N_STATISTIC_ENTRIES)
    a[0], b[1] = 3.0, 4.0
    assert mod.difference_statistic(a, b) == pytest.approx(5.0)


def test_the_statistic_is_symmetric() -> None:
    rng = np.random.default_rng(0)
    a = rng.normal(size=mod.N_STATISTIC_ENTRIES)
    b = rng.normal(size=mod.N_STATISTIC_ENTRIES)
    assert mod.difference_statistic(a, b) == pytest.approx(mod.difference_statistic(b, a))


@pytest.mark.parametrize("length", [0, 7, 9, 16])
def test_the_statistic_refuses_a_wrong_length_vector(length: int) -> None:
    good = np.zeros(mod.N_STATISTIC_ENTRIES)
    with pytest.raises(mod.ProtocolPError, match="entries"):
        mod.difference_statistic(good, np.zeros(length))


@pytest.mark.parametrize("bad", [float("nan"), float("inf")])
def test_the_statistic_refuses_a_non_finite_coefficient(bad: float) -> None:
    """A NaN reaching the statistic would propagate into the null silently."""

    good = np.zeros(mod.N_STATISTIC_ENTRIES)
    poisoned = np.zeros(mod.N_STATISTIC_ENTRIES)
    poisoned[3] = bad
    with pytest.raises(mod.ProtocolPError, match="non-finite"):
        mod.difference_statistic(good, poisoned)


def test_the_coefficient_vector_is_gauge_major_and_eight_entries_long() -> None:
    """One (cos, sin) pair per gauge, ordered gauge 0 first, as section 8's concat says."""

    window = 256
    f_ctrl, f_d = 500.0, 0.8
    t_s = np.arange(window) / f_ctrl
    values = np.zeros((window, N_GAUGES))
    values[:, 2] = np.cos(2.0 * np.pi * f_d * t_s)  # only gauge 2 carries a tone
    valid = np.ones((window, N_GAUGES), dtype=bool)

    vector = mod.coefficient_vector(values, valid, t_s, f_d)
    assert vector.shape == (mod.N_STATISTIC_ENTRIES,)
    assert np.linalg.norm(vector[4:6]) > 0.5  # gauge 2 occupies entries 4 and 5
    for gauge in (0, 1, 3):
        assert np.allclose(vector[2 * gauge : 2 * gauge + 2], 0.0, atol=1e-9)


def test_the_coefficient_vector_tolerates_invalid_samples() -> None:
    """``gauge_obs`` carries real dropout and latency NaNs; the fit must be NaN-aware."""

    window = 256
    f_ctrl, f_d = 500.0, 0.8
    t_s = np.arange(window) / f_ctrl
    values = np.tile(np.cos(2.0 * np.pi * f_d * t_s)[:, None], (1, N_GAUGES))
    valid = np.ones((window, N_GAUGES), dtype=bool)
    values[::7, :] = np.nan
    valid[::7, :] = False

    vector = mod.coefficient_vector(values, valid, t_s, f_d)
    assert np.all(np.isfinite(vector))


def test_the_coefficient_vector_refuses_a_mismatched_time_grid() -> None:
    window = 64
    t_s = np.arange(window + 1) / 500.0
    with pytest.raises(mod.ProtocolPError, match="time grid"):
        mod.coefficient_vector(
            np.zeros((window, N_GAUGES)),
            np.ones((window, N_GAUGES), dtype=bool),
            t_s,
            0.8,
        )


def test_the_coefficient_vector_refuses_a_wrong_gauge_count() -> None:
    window = 64
    with pytest.raises(mod.ProtocolPError, match="values must be"):
        mod.coefficient_vector(
            np.zeros((window, N_GAUGES + 1)),
            np.ones((window, N_GAUGES + 1), dtype=bool),
            np.arange(window) / 500.0,
            0.8,
        )


# --------------------------------------------------------------------------- #
# I1 — the two text-domain pins
# --------------------------------------------------------------------------- #
def test_the_committed_pre_registration_has_not_drifted() -> None:
    """A permanent automated check that the tracked pins still match the approved bytes.

    This is the same guarantee the replay gate's suite carries: if either tracked text
    file changes, this goes red rather than a stage silently absorbing the new digest
    into a valid-looking identity.
    """

    digests = mod.verify_text_pins(PROTOCOL_PATH, ASSIGNMENT_PATH)
    assert digests["protocol"] == mod.PROTOCOL_CANONICAL_SHA256
    assert digests["assignment"] == mod.ASSIGNMENT_CANONICAL_SHA256


def test_a_protocol_filename_the_script_was_not_approved_for_is_refused(
    tmp_path: Path,
) -> None:
    """A version bump must update the pinned digest in the same commit."""

    wrong = tmp_path / "protocol-p-v9.9.9.md"
    wrong.write_bytes(PROTOCOL_PATH.read_bytes())
    with pytest.raises(mod.ProtocolPError, match="approved for"):
        mod.verify_text_pins(wrong, ASSIGNMENT_PATH)


def test_a_drifted_protocol_digest_is_refused(tmp_path: Path) -> None:
    """Give the guard a real file with the right name and the wrong bytes."""

    drifted = tmp_path / mod.PROTOCOL_FILENAME
    drifted.write_bytes(PROTOCOL_PATH.read_bytes() + b"\nan unapproved edit\n")
    with pytest.raises(mod.ProtocolPError, match=r"I1 \[protocol\]: canonical digest"):
        mod.verify_text_pins(drifted, ASSIGNMENT_PATH)


def test_a_drifted_assignment_digest_is_refused(tmp_path: Path) -> None:
    drifted = tmp_path / mod.ASSIGNMENT_FILENAME
    drifted.write_bytes(ASSIGNMENT_PATH.read_bytes() + b"\n")
    with pytest.raises(mod.ProtocolPError, match=r"I1 \[assignment\]: canonical digest"):
        mod.verify_text_pins(PROTOCOL_PATH, drifted)


def test_an_absent_pin_is_refused_rather_than_skipped(tmp_path: Path) -> None:
    """Never fall back to whatever is on disk."""

    absent = tmp_path / mod.PROTOCOL_FILENAME
    with pytest.raises(mod.ProtocolPError, match="is absent"):
        mod.verify_text_pins(absent, ASSIGNMENT_PATH)


# --------------------------------------------------------------------------- #
# I8 — the artifact-level identity (Protocol P Correction 6)
# --------------------------------------------------------------------------- #
def test_the_identity_is_recomputable_from_the_recorded_canonical_string() -> None:
    """Correction 8's discipline: the recorded string must be the object that was hashed.

    A second call that ought to agree is not the same thing as the same object, so this
    recomputes the digest from the returned string rather than from a fresh payload.
    """

    import hashlib

    identity, canonical = mod.stage_0_identity(**_identity_kwargs())  # type: ignore[arg-type]
    recomputed = "dev-" + hashlib.sha256(canonical.encode("utf-8")).hexdigest()
    assert recomputed == identity


def test_the_identity_is_dev_prefixed_lowercase_hex() -> None:
    identity, _ = mod.stage_0_identity(**_identity_kwargs())  # type: ignore[arg-type]
    assert identity.startswith("dev-")
    body = identity[4:]
    assert len(body) == 64
    assert body == body.lower()
    int(body, 16)  # raises if it is not hex


def test_the_identity_records_the_pinned_output_schema() -> None:
    """The schema in the identity must be the same object the writer checks against."""

    _, canonical = mod.stage_0_identity(**_identity_kwargs())  # type: ignore[arg-type]
    payload = json.loads(canonical)
    assert payload["output_schema"] == sorted(mod.OUTPUT_TOP_LEVEL_KEYS)
    assert payload["stage"] == "0"


def test_the_identity_changes_when_any_cli_value_changes() -> None:
    """Two runs at different settings must not share one identity."""

    baseline, _ = mod.stage_0_identity(**_identity_kwargs())  # type: ignore[arg-type]
    for key in PINNED_CLI:
        altered = dict(PINNED_CLI)
        altered[key] = PINNED_CLI[key] + 1
        other, _ = mod.stage_0_identity(**_identity_kwargs(cli=altered))  # type: ignore[arg-type]
        assert other != baseline, f"identity ignored a change to {key}"


def test_i8_rejects_an_identity_equal_to_the_base_config_hash() -> None:
    """I8's base-distinctness requirement, fed the exact state it rejects.

    The guard is tested directly rather than through ``stage_0_identity``, because from
    that construction path the state is unreachable: the identity is a hash *of* a
    document containing ``base_config_hash``, so a collision would need a SHA-256 fixed
    point. Routing this through the constructor would produce a test that cannot go red.
    """

    collision = "dev-" + "a" * 64
    with pytest.raises(mod.ProtocolPError, match="must differ from the base config hash"):
        mod.require_valid_stage_0_identity(collision, collision)


@pytest.mark.parametrize(
    "bad",
    [
        "712abf27c3f8f3c331ae9b76e3f22c48857334cc15a81e819718165e47753e56",  # no prefix
        "screen-" + "a" * 64,  # wrong prefix
        "dev-" + "a" * 63,  # too short
        "dev-" + "a" * 65,  # too long
        "dev-" + "A" * 64,  # uppercase
        "dev-" + "z" * 64,  # not hex
    ],
)
def test_i8_rejects_a_malformed_identity(bad: str) -> None:
    """Each malformed shape must raise, not merely be reported."""

    with pytest.raises(mod.ProtocolPError, match="I8"):
        mod.require_valid_stage_0_identity(bad, BASE_CONFIG_HASH)


def test_i8_accepts_the_identity_the_constructor_actually_produces() -> None:
    """The guard's passing branch, and the wire from the constructor to the guard."""

    identity, _ = mod.stage_0_identity(**_identity_kwargs())  # type: ignore[arg-type]
    mod.require_valid_stage_0_identity(identity, BASE_CONFIG_HASH)


def test_the_constructor_is_wired_to_the_i8_guard(monkeypatch: pytest.MonkeyPatch) -> None:
    """Unit-testing both ends of a wire does not test the wire.

    ``stage_0_identity`` must actually call the guard, not merely be accompanied by it in
    the same module. Replacing the guard with one that always raises proves the call
    happens on the real construction path.
    """

    def explode(identity: str, base_config_hash: str) -> None:
        raise mod.ProtocolPError("guard reached")

    monkeypatch.setattr(mod, "require_valid_stage_0_identity", explode)
    with pytest.raises(mod.ProtocolPError, match="guard reached"):
        mod.stage_0_identity(**_identity_kwargs())  # type: ignore[arg-type]


def test_a_non_finite_cli_value_cannot_produce_an_identity() -> None:
    """``allow_nan=False`` reaching through the identity path, not just the helper."""

    altered = dict(PINNED_CLI)
    altered["thermal_ramp_c"] = float("nan")
    with pytest.raises(ValueError):
        mod.stage_0_identity(**_identity_kwargs(cli=altered))  # type: ignore[arg-type]


# --------------------------------------------------------------------------- #
# The null summary and the seed-uniqueness guard
# --------------------------------------------------------------------------- #
def test_the_q95_is_an_order_statistic_of_the_sample() -> None:
    """``method='higher'`` must return an observed value, never an interpolation.

    This is what makes Stage 0's Q95 comparable to the real-plant per-cell Q95 values,
    which are order statistics of 28 within-cell distances under the same method.
    """

    distances = [0.31, 0.33, 0.37, 0.41, 0.44]
    summary = mod.summarize_null(distances)
    assert summary["q95_method_higher"] in distances
    assert summary["q95_method_higher"] == pytest.approx(0.44)


def test_the_q95_takes_the_higher_of_two_bracketing_samples() -> None:
    """The discriminating case: 'lower' would return 0.40 here, 'higher' returns 0.45."""

    summary = mod.summarize_null([0.30, 0.35, 0.40, 0.45])
    assert summary["q95_method_higher"] == pytest.approx(0.45)
    assert summary["quantile_method"] == "higher"


def test_the_summary_describes_the_samples_it_was_given() -> None:
    distances = [0.31, 0.33, 0.37, 0.41, 0.44]
    summary = mod.summarize_null(distances)
    assert summary["mean"] == pytest.approx(float(np.mean(distances)))
    assert summary["std"] == pytest.approx(float(np.std(distances)))
    assert summary["min"] == pytest.approx(min(distances))
    assert summary["max"] == pytest.approx(max(distances))
    assert summary["median"] == pytest.approx(float(np.median(distances)))


@pytest.mark.parametrize("distances", [[], [0.3]])
def test_the_summary_refuses_a_sample_too_small_to_be_a_null(
    distances: list[float],
) -> None:
    with pytest.raises(mod.ProtocolPError, match="at least 2 samples"):
        mod.summarize_null(distances)


@pytest.mark.parametrize("bad", [float("nan"), float("inf")])
def test_the_summary_refuses_a_non_finite_sample(bad: float) -> None:
    with pytest.raises(mod.ProtocolPError, match="non-finite"):
        mod.summarize_null([0.3, 0.4, bad])


def test_the_seed_guard_rejects_a_repeated_identity() -> None:
    """Two samples at one sensor identity would not be independent.

    Fed the exact state it exists to catch. Unlike I8 this state is constructable, so the
    guard is genuinely reachable — a pair mapping that overlapped would produce it.
    """

    with pytest.raises(mod.ProtocolPError, match="exactly once"):
        mod.require_unique_seeds([0, 1, 1, 2])


def test_the_seed_guard_accepts_the_pinned_mapping() -> None:
    consumed: list[int] = []
    for index in range(PINNED_CLI["pairs"]):
        consumed.extend(mod.pair_seeds(PINNED_CLI["seed"], index))
    mod.require_unique_seeds(consumed)


# --------------------------------------------------------------------------- #
# The measurement loop's wires
#
# These call `run_null` at a deliberately tiny size. That is NOT an execution of
# Stage 0: the pre-registered stage is 100 pairs at window 768 with pair_id 1 writing
# `results/protocol_p/sensor_only_difference_null.json`, and nothing here writes any
# artifact or produces any protocol number. What they cover is the wiring the pure-layer
# tests structurally cannot: that the CLI values reach the sensor draws.
# --------------------------------------------------------------------------- #
# Three pairs, not two. At two samples every statistic in the summary is insensitive to
# order and to dropping one element, so a truncated or re-sorted summary would be an
# equivalent mutation and the wire test below could not go red. The fixture has to be
# large enough for the property it checks to be discriminating.
TINY = {"window": 640, "f_ctrl_hz": 500.0, "diagnostic_hz": 0.8, "thermal_ramp_c": 3.0,
        "pairs": 3, "seed": 0}


def test_run_null_passes_pair_id_through_to_the_draws() -> None:
    """A pair_id accepted by the CLI and dropped before the draws would be invisible.

    The identity written into the artifact records the requested ``pair_id``; if the
    measurement ignored it, every sample would come from a different identity than the
    one the artifact claims.
    """

    one = mod.run_null(pair_id=1, **TINY)
    two = mod.run_null(pair_id=2, **TINY)
    assert one["samples"]["distances"] != two["samples"]["distances"]
    assert two["samples"]["pair_id"] == 2


def test_run_null_is_deterministic_at_one_identity() -> None:
    """The complement: the same request must reproduce the same null exactly."""

    first = mod.run_null(pair_id=1, **TINY)
    second = mod.run_null(pair_id=1, **TINY)
    assert first["samples"]["distances"] == second["samples"]["distances"]


def test_run_null_consumes_each_sensor_seed_exactly_once() -> None:
    """Three pairs must consume six distinct seeds, reported as a contiguous range."""

    result = mod.run_null(pair_id=1, **TINY)
    assert result["samples"]["sensor_seeds_consumed"] == [0, 5]
    assert result["samples"]["n_pairs"] == 3
    assert len(result["samples"]["distances"]) == 3


def test_run_null_summarizes_the_samples_it_actually_collected() -> None:
    """The summary must describe this run's distances, not a subset or a second set.

    Comparing the returned block against the production summary of the returned distances
    is what makes a truncated or re-derived summary visible; asserting each statistic's
    value separately would not, because both sides would move together.
    """

    result = mod.run_null(pair_id=1, **TINY)
    assert result["null_distribution"] == mod.summarize_null(result["samples"]["distances"])


def test_run_null_is_wired_to_the_seed_uniqueness_guard(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    """Removing the call must not be invisible.

    With the correct pair mapping no duplicate seed can occur, so calling the guard and
    not calling it are behaviourally identical and no ordinary test can tell them apart.
    Replacing the guard with one that always raises is what observes the call itself.
    """

    def explode(consumed: object) -> None:
        raise mod.ProtocolPError("seed guard reached")

    monkeypatch.setattr(mod, "require_unique_seeds", explode)
    with pytest.raises(mod.ProtocolPError, match="seed guard reached"):
        mod.run_null(pair_id=1, **TINY)


def test_run_null_produces_a_positive_sensor_only_difference() -> None:
    """Two sensor identities over identical zero strain must not agree exactly.

    If they did, the statistic would be measuring nothing and the null would be a
    degenerate zero — the shape a silently-shared RNG stream would produce.
    """

    distances = mod.run_null(pair_id=1, **TINY)["samples"]["distances"]
    assert all(value > 0.0 for value in distances)
    assert all(math.isfinite(value) for value in distances)


@pytest.mark.parametrize(
    ("field", "value"),
    [("window", 4), ("pairs", 1), ("f_ctrl_hz", 0.0), ("diagnostic_hz", -1.0),
     ("thermal_ramp_c", float("nan"))],
)
def test_run_null_refuses_an_unusable_request(field: str, value: object) -> None:
    """Every precondition raises ProtocolPError rather than measuring something wrong."""

    request = dict(TINY)
    request[field] = value
    with pytest.raises(mod.ProtocolPError):
        mod.run_null(pair_id=1, **request)


# --------------------------------------------------------------------------- #
# The written artifact
# --------------------------------------------------------------------------- #
def test_the_document_top_level_keys_equal_the_pinned_set() -> None:
    document = _document([0.30, 0.35, 0.40, 0.45])
    assert sorted(document) == sorted(mod.OUTPUT_TOP_LEVEL_KEYS)


def test_a_document_whose_keys_drift_from_the_identity_is_refused(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    """The check must be able to go red, so make the pinned set disagree with the writer."""

    monkeypatch.setattr(
        mod, "OUTPUT_TOP_LEVEL_KEYS", mod.OUTPUT_TOP_LEVEL_KEYS + ("an_unwritten_key",)
    )
    with pytest.raises(mod.ProtocolPError, match="top-level keys"):
        _document([0.30, 0.35, 0.40, 0.45])


def test_the_document_records_the_canonical_string_verbatim() -> None:
    document = _document([0.30, 0.35, 0.40, 0.45])
    payload = json.loads(document["stage_0_canonical"])
    assert payload["cli"] == PINNED_CLI


def test_the_document_is_serializable_without_non_finite_tokens() -> None:
    """Nothing may reach the artifact that ``allow_nan=False`` would reject."""

    document = _document([0.30, 0.35, 0.40, 0.45])
    json.dumps(document, allow_nan=False)


def test_the_corroboration_flag_is_true_inside_the_real_plant_range() -> None:
    """A Q95 inside the recorded per-cell range is the only sense of corroboration."""

    document = _document([0.38] * 20)
    corroboration = document["corroboration"]
    assert corroboration["q95_inside_real_plant_range"] is True
    assert corroboration["real_plant_q95_range"] == [0.3176, 0.4251]


@pytest.mark.parametrize("value", [0.05, 0.90])
def test_the_corroboration_flag_is_false_outside_the_real_plant_range(value: float) -> None:
    """The flag must discriminate; a containment check that never fails says nothing."""

    document = _document([value] * 20)
    assert document["corroboration"]["q95_inside_real_plant_range"] is False


def test_the_corroboration_block_disclaims_all_authority() -> None:
    """Stage 0 sets no threshold and gates nothing; the artifact has to say so."""

    document = _document([0.38] * 20)
    authority = document["corroboration"]["authority"]
    assert "NONE" in authority
    assert "gates nothing" in authority


def test_the_artifact_carries_its_conditionality_boundaries() -> None:
    document = _document([0.38] * 20)
    joined = " ".join(document["boundaries"])
    for required in ("pair_id", "no plant", "threshold"):
        assert required in joined


def test_the_recorded_quantile_method_is_higher() -> None:
    """The protocol's Q95 is an order statistic under ``method='higher'``."""

    document = _document([0.30, 0.35, 0.40, 0.45])
    assert document["null_distribution"]["quantile_method"] == "higher"
    assert document["null_distribution"]["q95_method_higher"] == pytest.approx(0.45)


def test_the_distribution_summary_matches_the_recorded_samples() -> None:
    """The summary must describe the samples the artifact carries, not a second set."""

    distances = [0.31, 0.33, 0.37, 0.41, 0.44]
    document = _document(distances)
    recorded = document["samples"]["distances"]
    summary = document["null_distribution"]
    assert recorded == distances
    assert summary["mean"] == pytest.approx(float(np.mean(distances)))
    assert summary["min"] == pytest.approx(min(distances))
    assert summary["max"] == pytest.approx(max(distances))
    assert math.isclose(summary["median"], float(np.median(distances)))
