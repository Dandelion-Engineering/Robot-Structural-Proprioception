"""Tests for the development-only trainer (`utils.dev_fit_trainer`).

The discipline this file is built around is Session 65's: the exit paths of a program are
the region no unit test enters, and this project has been bitten there four times. So
every terminal exit of `main()` below is **driven through `main(argv)` and the artifact it
wrote is read back and asserted on** — not asserted from the return code alone, which is
the check that passes while the document is empty, malformed, or missing.

The second discipline is Session 81's Finding G: `DevFitProvenance` accepts any non-empty
string in `row_disclosure`, so the trainer's promise that it passes the census sentence
and nothing else is a promise only a test can keep.
"""

from __future__ import annotations

import json
import sys
from pathlib import Path

import numpy as np
import pytest

SCRIPTS_DIR = Path(__file__).resolve().parents[1] / "scripts"
sys.path.insert(0, str(SCRIPTS_DIR))

from utils.dev_fit_contract import (  # noqa: E402
    ASSIGNMENT_CANONICAL_SHA256,
    DEVELOPMENT_ONLY_AUTHORITY,
    DevFitContractError,
    DevRowCensus,
    matched_fit_plan,
)
from utils.dev_fit_trainer import (  # noqa: E402
    EXIT_CODES,
    X_CONTRACT_REFUSED,
    X_DATA_MISSING,
    X_FIT_OK,
    X_PLAN_INCOMPLETE,
    X_PLAN_OK,
    DevFitDataError,
    build_provenance,
    load_arm_examples,
    main,
    training_code_identity,
    window_record,
)
from utils.estimator import SOURCE_CLASS_ORDER, WindowFeatureExtractor  # noqa: E402
from utils.schema_types import (  # noqa: E402
    CHANNEL_NAMES,
    CHANNEL_WIDTH,
    SUITE_CHANNELS,
    ObservedRecord,
)
from utils.storage_contract import IdentityManifestRow, write_identity_manifest  # noqa: E402

CONFIG_HASH = "dev-" + "a" * 64
WINDOW = 16
STEPS = 24
ORIGIN = 4


def _record(run_id: str, suite: str, t: int = STEPS, *, seed: int = 0) -> ObservedRecord:
    """A fully-valid `t`-step observed record, absent channels NaN and masked off."""

    rng = np.random.default_rng(seed)
    times = np.arange(t, dtype=float) * 0.002
    values, valid, meas, avail, lat = {}, {}, {}, {}, {}
    for name in CHANNEL_NAMES:
        width = CHANNEL_WIDTH[name]
        if name in SUITE_CHANNELS[suite]:
            values[name] = rng.normal(size=(t, width))
            valid[name] = np.ones((t, width), dtype=bool)
        else:
            values[name] = np.full((t, width), np.nan)
            valid[name] = np.zeros((t, width), dtype=bool)
        meas[name] = times.copy()
        avail[name] = times.copy()
        lat[name] = np.zeros(t, dtype=float)
    return ObservedRecord(
        suite=suite,
        run_id=run_id,
        pair_id="basepair_dev_t01_f000_r00_dataset0",
        config_hash=CONFIG_HASH,
        values=values,
        valid_mask=valid,
        measurement_time_s=meas,
        availability_time_s=avail,
        latency_age_s=lat,
        suite_available_mask={n: n in SUITE_CHANNELS[suite] for n in CHANNEL_NAMES},
        split="dev",
    )


def _manifest_row(split: str, suite: str, index: int) -> IdentityManifestRow:
    """One schema-A identity row whose run_id carries its suite, as delivered rows do."""

    return IdentityManifestRow(
        schema_version="1.0",
        config_hash=CONFIG_HASH,
        scenario_spec_id=f"scenario_{split}_t01_f000_r{index:02d}",
        pair_id=f"basepair_{split}_t01_f000_r{index:02d}_dataset0",
        run_id=f"scenario_{split}_t01_f000_r{index:02d}_{suite}_dataset0",
        trajectory_spec_id=f"trajectory_{split}_diagnostic_b",
        fault_setting_id=f"fault_{split}_healthy",
        split_group_id=f"group_{split}_{index}",
        split=split,
        suite=suite,
        estimator_id="estimator_none",
        controller_id="controller_task",
        payload_id=f"payload_{split}_0",
        env_profile_id=f"env_{split}_iso25c",
        contact_profile_id=f"contact_{split}_none",
        sim_seed=110000 + index * 10,
        fault_seed=110001 + index * 10,
        sensor_seed=110002 + index * 10,
        controller_seed=110003 + index * 10,
        train_seed=110004 + index * 10,
    )


def _label_payload(source_class: str = "healthy", *, location: int = -1) -> dict:
    """The eight-key label payload `assignment_generator` writes, as 0-d arrays."""

    return {
        "source_class": np.asarray(source_class),
        "subtype": np.asarray("none"),
        "location": np.asarray(location, dtype=np.int64),
        "severity": np.asarray(0.5, dtype=np.float64),
        "onset_index": np.asarray(5, dtype=np.int64),
        "onset_time_s": np.asarray(0.01, dtype=np.float64),
        "compound_flag": np.asarray(False, dtype=np.bool_),
        "ood_flag": np.asarray(False, dtype=np.bool_),
    }


def _dataset(root: Path, *, rows_per_suite: int = 2, splits=("dev",)) -> list:
    """Write a miniature but structurally real dataset root; return its manifest rows."""

    rows = []
    for split in splits:
        for suite in ("C1", "S"):
            for index in range(rows_per_suite):
                rows.append(_manifest_row(split, suite, index))
    write_identity_manifest(root / "manifest.csv", rows)
    (root / "labels").mkdir(parents=True, exist_ok=True)
    for row in rows:
        observations = root / "observations" / row.suite
        observations.mkdir(parents=True, exist_ok=True)
        record = _record(row.run_id, row.suite, seed=row.sim_seed)
        np.savez(observations / f"{row.run_id}.npz", **record.to_npz_dict())
        np.savez(root / "labels" / f"{row.run_id}.npz", **_label_payload())
    return rows


# --------------------------------------------------------------------------- #
# The window seam.
# --------------------------------------------------------------------------- #
def test_window_record_slices_every_per_step_array_and_leaves_the_rest():
    """The slice must move every per-step array, or a channel silently misaligns."""

    record = _record("r", "S", t=STEPS)
    windowed = window_record(record, ORIGIN, WINDOW)
    assert windowed.n_steps == WINDOW
    for channel in CHANNEL_NAMES:
        assert windowed.values[channel].shape[0] == WINDOW
        assert windowed.valid_mask[channel].shape[0] == WINDOW
        assert windowed.measurement_time_s[channel].shape[0] == WINDOW
        np.testing.assert_allclose(
            windowed.values[channel], record.values[channel][ORIGIN : ORIGIN + WINDOW]
        )
    assert windowed.run_id == record.run_id and windowed.suite == record.suite


def test_window_record_refuses_a_window_that_does_not_fit():
    """A short tail zero-padded into a full window is an example that is not data."""

    record = _record("r", "S", t=STEPS)
    with pytest.raises(DevFitDataError, match="does not fit"):
        window_record(record, STEPS - 2, WINDOW)
    with pytest.raises(DevFitDataError, match="non-negative"):
        window_record(record, -1, WINDOW)


# --------------------------------------------------------------------------- #
# The contract wiring.
# --------------------------------------------------------------------------- #
def test_load_arm_examples_refuses_a_withheld_role_at_the_point_of_consumption(tmp_path):
    """Bound 1 is checked where rows are USED, because a caller can build the list."""

    _dataset(tmp_path, splits=("dev", "val"))
    val_rows = [_manifest_row("val", "S", 0)]
    extractor = WindowFeatureExtractor(window_steps=WINDOW)
    with pytest.raises(DevFitContractError, match="may read no withheld role"):
        load_arm_examples(tmp_path, val_rows, suite="S", origin=ORIGIN, extractor=extractor)


def test_load_arm_examples_refuses_a_row_from_the_other_matched_suite(tmp_path):
    """A nominal C1 arm may not consume S rows while every row still says `dev`."""

    _dataset(tmp_path)
    s_rows = [_manifest_row("dev", "S", 0)]
    extractor = WindowFeatureExtractor(window_steps=WINDOW)
    with pytest.raises(DevFitContractError, match="only rows from suite"):
        load_arm_examples(tmp_path, s_rows, suite="C1", origin=ORIGIN, extractor=extractor)


def test_training_code_identity_names_the_three_files_that_define_the_protocol():
    """Bound 4: a checkpoint names the code that produced it, built by `code_identity`."""

    identity = training_code_identity()
    assert set(identity) == {
        "dev_fit_trainer.py",
        "dev_fit_contract.py",
        "attribution_net.py",
    }
    for label, digest in identity.items():
        assert len(digest) == 64 and digest == digest.lower(), label


def test_build_provenance_passes_the_census_sentence_and_nothing_else(tmp_path):
    """Session 81 Finding G: `row_disclosure` accepts any string, so pin what we pass."""

    census = DevRowCensus(
        total_rows=4,
        rows_by_split={"dev": 4},
        rows_by_suite={"C1": 2, "S": 2},
        selected_rows=4,
        withheld_rows=0,
    )
    provenance = build_provenance(
        data_root=tmp_path,
        manifest_sha256="b" * 64,
        config_hash=CONFIG_HASH,
        assignment_sha256=ASSIGNMENT_CANONICAL_SHA256,
        suite="C1",
        seed=0,
        checkpoint_sha256="c" * 64,
        census=census,
    )
    assert provenance.row_disclosure == census.disclosure()
    assert provenance.data_root_name == tmp_path.resolve().name
    assert provenance.authority == DEVELOPMENT_ONLY_AUTHORITY
    # The field the record does not constrain must still carry no separator here.
    assert "/" not in provenance.row_disclosure
    assert "\\" not in provenance.row_disclosure


# --------------------------------------------------------------------------- #
# Every terminal exit, driven, with its artifact read back.
# --------------------------------------------------------------------------- #
def test_plan_exit_writes_the_ten_arms_and_runs_nothing(tmp_path):
    """X_PLAN_OK: the plan is a value the trainer iterates, not a loop it writes."""

    code = main(
        ["--mode", "plan", "--output-dir", str(tmp_path), "--window-origin-step", str(ORIGIN)]
    )
    assert code == EXIT_CODES[X_PLAN_OK]
    document = json.loads((tmp_path / "dev_fit_plan.json").read_text(encoding="utf-8"))
    assert document["exit"] == X_PLAN_OK
    assert document["authority"] == DEVELOPMENT_ONLY_AUTHORITY
    assert document["fits_run"] == 0 and document["rollouts_spent"] == 0
    assert document["n_arms"] == len(matched_fit_plan()) == 10
    assert [(arm["suite"], arm["seed"]) for arm in document["arms"]] == list(matched_fit_plan())


def test_fit_without_the_required_inputs_takes_the_data_missing_exit(tmp_path):
    """X_DATA_MISSING: the window origin has no default, so its absence is an exit."""

    code = main(["--mode", "fit", "--output-dir", str(tmp_path)])
    assert code == EXIT_CODES[X_DATA_MISSING]
    document = json.loads((tmp_path / "dev_fit_result.json").read_text(encoding="utf-8"))
    assert document["exit"] == X_DATA_MISSING
    assert document["fits_run"] == 0


def test_a_manifest_with_no_dev_row_takes_the_contract_refused_exit(tmp_path):
    """X_CONTRACT_REFUSED: a fit over zero rows is a defect, not an empty result."""

    root = tmp_path / "data"
    root.mkdir()
    _dataset(root, splits=("val",))
    output = tmp_path / "out"
    code = main(
        [
            "--mode", "fit",
            "--output-dir", str(output),
            "--data-root", str(root),
            "--window-origin-step", str(ORIGIN),
            "--window-steps", str(WINDOW),
        ]
    )
    assert code == EXIT_CODES[X_CONTRACT_REFUSED]
    document = json.loads((output / "dev_fit_result.json").read_text(encoding="utf-8"))
    assert document["exit"] == X_CONTRACT_REFUSED
    assert document["reason_class"] == "DevFitContractError"
    assert document["fits_run"] == 0


def test_the_refusal_message_itself_is_never_persisted(tmp_path):
    """The artifact records the exception CLASS; the message goes to stdout only.

    A refusal can quote a caller-supplied string, and requirement (z) forbids a result
    artifact from recording an absolute path. This trainer does not scrub — the accept
    side of a scrubber is where damage is invisible — it simply never writes the message.
    """

    root = tmp_path / "data"
    root.mkdir()
    _dataset(root, splits=("val",))
    output = tmp_path / "out"
    main(
        [
            "--mode", "fit",
            "--output-dir", str(output),
            "--data-root", str(root),
            "--window-origin-step", str(ORIGIN),
            "--window-steps", str(WINDOW),
        ]
    )
    text = (output / "dev_fit_result.json").read_text(encoding="utf-8")
    assert "reason_class" in text
    for leaked in ("manifest rows selected", "no dev row of suites", str(root)):
        assert leaked not in text, f"the artifact persisted {leaked!r}"


def test_a_missing_observation_payload_takes_the_data_missing_exit(tmp_path):
    """X_DATA_MISSING from inside the arm loop, with the arms completed so far recorded."""

    root = tmp_path / "data"
    root.mkdir()
    rows = _dataset(root)
    (root / "observations" / "C1" / f"{rows[0].run_id}.npz").unlink()
    output = tmp_path / "out"
    code = main(
        [
            "--mode", "fit",
            "--output-dir", str(output),
            "--data-root", str(root),
            "--window-origin-step", str(ORIGIN),
            "--window-steps", str(WINDOW),
            "--epochs", "1",
        ]
    )
    assert code == EXIT_CODES[X_DATA_MISSING]
    document = json.loads((output / "dev_fit_result.json").read_text(encoding="utf-8"))
    assert document["exit"] == X_DATA_MISSING
    assert document["reason_class"] == "DevFitDataError"
    assert document["fits_run"] == 0


def test_a_complete_fit_writes_one_validated_provenance_record_per_arm(tmp_path):
    """X_FIT_OK: ten arms, ten provenance records on disk, zero rollouts.

    This asserts what the exit WROTE, not that the model learned anything. Whether the
    loss falls on real dev rows is the measurement this trainer exists to make, and it is
    not authorized to run until this executable's own review closes.
    """

    root = tmp_path / "data"
    root.mkdir()
    _dataset(root)
    output = tmp_path / "out"
    code = main(
        [
            "--mode", "fit",
            "--output-dir", str(output),
            "--data-root", str(root),
            "--window-origin-step", str(ORIGIN),
            "--window-steps", str(WINDOW),
            "--epochs", "2",
            "--batch-size", "2",
        ]
    )
    assert code == EXIT_CODES[X_FIT_OK]
    document = json.loads((output / "dev_fit_result.json").read_text(encoding="utf-8"))
    assert document["exit"] == X_FIT_OK
    assert document["fits_run"] == 10
    assert document["rollouts_spent"] == 0
    assert document["window_origin_step"] == ORIGIN

    recorded = [(arm["suite"], arm["training_seed"]) for arm in document["arms"]]
    assert recorded == list(matched_fit_plan())
    for arm in document["arms"]:
        assert arm["authority"] == DEVELOPMENT_ONLY_AUTHORITY
        assert arm["assignment_sha256"] == ASSIGNMENT_CANONICAL_SHA256
        assert arm["config_hash"].startswith("dev-")
        assert len(arm["checkpoint_sha256"]) == 64
        assert set(arm["code_identity"]) == set(training_code_identity())
        assert arm["data_root_name"] == "data"
    for suite, seed in matched_fit_plan():
        assert (output / f"dev_fit_{suite}_seed{seed}.pt").is_file()


def test_an_incomplete_plan_cannot_be_reported_as_a_comparison(tmp_path):
    """X_PLAN_INCOMPLETE: an unbalanced set is a difference between two seed populations.

    Driven by handing `require_complete_matched_plan` the state `main()` would hold if an
    arm had been skipped, because that is the branch the exit exists for.
    """

    from utils.dev_fit_trainer import require_complete_matched_plan

    partial = [arm for arm in matched_fit_plan() if arm[0] == "C1"]
    with pytest.raises(DevFitContractError, match="incomplete"):
        require_complete_matched_plan(partial)
    assert EXIT_CODES[X_PLAN_INCOMPLETE] == 5
    assert X_PLAN_INCOMPLETE in EXIT_CODES


def test_every_named_exit_has_a_distinct_code_and_appears_in_the_table():
    """A named exit that is not in the table is an exit no artifact can report."""

    assert set(EXIT_CODES) == {
        X_PLAN_OK,
        X_FIT_OK,
        X_CONTRACT_REFUSED,
        X_DATA_MISSING,
        X_PLAN_INCOMPLETE,
    }
    failures = {name: code for name, code in EXIT_CODES.items() if code != 0}
    assert len(set(failures.values())) == len(failures), "two failures share an exit code"


def test_the_source_class_order_this_trainer_targets_is_the_projects_order():
    """The class head's index convention is a shared decision, not this file's."""

    assert SOURCE_CLASS_ORDER == ("healthy", "structure", "actuator", "sensor")
