# Summary of Only Necessary Context — Claude

*Rewritten every session. Restores my working context for the next session. Excludes anything already in `Project Details/Project Details.md` and `AgentPrompt.md` (I re-read those in full at session start). Last rewritten: end of Session 52, 2026-08-01 00:15 PDT.*

## READ THIS FIRST — Protocol P lives in a file, not in this summary

```text
Reproducibility Packet/protocol/protocol-p-v2.3.3.md
canonical sha256   5689dad7ce4194b9a7dbe381006027df178997adf732f5734a77ef048bdf421f
54,621 bytes, LF, no BOM, raw == canonical, pinned text eol=lf
JOINTLY APPROVED — Claude S43, Codex S43. The specification loop is CLOSED.
Re-verified by measurement in S45 (replay gate), S46/S47 (Stage-0 I1 check + a permanent
test in each of the two test files), S48 (the executed Stage-0 run recorded
protocol_spec_sha256 in its artifact), and S49 (re-derived from the file itself).
Drift fails loud in two places.
NOTE: §8's "roughly 0.39" for Stage 0 is an S39-era APPROXIMATION, not a pin. Executed
value is 0.400881 (+2.79%). CODEX AGREED IN ITS S48 THAT NO PROTOCOL CHANGE IS WARRANTED.
Settled — do not reopen, do not edit v2.3.3.
```

**Read that file before doing anything on Protocol P. Do not reconstruct the protocol from this summary.** The spec contains the universe, the two hash domains, the terms block, the provenance scope, the seam (§3), the construction path (§4), the screen reservation (§5), the identity table (§6), the replay gate (§7), the window table, the statistic, Stages 0/A/B/C (§8), both secondaries, the outcome cases (§9), role coverage, the terminal branches, the fail-loud invariants I1–I12, I13a, I13b (§10), and the cost (§11).

**Version discipline — three versions deep. If it ever needs correcting again, bump the version and `git mv`; do not edit in place.** v2.3.1 (`8c268f8f…401d76`) and v2.3.2 (`9d257017…738ba6e5`) are superseded, each approved by me and blocked by Codex, **neither ever executed**; bytes recoverable from the `Claude Session 41` / `Claude Session 42` commits. **A version bump must also update `PROTOCOL_FILENAME` and `PROTOCOL_CANONICAL_SHA256` in `scripts/protocol_p_replay_gate.py` — and, as of S46, the Stage-0 script inherits both by import, so one edit covers both scripts, but the two test files each pin the digest independently and will both go red.**

## Where the project is

- **Phase 2 (Execution) is OPEN.** All Phase-1 gates in force. **Schema v1.0 + Amendment A1 in force.** Contract changes run through the **amendment protocol**.
- I am **Claude**; last session was **Session 52**; next session I run is **Session 53**.
- **`config.json` is deliberately NOT frozen** and does not exist. All hashes are `dev-`; no `dev-` trace may enter confirmatory analysis.
- Real data exists: `data/gate3-base-dev-pilot-val-c1-s` (3.86 GB, git-ignored, local only). 472 reservations / 944 manifest rows / C1+S / dev 152, pilot 152, val 168. **Test untouched: 0 identities, 0 payloads.** **Slated for full regeneration from zero after A2 — these 472 payloads become a superseded pre-amendment set in the packet exclusion trail. Read them; do not build on them.**
- **Protocol-P STAGE rollouts spent: ZERO.** Stages A/B/C are unbuilt as executables and unauthorized. **Stage 0 RAN in S48 and cost ZERO rollouts. It has NOT been re-run since and must not be without a new decision.** `results/protocol_p/sensor_only_difference_null.json` EXISTS, is tracked, and is **JOINTLY APPROVED**.
- **The §7 replay gate has now been executed FOUR times: S45, twice in S46, once in S51. NOT run in S52.** Each is ONE MuJoCo rollout run as a regression check on the ordinary path, ~25–26 s, and none of them is a stage measurement. Say it that way — "one authorized rollout" was always shorthand for the stage budget.
- **Progress report DONE at S48** (regular, covered S41–S48), **and its review loop is now CLOSED** (Codex approved my returned state in its S49). **Next regular: my Session 56.**

### ONE LOOP IS OPEN AND CODEX OWNS IT (the S52 returned test file + the public-log count).

```text
CLOSED  Stage-0 result artifact    blob 31c1e6d1824c10bd5978d12c377f76cf556af03f
        Codex S48 reviewer / me S49 owner.  Do not re-review, do not edit, do not re-execute.
CLOSED  Progress Report Session 48 blob f01aa7d7b56b9b30e8279bc221a5f0e60613ab3f
        me S49 owner (returned) / Codex S49 reviewer.  Director-facing, settled.
CLOSED  Reproducibility Packet/README.md — Step 24 at 9363e144…
        Codex S49 reviewer / me S50 owner.  THEN REOPENED BY ME IN S51 (see below).
CLOSED  README.md (root, the public Live-Run log) blob 73b124fd5e85c4cd0ebef8cce9a16c37c8e465e5
        Codex S50 reviewer / me S51 owner.  Settled.  Codex's first S50 turn inferred my
        approval from the edit-and-return and it WITHDREW that inference in a second turn,
        correctly and narrowly, keeping the artifact approval intact.
JOINTLY APPROVED IN THE S51/S52 ROUND — do not re-review, do not edit:
        scripts/utils/protocol_p.py                 8d9005250769b85739e5be4ddf00280f46acf71c
        scripts/protocol_p_replay_gate.py           c6b1674990a46f097a942559fd9077041d8270de
        scripts/analyze_synchronous_difference_null.py
                                                    f104971d426af95ca664826cbc276228adff7963
        Reproducibility Packet/README.md (Step 24)  ba9c067a4d7ccce4b6c29edcf588b7eeb0e8150e
          all four: Codex approved UNCHANGED in its S51; I created them in S51.
        scripts/utils/protocol_p_conditions.py      7fdddf0eee5e3b3f02b2db21ecb1b70728234be5
        tests/test_protocol_p_shared.py             f505877fbc43adb8c3ec2311674008f0c3b0e337  20 tests
          both: Codex reviewer-edited S51, approved BY ME UNCHANGED in S52.

OPEN    TWO STATES I EDITED AND RETURNED IN S52 — CODEX OWNS THE NEXT TURN:
        EDIT  tests/test_protocol_p_conditions.py   1874773e1ee8ed41bb763ca3a8a235d89e7c02e9
                135 collected, +135/-1, six new tests, TESTS ONLY
                raw sha256 acff836ba48c432ca1887c7272d1f6280d556917965f231aa3d7c17e52082fc7
                45,658 bytes, UTF-8, no BOM, pure LF
        EDIT  README.md (public log, count 141/736 -> 155/750, +1 sentence)
                                                    78b4a734303d36ded16d29788084305c30798d80  +1/-1
```

My S52 turn is at transcript line 12,172 (`+238/−0`); transcript now **12,409 lines**. Codex's
S51 turns are at 11,942 and 12,143 (`+233/−0` for the commit, clean tail append — **streak
eighteen**). My S51 turns were at 11,618 and 11,701.

**WHY APPROVAL MUST BE ITS OWN ACT, and do not forget it:** in S48 Codex refused to close the Stage-0 result loop because my S48 turn created, self-audited and handed off the file without ever explicitly approving it. Approval is never inferred from creation, a self-audit, a handoff, or silence. **Post the explicit approval as its own act, every time, naming the exact blob.**

## THE S52 SESSION — the owner re-review. CARRY THIS BEFORE TOUCHING THE CONSTRUCTION LAYER.

**Codex blocked my S51 construction handoff on TWO findings. BOTH ARE REAL — I established
both by construction, not by reading its reasoning. Do not reopen either.**

```text
FINDING 1  the provenance object was not the approved one.
  old payload  11 FLAT keys: assignment_canonical_sha256 base_config_hash cell condition
               pair_id probe_peak_force_n probe_ramp_fraction_of_duration
               protocol_spec_sha256 sensor_seed severity stage
  spec §Correction 2 pins NINE, nested: base_config_hash assignment_canonical_sha256
               assignment_hash protocol_spec_sha256 stage cell condition
               overrides(4 non-provenance ScreenOverrides values) reservation(
               scenario_spec_id base_pair_id sensor_seed)
  THE PART THAT MATTERS: the old function had NO ONSET PARAMETER AT ALL, so a step-0 and
  a step-500 structural request were indistinguishable to any caller. Measured:
    old  both stamp  dev-99f25e2b86943e35b0989e2e3d6c8852b2455399ff20b68c3441f7ca32364ff4
    new  onset=500   dev-686ab14de76e447aa21790e34a7e41b5744b296c57c0d6282123225b400fc516
         onset=0     dev-0794d1d831012dcfa05ba4452fc7093106204b5ef0fe175e96f42b9548970bf5
  This is the S41 defect reappearing inside the object whose job is to say WHICH run ran.

FINDING 2  valid pieces from the wrong cell composed. Old accepted all three; new refuses
  all three, each with a distinguishing message:
    cell-5 reservation + cell-5 Stage-A identity, cell=4 requested   -> accepted, stamped cell=4
    Stage-C k=3 identity on a stage="A" request                      -> accepted
    stage="Z"                                                        -> accepted
```

**REACHABILITY, MEASURED — the reviewed cell guard is not over-strict.** I expanded the real
assignment and fed it the four delivered sources: cell 4/5/6/7 <- `scenario_dev_t01_f000_r00..r03`,
ALL ACCEPTED for their own cell and REFUSED for every other. Codex's expected strings are the
generator's own `f"scenario_{stem}"` / `f"basepair_{stem}"` / `f"group_{stem}"` at
`gate3_assignment.py:672-687`, `stem = dev_t01_f000_r{rr:02d}`. **This is now a permanent test
(`test_the_cell_binding_accepts_the_real_delivered_sources`) and it is the only test in that
file that reads the assignment document.**

### THE S52 FINDING — A TEST FOR ONE BRANCH OF A TWO-BRANCH GUARD CERTIFIES THE GUARD

18-case mutation sweep over CODEX'S OWN PATCH. 11 caught focused; 7 survived; re-run against
the FULL 736-test suite, **5 were real gaps**:

```text
1  stage_c_identity_membership_removed   <- THE SHARPEST. Codex bound stage/cell/identity,
     tested the Stage-A half, left the Stage-C half unexercised. Weakening it reopens its
     OWN finding 2 in the branch that supplies the operative null.
2  stage_vocabulary_check_removed        an unknown stage stops raising and silently takes
     the `else` branch -> accepted as Stage C.
3  source_cell_base_pair_check_removed   the only test swaps a WHOLE source, which the
4  source_cell_split_group_check_removed scenario_spec_id check refuses first. 3 identifiers,
     1 exercised.
5  BOTH_condition_preconditions_removed  neither call site can be removed alone (the other
     stands), and removing BOTH survives the full suite too.
```

**I added six tests (14 collected cases); 16 of 18 mutations now caught.** New tests:
`test_one_wrong_cell_field_in_an_otherwise_valid_source_is_refused` (2),
`test_the_cell_binding_accepts_the_real_delivered_sources`,
`test_a_stage_c_rollout_cannot_use_an_identity_from_outside_its_cell` (3; **k=0 deliberately
excluded — I6 makes it that cell's own Stage-A identity**),
`test_a_stage_outside_the_closed_vocabulary_is_refused` (5; each uses a VALID Stage-C
identity, which is what makes them discriminating),
`test_the_stamped_fault_tuple_must_match_the_stamped_condition` (3).

**THE TWO REMAINING SURVIVORS — do not re-report either as a gap:**
- `shared_binary_helper_rebound_locally` was **a malformed mutation of mine** (an unused alias
  import cannot break an identity assertion). Formed properly — the gate defining its own
  `raw_file_sha256` — Codex's new shared test CATCHES it. Measured.
- `build_overrides`'s added `require_constructed_condition` call is **TAUTOLOGICAL**: it
  compares `requested_fault_specs(...)` against a fresh call to the same function with the
  same arguments, so no input can make it fail. **I KEPT the line** (it models a future where
  `faults` arrives from elsewhere; same reasoning I used in S47 for a line of Codex's).
  **No Technical Report sentence may call it a live guard.**

**Deliberately not done in S52:** did NOT change any production file; did NOT run the replay
gate; did NOT re-execute Stage 0; did not touch the protocol file, the assignment, the draft
config, the Stage-0 artifact, the seam, `utils/gauge_windows.py`, the detection-floor screen,
`.gitattributes`, or any payload; did not touch any dated public-log entry; **did NOT start
the driver** — Codex conditioned it on the loops closing and I returned an edited file, so
building on it would land against a state that can still move.

## THE S51 SESSION — the Stage-A/B/C build started; what it produced and what it cost

**Two new modules, both MINE, both HANDED TO CODEX AND NOT APPROVED.** Read them before
touching anything Stage-A/B/C.

```text
scripts/utils/protocol_p.py            the shared primitives, STANDARD LIBRARY ONLY:
                                       ProtocolPError, require, canonical_text_sha256,
                                       raw_file_sha256, canonical_json, and the two
                                       TEXT-domain pins + filenames.
                                       The two .npz pins STAYED in the replay gate.
scripts/utils/protocol_p_conditions.py the Stage-A/B/C CONSTRUCTION layer. Enforces
                                       I3, I4, I5, I6, I7, I8, I13a as PRECONDITIONS.
                                       Enforces nothing else, and says where the rest live.
```

**Public surface of the construction layer:** `RolloutIdentity`, `require_screen_cell`,
`require_suffix_free_pair_id`, `stage_ab_identity`, `stage_c_identity`,
`stage_c_cell_identities`, `require_unique_cell_identities`,
`require_stage_c_k0_matches_stage_ab`, `require_matched_identity`,
`requested_fault_specs`, `require_constructed_condition`, `screen_reservation`,
`require_screen_source`, `require_screen_reservation`, `rollout_provenance`,
`require_base_distinct_provenance`, `require_admissible_probe`,
`require_torque_gate_constants`, `torque_gate_admits`, `admissible_candidates`,
`build_overrides`, `iter_stage_ab_conditions`. Constants include `P_SEED_BASE`,
`SCREEN_CELLS`, `LADDER_REMAINING_EI`, `STAGE_A_STRUCTURAL_SEVERITIES`,
`CANDIDATE_PEAK_FORCES_N`, `CANDIDATE_RAMP_FRACTIONS`, `PINNED_LINK_LENGTH_M`,
`PINNED_TORQUE_ABS_LIMIT_N_M`, `SCREEN_PAIR_ID_PREFIX`.

**THE EXTRACTION'S MEASURED CONSEQUENCE — Stage 0 no longer imports mujoco AT ALL.**
```text
                                      before   after
analyze_synchronous_difference_null    True    False
protocol_p_replay_gate                 True    True    <- intrinsic, it rebuilds a reservation
seven utils.* modules                  False   False
utils.protocol_p                         -     False
```
Pinned in BOTH directions by `tests/test_protocol_p_shared.py` in fresh `-B` interpreters.

**Stage 0 is numerically inert under the refactor. Do not re-run the pinned invocation to
check this again.** `run_null(..., pairs=2, seed=0, pair_id=1)` reproduces the artifact's
first two distances `0.17764883124109498` / `0.1894914916579524` bit-identically.

**The replay gate was re-run after its own edit and PASSED** (25.08 s, 3,164 watched files
unchanged). **Full packet suite 725 in 13.22 s.**

### THE S51 FINDING — A TEST THAT MATCHES A LABEL CERTIFIES A GUARD IT MAY NOT EXERCISE

The mutation sweep (16 cases) caught 15; the survivor — removing the CRLF fold from
`canonical_text_sha256` — is caught by the FULL suite (2 failed / 722 passed, measured),
so it is a scope artifact of a focused sweep, not a gap. **The real gap was mine:**
weakening I3's exact-set comparison to `set(changed) <= set(FIELDS)` survived the ENTIRE
724-test suite. All three I3 tests matched `"I3"`, which appears at BOTH raise sites in
`require_screen_reservation`, so the weakened guard still refused two of three bad states
via the second raise — for the wrong reason — and everything stayed green. **The state the
weakening admits: a reservation that moved ONLY its `sensor_seed`, carrying a delivered
`base_pair_id` into the screen band.** Fixed: every I3 test now matches
`"differ from its source in exactly"`, plus a new
`test_moving_only_the_sensor_seed_is_refused_as_i3`.

### THE S50 SESSION — an owner re-review, and what it found

**Codex edited two of my documents in its S49 and handed both back. Both of its edited states were correct AND all its stated reasons were correct — a separate question, tested separately. I closed one loop and returned the other for a scope defect.**

### What I verified by construction (never by reading agreement into it)

**1. The transitive MuJoCo import — Codex is right, and its chain is exactly right.**
```text
import analyze_synchronous_difference_null  ->  'mujoco' in sys.modules   True   (import only)
analyze_synchronous_difference_null.py:96   from protocol_p_replay_gate import (...)
protocol_p_replay_gate.py:99                from utils.assignment_generator import (...)
utils/assignment_generator.py:24            from .cable_plant import CablePlant
utils/cable_plant.py:15                     import mujoco
mujoco==3.10.0 is pinned at packet requirements.txt line 2, which packet Step 1 installs.
```

**MY NARROWING — MEASURED, RECORDED, NOT RETURNED. Carry this verbatim.** Each of Stage 0's eight project imports, loaded in its own fresh interpreter:
```text
utils.assignment_binding  False    utils.schema_types      False
utils.config_contract     False    utils.sensor_model      False
utils.gate3_assignment    False    utils.synchronous       False
utils.gauge_windows       False    protocol_p_replay_gate  TRUE   <- one of eight
```
The surface crossed is `ASSIGNMENT_CANONICAL_SHA256`, `ASSIGNMENT_FILENAME`, `PROTOCOL_CANONICAL_SHA256`, `PROTOCOL_FILENAME`, `ProtocolPError`, `canonical_text_sha256` — four constants, one exception class, one pure-text hashing helper, **nothing physical**. So the dependency is **incidental, not intrinsic**, and is a direct consequence of Codex's own S46 answer 2 (accept the replay-gate import now; extract `utils/protocol_p.py` at the third consumer). **It should disappear at that extraction — whoever performs it must move packet README Step 24's dependency sentence with it.** I did not edit Codex's runbook text: a runbook states the dependency a reader observes today, not a plan.

**2. The outsider-clean rule — Codex's playbook citation is real.** `Playbooks/reproducibility-packet.md` line 39 ("Do not reference the Collaboration Station, the agents, or a history of what was done when"), line 53 (checklist item), line 63 ("The README is a runbook, not a journal"). My original elapsed-time paragraph said "the team's session records carry only an informal order-of-magnitude note" — a session-history reference inside an outsider runbook. Its rewrite keeps every auditable fact.

**3. The JSON path — correct.** Artifact top-level keys are exactly `boundaries, corroboration, inputs, null_distribution, protocol, purpose, samples, stage_0_canonical, stage_0_identity, statistic`. **There is no top-level `authority`;** the real path is `corroboration.authority`.

**4. The one-ULP mean, quantified with a third instrument (`math.ulp`, and a naive left-to-right sum):**
```text
recorded (NumPy)  0.2787343038701652
statistics.fmean  0.27873430387016523     difference 5.551115123125783e-17
ulp(recorded)     5.551115123125783e-17   -> EXACTLY 1.0 ULP, adjacent floats
naive sum/len     0.27873430387016523     -> also 1.0 ULP from recorded
q95 / population std / min / median / max  -> ALL EXACT
```
**Refinement worth keeping:** TWO independent non-NumPy summation orders agree with each other and differ from NumPy, so it is NumPy's pairwise summation that is the outlier — not `fmean` being odd. My S49 phrasing implied the reverse.

### THE S50 FINDING — A CORRECTION IS AN ARTIFACT AND INHERITS EVERY FAILURE MODE ONE HAS

Codex's public-log entry opens "Two corrections to **the preceding entry**." The phrase it withdraws was published **twice**:
```text
README.md:94   2026-07-30 entry     "...needs no dataset and no physics engine..."
README.md:96   2026-07-31 entry     "...it needs no dataset and no physics engine..."
README.md:98   2026-07-31 correction — scoped to "the preceding entry" only
```
A reader who stops at line 94 carries a withdrawn claim with nothing pointing at the withdrawal. **This is Lesson 54 recurring one session later, one level up — inside the correction itself.**

**Why I edited rather than appended, and this reasoning is the precedent:** the dated entries at 94/95/96 are settled record and I touched none of them (corrections propagate forward). But Codex's correction entry is **not** settled record — it is the newest entry and was the state under active review, handed to me with "edit and return it" as an explicitly sanctioned outcome. A correction-to-a-correction is strictly worse for a stranger than one correctly scoped correction. My edit names both entries by date and adds the "one of eight imports, a constants import, not the physics" measurement in plain language. `+1/−1`, Codex's entry only.

## THE S49 FINDING — THE STAGE-0 IDENTITY BINDS THE INPUTS, NOT THE NUMBERS. CARRY VERBATIM.

Established **by construction**. In memory I set `samples.distances[0] = 999.0` and `null_distribution.q95_method_higher = 0.05`, left `inputs` untouched, and re-applied the identity rule and the production validator:
```text
tampered artifact still satisfies identity == dev- + sha256(stage_0_canonical)   TRUE
require_valid_stage_0_identity(tampered, base_config_hash)                      ACCEPTS
canonical key set (7): assignment_canonical_sha256, assignment_hash, base_config_hash,
                       cli, output_schema, protocol_spec_sha256, stage
```
**NOT A DEFECT.** §8's Correction 6 pins exactly that seven-key payload, and the spec's only claim is that the digest is "independently recomputable from the artifact alone" — true and re-measured. **`stage_0_identity` is a PROVENANCE identity over the run's INPUTS and OUTPUT SHAPE. It is NOT a tamper seal on the results.** **No Technical Report / packet / public sentence may say it certifies, seals or verifies the measured values.** Verify a result by recomputing from `samples.distances`, which the artifact records in full. **Codex accepted this in its S49 as a documentation boundary, not a protocol defect — no version bump. Closed.**

**Third member of a class:** I8 guards code not data (limitation 37); both config-binding guards defend code not data (limitation 39); the identity certifies inputs not outputs (limitation 43). **Our provenance objects certify what went IN.**

### THE STAGE-0 RESULT — the project's first pre-registered measurement (RAN S48, JOINTLY APPROVED S49)

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
It **exceeds three of the four cells**, below only c5, ~5.7% headroom. "Inside the range" is TRUE and is the pre-registered claim. **"Agrees with the real-plant null" is NOT supported.** Authority field (`corroboration.authority`) is `"NONE"`; it sets no threshold and gates nothing. The operative null remains Stage C's `Q95_c`.

**SELF-AUDIT FACTS FROM S48/S49 (from the file, not the console):** 100 distances recorded; Q95 and mean recompute bit-identically under NumPy; **the identity reproduces as `dev-` + sha256 of the artifact's own 650-char `stage_0_canonical`**; **the first two distances (`0.17764883`, `0.18949149`) reproduce my S47 sensor-config control (`0.1776`, `0.1895`) exactly**, independent evidence the sensor block is read from the bound document rather than defaulted. `count > q95 = 4`, `count >= q95 = 5` (Codex's S48 correction is right). **`samples` is a 6-key METADATA DICT** (`n_pairs`, `seed_map`, `sensor_seeds_consumed`, `sensor_seeds_consumed_note`, `pair_id`, `distances`) — `len()` returns 6, not 100. Check the type before reporting an alarm.

## THE BIGGEST S47 FINDING — BOTH GUARDS DEFEND CODE, NOT DATA. CARRY THIS VERBATIM.

`validate_approved_assignment_binding` runs BEFORE both guards in `main()` and reconstructs the approved parent hash from the whole document with `scenario_manifest` nulled. So every other `values` block — **`timing` AND `sensor_model` both** — is pinned by:
```text
values.timing / values.sensor_model -> parent reconstruction
  -> wrapper.parent_draft_config_hash -> must equal assignment.draft_config_hash
  -> assignment bytes pinned by I1 (canonical 76255a80...)
MEASURED: committed draft reconstructs its parent True; either mutation -> False;
a re-stamped divergent config is refused AT THE BINDING GATE under python and python -O.
```
**Neither Codex's guard nor mine can be reached in a failing state from any document that gets that far.** They defend a `main()` reordering, a caller that skips the binding gate, or a future driver — and become live data guards at exactly ONE moment: when a new draft config is authored for the pre-confirmatory build. **Both should stay.** Two tests pin the architectural fact (`test_the_binding_gate_pins_the_blocks_both_guards_read`, `test_main_validates_the_binding_before_reading_bound_values`). **[S48: CODEX ACCEPTED THIS CORRECTION IN ITS S47]** — inside the current I1-pinned lineage a later sensor-model change cannot merely move the artifact identity while leaving the measurement stale; **it requires a new lineage, assignment, and I1 pin.** Settled — do not reopen.

**MY ONE NARROWING OF CODEX'S S47 FIX — non-blocking, recorded, do not reopen.** Codex said its added line recomputes the config hash "so the mutation is not rejected merely as a stale self-hash." **That gate never checks the current draft's self-hash on this path:**
```text
assignment_binding.py:174  parent_document["config_hash"] = parent_hash  <- OVERWRITTEN
assignment_binding.py:175  reconstructed_hash = expected_config_hash(parent_document)
assignment_binding.py:176  if reconstructed_hash != parent_hash:  -> the matched raise
assignment_binding.py:190  if config.config_hash == parent_hash:   -> distinctness only, DOWNSTREAM
```
Delete the line and both parameters still pass. **I kept the line** (it models a re-stamped attacker faithfully) and did NOT block a round over a justification for a correct line. **No Technical Report sentence may claim this gate validates a draft's self-hash.**

**JOINTLY APPROVED AT EXACT BLOBS — these loops are CLOSED. Do not re-review, do not edit.**
```text
scripts/utils/gauge_windows.py                  blob 7f7c09da...   6,806 B   (Codex S46 / me S47)
scripts/analyze_synchronous_detection_floor.py  blob b99fe333...  19,540 B   (Codex S46 / me S47)
tests/test_gauge_windows.py                     blob 925b0bd8...   8,225 B   18 tests
scripts/analyze_synchronous_difference_null.py  blob 8435c764...  40,098 B   (me S47 / Codex S47, unchanged)
tests/test_synchronous_difference_null.py       blob 9591c91b...  44,285 B   99 tests (Codex S47 / me S48)
  sha256 2fe39d831fa500d5183108ee4aed6590ac676af8beafec122b9af4919c9402ff
all: UTF-8, no BOM, pure LF.  Packet suite 595 passed.  Not byte-pinned (S44 policy).
```
**COUNTS:** the Stage-0 test file collects **99**; `test_gauge_windows.py` collects **18**; **117 is the TWO-FILE focused total.**

**Public surface across those rounds:** Codex S46 added `PINNED_CLI`, `require_pinned_cli`, `sensor_config_from_document`; `run_null` REQUIRES `sensor_config`; `linear_thermal_profile` REQUIRES `reference_c` (`THERMAL_REFERENCE_C` is GONE). I added S47 `CLI_TO_BOUND_TIMING_PATH`, `require_bound_timing_matches_cli` — the three-member timing boundary, fixed by **EQUALITY, NOT ADOPTION**. `thermal_ramp_c=3.0` matches `env_val_sine3c.parameters.amplitude_c` numerically and is **NOT the same object** — Codex agreed.

## CODEX'S S46 ANSWERS TO MY FOUR QUESTIONS — settled, do not reopen
1. **Keep `utils/gauge_windows.py`.** Its domain is the sensor value path shared by two analyses.
2. **Accept the replay-gate import now.** Extract `utils/protocol_p.py` when the Stage-A/B/C driver is the third consumer, and take that extraction through exact-state re-review because it edits the closed gate. **[S50: that extraction also removes Stage 0's only transitive `mujoco` dependency and requires a packet README Step 24 edit.]**
3. **Consecutive pairing approved** — it consumes `0..199` once and invents no grouping.
4. **No pre-review wall clock was needed.** Record elapsed time when the approved implementation actually runs. *(Not done at the S48 execution — see limitation 45. Do not re-run to manufacture one.)*

## CODEX'S S45 ANSWERS — settled, do not reopen
1. **Keep `_plant_payload` private.** The gate is deliberately coupled to the producer's exact serialization; import failure is appropriately fail-loud.
2. **No skip-if-absent integration test.** Green-by-skip on every clean checkout advertises coverage it does not provide.
3. **Keep `MIN_WATCHED_FILES = 100`** as an anti-vacuity lower bound, not a coverage claim.

## CODEX'S ENUMERATED STAGE-DRIVER REQUIREMENTS — carry these verbatim
Before any Stage-A/B/C rollout, the driver review must show fail-loud coverage that:
- constructs the full `ScreenOverrides` bundle from an explicit condition;
- enforces I3 and suffix-free I4 rather than allowing the dataset fallback;
- enforces I5–I8 and I13a before the rollout;
- keys results from the explicit Protocol-P condition, never the stale returned label;
- persists no `ObservedRecord`, label payload, manifest, role index, or dataset payload; and
- **tests the actual results-only output root so the no-dataset-artifact check can fail on a real wrong write.**

## Session 51 in one block — what was done and what it cost

**The gain: the public-README loop CLOSED, the extraction done and measured, the Stage-A/B/C
construction layer built and handed off, zero stage rollouts.**

1. **Closed the public README as owner** at `73b124fd…` after re-verifying the withdrawal's
   scope repo-wide (wider than Codex's file-wide search) — no third instance exists.
2. **Extracted `utils/protocol_p.py`** and rewired both consumers; `_require` is bound
   privately in each (`from utils.protocol_p import require as _require`) so NO call site moved.
3. **Built `utils/protocol_p_conditions.py` + 130 tests**; ran a 16-case mutation sweep; found
   and fixed a real gap in my own I3 tests.
4. **Edited packet README Step 24** (+1/−1) because the extraction made its dependency
   sentence false — that REOPENS the Step-24 loop — and **added one public-log entry**,
   because leaving the log saying "currently imports MuJoCo transitively" while the runbook
   said the opposite would ship two outward-facing documents disagreeing about one fact.

**Deliberately not done in S51:** did NOT re-run the pinned Stage-0 invocation; did not edit
the Stage-0 result artifact, the protocol file, the assignment, the draft config,
`utils/gauge_windows.py`, the detection-floor screen or its artifacts, the seam,
`.gitattributes`, or any payload; did not touch any dated public-log entry; did not build the
driver script, the output root, the persistence-boundary test, I12, the §9 label-stamp test,
or the I13a runtime call site; no new dependency.

**A SEQUENCING DEVIATION IS OPEN AND CODEX OWNS IT.** Its S46 answer 2 conditioned the
extraction on "the Stage-A/B/C driver being the third consumer." The driver SCRIPT does not
exist; the construction layer does and is a real third consumer. I led the handoff with the
deviation, gave three reasons, and handed Codex the decision. **If Codex reads the trigger as
the finished script, treat the extraction as premature rather than argue it.**

## Session 50 in one block — what was done and what it cost

**The gain: the Step-24 loop CLOSED, the public log's withdrawal correctly scoped, zero rollouts, zero source-file changes.**

1. **Re-reviewed as work, not verdict.** Codex's review was accurate and short; agreeing would have produced the identical approval with none of the evidence. Verifying each claim by construction cost ~10 minutes and produced two things agreement would not: the eight-import measurement, and the scope defect in the correction.
2. **Split the two findings by the same deciding question as S49** — does leaving it alone leave a false claim in front of a reader? Import depth: no (Codex's sentence is true, just less specific) → recorded and approved. Correction scope: yes (a withdrawn claim keeps standing in the public log) → edited and returned.
3. **Checked the reviewer's reasons, not only its edits** (Lesson 49). Three reasons, three clean answers — the value is that the record holds reasons that were checked rather than reasons that were plausible.

**Deliberately not done in S50:** did NOT re-execute Stage 0; did not edit the result artifact, either Stage-0 file, the three approved helper/floor files, the replay gate, the protocol file, the assignment, the draft config, `.gitattributes`, or any payload; **changed no source file at all**; did not build any part of the Stage A/B/C driver; did not touch any dated public-log entry; did not add a new public-log entry (heartbeat ran, correctly produced none); no new dependency; no mutation sweep (no code was patched).

## Scratchpad (S52, NOT committed)

`append_turn.py` (**copied forward and reused unchanged, sha256 `3cf26db962bf3accb97880d1343fe791129f3790db1d70b68fd58a552d26fa2d`; TEN sessions now** — find it with
`ls -1 */scratchpad/append_turn.py | while read f; do echo "$(sha256sum "$f" | cut -c1-16)  $f"; done | grep ^3cf26db962bf3acc`
under `C:/Users/cresp/AppData/Local/Temp/claude/C--Users-.../` before rebuilding),
`turn_s52.md`, `old_conditions.py` (`git show 794a666:<path>`),
**`probe_s52_findings.py`** — **the instrument worth rebuilding.** It loads a PRE-REVIEW module
beside the reviewed one *in one process* via
`importlib.util.spec_from_file_location("utils.<alias>", path)` + `sys.modules[name] = mod`, so
the extracted file's relative imports resolve **without putting a second copy in the repo**.
That is the general way to verify "did the old version really accept this?" by construction.
**`verify_s52_mutations.py`** (18-case sweep, `finally`-restore, explicit survivor list — the
S51 template, reused) and **`probe_s52_survivors.py`** (re-runs survivors against the FULL
suite, and supports MULTI-EDIT cases, which is what exposed the double-removal gap).

## Scratchpad (S51, NOT committed)

`append_turn.py` (**copied forward and reused unchanged, sha256 `3cf26db962bf3accb97880d1343fe791129f3790db1d70b68fd58a552d26fa2d`; NINE sessions now** — find it with
`ls -1 */scratchpad/append_turn.py | while read f; do echo "$(sha256sum "$f" | cut -c1-16)  $f"; done | grep ^3cf26db962bf3acc`
under `C:/Users/cresp/AppData/Local/Temp/claude/C--Users-.../` before rebuilding),
`turn_s51_approval.md`, `turn_s51_work.md`, `log_entry.txt`,
**`probe_imports.py`** (per-import subprocess sweep, rebuilt from S50's `probe_chain.py` — the
generic "does X really need Y" instrument, now also prints the gate's module namespace so a
refactor's public-surface delta is measurable),
**`probe_stage0_inert.py`** (calls `run_null` at `pairs=2` and diffs against the approved
artifact — the way to check a refactor without re-running a spent measurement),
**`verify_s51_mutations.py`** (16-case sweep over the patch; **the template to copy** — it
restores every file it touches and reports survivors explicitly), and
**`probe_survivors.py`** (re-runs a survivor against the FULL suite to tell a real gap from a
scope artifact — that distinction is Lesson 60 and the probe is worth rebuilding).

## Scratchpad (S50, NOT committed)

`append_turn.py` (**copied forward and reused unchanged, sha256 `3cf26db962bf3accb97880d1343fe791129f3790db1d70b68fd58a552d26fa2d`; it has now survived EIGHT sessions — find it with
`ls -1 */scratchpad/append_turn.py | while read f; do echo "$(sha256sum "$f" | cut -c1-16)  $f"; done | grep ^3cf26db962bf3acc`
under `C:/Users/cresp/AppData/Local/Temp/claude/C--Users-.../` before rebuilding**), `turn_s50.md`, `probe_import.py`, `probe_chain.py`, `probe_ulp.py`. **The three probes are the S50 instrument and are worth rebuilding rather than recalling: `probe_chain.py` (per-import subprocess sweep for a transitive dependency) generalizes to any "does X really need Y" question.** No mutation-sweep harness — nothing was patched. **If a future session patches code, rebuild the sweep; `verify_s48_mutations.py` from S48 is the template and is recoverable in shape from `HumanReport48.md`.**

## The escalation trigger — content-based, and it has now held six times

**The binding rule: escalate to the director when a round re-litigates a point already settled, or when we disagree on a judgment neither of us can resolve from source — NOT when a round finds a new, verifiable defect.** The specification loop ran seven rounds and closed at Codex's S43 approval. The seam-implementation loop closed in ONE round. The replay-gate loop closed in TWO. **The Stage-0 implementation loop ran THREE rounds and closed at my S48; the Stage-0 result loop closed at my S49; the progress-report loop closed at Codex's S49; the Step-24 loop closed at my S50 in ONE round.** Every round found something new, which is exactly the case the trigger does NOT fire on. **S50 exercised both edges in one session, as S49 did: the import-depth narrowing changes no shipped text → recorded and approved; the correction's scope leaves a withdrawn claim standing in front of a public reader → edited and returned.** If a round repeats a settled point — the two-domain hashing split, the window origin, the statistic, the ladder, the driver-vs-seam scope boundary, the three S45 answers, the four S46 answers, the reachability closure Codex accepted in its S47, or the identity-scope narrowing it accepted in its S49 — escalate on the spot regardless of count.

## HONEST ODDS — unchanged since S40

Against the S39 gauge-only measurement's bar, projecting the S35 amplitude ratio ×3.15 over 0.05 → 0.15 N (**importing that ratio across configurations remains the weakest link — the exact Lesson-11/12 move**):

```text
remEI 0.50   c4 1.502 vs 0.711 x2.11    remEI 0.75   c4 0.491 vs 0.711 x0.69
             c5 1.475 vs 0.850 x1.74                 c5 0.470 vs 0.850 x0.55
             c6 0.856 vs 0.635 x1.35                 c6 0.315 vs 0.635 x0.50
             c7 0.853 vs 0.771 x1.11                 c7 0.294 vs 0.771 x0.38
```

**remEI 0.75 fails everywhere by a wide margin — the one robust statement.** remEI 0.50 clears the binding cell by only **1.11×**, computed with an **inflated signal** (Finding L) against a **deflated bar** (the gauge-only decomposition omits closed-loop divergence) — both errors favour the hypothesis. **Case B (dev coverage 1) and Case C remain roughly comparable.** Stage C settles it.

**The success bar is UNTOUCHED** (≥0.05 macro-F1, −0.02 per-class recall non-inferiority, ≥10% tracking reduction, paired hierarchical bootstrap, ≥5 seeds).

*Naming note: "M2" is **retired inside the protocol file**, where it was ambiguous. Below it still labels **my** S39 measurement — the gauge-path-only decomposition. Keep the two straight; if writing anything Codex will read, spell it out.*

## The two zero-rollout measurements from S39 (still valid)

**M1 — the observed path barely degrades a MATCHED difference.** Both delivered plant traces of a pair re-observed at ONE common identity, 6 identities. Isolates quantization/dropout/latency/hysteresis/bias/drift.
```text
setting        cell   D_true   D_obs mean   ratio        setting     cell  D_true  D_obs mean  ratio
remEI 0.50      4     0.4787     0.4768     0.996        remEI 0.75    4   0.1584    0.1559   0.984
remEI 0.50      5     0.4755     0.4683     0.985        remEI 0.75    5   0.1593    0.1492   0.937
remEI 0.50      6     0.2755     0.2717     0.986        remEI 0.75    6   0.0872    0.1001   1.148
remEI 0.50      7     0.2798     0.2709     0.968        remEI 0.75    7   0.0968    0.0934   0.965
```
**0–6% cost on average, ±10% spread; at small `D` the residue moves EITHER way.**

**M2 — the gauge-path-only component of the Stage-C null.** One delivered healthy plant trace per cell held EXACTLY fixed, redrawn at 8 identities, all 28 within-cell distances, `method="higher"`.
```text
cell   min / median / max           Q95 (27th of 28)   2*Q95
 4     0.1540  0.2807  0.3731            0.3555        0.7110
 5     0.1524  0.2620  0.4325            0.4251        0.8502
 6     0.1377  0.2709  0.3922            0.3176        0.6351
 7     0.1443  0.2983  0.4706            0.3854        0.7708
```
**A decomposition, NOT a bound.** It **validates Stage 0** (synthetic no-plant value sits inside the real-plant 0.318–0.425 — written into spec §8, and the S46 Stage-0 script computes this containment check explicitly with an `authority: NONE` field) and identifies **cell 7 (payload + warm + contact) as the binding cell**. **Conditional healthy-null diagnostic only — no mechanism attribution.**

**The enabling tool (S39, reconfirmed S40/S41/S45/S46).** `SensorModel().observe(delivered_plant, "S", pair_id=<manifest>, sensor_seed=<manifest>)` reproduces the delivered row **bit-for-bit without running any simulation**; a perturbed `pair_id` moves `gauge_obs` by up to **6.50 µε** (against `D` of order 0.1–0.5). **Any stored plant trace can be re-drawn on the observed path at any identity for free.** S45 extended this: the whole rollout, plant included, also reproduces exactly, and S46 reconfirmed it twice.

## GATE STATUS — the freeze path (central reference)

**Governing decision: `BLOCK_CONFIG_FREEZE_PENDING_PRECONFIRMATORY_BUILD_AND_VALIDATION`.** A **versioned DRAFT config** governs dev/val generation; the **final immutable `config.json` freeze comes AFTER model implementation + validation-only hyperparameter/threshold selection and BEFORE any untouched `test` payload.**

1. **Machine schema + config authority** — **DONE, APPROVED S28.** *(Codex/shared.)*
2. **Role-separated storage, deployable loader, leakage/split audits** — foundation DONE (S28), role-write DONE (S29), **real generator + base roles APPROVED (my S33)**, **generator hardening APPROVED (my S34)**. **STILL OPEN OVERALL:** `estimator_outputs` + `controller_logs` roles await the Gate-4 fits. *(Codex/shared.)*
3. **Multi-setting design + manifest** — was CLOSED at 808 reservations; **A2 reopens it** (full regeneration, new assignment, new hash). *(shared)*
4. **Matched learned models** — **MINE. GATED BY Protocol P v2.3.3, then the written A2.** `TemporalAttributionNet` + `RMALatentEncoder` behind shared `[W,D]`; within-suite capacity ladder; ≥5 seeds; identical protocol IDs across C0/C1/S. Toolchain verified (torch cu128 / sm_120).
5. **Calibration/abstention/OOD/uncertainty** — **MINE.** Per-suite calibrated probs (Brier/NLL/ECE), abstention + OOD thresholds on validation, `severity_uncertainty` as a **bias-inclusive predictive error scale** (NOT in-sample residual dispersion — S24: understates true by 5.72× for S). **Validation must NOT be touched until Gate 4 opens.**
6. **Confirmatory controller protocol** — **DECIDED S27 (both agents):** freeze the fair four-arm comparison (no-action/detection-only · transparent attribution-driven · RMA · oracle) and **RUN the pre-registered paired C1-vs-S comparison**; do NOT narrow to information-only, do NOT retune blocked families post-hoc. *(Codex owns controller; diagnosis→control seam shared.)*
7. **Evaluation driver + confirmatory manifest** — **MINE.** One CLI owning the `[t_c,t_c+5s]` slice, role joins, paired C1/S table, exclusions, CIs; rejects `dev-`/wrong-hash/cross-role/incomplete-pair/truncated. **Must implement pre-registered statements:** (a) `ood_flag` exclusion from known-class metrics; (b) the **degradation-ladder rule** (S30/S31); (c) **pilot→val moves one variable while val→test additionally moves half-fraction → complete factorial** — *and, under A2 pin 4, no longer moves the contact window*; (d) S33's two findings; (e) the mild-stratum development diagnostic **at its true scope** (dev contexts, EI 0.75/0.50) and the per-channel attribution; (f) **[S35]** the excitation discontinuity; (g) **[S36]** the yardstick discontinuity (D) + the run-to-run range statement (E) + trajectory-partial margin coverage; (h) **[S37]** the operation mismatch (F), thermal near-invariance (G) as a *property*, the amplitude ceiling (H); (i) **[S38]** the **window origin (J)** — the driver MUST use the same origin the protocol pins, since nothing in the codebase fixes it; plus the matched/unmatched asymmetry and role-coverage counts; (j) **[S39]** the **construction path (K)** — build/read records by the same C0-loop-then-post-hoc-observe path — and the **unmatched-identity confound (L)**, which governs how any delivered-row magnitude may be quoted; (k) **[S40]** if the seam ships, the driver must distinguish **`base_pair_id` from realized `pair_id`** in every identity join and audit, and must never stamp an overridden run with the base config hash; (l) **[S41]** any file whose **raw bytes** enter an identity or a verification pin must be hashed through the correct-domain helper; (m) **[S42]** and that helper must be chosen **by file domain** — text files fold CRLF, binary files never do; any driver-side byte pin must name its domain explicitly; (n) **[S43]** every identity expression in the driver must **name the object it hashes**, and the recorded canonical string must be the *same object* that was hashed; (o) **[S44]** the driver must be tested for the **wires between its stages**, not only for each stage's own behaviour; (p) **[S45]** every driver check that reports a clean result must **disclose its denominator** — and must refuse to report at all when that denominator cannot support the claim; (q) **[S46]** every driver guard must be **reachable from the construction that will run**, and where it is not, the guard must be extracted so the rejected state can be fed to it and the call site wire-tested — plus **every driver test fixture must be large enough for the defect it is meant to expose**; (r) **[S47]** every value the driver pins as a literal must be checked against the bound document wherever that document also carries it — by EQUALITY, never by adoption — and every such guard must state whether it is reachable from the construction that will run; (s) **[S48]** every driver test that claims to verify a production gate must CALL that gate rather than reimplement its arithmetic, and must assert the REASON for a refusal (a `match=` on a phrase unique to one raise site), not merely that a refusal occurred; **(t) [S50] every dependency, invariant or capability the driver's documentation claims must be verified against the running system rather than against the design — an import-only load of the driver module is enough to settle "does it need X", and the answer belongs in the runbook in the form a reader can reproduce; (u) [NEW S51] every driver test must assert a phrase UNIQUE TO ONE RAISE SITE, because a function with two raises that both name the same invariant will keep passing a label-matching test after the guard under test has been weakened — and the driver must construct its own preconditions through `utils/protocol_p_conditions.py` rather than re-deriving identities, conditions or provenance locally; **(v) [NEW S52] the driver must obtain its source reservation from the I1-pinned assignment document and never construct one — the cell binding in the construction layer is over three identifier strings, not over the `(payload_id, env_profile_id, contact_profile_id)` triple that physically defines the cell, and it is I1's byte pin plus `_context_cell_table`'s rotation check that binds the body; and every guard the driver adds needs a test per BRANCH, not per guard.**

**Order:** (1)✓ → (2 foundation)✓ → (2 role-write)✓ → (3 assignment)✓✓ → (2 generator + base roles)✓✓ → (2 hardening)✓✓ → (dev separability check)✓ **[NEGATIVE]** → Protocol P v2.3.3 spec ✓✓ → seam patch + 37 tests ✓✓ → replay gate run + implementation ✓✓ → Stage-0 implementation, three rounds ✓✓ **[LOOP CLOSED, my S48]** → **Stage 0 RAN, S48, Q95 0.400881, zero rollouts ✓** → **Stage-0 result JOINTLY APPROVED, my S49 ✓✓** → **Progress Report S48 JOINTLY APPROVED, Codex S49 ✓✓** → **packet README Step 24 JOINTLY APPROVED, my S50 ✓✓** → **public README JOINTLY APPROVED, my S51 ✓✓** → **S51 BUILD: `utils/protocol_p.py` extraction + `utils/protocol_p_conditions.py` construction layer + 130 tests** → **Codex S51 review: 4 states APPROVED UNCHANGED, 2 BLOCKING findings, 4 files reviewer-edited** → **my S52 owner re-review: both findings CONFIRMED BY CONSTRUCTION, construction module + shared test file APPROVED UNCHANGED, construction TEST FILE edited and returned on five unexercised guards [CODEX OWNS THIS TURN] ← WE ARE HERE** → Stage A/B/C DRIVER SCRIPT (output root, persistence boundary, I12, §9 label-stamp test, I13a call site) → Codex reviews implementation + result + branch → written amendment + replacement assignment (both approve) → **full regeneration from zero** → re-audit → (4/5 models+calibration) [me] → (2 remaining roles) [Codex] → (6 controller + sample-size) [shared] → **joint immutable freeze** → one-shot confirmatory generation + eval (7) → Phase 3.

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
- **Load one observation:** `ObservedRecord.load_npz(root/"observations"/suite/f"{run_id}.npz")`. Fields: `suite, run_id, pair_id, config_hash, values, valid_mask, measurement_time_s, availability_time_s, latency_age_s, suite_available_mask, schema_version, split`. **`values` and `valid_mask` are DICTs** channel → `[T, width]`. **`measurement_time_s` / `availability_time_s` / `latency_age_s` are DICTs of RANK-1 `[T]` arrays.** Gauges are `values["gauge_obs"]` `[T,4]`. **`config_hash` is a STORED field — what gets stamped changes the artifact's bytes (this is why the replay must stamp base).**
- **`ObservedRecord.to_npz_dict()` is the 38-entry serializer** (8 metadata + 5 per-channel dicts × 6 channels). npz keys are prefixed: `values__`, `valid__`, `meas_time__`, `avail_time__`, `latency__`. **`_plant_payload(record)` in the generator is the 20-key plant serializer** — use it rather than re-deriving from `dataclasses.fields`. **Codex's S45 answer: keep that import private.**
- **Load one plant trace:** `PrivilegedRecord.load_npz(root/"plant"/f"{run_id}.npz")` (`utils.schema_types`).
- **Re-observe any plant trace offline, no simulation:** `SensorModel().observe(plant, "S", pair_id=..., sensor_seed=..., fault=None, run_id=..., config_hash=..., split=...)` — verified bit-identical at the manifest identity (S39/S40) and confirmed suite-order-independent (S45).
- **These `.npz` are ZIP archives and DO contain CRLF byte pairs as payload (18 and 1 in the two pinned replay references). Never hash one through a text canonicalizer.**
- **Plant fields (20):** step, t_s, q_true, qd_true, qdd_true, tau_cmd, tau_delivered_true, deform_coords[90], curvature_true[4], gauge_true[4], imu_true[6], temperature_true[4], contact_state[2], task_reference, true_task_output, tracking_error, tracking_error_norm, control_effort, saturation_flag[2], safety_flag[7]. **`contact_state[:,0]` = summed force N, `[:,1]` = active flag.**
- **Registry D = 18:** q_obs[2], qd_obs[2], tau_cmd[2], current_proxy_obs[2], imu_obs[6], gauge_obs[4]. **C1's `gauge_obs` is all-NaN, mask False. S `gauge_obs` CONTAINS NaNs (dropout/latency) — use nan-aware statistics.** Measured S45 on one delivered S row: **531 NaN values across 5 of the 38 entries.**
- **Label fields:** source_class, subtype, location, severity, onset_index, onset_time_s, compound_flag, ood_flag.
- **Run lengths / timing:** `trajectory_dev_ordinary_a` (`t00`) 2900 steps, onset 400, **no probe**; `trajectory_dev_diagnostic_b` (`t01`) 3000 steps, onset 500, **probe steps 1000→1625**. Both carry 76 rows per suite. **Only `t01` has a probe.**
- **`assignment["trajectory_specs"]` is a LIST of dicts keyed by `"id"`, not a dict** (`_catalog()` builds the mapping). Same for `context_profiles`, whose keys are `payloads` / `environments` / `contacts`.
- **dev fault settings (t01):** `fault_dev_healthy` (f000); `fault_dev_structure_link_stiffness_loss_loc1_sev0p5` (f001); `..._sev0p75` (f002); then actuator loc0/loc1 × {0.5,0.75}; then sensor bias/drift/dropout × loc{0,1} × 2 sev. **Severity strings use `sev0p05`, not `sev0p5`, for 0.05 — query the assignment, do not recall it.**
- **The replayed reference row:** `scenario_dev_t01_f000_r00` → `pair_id basepair_dev_t01_f000_r00_dataset0`, `run_id scenario_dev_t01_f000_r00_S_dataset0`, `sim/fault/sensor/controller = 110760/110761/110762/110763`, `payload_dev_nominal`, `env_dev_iso25c`, `contact_dev_brief`, `fault_dev_healthy`, 3000 steps, 0 safety events, **0 contact steps**.
- **Two runs in the same context cell differ in sensor_seed, and the closed loop amplifies that into gauge variation that EXCEEDS the structural fault signature (S36 Finding E).** Any fault-effect *magnitude* measurement MUST match both `sensor_seed` AND realized `pair_id`. Separability measurement must NOT (that is the point). **Delivered fault and healthy rows do NOT share identity (S39 Finding L) — so any delivered-row magnitude is `||fault + divergence||`, on BOTH the privileged and observed paths.**

## Codex's Gate-1/2/3 layer — reference

`Reproducibility Packet/`:
- **`schema/schema.json`** (S28) — machine schema v1.0 + A1. Roles: identity_manifest, plant (20 fields = `PrivilegedRecord`), observations (deployable, fixed 6-channel registry + static suite mask), labels (8), estimator_outputs (9), controller_logs (6). `schema_sha256 = 0dae0dd0fec4269180139efc9a4c9ce38e7f8f23d890d182dc8eb063803e942f` (LF-pinned via root `.gitattributes`).
- **A1 safety envelope (schema-v1.0.md §Amendment A1):** `|q| ≤ π rad`, `|qd| ≤ 10 rad/s`, tip radius ≤ 0.82 m, `|gauge_true| ≤ 500 µε`, tip contact force ≤ 5 N; `safety_flag[T,7]` fixed order (joint_angle_0/1, joint_speed_0/1, tip_workspace, gauge_abs, tip_contact_force) computed in `cable_plant.py:_safety_flags` (line 272, called 377); `saturation_flag[T,2]` separate. Computed from privileged truth, never from a corrupted observed channel.
- **`config/draft-config-v0.1.json`** — the DRAFT, **CRLF in the working tree**. **`config_hash = dev-712abf27c3f8f3c331ae9b76e3f22c48857334cc15a81e819718165e47753e56`** (parent `dev-0211f2e71a473fef3c30cd53fd0a269df45156a3d58e83097bac7a5638bf6180`), computed over `canonical_json_bytes(document)` so it is EOL-immune — **which is exactly why it is deliberately NOT byte-pinned**. Embedded assignment hash at `/values/scenario_manifest/approved_assignment_hash`. Frozen candidates: plant (`n_def=90`, gauges [0.25,0.75], A1 thresholds, `point_count_per_link=17`, `simulation_timestep_s=1e-4`, `endpoint_contact_plane_z_m=0.2`), timing (`f_ctrl=500`, `control_dt_s=0.002`, `window_steps=768`, `stride=16`, **probe 0.05 N / 0.8 Hz / 1 cyc raised_cosine — RAMP UNPINNED, S35 Finding A**, `analysis_window_s=5.0`), sensor_model (**gauge noise 1.0 µε, thermal 10 µε/°C, ref 25 °C, bias 0.5 µε, drift 0.2 µε/√s, hysteresis 0.15, quant 0.5 µε, latency 0.002 s**).
- **`config/proposed-gate3-assignment-v0.1.json`** — **LF-pinned (S41)**. Canonical/raw SHA-256 `76255a8089f3e27d893b26d981cbf50e808bd75ba518c44b55c4635ec83514ae` (22,760 bytes; independently reproduced by Codex S42, the replay gate S45, and a permanent test in each of my two S46 test files); **its CRLF rendering is `00dacaf6277d6b274e3690ab3d3f68607eb61a22fe0df75ea8688fe4c7d4f87f`** — always hash through `canonical_text_sha256`. `assignment_hash = dev-eec59ec8a296a9a4ff4909f8e7f1de91a0a8f4bf289ae1533a427d1a87bc33f1`. Top keys include `trajectory_specs`, `fault_grid_by_split`, `compound_ood_settings`, `context_profiles`, `generation_plan`. **Superseded, never approve:** `dev-70832daa…765de` (656) and `dev-5939ff5f…0cedb` (blocked S30). Probe `start_offset_s` per split: **dev 1.0, pilot 1.2, val 0.9, test 1.1 — offsets FROM ONSET (Finding J).**
- **`scripts/utils/assignment_binding.py`** — `embed_approved_assignment_document` / `validate_approved_assignment_binding(config, *, expected_assignment)` — **`expected_assignment` is REQUIRED.** Returns an `ApprovedAssignmentBinding` whose **`.assignment_hash` property** is the document-derived `dev-eec59ec8…` (this is how Stage 0 gets it). `AUTHORIZED_RESEARCH_SPLITS = ("dev","pilot","val")`.
- **`scripts/utils/assignment_generator.py`** — `RESEARCH_SPLITS=("dev","pilot","val")`, `BASE_DATASET_SUITES=("C0","C1","S")`; `GenerationRuntimeParameters(control_dt_s, f_ctrl_hz, simulation_timestep_s, point_count)` + `_runtime_parameters(binding)`; **the S44 seam at the top: `ScreenOverrides` (frozen, 5 fields, `is_active()`), `screen_pair_id` (105), `_screen_stamped_hash` (122)**; `_step_index` (217) fails loud off-grid; `build_identity_manifest` (261) — **requires `{"C1","S"} ⊆ suites`**; **`audit_manifest_against_assignment` (321) — the two tested leak tripwires**; `_profile` (382), **`_physical_config` (401; `overrides=`; the ramp default `duration/2.0`)**, `_temperature_function` (474), `_fault_components` (500), `shared_channels_equal` (542), `preflight_assigned_mechanics` (560), **`_plant_payload` (600) — the 20-key plant serializer**, **`_generate_reservation` (607; 7 positional + keyword-only `overrides`; RETURNS a 6-tuple `(control_pair_id, result.plant, observations, label_payload, safety_count, contact_count)` — the CablePlant is NOT returned)**, `materialize_base_dataset` (731), `audit_materialized_base_dataset` (838). `ESTIMATOR_ID="gate4_unfit_shared_capacity_v1"`, `CONTROLLER_ID="bounded_observed_pd_no_recovery_v1"`, `DATASET_IDENTITY_TRAIN_SEED=0`. **Line 24 `from .cable_plant import CablePlant` is the link that makes every importer of this module a transitive `mujoco` importer (S50).**
- **`scripts/utils/gate3_assignment.py`** — `load_assignment`; `expand_reservations(document)` → `list[ScenarioReservation]`. **Lines 648-697** are the seed/ordinal/context-cell derivation: `seed = seed_base + 10*ordinal`, `sim/fault/sensor/controller = seed+0/1/2/3`, `base_pair_id = basepair_{split}_t{ti:02d}_f{fi:03d}_r{rr:02d}`, realized dataset `pair_id = base + "_dataset0"`. Ordinal nests (trajectory, fault, replicate), resets per split.
- **`scripts/utils/storage_contract.py`** — `IdentityManifestRow` (20 fields), `IDENTITY_MANIFEST_FIELDS`, `DeployableObservationLoader`, **`_valid_config_hash` (103-109) strips exactly `dev-` then `re_full_sha256` (364-367) requires 64 lowercase hex.**
- **`utils/config_contract.py`: loader is `load_config(config_path, schema_path, *, require_frozen=False)`.** `ValidatedConfig`: `source_path, schema_path, document, config_hash, status`. `file_sha256` (45) is a **RAW-byte** hash — do not use it on an unpinned text file; `canonical_json_bytes` (78) + `sort_keys`/`separators`/`ensure_ascii=False`/**`allow_nan=False`** is the document path and the canonical-JSON precedent Protocol P matches (spec §0 cites it by line); `config_hash` at 99.
- **`utils/sensor_model.py`** — `config_hash` is **free-form provenance, never validated** (`:235, :253, :612, :641`), which is what makes the derived screen-provenance stamp safe. Temperature reaches the gauges at `:423-424` (10 µε/°C); the 0.5 µε quantizer is at `:429-431`. **Carries no state across `observe` calls (measured S45).**
- **Rollout entry point is `utils/online_loop.run_online_rollout(plant, sensors, *, n_steps, history_steps, command_policy, reference_fn=None, temperature_fn=None)`** (there is no `utils/rollout`).
- **Assignment structure:** 19 known settings per split (1 healthy + 2 structure loc1 + 4 actuator loc{0,1} + 12 sensor {bias,drift,dropout}×loc{0,1}×2 sev), +2 compound/OOD in val/test; **2 trajectories per split** (ordinary + diagnostic), split-exclusive; realizations 4/4/4/8; seed bases 110000/210000/310000/410000; reservations **152/152/168/336 = 808**. Expansion order **healthy → structure → actuator → sensor** — **extending `grid["structure"]["severities"]` shifts every later ordinal and therefore every later seed**, which is why Codex chose full regeneration.
- **Structural severities by split: dev {0.75, 0.50}, pilot {0.85, 0.60}, val {0.90, 0.40} + OOD 0.55; test {0.65, 0.35} + OOD 0.45.** Payloads: dev {0.000, 0.050}, pilot {0.025, 0.075}, val {0.100, 0.125}, test {0.150, 0.200} kg.
- **Context cell table** (index `(trajectory_index * realizations + replicate) mod 8`), each `[payload_idx, env_idx, contact_idx]`: `0:[0,0,0] 1:[0,1,1] 2:[1,0,1] 3:[1,1,0] 4:[0,0,1] 5:[0,1,0] 6:[1,0,0] 7:[1,1,1]`. `t00`→{0,1,2,3}, `t01`→{4,5,6,7} (verified row by row, S36).
- **Contact profiles:** dev_none `null`; dev_brief `[2.0,2.5]`; pilot_none; pilot_delayed `[2.6,3.2]`; val_none; val_extended `[1.8,3.3]`; test_none; test_sustained `[1.6,3.8]` → **A2 pin 4 changes this to `[1.8,3.3]`**. Offsets are relative to onset (`_physical_config`). All non-null profiles use `endpoint_plane_z_m = 0.2`.

## My lanes — current state

`Reproducibility Packet/scripts/utils/estimator.py`:
- **`WindowFeatureExtractor(window_steps=W=768, probe_frequency_hz=0.8)`**: `window_tensor(record)` → `(values[W,D], valid[W,D])` NaN→0 + mask; **requires `record.n_steps <= W` and right-aligns (`estimator.py:366-375`) — it refuses a full run, so the caller owns the window origin**; `window_features(record)` → per-column `[last,mean,std,slope,sync_cos,sync_sin,sync_amplitude,valid_fraction]` over the 18-col registry → 144 features. `N_FEATURE_STATS=4`, `N_EXTRA_FEATURES=4`, sync cols 4/5/6, `VALID_FRACTION_COL=7`, `DIAGNOSTIC_PROBE_HZ=0.8`, `MIN_SYNC_SAMPLES=8`. **The only two function-level imports in the packet are here, lines 1299 and 1346, both `utils.schema_types` (measured S46).**
- **`synchronous_coefficient_vector(record, extractor)`** → the suite's live channels' (cos,sin) pairs; **the last `2*4=8` entries are the gauge columns for S**. **`coefficient_reference_distance(v, mean, scale)`** is scaled/normalized — for raw µε use `np.linalg.norm(v_fault[-8:] - v_healthy[-8:])`.
- **`WindowNoveltyDetector`** · **`CoefficientReferenceDetector`** (`fit_reference` atomic; `calibrate_threshold` fail-loud below `ceil(min_tail/far)`; `_scale_from(mean,std)`) · `_SCORE_STD_FLOOR=1e-3` shared · **`SeverityRidgeHead`** (`train_residual_std` is IN-SAMPLE — never feed a confidence gate) · `leave_one_group_out_residuals` (CALIBRATION-role diagnostic) · `OracleInterface` · `EstimatorCommandPolicy` · `RECOMMENDED_WINDOW=(768,16)` · **learned rungs specified-not-built (Gate 4).**
- **`utils/synchronous.py`** (Codex, S9) — `harmonic_coefficients(window, valid, time_s, frequency_hz)` returns `[cos, sin]` from a **least-squares fit with intercept + centred linear trend** (design `[ones, centered_time, cos, sin]`); `harmonic_amplitude` is the L2 norm of that **single-channel** pair. Requires ≥5 finite valid samples; fails loud on rank deficiency or non-increasing time. **Because `[ones, centered_time]` span a linear-in-time thermal ramp, such a ramp contributes exactly zero to `(cos,sin)` in exact arithmetic — quantization is what breaks it (S38 correction to Finding G).**
- **`utils/metrics.py` + `utils/stats.py`** (approved through S11): `tracking_reduction_pct`, `j_5s` fail-loud on full `[t_c,t_c+5s]`, `safety_incident_rate`, `safety_flag_rates`, `safety_regression_delta`, `hierarchical_bootstrap_ci` (crossed pair×seed). **Eval driver (Gate 7) — build once the frozen layout exists.**
- **Screens (all closed):** `screen_severity_estimation_quality.py`, `screen_severity_action_boundary.py`, `screen_actuator_probability_channel.py`, `tests/test_recovery_seam.py`, **`screen_structural_separability.py` (S34, report corrected S35; packet-README Step 22)**.
- **`analyze_synchronous_detection_floor.py`** — mine, **MODIFIED S46** to import the lifted helper (`gauge_window`, `linear_thermal_profile`) from `utils/gauge_windows.py` and pass `pair_id=SCREEN_PAIR_ID` (=1) explicitly. **Both published artifacts re-verified BYTE-IDENTICAL after the change.** Still carries **two usage corrections**: it publishes `detect_threshold_microstrain = nes_mean + 5*nes_std`, **per gauge**, at `--window 640`, `--thermal-ramp-c 3.0`, 200 realizations, `--seed 0`. **It is a threshold, not a floor (S36); and it is the null of a SINGLE window, not of a difference (S37).**
- **Mine, Codex reviews: `Reproducibility Packet/protocol/protocol-p-v2.3.3.md`** — the pre-registration artifact. Also mine to maintain: the **two-domain hashing convention** in its §0 and Corrections 3/4, the `CANONICAL_JSON` rule in Correction 2, and the **identifier-binding discipline** in Correction 8.
- **Co-owned with Codex (S43): `tests/test_cable_plant_softening_boundary.py`** — the permanent I13b guard. 6 tests. **Codex's call if the two ever conflict.**
- **The S44 seam inside Codex's file: `scripts/utils/assignment_generator.py` + `tests/test_assignment_generator_screen_overrides.py` (37 tests). APPROVED AT EXACT STATE BY CODEX (S44).** Blobs `1c565888…` and `2ec96c9f…`.
- **`scripts/protocol_p_replay_gate.py` + `tests/test_protocol_p_replay_gate.py` (36 tests) — JOINTLY APPROVED, my S46.** Public API: `canonical_text_sha256`, `raw_file_sha256`, `check_pinned_digests`, `load_npz_entries`, `compare_entry`, `compare_payload`, `compare_manifest_row`, `inventory(roots, *, shallow_roots=())`, `diff_inventory`, **`require_no_inventory_changes`**, `read_manifest_row`, `run_replay`, `ProtocolPError`, `_require`, `MIN_WATCHED_FILES`, and the six pinned digest/filename constants. **Re-run it after any generator change — it is a free bit-level regression test on the ordinary path.** **[S50] This module is the sole reason Stage 0 transitively imports `mujoco`.**
- **STAGE 0 — IMPLEMENTATION JOINTLY APPROVED (my S48), RUN ONCE (S48), RESULT JOINTLY APPROVED (my S49), RUNBOOK STEP 24 JOINTLY APPROVED (my S50).** Artifact tracked at `results/protocol_p/sensor_only_difference_null.json`. **`scripts/analyze_synchronous_difference_null.py`** + **`scripts/utils/gauge_windows.py`** (`gauge_window(*, signal_true, temperature_true, f_ctrl, sensor_seed, pair_id, config)`, `linear_thermal_profile(n_steps, ramp_c, *, n_gauges=4, reference_c)`) **+ `tests/test_synchronous_difference_null.py` (99) + `tests/test_gauge_windows.py` (18)**. Stage-0 public API: `canonical_json`, `pair_seeds`, `coefficient_vector`, `difference_statistic`, `verify_text_pins`, `require_valid_stage_0_identity`, `stage_0_identity`, `require_unique_seeds`, `summarize_null`, `run_null`, `build_document`, `parse_args`, `main`; constants `STAGE`, `OUTPUT_FILENAME`, `N_STATISTIC_ENTRIES`, `REAL_PLANT_FIXED_TRACE_Q95_BY_CELL`, `OUTPUT_TOP_LEVEL_KEYS`, `PINNED_CLI`, `CLI_TO_BOUND_TIMING_PATH`; plus `require_pinned_cli`, `sensor_config_from_document`, `require_bound_timing_matches_cli`.
- **Not yet built:** the Stage A/B/C **driver script** itself — its results-only output root and the test that it writes no dataset-role artifact, I12's hard gates over the returned `PrivilegedRecord`, the §9 label-stamp scope-condition test, `screen_physical_faults`, and the I13a runtime **call site** (the check itself now exists in `utils/protocol_p_conditions.py`). All of these need the output root or a real rollout to exist.

## Codex's OTHER lanes — current state

- `utils/cable_mechanics.py` — `CableModelConfig`: `link_length_m=0.40`, `link_thickness_m=0.004`, `distal_payload_mass_kg`, optional absolute `endpoint_contact_window_s`, `diagnostic_tip_load_{peak_n,frequency_hz,start_s,duration_s,ramp_s}`; `structural_ei_remaining` default **0.50**; `control_dt_s` default **0.002**; `endpoint_contact_plane_z_m` default 0.498 (assignment uses 0.2). **`diagnostic_tip_load_envelope` (`:444-454`) requires the ramp finite and ≥0, requires a duration if non-zero, and raises when `ramp > duration/2` → admissible fraction `(0, 0.5]`.** Probe local time is `time_s - diagnostic_tip_load_start_s` (466, 488).
- `utils/cable_plant.py` — `CablePlant(config, *, point_count=17, simulation_timestep_s=1e-4, fault=None, additional_faults=())`; scheduled contact; compound physical faults. **`import mujoco` at line 15. No RNG anywhere in the file (verified S37)** — which is why S41's gate measurement is identity-independent. **A structural fault does `dataclasses.replace(config, structural_ei_remaining=severity)` → `self._physical_config` (`:99-103`) and builds a SECOND softened MuJoCo model at `:118-121`; the healthy plant has `_soft_model is None`. `_softened` initialized False at `:117`, set True in `_activate_structural_fault_if_needed` (`:186-198`), called from `advance` at `:328` BEFORE the physics step and BEFORE `_step_index += 1` at `:405`. `_fault_active` (`:179-184`): `onset = max(int(fault.onset_index), 0); return self._step_index >= onset`.** The `structural_ei_remaining=0.50` dataclass default is INERT in the healthy branch — do not quote it as a healthy stiffness (S40). Fault severity **is** the remaining-EI fraction. **`cable_plant.py:124-125` restricts structural faults to location `{-1,1}` and severity to `(0,1]`** (verified S30 — a genuine plant constraint; do not re-litigate). Actuator severity = remaining gain fraction, location = joint index; applied at `:333-336`. **`rollout(n)` cannot be called twice on one plant** — `PrivilegedRecord`'s validator requires a contiguous 0-based step grid (S43).
- **`utils/schema_types.py`** — `N_JOINTS = 2` (line 38); `FaultSpec` (65-79): `source_class="healthy", subtype="none", location=-1, severity=0.0, **onset_index=-1**, compound_flag=False, ood_flag=False`. **That `-1` default is the S41 defect's origin, and is now pinned as behaviour by the S43 test.** `PrivilegedRecord` (123; 20 fields; `save_npz` 284, `load_npz` 297), `ObservedRecord` (`to_npz_dict` 443, `save_npz` 466, `from_npz_dict` 474, `load_npz` 496). Also exports `N_GAUGES`, `PlantStepState`, `observable_step_sources`.
- `utils/task_control.py`: `BoundedTaskProfile`, `ObservedJointPDController` — **`proportional_gain=(0.05,0.03)`, `derivative_gain=(0.005,0.003)`, `torque_abs_limit=(0.20,0.10)`**; reads ONLY `q_obs`/`qd_obs`. (`torque_abs_limit[0]=0.20` is what makes Finding H's 0.15 N ceiling.)
- `utils/recovery_control.py` — `GainScheduledRecoveryController`; `screen_actuator_recovery_action.py` (S25) → `BLOCK_ACTUATOR_ACTION_FAMILY_AT_SOURCE_SPECIFIC_GATE`; `screen_structural_recovery_action.py` (S20) → `BLOCK_STRUCTURAL_RECOVERY_ACTION_FAMILY`; `screen_fault_tracking_deficit.py` (S22); `run_bounded_noisy_information_review.py` (S19): S macro-F1 0.995 / C1 0.704.
- **`screen_synchronous_safe_probe.py`** — loads `window_samples` AND `detect_threshold_microstrain` from the floor summary JSON, so it is **internally coherent** (W=640, per-gauge, max-across-gauges). `--ramp-period-fraction` default **0.125**; **`--peak-loads-n` default `[0.05, 0.1, 0.15]`**; `--fault-onset-s` default 1.0 and it slices `post[:window_samples]` from onset — **correct there, because this screen puts the probe AT onset (Finding J)**. It measures the **privileged** `gauge_microstrain` difference, not the observed path. **Still reads the floor summary, so my S46 lift must not change that JSON — verified byte-identical.**
- `agents/Codex/Config Freeze Readiness Review.md` = the seven-gate plan (I approved S27).

## The evidence tables (development-evidence boundary)

**Structural (Codex S20):** remaining EI 0.50/0.25/0.10/0.05 → mean peak |gauge| 38.4/72.4/152.8/259.7 µε (healthy 19.2) but mean **joint** tracking deficit +0.08%/−0.89%/−2.23%/−5.00% — monotone in information, monotone the WRONG way in joint control (damage moves to the TIP, which the joint score never measures). **Use the direction, never the magnitudes.**

**Control-layer shape (Codex `bounded_noisy_information_review`):** healthy/actuator/sensor → S has no exclusive info + 0% tracking change; **structure → S exclusive info YES, C1 withholds actionable, `s_tracking_change_pct` −18.58%.** C1 per-class recall: structure **0.083**, else 1.000. **NOTE: ONE fixed fault setting per class at a severity far more severe than the reserved grid, at the screened (0.15625 s) ramp not the delivered one, under a per-gauge/W=640 yardstick, on a single-window statistic, with the probe at onset.** Every pre-dataset screen's absolute µε values belong to a different configuration than the delivered runs.

## The agreed contract's load-bearing specifics

- **Sensor suites (controlled variable):** C0 = joint encoders + commanded actuation · **C1 = C0 + noisy motor-current nominal-Kt torque estimate + one distal 6-axis IMU** · **S = C1 + four fixed strain/curvature gauge stations** · O = privileged oracle. **Temperature is observable ONLY through `gauge_obs`, i.e. only in S** (`sensor_model.py:423-424`, 10 µε/°C). **The closed loop is driven by a C0 session in every suite — the suites differ only in what is OBSERVED post-hoc (S39 Finding K).**
- **Two settled correctness points:** actuator-gain fault acts *downstream* of the current proxy; encoder fault has a *relational* signature.
- **Success bar (pre-declared, BOTH layers, UNCHANGED by A2):** S improves held-out four-way macro-F1 over C1 by **≥0.05 absolute** (paired 95% excludes zero; every source-class recall diff lower-95% above **−0.02**) AND reduces the **5-s post-change integral of absolute tracking error by ≥10%** (`100·(J_C1−J_S)/J_C1`, paired 95% excludes zero, no safety regression) under realistic confounds. Known-class abstention = error in headline macro-F1.
- **Failure shapes:** hypothesis failure (C1+temporal adaptation matches S — clean negative) vs **method failure**. **Inconclusive (Slot 13):** diagnostic-only · fault-specific/bounded · confound-fragile · excitation-dependent · **role-coverage-bounded**. **A2 Case C would land on method failure + excitation-bounded.**
- **Pre-specification:** freeze gauge placement, model/hyperparams, thresholds, analysis window, seeds/scenarios before confirmatory generation. Leakage-free splits. ≥5 training seeds. Paired hierarchical bootstrap.

## Carried limitations for the Technical Report / Gate 7

1. **2^(3−1) parity residual:** `I(trajectory ; full cell)` = 1 bit in dev/pilot/val, 0 at test; main effects and two-factor interactions estimable everywhere; cannot favour either suite.
2. **The OOD arm rests on only 2 compound settings per split** (16 val / 32 test runs, 2 fault types) — thin. **A2 adds no severe-band OOD settings; no severe-band OOD claim will be made.**
3. **Test severities sit partly outside the fit hull**; the severity regression head extrapolates at test.
4. **`split_group_id` is unique per reservation**, so `_assert_one_mapping(split_group_id → split)` is vacuous — the real guarantee is trajectory/fault exclusivity, which does hold.
5. **`_assert_fault_independent_context_cells`** uses `expected_cell_count = min(len(table), trajectory_count * repetitions)`, correct only because trajectory blocks are disjoint mod 8 at the actual values. Both pinned; cannot silently drift.
6. **[S33] Finding 1** — structural severity grid below the 2× synchronous margin at every reserved severity. **Quadruply qualified:** S35 Finding A (under-strength probe), S36 Finding D (mis-matched yardstick), S37 Finding F (wrong operation), S38 Finding J (wrong window origin).
7. **[S33] Finding 2 (contact), non-blocking.** 236 runs assigned a contact profile; **11 actually touched** (4.7%) — dev 0/76, pilot 11/76, val 0/84. All 11 are encoder **bias (7) or drift (4)**; 0 dropout/actuator/structure/healthy. Mechanism: bias/drift corrupt measured angle → observed-PD overdrives → tip descends. **Realized contact is an EFFECT OF THE FAULT**, peak 2.6–3.0 N, loudest in the S-exclusive gauge channel — direction **favours S**. `I(fault; assigned contact label)` = 0 exactly; `I(fault; contact actually occurring)` is not. Addressed by A2 pin 4. **Re-confirmed S45 on the replayed dev row: 0 contact steps despite `contact_dev_brief`.**
8. **[S34] The mild-stratum development diagnostic** — at dev EI 0.75/0.50 neither suite separates structure; no gauge column significant; the only consistent structural signature is a C1 IMU channel. **State at that scope only.**
9. **[S35] The excitation discontinuity** — the delivered probe is ~5.8× weaker than the screen that justified its amplitude, because the ramp was never pinned in config.
10. **[S36] The yardstick discontinuity (D)** — a per-gauge five-sigma threshold at W=640 applied to a four-gauge statistic at W=768; error 7.7%, direction lax.
11. **[S36] The run-to-run range statement (E)** — delivered fault−healthy gauge differences fall inside the range spanned by fault-free healthy pairs. **Report as a range statement, never as a test.**
12. **[S36] Margin coverage is trajectory-partial** — the rule certifies only diagnostic-trajectory rows; ordinary-trajectory structural rows stay in the estimand, **not certified by the diagnostic margin**.
13. **[S37] The operation mismatch (F)** — a threshold measured on a single window applied to a difference of two; and **a matched-seed difference admits no sensor-only threshold at all** because CRN cancels the sensor term.
14. **[S37→S38 CORRECTED] Thermal near-invariance (G)** — a *property*, not a defect: `D`'s null is essentially unchanged across 0–3 °C per-window excursion. **NOT exact cancellation** — thermal enters inside the 0.5 µε quantizer.
15. **[S37] The amplitude ceiling (H)** — the probe could not be strengthened past 0.15 N without violating an approved actuator-authority limit.
16. **[S37] Stage-C null dependence** — `Q95_c` comes from 28 pairwise distances generated by only 8 independent runs; a U-statistic. **[S38] Under `method="higher"` it is the 27th of 28 order statistics.**
17. **[S38] The window-origin discontinuity (J)** — the screens place the probe at onset, the generator places it at `onset + start_offset_s`; a window from onset captures 43% of the probe. **Nothing in the codebase fixes the window origin**, so the protocol's pin is effectively the pipeline's pre-registration and Gate 7 must reuse it. **[S40] The measured 2.37–3.64× is the ratio of TOTAL unmatched-row differences between two windows — NOT a fault-effect multiplier.**
18. **[S38] The matched/unmatched asymmetry** — Stage A/B signal is seed-matched (noise cancels), Stage C null is not. Favours S. `TESTABLE` is therefore **necessary, not sufficient**.
19. **[S38] Task motion leaks into the synchronous statistic** — probe-free `t00` healthy `||b||` at 0.8 Hz is 0.48–0.51 µε. The 0.8 Hz coefficient is not probe-specific; matched differencing is what makes it a fault statistic.
20. **[S39] The construction path (K)** — the closed loop is driven by a **C0** session and S gauges are produced **post-hoc** by replaying the privileged record. Both the protocol and the Gate-7 driver must build/read by the verified path. **Positive result, automated and re-verified twice (S45, S46): ONE delivered row reproduces bit-for-bit from committed inputs — put this in the packet at that exact scope, and cite `scripts/protocol_p_replay_gate.py` as the artifact that demonstrates it.**
21. **[S39] The unmatched-identity confound (L)** — delivered fault and healthy rows do not share `(sensor_seed, pair_id)`, so **every** delivered-row magnitude is `||fault + closed-loop divergence||`. Absolute magnitudes do not transfer to the protocol's matched `D`.
22. **[S39] The observed path is nearly free on a matched difference** — 0.937×–1.148× of the privileged result, mean ≈0.996.
23. **[S40] The realized-vs-base identity distinction** — `ScenarioReservation.base_pair_id` is NOT the RNG key; the `_dataset0` suffix makes the identity. Any protocol, audit, join, or leak guard that names "pair_id" must say **which one**.
24. **[S40] The ramp fraction is unreachable through the assignment document** — `duration/2.0` is computed, not read. A code change was always required.
25. **[S40] `Q95_c^gauge` and the S39 gauge-only measurement are conditional healthy-null diagnostics only.** No mechanism attribution for a Case C.
26. **[S41] The Stage-A safety gates are not a construction check.** A gate with a large margin certifies safety, not that the constructed experiment is the specified one. **[S43] Now covered by a permanent automated test rather than by vigilance.**
27. **[S41] A terminal branch that attributes a failure to physics must first exclude the construction.** Now fenced by **I13a AND I13b** as explicit preconditions.
28. **[S41] Raw-byte file pins are cross-platform contracts.** `core.autocrlf=true` here. Once bytes enter a scientific identity, line-ending policy is part of the protocol.
29. **[S42] A byte pin must name its DOMAIN, and a fix generalized past its domain is a new defect.** **Any file whose raw bytes enter an identity must be classified text-or-binary first.** Also: **a `.npz` is a ZIP, so byte-identity of a *regenerated* archive is not a claim to make** — pin the retained input by bytes, guard the reproduction by array equality.
30. **[S42] An undefined or overloaded token in a pre-registration is a scientific defect, not a style problem.**
31. **[S42] A specification can name an invariant its own architecture cannot express.** **Ask of every invariant: is this property reachable from the place I am asserting it?**
32. **[S43] A pre-registration's variable names are part of its executable surface.**
33. **[S44] The seam's own coverage history is part of the packet's honesty record.** The probe-override wire was untested in the first version of the seam's suite, and the gap closed only because the patch was adversarially mutated. **If the Gate-7 driver reuses this seam, it inherits the same wire and needs the same class of test.**
34. **[S44] The two seam files are not byte-pinned, deliberately** — and **[S45] Codex confirmed this is the policy, not an oversight**: Protocol P hashes no source file, so git blob hashes are the EOL-stable identifiers. **[S46] The four new Stage-0 files are in the same state for the same reason.** **Any future claim about these files' bytes must quote the blob hash or say which EOL rendering it means.**
35. **[S45] The one-row replay scope is exact and must be stated as such everywhere.** ONE row, ONE suite, reproduced exactly: 20 privileged fields + 38 observed entries. The 472-reservation / 944-pair dataset was **never regenerated** and no dataset-wide reproduction claim exists. What the row *does* license is stronger than it looks: because the references predate the S44 seam, it also certifies that the seam perturbed nothing on the ordinary path.
36. **[S45] The replay gate is not runnable by an outside reader, and the packet says so.** Packet README Step 23 states the step cannot be run from the distributed packet, that regenerating from Step 2C reproduces the references, and that the gate's comparison layer is covered portably by `tests/test_protocol_p_replay_gate.py`. **`DATA.md` must repeat this at Phase-3 curation.** **[S46] Contrast this with Stage 0, whose Step 24 IS runnable from a clean checkout — the two Protocol-P steps have opposite reader-reproducibility status. [S50 CORRECTION: state that as "no dataset, no MuJoCo *simulation*" — never as "no MuJoCo" or "no physics engine", see limitation 47.]**
37. **[S46] Stage-0's I8 guards the code, not the data, and the write-up must say which.** All three I8 sub-conditions are unreachable from the real construction path. Reported as a code guard with a wire test, not as a runtime data risk.
38. **[S46] The lifted gauge-window helper is a shared dependency of two screens, one of them closed.** `utils/gauge_windows.py` feeds both `analyze_synchronous_detection_floor.py` (closed, published `detect_threshold_microstrain`, still read by `screen_synchronous_safe_probe.py`) and Stage 0. **Any future edit to it must re-verify the floor screen's two published artifacts byte-identical, exactly as S46 did.** Standing obligation.
39. **[S47] BOTH Stage-0 config-binding guards defend CODE, not present-day DATA — and the write-up must say so for each.** The rejected state is unconstructible in this lineage; it becomes constructible only when a new draft config is authored for the pre-confirmatory build. **No Technical Report sentence may claim either guard prevents a falsely bound artifact that is constructible today.** [Codex accepted this in its S47.]
40. **[S47] A brute-force numeric scan of the config for a pinned literal produces numerological hits as well as semantic ones.** **Exactly three of the seven pins are real bindings.** The scan finds candidates, not bindings.
41. **[S48] Stage 0's corroboration is upper-tail and must never be written as agreement.** The Technical Report may say "falls inside the measured real-plant range" — the pre-registered claim — and may **not** say the synthetic null "agrees with" or "matches" the real-plant null.
42. **[S48, SETTLED S49] §8's "roughly 0.39" is an S39-era approximation, not a pinned prediction, and the executed value is 0.400881 (+2.79%).** Quote the artifact, not the protocol. Codex agreed no protocol change is warranted. Closed.
43. **[S49] `stage_0_identity` binds the run's INPUTS and OUTPUT SHAPE, not its measured values — it is provenance, not a tamper seal.** Demonstrated by construction. **No sentence anywhere may say the identity certifies, seals or verifies the numbers.** [Codex accepted this in its S49.]
44. **[S49] `null_distribution.std` is the POPULATION standard deviation and the artifact does not disclose which it is.** Any quotation of the spread must say population; any future results artifact of ours should name the convention in the file.
45. **[S49] The Stage-0 first-run elapsed time was never captured and cannot be honestly reconstructed.** Packet Step 24 records `first-run elapsed time: not captured`; any later timing must be labelled a separately authorized reproduction, and Stage 0 must not be re-run to manufacture one. **My summary's old informal `≈7 s` is NOT a measurement and has been removed from the timings list below.**
46. **[S49] Cross-platform bit-identity of the Stage-0 output has NOT been measured.** Determinism given the pinned seeds and pinned dependency versions is claimed; byte-identical output on another machine is not.

47. **[S50, RESOLVED S51] Stage 0 performed no MuJoCo simulation but its script DID import the `mujoco` package transitively. THE EXTRACTION REMOVED IT — measured zero after, pinned by a test. The historical statement below is kept because two published documents carried the withdrawn claim and the record of why must survive.** `analyze_synchronous_difference_null.py:96 -> protocol_p_replay_gate.py:99 -> assignment_generator.py:24 -> cable_plant.py:15 import mujoco`. **Never write "Stage 0 needs no MuJoCo" or "needs no physics engine"** — write "no dataset, no MuJoCo *simulation*, no plant rollout". Measured scope: **one of the script's eight project imports**, across a surface of four constants, one exception class and one text-hashing helper — so the dependency is **incidental, not intrinsic**, and should disappear at the `utils/protocol_p.py` extraction. `mujoco==3.10.0` is pinned in the packet `requirements.txt` and installed by Step 1, so clean-checkout runnability is unaffected. **The claim was published twice in the public log before being withdrawn; both instances are now covered by the corrected entry.**

48. **[NEW S51] `utils/__init__.py` re-exports `SCHEMA_VERSION` from `utils.schema_types`, so ANY `from utils import X` imports NumPy.** `utils/protocol_p.py` itself imports only the standard library — measured by loading it *by path*, outside the package. Two different claims; both pinned by their own tests so they cannot be conflated. Non-blocking, Codex's file, no change requested.
49. **[NEW S51] `require_screen_reservation`'s `sensor_seed` check is unreachable while its exact-set comparison stands, and I8's base-distinctness check is unreachable from `rollout_provenance`** (the base hash is inside the hashed payload). Both are CODE guards, both say so in their docstrings, and the second is factored into `require_base_distinct_provenance` so the rejected state can be fed to it and the call site wire-tested. **Fourth entry in the class** (I8-guards-code 37; both config-binding guards 39; identity-certifies-inputs 43).
50. **[NEW S51] The torque gate's inclusive boundary is EXACT in IEEE double at both association orders** — `0.15*2*0.40 == 0.60*0.20 == 0.12` exactly. Measured, and pinned by a test that asserts the equality itself. **Any refactor of that arithmetic must re-measure it; a `<` there silently drops the strongest admissible candidate.**
51. **[NEW S52] The construction layer's cell binding is over THREE IDENTIFIER STRINGS, not over the body.** `require_screen_source(..., cell=)` checks `scenario_spec_id`, `base_pair_id`, `split_group_id`; what physically makes a cell is the `(payload_id, env_profile_id, contact_profile_id)` triple. A source with cell-4 names and cell-5 profiles would pass. **NOT a defect and I did not request a guard:** the driver selects its source from the assignment document, whose bytes are pinned by I1 and whose rotation `_context_cell_table` validates, so the triple is bound transitively. **FIFTH member of the class** (I8-guards-code 37; both config-binding guards 39; identity-certifies-inputs 43; two unreachable construction guards 49). **The Technical Report may not say this module verifies the body.**

52. **[NEW S52] `build_overrides`'s `require_constructed_condition` call is tautological and no test can make it red.** It compares `requested_fault_specs(...)` against a fresh identical call. The real check is the one in `rollout_provenance`, over the tuple that is actually stamped. Line kept deliberately; **never describe it as a live guard.**


## Coherence / honesty bounds (keep loud)

- **Sensor RNG keyed on `(sensor_seed, pair_id, channel, stream)` jointly** (`utils/rng.py:76-78`) — changing either field changes the stream. **Measured S39: a `pair_id` change alone moves `gauge_obs` by up to 6.50 µε**, against `D` values of order 0.1–0.5. **S45: nothing else is in the key — suite call order does not enter it. S46: re-confirmed independently at the helper level.**
- Deployable floors are *detection*, not learned attribution; all S19 rates from ONE fixed fault setting per class; abstention untestable on this fault library; one-hot prototype probabilities NOT calibrated; **every joint-space control number comes from a condition where the structural fault causes no measurable JOINT deficit.**
- **A noise threshold is a property of the SENSOR MODEL, the window LENGTH, the window ORIGIN, the aggregation, the path (privileged vs observed), the operation (single vs difference, matched vs unmatched), the construction (which session drives the loop, which produces the channel), the identity (base vs realized), and the fault's activation step. The SIGNAL it is compared against depends on excitation, task and plant.** Never quote a µε number without naming all of these.

## Constraints / environment / ops (load-bearing)

- **Simulation-only, one desktop:** Windows 11, Ryzen 7 8700F (8C/16T), RTX 5060 Ti **16 GB VRAM** (sm_120), 32 GB RAM, Python **3.12.10** in `./venv`. Free/OSS, commercial-use-friendly only.
- **venv has:** numpy 2.5.1, scipy 1.18.0, scikit-learn 1.9.0, matplotlib 3.11.0, mujoco 3.10.0, pandas 3.0.3, control 0.10.2, gymnasium 1.3.0, pytest 9.1.1, **torch 2.11.0+cu128**. **No new dependency was added in S46-S52.**
- **Running packet tests:** from the REPO ROOT, `./venv/Scripts/python.exe -m pytest -q "Reproducibility Packet/tests"`. **Scope pytest to that path** — a root-wide invocation collides on duplicate test module names in the ignored `tmp/session6_packet_copy/`. Full suite **750 tests green** (S52, 13.60 s; `test_protocol_p_conditions.py` collects 135 and `test_protocol_p_shared.py` collects 20, so 155 is the two-file focused total). Prior: 736 (Codex S51), 725 (my S51). **Set `PYTHONIOENCODING=utf-8` for anything that prints non-ASCII** — the console is cp1252 and a bare `print` of `µ`/`ε`/`→` raises `UnicodeEncodeError` *after* useful output. **Use ASCII in probe scripts and in anything a gate prints.**
- **Packet scripts are invoked FROM the packet directory** (`scripts\<name>.py`, `--output-dir results\<name>`), per its README. From the packet dir the project venv is `..\venv\Scripts\python.exe`. **In my PowerShell tool the working directory is not the repo root — use `Set-Location` or absolute paths. My Bash tool's cwd PERSISTS between calls — prefer absolute paths or re-`cd` every time.**
- **Timings (measured S35–S50):** full packet suite ~12–13 s; one MuJoCo rollout (3000 steps) **25.6–27.5 s**; **a PARTIAL rollout is proportionally cheap — 480 steps ≈ 3.0 s**; **at reduced fidelity (`point_count=9`, `simulation_timestep_s=2e-4`) 501 control steps ≈ 0.37 s — roughly 8× cheaper, legitimate whenever the property under test is not fidelity-dependent (S43)**; a 200-realization sensor-only null at W=768 across 4 gauges ~40 s (no simulation); an offline re-observation of one delivered plant trace ≈ instantaneous; hashing both replay references ≈ instantaneous; a 3,124-file inventory ≈ instantaneous; the Stage-0 module import 0.21 s; a 26-case mutation sweep over two files ≈ 100 s; a 12-case sweep ≈ 40 s; a 5-case sweep ≈ 25 s; the detection-floor screen re-run ≈ 40 s; the Stage-0 measurement path at `pairs=2` ≈ 3 s; **[S50] an eight-import subprocess dependency sweep ≈ 10 s.** **NO figure exists for the pinned `pairs=100` Stage-0 run — see limitation 45; do not invent one.**
- **Background jobs:** `run_in_background: true` and wait for the notification. **Python buffers stdout when redirected — poll the results JSON, not the log.**
- **PowerShell 5.1** primary (no ternary/`??`; **`^` is not a continuation — use a backtick or a single line**); Bash tool also available. Use `git diff --numstat` to confirm `+N/−0` after every chat turn.
- **Root `.gitignore`** covers `venv/`, `/data/` (line 19), `tmp/`, `MUJOCO_LOG.TXT`, caches, model files, LaTeX aux, OS/IDE noise, and the three session locks (`.claude-session.lock`, `.codex-session.lock`, **`.agent-session.lock`** — the scheduled-task runner creates the last one at the repo root). **Root `.gitattributes`** pins `schema.json`, the assignment JSON, and **`Reproducibility?Packet/protocol/*.md`** to LF (the `?` wildcard matches the space in the folder name; **the wildcard covers each renamed protocol file — verified S42/S43 via `git check-attr`, no edit needed on a version bump**). **Packet `.gitignore`** ignores `*.npz` + caches/logs (so `results/*.json` and `*.md` ARE tracked). **Verified again S50; no change needed, and per Codex's S44 answer no source file should be added.**

## STANDING LESSONS

1. **Dry-run the analysis path before spending a rollout budget.** *(S39–S50 were all essentially this; the one authorized rollout is still the only one spent.)*
2. **Self-audit from row artifacts / raw bytes, not the summary.**
3. **Restate a proxy in the contract's units before comparing to the bar.**
4. **For a MuJoCo screen, re-run to scratch + diff against committed.** *(S46 extended this to a non-MuJoCo screen: any refactor touching a closed screen owes a byte-identical re-run of its published artifacts.)*
5. **Verify the live git state before trusting continuity.**
6. **Review a design by simulating its consequences, not by verifying its internal consistency.** Corollaries: dead arithmetic hides in small catalogs; **the dangerous confound is the one that favours you**.
7. **For any pre-registration, check that the pre-registered TEXT generates the pre-registered DATA.**
8. **Test a guard by feeding it the exact state it was written to catch.** Corollaries: check a flaw is REAL before reporting it; **and check a REPORTED flaw is real before fixing it**; report the scope you actually achieved.
9. **A design review that reads the design cannot find what the design does.** Corollaries: **audit the yardstick before the artifact**; **before calling a settled parameter a defect, search the history for why it was chosen.**
10. **A negative result is only readable if the same instrument produced a positive one.**
11. **(S35) A threshold and the signal it judges must be measured in the SAME configuration.**
12. **(S36) When you import a number, import its definition, not its name.** Corollary: **two configuration errors can cancel, and that is dangerous rather than lucky.**
13. **(S36) When a choice you must make favours you, measure how much, say so, and hand the decision to the reviewer.** *(Applied ten times now.)*
14. **(S36) A pre-registered protocol must be executable by someone who did not write it.** **Corollary (S37, reconfirmed S38–S50): the act of making it executable is itself the defect-finding technique.**
15. **(S36) The cleanest statement of a negative is often a comparison you have not made yet.**
16. **(S37) Match the null to the OPERATION, not just to the configuration.** And: common random numbers can void an entire class of threshold.
17. **(S37) Compute the closed-form consequences of every gate you approve, before it costs anything.** Corollary: **check boundary cases for `<` vs `<=`.**
18. **(S37) When the most likely branch creates a design problem, force the decision BEFORE the measurement that would make any fix look chosen.**
19. **(S38) When you import a convention, import the CONFIGURATION THAT MAKES IT TRUE.** Lessons 11/12 at increasing depth: window length → aggregation → operation → time origin → construction path → realized identity (S40) → fault activation step (S41) → file byte-domain (S42) → the name an expression actually binds (S43) → the denominator a clean report is computed over (S45) → the size of the example a test reasons over (S46) → **the scope a correction claims to cover (S50)**.
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
32. **(S43) A generic name in an operative expression is an open invitation, and something eventually accepts it.**
33. **(S43) A constant that looks authoritative and drives nothing is the same trap pointed the other way.**
34. **(S43) When you deviate from a collaborator's stated sequencing, say so at the top, give the reasoning, and hand them the decision.**
35. **(S44) Unit-testing both ends of a wire does not test the wire.** Sub-forms: (a) deleting a call site is invisible whenever the guard's rejected state is not producible — wire-test it by monkeypatching the guard to always raise; (b) a test helper that reimplements production arithmetic is a second copy that agrees with itself.
36. **(S44) Injecting defects into your own finished patch is cheap and it is not optional.**
37. **(S44) Deleting a vacuously-passing test is a contribution, not a gap.** **Ask of every new green test: what exact state would make this red?**
38. **(S44) Extending a stated principle to an unenumerated case is still a deviation — lead with it.**
39. **(S45) A clean report must disclose its denominator.** Three parts, all required: print the count examined, refuse the claim when it is too small, and encode the violation in the exit status.
40. **(S45) Ask what else a reproduction check happens to hold fixed.** **A comparison against an artifact from time T certifies everything that changed between T and now.**
41. **(S45) NaN tolerance and NaN blindness are one line apart.**
42. **(S46) A test fixture can be too small for the defect it is meant to expose.** **Ask of every fixture: is it big enough to distinguish the thing I am claiming to check?**
43. **(S46) Re-review the fix to your own defect as work, not as a verdict.** **An owner re-review that only confirms the reviewer's claims is not the review the cycle is asking for.**
44. **(S46) Promoting a diagnostic to a hard gate needs its own false-positive measurement.**
45. **(S47) A DIRTY report needs verifying as much as a clean one.** **A comparison must distinguish "these differ" from "I could not compare them"** — folding a missing file into "differs" fails in the *alarming* direction, which looks like diligence and passes unchallenged.
46. **(S47) When a pinned value also exists in a bound document, the fix is EQUALITY, never ADOPTION.** **Corollary: a guard that refuses is composable with a guard that pins; a guard that reads is not.**
47. **(S47) Establish reachability by construction, and do not conclude "unreachable" from failed attempts.**
48. **(S47) Asking "what exact state would make this red?" is a per-test question, not a per-file one.** **Assert the REASON for a refusal, not merely that one occurred.**
49. **(S48) A reviewer's correct fix and a reviewer's correct reasoning are separable, and the owner re-review owes both.** **Ask of every reviewer edit: is it correct, AND is the reason given for it correct?** *(S50 asked it three times and got three clean answers — the value is that the record then holds reasons that were checked rather than reasons that were plausible.)*
50. **(S48) Verify a correction the same way you would verify an accusation — by construction.** *(S50: I did not accept `mujoco_imported=True` on report; I imported the module and read `sys.modules`, then read the four import statements out of the files. Cost about two minutes.)*
51. **(S48) Extract the prior state from git rather than reconstructing it.** Any "was the old version really defective?" question is answerable with `git show <commit>:<path>` and should never be answered from memory.
52. **(S48) When a finding changes no shipped behaviour and the reviewer has asked for an unambiguous approval, record it and approve.** **The escalation trigger has a second edge: knowing when a real finding is not worth a round.**
53. **(S49) When you re-verify someone else's verification, CHANGE THE INSTRUMENT.** **An independent check that shares machinery with the thing it checks is only partly independent.** *(S50 applied it a third time — `math.ulp` plus a naive left-to-right sum — and that third instrument corrected my own S49 phrasing: two non-NumPy summation orders agree with each other, so NumPy's pairwise sum is the outlier, not `fmean`.)*
54. **(S49) After a reviewer corrects a claim, search the artifact for that claim's other instances.** **A `grep` takes seconds and a half-corrected director-facing artifact reads as corrected.**
55. **(S49) A name travels into the write-up faster than its mechanism does.** **For every verification object, write down what it does NOT cover, in the artifact, before someone quotes it.**
56. **(S49) Approval is an ACT, not a state you drift into.** Post the explicit approval as its own turn, naming the exact blob.

57. **(NEW S50) A correction is an artifact and inherits every failure mode an artifact has — including the one it was written to fix.** Codex's public-log correction was accurate and its scope was one entry short of where the withdrawn claim had actually been published, so a reader stopping earlier would carry a claim the project had withdrawn. **Check a withdrawal against the full publication history of the thing it withdraws, not against the entry that prompted it.** This is Lesson 54 one level up, and it recurred one session after Lesson 54 was written — which is itself the evidence that the generalization was needed. **Corollary on repair: for an append-only log, edit the correction if it is still under review, never a settled dated entry, and never append a correction-to-a-correction — a stranger reads one correctly scoped notice better than two nested ones.**

58. **(NEW S50) A documentation claim about a dependency is a measurable claim, and an import-only load settles it in seconds.** "Needs no MuJoCo" was false in the packet runbook and the public log for two entries, and nothing about reading the script would have revealed it — the dependency arrives four modules away through an import of constants. **Any runbook sentence of the form "this needs / does not need X" should be produced by running the thing and looking, not by reasoning about what it does.** And when the answer is yes-but-shallow, **measure the depth too**: "imports MuJoCo" and "imports MuJoCo through one of eight imports, across a constants-only surface, as a consequence of a scheduled refactor" leave a reader with very different impressions of how self-contained the work is.

59. **(NEW S51) A test that matches on a LABEL certifies a guard it may no longer exercise.** Three of my I3 tests matched `"I3"`, a string at both of the function's raise sites, so weakening the guard left them green while opening a real leak. **Match a phrase unique to ONE raise site — and when a function has two raises for one invariant, that is exactly when a label match stops being a reason match.** This is Lesson 48 (assert the reason) with the failure mode made concrete: the reason must also be *distinguishing*.
60. **(NEW S51) A mutation that survives a focused sweep is not yet a gap — re-run it against the full suite before calling it one.** Of my two survivors, one was a genuine hole in my tests and one was already covered by a test file the focused sweep did not run. Reporting both the same way would have been wrong in both directions: a fabricated gap, and an unearned claim of thoroughness. *(S52 applied it again and it fired again: of seven focused-sweep survivors, five were real and two were not — one a scope artifact, one a malformed mutation of my own.)*

61. **(NEW S52) Test per BRANCH, not per guard.** Codex's `require_stage_identity` refuses on three distinct paths; it wrote a test for one, and the other two survived the whole 736-test suite when weakened. The count of tests rose, the coverage of the relation did not. This is Lesson 59 one level up: there the two raise sites shared a *phrase*; here they are genuinely different checks, and testing the first made the second *look* covered. **Ask of every guard: how many ways can this be wrong, and is there a case for each?**

62. **(NEW S52) A guard that refuses everything is not a guard — test the ACCEPT side against the real inputs.** Every other test in the construction file feeds a hand-built fixture and can only show that a wrong state is refused. The complementary risk is a guard so strict it refuses the construction that will actually run, and only the real assignment document settles it. That test also pins the mapping the guard's literals depend on, so a change to the document goes red instead of silently rebinding the screen to another body. *(Lesson 25/47, turned into a permanent test rather than a session-time probe.)*

63. **(NEW S52) Two mutually redundant call sites of one guard are individually untestable.** Removing either leaves the other standing, so a single-mutation sweep reports both as covered. **Sweep the DOUBLE removal whenever one check appears at two call sites** — and when one of the two is tautological by construction, say so rather than counting it as depth.

64. **(NEW S52) When the reviewer's repair is itself an artifact, sweep it the way you sweep your own.** Two consecutive rounds now have found a real defect in the reviewer's repair (S48's evidence defects in my tests, S52's five unexercised guards in Codex's). **The round is not over when the reviewer is right; it is over when both passes have been attacked.**

## Pointers

- **Protocol P (in force, JOINTLY APPROVED): `Reproducibility Packet/protocol/protocol-p-v2.3.3.md`, canonical sha256 `5689dad7…8bdf421f`. READ THE FILE.** Superseded: v2.3.2 `9d257017…738ba6e5` and v2.3.1 `8c268f8f…401d76` (both blocked, never executed, recoverable from the `Claude Session 42` / `Claude Session 41` commits).
- **The replay gate (JOINTLY APPROVED at `7d3309b7…` in my S46; EDITED IN S51 to import the shared module, new blob `c6b16749…`, back under review): `Reproducibility Packet/scripts/protocol_p_replay_gate.py` + `tests/test_protocol_p_replay_gate.py` (36 tests, blob `6a7e7774…`, unchanged).** Run from the packet dir: `..\venv\Scripts\python.exe scripts\protocol_p_replay_gate.py --data-root ..\data\gate3-base-dev-pilot-val-c1-s`. **PASSED in S45 and again twice in S46.**
- **Stage 0 (JOINTLY APPROVED my S48; RUN ONCE S48): `Reproducibility Packet/scripts/analyze_synchronous_difference_null.py` (blob `8435c764…`) + `tests/test_synchronous_difference_null.py` (blob `9591c91b…`, 99 tests) — plus three files approved at Codex's blobs in my S47: `scripts/utils/gauge_windows.py` (`7f7c09da…`), `scripts/analyze_synchronous_detection_floor.py` (`b99fe333…`), `tests/test_gauge_windows.py` (`925b0bd8…`, 18 tests).** Pre-registered invocation, single line, run from the packet dir: `..\venv\Scripts\python.exe scripts\analyze_synchronous_difference_null.py --window 768 --f-ctrl-hz 500.0 --diagnostic-hz 0.8 --thermal-ramp-c 3.0 --pairs 100 --seed 0 --pair-id 1` — all seven are also the defaults. **It has been spent; re-running it is NOT authorized without a new decision.** No dataset, no MuJoCo *simulation* — and **as of S51 the script imports no `mujoco` package either** (limitation 47, resolved; the Stage-0 script blob is now `f104971d…` and is back under review).
- **The Stage-0 artifact — JOINTLY APPROVED (Codex S48 reviewer, me S49 owner). Tracked. DO NOT EDIT, DO NOT RE-EXECUTE.** `Reproducibility Packet/results/protocol_p/sensor_only_difference_null.json`, **git blob `31c1e6d1824c10bd5978d12c377f76cf556af03f`**, 6,765 bytes in checkout (177 CRLF), raw sha256 `4101c0b8dcc1c3ee01b37433ccb3563d4c1e15e5e22cd8094979645d36a40cae` (**disclosed, not a pin**). Top keys `purpose, protocol, stage_0_identity, stage_0_canonical, inputs, statistic, corroboration, boundaries, samples, null_distribution`. **`samples` is a 6-key metadata dict; the 100 values are `samples["distances"]`. There is no top-level `authority` — the path is `corroboration.authority`.** Q95 `0.400881`, identity `dev-71b33289…`, `std` is the **population** one.
- **Packet README Step 24 — reached joint approval at `9363e144…` (Codex S49 / me S50) and I REOPENED it in S51.** Its dependency sentence became false at the extraction; the new state is blob **`ba9c067a4d7ccce4b6c29edcf588b7eeb0e8150e`** (`+1/−1`) and says the stage's script imports no MuJoCo at all, naming `tests/test_protocol_p_shared.py` as the thing that pins it. **Codex reviews. Steps 22, 23 and 24 are mine to maintain.**
- **Root `README.md` (the public Live-Run log) — LOOP CLOSED at `73b124fd5e85c4cd0ebef8cce9a16c37c8e465e5`** (Codex S50 reviewer, me S51 owner). Then **my S51 appended ONE new entry** (`+2/−0`, current blob `ca1cdf0a5859098e002adb7c79a307231cdc2e3f`): the extraction removed the MuJoCo import the previous entry described as current, and leaving the log contradicting the rewritten packet runbook would ship two outward-facing documents disagreeing about one fact. **The entry states the code is under Codex's review and not approved.** No dated entry was edited.
- **THE S51/S52 ROUND — six of eight states JOINTLY APPROVED, one returned.** Approved: `scripts/utils/protocol_p.py` (`8d900525…`), `scripts/protocol_p_replay_gate.py` (`c6b16749…`), `scripts/analyze_synchronous_difference_null.py` (`f104971d…`), packet `README.md` Step 24 (`ba9c067a…`) — all four Codex approved UNCHANGED in its S51; plus `scripts/utils/protocol_p_conditions.py` (`7fdddf0e…`) and `tests/test_protocol_p_shared.py` (`f505877f…`, 20 tests) — both reviewer-edited by Codex in S51 and approved UNCHANGED by me in S52. **OPEN and Codex's turn:** `tests/test_protocol_p_conditions.py` (`1874773e…`, 135 collected, `+135/−1`) and the public log's newest-entry count (`78b4a734…`, `+1/−1`). **Codex's S51 answers to my three S51 questions, all settled:** the construction layer IS the third consumer (architectural, not a filename test); the binary *rule* belongs in the shared module while the four `.npz` *pins* stay with the gate that reads them; and a separate results module is acceptable **but the driver still owns the integration proof** — the boundary test must invoke the real driver against a real temporary results root and show an injected dataset/manifest/role-index/label write making it fail. A green module test beside an unwired driver repeats the D5 failure.
- **`agents/Claude/Progress Reports/Progress Report Session 48.md` — JOINTLY APPROVED, loop CLOSED** at blob `f01aa7d7b56b9b30e8279bc221a5f0e60613ab3f` (me S49 owner, Codex S49 reviewer).
- **The seam (APPROVED, Codex S44): `ScreenOverrides` in `Reproducibility Packet/scripts/utils/assignment_generator.py`, git blob `1c565888…`, and its tests, git blob `2ec96c9f…`.** Read spec §3 beside them.
- **The I13b guard: `Reproducibility Packet/tests/test_cable_plant_softening_boundary.py`** — 6 tests, co-owned, **approved in place by Codex (S43)**.
- Claim Sheet (in-force contract): `Claim Sheet.md` · plain-language: `Accessible Claim Sheet.md` · Study Guide Pass 1: `Study Guide/Pass 1 - Conceptual Foundation.tex`
- **Shared schema (in force, +A1):** prose `Reproducibility Packet/schema/schema-v1.0.md`; machine `schema.json`.
- **The freeze plan:** `agents/Codex/Config Freeze Readiness Review.md`.
- **The probe-amplitude record:** `Reproducibility Packet/results/synchronous_safe_probe/synchronous_safe_probe_report.md` — **read S35 Findings A–C, S36 D, S37 F, S38 J, S39 K/L, and S40/S41's narrowings beside it.**
- **The detection-floor record:** `Reproducibility Packet/results/synchronous_detection_floor/summary.json` — **`detect_threshold_microstrain` is a 5σ threshold, per gauge, at W=640, of a SINGLE window.** sha256 `4937e885…c2c67` as of S46; **re-verify this after any edit to `utils/gauge_windows.py`.**
- **My S34 screen:** `Reproducibility Packet/scripts/screen_structural_separability.py` + `results/structural_separability/` (packet README Step 22).
- **CONCLUDED director chat:** `chats/Claude-Codex-Human/Better Suited Task/…- Concluded.md` + `Summary.md` — the withdrawn task-redesign directive. **A2 must stay clear of it** (task, score and controller untouched).
- Director requests: `director_requests.md` (root) — entry 1 (Claim Sheet review) non-blocking, awaiting director reply. **Nothing else is blocked on the director.**
- My foundation `agents/Claude/Literature Foundation.md` · ledger `agents/Claude/references.md` (**no S20–S50 entries — reproduction/construction/measurement/review sessions, no external sources read**) · progress reports `agents/Claude/Progress Reports/` (Phase 0/1 Close, S8, S16, S24, S32, S40, **S48 — jointly approved, loop closed**). **NEXT DUE: my Session 56**, unless a phase transition or an approved written Claim-Sheet amendment fires sooner.
- **Live-Run README (co-maintained): root `README.md` — Phase 2 / In Progress, banner 2026-07-31.** **My S52 ran the heartbeat and added NO new entry, but DID edit the newest one** — its `141 new automated checks (suite total 736)` became stale at my additions, and Codex had corrected that same number one round earlier for the same reason, so the precedent that the newest entry is the state under review rather than settled record is established. Now `155 / 750` plus one sentence recording the two-way review. **Flagged to Codex: if it prefers the count frozen at its reviewed state, I revert.** **My S51 added ONE entry** (the extraction; states it is unreviewed) — the deciding question was consistency between two outward-facing documents, not milestone-worthiness. **My S50 ran the heartbeat and added NO new entry** (a documentation loop closing is not a milestone, and Codex explicitly noted a routine approval need not create one) **but did edit the newest entry** — see the open loop above. **My S49 added one entry** (joint approval of the result; the identity is provenance over inputs, not a seal on the numbers). **Codex's S49 appended a forward correction** withdrawing "needs no physics engine" and "every summary figure reproduced exactly"; **both withdrawals are correct and I verified both — do not reinstate either phrase.** **Standing decision, recorded so it is not re-litigated: dated entries are never edited; corrections propagate forward.**
- **Phase-2 chat:** `chats/Claude-Codex/Phase 2 Integration and Config Freeze/…- Active.md` (**12,409 lines**; Codex's S51 turns at 11,942 and 12,143 `+233/−0`, my S52 turn at 12,172 `+238/−0`; **Codex owns the next turn — exact-state review of the returned `tests/test_protocol_p_conditions.py` at `1874773e…` and the one-line public-log count change**).
- **Monitoring chat:** `chats/Claude-Codex-Human/Transcript Order Monitoring/…- Active.md` (88 lines; unchanged in S43-S52 — no recurrence; **streak eighteen**: Codex's S51 commit was `+233/−0`, its two headers once each at 11,942 and 12,143, both after my 11,938 boundary, Codex last). The duty is to flag recurrences, so a clean session adds no note; verify at the git level regardless.
