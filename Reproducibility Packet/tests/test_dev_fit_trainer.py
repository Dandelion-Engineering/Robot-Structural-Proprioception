"""Tests for the development-only trainer (`utils.dev_fit_trainer`).

The discipline this file is built around is Session 65's: the exit paths of a program are
the region no unit test enters, and this project has been bitten there four times. So
every terminal exit of `main()` below is **driven through `main(argv)` and the artifact it
wrote is read back and asserted on** — not asserted from the return code alone, which is
the check that passes while the document is empty, malformed, or missing.

The second discipline is Session 81's Finding G: `DevFitProvenance` accepts any non-empty
string in `row_disclosure`, so the trainer's promise that it passes the census sentence
and nothing else is a promise only a test can keep.

The third is Session 82's: the development training-window policy is a *scientific*
commitment, so the tests that pin it are run against the **real approved assignment
document**, not against a fixture. A fixture schedule can only show that the mechanics
work; only the real document can show that the dev diagnostic window this policy derives
is the one Protocol P already pre-registered.
"""

from __future__ import annotations

import dataclasses
import json
import sys
from pathlib import Path

import numpy as np
import pytest
import torch

SCRIPTS_DIR = Path(__file__).resolve().parents[1] / "scripts"
sys.path.insert(0, str(SCRIPTS_DIR))

from utils.dev_fit_contract import (  # noqa: E402
    ASSIGNMENT_CANONICAL_SHA256,
    DEVELOPMENT_ONLY_AUTHORITY,
    DevFitContractError,
    DevRowCensus,
    matched_fit_plan,
)
import utils.dev_fit_trainer as trainer  # noqa: E402
from utils.dev_fit_trainer import (  # noqa: E402
    EXIT_CODES,
    X_CONTRACT_REFUSED,
    X_DATA_MISSING,
    X_FIT_OK,
    X_OUTPUT_DIRTY,
    X_PLAN_INCOMPLETE,
    X_PLAN_OK,
    DevFitDataError,
    TrainingExample,
    TrainingProtocol,
    WindowSchedule,
    authorized_window_schedule,
    build_provenance,
    development_window_schedule,
    load_arm_examples,
    main,
    require_matched_trajectory_census,
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
from utils.storage_contract import (  # noqa: E402
    IdentityManifestRow,
    file_sha256,
    write_identity_manifest,
)

CONFIG_HASH = "dev-" + "a" * 64
WINDOW = 16
STEPS = 24

# The fixture schedule: two trajectories with DIFFERENT origins, which is the whole point
# the real policy exists to serve. Both windows fit inside `STEPS` and both open after
# their own onset.
ORDINARY = "trajectory_dev_ordinary_a"
DIAGNOSTIC = "trajectory_dev_diagnostic_b"
FIXTURE_LEAD = 4
FIXTURE_ONSET = {ORDINARY: 2, DIAGNOSTIC: 4}


def _fixture_schedule() -> dict[str, WindowSchedule]:
    """Return the small two-trajectory schedule the synthetic exits are driven with."""

    return {
        name: WindowSchedule(
            trajectory_spec_id=name,
            onset_step=onset,
            lead_steps=FIXTURE_LEAD,
            origin_step=onset + FIXTURE_LEAD,
            window_steps=WINDOW,
            decision_step=onset + FIXTURE_LEAD + WINDOW,
            run_steps=STEPS,
            has_diagnostic_probe=name == DIAGNOSTIC,
        ).validate()
        for name, onset in FIXTURE_ONSET.items()
    }


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


def _manifest_row(
    split: str, suite: str, index: int, *, trajectory: str = "diagnostic_b"
) -> IdentityManifestRow:
    """One schema-A identity row whose run_id carries its suite, as delivered rows do."""

    tag = "t00" if trajectory.startswith("ordinary") else "t01"
    scenario = f"scenario_{split}_{tag}_f000_r{index:02d}"
    return IdentityManifestRow(
        schema_version="1.0",
        config_hash=CONFIG_HASH,
        scenario_spec_id=scenario,
        pair_id=f"basepair_{split}_{tag}_f000_r{index:02d}_dataset0",
        run_id=f"{scenario}_{suite}_dataset0",
        trajectory_spec_id=f"trajectory_{split}_{trajectory}",
        fault_setting_id=f"fault_{split}_healthy",
        split_group_id=f"group_{split}_{tag}_{index}",
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


def _label_payload(
    source_class: str = "healthy",
    *,
    location: int = -1,
    onset_index: int = 5,
) -> dict:
    """The eight-key label payload `assignment_generator` writes, as 0-d arrays."""

    return {
        "source_class": np.asarray(source_class),
        "subtype": np.asarray("none"),
        "location": np.asarray(location, dtype=np.int64),
        "severity": np.asarray(0.5, dtype=np.float64),
        "onset_index": np.asarray(onset_index, dtype=np.int64),
        "onset_time_s": np.asarray(onset_index * 0.002, dtype=np.float64),
        "compound_flag": np.asarray(False, dtype=np.bool_),
        "ood_flag": np.asarray(False, dtype=np.bool_),
    }


def _dataset(
    root: Path,
    *,
    rows_per_suite: int = 1,
    splits=("dev",),
    trajectories=("ordinary_a", "diagnostic_b"),
    steps: dict[str, int] | None = None,
) -> list:
    """Write a miniature but structurally real dataset root; return its manifest rows."""

    rows = []
    for split in splits:
        for trajectory in trajectories:
            for suite in ("C1", "S"):
                for index in range(rows_per_suite):
                    rows.append(
                        _manifest_row(split, suite, index, trajectory=trajectory)
                    )
    write_identity_manifest(root / "manifest.csv", rows)
    (root / "labels").mkdir(parents=True, exist_ok=True)
    for row in rows:
        observations = root / "observations" / row.suite
        observations.mkdir(parents=True, exist_ok=True)
        n_steps = (steps or {}).get(row.run_id, STEPS)
        record = _record(row.run_id, row.suite, t=n_steps, seed=row.sim_seed)
        np.savez(observations / f"{row.run_id}.npz", **record.to_npz_dict())
        np.savez(
            root / "labels" / f"{row.run_id}.npz",
            **_label_payload(
                onset_index=(
                    FIXTURE_ONSET[ORDINARY]
                    if row.trajectory_spec_id.endswith("ordinary_a")
                    else FIXTURE_ONSET[DIAGNOSTIC]
                )
            ),
        )
    return rows


class _FixtureObservationLoader:
    """Minimal synthetic loader; production wiring is tested by the packet loaders."""

    def __init__(self, root: Path, suite: str) -> None:
        self.root = root
        self.suite = suite

    def load(self, run_id: str) -> ObservedRecord:
        return ObservedRecord.load_npz(
            self.root / "observations" / self.suite / f"{run_id}.npz"
        )


class _FixtureLabelLoader:
    """Minimal synthetic label loader matching RolePayloadLoader's return shape."""

    def __init__(self, root: Path) -> None:
        self.root = root

    def load(self, run_id: str) -> dict[str, np.ndarray]:
        with np.load(self.root / "labels" / f"{run_id}.npz", allow_pickle=False) as payload:
            return {name: np.asarray(payload[name]) for name in payload.files}


def _fixture_role_loaders(root: Path):
    """Return suite-scoped synthetic loaders for a temporary fixture root."""

    return (
        {suite: _FixtureObservationLoader(root, suite) for suite in ("C1", "S")},
        _FixtureLabelLoader(root),
    )


def _authorize_fixture_window(monkeypatch, schedule=None) -> None:
    """Substitute the small fixture schedule for the assignment-derived real one."""

    entries = _fixture_schedule() if schedule is None else schedule
    monkeypatch.setattr(trainer, "DEVELOPMENT_WINDOW_STEPS", WINDOW)
    monkeypatch.setattr(
        trainer,
        "authorized_window_schedule",
        lambda **_: (entries, ASSIGNMENT_CANONICAL_SHA256),
    )


def _authorize_fixture_dataset(monkeypatch, root: Path, schedule=None) -> None:
    """Bind one synthetic root to the executable's otherwise exact data/window pins."""

    monkeypatch.setattr(trainer, "AUTHORIZED_DATA_ROOT_NAME", root.resolve().name)
    monkeypatch.setattr(
        trainer, "AUTHORIZED_MANIFEST_SHA256", file_sha256(root / "manifest.csv")
    )
    monkeypatch.setattr(trainer, "AUTHORIZED_CONFIG_HASH", CONFIG_HASH)
    monkeypatch.setattr(
        trainer,
        "AUTHORIZED_ROLE_INDEX_SHA256",
        {
            "labels/index.csv": "d" * 64,
            "observations/C1/index.csv": "e" * 64,
            "observations/S/index.csv": "f" * 64,
        },
    )
    _authorize_fixture_window(monkeypatch, schedule)
    monkeypatch.setattr(
        trainer, "build_role_loaders", lambda data_root: _fixture_role_loaders(data_root)
    )


# --------------------------------------------------------------------------- #
# The training-window policy, against the REAL approved assignment.
# --------------------------------------------------------------------------- #
def test_the_derived_dev_schedule_reproduces_protocol_ps_diagnostic_window():
    """The policy's load-bearing claim: it does not invent a second window origin.

    Protocol P v2.3.3 prospectively fixed the diagnostic window at ``[1000, 1768)``. If
    the derivation ever stops landing there, the trainer and the pre-registration are
    describing different slices of the same run and the policy's justification is void.
    """

    schedule, digest = authorized_window_schedule()
    assert digest == ASSIGNMENT_CANONICAL_SHA256
    assert set(schedule) == {ORDINARY, DIAGNOSTIC}

    diagnostic = schedule[DIAGNOSTIC]
    assert (diagnostic.origin_step, diagnostic.decision_step) == (1000, 1768)
    assert diagnostic.onset_step == 500 and diagnostic.lead_steps == 500
    assert diagnostic.has_diagnostic_probe is True

    ordinary = schedule[ORDINARY]
    assert (ordinary.origin_step, ordinary.decision_step) == (900, 1668)
    assert ordinary.onset_step == 400 and ordinary.lead_steps == 500
    assert ordinary.has_diagnostic_probe is False

    # Both trajectories open at the same elapsed time after onset; that equality IS the
    # policy's reason for giving the probe-free trajectory the diagnostic one's lead.
    assert ordinary.lead_steps == diagnostic.lead_steps
    for entry in schedule.values():
        assert entry.window_steps == 768
        assert entry.origin_step > entry.onset_step  # entirely post-onset
        assert entry.decision_step <= entry.run_steps
        assert entry.as_document()["windows_per_run"] == 1


def test_the_schedule_refuses_an_assignment_file_that_is_not_the_approved_one(
    monkeypatch,
):
    """The digest a checkpoint records must gate the read, not merely describe it.

    Driven by moving the expected digest rather than the file: the refusal is what is
    under test, and rewriting the packet's approved assignment to test it would be a
    worse instrument than changing what the check compares against.
    """

    monkeypatch.setattr(trainer, "ASSIGNMENT_CANONICAL_SHA256", "0" * 64)
    with pytest.raises(DevFitContractError, match="not the approved assignment"):
        authorized_window_schedule()


def test_every_split_of_the_approved_assignment_admits_the_same_policy():
    """Gate 7 has to reuse this rule, so it must be total over the reserved design."""

    document = json.loads(
        (SCRIPTS_DIR.parent / "config" / trainer.ASSIGNMENT_DOCUMENT_NAME).read_text(
            encoding="utf-8"
        )
    )
    for split in ("dev", "pilot", "val", "test"):
        schedule = development_window_schedule(document, split=split)
        assert len(schedule) == 2, split
        assert len({entry.lead_steps for entry in schedule.values()}) == 1, split
        assert sum(e.has_diagnostic_probe for e in schedule.values()) == 1, split
        for entry in schedule.values():
            entry.validate()


def test_a_split_without_exactly_one_diagnostic_trajectory_is_refused():
    """With no probe there is no anchor; with two there is no single answer."""

    def _document(n_probes: int) -> dict:
        specs = []
        for index in range(2):
            specs.append(
                {
                    "id": f"trajectory_x_{index}",
                    "split": "x",
                    "onset_time_s": 0.8,
                    "duration_s": 5.8,
                    "diagnostic_probe": (
                        {"start_offset_s": 1.0} if index < n_probes else None
                    ),
                }
            )
        return {"trajectory_specs": specs}

    for n_probes in (0, 2):
        with pytest.raises(DevFitContractError, match="exactly one diagnostic"):
            development_window_schedule(_document(n_probes), split="x", window_steps=8)
    # The one-probe case is the control: the same construction must succeed.
    assert len(development_window_schedule(_document(1), split="x", window_steps=8)) == 2


@pytest.mark.parametrize(
    ("document", "kwargs", "message"),
    [
        ({"trajectory_specs": []}, {"window_steps": True}, "positive integer"),
        (
            {
                "trajectory_specs": [
                    {
                        "id": "t",
                        "split": "x",
                        "onset_time_s": 0.8,
                        "duration_s": 5.8,
                        "diagnostic_probe": {},
                    }
                ]
            },
            {"window_steps": 8},
            "finite non-negative",
        ),
        (
            {
                "trajectory_specs": [
                    {
                        "id": "t",
                        "split": "x",
                        "onset_time_s": 0.8,
                        "duration_s": 5.8,
                        "diagnostic_probe": {"start_offset_s": 1.0},
                    }
                ]
            },
            {"window_steps": 8, "control_dt_s": 0.0},
            "development control_dt_s",
        ),
        # Session 83. A zero period alone does not pin the rule: the sweep showed
        # `== DEVELOPMENT_CONTROL_DT_S` could be weakened to `!= 0.0` with the suite
        # green, because 0.0 was the only wrong period any case supplied. A period that
        # is positive, finite and simply NOT the development one is the state that
        # separates the two rules, and it silently halves every derived step count.
        (
            {
                "trajectory_specs": [
                    {
                        "id": "t",
                        "split": "x",
                        "onset_time_s": 0.8,
                        "duration_s": 5.8,
                        "diagnostic_probe": {"start_offset_s": 1.0},
                    }
                ]
            },
            {"window_steps": 8, "control_dt_s": 0.004},
            "development control_dt_s",
        ),
        # Session 83. `diagnostic_probe` is read as "an object or null"; a list reaches
        # `probes[0].get(...)` and raises `AttributeError` without the shape guard.
        (
            {
                "trajectory_specs": [
                    {
                        "id": "t",
                        "split": "x",
                        "onset_time_s": 0.8,
                        "duration_s": 5.8,
                        "diagnostic_probe": [{"start_offset_s": 1.0}],
                    }
                ]
            },
            {"window_steps": 8},
            "diagnostic_probe must be an object or null",
        ),
        # Session 83. The assignment itself must be a mapping before anything is read.
        ([], {"window_steps": 8}, "assignment document must be a mapping"),
    ],
)
def test_malformed_schedule_controls_take_the_named_contract_refusal(
    document, kwargs, message
):
    """Scientific controls reject bools/missing values without foreign exceptions."""

    with pytest.raises(DevFitContractError, match=message):
        development_window_schedule(document, split="x", **kwargs)


def test_the_schedules_probe_flag_must_be_a_bool_not_merely_truthy():
    """`has_diagnostic_probe` is recorded in the plan, so its type is part of the record.

    Session 83: the reviewer added this guard and no test constructed a schedule that
    could fail it, so it could be deleted with the focused suite green. A truthy payload
    (the probe object itself) is the realistic wrong value — it serializes into the plan
    artifact as an object where a reader expects a boolean.
    """

    fields = dict(
        trajectory_spec_id=DIAGNOSTIC,
        onset_step=4,
        lead_steps=FIXTURE_LEAD,
        origin_step=4 + FIXTURE_LEAD,
        window_steps=WINDOW,
        decision_step=4 + FIXTURE_LEAD + WINDOW,
        run_steps=STEPS,
    )
    for wrong in ({"start_offset_s": 1.0}, 1, None):
        with pytest.raises(DevFitContractError, match="has_diagnostic_probe must be a bool"):
            WindowSchedule(**fields, has_diagnostic_probe=wrong).validate()
    # The accept side: both booleans must still validate.
    for good in (True, False):
        assert WindowSchedule(**fields, has_diagnostic_probe=good).validate()


def test_an_off_grid_assignment_time_is_refused_rather_than_rounded():
    """A design time that is not on the control grid is a disagreement, not a rounding."""

    document = {
        "trajectory_specs": [
            {
                "id": "trajectory_x_0",
                "split": "x",
                "onset_time_s": 0.8005,
                "duration_s": 5.8,
                "diagnostic_probe": {"start_offset_s": 1.0},
            }
        ]
    }
    with pytest.raises(DevFitContractError, match="not an exact multiple"):
        development_window_schedule(document, split="x", window_steps=8)


def test_a_window_that_leaves_its_run_or_precedes_its_onset_is_refused():
    """The schedule validates itself, so a bad derivation cannot reach a training loop."""

    with pytest.raises(DevFitContractError, match="does not fit"):
        WindowSchedule(
            trajectory_spec_id="t",
            onset_step=2,
            lead_steps=4,
            origin_step=6,
            window_steps=WINDOW,
            decision_step=6 + WINDOW,
            run_steps=WINDOW,
            has_diagnostic_probe=False,
        ).validate()
    with pytest.raises(DevFitContractError, match="onset plus the split's lead"):
        WindowSchedule(
            trajectory_spec_id="t",
            onset_step=2,
            lead_steps=4,
            origin_step=99,
            window_steps=WINDOW,
            decision_step=99 + WINDOW,
            run_steps=STEPS,
            has_diagnostic_probe=False,
        ).validate()


def test_the_protocol_refuses_a_schedule_that_is_not_the_approved_assignments():
    """The recorded assignment digest must be the one the schedule was derived from."""

    real_schedule, _ = authorized_window_schedule()
    protocol = TrainingProtocol(
        schedule=tuple(real_schedule.values()),
        assignment_sha256="0" * 64,
        window_steps=trainer.DEVELOPMENT_WINDOW_STEPS,
        control_dt_s=0.002,
        epochs=1,
        batch_size=1,
        learning_rate=1.0e-3,
        device="cpu",
    )
    with pytest.raises(DevFitContractError, match="approved assignment"):
        protocol.validate()


# --------------------------------------------------------------------------- #
# The window seam.
# --------------------------------------------------------------------------- #
def test_window_record_slices_every_per_step_array_and_leaves_the_rest():
    """The slice must move every per-step array, or a channel silently misaligns."""

    entry = _fixture_schedule()[DIAGNOSTIC]
    record = _record("r", "S", t=STEPS)
    windowed = window_record(
        record, entry.origin_step, WINDOW, decision_time_s=entry.decision_time_s
    )
    assert windowed.n_steps == WINDOW
    start, stop = entry.origin_step, entry.origin_step + WINDOW
    for channel in CHANNEL_NAMES:
        assert windowed.values[channel].shape[0] == WINDOW
        assert windowed.valid_mask[channel].shape[0] == WINDOW
        assert windowed.measurement_time_s[channel].shape[0] == WINDOW
        np.testing.assert_allclose(
            windowed.values[channel], record.values[channel][start:stop]
        )
    assert windowed.run_id == record.run_id and windowed.suite == record.suite


def test_window_record_refuses_a_window_that_does_not_fit():
    """A short tail zero-padded into a full window is an example that is not data."""

    entry = _fixture_schedule()[DIAGNOSTIC]
    record = _record("r", "S", t=STEPS)
    with pytest.raises(DevFitDataError, match="does not fit"):
        window_record(
            record, STEPS - 2, WINDOW, decision_time_s=entry.decision_time_s
        )
    with pytest.raises(DevFitDataError, match="non-negative"):
        window_record(record, -1, WINDOW, decision_time_s=entry.decision_time_s)


def test_window_record_masks_a_sample_delivered_after_the_held_decision():
    """Persisted future delivery must not become training-only look-ahead information."""

    entry = _fixture_schedule()[DIAGNOSTIC]
    record = _record("r", "S", t=STEPS)
    last = entry.decision_step - 1
    record.values["q_obs"][last] = 12345.0
    record.availability_time_s["q_obs"][last] = entry.decision_time_s + 1.0
    windowed = window_record(
        record, entry.origin_step, WINDOW, decision_time_s=entry.decision_time_s
    )
    assert not np.any(windowed.valid_mask["q_obs"][-1])
    assert np.all(np.isnan(windowed.values["q_obs"][-1]))
    # ...and nothing else was eaten: a mask that empties the channel would also "pass".
    assert np.all(windowed.valid_mask["q_obs"][:-1])


# --------------------------------------------------------------------------- #
# The contract wiring.
# --------------------------------------------------------------------------- #
def test_each_row_is_windowed_by_its_own_trajectory_and_contributes_one_example(tmp_path):
    """Two trajectories, two origins, one window each — the policy's arithmetic."""

    rows = _dataset(tmp_path)
    schedule = _fixture_schedule()
    extractor = WindowFeatureExtractor(window_steps=WINDOW)
    observations, labels = _fixture_role_loaders(tmp_path)
    s_rows = [row for row in rows if row.suite == "S"]
    examples = load_arm_examples(
        s_rows,
        suite="S",
        schedule_by_trajectory=schedule,
        extractor=extractor,
        observation_loader=observations["S"],
        label_loader=labels,
    )
    assert len(examples) == len(s_rows)
    assert {e.trajectory_spec_id for e in examples} == {ORDINARY, DIAGNOSTIC}

    # The two windows really are different slices of otherwise identical construction.
    by_trajectory = {e.trajectory_spec_id: e for e in examples}
    raw = {
        row.trajectory_spec_id: observations["S"].load(row.run_id) for row in s_rows
    }
    for name, example in by_trajectory.items():
        origin = schedule[name].origin_step
        np.testing.assert_allclose(
            example.values[:, 0], raw[name].values["q_obs"][origin : origin + WINDOW, 0]
        )
    assert schedule[ORDINARY].origin_step != schedule[DIAGNOSTIC].origin_step


def test_a_row_naming_an_unscheduled_trajectory_is_refused(tmp_path):
    """A row with no window must refuse, never be silently dropped from the census."""

    _dataset(tmp_path)
    stray = _manifest_row("dev", "S", 0, trajectory="unscheduled_z")
    extractor = WindowFeatureExtractor(window_steps=WINDOW)
    observations, labels = _fixture_role_loaders(tmp_path)
    with pytest.raises(DevFitContractError, match="does not schedule"):
        load_arm_examples(
            [stray],
            suite="S",
            schedule_by_trajectory=_fixture_schedule(),
            extractor=extractor,
            observation_loader=observations["S"],
            label_loader=labels,
        )


def test_unmatched_per_trajectory_counts_are_refused():
    """C1/S matchedness is the paired comparison's premise, so it is measured."""

    schedule = _fixture_schedule()
    balanced = [
        _manifest_row("dev", suite, 0, trajectory=trajectory)
        for trajectory in ("ordinary_a", "diagnostic_b")
        for suite in ("C1", "S")
    ]
    census = require_matched_trajectory_census(balanced, schedule)
    assert census == {
        ORDINARY: {"C1": 1, "S": 1},
        DIAGNOSTIC: {"C1": 1, "S": 1},
    }

    extra = balanced + [_manifest_row("dev", "S", 1, trajectory="diagnostic_b")]
    with pytest.raises(DevFitContractError, match="not matched across suites"):
        require_matched_trajectory_census(extra, schedule)

    one_suite = [row for row in balanced if row.suite == "C1"]
    with pytest.raises(DevFitContractError, match="not present in both matched suites"):
        require_matched_trajectory_census(one_suite, schedule)

    missing_both = [row for row in balanced if row.trajectory_spec_id == DIAGNOSTIC]
    with pytest.raises(DevFitContractError, match="cover every scheduled trajectory"):
        require_matched_trajectory_census(missing_both, schedule)

    disjoint_pairs = [
        _manifest_row("dev", "C1", 0, trajectory="ordinary_a"),
        _manifest_row("dev", "S", 1, trajectory="ordinary_a"),
        _manifest_row("dev", "C1", 0, trajectory="diagnostic_b"),
        _manifest_row("dev", "S", 1, trajectory="diagnostic_b"),
    ]
    with pytest.raises(DevFitContractError, match="not identity-matched"):
        require_matched_trajectory_census(disjoint_pairs, schedule)


def test_a_payload_whose_length_disagrees_with_the_assignment_is_refused(tmp_path):
    """The schedule and the payload are independent sources for the same fact."""

    rows = _dataset(tmp_path)
    target = next(row for row in rows if row.suite == "S")
    _dataset(tmp_path, steps={target.run_id: STEPS + 1})
    extractor = WindowFeatureExtractor(window_steps=WINDOW)
    observations, labels = _fixture_role_loaders(tmp_path)
    with pytest.raises(DevFitDataError, match="the assignment reserves"):
        load_arm_examples(
            [target],
            suite="S",
            schedule_by_trajectory=_fixture_schedule(),
            extractor=extractor,
            observation_loader=observations["S"],
            label_loader=labels,
        )


def test_a_label_onset_that_disagrees_with_the_assignment_is_refused(tmp_path):
    """The schedule origin is assignment-derived, but the persisted label must agree."""

    rows = _dataset(tmp_path)
    target = next(row for row in rows if row.suite == "S")
    np.savez(
        tmp_path / "labels" / f"{target.run_id}.npz",
        **_label_payload(onset_index=FIXTURE_ONSET[target.trajectory_spec_id] + 1),
    )
    extractor = WindowFeatureExtractor(window_steps=WINDOW)
    observations, labels = _fixture_role_loaders(tmp_path)
    with pytest.raises(DevFitDataError, match="disagrees with assignment trajectory"):
        load_arm_examples(
            [target],
            suite="S",
            schedule_by_trajectory=_fixture_schedule(),
            extractor=extractor,
            observation_loader=observations["S"],
            label_loader=labels,
        )


@pytest.mark.parametrize(
    ("moved", "why"),
    [
        ("onset_index", "the index disagrees while the time still agrees"),
        ("onset_time_s", "the time disagrees while the index still agrees"),
    ],
)
def test_each_half_of_the_onset_binding_is_load_bearing_on_its_own(tmp_path, moved, why):
    """The index and the time must be checked SEPARATELY, and only this can show it.

    Session 83, and it is Session 52's lesson 63 in a new place. `_label_payload` derives
    `onset_time_s` from `onset_index`, so the existing disagreement test moves both at
    once and either check alone catches it — which is exactly why the sweep could delete
    either one individually with the focused suite green. Two conditions in one `or`
    chain are two mutually redundant guards unless something drives them apart.

    The state each case constructs is also the realistic one: a payload whose two onset
    fields disagree *with each other* is what a regeneration bug produces, and it is the
    reason the reviewer bound both rather than one.
    """

    rows = _dataset(tmp_path)
    target = next(row for row in rows if row.suite == "S")
    correct = FIXTURE_ONSET[target.trajectory_spec_id]
    payload = _label_payload(onset_index=correct)
    if moved == "onset_index":
        payload["onset_index"] = np.asarray(correct + 1, dtype=np.int64)
    else:
        payload["onset_time_s"] = np.asarray(
            correct * 0.002 + 0.5, dtype=np.float64
        )
    np.savez(tmp_path / "labels" / f"{target.run_id}.npz", **payload)

    observations, labels = _fixture_role_loaders(tmp_path)
    with pytest.raises(DevFitDataError, match="disagrees with assignment trajectory"):
        load_arm_examples(
            [target],
            suite="S",
            schedule_by_trajectory=_fixture_schedule(),
            extractor=WindowFeatureExtractor(window_steps=WINDOW),
            observation_loader=observations["S"],
            label_loader=labels,
        )


def test_the_onset_time_binding_is_an_equality_not_a_tolerance(tmp_path):
    """The 1e-12 comparison must not be readable as a loose agreement window.

    Session 83: the sweep widened the tolerance to a full second and the focused suite
    stayed green, because no case ever supplied a small disagreement. One control period
    (0.002 s) is the smallest disagreement that can mean anything here, and it must be
    refused.
    """

    rows = _dataset(tmp_path)
    target = next(row for row in rows if row.suite == "S")
    correct = FIXTURE_ONSET[target.trajectory_spec_id]
    payload = _label_payload(onset_index=correct)
    payload["onset_time_s"] = np.asarray(correct * 0.002 + 0.002, dtype=np.float64)
    np.savez(tmp_path / "labels" / f"{target.run_id}.npz", **payload)

    observations, labels = _fixture_role_loaders(tmp_path)
    with pytest.raises(DevFitDataError, match="disagrees with assignment trajectory"):
        load_arm_examples(
            [target],
            suite="S",
            schedule_by_trajectory=_fixture_schedule(),
            extractor=WindowFeatureExtractor(window_steps=WINDOW),
            observation_loader=observations["S"],
            label_loader=labels,
        )


def test_load_arm_examples_refuses_a_withheld_role_at_the_point_of_consumption(tmp_path):
    """Bound 1 is checked where rows are USED, because a caller can build the list."""

    _dataset(tmp_path, splits=("dev", "val"))
    val_rows = [_manifest_row("val", "S", 0)]
    extractor = WindowFeatureExtractor(window_steps=WINDOW)
    observations, labels = _fixture_role_loaders(tmp_path)
    with pytest.raises(DevFitContractError, match="may read no withheld role"):
        load_arm_examples(
            val_rows,
            suite="S",
            schedule_by_trajectory=_fixture_schedule(),
            extractor=extractor,
            observation_loader=observations["S"],
            label_loader=labels,
        )


def test_load_arm_examples_refuses_a_row_from_the_other_matched_suite(tmp_path):
    """A nominal C1 arm may not consume S rows while every row still says `dev`."""

    _dataset(tmp_path)
    s_rows = [_manifest_row("dev", "S", 0)]
    extractor = WindowFeatureExtractor(window_steps=WINDOW)
    observations, labels = _fixture_role_loaders(tmp_path)
    with pytest.raises(DevFitContractError, match="only rows from suite"):
        load_arm_examples(
            s_rows,
            suite="C1",
            schedule_by_trajectory=_fixture_schedule(),
            extractor=extractor,
            observation_loader=observations["C1"],
            label_loader=labels,
        )


def test_training_code_identity_names_every_runtime_module_that_defines_the_protocol():
    """Bound 4: a checkpoint names the code that produced it, built by `code_identity`."""

    identity = training_code_identity()
    assert set(identity) == {
        "dev_fit_trainer.py",
        "dev_fit_contract.py",
        "attribution_net.py",
        "config_contract.py",
        "estimator.py",
        "role_contract.py",
        "schema_types.py",
        "storage_contract.py",
    }
    for label, digest in identity.items():
        assert len(digest) == 64 and digest == digest.lower(), label


def test_fit_one_arm_refuses_a_nonfinite_loss_before_any_checkpoint(monkeypatch):
    """A diverged optimizer path becomes a named data failure, not invalid JSON later."""

    extractor = WindowFeatureExtractor(window_steps=WINDOW)
    example = TrainingExample(
        run_id="r",
        trajectory_spec_id=DIAGNOSTIC,
        values=np.zeros((WINDOW, extractor.registry_width), dtype=float),
        valid=np.ones((WINDOW, extractor.registry_width), dtype=bool),
        class_index=0,
        location_index=0,
        severity=0.0,
        ood_flag=False,
    )

    def _nonfinite_loss(_heads, batch):
        return torch.tensor(float("nan"), device=batch["inputs"].device, requires_grad=True)

    monkeypatch.setattr(trainer, "arm_loss", _nonfinite_loss)
    with pytest.raises(DevFitDataError, match="non-finite"):
        trainer.fit_one_arm(
            [example],
            seed=0,
            epochs=1,
            batch_size=1,
            learning_rate=1.0e-3,
            device=torch.device("cpu"),
        )


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
        protocol_code_identity=training_code_identity(),
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
def test_plan_mode_publishes_the_real_derived_schedule_and_runs_nothing(tmp_path):
    """X_PLAN_OK: no monkeypatching — the artifact carries the production schedule.

    The plan is the document a reviewer reads to see which slice the fit will consume, so
    it is worth nothing if the test that reads it substituted a fixture first.
    """

    code = main(["--mode", "plan", "--output-dir", str(tmp_path)])
    assert code == EXIT_CODES[X_PLAN_OK]
    document = json.loads((tmp_path / "dev_fit_plan.json").read_text(encoding="utf-8"))
    assert document["exit"] == X_PLAN_OK
    assert document["authority"] == DEVELOPMENT_ONLY_AUTHORITY
    assert document["fits_run"] == 0 and document["rollouts_spent"] == 0
    assert document["n_arms"] == len(matched_fit_plan()) == 10
    assert [(arm["suite"], arm["seed"]) for arm in document["arms"]] == list(matched_fit_plan())
    assert set(document["code_identity"]) == set(training_code_identity())

    protocol = document["training_protocol"]
    assert protocol["assignment_sha256"] == ASSIGNMENT_CANONICAL_SHA256
    assert protocol["split"] == "dev" and protocol["windows_per_run"] == 1
    published = {
        entry["trajectory_spec_id"]: (entry["origin_step"], entry["decision_step"])
        for entry in protocol["window_schedule"]
    }
    assert published == {ORDINARY: (900, 1668), DIAGNOSTIC: (1000, 1768)}


def test_plan_refuses_a_schedule_that_does_not_end_at_the_held_decision(
    tmp_path, monkeypatch
):
    """A derivation that drifts from the policy takes a named exit, not a silent fit."""

    drifted = _fixture_schedule()
    entry = drifted[DIAGNOSTIC]
    drifted[DIAGNOSTIC] = WindowSchedule(
        trajectory_spec_id=entry.trajectory_spec_id,
        onset_step=entry.onset_step,
        lead_steps=entry.lead_steps,
        origin_step=entry.origin_step,
        window_steps=WINDOW,
        decision_step=entry.decision_step + 1,
        run_steps=entry.run_steps,
        has_diagnostic_probe=True,
    )
    _authorize_fixture_window(monkeypatch, drifted)
    code = main(["--mode", "plan", "--output-dir", str(tmp_path)])
    assert code == EXIT_CODES[X_CONTRACT_REFUSED]
    document = json.loads((tmp_path / "dev_fit_plan.json").read_text(encoding="utf-8"))
    assert document["exit"] == X_CONTRACT_REFUSED
    assert document["reason_class"] == "DevFitContractError"
    assert document["fits_run"] == 0


def test_fit_without_the_required_inputs_takes_the_data_missing_exit(tmp_path):
    """X_DATA_MISSING: `--data-root` has no default, so its absence is an exit."""

    code = main(["--mode", "fit", "--output-dir", str(tmp_path)])
    assert code == EXIT_CODES[X_DATA_MISSING]
    document = json.loads((tmp_path / "dev_fit_result.json").read_text(encoding="utf-8"))
    assert document["exit"] == X_DATA_MISSING
    assert document["fits_run"] == 0


def test_a_manifest_with_no_dev_row_takes_the_contract_refused_exit(tmp_path, monkeypatch):
    """X_CONTRACT_REFUSED: a fit over zero rows is a defect, not an empty result."""

    root = tmp_path / "data"
    root.mkdir()
    _dataset(root, splits=("val",))
    _authorize_fixture_dataset(monkeypatch, root)
    output = tmp_path / "out"
    code = main(
        ["--mode", "fit", "--output-dir", str(output), "--data-root", str(root)]
    )
    assert code == EXIT_CODES[X_CONTRACT_REFUSED]
    document = json.loads((output / "dev_fit_result.json").read_text(encoding="utf-8"))
    assert document["exit"] == X_CONTRACT_REFUSED
    assert document["reason_class"] == "DevFitContractError"
    assert document["fits_run"] == 0
    assert document["trajectory_census"] is None


def test_the_refusal_message_itself_is_never_persisted(tmp_path, monkeypatch):
    """The artifact records the exception CLASS; the message goes to stdout only.

    A refusal can quote a caller-supplied string, and requirement (z) forbids a result
    artifact from recording an absolute path. This trainer does not scrub — the accept
    side of a scrubber is where damage is invisible — it simply never writes the message.
    """

    root = tmp_path / "data"
    root.mkdir()
    _dataset(root, splits=("val",))
    _authorize_fixture_dataset(monkeypatch, root)
    output = tmp_path / "out"
    main(["--mode", "fit", "--output-dir", str(output), "--data-root", str(root)])
    text = (output / "dev_fit_result.json").read_text(encoding="utf-8")
    assert "reason_class" in text
    for leaked in ("manifest rows selected", "no dev row of suites", str(root)):
        assert leaked not in text, f"the artifact persisted {leaked!r}"


def test_a_bound_violation_inside_the_fit_is_not_filed_as_missing_data(
    tmp_path, monkeypatch
):
    """Session 82: `DevFitContractError` is a `RuntimeError`, so it can be swallowed.

    `fit_one_arm` checks bound 3 (`require_predeclared_seed`) and the caller converts
    `RuntimeError` into a data error to name torch's runtime failures. Both are
    `RuntimeError` subclasses, so without an explicit re-raise a bound violation is filed
    as `X_DATA_MISSING`/`DevFitDataError` — the wrong exit, the wrong code, and a bound
    violation recorded as a missing file.
    """

    root = tmp_path / "data"
    root.mkdir()
    _dataset(root)
    _authorize_fixture_dataset(monkeypatch, root)
    monkeypatch.setattr(trainer, "matched_fit_plan", lambda: (("C1", 99),))
    output = tmp_path / "out"
    code = main(
        [
            "--mode", "fit",
            "--output-dir", str(output),
            "--data-root", str(root),
            "--epochs", "1",
        ]
    )
    assert code == EXIT_CODES[X_CONTRACT_REFUSED]
    document = json.loads((output / "dev_fit_result.json").read_text(encoding="utf-8"))
    assert document["exit"] == X_CONTRACT_REFUSED
    assert document["reason_class"] == "DevFitContractError"
    assert document["fits_run"] == 0
    assert not list(output.glob("*.pt"))


def test_a_missing_observation_payload_records_every_completed_arm(tmp_path, monkeypatch):
    """A partial failure leaves no checkpoint without its full provenance record."""

    root = tmp_path / "data"
    root.mkdir()
    rows = _dataset(root)
    _authorize_fixture_dataset(monkeypatch, root)
    first_s = next(row for row in rows if row.suite == "S")
    (root / "observations" / "S" / f"{first_s.run_id}.npz").unlink()
    output = tmp_path / "out"
    code = main(
        [
            "--mode", "fit",
            "--output-dir", str(output),
            "--data-root", str(root),
            "--epochs", "1",
        ]
    )
    assert code == EXIT_CODES[X_DATA_MISSING]
    document = json.loads((output / "dev_fit_result.json").read_text(encoding="utf-8"))
    assert document["exit"] == X_DATA_MISSING
    assert document["reason_class"] == "DevFitDataError"
    assert document["fits_run"] == 5
    assert len(document["arms"]) == 5
    assert document["trajectory_census"] == {
        ORDINARY: {"C1": 1, "S": 1},
        DIAGNOSTIC: {"C1": 1, "S": 1},
    }
    for arm in document["arms"]:
        assert arm["authority"] == DEVELOPMENT_ONLY_AUTHORITY
        assert arm["examples_by_trajectory"] == {ORDINARY: 1, DIAGNOSTIC: 1}
        assert (output / arm["checkpoint_name"]).is_file()


def test_a_complete_fit_writes_one_validated_provenance_record_per_arm(tmp_path, monkeypatch):
    """X_FIT_OK: ten arms, ten provenance records on disk, zero rollouts.

    This asserts what the exit WROTE, not that the model learned anything. Whether the
    loss falls on real dev rows is the measurement this trainer exists to make, and it is
    not authorized to run until this executable's own review closes.
    """

    root = tmp_path / "data"
    root.mkdir()
    _dataset(root)
    _authorize_fixture_dataset(monkeypatch, root)
    output = tmp_path / "out"
    code = main(
        [
            "--mode", "fit",
            "--output-dir", str(output),
            "--data-root", str(root),
            "--epochs", "2",
            "--batch-size", "2",
        ]
    )
    assert code == EXIT_CODES[X_FIT_OK]
    document = json.loads((output / "dev_fit_result.json").read_text(encoding="utf-8"))
    assert document["exit"] == X_FIT_OK
    assert document["fits_run"] == 10
    assert document["rollouts_spent"] == 0
    assert document["trajectory_census"] == {
        ORDINARY: {"C1": 1, "S": 1},
        DIAGNOSTIC: {"C1": 1, "S": 1},
    }
    published = {
        entry["trajectory_spec_id"]: entry
        for entry in document["training_protocol"]["window_schedule"]
    }
    assert set(published) == {ORDINARY, DIAGNOSTIC}
    for name, entry in published.items():
        assert entry["origin_step"] == FIXTURE_ONSET[name] + FIXTURE_LEAD
        assert entry["decision_step"] == entry["origin_step"] + WINDOW
        assert entry["windows_per_run"] == 1

    recorded = [(arm["suite"], arm["training_seed"]) for arm in document["arms"]]
    assert recorded == list(matched_fit_plan())
    for arm in document["arms"]:
        assert arm["authority"] == DEVELOPMENT_ONLY_AUTHORITY
        assert arm["assignment_sha256"] == ASSIGNMENT_CANONICAL_SHA256
        assert arm["config_hash"].startswith("dev-")
        assert len(arm["checkpoint_sha256"]) == 64
        assert set(arm["code_identity"]) == set(training_code_identity())
        assert arm["code_identity"] == document["code_identity"]
        assert arm["data_root_name"] == "data"
        assert arm["examples_by_trajectory"] == {ORDINARY: 1, DIAGNOSTIC: 1}
        assert arm["n_examples"] == 2
        assert arm["role_index_sha256"] == document["role_index_sha256"]
        assert arm["training_protocol"] == document["training_protocol"]
        assert file_sha256(output / arm["checkpoint_name"]) == arm["checkpoint_sha256"]
    for suite, seed in matched_fit_plan():
        assert (output / f"dev_fit_{suite}_seed{seed}.pt").is_file()


def test_fit_refuses_a_well_formed_but_unapproved_dataset(tmp_path, monkeypatch):
    """Recording an arbitrary manifest digest is not authority to train on that root."""

    root = tmp_path / "lookalike"
    root.mkdir()
    _dataset(root)
    _authorize_fixture_window(monkeypatch)
    output = tmp_path / "out"
    code = main(
        ["--mode", "fit", "--output-dir", str(output), "--data-root", str(root)]
    )
    assert code == EXIT_CODES[X_CONTRACT_REFUSED]
    document = json.loads((output / "dev_fit_result.json").read_text(encoding="utf-8"))
    assert document["exit"] == X_CONTRACT_REFUSED
    assert document["fits_run"] == 0
    assert not list(output.glob("*.pt"))


def test_fit_refuses_an_output_directory_with_a_stale_checkpoint(tmp_path, monkeypatch):
    """A rerun may not mix current arms with checkpoints left by an earlier attempt."""

    root = tmp_path / "data"
    root.mkdir()
    _dataset(root)
    _authorize_fixture_dataset(monkeypatch, root)
    output = tmp_path / "out"
    output.mkdir()
    (output / "dev_fit_C1_seed0.pt").write_bytes(b"stale")
    monkeypatch.setattr(
        trainer,
        "fit_one_arm",
        lambda *args, **kwargs: pytest.fail("fit began before stale output was refused"),
    )
    code = main(
        ["--mode", "fit", "--output-dir", str(output), "--data-root", str(root)]
    )
    assert code == EXIT_CODES[X_OUTPUT_DIRTY]
    document = json.loads(
        (output / trainer.OUTPUT_DIRTY_ARTIFACT).read_text(encoding="utf-8")
    )
    assert document["exit"] == X_OUTPUT_DIRTY
    assert document["fits_run"] == 0
    assert document["authority"] == DEVELOPMENT_ONLY_AUTHORITY


def test_the_refusal_does_not_destroy_the_record_it_is_protecting(tmp_path, monkeypatch):
    """The guard's own refusal may not overwrite `dev_fit_result.json`.

    Session 83. The reviewer state staged only a stale checkpoint, so the directory it
    refused had no prior result document to lose — the fixture already had the property
    that made the defect invisible (limitation 111's shape, and Session 58's). Staging the
    document too shows what the refusal did: `torch.save` embeds no provenance, so
    `dev_fit_result.json` is the ONLY record binding each surviving `.pt` to its data
    root, digests, suite, seed and code identity. Routing the refusal through an exit that
    writes that name deleted it and left the checkpoints orphaned beside a document
    reporting `fits_run: 0` — a worse mixed population than the one being refused.
    """

    root = tmp_path / "data"
    root.mkdir()
    _dataset(root)
    _authorize_fixture_dataset(monkeypatch, root)
    output = tmp_path / "out"
    output.mkdir()
    prior = output / "dev_fit_result.json"
    prior.write_text(
        json.dumps({"exit": X_FIT_OK, "fits_run": 2, "arms": ["provenance lives here"]}),
        encoding="utf-8",
        newline="\n",
    )
    prior_bytes = prior.read_bytes()
    checkpoint = output / "dev_fit_C1_seed0.pt"
    checkpoint.write_bytes(b"stale")
    checkpoint_bytes = checkpoint.read_bytes()
    monkeypatch.setattr(
        trainer,
        "fit_one_arm",
        lambda *args, **kwargs: pytest.fail("fit began before stale output was refused"),
    )

    code = main(
        ["--mode", "fit", "--output-dir", str(output), "--data-root", str(root)]
    )

    assert code == EXIT_CODES[X_OUTPUT_DIRTY]
    assert prior.read_bytes() == prior_bytes, "the prior result document was overwritten"
    assert checkpoint.read_bytes() == checkpoint_bytes
    document = json.loads(
        (output / trainer.OUTPUT_DIRTY_ARTIFACT).read_text(encoding="utf-8")
    )
    assert document["exit"] == X_OUTPUT_DIRTY
    assert trainer.OUTPUT_DIRTY_ARTIFACT != "dev_fit_result.json"


def test_the_staleness_guard_runs_before_the_first_write_of_any_exit(tmp_path):
    """The missing-`--data-root` exit sits ABOVE the guard and also writes the record.

    Session 83: with the guard placed inside the second `try`, this exit destroyed the
    prior result document without the guard running at all. Placement is the fix, so
    placement is what this test pins. It reaches no data root and no assignment file.
    """

    output = tmp_path / "out"
    output.mkdir()
    prior = output / "dev_fit_result.json"
    prior.write_text(
        json.dumps({"exit": X_FIT_OK, "fits_run": 2}), encoding="utf-8", newline="\n"
    )
    prior_bytes = prior.read_bytes()

    code = main(["--mode", "fit", "--output-dir", str(output)])

    assert code == EXIT_CODES[X_OUTPUT_DIRTY], "the data-missing exit ran first"
    assert prior.read_bytes() == prior_bytes
    document = json.loads(
        (output / trainer.OUTPUT_DIRTY_ARTIFACT).read_text(encoding="utf-8")
    )
    assert document["exit"] == X_OUTPUT_DIRTY


def test_a_prior_dirty_refusal_keeps_the_directory_closed_to_fitting(tmp_path):
    """A refused fit directory may not later carry two contradictory terminal exits.

    Codex Session 83 review. Claude's new refusal artifact sat outside the cleanliness
    guard as well as outside the checkpoint/result namespace. With only that artifact
    present, the current bytes accepted the directory, took the missing-data exit, and
    left `X_OUTPUT_DIRTY` beside a new `X_DATA_MISSING` result. That is not a fresh output
    directory and gives a reader two incompatible terminal records. A plan remains exempt,
    but every later fit invocation must keep this directory closed.
    """

    output = tmp_path / "out"
    output.mkdir()
    refusal = output / trainer.OUTPUT_DIRTY_ARTIFACT
    refusal.write_text(
        json.dumps({"exit": X_OUTPUT_DIRTY, "fits_run": 0}),
        encoding="utf-8",
        newline="\n",
    )

    code = main(["--mode", "fit", "--output-dir", str(output)])

    assert code == EXIT_CODES[X_OUTPUT_DIRTY], "the data-missing exit ran instead"
    assert not (output / "dev_fit_result.json").exists()
    document = json.loads(refusal.read_text(encoding="utf-8"))
    assert document["exit"] == X_OUTPUT_DIRTY
    assert document["fits_run"] == 0


def test_plan_mode_may_still_write_beside_an_earlier_fit_result(tmp_path):
    """The accept side of the exemption: the guard is fit-path only, deliberately.

    An operator may plan into a directory that already holds a completed fit, because a
    plan artifact overwrites nothing that binds a checkpoint to its provenance.
    """

    output = tmp_path / "out"
    output.mkdir()
    prior = output / "dev_fit_result.json"
    prior.write_text(
        json.dumps({"exit": X_FIT_OK, "fits_run": 10}), encoding="utf-8", newline="\n"
    )
    prior_bytes = prior.read_bytes()

    code = main(["--mode", "plan", "--output-dir", str(output)])

    assert code == EXIT_CODES[X_PLAN_OK]
    assert prior.read_bytes() == prior_bytes
    assert not (output / trainer.OUTPUT_DIRTY_ARTIFACT).exists()
    plan = json.loads((output / "dev_fit_plan.json").read_text(encoding="utf-8"))
    assert plan["exit"] == X_PLAN_OK


def test_equal_pair_id_sets_with_unequal_multiplicity_are_not_identity_matched():
    """Identity matching is a MULTISET property; a set comparison cannot establish it.

    Session 83, one layer below Finding O. The reviewer state upgraded matchedness from
    count equality to `pair_id` SET equality, which is the right property named with the
    wrong container: `C1 = [a, a, b]` against `S = [a, b, b]` has equal counts and equal
    sets, and two of its three rows have no partner. Measured accepted at `788fc240`.
    """

    schedule = _fixture_schedule()
    c1 = [_manifest_row("dev", "C1", i) for i in range(3)]
    s_rows = [_manifest_row("dev", "S", i) for i in range(3)]
    a, b = c1[0].pair_id, c1[1].pair_id
    skewed = [
        c1[0],
        dataclasses.replace(c1[1], pair_id=a),
        dataclasses.replace(c1[2], pair_id=b),
        dataclasses.replace(s_rows[0], pair_id=a),
        dataclasses.replace(s_rows[1], pair_id=b),
        dataclasses.replace(s_rows[2], pair_id=b),
    ]
    ordinary = [
        _manifest_row("dev", suite, 7, trajectory="ordinary_a") for suite in ("C1", "S")
    ]

    c1_ids = [row.pair_id for row in skewed if row.suite == "C1"]
    s_ids = [row.pair_id for row in skewed if row.suite == "S"]
    # The constructed state is exactly the one the weaker containers cannot see.
    assert len(c1_ids) == len(s_ids), "counts must be equal or a weaker check would fire"
    assert set(c1_ids) == set(s_ids), "sets must be equal or the set check would fire"
    assert sorted(c1_ids) != sorted(s_ids), "the multisets are what actually differ"

    with pytest.raises(DevFitContractError, match="not identity-matched"):
        require_matched_trajectory_census(skewed + ordinary, schedule)

    # The accept side, at the same shape: a genuinely matched population must pass.
    matched = [
        _manifest_row("dev", suite, index)
        for index in range(3)
        for suite in ("C1", "S")
    ] + ordinary
    census = require_matched_trajectory_census(matched, schedule)
    assert census[DIAGNOSTIC] == {"C1": 3, "S": 3}


def test_an_incomplete_plan_takes_its_named_main_exit(tmp_path, monkeypatch):
    """X_PLAN_INCOMPLETE: an unbalanced set is a difference between two seed populations.

    Monkeypatching the iterator to skip S models the code mutation this post-condition is
    meant to catch; the contract's independent expected plan remains unchanged.
    """

    root = tmp_path / "data"
    root.mkdir()
    _dataset(root)
    _authorize_fixture_dataset(monkeypatch, root)
    monkeypatch.setattr(
        trainer,
        "matched_fit_plan",
        lambda: tuple(arm for arm in matched_fit_plan() if arm[0] == "C1"),
    )
    output = tmp_path / "out"
    code = main(
        [
            "--mode", "fit",
            "--output-dir", str(output),
            "--data-root", str(root),
            "--epochs", "1",
        ]
    )
    assert code == EXIT_CODES[X_PLAN_INCOMPLETE]
    document = json.loads((output / "dev_fit_result.json").read_text(encoding="utf-8"))
    assert document["exit"] == X_PLAN_INCOMPLETE
    assert document["fits_run"] == 5 and len(document["arms"]) == 5


def test_every_named_exit_has_a_distinct_code_and_appears_in_the_table():
    """A named exit that is not in the table is an exit no artifact can report."""

    assert set(EXIT_CODES) == {
        X_PLAN_OK,
        X_FIT_OK,
        X_CONTRACT_REFUSED,
        X_DATA_MISSING,
        X_PLAN_INCOMPLETE,
        X_OUTPUT_DIRTY,
    }
    failures = {name: code for name, code in EXIT_CODES.items() if code != 0}
    assert len(set(failures.values())) == len(failures), "two failures share an exit code"


def test_the_source_class_order_this_trainer_targets_is_the_projects_order():
    """The class head's index convention is a shared decision, not this file's."""

    assert SOURCE_CLASS_ORDER == ("healthy", "structure", "actuator", "sensor")


def test_the_command_line_cannot_supply_a_window_origin():
    """The pre-registration-adjacent choice must be underivable from the command line."""

    with pytest.raises(SystemExit):
        trainer.parse_args(
            ["--mode", "plan", "--output-dir", ".", "--window-origin-step", "368"]
        )
