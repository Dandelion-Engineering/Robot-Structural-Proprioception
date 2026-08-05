# Summary of Only Necessary Context — Claude

*Rewritten every session. Restores my working context for the next session. Excludes anything already in `Project Details/Project Details.md` and `AgentPrompt.md` (I re-read those in full at session start). Last rewritten: end of Session 75, 2026-08-04.*

## S76 FIRST — A2 IS WRITTEN AND WITH CODEX. THE ONE THING I OWE IS COMING BACK TO IT.

```text
*** THE ONLY OPEN STATE IS THE A2 TWO-FILE REVIEW LOOP, AND CODEX OWNS THE NEXT TURN. ***
  Claim Sheet.md              blob d4c2fea2b64de359be536908c52331edc3d673af   +146/-0
  Accessible Claim Sheet.md   blob 5bd4a93dfcb2bba1e803d885a7cb813dfec2067b   +103/-0
  SUPERSEDED, do not review: 7206bb77… / 75fedf70…  (two late A2.1 narrowing edits;
  I appended a blob-correction turn rather than leave a handoff naming dead bytes)
  Both are PURE INSERTIONS.  Nothing above Slot 15 in either file was rewritten.
  Blobs are `git hash-object` (LF-normalized); NEITHER FILE IS eol-PINNED, so the
  working tree is CRLF and the blob is LF — quote the blob, never a raw byte count.

  I handed these off with MY EXPLICIT OWNER APPROVAL in my S75 chat turn.
  *** A2 IS NOT IN FORCE.  Both agents must approve the SAME BYTES OF BOTH FILES. ***

IF CODEX EDITED: RE-OPEN BOTH FILES AND GENUINELY RE-REVIEW BOTH THE FEEDBACK AND THE
  EDITS, then approve or edit-and-hand-back with explicit approval.  The review-cycle
  playbook names "the owner never comes back" as the failure mode, and this is the turn
  where it would happen.  Accepting a diagnosis but not its implementation is a REAL
  disagreement — say so, do not swallow it.
IF CODEX APPROVED THE SAME BYTES: A2 IS IN FORCE, and TWO THINGS FIRE IN THAT SESSION:
  (1) a Live-Run README entry — the first one that can say the contract changed; it owes
      the reader BOTH halves, that it changed and that NOT ONE BAR MOVED.
  (2) a PROGRESS REPORT.  An approved Claim-Sheet amendment is a trigger regardless of
      the per-agent count, and it does not reset the counter.  (Next regular: S80.)

TWO PLACES I ASKED CODEX TO PUSH ON — THEY ARE THE ONLY JUDGMENTS IN A2:
  1 THE 0/0/0/0 RECOUNT (A2.1 point 3).  New inference, not a transcription.
  2 THE NO-REGENERATION CORRECTION (A2.3).  It tells a future reader the OPPOSITE of
    what both continuity files have said since S33.  If Codex knows an assignment- or
    config-side reason Option C does oblige regeneration, this is where it says so.
  Neither is a settled point being re-litigated, so the escalation trigger is NOT live.
  It becomes live if either runs past about two round-trips.

CLOSED AND SETTLED — do not reopen any of these:
  the role-coverage four-file loop, the .gitattributes ruling, MEASURE FIRST,
  the payload-conditioning result artifact / both READMEs / analyzer + 105 tests,
  my Session-64 progress report (Codex approved b0ff7496 in its S65),
  the S67 authorization-gate question (Codex ruled in its S67; I took it in my S68),
  the scheme whitelist and its NAMES (settled S70/S71 — reopening ESCALATES),
  ALL THREE STEP-2 PREREQUISITES (jointly approved; the eight-round loop is closed),
  THE OPTION-C DIRECTION ITSELF (both agents named it in our S74 turns — A2 is the
    WRITING of a settled decision; six earlier A2 versions were blocked and the
    instinct to reopen the option choice is a trap),
  *** THE EXTENSION DOCUMENT — canonical 538ae06b…, blob d9f6e188, FROZEN ***
      Reproducibility Packet/protocol/payload-boundary-extension-v0.2.md
  *** STEP 3 — both agents read and approved the SAME plan bytes ***
      results/payload_boundary_extension/plan.json
      canonical 15298da4c7a903bf4b62a79eb384abe1f53182972dff41c6e1387dc0ce030be3
  *** STEP 4 — THE JOINT EXECUTION AUTHORIZATION WAS ISSUED AND IS NOW SPENT. ***
      I issued my half in S73; CODEX ISSUED A MATCHING HALF IN ITS S73, same scope.
  *** STEP 5 — RAN ONCE, IN CODEX'S S73.  IT IS SPENT.  §13 says "Once."
      A SECOND INVOCATION OF ANY KIND NEEDS A NEW JOINT AUTHORIZATION, NOT A RETRY. ***
  *** THE RESULT ARTIFACT — BOTH AGENTS APPROVED THE SAME BYTES.  LOOP CLOSED. ***
      results/payload_boundary_extension/payload_boundary.json
      canonical 7746372f1adea931722cf547adee36489971493c4e1b5217f588d4c6d1c9aa04
      raw == canonical, 388,550 bytes, 0 LF 0 CR
      Codex approved it in its S73 (its own reconstruction).  I APPROVED THE SAME BYTES
      IN MY S74 after 130 independent checks.  DO NOT RE-AUDIT THE ARITHMETIC.
      I RE-HASHED IT AGAIN AT THE END OF S75: unchanged.

THE RESULT — TAKE IT FROM HERE, IT IS RE-DERIVED FROM THE ARTIFACT, NOT REMEMBERED:
  outcome X_CASE_EMPTY (R10) | mass_coverage COMPLETE | anchor X_ANCHOR_PASS
  replay PASS 1 rollout | extension 126 | total 127 | 3,680.708815 s | 0 exclusions
    mass    split  own severities  TESTABLE                 role_retained
    0.025   pilot  {0.60, 0.85}    0.35 0.40 0.45 0.50      false
    0.050   dev    {0.50, 0.75}    0.35 0.40 0.45           false   <- anchor
    0.075   pilot  {0.60, 0.85}    0.35 0.40                false
    0.100   val    {0.40, 0.90}    0.35                     false
    0.125   val    {0.40, 0.90}    0.35                     false
    0.150   test   {0.35, 0.65}    (empty)                  false
    0.200   test   {0.35, 0.65}    (empty)                  false
  option_b_cap_kg null.  MONOTONE over all 21 pairs; PREFIX at all 7.
```

## WHAT A2 SAYS, SO THE NEXT SESSION DOES NOT RE-DERIVE IT

**Read the amendment itself — `Claim Sheet.md` → `# Amendments` → `## Amendment A2`. This
is an index, not a substitute.** Both files gained an `# Amendments` section after Slot 15
with a numbering note (**A1 amended the SCHEMA, not this sheet, and is recorded in place at
`Reproducibility Packet/schema/schema-v1.0.md`** — that is why the first Claim-Sheet
amendment is A2), and both opening sections now point a reader at the amendments before the
slots.

```text
A2.1  the four dev measurements in order (screen -> role coverage -> payload conditioning
      -> extension), the seven-mass table, and THE THREE THINGS IN IT THAT ARE THE
      AMENDMENT; then the scope statement (one env, one contact, one trajectory, one
      probe, seven masses; limitation 74 carried).
A2.2  why it changes the path: Slot 7 treated payload as a generalization axis; it is the
      determinant.  A pooled confirmatory read would report a fact about payload as a
      fact about structural sensing.
A2.3  Option C adopted; A and B shown unavailable against §9.5's own clause; and the
      NO-REGENERATION correction.
A2.4  Slot 11 — EVERY BAR UNCHANGED and stated as unchanged; adds a scope bound on the
      SENTENCE a success licenses (name the payload range; no extension by
      interpolation, extrapolation, or silence).
A2.5  Slot 12 — a structural null is a HYPOTHESIS failure only where the screen found
      signal.  A null where the instrument is blind is the Slot-13 shape.
      *** THIS MAKES OUR CLEAN NEGATIVE HARDER TO CLAIM, NOT EASIER, and A2 says so. ***
A2.6  Slot 13 — the payload-bounded non-transfer shape, four parts (a) negative reported
      as bounded (b) positive bounded to measured masses (c) state payload-conditionality,
      claim no mechanism (d) STRUCTURAL FAMILY ONLY — the extension measured no actuator
      or sensor signature.
A2.7  Slot 7 — confirmatory structural S-vs-C1 reported STRATIFIED BY PAYLOAD as well as
      pooled.  Explicitly a REPORTING rule: no per-stratum bars, no post-hoc stratum
      selection, pooled bars unchanged.
A2.8  six claim-strength limits, binding on A2 / Technical Report / Accessible Piece.
A2.9  what approving A2 does NOT authorize — written INSIDE the contract so approval
      cannot be read as reaching downstream.
```

**THE SENTENCE A2 EXISTS TO SAY (A2.1 point 3), and it is the one new inference:**

```text
The role-coverage read gave val and test ONE detectable severity each.  That read came
from the SCREEN, and THE SCREEN RAN ONLY AT 0.000 kg AND 0.050 kg — and the assignment
reserves BOTH of those for DEV (payload_dev_nominal, payload_dev_0p050kg).
  val  reserves 0.100 / 0.125   its 0.40 is SUB_THRESHOLD at both
  test reserves 0.150 / 0.200   its 0.35 is SUB_THRESHOLD at both
MEASURED AT THE PAYLOADS EACH SPLIT ACTUALLY CARRIES, ROLE COVERAGE IS 0/0/0/0.
I sourced the weight-to-split map from config/proposed-gate3-assignment-v0.1.json
(context_profiles.payloads) — NOT from either result artifact — precisely so the claim
does not depend on the artifact that motivated the question.  Rebuild it that way.
```

**THE NO-REGENERATION CORRECTION (A2.3), which retires a standing expectation:**

```text
Both continuity files have said since S33 that the delivered 472-reservation dev set is
"slated for full regeneration from zero after A2."  THAT WAS TRUE WHEN A2 WAS EXPECTED
TO ADD A SEVERITY BAND.  The generator expands healthy -> structure -> actuator ->
sensor per split and derives each seed from its ordinal, so extending
grid["structure"]["severities"] renumbers and reseeds everything after it.
*** OPTION C INSERTS NOTHING.  No reserved severity, no payload level, no split
assignment moves.  SO A2 SHIFTS NO SEED ORDINAL, INVALIDATES NO GENERATED DATA,
REQUIRES NO archive/ MOVE, AND PERFORMS NONE. ***
If the delivered set is superseded it is for some OTHER reason, under its own
authorization, with its own exclusion trail.  I asked Codex to block this if it sees an
assignment- or config-side reason I do not.
```

## THE S75 FINDING — MY OWN S74 DISCLOSURE DID NOT GO FAR ENOUGH

**S74 measured what a single well-shaped flip does to THE OUTCOME. That is a different
question from what it does to THE ROLE-RETENTION SENTENCE, because R10 fires before R11
and hides it. This is the same shape as every good finding in this project: the defect was
one layer below the layer I was checking.**

```text
CHEAPEST OWN-ROLE RUNG PER MASS, AS PCT OF THAT MASS'S OWN THRESHOLD
  0.025 pilot  0.60   -18.233%          0.100 val   0.40    -5.746%   <- IN BAND
  0.050 dev    0.50    -5.013% <- BAND  0.125 val   0.40   -17.605%
  0.075 pilot  0.60   -50.305%          0.150 test  0.35    -4.141%   <- IN BAND
  0.200 test   0.35   -22.583%
THREE OF SEVEN ROLE LOSSES ARE INSIDE THE SAME tau_anchor = 0.10 BAND.

WELL-SHAPED SINGLE-FLIP SWEEP, RE-RUN S75 against {outcome, empty set, all-roles-false,
Option-B cap}.  EXACTLY FOUR flips move ANY of them, ALL FOUR IN BAND:
  0.050@0.50 -5.0%  |  0.100@0.40 -5.7%  |  0.125@0.35 +2.1%  |  0.150@0.35 -4.1%
  Outcome stays X_CASE_EMPTY in all four.  Option-B cap stays None in all four.
  61 of the remaining 66 are MECHANICAL shape violations (an interior flip of a monotone
  ladder breaks PREFIX or MONOTONE by construction — split them or the number lies).

SO A2 WRITES THE AGGREGATE, NOT THE UNIVERSAL:
  "no measured mass retained its own reserved severity, AND AT THREE OF THE SEVEN THE
   MARGIN WAS INSIDE THE INSTRUMENT'S OWN REPRODUCIBILITY BAND."
LICENSING DOES NOT MOVE.  Option B breaks at the FIRST mass, 0.025 at 18.2%, well
outside the band, and no combination of in-band flips repairs the prefix (checked).
```

**THIRD CONSECUTIVE SESSION WHERE THE REPORTABLE THING WAS A LIMIT ON OUR OWN CLAIM RATHER
THAN A DEFECT IN AN ARTIFACT.** I think that is correct for this stage, and I named it in
the human report rather than letting it read as caution for its own sake. Watch it, though:
if a session produces *only* a claim-strength narrowing and no forward motion twice more,
that is a signal to check whether the project is polishing instead of moving.

## THE S74 FINDING — THE CLASSIFICATION IS ROBUST; THE SHAPE IT LICENSES IS NOT, AT ONE EDGE

**The artifact is arithmetically exact and I verified it that way. This is a different
question: how far is each sentence of the A2 reading from a different sentence? The scale
is NOT invented — it is §9.3's own `tau_anchor = 0.10` of a cell's own threshold, the band
the document already declared too small to constrain a verdict, fixed from the executed
screen's published margins before any extension datum existed. Rebuild this first if A2
is being drafted.**

```text
SIX OF SEVENTY RUNGS SIT INSIDE THAT BAND (|margin| / threshold < 0.10)
  0.125 @ 0.35   +2.1%  TESTABLE       <- the ONLY rung 0.125 has
  0.150 @ 0.35   -4.1%  SUB_THRESHOLD  <- the whole reason 0.150 is EMPTY
  0.050 @ 0.50   -5.0%  SUB_THRESHOLD  (the known anchor edge, cell 6 was -2.1%)
  0.100 @ 0.40   -5.7%  |  0.075 @ 0.45  -6.3%  |  0.025 @ 0.55  -1.6%

SINGLE-RUNG FLIP SWEEP over all 70 rungs, EACH FLIPPED ALONE.  *** SPLIT THE RESULTS OR
THE NUMBER LIES. ***  Flipping an INTERIOR rung of a monotone ladder breaks PREFIX or
MONOTONE BY CONSTRUCTION, so an R8/R9 landing measures the flip, not the result.  My
first pass reported "63 of 70 change the answer" and that framing was WRONG.
  61 mechanical (shape violation)  |  7 unchanged  |  2 WELL SHAPED AND CHANGED
    0.125 @ 0.35 at 2.1%  ->  still R10, empty = {0.125, 0.150, 0.200}
    0.150 @ 0.35 at 4.1%  ->  still R10, empty = {0.200}
  BOTH INSIDE THE BAND.  NO OTHER FLIP CHANGES ANYTHING.

ROBUST, WITH THE DISTANCE MEASURED
  "some mass is empty" (R10)    0.200 is empty by >= 22.6% of its own threshold.
                                Reaching R11 requires THAT rung to flip.  HOLDS.
  "Option B not licensed"       the prefix breaks at the FIRST ascending mass, 0.025
                                (pilot, reserves 0.60/0.85), cheapest own-role rung
                                18.2% away.  Reaching R12 needs a flip at 50.3%.  HOLDS.
  "Option A not licensed"       intersection empty AND R10 excludes it BY RULE.  HOLDS.

NOT ROBUST
  "the empty masses are exactly 0.150 and 0.200"  rests on +2.1% at 0.125 and -4.1% at
  0.150 — the two rungs nearest a threshold anywhere in the grid, both inside the band,
  both at the SAME severity (remEI 0.35) that separates them.
  *** THE EXISTENCE of a payload region with no testable reserved severity IS ESTABLISHED.
  THE LOCATION of its boundary IS NOT RESOLVED at this instrument's own reproducibility
  scale.  Say it that way in A2, the Technical Report, and the Accessible Piece. ***
  -> CARRIED LIMITATION for Gate 7.
```

## THE S74 AUDIT — WHAT IS NOW CHECKED, SO NOBODY RE-CHECKS IT

**130/130 pass. Written as a standalone instrument that does NOT import
`run_payload_boundary_extension.py` (X12). Three sources beyond the artifact: the approved
`plan.json`, the committed `stage_abc_screen.json`, and the two frozen protocol files on
disk. Rebuild recipe below; the instrument itself lived in the S74 scratchpad.**

```text
BYTES        raw == canonical JSON, 388,550 B, 0 LF / 0 CR, digest as named.
             *** LIMITATION 80 CANNOT BITE IT — canonical JSON emits NO newline of either
             kind, so no eol filter can act.  Same property as plan.json. ***
CARRIED FWD  inputs / protocol / plan BYTE-IDENTICAL to the approved plan document.
             plan.json still hashes to 15298da4….  preflight.plan_digest_match true.
PINS         protocol-p-v2.3.3.md -> 5689dad7… | extension doc -> 538ae06b… |
             assignment -> 76255a80…, ALL RECOMPUTED FROM THE FILES (LF-normalized).
             All 126 identity payloads carry those same five pins.
AUTHORITY    LIFTED FROM THE FROZEN DOCUMENT (its line 1016), not transcribed.  The exact
             string is "DEVELOPMENT ONLY: ineligible for confirmatory analysis; cannot
             change Protocol P outcome or role-coverage counts."  *** THERE IS NO "case"
             IN IT.  I hard-coded "outcome case" from memory and my own check went red. ***
LEDGER       126 entries | 126 distinct physical keys | 126 distinct stamps, each
             recomputing as dev-sha256(its OWN canonical string) | every canonical string
             is itself canonical | §11.3 field set exactly the pinned FOURTEEN on all 126 |
             `overrides` exactly the FIVE non-provenance inputs, provenance_hash absent.
KEY DIGEST   126 realized keys through the pinned two-stage recipe -> plan's 9889afa6….
X1           partition rebuilt FROM THE PAYLOADS: 77/7/7/7/7/7/7/7; every planned
             membership_count equals its realized class count; seeds 160000+1000k+2.
CRN          within a class, payloads differ ONLY in the three mass expressions, and
             `reservation` is byte-identical across masses.
X2           no pilot/val/test identity anywhere in 11,015 decoded string positions.
NULL         196 distances RECOMPUTED from the persisted coefficients; the 28 pairs at each
             mass are exactly C(8,2) over that mass's own healthy keys; Q95 =
             quantile(28, .95, method="higher"); threshold = 2*Q95; pause == (Q95>=0.30),
             WHICH IS TRUE AT ALL SEVEN MASSES.
LADDER       70 distances recomputed; margins == D - threshold; verdicts == sign of margin;
             every row's severity/condition/mass/identity/provenance agree with its keys;
             every row cites its own mass's k=0 healthy.
SHAPE        PREFIX at all 7; MONOTONE over all 21 pairs.  X8: 168 comparisons rebuilt,
             min 0.135079151914, no identical pair.
CENSUS       126+1=127; XA 18 / XM-C 48 / XM-B 60 REBUILT FROM THE LEDGER'S OWN STAGE
             STAMPS; 70+70+392 = 532 counted by walking the ACTUAL joins; step counts ==
             3,000 x stage rollouts; total elapsed == SIGMA ledger + replay.
CLASSIFIER   R0..R12 applied from scratch; R10 is the FIRST AND ONLY rule that fires.
X7           0 offenders; no DECODED string carries a backslash.  config/config.json absent.
VERIFY       full packet suite 1,306 passed in 123.31 s | compileall clean | 0 rollouts.

*** THE ANCHOR CAME OUT BETTER THAN §9.3 REQUIRED, AND IT IS WORTH KEEPING. ***
  Rebuilt cell 6 from stage_abc_screen.json ITSELF: its own 28 nulls give Q95 0.37033237,
  threshold 0.74066474, and its ten per-cell D values match the ten the artifact records.
  The NINE constrained rungs, the single unconstrained {0.50}, and the (0.0211, 0.1962)
  stability interval all re-derive.
  ALL TEN RUNGS AGREE, INCLUDING THE UNCONSTRAINED ONE.  D ratios anchor/cell6 span
  0.9605-1.1586.  Not a licensing claim; it is evidence the rebuilt probe/fault/identity
  instrument reproduces the screen rather than merely passing a passable test.

*** THE BOUNDARY OF BOTH AUDITS, AND IT MUST GO IN THE TECHNICAL REPORT. ***
  Everything DOWNSTREAM of the coefficient vectors is independently recomputable from the
  file and I recomputed all of it.  THE COEFFICIENT VECTORS THEMSELVES ARE NOT — the raw
  gauge traces are not persisted, so harmonic_coefficients over [1000,1768) cannot be
  re-derived from the artifact alone.  That step is covered by the replay gate, the
  anchor's agreement with the screen, and X8 — and by NOTHING either audit did.  Two
  independent reconstructions must not be allowed to imply coverage they do not have.
```

## S74 INSTRUMENT FAULTS — BOTH MINE, BOTH CAUGHT BY THE ARTIFACT DISAGREEING WITH ME

```text
1 I HARD-CODED THE AUTHORITY STRING FROM MEMORY and got one word wrong ("outcome case").
  THE FIX WAS NOT TO CORRECT THE TRANSCRIPTION.  It was to stop transcribing and lift the
  string out of the frozen document at run time.  *** X12 APPLIES TO MY OWN INSTRUMENT,
  NOT ONLY TO THE THING IT CHECKS.  Any literal I copy from a document is a SECOND COPY,
  not a second source.  Write it that way in the first draft. ***
2 I ASSERTED "no backslash anywhere in the artifact", carried over from plan.json where it
  IS true.  It CANNOT be true here: the result embeds 126 canonical JSON strings whose own
  quotes are escaped (9,576 raw backslashes, all exactly \").  The operative property is
  the DECODED domain, which is what X7 speaks about — 0 there.
  *** A PROPERTY THAT HOLDS OF ONE ARTIFACT IS NOT A PROPERTY OF THE ARTIFACT CLASS. ***
3 MY FIRST FLIP-SWEEP SUMMARY SAID "63 of 70 change the answer."  True and USELESS: 61 of
  those are shape violations a monotone ladder makes by construction.  I split the table
  before publishing it.  *** A SENSITIVITY NUMBER THAT COUNTS IMPOSSIBLE PERTURBATIONS
  OVERSTATES FRAGILITY EXACTLY AS BADLY AS OMITTING THEM UNDERSTATES IT. ***
```

## ONE §11.3 WORDING OBSERVATION, DELIBERATELY NOT ESCALATED

```text
§11.3's "Why this is unique per rollout" says two rollouts at different masses "differ in
mass_index, distal_payload_mass_kg and overrides.distal_payload_mass_kg."  MEASURED: within
a stage that is exact, but ACROSS THE XA/XM BOUNDARY they also differ in `stage` — the
anchor mass runs as XA and the other six as XM, exactly as §8 schedules.  The sentence
establishes SUFFICIENCY for distinctness and an extra differing field only strengthens it.
NO VERSION BUMP.  Same class as the §12 "the plan artifact must carry the executor's own
count" slip both agents agreed was non-operative in S72.  Recorded so the next reader
walking §11.3 against the ledger does not think a field drifted.
```

## THE S73 PRE-AUTHORIZATION AUDIT — SPENT, BUT TWO RULES SURVIVE IT

**The plan is consumed and the run is done, so most of that block retired with it. These
two facts still bind if a SECOND joint authorization is ever issued.**

```text
THE INVENTORY RULE.  run_replay_gate brackets its ONE rollout with
  inventory([data_root, PACKET_ROOT], shallow_roots=[REPO_ROOT]) and fails on ANY added /
  removed / modified file at a point where rollout_spent is ALREADY 1.  An incidental write
  does not merely fail a check: IT CONVERTS THE AUTHORIZED ROLLOUT INTO A TERMINAL
  X_DEFAULT_PATH_UNVERIFIED.  Nothing filters that list — __pycache__/, .pytest_cache/ and
  the repo root's MUJOCO_LOG.TXT are all inside it (3,203 files vs MIN_WATCHED_FILES=100).
  WHILE ANY FUTURE RUN EXECUTES: no pytest, no compileall, no second agent session, no
  editor save, no git write.  Run it as a background process and poll the RESULTS JSON.
THE TWO-LAYER AUTHORIZATION GATE.  require_authorized_plan accepts a CONTENT-edited plan
  named by its OWN digest — and that plan then dies at X0E, where build_plan_document is
  recomputed from the bound context and compared by canonical_json equality, FOR 0 ROLLOUTS
  and BEFORE the replay gate is called.  Naming gate and content gate are independent; a
  drifted plan cannot reach a rollout.
```

## THE S71 FINDING — THE WHITELIST IS THE WHOLE DECISION AND NOTHING WAS CHECKING IT

**Three gaps, all around code that BEHAVES CORRECTLY. Every one of my 18 new cases is GREEN
against the reviewed state. The evidence is the MUTATION SWEEP, not a red-check, and I said
so at the top of the turn rather than letting eighteen new tests imply eighteen defects.**

```text
                            sweep over Codex's c850a4b6      after my additions
   cases                            19                              19
   caught                           14                              18
   survivors                         5                               1

1 _URI_SCHEMES IS ADOPTED BY ITS OWN TESTS, NEVER CHECKED.
    Both scheme tests are @parametrize(..., x._URI_SCHEMES), so they FOLLOW the list.
      dropped "ftps"  -> focused suite PASSES        dropped "sftp"  -> PASSES
      added   "ws"    -> focused suite PASSES, and "ws://host/PRIVATE/row.npz" is
                         then PUBLISHED UNCHANGED.  ADDING IS THE LEAK DIRECTION.
    Dropping "https"/"git+ssh" is caught only because two tests quote those URLs as
    literals; adding "file"/"reason" only because they sit in a hard-coded 4-tuple.
    Neither catch is a property of the list.  REQUIREMENT (r) APPLIED TO A CONSTANT.
    This is my own S70 Lesson 98 written down and NOT implemented.
    FIX: an equality pin, with the measured survivor table in its docstring.

2 THE ACCEPT SIDE IS ONLY EVER TESTED AT A SPACE OR AT START-OF-STRING.
    Codex's 312-cell boundary matrix was a PROBE; the committed test it added is the
    suffix contract only, so requirement (cc) was not discharged for the accept side.
      guard's longer-token class [A-Za-z0-9+.\-] widened to [^\s]: suite PASSES
      '(https://example.org/spec)' -> '(https:spec)'   same for [ ] ' " 
    MEASURED over all 100 printable chars: the set that mangles a protected URL is
    EXACTLY [A-Za-z0-9+.-] plus "/" (the slash is a genuine POSIX root).  That is
    precisely the stated contract, so the test asserts the MEASUREMENT.
    FIX: 11 boundary cases (accept) + 6 scheme-character cases (refuse, pinning the
    class from the other end -- "." and "+" are legal scheme chars, so narrowing to
    [A-Za-z0-9] would leave "a.https://host/PRIVATE/row.npz" protected).

3 A DISCLOSURE OF MINE MISSTATES ITS OWN LIMITATION.  (S70, Codex reviewed past it.)
    docstring: an unlisted scheme's URL "becomes x".   MEASURED: "myscheme:x".
    The test whose docstring says it is "the test that keeps the two together"
    asserts the RIGHT value, so nothing could see the disagreement.  Same class as
    Codex's own S69 correction, one file over.  Sentence corrected to the measurement.
    Also corrected: test_every_protected_scheme_survives_the_scrub claimed "Dropping a
    scheme makes exactly this red."  READING the list is exactly why it cannot.
```

## WHAT I ACCEPTED FROM CODEX IN S70, AND WHAT I CHANGED IN S71

```text
ITS FINDING IS RIGHT AND I KEPT EVERY LINE.  My S70 guard was one bare lookbehind per
name -- (?<!https:)// -- which asks whether the text ENDS IN "https:", not whether
"https" is the complete scheme token.  Measured through both blobs:
  'reasonhttps://host/PRIVATE/row.npz'  MINE c7451068 UNCHANGED | CODEX 'reasonhttps:row.npz'
  my widened grid: 192 rooted survivors under mine, 112 under Codex's, 0 regressions.
  the 80 it closed are EXACTLY the suffix family: reasonhttps: prefixgit: myssh:
  xgit+ssh: shttp: sftps: 0https: -https: .https: +ssh:
  the 112 that remain are ALL BOUNDED NAMED SCHEMES = the disclosed third ambiguity.
Its construction, and it is correct: per name, branch 1 accepts text not ending in that
name; branch 2 RESTORES acceptance when the name is only the suffix of a longer
RFC-scheme token.  The pair declines only a bounded exact name.  "git+ssh" is now NAMED
rather than shielded by its own "ssh" suffix -- that inconsistency is what exposed it.

scripts/run_payload_boundary_extension.py  +7/-1    95040d93   DOCSTRING ONLY
tests/test_payload_boundary_extension.py   +91/-7   0d7b68fc   152 -> 170 tests

*** I VERIFIED MY OWN "NO OPERATIONAL CHANGE" CLAIM RATHER THAN ASSERTING IT ***
  codex S70 c850a4b6 vs MY S71   executable AST (docstrings stripped) EQUAL = True
  mine  S70 c7451068 vs codex    EQUAL = False
  3,256-cell grid: 0 outputs differ | 576-cell pair grid: 0 outputs differ

THE NEW AXIS, AND IT FOUND NOTHING -- WHICH IS A RESULT.
  TWO PATHS IN ONE MESSAGE.  Every grid either of us has built (my 286, my 968, my
  3,256, Codex's 312) put exactly ONE path in the string, and both patterns are re.sub
  whose `lead` group CONSUMES a character a following match might need.  8 first halves
  x 9 joiners x 9 second halves = 576 cells: 0 rooted survivors not explained by a
  protected URL, 0 destroyed messages, 0 guard refusals.  Rebuild this axis first.

VERIFICATION
  focused 170 | -O 170 | FULL SUITE 1,306 in 126.03 s | compileall clean
  *** THE -O WARNING WAS CHECKED, NOT REPORTED.  It appeared this session; I stashed my
  changes, re-ran against the untouched state, and found it there too -- it is pytest's
  own optimized-assertion notice.  Reporting it as new would have been a false alarm. ***
  RED-CHECK, HONEST RESULT: all 18 new cases GREEN against c850a4b6 = COVERAGE.
    Against my own pre-review c7451068 the equality pin and all 6 boundary-character
    cases are RED -- an independent reproduction of CODEX's finding through a different
    instrument (a boundary character class rather than the word "prefix"), not a find.
  SWEEP 19 cases | 18 caught | 1 survivor | 0 bad anchors | BOTH PASSES AGREE
    RE-RUN FROM SCRATCH because Codex's edit changed which rule reaches which input,
    which retires anchors silently (my own S70 lesson 98, third note).
    survivor: whole_message_discard_removed, unreachable BY CONSTRUCTION, covered as a
    pair by the LESSON-63 DOUBLE (substitution fixpoint + discard), which IS caught.
  ACCEPT SIDE: plan document / execute skeleton / failed-plan document -> 0 / 0 / 0
    offenders, builders called DIRECTLY.  No plan mode, no replay, 0 rollouts.
  results/payload_boundary_extension absent | config/config.json absent.

INSTRUMENT NOTE — the slice harness.  To drive two blobs in one process I exec a SLICE
of each (from `_WINDOWS_ABSOLUTE = re.compile(` to `def describe_error(`) rather than
importing whole modules.  A slice is a NEW INSTRUMENT.  It starts by comparing itself
against the genuinely-imported module over 400 inputs and REFUSES to continue on any
disagreement.  0 disagreements.  Do not skip that check when rebuilding it.
```

## THE S70 FINDING — A COMPLETE ROOTED PATH WAS PUBLISHED, BECAUSE A URL AND A UNC PATH ARE THE SAME SHAPE

**The instrument was the cross-product again, WIDENED WHERE IT WAS THIN. My S69 grid crossed
renderings with prefixes; it did not include a prefix ending in a LETTER-COLON. Twenty-two
renderings x eleven preceding contexts x four suffixes = 968 cells, each classified by what
SURVIVES: a rooted path, a relative suffix, a destroyed message, or clean.**

```text
                      committed f2d9f3b1      after my repair c7451068
   CLEAN                    632                     644
   RELATIVE_SURVIVOR        332                     324
   ROOTED_SURVIVOR            4                       0     <- X7 VIOLATED
   GUARD_REFUSES              0                       0

1 THE FOUR ROOTED SURVIVORS ARE ONE SHAPE.
    'reason://host/PRIVATE/row.npz'  ->  UNCHANGED.  Host, private dir and file name.
    CAUSE: the forward-UNC lookbehind (?<![A-Za-z0-9+.\-]:) means "any alnum + colon is a
    scheme", a far wider claim than "this is a URL".  THE WRITER'S GUARD SHARES THE PATTERN,
    so it declined too: the artifact IS written and the path IS published.  X6 satisfied,
    X7 violated -- the same severity class as the S69 glued-UNC family, which we FIXED.
    TRIGGER: a LETTER before the colon.  A DIGIT is caught by the non-letter drive rule; a
    space, quote, bracket or equals leaves the UNC rule free.  NOT reachable from any
    f-string in this file (there is no ":{...}" shape in it) -- reachable from str(exc),
    foreign content, and any future message.  I SAID SO rather than claiming reachability.

2 EIGHT CELLS KEPT THE DRIVE DESIGNATOR.
    r'opaque-prefixC:/My Data\PRIVATE\row.npz' -> r'opaque-prefixC:My Data\PRIVATE\row.npz'
    The forward-slash drive form carried (?<![A-Za-z0-9]) so it could not fire inside a
    word; the POSIX rule then matched only "/My" and put the drive back.  Inside Codex's
    disclosed whitespace family but WIDER than its sentence, which says the absolute root
    is removed.  I MADE THE CODE MATCH ITS SENTENCE rather than edit the sentence again.

THE REPAIR, AND THE JUDGMENT INSIDE IT
    A URL host and a UNC host are LEXICALLY IDENTICAL, so no boundary rule separates them
    and a NAME-BASED decision is unavoidable.  The honest version NAMES the protected set:
      _URI_SCHEMES = ("http", "https", "ftp", "ftps", "sftp", "ssh", "git")
      _URI_SCHEME_GUARD = "".join(f"(?<!(?i:{scheme}):)" for scheme in _URI_SCHEMES)
    "file" IS DELIBERATELY ABSENT: file://host/share IS a path.
    CONVERSE COST, DISCLOSED AND PINNED: an unlisted scheme's // form is reduced like a
    path, so "myscheme://host/x" -> "myscheme:x".
    The drive form drops its boundary and refuses a SECOND slash instead: [A-Za-z]:/(?!/).
    A URL's separator is always "://", so (?!/) declines it with no boundary needed.
    MEASURED PROSE COST OF THE PAIR: ZERO over 30 sentences (this project's vocabulary plus
    http/https/ftp/ftps/sftp/ssh/git in lower, UPPER and Title case).
```

## THE S69 FINDING (SUPERSEDED IN PART BY S70, KEPT FOR THE LESSON) — FOUR FAMILIES IN ONE GRID

**The instrument was a CROSS-PRODUCT, not a reading. Eleven path renderings x thirteen
prefixes x two suffixes = 286 sentences, all driven through BOTH agents' blobs in one
process, each output asked two questions: does the private directory marker survive, and
was the whole message replaced by `<path>`. Reading found nothing in three sessions; the
grid found four families in one run — and told me which one NOT to fix.**

```text
   leaking renderings (of 286)   MINE 04ec936e 82 | CODEX 9cd10305 34 | MINE 9fd723b0 0

THE POST-CONDITION CANNOT HELP WITH ANY OF THESE.  An embedded path leaves the WHOLE
string relative, so PurePath has nothing to say and the REGEX IS THE ONLY DEFENCE.

1 UNC GLUED TO PROSE — a complete absolute path published.  X7 violated.
    "opaque-prefix//host/PRIVATE/row.npz"  published unchanged; gate PASSED on self-digest
    The outer token boundary bought NOTHING: that alternative already carries its own
    (?<![A-Za-z0-9+.\-]:) lookbehind, and THAT is what keeps https:// safe.  Dropped.

2 A PATH CONTAINING A SPACE — *** THE LIKELIEST LEAK IN THE FILE. ***
    r"...absent: D:\My Data\PRIVATE\row.npz" -> r"...absent: My Data\PRIVATE\row.npz"
    r"C:\Program Files\PRIVATE\row.npz"      -> r"Program Files\PRIVATE\row.npz"
    r"...open \\host\My Share\PRIVATE\..."   -> r"...open <path> Share\PRIVATE\row.npz"
    The tail stopped at the first whitespace, so the substitution only ever saw the first
    SPACE-FREE RUN.  "Program Files", "My Documents" and THIS REPO'S OWN PARENT all
    contain a space; the repo-root replacement covers <repo> and nothing else.
    *** SCOPE, AND IT IS NOT THE SAME AS THE OTHER THREE.  What survives is RELATIVE, so
    the guard says false, the artifact IS written and X7 AS WRITTEN IS SATISFIED.  What
    fails is the scrubber's own final-component contract and the reason X7 exists.  Never
    call this an X7 violation. ***
    FIX: the tail may cross a space only when a BACKSLASH still lies ahead of the next
    whitespace.  The gate is a backslash because our prose is FORWARD-slashed
    (dev/pilot/val, C1/S, 0.10 N / 0.25), so no sentence of ours can satisfy it.
    Measured: 10-sentence vocabulary battery byte-identical; 4 adversarial sentences keep
    their tails.  ONE input over-consumes and I NAMED IT: r"C:\a\row.npz a\b" -> "b".

3 MIXED SEPARATORS — a bad REDUCTION, not a missed match.
    r"opaque-prefixC:/PRIVATE\row.npz" -> r"opaque-prefixC:PRIVATE\row.npz"
    PurePosixPath cannot see a backslash, so its .name for the span r"/PRIVATE\row.npz"
    is the WHOLE r"PRIVATE\row.npz".  _final_component() splits on BOTH separators.

4 *** NOT FIXED, DELIBERATELY — the single-slash POSIX form. ***
    "opaque-prefix/PRIVATE/row.npz"  and  "/mnt/My Data/PRIVATE/row.npz"  are published.
    Closing it means matching a lone "/" after an ordinary character, which MEASURED
    against our own vocabulary turns dev/pilot/val -> "val", C1/S -> "C1S", 1/2 -> "12".
    A silently corrupted reason is worse than a leaked one (limitation 93).  It is a
    DISCLOSED limitation in the docstring, PINNED BY A TEST so nobody closes it, and the
    guard uses the same pattern ON PURPOSE — widen one side only and X7 fires while X6 is
    writing the record.  On a Windows host the paths that arise are drive- or UNC-rooted
    and both are now covered in BOTH shapes.
```

## WHAT I ACCEPTED FROM CODEX IN S69, AND WHAT I CHANGED IN S70

```text
CODEX'S S69 WAS DOCUMENTATION ONLY AND I VERIFIED THAT RATHER THAN TAKING IT:
  mine S69 9fd723b0  vs codex S69 f2d9f3b1   executable AST (docstrings stripped) EQUAL
  codex S69 f2d9f3b1 vs mine S70 c7451068    NOT equal (mine changes two patterns)
Its finding is right and I kept every word: my disclosure said "two spellings" when the
measured behaviour was wider.  A disclosure that understates its own limitation is worth
less than none.  ITS THREE ADDED FORMS REPRODUCE under my own instrument.
*** THEREFORE THE S70 FINDING IS NOT A REGRESSION CODEX INTRODUCED.  It has been live
since MY S69 and both of us reviewed past it.  Say it that way. ***

scripts/run_payload_boundary_extension.py  +54/-24   c7451068
tests/test_payload_boundary_extension.py   +147/-0   485dcc3d   106 -> 141 tests

 - _URI_SCHEMES + _URI_SCHEME_GUARD replace the blanket "any alnum + colon" lookbehind.
 - the forward-slash drive form: [A-Za-z]:/(?!/) instead of (?<![A-Za-z0-9])[A-Za-z]:/.
 - the docstring now names THREE ambiguities as SHAPES, not spellings: the glued
   single-slash POSIX form; a path containing WHITESPACE (and a TAB is never crossed,
   because the gate is a literal space -- Codex's wording did not reach that); and a //
   preceded by a named scheme.  Every survivor in the 968-cell grid is in one of the three.
 - the grid property is now a COMMITTED TEST, not a paragraph.

*** MY OWN REPAIR MADE AN EXISTING GUARD UNTESTABLE, AND THE SWEEP CAUGHT IT. ***
  Once the drive form dropped its boundary, r"...opaque-prefixC:/PRIVATE\plant\row.npz" --
  the ONLY committed case exercising _final_component's both-separator split -- began being
  consumed by the WINDOWS rule first.  Deleting the split then SURVIVED the whole focused
  suite.  Closed with a case only the POSIX rule can match
  (r"OSError: cannot open /mnt/PRIVATE\plant\row.npz") plus a direct call on the span.
  FOURTH CONSECUTIVE SESSION where the defect lived one layer below the layer being fixed.

VERIFICATION
  focused 141 | -O 141 | FULL SUITE 1,277 in 127.33 s | compileall clean
  RED-CHECK vs f2d9f3b1, DRIVEN DIRECTLY: the test file cannot be COLLECTED against that
    blob (no _URI_SCHEMES), so pytest yields no verdicts -- A HARNESS RESULT, not a
    red-check, and I did not report it as one.  Contract by contract: 14 RED, 21 already
    true.  THE 21 ARE COVERAGE (the old lookbehind protected every scheme) AND I SAID SO.
  SWEEP 10 cases | 10 caught | 0 survivors | 0 bad anchors | BOTH PASSES AGREE
    UNC lookbehind restored; drive boundary restored; the (?!/) refusal removed; a scheme
    dropped; "file" added; the scheme guard made case-sensitive; space crossing removed;
    _final_component split on one separator; substitution fixpoint removed; repo-root
    replacement removed.
    *** ONE HARNESS FAULT, REPORTED: for the space-crossing case my name extraction picked
    up a captured-stdout line beginning "FAILED:" instead of the summary lines.  The
    VERDICT is sound (re-ran alone: 9 real failures); the DETAIL field was not. ***
  ACCEPT SIDE (a stricter predicate is how X7 fires while X6 writes): plan document /
    execute skeleton / failed-plan document -> 0 / 0 / 0 offenders under BOTH predicates.
    Built by calling the document builders DIRECTLY.  NO plan mode, no replay, 0 rollouts.
  ENUMERATION over the committed 37,448 strings: still absolute after the scrub, 0 in both.
```

## WHAT I ACCEPTED FROM CODEX IN S68, AND THE ONE THING THAT LOOKS LIKE A FALSE POSITIVE

```text
ITS FINDING REPRODUCES.  The code declares PureWindowsPath as its semantics and the
embedded regex accepted a narrower drive alphabet.  Measured through both blobs:
  r"opaque-prefix1:\PRIVATE\row.npz"   MINE 04ec936e published | CODEX 9cd10305 clean
  82 vs 34 leaking renderings of 286.  Its correction closed 48 real cases.
I KEPT EVERY LINE: the widened backslash drive, the separate non-letter forward-slash
form, the retained URI boundary on letter schemes, and all four new test contracts.

*** LOOKS LIKE A FALSE POSITIVE, IS NOT.  The widened [^\\/\r\n]:\\ now rewrites
r"pattern [A-Za-z]:[\\/] was rejected".  That is CORRECT:
PureWindowsPath(r"]:\dir").is_absolute() is True, so the string really does record an
absolute path under the semantics we chose.  If that cost is ever judged too high, change
the DECLARED SEMANTICS, never the enumerator alone — they must agree or the artifact
dies. ***
```

## WHAT I CHANGED IN S69

```text
scripts/run_payload_boundary_extension.py  +90/-31   9fd723b0
tests/test_payload_boundary_extension.py   +175/-11  191d9b4d   83 -> 106 tests

 - the Windows/UNC tail may cross a space, gated on a BACKSLASH lookahead.
 - the "//host/share" alternative loses its outer token boundary; the single-slash form
   KEEPS it, and the docstring now names what that leaves uncovered and why.
 - _final_component(): a matched POSIX span reduces under BOTH separators.
 - _substitution_pass(): one pass extracted so a test can DRIVE it.
 - the fixpoint's stated reason re-measured and rewritten (see the S68 block below).

VERIFICATION
  focused 106 | -O 106 | FULL SUITE 1,242 in 117.26 s | compileall clean
  REDCHECK vs CODEX's 9cd10305 in an isolated packet copy: 11 RED, 95 green, ALL 83 OF
    CODEX'S PASS.  10 are behavioural; the 11th is red by AttributeError because
    _substitution_pass does not exist in that blob — a HARNESS result, not a find, and I
    said so.  The disclosed-gap test PASSES against 9cd10305: it is COVERAGE.
  SWEEP 11 cases | 10 caught | 1 survivor | 0 bad anchors | BOTH PASSES AGREE
    caught: space crossing removed; space gate widened to any separator; UNC boundary
    restored; drive narrowed back to letters (Codex's own case, still live);
    _final_component -> PurePosixPath.name; _final_component -> whole span; fixpoint
    removed; LESSON-63 DOUBLE (fixpoint+discard); repo-root replacement removed; POSIX
    lead character dropped.  Survivor: whole_message_discard_removed, unreachable BY
    CONSTRUCTION and covered as a pair by the double.
  *** TWO FAULTS IN MY OWN SWEEP HARNESS, BOTH REPORTED.  (1) The verdict carried
  pytest's elapsed time, so the two-pass detector reported disagreement on EVERY clean
  case — the exact mistake my own S65 notes warn about, made again.  (2) One anchor's
  indentation was wrong -> BAD ANCHOR (0 matches).  Both fixed before any number was
  taken.  A sweep result is worth exactly what its harness is worth. ***
```

## THE S68 FINDING (SUPERSEDED IN MECHANISM, KEPT FOR THE LESSON) — A REPAIR CAN DISCARD THE WHOLE REASON

**Codex's S67 correction dropped the token boundary from the backslash drive form so that
a path glued onto prose is caught. That was RIGHT and I kept it. It also made a state
reachable that could not be reached before, and the only exit from that state throws the
entire message away.**

```text
THE MECHANISM.  The POSIX rule reduces "/plant/\row.npz" to its final component
"\row.npz" and re-emits it after the boundary character, which BUILDS "C:\row.npz"
inside prose the Windows rule had ALREADY been offered and declined.  One pass therefore
ends holding an EMBEDDED path that no reduction can touch -- the sentence as a whole is
relative, so PurePath.name has nothing to take -- and the post-condition's only remaining
exit replaces the WHOLE message with "<path>".

MEASURED on Codex's exact state 25386e27:
   r"read row1C:/plant/\row.npz"                                    -> "<path>"
   r"ProtocolPError: pinned input absent at run1C:/data/\gate3.npz" -> "<path>"
   r"value 1C:/\ was rejected"                                      -> "<path>"
   and 6 of the 37,448 strings the committed enumeration test already generates.

IT DOES NOT DEFEAT X6 OR X7.  The artifact is written and no path leaks.  What is lost is
the REASON, which on a failure exit is the entire content of the record.  Limitation 93:
a scrubber that silently REPLACES a reason is worse than one that truncates it, because
nothing discloses the loss.

THE FIX: run the substitutions to a FIXPOINT rather than once, extracted as
substitute_known_path_spellings() so the caller's post-condition is checkable from
OUTSIDE without a second copy of the substitution.  TERMINATION IS ARITHMETIC.
The discard branch is KEPT as a last resort and is a deliberate sweep survivor; the
LESSON-63 DOUBLE removal (fixpoint + discard together) is what covers the pair.

*** S69 UPDATE — THIS MECHANISM IS NOW CLOSED AT ITS SOURCE AND THE FIXPOINT'S REASON
CHANGED.  _final_component() splits on both separators, so the POSIX replacement can no
longer RE-EMIT one, and the three sentences above now survive a SINGLE pass.  RE-MEASURED
with one pass over the 37,448 enumerated strings: 969 still absolute, TEN reaching the
discard exit — the live mechanism is now a REPEATED ROOT ("///data/gate3.npz" -> one pass
-> "/gate3.npz", still recorded, still relative as a whole).  I extracted
_substitution_pass() so a test DRIVES one pass instead of a docstring claiming what it
would do — the old docstring had just stopped being true, which IS the argument for the
extraction.  Max productive passes over the enumeration: 2 (65 strings). ***
```

## WHAT I ACCEPTED FROM CODEX IN S67, AND THE SCOPE CORRECTION ON TWO OF THREE

**All three corrections kept unchanged. Two needed a scope correction — they are real, but
not in the shape they were reported in, and a number nobody can re-derive is worse than no
number.** Driven through BOTH blobs in one process.

```text
1 EMBEDDED WINDOWS PATH — reproduces exactly as reported.
    {"inputs": {"note": r"opaque-prefixC:\PRIVATE\row.npz"}}
      MINE 5a5b0562  rc=1 artifact written  *** PRIVATE PUBLISHED ***
      CODEX 25386e27 rc=1 artifact written  clean
    X7 is about what a string RECORDS, not whether the whole string parses as a path.

2 UNSERIALIZABLE VALUES — REAL, but ONLY under inputs / protocol / plan.
    execute_document_skeleton copies exactly those THREE members of a foreign plan.
    Codex demonstrated it with the value under "x", where it never reaches the writer:
                             MINE 5a5b0562                 CODEX 25386e27
      inf under "x"          rc=1 artifact written          rc=1 written
      inf under "inputs"     rc=None NO ARTIFACT            rc=1 written
      surrogate under "x"    rc=1 artifact written          rc=1 written
      surrogate under inputs rc=None TRUNCATED (0 bytes)    rc=1 written
    The surrogate case is the worse one: write_text CREATES the file and then fails to
    encode, so the reader gets a zero-length payload_boundary.json rather than none.
    I MOVED THE THREE TEST PAYLOADS UNDER inputs.  Requirement (q).

3 NESTING RECURSION — the class is real; 990 is not a property of this code.
    extra frames before main()      depth 200/400/600   depth 800/900/960
      +0    MINE                    written             written
      +300  MINE                    written             rc=None NO ARTIFACT x3
      +0/+300  CODEX                written             written
    The threshold is a property of the CALLER'S STACK.  That is exactly why a gate is the
    right fix -- it makes the outcome caller-independent.  I re-aimed its test at
    MAX_PLAN_JSON_DEPTH + 1 so the case exercises the gate at its own boundary.

NO FALSE POSITIVES ON THE SUCCESS PATH — the risk a stricter predicate most obviously
creates.  Plan document 0 offenders (depth 5); execute skeleton 0 offenders (depth 7);
gate 64.  The tool's own artifact cannot be refused by its own writer.
```

## WHAT I CHANGED IN S68

```text
scripts/run_payload_boundary_extension.py  +51/-12   04ec936e
tests/test_payload_boundary_extension.py   +102/-5   4979af07   76 -> 81 tests

 - substitute_known_path_spellings(): both patterns to a FIXPOINT, its own function.
 - the discard branch kept, re-commented as a measured-unreachable LAST RESORT that costs
   the reader the whole reason, and named as a deliberate sweep survivor.
 - the three unserializable payloads moved under `inputs`, measurement in the docstring.
 - the depth case re-aimed at MAX_PLAN_JSON_DEPTH + 1, ambient-stack measurement recorded
   so nobody re-derives "990" as a property of this file.
 - THE ACCEPT SIDE of the depth gate (Lesson 62).  NOT A SILENT GAP -- three existing
   execute-mode tests also go red when the constant is tightened to 4 -- but none NAMES
   the property, so a reader could not tell the accept side was covered.  Clarity, not a
   find, and I said so in the turn.
 - a parametrized test over the three destroying sentences; and one over the enumeration
   asserting the discard branch is never REACHED (the existing enumeration assertion is
   satisfied TRIVIALLY by discarding everything, which is the failure mode just fixed).

VERIFICATION
  focused 81 | -O 81 | FULL SUITE 1,217 in 119.02 s | compileall clean
  REDCHECK of CODEX's five additions vs 5a5b0562:  9 RED, 67 green -- load-bearing.
  REDCHECK of MY four additions vs 25386e27:  3 of 4 RED for the right reason
    ("assert scrubbed != '<path>'" failing with '<path>' != '<path>').  The 4th is red by
    AttributeError because it needs the extracted function -> COVERAGE, not a red-check.
    The three re-aimed payload tests PASS against 25386e27 (its fixes handle them); their
    red state is the DIRECT MEASUREMENT above, not a pytest run, because that test file
    cannot even be COLLECTED against a blob with no MAX_PLAN_JSON_DEPTH.
  SWEEP 8 cases | 7 caught | 1 survivor | 0 bad anchors | BOTH PASSES AGREE
    caught: depth gate tightened below the plan; canonical-UTF-8 validation removed;
    depth gate removed; shared predicate reduced to whole-string PurePath; drive boundary
    restored; substitution fixpoint removed; and the LESSON-63 DOUBLE (fixpoint+discard).
    the survivor is whole_message_discard_removed, unreachable BY CONSTRUCTION.
```

## THE S67 FINDING — THE SCRUBBER IS AN ENUMERATION, THE GUARD IS A PREDICATE

**X6 says every execute exit persists the record; X7 says no artifact records an absolute
path and enforces it by RAISING. Every defect for three sessions has lived where they
meet. S66 (mine) found four collisions, S66 (Codex's) found two more one layer down, and
this is the third layer: not a missing spelling, but the GAP BETWEEN A LIST OF SPELLINGS
AND A PREDICATE.**

```text
THE MOVE THAT FOUND IT: stop picking examples, ENUMERATE.  Every string over
{ / \ C : x space . 1 } up to length 5 = 37,448 strings, scrub each, ask the guard.

   absolute BEFORE the scrub   5,845
   STILL ABSOLUTE AFTER IT     1,358    <- every one of these destroys the write
   after the S67 fix               0

TWO FAMILIES, NEITHER MATCHABLE BY EITHER PATTERN:
1. A BARE ROOT.  "/", "//", "///", "/ x" — no path COMPONENT follows the separator, so
   there is nothing for either regex to match, and PurePosixPath calls all of them
   absolute.
2. A DRIVE LETTER PurePath ACCEPTS AND [A-Za-z] DOES NOT.  PureWindowsPath treats ANY
   single character before ':' as a drive, so r"1:\dir\row.npz" and r".:\dir\row.npz"
   are absolute to the guard and invisible to the scrubber.  REAL paths with a REAL
   directory portion, not degenerate tokens.
MEASURED THROUGH main(): nine such shapes (value, key, nested in a list) returned rc=None,
raised ProtocolPError from inside the terminal write, and left the output dir EMPTY.
Codex's three repaired shapes were CLEAN in the same run — that is how I know the harness
reached the exit rather than failing earlier.
```

**THE SECOND HALF — the authorized path could still destroy the artifact.**

```text
We both accepted (S66) that approved plan content is embedded VERBATIM, because silently
rewriting content both agents named would be worse than the risk.  I did NOT reverse it.
But it rests on a PREMISE — "plan mode's own writer refuses an absolute path, so a plan
this tool wrote cannot carry one" — and authorization means only "the operator named this
document's canonical digest", which ANY document satisfies by being hashed.  MEASURED:
  foreign plan with an absolute-path KEY, named by its OWN digest b71ae34b...
    authorization PASSES | rc=None | ProtocolPError escapes | ARTIFACT NONE
  the same document through PLAN mode's writer: REFUSED  <- the premise itself HOLDS
require_authorized_plan now REFUSES such a plan after the digest match.  A REFUSAL, NOT A
REWRITE: it routes to the exit that scrubs, so the record is still written and names why.
AFTER THIS, NO REACHABLE EXECUTE-MODE STATE DEFEATS X6.
```

## WHAT I CHANGED IN S67

```text
scripts/run_payload_boundary_extension.py  +85/-19   5a5b0562
tests/test_payload_boundary_extension.py   +186/-0   f2f5031d   58 -> 71 tests

 - scrub_machine_paths ENDS WITH THE WRITER'S OWN PREDICATE, run to a FIXPOINT.
   TWO WRONG VERSIONS FIRST, both measured, both recorded in the code:
     "PureWindowsPath(s).name or PurePosixPath(s).name"  left 63 of 37,448 absolute —
       PurePosixPath sees NO separator in a Windows-rooted string, so ITS name is the
       WHOLE value and the `or` hands it straight back to the guard.
     one reduction per flavour   left 11 — the POSIX name of "/ :\" is " :\", which is
       absolute to the OTHER flavour.  Hence the fixpoint.
   Each pass must SHORTEN the string strictly, which bounds the loop by input length.
 - absolute_path_strings(): the writer's nested `visit` lifted to module level, returning
   every offending string from BOTH member names and values.  ONE function, asked by the
   writer AND by the authorization gate, so they cannot drift.  Requirement (r) applied
   between two call sites IN ONE FILE — which is where S65 found it last time too.
 - require_authorized_plan refuses a named plan that records an absolute path, with a
   sentence unique to that raise site AS RENDERED (requirement (ee)).
 - the length bound in the fixpoint is ARITHMETIC, not a runtime check, and the code says
   so.  It is kept because it makes TERMINATION a property of the code rather than of an
   argument.  It survives a sweep BY CONSTRUCTION.  Never call it a live guard.

VERIFICATION
  focused 71 | -O 71 | FULL SUITE 1,207 in 117.49 s | compileall clean
  REDCHECK vs Codex's 86fc3fdb in an isolated packet copy: 12 of 13 NEW TESTS RED,
    ALL 58 OF CODEX'S GREEN.  The 13th is the collision test — it covers CODEX'S guard,
    which works, so it is COVERAGE and I did not count it as a red-check.
  SWEEP 16 cases | 15 caught | 1 survivor | 0 bad anchors | BOTH PASSES AGREE
    fresh copytree per case, PYTHONDONTWRITEBYTECODE=1, caches cleared, no -x,
    anchors translated to the target's own newline and each asserted unique
    includes BOTH Lesson-63 double removals (gate+writer; fixpoint+Codex's key scrub)
    the survivor is the arithmetic length bound above
  COST of the shared predicate: 0.83 ms on the plan document, 37 ms on one 40x larger.
```

## WHAT I ACCEPTED FROM CODEX IN S67, AND THE TWO SURVIVORS IN ITS REPAIR

```text
BOTH OF CODEX'S S66 FINDINGS REPRODUCE.  Driven through its blob and mine in one process:
  inputs = "foreign" / ["foreign"] / null   MINE rc=None NO ARTIFACT (AttributeError)
                                            CODEX rc=1 artifact written
  windows / posix absolute KEY              MINE rc=1 artifact written PATH LEAKED
                                            CODEX rc=1 artifact written, clean
I kept every line: the empty-mapping view for the verdict-scope placeholders, the raw
`inputs` kept as evidence, the key scrubbing, the deterministic [redacted-key-N] handling.
MEASURED the collision path directly: three paths with one basename keep all three
members, values in order, byte-identical across repeat calls.

TWO SURVIVORS IN THE SWEEP OF CODEX'S REPAIR, characterised BY CONSTRUCTION:
  codex_key_collision_not_preserved   REAL COVERAGE GAP, NOW CLOSED BY MY TEST.
    Nothing constructed two keys collapsing onto one basename.  With the loop off the
    second member OVERWRITES the first: a field of the evidence record disappears with no
    error and no disclosure — a silent exclusion inside a record whose only job is to be
    evidence.  Codex's implementation is right; it had no test that could fail.
  codex_writer_stops_visiting_keys    redundancy on every SCRUBBED path, and the ONLY
    defence on the AUTHORIZED one.  That IS the second half of my finding, and the new
    gate is what makes it live.  After the refactor the equivalent mutation is
    s67_shared_predicate_stops_visiting_keys, and it is CAUGHT.
```

## THE STANDING X7 SCOPE, AS IT NOW READS

```text
APPROVED PLAN CONTENT IS STILL EMBEDDED VERBATIM AND STILL NOT SCRUBBED.  What changed in
  S67 is that a plan RECORDING an absolute path can no longer BE approved at the gate.
  *** CODEX RULED IN ITS S67: that does NOT reopen the accepted scope.  I TOOK THE
  RULING IN MY S68.  SETTLED -- reopening it ESCALATES rather than loops. ***
THE WRITER'S GUARD STILL ASKS WHETHER A STRING *IS* A PATH.  It cannot see a path inside
  prose, and it never will.  THE SCRUBBER, NOT THE GUARD, IS WHAT MAKES X7 TRUE — and as
  of S67 the scrubber's POST-CONDITION *is* the guard, so they cannot disagree.
  *** S69: `_records_absolute_path` is REGEX **or** PurePath, so the guard DOES see an
  embedded path — which is exactly why the two must be widened TOGETHER.  Tighten the
  guard alone and X7 fires while X6 is writing.  That coupling is what forces the
  single-slash POSIX gap (limitation 99) to be DISCLOSED rather than closed on one side. ***
  *** S70: the SAME COUPLING is what made the URI lookbehind a LEAK rather than a refusal.
  Because the guard shares the pattern, a shape the pattern declines is a shape the guard
  declines, so the artifact is written and the path is published.  A widening that keeps
  the two together is SAFE FOR X6 BY CONSTRUCTION — which is why the accept side (0
  offenders in all three of the tool's own documents) was measured before the change. ***
CODEX'S TWO NON-BLOCKING POINTS FROM S65 STAND AND I DID NOT TOUCH THEM: the decorative
  provenance inequality, and X1's recorded-but-unasserted reduced-run reconciliation.
```

## THE EXTENSION DOCUMENT — WHAT IT SAYS, AS AN INDEX ONLY

**READ `payload-boundary-extension-v0.2.md`. This is an index, not the document. It is
APPROVED AND FROZEN — a change needs a version bump and a `git mv`, never an edit.**

```text
THE FIVE S62 CODEX EDITS, ALL ACCEPTED AND ALL NOW IN FORCE:
 1 THE PROVENANCE PAYLOAD WAS CIRCULAR.  ScreenOverrides had FIVE fields and the fifth
   IS provenance_hash, so requiring all of them would have made the payload contain its
   own digest.  NOW: exactly the FIVE non-provenance inputs (probe peak, probe ramp,
   physical_faults as objects carrying every FaultSpec field BY NAME, realized_pair_id,
   mass); provenance_hash is derived FIRST and inserted AFTER hashing.
   *** NOTE: ScreenOverrides NOW HAS SIX FIELDS (Codex S63 added the mass).  The payload
   is still the five non-provenance ones — that is now literally "all but one". ***
 2 TWO STAGE ORDERS, the single most important structural change:
     PLAN MODE     X0P only.  0 rollouts.  Writes the plan on PASS **AND ON FAILURE**.
     EXECUTE MODE  X0E -> XR(1) -> XA(18) -> XM-C(48) -> XL(0) -> XM-B(<=60) -> XZ(0)
   X0E recomputes the plan and must match the SEPARATELY AUTHORIZED plan digest before
   XR may spend its rollout.  Only a plan with plan_valid=true may be named.
 3 THE ANCHOR CANNOT PROVE THE PAYLOAD SEAM IS LIVE.  Its source reservation
   scenario_dev_t01_f000_r02 ALREADY carries payload_dev_0p050kg = 0.05 kg, so a DEAD
   payload override still hands the anchor exactly the body it asked for.  The anchor
   controls the rebuilt PROBE/FAULT/IDENTITY instrument and NOTHING ELSE; X8 IS THE SOLE
   PAYLOAD-LIVENESS CHECK.  All six non-anchor healthy blocks + X8 run BEFORE any
   non-anchor ladder, so a dead seam costs 67 rollouts, not 127.
 4 THE RESULT SCHEMA CARRIES ITS JOINS AS DATA.  Every ladder row cites
   fault_physical_key AND healthy_physical_key; every null distance cites BOTH endpoint
   keys; logical_reference_census splits 532 into 70+70+392.  The REPLAY IS NOT A LEDGER
   ENTRY; extension / replay / total rollout counts are SEPARATE FIELDS.
 5 REDUCED COVERAGE LICENSES NOTHING.  R7 X_REDUCED_MASS_COVERAGE precedes every
   shape/case rule; R2 X_INVALID_MEASUREMENT added; the classifier is R0..R12.
X1 is a statement about the PLANNED partition with realized counts allowed to differ by
exactly the persisted exclusions.  The `physical_keys` digest recipe is pinned end to end
(form via physical_key_report, sort the report objects by their own canonical JSON,
canonical-JSON the ordered list, hash those bytes).

THE S63 FIX, NOW IN FORCE: Option B has ONE rule and R10 X_CASE_EMPTY states it
identically to R11 X_CASE_ROLE_LOST — the cap comes from an ascending-mass initial prefix
in which EVERY mass retains its OWN reserved role.  An empty TESTABLE_SET necessarily
breaks that prefix, so the R11 rule already covers the empty case.  The counterexample
and the counts went INTO §9.5.

*** THE MASS ORDER TRAP.  Option B and MONOTONE are stated over ascending MASS, and mass
order is NOT index order: 0.025(m1,pilot) 0.050(m0,dev) 0.075(m2,pilot) 0.100(m3,val)
0.125(m4,val) 0.150(m5,test) 0.200(m6,test).  Any executable or test that iterates `m`
gets the wrong prefix. ***

FOR THE STEP-2 BUILD, NOT A DOCUMENT CHANGE: X8 needs all 8 healthy vectors at all 7
masses, so a non-anchor mass excluded under X_UNSAFE_MASS MUST STILL FINISH ITS HEALTHY
BLOCK.  Forced in three independent places.  Say it in the executable's review anyway.
```

## THE ARITHMETIC OF THE EXTENSION — ALL RE-DERIVED S63, ALL CLOSE

```text
7 MASSES     0.050 (ANCHOR, already measured) + 0.025 0.075 0.100 0.125 0.150 0.200
CONTEXT      FIXED: env_dev_iso25c + contact_dev_none + t01 + probe 0.10 N / ramp 0.25
             = screen cell 6 in everything but payload mass and identity.
IDENTITY     CRN.  sensor_seed = 160000 + 1000*k + 2 ; pair_id basepair_payloadext_k{k}
             band [160002,167002].  EIGHT identities reused at EVERY mass.
             CLASS k=0  77 rollouts (7 masses x 11) ; CLASS k>=1  7 each => 126 over 8
LADDER       the same ten reserved remEI values, FIXED not adaptive
COUNTS       7*11 + 7*7 = 126 rollouts ; 18 per mass (8 healthy FIRST, then 10 ladder)
             7 + 70 + 49 = 126 DISTINCT PHYSICAL KEYS (needs the §3.2 mass field)
             10 + 10 + 56 = 76 logical refs per mass ; 76*7 = 532 = 70+70+392
             8 * C(7,2) = 168 X8 comparisons
EXIT COSTS   X0P/X0E 0 | XR 1 | anchor-healthy <=9 | anchor-ladder <=19 | X8 fail 67
             | full run 127 MAXIMUM | 53.1-58.2 min at 25.1-27.5 s/rollout
INVARIANTS   X1-X14 (X13 the physical key; X14 returns exactly one of R0..R12)
AUTHORIZATION  five steps in §13; none inferable from another.  Document approval
             authorizes ONLY Step 2.  Executable approval authorizes ONLY plan mode.
```

**THREE PREREQUISITES — ALL THREE NOW BUILT; TWO JOINTLY APPROVED, THE THIRD OPEN.** `ScreenOverrides` sixth field
(`assignment_generator.py`, S44 approved `1c565888`/`2ec96c9f`); `PhysicalKey` seventh field
(`protocol_p_results.py`, `e84e5f9f`/`cbac30ed`, 77 tests); the executable. Both verified
S63 by AST: `ScreenOverrides` = 5 fields with `provenance_hash`; `PhysicalKey` =
`(sensor_seed, pair_id, condition, severity, probe_peak_force_n,
probe_ramp_fraction_of_duration)`, **no payload field**.

## S62 FACTS ABOUT THE PLANT — STILL LOAD-BEARING, NOT RE-MEASURED S63

```text
(a) *** THE PLANT HAS NO GRAVITY. ***  cable_mechanics.py:101 emits gravity="0 0 0".
    Stepped at ctrl=0 for 3.0 s, ALL EIGHT MASSES: peak |gauge_true| = 0.0000 ue and tip
    radius EXACTLY 0.80000 m, 0.200 kg included.  => PAYLOAD IS PURE TIP INERTIA.
    No sag, no static load, no static consumption of the A1 envelope.
    Nominal body mass 0.172800003 kg.  Limitation 82.
(b) THE PROBE SITS ~97x BELOW THE LOWEST ELASTIC MODE (f1 77.34 Hz vs 0.8 Hz), so
    RESONANCE IS RULED OUT.  f1/f3/f5 do not move with mass at all; f2/f4/f6 move and
    SATURATE.  The S60 attenuation's MECHANISM IS UNIDENTIFIED.  Limitation 83.
(c) v0.1's ANCHOR WAS BUILT TO FAIL ON NOISE.  Cell 6 fails remEI 0.50 by 2.1% of its
    threshold.  v0.2 §9.3: tau_anchor = 0.10, constrain the NINE rungs at/above it, leave
    0.50 unconstrained.  ANY tau in (0.021, 0.196) gives the IDENTICAL partition.
    Fixed from PUBLISHED margins before any extension datum exists.
```

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
- I am **Claude**; last session was **Session 75**; next session I run is **Session 76**. **THE S72 PROGRESS REPORT** (`Progress Report Session 72.md`, covers S65–S72) **was read by Codex in its S72 general recent-work review, which found no correction to carry — so NO explicit review cycle opened on it** (the Working Method's rule: the review cycle does not apply to the general recent-work review until that review flags something). Next regular report: **Session 80**, or sooner if a phase transition or an approved written Claim-Sheet amendment fires. **An approved A2 fires it.** **A Step-5 run does NOT by itself fire one** — it is neither a phase transition nor an amendment, though the result it produces will feed A2, which does.
- **`config.json` is deliberately NOT frozen** and does not exist. All hashes are `dev-`; no `dev-` trace may enter confirmatory analysis.
- Real data exists: `data/gate3-base-dev-pilot-val-c1-s` (3.86 GB, git-ignored, local only). 472 reservations / 944 manifest rows / C1+S / dev 152, pilot 152, val 168. **Test untouched: 0 identities, 0 payloads.** **THE "SLATED FOR FULL REGENERATION FROM ZERO AFTER A2" EXPECTATION IS RETIRED AS OF MY S75 — see A2.3.** Option C inserts no severity, so no seed ordinal shifts and A2 by itself invalidates none of this. If the set is ever superseded it is for some other reason, under its own authorization. **Still: read them, do not build on them** — nothing downstream of them is authorized either way.
- **THE PAYLOAD-BOUNDARY EXTENSION HAS RUN — Codex's S73, 127 physical rollouts, `X_CASE_EMPTY`, and the result artifact is JOINTLY APPROVED (Codex S73 / me S74).** The measurement is spent and no further payload-extension execution is authorized. **A2 IS DRAFTED (my S75) AND IN AN OPEN TWO-FILE REVIEW LOOP; CODEX OWNS THE NEXT TURN.**
- **STAGES A/B/C HAVE RUN — Codex's S57, 135 physical rollouts, CASE_B, JOINTLY APPROVED.** Stage 0 RAN in S48 at ZERO rollouts; `results/protocol_p/sensor_only_difference_null.json` is tracked and **JOINTLY APPROVED**. The §9 role-coverage read is now **JOINTLY APPROVED** (above). The payload read's **RESULT ARTIFACT is JOINTLY APPROVED** (S60 Codex / S61 me); its **script + tests are JOINTLY APPROVED (Codex S61)**.
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
NOT RUN IN S58-S72.  Nothing on the gate's watched path changed and the measurement it
guards was already spent.
+ Codex S73: THE ONE AUTHORIZED STEP-5 INVOCATION.  1 replay + 126 extension = 127,
  3,680.708815 s persisted.                                =>   TOTAL 278
*** TAKE THE COUNT FROM THE ARTIFACT'S OWN LEDGER, NEVER FROM A PER-ROLLOUT FIGURE. ***
MY S74 SPENT ZERO — the whole audit is a read of persisted fields.
MY S75 SPENT ZERO — drafting only; no plan mode, no replay, no execute mode.
```
- **Progress report DONE at S64** (regular, covers S57–S64) at `agents/Claude/Progress Reports/Progress Report Session 64.md`. **ITS LOOP IS OPEN AT MY S65 STATE `b0ff7496`** — Codex made two edits in its S64 (the ledger refuses a duplicate LOUDLY, not silently; and "151 rollouts, about 70 minutes" contradicted my own line 14's audited 4,432.16 s), I verified both against primary records and accepted both diagnoses AND implementations, then moved one clause out of the present tense (+4/-3) because "still cannot run until payload mass is part of the key" stopped being true in S63/S64. **Codex owns the next turn on it; I offered to take its wording.** Prior status — the S56 one ran five review rounds, so expect Codex may open one. `Progress Report Session 56.md` (S49–S56) stays closed at blob `83c527ce…`; do not reopen it. **THE S72 REGULAR IS WRITTEN** — `agents/Claude/Progress Reports/Progress Report Session 72.md`, covering S65–S72. **Codex read it in its S72 general recent-work review and found no correction to carry, so no explicit review cycle opened on it.** Its spine: eight complete adversarial rounds on one program, every round finding something real and each structurally below the last; then the loop closing and the program producing the zero-rollout plan. It states both halves of the trade — what the rounds bought, and that eight of my sessions produced no science — and names where I think the cost stopped being obviously worth it. **MY NEXT REGULAR IS SESSION 80.**

## Escalation trigger — content-based, and it has now held ten times

**The binding rule: escalate to the director when a round re-litigates a point already
settled, or when we disagree on a judgment neither of us can resolve from source — NOT
when a round finds a new, verifiable defect.** Every loop to date closed on new findings:
the specification loop (seven rounds), the seam, the replay gate, Stage-0 implementation,
the Stage-0 result, the progress report, Step 24, the public log, the extraction and
construction layers, the driver (blocked S54, corrected S55, approved S55), the S56/S57
round, and **the role-coverage loop (blocked S58, corrected S59, approved S59, closed at
the same state S60)**.
**THE EXECUTABLE LOOP WAS THE LONGEST YET — EIGHT FULL ROUNDS
(S64→S65→S65→S66→S66→S67→S67→S68→S68→S69→S69→S70→S70→S71→S71) AND IT IS NOW CLOSED.** It never tripped the trigger, and the reason is worth stating so a future
session does not escalate on count: every round accepted the previous round's findings in
full and blocked on NEW measured evidence, each time one structural layer below the last
(exception handling → container type and key position → the predicate itself → what the
predicate is applied to → what the repair does to the message → what the rule does to a
path that is not alone on the line → what the rule does to a path that follows a
letter-colon, i.e. the URL/UNC ambiguity → whether a scheme name is a complete TOKEN or a
suffix → **and finally, in S71, not behaviour at all but what the TESTS can see**).
**THE S69 JUDGMENT IS SETTLED: Codex agreed in its S69 that disclosing the single-slash
POSIX gap beats corrupting `dev/pilot/val`. THE SCHEME WHITELIST IS ALSO SETTLED: Codex
accepted the list and `file` staying off it in its S70, and I accepted its token-exactness
repair in full in my S71. If the NAMES come back contested, ESCALATE — that is exactly
the shape the rule is for.**
**S71 WAS THE FIRST ROUND THAT FOUND NO BROKEN BEHAVIOUR, AND IT WAS THE LAST ROUND.** Its
three findings were all "correct code with nothing guarding it," demonstrated by mutation
rather than by a failing test, with the executable AST unchanged — and I wrote down that
this was plausibly where the loop ends. Codex approved next turn and it did. **Carry the
heuristic: a round that finds only coverage is the signal to close, not to hunt for one
more.** **The S67 authorization-gate
question is SETTLED**: Codex ruled in its S67 that the gate's refusal does not reopen
the accepted "embed approved content verbatim" scope, and I took that ruling in my
S68 rather than re-arguing it. **If a later round reopens THAT, or reopens the
discard-versus-truncate choice, it escalates rather than looping.**
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

**The (a)–(ii) driver requirements, carried verbatim in shape:** (a) `ood_flag` exclusion from known-class metrics; (b) the **degradation-ladder rule** (S30/S31); (c) **pilot→val moves one variable while val→test additionally moves half-fraction → complete factorial** — *and, under A2 pin 4, no longer moves the contact window*; (d) S33's two findings; (e) the mild-stratum development diagnostic **at its true scope** and the per-channel attribution; (f) **[S35]** the excitation discontinuity; (g) **[S36]** the yardstick discontinuity (D) + the run-to-run range statement (E) + trajectory-partial margin coverage; (h) **[S37]** the operation mismatch (F), thermal near-invariance (G) as a *property*, the amplitude ceiling (H); (i) **[S38]** the **window origin (J)** — the driver MUST use the same origin the protocol pins — plus the matched/unmatched asymmetry and role-coverage counts; (j) **[S39]** the **construction path (K)** and the **unmatched-identity confound (L)**; (k) **[S40]** distinguish **`base_pair_id` from realized `pair_id`** in every identity join, and never stamp an overridden run with the base config hash; (l) **[S41]** any file whose **raw bytes** enter an identity must be hashed through the correct-domain helper; (m) **[S42]** that helper must be chosen **by file domain**; (n) **[S43]** every identity expression must **name the object it hashes**; (o) **[S44]** test the **wires between stages**, not only each stage; (p) **[S45]** every clean report must **disclose its denominator** and refuse to report when it cannot support the claim; (q) **[S46]** every guard must be **reachable from the construction that will run**, and every fixture large enough for the defect it exposes; (r) **[S47]** every pinned literal that also lives in a bound document is checked by EQUALITY, never adoption; (s) **[S48]** every test that claims to verify a gate must CALL it and assert the REASON for a refusal; (t) **[S50]** every documented dependency must be verified against the running system; (u) **[S51]** assert a phrase UNIQUE TO ONE RAISE SITE, and construct preconditions through `utils/protocol_p_conditions.py`; (v) **[S52]** obtain the source reservation from the I1-pinned assignment and never construct one, and test per BRANCH not per guard; (w) **[S53]** record a REUSED row's provenance by CITATION, and DERIVE the fault onset; (x) **[S54]** key the results table on the PHYSICAL BODY, and make every clean-census check reachable from a state that could fail it; (y) **[S55]** derive the reported set from what was MEASURED rather than from which candidates survived, CONSUME the hard-gate report in EVERY stage, and persist the gate evidence, step count and elapsed time on EVERY exit path including terminals; **(z) [S56]** every check the driver makes must be given a source INDEPENDENT of the thing it checks — a comparison whose two sides are produced by the same function from the same arguments is a report of a check rather than a check — and no result artifact may record an absolute filesystem path; **(aa) [S57]** every count must distinguish OCCURRENCES from IDENTITIES — 180 provenance references over 168 distinct stamps, never "180 stamps" — and every historical figure must be re-derived from primary records; **(bb) [S57]** no outcome case may be reported until the healthy-vs-faulted readback has distinguished a measured null from an override that never reached the plant; **(cc) [S59]** every digest a result artifact records must be taken in the domain of the file's KIND — canonical for tracked text, raw only for binary — and every check a review ADDS must have a committed test that constructs the state it refuses; **(dd) [NEW S60]** every verdict the driver reports must name the CONTEXT POPULATION it was established over, because a conjunction over context cells is a statement about exactly those cells and the confirmatory splits are not drawn from them — and no coverage count computed from those verdicts may be presented as a statement about a split's own contexts; **(ee) [NEW S61]** every refusal message must be unique to one raise site **as rendered**, not as written — a message assembled by an f-string can duplicate a literal one exactly, which no text search of the file will find, so the check is a runtime comparison of the sentences the sites actually emit. **(ff) [NEW S62]** every guard must be checked against what ELSE in the design produces its passing signal — a distinctness check over units that already differ for another reason certifies nothing — and after any change to what the design holds fixed, every downstream key, join and dedup must be re-asked what it was actually distinguishing, because a key is a claim about what makes two things different and the design just changed that claim. **(hh) [NEW S65]** every branch that reports a cost must read that cost from the object that incurred it — a handler reading a sibling handler's locals reports a number no run produced, or crashes — and every exit that a specification says must persist evidence needs a test that DRIVES that exit, because the exit paths of a CLI are the region no unit test enters. **(gg) [S64]** an additive field is only additive where something can **produce** it — after adding a field to a type, name every PRODUCER of that type and check each one passes the new input, because adding it to the type, its factory and its serializer covers every place the object is consumed or rendered and none of the places it is built. **(ii) [NEW S66]** a rule that FORBIDS content in an artifact must never be able to stop the write that rule's own specification REQUIRES — when one invariant refuses and another compels, name the exit where they meet and drive it, because the refusal fires while writing the evidence and destroys exactly the record it was protecting; and every value a failure artifact records must be validated for shape BEFORE it is recorded, not by the check that runs one exit later. **(jj) [NEW S67]** when one routine exists to make another routine's check pass, the first must END BY ASSERTING THAT CHECK rather than enumerating the cases it expects — a list of spellings and a predicate disagree on inputs nobody enumerated, and the disagreement surfaces as the destroyed artifact; and where a gate embeds content verbatim on the strength of a premise about where that content came from, the premise is a thing to CHECK at the gate, not to assume, because refusing is not the same act as rewriting. **(kk) [NEW S68]** a routine that REWRITES a persisted message must be run to a fixpoint, because one rewriting rule can BUILD the pattern another rule has already been offered and declined, and the state that leaves behind is one no reduction can repair — so the only exit left discards the record the rule existed to protect; and a fixture must be placed where the value it carries actually reaches the code under test, because an artifact writer copies named members rather than whole documents, and a bad value outside those members exercises nothing. **(ll) [NEW S69]** a rule that recognises a value must be checked against every way that value can appear IN COMPANY, not only alone — a cross-product of renderings against the characters that can precede and follow them is a different instrument from a list of examples, and it is the one that finds the family rather than the instance; and where the rule cannot be widened without corrupting the project's own vocabulary, the answer is a DISCLOSED limitation with a test that pins it, not a silent gap — because a scrubber's accept side is where damage is invisible, and because the guard that shares the rule must not be tightened alone. **(mm) [NEW S70]** where two things cannot be told apart by shape, the rule that separates them is a decision about NAMES and must be written as an explicit, tested, disclosed list rather than hidden inside a pattern — a lookbehind saying "any alphanumeric followed by a colon" is a naming decision nobody would have approved if it had been stated out loud; and after any change to which rule REACHES an input, re-run the mutation sweep before trusting the suite, because a test whose input is now handled by a different rule still passes and no longer guards anything. **(nn) [NEW S71]** a test parametrized OVER a constant is a statement about whatever that constant says and is therefore blind to the constant itself — where the constant IS the decision, it must additionally be pinned by EQUALITY, because dropping or adding a member changes what the program permits while the parametrization merely yields a different number of passing cases; and the accept side of any rule must be tested at every boundary its own contract names, not only at the one boundary the first example happened to use, because a probe that measures a boundary matrix and a committed test that pins one are different artifacts and only the second survives the session that measured it. **(oo) [NEW S73]** where a check brackets an expensive irreversible operation with a whole-tree invariant, that invariant is a COST rather than a check — it runs after the spend, so anything it can notice destroys what was spent — and therefore: read the bracket's watch list before authorizing the spend and say what is NOT filtered out of it, run every check that sits BELOW the spend in the same routine before authorizing rather than in exchange for it, and name the residual that no measurement can close (a concurrent writer) as an operational rule instead of pretending the measurement covered it; and an authorization is worth exactly what the gate reading it is worth, so drive that gate directly against the exact bytes and their neighbours before naming a digest, and record the SECOND layer that covers the first layer's gap and what that layer costs.

**Order:** (1)✓ → (2 foundation)✓ → (2 role-write)✓ → (3 assignment)✓✓ → (2 generator + base roles)✓✓ → (2 hardening)✓✓ → (dev separability check)✓ **[NEGATIVE]** → Protocol P v2.3.3 spec ✓✓ → seam + 37 tests ✓✓ → replay gate ✓✓ → Stage-0 implementation ✓✓ → **Stage 0 RAN, S48 ✓** → Stage-0 result ✓✓ → Progress Report S48 ✓✓ → packet Step 24 ✓✓ → public README ✓✓ → extraction + construction layer ✓✓ (S51–S53) → driver + results layer (S54 built, S54 blocked, S55 corrected, S55 approved ✓✓) → S56 pre-registered helper + Step 25 ✓✓ → **Codex S57: replay gate (36.42 s) then STAGES A/B/C — 135 rollouts, CASE_B ✓** → **my S58: every number independently reproduced, result APPROVED; §9's role-coverage read found UNIMPLEMENTED and built at zero rollouts — dev 0 / pilot 0 / val 1 / test 1** → **Codex S58 BLOCKED it on three real findings and corrected it** → **my S59: all three CONFIRMED; a FOURTH found in the repair (raw-domain digest of a tracked text file); 23-case sweep, 13 survivors, 12 real, closed with 12 tests** → **Codex S59 APPROVED all four states and held the loop open for my explicit approval** → **my S60: approval posted, LOOP CLOSED AT THE SAME STATE; the mutation-sweep harness found to give false verdicts and fixed; the approved analyzer re-swept clean (28/28); the payload-conditioning read built at zero rollouts** → **Codex S60 blocked the payload read on two real defects, corrected them, ruled MEASURE FIRST via a separate development-only pre-registration, and blocked A2** → **my S61: both findings confirmed independently; the result artifact and both READMEs approved at Codex's states; the sweep over Codex's repair found a SILENT GAP in one of its own new guards and a three-way message collision one copy of which is built by an f-string; script+tests returned at new blobs; the payload-boundary extension v0.1 DRAFTED** → **Codex S61 APPROVED the analyzer/tests (loop CLOSED) and BLOCKED the extension on four findings** → **my S62: all four confirmed against primary sources, none contested; v0.1 `git mv`'d to v0.2 and rewritten — CRN across masses, a SECOND prerequisite (`PhysicalKey`), one ordered exhaustive classifier, pinned artifact/provenance contracts, the anchor staged first; plus three findings of my own (zero gravity, probe 97x below the lowest mode, a noise-fragile anchor)** → **Codex S62 made FIVE direct edits to v0.2 and approved its own state `e5192eaa` — circular provenance payload, plan/execute split, the anchor cannot prove payload liveness (its source reservation already carries 0.050 kg), result joins as data, reduced coverage licenses nothing** → **my S63: all five accepted, three verified at source; ONE NEW DEFECT found in Codex's own new text — R10 `X_CASE_EMPTY` kept the weaker Option-B rule Codex had just tightened at R11, and over all 19,448 states DELETING a result raised the licensed cap in 3,185 of them; fixed by unifying the rule (0 remain), state returned at `538ae06b`** → **Codex S63 APPROVED `538ae06b`, CLOSING THE DOCUMENT LOOP, then built two of the three Step-2 prerequisites and approved its own four-file state** → **my S64: both of Codex's changes verified with my own 10-case two-pass sweep (10/10 caught, 0 survivors); ONE defect found — `PhysicalKey` gained the payload field while `LogicalRow.physical`, the ONLY producer of a key in that module, could not set it, so the extension's 126 rollouts resolved to 18 keys; fixed additively; four-file state approved at `b7b2430a`/`c23e61d3`/`2f7c33b2`/`ad6b32fe`** → **my S65: Codex's executable could not have completed ONE execute run — wrong replay reservation, `UnboundLocalError` in the XR handler, an exception class outside the measurement handler; five corrections, state returned at `ff0cdbe6`/`ebdfdf83`** → **Codex S65 accepted all five including the `resolve_replay_source` extraction, found TWO more real X6/X7 exits, corrected them, approved `eb94afb2`/`5d8dd369`, and closed my progress-report loop at `b0ff7496`** → **my S66: both of Codex's findings accepted in full; FOUR MORE defects found by RUNNING — X7's writer guard destroying the X6 record on the wrong-plan exit, the same crash reachable through Codex's brand-new missing-argument exit, `//host/share` surviving both scrubbers, and my own S65 Windows regex eating every URL — plus two silent execute exits and an untested branch; state returned at `431d9c08`/`4d194a67`** → **Codex S66 accepted all four, found TWO more — a non-object `inputs` field crashing `execute_document_skeleton` while assembling the failure record, and an absolute path used as a JSON MEMBER NAME surviving both the scrubber and the writer — corrected both and approved `86fc3fdb`/`e081a26d`** → **my S67: both reproduced against my own blob and both implementations kept unchanged; a THIRD family found by ENUMERATION rather than reading — the scrubber is a list of spellings and the writer's guard is a `PurePath` predicate, and they disagreed on 1,358 of 37,448 strings (bare roots; drive letters `PurePath` accepts and `[A-Za-z]` does not), nine of which killed the write through `main()`; fixed by making the scrubber's post-condition BE the guard, run to a fixpoint; plus the authorized path closed at the gate by a refusal rather than a rewrite; state returned at `5a5b0562`/`f2f5031d`** → **Codex S67 accepted all three, ruled that the authorization-gate refusal does NOT reopen the verbatim-embedding scope, found THREE more execute-exit shapes — a real Windows path glued onto prose with no delimiter, values `json.loads` accepts that canonical JSON cannot represent (`1e9999` -> `inf`, a lone surrogate), and a foreign plan too deeply nested for the recursive visitors — and approved `25386e27`/`ab4ddfc0`** → **my S68: all three accepted and kept unchanged, with a SCOPE CORRECTION on two (the unserializable values only reach the writer under `inputs`/`protocol`/`plan`, and the recursion threshold is a property of the CALLER'S stack, not of this file — measured at two ambient depths); ONE NEW DEFECT found in the repair itself — dropping the drive-letter token boundary made a state reachable where the post-condition discards the WHOLE reason, measured on three realistic sentences and 6 of 37,448; fixed by running the substitutions to a FIXPOINT; state returned at `04ec936e`/`4979af07`** → **Codex S68 accepted all of it and found ONE more — the embedded-path regex accepted a narrower drive alphabet than the file's own declared `PureWindowsPath` semantics, so an embedded `1:\…` was published — corrected it and approved `9cd10305`/`ce0cd642`** → **my S69: that finding reproduced (82 leaking renderings of 286 under my blob, 34 under Codex's, 0 under the state I returned) and every line of its repair kept; FOUR MORE found by a CROSS-PRODUCT rather than a reading — a UNC path glued to prose published whole, a path CONTAINING A SPACE reduced only to its first space-free run (this repo's own parent has a space), a mixed-separator span whose reduction kept the parent directory, and the single-slash POSIX form glued to a word, which I DID NOT FIX and disclosed instead because closing it turns `dev/pilot/val` into `val`; state returned at `9fd723b0`/`191d9b4d`** → **Codex S69 accepted all four and the single-slash judgment, changed NO operational expression (executable AST identical, which I verified), and corrected the DISCLOSURE — it was narrower than the measured behaviour, because a space-containing forward-drive, forward-UNC or mixed-separator path also leaves a relative private suffix — approving `f2d9f3b1`/`eb10bb23`** → **my S70: every word of that kept, and a NEW defect found by widening the grid where it was thinnest (a prefix ending in a letter-colon) — `reason://host/PRIVATE/row.npz` was published BYTE-IDENTICAL because the forward-UNC lookbehind read "any alphanumeric + colon is a URI scheme", and the writer's guard shares the pattern so it declined too; eight more cells kept the DRIVE DESIGNATOR; repaired by NAMING the protected schemes (`file` deliberately off the list) and by having the forward-slash drive form refuse a second slash, at zero measured prose cost, with the converse cost disclosed and pinned; the sweep also caught that my own repair had made `_final_component`'s both-separator split untestable; state returned at `c7451068`/`485dcc3d`** → **Codex S70 accepted both diagnoses and the whitelist judgment and found ONE more — my per-name lookbehind matched a listed scheme as the SUFFIX of a longer unlisted token — approving `c850a4b6`/`150870f4`** → **my S71: every line kept and NO operational expression changed (verified AST-identical), and THREE COVERAGE GAPS found by MUTATION rather than by a red check — `_URI_SCHEMES` was adopted by its own parametrized tests so adding a scheme leaked silently, the accept side was only ever tested at a space or at start-of-string, and one of my own disclosures misstated its measured behaviour; 18 cases added, state returned at `95040d93`/`0d7b68fc`** → **Codex S71 ACCEPTED ALL THREE AND APPROVED THOSE EXACT BYTES — the eight-round loop CLOSED, and STEP 2 with it** → **my S72: STEP 3 run, plan mode only, 0 rollouts, `plan_valid=true`; every load-bearing number re-derived from the artifact's own published fields without importing the executable; artifact APPROVED and the second read handed to Codex** → **Codex S72: the second independent read, 35 checks, anchor rebuilt from the committed screen result, 126/126 keys reproducing the published digest — SAME BYTES APPROVED, so STEP 3 IS COMPLETE** → **my S73: the whole §3.3 pre-rollout surface audited at ZERO rollouts (14/14, including the two checks that sit BELOW the rollout in the gate), the authorization gate driven directly (14/14), the ephemerality bracket measured (0 of 3,203 watched files change across a warm plan run) and its one uncloseable residual named — a CONCURRENT WRITER — and MY HALF of the Step-4 execution authorization issued with its scope pinned ← WE ARE HERE** → Codex issues the other half (same scope) → **the authorization is IN FORCE and Step 5 RUNS ONCE** → both audit the result → written amendment A2 + replacement assignment (both approve) → **full regeneration from zero** → re-audit → (4/5 models+calibration) [me] → (2 remaining roles) [Codex] → (6 controller + sample-size) [shared] → **joint immutable freeze** → one-shot confirmatory generation + eval (7) → Phase 3.

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

85. **[NEW S63] A CLASSIFIER CAN BE EXHAUSTIVE AND STILL LICENSE INCONSISTENTLY.** The extension's outcome rules were verified complete over all 19,448 reachable states — by Codex, correctly — and two mutually exclusive branches still granted different Option-B authority for the same evidence, because only one of them had been tightened. In 3,185 states **deleting the heaviest mass's result raised the licensed cap**, worst case 0.025 → 0.150 kg. **Exhaustiveness is a property of the partition; licensing is a separate property of each cell, and the check that establishes the first says nothing about the second.** Fixed by stating the rule once. Any future edit that re-splits an outcome rule owes the same enumeration.

86. **[NEW S64] `LogicalRow.physical` WAS THE ONLY PRODUCER OF A `PhysicalKey` IN THE RESULTS LAYER, AND IT DROPPED THE NEW PAYLOAD FIELD.** Measured: the extension's 126 rollouts, built as logical rows in the CRN shape, resolved to **18** distinct keys. Fixed in S64 by threading the mass through `.physical`; `.key` is deliberately untouched and the class docstring says why. **Two scope statements travel with it and must not be dropped: it failed LOUDLY (`ResultsLedger.record` refuses a duplicate key, and `ledger.has()` has no call site in `scripts/` at all), and Codex's build satisfied §3.2's bullet list exactly — what was missing was the property §3.2 gives as the REASON for the field.** Also carried: `ResultsLedger.record` only accepts `stage_of_origin in ("A","B","C")` and `require_inventory_shape` hard-codes 180/168/12, so the extension needs its own ledger and its own census shape. **No write-up may say the results layer's census checks the extension's counts.**

87. **[NEW S65] AN EXECUTABLE CAN BE COMPLETE, TESTED AND UNRUNNABLE.** Codex's payload-boundary executable implemented §§4–12 faithfully, passed 36 focused tests, a 17-case sweep and 1,172 packet tests, and **could not have completed a single execute run**: it verified itself against the wrong delivered simulation (a re-typed `scenario_dev_t00_f000_r00` against the approved gate's exported `t01`), and when that check failed the handler raised `UnboundLocalError` and wrote no artifact. **Both defects were invisible to every instrument either agent uses** — they are not in any function a unit test calls; they are in `main()`'s exit paths. **No write-up may present a suite count, a sweep result, or a synthetic end-to-end audit as evidence that a CLI runs.**

88. **[NEW S65] `ResultsLedger` AND `require_inventory_shape` STAY PROTOCOL-P-ONLY, AND THE EXTENSION NOW OWNS BOTH.** `ExtensionLedger` accepts the XA/XM vocabulary and the executable carries its own 126/532 census. **No write-up may say the results layer's census checks the extension's counts** — it cannot, and it was never asked to.

89. **[NEW S65] THE ARTIFACT'S ABSOLUTE-PATH GUARD ASKS WHETHER A STRING *IS* A PATH.** No refusal sentence is one. `'ProtocolPError: pinned input is absent: C:\\Users\\...'` passes; `'C:\\Users\\...'` alone is refused. The fix is a scrubber at the point the reason is FORMED plus a test on the WRITTEN artifact — **not** a stronger writer guard, which would block the terminal write X6 requires. **The scrubber does not cover a bare POSIX-rooted path inside prose** and its docstring says so; on a POSIX host that gap is live.

90. **[NEW S65] THE CELL-6 ANCHOR PINS ARE THE DOCUMENT'S 6-DECIMAL VALUES, NOT THE SCREEN ARTIFACT'S.** Measured deltas 3e-8 to 5e-7 against `stage_abc_screen.json`; **no margin sign flips**, so the anchor's verdict comparison is unaffected and `tau_anchor`'s partition is unchanged. But the extension's artifact publishes `cell_6_margins` as the screen's own margins, and a reader joining the two files finds them unequal in the 7th decimal. Now checked by a test at 6 dp with exact sign agreement. **Any sentence quoting these as the screen's values must say "to six decimals".**

91. **[NEW S66] ONE INVARIANT CAN DESTROY THE EVIDENCE ANOTHER INVARIANT REQUIRES.** X6 says every execute exit persists §11.2's field set; X7 says no artifact records an absolute path, and it is enforced by a writer guard that RAISES. On four exits the second fired while writing the first, so the program died with a traceback and persisted nothing — including on the exit Codex added in the same session precisely to satisfy X6. **No write-up may say the executable persists an artifact on every execute exit without naming the states that were driven to establish it.** The fix is a scrubber plus a shape check at the point of recording, not a stronger writer guard; a stronger guard would block the terminal write X6 compels.

92. **[NEW S66] `//host/share` IS ABSOLUTE TO BOTH `PurePath` FLAVOURS AND WAS SCRUBBED BY NEITHER.** The backslash UNC form was always caught; the forward-slash form never was, and the `(?!/)` that keeps URLs safe is exactly what let it through. Standing alone it crashes the writer; inside prose it is published. **The scrubber, not the writer's guard, is what makes X7 true** — the guard reads whole strings and no real refusal sentence is one.

93. **[NEW S66] MY OWN S65 WINDOWS SCRUBBER ATE EVERY URL.** `[A-Za-z]:[\\/]` matches a scheme separator, so `https://example.org/spec` became `httpspec`. Measured with each regex in isolation. A false positive in a scrubber does not leak a path — it silently corrupts a persisted reason, which is worse than a truncated one because the reader cannot tell. **Any claim that the scrubber leaves prose alone must be a runtime comparison over a battery, not a reading of the pattern.**

94. **[NEW S67] THE SCRUBBER AND THE WRITER'S GUARD DISAGREED ON 1,358 OF 37,448 ENUMERATED STRINGS.** The scrubber recognised a list of path SPELLINGS; the guard asks `PurePath` a PREDICATE. Two families sat in the gap and neither is exotic: a bare root (`/`, `//`, `///`, `/ x`), where no component follows the separator so no pattern can match, and a drive letter `PureWindowsPath` accepts while `[A-Za-z]` does not (`1:\dir\row.npz`, `.:\dir\row.npz`) — real paths with real directory portions. Nine such shapes, driven through `main()`, returned `rc=None` and left the output directory empty. Fixed by making the scrubber END with the guard's own predicate, run to a fixpoint; measured 0 of 37,448 afterwards. **No claim that a scrubber makes a guard true may rest on reading its patterns; it is an enumeration or it is nothing.**

95. **[NEW S67] AUTHORIZATION MEANT ONLY "THE OPERATOR NAMED THIS DOCUMENT'S DIGEST", WHICH ANY DOCUMENT SATISFIES.** Everything past `require_authorized_plan` embeds the plan verbatim by a decision both agents made deliberately, and that decision rested on the premise that plan mode's writer refuses absolute paths. The premise HOLDS (measured), but nothing checked that the named plan came from plan mode. A foreign plan carrying an absolute path, named by its own digest, passed authorization and then killed the terminal write. Closed at the gate by a REFUSAL, which routes to the scrubbing exit — not by a rewrite of approved content, which stays forbidden. **`config.json`'s eventual freeze has the same shape: a digest names a document, it does not certify its origin.**


96. **[NEW S68] A REPAIR TO A SCRUBBER CAN MAKE IT DISCARD THE WHOLE MESSAGE.** Removing the
    token boundary from the backslash drive form was correct and made a state reachable that
    was not before: the POSIX rule reduces `/plant/\row.npz` to `\row.npz` and re-emits it
    after the boundary character, rebuilding `C:\row.npz` inside prose the Windows rule had
    already declined. The whole string is then relative, so `PurePath.name` has nothing to
    take and the post-condition replaces the entire message with `<path>`. Measured on three
    realistic sentences and on 6 of the 37,448 enumerated strings. **It defeats neither X6 nor
    X7 — the artifact is written and no path leaks — it destroys the REASON, which on a failure
    exit is the whole record.** Fixed by running the substitutions to a fixpoint. **No claim
    that a scrubber "leaves prose alone" may rest on the accept side of a battery; the
    destruction case looks like a clean output.**

97. **[NEW S68] TWO OF A REVIEWER'S THREE FINDINGS WERE REAL AND NEITHER REPRODUCED AS
    REPORTED.** The unserializable-value defect only reaches the writer when the value sits
    under `inputs`, `protocol` or `plan` — the three members `execute_document_skeleton`
    copies — and it was demonstrated with the value under `"x"`, where the pre-fix code
    writes a perfectly good artifact. The recursion defect is real but "990 nested arrays" is
    a property of the AMBIENT CALL STACK, not of this file: measured at `+0` extra frames the
    pre-fix blob survived depth 960, and at `+300` frames it lost the artifact at 800.
    **A finding can be right while its demonstration is wrong, and the two must be separated
    before either is acted on.** Also measured, and worth carrying: a failed
    `Path.write_text` leaves a **zero-length file**, so "the artifact exists" is not the same
    check as "the artifact is readable."

98. **[NEW S69] A PATH CONTAINING A SPACE WAS ONLY HALF-SCRUBBED, AND THIS MACHINE'S OWN
    PROJECT DIRECTORY CONTAINS ONE.** The match's character class stopped at whitespace, so
    the substitution saw only the first space-free run and re-emitted everything after the
    space: r"D:\My Data\PRIVATE\row.npz" became r"My Data\PRIVATE\row.npz". Paths under
    `REPO_ROOT` are covered by the `<repo>` replacement; a sibling directory or the `D:`
    data drive was not. **It does NOT violate X7 as written** — the residue is relative, the
    guard passes and the artifact is written — it violates the scrubber's stated
    final-component contract and the reason X7 exists. Fixed by letting the tail cross a
    space only when a backslash lies ahead of the next whitespace. **One input still
    over-consumes and is named rather than hidden: r"C:\a\row.npz a\b" -> "b".**

99. **[NEW S69] THE SINGLE-SLASH POSIX FORM GLUED TO A WORD IS PUBLISHED, AND THAT IS A
    DECISION.** `"opaque-prefix/PRIVATE/row.npz"` and `"/mnt/My Data/PRIVATE/row.npz"` are
    recorded as-is. Closing it means matching a lone `/` after an ordinary character, which
    measured against this project's vocabulary turns `dev/pilot/val` into `val`, `C1/S` into
    `C1S` and `1/2` into `12`. Disclosed in the docstring, pinned by a test, and symmetric
    on purpose: the writer's guard shares the pattern, so it does not refuse those spellings
    either — tighten one side alone and X7 fires while X6 is writing the record. **This is a
    judgment and it is the one place the escalation trigger could plausibly fire.**

100. **[NEW S69] THE MUTATION SWEEP'S VERDICT MUST CARRY NOTHING THAT VARIES BETWEEN
    PASSES, AND I BROKE THAT AGAIN.** I embedded pytest's elapsed time in the verdict, so
    the two-pass detector reported a disagreement on every clean case — a detector that
    fires always is a detector that says nothing. My own S65 notes carry this exact warning.
    A second case came back BAD ANCHOR purely from an indentation mismatch. **Both are
    harness results and both were reported beside the corrected run; a sweep number is worth
    exactly what its harness is worth.**

101. **[NEW S70] A COMPLETE ROOTED PATH WAS PUBLISHED BECAUSE A URL AND A UNC PATH ARE THE
    SAME SHAPE.** `reason://host/PRIVATE/row.npz` came back byte-identical from the
    scrubber, and the writer's guard — which shares the pattern on purpose — declined too,
    so the artifact was written with the host, the private directory and the file name
    intact. The cause was a lookbehind that read "any alphanumeric followed by a colon is a
    URI scheme". **Once the scheme prefix is stripped, `//host/share` and
    `//example.org/spec` are lexically identical, so no boundary rule can separate them and
    a NAME-BASED decision is unavoidable** — the only honest form of it is an explicit list
    of protected schemes (`http, https, ftp, ftps, sftp, ssh, git`), with the converse cost
    disclosed: an unlisted scheme's `//` form is reduced like a path. `file` is deliberately
    off the list because `file://host/share` **is** a path. Reachability was NOT
    demonstrated through this file's own message shapes — it has no `":{...}"` f-string —
    and the finding was reported at that scope: reachable from `str(exc)`, foreign content,
    and any future message.

102. **[NEW S70] MY OWN REPAIR MADE AN EXISTING GUARD UNTESTABLE, AND ONLY THE SWEEP SAW
    IT.** Dropping the token boundary from the forward-slash drive form meant the Windows
    rule now consumes `r"opaque-prefixC:/PRIVATE\plant\row.npz"` — the only committed case
    exercising `_final_component`'s both-separator split. The test still passed, for a
    reason unrelated to what it checks, and deleting the split survived the entire focused
    suite. **A test's input is part of its contract: change which rule reaches that input
    and the test can become vacuous without changing a line of it.** Closed with a case
    carrying no drive letter, so only the POSIX rule can match it. Fourth consecutive
    session in which the defect lived one layer below the layer being fixed.

103. **[NEW S74] THE PAYLOAD BOUNDARY'S *EXISTENCE* IS ESTABLISHED; ITS *LOCATION* IS NOT.**
    `X_CASE_EMPTY` is robust — 0.200 kg is empty by ≥22.6% of its own threshold, and no
    single rung flip reaches R11. The **named** empty set `{0.150, 0.200}` is not: it rests
    on `0.125 @ remEI 0.35` holding by **+2.1%** and `0.150 @ remEI 0.35` missing by
    **−4.1%**, the two rungs nearest a threshold anywhere in the 70-rung grid, both inside
    §9.3's own `tau_anchor = 0.10` band — the band the frozen document already declared too
    small to constrain a verdict. **Every sentence that names 0.150 kg as the boundary must
    carry the disclosure that the boundary is unresolved at ±1 ladder rung.** This is a
    constraint on wording, not an amendment: §9.5's licensing sentence is satisfied as
    written.

104. **[NEW S74] NEITHER INDEPENDENT AUDIT REACHED THE COEFFICIENT VECTORS.** Both agents
    reconstructed the result artifact without importing the executable, and everything
    **downstream** of the 8-entry coefficient vectors — distances, thresholds, margins,
    verdicts, sets, shape rules, classifier, censuses, provenance — is recomputable from the
    file and was recomputed. The step from raw gauge trace to coefficients is **not**: the
    traces are not persisted, so `harmonic_coefficients` over `[1000,1768)` cannot be
    re-derived from the artifact alone. That step is covered by the replay gate, the
    anchor's agreement with the screen, and X8, and by nothing either audit did. **Say so in
    the Technical Report** — two independent reconstructions must not be allowed to imply
    coverage they do not have.
105. **[NEW S75] "NO MASS RETAINED ITS OWN ROLE" IS AN AGGREGATE, NOT A UNIVERSAL.** Three of
    the seven role losses are inside the same `tau_anchor = 0.10` band — 0.050 kg dev at
    −5.013%, 0.100 kg val at −5.746%, 0.150 kg test at −4.141% — and a single well-shaped
    flip at any one of them makes that mass retain its role. **Licensing does not move**
    (Option B breaks at 0.025 kg, 18.2% out, and no in-band combination repairs the prefix),
    so this narrows the sentence and nothing else. **Write: "no measured mass retained its
    own reserved severity, and at three of the seven the margin was inside the instrument's
    own reproducibility band."** In A2.8 item 2, and it goes in the Technical Report.
106. **[NEW S75] VAL'S AND TEST'S ROLE COVERAGE WAS ESTABLISHED AT MASSES THEY DO NOT
    RESERVE.** The screen ran at 0.000 and 0.050 kg only; the assignment reserves both for
    **dev**. Val's 0.40 and test's 0.35 are sub-threshold at every mass those splits actually
    carry, so the 0/0/1/1 role-coverage read is **0/0/0/0** at the reserved payloads. **This
    does not retract the role-coverage artifact** — it is a correct read of the screen at the
    screen's own masses — and it is a *development-context* statement about payload mass,
    **not** a claim about val's or test's own environments (limitation 74 still binds).
    A2.1 point 3; both statements must appear together wherever either appears.

## Coherence / honesty bounds (keep loud)

- **Sensor RNG keyed on `(sensor_seed, pair_id, channel, stream)` jointly** (`utils/rng.py:76-78`). **Measured S39: a `pair_id` change alone moves `gauge_obs` by up to 6.50 µε**, against `D` of order 0.1–0.5. **Nothing else is in the key.**
- Deployable floors are *detection*, not learned attribution; abstention untestable on this fault library; **every joint-space control number comes from a condition where the structural fault causes no measurable JOINT deficit.**
- **A noise threshold is a property of the SENSOR MODEL, the window LENGTH, the window ORIGIN, the aggregation, the path, the operation, the construction, the identity, the fault's activation step, and — S60 — the CONTEXT POPULATION, of which payload mass is the dominant factor. The SIGNAL it is compared against depends on excitation, task, plant and payload.** Never quote a µε number without naming all of these.

## Constraints / environment / ops (load-bearing)

- **Simulation-only, one desktop:** Windows 11, Ryzen 7 8700F (8C/16T), RTX 5060 Ti **16 GB VRAM** (sm_120), 32 GB RAM, Python **3.12.10** in `./venv`. Free/OSS, commercial-use-friendly only.
- **venv has:** numpy 2.5.1, scipy 1.18.0, scikit-learn 1.9.0, matplotlib 3.11.0, mujoco 3.10.0, pandas 3.0.3, control 0.10.2, gymnasium 1.3.0, pytest 9.1.1, **torch 2.11.0+cu128**. **No new dependency was added in S46–S61.**
- **Running packet tests:** from the REPO ROOT, `./venv/Scripts/python.exe -m pytest -q "Reproducibility Packet/tests"`. **Scope pytest to that path** — a root-wide invocation collides on duplicate test module names in the ignored `tmp/session6_packet_copy/`. **Full suite 1,306 tests green (S72, 122.77 s WITH the new `results/payload_boundary_extension/plan.json` present — nothing asserts that directory's absence; S71 126.03 s; Codex S70 1,288 in 123.18 s).** `test_payload_boundary_extension.py` now collects **170** — Codex handed off 36 in S64, I made it 45 in S65, Codex 47 in its S65, my S66 review made it 53, Codex's S66 made it 58, my S67 review made it 71, Codex's S67 made it 76, my S68 review made it 81, Codex's S68 made it 83, my S69 review made it 106, Codex's S69 kept it at 106 (a rename plus three added spellings), my S70 review added 35 (21 of which are one parametrization over `_URI_SCHEMES` x three letter cases), Codex's S70 added 11, and my S71 review added 18 — one equality pin, 11 boundary cases and 6 scheme-character cases. **The two closed Step-2 seam files together collect 124.** Prior: 1,217 (my S68), 1,207 (my S67), 1,189 (my S66), 1,136 (my S64), 1,133 (Codex S63), 1,126 (my S63 and Codex S61), 1,115 (Codex S60), 1,107 (my S60, 150.54 s), 1,021 (S59, 143.00 s), 999 (S58), 975 (S57), 938 (S55), 906 (S54), 750 (S53), 595 (pre-S51 baseline). **Set `PYTHONIOENCODING=utf-8` for anything that prints non-ASCII** — the console is cp1252. **Use ASCII in probe scripts and in anything a gate prints.**
- **MUTATION SWEEPS — MANDATORY HARNESS SHAPE AFTER S60:** clear `__pycache__` before every run **and** set `PYTHONDONTWRITEBYTECODE=1` in the subprocess env; drop `-x`; translate anchors to the target file's own newline; report bad anchors separately from survivors; restore exact bytes in a `finally` and verify the blob afterwards. **Run the whole sweep twice and require identical results** — that is the cheapest detector for a harness fault.
- **Packet scripts are invoked FROM the packet directory** (`scripts\<name>.py`, `--output-dir results\<name>`), per its README. From the packet dir the project venv is `..\venv\Scripts\python.exe`. **In my PowerShell tool the working directory is not the repo root — use `Set-Location` or absolute paths. My Bash tool's cwd PERSISTS between calls — prefer absolute paths or re-`cd` every time.**
- **Timings (measured S35–S60):** full packet suite ~150 s; one MuJoCo rollout (3000 steps) **25.6–27.5 s**; a PARTIAL rollout is proportionally cheap — 480 steps ≈ 3.0 s; at reduced fidelity (`point_count=9`, `simulation_timestep_s=2e-4`) 501 control steps ≈ 0.37 s; a 200-realization sensor-only null at W=768 ~40 s; an offline re-observation ≈ instantaneous; the driver's `--mode plan` 0.30–0.33 s; **the payload-extension executable's `--mode plan` 0.36–0.38 s (eight MuJoCo model compilations, zero steps)**; **one driver-file mutation case ≈ 100 s** (a 17-case sweep is ~28 min and belongs in the background); **a small-analyzer mutation case ≈ 0.5–0.7 s with the fixed harness, so a 44-case sweep is under a minute.** **NO figure exists for the pinned `pairs=100` Stage-0 run — see limitation 45; do not invent one.**
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

90. **(NEW S63) WHEN A REVIEWER TIGHTENS ONE BRANCH OF A RULE, THE UNTIGHTENED BRANCH BECOMES THE DEFECT — AND IT NOW LOOKS AUTHORITATIVE.** Codex correctly narrowed Option B under one outcome and left the neighbouring outcome stating the older, looser version of the same rule. The two are mutually exclusive, so nothing was internally contradictory to read; the disagreement only appears when you ask what each branch *does* with the same evidence. I found it by enumerating the whole outcome space and comparing what the two branches licensed — the same enumeration the reviewer had already run to prove the classifier complete. **The move: after any narrowing, grep for every other statement of the same rule and re-run whatever check the narrowing was supposed to satisfy across all of them; and when two branches must agree, state the rule ONCE rather than twice correctly.** Its companion, and the sharpest test I have for a licensing rule: **ask whether DELETING a result can ever license a bolder choice.** If it can, the rule is wrong regardless of how defensible each branch looks alone.

91. **(NEW S64) AN ADDITIVE FIELD IS ONLY ADDITIVE WHERE SOMETHING CAN PRODUCE IT.** The payload mass was added to `PhysicalKey`, to the factory that builds one, and to the serializer that writes one out — which is every place a key is *consumed* or *rendered*, and not the one place a key is *built from a row*. The completeness check that finds this is not "is the field everywhere the type appears"; it is **"name every producer of this object, and check each one passes the new input."** Its companion, and the reason I caught it at all: **read a partial build against what the piece was FOR, not against what its spec listed.** All three of §3.2's bullets were satisfied and the property they were written to secure was not. And note the recurrence — Lesson 88 (a control that varies the thing it controls for), Lesson 89 (fixing the science broke a key silently), and now this: **each defect lived one layer below the layer that was being fixed**, which is where to look first after any repair lands.

92. **(NEW S65) THE EXIT PATHS OF A PROGRAM ARE THE REGION NO TEST ENTERS, AND THEY ARE WHERE THE EVIDENCE LIVES.** Every serious defect I found this session was in `main()` — a name read from a sibling handler's scope, a re-typed identifier, an exception class outside a handler's hierarchy — and none was reachable from any of the 36 tests, all of which called internal functions. The pattern is not accidental: a test of a pure function is cheap and a test that drives a CLI to a terminal exit is not, so the expensive ones do not get written, and the terminal exits are exactly the paths that exist to preserve evidence when something has gone wrong. **The move: for every exit path a specification says must persist something, write the test that DRIVES that exit and READS the file.** Its companion: **when a handler reports a cost, check which object it read the cost from.** Codex built a custom exception carrying `rollout_spent` and `elapsed_s` for exactly the right reason and then read them from the wrong scope, which is a failure mode that looks, in review, like the careful thing it was meant to be.

93. **(NEW S65) A RE-TYPED CONSTANT DISAGREES SILENTLY WITH THE ONE IT COPIES, EVEN IN THE FILE THAT IMPORTS THE ORIGINAL.** `run_payload_boundary_extension.py` imports `RUN_ID` from the approved replay gate and then hand-types the scenario id that `RUN_ID` is *derived from* — as a neighbouring run's name. Nothing could see it: the uniqueness check one line earlier passes, because the wrong name is also a real reservation, and the disagreement surfaces one check later. **Requirement (r) is usually applied across documents; this is the same defect INSIDE one file, between an import and a literal.** The move: when a module already imports something from a source, take every related constant from the same source, and if you must pin one locally, assert the derivation relation. And note where it was found — not by reading the file, but by driving the function and printing both candidates side by side.

94. **(NEW S66) WHEN TWO RULES POINT OPPOSITE WAYS, THE BUG LIVES AT THE EXIT WHERE THEY MEET.** One rule said *always persist the record*; another said *never record a machine path*, enforced by a guard that raises. Everywhere they did not meet, both looked correct. Where they met — a failure writer embedding a file this tool did not produce — the prohibition fired while writing the record and destroyed it. Nobody had written the pair down as a pair. **The move: for every invariant that REFUSES, find the invariant that COMPELS, name the exit where both apply, and drive it.** Its companion, and the sharpest thing this session taught: **a repair aimed at a failure mode is where that failure mode reappears one layer down.** Codex added an exit specifically to satisfy X6, and that exit could fail X6, because it recorded a command-line argument before anything checked the argument's shape — the check exists, and it runs one exit later. That is the third consecutive session in which the defect lived one layer below the layer being fixed (Lessons 88, 89, 91), and it is now the first place to look after any repair lands. A third note, cheap and repeatable: **when you suspect a rewriting function, run each of its rules ALONE over the same input.** That is what turned "the scrubber eats URLs" into "MY regex eats URLs and the reviewer's is innocent," which is a different sentence and the honest one.


95. **(NEW S67) WHEN ONE ROUTINE EXISTS TO SATISFY ANOTHER ROUTINE'S CHECK, IT MUST END BY ASSERTING THAT CHECK.** The scrubber's entire job was to make the writer's guard true, and it did it by recognising a list of path spellings while the guard asked `PurePath` a question. Those disagree on inputs nobody thought to write down, and each disagreement destroyed an artifact. Two spellings had already been added in two consecutive sessions — each a correct fix to a real defect, and each an enumeration, so the class stayed open both times. **The move: name the predicate the other routine actually applies, make it the post-condition, and then ENUMERATE the input space to check it — 37,448 strings ran in 0.27 s and found 1,358 counterexamples that no amount of reading found in three sessions.** Its companion, and the reason I trust the fix rather than my reasoning about it: **my first two versions of the post-condition were both wrong, and the enumeration caught both in under a second** — the first reduced with whichever parser answered first, which hands a Windows path straight back; the second reduced once per flavour, and reducing a POSIX root can PRODUCE a Windows one. A fix to a class needs the same instrument the class needed. Third note: **an assumption a gate relies on is a thing to check at the gate.** We had agreed not to rewrite approved content and that agreement was right; what it rested on was the claim that approved content came from our own writer, and nothing checked it. **Refusing is not rewriting** — that distinction is what let the premise become a guard without reopening the decision.

96. **(NEW S68) WHEN A REVIEWER'S REPRODUCTION WILL NOT REPRODUCE, THE MOVE IS NOT TO DISPUTE
IT — IT IS TO ASK WHAT WOULD HAVE TO BE TRUE.** Two of Codex's three findings failed to
reproduce in my harness, and the cheap wrong conclusion was available in both cases: *the
finding is wrong.* Varying one thing at a time located the real conditions instead — the
member name the value sits under, and the depth of the ambient call stack — and both findings
turned out to be right, with fixes that are clearly correct rather than merely plausible. The
general form: **a claim and its demonstration are separate artifacts, and a broken
demonstration is evidence about the demonstration.** Its companion, and the reason the second
one mattered: **a number in a review can be a property of the harness rather than of the
code**, and the way to tell is to vary the harness deliberately — sweeping two ambient stack
depths turned an unrepeatable "990" into a repeatable statement, and changed what the fix had
to be FOR (not "block 990" but "make the answer independent of the caller"). Third note, and
the fourth consecutive session it has held: **a repair aimed at a failure mode is where that
failure mode reappears one layer down.** The repair that stopped a path being published is
what made the whole reason discardable. Fourth: **an enumeration test is satisfied trivially
by a rule that throws everything away** — after asserting the post-condition, assert that the
last-resort branch was never REACHED, or the strongest evidence in the file is compatible with
the worst behaviour.

97. **(NEW S69) A RULE WIDENED ONE INPUT FAMILY AT A TIME WILL BE WIDENED AGAIN NEXT
SESSION — THE FIX FOR A CLASS IS A CROSS-PRODUCT, NOT ANOTHER EXAMPLE.** Six consecutive
rounds have now found the same class one family further out, and every single fix was
correct. The reason the class stayed open is that each fix was an *instance* — add the
digit drive, add the UNC form, drop this boundary — while the property was never asserted
over the space of inputs. What worked this session was building the grid: eleven renderings
crossed with thirteen prefixes and two suffixes, both agents' blobs in one process, two
questions per cell (did the marker survive, was the message destroyed). Reading the patterns
found nothing in three sessions; the grid found four families in one run. **The companion,
and the harder half: the grid also told me which family NOT to close.** Two of the
cells could only be covered by a rule that mangles this project's own vocabulary, and the
right output there is a disclosed limitation with a test that pins it — a scrubber's accept
side is where damage is invisible, so an un-measured "improvement" is the dangerous
direction. Third note: **when a repair closes a mechanism, go back and re-measure whatever
was justified BY that mechanism.** `_final_component` retired the exact behaviour my own
Session-68 fixpoint test described in its docstring; the fixpoint is still needed, but for a
different reason and a different input family, and the honest move was to extract one pass so
a test could DRIVE the claim instead of narrating it.

98. **(NEW S70) WHEN TWO THINGS ARE THE SAME SHAPE, THE ONLY HONEST RULE IS ONE THAT NAMES
THEM — AND THE NAMING IS THE PART THAT MUST BE DISCLOSED.** A URL host and a UNC host are
lexically indistinguishable, so every "clever" boundary rule we tried was really a hidden
name-based decision with its criterion left implicit: *any alphanumeric-plus-colon counts as
a scheme.* Stated out loud, nobody would have agreed to that; buried in a lookbehind, it
survived three sessions of review and published a complete machine path. **The move: when a
pattern cannot decide a case on shape, write the list, put it in a named constant, test the
list itself rather than examples of it, and disclose what falls off the end.** The
companion, which is what made this findable at all: **when you widen a cross-product, widen
it where the previous one was THIN.** My S69 grid crossed renderings with prefixes and found
four families; it had no prefix ending in a letter-colon, and that one missing column was
the whole finding. A grid is only as good as its thinnest axis. Third note, and the one I
would keep if I could keep only one: **a repair that changes which rule reaches an input can
silently retire the test that guarded the rule it used to reach** — so after any change to
matching order or precedence, re-run the sweep before believing the suite.

99. **(NEW S71) A TEST THAT READS THE THING IT SHOULD BE CHECKING IS NOT A TEST OF IT, AND
THE PLACE THIS BITES IS WHEREVER A CONSTANT *IS* THE DECISION.** Last session I wrote the
lesson "write the list, put it in a named constant, **test the list itself rather than
examples of it**" — and then wrote a test parametrized over the list, which is examples of
it. Codex extended the same pattern. Neither of us could see it, because the tests pass and
the behaviour is right; it only surfaces when you damage the list on purpose and watch the
suite stay green. Dropping two of eight names, or adding a ninth, survives the entire
focused suite, and adding one immediately republishes a complete machine path. **The move:
for every constant, ask "if someone edits this, what goes red?" — if the answer is "the
tests just run different cases," it needs an equality pin, and the pin's docstring should
carry the measured survivor table so the next reader knows it is load-bearing.** This is
requirement (r) — equality, never adoption — which we have applied between documents and
between two call sites in one file, now applied between a test and a constant.

The companion, and the more general one: **a probe is not a test.** Codex measured a
312-cell boundary matrix, found zero errors, and committed a test for a different property;
the matrix's accept side therefore protected nothing past the session that ran it. My own
968-cell and 3,256-cell grids have exactly the same failure mode, which is why the grid
property became a committed test in S70 and the boundary class became one in S71.
**Whenever a review reports a measurement, ask which committed artifact will still be
making that measurement next month.**

Third note, and it is about honesty rather than technique: **when none of your new tests is
red against the state you are reviewing, say so first.** Eighteen new tests look like
eighteen new defects to anyone reading quickly, and in a loop this long the temptation to
let a count speak for itself is real. The tests are coverage; the evidence is the sweep; a
reader who has to work that out for themselves has been handed a worse report.

100. **(NEW S72) A GENERATED ARTIFACT MUST BE CHECKABLE FROM ITS OWN CONTENTS, OR THE
DIGEST EVERYONE SIGNS IS A DIGEST OF SOMETHING NOBODY VERIFIED.** The plan artifact exists
to be named by an authorization, which means both agents put their signature on a
fingerprint. The cheap version of "I read the plan" is to open it, see 126 where you
expected 126, and approve. The version that is worth anything is to **rebuild the artifact's
own claims out of the artifact's own published fields, with code that does not import the
program that wrote it** — all 126 physical-key reports from `plan.masses` / `plan.ladder` /
`plan.identities` / `inputs.probe_*`, then the two-stage sort-and-hash by hand. It matched,
and the fact that it *could* be done is the property that makes the artifact fit to sign.
**Ask of every artifact you are about to approve: what in here can only be checked by
trusting the writer? Then either check it another way or say out loud that you did not.**

The companion, and it is about provenance rather than arithmetic: **a digest is only a
signature on a document if the document is the same bytes everywhere.** Three runs from two
packet roots gave byte-identical files, and canonical JSON turned out to contain no newline
of either kind — so unlike our other tracked result artifact, no line-ending filter can
touch it and its raw and canonical digests are one number in every checkout. I checked that
by staging it and reading the index blob back rather than reasoning about `.gitattributes`.
**When a digest is about to become load-bearing, materialize the file the way a stranger
would receive it and hash that.**

Third note, and it is the smaller half of Lesson 75: **an artifact can also contain more
than its specification names, and additive fields deserve the same sentence as missing
ones.** Two fields here are not in §11.1's list. One is named in §11.2; the other is named
nowhere and is the only thing discharging X9. Both are right to be there — but a reader
walking the spec against the file would have found an unexplained difference, and the fix
for that is to say it first.

101. **(NEW S72) WHEN A REVIEW-DISCIPLINE CHECK STOPS BEING TRUE, RETIRE IT OUT LOUD.**
Both agents reported "results/payload_boundary_extension absent" in every verification block
for eight rounds. It was never a committed test — it was a habit, and habits that look like
checks are the ones that quietly become false. Step 3 made it false by design. Saying "that
line retires here, and nothing was ever enforcing it" costs one sentence and stops a future
reader treating eight rounds of a manual assertion as eight rounds of a guarantee.

## Pointers

- **Protocol P (in force, JOINTLY APPROVED): `Reproducibility Packet/protocol/protocol-p-v2.3.3.md`, canonical sha256 `5689dad7…8bdf421f`. READ THE FILE.**
- **The payload-boundary extension — JOINTLY APPROVED AND FROZEN, NOT YET EXECUTABLE: `Reproducibility Packet/protocol/payload-boundary-extension-v0.2.md`, canonical sha256 `538ae06b…df33b6a`, blob `d9f6e188`, 71,188 bytes, 1,285 lines, LF, raw == canonical.** Approved by me S63 and by Codex S63; **DO NOT EDIT IT — a change needs a version bump and a `git mv`.** It authorizes **Step 2 only**: build and review the three prerequisites. READ THE FILE — the blocks above are an index, not the document. Superseded states, never cite or build from them: v0.1 (`32a03930…`, blob `903962f8`, bytes in `Claude Session 61`), and inside v0.2 `c7facc13`/`e734c498…` (my S62 handoff) and `3d72e1f4`/`e5192eaa…` (Codex's S62 edits, which I did not approve).
- **STEP 2 IS CLOSED — ALL THREE PREREQUISITES JOINTLY APPROVED. STEP 3 HAS RUN. THE PLAN ARTIFACT IS THE OPEN STATE AND CODEX OWES THE SECOND READ.**
```text
THE STEP-3 ARTIFACT — I RAN IT AND APPROVED IT IN S72; CODEX OWES THE SECOND READ:
  Reproducibility Packet/results/payload_boundary_extension/plan.json
  canonical sha256  15298da4c7a903bf4b62a79eb384abe1f53182972dff41c6e1387dc0ce030be3
  git blob          04f2bccd53629d6b54895be20224a680a78325c7      5,386 bytes  TRACKED
  Reproduce it EXACTLY (from the packet dir; overwrites in place, byte-identical):
    ..\venv\Scripts\python.exe scripts\run_payload_boundary_extension.py --mode plan
  A REVIEW PROBE MAY POINT --output-dir AT A SCRATCH DIR and diff the bytes.
  DO NOT run --mode execute.  It needs --approved-plan-sha256 AND --data-root, and
  BOTH are gated on the Step-4 joint authorization, which does not exist yet.
JOINTLY APPROVED (me S64, Codex S64) — CLOSED, DO NOT REOPEN:
  scripts/utils/assignment_generator.py                b7b2430a28f2617c28b0924e16ce5b71aba0bf8a
  tests/test_assignment_generator_screen_overrides.py  c23e61d386c7213f93e4623cfd3a2b8bbfa30fa4
  scripts/utils/protocol_p_results.py                  2f7c33b274bfe7ee16ecdf0dc7227ca6bd159f9c
  tests/test_protocol_p_results.py                     ad6b32fef834cb55225b6cea1ac7831f090391de
  (Codex's own prior state of the last two, eaa33797 / 7361bfd8, is SUPERSEDED)
THE THIRD PREREQUISITE — THE MEASUREMENT EXECUTABLE — JOINTLY APPROVED, CLOSED S71:
  scripts/run_payload_boundary_extension.py  95040d9305e08da22d23d6b827c8d14cd0e5603c
  tests/test_payload_boundary_extension.py   0d7b68fc02295c9611b80a5e9c9b58ed71123eb6
  SUPERSEDED, never build from: 62e4c9e1/96906aab (Codex S64), ff0cdbe6/ebdfdf83 (my
  S65), eb94afb2/5d8dd369 (Codex S65), 431d9c08/4d194a67 (my S66), 86fc3fdb/e081a26d
  (Codex S66), 5a5b0562/f2f5031d (my S67), 25386e27/ab4ddfc0 (Codex S67),
  04ec936e/4979af07 (my S68), 9cd10305/ce0cd642 (Codex S68), 9fd723b0/191d9b4d (my S69),
  f2d9f3b1/eb10bb23 (Codex S69 — DOCUMENTATION ONLY, executable AST identical to mine),
  c7451068/485dcc3d (my S70), c850a4b6/150870f4 (Codex S70 — the LAST OPERATIONAL change;
  my S71 is AST-identical to it and differs only in docstrings and tests).
STEP 2 CLOSED S71.  STEP 3 RUN S72.  STEP 4 IS A SEPARATE JOINT AUTHORIZATION AND
DOES NOT EXIST.  NOTHING DOWNSTREAM RUNS.
```
- **The replay gate: `scripts/protocol_p_replay_gate.py` + `tests/test_protocol_p_replay_gate.py` (36 tests).** Run from the packet dir: `..\venv\Scripts\python.exe scripts\protocol_p_replay_gate.py --data-root ..\data\gate3-base-dev-pilot-val-c1-s`. **EXECUTED EIGHT TIMES; not run S52–S60. IT CERTIFIES `overrides=None` ONLY (limitation 63).**
- **Stage 0: `scripts/analyze_synchronous_difference_null.py` (blob `f104971d…`) + `tests/test_synchronous_difference_null.py` (99).** Pre-registered invocation from the packet dir: `..\venv\Scripts\python.exe scripts\analyze_synchronous_difference_null.py --window 768 --f-ctrl-hz 500.0 --diagnostic-hz 0.8 --thermal-ramp-c 3.0 --pairs 100 --seed 0 --pair-id 1`. **It has been spent; re-running it is NOT authorized.**
- **The Stage-0 artifact — JOINTLY APPROVED. Tracked. DO NOT EDIT, DO NOT RE-EXECUTE.** `results/protocol_p/sensor_only_difference_null.json`, blob `31c1e6d1824c10bd5978d12c377f76cf556af03f`. **`samples` is a 6-key metadata dict; the 100 values are `samples["distances"]`. There is no top-level `authority` — the path is `corroboration.authority`.**
- **THE STAGE-A/B/C PROGRAM — JOINTLY APPROVED AND EXECUTED. NOTE: `protocol_p_results.py` AND ITS TESTS HAVE MOVED ON — the blobs below are the EXECUTED state, not the current file. The current pair is the Step-2 state above.**
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
JOINTLY APPROVED (mine S61, Codex S61) — LOOP CLOSED:
  scripts/analyze_protocol_p_payload_conditioning.py  39048d2658963a345e3a46949a6070d421a155d9
  tests/test_protocol_p_payload_conditioning.py       b9e81f6320e1a3b68f952d631795f1d82abca5ff  105
Run either read from the packet dir; zero rollouts, ~0.3 s each:
  ..\venv\Scripts\python.exe scripts\analyze_protocol_p_<name>.py `
    --screen-result results\protocol_p\stage_abc_screen.json `
    --assignment config\proposed-gate3-assignment-v0.1.json --output-dir results\protocol_p
```
- **`agents/Claude/Progress Reports/Progress Report Session 64.md` — covers S57–S64. **LOOP CLOSED at `b0ff7496`**: Codex explicitly approved that exact blob in its S65, and I had already approved it, so both approvals name the same bytes. Do not reopen.** Its spine: the screen ran; its result turned out conditional on payload mass, measured at the two lightest of eight weights; the four sessions since went into designing the follow-up rather than writing the result up as though the dependency were not there. `Progress Report Session 56.md` (S49–S56) — **LOOP CLOSED AT ROUND FIVE, blob `83c527c…`. Do not reopen.** Its headline — that sixteen sessions produced no measurement — is overtaken by events: the measurement ran in Codex's S57. `Progress Report Session 48.md` remains jointly approved at blob `f01aa7d7…`.
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
- **Live-Run README (co-maintained): root `README.md` — Phase 2 / In Progress, banner 2026-08-04. MY S72 APPENDED ONE ENTRY (`+2/−0`), edited no dated entry, and left the banner alone (Codex had already advanced it to 2026-08-04 earlier the same day). THE TRIGGER FIRED: a finished artifact — the extension's plan document, the first thing the extension has produced. The entry deliberately continues Codex's own entry from hours earlier, which had told the reader "the next permitted step is a zero-simulation plan document"; mine closes that loop for them. It states what the plan fixes in advance, the 0.36–0.38 s against ~26 s per simulation, that the 126-body fingerprint was rebuilt from the plan document rather than taken from the program, and the honest boundary (no simulation, 151, second agent has not read it, nothing runs until a separate authorization names this document).** *(Prior: MY S71 RAN THE HEARTBEAT CHECK AND ADDED NOTHING — SEVENTH consecutive session, same reason: the executable loop is still open (round eight), so no artifact was finished and no phase closed. My S70 made the same call (round seven). My S69 made the same call (round six). My S68 and S67 made the same call, as did Codex for its own S66 and S68. THE ENTRY BELONGS ON THE LOG WHEN THE LOOP CLOSES, and whoever writes it owes the reader the four-round history, not just the outcome. Codex wrote that entry in its S71.)** (Banner history: I moved it to 2026-08-03 in S64; my S62 and S63 left it because those were same-day.) **My S65 appended one entry (`+2/−0`), left the banner alone (same day), and edited no dated entry** — the bar was cleared by the first review of the executable finding it could never have completed a run. **Codex's S64 also appended a dated correction entry to its own preceding one (the loud-not-silent refusal, and the 4,432.16 s / 73.9 min screen time against the withdrawn project-wide "seventy minutes"); I read it and it is right.** My S64 appended one entry (`+3/−1` including the banner line), because the trigger my S63 note named actually fired: **the extension document loop CLOSED**. The entry covers the agreed plan, the 19,448-state licensing enumeration, the start of construction, and the payload column that existed with nothing able to fill it. **The log's date order is out of chronological order in the middle and Codex's dated correction says so; dated entries are never edited, so it stays that way.** **Beware when appending: `README.md` is all-CRLF; split on `b"\r\n"`, insert before the `''/'---'/''` block that precedes `## Follow along`, assert both anchors before writing, and read the neighbouring lines back afterwards rather than trusting an offset.**
- **Phase-2 chat:** `chats/Claude-Codex/Phase 2 Integration and Config Freeze/…- Active.md` — **NOW 19,023 lines. My S72 turn is `+172/−0`, header unique at line 18,853, physically last, pre-write prefix (1,218,243 bytes) retained byte-for-byte with its SHA-256 (`c2c077b1…`) asserted inside the writer. CODEX OWNS THE NEXT TURN: the SECOND INDEPENDENT READ of `plan.json` (`15298da4…030be3`) and nothing else. WHAT IT HAS TO JUDGE: whether the Step-3 artifact is a faithful §11.1 plan. I gave it my re-derivations, the two additive fields, and the §12 "plan artifact must carry the executor's own count" observation, and told it that if it reads that sentence as requiring a version bump, its version wins rather than trading a round. IF IT APPROVES, THE TURN AFTER THAT IS THE STEP-4 JOINT AUTHORIZATION — and I explicitly declined to write anything readable as half of one, so do not let my approval be mistaken for it.** *(S71 record, kept: my S71 turn was `+168/−0`, header unique at line 18,622, prefix SHA-256 `83b52b2e…`; Codex approved those exact blobs and closed the loop in its S71 at `+63/−0`.)* *(S69 record, kept: my S69 turn was `+205/−0` with prefix SHA-256 `276c7630…`. I corrected my own header stamp in place immediately after writing it (20:40 → 20:35 PDT, same byte length, every byte outside the 46-byte span compared before and after) because an estimated stamp defeats the only thing a stamp is for; that is the ONLY edit I have ever made to posted transcript content. The S69 single-slash judgment it had to rule on is now SETTLED — Codex agreed in its S69.)* **If a judgment comes back contested and one exchange does not settle it from source, ESCALATE to the director rather than trade turns.** Codex answered my S64 open question in its S64: **the executable does NOT use `LogicalRow.key` across masses** — extension rows carry their own mass-bearing logical key and their joins use the mass-bearing `PhysicalKey`, so `.key` stays as it is. **Settled; do not reopen.** The things Codex has to judge now are the five S65 corrections and, explicitly, the one structural deviation: **I lifted the replay gate's pre-rollout half into `resolve_replay_source` so it is testable at zero cost.** Do NOT re-open: the extension document (both approved `538ae06b`), the five S62 edits, the unified Option-B rule, the four S62 questions, the measure-first ruling, the payload analyzer/tests, the role-coverage states, the readback ruling, `.gitattributes`, the Stage-C label, Step 25, the screen result, or the plan default. **The file is MIXED-EOL** — Codex appends LF, the older bulk is CRLF; append LF and verify `+N/−0` rather than assuming.
- **Monitoring chat:** `chats/Claude-Codex-Human/Transcript Order Monitoring/…- Active.md` (88 lines; unchanged S43–S72 — no recurrence; **streak FORTY-TWO**: Codex's S71 append verified at the git level in my S72 — commit `5250aa4`, `+63/−0`, header unique and correctly ordered after mine — and my own S72 append passed all five gates. *(Prior: **streak FORTY-ONE**: Codex's S70 append verified at the git level in my S71 — `+110/−0`, prior content a byte-identical prefix, header unique, physically last — and my own S71 append passed all five gates.)* *(Prior: **streak thirty-nine**: Codex's S69 append was `+92/−0` with its header unique at line 18,257 and physically last, verified at the git level in my S70, and my S70 append passed all five gates — pre-write prefix retained byte-for-byte with an identical SHA-256 asserted *inside* the writer, header unique, physically last, `+165/−0`.)* The duty is to flag recurrences, so a clean session adds no note; verify at the git level regardless.

## Scratchpad (S75, NOT committed)

**Nothing durable, deliberately.** S75 was drafting; the only file in the scratchpad was
`s75_turn.md`, the chat turn, appended verbatim and then dead. Every figure A2 quotes was
re-derived with short inline reads of the persisted artifact rather than with a saved
instrument, **and that is the right call precisely because they are re-derivations of
already-audited numbers** — the S74 auditor below is the instrument to rebuild if the
result artifact is ever re-opened, and a second half-instrument beside it would just be a
thing to keep in sync. **Two reads worth reproducing exactly if A2 is edited:** the
weight-to-split map comes from `config/proposed-gate3-assignment-v0.1.json` →
`context_profiles.payloads` (NOT from a result artifact), and the well-shaped-flip sweep
must classify each flip's landing through the full R0..R12 order and discard `R8`/`R9`
landings before counting, or 61 mechanical shape violations drown the four real ones.

**Append discipline that worked and should be reused:** record `sha256` / byte length /
CR and LF counts / the exact trailing bytes of the transcript BEFORE writing, assert the
file ends at that anchor and that the anchor is unique, append in `'ab'` mode, then assert
the prefix is byte-identical, the header occurs once and after the boundary, Claude is
physically last, and the pre-existing CR count is unchanged. All eight held; `+201/-0`.

## Scratchpad (S74, superseded)

`audit_result_artifact.py --packet-root "Reproducibility Packet"` — **the 130-check result
audit, and the one to rebuild first if the result artifact is ever re-opened.** Same
independence discipline as the S72 plan probe: it does NOT import
`run_payload_boundary_extension`, writes its own canonical-JSON and its own `D` statistic
(`np.linalg.norm(fault − healthy)` over the 8-entry coefficient vector), and takes its
literals from the frozen documents at run time rather than from my memory. It reaches
outside the artifact three times — the approved `plan.json`, the committed
`stage_abc_screen.json` (for the cell-6 rebuild), and the two protocol files on disk (for
the digest pins, LF-normalized before hashing). **Two shapes to keep when rebuilding it:**
the physical-key condition vocabulary is Protocol P's `"structural"` while the §11.3
identity payload's is `"structure"` — two closed vocabularies over the same fact, and
comparing them naively fails 70 of 126; and the raw file legitimately contains 9,576
backslashes, all `\"` from the embedded canonical strings, so X7 must be checked in the
**decoded** domain.
`sensitivity_sweep.py --result <payload_boundary.json>` — the τ-band flip sweep behind THE
S74 FINDING. Rebuilds `TESTABLE_SET` and `ROLE_RETAINED` under an arbitrary set of flipped
rungs, re-runs §9.5's R8–R12 and the Option-B prefix rule on the perturbed state, and
**separates shape-violating landings from informative ones** — without that split the
headline number is 63/70 and means nothing.
`append_s74.py` (inline) — the transcript appender, now matching the file's own physical
tail ending and emitting the `---` separator, with the prefix SHA-256 asserted **after**
the write. Both appends this session verified clean.

## Scratchpad (S72, NOT committed)

`probe_s72_plan.py` — **the artifact reader, and the one to rebuild first if the plan is
ever re-reviewed.** Reads `results/payload_boundary_extension/plan.json` and, using ONLY
fields the artifact itself publishes, rebuilds all 126 `physical_key_report` objects, sorts
them by their own canonical JSON, hashes the ordered list, and compares against the
published `plan.physical_keys.canonical_sha256`. It also re-derives the census, the anchor
partition and its stability interval, and the identity-band rule, and scans every string in
the document — object member names included — with an absolute-path regex written for the
probe alone. **The independence is the point:** it does not import
`run_payload_boundary_extension`, and it writes its own canonical-JSON function rather than
importing the project's. Output on the committed artifact: 126/126, digest MATCH, every
arithmetic check True, 285 strings scanned, 0 offenders, 0 backslashes.
`append_s72.py` — the five-gate transcript appender (prefix SHA-256 asserted **inside** the
writer, header uniqueness, header-after-boundary, Claude physically last, `+N/−0`).
`readme_s72.py` — the CRLF-safe Live-Run README appender. Anchors on the
`\r\n---\r\n\r\n## Follow along` block, asserts the anchor is unique, and reads the
neighbouring lines back afterwards. **Do not index README lines by splitting on `\r\n`** —
the banner's last row ends with a bare `\n`, so every index after it is off by one and I
briefly mis-read my own entry's position because of it.

## Scratchpad (S71, superseded)

`slice.py` — **the enabling instrument, and the one to rebuild first.** Loads the scrubber
layer of ANY blob of `run_payload_boundary_extension.py` by exec'ing the source slice from
`_WINDOWS_ABSOLUTE = re.compile(` to `def describe_error(` in a namespace holding `re`, both
`PurePath` flavours and `REPO_ROOT` — so two blobs run in one process without fighting over
`sys.modules` (the module imports mujoco-bearing siblings, so importing two copies is not
an option). **`verify_slice()` is not optional:** it compares the sliced namespace against
the genuinely-imported module over a 400-input battery and the probe REFUSES to continue on
any disagreement. 0 disagreements. *A slice is a new instrument; a wrong one produces
confident nonsense.*
`probe_s71_grid.py` — the S70 grid widened on the axis Codex's edit lives on: 22 renderings
x **37** preceding contexts (the old 11 plus 26 built from scheme tokens, case renderings,
suffix-of-a-longer-token forms, near misses and non-scheme boundary characters) x 4
suffixes = **3,256 cells**, classified CLEAN / RELATIVE_SURVIVOR / ROOTED_SURVIVOR /
DESTROYED / GUARD_REFUSES. `classify()` is reusable and the other probes import it.
`probe_s71_pairs.py` — **the new axis: TWO paths in one message.** 8 x 9 x 9 = 576 cells.
Found nothing, which rules out a family I had a specific reason to suspect (`re.sub` cannot
overlap, and the POSIX `lead` group consumes a character a following match may need).
`sweep_s71.py` — 19 cases, fresh copytree each, two passes, `PYTHONDONTWRITEBYTECODE=1`,
no `-x`, anchors asserted unique, verdicts carrying no elapsed time. Includes the
LESSON-63 DOUBLE via a `DOUBLE_EXTRA` map that applies a second mutation to the same copy.
**This is what produced all three findings** — none of them was reachable by a red-check.
`ast_check_s71.py` — verifies MY OWN "no operational change" claim the way Codex's S69
claim was verified: docstrings stripped from every module/function/class, then `ast.dump`
compared.
`turn_s71.md`, `append_s71.py` — the append writer asserts the pre-write SHA-256 as a
PREFIX *inside* itself before leaving the file in place, then re-checks header uniqueness,
position, physical-last and `+N/−0`.
**Boundary enumeration (inline, worth rebuilding):** over all 100 printable characters, the
set that mangles `https://example.org/dir/file.txt` is EXACTLY `[A-Za-z0-9+.-]` plus `/`.
That is how the accept-side test asserts a measurement instead of an assumption.

## Scratchpad (S70, superseded)

`probe_s70_disclosure.py` — **the instrument of the session and the one to rebuild first.**
The S69 grid, WIDENED WHERE IT WAS THIN: twenty-two renderings x eleven preceding contexts
x four suffixes = 968 cells, each classified into CLEAN / RELATIVE_SURVIVOR /
ROOTED_SURVIVOR / GUARD_REFUSES / DESTROYED. *The general move: when you widen a
cross-product, widen the axis the previous one was thinnest on — the missing column here
(a prefix ending in a letter-colon) was the whole finding.* The classifier is what made it
readable: separating "a relative suffix survived" from "a rooted path survived" is what
turned 332 disclosed survivors and 4 real leaks into two different sentences.
`probe_s70_scheme.py` — characterises the leak: what both sides say about it, the exact
trigger set (a LETTER before the colon; a digit is caught by the non-letter drive rule),
whether the other renderings leak the same way, and a first candidate.
`probe_s70_candidate.py` — the candidate measured BESIDE the committed blob on the same
batteries: the grid, a 30-sentence prose battery, the committed 37,448-string enumeration.
`probe_s70_accept.py` — **the accept side, and it is not optional when you widen a
predicate the writer uses.** Calls `resolve_context` / `build_plan_document` /
`execute_document_skeleton` / `failed_plan_document` DIRECTLY (no plan mode, nothing
written) and counts offenders under both predicates: 0 / 0 / 0 under each.
`redcheck_s70.py` / `redcheck_s70_direct.py` — **the first one produced NO RESULT and that
is the lesson.** The reviewed blob has no `_URI_SCHEMES`, so the test module cannot be
COLLECTED and pytest reports one collection error instead of verdicts. The direct version
evaluates each new contract in one process against both blobs: 14 RED, 21 already true.
`sweep_s70.py` — 10 cases, fresh copytree each, two passes, verdicts carrying nothing
pass-varying. **Anchors are raw TRIPLE-quoted strings**; my first run had two BAD ANCHORS
because I escaped quotes inside single-quoted raw strings, which is the same class of
mistake as S68's escaping and S69's indentation. It is also what caught limitation 102.
`ast_check_s70.py` — verifies Codex's own AST-equality claim rather than taking it.
`turn_s70.md`, `append_s70.py`, `readme_s70.py`, `fix_readme_s70.py`.
**`readme_s70.py` WROTE A LITERAL CR INTO `agents/Claude/README.md`** — `"...\PRIVATE\row.npz"`
in a non-raw Python string makes `\r` a carriage return. Caught by the SyntaxWarning, found
with `cat -A`, repaired with `chr()` fragments, and the whole line re-scanned for stray CRs.
*Any Windows path written into a document through Python must be a raw string or built with
`chr(92)`.*

## Scratchpad (S69, superseded)

`probe_s69_embedded.py` — **the instrument of the session and the one to rebuild first.**
Builds a CROSS-PRODUCT — eleven path renderings x thirteen prefixes x two suffixes — and
drives all 286 through BOTH agents' git blobs in one process, printing per cell whether the
private marker survived and whether the whole message was destroyed. *The general move:
when a rule keeps being widened one example at a time, stop adding examples and build the
grid.* It found four families in one run after three sessions of reading found none, and it
is also what told me which family NOT to close.
`probe_s69_spaces.py` / `probe_s69_spaces2.py` — the space finding. **The first version
loaded the module from a TEMP COPY, which moves `REPO_ROOT` (it is derived from `__file__`)
and made the repo-root replacement look dead.** That was a harness property, not a code
property; the second version imports the committed file IN PLACE. *Whenever a probe loads a
module from anywhere but its real path, ask what the module derives from `__file__`.*
`probe_s69_candidate.py` — patches the committed source in memory into a CANDIDATE module
and runs both side by side over the leak battery, a prose battery, and the 37,448-string
enumeration. Measuring the repair beside the original, on the same batteries, is what let
the prose cost be reported as a number rather than as a claim.
`probe_s69_cost.py` — the adversarial side: a REAL path followed by a slash-carrying token.
That is where the space gate would over-consume, and it is why the gate is a BACKSLASH.
`probe_s69_passes.py` / `probe_s69_twopass.py` / `probe_s69_onepass.py` — re-measure the
fixpoint's necessity after `_final_component` closed the S68 mechanism. *When a repair
closes a mechanism, re-measure whatever was justified BY that mechanism.*
`redcheck_s69.py` — takes the blob to restore as `sys.argv[1]`; isolated packet copy, the
reviewed source restored over the edited script, my tests kept.
`sweep_s69.py` — 11 cases, fresh copytree each, two passes. **Anchors are raw
triple-quoted strings** because the patterns contain both quote characters; that fixed the
S68 escaping problem, but I still shipped one anchor with the wrong INDENTATION and one
verdict carrying pytest's elapsed time. Both are recorded in limitation 100.
`turn_s69.md`, `append_s69.py`, `fix_stamp_s69.py`.

## Scratchpad (S68, superseded)

`probe_s68_payloads.py` — **the instrument of the session and the one to rebuild first.**
Drives the SAME defect through two placements — the value under `"x"` and the value under
`"inputs"` — across BOTH agents' blobs in one process, and prints rc / artifact-present
side by side. *The general move: when a reviewer's reproduction does not reproduce, do not
dispute it — ask what would have to be TRUE for it to happen, and vary that one thing.*
That is what separated "this finding is wrong" from "this finding is right and its
demonstration is in the wrong position."
`probe_s68_depth.py` — sweeps JSON nesting depth at two AMBIENT STACK DEPTHS (`+0` and
`+300` frames, via a recursive trampoline). *When a reported threshold will not reproduce,
suspect the harness variable nobody named.* It turned an unrepeatable "990" into a
reproducible statement about the caller's stack, and changed what the fix has to be FOR.
`probe_s68_destruction.py` — isolates the whole-message discard branch by emulating ONE
substitution pass, then tests the proposed fixpoint against the same enumeration. It is
what showed the branch fires on 6 of 37,448 today rather than "if a rule is later
weakened", and that the fixpoint takes it to 0 while preserving prose.
`probe_s68_predicate.py` — asks the three questions a stricter writer predicate raises:
does it refuse the tool's OWN documents (0 offenders), how deep is the official plan
(5, against a gate of 64), and is the new fallback reachable.
`redcheck_s68.py` — takes the blob to restore as `sys.argv[2]`, so the SAME harness
red-checks the reviewer's additions against my state and mine against the reviewer's.
**A test file that references a new module constant cannot be COLLECTED against an older
blob** — that is a harness result, not a coverage result, and it has to be reported as
one.
`sweep_s68.py` — 8 cases, fresh copytree each, two passes, 300 s cap per case.
**Anchors must avoid escaped backslashes**: my first three cases were all BAD ANCHOR
because I escaped a raw regex line four times over. Anchor on a short escape-free
substring and append the rest of the line as a comment instead.
`turn_s68.md`, `append_s68.py`, `rewrite_soonc_s68.py`, `rewrite_soonc_s68b.py`.

## Scratchpad (S67, superseded)

`probe_s67_roots.py` — **the instrument of the session and the one to rebuild first.**
Enumerates every string over `{ / \ C : x space . 1 }` up to length 5, scrubs each, and
asks both `PurePath` flavours whether the RESULT is still absolute; then drives the
survivors through the real writer, and finally prints a battery of real prose sentences
so the accept side is visible beside the refuse side. *The general move: when routine A
exists to make routine B's check pass, do not read A's rules — assert B's predicate over
an enumerated input space.* 37,448 strings in 0.27 s. It found the defect AND caught both
of my own wrong fixes.
`probe_s67_exits.py` — drives `main()` to the X0E refusal with a foreign plan carrying
each shape as a VALUE and as a KEY, and reports rc / whether the artifact landed / whether
a marker leaked. **Put the leak marker in the DIRECTORY portion, never the basename** —
my first version used "secret" inside `secret.txt` and reported a leak on every working
case. Carries controls (the shapes already fixed) so a clean row proves the harness
reached the exit.
`probe_s67_codex_findings.py` — loads BOTH agents' blobs as separate modules and drives
each case through both in one process, so the accusation and the fix appear in one table.
`probe_s67_survivors.py` — for each sweep survivor, builds the state the guard exists to
refuse and runs it, which is what separates REDUNDANT from REAL GAP. It is what showed the
key-collision loop was a real coverage gap and the writer's key visit was the only defence
on the authorized path.
`redcheck_s67.py` / `sweep_s67.py` — the red-check (restore the REVIEWED blob over the
edited script in an isolated packet copy, keep the new tests) and the mutation sweep.
**`Path.read_text(newline=...)` does not exist on 3.12** — read bytes and translate anchors
to the target's own newline. **A refactor makes old anchors stale**: two of my cases went
to `BAD ANCHOR (0 matches)` after I lifted the writer's guard into a function, which is a
HARNESS result, not coverage — retarget and re-run before quoting any number.
`append_s67.py`, `turn_s67.md`.

## Scratchpad (S66, superseded)

`probe_s66_exits.py` — **the instrument that turned four readings into four
measurements, and the one to rebuild first.** Drives every execute-mode exit against a
constructed plan file and prints, for each, the return code, whatever escaped, and
whether the artifact actually landed on disk — then runs a battery of realistic sentences
through the scrubber. *The general move: to test a rule that says "always persist", do
not read the branches; drive each one and look at the directory.*
`probe_s66_slashslash.py` — runs each scrubbing rule ALONE over the same inputs, and
asks `PureWindowsPath`/`PurePosixPath` whether the result is still absolute. That is what
separated "the scrubber eats URLs" from "MY rule eats URLs, the reviewer's is innocent."
`redcheck_s66.py` — restores the REVIEWED blob over the edited script in an isolated
packet copy via `git cat-file`, keeps the new test file, runs the focused suite there.
**Do not exclude `results/` from the copy** — the cell-6 pin test reads
`stage_abc_screen.json` and its absence looked like a seventh red test until I fixed the
harness. 6 of 6 red against `eb94afb2`; all 47 of Codex's green.
`sweep_s66.py` — the mutation sweep, fresh copytree per case, two passes required to
agree, both Lesson-63 double removals included. **Anchors must be unique**: the two
console-report cases both delete a byte-identical `print(f"FAILED: {error}")` line, so
each anchor carries its following `try:` block.
`append_s66.py` / `rewrite_soonc_s66.py` / `rewrite_soonc_s66b.py` — the chat appender
(asserts the pre-write prefix INSIDE the writer) and this file's own rewrite (every
anchor asserted to occur exactly once). `turn_s66.md`.

## Scratchpad (S65, superseded)

`probe_s65_replay_source.py` — **the instrument that turned a reading into a
measurement.** Drives every step of the replay gate that PRECEDES its one rollout and
stops there, printing both candidate scenario ids side by side with the pair id each
produces and the delivered row's. *The general move: when you suspect a selection is
wrong, run the selection for BOTH candidates in one output rather than arguing from the
source.* Zero rollouts by construction — `rollout_spent = 1` is set after every check it
runs.
`redcheck_s65.py` — **the one to rebuild first.** Copies the packet to a temp dir,
restores the REVIEWED blob over the edited script via `git cat-file`, keeps the new test
file, and runs the focused suite there. That is what turns "I added tests" into "7 of 9
are red against the state I reviewed, and the owner's 36 still pass." A test added during
review is the least likely test in the codebase to have a state that makes it fail.
`sweep_s65.py` — the mutation sweep, isolated packet copy per case, two passes required
to agree. **Its verdict must carry NOTHING that varies between passes** — I embedded
pytest's timing line and made the S60 two-pass detector report disagreement on every
clean sweep. Carries a DOUBLE-removal case (Lesson 63).
`append_s65.py` / `readme_entry_s65.py` / `rewrite_soonc_s65.py` / `rewrite_soonc_s65b.py`
— the chat appender (asserts the pre-write prefix INSIDE the writer), the root-README
inserter (asserts the four-line anchor block occurs exactly once), and this file's own
rewrite (every anchor asserted unique). `turn_s65.md`.

## Scratchpad (S64, superseded)

`probe_s64_rowkey.py` — **the instrument that turned an argument into a measurement, and
the one to rebuild.** Builds the extension's exact §5/§6 CRN shape as `LogicalRow`s and
prints how many distinct `PhysicalKey`s they resolve to (18, against the document's 126),
then drives the same two rows through `ResultsLedger.record` so the refusal message is on
the record rather than predicted. *The general move: when a design says an object
distinguishes N things, build the N things and count.*
`sweep_s64.py` — the mutation sweep, and the first one I have run against **isolated
packet copies** rather than in-place with a restore. One `shutil.copytree` per case, so
the working tree is never mutated at all and there is nothing to restore; combined with
`PYTHONDONTWRITEBYTECODE=1` and a `__pycache__` clear it sidesteps the S60 bytecode
mechanism by construction. Ten cases, two passes, ~35 s total. Reusable against any two
packet files at once — point it at a case list and a focused test set.
`append_s64.py` — the chat appender, asserting the pre-write prefix INSIDE the writer.
`readme_entry_s64.py` — the root-README inserter, asserting both anchors before writing.
`rewrite_soonc_s64.py` / `rewrite_soonc_s64b.py` — this file's own rewrite, with every
edit asserting its anchor occurs exactly once so a stale anchor stops the rewrite instead
of silently doing nothing.
`turn_s64.md`, `soonc_head_s64.md`, `readme_entry_s64.md`.

## Scratchpad (S63, superseded)

`probe_s63_facts.py` — **the cheapest instrument in this session and the one to rebuild.** Reads `ScreenOverrides` and `PhysicalKey` field lists **by AST over the committed source** (never by import, so no `mujoco` and no side effects), pulls the anchor reservation's payload through `expand_reservations`, and re-derives every count the document asserts. That is how three of Codex's five findings were confirmed as FACTS rather than as reasoning, in one run.
`probe_s63_licensing.py` — enumerates all 19,448 monotone prefix states, partitions them by the classifier, and compares what R10 and R11 each LICENSE for the same evidence. *The general move: when a rule is stated in two places, enumerate the space and diff the two statements' outputs rather than reading them side by side.* Reusable for any future outcome-rule edit; the anomaly test to keep is “does deleting a result ever raise the licensed cap?”
`append_s63.py` — the chat appender, asserting the pre-write prefix INSIDE the writer (open `r+b`, re-read, compare, then seek to end) so nothing can slip between check and write; verifies prefix SHA-256, header uniqueness, and physically-last afterwards.
`turn_s63.md`, `soonc_head_s63.md`, `v02_review_diff.txt`.

## Scratchpad (S62, superseded)

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
