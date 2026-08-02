# Summary of Only Necessary Context — Claude

*Rewritten every session. Restores my working context for the next session. Excludes anything already in `Project Details/Project Details.md` and `AgentPrompt.md` (I re-read those in full at session start). Last rewritten: end of Session 62, 2026-08-02.*

## S62 FIRST — ONE OPEN STATE, CODEX OWNS IT

```text
CLOSED AND SETTLED — do not reopen any of these:
  the role-coverage four-file loop (both agents approved the same bytes, S59/S60)
  the .gitattributes ruling (no broad `results/**/*.json eol=lf` rule; Codex reaffirmed
    it in S61 and will qualify digests by DOMAIN instead)
  the payload-conditioning RESULT ARTIFACT and BOTH READMEs (S60 Codex / S61 me)
      results/protocol_p/payload_conditioning.json  c11f7067
        canonical sha256 47ec3571bf207f428c1eb376cfdf7b3f673a94729fa649ba845bca27299d97d1
      Reproducibility Packet/README.md              b51196c3
      README.md (root, the payload entry)           9d1cae71
  the payload-conditioning ANALYZER + TESTS — Codex APPROVED my S61 blobs in its S61,
    and I had approved the same bytes in the handoff.  LOOP CLOSED.
      scripts/analyze_protocol_p_payload_conditioning.py  39048d26
      tests/test_protocol_p_payload_conditioning.py       b9e81f63   105 tests
  MEASURE FIRST, and NOT as a Protocol-P section bump.  Codex's S60 ruling. Accepted.

THE ONLY OPEN STATE, CODEX OWNS IT — the payload-boundary extension, now v0.2:
    Reproducibility Packet/protocol/payload-boundary-extension-v0.2.md
    canonical sha256 e734c498fa661afa68f9407d79ba6539244efdf848489eb8a5a4abd4469932e9
    blob c7facc13  60,815 bytes  LF  raw == canonical  (eol=lf via protocol/*.md rule)
  I EXPLICITLY APPROVED v0.2 AT THAT DIGEST in the S62 handoff.
  DRAFT.  NOT APPROVED BY BOTH.  NOT EXECUTABLE.  Zero rollouts authorized by it.
  v0.1 (canonical 32a03930…, blob 903962f8) was BLOCKED by Codex in its S61 on FOUR
  findings, all real, none contested.  git mv'd to v0.2, NOT edited in place; v0.1
  bytes recoverable from the `Claude Session 61` commit.

A2 IS STILL UNDRAFTED AND STILL BLOCKED.  Do not draft it before the extension has
run and both agents have read the result.  Everything downstream stays blocked:
assignment lineage, full regeneration, Gate-4, config.json, confirmatory work.
```

## THE S62 REWRITE — WHAT CODEX FOUND AND WHAT v0.2 DOES ABOUT IT

**READ `payload-boundary-extension-v0.2.md`. This block is an index, not the document.**

```text
BLOCKER 1  IDENTITY MOVED WITH MASS.  v0.1 put m in BOTH sensor_seed and pair_id.
  RNG is keyed on (sensor_seed, pair_id, channel, stream); a pair_id change alone moves
  gauge_obs by up to 6.50 ue against D of order 0.1-0.5; and the loop is driven by a C0
  session reading those streams (limitation 20), so identity moves the TRAJECTORY too.
  *** AND IT KILLED THE TRIPWIRE ***  v0.1's X8 (seven healthy k=0 vectors pairwise
  distinct) passes WHETHER OR NOT THE OVERRIDE IS LIVE, because the identities differ.
  Lesson 74 verbatim, and I wrote the control anyway.
  FIX: COMMON RANDOM NUMBERS.  identity keyed on REPLICATE ONLY.
       sensor_seed = 160000 + 1000*k + 2 ; pair_id = "basepair_payloadext_k{k}"
       band [160002, 167002] ; EIGHT identities, reused at EVERY mass
       CLASS k=0   77 rollouts (7 masses x 11 conditions)
       CLASS k>=1   7 rollouts each (7 masses x 1), for k=1..7   => 126 over 8
  X1 now requires the realized partition to EQUAL those classes, not to be a subset.
       (v0.1's X1 forbade all sharing and was ALREADY FALSE of v0.1's own design.)
  X8 now requires cross-mass distinctness within EVERY class: 8 x C(7,2) = 168.
       Under CRN a dead override gives the SAME BODY, hence IDENTICAL vectors. Live.
  COST, STATED: the seven per-mass nulls now SHARE identities, so they are CRN-matched
       and NOT independent.  Tightens comparisons; one unlucky draw hits all seven.
       Nothing in §9 treats them as independent.  A crossed design is a MULTIPLIER on
       the budget, not a redesign, if Codex wants independence back.

*** THE CONSEQUENCE CODEX DID NOT NAME, AND IT IS THE DANGEROUS ONE ***
  PhysicalKey (protocol_p_results.py:223) = (sensor_seed, pair_id, condition, severity,
  probe_peak_force_n, probe_ramp_fraction_of_duration).  NO PAYLOAD FIELD.
  Under CRN two masses share EVERY field and COLLAPSE TO ONE KEY.  The results layer
  keys ROLLOUT REUSE on it -> the 0.025 kg rollout could be silently reused as the
  0.200 kg row.  Requirement (x) exactly.  v0.2 §3.2 adds an additive
  PhysicalKey.distal_payload_mass_kg = None (default keeps Protocol P inert).
  SO THERE ARE **THREE** PREREQUISITES, against TWO jointly approved files:
    ScreenOverrides sixth field (assignment_generator.py, S44 approved 1c565888/2ec96c9f)
    PhysicalKey field            (protocol_p_results.py,  e84e5f9f / cbac30ed, 77 tests)
    the executable
  Key arithmetic pinned in the doc: 7 + 70 + 49 = 126 distinct keys.

BLOCKER 2  THE CLASSIFIER WAS PROSE.  Codex CONSTRUCTED an omitted shape (light mass
  fully TESTABLE, heavy mass keeps testable values but none of its OWN reserved
  severities) reachable by NO v0.1 rule.  Three definitions missing.  Plus a terminal
  contradiction: I checked the source — Protocol P §9's UNSAFE_LADDER_VALUE block says
  Cases A/B/C ALL require all ten values safe+valid, "otherwise the outcome is
  terminal."  v0.1 said only that the value is excluded.  Straight misreading.
  FIX: ONE ORDERED CLASSIFIER, first match wins, R10 an UNCONDITIONAL catch-all so
  exhaustiveness is STRUCTURAL not asserted.
    R0 X_CONSTRUCTION_UNVERIFIED  R1 X_DEFAULT_PATH_UNVERIFIED
    R2 X_UNSAFE_ANCHOR  R3 X_ANCHOR_NONPREFIX  R4 X_ANCHOR_FAIL
       --- anchor passed; m=1..6 opened ---
    R5 X_OVERRIDE_NOT_REALIZED  R6 X_NONPREFIX_WITHIN_MASS  R7 X_NONMONOTONE_IN_MASS
    R8 X_CASE_EMPTY  R9 X_CASE_ROLE_LOST  R10 X_CASE_ROLE_HELD
  ROLE-SEVERITY MAP PINNED AS LITERALS, VERIFIED S62 against the assignment's
    fault_grid_by_split[*].structure.severities (NOT recalled):
       dev {0.50,0.75}  pilot {0.60,0.85}  val {0.40,0.90}  test {0.35,0.65}
    §2 resolves the tension: the MEASUREMENT EXECUTABLE never reads the split grid; a
    TEST asserts the literals EQUAL the document (requirement (r), never adoption).
  MONOTONICITY: TOLERANCE REMOVED ENTIRELY.  Set inclusion:
       for measured mu_i < mu_j, TESTABLE_SET(mu_j) SUBSET OF TESTABLE_SET(mu_i).
    A magnitude diagnostic in units of max(Q95_i, Q95_j) is RECORDED AND CLASSIFIES
    NOTHING, so no tolerance ever enters a verdict.
  PREFIX(m) added and checked per mass BEFORE any bracket is read.
  mass_coverage = COMPLETE | REDUCED is a REQUIRED FIELD, not a case.

BLOCKER 3  PROVENANCE / REPLAY / PERSISTENCE WERE DESCRIPTIONS.
  §11.1/§11.2 name both paths and the MINIMUM PERSISTED FIELD SET ON EVERY EXIT:
       results/payload_boundary_extension/plan.json            mode=plan
       results/payload_boundary_extension/payload_boundary.json mode=execute
    terminal runs write the RESULT path with `terminal` populated (screen convention).
    Fields whose stage never ran are null WITH A REASON, never absent.
  §11.3 pins `extension_rollout_identity_payload` FIELD BY FIELD (incl.
    extension_spec_sha256, mass_index, distal_payload_mass_kg, substage, replicate, ALL
    SIX override values, reservation triple) and requires the FULL canonical string per
    rollout.  Under CRN two masses share `reservation` entirely and differ only in the
    mass fields — that is what keeps 126 digests distinct over 8 identities.
  §3.3 ADOPTS PROTOCOL P §7 REPLAY GATE UNCHANGED as Stage XR, 1 rollout, FIRST.
    Fail -> X_DEFAULT_PATH_UNVERIFIED, terminal.  Carries limitation 63 (certifies
    overrides=None ONLY, so NOT a substitute for the anchor and vice versa) and
    limitation 36 (not runnable by an outside reader).

BLOCKER 4  THE ANCHOR DID NOT GATE.  v0.2 §8 order:
    XR(1) -> X0(0) -> XA anchor alone(18) -> XM six masses(108) -> XZ(0)
  Within EVERY mass, XC healthy(8) runs BEFORE XB ladder(10), so an unsafe body costs
  8 not 18.  §12 gives EVERY exit cost: 1 / 1 / 9 / 19 TERMINAL / 127 MAXIMUM.
```

## THREE S62 FINDINGS OF MY OWN — TWO ARE FACTS ABOUT THE PLANT

```text
(a) *** THE PLANT HAS NO GRAVITY. ***  cable_mechanics.py:101 emits gravity="0 0 0".
    model.opt.gravity == [0,0,0] ; qfrc_bias == 0 at t0.
    Stepped the compiled model, ctrl=0, 3.0 s sim time, ALL EIGHT MASSES:
      peak |gauge_true| = 0.0000 ue and tip radius EXACTLY 0.80000 m at every mass,
      0.200 kg INCLUDED.   (A1 gauge limit is 500 ue; tip radius limit 0.82 m.)
    => PAYLOAD IS PURE TIP INERTIA.  No sag, no static load, no static consumption of
       the A1 envelope.  MY S61 SENTENCE "1.157x the mass of the whole arm, HUNG AT THE
       TIP" carried a static reading that is FALSE HERE.  Withdrawn in v0.2 §1; the mass
       comparison stands as a DYNAMIC perturbation.  Nominal body mass 0.172800003 kg.

(b) THE PROBE SITS ~97x BELOW THE LOWEST ELASTIC MODE, so RESONANCE IS RULED OUT.
    Linearized undamped modal estimate, zero rollouts: M from mj_fullM (note the 3.x
    signature is mj_fullM(model, data, dst)), K by central finite differences of
    qfrc_passive under mj_integratePos, then scipy.linalg.eigh(K, M).
      mass    f1      f2      f3      f4      f5      f6   (Hz)
      0.000  77.34  117.29  167.58  217.11  229.85  254.47
      0.050  77.34   92.17  167.58  201.59  229.85  249.52
      0.200  77.34   87.19  167.58  199.59  229.85  249.06
      probe 0.8 Hz -> f1/probe = 96.7
    SCOPE, stated before use: linearized about ONE configuration, undamped, and K
    OMITS THE ELBOW `connect` EQUALITY CONSTRAINT because qfrc_passive carries plugin
    elasticity + joint damping only.  The omission can only RAISE frequencies, so it is
    CONSERVATIVE for the one conclusion drawn and for nothing else.  NO VERDICT RESTS
    ON IT.  (The cable's stiffness is a PLUGIN — jnt_stiffness is all zero, which is why
    a naive modal analysis returns an empty spectrum.)
    TWO READINGS ONLY: payload moves NO mode onto the probe (f1/f3/f5 do not move with
    mass at all), so the S60 attenuation's MECHANISM IS UNIDENTIFIED and v0.2 §14 says
    so; and the modes that DO move SATURATE HARD (f2 falls 21% over 0.000->0.050 kg and
    a further 5% over 0.050->0.200 kg) — a HINT, not evidence, that the payload effect
    may saturate, which is an argument FOR seven measured levels over an extrapolation.

(c) v0.1's ANCHOR WAS BUILT TO FAIL ON NOISE.  It demanded the anchor bracket EQUAL
    cell 6's (0.45, 0.50) exactly.  Re-derived cell 6's OWN margins from the screen
    artifact (Q95 = 0.37033237, threshold = 0.74066474):
      remEI  0.35   0.40   0.45   0.50   0.55   0.60   0.65   0.75   0.85   0.90
      |m|/th 0.826  0.482  0.196  0.021  0.214  0.333  0.481  0.655  0.812  0.879
    CELL 6 FAILS 0.50 BY 2.1% OF ITS THRESHOLD.  Requiring a new identity to reproduce
    the SIGN of a 2.1% margin is requiring it to reproduce noise, and the resulting
    X_ANCHOR_FAIL would be TERMINAL and MEANINGLESS.
    v0.2 §9.3: tau_anchor = 0.10 of threshold; CONSTRAIN THE NINE rungs at/above it;
    leave 0.50 UNCONSTRAINED.  *** THE 0.10 DOES NO WORK: smallest constrained 0.196,
    largest unconstrained 0.021, so ANY tau in (0.021, 0.196) GIVES THE IDENTICAL
    PARTITION. ***  Fixed from PUBLISHED margins, before any extension datum exists.
```

**THE ONE DEVIATION FROM INHERITED §9, AND IT IS PERMISSIVE IN MY FAVOUR.** v0.2 §9.6:
`X_UNSAFE_MASS` / `X_UNSAFE_LADDER_VALUE` are terminal AT THE ANCHOR and **exclude the
mass** elsewhere (ladder not run, execution continues, `mass_coverage = REDUCED`).
Strict inheritance would discard all seven masses because one rollout at 0.200 kg failed
a gate. **I flagged the direction and handed the decision to Codex**; reverting is one
line — move non-anchor `X_UNSAFE_LADDER_VALUE` to a terminal rule between R5 and R6.
Pinned as a rule rather than offered as a menu, so there is one exact state to review.

## THE S60 HARNESS DEFECT — THE MUTATION SWEEP CAN CERTIFY AN UNTESTED GUARD

**This is the most transferable thing I learned this session and it invalidates the face
value of any sweep either agent ran at sub-second per-case cost.**

```text
MECHANISM.  The sweep imports the target through importlib.spec_from_file_location,
which CACHES BYTECODE and invalidates on (source mtime IN WHOLE SECONDS, source size).
Every `require(True or ...)` mutant is EXACTLY EIGHT BYTES longer than the original, so
CONSECUTIVE CASES HAVE IDENTICAL SIZE.  When the focused suite runs in under a second,
consecutive cases also land in the SAME SECOND -> Python executes the PREVIOUS mutant's
bytecode and the harness records that verdict against the current case.

REPRODUCED, with stat() timestamps:
  duplicate_payload_id_check_removed   size 38010  mtime ...354.515  -> caught
  payload_id_membership_check_removed  size 38010  mtime ...355.138  -> SURVIVED
  duplicate_payload_id_check_removed   size 38010  mtime ...355.957  -> SURVIVED
                                        ^ SAME CASE AS LINE 1, OPPOSITE VERDICT
in isolation, 3 runs each:  first two ALWAYS caught, third ALWAYS survives.

BEFORE I found the mechanism, three passes over one file gave THREE DIFFERENT survivor
sets.  THE DANGEROUS DIRECTION IS THE FALSE `caught`: it certifies a guard no test
exercises, inside the exact ritual performed in order to be sure.

FIX (two lines, in every future sweep):
  env = dict(os.environ, PYTHONDONTWRITEBYTECODE="1")
  for cache in PACKET.rglob("__pycache__"): shutil.rmtree(cache, ignore_errors=True)
  and drop `-x` (it adds nothing and hides which case failed).
It could not bite before S58 because a driver-file case cost ~100 s.  It bites exactly
in the S58/S59/S60 regime where a focused file runs in 0.1-0.7 s.

RE-SWEPT THE JOINTLY APPROVED ROLE-COVERAGE ANALYZER WITH THE CORRECTED HARNESS:
  28 cases | 28 caught | 0 survivors | blob f911f2f3 unchanged afterwards
  (one bad anchor on the first run was my indentation; re-run alone -> caught)
=> Codex's S58 repair and my S59 tests HOLD UP.  That sentence could not have been
   written honestly last session.
```

## THE S60 FINDING — THE LADDER'S VERDICTS ARE PAYLOAD-CONDITIONAL

**Zero rollouts. Both inputs were already on disk. Nobody had read the contrast.**

§8 runs the ladder in four dev context cells and **they are not exchangeable**: cells 4/5
carry `payload_dev_nominal` (0.000 kg), cells 6/7 carry `payload_dev_0p050kg` (0.050 kg),
and **environment and contact vary WITHIN each pair rather than across them** — so payload
is orthogonal to both and the screen is a balanced two-level payload contrast at every
one of the ten ladder values.

```text
remEI   mean d @ 0.000 kg   mean d @ 0.050 kg   ratio   verdict
 0.35        2.679957            1.344812      0.5018  TESTABLE
 0.40        2.163189            1.085688      0.5019  TESTABLE
 0.45        1.768199            0.883461      0.4996  TESTABLE
 0.50        1.437453            0.722144      0.5024  SUB_THRESHOLD
 0.55        1.192002            0.580157      0.4867  SUB_THRESHOLD
 0.60        0.968039            0.485288      0.5013  SUB_THRESHOLD
 0.65        0.768364            0.382757      0.4981  SUB_THRESHOLD
 0.75        0.480152            0.250925      0.5226  SUB_THRESHOLD
 0.85        0.260104            0.131053      0.5038  SUB_THRESHOLD
 0.90        0.161944            0.086898      0.5366  SUB_THRESHOLD
ratio across the ladder 0.4867-0.5366, mean 0.5055
within-level spread (env + contact) 0.18%-3.6%, one cell 12.9%
THE NULL DOES NOT MOVE WITH PAYLOAD: q95_c 0.4114 / 0.4217 light, 0.3703 / 0.4277 heavy.
SIGNAL FALLS, NOISE DOES NOT.

ZERO-MARGIN CROSSING, per cell:
  cell 4  0.000 kg  last + at 0.60 (+0.152980)  first - at 0.65 (-0.058558)
  cell 5  0.000 kg  last + at 0.60 (+0.116911)  first - at 0.65 (-0.070901)
  cell 6  0.050 kg  last + at 0.45 (+0.145352)  first - at 0.50 (-0.015614)  = -2.1% of thr
  cell 7  0.050 kg  last + at 0.45 (+0.025561)  first - at 0.50 (-0.136106)  = +2.99% of thr
```

**TWO CONSEQUENCES THAT ARE LOAD-BEARING FOR A2:**

1. **The dev zero is a PAYLOAD result.** dev's remEI 0.50 is comfortably TESTABLE in both
   unloaded cells (+0.6125, +0.5962) and fails the all-cell conjunction only in the loaded
   ones — cell 6 by **2.1% of its threshold**. The named non-transfer outcome is real and
   must not be softened, but its **mechanism is payload, not severity**.
2. **remEI 0.45 is the EDGE, not a design point.** The binding cell clears it by 2.99%.

**WHAT I DELIBERATELY DID NOT CONCLUDE, AND MUST NOT LATER:** compounding the 0.506 ratio
out to the heavier reserved masses. **Two levels determine a RATIO, not a CURVE.** No
functional form in payload mass is fitted, implied, or recoverable. Doing it would be the
exact Lesson-11/12 move I have flagged in other people's work twice. What IS established:
the direction, its size at 0.050 kg, and that **every TESTABLE verdict was established at
0.000 and 0.050 kg and at no other mass.**

**A SHARPENING OF THE S58 ROLE-COVERAGE READ, TO CARRY EVERYWHERE:** §9's counts for val
(1) and test (1) are **dev-context verdicts applied to a severity reserved in another
split**. That IS what §9 pre-registers, and it is **not** the claim that the severity is
testable in that split's own contexts. No write-up may collapse those two.

Reserved payloads: **dev 0.000/0.050 · pilot 0.025/0.075 · val 0.100/0.125 · test
0.150/0.200 kg.** Pilot, val and test each reserve ≥1 unscreened mass.

## THE A2 DECISION — RULED ON BY CODEX (S60), ANSWERED BY ME (S61)

```text
CODEX'S RULING, ACCEPTED IN FULL:
  MEASURE FIRST.  No Protocol-P v2.3.3 section bump — it is a closed, executed
  provenance object.  A SEPARATELY VERSIONED, DEVELOPMENT-ONLY pre-registration with a
  fresh private identity/seed band, materializing/reading NO pilot, val or test
  identity, payload, label, manifest row or outcome.
MY S60 50-ROLLOUT ESTIMATE WAS WRONG IN BOTH WAYS CODEX NAMED:
  SIX unmeasured masses, not five — 0.025 kg is unmeasured too, because two levels
    determine a RATIO not a curve, so an INTERIOR mass is unmeasured exactly as an
    exterior one is.  I wrote that sentence and then interpolated anyway.
  ONE structural candidate per mass answers whether that candidate survives; it does
    NOT locate a boundary.

THE THREE A2 OPTIONS ARE UNCHANGED AND STILL OPEN:
OPTION A  move the severity grid DOWN below the measured boundary with real margin.
          COST: the mild-degradation stratum becomes untestable by construction.
OPTION B  COMPRESS the payload ladder so every split sits inside a verified band.
          COST: payload stops being a generalization axis; Slot 7's factorial weakens.
OPTION C  keep both and PRE-REGISTER a payload-bounded non-transfer shape beside the
          role-coverage-bounded one.
The extension document (§9) pins which outcome licenses which option.  DO NOT choose
before the measurement.
```

## THE PAYLOAD-BOUNDARY EXTENSION — WHAT SURVIVES v0.1 UNCHANGED

**`Reproducibility Packet/protocol/payload-boundary-extension-v0.2.md`. READ THE FILE
before doing anything on it. Do not reconstruct it from this summary.** The block above
covers what CHANGED; this is what v0.2 carries forward from v0.1 unchanged.

```text
7 MASSES     0.050 (ANCHOR, already measured) + 0.025 0.075 0.100 0.125 0.150 0.200
CONTEXT      FIXED: env_dev_iso25c + contact_dev_none + t01 + probe 0.10 N / ramp 0.25
             = screen cell 6 in everything but payload mass and identity.  Within-level
             env+contact spread re-derived S61: 0.18-3.60% at eighteen of twenty rungs;
             the two outliers are 12.89% and 6.81% at remEI 0.85 and 0.90 (the MILDEST
             rungs, smallest D).  In the boundary region 0.45-0.65 everything is <=3.48%.
LADDER       the same ten reserved remEI values.  FIXED, not adaptive — those ten ARE
             the union of every split's reserved severities, so "which reserved
             severities survive at this mass" is answered exactly, with no sequential
             stopping rule that could be accused of being chosen after a result.
             A crossing below 0.35 is the pre-registered answer "none", not a failure.
COST         per mass 18 distinct physical rollouts (8 healthy FIRST, then 10 ladder;
             k=0 reused as the matched reference) and 76 logical references
             126 + 1 replay gate = 127 MAXIMUM; 19 ANCHOR-TERMINAL; 532 logical refs;
             53.1-58.2 min at the measured 25.1-27.5 s/rollout
INVARIANTS   X1-X14 (X13 the physical key, X14 the classifier returns exactly one
             outcome), carrying requirements (x)(y)(z)(aa)(bb)(cc)(dd) forward
AUTHORIZATION  five steps in §13; none inferable from another.

MEASURED S61, ZERO ROLLOUTS: the packet's existing mechanics preflight
(assignment_generator.py:566-597) compiles a plant per declared mass and asserts the
realized body-mass delta exactly.  All EIGHT masses realize exactly at atol 1e-12 in
0.04 s.  NOMINAL TOTAL BODY MASS IS 0.172800003 kg, so the 0.200 kg test payload is
1.157x the mass of the whole arm — AS TIP INERTIA, NOT AS A HANGING WEIGHT (S62 (a)).
X_UNSAFE_MASS exists for that reason and its mechanism is dynamic, not static.
```

## THE S61 SWEEP FINDINGS — ONE SILENT GAP IN CODEX'S REPAIR, ONE THREE-WAY COLLISION

**Both of Codex's S60 findings were REAL and I reproduced both with instruments sharing
no code with the analyzer. Then I swept its repair, because Lesson 79.**

```text
FIRST SWEEP (Codex's state 7f9ed558)  66 cases | 59 caught | 7 SURVIVORS | reproducible
CHARACTERISED ALL SEVEN BY CONSTRUCTION — each bad state driven through the committed
module AND through a copy with that one guard off, each variant in a UNIQUELY NAMED file
so the S60 stale-bytecode mechanism cannot apply at all.

line 426  isinstance(hard_gates_passed, bool)   [CODEX'S NEW GUARD]
  guard OFF -> *** ACCEPTED THE BAD STATE ***  the string "false" is TRUTHY, and the
  next line only tests for truth.  An unsafe cell's margin would enter the boundary
  read.  REAL SILENT GAP.  Nothing in 1,115 tests could have failed.
line 433  cell_verdict in LADDER_VERDICTS       [CODEX'S NEW GUARD]
  guard OFF -> still refused, by the margin/verdict equality check, but with a sentence
  blaming the margin for an unrecognised LABEL.  Not a gap; worth keeping and asserting.
lines 250/254/279/283  the payload list/object checks   [MINE]
  guard OFF -> still refused, with a BYTE-IDENTICAL message.

*** THE CAUSE, AND IT IS THE TRANSFERABLE PART ***
require_binary_context_factors builds its message with an F-STRING over the factor name:
    f"the assignment carries no context_profiles.{factor} list"
which for "payloads" renders VERBATIM the sentence the two payload readers each carried
as a STRING LITERAL.  THREE raise sites, ONE sentence, and grep for the literal finds
TWO OF THEM.  It runs FIRST on the document path, so the two document tests that look
like they cover the payload readers were certifying the binary-factor check all along,
and my own S60 docstring claiming these messages were distinct was true of the split
guards and FALSE of these.

FIXED: all three sites name their own read; direct-call tests for the two the document
path never reaches; a parametrized test that drives one malformed document through all
THREE functions and requires three distinct sentences — a COMPARISON, not a source
search, because a source search demonstrably cannot see this.
Codex's type guard gains a parametrized test over "false", "no", 1, [0].
Codex's closed-set guard gains a test asserting its own sentence on UNSAFE_LADDER_VALUE.

FINAL SWEEP (my state 39048d26)  66 cases | 65 caught | 1 SURVIVOR | reproducible | blob
  restored.  The survivor is `row.payload_id in masses` — arithmetic, limitation 76.
focused 105 (was 94) | full suite 1,126 (was 1,115) | artifact BYTE-IDENTICAL after
```

**ONE MORE THING THE SWEEP TAUGHT: refusing an `UNSAFE_LADDER_VALUE` row is a SCOPE
BOUNDARY, not a corrupt artifact.** The driver legitimately writes `verdict:
UNSAFE_LADDER_VALUE, margin: null` and continues (§9). Both my original and Codex's
version refuse such a document; only the reason a reader sees has changed. Now commented
at the guard. **No write-up may say this read covers every non-terminal §9 shape.**

## THREE DEFECTS THE S60 TESTS FOUND IN MY OWN NEW CODE

```text
1. FOREIGN EXCEPTION TYPE.  A mislabelled payload split killed the run inside
   expand_reservations with a bare IndexError — my contract says PayloadConditioningError.
   FIXED BY ORDERING (require_binary_context_factors runs BEFORE the expansion), not by
   catching, so the reason names the document.  Same shape as limitation 70.
2. TWO GUARDS NO DOCUMENT CAN REACH.  payload_levels's "exactly two levels" and "the
   levels are the same size" are FORCED by the §8 mass-equality check (four pinned values
   = two masses over two cells each).  Their tests call the function DIRECTLY, and a third
   test pins WHY they are unreachable so a future cell-table change turns them live.
3. A TEST ASSERTING A PROPERTY OF THE DOCUMENT.  Deleting `rows.sort(...)` survived the
   first sweep because the committed ladder is already ascending — Lesson 77 exactly.
   Closed with a case that stores the ladder reversed.
S60 SWEEP (fixed harness, two identical consecutive passes):
   44 cases | 43 caught | 1 SURVIVOR | 0 bad anchors
   the survivor is ARITHMETIC: `row.payload_id in masses` cannot fail once the duplicate-id
   check passes, because expand_reservations draws the id from the same list masses is
   keyed by.  Recorded in the code.  Never call it a runtime check.
```

## READ THIS FIRST — Protocol P lives in a file, not in this summary

```text
Reproducibility Packet/protocol/protocol-p-v2.3.3.md
canonical sha256   5689dad7ce4194b9a7dbe381006027df178997adf732f5734a77ef048bdf421f
54,621 bytes, LF, no BOM, raw == canonical, pinned text eol=lf
JOINTLY APPROVED — Claude S43, Codex S43. The specification loop is CLOSED.
NOTE: §8's "roughly 0.39" for Stage 0 is an S39-era APPROXIMATION, not a pin. Executed
value is 0.400881 (+2.79%). Codex agreed in its S48 that no protocol change is warranted.
Settled — do not reopen, do not edit v2.3.3.  Codex S55: no bump for the Stage-C label.
§8 LINES 520-523 PIN THE CELL TABLE IN PROSE (used by the S60 read):
  cell 4 = r00  payload 0.000 kg  iso25c  contact brief
  cell 5 = r01  payload 0.000 kg  warm2c  contact none
  cell 6 = r02  payload 0.050 kg  iso25c  contact none
  cell 7 = r03  payload 0.050 kg  warm2c  contact brief
```

**Read that file before doing anything on Protocol P. Do not reconstruct the protocol from this summary.** It contains the universe, the two hash domains, the terms block, the provenance scope, the seam (§3), the construction path (§4), the screen reservation (§5), the identity table (§6), the replay gate (§7), the window table, the statistic, Stages 0/A/B/C (§8), both secondaries, the outcome cases (§9), role coverage, the terminal branches, the fail-loud invariants I1–I12, I13a, I13b (§10), and the cost (§11).

**Version discipline — three versions deep. If it ever needs correcting again, bump the version and `git mv`; do not edit in place.** v2.3.1 (`8c268f8f…401d76`) and v2.3.2 (`9d257017…738ba6e5`) are superseded, each approved by me and blocked by Codex, **neither ever executed**; bytes recoverable from the `Claude Session 41` / `Claude Session 42` commits. **A version bump must also update `PROTOCOL_FILENAME` and `PROTOCOL_CANONICAL_SHA256` in `scripts/protocol_p_replay_gate.py`; the Stage-0 script and the driver inherit both by import, but three test files pin the digest independently.**

## Where the project is

- **Phase 2 (Execution) is OPEN.** All Phase-1 gates in force. **Schema v1.0 + Amendment A1 in force.** Contract changes run through the **amendment protocol**.
- I am **Claude**; last session was **Session 62**; next session I run is **Session 63**.
- **`config.json` is deliberately NOT frozen** and does not exist. All hashes are `dev-`; no `dev-` trace may enter confirmatory analysis.
- Real data exists: `data/gate3-base-dev-pilot-val-c1-s` (3.86 GB, git-ignored, local only). 472 reservations / 944 manifest rows / C1+S / dev 152, pilot 152, val 168. **Test untouched: 0 identities, 0 payloads.** **Slated for full regeneration from zero after A2 — these 472 payloads become a superseded pre-amendment set in the packet exclusion trail. Read them; do not build on them.**
- **STAGES A/B/C HAVE RUN — Codex's S57, 135 physical rollouts, CASE_B, JOINTLY APPROVED.** Stage 0 RAN in S48 at ZERO rollouts; `results/protocol_p/sensor_only_difference_null.json` is tracked and **JOINTLY APPROVED**. The §9 role-coverage read is now **JOINTLY APPROVED** (above). The payload read's **RESULT ARTIFACT is JOINTLY APPROVED** (S60 Codex / S61 me); its **script + tests are UNDER REVIEW at my S61 blobs**.
- **THE ROLLOUT COUNT HAS BEEN WRONG FIVE TIMES: one → four → thirteen → fourteen → FIFTEEN pre-run. Carry the table, never a remembered number.**
```text
FIFTEEN BEFORE CODEX'S S57.  Measured in S58 by sweeping BOTH agents' primary records:
  Claude S39  1   from-scratch reproduction of a delivered row, 26.9 s
  Codex  S39  1   its OWN independent replay (HumanReport39.md:49) *** every earlier
                  recount missed this one ***
  Claude S40  1   all-None transparency regression, 26.4 s
  Claude S41  5   FOUR onset-consequence + ONE all-None regression
  Claude S45  2   25.58 s (pre-ephemerality-fix) and 26.37 s (the recorded result)
  Codex  S45  2   reviewer runs; final reviewer replay 27.46 s (the first has NO
                  recorded time — do not invent one)
  Claude S46  2   26.64 s clean control, 27.03 s injected-stray-write refusal
  Claude S51  1   25.08 s regression after the shared-import edit
              --
              15
+ Codex S57: 1 replay (36.42 s) + 135 stage rollouts = 136   =>   TOTAL 151
NOT RUN IN S58, S59 OR S60.  Nothing on the gate's watched path changed and the
measurement it guards is already spent.
```
- **Progress report DONE at S56** (regular, covers S49–S56), **loop CLOSED at round five, blob `83c527ced4e12ce27cfbf83601c89fc0e670a3cd`. Do not reopen. NEXT REGULAR IS MY SESSION 64**, unless a phase transition or an **approved written Claim-Sheet amendment** fires sooner. **An approved A2 fires it.**

## Escalation trigger — content-based, and it has now held ten times

**The binding rule: escalate to the director when a round re-litigates a point already
settled, or when we disagree on a judgment neither of us can resolve from source — NOT
when a round finds a new, verifiable defect.** Every loop to date closed on new findings:
the specification loop (seven rounds), the seam, the replay gate, Stage-0 implementation,
the Stage-0 result, the progress report, Step 24, the public log, the extraction and
construction layers, the driver (blocked S54, corrected S55, approved S55), the S56/S57
round, and **the role-coverage loop (blocked S58, corrected S59, approved S59, closed at
the same state S60)**.
**If a round re-opens the two-domain hashing split, the window origin, the statistic, the
ladder, the driver-vs-seam boundary, the S45/S46 answers, the S47 reachability closure,
the S49 identity-scope narrowing, the S55 Stage-C label ruling, the S59 readback ruling,
or the S59/S60 `.gitattributes` ruling — escalate on the spot regardless of count.**

## HONEST ODDS — revised by the S60 finding

The S39-era projection is superseded in its framing: the screen has now MEASURED the
boundary at dev payloads, which is better evidence than any projection.

```text
MEASURED, at the selected probe (0.10 N / ramp 0.25), all four dev cells:
  detectable to remEI 0.60 at 0.000 kg, to remEI 0.45 at 0.050 kg
  the all-cell conjunction therefore stops at remEI 0.45, clearing by 2.99%
  dev's reserved severities (0.75, 0.50) and pilot's (0.85, 0.60) are BOTH sub-threshold
UNKNOWN, and not to be guessed: the boundary at 0.075-0.200 kg.
```
**The success bar is UNTOUCHED** (≥0.05 macro-F1, −0.02 per-class recall non-inferiority,
≥10% tracking reduction, paired hierarchical bootstrap, ≥5 seeds).

*Naming note: "M2" is **retired inside the protocol file**. Below it still labels **my** S39
measurement — the gauge-path-only decomposition. If writing anything Codex will read, spell it out.*

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
per cell held EXACTLY fixed, redrawn at 8 identities, all 28 within-cell distances, `method="higher"`.
```text
cell   min / median / max           Q95 (27th of 28)   2*Q95
 4     0.1540  0.2807  0.3731            0.3555        0.7110
 5     0.1524  0.2620  0.4325            0.4251        0.8502
 6     0.1377  0.2709  0.3922            0.3176        0.6351
 7     0.1443  0.2983  0.4706            0.3854        0.7708
```
**A decomposition, NOT a bound.** It **validates Stage 0** (the synthetic no-plant value sits
inside the real-plant 0.318–0.425) and identifies **cell 7 (payload + warm + contact) as the
binding cell** — **which the S60 read now explains: cell 7 is a 50 g cell.**
**Conditional healthy-null diagnostic only — no mechanism attribution.**

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

## THE SCREEN RESULT — approved, do not re-run, do not re-review the arithmetic

```text
artifact  Reproducibility Packet/results/protocol_p/stage_abc_screen.json
blob      209a87ae5daa171016d566e07ed14c7c71ef0f18
DOCUMENT DIGEST (canonical, the one to quote)  e800ae6c05c0dda0db82e2c94ab6350cd7d9e0bf544a9659fdacf2bad53999fc
raw CRLF working-tree rendering (NEVER quote unqualified)  c48c2e4d3a8a84a5b10127afc2a7c0f4bacc0ae6290712546432058327008756
  index 588,448 bytes / 0 CRLF pairs ; working tree 599,841 bytes / 11,393 CRLF pairs
  MEASURED S60 with a plain-bytes instrument: LF-normalised worktree bytes == index bytes.
selected candidate 0.10 N / ramp 0.25.  3 Stage-A drops => 168 - 11*3 = 135 rollouts.
TESTABLE at remEI 0.35 / 0.40 / 0.45 ; SUB_THRESHOLD at 0.50 through 0.90.
Stage-A worst-cell scores: 0.1|0.25 0.2464 (selected) > 0.1|0.125 n/a, 0.15|0.5 0.2090,
  0.05|0.125 0.1544, 0.1|0.5 0.1532, 0.05|0.25 0.1485, 0.05|0.5 0.0936.
  *** A HIGHER AMPLITUDE DID NOT WIN.  0.15 N scored BELOW 0.10 N.  The ramp matters. ***
diagnostic_pause TRUE in all four cells: q95_c 0.41139871 / 0.42169416 / 0.37033237 /
  0.42767186 vs §8's 0.30 trigger.  It gates nothing.  The packet README says so.
```

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
7. **Evaluation driver + confirmatory manifest** — **MINE.** One CLI owning the `[t_c,t_c+5s]` slice, role joins, paired C1/S table, exclusions, CIs; rejects `dev-`/wrong-hash/cross-role/incomplete-pair/truncated. **Must implement the pre-registered statements (a)–(dd) carried below.**

**The (a)–(dd) driver requirements, carried verbatim in shape:** (a) `ood_flag` exclusion from known-class metrics; (b) the **degradation-ladder rule** (S30/S31); (c) **pilot→val moves one variable while val→test additionally moves half-fraction → complete factorial** — *and, under A2 pin 4, no longer moves the contact window*; (d) S33's two findings; (e) the mild-stratum development diagnostic **at its true scope** and the per-channel attribution; (f) **[S35]** the excitation discontinuity; (g) **[S36]** the yardstick discontinuity (D) + the run-to-run range statement (E) + trajectory-partial margin coverage; (h) **[S37]** the operation mismatch (F), thermal near-invariance (G) as a *property*, the amplitude ceiling (H); (i) **[S38]** the **window origin (J)** — the driver MUST use the same origin the protocol pins — plus the matched/unmatched asymmetry and role-coverage counts; (j) **[S39]** the **construction path (K)** and the **unmatched-identity confound (L)**; (k) **[S40]** distinguish **`base_pair_id` from realized `pair_id`** in every identity join, and never stamp an overridden run with the base config hash; (l) **[S41]** any file whose **raw bytes** enter an identity must be hashed through the correct-domain helper; (m) **[S42]** that helper must be chosen **by file domain**; (n) **[S43]** every identity expression must **name the object it hashes**; (o) **[S44]** test the **wires between stages**, not only each stage; (p) **[S45]** every clean report must **disclose its denominator** and refuse to report when it cannot support the claim; (q) **[S46]** every guard must be **reachable from the construction that will run**, and every fixture large enough for the defect it exposes; (r) **[S47]** every pinned literal that also lives in a bound document is checked by EQUALITY, never adoption; (s) **[S48]** every test that claims to verify a gate must CALL it and assert the REASON for a refusal; (t) **[S50]** every documented dependency must be verified against the running system; (u) **[S51]** assert a phrase UNIQUE TO ONE RAISE SITE, and construct preconditions through `utils/protocol_p_conditions.py`; (v) **[S52]** obtain the source reservation from the I1-pinned assignment and never construct one, and test per BRANCH not per guard; (w) **[S53]** record a REUSED row's provenance by CITATION, and DERIVE the fault onset; (x) **[S54]** key the results table on the PHYSICAL BODY, and make every clean-census check reachable from a state that could fail it; (y) **[S55]** derive the reported set from what was MEASURED rather than from which candidates survived, CONSUME the hard-gate report in EVERY stage, and persist the gate evidence, step count and elapsed time on EVERY exit path including terminals; **(z) [S56]** every check the driver makes must be given a source INDEPENDENT of the thing it checks — a comparison whose two sides are produced by the same function from the same arguments is a report of a check rather than a check — and no result artifact may record an absolute filesystem path; **(aa) [S57]** every count must distinguish OCCURRENCES from IDENTITIES — 180 provenance references over 168 distinct stamps, never "180 stamps" — and every historical figure must be re-derived from primary records; **(bb) [S57]** no outcome case may be reported until the healthy-vs-faulted readback has distinguished a measured null from an override that never reached the plant; **(cc) [S59]** every digest a result artifact records must be taken in the domain of the file's KIND — canonical for tracked text, raw only for binary — and every check a review ADDS must have a committed test that constructs the state it refuses; **(dd) [NEW S60]** every verdict the driver reports must name the CONTEXT POPULATION it was established over, because a conjunction over context cells is a statement about exactly those cells and the confirmatory splits are not drawn from them — and no coverage count computed from those verdicts may be presented as a statement about a split's own contexts; **(ee) [NEW S61]** every refusal message must be unique to one raise site **as rendered**, not as written — a message assembled by an f-string can duplicate a literal one exactly, which no text search of the file will find, so the check is a runtime comparison of the sentences the sites actually emit. **(ff) [NEW S62]** every guard must be checked against what ELSE in the design produces its passing signal — a distinctness check over units that already differ for another reason certifies nothing — and after any change to what the design holds fixed, every downstream key, join and dedup must be re-asked what it was actually distinguishing, because a key is a claim about what makes two things different and the design just changed that claim.

**Order:** (1)✓ → (2 foundation)✓ → (2 role-write)✓ → (3 assignment)✓✓ → (2 generator + base roles)✓✓ → (2 hardening)✓✓ → (dev separability check)✓ **[NEGATIVE]** → Protocol P v2.3.3 spec ✓✓ → seam + 37 tests ✓✓ → replay gate ✓✓ → Stage-0 implementation ✓✓ → **Stage 0 RAN, S48 ✓** → Stage-0 result ✓✓ → Progress Report S48 ✓✓ → packet Step 24 ✓✓ → public README ✓✓ → extraction + construction layer ✓✓ (S51–S53) → driver + results layer (S54 built, S54 blocked, S55 corrected, S55 approved ✓✓) → S56 pre-registered helper + Step 25 ✓✓ → **Codex S57: replay gate (36.42 s) then STAGES A/B/C — 135 rollouts, CASE_B ✓** → **my S58: every number independently reproduced, result APPROVED; §9's role-coverage read found UNIMPLEMENTED and built at zero rollouts — dev 0 / pilot 0 / val 1 / test 1** → **Codex S58 BLOCKED it on three real findings and corrected it** → **my S59: all three CONFIRMED; a FOURTH found in the repair (raw-domain digest of a tracked text file); 23-case sweep, 13 survivors, 12 real, closed with 12 tests** → **Codex S59 APPROVED all four states and held the loop open for my explicit approval** → **my S60: approval posted, LOOP CLOSED AT THE SAME STATE; the mutation-sweep harness found to give false verdicts and fixed; the approved analyzer re-swept clean (28/28); the payload-conditioning read built at zero rollouts** → **Codex S60 blocked the payload read on two real defects, corrected them, ruled MEASURE FIRST via a separate development-only pre-registration, and blocked A2** → **my S61: both findings confirmed independently; the result artifact and both READMEs approved at Codex's states; the sweep over Codex's repair found a SILENT GAP in one of its own new guards and a three-way message collision one copy of which is built by an f-string; script+tests returned at new blobs; the payload-boundary extension v0.1 DRAFTED** → **Codex S61 APPROVED the analyzer/tests (loop CLOSED) and BLOCKED the extension on four findings** → **my S62: all four confirmed against primary sources, none contested; v0.1 `git mv`'d to v0.2 and rewritten — CRN across masses, a SECOND prerequisite (`PhysicalKey`), one ordered exhaustive classifier, pinned artifact/provenance contracts, the anchor staged first; plus three findings of my own (zero gravity, probe 97x below the lowest mode, a noise-fragile anchor) ← WE ARE HERE** → Codex reviews v0.2 → the THREE seam/key/executable prerequisites (both approve) → plan mode → SEPARATE execution authorization → the extension RUNS → both read it → written amendment A2 + replacement assignment (both approve) → **full regeneration from zero** → re-audit → (4/5 models+calibration) [me] → (2 remaining roles) [Codex] → (6 controller + sample-size) [shared] → **joint immutable freeze** → one-shot confirmatory generation + eval (7) → Phase 3.

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
- **`scripts/utils/assignment_generator.py`** — the S44 seam at the top: **`ScreenOverrides` (frozen, 5 fields, `is_active()`), `screen_pair_id` (105), `_screen_stamped_hash` (122)**; **`_step_index` (217) fails loud off-grid**; `build_identity_manifest` (261); `audit_manifest_against_assignment` (321); `_physical_config` (401; the ramp default `duration/2.0`); `_fault_components` (500); **`_plant_payload` (600)**; **`_generate_reservation` (607; RETURNS a 6-tuple; the CablePlant is NOT returned)**; `materialize_base_dataset` (731). **Line 24 `from .cable_plant import CablePlant` is what makes every importer of this module a transitive `mujoco` importer — including the driver and, as of S60, the payload read.**
- **`scripts/utils/gate3_assignment.py`** — `expand_reservations(document)` → `list[ScenarioReservation]` (fields include `payload_id`, `env_profile_id`, `contact_profile_id`, `split`). **`BALANCED_CONTEXT_CELL_TABLE` (line 28)** and `_context_cell_table` (616), checked for equality against the document's `context_cell_table`. **Lines 648-697:** `seed = seed_base + 10*ordinal`, `sim/fault/sensor/controller = seed+0/1/2/3`, `base_pair_id = basepair_{split}_t{ti:02d}_f{fi:03d}_r{rr:02d}`, realized `pair_id = base + "_dataset0"`. **`expand_reservations` indexes each split's payload/environment/contact list POSITIONALLY, so a short list raises a bare `IndexError` — validate counts before calling it (S60).**
- **`scripts/utils/storage_contract.py`** — `IdentityManifestRow` (20 fields); **`_valid_config_hash` strips exactly `dev-` then requires 64 lowercase hex.**
- **`utils/config_contract.py`:** `load_config(config_path, schema_path, *, require_frozen=False)`. `file_sha256` is a **RAW-byte** hash; `canonical_json_bytes` + `sort_keys`/`separators`/`ensure_ascii=False`/**`allow_nan=False`** is the document path and the canonical-JSON precedent Protocol P matches.
- **`utils/sensor_model.py`** — `config_hash` is **free-form provenance, never validated**, which is what makes the derived screen-provenance stamp safe. Temperature reaches the gauges at `:423-424` (10 µε/°C); the 0.5 µε quantizer at `:429-431`. **Carries no state across `observe` calls (measured S45).**
- **Rollout entry point is `utils/online_loop.run_online_rollout(plant, sensors, *, n_steps, history_steps, command_policy, reference_fn=None, temperature_fn=None)`.**
- **Assignment structure:** 19 known settings per split, +2 compound/OOD in val/test; **2 trajectories per split**, split-exclusive; realizations 4/4/4/8; seed bases 110000/210000/310000/410000; reservations **152/152/168/336 = 808**. Expansion order **healthy → structure → actuator → sensor** — **extending `grid["structure"]["severities"]` shifts every later ordinal and therefore every later seed**, which is why Codex chose full regeneration.
- **Structural severities by split: dev {0.75, 0.50}, pilot {0.85, 0.60}, val {0.90, 0.40} + OOD 0.55; test {0.65, 0.35} + OOD 0.45.** Payloads: **dev {0.000, 0.050}, pilot {0.025, 0.075}, val {0.100, 0.125}, test {0.150, 0.200} kg** — the S60 read's subject.
- **Context cell table** (index `(trajectory_index * realizations + replicate) mod 8`), each `[payload_idx, env_idx, contact_idx]`: `0:[0,0,0] 1:[0,1,1] 2:[1,0,1] 3:[1,1,0] 4:[0,0,1] 5:[0,1,0] 6:[1,0,0] 7:[1,1,1]`. `t00`→{0,1,2,3}, `t01`→{4,5,6,7}. **Each factor is addressed by a BINARY index, so every split reserves exactly two profiles of each kind.**
- **Contact profiles:** dev_none `null`; dev_brief `[2.0,2.5]`; pilot_delayed `[2.6,3.2]`; val_extended `[1.8,3.3]`; test_sustained `[1.6,3.8]` → **A2 pin 4 changes this to `[1.8,3.3]`**. Offsets are relative to onset. All non-null profiles use `endpoint_plane_z_m = 0.2`.

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
- **THE STAGE-A/B/C PROGRAM.** `scripts/utils/protocol_p_results.py` (`e84e5f9f…`) and `tests/test_protocol_p_results.py` (`cbac30ed…`, 77) are **JOINTLY APPROVED and UNTOUCHED.** `scripts/run_protocol_p_screen.py` (`7668793e…`) and `tests/test_protocol_p_driver.py` (`23222d0e…`, 148) are **JOINTLY APPROVED (Codex S56) AND EXECUTED ONCE (Codex S57, 135 rollouts). Do not re-run `--mode execute`.**
- **THE ROLE-COVERAGE READ — JOINTLY APPROVED S59/S60.** `scripts/analyze_protocol_p_role_coverage.py` (`f911f2f3`) + `tests/test_protocol_p_role_coverage.py` (`83c7d640`, 46) + `results/protocol_p/role_coverage.json` (`6d6d23b9`). **Its shape is pinned to the CURRENT assignment and it must be REVISED, not merely re-pointed, after A2 (limitation 71).**
- **THE PAYLOAD-CONDITIONING READ — RESULT JOINTLY APPROVED, CODE UNDER REVIEW.** `results/protocol_p/payload_conditioning.json` (`c11f7067`, canonical sha256 `47ec3571…`) is **jointly approved** (Codex S60, me S61) and my S61 edits regenerate it byte-identically. `scripts/analyze_protocol_p_payload_conditioning.py` (`39048d26`) + `tests/test_protocol_p_payload_conditioning.py` (`b9e81f63`, 105) are **under review at my S61 blobs**. **Not pre-registered; the artifact's second key is an `authority` field saying so and a test asserts that string.** Same post-A2 revision obligation as the role-coverage read.

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
- **Failure shapes:** hypothesis failure (clean negative) vs **method failure**. **Inconclusive (Slot 13):** diagnostic-only · fault-specific/bounded · confound-fragile · excitation-dependent · **role-coverage-bounded** · **[S60 CANDIDATE, not yet in the sheet] payload-bounded.**

## Carried limitations for the Technical Report / Gate 7

1. **2^(3−1) parity residual:** `I(trajectory ; full cell)` = 1 bit in dev/pilot/val, 0 at test.
2. **The OOD arm rests on only 2 compound settings per split** — thin. **No severe-band OOD claim will be made.**
3. **Test severities sit partly outside the fit hull.**
4. **`split_group_id` is unique per reservation**, so its one-mapping assertion is vacuous; the real guarantee is trajectory/fault exclusivity, which does hold.
5. **`_assert_fault_independent_context_cells`** is correct only because trajectory blocks are disjoint mod 8 at the actual values. Both pinned; cannot silently drift.
6. **[S33] Finding 1** — structural severity grid below the 2× synchronous margin at every reserved severity. **Quadruply qualified** (S35 A, S36 D, S37 F, S38 J). **[S60: now MEASURED at dev payloads — see limitation 72.]**
7. **[S33] Finding 2 (contact), non-blocking.** 236 runs assigned a contact profile; **11 actually touched** (4.7%). All 11 are encoder **bias (7) or drift (4)**. **Realized contact is an EFFECT OF THE FAULT**, direction **favours S**. Addressed by A2 pin 4.
8. **[S34] The mild-stratum development diagnostic** — at dev EI 0.75/0.50 neither suite separates structure; the only consistent structural signature is a C1 IMU channel. **State at that scope only.**
9. **[S35] The excitation discontinuity** — the delivered probe is ~5.8× weaker than the screen that justified its amplitude.
10. **[S36] The yardstick discontinuity (D)** — per-gauge five-sigma at W=640 applied to a four-gauge statistic at W=768; error 7.7%, direction lax.
11. **[S36] The run-to-run range statement (E)** — **report as a range statement, never as a test.**
12. **[S36] Margin coverage is trajectory-partial.**
13. **[S37] The operation mismatch (F)** — a threshold on a single window applied to a difference of two; and **a matched-seed difference admits no sensor-only threshold at all** because CRN cancels the sensor term.
14. **[S37→S38 CORRECTED] Thermal near-invariance (G)** — a *property*, not a defect. **NOT exact cancellation** — thermal enters inside the 0.5 µε quantizer.
15. **[S37] The amplitude ceiling (H)** — the probe could not exceed 0.15 N without violating an approved actuator-authority limit. **[S60: and 0.15 N scored BELOW 0.10 N in Stage A anyway — the ceiling was not the binding constraint.]**
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
47. **[S50, RESOLVED S51] Stage 0's script no longer imports `mujoco` at all** — measured zero after the extraction, pinned by a test. **The DRIVER still does** (via `assignment_generator → cable_plant`), which Step 25 states explicitly. **[S60: the payload read imports it too, through `expand_reservations`.] Never write "needs no physics engine".**
48. **[S51] `utils/__init__.py` re-exports `SCHEMA_VERSION`, so ANY `from utils import X` imports NumPy.** `utils/protocol_p.py` itself imports only the standard library.
49. **[S51] `require_screen_reservation`'s `sensor_seed` check and I8's base-distinctness check are both CODE guards.**
50. **[S51] The torque gate's inclusive boundary is EXACT in IEEE double at both association orders** — `0.15*2*0.40 == 0.60*0.20 == 0.12`. **Any refactor of that arithmetic must re-measure it.**
51. **[S52] The construction layer's cell binding is over THREE IDENTIFIER STRINGS, not over the body.** Not a defect — the driver's source comes from the I1-pinned assignment. **The Technical Report may not say this module verifies the body.**
52. **[S52, SUPERSEDED IN PART BY S56] `build_overrides`'s `require_constructed_condition` call is tautological and no test can make it red.** **STILL TRUE OF THAT CALL.** What changed is that the driver now ALSO checks the constructed tuple against a document-derived expectation (`require_preregistered_faults`), which is not tautological. **Never describe the `build_overrides` call as a live guard; DO credit the driver-level one.**
53. **[S53, CORRECTED S57]** **MEASURED: there are exactly 168 DISTINCT stamps, one per physical rollout, referenced 180 times.** Correct form: **168 distinct stamps, one per physical rollout; 180 references to them in the results table; the twelve reuses reference an origin's stamp a second time.** What must never be written is that the table contains 180 *stamps*.
54. **[S53] The Stage-0 artifact's reported statistic has NEVER been recomputed after the S51 refactor** and cannot be without re-spending the measurement. A 2-pair run's q95 is `0.1894914916579524` against the reported `0.4008810868833315`. **Never write "bit for bit" without naming the 2-of-100 scope.**
55. **[S54] `require_inventory_shape`'s distinct-body count is a CODE guard** — forced by arithmetic once the row keys are unique.
56. **[S54] The 28-distance check inside `gauge_only_null` is UNTESTED; the identical check in `stage_c_null` is the exercised one.** **Do not write that both Stage-C size checks are covered.**
57. **[S55] A green suite is evidence about the states it enters, and nothing else.** The 906-test suite passed while two of three real defects were live. **No write-up may present a suite count as evidence of driver correctness.**
58. **[S55] Section 9 does not define the consequence of a hard-gate failure in a Stage-C healthy replicate.** The driver terminates under `UNSAFE_STAGE_C_REPLICATE`, **the driver's name, not a pre-registered one**. **No Technical Report sentence may present that label as a Protocol-P branch.**
59. **[S55] The gate read on the two reused ladder values (0.75, 0.35) is forced to pass and is not coverage.** Only eight of the ten are live.
60. **[S56] The driver-level I13a check is live on the ONSET and on the condition/severity routing, and NOT on the fault's other fields.** **The write-up may say the driver verifies the stamped onset against the trajectory document; it may NOT say the driver independently verifies the constructed fault.**
61. **[S56] The helper's closed-vocabulary check is redundant with the construction layer's.** Kept for fidelity to Correction 1's text. **Do not count it as coverage of the closed-set property.**
62. **[S56] Plan-mode elapsed time is 0.30–0.33 s, measured.** **The 70–80 minute full-run figure IS an extrapolation from one measured rollout and Step 25 labels it as one.** **[S57 SUPERSEDES: the executed run recorded 4,432.16 s inside the executor.]**
63. **[S57] The §7 replay gate certifies the ORDINARY construction path, not the one the screen runs.** It executes `overrides=None`. **No write-up may say the replay gate verified the instrument that produced the screen's numbers** — it verified the shared machinery. Say exactly that.
64. **[S57] The Protocol-P simulator cost was misreported as "one rollout" in eleven consecutive human reports by BOTH agents.** The measured figure is **fifteen pre-run / 151 total**. **Never quote a historical cost figure from a summary — re-derive it from the primary session records.**
65. **[S57, HALF-RETRACTED S58] A uniformly SUB-THRESHOLD screen result and a broken override path are indistinguishable in the output.** Exact NON-EQUALITY of `gate_report.max_abs_gauge_true` survives; **the ORDERING claim is falsified in cells 6 and 7.** The operative check is Codex's post-onset coefficient-vector comparison. **All eight comparisons passed; I re-verified all eight in S58.**
66. **[S58] §9's role-coverage read is not implemented in the driver and never was.** It is supplied by `scripts/analyze_protocol_p_role_coverage.py` at zero rollout cost. **No write-up may present `CASE_B` as the complete §9 outcome without the coverage counts beside it.**
67. **[S58] The measured coverage is dev 0 / pilot 0 / val 1 / test 1**, so the result carries a role-coverage-bounded non-transfer outcome. It establishes **neither success nor hypothesis failure**. **Gate 4 trains structural attribution on dev, which has no testable structural setting at the selected probe.**
68. **[S58] The role-coverage script's OOD-exclusion filter is a NO-OP on the current assignment.** Exercised only by a **constructed** test. **Do not count the real-document test as coverage of that filter.**
69. **[S59] `c48c2e4d…` is the CRLF-rendering raw hash of an LF-tracked document, and both agents quoted it as "the screen result's sha256."** The document digest is **`e800ae6c…`**. **[S60 CONFIRMED by an independent plain-bytes instrument, and by Codex.]** Any future sentence naming the screen result's digest must use `e800ae6c…` or say which rendering it means.
70. **[S59] `compute_role_coverage` can raise a FOREIGN exception type** on a non-finite severity. **No write-up may say the analyzer refuses every malformed document with a named role-coverage error.**
71. **[S59] The role-coverage analyzer is pinned to the CURRENT assignment's shape and will refuse a post-A2 one.** **After A2 the script must be REVISED, not merely re-pointed**, and whoever does that owes the twelve S59 tests a re-check.
72. **[NEW S60] EVERY LADDER VERDICT IS CONDITIONAL ON DISTAL PAYLOAD MASS, AND THE SCREEN COVERED TWO MASSES.** 0.050 kg multiplies the structural distance by 0.4867–0.5366 at every one of the ten rungs while `Q95_c` does not move with payload; the zero-margin crossing sits at remEI 0.60–0.65 unloaded and 0.45–0.50 loaded; the all-cell conjunction is therefore decided by the loaded cells. **Pilot, val and test each reserve at least one payload mass the ladder says nothing about.** No write-up may state a `TESTABLE` verdict without naming the payloads it was established at.
73. **[NEW S60] TWO PAYLOAD LEVELS DETERMINE A RATIO, NOT A CURVE.** No functional form in payload mass is fitted or implied by the S60 artifact, and none may be read into it. **Do not compound 0.506 out to the reserved masses in any document.**
74. **[NEW S60] §9's coverage counts for val and test are DEV-CONTEXT verdicts applied to severities reserved elsewhere.** That is what §9 pre-registers; it is **not** the claim that those severities are testable in their own split's contexts. No write-up may collapse the two.
75. **[NEW S60] `payload_levels`'s two-level and balanced-size checks are FORCED by the §8 mass-equality check and cannot be reached from any document.** Tested by direct call; a third test pins why. **Not coverage of the level contract.**
76. **[NEW S60] `row.payload_id in masses` in the payload read cannot fail** once the duplicate-id check has passed. Arithmetic, not a runtime check. Survives the sweep by design and is documented in the code.
77. **[NEW S60] THE MUTATION-SWEEP HARNESS PRODUCED FALSE VERDICTS IN BOTH DIRECTIONS** at sub-second per-case cost, via stale bytecode (whole-second mtime + identical mutant size). **Any sweep result quoted from S58 or S59 was produced by the defective harness.** The role-coverage analyzer was re-swept clean in S60 (28/28) and the payload read in S61 (65/66); **nothing else has been re-checked.**
78. **[NEW S61] THREE RAISE SITES EMITTED ONE SENTENCE, AND ONE OF THEM BUILT IT WITH AN F-STRING.** `require_binary_context_factors`'s `f"…context_profiles.{factor} list"` renders the payload readers' literal exactly. **A duplicated refusal message is not findable by searching the source**; it is found by a runtime comparison of the sentences the sites emit, or by a mutation sweep. Fixed in the payload read; **the same pattern is not yet audited anywhere else in the packet**, and `{factor}`-style messages exist in other modules.
79. **[NEW S61] THE PAYLOAD READ REFUSES A LEGITIMATE §9 SHAPE.** A ladder row with `hard_gates_passed: false` / `verdict: UNSAFE_LADDER_VALUE` / `margin: null` is what the driver writes for an unsafe value, and the screen continues. This analyzer refuses such an artifact — correctly, since a cell with no margin has no place in an attenuation ratio — but **no write-up may say it covers every non-terminal §9 outcome.**
80. **[NEW S61] `47ec3571…` IS THE PAYLOAD ARTIFACT'S LF DOCUMENT DIGEST, NOT WHAT A CHECKOUT PRODUCES.** Measured with `git checkout-index` into a clean tree: a fresh checkout on this machine renders 8,809 bytes / 268 CRLF pairs / `0beb9afc…`. `role_coverage.json` renders `ea474c75…`. Both paths are `text: unspecified` with `core.autocrlf=true`, so the LF bytes exist because the analyzer wrote them, not because git will reproduce them. **Third file in three sessions to hit this. Qualify every digest of a tracked results JSON.**
81. **[NEW S61] THE ONE-CELL-PER-MASS MEASUREMENT I COSTED IN S60 CANNOT LOCATE A BOUNDARY**, and my "five unscreened masses" was six. Both errors are recorded in the extension's own cost section so the corrected numbers are not left to be reconstructed. **Never carry the S60 figures forward.**
82. **[NEW S62] THE PLANT HAS NO GRAVITY, SO DISTAL PAYLOAD IS TIP INERTIA AND NOT A LOAD.** `cable_mechanics.py:101` emits `gravity="0 0 0"`; `opt.gravity` is the zero vector and `qfrc_bias` is zero. Stepped at `ctrl=0` for 3.0 s, **every one of the eight declared masses deforms exactly zero and holds tip radius 0.80000 m**, 0.200 kg included. **No document may describe a payload as hanging, loading, sagging, or consuming the A1 strain envelope at rest** — my own S61 phrasing did and is withdrawn. Whatever the S60 attenuation is, it is not a static-preload effect.
83. **[NEW S62] THE DIAGNOSTIC PROBE SITS ~97x BELOW THE LOWEST ELASTIC MODE, SO RESONANCE IS NOT THE MECHANISM.** Linearized undamped estimate: f1 = 77.34 Hz against a 0.8 Hz probe, and **f1, f3 and f5 do not move with payload at all**; only f2/f4/f6 move, and they saturate (f2 −21% over 0.000→0.050 kg, a further −5% over 0.050→0.200 kg). The estimate omits the elbow `connect` constraint, which can only raise frequencies and is therefore conservative **for that one conclusion and no other**. **The mechanism of the payload attenuation is UNIDENTIFIED.** Do not let a plausible mechanism enter a write-up unmeasured.
84. **[NEW S62] `PhysicalKey` CARRIES NO PAYLOAD MASS.** `(sensor_seed, pair_id, condition, severity, probe_peak_force_n, probe_ramp_fraction_of_duration)` — harmless in Protocol P, where identity distinguishes the bodies, and **a silent reuse bug the moment any design shares identity across bodies**. The results layer keys rollout *reuse* on this object. Any future design that holds identity fixed while varying the body owes this key an additive field first.

## Coherence / honesty bounds (keep loud)

- **Sensor RNG keyed on `(sensor_seed, pair_id, channel, stream)` jointly** (`utils/rng.py:76-78`). **Measured S39: a `pair_id` change alone moves `gauge_obs` by up to 6.50 µε**, against `D` of order 0.1–0.5. **Nothing else is in the key.**
- Deployable floors are *detection*, not learned attribution; abstention untestable on this fault library; **every joint-space control number comes from a condition where the structural fault causes no measurable JOINT deficit.**
- **A noise threshold is a property of the SENSOR MODEL, the window LENGTH, the window ORIGIN, the aggregation, the path, the operation, the construction, the identity, the fault's activation step, and — S60 — the CONTEXT POPULATION, of which payload mass is the dominant factor. The SIGNAL it is compared against depends on excitation, task, plant and payload.** Never quote a µε number without naming all of these.

## Constraints / environment / ops (load-bearing)

- **Simulation-only, one desktop:** Windows 11, Ryzen 7 8700F (8C/16T), RTX 5060 Ti **16 GB VRAM** (sm_120), 32 GB RAM, Python **3.12.10** in `./venv`. Free/OSS, commercial-use-friendly only.
- **venv has:** numpy 2.5.1, scipy 1.18.0, scikit-learn 1.9.0, matplotlib 3.11.0, mujoco 3.10.0, pandas 3.0.3, control 0.10.2, gymnasium 1.3.0, pytest 9.1.1, **torch 2.11.0+cu128**. **No new dependency was added in S46–S61.**
- **Running packet tests:** from the REPO ROOT, `./venv/Scripts/python.exe -m pytest -q "Reproducibility Packet/tests"`. **Scope pytest to that path** — a root-wide invocation collides on duplicate test module names in the ignored `tmp/session6_packet_copy/`. **Full suite 1,126 tests green (re-run S62, 111.94 s, NO code changed that session; S61 137.87 s; `test_protocol_p_payload_conditioning.py` collects 105 after Codex's 8 S60 additions and my 11 S61 additions, and 1,021 + 105 = 1,126 exactly).** Prior: 1,126 (Codex S61), 1,115 (Codex S60), 1,107 (my S60, 150.54 s), 1,021 (S59, 143.00 s), 999 (S58), 975 (S57), 938 (S55), 906 (S54), 750 (S53), 595 (pre-S51 baseline). **Set `PYTHONIOENCODING=utf-8` for anything that prints non-ASCII** — the console is cp1252. **Use ASCII in probe scripts and in anything a gate prints.**
- **MUTATION SWEEPS — MANDATORY HARNESS SHAPE AFTER S60:** clear `__pycache__` before every run **and** set `PYTHONDONTWRITEBYTECODE=1` in the subprocess env; drop `-x`; translate anchors to the target file's own newline; report bad anchors separately from survivors; restore exact bytes in a `finally` and verify the blob afterwards. **Run the whole sweep twice and require identical results** — that is the cheapest detector for a harness fault.
- **Packet scripts are invoked FROM the packet directory** (`scripts\<name>.py`, `--output-dir results\<name>`), per its README. From the packet dir the project venv is `..\venv\Scripts\python.exe`. **In my PowerShell tool the working directory is not the repo root — use `Set-Location` or absolute paths. My Bash tool's cwd PERSISTS between calls — prefer absolute paths or re-`cd` every time.**
- **Timings (measured S35–S60):** full packet suite ~150 s; one MuJoCo rollout (3000 steps) **25.6–27.5 s**; a PARTIAL rollout is proportionally cheap — 480 steps ≈ 3.0 s; at reduced fidelity (`point_count=9`, `simulation_timestep_s=2e-4`) 501 control steps ≈ 0.37 s; a 200-realization sensor-only null at W=768 ~40 s; an offline re-observation ≈ instantaneous; the driver's `--mode plan` 0.30–0.33 s; **one driver-file mutation case ≈ 100 s** (a 17-case sweep is ~28 min and belongs in the background); **a small-analyzer mutation case ≈ 0.5–0.7 s with the fixed harness, so a 44-case sweep is under a minute.** **NO figure exists for the pinned `pairs=100` Stage-0 run — see limitation 45; do not invent one.**
- **Background jobs:** `run_in_background: true` and wait for the notification. **Python buffers stdout when redirected — use `flush=True` in the job and poll the file it writes, not a pipe.**
- **PowerShell 5.1** primary (no ternary/`??`; **`^` is not a continuation**); Bash tool also available. **`bc` and `/usr/bin/time` do NOT exist in the Bash tool** — time a subprocess from Python with `time.perf_counter()`. Use `git diff --numstat` to confirm `+N/−0` after every chat turn. **A bash heredoc (`<<'PY'`) is the reliable way to run a multi-line Python script from the Bash tool; inline `-c` with `chr()`/byte literals is where I make syntax errors.**
- **Root `.gitignore`** covers `venv/`, `/data/`, `tmp/`, `MUJOCO_LOG.TXT`, caches, model files, LaTeX aux, OS/IDE noise, and the three session locks (`.claude-session.lock`, `.codex-session.lock`, **`.agent-session.lock`** — the scheduled-task runner creates the last one at the repo root). **Root `.gitattributes`** pins `schema.json`, the assignment JSON, and **`Reproducibility?Packet/protocol/*.md`** to LF. **Packet `.gitignore`** ignores `*.npz` + caches/logs (so `results/*.json` and `*.md` ARE tracked). **Verified again S61; no change needed. The scheduled-task runner's `.agent-session.lock` is ignored and must be deleted at session end.**

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
13. **(S36) When a choice you must make favours you, measure how much, say so, and hand the decision to the reviewer.** *(Applied twelve times now.)*
14. **(S36) A pre-registered protocol must be executable by someone who did not write it.** **The act of making it executable is itself the defect-finding technique.**
15. **(S36) The cleanest statement of a negative is often a comparison you have not made yet.**
16. **(S37) Match the null to the OPERATION, not just to the configuration.**
17. **(S37) Compute the closed-form consequences of every gate you approve, before it costs anything.** **Check boundary cases for `<` vs `<=`.**
18. **(S37) When the most likely branch creates a design problem, force the decision BEFORE the measurement that would make any fix look chosen.**
19. **(S38) When you import a convention, import the CONFIGURATION THAT MAKES IT TRUE.** The chain: window length → aggregation → operation → time origin → construction path → realized identity → fault activation step → file byte-domain → the name an expression binds → the denominator → the fixture size → the scope a correction claims → **the context population (S60)**.
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
35. **(S44) Unit-testing both ends of a wire does not test the wire.**
36. **(S44) Injecting defects into your own finished patch is cheap and it is not optional.**
37. **(S44) Deleting a vacuously-passing test is a contribution, not a gap.** **Ask of every new green test: what exact state would make this red?**
38. **(S44) Extending a stated principle to an unenumerated case is still a deviation — lead with it.**
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
56. **(S49) Approval is an ACT, not a state you drift into.** Post it as its own turn, naming the exact blob. **(S60: Codex enforced this against my own handoff and was right to.)**
57. **(S50) A correction is an artifact and inherits every failure mode an artifact has.**
58. **(S50) A documentation claim about a dependency is a measurable claim.** *(S56: any claim about what a program writes is settled by running it and reading the file.)*
59. **(S51) A test that matches on a LABEL certifies a guard it may no longer exercise.** **Match a phrase unique to ONE raise site.** *(Sharpened S56: when you add a guard that duplicates an existing one, its MESSAGE is the thing most likely to be non-distinguishing. **S60 instance: my new binary-factor check emitted the SAME sentence as an existing guard; I changed one so a reason assertion can tell them apart, and pinned the distinction in a test.**)*
60. **(S51) A mutation that survives a focused sweep is not yet a gap — re-run it against the full suite before calling it one.**
61. **(S52) Test per BRANCH, not per guard.**
62. **(S52) A guard that refuses everything is not a guard — test the ACCEPT side against the real inputs.**
63. **(S52) Two mutually redundant call sites of one guard are individually untestable.** **Sweep the DOUBLE removal.**
64. **(S52) When the reviewer's repair is itself an artifact, sweep it the way you sweep your own.**
65. **(S53) A status clause that has been true for several consecutive entries is the most likely thing to be carried into one where it is false.**
66. **(S53) Build the WHOLE plan once, before building the thing that executes it.**
67. **(S54) A test can verify a property of the LANGUAGE and look like it verifies a property of your code.**
68. **(S54) A count pinned as a literal can only audit the one plan it was written for.**
69. **(S55) A reviewer's finding reached by READING is not the same evidence as one reached by RUNNING.** **When you reproduce a finding, first prove your instrument reached the thing it claims to have broken.**
70. **(S55) Measuring a check and discarding its result is indistinguishable, in the finished record, from never having run it.**
71. **(S56) A comparison whose two sides come from the same function and the same arguments is a report of a check, not a check.** **For every check, name the two sources and confirm they are actually different.**
72. **(S56) A finished artifact should be read as a stranger would read it.** **Before handing over anything that writes an artifact, open the artifact.**
73. **(S57) A claim about the project's HISTORY is never re-measured, because both parties treat it as a fact rather than as a measurement.** **Treat "both agents have said this for many sessions" as evidence that NOBODY has checked it.**
74. **(S57) A positive control must exercise the path the measurement uses, not a neighbouring one.** **When the broken-instrument outcome and the scientific null produce the same output, the discriminator has to be designed in before the run.**
75. **(S58) NOBODY EVER CHECKED THE SPECIFICATION FOR OUTPUTS THAT WERE NEVER BUILT.** **Before executing a pre-registered protocol, walk its section headings and name, for each one, the artifact field or code path that discharges it.** **The mutation sweep cannot see this class at all.**
76. **(S58) When auditing a total, re-derive the NONZERO entries.** **An audit that samples where you expect to find nothing is a measurement of your expectations.**
77. **(S58) A test written against the real committed document may be asserting a property of the DOCUMENT, not of your code.** **[S60: recurred — deleting a `sort` survived because the committed ladder is already ordered. Ask what exact state would make it red, then CONSTRUCT that state.]**
78. **(S58) Verify your own instrument before reporting a discrepancy, especially a large and consistent one.**
79. **(S59) A REVIEWER'S REPAIR ARRIVES WITH THE AUTHORITY OF HAVING BEEN RIGHT, AND THAT IS EXACTLY WHY IT NEEDS THE FULL SWEEP.** **When you have just been shown to be wrong, that is the moment your review of the correction is weakest.**
80. **(S59) A GUARD ADDED DURING REVIEW IS THE LEAST LIKELY GUARD IN THE CODEBASE TO HAVE A TEST THAT CAN FAIL.** **A check whose input space has three branches and whose real data sits in the middle one has both ends dead by default.**
81. **(S59) A HASH IS ONLY PROVENANCE IF IT IDENTIFIES THE DOCUMENT RATHER THAN THE COPY.** **Before recording a digest, ask what would have to change for it to change, and check that the answer is "the content" and not "the machine."**
82. **(NEW S60) THE INSTRUMENT THAT CERTIFIES YOUR OTHER INSTRUMENTS IS THE ONE NOBODY AUDITS.** The mutation sweep is the tool both agents use to decide whether a guard is real, and it had a silent failure mode for nine sessions. It surfaced only because the same file gave three different survivor sets — and my first instinct was to pick the answer that appeared most often rather than to ask why they differed. **The move: when a measurement is not reproducible, the non-reproducibility IS the finding; stop and characterise the instrument before using any of its outputs.** Its companion: **run every sweep twice and require identical results** — that is a one-line detector for the whole class, and it costs nothing.
83. **(NEW S60) A VERDICT AGGREGATED OVER CELLS IS A STATEMENT ABOUT THOSE CELLS, AND THE CELLS ARE USUALLY NOT A RANDOM SAMPLE OF ANYTHING.** The screen's conjunction over four development context cells reads like a robustness guarantee — "it holds in every cell" — and it is in fact a statement conditional on the two payload masses those cells happen to carry, which are the two lightest in the project. **Ask of every aggregated verdict: what population were the units drawn from, and is it the population the claim will be applied to?** Its companion, and the reason this one was free: **the contrast that answers it was already inside a completed, paid-for experiment** — a balanced factor nobody had read, because the design document called those cells "replicates."
84. **(NEW S60) FIXING AN ERROR BY REORDERING BEATS FIXING IT BY CATCHING.** A malformed document reached another module and died there with a foreign exception type. Wrapping it in a `try` would have produced the right exception class and the wrong sentence. Validating earlier produced a message that names the document and the field. **When a foreign exception escapes your contract, ask what you could have checked before calling out, not what you could catch after.**
85. **(NEW S61) A DUPLICATED MESSAGE CAN BE INVISIBLE TO THE ONLY TOOL YOU WOULD USE TO LOOK FOR IT.** I have applied Lesson 59 — assert a phrase unique to one raise site — by searching the file for the literal. That works only while every copy is a literal. One copy assembled with an f-string over a variable defeats the search completely, and it defeated it in a file I had audited the session before while writing a docstring claiming the messages were distinct. **The move: compare the sentences the sites actually emit at runtime, in a test, and let the mutation sweep tell you when two guards are covering for each other.** The general form: *a property of the rendered output cannot be verified by reading the source that renders it.*
86. **(NEW S61) A TYPE CHECK NEXT TO A TRUTH CHECK IS NOT REDUNDANT, AND IT IS THE ONE THAT WILL BE UNTESTED.** `isinstance(x, bool)` followed by `require(x)` looks like belt and braces; it is not, because every truthy non-boolean — the string `"false"` most of all — passes the second and only the first can stop it. The guard was added during review, which per Lesson 80 is exactly where an untestable guard is most likely to live. **Ask of every pair of adjacent guards: what input does the FIRST one alone reject? If the answer is "nothing", delete it. If it is "something dangerous", it needs its own test, and probably does not have one.**
87. **(NEW S61) READING A LINE NUMBER IS NOT READING THE LINE.** My first characterisation pass labelled two survivors by inferring which guards those line numbers were, and got both wrong; the outcome class happened to be right, which is how the mislabelling nearly survived. It surfaced only because I went back to print the actual source lines. **An instrument that reports a location has discharged half its job; the other half is yours.**
88. **(NEW S62) A CONTROL THAT VARIES THE THING IT CONTROLS FOR IS NOT A CONTROL.** I wrote a tripwire requiring seven measurements to be pairwise distinct as evidence that a setting had reached the simulator — and gave each of the seven its own random identity, which makes them distinct for free. The check passes in exactly the state it exists to catch. Codex found it by reading the design; I would have found it only by running a dead override, which nobody was going to do. **The move: for every guard, name the failure it exists to catch, then ask what ELSE in the design produces the passing signal. If anything does, the guard is decorative.** Its companion, and the fix here: **common random numbers turn a decorative check into a real one** — hold the identity fixed and a dead setting produces *identical* output, which is refusable.
89. **(NEW S62) FIXING THE SCIENCE CAN BREAK A KEY SOMEWHERE ELSE, AND THE BREAK IS SILENT.** Making identities common across payload masses was the right scientific fix and it immediately collapsed the results layer's physical key, because that key distinguished bodies *by identity* and nothing else. The consequence would have been one simulation silently reused as another's row — no error, no failing test, a plausible number. **The move: after changing what a design holds fixed, re-ask what every downstream key, join, cache, and dedup was actually distinguishing. A key is a claim about what makes two things different, and changing the design changes that claim.** Also: **state the tolerance-free rule when you can.** I replaced "non-monotone beyond what the null admits" with set inclusion rather than invent a threshold — a threshold in a *classifying* rule invites the argument that it was chosen to produce the outcome, and the same information survives as a diagnostic that classifies nothing.

## Pointers

- **Protocol P (in force, JOINTLY APPROVED): `Reproducibility Packet/protocol/protocol-p-v2.3.3.md`, canonical sha256 `5689dad7…8bdf421f`. READ THE FILE.**
- **The payload-boundary extension (DRAFT, UNDER REVIEW, NOT EXECUTABLE): `Reproducibility Packet/protocol/payload-boundary-extension-v0.2.md`, canonical sha256 `e734c498…469932e9`, blob `c7facc13`, 60,815 bytes, LF, raw == canonical. READ THE FILE — the summary blocks above are an index, not the document. v0.1 (`32a03930…`, blob `903962f8`) is SUPERSEDED and BLOCKED; its bytes are in the `Claude Session 61` commit. Do not approve, cite, or build from v0.1.**
- **The replay gate: `scripts/protocol_p_replay_gate.py` + `tests/test_protocol_p_replay_gate.py` (36 tests).** Run from the packet dir: `..\venv\Scripts\python.exe scripts\protocol_p_replay_gate.py --data-root ..\data\gate3-base-dev-pilot-val-c1-s`. **EXECUTED EIGHT TIMES; not run S52–S60. IT CERTIFIES `overrides=None` ONLY (limitation 63).**
- **Stage 0: `scripts/analyze_synchronous_difference_null.py` (blob `f104971d…`) + `tests/test_synchronous_difference_null.py` (99).** Pre-registered invocation from the packet dir: `..\venv\Scripts\python.exe scripts\analyze_synchronous_difference_null.py --window 768 --f-ctrl-hz 500.0 --diagnostic-hz 0.8 --thermal-ramp-c 3.0 --pairs 100 --seed 0 --pair-id 1`. **It has been spent; re-running it is NOT authorized.**
- **The Stage-0 artifact — JOINTLY APPROVED. Tracked. DO NOT EDIT, DO NOT RE-EXECUTE.** `results/protocol_p/sensor_only_difference_null.json`, blob `31c1e6d1824c10bd5978d12c377f76cf556af03f`. **`samples` is a 6-key metadata dict; the 100 values are `samples["distances"]`. There is no top-level `authority` — the path is `corroboration.authority`.**
- **THE STAGE-A/B/C PROGRAM — ALL FOUR FILES JOINTLY APPROVED AND EXECUTED.**
```text
JOINTLY APPROVED, CURRENT:
  scripts/utils/protocol_p_results.py  e84e5f9f4e6d10408873d87b81b2baef9535d50e  40,090 B
  tests/test_protocol_p_results.py     cbac30ed3d41c961f7d5c54c306c8a09fa1be1cd  77 collected
  scripts/run_protocol_p_screen.py     7668793e147a2776cb003ea90c79e76247d9b4de
  tests/test_protocol_p_driver.py      23222d0ed03c26f57cfff5f53267ca8186a8d31a  148 collected
  scripts/analyze_protocol_p_role_coverage.py  f911f2f38a4917cc898abf6c0d2a063cfce33842
  tests/test_protocol_p_role_coverage.py       83c7d6403d218be6d073a39b603ebf73afb45186  46
  results/protocol_p/role_coverage.json        6d6d23b9a42baaf81ec558fd21c6bc1148aa6890
`--mode execute` HAS BEEN RUN ONCE (Codex S57).  DO NOT RUN IT AGAIN without a new
  joint decision: it costs 135 rollouts and the result is approved.
JOINTLY APPROVED (Codex S60, me S61) — DO NOT REGENERATE TO A DIFFERENT STATE:
  results/protocol_p/payload_conditioning.json  c11f70673b043ea634481d47ad4137365c0cd12e
    canonical sha256 47ec3571bf207f428c1eb376cfdf7b3f673a94729fa649ba845bca27299d97d1
    (a FRESH CHECKOUT renders 0beb9afc…, 8,809 B, 268 CRLF — limitation 80)
UNDER REVIEW (S61, mine — Codex owns the turn):
  scripts/analyze_protocol_p_payload_conditioning.py  39048d2658963a345e3a46949a6070d421a155d9
  tests/test_protocol_p_payload_conditioning.py       b9e81f6320e1a3b68f952d631795f1d82abca5ff  105
Run either read from the packet dir; zero rollouts, ~0.3 s each:
  ..\venv\Scripts\python.exe scripts\analyze_protocol_p_<name>.py `
    --screen-result results\protocol_p\stage_abc_screen.json `
    --assignment config\proposed-gate3-assignment-v0.1.json --output-dir results\protocol_p
```
- **`agents/Claude/Progress Reports/Progress Report Session 56.md` — LOOP CLOSED AT ROUND FIVE, blob `83c527c…`. Do not reopen.** Covers S49–S56. Its headline — that sixteen sessions produced no measurement of the central question — is overtaken by events: the measurement ran in Codex's S57. `Progress Report Session 48.md` remains jointly approved at blob `f01aa7d7…`.
- **The seam (APPROVED, Codex S44): `ScreenOverrides` in `scripts/utils/assignment_generator.py`, blob `1c565888…`, and its tests, blob `2ec96c9f…`.** Read spec §3 beside them.
- **The I13b guard: `tests/test_cable_plant_softening_boundary.py`** — 6 tests, co-owned, approved in place by Codex (S43). **The driver NAMES it as a precondition it does not itself run.**
- Claim Sheet (in-force contract): `Claim Sheet.md` · plain-language: `Accessible Claim Sheet.md` · Study Guide Pass 1: `Study Guide/Pass 1 - Conceptual Foundation.tex`
- **Shared schema (in force, +A1):** prose `Reproducibility Packet/schema/schema-v1.0.md`; machine `schema.json`.
- **The freeze plan:** `agents/Codex/Config Freeze Readiness Review.md`.
- **The probe-amplitude record:** `results/synchronous_safe_probe/synchronous_safe_probe_report.md` — **read S35 Findings A–C, S36 D, S37 F, S38 J, S39 K/L beside it.**
- **The detection-floor record:** `results/synchronous_detection_floor/summary.json` — sha256 `4937e885…c2c67`; **re-verify after any edit to `utils/gauge_windows.py`.**
- **CONCLUDED director chat:** `chats/Claude-Codex-Human/Better Suited Task/…- Concluded.md` — the withdrawn task-redesign directive. **A2 must stay clear of it.**
- Director requests: `director_requests.md` (root) — entry 1 (Claim Sheet review) non-blocking, **still awaiting director reply**. Nothing else is blocked on the director.
- My foundation `agents/Claude/Literature Foundation.md` · ledger `agents/Claude/references.md` (**no S20–S60 entries — reproduction/construction/measurement/review sessions, no external sources read**).
- **Live-Run README (co-maintained): root `README.md` — Phase 2 / In Progress, banner 2026-08-02. My S62 appended ONE new entry (`+2/−0`) at the END of the log, edited no dated entry, and left the banner (same day; S61 did the same).** It reports the v0.2 rewrite in plain language — the identity confound and why the safety check could not have caught a dead setting, the results-table key that does not track payload, the zero-gravity fact (the payload is inertia, not a weight), the probe sitting ~100x below the arm's slowest vibration and what that rules out, and the control test that had been asking a measurement to reproduce noise. **The log's date order is out of chronological order in the middle and Codex's dated correction says so; dated entries are never edited, so it stays that way.** **Beware when appending: `README.md` is all-CRLF; split on `b"
"`, insert before the `''/'---'/''` block that precedes `## Follow along`, and verify by reading the neighbouring lines back rather than trusting an offset.**
- **Phase-2 chat:** `chats/Claude-Codex/Phase 2 Integration and Config Freeze/…- Active.md` — **NOW 15,918 lines. My S62 turn is at byte 1,059,356, `+256/−0`, header unique, physically last. CODEX OWNS THE NEXT TURN: the payload-boundary extension v0.2 (canonical `e734c498…`, blob `c7facc13`) and nothing else — the analyzer/tests loop is CLOSED.** The four things I explicitly asked Codex to judge: the CRN cost statement (§5), the `PhysicalKey` prerequisite against its own approved module (§3.2), the permissive per-mass exclusion rule (§9.6), and whether the nine-rung anchor is right or it wants the strict bracket back (§9.3). Do NOT re-ask the plan default, the Stage-0 imports, the Stage-C label, the vocabulary guard, Step 25, the readback ruling, the screen result, the role-coverage states, `.gitattributes`, the measure-first ruling, or the payload analyzer/tests; all eleven are settled. **The file is MIXED-EOL** — Codex appends LF, the older bulk is CRLF; append LF and verify `+N/−0` rather than assuming.
- **Monitoring chat:** `chats/Claude-Codex-Human/Transcript Order Monitoring/…- Active.md` (88 lines; unchanged S43–S62 — no recurrence; **streak twenty-nine**: my S62 append passed all four gates — pre-write prefix retained byte-for-byte (asserted inside the writer, not inspected afterwards), header unique, physically last, `+256/−0`). The duty is to flag recurrences, so a clean session adds no note; verify at the git level regardless.

## Scratchpad (S62, NOT committed)

`probe_s62_sag.py` — compiles a plant per declared mass, steps it at `ctrl=0` for 3.0 s,
reports peak/final |gauge_true| and tip radius. **This is the instrument that found the
zero-gravity fact, and it found it by FAILING to measure what I expected.** Reusable
whenever a claim about static loading needs checking.
`probe_s62_modes2.py` — the linearized modal estimate. `mj_fullM(model, data, dst)` in
MuJoCo 3.x (NOT `(model, dst, qM)`), K by central differences of `qfrc_passive` under
`mj_integratePos`, then `scipy.linalg.eigh(K, M)`. **`jnt_stiffness` is all zero here —
the cable's elasticity is a PLUGIN**, which is why the naive version returns nothing.
`append_s62.py` — the chat appender, asserting the pre-write prefix inside the writer.
`readme_entry_s62.py` — inserts one root-README log entry before the `''/'---'` block,
asserting the anchor lines before writing and reading the neighbours back afterwards.
`turn_s62.md`.

## Scratchpad (S61, superseded)

`audit_s61.py` — stdlib-only, imports NOTHING from the analyzer under review; re-derives
every relation Codex's guards check, with `==` rather than `isclose`, and derives
cell->payload from the screen's OWN `rollout_canonical` reservations joined to the
assignment's cell table. *The general move: to check a reviewer's checker, build a
checker that shares no code with either the producer or the reviewer.*
`sweep_s61.py` — the corrected harness, 66 sites, **two passes required to agree**, blob
verified after each pass. Reusable against any packet module; point it at a target and a
focused test file.
`probe_s61_survivors.py` — **the instrument worth rebuilding.** For each survivor it
builds the state the guard exists to refuse and runs it through the committed module AND
a copy with that one guard neutralised, printing both outcomes. That pair of outcomes is
what separates REDUNDANT from REAL GAP from FOREIGN EXCEPTION — a survivor list alone
cannot. Each variant goes to a uniquely named file, which sidesteps the S60 bytecode
mechanism entirely rather than working around it.
`turn_s61.md`.

## Scratchpad (S60, superseded)

`verify_s60_mutations.py` — 44 cases over the payload read with the S59 newline
translation plus the S60 bytecode fix.
`resweep_s59_role_coverage.py` — 28 cases over the **jointly approved** role-coverage
analyzer, 28/28 caught. *The general move: when you find a fault in a verification tool,
re-run the verifications that tool already blessed.*

## Scratchpad (S59, superseded)

`probe_s59_findings.py` — loads the pre-review analyzer from a git blob and the current one
from the packet, then drives each constructed bad state through BOTH in one process and
prints the two verdicts side by side. *To confirm a reviewer's finding, make the OLD code's
acceptance and the NEW code's refusal appear in the same output.* Runs each assignment
mutation twice, stale-hash and resealed, because the guard under test is unreachable until
the mutation is internally consistent.

## Scratchpad (S58/S57, superseded, kept for the instrument notes)

`audit_s58.py` — recomputes the ENTIRE screen result from the artifact and the assignment
ALONE, importing neither the driver nor the results layer. *To check a producer's output,
build a checker that shares no code with the producer.*
`probe_s57_stamps.py` — runs `driver.run_screen` end to end with `StubExecutor` **imported
from `tests/test_protocol_p_driver.py`** rather than reimplemented. Zero rollouts, 34.4 s.
*Importing the stub from the approved test file is what stops the probe from being a second
implementation that agrees with itself.* Gotchas: the ledger entry key is
`rollout_provenance`, not `provenance_hash`; `run_screen` needs `candidates=admissible_candidates()`
in full or the census refuses.
`append_turn.py` (sha256 `3cf26db962bf3accb97880d1343fe791129f3790db1d70b68fd58a552d26fa2d`)
— the chat appender, copied forward unchanged for many sessions.
