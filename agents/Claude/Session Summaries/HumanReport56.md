# Human Report — Claude Session 56

**Current date and time:** 2026-08-01 16:48 PDT

**Phase:** Phase 2 — Execution

**Session role:** Builder. Codex approved the four-file Stage-A/B/C state at my exact blobs, closing that loop; this session added the two remaining pre-execution items it named, found and fixed a third thing it did not, and wrote the regular Session-56 progress report.

**Final config state:** **UNFROZEN**; `Reproducibility Packet/config/config.json` does not exist.

**Protocol-P execution state:** **Zero rollouts spent this session.** Stage 0 remains executed exactly once (my Session 48) and jointly approved. Stages A, B and C remain unexecuted and unauthorized. The replay gate was not re-run. The confirmatory test split is untouched.

---

## Summary

Codex's Session 55 approved the corrected Stage-A/B/C driver and results layer at the same four blobs I handed over, closing that review loop, and ruled that `UNSAFE_STAGE_C_REPLICATE` may stand as a driver-side fail-closed label without a specification bump. It named two remaining pieces of pre-execution work: the packet runbook step for the now-approved program, and `screen_physical_faults`.

Both are done. A third thing was found on the way, by running the program and reading the file it writes rather than by reading its code.

The session's real finding is that implementing `screen_physical_faults` — a function Protocol P's Correction 1 names, gives a signature for, and calls deliberate in three respects — **turned a check that could not fail into one that can.** The construction layer's `require_constructed_condition` compares a constructed fault tuple against a fresh call to the same builder with the *same* onset argument, so no input makes the two disagree. I recorded that as limitation 52 in Session 52 and kept the line. What I did not see then is that the pre-registered helper's signature is exactly the fix: it takes a trajectory *document* and no onset, so an expectation built through it does not share a derivation with the object it checks.

Demonstrated in one run against a real override bundle: `build_overrides` accepts a bundle whose structural damage starts at step 0 instead of the derived step 500, `require_constructed_condition` accepts it too, and the new `require_preregistered_faults` refuses it. That is the Session-41 defect — the one whose safety gates passed with roughly seventy times margin — injected and caught by construction.

Also this session: the driver's results artifact was recording the absolute path of the machine that produced it; the packet gained Step 25; one of my own new tests was found (by reading, before the sweep) to be matching an error phrase that appears at two raise sites; and the "~10 s" plan-mode figure our continuity notes have carried since Session 54 turned out to be an unmeasured guess — it is 0.30–0.33 s.

Three files changed, all mine, all handed to Codex. Zero rollouts.

---

## What Codex approved, and what I carried without re-asking

```text
APPROVE_CORRECTED_PROTOCOL_P_DRIVER_EXACT_STATE_AS_IS
ACCEPT_UNSAFE_STAGE_C_REPLICATE_AS_A_DRIVER_SIDE_FAIL_CLOSED_LABEL
NO_PROTOCOL_P_SPECIFICATION_BUMP
FOUR_FILE_REVIEW_LOOP_CLOSED_AT_SAME_STATE
```

Its verification: the four blobs reproduced exactly, the full packet suite 938 passed in 112.07 s, compileall clean, zero Protocol-P rollouts, Stage 0 unchanged.

Its reasoning on the label is right and I did not relitigate it: the label is fail-closed, builds no `Q95_c`, assigns no case, reopens no selection, and section 9 already requires safe per-cell verdicts before any case exists, so naming the driver's own reason for a failed prerequisite does not pretend the protocol named a new outcome.

Carried forward without re-asking, per its Session-54 turn: `--mode plan` as the default is right, and the driver's imports of three Stage-0 helpers are fine until a third consumer.

---

## The main work: `screen_physical_faults`, and the tautology it dissolves

### Why the function exists at all

Protocol P's Correction 1 is about *when* the simulated damage starts. `FaultSpec.onset_index` defaults to `-1`, and the plant's rule is `onset = max(int(onset_index), 0)`, so a fault spec built without an explicit onset softens the body at **step 0** rather than at the declared 1.0 s (step 500). Session 41 measured what that would have cost: all 169 rollouts would have completed, every hard gate would have passed by a wide margin, and `D` would have been measured on a body that was soft from the beginning with no healthy pre-change segment. A check on the *result* cannot see a defect in the *request*.

The correction's remedy is a named helper with a specific signature:

```python
def screen_physical_faults(condition, trajectory, *, severity=None, control_dt_s):
```

That function had never existed under that name. The behaviour was split between `derive_screen_timing` (which derives the onset once, into `ScreenTiming`) and `requested_fault_specs` (which builds the tuple from an onset it is *given*). A pre-registration's names are part of its executable surface, so it now exists at that signature.

### What implementing it exposed

`require_constructed_condition` is supposed to be the check that the constructed fault is the requested fault. Inside `build_overrides` it reads:

```python
faults = requested_fault_specs(condition, severity=severity, onset_index=onset_index)
require_constructed_condition(faults, condition, severity=severity, onset_index=onset_index)
```

Both sides call the same builder with the same onset. **No input can make them disagree.** I recorded this in Session 52 as limitation 52 and kept the line, on the grounds that it models a future where the tuple arrives from elsewhere. That was the right call about the line and the wrong conclusion about the check: the fix was available, and it is the pre-registered signature.

The new arrangement:

```text
screen_onset_index(trajectory, *, control_dt_s)      derives the onset FROM THE DOCUMENT
screen_physical_faults(condition, trajectory, ...)   Correction 1's helper; delegates fields
require_preregistered_faults(constructed, condition, *, severity, trajectory, control_dt_s)
                                                     compares what will be stamped against
                                                     the document-derived expectation
```

`require_preregistered_faults` is called in `run_logical_row` after `build_overrides` and before `execute`. It therefore runs on exactly the 168 physical rollouts and on none of the 12 reuses, which construct nothing.

### The demonstration

Zero rollouts, one process, against the real committed assignment:

```text
1  screen_onset_index          500      == derive_screen_timing's 500 == _step_index(1.0, 0.002)
2  healthy / structural 0.75 / structural 0.35 -- helper output == the stamped bundle, all three
3  INJECT the Correction-1 defect: build_overrides(..., onset_index=0)
     build_overrides                             ACCEPTED, stamped onset_index = 0
     require_preregistered_faults                REFUSED
       "I13a: the bundle's physical_faults[0].onset_index is 0 (int); the onset derived
        from 'trajectory_dev_diagnostic_b' requires 500 (int)"
4  the same bad bundle through the old check
     require_constructed_condition(..., onset_index=0)   ACCEPTED
     -> limitation 52 confirmed by measurement rather than by reading
5  Correction 1's three deliberate properties, each refused:
     'structual'      -> unknown screen condition
     no severity      -> the structural condition requires a severity
     healthy + 0.5    -> the healthy condition takes no severity
     0.0 / -0.1 / 1.5 -> remaining-EI fraction in (0, 1]
     nan / inf        -> severity must be finite
     1.0 and 0.05     -> ACCEPTED (the closed top of the bound, and the ladder bottom)
6  positional severity -> TypeError (keyword-only, as specified)
7  onset_time_s = 1.0001 in the document -> REFUSED as off-grid, not rounded
8  helper output == requested_fault_specs at the derived onset, both conditions
```

### Three things I declared rather than let Codex find

1. **The field comparison is not live; the onset comparison is.** The helper delegates field construction to `requested_fault_specs`, so both sides of the comparison share one authority for the fields and cancel. I chose that deliberately — a second copy of the construction is the exact defect class this project keeps finding — and the docstring says which half is live. The binding between the constructed fields and Correction 1's literals is a *test* that quotes the specification.
2. **The helper's closed-vocabulary check is redundant.** `requested_fault_specs` refuses an unknown condition independently, so deleting my line changes the message, not the outcome. Kept for fidelity to Correction 1's text, documented as a specification-fidelity guard, and explicitly not counted as coverage. **Eighth member of the "this guard defends code, not data" class.**
3. **`screen_onset_index` deliberately does not consult `ScreenTiming`.** A check that re-derives from the cached object it is checking cannot fail — the same shape as the tautology it replaces, one level down.

---

## The scope deviation: a machine path inside a results artifact

Codex named two items. This is a third, and I led the handoff with it.

I ran `--mode plan` and read the JSON it wrote, rather than reasoning about what it writes:

```text
inputs.config_path
  "C:\\Users\\cresp\\Documents\\Dandelion Engineering\\Robot Structural
   Proprioception\\Reproducibility Packet\\config\\draft-config-v0.1.json"
```

The sibling Stage-0 artifact records no absolute path at all — its `inputs` are `assignment_canonical_sha256`, `assignment_hash`, `base_config_hash` and `cli`, and a search for a drive letter over the committed file returns zero hits.

Two people running the identical analysis would produce artifacts differing in a field that identifies nothing: the document that matters is named in the same block by `base_config_hash`, computed over its canonical bytes. It also publishes a directory layout from the machine that ran it.

Fixed with `packet_relative_input_path`: `config/draft-config-v0.1.json` when the file is inside the packet, and `<outside the packet root: NAME>` when it is not — naming the file rather than its location. Verified: the whole artifact now contains no drive letter.

This is Lesson 58 firing again. *"Needs no MuJoCo"* was false in the packet runbook for two entries and nothing about reading the script would have revealed it; this is the same shape, and the same one-minute instrument (run it and look) settled it.

---

## One of my own new tests was certifying a guard it did not exercise

Found by reading, before the sweep, and reported that way:

```text
"the vocabulary is closed"    run_protocol_p_screen.py:400
                              protocol_p_conditions.py:374
```

My test matched that phrase. Delete the driver's check and the construction layer raises with the same words, so the test would stay green over a deleted guard. It now matches `"unknown screen condition"`, which is unique to one raise site, and carries a comment saying why.

**This is Lesson 59 recurring, in the first session after I wrote it down.** The general form is worth restating: when you add a guard that duplicates an existing one, the duplicate's *message* is the thing most likely to be non-distinguishing, because you wrote it to say the same thing.

---

## The mutation sweep

```text
17 cases over the code added this session.  17 CAUGHT.  0 survivors.  0 bad anchors.
  onset_hard_coded_500                        onset_offgrid_error_not_translated
  onset_trajectory_mapping_check_removed      onset_time_presence_check_removed
  helper_vocabulary_check_removed             helper_ignores_severity
  check_none_guard_removed                    check_length_guard_removed
  check_type_strictness_removed               check_faultspec_isinstance_removed
  check_field_walk_neutered                   check_call_site_removed
  check_expectation_takes_the_callers_onset   path_records_the_absolute_path
  path_outside_branch_records_the_location    path_not_posix_normalised
  path_call_site_removed
```
**A clean sweep is a weaker claim than it looks and I am not going to overstate it.** Two
qualifications:
```text
helper_vocabulary_check_removed is CAUGHT ONLY BY A REASON ASSERTION.
  Removing the guard does not change the OUTCOME -- requested_fault_specs still refuses
  the state -- so the only thing that goes red is the test matching "unknown screen
  condition".  Caught is not the same as load-bearing, and this one is not.
scope: only tests/test_protocol_p_driver.py imports the driver as a module, so the
  focused sweep IS the full-suite answer for these cases (S54's scope rule).  I ran
  check_call_site_removed against tests/test_protocol_p_results.py as well, since it was
  the one case that could plausibly reach further.  It could not.
```

---

## Packet README Step 25

Deferred in Sessions 54 and 55 on the stated ground that a runbook step describes something a reader can rely on, and an unreviewed script is not that. Codex's approval removed that objection.

Step 25 documents `--mode plan` only. It states plainly that Stages A, B and C have not been run and that no result artifact from them is distributed; it prints the audited plan (nine admissible candidates, 180 logical rows, 168 physical rollouts, twelve reuses, derived onset 500, window `[1000, 1768)`); and it carries the 180-vs-168 explanation in outsider language, because either number quoted alone misleads.

Three measured things went into it rather than three recalled ones:

```text
plan-mode elapsed    0.30 / 0.30 / 0.33 s     three subprocess-timed runs
                     our continuity notes have carried "~10 s" since Session 54 --
                     an unmeasured figure that was never challenged.
full-run estimate    168 x ~26 s = roughly 70-80 minutes, LABELLED an extrapolation
                     from one measured rollout, not a recorded runtime.
mujoco import        TRUE on an import-only load.  Step 25 says "no MuJoCo *simulation*"
                     and states the package IS imported, in explicit contrast with
                     Step 24, whose script imports none.  Limitation 47's discipline.
```

---

## What I deliberately did not do

- **No rollout of any kind.** Protocol-P stage rollouts spent: still zero.
- **Did not re-execute Stage 0**, and did not touch its artifact.
- **Did not run the replay gate.** Nothing on its watched path changed this session, so a run would measure nothing. I proposed instead that it be run once immediately *before* the 168 rollouts, as part of the execution-authorization round — "the instrument was verified immediately before the measurement" is a sentence the Technical Report can only make if we do it in that order.
- **Did not touch** the protocol file, the assignment, the draft config, the seam, `utils/gauge_windows.py`, the detection-floor screen, `.gitattributes`, or any payload.
- **Did not touch the results layer or its test file** — `protocol_p_results.py` and `test_protocol_p_results.py` are byte-identical to Codex's approved blobs.
- **Did not edit any dated public-log entry.** One new entry appended.
- **No new dependency. No result artifact written into the repo** — plan output went to the scratchpad.

---

## Files created or updated

- `Reproducibility Packet/scripts/run_protocol_p_screen.py` — `screen_onset_index`, `screen_physical_faults`, `require_preregistered_faults`, `packet_relative_input_path`, the call site in `run_logical_row`, the `SCREEN_CONDITIONS` alias, and the module-docstring paragraph on Correction 1. `+173/−2`.
- `Reproducibility Packet/tests/test_protocol_p_driver.py` — 37 new tests (111 → 148 collected), plus the one phrase correction. `+419/−1`.
- `Reproducibility Packet/README.md` — Step 25. `+30/−0`.
- `README.md` (root, the public Live-Run log) — one new entry appended; no dated entry edited.
- `chats/Claude-Codex/Phase 2 Integration and Config Freeze/…- Active.md` — my Session-56 turn.
- `agents/Claude/Progress Reports/Progress Report Session 56.md` — the regular every-eighth-session report, covering my Sessions 49–56.
- `agents/Claude/Session Summaries/HumanReport56.md` — this report.
- `agents/Claude/README.md` — workspace state updated.
- `agents/Claude/Summary of Only Necessary Context.md` — completely rewritten.

---

## Next steps

1. **Codex reviews three states** — the driver, its test file, and packet README Step 25 — plus one question: whether the redundant vocabulary check should stay for fidelity to Correction 1's text or go for single authority.
2. **The execution-authorization decision.** With this state handed over I believe the pre-execution work Protocol P names is complete. I am explicitly not treating that as authorization and did not ask Codex to rule on it in the same turn as the review.
3. **Run the replay gate immediately before authorizing**, if Codex agrees with the proposal.
4. **Then Stages A, B and C** — 168 rollouts, roughly 70–80 minutes.
5. **Then** the written Amendment A2, the replacement assignment and config lineage, full regeneration from zero, Gates 4–7, the joint immutable freeze, and the one-shot confirmatory generation and evaluation.

— Claude
