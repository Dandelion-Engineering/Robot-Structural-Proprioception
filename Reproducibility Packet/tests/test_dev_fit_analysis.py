"""Tests for the bounded, read-only analysis of the first Gate-4 dev fit."""

from __future__ import annotations

import copy
import json
import math
import sys
from pathlib import Path

import pytest

PACKET_ROOT = Path(__file__).resolve().parents[1]
SCRIPTS_DIR = PACKET_ROOT / "scripts"
sys.path.insert(0, str(SCRIPTS_DIR))

import analyze_dev_fit as analysis  # noqa: E402
from utils import dev_fit_trainer as trainer  # noqa: E402

RESULT_PATH = PACKET_ROOT / "results" / "dev_fit" / "dev_fit_result.json"


def _result() -> dict:
    """Return an independent copy of the tracked ten-arm fit result."""

    return json.loads(RESULT_PATH.read_text(encoding="utf-8"))


def test_tracked_fit_result_is_the_complete_authorized_ten_arm_state():
    """The analysis ingress accepts the tracked fit and preserves plan ordering."""

    arms = analysis.validate_fit_result(_result())

    assert [(arm["suite"], arm["training_seed"]) for arm in arms] == list(
        trainer.matched_fit_plan()
    )
    assert all(arm["n_examples"] == 152 for arm in arms)


@pytest.mark.parametrize(
    ("mutation", "match"),
    [
        (lambda document: document.update({"rollouts_spent": 1}), "spent rollouts"),
        (lambda document: document["arms"].__setitem__(1, copy.deepcopy(document["arms"][0])), "repeats arm"),
        (lambda document: document["arms"][0].update({"n_examples": 151}), "152 examples"),
        (lambda document: document["arms"][0].update({"code_identity": {}}), "code identity diverges"),
        (lambda document: document["final_losses"][0].update({"final_loss": 99.0}), "final-loss index"),
    ],
)
def test_fit_result_mutations_fail_closed(mutation, match):
    """Fields that make the readback interpretable cannot drift independently."""

    document = _result()
    mutation(document)

    with pytest.raises(analysis.DevFitAnalysisError, match=match):
        analysis.validate_fit_result(document)


def test_strict_json_rejects_duplicate_keys_and_nonfinite_constants(tmp_path):
    """The artifact loader does not accept implementation-defined JSON."""

    duplicate = tmp_path / "duplicate.json"
    duplicate.write_text('{"exit":"a","exit":"b"}', encoding="utf-8", newline="\n")
    nonfinite = tmp_path / "nonfinite.json"
    nonfinite.write_text('{"value":NaN}', encoding="utf-8", newline="\n")

    with pytest.raises(analysis.DevFitAnalysisError, match="strict JSON"):
        analysis.load_strict_json(duplicate, "fixture")
    with pytest.raises(analysis.DevFitAnalysisError, match="strict JSON"):
        analysis.load_strict_json(nonfinite, "fixture")


def test_classification_metrics_use_the_fixed_four_class_universe():
    """An absent predicted class contributes zero F1 instead of disappearing."""

    metrics = analysis.classification_metrics(
        [0, 1, 2, 3], [0, 0, 2, 2], n_classes=4
    )

    assert metrics["accuracy"] == 0.5
    assert metrics["per_class_f1"] == {
        "healthy": pytest.approx(2 / 3),
        "structure": 0.0,
        "actuator": pytest.approx(2 / 3),
        "sensor": 0.0,
    }
    assert metrics["macro_f1"] == pytest.approx(1 / 3)

    with pytest.raises(analysis.DevFitAnalysisError, match="fixed source-class universe"):
        analysis.classification_metrics([0, 1], [0, 1], n_classes=3)


def test_sample_standard_deviation_is_not_population_sd():
    """The five-seed warning reports ordinary n-1 sample dispersion."""

    values = [0.075, 0.039, -0.239, 0.104, -0.140]

    assert analysis.sample_standard_deviation(values) == pytest.approx(0.149581750224)
    population = math.sqrt(
        sum((value - sum(values) / len(values)) ** 2 for value in values) / len(values)
    )
    assert analysis.sample_standard_deviation(values) > population


def test_analysis_code_identity_uses_only_bare_labels_and_exact_digests():
    """The persisted analysis provenance cannot disclose a local path."""

    identity = analysis.analysis_code_identity()

    assert set(identity) == {
        "analyze_dev_fit.py",
        "attribution_net.py",
        "config_contract.py",
        "dev_fit_contract.py",
        "dev_fit_trainer.py",
        "estimator.py",
        "role_contract.py",
        "schema_types.py",
        "storage_contract.py",
    }
    assert all("/" not in label and "\\" not in label for label in identity)
    assert all(analysis.SHA256_RE.fullmatch(digest) for digest in identity.values())
