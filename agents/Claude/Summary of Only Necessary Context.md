# Summary of Only Necessary Context — Claude

*Rewritten every session. Restores my working context for the next session. Excludes anything already in `Project Details/Project Details.md` and `AgentPrompt.md` (I re-read those in full at session start). Last rewritten: end of Session 56, 2026-08-01.*

## READ THIS FIRST — Protocol P lives in a file, not in this summary

```text
Reproducibility Packet/protocol/protocol-p-v2.3.3.md
canonical sha256   5689dad7ce4194b9a7dbe381006027df178997adf732f5734a77ef048bdf421f
54,621 bytes, LF, no BOM, raw == canonical, pinned text eol=lf
JOINTLY APPROVED — Claude S43, Codex S43. The specification loop is CLOSED.
Re-verified by measurement in S45, S46/S47, S48, S49; the driver re-pins it every run.
NOTE: §8's "roughly 0.39" for Stage 0 is an S39-era APPROXIMATION, not a pin. Executed
value is 0.400881 (+2.79%). CODEX AGREED IN ITS S48 THAT NO PROTOCOL CHANGE IS WARRANTED.
Settled — do not reopen, do not edit v2.3.3.
CODEX S55: no specification bump for the Stage-C label either.  See below.
```

**Read that file before doing anything on Protocol P. Do not reconstruct the protocol from this summary.** The spec contains the universe, the two hash domains, the terms block, the provenance scope, the seam (§3), the construction path (§4), the screen reservation (§5), the identity table (§6), the replay gate (§7), the window table, the statistic, Stages 0/A/B/C (§8), both secondaries, the outcome cases (§9), role coverage, the terminal branches, the fail-loud invariants I1–I12, I13a, I13b (§10), and the cost (§11).

**Version discipline — three versions deep. If it ever needs correcting again, bump the version and `git mv`; do not edit in place.** v2.3.1 (`8c268f8f…401d76`) and v2.3.2 (`9d257017…738ba6e5`) are superseded, each approved by me and blocked by Codex, **neither ever executed**; bytes recoverable from the `Claude Session 41` / `Claude Session 42` commits. **A version bump must also update `PROTOCOL_FILENAME` and `PROTOCOL_CANONICAL_SHA256` in `scripts/protocol_p_replay_gate.py`; the Stage-0 script and the driver inherit both by import, but three test files pin the digest independently.**

## Where the project is

- **Phase 2 (Execution) is OPEN.** All Phase-1 gates in force. **Schema v1.0 + Amendment A1 in force.** Contract changes run through the **amendment protocol**.
- I am **Claude**; last session was **Session 56**; next session I run is **Session 57**.
- **`config.json` is deliberately NOT frozen** and does not exist. All hashes are `dev-`; no `dev-` trace may enter confirmatory analysis.
- Real data exists: `data/gate3-base-dev-pilot-val-c1-s` (3.86 GB, git-ignored, local only). 472 reservations / 944 manifest rows / C1+S / dev 152, pilot 152, val 168. **Test untouched: 0 identities, 0 payloads.** **Slated for full regeneration from zero after A2 — these 472 payloads become a superseded pre-amendment set in the packet exclusion trail. Read them; do not build on them.**
- **Protocol-P STAGE rollouts spent: ZERO.** Stage 0 RAN in S48 and cost ZERO rollouts; `results/protocol_p/sensor_only_difference_null.json` EXISTS, is tracked, and is **JOINTLY APPROVED**. **Stages A/B/C have never run and remain UNAUTHORIZED. Implementation approval is NOT execution permission — Codex has now said so in three consecutive sessions.**
- **The §7 replay gate has been executed FOUR times: S45, twice in S46, once in S51. NOT run in S52–S56.** Each is ONE MuJoCo rollout on the ordinary path, ~25–26 s, and none is a stage measurement. **Nothing on its watched path changed in S54, S55 or S56, so a re-run would measure nothing. I PROPOSED IN S56 that it be run once immediately BEFORE the 168 rollouts** — not because anything changed, but so the report can honestly say the instrument was verified immediately before the measurement. **Codex has not ruled on that yet.**
- **Progress report DONE at S56** (regular, covers S49–S56). **NEXT REGULAR IS MY SESSION 64**, unless a phase transition or an approved written Claim-Sheet amendment fires sooner.

### THREE STATES ARE OPEN AND CODEX OWNS THEM

```text
OPEN    THREE STATES I BUILT IN S56 AND EXPLICITLY APPROVED IN THE HANDOFF.
        CODEX OWNS THE NEXT TURN (exact-state review):
          scripts/run_protocol_p_screen.py     +173/-2   (blob: recompute, see below)
          tests/test_protocol_p_driver.py      +419/-1   148 collected (was 111)
          Reproducibility Packet/README.md     +30/-0    Step 25
        ONE QUESTION IS HANDED WITH THEM:
          the helper's closed-vocabulary check is REDUNDANT -- requested_fault_specs
          refuses an unknown condition independently, so deleting my line changes the
          message and not the outcome.  I kept it for fidelity to Correction 1's text
          and documented it as a specification-fidelity guard.  Keep, or remove for
          single authority?  I do not have a strong view.
        ONE PROPOSAL, deliberately NOT for the same turn:
          run the replay gate once immediately before authorizing the 168 rollouts.

CLOSED  CODEX S55 APPROVED ALL FOUR S55-CORRECTED FILES AT MY EXACT BLOBS.
        Do not re-review, do not re-derive, do not re-ask:
          APPROVE_CORRECTED_PROTOCOL_P_DRIVER_EXACT_STATE_AS_IS
          ACCEPT_UNSAFE_STAGE_C_REPLICATE_AS_A_DRIVER_SIDE_FAIL_CLOSED_LABEL
          NO_PROTOCOL_P_SPECIFICATION_BUMP
          FOUR_FILE_REVIEW_LOOP_CLOSED_AT_SAME_STATE
        Its verification: four blobs exact, full suite 938 passed in 112.07 s,
        compileall clean, zero rollouts, Stage 0 unchanged, config.json absent.
        APPROVED BLOBS (two of the four are now SUPERSEDED by my S56 edits):
          scripts/utils/protocol_p_results.py  e84e5f9f4e6d10408873d87b81b2baef9535d50e  UNTOUCHED IN S56
          tests/test_protocol_p_results.py     cbac30ed3d41c961f7d5c54c306c8a09fa1be1cd  UNTOUCHED IN S56
          scripts/run_protocol_p_screen.py     99e2d44744eaf7ecd2bda1a21acce1ec9ce435c4  SUPERSEDED S56
          tests/test_protocol_p_driver.py      3f1a81067116f2815f8680e6307e15e06c629db6  SUPERSEDED S56
CLOSED  Codex's S54 acceptances, still in force -- do not re-ask:
          `--mode plan` as the default is right;
          the driver's imports of coefficient_vector / sensor_config_from_document /
            verify_text_pins from the Stage-0 script are FINE until a THIRD consumer;
          the origin-provenance reuse rule is APPROVED IN SUBSTANCE.
CLOSED  README.md (root, the public Live-Run log).  Settled.  I appended a NEW entry in
        S54, S55 and S56 (+2/-0 each); Codex appended one in its S55; no dated entry
        has ever been edited by either agent.
CLOSED  Stage-0 result artifact    blob 31c1e6d1824c10bd5978d12c377f76cf556af03f
CLOSED  Progress Report Session 48 blob f01aa7d7b56b9b30e8279bc221a5f0e60613ab3f
JOINTLY APPROVED ACROSS THE S51/S52/S53 ROUNDS -- do not re-review, do not edit:
        scripts/utils/protocol_p.py                 8d9005250769b85739e5be4ddf00280f46acf71c
        scripts/protocol_p_replay_gate.py           c6b1674990a46f097a942559fd9077041d8270de
        scripts/analyze_synchronous_difference_null.py
                                                    f104971d426af95ca664826cbc276228adff7963
        Reproducibility Packet/README.md (Step 24)  ba9c067a4d7ccce4b6c29edcf588b7eeb0e8150e
        scripts/utils/protocol_p_conditions.py      7fdddf0eee5e3b3f02b2db21ecb1b70728234be5
        tests/test_protocol_p_shared.py             f505877f81b0f3f6a13a3d2b57e9ea5f5b2ad367  20 tests
        tests/test_protocol_p_conditions.py         1874773e1ee8ed41bb763ca3a8a235d89e7c02e9  135 collected
```

## THE S56 SESSION — the pre-registered helper, and the tautology it dissolves

**THE ONE FACT TO CARRY ABOVE ALL OTHERS: `require_constructed_condition` inside
`build_overrides` could never fail, and the fix was a function the pre-registration had
already named by signature and that had never been implemented under that name.**

Protocol P Correction 1 names `screen_physical_faults(condition, trajectory, *,
severity=None, control_dt_s)` and calls three of its properties deliberate. The behaviour
existed, split between `derive_screen_timing` (derives the onset once into `ScreenTiming`)
and `requested_fault_specs` (builds the tuple from an onset it is *given*). Because the
construction layer's check receives the same onset the builder received, both sides share a
derivation and no input can make them disagree — limitation 52, which I recorded in S52 and
did not solve. **The pre-registered signature IS the solution: it takes a trajectory
document and no onset.**

```text
NEW IN THE DRIVER (all four are mine, all under review):
  screen_onset_index(trajectory, *, control_dt_s) -> int
      derives the onset FROM THE DOCUMENT via _step_index; translates
      AssignmentGenerationError into ProtocolPError("I13a: ...off-grid").
      DELIBERATELY does not consult ScreenTiming -- a check that re-derives from the
      cached object it is checking cannot fail.  Same shape as the tautology, one down.
  screen_physical_faults(condition, trajectory, *, severity=None, control_dt_s)
      Correction 1's helper at Correction 1's signature.  Validates the closed
      vocabulary, derives the onset, DELEGATES the tuple to requested_fault_specs.
  require_preregistered_faults(constructed, condition, *, severity, trajectory,
                               control_dt_s)
      compares what WILL BE STAMPED against the document-derived expectation, field by
      field, type-strict.  Called in run_logical_row AFTER build_overrides and BEFORE
      execute -> runs on exactly the 168 physical rollouts, on none of the 12 reuses.
  packet_relative_input_path(path) -> str      (the scope deviation, below)
  SCREEN_CONDITIONS = CONDITIONS   (an ALIAS import, not a second definition)
```

**THE DEMONSTRATION — one process, zero rollouts, real committed assignment:**

```text
screen_onset_index        500 == derive_screen_timing's 500 == _step_index(1.0, 0.002)
helper output == the stamped bundle for healthy / structural 0.75 / structural 0.35
INJECT the Correction-1 defect: build_overrides(..., onset_index=0)
  build_overrides                              ACCEPTED   stamped onset_index = 0
  require_constructed_condition(..., 0)        ACCEPTED   <- limitation 52, MEASURED
  require_preregistered_faults(..., document)  REFUSED
    "I13a: the bundle's physical_faults[0].onset_index is 0 (int); the onset derived
     from 'trajectory_dev_diagnostic_b' requires 500 (int)"
Correction 1's properties, each refused: 'structual' / no severity / healthy+0.5 /
  0.0 / -0.1 / 1.5 / nan / inf ; ACCEPTED at 1.0 (closed top) and 0.05 (ladder bottom);
  positional severity -> TypeError ; onset_time_s=1.0001 -> refused off-grid, not rounded
```

**THREE THINGS I DECLARED RATHER THAN LET CODEX FIND — carry all three:**

1. **The field half of the comparison is NOT live.** The helper delegates to
   `requested_fault_specs`, so both sides share one authority for the fields and cancel.
   **What is live is the ONSET and the condition/severity routing.** Docstring says so.
   The binding between the constructed fields and Correction 1's literals is a TEST that
   quotes the spec (`test_the_preregistered_helper_builds_correction_1s_exact_fault`),
   not a second copy in production. **No write-up may say the driver independently
   verifies the fault's fields.**
2. **The helper's closed-vocabulary check is REDUNDANT** — `requested_fault_specs` refuses
   an unknown condition independently. Kept for fidelity to Correction 1's text, docstring
   says it is a specification-fidelity guard and must not be counted as coverage.
   **EIGHTH MEMBER OF THE CLASS** (37, 39, 43, 49×2, 51, 55, 59).
3. **`screen_onset_index` does not read `ScreenTiming`,** on purpose, and that is stated.

### THE S56 SCOPE DEVIATION — a machine path inside a results artifact

**Found by RUNNING the program and reading the file it writes, not by reading the code.**

```text
inputs.config_path was  "C:\Users\cresp\Documents\Dandelion Engineering\Robot Structural
                         Proprioception\Reproducibility Packet\config\draft-config-v0.1.json"
the sibling Stage-0 artifact records NO absolute path at all -- its inputs are
  assignment_canonical_sha256 / assignment_hash / base_config_hash / cli, and a grep for
  a drive letter over the committed file returns 0.
FIXED  packet_relative_input_path -> "config/draft-config-v0.1.json"; the out-of-packet
       branch records "<outside the packet root: NAME>" -- the NAME, never the location.
       Nothing is lost: base_config_hash in the same block identifies the document.
VERIFIED  the whole plan artifact now contains no drive letter.
```
**Codex named two items (Step 25 and `screen_physical_faults`); this is a third and I led
the handoff with it (Lesson 38).**

### THE S56 TEST DEFECT I FOUND BY READING, BEFORE THE SWEEP

```text
"the vocabulary is closed"   run_protocol_p_screen.py:400  AND
                             protocol_p_conditions.py:374
```
My new test matched that phrase, so deleting the driver's check would have left it green.
Now matches `"unknown screen condition"`, unique to one raise site. **LESSON 59 RECURRING
IN THE FIRST SESSION AFTER I WROTE IT DOWN.** Its sharpened form: **when you add a guard
that duplicates an existing one, the duplicate's MESSAGE is the thing most likely to be
non-distinguishing, because you wrote it to say the same thing.**

### THE S56 MUTATION SWEEP — ```text
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

### THE S56 MEASUREMENT CORRECTIONS — both were carried, unmeasured, until now

```text
plan-mode elapsed   0.30 / 0.30 / 0.33 s   three subprocess-timed runs
                    THIS SUMMARY HAS CARRIED "~10 s" SINCE S54.  Never measured.
full-run estimate   168 x ~26 s = roughly 70-80 min, and Step 25 LABELS it an
                    extrapolation from one measured rollout, not a recorded runtime.
mujoco import       TRUE on an import-only load of the DRIVER (it imports
                    assignment_generator -> cable_plant).  Step 25 says "no MuJoCo
                    *simulation*" and states the package IS imported, in explicit
                    contrast with Step 24, whose script imports none.  Limitation 47.
```

### PACKET README STEP 25 — written in S56

Deferred in S54 and S55 on the stated ground that a runbook step describes something a
reader can rely on and an unreviewed script is not that; Codex's approval removed the
objection. Documents `--mode plan` ONLY. States that Stages A/B/C have not been run and
that no result artifact from them is distributed. Prints the audited plan (9 candidates,
180 logical rows, 168 physical rollouts, 12 reuses, onset 500, window `[1000, 1768)`) and
carries the 180-vs-168 explanation in outsider language. **Outsider-clean: no agent, no
session, no review history** (`Playbooks/reproducibility-packet.md` lines 39/53/63).

**Deliberately not done in S56:** no rollout of any kind; did NOT re-execute Stage 0; did
NOT run the replay gate (nothing on its watched path changed — and see the proposal above);
**did not touch `protocol_p_results.py` or `test_protocol_p_results.py`** (byte-identical to
Codex's approved blobs); did not touch the protocol file, the assignment, the draft config,
the Stage-0 artifact, the seam, `utils/gauge_windows.py`, the detection-floor screen,
`.gitattributes`, or any payload; did not edit any dated public-log entry; no new
dependency; **no result artifact written into the repo** (plan output went to the
scratchpad); did not build `screen_physical_faults` into the construction layer (Codex
ruled in its S43 that **the driver owns it** — chat line 9280).

## THE S55 SESSION — Codex blocked my S54 build on THREE findings. ALL THREE WERE REAL.

**THE ONE FACT TO CARRY: the full 906-test suite was GREEN while two of the three defects
were live.** Codex found them by driving the whole driver end to end through states my
tests never put it in, with synthetic bodies and no physics engine. **I reproduced every
finding by construction before changing a line, and my numbers matched its numbers.**

```text
F1  A MIXED STAGE-A DROP ABORTED AFTER SPENDING VALID LATER WORK.  73 rollouts spent,
    all 73 thrown away at the last step, because executed_rows was defined as "rows of
    SURVIVING candidates".  The all-dropped terminal returned drop summaries only.
F2  STAGE-B AND STAGE-C GATE FAILURES WERE MEASURED, THEN IGNORED.  run_logical_row
    computed a GateReport for EVERY rollout in every stage; run_reuse_aware_rows
    DISCARDED it.  A saturated remEI-0.40 body reported TESTABLE inside CASE_A;
    §9's UNSAFE_LADDER_VALUE branch was UNREACHABLE.  Stage C is the worse half -- a
    gate-failing healthy replicate went straight into Q95_c, the only operative null.
F3  THE PERSISTED RESULT WAS NOT AN I12 AUDIT RECORD -- no gate report, no n_steps,
    no elapsed_s, so no reader could have audited F1 or F2 from the artifact.
```

**THE FIXES — carry the shapes, read the files for the code:**

```text
F1  run_stage_a returns "measured_rows" -- every row it called run_logical_row on.
    THE PRINCIPLE: the function that RAN the rows is the one that says which rows ran.
    _executed_rows(rows, measured_stage_a) refuses a measured row absent from the
    inventory built at the selected candidate.  After: terminal None, 73 calls, 85 rows.
F2  run_reuse_aware_rows returns {"retained_plants", "unsafe"}.  build_ladder_table reads
    each fault-side body's gate_report FROM THE LEDGER; a failing cell gets
    UNSAFE_LADDER_VALUE and margin=None.  unsafe_ladder_values() is separate, and
    classify_outcome() RAISES on a table still holding one.  A failing Stage-C replicate
    terminates BEFORE stage_c_null is reached.
    THE TWO REUSED LADDER VALUES (0.75, 0.35) READ THE SAME GUARD BUT ARE FORCED TO PASS
    -- a candidate only survives Stage A with all twelve rows clean.  Only EIGHT of the
    ten are live.  Do NOT count those two as coverage.
F3  ledger_report(ledger) -> 168 entries: physical key, cell, stage_of_origin,
    origin_row_key, stamp, canonical payload, coefficients, the FULL gate report,
    n_steps, elapsed_s.  Rows CITE it via rollout_provenance.  I TOOK CODEX'S SECOND
    OPTION (a ledger the rows cite) NOT THE FIRST (copy into each row): a second copy is
    a SECOND AUTHORITY.  _with_measured_evidence() attaches evidence on EVERY exit path.
```

**SECTION 9's NO_ADMISSIBLE_PROBE SUB-BRANCHES ARE IMPLEMENTED** in
`classify_no_admissible_probe`, keyed to `REFERENCE_CANDIDATE = (0.05, 0.5)`:
healthy-or-remEI-0.75 failure → `IMPLEMENTATION_INTEGRITY` with an explicit
`defect_localization_claim: null`; failure only at the ladder bottom →
`PHYSICAL_SAFETY_OR_METHOD_LIMIT`; anything else → `RECORDED_ONLY_CLASSIFIES_NOTHING`.
**The fenced branch REPORTS its precondition rather than asserting it** — I13a named as
asserted by the construction layer before the rollout, I13b named as
`tests/test_cable_plant_softening_boundary.py`, **which the script does not run.**

**S55 sweep: 32 cases across two passes, 32 of 32 caught.** One real survivor in pass 1
(`section_9_branch_not_computed` — all three sub-branch tests called the classifier
directly, so deleting the driver's CALL SITE left them green; **third instance of that
shape**, so I swept every comparable call site and found one more). One BAD ANCHOR
(matched twice, produced no verdict) — **a bad anchor is not a survivor; never report one
as a gap.** Both fixes were TESTS, not production changes.

## THE S54 SESSION — the driver and the results layer were BUILT

**THE KEY DESIGN FACT — carry this verbatim.** `PhysicalKey` is
`(sensor_seed, pair_id, condition, severity, peak, ramp)`. **`stage` is DELIBERATELY NOT IN
IT**, and a test asserts that, because including it is exactly what makes the 12 reuses
vanish and 12 phantom stamps appear. A reused row carries `reused_from` = the origin
**Stage-A row key**, never reaches `run_logical_row` (which refuses a reused row outright),
and reads provenance only through `resolve_row_provenance`, which refuses a cited entry
whose `stage_of_origin` is not "A".

**THE DECLARED-VS-COMPUTED CHECK.** `require_inventory_shape` compares the **declared**
reuse set against the **computed** set of rows whose body was already measured; both
directions refused. Reaching it needs a **count-preserving** mutation.

**THE CENSUS IS DERIVED AND PINNED, NOT ONE OR THE OTHER.** `expected_counts(n)` derives
`12n + 72` logical / `12n + 60` physical / 12 reused and reconciles with the pinned totals
**by equality at `PRE_REGISTERED_CANDIDATE_COUNT` only**.

**PLAN MODE, verified against the real committed inputs:**
```text
admissible candidates 9    logical rows 180    physical rollouts 168    reused rows 12
derived onset index 500    window [1000, 1768)    rows_by_stage A 108 B 40 C 32
config.json absent.  `--mode plan` is the DEFAULT; `--mode execute` runs the screen.
```

**S54 sweep: 58 cases, 52 caught, 6 survivors, 5 real.** The two sharpest:
`severity_normalisation_removed` (**my test verified a property of PYTHON, not of my code**
— `1 == 1.0` and `hash(1) == hash(1.0)`, so the key deduplicated either way; narrowed to
assert the recorded TYPE) and `probe_torque_gate_call_site_removed` (**a real wire gap** —
the gate had a direct test, nothing tested that the driver REACHED it; having found one I
looked for the class and `require_derived_onset` had the identical gap). The sixth survivor
(`physical_body_count_check_removed`) is **arithmetic**: once row keys are unique the
distinct-body count is forced. Line kept, docstring says why.

## S53 — the inventory dry-run, and the reuse/stamp hazard (SETTLED)

**THE HAZARD — ONE BODY, TWO ADMISSIBLE STAMPS.** `stage` is inside the hashed payload and
`stage_c_identity(c, 0)` IS the Stage-A/B identity by design:
```text
cell 4  Stage-A healthy identity  (150002, 'basepair_protocolp_stageAB_c4')
cell 4  Stage-C k=0    identity   (150002, 'basepair_protocolp_stageAB_c4')   IDENTICAL
stage='A'  dev-d732ceb4ff2a8bc6a42932ff567586ea6d0c32afafe57aecbef9028db82e1892
stage='C'  dev-31089076be232e32b089ab21d44532183fe2b0c5ac4a1361e4c94a529a9339ca
```
**RULED BY CODEX S53: a reused row CITES the original rollout's stamp.** Implemented S54,
approved S55. The dry-run also pinned: 180 rows → 168 distinct physical runs (matches
§8's 108 + 32 + 28), 180 distinct stamps, 0 collisions, seed band `[150002, 157032]`,
no overlap with the dev band `[110000, 111514)`.

## Escalation trigger — content-based, and it has now held eight times

**The binding rule: escalate to the director when a round re-litigates a point already
settled, or when we disagree on a judgment neither of us can resolve from source — NOT
when a round finds a new, verifiable defect.** Every loop to date closed on new findings:
the specification loop (seven rounds), the seam (one), the replay gate (two), Stage-0
implementation (three), the Stage-0 result, the progress report, Step 24 (one), the public
log (four turns, each finding a NEW false claim), the extraction and construction layer
(two each), and **the driver (two rounds: blocked S54, corrected S55, approved S55)**.
**If a round re-opens the two-domain hashing split, the window origin, the statistic, the
ladder, the driver-vs-seam boundary, the S45/S46 answers, the S47 reachability closure, the
S49 identity-scope narrowing, or the S55 Stage-C label ruling — escalate on the spot
regardless of count.**

## HONEST ODDS — unchanged since S40

Against the S39 gauge-only measurement's bar, projecting the S35 amplitude ratio ×3.15 over
0.05 → 0.15 N (**importing that ratio across configurations remains the weakest link — the
exact Lesson-11/12 move**):

```text
remEI 0.50   c4 1.502 vs 0.711 x2.11    remEI 0.75   c4 0.491 vs 0.711 x0.69
             c5 1.475 vs 0.850 x1.74                 c5 0.470 vs 0.850 x0.55
             c6 0.856 vs 0.635 x1.35                 c6 0.315 vs 0.635 x0.50
             c7 0.853 vs 0.771 x1.11                 c7 0.294 vs 0.771 x0.38
```

**remEI 0.75 fails everywhere by a wide margin — the one robust statement.** remEI 0.50
clears the binding cell by only **1.11×**, computed with an **inflated signal** (Finding L)
against a **deflated bar** (the gauge-only decomposition omits closed-loop divergence) —
both errors favour the hypothesis. **Case B (dev coverage 1) and Case C remain roughly
comparable.** Stage C settles it.

**The success bar is UNTOUCHED** (≥0.05 macro-F1, −0.02 per-class recall non-inferiority,
≥10% tracking reduction, paired hierarchical bootstrap, ≥5 seeds).

*Naming note: "M2" is **retired inside the protocol file**. Below it still labels **my** S39
measurement — the gauge-path-only decomposition. If writing anything Codex will read, spell
it out.*

## The two zero-rollout measurements from S39 (still valid)

**M1 — the observed path barely degrades a MATCHED difference.** Both delivered plant traces
of a pair re-observed at ONE common identity, 6 identities.
```text
setting        cell   D_true   D_obs mean   ratio        setting     cell  D_true  D_obs mean  ratio
remEI 0.50      4     0.4787     0.4768     0.996        remEI 0.75    4   0.1584    0.1559   0.984
remEI 0.50      5     0.4755     0.4683     0.985        remEI 0.75    5   0.1593    0.1492   0.937
remEI 0.50      6     0.2755     0.2717     0.986        remEI 0.75    6   0.0872    0.1001   1.148
remEI 0.50      7     0.2798     0.2709     0.968        remEI 0.75    7   0.0968    0.0934   0.965
```
**0–6% cost on average, ±10% spread; at small `D` the residue moves EITHER way.**

**M2 — the gauge-path-only component of the Stage-C null.** One delivered healthy plant trace
per cell held EXACTLY fixed, redrawn at 8 identities, all 28 within-cell distances,
`method="higher"`.
```text
cell   min / median / max           Q95 (27th of 28)   2*Q95
 4     0.1540  0.2807  0.3731            0.3555        0.7110
 5     0.1524  0.2620  0.4325            0.4251        0.8502
 6     0.1377  0.2709  0.3922            0.3176        0.6351
 7     0.1443  0.2983  0.4706            0.3854        0.7708
```
**A decomposition, NOT a bound.** It **validates Stage 0** (the synthetic no-plant value sits
inside the real-plant 0.318–0.425) and identifies **cell 7 (payload + warm + contact) as the
binding cell**. **Conditional healthy-null diagnostic only — no mechanism attribution.**

**The enabling tool (S39, reconfirmed S40/S41/S45/S46).**
`SensorModel().observe(delivered_plant, "S", pair_id=<manifest>, sensor_seed=<manifest>)`
reproduces the delivered row **bit-for-bit without running any simulation**; a perturbed
`pair_id` moves `gauge_obs` by up to **6.50 µε** (against `D` of order 0.1–0.5). **Any stored
plant trace can be re-drawn on the observed path at any identity for free.**

## THE STAGE-0 RESULT — the project's first pre-registered measurement (RAN S48, APPROVED S49)

Ran once, at the pinned invocation, all seven values also being the defaults. **Zero rollouts.**
```text
n pairs 100 (sensor_seeds 0..199 consumed once, consecutive pairing)   pair_id = 1
mean 0.278734   std 0.074773 (POPULATION)   min 0.114994   median 0.279701   max 0.569876
q95_method_higher  0.400881        <- THE reported statistic
identity  dev-71b332893d007036625f666589f8c74b0ac3b946b47b5186ddf8de6a2d8ce31e
I8 PASS.  artifact: Reproducibility Packet/results/protocol_p/sensor_only_difference_null.json
```
**CORROBORATION HOLDS BUT IS UPPER-TAIL — state it this way every time:**
```text
real-plant per-cell Q95   c6 0.3176   c4 0.3555   c7 0.3854   c5 0.4251
Stage 0                                              0.400881
```
It **exceeds three of the four cells**, below only c5, ~5.7% headroom. "Inside the range" is
TRUE and is the pre-registered claim. **"Agrees with the real-plant null" is NOT supported.**
`corroboration.authority` is `"NONE"`. The operative null remains Stage C's `Q95_c`.

**SELF-AUDIT FACTS:** 100 distances recorded; Q95 and mean recompute bit-identically under
NumPy; the identity reproduces as `dev-` + sha256 of the artifact's own 650-char
`stage_0_canonical`; the first two distances (`0.17764883`, `0.18949149`) reproduce the S47
sensor-config control exactly. `count > q95 = 4`, `count >= q95 = 5`. **`samples` is a 6-key
METADATA DICT** — `len()` returns 6, not 100. Check the type before reporting an alarm.

## GATE STATUS — the freeze path (central reference)

**Governing decision: `BLOCK_CONFIG_FREEZE_PENDING_PRECONFIRMATORY_BUILD_AND_VALIDATION`.** A
**versioned DRAFT config** governs dev/val generation; the **final immutable `config.json`
freeze comes AFTER model implementation + validation-only hyperparameter/threshold selection
and BEFORE any untouched `test` payload.**

1. **Machine schema + config authority** — **DONE, APPROVED S28.** *(Codex/shared.)*
2. **Role-separated storage, deployable loader, leakage/split audits** — foundation DONE (S28), role-write DONE (S29), **real generator + base roles APPROVED (my S33)**, **generator hardening APPROVED (my S34)**. **STILL OPEN OVERALL:** `estimator_outputs` + `controller_logs` roles await the Gate-4 fits. *(Codex/shared.)*
3. **Multi-setting design + manifest** — was CLOSED at 808 reservations; **A2 reopens it** (full regeneration, new assignment, new hash). *(shared)*
4. **Matched learned models** — **MINE. GATED BY Protocol P v2.3.3, then the written A2.** `TemporalAttributionNet` + `RMALatentEncoder` behind shared `[W,D]`; within-suite capacity ladder; ≥5 seeds; identical protocol IDs across C0/C1/S. Toolchain verified (torch cu128 / sm_120).
5. **Calibration/abstention/OOD/uncertainty** — **MINE.** Per-suite calibrated probs (Brier/NLL/ECE), abstention + OOD thresholds on validation, `severity_uncertainty` as a **bias-inclusive predictive error scale** (NOT in-sample residual dispersion — S24: understates true by 5.72× for S). **Validation must NOT be touched until Gate 4 opens.**
6. **Confirmatory controller protocol** — **DECIDED S27 (both agents):** freeze the fair four-arm comparison (no-action/detection-only · transparent attribution-driven · RMA · oracle) and **RUN the pre-registered paired C1-vs-S comparison**; do NOT narrow to information-only, do NOT retune blocked families post-hoc. *(Codex owns controller; diagnosis→control seam shared.)*
7. **Evaluation driver + confirmatory manifest** — **MINE.** One CLI owning the `[t_c,t_c+5s]` slice, role joins, paired C1/S table, exclusions, CIs; rejects `dev-`/wrong-hash/cross-role/incomplete-pair/truncated. **Must implement the pre-registered statements (a)–(y) carried below.**

**The (a)–(y) driver requirements, carried verbatim in shape:** (a) `ood_flag` exclusion from known-class metrics; (b) the **degradation-ladder rule** (S30/S31); (c) **pilot→val moves one variable while val→test additionally moves half-fraction → complete factorial** — *and, under A2 pin 4, no longer moves the contact window*; (d) S33's two findings; (e) the mild-stratum development diagnostic **at its true scope** and the per-channel attribution; (f) **[S35]** the excitation discontinuity; (g) **[S36]** the yardstick discontinuity (D) + the run-to-run range statement (E) + trajectory-partial margin coverage; (h) **[S37]** the operation mismatch (F), thermal near-invariance (G) as a *property*, the amplitude ceiling (H); (i) **[S38]** the **window origin (J)** — the driver MUST use the same origin the protocol pins — plus the matched/unmatched asymmetry and role-coverage counts; (j) **[S39]** the **construction path (K)** and the **unmatched-identity confound (L)**; (k) **[S40]** distinguish **`base_pair_id` from realized `pair_id`** in every identity join, and never stamp an overridden run with the base config hash; (l) **[S41]** any file whose **raw bytes** enter an identity must be hashed through the correct-domain helper; (m) **[S42]** that helper must be chosen **by file domain**; (n) **[S43]** every identity expression must **name the object it hashes**; (o) **[S44]** test the **wires between stages**, not only each stage; (p) **[S45]** every clean report must **disclose its denominator** and refuse to report when it cannot support the claim; (q) **[S46]** every guard must be **reachable from the construction that will run**, and every fixture large enough for the defect it exposes; (r) **[S47]** every pinned literal that also lives in a bound document is checked by EQUALITY, never adoption; (s) **[S48]** every test that claims to verify a gate must CALL it and assert the REASON for a refusal; (t) **[S50]** every documented dependency must be verified against the running system; (u) **[S51]** assert a phrase UNIQUE TO ONE RAISE SITE, and construct preconditions through `utils/protocol_p_conditions.py`; (v) **[S52]** obtain the source reservation from the I1-pinned assignment and never construct one, and test per BRANCH not per guard; (w) **[S53]** record a REUSED row's provenance by CITATION, and DERIVE the fault onset; (x) **[S54]** key the results table on the PHYSICAL BODY, and make every clean-census check reachable from a state that could fail it; (y) **[S55]** derive the reported set from what was MEASURED rather than from which candidates survived, CONSUME the hard-gate report in EVERY stage, and persist the gate evidence, step count and elapsed time on EVERY exit path including terminals. **(z) [NEW S56] every check the driver makes must be given a source INDEPENDENT of the thing it checks — a comparison whose two sides are produced by the same function from the same arguments is a report of a check rather than a check — and no result artifact may record an absolute filesystem path, because a machine path identifies nothing that the artifact's own hashes do not identify better and it makes two identical reproductions differ.**

**Order:** (1)✓ → (2 foundation)✓ → (2 role-write)✓ → (3 assignment)✓✓ → (2 generator + base roles)✓✓ → (2 hardening)✓✓ → (dev separability check)✓ **[NEGATIVE]** → Protocol P v2.3.3 spec ✓✓ → seam + 37 tests ✓✓ → replay gate ✓✓ → Stage-0 implementation ✓✓ → **Stage 0 RAN, S48, Q95 0.400881, zero rollouts ✓** → Stage-0 result ✓✓ → Progress Report S48 ✓✓ → packet Step 24 ✓✓ → public README ✓✓ → extraction + construction layer ✓✓ (S51–S53) → **S54 BUILD: driver + results layer + 156 tests** → **Codex S54: three BLOCKING findings** → **my S55: all three confirmed by construction and corrected, 32 tests, 32/32 sweep** → **Codex S55: ALL FOUR APPROVED AT EXACT BLOBS, Stage-C label accepted, loop CLOSED ✓✓** → **my S56: `screen_physical_faults` implemented at Correction 1's signature, the tautological I13a comparison made LIVE, the machine path removed from the artifact, packet Step 25 written, 37 tests (938 → 975), 17-case sweep ← WE ARE HERE** → Codex reviews three states → **EXECUTION-AUTHORIZATION DECISION (separate, explicit)** → replay gate immediately before → **Stages A/B/C, 168 rollouts, ~70–80 min** → Codex reviews result + branch → written amendment A2 + replacement assignment (both approve) → **full regeneration from zero** → re-audit → (4/5 models+calibration) [me] → (2 remaining roles) [Codex] → (6 controller + sample-size) [shared] → **joint immutable freeze** → one-shot confirmatory generation + eval (7) → Phase 3.

Not freeze blockers (still required before completion): Slot-8 verification artifact; Technical Report / Accessible Piece / Study Guide Pass 2 (Phase 3); fresh-environment packet validation.

## The delivered dataset — layout and how to read it

`data/gate3-base-dev-pilot-val-c1-s/` (git-ignored). **Slated for supersession under A2 — read it, do not build on it.**
```text
manifest.csv        945 lines (header + 944 rows)
plant/              945 files (index.csv + 944 npz)   2.8 GB  <- half is duplicate (documented)
labels/             945 files                          4.4 MB
observations/C1/    473 files (index.csv + 472 npz)
observations/S/     473 files                          835 MB total
generation_audit.json · independent_audit.json
```
- **Generated with `splits=("dev","pilot","val")`, `suites=("C1","S")`** — pass these explicitly to `build_identity_manifest`, whose *default* suites are `("C0","C1","S")` and which **requires `{"C1","S"} ⊆ suites`**. `_generate_reservation` has no such constraint and accepts `("S",)`, which is what §4 pins.
- **Manifest columns** (= `IdentityManifestRow` fields, 20): `schema_version, config_hash, scenario_spec_id, pair_id, run_id, trajectory_spec_id, fault_setting_id, split_group_id, split, suite, estimator_id, controller_id, payload_id, env_profile_id, contact_profile_id, sim_seed, fault_seed, sensor_seed, controller_seed, train_seed`. **Note `trajectory_spec_id`, not `trajectory_id`; `fault_setting_id`, not `source_class`. `pair_id` here is the REALIZED id (with `_dataset0`), not `base_pair_id`.**
- **`run_id` carries the suite:** `scenario_dev_t01_f000_r00_S_dataset0`. The **plant** role is stored per suite too (C1 and S share a byte-identical payload — documented duplication), so a plant path is `plant/{run_id}.npz` with the suite suffix included.
- **Load one observation:** `ObservedRecord.load_npz(root/"observations"/suite/f"{run_id}.npz")`. **`values` and `valid_mask` are DICTs** channel → `[T, width]`. **`measurement_time_s` / `availability_time_s` / `latency_age_s` are DICTs of RANK-1 `[T]` arrays.** Gauges are `values["gauge_obs"]` `[T,4]`. **`config_hash` is a STORED field.**
- **`ObservedRecord.to_npz_dict()` is the 38-entry serializer.** **`_plant_payload(record)` is the 20-key plant serializer** — use it rather than re-deriving. **Codex's S45 answer: keep that import private.**
- **Re-observe any plant trace offline, no simulation:** `SensorModel().observe(plant, "S", pair_id=..., sensor_seed=..., fault=None, run_id=..., config_hash=..., split=...)` — verified bit-identical at the manifest identity (S39/S40), suite-order-independent (S45).
- **These `.npz` are ZIP archives and DO contain CRLF byte pairs as payload. Never hash one through a text canonicalizer.**
- **Plant fields (20):** step, t_s, q_true, qd_true, qdd_true, tau_cmd, tau_delivered_true, deform_coords[90], curvature_true[4], gauge_true[4], imu_true[6], temperature_true[4], contact_state[2], task_reference, true_task_output, tracking_error, tracking_error_norm, control_effort, saturation_flag[2], safety_flag[7]. **`contact_state[:,0]` = summed force N, `[:,1]` = active flag.**
- **Registry D = 18:** q_obs[2], qd_obs[2], tau_cmd[2], current_proxy_obs[2], imu_obs[6], gauge_obs[4]. **C1's `gauge_obs` is all-NaN, mask False. S `gauge_obs` CONTAINS NaNs — use nan-aware statistics.** Measured S45 on one delivered S row: **531 NaN values across 5 of the 38 entries.**
- **Label fields:** source_class, subtype, location, severity, onset_index, onset_time_s, compound_flag, ood_flag.
- **Run lengths / timing:** `trajectory_dev_ordinary_a` (`t00`) 2900 steps, onset 400, **no probe**; `trajectory_dev_diagnostic_b` (`t01`) 3000 steps, onset 500, **probe steps 1000→1625**. Both carry 76 rows per suite. **Only `t01` has a probe.**
- **`assignment["trajectory_specs"]` is a LIST of dicts keyed by `"id"`, not a dict.** Same for `context_profiles`, whose keys are `payloads` / `environments` / `contacts`.
- **dev fault settings (t01):** `fault_dev_healthy` (f000); `fault_dev_structure_link_stiffness_loss_loc1_sev0p5` (f001); `..._sev0p75` (f002); then actuator loc0/loc1 × {0.5,0.75}; then sensor bias/drift/dropout × loc{0,1} × 2 sev. **Severity strings use `sev0p05`, not `sev0p5`, for 0.05 — query the assignment, do not recall it.**
- **The replayed reference row:** `scenario_dev_t01_f000_r00` → `pair_id basepair_dev_t01_f000_r00_dataset0`, `run_id scenario_dev_t01_f000_r00_S_dataset0`, `sim/fault/sensor/controller = 110760/110761/110762/110763`, 3000 steps, 0 safety events, **0 contact steps**.
- **Two runs in the same context cell differ in sensor_seed, and the closed loop amplifies that into gauge variation that EXCEEDS the structural fault signature (S36 Finding E).** Any fault-effect *magnitude* measurement MUST match both `sensor_seed` AND realized `pair_id`. Separability measurement must NOT. **Delivered fault and healthy rows do NOT share identity (S39 Finding L).**

## Codex's Gate-1/2/3 layer — reference

`Reproducibility Packet/`:
- **`schema/schema.json`** (S28) — machine schema v1.0 + A1. Roles: identity_manifest, plant (20 fields), observations (fixed 6-channel registry + static suite mask), labels (8), estimator_outputs (9), controller_logs (6). `schema_sha256 = 0dae0dd0fec4269180139efc9a4c9ce38e7f8f23d890d182dc8eb063803e942f` (LF-pinned via root `.gitattributes`).
- **A1 safety envelope:** `|q| ≤ π rad`, `|qd| ≤ 10 rad/s`, tip radius ≤ 0.82 m, `|gauge_true| ≤ 500 µε`, tip contact force ≤ 5 N; `safety_flag[T,7]` fixed order computed in `cable_plant.py:_safety_flags`; `saturation_flag[T,2]` separate. Computed from privileged truth, never from a corrupted observed channel.
- **`config/draft-config-v0.1.json`** — the DRAFT, **CRLF in the working tree**. **`config_hash = dev-712abf27c3f8f3c331ae9b76e3f22c48857334cc15a81e819718165e47753e56`** (parent `dev-0211f2e7…`), computed over `canonical_json_bytes(document)` so it is EOL-immune — **which is why it is deliberately NOT byte-pinned**. Frozen candidates: plant (`n_def=90`, gauges [0.25,0.75], A1 thresholds, `point_count_per_link=17`, `simulation_timestep_s=1e-4`, `endpoint_contact_plane_z_m=0.2`), timing (`f_ctrl=500`, `control_dt_s=0.002`, `window_steps=768`, `stride=16`, **probe 0.05 N / 0.8 Hz / 1 cyc raised_cosine — RAMP UNPINNED, S35 Finding A**, `analysis_window_s=5.0`), sensor_model (**gauge noise 1.0 µε, thermal 10 µε/°C, ref 25 °C, bias 0.5 µε, drift 0.2 µε/√s, hysteresis 0.15, quant 0.5 µε, latency 0.002 s**).
- **`config/proposed-gate3-assignment-v0.1.json`** — **LF-pinned (S41)**. Canonical/raw SHA-256 `76255a8089f3e27d893b26d981cbf50e808bd75ba518c44b55c4635ec83514ae` (22,760 bytes); **its CRLF rendering is `00dacaf6…`** — always hash through `canonical_text_sha256`. `assignment_hash = dev-eec59ec8a296a9a4ff4909f8e7f1de91a0a8f4bf289ae1533a427d1a87bc33f1`. **Superseded, never approve:** `dev-70832daa…765de` and `dev-5939ff5f…0cedb`. Probe `start_offset_s` per split: **dev 1.0, pilot 1.2, val 0.9, test 1.1 — offsets FROM ONSET (Finding J).**
- **`scripts/utils/assignment_binding.py`** — `validate_approved_assignment_binding(config, *, expected_assignment)` — **`expected_assignment` is REQUIRED.** Its **`.assignment_hash` property** is the document-derived `dev-eec59ec8…`. `AUTHORIZED_RESEARCH_SPLITS = ("dev","pilot","val")`.
- **`scripts/utils/assignment_generator.py`** — the S44 seam at the top: **`ScreenOverrides` (frozen, 5 fields, `is_active()`), `screen_pair_id` (105), `_screen_stamped_hash` (122)**; **`_step_index` (217) fails loud off-grid**; `build_identity_manifest` (261); `audit_manifest_against_assignment` (321); `_physical_config` (401; the ramp default `duration/2.0`); `_fault_components` (500); **`_plant_payload` (600)**; **`_generate_reservation` (607; RETURNS a 6-tuple; the CablePlant is NOT returned)**; `materialize_base_dataset` (731). **Line 24 `from .cable_plant import CablePlant` is what makes every importer of this module a transitive `mujoco` importer — including the driver.**
- **`scripts/utils/gate3_assignment.py`** — `expand_reservations(document)` → `list[ScenarioReservation]`. **Lines 648-697:** `seed = seed_base + 10*ordinal`, `sim/fault/sensor/controller = seed+0/1/2/3`, `base_pair_id = basepair_{split}_t{ti:02d}_f{fi:03d}_r{rr:02d}`, realized `pair_id = base + "_dataset0"`.
- **`scripts/utils/storage_contract.py`** — `IdentityManifestRow` (20 fields); **`_valid_config_hash` strips exactly `dev-` then requires 64 lowercase hex.**
- **`utils/config_contract.py`:** `load_config(config_path, schema_path, *, require_frozen=False)`. `file_sha256` is a **RAW-byte** hash; `canonical_json_bytes` + `sort_keys`/`separators`/`ensure_ascii=False`/**`allow_nan=False`** is the document path and the canonical-JSON precedent Protocol P matches.
- **`utils/sensor_model.py`** — `config_hash` is **free-form provenance, never validated**, which is what makes the derived screen-provenance stamp safe. Temperature reaches the gauges at `:423-424` (10 µε/°C); the 0.5 µε quantizer at `:429-431`. **Carries no state across `observe` calls (measured S45).**
- **Rollout entry point is `utils/online_loop.run_online_rollout(plant, sensors, *, n_steps, history_steps, command_policy, reference_fn=None, temperature_fn=None)`.**
- **Assignment structure:** 19 known settings per split, +2 compound/OOD in val/test; **2 trajectories per split**, split-exclusive; realizations 4/4/4/8; seed bases 110000/210000/310000/410000; reservations **152/152/168/336 = 808**. Expansion order **healthy → structure → actuator → sensor** — **extending `grid["structure"]["severities"]` shifts every later ordinal and therefore every later seed**, which is why Codex chose full regeneration.
- **Structural severities by split: dev {0.75, 0.50}, pilot {0.85, 0.60}, val {0.90, 0.40} + OOD 0.55; test {0.65, 0.35} + OOD 0.45.** Payloads: dev {0.000, 0.050}, pilot {0.025, 0.075}, val {0.100, 0.125}, test {0.150, 0.200} kg.
- **Context cell table** (index `(trajectory_index * realizations + replicate) mod 8`), each `[payload_idx, env_idx, contact_idx]`: `0:[0,0,0] 1:[0,1,1] 2:[1,0,1] 3:[1,1,0] 4:[0,0,1] 5:[0,1,0] 6:[1,0,0] 7:[1,1,1]`. `t00`→{0,1,2,3}, `t01`→{4,5,6,7}.
- **Contact profiles:** dev_none `null`; dev_brief `[2.0,2.5]`; val_extended `[1.8,3.3]`; test_sustained `[1.6,3.8]` → **A2 pin 4 changes this to `[1.8,3.3]`**. Offsets are relative to onset. All non-null profiles use `endpoint_plane_z_m = 0.2`.

## My lanes — current state

`Reproducibility Packet/scripts/utils/estimator.py`:
- **`WindowFeatureExtractor(window_steps=W=768, probe_frequency_hz=0.8)`**: `window_tensor(record)` → `(values[W,D], valid[W,D])`; **requires `record.n_steps <= W` and right-aligns (`estimator.py:366-375`) — it refuses a full run, so the caller owns the window origin**; `window_features(record)` → 144 features. `N_FEATURE_STATS=4`, `N_EXTRA_FEATURES=4`, sync cols 4/5/6, `VALID_FRACTION_COL=7`, `MIN_SYNC_SAMPLES=8`.
- **`synchronous_coefficient_vector(record, extractor)`** → **the last `2*4=8` entries are the gauge columns for S**. **`coefficient_reference_distance`** is scaled/normalized — for raw µε use `np.linalg.norm(v_fault[-8:] - v_healthy[-8:])`.
- **`WindowNoveltyDetector`** · **`CoefficientReferenceDetector`** · `_SCORE_STD_FLOOR=1e-3` · **`SeverityRidgeHead`** (`train_residual_std` is IN-SAMPLE — never feed a confidence gate) · `leave_one_group_out_residuals` (CALIBRATION-role diagnostic) · `OracleInterface` · `EstimatorCommandPolicy` · `RECOMMENDED_WINDOW=(768,16)` · **learned rungs specified-not-built (Gate 4).**
- **`utils/synchronous.py`** (Codex, S9) — `harmonic_coefficients` from a **least-squares fit with intercept + centred linear trend**. **Because `[ones, centered_time]` span a linear-in-time thermal ramp, such a ramp contributes exactly zero to `(cos,sin)` in exact arithmetic — quantization is what breaks it (S38 correction to Finding G).**
- **`utils/metrics.py` + `utils/stats.py`** (approved through S11): `tracking_reduction_pct`, `j_5s`, `safety_incident_rate`, `safety_flag_rates`, `safety_regression_delta`, `hierarchical_bootstrap_ci` (crossed pair×seed). **Eval driver (Gate 7) — build once the frozen layout exists.**
- **Screens (all closed):** `screen_severity_estimation_quality.py`, `screen_severity_action_boundary.py`, `screen_actuator_probability_channel.py`, `tests/test_recovery_seam.py`, **`screen_structural_separability.py` (packet-README Step 22)**.
- **`analyze_synchronous_detection_floor.py`** — mine, **MODIFIED S46** to import from `utils/gauge_windows.py`. **Both published artifacts re-verified BYTE-IDENTICAL.** It publishes `detect_threshold_microstrain = nes_mean + 5*nes_std`, **per gauge**, at `--window 640`. **It is a threshold, not a floor (S36); and it is the null of a SINGLE window, not of a difference (S37).**
- **Mine, Codex reviews: `Reproducibility Packet/protocol/protocol-p-v2.3.3.md`.**
- **Co-owned with Codex (S43): `tests/test_cable_plant_softening_boundary.py`** — the permanent I13b guard. 6 tests. **Codex's call if the two ever conflict.**
- **The S44 seam inside Codex's file + `tests/test_assignment_generator_screen_overrides.py` (37 tests). APPROVED AT EXACT STATE BY CODEX (S44).** Blobs `1c565888…` and `2ec96c9f…`.
- **`scripts/protocol_p_replay_gate.py` + `tests/test_protocol_p_replay_gate.py` (36 tests) — JOINTLY APPROVED.** **Re-run it after any generator change — it is a free bit-level regression test on the ordinary path.**
- **STAGE 0 — JOINTLY APPROVED, RUN ONCE (S48), RESULT APPROVED (S49), RUNBOOK STEP 24 APPROVED (S50).** `scripts/analyze_synchronous_difference_null.py` + `scripts/utils/gauge_windows.py` + `tests/test_synchronous_difference_null.py` (99) + `tests/test_gauge_windows.py` (18).
- **THE STAGE-A/B/C PROGRAM.** `scripts/utils/protocol_p_results.py` and `tests/test_protocol_p_results.py` are **JOINTLY APPROVED and UNTOUCHED SINCE** (`e84e5f9f…` / `cbac30ed…`, 77 collected). `scripts/run_protocol_p_screen.py` and `tests/test_protocol_p_driver.py` were approved at `99e2d447…` / `3f1a8106…` and then **EDITED BY ME IN S56 — both are back under exact-state review** (148 collected). **`screen_physical_faults` is now BUILT** — the last item on the pre-execution list. **Nothing else on that list remains open that I know of.**

## Codex's OTHER lanes — reference

- `utils/cable_mechanics.py` — `CableModelConfig`: `link_length_m=0.40`, `structural_ei_remaining` default **0.50**, `control_dt_s` default **0.002**, `endpoint_contact_plane_z_m` default 0.498 (assignment uses 0.2). **`diagnostic_tip_load_envelope` (`:444-454`) raises when `ramp > duration/2` → admissible fraction `(0, 0.5]`.**
- `utils/cable_plant.py` — **`import mujoco` at line 15. No RNG anywhere in the file (verified S37).** A structural fault builds a SECOND softened MuJoCo model; the healthy plant has `_soft_model is None`. `_activate_structural_fault_if_needed` is called from `advance` BEFORE the physics step and BEFORE `_step_index += 1`. `_fault_active`: `onset = max(int(fault.onset_index), 0); return self._step_index >= onset`. The `structural_ei_remaining=0.50` dataclass default is INERT in the healthy branch. **`cable_plant.py:124-125` restricts structural faults to location `{-1,1}` and severity to `(0,1]`** (do not re-litigate). **`rollout(n)` cannot be called twice on one plant.**
- **`utils/schema_types.py`** — `N_JOINTS = 2`; `FaultSpec` (65-79): `source_class="healthy", subtype="none", location=-1, severity=0.0, **onset_index=-1**, compound_flag=False, ood_flag=False`. **That `-1` default is the S41 defect's origin and is pinned as behaviour by the S43 test.**
- `utils/task_control.py`: **`proportional_gain=(0.05,0.03)`, `derivative_gain=(0.005,0.003)`, `torque_abs_limit=(0.20,0.10)`**; reads ONLY `q_obs`/`qd_obs`.
- `utils/recovery_control.py` + the four closed recovery/action screens; `run_bounded_noisy_information_review.py`: S macro-F1 0.995 / C1 0.704.
- **`screen_synchronous_safe_probe.py`** — `--ramp-period-fraction` default **0.125**; **`--peak-loads-n` default `[0.05, 0.1, 0.15]`**. It measures the **privileged** difference, not the observed path. **Still reads the floor summary JSON, so any edit to `utils/gauge_windows.py` must re-verify that JSON byte-identical.**
- `agents/Codex/Config Freeze Readiness Review.md` = the seven-gate plan (I approved S27).

## The evidence tables (development-evidence boundary)

**Structural (Codex S20):** remaining EI 0.50/0.25/0.10/0.05 → mean peak |gauge| 38.4/72.4/152.8/259.7 µε (healthy 19.2) but mean **joint** tracking deficit +0.08%/−0.89%/−2.23%/−5.00% — monotone in information, monotone the WRONG way in joint control (damage moves to the TIP, which the joint score never measures). **Use the direction, never the magnitudes.**

**Control-layer shape:** healthy/actuator/sensor → S has no exclusive info + 0% tracking change; **structure → S exclusive info YES, C1 withholds actionable, `s_tracking_change_pct` −18.58%.** C1 per-class recall: structure **0.083**, else 1.000. **NOTE: ONE fixed fault setting per class at a severity far more severe than the reserved grid, at the screened ramp not the delivered one, under a per-gauge/W=640 yardstick, on a single-window statistic, with the probe at onset.**

## The agreed contract's load-bearing specifics

- **Sensor suites (controlled variable):** C0 = joint encoders + commanded actuation · **C1 = C0 + noisy motor-current nominal-Kt torque estimate + one distal 6-axis IMU** · **S = C1 + four fixed strain/curvature gauge stations** · O = privileged oracle. **Temperature is observable ONLY through `gauge_obs`, i.e. only in S.** **The closed loop is driven by a C0 session in every suite — the suites differ only in what is OBSERVED post-hoc (S39 Finding K).**
- **Two settled correctness points:** actuator-gain fault acts *downstream* of the current proxy; encoder fault has a *relational* signature.
- **Success bar (pre-declared, BOTH layers, UNCHANGED by A2):** S improves held-out four-way macro-F1 over C1 by **≥0.05 absolute** (paired 95% excludes zero; every source-class recall diff lower-95% above **−0.02**) AND reduces the **5-s post-change integral of absolute tracking error by ≥10%**, paired 95% excludes zero, no safety regression. Known-class abstention = error in headline macro-F1.
- **Failure shapes:** hypothesis failure (clean negative) vs **method failure**. **Inconclusive (Slot 13):** diagnostic-only · fault-specific/bounded · confound-fragile · excitation-dependent · **role-coverage-bounded**.

## Carried limitations for the Technical Report / Gate 7

1. **2^(3−1) parity residual:** `I(trajectory ; full cell)` = 1 bit in dev/pilot/val, 0 at test.
2. **The OOD arm rests on only 2 compound settings per split** — thin. **No severe-band OOD claim will be made.**
3. **Test severities sit partly outside the fit hull.**
4. **`split_group_id` is unique per reservation**, so its one-mapping assertion is vacuous; the real guarantee is trajectory/fault exclusivity, which does hold.
5. **`_assert_fault_independent_context_cells`** is correct only because trajectory blocks are disjoint mod 8 at the actual values. Both pinned; cannot silently drift.
6. **[S33] Finding 1** — structural severity grid below the 2× synchronous margin at every reserved severity. **Quadruply qualified** (S35 A, S36 D, S37 F, S38 J).
7. **[S33] Finding 2 (contact), non-blocking.** 236 runs assigned a contact profile; **11 actually touched** (4.7%). All 11 are encoder **bias (7) or drift (4)**. **Realized contact is an EFFECT OF THE FAULT**, direction **favours S**. Addressed by A2 pin 4.
8. **[S34] The mild-stratum development diagnostic** — at dev EI 0.75/0.50 neither suite separates structure; the only consistent structural signature is a C1 IMU channel. **State at that scope only.**
9. **[S35] The excitation discontinuity** — the delivered probe is ~5.8× weaker than the screen that justified its amplitude.
10. **[S36] The yardstick discontinuity (D)** — per-gauge five-sigma at W=640 applied to a four-gauge statistic at W=768; error 7.7%, direction lax.
11. **[S36] The run-to-run range statement (E)** — **report as a range statement, never as a test.**
12. **[S36] Margin coverage is trajectory-partial.**
13. **[S37] The operation mismatch (F)** — a threshold on a single window applied to a difference of two; and **a matched-seed difference admits no sensor-only threshold at all** because CRN cancels the sensor term.
14. **[S37→S38 CORRECTED] Thermal near-invariance (G)** — a *property*, not a defect. **NOT exact cancellation** — thermal enters inside the 0.5 µε quantizer.
15. **[S37] The amplitude ceiling (H)** — the probe could not exceed 0.15 N without violating an approved actuator-authority limit.
16. **[S37] Stage-C null dependence** — `Q95_c` from 28 pairwise distances generated by only 8 independent runs; a U-statistic. **[S38] Under `method="higher"` it is the 27th of 28.**
17. **[S38] The window-origin discontinuity (J)** — **nothing in the codebase fixes the window origin**, so the protocol's pin is effectively the pipeline's pre-registration and Gate 7 must reuse it.
18. **[S38] The matched/unmatched asymmetry** — Stage A/B signal is seed-matched, Stage C null is not. Favours S. `TESTABLE` is **necessary, not sufficient**.
19. **[S38] Task motion leaks into the synchronous statistic** — probe-free `t00` healthy `||b||` at 0.8 Hz is 0.48–0.51 µε.
20. **[S39] The construction path (K)** — the loop is driven by a **C0** session and S gauges are produced **post-hoc**. **ONE delivered row reproduces bit-for-bit from committed inputs — put this in the packet at that exact scope.**
21. **[S39] The unmatched-identity confound (L)** — **every** delivered-row magnitude is `||fault + closed-loop divergence||`.
22. **[S39] The observed path is nearly free on a matched difference** — 0.937×–1.148×, mean ≈0.996.
23. **[S40] The realized-vs-base identity distinction** — any protocol, audit, join or leak guard that names "pair_id" must say **which one**.
24. **[S40] The ramp fraction is unreachable through the assignment document** — `duration/2.0` is computed, not read.
25. **[S40] `Q95_c^gauge` and the S39 gauge-only measurement are conditional healthy-null diagnostics only.**
26. **[S41] The Stage-A safety gates are not a construction check.** **[S43] Now covered by a permanent automated test rather than by vigilance.**
27. **[S41] A terminal branch that attributes a failure to physics must first exclude the construction.** Fenced by I13a AND I13b.
28. **[S41] Raw-byte file pins are cross-platform contracts.** `core.autocrlf=true` here.
29. **[S42] A byte pin must name its DOMAIN.** Also: **a `.npz` is a ZIP, so byte-identity of a *regenerated* archive is not a claim to make.**
30. **[S42] An undefined or overloaded token in a pre-registration is a scientific defect.**
31. **[S42] A specification can name an invariant its own architecture cannot express.**
32. **[S43] A pre-registration's variable names are part of its executable surface.** **[S56: this is why `screen_physical_faults` now exists under that name.]**
33. **[S44] The seam's own coverage history is part of the packet's honesty record.**
34. **[S44/S45] The seam and Stage-0 files are not byte-pinned, deliberately.** **Any claim about these files' bytes must quote the blob hash or say which EOL rendering it means.**
35. **[S45] The one-row replay scope is exact and must be stated as such everywhere.** ONE row, ONE suite: 20 privileged fields + 38 observed entries. **No dataset-wide reproduction claim exists.**
36. **[S45] The replay gate is not runnable by an outside reader, and the packet says so.** **Contrast Step 24, which IS runnable. [S50 CORRECTION: say "no dataset, no MuJoCo *simulation*", never "no MuJoCo".]**
37. **[S46] Stage-0's I8 guards the code, not the data.**
38. **[S46] `utils/gauge_windows.py` is a shared dependency of two screens, one closed.** **Any future edit must re-verify the floor screen's two published artifacts byte-identical.** Standing obligation.
39. **[S47] BOTH Stage-0 config-binding guards defend CODE, not present-day DATA.**
40. **[S47] A brute-force numeric scan for a pinned literal produces numerological hits as well as semantic ones.** **Exactly three of the seven pins are real bindings.**
41. **[S48] Stage 0's corroboration is upper-tail and must never be written as agreement.**
42. **[S48/S49] §8's "roughly 0.39" is an approximation; the executed value is 0.400881.** Quote the artifact. Closed.
43. **[S49] `stage_0_identity` binds INPUTS and OUTPUT SHAPE, not measured values — provenance, not a tamper seal.**
44. **[S49] `null_distribution.std` is the POPULATION standard deviation and the artifact does not disclose which.**
45. **[S49] The Stage-0 first-run elapsed time was never captured and cannot be honestly reconstructed.** Do not re-run Stage 0 to manufacture one.
46. **[S49] Cross-platform bit-identity of the Stage-0 output has NOT been measured.**
47. **[S50, RESOLVED S51] Stage 0's script no longer imports `mujoco` at all** — measured zero after the extraction, pinned by a test. **The DRIVER still does** (via `assignment_generator → cable_plant`), which Step 25 states explicitly. **Never write "needs no physics engine".**
48. **[S51] `utils/__init__.py` re-exports `SCHEMA_VERSION`, so ANY `from utils import X` imports NumPy.** `utils/protocol_p.py` itself imports only the standard library.
49. **[S51] `require_screen_reservation`'s `sensor_seed` check and I8's base-distinctness check are both CODE guards.**
50. **[S51] The torque gate's inclusive boundary is EXACT in IEEE double at both association orders** — `0.15*2*0.40 == 0.60*0.20 == 0.12`. **Any refactor of that arithmetic must re-measure it.**
51. **[S52] The construction layer's cell binding is over THREE IDENTIFIER STRINGS, not over the body.** Not a defect — the driver's source comes from the I1-pinned assignment. **The Technical Report may not say this module verifies the body.**
52. **[S52, SUPERSEDED IN PART BY S56] `build_overrides`'s `require_constructed_condition` call is tautological and no test can make it red.** **STILL TRUE OF THAT CALL — I did not change it.** What changed is that the driver now ALSO checks the constructed tuple against a document-derived expectation (`require_preregistered_faults`), which is not tautological and is measured to refuse a state the old call accepts. **Never describe the `build_overrides` call as a live guard; DO credit the driver-level one, at the scope in the S56 block above.**
53. **[S53] The screen's provenance stamps outnumber its rollouts 180 to 168, by design.** **No write-up may say "one provenance stamp per rollout."**
54. **[S53] The Stage-0 artifact's reported statistic has NEVER been recomputed after the S51 refactor and cannot be without re-spending the measurement.** A 2-pair run's q95 is `0.1894914916579524` against the reported `0.4008810868833315`. **Never write that the refactor preserved the result "bit for bit" without naming the 2-of-100 scope.**
55. **[S54] `require_inventory_shape`'s distinct-body count is a CODE guard** — forced by arithmetic once the row keys are unique. **No write-up may present it as evidence that the 168 count was independently verified at runtime.**
56. **[S54] The 28-distance check inside `gauge_only_null` is UNTESTED; the identical check in `stage_c_null` is the exercised one.** **Do not write that both Stage-C size checks are covered.**
57. **[S55] A green suite is evidence about the states it enters, and nothing else.** The 906-test suite passed while two of three real defects were live. **No write-up may present a suite count as evidence of driver correctness.**
58. **[S55] Section 9 does not define the consequence of a hard-gate failure in a Stage-C healthy replicate.** The driver terminates under `UNSAFE_STAGE_C_REPLICATE`, **which is the driver's name, not a pre-registered one**. **[S55 RULING: Codex accepted this without a specification bump. No Technical Report sentence may present that label as a Protocol-P branch.]**
59. **[S55] The gate read on the two reused ladder values (0.75, 0.35) is forced to pass and is not coverage.** Only eight of the ten are live.
60. **[NEW S56] The driver-level I13a check is live on the ONSET and on the condition/severity routing, and NOT on the fault's other fields.** `screen_physical_faults` delegates field construction to `requested_fault_specs`, the same function `build_overrides` uses, so a change to that builder moves both sides together and cancels. That was chosen deliberately over a second copy. **The write-up may say the driver verifies the stamped onset against the trajectory document; it may NOT say the driver independently verifies the constructed fault.** What binds the fields to Correction 1's literals is a test that quotes the specification.
61. **[NEW S56] The helper's closed-vocabulary check is redundant with the construction layer's.** Deleting it changes the message, not the outcome. Kept for fidelity to Correction 1's text. **EIGHTH MEMBER OF THE CLASS** (37, 39, 43, 49×2, 51, 55, 59). **Do not count it as coverage of the closed-set property.**
62. **[NEW S56] Plan-mode elapsed time is 0.30–0.33 s, measured over three subprocess-timed runs.** The "~10 s" figure this summary carried from S54 to S55 was never measured. **The 70–80 minute full-run figure IS an extrapolation from one measured rollout and Step 25 labels it as one — do not quote it as a recorded runtime.**

## Coherence / honesty bounds (keep loud)

- **Sensor RNG keyed on `(sensor_seed, pair_id, channel, stream)` jointly** (`utils/rng.py:76-78`). **Measured S39: a `pair_id` change alone moves `gauge_obs` by up to 6.50 µε**, against `D` of order 0.1–0.5. **Nothing else is in the key.**
- Deployable floors are *detection*, not learned attribution; abstention untestable on this fault library; **every joint-space control number comes from a condition where the structural fault causes no measurable JOINT deficit.**
- **A noise threshold is a property of the SENSOR MODEL, the window LENGTH, the window ORIGIN, the aggregation, the path, the operation, the construction, the identity, and the fault's activation step. The SIGNAL it is compared against depends on excitation, task and plant.** Never quote a µε number without naming all of these.

## Constraints / environment / ops (load-bearing)

- **Simulation-only, one desktop:** Windows 11, Ryzen 7 8700F (8C/16T), RTX 5060 Ti **16 GB VRAM** (sm_120), 32 GB RAM, Python **3.12.10** in `./venv`. Free/OSS, commercial-use-friendly only.
- **venv has:** numpy 2.5.1, scipy 1.18.0, scikit-learn 1.9.0, matplotlib 3.11.0, mujoco 3.10.0, pandas 3.0.3, control 0.10.2, gymnasium 1.3.0, pytest 9.1.1, **torch 2.11.0+cu128**. **No new dependency was added in S46–S56.**
- **Running packet tests:** from the REPO ROOT, `./venv/Scripts/python.exe -m pytest -q "Reproducibility Packet/tests"`. **Scope pytest to that path** — a root-wide invocation collides on duplicate test module names in the ignored `tmp/session6_packet_copy/`. **Full suite 975 tests green (S56, 113.09 s; `test_protocol_p_driver.py` now collects 148, and 938 + 37 = 975 exactly, so the S56 additions are the entire delta).** Prior: 938 (S55, 114.30 s), 906 (S54), 750 (S53), 595 (pre-S51 baseline). **The suite is ~4x slower than pre-S54 because the driver's end-to-end test rehearses all 168 rollouts through the real SensorModel on synthetic bodies — deliberate, and it spends no MuJoCo rollout.** **Set `PYTHONIOENCODING=utf-8` for anything that prints non-ASCII** — the console is cp1252. **Use ASCII in probe scripts and in anything a gate prints.**
- **Packet scripts are invoked FROM the packet directory** (`scripts\<name>.py`, `--output-dir results\<name>`), per its README. From the packet dir the project venv is `..\venv\Scripts\python.exe`. **In my PowerShell tool the working directory is not the repo root — use `Set-Location` or absolute paths. My Bash tool's cwd PERSISTS between calls — prefer absolute paths or re-`cd` every time.**
- **Timings (measured S35–S56):** full packet suite ~115 s (S55/S56; ~12–13 s before the driver test landed); one MuJoCo rollout (3000 steps) **25.6–27.5 s**; a PARTIAL rollout is proportionally cheap — 480 steps ≈ 3.0 s; at reduced fidelity (`point_count=9`, `simulation_timestep_s=2e-4`) 501 control steps ≈ 0.37 s; a 200-realization sensor-only null at W=768 ~40 s; an offline re-observation ≈ instantaneous; a 3,124-file inventory ≈ instantaneous; **the driver's `--mode plan` 0.30–0.33 s [S56, measured]**; **one driver-file mutation case ≈ 100 s, so a 17-case sweep is ~28 min and belongs in the background**; a 26-case sweep over two small files ≈ 100 s. **NO figure exists for the pinned `pairs=100` Stage-0 run — see limitation 45; do not invent one.**
- **Background jobs:** `run_in_background: true` and wait for the notification. **Python buffers stdout when redirected — use `flush=True` in the job and poll the file it writes, not a pipe.**
- **PowerShell 5.1** primary (no ternary/`??`; **`^` is not a continuation**); Bash tool also available. **`bc` and `/usr/bin/time` do NOT exist in the Bash tool** — time a subprocess from Python with `time.perf_counter()`. Use `git diff --numstat` to confirm `+N/−0` after every chat turn.
- **Root `.gitignore`** covers `venv/`, `/data/`, `tmp/`, `MUJOCO_LOG.TXT`, caches, model files, LaTeX aux, OS/IDE noise, and the three session locks (`.claude-session.lock`, `.codex-session.lock`, **`.agent-session.lock`** — the scheduled-task runner creates the last one at the repo root). **Root `.gitattributes`** pins `schema.json`, the assignment JSON, and **`Reproducibility?Packet/protocol/*.md`** to LF. **Packet `.gitignore`** ignores `*.npz` + caches/logs (so `results/*.json` and `*.md` ARE tracked). **Verified again S56; no change needed.**

## STANDING LESSONS

1. **Dry-run the analysis path before spending a rollout budget.**
2. **Self-audit from row artifacts / raw bytes, not the summary.**
3. **Restate a proxy in the contract's units before comparing to the bar.**
4. **For a MuJoCo screen, re-run to scratch + diff against committed.** *(S46: any refactor touching a closed screen owes a byte-identical re-run of its published artifacts.)*
5. **Verify the live git state before trusting continuity.**
6. **Review a design by simulating its consequences, not by verifying its internal consistency.** **The dangerous confound is the one that favours you.**
7. **For any pre-registration, check that the pre-registered TEXT generates the pre-registered DATA.**
8. **Test a guard by feeding it the exact state it was written to catch.** **Check a flaw is REAL before reporting it; check a REPORTED flaw is real before fixing it.**
9. **A design review that reads the design cannot find what the design does.** **Audit the yardstick before the artifact.**
10. **A negative result is only readable if the same instrument produced a positive one.**
11. **(S35) A threshold and the signal it judges must be measured in the SAME configuration.**
12. **(S36) When you import a number, import its definition, not its name.** **Two configuration errors can cancel, and that is dangerous rather than lucky.**
13. **(S36) When a choice you must make favours you, measure how much, say so, and hand the decision to the reviewer.** *(Applied eleven times now.)*
14. **(S36) A pre-registered protocol must be executable by someone who did not write it.** **The act of making it executable is itself the defect-finding technique.** *(S56 is the strongest instance yet: implementing a function the specification had merely named exposed that a different check could not fail.)*
15. **(S36) The cleanest statement of a negative is often a comparison you have not made yet.**
16. **(S37) Match the null to the OPERATION, not just to the configuration.**
17. **(S37) Compute the closed-form consequences of every gate you approve, before it costs anything.** **Check boundary cases for `<` vs `<=`.**
18. **(S37) When the most likely branch creates a design problem, force the decision BEFORE the measurement that would make any fix look chosen.**
19. **(S38) When you import a convention, import the CONFIGURATION THAT MAKES IT TRUE.** The chain: window length → aggregation → operation → time origin → construction path → realized identity → fault activation step → file byte-domain → the name an expression binds → the denominator → the fixture size → the scope a correction claims.
20. **(S38) A guard that checks a NECESSARY condition will silently license the SUFFICIENT one.**
21. **(S38) Check your own published claim against your own published table.**
22. **(S39) A specification can be complete about the MEASUREMENT and silent about the INSTRUMENT.**
23. **(S39) Two independent errors that point the SAME way are the dangerous case.**
24. **(S39) Cheap exact reproduction is a measurement instrument, not just a confidence check.**
25. **(S40) A guard's claimed scope must be tested against the construction that will actually run.**
26. **(S41) A check that passes with a large margin is evidence about the property it measures, not about the construction that produced it.**
27. **(S41) An escalation trigger should be content-based, not count-based.**
28. **(S42) Generalizing a fix is making a new claim about a new domain — check it there.**
29. **(S42) Name a tool for its domain, because the name is part of the interface.**
30. **(S42) Ask of every invariant: is this property reachable from where I am asserting it?**
31. **(S42) Verify a reported flaw before fixing it, and audit its class before calling it fixed.** **One instance reported usually means a class present.**
32. **(S43) A generic name in an operative expression is an open invitation.**
33. **(S43) A constant that looks authoritative and drives nothing is the same trap pointed the other way.**
34. **(S43) When you deviate from a collaborator's stated sequencing, say so at the top, give the reasoning, and hand them the decision.**
35. **(S44) Unit-testing both ends of a wire does not test the wire.** (a) deleting a call site is invisible whenever the guard's rejected state is not producible — wire-test it by monkeypatching the guard to always raise; (b) a test helper that reimplements production arithmetic is a second copy that agrees with itself.
36. **(S44) Injecting defects into your own finished patch is cheap and it is not optional.**
37. **(S44) Deleting a vacuously-passing test is a contribution, not a gap.** **Ask of every new green test: what exact state would make this red?**
38. **(S44) Extending a stated principle to an unenumerated case is still a deviation — lead with it.** *(Applied in S56 for the machine-path fix.)*
39. **(S45) A clean report must disclose its denominator.**
40. **(S45) Ask what else a reproduction check happens to hold fixed.**
41. **(S45) NaN tolerance and NaN blindness are one line apart.**
42. **(S46) A test fixture can be too small for the defect it is meant to expose.**
43. **(S46) Re-review the fix to your own defect as work, not as a verdict.**
44. **(S46) Promoting a diagnostic to a hard gate needs its own false-positive measurement.**
45. **(S47) A DIRTY report needs verifying as much as a clean one.**
46. **(S47) When a pinned value also exists in a bound document, the fix is EQUALITY, never ADOPTION.**
47. **(S47) Establish reachability by construction, and do not conclude "unreachable" from failed attempts.**
48. **(S47) Asking "what exact state would make this red?" is a per-test question.** **Assert the REASON for a refusal.**
49. **(S48) A reviewer's correct fix and a reviewer's correct reasoning are separable, and the owner re-review owes both.**
50. **(S48) Verify a correction the same way you would verify an accusation — by construction.**
51. **(S48) Extract the prior state from git rather than reconstructing it.**
52. **(S48) When a finding changes no shipped behaviour and the reviewer has asked for an unambiguous approval, record it and approve.**
53. **(S49) When you re-verify someone else's verification, CHANGE THE INSTRUMENT.**
54. **(S49) After a reviewer corrects a claim, search the artifact for that claim's other instances.**
55. **(S49) A name travels into the write-up faster than its mechanism does.**
56. **(S49) Approval is an ACT, not a state you drift into.** Post it as its own turn, naming the exact blob.
57. **(S50) A correction is an artifact and inherits every failure mode an artifact has.** **For an append-only log, edit the correction if it is still under review, never a settled dated entry, and never append a correction-to-a-correction.**
58. **(S50) A documentation claim about a dependency is a measurable claim, and an import-only load settles it in seconds.** *(S56 generalized it: **any claim about what a program writes is settled by running it and reading the file.** The absolute machine path had been in the artifact since S54 and three review passes read the code without seeing it.)*
59. **(S51) A test that matches on a LABEL certifies a guard it may no longer exercise.** **Match a phrase unique to ONE raise site.** *(Recurred in S56, in the first session after it was written down. Its sharpened form: **when you add a guard that duplicates an existing one, its MESSAGE is the thing most likely to be non-distinguishing, because you wrote it to say the same thing.**)*
60. **(S51) A mutation that survives a focused sweep is not yet a gap — re-run it against the full suite before calling it one.**
61. **(S52) Test per BRANCH, not per guard.**
62. **(S52) A guard that refuses everything is not a guard — test the ACCEPT side against the real inputs.**
63. **(S52) Two mutually redundant call sites of one guard are individually untestable.** **Sweep the DOUBLE removal.**
64. **(S52) When the reviewer's repair is itself an artifact, sweep it the way you sweep your own.**
65. **(S53) A status clause that has been true for several consecutive entries is the most likely thing to be carried into one where it is false.**
66. **(S53) Build the WHOLE plan once, before building the thing that executes it.** **Whole-set questions are invisible to per-item tests by construction.**
67. **(S54) A test can verify a property of the LANGUAGE and look like it verifies a property of your code.** **Ask: is the behaviour I am asserting mine, or the runtime's?**
68. **(S54) A count pinned as a literal can only audit the one plan it was written for.** Derive the quantity, keep the pre-registered number as a pin, reconcile by equality at exactly the configuration the pin is stated for.
69. **(S55) A reviewer's finding reached by READING is not the same evidence as one reached by RUNNING, and the owner re-review owes the difference.** **When you reproduce a finding, first prove your instrument reached the thing it claims to have broken.**
70. **(S55) Measuring a check and discarding its result is indistinguishable, in the finished record, from never having run it — and it reads in code review as coverage.** **For every value a function returns, ask which caller acts on it.**
71. **(NEW S56) A comparison whose two sides come from the same function and the same arguments is a report of a check, not a check — and it is indistinguishable from a real one in every artifact a reviewer reads.** `require_constructed_condition` had a name that says what it does, a docstring citing the Session-41 measurement, tests that pass, and a call site on the executing path. What it did not have was two independent sources. I found this in S52, wrote it down as a limitation, and **kept working for four sessions with the check still dead**, because a documented tautology feels handled. **The general move: for every check, name the two sources and confirm they are actually different. If you cannot name a second source, the check is a restatement.** Its companion: **the fix for a tautology is usually an independent derivation you already have somewhere** — here it was written into the pre-registration two years of sessions ago, under a function name nobody had implemented.
72. **(NEW S56) A finished artifact should be read as a stranger would read it, not just built to a specification.** The Stage-A/B/C results document carried the author's home directory from the session it was written in through two full review rounds and a joint approval. Nothing in the code says `C:\Users`; it is an obviously-correct `str(path)`. It shows up only if you run the program and open the file. **Before handing over anything that writes an artifact, open the artifact.**

## Pointers

- **Protocol P (in force, JOINTLY APPROVED): `Reproducibility Packet/protocol/protocol-p-v2.3.3.md`, canonical sha256 `5689dad7…8bdf421f`. READ THE FILE.**
- **The replay gate: `Reproducibility Packet/scripts/protocol_p_replay_gate.py` + `tests/test_protocol_p_replay_gate.py` (36 tests).** Run from the packet dir: `..\venv\Scripts\python.exe scripts\protocol_p_replay_gate.py --data-root ..\data\gate3-base-dev-pilot-val-c1-s`. **PASSED in S45, twice in S46, once in S51. NOT run S52–S56. I proposed running it once immediately before the 168 rollouts.**
- **Stage 0: `Reproducibility Packet/scripts/analyze_synchronous_difference_null.py` (blob `f104971d…`) + `tests/test_synchronous_difference_null.py` (99).** Pre-registered invocation, run from the packet dir: `..\venv\Scripts\python.exe scripts\analyze_synchronous_difference_null.py --window 768 --f-ctrl-hz 500.0 --diagnostic-hz 0.8 --thermal-ramp-c 3.0 --pairs 100 --seed 0 --pair-id 1` — all seven are also the defaults. **It has been spent; re-running it is NOT authorized without a new decision.**
- **The Stage-0 artifact — JOINTLY APPROVED. Tracked. DO NOT EDIT, DO NOT RE-EXECUTE.** `Reproducibility Packet/results/protocol_p/sensor_only_difference_null.json`, git blob `31c1e6d1824c10bd5978d12c377f76cf556af03f`. **`samples` is a 6-key metadata dict; the 100 values are `samples["distances"]`. There is no top-level `authority` — the path is `corroboration.authority`.**
- **THE STAGE-A/B/C PROGRAM — two files APPROVED AND UNTOUCHED, two UNDER REVIEW AFTER MY S56 EDITS.**
```text
APPROVED, UNTOUCHED IN S56 (Codex S55):
  Reproducibility Packet/scripts/utils/protocol_p_results.py  e84e5f9f4e6d10408873d87b81b2baef9535d50e  40,090 B
  Reproducibility Packet/tests/test_protocol_p_results.py     cbac30ed3d41c961f7d5c54c306c8a09fa1be1cd  33,724 B  77 collected
UNDER REVIEW (my S56 edits; the S55-approved blobs are SUPERSEDED, never quote as current):
  Reproducibility Packet/scripts/run_protocol_p_screen.py     was 99e2d44744eaf7ecd2bda1a21acce1ec9ce435c4   +173/-2
  Reproducibility Packet/tests/test_protocol_p_driver.py      was 3f1a81067116f2815f8680e6307e15e06c629db6   +419/-1  148 collected
  Reproducibility Packet/README.md (Step 25)                  +30/-0
NEW PUBLIC SURFACE SINCE S55: screen_onset_index, screen_physical_faults,
  require_preregistered_faults, packet_relative_input_path, SCREEN_CONDITIONS (an alias).
Run plan mode from the packet dir:
  ..\venv\Scripts\python.exe scripts\run_protocol_p_screen.py --output-dir <dir>
  zero rollouts, 0.30-0.33 s, writes stage_abc_screen.json.  `--mode execute` is UNAUTHORIZED.
```
- **`agents/Claude/Progress Reports/Progress Report Session 56.md` — NEW in S56, unreviewed.** Covers S49–S56. Its honest headline is that sixteen sessions have now produced no measurement of the central question, and it hands the pace trade-off back to the director explicitly rather than defending it unilaterally. `Progress Report Session 48.md` remains jointly approved at blob `f01aa7d7…`.
- **The seam (APPROVED, Codex S44): `ScreenOverrides` in `Reproducibility Packet/scripts/utils/assignment_generator.py`, git blob `1c565888…`, and its tests, git blob `2ec96c9f…`.** Read spec §3 beside them.
- **The I13b guard: `Reproducibility Packet/tests/test_cable_plant_softening_boundary.py`** — 6 tests, co-owned, **approved in place by Codex (S43)**. **The driver NAMES it as a precondition it does not itself run.**
- Claim Sheet (in-force contract): `Claim Sheet.md` · plain-language: `Accessible Claim Sheet.md` · Study Guide Pass 1: `Study Guide/Pass 1 - Conceptual Foundation.tex`
- **Shared schema (in force, +A1):** prose `Reproducibility Packet/schema/schema-v1.0.md`; machine `schema.json`.
- **The freeze plan:** `agents/Codex/Config Freeze Readiness Review.md`.
- **The probe-amplitude record:** `Reproducibility Packet/results/synchronous_safe_probe/synchronous_safe_probe_report.md` — **read S35 Findings A–C, S36 D, S37 F, S38 J, S39 K/L beside it.**
- **The detection-floor record:** `Reproducibility Packet/results/synchronous_detection_floor/summary.json` — **`detect_threshold_microstrain` is a 5σ threshold, per gauge, at W=640, of a SINGLE window.** sha256 `4937e885…c2c67`; **re-verify after any edit to `utils/gauge_windows.py`.**
- **CONCLUDED director chat:** `chats/Claude-Codex-Human/Better Suited Task/…- Concluded.md` — the withdrawn task-redesign directive. **A2 must stay clear of it.**
- Director requests: `director_requests.md` (root) — entry 1 (Claim Sheet review) non-blocking, **still awaiting director reply; it is named in the S56 progress report's "what isn't working"**. Nothing else is blocked on the director.
- My foundation `agents/Claude/Literature Foundation.md` · ledger `agents/Claude/references.md` (**no S20–S56 entries — reproduction/construction/measurement/review sessions, no external sources read**).
- **Live-Run README (co-maintained): root `README.md` — Phase 2 / In Progress, banner 2026-08-01.** **My S56 appended ONE new entry (`+2/−0`) and edited no dated entry.** The deciding question was again a claim going stale: Codex's S55 entry says the program is approved by both agents at the same exact state, and I changed it. **Standing decision, recorded so it is not re-litigated: dated entries are never edited; corrections propagate forward.**
- **Phase-2 chat:** `chats/Claude-Codex/Phase 2 Integration and Config Freeze/…- Active.md` (**13,628 lines**; Codex's S55 turn at 13,341 `+64/−0`, my S56 turn at 13,405 `+227/-0`. **Codex owns the next turn — exact-state review of three states, plus the vocabulary-check question. Do NOT re-ask the plan default, the Stage-0 imports, or the Stage-C label.**).
- **Monitoring chat:** `chats/Claude-Codex-Human/Transcript Order Monitoring/…- Active.md` (88 lines; unchanged S43–S56 — no recurrence; **streak twenty-two**: Codex's S55 commit was `+64/−0`, its header once at 13,341, after its recorded 13,337-line boundary, and it was physically last). The duty is to flag recurrences, so a clean session adds no note; verify at the git level regardless.

## Scratchpad (S56, NOT committed)

`append_turn.py` (**copied forward and reused unchanged, sha256
`3cf26db962bf3accb97880d1343fe791129f3790db1d70b68fd58a552d26fa2d`; FOURTEEN sessions now** --
find it with
`ls -1 */scratchpad/append_turn.py | while read f; do echo "$(sha256sum "$f" | cut -c1-16)  $f"; done | grep ^3cf26db962bf3acc`
under `C:/Users/cresp/AppData/Local/Temp/claude/C--Users-.../` before rebuilding),
`turn_s56.md`, `log_entry_s56.txt`, `new_driver_tests_s56.py` / `new_driver_tests_s56b.py`
(the appended test blocks, kept out of the repo edit path so the append could preserve exact
LF bytes -- `Path.read_text(newline=...)` does not exist on 3.12, so use
`read_bytes().decode()` / `write_bytes()`).
**`probe_s56_helper.py` -- the instrument worth rebuilding.** It resolves the REAL driver
context from the four committed inputs, builds real override bundles through
`build_overrides`, and drives the old and new checks over the SAME bad bundle in one run --
which is what turns "this check is tautological" from a code-reading claim into a
measurement. **Zero rollouts, ~3 s.** The general move: *to show a check is dead, feed the
state it exists to catch to BOTH the old check and the new one and print both verdicts side
by side.* Printing only the new one's refusal would have proved nothing about the old one.
**`verify_s56_mutations.py`** -- the sweep, in the S51/S52/S54/S55 template (per-case target
test files, `finally`-restore of exact bytes, explicit survivor list, bad-anchor detection).
**Each driver-file case costs ~100 s** because the module-scoped fixtures run a full 168-row
screen, so a 17-case pass is ~28 min and belongs in the background with `flush=True` prints
polled from the file, not a pipe.
