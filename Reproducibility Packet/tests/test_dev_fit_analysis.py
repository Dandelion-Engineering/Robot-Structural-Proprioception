"""Tests for the bounded, read-only analysis of the first Gate-4 dev fit."""

from __future__ import annotations

import copy
import json
import math
import sys
from pathlib import Path
from types import SimpleNamespace

import pytest

PACKET_ROOT = Path(__file__).resolve().parents[1]
SCRIPTS_DIR = PACKET_ROOT / "scripts"
sys.path.insert(0, str(SCRIPTS_DIR))

import torch  # noqa: E402

import analyze_dev_fit as analysis  # noqa: E402
from utils import dev_fit_trainer as trainer  # noqa: E402
from utils.attribution_net import TemporalAttributionNet, deterministic_conv_precision  # noqa: E402
from utils.dev_fit_contract import PREDECLARED_TRAINING_SEEDS, matched_fit_plan  # noqa: E402

RESULT_PATH = PACKET_ROOT / "results" / "dev_fit" / "dev_fit_result.json"
ANALYSIS_PATH = PACKET_ROOT / "results" / "dev_fit" / "dev_fit_analysis.json"


def _result() -> dict:
    """Return an independent copy of the tracked ten-arm fit result."""

    return json.loads(RESULT_PATH.read_text(encoding="utf-8"))


def _analysis() -> dict:
    """Return an independent copy of the tracked in-sample readback."""

    return json.loads(ANALYSIS_PATH.read_text(encoding="utf-8"))


def _synthetic_forward(n: int = 4, seed: int = 0):
    """Return heads and targets from one real forward pass at the production shape.

    No checkpoint, no delivered row: this exists so the loss decomposition can be driven
    against the trainer's own composite without the git-ignored dataset.
    """

    torch.manual_seed(seed)
    net = TemporalAttributionNet(seed=seed)
    net.eval()
    inputs = torch.randn(n, 36, trainer.DEVELOPMENT_WINDOW_STEPS)
    batch = {
        "inputs": inputs,
        "class_index": torch.zeros(n, dtype=torch.long),
        "location_index": torch.zeros(n, dtype=torch.long),
        "severity": torch.rand(n),
        "ood": torch.zeros(n),
    }
    with torch.no_grad(), deterministic_conv_precision():
        return net(inputs), batch


def _derived_examples(*, mismatched_s: bool = False, ood_s: bool = False):
    """Return a tiny dataset-free census for driving the derivation seam."""

    c1 = [SimpleNamespace(class_index=index, ood_flag=False) for index in range(4)]
    structural = [
        SimpleNamespace(class_index=index, ood_flag=(ood_s and index == 0))
        for index in range(4)
    ]
    if mismatched_s:
        structural[-1].class_index = 0
    return {"C1": c1, "S": structural}


def _patch_derive_inputs(monkeypatch, examples_by_suite):
    """Replace only the real-data/evaluation seams with deterministic fixtures."""

    fit_result = _result()
    data_census = {
        "manifest_sha256": "0" * 64,
        "assignment_sha256": fit_result["training_protocol"]["assignment_sha256"],
        "row_disclosure": "synthetic derivation fixture",
        "trajectory_census": analysis.EXPECTED_TRAJECTORY_CENSUS,
    }
    monkeypatch.setattr(
        analysis,
        "load_authorized_examples",
        lambda _data_root: (examples_by_suite, data_census),
    )

    def evaluate(arm, examples, _checkpoint_dir):
        suite_offset = 0.02 if arm["suite"] == "S" else 0.0
        score = 0.40 + 0.01 * arm["training_seed"] + suite_offset
        return {
            "suite": arm["suite"],
            "seed": arm["training_seed"],
            "n_examples": len(examples),
            "checkpoint_name": arm["checkpoint_name"],
            "checkpoint_sha256": arm["checkpoint_sha256"],
            "training_final_epoch_mean_loss": arm["final_loss"],
            "post_fit_full_batch_loss_terms": {
                "class_cross_entropy": 1.0,
                "location_cross_entropy": 2.0,
                "severity_gaussian_nll": -1.0,
                "ood_binary_cross_entropy": 0.5,
                "total": 2.5,
                "severity_log_scale_mean": -0.5,
            },
            "classification": {
                "accuracy": score,
                "macro_f1": score,
                "per_class_f1": {
                    "healthy": score,
                    "structure": score,
                    "actuator": score,
                    "sensor": score,
                },
            },
        }

    monkeypatch.setattr(analysis, "evaluate_arm", evaluate)


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
        # Every pin below was a mutation-sweep survivor before these cases existed: the
        # guard was correct and no test constructed a document that could violate it.
        (lambda document: document.update({"authority": "development-ish"}), "wrong authority"),
        (lambda document: document.update({"exit": "X_PLAN_OK"}), "X_FIT_OK"),
        (lambda document: document.update({"trajectory_census": {}}), "wrong trajectory census"),
        (lambda document: document["training_protocol"].update({"split": "pilot"}), "not dev-only"),
        (lambda document: document["training_protocol"].update({"epochs": 19}), "20 epochs"),
        (lambda document: document["training_protocol"].update({"batch_size": 16}), "batch size 8"),
        (lambda document: document["training_protocol"].update({"learning_rate": 0.01}),
         "learning rate 1e-3"),
        (lambda document: document["training_protocol"].update({"window_steps": 512}), "768 steps"),
        (lambda document: document["training_protocol"].update({"windows_per_run": 2}),
         "more than one window"),
        (lambda document: document["training_protocol"].update({"assignment_sha256": "0" * 64}),
         "approved assignment"),
        # A digest that is hexadecimal but the wrong LENGTH. This is the shape that
        # distinguishes a 64-character pin from a permissive one, and nothing reached it.
        (lambda document: document["arms"][0].update({"checkpoint_sha256": "abc"}),
         "no valid checkpoint digest"),
        (lambda document: document["code_identity"].update({"estimator.py": "abc"}),
         "is not a SHA-256 digest"),
        (lambda document: document["code_identity"].update({"utils/estimator.py": "0" * 64}),
         "not a bare name"),
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


def test_decomposed_loss_terms_sum_to_the_trainers_own_composite():
    """The decomposition is checked against `arm_loss`, not against a reading of it."""

    heads, batch = _synthetic_forward()

    terms = analysis.post_fit_loss_terms(heads, batch)
    composite = float(trainer.arm_loss(heads, batch))

    assert terms["total"] == pytest.approx(composite, abs=analysis.DECOMPOSITION_TOLERANCE)
    assert terms["total"] == pytest.approx(
        terms["class_cross_entropy"]
        + terms["location_cross_entropy"]
        + terms["severity_gaussian_nll"]
        + terms["ood_binary_cross_entropy"]
    )
    # The dict carries six keys and the total is the sum of exactly four of them, so a
    # future key cannot be absorbed into the total by being added above it.
    assert set(terms) == {
        "class_cross_entropy",
        "location_cross_entropy",
        "severity_gaussian_nll",
        "ood_binary_cross_entropy",
        "total",
        "severity_log_scale_mean",
    }
    assert terms["total"] != pytest.approx(sum(
        value for key, value in terms.items() if key != "total"
    ))


def test_decomposition_refuses_when_it_disagrees_with_the_trainer(monkeypatch):
    """A copy that drifts from its original is refused rather than persisted."""

    heads, batch = _synthetic_forward()
    monkeypatch.setattr(
        trainer, "arm_loss", lambda _heads, _batch: torch.tensor(99.0)
    )

    with pytest.raises(analysis.DevFitAnalysisError, match="composite loss"):
        analysis.post_fit_loss_terms(heads, batch)


def test_the_accepted_arm_count_follows_the_contract_plan():
    """Cardinality is derived from `matched_fit_plan()`, not typed as a literal."""

    document = _result()
    assert document["fits_run"] == len(matched_fit_plan())
    assert len(document["arms"]) == len(matched_fit_plan())

    short = _result()
    short["arms"] = short["arms"][:-1]
    short["fits_run"] = len(short["arms"])
    short["final_losses"] = short["final_losses"][:-1]
    with pytest.raises(analysis.DevFitAnalysisError, match="one completed fit per planned arm"):
        analysis.validate_fit_result(short)

    padded = _result()
    padded["arms"] = padded["arms"] + [copy.deepcopy(padded["arms"][0])]
    with pytest.raises(
        analysis.DevFitAnalysisError, match="one arm record for every arm the plan declares"
    ):
        analysis.validate_fit_result(padded)


def test_evaluate_arm_refuses_a_checkpoint_that_is_absent_or_moved(tmp_path):
    """The digest guard runs before any weight is loaded, and it is reachable."""

    arm = {
        "checkpoint_name": "dev_fit_C1_seed0.pt",
        "checkpoint_sha256": "0" * 64,
        "suite": "C1",
        "training_seed": 0,
        "final_loss": 0.0,
    }

    with pytest.raises(analysis.DevFitAnalysisError, match="does not exist"):
        analysis.evaluate_arm(arm, [], tmp_path)

    (tmp_path / arm["checkpoint_name"]).write_bytes(b"not the fitted weights")
    with pytest.raises(analysis.DevFitAnalysisError, match="does not match its recorded digest"):
        analysis.evaluate_arm(arm, [], tmp_path)


def test_load_authorized_examples_guards_census_and_arm_size_without_real_data(
    tmp_path, monkeypatch
):
    """The real-data ingress guards are reachable through their production seams."""

    (tmp_path / "manifest.csv").write_text("fixture\n", encoding="utf-8", newline="\n")
    rows = [SimpleNamespace(suite="C1"), SimpleNamespace(suite="S")]
    census = SimpleNamespace(disclosure=lambda: "synthetic loader fixture")
    counts = {"C1": 152, "S": 152}
    trajectory = {"value": analysis.EXPECTED_TRAJECTORY_CENSUS}

    monkeypatch.setattr(trainer, "file_sha256", lambda _path: "0" * 64)
    monkeypatch.setattr(trainer, "require_authorized_dataset", lambda *_args, **_kwargs: None)
    monkeypatch.setattr(trainer, "select_dev_rows", lambda _manifest: (rows, census))
    monkeypatch.setattr(trainer, "authorized_window_schedule", lambda: ({}, "1" * 64))
    monkeypatch.setattr(
        trainer, "build_role_loaders", lambda _root: ({"C1": object(), "S": object()}, object())
    )
    monkeypatch.setattr(
        trainer, "require_matched_trajectory_census", lambda *_args: trajectory["value"]
    )
    monkeypatch.setattr(trainer, "WindowFeatureExtractor", lambda **_kwargs: object())
    monkeypatch.setattr(
        trainer,
        "load_arm_examples",
        lambda *_args, suite, **_kwargs: [SimpleNamespace()] * counts[suite],
    )

    examples, loaded_census = analysis.load_authorized_examples(tmp_path)
    assert {suite: len(items) for suite, items in examples.items()} == {"C1": 152, "S": 152}
    assert loaded_census["trajectory_census"] == analysis.EXPECTED_TRAJECTORY_CENSUS

    counts["S"] = 151
    with pytest.raises(analysis.DevFitAnalysisError, match="exactly 152"):
        analysis.load_authorized_examples(tmp_path)

    counts["S"] = 152
    trajectory["value"] = {}
    with pytest.raises(analysis.DevFitAnalysisError, match="wrong trajectory census"):
        analysis.load_authorized_examples(tmp_path)


def test_derive_analysis_census_baselines_and_pairing_are_dataset_independent(
    monkeypatch
):
    """The derivation arithmetic is driven without the 3.86 GB delivered dataset."""

    _patch_derive_inputs(monkeypatch, _derived_examples())

    report = analysis.derive_analysis(
        data_root=Path("unused-data-root"),
        fit_result_path=RESULT_PATH,
        checkpoint_dir=Path("unused-checkpoint-dir"),
    )

    assert report["data_census"]["class_counts_by_suite"] == {
        "C1": {"healthy": 1, "structure": 1, "actuator": 1, "sensor": 1},
        "S": {"healthy": 1, "structure": 1, "actuator": 1, "sensor": 1},
    }
    assert report["baselines"] == {
        "empirical_prior_cross_entropy": pytest.approx(math.log(4)),
        "majority_class_accuracy": 0.25,
        "majority_class": "healthy",
    }
    assert report["paired_macro_f1"]["mean_S_minus_C1"] == pytest.approx(0.02)
    assert report["paired_macro_f1"]["sample_sd_S_minus_C1"] == pytest.approx(0.0)


@pytest.mark.parametrize(
    ("examples", "match"),
    [
        (_derived_examples(mismatched_s=True), "same class census"),
        (_derived_examples(ood_s=True), "unexpectedly carries OOD rows"),
    ],
)
def test_derive_analysis_refuses_bad_loaded_census_without_real_data(
    monkeypatch, examples, match
):
    """Matched-class and OOD guards are executable, not real-data-only assertions."""

    _patch_derive_inputs(monkeypatch, examples)

    with pytest.raises(analysis.DevFitAnalysisError, match=match):
        analysis.derive_analysis(
            data_root=Path("unused-data-root"),
            fit_result_path=RESULT_PATH,
            checkpoint_dir=Path("unused-checkpoint-dir"),
        )


def test_derive_analysis_refuses_a_fit_not_bound_to_the_current_trainer(
    monkeypatch,
):
    """The historical fit cannot be read through a different training producer."""

    monkeypatch.setattr(trainer, "training_code_identity", lambda: {"wrong.py": "0" * 64})

    with pytest.raises(analysis.DevFitAnalysisError, match="current executable training state"):
        analysis.derive_analysis(
            data_root=Path("unused-data-root"),
            fit_result_path=RESULT_PATH,
            checkpoint_dir=Path("unused-checkpoint-dir"),
        )


def test_tracked_analysis_names_the_current_analyzer():
    """The tracked readback must have been produced by the analyzer now in the tree.

    The fit side already has this binding — `derive_analysis` refuses a ledger that does
    not name `trainer.training_code_identity()`. The analysis side did not, so an edit to
    `analyze_dev_fit.py` without a regeneration left a tracked artifact whose recorded
    producer no longer existed, silently. This is that missing half.

    WARNING TO ANYONE RUNNING A MUTATION SWEEP OVER `analyze_dev_fit.py`: this test is a
    byte-identity tripwire, not a behaviour test. It fails for *any* change to that file,
    so it reports every mutation as caught and drives the survivor count to zero. Deselect
    it — and confirm the deselection took effect, because `pytest --deselect` ignores a
    node id that matches nothing, without warning or error. Two sweeps in Session 85
    reported perfect coverage for exactly these two reasons before the numbers were
    believed.
    """

    report = _analysis()

    assert report["inputs"]["analysis_code_identity"] == analysis.analysis_code_identity()
    assert report["inputs"]["fit_code_identity"] == trainer.training_code_identity()
    assert report["inputs"]["fit_code_identity"] == _result()["code_identity"]


def test_tracked_analysis_arithmetic_is_reproducible_from_its_own_fields():
    """Every aggregate the artifact publishes is rebuilt from its own per-arm records."""

    report = _analysis()
    arms = report["arms"]
    assert len(arms) == len(matched_fit_plan())

    for arm in arms:
        terms = arm["post_fit_full_batch_loss_terms"]
        assert terms["total"] == pytest.approx(
            terms["class_cross_entropy"]
            + terms["location_cross_entropy"]
            + terms["severity_gaussian_nll"]
            + terms["ood_binary_cross_entropy"],
            abs=1e-11,
        )

    for suite in ("C1", "S"):
        subset = [arm for arm in arms if arm["suite"] == suite]
        summary = report["suite_summary"][suite]
        assert summary["n_arms"] == len(subset)
        assert summary["mean_macro_f1"] == pytest.approx(
            sum(arm["classification"]["macro_f1"] for arm in subset) / len(subset), abs=1e-11
        )
        assert summary["mean_accuracy"] == pytest.approx(
            sum(arm["classification"]["accuracy"] for arm in subset) / len(subset), abs=1e-11
        )

    paired = report["paired_macro_f1"]["by_seed"]
    assert [row["seed"] for row in paired] == list(PREDECLARED_TRAINING_SEEDS)
    differences = []
    for row in paired:
        c1 = next(a for a in arms if a["suite"] == "C1" and a["seed"] == row["seed"])
        structural = next(a for a in arms if a["suite"] == "S" and a["seed"] == row["seed"])
        expected = structural["classification"]["macro_f1"] - c1["classification"]["macro_f1"]
        assert row["S_minus_C1_macro_f1"] == pytest.approx(expected, abs=1e-11)
        differences.append(row["S_minus_C1_macro_f1"])

    assert report["paired_macro_f1"]["mean_S_minus_C1"] == pytest.approx(
        analysis.arithmetic_mean(differences), abs=1e-11
    )
    assert report["paired_macro_f1"]["sample_sd_S_minus_C1"] == pytest.approx(
        analysis.sample_standard_deviation(differences), abs=1e-11
    )

    census = report["data_census"]["class_counts_by_suite"]["C1"]
    total = sum(census.values())
    proportions = [count / total for count in census.values()]
    assert report["baselines"]["majority_class_accuracy"] == pytest.approx(
        max(proportions), abs=1e-11
    )
    assert report["baselines"]["empirical_prior_cross_entropy"] == pytest.approx(
        -sum(p * math.log(p) for p in proportions if p > 0), abs=1e-11
    )
    assert report["data_census"]["ood_counts_by_suite"] == {"C1": 0, "S": 0}
    assert report["fits_run"] == 0 and report["rollouts_spent"] == 0


def test_rounding_bounds_the_decimal_tail_and_does_not_stabilise_float32():
    """`rounded` is documented as a tail trim, and the docstring's measurement is pinned.

    Every float the artifact carries round-trips through `round(x, 12)` to the identical
    float32, which is why the docstring refuses to call this a hardware-stability
    mechanism. If that ever stops being true the claim in the docstring changes with it.
    """

    values = []

    def walk(node):
        if isinstance(node, float):
            values.append(node)
        elif isinstance(node, list):
            for item in node:
                walk(item)
        elif isinstance(node, dict):
            for item in node.values():
                walk(item)

    walk(_analysis())
    assert values

    for value in values:
        assert analysis.rounded(value) == round(value, 12)
        assert torch.tensor(round(value, 12), dtype=torch.float32) == torch.tensor(
            value, dtype=torch.float32
        )

    assert analysis.rounded({"a": [1.0 / 3.0]}) == {"a": [round(1.0 / 3.0, 12)]}
    with pytest.raises(analysis.DevFitAnalysisError, match="non-finite float"):
        analysis.rounded(float("inf"))
